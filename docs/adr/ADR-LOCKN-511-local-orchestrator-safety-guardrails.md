# ADR: LOCKN-511 Local-Orchestrator Safety Routing Guardrails

- **Ticket:** <https://linear.app/lockn-ai/issue/LOCKN-511|LOCKN-511>
- **Date:** 2026-02-11
- **Status:** Accepted (feature-flagged, default OFF)

## Context

OpenClaw currently supports local-first orchestration, but sensitive operations require stricter routing controls to prevent privileged/destructive actions from being executed on local orchestration paths.

## Decision

Introduce a policy-driven safety guardrail layer with:

1. **Risk classifier** over tool + action + intent + payload.
2. **Policy matrix** mapping risk tier to allowed model tiers and required approvals.
3. **Router enforcement** that blocks privileged/destructive execution on local orchestrator and escalates to cloud.
4. **Hard triggers** for elevated exec, gateway lifecycle actions, sensitive keywords, and destructive shell patterns.
5. **Two-model approval path** (local planning + cloud approval) and **human gate** for destructive actions.
6. **Escalation telemetry** JSONL logs (reason/trigger/model/outcome).

## Why feature-flagged

Integration points vary by orchestrator flow. To avoid breaking existing routing, enforcement is behind `LOCKN511_GUARDRAILS_ENABLED` (default `false`).

## Consequences

- Minimal risk to current production behavior while policy matures.
- Dry-run and telemetry provide confidence before default-on rollout.
- Enables measurable KPI-based rollout over 2-week trial.
