using LockNGen.Api.DTOs;
using LockNGen.Api.Telemetry;
using LockNGen.Api.Validation;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;

namespace LockNGen.Api.Endpoints;

/// <summary>
/// API endpoints for image generation.
/// </summary>
public static class GenerationEndpoints
{
    public static void MapGenerationEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/generations")
            .WithTags("Generations")
            .WithOpenApi();

        group.MapPost("/", QueueGeneration)
            .WithName("QueueGeneration")
            .WithSummary("Queue a new image generation request")
            .Produces<GenerationResponse>(201)
            .ProducesValidationProblem();

        group.MapGet("/", ListGenerations)
            .WithName("ListGenerations")
            .WithSummary("List generations with pagination")
            .Produces<PagedResponse<GenerationResponse>>();

        group.MapGet("/{id:guid}", GetGeneration)
            .WithName("GetGeneration")
            .WithSummary("Get generation by ID")
            .Produces<GenerationResponse>()
            .Produces(404);

        group.MapDelete("/{id:guid}", CancelGeneration)
            .WithName("CancelGeneration")
            .WithSummary("Cancel a queued generation")
            .Produces(204)
            .Produces(404)
            .Produces(409);

        group.MapGet("/{id:guid}/image", GetGenerationImage)
            .WithName("GetGenerationImage")
            .WithSummary("Get generated image")
            .Produces(200, contentType: "image/png")
            .Produces(404);
    }

    private static async Task<IResult> QueueGeneration(
        GenerationRequest request,
        IGenerationService generationService,
        CancellationToken ct)
    {
        var validationError = GenerationValidator.Validate(request);
        if (validationError is not null)
            return validationError;

        var generation = await generationService.QueueAsync(request.ToParameters(), ct);
        
        // Record telemetry for the incoming request
        GenerationTelemetry.RecordGenerationRequest(
            request.Model,
            request.Width,
            request.Height);
        
        // Estimate cost based on resolution and steps (simple formula)
        var pixels = request.Width * request.Height;
        var costEstimate = pixels / 1_000_000.0 * request.Steps * 0.01; // 0.01 credits per megapixel-step
        GenerationTelemetry.RecordGenerationCost(
            request.Model,
            request.Width,
            request.Height,
            request.Steps,
            costEstimate);
        
        return Results.Created($"/api/generations/{generation.Id}", generation.ToResponse());
    }

    private static async Task<IResult> ListGenerations(
        IGenerationService generationService,
        int page = 1,
        int pageSize = 20,
        GenerationStatus? status = null,
        CancellationToken ct = default)
    {
        var skip = (page - 1) * pageSize;
        var generations = await generationService.ListAsync(skip, pageSize, ct);
        
        // Filter by status if provided
        var filtered = status.HasValue 
            ? generations.Where(g => g.Status == status.Value).ToList()
            : generations;

        return Results.Ok(new PagedResponse<GenerationResponse>
        {
            Items = filtered.Select(g => g.ToResponse()).ToList(),
            Page = page,
            PageSize = pageSize,
            TotalItems = filtered.Count // Note: actual total requires separate count query
        });
    }

    private static async Task<IResult> GetGeneration(
        Guid id,
        IGenerationService generationService,
        CancellationToken ct)
    {
        var generation = await generationService.GetAsync(id, ct);
        return generation is null 
            ? Results.NotFound(new { error = "Generation not found" }) 
            : Results.Ok(generation.ToResponse());
    }

    private static async Task<IResult> CancelGeneration(
        Guid id,
        IGenerationService generationService,
        CancellationToken ct)
    {
        var generation = await generationService.GetAsync(id, ct);
        if (generation is null)
            return Results.NotFound(new { error = "Generation not found" });

        if (generation.Status != GenerationStatus.Queued)
            return Results.Conflict(new { error = $"Cannot cancel generation with status {generation.Status}" });

        var cancelled = await generationService.CancelAsync(id, ct);
        
        if (cancelled)
        {
            GenerationTelemetry.RecordGenerationCancelled(generation.Model);
        }
        
        return cancelled ? Results.NoContent() : Results.NotFound();
    }

    private static async Task<IResult> GetGenerationImage(
        Guid id,
        IGenerationService generationService,
        CancellationToken ct)
    {
        var generation = await generationService.GetAsync(id, ct);
        if (generation is null)
            return Results.NotFound(new { error = "Generation not found" });

        if (generation.Status != GenerationStatus.Completed)
            return Results.NotFound(new { error = "Image not available - generation not completed" });

        var stream = await generationService.GetImageStreamAsync(id, ct);
        if (stream is null)
            return Results.NotFound(new { error = "Image file not found" });

        return Results.File(stream, "image/png", $"{id}.png");
    }
}
