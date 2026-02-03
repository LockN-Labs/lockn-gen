# LOC-63: WebSocket Progress Updates — Architecture

## Component Design

### 1. WebSocket Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                        LockN Gen API                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌────────────────────┐                 │
│  │ WebSocket        │    │ Progress           │                 │
│  │ Handler          │◄───│ Broadcaster        │                 │
│  │ /api/ws/progress │    │ (IProgressBroadcast│                 │
│  └────────┬─────────┘    └─────────┬──────────┘                 │
│           │                        │                             │
│           │              ┌─────────▼──────────┐                  │
│           │              │ ComfyUI Progress   │                  │
│           │              │ Monitor            │                  │
│           │              │ (Background Worker)│                  │
│           │              └─────────┬──────────┘                  │
└───────────┼────────────────────────┼────────────────────────────┘
            │                        │
            ▼                        ▼
      ┌──────────┐           ┌───────────────┐
      │ Clients  │           │ ComfyUI WS    │
      │ (Browser)│           │ localhost:8188│
      └──────────┘           └───────────────┘
```

### 2. New Components

#### IProgressBroadcaster
```csharp
public interface IProgressBroadcaster
{
    Task BroadcastAsync(ProgressMessage message);
    Task BroadcastToGenerationAsync(Guid generationId, ProgressMessage message);
    void RegisterClient(WebSocket socket, Guid? filterGenerationId = null);
    void UnregisterClient(WebSocket socket);
}
```

#### ProgressMessage
```csharp
public record ProgressMessage(
    string Type,            // "generation.progress", "generation.completed", etc.
    Guid GenerationId,
    ProgressData? Data,
    DateTime Timestamp
);

public record ProgressData(
    int Progress,           // 0-100
    string? CurrentNode,    // "KSampler", "VAEDecode", etc.
    int? Step,
    int? TotalSteps,
    string? PreviewUrl,
    string? Error
);
```

#### ComfyUiProgressMonitor (Background Service)
```csharp
public class ComfyUiProgressMonitor : BackgroundService
{
    // Connects to ComfyUI WebSocket
    // Parses progress events
    // Maps to ProgressMessage
    // Calls IProgressBroadcaster
}
```

### 3. File Changes

| File | Change |
|------|--------|
| `src/LockNGen.Domain/DTOs/ProgressMessage.cs` | New — progress message types |
| `src/LockNGen.Domain/Services/IProgressBroadcaster.cs` | New — broadcast interface |
| `src/LockNGen.Infrastructure/WebSockets/ProgressBroadcaster.cs` | New — thread-safe broadcaster |
| `src/LockNGen.Infrastructure/ComfyUi/ComfyUiProgressMonitor.cs` | New — background monitor |
| `src/LockNGen.Api/WebSockets/ProgressWebSocketHandler.cs` | New — endpoint handler |
| `src/LockNGen.Api/Endpoints/ProgressWebSocketEndpoints.cs` | New — route mapping |
| `src/LockNGen.Api/Program.cs` | Modified — register services |
| `src/LockNGen.Api/wwwroot/js/gallery.js` | Modified — real-time progress UI |

### 4. ComfyUI WebSocket Protocol

ComfyUI sends JSON messages:
```json
{"type": "status", "data": {"status": {"exec_info": {"queue_remaining": 1}}}}
{"type": "execution_start", "data": {"prompt_id": "..."}}
{"type": "executing", "data": {"node": "3", "prompt_id": "..."}}
{"type": "progress", "data": {"value": 5, "max": 20, "prompt_id": "..."}}
{"type": "executed", "data": {"node": "9", "output": {...}, "prompt_id": "..."}}
{"type": "execution_cached", "data": {"nodes": ["1", "2"], "prompt_id": "..."}}
```

### 5. Thread Safety

- `ConcurrentDictionary<WebSocket, ClientInfo>` for client tracking
- `SemaphoreSlim` for broadcast serialization
- Async/await throughout

### 6. Connection Lifecycle

1. Client connects to `/api/ws/progress?generationId={optional}`
2. Server validates (optional auth header)
3. Client registered in broadcaster
4. Progress events streamed as JSON
5. Ping/pong every 30s to detect dead connections
6. Client disconnect → cleanup

## Testing Approach

1. Unit tests for message serialization
2. Integration test with mock ComfyUI WebSocket
3. Manual test with real ComfyUI

## Estimated Lines

~500-600 lines total across all files.
