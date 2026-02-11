#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR" || exit 2

echo "[LockN QA] Running smoke suite..."
pytest -m smoke -q
status=$?

if [ "$status" -eq 0 ]; then
  echo "[LockN QA] SMOKE RESULT: PASS"
else
  echo "[LockN QA] SMOKE RESULT: FAIL (exit code: $status)"
fi

exit "$status"
