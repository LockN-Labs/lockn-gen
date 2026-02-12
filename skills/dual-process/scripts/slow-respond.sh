#!/usr/bin/env bash
# slow-respond.sh — System 2 deep response generator using Qwen3-Coder-Next
# Usage: echo "user message" | slow-respond.sh [--context file.txt]
# Output: Detailed analytical response

set -euo pipefail

# Primary: GPU model on :11439, Fallback: CPU model on :11440
API_URL="${SYSTEM2_API_URL:-http://127.0.0.1:11439/v1/chat/completions}"
API_URL_FALLBACK="${SYSTEM2_API_URL_FALLBACK:-http://127.0.0.1:11440/v1/chat/completions}"
MODEL="${SYSTEM2_MODEL:-qwen3-coder-next}"
MAX_TOKENS="${SYSTEM2_MAX_TOKENS:-4096}"
TIMEOUT="${SYSTEM2_TIMEOUT:-300}"  # 5 min default for deep thinking

CONTEXT_FILE=""
SYSTEM_OVERRIDE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --context)
      CONTEXT_FILE="$2"
      shift 2
      ;;
    --system)
      SYSTEM_OVERRIDE="$2"
      shift 2
      ;;
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

MESSAGE=$(cat)

if [ -z "$MESSAGE" ]; then
  echo '{"error": "empty message", "success": false}'
  exit 1
fi

# Build context if provided
CONTEXT=""
if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
  CONTEXT=$(cat "$CONTEXT_FILE")
fi

# System prompt for deep analytical work
if [ -n "$SYSTEM_OVERRIDE" ]; then
  SYSTEM_PROMPT="$SYSTEM_OVERRIDE"
else
  SYSTEM_PROMPT="You are an expert AI assistant performing deep analytical work. Take your time to think through the problem carefully. Provide thorough, well-reasoned responses. When coding, write production-quality code with proper error handling and documentation."
fi

# Build the user message with context
if [ -n "$CONTEXT" ]; then
  USER_MESSAGE="Context:\n\`\`\`\n$CONTEXT\n\`\`\`\n\nTask:\n$MESSAGE"
else
  USER_MESSAGE="$MESSAGE"
fi

PAYLOAD=$(python3 -c "
import json
system = '''$SYSTEM_PROMPT'''
user = '''$USER_MESSAGE'''
print(json.dumps({
    'model': '$MODEL',
    'messages': [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user}
    ],
    'max_tokens': $MAX_TOKENS,
    'temperature': 0.2
}))
")

# Try primary GPU endpoint first
RESPONSE=$(curl -s --max-time "$TIMEOUT" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$API_URL" 2>/dev/null)

# Check if we got a valid response
VALID=$(echo "$RESPONSE" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if 'choices' in data and len(data['choices']) > 0:
        print('true')
    else:
        print('false')
except:
    print('false')
" 2>/dev/null || echo "false")

# Fallback to CPU endpoint if GPU failed
if [ "$VALID" = "false" ]; then
  >&2 echo "Warning: GPU endpoint failed, falling back to CPU endpoint"
  RESPONSE=$(curl -s --max-time "$TIMEOUT" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "$API_URL_FALLBACK" 2>/dev/null)
fi

# Parse and return result
python3 -c "
import json, sys, re, time

try:
    data = json.load(sys.stdin)
    if 'choices' in data and len(data['choices']) > 0:
        content = data['choices'][0]['message']['content'].strip()
        
        # Extract thinking if present (for logging/debugging)
        thinking = ''
        think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
        if think_match:
            thinking = think_match.group(1).strip()
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        
        # Calculate token usage if available
        usage = data.get('usage', {})
        
        print(json.dumps({
            'success': True,
            'response': content,
            'thinking': thinking if thinking else None,
            'tokens': {
                'prompt': usage.get('prompt_tokens', 0),
                'completion': usage.get('completion_tokens', 0),
                'total': usage.get('total_tokens', 0)
            },
            'model': data.get('model', '$MODEL'),
            'timestamp': int(time.time())
        }, indent=2))
    else:
        print(json.dumps({
            'success': False,
            'error': 'No valid response from model',
            'raw': str(data)[:500]
        }))
except Exception as e:
    print(json.dumps({
        'success': False,
        'error': str(e)
    }))
" <<< "$RESPONSE"
