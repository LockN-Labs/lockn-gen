using System.Text.Json;
using LockNGen.Domain.Entities;
using LockNGen.Domain.Services;

namespace LockNGen.Api.Endpoints;

public static class AdminEndpoints
{
    public static void MapAdminEndpoints(this WebApplication app)
    {
        var group = app.MapGroup("/api/admin")
            .WithTags("Admin")
            .WithOpenApi();

        group.MapPost("/keys", CreateApiKey)
            .WithName("CreateApiKey")
            .WithSummary("Create a new API key")
            .Produces<CreateKeyResponse>(201)
            .Produces(401);

        group.MapGet("/keys", ListApiKeys)
            .WithName("ListApiKeys")
            .WithSummary("List all API keys")
            .Produces<IEnumerable<KeyResponse>>();

        group.MapDelete("/keys/{id:guid}", RevokeApiKey)
            .WithName("RevokeApiKey")
            .WithSummary("Revoke an API key")
            .Produces(204)
            .Produces(404);

        group.MapGet("/keys/{id:guid}/usage", GetApiKeyUsage)
            .WithName("GetApiKeyUsage")
            .WithSummary("Get API key usage statistics")
            .Produces<KeyUsageStats>()
            .Produces(404);
    }

    private static async Task<IResult> CreateApiKey(
        CreateKeyRequest request,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var (key, plainTextKey) = await apiKeyService.CreateKeyAsync(request.Name, request.IsAdmin, request.RateLimit);
        
        return Results.Created($"/api/admin/keys/{key.Id}", new CreateKeyResponse(
            key.Id,
            key.Name,
            key.KeyPrefix,
            plainTextKey,
            key.IsAdmin,
            key.RateLimit,
            key.CreatedAt
        ));
    }

    private static async Task<IResult> ListApiKeys(
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var keys = await apiKeyService.GetAllKeysAsync();
        return Results.Ok(keys.Select(k => new KeyResponse(
            k.Id,
            k.Name,
            k.KeyPrefix,
            k.IsAdmin,
            k.RateLimit,
            k.CreatedAt,
            k.LastUsedAt
        )));
    }

    private static async Task<IResult> RevokeApiKey(
        Guid id,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var success = await apiKeyService.RevokeKeyAsync(id);
        return success ? Results.NoContent() : Results.NotFound();
    }

    private static async Task<IResult> GetApiKeyUsage(
        Guid id,
        IApiKeyService apiKeyService,
        HttpContext context)
    {
        if (!ValidateAdminKey(context))
            return Results.Json(new { error = "unauthorized", message = "Admin key required" }, statusCode: 401);

        var usage = await apiKeyService.GetKeyUsageAsync(id);
        return usage is null ? Results.NotFound() : Results.Ok(usage);
    }

    private static bool ValidateAdminKey(HttpContext context)
    {
        var adminKey = Environment.GetEnvironmentVariable("ADMIN_API_KEY");
        if (string.IsNullOrEmpty(adminKey)) return false;
        
        var providedKey = context.Request.Headers["X-Admin-Key"].FirstOrDefault();
        return adminKey == providedKey;
    }
}

// DTOs for admin endpoints
public record CreateKeyRequest(string Name, bool IsAdmin = false, int? RateLimit = null);

public record CreateKeyResponse(
    Guid Id,
    string Name,
    string KeyPrefix,
    string PlainTextKey,
    bool IsAdmin,
    int RateLimit,
    DateTime CreatedAt
);

public record KeyResponse(
    Guid Id,
    string Name,
    string KeyPrefix,
    bool IsAdmin,
    int RateLimit,
    DateTime CreatedAt,
    DateTime? LastUsedAt
);
