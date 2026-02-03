namespace LockNGen.Infrastructure.RateLimiting;

/// <summary>
/// Configuration options for rate limiting.
/// </summary>
public class RateLimitOptions
{
    /// <summary>
    /// Configuration section name.
    /// </summary>
    public const string SectionName = "RateLimiting";

    /// <summary>
    /// Whether rate limiting is enabled.
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Default requests per minute for API keys without explicit limits.
    /// </summary>
    public int DefaultRequestsPerMinute { get; set; } = 60;

    /// <summary>
    /// Window duration in seconds.
    /// </summary>
    public int WindowDurationSeconds { get; set; } = 60;

    /// <summary>
    /// Rate limit to apply in degraded mode (when Redis is unavailable).
    /// </summary>
    public int DegradedModeLimit { get; set; } = 30;

    /// <summary>
    /// Redis configuration.
    /// </summary>
    public RedisOptions Redis { get; set; } = new();
}

/// <summary>
/// Redis connection options.
/// </summary>
public class RedisOptions
{
    /// <summary>
    /// Redis connection string.
    /// </summary>
    public string ConnectionString { get; set; } = "localhost:6379";

    /// <summary>
    /// Key prefix for rate limit entries.
    /// </summary>
    public string KeyPrefix { get; set; } = "lockn-gen:ratelimit:";

    /// <summary>
    /// Connection timeout in milliseconds.
    /// </summary>
    public int ConnectTimeoutMs { get; set; } = 5000;

    /// <summary>
    /// Sync timeout in milliseconds.
    /// </summary>
    public int SyncTimeoutMs { get; set; } = 1000;
}
