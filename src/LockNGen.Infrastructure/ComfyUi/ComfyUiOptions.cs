namespace LockNGen.Infrastructure.ComfyUi;

/// <summary>
/// Configuration options for ComfyUI integration.
/// </summary>
public class ComfyUiOptions
{
    public const string SectionName = "ComfyUi";
    
    public string BaseUrl { get; set; } = "http://localhost:8188";
    public int TimeoutSeconds { get; set; } = 300;
    public int PollIntervalMs { get; set; } = 2000;
    public int MaxConcurrentGenerations { get; set; } = 1;
    public string WorkflowsPath { get; set; } = "./workflows";
    public string OutputPath { get; set; } = "./outputs";
}
