# Design Review Quality Gate — Vision Model Scoring

**Status:** Active  
**Owner:** Sean / Claws  
**Ticket:** [LOCKN-509](https://linear.app/lockn-ai/issue/LOCKN-509)  
**Created:** 2026-02-11

---

## Summary

Every Figma design iteration must pass a vision model quality gate before being considered complete. The vision agent scores designs on a 0.00–10.00 scale. **Minimum passing score: 9.81.**

## When This Applies

- Any new Figma screen or component design
- Any significant UI change to existing screens
- Before handing off designs for implementation
- During iterative design loops (score after each revision)

## Scoring Criteria

The vision model evaluates six dimensions and produces a **composite score** from weighted sub-scores.

| Dimension | Weight |
|-----------|--------|
| **Visual Styling** | 20% |
| **Platform Cohesiveness** | 25% |
| **Layout & Spacing** | 15% |
| **Typography** | 15% |
| **UI/UX Patterns** | 15% |
| **Accessibility** | 10% |

### Sub-score rubric (second-pass standard)

Each dimension is scored from **0.00–10.00** as a weighted sum of sub-scores.

#### 1) Visual Styling (20%)
- Color harmony & palette discipline — **35%**
- Contrast quality & depth balance — **25%**
- Visual hierarchy clarity — **25%**
- Polish/finish (iconography, edge consistency) — **15%**

#### 2) Platform Cohesiveness (25%)
- Design token compliance (colors/spacing/type) — **40%**
- Component pattern consistency — **35%**
- Brand alignment (LockN identity, dark-first) — **25%**

#### 3) Layout & Spacing (15%)
- Grid alignment and structure — **35%**
- Spacing rhythm consistency (4/8/12/etc) — **40%**
- Responsive readiness (breakpoint behavior) — **25%**

#### 4) Typography (15%)
- Hierarchy clarity (title/body/meta differentiation) — **40%**
- Readability (line length, line height, contrast) — **35%**
- Font consistency and semantic use — **25%**

#### 5) UI/UX Patterns (15%)
- Affordance clarity (what is clickable/tappable) — **35%**
- Interaction predictability (states, feedback) — **40%**
- Flow simplicity / cognitive load — **25%**

#### 6) Accessibility (10%)
- Contrast & legibility baseline — **45%**
- Touch target sizing / hit area safety — **30%**
- Keyboard/focus/screen-reader readiness cues — **25%**

### Formula

```text
DimensionScore = Σ(Subscore × SubWeight)
CompositeScore = Σ(DimensionScore × DimensionWeight)
PassThreshold = CompositeScore ≥ 9.81
```

All reported scores must include:
1) Dimension scores
2) Sub-scores per dimension
3) Final weighted composite (2 decimals)
4) Gap-to-threshold (`9.81 - CompositeScore`)


## Process

### Step 1: Capture Design
- Export the Figma frame/component as PNG (2x scale)
- Use `figma_get_component_image` or `figma_capture_screenshot` for the target node

### Step 2: Vision Model Review (two-stage)
1. **Pre-check (fast):** run `qwen3-vl-local` first for quick drift detection and immediate iteration loops.
2. **Final gate (authoritative):** run `qwen3-vl-cloud` before any handoff decision.
3. Use the standard scoring prompt (see below) in both passes.

### Step 3: Score Evaluation
- **Final gate score ≥ 9.81** → PASS — design approved for implementation
- **Final gate score 9.50–9.80** → REVISE — minor issues, iterate and re-score
- **Final gate score < 9.50** → REWORK — significant issues, needs design rethink
- If local/cloud delta >0.30 on composite, flag for calibration review in weekly memo

### Step 3.5: Gate Enforcement (operational)
Before handoff, reviewer must post a **Gate Card** in Linear comment + Slack update:
- Composite score (weighted)
- 6 dimension scores
- Lowest 2 sub-scores with remediation owners
- Pass/fail verdict
- Screenshot link and Figma node link

If FAIL/REVISE:
- Create or update explicit fix checklist items
- Assign owner + due date
- Re-run review after fix commit or Figma update

#### Gate Card Template (copy/paste)
Use this exact template in Linear comments and Slack updates:

```markdown
### Design Quality Gate Card
- Ticket: <LOCKN-###>
- Frame/Node: <Figma link>
- Review pass: <Pre-check local / Final cloud>
- Composite: <9.74>
- Gap to 9.81: <0.07>
- Verdict: <PASS | REVISE | REWORK>

#### Dimension Scores
- Visual Styling: <x.xx>
- Platform Cohesiveness: <x.xx>
- Layout & Spacing: <x.xx>
- Typography: <x.xx>
- UI/UX Patterns: <x.xx>
- Accessibility: <x.xx>

#### Weakest Sub-scores (Top 2)
1. <dimension.subscore> — <x.xx> — Owner: <name> — Fix by: <date>
2. <dimension.subscore> — <x.xx> — Owner: <name> — Fix by: <date>

#### Evidence
- Screenshot: <link/path>
- Comparison notes: <1-3 bullets>
```

### Step 4: Iterate
- If score < 9.81, review the per-dimension feedback
- Make targeted fixes in Figma
- Re-score until ≥ 9.81 is achieved
- Each iteration logged with score + feedback

## Standard Scoring Prompt

```
You are a senior UI/UX design reviewer for LockN, a sports tech platform with a dark-mode-first aesthetic.

Score this design on a 0.00 to 10.00 scale (two decimal places) across these dimensions:
1. Visual Styling (color harmony, contrast, hierarchy, polish)
2. Platform Cohesiveness (consistency with dark theme, modern sports tech brand)
3. Layout & Spacing (grid alignment, whitespace, balance)
4. Typography (hierarchy, readability, consistency)
5. UI/UX Patterns (affordances, interaction clarity, standard patterns)
6. Accessibility (contrast ratios, touch targets, readability)

For each dimension, provide:
- Score (0.00–10.00)
- Sub-scores using these weights:
  - Visual Styling: harmony 35%, contrast 25%, hierarchy 25%, polish 15%
  - Platform Cohesiveness: token compliance 40%, pattern consistency 35%, brand alignment 25%
  - Layout & Spacing: grid 35%, spacing rhythm 40%, responsive readiness 25%
  - Typography: hierarchy 40%, readability 35%, consistency 25%
  - UI/UX Patterns: affordance 35%, interaction predictability 40%, cognitive load 25%
  - Accessibility: contrast baseline 45%, touch targets 30%, keyboard/screen-reader readiness 25%
- 1-2 sentence justification
- Specific fix if any sub-score < 9.81

Then provide:
- Composite Score (weighted: Styling 20%, Cohesiveness 25%, Layout 15%, Typography 15%, UI/UX 15%, Accessibility 10%)
- Gap to threshold (9.81 - composite)
- PASS/REVISE/REWORK verdict (threshold: 9.81)
- Top 3 actionable improvements if not passing

Output format:
1) Human-readable summary
2) Strict JSON block with all dimension scores, sub-scores, and composite math

Be rigorous. 10.00 = best-in-class production design. 9.81 is a high bar — only award it when polish is genuinely excellent.
```

## Integration Points

- **UX-lead agent**: Runs this gate as mandatory Workflow E before implementation handoff
- **Iterative design loop**: Score → fix → re-score cycle until passing
- **Linear tickets**: Add Gate Card comment per iteration; auto-create fix tasks for sub-threshold areas
- **Figma comments**: Post score + feedback as comments on reviewed frames
- **Slack #ux-design**: Post pass/fail summary and link to Gate Card
- **Slack #process-improvements**: Post weekly trends and systemic improvement opportunities

## Operational Cadence

### Per-review (required)
- Gate Card posted
- Evidence attached (image + node link)
- Owner + deadline for remediation when score <9.81

### Weekly (required)
- Roll up last 7 days:
  - Pass rate
  - **First-pass pass rate** (`# of tickets passing on first gate attempt / # of tickets reviewed`)
  - Median composite score
  - Most common low sub-scores
  - Recurring root causes
- Publish one improvement memo to `#process-improvements` with 1-3 process changes

### Monthly (required)
- Recalibrate rubric weights if drift observed
- Compare model consistency (`qwen3-vl-cloud` final gate vs `qwen3-vl-local` pre-check deltas)
- Update this standard and UX runbook if needed
- Track KPI trend: **First-pass pass rate target >70%**

## Audit Trail

Every review produces a record:
- Timestamp
- Node/frame reviewed
- Score breakdown
- PASS/REVISE/REWORK verdict
- Iteration number

Store in daily memory log and as Linear comments on the relevant ticket.
