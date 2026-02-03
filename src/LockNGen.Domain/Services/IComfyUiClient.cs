using LockNGen.Domain.DTOs;

namespace LockNGen.Domain.Services;

/// <summary>
/// HTTP client for ComfyUI API communication.
/// </summary>
public interface IComfyUiClient
{
    /// <summary>
    /// Gets system statistics including GPU memory and queue status.
    /// </summary>
    Task<SystemStats> GetSystemStatsAsync(CancellationToken ct = default);
    
    /// <summary>
    /// Queues a workflow for execution.
    /// </summary>
    /// <returns>The prompt ID for tracking.</returns>
    Task<string> QueuePromptAsync(ComfyWorkflow workflow, CancellationToken ct = default);
    
    /// <summary>
    /// Gets the execution history for a prompt.
    /// </summary>
    Task<PromptHistory?> GetHistoryAsync(string promptId, CancellationToken ct = default);
    
    /// <summary>
    /// Downloads a generated image.
    /// </summary>
    Task<Stream> GetImageAsync(string filename, string subfolder = "", string type = "output", CancellationToken ct = default);
    
    /// <summary>
    /// Checks if ComfyUI is reachable and responsive.
    /// </summary>
    Task<bool> IsHealthyAsync(CancellationToken ct = default);
}
