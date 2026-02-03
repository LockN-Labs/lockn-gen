# LOC-67 Requirements: Admin Dashboard & Metrics

## Phase 1: Requirements (Opus)

### Goal
Create an MVP admin dashboard providing real-time operational visibility for LockN Gen API operators.

### Acceptance Criteria
- [ ] GET /admin/stats returns real-time generation statistics (total, success, failed, in-progress)
- [ ] GET /admin/metrics returns API key usage data for the last 24h
- [ ] GET /admin/queue returns current ComfyUI queue depth
- [ ] Embedded HTML dashboard at /admin displays stats with auto-refresh
- [ ] All endpoints require admin API key (IsAdmin = true)
- [ ] Dashboard shows generation success/failure rates as a percentage

### Scope
**Files to create:**
- `src/LockNGen.Api/Controllers/AdminController.cs` - MVC controller with stats endpoints
- `src/LockNGen.Api/Views/Admin/Index.cshtml` - Embedded Razor view for dashboard
- `src/LockNGen.Api/DTOs/AdminStatsResponse.cs` - Response DTOs
- `src/LockNGen.Infrastructure/Services/MetricsService.cs` - Metrics aggregation service
- `tests/LockNGen.Tests/AdminControllerTests.cs` - Unit tests

**Existing code to reference:**
- `src/LockNGen.Api/Middleware/ApiKeyAuthMiddleware.cs` - For admin key validation pattern
- `src/LockNGen.Infrastructure/Data/AppDbContext.cs` - For generation queries
- `src/LockNGen.Domain/Models/Generation.cs` - Entity model

### Constraints
- Use existing API key auth middleware pattern (IsAdmin flag)
- No external frontend frameworks - use vanilla JS + Chart.js CDN
- Keep dashboard simple - single page, no SPA complexity
- Metrics from PostgreSQL (Generation table), not separate metrics store
- Follow existing code patterns in the project

### Out of Scope (Future)
- Historical metrics beyond 24h
- User-facing analytics
- Alert/notification system
- Custom date range queries
