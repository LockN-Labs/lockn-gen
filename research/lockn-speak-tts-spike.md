# LockN Speak TTS — Research Spike Report
**Date:** 2026-02-07 | **Author:** Research Agent

---

## 1. Competitive Landscape (Feb 2026)

### Cloud TTS Providers

| Provider | Quality Tier | Latency | Voice Cloning | Languages | Pricing |
|----------|-------------|---------|---------------|-----------|---------|
| **ElevenLabs** | Best-in-class | ~200ms TTFB | Yes (Instant + Professional) | 32+ | Free tier → $5/mo (Starter) → $22/mo (Creator) → $330/mo (Scale) → $1,320/mo (Business). ~$0.30/1K chars at scale |
| **OpenAI TTS** | Very good | ~300ms | No (6 preset voices) | 50+ | $15/1M chars (tts-1), $30/1M chars (tts-1-hd), gpt-4o-mini-tts token-based |
| **PlayHT** | Very good | ~200ms (Turbo) | Yes (instant clone) | 140+ | $31.20/mo (Creator) → $99/mo (Pro). Per-char pricing on API |
| **Amazon Polly** | Good (Neural) | ~100ms | No | 30+ | $19.20/1M chars (Neural), $4/1M (Standard). Free tier: 5M chars/mo yr1 |
| **Google Cloud TTS** | Good-Very good | ~100ms | No (limited custom voice) | 40+ | $4/1M chars (Standard), $16/1M (WaveNet), $16/1M (Neural2). 1M free/mo |
| **Azure Speech** | Good-Very good | ~100ms | Yes (Custom Neural Voice) | 60+ | $15/1M chars (Neural). Free tier: 0.5M chars/mo |

### Open-Source / Local TTS Models

| Model | Params | Quality | Latency | Voice Cloning | Emotion Control | Languages | License |
|-------|--------|---------|---------|---------------|-----------------|-----------|---------|
| **Chatterbox Turbo** | 350M | ⭐⭐⭐⭐⭐ (beats ElevenLabs in blind tests) | <200ms TTFB | Yes (10s ref) | Paralinguistic tags ([laugh], [cough]) | EN only (Multilingual: 23) | MIT |
| **FishAudio S1-mini** | 500M (full S1: 4B) | ⭐⭐⭐⭐⭐ (#1 on TTS-Arena2) | Medium | Yes (10-30s ref) | **50+ emotion/tone markers** | 13 | Apache 2.0 |
| **Kokoro** | 82M | ⭐⭐⭐⭐ (excellent for size) | Ultra-fast (<0.3s) | Limited | No | EN, JA, ZH, KO, FR | Apache 2.0 |
| **Dia2** (Nari Labs) | 1B-2B | ⭐⭐⭐⭐ | Streaming capable | No (multi-speaker via tags) | Yes (laughter, sighs, nonverbal) | EN | Apache 2.0 |
| **Sesame CSM-1B** | 1B | ⭐⭐⭐⭐ (conversational focus) | Medium | Yes (context-based) | Conversational prosody | EN | CC-BY-NC 4.0 |
| **VibeVoice** (Microsoft) | 0.5B-1.5B | ⭐⭐⭐⭐ | ~300ms (Realtime) | No | Multi-speaker, long-form | EN, ZH | Research only |
| **NVIDIA Magpie** | 357M | ⭐⭐⭐⭐ | ~300-600ms | Yes | Limited | Multilingual | Apache 2.0 |
| **F5-TTS** | ~300M | ⭐⭐⭐½ | Good (<7s) | Yes (zero-shot) | Limited | EN, ZH | MIT |
| **Piper** | Tiny | ⭐⭐⭐ (fast/functional) | Ultra-fast | No | No | 30+ | MIT |
| **XTTS v2** (Coqui) | ~400M | ⭐⭐⭐½ | Medium | Yes (voice cloning) | Limited | 17 | CPML (restrictive) |
| **MeloTTS** | Small | ⭐⭐⭐ | Very fast | No | No | EN, ZH, JA, KO, FR, ES | MIT |
| **Parler-TTS** | 600M | ⭐⭐⭐ | Slow | No (text-described voice) | Text-described style | EN | Apache 2.0 |
| **OuteTTS** | ~400M | ⭐⭐⭐ | Medium | Yes (zero-shot) | Limited | EN, ZH, JA, KO | Apache 2.0 |
| **Qwen3-TTS** | Unknown | ⭐⭐⭐⭐ (new, Jan 2026) | Streaming (25Hz) | Yes | Yes | Multilingual | TBD |
| **Marvis TTS** | 250M+60M | ⭐⭐⭐½ | Real-time streaming | Yes | Conversational | EN | Open |

---

## 2. Quality Improvement Opportunities

### Current Best-in-Class Open-Source (Feb 2026)

**Tier 1 — Production-ready, competing with ElevenLabs:**
1. **FishAudio S1-mini** — #1 on TTS-Arena2. Best emotion control (50+ markers). Best voice cloning quality locally. 13 languages.
2. **Chatterbox Turbo** — Wins blind tests vs ElevenLabs. MIT license. Paralinguistic tags. You're already running this.
3. **Dia2** — Best for dialogue/conversational. Streaming architecture.

**Tier 2 — Strong contenders:**
4. **Sesame CSM-1B** — Conversational focus, great prosody. CC-BY-NC limits commercial use.
5. **VibeVoice** — Long-form champion (90 min). Research license limits use.
6. **Qwen3-TTS** — Brand new (Jan 2026), streaming-native, from Alibaba. Watch this space.

### Chatterbox vs Alternatives

| Dimension | Chatterbox Turbo | FishAudio S1-mini | Dia2 |
|-----------|-----------------|-------------------|------|
| Overall quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Emotion control | Basic (paralinguistic tags) | **Best** (50+ markers) | Good (nonverbal) |
| Voice cloning | Good (10s ref) | **Best** (10-30s, captures style) | No |
| Streaming | Not native | Not optimized for RT | **Yes, native** |
| Languages | EN (23 with Multilingual) | 13 | EN only |
| License | **MIT** ✅ | Apache 2.0 ✅ | Apache 2.0 ✅ |
| VRAM | Low (~2GB) | Medium (~4GB) | Medium (~4-8GB) |

### Recommendations for Quality Uplift

1. **Add FishAudio S1-mini as alternative engine** — Superior emotion control, better voice cloning. Could be primary for expressive use cases.
2. **Add Dia2 for streaming/conversational** — Native streaming makes it ideal for agent responses.
3. **Keep Chatterbox Turbo as default** — MIT license, proven quality, low VRAM, great for production.
4. **Watch Qwen3-TTS** — Just released, could be a game-changer with streaming + multilingual.

---

## 3. Configurability Features to Build

### What Power Users Want (Competitive Analysis)

| Feature | ElevenLabs | FishAudio S1 | Chatterbox | **LockN Speak (Build?)** |
|---------|-----------|--------------|------------|--------------------------|
| Speed/rate control | ✅ | ✅ | ❌ | **Yes — easy win** |
| Pitch control | ✅ | Partial | ❌ | **Yes** |
| Emotion tags | ✅ (via text) | ✅ (50+ markers) | ✅ (basic) | **Expand markers** |
| SSML support | ✅ | ❌ | ❌ | **Medium priority** |
| Voice blending | ✅ (voice design) | ❌ | ❌ | **Differentiator** |
| Per-sentence style | ❌ | ✅ | ❌ | **Yes — key feature** |
| Emphasis/stress | ✅ (SSML) | Partial | ❌ | **Yes** |
| Streaming output | ✅ | ❌ | ❌ | **Critical for agents** |
| Multi-speaker | ❌ | ❌ | ❌ (Dia2 yes) | **Yes via Dia2** |
| Voice personas/presets | ✅ | ✅ | ❌ | **Yes — agent personas** |

### Priority Features to Build

1. **Multi-engine support** — Hot-swap between Chatterbox, FishAudio S1-mini, Dia2, Kokoro based on use case
2. **Voice persona system** — Named voices with saved reference clips + style presets
3. **Streaming synthesis** — Chunk-based output as LLM generates tokens
4. **Emotion/style API** — Unified interface for emotion tags across engines
5. **Speed/pitch/rate controls** — Post-processing with librosa/rubberband
6. **Per-sentence voice switching** — Parse text, route segments to different voices/styles

---

## 4. Differentiation: TTS + Agentic AI

### Does Anyone Do This Today?

| Product | Local? | Agent-integrated TTS? | Emotion-aware? | Notes |
|---------|--------|----------------------|----------------|-------|
| **ElevenLabs Conversational AI 2.0** | ❌ Cloud | Yes — full agent platform | Basic | $330+/mo. Multi-agent flows, auto language detection. Cloud lock-in. |
| **OpenAI Realtime API** | ❌ Cloud | Yes — native voice mode | Native (GPT-4o) | Expensive. Voice is baked into the model, not separable. |
| **LocalAIVoiceChat** | ✅ Local | Basic (Whisper + Zephyr + XTTS) | ❌ | Hobby project. No agent framework integration. |
| **Daily.co + NVIDIA** | Hybrid | Yes (Magpie + LLM) | ❌ | Focus on WebRTC infra, not agent intelligence. |

**Key finding: Nobody offers deeply integrated local TTS with agentic AI and dual-process thinking.** This is a wide-open niche.

### The LockN Speak Vision: Agentic Voice

```
User speaks/types → STT (local) → Agent (Qwen3-Coder on RTX 6000)
                                        ↓
                            Fast thinking: quick response draft
                            Slow thinking: deep reasoning if needed
                                        ↓
                            Emotion analysis of response text
                                        ↓
                            Voice persona selection (per agent role)
                                        ↓
                        Streaming TTS → Audio output (real-time)
```

### Killer Features (What No One Else Has)

1. **Auto-emotion from text** — LLM annotates its own output with emotion tags before TTS. "I'm sorry to hear that [sad]" → sad prosody. No one does this automatically.

2. **Agent voice personas** — Each agent/role gets a distinct voice + style profile:
   - "Assistant" → warm, measured tone
   - "Code reviewer" → precise, neutral
   - "Storyteller" → dramatic, varied
   - Stored as: reference clip + emotion defaults + speed/pitch prefs

3. **Streaming TTS as tokens generate** — Agent starts speaking its first sentence while still generating the rest. Key latency win:
   - Sentence boundary detection on streaming LLM output
   - Queue sentences to TTS engine
   - Overlap: sentence N plays while sentence N+2 generates

4. **Dual-process voice** — Fast thinking = immediate spoken response. Slow thinking = "Let me think about that..." (filler/acknowledgment), then deeper answer. Natural conversational pattern.

5. **100% local, zero cloud** — Privacy, no per-character costs, no rate limits. On 96GB VRAM you can run LLM + TTS + STT simultaneously.

6. **Context-aware prosody** — Agent knows conversation history → adjusts tone. Delivering bad news? Softer. Celebrating? Energetic.

### vs ElevenLabs Conversational AI: The "10x Better" Pitch

| Dimension | ElevenLabs | LockN Speak |
|-----------|-----------|-------------|
| Cost | $330-1,320+/mo + per-char | **$0/mo** (own hardware) |
| Privacy | Cloud (data leaves premises) | **100% local** |
| Latency | ~200ms + network RTT | **<200ms** (no network) |
| Customization | Limited to their API | **Full control** (swap models, modify everything) |
| Agent integration | Their platform only | **Any local LLM** (OpenClaw, Ollama, llama.cpp) |
| Emotion intelligence | Basic | **LLM-driven auto-emotion** |
| Voice personas | Static voice selection | **Dynamic, context-aware personas** |
| Offline capability | ❌ | **✅** |
| Scale ceiling | Monthly char limits | **Unlimited** (GPU-bound only) |

---

## 5. Prioritized Recommendations

### 🟢 Quick Wins (1-2 weeks)

1. **Add FishAudio S1-mini as second engine** — `pip install fish-speech`. Superior emotion control with 50+ markers. Run alongside Chatterbox. Your 96GB VRAM can easily handle both loaded.

2. **Implement voice persona system** — JSON config with reference clips, default emotion, speed preferences. Simple but transforms UX.
   ```json
   {
     "name": "assistant",
     "engine": "chatterbox-turbo",
     "ref_clip": "voices/assistant.wav",
     "default_emotion": "neutral",
     "speed": 1.0
   }
   ```

3. **Add speed/pitch post-processing** — Use `torchaudio.functional` or `rubberband-cli` for real-time rate/pitch shifting. ~50 lines of code.

4. **OpenAI-compatible API endpoint** — Match the `/v1/audio/speech` API shape so any tool expecting OpenAI TTS just works.

### 🟡 Medium-Term (1-2 months)

5. **Streaming TTS pipeline** — Sentence boundary detection on LLM output stream → queue to TTS → stream audio chunks via WebSocket. This is the single most impactful feature for agent UX.

6. **Auto-emotion annotation** — Before TTS, run a lightweight classifier (or prompt the LLM) to insert emotion tags. Map to engine-specific syntax (Chatterbox paralinguistic tags or FishAudio emotion markers).

7. **Multi-engine router** — Select engine by use case:
   - Quick responses → Kokoro (82M, ultra-fast)
   - Expressive/emotional → FishAudio S1-mini
   - Voice cloning → Chatterbox Turbo
   - Dialogue/conversation → Dia2

8. **Integrate Dia2 for multi-speaker** — Enable agent conversations where multiple AI personas speak with distinct voices in a single audio stream.

9. **Voice cloning UI** — Simple web interface: upload 10-30s clip → create named persona. Store in voice library.

### 🔴 Long-Term Differentiators (3-6 months)

10. **Agentic Voice Pipeline** — The full vision: OpenClaw agent → emotion analysis → persona selection → streaming TTS. This doesn't exist anywhere in the local AI space. Position as the **"local ElevenLabs Conversational AI"** but open, private, and free.

11. **Dual-process voice UX** — Fast response with filler ("Sure, let me look into that...") while slow thinking generates the real answer. Natural conversational flow that no other system does.

12. **Context-aware prosody engine** — Track conversation sentiment over time. Adjust voice characteristics based on emotional arc. Serious topic → measured delivery. Good news → upbeat.

13. **Voice mixing/interpolation** — Blend two reference voices to create new personas. Experimental but unique. FishAudio S1's architecture might support this.

14. **Real-time voice activity detection + interrupt handling** — Full duplex conversation: user can interrupt the agent mid-sentence, agent stops and responds naturally.

15. **LockN Suite integration** — PANNs audio classification feeds into the pipeline (detect user emotion from their voice → agent adjusts response tone). Vision (Qwen2.5-VL) describes visual context → agent speaks about what it sees with appropriate affect.

---

## Key Takeaways

1. **You're already on a top-tier engine** (Chatterbox). The MIT license and quality are excellent. Don't replace it — supplement it.

2. **FishAudio S1-mini is the biggest upgrade opportunity** — #1 on TTS-Arena2, 50+ emotion controls, Apache 2.0. Add it as a second engine this week.

3. **The real moat is agentic integration, not TTS quality alone.** Everyone will converge on similar quality. Nobody is doing intelligent, context-aware, local voice personas for AI agents.

4. **Streaming is table stakes for agent UX.** Dia2 and VibeVoice-Realtime show the way. Build sentence-level streaming into LockN Speak ASAP.

5. **96GB VRAM is a massive advantage.** You can run Qwen3-Coder (23GB) + Chatterbox (2GB) + FishAudio S1-mini (4GB) + Kokoro (< 1GB) + Qwen2.5-VL (12GB) simultaneously with room to spare. No one in the cloud-TTS world can match this for integrated local AI.
