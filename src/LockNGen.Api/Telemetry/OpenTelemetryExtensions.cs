using LockNGen.Infrastructure.Telemetry;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace LockNGen.Api.Telemetry;

/// <summary>
/// Extension methods for configuring OpenTelemetry in the application.
/// </summary>
public static class OpenTelemetryExtensions
{
    private const string ServiceName = "lockn-gen";
    private const string ServiceVersion = "1.0.0";
    
    /// <summary>
    /// Adds OpenTelemetry tracing and metrics to the service collection.
    /// </summary>
    public static IServiceCollection AddGenerationTelemetry(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var endpoint = configuration["OTEL_EXPORTER_OTLP_ENDPOINT"] ?? "http://localhost:4317";
        
        services.AddOpenTelemetry()
            .ConfigureResource(resource => resource
                .AddService(
                    serviceName: ServiceName,
                    serviceVersion: ServiceVersion)
                .AddAttributes(new[]
                {
                    new KeyValuePair<string, object>("deployment.environment", 
                        configuration["ASPNETCORE_ENVIRONMENT"] ?? "Development")
                }))
            .WithTracing(tracing => tracing
                // Add both Api and Infrastructure activity sources
                .AddSource(ServiceName)
                .AddSource(GenerationInstrumentation.ServiceName)
                .AddAspNetCoreInstrumentation(options =>
                {
                    // Filter out health checks and swagger from traces
                    options.Filter = ctx =>
                        !ctx.Request.Path.StartsWithSegments("/health") &&
                        !ctx.Request.Path.StartsWithSegments("/swagger");
                })
                .AddHttpClientInstrumentation()
                .AddEntityFrameworkCoreInstrumentation()
                .AddOtlpExporter(options =>
                {
                    options.Endpoint = new Uri(endpoint);
                }))
            .WithMetrics(metrics => metrics
                // Add both Api and Infrastructure meters
                .AddMeter(ServiceName)
                .AddMeter(GenerationInstrumentation.ServiceName)
                .AddAspNetCoreInstrumentation()
                .AddHttpClientInstrumentation()
                .AddOtlpExporter(options =>
                {
                    options.Endpoint = new Uri(endpoint);
                }));
        
        return services;
    }
}
