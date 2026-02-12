#!/usr/bin/env bash
# restart-infra.sh — Ordered infrastructure restart with dependency-aware tiering
# Eliminates race conditions by waiting for health between tiers.
#
# Usage:
#   bash restart-infra.sh              # Full ordered restart
#   bash restart-infra.sh --check      # Status check only (no restarts)
#   bash restart-infra.sh --dry-run    # Show plan without executing
#   bash restart-infra.sh --skip-systemd  # Skip tier 0 (systemd services)
#   bash restart-infra.sh --tier N     # Only restart tier N
set -uo pipefail

# --- Config ---
TIER_TIMEOUT=${TIER_TIMEOUT:-60}       # seconds to wait per tier for health
HEALTH_INTERVAL=3                       # seconds between health polls
COLOR=${COLOR:-true}

# --- Parse args ---
CHECK_ONLY=false
DRY_RUN=false
SKIP_SYSTEMD=false
ONLY_TIER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)       CHECK_ONLY=true; shift ;;
    --dry-run)     DRY_RUN=true; shift ;;
    --skip-systemd) SKIP_SYSTEMD=true; shift ;;
    --tier)        ONLY_TIER="$2"; shift 2 ;;
    *)             echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# --- Colors ---
if [[ "$COLOR" == "true" ]]; then
  GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
else
  GREEN=''; RED=''; YELLOW=''; BLUE=''; NC=''
fi

ok()   { echo -e "  ${GREEN}✅ $1${NC}"; }
fail() { echo -e "  ${RED}❌ $1${NC}"; }
warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "${BLUE}$1${NC}"; }

TOTAL_OK=0; TOTAL_FAIL=0; TOTAL_RESTARTED=0
HAS_CRITICAL_FAIL=false

# ============================================================
# TIER 0: Systemd services
# ============================================================
declare -A SYSTEMD_SERVICES=(
  ["llama-coder-next"]="11439"
  ["llama-qwen"]="11437"
  ["llama-coder-cpu"]="11440"
)
declare -A SYSTEMD_USER_SERVICES=(
  ["llama-coder-next"]="1"
  ["llama-qwen"]="1"
  ["llama-coder-cpu"]="1"
  ["openclaw-gateway"]="1"
)
declare -A SYSTEMD_SYSTEM_SERVICES=(
  ["ollama"]="11434"
)

check_systemd_service() {
  local svc="$1" port="$2" is_user="$3"
  local cmd="systemctl"
  [[ "$is_user" == "1" ]] && cmd="systemctl --user"
  
  if $cmd is-active --quiet "$svc.service" 2>/dev/null; then
    if [[ -n "$port" ]]; then
      if curl -s -m 3 -o /dev/null "http://127.0.0.1:$port/v1/models" 2>/dev/null || \
         curl -s -m 3 -o /dev/null "http://127.0.0.1:$port/api/tags" 2>/dev/null; then
        return 0
      fi
    else
      return 0
    fi
  fi
  return 1
}

restart_systemd_service() {
  local svc="$1" is_user="$2"
  local cmd="sudo systemctl"
  [[ "$is_user" == "1" ]] && cmd="systemctl --user"
  $cmd restart "$svc.service" 2>/dev/null
}

do_tier0() {
  info "[TIER 0] Systemd services..."
  
  # User services
  for svc in llama-coder-next llama-qwen llama-coder-cpu openclaw-gateway; do
    local port="${SYSTEMD_SERVICES[$svc]:-}"
    [[ "$svc" == "openclaw-gateway" ]] && port="18789"
    
    if check_systemd_service "$svc" "$port" "1"; then
      ok "$svc (port ${port:-n/a})"
      ((TOTAL_OK++))
    elif [[ "$CHECK_ONLY" == "true" ]]; then
      fail "$svc (port ${port:-n/a}) — DOWN"
      ((TOTAL_FAIL++))
      HAS_CRITICAL_FAIL=true
    elif [[ "$DRY_RUN" == "true" ]]; then
      warn "$svc (port ${port:-n/a}) — would restart"
    else
      warn "$svc (port ${port:-n/a}) — restarting..."
      restart_systemd_service "$svc" "1"
      ((TOTAL_RESTARTED++))
    fi
  done
  
  # System services (ollama)
  for svc in ollama; do
    local port="${SYSTEMD_SYSTEM_SERVICES[$svc]}"
    if check_systemd_service "$svc" "$port" "0"; then
      ok "$svc (port $port)"
      ((TOTAL_OK++))
    elif [[ "$CHECK_ONLY" == "true" ]]; then
      fail "$svc (port $port) — DOWN"
      ((TOTAL_FAIL++))
      HAS_CRITICAL_FAIL=true
    elif [[ "$DRY_RUN" == "true" ]]; then
      warn "$svc (port $port) — would restart"
    else
      warn "$svc (port $port) — restarting..."
      restart_systemd_service "$svc" "0"
      ((TOTAL_RESTARTED++))
    fi
  done
  
  # Wait for systemd services to become healthy if we restarted any
  if [[ "$TOTAL_RESTARTED" -gt 0 && "$DRY_RUN" != "true" && "$CHECK_ONLY" != "true" ]]; then
    info "  Waiting for systemd services to stabilize..."
    local elapsed=0
    while [[ $elapsed -lt $TIER_TIMEOUT ]]; do
      local all_up=true
      for svc in llama-coder-next llama-qwen llama-coder-cpu; do
        local port="${SYSTEMD_SERVICES[$svc]}"
        if ! curl -s -m 2 -o /dev/null "http://127.0.0.1:$port/v1/models" 2>/dev/null; then
          all_up=false; break
        fi
      done
      if $all_up; then break; fi
      sleep "$HEALTH_INTERVAL"
      elapsed=$((elapsed + HEALTH_INTERVAL))
    done
  fi
}

# ============================================================
# TIER 1-4: Docker containers
# ============================================================

# Compose projects in start order within each tier
# Format: "project_name:compose_dir"
declare -A COMPOSE_PROJECTS=(
  ["lockn-infra"]="/home/sean/.openclaw/workspace/lockn-infra"
  ["lockn-test"]="/home/sean/.openclaw/workspace/lockn-infra"
  ["lockn-auth"]="/home/sean/repos/lockn-auth"
  ["lockn-gen"]="/home/sean/repos/lockn-gen"
  ["lockn-logger"]="/home/sean/.openclaw/workspace/lockn-logger"
  ["lockn-score"]="/home/sean/repos/lockn-score"
  ["lockn-listen"]="/home/sean/.openclaw/workspace/lockn-listen"
  ["lockn-ai-platform"]="/home/sean/.openclaw/workspace/lockn-ai-platform"
  ["otel"]="/home/sean/.openclaw/workspace/lockn-infra/otel"
  ["lockn-git"]="/home/sean/repos/lockn-git"
  ["rippled"]="/home/sean/repos/lockn-swap/infra/rippled"
)

# Tier 1: Databases & storage (must be healthy before APIs start)
TIER1_CONTAINERS=(
  "lockn-postgres-dev"
  "lockn-postgres-test"
  "lockn-logger-postgres-1"
  "lockn-auth-db-1"
  "lockn-gen-db-1"
  "lockn-logger-garnet-1"
  "lockn-logger-seaweedfs-1"
  "qdrant"
)

# Tier 2: Shared infra services (no DB dependency, or DB-independent)
TIER2_CONTAINERS=(
  "lockn-whisper-gpu"
  "lockn-panns"
  "qwen3-tts-api"
  "chatterbox-v4"
  "lockn-otel-collector"
  "lockn-grafana"
  "lockn-tempo"
  "lockn-cloudflared"
  "lockn-git"
  "lockn-git-mirror"
  # "lockn-rippled"  # disabled per Sean — leave stopped
)

# Tier 3: API services (depend on databases from tier 1)
TIER3_CONTAINERS=(
  "lockn-auth-api-1"
  "lockn-gen-api-1"
  "lockn-logger-api-1"
  "lockn-platform-api"
  "lockn-platform-api-test"
  "lockn-score-api"
  "lockn-speak-api"
  "lockn-speak-api-test"
  "lockn-speak-dev"
  "lockn-email-api"
  "lockn-email-api-test"
  "lockn-brain"
)

# Tier 4: Frontends & routing (depend on APIs from tier 3)
TIER4_CONTAINERS=(
  "lockn-caddy"
  "lockn-caddy-test"
  "lockn-score-web"
  "lockn-swagger"
)

check_container() {
  local name="$1"
  local status
  status=$(docker inspect --format='{{.State.Status}}' "$name" 2>/dev/null) || return 1
  
  if [[ "$status" != "running" ]]; then
    return 1
  fi
  
  # Check if container has a healthcheck and if it's healthy
  local health
  health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$name" 2>/dev/null) || return 0
  
  if [[ "$health" == "healthy" || "$health" == "none" ]]; then
    return 0
  fi
  return 1  # unhealthy or starting
}

wait_for_containers() {
  local -n containers=$1
  local elapsed=0
  
  while [[ $elapsed -lt $TIER_TIMEOUT ]]; do
    local all_healthy=true
    for c in "${containers[@]}"; do
      if ! docker inspect "$c" &>/dev/null; then continue; fi  # skip non-existent
      if ! check_container "$c"; then
        all_healthy=false
        break
      fi
    done
    if $all_healthy; then return 0; fi
    sleep "$HEALTH_INTERVAL"
    elapsed=$((elapsed + HEALTH_INTERVAL))
  done
  return 1  # timeout
}

do_docker_tier() {
  local tier_num="$1" tier_label="$2"
  local -n tier_containers=$3
  
  info "[TIER $tier_num] $tier_label..."
  
  local tier_restarted=0
  for c in "${tier_containers[@]}"; do
    # Skip containers that don't exist on this system
    if ! docker inspect "$c" &>/dev/null 2>&1; then
      continue
    fi
    
    if check_container "$c"; then
      local health
      health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}running{{end}}' "$c" 2>/dev/null)
      ok "$c ($health)"
      ((TOTAL_OK++))
    elif [[ "$CHECK_ONLY" == "true" ]]; then
      local state
      state=$(docker inspect --format='{{.State.Status}}' "$c" 2>/dev/null || echo "not found")
      fail "$c ($state)"
      ((TOTAL_FAIL++))
      [[ "$tier_num" -le 1 ]] && HAS_CRITICAL_FAIL=true
    elif [[ "$DRY_RUN" == "true" ]]; then
      local state
      state=$(docker inspect --format='{{.State.Status}}' "$c" 2>/dev/null || echo "not found")
      warn "$c ($state) — would restart"
    else
      local state
      state=$(docker inspect --format='{{.State.Status}}' "$c" 2>/dev/null || echo "not found")
      warn "$c ($state) — starting..."
      docker start "$c" 2>/dev/null || true
      ((TOTAL_RESTARTED++))
      ((tier_restarted++))
    fi
  done
  
  # Wait for tier health if we restarted anything
  if [[ $tier_restarted -gt 0 && "$DRY_RUN" != "true" && "$CHECK_ONLY" != "true" ]]; then
    info "  Waiting for tier $tier_num health checks (up to ${TIER_TIMEOUT}s)..."
    if wait_for_containers "$3"; then
      info "  ✅ Tier $tier_num healthy"
    else
      # Check which ones are still unhealthy
      for c in "${tier_containers[@]}"; do
        if ! docker inspect "$c" &>/dev/null 2>&1; then continue; fi
        if ! check_container "$c"; then
          fail "$c — still unhealthy after ${TIER_TIMEOUT}s"
          ((TOTAL_FAIL++))
          [[ "$tier_num" -le 1 ]] && HAS_CRITICAL_FAIL=true
        fi
      done
    fi
  fi
}

# ============================================================
# Main
# ============================================================
echo ""
info "╔══════════════════════════════════════════════╗"
if [[ "$CHECK_ONLY" == "true" ]]; then
  info "║  LockN Infrastructure Health Check           ║"
elif [[ "$DRY_RUN" == "true" ]]; then
  info "║  LockN Infrastructure Restart (DRY RUN)      ║"
else
  info "║  LockN Infrastructure Ordered Restart         ║"
fi
info "╚══════════════════════════════════════════════╝"
echo ""

run_tier() {
  local n="$1"
  case "$n" in
    0) [[ "$SKIP_SYSTEMD" != "true" ]] && do_tier0 ;;
    1) do_docker_tier 1 "Databases & storage" TIER1_CONTAINERS ;;
    2) do_docker_tier 2 "Shared infrastructure" TIER2_CONTAINERS ;;
    3) do_docker_tier 3 "API services" TIER3_CONTAINERS ;;
    4) do_docker_tier 4 "Frontends & routing" TIER4_CONTAINERS ;;
  esac
  echo ""
}

if [[ -n "$ONLY_TIER" ]]; then
  run_tier "$ONLY_TIER"
else
  for t in 0 1 2 3 4; do run_tier "$t"; done
fi

# --- Summary ---
info "════════════════════════════════════════════════"
echo -e "  Healthy: ${GREEN}${TOTAL_OK}${NC}  |  Failed: ${RED}${TOTAL_FAIL}${NC}  |  Restarted: ${YELLOW}${TOTAL_RESTARTED}${NC}"
info "════════════════════════════════════════════════"

if [[ "$HAS_CRITICAL_FAIL" == "true" ]]; then
  echo -e "${RED}CRITICAL: Infrastructure services failed${NC}"
  exit 2
elif [[ $TOTAL_FAIL -gt 0 ]]; then
  exit 1
else
  exit 0
fi
