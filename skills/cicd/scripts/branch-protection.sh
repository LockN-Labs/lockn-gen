#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: branch-protection.sh [--branch <name>] [--checks <comma-separated>]

Applies GitHub branch protection using gh CLI.
EOF
}

BRANCH=""
CHECKS="CI"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --branch)
      BRANCH="$2"; shift 2;;
    --checks)
      CHECKS="$2"; shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown argument: $1" >&2
      usage; exit 1;;
  esac
 done

repo_slug=""
origin_url="$(git config --get remote.origin.url || true)"
if [[ -n "$origin_url" ]]; then
  if [[ "$origin_url" =~ github.com[:/]+([^/]+)/([^/.]+)(\.git)?$ ]]; then
    owner="${BASH_REMATCH[1]}"
    repo="${BASH_REMATCH[2]}"
    repo_slug="$owner/$repo"
  fi
fi

if [[ -z "$repo_slug" ]]; then
  echo "Unable to determine repo slug from git remote." >&2
  exit 1
fi

if [[ -z "$BRANCH" ]]; then
  BRANCH="$(git remote show origin 2>/dev/null | awk '/HEAD branch/ {print $NF}')"
fi
BRANCH="${BRANCH:-main}"

IFS=',' read -r -a CHECK_ARRAY <<< "$CHECKS"

json_checks=""
for check in "${CHECK_ARRAY[@]}"; do
  check_trimmed="$(echo "$check" | xargs)"
  [[ -z "$check_trimmed" ]] && continue
  json_checks+="\"${check_trimmed}\","
done
json_checks="${json_checks%,}"
if [[ -z "$json_checks" ]]; then
  json_checks="\"CI\""
fi

payload=$(cat <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": [${json_checks}]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}
EOF
)

printf "%s" "$payload" | gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${repo_slug}/branches/${BRANCH}/protection" \
  --input - >/dev/null

echo "Branch protection updated for ${repo_slug}:${BRANCH}"
