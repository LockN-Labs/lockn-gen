# LOC-109: Model Research — ML Runtime Candidates

**Date:** 2026-02-04  
**Hardware:** RTX Pro 6000 Blackwell (96GB VRAM)

---

## 1. Vision-Language Models (Qwen VL)

**Use cases:** Screenshot analysis, QA automation, UI understanding, OCR, document processing

### Recommended: Qwen2.5-VL-7B-Instruct

| Spec | Value |
|------|-------|
| Parameters | 7B |
| VRAM (FP16) | ~14GB |
| VRAM (Q4) | ~8GB |
| License | Apache 2.0 |
| Strengths | Fast inference, good OCR, UI screenshot analysis |

**Why this one:**
- Fits easily in 96GB VRAM alongside other models
- Specifically praised for OCR and document understanding
- Can run via Ollama or vLLM
- Good for QA screenshot verification

### Alternative: Qwen2.5-VL-32B-Instruct

| Spec | Value |
|------|-------|
| Parameters | 32B |
| VRAM (FP16) | ~65GB |
| VRAM (Q4) | ~20GB |
| License | Apache 2.0 |
| Strengths | Better reasoning, more accurate |

**When to use:** Complex multi-step visual reasoning, higher accuracy requirements

### NOT Recommended: Qwen3-VL (flagship MoE)

- Requires **8x 80GB GPUs** (640GB total)
- Way beyond our single-GPU setup

---

## 2. Voice Cloning / TTS

**Use cases:** LockN Voice, real-time chat, voice profiles

### Current: Qwen3-TTS ✅ (Already deployed)

| Spec | Value |
|------|-------|
| Parameters | 0.6B - 1.7B |
| Latency | **97ms** (streaming) |
| Languages | 10 (CN, EN, JP, KR, DE, FR, RU, PT, ES, IT) |
| License | Apache 2.0 |
| Status | **WORKING** (qwen3-tts-api container) |

**Verdict:** Keep using. It's working, fast, and high quality.

### Alternative: CosyVoice2-0.5B

| Spec | Value |
|------|-------|
| Parameters | 0.5B |
| Latency | Ultra-low (streaming) |
| Features | Emotional control, real-time |
| License | Apache 2.0 |

**When to consider:**
- If Qwen3-TTS doesn't meet emotional expression needs
- For real-time conversational agents needing more nuance

### Alternative: Kokoro (82M)

| Spec | Value |
|------|-------|
| Parameters | **82M** (tiny!) |
| Quality | Comparable to larger models |
| Speed | Extremely fast |
| Use case | Edge deployment, resource-constrained |

**When to consider:**
- Running on CPU
- Multiple concurrent TTS streams
- Embedded/edge scenarios

### Fish Speech v1.5 ❌ (On hold)

- **Status:** Unhealthy (sm_120 CUDA kernel issue)
- **Decision:** Deprioritized per Sean
- **Qwen3-TTS covers the gap**

---

## 3. Image Generation (LockN Gen)

**Use cases:** Marketing assets, thumbnails, concept art, UI mockups

### Recommended: FLUX.1 Dev or SDXL Lightning

| Model | VRAM | Speed | Quality | License |
|-------|------|-------|---------|---------|
| **FLUX.1 Dev** | ~12GB | Medium | Excellent | Apache 2.0 |
| **SDXL Lightning** | ~8GB | **Fast** | Very Good | Open |
| Juggernaut XL | ~8GB | Medium | Great for realism | Custom |
| SD 3.5 | ~12GB | Medium | Good | Stability AI |

**Recommendation:** Start with **FLUX.1 Dev** for quality, **SDXL Lightning** for speed.

**ComfyUI Integration:**
- All models work with ComfyUI
- Can be served via API for LockN Gen integration
- Requires PyTorch with sm_120 support (cu128 nightly)

---

## 4. Model Stack Summary

### Immediate (Already Working)
| Model | Use | Status |
|-------|-----|--------|
| Qwen3-TTS | Voice synthesis | ✅ Running |
| Qwen3-32B | Text generation | ✅ Running (llama.cpp) |
| Qwen3-Coder-Next | Coding | ✅ Running (llama.cpp) |

### Priority 1 (cu128 Required)
| Model | Use | VRAM | Notes |
|-------|-----|------|-------|
| **Qwen2.5-VL-7B** | Screenshot/QA | ~14GB | PyTorch cu128 needed |
| **FLUX.1 Dev** | Image gen | ~12GB | PyTorch cu128 needed |

### Priority 2 (If Needed)
| Model | Use | VRAM | Notes |
|-------|-----|------|-------|
| CosyVoice2-0.5B | Emotional TTS | ~4GB | If Qwen3-TTS insufficient |
| Qwen2.5-VL-32B | Better vision | ~65GB | If 7B insufficient |
| SDXL Lightning | Fast image gen | ~8GB | If FLUX too slow |

---

## 5. VRAM Budget (96GB)

**Current usage:**
- Qwen3-Coder-Next (Q5): ~57GB
- Qwen3-32B (Q5): ~23GB (separate service)
- Qwen3-TTS: ~4GB
- KV cache headroom: ~10GB

**Proposed addition:**
- Qwen2.5-VL-7B: ~14GB (on-demand load)
- FLUX.1 Dev: ~12GB (on-demand load)

**Strategy:** Load vision/image models on-demand, unload when idle. With 96GB, we have flexibility.

---

## 6. Next Steps

1. **Build cu128 base** (LOC-109 Phase 1-2)
2. **Add Qwen2.5-VL-7B** for QA screenshot testing
3. **Add FLUX.1 Dev** for LockN Gen
4. **Model matrix** tracks all enabled models
5. **Dynamic loading** via capability flags

---

## References

- [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)
- [Qwen3-TTS Technical Report](https://arxiv.org/html/2601.15621v1)
- [FLUX.1 Dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)
- [CosyVoice2](https://github.com/FunAudioLLM/CosyVoice)
- [Best Open Source Voice Cloning 2026](https://www.siliconflow.com/articles/en/best-open-source-models-for-voice-cloning)
