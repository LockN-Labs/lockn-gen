# LockN Tune — Project Brief

*Synthesized from 5 stakeholder reviews | Feb 11, 2026*

## Executive Summary
LockN Tune is a local-first fine-tuning pipeline that enables users to customize LLMs and TTS voices on their own hardware — no ML expertise, no cloud GPU costs, full data privacy. It's the "personalization engine" of the LockN ecosystem, transforming the suite from AI tools into an AI customization platform.

**Decision: CONDITIONAL GO** (finance)
**Feasibility: HIGH** (engineering)
**RICE Score: 64** (product)

## Business Case
- **Projected MRR:** $72K at 12 months post-launch
- **Pricing:** Starter $29 one-time / Pro $79/mo / Enterprise $299/mo
- **Break-even:** Month 13 (Sep 2027)
- **Implementation cost:** ~$63.5K (10-12 weeks engineering)
- **Infra cost:** Minimal for local-first; $50-200/mo for control-plane services

### Conditions (must meet by Jun 2026)
1. 200+ email sign-ups from landing page
2. Working prototype on consumer GPU (RTX 4070 class) by May 2026
3. $80K funding buffer secured
4. 3-5 content-creator beta testers committed

## Target Users
1. **Indie Creators** (40%) — YouTubers, podcasters wanting custom AI voices
2. **Small Businesses** (35%) — Domain-specific LLMs for customer service/content
3. **Developers** (25%) — Custom model behavior without ML expertise

## Positioning
> "Own your AI models. Train locally, keep privately, use forever — without cloud GPU bills."

## Technical Architecture
- **Pattern:** Control-plane + GPU worker
- **Stack:** Next.js/React UI → FastAPI backend → PyTorch/PEFT/HuggingFace
- **Training:** LoRA/QLoRA via Axolotl or LLaMA-Factory
- **Queue:** Redis + Celery (or Temporal for durable workflows)
- **Storage:** PostgreSQL (metadata) + local FS (artifacts, S3-compatible later)
- **Monitoring:** OpenTelemetry + Prometheus/Grafana (via LockN Control)

## MVP Scope (v1)
- LoRA/QLoRA fine-tuning for Llama/Mistral family
- TTS voice cloning (5-min minimum sample)
- Drag-and-drop data upload
- One-click fine-tuning with preset configs
- Local GPU execution with progress monitoring
- Model export for LockN Speak integration
- Simple web UI for non-technical users
- Checkpoint/resume for long-running jobs

## Deferred (v2+)
- Multi-modal fine-tuning, distributed/cloud training
- Team collaboration, model sharing
- Advanced hyperparameter UI, data augmentation
- Differential privacy, federated learning

## Cross-Product Dependencies
- **LockN Speak:** Tuned voice registration/versioning API
- **LockN Control:** Training job monitoring dashboards
- **LockN Eval:** Baseline-vs-tuned comparison (API must be defined)
- **Auth0:** Role mappings for project/run permissions

## Key Risks
1. Consumer GPU/CUDA environment incompatibilities
2. Poor TTS quality from low-quality user datasets
3. Voice cloning legal/compliance concerns
4. Open-source alternatives (Axolotl, unsloth) are free
5. Cloud competitors could add local-first features
6. Long-running job interruption without robust checkpoint/resume

## Go-to-Market
- **Pre-launch:** Landing page with ROI calculator, email capture, creator outreach
- **Soft launch (Jul 2026):** Starter tier, 50 beta users, creator ambassadors
- **Full launch (Aug 2026):** All tiers, content marketing, community building
- **Growth:** Creator-led viral loop, case studies, YouTube tutorials

## Milestones
| Milestone | Target Date | Key Deliverables |
|-----------|------------|-----------------|
| Foundation Sprint | Mar 15, 2026 | Architecture, dev env, LoRA prototype, UI mockups |
| Core Pipeline | May 1, 2026 | LLM fine-tuning worker, wizard UI, job orchestration |
| TTS Integration | Jun 15, 2026 | Voice cloning pipeline, LockN Speak integration |
| MVP Launch | Aug 1, 2026 | Full product, landing page, beta program |

## Success Metrics
| Metric | Target | Timeframe |
|--------|--------|-----------|
| MRR | $72K | 12 months post-launch |
| Active monthly users | 1,500 | 6 months post-launch |
| Models created/month | 300 | 6 months post-launch |
| 90-day retention | 60% | Ongoing after month 3 |
| Cross-product (Tune → Speak) | 40% | 9 months post-launch |

## Open Questions
1. Which base model families for MVP? (Llama + Mistral recommended)
2. Fully offline MVP, or cloud-assisted control plane?
3. Minimum TTS dataset requirements (duration, quality)?
4. Voice cloning compliance bar at launch?
5. Is LockN Eval API stable, or does Tune define it?
6. Single-user MVP or team collaboration?
7. Model export portability outside LockN ecosystem?

## Stakeholder Reviews
- [Engineering](reviews/engineering.md) — Feasibility high, 10 weeks, 10 tickets
- [DevOps](reviews/devops.md) — $2.5-4K/mo cloud estimate, 12 tickets
- [Finance](reviews/finance.md) — Conditional go, $72K MRR at 12mo
- [Marketing](reviews/marketing.md) — Creator-led GTM, "own your models" positioning
- [Product](reviews/product.md) — RICE 64, 9 MVP features, 4 milestones
