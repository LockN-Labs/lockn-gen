#!/usr/bin/env bash
# test-route.sh — Integration tests for route.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUTE="$SCRIPT_DIR/../scripts/route.sh"

PASSED=0
FAILED=0

test_route() {
  local name="$1"
  local input="$2"
  local expected_category="$3"
  local expected_spawned="$4"
  
  result=$(echo "$input" | "$ROUTE" 2>/dev/null || echo '{"category": "ERROR", "spawned": false}')
  
  actual_category=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('category', 'ERROR'))" 2>/dev/null || echo "ERROR")
  actual_spawned=$(echo "$result" | python3 -c "import json,sys; print(str(json.load(sys.stdin).get('spawned', False)).lower())" 2>/dev/null || echo "false")
  
  cat_ok=false
  spawn_ok=false
  
  if [ "$actual_category" = "$expected_category" ]; then
    cat_ok=true
  fi
  
  if [ "$actual_spawned" = "$expected_spawned" ]; then
    spawn_ok=true
  fi
  
  if [ "$cat_ok" = true ] && [ "$spawn_ok" = true ]; then
    echo "✓ $name"
    PASSED=$((PASSED + 1))
  else
    echo "✗ $name"
    [ "$cat_ok" = false ] && echo "  Category: expected '$expected_category', got '$actual_category'"
    [ "$spawn_ok" = false ] && echo "  Spawned: expected '$expected_spawned', got '$actual_spawned'"
    FAILED=$((FAILED + 1))
  fi
}

echo "=== Routing Tests ==="

# Trivial - no spawn
test_route "trivial: greeting" "hi" "TRIVIAL" "false"
test_route "trivial: thanks" "thanks" "TRIVIAL" "false"
test_route "trivial: emoji" "👍" "TRIVIAL" "false"

# Complex - spawn System 2
test_route "complex: implement" "implement the auth service" "COMPLEX" "true"
test_route "complex: refactor" "refactor the database layer" "COMPLEX" "true"
test_route "complex: debug" "debug the login issue" "COMPLEX" "true"

# Empty
test_route "empty input" "" "TRIVIAL" "false"

echo ""
echo "=== Response Structure Tests ==="

# Verify JSON structure with --full
result=$(echo "test message" | "$ROUTE" --full 2>/dev/null || echo '{}')
echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    required = ['response', 'category', 'confidence', 'spawned', 'system', 'latency_ms']
    missing = [k for k in required if k not in data]
    if missing:
        print(f'✗ JSON missing fields: {missing}')
        sys.exit(1)
    
    # Full mode should have additional fields
    if 'classification' not in data or 'original_message' not in data:
        print('✗ --full mode missing extended fields')
        sys.exit(1)
    
    print('✓ JSON has all required fields (including --full)')
    sys.exit(0)
except Exception as e:
    print(f'✗ JSON parse error: {e}')
    sys.exit(1)
" && PASSED=$((PASSED + 1)) || FAILED=$((FAILED + 1))

echo ""
echo "=== Latency Tests ==="

# Verify latency tracking
result=$(echo "hello" | "$ROUTE" 2>/dev/null)
latency=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('latency_ms', -1))" 2>/dev/null || echo "-1")

if [ "$latency" -gt 0 ] && [ "$latency" -lt 10000 ]; then
  echo "✓ Latency tracked: ${latency}ms"
  PASSED=$((PASSED + 1))
else
  echo "✗ Latency tracking failed: $latency"
  FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ "$FAILED" -gt 0 ]; then
  exit 1
fi
