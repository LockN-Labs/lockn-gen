# MEMORY.md — Long-Term Memory

*Last curated: 2026-02-11*

---

## 🧑 Sean — Preferences & Working Style
- CEO of LockN Labs. Treats this as a true partnership, not assistant/user.
- Prefers: blunt, direct, structured communication. A/B/C options with recommendation.
- Hates: sycophancy, "Great question!", unnecessary questions, silence without ack.
- **NEVER tell Sean to investigate anything.** Always dispatch investigation to appropriate subagent autonomously. Sean is CEO — he sets priorities, agents execute. No "please check X" or "recommend you run Y". Just do it.
- **Always ack immediately in Slack** before starting work. Never go silent >2 min.
- Sends main progress as new DM messages; thread replies only for deep side discussions.
- Timezone: America/New_York.
- Hardware: Threadripper + RTX Pro 6000 Ada (48GB VRAM).

## 🏗️ Architecture & Infrastructure
- **WSL2** on DESKTOP-VTU9OLK, Docker for all services.
- **Local LLM stack**: llama.cpp servers on ports 11436-11440, Ollama on 11434.
- **Model hierarchy**: Opus (orchestration) → Codex/Coder-Next (execution) → Qwen3-32B (fast queries).
- **Domains**: lockn.ai (prod, currently routed to test), test.lockn.ai (active dev).
- **Auth**: Auth0 SPA with role-based access. Single callback route at `/auth/callback/` (LOC-425, fixed 2026-02-10).
- **Caddy** reverse proxy for all web traffic. Cloudflare tunnel for public access.
- **Email**: Google Workspace, SPF/DKIM/DMARC configured (2026-02-08).

## 🧪 QA Policy (2026-02-11, Sean directive)
- **BE PROACTIVE.** Don't ask Sean whether to continue proactive testing — just do it.
- Never ask the CEO for permission to test. See something that needs testing? Test it.
- QA agents should autonomously find and run tests, flag regressions, expand coverage.

## 📚 Continuous Improvement Protocol (2026-02-11, Sean directive)
- **When a lesson is learned, BURN IT INTO MEMORY immediately.** Don't wait.
- After capturing the lesson, assess: is there a **systemic improvement** to operationalize it?
- Post recommendations/suggestions to **#strategy** (C0ADGH08ZD1).
- Goal: never make the same mistake twice.

## 🔑 Key Decisions
- **2026-02-08**: Auto-allow exec mode enabled. Sean: "remain in auto-allow mode until he disables it."
- **2026-02-08**: Linear upgraded to Business ($18/mo). Slack groupPolicy stays open (single-human workspace).
- **2026-02-08**: HTTPS required before Stripe billing go-live.
- **2026-02-08**: Ship suggestions don't require login; apps do require login.
- **2026-02-10**: Auth0 consolidated to single `/auth/callback/` route (was 55 per-page callbacks).
- **2026-02-10**: 4 Opus-heavy monitoring crons paused to reduce spend.
- **2026-02-11**: Execution-first policy: observation:execution cron ratio must be <3:1.
- **2026-02-11**: Work-executor-hourly cron created (Coder-Next, picks top unblocked ticket).
- **2026-02-11**: WIP limit replaced with staleness tracking. No hard cap — instead flag >48h stale, auto-backlog >7 days.

## 💰 Revenue Path
- Target: $500/mo MRR.
- Current revenue: $0.
- Monthly spend: ~$420 (OpenAI Pro $200, Claude Max $200, Ollama Pro $20).
- Critical path: Auth → Waitlist → Checkout (LOC-421) → Stripe integration → first paying customer.
- **Ship before optimizing.** No dunning, referral loops, or attribution until someone pays.

## 🎯 Products
- **LockN Score**: Local-first sports scoring with CV. Zero direct competitors in on-device space. MVP priority.
- **LockN Speak**: Voice synthesis. Coqui is dead — opportunity to fill open-source gap.
- **LockN Gen**: Media generation (image/video/music). ACE-Step 1.5 for music.
- **LockN Ship**: Suggestion box, posts to Slack #ship channel + creates Linear tickets.

## 🏛️ Linear Organization
- 7 initiatives, ~21 projects.
- **Project-Level Priorities view is the canonical priority order.** Top project = what to work on next. Sean drag-and-drops to reorder. NOT initiative order — project order is what matters.
- Labels: `agent:coder`, `agent:qa`, `revenue-critical` drive automation.
- Naming convention: `[Category] Descriptive title` for issues.
- **Team prefix changed from LOC → LOCKN** (2026-02-11). Old tickets keep LOC-xxx.
- **Slack rule**: Always include full Linear URL when referencing tickets so they unfurl. Format: `<https://linear.app/lockn-ai/issue/LOCKN-xxx|LOCKN-xxx>` (linked ticket name)
- **#ticket-tracking** channel used for ticket tracking threads.

## 🛡️ Memory Integrity Rules (added 2026-02-11)
- **Corrections register:** `memory/corrections.md` overrides stale search results. Check it after every memory_search.
- **Live > Memory:** For infra status, always run live checks before asserting. Memory = history, tools = current state.
- **Conflict resolution:** Most recent source wins. If unsure, say "checking..." and verify live.
- **Correction discipline:** When any fact changes, immediately add SUPERSEDES entry to corrections.md.

## 🧪 QA Policy (2026-02-11, Sean directive)
- **BE PROACTIVE.** Don't ask Sean whether to continue proactive testing — just do it.
- Never ask the CEO for permission to test. See something that needs testing? Test it.
- QA agents should autonomously find and run tests, flag regressions, expand coverage.
- This applies to all agents, not just QA-labeled ones. If you spot a gap, fill it.

## 🔧 Operational Lessons
- **2026-02-10 Auth Cascade**: 3 stacked failures (Auth0 Action SDK mismatch, legacy Caddy basic_auth gate, missing callback URLs). 45 min to resolve. Lesson: temp security gates need expiration tracking.
- **2026-02-11 Execution Gap**: 30+ monitoring crons, 0 execution crons. System went idle for 6+ hours. Lesson: observation without execution is theater.
- **2026-02-11 Demo Bugs**: 4 bugs all avoidable with basic tests. Zero test coverage across all repos. 10 QA tickets created (LOC-459–468).
- **2026-02-11 Stale Memory Hallucination**: Memory search returns old indexed chunks describing past states even after correction. Fix: corrections register (`memory/corrections.md`) as override layer + live-check-first rule for operational facts.
- **2026-02-11 Cron Backlog Storm**: After 8h reboot downtime, 23 overdue cron jobs fired simultaneously, overwhelming the scheduler. Fix: reset stale nextRunAtMs, purge disabled jobs, clear run history.
- **2026-02-11 Slack Message Ordering**: Sending multiple message fragments during investigation causes reverse-order display in Slack. Fix: compose one complete message, don't stream fragments.

## 🤖 Agent Configuration
- **Main (Claws)**: Opus, direct chat with Sean.
- **Orchestrator**: Sonnet, pipeline coordination.
- **Subagents default**: A3B CPU (primary), fallback → Coder-Next GPU → Sonnet → Kimi → Codex.
- **Heartbeat**: Every 1h, Sonnet model.
- **UX agents**: ux-lead (Codex), ux-vision-cloud (Qwen3-VL 235B), ux-vision-local (Qwen3-VL 8B).

## 🖥️ Local Model Infrastructure (2026-02-11)
- **:11437** — Qwen3-32B Q5_K_M (GPU, general queries)
- **:11438** — Qwen3-30B-A3B Q8_0 (CPU, --parallel 8 --ctx-size 524288, subagent default) — 31GB model + ~25GB KV cache, MoE 3B active
- **CRITICAL**: llama.cpp divides ctx-size across parallel slots. 65536/16=4096 per slot → too small. Need 65K+ per slot for subagents (~49K system prompt).
- **:11439** — Coder-Next Q5_K_M (GPU, heavy dev tasks only)
- **:11440** — FREE (reserved for Nemotron-3-Nano 30B-A3B)
- **:11434** — Ollama (cloud gateway: Kimi, DeepSeek, Gemini)
- **A3B not yet systemd-managed** — started via nohup, needs service file
- **Cron routing**: ~60-70% of cron invocations on free local CPU (A3B), rest on cloud/GPU for capability
- **MoE quant rule**: Q8_0 for MoE models (routing decisions sensitive to quantization, RAM is abundant)

## 📊 LockN Control (NEW — 2026-02-11)
- Observability & cost-control plane: Prometheus + Grafana
- Linear project: d73dec54-b377-47cd-9cde-6c5fe9305399
- 15 tickets (LOC-482–496), 3 milestones, 49 story points
- Ports: Grafana 3300, Prometheus 9090, Alertmanager 9093
- Finance: conditional go, must hit $250 MRR in 60 days post-launch
- Brief: projects/control/brief.md

## 🔧 Gateway Health (2026-02-11)
- sessions.json bloat is the #1 gateway perf killer — cron runs accumulate and never get cleaned
- Session pruning cron (8a6aaef5) runs daily at 3am to keep sessions <500
- Backup convention: sessions.json.bak.pre-prune

## 💳 Billing (2026-02-11)
- OpenAI Codex (gpt-5.3-codex) hit billing/credits error — multiple cron jobs affected
- Sean needs to check OpenAI billing dashboard

## 📊 Figma
- Desktop app, Bridge plugin via WebSocket port 9223.
- Main file: "LockN AI" (key: 6MEJFHJ04qsFBtTJt7bZJO).
- 9 components built, 56 design tokens, Light/Dark modes.
- Bridge plugin must run from Design mode (Dev mode = read-only).

## 📢 Slack Channel Management
- **🔥 HARD RULE: No DM thread.** Route ALL messages through appropriate Slack channels. When the right channel doesn't exist yet, surface a channel creation suggestion in #process-improvements.
- **Standing directive**: Whenever there's an opportunity to add a new Slack channel that adds value, suggest it in #process-improvements. Always be thinking about better information architecture.
- **2026-02-11 #product-vision directive**: Sean will post guiding vision messages in `#product-vision`; treat that channel as strategy source-of-truth and operationalize those directives into process + execution handoffs.
- **2026-02-11 #system-prompts directive**: Treat `#system-prompts` as the agent control plane for prompt/process governance (policy changes, incident analysis, behavior validation), not general execution chatter. No policy is complete without a validation check/evidence.
- **2026-02-11 #product-accountability directive**: Use `#product-accountability` as the execution-truth layer (commitments, risks, shipped vs missed outcomes, corrective actions). Sean will use the thread there to interrogate product expectations; per-project PM subagents + CPO must be looped into that channel/thread.

## 🔒 Security Notes
- Elevated exec allowlist has wildcard (`*`) — flagged, acceptable for single-human workspace.
- Slack groupPolicy is open — acceptable per Sean's explicit decision.
- No secrets in MEMORY.md. Keys live in .env files and OpenClaw config (redacted).
