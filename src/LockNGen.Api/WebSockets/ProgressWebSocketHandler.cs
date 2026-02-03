using System.Net.WebSockets;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;

namespace LockNGen.Api.WebSockets;

/// <summary>
/// Handles WebSocket connections for progress updates.
/// </summary>
public class ProgressWebSocketHandler
{
    private readonly IProgressBroadcaster _broadcaster;
    private readonly ILogger<ProgressWebSocketHandler> _logger;

    public ProgressWebSocketHandler(
        IProgressBroadcaster broadcaster,
        ILogger<ProgressWebSocketHandler> logger)
    {
        _broadcaster = broadcaster;
        _logger = logger;
    }

    public async Task HandleAsync(HttpContext context, Guid? generationId)
    {
        if (!context.WebSockets.IsWebSocketRequest)
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsync("WebSocket connection required");
            return;
        }

        using var webSocket = await context.WebSockets.AcceptWebSocketAsync();
        _broadcaster.RegisterClient(webSocket, generationId);
        
        _logger.LogInformation(
            "Progress WebSocket connected. GenerationFilter: {GenerationId}, Total clients: {Count}",
            generationId?.ToString() ?? "all",
            _broadcaster.ClientCount
        );

        try
        {
            await ReceiveLoopAsync(webSocket, context.RequestAborted);
        }
        finally
        {
            _broadcaster.UnregisterClient(webSocket);
            _logger.LogInformation("Progress WebSocket disconnected. Total clients: {Count}", _broadcaster.ClientCount);
        }
    }

    private async Task ReceiveLoopAsync(WebSocket webSocket, CancellationToken cancellationToken)
    {
        var buffer = new byte[1024];
        
        while (webSocket.State == WebSocketState.Open && !cancellationToken.IsCancellationRequested)
        {
            try
            {
                var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), cancellationToken);
                
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    await webSocket.CloseAsync(
                        WebSocketCloseStatus.NormalClosure,
                        "Closing",
                        cancellationToken
                    );
                    break;
                }
                
                // We don't expect client messages, but handle ping/pong
                if (result.MessageType == WebSocketMessageType.Text)
                {
                    var message = System.Text.Encoding.UTF8.GetString(buffer, 0, result.Count);
                    if (message == "ping")
                    {
                        var pong = System.Text.Encoding.UTF8.GetBytes("pong");
                        await webSocket.SendAsync(
                            new ArraySegment<byte>(pong),
                            WebSocketMessageType.Text,
                            true,
                            cancellationToken
                        );
                    }
                }
            }
            catch (WebSocketException)
            {
                break;
            }
            catch (OperationCanceledException)
            {
                break;
            }
        }
    }
}
