# LOC-58: ComfyUI Backend Integration — Requirements

## Overview

Integrate ComfyUI API mode as the image generation backend for LockN Gen. ComfyUI provides a powerful node-based workflow system with an HTTP API for programmatic control.

## Goals

1. Connect to ComfyUI instance via HTTP API
2. Execute text-to-image workflows
3. Manage generation queue
4. Handle model loading and GPU resources
5. Provide health status for ComfyUI connection

## ComfyUI API Reference

ComfyUI exposes these endpoints when running in API mode (`--listen`):

- `GET /system_stats` — System info, GPU status
- `GET /object_info` — Available nodes and their parameters
- `POST /prompt` — Queue a workflow for execution
- `GET /history/{prompt_id}` — Get results of completed workflow
- `GET /view?filename=...` — Retrieve generated images
- `WS /ws` — WebSocket for progress updates

## Requirements

### R1: ComfyUI HTTP Client

Create `IComfyUiClient` interface and implementation:

```csharp
public interface IComfyUiClient
{
    Task<SystemStats> GetSystemStatsAsync();
    Task<string> QueuePromptAsync(ComfyWorkflow workflow);
    Task<PromptHistory> GetHistoryAsync(string promptId);
    Task<Stream> GetImageAsync(string filename, string subfolder = "", string type = "output");
    Task<bool> IsHealthyAsync();
}
```

### R2: Workflow Templates

Store workflow JSON templates that can be parameterized:

```
workflows/
  txt2img-sdxl.json       # Basic SDXL text-to-image
  txt2img-flux.json       # Flux model workflow
  img2img-sdxl.json       # Image-to-image
```

Template variables (replaced at runtime):
- `{{prompt}}` — Positive prompt text
- `{{negative_prompt}}` — Negative prompt
- `{{seed}}` — Random seed (or -1 for random)
- `{{steps}}` — Sampling steps
- `{{cfg}}` — Guidance scale
- `{{width}}`, `{{height}}` — Image dimensions

### R3: Generation Service

```csharp
public interface IGenerationService
{
    Task<Generation> QueueGenerationAsync(GenerationRequest request);
    Task<GenerationStatus> GetStatusAsync(Guid generationId);
    Task<Stream?> GetImageAsync(Guid generationId);
    Task CancelAsync(Guid generationId);
}
```

### R4: Background Worker

Process queued generations:
1. Poll for pending Generation entities
2. Load appropriate workflow template
3. Substitute parameters
4. Submit to ComfyUI
5. Poll for completion (or use WebSocket)
6. Download result image and save to storage
7. Update Generation entity with result

### R5: Configuration

```json
{
  "ComfyUi": {
    "BaseUrl": "http://localhost:8188",
    "TimeoutSeconds": 300,
    "DefaultModel": "sdxl",
    "OutputPath": "./outputs"
  }
}
```

### R6: Health Check

Add ComfyUI health to `/health` endpoint:

```json
{
  "status": "healthy",
  "database": "connected",
  "comfyui": {
    "status": "connected",
    "gpuMemory": "12GB / 24GB",
    "queueLength": 2
  }
}
```

## Non-Requirements (Phase 2+)

- WebSocket progress streaming (LOC-59+)
- ControlNet support
- LoRA management
- Video generation

## Dependencies

- ComfyUI instance accessible at configured URL
- GPU with sufficient VRAM for target models
- Storage path for generated images

## Acceptance Criteria

1. ✅ Can connect to ComfyUI and verify health
2. ✅ Can queue a text-to-image generation
3. ✅ Generation completes and image is saved
4. ✅ Generation entity updated with result path
5. ✅ Errors handled gracefully (GPU OOM, model not found)

---

*Phase 1 Requirements — Created 2026-02-03*
