namespace LockNGen.Domain.DTOs;

/// <summary>
/// Progress update message sent to WebSocket clients.
/// </summary>
public record ProgressMessage(
    string Type,
    Guid GenerationId,
    ProgressData? Data,
    DateTime Timestamp
)
{
    public static class Types
    {
        public const string Started = "generation.started";
        public const string Progress = "generation.progress";
        public const string Node = "generation.node";
        public const string Preview = "generation.preview";
        public const string Completed = "generation.completed";
        public const string Failed = "generation.failed";
        public const string Cancelled = "generation.cancelled";
    }
}

/// <summary>
/// Progress data payload.
/// </summary>
public record ProgressData(
    int Progress,
    string? CurrentNode = null,
    int? Step = null,
    int? TotalSteps = null,
    string? PreviewUrl = null,
    string? Error = null
);
