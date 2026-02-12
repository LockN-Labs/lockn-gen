# LockN Sense: Unified Audio Analytics Strategy Brief
## Unifying LockN Listen + LockN Sound → LockN Score

**Date:** 2026-02-08  
**Research Lead:** Research Agent  
**Status:** Implementation-Ready Strategy

---

## Executive Summary

This brief delivers a practical, implementation-ready strategy for unifying LockN Listen (audio event detection) and LockN Sound (sound classification) into a single applied stack that feeds LockN Score. The focus is on solving **ping-pong constraints**: distinguishing paddle-hits vs table-bounces, detecting multi-bounce same-side violations, and handling solo hit-back mode rules.

**Key Research Findings:**
- Sony AI's recent work (2024-2025) demonstrates millisecond-accurate bounce detection and spin classification from audio alone using energy-based detection + lightweight CNNs on mel spectrograms
- Table tennis ball-racket contact times are extremely brief: **1.3-1.8ms** (vs ~5ms in tennis), requiring fine temporal resolution
- Edge-optimized architectures (MobileNet, EfficientNet, depthwise separable convolutions) achieve <50ms inference on modern mobile hardware
- ONNX Runtime enables sub-10ms inference overhead with cross-platform deployment

---

## 1. Recommended System Architecture

### 1.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LOCKN SENSE PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Audio     │───▶│  Stream      │───▶│   Event     │───▶│   State     │ │
│  │   Capture   │    │  Buffer      │    │   Detector  │    │   Machine   │ │
│  │  (48kHz)    │    │  (Ring Buf)  │    │  (Peak+CNN) │    │  (Rally FSM)│ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └──────┬──────┘ │
│        │                                                            │       │
│        │                                                            ▼       │
│        │                                                     ┌─────────────┐│
│        │                                                     │   Rally     ││
│        │                                                     │   Logic     ││
│        │                                                     │  (Rules)    ││
│        │                                                     └──────┬──────┘│
│        │                                                            │       │
│        ▼                                                            ▼       │
│  ┌─────────────┐                                            ┌─────────────┐│
│  │  Feature    │                                            │  LockN      ││
│  │  Extractor  │───────────────────────────────────────────▶│  Score      ││
│  │(Mel Spec+   │           Classification Results          │  (Output)   ││
│  │  MFCC)      │                                            │             ││
│  └─────────────┘                                            └─────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Model Stack Architecture

#### Stage 1: Real-Time Event Detection (LockN Listen)
**Purpose:** Millisecond-accurate onset detection of acoustic events

| Component | Implementation | Latency Target |
|-----------|---------------|----------------|
| Energy Peak Detector | Exponential moving average + adaptive threshold | <5ms |
| High-Pass Filter | 2nd-order Butterworth, fc=500Hz | <1ms |
| Candidate Windowing | 50ms context windows around peaks | - |

**Algorithm (from Sony AI research):**
```python
# Adaptive energy-based detection
def detect_bounce_candidates(audio_buffer, sample_rate=48000):
    # High-pass filter to remove low-freq noise (footsteps, voice)
    filtered = highpass_filter(audio_buffer, cutoff=500)
    
    # Exponential moving average with attack/release
    envelope = ema_with_attack_release(filtered, attack=0.1, release=10)
    
    # Adaptive threshold based on recent noise floor
    threshold = noise_floor_estimate + adaptive_margin
    
    # Peak detection with minimum distance (debounce)
    peaks = find_peaks(envelope, threshold, min_distance_ms=50)
    return peaks
```

#### Stage 2: Event Classification (LockN Sound)
**Purpose:** Classify detected events into semantic categories

| Model | Architecture | Input | Output Classes | Model Size |
|-------|-------------|-------|---------------|------------|
| Surface Classifier | EfficientNet-B0 variant | Mel spectrogram (64 bins, 96ms) | paddle-hit, table-bounce, floor-bounce, net-hit, noise | 5.3MB |
| Game Mode Classifier | MobileNetV3-Small | MFCC (40 coeffs, 13 deltas) | serve, rally, solo-return, invalid | 2.1MB |
| Spin Detector (v2) | Custom Depthwise CNN | Mel spectrogram + high-freq bands | topspin, backspin, flat, sidespin | 3.8MB |

**Architecture Details:**
- **Mel Spectrogram:** 64 mel bins, 20-20kHz, 10ms hop length, 25ms window
- **Inference:** ONNX Runtime with CoreML/NNAPI delegates for mobile acceleration
- **Batch size:** 1 (real-time streaming)

#### Stage 3: Rally State Machine (LockN Score Integration)
**Purpose:** Apply table tennis rules to event sequence

```
States:
- IDLE: Waiting for serve
- SERVE_CONTACT: Ball hit on serve
- SERVE_BOUNCE: Ball bounced on receiver side
- RALLY: Active rally in progress
- SOLO_MODE: Solo hit-back (training mode)
- POINT_END: Scoring condition met

Transitions:
(paddle-hit) → track which player (based on directional audio features)
(table-bounce) → validate same-side constraints
(floor-bounce) → point ends, opponent scores
(double-bounce same side) → point ends, opponent scores
```

### 1.3 Audio Feature Pipeline

```
Raw Audio (48kHz, 16-bit, mono)
    │
    ▼
Pre-emphasis (0.97) ──▶ High-pass filter (500Hz)
    │
    ▼
Framing (25ms window, 10ms hop) ──▶ Hamming window
    │
    ├──▶ Energy envelope (for peak detection)
    │
    └──▶ FFT (2048 points)
            │
            ├──▶ Mel filterbank (64 bins, 20-20kHz) ──▶ Log compression ──▶ Mel Spectrogram
            │
            └──▶ MFCC (40 coefficients + deltas) ──▶ Game mode classifier
```

---

## 2. Training/Data Strategy & Annotation Schema

### 2.1 Dataset Requirements

| Category | Minimum Samples | Priority | Sources |
|----------|-----------------|----------|---------|
| Paddle hits (flat) | 2,000 | P0 | Recorded sessions + synthetic |
| Paddle hits (topspin) | 1,500 | P0 | Recorded sessions |
| Paddle hits (backspin) | 1,500 | P0 | Recorded sessions |
| Table bounces (normal) | 2,500 | P0 | Recorded sessions |
| Table bounces (serve) | 1,000 | P1 | Recorded sessions |
| Floor bounces | 800 | P1 | Recorded sessions |
| Net hits | 500 | P2 | Recorded sessions |
| Environmental noise | 3,000 | P0 | Field recordings + AudioSet |
| Player vocalizations | 1,000 | P1 | Field recordings |
| Footsteps/movement | 1,000 | P1 | Field recordings |
| **Total** | **14,800+** | | |

### 2.2 Recording Specifications

**Hardware Setup:**
- Primary: Directional shotgun mic (Zoom H4n Pro or similar) at 44.1-48kHz
- Secondary: Boundary mics on table edges for spatial separation
- Distance: 0.5-2m from table center

**Racket Configurations to Capture:**
| Blade Type | Sponge Thickness | Rubber Type | Config ID |
|------------|------------------|-------------|-----------|
| Offensive | 2.1mm | Inverted (offensive) | CFG-01 |
| Offensive | 1.8mm | Inverted (allround) | CFG-02 |
| Defensive | 2.1mm | Inverted (offensive) | CFG-03 |
| Defensive | 1.8mm | Inverted (allround) | CFG-04 |
| Allrounder | 1.2mm | Long pips | CFG-05 |
| Allrounder | 0mm | Long pips | CFG-06 |
| Allrounder | 1.2mm | Medium pips | CFG-07 |
| Offensive | 2.0mm | Short pips | CFG-08 |
| Offensive | 2.1mm | Anti-spin | CFG-09 |

### 2.3 Annotation Schema (JSON-LD)

```json
{
  "annotation_version": "1.0.0",
  "audio_file": "session_001.wav",
  "sample_rate": 48000,
  "duration_ms": 125000,
  "recording_config": {
    "microphone": "Zoom H4n Pro",
    "distance_m": 1.5,
    "environment": "indoor_club",
    "racket_config": "CFG-01"
  },
  "events": [
    {
      "event_id": "evt_001",
      "onset_ms": 2340.5,
      "offset_ms": 2385.2,
      "duration_ms": 44.7,
      "labels": {
        "surface": "racket",
        "spin_type": "topspin",
        "spin_magnitude": "heavy",
        "game_context": "serve",
        "player_position": "right_side_near",
        "confidence": 0.95
      },
      "audio_features": {
        "peak_amplitude_db": -12.4,
        "freq centroid_hz": 2850,
        "spectral_rolloff_hz": 5200
      },
      "validation": {
        "annotator_id": "ann_003",
        "timestamp": "2026-02-08T14:23:11Z",
        "verified": true
      }
    }
  ],
  "rally_segments": [
    {
      "rally_id": "ral_001",
      "start_ms": 2340.5,
      "end_ms": 8940.2,
      "event_sequence": ["evt_001", "evt_002", "evt_003", "evt_004"],
      "rally_context": "match_play",
      "point_winner": "player_a",
      "termination_reason": "floor_bounce"
    }
  ]
}
```

### 2.4 Augmentation Strategy

| Augmentation | Parameters | Application |
|--------------|------------|-------------|
| Time stretching | 0.8-1.2x | All events |
| Pitch shifting | ±3 semitones | All events |
| Additive noise | SNR 10-30dB (crowd, HVAC, footsteps) | All events |
| Room simulation | RT60 0.2-1.5s (small room to arena) | All events |
| Frequency masking | 1-3 bands, max 15% | Training only |
| Time masking | 10-50ms gaps | Training only |
| Elastic deformation | Time warping | Spectrogram augment |
| Mixup | α=0.2 | Between same-class samples |

---

## 3. Real-Time Inference Design

### 3.1 Latency Budget Allocation

| Component | Target Latency | Worst Case | Notes |
|-----------|---------------|------------|-------|
| Audio capture buffer | 5ms | 10ms | 240 samples @ 48kHz |
| Feature extraction | 8ms | 15ms | Mel spec + MFCC on CPU |
| Peak detection | 2ms | 5ms | EMA-based, very fast |
| CNN inference | 15ms | 30ms | ONNX Runtime, quantized |
| State machine update | 1ms | 2ms | Simple FSM |
| Output dispatch | 1ms | 3ms | MQTT/WebSocket |
| **End-to-end** | **32ms** | **65ms** | |

### 3.2 Inference Pipeline Architecture

```python
class LockNSensePipeline:
    """
    Streaming audio event detection and classification.
    Optimized for <50ms end-to-end latency.
    """
    
    def __init__(self):
        # Ring buffer for continuous audio streaming
        self.audio_buffer = RingBuffer(capacity=48000)  # 1 second @ 48kHz
        
        # ONNX Runtime session with optimizations
        self.ort_session = ort.InferenceSession(
            "lockn_sound_quantized.onnx",
            providers=['CoreMLExecutionProvider', 'CPUExecutionProvider'],
            sess_options=self._create_sess_options()
        )
        
        # State machines
        self.rally_fsm = RallyStateMachine()
        self.solo_fsm = SoloModeStateMachine()
        
        # Feature extractors
        self.mel_extractor = MelSpectrogram(
            sample_rate=48000,
            n_fft=2048,
            hop_length=480,  # 10ms
            n_mels=64,
            f_min=50,
            f_max=20000
        )
        
    def _create_sess_options(self):
        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        opts.enable_cpu_mem_arena = False
        opts.intra_op_num_threads = 2
        opts.inter_op_num_threads = 2
        return opts
    
    def process_chunk(self, audio_chunk: np.ndarray):
        """Process 10ms audio chunk (480 samples)."""
        # Add to ring buffer
        self.audio_buffer.extend(audio_chunk)
        
        # Energy-based candidate detection
        candidates = self._detect_candidates()
        
        events = []
        for onset_ms in candidates:
            # Extract 96ms window around candidate (50ms before, 46ms after)
            window = self.audio_buffer.get_window(
                center_ms=onset_ms, 
                duration_ms=96
            )
            
            # Feature extraction
            mel_spec = self.mel_extractor(window)
            
            # ONNX inference
            outputs = self.ort_session.run(None, {'input': mel_spec[np.newaxis, ...]})
            
            # Post-process
            event = self._classify_output(outputs, onset_ms)
            if event.confidence > 0.75:
                events.append(event)
        
        # Update state machines
        for event in events:
            self.rally_fsm.process(event)
            self.solo_fsm.process(event)
        
        return events
```

### 3.3 Deployment Targets

| Platform | Runtime | Expected Latency | Quantization |
|----------|---------|------------------|--------------|
| iOS (A17+) | CoreML | 15-25ms | INT8 |
| Android (SD8G3+) | NNAPI | 20-30ms | INT8 |
| Raspberry Pi 5 | ONNX Runtime | 40-60ms | INT8 |
| Edge TPU | TFLite | 10-20ms | INT8 |
| Desktop (GPU) | ONNX Runtime + CUDA | 5-15ms | FP16 |

### 3.4 Multi-Threading Strategy

```
Thread 1 (Audio Capture - RT Priority):
  - Capture audio from microphone
  - Feed to ring buffer
  - Trigger processing thread every 10ms

Thread 2 (Feature Extraction):
  - Compute mel spectrograms
  - Batch up to 3 windows for efficiency
  - Queue for inference

Thread 3 (Inference - GPU/Accelerator):
  - Run ONNX inference
  - Post-process outputs
  - Emit events

Thread 4 (State Machine + Score):
  - Consume events
  - Update FSMs
  - Send to LockN Score
```

---

## 4. Evaluation Framework & Acceptance Metrics

### 4.1 Performance Metrics

#### Event Detection (LockN Listen)
| Metric | Target | Acceptance Threshold |
|--------|--------|---------------------|
| Recall (paddle-hit) | >95% | >90% |
| Recall (table-bounce) | >92% | >85% |
| Precision (all events) | >90% | >85% |
| Onset accuracy (<10ms error) | >85% | >75% |
| False positive rate | <5% | <10% |
| Latency (p50) | <35ms | <50ms |
| Latency (p99) | <50ms | <75ms |

#### Event Classification (LockN Sound)
| Class | F1-Score Target | F1-Score Min |
|-------|-----------------|--------------|
| paddle-hit | >0.94 | >0.88 |
| table-bounce | >0.92 | >0.85 |
| floor-bounce | >0.90 | >0.82 |
| net-hit | >0.85 | >0.75 |
| spin detection (binary) | >0.88 | >0.80 |
| spin type (4-class) | >0.75 | >0.65 |

#### Rally Logic (LockN Score Integration)
| Scenario | Accuracy Target |
|----------|----------------|
| Standard rally end detection | >98% |
| Same-side double-bounce detection | >95% |
| Solo mode rally identification | >90% |
| Serve fault detection | >92% |
| Point attribution (which player) | >95% |

### 4.2 Evaluation Datasets

| Dataset | Purpose | Size | Held-out Rackets |
|---------|---------|------|------------------|
| dev-clean | Hyperparameter tuning | 2hr | CFG-01, CFG-05 |
| test-match | Match play scenarios | 1hr | CFG-03, CFG-07 |
| test-solo | Solo practice detection | 30min | CFG-04 |
| test-noisy | Real-world noise | 45min | All configs |
| test-adversarial | Edge cases | 20min | Synthetic configs |

### 4.3 Test Scenarios

```yaml
scenarios:
  - name: "Standard Rally"
    description: "Normal 4-8 shot rally with clear events"
    events: [paddle, table, paddle, table, paddle, floor]
    expected: "Point ends on floor bounce"
    
  - name: "Same-Side Double Bounce"
    description: "Double bounce on one side (rule violation)"
    events: [paddle, table, table, paddle]
    expected: "Point awarded to opponent after second bounce"
    
  - name: "Net Cord Serve"
    description: "Serve hits net but goes over (let)"
    events: [paddle, net, table]
    expected: "Detected as net event, point replayed"
    
  - name: "Solo Hit-Back"
    description: "Player hitting back to self"
    events: [paddle, table, paddle, table, paddle, table]
    constraints: "Player same throughout, no opponent paddle"
    expected: "Detected as solo mode, no scoring"
    
  - name: "Fast Exchange"
    description: "Close-to-table rapid fire rally"
    inter_event_ms: 80-120
    expected: "All events detected with >90% recall"
    
  - name: "Far Distance"
    description: "Chopping rally with slow high balls"
    inter_event_ms: 400-800
    expected: "Accurate event typing maintained"
```

### 4.4 Continuous Evaluation Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  New Data   │───▶│  Auto-Label │───▶│  Human      │
│  Capture    │    │  (Weak)     │    │  Validation │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Model      │◀───│  Performance│◀───│  Metrics    │
│  Update     │    │  Analysis   │    │  Compute    │
│  Decision   │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

---

## 5. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **R1: Similar acoustic signature for paddle-hit vs table-bounce** | High | High | Use high-frequency content (>4kHz) differentiation; multi-microphone spatial features; temporal context (rally state priors) |
| **R2: Multi-bounce edge cases (ball grazes table edge)** | Medium | Medium | Confidence thresholding with escalation to "uncertain" state; high-speed camera backup for disputed calls |
| **R3: Environmental noise in real venues** | High | Medium | Robust augmentation during training; adaptive noise floor estimation; voice activity detection to filter player vocalizations |
| **R4: Racket configuration variability** | Medium | High | Collect diverse training data across 9+ configurations; domain randomization; on-device fine-tuning capability |
| **R5: Solo mode vs match mode confusion** | Medium | High | Explicit mode detection using rally pattern analysis; player confirmation for ambiguous sequences |
| **R6: Latency regression on edge devices** | Medium | High | Continuous latency benchmarking in CI; quantized model variants by device tier; graceful degradation (skip spin detection if slow) |
| **R7: Concurrent events (two tables nearby)** | Low | High | Directional microphone requirement; optional microphone array for source separation; spatial filtering |
| **R8: Dataset bias (indoor club vs outdoor)** | Medium | Medium | Multi-venue data collection; environment classification head; adaptive preprocessing per environment |

---

## 6. Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Goals:** Establish data pipeline, baseline detection, and evaluation framework

| Week | Deliverable | Success Criteria |
|------|-------------|------------------|
| 1.1 | Data collection setup | Record 500+ labeled events across 3 racket configs |
| 1.2 | Baseline detector | Energy-peak detection >80% recall on paddle hits |
| 1.3 | Annotation tooling | JSON-LD schema validation, audacity integration |
| 1.4 | Test harness | Automated evaluation pipeline with 5 scenarios |
| 2.1 | Feature extraction | Real-time mel spectrogram + MFCC <10ms |
| 2.2 | Simple classifier | 2-class (paddle vs table) >85% F1 |
| 2.3 | Baseline integration | End-to-end pipeline with mock LockN Score |
| 2.4 | Evaluation report | Metrics on dev-clean dataset |

**Milestone Gate (End Week 2):**
- [ ] >80% recall on paddle-hit detection
- [ ] <50ms end-to-end latency on target hardware
- [ ] Baseline classification >85% F1

### Phase 2: Core System (Weeks 3-6)

**Goals:** Full event classification, rally state machine, and rule implementation

| Week | Deliverable | Success Criteria |
|------|-------------|------------------|
| 3.1 | Expanded dataset | 3000+ labeled events across all racket configs |
| 3.2 | Full classifier | 5-class surface detection >90% F1 |
| 3.3 | Spin detection v1 | Binary spin/no-spin >80% F1 |
| 3.4 | ONNX optimization | INT8 quantization, <20ms inference |
| 4.1 | Rally FSM | State machine handles standard rallies correctly |
| 4.2 | Same-side detection | Double-bounce detection >90% accuracy |
| 4.3 | LockN Score API | Stable event stream to scoring system |
| 4.4 | Solo mode FSM | Solo hit-back detection and handling |
| 5.1 | Noise robustness | >85% recall in 20dB SNR environments |
| 5.2 | Multi-platform | iOS + Android deployment |
| 5.3 | Edge case suite | 15+ test scenarios passing |
| 5.4 | Performance tuning | <35ms p50, <50ms p99 latency |
| 6.1 | Field testing | 10+ hours real match data collection |
| 6.2 | Model refinement | Incremental training with field data |
| 6.3 | Documentation | API docs, integration guide |
| 6.4 | Release candidate | Tagged v0.1.0, all acceptance criteria |

**Milestone Gate (End Week 6):**
- [ ] >90% F1 on surface classification
- [ ] Rally state machine >95% accuracy
- [ ] Same-side double-bounce detection >90%
- [ ] Solo mode support functional
- [ ] <35ms median latency on target devices
- [ ] Real-world test: 5 matches, >95% accurate point detection

---

## Appendix A: Research Sources

1. **Sony AI (2024-2025)** - "Sound-Based Spin Estimation in Table Tennis: Dataset and Real-Time Classification Pipeline" - Primary reference for detection pipeline
2. **Zhang et al. (2006)** - "Ball Hit Detection in Table Tennis Games Based on Audio Analysis" - Classic EPD + MFCC approach
3. **Gossard et al. (2024)** - arXiv:2409.11760 - CNN-based classification on mel spectrograms
4. **TensorFlow YAMNet** - MobileNetV1 audio event detection architecture reference
5. **ONNX Runtime Docs** - Edge inference optimization strategies
6. **ITTF Rulebook** - Official table tennis rules for rally logic implementation

---

## Appendix B: Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **Mel spectrogram over MFCC for surface classifier** | Preserves more frequency information critical for distinguishing contact surfaces |
| **Energy peak detection before CNN** | Reduces CNN inference load by 90%+; enables millisecond-accurate onset timing |
| **EfficientNet-B0 over YAMNet** | Better accuracy/compute trade-off for 5-class problem; pretrained ImageNet features transfer well to spectrograms |
| **ONNX Runtime over TFLite** | Better cross-platform support, CoreML/NNAPI integration, dynamic shapes for variable-length audio |
| **48kHz sampling** | Captures high-frequency content up to 24kHz critical for paddle-ball contact characterization |
| **Dual FSM (rally + solo)** | Clean separation of concerns; solo mode has fundamentally different rules and scoring |

---

*Document generated by Research Agent for LockN Sense strategic planning.*
