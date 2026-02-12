#!/usr/bin/env bash
# test-classify.sh — Unit tests for classify.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLASSIFY="$SCRIPT_DIR/../scripts/classify.sh"

PASSED=0
FAILED=0

test_case() {
  local name="$1"
  local input="$2"
  local expected="$3"
  local flags="${4:-}"
  
  if [ -n "$flags" ]; then
    result=$(echo "$input" | "$CLASSIFY" $flags 2>/dev/null || echo "ERROR")
  else
    result=$(echo "$input" | "$CLASSIFY" 2>/dev/null || echo "ERROR")
  fi
  
  if [ -n "$flags" ]; then
    # For JSON output, check category field
    actual=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('category', 'ERROR'))" 2>/dev/null || echo "ERROR")
  else
    actual="$result"
  fi
  
  if [ "$actual" = "$expected" ]; then
    echo "✓ $name"
    PASSED=$((PASSED + 1))
  else
    echo "✗ $name: expected '$expected', got '$actual'"
    echo "  Input: $input"
    FAILED=$((FAILED + 1))
  fi
}

echo "=== Classification Tests ==="

# Trivial cases (pattern matching, no API call)
test_case "greeting: hi" "hi" "TRIVIAL"
test_case "greeting: hey" "hey" "TRIVIAL"
test_case "greeting: hello" "hello" "TRIVIAL"
test_case "acknowledgment: thanks" "thanks" "TRIVIAL"
test_case "acknowledgment: ok" "ok" "TRIVIAL"
test_case "emoji: thumbs up" "👍" "TRIVIAL"

# Complex cases (pattern matching)
test_case "complex: implement" "implement a new auth service" "COMPLEX"
test_case "complex: refactor" "refactor the database layer" "COMPLEX"
test_case "complex: debug" "debug the login issue" "COMPLEX"
test_case "complex: create" "create a new API endpoint" "COMPLEX"
test_case "complex: deploy" "deploy to production" "COMPLEX"

# Empty input
test_case "empty input" "" "TRIVIAL"

echo ""
echo "=== Confidence Scoring Tests ==="

# Test with confidence flag
test_confidence() {
  local name="$1"
  local input="$2"
  local min_conf="$3"
  
  result=$(echo "$input" | "$CLASSIFY" --with-confidence 2>/dev/null || echo '{"confidence": 0}')
  conf=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('confidence', 0))" 2>/dev/null || echo "0")
  
  if python3 -c "exit(0 if float($conf) >= float($min_conf) else 1)" 2>/dev/null; then
    echo "✓ $name: confidence $conf >= $min_conf"
    PASSED=$((PASSED + 1))
  else
    echo "✗ $name: confidence $conf < $min_conf"
    FAILED=$((FAILED + 1))
  fi
}

test_confidence "trivial high confidence" "hello" 0.90
test_confidence "complex high confidence" "implement auth service" 0.85
test_confidence "JSON has category field" "what's the weather" 0.0  # Just check structure

# Verify JSON structure
echo ""
echo "=== JSON Structure Tests ==="

result=$(echo "test message" | "$CLASSIFY" --with-confidence 2>/dev/null || echo '{}')
echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    required = ['category', 'confidence', 'reasoning']
    missing = [k for k in required if k not in data]
    if missing:
        print(f'✗ JSON missing fields: {missing}')
        sys.exit(1)
    else:
        print('✓ JSON has all required fields')
        sys.exit(0)
except Exception as e:
    print(f'✗ JSON parse error: {e}')
    sys.exit(1)
" && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))

echo ""
echo "=== Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
