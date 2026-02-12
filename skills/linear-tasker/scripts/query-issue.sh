#!/usr/bin/env bash
# query-issue.sh — Query a Linear issue by ID
# Usage: query-issue.sh "issue-id" ["fields" ...]
# Output: Issue details in JSON to stdout

set -euo pipefail

API_URL="https://api.linear.app/graphql"
API_KEY="${LINEAR_API_KEY:-}"
ISSUE_ID="$1"
FIELDS="${2:-id title description status labels assignee createdAt updatedAt}"

if [ -z "$API_KEY" ]; then
  echo "Error: LINEAR_API_KEY not set" >&2
  exit 1
fi

if [ -z "$ISSUE_ID" ]; then
  echo "Error: Issue ID required" >&2
  echo "Usage: query-issue.sh \"issue-id\" [fields]" >&2
  exit 1
fi

# Build GraphQL query
FIELD_LIST=$(echo "$FIELDS" | tr ' ' '" "' | sed 's/^"/"/; s/ $/"}/')

QUERY=$(cat <<EOF
{
  issue(input: { id: "$ISSUE_ID" }) {
    $FIELD_LIST
  }
}
EOF
)

# Execute query
RESPONSE=$(curl -s --fail \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$QUERY" \
  "$API_URL" 2>&1)

# Check for errors
ERROR=$(echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'errors' in data:
        print('\n'.join(e['message'] for e in data['errors']))
        sys.exit(1)
    if 'issue' not in data['data']:
        print('ERROR: No issue in response')
        sys.exit(1)
except json.JSONDecodeError:
    print('ERROR: Invalid JSON response')
    sys.exit(1)
" 2>&1)

if [ -n "$ERROR" ]; then
  echo "$ERROR" >&2
  exit 1
fi

# Output issue details
echo "$RESPONSE"
