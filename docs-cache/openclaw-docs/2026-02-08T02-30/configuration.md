OpenClaw reads an optional JSON5 config from ~/.openclaw/openclaw.json (comments + trailing commas allowed).
If the file is missing, OpenClaw uses safe-ish defaults (embedded Pi agent + per-sender sessions + workspace ~/.openclaw/workspace). You usually only need a config to:

- restrict who can trigger the bot (channels.whatsapp.allowFrom, channels.telegram.allowFrom, etc.)
- control group allowlists + mention behavior (channels.whatsapp.groups, channels.telegram.groups, channels.discord.guilds, agents.list[].groupChat)
- customize message prefixes (messages)
- set the agent’s workspace (agents.defaults.workspace or agents.list[].workspace)
- tune the embedded agent defaults (agents.defaults) and session behavior (session)
- set per-agent identity (agents.list[].identity)

New to configuration? Check out the Configuration Examples guide for complete examples with detailed explanations!

## ​Strict config validation

OpenClaw only accepts configurations that fully match the schema.
Unknown keys, malformed types, or invalid values cause the Gateway to refuse to start for safety.
When validation fails:

- The Gateway does not boot.
- Only diagnostic commands are allowed (for example: openclaw doctor, openclaw logs, openclaw health, openclaw status, openclaw service, openclaw help).
- Run openclaw doctor to see the exact issues.
- Run openclaw doctor --fix (or --yes) to apply migrations/repairs.

Doctor never writes changes unless you explicitly opt into --fix/--yes.

## ​Schema + UI hints

The Gateway exposes a JSON Schema representation of the config via config.schema for UI editors.
The Control UI renders a form from this schema, with a Raw JSON editor as an escape hatch.
Channel plugins and extensions can register schema + UI hints for their config, so channel settings
stay schema-driven across apps without hard-coded forms.
Hints (labels, grouping, sensitive fields) ship alongside the schema so clients can render
better forms without hard-coding config knowledge.

## ​Apply + restart (RPC)

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
Copy
```
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.apply --params '{
  "raw": "{\\n  agents: { defaults: { workspace: \\"~/.openclaw/workspace\\" } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'

```

## ​Partial updates (RPC)

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
Copy
```
openclaw gateway call config.get --params '{}' # capture payload.hash
openclaw gateway call config.patch --params '{
  "raw": "{\\n  channels: { telegram: { groups: { \\"*\\": { requireMention: false } } } }\\n}\\n",
  "baseHash": "<hash-from-config.get>",
  "sessionKey": "agent:main:whatsapp:dm:+15555550123",
  "restartDelayMs": 1000
}'

```

## ​Minimal config (recommended starting point)

Copy
```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}

```

Build the default image once with:
Copy
```
scripts/sandbox-setup.sh

```

## ​Self-chat mode (recommended for group control)

To prevent the bot from responding to WhatsApp @-mentions in groups (only respond to specific text triggers):
Copy
```
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
      // Allowlist is DMs only; including your own number enables self-chat mode.
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
}

```

## ​Config Includes ($include)

Split your config into multiple files using the $include directive. This is useful for:

- Organizing large configs (e.g., per-client agent definitions)
- Sharing common settings across environments
- Keeping sensitive configs separate

### ​Basic usage

Copy
```
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

```

Copy
```
// ~/.openclaw/agents.json5
{
  defaults: { sandbox: { mode: "all", scope: "session" } },
  list: [{ id: "main", workspace: "~/.openclaw/workspace" }],
}

```

### ​Merge behavior

- Single file: Replaces the object containing $include
- Array of files: Deep-merges files in order (later files override earlier ones)
- With sibling keys: Sibling keys are merged after includes (override included values)
- Sibling keys + arrays/primitives: Not supported (included content must be an object)

Copy
```
// Sibling keys override included values
{
  $include: "./base.json5", // { a: 1, b: 2 }
  b: 99, // Result: { a: 1, b: 99 }
}

```

### ​Nested includes

Included files can themselves contain $include directives (up to 10 levels deep):
Copy
```
// clients/mueller.json5
{
  agents: { $include: "./mueller/agents.json5" },
  broadcast: { $include: "./mueller/broadcast.json5" },
}

```

### ​Path resolution

- Relative paths: Resolved relative to the including file
- Absolute paths: Used as-is
- Parent directories: ../ references work as expected

Copy
```
{ "$include": "./sub/config.json5" }      // relative
{ "$include": "/etc/openclaw/base.json5" } // absolute
{ "$include": "../shared/common.json5" }   // parent dir

```

### ​Error handling

- Missing file: Clear error with resolved path
- Parse error: Shows which included file failed
- Circular includes: Detected and reported with include chain

### ​Example: Multi-client legal setup

Copy
```
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

```

Copy
```
// ~/.openclaw/clients/mueller/agents.json5
[
  { id: "mueller-transcribe", workspace: "~/clients/mueller/transcribe" },
  { id: "mueller-docs", workspace: "~/clients/mueller/docs" },
]

```

Copy
```
// ~/.openclaw/clients/mueller/broadcast.json5
{
  "[email protected]": ["mueller-transcribe", "mueller-docs"],
}

```

## ​Common options

### ​Env vars + .env

OpenClaw reads env vars from the parent process (shell, launchd/systemd, CI, etc.).
Additionally, it loads:

- .env from the current working directory (if present)
- a global fallback .env from ~/.openclaw/.env (aka $OPENCLAW_STATE_DIR/.env)

Neither .env file overrides existing env vars.
You can also provide inline env vars in config. These are only applied if the
process env is missing the key (same non-overriding rule):
Copy
```
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: {
      GROQ_API_KEY: "gsk-...",
    },
  },
}

```

See /environment for full precedence and sources.

### ​env.shellEnv (optional)

Opt-in convenience: if enabled and none of the expected keys are set yet, OpenClaw runs your login shell and imports only the missing expected keys (never overrides).
This effectively sources your shell profile.
Copy
```
{
  env: {
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}

```

Env var equivalent:

- OPENCLAW_LOAD_SHELL_ENV=1
- OPENCLAW_SHELL_ENV_TIMEOUT_MS=15000

### ​Env var substitution in config

You can reference environment variables directly in any config string value using
${VAR_NAME} syntax. Variables are substituted at config load time, before validation.
Copy
```
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

```

Rules:

- Only uppercase env var names are matched: [A-Z_][A-Z0-9_]*
- Missing or empty env vars throw an error at config load
- Escape with $${VAR} to output a literal ${VAR}
- Works with $include (included files also get substitution)

Inline substitution:
Copy
```
{
  models: {
    providers: {
      custom: {
        baseUrl: "${CUSTOM_API_BASE}/v1", // → "https://api.example.com/v1"
      },
    },
  },
}

```

### ​Auth storage (OAuth + API keys)

OpenClaw stores per-agent auth profiles (OAuth + API keys) in:

- <agentDir>/auth-profiles.json (default: ~/.openclaw/agents/<agentId>/agent/auth-profiles.json)

See also: /concepts/oauth
Legacy OAuth imports:

- ~/.openclaw/credentials/oauth.json (or $OPENCLAW_STATE_DIR/credentials/oauth.json)

The embedded Pi agent maintains a runtime cache at:

- <agentDir>/auth.json (managed automatically; don’t edit manually)

Legacy agent dir (pre multi-agent):

- ~/.openclaw/agent/* (migrated by openclaw doctor into ~/.openclaw/agents/<defaultAgentId>/agent/*)

Overrides:

- OAuth dir (legacy import only): OPENCLAW_OAUTH_DIR
- Agent dir (default agent root override): OPENCLAW_AGENT_DIR (preferred), PI_CODING_AGENT_DIR (legacy)

On first use, OpenClaw imports oauth.json entries into auth-profiles.json.

### ​auth

Optional metadata for auth profiles. This does not store secrets; it maps
profile IDs to a provider + mode (and optional email) and defines the provider
rotation order used for failover.
Copy
```
{
  auth: {
    profiles: {
      "anthropic:[email protected]": { provider: "anthropic", mode: "oauth", email: "[email protected]" },
      "anthropic:work": { provider: "anthropic", mode: "api_key" },
    },
    order: {
      anthropic: ["anthropic:[email protected]", "anthropic:work"],
    },
  },
}

```

### ​agents.list[].identity

Optional per-agent identity used for defaults and UX. This is written by the macOS onboarding assistant.
If set, OpenClaw derives defaults (only when you haven’t set them explicitly):

- messages.ackReaction from the active agent’s identity.emoji (falls back to 👀)
- agents.list[].groupChat.mentionPatterns from the agent’s identity.name/identity.emoji (so “@Samantha” works in groups across Telegram/Slack/Discord/Google Chat/iMessage/WhatsApp)
- identity.avatar accepts a workspace-relative image path or a remote URL/data URL. Local files must live inside the agent workspace.

identity.avatar accepts:

- Workspace-relative path (must stay within the agent workspace)
- http(s) URL
- data: URI

Copy
```
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

```

### ​wizard

Metadata written by CLI wizards (onboard, configure, doctor).
Copy
```
{
  wizard: {
    lastRunAt: "2026-01-01T00:00:00.000Z",
    lastRunVersion: "2026.1.4",
    lastRunCommit: "abc1234",
    lastRunCommand: "configure",
    lastRunMode: "local",
  },
}

```

### ​logging

- Default log file: /tmp/openclaw/openclaw-YYYY-MM-DD.log
- If you want a stable path, set logging.file to /tmp/openclaw/openclaw.log.
- Console output can be tuned separately via:

- logging.consoleLevel (defaults to info, bumps to debug when --verbose)
- logging.consoleStyle (pretty | compact | json)

- Tool summaries can be redacted to avoid leaking secrets:

- logging.redactSensitive (off | tools, default: tools)
- logging.redactPatterns (array of regex strings; overrides defaults)

Copy
```
{
  logging: {
    level: "info",
    file: "/tmp/openclaw/openclaw.log",
    consoleLevel: "info",
    consoleStyle: "pretty",
    redactSensitive: "tools",
    redactPatterns: [
      // Example: override defaults with your own rules.
      "\\bTOKEN\\b\\s*[=:]\\s*([\"']?)([^\\s\"']+)\\1",
      "/\\bsk-[A-Za-z0-9_-]{8,}\\b/gi",
    ],
  },
}

```

### ​channels.whatsapp.dmPolicy

Controls how WhatsApp direct chats (DMs) are handled:

- "pairing" (default): unknown senders get a pairing code; owner must approve
- "allowlist": only allow senders in channels.whatsapp.allowFrom (or paired allow store)
- "open": allow all inbound DMs (requires channels.whatsapp.allowFrom to include "*")
- "disabled": ignore all inbound DMs

Pairing codes expire after 1 hour; the bot only sends a pairing code when a new request is created. Pending DM pairing requests are capped at 3 per channel by default.
Pairing approvals:

- openclaw pairing list whatsapp
- openclaw pairing approve whatsapp <code>

### ​channels.whatsapp.allowFrom

Allowlist of E.164 phone numbers that may trigger WhatsApp auto-replies (DMs only).
If empty and channels.whatsapp.dmPolicy="pairing", unknown senders will receive a pairing code.
For groups, use channels.whatsapp.groupPolicy + channels.whatsapp.groupAllowFrom.
Copy
```
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "+447700900123"],
      textChunkLimit: 4000, // optional outbound chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      mediaMaxMb: 50, // optional inbound media cap (MB)
    },
  },
}

```

### ​channels.whatsapp.sendReadReceipts

Controls whether inbound WhatsApp messages are marked as read (blue ticks). Default: true.
Self-chat mode always skips read receipts, even when enabled.
Per-account override: channels.whatsapp.accounts.<id>.sendReadReceipts.
Copy
```
{
  channels: {
    whatsapp: { sendReadReceipts: false },
  },
}

```

### ​channels.whatsapp.accounts (multi-account)

Run multiple WhatsApp accounts in one gateway:
Copy
```
{
  channels: {
    whatsapp: {
      accounts: {
        default: {}, // optional; keeps the default id stable
        personal: {},
        biz: {
          // Optional override. Default: ~/.openclaw/credentials/whatsapp/biz
          // authDir: "~/.openclaw/credentials/whatsapp/biz",
        },
      },
    },
  },
}

```

Notes:

- Outbound commands default to account default if present; otherwise the first configured account id (sorted).
- The legacy single-account Baileys auth dir is migrated by openclaw doctor into whatsapp/default.

### ​channels.telegram.accounts / channels.discord.accounts / channels.googlechat.accounts / channels.slack.accounts / channels.mattermost.accounts / channels.signal.accounts / channels.imessage.accounts

Run multiple accounts per channel (each account has its own accountId and optional name):
Copy
```
{
  channels: {
    telegram: {
      accounts: {
        default: {
          name: "Primary bot",
          botToken: "123456:ABC...",
        },
        alerts: {
          name: "Alerts bot",
          botToken: "987654:XYZ...",
        },
      },
    },
  },
}

```

Notes:

- default is used when accountId is omitted (CLI + routing).
- Env tokens only apply to the default account.
- Base channel settings (group policy, mention gating, etc.) apply to all accounts unless overridden per account.
- Use bindings[].match.accountId to route each account to a different agents.defaults.

### ​Group chat mention gating (agents.list[].groupChat + messages.groupChat)

Group messages default to require mention (either metadata mention or regex patterns). Applies to WhatsApp, Telegram, Discord, Google Chat, and iMessage group chats.
Mention types:

- Metadata mentions: Native platform @-mentions (e.g., WhatsApp tap-to-mention). Ignored in WhatsApp self-chat mode (see channels.whatsapp.allowFrom).
- Text patterns: Regex patterns defined in agents.list[].groupChat.mentionPatterns. Always checked regardless of self-chat mode.
- Mention gating is enforced only when mention detection is possible (native mentions or at least one mentionPattern).

Copy
```
{
  messages: {
    groupChat: { historyLimit: 50 },
  },
  agents: {
    list: [{ id: "main", groupChat: { mentionPatterns: ["@openclaw", "openclaw"] } }],
  },
}

```

messages.groupChat.historyLimit sets the global default for group history context. Channels can override with channels.<channel>.historyLimit (or channels.<channel>.accounts.*.historyLimit for multi-account). Set 0 to disable history wrapping.

#### ​DM history limits

DM conversations use session-based history managed by the agent. You can limit the number of user turns retained per DM session:
Copy
```
{
  channels: {
    telegram: {
      dmHistoryLimit: 30, // limit DM sessions to 30 user turns
      dms: {
        "123456789": { historyLimit: 50 }, // per-user override (user ID)
      },
    },
  },
}

```

Resolution order:

- Per-DM override: channels.<provider>.dms[userId].historyLimit
- Provider default: channels.<provider>.dmHistoryLimit
- No limit (all history retained)

Supported providers: telegram, whatsapp, discord, slack, signal, imessage, msteams.
Per-agent override (takes precedence when set, even []):
Copy
```
{
  agents: {
    list: [
      { id: "work", groupChat: { mentionPatterns: ["@workbot", "\\+15555550123"] } },
      { id: "personal", groupChat: { mentionPatterns: ["@homebot", "\\+15555550999"] } },
    ],
  },
}

```

Mention gating defaults live per channel (channels.whatsapp.groups, channels.telegram.groups, channels.imessage.groups, channels.discord.guilds). When *.groups is set, it also acts as a group allowlist; include "*" to allow all groups.
To respond only to specific text triggers (ignoring native @-mentions):
Copy
```
{
  channels: {
    whatsapp: {
      // Include your own number to enable self-chat mode (ignore native @-mentions).
      allowFrom: ["+15555550123"],
      groups: { "*": { requireMention: true } },
    },
  },
  agents: {
    list: [
      {
        id: "main",
        groupChat: {
          // Only these text patterns will trigger responses
          mentionPatterns: ["reisponde", "@openclaw"],
        },
      },
    ],
  },
}

```

### ​Group policy (per channel)

Use channels.*.groupPolicy to control whether group/room messages are accepted at all:
Copy
```
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    telegram: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["tg:123456789", "@alice"],
    },
    signal: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
    },
    imessage: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["chat_id:123"],
    },
    msteams: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["[email protected]"],
    },
    discord: {
      groupPolicy: "allowlist",
      guilds: {
        GUILD_ID: {
          channels: { help: { allow: true } },
        },
      },
    },
    slack: {
      groupPolicy: "allowlist",
      channels: { "#general": { allow: true } },
    },
  },
}

```

Notes:

- "open": groups bypass allowlists; mention-gating still applies.
- "disabled": block all group/room messages.
- "allowlist": only allow groups/rooms that match the configured allowlist.
- channels.defaults.groupPolicy sets the default when a provider’s groupPolicy is unset.
- WhatsApp/Telegram/Signal/iMessage/Microsoft Teams use groupAllowFrom (fallback: explicit allowFrom).
- Discord/Slack use channel allowlists (channels.discord.guilds.*.channels, channels.slack.channels).
- Group DMs (Discord/Slack) are still controlled by dm.groupEnabled + dm.groupChannels.
- Default is groupPolicy: "allowlist" (unless overridden by channels.defaults.groupPolicy); if no allowlist is configured, group messages are blocked.

### ​Multi-agent routing (agents.list + bindings)

Run multiple isolated agents (separate workspace, agentDir, sessions) inside one Gateway.
Inbound messages are routed to an agent via bindings.

- agents.list[]: per-agent overrides.

- id: stable agent id (required).
- default: optional; when multiple are set, the first wins and a warning is logged.
If none are set, the first entry in the list is the default agent.
- name: display name for the agent.
- workspace: default ~/.openclaw/workspace-<agentId> (for main, falls back to agents.defaults.workspace).
- agentDir: default ~/.openclaw/agents/<agentId>/agent.
- model: per-agent default model, overrides agents.defaults.model for that agent.

- string form: "provider/model", overrides only agents.defaults.model.primary
- object form: { primary, fallbacks } (fallbacks override agents.defaults.model.fallbacks; [] disables global fallbacks for that agent)

- identity: per-agent name/theme/emoji (used for mention patterns + ack reactions).
- groupChat: per-agent mention-gating (mentionPatterns).
- sandbox: per-agent sandbox config (overrides agents.defaults.sandbox).

- mode: "off" | "non-main" | "all"
- workspaceAccess: "none" | "ro" | "rw"
- scope: "session" | "agent" | "shared"
- workspaceRoot: custom sandbox workspace root
- docker: per-agent docker overrides (e.g. image, network, env, setupCommand, limits; ignored when scope: "shared")
- browser: per-agent sandboxed browser overrides (ignored when scope: "shared")
- prune: per-agent sandbox pruning overrides (ignored when scope: "shared")

- subagents: per-agent sub-agent defaults.

- allowAgents: allowlist of agent ids for sessions_spawn from this agent (["*"] = allow any; default: only same agent)

- tools: per-agent tool restrictions (applied before sandbox tool policy).

- profile: base tool profile (applied before allow/deny)
- allow: array of allowed tool names
- deny: array of denied tool names (deny wins)

- agents.defaults: shared agent defaults (model, workspace, sandbox, etc.).
- bindings[]: routes inbound messages to an agentId.

- match.channel (required)
- match.accountId (optional; * = any account; omitted = default account)
- match.peer (optional; { kind: dm|group|channel, id })
- match.guildId / match.teamId (optional; channel-specific)

Deterministic match order:

- match.peer
- match.guildId
- match.teamId
- match.accountId (exact, no peer/guild/team)
- match.accountId: "*" (channel-wide, no peer/guild/team)
- default agent (agents.list[].default, else first list entry, else "main")

Within each match tier, the first matching entry in bindings wins.

#### ​Per-agent access profiles (multi-agent)

Each agent can carry its own sandbox + tool policy. Use this to mix access
levels in one gateway:

- Full access (personal agent)
- Read-only tools + workspace
- No filesystem access (messaging/session tools only)

See Multi-Agent Sandbox & Tools for precedence and
additional examples.
Full access (no sandbox):
Copy
```
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: { mode: "off" },
      },
    ],
  },
}

```

Read-only tools + read-only workspace:
Copy
```
{
  agents: {
    list: [
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: [
            "read",
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
          ],
          deny: ["write", "edit", "apply_patch", "exec", "process", "browser"],
        },
      },
    ],
  },
}

```

No filesystem access (messaging/session tools enabled):
Copy
```
{
  agents: {
    list: [
      {
        id: "public",
        workspace: "~/.openclaw/workspace-public",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "none",
        },
        tools: {
          allow: [
            "sessions_list",
            "sessions_history",
            "sessions_send",
            "sessions_spawn",
            "session_status",
            "whatsapp",
            "telegram",
            "slack",
            "discord",
            "gateway",
          ],
          deny: [
            "read",
            "write",
            "edit",
            "apply_patch",
            "exec",
            "process",
            "browser",
            "canvas",
            "nodes",
            "cron",
            "gateway",
            "image",
          ],
        },
      },
    ],
  },
}

```

Example: two WhatsApp accounts → two agents:
Copy
```
{
  agents: {
    list: [
      { id: "home", default: true, workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}

```

### ​tools.agentToAgent (optional)

Agent-to-agent messaging is opt-in:
Copy
```
{
  tools: {
    agentToAgent: {
      enabled: false,
      allow: ["home", "work"],
    },
  },
}

```

### ​messages.queue

Controls how inbound messages behave when an agent run is already active.
Copy
```
{
  messages: {
    queue: {
      mode: "collect", // steer | followup | collect | steer-backlog (steer+backlog ok) | interrupt (queue=steer legacy)
      debounceMs: 1000,
      cap: 20,
      drop: "summarize", // old | new | summarize
      byChannel: {
        whatsapp: "collect",
        telegram: "collect",
        discord: "collect",
        imessage: "collect",
        webchat: "collect",
      },
    },
  },
}

```

### ​messages.inbound

Debounce rapid inbound messages from the same sender so multiple back-to-back
messages become a single agent turn. Debouncing is scoped per channel + conversation
and uses the most recent message for reply threading/IDs.
Copy
```
{
  messages: {
    inbound: {
      debounceMs: 2000, // 0 disables
      byChannel: {
        whatsapp: 5000,
        slack: 1500,
        discord: 1500,
      },
    },
  },
}

```

Notes:

- Debounce batches text-only messages; media/attachments flush immediately.
- Control commands (e.g. /queue, /new) bypass debouncing so they stay standalone.

### ​commands (chat command handling)

Controls how chat commands are enabled across connectors.
Copy
```
{
  commands: {
    native: "auto", // register native commands when supported (auto)
    text: true, // parse slash commands in chat messages
    bash: false, // allow ! (alias: /bash) (host-only; requires tools.elevated allowlists)
    bashForegroundMs: 2000, // bash foreground window (0 backgrounds immediately)
    config: false, // allow /config (writes to disk)
    debug: false, // allow /debug (runtime-only overrides)
    restart: false, // allow /restart + gateway restart tool
    useAccessGroups: true, // enforce access-group allowlists/policies for commands
  },
}

```

Notes:

- Text commands must be sent as a standalone message and use the leading / (no plain-text aliases).
- commands.text: false disables parsing chat messages for commands.
- commands.native: "auto" (default) turns on native commands for Discord/Telegram and leaves Slack off; unsupported channels stay text-only.
- Set commands.native: true|false to force all, or override per channel with channels.discord.commands.native, channels.telegram.commands.native, channels.slack.commands.native (bool or "auto"). false clears previously registered commands on Discord/Telegram at startup; Slack commands are managed in the Slack app.
- channels.telegram.customCommands adds extra Telegram bot menu entries. Names are normalized; conflicts with native commands are ignored.
- commands.bash: true enables ! <cmd> to run host shell commands (/bash <cmd> also works as an alias). Requires tools.elevated.enabled and allowlisting the sender in tools.elevated.allowFrom.<channel>.
- commands.bashForegroundMs controls how long bash waits before backgrounding. While a bash job is running, new ! <cmd> requests are rejected (one at a time).
- commands.config: true enables /config (reads/writes openclaw.json).
- channels.<provider>.configWrites gates config mutations initiated by that channel (default: true). This applies to /config set|unset plus provider-specific auto-migrations (Telegram supergroup ID changes, Slack channel ID changes).
- commands.debug: true enables /debug (runtime-only overrides).
- commands.restart: true enables /restart and the gateway tool restart action.
- commands.useAccessGroups: false allows commands to bypass access-group allowlists/policies.
- Slash commands and directives are only honored for authorized senders. Authorization is derived from
channel allowlists/pairing plus commands.useAccessGroups.

### ​web (WhatsApp web channel runtime)

WhatsApp runs through the gateway’s web channel (Baileys Web). It starts automatically when a linked session exists.
Set web.enabled: false to keep it off by default.
Copy
```
{
  web: {
    enabled: true,
    heartbeatSeconds: 60,
    reconnect: {
      initialMs: 2000,
      maxMs: 120000,
      factor: 1.4,
      jitter: 0.2,
      maxAttempts: 0,
    },
  },
}

```

### ​channels.telegram (bot transport)

OpenClaw starts Telegram only when a channels.telegram config section exists. The bot token is resolved from channels.telegram.botToken (or channels.telegram.tokenFile), with TELEGRAM_BOT_TOKEN as a fallback for the default account.
Set channels.telegram.enabled: false to disable automatic startup.
Multi-account support lives under channels.telegram.accounts (see the multi-account section above). Env tokens only apply to the default account.
Set channels.telegram.configWrites: false to block Telegram-initiated config writes (including supergroup ID migrations and /config set|unset).
Copy
```
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["tg:123456789"], // optional; "open" requires ["*"]
      groups: {
        "*": { requireMention: true },
        "-1001234567890": {
          allowFrom: ["@admin"],
          systemPrompt: "Keep answers brief.",
          topics: {
            "99": {
              requireMention: false,
              skills: ["search"],
              systemPrompt: "Stay on topic.",
            },
          },
        },
      },
      customCommands: [
        { command: "backup", description: "Git backup" },
        { command: "generate", description: "Create an image" },
      ],
      historyLimit: 50, // include last N group messages as context (0 disables)
      replyToMode: "first", // off | first | all
      linkPreview: true, // toggle outbound link previews
      streamMode: "partial", // off | partial | block (draft streaming; separate from block streaming)
      draftChunk: {
        // optional; only for streamMode=block
        minChars: 200,
        maxChars: 800,
        breakPreference: "paragraph", // paragraph | newline | sentence
      },
      actions: { reactions: true, sendMessage: true }, // tool action gates (false disables)
      reactionNotifications: "own", // off | own | all
      mediaMaxMb: 5,
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
      network: {
        // transport overrides
        autoSelectFamily: false,
      },
      proxy: "socks5://localhost:9050",
      webhookUrl: "https://example.com/telegram-webhook", // requires webhookSecret
      webhookSecret: "secret",
      webhookPath: "/telegram-webhook",
    },
  },
}

```

Draft streaming notes:

- Uses Telegram sendMessageDraft (draft bubble, not a real message).
- Requires private chat topics (message_thread_id in DMs; bot has topics enabled).
- /reasoning stream streams reasoning into the draft, then sends the final answer.
Retry policy defaults and behavior are documented in Retry policy.

### ​channels.discord (bot transport)

Configure the Discord bot by setting the bot token and optional gating:
Multi-account support lives under channels.discord.accounts (see the multi-account section above). Env tokens only apply to the default account.
Copy
```
{
  channels: {
    discord: {
      enabled: true,
      token: "your-bot-token",
      mediaMaxMb: 8, // clamp inbound media size
      allowBots: false, // allow bot-authored messages
      actions: {
        // tool action gates (false disables)
        reactions: true,
        stickers: true,
        polls: true,
        permissions: true,
        messages: true,
        threads: true,
        pins: true,
        search: true,
        memberInfo: true,
        roleInfo: true,
        roles: false,
        channelInfo: true,
        voiceStatus: true,
        events: true,
        moderation: false,
      },
      replyToMode: "off", // off | first | all
      dm: {
        enabled: true, // disable all DMs when false
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["1234567890", "steipete"], // optional DM allowlist ("open" requires ["*"])
        groupEnabled: false, // enable group DMs
        groupChannels: ["openclaw-dm"], // optional group DM allowlist
      },
      guilds: {
        "123456789012345678": {
          // guild id (preferred) or slug
          slug: "friends-of-openclaw",
          requireMention: false, // per-guild default
          reactionNotifications: "own", // off | own | all | allowlist
          users: ["987654321098765432"], // optional per-guild user allowlist
          channels: {
            general: { allow: true },
            help: {
              allow: true,
              requireMention: true,
              users: ["987654321098765432"],
              skills: ["docs"],
              systemPrompt: "Short answers only.",
            },
          },
        },
      },
      historyLimit: 20, // include last N guild messages as context
      textChunkLimit: 2000, // optional outbound text chunk size (chars)
      chunkMode: "length", // optional chunking mode (length | newline)
      maxLinesPerMessage: 17, // soft max lines per message (Discord UI clipping)
      retry: {
        // outbound retry policy
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}

```

OpenClaw starts Discord only when a channels.discord config section exists. The token is resolved from channels.discord.token, with DISCORD_BOT_TOKEN as a fallback for the default account (unless channels.discord.enabled is false). Use user:<id> (DM) or channel:<id> (guild channel) when specifying delivery targets for cron/CLI commands; bare numeric IDs are ambiguous and rejected.
Guild slugs are lowercase with spaces replaced by -; channel keys use the slugged channel name (no leading #). Prefer guild ids as keys to avoid rename ambiguity.
Bot-authored messages are ignored by default. Enable with channels.discord.allowBots (own messages are still filtered to prevent self-reply loops).
Reaction notification modes:

- off: no reaction events.
- own: reactions on the bot’s own messages (default).
- all: all reactions on all messages.
- allowlist: reactions from guilds.<id>.users on all messages (empty list disables).
Outbound text is chunked by channels.discord.textChunkLimit (default 2000). Set channels.discord.chunkMode="newline" to split on blank lines (paragraph boundaries) before length chunking. Discord clients can clip very tall messages, so channels.discord.maxLinesPerMessage (default 17) splits long multi-line replies even when under 2000 chars.
Retry policy defaults and behavior are documented in Retry policy.

### ​channels.googlechat (Chat API webhook)

Google Chat runs over HTTP webhooks with app-level auth (service account).
Multi-account support lives under channels.googlechat.accounts (see the multi-account section above). Env vars only apply to the default account.
Copy
```
{
  channels: {
    googlechat: {
      enabled: true,
      serviceAccountFile: "/path/to/service-account.json",
      audienceType: "app-url", // app-url | project-number
      audience: "https://gateway.example.com/googlechat",
      webhookPath: "/googlechat",
      botUser: "users/1234567890", // optional; improves mention detection
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["users/1234567890"], // optional; "open" requires ["*"]
      },
      groupPolicy: "allowlist",
      groups: {
        "spaces/AAAA": { allow: true, requireMention: true },
      },
      actions: { reactions: true },
      typingIndicator: "message",
      mediaMaxMb: 20,
    },
  },
}

```

Notes:

- Service account JSON can be inline (serviceAccount) or file-based (serviceAccountFile).
- Env fallbacks for the default account: GOOGLE_CHAT_SERVICE_ACCOUNT or GOOGLE_CHAT_SERVICE_ACCOUNT_FILE.
- audienceType + audience must match the Chat app’s webhook auth config.
- Use spaces/<spaceId> or users/<userId|email> when setting delivery targets.

### ​channels.slack (socket mode)

Slack runs in Socket Mode and requires both a bot token and app token:
Copy
```
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
      dm: {
        enabled: true,
        policy: "pairing", // pairing | allowlist | open | disabled
        allowFrom: ["U123", "U456", "*"], // optional; "open" requires ["*"]
        groupEnabled: false,
        groupChannels: ["G123"],
      },
      channels: {
        C123: { allow: true, requireMention: true, allowBots: false },
        "#general": {
          allow: true,
          requireMention: true,
          allowBots: false,
          users: ["U123"],
          skills: ["docs"],
          systemPrompt: "Short answers only.",
        },
      },
      historyLimit: 50, // include last N channel/group messages as context (0 disables)
      allowBots: false,
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["U123"],
      replyToMode: "off", // off | first | all
      thread: {
        historyScope: "thread", // thread | channel
        inheritParent: false,
      },
      actions: {
        reactions: true,
        messages: true,
        pins: true,
        memberInfo: true,
        emojiList: true,
      },
      slashCommand: {
        enabled: true,
        name: "openclaw",
        sessionPrefix: "slack:slash",
        ephemeral: true,
      },
      textChunkLimit: 4000,
      chunkMode: "length",
      mediaMaxMb: 20,
    },
  },
}

```

Multi-account support lives under channels.slack.accounts (see the multi-account section above). Env tokens only apply to the default account.
OpenClaw starts Slack when the provider is enabled and both tokens are set (via config or SLACK_BOT_TOKEN + SLACK_APP_TOKEN). Use user:<id> (DM) or channel:<id> when specifying delivery targets for cron/CLI commands.
Set channels.slack.configWrites: false to block Slack-initiated config writes (including channel ID migrations and /config set|unset).
Bot-authored messages are ignored by default. Enable with channels.slack.allowBots or channels.slack.channels.<id>.allowBots.
Reaction notification modes:

- off: no reaction events.
- own: reactions on the bot’s own messages (default).
- all: all reactions on all messages.
- allowlist: reactions from channels.slack.reactionAllowlist on all messages (empty list disables).

Thread session isolation:

- channels.slack.thread.historyScope controls whether thread history is per-thread (thread, default) or shared across the channel (channel).
- channels.slack.thread.inheritParent controls whether new thread sessions inherit the parent channel transcript (default: false).

Slack action groups (gate slack tool actions):
Action groupDefaultNotesreactionsenabledReact + list reactionsmessagesenabledRead/send/edit/deletepinsenabledPin/unpin/listmemberInfoenabledMember infoemojiListenabledCustom emoji list

### ​channels.mattermost (bot token)

Mattermost ships as a plugin and is not bundled with the core install.
Install it first: openclaw plugins install @openclaw/mattermost (or ./extensions/mattermost from a git checkout).
Mattermost requires a bot token plus the base URL for your server:
Copy
```
{
  channels: {
    mattermost: {
      enabled: true,
      botToken: "mm-token",
      baseUrl: "https://chat.example.com",
      dmPolicy: "pairing",
      chatmode: "oncall", // oncall | onmessage | onchar
      oncharPrefixes: [">", "!"],
      textChunkLimit: 4000,
      chunkMode: "length",
    },
  },
}

```

OpenClaw starts Mattermost when the account is configured (bot token + base URL) and enabled. The token + base URL are resolved from channels.mattermost.botToken + channels.mattermost.baseUrl or MATTERMOST_BOT_TOKEN + MATTERMOST_URL for the default account (unless channels.mattermost.enabled is false).
Chat modes:

- oncall (default): respond to channel messages only when @mentioned.
- onmessage: respond to every channel message.
- onchar: respond when a message starts with a trigger prefix (channels.mattermost.oncharPrefixes, default [">", "!"]).

Access control:

- Default DMs: channels.mattermost.dmPolicy="pairing" (unknown senders get a pairing code).
- Public DMs: channels.mattermost.dmPolicy="open" plus channels.mattermost.allowFrom=["*"].
- Groups: channels.mattermost.groupPolicy="allowlist" by default (mention-gated). Use channels.mattermost.groupAllowFrom to restrict senders.

Multi-account support lives under channels.mattermost.accounts (see the multi-account section above). Env vars only apply to the default account.
Use channel:<id> or user:<id> (or @username) when specifying delivery targets; bare ids are treated as channel ids.

### ​channels.signal (signal-cli)

Signal reactions can emit system events (shared reaction tooling):
Copy
```
{
  channels: {
    signal: {
      reactionNotifications: "own", // off | own | all | allowlist
      reactionAllowlist: ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
      historyLimit: 50, // include last N group messages as context (0 disables)
    },
  },
}

```

Reaction notification modes:

- off: no reaction events.
- own: reactions on the bot’s own messages (default).
- all: all reactions on all messages.
- allowlist: reactions from channels.signal.reactionAllowlist on all messages (empty list disables).

### ​channels.imessage (imsg CLI)

OpenClaw spawns imsg rpc (JSON-RPC over stdio). No daemon or port required.
Copy
```
{
  channels: {
    imessage: {
      enabled: true,
      cliPath: "imsg",
      dbPath: "~/Library/Messages/chat.db",
      remoteHost: "user@gateway-host", // SCP for remote attachments when using SSH wrapper
      dmPolicy: "pairing", // pairing | allowlist | open | disabled
      allowFrom: ["+15555550123", "[email protected]", "chat_id:123"],
      historyLimit: 50, // include last N group messages as context (0 disables)
      includeAttachments: false,
      mediaMaxMb: 16,
      service: "auto",
      region: "US",
    },
  },
}

```

Multi-account support lives under channels.imessage.accounts (see the multi-account section above).
Notes:

- Requires Full Disk Access to the Messages DB.
- The first send will prompt for Messages automation permission.
- Prefer chat_id:<id> targets. Use imsg chats --limit 20 to list chats.
- channels.imessage.cliPath can point to a wrapper script (e.g. ssh to another Mac that runs imsg rpc); use SSH keys to avoid password prompts.
- For remote SSH wrappers, set channels.imessage.remoteHost to fetch attachments via SCP when includeAttachments is enabled.

Example wrapper:
Copy
```
#!/usr/bin/env bash
exec ssh -T gateway-host imsg "$@"

```

### ​agents.defaults.workspace

Sets the single global workspace directory used by the agent for file operations.
Default: ~/.openclaw/workspace.
Copy
```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}

```

If agents.defaults.sandbox is enabled, non-main sessions can override this with their
own per-scope workspaces under agents.defaults.sandbox.workspaceRoot.

### ​agents.defaults.repoRoot

Optional repository root to show in the system prompt’s Runtime line. If unset, OpenClaw
tries to detect a .git directory by walking upward from the workspace (and current
working directory). The path must exist to be used.
Copy
```
{
  agents: { defaults: { repoRoot: "~/Projects/openclaw" } },
}

```

### ​agents.defaults.skipBootstrap

Disables automatic creation of the workspace bootstrap files (AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, and BOOTSTRAP.md).
Use this for pre-seeded deployments where your workspace files come from a repo.
Copy
```
{
  agents: { defaults: { skipBootstrap: true } },
}

```

### ​agents.defaults.bootstrapMaxChars

Max characters of each workspace bootstrap file injected into the system prompt
before truncation. Default: 20000.
When a file exceeds this limit, OpenClaw logs a warning and injects a truncated
head/tail with a marker.
Copy
```
{
  agents: { defaults: { bootstrapMaxChars: 20000 } },
}

```

### ​agents.defaults.userTimezone

Sets the user’s timezone for system prompt context (not for timestamps in
message envelopes). If unset, OpenClaw uses the host timezone at runtime.
Copy
```
{
  agents: { defaults: { userTimezone: "America/Chicago" } },
}

```

### ​agents.defaults.timeFormat

Controls the time format shown in the system prompt’s Current Date & Time section.
Default: auto (OS preference).
Copy
```
{
  agents: { defaults: { timeFormat: "auto" } }, // auto | 12 | 24
}

```

### ​messages

Controls inbound/outbound prefixes and optional ack reactions.
See Messages for queueing, sessions, and streaming context.
Copy
```
{
  messages: {
    responsePrefix: "🦞", // or "auto"
    ackReaction: "👀",
    ackReactionScope: "group-mentions",
    removeAckAfterReply: false,
  },
}

```

responsePrefix is applied to all outbound replies (tool summaries, block
streaming, final replies) across channels unless already present.
Overrides can be configured per channel and per account:

- channels.<channel>.responsePrefix
- channels.<channel>.accounts.<id>.responsePrefix

Resolution order (most specific wins):

- channels.<channel>.accounts.<id>.responsePrefix
- channels.<channel>.responsePrefix
- messages.responsePrefix

Semantics:

- undefined falls through to the next level.
- "" explicitly disables the prefix and stops the cascade.
- "auto" derives [{identity.name}] for the routed agent.

Overrides apply to all channels, including extensions, and to every outbound reply kind.
If messages.responsePrefix is unset, no prefix is applied by default. WhatsApp self-chat
replies are the exception: they default to [{identity.name}] when set, otherwise
[openclaw], so same-phone conversations stay legible.
Set it to "auto" to derive [{identity.name}] for the routed agent (when set).

#### ​Template variables

The responsePrefix string can include template variables that resolve dynamically:
VariableDescriptionExample{model}Short model nameclaude-opus-4-6, gpt-4o{modelFull}Full model identifieranthropic/claude-opus-4-6{provider}Provider nameanthropic, openai{thinkingLevel}Current thinking levelhigh, low, off{identity.name}Agent identity name(same as "auto" mode)
Variables are case-insensitive ({MODEL} = {model}). {think} is an alias for {thinkingLevel}.
Unresolved variables remain as literal text.
Copy
```
{
  messages: {
    responsePrefix: "[{model} | think:{thinkingLevel}]",
  },
}

```

Example output: [claude-opus-4-6 | think:high] Here's my response...
WhatsApp inbound prefix is configured via channels.whatsapp.messagePrefix (deprecated:
messages.messagePrefix). Default stays unchanged: "[openclaw]" when
channels.whatsapp.allowFrom is empty, otherwise "" (no prefix). When using
"[openclaw]", OpenClaw will instead use [{identity.name}] when the routed
agent has identity.name set.
ackReaction sends a best-effort emoji reaction to acknowledge inbound messages
on channels that support reactions (Slack/Discord/Telegram/Google Chat). Defaults to the
active agent’s identity.emoji when set, otherwise "👀". Set it to "" to disable.
ackReactionScope controls when reactions fire:

- group-mentions (default): only when a group/room requires mentions and the bot was mentioned
- group-all: all group/room messages
- direct: direct messages only
- all: all messages

removeAckAfterReply removes the bot’s ack reaction after a reply is sent
(Slack/Discord/Telegram/Google Chat only). Default: false.

#### ​messages.tts

Enable text-to-speech for outbound replies. When on, OpenClaw generates audio
using ElevenLabs or OpenAI and attaches it to responses. Telegram uses Opus
voice notes; other channels send MP3 audio.
Copy
```
{
  messages: {
    tts: {
      auto: "always", // off | always | inbound | tagged
      mode: "final", // final | all (include tool/block replies)
      provider: "elevenlabs",
      summaryModel: "openai/gpt-4.1-mini",
      modelOverrides: {
        enabled: true,
      },
      maxTextLength: 4000,
      timeoutMs: 30000,
      prefsPath: "~/.openclaw/settings/tts.json",
      elevenlabs: {
        apiKey: "elevenlabs_api_key",
        baseUrl: "https://api.elevenlabs.io",
        voiceId: "voice_id",
        modelId: "eleven_multilingual_v2",
        seed: 42,
        applyTextNormalization: "auto",
        languageCode: "en",
        voiceSettings: {
          stability: 0.5,
          similarityBoost: 0.75,
          style: 0.0,
          useSpeakerBoost: true,
          speed: 1.0,
        },
      },
      openai: {
        apiKey: "openai_api_key",
        model: "gpt-4o-mini-tts",
        voice: "alloy",
      },
    },
  },
}

```

Notes:

- messages.tts.auto controls auto‑TTS (off, always, inbound, tagged).
- /tts off|always|inbound|tagged sets the per‑session auto mode (overrides config).
- messages.tts.enabled is legacy; doctor migrates it to messages.tts.auto.
- prefsPath stores local overrides (provider/limit/summarize).
- maxTextLength is a hard cap for TTS input; summaries are truncated to fit.
- summaryModel overrides agents.defaults.model.primary for auto-summary.

- Accepts provider/model or an alias from agents.defaults.models.

- modelOverrides enables model-driven overrides like [[tts:...]] tags (on by default).
- /tts limit and /tts summary control per-user summarization settings.
- apiKey values fall back to ELEVENLABS_API_KEY/XI_API_KEY and OPENAI_API_KEY.
- elevenlabs.baseUrl overrides the ElevenLabs API base URL.
- elevenlabs.voiceSettings supports stability/similarityBoost/style (0..1),
useSpeakerBoost, and speed (0.5..2.0).

### ​talk

Defaults for Talk mode (macOS/iOS/Android). Voice IDs fall back to ELEVENLABS_VOICE_ID or SAG_VOICE_ID when unset.
apiKey falls back to ELEVENLABS_API_KEY (or the gateway’s shell profile) when unset.
voiceAliases lets Talk directives use friendly names (e.g. "voice":"Clawd").
Copy
```
{
  talk: {
    voiceId: "elevenlabs_voice_id",
    voiceAliases: {
      Clawd: "EXAVITQu4vr4xnSDxMaL",
      Roger: "CwhRBWXzGAHq8TQ4Fs17",
    },
    modelId: "eleven_v3",
    outputFormat: "mp3_44100_128",
    apiKey: "elevenlabs_api_key",
    interruptOnSpeech: true,
  },
}

```

### ​agents.defaults

Controls the embedded agent runtime (model/thinking/verbose/timeouts).
agents.defaults.models defines the configured model catalog (and acts as the allowlist for /model).
agents.defaults.model.primary sets the default model; agents.defaults.model.fallbacks are global failovers.
agents.defaults.imageModel is optional and is only used if the primary model lacks image input.
Each agents.defaults.models entry can include:

- alias (optional model shortcut, e.g. /opus).
- params (optional provider-specific API params passed through to the model request).

params is also applied to streaming runs (embedded agent + compaction). Supported keys today: temperature, maxTokens. These merge with call-time options; caller-supplied values win. temperature is an advanced knob—leave unset unless you know the model’s defaults and need a change.
Example:
Copy
```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-sonnet-4-5-20250929": {
          params: { temperature: 0.6 },
        },
        "openai/gpt-5.2": {
          params: { maxTokens: 8192 },
        },
      },
    },
  },
}

```

Z.AI GLM-4.x models automatically enable thinking mode unless you:

- set --thinking off, or
- define agents.defaults.models["zai/<model>"].params.thinking yourself.

OpenClaw also ships a few built-in alias shorthands. Defaults only apply when the model
is already present in agents.defaults.models:

- opus -> anthropic/claude-opus-4-6
- sonnet -> anthropic/claude-sonnet-4-5
- gpt -> openai/gpt-5.2
- gpt-mini -> openai/gpt-5-mini
- gemini -> google/gemini-3-pro-preview
- gemini-flash -> google/gemini-3-flash-preview

If you configure the same alias name (case-insensitive) yourself, your value wins (defaults never override).
Example: Opus 4.6 primary with MiniMax M2.1 fallback (hosted MiniMax):
Copy
```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "opus" },
        "minimax/MiniMax-M2.1": { alias: "minimax" },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: ["minimax/MiniMax-M2.1"],
      },
    },
  },
}

```

MiniMax auth: set MINIMAX_API_KEY (env) or configure models.providers.minimax.

#### ​agents.defaults.cliBackends (CLI fallback)

Optional CLI backends for text-only fallback runs (no tool calls). These are useful as a
backup path when API providers fail. Image pass-through is supported when you configure
an imageArg that accepts file paths.
Notes:

- CLI backends are text-first; tools are always disabled.
- Sessions are supported when sessionArg is set; session ids are persisted per backend.
- For claude-cli, defaults are wired in. Override the command path if PATH is minimal
(launchd/systemd).

Example:
Copy
```
{
  agents: {
    defaults: {
      cliBackends: {
        "claude-cli": {
          command: "/opt/homebrew/bin/claude",
        },
        "my-cli": {
          command: "my-cli",
          args: ["--json"],
          output: "json",
          modelArg: "--model",
          sessionArg: "--session",
          sessionMode: "existing",
          systemPromptArg: "--system",
          systemPromptWhen: "first",
          imageArg: "--image",
          imageMode: "repeat",
        },
      },
    },
  },
}

```

Copy
```
{
  agents: {
    defaults: {
      models: {
        "anthropic/claude-opus-4-6": { alias: "Opus" },
        "anthropic/claude-sonnet-4-1": { alias: "Sonnet" },
        "openrouter/deepseek/deepseek-r1:free": {},
        "zai/glm-4.7": {
          alias: "GLM",
          params: {
            thinking: {
              type: "enabled",
              clear_thinking: false,
            },
          },
        },
      },
      model: {
        primary: "anthropic/claude-opus-4-6",
        fallbacks: [
          "o