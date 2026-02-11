from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict


class OrchestrationMode(str, Enum):
    CLOUD_FIRST = "cloud-first"
    LOCAL_FIRST = "local-first"
    HYBRID = "hybrid"


@dataclass
class ModeStatus:
    mode: OrchestrationMode
    guardrails_enabled: bool
    updated_at: str | None
    updated_by: str | None


class RuntimeModeStore:
    """File-backed runtime mode toggle (no redeploy)."""

    def __init__(self, path: str | Path = ".runs/lockn511_runtime_mode.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _default(self) -> Dict[str, Any]:
        return {
            "mode": OrchestrationMode.HYBRID.value,
            "guardrails_enabled": False,
            "updated_at": None,
            "updated_by": None,
        }

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            data = self._default()
            self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return data
        return json.loads(self.path.read_text(encoding="utf-8"))

    def get_status(self) -> ModeStatus:
        data = self._load()
        mode = OrchestrationMode(data.get("mode", OrchestrationMode.HYBRID.value))
        return ModeStatus(
            mode=mode,
            guardrails_enabled=bool(data.get("guardrails_enabled", False)),
            updated_at=data.get("updated_at"),
            updated_by=data.get("updated_by"),
        )

    def set_mode(self, mode: str, actor: str = "system") -> ModeStatus:
        target = OrchestrationMode(mode)
        data = self._load()
        data["mode"] = target.value
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        data["updated_by"] = actor
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return self.get_status()

    def set_guardrails_enabled(self, enabled: bool, actor: str = "system") -> ModeStatus:
        data = self._load()
        data["guardrails_enabled"] = bool(enabled)
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        data["updated_by"] = actor
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return self.get_status()
