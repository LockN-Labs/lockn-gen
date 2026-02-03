using LockNGen.Domain.Services;
using LockNGen.Infrastructure.ComfyUi;
using LockNGen.Infrastructure.Data;
using LockNGen.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;

var builder = WebApplication.CreateBuilder(args);

// Configuration
builder.Services.Configure<ComfyUiOptions>(
    builder.Configuration.GetSection(ComfyUiOptions.SectionName));

// Database configuration
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
if (string.IsNullOrEmpty(connectionString))
{
    // InMemory fallback for local dev without Docker
    builder.Services.AddDbContext<AppDbContext>(options =>
        options.UseInMemoryDatabase("LockNGen"));
}
else
{
    builder.Services.AddDbContext<AppDbContext>(options =>
        options.UseNpgsql(connectionString));
}

// ComfyUI client
builder.Services.AddHttpClient<IComfyUiClient, ComfyUiClient>();

// Services
builder.Services.AddSingleton<IWorkflowLoader, WorkflowLoader>();
builder.Services.AddScoped<IGenerationService, GenerationService>();

// Background worker
builder.Services.AddHostedService<GenerationWorker>();

// Health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>()
    .AddCheck<ComfyUiHealthCheck>("comfyui");

var app = builder.Build();

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Health endpoint
app.MapHealthChecks("/health");

// Root endpoint
app.MapGet("/", () => Results.Ok(new { 
    service = "LockN Gen", 
    version = "0.1.0",
    status = "running"
}));

app.Run();

/// <summary>
/// Health check for ComfyUI connectivity.
/// </summary>
public class ComfyUiHealthCheck : IHealthCheck
{
    private readonly IComfyUiClient _client;

    public ComfyUiHealthCheck(IComfyUiClient client) => _client = client;

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken ct = default)
    {
        try
        {
            var healthy = await _client.IsHealthyAsync(ct);
            return healthy 
                ? HealthCheckResult.Healthy("ComfyUI connected")
                : HealthCheckResult.Degraded("ComfyUI unreachable");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("ComfyUI error", ex);
        }
    }
}
