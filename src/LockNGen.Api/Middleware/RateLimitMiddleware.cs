using System.Text.Json;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;

namespace LockNGen.Api.Middleware;

/// <summary>
/// Middleware for enforcing API rate limits with proper headers.
/// </summary>
public class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RateLimitMiddleware> _logger;

    public RateLimitMiddleware(RequestDelegate next, ILogger<RateLimitMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context, IRateLimitService rateLimitService)
    {
        // Skip rate limiting for health checks and swagger
        var path = context.Request.Path.Value?.ToLowerInvariant() ?? "";
        if (path.StartsWith("/health") || path.StartsWith("/swagger"))
        {
            await _next(context);
            return;
        }

        // Get API key from context (set by ApiKeyAuthMiddleware)
        if (!context.Items.TryGetValue("ApiKey", out var apiKeyObj) || apiKeyObj is not ApiKey apiKey)
        {
            await _next(context);
            return;
        }

        var key = apiKey.Id.ToString();
        var limit = apiKey.RateLimit;

        var result = await rateLimitService.CheckAndIncrementAsync(key, limit, context.RequestAborted);

        // Always add rate limit headers
        context.Response.Headers["X-RateLimit-Limit"] = result.Limit.ToString();
        context.Response.Headers["X-RateLimit-Remaining"] = result.Remaining.ToString();
        context.Response.Headers["X-RateLimit-Reset"] = result.ResetAt.ToString();

        if (result.IsDegraded)
        {
            context.Response.Headers["X-RateLimit-Degraded"] = "true";
        }

        if (!result.IsAllowed)
        {
            _logger.LogInformation(
                "Rate limit exceeded for API key {KeyId}: {Count}/{Limit}",
                apiKey.Id,
                result.Limit - result.Remaining + 1,
                result.Limit);

            context.Response.StatusCode = 429;
            context.Response.ContentType = "application/json";
            context.Response.Headers["Retry-After"] = result.RetryAfterSeconds.ToString();

            await context.Response.WriteAsync(JsonSerializer.Serialize(new
            {
                error = "rate_limited",
                message = "Rate limit exceeded. Please retry after the specified time.",
                retry_after_seconds = result.RetryAfterSeconds,
                limit = result.Limit,
                reset_at = result.ResetAt
            }));
            return;
        }

        await _next(context);
    }
}
