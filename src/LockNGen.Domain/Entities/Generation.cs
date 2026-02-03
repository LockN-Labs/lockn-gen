namespace LockNGen.Domain.Entities;

public class Generation
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = string.Empty;
    public string Prompt { get; set; } = string.Empty;
    public string? NegativePrompt { get; set; }
    public string Model { get; set; } = "sdxl";
    public int Width { get; set; } = 1024;
    public int Height { get; set; } = 1024;
    public int Steps { get; set; } = 20;
    public float Guidance { get; set; } = 7.5f;
    public int? Seed { get; set; }
    public GenerationStatus Status { get; set; } = GenerationStatus.Queued;
    public string? PromptId { get; set; }
    public string? OutputPath { get; set; }
    public string? ThumbnailPath { get; set; }
    public string? ErrorMessage { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? UpdatedAt { get; set; }
    public DateTime? CompletedAt { get; set; }
    public int? DurationMs { get; set; }
}

public enum GenerationStatus
{
    Queued,
    Processing,
    Completed,
    Failed,
    Cancelled
}
