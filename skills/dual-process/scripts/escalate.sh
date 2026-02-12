#!/usr/bin/env bash
# escalate.sh — Determine if System 1 response needs escalation to System 2
# Usage: echo '{"message":"...", "response":"...", "confidence":0.7}' | escalate.sh
# Output: JSON with escalate decision and reasoning

set -euo pipefail

API_URL="${ROUTER_API_URL:-http://127.0.0.1:11437/v1/chat/completions}"
MODEL="${ROUTER_MODEL:-qwen3-32b}"
TIMEOUT=5

# Thresholds for escalation
CONFIDENCE_THRESHOLD="${CONFIDENCE_THRESHOLD:-0.70}"
RESPONSE_LENGTH_MIN="${RESPONSE_LENGTH_MIN:-10}"

INPUT=$(cat)

if [ -z "$INPUT" ]; then
  echo '{"escalate": false, "reason": "empty input"}'
  exit 0
fi

# Parse input JSON
RESULT=$(python3 -c "
import json, sys

try:
    data = json.load(sys.stdin)
    message = data.get('message', '')
    response = data.get('response', '')
    confidence = data.get('confidence', 1.0)
    category = data.get('category', 'CONVERSATIONAL')
    
    # Quick checks that don't need model
    escalate = False
    reason = 'no escalation needed'
    
    # Already complex - should have been routed to System 2
    if category == 'COMPLEX':
        print(json.dumps({'escalate': True, 'reason': 'category was COMPLEX', 'fast_check': True}))
        sys.exit(0)
    
    # Low confidence classification
    if confidence < $CONFIDENCE_THRESHOLD:
        print(json.dumps({'escalate': True, 'reason': f'low confidence ({confidence:.2f} < $CONFIDENCE_THRESHOLD)', 'fast_check': True}))
        sys.exit(0)
    
    # Response too short (might indicate uncertainty)
    if len(response.strip()) < $RESPONSE_LENGTH_MIN:
        print(json.dumps({'escalate': True, 'reason': 'response too short', 'fast_check': True}))
        sys.exit(0)
    
    # Response contains uncertainty markers
    uncertainty_markers = ['i\\'m not sure', 'i don\\'t know', 'unclear', 'might need', 'could be wrong', 'let me think', 'hmm', 'possibly', 'maybe we should']
    response_lower = response.lower()
    for marker in uncertainty_markers:
        if marker in response_lower:
            print(json.dumps({'escalate': True, 'reason': f'uncertainty detected: {marker}', 'fast_check': True}))
            sys.exit(0)
    
    # Check for questions that need technical depth
    technical_indicators = ['how does', 'why does', 'explain', 'what\\'s the difference', 'compare', 'best practice', 'architecture', 'trade-off', 'performance']
    message_lower = message.lower()
    for indicator in technical_indicators:
        if indicator in message_lower:
            print(json.dumps({'escalate': True, 'reason': f'technical depth needed: {indicator}', 'fast_check': True}))
            sys.exit(0)
    
    # All quick checks passed - no escalation
    print(json.dumps({'escalate': False, 'reason': 'passed all quick checks', 'fast_check': True}))
    
except json.JSONDecodeError:
    print(json.dumps({'escalate': False, 'reason': 'invalid JSON input', 'error': True}))
except Exception as e:
    print(json.dumps({'escalate': False, 'reason': str(e), 'error': True}))
" <<< "$INPUT")

echo "$RESULT"
