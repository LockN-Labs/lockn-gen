#!/bin/bash
# OpenClaw Update - Phase 4: Validation
set -e

GREEN_PORT=18810
GREEN_NPM="$HOME/.npm-global-green"

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw GREEN Validation - Phase 4"
echo "═══════════════════════════════════════════════════════════════"

PASS=0
FAIL=0

# Check 1: Service running
echo -n "1. Service status: "
if systemctl --user is-active --quiet openclaw-gateway-green.service; then
    echo "✅ Running"
    ((PASS++))
else
    echo "❌ Not running"
    ((FAIL++))
fi

# Check 2: Health endpoint
echo -n "2. Health endpoint: "
HEALTH=$(curl -s "http://127.0.0.1:${GREEN_PORT}/health" 2>/dev/null || echo "failed")
if echo "$HEALTH" | grep -q "ok\|healthy"; then
    echo "✅ Healthy"
    ((PASS++))
else
    echo "❌ Failed ($HEALTH)"
    ((FAIL++))
fi

# Check 3: Version
echo -n "3. Version check: "
VERSION=$(${GREEN_NPM}/bin/openclaw --version 2>/dev/null || echo "unknown")
TARGET=$(npm view openclaw version 2>/dev/null)
if [ "$VERSION" = "$TARGET" ]; then
    echo "✅ v${VERSION}"
    ((PASS++))
else
    echo "⚠️  v${VERSION} (expected v${TARGET})"
    ((FAIL++))
fi

# Check 4: Logs (no errors)
echo -n "4. Recent logs: "
ERRORS=$(journalctl --user -u openclaw-gateway-green.service --since "2 min ago" --no-pager 2>/dev/null | grep -i "error\|fatal\|crash" | wc -l)
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ No errors"
    ((PASS++))
else
    echo "⚠️  ${ERRORS} error(s) found"
    ((FAIL++))
fi

# Check 5: BLUE still running
echo -n "5. BLUE status: "
if systemctl --user is-active --quiet openclaw-gateway.service; then
    BLUE_VERSION=$(openclaw --version 2>/dev/null)
    echo "✅ Running (v${BLUE_VERSION})"
    ((PASS++))
else
    echo "⚠️  Not running"
    ((FAIL++))
fi

echo ""
echo "───────────────────────────────────────────────────────────────"
echo "Results: ${PASS} passed, ${FAIL} failed"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "✅ All checks passed - GREEN is ready for swap"
    echo ""
    echo "BLUE (Current): v$(openclaw --version) on port 18789"
    echo "GREEN (Staged): v${VERSION} on port ${GREEN_PORT}"
    echo ""
    echo "⚠️  Reply 'proceed with swap' to continue, or 'abort' to cancel."
    exit 0
else
    echo "❌ Validation failed - do not proceed with swap"
    exit 1
fi
