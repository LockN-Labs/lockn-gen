# LockN Bod — Talking Head Avatar Research Spike

**Date:** 2026-02-07  
**Status:** Complete  
**Purpose:** Evaluate real-time talking head / avatar generation for the LockN agent stack

---

## Executive Summary

The talking head generation space has matured significantly. For LockN Bod, the recommended approach is a **hybrid architecture**: use **MuseTalk** (lightweight, real-time lip sync) for immediate results, combined with **LivePortrait** (expression/pose control) for emotion-driven animation, delivered via **TalkingHead 3D** (browser-based Three.js avatar) for the web UI. This stack fits within the ~50GB VRAM budget remaining alongside existing LockN services, and delivers sub-500ms end-to-end latency.

---

## 1. Competitive Landscape

### Cloud Services

| Service | Pricing | Key Features | Latency | Limitations |
|---------|---------|-------------|---------|-------------|
| **HeyGen** | $24-144+/mo (API from $99/mo) | 200+ stock avatars, custom avatar cloning, LiveAvatar for real-time, 175+ languages | ~2-5s for video gen, <1s for LiveAvatar | Cloud-only, per-credit billing, no local option |
| **Synthesia** | $29-99+/mo | 240+ avatars, enterprise focus, SCORM support, personal avatar studio | ~3-10s per clip | Expensive at scale, no real-time streaming |
| **D-ID** | $6-108+/mo | API-first, streaming avatar API, photo-to-video | <1s streaming mode | Lower quality than HeyGen/Synthesia |
| **Tavus** | Custom pricing | Conversational Video Interface (CVI), real-time persona replication | Sub-second | Enterprise-only pricing |
| **Colossyan** | $27-100+/mo | Multilingual, emotion controls, screen recording integration | 3-10s | Limited API access |
| **Hour One** | Custom | Enterprise virtual presenters, brand customization | 3-10s | Enterprise-only |

**Cloud pricing reality:** For always-on agent avatars, cloud costs escalate rapidly. At even modest usage (1hr/day of avatar interaction), HeyGen API costs ~$200-500/mo. Local inference pays for itself almost immediately.

### Open-Source Models — Comparison Matrix

| Model | Approach | Real-Time? | VRAM | Emotion? | License | Quality | One-Shot? |
|-------|----------|-----------|------|----------|---------|---------|-----------|
| **MuseTalk** (Tencent) | Latent-space lip inpainting | ✅ 30+ fps (V100) | ~4-6 GB | ❌ Lip-only | Apache 2.0 | ⭐⭐⭐⭐ | ✅ |
| **LivePortrait** (Kuaishou) | Implicit keypoint reenactment | ⚠️ ~5-8 fps (3060 12GB) | ~4-8 GB | ✅ Expression retargeting | Apache 2.0 | ⭐⭐⭐⭐⭐ | ✅ |
| **Ditto** (Ant Group) | Motion-space diffusion + TensorRT | ✅ RTF <1, <400ms latency | ~6-10 GB | ✅ Controllable motion | Apache 2.0 | ⭐⭐⭐⭐⭐ | ✅ |
| **Hallo / Hallo2** (Fudan) | Diffusion-based audio-driven | ❌ Slow (~2-5 fps) | ~12-24 GB | ⚠️ Implicit | Apache 2.0 | ⭐⭐⭐⭐⭐ | ✅ |
| **EchoMimic** (Ant Group) | Audio + landmark conditioning | ❌ ~3-5 fps | ~10-16 GB | ✅ Landmark-editable | Apache 2.0 | ⭐⭐⭐⭐ | ✅ |
| **SadTalker** | 3DMM coefficient prediction | ⚠️ ~10-15 fps | ~6-8 GB | ✅ Expression params | MIT | ⭐⭐⭐ | ✅ |
| **Wav2Lip** | GAN lip sync | ✅ 25+ fps | ~2-4 GB | ❌ Lip-only | Custom academic | ⭐⭐⭐ | ✅ |
| **DreamTalk** | Diffusion + style tokens | ❌ Slow | ~8-12 GB | ✅ Style control | Apache 2.0 | ⭐⭐⭐⭐ | ✅ |
| **V-Express** | Progressive training | ❌ ~2-4 fps | ~10-16 GB | ✅ Expression control | Apache 2.0 | ⭐⭐⭐⭐ | ✅ |
| **GeneFace++** | NeRF-based 3D | ⚠️ ~15 fps with caching | ~8-12 GB | ⚠️ Limited | Custom | ⭐⭐⭐⭐ | ❌ (needs training) |
| **OmniTalker** (Alibaba) | Text-driven, style mimicking | ✅ Real-time | TBD | ✅ Style replication | TBD (NeurIPS 2025) | ⭐⭐⭐⭐⭐ | ✅ |
| **SyncTalk** | NeRF talking head | ❌ ~5 fps | ~10-16 GB | ⚠️ | Apache 2.0 | ⭐⭐⭐⭐ | ❌ |

### Notable Newcomers (Late 2025 / Early 2026)

- **Ditto** — Best-in-class for real-time. Uses TensorRT optimization, achieves RTF <1 (real-time factor). Full-body support. Training code released Nov 2025.
- **OmniTalker** — Text-driven (no separate TTS needed!). One-shot, real-time, with audio-visual style mimicking. NeurIPS 2025. Code available on GitHub.
- **LiveTalk-Unity** — Unity package combining LivePortrait + MuseTalk + SparkTTS. On-device, no cloud. Released July 2025.
- **Linly-Talker** — Full integration framework: LLM + ASR + TTS + Avatar (supports SadTalker, MuseTalk, Wav2Lip). Gradio WebUI.

---

## 2. Real-Time Capability Assessment

### Tier 1: Real-Time Ready (<100ms per frame, 25+ fps)

| Model | FPS | Latency | VRAM | Notes |
|-------|-----|---------|------|-------|
| **MuseTalk** | 30+ fps | ~33ms/frame | 4-6 GB | Lip-sync only, 256×256 face region |
| **Wav2Lip** | 25+ fps | ~40ms/frame | 2-4 GB | Lower quality but battle-tested |
| **Ditto** (TensorRT) | 25+ fps | <400ms e2e | 6-10 GB | Full pipeline including audio processing |
| **TalkingHead 3D** (JS) | 60 fps | <5ms/frame | 0 GPU | Browser-based 3D, viseme-driven |

### Tier 2: Near-Real-Time (10-25 fps, usable with buffering)

| Model | FPS | VRAM | Notes |
|-------|-----|------|-------|
| **SadTalker** | 10-15 fps | 6-8 GB | Full head motion + expression |
| **LivePortrait** | 5-15 fps | 4-8 GB | With TensorRT optimization can reach ~15 fps |
| **GeneFace++** | ~15 fps | 8-12 GB | Requires per-identity training |

### Tier 3: Offline Only (<10 fps)

Hallo2, EchoMimic, V-Express, DreamTalk — high quality but diffusion-based, too slow for real-time.

### VRAM Budget Analysis

Current LockN stack usage:
| Service | VRAM |
|---------|------|
| Qwen3-Coder-Next (port 11439) | ~57 GB |
| Qwen2.5-VL (port 11441) | ~12 GB |
| **Total existing** | **~69 GB** |
| **Available on 96 GB** | **~27 GB** |

**However:** Coder-Next is MoE — active VRAM usage is lower during inference pauses. Realistically ~45-50 GB actively used, leaving ~46-51 GB available.

Recommended avatar VRAM budget: **4-10 GB** — easily fits.

| Avatar Option | VRAM Needed | Fits? |
|---------------|-------------|-------|
| MuseTalk | 4-6 GB | ✅ Easily |
| MuseTalk + LivePortrait | 8-14 GB | ✅ Comfortable |
| Ditto (TensorRT) | 6-10 GB | ✅ Comfortable |
| TalkingHead 3D (browser) | 0 GPU | ✅ Zero GPU cost |

### Streaming Architecture

```
LockN Brain (LLM) → text + emotion tags
        ↓
LockN Speak (TTS) → audio chunks (streaming, 200ms chunks)
        ↓
LockN Bod (Avatar) → animated frames (streaming, 30fps)
        ↓
Web UI (WebSocket/WebRTC) → browser display
```

**Latency budget:**
| Stage | Latency |
|-------|---------|
| LLM first token | ~100-200ms |
| TTS first chunk | ~150-300ms |
| Avatar first frame | ~30-100ms |
| Network/display | ~10-50ms |
| **Total to first visible speech** | **~300-650ms** |

This is comparable to natural conversation turn-taking delay (~500-700ms).

---

## 3. Emotion & Gesture Support

### Emotion-Capable Models

| Model | Emotion Input | Method | Quality |
|-------|--------------|--------|---------|
| **LivePortrait** | Expression coefficients, retargeting | Stitching module maps source expressions to target | ⭐⭐⭐⭐⭐ |
| **EchoMimic** | Editable facial landmarks | Direct landmark control per frame | ⭐⭐⭐⭐ |
| **SadTalker** | 3DMM expression params | ExpNet predicts expression from audio | ⭐⭐⭐ |
| **DreamTalk** | Style tokens/embeddings | Diffusion-based style transfer | ⭐⭐⭐⭐ |
| **V-Express** | Reference expression video | Progressive training disentangles expression | ⭐⭐⭐⭐ |
| **Ditto** | Motion-space control | Full motion controllability | ⭐⭐⭐⭐⭐ |
| **TalkingHead 3D** | Morph targets (blendshapes) | Direct 3D face control (52 ARKit shapes) | ⭐⭐⭐⭐⭐ |

### Emotion Tag → Avatar Expression Mapping

LockN Speak emotion tags can map to avatar controls:

```python
EMOTION_MAP = {
    "neutral":   {"mouth_smile": 0.0, "brow_raise": 0.0, "eye_wide": 0.0},
    "happy":     {"mouth_smile": 0.8, "brow_raise": 0.2, "eye_wide": 0.1},
    "sad":       {"mouth_smile": -0.5, "brow_lower": 0.6, "eye_narrow": 0.3},
    "angry":     {"brow_lower": 0.8, "mouth_tension": 0.6, "eye_narrow": 0.4},
    "surprised": {"brow_raise": 0.9, "eye_wide": 0.8, "mouth_open": 0.6},
    "thinking":  {"brow_raise_left": 0.4, "eye_look_up": 0.3, "mouth_pucker": 0.2},
}
```

### Gesture Generation

- **DiffTED** — Diffusion-based co-speech gesture generation (upper body)
- **BEAT** — Body-Expression-Audio-Text dataset + baseline model for gesture synthesis
- **GestureDiffuCLIP** — Text/speech → gesture via diffusion
- **TalkSHOW** — Speech-driven holistic body + hand motion

For a 3D avatar approach, gestures are significantly easier — just trigger animation clips based on semantic content.

---

## 4. Customization & Identity

### Avatar Creation Methods

| Method | Input | Quality | Speed | Flexibility |
|--------|-------|---------|-------|-------------|
| **Single photo → reenactment** | 1 photo | ⭐⭐⭐⭐ | Instant | High (any photo) |
| **Ready Player Me** | Selfie → 3D model | ⭐⭐⭐ | ~30s | Full customization |
| **AI-generated face** | Text prompt (SD/FLUX) | ⭐⭐⭐⭐⭐ | ~5s | Infinite variety |
| **3D scan / photogrammetry** | Multi-photo capture | ⭐⭐⭐⭐⭐ | Minutes | Highest fidelity |
| **Custom 3D model** | Blender/Maya | ⭐⭐⭐⭐⭐ | Hours | Total control |

### Recommended Flow for LockN Bod

1. **Quick start:** User selects from AI-generated avatar gallery or uploads a single photo
2. **Photo-based:** LivePortrait/MuseTalk animate the photo directly — instant talking head
3. **3D avatar:** Ready Player Me GLB → TalkingHead 3D in browser — full body, gestures, customizable
4. **Advanced:** Custom 3D model with full blendshape rigging

### Style Options

- **Realistic:** Photo-based reenactment (LivePortrait, MuseTalk, Ditto)
- **Stylized/Cartoon:** Style transfer on source image, then animate; or use 3D cartoon avatar
- **Anime:** Use anime-style reference images with LivePortrait (works well)
- **Professional/Corporate:** Ready Player Me business avatars + TalkingHead 3D

---

## 5. Integration Architecture

### Option A: Neural Talking Head (Recommended for V1)

```
┌─────────────────────────────────────────────┐
│                  LockN Bod                   │
│                                              │
│  Audio In ──→ MuseTalk ──→ Lip-synced        │
│  (from TTS)    (GPU)       Face Frames       │
│                    │                         │
│  Emotion Tags ──→ Expression                 │
│  (from Brain)    Blending ──→ Final Frames   │
│                                    │         │
│                              MJPEG/WebRTC    │
│                              Stream Out      │
└─────────────────────────────────────────────┘
```

- **Input:** TTS audio stream + emotion tags
- **Processing:** MuseTalk for lip sync (4-6 GB VRAM, 30+ fps)
- **Expression overlay:** LivePortrait or post-processing for emotion blending
- **Output:** MJPEG stream or WebRTC video to browser
- **Latency:** ~30-100ms per frame

### Option B: 3D Browser Avatar (Recommended for richest experience)

```
┌─────────────────────────────────────────────┐
│              Browser (Client)                │
│                                              │
│  TalkingHead 3D (Three.js)                   │
│  ├── Audio ──→ Viseme extraction ──→ Lip sync│
│  ├── Emotion ──→ Blendshape morph targets    │
│  └── Gestures ──→ Animation clips            │
│                                              │
│  Renders at 60fps, zero GPU server cost      │
└─────────────────────────────────────────────┘
```

- **Input:** TTS audio (streamed to browser) + emotion/gesture JSON commands
- **Processing:** All in-browser via Three.js/WebGL
- **Avatar:** Ready Player Me GLB or custom 3D model
- **Output:** Native browser rendering at 60fps
- **Latency:** <5ms rendering (audio playback is the bottleneck)
- **VRAM cost:** Zero server-side GPU

### Option C: Hybrid (Recommended for V2+)

Combine both: 3D avatar for default interaction (zero GPU cost, instant, gestures), with neural rendering for "ultra-realistic" mode when a photo-real avatar is desired.

### Rendering & Delivery

| Method | Pros | Cons |
|--------|------|------|
| **WebRTC video stream** | Works with neural rendered frames, low latency | Requires server GPU, encoding overhead |
| **MJPEG over WebSocket** | Simple, works with any frame source | Higher bandwidth, no audio sync built-in |
| **Three.js in-browser** | Zero server GPU, 60fps, full interactivity | 3D-only (not photorealistic) |
| **WebGPU compute** | Future: run small models in-browser | Immature, limited model support |

---

## 6. Ethical & Legal Considerations

### Deepfake Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Impersonation of real people | Default to AI-generated or 3D avatars; require explicit consent for photo-based |
| Non-consensual face cloning | Consent framework: signed permission for face enrollment |
| Misuse for fraud/scams | Watermark generated frames (C2PA metadata); rate-limit face enrollment |
| Platform policy violations | Most platforms prohibit deceptive use of AI-generated faces |

### Best Practices for LockN Bod

1. **Consent-first:** If using a real person's face, require explicit opt-in with clear explanation
2. **Watermarking:** Embed invisible watermarks in neural-rendered frames (C2PA standard)
3. **Disclosure:** UI clearly labels avatar as "AI-generated" or "AI-animated"
4. **Default to synthetic:** Provide beautiful AI-generated or 3D avatars as default — no real faces needed
5. **Local processing:** All face data stays on-device — major privacy advantage over cloud services
6. **No face database:** Don't store enrolled faces beyond the active session unless user explicitly saves

### Legal Landscape (2025-2026)

- EU AI Act: Deepfakes must be disclosed; avatar systems likely "limited risk" category
- US: State-level laws (CA, TX, etc.) require consent for digital replicas
- Platform ToS: Major platforms require disclosure of AI-generated content

---

## 7. Market Opportunity

### Pricing Comparison: Cloud vs Local

| Service | Monthly Cost (moderate use) | Annual Cost |
|---------|---------------------------|-------------|
| HeyGen (Creator) | $24-29/mo | $288-348/yr |
| HeyGen (API) | $99-499/mo | $1,188-5,988/yr |
| Synthesia (Starter) | $29/mo | $348/yr |
| Synthesia (Enterprise) | $100+/mo | $1,200+/yr |
| D-ID (Pro) | $48/mo | $576/yr |
| **LockN Bod (local)** | **$0/mo** (after hardware) | **$0/yr** |

### The Gap

Cloud avatar services are:
- **Expensive** at scale (per-minute/per-credit billing)
- **Latency-bound** (round-trip to cloud adds 200-500ms)
- **Privacy-hostile** (face data uploaded to third-party servers)
- **Limited customization** (pre-built avatars, limited emotion control)
- **Not composable** (can't integrate deeply with local LLM/TTS)

LockN Bod fills the gap as:
- **Zero marginal cost** — runs on hardware you already own
- **Sub-second latency** — local pipeline, no network round-trip
- **Full privacy** — face data never leaves the machine
- **Deep integration** — native pipeline with LockN Brain + Speak
- **Full customization** — any avatar, any style, emotion-aware

### Target Customers

1. **AI agent developers** building conversational interfaces
2. **Content creators** wanting local, unlimited avatar generation
3. **Enterprise** needing on-prem avatar solutions (privacy/compliance)
4. **Education/training** platforms wanting personalized tutors
5. **Accessibility** — sign language avatars, assistive tech

---

## 8. Recommendations & Roadmap

### Phase 1: Quick Win (1-2 weeks) — "LockN Bod MVP"

**Goal:** Get a talking avatar working in the OpenClaw web UI.

**Approach:** **TalkingHead 3D** (browser-based)
- Zero GPU cost — runs entirely in-browser via Three.js
- Ready Player Me avatar customization
- Receives TTS audio from LockN Speak → viseme-based lip sync
- Emotion tags from LockN Brain → blendshape morphing
- Gesture triggers → animation clips
- npm package available: `talkinghead` v1.7.0

**Why this first:** Immediate visual impact, no GPU allocation needed, rich interactivity, full emotion/gesture support. Gets the integration architecture right before investing in neural rendering.

**Integration steps:**
1. Add TalkingHead 3D to OpenClaw web UI
2. Pipe LockN Speak TTS audio to browser
3. Map emotion tags to avatar expressions
4. Add gesture triggers based on content type

### Phase 2: Neural Enhancement (2-4 weeks) — "Photo-Real Mode"

**Goal:** Optional photorealistic avatar from a single photo.

**Approach:** **MuseTalk** for lip sync + **LivePortrait** for expressions
- MuseTalk: 4-6 GB VRAM, 30+ fps real-time lip sync
- LivePortrait: 4-8 GB VRAM, expression retargeting
- Combined: ~8-14 GB VRAM — fits easily alongside existing stack
- Server renders frames → streams to browser via WebRTC

**Integration steps:**
1. Deploy MuseTalk as a local service (systemd unit)
2. Audio chunk streaming: TTS → MuseTalk → frames
3. Add LivePortrait expression blending layer
4. WebRTC stream to browser as alternative to 3D avatar
5. User chooses: "3D Avatar" or "Photo-Real" mode

### Phase 3: Full Embodied Agent (1-3 months) — "The Vision"

**Goal:** Emotion-aware, gesture-rich, fully customizable avatar agent.

**Approach:** Best of all worlds
- **Ditto** for highest-quality real-time neural rendering (once TensorRT pipeline stabilizes)
- **OmniTalker** evaluation — text-driven, could bypass separate TTS for avatar
- Full emotion mapping pipeline: LLM → emotion analysis → avatar expression
- Gesture generation from speech/text content
- Multi-avatar support (switch personas)
- Avatar memory (consistent identity across sessions)

### Architecture Decision Matrix

| Criteria | TalkingHead 3D | MuseTalk | Ditto | OmniTalker |
|----------|---------------|----------|-------|------------|
| Time to integrate | 1-2 days | 3-5 days | 1-2 weeks | 2-4 weeks |
| GPU cost | 0 | 4-6 GB | 6-10 GB | TBD |
| Quality | Good (3D) | Great (2D) | Excellent (2D) | Excellent |
| Emotion support | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Real-time | ✅ 60fps | ✅ 30fps | ✅ 25fps | ✅ Real-time |
| Customization | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Gestures | ✅ Full body | ❌ Face only | ✅ Full body | TBD |

### 🏆 Top Recommendation

**Start with TalkingHead 3D for Phase 1.** It's the fastest path to a working avatar with the richest feature set (emotion, gestures, full body, customization) at zero GPU cost. Then layer in neural rendering (MuseTalk/Ditto) as a "photo-real upgrade" in Phase 2.

This mirrors how companies like HeyGen evolved — 3D avatars first, then photorealistic ones — but you'll have both running locally.

### Key Projects to Watch

| Project | Why | Status |
|---------|-----|--------|
| [TalkingHead 3D](https://github.com/met4citizen/TalkingHead) | Browser-based, full-body, npm package | Active, v1.7.0 |
| [MuseTalk](https://github.com/TMElyralab/MuseTalk) | Real-time lip sync, Apache 2.0 | Active, v1.5 |
| [Ditto](https://github.com/antgroup/ditto-talkinghead) | Best real-time neural rendering | Active, training code released |
| [OmniTalker](https://github.com/HumanAIGC/omnitalker) | Text-driven, NeurIPS 2025 | Code released |
| [LivePortrait](https://github.com/KwaiVGI/LivePortrait) | Expression retargeting | Mature, widely used |
| [Linly-Talker](https://github.com/Kedreamix/Linly-Talker) | Full integration framework (reference arch) | Active |
| [LiveTalk-Unity](https://reddit.com/r/Unity3D/comments/1lqy72h/) | Unity package, on-device | New (July 2025) |

---

## Appendix: VRAM Allocation Plan

```
RTX Pro 6000 Blackwell: 96 GB VRAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Qwen3-Coder-Next (11439):    ~57 GB  (MoE, active usage lower)
Qwen2.5-VL (11441):          ~12 GB
MuseTalk (planned):           ~ 5 GB
LivePortrait (planned):       ~ 6 GB
Buffer/overhead:              ~16 GB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total:                        ~96 GB  ✅ Fits!
```

Note: MuseTalk and LivePortrait can be loaded/unloaded on demand if VRAM is tight. The 3D browser avatar (Phase 1) uses zero GPU.
