using LockNGen.Api.DTOs;

namespace LockNGen.Api.Validation;

/// <summary>
/// Validates generation requests.
/// </summary>
public static class GenerationValidator
{
    public static IResult? Validate(GenerationRequest req)
    {
        if (string.IsNullOrWhiteSpace(req.Prompt))
            return Results.BadRequest(new { error = "Prompt is required" });
            
        if (req.Prompt.Length > 2000)
            return Results.BadRequest(new { error = "Prompt exceeds 2000 characters" });
            
        if (req.Width < 64 || req.Width > 2048 || req.Width % 64 != 0)
            return Results.BadRequest(new { error = "Width must be 64-2048 and divisible by 64" });
            
        if (req.Height < 64 || req.Height > 2048 || req.Height % 64 != 0)
            return Results.BadRequest(new { error = "Height must be 64-2048 and divisible by 64" });
            
        if (req.Steps < 1 || req.Steps > 100)
            return Results.BadRequest(new { error = "Steps must be 1-100" });
            
        if (req.Guidance < 0 || req.Guidance > 30)
            return Results.BadRequest(new { error = "Guidance must be 0-30" });
            
        return null; // Valid
    }
}
