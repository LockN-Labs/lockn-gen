#!/usr/bin/env bash
# comment-issue.sh — Add a comment to a Linear issue
# Usage: comment-issue.sh "issue-id" "comment body (markdown)"
# Output: Comment ID written to stdout

set -euo pipefail

API_URL="https://api.linear.app/graphql"
API_KEY="${LINEAR_API_KEY:-}"
ISSUE_ID="${1:-}"
BODY="${2:-}"

if [ -z "$API_KEY" ]; then
  echo "Error: LINEAR_API_KEY not set" >&2
  exit 1
fi

if [ -z "$ISSUE_ID" ] || [ -z "$BODY" ]; then
  echo "Usage: comment-issue.sh \"issue-id\" \"comment body\"" >&2
  exit 1
fi

# Escape body for JSON
ESCAPED_BODY=$(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$BODY")

QUERY=$(cat <<EOF
{
  "query": "mutation(\$issueId: String!, \$body: String!) { commentCreate(input: { issueId: \$issueId, body: \$body }) { success comment { id body createdAt } } }",
  "variables": {
    "issueId": "$ISSUE_ID",
    "body": $ESCAPED_BODY
  }
}
EOF
)

RESPONSE=$(curl -s --max-time 30 \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$QUERY" \
  "$API_URL" 2>&1)

# Parse response
python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'errors' in data:
        for e in data['errors']:
            print(f\"Error: {e['message']}\", file=sys.stderr)
        sys.exit(1)
    comment = data['data']['commentCreate']['comment']
    print(comment['id'])
    print(f\"Comment added at {comment['createdAt']}\", file=sys.stderr)
except (json.JSONDecodeError, KeyError) as e:
    print(f'Error parsing response: {e}', file=sys.stderr)
    sys.exit(1)
" <<< "$RESPONSE"
