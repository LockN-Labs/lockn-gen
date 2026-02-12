"""Continuous audio listener that runs Whisper + command parsing."""

from __future__ import annotations

import base64
import io
import json
import logging
import threading
import time
import wave
from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np

from .commands import CommandDispatcher, VoiceCommand, parse_command
from .config import VoiceConfig

logger = logging.getLogger(__name__)

try:  # Optional dependency
    import sounddevice as sd
except Exception:  # pragma: no cover - optional
    sd = None

try:  # Optional dependency
    import requests
except Exception:  # pragma: no cover - optional
    requests = None

try:  # Optional dependency
    import websocket
except Exception:  # pragma: no cover - optional
    websocket = None


@dataclass
class TranscriptionResult:
    text: str
    confidence: float
    raw: Dict[str, Any]


class WebSocketBroadcaster:
    def __init__(self, url: str) -> None:
        self.url = url
        self._lock = threading.Lock()
        self._ws = None

    def _ensure(self) -> None:
        if websocket is None:
            raise RuntimeError("websocket-client is not installed")
        with self._lock:
            if self._ws is None:
                self._ws = websocket.create_connection(self.url, timeout=2)

    def send(self, payload: Dict[str, Any]) -> None:
        try:
            self._ensure()
            assert self._ws is not None
            self._ws.send(json.dumps(payload))
        except Exception as exc:  # pragma: no cover
            logger.warning("WebSocket send failed: %s", exc)
            with self._lock:
                try:
                    if self._ws:
                        self._ws.close()
                finally:
                    self._ws = None


class WhisperClient:
    def __init__(self, cfg: VoiceConfig) -> None:
        self.cfg = cfg

    def transcribe(self, audio: np.ndarray, sample_rate: int) -> TranscriptionResult:
        if requests is None:
            raise RuntimeError("requests is required for WhisperClient")

        wav_data = self._to_wav(audio, sample_rate)
        endpoint = self.cfg.whisper_endpoint

        if endpoint.rstrip("/").endswith("/v1/audio/transcriptions"):
            files = {
                "file": ("audio.wav", wav_data, "audio/wav"),
            }
            data = {
                "model": "whisper-1",
                "language": self.cfg.whisper_language,
                "temperature": str(self.cfg.whisper_temperature),
                "response_format": "json",
            }
            response = requests.post(endpoint, files=files, data=data, timeout=10)
            response.raise_for_status()
            payload = response.json()
        else:
            b64 = base64.b64encode(wav_data).decode("utf-8")
            payload = {
                "language": self.cfg.whisper_language,
                "temperature": self.cfg.whisper_temperature,
                "audio_data": b64,
            }
            response = requests.post(endpoint, json=payload, timeout=10)
            response.raise_for_status()
            payload = response.json()

        text = payload.get(self.cfg.whisper_response_field) or payload.get("text") or ""
        confidence = _extract_confidence(payload)
        return TranscriptionResult(text=text, confidence=confidence, raw=payload)

    @staticmethod
    def _to_wav(audio: np.ndarray, sample_rate: int) -> bytes:
        audio = np.clip(audio, -1.0, 1.0)
        int16 = (audio * 32767).astype(np.int16)
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(int16.tobytes())
        return buf.getvalue()


def _extract_confidence(payload: Dict[str, Any]) -> float:
    if "confidence" in payload:
        try:
            return float(payload["confidence"])
        except Exception:
            pass
    segments = payload.get("segments") or []
    if segments:
        avg = np.mean([seg.get("avg_logprob", -1.0) for seg in segments])
        try:
            return float(np.exp(avg))
        except Exception:
            return 0.5
    return 0.5


class VoiceListener:
    def __init__(
        self,
        cfg: VoiceConfig,
        dispatcher: Optional[CommandDispatcher] = None,
        broadcaster: Optional[WebSocketBroadcaster] = None,
    ) -> None:
        if sd is None:
            raise RuntimeError("sounddevice is required for VoiceListener")
        self.cfg = cfg
        self.dispatcher = dispatcher or CommandDispatcher()
        self.broadcaster = broadcaster
        self.whisper = WhisperClient(cfg)
        self._queue: "queue.Queue[np.ndarray]" = __import__("queue").Queue()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._stream: Optional[sd.InputStream] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._stream = sd.InputStream(
            samplerate=self.cfg.sample_rate,
            channels=self.cfg.channels,
            dtype="float32",
            callback=self._on_audio,
        )
        self._stream.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None

    def _on_audio(self, indata, frames, time_info, status) -> None:  # pragma: no cover - callback
        if status:
            logger.debug("Audio status: %s", status)
        mono = indata[:, 0].copy()
        self._queue.put(mono)

    def _run(self) -> None:
        chunk_ms = self.cfg.chunk_ms
        silence_limit = self.cfg.silence_timeout_ms / 1000.0
        min_samples = int(self.cfg.sample_rate * self.cfg.min_record_ms / 1000)
        max_samples = int(self.cfg.sample_rate * self.cfg.max_record_ms / 1000)
        buffer: list[np.ndarray] = []
        recording = False
        last_voice = 0.0

        while not self._stop_event.is_set():
            try:
                chunk = self._queue.get(timeout=0.1)
            except Exception:
                continue

            rms = float(np.sqrt(np.mean(chunk**2)))
            now = time.time()

            if rms >= self.cfg.min_rms:
                if not recording:
                    recording = True
                    buffer = []
                buffer.append(chunk)
                last_voice = now
            elif recording:
                buffer.append(chunk)
                if now - last_voice >= silence_limit:
                    recording = False
                    audio = np.concatenate(buffer) if buffer else np.array([], dtype=np.float32)
                    if audio.size >= min_samples:
                        audio = audio[:max_samples]
                        self._handle_audio(audio)
                    buffer = []

            # Avoid unbounded buffer in long noise
            if recording and sum(len(c) for c in buffer) > max_samples:
                audio = np.concatenate(buffer)[:max_samples]
                recording = False
                buffer = []
                self._handle_audio(audio)

    def _handle_audio(self, audio: np.ndarray) -> None:
        try:
            result = self.whisper.transcribe(audio, self.cfg.sample_rate)
        except Exception as exc:  # pragma: no cover
            logger.warning("Whisper failed: %s", exc)
            return

        text = result.text.strip()
        if not text:
            return

        if self.broadcaster:
            self.broadcaster.send(
                {
                    "type": "voice_heard",
                    "text": text,
                    "confidence": result.confidence,
                }
            )

        command = parse_command(text, result.confidence, self.cfg)
        if command:
            if self.broadcaster:
                self.broadcaster.send(
                    {
                        "type": "voice_command",
                        "command": command.action,
                        "player": command.player_name,
                        "text": command.raw_text,
                        "confidence": command.confidence,
                    }
                )
            self.dispatcher.dispatch(command)


__all__ = [
    "VoiceListener",
    "WebSocketBroadcaster",
    "WhisperClient",
    "TranscriptionResult",
]
