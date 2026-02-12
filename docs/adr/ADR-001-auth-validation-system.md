# ADR-001: Auth Validation & Config Drift Detection System

**Status:** Accepted  
**Date:** 2026-02-10  
**Author:** Sean (via OpenClaw)  
**Triggered by:** Auth cascade incident (2026-02-10)

## Context

On 2026-02-10, three stacked auth issues blocked all users for 45 minutes:

1. **Auth0 Action SDK mismatch** — A silent `try/catch` in the post-login Action swallowed an SDK version error, causing roles to be empty. With empty roles, every user was denied access.
2. **Legacy Caddy basic_auth gate** — A "temporary" basic_auth block in Caddy had no expiration tracking. It persisted long past its intended lifetime.
3. **Missing Auth0 callback URLs** — Per-page callback URL registration meant new pages required manual Auth0 dashboard updates. Missing URLs caused redirect failures.

No single issue was catastrophic, but stacked together they created a total auth failure with no clear error messaging.

## Decision

We implement a layered auth validation system:

### 1. Single Callback Route (LOC-425)
Replace per-page Auth0 callback URLs with a single `/auth/callback` route that stores and restores the user's intended destination via `sessionStorage`.

**Rationale:** Industry standard for SPAs. Auth0's own docs recommend minimal callback URLs. Eliminates the class of "forgot to add callback URL" errors entirely.

### 2. Post-Deploy Auth Smoke Tests (LOC-426)
Automated tests that run after every deploy and every 6 hours, validating:
- Login flow completes
- Token contains expected claims (roles non-empty)
- Callback URL resolves
- Silent token renewal works

**Rationale:** Auth flows are high-impact but rarely tested post-deploy. Smoke tests catch SDK mismatches, config drift, and infrastructure changes before users hit them.

### 3. Temporary Security Gate Tracker (LOC-427)
All temporary security measures (basic_auth gates, firewall rules, feature flags used as security controls) must be registered in `temp-gates.json` with:
- Expiration date
- Linear ticket
- Owner
- Removal instructions

Automated checks alert on expired gates.

**Rationale:** "Temporary" measures becoming permanent is a well-documented DevOps anti-pattern. Explicit tracking with expiration enforcement prevents this.

### 4. Config Drift Detection
A script (`drift-check.sh`) runs every 6 hours and checks:
- Caddy config matches repo (no untracked basic_auth blocks)
- Auth0 callback URLs match expected set
- No expired temporary security gates
- Auth endpoints are reachable

**Rationale:** Configuration drift is the root cause of most "it worked yesterday" incidents. Continuous comparison against desired state catches drift early.

### 5. Auth Error Surfacing (auth-guard skill)
All auth error handlers must:
- Log structured JSON with error codes
- Surface errors to users (never silent catch + redirect)
- Report to monitoring system
- Include reference codes for debugging

**Rationale:** The incident's 45-minute resolution time was largely due to silent error handling hiding the root cause.

## Consequences

**Positive:**
- Auth failures detected in minutes, not when users report them
- No more "temporary" security measures becoming permanent
- Config drift caught before it causes incidents
- Clear error messages reduce MTTR

**Negative:**
- Additional monitoring infrastructure to maintain
- Smoke tests need Auth0 test credentials (secret management overhead)
- Drift detection script needs access to Caddy admin API and Auth0 Management API

## Alternatives Considered

1. **Manual post-deploy checklist** — Rejected; humans forget, especially under deploy pressure.
2. **Auth0 Deploy CLI only** — Partial solution; doesn't cover Caddy or detect runtime drift.
3. **Full IaC (Terraform for Auth0)** — Good long-term goal but over-engineered for current scale. Drift detection script is the pragmatic first step.
