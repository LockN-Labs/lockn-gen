#!/usr/bin/env bash
set -euo pipefail

PR_REF=""
if [[ ${1:-} == "--pr" ]]; then
  PR_REF="${2:-}"
fi

PREFIX="${LINEAR_TICKET_PREFIX:-LOC-}"
TARGET_STATE_NAME="${LINEAR_TARGET_STATE:-Done}"

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

PR_JSON=$(gh pr view ${PR_REF:+"$PR_REF"} --json title,headRefName,url,merged)
PR_TITLE=$(echo "$PR_JSON" | jq -r '.title')
PR_BRANCH=$(echo "$PR_JSON" | jq -r '.headRefName')
PR_URL=$(echo "$PR_JSON" | jq -r '.url')
MERGED=$(echo "$PR_JSON" | jq -r '.merged')

if [[ "$MERGED" != "true" ]]; then
  echo "PR not merged; skipping" >&2
  exit 0
fi

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

ISSUE_QUERY='query ($identifier: String!) { issueByIdentifier(identifier: $identifier) { id identifier title team { id } } }'
ISSUE_RESP=$(linear_query "$ISSUE_QUERY" "$(jq -nc --arg identifier "$TICKET_ID" '{identifier:$identifier}')")
ISSUE_ID=$(echo "$ISSUE_RESP" | jq -r '.data.issueByIdentifier.id // empty')
TEAM_ID=$(echo "$ISSUE_RESP" | jq -r '.data.issueByIdentifier.team.id // empty')
if [[ -z "$ISSUE_ID" || -z "$TEAM_ID" ]]; then
  echo "Unable to resolve Linear issue/team: $TICKET_ID" >&2
  exit 1
fi

STATES_QUERY='query ($teamId: String!) { team(id: $teamId) { workflowStates { nodes { id name } } } }'
STATES_RESP=$(linear_query "$STATES_QUERY" "$(jq -nc --arg teamId "$TEAM_ID" '{teamId:$teamId}')")
STATE_ID=$(echo "$STATES_RESP" | jq -r --arg name "$TARGET_STATE_NAME" '.data.team.workflowStates.nodes[] | select(.name == $name) | .id' | head -n1)
if [[ -z "$STATE_ID" ]]; then
  echo "Target state not found: $TARGET_STATE_NAME" >&2
  exit 1
fi

UPDATE_MUTATION='mutation ($issueId: String!, $stateId: String!) { updateIssue(input: { id: $issueId, stateId: $stateId }) { issue { id } } }'
linear_query "$UPDATE_MUTATION" "$(jq -nc --arg issueId "$ISSUE_ID" --arg stateId "$STATE_ID" '{issueId:$issueId, stateId:$stateId}')" >/dev/null

COMMENT_MUTATION='mutation ($issueId: String!, $body: String!) { createComment(input: { issueId: $issueId, body: $body }) { comment { id } } }'
COMMENT_BODY=$(cat <<EOF
PR merged: $PR_URL
Moved to state: $TARGET_STATE_NAME
EOF
)
linear_query "$COMMENT_MUTATION" "$(jq -nc --arg issueId "$ISSUE_ID" --arg body "$COMMENT_BODY" '{issueId:$issueId, body:$body}')" >/dev/null

echo "Updated $TICKET_ID to $TARGET_STATE_NAME"
