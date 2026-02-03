using System.Text.Json;
using LockNGen.Domain.Services;

namespace LockNGen.Api.Middleware;

public class ApiKeyAuthMiddleware
{
    private readonly RequestDelegate _next;

    public ApiKeyAuthMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context, IApiKeyService apiKeyService)
    {
        var path = context.Request.Path.ToString().ToLowerInvariant();

        // Skip authentication for health, swagger, and static files
        if (path.StartsWith("/health") || 
            path.StartsWith("/swagger") ||
            path == "/" ||
            path.StartsWith("/css") ||
            path.StartsWith("/js") ||
            !path.StartsWith("/api"))
        {
            await _next(context);
            return;
        }

        // Admin endpoints have their own validation
        if (path.StartsWith("/api/admin"))
        {
            await _next(context);
            return;
        }

        var authHeader = context.Request.Headers.Authorization.FirstOrDefault();
        
        if (string.IsNullOrEmpty(authHeader) || !authHeader.StartsWith("Bearer "))
        {
            context.Response.StatusCode = 401;
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = "unauthorized", message = "API key required" }));
            return;
        }

        var token = authHeader["Bearer ".Length..].Trim();
        var apiKey = await apiKeyService.ValidateKeyAsync(token);

        if (apiKey == null)
        {
            context.Response.StatusCode = 401;
            context.Response.ContentType = "application/json";
            await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = "unauthorized", message = "Invalid or expired API key" }));
            return;
        }

        context.Items["ApiKey"] = apiKey;
        await _next(context);
    }
}
