#!/usr/bin/env bash
# create-subtask.sh — Create a subtask under a parent issue
# Usage: create-subtask.sh "task title" "parent-issue-id" ["label1" "label2" ...]
# Output: Subtask ID written to stdout

set -euo pipefail

API_URL="https://api.linear.app/graphql"
API_KEY="${LINEAR_API_KEY:-}"
PARENT_ID="$1"
TITLE="$2"
shift 2
LABELS=("$@")

if [ -z "$API_KEY" ]; then
  echo "Error: LINEAR_API_KEY not set" >&2
  exit 1
fi

if [ -z "$PARENT_ID" ]; then
  echo "Error: Parent issue ID required" >&2
  echo "Usage: create-subtask.sh \"title\" \"parent-issue-id\" [label1 label2 ...]" >&2
  exit 1
fi

if [ -z "$TITLE" ]; then
  echo "Error: Task title required" >&2
  echo "Usage: create-subtask.sh \"title\" \"parent-issue-id\" [label1 label2 ...]" >&2
  exit 1
fi

# Build GraphQL mutation
LABELS_ARG=""
if [ ${#LABELS[@]} -gt 0 ]; then
  LABELS_JSON=$(printf '%s\n' "${LABELS[@]}" | jq -R . | jq -s .)
  LABELS_ARG=$(cat <<EOF
  labels: {
    create: $LABELS_JSON
  }
EOF
)
fi

MUTATION=$(cat <<EOF
mutation {
  createIssue(input: {
    title: "$TITLE"
    teamId: "TBD"  # TODO: Get from parent issue or configuration
    $LABELS_ARG
  }) {
    id
    title
    status
  }
}
EOF
)

# Execute query
RESPONSE=$(curl -s --fail \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$MUTATION" \
  "$API_URL" 2>&1)

# Check for errors
ERROR=$(echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'errors' in data:
        print('\n'.join(e['message'] for e in data['errors']))
        sys.exit(1)
    if 'createIssue' not in data['data']:
        print('ERROR: No createIssue in response')
        sys.exit(1)
except json.JSONDecodeError:
    print('ERROR: Invalid JSON response')
    sys.exit(1)
" 2>&1)

if [ -n "$ERROR" ]; then
  echo "$ERROR" >&2
  exit 1
fi

# Extract subtask ID
SUBTASK_ID=$(echo "$RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data['data']['createIssue']['id'])
")

echo "$SUBTASK_ID"
echo "Created subtask: $TITLE" >&2
