# LockN Swap/Swing — Project Brief

## Status
- **Linear Ticket:** LOC-323
- **State:** Todo
- **Priority:** Urgent (P1)
- **Phase:** discovery → mvp
- **Last Verified:** 2026-02-09

## Overview
LockN Swap/Swing is the XRPL trading platform initiative for the LockN ecosystem. It is intended to provide swap and swing-style trading workflows with production-grade reliability, clear execution paths, and secure integration with LockN services.

Primary goals:
- Ship a practical trading MVP on XRPL.
- Establish a reliable execution path for swap/swing actions.
- Integrate with shared LockN platform services (auth, logging, observability).

## Architecture
### Core Stack (planned)
- **Repository:** https://github.com/LockN-AI/lockn-swap
- **Domain:** XRPL trading execution + strategy orchestration
- **Service model:** API-first service with modular trading components
- **Infra:** Containerized deployment (Docker), environment-based config

### Planned Components
- Order/swap orchestration service
- XRPL connectivity/execution adapter
- Risk/guardrail layer (limits, validation, fail-safe rules)
- Observability hooks (metrics, traces, execution logs)

## Priorities
1. Define MVP scope and acceptance criteria for LOC-323.
2. Establish secure XRPL transaction flow and failure handling.
3. Implement baseline observability and audit logging from day one.
4. Align execution/state model with downstream reporting/analytics needs.

## Dependencies
- **Upstream:** XRPL network/tooling; wallet/key management strategy
- **Cross-module:**
  - LockN Auth (identity + secrets/access)
  - LockN Logger (execution telemetry)
  - LockN Score (quality/performance evaluation, optional)
- **Delivery dependencies:** CI/CD baseline, testnet validation environment
