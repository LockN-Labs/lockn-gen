namespace LockNGen.Domain.DTOs;

/// <summary>
/// ComfyUI system statistics response.
/// </summary>
public record SystemStats
{
    public required SystemInfo System { get; init; }
    public required Dictionary<string, DeviceInfo> Devices { get; init; }
}

public record SystemInfo
{
    public required string Os { get; init; }
    public required string PythonVersion { get; init; }
    public int? EmbeddedPython { get; init; }
}

public record DeviceInfo
{
    public required string Name { get; init; }
    public required string Type { get; init; }
    public int Index { get; init; }
    public long VramTotal { get; init; }
    public long VramFree { get; init; }
    public string TorchVramTotal { get; init; } = "";
    public string TorchVramFree { get; init; } = "";
}
