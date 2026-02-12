# OpenClaw Agent Architecture & Model Routing Plan

**Date:** 2026-02-02 | **Hardware:** RTX Pro 6000 96GB / TR Pro 32c / 256GB RAM

---

## 1. Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        OPENCLAW GATEWAY :18789                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  LOCKN INFER (Orchestrator Layer)                         │   │
│  │                                                           │   │
│  │  Default: anthropic/claude-opus-4-5                       │   │
│  │  Role: Intelligently route tasks, spawn subagents         │   │
│  │  Strategy: Preserve tokens — Claude Opus orchestrates,    │   │
│  │            local subagents handle the heavy lifting       │   │
│  └──────────────────────────────────────────────────────────┘   │
│             │ spawns (via sessions_spawn)                        │
│  ┌──────────▼───────────────────────────────────────────────┐   │
│  │  SUBAGENTS (on-demand, per-task)                          │   │
│  │                                                           │   │
│  │  Light tasks (file ops, search, simple code):             │   │
│  │    → ollama/glm-4.7-flash:latest ($0)                     │   │
│  │                                                           │   │
│  │  Dense reasoning (math, architecture, analysis):          │   │
│  │    → ollama/qwen3-32b:latest ($0) [load on demand]        │   │
│  │                                                           │   │
│  │  Complex code / multi-file refactors / novel problems:    │   │
│  │    → anthropic/claude-opus-4-5 (LockN Infer)               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  CRON JOBS (already configured + new)                     │   │
│  │                                                           │   │
│  │  heartbeat (30m) → GLM-4.7-Flash — email/calendar/checks │   │
│  │  daily-7am-summary → GLM-4.7-Flash — morning briefing    │   │
│  │  nightly-docs-crawl → GLM-4.7-Flash — docs maintenance   │   │
│  │  monitor-codex (8h) → GLM-4.7-Flash — subscription check │   │
│  │  monitor-claude-code (8h) → GLM-4.7-Flash — sub check    │   │
│  │  NEW: memory-maintenance (daily 3am) → GLM-4.7-Flash     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  EMBEDDINGS (always-on)                                   │   │
│  │  qwen3-embedding on Ollama :11434 (~1GB VRAM)             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

LOCKN INFER FLOW:
  Claude Opus 4.5 (orchestrator) ──► GLM-4.7-Flash (tool-calling, 90% of tasks)
       │                                           │
   Decide task type                           Spawns subagent via sessions_spawn
       │                                           │
       └─► 90% local (GLM) ──► $0 cost
       └─► 5% reasoning (Qwen3-32B) ──► $0 cost
       └─► 5% complex (Claude Opus) ──► $0.05-0.30/turn
```

**Key Insight**: Claude Opus is expensive, but we only use it for *orchestration* — deciding which task needs which model. The actual work is done by local models or other cloud models as appropriate. This preserves tokens while maintaining high quality.

### Escalation Triggers (Local → Cloud)

| Trigger | Action |
|---------|--------|
| Sean says `/opus` or `/codex` | Use that cloud model for the turn |
| Task explicitly requests "think hard" / "be thorough" | Escalate to Opus |
| Local model fails tool-calling 2x on same task | Auto-escalate |
| Context exceeds 32K tokens (llama.cpp limit) | Use Ollama GLM (200K) or cloud |
| Code generation in unfamiliar language/framework | Prefer cloud |
| Subagent task estimated >30 min with local | Consider cloud for speed |

---

## 2. Model Routing Decision Framework (LockN Infer)

### Task Categories → Model Assignment

| Category | Examples | Model | Cost |
|----------|----------|-------|------|
| **Chat / Q&A** | Casual conversation, quick questions | GLM-4.7-Flash | $0 |
| **Tool-calling** | File ops, web search, browser, shell | GLM-4.7-Flash | $0 |
| **Heartbeats/Cron** | Email check, calendar, maintenance | GLM-4.7-Flash | $0 |
| **Code (simple)** | Bug fixes, small features, scripts | GLM-4.7-Flash | $0 |
| **Reasoning** | Architecture, math, analysis | Qwen3-32B (on-demand) | $0 |
| **Code (complex)** | Multi-file refactors, new systems | Claude Opus 4.5 (LockN Infer) | ~$0.05-0.30/turn |
| **Code (bulk)** | Large codebases, autonomous coding | GPT-5.2-codex (LockN Infer) | ~$0.03-0.15/turn |
| **Creative writing** | Long-form, nuanced prose | Claude Opus 4.5 (LockN Infer) | ~$0.05-0.30/turn |
| **Embeddings** | Memory search | qwen3-embedding | $0 |

### Cloud Cost Estimates

| Model | Input | Output | Typical Turn |
|-------|-------|--------|-------------|
| Claude Opus 4.5 | $15/MTok | $75/MTok | $0.05-0.30 |
| Claude Sonnet 4.5 | $3/MTok | $15/MTok | $0.01-0.06 |
| GPT-5.2-codex | ~$2/MTok | ~$10/MTok | $0.01-0.05 |

**Target monthly cloud spend:** <$30 (mostly local, cloud for ~50-100 turns/month, all routed through LockN Infer)

### LockN Infer Orchestration Strategy

Claude Opus 4.5 is the default orchestrator. It:
- **Analyzes incoming tasks** and decides the optimal model
- **Spawns subagents** via `sessions_spawn` with appropriate model configs
- **Preserves tokens** by delegating to local models for 90% of tasks
- **Escalates only when necessary** — complex reasoning, novel problems, multi-file refactors

**Token Preservation Math:**
- Without orchestration: Claude Opus does 100% of work → ~$100-300/month
- With LockN Infer: Claude Opus does 5% orchestration, GLM/Qwen3 do 90% → ~$5-15/month
- 95% token savings while maintaining quality

---

## 3. Concurrent Inference Plan

### VRAM Allocation Map

```
96GB VRAM Total
├── qwen3-embedding (always loaded)     ~1 GB
├── GLM-4.7-Flash Q6_K (always loaded) ~25 GB
├── [RESERVED for on-demand]            ~47 GB  ← Qwen3-32B Q5_K_M fits here
└── [Headroom / KV cache / overhead]    ~23 GB
                                        ──────
                                        96 GB
```

### Always Loaded (24/7)
- **qwen3-embedding** on Ollama :11434 — 1GB, always needed for memory search
- **GLM-4.7-Flash Q6_K** on Ollama :11435 — 25GB, primary workhorse

### On-Demand Loading
- **Qwen3-32B Q5_K_M** — Load via Ollama when reasoning tasks arise, unload after idle
- **Qwen3-4B Q8_0** — Not needed; GLM-4.7-Flash already handles routing tasks well enough

### Contention Strategy
- Ollama handles model loading/unloading automatically with `OLLAMA_MAX_LOADED_MODELS`
- Set `OLLAMA_MAX_LOADED_MODELS=3` to allow embedding + GLM + one more
- Set `OLLAMA_KEEP_ALIVE=30m` for on-demand models (auto-unload after 30m idle)
- **Retire llama.cpp :11436** — Ollama on :11435 already serves GLM-4.7-Flash with 200K context; no need for a second inference server with worse context (32K)

---

## 4. 24/7 Operation Plan

### Heartbeat (every 30m) — GLM-4.7-Flash
- Check email for urgent messages
- Check calendar for upcoming events (<2h)
- Review HEARTBEAT.md for pending tasks
- Rotate: weather, social mentions (2-4x/day)

### Cron Jobs — All GLM-4.7-Flash
| Job | Schedule | Purpose |
|-----|----------|---------|
| heartbeat | every 30m | See above |
| daily-7am-summary | 7:00 AM ET | Morning briefing |
| nightly-docs-crawl | 2:30 AM ET | Docs maintenance |
| monitor-codex | every 8h | Subscription health |
| monitor-claude-code | every 8h | Subscription health |
| **NEW:** memory-maintenance | 3:00 AM ET | Review daily notes → update MEMORY.md |

### Event-Driven
- Slack messages → Main agent (GLM-4.7-Flash, escalate as needed)
- Subagent spawns → Model chosen by task type
- `/opus` command → Force Claude Opus for that turn

### Night Mode (11 PM – 8 AM ET)
- Heartbeats: silent unless urgent (no Slack messages)
- Cron jobs run normally (docs crawl, memory maintenance)
- Cloud models: never auto-escalated (save money while sleeping)

### Day Mode (8 AM – 11 PM ET)
- Full responsiveness
- Auto-escalation enabled
- Proactive heartbeat messages allowed

---

## 5. Draft openclaw.json Changes

### Key Changes from Current Config:
1. **Default model → GLM-4.7-Flash** (was Opus — biggest cost savings)
2. **Add Qwen3-32B as on-demand model**
3. **Add model aliases** for easy switching
4. **Fallback chain:** GLM → Qwen3-32B → Opus → Codex
5. **Retire llama.cpp** (redundant with Ollama)

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11435/v1",
        "apiKey": "${OLLAMA_API_KEY}",
        "auth": "api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "glm-4.7-flash:latest",
            "name": "GLM-4.7-Flash",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 202752,
            "maxTokens": 2027520
          },
          {
            "id": "qwen3:32b-q5_K_M",
            "name": "Qwen3-32B",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 131072
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/glm-4.7-flash:latest",
        "fallbacks": [
          "ollama/qwen3:32b-q5_K_M",
          "anthropic/claude-opus-4-5",
          "openai-codex/gpt-5.2-codex"
        ]
      },
      "models": {
        "anthropic/claude-opus-4-5": { "alias": "opus" },
        "anthropic/claude-sonnet-4-5-20250514": { "alias": "sonnet" },
        "openai-codex/gpt-5.2-codex": { "alias": "codex" },
        "ollama/glm-4.7-flash:latest": { "alias": "glm" },
        "ollama/qwen3:32b-q5_K_M": { "alias": "qwen" }
      }
    }
  }
}
```

---

## 6. Implementation Steps (Today)

### Step 1: Pull Qwen3-32B into Ollama
```bash
# On the Ollama instance running on :11435
OLLAMA_HOST=127.0.0.1:11435 ollama pull qwen3:32b-q5_K_M
```

### Step 2: Configure Ollama for concurrent models
```bash
# In systemd service or environment:
OLLAMA_MAX_LOADED_MODELS=3
OLLAMA_KEEP_ALIVE=30m
```

### Step 3: Update openclaw.json (LockN Infer config)
- Keep Claude Opus 4.5 as the **default orchestrator** (LockN Infer layer)
- Configure GLM-4.7-Flash and Qwen3-32B as available subagent models
- Set up proper fallback chain for subagents
- Add aliases for easy `/model` switching

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": [
          "ollama/qwen3:32b-q5_K_M",
          "ollama/glm-4.7-flash:latest",
          "openai-codex/gpt-5.2-codex"
        ]
      },
      "models": {
        "anthropic/claude-opus-4-5": { "alias": "opus" },
        "anthropic/claude-sonnet-4-5-20250514": { "alias": "sonnet" },
        "openai-codex/gpt-5.2-codex": { "alias": "codex" },
        "ollama/glm-4.7-flash:latest": { "alias": "glm" },
        "ollama/qwen3:32b-q5_K_M": { "alias": "qwen" }
      }
    }
  },
  "sessions_spawn": {
    "maxConcurrent": 5,
    "timeoutSeconds": 300
  }
}
```

### Step 4: Verify LockN Infer routing
- Test with simple chat → should use GLM (subagent)
- Test with `/opus` → should use Claude Opus directly
- Test with complex reasoning task → should spawn Qwen3 subagent

### Step 5: Update cron jobs to use local model
```bash
openclaw cron edit <id> --model ollama/glm-4.7-flash:latest
```

### Step 6: Add memory-maintenance cron
```bash
openclaw cron add --name "memory-maintenance" \
  --schedule "cron 0 3 * * * @ America/New_York" \
  --prompt "Review memory/YYYY-MM-DD.md files from the past week. Update MEMORY.md with significant events and lessons. Remove outdated entries." \
  --model ollama/glm-4.7-flash:latest
```

---

## Summary

| Metric | Before | After (LockN Infer) |
|--------|--------|---------------------|
| Orchestrator | Local model router | Claude Opus 4.5 (LockN Infer) |
| Default model | Claude Opus 4.5 ($$$) | Claude Opus 4.5 (orchestrator) |
| Local workhorse | GLM-4.7-Flash ($0) | GLM-4.7-Flash ($0) |
| Reasoning model | Qwen3-32B ($0) | Qwen3-32B ($0) |
| Monthly cloud cost (est.) | $100-300+ | <$30 |
| Token preservation | ~5% | ~95% |
| Heartbeat/cron cost | ~$2-5/day | $0 |
| Response latency | Network-dependent | Local, <2s |
| 24/7 capability | Yes (cloud) | Yes (local) |
| Reasoning fallback | N/A | Qwen3-32B → Opus |
