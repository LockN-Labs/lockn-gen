# HEARTBEAT.md

## Cron Scheduler Health Check
- Run `cron status` (10s timeout). If it times out or errors, **DO NOT restart gateway** — just post an alert to #system-heartbeat (C0ACDPDQ9L5) noting the timeout. Restarting on cron timeout causes a restart loop (overdue jobs flood on restart → timeout → restart again).
- If status returns OK, check that work-executor-10min last ran within 30min. If stale, flag in #system-heartbeat.

## Workspace State Guard
- Verify `git branch --show-current` == `main`. If not, switch back and alert.
- Check these files are tracked: `git ls-files MEMORY.md TOOLS.md USER.md HEARTBEAT.md AGENTS.md SOUL.md BOOT.md IDENTITY.md` — all 8 must appear. Flag any missing as DEGRADED.
- Check for uncommitted state file changes: `git diff --name-only MEMORY.md TOOLS.md USER.md HEARTBEAT.md AGENTS.md SOUL.md BOOT.md IDENTITY.md` — if any dirty, auto-commit with `chore: auto-commit state files (heartbeat guard)`.

## Dev Agents Channel Accountability
- If any subagent completed work since last heartbeat, ensure results were posted to #dev-agents with PR/ticket links.
