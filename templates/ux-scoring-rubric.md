# UX Design Scoring Rubric v1.0

**Gate threshold: 9.81 / 10**
**Internal target: 9.85+ (safety margin)**

## Weighted Categories

| # | Category | Weight | Description | Score Range |
|---|----------|--------|-------------|-------------|
| 1 | Information Hierarchy | 22% | Type scale separation, visual weight distribution, scanability of key metrics vs metadata | 1–10 |
| 2 | Operational Clarity | 20% | Alert urgency cueing, action affordances, severity tiers, SLA visibility | 1–10 |
| 3 | Visual Consistency & Grid | 15% | Spacing rhythm (8pt grid), alignment, consistent component patterns across panels | 1–10 |
| 4 | Readability & Density | 13% | Row-level tracking, contrast ratios, information density balance, whitespace | 1–10 |
| 5 | Status Semantics & Accessibility | 12% | Color + icon + text redundancy for states, WCAG contrast, screen reader compatibility | 1–10 |
| 6 | Interaction Affordance | 10% | Clickable targets, hover/focus states, CTA visibility, filtering/sorting access | 1–10 |
| 7 | Responsiveness & Scalability | 8% | Layout adaptability, overflow handling, data scaling (empty/full states) | 1–10 |

## Scoring Formula

```
Total = Σ (category_score × weight)
```

## Per-Category Minimum Targets (to guarantee >9.81)

| Category | Minimum Score |
|----------|--------------|
| Information Hierarchy | 9.8 |
| Operational Clarity | 9.9 |
| Visual Consistency & Grid | 9.7 |
| Readability & Density | 9.7 |
| Status Semantics & Accessibility | 9.8 |
| Interaction Affordance | 9.6 |
| Responsiveness & Scalability | 9.6 |

**Computed floor with these minimums: ~9.81**

## Scoring Guidelines

### 10.0 (Exceptional)
- Zero issues found in the category
- Exceeds best practices (e.g., innovative interaction patterns)
- Would serve as a reference example

### 9.5–9.9 (Excellent)
- Minor polish items only (e.g., 1px alignment, slight spacing inconsistency)
- All critical patterns implemented correctly
- Passes all accessibility checks

### 9.0–9.4 (Good)
- A few noticeable issues that affect experience but not usability
- Missing one recommended pattern (e.g., no sparklines, missing sort presets)

### 8.0–8.9 (Needs Work)
- Multiple issues affecting usability or scanability
- Missing required patterns (e.g., no severity tiers in alerts)
- Does NOT pass gate

### Below 8.0 (Significant Issues)
- Structural problems (clipping, overflow, broken layout)
- Missing accessibility fundamentals
- Requires redesign of affected sections

## Gate Rules

1. **Total weighted score must be ≥ 9.81** to pass
2. **No single category below 9.0** (hard floor)
3. If gate fails, list specific deltas needed per category
4. Maximum 3 iteration passes before escalation to human review
5. Each pass must improve total score (no regressions)

## Review Process

1. Capture screenshot at 2× scale
2. Pull component metadata from Figma
3. Score each category with specific findings
4. Compute weighted total
5. If < 9.81: identify fixes, apply in Figma, re-score
6. If ≥ 9.81: post scorecard + before/after to `#ux-design`

## Output Template

```
## UX Scorecard — [Component/Page Name]

| Category | Weight | Score | Weighted | Status |
|----------|--------|-------|----------|--------|
| Info Hierarchy | 22% | X.X | X.XX | ✅/❌ |
| Operational Clarity | 20% | X.X | X.XX | ✅/❌ |
| Visual Consistency | 15% | X.X | X.XX | ✅/❌ |
| Readability & Density | 13% | X.X | X.XX | ✅/❌ |
| Status Semantics | 12% | X.X | X.XX | ✅/❌ |
| Interaction Affordance | 10% | X.X | X.XX | ✅/❌ |
| Responsiveness | 8% | X.X | X.XX | ✅/❌ |
| **TOTAL** | **100%** | | **X.XX** | **✅/❌** |

Gate: X.XX / 9.81 — PASS / FAIL
```
