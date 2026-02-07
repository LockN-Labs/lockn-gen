# Notion Integration

## Workspace

- **Name:** LockN AI
- **API:** REST via `NOTION_API_KEY` env var
- **Skill:** `notion` skill for page operations

## Purpose

Notion serves as the **knowledge base** while Linear tracks **work items**.

| System | Purpose |
|--------|---------|
| Linear | Task tracking, sprint planning |
| Notion | Documentation, architecture, decisions |
| GitHub | Code, PRs, version control |

## Page Structure

```
LockN AI Workspace
├── System Architecture
│   └── Current infrastructure, model stack
├── Model Configuration  
│   └── LLM endpoints, VRAM allocation
├── Development Workflow
│   └── PR process, review checklist
├── Cron Jobs
│   └── Scheduled tasks, heartbeat config
├── Skills Reference
│   └── Available skills, usage patterns
└── Troubleshooting
    └── Common issues, resolution steps
```

## Sync Strategy

### Automated (Cron)
- **Hourly:** Qwen3-32B syncs changes (free, fast)
- **6-hour:** Opus reviews for quality improvements

### Manual Triggers
- Major architecture changes
- New skill additions
- Process updates

## API Usage

```bash
# Get page
curl https://api.notion.com/v1/pages/{page_id} \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"

# Update page
curl -X PATCH https://api.notion.com/v1/pages/{page_id} \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"properties": {...}}'
```

## Best Practices

1. **Single source of truth** — Notion for docs, Linear for tasks
2. **Link everything** — Cross-reference between systems
3. **Keep current** — Stale docs are worse than no docs
4. **Structure for search** — Use headers, tags, consistent naming
