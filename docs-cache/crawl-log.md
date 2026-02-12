# Docs Crawl Log

## 2026-02-03T02:30 (America/New_York)

**Site:** OpenClaw Docs (https://docs.openclaw.ai)
**Status:** ✅ Initial snapshot complete
**Output:** `docs-cache/openclaw-docs/2026-02-03T02-30/`

### Pages captured:
| Page | URL | Size | Notes |
|------|-----|------|-------|
| index.md | / | 3.6 KB | Main docs landing page |
| getting-started.md | /start/getting-started | 2.8 KB | Quickstart guide |
| configuration.md | /gateway/configuration | 2.9 KB | Truncated (full page >50KB) |
| help.md | /help | 4.4 KB | Full docs navigation/index |

**Total:** 13.8 KB across 4 pages

### Diff vs prior:
- **Status:** Initial crawl (no prior snapshot)
- **Next crawl:** Will compare MD5 checksums to detect changes

### Checksums (MD5):
```
c57b6dc9f7e71ed1078d075fbc68725a  index.md
6bd26e0e1ec1aac1088489d2615ca3ad  getting-started.md
f7f1d9ef14260579fdbda5dd34d8f25c  configuration.md
a7000881998f70a8bba919a7149e15f1  help.md
```

---

## 2026-02-04T02:30 (America/New_York)

**Site:** OpenClaw Docs (https://docs.openclaw.ai)
**Status:** ✅ Crawl complete — significant changes detected
**Output:** `docs-cache/openclaw-docs/2026-02-04T02-30/`

### Pages captured:
| Page | URL | Size | Notes |
|------|-----|------|-------|
| index.md | / | 8.5 KB | Main docs landing page |

**Total:** 8.5 KB (index page only)

### Diff vs prior (2026-02-03):
**Status:** 🔴 SIGNIFICANT CHANGES (~5KB added)

#### Key changes:
1. **Dashboard URL** — Added localhost alternative + browser behavior clarification
2. **Network model** — Expanded with multiple gateways link, token generation note, TCP bridge deprecation
3. **Features** — Added streaming doc link, subscription auth details (Claude Pro/Max, ChatGPT/Codex), group activation toggle
4. **Deprecation notice** — Legacy Claude/Codex/Gemini/Opencode paths removed; Pi is only path
5. **Quick start** — Massively expanded: from-source, multi-instance, pnpm/npm alternatives, openclaw doctor
6. **NEW: Configuration section** — Basic config example with allowFrom and mention rules
7. **NEW: Docs index** — Full navigation tree (~50 doc pages organized by category)
8. **Credits** — Added titles ("lobster whisperer", "security pen-tester")
9. **NEW: Core Contributors** — Maxim Vovshin (Blogwatcher), Nacho Iacovino (Location parsing)

**Full diff saved to:** `diff-vs-prior.patch`

### Checksums (MD5):
```
d3408d353527c6acce5033fa1c9e6fd8  index.md
```

---

## 2026-02-05T02:30 (America/New_York)

**Site:** OpenClaw Docs (https://docs.openclaw.ai)
**Status:** ✅ Crawl complete — landing page restructured
**Output:** `docs-cache/openclaw-docs/2026-02-05T02-30/`

### Pages captured:
| Page | URL | Size | Notes |
|------|-----|------|-------|
| index.md | / | 1.3 KB | Main docs landing page (simplified) |
| quickstart.md | /start/quickstart | 0.8 KB | Quick start guide |
| help.md | /help | 0.5 KB | Help/troubleshooting links |
| configuration.md | /gateway/configuration | 1.6 KB | Truncated (full page ~99KB) |

**Total:** 4.2 KB across 4 pages

### Diff vs prior (2026-02-04):
**Status:** 🟡 MODERATE CHANGES (restructure, ~4KB reduction in landing page)

#### Key changes:
1. **Landing page simplified** — Removed detailed architecture diagram, network model section, features list
2. **Tagline updated** — "Any OS gateway for AI agents" (was "Any OS + WhatsApp/Telegram/Discord/iMessage gateway")
3. **Structure cleaned up** — More concise intro, links to Quick start instead of inline steps
4. **Sections removed from landing:**
   - "How it works" architecture diagram (ASCII art)
   - "Network model" details
   - "Features (high level)" list
   - Dashboard/Control UI details moved elsewhere
5. **Configuration page** — Massive expansion (~99KB, truncated in snapshot), now includes:
   - Full schema documentation
   - Config includes ($include)
   - Per-channel settings (WhatsApp, Telegram, Discord, Slack, Signal, iMessage, etc.)
   - Multi-agent routing
   - Sandbox configuration
   - Model providers (MiniMax, Z.AI, Moonshot, Cerebras, local LLMs)
   - Hooks/webhooks
   - Gateway settings

**Full diff saved to:** `diff-vs-prior.patch`

### Checksums (MD5):
```
adc65cc0b4a43ff4ebe91f8e05163c42  configuration.md
baf7e6edf5a0326ff27de1d7a87f1e87  index.md
cabb0b79f4d39e6cb00843a905bf7d60  help.md
ea0fd1a05a9dbd010498bd01b02f7b1c  quickstart.md
```

---

## 2026-02-07T02:30 (America/New_York)

**Site:** OpenClaw Docs (https://docs.openclaw.ai)
**Status:** ✅ Crawl complete — landing page expanded, URL restructure
**Output:** `docs-cache/openclaw-docs/2026-02-07T02-30/`
**Note:** Missed 2026-02-06 crawl (cron gap)

### Pages captured:
| Page | URL | Size | Notes |
|------|-----|------|-------|
| index.md | / | 2.0 KB | Main docs landing page (expanded) |
| getting-started.md | /start/getting-started | 1.6 KB | Quickstart guide (URL changed) |
| help.md | /help | 0.5 KB | Help/troubleshooting links |
| configuration.md | /gateway/configuration | 13.7 KB | Truncated (full page ~99KB) |

**Total:** 17.8 KB across 4 pages

### Diff vs prior (2026-02-05):
**Status:** 🟡 MODERATE CHANGES (content expansion, URL redirect)

#### Key changes:
1. **Landing page expanded** — Added "What is OpenClaw?" section with:
   - Full value proposition (self-hosted gateway for chat apps → AI agents)
   - Target audience: "Developers and power users"
   - 4 key differentiators: Self-hosted, Multi-channel, Agent-native, Open source
   - Requirements line: "Node 22+, an API key (Anthropic recommended), and 5 minutes"
   - Removed `# OpenClaw` H1 heading (page title now from metadata)
2. **URL restructure** — `/start/quickstart` now redirects to `/start/getting-started`
3. **Heading consistency** — `# Help` → `## Help` (minor)
4. **Configuration page** — More content captured (13.7KB vs 1.6KB) — includes:
   - Strict config validation section
   - Schema + UI hints documentation
   - config.apply and config.patch RPC documentation
   - $include directive examples
   - Env var substitution documentation
   - Auth storage and profiles
   - agents.list[].identity configuration
   - logging configuration with redaction
   - WhatsApp dmPolicy and allowFrom examples

**Full diff saved to:** `diff-vs-prior.patch`

### Checksums (MD5):
```
11d20572a95ba4c6f855482ec5661833  index.md
5f5b2aeff14db6a3959419d56b9d6494  getting-started.md
46521dfd9698863e8a14b751eee793d2  help.md
af3d7dfcf90657d5b63505532becff5b  configuration.md
```

## 2026-02-08T02:30 (nightly)

**Site:** OpenClaw Docs (https://docs.openclaw.ai)
**Pages crawled:** 4 (index, getting-started, configuration, help)
**Changes detected:**
- `getting-started.md`: Minor link fix — Pairing link changed from `/start/pairing` → `/channels/pairing`
- `configuration.md`: Significantly more content captured vs prior snapshot (+1569/-225 lines). Prior snapshot was truncated at `channels.whatsapp.sendReadReceipts`; full page now includes 30+ additional sections covering all channel configs (Telegram, Discord, Google Chat, Slack, Mattermost, Signal, iMessage), multi-agent routing, messages, TTS, session config, plugins, browser, gateway, cron, and more.
- `index.md`: No changes
- `help.md`: No changes

## 2026-02-10T02:30 (nightly-docs-crawl)

**Pages crawled:** 4 (index, getting-started, configuration, help)
**Prior snapshot:** 2026-02-08T02-30

### Diffs
- **index.md:** No changes
- **help.md:** No changes
- **getting-started.md:** Content simplified — removed inline CLI examples (install commands, `openclaw onboard`, `openclaw gateway status`, `openclaw dashboard`), environment variable docs expanded (OPENCLAW_HOME, STATE_DIR, CONFIG_PATH), added link to full env var reference
- **configuration.md:** Extraction improvement captured full page (~115K vs prior ~57K truncated). New sections visible at end include **cron configuration** (`sessionRetention`, `maxConcurrentRuns`). Minor formatting: list markers changed from `- item` to bare text in some places.

### Notes
- Switched configuration.md extraction from readability (truncated at 50K) to cleaned HTML extraction for full coverage
- No snapshot on 2026-02-09 (gap)
