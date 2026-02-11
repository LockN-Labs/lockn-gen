from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


class EscalationTelemetry:
    def __init__(self, path: str | Path = "logs/escalation_telemetry.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, record: Dict[str, Any]) -> None:
        envelope = {
            "ts": datetime.now(timezone.utc).isoformat(),
            **record,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(envelope, ensure_ascii=False) + "\n")
