# UX Regression - Visual Regression Testing Skill

**Purpose:** Automated visual regression testing using Playwright screenshots with diff analysis and defect reporting.

## Overview

This skill provides a complete workflow for visual regression testing:

1. **Baseline Capture**: Generate screenshot baselines using the browser tool (Playwright)
2. **Comparison Testing**: Capture new screenshots and compare against baselines
3. **Diff Analysis**: Generate pixel-level differences with threshold scoring
4. **Defect Reports**: Create machine-readable JSON reports of regressions
5. **Linear Integration**: Auto-create tickets for regressions above threshold
6. **CI/PR Integration**: Provide artifacts and exit codes for pipeline integration

## Parameters

### Required
- `target_urls`: Array of URLs to test (JSON array or comma-separated)
- `test_name`: Identifier for this test run (used in filenames and reports)

### Optional
- `baseline_mode`: `true` to capture baselines instead of testing (default: `false`)
- `threshold`: Pixel difference threshold percentage (default: `0.5`)
- `create_tickets`: Auto-create Linear tickets for failures (default: `true`)
- `team`: Linear team for ticket creation (default: auto-detect)
- `viewport_width`: Browser viewport width (default: `1920`)
- `viewport_height`: Browser viewport height (default: `1080`)
- `wait_timeout`: Wait time after page load (ms) (default: `2000`)
- `output_dir`: Directory for artifacts (default: `./regression-artifacts`)

## Usage

This is an agent-executed workflow — not a standalone CLI tool. Agents follow these steps using OpenClaw tools (browser, image, linear_*).

### Modes
- **Baseline capture**: Agent screenshots target URLs and saves as baselines
- **Regression test**: Agent compares new screenshots against saved baselines
- **CI integration**: Can be triggered by PR events via cron/webhook

## Implementation

### Baseline Capture Workflow

```javascript
async function captureBaselines(urls, testName, options = {}) {
  const results = [];
  const outputDir = path.join(options.outputDir || './regression-artifacts', testName);
  
  // Ensure output directory exists
  await fs.mkdir(outputDir, { recursive: true });
  
  for (const [index, url] of urls.entries()) {
    // Use browser tool to capture screenshot
    const screenshotResult = await browser({
      action: "open",
      targetUrl: url
    });
    
    // Wait for page to stabilize
    await browser({
      action: "act",
      request: {
        kind: "wait",
        timeMs: options.waitTimeout || 2000
      }
    });
    
    // Resize viewport if needed
    if (options.viewportWidth || options.viewportHeight) {
      await browser({
        action: "act",
        request: {
          kind: "resize",
          width: options.viewportWidth || 1920,
          height: options.viewportHeight || 1080
        }
      });
    }
    
    // Take screenshot
    const screenshot = await browser({
      action: "screenshot",
      type: "png",
      fullPage: true
    });
    
    const filename = `baseline-${index.toString().padStart(3, '0')}-${sanitizeFilename(url)}.png`;
    const filepath = path.join(outputDir, filename);
    
    // Save baseline image
    await fs.writeFile(filepath, screenshot.data, 'base64');
    
    results.push({
      url,
      index,
      filename,
      filepath,
      timestamp: new Date().toISOString()
    });
  }
  
  // Save baseline metadata
  const metadata = {
    testName,
    timestamp: new Date().toISOString(),
    viewport: {
      width: options.viewportWidth || 1920,
      height: options.viewportHeight || 1080
    },
    baselines: results
  };
  
  await fs.writeFile(
    path.join(outputDir, 'baselines.json'),
    JSON.stringify(metadata, null, 2)
  );
  
  return results;
}
```

### Regression Testing Workflow

```javascript
async function runRegressionTest(urls, testName, options = {}) {
  const outputDir = path.join(options.outputDir || './regression-artifacts', testName);
  const threshold = options.threshold || 0.5;
  
  // Load baseline metadata
  const baselineMetadata = JSON.parse(
    await fs.readFile(path.join(outputDir, 'baselines.json'), 'utf8')
  );
  
  const regressions = [];
  const results = [];
  
  for (const [index, url] of urls.entries()) {
    // Capture new screenshot
    await browser({
      action: "open",
      targetUrl: url
    });
    
    await browser({
      action: "act",
      request: {
        kind: "wait",
        timeMs: options.waitTimeout || 2000
      }
    });
    
    if (options.viewportWidth || options.viewportHeight) {
      await browser({
        action: "act",
        request: {
          kind: "resize",
          width: options.viewportWidth || 1920,
          height: options.viewportHeight || 1080
        }
      });
    }
    
    const screenshot = await browser({
      action: "screenshot",
      type: "png",
      fullPage: true
    });
    
    const testFilename = `test-${index.toString().padStart(3, '0')}-${sanitizeFilename(url)}.png`;
    const testFilepath = path.join(outputDir, testFilename);
    
    // Save test image
    await fs.writeFile(testFilepath, screenshot.data, 'base64');
    
    // Find corresponding baseline
    const baseline = baselineMetadata.baselines.find(b => b.index === index);
    if (!baseline) {
      throw new Error(`No baseline found for URL ${url} at index ${index}`);
    }
    
    // Generate diff using pixelmatch or similar
    const diffResult = await generateDiff(
      path.join(outputDir, baseline.filename),
      testFilepath,
      path.join(outputDir, `diff-${index.toString().padStart(3, '0')}.png`)
    );
    
    const result = {
      url,
      index,
      baseline: baseline.filename,
      test: testFilename,
      diff: `diff-${index.toString().padStart(3, '0')}.png`,
      pixelsDifferent: diffResult.pixelsDifferent,
      totalPixels: diffResult.totalPixels,
      differencePercentage: (diffResult.pixelsDifferent / diffResult.totalPixels) * 100,
      passed: (diffResult.pixelsDifferent / diffResult.totalPixels) * 100 < threshold,
      timestamp: new Date().toISOString()
    };
    
    results.push(result);
    
    if (!result.passed) {
      regressions.push(result);
    }
  }
  
  const report = {
    testName,
    timestamp: new Date().toISOString(),
    threshold,
    totalTests: results.length,
    passed: results.filter(r => r.passed).length,
    failed: results.filter(r => !r.passed).length,
    results,
    regressions
  };
  
  // Save test report
  await fs.writeFile(
    path.join(outputDir, 'regression-report.json'),
    JSON.stringify(report, null, 2)
  );
  
  return report;
}
```

### Diff Generation

```javascript
async function generateDiff(baselinePath, testPath, outputPath) {
  const PNG = require('pngjs').PNG;
  const pixelmatch = require('pixelmatch');
  
  const baseline = PNG.sync.read(await fs.readFile(baselinePath));
  const test = PNG.sync.read(await fs.readFile(testPath));
  
  const { width, height } = baseline;
  const diff = new PNG({ width, height });
  
  const pixelsDifferent = pixelmatch(
    baseline.data,
    test.data,
    diff.data,
    width,
    height,
    {
      threshold: 0.1,
      includeAA: false,
      diffColor: [255, 0, 0], // Red for differences
      diffColorAlt: [255, 255, 0] // Yellow for anti-aliasing
    }
  );
  
  // Save diff image
  await fs.writeFile(outputPath, PNG.sync.write(diff));
  
  return {
    pixelsDifferent,
    totalPixels: width * height,
    width,
    height
  };
}
```

### Linear Integration

```javascript
async function createRegressionTickets(report, options = {}) {
  const tickets = [];
  
  for (const regression of report.regressions) {
    const title = `Visual regression detected: ${regression.url}`;
    const description = `# Visual Regression Report

**Test Run:** ${report.testName}
**URL:** ${regression.url}
**Difference:** ${regression.differencePercentage.toFixed(2)}% (threshold: ${report.threshold}%)
**Pixels Changed:** ${regression.pixelsDifferent.toLocaleString()} / ${regression.totalPixels.toLocaleString()}

## Artifacts

- Baseline: \`${regression.baseline}\`
- Test Screenshot: \`${regression.test}\`
- Diff Image: \`${regression.diff}\`

## Next Steps

1. Review the diff image to identify the visual changes
2. Determine if the change is intentional or a regression
3. If intentional: Update baseline with \`ux-regression --baseline-mode\`
4. If regression: Investigate and fix the underlying cause

*Auto-generated by UX Regression Testing*
`;

    try {
      const ticket = await linear_create_issue({
        title,
        description,
        team: options.team || await detectTeam(),
        labels: ['visual-regression', 'automated'],
        priority: 2, // High priority
        project: 'QA Testing'
      });
      
      tickets.push({
        regression,
        ticket: ticket.id,
        url: ticket.url
      });
      
    } catch (error) {
      console.error(`Failed to create ticket for ${regression.url}:`, error);
    }
  }
  
  return tickets;
}
```

### CI/PR Pipeline Integration

```javascript
async function generateCiArtifacts(report, outputDir) {
  // Generate JUnit XML for CI systems
  const junitXml = generateJunitXml(report);
  await fs.writeFile(path.join(outputDir, 'junit-results.xml'), junitXml);
  
  // Generate markdown summary for PR comments
  const markdownSummary = generateMarkdownSummary(report);
  await fs.writeFile(path.join(outputDir, 'summary.md'), markdownSummary);
  
  // Generate GitHub Actions annotations
  const annotations = generateAnnotations(report);
  await fs.writeFile(path.join(outputDir, 'annotations.json'), JSON.stringify(annotations, null, 2));
  
  // Set appropriate exit code
  return report.failed > 0 ? 1 : 0;
}

function generateMarkdownSummary(report) {
  let summary = `# 📸 Visual Regression Test Results

**Test:** ${report.testName}  
**Timestamp:** ${report.timestamp}  
**Threshold:** ${report.threshold}%  

## Summary
- ✅ **Passed:** ${report.passed}
- ❌ **Failed:** ${report.failed}
- 📊 **Total:** ${report.totalTests}

`;

  if (report.regressions.length > 0) {
    summary += `## 🚨 Regressions Detected

| URL | Difference | Status |
|-----|------------|--------|
`;
    
    for (const regression of report.regressions) {
      summary += `| ${regression.url} | ${regression.differencePercentage.toFixed(2)}% | ❌ Failed |\n`;
    }
    
    summary += `
## 📁 Artifacts

Diff images and detailed reports are available in the \`regression-artifacts\` directory.

`;
  }

  return summary;
}
```

## Configuration

### Environment Variables
- `UX_REGRESSION_THRESHOLD`: Default threshold percentage
- `UX_REGRESSION_OUTPUT_DIR`: Default output directory
- `LINEAR_TEAM`: Default Linear team for ticket creation
- `UX_REGRESSION_VIEWPORT`: Default viewport (format: "1920x1080")

### Config File (optional)
Create `.ux-regression.json` in project root:

```json
{
  "threshold": 0.5,
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "waitTimeout": 2000,
  "outputDir": "./regression-artifacts",
  "linear": {
    "team": "Frontend",
    "project": "QA Testing",
    "labels": ["visual-regression", "automated"]
  },
  "urls": {
    "critical": [
      "https://app.example.com/login",
      "https://app.example.com/dashboard"
    ],
    "marketing": [
      "https://example.com",
      "https://example.com/pricing"
    ]
  }
}
```

## Error Handling

- Invalid URLs: Skip and log warning
- Missing baselines: Fail with helpful error message
- Screenshot failures: Retry up to 3 times with exponential backoff
- Network timeouts: Configure reasonable timeouts and retry logic
- Linear API failures: Log error but continue execution

## File Structure

```
regression-artifacts/
├── {test-name}/
│   ├── baselines.json              # Baseline metadata
│   ├── baseline-001-example.png    # Baseline screenshots
│   ├── test-001-example.png        # Test screenshots
│   ├── diff-001.png               # Diff images
│   ├── regression-report.json      # Test results
│   ├── junit-results.xml          # CI integration
│   ├── summary.md                 # PR comment
│   └── annotations.json           # GitHub Actions
```

## Dependencies

Required packages:
- `pixelmatch`: Fast pixel-level image comparison
- `pngjs`: PNG image manipulation
- `playwright`: Browser automation (via browser tool)
- Standard Node.js modules: `fs/promises`, `path`

Install via: `npm install pixelmatch pngjs`

## Best Practices

1. **Stable Baselines**: Capture baselines on stable, production-like environments
2. **Consistent Timing**: Use sufficient wait times for dynamic content
3. **Selective Testing**: Test critical user journeys, not every page
4. **Threshold Tuning**: Start with conservative thresholds (0.1-0.5%)
5. **Regular Updates**: Update baselines when intentional changes are made
6. **CI Integration**: Run on every PR but don't block for minor differences
7. **Artifact Management**: Clean up old artifacts to prevent disk bloat

## Troubleshooting

### Common Issues

**High False Positives**: Lower threshold or increase wait timeout
**Missing Diffs**: Check file permissions and disk space
**Slow Execution**: Reduce viewport size or test fewer URLs
**Baseline Drift**: Regularly refresh baselines on stable builds

### Debug Mode

Add `--debug` flag for verbose logging:
```bash
ux-regression --debug --target-urls "https://example.com" --test-name "debug-test"
```

## Examples

### Basic Usage
```bash
# First time: capture baselines
ux-regression --baseline-mode --target-urls "https://myapp.com,https://myapp.com/about" --test-name "smoke-test"

# Run regression test
ux-regression --target-urls "https://myapp.com,https://myapp.com/about" --test-name "smoke-test"
```

### Advanced Configuration
```bash
ux-regression \
  --target-urls "https://staging.myapp.com/dashboard,https://staging.myapp.com/profile" \
  --test-name "pr-1234" \
  --threshold 0.8 \
  --viewport-width 1440 \
  --viewport-height 900 \
  --wait-timeout 3000 \
  --create-tickets false \
  --output-dir "./artifacts/visual-tests"
```

### CI Pipeline Example

```yaml
name: Visual Regression Tests

on:
  pull_request:
    paths: ['frontend/**', 'styles/**']

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm install pixelmatch pngjs
        
      - name: Run visual regression tests
        run: |
          # Deploy to staging or use existing staging URL
          STAGING_URL="https://pr-${{ github.event.number }}.staging.myapp.com"
          
          # Run regression test
          ux-regression \
            --target-urls "$STAGING_URL,$STAGING_URL/dashboard" \
            --test-name "pr-${{ github.event.number }}" \
            --create-tickets false \
            --output-dir "./artifacts"
            
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: visual-regression-artifacts
          path: ./artifacts
          
      - name: Comment PR
        uses: actions/github-script@v6
        if: failure()
        with:
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('./artifacts/pr-${{ github.event.number }}/summary.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: summary
            });
```

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-02-10  
**Dependencies**: pixelmatch, pngjs, browser tool (Playwright)