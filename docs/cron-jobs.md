# Cron Jobs (Source of Truth)

Purpose: operational map of active scheduler lanes and governance.

Last reviewed: 2026-02-09 18:00 EST

## Runtime Snapshot
- Total configured jobs: **24**
- Enabled: **24**
- Disabled: **0**
- One-shot pending: 1 (`Reminder: revisit C after focusing on A/B` — fires 2026-02-11 10:05 AM EST)

## Operational Lanes

### 1. Heartbeat / Orchestration
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `heartbeat-7min-main-orchestrator` | Every 7m | Default (Opus) | #agent-status |
| `Approval timeout policy (1h)` | Every 1h | systemEvent → main | Main session |
| `Slack workspace comms health reminder` | Every 2h | systemEvent → main | Main session |

### 2. Infrastructure / Reliability
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `devops-infra-check-15min` | Every 15m | Codex | #agent-status |
| `docker-infra-audit-6h` | 3:30/9:30/15:30/21:30 | Codex | #agent-status |
| `gpu-monitor-stale-containers` | Every 4h (0,4,8,12,16,20) | Codex | #agent-status |
| `2am-regression-qa` | 2:00 AM | Codex | #agent-status |
| `lockn-usage-collector` | Every 5m | Default | #lockn-logger |

### 3. Documentation & Architecture
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `docs-review-organize-3h-alternating` | 0:00/6:00/12:00/18:00 | **Opus** | Sean DM |
| `docs-review-organize-kimi-3h` | 3:00/9:00/15:00/21:00 | **Codex** | Sean DM |
| `nightly-docs-crawl` | 2:30 AM | Default | Announce |
| `nightly-architecture-analysis` | 1:00 AM | Coder-Next | None |
| `arch-decisions-review-kimi` | 7:00 AM | Codex | #lockn-dev |

### 4. Revenue / Backlog
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `revenue-triage-and-tickets` | 8:00/14:00/20:00 | Codex | #lockn-dev |
| `revenue-triage-ticket-gen` | 6:00/12:00/18:00 | Codex | #lockn-dev |
| `backlog-brainstorm-kimi-am` | 4:30 AM | Kimi K2.5 | Sean DM |
| `backlog-brainstorm-opus-pm` | 4:30 PM | Opus | Sean DM |
| `ticket-quality-audit-am` | 6:00 AM | Codex | #lockn-dev |
| `ticket-quality-audit-pm` | 6:00 PM | Codex | #lockn-dev |

### 5. Strategic / Intelligence
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `system-review-opus-am` | 5:00 AM | Opus | #lockn-dev |
| `system-review-kimi-pm` | 5:00 PM | Codex | #lockn-dev |
| `competitive-intelligence-kimi` | 8:00 AM | Codex | #lockn-dev |
| `ecosystem-monitor-kimi` | 4:00 AM | Kimi K2.5 | Announce |
| `daily-7am-summary` | 7:00 AM | Sonnet | #agent-status |

### 6. Weekly
| Job | Schedule | Model | Target |
|-----|----------|-------|--------|
| `weekly-memory-compaction` | Sun 3:00 AM | Codex | Sean DM |
| `cmo-review-weekly` | Mon 9:00 AM | Codex | Sean DM |
| `cfo-review-weekly` | Mon 10:00 AM | Codex | Sean DM |
| `linear-invite-reminder` | Daily 9:00 AM | Codex | Announce |

### 7. One-Shot
| Job | Fires | Model | Purpose |
|-----|-------|-------|---------|
| `Reminder: revisit C` | 2026-02-11 10:05 AM | systemEvent | Priority review reminder |

## Known Issues
1. **Naming drift:** Several jobs named "kimi" now use Codex (names haven't been updated to match payload model)
2. **Overlap risk:** Revenue triage runs at both 6:00/12:00/18:00 AND 8:00/14:00/20:00 — potential duplicate ticket creation
3. **Density:** 24 jobs with some running every 5-15 minutes creates significant token burn

## Recommendations
1. **Rename jobs** whose names reference wrong models (e.g., `docs-review-organize-kimi-3h` uses Codex)
2. **Consolidate revenue jobs** — `revenue-triage-ticket-gen` and `revenue-triage-and-tickets` overlap
3. **Track token cost per job** to identify high-burn/low-value jobs
4. **Add SLOs** per lane (e.g., infra checks must complete <60s)

## Maintenance Rule
Update this file when cron jobs are added, removed, renamed, or have their model changed.
