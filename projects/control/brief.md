# LockN Control — Project Brief

*Kickoff Date: 2026-02-11*
*Status: Planning*
*Owner: Sean (CEO)*

---

## Executive Summary

LockN Control is the observability and cost-control plane for the LockN AI ecosystem. It provides real-time dashboards for model usage (tokens in/out/total per model), infrastructure health, cost tracking, and subscription cap proximity alerts — built on Prometheus + Grafana. Internal tool first, then productized as a standalone offering for teams running hybrid local+cloud AI stacks.

**Positioning:** "Real-time visibility into your AI stack — usage, cost, and health in one dashboard."

## Business Case

### Revenue Model
- **Freemium conversion engine:** Basic dashboards (usage + uptime) free, advanced controls (cost caps, alerting, multi-node, audit exports) paid
- **Pricing tiers:** Free (1 node, 7-day retention) → Starter $19/mo → Pro $59/mo → Scale $149/mo
- **Projected MRR:** $540/month at 6 months (9 paying customers at ~$60 ARPU)
- **Break-even:** 4-6 months
- **Go/No-Go:** Conditional — must ship MVP in ≤4 weeks, validate with design partners, hit $250 MRR within 60 days of launch

### Cost to Implement
- Compute: $25-60/month (self-hosted Prometheus + Grafana + exporters)
- Services: $0-40/month
- Engineering time: 3-5 weeks for MVP, 7 weeks for full v1

### Financial Risks
- Founder time overrun delays core product
- Low willingness to pay if seen as commodity/OSS feature
- Storage costs can grow with retention-heavy tiers
- Must hit $250 MRR in 60 days or freeze expansion

## Technical Architecture

### Feasibility: HIGH (7-week estimate for full v1)

### Three Ingestion Lanes
1. **Native infra exporters:** node_exporter, cAdvisor, DCGM/nvidia-smi exporter, llama.cpp `/metrics`
2. **Custom LockN exporter:** Reads LockN Logger SQLite → emits low-cardinality Prometheus counters/histograms (tokens in/out/total, latency, errors, cost)
3. **Quota exporter:** Subscription cap proximity for Claude Max weekly limits, OpenAI Pro/Codex session limits (estimated, not official API)

### Tech Stack
- Prometheus (metrics backbone)
- Grafana (visualization + alerting UI)
- Alertmanager (alert routing — Slack, email, webhook)
- cAdvisor + node_exporter (container + host metrics)
- NVIDIA DCGM/nvidia-smi exporter (GPU telemetry)
- Custom SQLite exporter (LockN Logger bridge)
- Docker Compose (deployment)
- Caddy (auth + reverse proxy)
- Optional: Loki + Promtail (logs), OpenTelemetry Collector, VictoriaMetrics (long-term storage)

### Key Design Decisions
- Labels constrained to provider/model/environment — avoid per-request cardinality explosion
- Dashboard folders: Exec Summary, Model Usage, Infra Health, Cost & Quotas, Alert Triage
- Start with local retention (15-30 days), add remote_write later for productization
- Single-tenant first, multi-tenant architecture planned for product release

## Infrastructure Plan

### Requirements
- Prometheus + Grafana + Alertmanager containers with persistent volumes
- cAdvisor + node_exporter + GPU exporter containers
- Custom SQLite metrics exporter
- Blackbox exporter for endpoint health checks
- Dedicated observability Docker network + volumes
- Grafana behind Cloudflare Access/OIDC with MFA

### Security
- Prometheus restricted to internal Docker network only (never public)
- Grafana behind auth proxy, anonymous access disabled
- API keys/webhook URLs in env/secrets, not in repo
- SQLite exporter: read-only DB access
- TLS end-to-end via Cloudflare tunnel
- No PII/prompts in metric labels

### Estimated Infra Cost: $25-120/month
- Base: ~$25/month (self-hosted storage/backup)
- With managed long-term metrics + paging: up to $120/month

## Go-to-Market Plan

### Target Persona
DevOps/Platform Engineering leads at startups/SMBs running self-hosted or hybrid AI inference (Ollama, llama.cpp, vLLM) who need cost control and reliability.

### Competitive Landscape
| Competitor | Gap LockN Fills |
|---|---|
| Grafana Cloud | Not AI-native — no token economics, model cost, or cap proximity |
| Cloud provider dashboards | Single-provider only, no local inference visibility |
| Langfuse/Helicone/OpenLIT | App-level tracing, weak on infra/GPU/SRE workflows |
| DIY Prometheus | High setup burden — LockN provides opinionated quick-start |

### Launch Sequence
- **Weeks 1-4:** Metric schema + core exporters + dashboard MVP + internal deployment
- **Weeks 5-6:** Internal KPI validation and reliability hardening
- **Weeks 7-10:** Closed alpha with 5-10 design partners
- **Weeks 11-12:** Public waitlist launch + case study + docs

### Content Needs
- Product landing page
- Technical docs (installation, metrics schema, alert setup)
- Quickstart guide (<30 min setup)
- Dashboard library docs
- Alert playbooks
- Comparison page: LockN Control vs alternatives
- Blog post: "Why generic observability fails for local AI"

## Product Vision

LockN Control is the "nervous system" of the LockN suite — the module that connects all other products (Score, Speak, Gen, Loader, Brain) into a single observable, controllable platform. It's the first thing you see when you open LockN, and the thing that makes you trust the system enough to pay for it.

### User Stories
1. As a developer running local models, I want to see real-time token usage per model so I can understand my workload distribution
2. As a team lead, I want cost tracking across cloud + local inference so I can justify infrastructure decisions
3. As an ops engineer, I want subscription cap alerts so I never hit Claude/Codex limits mid-sprint
4. As a platform user, I want infrastructure health dashboards so I can diagnose issues before they impact my work

### MVP Scope (v1)
- Prometheus + Grafana + Alertmanager deployment
- Model usage dashboards (tokens in/out/total, per model, realtime line graphs)
- Infrastructure dashboards (containers, GPU, disk, memory)
- LockN Logger SQLite integration
- llama.cpp native metrics scraping
- Subscription cap proximity (estimated)
- Slack alert routing

### Deferred Scope (v2+)
- Multi-tenant architecture
- Ollama full metrics parity
- Long-term storage (VictoriaMetrics/Mimir)
- Log aggregation (Loki)
- Enterprise RBAC/SSO/audit
- Custom dashboard builder
- ROI calculator
- Design partner onboarding kit

### Success Metrics
| Metric | Target | Timeframe |
|---|---|---|
| Internal deployment | Fully operational | 4 weeks |
| Dashboard accuracy | >95% token count parity | 4 weeks |
| Design partners onboarded | 5-10 teams | 10 weeks |
| Public alpha launch | Waitlist live | 12 weeks |
| Paying customers | 5+ conversions | 60 days post-launch |
| MRR | $250+ | 60 days post-launch |

### RICE Score
- Revenue Impact: 7/10 (direct revenue + platform stickiness)
- Reach: 6/10 (every AI team needs observability)
- Confidence: 7/10 (proven tech stack, clear demand signals)
- Effort: 5/10 (3-5 weeks MVP, 7 weeks full)
- **Total: 11.2** (high priority)

## Risk Register

| Risk | Source | Severity | Mitigation |
|---|---|---|---|
| No official subscription cap APIs | Engineering | High | Track usage locally, set soft alerts at estimated thresholds |
| Token/cost normalization across providers | Engineering | Medium | Define canonical schema early, accept approximation |
| WSL2 GPU exporter brittleness | DevOps | Medium | Test across restarts, add fallback nvidia-smi polling |
| High-cardinality label explosion | Engineering | High | Strict label policy: provider/model/env only |
| Alert fatigue | DevOps | Medium | Severity tiers, inhibition rules, iterative tuning |
| Founder time overrun | Finance | High | 4-week MVP timebox, freeze expansion if no traction |
| Low WTP for observability | Finance | Medium | Freemium hook, validate with design partners first |

## Open Questions

1. Do Claude Max / OpenAI Pro expose remaining quota APIs? (Likely no — must infer)
2. What retention window for internal use? (Recommend 30 days)
3. Metrics-only MVP or include logs/traces? (Recommend metrics-only)
4. Single-tenant first or multi-tenant from day one? (Recommend single-tenant)
5. What notification channels for alerts? (Recommend Slack-first, email later)
6. Who owns LockN Logger SQLite schema versioning? (Need to formalize)

## Stakeholder Scorecard

| Stakeholder | Assessment |
|---|---|
| Engineering | Feasibility: **HIGH** · 7 weeks · 13 tickets suggested |
| DevOps | Infra cost: **$25-120/mo** · Security: flagged (auth required) · 10 tickets |
| Finance | Go/No-Go: **CONDITIONAL** · Break-even: 4-6 months · Projected $540 MRR at 6mo |
| Marketing | Persona: DevOps leads · Strong differentiation vs generic tools · 12 tickets |
| Product | MVP: 4 weeks · RICE: 11.2 · 5+ success metrics defined |
