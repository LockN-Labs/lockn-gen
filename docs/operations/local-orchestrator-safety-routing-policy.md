# Local-Orchestrator Safety Routing Policy (LOCKN-511)

## Risk classifier tiers

- **safe**: read-only and low-impact internal actions.
- **caution**: external writes / moderate impact.
- **privileged**: sensitive domain or infra lifecycle changes.
- **destructive**: potentially irreversible or elevated execution.

## Hard triggers

Classify immediately as privileged/destructive when any trigger matches:

1. `exec.elevated == true` → **destructive**
2. Gateway lifecycle action (`gateway config|update|restart|stop`) → **privileged**
3. Intent or command includes `prod|auth|billing|security|token|credential` → **privileged**
4. Destructive shell patterns (`rm -rf`, `terraform destroy`, `kubectl delete`, `mkfs`, `dd if=`, etc.) → **destructive**

## Policy matrix

| Risk | Allowed model tier | Local execution | Cloud approval | Human approval |
|---|---|---|---|---|
| safe | local-small / local-large / cloud | yes | no | no |
| caution | local-large / cloud | yes | no | no |
| privileged | cloud only | no | yes (two-model path) | no |
| destructive | cloud only | no | yes (two-model path) | yes |

## Enforcement behavior

- If risk is `privileged` or `destructive`, local orchestrator is blocked and routed to cloud path in **all orchestration modes**.
- Two-model path for sensitive ops:
  1) local model generates plan/context (`local_plan`)
  2) cloud model approves/executes route (`cloud_approval`)
- Destructive operations require explicit human gate before execution (`human_approval`).

## Runtime orchestration mode toggle (no redeploy)

Supported runtime modes:
- `cloud-first`
- `local-first`
- `hybrid`

Mode state file: `.runs/lockn511_runtime_mode.json`

Guardrails rollout switch: `guardrails_enabled` (default `false` for safe rollout).

CLI control:

```bash
python scripts/lockn511_mode_ctl.py status
python scripts/lockn511_mode_ctl.py set-mode cloud-first --actor sean
python scripts/lockn511_mode_ctl.py set-mode local-first --actor sean
python scripts/lockn511_mode_ctl.py set-mode hybrid --actor sean
python scripts/lockn511_mode_ctl.py set-guardrails on --actor sean
python scripts/lockn511_mode_ctl.py set-guardrails off --actor sean
```

Every mode/guardrail change is audit-logged to `logs/escalation_telemetry.jsonl`.

## Telemetry

Append JSONL records to `logs/escalation_telemetry.jsonl`:

```json
{
  "ts": "2026-02-11T22:00:00Z",
  "reason": "Elevated shell execution requested",
  "trigger": ["exec.elevated"],
  "selected_model": "cloud",
  "outcome": "escalated",
  "risk": "destructive",
  "tool": "exec",
  "action": ""
}
```

## Rollout plan (2-week KPI trial)

- Week 1: Feature flag OFF in prod, run dry-run simulations + telemetry only.
- Week 2: Enable for internal channels first, monitor, tune patterns.

### KPIs

- Escalation rate (`cloud_routed / total_calls`)
- False-positive rate (`manual_override_allow / escalations`)
- Human approval volume and latency for destructive ops
- Policy coverage (`classified_calls / total_calls`)
- Incident count from unsafe local execution (target: 0)
