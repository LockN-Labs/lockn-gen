---
name: notion
description: Notion API for creating and managing pages, databases, and blocks. Includes structured workflows for knowledge capture, research documentation, meeting prep, and spec-to-implementation pipelines.
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: ["NOTION_API_KEY"]
    primaryEnv: "NOTION_API_KEY"
---

# Notion Skill (Enhanced)

Use the Notion API to create/read/update pages, databases, and blocks. Includes structured workflows adapted from OpenAI's curated Notion skills.

## Setup

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Set `NOTION_API_KEY` in your environment (already in `/home/sean/.openclaw/.env`)
4. Share target pages/databases with your integration (click "..." → "Connect to" → your integration name)

## API Basics

```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

> **Rate limit:** ~3 requests/second average. Implement exponential backoff on 429 responses.

## Core Operations

### Search
```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "search term"}'
```

### Get Page
```bash
curl "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Get Page Content (Blocks)
```bash
curl "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### Create Page
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

### Update Page
```bash
curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Add Blocks to Page
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello"}}]}}
    ]
  }'
```

### Query a Database (Data Source)
```bash
curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

## Property Types

- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "a@b.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

## API Version Notes (2025-09-03)

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries
- **Two IDs:** Each database has `database_id` (for creating pages) and `data_source_id` (for querying)
- **Search results:** Databases return as `"object": "data_source"`

## Structured Workflows

### Knowledge Capture
Convert conversations and decisions into structured Notion pages.
See: `reference/databases/` for database schemas and templates.

**Workflow:**
1. Determine content type (decision, how-to, FAQ, wiki, documentation)
2. Search for existing pages to update/link
3. Extract facts, decisions, actions, rationale
4. Create page with proper database schema
5. Link to related pages and hub pages

### Research & Documentation
Synthesize information into structured briefs, comparisons, or reports.
See: `reference/research/` for format guides and templates.

**Format selection:**
- Quick readout → `reference/research/quick-brief-template.md`
- Single-topic → `reference/research/research-summary-template.md`
- Option tradeoffs → `reference/research/comparison-template.md`
- Deep dive → `reference/research/comprehensive-report-template.md`

### Meeting Intelligence
Prepare meeting materials with Notion context.
See: `reference/meetings/` for templates by meeting type.

**Templates:** status update, decision meeting, sprint planning, 1:1, retrospective, brainstorming.

### Spec-to-Implementation
Turn Notion specs into implementation plans and Linear tickets.
See: `reference/implementation/` for parsing guides and plan templates.

**Flow:**
1. Fetch spec → parse requirements (`reference/implementation/spec-parsing.md`)
2. Choose plan depth (`quick-implementation-plan.md` vs `standard-implementation-plan.md`)
3. Size tasks to 1-2 days (`reference/implementation/task-creation.md`)
4. Create Linear tickets with acceptance criteria
5. Track progress (`reference/implementation/progress-tracking.md`)

## Rate Limit Best Practices

- **Rate:** ~3 req/sec average
- **Retry:** Exponential backoff with jitter on HTTP 429
- **Batch:** Consolidate block appends (send multiple children in one call)
- **Cache:** Cache frequently-read pages to reduce API hits
- **Queue:** For bulk operations, queue writes and drain at sustainable rate

## Reference Files

```
reference/
├── databases/          # Database schemas & best practices
│   ├── database-best-practices.md
│   ├── decision-log-database.md
│   ├── documentation-database.md
│   ├── faq-database.md
│   ├── how-to-guide-database.md
│   ├── learning-database.md
│   └── team-wiki-database.md
├── meetings/           # Meeting prep templates
│   ├── template-selection-guide.md
│   ├── status-update-template.md
│   ├── decision-meeting-template.md
│   ├── sprint-planning-template.md
│   ├── one-on-one-template.md
│   ├── retrospective-template.md
│   └── brainstorming-template.md
├── research/           # Research & documentation formats
│   ├── format-selection-guide.md
│   ├── quick-brief-template.md
│   ├── research-summary-template.md
│   ├── comparison-template.md
│   ├── comprehensive-report-template.md
│   ├── advanced-search.md
│   └── citations.md
└── implementation/     # Spec-to-implementation
    ├── spec-parsing.md
    ├── quick-implementation-plan.md
    ├── standard-implementation-plan.md
    ├── task-creation.md
    ├── task-creation-template.md
    ├── progress-tracking.md
    ├── progress-update-template.md
    └── milestone-summary-template.md
```

## MCP Integration (Live — LOC-350 ✅)

Notion access is available via native MCP tools through `openclaw-mcp-adapter`:

**Transport:** Local stdio (`@notionhq/notion-mcp-server` v2.0.0)
**Auth:** API key via `NOTION_TOKEN` env var (no OAuth needed)
**Tools:** 22 native tools with `notion_API-` prefix

### Available Tools
- `notion_API-post-search` — Search by title
- `notion_API-retrieve-a-page` — Get page properties
- `notion_API-get-block-children` — Read page content
- `notion_API-patch-block-children` — Append content to pages
- `notion_API-post-page` — Create pages
- `notion_API-patch-page` — Update page properties
- `notion_API-query-data-source` — Query databases (v2.0 "data sources")
- `notion_API-create-a-data-source` — Create databases
- `notion_API-retrieve-a-data-source` — Get database schema
- `notion_API-move-page` — Move pages between parents
- And more (comments, blocks, users, templates)

### Workspace Structure (2026-02-09 restructure)
```
LockN AI (root: 2ffb5f0c-1a51-800c-891b-c16ee9e721a3)
├── 🚀 Product Hub          — product dashboards
├── ⚙️ Engineering Hub       — infra, models, dev workflow
├── 💼 Business Hub          — company, costs, revenue
├── 📂 Databases             — Projects Registry, ADR Log, Research Library
├── 🏗️ Architecture          — decisions, agent arch, model hierarchy
├── 🔧 Operations            — infrastructure, cron, skills, permissions
├── 🔬 Research              — research summaries and spikes
├── 🔒 Security              — assessments and audits
├── 💼 Business Summaries
└── 📊 Executive Summaries
```

### Where to Put Things
| Content Type | Destination |
|-------------|-------------|
| Architecture decision | ADR Log database (📂 Databases) |
| Research findings | Research Library database (📂 Databases) |
| Project status | Projects Registry database (📂 Databases) |
| Technical doc | 🏗️ Architecture section |
| Operational config | 🔧 Operations section |
| Security assessment | 🔒 Security section |
| Product overview | 🚀 Product Hub |

Config: `/home/sean/.openclaw/workspace/config/notion-pages.json`
