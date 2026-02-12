#!/bin/bash
# OpenClaw Update - Phase 3: Blue-Green Staging (FIXED)
# Uses isolated config + state directory for true parallel instances
set -e

TARGET=${1:-$(npm view openclaw version)}
GREEN_NPM="$HOME/.npm-global-green"
GREEN_STATE="$HOME/.openclaw-green"
GREEN_PORT=18810  # Well-spaced from 18789 (need 20+ gap for derived ports)
GREEN_CONFIG="${GREEN_STATE}/openclaw.json"

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw Blue-Green Staging - Phase 3"
echo "═══════════════════════════════════════════════════════════════"
echo "Target version: v${TARGET}"
echo "GREEN npm:      ${GREEN_NPM}"
echo "GREEN state:    ${GREEN_STATE}"
echo "GREEN port:     ${GREEN_PORT}"
echo ""

# Create green npm prefix
echo "📦 Creating GREEN npm environment..."
mkdir -p "${GREEN_NPM}/lib"
mkdir -p "${GREEN_NPM}/bin"

# Install new version
echo "📥 Installing openclaw@${TARGET} to GREEN..."
npm install -g "openclaw@${TARGET}" --prefix "${GREEN_NPM}" 2>&1 | tail -5

# Verify installation
if [ ! -f "${GREEN_NPM}/lib/node_modules/openclaw/openclaw.mjs" ]; then
    echo "❌ Installation failed"
    exit 1
fi
echo "✅ Installed: $(${GREEN_NPM}/bin/openclaw --version 2>/dev/null || echo 'version check failed')"

# Create green state directory with isolated config
echo ""
echo "📋 Creating GREEN state directory..."
mkdir -p "${GREEN_STATE}"
mkdir -p "${GREEN_STATE}/workspace"

# Create isolated config (copy and modify)
echo "🔧 Creating isolated config for port ${GREEN_PORT}..."
if [ -f "$HOME/.openclaw/openclaw.json" ]; then
    # Copy and modify the config
    jq ".gateway.port = ${GREEN_PORT} | .agents.defaults.workspace = \"${GREEN_STATE}/workspace\"" \
        "$HOME/.openclaw/openclaw.json" > "${GREEN_CONFIG}"
else
    # Create minimal config
    cat > "${GREEN_CONFIG}" << EOF
{
  "gateway": {
    "port": ${GREEN_PORT},
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    }
  },
  "agents": {
    "defaults": {
      "workspace": "${GREEN_STATE}/workspace"
    }
  }
}
EOF
fi

# Copy .env if exists
cp "$HOME/.openclaw/.env" "${GREEN_STATE}/" 2>/dev/null || true

# Create systemd service with proper env vars
echo ""
echo "🔧 Creating GREEN systemd service..."
cat > "$HOME/.config/systemd/user/openclaw-gateway-green.service" << EOF
[Unit]
Description=OpenClaw Gateway GREEN (v${TARGET} - Staged)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=${GREEN_NPM}/bin/openclaw gateway --port ${GREEN_PORT} --allow-unconfigured
Restart=on-failure
RestartSec=10
KillMode=process
Environment="HOME=${HOME}"
Environment="OPENCLAW_CONFIG_PATH=${GREEN_CONFIG}"
Environment="OPENCLAW_STATE_DIR=${GREEN_STATE}"
Environment="OPENCLAW_GATEWAY_PORT=${GREEN_PORT}"
Environment="OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}"
WorkingDirectory=${GREEN_STATE}

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload

# Start green service
echo ""
echo "🚀 Starting GREEN service..."
systemctl --user start openclaw-gateway-green.service
sleep 8

# Check status
if systemctl --user is-active --quiet openclaw-gateway-green.service; then
    echo "✅ GREEN service started successfully"
    GREEN_VERSION=$(${GREEN_NPM}/bin/openclaw --version 2>/dev/null)
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "✅ GREEN instance staged successfully!"
    echo ""
    echo "BLUE (Production): v$(openclaw --version) on port 18789"
    echo "GREEN (Staged):    v${GREEN_VERSION} on port ${GREEN_PORT}"
    echo ""
    echo "Both instances running in parallel."
    echo "═══════════════════════════════════════════════════════════════"
else
    echo "❌ GREEN service failed to start"
    journalctl --user -u openclaw-gateway-green.service -n 20 --no-pager
    exit 1
fi
