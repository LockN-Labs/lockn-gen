using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using StackExchange.Redis;

namespace LockNGen.Infrastructure.RateLimiting;

/// <summary>
/// Redis-backed rate limiting service using sliding window counter algorithm.
/// Falls back to in-memory rate limiting when Redis is unavailable.
/// </summary>
public class RedisRateLimitService : IRateLimitService
{
    private readonly IConnectionMultiplexer? _redis;
    private readonly InMemoryRateLimitService _fallback;
    private readonly RateLimitOptions _options;
    private readonly ILogger<RedisRateLimitService> _logger;
    private bool _redisAvailable = true;
    private DateTime _lastRedisCheck = DateTime.MinValue;
    private readonly TimeSpan _redisCheckInterval = TimeSpan.FromSeconds(30);

    public RedisRateLimitService(
        IConnectionMultiplexer? redis,
        InMemoryRateLimitService fallback,
        IOptions<RateLimitOptions> options,
        ILogger<RedisRateLimitService> logger)
    {
        _redis = redis;
        _fallback = fallback;
        _options = options.Value;
        _logger = logger;
    }

    public async Task<RateLimitResult> CheckAndIncrementAsync(string key, int limit, CancellationToken cancellationToken = default)
    {
        // Check if we should try Redis again
        if (!_redisAvailable && DateTime.UtcNow - _lastRedisCheck > _redisCheckInterval)
        {
            _redisAvailable = true;
        }

        if (!_redisAvailable || _redis == null)
        {
            return await UseFallbackAsync(key, limit, cancellationToken);
        }

        try
        {
            return await CheckRedisAsync(key, limit, cancellationToken);
        }
        catch (RedisException ex)
        {
            _logger.LogWarning(ex, "Redis rate limit check failed, falling back to in-memory");
            _redisAvailable = false;
            _lastRedisCheck = DateTime.UtcNow;
            return await UseFallbackAsync(key, limit, cancellationToken);
        }
        catch (Exception ex) when (ex is TimeoutException or OperationCanceledException)
        {
            _logger.LogWarning(ex, "Redis operation timed out, falling back to in-memory");
            _redisAvailable = false;
            _lastRedisCheck = DateTime.UtcNow;
            return await UseFallbackAsync(key, limit, cancellationToken);
        }
    }

    private async Task<RateLimitResult> CheckRedisAsync(string key, int limit, CancellationToken cancellationToken)
    {
        var db = _redis!.GetDatabase();
        var now = DateTimeOffset.UtcNow;
        var windowDuration = TimeSpan.FromSeconds(_options.WindowDurationSeconds);
        var windowStart = new DateTimeOffset(now.Ticks - (now.Ticks % windowDuration.Ticks), TimeSpan.Zero);
        var resetAt = windowStart.Add(windowDuration);
        var ttl = resetAt - now + TimeSpan.FromSeconds(1); // Add 1s buffer

        var redisKey = $"{_options.Redis.KeyPrefix}{key}:{windowStart.ToUnixTimeSeconds()}";

        // Increment and get current count atomically
        var count = await db.StringIncrementAsync(redisKey);
        
        // Set expiry on first request of window
        if (count == 1)
        {
            await db.KeyExpireAsync(redisKey, ttl);
        }

        var remaining = Math.Max(0, limit - (int)count);
        var retryAfter = (int)Math.Ceiling((resetAt - now).TotalSeconds);

        return new RateLimitResult
        {
            IsAllowed = count <= limit,
            Limit = limit,
            Remaining = remaining,
            ResetAt = resetAt.ToUnixTimeSeconds(),
            RetryAfterSeconds = retryAfter,
            IsDegraded = false
        };
    }

    private async Task<RateLimitResult> UseFallbackAsync(string key, int limit, CancellationToken cancellationToken)
    {
        // Apply degraded mode limit (more restrictive)
        var degradedLimit = Math.Min(limit, _options.DegradedModeLimit);
        return await _fallback.CheckAndIncrementAsync(key, degradedLimit, cancellationToken);
    }
}
