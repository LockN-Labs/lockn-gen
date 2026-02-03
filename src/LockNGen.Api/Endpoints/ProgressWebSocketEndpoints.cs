using LockNGen.Api.WebSockets;

namespace LockNGen.Api.Endpoints;

/// <summary>
/// WebSocket endpoint for real-time progress updates.
/// </summary>
public static class ProgressWebSocketEndpoints
{
    public static WebApplication MapProgressWebSocketEndpoints(this WebApplication app)
    {
        app.Map("/api/ws/progress", async (HttpContext context, ProgressWebSocketHandler handler) =>
        {
            // Parse optional generationId from query string
            Guid? generationId = null;
            if (context.Request.Query.TryGetValue("generationId", out var genIdStr) &&
                Guid.TryParse(genIdStr, out var parsed))
            {
                generationId = parsed;
            }

            await handler.HandleAsync(context, generationId);
        });

        return app;
    }
}
