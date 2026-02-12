# LockN Score — Project Brief

## Status
- Phase: mvp
- Confidence: 0.65
- Last Verified: 2026-02-09

## Overview
LockN Score is now past pure discovery and has a proven MVP foundation for automated sports scoring. The original MVP and generic sport perception pipeline are complete, confirming that the core architecture can ingest gameplay signals and produce scoring outputs. The next phase is execution-heavy: integrating camera perception through to a live dashboard with production reliability.

## Current State (What Works)
### Completed and validated
- **LOC-124 — Original MVP:** Done
  - Baseline automated scoring workflow established
  - Core system components integrated enough to validate end-to-end concept
- **LOC-137 — Generic sport perception pipeline:** Done
  - Reusable perception layer exists for sport-specific extensions
  - Foundation for expanding beyond initial hardcoded logic is in place

### Practical capability today
- LockN Score can run an MVP-level scoring flow using established perception primitives.
- Architectural direction (camera/perception-driven scoring) is validated.
- The platform is ready for next-gen productization rather than greenfield R&D.

## Next Phase Priorities
### Critical path (highest priority)
1. **LOC-232 — E2E Camera → Dashboard integration**
   - This is the **primary critical path** for next-phase execution.
   - Goal: robust real-time pipeline from camera ingest to operator/customer-visible score dashboard.
   - Without this, other next-gen work has limited product impact.

### Enabling next-gen scoring quality
2. **LOC-228 — Fuse Camera + Audio**
   - Improves event confidence and edge-case handling.
   - Necessary for resilient real-world scoring under noisy conditions.

3. **LOC-200 — Ping Pong Scoring v2**
   - First concrete sport-specific quality upgrade on top of the generic pipeline.

### Product and GTM readiness
4. **LOC-184 — UI/UX Overhaul**
   - Required to make dashboard outputs operator-friendly and venue-ready.

5. **LOC-226 — Sports Market MVP**
   - Connects technical scoring capability to a sellable market-facing product.

6. **LOC-240 — YOLOv8 Ball Tracking Feasibility**
   - High-leverage validation task that can materially affect tracking accuracy, scope, and timeline.

## Revenue Path
### Target model
- **$49/month per venue** (baseline target)

### Path to revenue
1. Ship reliable **Camera → Dashboard** E2E flow (LOC-232) as the minimum sellable core.
2. Raise event accuracy via **camera+audio fusion** and validated ball tracking strategy.
3. Deliver polished venue UX so score output is trusted and easy to operate.
4. Launch sports market MVP and onboard first paying venues at the $49/mo price point.

## Key Blockers
1. **YOLOv8 ball tracking feasibility (LOC-240)**
   - Unknowns around detection quality, latency, and deployment constraints.
   - Directly impacts confidence in next-gen scoring performance.

2. **Fusion engine maturity (camera + audio, LOC-228)**
   - Sensor fusion complexity is a core technical risk.
   - Required for robust scoring in real-world conditions and false-event reduction.

## Backlog Snapshot (Next-Gen)
All currently in **Backlog**:
- LOC-200 — Ping Pong Scoring v2
- LOC-232 — E2E Camera → Dashboard
- LOC-228 — Fuse Camera + Audio
- LOC-226 — Sports Market MVP
- LOC-184 — UI/UX Overhaul
- LOC-240 — YOLOv8 Ball Tracking Feasibility

## Assessment
LockN Score has graduated from discovery into an MVP-proven state with meaningful foundational wins (LOC-124, LOC-137). However, key next-phase delivery items remain backlogged, so execution risk is still material. Confidence is set to **0.65** to reflect solid base validation plus pending critical-path integration work.

## Sources
- `skills/pm-bootstrap/SKILL.md`
- Project status update provided in session (LOC-124, LOC-137 done; LOC-200/232/228/226/184/240 backlog)
- `projects/_index.md` (existing project index entry)
