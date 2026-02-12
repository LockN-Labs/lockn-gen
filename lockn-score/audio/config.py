"""Audio configuration for bounce detection.

Notes on PANNs:
- PANNs models (Cnn14/Cnn6/Wavegram-Logmel) are trained on AudioSet
  at 32 kHz with log-mel features (64 bins). Cnn14 is the strongest
  baseline (higher mAP, heavier), while Cnn6 is lighter/faster. For
  low-latency streaming, we default to Cnn6 and allow Cnn14 when GPU
  latency is acceptable.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioConfig:
    # Core audio settings
    sample_rate: int = 32000
    channels: int = 1
    dtype: str = "float32"

    # Streaming windowing
    # We run inference on a 1.0s rolling window for stability, but hop
    # every 50ms to satisfy <50ms detection latency.
    window_seconds: float = 1.0
    hop_seconds: float = 0.05

    # SoundDevice block size: keep small to reduce input latency.
    # 32000 * 0.02 = 640 frames ≈ 20ms block.
    block_seconds: float = 0.02

    # Detection thresholds
    bounce_threshold: float = 0.35
    cooldown_seconds: float = 0.08

    # Model choice
    model_name: str = "Cnn6"  # alternatives: "Cnn14", "Wavegram_Logmel_Cnn14"

    # Target AudioSet labels used for bounce detection.
    # "Basketball bounce" is the closest explicit class. We add impact
    # sounds to improve recall in noisy environments.
    target_labels: tuple[str, ...] = (
        "Basketball bounce",
        "Thump, thud",
        "Generic impact sounds",
        "Specific impact sounds",
        "Burst, pop",
    )


DEFAULT_CONFIG = AudioConfig()
