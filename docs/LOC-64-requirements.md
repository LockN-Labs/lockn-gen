# LOC-64 Requirements: Authentication & API Keys

## Goal
Add API key authentication to LockN Gen, protecting all generation endpoints from unauthorized access while maintaining a smooth developer experience for authorized consumers.

## Acceptance Criteria
- [ ] API keys can be generated, listed, and revoked
- [ ] All `/api/*` endpoints require valid API key in Authorization header
- [ ] Invalid/missing keys return 401 Unauthorized with JSON error body
- [ ] Keys are stored hashed (not plaintext) in PostgreSQL
- [ ] Rate limiting by API key (100 req/min default)
- [ ] Existing WebSocket progress endpoint (`/api/ws/progress`) validates key on handshake

## Requirements

### 1. API Key Management
- Generate API keys with 256-bit entropy (base64-url encoded)
- Keys follow format: `lg_live_<32-char-base64>` (production) or `lg_test_<32-char-base64>` (test)
- Store hashed version (SHA-256) in `ApiKeys` table
- Support key metadata: name, created_at, last_used_at, expires_at, rate_limit

### 2. Key Validation Middleware
- Extract key from `Authorization: Bearer <key>` header
- Validate against hashed storage
- Update `last_used_at` on successful validation (debounced to 1/minute)
- Block invalid/missing keys with JSON error:
  ```json
  { "error": "unauthorized", "message": "Invalid or missing API key" }
  ```

### 3. Rate Limiting
- Per-key sliding window (1 minute)
- Default: 100 requests/minute
- Configurable per-key in database
- Return 429 with `Retry-After` header when exceeded:
  ```json
  { "error": "rate_limited", "message": "Rate limit exceeded", "retry_after": 42 }
  ```

### 4. Admin Endpoints (protected by admin key)
- `POST /api/admin/keys` — Create new API key (returns plaintext once)
- `GET /api/admin/keys` — List all keys (hashed, no plaintext)
- `DELETE /api/admin/keys/{id}` — Revoke key
- `GET /api/admin/keys/{id}/usage` — Key usage stats

### 5. Database Schema
```sql
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  key_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA-256 hex
  key_prefix VARCHAR(16) NOT NULL,        -- First 8 chars for identification
  is_admin BOOLEAN DEFAULT FALSE,
  rate_limit INT DEFAULT 100,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_used_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ
);

CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
```

### 6. WebSocket Authentication
- Validate API key in WebSocket handshake query param: `/api/ws/progress?api_key=<key>`
- Reject connection with 401 if invalid
- Apply same rate limiting to WebSocket connections

## Scope
**In scope:**
- `src/LockNGen.Domain/Entities/ApiKey.cs`
- `src/LockNGen.Domain/Services/IApiKeyService.cs`
- `src/LockNGen.Infrastructure/Services/ApiKeyService.cs`
- `src/LockNGen.Api/Middleware/ApiKeyAuthMiddleware.cs`
- `src/LockNGen.Api/Middleware/RateLimitMiddleware.cs`
- `src/LockNGen.Api/Endpoints/AdminEndpoints.cs`
- EF Core migration for ApiKeys table
- Update `Program.cs` to register middleware

**Out of scope:**
- OAuth/JWT authentication
- User accounts (keys are standalone)
- Complex RBAC (only admin vs regular key)

## Constraints
- Use SHA-256 for key hashing (fast, sufficient for API keys)
- In-memory rate limit cache (no Redis dependency)
- Follow existing project patterns (minimal APIs, EF Core)
- No new NuGet dependencies if possible

## Dependencies
- Existing EF Core setup (LOC-54)
- WebSocket progress handler (LOC-63)

## Performance Requirements
- <1ms key validation (hash lookup)
- Rate limit check adds <0.1ms overhead
