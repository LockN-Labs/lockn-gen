# Codex → Local Worker Workflow

## Overview

Codex (gpt-5.2-codex) acts as **orchestrator/architect**, while local Qwen3-Coder instances (Q6_K, 23.4GB) handle **implementation and QA**. This pattern maximizes token efficiency by offloading 90%+ of coding tasks to local models.

## Pipeline Flow

```
┌─────────────────────────────────┐
│  Codex (gpt-5.2-codex)         │
│  • Reads ticket/spec            │
│  • Designs solution             │
│  • Breaks into subtasks         │
│  • Reviews worker output        │
│  • Creates PR                   │
└──────────┬──────────────────────┘
           │ delegates via tmux/API
    ┌──────┴──────┐
    ▼             ▼
┌────────┐  ┌────────┐
│ Coder1 │  │ Coder2 │  (Qwen3-Coder local, port 11438)
│ impl   │  │ tests  │
└────────┘  └────────┘
```

## Workflow Steps

### 1. Codex Reads & Designs
```
INPUT: GitHub issue, task spec, or requirement
OUTPUT: Solution design, file list, interfaces, subtask breakdown
```

**Codex actions:**
- Analyze requirements
- Design architecture
- Identify files to modify/create
- Define interfaces and contracts
- Break down into logical subtasks

### 2. Codex Generates Subtask Prompts
```
Each subtask receives:
- Specific task description
- Target file(s)
- Required interfaces
- Acceptance criteria
- Constraints (type safety, performance, etc.)
```

**Example subtask:**
> "Implement `GetReceiptById(int id)` in ReceiptService.cs. Returns `ReceiptDto?` or null. Use EF Core repository pattern. Add unit tests covering happy path and not-found case."

### 3. Subtasks Dispatched to Local Workers
- **Parallel execution** of independent subtasks
- Each task runs in separate tmux session or llama.cpp API call
- Workers return: code output, test results, errors

### 4. Codex Reviews Results
```
INPUT: Worker outputs (code + tests)
OUTPUT: Approve, request fixes, or re-delegate
```

**Review checklist:**
- Code follows design
- Tests are comprehensive
- No regressions
- Interfaces are compatible
- Documentation is adequate

### 5. Codex Assembles & Creates PR
- Merge approved worker outputs
- Add PR description with summary
- Reference original issue
- Include link to worker run logs

## Local Worker Configuration

### llama.cpp Service
```bash
# Port 11438 (configured)
./llama-server \
  -m ~/models/Qwen3-Coder-30B-A3B-Q6_K.gguf \
  -ngl 33 \
  -c 8192 \
  -p 2048 \
  -n 2048 \
  --port 11438 \
  -fa \
  -cnv
```

### Worker Prompts
Workers receive the **same system prompt**:
```
You are Qwen3-Coder, a specialized coding assistant. Your task is to implement code according to specifications.

Guidelines:
- Follow .NET/C# best practices
- Write clean, maintainable code
- Include comprehensive unit tests
- Use existing patterns from the codebase
- Return only code and tests (no explanations)
```

## Token Savings Estimate

| Task | Cloud Model | Local Model | Savings |
|------|-------------|-------------|---------|
| Solution design | 5k tokens | — | — |
| Code generation | 20k tokens/task | 0 tokens | 100% |
| Test generation | 8k tokens | 0 tokens | 100% |
| Review | 3k tokens | — | — |
| **Total** | **36k tokens** | **0 tokens** | **100%** |

## Implementation

### Option A: Codex Instructions (Recommended First Step)
Update Codex's behavior by modifying its prompts to:
1. Always delegate coding tasks to local Qwen3-Coder
2. Always generate tests for new code
3. Always review worker output before approving

### Option B: Formal Skill
Create a reusable `coding-pipeline` skill with scripts:
- `dispatch-task.sh` — spawns local worker
- `review-output.sh` — validates worker results
- `merge-results.sh` — combines approved changes

### Option C: Custom Orchestration
Python/bash script that manages:
- Parallel task execution
- Worker result collection
- PR assembly
- Error handling and retries

## Monitoring

Track:
- **Worker latency** — time per subtask completion
- **Token usage** — cloud vs local
- **Success rate** — approvals vs re-delegations
- **Throughput** — subtasks per hour

## Error Handling

- **Worker timeout** — re-delegate to new worker
- **Code compilation errors** — worker returns error, Codex fixes and re-delegates
- **Test failures** — Codex reviews, requests fixes, re-delegates
- **Conflicting changes** — Codex resolves conflicts, re-delegates affected subtasks

## Future Enhancements

1. **Dynamic task sizing** — adjust subtask granularity based on complexity
2. **Caching** — cache common code patterns to avoid redundant generation
3. **Quality gates** — automated linting/style checks before merging
4. **Rollback** — automatic PR rollback on critical failures
5. **Metrics dashboard** — track worker performance and token savings

## References

- Qwen3-Coder: https://huggingface.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF
- llama.cpp: https://github.com/ggerganov/llama.cpp
- .NET Coding Standards: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
