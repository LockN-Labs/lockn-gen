# Linear Integration

## Workspace

- **Team:** LockN AI
- **API:** GraphQL via `LINEAR_API_KEY` env var

## Ticket Lifecycle

```
Backlog → Todo → In Progress → In Review → Done
                                    ↓
                              (QA validation)
                                    ↓
                                  Done
```

### States
| State | Meaning |
|-------|---------|
| Backlog | Future work, not prioritized |
| Todo | Ready to start, prioritized |
| In Progress | Active development |
| In Review | Code complete, awaiting review/QA |
| Done | Deployed and verified |
| Canceled | Won't do |

## Labels

| Label | Use |
|-------|-----|
| `spike` | Research/exploration task |
| `bug` | Defect fix |
| `feature` | New capability |
| `refactor` | Code improvement |
| `docs` | Documentation |

## Ticket Format

### Title
```
[Type]: <Brief description>
```

### Description
```markdown
## Goal
What we're trying to achieve

## Approach
How we'll do it

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Related
- LOC-XXX (parent/related)
```

## Automation

### Orchestrator Responsibilities
1. Create tickets before starting work
2. Update status as work progresses
3. Link PRs to tickets
4. Close tickets after QA validation
5. Don't mark Done until deployed + verified

### Comments
- Add deployment notes: `✅ Deployed to Dev (commit abc123)`
- Add QA results: `✅ QA Passed — promoted to Test`
- Add blockers: `⚠️ Blocked on LOC-XXX`

## API Examples

```bash
# List team tickets
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "{ issues { nodes { identifier title state { name } } } }"}'

# Create ticket
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "mutation { issueCreate(input: {...}) { success } }"}'
```
