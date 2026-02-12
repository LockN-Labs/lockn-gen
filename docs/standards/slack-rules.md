# Slack Communication Rules

**All agents and cron jobs MUST follow these rules when posting to Slack.**

## Threading Policy
- **ALWAYS post as top-level channel messages** — never use `replyTo` or `threadId` in message sends.
- Only use thread replies when the human operator explicitly starts replying to a specific message (intentionally going down a rabbit hole).
- Default is ALWAYS top-level channel messages.

## Message Quality
- One composed message, not fragments. Wait until you have the full picture, then send ONE coherent message.
- When referencing Linear tickets, ALWAYS format as linked: `<https://linear.app/lockn-ai/issue/LOCKN-xxx|LOCKN-xxx>`. Never bare text.
- When referencing text/markdown files for review, attach the actual files in the same Slack message.
- Include ticket and/or PR links when referencing code changes, syntax, or formatting.

## Channel Routing
- Never use the DM thread for comms. Route ALL messages through the appropriate Slack channel.
- If no appropriate channel exists, suggest creation in #process-improvements.
