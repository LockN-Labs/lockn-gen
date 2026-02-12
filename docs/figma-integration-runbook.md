# Figma Integration Runbook

> **Purpose:** Fool-proof guide for the Figma ↔ OpenClaw integration chain.
> Last updated: 2026-02-11

## Architecture

```
Figma Desktop (Windows)
  └─ Desktop Bridge Plugin (manual activation per session)
       └─ WebSocket → localhost:9223 (Windows)
            └─ netsh portproxy → WSL IP:9223
                 └─ figma-console-mcp (node, managed by OpenClaw)
                      └─ OpenClaw gateway → Claws (main agent)
```

## The 5-Link Chain

| # | Link | Survives Reboot? | Auto-starts? | Fix |
|---|------|-----------------|-------------|-----|
| 1 | **figma-console-mcp** (WSL) | ✅ Yes | ✅ OpenClaw spawns it | Restart OpenClaw gateway |
| 2 | **figma-developer-mcp** (WSL) | ✅ Yes | ✅ OpenClaw spawns it | Restart OpenClaw gateway |
| 3 | **netsh portproxy** (Windows) | ✅ Yes | ✅ Persists across reboots | Re-run setup script |
| 4 | **WSL IP address** | ❌ Changes on reboot | N/A | Re-run portproxy with new IP |
| 5 | **Desktop Bridge Plugin** (Figma) | ❌ No | ❌ Manual every session | Right-click → Plugins → Development → Figma Desktop Bridge |

## ⚠️ Known Failure Points

### 1. WSL IP Changes After Reboot (CRITICAL)
The `netsh portproxy` rule hardcodes the WSL IP. After Windows restart, WSL gets a new IP and the proxy breaks silently.

**Fix:** Run the PowerShell script below after every Windows reboot.

### 2. Bridge Plugin Requires Manual Activation
Figma plugins don't auto-run. Must be manually started each Figma session.

**Fix:** None possible (Figma limitation). Add to startup checklist.

### 3. Subagent Port Conflict
Subagent sessions cannot connect to port 9223 — the MCP server already owns it. Only the main session has Figma access.

**Fix:** All Figma work must happen from main session or use HTML/CSS fallback for mockups.

### 4. MCP Server Binds to 127.0.0.1 Only
The figma-console-mcp listens on `127.0.0.1:9223`, not `0.0.0.0:9223`. The portproxy must target the WSL IP, which routes internally to localhost.

**Fix:** The portproxy `connectaddress` must be the WSL IP (not 127.0.0.1).

## Setup Scripts

### Windows: Port Proxy Setup (Run as Admin PowerShell)
Run this after every Windows restart:

```powershell
# figma-bridge-proxy.ps1 — Run as Administrator
# Updates the netsh portproxy rule with current WSL IP

# Get current WSL IP
$wslIp = (wsl hostname -I).Trim().Split(' ')[0]
if (-not $wslIp) {
    Write-Error "Could not get WSL IP. Is WSL running?"
    exit 1
}

Write-Host "WSL IP: $wslIp" -ForegroundColor Cyan

# Remove existing rule (ignore errors if none exists)
netsh interface portproxy delete v4tov4 listenport=9223 listenaddress=127.0.0.1 2>$null

# Add fresh rule
netsh interface portproxy add v4tov4 listenport=9223 listenaddress=127.0.0.1 connectport=9223 connectaddress=$wslIp

# Verify
Write-Host "`nActive port proxies:" -ForegroundColor Green
netsh interface portproxy show v4tov4

Write-Host "`nDone. Bridge plugin should connect via localhost:9223" -ForegroundColor Green
```

### Windows: Auto-Run on Login (Optional)
Save the script above as `C:\Scripts\figma-bridge-proxy.ps1`, then:

```powershell
# Create scheduled task to run at login (elevated)
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Scripts\figma-bridge-proxy.ps1"
$trigger = New-ScheduledTaskTrigger -AtLogon
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest
Register-ScheduledTask -TaskName "FigmaBridgeProxy" -Action $action -Trigger $trigger -Principal $principal -Description "Update WSL port proxy for Figma Desktop Bridge"
```

## Verification Checklist

Run from WSL to verify the full chain:

```bash
# 1. MCP server listening?
ss -tlnp | grep 9223
# Expected: LISTEN ... 127.0.0.1:9223 ... node

# 2. HTTP upgrade response? (proves WebSocket endpoint works)
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9223
# Expected: 426 (Upgrade Required)

# 3. From OpenClaw: check Figma connection status
# Use figma-console_figma_get_status tool
# Expected: transport.websocket.available = true, clientCount >= 1
```

## Startup Sequence (After Windows Reboot)

1. ✅ Windows boots → WSL starts automatically
2. ✅ OpenClaw gateway starts → spawns MCP servers (auto)
3. ⚠️ Run `figma-bridge-proxy.ps1` as Admin (or auto via scheduled task)
4. ⚠️ Open Figma Desktop
5. ⚠️ Right-click canvas → Plugins → Development → **Figma Desktop Bridge**
6. ✅ Bridge connects → Claws has Figma access

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "EADDRINUSE port 9223" | Stale error or duplicate MCP process | `kill $(lsof -t -i:9223)` then restart gateway |
| Bridge plugin says "Disconnected" | Port proxy stale (WSL IP changed) | Re-run portproxy script |
| `figma_get_status` shows no clients | Bridge plugin not running | Activate in Figma |
| Subagent can't use Figma tools | Expected — only main session can | Use main session or HTML fallback |
| "Cannot connect to Figma Desktop" | Bridge not activated yet | Step 5 above |
