# Blocker Audit Process (Established 2026-02-07)

## When to Run
- Every heartbeat (10-minute cycle)
- After completing major work items
- When encountering new blockers

## Process
1. Audit all work streams for items waiting on Sean
2. Rate each item on predicted automatability (0.00-10.00)
3. Bucket into three categories:
   - **Automatable** (≥7.00) — Can be automated with existing tools/skills
   - **Potentially Automatable** (≥4.00) — May be automatable with new tooling or access
   - **Not Automatable Yet** (<4.00) — Requires human decision, external access, or policy change

4. Post summary to #C0ACDPDQ9L5 (system-heartbeat)
5. Escalate "Not Automatable Yet" items to #C0ACLQVLFNG (escalations channel)

## Rating Criteria
- 9.00-10.00: Already have tools, just need to do it
- 7.00-8.99: Need minor tooling or one-time setup
- 4.00-6.99: Need new skill, API access, or permissions
- 1.00-3.99: Requires human judgment, financial decision, or external party
- 0.00-0.99: Fundamentally requires Sean (legal, identity, relationships)

## Documentation
Track all blockers in daily memory file with resolution status.
