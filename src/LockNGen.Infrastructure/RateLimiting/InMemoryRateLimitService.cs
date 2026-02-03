using System.Collections.Concurrent;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace LockNGen.Infrastructure.RateLimiting;

/// <summary>
/// In-memory rate limiting service. Used as fallback when Redis is unavailable.
/// </summary>
public class InMemoryRateLimitService : IRateLimitService, IDisposable
{
    private readonly ConcurrentDictionary<string, RateLimitEntry> _entries = new();
    private readonly RateLimitOptions _options;
    private readonly ILogger<InMemoryRateLimitService> _logger;
    private readonly Timer _cleanupTimer;
    private bool _disposed;

    public InMemoryRateLimitService(
        IOptions<RateLimitOptions> options,
        ILogger<InMemoryRateLimitService> logger)
    {
        _options = options.Value;
        _logger = logger;
        
        // Cleanup old entries every minute
        _cleanupTimer = new Timer(CleanupOldEntries, null, TimeSpan.FromMinutes(1), TimeSpan.FromMinutes(1));
    }

    public Task<RateLimitResult> CheckAndIncrementAsync(string key, int limit, CancellationToken cancellationToken = default)
    {
        var now = DateTimeOffset.UtcNow;
        var windowDuration = TimeSpan.FromSeconds(_options.WindowDurationSeconds);
        var windowStart = new DateTimeOffset(now.Ticks - (now.Ticks % windowDuration.Ticks), TimeSpan.Zero);
        var resetAt = windowStart.Add(windowDuration);

        var entry = _entries.AddOrUpdate(
            key,
            _ => new RateLimitEntry { WindowStart = windowStart, Count = 1 },
            (_, existing) =>
            {
                if (existing.WindowStart < windowStart)
                {
                    // New window
                    return new RateLimitEntry { WindowStart = windowStart, Count = 1 };
                }
                // Same window, increment
                existing.Count++;
                return existing;
            });

        var remaining = Math.Max(0, limit - entry.Count);
        var retryAfter = (int)Math.Ceiling((resetAt - now).TotalSeconds);

        return Task.FromResult(new RateLimitResult
        {
            IsAllowed = entry.Count <= limit,
            Limit = limit,
            Remaining = remaining,
            ResetAt = resetAt.ToUnixTimeSeconds(),
            RetryAfterSeconds = retryAfter,
            IsDegraded = true // In-memory is always considered degraded mode
        });
    }

    private void CleanupOldEntries(object? state)
    {
        if (_disposed) return;

        var threshold = DateTimeOffset.UtcNow.AddMinutes(-5);
        var removed = 0;

        foreach (var kvp in _entries)
        {
            if (kvp.Value.WindowStart < threshold)
            {
                if (_entries.TryRemove(kvp.Key, out _))
                {
                    removed++;
                }
            }
        }

        if (removed > 0)
        {
            _logger.LogDebug("Cleaned up {Count} expired rate limit entries", removed);
        }
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        _cleanupTimer.Dispose();
        GC.SuppressFinalize(this);
    }

    private class RateLimitEntry
    {
        public DateTimeOffset WindowStart { get; set; }
        public int Count { get; set; }
    }
}
