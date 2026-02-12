"""FastAPI endpoints for rally score state."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from src.fusion.engine import FusionEngine
from src.fusion.rally_tracker import RallyState

app = FastAPI(title="LockN Score API")
engine = FusionEngine()


class VisionPayload(BaseModel):
    timestamp: Optional[float] = None
    x: float
    y: float
    confidence: float


class AudioPayload(BaseModel):
    timestamp: Optional[float] = None
    confidence: float


class ScoreState(BaseModel):
    state: RallyState
    rally_count: int
    last_bounce_ts: Optional[float]
    last_ball_ts: Optional[float]


@app.get("/score/state", response_model=ScoreState)
def get_state() -> ScoreState:
    status = engine.tracker.get_status()
    return ScoreState(**status.__dict__)


@app.post("/score/vision", response_model=ScoreState)
def post_vision(payload: VisionPayload) -> ScoreState:
    output = engine.process_vision(
        payload.timestamp, payload.x, payload.y, payload.confidence
    )
    status = output.status
    return ScoreState(**status.__dict__)


@app.post("/score/audio", response_model=ScoreState)
def post_audio(payload: AudioPayload) -> ScoreState:
    output = engine.process_audio(payload.timestamp, payload.confidence)
    status = output.status
    return ScoreState(**status.__dict__)


@app.post("/score/tick", response_model=ScoreState)
def post_tick(timestamp: Optional[float] = None) -> ScoreState:
    output = engine.tick(timestamp)
    status = output.status
    return ScoreState(**status.__dict__)


@app.post("/score/reset")
def post_reset() -> dict:
    engine.reset()
    return {"ok": True}
