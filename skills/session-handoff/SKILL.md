---
name: session-handoff
description: Persist session state before context flush or /new. Writes handoff.md, updates daily log, and triggers memory re-index so Qdrant stays fresh.
---

# Session Handoff

**Purpose:** Capture session state so the next session resumes seamlessly.

## When to Run
- **Before `/new`** — always
- **At 50% context** — proactively
- **Before long idle** (>2h gap expected)
- **On request** — "save state", "handoff", etc.

## Handoff Steps

### 1. Write `memory/state/handoff.md`

Include:
```markdown
# Session Handoff
- **Written:** ISO timestamp
- **Session model:** model name
- **Context at write:** tokens used / capacity

## Active Work
- What's in progress, with ticket numbers

## Sean's Current Priority
- What Sean cares about right now

## Immediate Next Actions (priority order)
1. First thing next session should do
2. Second thing
3. ...

## Blocked Items
- What's stuck and why

## Decisions Made This Session
- Key decisions with rationale

## Conversations with Sean
- Important context from human interaction

## Files Modified This Session
- List of files changed

## Context for Next Session
- Anything the next session needs to know that doesn't fit above
```

### 2. Update Daily Log

Append session summary to `memory/daily/YYYY-MM-DD.md`:
- What was accomplished
- Decisions made
- Blockers encountered
- Tickets progressed

### 3. Trigger Memory Re-Index

After writing handoff + daily log, trigger incremental re-index so Qdrant has fresh data:

```bash
python3 /home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py
```

This ensures the next session's Qdrant queries return current context.

### 4. Verify

Confirm handoff is written and Qdrant is updated. Don't just "plan to write it" — actually write it.

## Anti-Patterns
- ❌ Writing handoff but forgetting to update daily log
- ❌ Writing handoff but not re-indexing (Qdrant goes stale)
- ❌ Waiting until context overflow to handoff (data loss)
- ❌ Including raw conversation dumps (too verbose — distill key points)
