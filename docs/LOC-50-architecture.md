# LOC-50 Architecture

## Solution Design
- Core domain entity `ProviderMetrics` tracks health/latency data
- Health status DTOs for API responses
- Service interface for health monitoring logic
- Infrastructure implementation with health checks
- API endpoints for status retrieval

## File Changes
1. `src/LockNLogger.Domain/Entities/ProviderMetrics.cs`
2. `src/LockNLogger.Domain/DTOs/ProviderHealthStatus.cs`
3. `src/LockNLogger.Domain/Services/IProviderHealthService.cs`
4. `src/LockNLogger.Infrastructure/Services/ProviderHealthService.cs`
5. `src/LockNLogger.Api/Endpoints/ProviderHealthEndpoints.cs`
6. `src/LockNLogger.Domain/AppDbContext.cs` (update)
7. `src/LockNLogger.Api/Program.cs` (update)

## Interfaces/Types
```csharp
public interface IProviderHealthService {
  Task<ProviderHealthStatus> GetHealthStatus(string providerId);
}

public class ProviderHealthStatus {
  public string ProviderId { get; set; }
  public HealthStatus Status { get; set; }
  public TimeSpan Latency { get; set; }
}
```

## Phase 3 Subtasks
1. Create ProviderMetrics entity
2. Create health status DTO
3. Implement service interface
4. Write service implementation
5. Add API endpoints
6. Update DbContext
7. Integrate service in Program.cs
8. Verify build