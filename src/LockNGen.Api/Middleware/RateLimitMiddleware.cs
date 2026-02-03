using System.Collections.Concurrent;
using System.Text.Json;
using LockNGen.Domain.Entities;

namespace LockNGen.Api.Middleware;

public class RateLimitMiddleware
{
    private readonly RequestDelegate _next;
    private static readonly ConcurrentDictionary<Guid, RateLimitEntry> _rateLimits = new();
    private static DateTime _lastCleanup = DateTime.UtcNow;

    public RateLimitMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        if (!context.Items.TryGetValue("ApiKey", out var apiKeyObj) || apiKeyObj is not ApiKey apiKey)
        {
            await _next(context);
            return;
        }

        var now = DateTime.UtcNow;
        var entry = _rateLimits.GetOrAdd(apiKey.Id, _ => new RateLimitEntry(now));

        // Reset window if more than 1 minute old
        if ((now - entry.WindowStart).TotalMinutes >= 1)
        {
            entry.Reset(now);
        }

        entry.Increment();

        if (entry.RequestCount > apiKey.RateLimit)
        {
            var retryAfter = (int)Math.Ceiling(60 - (now - entry.WindowStart).TotalSeconds);
            context.Response.StatusCode = 429;
            context.Response.ContentType = "application/json";
            context.Response.Headers.RetryAfter = retryAfter.ToString();
            
            await context.Response.WriteAsync(JsonSerializer.Serialize(new
            {
                error = "rate_limited",
                message = "Rate limit exceeded",
                retry_after = retryAfter
            }));
            return;
        }

        await _next(context);

        // Cleanup old entries periodically
        if ((now - _lastCleanup).TotalMinutes >= 5)
        {
            CleanupOldEntries(now);
        }
    }

    private static void CleanupOldEntries(DateTime now)
    {
        _lastCleanup = now;
        var threshold = now.AddMinutes(-5);
        
        foreach (var kvp in _rateLimits)
        {
            if (kvp.Value.WindowStart < threshold)
            {
                _rateLimits.TryRemove(kvp.Key, out _);
            }
        }
    }

    private class RateLimitEntry
    {
        private int _requestCount;
        public DateTime WindowStart { get; private set; }
        public int RequestCount => _requestCount;

        public RateLimitEntry(DateTime windowStart)
        {
            WindowStart = windowStart;
            _requestCount = 0;
        }

        public void Increment() => Interlocked.Increment(ref _requestCount);

        public void Reset(DateTime windowStart)
        {
            WindowStart = windowStart;
            Interlocked.Exchange(ref _requestCount, 0);
        }
    }
}
