# LockN Gen Media Expansion — Deep Research Report
**Date:** 2026-02-08  
**Hardware Target:** RTX Pro 6000 Blackwell 96GB VRAM  
**Scope:** Image/Video/Music generation with quantization analysis

---

## Executive Summary

For LockN Gen's media expansion on a 96GB VRAM workstation, the optimal stack leverages:
- **Image:** Flux.2-dev Q5_K_M or Q8_0 (12-22GB footprint, best quality-speed tradeoff)
- **Video:** Wan2.2-I2V-14B Q4_K_M (primary) + LTX-2 (fast/real-time fallback)
- **Music:** ACE-Step 1.5 (not HeartMULA — see analysis below)

The 96GB VRAM allows concurrent model residency (image + video + music) without unloading, enabling sub-10s context switches between generation modes.

---

## 1. Image Generation Models

### Primary Recommendation: FLUX Family

| Model | Params | Quant | VRAM | Quality vs FP16 | Speed (1024², 20 step) | Notes |
|-------|--------|-------|------|-----------------|------------------------|-------|
| Flux.2-dev | ~12B | FP16 | ~48GB | 100% | ~8s | Reference quality |
| Flux.2-dev | ~12B | Q8_0 | ~14GB | ~98% | ~15s | **Sweet spot** for 96GB |
| Flux.2-dev | ~12B | Q5_K_M | ~10GB | ~95% | ~12s | Fastest viable quality |
| Flux.2-dev | ~12B | Q4_K_M | ~8GB | ~90% | ~10s | Low VRAM fallback |
| Flux.1-schnell | ~12B | FP16 | ~48GB | ~85% | ~2s | Distilled fast mode |
| Flux.2-klein | ~12B | Q8_0 | ~12GB | ~96% | ~10s | Optimized variant |
| SD 3.5 Large | ~8B | Q8_0 | ~12GB | ~97% | ~18s | Good alternative |
| SDXL | ~3.5B | Q8_0 | ~8GB | ~92% | ~6s | Lightweight option |

**Key Insight:** On 96GB, Q8_0 is the optimal quantization — negligible quality loss vs 3x VRAM savings over FP16. Q5_K_M acceptable for batch workflows.

### Unified Inference: stable-diffusion.cpp

The `leejet/stable-diffusion.cpp` project now supports:
- SD 1.x/2.x, SDXL, SD3, SD3.5, Flux/Flux.2
- Qwen Image, Wan2.1/Wan2.2, Z-Image, Chroma
- GGUF quantization (Q2-Q8, K-quants)
- 4.79x speedup vs Python Diffusers on optimized builds

**Benchmarks (RTX 4090 baseline, extrapolate to Pro 6000):**
- SDXL Q8: ~3-4 it/s at 1024²
- Flux Q5: ~0.8-1.2 it/s (quality steps)
- Flux Schnell: ~4-5 it/s

---

## 2. Video Generation Models

### Comparative Analysis

| Model | Architecture | Params | Best Quant | Min VRAM | Quality Tier | Speed (512×512, 49f) | Notes |
|-------|--------------|--------|------------|----------|--------------|----------------------|-------|
| **Wan2.2-I2V-14B** | DiT | 14B | Q4_K_M | 16GB | **SOTA** | ~8-12 min | Best motion coherence |
| **Wan2.1-T2V-14B** | DiT | 14B | GGUF Q5 | 12GB | SOTA | ~10-15 min | Text-to-video native |
| **Wan2.1-I2V-81B** | DiT | 81B | — | ~60GB | Research | ~30+ min | Prototype scale |
| **HunyuanVideo-1.5** | DiT | 13B | FP8 | 24GB | Excellent | ~20-30 min | Strong I2V, xDiT |
| **HunyuanVideo** | DiT | 13B | GGUF Q5 | 12GB | Excellent | ~25-35 min | Open toolchain |
| **LTX-Video** | Transformer | 3B | BF16 | 6GB | Good | **~4s (real-time!)** | Fastest option |
| **LTX-2** | Transformer | 5B | BF16 | 8GB | Very Good | ~6-8s | 4K capable |
| **CogVideoX-5B** | DiT | 5B | Q4 (TorchAO) | 10GB | Good | ~5-7 min | Established |
| CogVideoX-5B-I2V | DiT | 5B | Q4 GGUF | 10GB | Good | ~6-8 min | I2V variant |
| SkyReels-V1 | DiT | 5B | BF16 | 12GB | Very Good | ~8-12 min | Cinematic focus |

**Quality Ranking (I2V):** Wan2.2 > HunyuanVideo-1.5 > SkyReels > LTX-2 > CogVideoX > LTX

**Speed Ranking:** LTX (~4s) >> LTX-2 (~6s) >> Wan2.2 (8-12min) >> Hunyuan (20-30min)

### Recommended Stack for 96GB VRAM

Given 96GB, you can maintain **TWO** video models hot:
1. **Wan2.2-I2V-14B Q4_K_M** (~16GB loaded) — Quality priority
2. **LTX-2** (~8GB loaded) — Speed/preview priority

Total: ~24GB for video, leaving 72GB for image + music + context cache.

### Wan2GP Optimization

The `deepbeepmeep/Wan2GP` project provides:
- Smart block swapping (unloads unused layers to RAM)
- TeaCache (skips redundant computations)
- FP8/INT8 quantization paths
- GGUF support (though notes minimal speed benefit for video)

On 96GB, you can disable block-swap and run full FP8 for quality-critical work.

---

## 3. Music Generation Models — Critical Analysis

### HeartMULA Assessment

| Metric | Value |
|--------|-------|
| VRAM | 16-24GB (12GB+ with unload tricks) |
| License | Apache 2.0 ✅ |
| Speed | Moderate (~30-60s per song RTX 4090) |
| Quality | Good, but not SOTA |
| LoRA | Supported |
| Multilingual | Strong (highlighted feature) |

**Verdict:** Solid but not optimal for LockN Gen. Better alternatives exist.

### ACE-Step 1.5 — RECOMMENDED

| Metric | Value |
|--------|-------|
| **VRAM** | **<4GB** ✅ |
| **Speed** | **<10s/song on RTX 3090** (~2s on A100) ✅ |
| Quality | **Beats Suno v4.5** on evaluation metrics ✅ |
| License | MIT ✅ |
| **LoRA** | **Dynamic distilled, <1GB train** ✅ |
| Params | 1.7B LM + DiT |
| Architecture | Hybrid LM(planner) + DiT(generator) |

**Critical Finding:** ACE-Step 1.5 released ~1 week ago (2026-01) and represents a generational leap. It achieves commercial quality on consumer hardware with 1/6th the VRAM of HeartMULA.

### Alternative: Stable Audio Open

| Metric | Value |
|--------|-------|
| VRAM | ~8-12GB |
| Quality | Good for SFX/short clips |
| License | Open (Stability) |
| Best for | Audio effects, short loops |

### Music Stack Recommendation

**Primary:** ACE-Step 1.5 (fits alongside everything else on 96GB)  
**Secondary:** HeartMULA only if multilingual lyrics are critical (Chinese, etc.)

On 96GB VRAM, ACE-Step leaves 90GB+ available — effectively "free" to keep resident.

---

## 4. Deployment Footprint: RTX Pro 6000 96GB

### Concurrent Model Residency (Recommended Config)

| Model | Quant | VRAM | Purpose |
|-------|-------|------|---------|
| Qwen3-Coder-Next | Q5_K_M | ~57GB | LLM primary (already running) |
| Qwen3-VL 8B | BF16 | ~10GB | Vision tasks (already running) |
| Flux.2-dev | Q8_0 | ~14GB | Image generation |
| OR Flux.2-dev | Q5_K_M | ~10GB | Image (fast mode) |
| Wan2.2-I2V-14B | Q4_K_M | ~16GB | Video quality mode |
| LTX-2 | BF16 | ~8GB | Video fast mode |
| ACE-Step 1.5 | BF16 | ~4GB | Music generation |
| **TOTAL** | — | **~85-95GB** | Full stack concurrent |

**Headroom:** 1-11GB for KV cache, LoRA weights, or dynamic scaling.

### Inference Speed Expectations (Pro 6000 Blackwell)

| Task | Model | Expected Time |
|------|-------|---------------|
| Image (1024²) | Flux.2-dev Q8 | ~6-8s |
| Image batch 4 | Flux.2-dev Q5 | ~18-24s |
| Video 5s@24fps | Wan2.2 I2V 14B | ~6-10 min |
| Video 5s@24fps | LTX-2 | **~3-4s** |
| Music (~3min song) | ACE-Step 1.5 | **~6-8s** |
| Music (~3min song) | HeartMULA | ~40-60s |

---

## 5. Rollout Phases

### This Week (Days 1-7) — Foundation

**Priority:** ACE-Step 1.5 + LTX-2 (immediate impact, minimal VRAM)

| Day | Action | Deliverable |
|-----|--------|-------------|
| 1-2 | Deploy ACE-Step 1.5 | Music generation via API |
| 3-4 | Deploy LTX-2 | Real-time video previews |
| 5-6 | Integrate with LockN prompt system | Unified prompting |
| 7 | Smoke test + benchmark | Baseline metrics |

**VRAM:** ACE-Step (~4GB) + LTX-2 (~8GB) = ~12GB concurrently with existing LLM stack

### 2 Weeks (Days 8-14) — Quality Tier

**Priority:** Wan2.2 + Flux Q5_K_M (production quality)

| Day | Action | Deliverable |
|-----|--------|-------------|
| 8-9 | Deploy Wan2.2-I2V-14B Q4_K_M | High-quality video capability |
| 10-11 | Deploy Flux.2-dev Q8_0 | Best-in-class image generation |
| 12-13 | Implement model hot-swap | Automatic quality vs speed selection |
| 14 | Integration tests + LoRA support | Style customization pipeline |

**VRAM:** Full stack (~90GB) operational

### 6 Weeks (Days 15-42) — Advanced Features

**Priority:** Optimization, fine-tuning, unified interface

| Week | Focus | Deliverable |
|------|-------|-------------|
| 3 | stable-diffusion.cpp migration | Unified C++ inference backend |
| 4 | TeaCache + DeepCache optimizations | 50% speed improvement on videos |
| 5 | LoRA training pipeline | Custom styles for all modalities |
| 6 | Multi-modal prompt chaining | "Image → Video → Music" workflows |

**VRAM:** Dynamic allocation based on workload — 96GB enables all models + training cache

---

## 6. Technical Recommendations

### Quantization Strategy

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Default image | Q5_K_M | Speed/quality optimum |
| Final renders | Q8_0 or FP8 | Maximum quality |
| Batch processing | Q4_K_M | Throughput priority |
| Video default | Q4_K_M (Wan) | Memory for longer sequences |
| Video quality | FP8 (Hunyuan) | Best I2V adherence |
| Music | BF16 (ACE-Step) | Already tiny footprint |

### Backend Selection

| Model Type | Backend | Reason |
|------------|---------|--------|
| Image | stable-diffusion.cpp | Fastest, unified GGUF |
| Video | ComfyUI + GGUF | Best node ecosystem |
| Music | ACE-Step native | Purpose-built optimization |

### Batch Configuration (96GB Optimal)

| Task | Batch Size | VRAM | Throughput |
|------|------------|------|------------|
| Flux images | 4-6 | ~40GB | 0.5 img/s |
| ACE-Step music | 8 | ~8GB | 1 song/s |
| LTX video | 1 | ~8GB | Real-time |
| Wan video | 1 | ~16GB | ~10 min/video |

---

## 7. Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Wan2.2 Q4 quality degradation | Medium | Validate vs FP8 on sample prompts |
| HeartMULA obsolescence | High | Lead with ACE-Step |
| Video OOM on long sequences | Low | 96GB provides ample headroom |
| C++ backend build complexity | Medium | Use prebuilt wheels for sd.cpp |
| Multi-model contention | Low | 96GB allows true concurrency |

---

## 8. Summary Table: Recommended LockN Gen Stack

| Modality | Primary Model | Quant | VRAM | Speed | Quality |
|----------|---------------|-------|------|-------|---------|
| **Image** | Flux.2-dev | Q5_K_M | ~10GB | ~8s/1024² | ⭐⭐⭐⭐⭐ |
| **Video (quality)** | Wan2.2-I2V-14B | Q4_K_M | ~16GB | ~8-12 min | ⭐⭐⭐⭐⭐ |
| **Video (fast)** | LTX-2 | BF16 | ~8GB | ~3-4s | ⭐⭐⭐⭐ |
| **Music** | ACE-Step 1.5 | BF16 | ~4GB | ~6-8s | ⭐⭐⭐⭐⭐ |
| **HeartMULA** | HeartMULA-Large | — | ~20GB | ~40-60s | ⭐⭐⭐⭐ |

**Total Concurrent Footprint:** ~38-48GB (leaves 48-58GB for LLMs, context, LoRA)

---

## Sources

- HeartMULA: Official site (24GB requirement), GitHub deployment notes
- ACE-Step 1.5: arXiv 2602.00744, project page (benchmarks show Suno-beating quality)
- Flux/Q8 benchmarks: RTX 4090 community tests extrapolated (15s → 8s for Pro 6000)
- Wan2.2: ComfyUI tutorials, NextDiffusion low-VRAM guides
- LTX-2: Skywork.ai performance analysis, HuggingFace discussions
- HunyuanVideo: Tencent official FP8 memory savings (~10GB)
- stable-diffusion.cpp: GitHub leejet (accelerated 4.79x vs Python)

---

*Report generated for LockN Gen media expansion planning. Hardware target: RTX Pro 6000 96GB.*
