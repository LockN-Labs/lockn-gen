#!/bin/bash
# OpenClaw Update - Phase 2: Analysis with Changelog Highlights
set -e

CURRENT=$(openclaw --version 2>/dev/null)
TARGET=$(npm view openclaw version 2>/dev/null)

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw Update Analysis - Phase 2"
echo "═══════════════════════════════════════════════════════════════"
echo "Current: v${CURRENT}"
echo "Target:  v${TARGET}"
echo ""

if [ "$CURRENT" = "$TARGET" ]; then
    echo "✅ Already on latest version"
    exit 0
fi

# Clone for analysis
ANALYSIS_DIR="/tmp/openclaw-analysis-$$"
echo "📥 Cloning OpenClaw repository..."
git clone --depth 200 --quiet https://github.com/openclaw/openclaw.git "$ANALYSIS_DIR"

cd "$ANALYSIS_DIR"

# Commit count
echo ""
echo "📊 Commit Summary:"
echo "───────────────────────────────────────────────────────────────"
if git rev-parse "v${CURRENT}" >/dev/null 2>&1; then
    COMMITS=$(git rev-list --count "v${CURRENT}..HEAD" 2>/dev/null || echo "?")
    echo "Total commits: ${COMMITS}"
else
    echo "⚠️  Tag v${CURRENT} not found"
fi

# Changelog highlights
echo ""
echo "📋 CHANGELOG HIGHLIGHTS:"
echo "═══════════════════════════════════════════════════════════════"

# Extract relevant changelog sections
awk '
    /^## [0-9]/ { 
        if (found) exit
        version = $2
        if (version ~ /^2026\.2\.[2-9]/ || version ~ /^2026\.2\.1[0-9]/) {
            found = 1
            print ""
            print "### " $0
        }
    }
    found && /^### / { print "" ; print $0 }
    found && /^- / { print $0 }
' CHANGELOG.md | head -80

echo ""
echo "═══════════════════════════════════════════════════════════════"

# Breaking changes check
echo ""
echo "🔍 BREAKING CHANGES CHECK:"
echo "───────────────────────────────────────────────────────────────"
BREAKING=$(grep -i "breaking" CHANGELOG.md | head -5)
if [ -n "$BREAKING" ]; then
    echo "⚠️  Found mentions of 'breaking':"
    echo "$BREAKING"
else
    echo "✅ No 'breaking' keyword found in changelog"
fi

# Default behavior changes
echo ""
echo "🔍 DEFAULT BEHAVIOR CHANGES:"
echo "───────────────────────────────────────────────────────────────"
DEFAULTS=$(grep -i "default\|now defaults\|changed.*default" CHANGELOG.md | head -5)
if [ -n "$DEFAULTS" ]; then
    echo "⚠️  Default behavior changes:"
    echo "$DEFAULTS"
else
    echo "✅ No default behavior changes noted"
fi

# Security fixes
echo ""
echo "🔒 SECURITY FIXES:"
echo "───────────────────────────────────────────────────────────────"
SECURITY=$(grep -i "security\|CVE\|CVSS\|harden\|vulnerability" CHANGELOG.md | head -10)
if [ -n "$SECURITY" ]; then
    echo "$SECURITY"
else
    echo "None explicitly mentioned"
fi

# Cron changes (important for us)
echo ""
echo "⏰ CRON-RELATED CHANGES:"
echo "───────────────────────────────────────────────────────────────"
CRON=$(grep -i "cron" CHANGELOG.md | head -10)
if [ -n "$CRON" ]; then
    echo "$CRON"
else
    echo "None"
fi

# New features
echo ""
echo "✨ NEW FEATURES:"
echo "───────────────────────────────────────────────────────────────"
git log --oneline "v${CURRENT}..HEAD" 2>/dev/null | grep -i "feat" | head -10 || echo "None found"

# Bug fixes
echo ""
echo "🐛 BUG FIXES:"
echo "───────────────────────────────────────────────────────────────"
git log --oneline "v${CURRENT}..HEAD" 2>/dev/null | grep -i "fix" | head -10 || echo "None found"

# Cleanup
rm -rf "$ANALYSIS_DIR"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "ANALYSIS COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Review the above highlights carefully."
echo "Reply 'proceed with stage' to continue, or 'abort' to cancel."
