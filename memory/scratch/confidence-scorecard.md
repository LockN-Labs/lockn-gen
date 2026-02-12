# LockN Full Stack Confidence Scorecard
**Audit Date:** 2026-02-11 19:55 EST
**Target:** Every flow ≥ 9.81/10.00
**Auditor:** Claws (automated + manual)

---

## INFRASTRUCTURE LAYER

| Component | Container | Health | Dev URL | Test URL | Score |
|-----------|-----------|--------|---------|----------|-------|
| Caddy (routing) | ✅ Up 7h | ✅ | ✅ 200 | ✅ 200 | **9.50** |
| Cloudflare Tunnel | ✅ Up 7h | ✅ | ✅ | ✅ | **9.50** |
| Grafana (observability) | ✅ Up 7h | ✅ | — | — | **8.00** |
| OTel Collector | ✅ Up 7h | ✅ | — | — | **8.00** |
| Qdrant (vector DB) | ✅ Up 6h | ✅ | — | — | **8.50** |

**Infra subscore: 8.70** — No automated infra tests. Healthy but untested resilience.

---

## LOCKN AI PLATFORM (lockn-ai-platform)

| Flow | E2E Tests | Tests Pass? | Health | Score | Gap |
|------|-----------|-------------|--------|-------|-----|
| Landing Page | 20 tests | ❌ BROKEN | ✅ 200 | **3.00** | Playwright version conflict — 0 tests run |
| Speak | 18 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same Playwright error |
| Listen | 7 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Look | 8 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Sense | 7 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Brain | 7 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Logger | 7 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Portfolio | 6 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Waitlist | 5 tests | ❌ BROKEN | ✅ 200 | **3.00** | Same |
| Ship | 0 tests | — | ✅ 200 | **2.00** | No E2E tests at all |
| Cross-Nav | 10 tests | ❌ BROKEN | — | **3.00** | Same Playwright error |
| API Health | 15 tests | ❌ BROKEN | — | **3.00** | Same |
| Smoke | 6 tests | ❌ BROKEN | — | **3.00** | Same |

**Platform subscore: 2.92** — 🔴 CRITICAL. 116 tests exist but ZERO run. Playwright has a dual-version conflict (`test.describe()` error). The entire E2E suite is non-functional.

**Root cause:** `Error: Playwright Test did not expect test.describe() to be called here` — two different versions of `@playwright/test` in dependency tree.

---

## LOCKN AUTH (lockn-auth) — .NET 9

| Flow | Unit Tests | Tests Pass? | Container | Health | Score |
|------|-----------|-------------|-----------|--------|-------|
| API Key CRUD | 11 tests | ✅ ALL PASS | ✅ healthy | ⚠️ No /health endpoint | **7.50** |
| Auth0 Login | 0 tests | — | ✅ | — | **4.00** |
| Waitlist Signup | 0 tests | — | ✅ | — | **4.00** |
| Invite Tokens | 0 tests | — | ✅ | — | **4.00** |
| Drip Emails | 0 tests | — | ✅ | — | **4.00** |

**Auth subscore: 4.70** — 🟡 Only API key CRUD has test coverage. Auth flows, waitlist, invites, emails all untested.

---

## LOCKN SCORE (lockn-score) — Python

| Flow | Tests | Tests Pass? | Container | Score |
|------|-------|-------------|-----------|-------|
| Vision (ball detect) | ~15 tests | ✅ | ✅ healthy | **8.50** |
| Audio (bounce detect) | ~12 tests | ✅ | ✅ healthy | **8.50** |
| Fusion (rally state) | ~10 tests | ✅ | ✅ healthy | **8.50** |
| Integration | ~12 tests | ✅ | ✅ healthy | **8.50** |
| WebSocket spectator | ~5 tests | ✅ | ✅ | **7.50** |
| Solo mode | ~5 tests | ✅ | ✅ | **7.50** |
| Confidence system | EXISTS | ❌ cv2 missing | — | **6.00** |

**Score subscore: 7.86** — 🟡 68 pass, 3 skipped. Best-tested service. But confidence.py (the scoring runner itself) is broken due to missing cv2 dependency. No load testing.

---

## LOCKN VOICE (lockn-voice)

| Flow | Tests | Health | Score |
|------|-------|--------|-------|
| TTS API | 0 tests | ✅ 200 | **4.00** |
| Voice Cloning | 0 tests | — | **2.00** |

**Voice subscore: 3.00** — 🔴 Zero test coverage. Service runs but completely untested.

---

## LOCKN SPEAK (lockn-speak)

| Flow | Tests | Container | Score |
|------|-------|-----------|-------|
| Speak API | 0 dedicated | ✅ Up 7h | **4.00** |
| Speak DB | — | ✅ Up 6h | **5.00** |

**Speak subscore: 4.50** — 🔴 No dedicated test suite.

---

## WHISPER / PANNS (AI Services)

| Service | Container | Health | Tests | Score |
|---------|-----------|--------|-------|-------|
| Whisper GPU (STT) | ✅ Up 3h (healthy) | ✅ | 0 | **5.00** |
| PANNs (audio classify) | ✅ Up 6h (healthy) | ✅ | 0 | **5.00** |
| Qwen3 TTS | ✅ Up 6h | — | 0 | **4.00** |
| Chatterbox | ✅ Up 3h | — | 0 | **3.00** |

**AI Services subscore: 4.25** — 🔴 All running, zero tested.

---

## 📊 AGGREGATE SCORECARD

| Layer | Subscore | Weight | Weighted |
|-------|----------|--------|----------|
| Infrastructure | 8.70 | 15% | 1.31 |
| Platform (E2E) | 2.92 | 30% | 0.88 |
| Auth | 4.70 | 15% | 0.71 |
| Score | 7.86 | 15% | 1.18 |
| Voice | 3.00 | 10% | 0.30 |
| Speak | 4.50 | 5% | 0.23 |
| AI Services | 4.25 | 10% | 0.43 |

## **OVERALL CONFIDENCE: 5.02 / 10.00** 🔴

---

## 🚨 CRITICAL GAPS (to reach 9.81)

### P0 — Blocking (must fix first)
1. **Playwright version conflict** — Fix dual `@playwright/test` versions. This alone blocks 116 tests from running. One `npm dedupe` or dependency pin could restore the entire E2E suite.
2. **Missing cv2 in Score test env** — `pip install opencv-python-headless` fixes the confidence runner.
3. **Auth health endpoint** — Service returns 404 on every health path. Need `/health` endpoint.

### P1 — Coverage gaps
4. **Voice service** — Zero tests. Need: TTS request/response test, voice cloning test, error handling.
5. **Auth flows** — Auth0 login, waitlist signup, invite tokens, drip emails all untested. Need integration tests.
6. **Speak API** — No dedicated tests. Need API contract tests.
7. **AI services** — Whisper, PANNs, Qwen3-TTS, Chatterbox all need health + functional tests.

### P2 — Hardening
8. **Load testing** — Zero load tests across entire stack.
9. **Error handling tests** — No negative/edge case testing outside Score.
10. **Infra resilience** — No container restart/failover tests.
