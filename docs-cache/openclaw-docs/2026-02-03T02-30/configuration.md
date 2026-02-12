# Configuration - OpenClaw Docs
Fetched: 2026-02-03T07:30:34Z
Note: Truncated at 50KB - full page larger

OpenClaw reads an optional JSON5 config from ~/.openclaw/openclaw.json.

If the file is missing, OpenClaw uses safe-ish defaults (embedded Pi agent + per-sender sessions + workspace ~/.openclaw/workspace).

## Strict config validation

OpenClaw only accepts configurations that fully match the schema. Unknown keys, malformed types, or invalid values cause the Gateway to refuse to start.

When validation fails:
- The Gateway does not boot
- Run `openclaw doctor` to see the exact issues
- Run `openclaw doctor --fix` to apply migrations/repairs

## Schema + UI hints

The Gateway exposes a JSON Schema representation of the config via config.schema for UI editors.

## Apply + restart (RPC)

Use config.apply to validate + write the full config and restart the Gateway in one step.

## Partial updates (RPC)

Use config.patch to merge a partial update into the existing config.

## Minimal config (recommended starting point)

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

## Config Includes ($include)

Split your config into multiple files using the $include directive.

## Common options

### Env vars + .env

OpenClaw reads env vars from the parent process and loads .env files.

### Auth storage (OAuth + API keys)

OpenClaw stores per-agent auth profiles in:
- <agentDir>/auth-profiles.json

### agents.list[].identity

Optional per-agent identity used for defaults and UX.

### logging

- Default log file: /tmp/openclaw/openclaw-YYYY-MM-DD.log

### channels.whatsapp.dmPolicy

Controls how WhatsApp direct chats (DMs) are handled:
- "pairing" (default)
- "allowlist"
- "open"
- "disabled"

### channels.whatsapp.allowFrom

Allowlist of E.164 phone numbers that may trigger WhatsApp auto-replies.

### Multi-account support

Run multiple accounts per channel (WhatsApp, Telegram, Discord, Slack, etc.)

### Group chat mention gating

Group messages default to require mention.

### Group policy (per channel)

Use channels.*.groupPolicy to control whether group/room messages are accepted.

### Multi-agent routing

Run multiple isolated agents inside one Gateway.

### messages.queue

Controls how inbound messages behave when an agent run is already active.

### messages.inbound

Debounce rapid inbound messages from the same sender.

### commands (chat command handling)

Controls how chat commands are enabled across connectors.

### messages.tts

Enable text-to-speech for outbound replies.

### agents.defaults.workspace

Sets the single global workspace directory.

### agents.defaults.skipBootstrap

Disables automatic creation of workspace bootstrap files.

[Content truncated - full configuration reference available at https://docs.openclaw.ai/gateway/configuration]
