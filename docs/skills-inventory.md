# Skills Inventory (Runtime + Workspace)

Purpose: authoritative inventory of usable skills and when to apply them.

Last reviewed: 2026-02-09 18:00 EST

## Runtime-Available Skills

### Built-in (shipped with OpenClaw)
| Skill | Purpose |
|-------|---------|
| `github` | Repository management, PRs, issues, CI via `gh` CLI |
| `notion` | Documentation sync, knowledge base via Notion API |
| `slack` | Messaging, reactions, pins via Slack bot |
| `tmux` | Remote-control tmux sessions for interactive CLIs |

### Workspace Custom Skills
| Skill | Purpose |
|-------|---------|
| `cicd` | GitHub Actions CI/CD workflows, branch protection, Docker publish |
| `coding-pipeline` | Delegate implementation to local Qwen3-Coder-Next (:11439) |
| `compute-priority` | Toggle local-first vs cloud-first compute modes |
| `dual-process` | Kahneman-inspired fast/slow reasoning (System 1: Qwen3-32B, System 2: Coder-Next) |
| `linear-tasker` | Linear issue creation, status updates, dependency management |
| `pm-bootstrap` | Multi-model project bootstrap for LockN modules |
| `rapid-dev` | Fast iteration mode — commits directly to main, summary PR at end |
| `semantic-search` | Search LockN codebase and memory via Qdrant |
| `session-bootstrap` | Load handoff state, daily logs, Linear tickets at session start |
| `session-handoff` | Persist session state before context flush or `/new` |

## Skill Selection Rules
1. Pick exactly one most-specific skill first
2. Read that skill's `SKILL.md` before executing skill-specific workflows
3. Do not load multiple skills up front unless task progression requires it

## Usage Patterns
| Task Type | Skill |
|-----------|-------|
| Code implementation | `coding-pipeline` |
| Issue tracking | `linear-tasker` |
| PR/repo management | `github` |
| Model mode switching | `compute-priority` |
| Fast vs deep reasoning | `dual-process` |
| Session continuity | `session-bootstrap` / `session-handoff` |
| Documentation sync | `notion` |
| Interactive terminals | `tmux` |
| Quick iteration | `rapid-dev` |

## Maintenance Rule
Update immediately when skills are added, removed, or re-scoped.
