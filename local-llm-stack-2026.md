# Local LLM Multi-Model Stack for OpenClaw Agents
## RTX Pro 6000 Blackwell (96GB VRAM) — February 2026

---

## 1. Best Models by Task Category

### 🧠 Reasoning/Planning

| Model | Params | Active | Context | Notes |
|-------|--------|--------|---------|-------|
| **DeepSeek V3.2-Speciale** | 685B | ~37B (MoE) | 128K | IMO gold-level reasoning; MIT license; **too large for single GPU** — needs 8×H100 or heavy quant on multi-GPU |
| **Qwen3-32B** | 32B | 32B (dense) | 128K | Best dense reasoning model that fits in 96GB at high quant; strong chain-of-thought in thinking mode |
| **Qwen3-235B-A22B** | 235B | 22B (MoE) | 128K | Q4_K_M ≈ ~70GB VRAM; excellent reasoning at low active param cost |
| **GPT-OSS-120B** | 117B | ~5B (MoE) | 128K | OpenAI's open-weight reasoning model; MMLU ~90%; competitive with o4-mini |

**Winner for your setup:** **Qwen3-235B-A22B** at Q4_K_M (~70GB) for maximum reasoning power, or **Qwen3-32B** at Q6_K (~26GB) for reasoning + room for other models.

### 🔧 Tool-Calling / Agentic

| Model | Params | Active | Context | Tool-Calling Quality |
|-------|--------|--------|---------|---------------------|
| **GLM-4.7-Flash** | 30B | 3B (MoE) | 200K | ⭐ **Best-in-class for agentic/tool-calling at its size.** Hundreds of thousands of tokens in agentic sessions without tool-call errors. Beats GPT-OSS-20B. |
| **Qwen3-14B** | 14B | 14B (dense) | 128K | Strong tool-calling; dual-mode (thinking/fast); proven working with OpenClaw + 40 tools |
| **Qwen3-32B** | 32B | 32B (dense) | 128K | Best dense model for complex multi-step tool orchestration |
| **DeepSeek V3.2-Thinking** | 685B | ~37B (MoE) | 128K | First model to integrate reasoning directly into tool-use; **too large for single GPU** |
| **GPT-OSS-20B** | 21B | 21B (dense) | 32K | Decent tool-calling, "competitive with o4-mini" on benchmarks, but GLM-4.7 beats it in practice |

**Winner for your setup:** **GLM-4.7-Flash** — you're already running it. It's the community consensus best agentic local model. 3B active params = blazing fast, 200K context, rock-solid tool calling.

### 💻 Coding

| Model | Params | Active | Context | Notes |
|-------|--------|--------|---------|-------|
| **Qwen3-Coder-30B-A3B** | 30B | 3B (MoE) | 128K | Purpose-built coder; Terminal-Bench 37.5% (beats Sonnet in some areas) |
| **Devstral 2 (24B)** | 24B | 24B (dense) | 128K | Mistral's coding model; community reports it beating Qwen3-Coder-30B for sub-30B coding |
| **GLM-4.7-Flash** | 30B | 3B (MoE) | 200K | Surprisingly strong at coding — better than GPT-OSS-120B and Devstral 24B for repo-level refactoring per user reports |
| **Kimi K2.5** | ~1T | 32B (MoE) | 128K | Open-weight; AIME 96.1%, SWEBench verified 76.8%; **too large for single GPU at full precision** |
| **Devstral 2 (123B)** | 123B | ? (MoE) | 128K | Mistral's large coding model; likely ~60-80GB at Q4 |

**Winner for your setup:** **GLM-4.7-Flash** for everyday coding agent work (fast, reliable). **Devstral 2 24B** at Q6_K (~20GB) as a second opinion / specialized coder. For maximum quality, run **Qwen3-32B** at Q5_K_M (~25GB).

### 📚 Research/Summarization (Fast, Long Context)

| Model | Params | Active | Context | Notes |
|-------|--------|--------|---------|-------|
| **GLM-4.7-Flash** | 30B | 3B (MoE) | **200K** | Longest context + fastest inference = perfect for bulk processing |
| **Qwen3-30B-A3B** | 30B | 3B (MoE) | 128K | MoE efficiency; 90% cheaper than running all 30B |
| **Llama 4 Scout** | 109B | 17B (MoE) | **10M** | Insane context window; Q4 ≈ ~60GB VRAM; great for massive document processing |

**Winner:** **GLM-4.7-Flash** for speed. **Llama 4 Scout** if you need extreme context length (10M tokens!).

### ⚡ Small/Fast Utility (Sub-7B)

| Model | Params | Context | Use Case |
|-------|--------|---------|----------|
| **Qwen3-4B** | 4B | 128K | Classification, routing, parsing; thinking/non-thinking modes |
| **Qwen3-1.7B** | 1.7B | 32K | Ultra-fast routing, intent classification |
| **Qwen3-0.6B** | 0.6B | 32K | Bare minimum tasks; ~0.5GB VRAM |
| **Phi-4-mini (3.8B)** | 3.8B | 128K | Microsoft's small model; good reasoning for size |
| **Gemma 3 1B** | 1B | 32K | Google's tiny model |

**Winner:** **Qwen3-4B** at Q8 (~4GB VRAM) — best balance of capability and speed for routing/classification. **Qwen3-1.7B** if you need absolute minimum latency.

---

## 2. Concurrent Inference Strategy for 96GB VRAM

### VRAM Estimates (GGUF Quantized)

| Model | Quant | Model Size | +8K ctx | +32K ctx | +128K ctx |
|-------|-------|-----------|---------|----------|-----------|
| **Qwen3-235B-A22B** | Q4_K_M | ~68GB | ~70GB | ~74GB | ~84GB |
| **Qwen3-32B** | Q6_K | ~26GB | ~28GB | ~32GB | ~42GB |
| **Qwen3-32B** | Q4_K_M | ~20GB | ~22GB | ~26GB | ~36GB |
| **GLM-4.7-Flash (30B-A3B)** | Q4_K_M | ~18GB | ~19GB | ~20GB | ~24GB |
| **GLM-4.7-Flash (30B-A3B)** | Q6_K | ~24GB | ~25GB | ~27GB | ~31GB |
| **GPT-OSS-120B** | Q4_K_M | ~65GB | ~67GB | ~71GB | ~81GB |
| **GPT-OSS-20B** | Q6_K | ~17GB | ~19GB | ~23GB | ~33GB |
| **Devstral 2 24B** | Q6_K | ~20GB | ~22GB | ~26GB | ~36GB |
| **Qwen3-14B** | Q6_K | ~12GB | ~14GB | ~18GB | ~28GB |
| **Qwen3-4B** | Q8_0 | ~4GB | ~5GB | ~6GB | ~8GB |
| **Llama 4 Scout (109B)** | Q4_K_M | ~60GB | ~62GB | ~66GB | ~76GB |
| **Qwen3-embedding** | - | ~1GB | - | - | - |

### Recommended Multi-Model Combos (Fitting in 96GB)

#### 🏆 Combo A: "The Powerhouse" (Maximum reasoning)
```
Qwen3-235B-A22B Q4_K_M    ~70GB  (reasoning/planning primary)
Qwen3-4B Q8_0              ~4GB   (router/classifier)
Qwen3-embedding            ~1GB   (embeddings)
                           ═══════
Total:                     ~75GB  (21GB headroom for KV cache)
```
*Best when: Complex agentic tasks need maximum intelligence. Single-model focus.*

#### 🏆 Combo B: "The Multi-Agent Stack" (Best overall)
```
GLM-4.7-Flash Q6_K         ~25GB  (primary agentic/tool-calling)
Qwen3-32B Q4_K_M           ~20GB  (reasoning/complex tasks)
Devstral 2 24B Q4_K_M      ~16GB  (coding specialist)
Qwen3-4B Q8_0              ~4GB   (router/classifier)
Qwen3-embedding            ~1GB   (embeddings)
                           ═══════
Total:                     ~66GB  (30GB headroom)
```
*Best when: Running multiple concurrent agents with different specializations.*

#### 🏆 Combo C: "The Speed Demon" (Maximum throughput)
```
GLM-4.7-Flash Q6_K         ~25GB  (primary everything model)
GPT-OSS-20B Q6_K           ~17GB  (secondary/verification)
Qwen3-14B Q6_K             ~12GB  (tertiary/tool-calling)
Qwen3-4B Q8_0              ~4GB   (router)
Qwen3-embedding            ~1GB   (embeddings)
                           ═══════
Total:                     ~59GB  (37GB headroom for parallel requests)
```
*Best when: High-concurrency, many parallel agents.*

#### 🏆 Combo D: "The Context Monster"
```
Llama 4 Scout Q4_K_M       ~60GB  (10M context for massive docs)
Qwen3-4B Q8_0              ~4GB   (router)
Qwen3-embedding            ~1GB   (embeddings)
                           ═══════
Total:                     ~65GB  (31GB headroom for KV cache — you'll need it)
```
*Best when: Processing enormous documents, codebases, or research corpora.*

### Multi-Model Inference Infrastructure

**llama.cpp:**
- Run multiple `llama-server` instances on different ports, each loading a different model
- Each instance claims its own VRAM allocation at startup
- No dynamic sharing — you pre-allocate VRAM per model
- Use `--n-gpu-layers` to control how much goes to GPU vs CPU offload
- **CES 2026 NVIDIA announcements** included llama.cpp + Ollama acceleration for RTX GPUs

**Ollama:**
- Model switching has **cold-start overhead** (~2-5 seconds for loading/unloading)
- Ollama keeps the last-used model in VRAM; loading a second evicts the first (by default)
- `OLLAMA_NUM_PARALLEL` controls concurrent request slots per model
- For true multi-model concurrency, run **separate Ollama instances on different ports** (which you're already doing: 11434, 11435)
- Or use `OLLAMA_MAX_LOADED_MODELS` to keep multiple models resident

**Recommended architecture:**
```
Port 11434: Ollama — Qwen3-embedding (always resident, ~1GB)
Port 11435: Ollama — GLM-4.7-Flash (primary agent, always resident)
Port 11436: llama.cpp — Qwen3-32B Q4_K_M (reasoning, always resident)
Port 11437: llama.cpp — Qwen3-4B Q8_0 (router, always resident)
Port 11438: llama.cpp — Devstral 2 24B Q4_K_M (on-demand coding)
```

---

## 3. Quantization Recommendations

### General Rules for 96GB VRAM

You have the luxury of VRAM. **Use higher quants than most people can.**

| Model Size Class | Recommended Quant | Rationale |
|-----------------|-------------------|-----------|
| **Sub-7B** | **Q8_0 or FP16** | Tiny models — no reason to quantize aggressively. Q8 is nearly lossless. |
| **14B** | **Q6_K** | Fits easily; Q6_K preserves quality well. Only drop to Q4_K_M if running 3+ models concurrently. |
| **24-32B (dense)** | **Q5_K_M or Q6_K** | Sweet spot. Q6_K at 32B ≈ 26GB — very comfortable. Q5_K_M saves ~4GB with minimal quality loss. |
| **30B MoE (3B active)** | **Q6_K** | MoE models store all expert weights but only activate a fraction. Higher quant on the stored weights matters. ~24GB. |
| **70-120B** | **Q4_K_M** | This is where budget starts mattering. Q4_K_M is the best quality-per-byte at this scale. |
| **235B MoE (22B active)** | **Q4_K_M** | Only option that fits in 96GB. ~68-70GB base. |

### Quant Quality Comparison

| Quantization | Bits/Weight | Quality Loss vs FP16 | When to Use |
|-------------|-------------|----------------------|-------------|
| **Q8_0** | 8.0 | ~0.1% | Sub-14B models where you have the room |
| **Q6_K** | 6.6 | ~0.5% | Default choice for 14-32B models |
| **Q5_K_M** | 5.5 | ~1.0% | Good balance when juggling multiple models |
| **Q4_K_M** | 4.8 | ~2-3% | Large models (70B+); best quality at 4-bit |
| **Q4_K_S** | 4.5 | ~3-4% | Squeeze play; only if Q4_K_M doesn't fit |
| **IQ4_XS** | 4.3 | ~4-5% | Ultra-compressed; some users report Qwen MoE models do well here |

### Special Notes
- **MoE models benefit more from higher quants** because only a subset of experts fire per token — quantization errors in the wrong expert have outsized impact
- **GLM-4.7-Flash** users on r/LocalLLaMA report Q6_K is noticeably better than Q4_K for coding tasks
- **Unsloth quantizations** (UD-Q6_K_XL variants) are specifically optimized and often outperform standard GGUF quants — use them when available

---

## 4. Specific Model Recommendations (Final Picks)

### Tier 1: Always Loaded (Primary Stack)

| Role | Model | Quant | VRAM | Context | Speed |
|------|-------|-------|------|---------|-------|
| **Primary Agent** | GLM-4.7-Flash | Q6_K (Unsloth UD) | ~25GB | 48K default, 200K max | ~130-150 t/s on 5090-class GPU |
| **Reasoning** | Qwen3-32B | Q5_K_M | ~23GB | 32K default | ~30-40 t/s |
| **Router** | Qwen3-4B | Q8_0 | ~4GB | 8K | ~200+ t/s |
| **Embeddings** | Qwen3-embedding | native | ~1GB | 8K | fast |
| | | **Total:** | **~53GB** | | |

### Tier 2: On-Demand (Load When Needed)

| Role | Model | Quant | VRAM | When to Load |
|------|-------|-------|------|-------------|
| **Heavy Reasoning** | Qwen3-235B-A22B | Q4_K_M | ~70GB | Complex planning; swap out Tier 1 reasoning |
| **Coding Specialist** | Devstral 2 24B | Q5_K_M | ~18GB | Dedicated coding sessions |
| **Mega Context** | Llama 4 Scout | Q4_K_M | ~60GB | Processing massive documents |
| **Verification** | GPT-OSS-20B | Q6_K | ~17GB | Second opinion / cross-validation |

### Model Comparison: Tool-Calling & Agentic Capabilities

| Model | Tool-Call Reliability | Structured Output | Multi-Step Chains | Context Mgmt | Overall Agentic Score |
|-------|----------------------|-------------------|-------------------|-------------|----------------------|
| **GLM-4.7-Flash** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (200K) | **9.5/10** |
| **Qwen3-32B** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ (128K) | **8.5/10** |
| **Qwen3-14B** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ (128K) | **8/10** |
| **GPT-OSS-120B** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ (128K) | **7/10** (had "harmony" template issues) |
| **GPT-OSS-20B** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ (32K) | **6.5/10** |
| **Devstral 2 24B** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ (128K) | **7/10** (coding-focused) |
| **Llama 4 Scout** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (10M) | **7/10** (context king) |

---

## 5. Cost-Routing Strategy

### Decision Framework

```
┌─────────────────────────────────────────────────┐
│              INCOMING TASK                        │
│                                                   │
│  Qwen3-4B Router classifies:                     │
│  - complexity (1-5)                               │
│  - tool_calls_needed (bool)                       │
│  - context_length (tokens)                        │
│  - latency_tolerance (low/medium/high)            │
│  - task_type (reason/code/agent/summarize/simple) │
└───────────────────┬─────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   SIMPLE/FAST   STANDARD    COMPLEX
   (local fast)  (local big) (cloud)
```

### Routing Rules

| Condition | Route To | Cost |
|-----------|----------|------|
| **Simple classification, parsing, routing** | Qwen3-4B local | $0 |
| **Standard tool-calling, agentic work** | GLM-4.7-Flash local | $0 |
| **Coding tasks (standard)** | GLM-4.7-Flash or Devstral 2 local | $0 |
| **Complex reasoning, planning** | Qwen3-32B local | $0 |
| **Ultra-complex reasoning** | Qwen3-235B-A22B local (swap in) | $0 |
| **Massive document processing** | Llama 4 Scout local OR GLM-4.7-Flash 200K | $0 |
| **Mission-critical coding (production deploys)** | **Claude Opus 4.5** | ~$15/MTok in, $75/MTok out |
| **Novel/creative problem solving** | **Claude Opus 4.5** | expensive but worth it |
| **Tasks where local models fail/loop** | **Claude Sonnet 4.5** | ~$3/$15 per MTok |
| **Bulk code generation with verification** | Local first → Claude for review | hybrid |
| **Real-time pair programming** | **Claude Opus 4.5 / Codex** | latency-sensitive, quality matters |

### When to Use Cloud (Claude/OpenAI) vs Local

**Use Local When:**
- Task is well-defined and repeatable (tool calling, structured output)
- Latency tolerance > 2 seconds
- Context fits in model's window
- Task doesn't require cutting-edge reasoning
- You're running many parallel agents (cost adds up fast on cloud)
- Privacy/data sensitivity concerns
- **≈ 80-90% of agentic tasks should run locally on your hardware**

**Use Claude Opus 4.5 When:**
- Novel problem requiring deep reasoning + world knowledge
- Complex multi-file code refactoring where getting it wrong is expensive
- Tasks where local models hallucinate or get stuck in loops
- Creative writing, nuanced communication
- First-time architecture decisions
- **≈ 5-10% of tasks**

**Use Claude Sonnet 4.5 / GPT-4.1 When:**
- Middle ground: too complex for local, doesn't need Opus
- Verification/review of local model outputs
- Moderate coding tasks with tight timelines
- **≈ 5-10% of tasks**

### ROI Maximization

**Your cost structure:**
- Local inference: ~$0.15/hr electricity (GPU at load) = **~$0.0003/1K tokens**
- Claude Opus 4.5: $15/$75 per MTok = **~$0.015-0.075/1K tokens** (50-250× more expensive)
- Claude Sonnet 4.5: $3/$15 per MTok = **~$0.003-0.015/1K tokens** (10-50× more expensive)

**Strategy:**
1. **Default everything to local** — GLM-4.7-Flash handles 80%+ of agent tasks
2. **Escalate on failure** — if local model fails after 2 attempts, route to cloud
3. **Use local for drafting, cloud for review** — generate with GLM/Qwen, verify with Claude
4. **Batch cloud calls** — accumulate non-urgent tasks, send in batches to minimize API overhead
5. **Track cost per task** — log which tasks go to cloud, optimize local models to handle more over time

---

## 6. Immediate Action Items

### What to Download Now

```bash
# Primary agentic model (you already have this!)
# GLM-4.7-Flash — keep running it

# Reasoning model
ollama pull qwen3:32b-q5_k_m

# Router model
ollama pull qwen3:4b-q8_0

# Coding specialist (grab GGUF from HuggingFace)
# Devstral-2-24B-Q5_K_M.gguf from bartowski or unsloth

# Optional: heavy reasoning (grab when needed)
# Qwen3-235B-A22B-Q4_K_M.gguf (~70GB download)
```

### Watch List (Coming Soon)
- **DeepSeek V4** — Expected mid-February 2026. If open-weight and MoE like V3, could be the new king. Reportedly beats Claude Opus and GPT-5.2 at coding.
- **Kimi K2.5 quantized** — If someone produces good GGUF quants of the 32B-active MoE, it could fit in 96GB and is benchmarking incredibly well (AIME 96.1%).
- **Llama 4 Behemoth** — Meta's unreleased largest model. No timeline yet.
- **Nemotron 3 Super/Ultra** — NVIDIA's own models, H1 2026. Optimized for their GPUs.

---

*Last updated: February 2, 2026*
*Hardware: RTX Pro 6000 Blackwell 96GB | Threadripper Pro 32c/64t | 256GB RAM*
