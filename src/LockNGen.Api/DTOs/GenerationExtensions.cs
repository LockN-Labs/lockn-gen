using LockNGen.Domain.DTOs;
using LockNGen.Domain.Entities;

namespace LockNGen.Api.DTOs;

/// <summary>
/// Extension methods for mapping between entities and DTOs.
/// </summary>
public static class GenerationExtensions
{
    public static GenerationResponse ToResponse(this Generation entity) => new()
    {
        Id = entity.Id,
        Prompt = entity.Prompt,
        NegativePrompt = entity.NegativePrompt,
        Status = entity.Status.ToString(),
        Model = entity.Model,
        Steps = entity.Steps,
        Guidance = entity.Guidance,
        Width = entity.Width,
        Height = entity.Height,
        Seed = entity.Seed,
        ErrorMessage = entity.ErrorMessage,
        DurationMs = entity.DurationMs,
        CreatedAt = entity.CreatedAt,
        CompletedAt = entity.CompletedAt
    };
    
    public static GenerationParameters ToParameters(this GenerationRequest request) => new()
    {
        Prompt = request.Prompt,
        NegativePrompt = request.NegativePrompt,
        Steps = request.Steps,
        Guidance = request.Guidance,
        Seed = request.Seed == -1 ? null : request.Seed,
        Width = request.Width,
        Height = request.Height,
        Model = request.Model
    };
}
