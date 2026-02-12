"""Command parsing + dispatch for voice commands."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Optional

from .config import VoiceConfig


@dataclass
class VoiceCommand:
    action: str
    raw_text: str
    confidence: float
    player_name: Optional[str] = None


def _normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s']+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def parse_command(text: str, confidence: float, cfg: VoiceConfig) -> Optional[VoiceCommand]:
    """Parse a transcription into a VoiceCommand.

    Returns None if no command recognized or confidence too low.
    """

    if confidence < cfg.min_confidence:
        return None

    normalized = _normalize(text)

    if cfg.wake_word:
        wake = _normalize(cfg.wake_word)
        if not normalized.startswith(wake + " ") and normalized != wake:
            return None
        normalized = normalized[len(wake) :].strip()

    if not normalized:
        return None

    # Point command
    match = re.match(r"point\s+(.+)$", normalized)
    if match:
        player = match.group(1).strip()
        if player:
            return VoiceCommand(action="point", raw_text=text, confidence=confidence, player_name=player)

    # Alias based commands
    for action, phrases in cfg.command_aliases.items():
        for phrase in phrases:
            if normalized == _normalize(phrase):
                return VoiceCommand(action=action, raw_text=text, confidence=confidence)

    return None


class CommandDispatcher:
    """Dispatch parsed commands to callbacks."""

    def __init__(
        self,
        on_point: Optional[Callable[[str], None]] = None,
        on_reset: Optional[Callable[[], None]] = None,
        on_new_game: Optional[Callable[[], None]] = None,
        on_pause: Optional[Callable[[], None]] = None,
        on_resume: Optional[Callable[[], None]] = None,
        on_undo: Optional[Callable[[], None]] = None,
        on_score: Optional[Callable[[], None]] = None,
    ) -> None:
        self.on_point = on_point
        self.on_reset = on_reset
        self.on_new_game = on_new_game
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.on_undo = on_undo
        self.on_score = on_score

    def dispatch(self, command: VoiceCommand) -> None:
        if command.action == "point" and self.on_point:
            self.on_point(command.player_name or "")
        elif command.action == "reset" and self.on_reset:
            self.on_reset()
        elif command.action == "new_game" and self.on_new_game:
            self.on_new_game()
        elif command.action == "pause" and self.on_pause:
            self.on_pause()
        elif command.action == "resume" and self.on_resume:
            self.on_resume()
        elif command.action == "undo" and self.on_undo:
            self.on_undo()
        elif command.action == "score" and self.on_score:
            self.on_score()
