#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-}"
IMAGE_TAG="${2:-}"

if [[ -z "$SERVICE" || -z "$IMAGE_TAG" ]]; then
  echo "Usage: $0 <service> <image_tag>" >&2
  exit 2
fi

DEPLOY_HOST="${DEPLOY_HOST:-}"
if [[ -z "$DEPLOY_HOST" ]]; then
  echo "DEPLOY_HOST is required" >&2
  exit 3
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/services.yaml"

read_config() {
  local key="$1"
  python - <<'PY' "$CONFIG_FILE" "$SERVICE" "$key"
import sys, yaml
config_file, service, key = sys.argv[1], sys.argv[2], sys.argv[3]
with open(config_file) as f:
    data = yaml.safe_load(f)
svc = data.get('services', {}).get(service)
if not svc:
    sys.exit(4)
val = svc.get(key)
if isinstance(val, list):
    for v in val:
        print(v)
elif val is not None:
    print(val)
PY
}

HEALTH_ENDPOINT="$(read_config health_endpoint || true)"

DEPLOY_SSH_PORT="${DEPLOY_SSH_PORT:-22}"
DEPLOY_SSH_OPTS="${DEPLOY_SSH_OPTS:-}"
DEPLOY_COMPOSE_DIR="${DEPLOY_COMPOSE_DIR:-/srv/apps}"
DEPLOY_CADDY_API="${DEPLOY_CADDY_API:-http://127.0.0.1:2019}"
DEPLOY_TIMEOUT="${DEPLOY_TIMEOUT:-60}"

ssh -p "$DEPLOY_SSH_PORT" $DEPLOY_SSH_OPTS "$DEPLOY_HOST" \
  DEPLOY_COMPOSE_DIR="$DEPLOY_COMPOSE_DIR" \
  DEPLOY_CADDY_API="$DEPLOY_CADDY_API" \
  DEPLOY_TIMEOUT="$DEPLOY_TIMEOUT" \
  SERVICE="$SERVICE" \
  IMAGE_TAG="$IMAGE_TAG" \
  HEALTH_ENDPOINT="$HEALTH_ENDPOINT" \
  bash -s <<'EOS'
set -euo pipefail

SERVICE_DIR="$DEPLOY_COMPOSE_DIR/$SERVICE"
ACTIVE_FILE="$SERVICE_DIR/active_color"
PREVIOUS_FILE="$SERVICE_DIR/previous_color"

mkdir -p "$SERVICE_DIR"

ACTIVE_COLOR="blue"
if [[ -f "$ACTIVE_FILE" ]]; then
  ACTIVE_COLOR="$(cat "$ACTIVE_FILE")"
fi

if [[ "$ACTIVE_COLOR" == "blue" ]]; then
  STANDBY_COLOR="green"
else
  STANDBY_COLOR="blue"
fi

COMPOSE_FILE="$SERVICE_DIR/$STANDBY_COLOR/docker-compose.yml"
if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "Missing compose file: $COMPOSE_FILE" >&2
  exit 4
fi

# Expect docker-compose to use IMAGE_TAG env var for the service image
IMAGE_TAG="$IMAGE_TAG" docker compose -f "$COMPOSE_FILE" pull
IMAGE_TAG="$IMAGE_TAG" docker compose -f "$COMPOSE_FILE" up -d

# Health check on standby
HEALTH_URL="http://$SERVICE-$STANDBY_COLOR$HEALTH_ENDPOINT"
# If a specific health endpoint is not configured, allow container to start anyway
if [[ -n "${HEALTH_ENDPOINT:-}" ]]; then
  timeout "$DEPLOY_TIMEOUT" bash -c "until curl -fsS '$HEALTH_URL' >/dev/null; do sleep 2; done"
fi

# Swap Caddy upstream to standby
# Expect Caddy config to use an id like <service>_upstream
curl -fsS -X PATCH "$DEPLOY_CADDY_API/id/${SERVICE}_upstream" \
  -H 'Content-Type: application/json' \
  -d "{\"upstreams\":[{\"dial\":\"${SERVICE}-${STANDBY_COLOR}:80\"}]}" >/dev/null

# Stop old color
OLD_COMPOSE_FILE="$SERVICE_DIR/$ACTIVE_COLOR/docker-compose.yml"
if [[ -f "$OLD_COMPOSE_FILE" ]]; then
  docker compose -f "$OLD_COMPOSE_FILE" down
fi

echo "$ACTIVE_COLOR" > "$PREVIOUS_FILE"
echo "$STANDBY_COLOR" > "$ACTIVE_FILE"

echo "Promoted $SERVICE from $ACTIVE_COLOR to $STANDBY_COLOR with tag $IMAGE_TAG"
EOS
