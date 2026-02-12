# Infrastructure (Current State)

Purpose: live infrastructure baseline for LockN/OpenClaw operations.

Last reviewed: 2026-02-09 18:00 EST

## Host / Runtime
- Host: `DESKTOP-VTU9OLK` (WSL2 Linux 6.6.87.2-microsoft-standard-WSL2, x64)
- CPU: AMD Threadripper Pro 32c/64t
- GPU: NVIDIA RTX Pro 6000 Blackwell 96GB VRAM
- RAM: 256GB
- Storage: 2× Samsung 9100 Pro 4TB NVMe
- OpenClaw gateway: `127.0.0.1:18789` (v2026.2.6-3)
- Tailscale: WSL 100.90.242.54 / Windows 100.101.173.95 / iPhone 100.91.50.58

## Core User Services (systemd --user)

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| `openclaw-gateway` | 18789 | ✅ Active | v2026.2.6-3 |
| `llama-coder-next` | 11439 | ✅ Active | Qwen3-Coder-Next Q5_K_M (PRIMARY) |
| `llama-coder-cpu` | 11440 | ✅ Active | Qwen3-Coder-Next Q3_K_M (CPU, 2M context) |
| `llama-qwen` | 11437 | ⚠️ Inactive | Qwen3-32B Q5_K_M — needs restart |

## Container Runtime Snapshot (as of 18:00 EST)

### Running (22 containers)
| Container | Ports | Purpose |
|-----------|-------|---------|
| lockn-brain | 8100 | LockN Brain API |
| lockn-caddy | 3080, 3081 | Dev reverse proxy |
| lockn-caddy-test | 3180, 3182 | Test reverse proxy |
| lockn-cloudflared | — | Cloudflare tunnel |
| lockn-email-api | 3004 (internal) | Email API (Dev) |
| lockn-email-api-test | 3104 | Email API (Test) |
| lockn-git | 3300, 2222 | Forgejo git server |
| lockn-git-mirror | — | GitHub ↔ Forgejo sync |
| lockn-grafana | 3200 | Observability dashboard |
| lockn-otel-collector | 4317-4318, 8889 | OpenTelemetry collector |
| lockn-panns | 8893 | Audio classification |
| lockn-platform-api | 8090 (internal) | Platform API (Dev) |
| lockn-platform-api-test | 3181 | Platform API (Test) |
| lockn-score-api | 8000 | Score API |
| lockn-score-web | 3000 | Score frontend |
| lockn-speak-api | 3003 (internal) | Speak TTS (Dev) |
| lockn-speak-api-test | 3103 | Speak TTS (Test) |
| lockn-swagger | 80, 8080 (internal) | API documentation |
| lockn-tempo | 3100, 9411 | Distributed tracing |
| lockn-whisper-gpu | 8890 | Whisper STT |
| qwen3-tts-api | 8880 | Qwen3-TTS engine |
| openclaw-sbx-agent-main-* | — | OpenClaw sandbox |

### Stopped / Crashed (needs attention)
| Container | Status | Severity |
|-----------|--------|----------|
| **lockn-speak-dev** | 🔴 Restart loop (SIGSEGV/139) | Medium — dev only |
| **qdrant** | 🔴 Exited (255) | **High** — vector DB for RAG |
| **chatterbox-v4** | 🔴 Exited (255) | Medium — voice cloning |
| **lockn-auth-api-1** | 🔴 Exited (255) | **High** — auth service |
| **lockn-auth-db-1** | 🔴 Exited (255) | **High** — auth database |
| **lockn-gen-api-1** | 🔴 Exited (255) | Medium — gen API |
| **lockn-gen-db-1** | 🔴 Exited (255) | Medium — gen database |
| **lockn-logger-api-1** | 🔴 Exited (255) | **High** — usage logging |
| **lockn-logger-postgres-1** | 🔴 Exited (255) | **High** — logger DB |
| **lockn-logger-garnet-1** | 🔴 Exited (255) | Medium — logger cache |
| **lockn-logger-seaweedfs-1** | 🔴 Exited (255) | Medium — logger blob storage |
| **lockn-postgres-dev** | 🔴 Exited (255) | **High** — shared dev DB |
| **lockn-postgres-test** | 🔴 Exited (255) | **High** — shared test DB |

**Root cause hypothesis:** All exited ~2 hours ago with code 255 — likely a system restart or Docker daemon restart that didn't bring all compose stacks back. The running containers (lockn-infra stack) appear to have auto-restarted while the independently-composed stacks (auth, gen, logger, qdrant) did not.

## Port Allocation Convention
| Range | Environment |
|-------|-------------|
| 3001-3099 | Dev |
| 3101-3199 | Test |
| 3201-3299 | Prod |
| 8000-8999 | Services / ML |

## Observability Stack
- **Grafana:** :3200 (dashboards)
- **Tempo:** :3100 (distributed tracing)
- **OTel Collector:** :4317-4318 (telemetry ingestion)
- **Prometheus metrics:** :8889

## Security Posture
Current critical findings (from `openclaw status` audit):
1. Elevated exec allowlist contains wildcard on Slack
2. Slack group policy is open while elevated tooling is enabled
3. Config file permission too broad (`664`)
4. Slack channel policy warning (allowlist not enforced)

These are active operational risk — not documentation issues.

## Maintenance Rule
Update this page after:
- Major service additions/removals
- Security policy changes
- Model endpoint topology changes
- Container state changes (after restart/recovery)
