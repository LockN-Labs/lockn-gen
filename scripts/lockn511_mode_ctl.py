#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.safety_router.mode import RuntimeModeStore
from tools.safety_router.telemetry import EscalationTelemetry


def main() -> int:
    parser = argparse.ArgumentParser(description="LOCKN-511 runtime orchestration mode control")
    sub = parser.add_subparsers(dest="cmd", required=True)

    status_p = sub.add_parser("status")
    status_p.add_argument("--state-file", default=".runs/lockn511_runtime_mode.json")

    set_mode_p = sub.add_parser("set-mode")
    set_mode_p.add_argument("mode", choices=["cloud-first", "local-first", "hybrid"])
    set_mode_p.add_argument("--actor", default="operator")
    set_mode_p.add_argument("--state-file", default=".runs/lockn511_runtime_mode.json")
    set_mode_p.add_argument("--telemetry", default="logs/escalation_telemetry.jsonl")

    set_guard_p = sub.add_parser("set-guardrails")
    set_guard_p.add_argument("enabled", choices=["on", "off"])
    set_guard_p.add_argument("--actor", default="operator")
    set_guard_p.add_argument("--state-file", default=".runs/lockn511_runtime_mode.json")
    set_guard_p.add_argument("--telemetry", default="logs/escalation_telemetry.jsonl")

    args = parser.parse_args()
    store = RuntimeModeStore(args.state_file)

    if args.cmd == "status":
        status = store.get_status()
        print(json.dumps({
            "mode": status.mode.value,
            "guardrails_enabled": status.guardrails_enabled,
            "updated_at": status.updated_at,
            "updated_by": status.updated_by,
        }, indent=2))
        return 0

    telemetry = EscalationTelemetry(args.telemetry)

    if args.cmd == "set-mode":
        before = store.get_status()
        after = store.set_mode(args.mode, actor=args.actor)
        telemetry.log(
            {
                "event": "lockn511_mode_change",
                "actor": args.actor,
                "before_mode": before.mode.value,
                "after_mode": after.mode.value,
                "guardrails_enabled": after.guardrails_enabled,
                "outcome": "applied",
            }
        )
    elif args.cmd == "set-guardrails":
        enabled = args.enabled == "on"
        before = store.get_status()
        after = store.set_guardrails_enabled(enabled, actor=args.actor)
        telemetry.log(
            {
                "event": "lockn511_guardrails_toggle",
                "actor": args.actor,
                "before_enabled": before.guardrails_enabled,
                "after_enabled": after.guardrails_enabled,
                "mode": after.mode.value,
                "outcome": "applied",
            }
        )
    else:
        return 2

    print(
        json.dumps(
            {
                "mode": after.mode.value,
                "guardrails_enabled": after.guardrails_enabled,
                "updated_at": after.updated_at,
                "updated_by": after.updated_by,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
