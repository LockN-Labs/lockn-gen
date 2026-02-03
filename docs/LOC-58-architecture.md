# LOC-58: ComfyUI Backend Integration — Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        LockN Gen API                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │ GenerationService │───▶│  ComfyUiClient   │──────┐          │
│  └────────┬─────────┘    └──────────────────┘      │          │
│           │                                         │          │
│           ▼                                         ▼          │
│  ┌──────────────────┐    ┌──────────────────┐  ┌────────┐     │
│  │ GenerationWorker │    │ WorkflowLoader   │  │ComfyUI │     │
│  │ (BackgroundSvc)  │    └──────────────────┘  │ :8188  │     │
│  └────────┬─────────┘                          └────────┘     │
│           │                                                    │
│           ▼                                                    │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │   AppDbContext   │    │  File Storage    │                 │
│  │   (PostgreSQL)   │    │  (./outputs)     │                 │
│  └──────────────────┘    └──────────────────┘                 │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. Client POST /api/generations
   │
   ▼
2. GenerationService.QueueGenerationAsync()
   - Validate request
   - Create Generation entity (Status: Queued)
   - Save to database
   - Return generation ID
   │
   ▼
3. GenerationWorker (polling every 5s)
   - Query for Queued generations
   - Lock generation (Status: Processing)
   │
   ▼
4. WorkflowLoader.LoadWorkflow(model)
   - Read template JSON from workflows/
   - Substitute parameters (prompt, seed, etc.)
   │
   ▼
5. ComfyUiClient.QueuePromptAsync(workflow)
   - POST to ComfyUI /prompt
   - Returns prompt_id
   │
   ▼
6. Poll ComfyUI /history/{prompt_id}
   - Wait for completion
   - Timeout after 5 minutes
   │
   ▼
7. ComfyUiClient.GetImageAsync(filename)
   - Download generated image
   - Save to outputs/{generation_id}.png
   │
   ▼
8. Update Generation entity
   - Status: Complete
   - OutputPath: outputs/{id}.png
   - CompletedAt, DurationMs
```

## File Structure

```
src/
├── LockNGen.Domain/
│   ├── Entities/
│   │   └── Generation.cs          # Extended with ComfyUI fields
│   ├── Services/
│   │   ├── IComfyUiClient.cs      # ComfyUI HTTP client interface
│   │   ├── IGenerationService.cs  # Generation queue service
│   │   └── IWorkflowLoader.cs     # Workflow template loader
│   └── DTOs/
│       ├── ComfyWorkflow.cs       # Workflow JSON model
│       ├── PromptHistory.cs       # ComfyUI history response
│       └── SystemStats.cs         # ComfyUI system stats
│
├── LockNGen.Infrastructure/
│   ├── ComfyUi/
│   │   ├── ComfyUiClient.cs       # HTTP client implementation
│   │   ├── ComfyUiOptions.cs      # Configuration POCO
│   │   └── WorkflowLoader.cs      # Template loading
│   └── Services/
│       ├── GenerationService.cs   # Queue management
│       └── GenerationWorker.cs    # Background processor
│
└── LockNGen.Api/
    └── Program.cs                 # DI registration, health check
```

## Interface Definitions

### IComfyUiClient

```csharp
namespace LockNGen.Domain.Services;

/// <summary>
/// HTTP client for ComfyUI API communication.
/// </summary>
public interface IComfyUiClient
{
    /// <summary>
    /// Gets system statistics including GPU memory and queue status.
    /// </summary>
    Task<SystemStats> GetSystemStatsAsync(CancellationToken ct = default);
    
    /// <summary>
    /// Queues a workflow for execution.
    /// </summary>
    /// <returns>The prompt ID for tracking.</returns>
    Task<string> QueuePromptAsync(ComfyWorkflow workflow, CancellationToken ct = default);
    
    /// <summary>
    /// Gets the execution history for a prompt.
    /// </summary>
    Task<PromptHistory?> GetHistoryAsync(string promptId, CancellationToken ct = default);
    
    /// <summary>
    /// Downloads a generated image.
    /// </summary>
    Task<Stream> GetImageAsync(string filename, string subfolder = "", string type = "output", CancellationToken ct = default);
    
    /// <summary>
    /// Checks if ComfyUI is reachable and responsive.
    /// </summary>
    Task<bool> IsHealthyAsync(CancellationToken ct = default);
}
```

### IGenerationService

```csharp
namespace LockNGen.Domain.Services;

/// <summary>
/// Manages the generation queue and lifecycle.
/// </summary>
public interface IGenerationService
{
    /// <summary>
    /// Queues a new generation request.
    /// </summary>
    Task<Generation> QueueAsync(GenerationRequest request, CancellationToken ct = default);
    
    /// <summary>
    /// Gets generation by ID with current status.
    /// </summary>
    Task<Generation?> GetAsync(Guid id, CancellationToken ct = default);
    
    /// <summary>
    /// Lists generations with optional filters.
    /// </summary>
    Task<IReadOnlyList<Generation>> ListAsync(int skip = 0, int take = 20, CancellationToken ct = default);
    
    /// <summary>
    /// Cancels a queued generation.
    /// </summary>
    Task<bool> CancelAsync(Guid id, CancellationToken ct = default);
    
    /// <summary>
    /// Gets the output image stream for a completed generation.
    /// </summary>
    Task<Stream?> GetImageStreamAsync(Guid id, CancellationToken ct = default);
}
```

### IWorkflowLoader

```csharp
namespace LockNGen.Domain.Services;

/// <summary>
/// Loads and parameterizes ComfyUI workflow templates.
/// </summary>
public interface IWorkflowLoader
{
    /// <summary>
    /// Loads a workflow template and substitutes parameters.
    /// </summary>
    Task<ComfyWorkflow> LoadAsync(string templateName, GenerationParameters parameters, CancellationToken ct = default);
    
    /// <summary>
    /// Lists available workflow templates.
    /// </summary>
    Task<IReadOnlyList<string>> ListTemplatesAsync(CancellationToken ct = default);
}
```

## Error Handling Strategy

| Error | Detection | Response |
|-------|-----------|----------|
| ComfyUI unreachable | HTTP timeout/connection refused | Mark health degraded, retry with backoff |
| GPU OOM | ComfyUI error response | Mark generation Failed, log error details |
| Model not found | ComfyUI error "model not found" | Mark Failed, suggest valid models |
| Generation timeout | 5 min without completion | Mark Failed, attempt ComfyUI queue clear |
| Invalid workflow | JSON parse error | Mark Failed, log template issue |
| Storage full | IOException on save | Mark Failed, alert, pause worker |

**Retry Policy:**
- ComfyUI API calls: 3 retries with exponential backoff (1s, 2s, 4s)
- Transient failures only (timeouts, 5xx)
- No retry on 4xx (client error)

## Configuration Schema

```json
{
  "ComfyUi": {
    "BaseUrl": "http://localhost:8188",
    "TimeoutSeconds": 300,
    "PollIntervalMs": 2000,
    "MaxConcurrentGenerations": 1,
    "WorkflowsPath": "./workflows",
    "OutputPath": "./outputs"
  }
}
```

**appsettings.json integration:**

```csharp
public class ComfyUiOptions
{
    public const string SectionName = "ComfyUi";
    
    public string BaseUrl { get; set; } = "http://localhost:8188";
    public int TimeoutSeconds { get; set; } = 300;
    public int PollIntervalMs { get; set; } = 2000;
    public int MaxConcurrentGenerations { get; set; } = 1;
    public string WorkflowsPath { get; set; } = "./workflows";
    public string OutputPath { get; set; } = "./outputs";
}
```

## Health Check Integration

```csharp
// In Program.cs
builder.Services.AddHealthChecks()
    .AddCheck<ComfyUiHealthCheck>("comfyui");

public class ComfyUiHealthCheck : IHealthCheck
{
    private readonly IComfyUiClient _client;
    
    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context, 
        CancellationToken ct = default)
    {
        try
        {
            var stats = await _client.GetSystemStatsAsync(ct);
            return HealthCheckResult.Healthy($"GPU: {stats.GpuMemoryUsed}/{stats.GpuMemoryTotal}");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("ComfyUI unreachable", ex);
        }
    }
}
```

---

*Phase 2 Architecture — Created 2026-02-03*
