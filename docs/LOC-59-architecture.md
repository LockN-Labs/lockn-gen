# LOC-59: Text-to-Image API Endpoints — Architecture

## Endpoint Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (Minimal API)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  POST   /api/generations          → QueueAsync()               │
│  GET    /api/generations          → ListAsync()                │
│  GET    /api/generations/{id}     → GetAsync()                 │
│  DELETE /api/generations/{id}     → CancelAsync()              │
│  GET    /api/generations/{id}/image → GetImageStreamAsync()    │
│  GET    /api/models               → ListTemplatesAsync()       │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   IGenerationService    │
              │   IWorkflowLoader       │
              └─────────────────────────┘
```

## Request/Response DTOs

### GenerationRequest

```csharp
namespace LockNGen.Api.DTOs;

public record GenerationRequest
{
    public required string Prompt { get; init; }
    public string? NegativePrompt { get; init; }
    public string Model { get; init; } = "txt2img-sdxl";
    public int Steps { get; init; } = 20;
    public float Guidance { get; init; } = 7.5f;
    public int Width { get; init; } = 1024;
    public int Height { get; init; } = 1024;
    public int Seed { get; init; } = -1;
}
```

### GenerationResponse

```csharp
public record GenerationResponse
{
    public Guid Id { get; init; }
    public string Prompt { get; init; } = "";
    public string Status { get; init; } = "";
    public string? Model { get; init; }
    public int? Steps { get; init; }
    public float? Guidance { get; init; }
    public int? Width { get; init; }
    public int? Height { get; init; }
    public int? Seed { get; init; }
    public string? ErrorMessage { get; init; }
    public long? DurationMs { get; init; }
    public DateTime CreatedAt { get; init; }
    public DateTime? CompletedAt { get; init; }
}
```

### PagedResponse

```csharp
public record PagedResponse<T>
{
    public IReadOnlyList<T> Items { get; init; } = [];
    public int Page { get; init; }
    public int PageSize { get; init; }
    public int TotalItems { get; init; }
    public int TotalPages => (int)Math.Ceiling(TotalItems / (double)PageSize);
}
```

## Input Validation

```csharp
public static class GenerationValidator
{
    public static IResult? Validate(GenerationRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Prompt))
            return Results.BadRequest(new { error = "Prompt is required" });
            
        if (req.Prompt.Length > 2000)
            return Results.BadRequest(new { error = "Prompt exceeds 2000 characters" });
            
        if (req.Width < 64 || req.Width > 2048 || req.Width % 64 != 0)
            return Results.BadRequest(new { error = "Width must be 64-2048 and divisible by 64" });
            
        if (req.Height < 64 || req.Height > 2048 || req.Height % 64 != 0)
            return Results.BadRequest(new { error = "Height must be 64-2048 and divisible by 64" });
            
        if (req.Steps < 1 || req.Steps > 100)
            return Results.BadRequest(new { error = "Steps must be 1-100" });
            
        if (req.Guidance < 0 || req.Guidance > 30)
            return Results.BadRequest(new { error = "Guidance must be 0-30" });
            
        return null; // Valid
    }
}
```

## Endpoint Implementation

```csharp
public static class GenerationEndpoints
{
    public static void MapGenerationEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/generations")
            .WithTags("Generations")
            .WithOpenApi();

        group.MapPost("/", QueueGeneration)
            .WithName("QueueGeneration")
            .WithSummary("Queue a new image generation request")
            .Produces<GenerationResponse>(201)
            .Produces(400);

        group.MapGet("/", ListGenerations)
            .WithName("ListGenerations")
            .WithSummary("List generations with pagination")
            .Produces<PagedResponse<GenerationResponse>>();

        group.MapGet("/{id:guid}", GetGeneration)
            .WithName("GetGeneration")
            .WithSummary("Get generation by ID")
            .Produces<GenerationResponse>()
            .Produces(404);

        group.MapDelete("/{id:guid}", CancelGeneration)
            .WithName("CancelGeneration")
            .WithSummary("Cancel a queued generation")
            .Produces(204)
            .Produces(404);

        group.MapGet("/{id:guid}/image", GetGenerationImage)
            .WithName("GetGenerationImage")
            .WithSummary("Get generated image")
            .Produces(200, contentType: "image/png")
            .Produces(404);
    }
    
    // Implementation methods...
}
```

## Error Response Format

```json
{
  "error": "Human readable message",
  "code": "VALIDATION_ERROR",
  "details": { }
}
```

| Status | Scenario |
|--------|----------|
| 400 | Validation failed |
| 404 | Generation not found |
| 409 | Cannot cancel (already processing/complete) |
| 500 | Internal error |

## OpenAPI Integration

```csharp
// In Program.cs
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new()
    {
        Title = "LockN Gen API",
        Version = "v1",
        Description = "Text-to-image generation API powered by ComfyUI"
    });
});

// Enable in dev
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}
```

## File Structure

```
src/LockNGen.Api/
├── DTOs/
│   ├── GenerationRequest.cs
│   ├── GenerationResponse.cs
│   └── PagedResponse.cs
├── Endpoints/
│   ├── GenerationEndpoints.cs
│   └── ModelEndpoints.cs
├── Validation/
│   └── GenerationValidator.cs
└── Program.cs (updated with endpoint mapping)
```

## Mapping: Entity ↔ Response

```csharp
public static GenerationResponse ToResponse(this Generation entity) => new()
{
    Id = entity.Id,
    Prompt = entity.Name,
    Status = entity.Status.ToString(),
    Model = entity.Model,
    Steps = entity.Steps,
    Guidance = entity.Guidance,
    Width = entity.Width,
    Height = entity.Height,
    Seed = entity.Seed,
    ErrorMessage = entity.ErrorMessage,
    DurationMs = entity.DurationMs,
    CreatedAt = entity.CreatedAt,
    CompletedAt = entity.CompletedAt
};
```

---

*Phase 2 Architecture — Created 2026-02-03*
