# Agent Architecture (Current)

Purpose: canonical view of runtime agent roles, boundaries, and execution flow.

Last reviewed: 2026-02-09 18:00 EST

## Current Topology

### Sessions
- **main:** Orchestrator session (Slack-facing, planning + coordination, Opus)
- **isolated cron sessions:** 24 scheduled autonomous tasks across 7 lanes
- **subagents:** Spawned for bounded work (review, audits, implementation slices)

### Model-to-Role Mapping
| Role | Model | Port/Service |
|------|-------|-------------|
| Orchestrator | Opus (cloud) | Gateway default |
| Implementation | Coder-Next Q5 (local) | :11439 |
| Extended analysis | Coder-Next Q3 CPU (local) | :11440 |
| Review / Summarization | Qwen3-32B (local) | :11437 (⚠️ inactive) |
| Vision | Qwen3-VL 8B (local) | :11434 (Ollama) |
| Cloud coding fallback | Codex (cloud) | OpenAI |
| Cloud research | Kimi K2.5, DeepSeek, Gemini | Ollama Cloud |

## Execution Pattern
1. Parse work into independent lanes
2. Run parallel where safe (review/audit/research)
3. Keep implementation local-first (`coder-next` via coding-pipeline)
4. Use cloud models for orchestration and high-ambiguity decisions
5. Qwen3-32B handles lightweight review/summaries (when active)

## Sandbox Security Model (AD-007)
| Model Size | Web Access | Sandbox | Use Case |
|------------|------------|---------|----------|
| ≤32B (Qwen3-32B) | ❌ Denied | ✅ Enabled | Code execution, review |
| 80B+ (Coder-Next) | ✅ Allowed | ❌ Off | Implementation |
| Cloud (Opus, Codex) | ✅ Allowed | ❌ Off | Orchestration |

## Guardrails
- No direct production merges without review state checks
- Keep tasks bounded when delegating to local models (see AGENTS.md "Bounded Task Design")
- Never spawn local-model subagents from contexts >100K tokens
- Elevated exec uses `elevated: true` flag; always backup configs before changes

## GitHub App Bot Identities
5 GitHub Apps provide per-agent attribution on PRs and reviews:
- lockn-orchestrator (primary — reviews/merges)
- lockn-coder, lockn-architect, lockn-qa, lockn-devops
- Auth flow: JWT (RS256) → installation token (1hr expiry)

## Known Issues
1. **llama-qwen service inactive** — Qwen3-32B review lane is down
2. **13 containers stopped** — Auth, Gen, Logger, Qdrant stacks need restart
3. **lockn-speak-dev crash loop** — SIGSEGV (signal 139), needs investigation

## Maintenance Rule
Update when agent topology, model assignments, or security boundaries change.
