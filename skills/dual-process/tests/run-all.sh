#!/usr/bin/env bash
# run-all.sh — Run all dual-process skill tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════╗"
echo "║  Dual-Process Thinking Skill Tests     ║"
echo "╚════════════════════════════════════════╝"
echo ""

TOTAL_PASSED=0
TOTAL_FAILED=0
SUITES_PASSED=0
SUITES_FAILED=0

run_suite() {
  local name="$1"
  local script="$2"
  
  echo "┌─────────────────────────────────────────"
  echo "│ $name"
  echo "└─────────────────────────────────────────"
  
  if bash "$script"; then
    echo ""
    SUITES_PASSED=$((SUITES_PASSED + 1))
  else
    echo ""
    SUITES_FAILED=$((SUITES_FAILED + 1))
  fi
}

# Make scripts executable
chmod +x "$SCRIPT_DIR/../scripts/"*.sh 2>/dev/null || true
chmod +x "$SCRIPT_DIR/"*.sh 2>/dev/null || true

# Run test suites
run_suite "Classification Tests" "./test-classify.sh"
run_suite "Escalation Tests" "./test-escalate.sh"
run_suite "Routing Tests" "./test-route.sh"

echo "╔════════════════════════════════════════╗"
echo "║  Final Summary                         ║"
echo "╚════════════════════════════════════════╝"
echo "Test Suites Passed: $SUITES_PASSED"
echo "Test Suites Failed: $SUITES_FAILED"

if [ "$SUITES_FAILED" -gt 0 ]; then
  echo ""
  echo "❌ Some tests failed!"
  exit 1
else
  echo ""
  echo "✅ All tests passed!"
  exit 0
fi
