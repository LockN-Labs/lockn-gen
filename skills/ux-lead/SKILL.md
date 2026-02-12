# UX Lead Runbook

Orchestrates design-to-code validation using Figma MCP + implementation screenshots + Linear issue management.

## Metadata
- **Name:** ux-lead
- **Version:** 0.1.0
- **Owner:** sean@lockn.ai
- **Primary Model:** openai-codex/gpt-5.3-codex
- **Core Tools:** figma_get_figma_data, figma_download_figma_images, browser (Playwright), linear_*

## Required Inputs
- Figma file URL or `fileKey`
- Optional frame/node IDs (`node-id`)
- Implementation URL or local route for screenshots
- Linear team/project context

## Workflow A — Mockup extraction from Figma
1. Parse `fileKey` from Figma URL (`/design/<fileKey>/...` or `/file/<fileKey>/...`).
2. If comparing a specific frame, parse `node-id` and pass as `nodeId`.
3. Call `figma_get_figma_data` with `fileKey` (+ `nodeId` when available).
4. Extract:
   - Layout dimensions / spacing
   - Typography styles
   - Color tokens
   - Component names/variants
5. If raster/SVG assets are needed, call `figma_download_figma_images` for target nodes.

## Workflow B — Screenshot capture of implementation
1. Open target URL with `browser.open` / `browser.navigate`.
2. Set deterministic viewport (`browser.act` resize), then wait for stable UI state.
3. Capture screenshot with `browser.screenshot` (PNG, full page optional).
4. Save screenshot paths for comparison and ticket attachments.

## Workflow C — Visual diff/comparison
1. Compare Figma-derived target attributes vs implementation screenshot.
2. Check for drift categories:
   - Layout/spacing
   - Typography and hierarchy
   - Color and contrast
   - Component state mismatch
3. Assign severity:
   - **Critical:** broken flow / missing key component
   - **Major:** obvious spec mismatch affecting UX
   - **Minor:** polish differences
4. Produce a concise mismatch table in notes.

## Workflow E — Design Quality Gate (MANDATORY)
**Reference:** `docs/standards/design-review-quality-gate.md`

Every Figma design must pass vision model scoring before handoff to implementation.

1. Capture design frame as PNG (2x) via `figma_capture_screenshot` or `figma_get_component_image`.
2. Run **fail-fast pre-check** with `qwen3-vl-local` for rapid iteration.
3. Run **final authoritative gate** with `qwen3-vl-cloud` before any handoff.
4. Use standard scoring prompt from `docs/standards/design-review-quality-gate.md`.
5. Score using weighted sub-scores per dimension, then compute weighted composite.
6. Evaluate **final gate** composite score:
   - **≥ 9.81** → PASS, proceed to implementation
   - **9.50–9.80** → REVISE, iterate in Figma, re-score
   - **< 9.50** → REWORK, major design changes needed
   - If local/cloud composite delta >0.30, flag calibration issue in weekly memo
7. If not passing: identify lowest-scoring **sub-scores**, make targeted Figma edits, re-score.
8. Post a **Gate Card** (Linear + Slack) using the template in `design-review-quality-gate.md`: composite, 6 dimension scores, weakest sub-scores, verdict, links.
9. Log every iteration (score + feedback) in daily memory and as Linear/Figma comments.
10. **Do not hand off to implementation until final cloud gate score ≥ 9.81.**

## Workflow D — Ticket creation for UX issues found
1. Create or update a Linear issue with:
   - Repro steps + affected route
   - Expected (Figma reference) vs actual
   - Severity and acceptance criteria
2. Include links:
   - Figma URL (+ node id)
   - Screenshot evidence
3. Use labels like `ux`, `visual-regression`, `design-system` as appropriate.
4. Post summary comment to parent epic/task when running as part of QA sweep.

## Quality KPI Tracking (required)
- Track and report **first-pass pass rate** weekly:
  - Formula: `first_pass_rate = (# tickets PASS on first final-cloud gate) / (# tickets gated)`
  - Target: **>70%**
- Include KPI in weekly post to `#process-improvements` plus top recurring root causes.

## Guardrails
- Prefer frame-scoped comparisons (node-level) over whole-page subjective reviews.
- Always include objective evidence (dimensions, screenshots, component names).
- Don’t mark tickets Done without at least one verified screenshot pass.
