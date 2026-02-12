"""Rally tracking state machine."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .config import FusionConfig


class RallyState(str, Enum):
    IDLE = "IDLE"
    IN_PLAY = "IN_PLAY"
    ENDED = "ENDED"


@dataclass
class BallDetection:
    """Vision detection for the ball."""

    timestamp: float  # seconds
    x: float
    y: float
    confidence: float


@dataclass
class BounceEvent:
    """Audio bounce event."""

    timestamp: float  # seconds
    confidence: float


@dataclass
class RallyStatus:
    state: RallyState
    rally_count: int
    last_bounce_ts: Optional[float]
    last_ball_ts: Optional[float]


class RallyTracker:
    """State machine for rally tracking using fused audio/vision input."""

    def __init__(self, config: FusionConfig) -> None:
        self.config = config
        self.state = RallyState.IDLE
        self.rally_count = 0
        self.last_bounce_ts: Optional[float] = None
        self.last_ball_ts: Optional[float] = None
        self.last_audio_ts: Optional[float] = None

    def reset(self) -> None:
        self.state = RallyState.IDLE
        self.rally_count = 0
        self.last_bounce_ts = None
        self.last_ball_ts = None
        self.last_audio_ts = None

    def get_status(self) -> RallyStatus:
        return RallyStatus(
            state=self.state,
            rally_count=self.rally_count,
            last_bounce_ts=self.last_bounce_ts,
            last_ball_ts=self.last_ball_ts,
        )

    def update_vision(self, detection: BallDetection) -> RallyStatus:
        """Update state machine from a vision detection."""
        if detection.confidence < self.config.vision_confidence_threshold:
            return self.get_status()

        in_table = self._in_table(detection.x, detection.y)
        self.last_ball_ts = detection.timestamp

        if self.state == RallyState.IDLE:
            if in_table:
                self.state = RallyState.IN_PLAY
            return self.get_status()

        if self.state == RallyState.IN_PLAY:
            if not in_table:
                # Ball left table area
                self.state = RallyState.ENDED
                return self.get_status()

            # Vision-only bounce heuristic
            if (
                self.config.allow_vision_only
                and self._audio_silent(detection.timestamp)
                and self._bounce_interval_ok(detection.timestamp)
            ):
                self._count_bounce(detection.timestamp)

        return self.get_status()

    def update_audio(self, bounce: BounceEvent) -> RallyStatus:
        """Update state machine from an audio bounce event."""
        if bounce.confidence < self.config.audio_confidence_threshold:
            return self.get_status()

        self.last_audio_ts = bounce.timestamp

        if not self._bounce_interval_ok(bounce.timestamp):
            return self.get_status()

        if self.state == RallyState.IDLE:
            # Wait for vision confirmation to start
            return self.get_status()

        if self.state == RallyState.IN_PLAY:
            if self._audio_confirmed_by_vision(bounce.timestamp):
                self._count_bounce(bounce.timestamp)

        return self.get_status()

    def tick(self, now_ts: float) -> RallyStatus:
        """Periodic update for timeouts."""
        if self.state == RallyState.IN_PLAY:
            if self.last_ball_ts is not None:
                if (now_ts - self.last_ball_ts) * 1000 > self.config.vision_timeout_ms:
                    self.state = RallyState.ENDED
            if self.last_bounce_ts is not None:
                if (now_ts - self.last_bounce_ts) * 1000 > self.config.rally_timeout_ms:
                    self.state = RallyState.ENDED
        return self.get_status()

    def _count_bounce(self, ts: float) -> None:
        self.rally_count += 1
        self.last_bounce_ts = ts

    def _in_table(self, x: float, y: float) -> bool:
        x_min, y_min, x_max, y_max = self.config.table_bbox
        return x_min <= x <= x_max and y_min <= y <= y_max

    def _audio_confirmed_by_vision(self, bounce_ts: float) -> bool:
        """Confirm audio bounce with recent vision signal."""
        if self.last_ball_ts is None:
            return False
        delta_ms = abs(bounce_ts - self.last_ball_ts) * 1000
        return delta_ms <= self.config.audio_window_ms

    def _audio_silent(self, now_ts: float) -> bool:
        if self.last_audio_ts is None:
            return True
        return (now_ts - self.last_audio_ts) * 1000 > self.config.vision_only_audio_silence_ms

    def _bounce_interval_ok(self, ts: float) -> bool:
        if self.last_bounce_ts is None:
            return True
        return (ts - self.last_bounce_ts) * 1000 >= self.config.min_bounce_interval_ms
