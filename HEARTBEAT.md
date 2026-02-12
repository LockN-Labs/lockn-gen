# HEARTBEAT.md

## Cron Scheduler Health Check
- Run `cron status` (10s timeout). If it times out or errors, restart gateway and post alert to #dev-agents (C0AECSTM8ER).
- If status returns OK, check that work-executor-hourly last ran within 30min. If stale, flag in #dev-agents.

## Workspace State Guard
- Verify `git branch --show-current` == `main`. If not, switch back and alert.
- Check these files are tracked: `git ls-files MEMORY.md TOOLS.md USER.md HEARTBEAT.md AGENTS.md SOUL.md BOOT.md IDENTITY.md` — all 8 must appear. Flag any missing as DEGRADED.
- Check for uncommitted state file changes: `git diff --name-only MEMORY.md TOOLS.md USER.md HEARTBEAT.md AGENTS.md SOUL.md BOOT.md IDENTITY.md` — if any dirty, auto-commit with `chore: auto-commit state files (heartbeat guard)`.

## Dev Agents Channel Accountability
- If any subagent completed work since last heartbeat, ensure results were posted to #dev-agents with PR/ticket links.
