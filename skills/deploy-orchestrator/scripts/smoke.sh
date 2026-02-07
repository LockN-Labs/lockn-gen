#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-}"
if [[ -z "$SERVICE" ]]; then
  echo "Usage: $0 <service>" >&2
  exit 2
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

PROD_URL="$(read_config prod_url)"
CRITICAL_PATHS=( $(read_config critical_paths || true) )

if [[ -z "$PROD_URL" ]]; then
  echo "Missing configuration for $SERVICE" >&2
  exit 4
fi

DETAILS_FILE="$(mktemp)"
trap 'rm -f "$DETAILS_FILE"' EXIT

add_detail() {
  local check="$1" url="$2" ok="$3" err="$4"
  echo "${check}|${url}|${ok}|${err:-}" >> "$DETAILS_FILE"
}

check_url() {
  local check="$1" url="$2"
  if curl -fsS --max-time 20 "$url" >/dev/null; then
    add_detail "$check" "$url" true "-"
  else
    add_detail "$check" "$url" false "curl_failed"
  fi
}

for path in "${CRITICAL_PATHS[@]}"; do
  check_url "critical" "${PROD_URL}${path}"
done

python - <<'PY' "$SERVICE" "$DETAILS_FILE"
import json, sys
service, details_file = sys.argv[1], sys.argv[2]
details = []
with open(details_file) as f:
    for line in f:
        check, url, ok, err = line.rstrip('\n').split('|', 3)
        details.append({
            "check": check,
            "url": url,
            "ok": ok == "true",
            "error": "" if err == "-" else err,
        })
passed = all(d["ok"] for d in details) if details else False
print(json.dumps({"service": service, "pass": passed, "details": details}))
PY
