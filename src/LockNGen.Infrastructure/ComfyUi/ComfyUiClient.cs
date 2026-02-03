using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using LockNGen.Domain.DTOs;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace LockNGen.Infrastructure.ComfyUi;

/// <summary>
/// HTTP client for ComfyUI API.
/// </summary>
public class ComfyUiClient : IComfyUiClient
{
    private readonly HttpClient _http;
    private readonly ILogger<ComfyUiClient> _logger;
    private readonly ComfyUiOptions _options;
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true
    };

    public ComfyUiClient(HttpClient http, IOptions<ComfyUiOptions> options, ILogger<ComfyUiClient> logger)
    {
        _http = http;
        _options = options.Value;
        _logger = logger;
        _http.BaseAddress = new Uri(_options.BaseUrl);
        _http.Timeout = TimeSpan.FromSeconds(_options.TimeoutSeconds);
    }

    public async Task<SystemStats> GetSystemStatsAsync(CancellationToken ct = default)
    {
        var response = await _http.GetAsync("/system_stats", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<SystemStats>(JsonOptions, ct) 
            ?? throw new InvalidOperationException("Failed to parse system stats");
    }

    public async Task<string> QueuePromptAsync(ComfyWorkflow workflow, CancellationToken ct = default)
    {
        var payload = new JsonObject
        {
            ["prompt"] = workflow.Prompt,
            ["client_id"] = workflow.ClientId
        };

        var content = new StringContent(payload.ToJsonString(), Encoding.UTF8, "application/json");
        var response = await _http.PostAsync("/prompt", content, ct);
        response.EnsureSuccessStatusCode();

        var result = await response.Content.ReadFromJsonAsync<JsonObject>(ct);
        var promptId = result?["prompt_id"]?.GetValue<string>();
        
        if (string.IsNullOrEmpty(promptId))
            throw new InvalidOperationException("No prompt_id in response");

        _logger.LogInformation("Queued prompt {PromptId}", promptId);
        return promptId;
    }

    public async Task<PromptHistory?> GetHistoryAsync(string promptId, CancellationToken ct = default)
    {
        var response = await _http.GetAsync($"/history/{promptId}", ct);
        if (!response.IsSuccessStatusCode)
            return null;

        var historyDict = await response.Content.ReadFromJsonAsync<Dictionary<string, PromptHistory>>(JsonOptions, ct);
        return historyDict?.GetValueOrDefault(promptId);
    }

    public async Task<Stream> GetImageAsync(string filename, string subfolder = "", string type = "output", CancellationToken ct = default)
    {
        var url = $"/view?filename={Uri.EscapeDataString(filename)}&type={type}";
        if (!string.IsNullOrEmpty(subfolder))
            url += $"&subfolder={Uri.EscapeDataString(subfolder)}";

        var response = await _http.GetAsync(url, ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadAsStreamAsync(ct);
    }

    public async Task<bool> IsHealthyAsync(CancellationToken ct = default)
    {
        try
        {
            var response = await _http.GetAsync("/system_stats", ct);
            return response.IsSuccessStatusCode;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "ComfyUI health check failed");
            return false;
        }
    }
}
