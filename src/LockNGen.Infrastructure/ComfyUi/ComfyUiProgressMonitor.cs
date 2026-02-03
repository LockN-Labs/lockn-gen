using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using LockNGen.Domain.DTOs;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace LockNGen.Infrastructure.ComfyUi;

/// <summary>
/// Background service that monitors ComfyUI WebSocket for progress events.
/// </summary>
public class ComfyUiProgressMonitor : BackgroundService
{
    private readonly IProgressBroadcaster _broadcaster;
    private readonly ComfyUiOptions _options;
    private readonly ILogger<ComfyUiProgressMonitor> _logger;
    private readonly Dictionary<string, Guid> _promptToGeneration = new();
    
    public ComfyUiProgressMonitor(
        IProgressBroadcaster broadcaster,
        IOptions<ComfyUiOptions> options,
        ILogger<ComfyUiProgressMonitor> logger)
    {
        _broadcaster = broadcaster;
        _options = options.Value;
        _logger = logger;
    }

    /// <summary>
    /// Maps a ComfyUI prompt ID to a generation ID for progress tracking.
    /// </summary>
    public void MapPromptToGeneration(string promptId, Guid generationId)
    {
        _promptToGeneration[promptId] = generationId;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ConnectAndMonitorAsync(stoppingToken);
            }
            catch (Exception ex) when (!stoppingToken.IsCancellationRequested)
            {
                _logger.LogWarning(ex, "ComfyUI WebSocket connection failed, retrying in 5s");
                await Task.Delay(5000, stoppingToken);
            }
        }
    }

    private async Task ConnectAndMonitorAsync(CancellationToken stoppingToken)
    {
        using var ws = new ClientWebSocket();
        var wsUrl = $"ws://{_options.BaseUrl.Replace("http://", "").Replace("https://", "").TrimEnd('/')}/ws";
        
        _logger.LogInformation("Connecting to ComfyUI WebSocket at {Url}", wsUrl);
        
        try
        {
            await ws.ConnectAsync(new Uri(wsUrl), stoppingToken);
            _logger.LogInformation("Connected to ComfyUI WebSocket");
            
            var buffer = new byte[4096];
            var messageBuffer = new StringBuilder();
            
            while (ws.State == WebSocketState.Open && !stoppingToken.IsCancellationRequested)
            {
                var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), stoppingToken);
                
                if (result.MessageType == WebSocketMessageType.Close)
                {
                    _logger.LogInformation("ComfyUI WebSocket closed");
                    break;
                }
                
                messageBuffer.Append(Encoding.UTF8.GetString(buffer, 0, result.Count));
                
                if (result.EndOfMessage)
                {
                    var message = messageBuffer.ToString();
                    messageBuffer.Clear();
                    await ProcessComfyMessageAsync(message, stoppingToken);
                }
            }
        }
        catch (WebSocketException ex)
        {
            _logger.LogWarning(ex, "ComfyUI WebSocket error");
            throw;
        }
    }

    private async Task ProcessComfyMessageAsync(string message, CancellationToken cancellationToken)
    {
        try
        {
            using var doc = JsonDocument.Parse(message);
            var root = doc.RootElement;
            
            if (!root.TryGetProperty("type", out var typeElement))
                return;
            
            var type = typeElement.GetString();
            var data = root.TryGetProperty("data", out var dataElement) ? dataElement : default;
            
            var promptId = data.ValueKind == JsonValueKind.Object && 
                           data.TryGetProperty("prompt_id", out var pidElement) 
                           ? pidElement.GetString() 
                           : null;
            
            if (promptId == null || !_promptToGeneration.TryGetValue(promptId, out var generationId))
            {
                // Unknown prompt, skip
                return;
            }

            ProgressMessage? progressMessage = type switch
            {
                "execution_start" => new ProgressMessage(
                    ProgressMessage.Types.Started,
                    generationId,
                    new ProgressData(0),
                    DateTime.UtcNow
                ),
                
                "executing" => new ProgressMessage(
                    ProgressMessage.Types.Node,
                    generationId,
                    new ProgressData(
                        Progress: 0,
                        CurrentNode: data.TryGetProperty("node", out var nodeEl) ? nodeEl.GetString() : null
                    ),
                    DateTime.UtcNow
                ),
                
                "progress" => new ProgressMessage(
                    ProgressMessage.Types.Progress,
                    generationId,
                    new ProgressData(
                        Progress: data.TryGetProperty("max", out var maxEl) && maxEl.GetInt32() > 0
                            ? (int)(100.0 * data.GetProperty("value").GetInt32() / maxEl.GetInt32())
                            : 0,
                        Step: data.TryGetProperty("value", out var valEl) ? valEl.GetInt32() : null,
                        TotalSteps: data.TryGetProperty("max", out var maxEl2) ? maxEl2.GetInt32() : null
                    ),
                    DateTime.UtcNow
                ),
                
                "executed" => null, // Individual node completed, not final
                
                "execution_cached" => null, // Cached execution, skip
                
                _ => null
            };

            if (progressMessage != null)
            {
                await _broadcaster.BroadcastToGenerationAsync(generationId, progressMessage, cancellationToken);
            }
        }
        catch (JsonException ex)
        {
            _logger.LogDebug(ex, "Failed to parse ComfyUI message");
        }
    }

    /// <summary>
    /// Notify completion of a generation (called by GenerationService).
    /// </summary>
    public async Task NotifyCompletedAsync(Guid generationId, string? outputPath, CancellationToken cancellationToken = default)
    {
        var message = new ProgressMessage(
            ProgressMessage.Types.Completed,
            generationId,
            new ProgressData(100, PreviewUrl: outputPath != null ? $"/api/generations/{generationId}/image" : null),
            DateTime.UtcNow
        );
        await _broadcaster.BroadcastToGenerationAsync(generationId, message, cancellationToken);
        
        // Cleanup mapping
        var promptId = _promptToGeneration.FirstOrDefault(x => x.Value == generationId).Key;
        if (promptId != null)
            _promptToGeneration.Remove(promptId);
    }

    /// <summary>
    /// Notify failure of a generation.
    /// </summary>
    public async Task NotifyFailedAsync(Guid generationId, string error, CancellationToken cancellationToken = default)
    {
        var message = new ProgressMessage(
            ProgressMessage.Types.Failed,
            generationId,
            new ProgressData(0, Error: error),
            DateTime.UtcNow
        );
        await _broadcaster.BroadcastToGenerationAsync(generationId, message, cancellationToken);
        
        // Cleanup mapping
        var promptId = _promptToGeneration.FirstOrDefault(x => x.Value == generationId).Key;
        if (promptId != null)
            _promptToGeneration.Remove(promptId);
    }
}
