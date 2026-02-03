using System.Text.Json.Serialization;

namespace LockNGen.Domain.DTOs;

/// <summary>
/// ComfyUI prompt execution history.
/// </summary>
public record PromptHistory
{
    [JsonPropertyName("status")]
    public PromptStatus? Status { get; init; }
    
    [JsonPropertyName("outputs")]
    public Dictionary<string, NodeOutput>? Outputs { get; init; }
}

public record PromptStatus
{
    [JsonPropertyName("status_str")]
    public string StatusStr { get; init; } = "";
    
    [JsonPropertyName("completed")]
    public bool Completed { get; init; }
    
    [JsonPropertyName("messages")]
    public List<List<object>>? Messages { get; init; }
}

public record NodeOutput
{
    [JsonPropertyName("images")]
    public List<ImageOutput>? Images { get; init; }
}

public record ImageOutput
{
    [JsonPropertyName("filename")]
    public string Filename { get; init; } = "";
    
    [JsonPropertyName("subfolder")]
    public string Subfolder { get; init; } = "";
    
    [JsonPropertyName("type")]
    public string Type { get; init; } = "output";
}
