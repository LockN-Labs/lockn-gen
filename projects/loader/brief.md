# LockN Loader — Project Brief

## Status
- **Linear Ticket:** LOC-246
- **State:** Backlog
- **Priority:** High (P1)
- **Phase:** mvp foundation exists → expansion
- **Last Verified:** 2026-02-09

## Overview
LockN Loader is the content ingestion layer for the LockN ecosystem. It standardizes intake, normalization, chunking, and indexing of source material for downstream retrieval and reasoning systems.

Context from related work:
- **LOC-247 (fork):** Done
- **LOC-160 (RAG pipeline):** Done

This project now focuses on hardening and scaling ingestion into a reusable platform service.

## Architecture
### Core Stack
- **Lineage:** Fork/extension of lockn-code-search patterns
- **Domain:** Multi-source ingestion + transformation + indexing
- **Storage targets:** Structured metadata store + vector index targets (where applicable)
- **Runtime:** Batch + incremental ingestion workflows

### Planned Components
- Source connectors (docs/repos/files/etc.)
- Parsing + normalization pipeline
- Chunking/embedding handoff pipeline
- Incremental re-indexing and dedupe controls
- Operational dashboarding and job observability

## Priorities
1. Define source connector priorities and ingestion SLAs.
2. Standardize pipeline contracts with Brain/retrieval consumers.
3. Improve incremental indexing and replay safety.
4. Add robust observability and failure recovery paths.

## Dependencies
- **Cross-module:**
  - LockN Brain (primary consumer of indexed knowledge)
  - Vector DB + embedding endpoints
  - LockN Logger (pipeline telemetry)
- **Operational:** Scheduler/queue infrastructure, storage lifecycle policy
