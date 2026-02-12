# Backlog Refinement Analysis — 2026-02-08 Morning Pass

## Linear Snapshot Summary

```
By State:
  Done: 75 tickets (incl LOC-1 through LOC-175 core pipeline)
  In Progress: 1 ticket (LOC-172: Local Compute Maximization)
  Todo: 1 ticket (LOC-239: Gen Sprint Plan)
  Backlog: 45+ tickets (needs triage)
```

```
By Project (P=Priority, 🅱️=Backlog, 🔴=In Progress, ✅=Done):

LockN Logger (Analytics/Billing): ✅ LOC-211/212/213 | 🅱️ LOC-231 (P1 billing)
LockN Speak (TTS): ✅ LOC-210 | 🅱️ LOC-236 (P2 metering), LOC-190 (P3 enhancements)
LockN Listen (STT): 🔴 LOC-206 | 🅱️ LOC-227(P1), LOC-233(P1)
LockN Score (Sports): 🅱️ LOC-200(P1), LOC-201-205, LOC-186-189, LOC-226-228
LockN Gen (Image Gen): 🔴 LOC-239 (Sprint Plan) | 🅱️ LOC-209, 229, 234
LockN Auth: 🅱️ LOC-224(P2), LOC-237(P2)
LockN Platform: ✅ LOC-214/215 | 🅱️ LOC-208(P2), LOC-235(P2)
```

---

## Per-Project Analysis

### 1. LockN Score — Sports Market MVP 🎯 CRITICAL PATH
**Revenue Connection:** Most direct path to $500/mo — sports leagues/pickleball clubs
**Current State:** Basic audio working (LOC-201 Done), vision needs work, fusion missing
**Critical Gap:** No E2E flow from camera → scoreboard → history

| Ticket | State | Risk | Revenue Impact |
|--------|-------|------|----------------|
| LOC-186 | 🅱️ P1 | HIGH | No vision = can't track ball |
| LOC-187 | 🅱️ P1 | HIGH | Audio alone can't score games |
| LOC-188 | 🅱️ P1 | HIGH | No fusion = no working product |
| LOC-228 | 🅱️ P1 | HIGH | Duplicate of LOC-188 essentially |
| LOC-226 | 🅱️ P2 | MED | GTM strategy needed |
| LOC-189 | 🅱️ P3 | LOW | Tests can come later |

**Action:** Merge LOC-188/LOC-228 (duplicate). Prioritize LOC-186→LOC-187→LOC-188 chain.
**Tech Debt:** Need to verify YOLOv8 can track table tennis balls at high speeds.

---

### 2. LockN Listen — STT Service (Foundation for Agent Pipeline)
**Revenue Connection:** Enables voice commands → expands Score UX, enables future apps
**Current State:** Repository bootstrapped (LOC-206 Done), needs full implementation
**Critical Gap:** No Whisper integration, no streaming, no API keys

| Ticket | State | Risk | Dependency |
|--------|-------|------|------------|
| LOC-227 | 🅱️ P1 | HIGH | Blocked on LOC-233 for auth |
| LOC-233 | 🅱️ P1 | HIGH | Needs Auth service first |

**Action:** Create LOC-XX to implement Whisper FastAPI. Note dependency on LOC-224 (Auth).
**Tech Debt:** Consider if streaming needed for MVP or can be REST-only.

---

### 3. LockN Speak — TTS Service (Quality & Billing)
**Revenue Connection:** Per-character billing = direct monetization
**Current State:** Crisis resolved (LOC-210 Done, Chatterbox v4 working)
**Critical Gap:** No usage metering, no voice personas

| Ticket | State | Risk | Action |
|--------|-------|------|--------|
| LOC-236 | 🅱️ P2 | HIGH | Revenue blocker — implement first |
| LOC-170 | 🅱️ P3 | MED | Fix Describe Voice |
| LOC-190 | 🅱️ P3 | LOW | Fancy features — defer |

**Action:** Prioritize LOC-236 to P1 (billing). LOC-190 features are nice-to-have.

---

### 4. LockN Gen — Image Generation (Stalled Project)
**Revenue Connection:** Potential NFT/art market, but lower priority than Score
**Current State:** Completely stalled — LOC-239 just created today (Todo)
**Critical Gap:** No scope defined, no dev environment, no integration

| Ticket | State | Risk | Recommendation |
|--------|-------|------|----------------|
| LOC-239 | 🔴 P2 | HIGH | Needs immediate sprint planning |
| LOC-234 | 🅱️ P1 | HIGH | ComfyUI deploy blocked by LOC-239 |
| LOC-229 | 🅱️ P2 | MED | Platform integration blocked |

**Decision Required:** 
- Option A: Archive Gen, focus on Score (revenue-first)
- Option B: Minimal Gen effort — just enough for platform completeness
- Option C: Full Gen sprint (delays Score by ~2 weeks)

**Recommendation:** Option B — minimal integration so platform has all services, but don't build Gen features until Score is revenue-ready.

---

### 5. LockN Logger — Analytics & Billing Foundation
**Revenue Connection:** Required infrastructure for usage-based billing
**Current State:** Core infrastructure done (aggregation, OTEL, dashboard)
**Critical Gap:** No billing schema, no per-service metering

| Ticket | State | Risk | Action |
|--------|-------|------|--------|
| LOC-231 | 🅱️ P1 | HIGH | Blocking Speak/Listen billing |

**Note:** LOC-231 should have successors: LOC-236 (Speak metering), LOC-237 (Auth provisioning). Update ticket.

---

### 6. LockN Auth — Identity & API Keys
**Revenue Connection:** Required for multi-tenant, required for API resale
**Current State:** Waitlist system done (LOC-144), but API key service not started
**Critical Gap:** No automated key provisioning = can't sell API access

| Ticket | State | Risk | Blocking |
|--------|-------|------|----------|
| LOC-224 | 🅱️ P2 | HIGH | Blocks Listen, Gen, Platform integration |
| LOC-237 | 🅱️ P2 | HIGH | Depends on LOC-231 (billing schema) |

**Action:** Make LOC-224 P1. It's foundational — can't sell API access without it.

---

### 7. LockN Platform — Landing Page & Integration
**Revenue Connection:** Waitlist → paid conversion funnel
**Current State:** Auth/CI/CD done, but no public presence
**Critical Gap:** No landing page, no automated deployment

| Ticket | State | Risk | Priority |
|--------|-------|------|----------|
| LOC-235 | 🅱️ P2 | HIGH | Waitlist conversion depends on it |
| LOC-208 | 🅱️ P2 | HIGH | Blocks test environment testing |

---

## Critical Path to Revenue ($500/mo)

```
Phase 1: Foundation (Weeks 1-2)
├── LOC-224 [Auth API Keys] — P1 ↑ from P2
├── LOC-231 [Logger Billing Schema] — P1
└── LOC-235 [Platform Landing Page] — P2 → P1

Phase 2: Core Services (Weeks 2-4)
├── LOC-227 [Listen Whisper STT] — P1
├── LOC-236 [Speak Usage Metering] — P1 ↑ from P2
└── LOC-233 [Listen Platform Integration] — P1

Phase 3: Score MVP (Weeks 4-6)
├── LOC-186 [Score Vision Pipeline] — P1
├── LOC-187 [Score Audio Pipeline] — P1 (depends on Listen)
├── LOC-188 [Score E2E Fusion] — P1 (depends on 186+187)
└── LOC-226 [Score GTM Strategy] — P2 (parallel)

Phase 4: Monetization (Week 6+)
├── Beta testing with early access customers
├── Usage billing activation
└── First paid conversions
```

## Ticketing Actions

### Create New Tickets
1. **LOC-XXX:** Merge LOC-188 + LOC-228 (duplicate E2E tickets)
2. **LOC-XXX:** Score Vision Pipeline dependencies — YOLOv8 ball tracking research
3. **LOC-XXX:** Platform automated smoke test suite for deploy-to-test
4. **LOC-XXX:** Chatterbox TTS health monitoring (alert if 502s return)

### Update Existing Tickets
1. **LOC-224:** Upgrade P2 → P1 ([Auth] foundational for all services)
2. **LOC-231:** Add successors LOC-236, LOC-237
3. **LOC-236:** Upgrade P2 → P1 (revenue critical)
4. **LOC-239:** Add description — "Decision: Minimal integration, defer features"

### Close Stale Tickets
- **LOC-171:** [Spike] pre-synthesis padding — no action since Jan, low value → Close
- **LOC-220:** Continuous GPU monitoring — superseded by LOC-225 observability → Close as duplicate

---

## Big Picture Assessment

**Q: How does each project move toward $500/mo?**

| Project | Revenue Path | Confidence | Priority |
|---------|--------------|------------|----------|
| **Score** | Sports leagues, pickleball clubs, table tennis tournaments | HIGH | P1 |
| **Speak** | Per-character TTS API resale | MEDIUM | P2 |
| **Listen** | STT API resale, Score feature enablement | MEDIUM | P2 |
| **Auth** | Required for multi-tenant, API resale | HIGH | P1 (infrastructure) |
| **Logger** | Required for billing infrastructure | HIGH | P1 (infrastructure) |
| **Platform** | Waitlist → paid conversion funnel | MEDIUM | P1 (GTM) |
| **Gen** | Art/NFT market, creative tools | LOW | P3 (defer until Score works) |

**Q: What's the critical path?**
Score MVP (LOC-186→187→188 chain) is the only direct revenue play right now. Everything else is infrastructure that enables Scale. Auth/Logger are P1 because they block Score's monetization.

**Recommendation:** 
- Keep Gen in minimal mode (LOC-239 → just enough for platform completeness)
- Full focus on Score MVP + infrastructure
- Once Score is beta-ready, pivot to GTM (LOC-226) while polishing other services
