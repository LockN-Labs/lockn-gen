# Dev Workflow: SDLC Automation

## Architecture

```
Sean (idea/goal)
  → Opus PO (Product Owner)
    → Breaks down into Linear epics + stories with acceptance criteria
    → Prioritizes backlog
  
  → Codex Dev (Execution Agent)
    → Picks up Linear issues
    → Spawns Qwen3 subagents for distributed task execution
    → Owns compilation, integration, and merging
    → Creates PR with tests
  
  → Opus Reviewer (Code Review + Product Sign-off)
    → Reviews code quality
    → Validates against Linear acceptance criteria
    → Approves or requests changes
  
  → Sean (final merge + release decision)
```

## Completion Integrity Rule (MANDATORY)
Before any ticket is moved to **Done**, the executing agent must:
1. Query the ticket's parent + related tickets (`relatedTo` / `blockedBy` / `blocks`)
2. Inspect open siblings for overlap with shipped code
3. Comment on each overlapping sibling with delivered scope
4. Update sibling descriptions with `## [Already Built]` and checkbox acceptance criteria
5. Auto-close siblings that are fully delivered (with explicit attribution comment)

## Roles

### Opus — Product Owner & Reviewer
- **PO mode:** Decomposes goals into Linear epics/stories with clear acceptance criteria
- **Review mode:** Code review + product validation against AC
- **Model:** Claude Opus 4.5 (cloud)
- **Trigger:** Manual via `/project`, `/review`, `/ship`

### Codex — Development Agent  
- **Role:** Primary execution agent for all code changes
- **Model:** OpenAI GPT-5.2 Codex (cloud)
- **Can spawn:** Qwen3-32B subagents (local, port :11437) for parallel task execution
- **Owns:** Branch creation, coding, testing, PR creation, merge conflict resolution
- **Trigger:** Picks up issues from Linear sprint board

### Qwen3 — Task Workers (spawned by Codex)
- **Role:** Distributed code generation for individual files/components
- **Model:** Qwen3-32B Q5_K_M (local, port :11437)
- **Scope:** Individual functions, components, tests — never full integration
- **Reports to:** Codex (who compiles and validates)

## Workflow Steps

### 1. Project Init (`/project new`)
```
Sean: "Build a receipt logging API"
  → Opus PO creates:
    - GitHub repo at ~/repos/<name>
    - Linear project + epic
    - User stories with acceptance criteria
    - Initial backlog prioritization
```

### 2. Sprint Planning (`/sprint`)
```
Opus PO:
  - Reviews Linear backlog
  - Selects stories for sprint
  - Sets priority order
  - Assigns to Codex execution queue
```

### 3. Development (`/build <issue>`)
```
Codex Dev:
  - Reads Linear issue + AC
  - Creates feature branch
  - Optionally spawns Qwen3 workers for:
    - Individual component scaffolding
    - Unit test generation
    - Documentation
  - Compiles all work into cohesive solution
  - Runs tests locally
  - Creates PR linked to Linear issue
```

### 4. Review (`/review <pr>`)
```
Opus Reviewer:
  - Reads PR diff
  - Checks code quality, patterns, security
  - Validates against Linear AC
  - Posts review (approve / request changes)
  - If approved → ready for merge
```

### 5. Ship (`/ship`)
```
Opus PO:
  - Final product sign-off
  - Updates Linear issue status
  - Sean merges (or auto-merge if configured)
```

## Tools & Integrations

| Tool | Purpose | Auth |
|------|---------|------|
| **GitHub** (`gh` CLI) | Repos, branches, PRs | `gh auth login` |
| **Linear** (GraphQL API) | Issues, sprints, projects | API key |
| **Git** | Version control | ✅ Configured (sean@lockn.ai) |
| **sessions_spawn** | Agent orchestration | ✅ Built-in |

## Directory Convention

```
~/repos/
  ├── <project-a>/     ← git repo
  ├── <project-b>/     ← git repo
  └── ...
```

## Credentials Needed

- [ ] `gh auth login` — GitHub authentication
- [ ] `LINEAR_API_KEY` — Linear API key
- [ ] Linear workspace/team ID

## Config Updates Needed

```json5
// openclaw.json additions
{
  tools: {
    agentToAgent: {
      enabled: true,
      allow: ["main"]  // Allow spawned agents to communicate
    }
  }
}
```
