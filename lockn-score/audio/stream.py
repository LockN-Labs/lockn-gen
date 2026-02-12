"""Microphone audio stream utilities using sounddevice.

This module provides a low-latency audio capture generator suitable for
real-time bounce detection. It yields numpy arrays plus the capture
start time in seconds (monotonic).
"""
from __future__ import annotations

import queue
import time
from dataclasses import dataclass
from typing import Generator, Optional, Tuple

import numpy as np

try:
    import sounddevice as sd
except Exception as exc:  # pragma: no cover - optional dependency
    sd = None  # type: ignore
    _sounddevice_error = exc
else:
    _sounddevice_error = None

from .config import AudioConfig, DEFAULT_CONFIG


@dataclass
class AudioChunk:
    data: np.ndarray
    timestamp: float  # monotonic time (seconds)


class MicStream:
    """Low-latency microphone input stream.

    Example:
        stream = MicStream()
        for chunk in stream.chunks():
            process(chunk.data, chunk.timestamp)
    """

    def __init__(self, config: AudioConfig = DEFAULT_CONFIG, device: Optional[int] = None):
        self.config = config
        self.device = device
        self._queue: "queue.Queue[AudioChunk]" = queue.Queue(maxsize=32)
        self._stream: Optional[sd.InputStream] = None

        if sd is None:
            raise RuntimeError(
                f"sounddevice not available: {_sounddevice_error}. "
                "Install with: pip install sounddevice"
            )

    def _callback(self, indata, frames, time_info, status):  # type: ignore[override]
        if status:
            # Drop or log? For now we just continue.
            pass
        # Flatten to mono if needed
        if indata.ndim > 1:
            data = indata.mean(axis=1)
        else:
            data = indata
        timestamp = time.perf_counter()
        try:
            self._queue.put_nowait(AudioChunk(data.copy(), timestamp))
        except queue.Full:
            # Drop oldest to keep latency low
            try:
                _ = self._queue.get_nowait()
            except queue.Empty:
                pass
            try:
                self._queue.put_nowait(AudioChunk(data.copy(), timestamp))
            except queue.Full:
                pass

    def start(self) -> None:
        if self._stream is not None:
            return
        blocksize = int(self.config.sample_rate * self.config.block_seconds)
        self._stream = sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            dtype=self.config.dtype,
            blocksize=blocksize,
            device=self.device,
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is None:
            return
        self._stream.stop()
        self._stream.close()
        self._stream = None

    def chunks(self) -> Generator[AudioChunk, None, None]:
        """Yield audio chunks (non-blocking)."""
        self.start()
        while True:
            chunk = self._queue.get()
            yield chunk


def mic_chunks(config: AudioConfig = DEFAULT_CONFIG) -> Generator[Tuple[np.ndarray, float], None, None]:
    """Convenience generator yielding (data, timestamp)."""
    stream = MicStream(config=config)
    for chunk in stream.chunks():
        yield chunk.data, chunk.timestamp
