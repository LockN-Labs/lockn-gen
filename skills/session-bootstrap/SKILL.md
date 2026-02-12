---
name: session-bootstrap
description: Bootstrap a new session with continuity context. Loads handoff state, today's daily log, active Linear tickets, and queries Qdrant memory for relevant context. Run at session start to resume with momentum.
---

# Session Bootstrap

**Purpose:** Zero momentum loss between sessions. Load the minimum context needed to resume work without asking "what are we working on?"

## When to Run
- **Every session start** (mandated in AGENTS.md)
- After `/new` (fresh context)
- When context feels stale

## Bootstrap Sequence (priority order)

### Phase 1: Core State (~5K tokens)

1. **Read handoff:** `memory/state/handoff.md` — last session's active work, blockers, decisions
2. **Read today's daily log:** `memory/daily/YYYY-MM-DD.md` — what happened today
3. **Read yesterday's daily log** (if today's is missing or thin)

### Phase 2: Qdrant Memory Search (~3K tokens)

Query `lockn-memory` collection for context relevant to current work. Extract active projects/topics from handoff, then search:

```bash
# Search memory for active work context
python3 /home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py \
  --search "TOPIC_FROM_HANDOFF" --limit 3
```

**Or via direct Qdrant REST (works from any container):**

```bash
# 1. Get embedding for the query
EMBEDDING=$(curl -s http://localhost:11434/api/embed \
  -d '{"model":"qwen3-embedding","input":["active work priorities blockers"]}' \
  | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['embeddings'][0]))")

# 2. Search lockn-memory
curl -s http://localhost:6333/collections/lockn-memory/points/search \
  -H "Content-Type: application/json" \
  -d "{\"vector\": $EMBEDDING, \"limit\": 5, \"with_payload\": true}"
```

**Smart query construction:**
- Extract project names from handoff → search each project's decisions
- Extract blocker keywords → search for resolution context
- If handoff mentions a ticket (LOC-XXX) → search for related decisions/discussions

### Phase 3: Active Tickets (~2K tokens)

Query Linear for in-progress tickets (see linear-tasker skill).

### Phase 4: Project Index (if needed, ~500 tokens)

Read `projects/_index.md` for portfolio overview — only if handoff doesn't cover enough context.

## Budget Constraints

| Model | Max Bootstrap Context | Warning |
|-------|----------------------|---------|
| Opus (200K) | 15K tokens (~7.5%) | Keep under 30K |
| Coder-Next (256K) | 15K tokens (~6%) | Keep under 30K |
| Qwen3-32B (65K) | 8K tokens (~12%) | Keep under 15K |

**Rules:**
- Total bootstrap load must stay under 15% of model context capacity
- Qdrant results: max 5 chunks, truncate each to 500 chars if over budget
- If handoff is >5K tokens alone, skip Phase 4
- Never load all project briefs at boot — use Qdrant to pull only relevant ones

## Output

After bootstrap, you should know:
1. What was being worked on (handoff)
2. What happened today (daily log)
3. Relevant decisions/context for active work (Qdrant)
4. What tickets need attention (Linear)

**Then act.** Don't summarize what you loaded. Don't ask what to work on. Resume.

## Qdrant Collection Reference

| Collection | Vectors | What's in it |
|-----------|---------|-------------|
| `lockn-memory` | ~133 | Daily logs, handoffs, project briefs, decisions, conventions |
| `lockn-code` | ~948 | Code chunks from all LockN repos |

Both searchable at `localhost:6333` from any session/container.

## Example Bootstrap Flow

```
1. Read memory/state/handoff.md
   → Active: LOC-325 XRPL WebSocket, LOC-271 Phase 3
   → Blockers: sandbox can't run git

2. Read memory/daily/2026-02-09.md
   → Today: shipped LOC-313-317, Brain architecture decided, Swap repo created

3. Search Qdrant: "XRPL WebSocket implementation status"
   → Hit: daily log section about LOC-325 staged files
   → Hit: Swap project decisions about .NET client architecture

4. Search Qdrant: "sandbox blocker resolution"
   → Hit: daily log about elevated exec options

5. Check Linear: In Progress tickets
   → LOC-325 (In Progress), LOC-271 (In Progress)

→ Resume: Apply LOC-325 staged files, continue LOC-271 Phase 3
```
