# Dev Workflow Skill

Automates the SDLC for LockN-AI by wiring GitHub + Linear workflows: project initialization, issue-driven development, and PR review preparation.

## Metadata
- **Name:** dev-workflow
- **Version:** 0.2.0
- **Owner:** sean@lockn.ai
- **GitHub Org:** LockN-AI
- **Linear Org:** LockN AI
- **Linear Team ID:** f37ff2bb-141f-421a-9401-fb0008bfb67f
- **Linear Team Key:** LOC
- **Repos Root:** ~/repos/
- **Skills:** coding-pipeline, linear

## Entry Points
- `scripts/project-init.sh` — create repo, clone, create Linear epic + stories
- `scripts/linear-api.sh` — Linear GraphQL helper (create/list/update)
- `scripts/build-issue.sh` — create feature branch from Linear issue
- `scripts/review-pr.sh` — fetch PR diff for review

## Skills Integration
This workflow integrates with the following skills:

### coding-pipeline
Delegates implementation tasks to local Qwen3-Coder model via llama-server (port 11438).
Use for: Code generation, tests, bug fixes, refactoring.

### linear-tasker
Manages Linear work items and subtasks via GraphQL API.
Use for: Creating tickets, tracking status, assigning labels, auditing work.

## Requirements
- `~/bin/gh` authenticated for GitHub
- `LINEAR_API_KEY` env var set
- `curl` and `jq` available
- `llama-server` running on port 11438 (for coding-pipeline)
