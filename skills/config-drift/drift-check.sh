#!/usr/bin/env bash
# Config Drift Detection for LockN Labs
# Called by: auth-flow-validation-6h cron
# Outputs: JSON report to stdout, alerts on drift

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
TEMP_GATES="$WORKSPACE/memory/state/temp-gates.json"
REPORT_FILE="/tmp/drift-report-$(date +%Y%m%d-%H%M%S).json"
DRIFT_FOUND=0

echo '{"timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","checks":[' > "$REPORT_FILE"
FIRST=true

add_check() {
  local name="$1" status="$2" detail="$3"
  if [ "$FIRST" = true ]; then FIRST=false; else echo ',' >> "$REPORT_FILE"; fi
  echo "{\"check\":\"$name\",\"status\":\"$status\",\"detail\":\"$detail\"}" >> "$REPORT_FILE"
  if [ "$status" = "DRIFT" ] || [ "$status" = "ALERT" ]; then
    DRIFT_FOUND=1
  fi
}

# --- Check 1: Caddy Config ---
if CADDY_CONFIG=$(curl -sf http://localhost:2019/config/ 2>/dev/null); then
  if echo "$CADDY_CONFIG" | grep -q "basic_auth"; then
    add_check "caddy_basic_auth" "ALERT" "basic_auth block found in running Caddy config"
  else
    add_check "caddy_basic_auth" "OK" "No basic_auth gates detected"
  fi
  
  REPO_CADDYFILE="$WORKSPACE/../lockn-infra/Caddyfile"
  if [ -f "$REPO_CADDYFILE" ]; then
    REPO_HASH=$(sha256sum "$REPO_CADDYFILE" | cut -d' ' -f1)
    RUNNING_HASH=$(echo "$CADDY_CONFIG" | sha256sum | cut -d' ' -f1)
    if [ "$REPO_HASH" != "$RUNNING_HASH" ]; then
      add_check "caddy_config_drift" "DRIFT" "Running config differs from repo Caddyfile"
    else
      add_check "caddy_config_drift" "OK" "Config matches repo"
    fi
  else
    add_check "caddy_config_drift" "SKIP" "Repo Caddyfile not found"
  fi
else
  add_check "caddy_admin_api" "WARN" "Caddy admin API not reachable"
fi

# --- Check 2: Auth0 Callback URLs ---
if [ -n "${AUTH0_DOMAIN:-}" ] && [ -n "${AUTH0_MGMT_TOKEN:-}" ] && [ -n "${AUTH0_CLIENT_ID:-}" ]; then
  CALLBACKS=$(curl -sf -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
    "https://$AUTH0_DOMAIN/api/v2/clients/$AUTH0_CLIENT_ID?fields=callbacks" 2>/dev/null)
  
  if [ -n "$CALLBACKS" ]; then
    CALLBACK_COUNT=$(echo "$CALLBACKS" | jq '.callbacks | length' 2>/dev/null || echo "0")
    EXPECTED_CALLBACK="https://app.lockn.dev/auth/callback"
    
    if echo "$CALLBACKS" | jq -e ".callbacks | index(\"$EXPECTED_CALLBACK\")" > /dev/null 2>&1; then
      add_check "auth0_callback_primary" "OK" "Primary callback URL present"
    else
      add_check "auth0_callback_primary" "DRIFT" "Primary callback URL missing: $EXPECTED_CALLBACK"
    fi
    
    if [ "$CALLBACK_COUNT" -gt 3 ]; then
      add_check "auth0_callback_sprawl" "WARN" "Found $CALLBACK_COUNT callback URLs — consolidate per LOC-425"
    else
      add_check "auth0_callback_sprawl" "OK" "$CALLBACK_COUNT callback URLs registered"
    fi
  else
    add_check "auth0_callbacks" "WARN" "Could not fetch Auth0 client config"
  fi
else
  add_check "auth0_callbacks" "SKIP" "Auth0 management credentials not configured"
fi

# --- Check 3: Temporary Security Gates ---
if [ -f "$TEMP_GATES" ]; then
  NOW=$(date +%s)
  EXPIRED=$(jq --arg now "$NOW" '
    [.gates[] | select(.expiresAt != null) | 
     select((.expiresAt | sub("\\.[0-9]+Z$"; "Z") | strptime("%Y-%m-%dT%H:%M:%SZ") | mktime) < ($now | tonumber))]
    | length' "$TEMP_GATES" 2>/dev/null || echo "0")
  TOTAL=$(jq '.gates | length' "$TEMP_GATES" 2>/dev/null || echo "0")
  
  if [ "$EXPIRED" -gt 0 ]; then
    add_check "temp_gates_expired" "ALERT" "$EXPIRED of $TOTAL temporary gates have expired"
  elif [ "$TOTAL" -gt 0 ]; then
    add_check "temp_gates" "WARN" "$TOTAL active temporary gates"
  else
    add_check "temp_gates" "OK" "No temporary security gates active"
  fi
else
  add_check "temp_gates_file" "WARN" "temp-gates.json not found"
fi

# --- Check 4: Auth Endpoint Reachability ---
if [ -n "${LOCKN_APP_URL:-}" ]; then
  HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" "$LOCKN_APP_URL/auth/callback" 2>/dev/null || echo "000")
  if [ "$HTTP_CODE" = "000" ]; then
    add_check "auth_endpoint" "ALERT" "Auth callback endpoint unreachable"
  elif [ "$HTTP_CODE" -ge 500 ]; then
    add_check "auth_endpoint" "ALERT" "Auth callback returned HTTP $HTTP_CODE"
  else
    add_check "auth_endpoint" "OK" "Auth callback reachable (HTTP $HTTP_CODE)"
  fi
else
  add_check "auth_endpoint" "SKIP" "LOCKN_APP_URL not configured"
fi

echo ']}' >> "$REPORT_FILE"
cat "$REPORT_FILE"
exit $DRIFT_FOUND
