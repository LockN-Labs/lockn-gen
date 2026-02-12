#!/usr/bin/env bash
# route.sh — Main dual-process router with confidence scoring and escalation
# Usage: echo "user message" | route.sh [--full]
# Output: JSON with response, category, confidence, and optional spawn info

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FULL_OUTPUT=false
if [ "${1:-}" = "--full" ]; then
  FULL_OUTPUT=true
fi

MESSAGE=$(cat)

if [ -z "$MESSAGE" ]; then
  echo '{"response": "Hey!", "category": "TRIVIAL", "confidence": 1.0, "spawned": false}'
  exit 0
fi

# Step 1: Classify intent with confidence scoring
CLASSIFICATION=$("$SCRIPT_DIR/classify.sh" --with-confidence <<< "$MESSAGE" 2>/dev/null)

CATEGORY=$(echo "$CLASSIFICATION" | python3 -c "import json,sys; print(json.load(sys.stdin).get('category', 'CONVERSATIONAL'))" 2>/dev/null || echo "CONVERSATIONAL")
CONFIDENCE=$(echo "$CLASSIFICATION" | python3 -c "import json,sys; print(json.load(sys.stdin).get('confidence', 0.5))" 2>/dev/null || echo "0.5")
REASONING=$(echo "$CLASSIFICATION" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reasoning', 'unknown'))" 2>/dev/null || echo "unknown")

# Step 2: Generate response based on category
START_TIME=$(date +%s%3N)

case "$CATEGORY" in
  TRIVIAL)
    RESPONSE=$("$SCRIPT_DIR/fast-respond.sh" <<< "$MESSAGE" 2>/dev/null || echo "Hey!")
    SPAWNED=false
    SYSTEM="1"
    ;;
  
  CONVERSATIONAL)
    RESPONSE=$("$SCRIPT_DIR/fast-respond.sh" <<< "$MESSAGE" 2>/dev/null || echo "Let me think...")
    SPAWNED=false
    SYSTEM="1"
    ESCALATION_REASON=""
    
    # Check if escalation is needed
    ESCALATION_INPUT=$(python3 -c "
import json
print(json.dumps({
    'message': '''$MESSAGE''',
    'response': '''$RESPONSE''',
    'confidence': $CONFIDENCE,
    'category': '$CATEGORY'
}))
")
    ESCALATION=$("$SCRIPT_DIR/escalate.sh" <<< "$ESCALATION_INPUT" 2>/dev/null || echo '{"escalate": false}')
    SHOULD_ESCALATE=$(echo "$ESCALATION" | python3 -c "import json,sys; print(str(json.load(sys.stdin).get('escalate', False)).lower())" 2>/dev/null || echo "false")
    ESCALATION_REASON=$(echo "$ESCALATION" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason', ''))" 2>/dev/null || echo "")
    
    if [ "$SHOULD_ESCALATE" = "true" ]; then
      # Escalate: provide quick ack, spawn System 2
      RESPONSE=$("$SCRIPT_DIR/fast-respond.sh" --spawning <<< "$MESSAGE" 2>/dev/null || echo "Let me look into that more carefully...")
      SPAWNED=true
      SYSTEM="1→2"
      CATEGORY="ESCALATED"
    fi
    ;;
  
  COMPLEX)
    # Fast acknowledgment + spawn System 2
    RESPONSE=$("$SCRIPT_DIR/fast-respond.sh" --spawning <<< "$MESSAGE" 2>/dev/null || echo "On it!")
    SPAWNED=true
    SYSTEM="2"
    ;;
  
  *)
    RESPONSE="I'm here! What can I help with?"
    CATEGORY="CONVERSATIONAL"
    SPAWNED=false
    SYSTEM="1"
    ESCALATION_REASON=""
    ;;
esac

# Ensure ESCALATION_REASON is set
ESCALATION_REASON="${ESCALATION_REASON:-}"

END_TIME=$(date +%s%3N)
LATENCY=$((END_TIME - START_TIME))

# Build output JSON
SPAWNED_PY=$([[ "$SPAWNED" == "true" ]] && echo "True" || echo "False")
FULL_PY=$([[ "$FULL_OUTPUT" == "true" ]] && echo "True" || echo "False")

python3 << PYSCRIPT
import json

result = {
    'response': '''$(echo "$RESPONSE" | sed "s/'/\\\\'/g")''',
    'category': '$CATEGORY',
    'confidence': $CONFIDENCE,
    'spawned': $SPAWNED_PY,
    'system': '$SYSTEM',
    'latency_ms': $LATENCY
}

if $FULL_PY:
    result['classification'] = {
        'reasoning': '$REASONING',
        'original_category': '$CATEGORY' if '$CATEGORY' != 'ESCALATED' else 'CONVERSATIONAL'
    }
    if '$SPAWNED' == 'true' and '$CATEGORY' == 'ESCALATED':
        result['escalation_reason'] = '$ESCALATION_REASON'
    result['original_message'] = '''$(echo "$MESSAGE" | sed "s/'/\\\\'/g")'''

print(json.dumps(result, indent=2))
PYSCRIPT
