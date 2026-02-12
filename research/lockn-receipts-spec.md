# LocknReceipts — System Specification

> **Version:** 0.1.0-draft
> **Date:** 2026-02-02
> **Author:** LockN Labs
> **Status:** Design / Pre-implementation

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Postgres Schema](#3-postgres-schema)
4. [Receipt Envelope JSON Schema](#4-receipt-envelope-json-schema)
5. [LocknReceipts API Spec](#5-locknreceipts-api-spec)
6. [OpenClaw Skill Design](#6-openclaw-skill-design)
7. [OTel Alignment](#7-otel-alignment)
8. [Tech Stack & Deployment](#8-tech-stack--deployment)

---

## 1. Overview

LocknReceipts is a receipt-logging system for AI agent tool usage. Every tool call an agent makes (web search, browser action, fetch, etc.) produces a structured **receipt** — an immutable record of what was called, what was returned, how long it took, what it cost, and how useful it was.

**Why:**
- Cost visibility — know exactly what every agent session costs in API calls, tokens, and external tool usage
- Audit trail — immutable log of every tool invocation for compliance and debugging
- Quality metrics — track which searches return useful results, which tools fail, latency trends
- OTel-compatible — receipts map to OpenTelemetry GenAI semantic conventions for observability pipelines

**Data flow:**
```
Agent calls web_search
  → OpenClaw skill wrapper intercepts
  → Executes actual tool call, captures timing
  → Hashes request + response payloads
  → Uploads large payloads to MinIO (content-addressable, dedup by sha256)
  → Constructs receipt envelopes (tool.call + tool.eval)
  → POST /websearch/record → Postgres
  → Returns original tool response to agent (unchanged)
```

---

## 2. Architecture

```
┌─────────────────────────────────────────────────┐
│  OpenClaw Agent (Clawdbot)                      │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │  lockn-receipts skill (wrapper)           │  │
│  │  - intercepts tool calls                  │  │
│  │  - times execution                        │  │
│  │  - hashes + uploads payloads to MinIO     │  │
│  │  - builds receipt envelopes               │  │
│  │  - POSTs to LocknReceipts API             │  │
│  └──────────┬──────────────┬─────────────────┘  │
│             │              │                     │
└─────────────┼──────────────┼─────────────────────┘
              │              │
              ▼              ▼
     ┌────────────┐  ┌──────────────┐
     │   MinIO     │  │ LocknReceipts│
     │  (blobs)    │  │   API        │
     │  port 9000  │  │  port 8420   │
     └────────────┘  └──────┬───────┘
                            │
                            ▼
                     ┌─────────────┐
                     │  Postgres   │
                     │  port 5432  │
                     └─────────────┘
```

All components run on the same machine (Threadripper Pro, 256GB RAM). No external network calls for receipt storage.

---

## 3. Postgres Schema

### 3.1 Full DDL

```sql
-- ============================================================
-- LocknReceipts Schema
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ----------------------------------------------------------
-- payload_blobs: content-addressable blob references
-- ----------------------------------------------------------
CREATE TABLE payload_blobs (
    sha256        TEXT        PRIMARY KEY,  -- hex-encoded sha256
    minio_uri     TEXT        NOT NULL,     -- s3://lockn-receipts/<sha256>
    bytes         BIGINT      NOT NULL,
    content_type  TEXT        NOT NULL DEFAULT 'application/json',
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE payload_blobs IS 'Content-addressable refs to MinIO blobs. Dedup by sha256.';

-- ----------------------------------------------------------
-- receipts: envelope metadata (partitioned by month)
-- ----------------------------------------------------------
CREATE TABLE receipts (
    id            UUID        NOT NULL DEFAULT gen_random_uuid(),
    type          TEXT        NOT NULL,  -- 'tool.call', 'tool.eval'
    tool_name     TEXT        NOT NULL,  -- 'web_search', 'web_fetch', 'browser', ...
    agent_id      TEXT        NOT NULL,  -- e.g. 'agent:main'
    session_id    TEXT,                  -- OpenClaw session id
    trace_id      TEXT,                  -- OTel trace id (hex, 32 chars)
    span_id       TEXT,                  -- OTel span id (hex, 16 chars)
    parent_span_id TEXT,
    model         TEXT,                  -- e.g. 'anthropic/claude-opus-4-5'
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- cost tracking (nullable — not all tools have token costs)
    cost_usd      NUMERIC(12,8),

    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create initial partitions (auto-create monthly via pg_partman or cron)
CREATE TABLE receipts_2026_01 PARTITION OF receipts
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE receipts_2026_02 PARTITION OF receipts
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE receipts_2026_03 PARTITION OF receipts
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
-- ... generate monthly via cron or pg_partman

CREATE INDEX idx_receipts_agent_id ON receipts (agent_id, created_at DESC);
CREATE INDEX idx_receipts_session_id ON receipts (session_id, created_at DESC);
CREATE INDEX idx_receipts_type ON receipts (type, created_at DESC);
CREATE INDEX idx_receipts_tool_name ON receipts (tool_name, created_at DESC);
CREATE INDEX idx_receipts_trace_id ON receipts (trace_id) WHERE trace_id IS NOT NULL;

-- ----------------------------------------------------------
-- receipt_payload_refs: links receipts to payload blobs
-- ----------------------------------------------------------
CREATE TABLE receipt_payload_refs (
    receipt_id    UUID        NOT NULL,
    receipt_ts    TIMESTAMPTZ NOT NULL,  -- needed for partition routing
    role          TEXT        NOT NULL,  -- 'request', 'response', 'eval'
    payload_sha256 TEXT       NOT NULL REFERENCES payload_blobs(sha256),

    PRIMARY KEY (receipt_id, role),
    FOREIGN KEY (receipt_id, receipt_ts) REFERENCES receipts(id, created_at)
);

CREATE INDEX idx_rpr_payload ON receipt_payload_refs (payload_sha256);

-- ----------------------------------------------------------
-- tool_calls: generic tool call metadata
-- ----------------------------------------------------------
CREATE TABLE tool_calls (
    receipt_id        UUID        PRIMARY KEY,
    receipt_ts        TIMESTAMPTZ NOT NULL,
    tool_name         TEXT        NOT NULL,
    tool_call_id      TEXT,                  -- OTel gen_ai.tool.call.id
    status            TEXT        NOT NULL DEFAULT 'success',  -- success | error | timeout
    duration_ms       INTEGER     NOT NULL,
    error_type        TEXT,                  -- error class if status != success
    error_message     TEXT,

    -- token usage (if the tool call itself consumes tokens, e.g. via an LLM sub-call)
    token_usage_input   INTEGER,
    token_usage_output  INTEGER,

    FOREIGN KEY (receipt_id, receipt_ts) REFERENCES receipts(id, created_at)
);

CREATE INDEX idx_tool_calls_tool ON tool_calls (tool_name, receipt_ts DESC);
CREATE INDEX idx_tool_calls_status ON tool_calls (status) WHERE status != 'success';

-- ----------------------------------------------------------
-- web_search_calls: web_search-specific fields
-- ----------------------------------------------------------
CREATE TABLE web_search_calls (
    receipt_id      UUID        PRIMARY KEY REFERENCES tool_calls(receipt_id),
    query           TEXT        NOT NULL,
    locale          TEXT,               -- e.g. 'en-US'
    country         TEXT,               -- 2-letter code
    search_lang     TEXT,
    freshness       TEXT,               -- 'pd', 'pw', 'pm', 'py', or date range
    result_count    INTEGER,            -- number of results returned
    provider        TEXT        NOT NULL DEFAULT 'brave'  -- brave, google, etc.
);

CREATE INDEX idx_wsc_query ON web_search_calls USING gin (to_tsvector('english', query));

-- ----------------------------------------------------------
-- web_search_evals: quality/evaluation metrics
-- ----------------------------------------------------------
CREATE TABLE web_search_evals (
    receipt_id        UUID        PRIMARY KEY,
    receipt_ts        TIMESTAMPTZ NOT NULL,
    call_receipt_id   UUID        NOT NULL,  -- links eval to the tool.call receipt
    relevance_score   REAL,                  -- 0.0–1.0 agent-assessed relevance
    result_quality    TEXT,                  -- 'excellent', 'good', 'fair', 'poor', 'irrelevant'
    results_used      INTEGER,               -- how many results the agent actually used
    latency_ms        INTEGER,               -- end-to-end including network
    notes             TEXT,                  -- free-form eval notes

    FOREIGN KEY (receipt_id, receipt_ts) REFERENCES receipts(id, created_at)
);

-- ----------------------------------------------------------
-- Partition maintenance helper
-- ----------------------------------------------------------
-- Recommend: pg_partman extension or a monthly cron job:
-- SELECT create_partition('receipts', date_trunc('month', now() + interval '1 month'));
```

### 3.2 Partitioning Strategy

- **`receipts`** is range-partitioned by `created_at` (monthly).
- Child tables: `receipts_YYYY_MM`. Create 3 months ahead via cron.
- All other tables reference receipts but are NOT partitioned (they're smaller and queried by receipt_id).
- If volume exceeds ~100M rows/month, partition `tool_calls` similarly.

### 3.3 Retention

- Hot data: last 90 days (fast queries)
- Warm: 90d–1y (kept but could be on slower storage)
- Cold: >1y — detach old partitions, archive to MinIO as parquet, drop

---

## 4. Receipt Envelope JSON Schema

### 4.1 `tool.call` Receipt

```jsonc
{
  // --- envelope ---
  "receipt_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "type": "tool.call",
  "version": "0.1.0",
  "timestamp": "2026-02-02T18:22:42.123Z",

  // --- identity ---
  "agent_id": "agent:main",
  "session_id": "agent:main:main",
  "model": "anthropic/claude-opus-4-5",

  // --- OTel trace context ---
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "parent_span_id": "b3e1d5a2f0c8e9d4",

  // --- tool call ---
  "tool": {
    "name": "web_search",
    "call_id": "call_abc123",
    "status": "success",         // success | error | timeout
    "duration_ms": 842,
    "error": null                // { "type": "...", "message": "..." } if failed
  },

  // --- token usage (if applicable) ---
  "usage": {
    "input_tokens": null,
    "output_tokens": null
  },

  // --- cost ---
  "cost_usd": null,

  // --- payload refs (sha256 → MinIO) ---
  "payloads": {
    "request": {
      "sha256": "a1b2c3d4e5f6...",
      "uri": "s3://lockn-receipts/a1b2c3d4e5f6...",
      "bytes": 256,
      "content_type": "application/json"
    },
    "response": {
      "sha256": "f6e5d4c3b2a1...",
      "uri": "s3://lockn-receipts/f6e5d4c3b2a1...",
      "bytes": 14832,
      "content_type": "application/json"
    }
  },

  // --- tool-specific metadata (inline, not in blob) ---
  "web_search": {
    "query": "OpenTelemetry GenAI semantic conventions",
    "locale": "en-US",
    "country": "US",
    "freshness": null,
    "result_count": 5,
    "provider": "brave"
  }
}
```

### 4.2 `tool.eval` Receipt

```jsonc
{
  "receipt_id": "e82f1a3b-7cc4-4a12-9d67-1f03c4d5e580",
  "type": "tool.eval",
  "version": "0.1.0",
  "timestamp": "2026-02-02T18:22:43.456Z",

  "agent_id": "agent:main",
  "session_id": "agent:main:main",
  "model": "anthropic/claude-opus-4-5",

  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "11a178bb1cb013c8",
  "parent_span_id": "00f067aa0ba902b7",  // parent = the tool.call span

  // --- what this evaluates ---
  "evaluates": {
    "receipt_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "tool_name": "web_search"
  },

  // --- evaluation metrics ---
  "eval": {
    "relevance_score": 0.85,
    "result_quality": "good",
    "results_used": 3,
    "latency_ms": 842,
    "notes": "Top 3 results were directly relevant. Result 4-5 were tangential."
  },

  // --- payload refs ---
  "payloads": {
    "eval": {
      "sha256": "c3d4e5f6a1b2...",
      "uri": "s3://lockn-receipts/c3d4e5f6a1b2...",
      "bytes": 512,
      "content_type": "application/json"
    }
  }
}
```

### 4.3 Design Notes

- **Inline vs blob:** Small structured metadata (query, result_count, scores) goes inline. Raw request/response bodies go to MinIO blobs referenced by sha256.
- **Content-addressable:** If two searches return identical results, they share the same blob. No duplication.
- **Immutable:** Receipts are append-only. Never updated or deleted (except retention policy).

---

## 5. LocknReceipts API Spec

**Base URL:** `http://localhost:8420/api/v1`
**Auth:** Bearer token (shared secret, env var `LOCKN_RECEIPTS_TOKEN`)

### 5.1 `POST /websearch/record`

Record a web_search tool call + optional eval in one request.

**Request:**
```jsonc
{
  "call": { /* tool.call receipt envelope (§4.1) */ },
  "eval": { /* tool.eval receipt envelope (§4.2), optional */ }
}
```

**Response:** `201 Created`
```jsonc
{
  "call_receipt_id": "f47ac10b-...",
  "eval_receipt_id": "e82f1a3b-...",  // null if no eval
  "payloads_stored": 3,
  "payloads_deduped": 0
}
```

**Behavior:**
1. Validate envelope schemas
2. Upsert payload_blobs (skip if sha256 already exists — dedup)
3. Insert into `receipts`, `receipt_payload_refs`, `tool_calls`, `web_search_calls`
4. If eval present: insert into `receipts`, `receipt_payload_refs`, `web_search_evals`
5. Return created IDs

### 5.2 `POST /tool/record` (future — generic)

Same pattern but without tool-specific tables. Just `receipts` + `tool_calls` + `receipt_payload_refs`.

```jsonc
{
  "call": { /* tool.call receipt */ },
  "eval": { /* tool.eval receipt, optional */ }
}
```

### 5.3 `GET /receipts`

Query receipts with filters.

**Query params:**
| Param | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Filter by agent |
| `session_id` | string | Filter by session |
| `tool_name` | string | Filter by tool |
| `type` | string | `tool.call` or `tool.eval` |
| `status` | string | `success`, `error`, `timeout` |
| `from` | ISO datetime | Start of time range |
| `to` | ISO datetime | End of time range |
| `trace_id` | string | Filter by OTel trace |
| `limit` | integer | Max results (default 50, max 500) |
| `offset` | integer | Pagination offset |

**Response:** `200 OK`
```jsonc
{
  "receipts": [ /* receipt envelopes */ ],
  "total": 1234,
  "limit": 50,
  "offset": 0
}
```

### 5.4 `GET /receipts/:id`

Single receipt with full payload refs (not payload bodies — those come from MinIO directly).

**Response:** `200 OK`
```jsonc
{
  "receipt": { /* full envelope */ },
  "payload_refs": [
    { "role": "request", "sha256": "...", "uri": "...", "bytes": 256 },
    { "role": "response", "sha256": "...", "uri": "...", "bytes": 14832 }
  ]
}
```

### 5.5 `GET /stats`

Aggregated metrics.

**Query params:** `agent_id`, `session_id`, `tool_name`, `model`, `from`, `to`, `group_by` (comma-separated: `tool_name`, `agent_id`, `model`, `hour`, `day`)

**Response:** `200 OK`
```jsonc
{
  "period": { "from": "...", "to": "..." },
  "totals": {
    "calls": 4521,
    "errors": 23,
    "error_rate": 0.0051,
    "total_duration_ms": 3842100,
    "avg_duration_ms": 850,
    "p50_duration_ms": 780,
    "p95_duration_ms": 1450,
    "p99_duration_ms": 2100,
    "total_tokens_input": null,
    "total_tokens_output": null,
    "total_cost_usd": null,
    "avg_relevance_score": 0.72,
    "payloads_bytes": 182934521
  },
  "groups": [
    {
      "key": { "tool_name": "web_search" },
      "calls": 3200,
      "errors": 15,
      "avg_duration_ms": 820,
      "avg_relevance_score": 0.74
    }
  ]
}
```

### 5.6 Error Responses

All errors follow:
```jsonc
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "receipt.type must be 'tool.call' or 'tool.eval'",
    "details": {}
  }
}
```

Standard HTTP codes: 400 (validation), 401 (auth), 404, 500.

---

## 6. OpenClaw Skill Design

### 6.1 Skill Structure

```
skills/lockn-receipts/
├── SKILL.md            # Skill manifest
├── wrapper.js          # Tool call wrapper logic
├── minio.js            # MinIO upload client
├── receipts.js         # Receipt envelope construction
├── config.js           # Config from env vars
└── package.json
```

### 6.2 SKILL.md

```markdown
---
name: lockn-receipts
version: 0.1.0
description: Receipt logging for tool calls — tracks usage, cost, and quality
author: LockN Labs
capabilities: []
---

# lockn-receipts

Wraps tool calls to produce immutable receipts. Captures request, response,
timing, and quality metrics. Stores payloads in MinIO, metadata in Postgres
via the LocknReceipts API.

## Configuration (env vars)

| Variable | Required | Description |
|----------|----------|-------------|
| `LOCKN_RECEIPTS_API` | yes | API base URL (e.g. `http://localhost:8420/api/v1`) |
| `LOCKN_RECEIPTS_TOKEN` | yes | Bearer token for API auth |
| `LOCKN_MINIO_ENDPOINT` | yes | MinIO endpoint (e.g. `localhost:9000`) |
| `LOCKN_MINIO_ACCESS_KEY` | yes | MinIO access key |
| `LOCKN_MINIO_SECRET_KEY` | yes | MinIO secret key |
| `LOCKN_MINIO_BUCKET` | no | Bucket name (default: `lockn-receipts`) |
| `LOCKN_RECEIPTS_ENABLED` | no | `true`/`false` (default: `true`) |

## Wrapped Tools

- `web_search` (v0.1)
- `web_fetch` (planned)
- `browser` (planned)

## Behavior

- Wrapping is transparent — tool output is unchanged
- Receipt failures are logged but never block tool execution
- Large payloads (>1KB) go to MinIO; small ones inline
- Content-addressable dedup via sha256
```

### 6.3 Interception Strategy

OpenClaw skills can register **tool middleware** — functions that wrap tool execution. The wrapper:

```javascript
// wrapper.js — pseudocode
export function wrapToolCall(toolName, originalFn) {
  return async (params, context) => {
    if (!config.enabled) return originalFn(params, context);

    const startTime = Date.now();
    let result, status = 'success', error = null;

    try {
      result = await originalFn(params, context);
    } catch (err) {
      status = err.name === 'TimeoutError' ? 'timeout' : 'error';
      error = { type: err.name, message: err.message };
      throw err;  // re-throw — don't swallow
    } finally {
      // Fire-and-forget — never block the agent
      recordReceipt(toolName, params, result, {
        status, error,
        duration_ms: Date.now() - startTime,
        agent_id: context.agentId,
        session_id: context.sessionId,
        model: context.model,
      }).catch(err => console.error('[lockn-receipts] record failed:', err));
    }

    return result;
  };
}
```

### 6.4 MinIO Upload Logic

```javascript
// minio.js — pseudocode
import { createHash } from 'crypto';
import { Client as MinioClient } from 'minio';

const client = new MinioClient({ /* from config */ });
const BUCKET = config.bucket || 'lockn-receipts';
const INLINE_THRESHOLD = 1024; // 1KB

export async function storePayload(data) {
  const json = JSON.stringify(data);
  const sha256 = createHash('sha256').update(json).digest('hex');
  const bytes = Buffer.byteLength(json);

  // Check if already stored (content-addressable dedup)
  try {
    await client.statObject(BUCKET, sha256);
    // Already exists — return ref only
  } catch {
    await client.putObject(BUCKET, sha256, json, {
      'Content-Type': 'application/json',
    });
  }

  return {
    sha256,
    uri: `s3://${BUCKET}/${sha256}`,
    bytes,
    content_type: 'application/json',
  };
}
```

### 6.5 Receipt Construction

```javascript
// receipts.js
import { randomUUID } from 'crypto';
import { storePayload } from './minio.js';

export async function buildCallReceipt(toolName, params, result, meta) {
  const [reqRef, resRef] = await Promise.all([
    storePayload(params),
    result ? storePayload(result) : null,
  ]);

  return {
    receipt_id: randomUUID(),
    type: 'tool.call',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
    agent_id: meta.agent_id,
    session_id: meta.session_id,
    model: meta.model,
    trace_id: meta.trace_id || null,
    span_id: meta.span_id || randomHex(16),
    parent_span_id: meta.parent_span_id || null,
    tool: {
      name: toolName,
      call_id: meta.call_id || randomUUID(),
      status: meta.status,
      duration_ms: meta.duration_ms,
      error: meta.error,
    },
    usage: { input_tokens: null, output_tokens: null },
    cost_usd: null,
    payloads: {
      request: reqRef,
      response: resRef,
    },
    // Tool-specific metadata extractor
    ...(toolName === 'web_search' ? {
      web_search: extractWebSearchMeta(params, result),
    } : {}),
  };
}

function extractWebSearchMeta(params, result) {
  return {
    query: params.query,
    locale: params.ui_lang || null,
    country: params.country || 'US',
    freshness: params.freshness || null,
    result_count: result?.web?.results?.length || 0,
    provider: 'brave',
  };
}
```

### 6.6 Error Handling Philosophy

**Rule: Receipt logging must NEVER break the tool call.**

- All receipt operations are fire-and-forget (`catch` + log)
- Timeouts on MinIO uploads: 5s max
- Timeouts on API POST: 5s max
- If receipts API is down, log locally to `~/.openclaw/lockn-receipts/pending/` as JSONL for later replay
- Circuit breaker: after 5 consecutive failures, disable for 60s, then retry

---

## 7. OTel Alignment

### 7.1 Semantic Convention Mapping

| Receipt Field | OTel GenAI Convention | Notes |
|---|---|---|
| `model` | `gen_ai.request.model` | e.g. `anthropic/claude-opus-4-5` |
| `agent_id` | `gen_ai.system` | The agent system (OpenClaw) |
| `tool.name` | `gen_ai.tool.name` | `web_search`, `browser`, etc. |
| `tool.call_id` | `gen_ai.tool.call.id` | Unique call identifier |
| `usage.input_tokens` | `gen_ai.usage.input_tokens` | If applicable |
| `usage.output_tokens` | `gen_ai.usage.output_tokens` | If applicable |
| `trace_id` | W3C `traceparent` trace-id | 32 hex chars |
| `span_id` | W3C `traceparent` span-id | 16 hex chars |
| `parent_span_id` | W3C parent span | Links call → eval |
| `tool.status` | `otel.status_code` | `OK` / `ERROR` |
| `tool.duration_ms` | span duration | `end_time - start_time` |
| `tool.error.type` | `error.type` | Exception class |
| `tool.error.message` | `exception.message` | Error detail |

### 7.2 Span Structure

```
Trace: 4bf92f3577b34da6a3ce929d0e0e4736
│
├── Span: agent_turn (parent)
│   ├── Span: tool.call/web_search  ← tool.call receipt
│   │   └── Span: tool.eval/web_search  ← tool.eval receipt
│   ├── Span: tool.call/web_fetch
│   │   └── Span: tool.eval/web_fetch
```

### 7.3 Export Path

Receipts can be exported as OTel spans via:

1. **Direct OTLP export** — API has a `/export/otlp` endpoint that converts receipts to OTLP protobuf and ships to a collector
2. **Batch job** — Periodic cron reads recent receipts and pushes to OTLP endpoint (Grafana Tempo, Jaeger, etc.)
3. **Postgres → OTEL collector** — Use the OTel Postgres receiver or a custom exporter

Recommended: Option 2 (batch), since receipts are already in Postgres with all needed fields.

### 7.4 Additional OTel Attributes

```
gen_ai.system = "openclaw"
gen_ai.operation.name = "tool_call"
lockn.receipt.id = "<receipt_id>"
lockn.receipt.version = "0.1.0"
lockn.payload.request.sha256 = "<hash>"
lockn.payload.response.sha256 = "<hash>"
lockn.web_search.query = "<query>"
lockn.web_search.provider = "brave"
lockn.web_search.result_count = 5
lockn.eval.relevance_score = 0.85
lockn.eval.result_quality = "good"
```

---

## 8. Tech Stack & Deployment

### 8.1 Recommendations

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **API** | **FastAPI (Python)** | Rapid development, async, Pydantic validation, auto OpenAPI docs. Team familiarity. |
| **ORM/DB** | **SQLAlchemy 2.0 + asyncpg** | Async Postgres with good migration support (Alembic). |
| **MinIO client** | **minio-py** or **boto3** | minio-py is lighter; boto3 if you want S3 compat flexibility. |
| **Postgres** | **PostgreSQL 16** | Partitioning, JSONB, mature. Already likely running. |
| **MinIO** | **MinIO (Docker)** | Single-node, S3-compatible. Trivial to run. |
| **Deployment** | **Docker Compose** | All on same machine. Simple. |

### 8.2 Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: lockn_receipts
      POSTGRES_USER: lockn
      POSTGRES_PASSWORD: ${LOCKN_PG_PASSWORD}
    ports:
      - "127.0.0.1:5433:5432"  # 5433 to avoid conflicts
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./schema.sql:/docker-entrypoint-initdb.d/001-schema.sql
    restart: unless-stopped

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${LOCKN_MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${LOCKN_MINIO_SECRET_KEY}
    ports:
      - "127.0.0.1:9000:9000"
      - "127.0.0.1:9001:9001"
    volumes:
      - miniodata:/data
    restart: unless-stopped

  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql+asyncpg://lockn:${LOCKN_PG_PASSWORD}@postgres:5432/lockn_receipts
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: ${LOCKN_MINIO_ACCESS_KEY}
      MINIO_SECRET_KEY: ${LOCKN_MINIO_SECRET_KEY}
      MINIO_BUCKET: lockn-receipts
      LOCKN_RECEIPTS_TOKEN: ${LOCKN_RECEIPTS_TOKEN}
    ports:
      - "127.0.0.1:8420:8420"
    depends_on:
      - postgres
      - minio
    restart: unless-stopped

volumes:
  pgdata:
  miniodata:
```

### 8.3 Resource Estimates

Running on the Threadripper Pro (256GB RAM):

| Component | RAM | CPU | Disk |
|-----------|-----|-----|------|
| Postgres | ~256MB idle, 1-2GB under load | Minimal | Grows with receipts (~1KB/receipt metadata) |
| MinIO | ~128MB | Minimal | Grows with payloads (~10-50KB/search response) |
| FastAPI | ~128MB | Minimal | None |
| **Total** | **~500MB–2GB** | **<1 core** | **~1GB/month at moderate usage** |

This is negligible on a 256GB machine. Run it all locally.

### 8.4 Bootstrap Bucket

MinIO needs the bucket created on first run:

```bash
# After compose up:
mc alias set lockn http://localhost:9000 $LOCKN_MINIO_ACCESS_KEY $LOCKN_MINIO_SECRET_KEY
mc mb lockn/lockn-receipts
mc policy set none lockn/lockn-receipts  # private
```

Or add an init container to docker-compose.

### 8.5 Migration Strategy

Use **Alembic** for Postgres schema migrations:
```
api/
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py
│   └── env.py
├── alembic.ini
```

### 8.6 Implementation Order

1. **Phase 1:** Postgres schema + MinIO + API (`/websearch/record` + `/receipts`) — 2-3 days
2. **Phase 2:** OpenClaw skill wrapper for `web_search` — 1-2 days
3. **Phase 3:** `/stats` endpoint + basic dashboard — 1-2 days
4. **Phase 4:** `tool.eval` receipts (needs agent integration) — 1-2 days
5. **Phase 5:** OTel export, additional tool wrappers — ongoing
6. **Phase 6:** Generic `/tool/record` endpoint — when 2nd tool is wrapped

---

## Appendix A: Example Full Request/Response

### POST /websearch/record

```bash
curl -X POST http://localhost:8420/api/v1/websearch/record \
  -H "Authorization: Bearer $LOCKN_RECEIPTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "call": {
      "receipt_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "type": "tool.call",
      "version": "0.1.0",
      "timestamp": "2026-02-02T18:22:42.123Z",
      "agent_id": "agent:main",
      "session_id": "agent:main:main",
      "model": "anthropic/claude-opus-4-5",
      "trace_id": null,
      "span_id": "00f067aa0ba902b7",
      "parent_span_id": null,
      "tool": {
        "name": "web_search",
        "call_id": "call_abc123",
        "status": "success",
        "duration_ms": 842,
        "error": null
      },
      "usage": { "input_tokens": null, "output_tokens": null },
      "cost_usd": null,
      "payloads": {
        "request": {
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "uri": "s3://lockn-receipts/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
          "bytes": 89,
          "content_type": "application/json"
        },
        "response": {
          "sha256": "a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890",
          "uri": "s3://lockn-receipts/a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890",
          "bytes": 14832,
          "content_type": "application/json"
        }
      },
      "web_search": {
        "query": "OpenTelemetry GenAI semantic conventions",
        "locale": "en",
        "country": "US",
        "freshness": null,
        "result_count": 5,
        "provider": "brave"
      }
    },
    "eval": null
  }'
```

---

## Appendix B: Future Extensions

- **Cost tracking:** Integrate with provider pricing APIs to auto-calculate `cost_usd`
- **Token metering:** If tools consume LLM tokens (e.g. browser with vision), track input/output tokens
- **Dashboard:** Grafana dashboard reading from Postgres for real-time cost/usage monitoring
- **Alerts:** Spike in error rate, cost threshold exceeded, latency degradation
- **Multi-agent:** Support multiple agents with per-agent API keys and RBAC
- **Replay:** Re-execute tool calls from stored payloads for testing/debugging
