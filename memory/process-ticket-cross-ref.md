# Process: Ticket Cross-Reference on Completion

**Created:** 2026-02-11
**Trigger:** Sean identified systemic gap — tickets marked Done while sibling tickets covering overlapping work stayed in Backlog with stale descriptions. Led to false "not started" status when work was actually ~70% done.

## Root Cause
Agents close their assigned ticket without checking if their implementation also delivered work scoped under sibling/related tickets. No post-completion cross-reference step exists.

## Rule: Post-Completion Sibling Scan
When closing ANY Linear ticket:
1. Check the parent issue (if exists) for sibling subtasks
2. Check `relatedTo` / `blockedBy` / `blocks` issues
3. For each sibling/related ticket still open:
   - Compare its acceptance criteria against what was just implemented
   - If partial overlap: comment on the sibling with what was delivered + update description with "Already Built" section
   - If fully delivered: move sibling to Done with comment explaining which ticket delivered it
4. Update ticket descriptions to use atomic checkboxes so partial delivery is visible

## Rule: Acceptance Criteria Format
All tickets MUST use checkbox format for acceptance criteria:
```
- [ ] QR code encodes real session ID
- [x] Role selection (player/camera) works
- [ ] Auth redirect on join
```
This makes partial completion visible at a glance.

## Enforcement
- Orchestrator must include this in all agent task prompts that can close tickets
- Work executor cron prompt must enforce this before marking any ticket Done
- QA audits should flag tickets with stale descriptions vs actual code state
- Sibling updates must use `## [Already Built]` plus checkbox acceptance criteria (`- [x]`, `- [ ]`)
