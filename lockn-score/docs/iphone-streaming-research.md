# iPhone 16 Pro → Local Server Streaming Research (LOC-125)

## Requirements Recap
- **4K@120fps or 1080p@240fps capability**
- **Low latency (target <100ms)**
- **Local Wi‑Fi**
- **Python/FFmpeg compatible**

> **Key capability note:** Apple lists **4K Dolby Vision recording up to 120 fps** on iPhone 16 Pro (Fusion camera). This confirms hardware/encoder support for 4K120 capture. (Apple Tech Specs)

## Options Comparison (summary)

| Option | Protocol/Stack | Max Capture (iPhone 16 Pro) | Typical Latency (LAN) | FFmpeg/Python Ingest | Pros | Cons |
|---|---|---|---|---|---|---|
| **Native iOS app (AVFoundation)** | Custom app + H.264/HEVC + UDP/SRT/WebRTC/RTMP | 4K120 supported; 1080p240 possible if format supports | **Potentially <100ms** with WebRTC/UDP | Yes (depends on protocol) | Full control, lowest latency possible | Requires iOS development
| **Larix Broadcaster** | RTMP / SRT / RTSP / NDI / WebRTC (app) | Depends on device; H.264/H.265 | RTMP: 1–3s; SRT: 200–800ms (tunable); **WebRTC: ~50–150ms** | Yes for RTMP/SRT/RTSP; WebRTC requires WebRTC server | Multi‑protocol, widely used, stable | Latency varies by protocol; WebRTC server needed for low‑latency
| **NDI HX Camera apps** | NDI HX | 1080p60 typical; 4K possible but heavy | **~80–200ms** on good LAN | Not native in FFmpeg; requires NDI SDK or NDI‑enabled FFmpeg build | Low latency on LAN, easy discovery | Bandwidth heavy; FFmpeg ingest needs NDI support
| **RTSP camera apps** | RTSP (H.264) | Usually 1080p30/60 | 200–800ms | Yes (FFmpeg RTSP) | Simple FFmpeg ingest | Many iOS RTSP apps are limited; latency higher than WebRTC/NDI
| **RTMP apps** | RTMP (H.264) | 1080p30/60 (app dependent) | 1–3s | Yes | Easy to implement (NGINX‑RTMP, FFmpeg) | Too high latency for target
| **USB tethering + Ethernet** | Any protocol over wired (Lightning/USB‑C + adapter) | Same as Wi‑Fi | Lower/consistent latency | Yes | Best reliability | Adds hardware, still protocol‑dependent

**Sources:** Apple iPhone 16 Pro tech specs (4K@120fps), Larix Broadcaster protocol support (SRT/RTMP/RTSP/NDI/WebRTC).

---

## 1. Native iOS Approaches (AVFoundation / custom app)
**Approach:** Build a custom iOS capture app using **AVFoundation**. Configure `AVCaptureSession`, select `AVCaptureDeviceFormat` with target resolution and frame rate, encode via **VideoToolbox** (H.264/HEVC), and transmit via **WebRTC** or **UDP/SRT**.

**Pros**
- Best shot at **<100ms** latency (especially with WebRTC/UDP)
- Full control over FPS, bitrate, keyframe interval, color space
- Can push metadata (timestamps) for sync

**Cons**
- Requires iOS development effort
- WebRTC stack integration needed for very low latency

**Notes**
- **4K120** capture is supported by hardware; not all formats support 240fps at 1080p in live modes (often restricted to slo‑mo recording). You’ll need to inspect `AVCaptureDeviceFormat.videoSupportedFrameRateRanges` on device to confirm.

---

## 2. Third‑Party Apps
### **Larix Broadcaster (Softvelum)**
- Supports **SRT, RTMP, RTSP, NDI, WebRTC** on iOS (single app, multi‑protocol)
- H.264/HEVC supported (HEVC premium)
- Best for quick testing and multi‑protocol evaluation

**Latency expectations** (varies):
- **WebRTC:** ~50–150ms LAN (best path to <100ms)
- **SRT:** 200–800ms depending on latency buffer settings
- **RTMP:** typically >1s (not suitable for target)

### **NDI HX Camera apps (NDI)**
- Very low latency on LAN, optimized for live production
- Requires **NDI SDK** or NDI‑enabled tools to ingest
- Often capped around 1080p60; 4K may be possible but heavy on Wi‑Fi

---

## 3. RTSP / RTMP Streaming
- **RTSP**: Simple to ingest with FFmpeg, but latency is moderate (200–800ms typical).
- **RTMP**: High latency (1–3s). Not suitable for <100ms.

---

## 4. WebRTC (Low‑Latency)
- Best overall choice for **sub‑100ms** on LAN.
- Requires a **WebRTC server** (e.g., mediasoup, Janus, Pion, WHIP/WHEP‑capable servers).
- Some apps (Larix) can publish WebRTC, or you can build a custom iOS WebRTC app.

**FFmpeg ingest:**
- FFmpeg doesn’t natively ingest WebRTC without extra components (WHIP/WHEP, GStreamer, or a WebRTC → RTP gateway).
- Typical workflow: **WebRTC → RTP** or **WebRTC → SRT** bridge → FFmpeg.

---

## 5. USB / Wired Fallback
- Use **USB‑C/Lightning → Ethernet** adapter to keep LAN transport but avoid Wi‑Fi jitter.
- Still use SRT/WebRTC/NDI, but with better stability and lower latency.

---

# Recommended Approach
**Recommended:** **Larix Broadcaster (WebRTC mode)** for immediate testing, then **custom iOS AVFoundation + WebRTC** for best control/latency.

**Why:**
- WebRTC is the only common path that consistently reaches **<100ms** on LAN.
- Larix allows fast validation with no custom iOS development.
- If Larix WebRTC latency is acceptable, keep it. If not, build custom AVFoundation app to reduce encoding latency and jitter.

---

# Implementation Notes (Practical)

### **WebRTC path (preferred)**
1. **Sender (iPhone):** Larix Broadcaster (WebRTC) or custom AVFoundation + WebRTC stack.
2. **Server:** WebRTC SFU (mediasoup/Janus/Pion) or WHIP endpoint.
3. **Processing:** Use a WebRTC → RTP/SRT gateway to feed FFmpeg/Python.

### **SRT path (fallback)**
- Set low latency buffers (50–200ms) and use UDP‑optimized network.
- Still likely >200ms latency overall.

### **NDI path**
- Use NDI tools or FFmpeg compiled with NDI SDK for ingestion.
- Often near‑real‑time if Wi‑Fi is strong.

---

# Latency Benchmarks (public/observed ranges)
*(Exact numbers depend on Wi‑Fi quality, device load, and encoder settings.)*

- **WebRTC (LAN):** ~50–150ms typical best‑case
- **NDI (LAN):** ~80–200ms (can be lower on wired)
- **SRT:** 200–800ms (buffer tunable)
- **RTSP:** 200–800ms
- **RTMP:** 1–3s

---

# Sources
- Apple iPhone 16 Pro Tech Specs — 4K Dolby Vision recording up to 120 fps
  - https://support.apple.com/en-bw/121031
- Larix Broadcaster — protocol support (SRT/RTMP/RTSP/NDI/WebRTC)
  - https://softvelum.com/larix/

---

## Next Steps (if desired)
- Validate if **1080p240** is supported in live capture via `AVCaptureDeviceFormat` on an actual iPhone 16 Pro.
- Test Larix WebRTC → local SFU with latency measurement using timestamps.
- If WebRTC ingest is a bottleneck, test **WebRTC → RTP gateway** feeding FFmpeg/Python.
