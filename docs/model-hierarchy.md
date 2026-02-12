# Model Hierarchy (Source of Truth)

Purpose: define model routing by workload, including current runtime reality.

Last reviewed: 2026-02-09 18:00 EST

## Runtime Snapshot (verified)
- Main session default model: `anthropic/claude-opus-4-6` (restored 2026-02-09)
- This docs-review cron session: `anthropic/claude-opus-4-6`
- Previous drift (Kimi cloud as default) was resolved via one-shot revert job (already executed and deleted)

## Primary Routing Policy

### 1. Orchestration / Human-Facing Communication
- **Model:** `anthropic/claude-opus-4-6` (alias: `opus`)
- **Context:** 200K tokens
- **Use:** Strategic planning, user communication, complex decisions, PR merges

### 2. Implementation (Local-First, PRIMARY)
- **Model:** `llamacpp-coder-next/qwen3-coder-next-q5k` (alias: `coder-next`)
- **Port:** 11439 (GPU, ~500 tok/s)
- **Context:** 1M tokens (YaRN scaling from 256K native)
- **VRAM:** ~57GB + 24GB KV cache
- **Use:** Feature implementation, refactors, code generation
- **Status:** ✅ Active

### 3. Large-Context Overflow
- **Model:** Qwen3-Coder-Next Q3_K_M (CPU)
- **Port:** 11440 (~15-30 tok/s)
- **Context:** 2M tokens (YaRN scaling)
- **RAM:** ~42GB model + ~100GB KV cache
- **Use:** Massive-context analysis, full codebase reviews
- **Status:** ✅ Active

### 4. Fast Review & Summarization
- **Model:** `llamacpp-qwen/qwen3-32b-q5k` (alias: `qwen`)
- **Port:** 11437
- **Context:** 65K tokens
- **VRAM:** ~23GB
- **Use:** Code review, audits, summaries, architecture validation
- **Status:** ⚠️ Inactive — service needs restart (`systemctl --user start llama-qwen`)

### 5. Cloud Coding/Review Fallback
- **Model:** `openai-codex/gpt-5.3-codex` (alias: `codex`)
- **Use:** When local queues saturated or cloud tooling required

### 6. Cloud Proxy Models (via Ollama Cloud)
- `ollama-cloud/kimi-k2.5:cloud` (alias: `kimi`) — Long-context reasoning, research
- `ollama-cloud/deepseek-v3.2:cloud` (alias: `deepseek`) — Alternative reasoning
- `ollama-cloud/gemini-3-pro-preview:latest` (alias: `gemini`) — Multimodal, large context

### 7. Vision
- **Model:** `qwen3-vl:8b` via Ollama (:11434)
- **Context:** 256K tokens
- **VRAM:** ~10GB (loaded on demand)
- **Use:** Screenshot QA, image analysis, visual debugging, OCR
- **Note:** Port 11441 is RETIRED. All vision goes through Ollama :11434.

### 8. Embeddings
- **Model:** `qwen3-embedding` via Ollama (:11434)
- **Use:** Vector embeddings for Qdrant/RAG

## Active Endpoint Map
| Port | Model | Role | Status |
|------|-------|------|--------|
| 11434 | Ollama (VL + embeddings) | Vision + Embeddings | ✅ Active |
| 11437 | Qwen3-32B Q5_K_M | Review/Summarization | ⚠️ Inactive |
| 11439 | Qwen3-Coder-Next Q5_K_M | PRIMARY Implementation | ✅ Active |
| 11440 | Qwen3-Coder-Next Q3_K_M | Extended Context (CPU) | ✅ Active |

## Governance Notes
- Model default is set in OpenClaw gateway config (`openclaw.json`)
- Cron jobs may override model per-job via `payload.model`
- **Single source of truth:** gateway config owns the default; cron payloads own per-job overrides
- Previous drift (Kimi as default) was resolved 2026-02-09

## Maintenance Rule
Update this file whenever:
- Gateway default model changes
- A model endpoint is added/retired
- Workload routing policy changes
- Service status changes
