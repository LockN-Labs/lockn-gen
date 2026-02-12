# GitHub Admin Skill

Manage GitHub Apps, installations, and organization-level operations for LockN-Labs.

## Overview

This skill provides authenticated access to GitHub via LockN GitHub Apps, enabling:
- App installation management
- Webhook configuration
- Repository operations with agent-specific attribution
- Status check posting

## Available Apps

| App | ID | Purpose | Key File |
|-----|-----|---------|----------|
| LockN Coder | 2816646 | Push code, create PRs | `lockn-coder.2026-02-07.private-key.pem` |
| LockN QA | 2816677 | Run tests, post checks, log bugs | `lockn-qa.2026-02-07.private-key.pem` |
| LockN Architect | 2816706 | Review PRs, set priorities | `lockn-architect.2026-02-07.private-key.pem` |
| LockN DevOps | 2816768 | Deployments, workflows, IaC | `lockn-devops.2026-02-07.private-key.pem` |
| LockN Orchestrator | 2816797 | Full org admin, merges, coordination | `lockn-orchestrator.2026-02-07.private-key.pem` |

Keys stored in: `/home/sean/keys/`

## Usage

### Get Installation Token

```bash
# Source the helper
source /home/sean/.openclaw/workspace/skills/github-admin/gh_app.sh

# Get token for specific app
TOKEN=$(gh_app_token orchestrator)

# Use with gh CLI
GH_TOKEN=$TOKEN gh api /repos/LockN-Labs/lockn-ai-platform
```

### Python API

```python
from gh_admin import GitHubAppAuth

# Authenticate as Orchestrator
auth = GitHubAppAuth('orchestrator')
token = auth.get_installation_token('LockN-Labs')

# Use token for API calls
headers = {'Authorization': f'token {token}'}
```

## Common Operations

### Install App on Org
```bash
# Opens browser to install app
gh_app_install orchestrator LockN-Labs
```

### Post Status Check
```bash
gh_app_status qa LockN-Labs/lockn-logger $SHA "success" "Tests passed"
```

### Create PR as Agent
```bash
TOKEN=$(gh_app_token coder)
GH_TOKEN=$TOKEN gh pr create --title "feat: ..." --body "..."
```

## Webhook Configuration

Webhook URL: `https://api.dev.lockn.ai/webhooks/github`

Events per app:
- **Coder**: push, pull_request
- **QA**: check_run, check_suite
- **Architect**: pull_request, pull_request_review  
- **DevOps**: push, pull_request, deployment, workflow_run
- **Orchestrator**: push, pull_request, issues

## Security Notes

- Private keys stored in `/home/sean/keys/` (not in repo)
- Installation tokens expire after 1 hour
- Use minimum-privilege app for each operation
- Orchestrator has full org admin — use sparingly
