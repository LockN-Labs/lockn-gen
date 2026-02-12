# Linear Business Plan - Deep Capability Map
## For High-Throughput AI Swarms & Slack-First Triage Workflows

**Research Date:** 2026-02-08  
**Focus:** Slack integrations, triage/automation patterns, agent workflow scalability

---

## 1. Feature Matrix: Basic vs Business (AI Swarm Relevance)

| Feature | Basic | Business | AI Swarm Relevance |
|---------|-------|----------|-------------------|
| **Pricing** | $8/mo ($76.80/yr) | $12/mo ($115.20/yr) | +$38.40/yr per seat |
| **Teams** | 2 max | Unlimited | ✅ Critical: Separate teams per agent domain |
| **Issues** | 250 max | Unlimited | ✅ Required for high-volume agent output |
| **File uploads** | 10MB | Unlimited | ✅ Agents attach logs, screenshots, docs |
| **API Rate Limit** | 5,000 req/hr | 5,000 req/hr (same) | ⚠️ Plan for 5K/hr ceiling per user/API key |
| **Triage** | ✅ | ✅ | Core intake mechanism |
| **Triage Rules** | ❌ | ✅ | **🔥 Critical: Auto-route by label/keywords** |
| **Triage Intelligence** | ❌ | ✅ | **🔥 AI-suggested assignee, labels, duplicates** |
| **Linear Agent (@linear)** | ❌ | ✅ | **🔥 Natural language issue creation in Slack** |
| **Linear Asks** | ❌ | ✅ | **🔥 Non-Linear users → issues via Slack/email** |
| **Asks (Auto-create :ticket:)** | ❌ | ✅ | Bot-to-issue automation |
| **Insights/Dashboards** | ❌ | ✅ | **🔥 Cycle time, SLA, triage time analytics** |
| **Data Warehouse Sync** | ❌ | ✅ | Export to BigQuery/Snowflake for custom ML |
| **Private Teams** | ❌ | ✅ | Isolate sensitive agent operations |
| **Guest Accounts** | ❌ | ✅ | External stakeholders in specific projects |
| **Issue SLAs** | ✅ | ✅ | Track breach rates |
| **Sub-teams** | ❌ | ✅ | Organize agent squads |
| **MCP Access** | ✅ | ✅ | Model Context Protocol for tool use |
| **Multi Slack workspaces** | ❌ | Enterprise only | Needed for Grid/Enterprise Slack |
| **Asks on new message** | ❌ | Enterprise only | Full auto-conversion channel → issue |

### 🔥 Must-Have for AI Swarms (Business Plan)
1. **Triage Rules** - Auto-assign, auto-label, auto-route to teams based on issue content
2. **Triage Intelligence** - LLM-powered duplicate detection and property suggestions
3. **Linear Agent** - Natural language issue creation from Slack (`@linear file a bug`)
4. **Linear Asks** - Let non-Linear users (bots, guests, other teams) create issues
5. **Insights** - Track cycle time, triage time, SLA compliance across all agent work

---

## 2. Slack Intake/Triage Automation Patterns

### Pattern A: 🎫 Emoji-Driven Triage (Basic Automation)
**Setup:** Asks with `:ticket:` reaction auto-creation
```
Slack Message + 🎫 emoji → Auto-creates Linear issue in Triage
↓
Triage Rules evaluate: keywords, sender, channel → Auto-assign/reroute
↓
Triage Intelligence suggests: labels, assignee, related issues
↓
Agent picks up from In Progress
```
**Best for:** Community support, internal bug reports, ad-hoc requests

### Pattern B: Channel-Level Auto-Create (Enterprise Feature)
**Setup:** `#ai-bugs`, `#agent-failures` → Every message becomes an issue
```
Any message in #agent-failures → Auto-creates Linear issue
↓
Template pre-applies: Team=AI-Infra, Label=agent-failure, Priority=p1
↓
Triage responsibility rotates to on-call engineer
```
**Best for:** High-signal, dedicated intake channels

### Pattern C: @linear Agent Pattern (Business+)
**Setup:** Natural language in any channel
```
"@linear create p1 bug about memory leak in embedding service, assign to infra team"
↓
Linear Agent parses intent → Creates structured issue
↓
Synced thread keeps Slack + Linear comments in sync
```
**Best for:** PMs, leads, anyone who hates forms

### Pattern D: Asks Template Routing (Business+)
**Setup:** Multiple templates per channel with different destinations
```
#engineering-requests
  ├── "Bug Report" template → Team: Engineering, Labels: bug
  ├── "Feature Request" template → Team: Product, Labels: feature
  └── "Agent Incident" template → Team: AI-Ops, Labels: incident
```
**Best for:** Organized intake with structured fields

### Pattern E: Email-to-Issue Pipeline
**Setup:** `agents@company.com` forwards to Linear Asks email
```
External alert email → Creates Linear issue
↓
Synced email thread: replies go to Linear comments
↓
Linear replies sent back to email thread
```
**Best for:** External monitoring, vendor alerts, customer emails

---

## 3. Suggested Channel-to-Workflow Mapping

### For AI Swarm Operations:

| Slack Channel | Linear Team | Triage Rule | Template | Auto-Create |
|--------------|-------------|-------------|----------|-------------|
| `#ai-failures` | AI-Infra | Label: agent-failure, Priority: High | Agent Incident | 🎫 emoji |
| `#model-issues` | ML-Platform | Assign: ML-oncall | Model Bug | 🎫 emoji |
| `#agent-requests` | AI-Product | Label: feature-request | Feature Request | Mention @linear |
| `#infra-alerts` | Platform | Priority: P1, Assign: Infra-oncall | Alert | Email intake |
| `#triage` | Triage (all) | Triage Intelligence enabled | Generic | Manual |
| `#customer-escalations` | CX | Label: escalation, Link customer | Escalation | 🎫 emoji |

### Recommended Triage Rules (Business Plan):

```
Rule 1: Agent Failure Auto-Route
IF: Title contains "agent" OR "swarm" OR "pipeline"
AND: Label = "failure" OR "error"
THEN: Move to AI-Infra team, Set Priority = High, Assign = Triage rotation

Rule 2: Performance Issues
IF: Title contains "slow" OR "timeout" OR "memory"
THEN: Add Label = "performance", Move to Platform team

Rule 3: External Customer Reports
IF: Created via Asks AND Customer field is set
THEN: Add Label = "customer-request", Set Priority = Medium
```

---

## 4. Metrics to Track

### Available in Linear Insights (Business Plan Required):

| Metric | Definition | Target for AI Swarms |
|--------|-----------|---------------------|
| **Triage Time** | Issue created → moved to In Progress | < 4 hours (P1), < 24h (P2) |
| **Cycle Time** | In Progress → Completed | Track by team, trend down |
| **Lead Time** | Created → Completed | Overall velocity indicator |
| **Issue Age** | Time since creation (for open issues) | Alert if > 7 days |
| **SLA Status** | Breach rate by priority | < 5% breach rate |
| **Reopen Rate** | Completed → Reopened | < 10% (signals quality issues) |
| **Blocked Time** | Time in "Blocked" status | Minimize, track blockers |

### Custom Metrics (via API + Dashboard):

| Metric | Source | Purpose |
|--------|--------|---------|
| **Agent Creation Rate** | Issues with "agent" label / day | Volume tracking |
| **Auto-Triage Accuracy** | Triage rule matches / total triaged | Rule effectiveness |
| **Duplicate Detection Rate** | Triage Intelligence merges / total | AI efficiency |
| **Time to First Response** | First comment time - creation time | Responsiveness |
| **In-Flight Workload** | Open issues per agent/team | Capacity planning |

### Recommended Dashboard Views:

1. **Executive Summary:** Cycle time trend, SLA breach rate, team velocity
2. **Agent Operations:** Agent-failure issues open/closed, triage queue depth
3. **Quality Metrics:** Reopen rate, bug escape rate, customer escalations
4. **Capacity Planning:** Issues per assignee, blocked issues, aging issues

---

## 5. Fast Implementation Checklist (This Week)

### Day 1-2: Foundation
- [ ] Upgrade to Business plan (if not already)
- [ ] Connect Slack workspace: Settings → Integrations → Slack
- [ ] Enable Triage for AI teams: Team Settings → Triage → Enable
- [ ] Set Triage Responsibility: Rotate weekly among team members
- [ ] Invite @Linear and @Linear Asks to relevant Slack channels

### Day 3-4: Automation Setup
- [ ] Create Triage Rules (Business feature):
  - Auto-route by keyword patterns
  - Auto-label by source channel
  - Auto-assign P1 issues to on-call
- [ ] Configure Linear Asks:
  - Add 🎫 emoji reaction auto-create
  - Create 2-3 issue templates per team
  - Connect templates to Slack channels
- [ ] Set up Linear Agent guidance:
  - Document channel-to-team mappings
  - Define default labels/priorities

### Day 5: Metrics & Monitoring
- [ ] Enable Insights for key views:
  - Create custom view for "All Agent Issues"
  - Add cycle time, triage time widgets
  - Set up SLA tracking by priority
- [ ] Create team notifications:
  - Push status changes to #linear-updates
  - Personal notifications for assignments
- [ ] Document the workflow in team wiki

### API Considerations for Swarms:
- [ ] Linear API rate limit: **5,000 requests/hour per user/API key**
- [ ] Complexity limit: 10,000 points per query, 250,000 points/hour
- [ ] Webhook support: Use instead of polling (strongly recommended)
- [ ] GraphQL endpoint: `https://api.linear.app/graphql`

---

## Key Integration Patterns for AI Swarm Workflows

### Webhook → Slack Notification Pipeline
```
Linear Webhook (issue created) → Filter (agent-related) → Slack #ai-ops
Linear Webhook (status change) → Update synced Slack thread
```

### Automated Triage with External Schedules
```
PagerDuty/OpsGenie on-call schedule → Linear Triage Responsibility API
→ Auto-assigns new issues to current on-call engineer
```

### Round-Robin Agent Assignment
```
Triage Rules + Webhook → External function (custom) → Update assignee
```

---

## Resources

- **Linear Triage Docs:** https://linear.app/docs/triage
- **Linear Slack Integration:** https://linear.app/docs/slack
- **Linear Asks Docs:** https://linear.app/docs/linear-asks
- **Linear Insights:** https://linear.app/docs/insights
- **API Rate Limiting:** https://linear.app/developers/rate-limiting
- **GraphQL Explorer:** https://studio.apollographql.com/public/Linear-API

---

*Generated for Linear Business Plan evaluation - AI swarm workflow optimization*
