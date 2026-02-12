# Post-Mortem: 6-Hour Execution Gap (2026-02-10)

## Incident
Between ~6:30 PM and 12:30 AM ET on 2026-02-10/11, zero Linear tickets were worked despite 3 Urgent items In Progress and 7+ Urgent items in Todo. The system had 30+ active cron jobs monitoring, auditing, and triaging — but none executing.

## Timeline
- **~12:00 PM**: Demo prep session begins — reactive firefighting on Score infra, camera streaming, auth
- **~6:00 PM**: Demo prep work completed. Session goes idle.
- **~6:00 PM – 12:30 AM**: No work executed. Heartbeat fires every hour but just checks priorities and replies HEARTBEAT_OK. No tickets picked up.
- **12:29 AM**: Sean notices and flags in Slack.

## Root Causes

### 1. All observation, zero execution
The cron system had grown to 30+ jobs, all focused on monitoring, auditing, reviewing, and generating tickets. Not a single job was designed to actually implement code. The ratio was:
- **Observation jobs**: 30+
- **Execution jobs**: 0

### 2. Heartbeat couldn't sustain work
HEARTBEAT.md said "pick that item and start it" but heartbeats run in isolated sessions that die after one turn. They can't do sustained multi-hour coding work.

### 3. Session idle = full stop
Session resets after 90min idle. After the demo session ended, no mechanism re-engaged. The orchestrator heartbeat fired every 7 minutes but had nothing actionable to do in isolation.

### 4. Ticket generators outpaced closers
- `revenue-triage-ticket-gen`: 3x/day, 3-5 tickets each = ~12 tickets/day created
- `backlog-brainstorm`: 2x/day, 1-3 tickets each = ~4 tickets/day created
- **Tickets closed per day**: 0 (no execution mechanism)

### 5. Ad-hoc work untracked
6 hours of demo prep work (Docker networking, WebSocket routing, auth fixes, camera streaming) was done without any Linear tickets. No status updates, no subtasks. Work happened but was invisible to the system.

## Fixes Applied

### New: Work Executor Cron (hourly)
- **Job**: `work-executor-hourly`
- **Model**: Coder-Next (local, free compute)
- **Runs**: Every 1 hour
- **Action**: Picks top unblocked `agent:coder` ticket, implements it, commits, pushes, creates PR, updates Linear status
- **Reports to**: #main-realtime

### New: Idle Watchdog (every 2h)
- **Job**: `idle-watchdog-2h`
- **Model**: Codex
- **Runs**: Every 2 hours
- **Action**: Checks if any ticket moved to Done in last 2h. If not, alerts #main-realtime with queue depth and executor status.

### Updated: HEARTBEAT.md
- Primary directive changed from "check priorities" to "SPAWN WORK"
- Added anti-idle rule: if no Done tickets in 2h during waking hours, spawn work or alert
- Added QA awareness: verify changes didn't break existing flows

### Paused: Redundant observation crons
- `backlog-brainstorm-opus-pm` (Opus, expensive, duplicates Kimi AM pass)
- `ticket-quality-audit-am` (Codex, duplicates PM pass)
- `ticket-quality-audit-pm` (Codex, duplicates AM pass)
- `docs-review-organize-3h-alternating` (Opus 4x/day, duplicates Codex pass)

**Token savings**: ~$2-4/day in Opus + Codex costs redirected toward actual execution.

## Lessons for QA

### Issues discovered during demo prep (all avoidable):
1. **WebSocket room mismatch**: Spectator connected to `/ws/solo`, camera streamed to `/ws/game/{sessionId}`. Would have been caught by an integration test that connects both endpoints and verifies message delivery.
2. **Docker network isolation**: Score containers not reachable via Caddy. Would have been caught by a connectivity test in CI.
3. **Auth0 redirect override**: `docker-compose.yml` env var overrode Dockerfile default. Would have been caught by a smoke test that follows the QR scan → auth flow.
4. **Camera streaming stub**: "Start Streaming" button was a `console.log`. Would have been caught by any E2E test of the camera flow.

### QA improvements needed:
- **E2E smoke tests**: Run after every deploy, test actual user flows (not just health endpoints)
- **WebSocket integration tests**: Verify rooms, message delivery, connection lifecycle
- **Auth flow validation**: Already have `auth-flow-validation-6h` cron, but it checks config, not actual user flows
- **Cross-service connectivity tests**: Verify Docker network topology matches expected routing

## Metrics to Track
- **Tickets closed per day** (target: ≥2)
- **Time from In Progress to Done** (target: <24h for standard tickets)
- **Idle hours per day** (target: <1h during waking hours)
- **Observation:Execution cron ratio** (target: <3:1)

## Status
- [x] Work executor cron created and enabled
- [x] Idle watchdog created and enabled
- [x] HEARTBEAT.md updated
- [x] Redundant crons paused
- [ ] E2E smoke test suite (needs ticket)
- [ ] WebSocket integration tests (needs ticket)
- [ ] Cross-service connectivity tests (needs ticket)
