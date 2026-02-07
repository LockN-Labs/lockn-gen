---
name: rapid-dev
description: Rapid development mode for quick UI/config changes. Commits directly to main during session, creates summary PR at end. Use for iterative work with Sean where PR overhead slows momentum.
aliases: [rapid-dev, rapid, quick-dev]
---

# Rapid Development Mode

Use this mode when doing iterative UI/config work with Sean where the normal PR workflow adds friction.

## When to Use

- Quick UI tweaks with immediate feedback
- Config changes that need rapid iteration
- Bug fixes during live debugging sessions
- Any work where Sean says "rapid-dev" or "let's iterate quickly"

## Workflow

### 1. Enter Rapid Dev Mode

When Sean requests rapid iteration:
```
🚀 Entering rapid-dev mode for [repo/feature]
- Commits will go directly to main
- Will create summary PR at session end
```

### 2. During Session

- Commit directly to main with clear commit messages
- Track all commits made (store in session context)
- Prefix commits with `rapid:` for easy identification

### 3. Exit Rapid Dev Mode

At session end or when Sean says "wrap up":

```bash
# Create a branch from before the rapid commits
git checkout -b rapid-dev/[date]-[feature] [first-commit]^

# Cherry-pick all rapid commits
git cherry-pick [commit1] [commit2] ...

# Or: Create documentation PR with summary
```

**Alternative:** Create a retroactive documentation PR:
```bash
# Just document what was done
gh pr create --title "docs: Rapid-dev session [date] - [feature]" \
  --body "## Changes made in rapid-dev session\n\n[commit list with descriptions]"
```

## Tracking Commits

Keep a running list during the session:
```
📝 Rapid-dev commits:
- abc1234: feat(speak): add Download button
- def5678: fix(speak): update branding
- ghi9012: feat(speak): add edit profiles
```

## Exit Checklist

- [ ] All changes tested by Sean
- [ ] Create summary PR or documentation
- [ ] Update Linear tickets if applicable
- [ ] Return to normal PR workflow

## Example Session

```
Sean: "Let's iterate on the Speak UI quickly"
Claws: "🚀 Entering rapid-dev mode for lockn-ai-platform/speak"

[... multiple commits directly to main ...]

Sean: "OK wrap it up"
Claws: "📋 Rapid-dev session complete. 9 commits made:
- 0e9e920: TTS Playground default tab
- 8440f7c: tab reorder
[...]

Creating summary PR..."
```
