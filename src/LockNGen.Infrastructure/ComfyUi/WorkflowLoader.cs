using LockNGen.Domain.DTOs;
using LockNGen.Domain.Services;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace LockNGen.Infrastructure.ComfyUi;

/// <summary>
/// Loads workflow templates from the filesystem.
/// </summary>
public class WorkflowLoader : IWorkflowLoader
{
    private readonly ComfyUiOptions _options;
    private readonly ILogger<WorkflowLoader> _logger;

    public WorkflowLoader(IOptions<ComfyUiOptions> options, ILogger<WorkflowLoader> logger)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task<ComfyWorkflow> LoadAsync(string templateName, GenerationParameters parameters, CancellationToken ct = default)
    {
        var filename = templateName.EndsWith(".json") ? templateName : $"{templateName}.json";
        var path = Path.Combine(_options.WorkflowsPath, filename);

        if (!File.Exists(path))
        {
            _logger.LogError("Workflow template not found: {Path}", path);
            throw new FileNotFoundException($"Workflow template not found: {filename}", path);
        }

        var templateJson = await File.ReadAllTextAsync(path, ct);
        _logger.LogDebug("Loaded workflow template {Name} with parameters: Steps={Steps}, Guidance={Guidance}", 
            templateName, parameters.Steps, parameters.Guidance);

        return ComfyWorkflow.FromTemplate(templateJson, parameters);
    }

    public Task<IReadOnlyList<string>> ListTemplatesAsync(CancellationToken ct = default)
    {
        if (!Directory.Exists(_options.WorkflowsPath))
        {
            _logger.LogWarning("Workflows directory does not exist: {Path}", _options.WorkflowsPath);
            return Task.FromResult<IReadOnlyList<string>>(Array.Empty<string>());
        }

        var templates = Directory.GetFiles(_options.WorkflowsPath, "*.json")
            .Select(Path.GetFileNameWithoutExtension)
            .Where(n => n != null)
            .Cast<string>()
            .ToList();

        return Task.FromResult<IReadOnlyList<string>>(templates);
    }
}
