#!/usr/bin/env bash
# classify.sh — Quick intent classification for dual-process routing
# Usage: echo "user message" | classify.sh [--with-confidence]
# Output: TRIVIAL | CONVERSATIONAL | COMPLEX
# With --with-confidence: JSON with category and confidence score

set -euo pipefail

API_URL="${ROUTER_API_URL:-http://127.0.0.1:11437/v1/chat/completions}"
MODEL="${ROUTER_MODEL:-qwen3-32b}"
TIMEOUT=5  # Must be fast

WITH_CONFIDENCE=false
if [ "${1:-}" = "--with-confidence" ]; then
  WITH_CONFIDENCE=true
fi

# Read message from stdin
MESSAGE=$(cat)

if [ -z "$MESSAGE" ]; then
  if [ "$WITH_CONFIDENCE" = true ]; then
    echo '{"category": "TRIVIAL", "confidence": 1.0, "reasoning": "empty message"}'
  else
    echo "TRIVIAL"
  fi
  exit 0
fi

# Quick heuristics before hitting the model (System 0.5)
# These have high confidence because they're deterministic patterns
MSG_LOWER=$(echo "$MESSAGE" | tr '[:upper:]' '[:lower:]')
WORD_COUNT=$(echo "$MESSAGE" | wc -w)

# Trivial patterns - very short messages with greeting/ack keywords
if [ "$WORD_COUNT" -le 3 ] && echo "$MSG_LOWER" | grep -qE '^(hi|hey|hello|thanks|thank you|ok|okay|sure|yes|no|yep|nope|cool|nice|great|good|bye|later|yo|sup|👍|🙏|❤️|lol|haha|lmao)[!?.]*$'; then
  if [ "$WITH_CONFIDENCE" = true ]; then
    echo '{"category": "TRIVIAL", "confidence": 0.95, "reasoning": "pattern match: greeting/ack"}'
  else
    echo "TRIVIAL"
  fi
  exit 0
fi

# Complex patterns - strong keywords that indicate deep work
COMPLEX_KEYWORDS='(implement|refactor|create|build|fix|debug|analyze|research|design|architect|write code|add feature|update|deploy|migrate|optimize|investigate|develop|code review|pull request|pr review|test coverage|explain how|walk me through|deep dive)'
if echo "$MSG_LOWER" | grep -qE "$COMPLEX_KEYWORDS"; then
  if [ "$WITH_CONFIDENCE" = true ]; then
    echo '{"category": "COMPLEX", "confidence": 0.90, "reasoning": "pattern match: complex keyword"}'
  else
    echo "COMPLEX"
  fi
  exit 0
fi

# For ambiguous cases, use the model with confidence scoring
PAYLOAD=$(cat <<EOF
{
  "model": "${MODEL}",
  "messages": [
    {"role": "system", "content": "Classify the user message into exactly one category and provide a confidence score (0.0-1.0).\n\nCategories:\n- TRIVIAL: greetings, thanks, simple yes/no, acknowledgments, emojis, casual small talk\n- CONVERSATIONAL: discussion, opinions, clarification, questions, status checks, simple requests\n- COMPLEX: coding, implementation, analysis, research, planning, debugging, multi-step tasks, technical work\n\nRespond in this exact format:\nCATEGORY: <category>\nCONFIDENCE: <0.0-1.0>\nREASONING: <brief reason>"},
    {"role": "user", "content": $(echo "$MESSAGE /no_think" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))")}
  ],
  "max_tokens": 50,
  "temperature": 0
}
EOF
)

RESPONSE=$(curl -s --max-time "$TIMEOUT" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "$API_URL" 2>/dev/null || echo '{"error": true}')

if [ "$WITH_CONFIDENCE" = true ]; then
  python3 -c "
import json, sys, re

try:
    data = json.load(sys.stdin)
    if 'choices' in data:
        content = data['choices'][0]['message']['content'].strip()
        # Remove <think>...</think> blocks
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        
        # Parse structured response
        category = 'CONVERSATIONAL'
        confidence = 0.6
        reasoning = 'model classification'
        
        for line in content.split('\n'):
            line = line.strip()
            if line.upper().startswith('CATEGORY:'):
                cat = line.split(':', 1)[1].strip().upper()
                if cat in ['TRIVIAL', 'CONVERSATIONAL', 'COMPLEX']:
                    category = cat
            elif line.upper().startswith('CONFIDENCE:'):
                try:
                    conf = float(line.split(':', 1)[1].strip())
                    if 0.0 <= conf <= 1.0:
                        confidence = conf
                except:
                    pass
            elif line.upper().startswith('REASONING:'):
                reasoning = line.split(':', 1)[1].strip()
        
        print(json.dumps({'category': category, 'confidence': confidence, 'reasoning': reasoning}))
    else:
        print(json.dumps({'category': 'CONVERSATIONAL', 'confidence': 0.5, 'reasoning': 'api error fallback'}))
except Exception as e:
    print(json.dumps({'category': 'CONVERSATIONAL', 'confidence': 0.5, 'reasoning': 'parse error fallback'}))
" <<< "$RESPONSE"
else
  python3 -c "
import json, sys, re
try:
    data = json.load(sys.stdin)
    if 'choices' in data:
        content = data['choices'][0]['message']['content'].strip()
        # Remove <think>...</think> blocks
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip().upper()
        # Extract just the category word
        for cat in ['TRIVIAL', 'CONVERSATIONAL', 'COMPLEX']:
            if cat in content:
                print(cat)
                sys.exit(0)
        print('CONVERSATIONAL')
    else:
        print('CONVERSATIONAL')
except:
    print('CONVERSATIONAL')
" <<< "$RESPONSE"
fi
