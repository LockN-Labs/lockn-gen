#!/usr/bin/env bash
# update-status.sh — Update a Linear task's status
# Usage: update-status.sh "task-id" "status" ["assignee-id"]
# Status options: backlog, todo, in-progress, done, cancelled
# Output: Updated task written to stdout

set -euo pipefail

API_URL="https://api.linear.app/graphql"
API_KEY="${LINEAR_API_KEY:-}"
TASK_ID="$1"
STATUS="$2"
ASSIGNEE_ID="${3:-}"

if [ -z "$API_KEY" ]; then
  echo "Error: LINEAR_API_KEY not set" >&2
  exit 1
fi

if [ -z "$TASK_ID" ]; then
  echo "Error: Task ID required" >&2
  echo "Usage: update-status.sh \"task-id\" \"status\" [assignee-id]" >&2
  exit 1
fi

if [ -z "$STATUS" ]; then
  echo "Error: Status required" >&2
  echo "Status options: backlog, todo, in-progress, done, cancelled" >&2
  exit 1
fi

# Validate status
VALID_STATUSES=("backlog" "todo" "in-progress" "done" "cancelled")
if [[ ! " ${VALID_STATUSES[@]} " =~ " ${STATUS} " ]]; then
  echo "Error: Invalid status '$STATUS'" >&2
  echo "Valid statuses: ${VALID_STATUSES[*]}" >&2
  exit 1
fi

# Build GraphQL mutation
ASSIGNEE_ARG=""
if [ -n "$ASSIGNEE_ID" ]; then
  ASSIGNEE_ARG=$(cat <<EOF
  assignee: {
    set: "$ASSIGNEE_ID"
  }
EOF
)
fi

MUTATION=$(cat <<EOF
mutation {
  updateIssue(input: {
    id: "$TASK_ID"
    status: "$STATUS"
    $ASSIGNEE_ARG
  }) {
    id
    title
    status
    assignee {
      id
      name
    }
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
    if 'updateIssue' not in data['data']:
        print('ERROR: No updateIssue in response')
        sys.exit(1)
except json.JSONDecodeError:
    print('ERROR: Invalid JSON response')
    sys.exit(1)
" 2>&1)

if [ -n "$ERROR" ]; then
  echo "$ERROR" >&2
  exit 1
fi

# Extract updated task
UPDATED_TASK=$(echo "$RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
task = data['data']['updateIssue']
print(json.dumps(task, indent=2))
")

echo "$UPDATED_TASK"
echo "Updated $TASK_ID to status: $STATUS" >&2
