# OpenClaw Lifecycle Management

Comprehensive skill for OpenClaw backup, update, and restore operations using blue-green deployment.

## Commands

| Command | Script | Description |
|---------|--------|-------------|
| `backup` | `01-backup.sh` | Full atomic backup to WSL + Windows |
| `analyze` | `02-analyze.sh` | Analyze update safety (breaking changes, cron compatibility) |
| `stage` | `03-stage.sh` | Install new version in GREEN slot |
| `validate` | `04-validate.sh` | Start GREEN, run health checks |
| `swap` | `05-swap.sh` | Swap GREEN→BLUE, restart gateway |
| `abort` | `06-abort.sh` | Rollback to BLUE, restore from backup |

## Architecture

```
BLUE (production)          GREEN (staging)
~/.npm-global/             ~/.npm-global-green/
~/.openclaw/               ~/.openclaw-green/
Port 18789                 Port 18810
```

**Port gap:** 20+ between instances for derived ports (healthcheck, metrics, etc.)

## Usage

### Full Update Workflow

```bash
# 1. Create backup
./scripts/01-backup.sh

# 2. Analyze update safety
./scripts/02-analyze.sh

# 3. Stage new version in GREEN
./scripts/03-stage.sh

# 4. Validate GREEN instance
./scripts/04-validate.sh

# 5. Swap GREEN→BLUE (commits update)
./scripts/05-swap.sh

# If anything fails:
./scripts/06-abort.sh
```

### Quick Backup Only

```bash
./scripts/01-backup.sh
# Output: ~/backups/openclaw-full-{timestamp}-v{version}.tar.gz
# Mirror: S:\Recovery\OpenClaw\
```

### Restore from Backup

```bash
./scripts/06-abort.sh  # Stops GREEN, restores BLUE from backup
```

## Key Locations

| Item | BLUE (prod) | GREEN (staging) |
|------|-------------|-----------------|
| NPM global | `~/.npm-global/` | `~/.npm-global-green/` |
| Config/state | `~/.openclaw/` | `~/.openclaw-green/` |
| Port | 18789 | 18810 |
| Env var | (default) | `OPENCLAW_CONFIG_PATH`, `OPENCLAW_STATE_DIR` |

## Backup Contents

- `~/.openclaw/` — Config, workspace, state
- `~/.npm-global/lib/node_modules/openclaw/` — Installed package
- Metadata: version, timestamp, cron job count

## Safety Checks

The `analyze` step checks:
- Breaking changes in CHANGELOG
- Cron job compatibility (wakeMode defaults)
- Config schema changes
- Required migrations

## Recovery Scripts

Scripts are persisted in 3 locations for disaster recovery:
1. `~/.openclaw/workspace/skills/openclaw-lifecycle/scripts/`
2. `~/backups/scripts/`
3. `S:\Recovery\Scripts\`

## Environment Variables

GREEN instance requires:
```bash
export OPENCLAW_CONFIG_PATH=~/.openclaw-green/config.yaml
export OPENCLAW_STATE_DIR=~/.openclaw-green/
export PORT=18810
```

## Troubleshooting

**Swap interrupted:** Check for orphaned processes (`pgrep -f openclaw`), manually stop, re-run swap.

**GREEN won't start:** Check port conflicts, validate config syntax, review logs.

**Backup restore fails:** Use Windows mirror at `S:\Recovery\OpenClaw\`.
