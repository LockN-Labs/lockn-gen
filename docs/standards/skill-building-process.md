# Skill Building Process

## Quality Gate: Dual Sign-Off Required

Every new or updated skill must pass review by **both Opus and Codex** before shipping.

### Pipeline

1. **Draft** — Sonnet, Codex, or Coder-Next creates the initial SKILL.md
2. **Opus Review** — Strategic review for:
   - Completeness (all edge cases covered?)
   - Accuracy (correct tool names, API patterns, thresholds?)
   - Clarity (would an agent with no context follow this successfully?)
   - Improvements (what's missing? what could be better?)
3. **Codex Review** — Technical validation for:
   - Tool names match actual OpenClaw tools (no hallucinated CLIs)
   - Code examples are executable, not pseudo-code
   - File paths and config references are real
   - Integration points are tested
4. **Ship** — Only after both approve, merge into workspace

### Why

Skills are our institutional knowledge. Bad skills compound into bad outputs across every agent that uses them. High-quality skills = high-quality autonomous work.

### Implementation

When spawning skill-building work:
```
1. Spawn drafter (Sonnet/Codex) → creates SKILL.md
2. Spawn Opus reviewer → reads SKILL.md, posts improvements
3. Spawn Codex reviewer → validates technical accuracy
4. Apply fixes from both reviews
5. Mark ticket Done
```

### Anti-Patterns to Avoid
- Fake CLI commands that don't exist as executables
- Pseudo-code presented as runnable implementations
- Referencing tools by wrong names
- Missing error handling or escalation paths
- Overly verbose boilerplate that dilutes the actual workflow
