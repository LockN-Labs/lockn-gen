# LockN Suite + OpenClaw Model Roadmap (Draft)

Date: 2026-02-08
Owner: Claws

## Objective
Fastest path to cash flow via subscription-ready capabilities: realtime voice loop, reliable agent orchestration, and higher-quality RAG.

## Current baseline (already strong)
- Primary local coding/orchestration: Qwen3-Coder-Next (llama.cpp :11439)
- Local reasoning/review: Qwen3-32B (:11437)
- Local vision: Qwen3-VL 8B (Ollama)
- Embeddings: qwen3-embedding
- Orchestration: OpenClaw + cron heartbeat system

## 0-2 Weeks (Now)
1. Realtime voice MVP (Sean <-> Claws)
   - STT: Parakeet TDT 0.6B-v3 (try)
   - TTS: Qwen3-TTS (or current Speak path fallback)
   - LLM brain: existing local Qwen3-Coder-Next + cloud fallback
   - KPI: median turn latency, interruption handling, reliability

2. Subscription packaging + manual close motion
   - Productize tiers and upsell triggers before Stripe unblock
   - Use manual onboarding/checklists while billing automation catches up

3. RAG quality uplift
   - Add reranking experiment (BGE reranker class)
   - Compare qwen3-embedding vs nomic-embed-v1.5 on retrieval accuracy

## 2-6 Weeks (Next)
1. Multi-provider router
   - Local-first routing with cloud escalation by task class/SLA
2. Premium voice tier
   - Higher quality/prosody options and response style controls
3. Capability-gated plans
   - Core, Pro Voice, Managed Ops tiers

## 6-12 Weeks (Later)
1. Telephony/real-time hardening
2. Advanced multimodal workflows
3. Cost/latency policy engine + automatic failover

## Buy / Try / Skip (initial)
- BUY/KEEP: Qwen3-Coder-Next, Qwen3-32B, Qwen3-VL, OpenClaw orchestration
- TRY NOW: Parakeet STT, Qwen3-TTS path, BGE reranker, Nomic embeddings
- TRY LATER: DeepSeek-R1 reasoning tier, Orpheus premium voice
- SKIP FOR NOW: overlapping heavyweight models with weak incremental ROI

## This-week experiments
1. Voice bakeoff: cloud realtime vs local STT+LLM+TTS chain
2. RAG bakeoff: baseline vs reranker-enabled pipeline
3. Coding throughput: local-default + cloud-escalation policy tuning

## Success metrics
- First paid subscription close
- Voice latency and success-rate SLO met
- Higher retrieval precision with minimal latency/cost increase
- Clear upsell path from base integration to premium capabilities
