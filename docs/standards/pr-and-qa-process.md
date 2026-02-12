# LockN Labs — PR & QA Process Standard

**Applies to:** All LockN repos (lockn-score, lockn-logger, lockn-auth, lockn-web, lockn-ai-platform, lockn-brain, lockn-speak, lockn-listen, lockn-sense, lockn-gen, lockn-loader, lockn-infra, lockn-suite, lockn-swap, lockn-bot)

**Effective:** 2026-02-10

---

## 1. Design-First Workflow

```
Figma Design → Design Approval → Implementation → PR → Review → Visual QA → Stakeholder Testing → Merge → Deploy
```

**Rule:** No UI implementation begins until Figma mockups exist and are linked in the Linear ticket. Design tickets BLOCK implementation tickets.

For non-UI work (backend, infra, config), skip Figma but still follow the PR process below.

---

## 2. Pull Request Requirements

Every PR must use the `.github/PULL_REQUEST_TEMPLATE.md` template:

### Required Sections

| Section | UI Changes | Non-UI Changes |
|---------|-----------|----------------|
| **Summary + Linear ticket** | ✅ Required | ✅ Required |
| **Screenshots (before/after)** | ✅ Required | "N/A — no visual changes" |
| **Changes list** | ✅ Required | ✅ Required |
| **Testing steps** | ✅ Required | ✅ Required |
| **Design alignment (Figma link)** | ✅ Required | N/A |

### Screenshot Standards

- **Before/after table** for any visual change
- **Full-page screenshots** at key breakpoints (mobile, tablet, desktop as applicable)
- **Component-level screenshots** for isolated component changes
- **Screen recordings** for animations, transitions, or interactive flows
- **Figma frame link** alongside implementation screenshot for comparison

---

## 3. Review Pipeline

```
PR Opened
  → Automated Build Check (TS/lint/test)
  → Code Review Agent (quality, SOLID, security, scope)
  → Visual QA (Qwen3-VL — Figma vs implementation)
  → Stakeholder Testing (PM + UX + QA agents)
  → Merge
```

### 3a. Code Review (Automated)
- Code quality, SOLID principles, security
- Scope check — no files outside ticket scope
- Build must pass (`npm run build` / `dotnet build`)
- PRs with build failures are auto-blocked

### 3b. Visual QA — Qwen3-VL (LOC-418)
- **Trigger:** After code review passes, for any PR with UI changes
- **Process:** Playwright captures implementation screenshots → compared against Figma exports
- **Scoring:** Layout, spacing, colors, typography, overall (0-10 each)
- **Gate:** ≥8.0 pass, 6.0-7.9 conditional (PM decides), <6.0 block

| Model | Use Case | Cost |
|-------|----------|------|
| Qwen3-VL 8B (local) | Per-screen quick checks | $0 |
| Qwen3-VL 235B (cloud) | Complex layouts, borderline scores | ~$0.01/comparison |

### 3c. Stakeholder Testing Phase
For significant UI/UX changes, the full stakeholder review runs:

| Agent | Model | Reviews |
|-------|-------|---------|
| **QA** | Playwright + VL 8B | Visual fidelity, interaction bugs, edge cases |
| **PM** | Opus/Codex | Business logic, user flow, copy accuracy |
| **UX** | VL 235B (cloud) | Design system compliance, accessibility, patterns |

Each agent posts structured feedback on the Linear ticket. All must pass before merge.

---

## 4. Linear Ticket Lifecycle

```
Backlog → Todo → In Progress → In Review → Visual QA → Stakeholder Testing → Done
```

- **In Progress:** Implementation underway
- **In Review:** PR open, code review in progress
- **Visual QA:** Automated Figma comparison running
- **Stakeholder Testing:** PM/UX/QA agents reviewing
- **Done:** Only after QA sign-off + deploy to Test verified

---

## 5. Repo Setup Checklist

Every LockN repo must have:

- [ ] `.github/PULL_REQUEST_TEMPLATE.md` (standardized)
- [ ] Branch protection on main/master (require PR, require build pass)
- [ ] GitHub Actions CI workflow (build + lint + test)
- [ ] Linear ticket prefix in branch names (`feat/loc-XXX-description`)

---

*This standard is maintained by the LockN orchestration system. Updates require Sean's approval for scope changes.*
