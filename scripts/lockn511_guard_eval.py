#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.safety_router.router_guard import SafetyRouterGuard
from tools.safety_router.telemetry import EscalationTelemetry


def main() -> int:
    parser = argparse.ArgumentParser(description="LOCKN-511 safety guard evaluator")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--action", default="")
    parser.add_argument("--intent", default="")
    parser.add_argument("--payload", default="{}", help="JSON payload")
    parser.add_argument("--telemetry", default="logs/escalation_telemetry.jsonl")
    parser.add_argument("--local-orchestrator", action="store_true", default=True)
    args = parser.parse_args()

    payload: Dict[str, Any] = json.loads(args.payload)
    guard = SafetyRouterGuard()
    telemetry = EscalationTelemetry(args.telemetry)

    decision = guard.evaluate(
        tool=args.tool,
        action=args.action,
        intent=args.intent,
        payload=payload,
        local_orchestrator=args.local_orchestrator,
    )

    record = {
        "reason": "; ".join(decision.reasons),
        "trigger": decision.triggers,
        "selected_model": decision.selected_model_tier,
        "outcome": decision.outcome,
        "risk": decision.risk,
        "tool": args.tool,
        "action": args.action,
    }
    telemetry.log(record)
    print(json.dumps(guard.to_dict(decision), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
