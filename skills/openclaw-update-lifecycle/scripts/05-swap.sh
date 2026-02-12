#!/bin/bash
# OpenClaw Update - Phase 5: Swap (HUMAN APPROVED)
# DETACHED EXECUTION - survives gateway stop
set -e

GREEN_NPM="$HOME/.npm-global-green"
GREEN_STATE="$HOME/.openclaw-green"
BLUE_NPM="$HOME/.npm-global"
LOG_FILE="/tmp/openclaw-swap-$(date +%Y%m%d-%H%M%S).log"

# If not running detached, re-exec detached
if [ -z "$OPENCLAW_SWAP_DETACHED" ]; then
    echo "Starting detached swap process..."
    echo "Log file: ${LOG_FILE}"
    OPENCLAW_SWAP_DETACHED=1 nohup "$0" "$@" > "$LOG_FILE" 2>&1 &
    SWAP_PID=$!
    echo "Swap PID: $SWAP_PID"
    echo ""
    echo "Swap is running in background. Gateway will restart with new version."
    echo "Check log: tail -f ${LOG_FILE}"
    exit 0
fi

# === DETACHED EXECUTION STARTS HERE ===

exec > >(tee -a "$LOG_FILE") 2>&1

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw Blue-Green SWAP - Phase 5 (Detached)"
echo "Started: $(date)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Pre-swap verification
echo "Pre-swap checks..."
GREEN_VERSION=$(${GREEN_NPM}/bin/openclaw --version 2>/dev/null)
BLUE_VERSION=$(${BLUE_NPM}/bin/openclaw --version 2>/dev/null)
echo "BLUE:  v${BLUE_VERSION}"
echo "GREEN: v${GREEN_VERSION}"
echo ""

# Step 1: Stop GREEN
echo "1. Stopping GREEN service..."
systemctl --user stop openclaw-gateway-green.service 2>/dev/null || true
sleep 2

# Step 2: Stop BLUE
echo "2. Stopping BLUE service..."
systemctl --user stop openclaw-gateway.service
sleep 3

# Step 3: Archive BLUE
echo "3. Archiving BLUE package..."
BACKUP_NAME="openclaw.blue-backup-$(date +%Y%m%d)"
if [ -d "${BLUE_NPM}/lib/node_modules/openclaw" ]; then
    mv "${BLUE_NPM}/lib/node_modules/openclaw" \
       "${BLUE_NPM}/lib/node_modules/${BACKUP_NAME}"
    echo "   Archived to: ${BACKUP_NAME}"
fi

# Step 4: Promote GREEN
echo "4. Promoting GREEN to BLUE location..."
mv "${GREEN_NPM}/lib/node_modules/openclaw" \
   "${BLUE_NPM}/lib/node_modules/openclaw"

# Step 5: Update symlink
echo "5. Updating bin symlink..."
rm -f "${BLUE_NPM}/bin/openclaw"
ln -s "${BLUE_NPM}/lib/node_modules/openclaw/openclaw.mjs" \
      "${BLUE_NPM}/bin/openclaw"

# Step 6: Update systemd service version
echo "6. Updating systemd service version..."
NEW_VERSION=$(${BLUE_NPM}/bin/openclaw --version 2>/dev/null)
sed -i "s/OPENCLAW_SERVICE_VERSION=.*/OPENCLAW_SERVICE_VERSION=${NEW_VERSION}/" \
    "$HOME/.config/systemd/user/openclaw-gateway.service" 2>/dev/null || true
sed -i "s/Description=OpenClaw Gateway.*/Description=OpenClaw Gateway (v${NEW_VERSION})/" \
    "$HOME/.config/systemd/user/openclaw-gateway.service" 2>/dev/null || true
systemctl --user daemon-reload

# Step 7: Start BLUE (now new version)
echo "7. Starting BLUE service (new version)..."
systemctl --user start openclaw-gateway.service
sleep 5

# Step 8: Verify
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Post-swap verification..."
echo "───────────────────────────────────────────────────────────────"

echo -n "Service: "
if systemctl --user is-active --quiet openclaw-gateway.service; then
    echo "✅ Running"
else
    echo "❌ Failed to start"
    exit 1
fi

echo -n "Version: "
FINAL_VERSION=$(${BLUE_NPM}/bin/openclaw --version 2>/dev/null)
echo "v${FINAL_VERSION}"

echo -n "Health: "
sleep 2
HEALTH=$(curl -s http://127.0.0.1:18789/health 2>/dev/null | head -c 50)
if [ -n "$HEALTH" ]; then
    echo "✅ Responding"
else
    echo "⚠️  Checking..."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ SWAP COMPLETE: v${BLUE_VERSION} → v${FINAL_VERSION}"
echo "Finished: $(date)"
echo "═══════════════════════════════════════════════════════════════"

# Step 9: Cleanup
echo ""
echo "Cleaning up GREEN artifacts..."
rm -rf "${GREEN_NPM}"
rm -rf "${GREEN_STATE}"
rm -f "$HOME/.config/systemd/user/openclaw-gateway-green.service"
systemctl --user daemon-reload 2>/dev/null || true

echo "✅ Cleanup complete"
echo ""
echo "Old version archived at: ${BLUE_NPM}/lib/node_modules/${BACKUP_NAME}"
echo "Safe to delete after 7 days of stable operation."
