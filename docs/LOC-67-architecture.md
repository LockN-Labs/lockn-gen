# LOC-67 Admin Dashboard & Metrics Architecture

## 1. Overview
Provides real-time operational visibility for LockN Gen API with:
- Generation statistics (success/failure rates)
- API key usage tracking
- ComfyUI queue depth visualization
- Node status monitoring

## 2. Components
- Embedded HTML dashboard served from /admin endpoint
- Metrics API endpoints (GET /admin/stats, GET /admin/metrics)
- Real-time Redis counters for queue depth
- PostgreSQL hourly aggregation jobs for historical data

## 3. Data Model
```text
Metrics (PostgreSQL table)
- MetricType (enum: Generation, APIKey, QueueDepth, NodeStatus)
- Timestamp (UTC)
- Value (JSONB)
- ApiKeyId (nullable)
- NodeId (nullable)

Redis Keys:
- comfyui:queue:depth (integer)
- nodes:<id>:status (string)
```

## 4. API Endpoints
| Endpoint | Method | Description | Auth |
|---------|--------|-------------|------|
| /admin/stats | GET | Real-time metrics | Admin API key |
| /admin/metrics | GET | Historical data | Admin API key |
| /admin/queue | GET | Current queue depth | Admin API key |
| /admin/nodes | GET | ComfyUI node statuses | Admin API key |

## 5. UI Approach
- Embedded HTML page using Chart.js for visualizations
- Auto-refreshing iframe for real-time updates
- Served from ASP.NET Core MVC controller

## 6. Dependencies
- NuGet: Microsoft.AspNetCore.Mvc.TagHelpers (for embedded views)
- Chart.js 4.4.0 via CDN

## 7. Security
- Requires API key with isAdmin = true
- Rate limited to 100RPS per admin key
- All endpoints protected by JWT bearer authentication

MVP Constraints:
- No user authentication UI
- Metrics retention: 90 days historical data
- 1-minute aggregation intervals for performance
