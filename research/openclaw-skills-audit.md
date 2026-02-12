# OpenClaw Skills Audit — 24/7 Agentic Setup

**Date:** 2026-02-02
**Purpose:** Identify essential, useful, and missing skills for a production 24/7 OpenClaw system
**Hardware:** Threadripper Pro 32c, RTX Pro 6000 96GB, 256GB RAM
**Stack:** Local LLMs (GLM-4.7-flash) + cloud escalation (Claude Opus), Slack channel

---

## Current Ecosystem Overview

- **ClawHub Registry:** 3,000+ skills published (clawhub.com)
- **Awesome List:** [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 1,715+ curated (spam/crypto filtered)
- **Official Archive:** [openclaw/skills](https://github.com/openclaw/skills) — all published skill versions archived
- **ClawHub CLI:** `npx clawhub@latest install <slug>` or use the bundled `clawhub` skill

---

## Already Installed (52 bundled skills)

These came with the OpenClaw install. Relevant ones bolded:

| Skill | What it Does | Relevance |
|-------|-------------|-----------|
| **slack** | Slack channel control (send, react, pin) | ✅ CORE — our primary channel |
| **skill-creator** | Create/update skills with proper structure | ✅ CORE — build custom skills |
| **clawhub** | Search/install/publish skills from registry | ✅ CORE — skill management |
| **coding-agent** | Run Codex/Claude Code/OpenCode via bg process | ✅ CORE — dev workflows |
| **tmux** | Remote-control tmux sessions, send keystrokes | ✅ CORE — interactive CLI automation |
| **github** | gh CLI for issues, PRs, CI, API | ✅ CORE — dev workflows |
| **weather** | Current weather + forecasts via wttr.in | ✅ Useful for daily briefings |
| **himalaya** | Email via IMAP/SMTP (list, read, send, search) | ✅ MUST HAVE — email integration |
| **gog** | Google Workspace: Gmail, Calendar, Drive, Sheets | ✅ MUST HAVE — calendar/email/docs |
| **summarize** | Summarize URLs, podcasts, transcripts | ✅ Useful for research |
| **blogwatcher** | Monitor RSS/Atom feeds for updates | ✅ Useful for market monitoring |
| **session-logs** | Search/analyze own session logs with jq/rg | ✅ Useful for ops/debugging |
| **model-usage** | Per-model usage/cost tracking | ✅ Useful for cost management |
| **1password** | 1Password CLI for secrets management | ✅ Auth management |
| **browser** | (bundled tool, not skill) Web automation | ✅ CORE |
| **canvas** | Display HTML on connected nodes | Nice to have |
| **gemini** | Gemini CLI for one-shot Q&A | Nice to have (backup model) |
| **openai-whisper** | Local speech-to-text (no API) | Nice to have |
| **openai-whisper-api** | Cloud Whisper transcription | Nice to have |
| **openai-image-gen** | Image generation via OpenAI | Nice to have |
| **nano-banana-pro** | Image gen via Gemini 3 Pro | Nice to have |
| **nano-pdf** | PDF editing with natural language | Nice to have |
| **notion** | Notion API integration | Skip (unless using Notion) |
| **obsidian** | Obsidian vault management | Skip (unless using Obsidian) |
| **trello** | Trello board management | Skip (unless using Trello) |
| **bird** | X/Twitter CLI | Nice to have (social monitoring) |
| **sag** | ElevenLabs TTS | Nice to have |
| **sherpa-onnx-tts** | Local TTS (offline) | Nice to have |
| **discord** | Discord channel control | Skip (not our channel) |
| **bluebubbles** | iMessage bridge | Skip (WSL, no macOS) |
| **imsg** | iMessage CLI | Skip (no macOS) |
| **wacli** | WhatsApp CLI | Skip (unless needed) |
| **spotify-player** | Spotify control | Skip |
| **sonoscli** | Sonos control | Skip |
| **blucli** | BluOS control | Skip |
| **openhue** | Philips Hue control | Skip |
| **eightctl** | Eight Sleep pod control | Skip |
| **camsnap** | RTSP/ONVIF camera capture | Skip |
| **peekaboo** | macOS UI automation | Skip (WSL) |
| **voice-call** | Voice call plugin | Skip |
| **apple-notes** | Apple Notes via memo CLI | Skip (no macOS) |
| **apple-reminders** | Apple Reminders | Skip (no macOS) |
| **bear-notes** | Bear notes | Skip (no macOS) |
| **things-mac** | Things 3 task manager | Skip (no macOS) |
| **food-order** | Foodora reorder | Skip |
| **ordercli** | Foodora CLI | Skip |
| **goplaces** | Google Places search | Nice to have |
| **local-places** | Local places proxy | Skip |
| **gifgrep** | GIF search | Skip |
| **songsee** | Audio spectrograms | Skip |
| **video-frames** | Extract video frames | Nice to have |
| **mcporter** | MCP server management | ✅ Useful — MCP ecosystem |
| **oracle** | Oracle CLI for prompt bundling | Nice to have |

---

## Skills to Install from ClawHub

### 🔴 MUST HAVE

| Skill | What it Does | Source | Security |
|-------|-------------|--------|----------|
| **chromadb-memory** | Long-term memory via ChromaDB + local Ollama embeddings | ClawHub | ⚠️ Review — community skill, but aligns with our Ollama setup |
| **miniflux-news** | Fetch/triage unread RSS from Miniflux instance | ClawHub (hartlco) | ✅ Simple API wrapper |
| **technews** | TechMeme top stories + social reactions | ClawHub (kesslerio) | ✅ Read-only scraping |
| **commit-analyzer** | Analyze git commit patterns for autonomous operation health | ClawHub (bobrenze-bot) | ✅ Local git analysis |
| **agent-news** | Monitor HN, Reddit, arXiv for AI agent developments | ClawHub (bobrenze-bot) | ✅ Read-only monitoring |
| **linux-service-triage** | Diagnose Linux service issues (logs, systemd, permissions) | ClawHub (kowl64) | ✅ Diagnostic commands |
| **skill-vetter** | Security-first skill vetting for AI agents | ClawHub (spclaudehome) | ✅ Security tool |

### 🟡 NICE TO HAVE

| Skill | What it Does | Source | Security |
|-------|-------------|--------|----------|
| **exa-web-search-free** | Free AI-powered web search via Exa | ClawHub | ⚠️ External API |
| **deepwiki** | Query DeepWiki for GitHub repo documentation | ClawHub (arun-8687) | ✅ Read-only |
| **read-github** | Read GitHub repos via gitmcp.io (LLM-optimized) | ClawHub (am-will) | ✅ Read-only |
| **gitclaw** | Auto-backup workspace to GitHub via cron | ClawHub (marian2js) | ✅ Git operations |
| **docker-essentials** | Docker management commands/workflows | ClawHub (arnarsson) | ✅ Reference skill |
| **multi-coding-agent** | Run multiple coding agents in parallel | ClawHub (kesslerio) | ⚠️ Spawns processes |
| **prompt-log** | Extract transcripts from AI session logs | ClawHub (thesash) | ✅ Local file parsing |
| **fabric-pattern** | Integration with Fabric AI framework | ClawHub (apuryear) | ⚠️ Review |
| **nodetool** | Visual AI workflow builder (ComfyUI meets n8n) | ClawHub (georgi) | ⚠️ Complex, review |
| **post-queue** | Queue posts for rate-limited platforms | ClawHub (luluf0x) | ✅ Local queue |
| **beszel-check** | Monitor home lab servers via Beszel/PocketBase | ClawHub (karakuscem) | ✅ API wrapper |
| **agentmemory** | E2E encrypted cloud memory, 100GB free | ClawHub (badaramoni) | ⚠️ External service — trust? |
| **work-report** | Generate work reports from git commits | ClawHub (leeguooooo) | ✅ Local git analysis |
| **project-context-sync** | Keep project state doc updated per commit | ClawHub (joe3112) | ✅ Local file management |
| **senior-architect** | System architecture design guidance | ClawHub (alirezarezvani) | ✅ Prompt-only skill |
| **tdd-guide** | Test-driven development workflow | ClawHub (alirezarezvani) | ✅ Prompt-only skill |
| **autoresponder** | Auto-respond to iMessage based on rules | ClawHub (koba42corp) | ⚠️ macOS only |
| **smtp-send** | Send emails via SMTP (plain, HTML) | ClawHub (xiwan) | ✅ Standard SMTP |
| **conventional-commits** | Format commit messages to spec | ClawHub (bastos) | ✅ Prompt-only |
| **claude-optimised** | Guide for optimizing CLAUDE.md files | ClawHub (hexnickk) | ✅ Prompt-only |

### 🔵 SKIP

- **Moltbook ecosystem** (27 skills) — AI social network, meme coins, agent-to-agent chat. Fun but not production-relevant.
- **Apple-specific skills** — We're on WSL2/Linux, no macOS.
- **Smart home skills** (Hue, Sonos, Eight Sleep) — Not relevant to business ops.
- **Food ordering** — Not relevant.
- **Gaming skills** — Not relevant.
- **Crypto/DeFi skills** — Filtered from awesome list already, high risk.

---

## Gap Analysis — Skills to Build

These don't exist in ClawHub and should be created using `skill-creator`:

### 🔴 Critical Gaps

| Skill to Build | Purpose | Priority |
|----------------|---------|----------|
| **model-router** | Route tasks to local LLM vs cloud based on complexity/cost/latency. Core to our hybrid setup. | P0 |
| **polymarket-monitor** | Monitor Polymarket prediction markets for specified topics, alert on movements. | P1 |
| **system-health** | Monitor local system: GPU VRAM, CPU, disk, Ollama/llama.cpp status, gateway health. Cron-friendly. | P0 |
| **invoice-tracker** | Track consulting invoices, billable hours, payment status. Solo founder essential. | P1 |
| **client-crm** | Lightweight CRM: track leads, clients, project status, follow-ups. | P1 |
| **local-llm-bench** | Benchmark local models, track inference speed, compare quantizations. | P2 |

### 🟡 Nice-to-Have Gaps

| Skill to Build | Purpose | Priority |
|----------------|---------|----------|
| **calendar-digest** | Daily/weekly calendar briefing with smart prioritization (wraps gog) | P2 |
| **email-triage** | Auto-classify emails by urgency, draft responses for review (wraps himalaya/gog) | P2 |
| **research-pipeline** | Multi-step research: web search → fetch → summarize → save to knowledge base | P2 |
| **cron-manager** | UI/helper for managing OpenClaw cron jobs, viewing schedules, debugging | P3 |
| **cost-tracker** | Track all API costs across providers (OpenAI, Anthropic, Google) in one place | P2 |
| **webhook-handler** | Generic webhook receiver for external service integrations | P3 |

---

## Recommended Installation Priority

### Phase 1 — Immediate (this week)
```bash
npx clawhub@latest install technews
npx clawhub@latest install linux-service-triage
npx clawhub@latest install skill-vetter
npx clawhub@latest install commit-analyzer
npx clawhub@latest install conventional-commits
```

### Phase 2 — After custom skills built
```bash
npx clawhub@latest install chromadb-memory
npx clawhub@latest install agent-news
npx clawhub@latest install read-github
npx clawhub@latest install deepwiki
npx clawhub@latest install work-report
```

### Phase 3 — Custom skills to create
1. `model-router` — P0, build first
2. `system-health` — P0, build second
3. `polymarket-monitor` — P1
4. `client-crm` / `invoice-tracker` — P1

---

## Security Notes

- **ClawHub is open by default** — anyone with a 1-week-old GitHub account can publish
- **Always vet skills before installing** — use `skill-vetter` skill or manual review
- **Prompt-only skills** (senior-architect, tdd-guide, etc.) are lowest risk — just SKILL.md guidance
- **Skills with scripts** (install steps, binaries) need careful review
- **Skills hitting external APIs** — review what data leaves the machine
- The `openclaw/skills` repo archives all published versions for auditing

---

## Sources

- [ClawHub Registry](https://clawhub.com) — 3,000+ skills
- [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 1,715+ curated
- [openclaw/skills](https://github.com/openclaw/skills) — official archive
- [openclaw/clawhub](https://github.com/openclaw/clawhub) — registry source
- [OpenClaw Skills Docs](https://docs.openclaw.ai/tools/skills)
- Local inspection: `/home/sean/.npm-global/lib/node_modules/openclaw/skills/`
