# Visual QA Pipeline

**Automated Figma vs Implementation Comparison using Qwen3-VL**

## Quick Start

```bash
# Compare a single design vs implementation
ux-qa compare \
  --figma-key "ABC123" \
  --node-id "1:234" \
  --url "https://app.example.com/page"
```

## What it does

1. **Downloads** Figma design as PNG
2. **Screenshots** live implementation  
3. **Compares** using Qwen3-VL (local 8B → cloud 235B)
4. **Scores** 5 categories: Layout, Color, Typography, Spacing, Overall
5. **Creates** Linear tickets for failing issues

## Scoring

- **≥8.0/10:** ✅ PASS  
- **6.0-7.9:** ⚠️ CONDITIONAL
- **<6.0:** ❌ FAIL

## Files

- `SKILL.md` - Complete documentation and implementation
- `README.md` - This quick reference

## Usage Examples

See `SKILL.md` for full documentation, API reference, and integration examples.