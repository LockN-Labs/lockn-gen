# LockN Control — Mission Control Dashboard Vision

## Purpose
An always-on, high-density operations dashboard for a **solo founder + AI agent swarm**. Designed for passive monitoring at 3–4 ft distance, with immediate detection of blockers and rapid drill-down into root causes.

---

## 1) Wireframe Layout (Grafana, 16:9 monitor)

> Recommended canvas: 1920×1080 (scales to 2560×1440). 12-column grid.

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ LOCKN CONTROL · Mission Control                Last Refresh: 15:30:12   Auto: ON (5s/15s)  │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 🔴 ALERTS & BLOCKERS (100% width, ~22% height, highest visual weight)                      │
│ ┌──────────────────────────────┬──────────────────────────────┬────────────────────────────┐ │
│ │ P1: llama.cpp:11438 DOWN     │ P1: Cron failed: nightly CI │ P2: Billing threshold 82% │ │
│ │ 3m ago · impact: dev blocked  │ 14m ago · retrying          │ est 5 days remaining      │ │
│ │ [ACK] [Open Logs]             │ [ACK] [Open Job]            │ [Open Billing]            │ │
│ └──────────────────────────────┴──────────────────────────────┴────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ LEFT: 🟢 ACTIVE THREADS (~58% width, ~46% height)   │ RIGHT: ⚡ SYSTEM STATUS (~42% width) │
│ ┌───────────────────────────────────────────────────┐ │ ┌──────────────────────────────────┐ │
│ │ Subagent Sessions (table)                        │ │ │ Resource Gauges                  │ │
│ │ Agent       Task                  Elapsed Status │ │ │ CPU 67%  RAM 74%  GPU 81%       │ │
│ │ orchestrator Sprint planner       00:21  RUNNING│ │ │                                  │ │
│ │ dev         LIN-342 fix auth      01:07  RUNNING│ │ │ Model Servers (11436-11440)     │ │
│ │ ux          dashboard wireframe   00:09  RUNNING│ │ │ 11436 ✅ q:0  model:Qwen-Coder  │ │
│ │                                           ...    │ │ │ 11437 ✅ q:2  model:Llama-70B   │ │
│ │                                                   │ │ │ 11438 ❌ q:-  model:-           │ │
│ │ Cron Jobs (compact list)                          │ │ │ Ollama ✅ q:1                    │ │
│ │ ingest-linear 2m ago ✅ | heartbeat 1m ago ✅     │ │ │                                  │ │
│ │ nightly-ci 14m ago ❌ | backup 22m ago ✅         │ │ │ Docker Health Grid (20+ cells)  │ │
│ │                                                   │ │ │ ■■■■■■■■■■■■■■■■■■□□            │ │
│ │ In-Progress Linear Tickets                        │ │ │ green/yellow/red by container    │ │
│ │ LIN-342 dev | LIN-355 devops | LIN-361 research  │ │ │                                  │ │
│ └───────────────────────────────────────────────────┘ │ │ Gateway                           │ │
│                                                       │ │ Sessions: 7  Mem: 1.8GB  Cron: 6 │ │
│                                                       │ └──────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ 📋 PRIORITY QUEUE (100% width, ~32% height)                                                   │
│ ┌────────────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ WIP: 3 / 3  (AT LIMIT)      Next Ready: LIN-377 (unblocked, est 3h, project: Platform) │ │
│ │--------------------------------------------------------------------------------------------│ │
│ │ Rank │ Ticket  │ Title                         │ Owner/Agent │ Priority │ Blocker         │ │
│ │ 1    │ LIN-355 │ Stabilize cron retries        │ devops      │ Urgent   │ none            │ │
│ │ 2    │ LIN-342 │ Auth token race condition     │ dev         │ High     │ none            │ │
│ │ 3    │ LIN-361 │ Research eval harness         │ research    │ High     │ waiting on GPU  │ │
│ │ 4    │ LIN-377 │ OpenClaw memory compaction    │ unassigned  │ Medium   │ none            │ │
│ │ 5    │ LIN-369 │ Refactor agent prompt router  │ dev         │ Medium   │ blocked by LIN-355││
│ └────────────────────────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Layout hierarchy
1. **Top strip = interruption layer** (must force attention)
2. **Middle split = runtime awareness** (who is doing what + infra health)
3. **Bottom = decision queue** (what to do next)

---

## 2) Component Spec (data, refresh, source)

## A. 🔴 Alerts & Blockers Panel (Top)
**Goal:** Surface only items requiring action/decision now.

- **Contents**
  - Critical service outages (model servers, Ollama, Grafana, Gateway)
  - Failed cron jobs (last run failed + retries exhausted/ongoing)
  - Billing/cost threshold breaches (GPU cloud, API spend)
  - Blocked approvals requiring CEO input (if present from OpenClaw/Linear tags)
- **Visual format**
  - Alert cards with severity badge: `P1/P2/P3`
  - Age timer (`3m ago`) and impact summary (`dev blocked`)
- **Refresh**
  - **5s** for runtime outages / job failures
  - **60s** for billing + decision-needed flags
- **Data sources**
  - Prometheus alertmanager-style metrics (or recording rules)
  - OpenClaw API: cron run status, failed jobs, pending approvals
  - Docker health endpoints via exporter
  - Optional billing API adapter metric into Prometheus

---

## B. 🟢 Active Threads Panel (Left Middle)
**Goal:** Show what agents/jobs are actively moving and whether work is stuck.

### B1. Subagent Sessions
- **Fields**
  - Agent name, model, task summary, elapsed time, status (`RUNNING/WAITING/BLOCKED/ERROR`)
- **Refresh**: **5s**
- **Source**: OpenClaw sessions API / gateway runtime stats

### B2. Active Cron Jobs
- **Fields**
  - Job name, last run timestamp, last result, next scheduled run
- **Refresh**: **10s**
- **Source**: OpenClaw cron scheduler API + Prometheus job metrics

### B3. In-Progress Linear Tickets
- **Fields**
  - Issue ID, title, assignee/delegate agent, status, updated-at freshness
- **Refresh**: **30s**
- **Source**: Linear API (filtered by in-progress states)

---

## C. ⚡ System Status Panel (Right Middle)
**Goal:** Quick confidence check that core system can execute workload.

### C1. Resource Utilization
- **Metrics**
  - CPU %, RAM %, GPU util %, GPU VRAM %, load average
- **Refresh**: **2–5s**
- **Source**: Prometheus node_exporter + GPU exporter

### C2. Local Model Server Matrix
- **Metrics per endpoint (11436–11440 + Ollama)**
  - Up/Down
  - Current loaded model
  - Queue depth / active requests
  - p95 latency
- **Refresh**: **5s**
- **Source**: Prometheus scrape of model server health endpoints

### C3. Docker Health Grid
- **Metrics**
  - Container status for all critical services (20+)
  - Health state (`healthy/unhealthy/restarting`)
- **Refresh**: **5s**
- **Source**: Docker API exporter to Prometheus

### C4. Gateway Status
- **Metrics**
  - Active sessions, memory footprint, queue backlog, heartbeat lag
- **Refresh**: **5s**
- **Source**: OpenClaw API + exporter metrics

---

## D. 📋 Priority Queue Panel (Bottom)
**Goal:** Show execution order and immediate next move under WIP constraints.

- **Contents**
  - Top 5 Linear issues sorted by project priority + urgency rules
  - WIP count vs WIP limit (3)
  - “Next unblocked ticket” recommendation
  - Blocked list with explicit blocker reason (dependency, waiting on decision, infra)
- **Refresh**
  - **30–60s** (Linear polling)
- **Source**
  - Linear API (issues, projects, priorities, dependencies)
  - Optional OpenClaw policy engine for “next-best-ticket” recommendation

---

## 3) Visual Design Guidelines

## Theme
- **Mode:** Dark, high contrast, low glare for always-on display
- **Backgrounds**
  - App background: `#0B0F14`
  - Panel background: `#121821`
  - Elevated card: `#18212B`
  - Borders/dividers: `#243041`

## Status colors (semantic, consistent everywhere)
- **Critical / P1 / Down:** `#FF4D4F` (red)
- **Warning / Degraded / P2:** `#FAAD14` (amber)
- **Healthy / Running:** `#52C41A` (green)
- **Info / Neutral:** `#4DA3FF` (blue)
- **Muted text:** `#94A3B8`
- **Primary text:** `#E6EDF3`

## Typography (distance-readable)
- Dashboard title: **28px / 700**
- Section headers: **20px / 700**
- KPI values (CPU%, WIP): **34–44px / 700**
- Table/body text: **16–18px / 500**
- Metadata (timestamps): **14px / 400**

> Rule: no essential information below 16px.

## Spacing + density
- Global panel gap: **12px**
- Panel padding: **12–16px**
- Card radius: **8px**
- Minimum row height (tables): **34px**
- Keep max 3 visual weights per panel (header, value, metadata)

## Status indicator style
- Dot + label pattern: `● RUNNING`, `● BLOCKED`, etc.
- Dot sizes:
  - Inline: 8px
  - Critical tiles: 12px + subtle glow
- Blink/animation only for **new P1 within last 60s** (avoid constant motion fatigue)

---

## 4) Interaction Model (always-on first, drill-down second)

## Default mode
- Primarily **view-only**, auto-refreshing
- No routine interaction required for monitoring

## Clickable elements (for investigation)
- Alert card → opens relevant Grafana logs panel / external runbook URL
- Session row → opens OpenClaw session detail/log stream
- Cron item → opens job history + last failure output
- Linear issue row → opens issue in Linear
- Docker container cell → opens container logs/metrics drill-down

## Drill-down behavior
- Open in new tab/window (dashboard remains on monitor)
- Drill-down must preserve context (time range + selected entity)
- Keyboard quick actions (optional)
  - `A` jump to alerts
  - `S` system status
  - `Q` priority queue

## Guardrails
- No modal popups on passive dashboard
- No auto-navigation on refresh
- Acknowledge buttons only for reducing visual noise; underlying condition stays tracked until resolved

---

## 5) Priority Order for Implementation

## Phase 1 — Core visibility (must-have)
1. **Alerts & Blockers panel** (highest value, immediate risk detection)
2. **System Status panel** (CPU/RAM/GPU + model server up/down + Docker health)
3. **WIP counter + top 5 Priority Queue**

## Phase 2 — Operational flow
4. **Active Threads: subagent sessions table**
5. **Active cron jobs + last run status**
6. **Next unblocked ticket recommendation logic**

## Phase 3 — Deep operations UX
7. Click-through drill-down links (logs, runs, Linear)
8. Alert acknowledgements + noise suppression rules
9. Visual polish: animation constraints, final spacing/contrast tuning

## Phase 4 — Advanced optimization
10. Predictive indicators (queue growth, memory pressure forecast)
11. SLA/MTTR trend sparklines by subsystem
12. Shift/day summary strip for founder handoff context

---

## Grafana Implementation Notes (practical)
- Use a **single dashboard** with fixed layout and panel repeat only where needed (model ports, containers).
- Prefer **Stat**, **Table**, and **State timeline** panels for readability.
- For Docker health grid, use transformed table with cell background thresholds.
- Normalize all statuses into a shared enum: `healthy | degraded | down | blocked | unknown`.
- Standardize refresh intervals by panel class:
  - critical runtime: 5s
  - infra + sessions: 10s
  - Linear/project data: 30–60s
- Keep time range pinned to “last 15m” for runtime panels, “last 24h” for cron/billing context.

---

## Definition of Done (Dashboard v1)
- Founder can stand 3–4 ft away and answer in <10 seconds:
  1. **Is anything on fire?** (top red/yellow strip)
  2. **What are agents doing now?** (left middle)
  3. **Can the stack handle load?** (right middle)
  4. **What should happen next?** (bottom queue + WIP)
- No panel requires manual refresh.
- All key statuses are color-coded and text-labeled (never color-only).
- Drill-down links work without disrupting main monitor view.
