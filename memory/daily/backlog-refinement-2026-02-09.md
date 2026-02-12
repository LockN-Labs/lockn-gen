# Backlog Refinement — 2026-02-09 Afternoon (Opus Deep Pass)

## Linear Snapshot

| State | Count | Δ from Feb 8 |
|-------|-------|---------------|
| Done | 92 | +17 |
| Backlog | 122 | +77 |
| Todo | 26 | +25 |
| In Progress | 6 | +5 |
| Canceled | 2 | — |
| Duplicate | 2 | — |
| **Total** | **250** | **+124** |

Observation: Backlog grew massively (45→122) due to brainstorm ticket creation. Needs aggressive triage.

---

## Per-Project Analysis

### 1. lockn-logger (Analytics/Billing) — ⚡ HEALTHY
**Recent:** HSTS headers (Feb 9), non-root Docker (Feb 8), CI/CD Phase 3 (Feb 8)
**State:** Operational, security-hardened, CI pipeline complete
**Gaps:**
- LOC-231 (Usage-Based Billing Schema) — Urgent, STILL Backlog. This is THE revenue enabler.
- LOC-225 (Observability Dashboard) — High, deprioritize vs billing
- LOC-296 (Revenue Ledger) — Urgent, depends on LOC-231
**Action needed:** Move LOC-231 to Todo. It gates LOC-236 (Speak metering) and LOC-301 (Gen credits).

### 2. lockn-speak (TTS) — ✅ STABLE
**Recent:** Chatterbox v4 working (Feb 8), non-root Docker, Logger integration
**State:** Functional TTS with Chatterbox backend
**Gaps:**
- LOC-236 (Per-Character Billing) — Revenue blocker, needs LOC-231 first
- LOC-297 (Engine Fallback Router) — Important for SLA but not urgent
- LOC-190 suite (enhancements) — Nice-to-have, defer
**No new tickets needed.** Focus: billing integration once Logger billing schema ships.

### 3. lockn-listen (STT) — 🟡 BOOTSTRAPPED, NEEDS IMPLEMENTATION
**Recent:** Repo created, streaming fix, non-root Docker (all Feb 8)
**State:** FastAPI shell exists but NO Whisper integration yet
**Gaps:**
- LOC-227 (Whisper STT) — Urgent, Backlog. The core service doesn't work.
- LOC-259 (Error handling) — Urgent, good to pair with LOC-227
- LOC-233 (Platform integration) — Blocked on LOC-227
**Action needed:** LOC-227 should be Todo and top priority for Listen.

### 4. lockn-ai-platform — 🔴 PR BOTTLENECK (9 OPEN PRs!)
**Recent:** HSTS headers, Ship integration, demo features (Feb 8-9)
**State:** 9 open PRs all from Feb 8 — nothing merged in 24h
**Critical PRs blocking revenue:**
- PR #19: Stripe checkout (LOC-256)
- PR #20: Landing v2 (LOC-255)
- PR #22: Public trial flow (LOC-257)
- PR #21: Waitlist activation (LOC-270)
**Created LOC-341** to clear this bottleneck with merge ordering.

### 5. lockn-score (Sports Scoring) — 🟡 MVP INCOMPLETE
**Recent:** Auth0 stabilization (Feb 9), non-root Docker (Feb 8)
**State:** Basic audio detection works, Auth0 integrated, but no E2E flow
**Gaps:**
- LOC-200 (Ping Pong MVP) and subtasks (LOC-202-205) all Backlog
- LOC-188/228/232 — Three overlapping E2E tickets. Consolidate.
- LOC-186/187 — Vision + Audio pipelines need implementation
- LOC-295 — User submitted suggestion (Pac-Man resize) — low priority
**Action needed:** Consolidate E2E tickets. Move LOC-202 (Rally counter) to Todo as the next Score priority after platform PR merge.

### 6. lockn-gen (Image Generation) — 🔴 STALLED
**Recent:** Release fixes only (Feb 8). Last feature: Feb 3 (Admin Dashboard)
**State:** 14 backlog tickets accumulating. No clear direction.
**Created LOC-343** — Ship-or-Shelve decision. Recommending Option A (ship image-only MVP).

### 7. lockn-swap (XRPL Trading) — 🆕 JUST SCAFFOLDED
**Recent:** Created today (Feb 9), .NET solution scaffolded
**State:** LOC-323 parent + 10 subtasks (LOC-324-332). LOC-325 In Progress.
**Risk:** New project competing for bandwidth with revenue pipeline.
**Note:** This is a potentially high-value play (crypto arbitrage) but requires significant infrastructure.

### 8. lockn-loader (RAG Ingestion) — ✅ COMPLETE
**Recent:** Phase 1 complete (Feb 8) — document loaders, multi-collection, chunk config
**State:** All 7 subtasks Done (LOC-247-253).

---

## Critical Path to $500/mo Revenue

```
LOC-341 (Merge 9 PRs) ──→ LOC-256 (Stripe) + LOC-257 (Trial)
                              │                    │
                              ▼                    ▼
                         LOC-342 (E2E Smoke Test)
                              │
                              ▼
                         LOC-271 (Paid Onboarding)
                              │
                              ▼
                         LOC-309 (Self-Serve Checkout)
                              │
                              ▼
                         FIRST REVENUE 💰
```

**Parallel track:** LOC-231 (Billing Schema) → LOC-236 (Speak Metering) → LOC-242 (Shared Billing SDK)

---

## New Tickets Created

| Ticket | Priority | Project | Rationale |
|--------|----------|---------|-----------|
| LOC-341 | Urgent | Platform | 9 stale PRs blocking revenue pipeline |
| LOC-342 | Urgent | Revenue | E2E payment flow validation |
| LOC-343 | High | Gen | Ship-or-shelve decision needed |

---

## Kimi AM Brainstorm Comparison

**No Kimi AM brainstorm found for Feb 9.** The cron may not have run or gateway was unavailable (Sean had GPU driver issues causing black screen this afternoon). Previous brainstorm (Feb 8) identified Score as critical path — this analysis agrees but adds urgency on the platform PR bottleneck.

---

## Priority Recommendations

### Immediate (This Week)
1. **LOC-341** — Merge 9 platform PRs (blocks everything)
2. **LOC-256/257** — Verify Stripe + Trial after merge
3. **LOC-342** — E2E smoke test the payment funnel
4. **LOC-343** — Sean decides Gen's fate

### Next Sprint
5. **LOC-231** — Billing schema (gates all metering)
6. **LOC-227** — Whisper STT implementation
7. **LOC-271** — Paid onboarding wizard
8. **LOC-202** — Rally counter (Score MVP progress)

### Backlog Hygiene
- Consolidate LOC-188/228/232 (three E2E Score tickets)
- LOC-287-294 — Ship suggestion tickets (auto-created, mostly noise) — bulk close or label
- LOC-109 — ML Runtime spike, In Progress since forever — close or timebox
