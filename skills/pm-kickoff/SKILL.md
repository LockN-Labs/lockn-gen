---
name: pm-kickoff
description: Comprehensive project kickoff that ensures every new initiative gets stakeholder input from engineering, devops, finance, marketing, and product before implementation begins. Creates tickets, roadmap, documentation, and gets all agents aligned.
---

# PM Kickoff Skill

## Purpose
When a new product, feature set, or initiative is greenlit, this skill runs a structured kickoff that:
1. Gathers input from all relevant stakeholder perspectives
2. Produces thorough documentation
3. Creates a complete Linear ticket structure with roadmap
4. Sets up Notion documentation
5. Ensures nothing falls through the cracks before code starts

**This is NOT pm-bootstrap** (which discovers existing state). This is forward-looking: "We're building X — let's plan it right."

## When to Use
- New LockN product module (e.g., LockN Swap)
- Major feature initiative (e.g., "add Stripe billing across all products")
- New business line or revenue stream
- Any work spanning >5 tickets or >2 weeks

## Kickoff Phases

### Phase 0: Intake (Orchestrator — Opus/Claws)
Gather the minimum viable brief from the requester:

**Required inputs:**
- **What:** One-paragraph description of the initiative
- **Why:** Business justification (revenue, cost reduction, strategic)
- **Who:** Target users/customers
- **When:** Desired timeline or urgency

**If any are missing, ask before proceeding.** Don't guess on business intent.

### Phase 1: Stakeholder Review (Staggered Agents)
Spawn review agents in two waves to avoid GPU contention on local models.

**Wave 1 (spawn immediately):** Engineering + DevOps + Finance
**Wave 2 (spawn after Wave 1 completes, or after ~60s):** Marketing + Product

**Model assignments per role:**
| Role | Agent ID | Model | Rationale |
|------|----------|-------|-----------|
| Engineering | dev-cloud | `codex` | Code-aware reasoning |
| DevOps | devops-cloud | `deepseek` | Infrastructure analysis |
| Finance | reasoning-cloud | `deepseek` | Structured financial reasoning |
| Marketing | research-cloud | `sonnet` | Creative positioning |
| Product | reasoning-cloud | `sonnet` | Product strategy synthesis |

Always pass the `model` parameter explicitly in `sessions_spawn`. Never rely on subagent defaults — they cascade through fallbacks unpredictably when GPU is contended.

#### 1a. Engineering Review (model: codex)
```
You are the Engineering Lead for LockN Labs. Review this initiative:

[Initiative brief]
[Existing codebase context from projects/{slug}/brief.md if exists]

Evaluate and return JSON:
{
  "feasibility": "high|medium|low",
  "estimateWeeks": <number>,
  "techStack": ["recommended technologies"],
  "risks": ["technical risks"],
  "dependencies": ["other systems/services needed"],
  "architectureNotes": "key design considerations",
  "suggestedTickets": [{"title": "...", "estimate": "S|M|L|XL", "priority": 1-4}],
  "openQuestions": ["things needing clarification"]
}
```

#### 1b. DevOps Review (model: deepseek)
```
You are the DevOps Lead for LockN Labs. Review this initiative:

[Initiative brief]
[Current infra context: Docker, 3-stage pipeline Dev→Test→Prod, ports 3001-3299]

Evaluate and return JSON:
{
  "infraRequirements": ["what needs to be provisioned"],
  "cicdChanges": ["pipeline modifications needed"],
  "securityConsiderations": ["auth, secrets, network"],
  "monitoringNeeds": ["metrics, alerts, dashboards"],
  "estimatedInfraCost": "$X/month",
  "suggestedTickets": [{"title": "...", "estimate": "S|M|L|XL", "priority": 1-4}],
  "risks": ["operational risks"]
}
```

#### 1c. Finance Review (model: deepseek)
```
You are the Finance Advisor for LockN Labs (solo founder, targeting $500/mo MRR).

[Initiative brief]
[Revenue model if specified]

Evaluate and return JSON:
{
  "revenueModel": "how this makes money",
  "projectedMRR": "$X/month at [timeframe]",
  "costToImplement": {"compute": "$X", "services": "$X", "time": "X weeks"},
  "breakEvenTimeline": "X months",
  "pricingRecommendation": "suggested pricing tiers",
  "financialRisks": ["risks"],
  "goNoGo": "go|conditional|no-go",
  "conditions": ["if conditional, what must be true"]
}
```

#### 1d. Marketing Review (model: sonnet) — Wave 2
```
You are the Marketing Lead for LockN Labs. The product brand is LockN.

[Initiative brief]
[Target audience]

Evaluate and return JSON:
{
  "targetPersona": "who buys this",
  "positioningStatement": "one-liner value prop",
  "competitorLandscape": ["key competitors and differentiators"],
  "goToMarketStrategy": "launch approach",
  "contentNeeds": ["landing page", "docs", "blog post", etc.],
  "suggestedTickets": [{"title": "...", "estimate": "S|M|L|XL", "priority": 1-4}],
  "launchTimeline": "suggested launch sequence"
}
```

#### 1e. Product Review (model: sonnet) — Wave 2
```
You are the Product Manager for this initiative at LockN Labs.

[Initiative brief]
[All LockN products context from projects/_index.md]

Evaluate and return JSON:
{
  "productVision": "where this fits in the LockN suite",
  "userStories": [{"as": "...", "iWant": "...", "soThat": "..."}],
  "mvpScope": ["minimum features for v1"],
  "deferredScope": ["nice-to-haves for v2+"],
  "successMetrics": [{"metric": "...", "target": "...", "timeframe": "..."}],
  "crossProductDependencies": ["other LockN modules affected"],
  "suggestedMilestones": [{"name": "...", "targetDate": "...", "deliverables": [...]}],
  "riceScore": {"revenue": X, "reach": X, "confidence": X, "effort": X, "total": X}
}
```

### Phase 2: Synthesis (Orchestrator)
Compile all 5 reviews into a unified kickoff document:

#### 2a. Create Project Brief
Write `projects/{slug}/brief.md` with:
- Executive summary (from product review)
- Technical architecture (from engineering review)
- Infrastructure plan (from devops review)
- Business case (from finance review)
- Go-to-market plan (from marketing review)
- Risk register (merged from all reviews)
- Open questions (merged, deduplicated)

#### 2b. Create Roadmap
Write `projects/{slug}/roadmap.md` with:
- Milestones (from product review)
- Ticket breakdown by milestone
- Dependency graph (cross-product)
- Resource allocation recommendation

#### 2c. Decision Log
Write first entry to `projects/{slug}/log.md`:
```markdown
## YYYY-MM-DD — Project Kickoff
**Decision:** Greenlit [initiative name]
**Stakeholder Input:** Engineering (feasibility: X), DevOps (infra: $X/mo), Finance (go/no-go: X), Marketing (persona: X), Product (MVP: X features)
**Key Risks:** [top 3 from risk register]
**Open Questions:** [top 3 unresolved]
**Next Steps:** [first 3 tickets to start]
```

### Phase 3: Linear Ticket Creation
Create the full ticket structure in Linear:

1. **Parent epic** — the initiative itself
2. **Milestone tickets** — one per milestone from product review
3. **Implementation tickets** — merged from all stakeholder suggestions, deduplicated
4. **Infrastructure tickets** — from devops review
5. **Marketing tickets** — from marketing review
6. **QA/Testing tickets** — derived from acceptance criteria

Each ticket gets:
- RICE score (from PM scoring framework)
- Labels: `agent:coder`, `agent:qa`, `revenue-critical` (if applicable), product label
- Dependencies linked
- Acceptance criteria from user stories

### Phase 4: Notion Documentation
Create/update Notion page under Technical Architecture:
- Link to Linear project
- Embed key sections from brief.md
- Architecture diagrams (if applicable)
- API contracts (if applicable)

### Phase 5: Kickoff Summary
Post to Slack #system-heartbeat:
```
🚀 Project Kickoff Complete: [Name]

📊 Stakeholder Scorecard:
  Engineering: [feasibility] | [X weeks est.]
  DevOps: [infra cost] | [security: OK/flagged]
  Finance: [go/no-go] | [projected MRR]
  Marketing: [persona] | [GTM ready: Y/N]
  Product: [RICE score] | [MVP: X features]

📋 Created: [X] Linear tickets across [Y] milestones
📄 Docs: [Notion link] | [brief.md path]
⚠️ Open Questions: [count] (see brief for details)
🎯 First Sprint: [top 3 tickets to start]
```

## Guardrails

### When to Escalate to Sean
- Finance says "no-go"
- Engineering feasibility is "low"
- Estimated cost > $500/month
- Initiative conflicts with existing product strategy
- Open questions that only Sean can answer (business relationships, legal, partnerships)

### Quality Gates
- **Don't create tickets until Phase 2 synthesis is complete** — avoid premature ticket explosion
- **Minimum 3/5 stakeholder reviews must complete** — if an agent fails, proceed with partial input but flag gaps
- **All tickets must have acceptance criteria** — no vague tickets
- **RICE score required on every ticket** — no unscored work enters the pipeline

### Relationship to Other Skills
- **pm-bootstrap:** Discovers existing state of a project → use BEFORE kickoff if project already has code/tickets
- **pm-kickoff (this):** Plans new work → use when starting something new
- **product-management:** Ongoing prioritization → use AFTER kickoff for day-to-day PM decisions
- **coding-pipeline:** Implementation → use AFTER tickets are created and scored

## Quick Start

To kick off a new project:
```
"Kick off [project name]: [one paragraph description]"
```

The orchestrator will:
1. Create project directory if needed
2. Spawn 5 stakeholder agents in parallel
3. Synthesize results
4. Create all Linear tickets
5. Set up Notion docs
6. Post summary to Slack
