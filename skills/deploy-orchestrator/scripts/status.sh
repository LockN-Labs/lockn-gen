#!/usr/bin/env bash
# status.sh - Report deployment status
set -euo pipefail

SERVICE="${1:-all}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="${DEPLOY_STATE_DIR:-$ROOT_DIR/state}"

if [[ ! -d "$STATE_DIR" ]]; then
  echo '{"error":"No deployment state found"}'
  exit 0
fi

if [[ "$SERVICE" == "all" ]]; then
  # Report all services
  echo '{"services":['
  first=true
  for f in "$STATE_DIR"/*.json; do
    [[ -f "$f" ]] || continue
    if [[ "$first" == "true" ]]; then
      first=false
    else
      echo ","
    fi
    cat "$f"
  done
  echo ']}'
else
  # Report single service
  STATE_FILE="$STATE_DIR/$SERVICE.json"
  if [[ -f "$STATE_FILE" ]]; then
    cat "$STATE_FILE"
  else
    echo "{\"service\":\"$SERVICE\",\"status\":\"unknown\",\"notes\":\"No deployment state found\"}"
  fi
fi
