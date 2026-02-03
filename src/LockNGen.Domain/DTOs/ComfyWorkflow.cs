using System.Text.Json;
using System.Text.Json.Nodes;

namespace LockNGen.Domain.DTOs;

/// <summary>
/// ComfyUI workflow definition with parameter substitution.
/// </summary>
public class ComfyWorkflow
{
    public JsonObject Prompt { get; set; } = new();
    public string? ClientId { get; set; }

    /// <summary>
    /// Creates a workflow from a JSON template with parameter substitution.
    /// </summary>
    public static ComfyWorkflow FromTemplate(string templateJson, GenerationParameters parameters)
    {
        var json = templateJson
            .Replace("{{prompt}}", EscapeJson(parameters.Prompt))
            .Replace("{{negative_prompt}}", EscapeJson(parameters.NegativePrompt ?? ""))
            .Replace("{{seed}}", parameters.Seed?.ToString() ?? "-1")
            .Replace("{{steps}}", parameters.Steps.ToString())
            .Replace("{{cfg}}", parameters.Guidance.ToString("F1"))
            .Replace("{{width}}", parameters.Width.ToString())
            .Replace("{{height}}", parameters.Height.ToString());

        var prompt = JsonNode.Parse(json)?.AsObject() ?? new JsonObject();
        
        return new ComfyWorkflow
        {
            Prompt = prompt,
            ClientId = Guid.NewGuid().ToString()
        };
    }

    private static string EscapeJson(string value)
        => value.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n");
}

/// <summary>
/// Parameters for image generation.
/// </summary>
public record GenerationParameters
{
    public required string Prompt { get; init; }
    public string? NegativePrompt { get; init; }
    public int Steps { get; init; } = 20;
    public float Guidance { get; init; } = 7.5f;
    public int? Seed { get; init; }
    public int Width { get; init; } = 1024;
    public int Height { get; init; } = 1024;
    public string Model { get; init; } = "sdxl";
}
