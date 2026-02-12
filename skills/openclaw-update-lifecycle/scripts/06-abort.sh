#!/bin/bash
# OpenClaw Update - Abort (cleanup GREEN without swapping)
set -e

GREEN_NPM="$HOME/.npm-global-green"
GREEN_STATE="$HOME/.openclaw-green"

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw Update ABORT - Cleanup"
echo "═══════════════════════════════════════════════════════════════"

# Stop GREEN if running
echo "Stopping GREEN service..."
systemctl --user stop openclaw-gateway-green.service 2>/dev/null || true
systemctl --user disable openclaw-gateway-green.service 2>/dev/null || true

# Remove GREEN artifacts
echo "Removing GREEN artifacts..."
rm -rf "${GREEN_NPM}"
rm -rf "${GREEN_STATE}"
rm -f "$HOME/.config/systemd/user/openclaw-gateway-green.service"
systemctl --user daemon-reload

# Verify BLUE still running
echo ""
echo "Verifying BLUE is unaffected..."
if systemctl --user is-active --quiet openclaw-gateway.service; then
    VERSION=$(openclaw --version 2>/dev/null)
    echo "✅ BLUE still running: v${VERSION}"
else
    echo "⚠️  BLUE not running - starting..."
    systemctl --user start openclaw-gateway.service
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Abort complete - BLUE unchanged, GREEN removed"
echo "═══════════════════════════════════════════════════════════════"
