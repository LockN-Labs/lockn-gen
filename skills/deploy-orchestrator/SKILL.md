# deploy-orchestrator

Production-grade blue/green deployment with automated QA gates.

## Purpose

Automate zero-downtime deployments for LockN services using blue/green switching via Caddy upstreams. Includes pre-deploy regression tests, post-deploy smoke tests, and automatic rollback on failure.

## Tools

| Tool | Description |
|------|-------------|
| `deploy.full` | Full deployment: regression → promote → smoke → rollback if needed |
| `deploy.regression` | Run QA regression tests against Test environment |
| `deploy.promote` | Promote service to Prod using blue/green swap |
| `deploy.smoke` | Run smoke tests against Prod |
| `deploy.rollback` | Rollback to previous color |
| `deploy.status` | Report last deployment status |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEPLOY_HOST` | Yes | SSH host for deployment (e.g., `deploy@prod-host`) |
| `DEPLOY_SSH_OPTS` | No | SSH options (e.g., `-i ~/.ssh/deploy_key`) |
| `DEPLOY_SSH_PORT` | No | SSH port (default: 22) |
| `DEPLOY_COMPOSE_DIR` | No | Docker Compose base dir on host (default: `/srv/apps`) |
| `DEPLOY_CADDY_API` | No | Caddy Admin API endpoint (default: `http://127.0.0.1:2019`) |
| `DEPLOY_TIMEOUT` | No | Health check timeout in seconds (default: 60) |
| `SLACK_WEBHOOK_URL` | No | Slack webhook for deployment notifications |
| `SLACK_CHANNEL` | No | Slack channel name |
| `GITHUB_TOKEN` | No | GitHub token for fetching latest image tags |
| `REGISTRY_URL` | No | Container registry URL (default: `ghcr.io/lockn-ai`) |

## Usage Examples

```bash
# Full deployment (recommended)
./scripts/deploy.sh lockn-logger v1.2.3

# Individual steps
./scripts/regression.sh lockn-logger    # Pre-deploy tests
./scripts/promote.sh lockn-logger v1.2.3  # Blue/green swap
./scripts/smoke.sh lockn-logger          # Post-deploy tests
./scripts/rollback.sh lockn-logger       # Emergency rollback

# Check status
./scripts/status.sh lockn-logger
./scripts/status.sh all
```

## Deployment Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        deploy.sh <service> <tag>                    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Step 1: Regression Tests (Test Environment)                       │
│  - Hit health endpoint                                              │
│  - Test critical paths                                              │
│  - Verify service stability                                         │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                           ┌──────┴──────┐
                           │   PASS?     │
                           └──────┬──────┘
                        No │             │ Yes
                           ▼             ▼
                    ┌──────────┐   ┌─────────────────────────────────┐
                    │  ABORT   │   │  Step 2: Blue/Green Promotion   │
                    │ (notify) │   │  - Pull new image               │
                    └──────────┘   │  - Start standby container      │
                                   │  - Wait for health              │
                                   │  - Swap Caddy upstream (API)    │
                                   │  - Stop old container           │
                                   └─────────────────────────────────┘
                                                  │
                                                  ▼
                    ┌─────────────────────────────────────────────────┐
                    │  Step 3: Smoke Tests (Production)               │
                    │  - Test critical paths on live traffic          │
                    │  - Verify response codes and latency            │
                    └─────────────────────────────────────────────────┘
                                                  │
                                          ┌───────┴───────┐
                                          │    PASS?      │
                                          └───────┬───────┘
                                       No │               │ Yes
                                          ▼               ▼
                    ┌─────────────────────────────┐   ┌───────────────┐
                    │  Step 4: Automatic Rollback │   │   SUCCESS!    │
                    │  - Swap back to old color   │   │   (notify)    │
                    │  - Stop failed container    │   └───────────────┘
                    │  - Notify Slack             │
                    └─────────────────────────────┘
```

## Caddy Blue/Green Switching

The deployment uses Caddy's Admin API to switch upstreams without reload:

```bash
# Switch lockn-logger to green
curl -X PATCH http://127.0.0.1:2019/id/lockn-logger_upstream \
  -H 'Content-Type: application/json' \
  -d '{"upstreams":[{"dial":"lockn-logger-green:5000"}]}'

# Verify current config
curl http://127.0.0.1:2019/id/lockn-logger_upstream | jq
```

## Directory Structure on Deploy Host

```
/srv/apps/
├── lockn-logger/
│   ├── active_color       # "blue" or "green"
│   ├── previous_color     # for rollback
│   ├── blue/
│   │   └── docker-compose.yml
│   └── green/
│       └── docker-compose.yml
├── lockn-score/
│   ├── active_color
│   ├── previous_color
│   ├── blue/
│   │   └── docker-compose.yml
│   └── green/
│       └── docker-compose.yml
└── ...
```

## Service Configuration

Edit `config/services.yaml` to configure services:

```yaml
services:
  lockn-logger:
    test_url: "https://test.lockn.ai"
    prod_url: "https://lockn.ai"
    health_endpoint: "/health"
    critical_paths:
      - "/"
      - "/metrics"
```

## 5am Production Cron

Install the cron job for automated daily deployments:

```bash
# Add to crontab
0 5 * * * /path/to/skills/deploy-orchestrator/scripts/cron-prod-deploy.sh >> /var/log/lockn-deploy.log 2>&1
```

The cron job:
1. Iterates all configured services
2. Fetches latest semantic version tag from registry
3. Skips if already deployed
4. Runs full deployment flow
5. Logs results and notifies Slack

## Rollback

Manual rollback if needed:

```bash
./scripts/rollback.sh lockn-logger
```

This:
1. Swaps Caddy upstream back to previous color
2. Stops the failed container
3. Updates active_color state file

## State Files

Deployment state is stored in `state/`:

```json
{
  "service": "lockn-logger",
  "image_tag": "v1.2.3",
  "status": "success",
  "timestamp": "2026-02-07T05:00:00-05:00",
  "notes": "Deployed v1.2.3 successfully"
}
```

Status values: `success`, `failed`, `rolled_back`

## Slack Notifications

If `SLACK_WEBHOOK_URL` is set, deployments send:
- 🚀 Starting deployment
- ✅ Success
- ⚠️ Rolled back
- ❌ Failed
- 🚨 Critical (rollback also failed)

## Troubleshooting

### Health check fails
```bash
# Check container logs
ssh $DEPLOY_HOST "docker logs lockn-logger-green"

# Check health endpoint manually
ssh $DEPLOY_HOST "curl -v http://lockn-logger-green:5000/health"
```

### Caddy API not responding
```bash
# Check Caddy is running
ssh $DEPLOY_HOST "systemctl status caddy"

# Check admin API
ssh $DEPLOY_HOST "curl http://127.0.0.1:2019/config/"
```

### Rollback fails
```bash
# Manual intervention required
ssh $DEPLOY_HOST "docker ps -a"  # Check container state
ssh $DEPLOY_HOST "cat /srv/apps/lockn-logger/active_color"
ssh $DEPLOY_HOST "cat /srv/apps/lockn-logger/previous_color"
```
