# BOOT.md - Startup Checklist

Run these checks on gateway restart. Report issues to Sean via Slack.

## 1. LLM Endpoints
Check all model servers are responding (GET `/v1/models` or `/health`):

| Port  | Service                        | Model                              | Compute |
|-------|--------------------------------|------------------------------------|---------|
| 11434 | Ollama                         | qwen3-embedding, qwen3-vl:8b + cloud gateway (Kimi, DeepSeek, Gemini, Qwen3-VL-235B, Coder-Next-Cloud) | GPU/Cloud |
| 11436 | llama.cpp (GLM)                | GLM-4.7-Flash Q6_K_XL             | GPU     | *Optional — may be intentionally offline* |
| 11437 | llama.cpp (Qwen)               | Qwen3-32B Q5_K_M                  | GPU     |
| 11438 | llama.cpp (A3B)                | Qwen3-Coder-30B-A3B Q8_0          | CPU     |
| 11439 | llama.cpp (Coder-Next)         | Qwen3-Coder-Next Q5_K_M           | GPU     |

**Note:** Port 11440 is currently free (reserved for future model like Nemotron-3-Nano).

Mark any 503/timeout as ⚠️ degraded. A3B on :11438 is subagent default — if it's down, all cron work stalls.

## 2. Model Verification
- Confirm default model is `anthropic/claude-opus-4-6`
- Confirm subagent primary is `llamacpp-coder/qwen3-coder-30b-a3b-q8` (A3B on CPU)
- Confirm subagent fallbacks: Coder-Next GPU → Sonnet → Kimi → Codex (gpt-5.3-codex) → Qwen3-32B

## 3. MCP Integration Validation

**Boot checks run from main session only.** Main session has full MCP tool access (Linear, Notion, Figma), so all integrations are validated in a single pass — no split needed.

| Integration      | Check                          | Pass Condition |
|------------------|--------------------------------|----------------|
| **Linear**       | `linear_list_teams`            | Returns at least one team (expect LockN AI visible) |
| **Notion**       | `notion_API-get-self`          | Returns bot user object |
| **Figma (API)**  | `figma_get_figma_data` with fileKey `6MEJFHJ04qsFBtTJt7bZJO` | Returns file data |
| **Figma Bridge** | `figma-console_figma_get_status` | Connected/healthy transport; if disconnected, include remediation (run Bridge plugin in Figma Desktop Design mode) |

Mark disconnected integrations as ⚠️ and note what's needed to fix.

## 4. Docker Container Health (via DevOps Agent)
Spawn the `devops-cloud` agent to verify all expected containers are running:
- Reference manifest: `memory/state/docker-manifest.json` (32 expected containers)
- Agent runs `docker ps --format '{{.Names}} {{.Status}}'` and diffs against manifest
- Report: missing containers, unhealthy containers, crash-looping containers
- Known issues are noted in the manifest's `notes` field — don't re-alert on those unless status changed
- If `devops-cloud` agent is unavailable, fall back to running the check directly

## 5. Core Services
- Verify Slack socket is connected
- Check LockN Logger API (port 8080) — `curl -s http://localhost:8080/health`
- Check Qdrant vector DB (port 6333) — `curl -s http://localhost:6333/collections`
- Verify `memory_search` returns results (not empty)

## 6. Notify
**Always send boot results to `#system-heartbeat` (`C0ACDPDQ9L5`).** Never post boot output to whatever channel triggered the session.

Include:
- Gateway version
- LLM endpoint status (all green / which degraded)
- MCP integration status (all green / which disconnected)
- Docker health (all green / missing / unhealthy)
- Any config warnings

## 7. Context
- Read today's memory file (`memory/YYYY-MM-DD.md`)
- Check HEARTBEAT.md for pending tasks

## 8. Operational Guardrails
- Boot checks are a **main-session responsibility**. Do not run boot from cron or subagents.
- Boot output goes to `#system-heartbeat` (`C0ACDPDQ9L5`) — never to the triggering channel.
- All integrations must be directly validated (no `NOT_VALIDATED` — main session has full tool access).

---

**All pass:** Reply "🟢 Gateway online, all systems nominal"
**Issues found:** Report them with specific remediation steps. Attempt auto-recovery where safe (e.g., restart a container), but never modify config without asking.
