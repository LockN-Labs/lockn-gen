# LockN Email — Project Brief

## Status
- **Linear Ticket:** LOC-223
- **State:** Backlog
- **Priority:** Urgent (P1)
- **Phase:** discovery
- **Last Verified:** 2026-02-09

## Overview
LockN Email is the transactional email service for LockN, built around Postmark for reliable delivery, templating, and event visibility. The service will centralize outbound transactional messaging for system notifications, account/security events, and workflow updates.

## Architecture
### Core Stack (planned)
- **Provider:** Postmark
- **Service model:** Internal email API + template/rendering layer
- **Eventing:** Delivery, bounce, open/click, and failure webhooks
- **Infra:** Containerized service with environment-based secrets/config

### Planned Components
- Template registry and versioning
- Send pipeline (idempotent requests + retries)
- Webhook ingestion for delivery lifecycle events
- Policy controls (rate limits, suppression/bounce handling)
- Audit/event log integration

## Priorities
1. Define transactional email use-cases and template catalog.
2. Implement secure Postmark integration with key rotation support.
3. Build reliable send + retry + idempotency behavior.
4. Capture delivery telemetry and integrate with platform logging.

## Dependencies
- **Upstream:** Postmark API + webhook endpoints
- **Cross-module:**
  - LockN Auth (account/security notification triggers)
  - LockN Logger (send/delivery observability)
  - Product modules needing transactional notifications
- **Compliance:** Domain verification, SPF/DKIM/DMARC alignment
