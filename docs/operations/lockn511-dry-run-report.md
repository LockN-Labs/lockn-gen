# LOCKN-511 Dry Run Report

Sample size: **10**

## Aggregate results

- Safe: 3
- Caution: 1
- Privileged: 4
- Destructive: 2
- Routed local: 4
- Routed cloud: 6

## Per-task decisions

| # | Tool | Action | Risk | Route | Outcome | Triggers |
|---|------|--------|------|-------|---------|----------|
| 1 | `read` | `` | safe | local | allowed | - |
| 2 | `exec` | `` | safe | local | allowed | - |
| 3 | `exec` | `` | privileged | cloud | escalated | gateway.command:\bopenclaw\s+gateway\s+restart\b |
| 4 | `exec` | `` | destructive | cloud | escalated | destructive_pattern:\brm\s+-rf\b |
| 5 | `exec` | `` | privileged | cloud | escalated | sensitive_keyword |
| 6 | `linear_update_issue` | `` | caution | local | allowed | tool.write |
| 7 | `exec` | `gateway restart` | privileged | cloud | escalated | gateway.action:gateway restart, gateway.command:\bopenclaw\s+gateway\s+restart\b |
| 8 | `exec` | `` | destructive | cloud | escalated | exec.elevated |
| 9 | `write` | `` | safe | local | allowed | - |
| 10 | `exec` | `` | privileged | cloud | escalated | sensitive_keyword |

## KPI trial (2 weeks)

Track daily:
- Escalation rate = cloud_routed / total_tool_calls
- False positive rate = manual_overrides_allow / escalations
- Human approval volume for destructive ops
- Mean approval latency (cloud + human)
- Policy coverage = classified_calls / total_tool_calls
