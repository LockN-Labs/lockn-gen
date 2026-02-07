#!/usr/bin/env bash
# deploy.sh - Master deployment orchestrator
# Runs: regression → promote → smoke → rollback on failure
set -euo pipefail

SERVICE="${1:-}"
IMAGE_TAG="${2:-}"

if [[ -z "$SERVICE" || -z "$IMAGE_TAG" ]]; then
  echo "Usage: $0 <service> <image_tag>" >&2
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$ROOT_DIR/scripts"
STATE_DIR="${DEPLOY_STATE_DIR:-$ROOT_DIR/state}"
SLACK_CHANNEL="${SLACK_CHANNEL:-}"
SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

mkdir -p "$STATE_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
log_step() { log "=== $* ==="; }

announce() {
  local msg="$1"
  local color="${2:-good}"  # good=green, warning=yellow, danger=red
  
  if [[ -n "$SLACK_WEBHOOK_URL" ]]; then
    curl -sS -X POST "$SLACK_WEBHOOK_URL" \
      -H 'Content-Type: application/json' \
      -d "{\"attachments\":[{\"color\":\"$color\",\"text\":\"$msg\"}]}" >/dev/null || true
  fi
  log "$msg"
}

save_state() {
  local status="$1"
  local notes="${2:-}"
  cat > "$STATE_DIR/$SERVICE.json" <<EOF
{
  "service": "$SERVICE",
  "image_tag": "$IMAGE_TAG",
  "status": "$status",
  "timestamp": "$(date -Iseconds)",
  "notes": "$notes"
}
EOF
}

# Track overall result
RESULT="success"
NOTES=""

cleanup() {
  if [[ "$RESULT" != "success" ]]; then
    save_state "failed" "$NOTES"
  fi
}
trap cleanup EXIT

log_step "Starting deployment: $SERVICE → $IMAGE_TAG"
announce ":rocket: Starting deployment: \`$SERVICE\` → \`$IMAGE_TAG\`" "warning"

# Step 1: Pre-deploy regression tests on Test environment
log_step "Step 1: Regression tests (Test environment)"
REGRESSION_OUTPUT=$("$SCRIPTS_DIR/regression.sh" "$SERVICE" 2>&1) || {
  RESULT="failed"
  NOTES="Regression tests failed"
  announce ":x: Deployment FAILED: \`$SERVICE\` - Regression tests failed\n\`\`\`$REGRESSION_OUTPUT\`\`\`" "danger"
  exit 1
}
log "Regression tests passed"
echo "$REGRESSION_OUTPUT"

# Step 2: Blue/green promotion
log_step "Step 2: Promoting to production (blue/green swap)"
PROMOTE_OUTPUT=$("$SCRIPTS_DIR/promote.sh" "$SERVICE" "$IMAGE_TAG" 2>&1) || {
  RESULT="failed"
  NOTES="Promotion failed: $PROMOTE_OUTPUT"
  announce ":x: Deployment FAILED: \`$SERVICE\` - Promotion failed\n\`\`\`$PROMOTE_OUTPUT\`\`\`" "danger"
  exit 1
}
log "Promotion complete"
echo "$PROMOTE_OUTPUT"

# Step 3: Post-deploy smoke tests on Production
log_step "Step 3: Smoke tests (Production)"
SMOKE_OUTPUT=$("$SCRIPTS_DIR/smoke.sh" "$SERVICE" 2>&1)
SMOKE_RESULT=$?

# Parse smoke test result
SMOKE_PASSED=$(echo "$SMOKE_OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('true' if d.get('pass') else 'false')" 2>/dev/null || echo "false")

if [[ "$SMOKE_PASSED" != "true" || $SMOKE_RESULT -ne 0 ]]; then
  log "Smoke tests FAILED - initiating rollback"
  
  # Step 4: Rollback on failure
  log_step "Step 4: Rolling back"
  ROLLBACK_OUTPUT=$("$SCRIPTS_DIR/rollback.sh" "$SERVICE" 2>&1) || {
    RESULT="failed"
    NOTES="Smoke tests failed AND rollback failed"
    announce ":rotating_light: CRITICAL: \`$SERVICE\` - Smoke failed AND rollback failed!\n\`\`\`$ROLLBACK_OUTPUT\`\`\`" "danger"
    exit 1
  }
  
  RESULT="rolled_back"
  NOTES="Smoke tests failed, rolled back successfully"
  save_state "rolled_back" "$NOTES"
  announce ":warning: Deployment ROLLED BACK: \`$SERVICE\` - Smoke tests failed\n\`\`\`$SMOKE_OUTPUT\`\`\`" "warning"
  exit 1
fi

log "Smoke tests passed"
echo "$SMOKE_OUTPUT"

# Success!
log_step "Deployment complete"
save_state "success" "Deployed $IMAGE_TAG successfully"
announce ":white_check_mark: Deployment SUCCESS: \`$SERVICE\` → \`$IMAGE_TAG\`" "good"
