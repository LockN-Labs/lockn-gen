# LOC-65: Rate Limiting & Redis Integration

## Overview
Implement rate limiting for API endpoints using Redis as the backing store for distributed state management.

## Problem Statement
Currently, the API has no rate limiting, allowing unlimited requests per API key. This creates risk of:
- Resource exhaustion from runaway clients
- Unfair usage distribution
- Potential abuse

## Requirements

### Functional Requirements
1. **Per-Key Rate Limits**
   - Configurable requests/minute per API key
   - Default limits for keys without explicit configuration
   - Admin override capability

2. **Rate Limit Algorithm**
   - Sliding window counter algorithm
   - Smooth distribution without burst spikes
   - Configurable window duration (default: 1 minute)

3. **Redis Integration**
   - StackExchange.Redis client
   - Connection pooling
   - Automatic reconnection
   - Configurable connection string

4. **Response Headers**
   - `X-RateLimit-Limit`: Max requests per window
   - `X-RateLimit-Remaining`: Requests remaining
   - `X-RateLimit-Reset`: Unix timestamp of window reset
   - `Retry-After`: Seconds until retry (on 429)

5. **Graceful Degradation**
   - Fallback to in-memory rate limiting if Redis unavailable
   - Log warnings on fallback
   - Continue operation without hard failure

### Non-Functional Requirements
- < 5ms overhead per request
- No memory leaks from sliding window tracking
- Thread-safe operations

## Technical Approach

### Dependencies
- StackExchange.Redis (>= 2.7.0)
- Microsoft.Extensions.Caching.StackExchangeRedis

### Configuration
```json
{
  "RateLimiting": {
    "Enabled": true,
    "DefaultRequestsPerMinute": 60,
    "WindowDurationSeconds": 60,
    "Redis": {
      "ConnectionString": "localhost:6379",
      "InstanceName": "lockn-gen:"
    }
  }
}
```

### Middleware Flow
1. Extract API key from request
2. Check Redis for current window count
3. If under limit: increment and continue
4. If at/over limit: return 429 with headers
5. If Redis unavailable: fall back to in-memory

## Acceptance Criteria
- [ ] Redis client configured and tested
- [ ] Rate limit middleware implemented
- [ ] Per-key configuration support
- [ ] All response headers present
- [ ] Fallback to in-memory works
- [ ] Unit tests for rate limit logic
- [ ] Integration test with Redis container

## Out of Scope
- Dynamic rate limit adjustment
- Rate limit analytics/dashboard
- Distributed rate limiting across multiple instances (future)

## Dependencies
- LOC-64 (Authentication) - DONE ✅
