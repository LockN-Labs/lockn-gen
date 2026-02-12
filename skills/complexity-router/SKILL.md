# Complexity Router Skill

Auto-escalates complex requests from Sonnet to Opus via `complex-cloud` subagent.

## Flow

1. **Score complexity** (0.00-10.00 scale) of incoming request
2. **If complexity_score > 8.21**: Spawn `complex-cloud` subagent (Opus) 
3. **If complexity_score ≤ 8.21**: Handle normally with Sonnet

## Complexity Scoring Criteria (0.00-10.00)

| Score Range | Category | Examples |
|-------------|----------|----------|
| 0.00-2.00 | **Trivial** | Status checks, simple questions, basic info retrieval |
| 2.01-4.00 | **Simple** | File operations, straightforward coding tasks, routine admin |
| 4.01-6.00 | **Moderate** | Multi-step workflows, analysis tasks, moderate debugging |
| 6.01-8.20 | **Complex** | Architecture decisions, complex analysis, cross-system integration |
| **8.21-10.00** | **Very Complex** | **→ ESCALATE TO OPUS** Strategic planning, novel problem-solving, high-stakes decisions |

## Usage

```bash
# Route a request through complexity analysis
complexity-router "Design a multi-tenant auth system with RBAC, SAML SSO, and audit logging"
# → Complexity: 9.2 → Spawns complex-cloud subagent

complexity-router "Check the status of port 11439"  
# → Complexity: 1.5 → Handles with Sonnet
```

## Scoring Factors

- **Cross-system dependencies** (+1 to +3)
- **Novel/research required** (+2 to +4) 
- **High-stakes/business impact** (+1 to +2)
- **Multi-domain expertise needed** (+1 to +3)
- **Strategic/long-term planning** (+2 to +4)
- **Ambiguous requirements** (+1 to +2)

## Implementation

Use this skill to wrap complex requests automatically. Sonnet scores, escalates when needed.