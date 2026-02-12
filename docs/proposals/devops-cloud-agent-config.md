# DevSecOps Agent Configuration Proposal

**Agent:** `devops-cloud`  
**Date:** 2026-02-10  
**Status:** Proposal

## Current State
The `devops-cloud` agent exists but is unconfigured. After the auth cascade incident, it's clear this agent needs to own auth/infra validation.

## Proposed Ownership

### 1. Auth Flow Validation
- **Owns:** `auth-flow-validation-6h` cron
- **Runs:** Post-deploy auth smoke tests (LOC-426)
- **Monitors:** Auth error rates, silent auth failures, token claim anomalies
- **Escalates:** To #process-improvements on failure, pages Sean on critical

### 2. Security Gate Lifecycle
- **Owns:** `temp-gates.json` maintenance
- **Runs:** Expiration checks on every infra-check cycle
- **Actions:** Alerts 48h before gate expiration, escalates expired gates
- **Reports:** Weekly temp-gate summary

### 3. Config Drift Detection
- **Owns:** `drift-check.sh` execution
- **Monitors:** Caddy config, Auth0 callback URLs, DNS records
- **Compares:** Running state vs repo/expected state
- **Escalates:** DRIFT or ALERT status to appropriate channel

### 4. Incident Response Automation
- **Detects:** Auth flow failures via smoke tests
- **First response:** Run drift detection, gather diagnostic data
- **Provides:** Structured incident report with likely root cause
- **Tracks:** MTTR and incident frequency

## Recommended Agent Config

```yaml
name: devops-cloud
description: DevSecOps automation — auth validation, config drift, security gate lifecycle
model: claude-sonnet-4-20250514  # Fast, reliable for automated checks
skills:
  - config-drift
  - auth-guard
  - devops-infra-restart
crons:
  - auth-flow-validation-6h  # Already created
  - devops-infra-check-15min  # Already updated with Caddy audit
environment:
  AUTH0_DOMAIN: "${AUTH0_DOMAIN}"
  AUTH0_CLIENT_ID: "${AUTH0_CLIENT_ID}"
  LOCKN_APP_URL: "https://app.lockn.dev"
channels:
  alerts: "#process-improvements"
  incidents: "#incidents"
```

## Implementation Steps
1. Configure the agent with the above settings
2. Grant access to Auth0 Management API (read-only)
3. Grant access to Caddy admin API
4. Set up secret management for API tokens
5. Run initial drift check to establish baseline
6. Monitor for 1 week, tune alert thresholds
