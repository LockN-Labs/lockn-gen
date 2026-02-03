# LOC-57: Project Setup & Requirements

## Overview

Initial project scaffold for LockN Gen — a generative media UI wrapper following the same architecture pattern as LockN Speak and LockN Logger.

## Scope

### In Scope
- .NET 9 solution structure with Domain/Infrastructure/Api layers
- Basic project configuration (csproj, solution file)
- Docker and docker-compose setup (dev environment)
- PostgreSQL integration (EF Core with initial migration)
- Basic entities: Generation, Preset, Model
- Health check endpoint
- README with setup instructions

### Out of Scope
- ComfyUI integration (LOC-58)
- Full API endpoints (future tickets)
- Frontend UI (future tickets)
- Video generation (post-MVP)

## Technical Requirements

### Solution Structure
```
lockn-gen/
├── src/
│   ├── LockNGen.Domain/          # Entities, interfaces, DTOs
│   ├── LockNGen.Infrastructure/  # EF Core, ComfyUI client
│   └── LockNGen.Api/             # ASP.NET Minimal API
├── tests/
│   └── LockNGen.Domain.Tests/    # Unit tests
├── docker-compose.yml            # Dev environment
├── Dockerfile                    # Multi-stage build
└── LockNGen.sln                  # Solution file
```

### Entities (Initial)

#### Generation
```csharp
public class Generation
{
    public Guid Id { get; set; }
    public string Prompt { get; set; } = string.Empty;
    public string? NegativePrompt { get; set; }
    public string Model { get; set; } = "sdxl-1.0";
    public int Width { get; set; } = 1024;
    public int Height { get; set; } = 1024;
    public int Steps { get; set; } = 20;
    public double Guidance { get; set; } = 7.5;
    public long? Seed { get; set; }
    public GenerationStatus Status { get; set; } = GenerationStatus.Queued;
    public string? OutputPath { get; set; }
    public string? ThumbnailPath { get; set; }
    public string? ErrorMessage { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
    public int? DurationMs { get; set; }
}

public enum GenerationStatus
{
    Queued,
    Processing,
    Complete,
    Failed
}
```

### Configuration
- PostgreSQL connection string from environment
- InMemory fallback for local dev without Docker
- Health check with database connectivity

### Docker Setup
- Multi-stage Dockerfile (SDK → runtime)
- docker-compose.yml with:
  - api (LockN Gen API)
  - db (PostgreSQL 16)
  - volumes for database persistence

## Acceptance Criteria

1. ✅ Solution builds with `dotnet build`
2. ✅ `dotnet run` starts API on port 8080
3. ✅ `/health` returns 200 OK
4. ✅ `docker compose up` starts full stack
5. ✅ EF Core migration runs on startup
6. ✅ Basic entity structure matches requirements.md

## Dependencies

- .NET 9 SDK
- PostgreSQL 16
- Docker & Docker Compose

---

*Phase 1 Requirements — Created 2026-02-03*
