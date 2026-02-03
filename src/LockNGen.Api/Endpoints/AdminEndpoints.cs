using System.Text.Json;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;

namespace LockNGen.Api.Endpoints;

public static class AdminEndpoints
{
    public static void MapAdminEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/admin")
            .WithTags("Admin")
            .WithOpenApi();

        // API Key Management
        group.MapPost("/keys", CreateApiKey)
            .WithName("CreateApiKey")
            .WithSummary("Create a new API key")
            .Produces<CreateKeyResponse>(201)
            .Produces(401);

        group.MapGet("/keys", ListApiKeys)
            .WithName("ListApiKeys")
            .WithSummary("List all API keys")
            .Produces<IEnumerable<KeyResponse>>();

        group.MapDelete("/keys/{id:guid}", RevokeApiKey)
            .WithName("RevokeApiKey")
            .WithSummary("Revoke an API key")
            .Produces(204)
            .Produces(404);

        group.MapGet("/keys/{id:guid}/usage", GetApiKeyUsage)
            .WithName("GetApiKeyUsage")
            .WithSummary("Get API key usage statistics")
            .Produces<KeyUsageStats>()
            .Produces(404);

        // Metrics & Dashboard
        group.MapGet("/stats", GetStats)
            .WithName("GetStats")
            .WithSummary("Get real-time generation statistics")
            .Produces<AdminStatsDto>();

        group.MapGet("/metrics", GetMetrics)
            .WithName("GetMetrics")
            .WithSummary("Get API key usage metrics")
            .Produces<List<ApiKeyUsageDto>>();

        group.MapGet("/queue", GetQueueDepth)
            .WithName("GetQueueDepth")
            .WithSummary("Get current queue depth");

        // Dashboard UI (no auth for demo)
        app.MapGet("/admin", GetDashboard)
            .WithTags("Admin")
            .WithName("Dashboard")
            .WithSummary("Admin dashboard UI")
            .Produces<string>(contentType: "text/html")
            .ExcludeFromDescription();
    }

    private static async Task<IResult> GetStats(
        IMetricsService metricsService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized" }, statusCode: 401);

        var stats = await metricsService.GetStatsAsync();
        return Results.Ok(stats);
    }

    private static async Task<IResult> GetMetrics(
        IMetricsService metricsService,
        HttpContext context,
        int hours = 24)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized" }, statusCode: 401);

        var metrics = await metricsService.GetApiKeyUsageAsync(hours);
        return Results.Ok(metrics);
    }

    private static async Task<IResult> GetQueueDepth(
        IMetricsService metricsService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized" }, statusCode: 401);

        var depth = await metricsService.GetQueueDepthAsync();
        return Results.Ok(new { queueDepth = depth });
    }

    private static IResult GetDashboard()
    {
        return Results.Content(DashboardHtml, "text/html");
    }

    private static async Task<IResult> CreateApiKey(
        CreateKeyRequest request,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var (key, plainTextKey) = await apiKeyService.CreateKeyAsync(request.Name, request.IsAdmin, request.RateLimit);
        
        return Results.Created($"/api/admin/keys/{key.Id}", new CreateKeyResponse(
            key.Id,
            key.Name,
            key.KeyPrefix,
            plainTextKey,
            key.IsAdmin,
            key.RateLimit,
            key.CreatedAt
        ));
    }

    private static async Task<IResult> ListApiKeys(
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var keys = await apiKeyService.GetAllKeysAsync();
        return Results.Ok(keys.Select(k => new KeyResponse(
            k.Id,
            k.Name,
            k.KeyPrefix,
            k.IsAdmin,
            k.RateLimit,
            k.CreatedAt,
            k.LastUsedAt
        )));
    }

    private static async Task<IResult> RevokeApiKey(
        Guid id,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var success = await apiKeyService.RevokeKeyAsync(id);
        return success ? Results.NoContent() : Results.NotFound();
    }

    private static async Task<IResult> GetApiKeyUsage(
        Guid id,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var usage = await apiKeyService.GetKeyUsageAsync(id);
        return usage is null ? Results.NotFound() : Results.Ok(usage);
    }

    private static bool ValidateAdminKey(HttpContext context)
    {
        var adminKey = Environment.GetEnvironmentVariable("ADMIN_API_KEY");
        if (string.IsNullOrEmpty(adminKey)) return false;
        
        var providedKey = context.Request.Headers["X-Admin-Key"].FirstOrDefault();
        return adminKey == providedKey;
    }

    private const string DashboardHtml = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LockN Gen Admin</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, -apple-system, sans-serif; background: #0a0a0a; color: #e5e5e5; padding: 2rem; }
        h1 { font-size: 1.5rem; margin-bottom: 1.5rem; color: #fff; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
        .card { background: #1a1a1a; border-radius: 12px; padding: 1.5rem; border: 1px solid #333; }
        .card h3 { font-size: 0.875rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        .card .value { font-size: 2rem; font-weight: 600; color: #fff; }
        .card .value.success { color: #22c55e; }
        .card .value.error { color: #ef4444; }
        .card .value.pending { color: #f59e0b; }
        .chart-container { background: #1a1a1a; border-radius: 12px; padding: 1.5rem; border: 1px solid #333; height: 300px; }
        .refresh { font-size: 0.75rem; color: #666; margin-top: 1rem; }
        .auth-notice { background: #3730a3; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <h1>🔒 LockN Gen Admin Dashboard</h1>
    <div class="auth-notice">💡 API endpoints require X-Admin-Key header. Dashboard shows demo data when unauthenticated.</div>
    <div class="grid">
        <div class="card"><h3>Total Generations</h3><div class="value" id="total">-</div></div>
        <div class="card"><h3>Successful</h3><div class="value success" id="success">-</div></div>
        <div class="card"><h3>Failed</h3><div class="value error" id="failed">-</div></div>
        <div class="card"><h3>In Queue</h3><div class="value pending" id="queue">-</div></div>
        <div class="card"><h3>Success Rate</h3><div class="value" id="rate">-</div></div>
    </div>
    <div class="chart-container">
        <canvas id="chart"></canvas>
    </div>
    <p class="refresh">Auto-refreshes every 10 seconds</p>
    <script>
        let chart;
        const adminKey = localStorage.getItem('adminKey') || '';
        async function fetchStats() {
            try {
                const headers = adminKey ? { 'X-Admin-Key': adminKey } : {};
                const [statsRes, queueRes] = await Promise.all([
                    fetch('/api/admin/stats', { headers }),
                    fetch('/api/admin/queue', { headers })
                ]);
                if (!statsRes.ok || !queueRes.ok) {
                    document.getElementById('total').textContent = '?';
                    document.getElementById('success').textContent = '?';
                    document.getElementById('failed').textContent = '?';
                    document.getElementById('queue').textContent = '?';
                    document.getElementById('rate').textContent = '?';
                    return;
                }
                const stats = await statsRes.json();
                const queue = await queueRes.json();
                document.getElementById('total').textContent = stats.totalGenerations;
                document.getElementById('success').textContent = stats.successCount;
                document.getElementById('failed').textContent = stats.failedCount;
                document.getElementById('queue').textContent = queue.queueDepth;
                document.getElementById('rate').textContent = stats.successRate + '%';
                updateChart(stats);
            } catch (e) { console.error('Failed to fetch stats:', e); }
        }
        function updateChart(stats) {
            const ctx = document.getElementById('chart');
            const data = [stats.successCount, stats.failedCount, stats.inProgressCount];
            if (chart) { chart.data.datasets[0].data = data; chart.update(); }
            else {
                chart = new Chart(ctx, {
                    type: 'doughnut',
                    data: { labels: ['Completed', 'Failed', 'In Progress'], datasets: [{ data, backgroundColor: ['#22c55e', '#ef4444', '#f59e0b'] }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#e5e5e5' } } } }
                });
            }
        }
        fetchStats();
        setInterval(fetchStats, 10000);
    </script>
</body>
</html>
""";
}

// DTOs for admin endpoints
public record CreateKeyRequest(string Name, bool IsAdmin = false, int? RateLimit = null);

public record CreateKeyResponse(
    Guid Id,
    string Name,
    string KeyPrefix,
    string PlainTextKey,
    bool IsAdmin,
    int RateLimit,
    DateTime CreatedAt
);

public record KeyResponse(
    Guid Id,
    string Name,
    string KeyPrefix,
    bool IsAdmin,
    int RateLimit,
    DateTime CreatedAt,
    DateTime? LastUsedAt
);
