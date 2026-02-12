#!/usr/bin/env bash
# fast-respond.sh — System 1 fast response generator
# Usage: echo "user message" | fast-respond.sh [--spawning]
# Output: Quick response suitable for TTS

set -euo pipefail

API_URL="${SYSTEM1_API_URL:-http://127.0.0.1:11437/v1/chat/completions}"
MODEL="${SYSTEM1_MODEL:-qwen3-32b}"
MAX_TOKENS="${SYSTEM1_MAX_TOKENS:-128}"
TIMEOUT=10

SPAWNING=false
if [ "${1:-}" = "--spawning" ]; then
  SPAWNING=true
fi

MESSAGE=$(cat)

if [ -z "$MESSAGE" ]; then
  echo "Hey! What can I help you with?"
  exit 0
fi

if [ "$SPAWNING" = true ]; then
  # Generate acknowledgment for complex task
  SYSTEM_PROMPT="You are a helpful AI assistant. The user has asked for something that requires deep thinking/coding. Generate a brief, natural acknowledgment (1-2 sentences) that lets them know you're working on it. Be conversational and friendly. Examples:
- 'On it — I'll have that ready in a moment.'
- 'Good question! Let me dig into that. Back shortly.'
- 'Spawning the analysis now. I'll ping you when it's ready.'
Do NOT solve the problem. Just acknowledge and indicate you're spawning background work."
else
  # Normal conversational response
  SYSTEM_PROMPT="You are a helpful AI assistant having a real-time voice conversation. Be concise, natural, and conversational. Keep responses brief (1-3 sentences) since this will be spoken via TTS. Be friendly but efficient."
fi

PAYLOAD=$(cat <<EOF
{
  "model": "${MODEL}",
  "messages": [
    {"role": "system", "content": $(echo "$SYSTEM_PROMPT" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")},
    {"role": "user", "content": $(echo "$MESSAGE /no_think" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")}
  ],
  "max_tokens": ${MAX_TOKENS},
  "temperature": 0.7
}
EOF
)

RESPONSE=$(curl -s --max-time "$TIMEOUT" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$API_URL" 2>/dev/null || echo '{"error": true}')

echo "$RESPONSE" | python3 -c "
import json, sys, re
try:
    data = json.load(sys.stdin)
    if 'choices' in data:
        content = data['choices'][0]['message']['content'].strip()
        # Remove <think>...</think> blocks
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        print(content if content else 'Got it!')
    else:
        print('Let me think about that...')
except:
    print('One moment...')
"
