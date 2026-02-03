# LOC-64 Architecture: Authentication & API Keys

## Solution Design Approach

1. **Core Pattern**: Use existing minimal API/EF Core pattern with clean separation of domain entities, services, and middleware
2. **Security Model**: Store only hashed keys (SHA-256) in DB with salt from environment variable
3. **Rate Limiting**: In-memory cache with sliding window (no Redis) using ConcurrentDictionary
4. **Admin Flow**: Requires special admin key in header for management operations

## File List

| File | Purpose |
|---|---|
| `src/LockNGen.Domain/Entities/ApiKey.cs` | Entity model for API keys |
| `src/LockNGen.Domain/Services/IApiKeyService.cs` | Interface for key management operations |
| `src/LockNGen.Infrastructure/Services/ApiKeyService.cs` | Implementation of IApiKeyService with EF Core |
| `src/LockNGen.Api/Middleware/ApiKeyAuthMiddleware.cs` | Middleware for key validation and auth |
| `src/LockNGen.Api/Middleware/RateLimitMiddleware.cs` | Request rate limiting by API key |
| `src/LockNGen.Api/Endpoints/AdminEndpoints.cs` | Admin key management endpoints |
| `src/LockNGen.Infrastructure/Migrations/ApiKeyMigration.cs` | EF Core migration for api_keys table |
| `src/LockNGen.Api/Program.cs` | Add middleware registrations |

## Interfaces and Types

### IApiKeyService
```csharp
public interface IApiKeyService
{
    Task<ApiKey> CreateKeyAsync(string name, bool isAdmin, int? rateLimit = null);
    Task<ApiKey?> GetKeyByHashAsync(string keyHash);
    Task RevokeKeyAsync(Guid keyId);
    Task UpdateLastUsedAsync(Guid keyId);
    Task<int> GetRemainingRequestsAsync(Guid keyId);
}
```

### Admin DTOs
```csharp
public class CreateKeyRequest
{
    public string Name { get; set; } = null!;
    public bool IsAdmin { get; set; }
    public int? RateLimit { get; set; }
}

public class KeyResponse
{
    public Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string KeyPrefix { get; set; } = null!;
    public bool IsAdmin { get; set; }
    public int RateLimit { get; set; }
    public DateTime? ExpiresAt { get; set; }
}
```

## Data Flow: Key Validation

1. Request → ApiKeyAuthMiddleware
2. Extract bearer token → Compute SHA-256 hash
3. Query `api_keys` table by hash
4. Validate: not revoked/expired + active
5. If valid → Update last_used_at (debounced)
6. Pass to next middleware

## Security Considerations
- Key generation: Use `System.Security.Cryptography.RandomNumberGenerator`
- Hashing: SHA-256 with salt from `API_KEY_SALT` env var
- Error responses: Generic messages to avoid leaking validation info

## Rate Limit Implementation

```csharp
// In-memory cache structure
private readonly ConcurrentDictionary<Guid, RateLimitEntry> _rateLimits = 
    new ConcurrentDictionary<Guid, RateLimitEntry>();

// RateLimitMiddleware
public async Task InvokeAsync(HttpContext context, IApiKeyService keyService)
{
    var keyId = GetKeyIdFromContext(context);
    var entry = _rateLimits.GetOrAdd(keyId, id => new RateLimitEntry());
    
    if (entry.RequestCount >= entry.Limit)
    {
        context.Response.StatusCode = 429;
        await context.Response.WriteJsonAsync(new
        {
            error = "rate_limited",
            message = "Rate limit exceeded",
            retry_after = entry.ResetIn.TotalSeconds
        });
        return;
    }
    
    entry.Increment();
    await next(context);
}
```

## WebSocket Integration

- Extract key from query param: `?api_key=...`
- Same validation flow as regular endpoints
- Use same rate limit tracking
- Reject with 401 if invalid (WebSocket connection fails)

Next step: Run git commands to create draft PR for architecture review