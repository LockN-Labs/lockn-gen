# LockN Tune — Engineering Review

## Summary
- **Feasibility:** High
- **Estimate:** 10 weeks
- **Architecture:** Control-plane + worker pattern

## Tech Stack
- Next.js/React (wizard-style SPA)
- FastAPI (Python backend)
- PyTorch + Hugging Face Transformers
- PEFT (LoRA/QLoRA) + TRL + bitsandbytes + Accelerate
- Axolotl or LLaMA-Factory (standardized training recipes)
- Qwen3-TTS-compatible fine-tuning pipeline
- Redis + Celery/RQ (or Temporal for durable workflows)
- PostgreSQL (runs, metadata, lineage)
- Artifact storage abstraction (local FS first, MinIO/S3-compatible later)
- Docker + NVIDIA Container Toolkit
- OpenTelemetry + Prometheus/Grafana (observability)

## Risks
- Inconsistent TTS quality due to poor/variable user datasets
- Consumer GPU/CUDA/driver environment incompatibilities
- Adapter compatibility gaps across llama.cpp/Ollama model variants
- Bad default hyperparameters causing poor outcomes for non-experts
- Offline eval improvements not matching perceived real-world quality
- Long-running local jobs interrupted without robust checkpoint/resume
- Voice-cloning abuse/safety/compliance concerns

## Dependencies
- LockN Speak API support for tuned voice registration/versioning
- LockN Eval job submission and report ingestion API
- Auth0 role mappings for project/run permissions
- GPU container runtime stack (NVIDIA drivers + toolkit)
- Queue/orchestration service (Redis + workers or Temporal)
- Postgres database for metadata and lineage tracking

## Architecture Notes
Use a control-plane + worker architecture: wizard UI and API manage run configs, validation, permissions, and lifecycle; GPU workers execute LLM/TTS tuning jobs asynchronously with checkpoint/resume; a metadata layer tracks reproducibility (dataset snapshot hash, config manifest, image version); artifact registry stores adapters/voices and publishes to LockN Speak + local LLM serving; LockN Eval integration provides baseline-vs-tuned comparisons. Prioritize strict preflight checks, constrained supported model matrix, and guardrails for dataset quality and voice consent.

## Suggested Tickets
| # | Title | Estimate | Priority |
|---|-------|----------|----------|
| 1 | Define supported model matrix + GPU preflight validator | L | P1 |
| 2 | Implement LLM LoRA/QLoRA training worker v1 | XL | P1 |
| 3 | Build Tune wizard UI (dataset → config → run → results) | XL | P1 |
| 4 | Run orchestration API + queue + state machine | L | P1 |
| 5 | Checkpoint/resume/retry for long-running jobs | L | P1 |
| 6 | Artifact metadata + lineage/versioning service | M | P1 |
| 7 | Integrate LockN Eval comparison workflow | M | P2 |
| 8 | Integrate LockN Speak tuned voice registry | M | P2 |
| 9 | TTS fine-tune beta pipeline + dataset quality checks | XL | P2 |
| 10 | Voice cloning consent/policy enforcement layer | L | P1 |

## Open Questions
1. Which base model families are officially supported for MVP?
2. Must MVP run fully offline/local, or can control-plane services be cloud-assisted?
3. What minimum TTS dataset requirements (duration, quality, transcript alignment) are acceptable?
4. What policy/compliance bar is required for custom voice creation at launch?
5. Is LockN Eval API already stable, or should this project define it?
6. Do tuned artifacts need export portability outside the LockN ecosystem?
7. Is MVP single-user only, or does it require team collaboration/project sharing?
