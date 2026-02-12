# Config Drift Detection Skill

## Purpose
Detect configuration drift between expected (IaC/repo) and actual (running) infrastructure configs for LockN Labs. Covers Caddy, Auth0, and temporary security measures.

## Usage
Called by `auth-flow-validation-6h` cron or manually during incident response.

## What It Checks

### 1. Caddy Config Drift
Compares repo Caddyfile against running Caddy config.

### 2. Auth0 Callback URL Alignment
Ensures Auth0 application callback URLs match expected set.

### 3. Temporary Security Gate Audit
Checks `memory/state/temp-gates.json` for expired or untracked gates.

## Scripts

### drift-check.sh — Main Drift Detection Script

```bash
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
# Fetch running Caddy config via admin API
if CADDY_CONFIG=$(curl -sf http://localhost:2019/config/ 2>/dev/null); then
  # Check for basic_auth blocks (should not exist post-incident)
  if echo "$CADDY_CONFIG" | grep -q "basic_auth"; then
    add_check "caddy_basic_auth" "ALERT" "basic_auth block found in running Caddy config"
  else
    add_check "caddy_basic_auth" "OK" "No basic_auth gates detected"
  fi
  
  # Compare against repo Caddyfile if available
  REPO_CADDYFILE="$WORKSPACE/../lockn-infra/Caddyfile"
  if [ -f "$REPO_CADDYFILE" ]; then
    REPO_HASH=$(sha256sum "$REPO_CADDYFILE" | cut -d' ' -f1)
    # Export running config and compare
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
# Requires AUTH0_DOMAIN and AUTH0_MGMT_TOKEN env vars
if [ -n "${AUTH0_DOMAIN:-}" ] && [ -n "${AUTH0_MGMT_TOKEN:-}" ] && [ -n "${AUTH0_CLIENT_ID:-}" ]; then
  CALLBACKS=$(curl -sf -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
    "https://$AUTH0_DOMAIN/api/v2/clients/$AUTH0_CLIENT_ID?fields=callbacks" 2>/dev/null)
  
  if [ -n "$CALLBACKS" ]; then
    # Check for single callback pattern (LOC-425)
    CALLBACK_COUNT=$(echo "$CALLBACKS" | jq '.callbacks | length' 2>/dev/null || echo "0")
    EXPECTED_CALLBACK="https://app.lockn.dev/auth/callback"
    
    if echo "$CALLBACKS" | jq -e ".callbacks | index(\"$EXPECTED_CALLBACK\")" > /dev/null 2>&1; then
      add_check "auth0_callback_primary" "OK" "Primary callback URL present"
    else
      add_check "auth0_callback_primary" "DRIFT" "Primary callback URL missing: $EXPECTED_CALLBACK"
    fi
    
    if [ "$CALLBACK_COUNT" -gt 3 ]; then
      add_check "auth0_callback_sprawl" "WARN" "Found $CALLBACK_COUNT callback URLs — consider consolidating per LOC-425"
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
    add_check "temp_gates_expired" "ALERT" "$EXPIRED of $TOTAL temporary gates have expired and need removal"
  elif [ "$TOTAL" -gt 0 ]; then
    add_check "temp_gates" "WARN" "$TOTAL active temporary gates — review needed"
  else
    add_check "temp_gates" "OK" "No temporary security gates active"
  fi
  
  # Check last audit freshness
  LAST_AUDIT=$(jq -r '.lastAudit // empty' "$TEMP_GATES" 2>/dev/null)
  if [ -n "$LAST_AUDIT" ]; then
    AUDIT_AGE=$(( NOW - $(date -d "$LAST_AUDIT" +%s 2>/dev/null || echo "$NOW") ))
    if [ "$AUDIT_AGE" -gt 604800 ]; then  # 7 days
      add_check "temp_gates_audit_age" "WARN" "Last temp-gate audit was $(( AUDIT_AGE / 86400 )) days ago"
    else
      add_check "temp_gates_audit_age" "OK" "Last audit: $LAST_AUDIT"
    fi
  fi
else
  add_check "temp_gates_file" "WARN" "temp-gates.json not found"
fi

# --- Check 4: Auth Flow Smoke Test ---
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

# Output report
cat "$REPORT_FILE"

# Exit code reflects drift status
exit $DRIFT_FOUND
```

## Temp-Gate Lifecycle

Temporary security measures follow this lifecycle:
1. **Created** → Entry added to `temp-gates.json` with `expiresAt` and Linear ticket
2. **Active** → Checked every 6h by drift detection
3. **Expiring** → Alert 48h before expiration
4. **Expired** → ALERT status until removed or renewed (with justification)
5. **Removed** → Entry moved to `removedGates` array with removal date

### temp-gates.json Schema

```json
{
  "description": "Tracks all temporary security measures",
  "gates": [
    {
      "id": "gate-001",
      "type": "caddy_basic_auth|firewall_rule|feature_flag|auth0_override",
      "description": "What this gate does",
      "location": "Where it's configured (file path, service, etc.)",
      "createdAt": "2026-02-10T12:00:00Z",
      "expiresAt": "2026-03-10T12:00:00Z",
      "linearTicket": "LOC-XXX",
      "owner": "person responsible",
      "removalSteps": "How to remove this gate"
    }
  ],
  "removedGates": [],
  "lastAudit": "2026-02-10T13:23:00Z"
}
```

## Related
- LOC-427: Temporary Security Gate Tracker
- `auth-flow-validation-6h` cron
- `devops-infra-check-15min` (Caddy audit step)
