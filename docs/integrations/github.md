# GitHub Integration

## Repositories

| Repo | Purpose | Status |
|------|---------|--------|
| [lockn-score](https://github.com/LockN-AI/lockn-score) | AI Sports Scoring MVP | Active |
| [lockn-logger](https://github.com/LockN-AI/lockn-logger) | Usage logging API | Active |
| [lockn-sense](https://github.com/LockN-AI/lockn-sense) | Unified multimodal perception | Planned |

## PR Workflow

### Branch Naming
- `feature/<ticket-id>-<description>` — New features
- `fix/<ticket-id>-<description>` — Bug fixes
- `refactor/<description>` — Code improvements
- `docs/<description>` — Documentation updates
- `catchup/<description>` — Retroactive PRs

### PR Process
1. **Create branch** from `master`/`main`
2. **Implement** with atomic commits
3. **Open PR** with:
   - Clear title matching ticket
   - Description with context
   - Link to Linear ticket
4. **Automated Review** by review agent:
   - Code quality
   - Optimization opportunities
   - SOLID architecture
   - Security review
   - Extensibility alignment
   - Correctness
   - Composability
   - Testability
   - Maintainability
   - Usability
5. **Test** — Pull locally, run tests
6. **Merge** — Orchestrator merges after review passes
7. **Close ticket** — Update Linear status

### Commit Convention
```
<type>(<scope>): <description>

[optional body]

[optional footer: Closes LOC-XXX]
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`

## CI/CD (Planned)

- **Dev** — Auto-deploy on push to feature branch
- **Test** — Promote after Codex QA pass
- **Prod** — Promote after regression suite

## Access

- **CLI:** `gh` (GitHub CLI) authenticated
- **API:** Via `gh api` for advanced queries
