#!/usr/bin/env bash
set -euo pipefail

ORG="LockN-AI"
GH="$HOME/bin/gh"

usage() {
  cat <<EOF
Usage: review-pr.sh <repo-name> <pr-number>

Fetches PR diff for review and prints to stdout.
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }
}

main() {
  local repo_name="${1:-}"
  local pr_number="${2:-}"
  if [[ -z "$repo_name" || -z "$pr_number" ]]; then
    usage
    exit 1
  fi

  require_cmd "$GH"

  "$GH" pr diff "$pr_number" --repo "$ORG/$repo_name"
}

main "$@"
