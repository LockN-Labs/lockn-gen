# linear-pr-linker

Auto-link Linear tickets to GitHub PRs and keep ticket status in sync with PR status.

## Requirements

- `gh` (GitHub CLI) authenticated to the repo
- `jq`
- `curl`
- `LINEAR_API_KEY` environment variable with access to Linear GraphQL API

## Environment Variables

- `LINEAR_API_KEY` **(required)**: Linear GraphQL API key
- `LINEAR_TICKET_PREFIX` *(optional)*: Ticket prefix to detect (default: `LOC-`)
- `LINEAR_TARGET_STATE` *(optional)*: Target state name for merged PRs (default: `Done`)

## Scripts

### `link-pr.sh`
Links a PR to a Linear ticket when the PR title or branch contains `LOC-XXX`.

**Usage**:
```bash
./link-pr.sh [--pr <number>|<url>]
```

If `--pr` is omitted, it uses the current PR from the git repo context (via `gh`).

### `sync-status.sh`
Syncs PR review status (approved/changes requested/review required) to Linear by posting a comment on the ticket.

**Usage**:
```bash
./sync-status.sh [--pr <number>|<url>]
```

### `on-merge.sh`
When a PR merges, move the linked Linear ticket from **In Review** → **Done** (or `LINEAR_TARGET_STATE`).

**Usage**:
```bash
./on-merge.sh [--pr <number>|<url>]
```

## How it works

1. Uses `gh pr view` to fetch PR metadata and review status.
2. Extracts `LOC-XXX` from the PR title or branch name.
3. Calls Linear GraphQL API:
   - `createComment` to add PR link or review status
   - `updateIssue` to move ticket to the target workflow state

## Example

```bash
export LINEAR_API_KEY=lin_api_...
export LINEAR_TARGET_STATE="Done"

./link-pr.sh --pr 123
./sync-status.sh --pr 123
./on-merge.sh --pr 123
```
