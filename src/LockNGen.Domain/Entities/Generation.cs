namespace LockNGen.Domain.Entities;

public class Generation
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Prompt { get; set; } = string.Empty;
    public string? NegativePrompt { get; set; }
    public string Model { get; set; } = "sdxl-1.0";
    public int Width { get; set; } = 1024;
    public int Height { get; set; } = 1024;
    public int Steps { get; set; } = 20;
    public double Guidance { get; set; } = 7.5;
    public long? Seed { get; set; }
    public GenerationStatus Status { get; set; } = GenerationStatus.Queued;
    public string? OutputPath { get; set; }
    public string? ThumbnailPath { get; set; }
    public string? ErrorMessage { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
    public int? DurationMs { get; set; }
}

public enum GenerationStatus
{
    Queued,
    Processing,
    Complete,
    Failed
}
