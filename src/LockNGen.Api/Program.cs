using LockNGen.Api.Endpoints;
using LockNGen.Api.Middleware;
using LockNGen.Api.WebSockets;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.ComfyUi;
using LockNGen.Infrastructure.Data;
using LockNGen.Infrastructure.Services;
using LockNGen.Infrastructure.WebSockets;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.OpenApi.Models;

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
builder.Services.AddScoped<IApiKeyService, ApiKeyService>();

// Background workers
builder.Services.AddHostedService<GenerationWorker>();

// WebSocket progress broadcasting
builder.Services.AddSingleton<IProgressBroadcaster, ProgressBroadcaster>();
builder.Services.AddSingleton<ComfyUiProgressMonitor>();
builder.Services.AddHostedService(sp => sp.GetRequiredService<ComfyUiProgressMonitor>());
builder.Services.AddScoped<ProgressWebSocketHandler>();

// Health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>()
    .AddCheck<ComfyUiHealthCheck>("comfyui");

// OpenAPI/Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "LockN Gen API",
        Version = "v1",
        Description = "Text-to-image generation API powered by ComfyUI"
    });
    c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "API key authentication. Enter your API key (without 'Bearer' prefix).",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.ApiKey,
        Scheme = "Bearer"
    });
    c.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference { Type = ReferenceType.SecurityScheme, Id = "Bearer" }
            },
            Array.Empty<string>()
        }
    });
});

var app = builder.Build();

// Ensure database is created
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}

// Swagger UI (all environments for API visibility)
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "LockN Gen API v1");
    c.RoutePrefix = "swagger";
});

// WebSocket support
app.UseWebSockets();

// Authentication and rate limiting middleware
app.UseMiddleware<ApiKeyAuthMiddleware>();
app.UseMiddleware<RateLimitMiddleware>();

// Static files for frontend
app.UseDefaultFiles();
app.UseStaticFiles();

// Health endpoint
app.MapHealthChecks("/health");

// Root endpoint
app.MapGet("/", () => Results.Ok(new { 
    service = "LockN Gen", 
    version = "0.1.0",
    status = "running"
}));

// API Endpoints
app.MapGenerationEndpoints();
app.MapModelEndpoints();
app.MapProgressWebSocketEndpoints();
app.MapAdminEndpoints();

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
