using LockNGen.Domain.DTOs;

namespace LockNGen.Domain.Services;

/// <summary>
/// Loads and parameterizes ComfyUI workflow templates.
/// </summary>
public interface IWorkflowLoader
{
    /// <summary>
    /// Loads a workflow template and substitutes parameters.
    /// </summary>
    Task<ComfyWorkflow> LoadAsync(string templateName, GenerationParameters parameters, CancellationToken ct = default);
    
    /// <summary>
    /// Lists available workflow templates.
    /// </summary>
    Task<IReadOnlyList<string>> ListTemplatesAsync(CancellationToken ct = default);
}
