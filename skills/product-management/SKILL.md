# Product Management Skill — Autonomous Prioritization

## Purpose
Eliminate "waiting on Sean's prioritization" as a blocker. PM agents make product decisions autonomously, escalating to CPO agent for cross-product conflicts, and to Sean only for strategic pivots.

## Agent Roles

### PM Agent (per-product, spawned as needed)
- **Scope:** Single product (e.g., LockN Auth, LockN Score)
- **Authority:** Prioritize tickets within their product, approve implementation order, define acceptance criteria
- **Model:** `reasoning-cloud` (Kimi K2.5 — good at structured reasoning, $0 marginal cost)
- **Triggers:** New tickets created, dependency completion, heartbeat review

### CPO Agent (cross-product, escalation target)
- **Scope:** All 13 LockN products + infrastructure
- **Authority:** Resolve cross-product priority conflicts, allocate shared resources (compute, agent time), approve new product initiatives
- **Model:** `research-cloud` (Kimi K2.5 or DeepSeek for deep analysis)
- **Triggers:** PM conflict escalation, weekly portfolio review, revenue milestone events

### CEO (Sean) — Escalation of Last Resort
- **Scope:** Strategic pivots, budget decisions, new business lines
- **Triggers:** See escalation matrix below

## Scoring Framework: Modified RICE

Every ticket gets a **Priority Score** (0-100) computed automatically:

```
Score = (Revenue × 3 + Reach × 2 + Confidence × 1) / (Effort × 1.5)
```

### Dimensions (each 1-10):

| Dimension | How to Score | Data Source |
|-----------|-------------|-------------|
| **Revenue** | Direct revenue impact (1=none, 10=immediate $$$) | Ticket labels, product phase |
| **Reach** | Users/systems affected (1=internal, 10=all customers) | Product brief, user count |
| **Confidence** | How well-defined is the work? (1=vague, 10=clear AC) | Ticket description completeness |
| **Effort** | Implementation complexity (1=trivial, 10=multi-week) | Ticket estimate, subtask count |

### Auto-scoring Rules:
- Tickets with `revenue-critical` label: Revenue = 8+
- Tickets blocking other tickets: Reach += 2
- Tickets with complete acceptance criteria: Confidence += 2
- Tickets in `discovery` phase products: Confidence cap at 5
- Tickets in `growth` phase products: Revenue += 2

## Decision Authority Matrix

| Decision Type | PM Agent | CPO Agent | Sean |
|--------------|----------|-----------|------|
| Ticket priority within product | ✅ Decides | Informed | — |
| Implementation order within product | ✅ Decides | — | — |
| Cross-product resource allocation | Recommends | ✅ Decides | Informed |
| New product initiative (< $100 effort) | — | ✅ Decides | Informed |
| New product initiative (> $100 effort) | — | Recommends | ✅ Decides |
| Strategic pivot / kill product | — | Recommends | ✅ Decides |
| Architecture decisions (tech stack) | Recommends | ✅ Decides | — |
| Revenue model changes | — | Recommends | ✅ Decides |
| Deprioritize revenue-critical ticket | — | ✅ Decides | Informed |

## Escalation Triggers (PM → CPO)

1. **Resource conflict:** Two products need the same agent/compute simultaneously
2. **Priority tie:** Two tickets score within 5 points of each other across products
3. **Dependency deadlock:** Circular or conflicting cross-product dependencies
4. **Confidence < 3:** Ticket too vague to implement — needs product direction
5. **Phase transition:** Product moving between phases (discovery→mvp, mvp→growth)

## Escalation Triggers (CPO → Sean)

1. **Kill decision:** Recommending to stop/pause a product line
2. **Revenue model change:** Pricing, billing, monetization strategy
3. **New business line:** Work outside existing product portfolio
4. **Budget > $500:** Infrastructure or service costs
5. **Legal/compliance:** Licensing, terms of service, privacy

## Integration with Pipeline

### Heartbeat Integration
Every heartbeat, the orchestrator (Claws):
1. Checks for Todo tickets without a priority score → spawns PM agent to score them
2. Checks for scored tickets ready to implement → feeds highest-scored to coding pipeline
3. Checks for cross-product conflicts → spawns CPO agent if needed

### Ticket Lifecycle with PM
```
New Ticket → PM Agent Scores (auto) → Backlog (sorted by score)
                                          ↓
Heartbeat picks highest score → Coding Pipeline → Review → Merge → Done
```

### Weekly Portfolio Review (CPO Agent, cron job)
- Every Monday 6:00 AM ET
- Reviews all product phases, scores, velocity
- Rebalances priorities across products
- Posts summary to #system-heartbeat

## File Structure
```
projects/{slug}/brief.md    — Product brief (exists)
projects/{slug}/log.md      — PM decision log (new)
projects/{slug}/backlog.md  — Scored backlog snapshot (new)
```

## PM Decision Log Format (log.md)
```markdown
## YYYY-MM-DD HH:MM — [Decision Type]
**Agent:** PM-{product} | CPO
**Decision:** [What was decided]
**Rationale:** [Why]
**Score Delta:** [If priority changed, old→new]
**Escalated:** Yes/No (to whom)
```

## Usage

### Score a ticket
```
Spawn PM agent with:
- Ticket details (title, description, labels, estimate)
- Product brief
- Current backlog state
- Ask: Score this ticket using RICE framework, return JSON
```

### Resolve a conflict
```
Spawn CPO agent with:
- Both competing tickets + scores
- Product briefs for both
- Current resource state
- Ask: Which takes priority and why?
```

### Weekly review
```
Spawn CPO agent with:
- All product briefs
- All scored backlogs
- Last week's velocity (tickets completed)
- Ask: Rebalance portfolio priorities, identify blocked products
```
