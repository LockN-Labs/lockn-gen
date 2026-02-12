# LockN Sense — Project Brief

## Status
- **Phase:** mvp
- **Confidence:** 0.70
- **Last Verified:** 2026-02-09

## Current State
LockN Sense MVP (**LOC-155**) is complete. The core audio perception pipeline is working end-to-end:
- **Silero VAD** (**LOC-156**) — Done
- **faster-whisper STT** (**LOC-157**) — Done
- **PANNs audio classification** (**LOC-158**) — Done

This means Sense can detect speech/activity, transcribe audio, and classify audio events in a single pipeline.

## Next Phase
Primary next milestone is **N-stream multi-device ingestion** at the Sense platform level:
- **LOC-382** — Multi-Stream Ingestion Layer (Urgent) — N concurrent audio+video streams with device registry, sport-agnostic
- **LOC-159** — Multi-feed sync (Backlog) — subsumed by LOC-382

**Strategic direction (Sean, 2026-02-09):** Sense is the platform layer. Score, and all future verticals (tennis, padel, non-sport), consume Sense event streams. Multi-stream is a Sense capability, not Score-specific. Ping pong first, extend to other paddle sports with dedicated fine-tunes.

## Integration Points
- **LockN Score** depends on **LockN Sense** for audio classification outputs.
- Sense provides classification signals that Score can use for evaluation/scoring workflows.

## Backlog
- **LOC-159** — Multi-feed sync
- **LOC-136** — Spike research

## Confidence Rationale
Confidence is set to **0.70** because the MVP pipeline is complete and functional, but major integration and scaling work (especially multi-feed synchronization and downstream Score integration hardening) is still pending.
