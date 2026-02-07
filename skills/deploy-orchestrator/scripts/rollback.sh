#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-}"
if [[ -z "$SERVICE" ]]; then
  echo "Usage: $0 <service>" >&2
  exit 2
fi

DEPLOY_HOST="${DEPLOY_HOST:-}"
if [[ -z "$DEPLOY_HOST" ]]; then
  echo "DEPLOY_HOST is required" >&2
  exit 3
fi

DEPLOY_SSH_PORT="${DEPLOY_SSH_PORT:-22}"
DEPLOY_SSH_OPTS="${DEPLOY_SSH_OPTS:-}"
DEPLOY_COMPOSE_DIR="${DEPLOY_COMPOSE_DIR:-/srv/apps}"
DEPLOY_CADDY_API="${DEPLOY_CADDY_API:-http://127.0.0.1:2019}"

ssh -p "$DEPLOY_SSH_PORT" $DEPLOY_SSH_OPTS "$DEPLOY_HOST" \
  DEPLOY_COMPOSE_DIR="$DEPLOY_COMPOSE_DIR" \
  DEPLOY_CADDY_API="$DEPLOY_CADDY_API" \
  SERVICE="$SERVICE" \
  bash -s <<'EOS'
set -euo pipefail

SERVICE_DIR="$DEPLOY_COMPOSE_DIR/$SERVICE"
ACTIVE_FILE="$SERVICE_DIR/active_color"
PREVIOUS_FILE="$SERVICE_DIR/previous_color"

if [[ ! -f "$ACTIVE_FILE" || ! -f "$PREVIOUS_FILE" ]]; then
  echo "Missing active/previous color files for $SERVICE" >&2
  exit 4
fi

ACTIVE_COLOR="$(cat "$ACTIVE_FILE")"
PREVIOUS_COLOR="$(cat "$PREVIOUS_FILE")"

# Swap Caddy back to previous upstream
curl -fsS -X PATCH "$DEPLOY_CADDY_API/id/${SERVICE}_upstream" \
  -H 'Content-Type: application/json' \
  -d "{\"upstreams\":[{\"dial\":\"${SERVICE}-${PREVIOUS_COLOR}:80\"}]}" >/dev/null

# Stop failed deployment
FAILED_COMPOSE_FILE="$SERVICE_DIR/$ACTIVE_COLOR/docker-compose.yml"
if [[ -f "$FAILED_COMPOSE_FILE" ]]; then
  docker compose -f "$FAILED_COMPOSE_FILE" down
fi

echo "$PREVIOUS_COLOR" > "$ACTIVE_FILE"

echo "Rolled back $SERVICE to $PREVIOUS_COLOR"
EOS
