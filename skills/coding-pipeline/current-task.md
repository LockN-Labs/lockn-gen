LOCKN-515 - Decision Reminder Engine Implementation

Implement 3-tier decision reminder cadence system with cron-backed scheduling.

Requirements:
- High urgency: fast cadence (every 15-30 min)
- Medium urgency: balanced cadence (hourly)
- Low urgency: light cadence (daily)
- Quiet-hour safeguards (no reminders 10pm-7am unless urgent)
- Stop reminders when decision marked resolved
- Include channel/thread and correlation ID in reminder sends
- Use OpenClaw cron for scheduling
- Prevent duplicate reminders with tracking state

Architecture:
- reminder-engine service with configurable cadence rules
- integration with LockN Control decision system
- correlation ID tracking for each decision
- state persistence to prevent duplicates
- cron job registration for each urgency tier

Implementation should be in lockn-ai-platform repository.
