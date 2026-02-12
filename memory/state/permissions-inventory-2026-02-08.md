# Permissions Inventory: 2026-02-08 (Weekly Check)

## Current Access Status

| System | Access Level | Status | Impact |
|--------|--------------|--------|--------|
| **GitHub (LockN-AI)** | Full repo access | ✅ Active | Code, PRs, issues, CI |
| **GitHub Apps** | 5 apps created | ✅ Active | Coder, QA, Architect, DevOps, Orchestrator |
| **Linear** | API key (lockn-ai) | ✅ Active | Issue management, comments |
| **Linear Agents** | 5 accounts invited | ✅ Active | Per-agent attribution |
| **Gmail (OAuth)** | Desktop client created | ❌ Pending Auth | Auto-verify accounts, notifications |
| **Slack** | Bot + App tokens | ✅ Active | Messaging, reactions |
| **Cloudflare** | API token | ✅ Active | DNS management |
| **Postmark** | Server token | ✅ Active | Transactional email |
| **Auth0** | M2M tokens working | ✅ Active | User management, roles |

## High Priority Gaps (Need Action)

### 1. Gmail OAuth Authorization ❌
- **Impact:** Cannot read inbox for account verification, notifications
- **Status:** Desktop client created but not authorized
- **Automatability:** 2.00/10.00 (Requires Sean's OAuth consent)
- **Action Required:** Escalate to Sean for OAuth flow completion

### 2. Auth0 Management API Key ❌
- **Impact:** Limited user management automation
- **Status:** M2M tokens work for basic operations
- **Automatability:** 6.00/10.00 (Could research self-service creation)
- **Action Required:** Research Auth0 mgmt API key generation

## Medium Priority (Next Sprint)

### 3. Google Calendar API ❌
- **Impact:** No schedule awareness, meeting prep
- **Automatability:** 3.00/10.00 (Similar OAuth consent needed)

### 4. SSH Access to LockN Servers ❌
- **Impact:** No remote deployments, server management
- **Automatability:** 8.00/10.00 (Can generate SSH keys, need server access)

## Recommendations

**Immediate (this week):**
1. Escalate Gmail OAuth to Sean - critical for notification automation
2. Research Auth0 management API key creation process

**Next sprint:**
1. Generate SSH keypair for server access
2. Calendar API integration planning

**Future:**
1. Cloud provider IAM (AWS/GCP/Azure)
2. Social media APIs (Twitter/LinkedIn)
3. Payment/billing APIs (Stripe read-only)

## Blocker Items for Sean

| Item | Automatability Score | Action |
|------|---------------------|--------|
| Gmail OAuth consent | 2.00/10.00 | **Escalate to #agent-blockers** |
| Calendar API OAuth | 3.00/10.00 | **Escalate to #agent-blockers** |

## Progress Since Last Check (2026-02-07)
- No new permissions gained
- Auth0 M2M tokens confirmed working
- Identified Gmail OAuth as highest impact blocker