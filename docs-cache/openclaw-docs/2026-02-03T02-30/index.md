# OpenClaw Docs - Index
Fetched: 2026-02-03T07:30:15Z

"EXFOLIATE! EXFOLIATE!" — A space lobster, probably

Any OS + WhatsApp/Telegram/Discord/iMessage gateway for AI agents (Pi).

Plugins add Mattermost and more.
Send a message, get an agent response — from your pocket.

[GitHub](https://github.com/openclaw/openclaw) ·
[Releases](https://github.com/openclaw/openclaw/releases) ·
[Docs](/) ·
[OpenClaw assistant setup](/start/openclaw)

OpenClaw bridges WhatsApp (via WhatsApp Web / Baileys), Telegram (Bot API / grammY), Discord (Bot API / channels.discord.js), and iMessage (imsg CLI) to coding agents like [Pi](https://github.com/badlogic/pi-mono). Plugins add Mattermost (Bot API + WebSocket) and more.
OpenClaw also powers the OpenClaw assistant.

## Start here

- New install from zero: [Getting Started](/start/getting-started)
- Guided setup (recommended): [Wizard](/start/wizard) (openclaw onboard)
- Open the dashboard (local Gateway): [http://127.0.0.1:18789/](http://127.0.0.1:18789/)

## Dashboard (browser Control UI)

The dashboard is the browser Control UI for chat, config, nodes, sessions, and more.
Local default: [http://127.0.0.1:18789/](http://127.0.0.1:18789/)
Remote access: [Web surfaces](/web) and [Tailscale](/gateway/tailscale)

## How it works

WhatsApp / Telegram / Discord / iMessage (+ plugins)
 │
 ▼
┌───────────────────────────┐
│     Gateway               │ ws://127.0.0.1:18789 (loopback-only)
│   (single source)         │
│                           │ http://<gateway-host>:18793
│                           │ /__openclaw__/canvas/ (Canvas host)
└───────────┬───────────────┘
            │
            ├─ Pi agent (RPC)
            ├─ CLI (openclaw …)
            ├─ Chat UI (SwiftUI)
            ├─ macOS app (OpenClaw.app)
            ├─ iOS node via Gateway WS + pairing
            └─ Android node via Gateway WS + pairing

## Network model

- One Gateway per host (recommended)
- Loopback-first: Gateway WS defaults to ws://127.0.0.1:18789
- For Tailnet access, run openclaw gateway --bind tailnet --token ...
- Nodes: connect to the Gateway WebSocket
- Canvas host: HTTP file server on canvasHost.port (default 18793)
- Remote use: SSH tunnel or tailnet/VPN

## Features (high level)

- 📱 WhatsApp Integration — Uses Baileys for WhatsApp Web protocol
- ✈️ Telegram Bot — DMs + groups via grammY
- 🎮 Discord Bot — DMs + guild channels via channels.discord.js
- 🧩 Mattermost Bot (plugin) — Bot token + WebSocket events
- 💬 iMessage — Local imsg CLI integration (macOS)
- 🤖 Agent bridge — Pi (RPC mode) with tool streaming
- ⏱️ Streaming + chunking — Block streaming + Telegram draft streaming
- 🧠 Multi-agent routing — Route provider accounts/peers to isolated agents
- 🔐 Subscription auth — Anthropic + OpenAI via OAuth
- 💬 Sessions — Direct chats collapse into shared main; groups isolated
- 👥 Group Chat Support — Mention-based by default
- 📎 Media Support — Send and receive images, audio, documents
- 🎤 Voice notes — Optional transcription hook
- 🖥️ WebChat + macOS app — Local UI + menu bar companion
- 📱 iOS node — Pairs as a node and exposes a Canvas surface
- 📱 Android node — Pairs as a node and exposes Canvas + Chat + Camera

## Quick start

Runtime requirement: Node ≥ 22.

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
openclaw channels login
openclaw gateway --port 18789
```

## The name

OpenClaw = CLAW + TARDIS — because every space lobster needs a time-and-space machine.

## Credits

- Peter Steinberger (@steipete) — Creator
- Mario Zechner (@badlogicc) — Pi creator
- Clawd — The space lobster

## License

MIT — Free as a lobster in the ocean 🦞
