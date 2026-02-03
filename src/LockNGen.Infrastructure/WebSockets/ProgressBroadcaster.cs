using System.Collections.Concurrent;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using LockNGen.Domain.DTOs;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;

namespace LockNGen.Infrastructure.WebSockets;

/// <summary>
/// Thread-safe broadcaster for WebSocket progress updates.
/// </summary>
public class ProgressBroadcaster : IProgressBroadcaster
{
    private readonly ConcurrentDictionary<WebSocket, ClientInfo> _clients = new();
    private readonly ILogger<ProgressBroadcaster> _logger;
    private readonly JsonSerializerOptions _jsonOptions;

    public ProgressBroadcaster(ILogger<ProgressBroadcaster> logger)
    {
        _logger = logger;
        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = false
        };
    }

    public int ClientCount => _clients.Count;

    public void RegisterClient(WebSocket socket, Guid? filterGenerationId = null)
    {
        var info = new ClientInfo(filterGenerationId, DateTime.UtcNow);
        if (_clients.TryAdd(socket, info))
        {
            _logger.LogDebug("Client registered. Total clients: {Count}", _clients.Count);
        }
    }

    public void UnregisterClient(WebSocket socket)
    {
        if (_clients.TryRemove(socket, out _))
        {
            _logger.LogDebug("Client unregistered. Total clients: {Count}", _clients.Count);
        }
    }

    public async Task BroadcastAsync(ProgressMessage message, CancellationToken cancellationToken = default)
    {
        var json = JsonSerializer.Serialize(message, _jsonOptions);
        var bytes = Encoding.UTF8.GetBytes(json);
        var segment = new ArraySegment<byte>(bytes);

        var tasks = new List<Task>();
        foreach (var (socket, info) in _clients)
        {
            // Skip if client is filtering for a different generation
            if (info.FilterGenerationId.HasValue && info.FilterGenerationId != message.GenerationId)
                continue;

            if (socket.State == WebSocketState.Open)
            {
                tasks.Add(SendSafeAsync(socket, segment, cancellationToken));
            }
            else
            {
                UnregisterClient(socket);
            }
        }

        await Task.WhenAll(tasks);
    }

    public async Task BroadcastToGenerationAsync(Guid generationId, ProgressMessage message, CancellationToken cancellationToken = default)
    {
        var json = JsonSerializer.Serialize(message, _jsonOptions);
        var bytes = Encoding.UTF8.GetBytes(json);
        var segment = new ArraySegment<byte>(bytes);

        var tasks = new List<Task>();
        foreach (var (socket, info) in _clients)
        {
            // Only send to clients filtering for this generation or all generations
            if (info.FilterGenerationId.HasValue && info.FilterGenerationId != generationId)
                continue;

            if (socket.State == WebSocketState.Open)
            {
                tasks.Add(SendSafeAsync(socket, segment, cancellationToken));
            }
            else
            {
                UnregisterClient(socket);
            }
        }

        await Task.WhenAll(tasks);
    }

    private async Task SendSafeAsync(WebSocket socket, ArraySegment<byte> data, CancellationToken cancellationToken)
    {
        try
        {
            await socket.SendAsync(data, WebSocketMessageType.Text, true, cancellationToken);
        }
        catch (WebSocketException ex)
        {
            _logger.LogWarning(ex, "Failed to send to WebSocket client");
            UnregisterClient(socket);
        }
        catch (OperationCanceledException)
        {
            // Expected on shutdown
        }
    }

    private record ClientInfo(Guid? FilterGenerationId, DateTime ConnectedAt);
}
