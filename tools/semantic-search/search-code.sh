#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 \"query string\""
  exit 1
fi

python3 "$SCRIPT_DIR/search-code.py" "$*" --limit 10
