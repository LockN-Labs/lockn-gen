# LOC-66: PostgreSQL Persistence & Migrations

## Overview
Add proper PostgreSQL persistence with EF Core migrations for LockN Gen, replacing the current InMemory fallback with production-ready database support.

## Problem Statement
Currently the application:
- Uses InMemory database in development (no persistence)
- Has no EF Core migrations defined
- Missing proper schema for Generation and ApiKey entities
- No database seeding for default data

## Requirements

### Functional Requirements

1. **EF Core Migrations**
   - Initial migration for existing entities (Generation, ApiKey)
   - Migration history tracking
   - Support for `dotnet ef` CLI commands
   - Idempotent migration application

2. **Entity Configuration**
   - Proper column types and lengths
   - Indexes on frequently queried columns
   - Foreign key relationships (if any)
   - Soft delete support (IsDeleted flag)

3. **Connection Configuration**
   - Connection string from appsettings.json
   - Environment variable override support
   - Connection pooling configuration
   - Timeout settings

4. **Health Check Integration**
   - Database connectivity check
   - Migration status check (optional)
   - Connection pool health

5. **Docker Compose**
   - PostgreSQL 16 service
   - Volume for data persistence
   - Health check for container
   - Environment variables for credentials

### Non-Functional Requirements
- Automatic migration on startup (development mode only)
- Connection resilience (retry on transient failures)
- < 100ms connection establishment

## Technical Approach

### Entity Configurations
```csharp
// Generation entity
- Id: UUID (primary key)
- Prompt: nvarchar(2000)
- Status: enum (int)
- ImagePath: nvarchar(500), nullable
- ErrorMessage: nvarchar(1000), nullable
- CreatedAt: timestamptz
- CompletedAt: timestamptz, nullable

// ApiKey entity
- Id: UUID (primary key)
- KeyHash: char(64), indexed
- Name: nvarchar(100)
- RateLimit: int
- IsActive: bool
- CreatedAt: timestamptz
```

### Configuration
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=lockngen;Username=lockn;Password=secret"
  }
}
```

### Docker Compose Addition
```yaml
services:
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
```

## Acceptance Criteria
- [ ] Initial migration created and tested
- [ ] docker-compose.yml includes postgres service
- [ ] Health endpoint reports database status
- [ ] Connection pooling properly configured
- [ ] Entity configurations with proper column types
- [ ] Seeding for default API key (development)
- [ ] README updated with database setup instructions

## Out of Scope
- Database backup/restore automation
- Read replicas
- Sharding

## Dependencies
- LOC-64 (Authentication) - ApiKey entity defined
