# TOOLS.md - Local Notes

## Hardware

- **CPU:** AMD Threadripper Pro 32c/64t
- **GPU:** NVIDIA RTX Pro 6000 Blackwell 96GB VRAM
- **RAM:** 256GB
- **Storage:** 2× Samsung 9100 Pro 4TB NVMe

## Local Inference Endpoints

| Service    | Port  | URL                          | Models                              |
|------------|-------|------------------------------|-------------------------------------|
| Ollama     | 11434 | http://127.0.0.1:11434      | qwen3-embedding:latest              |
| Ollama (v1)| 11435 | http://127.0.0.1:11435/v1   | glm-4.7-flash:latest (200K ctx)     |
| llama.cpp  | 11436 | http://127.0.0.1:11436/v1   | glm-4.7-flash-heretic Q4_K_M (32K ctx) |

- Ollama port 11434 is used for embeddings (memory search)
- Ollama port 11435 is the OpenAI-compatible completions endpoint
- llama.cpp port 11436 runs the reasoning-capable quantized model

## Gateway

- **Port:** 18789 (loopback only)
- **Auth:** Token-based (env var `OPENCLAW_GATEWAY_TOKEN`)
- **Systemd unit:** `openclaw-gateway.service` (user service)

## Channels

- **Slack:** Socket mode, bot + app tokens via env vars

## Skills Installed

- slack, skill-creator, bluebubbles, tmux, weather, browser

## Notes

- Both Ollama and llama.cpp compete for the same GPU; avoid running heavy concurrent inference on both
- Embeddings (qwen3-embedding) run on the separate Ollama instance (port 11434)
