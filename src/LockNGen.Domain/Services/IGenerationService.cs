using LockNGen.Domain.DTOs;
using LockNGen.Domain.Entities;

namespace LockNGen.Domain.Services;

/// <summary>
/// Manages the generation queue and lifecycle.
/// </summary>
public interface IGenerationService
{
    /// <summary>
    /// Queues a new generation request.
    /// </summary>
    Task<Generation> QueueAsync(GenerationParameters request, CancellationToken ct = default);
    
    /// <summary>
    /// Gets generation by ID with current status.
    /// </summary>
    Task<Generation?> GetAsync(Guid id, CancellationToken ct = default);
    
    /// <summary>
    /// Lists generations with optional filters.
    /// </summary>
    Task<IReadOnlyList<Generation>> ListAsync(int skip = 0, int take = 20, CancellationToken ct = default);
    
    /// <summary>
    /// Cancels a queued generation.
    /// </summary>
    Task<bool> CancelAsync(Guid id, CancellationToken ct = default);
    
    /// <summary>
    /// Gets the output image stream for a completed generation.
    /// </summary>
    Task<Stream?> GetImageStreamAsync(Guid id, CancellationToken ct = default);
}
