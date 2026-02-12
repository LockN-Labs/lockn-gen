# Coding Pipeline Setup

## llama.cpp Service for Qwen3-Coder

### Systemd Service: `llama-qwen3coder.service`

```ini
[Unit]
Description=llama.cpp server - Qwen3-Coder-30B-A3B Q8_0
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/llama-server \
  -m %h/models/Qwen3-Coder-30B-A3B-Q8_0.gguf \
  -ngl 99 \
  -c 32768 \
  --port 11438 \
  -fa \
  -cnv \
  --threads 8
Restart=on-failure
RestartSec=5
Environment=CUDA_VISIBLE_DEVICES=0

[Install]
WantedBy=default.target
```

### Installation

```bash
# Copy service file
mkdir -p ~/.config/systemd/user/
cp llama-qwen3coder.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now llama-qwen3coder.service
```

### Verification

```bash
curl -s http://127.0.0.1:11438/v1/models | python3 -m json.tool
curl -s http://127.0.0.1:11438/health
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CODER_API_URL` | `http://127.0.0.1:11438/v1/chat/completions` | Worker API endpoint |
| `CODER_MODEL` | `qwen3-coder` | Model name for API requests |
| `CODER_MAX_TOKENS` | `4096` | Max output tokens per request |
| `CODER_TEMPERATURE` | `0.2` | Generation temperature |
| `CODER_TIMEOUT` | `120` | Request timeout in seconds |
| `SYSTEM_PROMPT` | (built-in) | Override system prompt |

## VRAM Budget

| Model | VRAM | Port | Purpose |
|-------|------|------|---------|
| qwen3-embedding | ~1 GB | 11434 | Embeddings |
| GLM-4.7-Flash Q6_K | ~26 GB | 11436 | General agent |
| Qwen3-32B Q5_K_M | ~23 GB | 11437 | Reasoning |
| Qwen3-Coder Q8_0 | ~30 GB | 11438 | Code generation |
| **Total** | **~80 GB** | | **of 96 GB** |

Note: With all 4 models loaded, ~16 GB remains for KV caches. Qwen3-Coder is MoE (3B active params) so KV cache needs are modest. Monitor with `nvidia-smi`.
