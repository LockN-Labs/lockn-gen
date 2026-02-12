# Configuration

OpenClaw reads an optional JSON5 config from ~/.openclaw/openclaw.json (comments + trailing commas allowed).
If the file is missing, OpenClaw uses safe-ish defaults (embedded Pi agent + per-sender sessions + workspace ~/.openclaw/workspace). You usually only need a config to:

- restrict who can trigger the bot (channels.whatsapp.allowFrom, channels.telegram.allowFrom, etc.)
- control group allowlists + mention behavior (channels.whatsapp.groups, channels.telegram.groups, channels.discord.guilds, agents.list[].groupChat)
- customize message prefixes (messages)
- set the agent's workspace (agents.defaults.workspace or agents.list[].workspace)
- tune the embedded agent defaults (agents.defaults) and session behavior (session)
- set per-agent identity (agents.list[].identity)

New to configuration? Check out the [Configuration Examples](/gateway/configuration-examples) guide for complete examples with detailed explanations!

## Strict config validation

OpenClaw only accepts configurations that fully match the schema.
Unknown keys, malformed types, or invalid values cause the Gateway to refuse to start for safety.

## Schema + UI hints

The Gateway exposes a JSON Schema representation of the config via config.schema for UI editors.

## Apply + restart (RPC)

Use config.apply to validate + write the full config and restart the Gateway in one step.

## Partial updates (RPC)

Use config.patch to merge a partial update into the existing config without clobbering unrelated keys.

[... content truncated at ~99KB, full configuration reference continues ...]
