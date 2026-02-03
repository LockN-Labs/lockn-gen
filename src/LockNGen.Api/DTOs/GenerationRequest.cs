namespace LockNGen.Api.DTOs;

/// <summary>
/// Request model for queueing a new image generation.
/// </summary>
public record GenerationRequest
{
    /// <summary>
    /// The text prompt describing the image to generate.
    /// </summary>
    public required string Prompt { get; init; }
    
    /// <summary>
    /// Optional negative prompt to exclude elements from generation.
    /// </summary>
    public string? NegativePrompt { get; init; }
    
    /// <summary>
    /// Workflow template to use (default: txt2img-sdxl).
    /// </summary>
    public string Model { get; init; } = "txt2img-sdxl";
    
    /// <summary>
    /// Number of inference steps (1-100, default: 20).
    /// </summary>
    public int Steps { get; init; } = 20;
    
    /// <summary>
    /// Classifier-free guidance scale (0-30, default: 7.5).
    /// </summary>
    public float Guidance { get; init; } = 7.5f;
    
    /// <summary>
    /// Output image width in pixels (64-2048, must be divisible by 64).
    /// </summary>
    public int Width { get; init; } = 1024;
    
    /// <summary>
    /// Output image height in pixels (64-2048, must be divisible by 64).
    /// </summary>
    public int Height { get; init; } = 1024;
    
    /// <summary>
    /// Random seed (-1 for random, or specific value for reproducibility).
    /// </summary>
    public int Seed { get; init; } = -1;
}
