#!/usr/bin/env bash
# test-escalate.sh — Unit tests for escalate.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ESCALATE="$SCRIPT_DIR/../scripts/escalate.sh"

PASSED=0
FAILED=0

test_escalation() {
  local name="$1"
  local message="$2"
  local response="$3"
  local confidence="$4"
  local category="$5"
  local expected_escalate="$6"
  
  input=$(python3 << EOF
import json
print(json.dumps({
    "message": "$message",
    "response": "$response",
    "confidence": $confidence,
    "category": "$category"
}))
EOF
)
  
  result=$(echo "$input" | "$ESCALATE" 2>/dev/null || echo '{"escalate": false}')
  actual=$(echo "$result" | python3 -c "import json,sys; print(str(json.load(sys.stdin).get('escalate', False)).lower())" 2>/dev/null || echo "false")
  
  if [ "$actual" = "$expected_escalate" ]; then
    echo "✓ $name"
    PASSED=$((PASSED + 1))
  else
    echo "✗ $name: expected escalate=$expected_escalate, got $actual"
    reason=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('reason', 'unknown'))" 2>/dev/null || echo "unknown")
    echo "  Reason: $reason"
    FAILED=$((FAILED + 1))
  fi
}

echo "=== Escalation Tests ==="

# Should NOT escalate
test_escalation "high confidence simple" \
  "how are you" \
  "Doing great, thanks for asking!" \
  0.95 "CONVERSATIONAL" "false"

test_escalation "trivial category" \
  "hello" \
  "Hi there, how are you?" \
  0.9 "TRIVIAL" "false"

# Should escalate - low confidence
test_escalation "low confidence" \
  "what is the best database" \
  "It depends on your use case" \
  0.5 "CONVERSATIONAL" "true"

# Should escalate - COMPLEX category  
test_escalation "complex category" \
  "implement new feature" \
  "On it!" \
  0.9 "COMPLEX" "true"

# Should escalate - uncertainty markers
test_escalation "uncertainty: not sure" \
  "what framework should I use" \
  "well i'm not sure, there are many options to consider" \
  0.8 "CONVERSATIONAL" "true"

test_escalation "uncertainty: maybe" \
  "is this approach good" \
  "Maybe we should consider alternatives" \
  0.8 "CONVERSATIONAL" "true"

# Should escalate - technical depth indicators
test_escalation "technical: how does" \
  "how does the auth system work" \
  "It uses JWT tokens" \
  0.85 "CONVERSATIONAL" "true"

test_escalation "technical: explain" \
  "explain the architecture" \
  "Sure, let me explain" \
  0.85 "CONVERSATIONAL" "true"

test_escalation "technical: best practice" \
  "what is the best practice for caching" \
  "Use Redis" \
  0.85 "CONVERSATIONAL" "true"

# Should escalate - response too short
test_escalation "short response" \
  "what should I do about the bug" \
  "Hmm" \
  0.8 "CONVERSATIONAL" "true"

echo ""
echo "=== Edge Cases ==="

# Empty input
result=$(echo "" | "$ESCALATE" 2>/dev/null)
if echo "$result" | python3 -c "import json,sys; exit(0 if not json.load(sys.stdin).get('escalate') else 1)" 2>/dev/null; then
  echo "✓ Empty input: no escalation"
  PASSED=$((PASSED + 1))
else
  echo "✗ Empty input: unexpected escalation"
  FAILED=$((FAILED + 1))
fi

# Invalid JSON
result=$(echo "not json" | "$ESCALATE" 2>/dev/null)
if echo "$result" | python3 -c "import json,sys; exit(0 if not json.load(sys.stdin).get('escalate') else 1)" 2>/dev/null; then
  echo "✓ Invalid JSON: no escalation (graceful)"
  PASSED=$((PASSED + 1))
else
  echo "✗ Invalid JSON: unexpected behavior"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
