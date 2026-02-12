# Corrections Register

## 2026-02-11: Codex "billing error" is actually rate limiting
- SUPERSEDES: "Codex credits exhausted" (earlier today)
- CORRECTED: Codex has 96% of 5h limit and 87% weekly remaining. The "billing/credits" error is a misleading rate limit response triggered by concurrent parallel requests (e.g., 5 subagents spawned simultaneously). Not a credits issue.
- Fix: stagger parallel Codex requests with 5-10s delays, or add fallback model

## 2026-02-11: Gateway CPU root cause
- SUPERSEDES: "cron backlog causing high CPU"
- CORRECTED: Root cause was sessions.json bloat (29MB, 2255 entries), not cron backlog itself. Cron runs created session entries that were never cleaned up.

When a fact is corrected, add an entry here. Memory search results that conflict with entries in this file should be treated as STALE and overridden.

Format: `[date] SUPERSEDES: "<old claim>" → "<corrected fact>" (source: <context>)`

---

## Infrastructure & Services
- [2026-02-11] SUPERSEDES: "llama.cpp port 11437 is down" → "llama-qwen.service (port 11437) is running but not auto-enabled at boot — requires manual `systemctl --user start llama-qwen.service` after reboot" (source: live check 2026-02-11 13:51)
- [2026-02-11] SUPERSEDES: "cron subsystem is broken due to Kimi structured outputs" → "cron list times out due to 23 stale nextRunAtMs entries causing backlog storm + 46 total jobs overwhelming the scheduler. Kimi jobs swapped to DeepSeek, disabled jobs purged, stale schedules reset." (source: investigation 2026-02-11 14:25-14:35)
- [2026-02-11] SUPERSEDES: "9 dirty PRs need rebase" → "Status unknown — last checked Feb 8. Needs fresh git audit." (source: stale info, no live verification since Feb 8)

## Communication
- [2026-02-11] **CRITICAL** SUPERSEDES: any implicit "DM is okay for quick updates" → "NEVER use the DM thread (D0AC46HCRNZ) for ANY communication. Route ALL messages through appropriate Slack channels. If no appropriate channel exists, suggest creation in #process-improvements (C0ADGH08ZD1). This is non-negotiable — Sean has flagged this multiple times."

## Operational Facts
- [2026-02-11] SUPERSEDES: "OpenClaw version 2026.2.6-3" → "Updated to 2026.2.9 on 2026-02-11" (source: `openclaw --version`)
- [2026-02-11] SUPERSEDES: "commands.restart disabled in gateway" → "commands.restart=true enabled 2026-02-11 14:02" (source: config.patch applied)

## Revenue & Product
- [2026-02-10] SUPERSEDES: "Auth0 has 55 per-page callbacks" → "Consolidated to single `/auth/callback/` route (LOC-425, fixed 2026-02-10)" (source: already in MEMORY.md but old chunks may still exist)
