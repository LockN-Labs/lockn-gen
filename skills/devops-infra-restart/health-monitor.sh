#!/usr/bin/env bash
# health-monitor.sh — Quick health check for heartbeat integration
# Returns exit 0 if all healthy, exit 1 if >=THRESHOLD unhealthy
# Output: JSON summary for agent consumption
#
# Usage:
#   bash health-monitor.sh              # Check all, threshold=2
#   bash health-monitor.sh --threshold 3  # Custom threshold
#   bash health-monitor.sh --auto-fix   # Auto-restart if threshold exceeded
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THRESHOLD=2
AUTO_FIX=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --threshold) THRESHOLD="$2"; shift 2 ;;
    --auto-fix)  AUTO_FIX=true; shift ;;
    *)           shift ;;
  esac
done

# --- Docker containers to check ---
CONTAINERS=(
  # Tier 1: Databases
  "lockn-postgres" "lockn-garnet" "lockn-seaweedfs-master" "lockn-seaweedfs-volume" "lockn-seaweedfs-filer" "lockn-qdrant"
  # Tier 2: Shared infra
  "lockn-whisper-gpu" "lockn-panns" "lockn-speak-api" "lockn-otel-collector" "lockn-gitea" "lockn-cloudflared"
  # Tier 3: API services
  "lockn-auth-api" "lockn-gen-api" "lockn-logger-api" "lockn-platform-api" "lockn-score-api" "lockn-speak-web" "lockn-email-api" "lockn-brain-api"
  # Tier 4: Frontends
  "lockn-caddy" "lockn-score-web" "lockn-swagger-ui"
)

# --- Systemd services ---
SYSTEMD_SERVICES=("llama-coder-next" "llama-qwen" "openclaw-gateway")

down_containers=()
down_systemd=()
total_checked=0
total_healthy=0

# Check systemd services
for svc in "${SYSTEMD_SERVICES[@]}"; do
  total_checked=$((total_checked + 1))
  if systemctl --user is-active "$svc" &>/dev/null; then
    total_healthy=$((total_healthy + 1))
  else
    down_systemd+=("$svc")
  fi
done

# Check docker containers
for container in "${CONTAINERS[@]}"; do
  total_checked=$((total_checked + 1))
  status=$(docker inspect -f '{{.State.Status}}' "$container" 2>/dev/null || echo "missing")
  if [[ "$status" == "running" ]]; then
    # Check health status if available
    health=$(docker inspect -f '{{.State.Health.Status}}' "$container" 2>/dev/null || echo "none")
    if [[ "$health" == "healthy" || "$health" == "none" ]]; then
      total_healthy=$((total_healthy + 1))
    else
      down_containers+=("$container:$health")
    fi
  else
    down_containers+=("$container:$status")
  fi
done

total_down=$(( ${#down_containers[@]} + ${#down_systemd[@]} ))

# Output JSON summary
cat <<EOF
{
  "checked": $total_checked,
  "healthy": $total_healthy,
  "down": $total_down,
  "threshold": $THRESHOLD,
  "needs_restart": $([ "$total_down" -ge "$THRESHOLD" ] && echo "true" || echo "false"),
  "down_containers": [$(printf '"%s",' "${down_containers[@]}" 2>/dev/null | sed 's/,$//')],
  "down_systemd": [$(printf '"%s",' "${down_systemd[@]}" 2>/dev/null | sed 's/,$//')]
}
EOF

# Auto-fix if threshold exceeded
if [[ "$AUTO_FIX" == "true" && "$total_down" -ge "$THRESHOLD" ]]; then
  echo "--- AUTO-FIX: Running ordered restart ---" >&2
  bash "$SCRIPT_DIR/restart-infra.sh" --skip-systemd
  exit 2  # Exit 2 = auto-fix triggered
fi

# Exit code: 0=healthy, 1=degraded
[[ "$total_down" -ge "$THRESHOLD" ]] && exit 1 || exit 0
