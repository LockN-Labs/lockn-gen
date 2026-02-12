# LOC-255: Landing Page v2 — Conversion Funnel Architecture

**Status:** Architecture Complete | **Priority:** CRITICAL  
**Date:** 2026-02-08 | **Author:** Research Agent

---

## 1. System Overview

```
                    ┌─────────────────────────────────────┐
                    │         PUBLIC LANDING PAGE          │
                    │     /landing (no auth required)      │
                    │                                      │
                    │  Hero → Value Props → Social Proof   │
                    │       → Waitlist CTA Form            │
                    └──────────────┬───────────────────────┘
                                   │ POST /api/waitlist
                    ┌──────────────▼───────────────────────┐
                    │        PLATFORM API (Express)        │
                    │     POST /api/waitlist/signup         │
                    │     POST /api/waitlist/confirm/:token │
                    │     GET  /api/waitlist/status/:email  │
                    └──┬───────────┬───────────────────────┘
                       │           │
              ┌────────▼──┐  ┌─────▼──────────┐
              │   Auth0    │  │   Postmark     │
              │ Pre-signup │  │ Transactional  │
              │ User Store │  │ Email          │
              └────────────┘  └────────────────┘
```

---

## 2. Frontend Architecture

### 2.1 Route: `/landing` (Public, No Auth)

Add to `lockn-score/web/src/App.tsx` — sits **outside** the authenticated shell.

### 2.2 Component Tree

```
<LandingPage>
  ├── <LandingHero />           # Headline, subhead, primary CTA
  ├── <ValuePropositions />     # 3 feature cards with icons
  ├── <SocialProof />           # Testimonials / beta user count
  ├── <WaitlistForm />          # Email input + submit (the conversion point)
  │   ├── UTM param capture (hidden fields from URL)
  │   └── <WaitlistConfirmation /> # Success state after submit
  ├── <PricingPreview />        # Anchor $5/mo price, show value
  └── <LandingFooter />         # Minimal footer, legal links
```

### 2.3 Key Frontend Files

| File | Purpose |
|------|---------|
| `src/pages/Landing.tsx` | Page component, UTM extraction |
| `src/components/landing/WaitlistForm.tsx` | Email capture form |
| `src/components/landing/LandingHero.tsx` | Above-the-fold hero |
| `src/components/landing/ValuePropositions.tsx` | Feature cards |
| `src/components/landing/SocialProof.tsx` | Trust signals |
| `src/components/landing/PricingPreview.tsx` | Price anchoring |
| `src/hooks/useUtmParams.ts` | Extract/persist UTM from URL |
| `src/hooks/useWaitlistSubmit.ts` | API call + state management |

### 2.4 UTM Tracking Hook

```typescript
// src/hooks/useUtmParams.ts
export function useUtmParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    utm_source: params.get('utm_source') ?? sessionStorage.getItem('utm_source') ?? undefined,
    utm_medium: params.get('utm_medium') ?? undefined,
    utm_campaign: params.get('utm_campaign') ?? undefined,
    referrer: document.referrer || undefined,
  };
}
```

On mount, persist to `sessionStorage` so they survive navigation within the SPA.

---

## 3. API Endpoints

All added to `platform-api` (Express, already has Stripe routes).

### 3.1 `POST /api/waitlist/signup`

```typescript
// Request
{
  email: string;           // required, validated
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  referrer?: string;
}

// Response 201
{
  status: "pending_confirmation";
  message: "Check your email to confirm.";
}

// Response 409
{ error: "already_registered" }
```

**Logic:**
1. Validate email format
2. Check if already exists → 409
3. Generate confirmation token (crypto.randomUUID())
4. Store waitlist entry with `status: "pending"`
5. Send double opt-in email via Postmark
6. Fire `waitlist_submit` conversion event
7. Return 201

### 3.2 `GET /api/waitlist/confirm/:token`

```typescript
// Response 200 — renders redirect to /landing?confirmed=true
```

**Logic:**
1. Look up token → validate not expired (24h TTL)
2. Update status to `"confirmed"`
3. Create Auth0 pre-user (Management API) with `app_metadata: { waitlistPosition, accessTier: "waitlist" }`
4. Send welcome email via Postmark
5. Fire `waitlist_confirmed` conversion event
6. Redirect to `/landing?confirmed=true`

### 3.3 `GET /api/waitlist/status/:email`

```typescript
// Response 200
{
  status: "pending" | "confirmed" | "beta" | "paid";
  position?: number;
  estimatedAccess?: string;  // "Early March 2026"
}
```

---

## 4. Data Model

### 4.1 Option A: Auth0-Native (Recommended for MVP)

No separate database. Store everything in Auth0 user `app_metadata`:

```json
{
  "waitlistPosition": 42,
  "accessTier": "waitlist",
  "waitlistSignupDate": "2026-02-10T12:00:00Z",
  "waitlistConfirmedDate": "2026-02-10T12:05:00Z",
  "utmSource": "twitter",
  "utmCampaign": "launch-feb-2026",
  "referrer": "https://twitter.com/..."
}
```

**Confirmation tokens:** Use a simple in-memory Map with TTL (or Redis if available). For MVP at <1000 users, a `Map<string, {email, expiry}>` is fine.

### 4.2 Option B: SQLite/PostgreSQL (Scale Path)

If we outgrow Auth0 metadata:

```sql
CREATE TABLE waitlist_entries (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  status        TEXT NOT NULL DEFAULT 'pending',  -- pending/confirmed/beta/paid
  position      INT,
  confirm_token TEXT UNIQUE,
  token_expires TIMESTAMPTZ,
  auth0_user_id TEXT,
  utm_source    TEXT,
  utm_medium    TEXT,
  utm_campaign  TEXT,
  referrer      TEXT,
  created_at    TIMESTAMPTZ DEFAULT now(),
  confirmed_at  TIMESTAMPTZ,
  promoted_at   TIMESTAMPTZ
);

CREATE INDEX idx_waitlist_email ON waitlist_entries(email);
CREATE INDEX idx_waitlist_token ON waitlist_entries(confirm_token);
```

**Recommendation:** Start with **Option A** (Auth0-native). The confirmation token store is the only piece that needs local state — use a simple Map with cleanup interval. Migrate to Option B when approaching 500+ waitlist entries.

---

## 5. Auth0 Integration Points

### 5.1 Pre-Registration (New)

On waitlist confirmation, use Auth0 Management API to create a user:

```typescript
import { ManagementClient } from 'auth0';

const auth0 = new ManagementClient({
  domain: process.env.AUTH0_DOMAIN,
  clientId: process.env.AUTH0_MGMT_CLIENT_ID,
  clientSecret: process.env.AUTH0_MGMT_CLIENT_SECRET,
});

// Create pre-registered user
await auth0.users.create({
  connection: 'Username-Password-Authentication',
  email,
  password: crypto.randomBytes(32).toString('hex'), // Random, user resets later
  app_metadata: {
    accessTier: 'waitlist',
    waitlistPosition: nextPosition,
  },
});
```

### 5.2 Existing Auth0 Actions (from LOC-144)

The existing `assign-waitlist-role` action already handles:
- Assigning `waitlist-member` role on signup
- Setting initial `app_metadata`

**No changes needed** to existing Auth0 actions.

### 5.3 Promotion Flow (Admin)

Reuse existing `/admin/invites` page. When promoting:
1. Update `app_metadata.accessTier` → `"beta"`
2. Assign `beta-tester` role
3. Trigger Postmark promotion email

---

## 6. Conversion Tracking Pipeline

### 6.1 Event Schema

```typescript
interface ConversionEvent {
  event: 'page_view' | 'waitlist_submit' | 'waitlist_confirmed' | 'beta_activated' | 'paid_converted';
  email?: string;          // hashed after confirmation
  utm_source?: string;
  utm_campaign?: string;
  utm_medium?: string;
  referrer?: string;
  timestamp: string;       // ISO 8601
  sessionId: string;       // browser session ID
  userAgent: string;
}
```

### 6.2 Implementation (MVP)

For MVP, log events server-side to stdout (structured JSON). Platform API already runs in Docker — logs are captured.

```typescript
// src/services/analytics.ts
export function trackEvent(event: ConversionEvent) {
  console.log(JSON.stringify({ type: 'conversion_event', ...event }));
}
```

**Future:** Pipe to PostHog, Mixpanel, or custom analytics table.

### 6.3 Frontend Events

```typescript
// In Landing.tsx — on mount
trackPageView({ utm_source, utm_campaign, referrer });

// In WaitlistForm.tsx — on submit
trackWaitlistSubmit({ email_hash, utm_source, utm_campaign });
```

For frontend, use a simple `fetch('/api/events/track', ...)` or `navigator.sendBeacon()` for fire-and-forget.

---

## 7. Email Flow (Postmark)

### 7.1 Templates Needed

| Template | Trigger | Content |
|----------|---------|---------|
| `waitlist-confirm` | POST /waitlist/signup | "Confirm your email" + CTA link |
| `waitlist-welcome` | GET /waitlist/confirm/:token | "You're on the list! Position #X" |
| `waitlist-promoted` | Admin promotes user | "You're in! Login to access beta" |

### 7.2 Double Opt-In Flow

```
User submits email
  → API stores with status="pending"
  → Postmark sends "waitlist-confirm" email
  → User clicks confirm link
  → GET /api/waitlist/confirm/:token
  → Status → "confirmed", Auth0 user created
  → Postmark sends "waitlist-welcome" email
  → Redirect to /landing?confirmed=true
```

### 7.3 Postmark Integration

```typescript
import * as postmark from 'postmark';
const client = new postmark.ServerClient(process.env.POSTMARK_API_KEY);

await client.sendEmailWithTemplate({
  From: 'hello@lockn.ai',
  To: email,
  TemplateAlias: 'waitlist-confirm',
  TemplateModel: {
    confirm_url: `${BASE_URL}/api/waitlist/confirm/${token}`,
    product_name: 'LockN Score',
  },
});
```

---

## 8. Environment Strategy

| Environment | URL | Auth0 Tenant | Postmark | Purpose |
|-------------|-----|-------------|----------|---------|
| **Dev** | localhost:5173 | dev tenant | sandbox server | Development |
| **Test** | test.lockn.ai | dev tenant | sandbox server | QA verification |
| **Prod** | lockn.ai/landing | prod tenant | live server | Public traffic |

### 8.1 Environment Variables

```env
# Add to platform-api .env
WAITLIST_CONFIRM_BASE_URL=https://lockn.ai    # per-env
POSTMARK_API_KEY=xxx                           # per-env
AUTH0_MGMT_CLIENT_ID=xxx                       # existing
AUTH0_MGMT_CLIENT_SECRET=xxx                   # existing
```

### 8.2 Deployment Path

```
feature/loc-255-landing-v2  →  PR  →  main  →  Dev auto-deploy
                                              →  Manual promote to Test
                                              →  QA pass → Promote to Prod
```

---

## 9. Testing Strategy

### 9.1 Unit Tests

| Test | Scope |
|------|-------|
| Email validation | Reject invalid formats, accept valid |
| Token generation/expiry | Token created, expires after 24h |
| Duplicate detection | 409 on re-submit |
| UTM param extraction | Parse from URL correctly |

### 9.2 Integration Tests

| Test | Scope |
|------|-------|
| Full signup flow | Submit → email sent → confirm → user created |
| Postmark template rendering | Templates render with correct variables |
| Auth0 user creation | User appears in Auth0 with correct metadata |

### 9.3 E2E / Conversion Tests

| Test | Scope |
|------|-------|
| Landing page loads < 2s | Performance budget |
| Form submits successfully | Happy path |
| Confirmation email received | Postmark sandbox |
| Confirmed user can login | Auth0 round-trip |
| UTM params persist through flow | Attribution accuracy |

### 9.4 Conversion Metrics to Track Post-Launch

| Metric | Target | How |
|--------|--------|-----|
| Page → Form visible | >80% scroll rate | Intersection Observer |
| Form visible → Submit | >15% conversion | Event tracking |
| Submit → Confirm email | >60% confirm rate | Postmark + DB |
| Confirm → Beta activate | Manual promotion | Admin tracking |
| Beta → Paid ($5/mo) | >20% conversion | Stripe data |

---

## 10. Implementation Order (Estimated: 16h)

| Phase | Task | Effort | Depends On |
|-------|------|--------|------------|
| 1 | API: `POST /waitlist/signup` + token store | 2h | — |
| 2 | API: `GET /waitlist/confirm/:token` + Auth0 | 2h | Phase 1 |
| 3 | Postmark templates (confirm + welcome) | 2h | — |
| 4 | Frontend: `Landing.tsx` + hero + form | 4h | — |
| 5 | Frontend: UTM hooks + tracking | 1h | Phase 4 |
| 6 | Frontend: Value props + social proof + pricing | 2h | Phase 4 |
| 7 | Integration testing | 2h | Phases 1-6 |
| 8 | Deploy to Test + QA | 1h | Phase 7 |

**Phases 1, 3, 4 can run in parallel.**

---

## 11. Conversion Optimization Recommendations

1. **Single CTA above the fold** — Email input + "Join the Waitlist" button. No distractions.
2. **Social proof counter** — "Join 47 others already on the waitlist" (query Auth0 user count).
3. **Price anchor early** — Show "$5/month" prominently. At this price point, the decision is impulse-level.
4. **Urgency without sleaze** — "Limited beta spots" is true and creates action.
5. **Mobile-first design** — 60%+ of traffic will be mobile from social campaigns.
6. **< 3 second load time** — No heavy dependencies on the landing page. Lazy-load everything below fold.
7. **Confirmation page upsell** — After email confirm, show "Share with a friend, skip the line" referral CTA.

---

## 12. Open Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Token storage | In-memory Map vs Redis vs SQLite | Map for MVP (<500 users) |
| Analytics provider | Console logs vs PostHog vs Mixpanel | Console logs → PostHog later |
| Landing page location | Same SPA vs separate static page | Same SPA (simpler deployment) |
| A/B testing | None vs simple feature flags | Skip for v1, add when >100 visits/day |
