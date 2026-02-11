#!/bin/bash
set -euo pipefail

# Complexity Router - Auto-escalate complex tasks to Opus via complex-cloud subagent
# Usage: ./route.sh "task description"

TASK="$1"
THRESHOLD=8.21
GUARDRAILS_ENABLED="${LOCKN511_GUARDRAILS_ENABLED:-false}"

if [[ "$GUARDRAILS_ENABLED" == "true" ]]; then
  echo "🛡️ LOCKN-511 guardrails enabled; evaluating escalation safety..."
  GUARD_JSON=$(python3 /home/sean/.openclaw/workspace/scripts/lockn511_guard_eval.py \
    --tool exec \
    --intent "$TASK" \
    --payload "{\"command\": \"$TASK\"}" 2>/dev/null || true)

  if echo "$GUARD_JSON" | jq -e '.route == "cloud"' >/dev/null 2>&1; then
    echo "🚫 Local execution blocked by guardrails (risk: $(echo "$GUARD_JSON" | jq -r '.risk'))"
    echo "☁️ Escalating to cloud approval path"
    openclaw spawn \
      --agent complex-cloud \
      --task "$TASK" \
      --cleanup delete \
      --label "LOCKN-511 escalation"
    exit 0
  fi
fi

echo "🧠 Analyzing task complexity..."

# Score complexity using local Qwen3-32B (fast, free scoring)
COMPLEXITY_JSON=$(curl -s -X POST "http://127.0.0.1:11437/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-no-key-required" \
  -d "{
    \"model\": \"qwen3-32b-q5k\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a complexity scoring agent. Score tasks 0.00-10.00 based on:\n\nFACTORS:\n- Cross-system dependencies (+1 to +3)\n- Novel/research required (+2 to +4)\n- High-stakes/business impact (+1 to +2) \n- Multi-domain expertise needed (+1 to +3)\n- Strategic/long-term planning (+2 to +4)\n- Ambiguous requirements (+1 to +2)\n\nSCALE:\n0.00-2.00: Trivial (status, simple questions)\n2.01-4.00: Simple (files, basic coding, admin)\n4.01-6.00: Moderate (workflows, analysis, debugging)\n6.01-8.20: Complex (architecture, integration)\n8.21-10.00: Very Complex (strategic, novel, high-stakes)\n\nRespond ONLY with valid JSON: {\\\"score\\\": X.XX, \\\"reasoning\\\": \\\"brief explanation\\\"}\"
      },
      {
        \"role\": \"user\",
        \"content\": \"Score this task: ${TASK}\"
      }
    ],
    \"temperature\": 0.1,
    \"max_tokens\": 200
  }")

# Extract score and reasoning
SCORE=$(echo "$COMPLEXITY_JSON" | jq -r '.choices[0].message.content' | jq -r '.score')
REASONING=$(echo "$COMPLEXITY_JSON" | jq -r '.choices[0].message.content' | jq -r '.reasoning')

echo "📊 Complexity Score: $SCORE/10.00"
echo "💭 Reasoning: $REASONING"

# Compare score to threshold (bash doesn't do float comparison well)
if (( $(echo "$SCORE > $THRESHOLD" | bc -l) )); then
    echo "🚀 ESCALATING to complex-cloud subagent (Opus)"
    echo "📤 Spawning Opus for high-complexity task..."
    
    # Spawn complex-cloud subagent 
    openclaw spawn \
        --agent complex-cloud \
        --task "$TASK" \
        --cleanup delete \
        --label "Complexity: $SCORE (escalated)"
        
else
    echo "✅ HANDLING with Sonnet (complexity ≤ $THRESHOLD)"
    echo "📝 Processing task with current agent..."
    
    # Handle with current agent (Sonnet)
    echo "Task: $TASK"
    echo "Result: [Handle this task normally - complexity under threshold]"
fi