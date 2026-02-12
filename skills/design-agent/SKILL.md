# Design Agent Skill

Backend-agnostic design creation abstraction. Agents use this skill instead of calling design tool MCPs directly.

## Architecture

```
UX Agents / Any Agent
    ↓
skills/design-agent/ (this skill)
    ↓
┌─────────────────┬──────────────┬─────────────┐
│ figma-console   │ penpot-mcp   │ local render│
│ (active)        │ (LOC-438)    │ (LOC-439)   │
└─────────────────┴──────────────┴─────────────┘
```

## Current Backend: figma-console-mcp

Connected via OpenClaw MCP adapter. Tools are prefixed with `figma-console_`.

### Connection Requirements

The figma-console-mcp server communicates with Figma Desktop via the **Desktop Bridge Plugin**:
- Plugin location: `~/.npm/_npx/b547afed9fcf6dcb/node_modules/figma-console-mcp/figma-desktop-bridge/`
- WebSocket port: 9223 (localhost)
- Figma Desktop must be running with the bridge plugin active

### Available Operations

#### Read Operations (via figma-console_ prefix)
- `figma-console_get_file_info` — Get file metadata
- `figma-console_get_node` — Get node details
- `figma-console_get_styles` — Get styles from file
- `figma-console_get_variables` — Get design tokens/variables
- `figma-console_get_components` — List components
- `figma-console_screenshot` — Take screenshot of current view
- `figma-console_get_console_logs` — Get plugin console logs

#### Write Operations (via figma-console_ prefix)
- `figma-console_create_frame` — Create a new frame
- `figma-console_create_rectangle` — Create rectangle
- `figma-console_create_text` — Create text node
- `figma-console_create_component` — Create component
- `figma-console_create_instance` — Instantiate a component
- `figma-console_set_fill` — Set fill color
- `figma-console_set_stroke` — Set stroke
- `figma-console_resize_node` — Resize a node
- `figma-console_move_node` — Move a node
- `figma-console_delete_node` — Delete a node
- `figma-console_set_text` — Set text content
- `figma-console_create_variable` — Create design token
- `figma-console_update_variable` — Update design token
- `figma-console_rename_variable` — Rename design token
- `figma-console_delete_variable` — Delete design token

#### Read-Only API (via figma_ prefix — figma-developer-mcp)
For pulling existing design data without the bridge:
- `figma_get_figma_data` — Get file data, layout, components
- `figma_download_figma_images` — Download images/icons from files

## Usage Pattern

### Creating a Simple UI Component

```
1. Create a frame:     figma-console_create_frame(name, width, height, x, y)
2. Add background:     figma-console_set_fill(nodeId, color)
3. Add text:           figma-console_create_text(text, fontSize, x, y, parentId)
4. Add elements:       figma-console_create_rectangle(width, height, x, y, parentId)
```

### Design Token Management

```
1. List tokens:        figma-console_get_variables(collectionName)
2. Create token:       figma-console_create_variable(name, type, value, collection)
3. Update token:       figma-console_update_variable(variableId, value)
```

## Key Constraints

1. **Never call figma-console-mcp tools directly** — always go through this skill's documented interface
2. **Check connection first** — run `figma-console_get_file_info` to verify the bridge is connected before write operations
3. **The bridge plugin must be running** in Figma Desktop for write operations to work
4. **Read-only operations** (figma_ prefix) work without the bridge via REST API

## Swapping Backends

When LOC-438 (Penpot) or LOC-439 (local render) are ready, this skill will be updated to route through those backends instead. Agent code using this skill won't need to change.

## Troubleshooting

- **"Neither CDP nor WebSocket transport available"** — Open the Desktop Bridge plugin in Figma Desktop
- **Write operations fail but reads work** — Bridge plugin not connected, only REST API available
- **WebSocket connection refused on 9223** — figma-console-mcp server not running (restart OpenClaw)
