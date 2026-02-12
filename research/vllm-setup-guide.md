# vLLM Setup Guide — RTX Pro 6000 Blackwell 96GB

**Hardware:** RTX Pro 6000 Blackwell 96GB VRAM, Threadripper Pro 32c/64t, 256GB RAM, Ubuntu/WSL2  
**Purpose:** Serving Qwen3-32B for 1-5 concurrent agent requests, 24/7 production  
**Last updated:** 2026-02-02

---

## Table of Contents

1. [Installation](#1-installation)
2. [Serving Qwen3-32B](#2-serving-qwen3-32b)
3. [Quantization Support](#3-quantization-support)
4. [Performance Tuning](#4-performance-tuning)
5. [Concurrent Request Handling](#5-concurrent-request-handling)
6. [Speculative Decoding](#6-speculative-decoding)
7. [Memory Management](#7-memory-management)
8. [Comparison with llama.cpp](#8-comparison-with-llamacpp)
9. [Systemd Service](#9-systemd-service)
10. [OpenClaw Integration](#10-openclaw-integration)

---

## 1. Installation

### Blackwell GPU Requirements

The RTX Pro 6000 Blackwell uses **sm_120** compute capability. This requires:

- **CUDA ≥ 12.8** (CUDA 12.9+ recommended for latest vLLM)
- **PyTorch ≥ 2.6** with CUDA 12.8+ wheels
- **Python 3.10–3.12** (3.12 recommended)
- **Driver ≥ 570.x** (Blackwell-compatible)

NVIDIA's vLLM release 25.09 explicitly lists **RTX PRO 6000 Blackwell Server Edition functional support** and compatibility with CUDA 13.0.

### Recommended: Docker (NVIDIA NGC Container)

For Blackwell GPUs, Docker is the most reliable path — it bundles the correct CUDA toolkit, PyTorch, and FlashInfer kernels:

```bash
# Pull NVIDIA's official vLLM container (includes Blackwell support)
docker pull nvcr.io/nvidia/vllm:25.09-v1

# Or use the vLLM project's own image
docker pull vllm/vllm-openai:latest

# Run with GPU access
docker run --gpus all \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -p 11437:8000 \
  --ipc=host \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen3-32B \
  --port 8000
```

### Alternative: pip install

```bash
# Create environment
conda create -n vllm python=3.12 -y
conda activate vllm

# Install vLLM (auto-selects correct PyTorch/CUDA)
pip install --upgrade uv
uv pip install vllm --torch-backend=auto

# Verify Blackwell support
python -c "import torch; print(torch.cuda.get_device_name(0)); print(torch.version.cuda)"
```

**⚠️ WSL2 Note:** Ensure the Windows NVIDIA driver is ≥ 570.x. The CUDA toolkit inside WSL2 must match. Docker Desktop with GPU passthrough is the cleanest path on WSL2.

### Alternative: From Source

Only needed if pip/Docker don't have Blackwell kernel support yet:

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e .
```

**Recommendation:** Use Docker for production. Pip for dev/testing. Source only if you hit kernel compilation issues.

---

## 2. Serving Qwen3-32B

### BF16 (Full Precision) — Fits in 96GB

Qwen3-32B at BF16 requires ~64GB VRAM for weights alone. With 96GB VRAM, it fits comfortably with room for KV cache:

```bash
vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 \
  --port 11437 \
  --served-model-name qwen3-32b \
  --dtype bfloat16 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --trust-remote-code
```

### AWQ Quantized (Recommended for Max Context)

```bash
vllm serve Qwen/Qwen3-32B-AWQ \
  --host 127.0.0.1 \
  --port 11437 \
  --served-model-name qwen3-32b \
  --quantization awq \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90
```

AWQ 4-bit reduces model to ~18GB, leaving ~68GB for KV cache — enough for very long contexts or many concurrent sequences.

### GGUF Quantized

```bash
# Download GGUF file first
huggingface-cli download Qwen/Qwen3-32B-GGUF qwen3-32b-q5_k_m.gguf --local-dir ./models

vllm serve ./models/qwen3-32b-q5_k_m.gguf \
  --host 127.0.0.1 \
  --port 11437 \
  --served-model-name qwen3-32b \
  --tokenizer Qwen/Qwen3-32B \
  --quantization gguf \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90
```

### Key Notes

- The Qwen3 pretrained context length is **32,768 tokens**
- vLLM's OpenAI-compatible API is at `http://127.0.0.1:11437/v1`
- Supports `/v1/chat/completions`, `/v1/completions`, `/v1/models`

---

## 3. Quantization Support

### Supported Formats in vLLM

| Format | Supported | Kernel Backend | Quality | Speed | Notes |
|--------|-----------|---------------|---------|-------|-------|
| **BF16** | ✅ | Native | Best | Baseline | ~64GB for 32B model |
| **FP8 (W8A8)** | ✅ | Native/Marlin | Excellent | Fastest | ~32GB, best perf/quality ratio |
| **AWQ (W4A16)** | ✅ | Marlin | Very Good | Very Fast | ~18GB, well-supported |
| **GPTQ (W4A16)** | ✅ | Marlin/GPTQModel | Very Good | Very Fast | ~18GB, widely available |
| **GGUF** | ✅ | Custom | Good | Slower | Any GGUF quant works |
| **BitsAndBytes** | ✅ | BnB | Good | Slow | On-the-fly quantization |
| **NVFP4** | ✅ | TensorRT | Good | Very Fast | Blackwell-native FP4 |

### Can You Use the Same Q5_K_M Quants?

**Yes**, vLLM supports GGUF files including Q5_K_M. However:

- **GGUF in vLLM is slower than AWQ/GPTQ** — GGUF kernels in vLLM are not as optimized as llama.cpp's hand-tuned CUDA kernels
- **AWQ/GPTQ use Marlin kernels** — highly optimized GPU matrix multiplication, significantly faster
- **For vLLM, prefer AWQ or GPTQ quants** over GGUF

### Recommendation for 96GB GPU

| Scenario | Format | Why |
|----------|--------|-----|
| **Best quality, fits easily** | BF16 | 64GB weights + 32GB KV cache, no quality loss |
| **Best quality + long context** | FP8 | 32GB weights + 64GB KV cache, negligible quality loss |
| **Want 4-bit** | AWQ | Fast Marlin kernels, good quality |
| **Already have GGUF files** | GGUF | Works but slower than AWQ |

**With 96GB VRAM, running BF16 or FP8 is the best choice.** You don't need aggressive quantization. Save quantization for when you need longer context or GPU sharing.

---

## 4. Performance Tuning

### Optimal Settings for Single-GPU 96GB

```bash
vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 \
  --port 11437 \
  --served-model-name qwen3-32b \
  --dtype bfloat16 \
  --tensor-parallel-size 1 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 8 \
  --max-num-batched-tokens 32768 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --trust-remote-code
```

### Key Parameters Explained

| Parameter | Value | Why |
|-----------|-------|-----|
| `--tensor-parallel-size 1` | 1 | Single GPU, no TP needed |
| `--max-model-len 32768` | 32768 | Qwen3's full pretrained context |
| `--gpu-memory-utilization 0.90` | 0.90 | Leave 10% headroom (~9.6GB) for CUDA overhead. **Lower to 0.50-0.70 if coexisting with llama.cpp** |
| `--max-num-seqs 8` | 8 | Max concurrent sequences; 8 is fine for 1-5 agent requests |
| `--enable-chunked-prefill` | — | Better ITL by chunking long prompts |
| `--enable-prefix-caching` | — | Caches common prompt prefixes in KV cache; great for agents with system prompts |
| `--enforce-eager` | Optional | Disables CUDA graphs; use only if hitting memory issues or debugging. **Leave off for production** (graphs improve throughput) |
| `--dtype bfloat16` | bfloat16 | Blackwell natively supports BF16 |

### Additional Tuning

- **`--max-num-batched-tokens 2048`** — Lower for better inter-token latency (fewer prefills batched). Raise for better throughput.
- **`--disable-log-requests`** — Reduce logging overhead in production
- **`--uvicorn-log-level warning`** — Less noise

---

## 5. Concurrent Request Handling

### How vLLM Handles Concurrency

vLLM uses **continuous batching** — it doesn't wait for a batch to fill before processing. New requests join the running batch immediately. This is fundamentally different from llama.cpp's slot-based approach.

**PagedAttention** allows dynamic memory allocation per sequence, so sequences of varying lengths share GPU memory efficiently without fragmentation.

### For Your Use Case (1-5 Concurrent Agent Requests)

| Metric | Expected Performance |
|--------|---------------------|
| Single request latency | Comparable to llama.cpp |
| 3-5 concurrent requests | Better throughput than llama.cpp, similar per-request latency |
| 10+ concurrent requests | Dramatically better than llama.cpp |

**At low concurrency (1-2 requests), vLLM and llama.cpp perform similarly.** vLLM's advantage grows with concurrency — at peak load it can deliver **35x+ the throughput** of llama.cpp (Red Hat benchmarks, Sept 2025).

For 1-5 agent requests, vLLM will handle them well but the difference vs llama.cpp won't be dramatic. The main vLLM advantage here is:
- **Prefix caching** — if agents share system prompts, cached prefixes speed up every request
- **No slot starvation** — llama.cpp has fixed slots; vLLM dynamically manages memory

---

## 6. Speculative Decoding

### Status

⚠️ **Speculative decoding in vLLM is not yet fully optimized** (as of early 2026). The docs explicitly warn it "does not usually yield inter-token latency reductions for all prompt datasets or sampling parameters."

### Available Methods

1. **Draft Model** — Use a smaller model (e.g., Qwen3-0.6B) to propose tokens
2. **N-gram** — Match patterns from the prompt to speculate continuations
3. **EAGLE/Eagle3** — SOTA speculative method using a trained draft head
4. **Suffix Decoding** — Pattern matching against prompt + previous generations (great for agentic loops)
5. **Medusa** — Multi-head draft prediction

### Configuration Example (Draft Model)

```bash
vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 \
  --port 11437 \
  --speculative_config '{"model": "Qwen/Qwen3-0.6B", "num_speculative_tokens": 5}'
```

### N-gram (No Extra Model)

```bash
vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 \
  --port 11437 \
  --speculative_config '{"method": "ngram", "num_speculative_tokens": 5, "prompt_lookup_max": 4}'
```

### Recommendation

- **For agentic workloads**, try **suffix decoding** — it excels at repetitive patterns common in agent loops
- **N-gram** is zero-cost to try (no extra model)
- **Draft model** approach has been unstable in recent versions — test thoroughly before production
- **EAGLE3 is SOTA** but requires a trained draft head specific to your model

**Practical advice:** Don't rely on speculative decoding for production yet. It's an optimization to experiment with after your basic setup is stable.

---

## 7. Memory Management

### PagedAttention

vLLM's core innovation. Instead of pre-allocating contiguous memory per sequence, it uses virtual memory pages:

- **Page size:** Typically 16 tokens per block
- **No memory waste:** Sequences only use what they need
- **Dynamic allocation:** Memory freed immediately when sequences complete

### VRAM Budget (BF16 Qwen3-32B on 96GB)

| Component | VRAM |
|-----------|------|
| Model weights (BF16) | ~64 GB |
| CUDA overhead + kernels | ~2-4 GB |
| KV cache (at 90% util) | ~22-26 GB |
| **Available for KV cache** | Enough for ~4-8 concurrent 32K sequences |

### Coexisting with llama.cpp on Same GPU

**This is possible but requires careful memory budgeting:**

```bash
# vLLM: use only 50% of GPU memory
vllm serve Qwen/Qwen3-32B-AWQ \
  --quantization awq \
  --gpu-memory-utilization 0.50 \
  --max-model-len 8192 \
  --port 11437

# llama.cpp: uses remaining ~48GB
# Set llama.cpp's --n-gpu-layers and context appropriately
```

**Key considerations:**
- `--gpu-memory-utilization` controls the **total** fraction of GPU memory vLLM will allocate (weights + KV cache + overhead)
- vLLM pre-allocates this memory at startup and does NOT release it
- **vLLM does not play nice with dynamic GPU sharing** — it grabs its allocation and holds it
- For coexistence, use AWQ/GPTQ (~18GB weights) with `--gpu-memory-utilization 0.50` (~48GB total for vLLM)
- Start vLLM first, then llama.cpp (or vice versa — but be consistent)

**⚠️ Warning:** Running both on the same GPU is fragile. If either process OOMs, both may crash. Consider running them as separate services with health checks.

**Better approach:** Run one at a time, or use vLLM for everything (it can serve multiple models).

---

## 8. Comparison with llama.cpp

### For Your Specific Use Case

| Factor | llama.cpp | vLLM | Winner |
|--------|-----------|------|--------|
| **Setup complexity** | Simple, single binary | Python ecosystem, CUDA deps | llama.cpp |
| **1-2 concurrent requests** | Fast, low overhead | Similar speed, more overhead | Tie / llama.cpp |
| **3-5 concurrent requests** | Degrades (slot contention) | Handles well (continuous batching) | vLLM |
| **Quantization flexibility** | GGUF king, many quant levels | AWQ/GPTQ/FP8, GGUF slower | Depends |
| **GGUF performance** | Highly optimized CUDA kernels | Functional but slower | llama.cpp |
| **AWQ/GPTQ performance** | Not supported | Marlin kernels, very fast | vLLM |
| **BF16 full precision** | Supported but less optimized | Excellent | vLLM |
| **Prefix caching** | Limited/manual | Built-in, automatic | vLLM |
| **Memory efficiency** | Fixed slot allocation | PagedAttention, dynamic | vLLM |
| **OpenAI API compat** | Basic (via server mode) | Full-featured | vLLM |
| **Resource usage** | ~200MB process overhead | ~2-4GB Python/CUDA overhead | llama.cpp |
| **Stability / maturity** | Very stable | Rapidly evolving, occasional bugs | llama.cpp |
| **WSL2 support** | Excellent | Good (Docker recommended) | llama.cpp |

### Verdict

**For 1-2 concurrent requests:** llama.cpp is simpler, lighter, and performs identically. Stick with it.

**For 3-5 concurrent requests with shared system prompts:** vLLM's prefix caching and continuous batching provide a real advantage.

**Is vLLM overkill?** Somewhat, yes — for 1-5 agent requests. vLLM shines at 10+ concurrent requests where it delivers 35x+ throughput gains. At low concurrency, you're paying the complexity cost for modest gains.

### Recommendation

**Keep llama.cpp as your primary server.** Consider vLLM if:
1. You regularly hit 3+ concurrent agent requests
2. Your agents share long system prompts (prefix caching saves significant compute)
3. You want to run BF16 or FP8 instead of GGUF quants
4. You need features like guided generation (structured output) at the serving layer

**Or:** Run both! llama.cpp on port 11436 (current), vLLM on port 11437. Route different workloads to each. Use `--gpu-memory-utilization 0.45` for vLLM with AWQ to leave room for llama.cpp.

---

## 9. Systemd Service

### User Service (recommended)

```bash
mkdir -p ~/.config/systemd/user
```

Create `~/.config/systemd/user/vllm.service`:

```ini
[Unit]
Description=vLLM Inference Server (Qwen3-32B)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/home/sean/miniconda3/envs/vllm/bin/vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 \
  --port 11437 \
  --served-model-name qwen3-32b \
  --dtype bfloat16 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 8 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --disable-log-requests \
  --trust-remote-code
Restart=always
RestartSec=10
Environment=HUGGING_FACE_HUB_TOKEN=<your-token>
Environment=CUDA_VISIBLE_DEVICES=0
WorkingDirectory=/home/sean

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=vllm

[Install]
WantedBy=default.target
```

### Docker variant

```ini
[Unit]
Description=vLLM Inference Server (Docker)
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStartPre=-/usr/bin/docker rm -f vllm-server
ExecStart=/usr/bin/docker run --rm --name vllm-server \
  --gpus all \
  --ipc=host \
  -v /home/sean/.cache/huggingface:/root/.cache/huggingface \
  -p 127.0.0.1:11437:8000 \
  -e HUGGING_FACE_HUB_TOKEN=<your-token> \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen3-32B \
  --served-model-name qwen3-32b \
  --dtype bfloat16 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 8 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --disable-log-requests \
  --trust-remote-code
Restart=always
RestartSec=15
ExecStop=/usr/bin/docker stop vllm-server

[Install]
WantedBy=default.target
```

### Enable and Start

```bash
systemctl --user daemon-reload
systemctl --user enable vllm.service
systemctl --user start vllm.service
systemctl --user status vllm.service
journalctl --user -u vllm -f  # tail logs
```

---

## 10. OpenClaw Integration

vLLM's OpenAI-compatible API works directly as an `openai-completions` provider in OpenClaw.

### OpenClaw Gateway Config Snippet

In your OpenClaw gateway configuration (e.g., `config.yaml` or provider config):

```yaml
providers:
  - id: vllm-qwen3-32b
    type: openai-completions
    model: qwen3-32b  # matches --served-model-name
    baseUrl: http://127.0.0.1:11437/v1
    apiKey: "not-needed"  # vLLM doesn't require auth by default
    options:
      temperature: 0.7
      max_tokens: 4096
```

Or as an OpenClaw model entry:

```yaml
models:
  - id: qwen3-32b
    provider: openai-completions
    config:
      baseUrl: http://127.0.0.1:11437/v1
      apiKey: "none"
      model: qwen3-32b
```

### Verification

```bash
# Test the endpoint directly
curl http://127.0.0.1:11437/v1/models

curl http://127.0.0.1:11437/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-32b",
    "messages": [{"role": "user", "content": "Hello!"}],
    "max_tokens": 100
  }'
```

### Notes

- vLLM supports streaming (`"stream": true`) — works with OpenClaw's streaming
- Tool/function calling is supported for chat models
- The `/v1/completions` endpoint also works for raw completion providers
- No API key needed by default; add `--api-key <key>` to vLLM if you want auth

---

## Quick Start TL;DR

**Fastest path to production:**

```bash
# 1. Install
pip install vllm  # or use Docker

# 2. Serve (BF16, full quality, fits in 96GB)
vllm serve Qwen/Qwen3-32B \
  --host 127.0.0.1 --port 11437 \
  --served-model-name qwen3-32b \
  --dtype bfloat16 --max-model-len 32768 \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 8 \
  --enable-chunked-prefill --enable-prefix-caching

# 3. Test
curl http://127.0.0.1:11437/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-32b","messages":[{"role":"user","content":"Hi"}]}'

# 4. Daemonize with systemd (see Section 9)
```

**If coexisting with llama.cpp:** Use AWQ quant + `--gpu-memory-utilization 0.50`.

**If only 1-2 concurrent requests:** Stick with llama.cpp. It's simpler and equally fast.
