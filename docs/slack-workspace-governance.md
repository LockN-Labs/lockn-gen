# Slack Workspace Governance (LockN AI)

Updated: 2026-02-08
Owner: Sean + Claws

## 1) Operating Mode
- Slack remains the primary communication surface across LockN AI workspace.
- New channels are allowed when they add clear value.
- Consolidation rule is mandatory: no duplicate-purpose channels.

## 2) Channel Creation Rules
Create a new channel only if one of these is true:
- Distinct audience (e.g., customer-facing vs internal build)
- Distinct lifecycle stage (e.g., intake vs delivery)
- Distinct confidentiality boundary

Before creating, check for existing channels with same purpose.

## 3) Naming Taxonomy
Use consistent prefixes:
- `lockn-ops-*` -> operations, monitoring, incident flow
- `lockn-build-*` -> implementation, engineering execution
- `lockn-customer-*` -> customer delivery and support
- `lockn-research-*` -> exploration and experiments

## 4) De-duplication Policy
If overlap is found:
1. pick canonical channel
2. post migration notice in duplicate channel
3. move active threads to canonical channel
4. archive duplicate channel

## 5) Health Monitoring
Minimum recurring checks:
- `openclaw status`
- `openclaw security audit`
- Slack channel connection/tokens state

Alert only on:
- channel disconnect/token issues
- failed message delivery/read
- security policy drift

## 6) Multi-Surface Expansion (Phased)
Priority order:
1. Slack (command center)
2. Signal or Telegram for mobile failover alerts
3. Custom surface/webhooks for structured approvals/status views

## 7) Implemented Automation
- Cron reminder added (every 2h): Slack+Gateway comms health check
  - Job ID: `faa1fa44-9c70-4cb0-a112-ce482c2a303b`
