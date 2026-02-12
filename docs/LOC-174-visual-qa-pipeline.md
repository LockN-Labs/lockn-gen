# LOC-174: Visual QA Pipeline — Implementation Plan

## Overview

Automated screenshot regression testing using Playwright for capture and Qwen3-VL (8B, port 11434 via Ollama) for AI-powered visual analysis. Unlike pixel-diff tools (Percy, Applitools), we use a VLM to understand *semantic* visual changes — "the button moved" vs "a pixel shifted."

## Architecture

```
Deploy Pipeline
    │
    ▼
Playwright Test Suite (headless Chromium)
    │ captures screenshots per flow
    ▼
Screenshot Storage (git LFS or local dir)
    │
    ├──► Pixel Diff (Playwright built-in toHaveScreenshot)
    │        quick pass/fail gate
    │
    └──► Qwen3-VL Analysis (when pixel diff detects change)
             │ compare baseline vs current
             ▼
         Visual Diff Report (JSON + markdown)
             │
             ▼
         Deploy Gate (fail/warn/pass)
```

## Target Flows & Screenshots

### 1. LockN Score UI (`lockn-score/`)
- **URL:** Local dev or deployed Score frontend
- **Captures:**
  - Dashboard/home view (score display)
  - Score detail/breakdown view
- **Mask:** Dynamic score values, timestamps

### 2. LockN Platform Login (`lockn-ai-platform/web/`)
- **URL:** Keycloak login page
- **Captures:**
  - Login form (empty state)
  - Login form (error state)
  - Post-login redirect/landing
- **Mask:** Session tokens, CSRF fields

### 3. API Docs Pages (`lockn-ai-platform/swagger-specs/`)
- **URL:** Swagger/OpenAPI rendered docs
- **Captures:**
  - API docs landing page
  - Expanded endpoint example
- **Mask:** Version strings, timestamps

## Technical Design

### Playwright Configuration

```typescript
// visual-qa/playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    // Consistent rendering
    deviceScaleFactor: 1,
    colorScheme: 'light',
    locale: 'en-US',
    timezoneId: 'America/New_York',
  },
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01,  // 1% threshold for pixel diff
      animations: 'disabled',
      caret: 'hide',
    },
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
  ],
});
```

**Key Playwright best practices applied:**
- `animations: 'disabled'` — eliminates flaky diffs from CSS transitions
- `caret: 'hide'` — no blinking cursor artifacts
- Fixed viewport, scale factor, locale, timezone — deterministic renders
- `maxDiffPixelRatio: 0.01` — quick pixel gate before expensive VLM call
- Mask dynamic content via `page.evaluate()` before capture

### Qwen3-VL Integration

Two-phase analysis when pixel diff detects a change:

**Phase 1: Describe** — Send current screenshot alone
```
POST http://127.0.0.1:11434/api/chat
{
  "model": "qwen3-vl:8b",
  "messages": [{
    "role": "user",
    "content": "Describe this UI screenshot. List all visible elements, layout, colors, and any issues (misalignment, overflow, broken images).",
    "images": ["<base64_current>"]
  }]
}
```

**Phase 2: Compare** — Send baseline + current side by side
```
{
  "model": "qwen3-vl:8b",
  "messages": [{
    "role": "user",
    "content": "Compare these two UI screenshots. The first is the baseline (expected), the second is the current build. List all visual differences. For each difference, classify as: REGRESSION (broken/wrong), EXPECTED (intentional change), or COSMETIC (minor, non-breaking). Output JSON.",
    "images": ["<base64_baseline>", "<base64_current>"]
  }]
}
```

**Output format:**
```json
{
  "differences": [
    {
      "element": "Login button",
      "change": "Color changed from blue (#2563eb) to green (#16a34a)",
      "classification": "REGRESSION",
      "severity": "high",
      "location": "center, below form fields"
    }
  ],
  "overall_assessment": "FAIL",
  "summary": "1 regression detected: button color change"
}
```

### Baseline Storage Strategy

```
visual-qa/
├── baselines/
│   ├── score-dashboard.png
│   ├── score-detail.png
│   ├── platform-login-empty.png
│   ├── platform-login-error.png
│   ├── platform-post-login.png
│   ├── api-docs-landing.png
│   └── api-docs-endpoint.png
├── current/          # gitignored, generated each run
├── diffs/            # gitignored, pixel diff output
├── reports/          # gitignored, VLM analysis reports
├── tests/
│   ├── score.spec.ts
│   ├── platform-login.spec.ts
│   └── api-docs.spec.ts
├── lib/
│   ├── qwen-vl-client.ts    # Ollama API wrapper
│   ├── visual-analyzer.ts    # Orchestrates capture → diff → VLM
│   └── report-generator.ts   # Markdown + JSON reports
├── playwright.config.ts
└── package.json
```

- **Baselines in git** (not LFS for now — ~7 PNGs, <5MB total)
- Update baselines explicitly: `npx playwright test --update-snapshots`
- Current/diffs/reports regenerated each run, gitignored

### Deploy Pipeline Integration

```bash
#!/bin/bash
# visual-qa/run-visual-qa.sh

set -e

# 1. Capture screenshots via Playwright
npx playwright test --reporter=json

# 2. For any pixel-diff failures, run Qwen3-VL analysis
node lib/visual-analyzer.js

# 3. Check report for regressions
REGRESSIONS=$(jq '.differences[] | select(.classification == "REGRESSION")' reports/latest.json | wc -l)

if [ "$REGRESSIONS" -gt 0 ]; then
  echo "❌ Visual QA FAILED: $REGRESSIONS regression(s) detected"
  cat reports/latest.md
  exit 1
fi

echo "✅ Visual QA passed"
```

## Subtasks for Linear

| # | Title | Description | Estimate |
|---|-------|-------------|----------|
| 1 | **Scaffold visual-qa project** | Init npm project, install Playwright, create directory structure, playwright.config.ts | 1h |
| 2 | **Write Playwright test: Score UI** | score.spec.ts — navigate to Score UI, mask dynamic content, capture 2 screenshots | 2h |
| 3 | **Write Playwright test: Platform Login** | platform-login.spec.ts — login form empty/error/post-login, 3 screenshots | 2h |
| 4 | **Write Playwright test: API Docs** | api-docs.spec.ts — docs landing + expanded endpoint, 2 screenshots | 1h |
| 5 | **Build Qwen3-VL client** | qwen-vl-client.ts — Ollama API wrapper with image encoding, retry logic, structured JSON output parsing | 2h |
| 6 | **Build visual analyzer orchestrator** | visual-analyzer.ts — reads Playwright results, triggers VLM comparison for failures, generates report | 3h |
| 7 | **Build report generator** | report-generator.ts — JSON + markdown report, summary with pass/fail gate | 1h |
| 8 | **Generate initial baselines** | Run all tests with --update-snapshots, commit baselines to git | 30m |
| 9 | **Integration script + deploy hook** | run-visual-qa.sh, integrate with existing deploy pipeline | 1h |
| 10 | **End-to-end test of full pipeline** | Intentionally break UI, verify pipeline catches it, test baseline update flow | 2h |

**Total estimate:** ~15.5 hours

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| VLM hallucinations (false positives) | Pixel diff as first gate; VLM only runs on actual changes |
| Qwen3-VL 8B accuracy insufficient | Can escalate to qwen3-vl:235b-cloud for ambiguous cases |
| Screenshot flakiness (fonts, rendering) | Fixed viewport/locale/timezone, disabled animations, deterministic setup |
| Target apps not running during QA | Health check before capture; skip with warning if service unavailable |
| Ollama cold start latency | Pre-warm model before test suite runs |

## Dependencies

- Playwright npm package
- Ollama running on port 11434 with qwen3-vl:8b loaded
- Target services accessible (Score UI, Platform, API docs)
- Node.js 22+ (already available)
