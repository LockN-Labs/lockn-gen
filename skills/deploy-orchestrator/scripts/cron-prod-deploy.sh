#!/usr/bin/env bash
# cron-prod-deploy.sh - 5am production deployment cron job
# Runs daily at 5am to deploy latest tagged images
#
# Install: 
#   0 5 * * * /path/to/cron-prod-deploy.sh >> /var/log/lockn-deploy.log 2>&1
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/services.yaml"
DEPLOY_SCRIPT="$ROOT_DIR/scripts/deploy.sh"
LOG_DIR="${DEPLOY_LOG_DIR:-/var/log/lockn-deploy}"

# Source environment (Slack webhooks, SSH config, etc.)
if [[ -f /etc/lockn/deploy.env ]]; then
  source /etc/lockn/deploy.env
elif [[ -f "$HOME/.lockn/deploy.env" ]]; then
  source "$HOME/.lockn/deploy.env"
fi

mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

# Get list of services from config
get_services() {
  python3 - <<'PY' "$CONFIG_FILE"
import sys, yaml
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)
for svc in data.get('services', {}).keys():
    print(svc)
PY
}

# Get latest tag for a service from registry
# Override with REGISTRY_URL env var for your container registry
get_latest_tag() {
  local service="$1"
  local registry="${REGISTRY_URL:-ghcr.io/lockn-ai}"
  
  # Try to get latest semantic version tag
  # Falls back to 'latest' if no semver tags found
  local tag
  tag=$(curl -sS "https://api.github.com/orgs/lockn-ai/packages/container/$service/versions" \
    -H "Authorization: Bearer ${GITHUB_TOKEN:-}" 2>/dev/null \
    | python3 -c "
import sys, json
try:
    versions = json.load(sys.stdin)
    tags = [t for v in versions for t in v.get('metadata', {}).get('container', {}).get('tags', []) if t.startswith('v')]
    if tags:
        print(sorted(tags, reverse=True)[0])
    else:
        print('latest')
except:
    print('latest')
" 2>/dev/null) || echo "latest"
  
  echo "$tag"
}

log "=== Starting 5am production deployment run ==="

SERVICES=$(get_services)
FAILED=()
SUCCEEDED=()

for service in $SERVICES; do
  log "Processing: $service"
  
  # Get latest tag
  TAG=$(get_latest_tag "$service")
  log "  Latest tag: $TAG"
  
  # Skip if no new tag (check against last deployed)
  STATE_FILE="$ROOT_DIR/state/$service.json"
  if [[ -f "$STATE_FILE" ]]; then
    LAST_TAG=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('image_tag', ''))" 2>/dev/null || true)
    if [[ "$LAST_TAG" == "$TAG" ]]; then
      log "  Skipping: already deployed $TAG"
      continue
    fi
  fi
  
  # Deploy
  if "$DEPLOY_SCRIPT" "$service" "$TAG" >> "$LOG_FILE" 2>&1; then
    SUCCEEDED+=("$service:$TAG")
    log "  SUCCESS: $service → $TAG"
  else
    FAILED+=("$service:$TAG")
    log "  FAILED: $service → $TAG"
  fi
done

log "=== Deployment run complete ==="
log "Succeeded: ${SUCCEEDED[*]:-none}"
log "Failed: ${FAILED[*]:-none}"

# Exit with error if any failed
[[ ${#FAILED[@]} -eq 0 ]]
