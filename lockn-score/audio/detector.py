"""PANNs-based ping pong bounce detector.

Implementation notes / research:
- PANNs (Kong et al. 2019) provide pretrained CNNs for AudioSet tagging.
- Cnn14 is highest-performing but heavier; Cnn6 is lighter/faster for
  real-time (<50ms hop). We default to Cnn6 with 1s windows and 50ms hop.
- AudioSet does not include a "ping pong" class. Closest label is
  "Basketball bounce" plus generic impact/thump classes. We combine
  probabilities from these labels to detect bounces.

Fine-tuning approach (recommended for higher precision):
1) Collect ping pong bounce clips + negative ambient noise.
2) Use PANNs transfer learning (Transfer_Cnn14 or Transfer_Cnn6)
   from the audioset_tagging_cnn repo. Replace last layer with
   bounce/no-bounce classes and fine-tune with your dataset.
3) Export fine-tuned checkpoint and load it here.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, List, Optional

import numpy as np

try:
    import torch
    from panns_inference import AudioTagging, labels as panns_labels
except Exception as exc:  # pragma: no cover
    torch = None  # type: ignore
    AudioTagging = None  # type: ignore
    panns_labels = None  # type: ignore
    _panns_error = exc
else:
    _panns_error = None

from .config import AudioConfig, DEFAULT_CONFIG


@dataclass
class BounceEvent:
    timestamp: float
    score: float


class BounceDetector:
    def __init__(self, config: AudioConfig = DEFAULT_CONFIG, device: Optional[str] = None):
        self.config = config
        self.device = device or ("cuda" if torch and torch.cuda.is_available() else "cpu")

        if AudioTagging is None:
            raise RuntimeError(
                f"panns_inference not available: {_panns_error}. "
                "Install with: pip install panns-inference torch torchaudio"
            )

        # Load PANNs model
        self.model = AudioTagging(checkpoint_path=None, device=self.device, model_type=self.config.model_name)
        self.label_map = {name: idx for idx, name in enumerate(panns_labels)}
        self.target_indices = [
            self.label_map[name] for name in self.config.target_labels if name in self.label_map
        ]
        if not self.target_indices:
            raise RuntimeError("No target labels found in PANNs label list.")

        self._buffer: List[np.ndarray] = []
        self._buffer_samples: int = 0
        self._last_fire_time: float = -1.0
        self._samples_seen: int = 0

        self._window_samples = int(self.config.sample_rate * self.config.window_seconds)
        self._hop_samples = int(self.config.sample_rate * self.config.hop_seconds)

    def _append_audio(self, audio: np.ndarray) -> None:
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        self._buffer.append(audio.astype(np.float32, copy=False))
        self._buffer_samples += len(audio)

    def _pop_window(self) -> Optional[np.ndarray]:
        if self._buffer_samples < self._window_samples:
            return None
        # Concatenate only as needed
        data = np.concatenate(self._buffer)
        window = data[: self._window_samples]
        remaining = data[self._hop_samples :]
        self._buffer = [remaining] if len(remaining) else []
        self._buffer_samples = len(remaining)
        return window

    def process_chunk(self, audio: np.ndarray) -> List[BounceEvent]:
        """Process a chunk of audio and return any bounce detections."""
        self._append_audio(audio)
        events: List[BounceEvent] = []
        while True:
            window = self._pop_window()
            if window is None:
                break
            # PANNs expects batch shape (1, samples)
            window = window.reshape(1, -1)
            with torch.no_grad():
                _, clipwise_output = self.model.inference(window)
            scores = clipwise_output[0]
            score = float(np.max(scores[self.target_indices]))

            current_time = time.perf_counter()
            if score >= self.config.bounce_threshold:
                if self._last_fire_time < 0 or (current_time - self._last_fire_time) >= self.config.cooldown_seconds:
                    timestamp = self._samples_seen / self.config.sample_rate
                    events.append(BounceEvent(timestamp=timestamp, score=score))
                    self._last_fire_time = current_time
            self._samples_seen += self._hop_samples
        return events


def detect_bounces_from_stream(stream: Iterable[np.ndarray], config: AudioConfig = DEFAULT_CONFIG) -> Iterable[BounceEvent]:
    detector = BounceDetector(config=config)
    for chunk in stream:
        for event in detector.process_chunk(chunk):
            yield event


if __name__ == "__main__":
    # Example real-time run from microphone
    from .stream import mic_chunks

    cfg = DEFAULT_CONFIG
    detector = BounceDetector(config=cfg)
    print("Listening for bounce events...")
    for data, _ in mic_chunks(cfg):
        events = detector.process_chunk(data)
        for event in events:
            print(f"BOUNCE @ {event.timestamp:.3f}s (score={event.score:.3f})")
