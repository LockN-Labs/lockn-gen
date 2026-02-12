# HEARTBEAT.md

## Cron Scheduler Health Check
- Run `cron status` (10s timeout). If it times out or errors, restart gateway and post alert to #dev-agents (C0AECSTM8ER).
- If status returns OK, check that work-executor-hourly last ran within 30min. If stale, flag in #dev-agents.

## Dev Agents Channel Accountability
- If any subagent completed work since last heartbeat, ensure results were posted to #dev-agents with PR/ticket links.
