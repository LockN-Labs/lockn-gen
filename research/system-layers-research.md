# System Layers Research: LockN Labs
**Date:** 2026-02-11 | **Author:** OpenClaw Research Agent

---

## 1. Executive Summary

### Layer 1 — Workflow Orchestration: **Temporal** (Winner) / **Inngest** (Runner-up)
**Temporal** is the clear winner for LockN's agentic workloads. MIT-licensed (fully productizable), battle-tested durable execution, multi-language SDKs (Go, Python, TypeScript, Java, .NET), and purpose-built for exactly what OpenClaw needs: long-running, fault-tolerant, async workflows that agents can drive programmatically. ~12k GitHub stars, backed by $1.4B+ valuation company.

**Inngest** is the pragmatic runner-up — event-driven, serverless-friendly, TypeScript-first, easier to adopt quickly. SSPL license limits productizability but it's excellent for internal orchestration.

### Layer 2 — Architecture Diagramming: **D2** (Winner) / **Mermaid** (Runner-up)
**D2** wins on visual quality, agent-friendliness, and embeddability. MPL-2.0 licensed, text-based, beautiful output, Go library for programmatic generation. 23k GitHub stars.

**Mermaid** is the pragmatic default — already rendered natively in GitHub, Notion, and most docs platforms. 76k+ stars, massive ecosystem. Use it everywhere D2 isn't needed.

---

## 2. Comparison Matrix

### Layer 1: Workflow Orchestration

| Criteria | n8n | Temporal | Windmill | Prefect | Airflow | Inngest |
|---|---|---|---|---|---|---|
| **License** | Sustainable Use (fair-code) | MIT ✅ | AGPL-3.0 | Apache 2.0 ✅ | Apache 2.0 ✅ | SSPL + DOSP Apache 2.0 |
| **Productizable?** | ⚠️ No resale/embed | ✅ Full freedom | ⚠️ AGPL copyleft; dual license available | ✅ Full freedom | ✅ Full freedom | ❌ SSPL restricts SaaS |
| **GitHub Stars** | ~100k | ~12k | ~12k | ~18k | ~38k | ~7k |
| **Slack Integration** | ✅ Native node | Via SDK/webhook | Via scripts | Via notifications | Via operators | Via events/webhook |
| **Linear Integration** | ✅ Community node | Via SDK | Via API scripts | Via API | Via API | Via webhook |
| **GitHub Integration** | ✅ Native node | Via SDK | Via scripts | Via API | Via operators | Via webhook |
| **Docker** | ✅ Official image | ✅ Official image | ✅ Official image | ✅ Docker support | ✅ Official image | ✅ Single binary/Docker |
| **Self-hosted** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (since v1.0) |
| **Cloud offering** | n8n Cloud | Temporal Cloud | Windmill Cloud | Prefect Cloud | MWAA, Astronomer | Inngest Cloud |
| **API-first/Headless** | ✅ REST API | ✅ gRPC + REST | ✅ Full REST API | ✅ REST API | ✅ REST API | ✅ REST + event API |
| **Agent-drivable** | ⚠️ Visual-first | ✅ Code-first, ideal | ✅ Script-native | ✅ Python decorators | ⚠️ DAG-heavy | ✅ Event-driven |
| **Learning Curve** | Low (visual) | High (concepts) | Medium | Medium | High (ops overhead) | Low-Medium |
| **Agentic Workloads** | ❌ Not designed for | ✅ Purpose-built | ⚠️ Good, not ideal | ⚠️ Python-only | ❌ Batch-oriented | ✅ Good (step functions) |
| **Long-running Tasks** | ⚠️ Limited | ✅ Months/years | ✅ Good | ⚠️ Limited | ❌ Task timeout issues | ✅ Good |
| **Multi-language** | JS (nodes) | Go, Python, TS, Java, .NET | Python, TS, Go, Bash, SQL | Python only | Python only | TS, Python, Go |

### Layer 2: Architecture Diagramming

| Criteria | Mermaid | Structurizr | D2 | Eraser.io | IcePanel | Diagrams (Python) | PlantUML | Excalidraw | tldraw |
|---|---|---|---|---|---|---|---|---|---|
| **License** | MIT | Freemium/Paid | MPL-2.0 | Proprietary SaaS | Proprietary SaaS | MIT | GPL/MIT dual | MIT | tldraw License (custom) |
| **Productizable?** | ✅ Fully | ⚠️ Limited | ✅ Embeddable Go lib | ❌ SaaS only | ❌ SaaS only | ✅ Fully | ✅ With care (GPL) | ✅ React component | ⚠️ Custom license |
| **GitHub Stars** | ~76k | ~4k | ~23k | N/A | N/A | ~40k | ~11k | ~95k | ~42k |
| **Text-based/Diffable** | ✅ | ✅ DSL | ✅ | ❌ | ❌ | ✅ Python | ✅ | ❌ (JSON) | ❌ (JSON) |
| **C4 Model Support** | ⚠️ Basic | ✅ Native, best-in-class | ⚠️ Manual | ⚠️ Templates | ✅ Native | ❌ Infra diagrams | ✅ Via C4-PlantUML | ❌ | ❌ |
| **GitHub Rendering** | ✅ Native | ❌ | ❌ (needs CI) | ❌ | ❌ | ❌ (needs CI) | ❌ (needs CI) | ❌ | ❌ |
| **Notion Integration** | ✅ Embed blocks | ❌ | ❌ | ✅ Native | ❌ | ❌ | ❌ | ✅ Embed | ✅ Embed |
| **Docusaurus** | ✅ Plugin | ⚠️ Export | ⚠️ Export | ❌ | ❌ | ⚠️ Export | ✅ Plugin | ✅ React | ✅ React |
| **Agent-generatable** | ✅ Easy text | ✅ DSL text | ✅ Easy text | ❌ GUI | ❌ GUI | ✅ Python code | ✅ Text | ⚠️ Complex JSON | ⚠️ Complex JSON |
| **Visual Quality** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ (hand-drawn) | ⭐⭐⭐ (hand-drawn) |
| **Collaboration** | Via Git | Cloud workspace | Via Git | ✅ Real-time | ✅ Real-time | Via Git | Via Git | ✅ Real-time | ✅ Real-time |

---

## 3. Productizability Analysis

### Can Become Part of a LockN Product

| Tool | Verdict | Why |
|---|---|---|
| **Temporal** | ✅ **YES — Core infrastructure** | MIT license. Embed as OpenClaw's execution engine. Agents run workflows, customers get durable execution for free. This is the backbone. |
| **Prefect** | ✅ YES — Alternative | Apache 2.0. Could embed for Python-heavy customer workflows. Less versatile than Temporal. |
| **Airflow** | ⚠️ Possible but heavy | Apache 2.0 but massive operational overhead. Better as customer's own infra, not embedded. |
| **D2** | ✅ **YES — Embeddable** | MPL-2.0. Go library generates SVG/PNG programmatically. OpenClaw agents generate architecture diagrams for customers. Ship in docs, proposals, audits. |
| **Mermaid** | ✅ YES — Lightweight | MIT. JS library renders anywhere. Lower quality than D2 but zero-friction in markdown. |
| **Excalidraw** | ✅ YES — Whiteboard feature | MIT. React component embeds into any web UI. Potential customer-facing collaborative canvas. |
| **Diagrams (Python)** | ✅ YES — Infra diagrams | MIT. Agents generate cloud architecture diagrams programmatically. |

### Internal Tooling Only

| Tool | Why Internal Only |
|---|---|
| **n8n** | Sustainable Use License prohibits embedding/resale. Great for internal automation (connecting Slack→Linear→GitHub) but can't ship to customers. |
| **Windmill** | AGPL means any modifications must be open-sourced. Dual license available but adds cost/complexity. Good for internal scripts-as-workflows. |
| **Inngest** | SSPL prevents offering as a service. Excellent for internal event-driven orchestration. |
| **IcePanel / Eraser.io** | Proprietary SaaS. No API for embedding. Internal architecture documentation only. |
| **Structurizr** | Paid cloud/on-prem. DSL is open but tooling is proprietary. C4 modeling for internal use. |

---

## 4. Integration Map

### How Each Connects to Our Stack

```
┌─────────────────────────────────────────────────────┐
│                    OpenClaw Agent                     │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Temporal  │  │ Inngest  │  │ n8n (internal)   │   │
│  │ (core)   │  │ (events) │  │                   │   │
│  └────┬─────┘  └────┬─────┘  └────────┬──────────┘  │
│       │              │                  │             │
└───────┼──────────────┼──────────────────┼─────────────┘
        │              │                  │
   ┌────▼────┐   ┌────▼────┐   ┌────────▼──────────┐
   │ Slack   │   │ GitHub  │   │ Linear            │
   │ (bot)   │   │ (webhk) │   │ (issues/projects) │
   └─────────┘   └─────────┘   └───────────────────┘
        │              │                  │
   ┌────▼────┐   ┌────▼────┐   ┌────────▼──────────┐
   │ Docker  │   │ Caddy   │   │ Auth0             │
   │ (deploy)│   │ (proxy) │   │ (auth)            │
   └─────────┘   └─────────┘   └───────────────────┘
```

#### Temporal + OpenClaw
- **Slack:** Temporal workflows trigger Slack notifications on completion/failure. Slack commands start workflows.
- **Linear:** Workflows create/update Linear issues. Issue state changes trigger workflows.
- **GitHub:** PR creation, code review, deployment workflows. Git operations as activities.
- **Docker:** Temporal workers run in Docker containers. Workflows orchestrate container lifecycle.
- **Auth0:** Workflow authorization via Auth0 tokens. Multi-tenant workflow isolation.

#### D2 + Mermaid + OpenClaw
- **GitHub:** Mermaid renders natively in READMEs. D2 generates SVGs via CI. Both committed as code.
- **Linear:** Agents attach generated architecture diagrams to issues/documents.
- **Notion:** Mermaid blocks embed directly. D2 exports as images.
- **Docusaurus:** Both integrate via plugins or image export.

---

## 5. Recommendation

### Option A: **Temporal + D2** (Recommended ✅)

**Workflow:** Temporal as the durable execution engine for all agentic workloads.
**Diagramming:** D2 as the primary diagram-as-code tool, Mermaid for lightweight inline diagrams.

**Pros:**
- MIT + MPL-2.0 = fully productizable stack
- Temporal is purpose-built for exactly what OpenClaw agents need (long-running, fault-tolerant, multi-language)
- D2 produces the highest quality output and is trivially agent-generated
- Both are API-first and headless
- Temporal has the strongest enterprise adoption trajectory

**Cons:**
- Temporal has a steep learning curve (concepts like workflows, activities, signals, queries)
- D2 doesn't render natively in GitHub (need CI pipeline or export)
- Temporal self-hosting requires PostgreSQL/MySQL + Elasticsearch

**Cost:** Free (self-hosted) / Temporal Cloud for production (~$200/mo starting)

### Option B: **Inngest + Mermaid** (Fast Start)

**Workflow:** Inngest for event-driven orchestration with minimal setup.
**Diagramming:** Mermaid everywhere (GitHub-native, zero friction).

**Pros:**
- Fastest time to value — single binary, TypeScript-first
- Mermaid is already everywhere, zero adoption friction
- Event-driven model fits webhook-heavy architecture
- Lower learning curve

**Cons:**
- SSPL license blocks productization of orchestration layer
- Mermaid visual quality is mediocre for customer-facing docs
- Less mature than Temporal for complex agentic patterns

**Cost:** Free (self-hosted) / Inngest Cloud free tier generous

### Option C: **Windmill + Structurizr** (Developer Platform)

**Workflow:** Windmill as scripts-as-workflows platform.
**Diagramming:** Structurizr for rigorous C4 architecture modeling.

**Pros:**
- Windmill is blazing fast (13x Airflow), great DX
- Structurizr is the gold standard for C4 modeling
- Windmill's UI builder adds internal tool capability
- Dual license available for commercial use

**Cons:**
- AGPL complicates productization without dual license
- Structurizr is proprietary/paid for serious use
- Neither has the community momentum of Options A or B

**Cost:** Windmill dual license (negotiable) / Structurizr Cloud ($100/mo)

### 🏆 Clear Winner: **Option A (Temporal + D2)**

Temporal's MIT license, durable execution model, and multi-language SDKs make it the only choice that can become core product infrastructure. D2's visual quality and Go library make it the best choice for agent-generated diagrams that customers actually want to look at.

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Deploy Temporal server (Docker Compose) on existing infrastructure
- [ ] Create first Temporal worker in TypeScript (OpenClaw's primary language)
- [ ] Implement basic workflow: Slack command → Linear issue creation → GitHub branch
- [ ] Set up D2 CLI in development environment
- [ ] Create initial system architecture diagram in D2
- [ ] Add Mermaid diagrams to existing GitHub READMEs

### Phase 2: Agent Integration (Weeks 3-4)
- [ ] Build OpenClaw ↔ Temporal SDK integration layer
- [ ] Implement agent-triggered workflows (deploy, review, notify)
- [ ] Create D2 diagram generation templates for common patterns
- [ ] Set up CI pipeline to render D2 → SVG on commit
- [ ] Build "generate architecture diagram" agent capability
- [ ] Temporal workflow for Linear issue lifecycle management

### Phase 3: Productization (Weeks 5-8)
- [ ] Abstract Temporal workflows into reusable customer-facing templates
- [ ] Build multi-tenant workflow isolation (Auth0 + Temporal namespaces)
- [ ] Package D2 diagram generation as a customer deliverable feature
- [ ] Create customer onboarding workflow (Temporal)
- [ ] Architecture audit workflow: agent inspects infra → generates D2 diagram → creates Linear issue
- [ ] Documentation: internal architecture fully diagrammed in D2

### Phase 4: Scale (Months 3-6)
- [ ] Migrate from Docker Compose to Temporal Cloud or K8s deployment
- [ ] Build workflow marketplace (reusable Temporal workflow templates)
- [ ] D2 diagram library for common cloud architectures
- [ ] Customer-facing workflow dashboard (Temporal UI embed)
- [ ] Advanced patterns: saga orchestration, human-in-the-loop workflows
- [ ] Evaluate adding n8n for non-technical user automation (internal only)

### Quick Wins (Do This Week)
1. `docker run temporalio/auto-setup:latest` — get Temporal running locally
2. `brew install d2` — start generating diagrams immediately
3. Add Mermaid diagrams to the OpenClaw architecture docs in GitHub
4. Create a Temporal "hello world" workflow that posts to Slack

---

## Appendix: License Quick Reference

| Tool | License | Embed in Product? | Offer as SaaS? | Modify & Keep Private? |
|---|---|---|---|---|
| Temporal | MIT | ✅ | ✅ | ✅ |
| Prefect | Apache 2.0 | ✅ | ✅ | ✅ |
| Airflow | Apache 2.0 | ✅ | ✅ | ✅ |
| n8n | Sustainable Use | ❌ | ❌ | ⚠️ Internal only |
| Windmill | AGPL-3.0 | ❌ (without dual license) | ❌ | ❌ Must open-source |
| Inngest | SSPL | ❌ | ❌ | ⚠️ Internal only |
| D2 | MPL-2.0 | ✅ | ✅ | ✅ (modified files must be MPL) |
| Mermaid | MIT | ✅ | ✅ | ✅ |
| Excalidraw | MIT | ✅ | ✅ | ✅ |
| tldraw | Custom (tldraw license) | ⚠️ Paid for commercial | ⚠️ | ⚠️ |
| PlantUML | GPL + MIT dual | ⚠️ GPL complications | ⚠️ | ❌ GPL |
| Diagrams (Python) | MIT | ✅ | ✅ | ✅ |
| Structurizr | Proprietary | ❌ | ❌ | ❌ |
| IcePanel | Proprietary | ❌ | ❌ | ❌ |
| Eraser.io | Proprietary | ❌ | ❌ | ❌ |
