#!/bin/bash
# OpenClaw Update - Phase 1: Backup
set -e

VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="openclaw-full-${TIMESTAMP}-v${VERSION}.tar.gz"
BACKUP_PATH="$HOME/backups/${BACKUP_NAME}"
WIN_PATH="/mnt/s/Recovery/OpenClaw"

echo "═══════════════════════════════════════════════════════════════"
echo "OpenClaw Backup - Phase 1"
echo "═══════════════════════════════════════════════════════════════"

mkdir -p "$HOME/backups"
mkdir -p "$WIN_PATH" 2>/dev/null || true

echo "📦 Creating backup: ${BACKUP_NAME}"

tar -czf "$BACKUP_PATH" \
    -C "$HOME" \
    .openclaw \
    .npm-global/lib/node_modules/openclaw \
    .npm-global/bin/openclaw \
    .config/systemd/user/openclaw-gateway.service \
    2>/dev/null

SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
echo "✅ Backup created: ${BACKUP_PATH} (${SIZE})"

# Copy to Windows
if [ -d "$WIN_PATH" ]; then
    cp "$BACKUP_PATH" "$WIN_PATH/"
    echo "✅ Copied to Windows: ${WIN_PATH}/${BACKUP_NAME}"
fi

# Verify
if [ -f "$BACKUP_PATH" ] && [ $(stat -c%s "$BACKUP_PATH") -gt 100000000 ]; then
    echo "✅ Backup verified (>100MB)"
    echo "$BACKUP_PATH"
    exit 0
else
    echo "❌ Backup verification failed"
    exit 1
fi
