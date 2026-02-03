using System.Net.WebSockets;
using LockNGen.Domain.DTOs;

namespace LockNGen.Domain.Services;

/// <summary>
/// Broadcasts progress updates to connected WebSocket clients.
/// </summary>
public interface IProgressBroadcaster
{
    /// <summary>
    /// Broadcast a progress message to all connected clients.
    /// </summary>
    Task BroadcastAsync(ProgressMessage message, CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Broadcast a progress message to clients subscribed to a specific generation.
    /// </summary>
    Task BroadcastToGenerationAsync(Guid generationId, ProgressMessage message, CancellationToken cancellationToken = default);
    
    /// <summary>
    /// Register a client WebSocket connection.
    /// </summary>
    /// <param name="socket">The WebSocket connection.</param>
    /// <param name="filterGenerationId">Optional generation ID to filter messages.</param>
    void RegisterClient(WebSocket socket, Guid? filterGenerationId = null);
    
    /// <summary>
    /// Unregister a client WebSocket connection.
    /// </summary>
    void UnregisterClient(WebSocket socket);
    
    /// <summary>
    /// Get the count of connected clients.
    /// </summary>
    int ClientCount { get; }
}
