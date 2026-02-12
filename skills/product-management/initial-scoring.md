# Initial Backlog Scoring — PM Agent (2026-02-09 21:45 EST)

## Scoring: `Score = (Revenue×3 + Reach×2 + Confidence×1) / (Effort×1.5)`

| Ticket | Title | Rev | Reach | Conf | Effort | Score | Notes |
|--------|-------|-----|-------|------|--------|-------|-------|
| **LOC-309** | Self-Serve Stripe Checkout | 10 | 8 | 8 | 5 | **7.7** | Direct $ — first paid users. Foundation for everything. |
| **LOC-325** | XRPL WebSocket Client | 9 | 6 | 8 | 4 | **7.3** | Foundation for Swap/Swing — potential daily rev from arbitrage |
| **LOC-311** | 15-Min Onboarding Path | 8 | 9 | 7 | 5 | **6.9** | Depends on LOC-309 (checkout) |
| **LOC-271** | Paid Onboarding Wizard | 8 | 8 | 7 | 6 | **6.1** | Overlaps LOC-311 — combine or sequence |
| **LOC-332** | Risk Manager (stop-loss) | 8 | 4 | 9 | 5 | **6.1** | Critical safety for trading — must ship before live capital |
| **LOC-326** | Arb Detection Engine | 9 | 5 | 7 | 6 | **5.8** | Depends on LOC-325 |
| **LOC-330** | Capital Allocator | 8 | 5 | 8 | 6 | **5.6** | Depends on LOC-325 |
| **LOC-335** | Finer Daily Log Chunking | 2 | 8 | 9 | 3 | **5.6** | Internal infra but high reach (all agents benefit) |
| **LOC-305** | API Quickstart Kits | 7 | 8 | 8 | 4 | **5.5** | Depends on LOC-309 |
| **LOC-347** | API Monetization Guardrails | 9 | 7 | 6 | 7 | **5.3** | Depends on LOC-309 |
| **LOC-336** | Recency Boost Memory | 2 | 8 | 8 | 4 | **4.7** | Internal infra |
| **LOC-303** | Waitlist Lead Scoring | 7 | 6 | 6 | 5 | **5.2** | Depends on waitlist having traffic |
| **LOC-310** | Waitlist Referral Loop | 6 | 7 | 7 | 5 | **5.1** | Growth multiplier |
| **LOC-302** | Landing Page A/B Tests | 6 | 8 | 5 | 5 | **4.8** | Needs traffic to test |
| **LOC-304** | Stripe Dunning | 7 | 5 | 7 | 5 | **5.1** | Needs paying users first |
| **LOC-345** | Waitlist-to-Checkout Fast Lane | 7 | 6 | 7 | 4 | **5.8** | Quick win after LOC-309 |
| **LOC-344** | Landing Trust Stack | 5 | 8 | 5 | 4 | **4.5** | Content/design heavy |
| **LOC-312** | Marketing Launch Ops | 5 | 6 | 4 | 6 | **3.6** | Process design, less code |
| **LOC-348** | Weekly Growth OS | 4 | 5 | 5 | 5 | **3.7** | Needs data to operate on |
| **LOC-346** | Payments Recovery v2 | 7 | 5 | 6 | 6 | **4.6** | Dup of LOC-304 |
| **LOC-338** | Query Expansion Memory | 2 | 7 | 8 | 3 | **4.9** | Internal infra |
| **LOC-339** | Enrich Chunks w/ Tickets | 2 | 6 | 8 | 3 | **4.4** | Internal infra |

## PM Decisions

### Priority Lanes (parallel execution):

**Lane 1: Revenue Pipeline (LockN Auth/Platform)**
1. **LOC-309** (Stripe Checkout) → Score 7.7 — START NOW
2. LOC-311 (Onboarding) → after LOC-309
3. LOC-305 (Quickstart Kits) → after LOC-309

**Lane 2: Trading Revenue (LockN Swap/Swing)**
1. **LOC-325** (XRPL WebSocket) → Score 7.3 — START NOW
2. LOC-332 (Risk Manager) → parallel with LOC-326
3. LOC-326 (Arb Detection) → after LOC-325

**Lane 3: Infrastructure (Memory Search)**
1. **LOC-335** (Chunking) → Score 5.6 — START NOW (quick win, Urgent)
2. LOC-336 (Recency) → after LOC-335

### Duplicate Detection:
- LOC-304 and LOC-346 are near-duplicates (Stripe dunning). **Mark LOC-346 as dup of LOC-304.**
- LOC-271 and LOC-311 overlap significantly. **Sequence: LOC-309 → LOC-311 → LOC-271 as enhancement.**
