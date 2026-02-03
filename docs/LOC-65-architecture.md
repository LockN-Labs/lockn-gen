# LOC-65: Rate Limiting Architecture

## Overview
This document describes the architecture for rate limiting in LockN Gen, implementing a Redis-backed sliding window counter with in-memory fallback for high availability.

## Component Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         Request Flow                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Request → ApiKeyAuthMiddleware → RateLimitMiddleware → API     │
│                    │                     │                       │
│                    │                     ▼                       │
│                    │            IRateLimitService                │
│                    │                     │                       │
│                    │         ┌──────────┴──────────┐            │
│                    │         ▼                     ▼            │
│                    │  RedisRateLimitService  InMemoryService    │
│                    │         │              (fallback)           │
│                    │         ▼                                   │
│                    │    Redis Server                             │
│                    │                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Service Interfaces

### IRateLimitService
```csharp
public interface IRateLimitService
{
    Task<RateLimitResult> CheckAndIncrementAsync(
        string key, 
        int limit, 
        CancellationToken cancellationToken = default);
}
```

### RateLimitResult
Returns comprehensive state for header generation:
- `IsAllowed` - Whether request should proceed
- `Limit` - Configured max requests
- `Remaining` - Requests left in window
- `ResetAt` - Unix timestamp of window reset
- `RetryAfterSeconds` - Seconds until retry
- `IsDegraded` - Whether using fallback mode

## Redis Implementation

### Key Structure
```
{prefix}{api_key_id}:{window_start_unix}
```
Example: `lockn-gen:ratelimit:abc123:1707000000`

### Algorithm (Sliding Window Counter)
1. Calculate current window start (floored to window duration)
2. Atomic INCR on window key
3. Set TTL on first request (window duration + 1s buffer)
4. Return count for limit check

### Advantages
- Atomic operations (no race conditions)
- Automatic expiry (no cleanup needed)
- Distributed state (works across instances)

## Fallback Strategy

### Trigger Conditions
- Redis connection failure
- Operation timeout
- Initial connection unavailable

### Behavior
1. Log warning on first fallback
2. Switch to InMemoryRateLimitService
3. Apply degraded mode limit (more restrictive)
4. Retry Redis connection every 30 seconds

### Degraded Mode
- Uses stricter limit (`DegradedModeLimit` config)
- Sets `X-RateLimit-Degraded: true` header
- Per-instance state (not distributed)

## Configuration

```json
{
  "RateLimiting": {
    "Enabled": true,
    "DefaultRequestsPerMinute": 60,
    "WindowDurationSeconds": 60,
    "DegradedModeLimit": 30,
    "Redis": {
      "ConnectionString": "localhost:6379",
      "KeyPrefix": "lockn-gen:ratelimit:",
      "ConnectTimeoutMs": 5000,
      "SyncTimeoutMs": 1000
    }
  }
}
```

## Response Headers

All rate-limited responses include:
| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Max requests per window |
| `X-RateLimit-Remaining` | Requests remaining |
| `X-RateLimit-Reset` | Unix timestamp of reset |
| `X-RateLimit-Degraded` | Present if using fallback |
| `Retry-After` | Seconds until retry (429 only) |

## 429 Response Format
```json
{
  "error": "rate_limited",
  "message": "Rate limit exceeded. Please retry after the specified time.",
  "retry_after_seconds": 45,
  "limit": 60,
  "reset_at": 1707000060
}
```

## File Structure

```
src/
├── LockNGen.Domain/Services/
│   └── IRateLimitService.cs
├── LockNGen.Infrastructure/RateLimiting/
│   ├── RateLimitOptions.cs
│   ├── RedisRateLimitService.cs
│   └── InMemoryRateLimitService.cs
└── LockNGen.Api/Middleware/
    └── RateLimitMiddleware.cs
```

## Dependencies

- StackExchange.Redis >= 2.8.0
- LOC-64 (Authentication) - For ApiKey entity
