# Orchestration Framework - Option A Implementation

## Architecture Overview

```
Main Session (Opus) ← Sean's direct conversations
├── Orchestrator Agent (Sonnet) ← Autonomous pipeline management
│   ├── Dev Agents (Coder-Next) ← Implementation work
│   ├── Review Agents (Qwen3-32B) ← Code review
│   ├── Research Agents (Mixed) ← Analysis
│   └── DevOps Agents (Codex) ← Infrastructure
└── Other Subagents ← Ad-hoc tasks
```

## Delegation Pattern

**Main Session responsibilities:**
- Respond to Sean's direct messages with Opus quality
- High-level strategic decisions
- Spawn orchestrator when autonomous work is needed
- Monitor orchestrator progress

**Orchestrator responsibilities:**  
- Pipeline management (coding-pipeline, ticket monitoring)
- Heartbeat-style autonomous work (moved from heartbeat)
- Subagent spawning and coordination
- Progress reporting back to main session

**Subagent responsibilities:**
- Focused execution (coding, review, research)
- Report results back to orchestrator

## Usage Patterns

### 1. Sean Request → Orchestrated Work
```
Sean: "Implement feature X"
Main (Opus): "I'll coordinate the implementation"
  → Spawn Orchestrator (Sonnet)
    → Orchestrator spawns Dev Agent (Coder-Next)  
    → Dev Agent implements
    → Orchestrator spawns Review Agent (Qwen3-32B)
    → Review Agent reviews
    → Orchestrator merges & updates Linear
  → Main reports back to Sean
```

### 2. Autonomous Pipeline Monitoring  
```
Main Session: Spawn persistent Orchestrator
Orchestrator: 
  - Check Linear for Todo tickets
  - Monitor open PRs
  - Trigger coding-pipeline when ready
  - Spawn review agents for PRs
  - Merge completed work
  - Report periodic status to main
```

### 3. Mixed Work (Conversation + Automation)
```
Sean: Asks question while pipeline runs
Main (Opus): Responds directly to Sean
Orchestrator: Continues autonomous work in parallel  
```

## Implementation Status

✅ **Config Updated**: Main session now Opus, orchestrator agent created
⏳ **Framework Design**: This document  
⏳ **Heartbeat Migration**: Move autonomous work from heartbeat to orchestrator
⏳ **Testing**: Verify orchestrator can manage pipeline

## Cost Impact

**Before (Sonnet Main):**
- Sean conversations: ~$3/1M tokens
- Orchestration: ~$3/1M tokens  
- Total main session: ~$3/1M tokens

**After (Option A):**
- Sean conversations: ~$15/1M tokens (Opus)
- Orchestration: ~$3/1M tokens (delegated to Sonnet orchestrator)
- **Net**: 5x cost for conversations, same cost for automation

**Productivity gain**: +30% (estimated) from better decision quality

## Next Steps

1. **Update HEARTBEAT.md** - Shift autonomous work to orchestrator pattern
2. **Test orchestrator** - Spawn and verify it can manage pipeline  
3. **Monitor costs** - Track actual usage patterns
4. **Optimize** - Fine-tune delegation boundaries

---

*Architecture implemented: 2026-02-10*