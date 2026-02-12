# OpenClaw

"EXFOLIATE! EXFOLIATE!" — A space lobster, probably

Any OS gateway for AI agents across WhatsApp, Telegram, Discord, iMessage, and more.

Send a message, get an agent response from your pocket. Plugins add Mattermost and more.

OpenClaw connects chat apps to coding agents like Pi through a single Gateway process. It powers the OpenClaw assistant and supports local or remote setups.

## How it works

The Gateway is the single source of truth for sessions, routing, and channel connections.

## Key capabilities

## Quick start

1

2

3

Need the full install and dev setup? See [Quick start](/start/quickstart).

## Dashboard

Open the browser Control UI after the Gateway starts.

- Local default: [http://127.0.0.1:18789/](http://127.0.0.1:18789/)

- Remote access: [Web surfaces](/web) and [Tailscale](/gateway/tailscale)

## Configuration (optional)

Config lives at ~/.openclaw/openclaw.json.

- If you do nothing, OpenClaw uses the bundled Pi binary in RPC mode with per-sender sessions.

- If you want to lock it down, start with channels.whatsapp.allowFrom and (for groups) mention rules.

Example:
{
 channels: {
 whatsapp: {
 allowFrom: ["+15555550123"],
 groups: { "*": { requireMention: true } },
 },
 },
 messages: { groupChat: { mentionPatterns: ["@openclaw"] } },
}

## Start here

## Learn more
