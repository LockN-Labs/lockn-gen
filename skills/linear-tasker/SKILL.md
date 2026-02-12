---
name: linear-tasker
description: Manage Linear work items and subtasks via GraphQL API. Use when creating or tracking work items, assigning tasks to agents, or updating task status. Supports creating subtasks under parent issues, updating status (todo, in-progress, done), adding labels, and querying issue details for context. Triggers on any task creation, issue tracking, or workflow management request.
aliases: [linear-tasker]
---

# Linear Workflow Integration

Use Linear as the source of truth for all coding tasks. When implementing features or fixing bugs, always create work items first — don't work from memory or loose notes.

## Core Principle

**Never start work without a Linear ticket.** Every implementation task should have:
- A parent issue (e.g., LOC-7, LOC-8, LOC-9)
- A subtask (e.g., LOC-7-1 "Create AgentSession entity")
- A label indicating which agent should handle it (e.g., `agent:coder`, `agent:qa`)

## Quick Start

```bash
# Create a subtask under parent issue
{baseDir}/scripts/create-subtask.sh "Create QueryService.cs" "loc-10" "agent:coder"

# Update status to in-progress
{baseDir}/scripts/update-status.sh "loc-10-1" "in-progress"

# Update status to done
{baseDir}/scripts/update-status.sh "loc-10-1" "done"
```

## Workflow Integration

### For the Coding Pipeline

When you (the orchestrator) break a feature into subtasks:

1. **Create parent issue** if it doesn't exist
2. **Create subtasks** for each implementation step
3. **Assign labels** (`agent:coder` for implementation, `agent:qa` for tests)
4. **Dispatch agents** to pick up subtasks from Linear
5. **Update status** as agents complete work
6. **Before closing any ticket, run sibling cross-reference**
   - Query parent + related tickets for open siblings
   - Compare delivered code against sibling acceptance criteria
   - Comment on overlapping siblings with delivered scope
   - Update sibling descriptions with `## [Already Built]` + checkbox AC updates
   - Close sibling too if fully delivered (with attribution comment)
7. **Review done subtasks** before merging into PR

### Example: LOC-10 Query API

```
Parent: LOC-10 "Query/Search API"

Subtasks:
• LOC-10-1 "Create QueryService with SearchRecord query" [agent:coder]
• LOC-10-2 "Write QueryService tests" [agent:qa]
• LOC-10-3 "Add search endpoint to API" [agent:coder]
• LOC-10-4 "Write API controller tests" [agent:qa]

Flow:
  Codex creates tickets → Coding agents pick up → Codex reviews → PR created
```

## API Configuration

API endpoint: `https://api.linear.app/graphql`

Authentication: Use `LINEAR_API_KEY` environment variable (set in your shell).

Default headers:
```bash
-H "Authorization: Bearer $LINEAR_API_KEY"
-H "Content-Type: application/json"
```

## Subtask Naming Convention

Follow this pattern for consistency:

```
{PARENT}-{SEQ}-{TASK_NAME}

Examples:
• loc-7-1 "Create AgentSession entity"
• loc-8-2 "Implement CreateReceipt endpoint"
• loc-9-1 "Add MinIO bucket configuration"
```

## Labels for Agents

Use these labels to route work:

| Label | Purpose | Example |
|-------|---------|---------|
| `agent:coder` | Implementation | `agent:coder` |
| `agent:qa` | Testing | `agent:qa` |
| `agent:review` | Code review | `agent:review` |

## When NOT to Use Linear

- **Quick mental tasks**: "Remember to check disk space" — don't create a ticket
- **Already tracked**: If there's an existing ticket, use it instead of creating a new one
- **Done work**: Don't create tickets for completed work — just close them

## Querying Issues

To read issue details for context:

```bash
{baseDir}/scripts/query-issue.sh "loc-10"
```

This returns title, description, status, labels, and assignee.

## Error Handling

- **401 Unauthorized**: Check `LINEAR_API_KEY` is set
- **404 Not Found**: Issue/Task ID doesn't exist
- **500 Internal Error**: Linear API issue — retry after 5 seconds
