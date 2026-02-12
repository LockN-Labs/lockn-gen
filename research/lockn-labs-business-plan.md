# LockN Labs — Business Plan

**Confidential** | February 2026 | v2.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Company Overview](#2-company-overview)
3. [Market Opportunity](#3-market-opportunity)
4. [Product Architecture](#4-product-architecture)
5. [Vertical Expansion Flywheel](#5-vertical-expansion-flywheel)
6. [Product Roadmap](#6-product-roadmap)
7. [Go-to-Market Strategy](#7-go-to-market-strategy)
8. [Competitive Landscape & Moat Analysis](#8-competitive-landscape--moat-analysis)
9. [Business Model & Pricing](#9-business-model--pricing)
10. [Financial Projections](#10-financial-projections)
11. [Team & Operations](#11-team--operations)
12. [Risks & Mitigations](#12-risks--mitigations)
13. [Key Metrics & Milestones](#13-key-metrics--milestones)
14. [Long-Term Vision](#14-long-term-vision)

---

## 1. Executive Summary

**LockN Labs** (DBA of OneSun Labs LLC) is building a two-layer AI company: an **integrated local-first AI platform** that powers **vertical consumer and enterprise products** — starting with sports technology.

**The problem:** Today's AI agent builders face a fragmented landscape. Speech synthesis costs $330+/mo (ElevenLabs), avatar generation runs $24–499+/mo (HeyGen/Synthesia), and LLM inference carries per-token fees that scale unpredictably. Every capability is a separate vendor, a separate API, a separate bill. Privacy-sensitive users and organizations have no viable local alternative. Meanwhile, powerful AI perception technology sits locked in developer toolkits, never reaching consumers.

**The solution:** LockN Labs delivers two things:

1. **The LockN Platform** — a unified, local-first AI engine distributed through OpenClaw. Seven core capabilities (Brain, Speak, Listen, Look, Sense, Tune, Embody) run entirely on a single prosumer GPU, giving developers cloud-quality AI with complete privacy and zero per-use costs.

2. **Vertical Products** built on the platform — starting with **LockN Score**, an AI-powered sports analysis and automatic scoring system for ping pong and paddle sports, and **LockN Eval**, a custom model evaluation and benchmarking offering. The platform enables rapid creation of new vertical products at near-zero marginal cost.

**Traction:**
- LockN Speak MVP deployed with API running
- LockN Listen (Whisper) and Look (Qwen2.5-VL) deployed
- LockN Sense multimodal pipeline operational
- LockN Brain architecture designed with development tickets created
- Full stack proven on owned hardware (96GB VRAM RTX Pro 6000 Blackwell)

**Business model:** Multi-stream revenue. Free platform tier drives adoption via OpenClaw; Pro/Team subscriptions unlock power features (voice cloning, custom models, Embody). Vertical products (Score, future) carry separate consumer pricing. LockN Cloud captures non-GPU users. Enterprise gets on-prem deployment with SLAs.

**The bigger picture:** The platform is a machine for creating vertical AI products. Score proves the technology in sports; the same perception pipeline powers fitness, physical therapy, music practice, dance instruction, education, and security. Each new vertical is a new revenue stream on shared infrastructure — a company that can disrupt multiple markets in parallel with low overhead at rapid speed.

**Ask:** This plan outlines a bootstrapped, capital-efficient path to $1M+ ARR within 18–24 months, powered by the OpenClaw distribution channel, vertical product revenue, and near-zero infrastructure costs on owned hardware.

---

## 2. Company Overview

| | |
|---|---|
| **Legal Entity** | OneSun Labs LLC |
| **DBA** | LockN Labs |
| **Founded** | 2025 |
| **Location** | Johns Creek/Alpharetta, GA (Atlanta metro) |
| **Founder** | Sean Lachenberg |
| **Structure** | Solo founder + AI agent development team |

### Founder Profile

**Sean Lachenberg** — Principal-level individual contributor with 10+ years of engineering experience spanning utilities, defense, and healthcare sectors. Georgia Tech Computer Science graduate. Deep expertise in systems architecture, AI/ML infrastructure, and full-stack development.

Sean's cross-domain experience is a strategic asset: defense work brings security-first thinking, healthcare brings compliance awareness (HIPAA/SOC2), and utilities work brings reliability engineering. This combination is rare in the AI tooling space and directly informs LockN's product design.

### Infrastructure

LockN Labs operates on owned, high-performance hardware that eliminates cloud compute dependency:

| Component | Specification |
|-----------|--------------|
| CPU | AMD Threadripper Pro 32-core / 64-thread |
| GPU | NVIDIA RTX Pro 6000 Blackwell — **96GB VRAM** |
| RAM | 256GB DDR5 |
| Storage | 2× Samsung 9100 Pro 4TB NVMe (8TB total) |

**Why this matters:** The entire LockN stack runs simultaneously on this single workstation:

| Workload | VRAM Allocation |
|----------|----------------|
| LLM inference (Brain) | 23–57 GB |
| Text-to-speech (Speak) | 2–6 GB |
| Vision models (Look/Sense) | 12 GB |
| Avatar rendering (Embody) | 0–6 GB |
| **Total** | **37–81 GB of 96 GB** |

This means development, testing, and initial production serving all run at $0 marginal cost. Cloud infrastructure is additive revenue, not a prerequisite.

---

## 3. Market Opportunity

### Industry Context

The AI agent ecosystem is at an inflection point. Large language models have proven capable, but agents need more than text — they need voice, vision, embodiment, and orchestration. The market is shifting from "AI chatbots" to "AI agents that perceive, reason, and act."

Simultaneously, a counter-trend is emerging: **local AI**. Privacy regulations (GDPR, HIPAA, CCPA), cost concerns, and latency requirements are driving demand for on-premise and edge AI solutions. The availability of prosumer GPUs with 24–96GB VRAM has made local inference practical for the first time.

A third trend is equally important: **AI-powered consumer products**. The technology that powers developer tools can also power consumer experiences — sports scoring, fitness coaching, music instruction. The companies that own the platform and the products built on it capture value at both layers.

### Total Addressable Market (TAM)

**Global AI software market:** $150B by 2027 (Gartner, IDC estimates).

The segments relevant to LockN:

| Segment | 2026 Est. | 2028 Est. | Source/Basis |
|---------|-----------|-----------|--------------|
| AI speech & voice | $7.2B | $12.5B | Markets & Markets, Grand View Research |
| AI agent platforms | $5.8B | $14.2B | Gartner AI agent forecast |
| AI avatar/digital human | $2.1B | $5.8B | Emergen Research |
| AI fine-tuning/MLOps | $3.4B | $8.1B | Cognilytica, MLOps market reports |
| AI in sports technology | $3.2B | $7.5B | Grand View Research, sports analytics |
| **Combined relevant TAM** | **$21.7B** | **$48.1B** | |

### Serviceable Addressable Market (SAM)

LockN targets two intersecting markets:

1. **Developer AI tooling (local/hybrid):** ~$2.5B by 2027 — developers and small teams purchasing AI tooling for local deployment
2. **AI-powered sports & fitness technology:** ~$1.2B by 2027 — consumer and prosumer sports analysis tools

### Serviceable Obtainable Market (SOM)

**Year 1 realistic target:** $120K–$360K ARR
**Year 2 realistic target:** $600K–$1.8M ARR
**Year 3 realistic target:** $1.5M–$5M ARR

Basis: OpenClaw's user base is the primary funnel for platform revenue. Vertical products (Score) add direct consumer revenue on top.

Assuming OpenClaw reaches 50,000–100,000 active users by end of 2026 (consistent with growth trajectory of comparable frameworks like LangChain, CrewAI), and LockN captures 2–5% as free users, with 5–15% free-to-paid conversion:

| Metric | Conservative | Moderate | Aggressive |
|--------|-------------|----------|------------|
| OpenClaw active users (EOY 2026) | 30,000 | 60,000 | 100,000 |
| LockN free installs (2–5%) | 600 | 1,800 | 5,000 |
| Paid conversions (5–15%) | 30 | 180 | 750 |
| Avg. revenue/user/mo | $24 | $29 | $39 |
| **Monthly platform revenue (Dec 2026)** | **$720** | **$5,220** | **$29,250** |
| **+ Score consumer revenue** | **+$500** | **+$2,000** | **+$8,000** |
| **Annualized run rate** | **$14,640** | **$86,640** | **$447,000** |

These are conservative acquisition assumptions. The moderate scenario assumes LockN Speak becomes a "must-have" OpenClaw skill, creating pull for the broader suite, while Score builds its own consumer audience.

---

## 4. Product Architecture

LockN Labs' architecture has two distinct layers: a **Platform** of composable AI capabilities and **Products** built on that platform for specific markets. Each platform component is valuable standalone, but the integrated suite creates compounding value — and a competitive moat. Products demonstrate platform power while generating their own revenue streams.

### Platform Layer — The Engine

The platform provides the foundational AI capabilities that power everything LockN builds.

#### 4.1 LockN Brain — AI Orchestration

**What:** LLM orchestration layer implementing dual-process thinking (System 1 fast / System 2 slow), multi-agent routing, and retrieval-augmented generation (RAG).

**Status:** Architecture designed, Linear development tickets created.

**Key Features:**
- Dual-process cognition: fast responses for simple queries, deep reasoning for complex tasks
- Multi-agent routing: delegate subtasks to specialized agents
- RAG pipeline: integrate private knowledge bases without cloud exposure
- Model-agnostic: works with any local LLM (Qwen, Llama, Mistral, etc.)

**Why it matters:** Brain is the connective tissue. It decides when to speak, what to look at, how to reason. Every other LockN product is more valuable when orchestrated by Brain.

#### 4.2 LockN Speak — Text-to-Speech

**What:** Multi-engine TTS with voice cloning, emotion control, and streaming output.

**Status:** ✅ MVP deployed, API running (Chatterbox engine). FishAudio S1-mini integration planned.

**Key Features:**
- Multiple TTS engines (Chatterbox live, FishAudio S1-mini planned)
- Voice cloning from short audio samples
- Emotion and prosody control
- OpenAI-compatible API endpoint
- Streaming audio output for real-time applications

**Why it matters:** Speak is the fastest path to revenue. Voice is the most emotionally compelling AI capability, and the local advantage (unlimited generation, no per-character fees) is immediately obvious vs. ElevenLabs' $330+/mo pricing.

#### 4.3 LockN Listen — Speech-to-Text

**What:** Audio transcription and event detection using Whisper.

**Status:** ✅ Deployed (Whisper).

**Key Features:**
- Real-time and batch transcription
- Multi-language support
- Speaker diarization
- Audio event detection (doorbell, alarm, speech, music)

#### 4.4 LockN Look — Vision Analysis

**What:** Visual question answering, OCR, and scene description.

**Status:** ✅ Deployed (Qwen2.5-VL).

**Key Features:**
- Image and video analysis
- Document OCR and understanding
- Visual QA (ask questions about what the camera sees)
- Scene description for accessibility

#### 4.5 LockN Sense — Multimodal Perception

**What:** Unified perception layer that combines Look (vision) and Listen (audio) signals into coherent multimodal understanding.

**Status:** ✅ Components deployed and operational.

**Key Features:**
- Visual scene understanding via Qwen2.5-VL
- Audio event detection and classification
- Multi-sensor fusion combining visual and audio signals
- Webhook triggers for detected events
- Foundation for vertical products (Score, future applications)

**Why it matters:** Sense is the key enabler for vertical products. By combining what the system *sees* and *hears*, Sense powers applications that require real-world awareness — sports analysis, security, accessibility, and more.

#### 4.6 LockN Tune — Fine-Tuning Pipeline

**What:** User-friendly model customization for LLMs and TTS models.

**Status:** Planned (8–12 week MVP).

**Key Features:**
- Guided fine-tuning workflow (no ML expertise required)
- LoRA/QLoRA for efficient training on consumer hardware
- TTS voice fine-tuning for custom voice creation
- Model evaluation and comparison (integrates with Eval)

#### 4.7 LockN Embody — Animated Avatars

**What:** Emotion-aware, lip-synced talking head avatars for agent embodiment.

**Status:** Research complete, implementation planned.

**Key Features:**
- Photo-realistic avatar generation from single photo
- Real-time lip sync with LockN Speak output
- Emotion-driven facial expressions
- Browser-based rendering (TalkingHead 3D)
- Customizable appearance and personality

**Why it matters:** Embodiment transforms agents from text boxes into characters. This is the premium differentiator — no competitor offers integrated local thinking + speaking + embodiment.

### Product Layer — Built on the Platform

Products are market-facing applications built on platform capabilities. They generate their own revenue while proving and marketing the platform.

#### 4.8 LockN Score — AI Sports Analysis & Scoring

**What:** AI-powered sports analysis and automatic scoring system. A **consumer product** that uses the Sense platform (Look + Listen) to watch, understand, and score sports matches in real-time.

**Status:** In development. Built on deployed Sense infrastructure.

**Starting market:** Ping pong / table tennis — a sport with clear scoring events, defined court boundaries, and a massive global player base (300M+ recreational players worldwide).

**Key Features:**
- Real-time match scoring from camera feed (no manual input)
- Rally analysis: speed, spin, placement tracking
- Player statistics and improvement tracking over time
- Match history and leaderboards
- Social sharing and community features
- Extensible to paddle sports (pickleball, padel, badminton) and beyond

**Why it matters:** Score is the proof-of-concept for the vertical expansion strategy. It takes platform technology (Sense) and packages it into a consumer product with its own distribution, pricing, and brand. Success here validates the entire flywheel.

**Revenue model:** Freemium mobile/web app. Free basic scoring; premium analytics, coaching insights, and league features via subscription ($4.99–$14.99/mo).

#### 4.9 LockN Eval — Model Evaluation & Benchmarking

**What:** Custom model and system evaluation offering. The platform's quality scoring and benchmarking tool, also available as a standalone product for teams that need eval pipelines.

**Status:** In development.

**Key Features:**
- Automated model quality assessment
- A/B comparison between models
- TTS quality metrics (MOS estimation, intelligibility)
- Custom benchmark and eval pipeline creation
- Quality regression detection
- Report generation for compliance and audit

**Why it matters:** Eval closes the platform's feedback loop — deploy → measure → tune → redeploy. As a standalone product, it serves ML teams who need structured evaluation regardless of whether they use the rest of the LockN platform.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PRODUCT LAYER                        │
│  ┌─────────────────────┐  ┌──────────────────────────┐  │
│  │    LockN Score       │  │      LockN Eval          │  │
│  │  (Sports Analysis)   │  │  (Model Benchmarking)    │  │
│  │  Consumer Product    │  │  Developer/Enterprise    │  │
│  └─────────┬───────────┘  └──────────┬───────────────┘  │
├────────────┼─────────────────────────┼──────────────────┤
│            │      PLATFORM LAYER     │                  │
│  ┌─────────▼─────────────────────────▼───────────────┐  │
│  │              LockN Brain (Orchestration)           │  │
│  ├───────┬───────┬───────┬───────┬───────┬───────────┤  │
│  │ Speak │Listen │ Look  │ Sense │Embody │   Tune    │  │
│  │ (TTS) │ (STT) │ (VQA) │(Multi)│(Avtr) │(Fine-tune)│  │
│  └───────┴───────┴───────┴───────┴───────┴───────────┘  │
└─────────────────────────────────────────────────────────┘
```

Brain orchestrates all platform capabilities. Eval measures them. Tune improves them. Score packages them for consumers. The flywheel is: **build platform → launch product → prove technology → expand to new verticals**.

---

## 5. Vertical Expansion Flywheel

### The Insight

LockN's platform architecture enables something powerful: **rapid creation of vertical AI products at near-zero marginal cost**. Once the Sense pipeline (Look + Listen) can understand one physical activity, adapting it to another is primarily a training data and UI problem — not an infrastructure rebuild.

### The Flywheel

```
Platform capabilities mature
        ↓
Launch vertical product (Score → ping pong)
        ↓
Prove technology in market, collect training data
        ↓
Adapt to adjacent vertical (paddle sports → fitness → therapy)
        ↓
Each vertical = new revenue stream, same infrastructure
        ↓
Revenue funds platform improvement
        ↓
Better platform enables more verticals, faster
        ↓
(repeat)
```

### Expansion Roadmap

**Starting point:** LockN Score for ping pong — clear scoring events, defined boundaries, large global player base.

**Near-term expansions (same Sense pipeline, adapted models):**

| Vertical | Technology Reuse | New Revenue Stream |
|----------|-----------------|-------------------|
| Pickleball / Padel | Same ball tracking, court detection, scoring logic | Sports scoring & analytics |
| Badminton / Tennis | Same motion tracking, rally analysis | Sports scoring & analytics |
| Fitness / Exercise | Pose estimation, rep counting, form analysis | Personal training / coaching |
| Physical Therapy | Movement analysis, range-of-motion tracking | Healthcare / rehab |
| Music Practice | Audio analysis (Listen), performance scoring | Education / arts |
| Dance Instruction | Motion analysis (Look), rhythm sync (Listen + Look) | Education / performing arts |
| Education | Visual + audio understanding, engagement detection | EdTech |
| Security | Scene analysis, anomaly detection, audio alerts | Commercial / residential |

**Key insight:** Each vertical listed above uses the **same core Sense technology** — combining what the system sees (Look) and hears (Listen) into actionable understanding. The marginal cost of entering a new vertical is primarily:
- Domain-specific training data collection
- Vertical-specific UI/UX
- Market-specific go-to-market

The platform infrastructure, model serving, and multimodal fusion are already built and paid for.

### The Strategic Narrative

> LockN Labs is building a machine that can disrupt multiple verticals in parallel with low overhead at rapid speeds.

This is not a single-product company. It's a **platform company** that happens to launch products. The platform is the moat; the products are the revenue. Every successful vertical proves the platform, attracts developers, and funds the next expansion.

**Comparison:** Think of how AWS's infrastructure enables rapid service launches, or how Stripe's payment platform enables fintech products. LockN's AI perception platform enables rapid creation of "AI that watches and understands the physical world" products across any domain.

---

## 6. Product Roadmap

### Phase 1: Foundation (Q1 2026 — Now through March)

**Theme:** Ship what we have, establish OpenClaw presence.

| Milestone | Target Date | Product |
|-----------|------------|---------|
| LockN Speak landing page live | Feb 2026 | Speak |
| FishAudio S1-mini integration | Feb–Mar 2026 | Speak |
| Voice persona system | Mar 2026 | Speak |
| OpenAI-compatible TTS API | Mar 2026 | Speak |
| Free tier published on OpenClaw/ClawHub | Mar 2026 | Speak, Listen, Look |
| LockN Brain MVP (dual-process) | Mar 2026 | Brain |
| LockN Eval v0.1 (basic eval) | Mar 2026 | Eval |
| LockN Score prototype (ping pong scoring) | Mar 2026 | Score |

**Key result:** First external users running LockN skills via OpenClaw. Score prototype demonstrating Sense technology in consumer context.

### Phase 2: Monetization (Q2 2026 — April through June)

**Theme:** Convert free users to paid. Ship premium features. Launch Score beta.

| Milestone | Target Date | Product |
|-----------|------------|---------|
| Pro tier launch ($19–29/mo) | Apr 2026 | Platform |
| Voice cloning (Pro feature) | Apr 2026 | Speak |
| Multi-agent orchestration | May 2026 | Brain |
| LockN Embody Phase 1 (TalkingHead 3D) | May 2026 | Embody |
| LockN Sense unified API | Jun 2026 | Sense |
| LockN Score public beta | Jun 2026 | Score |
| Payment infrastructure (Stripe) | Apr 2026 | Platform |

**Key result:** First paying platform customers. Score beta generating consumer interest and training data.

### Phase 3: Expansion (Q3 2026 — July through September)

**Theme:** Higher-value tiers. Suite integration. Score launch. Vertical expansion begins.

| Milestone | Target Date | Product |
|-----------|------------|---------|
| Team tier launch ($49–99/mo) | Jul 2026 | Platform |
| LockN Tune MVP (LoRA fine-tuning) | Jul–Aug 2026 | Tune |
| Custom Tune'd voice models | Aug 2026 | Speak + Tune |
| Branded avatar system | Aug 2026 | Embody |
| LockN Brain advanced RAG | Sep 2026 | Brain |
| Eval v1.0 (comprehensive benchmarks) | Sep 2026 | Eval |
| LockN Score v1.0 launch | Aug 2026 | Score |
| Score expansion: pickleball support | Sep 2026 | Score |

**Key result:** ARPU increase via Team tier. Score generating consumer revenue. First vertical expansion validates flywheel.

### Phase 4: Scale (Q4 2026 — October through December)

**Theme:** Enterprise readiness. Cloud tier. Vertical expansion acceleration.

| Milestone | Target Date | Product |
|-----------|------------|---------|
| Enterprise tier (custom pricing) | Oct 2026 | Platform |
| LockN Cloud beta (hosted offering) | Oct–Nov 2026 | Platform |
| HIPAA/SOC2 compliance documentation | Nov 2026 | Platform |
| White-label avatar system | Nov 2026 | Embody |
| On-premise deployment packaging | Dec 2026 | Platform |
| Score expansion: padel, badminton | Nov 2026 | Score |
| Fitness/exercise vertical exploration | Dec 2026 | New Product |

**Key result:** Enterprise pipeline. Cloud tier as margin accelerator. Multiple Score verticals live. Fitness vertical in prototype.

### 2027 Horizon

- LockN Cloud general availability
- Score expansion to 5+ sports
- Fitness / physical therapy vertical launch
- Mobile SDK (on-device inference for phones)
- Partner integrations beyond OpenClaw
- International expansion (multilingual voice/avatar)
- Potential seed round if growth warrants acceleration

---

## 7. Go-to-Market Strategy

### Primary Channel: OpenClaw Ecosystem (Platform)

OpenClaw is both the distribution platform and the product context for the LockN Platform. This is not a marketplace listing — it's deep integration.

**Why OpenClaw:**
1. **Built-in audience:** Every OpenClaw user needs agent capabilities (voice, vision, orchestration)
2. **Zero CAC for free tier:** Plugin discovery is organic within the framework
3. **Sticky integration:** Once users build agents with LockN skills, switching cost is high
4. **Aligned incentives:** OpenClaw benefits from a richer plugin ecosystem

**Platform Funnel:**

```
OpenClaw user discovers LockN skill
        ↓
Installs free tier (Speak/Listen/Look)
        ↓
Hits free tier limits or wants premium features
        ↓
Converts to Pro ($19-29/mo)
        ↓
Builds team workflows → Team tier ($49-99/mo)
        ↓
Organization adopts → Enterprise (custom)
```

### Secondary Channel: Direct Consumer (Products)

Vertical products like Score have their own GTM, independent of OpenClaw:

**Score GTM:**
- App store distribution (iOS/Android/Web)
- Content marketing: viral ping pong scoring videos on TikTok/YouTube/Instagram
- Community: ping pong clubs, leagues, recreation centers
- Partnerships: table tennis equipment brands, tournament organizers
- Word of mouth: players sharing match results and stats

### Tertiary Channels

| Channel | Role | Timeline |
|---------|------|----------|
| GitHub / open-source community | Credibility, contributions, developer trust | Ongoing |
| Technical blog / tutorials | SEO, thought leadership, "local AI" keyword capture | Q1 2026+ |
| YouTube / demo videos | Show don't tell — avatar demos, voice demos, Score demos | Q2 2026+ |
| Developer conferences | In-person credibility (Atlanta tech scene) | Q3 2026+ |
| LockN Cloud landing page | Capture non-OpenClaw users who want hosted | Q4 2026+ |
| Sports/fitness influencers | Score product awareness in consumer market | Q3 2026+ |

### Content Strategy

**Core narratives:**

1. **Platform:** "Your AI agent deserves a voice, a face, and a brain — and it should all run on YOUR hardware."
2. **Products:** "AI that watches your game, scores it automatically, and helps you improve."

Content pillars:
1. **Local AI advocacy** — privacy, cost, control arguments
2. **Technical deep-dives** — how dual-process thinking works, VRAM optimization, etc.
3. **Demo-driven marketing** — short videos showing the integrated stack in action
4. **Score viral content** — impressive real-time scoring clips, player reaction videos
5. **Community spotlights** — showcase what users build with LockN

### Pricing Psychology

The free platform tier is generous enough to be genuinely useful (3 voices, 10K chars/mo, basic vision). This builds goodwill and habit. Pro pricing ($19–29/mo) is positioned against the alternative: ElevenLabs alone costs $330+/mo for comparable capabilities. The value proposition is obvious.

Score's consumer pricing ($4.99–$14.99/mo) is positioned as trivially cheap compared to the value — automatic, reliable match scoring that replaces manual scorekeeping and provides analytics no human scorer could.

---

## 8. Competitive Landscape & Moat Analysis

### Direct Competitors

**Platform competitors:**

| Competitor | Offering | Pricing | Local Option | Integrated Stack |
|-----------|---------|---------|-------------|-----------------|
| **ElevenLabs** | TTS, voice cloning, conversational AI | $5–$330+/mo | ❌ Cloud-only | Partial (voice only) |
| **HeyGen** | AI avatars, video generation | $24–$499+/mo | ❌ Cloud-only | ❌ Avatar only |
| **Synthesia** | AI video avatars | $22–$499+/mo | ❌ Cloud-only | ❌ Avatar only |
| **OpenAI** | TTS, STT, vision, LLM | Per-token | ❌ Cloud-only | Partial (API-level) |
| **Coqui/Mozilla TTS** | Open-source TTS | Free | ✅ | ❌ TTS only |
| **Ollama** | Local LLM runtime | Free | ✅ | ❌ LLM only |

**Score competitors:**

| Competitor | Offering | Pricing | AI-Powered | Multi-Sport |
|-----------|---------|---------|------------|-------------|
| **SwingVision** | Tennis analysis | $9.99–$29.99/mo | Partial | Tennis only |
| **Manual scorekeeping apps** | Score tracking | Free–$4.99 | ❌ | Various |
| **Custom hardware systems** | Ball tracking | $5K–$50K+ | ✅ | Single sport |

**Score's advantage:** No competitor offers AI-powered automatic scoring from a standard camera feed at consumer pricing across multiple paddle sports.

### Competitive Positioning

No competitor offers what LockN offers: **a fully integrated, local-first platform spanning orchestration, voice, vision, perception, avatars, fine-tuning, and evaluation — PLUS vertical consumer products built on that platform.**

```
                    Integrated ←──────────→ Point Solution
                         │                       │
            Local   LockN Labs ●                  │  Ollama, Coqui
                         │                        │
                         │                        │
           Cloud         │        OpenAI ●        │  ElevenLabs, HeyGen
                         │                        │
```

### Moat Analysis

**1. Integration Depth (Strong — widens over time)**
Each new LockN platform component makes the others more valuable. Brain orchestrates Speak, which lip-syncs Embody, which is evaluated by Eval, which is improved by Tune. Competitors would need to build or acquire 7+ platform components to replicate this.

**2. Platform + Product Flywheel (Strong — unique position)**
Owning both the platform and the products built on it creates a compounding advantage. Products generate revenue and training data; platform improvements make products better; better products attract more users to the platform. No pure-platform or pure-product competitor can replicate this cycle.

**3. OpenClaw Native Position (Moderate — first-mover)**
Being the first comprehensive agent skill suite on OpenClaw creates switching costs. Users build workflows around LockN APIs. Early presence means early mindshare.

**4. Local-First Architecture (Moderate — philosophical moat)**
Cloud competitors would need to fundamentally restructure their business model to compete on local deployment. Their economics depend on per-use pricing; ours depends on subscriptions for premium features.

**5. Zero Marginal Cost (Strong — structural advantage)**
Running on owned hardware means every additional user (local tier) costs us nothing. Cloud competitors' COGS scales with usage. This allows aggressive free tier and rapid iteration.

**6. Vertical Expansion Speed (Strong — accelerating)**
Once the Sense platform is proven in one vertical, entering the next requires domain data and UI — not infrastructure. Each vertical entered increases the moat because competitors must replicate both the platform AND the vertical expertise.

---

## 9. Business Model & Pricing

### Revenue Model: Platform Subscriptions + Vertical Products + Cloud

**Revenue streams:**

1. **Platform subscriptions** (Free/Pro/Team) — primary platform revenue via OpenClaw
2. **Vertical product revenue** (Score, future products) — consumer/prosumer subscriptions
3. **LockN Cloud** (hosted inference) — margin play for non-GPU users
4. **Enterprise** (on-prem deployment, SLAs, compliance) — high-value contracts
5. **Marketplace commissions** (community-created voices, avatars, models) — future

### Platform Pricing Tiers

| Feature | Free | Pro ($24/mo) | Team ($74/mo) | Enterprise |
|---------|------|-------------|---------------|------------|
| **Brain** | 1 agent, basic routing | Multi-agent, dual-process thinking | Custom models, priority routing | Dedicated instances, SLA |
| **Speak** | 3 voices, 10K chars/mo | Unlimited chars, voice cloning | Custom Tune'd voices, SSML | On-prem, white-label |
| **Listen** | Basic transcription | Real-time + diarization | Custom vocabulary | Compliance-ready |
| **Look** | Basic VQA | Full pipeline, batch processing | Custom classifiers | HIPAA-compliant |
| **Sense** | Basic vision + audio | Full multimodal, webhooks | Custom event classifiers | Edge deployment |
| **Embody** | — | Custom photo-real avatar | Branded avatars, gestures | White-label SDK |
| **Tune** | — | Community models | Custom fine-tuning jobs | Dedicated training infra |
| **Eval** | Basic metrics | Full benchmarking suite | Custom eval pipelines | Audit-grade reports |
| **Support** | Community | Email, 48h response | Priority, 12h response | Dedicated, 2h response |

**Free tier strategy:** Generous enough to drive adoption through OpenClaw. Users get real value at zero cost, building habit and community. The free tier IS the marketing — it creates advocates who upgrade when they need power features.

*Mid-point pricing used for projections: Pro at $24/mo, Team at $74/mo.*

### Vertical Product Pricing

| Product | Free Tier | Premium | Notes |
|---------|-----------|---------|-------|
| **LockN Score** | Basic match scoring (3 matches/day) | $4.99–$14.99/mo: unlimited matches, analytics, coaching, leagues | Can bundle with platform Pro |
| **Future verticals** | TBD per market | TBD | Separate pricing per vertical |

### LockN Cloud Pricing

For users without GPU hardware who want platform access:

| Tier | Price | Includes |
|------|-------|----------|
| Cloud Basic | $9.99/mo | Hosted inference for Speak, Listen, Look |
| Cloud Pro | $34.99/mo | All platform features, hosted |
| Cloud Team | $99.99/mo | Team features, priority compute |

Cloud is a pure margin play — the platform is already built; cloud pricing covers compute costs plus healthy margin.

### Unit Economics

| Metric | Value | Notes |
|--------|-------|-------|
| CAC (free → paid) | ~$0 | Organic via OpenClaw discovery |
| CAC (paid acquisition) | $20–50 | Content marketing, SEO |
| CAC (Score consumer) | $5–15 | Viral content, app store |
| Monthly COGS (local user) | ~$0 | Runs on user's hardware |
| Monthly COGS (cloud user) | $5–15 | GPU compute per user |
| Gross margin (local) | ~95% | Platform costs only |
| Gross margin (cloud) | 60–75% | Compute + platform |
| Target LTV (Pro) | $288–576 | 12–24 month retention |
| Target LTV (Team) | $888–1,776 | 12–24 month retention |
| Target LTV (Score) | $60–180 | 12+ month retention |
| LTV:CAC ratio | >10:1 | Exceptional due to organic acquisition |

---

## 10. Financial Projections

### Assumptions

- OpenClaw user growth: 20–50K users by EOY 2026, 80–200K by EOY 2027
- LockN skill discovery rate: 2–5% of OpenClaw users install a LockN skill
- Free-to-paid conversion: 5–10% (industry benchmark for developer tools: 2–5%; we estimate higher due to clear value prop vs. expensive cloud alternatives)
- Monthly churn: 5% (Pro), 3% (Team), 1% (Enterprise)
- Cloud tier launches Q4 2026, adds 20–40% to user base
- Score consumer revenue begins Q3 2026, grows independently of platform
- No external funding assumed; all growth is organic/bootstrapped

### Conservative Scenario

*Assumes slow OpenClaw growth, lower conversion, higher churn.*

| Quarter | Free Users | Paid (Pro) | Paid (Team) | Score Subs | MRR | ARR |
|---------|-----------|------------|-------------|-----------|-----|-----|
| Q1 2026 | 50 | 0 | 0 | 0 | $0 | $0 |
| Q2 2026 | 200 | 10 | 0 | 0 | $240 | $2,880 |
| Q3 2026 | 500 | 35 | 3 | 50 | $1,562 | $18,744 |
| Q4 2026 | 900 | 70 | 8 | 150 | $3,772 | $45,264 |
| Q1 2027 | 1,400 | 120 | 15 | 300 | $6,990 | $83,880 |
| Q2 2027 | 2,000 | 200 | 30 | 600 | $13,020 | $156,240 |
| Q3 2027 | 2,800 | 300 | 50 | 1,000 | $20,900 | $250,800 |
| Q4 2027 | 3,500 | 400 | 80 | 1,500 | $30,520 | $366,240 |

**Year 1 total revenue:** ~$67K | **Year 2 total revenue:** ~$366K

*Score subscribers at avg. $10/mo.*

### Moderate Scenario

*Assumes healthy OpenClaw growth, good product-market fit, Score gains traction.*

| Quarter | Free Users | Paid (Pro) | Paid (Team) | Enterprise | Score Subs | MRR | ARR |
|---------|-----------|------------|-------------|-----------|-----------|-----|-----|
| Q1 2026 | 150 | 0 | 0 | 0 | 0 | $0 | $0 |
| Q2 2026 | 600 | 40 | 0 | 0 | 0 | $960 | $11,520 |
| Q3 2026 | 1,500 | 120 | 10 | 0 | 200 | $5,620 | $67,440 |
| Q4 2026 | 3,000 | 250 | 30 | 1 | 600 | $14,220 | $170,640 |
| Q1 2027 | 5,000 | 450 | 60 | 2 | 1,500 | $30,440 | $365,280 |
| Q2 2027 | 8,000 | 750 | 100 | 4 | 3,000 | $56,400 | $676,800 |
| Q3 2027 | 12,000 | 1,100 | 160 | 6 | 5,000 | $88,640 | $1,063,680 |
| Q4 2027 | 16,000 | 1,500 | 250 | 10 | 8,000 | $134,500 | $1,614,000 |

**Year 1 total revenue:** ~$250K | **Year 2 total revenue:** ~$1.6M

*Enterprise assumed at $2,000/mo average. Score subscribers at avg. $10/mo.*

### Aggressive Scenario

*Assumes LockN becomes a breakout OpenClaw skill, Score goes viral in sports communities.*

| Quarter | Free Users | Paid (Pro) | Paid (Team) | Enterprise | Score Subs | MRR | ARR |
|---------|-----------|------------|-------------|-----------|-----------|-----|-----|
| Q1 2026 | 400 | 0 | 0 | 0 | 0 | $0 | $0 |
| Q2 2026 | 2,000 | 150 | 5 | 0 | 0 | $3,970 | $47,640 |
| Q3 2026 | 6,000 | 500 | 40 | 1 | 1,000 | $26,960 | $323,520 |
| Q4 2026 | 12,000 | 1,200 | 100 | 3 | 4,000 | $82,200 | $986,400 |
| Q1 2027 | 20,000 | 2,500 | 200 | 8 | 10,000 | $190,800 | $2,289,600 |
| Q2 2027 | 30,000 | 4,000 | 350 | 15 | 18,000 | $331,900 | $3,982,800 |
| Q3 2027 | 40,000 | 5,500 | 500 | 25 | 28,000 | $499,000 | $5,988,000 |
| Q4 2027 | 50,000 | 7,000 | 700 | 40 | 40,000 | $699,800 | $8,397,600 |

**Year 1 total revenue:** ~$986K | **Year 2 total revenue:** ~$8.4M

### Expense Structure (All Scenarios)

| Category | Monthly (Q1-Q2) | Monthly (Q3-Q4) | Notes |
|----------|----------------|-----------------|-------|
| Infrastructure (owned HW) | $0 | $0 | Already purchased, depreciation only |
| Cloud hosting (website, API) | $50 | $200 | Minimal; local-first |
| Cloud GPU (LockN Cloud) | $0 | $500–2,000 | Scales with cloud tier adoption |
| SaaS tools | $100 | $200 | Stripe, monitoring, analytics |
| Marketing/content | $0 | $200–500 | Content creation, SEO tools |
| App store fees (Score) | $0 | $100–500 | Apple/Google 15–30% on consumer subs |
| Legal/accounting | $100 | $200 | LLC maintenance, tax prep |
| **Total monthly burn** | **$250** | **$1,400–3,600** | |

**Breakeven (moderate scenario):** Q3 2026 (~$5,600 MRR vs. ~$2,000 expenses)

The bootstrapped model means profitability comes early. There is no venture-scale burn to outrun.

### Path to $1M ARR

| Scenario | $1M ARR Target |
|----------|---------------|
| Conservative | Q2–Q3 2028 |
| Moderate | Q3 2027 |
| Aggressive | Q4 2026 |

The addition of Score's consumer revenue accelerates every scenario by 2–3 quarters compared to platform-only projections.

---

## 11. Team & Operations

### Current Team

**Sean Lachenberg — Founder, CEO, Principal Engineer**
- Owns strategy, architecture, product decisions, and key partnerships
- Hands-on engineering for critical path items
- 10+ years principal-level IC experience

**AI Agent Development Team**
LockN Labs operates with an AI-augmented development model where autonomous AI agents handle 80%+ of implementation work:

- **Code generation and implementation** — AI agents write, test, and iterate on code
- **Documentation and content** — Technical writing, API docs, tutorials
- **Testing and evaluation** — Automated test generation and benchmark running
- **DevOps and deployment** — Infrastructure management, CI/CD

This is not aspirational — it's the current operating model. The LockN products themselves are being built using this approach, on the same infrastructure they'll run on.

**Why this works:**
- Solo founder capacity is multiplied 5–10× by AI agents
- 96GB VRAM means local AI agents run at zero marginal cost
- The agents use LockN products (dogfooding), creating a tight feedback loop
- No hiring overhead, no coordination cost, no equity dilution

### Hiring Plan

Near-term (2026): No hires planned. AI agent productivity is sufficient.

Growth triggers for first hire:
- MRR > $15K sustained (can fund a contractor)
- Specific skill gap AI can't fill (e.g., enterprise sales)
- Community management exceeds founder bandwidth

First hires (when ready):
1. Developer advocate / community manager
2. Enterprise sales (commission-based)
3. Part-time designer (brand, landing pages)

### Operations Model

```
Sean (Strategy + Architecture + Product)
  ├── AI Agents (Implementation, 80%+ of dev work)
  ├── OpenClaw Community (Feedback, bug reports, feature requests)
  └── Automated Infrastructure (CI/CD, monitoring, deployment)
```

Capital-efficient. No office. No payroll. Revenue drops almost entirely to the bottom line until deliberate scaling decisions are made.

---

## 12. Risks & Mitigations

### Technical Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Model quality falls behind cloud providers | Medium | Medium | Leverage open-source model improvements (Qwen, Llama, etc.); Tune allows custom optimization; Eval monitors quality gaps |
| GPU hardware failure | High | Low | RAID NVMe storage; daily backups; replacement GPU available in 1–2 days via pro channel |
| VRAM insufficient for future models | Medium | Medium | Quantization techniques; CPU offloading for overflow; cloud tier as fallback; second GPU when justified |
| Score computer vision accuracy insufficient | Medium | Medium | Start with constrained environment (overhead camera, standard table); improve with collected data; Tune pipeline for rapid iteration |

### Market Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Cloud providers add local deployment options | High | Medium | Our integration depth is the moat, not just "runs locally"; 12+ months ahead on integrated stack |
| OpenClaw growth stalls or pivots | High | Low | Diversify distribution (direct, GitHub, website); Score has independent distribution; maintain framework-agnostic core |
| Open-source competitors replicate the stack | Medium | Medium | Execution speed; integration quality; community relationships; vertical products create value competitors can't copy by cloning code |
| AI agent market hype collapses | Medium | Low | Products have standalone value (TTS, STT, vision, Score) regardless of "agent" framing |
| Score faces established sports tech competition | Medium | Medium | Differentiate on price (consumer vs. $5K+ hardware), multi-sport flexibility, and platform integration |

### Business Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Solo founder burnout / capacity | High | Medium | AI agents handle implementation; focus founder time on highest-leverage decisions; maintain sustainable pace |
| Slow free-to-paid conversion | Medium | Medium | Generous free tier builds habit; clear value cliff at limits; A/B test pricing and limits |
| Enterprise sales cycle too long for solo founder | Medium | High | Delay enterprise until inbound demand; focus on self-serve Pro/Team tiers first |
| Vertical expansion spreads focus too thin | Medium | Medium | Disciplined sequencing; only expand after current vertical proves unit economics; platform handles shared infrastructure |

### Regulatory Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|------------|
| Voice cloning regulation | Medium | Medium | Consent-based cloning only; clear terms of service; local deployment means user responsibility |
| AI content labeling requirements | Low | Medium | Support metadata/watermarking in generated content |
| Data privacy regulation changes | Low | Medium | Local-first positioning is inherently privacy-compliant |

---

## 13. Key Metrics & Milestones

### North Star Metrics

1. **Monthly active LockN platform users on OpenClaw** — measures distribution reach and product stickiness
2. **LockN Score monthly active users** — measures consumer product traction

### Tracking Dashboard

| Category | Metric | Target (Q2 2026) | Target (Q4 2026) | Target (Q4 2027) |
|----------|--------|-------------------|-------------------|-------------------|
| **Acquisition** | OpenClaw skill installs (cumulative) | 500 | 3,000 | 16,000 |
| **Activation** | Monthly active platform users | 200 | 1,500 | 8,000 |
| **Revenue** | Platform MRR | $500 | $5,000 | $50,000 |
| **Revenue** | Score MRR | $0 | $3,000 | $40,000 |
| **Revenue** | Total MRR | $500 | $8,000 | $90,000 |
| **Revenue** | Paid subscribers (platform) | 20 | 200 | 2,000 |
| **Revenue** | Score subscribers | 0 | 400 | 5,000 |
| **Conversion** | Free → Pro rate | 5% | 8% | 10% |
| **Retention** | Monthly churn (Pro) | <8% | <5% | <4% |
| **Engagement** | Voice synth requests/month | 50K | 500K | 5M |
| **Engagement** | Score matches tracked/month | 0 | 5K | 100K |
| **Community** | GitHub stars | 100 | 500 | 2,000 |
| **Community** | Contributors | 5 | 20 | 50 |

### Key Milestones

| Milestone | Target Date | Significance |
|-----------|------------|--------------|
| First external user (free) | Mar 2026 | Product-market signal |
| 100 free users | Apr 2026 | Distribution working |
| First paying customer (platform) | Apr 2026 | Revenue validation |
| Score prototype demo | Apr 2026 | Consumer product viability |
| $1K MRR | Jun 2026 | Business viability signal |
| Score public beta | Jun 2026 | Consumer market entry |
| 1,000 free users | Aug 2026 | Community traction |
| Score v1.0 launch | Aug 2026 | Consumer revenue stream live |
| $5K MRR | Oct 2026 | Sustainable solo business |
| First vertical expansion (pickleball) | Sep 2026 | Flywheel validation |
| First enterprise contract | Dec 2026 | Market expansion |
| $10K MRR | Feb 2027 | Growth confirmation |
| $50K MRR | Sep 2027 | Scale threshold |
| $100K MRR | 2028 | Category leadership |

---

## 14. Long-Term Vision

LockN Labs becomes **the company that owns both the AI perception platform and the products it powers**. On the platform side, every serious OpenClaw user runs LockN. The suite handles thinking, speaking, seeing, hearing, and embodiment — a complete AI presence that's private, fast, and endlessly customizable. On the product side, LockN Score becomes the default AI sports analysis tool, and the same technology expands into fitness, education, healthcare, and beyond.

**The end state:**

- A developer installs OpenClaw, discovers LockN, and within an hour has an AI agent that can reason, speak in a custom voice, see through a camera, and appear as a lip-synced avatar — all running locally on their GPU.

- A ping pong player sets up their phone, opens Score, and gets automatic real-time scoring, rally analytics, and improvement tracking — no manual input, no expensive equipment, just AI that watches and understands the game.

- An enterprise deploys LockN on-premise for a HIPAA-compliant healthcare assistant that interviews patients, reads medical images, and speaks results — with zero data leaving the building.

- A physical therapy clinic uses LockN-powered movement analysis to track patient range-of-motion recovery with clinical precision using a standard camera.

- A creator fine-tunes a custom voice and avatar through LockN Tune, creating a unique AI personality that becomes their brand's digital representative.

**Cloud captures the rest:** LockN Cloud offers the same experience for users without GPU hardware. The cloud tier is pure margin — the product is already built and proven locally.

**The flywheel:**

```
Platform improves → New vertical products launch faster
        ↓
Products generate revenue + training data
        ↓
Revenue funds platform R&D
        ↓
Better platform attracts more developers
        ↓
More developers = more innovation on platform
        ↓
More products, more verticals, more revenue
        ↓
A machine that disrupts multiple markets in parallel
```

### Sean's Founding Principle

> "We have to start winning with what we have already, which is truly a lot. And the opportunity is here for our taking."

The hardware is owned. The models are running. The products are shipping. The distribution channel is growing. The marginal cost is zero. This isn't a plan waiting for funding — it's a plan already in execution. And it's not just a developer tools company — it's a platform that can spawn entire product lines at will.

---

*LockN Labs — Platform + Products. Private. Integrated. Local-first. The complete AI stack.*

---

**Document prepared:** February 7, 2026
**Version:** 2.0
**Contact:** Sean Lachenberg, Founder — OneSun Labs LLC (DBA LockN Labs)
**Location:** Atlanta Metro, Georgia
