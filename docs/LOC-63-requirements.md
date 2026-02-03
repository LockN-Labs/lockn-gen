# LOC-63: WebSocket Progress Updates

## Overview
Add real-time progress updates for image generation via WebSocket connections. Users should see live updates as their generation progresses through ComfyUI's workflow nodes.

## Requirements

### Functional Requirements

1. **WebSocket Endpoint**
   - `GET /api/ws/progress` — WebSocket connection for progress updates
   - Support connection with optional generation ID filter
   - Handle multiple concurrent connections

2. **Progress Messages**
   - `generation.started` — Generation queued and started
   - `generation.progress` — Node execution progress (0-100%)
   - `generation.node` — Current node being executed
   - `generation.preview` — Preview image available (base64 or URL)
   - `generation.completed` — Generation finished successfully
   - `generation.failed` — Generation failed with error
   - `generation.cancelled` — Generation was cancelled

3. **Message Format**
   ```json
   {
     "type": "generation.progress",
     "generationId": "uuid",
     "data": {
       "progress": 45,
       "currentNode": "KSampler",
       "step": 9,
       "totalSteps": 20,
       "previewUrl": "/api/generations/{id}/preview"
     },
     "timestamp": "2026-02-03T15:07:00Z"
   }
   ```

4. **ComfyUI Integration**
   - Poll or WebSocket connect to ComfyUI's `/ws` endpoint
   - Parse ComfyUI progress events
   - Map to LockN Gen progress format
   - Handle ComfyUI reconnection on disconnect

5. **Connection Management**
   - Heartbeat/ping-pong to detect stale connections
   - Automatic cleanup of disconnected clients
   - Connection limit per client (prevent abuse)

### Non-Functional Requirements

1. **Performance**
   - < 100ms latency from ComfyUI event to client
   - Support 100+ concurrent WebSocket connections
   - Efficient broadcast to multiple subscribers

2. **Reliability**
   - Graceful handling of ComfyUI disconnects
   - Message buffering for brief disconnects
   - Clear error messages on failures

3. **Security**
   - Optional authentication header on upgrade
   - Rate limiting on connection attempts

## Technical Notes

- Use `System.Net.WebSockets` for server-side
- ComfyUI WebSocket is at `ws://localhost:8188/ws`
- Preview images via ComfyUI's `/view` endpoint

## Acceptance Criteria

- [ ] WebSocket endpoint accepts connections
- [ ] Progress updates broadcast within 100ms of ComfyUI event
- [ ] Frontend gallery shows real-time progress bars
- [ ] Disconnected clients cleaned up automatically
- [ ] ComfyUI reconnection works after brief outage

## Dependencies

- LOC-58 (ComfyUI Backend Integration) ✅
- LOC-60 (Frontend Gallery UI) ✅
