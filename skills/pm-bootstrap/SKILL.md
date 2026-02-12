---
name: pm-bootstrap
description: Multi-model project bootstrap for LockN modules. Uses research crew (Opus + Codex + Kimi) for comprehensive discovery, then synthesizes into project brief, Notion page, and Linear tickets.
---

# PM Bootstrap Skill

## Purpose
One-time deep bootstrap for each LockN module. After bootstrap, recurring PM maintenance switches to Qwen3-32B (free, fast, sufficient for incremental updates).

## Strategy
- **Bootstrap crew:** Opus (orchestrator/synthesizer) + Codex (code/GitHub research) + Kimi (Linear/competitive research)
- **Ongoing PM:** Qwen3-32B on :11437

## Phases

### Phase 1: Discovery (parallel research agents)
Each agent searches different sources for the target module:

**Codex agent:**
- GitHub repo (README, tree, recent PRs, CI status)
- Codebase architecture (solution structure, key files)
- Open PRs and their status
- Build/test health

**Kimi agent:**
- Linear tickets (Done, In Progress, Backlog) via API
- Ticket relationships and dependencies
- Cross-module references
- Competitive landscape / industry context

**Opus (orchestrator):**
- Workspace memory (daily logs, handoff, MEMORY.md)
- Notion existing pages
- Slack conversation history
- Cross-module dependency mapping
- Today's architectural decisions

### Phase 2: Synthesis (Opus)
Compile all research into:
- `projects/{slug}/brief.md` — comprehensive project brief
- `projects/{slug}/log.md` — project activity log
- `projects/{slug}/decisions.md` — decision log with rationale

### Phase 3: Publish
- Create/update Notion page under Technical Architecture
- Update `projects/_index.md` with new confidence score
- Create any missing Linear tickets identified during discovery

### Phase 4: Verify
- Confirm Notion page exists and has content
- Confirm brief.md confidence >= 0.7
- Confirm Linear ticket count matches expectations
- Report summary to Sean

## Output Format (brief.md)
```markdown
# LockN {Name} — Project Brief

## Status
- Phase: {discovery|mvp|growth|mature}
- Confidence: {0.0-1.0}
- Last Verified: {YYYY-MM-DD}

## Overview
{2-3 sentence description}

## Architecture
{Stack, repo, infra, key components}

## Key Decisions
{Table: Date | Decision | Rationale | Ticket}

## Dependencies
{Upstream, downstream, cross-module}

## Completed Work
{Done tickets with brief descriptions}

## Backlog
{Prioritized backlog tickets}

## Open Questions
{Unresolved architectural/strategic questions}

## Sources
{Where this information came from}
```

## Persistence Checklist
1. ✅ brief.md in projects/{slug}/
2. ✅ log.md in projects/{slug}/
3. ✅ decisions.md in projects/{slug}/
4. ✅ _index.md updated with confidence
5. ✅ Notion page under Technical Architecture
6. ✅ Daily memory log updated
7. ✅ Files synced to workspace (not just sandbox)

## Notion Location
Parent: Technical Architecture (`302b5f0c-1a51-8169-b03d-c136785b195e`)
