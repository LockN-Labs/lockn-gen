# Infrastructure Modernization v2 — Project Brief

## Status
- **Linear Project ID:** 7c2a2f56
- **State:** Active planning
- **Priority:** High (platform-critical)
- **Phase:** architecture
- **Last Verified:** 2026-02-09

## Overview
Infrastructure Modernization v2 is the next-generation platform infrastructure initiative for LockN, centered on a 4-stack Docker architecture. The goal is to improve deployability, isolation, observability, and operational consistency across all LockN services.

## Architecture
### Target Topology
- **Deployment model:** 4-stack Docker architecture
- **Design intent:** Clear separation of concerns across service groupings
- **Operations:** Standardized environment configuration, health checks, and rollout patterns

### Planned Stack Domains
1. Core platform services
2. Data/retrieval infrastructure
3. Interface/API edge services
4. Observability/ops tooling

### Platform Requirements
- Deterministic local/dev/test parity
- Secure secret management and network boundaries
- Unified logging/metrics/tracing pipeline
- Repeatable CI/CD and promotion flow

## Priorities
1. Define exact 4-stack boundaries and ownership model.
2. Produce baseline compose/deploy manifests for each stack.
3. Standardize health/readiness checks and dependency startup sequencing.
4. Implement centralized observability and incident triage workflows.

## Dependencies
- **Cross-project:** All LockN module services and shared platform components
- **Tooling:** Docker/Compose runtime, CI/CD pipeline integrations
- **Operational:** Environment strategy (dev/test/prod), secret management, runbook ownership
