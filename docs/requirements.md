# LockN Gen — Requirements

## Overview

LockN Gen is a generative media UI wrapper for image and video generation models. Same architecture pattern as LockN Speak: .NET 9 ASP.NET Minimal API + simple web UI frontend.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  Web UI      │────▶│  .NET API         │────▶│  Model Backends     │
│  (HTML/JS)   │     │  (ASP.NET 9)      │     │  (ComfyUI/etc.)     │
└─────────────┘     └──────────────────┘     └─────────────────────┘
                           │
                    ┌──────┴──────┐
                    │ PostgreSQL  │
                    │ + File Store│
                    └─────────────┘
```

## Core Features

### Image Generation
- [ ] Text-to-image generation
- [ ] Image-to-image (with style transfer, inpainting)
- [ ] ControlNet support (pose, depth, canny)
- [ ] Model selection (SDXL, Flux, etc.)

### Video Generation
- [ ] Text-to-video
- [ ] Image-to-video (animate still images)
- [ ] Video-to-video style transfer

### UI Features
- [ ] Prompt input with history
- [ ] Parameter controls (steps, guidance, seed, etc.)
- [ ] Gallery view of generated media
- [ ] Generation queue status
- [ ] Download/export options

### Backend Integration Options
- **ComfyUI** — Workflow-based, highly customizable (Apache 2.0)
- **SD.Next** — Feature-rich Stable Diffusion frontend (AGPL-3.0 ❌)
- **InvokeAI** — Clean API, good UX (Apache 2.0)
- **Fooocus** — Simple, Midjourney-like (GPL-3.0 ❌)

**Recommendation:** ComfyUI API mode for maximum flexibility + Apache 2.0 license.

## Tech Stack (Matching LockN Speak)

- .NET 9 / ASP.NET Minimal APIs
- PostgreSQL (EF Core)
- Simple HTML/JS frontend (no framework)
- Docker Compose
- ComfyUI backend (GPU container)

## Entities

### Generation
- Id, Prompt, NegativePrompt, Model, Width, Height, Steps, Guidance, Seed
- Status (Queued, Processing, Complete, Failed)
- OutputPath, ThumbnailPath
- CreatedAt, CompletedAt, DurationMs

### Preset
- Id, Name, Description
- Model, Width, Height, Steps, Guidance
- DefaultPromptPrefix, DefaultNegativePrompt

### Model
- Id, Name, Type (Checkpoint, LoRA, ControlNet)
- Backend (ComfyUI, etc.)
- FilePath, Hash

## API Endpoints

### Generations
- `POST /api/generations` — Queue new generation
- `GET /api/generations` — List generations (paginated)
- `GET /api/generations/{id}` — Get generation details
- `GET /api/generations/{id}/image` — Get generated image
- `DELETE /api/generations/{id}` — Delete generation

### Presets
- `GET /api/presets` — List presets
- `POST /api/presets` — Create preset
- `PUT /api/presets/{id}` — Update preset
- `DELETE /api/presets/{id}` — Delete preset

### Models
- `GET /api/models` — List available models
- `POST /api/models/refresh` — Rescan model directory

### Queue
- `GET /api/queue` — Current queue status
- `DELETE /api/queue/{id}` — Cancel queued generation

## Open Questions

1. **Video models** — Which video generation models to support initially? (Mochi, CogVideoX, AnimateDiff?)
2. **Storage** — Local filesystem or SeaweedFS like LockN Logger?
3. **Batch generation** — Support generating multiple variations at once?
4. **WebSocket** — Real-time progress updates for long generations?

## Phase 1 MVP

1. Text-to-image with SDXL
2. Basic parameter controls
3. Gallery view
4. ComfyUI backend integration
5. Generation history with PostgreSQL

---

*Created: 2026-02-03*
