"""Fusion configuration for audio/vision rally detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class FusionConfig:
    """Configuration values for fusion and rally tracking.

    All time values are in milliseconds to make tuning easy.
    """

    # Vision parameters
    vision_confidence_threshold: float = 0.4
    vision_timeout_ms: int = 500  # end rally if ball not seen recently

    # Audio parameters
    audio_confidence_threshold: float = 0.35
    audio_window_ms: int = 120  # window to align audio bounce with vision
    min_bounce_interval_ms: int = 180  # debounce audio bounce events

    # Fusion heuristics
    allow_audio_only_ms: int = 400  # allow audio-only bounce if vision recently seen
    allow_vision_only: bool = True
    vision_only_audio_silence_ms: int = 1000  # if no audio, allow vision-only bounces

    # Rally lifecycle
    rally_timeout_ms: int = 2500  # end rally if no bounces for this long

    # Table bounding box (normalized coordinates [0,1])
    # (x_min, y_min, x_max, y_max)
    table_bbox: Tuple[float, float, float, float] = (0.1, 0.2, 0.9, 0.8)
