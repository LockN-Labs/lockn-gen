# LockN Brain — Project Brief

## Status
- **Phase:** mvp (existing foundation) → growth (expanded cognitive framework)
- **Confidence:** 0.85
- **Last Verified:** 2026-02-10

## Overview
LockN Brain is the cognitive orchestration framework for the LockN ecosystem — the nervous system that makes every other module intelligent. Inspired by Kahneman's "Thinking Fast and Slow," it separates fast acknowledgments from deep analysis, retrieves context from vector stores, routes requests to optimal models, and manages session memory for continuity across context resets. As of 2026-02-09, Brain is being expanded from a basic orchestration layer to a full cognitive framework with three sub-systems: Cognition, Memory, and Orchestration.

**Strategic significance:** Brain is the only module customers can't skip — it's the hub. Every other LockN module (Speak, Sense, Look, Logger, Score, Gen, Auth) is a peripheral that plugs into Brain.

## Architecture

### Stack
- **Language:** Python (current), migration to .NET 9 planned for platform consistency
- **Repo:** https://github.com/LockN-Labs/lockn-brain (private, default branch: master)
- **Vector DB:** Qdrant (Apache 2.0, Docker on :6333)
- **Embeddings:** qwen3-embedding (Ollama :11434)
- **Job Queue:** SQLite (existing, proven)
- **Infra:** Docker Compose, local-first

### Solution Structure (Current — Python)
```
lockn-brain/
├── README.md
├── docs/ARCHITECTURE.md          # Detailed design doc (v1.1, 2026-02-05)
├── pyproject.toml
├── src/lockn_brain/
│   ├── __init__.py
│   ├── api.py                    # FastAPI endpoints
│   ├── cli.py                    # CLI interface
│   ├── config.py                 # Pydantic settings (env vars, model endpoints)
│   ├── models.py                 # Pydantic models (ChatRequest, Job, RouteDecision, Citation)
│   ├── queue.py                  # SQLite-backed async job queue
│   ├── retrieval.py              # Qdrant retrieval client (async, multi-hop)
│   ├── router.py                 # System 0: Rule-based intent router (<5ms)
│   └── worker.py                 # System 2 background worker (polls queue → Coder-Next)
└── tests/
    ├── __init__.py
    ├── test_queue.py
    ├── test_retrieval.py
    └── test_router.py
```

### Expanded Architecture (2026-02-09 Vision)
```
LockN Brain
├── Cognition Layer (dual-process reasoning)
│   ├── System 0: Intent Router — rule-based, <5ms, no model call
│   ├── System 1: Fast Path — Qwen3-32B (:11437), 200-500ms, SQLite only
│   ├── System 2: Deep Path — Coder-Next (:11439/:11440), async, SQLite + Vector
│   └── Escalation: Cloud — Opus API, for ambiguity/strategy/200K+ context
│
├── Memory Layer (hybrid storage — NEW)
│   ├── Working Memory: Session context, handoffs (ephemeral)
│   ├── Structured Memory: SQLite — deterministic, fast, bootstrap hot path
│   │   └── Tables: handoffs, project_index, ticket_state, session_metadata
│   └── Semantic Memory: Qdrant Vector DB — probabilistic, growing corpus
│       └── Collections: daily_logs, decisions, conversation_chunks
│
├── Orchestration Layer
│   ├── Agent Spawning + Delegation (model-aware)
│   ├── Model Routing: local vs cloud, cost-aware, context-aware
│   ├── Pipeline Management: coding, review, deploy lifecycles
│   └── Job Queue: SQLite-backed async processing (existing)
│
└── Integration Layer (hub for all modules)
    ├── LockN Speak — TTS output (ACK voice, completion summaries)
    ├── LockN Sense — STT input (voice → text → Brain)
    ├── LockN Look — Vision input (screenshots, visual analysis)
    ├── LockN Logger — Observability (usage tracking, cost attribution)
    ├── LockN Score — Evaluation (quality scoring, confidence)
    ├── LockN Gen — Generative output (images, video)
    └── LockN Auth — Security (API keys, access control)
```

### Dual-Process Flow (Implemented)
```
Request → Embed → Qdrant Search → Router (System 0)
  ├─ FAST → System 1 (Qwen3-32B, <500ms) → Response [+ TTS]
  └─ SLOW → System 1 ACK [+ TTS] → Enqueue → Worker → System 2 (Coder-Next)
            → On completion: Full response [+ TTS summary]
```

### Router Rules (Implemented in router.py)
| Route to System 2 (Slow) | Route to System 1 (Fast) |
|--------------------------|--------------------------|
| Action verbs: refactor, implement, debug, design... | Greetings, confirmations, short Q&A |
| Complex phrases: trade-offs, step-by-step, in-depth | System commands (/status, /help) |
| Long messages (>200 chars) | Short messages (<20 chars) |
| Code blocks or file references | Questions with retrieved context |

### Memory Layer Design (2026-02-09)
| Storage | Purpose | Access Pattern | Latency |
|---------|---------|---------------|---------|
| SQLite | Bootstrap, project index, ticket state, handoffs | Deterministic key lookup | <1ms |
| Qdrant | Daily logs, decisions, conversation history | Semantic similarity search | 50-200ms |

**Critical rule:** System 1 should NEVER need the vector DB. If bootstrap requires semantic search, the structured layer has a gap.

## Key Decisions
| Date | Decision | Rationale | Ticket |
|------|----------|-----------|--------|
| 2026-02-02 | Kahneman dual-process architecture | Natural voice-first interaction without silences | LOC-107 |
| 2026-02-04 | Context-aware routing (Option C) | 95% local ($0), escalate to Opus for complex | MEMORY.md |
| 2026-02-05 | ARCHITECTURE.md v1.1 | Detailed implementation plan with 4 phases | docs/ |
| 2026-02-09 | Brain = Cognitive Orchestration Framework | Every LockN module is a peripheral; Brain is the hub | Today's conversation |
| 2026-02-09 | SQLite + Vector DB hybrid memory | SQLite for deterministic hot path, Qdrant for semantic retrieval | Today's conversation |
| 2026-02-09 | System 1 → SQLite only, System 2 → SQLite + Vector | Fast path never waits for embeddings | Today's conversation |
| 2026-02-09 | PM bootstrap with research crew | Opus + Codex + Kimi for deep bootstrap, Qwen3-32B for ongoing PM | Sean mandate |

## Dependencies
- **Upstream:** Qdrant (vector store), qwen3-embedding (Ollama), llama.cpp endpoints (:11437, :11439, :11440), Claude Opus API
- **Downstream:** Every LockN module depends on Brain for intelligent routing
- **Cross-module:**
  - LockN Loader (LOC-160, Done) → ingests documents into Qdrant for Brain retrieval
  - LockN Speak (LOC-122, Done) → TTS integration for voice-first interaction
  - LockN Sense → STT input to Brain
  - LockN Logger → observability and cost tracking for Brain operations
  - LockN Auth → API key management for Brain endpoints

## Completed Work (6 tickets Done)
| Ticket | Title | Description |
|--------|-------|-------------|
| LOC-120 | Brain Phase 1: Foundation | Qdrant deploy, rule-based router, SQLite job queue, System 1↔2 handoff |
| LOC-121 | Brain Phase 2: Retrieval Integration | Qdrant search, context injection, multi-hop retrieval, citations |
| LOC-122 | Brain Phase 3: TTS Integration | ACK→TTS pipeline, completion summaries, voice-first conversation |
| LOC-123 | Brain Phase 4: Optimization | LLM gate for edge cases, job cancellation, speculative execution, Logger metrics |
| LOC-160 | LockN Loader: RAG Pipeline | Document ingestion, smart chunking, embedding, Qdrant loading, incremental indexing |
| LOC-173 | Semantic Code Search | Indexed all LockN repos into Qdrant |

## Backlog
| Ticket | Title | Priority | Status |
|--------|-------|----------|--------|
| LOC-119 | LockN Brain — Intelligent Orchestration Layer | P2 | Epic (parent) |
| LOC-107 | Dual-Process Thinking Skill (System 1/2 Pattern) | P1 | Backlog — spike for skill design |
| LOC-262 | Realtime Voice Chat MVP (Speak + Brain) | P1 | Backlog — voice loop |
| LOC-266 | OpenClaw x LockN Integration Sprint (Speak/Brain first) | P1 | Backlog — customer-visible skills |
| LOC-246 | LockN Loader — General-Purpose Content Ingestion | P1 | Backlog — expand ingestion |
| LOC-263 | Claws Native Skills Pack for LockN Services | P1 | Backlog — agent skills |
| LOC-374 | [Brain→Score] Real-time Game Intelligence Context API | P1 | Backlog — next sprint candidate |
| LOC-375 | [Brain→Score] Confidence-Gated Referee Decisions + Escalation | P1 | Backlog — next sprint candidate |
| LOC-376 | [Brain→Score] Session Memory Schema for Match Intelligence (SQLite hot path) | P1 | Backlog — next sprint candidate |
| LOC-377 | [Brain→Score] Post-Game Tactical Insights + Voice Coach Summary | P2 | Backlog — next sprint candidate |
| LOC-108 | LockN Loader — Custom RAG Pipeline with Proposition Chunking | P2 | Backlog — advanced chunking |
| LOC-333 | LockN Logger Integration with Project Memory System | P3 | Backlog |

## Remaining Missing Tickets (Post 2026-02-10 Planning Pass)
Created this pass: LOC-374, LOC-375, LOC-376, LOC-377.

Still not explicitly ticketed:
1. **Brain: Memory Layer — Qdrant Semantic Memory Collections** (daily logs, decisions, conversation chunks)
2. **Brain: Memory Layer — Session Bootstrap Service** (deterministic context loading, <15% budget, <100ms)
3. **Brain: Memory Layer — Session Handoff Service** (persist state before context reset)
4. **Brain: Orchestration Layer — Agent Spawning Framework** (model-aware delegation, cost routing)
5. **Brain: Orchestration Layer — Pipeline Manager** (coding/review/deploy lifecycle tracking)
6. **Brain: Integration Layer — Module Hub API** (standardized interface for Speak/Sense/Look/Logger/Score/Gen/Auth)
7. **Brain: .NET Migration Planning** (Python→.NET 9 for platform consistency, or keep Python + interop)

## Implementation State Check (Repo Audit — 2026-02-10)
- **Repo path checked:** `/home/sean/repos/lockn-brain`
- **Git state:** clean tracked files, 1 untracked file (`src/lockn_brain/retrieval.py`)
- **Recent commits:** Phase 4 optimization + container security hardening present
- **Test status:** `40 passed` (`pytest -q`)
- **Implemented modules observed:** `api.py`, `router.py`, `queue.py`, `worker.py`, `gate.py`, `speculative.py`, `metrics.py`, `tts.py`
- **Current gap for Score game intelligence:** no dedicated Brain↔Score intelligence API, no Score-specific memory schema, no referee confidence policy endpoint, no post-game coaching endpoint.

## Next Sprint Focus (Brain supporting Score)
1. Real-time context API for rally/serve/momentum
2. Confidence-gated referee decisions with escalation
3. SQLite hot-path session memory for active matches
4. Post-game tactical insights + voice coach summaries

## Open Questions
1. **.NET or Python?** Current codebase is Python. Rest of LockN is .NET 9. Migrate or interop?
2. **Qdrant deployment model?** Currently Docker. Managed cloud for production? Or embedded (qdrant-client local mode)?
3. **Session bootstrap token budget?** Current target: 15% of model context / 30K tokens max. Validate with usage data.
4. **Confidence threshold for escalation?** System 1 → System 2 cutoff. Needs calibration.
5. **Memory retention policy?** How long to keep semantic memory? Tiered (hot/warm/cold)?
6. **Brain as standalone service vs embedded library?** API server (current) vs NuGet package for other modules?
7. **Multi-tenant support?** If Brain is the product, does each customer get isolated memory?

## Latency Targets (from ARCHITECTURE.md)
| Component | Target | Notes |
|-----------|--------|-------|
| Embedding | <20ms | qwen3-embedding local |
| Qdrant search | <50ms | Hybrid search |
| Router (rules) | <5ms | No model call |
| Router (LLM gate) | <200ms | 1-token classification |
| **System 1 total** | **200-500ms** | Retrieval + routing + response |
| System 2 ACK | <500ms | Before async handoff |
| System 2 completion | 30s-5min | Task-dependent |
| **Bootstrap (SQLite)** | **<100ms** | Deterministic, no embeddings |

## Model Allocation
| Port | Model | Role | Context | Speed |
|------|-------|------|---------|-------|
| 6333 | Qdrant | Vector store | N/A | <50ms |
| 11434 | qwen3-embedding | Embeddings | N/A | ~10ms |
| 11437 | Qwen3-32B Q5_K_M | System 1 (Fast) | 65K | ~200 tok/s |
| 11439 | Qwen3-Coder-Next Q5 | System 2 (GPU) | 1M | ~500 tok/s |
| 11440 | Qwen3-Coder-Next Q3 | System 2 (CPU) | 2M | ~15-30 tok/s |
| API | Claude Opus | Escalation | 200K | N/A |

## LockN Ecosystem Map
| Component | Role | Metaphor | Integration Point |
|-----------|------|----------|------------------|
| **LockN Brain** | Orchestration + cognition + memory | Brain (thinks) | Central hub |
| **LockN Loader** | Document ingestion + chunking | Mouth (ingests) | Feeds Qdrant |
| **LockN Speak** | Voice output (TTS) | Mouth (speaks) | ACK + completion TTS |
| **LockN Sense** | Audio perception (STT + VAD) | Ears (hears) | Voice input |
| **LockN Look** | Vision (image analysis) | Eyes (sees) | Visual input |
| **LockN Listen** | STT microservice | Ears (transcribes) | Speech→text |
| **LockN Logger** | Observability + cost tracking | Nervous system | Metrics |
| **LockN Score** | Evaluation + scoring | Judgment | Quality gates |
| **LockN Gen** | Generative media | Hands (creates) | Creative output |
| **LockN Auth** | Security + access control | Immune system | Trust boundaries |

## Sources
- GitHub: LockN-Labs/lockn-brain (full codebase — router.py, retrieval.py, worker.py, queue.py, models.py, config.py)
- GitHub: docs/ARCHITECTURE.md (v1.1, 2026-02-05)
- Linear: LOC-107, LOC-119-123, LOC-160, LOC-173, LOC-246, LOC-262, LOC-263, LOC-266, LOC-333
- Workspace: MEMORY.md (Brain dual-process architecture, model infrastructure)
- Workspace: memory/daily/2026-02-09.md (session memory architecture decision, pm-bootstrap)
- Workspace: skills/dual-process/SKILL.md (existing dual-process skill)
- Notion: Technical Architecture summaries page
- Conversation: Sean + Claws 2026-02-09 (Brain = cognitive framework, SQLite + Vector hybrid, System 1/2 storage paths)
