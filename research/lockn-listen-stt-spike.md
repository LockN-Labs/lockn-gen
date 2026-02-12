# LockN Listen — STT Research Spike

**Date:** 2026-02-07  
**Author:** Research Agent  
**Status:** Complete  
**Hardware:** RTX Pro 6000 Blackwell 96GB VRAM | Threadripper Pro 32c/64t | 256GB RAM  
**Available VRAM for STT:** ~21GB (after LLM 57GB + TTS 6GB + Vision 12GB = 75GB used)

---

## 1. STT Model Landscape (Feb 2026)

### Tier 1: Best-in-Class Open Source

| Model | Params | WER (Avg) | RTFx | VRAM | Streaming | Languages | License |
|-------|--------|-----------|------|------|-----------|-----------|---------|
| **NVIDIA Canary Qwen 2.5B** | 2.5B | 5.63% | 418x | ~8GB | ❌ Batch only | English | CC-BY-4.0 |
| **NVIDIA Parakeet TDT 0.6B v2** | 600M | 6.05% | 3,386x | ~2-3GB | ✅ Via RNNT | English | CC-BY-4.0 |
| **NVIDIA Parakeet TDT 0.6B v3** | 600M | ~5.8% | ~3,400x | ~2-3GB | ✅ | English | CC-BY-4.0 |
| **Kyutai STT 2.6B** | 2.6B | 6.4% | 88x | ~6-8GB | ✅ Native | English | CC-BY-4.0 |
| **Kyutai STT 1B** | 1B | ~7% | ~150x | ~3-4GB | ✅ Native + Semantic VAD | EN + FR | CC-BY-4.0 |
| **IBM Granite Speech 3.3 8B** | ~9B | 5.85% | 31x | ~18-20GB | ❌ | EN + multilingual translate | Apache 2.0 |

### Tier 2: Whisper Family

| Model | Params | WER (Avg) | RTFx | VRAM | Streaming | Languages | License |
|-------|--------|-----------|------|------|-----------|-----------|---------|
| **Whisper Large V3** | 1.55B | 7.4% | ~50-100x | ~10GB | ❌ (30s chunks) | 99+ | MIT |
| **Whisper Large V3 Turbo** | 809M | 7.75% | 216x | ~6GB | ❌ (30s chunks) | 99+ | MIT |
| **Distil-Whisper Large V3** | 756M | ~7.5% | ~300x | ~5GB | ❌ | English | MIT |
| **faster-whisper** (CTranslate2) | same | same WER | 4-8x over vanilla | ~4-6GB (int8) | Pseudo-stream | 99+ | MIT |
| **whisper.cpp** (GGML) | same | same WER | Good CPU perf | CPU-friendly | Pseudo-stream | 99+ | MIT |
| **WhisperX** | same | same WER | ~3x whisper | ~6GB | ❌ (+ alignment) | 99+ | BSD |

### Tier 3: Specialized / Edge

| Model | Params | WER | VRAM | Streaming | Notes |
|-------|--------|-----|------|-----------|-------|
| **Moonshine Base** | 61M | ~12% | <1GB | ✅ | Edge-optimized, English only |
| **Moonshine Tiny** | 27M | ~15% | <0.5GB | ✅ | Smallest footprint |
| **SenseVoice (Alibaba)** | ~600M | ~8% | ~2GB | ❌ | Multilingual + audio events + emotion |
| **Vosk** | various | ~15-20% | CPU | ✅ | Lightweight, offline, many languages |
| **DeepSpeech** | ~47M | ~20%+ | CPU | ✅ | Mozilla, effectively deprecated |

### Tier 4: Commercial Cloud (for reference)

| Service | WER | Latency | Streaming | Notes |
|---------|-----|---------|-----------|-------|
| **Deepgram Nova-3** | ~5-8% | <300ms | ✅ | Best commercial streaming |
| **AssemblyAI Universal-2** | ~8.4% | ~300ms | ✅ | 30% fewer hallucinations vs Whisper |
| **Google Chirp 3** | ~6-8% | ~500ms | ✅ | Best multilingual |
| **Azure Speech** | ~7-10% | ~300ms | ✅ | Enterprise integration |
| **GPT-4o-transcribe** | ~2.5% | N/A | ❌ | Best accuracy, expensive, batch only |

---

## 2. Real-Time / Streaming Capability

### True Streaming Models (process audio as it arrives)

| Model | Architecture | Latency (speech→text) | Built-in VAD | Endpointing |
|-------|-------------|----------------------|--------------|-------------|
| **Kyutai STT 1B** | Decoder-only multistream | **0.5s delay** | ✅ Semantic VAD | ✅ Built-in |
| **Kyutai STT 2.6B** | Decoder-only multistream | **2.5s delay** | ❌ | ❌ |
| **Parakeet RNNT 1.1B** | FastConformer-RNNT | **<200ms** | ✅ Silero VAD | ✅ |
| **Parakeet CTC 1.1B** | FastConformer-CTC | **<100ms** | ✅ Silero VAD optional | ✅ |
| **Moonshine (streaming)** | Sliding-window Transformer | **~500ms** | External | Basic |
| **Vosk** | Kaldi/RNNT | **~200ms** | ✅ | ✅ |

### Pseudo-Streaming (chunked processing)

| Model | Approach | Effective Latency | Notes |
|-------|----------|-------------------|-------|
| **faster-whisper** | VAD-segmented chunks | 1-3s | Silero VAD segments → process each |
| **whisper.cpp** | Sliding window | 2-5s | Real-time mode with --stream flag |
| **WhisperX** | VAD + forced alignment | 3-5s | Best for diarization, not real-time |

### 🏆 For Duplex Conversation

**Kyutai STT 1B is the clear winner** for duplex conversation:
- Built for the Moshi/Unmute voice AI system (designed for real-time duplex)
- 0.5s text delay from speech
- Semantic VAD detects when user is done speaking vs. pausing
- Handles 2+ hour continuous audio without degradation
- Only ~3-4GB VRAM
- Produces capitalized + punctuated text natively

---

## 3. Quality Benchmarks

### LibriSpeech (standard benchmark)

| Model | Clean | Other |
|-------|-------|-------|
| Canary Qwen 2.5B | **1.6%** | **3.1%** |
| Parakeet TDT 0.6B v2 | 2.0% | 3.8% |
| Kyutai STT 2.6B | 2.1% | 4.2% |
| Whisper Large V3 | 2.5% | 5.2% |
| Whisper Turbo | 2.7% | 5.8% |
| Distil-Whisper | 2.6% | 5.5% |

### Noise Robustness

| Model | Clean WER | 10dB SNR WER | Degradation |
|-------|-----------|-------------|-------------|
| Canary Qwen 2.5B | 5.63% | 2.41% (@10dB) | Excellent |
| Granite Speech 3.3 8B | 8.18% | ~15.7% | 7.5% degradation |
| Kyutai STT | Robust (trained on noisy data) | — | Good |
| Parakeet CTC + Silero VAD | Good | Good | VAD helps significantly |

### Long-Form Accuracy
- **Kyutai STT 2.6B**: Tested up to 2 hours continuously, no quality degradation
- **Whisper Large V3**: Degrades on >30s segments, requires chunking (30s windows)
- **Canary Qwen 2.5B**: Requires 10s chunked inference for best results
- **Parakeet**: Handles long-form well via streaming architecture

### Punctuation & Formatting
- **Kyutai STT**: ✅ Native capitalization + punctuation
- **Canary Qwen**: ✅ Automatic punctuation and capitalization
- **Parakeet TDT v2**: ✅ Punctuation-aware
- **Whisper**: ✅ Good punctuation (but can hallucinate on silence)
- **Parakeet CTC 0.6B**: ⚠️ Lowercase only, minimal punctuation

---

## 4. Hardware Fit for LockN Stack

### VRAM Budget

```
Total VRAM:          96 GB
LLM (Qwen3-Coder):  57 GB
TTS (Chatterbox):     6 GB
Vision (Qwen2.5-VL):  12 GB
─────────────────────────
Used:                75 GB
Available for STT:   ~21 GB
```

### Model Fit Analysis

| Model | VRAM | Fits? | Notes |
|-------|------|-------|-------|
| **Kyutai STT 1B** | ~3-4GB | ✅ Easily | Best for real-time, leaves headroom |
| **Parakeet TDT 0.6B v3** | ~2-3GB | ✅ Easily | Fastest, best for batch |
| **Parakeet CTC 1.1B + Silero VAD** | ~4GB | ✅ Easily | Good streaming option |
| **Canary Qwen 2.5B** | ~8GB | ✅ Yes | Best accuracy, batch only |
| **Distil-Whisper** | ~5GB | ✅ Yes | Good Whisper replacement |
| **Whisper Large V3 Turbo** | ~6GB | ✅ Yes | Current deployment equivalent |
| **Kyutai STT 2.6B** | ~6-8GB | ✅ Yes | Streaming + high accuracy |
| **IBM Granite 8B** | ~18-20GB | ⚠️ Tight | Would consume nearly all headroom |
| **Whisper Large V3** | ~10GB | ✅ Yes | But slower than alternatives |

### CPU-Only Options for Overflow

| Model | RAM | Speed | Use Case |
|-------|-----|-------|----------|
| **whisper.cpp (turbo, Q5)** | ~3GB | 5-10x real-time on 32c | Batch file transcription |
| **Vosk** | <1GB | Real-time capable | Voice commands, lightweight |
| **Moonshine** | <0.5GB | Real-time on CPU | Edge/fallback |

### Recommended Dual-Model Strategy

Run **two models simultaneously** within 21GB budget:

1. **Kyutai STT 1B** (~3-4GB) — Real-time streaming for conversations
2. **Parakeet TDT 0.6B v3** (~2-3GB) — Batch file transcription at 3,400x speed

Total: **~6-7GB VRAM**, leaving 14GB headroom for peaks.

---

## 5. Integration Architecture

### Real-Time Agent Pipeline

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐
│ Browser  │───▶│ VAD +   │───▶│ Kyutai   │───▶│ LLM      │───▶│ TTS     │
│ Mic/WS   │    │ Audio   │    │ STT 1B   │    │ (Brain)  │    │ (Speak) │
│          │◀───│ Buffer  │    │ Stream   │    │ Streaming│    │         │
└─────────┘    └─────────┘    └──────────┘    └──────────┘    └─────────┘
                                  0.5s            ~1-2s          ~0.5s
                              ◀──────────── Total: ~2-3s ──────────────▶
```

### Latency Budget (Duplex Conversation)

| Stage | Latency | Model |
|-------|---------|-------|
| Audio capture + WebSocket | ~50ms | Browser → Server |
| VAD endpointing | ~200ms | Silero VAD / Kyutai Semantic VAD |
| STT processing | ~500ms | Kyutai STT 1B (0.5s delay) |
| LLM first token | ~200ms | Qwen3-Coder (500 tok/s) |
| LLM generation | ~500ms (first sentence) | Streaming to TTS |
| TTS synthesis | ~300ms | Chatterbox / FishAudio |
| Audio playback start | ~50ms | WebSocket → Browser |
| **Total round-trip** | **~1.8s** | Competitive with commercial |

### WebSocket Streaming Architecture

```python
# Proposed LockN Listen service architecture
class LockNListen:
    def __init__(self):
        self.stt_realtime = KyutaiSTT("kyutai/stt-1b-en_fr")  # Streaming
        self.stt_batch = ParakeetTDT("nvidia/parakeet-tdt-0.6b-v3")  # Batch
        self.vad = SileroVAD()  # Voice Activity Detection

    async def handle_websocket(self, ws):
        """Real-time streaming transcription via WebSocket"""
        async for audio_chunk in ws:
            # Kyutai processes chunks as they arrive
            text = self.stt_realtime.process_chunk(audio_chunk)
            if text:
                await ws.send(json.dumps({"text": text, "final": False}))

    async def transcribe_file(self, audio_path):
        """Batch file transcription — max speed"""
        return self.stt_batch.transcribe(audio_path)  # 3,400x real-time
```

### Service Configuration

```yaml
# lockn-listen service (proposed)
name: lockn-listen
port: 8891  # Next to lockn-whisper-gpu on 8890
endpoints:
  - /ws/stream     # WebSocket real-time (Kyutai)
  - /api/transcribe # REST batch (Parakeet)
  - /api/commands   # Voice command mode (Kyutai with short timeout)
gpu: shared  # Uses ~6-7GB of remaining VRAM
```

---

## 6. Recommendations

### 🥇 Best for Real-Time Agent Conversations (Lowest Latency)

**NVIDIA Parakeet CTC 1.1B + Silero VAD**
- <100ms processing latency
- ~4GB VRAM
- Built-in noise robustness
- Via NeMo/Riva for production deployment

**Runner-up: Kyutai STT 1B**
- 500ms delay but with semantic VAD (knows when you're done talking)
- Purpose-built for duplex conversation (from the Moshi/Unmute team)
- Better endpointing intelligence

**Recommendation:** Start with Parakeet CTC for lowest raw latency. Add Kyutai STT 1B when building duplex conversation mode — its semantic VAD is uniquely suited for natural turn-taking.

### 🥇 Best for File Transcription (Highest Accuracy)

**NVIDIA Canary Qwen 2.5B**
- 5.63% WER (best open-source)
- 418x RTFx — a 1-hour file transcribes in ~8.6 seconds
- ~8GB VRAM
- Excellent noise robustness (2.41% WER at 10dB SNR)

**For speed over accuracy: Parakeet TDT 0.6B v3**
- 3,400x RTFx — a 1-hour file transcribes in ~1 second
- 6.05% WER (still excellent)
- Only ~2-3GB VRAM

### 🥇 Best Overall for LockN Listen

**Dual-model deployment:**

| Use Case | Model | VRAM | Why |
|----------|-------|------|-----|
| Real-time conversations | Kyutai STT 1B | ~3-4GB | Streaming, semantic VAD, duplex-ready |
| File transcription | Parakeet TDT 0.6B v3 | ~2-3GB | 3,400x speed, excellent accuracy |
| Voice commands | Kyutai STT 1B | (shared) | Low latency, built-in endpointing |
| Duplex conversation | Kyutai STT 1B | (shared) | Designed for this exact use case |
| **Total VRAM** | | **~6-7GB** | Well within 21GB budget |

### 🔄 Migration Path from Current Whisper Deployment

**Phase 1: Quick Win (This Week)**
1. Deploy **Parakeet TDT 0.6B v3** alongside existing Whisper on port 8891
2. Route file transcription to Parakeet (3,400x faster, better accuracy)
3. Keep Whisper on port 8890 as fallback
4. Install: `pip install nemo_toolkit[asr]` or use NVIDIA NIM container

**Phase 2: Real-Time STT (Next 2 Weeks)**
1. Deploy **Kyutai STT 1B** for streaming transcription
2. Build WebSocket endpoint for browser-based voice input
3. Integrate with LockN Brain for streaming text → LLM pipeline
4. Test end-to-end latency budget

**Phase 3: Duplex Conversation (Month 2)**
1. Implement semantic VAD-based turn-taking with Kyutai STT 1B
2. Build concurrent listen+speak pipeline (STT runs while TTS plays)
3. Add barge-in detection (user interrupts agent)
4. Optimize total round-trip to <2s

**Phase 4: Retire Whisper (Month 3)**
1. Validate Parakeet + Kyutai cover all Whisper use cases
2. Shut down lockn-whisper-gpu service (port 8890)
3. Reclaim ~6-10GB VRAM

### ⚡ Quick Wins vs Medium-Term

| Timeframe | Action | Impact |
|-----------|--------|--------|
| **Today** | Deploy Parakeet TDT for batch transcription | 50-100x faster file processing |
| **This week** | Add Silero VAD to audio pipeline | Better speech segmentation |
| **Week 2** | Deploy Kyutai STT 1B for streaming | Real-time transcription unlocked |
| **Week 3** | WebSocket streaming endpoint | Browser voice input enabled |
| **Month 2** | Duplex conversation pipeline | Agent conversations feel natural |
| **Month 3** | Retire Whisper, optimize latency | Cleaner stack, less VRAM |

---

## Key Links

- [NVIDIA Parakeet TDT 0.6B v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
- [NVIDIA Canary Qwen 2.5B](https://huggingface.co/nvidia/canary-qwen-2.5b)
- [NVIDIA Parakeet RNNT 1.1B (NIM)](https://build.nvidia.com/nvidia/parakeet-1_1b-rnnt-multilingual-asr)
- [Kyutai STT 2.6B](https://huggingface.co/kyutai/stt-2.6b-en)
- [Kyutai STT 1B](https://huggingface.co/kyutai/stt-1b-en_fr)
- [Kyutai GitHub](https://github.com/kyutai-labs/delayed-streams-modeling)
- [IBM Granite Speech 3.3](https://huggingface.co/ibm-granite/granite-speech-3.3-8b)
- [Moonshine](https://github.com/moonshine-ai/moonshine)
- [Silero VAD](https://github.com/snakers4/silero-vad)
- [Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
- [NVIDIA NeMo Toolkit](https://github.com/NVIDIA/NeMo)

---

## TL;DR

**Replace Whisper with a dual-model setup:**
1. **Kyutai STT 1B** for real-time/streaming/duplex (~3-4GB VRAM, 0.5s latency, semantic VAD)
2. **Parakeet TDT 0.6B v3** for batch file transcription (~2-3GB VRAM, 3,400x real-time speed)

Total: ~6-7GB VRAM (vs ~10GB for Whisper). Better accuracy. 50-100x faster batch. True streaming. Duplex-ready. All within budget.
