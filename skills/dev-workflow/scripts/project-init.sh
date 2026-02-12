#!/usr/bin/env bash
set -euo pipefail

ORG="LockN-AI"
TEAM_ID="f37ff2bb-141f-421a-9401-fb0008bfb67f"
REPOS_ROOT="$HOME/repos"
GH="$HOME/bin/gh"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINEAR_API="$SCRIPT_DIR/linear-api.sh"

usage() {
  cat <<EOF
Usage: project-init.sh <repo-name> <description|description-file>

Creates:
  - GitHub repo in org: $ORG
  - Clones to: $REPOS_ROOT/<repo-name>
  - Linear epic (parent issue) + stories from bullet lines

Description parsing:
  - If <description> is a file path, its contents are used.
  - The epic title is: "<repo-name> Epic"
  - Stories are created from lines beginning with '-' or '*'.
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }
}

main() {
  local repo_name="${1:-}"
  local desc_input="${2:-}"
  if [[ -z "$repo_name" || -z "$desc_input" ]]; then
    usage
    exit 1
  fi

  require_cmd "$GH"
  require_cmd jq

  local description
  if [[ -f "$desc_input" ]]; then
    description="$(cat "$desc_input")"
  else
    description="$desc_input"
  fi

  echo "Creating GitHub repo $ORG/$repo_name..."
  "$GH" repo create "$ORG/$repo_name" --private --confirm

  mkdir -p "$REPOS_ROOT"
  if [[ ! -d "$REPOS_ROOT/$repo_name" ]]; then
    echo "Cloning repo to $REPOS_ROOT/$repo_name..."
    git clone "git@github.com:$ORG/$repo_name.git" "$REPOS_ROOT/$repo_name"
  fi

  echo "Creating Linear epic + stories..."
  local epic_title="$repo_name Epic"
  local epic_json
  epic_json=$("$LINEAR_API" create-issue "$epic_title" "$description" 2 "$TEAM_ID")
  local epic_id
  epic_id=$(echo "$epic_json" | jq -r '.data.issueCreate.issue.id')
  local epic_identifier
  epic_identifier=$(echo "$epic_json" | jq -r '.data.issueCreate.issue.identifier')
  local epic_url
  epic_url=$(echo "$epic_json" | jq -r '.data.issueCreate.issue.url')

  if [[ -z "$epic_id" || "$epic_id" == "null" ]]; then
    echo "Failed to create epic in Linear" >&2
    echo "$epic_json" >&2
    exit 1
  fi

  local story_count=0
  while IFS= read -r line; do
    if [[ "$line" =~ ^[[:space:]]*[-*][[:space:]]+(.+) ]]; then
      local story_title="${BASH_REMATCH[1]}"
      "$LINEAR_API" create-issue "$story_title" "Story for $repo_name" 3 "$TEAM_ID" "$epic_id" >/dev/null
      story_count=$((story_count + 1))
    fi
  done <<< "$description"

  cat <<EOF
Done.
Repo: $ORG/$repo_name
Epic: $epic_identifier
URL:  $epic_url
Stories created: $story_count
EOF
}

main "$@"
