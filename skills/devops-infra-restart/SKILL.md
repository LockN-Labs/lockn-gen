# Skill: devops-infra-restart

Ordered infrastructure restart that eliminates race conditions between services and their dependencies.

## When to Use
- After a system reboot (WSL restart, Docker daemon restart)
- When multiple services are down simultaneously
- On heartbeat detection of multiple unhealthy containers
- Manual trigger: "restart infra", "infra check", "services down"

## How It Works

The restart script (`restart-infra.sh`) brings up services in dependency tiers, waiting for health checks between each tier before proceeding. This prevents the race condition where an API service starts before its database is ready.

### Tier Architecture

```
Tier 0: Systemd services (llama.cpp, Ollama, OpenClaw gateway)
Tier 1: Databases & storage (postgres, garnet, seaweedfs, qdrant)
Tier 2: Shared infra (whisper, panns, tts, chatterbox, otel, cloudflared, git)
Tier 3: API services (auth-api, gen-api, logger-api, platform-api, score-api, speak-api, email-api, brain)
Tier 4: Frontend & routing (caddy, score-web, swagger)
```

Each tier waits for all services to be healthy (or reach a timeout) before the next tier starts.

### Health Check Strategy

1. **Docker healthcheck**: Preferred — uses the container's built-in healthcheck
2. **HTTP probe**: Falls back to HTTP GET on the container's exposed port
3. **TCP probe**: Last resort — checks if the port is accepting connections
4. **Timeout**: 60s per tier (configurable via `TIER_TIMEOUT`)

## Usage

### Automatic (from agent)
```bash
bash /home/sean/.openclaw/workspace/skills/devops-infra-restart/restart-infra.sh
```

### Options
```bash
# Full restart (default) — restarts all tiers
bash restart-infra.sh

# Check only — report status without restarting anything
bash restart-infra.sh --check

# Specific tier only
bash restart-infra.sh --tier 1

# Skip systemd (tiers 1-4 only, Docker containers)
bash restart-infra.sh --skip-systemd

# Dry run — show what would be restarted
bash restart-infra.sh --dry-run
```

### Output
The script outputs structured status for each service:
```
[TIER 0] Systemd services...
  ✅ llama-coder-next (port 11439)
  ✅ llama-qwen (port 11437)
  ⚠️  llama-coder-cpu (port 11440) — restarted
  ✅ ollama (port 11434)
  ✅ openclaw-gateway (port 18789)

[TIER 1] Databases & storage...
  ✅ lockn-postgres-dev (healthy)
  ✅ qdrant (healthy)
  ...
```

Exit codes:
- `0` — all services healthy
- `1` — some services failed to start (details in output)
- `2` — critical infrastructure down (databases or systemd)

## Agent Integration

When detecting down services during heartbeat:
1. Run `restart-infra.sh --check` to assess scope
2. If >2 services down across tiers, run full `restart-infra.sh`
3. If only 1-2 services down in same tier, restart individually
4. Report results to `#devops` channel

## Compose Projects Registry

| Project | Config Dir | Services |
|---------|-----------|----------|
| lockn-infra | workspace/lockn-infra | postgres-dev, caddy, speak, email |
| lockn-test | workspace/lockn-infra | postgres-test, caddy-test, speak-test, email-test, platform-api-test |
| lockn-auth | ~/repos/lockn-auth | auth-api, auth-db |
| lockn-gen | ~/repos/lockn-gen | gen-api, gen-db |
| lockn-logger | workspace/lockn-logger | logger-api, postgres, garnet, seaweedfs |
| lockn-score | ~/repos/lockn-score | score-api, score-web |
| lockn-listen | workspace/lockn-listen | whisper-gpu, panns |
| lockn-ai-platform | workspace/lockn-ai-platform | platform-api, brain |
| otel | workspace/lockn-infra/otel | otel-collector, grafana, tempo |
| lockn-git | ~/repos/lockn-git | git, git-mirror |
| rippled | ~/repos/lockn-swap/infra/rippled | rippled |
| (standalone) | workspace/lockn-infra | chatterbox, qdrant, qwen3-tts |

## Maintenance

When adding new services:
1. Add to the appropriate tier in `restart-infra.sh` (TIER_* arrays)
2. Ensure the container has a healthcheck in its docker-compose.yml
3. Update the compose projects table above
