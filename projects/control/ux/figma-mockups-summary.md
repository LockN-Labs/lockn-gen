# LockN Control Mockups — Delivery Summary

## What I attempted
- Read source brief: `projects/control/ux/dashboard-vision.md`
- Attempted to connect to Figma Desktop Bridge using MCP tools:
  - `figma-console_figma_get_status`
  - `figma-console_figma_list_open_files`

## Figma connection result
Bridge connection was not available from this session:
- `transport.active: none`
- WebSocket server unavailable for this MCP process
- Port conflict reported: `EADDRINUSE` on port `9223`
- No connected files detected (`No files connected`)

Because the request explicitly required fallback delivery if bridge connection fails, I created a full visual mockup in HTML/CSS.

## Fallback visual delivered
Created:
- `projects/control/ux/dashboard-mockup.html`

This mockup includes all requested frames and states:
1. **Mission Control — Full Dashboard (1920×1080)**
   - Dark theme
   - 3-tier layout (22% alerts, 46% middle split, 32% queue)
   - Alerts & blockers cards (P1/P2)
   - Active threads table + cron + Linear in-progress area
   - System status with CPU/RAM/GPU KPIs, model servers, docker health grid, gateway stats
   - Priority queue table + WIP gauge (3/3)

2. **Component States**
   - Alert card states (P1/P2/P3/Acked)
   - Model server states (online/offline/degraded)
   - Docker cell states (healthy/unhealthy/starting)
   - Ticket row state references
   - WIP gauge states (under/at/over limit)

3. **Empty/Zero States**
   - All clear
   - No active threads
   - Queue empty

4. **2560×1440 variant**
   - Scaled variant section with sizing and density notes

## Design-rule compliance notes
- Minimum readable sizes maintained (14px metadata, 16px+ body, 18px+ section labels)
- Monospace used for IDs/timestamps/KPI values; sans-serif for labels
- Status-color semantics constrained to green/yellow/red/blue
- 8px-aligned spacing system and structured blocks suitable for Grafana translation
- Density prioritized over decorative whitespace

## Next step to place in Figma directly
Once the port conflict is cleared and this MCP instance can attach to the Desktop Bridge, I can immediately recreate these frames as native Figma frames/components on page **"LockN Control"** in file **"LockN AI"**.
