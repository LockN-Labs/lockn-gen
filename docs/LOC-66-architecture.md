# LOC-66: PostgreSQL Persistence Architecture

## Overview
This document describes the architecture for PostgreSQL persistence in LockN Gen, including migrations, connection management, and Docker integration.

## Database Schema

### Generation Table
```sql
CREATE TABLE "Generations" (
    "Id" uuid PRIMARY KEY,
    "Name" varchar(255) NOT NULL DEFAULT '',
    "Prompt" varchar(4000) NOT NULL,
    "NegativePrompt" varchar(4000),
    "Model" varchar(100) NOT NULL DEFAULT 'sdxl',
    "Width" int NOT NULL DEFAULT 1024,
    "Height" int NOT NULL DEFAULT 1024,
    "Steps" int NOT NULL DEFAULT 20,
    "Guidance" real NOT NULL DEFAULT 7.5,
    "Seed" int,
    "Status" int NOT NULL DEFAULT 0,
    "PromptId" varchar(100),
    "OutputPath" varchar(500),
    "ThumbnailPath" varchar(500),
    "ErrorMessage" varchar(2000),
    "CreatedAt" timestamptz NOT NULL,
    "UpdatedAt" timestamptz,
    "CompletedAt" timestamptz,
    "DurationMs" int
);

CREATE INDEX "IX_Generations_Status" ON "Generations" ("Status");
CREATE INDEX "IX_Generations_CreatedAt" ON "Generations" ("CreatedAt");
```

### ApiKeys Table
```sql
CREATE TABLE "ApiKeys" (
    "Id" uuid PRIMARY KEY,
    "Name" varchar(255) NOT NULL,
    "KeyHash" char(64) NOT NULL,
    "KeyPrefix" varchar(16) NOT NULL,
    "IsAdmin" boolean NOT NULL DEFAULT false,
    "RateLimit" int NOT NULL DEFAULT 100,
    "CreatedAt" timestamptz NOT NULL,
    "LastUsedAt" timestamptz,
    "ExpiresAt" timestamptz,
    "RevokedAt" timestamptz
);

CREATE UNIQUE INDEX "IX_ApiKeys_KeyHash" ON "ApiKeys" ("KeyHash");
CREATE INDEX "IX_ApiKeys_KeyPrefix" ON "ApiKeys" ("KeyPrefix");
```

## Component Design

```
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  Program.cs                                                      │
│  ├── Connection string resolution (config → env → default)      │
│  ├── DbContext registration (PostgreSQL or InMemory)            │
│  ├── Migration application (dev mode only)                      │
│  └── Health check registration                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  AppDbContext                                                    │
│  ├── Entity configurations (OnModelCreating)                    │
│  ├── Change tracking                                            │
│  └── Query optimization hints                                   │
│                                                                  │
│  Migrations/                                                     │
│  ├── InitialCreate                                              │
│  └── AppDbContextModelSnapshot                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Database Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL 16                                                   │
│  ├── Connection pooling (Npgsql)                                │
│  ├── Automatic reconnection                                     │
│  └── SSL/TLS support (production)                               │
└─────────────────────────────────────────────────────────────────┘
```

## Connection Management

### Connection String Resolution
1. `ConnectionStrings:DefaultConnection` from appsettings.json
2. `DATABASE_URL` environment variable (Heroku/Railway style)
3. Fallback to InMemory database for local dev

### Connection Pooling
- Min pool size: 5
- Max pool size: 100
- Connection lifetime: 300 seconds
- Command timeout: 30 seconds

## Docker Compose

```yaml
services:
  api:
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - ConnectionStrings__DefaultConnection=Host=postgres;Database=lockngen;Username=lockn;Password=secret

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: lockngen
      POSTGRES_USER: lockn
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U lockn -d lockngen"]
      interval: 5s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Migration Strategy

### Development
- Automatic migration on startup
- EnsureCreated() for InMemory fallback
- Seed data for testing

### Production
- Manual migration via CLI or deployment script
- No automatic migration
- Health check blocks traffic until DB ready

## Health Check

```csharp
services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database", tags: ["db", "ready"]);
```

Returns:
- `Healthy`: Database connected and responsive
- `Degraded`: Using InMemory fallback
- `Unhealthy`: Connection failed

## File Structure

```
src/LockNGen.Infrastructure/
├── Data/
│   ├── AppDbContext.cs
│   └── Migrations/
│       ├── 20260203_InitialCreate.cs
│       └── AppDbContextModelSnapshot.cs
└── LockNGen.Infrastructure.csproj
```

## Dependencies

- Npgsql.EntityFrameworkCore.PostgreSQL >= 9.0.0
- Microsoft.EntityFrameworkCore.Design >= 9.0.0 (tools)
