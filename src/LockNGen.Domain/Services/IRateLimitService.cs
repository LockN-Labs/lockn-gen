namespace LockNGen.Domain.Services;

/// <summary>
/// Rate limiting service interface for tracking and enforcing API request limits.
/// </summary>
public interface IRateLimitService
{
    /// <summary>
    /// Checks if the request should be allowed and increments the counter.
    /// </summary>
    /// <param name="key">Unique identifier for the rate limit bucket (e.g., API key ID).</param>
    /// <param name="limit">Maximum requests allowed per window.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Rate limit result with current state.</returns>
    Task<RateLimitResult> CheckAndIncrementAsync(string key, int limit, CancellationToken cancellationToken = default);
}

/// <summary>
/// Result of a rate limit check.
/// </summary>
public record RateLimitResult
{
    /// <summary>
    /// Whether the request is allowed.
    /// </summary>
    public required bool IsAllowed { get; init; }

    /// <summary>
    /// Maximum requests allowed per window.
    /// </summary>
    public required int Limit { get; init; }

    /// <summary>
    /// Remaining requests in the current window.
    /// </summary>
    public required int Remaining { get; init; }

    /// <summary>
    /// Unix timestamp when the current window resets.
    /// </summary>
    public required long ResetAt { get; init; }

    /// <summary>
    /// Seconds until the window resets (for Retry-After header).
    /// </summary>
    public required int RetryAfterSeconds { get; init; }

    /// <summary>
    /// Whether this result came from a fallback (degraded) mode.
    /// </summary>
    public bool IsDegraded { get; init; }
}
