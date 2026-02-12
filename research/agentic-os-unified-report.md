# Agentic OS — Unified Research Report

**Date:** 2026-02-11 | **Compiled by:** Claws (Opus)
**Context:** LockN Labs is evaluating a fully productizable OpenClaw-based agentic operating system with all modules owned.

---

## Executive Summary

| Layer | Winner | License | Runner-up |
|---|---|---|---|
| **Workflow Orchestration** | Temporal | MIT | Inngest (SSPL — internal only) |
| **Architecture Diagramming** | D2 + Mermaid | MPL-2.0 + MIT | Structurizr (proprietary) |
| **Communications** | Matrix protocol + custom client | Apache 2.0 | Rocket.Chat (MIT) |
| **Auth & Identity** | Zitadel | Apache 2.0 | Keycloak (Apache 2.0) |
| **Project Management** | Plane | AGPL-3.0 (commercial avail) | Huly (EPL-2.0) |
| **Knowledge Base** | AFFiNE | MIT | Outline (BSL → Apache) |
| **Observability** | OpenTelemetry + Grafana | Apache 2.0 + AGPL | — |
| **Inference Routing** | OpenClaw (already owned) | Proprietary | — |

**Full stack cost to self-host: $0/mo software licensing** (all OSS). Infra costs only.

---

## Layer 1: Workflow Orchestration → Temporal
*Full report: `system-layers-research.md`*

- **MIT license** — fully productizable
- Purpose-built for durable, long-running agentic workloads
- Multi-language SDKs (Go, Python, TS, Java, .NET)
- Code-first, API-first — agents drive it programmatically
- ~12k GitHub stars, $1.4B+ company behind it

## Layer 2: Architecture Diagramming → D2 + Mermaid
*Full report: `system-layers-research.md`*

- **D2** (MPL-2.0): highest visual quality, Go library for programmatic generation, 23k stars
- **Mermaid** (MIT): universal fallback, renders natively in GitHub/Notion, 76k stars
- Both text-based, diffable, agent-generatable

## Layer 3: Communications → Matrix Protocol
*Full report: `comms-layer-research.md`*

### Why Matrix
- **Apache 2.0 protocol** — you own the protocol, not just the software
- Rooms = agent contexts, bots are first-class citizens
- Best bridge ecosystem: mautrix covers Slack, Discord, Teams, WhatsApp, Telegram
- Federation built-in (can run closed or federated)
- Government adoption: France, Germany, NATO, Ukraine
- E2EE optional per-room, immutable event DAG = perfect audit trail
- Multiple server impls: Synapse (Python), Dendrite (Go), Conduit (Rust)

### Key Insight
**Nobody in the agentic space owns their comms layer.** Dust.tt, CrewAI, AutoGen — all parasitize Slack or have no real comms. This is greenfield and a potential product differentiator.

### Implementation Path
1. **Now:** Build `CommsProvider` abstraction + Slack provider (keep working)
2. **Month 1-4:** Stand up Matrix server + custom client on matrix-js-sdk + mautrix-slack bridge
3. **Month 4+:** Matrix as primary, bridges to Slack/Discord/Teams for interop

### Complementary: Chatwoot (MIT)
- Customer-facing chat widget (embeddable JS snippet)
- Complements Matrix for external-facing comms

## Layer 4: Auth & Identity → Zitadel
*Full report: `auth-identity-research.md`*

### Why Zitadel
- **Apache 2.0** — embed, white-label, resell freely
- First-class multi-tenancy (org/project model)
- Modern event-sourced architecture
- Strong API-first design with passkeys/MFA
- Clear Auth0 migration guidance
- OIDC/OAuth2/SAML + federation

### Agent Auth Patterns
- **Service accounts** with scoped API keys per agent
- **Delegation tokens** for "agent acts on behalf of user"
- **Per-tenant agent permissions** via Zitadel's org model
- **Audit trails** via event-sourced architecture (every action logged)

### Migration from Auth0
- Bulk user export via Auth0 Management API → Zitadel import
- Lazy migration for password hashes (re-auth on first login)
- ~2-4 week migration window for our current user base

### Alternatives
- **Keycloak** (Apache 2.0): Most mature, but heavier ops (Java stack)
- **Ory** (Apache 2.0): Most flexible/modular, but highest implementation complexity

## Layer 5: Project Management → Plane
*Research compiled from web sources*

### Why Plane
- **AGPL-3.0** with commercial license available for embedding
- Closest feature parity to Linear: cycles, views, modules, roadmaps
- Strong API (REST + webhooks)
- Self-hosted via Docker
- Active development, ~30k GitHub stars
- UI quality approaching Linear-level polish

### Key Considerations
- AGPL requires commercial license for embedded/SaaS use — Plane offers this
- Less keyboard-shortcut-driven than Linear (gap)
- No native Slack integration yet (webhook-based)

### Alternatives
- **Huly** (EPL-2.0): Strong all-in-one (PM + docs + HR), embeddable, but smaller community
- **Focalboard** (Mattermost): Effectively abandoned as standalone
- **Taiga** (MPL-2.0): Good agile features but dated UI

### Abstraction Layer Design
Build a `WorkItemProvider` interface:
```typescript
interface WorkItemProvider {
  createIssue(params: CreateIssueParams): Promise<Issue>
  updateIssue(id: string, params: UpdateParams): Promise<Issue>
  listIssues(filter: IssueFilter): Promise<Issue[]>
  subscribe(event: WorkItemEvent): Observable<Issue>
  // ... cycles, labels, assignments
}
```
Implementations: `LinearProvider`, `PlaneProvider`, `GitHubIssuesProvider`

## Layer 6: Knowledge Base → AFFiNE
*Research compiled from web sources*

### Why AFFiNE
- **MIT license** — fully productizable, no restrictions
- Local-first architecture (offline-capable, sync optional)
- Block editor + whiteboard (Notion-like + Miro-like in one)
- Real-time collaboration via CRDT (Yjs)
- Self-hosted via Docker
- ~45k GitHub stars, very active development
- Canvas/whiteboard mode is unique differentiator

### Key Considerations
- API still maturing (less robust than Notion's)
- Mobile apps in early stages
- Database/view features less mature than Notion
- But MIT license + local-first is unbeatable for productization

### Alternatives
- **Outline** (BSL 1.1 → Apache 2.0 after 3 years): Best docs-focused option, Slack-like slash commands, but BSL limits immediate productization
- **BookStack** (MIT): Simple, reliable, great for structured docs — less collaborative
- **Silverbullet** (MIT): Developer-focused, markdown-native, lightweight

### Abstraction Layer Design
Build a `KnowledgeProvider` interface:
```typescript
interface KnowledgeProvider {
  createDocument(params: CreateDocParams): Promise<Document>
  updateDocument(id: string, content: string): Promise<Document>
  search(query: string): Promise<Document[]>
  getBlocks(docId: string): Promise<Block[]>
  subscribe(event: KnowledgeEvent): Observable<Document>
}
```
Implementations: `NotionProvider`, `AFFiNeProvider`, `OutlineProvider`

## Layer 7: Observability → OpenTelemetry + Grafana
*Already partially in progress (LockN Control project)*

- **OpenTelemetry** (Apache 2.0): Industry standard for traces/metrics/logs
- **Grafana** (AGPL-3.0): Dashboards and alerting — AGPL is fine for internal use, Grafana Cloud for customer-facing
- **Prometheus** (Apache 2.0): Metrics collection
- **Loki** (AGPL-3.0): Log aggregation
- Already have Grafana 3300 + Prometheus 9090 running

## Layer 8: Inference Routing → OpenClaw (Already Owned)
- Model routing between local (llama.cpp) and cloud (Anthropic, OpenAI, Ollama)
- Cost optimization, fallback chains, context management
- This IS the product core — already proprietary

---

## Full Agentic OS Module Map

```
┌─────────────────────────────────────────────────────────────┐
│                    LockN Agentic OS                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  OpenClaw     │  │  Temporal     │  │  Matrix          │  │
│  │  (Runtime)    │  │  (Orchestr.)  │  │  (Comms)         │  │
│  │  Proprietary  │  │  MIT          │  │  Apache 2.0      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────┘  │
│         │                  │                  │              │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────────┐  │
│  │  Zitadel      │  │  Plane       │  │  AFFiNE          │  │
│  │  (Auth)       │  │  (PM)        │  │  (Knowledge)     │  │
│  │  Apache 2.0   │  │  AGPL+Comm.  │  │  MIT             │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────┘  │
│         │                  │                  │              │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────────┐  │
│  │  OTel+Grafana │  │  D2+Mermaid  │  │  Qdrant          │  │
│  │  (Observ.)    │  │  (Diagrams)  │  │  (Vector DB)     │  │
│  │  Apache+AGPL  │  │  MPL+MIT     │  │  Apache 2.0      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Infrastructure: Docker + Caddy + Cloudflare          │   │
│  │  All open/portable (Docker: Apache 2.0, Caddy: Apache)│   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Competitive Landscape

| Competitor | What They Do | Comms | Auth | PM | Knowledge | Inference | Self-Host |
|---|---|---|---|---|---|---|---|
| **Dust.tt** | Enterprise AI assistant | Slack parasitic | Auth0/own | None | Notion parasitic | Multi-model | ❌ Cloud only |
| **CrewAI** | Multi-agent framework | None | None | None | None | Multi-model | ✅ Framework |
| **AutoGen (MS)** | Agent conversations | None | None | None | None | Multi-model | ✅ Framework |
| **LangGraph** | Agent orchestration | None | None | None | None | Multi-model | ✅ Framework |
| **Composio** | Agent tool integration | None | None | None | None | Multi-model | Partial |
| **Relevance AI** | Agent builder | Slack/Teams | Own | None | None | Multi-model | ❌ Cloud only |
| **LockN (proposed)** | Full agentic OS | ✅ Owned (Matrix) | ✅ Owned (Zitadel) | ✅ Owned (Plane) | ✅ Owned (AFFiNE) | ✅ Owned (OpenClaw) | ✅ Full |

**Key insight:** Nobody owns the full stack. Every competitor either parasitizes SaaS tools or only provides a framework without operational infrastructure. A fully self-hostable agentic OS with owned comms, auth, PM, and knowledge is genuinely differentiated.

---

## Productization Strategy

### Pricing Model (Recommended: Hybrid)
- **Per-agent seat**: $29-99/mo per active agent (scales with usage)
- **Platform fee**: $199-499/mo base (includes infra modules)
- **Enterprise**: Custom pricing for self-hosted + support + SLA
- **Free tier**: 1 agent, community support, self-hosted only

### Open-Core Model
- **Open**: Runtime, basic tools, single-agent, community integrations
- **Commercial**: Multi-agent orchestration, Temporal workflows, enterprise auth, observability dashboards, priority support

### Go-to-Market
- **Entry point**: Single agent use case (customer support, internal ops)
- **Expand**: Multi-agent teams, cross-department workflows
- **Enterprise**: Self-hosted, compliance, custom integrations
- **Buyer**: VP Engineering / Head of AI / CTO

### "10x Better" Narrative
> "Stop renting your AI infrastructure from 8 different SaaS vendors. Own the full stack. One platform, one bill, zero vendor lock-in. Your agents run on your infrastructure, your data never leaves your network."

---

## Implementation Roadmap

### Phase 1: Abstraction Layers (Weeks 1-4)
- [ ] Build `CommsProvider` interface + Slack implementation (keep working today)
- [ ] Build `AuthProvider` interface + Auth0 implementation (keep working today)
- [ ] Build `WorkItemProvider` interface + Linear implementation (keep working today)
- [ ] Build `KnowledgeProvider` interface + Notion implementation (keep working today)
- [ ] Deploy Temporal (Docker Compose) for workflow orchestration
- [ ] Create v1 system architecture diagrams in D2

### Phase 2: OSS Module Integration (Months 2-3)
- [ ] Stand up Matrix (Dendrite) + custom client on matrix-js-sdk
- [ ] Deploy Zitadel, migrate from Auth0
- [ ] Deploy Plane, build PlaneProvider
- [ ] Deploy AFFiNE, build AFFiNeProvider
- [ ] Mautrix-Slack bridge for backwards compatibility

### Phase 3: Productization (Months 3-6)
- [ ] Multi-tenant isolation across all modules
- [ ] Unified admin dashboard
- [ ] Customer onboarding workflow (Temporal)
- [ ] Self-hosted installer / Docker Compose stack
- [ ] Documentation site with D2 architecture diagrams
- [ ] Pricing page + Stripe billing

### Phase 4: Enterprise (Months 6-12)
- [ ] SOC2 compliance path
- [ ] On-prem deployment automation
- [ ] SLA management
- [ ] Custom integration marketplace
- [ ] Federation support (Matrix-native)

---

## Risk Analysis

| Risk | Severity | Mitigation |
|---|---|---|
| Abstraction layer complexity | High | Start with 2 providers per interface, not 5. Ship thin. |
| Matrix adoption curve | Medium | Keep Slack bridge running indefinitely. Migration is optional for users. |
| Plane feature gap vs Linear | Medium | Use as internal dogfood first. Contribute upstream. |
| AFFiNE API immaturity | Medium | Start with basic CRUD. Contribute API PRs upstream. |
| Temporal learning curve | Medium | Start with 3 simple workflows. Team ramp over 2-4 weeks. |
| Market timing | Low | Agentic AI adoption accelerating. Better early than late. |
| Regulatory (AI governance) | Medium | Self-hosted = customer controls their data. Strong positioning. |

---

## Appendix: Individual Report Locations

| Report | Path | Author |
|---|---|---|
| Workflow + Diagrams | `research/system-layers-research.md` | Opus |
| Communications Layer | `research/comms-layer-research.md` | Opus |
| Auth & Identity | `research/auth-identity-research.md` | Codex |
| Unified Synthesis | `research/agentic-os-unified-report.md` | Claws (this file) |
