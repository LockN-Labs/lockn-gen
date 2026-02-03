#!/usr/bin/env bash
# dispatch.sh — Send a coding task to local Qwen3-Coder via llama.cpp API
# Usage: dispatch.sh "prompt" [--context file1 file2 ...]
#        echo "context" | dispatch.sh "prompt"
# Output: Generated code written to stdout

set -euo pipefail

API_URL="${CODER_API_URL:-http://127.0.0.1:11438/v1/chat/completions}"
MODEL="${CODER_MODEL:-qwen3-coder}"
MAX_TOKENS="${CODER_MAX_TOKENS:-4096}"
TEMPERATURE="${CODER_TEMPERATURE:-0.2}"
TIMEOUT="${CODER_TIMEOUT:-120}"

DEFAULT_SYSTEM="You are Qwen3-Coder, a specialized coding assistant. Output ONLY code. No explanations, no markdown fences unless the output is a markdown file. Follow the exact specifications given. Use modern best practices."
SYSTEM_PROMPT="${SYSTEM_PROMPT:-$DEFAULT_SYSTEM}"

if [ $# -lt 1 ]; then
  echo "Usage: dispatch.sh \"prompt\" [--context file1 file2 ...]" >&2
  exit 1
fi

PROMPT="$1"
shift

# Collect context from --context flag
CONTEXT=""
if [ "${1:-}" = "--context" ]; then
  shift
  for f in "$@"; do
    if [ -f "$f" ]; then
      CONTEXT="${CONTEXT}\n\n--- ${f} ---\n$(cat "$f")"
    else
      echo "Warning: context file not found: $f" >&2
    fi
  done
fi

# Collect context from stdin if piped
if [ ! -t 0 ]; then
  STDIN_CONTENT=$(cat)
  if [ -n "$STDIN_CONTENT" ]; then
    CONTEXT="${CONTEXT}\n\n--- stdin ---\n${STDIN_CONTENT}"
  fi
fi

# Build user message
USER_MSG="$PROMPT"
if [ -n "$CONTEXT" ]; then
  USER_MSG="${PROMPT}\n\nReference code:\n${CONTEXT}"
fi

# Escape for JSON
json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$1"
}

ESCAPED_SYSTEM=$(json_escape "$SYSTEM_PROMPT")
ESCAPED_USER=$(json_escape "$USER_MSG")

# Build request
PAYLOAD=$(cat <<EOF
{
  "model": "${MODEL}",
  "messages": [
    {"role": "system", "content": ${ESCAPED_SYSTEM}},
    {"role": "user", "content": ${ESCAPED_USER}}
  ],
  "max_tokens": ${MAX_TOKENS},
  "temperature": ${TEMPERATURE},
  "stream": false
}
EOF
)

# Send request
RESPONSE=$(curl -s --max-time "$TIMEOUT" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$API_URL" 2>&1)

# Extract content and usage
PARSED=$(echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'choices' in data and len(data['choices']) > 0:
        content = data['choices'][0]['message']['content']
        usage = data.get('usage', {})
        # Print content on first line, usage JSON on second
        print(content)
        print('__USAGE__' + json.dumps(usage))
    elif 'error' in data:
        print(f'ERROR: {data[\"error\"]}', file=sys.stderr)
        sys.exit(1)
    else:
        print(f'ERROR: Unexpected response: {json.dumps(data)[:200]}', file=sys.stderr)
        sys.exit(1)
except json.JSONDecodeError:
    print(f'ERROR: Non-JSON response: {sys.stdin.read()[:200]}', file=sys.stderr)
    sys.exit(1)
" 2>&1)

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
  echo "$PARSED" >&2
  exit $EXIT_CODE
fi

# Split content from usage marker
CONTENT=$(echo "$PARSED" | sed '/__USAGE__/,$d')
USAGE_LINE=$(echo "$PARSED" | grep '^__USAGE__' | sed 's/^__USAGE__//')

echo "$CONTENT"

# Log receipt to LockN Logger (best-effort, don't fail the dispatch)
if [ -n "$USAGE_LINE" ]; then
  PROMPT_TOKENS=$(echo "$USAGE_LINE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('prompt_tokens', d.get('input_tokens', 0)))" 2>/dev/null || echo 0)
  COMPLETION_TOKENS=$(echo "$USAGE_LINE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('completion_tokens', d.get('output_tokens', 0)))" 2>/dev/null || echo 0)

  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  LOG_RECEIPT="${SCRIPT_DIR}/../../lockn-logger/scripts/log-receipt.sh"

  # Also check the workspace skills path
  if [ ! -f "$LOG_RECEIPT" ]; then
    LOG_RECEIPT="$(dirname "$SCRIPT_DIR")/../lockn-logger/scripts/log-receipt.sh"
  fi
  if [ ! -f "$LOG_RECEIPT" ]; then
    LOG_RECEIPT="/home/sean/.openclaw/workspace/lockn-logger/skills/lockn-logger/scripts/log-receipt.sh"
  fi

  if [ -f "$LOG_RECEIPT" ] && [ "$PROMPT_TOKENS" -gt 0 ] 2>/dev/null; then
    bash "$LOG_RECEIPT" \
      --session-id "dispatch:coding-pipeline" \
      --model "${MODEL}" \
      --provider "local" \
      --input-tokens "$PROMPT_TOKENS" \
      --output-tokens "$COMPLETION_TOKENS" \
      --cost 0 \
      --source "coding-pipeline" \
      2>/dev/null &
  fi
fi
