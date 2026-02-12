# UX Walkthrough - Daily UX Audit Skill

**Purpose:** Automated daily UX audits with screenshot capture, vision analysis, defect tracking, and Slack reporting.

## Overview

This skill performs comprehensive daily UX audits by:
1. Capturing screenshots of key pages/flows
2. Running vision model analysis for UX issues
3. Classifying findings by severity
4. Creating/updating Linear tickets for actionable defects
5. Posting daily summaries to Slack

## Audit Checklist

### Core UX Areas
- **Accessibility**: WCAG compliance, alt text, keyboard navigation, color contrast
- **Responsiveness**: Mobile/tablet/desktop layouts, breakpoint behavior
- **Broken States**: Error handling, loading states, empty states, 404s
- **Visual Consistency**: Typography, spacing, color usage, component alignment
- **Interaction**: Button states, form validation, micro-interactions
- **Performance**: Page load indicators, perceived performance

### Key Pages to Audit
- Homepage / Landing page
- Product/service pages
- Sign-up/login flows
- Dashboard/main app areas
- Checkout/payment flows
- Mobile responsive views
- Error pages (404, 500, etc.)

## Tools Required

- **browser**: Screenshot capture via Playwright
- **image**: Vision model analysis (Qwen3-VL local 8B)
- **linear_create_issue** / **linear_update_issue**: Defect tracking
- **message**: Slack reporting

## Severity Classification

### Critical (🔴 P1)
- Accessibility violations preventing usage
- Complete functional breakage
- Data loss or security issues
- Core user flows blocked

### Major (🟡 P2) 
- Significant usability issues
- Design system violations
- Poor mobile experience
- Performance degradation

### Minor (🟠 P3)
- Inconsistent styling
- Minor accessibility improvements
- Optimization opportunities
- Polish improvements

### Cosmetic (🔵 P4)
- Visual tweaks
- Nice-to-have improvements
- Non-critical alignment issues

## Implementation

### Daily Audit Process

```javascript
async function runDailyUXAudit() {
  const auditDate = new Date().toISOString().split('T')[0];
  const results = {
    date: auditDate,
    findings: [],
    screenshots: [],
    tickets: []
  };
  
  // 1. Capture screenshots of key pages
  const keyPages = [
    { name: 'Homepage', url: 'https://app.example.com/' },
    { name: 'Dashboard', url: 'https://app.example.com/dashboard' },
    { name: 'Mobile Homepage', url: 'https://app.example.com/', viewport: 'mobile' },
    // Add more pages as needed
  ];
  
  for (const page of keyPages) {
    const screenshot = await capturePageScreenshot(page);
    results.screenshots.push(screenshot);
    
    // 2. Run vision analysis
    const analysis = await analyzeScreenshotForUXIssues(screenshot);
    results.findings.push(...analysis.findings);
  }
  
  // 3. Process findings and create/update tickets
  await processFindings(results.findings);
  
  // 4. Post daily summary to Slack
  await postDailySummary(results);
  
  return results;
}

async function capturePageScreenshot(page) {
  // Use browser tool to capture screenshot
  const viewport = page.viewport === 'mobile' ? { width: 375, height: 812 } : { width: 1920, height: 1080 };
  
  await browser({
    action: 'open',
    targetUrl: page.url
  });
  
  if (page.viewport === 'mobile') {
    await browser({
      action: 'act',
      request: { kind: 'resize', width: 375, height: 812 }
    });
  }
  
  const screenshot = await browser({
    action: 'screenshot',
    fullPage: true,
    type: 'png'
  });
  
  return {
    name: page.name,
    url: page.url,
    viewport: page.viewport || 'desktop',
    screenshot: screenshot,
    timestamp: new Date().toISOString()
  };
}

async function analyzeScreenshotForUXIssues(screenshot) {
  const prompt = `
Analyze this screenshot for UX issues across these areas:

1. **Accessibility**: Missing alt text, poor contrast, keyboard navigation issues
2. **Responsiveness**: Layout problems, content overflow, mobile usability
3. **Broken States**: Error states, loading indicators, empty states
4. **Visual Consistency**: Typography, spacing, color usage, alignment
5. **Interaction Design**: Button states, form design, micro-interactions

For each issue found:
- Describe the specific problem
- Classify severity (Critical/Major/Minor/Cosmetic)
- Suggest actionable fix
- Provide element location if visible

Focus on actionable issues that impact user experience.
`;

  const analysis = await image({
    image: screenshot.screenshot,
    prompt: prompt,
    model: 'qwen3-vl-8b' // Local vision model
  });
  
  return parseVisionAnalysis(analysis);
}

function parseVisionAnalysis(analysisText) {
  // Parse the vision model response into structured findings
  const findings = [];
  
  // Extract issues from analysis text
  // This would parse the AI response to extract:
  // - Issue description
  // - Severity level
  // - Suggested fix
  // - Location/element details
  
  return { findings };
}

async function processFindings(findings) {
  for (const finding of findings) {
    if (finding.severity === 'Critical' || finding.severity === 'Major') {
      await createOrUpdateLinearTicket(finding);
    }
  }
}

async function createOrUpdateLinearTicket(finding) {
  // Check if similar ticket already exists
  const existingTickets = await linear_list_issues({
    query: finding.title.substring(0, 50),
    team: 'Design', // Adjust team as needed
    state: 'Todo,In Progress'
  });
  
  if (existingTickets.issues.length > 0) {
    // Update existing ticket with new findings
    const ticketId = existingTickets.issues[0].id;
    await linear_update_issue({
      id: ticketId,
      description: `${existingTickets.issues[0].description}\n\n**New finding (${new Date().toISOString().split('T')[0]}):**\n${finding.description}\n\nSuggested fix: ${finding.suggestedFix}`
    });
  } else {
    // Create new ticket
    await linear_create_issue({
      title: `[UX Audit] ${finding.title}`,
      description: `**Issue:** ${finding.description}\n\n**Severity:** ${finding.severity}\n\n**Location:** ${finding.location}\n\n**Suggested Fix:** ${finding.suggestedFix}\n\n**Found on:** ${new Date().toISOString().split('T')[0]}`,
      team: 'Design', // Adjust team as needed
      priority: getSeverityPriority(finding.severity),
      labels: ['ux-audit', 'accessibility', finding.severity.toLowerCase()]
    });
  }
}

function getSeverityPriority(severity) {
  const mapping = {
    'Critical': 1, // Urgent
    'Major': 2,    // High
    'Minor': 3,    // Normal
    'Cosmetic': 4  // Low
  };
  return mapping[severity] || 3;
}

async function postDailySummary(results) {
  const summary = generateSummaryMessage(results);
  
  await message({
    action: 'send',
    target: '#ux-audit', // Adjust channel as needed
    message: summary
  });
}

function generateSummaryMessage(results) {
  const { findings, screenshots } = results;
  const severityCount = {
    Critical: findings.filter(f => f.severity === 'Critical').length,
    Major: findings.filter(f => f.severity === 'Major').length,
    Minor: findings.filter(f => f.severity === 'Minor').length,
    Cosmetic: findings.filter(f => f.severity === 'Cosmetic').length
  };
  
  return `
## 🔍 Daily UX Audit Summary - ${results.date}

**Pages Audited:** ${screenshots.length}
**Total Findings:** ${findings.length}

**Severity Breakdown:**
🔴 Critical: ${severityCount.Critical}
🟡 Major: ${severityCount.Major} 
🟠 Minor: ${severityCount.Minor}
🔵 Cosmetic: ${severityCount.Cosmetic}

**Key Issues:**
${findings
  .filter(f => f.severity === 'Critical' || f.severity === 'Major')
  .slice(0, 5)
  .map(f => `• **${f.severity}**: ${f.title} - ${f.description.substring(0, 100)}...`)
  .join('\n')}

**Linear Tickets:** ${results.tickets.length} tickets created/updated

---
_Automated UX audit via OpenClaw ux-walkthrough skill_
`.trim();
}
```

## Cron Schedule

Run daily at 9:00 AM EST:
```
0 9 * * * /usr/bin/openclaw run skill ux-walkthrough
```

## Configuration

### Environment Variables
- `UX_AUDIT_BASE_URL`: Base URL to audit
- `UX_AUDIT_SLACK_CHANNEL`: Slack channel for reports (default: #ux-audit)
- `UX_AUDIT_LINEAR_TEAM`: Linear team for tickets (default: Design)

### Page Configuration
Create `/home/sean/.openclaw/workspace/skills/ux-walkthrough/pages.json`:
```json
{
  "pages": [
    {
      "name": "Homepage",
      "url": "https://app.example.com/",
      "priority": "high"
    },
    {
      "name": "Dashboard",
      "url": "https://app.example.com/dashboard", 
      "priority": "high",
      "authRequired": true
    },
    {
      "name": "Mobile Homepage",
      "url": "https://app.example.com/",
      "viewport": "mobile",
      "priority": "medium"
    }
  ]
}
```

## Usage

### Manual Execution
```bash
openclaw run skill ux-walkthrough
```

### Cron Setup
```bash
# Add to crontab
crontab -e

# Add line:
0 9 * * * /usr/bin/openclaw run skill ux-walkthrough
```

## Output

- Daily Slack summary with findings count and key issues
- Screenshots saved to `/tmp/ux-audit-YYYY-MM-DD/`
- Linear tickets for Critical/Major issues
- Audit log in `/var/log/openclaw/ux-walkthrough.log`

## Monitoring

- Check Slack channel for daily reports
- Monitor Linear team for new UX tickets
- Review logs for any execution errors
- Weekly review of cosmetic findings for batch processing

---

**Last Updated:** 2026-02-10
**Owner:** UX/Design Team
**Dependencies:** browser, image (Qwen3-VL), linear, message tools