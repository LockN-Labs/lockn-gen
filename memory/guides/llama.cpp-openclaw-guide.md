# llama.cpp + OpenClaw Integration Guide

## Summary

**Fact:** llama.cpp provides an OpenAI-compatible API that OpenClaw can connect to directly. No special provider module needed—just configure a custom provider with the correct OpenAI-compatible base URL.

**Recommendation:** Use this as an alternative to Ollama given the tool message format issue documented on 2026-02-01.

---

## Prerequisites

✅ **Completed:** llama.cpp build (all executables and libraries ready).

**Still needed:**
- llama.cpp server executable (already built: `llama-server`)
- At least one `.gguf` model file

### Get a Model

llama.cpp requires `.gguf` format models:

```bash
# Convert Hugging Face model to GGUF (if needed)
python convert_hf_to_gguf.py <path-to-hf-model>

# Or download pre-converted GGUF models
# Example repositories:
# - https://huggingface.co/models?search=gguf
```

---

## Step 1: Start the llama.cpp Server

The server provides an OpenAI-compatible `/v1/chat/completions` endpoint.

```bash
# Basic server startup
./llama-server -m <model.gguf> --port 8080

# With options
./llama-server \
  -m <model.gguf> \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 4096 \
  --threads 32
```

**Verification:**
```bash
# Test with curl
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "any-model",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

---

## Step 2: Configure OpenClaw

Edit your OpenClaw configuration (`~/.openclaw/openclaw.json`):

```json
{
  "models": {
    "providers": {
      "llamacpp": {
        "baseUrl": "http://127.0.0.1:8080/v1",
        "apiKey": "1234",
        "api": "openai-completions",
        "models": [
          {
            "id": "my-model",
            "name": "My llama.cpp Model",
            "reasoning": false,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 8192,
            "maxTokens": 4096
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "llamacpp/my-model"
      }
    }
  }
}
```

**Key Points:**
- `baseUrl`: The llama-server endpoint (port 8080 by default)
- `api`: Must be `"openai-completions"` for standard OpenAI-compatible proxies
- `models[].id`: Used as model reference in primary model selector
- `models[].name`: Display name (optional but recommended)

---

## Step 3: Verify OpenClaw Gateway Restart

After editing `openclaw.json`, restart the OpenClaw gateway to apply the new provider:

```bash
openclaw gateway restart
```

---

## Step 4: Test OpenClaw Integration

Test that OpenClaw can communicate with llama.cpp:

```bash
# List models
openclaw models list

# Set primary model
openclaw models set llamacpp/my-model
```

Test via chat (Slack/Telegram/etc.):

```
Can you help me with a coding task using llama.cpp?
```

---

## Architecture Overview

```
┌─────────────────┐
│   OpenClaw      │
│   Gateway       │
│                 │
│  models.json    │
└────────┬────────┘
         │ OpenAI-compatible API
         │ (http://127.0.0.1:8080/v1)
         │
         ▼
┌─────────────────┐
│  llama-server   │
│  (llama.cpp)    │
│                 │
│  - Port: 8080   │
│  - GGUF models  │
└─────────────────┘
```

---

## Comparison: llama.cpp vs Ollama

| Aspect | llama.cpp | Ollama |
|--------|-----------|--------|
| **API** | OpenAI-compatible (built-in) | OpenAI-compatible (built-in) |
| **API Type** | `openai-completions` | `openai-completions` |
| **Build** | ✅ Complete (session warm-nudibranch) | ❌ Known issues with tool messages |
| **Model Format** | `.gguf` only | Multiple formats (gguf, etc.) |
| **Configuration** | Custom provider in `models.providers` | Built-in `ollama` provider |
| **Recommendation** | Use if Ollama tool calling fails | Use if llama.cpp model selection is complex |

---

## Known Limitations

1. **Model Format:** Only `.gguf` format supported
2. **Tool Calling:** May have same limitations as Ollama (ADK/LiteLLM array content issue)
3. **Model Management:** Need to manually manage `.gguf` files and conversions
4. **Server Process:** Requires keeping `llama-server` running

---

## Troubleshooting

### Server won't start

- Check model file path and format
- Verify enough RAM/CPU for the model size
- Check logs in terminal where server started

### OpenClaw reports connection errors

- Verify server is running: `curl http://localhost:8080/v1/models`
- Check `baseUrl` in `models.providers` matches server port
- Restart gateway: `openclaw gateway restart`

### Model not found

- Verify `models[].id` in config matches what you reference in `agents.defaults.model.primary`
- Confirm model is loaded in llama-server

### Slow responses

- Increase context size (`--ctx-size`)
- Increase threads (`--threads`)
- Use smaller quantization (e.g., Q4_0 vs Q5_K_M)
- Check GPU availability if using CUDA build

---

## Production Best Practices (2026-02-01 Research)

### OpenClaw Configuration
- **API Type:** Use `api: "openai-completions"` for standard OpenAI-compatible proxies (llama.cpp, vLLM, LiteLLM)
- **Only use `openai-responses`** for specialized APIs (e.g., MiniMax)
- **Model ID:** Any name works (llama-server ignores it, uses it for routing only)
- **Context Window:** Match model's native context window (e.g., 8192-128000 for newer models)
- **Max Tokens:** Set conservatively based on use case

### llama-server Production Setup

#### Option A: Native Build with Systemd (Recommended for Production)
```bash
# Build with CUDA
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

# Systemd service example
[Unit]
Description=Llama Server: GLM 4.7 Flash Heretic
After=network.target

[Service]
Type=simple
User=sean
WorkingDirectory=/home/sean/llama.cpp
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="CUDA_SCALE_LAUNCH_QUEUES=4x"
ExecStart=/home/sean/llama.cpp/build/bin/llama-server \
  --model /home/sean/models/glm-4.7-flash-heretic.Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 4096 \
  --threads 32 \
  --n-gpu-layers 33 \
  --log-prefix
Restart=on-failure
RestartSec=5s
StandardOutput=file:/home/sean/llama.cpp/logs/llama-server.stdout.log
StandardError=file:/home/sean/llama.cpp/logs/llama-server.stderr.log

[Install]
WantedBy=multi-user.target
```

**Key Parameters:**
- `--ctx-size`: Context window size (matches model's native context)
- `--threads`: CPU threads (match CPU core count)
- `--n-gpu-layers`: Number of layers on GPU (33 for ~17GB model in Q4 quantization)
- `CUDA_VISIBLE_DEVICES`: GPU selection (0 for single GPU)
- `CUDA_SCALE_LAUNCH_QUEUES=4x`: Multi-GPU optimization (4x default buffer)

#### Option B: Docker Compose (Good for Dev/Test)
```yaml
# docker-compose.yml
version: '3'
services:
  llama-server:
    image: ghcr.io/ggml-org/llama.cpp:server-cuda
    environment:
      - LLAMA_ARG_MODEL=/models/glm-4.7-flash-heretic.Q4_K_M.gguf
      - LLAMA_ARG_CTX_SIZE=4096
      - LLAMA_ARG_N_GPU_LAYERS=33
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### Model Management

#### Recommended Models (2026-02-01)
- **Phi-4 14B** (Microsoft) - Good balance of size/performance
- **Gemma3 27B** (Google) - Strong reasoning capabilities
- **Mistral Small 3.1 24B** (Mistral AI) - Balanced performance
- **GLM 4.7 Flash Heretic** (already selected) - 29.94B params, 16.88 GiB (Q4)

#### Model Selection Guidelines
- **Context Window:** Match use case requirements (8192-128000 for newer models)
- **Quantization:** Q4_K_M (4-bit) balances size/performance for local inference
- **GPU Memory:** Calculate required VRAM (model size × quantization factor)
- **Multiple Models:** Consider separate instances for different use cases

### Monitoring & Observability

#### Systemd Logging
- Enable `StandardOutput` and `StandardError` to log files
- Check logs periodically: `journalctl -u llama-server -f`
- Monitor restarts: `systemctl status llama-server`

#### GPU Monitoring
```bash
# Monitor GPU utilization
watch -n 1 nvidia-smi

# Check CUDA memory
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv
```

#### API Monitoring
```bash
# Health check
curl http://localhost:8080/v1/models

# Chat completion test
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "any-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Security Best Practices

1. **Network Binding:** Use `--host 127.0.0.1` for local-only access (not `0.0.0.0`)
2. **API Key:** Set in OpenClaw config (even if not strictly required)
3. **Docker:** Use `--gpus all` with proper NVIDIA driver
4. **Access Control:** Restrict to trusted hosts if exposing to network
5. **API Server Gateway:** Consider using AI Server gateway for multiple endpoints

### Troubleshooting

#### Server Won't Start
- Verify model file path and format (.gguf only)
- Check GPU availability and CUDA installation
- Review logs for specific error messages
- Verify sufficient RAM/CPU for model size

#### OpenClaw Connection Errors
- Verify server is running: `curl http://localhost:8080/v1/models`
- Check `baseUrl` matches server port
- Restart gateway: `openclaw gateway restart`
- Verify API key configuration

#### Performance Issues
- Increase `--n-gpu-layers` (up to model's total layers)
- Increase `--ctx-size` for larger context windows
- Increase `--threads` for CPU-bound operations
- Check GPU utilization and memory usage
- Use smaller quantization (e.g., Q4_0 vs Q5_K_M)

#### Model Not Found
- Verify `models[].id` in config matches reference
- Confirm model is loaded in llama-server
- Check model name matches model file

### Advanced Patterns

#### API Server Gateway (AI Server)
- **Purpose:** Manage multiple llama-server instances behind single endpoint
- **Benefits:** Centralized management, load balancing, API key management
- **Install:** `https://openai.servicestack.net`
- **Access:** `https://localhost:5006/admin`

#### Async Patterns
- **Queued Requests:** Use `QueueOpenAiChatCompletion` for background processing
- **Callback Pattern:** Use `ReplyTo` callback URL for push notifications
- **Polling:** Check job status with `GetOpenAiChatStatus`

#### Multi-Instance Setup
```yaml
# docker-compose.yml
services:
  llama-server-phi4:
    image: ghcr.io/ggml-org/llama.cpp:server-cuda
    environment:
      - LLAMA_ARG_MODEL=/models/phi-4.Q4_K_M.gguf
      - LLAMA_ARG_CTX_SIZE=4096
    ports:
      - "8000:8080"
    volumes:
      - ./models:/models

  llama-server-gemma:
    image: ghcr.io/ggml-org/llama.cpp:server-cuda
    environment:
      - LLAMA_ARG_MODEL=/models/gemma-3-27b-it-qat-q4_0-gguf
      - LLAMA_ARG_CTX_SIZE=8192
    ports:
      - "8001:8080"
    volumes:
      - ./models:/models
```

### References

- [OpenClaw Model Providers Documentation](https://docs.openclaw.ai/concepts/model-providers)
- [llama.cpp GitHub Repository](https://github.com/ggml-org/llama.cpp)
- [llama.cpp Server Usage](https://github.com/ggml-org/llama.cpp/tree/master/examples/server)
- [OpenAI-Compatible Server Usage](https://learn.arm.com/learning-paths/servers-and-cloud-computing/llama-cpu/llama-server/)
- [ServiceStack AI Server Documentation](https://docs.servicestack.net/ai-server/llama-server)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
- [llama-cpp-python Server](https://llama-cpp-python.readthedocs.io/en/latest/server/)

---

## Status

- ✅ llama.cpp build complete
- ⏳ Awaiting model files and configuration
- ⏳ Gateway restart pending user confirmation

**Next steps for Sean:**
1. Obtain a `.gguf` model file
2. Start `llama-server` to test connectivity
3. Configure `openclaw.json` with `llamacpp` provider
4. Test via OpenClaw chat
5. Decide if this approach works better than Ollama
