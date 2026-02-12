"""Fusion engine combining YOLOv8 vision and PANNs audio."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from .config import FusionConfig
from .rally_tracker import BallDetection, BounceEvent, RallyStatus, RallyTracker


@dataclass
class FusionOutput:
    status: RallyStatus
    last_event: Optional[str] = None


class FusionEngine:
    """Fusion engine entry point.

    Feed audio and vision events via `process_audio` / `process_vision`.
    """

    def __init__(self, config: Optional[FusionConfig] = None) -> None:
        self.config = config or FusionConfig()
        self.tracker = RallyTracker(self.config)

    def reset(self) -> None:
        self.tracker.reset()

    def process_vision(
        self,
        timestamp: Optional[float],
        x: float,
        y: float,
        confidence: float,
    ) -> FusionOutput:
        ts = timestamp if timestamp is not None else time.time()
        status = self.tracker.update_vision(BallDetection(ts, x, y, confidence))
        return FusionOutput(status=status, last_event="vision")

    def process_audio(
        self, timestamp: Optional[float], confidence: float
    ) -> FusionOutput:
        ts = timestamp if timestamp is not None else time.time()
        status = self.tracker.update_audio(BounceEvent(ts, confidence))
        return FusionOutput(status=status, last_event="audio")

    def tick(self, timestamp: Optional[float] = None) -> FusionOutput:
        ts = timestamp if timestamp is not None else time.time()
        status = self.tracker.tick(ts)
        return FusionOutput(status=status, last_event="tick")
