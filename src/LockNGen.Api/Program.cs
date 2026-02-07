using LockNGen.Api.Endpoints;
using LockNGen.Api.Middleware;
using LockNGen.Api.Telemetry;
using LockNGen.Api.WebSockets;
using LockNGen.Domain.Services;
using LockNGen.Infrastructure.ComfyUi;
using LockNGen.Infrastructure.Data;
using LockNGen.Infrastructure.RateLimiting;
using LockNGen.Infrastructure.Services;
using LockNGen.Infrastructure.WebSockets;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.OpenApi.Models;
using StackExchange.Redis;

var builder = WebApplication.CreateBuilder(args);

// OpenTelemetry observability
builder.Services.AddGenerationTelemetry(builder.Configuration);

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
builder.Services.AddScoped<IMetricsService, MetricsService>();

// Rate limiting
builder.Services.Configure<RateLimitOptions>(
    builder.Configuration.GetSection(RateLimitOptions.SectionName));

var redisConfig = builder.Configuration.GetSection("RateLimiting:Redis");
var redisConnectionString = redisConfig.GetValue<string>("ConnectionString");
if (!string.IsNullOrEmpty(redisConnectionString))
{
    try
    {
        var redisOptions = ConfigurationOptions.Parse(redisConnectionString);
        redisOptions.ConnectTimeout = redisConfig.GetValue("ConnectTimeoutMs", 5000);
        redisOptions.SyncTimeout = redisConfig.GetValue("SyncTimeoutMs", 1000);
        redisOptions.AbortOnConnectFail = false;
        
        builder.Services.AddSingleton<IConnectionMultiplexer>(
            ConnectionMultiplexer.Connect(redisOptions));
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Failed to connect to Redis: {ex.Message}. Rate limiting will use in-memory fallback.");
        builder.Services.AddSingleton<IConnectionMultiplexer?>(sp => null);
    }
}
else
{
    builder.Services.AddSingleton<IConnectionMultiplexer?>(sp => null);
}

builder.Services.AddSingleton<InMemoryRateLimitService>();
builder.Services.AddSingleton<IRateLimitService, RedisRateLimitService>();

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

// Database initialization
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    var logger = scope.ServiceProvider.GetRequiredService<ILogger<Program>>();
    
    if (db.Database.IsNpgsql())
    {
        // Apply pending migrations for PostgreSQL
        logger.LogInformation("Applying database migrations...");
        db.Database.Migrate();
        logger.LogInformation("Database migrations applied successfully");
    }
    else
    {
        // Use EnsureCreated for InMemory database
        db.Database.EnsureCreated();
        logger.LogInformation("InMemory database created");
    }
    
    // Seed development API key if none exists
    if (app.Environment.IsDevelopment() && !db.ApiKeys.Any())
    {
        var devKey = new LockNGen.Domain.Entities.ApiKey
        {
            Id = Guid.Parse("00000000-0000-0000-0000-000000000001"),
            Name = "Development Key",
            KeyHash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", // SHA256 of empty string
            KeyPrefix = "dev_",
            IsAdmin = true,
            RateLimit = 1000,
            CreatedAt = DateTime.UtcNow
        };
        db.ApiKeys.Add(devKey);
        db.SaveChanges();
        logger.LogInformation("Development API key seeded: dev_*** (use any key starting with 'dev_' in development)");
    }
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

// Static files for frontend (landing.html as default)
var defaultFilesOptions = new DefaultFilesOptions();
defaultFilesOptions.DefaultFileNames.Clear();
defaultFilesOptions.DefaultFileNames.Add("landing.html");
app.UseDefaultFiles(defaultFilesOptions);
app.UseStaticFiles();

// Health endpoint
app.MapHealthChecks("/health");

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
