# Linear Project Restructure — Ops Procedure

## Problem
- Only 4 projects exist; ~150+ issues are unassigned to any project
- CEO cannot drag-to-prioritize projects because the project list doesn't reflect actual initiatives
- No "System Improvements" catch-all for cross-cutting work

## Linear Hierarchy (as designed)
```
Initiatives (strategic themes)
  └── Projects (time-bound deliverables)
       └── Issues (tasks)
            └── Sub-issues
```

## Target Project Structure

### Initiative: Revenue Engine
| Project | Key Issues | Status |
|---------|-----------|--------|
| Revenue: Auth-to-Checkout Pipeline | LOC-421, 256, 257, 441, 442, 342 | Active |
| Revenue: Landing & Conversion | LOC-255, 302, 344, 345, 415 | Active |
| Revenue: Marketing & Growth Ops | LOC-303, 306, 310, 312, 348, 414 | Planned |
| Revenue: Billing & Monetization | LOC-347, 443, 444, 231, 236, 296, 413 | Planned |

### Initiative: LockN Product Suite
| Project | Key Issues | Status |
|---------|-----------|--------|
| LockN Score MVP | LOC-200, 367-370, 382-387 | Active |
| LockN Score UX | LOC-405-410 | Active |
| LockN Brain | LOC-119, 374-377 | Planned |
| LockN Listen | LOC-227, 241, 259-261, 298 | Planned |
| LockN Gen | LOC-234, 239, 243, 268-269, 280-283, 301 | Stalled |
| LockN Voice | (existing project) | Backlog |
| LockN Loader | LOC-246 | Backlog |

### Initiative: Platform & Auth
| Project | Key Issues | Status |
|---------|-----------|--------|
| Auth & Security | LOC-425, 426, 422, 423, 411, 284, 285 | Active |
| XRPL Trading (Swap+Swing) | LOC-323-332 | Planned |

### Initiative: Operations & Infrastructure
| Project | Key Issues | Status |
|---------|-----------|--------|
| Infrastructure Modernization v2 | (existing, has issues) | In Progress |
| System Improvements | LOC-172, 404, 351, 307, 349, 308, etc. | Ongoing |
| OpenClaw Skills | (existing, has issues) | Active |
| C-Suite Agent Profiles | LOC-429-440 | Backlog |
| Memory Search Quality | LOC-334-340 | Active |

### Initiative: UX & Design
| Project | Key Issues | Status |
|---------|-----------|--------|
| UX Redesign Overhaul | LOC-397-403 | Active |

## Execution Rules

1. **Every issue MUST belong to a project** — orphan issues get filed to "System Improvements"
2. **Projects have priorities** — CEO drags to reorder in Priority Queue view
3. **Projects have statuses**: Backlog → Planned → In Progress → Done
4. **Projects have leads** — default to Sean until agent leads are assigned
5. **New issues**: Creating agent checks if a matching project exists; if not, files to "System Improvements" and flags for triage

## Automation (Heartbeat Check)

Every heartbeat, verify:
- No orphan issues (issues without project assignment)
- No stale projects (In Progress with no activity >7 days)
- Project priority queue matches CEO's latest ordering

## Agent Execution Plan

Phase 1: Create missing projects with descriptions, priorities, and statuses
Phase 2: Assign all existing issues to their correct projects
Phase 3: Verify Priority Queue view works with the new structure
