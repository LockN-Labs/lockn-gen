namespace LockNGen.Api.DTOs;

/// <summary>
/// Response model for generation details.
/// </summary>
public record GenerationResponse
{
    public Guid Id { get; init; }
    public string Prompt { get; init; } = "";
    public string? NegativePrompt { get; init; }
    public string Status { get; init; } = "";
    public string? Model { get; init; }
    public int? Steps { get; init; }
    public float? Guidance { get; init; }
    public int? Width { get; init; }
    public int? Height { get; init; }
    public int? Seed { get; init; }
    public string? ErrorMessage { get; init; }
    public long? DurationMs { get; init; }
    public DateTime CreatedAt { get; init; }
    public DateTime? CompletedAt { get; init; }
}
