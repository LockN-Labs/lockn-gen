---
name: compute-priority
description: Toggle between local-first (Qwen3-Coder-Next) and cloud-first (Opus) compute modes. Use when switching primary model for cost optimization or capability needs. Triggers on "compute local", "compute cloud", "compute status", "switch to local", "switch to cloud", "go local", "go cloud".
---

# Compute Priority

Toggle the primary inference model between local (free, fast) and cloud (premium, nuanced).

## Modes

| Mode | Primary Model | Fallbacks | Use Case |
|------|---------------|-----------|----------|
| `local` | Qwen3-Coder-Next (port 11439) | Opus → Codex → Qwen3-32B | Cost optimization, coding tasks, large context |
| `cloud` | Claude Opus 4.5 | Coder-Next → Codex → Qwen3-32B | Complex reasoning, nuanced communication |

## Commands

### Switch to Local
```
/compute local
```
Sets Coder-Next as primary. Use for routine work, coding, large context sessions.

### Switch to Cloud
```
/compute cloud
```
Sets Opus as primary. Use for complex reasoning, ambiguous decisions, important communication.

### Check Status
```
/compute status
```
Shows current mode and active model.

## Implementation

To switch modes, use `gateway config.patch`:

### Local Mode Config
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "llamacpp-coder-next/qwen3-coder-next-q5k",
        "fallbacks": ["anthropic/claude-opus-4-5", "openai-codex/gpt-5.2-codex", "llamacpp-qwen/qwen3-32b-q5k"]
      },
      "heartbeat": { "model": "llamacpp-coder-next/qwen3-coder-next-q5k" },
      "subagents": { "model": "llamacpp-coder-next/qwen3-coder-next-q5k" }
    }
  }
}
```

### Cloud Mode Config
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-5",
        "fallbacks": ["llamacpp-coder-next/qwen3-coder-next-q5k", "openai-codex/gpt-5.2-codex", "llamacpp-qwen/qwen3-32b-q5k"]
      },
      "heartbeat": { "model": "anthropic/claude-opus-4-5" },
      "subagents": { "model": "anthropic/claude-opus-4-5" }
    }
  }
}
```

### Status Check
Use `session_status` tool to get current model, then report:
- Current mode (local/cloud) based on primary model
- Active model name
- Context usage

## After Switching

Gateway restarts automatically after config.patch. Confirm new model via `session_status`.
