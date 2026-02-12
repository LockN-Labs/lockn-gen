# LockN Brain — Decision Log

## DEC-001: Kahneman Dual-Process Architecture (2026-02-02)
**Decision:** Adopt System 0/1/2 pattern inspired by "Thinking Fast and Slow"
**Rationale:** Enables natural voice-first interaction without awkward silences. Fast path handles conversational flow while slow path handles deep work async.
**Alternatives considered:** Single-model routing, priority queue, simple if/else
**Outcome:** Implemented in router.py, worker.py — working well

## DEC-002: Context-Aware Routing — Option C (2026-02-04)
**Decision:** Qwen3-Coder-Next as primary model, escalate to Opus for complex decisions
**Rationale:** 95% of work runs locally at $0. Only strategic planning, ambiguity, and user communication go to cloud.
**Alternatives considered:** A) Cloud-first, B) Local-only, C) Context-aware routing
**Outcome:** Adopted — local-first working as designed

## DEC-003: Qdrant as Vector DB (2026-02-02)
**Decision:** Qdrant for vector storage and hybrid search
**Rationale:** Apache 2.0, production-ready, Docker deployment, gRPC + REST, hybrid vector+BM25 search
**Alternatives considered:** LanceDB (petabyte-scale), Milvus, Chroma
**Outcome:** Running on :6333, used by retrieval.py and Loader

## DEC-004: SQLite Job Queue (2026-02-02)
**Decision:** SQLite for async job queue (System 2 work)
**Rationale:** Simple, reliable, zero-config, proven. No need for Redis/RabbitMQ at current scale.
**Outcome:** Implemented in queue.py — handles pending/running/completed/failed lifecycle

## DEC-005: Brain = Cognitive Orchestration Framework (2026-02-09)
**Decision:** Expand Brain from "orchestration module" to full cognitive framework with Cognition, Memory, and Orchestration layers
**Rationale:** Everything we're building (dual-process, session memory, bootstrap, agent spawning) IS Brain. It's the only module customers can't skip — it's the hub. Productizing our own infrastructure.
**Alternatives considered:** Keep Brain as simple router, build memory/orchestration as separate modules
**Outcome:** Architecture defined, brief updated, tickets to be created

## DEC-006: Hybrid Storage — SQLite + Vector DB (2026-02-09)
**Decision:** SQLite for structured/deterministic data, Qdrant for semantic/probabilistic data
**Rationale:** Bootstrap needs deterministic lookups (<1ms) — can't depend on embeddings. Semantic search needed for "find context about X" queries. Different jobs, different stores.
**Critical rule:** System 1 should NEVER need the vector DB.
**Alternatives considered:** Vector-only, SQLite-only
**Outcome:** Architecture defined, implementation pending

## DEC-007: PM Bootstrap with Research Crew (2026-02-09)
**Decision:** Use Opus + Codex + Kimi for one-time deep bootstraps, Qwen3-32B for ongoing PM
**Rationale:** Best possible start (multi-model ensemble) → efficient maintenance (free local model). Sean mandate.
**Outcome:** Strategy documented in AGENTS.md, first run completed for Brain

## PENDING: .NET vs Python (2026-02-09)
**Status:** Open question. Current codebase is Python. Rest of LockN is .NET 9. Need to decide: migrate, interop, or keep Python.
**Factors:** Platform consistency, team expertise, performance characteristics, existing code investment
