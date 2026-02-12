# Architecture Decisions (Active)

Purpose: track accepted decisions, superseded choices, and unresolved governance gaps.

Last reviewed: 2026-02-09 18:00 EST

## Accepted Decisions

### AD-001 — Local-first implementation routing
- **Decision:** Implement via Coder-Next first; use cloud models for orchestration/fallback
- **Status:** Active
- **Why:** Cost control + high throughput on local hardware
- **Implementation:** coding-pipeline skill dispatches to :11439

### AD-002 — PR-centered delivery workflow
- **Decision:** All code changes flow through PR review before merge
- **Status:** Active
- **Why:** Auditability, quality gates, reversible history
- **Authority:** Top orchestrator (Opus) owns process end-to-end

### AD-003 — Dual endpoint Coder-Next strategy
- **Decision:** GPU (:11439, 1M context) + CPU (:11440, 2M context) lanes
- **Status:** Active
- **Why:** Balance speed with very-large-context analysis capacity
- **GPU:** ~500 tok/s for standard work
- **CPU:** ~15-30 tok/s for massive context tasks

### AD-004 — Vision endpoint consolidation
- **Decision:** Retire legacy :11441 VL path; standardize on Ollama :11434 (Qwen3-VL 8B)
- **Status:** Active (completed 2026-02-08)
- **Why:** Qwen3-VL 8B via Ollama has 256K context, better spatial reasoning, on-demand VRAM

### AD-005 — Local-first, cloud-enhanced product strategy
- **Decision:** Every LockN module works standalone; cloud services enhance but never lock users in
- **Status:** Active (established 2026-02-09 with lockn-git)
- **Why:** Sean's core product principle — no vendor lock-in for customers
- **Example:** lockn-git uses Forgejo locally with GitHub mirror sync

### AD-006 — Multi-model review diversity
- **Decision:** Run docs/system reviews with alternating models (Opus, Codex, Kimi) to get diverse perspectives
- **Status:** Active
- **Why:** Different models catch different issues; diversity of thought reduces blind spots

### AD-007 — Sandbox security by model size
- **Decision:** Sandbox small models (≤32B), trust large models (80B+) and cloud models
- **Status:** Active (established 2026-02-09)
- **Why:** Small models lack safety filters; sandbox provides exec guardrails

## Superseded Decisions
- **Opus-only orchestration:** Drifted to multi-model; now explicitly multi-model by design (AD-006)
- **Port 11441 for VL:** Retired in favor of Ollama :11434 (AD-004)
- **Kimi as default model:** Was briefly default; reverted to Opus 2026-02-09

## Open Decisions (Not Resolved)

### OD-001 — Model governance source of truth
- **Problem:** Default model policy exists in gateway config, memory files, and cron payloads
- **Need:** Single canonical enforcement layer
- **Recommendation:** Gateway config is authoritative; cron payloads override per-job only

### OD-002 — Cron portfolio governance
- **Problem:** 24 jobs, some overlapping (revenue triage runs 6x/day across 2 jobs)
- **Need:** Explicit ownership, dedupe policy, max overlap budget, cost tracking per job
- **Recommendation:** Consolidate revenue-triage-ticket-gen into revenue-triage-and-tickets

### OD-003 — Security hardening ownership
- **Problem:** 4 critical audit findings from `openclaw status` remain open
- **Need:** Named owner + SLA for closing findings
- **Recommendation:** Track as Linear tickets with deadlines

### OD-004 — Stopped container recovery
- **Problem:** 13 containers down after apparent system restart; no auto-recovery for non-infra stacks
- **Need:** Recovery automation or docker compose restart policies
- **Recommendation:** Add `restart: unless-stopped` to all compose files; create recovery script

## Maintenance Rule
Add a new AD entry whenever a material architecture choice changes behavior, cost, or security posture.
