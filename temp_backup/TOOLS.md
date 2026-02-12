# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Figma
- Desktop app: C:\Users\Sean\AppData\Local\Figma\Figma.exe (auto-starts on boot)
- Bridge plugin: ~/.npm/_npx/b547afed9fcf6dcb/node_modules/figma-console-mcp/figma-desktop-bridge/
- WebSocket port: 9223
- Main file: "LockN AI" (key: 6MEJFHJ04qsFBtTJt7bZJO)
- PAT: in .env as FIGMA_API_KEY
- AI credits: 3,000/month (Figma plan)
- IMPORTANT: Bridge plugin must run from Design mode (Dev mode = read-only)
- **Port proxy**: Windows `netsh portproxy` forwards localhost:9223 → WSL IP:9223. WSL IP changes on reboot — re-run `figma-bridge-proxy.ps1` as Admin.
- **Subagent limitation**: Only main session can use Figma tools (MCP server owns port 9223). Subagents must use HTML/CSS fallback.
- **Full runbook**: `docs/figma-integration-runbook.md`
- **Startup sequence**: Gateway auto → portproxy script → open Figma → activate Bridge plugin manually

Add whatever helps you do your job. This is your cheat sheet.
