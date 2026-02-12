---
name: coding-pipeline
description: Orchestrate coding tasks by delegating implementation and QA to local Qwen3-Coder-Next (256K context) via llama.cpp API. Use when a coding agent (Codex, Claude Code) needs to implement code changes, write tests, or build features. Instead of generating code directly (burning cloud tokens), delegate coding subtasks to local models running on llama.cpp, then review and assemble results. Triggers on any code generation, test writing, feature implementation, bug fix, or refactoring task.
---

# Coding Pipeline

A five-phase pipeline that separates concerns across three models to maximize quality and minimize cloud token spend. Every phase is observable via Linear comments and GitHub PR history.

## Model Roles

| Phase | Model | Role | Cost |
|-------|-------|------|------|
| 1. Requirements | **Opus** (orchestrator) | Define spec, acceptance criteria, scope | Cloud |
| 2. Architecture | **Codex** (sub-agent) | Solution design, subtask breakdown, draft PR | Cloud |
| 3. Implementation | **Qwen3-Coder-Next** (local :11439, 256K ctx) | Write code + tests via `dispatch.sh` | Free |
| 4. Code Review | **Codex** (sub-agent) | Verify implementation matches design, approve or reject | Cloud |
| 5. Product Sign-off | **Opus** (orchestrator) | Verify acceptance criteria met, close ticket | Cloud |

**Token split:** ~5-10% cloud (Opus + Codex on design/review) / ~90% local (Qwen3-Coder-Next on implementation).

**Context capacity:** Qwen3-Coder-Next supports 256K native context (extendable to 3.1M), allowing full codebase context injection without truncation.

## Core Rules

1. **Opus never writes implementation code.** Opus defines *what*, not *how*.
2. **Codex never writes implementation code.** Codex designs *how*, dispatches to Qwen3-Coder, and reviews results.
3. **Qwen3-Coder does all coding.** Every line of implementation and test code goes through `dispatch.sh`.
4. **Codex signs off before PR.** Implementation must pass architect review before merging.
5. **Every phase transition is logged.** Linear comments + GitHub PR trail = full audit history.
6. **Pipeline is fully autonomous.** Opus handles the entire lifecycle without human intervention — including merging PRs, closing tickets, and starting the next ticket. Only escalate to Sean for strategic decisions, scope changes, or unexpected blockers.

---

## Observability: Linear + GitHub Trail

Every phase posts a structured comment to the Linear ticket so the full pipeline is visible.

### Linear Comments (via `linear-tasker/scripts/comment-issue.sh`)

Post a comment at each phase transition:

**Phase 1 → 2 (Requirements complete):**
```markdown
## 📋 Phase 1: Requirements Complete
**Agent:** Opus (orchestrator)

**Goal:** <one-line summary>

**Acceptance Criteria:**
- [ ] <criterion 1>
- [ ] <criterion 2>

**Scope:** <files/areas affected>
**Constraints:** <patterns, dependencies, things to avoid>

→ Handing off to Codex for architecture.
```

**Phase 2 → 3 (Architecture complete):**
```markdown
## 🏗️ Phase 2: Architecture Complete
**Agent:** Codex (architect)

**Design:**
<brief approach description>

**Subtasks dispatched to Qwen3-Coder:**
1. `<file>` — <what>
2. `<file>` — <what>
3. `<file>` — <what>

**Interfaces defined:**
- `<interface/type signature>`

→ Dispatching {N} subtasks to Qwen3-Coder (local).
```

**Phase 3 → 4 (Implementation complete):**
```markdown
## ⚙️ Phase 3: Implementation Complete
**Agent:** Qwen3-Coder (local, $0 cloud cost)

**Files created/modified:**
- `src/...` ✅
- `tests/...` ✅

**Build:** ✅ passing / ❌ failed (iteration {N})
**Tests:** ✅ {X} passing / ❌ {Y} failing

**Iterations:** {N} (re-dispatches due to build/test failures)

→ Submitting for architect review (Codex).
```

**Phase 4 complete (Sign-off):**
```markdown
## ✅ Phase 4: Architect Sign-off
**Agent:** Codex (architect)

**Verdict:** APPROVED / REJECTED

**Review notes:**
- <finding 1>
- <finding 2>

**If rejected:** <what needs fixing, re-dispatching to Phase 3>
**If approved:** → Creating PR.
```

### Linear Status Transitions

| Event | Linear Status |
|-------|--------------|
| Phase 1 starts | `In Progress` |
| Phase 3 completes | `In Review` |
| Phase 4 approves | Stays `In Review` (PR ready for merge) |
| Phase 4 rejects | Stays `In Review`, comment explains why |
| Phase 5 signs off | `Done` (after PR merge + acceptance verified) |

### GitHub PR Description Template

When Codex creates the PR after Phase 4 sign-off:

```markdown
## Summary
<one-line description>

Closes <LINEAR-TICKET-ID>

## Pipeline Trail
| Phase | Agent | Status |
|-------|-------|--------|
| 1. Requirements | Opus | ✅ Spec defined |
| 2. Architecture | Codex | ✅ {N} subtasks designed |
| 3. Implementation | Qwen3-Coder (local) | ✅ {N} files, {iterations} iterations |
| 4. Code Review | Codex | ✅ Approved |
| 5. Product Sign-off | Opus | ⏳ Pending merge |

## Design Decisions
<key architectural choices and why>

## Changes
- `src/...` — <what changed>
- `tests/...` — <what's tested>

## Acceptance Criteria
- [x] <criterion 1>
- [x] <criterion 2>

## Token Efficiency
- Cloud tokens: ~{X}k (Opus: requirements, Codex: design + review)
- Local tokens: ~{Y}k (Qwen3-Coder: implementation, $0 cost)
```

### GitHub PR Review Comments

If Phase 4 required iterations (Codex rejected, re-dispatched):

```markdown
### Iteration {N} — Architect Feedback
**Rejected:** <reason>
**Re-dispatched:** <subtask description>
**Result:** <fixed / still failing>
```

Post as PR review comments so the iteration history is visible in the PR timeline.

---

## Phase 1: Requirements (Opus)

Opus reads the ticket/issue and produces a structured spec:

- **Goal:** What the feature/fix accomplishes
- **Acceptance criteria:** Measurable conditions for "done"
- **Scope:** Files likely affected, boundaries of change
- **Constraints:** Patterns to follow, tech debt to avoid, dependencies

**Post Linear comment** (Phase 1 template above).
**Update Linear status** to `In Progress`.

Output: A clear spec passed to Codex via `sessions_spawn`.

### Spawning Codex for Phase 2

```
sessions_spawn(
  task: "<spec from Phase 1> + instructions to use coding-pipeline Phases 2-4",
  agentId: "codex",
  label: "loc-XX-pipeline"
)
```

The Codex sub-agent handles Phases 2, 3, and 4 in sequence.

## Phase 2: Architecture (Codex)

Codex receives the spec and produces:

- **Solution design:** Approach, patterns, data flow
- **File list:** Every file to create or modify
- **Interfaces & types:** Method signatures, DTOs, contracts
- **Subtask prompts:** One per file, each with:
  - **What**: Specific implementation task
  - **Where**: Target file path
  - **Interfaces**: Types, method signatures, dependencies
  - **Context**: Relevant existing code (paste snippets or use `--context`)
  - **Constraints**: Patterns to follow, things to avoid

**Post Linear comment** (Phase 2 template above).

**Create Draft PR immediately** after architecture is complete:
```bash
git checkout main && git pull && git checkout -b <branch-name>
git commit --allow-empty -m "LOC-XX: begin <feature> (Phase 2: architecture complete)"
git push -u origin <branch-name>
gh pr create --draft --title "LOC-XX: <feature>" --body "<initial PR body with Phase 2 design>"
```
This creates the PR *before* any implementation so the full evolution is visible.

Good subtask prompt:
> "Create `src/Services/ReceiptService.cs` implementing `IReceiptService`. Methods: `GetByIdAsync(int id) -> ReceiptDto?`, `CreateAsync(CreateReceiptDto dto) -> ReceiptDto`. Use constructor-injected `AppDbContext`. Map entities with manual mapping (no AutoMapper). Follow nullable reference types. Existing entity in `src/Models/Receipt.cs`."

Bad subtask prompt:
> "Write receipt service"

## Phase 3: Implementation (Qwen3-Coder via dispatch.sh)

Codex dispatches subtasks to local Qwen3-Coder:

```bash
# Single task
{baseDir}/scripts/dispatch.sh "Implement GetReceiptById in ReceiptService.cs..."

# With file context piped in
cat src/Models/Receipt.cs | {baseDir}/scripts/dispatch.sh "Implement ReceiptService using this entity model"

# Parallel — independent subtasks
{baseDir}/scripts/dispatch.sh "Implement ReceiptService.cs with CRUD operations" > /tmp/impl.txt &
{baseDir}/scripts/dispatch.sh "Write unit tests for ReceiptService" > /tmp/tests.txt &
wait

# Custom system prompt
SYSTEM_PROMPT="You are a .NET test specialist. Write xUnit tests only." \
  {baseDir}/scripts/dispatch.sh "Write tests for ReceiptService"
```

### Commit After Every Subtask

**Each dispatch result gets its own commit and push** — even if it doesn't build yet:
```bash
# After each dispatch, apply and commit immediately
git add -A && git commit -m "LOC-XX: implement <subtask> (Phase 3, dispatch {N})"
git push
```

This makes every Qwen3-Coder output visible in the draft PR timeline. Raw output first, fixes later.

### Build/Test Verification

After all subtasks are committed, run `dotnet build` / `dotnet test`.
If build/test fails → dispatch fix task with error output as context → commit the fix as a separate commit. Do NOT fix code manually.

**Post Linear comment** (Phase 3 template above) with iteration count and build/test status.

## Phase 4: Review & Sign-off (Codex)

After all implementation is applied and building/passing:

Codex reviews the complete changeset against the Phase 2 design:
- [ ] Implementation matches the architecture design
- [ ] All acceptance criteria from Phase 1 are met
- [ ] No hallucinated imports or dependencies
- [ ] Tests cover meaningful cases (happy path + error cases)
- [ ] Code follows project patterns and conventions
- [ ] Build passes, tests pass

**If approved:** Post Linear comment (Phase 4 approved). Convert draft PR to ready for review:
```bash
gh pr ready <PR-NUMBER>
```
Update PR body with final pipeline trail table.

**If rejected:** Post rejection as a **PR review comment** (not just Linear) so iteration is visible in the PR timeline:
```bash
gh pr review <PR-NUMBER> --comment --body "### Iteration {N} — Architect Feedback
**Rejected:** <reason>
**Re-dispatching:** <subtask description>"
```
Then re-dispatch fixes to Qwen3-Coder (Phase 3), commit the fix, push, and re-review.

**Update Linear status** to `In Review` after PR is marked ready.

---

## Phase 5: Product Sign-off (Opus)

After the PR is merged, Opus closes the loop:

1. **Verify PR merged** — confirm via `gh pr view <NUMBER> --json state`
2. **Review acceptance criteria** from Phase 1 against what actually shipped
3. **Post final Linear comment:**

```markdown
## 🏁 Phase 5: Product Sign-off
**Agent:** Opus (orchestrator)

**PR:** <link> — MERGED ✅

**Acceptance Criteria Review:**
- [x] <criterion 1> — verified
- [x] <criterion 2> — verified
- [ ] <criterion> — deferred to <ticket>

**Notes:** <any observations, follow-up items>

→ Ticket complete.
```

4. **Run sibling cross-reference (MANDATORY) before moving to Done**
   - Query the ticket's parent and related issues (`relatedTo`, `blockedBy`, `blocks`)
   - For each open sibling/related ticket, compare acceptance criteria vs shipped code
   - Add a Linear comment on each overlapping sibling with what was already delivered
   - Update sibling descriptions with an `## [Already Built]` section and checkbox AC format (`- [x]`, `- [ ]`)
   - If a sibling is fully delivered by this work, move that sibling to `Done` with attribution comment
5. **Update Linear status** to `Done`
6. **Update pipeline tracking** (HEARTBEAT.md, memory) with completion

### Why This Matters
Without Phase 5, tickets stay "In Progress" forever and sibling tickets drift stale. Opus owns the full lifecycle — requirements in, product sign-off out. The architect (Codex) validates the *code*; the orchestrator (Opus) validates the *product + ticket graph integrity*.

## Configuration

Worker endpoint defaults to `http://127.0.0.1:11438/v1/chat/completions`.

Override via environment:
```bash
export CODER_API_URL="http://127.0.0.1:11438/v1/chat/completions"
export CODER_MODEL="qwen3-coder"
export CODER_MAX_TOKENS=4096
export CODER_TEMPERATURE=0.2
```

## Error Recovery

- **Worker timeout**: Re-dispatch with shorter/simpler prompt
- **Bad output**: Add more context (paste existing code, error messages)
- **Build failure**: Dispatch fix task with build error as context
- **Test failure**: Dispatch fix task with test output as context
- **Codex rejects in Phase 4**: Specific feedback → re-dispatch to Qwen3-Coder → re-review

## When NOT to Use This Pipeline

- Trivial one-line fixes (just do it directly)
- Documentation-only changes
- Config/CI changes
- Git operations, PR descriptions
