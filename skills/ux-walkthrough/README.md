# UX Walkthrough Skill

Daily automated UX audits with screenshot capture, vision analysis, and defect tracking.

## Quick Start

1. **Configure pages**: Edit `pages.json` with your target URLs
2. **Set environment variables**:
   ```bash
   export UX_AUDIT_BASE_URL="https://your-app.com"
   export UX_AUDIT_SLACK_CHANNEL="#ux-audit"
   export UX_AUDIT_LINEAR_TEAM="Design"
   ```
3. **Test manually**: `openclaw run skill ux-walkthrough`
4. **Schedule daily**: Add to crontab for 9 AM daily runs

## What It Does

✅ **Screenshots**: Captures key pages in desktop & mobile views  
✅ **AI Analysis**: Uses Qwen3-VL to identify UX issues  
✅ **Severity Classification**: Critical → Cosmetic ranking  
✅ **Linear Integration**: Auto-creates tickets for actionable defects  
✅ **Slack Reports**: Daily summary with findings breakdown  

## Audit Focus

- **Accessibility**: WCAG compliance, contrast, keyboard navigation
- **Responsiveness**: Mobile/tablet layouts, breakpoints
- **Broken States**: Errors, loading, empty states
- **Visual Consistency**: Typography, spacing, alignment
- **Performance**: Load states, perceived performance

## Output

- **Slack**: Daily summary in configured channel
- **Linear**: Tickets for Critical/Major issues only
- **Screenshots**: Saved to `/tmp/ux-audit-YYYY-MM-DD/`
- **Logs**: Execution details in `/var/log/openclaw/`

## Customization

- **Pages**: Edit `pages.json` to change audit targets
- **Severity Thresholds**: Modify `getSeverityPriority()` in SKILL.md
- **Slack Format**: Customize `generateSummaryMessage()`
- **Vision Prompts**: Update `analyzeScreenshotForUXIssues()` prompt

## Monitoring

Check these daily:
- Slack channel receives summary
- Linear tickets created for major issues  
- No execution errors in logs
- Screenshots captured successfully

---

**Created**: 2026-02-10  
**Issue**: LOC-396  
**Dependencies**: browser, image (Qwen3-VL), linear, message