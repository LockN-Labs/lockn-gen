# LOC-109: LockN ML Runtime Layer Analysis

**Status:** In Progress  
**Date:** 2026-02-04  
**Author:** Claws (AI)

---

## 1. Current State Audit

### Infrastructure
| Component | Status | Notes |
|-----------|--------|-------|
| **GPU** | ✅ RTX Pro 6000 Blackwell (sm_120) | 96GB VRAM, CUDA 13.0, Driver 582.16 |
| **WSL2** | ✅ Working | Linux 6.6.87.2-microsoft-standard-WSL2 |
| **Docker** | ✅ Running | 18+ containers active |
| **Venvs** | ❌ None exist | No `~/venvs/` directory |
| **PyTorch (default)** | ❌ Not installed | Base WSL env has no torch |

### ML Containers
| Container | Image | Status | PyTorch | Issue |
|-----------|-------|--------|---------|-------|
| qwen3-tts-api | qwen3-tts-gpu | ✅ Healthy | 2.5.1+cu121 | Works (pure PyTorch ops) |
| lockn-fish-speech-test | fish-speech:local | ❌ Unhealthy | 2.x+cu124 | sm_120 missing, CUDA kernel fail |
| lockn-fish-speech-dev | fish-speech:local | ✅ Healthy | Same | (Different workload?) |

### Key Insight
**Qwen3-TTS works despite PyTorch lacking sm_120** because it uses pure PyTorch operations that have PTX JIT fallback.  
**Fish Speech fails** because it uses custom CUDA kernels compiled for specific architectures (sm_50-sm_90) that don't have sm_120 support.

---

## 2. PyTorch cu128 Nightly Availability

### Confirmed Available
```
Index: https://download.pytorch.org/whl/nightly/cu128/torch/
Latest: torch-2.10.0.dev20260204+cu128 (daily builds)
Python: 3.10, 3.11, 3.12, 3.13, 3.14
Platforms: linux_x86_64, linux_aarch64, win_amd64
```

### sm_120 Support Status
- ✅ **cu128 nightly builds include sm_120** (confirmed by web research)
- ⚠️ Stable PyTorch releases do NOT yet support sm_120
- ⚠️ Nightly builds are pre-release; may have bugs

---

## 3. Decision Recommendations

### Decision A: Container-first vs Venv-first?

**Recommendation: Container-first (Option A)**

| Criteria | Container-first | Venv-first |
|----------|-----------------|------------|
| Drift prevention | ✅ Excellent | ⚠️ Moderate |
| GPU passthrough (WSL2) | ✅ Works with --gpus all | ✅ Native |
| Build reproducibility | ✅ Lockfile + image hash | ⚠️ Lockfile only |
| Dev iteration speed | ⚠️ Slower rebuilds | ✅ Faster |
| OpenClaw integration | ✅ Cleaner capability gating | ⚠️ More complex |

**Rationale:**
- We already run 18+ containers; ops team knows Docker
- Container images are atomic units for promotion
- Venvs can coexist for quick local dev, but containers are source of truth

**Hybrid approach:** Use venvs for rapid prototyping, containers for CI/promotion gates.

---

### Decision B: Matrix scope v1?

**Recommendation: Qwen3-TTS only (minimal scope)**

| Option | Scope | Risk | Effort |
|--------|-------|------|--------|
| **B1: TTS only** | Qwen3-TTS | Low | 1-2 days |
| B2: TTS + Whisper | Add ASR | Medium | 3-4 days |
| B3: TTS + Whisper + Vision | Full stack | High | 1+ week |

**Rationale:**
- Fish Speech is currently broken; fix that first
- Qwen3-TTS works; it's our canary
- Adding Whisper/vision before base is stable = more breakage vectors
- **Ship small, validate, expand**

---

### Decision C: Promotion gate strictness?

**Recommendation: Smoke + 1-second inference test (Option C)**

| Gate | What it catches | Time | Reliability |
|------|-----------------|------|-------------|
| Smoke only | Import failures, missing deps | ~5s | High |
| **Smoke + inference** | Runtime CUDA issues, model load failures | ~30s | Higher |
| Smoke + full test suite | Everything | ~5min | Highest but slow |

**Rationale:**
- Smoke-only missed the Fish Speech sm_120 issue (imports passed, runtime failed)
- A 1-second audio generation proves the full path works
- Keep it fast enough to run on every promotion

**Proposed test:**
```python
# Generate 1 second of "test" audio
response = tts_client.synthesize("test", max_duration=1.0)
assert len(response.audio) > 0
```

---

## 4. Migration Plan

### Phase 1: Foundation (2-3 days)
1. Create `~/venvs/` directory structure
2. Install PyTorch cu128 nightly in `lockn-ai-dev-cu128`
3. Run smoke test, verify sm_120 in arch list
4. Generate initial lockfiles

### Phase 2: Base Container (2-3 days)
1. Create `lockn-ai-base` Dockerfile with cu128 PyTorch
2. Add `lockn-smoke-ml-stack` script
3. Build and test with `--gpus all`
4. Verify sm_120 inside container

### Phase 3: Fix Fish Speech (1-2 days)
1. Rebuild Fish Speech FROM lockn-ai-base
2. Test that sm_120 kernel issue is resolved
3. Promote to test environment

### Phase 4: Model Matrix (1 day)
1. Create minimal `model-matrix.yaml` with qwen3_tts
2. Extend smoke script to read matrix
3. Add inference gate for enabled models

### Phase 5: OpenClaw Integration (2-3 days)
1. Add capability.ml_stack config
2. Run smoke at startup
3. Emit OTEL receipts on smoke runs
4. Disable model tools if smoke fails

---

## 5. Effort Estimate

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| Phase 1: Foundation | 2-3 days | None |
| Phase 2: Base Container | 2-3 days | Phase 1 |
| Phase 3: Fish Speech | 1-2 days | Phase 2 |
| Phase 4: Model Matrix | 1 day | Phase 2 |
| Phase 5: OpenClaw | 2-3 days | Phase 2 |

**Total: 8-12 days** (can parallelize Phases 3-5 after Phase 2)

---

## 6. Immediate Next Steps

1. **Get your decisions on A/B/C** (this doc)
2. **Create `~/venvs/lockn-ai-dev-cu128`** and install PyTorch nightly
3. **Verify sm_120 appears in arch list**
4. **If yes:** Proceed with base container build
5. **If no:** Research alternative (custom wheels, build from source)

---

## Appendix: Relevant Files

- **Handoff Pack:** Slack message 1770214552.992599
- **Fish Speech Dockerfile:** `~/.openclaw/workspace/lockn-voice/docker/fish-speech/Dockerfile`
- **Existing infra:** `~/.openclaw/workspace/lockn-infra/`
- **This analysis:** `~/.openclaw/workspace/docs/LOC-109-ml-runtime-analysis.md`
