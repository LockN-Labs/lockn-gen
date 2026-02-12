---
name: dual-process
description: Kahneman-inspired dual-process thinking. Routes simple queries to fast System 1 (Qwen3-32B on :11437) and complex queries to slow System 2 (Qwen3-Coder-Next on :11439). Includes confidence scoring and automatic escalation when System 1 responses need deeper analysis.
---

# Dual-Process Thinking Skill

Implements Kahneman's "Thinking, Fast and Slow" cognitive model for AI routing:
- **System 1 (Fast)**: Intuitive, quick responses for simple queries
- **System 2 (Slow)**: Analytical, deep responses for complex tasks

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Message                          │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│              classify.sh (System 0: Router)              │
│           Quick intent classification (~50ms)            │
│                                                          │
│  Categories + Confidence Scoring:                        │
│  • TRIVIAL (0.95+): greetings, acknowledgments          │
│  • CONVERSATIONAL (0.6-0.9): discussion, questions      │
│  • COMPLEX (0.85+): coding, analysis, planning          │
└─────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────┐         ┌──────────┐         ┌──────────┐
    │ TRIVIAL  │         │  CONV +  │         │ COMPLEX  │
    │ System 1 │         │ escalate │         │ System 2 │
    └────┬─────┘         └────┬─────┘         └────┬─────┘
         ↓                    ↓                    ↓
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│fast-respond.sh  │   │ escalate.sh →   │   │ slow-respond.sh │
│ Qwen3-32B       │   │ spawn System 2  │   │ Qwen3-Coder-Next│
│ :11437          │   │ if needed       │   │ :11439 (GPU)    │
│ 200-500ms       │   └─────────────────┘   │ :11440 (CPU fb) │
│ 256 tokens max  │                         │ 10s-5min        │
└─────────────────┘                         │ 4096 tokens     │
                                            └─────────────────┘
```

## Model Endpoints

| System | Model | Endpoint | Context | VRAM |
|--------|-------|----------|---------|------|
| Router (System 0) | Qwen3-32B | http://127.0.0.1:11437/v1 | 65K | ~23 GB |
| Fast (System 1) | Qwen3-32B | http://127.0.0.1:11437/v1 | 65K | ~23 GB |
| Slow (System 2) | Qwen3-Coder-Next Q5 | http://127.0.0.1:11439/v1 | 1M | ~57 GB |
| Slow Fallback | Qwen3-Coder-Next Q3 | http://127.0.0.1:11440/v1 | 2M | CPU |

## Scripts

### classify.sh — Intent Classification
```bash
# Basic classification
echo "implement auth service" | ./scripts/classify.sh
# Output: COMPLEX

# With confidence scoring
echo "what's the weather" | ./scripts/classify.sh --with-confidence
# Output: {"category": "CONVERSATIONAL", "confidence": 0.75, "reasoning": "model classification"}
```

**Confidence Thresholds:**
- `>= 0.90`: High confidence, pattern-matched
- `0.70-0.90`: Model-classified, reliable
- `< 0.70`: Low confidence, may escalate

### fast-respond.sh — System 1 Responses
```bash
# Normal response
echo "how are you" | ./scripts/fast-respond.sh
# Output: "Doing well! What can I help you with?"

# Spawning acknowledgment (for complex tasks)
echo "refactor the auth" | ./scripts/fast-respond.sh --spawning
# Output: "On it — spawning that analysis now. I'll ping you when it's ready."
```

### slow-respond.sh — System 2 Deep Analysis
```bash
# Basic deep response
echo "explain the microservices architecture" | ./scripts/slow-respond.sh
# Output: JSON with full analytical response

# With file context
cat ./src/auth.ts | ./scripts/slow-respond.sh --context ./context.txt

# Custom timeout
echo "analyze this codebase" | ./scripts/slow-respond.sh --timeout 600
```

### escalate.sh — Escalation Logic
Determines if a System 1 response should be escalated to System 2.

```bash
echo '{"message":"how does auth work", "response":"It uses JWT", "confidence":0.8, "category":"CONVERSATIONAL"}' | ./scripts/escalate.sh
# Output: {"escalate": true, "reason": "technical depth needed: how does"}
```

**Escalation Triggers:**
- Low confidence (`< 0.70`)
- COMPLEX category
- Response too short (`< 10 chars`)
- Uncertainty markers ("I'm not sure", "maybe", etc.)
- Technical depth indicators ("how does", "explain", "architecture", etc.)

### route.sh — Main Router
```bash
# Basic routing
echo "hello" | ./scripts/route.sh
# Output: {"response": "Hey there!", "category": "TRIVIAL", "confidence": 0.95, "spawned": false, "system": "1", "latency_ms": 245}

# Full output with classification details
echo "implement new feature" | ./scripts/route.sh --full
# Output includes: classification reasoning, escalation reason, original message
```

## Configuration

Environment variables for customization:

```bash
# Router/Classifier
export ROUTER_API_URL="http://127.0.0.1:11437/v1/chat/completions"
export ROUTER_MODEL="qwen3-32b"

# System 1 (Fast)
export SYSTEM1_API_URL="http://127.0.0.1:11437/v1/chat/completions"
export SYSTEM1_MODEL="qwen3-32b"
export SYSTEM1_MAX_TOKENS=128

# System 2 (Slow)
export SYSTEM2_API_URL="http://127.0.0.1:11439/v1/chat/completions"
export SYSTEM2_API_URL_FALLBACK="http://127.0.0.1:11440/v1/chat/completions"
export SYSTEM2_MODEL="qwen3-coder-next"
export SYSTEM2_MAX_TOKENS=4096
export SYSTEM2_TIMEOUT=300

# Escalation thresholds
export CONFIDENCE_THRESHOLD=0.70
export RESPONSE_LENGTH_MIN=10
```

## Confidence Scoring

The classification system uses a tiered approach:

1. **Pattern Matching (System 0.5)** — Deterministic, ~95% confidence
   - Greeting patterns: `^(hi|hey|hello|thanks|ok|👍)$`
   - Complex keywords: `(implement|refactor|debug|analyze|deploy)`

2. **Model Classification (System 0)** — Probabilistic, 50-90% confidence
   - Uses Qwen3-32B for ambiguous cases
   - Returns structured `CATEGORY: / CONFIDENCE: / REASONING:` format

3. **Escalation Override** — Can bump CONVERSATIONAL → COMPLEX
   - Low confidence triggers
   - Uncertainty markers in response
   - Technical depth indicators in query

## Example Flows

### Flow 1: Trivial (No Spawn)
```
User: "hey"
→ classify.sh: TRIVIAL (0.95, pattern match)
→ fast-respond.sh: "Hey! What's up?"
→ Output: immediate response, no spawn
```

### Flow 2: Complex (Spawn System 2)
```
User: "refactor the auth service to use OAuth2"
→ classify.sh: COMPLEX (0.90, keyword match)
→ fast-respond.sh --spawning: "On it — I'll have that ready shortly."
→ slow-respond.sh: (spawned in background)
→ Output: quick ack, spawned=true
```

### Flow 3: Escalated (System 1 → System 2)
```
User: "how does the caching layer work"
→ classify.sh: CONVERSATIONAL (0.75, ambiguous)
→ fast-respond.sh: "It uses Redis for session storage"
→ escalate.sh: TRUE (technical depth: "how does")
→ fast-respond.sh --spawning: "Let me dig into that more..."
→ slow-respond.sh: (spawned for deeper analysis)
→ Output: quick ack, spawned=true, category=ESCALATED
```

## Testing

```bash
# Run all tests
./tests/run-all.sh

# Individual test suites
./tests/test-classify.sh    # Classification tests
./tests/test-escalate.sh    # Escalation logic tests
./tests/test-route.sh       # Integration tests
```

## Metrics (for Observability)

Track these metrics for monitoring:

| Metric | Description |
|--------|-------------|
| `dual_process.classify.trivial` | Count of TRIVIAL classifications |
| `dual_process.classify.conversational` | Count of CONVERSATIONAL |
| `dual_process.classify.complex` | Count of COMPLEX |
| `dual_process.escalation.triggered` | Times System 1 escalated to 2 |
| `dual_process.system1.latency_ms` | Time to first response |
| `dual_process.system2.latency_ms` | Deep thinking duration |
| `dual_process.confidence.avg` | Average classification confidence |

## Benefits

1. **Responsiveness** — User gets immediate feedback for all queries
2. **Efficiency** — Simple queries don't waste GPU on deep models
3. **Quality** — Complex tasks get full analytical treatment
4. **Natural UX** — Feels like talking to someone who says "let me think..."
5. **Cost Optimization** — Routes appropriately based on query complexity
6. **Confidence Awareness** — Knows when it's uncertain and escalates

## Integration with OpenClaw

When `spawned=true`, the caller should use OpenClaw's `sessions_spawn` to run System 2:

```javascript
const result = await route(userMessage);
if (result.spawned) {
  // Send quick acknowledgment via TTS
  await tts(result.response);
  
  // Spawn System 2 in background
  await sessions_spawn({
    task: userMessage,
    agentId: "local-coder",  // Qwen3-Coder-Next
    label: "system2-analysis",
    onComplete: (response) => {
      // Deliver result when ready
      await notify(response);
    }
  });
}
```
