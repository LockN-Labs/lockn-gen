# HEARTBEAT.md

## Primary Directive: SPAWN WORK
The heartbeat's #1 job is ensuring productive work is happening. Observation without execution is failure.

## Priority Check (every heartbeat)
1. Check Linear **Project-Level Priorities view** — top project = current org focus (NOT initiative order)
2. Within top project, find highest-priority unblocked issue with `agent:coder` label
3. Check if work-executor cron is producing results (any Done tickets in last 2h?)
4. If work-executor seems stalled or idle, spawn a dev subagent on the top ticket NOW
5. Respect blockedBy/blocks relations — never start blocked work
6. If something is blocked, flag it in Slack #main-realtime

## Staleness Tracking (replaces WIP limit)
No cap on parallel In Progress items. Instead, track time-in-status:
- **>48h with no commit/comment** → flag as stale in #main-realtime, ping assignee or agent
- **>7 days In Progress** → auto-move to Backlog with a comment explaining why ("No activity for 7 days, moving to Backlog to keep the board clean. Reopen when ready to resume.")
- Parallel work across different domains (revenue, design, ops, infra) is fine and expected in a multi-agent system

## Quick Checks (rotate, 2-3x daily)
- Stale In Progress items per rules above
- Linear items with no assignee that should have one
- **Orphan issues**: Any issue without a project assignment → assign to correct project
- **Stale projects**: Any project In Progress with no issue activity >7 days → flag

## QA Awareness
After any ticket is marked Done, verify the change didn't break existing flows:
- Check health endpoints for affected services
- If the ticket touched auth/routing/Docker, run a quick smoke test
- Flag regressions immediately in #main-realtime

## Anti-Idle Rule
If you notice no tickets have moved to Done in >2h during waking hours (8am-midnight ET), that's a red flag. Either spawn work or alert Sean.
