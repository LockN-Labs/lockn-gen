"""Voice command configuration for LockN Score."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class VoiceConfig:
    """Configuration for voice command listening and parsing."""

    # Audio capture
    sample_rate: int = 16000
    channels: int = 1
    chunk_ms: int = 30
    min_record_ms: int = 350
    max_record_ms: int = 5000

    # Simple energy-based VAD
    min_rms: float = 0.008
    silence_timeout_ms: int = 700

    # Whisper
    whisper_endpoint: str = "http://localhost:8880/v1/audio/transcriptions"
    whisper_language: str = "en"
    whisper_temperature: float = 0.0
    whisper_response_field: str = "text"

    # Confidence / noise rejection
    min_confidence: float = 0.5

    # Optional wake word (None disables)
    wake_word: Optional[str] = None

    # WebSocket broadcast
    websocket_url: str = "ws://localhost:8765/ws"

    # Command aliases/phrases
    command_aliases: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "reset": ["reset", "reset rally", "clear"],
            "new_game": ["new game", "new match", "start over"],
            "pause": ["pause", "hold"],
            "resume": ["resume", "continue"],
            "undo": ["undo", "take back"],
            "score": ["score", "what's the score", "what is the score"],
        }
    )
