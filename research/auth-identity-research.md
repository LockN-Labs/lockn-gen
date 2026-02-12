# Auth & Identity Layer for an Agentic Operating System

**Audience:** LockN Labs (OpenClaw-based productized agentic OS)
**Goal:** Replace Auth0 with a self-hostable, embeddable, multi-tenant auth and authorization layer suitable for agentic workloads.
**Date:** 2026-02-11 (EST)

---

## Executive Summary

For a **productizable, self-hosted, multi-tenant agentic platform**, the strongest options are:

1. **ZITADEL** (best overall fit)
2. **Keycloak** (most mature OSS baseline; heavier ops)
3. **Ory stack** (most flexible for custom architecture; highest implementation overhead)

If LockN wants **fastest path to Auth0-like features with strong multi-tenancy and migration tooling**, choose **ZITADEL**.
If LockN wants **maximum ecosystem maturity and pure OSS control**, choose **Keycloak**.
If LockN wants **modular policy + zero-trust API auth with deep custom engineering**, choose **Ory (Kratos/Hydra/Keto/Oathkeeper)**.

---

## 1) Open-Source Identity Platforms (Deep Dive)

## 1.1 Side-by-side comparison

| Platform | License | Productizability / Resell / Embed | Multi-tenancy | Protocols (OIDC/OAuth2/SAML) | Social Login | MFA | API-first | Self-host complexity | Scalability | Community / Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| **Keycloak** | Apache 2.0 | Very strong (embed, white-label, resell OK) | Historically realm-based; new Organizations improves CIAM patterns | Strong OIDC/OAuth2/SAML | Yes | Yes (TOTP, WebAuthn, etc) | Good admin REST + SPIs | Medium-High (Java stack, tuning needed) | High (battle-tested at large scale) | Very strong (Red Hat backed) |
| **Ory (Kratos/Hydra/Keto/Oathkeeper)** | Apache 2.0 OSS core + OEL for enterprise features | Strong, but some high-value features commercial in OEL | OSS supports tenant patterns, but some org/multi-tenant features are enterprise | Hydra strong OIDC/OAuth2; SAML via other components/integration patterns | Kratos supports social | Yes | Very API/headless-first | High (multiple services, orchestration required) | Very high (cloud-native, componentized) | Strong engineering community |
| **SuperTokens** | Apache 2.0 core (with feature gating in commercial plans) | Strong for embedding auth into app UX | Good tenant model in modern versions | OIDC/OAuth2 strong; enterprise SSO/SAML support in higher tiers | Yes | Yes | Very developer-centric | Low-Medium | High for app-auth scope | Growing, dev-friendly |
| **Authentik** | Source-available + enterprise terms (not pure permissive OSS posture) | Good technically, but **license/commercial terms need legal review** for resale/embedding | Supports tenant-like partitioning and brand/domain segregation | OIDC/OAuth2/SAML/LDAP/proxy patterns | Yes | Yes | Good APIs | Medium | Medium-High | Strong self-host community |
| **Logto** | MPL-2.0 | Good; MPL is file-level copyleft (usually productizable, but keep modifications to MPL files compliant) | Strong org-centric multi-tenant model | OIDC/OAuth2 native; SAML/enterprise SSO features available | Yes | Yes | API-first and SDK-first | Low-Medium | Medium-High | Rapidly growing |
| **Casdoor** | Apache 2.0 | Strong legally, broad protocol support | Has org/app abstractions but less enterprise-proven multi-tenant governance than top 3 | Very broad: OAuth2/OIDC/SAML/CAS/LDAP/SCIM etc. | Yes (many providers) | Yes | Good APIs | Medium | Medium | Active but smaller than Keycloak/ZITADEL |
| **ZITADEL** | Apache 2.0 | Excellent (embed/white-label/resell friendly) | First-class multi-tenancy (org/project model) | OIDC/OAuth2/SAML + federation | Yes | Yes incl passkeys | Strong API-first | Medium (simpler than Keycloak in many setups) | High (event-sourced architecture) | Strong and accelerating |
| **FusionAuth** | Community edition free but **not OSI OSS**; paid tiers | Productizable but licensing/commercial lock risk | Strong tenant model | OIDC/OAuth2/SAML (by plan) | Yes | Yes | Strong APIs | Low-Medium | High | Mature commercial vendor |

---

## 1.2 Platform-specific notes

### Keycloak
- **Strengths:** Most established OSS IAM option; deep protocol support; broad adapter ecosystem; robust theming/customization; strong federation.
- **Weaknesses:** Ops-heavy at scale (DB/session/cache tuning, upgrades); multi-tenancy historically awkward (realm-per-tenant tradeoffs), though Organizations feature is improving this.
- **Best when:** You want maximum OSS control and are willing to run a serious IAM platform.

### Ory stack
- **Strengths:** Highly modular, cloud-native, API-first; excellent for custom architecture; Oathkeeper+Keto are strong for API and policy layering.
- **Weaknesses:** More moving parts; architecture burden on your team; some production-grade features (org/multi-tenant extras, etc.) are tied to enterprise license.
- **Best when:** You want composable identity + authz primitives and can invest in platform engineering.

### SuperTokens
- **Strengths:** Developer experience, embeddable auth flows, easy React integration, gradual adoption.
- **Weaknesses:** Not as broad as Keycloak/ZITADEL for enterprise IAM/federation edge cases.
- **Best when:** Product UX and fast integration matter more than full IAM breadth.

### Authentik
- **Strengths:** Strong self-host feature set, flexible providers, modern admin UX, branding/domain controls.
- **Weaknesses:** Licensing posture requires legal diligence for resale/embedded product scenarios; less ideal if you require frictionless permissive licensing.
- **Best when:** You value features and can accept/contract around source-available + enterprise terms.

### Logto
- **Strengths:** Clean developer experience, good org/multi-tenant support, modern SDKs.
- **Weaknesses:** MPL-2.0 is usually acceptable, but legal/compliance should review obligations around modified MPL-covered files.
- **Best when:** You want a modern Auth0-like DX with open-source core and can handle MPL obligations.

### Casdoor
- **Strengths:** Broad protocol matrix; permissive Apache 2.0; UI-first with many integrations.
- **Weaknesses:** Relative ecosystem depth/governance less proven than Keycloak/ZITADEL for very large B2B SaaS auth estates.
- **Best when:** You need broad protocol connectivity fast and permissive licensing.

### ZITADEL
- **Strengths:** Excellent for B2B multi-tenant SaaS, modern architecture, strong API-first model, passkeys/MFA, strong auditability, clear Auth0 migration guidance.
- **Weaknesses:** Smaller ecosystem than Keycloak, but rapidly improving.
- **Best when:** You want a modern self-hosted IAM that balances product velocity and enterprise capabilities.

### FusionAuth
- **Strengths:** Practical migration docs/tools from Auth0, strong tenant model, polished self-host story, good SDKs.
- **Weaknesses:** Not open source in OSI sense for core commercial posture; feature access/paywall boundaries may affect product economics.
- **Best when:** You’re okay with vendor licensing and prioritize migration speed + operational simplicity.

---

## 2) Multi-Tenant Agentic Auth Patterns

## 2.1 How agents should authenticate

Use **four identity types**:

1. **Human users** (interactive): OIDC auth code + PKCE, session/token lifecycle.
2. **Service agents** (non-human first-party agents): client credentials with short-lived JWT access tokens.
3. **Delegated agents** (“act on behalf of user”): token exchange / delegated token with explicit actor claim.
4. **External machine integrations**: API keys only as bootstrap -> exchanged for short-lived JWT; prefer mTLS where possible.

Recommended baseline:
- Access tokens: 5–15 min TTL
- Refresh tokens: rotation + replay detection
- Workload identity: mTLS between internal services + JWT at app layer

## 2.2 Agent-to-agent auth (multi-tenant)

Pattern:
- Every agent gets a **workload principal** (agent_id, tenant_id, environment)
- Agent calls gateway with mTLS + JWT
- JWT includes:
  - `sub` = agent principal
  - `tid` = tenant
  - `scp` or `permissions` = least-privilege actions
  - `act` = actor chain when delegated
  - `jti` = unique token id for replay/audit correlation

Use policy decision point (PDP) for cross-agent operations:
- Permit only if `tenant(source)==tenant(target)` unless explicit cross-tenant trust policy exists.
- Require signed workflow context IDs for async calls.

## 2.3 Per-tenant permissions and scoping

Model:
- **RBAC + ABAC hybrid**
- RBAC for coarse roles (tenant_admin, analyst_agent, comms_agent)
- ABAC for runtime attributes (workflow_type, data_classification, channel, time window)

Permissions should be namespaced:
- `tenant:{tid}:agent:run`
- `tenant:{tid}:secrets:read`
- `tenant:{tid}:comms:matrix:send`

## 2.4 Audit trails for agent actions

Audit must capture:
- `who`: human/agent IDs
- `on_behalf_of`: optional user ID
- `what`: action + resource + decision
- `why`: policy/rule id matched
- `where`: source service, IP, node
- `when`: immutable timestamp
- `correlation`: workflow/run id (Temporal workflowId/runId)

Store append-only and stream to SIEM.

## 2.5 Delegation / impersonation (“agent acts for user”)

Use explicit delegation tokens (never silent impersonation):
- Token exchange creates **derived token** with:
  - `sub=agent`
  - `act.sub=user`
  - `delegation_id`
  - constrained scopes
  - short TTL
- Policy requires:
  - user consent or pre-approved policy
  - step-up auth for sensitive scopes
  - hard denials for privileged admin actions unless explicitly delegated

---

## 3) Productizability Analysis

## 3.1 Embed/white-label/resell without attribution constraints

- **Best (permissive):** Keycloak, ZITADEL, Casdoor, Ory OSS core (Apache 2.0)
- **Usually workable with obligations:** Logto (MPL-2.0)
- **Needs legal scrutiny for commercial embedding:** Authentik (source-available + enterprise terms), FusionAuth (commercial license model)

## 3.2 Custom login pages / custom domains / branding removal

- **Strong:** Keycloak, ZITADEL, FusionAuth, Authentik, Logto
- **Ory:** bring-your-own UI is a strength (headless), but you build/maintain UX
- **SuperTokens:** very strong embeddable UI customization via SDK/prebuilt overrides

## 3.3 React SDKs / embeddable components

- **Excellent:** SuperTokens, Logto, FusionAuth, ZITADEL (React SDK/examples)
- **Good:** Keycloak (OIDC libs + adapters rather than polished “single React SDK” approach)
- **Ory:** reference React UIs + API-driven approach (powerful but more work)
- **Authentik/Casdoor:** workable via OIDC/OAuth2 and custom flows

## 3.4 Pricing model implications

- **Apache OSS options:** infra + ops cost dominant; no per-MAU vendor lock by default.
- **MPL option:** similar infra economics with license-compliance overhead.
- **Commercial/community split (FusionAuth/Auth0-like models):** possible predictable support, but feature gating and scale pricing risk.
- **For agentic OS:** avoid per-user-only pricing assumptions; model includes **human users + machine principals + tenant count + workflow volume**.

---

## 4) Migration Path from Auth0

## 4.1 Platform migration readiness

- **ZITADEL:** Explicit Auth0 migration guidance and tooling, including password-hash handling path.
- **Ory:** Auth0 migration guides available.
- **FusionAuth:** Strong Auth0 migration docs/scripts and import guidance.
- **Keycloak:** No official first-party “Auth0 one-click” path; migration typically custom export/transform/import.
- **Logto:** General user migration docs (manual/API-driven), but less turnkey Auth0-specific than ZITADEL/FusionAuth.
- **SuperTokens/Casdoor/Authentik:** Migration feasible through API/import pipelines; usually custom mapping.

## 4.2 User migration strategies

### A) Bulk migration (preferred when possible)
1. Export users + metadata from Auth0.
2. Export password hashes (requires Auth0 support process for some hash data).
3. Transform schemas to target format.
4. Import in batches with verification and rollback checkpoints.

### B) Lazy migration (when hash export is blocked)
1. Keep Auth0 as temporary upstream IdP.
2. On first login, authenticate against old source and re-home user in new IdP.
3. Force reset only for users not migrated after cutoff window.

### C) Hybrid
- Bulk import active users, lazy-migrate long-tail accounts.

## 4.3 Feature parity gaps vs Auth0 to assess early

- Actions/Rules equivalents (hooks, post-login pipelines)
- B2B org model semantics
- Attack protection / bot detection / anomaly detection
- Marketplace integrations
- Fine-grained tenant admin UX

---

## 5) Integration with LockN Stack

## 5.1 Caddy reverse proxy

Pattern:
- Caddy terminates TLS and forwards to IdP + app services.
- Use OIDC auth at edge for user-facing routes.
- For APIs, validate JWT at gateway layer and forward verified claims headers.
- For internal service mesh, add mTLS between gateway and services.

## 5.2 Docker deployment

All candidates support Docker; production baseline:
- Dedicated Postgres (or supported DB)
- Redis/cache where needed
- Secrets via Vault/SOPS/KMS (not env vars in plaintext)
- Blue/green upgrades for IdP

## 5.3 Temporal workflows

- Temporal workers authenticate as workload principals (client credentials/mTLS).
- Every workflow run carries identity context (`tenant_id`, `subject`, `delegation`).
- Enforce permission check in activity boundaries, not only at workflow ingress.
- Attach workflow ids to audit events.

## 5.4 Matrix / Mattermost comms integrations

- Treat each connector as an agent principal with per-tenant scoped permissions.
- Use outbound token minting for connectors; rotate aggressively.
- For “post message on behalf of user,” require delegation token + policy check.

## 5.5 RBAC/ABAC for agent permissions

- If choosing **Ory**, Keto can be PDP for relationship-based ABAC/ReBAC.
- If choosing **Keycloak/ZITADEL/Logto/FusionAuth**, pair with OpenFGA/OPA/Cedar for fine-grained authz where built-in roles are insufficient.

## 5.6 API gateway auth patterns

Recommended:
- External APIs: OAuth2/OIDC bearer JWT, introspection fallback
- Internal APIs: SPIFFE/SPIRE-style mTLS + JWT claims propagation
- Agent APIs: signed workload JWT + tenant claim mandatory
- Sensitive operations: step-up token with `acr` or dedicated high-assurance scope

---

## 6) Recommendation

## 6.1 Best option for productizable agentic OS

### Primary recommendation: **ZITADEL**

Why:
- Apache 2.0 (clean productization posture)
- Strong multi-tenant model aligned to B2B SaaS and tenant isolation
- Good modern API-first architecture
- Built-in story for auth hardening (MFA/passkeys, auditability)
- Better migration path from Auth0 than most OSS options
- Lower operational burden than heavily customized Keycloak setups in many teams

### Secondary recommendation: **Keycloak**
Use when:
- You prioritize ecosystem maturity and broad enterprise compatibility
- You can staff IAM platform operations properly

### Tertiary recommendation: **Ory stack**
Use when:
- You want deeply composable identity + policy + gateway architecture
- You accept higher engineering complexity and possible enterprise licensing for some advanced capabilities

---

## 6.2 Implementation complexity and timeline estimate

### Option A: ZITADEL (recommended)
- **Phase 0 (1–2 weeks):** architecture, tenant model, token schema, migration plan
- **Phase 1 (2–4 weeks):** core auth flows (OIDC, social, MFA), Caddy integration, Docker prod baseline
- **Phase 2 (2–4 weeks):** agent identities, delegation, audit trail, Temporal integration
- **Phase 3 (2–3 weeks):** Auth0 migration rehearsal + staged cutover
- **Total:** ~7–13 weeks to production-grade initial rollout

### Option B: Keycloak
- **Total:** ~10–16 weeks (more ops/theming/customization burden likely)

### Option C: Ory stack
- **Total:** ~12–20 weeks (modular power, but more integration work)

---

## Suggested target architecture (LockN)

- **IdP:** ZITADEL
- **Authz PDP:** OPA/Cedar or OpenFGA (for fine-grained agent permissions)
- **Gateway:** Caddy + JWT verification layer
- **Workload identity:** mTLS (SPIFFE-like) + short-lived JWT
- **Audit pipeline:** append-only audit log + SIEM export
- **Delegation model:** OAuth token exchange with actor claim chain

---

## Risks and mitigation

1. **Tenant isolation mistakes**
   - Mitigation: enforce `tenant_id` in every token and every DB query policy.
2. **Delegation abuse**
   - Mitigation: short-lived delegation tokens, explicit consent, high-risk step-up.
3. **Migration password hash limitations**
   - Mitigation: hybrid bulk + lazy migration fallback.
4. **Authorization sprawl**
   - Mitigation: centralized policy engine + policy-as-code review process.

---

## Practical decision rubric (quick)

Choose **ZITADEL** if you want: modern OSS, multi-tenant SaaS focus, Auth0 migration path, strong productizability.
Choose **Keycloak** if you want: maximum ecosystem maturity and can absorb ops complexity.
Choose **Ory** if you want: composable platform primitives and can invest in deeper engineering.

---

## Reference links used for validation (non-exhaustive)

- Keycloak docs and organizations announcement
- Ory docs (enterprise license + migration)
- SuperTokens docs (multi-tenancy, frontend SDK)
- Authentik docs (providers, branding) and licensing discussions/pages
- Logto docs (customization, React, migration)
- Casdoor GitHub/docs (protocol support)
- ZITADEL docs (Auth0 migration, React, feature set)
- FusionAuth docs (pricing, migration, React SDK)

(Exact URL set available from research notes; all claims above should still be validated against current vendor docs during implementation planning.)
