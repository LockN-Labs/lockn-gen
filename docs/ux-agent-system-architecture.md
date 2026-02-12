# UX Agent System Architecture — LockN Labs

> Designed 2026-02-09 | Investor demo: 2026-02-10

---

## 1. Agent Definitions

### UX-vision-local (Qwen3-VL 8B — localhost:11434)

**Role:** Fast visual triage & regression checks.

| Task | Details |
|------|---------|
| Screenshot QA | Compare live screenshot to Figma export. Binary pass/fail + bounding-box annotations |
| Component-level scoring | Score individual UI components (buttons, cards, nav) on a 1-5 rubric |
| Quick diff | "Does this look the same as before?" — sub-2s latency |
| Visual regression gate | CI/CD blocker: screenshot before/after on every PR |

**When to use:** Any task where latency matters more than nuance. Batch jobs (daily walkthrough screenshots), PR gates, quick yes/no comparisons. Free, fast (~500ms/image), always available.

**Limitations:** Misses subtle design system violations (e.g., 2px spacing errors, slight color mismatches). Weaker at holistic page-level composition judgment.

### UX-vision-cloud (Qwen3-VL 235B — Ollama Cloud)

**Role:** Deep design analysis & creative evaluation.

| Task | Details |
|------|---------|
| Full-page UX audit | Holistic assessment: layout, hierarchy, whitespace, typography, color harmony |
| Design comparison | Side-by-side Figma mockup vs live app with detailed written critique |
| Competitive analysis | Compare LockN UI against competitor screenshots |
| Accessibility review | Color contrast, touch target sizes, readability scoring |
| Design generation guidance | Describe what a redesigned component should look like (text prompt for Figma Make) |

**When to use:** Escalation from local model (low-confidence scores), design overhauls, investor-facing reports, any task requiring nuanced aesthetic judgment. Costs money per call — use judiciously.

**Routing rule:** Local model runs first. If confidence < 0.7 OR score delta > 1.5 from previous audit, escalate to cloud.

### UX-lead (Codex — OpenAI)

**Role:** Orchestrator. Owns the design pipeline end-to-end.

**Tools it controls:**
- **Figma MCP** — Create/read/update Figma files, export frames, read design tokens
- **Playwright** — Navigate apps, take screenshots at specified viewports
- **OpenClaw subagent spawning** — Dispatch work to vision models
- **Linear API** — Create/update UX tickets
- **GitHub** — Read component code, trigger PRs via coding-pipeline

**Responsibilities:**
1. Decide what needs auditing and when
2. Translate vision model findings into actionable tickets
3. Maintain the design system source of truth in Figma
4. Approve/reject implementation PRs based on visual match
5. Generate Figma designs via Figma Make + manual refinement prompts

---

## 2. Skills

### a) `ux-kickoff`

**Trigger:** New project created in Linear OR manual invocation.

```
Step 1: UX-lead reads project brief (Linear ticket + Notion doc)
Step 2: UX-lead generates wireframe prompts → Figma Make creates initial layouts
Step 3: UX-vision-cloud reviews Figma output for:
        - Design system consistency (matches LockN design tokens)
        - Layout quality & hierarchy
        - Accessibility baseline
Step 4: UX-lead iterates on Figma (up to 3 rounds based on cloud feedback)
Step 5: UX-lead exports final frames, creates Linear ticket:
        "Implement [feature] per Figma frame [link]"
        Tags: ux-approved, has-figma
Step 6: Notify Sean in Slack with Figma link for final sign-off
```

**Design tokens source:** Single Figma file `LockN Design System` with:
- Colors (primary, secondary, semantic)
- Typography scale
- Spacing scale (4px base)
- Component library (buttons, cards, inputs, nav)

### b) `ux-regression`

**Trigger:** Every PR to main on any LockN app repo. Also runs on cron.

```
Step 1: Playwright navigates to each route in the affected app
        Viewports: [1920×1080, 1366×768, 390×844]
Step 2: Screenshots saved to workspace/screenshots/{app}/{route}/{viewport}/{timestamp}.png
Step 3: UX-vision-local compares each screenshot to:
        a) Previous baseline (pixel-level + perceptual)
        b) Figma export of same page (design fidelity)
Step 4: For each comparison, output:
        { route, viewport, drift_score: 0-10, changed_regions: [...], summary: "..." }
Step 5: If drift_score > 3 on any screenshot:
        - Escalate to UX-vision-cloud for detailed analysis
        - Block PR merge (add GitHub check)
        - Create Linear ticket tagged "visual-regression"
Step 6: If all scores ≤ 3: auto-approve visual check on PR
```

**Baseline management:**
- Baselines stored in `workspace/screenshots/baselines/{app}/`
- Updated automatically when PR merges to main
- Figma baselines re-exported weekly or on Figma file change (webhook)

### c) `ux-design-overhaul`

**Trigger:** Manual invocation with target app name.

```
Step 1: INVENTORY
        Playwright crawls target app, discovers all routes
        Screenshots every page at 3 viewports
        Save to workspace/screenshots/{app}/audit-{date}/

Step 2: LOCAL TRIAGE (parallel, all screenshots)
        UX-vision-local scores each page:
        { page, viewport, scores: { layout: 1-5, typography: 1-5, color: 1-5,
          spacing: 1-5, consistency: 1-5 }, overall: 1-5, notes: "..." }

Step 3: CLOUD DEEP-DIVE (worst 5 pages only)
        UX-vision-cloud provides:
        - Detailed critique (what's wrong, why)
        - Specific improvement recommendations
        - Reference to design system violations

Step 4: REDESIGN
        UX-lead synthesizes findings into Figma Make prompts
        Creates redesigned frames in Figma for each flagged page
        UX-vision-cloud reviews redesigns (1-2 iteration rounds)

Step 5: TICKET CREATION
        For each redesigned page, create Linear ticket:
        Title: "UX Overhaul: [App] — [Page Name]"
        Description: Before screenshot, Figma link, specific changes list
        Priority: Based on page traffic × severity score
        Labels: ux-overhaul, has-figma

Step 6: REPORT
        Generate summary in Notion: "UX Audit Report — [App] — [Date]"
        Post to Slack with top findings + Figma link
```

### d) `ux-walkthrough`

**Trigger:** Daily cron (6:00 AM ET).

```
Step 1: For each app in [lockn-score, lockn-logger, lockn-auth, lockn-ai]:
        Playwright navigates all known routes
        Screenshots at 1920×1080 (primary) + 390×844 (mobile)

Step 2: UX-vision-local scores every screenshot (parallel batch)
        Output: { app, page, viewport, overall_score: 1-5, issues: [...] }

Step 3: Compare to yesterday's scores
        Flag any page where score dropped ≥ 1 point

Step 4: Aggregate into daily UX health report:
        { date, apps: [{ name, avg_score, worst_page, trend }] }

Step 5: If any page scores < 3:
        Create Linear ticket (if one doesn't already exist for that page)
        Priority: Urgent if score < 2, Normal if 2-3

Step 6: Post daily summary to Slack #dev channel
        "🎨 UX Daily: Score 4.1 (+0.2) | Logger 3.8 (-0.1) ⚠️ | Auth 4.3 | Landing 4.5"
```

---

## 3. Collaboration Patterns

### UX → Code Pipeline

```
UX-lead approves Figma design
        ↓
Linear ticket created: "Implement [X] per Figma [link]"
  Labels: ux-approved, has-figma
  Acceptance criteria: "Must pass visual regression against Figma frame [ID]"
        ↓
Coder-Next picks up ticket (coding-pipeline skill)
  Reads Figma frame via MCP → extracts layout, colors, spacing
  Implements in React
  Opens PR
        ↓
PR triggers ux-regression skill
  Screenshots new implementation
  UX-vision-local compares to Figma export
  Pass → merge. Fail → comment on PR with annotated diff
        ↓
On merge: UX-vision-local takes final screenshot → new baseline
```

### Figma MCP Integration

Wire into `openclaw-mcp-adapter` as a new transport:

```yaml
# openclaw-mcp-adapter config
transports:
  figma:
    type: http
    server: "@anthropic/figma-mcp"
    capabilities:
      - read_file          # Get file structure, frames, components
      - export_frame       # Export frame as PNG/SVG
      - read_styles        # Get design tokens (colors, typography)
      - create_frame       # Create new frames via Figma Make
      - update_frame       # Modify existing frames
```

UX-lead is the only agent that talks to Figma MCP directly. Vision models receive exported PNGs only.

### Escalation Chain

```
UX-vision-local (fast, free)
  → confidence < 0.7 → UX-vision-cloud (slow, paid)
    → disagreement or complex judgment → UX-lead (orchestrator decides)
      → ambiguous/strategic → Sean (Slack notification)
```

---

## 4. Recurring Jobs

### Cron Schedule

| Job | Schedule | Model Cost |
|-----|----------|------------|
| `ux-walkthrough` | Daily 6:00 AM ET | Local only (free) |
| `ux-regression` (baseline refresh) | Weekly Sun 2:00 AM ET | Local only |
| Figma export sync | Weekly Mon 3:00 AM ET | None (API only) |
| Design system audit | Biweekly Fri 6:00 AM ET | Cloud (1 call) |
| Full overhaul scan | Monthly 1st, 6:00 AM ET | Cloud (5-10 calls) |

### Screenshot Strategy

**Apps & Routes:**

| App | Key Routes | Priority |
|-----|-----------|----------|
| LockN Score | `/dashboard`, `/reports`, `/settings`, `/onboarding` | High |
| LockN Logger | `/events`, `/analytics`, `/config` | High |
| LockN Auth | `/login`, `/signup`, `/reset`, `/profile` | Medium |
| lockn.ai | `/` (landing), `/pricing`, `/docs` | High (investor-facing) |

**Viewports:** `1920×1080` (desktop), `1366×768` (laptop), `390×844` (iPhone 14)

**Scoring rubric (each 1-5):**
- **Layout** — Visual hierarchy, alignment, grid consistency
- **Typography** — Scale, readability, font consistency
- **Color** — Palette adherence, contrast, harmony
- **Spacing** — Consistent padding/margins, breathing room
- **Consistency** — Cross-page coherence with design system

**Overall = weighted average:** Layout 25%, Typography 20%, Color 20%, Spacing 15%, Consistency 20%

**Linear ticket template:**
```
Title: 🎨 UX: [App] [Page] — [Primary Issue]
Priority: {Urgent|High|Normal} based on score
Labels: ux-audit, {app-name}
Description:
  Score: X.X/5 (down from Y.Y)
  Screenshot: [link]
  Issues:
  - [specific issue 1]
  - [specific issue 2]
  Figma reference: [link to design system page]
  Suggested fix: [actionable description]
```

---

## 5. Quick Wins for Tomorrow's Demo (TONIGHT)

### Win 1: Figma Mockup of LockN Score Dashboard (2 hours)

1. Take screenshots of current LockN Score dashboard
2. Use Figma Make to generate a polished redesign
3. UX-vision-cloud critiques → iterate once
4. Result: Before/after in Figma, shareable link

**Demo narrative:** "Our AI UX team audited the dashboard and produced this redesign autonomously."

### Win 2: Live Visual Regression Demo (1 hour)

1. Set up `ux-regression` skill with Playwright on lockn.ai landing page
2. Take baseline screenshots
3. Make a small intentional CSS change (e.g., shift a button 20px)
4. Run regression → show the agent detecting and flagging the drift
5. Show auto-created Linear ticket with annotated screenshot

**Demo narrative:** "Every code change is visually verified against our Figma designs. Drift is caught automatically."

### Win 3: UX Scorecard (30 min)

1. Run `ux-walkthrough` against all 4 apps (just the homepages)
2. Generate a scorecard: app name, score, top issue
3. Display in Notion or as a Slack message

**Demo narrative:** "Every morning, our AI UX team walks through every product and scores it. Here's today's report."

### Execution Order Tonight

```
23:30  Start Figma Make on LockN Score dashboard redesign
00:00  While Figma iterates, set up Playwright screenshot routes
00:30  Wire ux-regression skill (minimal: 1 app, 1 viewport)
01:00  Run walkthrough scorecard against all 4 apps
01:30  Refine Figma mockup based on cloud vision feedback
02:00  Dry-run full demo flow end-to-end
02:30  Sleep
```

---

## 6. Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DESIGN LAYER                             │
│  Figma Pro ──── MCP Server ──── OpenClaw MCP Adapter        │
│  (source of truth)              (figma transport)            │
└──────────────────────┬──────────────────────────────────────┘
                       │ export PNGs, read tokens
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                         │
│                                                               │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │  UX-lead    │───▶│ UX-vision    │    │ UX-vision      │  │
│  │  (Codex)    │    │ local (8B)   │    │ cloud (235B)   │  │
│  │             │───▶│ fast triage  │──▶ │ deep analysis  │  │
│  └──────┬──────┘    └──────────────┘    └────────────────┘  │
│         │                                                     │
│         │ spawns via OpenClaw subagent API                    │
└─────────┼───────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    ACTION LAYER                               │
│                                                               │
│  Linear (tickets) ◄── UX-lead ──► GitHub (PRs)              │
│       │                                │                      │
│       ▼                                ▼                      │
│  Coder-Next ◄──── coding-pipeline ────► Feature branch       │
│  (implement)         skill              (PR opened)           │
│                                                               │
└─────────────────────┬───────────────────────────────────────┘
                      │ PR triggers
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  VERIFICATION LAYER                           │
│                                                               │
│  Playwright ──► Screenshots ──► UX-vision-local              │
│  (navigate)     (capture)       (compare to Figma export)    │
│                                                               │
│  Pass? ──► Merge PR ──► Update baseline                      │
│  Fail? ──► Block PR ──► Comment with visual diff             │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   REPORTING LAYER                             │
│                                                               │
│  Notion (audit reports) ◄── UX-lead                          │
│  Slack (daily scorecard) ◄── ux-walkthrough cron             │
│  Linear (trend tracking) ◄── score history                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow for a Single Design Change

```
1. Figma design updated (manual or Figma Make)
2. Figma MCP webhook → OpenClaw detects change
3. UX-lead exports affected frames as PNG
4. UX-lead creates Linear ticket with Figma link
5. Coder-Next implements the design change
6. PR opened → Playwright screenshots new UI
7. UX-vision-local compares screenshot to Figma export
8. Score > threshold → PR approved → merge
9. New baseline saved
10. Next daily walkthrough confirms score improved
```

---

## 7. File & Directory Structure

```
workspace/
├── skills/
│   ├── ux-kickoff/
│   │   └── SKILL.md
│   ├── ux-regression/
│   │   └── SKILL.md
│   ├── ux-design-overhaul/
│   │   └── SKILL.md
│   └── ux-walkthrough/
│       └── SKILL.md
├── screenshots/
│   ├── baselines/
│   │   ├── lockn-score/
│   │   ├── lockn-logger/
│   │   ├── lockn-auth/
│   │   └── lockn-ai/
│   └── audits/
│       └── {date}/
├── figma-exports/
│   ├── lockn-score/
│   └── design-system/
└── docs/
    ├── ux-agent-system-architecture.md  ← this file
    └── ux-audit-reports/
```

---

## 8. Implementation Priority

| Phase | What | When | Effort |
|-------|------|------|--------|
| **Tonight** | Figma mockup + regression demo + scorecard | Now | 3h |
| **Week 1** | `ux-walkthrough` cron + `ux-regression` on PRs | Post-demo | 8h |
| **Week 2** | Figma MCP wired into OpenClaw adapter | +1 week | 4h |
| **Week 3** | `ux-kickoff` + `ux-design-overhaul` skills | +2 weeks | 12h |
| **Week 4** | Full pipeline: design → implement → verify loop | +3 weeks | 8h |

---

*This system turns UX from a manual bottleneck into a continuous, automated quality loop. The vision models are the eyes, Codex is the brain, and Figma is the canvas.*
