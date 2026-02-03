using LockNGen.Domain.Services;

namespace LockNGen.Api.Endpoints;

/// <summary>
/// API endpoints for available models/workflows.
/// </summary>
public static class ModelEndpoints
{
    public static void MapModelEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/models")
            .WithTags("Models")
            .WithOpenApi();

        group.MapGet("/", ListModels)
            .WithName("ListModels")
            .WithSummary("List available workflow templates")
            .Produces<IEnumerable<string>>();
    }

    private static async Task<IResult> ListModels(
        IWorkflowLoader workflowLoader,
        CancellationToken ct)
    {
        var templates = await workflowLoader.ListTemplatesAsync(ct);
        return Results.Ok(templates);
    }
}
