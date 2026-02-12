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
When validation fails:

- The Gateway does not boot.

- Only diagnostic commands are allowed (for example: openclaw doctor, openclaw logs, openclaw health, openclaw status, openclaw service, openclaw help).

- Run openclaw doctor to see the exact issues.

- Run openclaw doctor --fix (or --yes) to apply migrations/repairs.

Doctor never writes changes unless you explicitly opt into --fix/--yes.

## Schema + UI hints

The Gateway exposes a JSON Schema representation of the config via config.schema for UI editors.
The Control UI renders a form from this schema, with a Raw JSON editor as an escape hatch.
Channel plugins and extensions can register schema + UI hints for their config, so channel settings
stay schema-driven across apps without hard-coded forms.
Hints (labels, grouping, sensitive fields) ship alongside the schema so clients can render
better forms without hard-coding config knowledge.

## Apply + restart (RPC)

Use config.apply to validate + write the full config and restart the Gateway in one step.
It writes a restart sentinel and pings the last active session after the Gateway comes back.
Warning: config.apply replaces the entire config. If you want to change only a few keys,
use config.patch or openclaw config set. Keep a backup of ~/.openclaw/openclaw.json.
Params:

- raw (string) — JSON5 payload for the entire config

- baseHash (optional) — config hash from config.get (required when a config already exists)

- sessionKey (optional) — last active session key for the wake-up ping

- note (optional) — note to include in the restart sentinel

- restartDelayMs (optional) — delay before restart (default 2000)

Example (via gateway call):
openclaw gateway call config.get --params '{}'
openclaw gateway call config.apply --params '{
 "raw": "{\\n agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
 "baseHash": "<hash-from-config.get>",
 "sessionKey": "agent:main:whatsapp:dm:+15555550123",
 "restartDelayMs": 1000
}'

## Partial updates (RPC)

Use config.patch to merge a partial update into the existing config without clobbering
unrelated keys. It applies JSON merge patch semantics:

- objects merge recursively

- null deletes a key

- arrays replace
Like config.apply, it validates, writes the config, stores a restart sentinel, and schedules
the Gateway restart (with an optional wake when sessionKey is provided).

Params:

- raw (string) — JSON5 payload containing just the keys to change

- baseHash (required) — config hash from config.get

- sessionKey (optional) — last active session key for the wake-up ping

- note (optional) — note to include in the restart sentinel

- restartDelayMs (optional) — delay before restart (default 2000)

Example:
openclaw gateway call config.get --params '{}'
openclaw gateway call config.patch --params '{
 "raw": "{\\n channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
 "baseHash": "<hash-from-config.get>",
 "sessionKey": "agent:main:whatsapp:dm:+15555550123",
 "restartDelayMs": 1000
}'

## Minimal config (recommended starting point)

{
 agents: { defaults: { workspace: "~/.openclaw/workspace" } },
 channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}

Build the default image once with:
scripts/sandbox-setup.sh

## Self-chat mode (recommended for group control)

To prevent the bot from responding to WhatsApp @-mentions in groups (only respond to specific text triggers):
{
 agents: {
 defaults: { workspace: "~/.openclaw/workspace" },
 list: [
 {
 id: "main",
 groupChat: { mentionPatterns: ["@openclaw", "reisponde"] },
 },
 ],
 },
 channels: {
 whatsapp: {
 allowFrom: ["+15555550123"],
 groups: { "*": { requireMention: true } },
 },
 },
}

## Config Includes ($include)

Split your config into multiple files using the $include directive. This is useful for:

- Organizing large configs (e.g., per-client agent definitions)

- Sharing common settings across environments

- Keeping sensitive configs separate

### Basic usage

// ~/.openclaw/openclaw.json
{
 gateway: { port: 18789 },

 // Include a single file (replaces the key's value)
 agents: { $include: "./agents.json5" },

 // Include multiple files (deep-merged in order)
 broadcast: {
 $include: ["./clients/mueller.json5", "./clients/schmidt.json5"],
 },
}

// ~/.openclaw/agents.json5
{
 defaults: { sandbox: { mode: "all", scope: "session" } },
 list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}

### Merge behavior

- Single file: Replaces the object containing $include

- Array of files: Deep-merges files in order (later files override earlier ones)

- With sibling keys: Sibling keys are merged after includes (override included values)

- Sibling keys + arrays/primitives: Not supported (included content must be an object)

// Sibling keys override included values
{
 $include: "./base.json5", // { a: 1, b: 2 }
 b: 99, // Result: { a: 1, b: 99 }
}

### Nested includes

Included files can themselves contain $include directives (up to 10 levels deep):
// clients/mueller.json5
{
 agents: { $include: "./mueller/agents.json5" },
 broadcast: { $include: "./mueller/broadcast.json5" },
}

### Path resolution

- Relative paths: Resolved relative to the including file

- Absolute paths: Used as-is

- Parent directories: ../ references work as expected

{ "$include": "./sub/config.json5" }
{ "$include": "/etc/openclaw/base.json5" }
{ "$include": "../shared/common.json5" }

### Error handling

- Missing file: Clear error with resolved path

- Parse error: Shows which included file failed

- Circular includes: Detected and reported with include chain

### Example: Multi-client legal setup

// ~/.openclaw/openclaw.json
{
 gateway: { port: 18789, auth: { token: "secret" } },

 // Common agent defaults
 agents: {
 defaults: {
 sandbox: { mode: "all", scope: "session" },
 },
 // Merge agent lists from all clients
 list: { $include: ["./clients/mueller/agents.json5", "./clients/schmidt/agents.json5"] },
 },

 // Merge broadcast configs
 broadcast: {
 $include: ["./clients/mueller/broadcast.json5", "./clients/schmidt/broadcast.json5"],
 },

 channels: { whatsapp: { groupPolicy: "allowlist" } },
}

// ~/.openclaw/clients/mueller/agents.json5
[
 { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
 { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]

// ~/.openclaw/clients/mueller/broadcast.json5
{
 "[[email protected]]": ["mueller-transcribe", "mueller-docs"],
}

## Common options

### Env vars + .env

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.).
Additionally, it loads:

- .env from the current working directory (if present)

- a global fallback .env from ~/.openclaw/.env (aka $OPENCLAW_STATE_DIR/.env)

Neither .env file overrides existing env vars.
You can also provide inline env vars in config. These are only applied if the
process env is missing the key (same non-overriding rule):
{
 env: {
 OPENROUTER_API_KEY: "sk-or-...",
 vars: {
 GROQ_API_KEY: "gsk-...",
 },
 },
}

See [/environment](/environment) for full precedence and sources.

### env.shellEnv (optional)

Opt-in convenience: if enabled and none of the expected keys are set yet, OpenClaw runs your login shell and imports only the missing expected keys (never overrides).
This effectively sources your shell profile.
{
 env: {
 shellEnv: {
 enabled: true,
 timeoutMs: 15000,
 },
 },
}

Env var equivalent:

- OPENCLAW_LOAD_SHELL_ENV=1

- OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000

### Env var substitution in config

You can reference environment variables directly in any config string value using
${VAR_NAME} syntax. Variables are substituted at config load time, before validation.
{
 models: {
 providers: {
 "vercel-gateway": {
 apiKey: "${VERCEL_GATEWAY_API_KEY}",
 },
 },
 },
 gateway: {
 auth: {
 token: "${OPENCLAW_GATEWAY_TOKEN}",
 },
 },
}

Rules:

- Only uppercase env var names are matched: [A-Z_][A-Z0-9_]*

- Missing or empty env vars throw an error at config load

- Escape with $${VAR} to output a literal ${VAR}

- Works with $include (included files also get substitution)

Inline substitution:
{
 models: {
 providers: {
 custom: {
 baseUrl: "${CUSTOM_API_BASE}/v1",
 },
 },
 },
}

### Auth storage (OAuth + API keys)

OpenClaw stores per-agent auth profiles (OAuth + API keys) in:

- /auth-profiles.json (default: ~/.openclaw/agents//agent/auth-profiles.json)

See also: [/concepts/oauth](/concepts/oauth)
Legacy OAuth imports:

- ~/.openclaw/credentials/oauth.json (or $OPENCLAW_STATE_DIR/credentials/oauth.json)

The embedded Pi agent maintains a runtime cache at:

- /auth.json (managed automatically; don't edit manually)

Legacy agent dir (pre multi-agent):

- ~/.openclaw/agent/* (migrated by openclaw doctor into ~/.openclaw/agents//agent/*)

Overrides:

- OAuth dir (legacy import only): OPENCLAW_OAUTH_DIR

- Agent dir (default agent root override): OPENCLAW_AGENT_DIR (preferred), PI_CODING_AGENT_DIR (legacy)

On first use, OpenClaw imports oauth.json entries into auth-profiles.json.

### auth

Optional metadata for auth profiles. This does not store secrets; it maps
profile IDs to a provider + mode (and optional email) and defines the provider
rotation order used for failover.
{
 auth: {
 profiles: {
 "anthropic:[email protected]": { provider: "anthropic", mode: "oauth", email: "[email protected]" },
 "anthropic:work": { provider: "anthropic", mode: "api_key" },
 },
 order: {
 anthropic: ["anthropic:[email protected]", "anthropic:work"],
 },
 },
}

### agents.list[].identity

Optional per-agent identity used for defaults and UX. This is written by the macOS onboarding assistant.
If set, OpenClaw derives defaults (only when you haven't set them explicitly):

- messages.ackReaction from the active agent's identity.emoji (falls back to 👀)

- agents.list[].groupChat.mentionPatterns from the agent's identity.name/identity.emoji (so "@Samantha" works in groups across Telegram/Slack/Discord/Google Chat/iMessage/WhatsApp)

- identity.avatar accepts a workspace-relative image path or a remote URL/data URL. Local files must live inside the agent workspace.

identity.avatar accepts:

- Workspace-relative path (must stay within the agent workspace)

- http(s) URL

- data: URI

{
 agents: {
 list: [
 {
 id: "main",
 identity: {
 name: "Samantha",
 theme: "helpful sloth",
 emoji: "🦥",
 avatar: "avatars/samantha.png",
 },
 },
 ],
 },
}

### wizard

Metadata written by CLI wizards (onboard, configure, doctor).
{
 wizard: {
 lastRunAt: "2026-01-01T00:00:00.000Z",
 lastRunVersion: "2026.1.4",
 lastRunCommit: "abc1234",
 lastRunCommand: "configure",
 lastRunMode: "local",
 },
}

### logging

- Default log file: /tmp/openclaw/openclaw-YYYY-MM-DD.log

- If you want a stable path, set logging.file to /tmp/openclaw/openclaw.log.

- Console output can be tuned separately via:

logging.consoleLevel (defaults to info, bumps to debug when --verbose)

- logging.consoleStyle (pretty | compact | json)

- Tool summaries can be redacted to avoid leaking secrets:

logging.redactSensitive (off | tools, default: tools)

- logging.redactPatterns (array of regex strings; overrides defaults)

{
 logging: {
 level: "info",
 file: "/tmp/openclaw/openclaw.log",
 consoleLevel: "info",
 consoleStyle: "pretty",
 redactSensitive: "tools",
 redactPatterns: [
 "\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1",
 "/\\bsk-[A-Za-z0-9_-]{8,}\\b/gi",
 ],
 },
}

### channels.whatsapp.dmPolicy

Controls how WhatsApp direct chats (DMs) are handled:

- "pairing" (default): unknown senders get a pairing code; owner must approve

- "allowlist": only allow senders in channels.whatsapp.allowFrom (or paired allow store)

- "open": allow all inbound DMs (requires channels.whatsapp.allowFrom to include "*")

- "disabled": ignore all inbound DMs

Pairing codes expire after 1 hour; the bot only sends a pairing code when a new request is created. Pending DM pairing requests are capped at 3 per channel by default.
Pairing approvals:

- openclaw pairing list whatsapp

- openclaw pairing approve whatsapp

### channels.whatsapp.allowFrom

Allowlist of E.164 phone numbers that may trigger WhatsApp auto-replies (DMs only).
If empty and channels.whatsapp.dmPolicy="pairing", unknown senders will receive a pairing code.
For groups, use channels.whatsapp.groupPolicy + channels.whatsapp.groupAllowFrom.
{
 channels: {
 whatsapp: {
 dmPolicy: "pairing",
 allowFrom: ["+15555550123", "+447700900123"],
 textChunkLimit: 4000,
 chunkMode: "length",
 mediaMaxMb: 50,
 },
 },
}

### channels.whatsapp.sendReadReceipts

(truncated - full page ~99KB)
