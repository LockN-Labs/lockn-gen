#!/usr/bin/env bash
set -euo pipefail

REPOS_ROOT="$HOME/repos"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINEAR_API="$SCRIPT_DIR/linear-api.sh"

usage() {
  cat <<EOF
Usage: build-issue.sh <repo-name> <issue-identifier>

Example:
  build-issue.sh my-repo LOC-123

Outputs context for the agent and creates a feature branch:
  feature/<identifier>-<slug>
EOF
}

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g'
}

main() {
  local repo_name="${1:-}"
  local identifier="${2:-}"
  if [[ -z "$repo_name" || -z "$identifier" ]]; then
    usage
    exit 1
  fi

  local repo_path="$REPOS_ROOT/$repo_name"
  if [[ ! -d "$repo_path/.git" ]]; then
    echo "Repo not found: $repo_path" >&2
    exit 1
  fi

  local issue_json
  issue_json=$("$LINEAR_API" get-issue "$identifier")
  local issue_id title description url
  issue_id=$(echo "$issue_json" | jq -r '.data.issue.id')
  title=$(echo "$issue_json" | jq -r '.data.issue.title')
  description=$(echo "$issue_json" | jq -r '.data.issue.description')
  url=$(echo "$issue_json" | jq -r '.data.issue.url')

  if [[ -z "$issue_id" || "$issue_id" == "null" ]]; then
    echo "Issue not found: $identifier" >&2
    echo "$issue_json" >&2
    exit 1
  fi

  local branch_slug
  branch_slug=$(slugify "$title")
  local branch_name="feature/${identifier}-${branch_slug}"

  cd "$repo_path"
  git fetch origin
  if ! git rev-parse --verify "$branch_name" >/dev/null 2>&1; then
    git checkout -b "$branch_name"
  else
    git checkout "$branch_name"
  fi

  cat <<EOF
Issue: $identifier
Title: $title
URL: $url
Branch: $branch_name

Description:
$description
EOF
}

main "$@"
