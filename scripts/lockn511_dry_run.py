#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.safety_router.router_guard import SafetyRouterGuard
from tools.safety_router.telemetry import EscalationTelemetry


def load_tasks(path: Path) -> List[Dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Task sample file must be a JSON array")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description="LOCKN-511 dry run simulation")
    parser.add_argument("--input", default="docs/operations/lockn511-sample-tasks.json")
    parser.add_argument("--report", default="docs/operations/lockn511-dry-run-report.md")
    parser.add_argument("--telemetry", default="logs/escalation_telemetry.jsonl")
    args = parser.parse_args()

    guard = SafetyRouterGuard()
    telemetry = EscalationTelemetry(args.telemetry)

    tasks = load_tasks(Path(args.input))
    counters = Counter()
    rows: List[str] = []

    for i, t in enumerate(tasks, start=1):
        decision = guard.evaluate(
            tool=t.get("tool", "unknown"),
            action=t.get("action", ""),
            intent=t.get("intent", ""),
            payload=t.get("payload", {}),
            local_orchestrator=True,
        )
        counters[decision.risk] += 1
        counters[f"route:{decision.route}"] += 1
        counters[f"outcome:{decision.outcome}"] += 1
        telemetry.log(
            {
                "event": "lockn511_dry_run",
                "task_index": i,
                "tool": t.get("tool"),
                "action": t.get("action"),
                "reason": "; ".join(decision.reasons),
                "trigger": decision.triggers,
                "selected_model": decision.selected_model_tier,
                "outcome": decision.outcome,
                "risk": decision.risk,
            }
        )
        rows.append(
            f"| {i} | `{t.get('tool')}` | `{t.get('action','')}` | {decision.risk} | {decision.route} | {decision.outcome} | {', '.join(decision.triggers) or '-'} |"
        )

    report = [
        "# LOCKN-511 Dry Run Report",
        "",
        f"Sample size: **{len(tasks)}**",
        "",
        "## Aggregate results",
        "",
        f"- Safe: {counters['safe']}",
        f"- Caution: {counters['caution']}",
        f"- Privileged: {counters['privileged']}",
        f"- Destructive: {counters['destructive']}",
        f"- Routed local: {counters['route:local']}",
        f"- Routed cloud: {counters['route:cloud']}",
        "",
        "## Per-task decisions",
        "",
        "| # | Tool | Action | Risk | Route | Outcome | Triggers |",
        "|---|------|--------|------|-------|---------|----------|",
        *rows,
        "",
        "## KPI trial (2 weeks)",
        "",
        "Track daily:",
        "- Escalation rate = cloud_routed / total_tool_calls",
        "- False positive rate = manual_overrides_allow / escalations",
        "- Human approval volume for destructive ops",
        "- Mean approval latency (cloud + human)",
        "- Policy coverage = classified_calls / total_tool_calls",
        "",
    ]

    Path(args.report).write_text("\n".join(report), encoding="utf-8")
    print(f"Wrote report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
