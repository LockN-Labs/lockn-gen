#!/usr/bin/env bash
set -euo pipefail

PR_REF=""
if [[ ${1:-} == "--pr" ]]; then
  PR_REF="${2:-}"
fi

PREFIX="${LINEAR_TICKET_PREFIX:-LOC-}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required" >&2
  exit 1
fi
if [[ -z "${LINEAR_API_KEY:-}" ]]; then
  echo "LINEAR_API_KEY is required" >&2
  exit 1
fi

PR_JSON=$(gh pr view ${PR_REF:+"$PR_REF"} --json title,headRefName,url,reviewDecision)
PR_TITLE=$(echo "$PR_JSON" | jq -r '.title')
PR_BRANCH=$(echo "$PR_JSON" | jq -r '.headRefName')
PR_URL=$(echo "$PR_JSON" | jq -r '.url')
REVIEW_DECISION=$(echo "$PR_JSON" | jq -r '.reviewDecision // "REVIEW_REQUIRED"')

TICKET_ID=$(printf "%s\n%s\n" "$PR_TITLE" "$PR_BRANCH" | grep -oE "${PREFIX}[0-9]+" | head -n1 || true)
if [[ -z "$TICKET_ID" ]]; then
  echo "No ticket id found in PR title/branch" >&2
  exit 0
fi

linear_query() {
  local query="$1"
  local variables="$2"
  curl -sS -X POST https://api.linear.app/graphql \
    -H "Content-Type: application/json" \
    -H "Authorization: ${LINEAR_API_KEY}" \
    -d "$(jq -nc --arg q "$query" --argjson v "$variables" '{query:$q, variables:$v}')"
}

ISSUE_QUERY='query ($identifier: String!) { issueByIdentifier(identifier: $identifier) { id identifier title } }'
ISSUE_RESP=$(linear_query "$ISSUE_QUERY" "$(jq -nc --arg identifier "$TICKET_ID" '{identifier:$identifier}')")
ISSUE_ID=$(echo "$ISSUE_RESP" | jq -r '.data.issueByIdentifier.id // empty')
if [[ -z "$ISSUE_ID" ]]; then
  echo "Unable to resolve Linear issue: $TICKET_ID" >&2
  exit 1
fi

COMMENT_BODY=$(cat <<EOF
PR review status: $REVIEW_DECISION
PR: $PR_URL
EOF
)

COMMENT_MUTATION='mutation ($issueId: String!, $body: String!) { createComment(input: { issueId: $issueId, body: $body }) { comment { id } } }'
linear_query "$COMMENT_MUTATION" "$(jq -nc --arg issueId "$ISSUE_ID" --arg body "$COMMENT_BODY" '{issueId:$issueId, body:$body}')" >/dev/null

echo "Synced review status for $TICKET_ID: $REVIEW_DECISION"
