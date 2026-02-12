# OpenClaw Subagent Orchestration & Queueing Research Report

**Date:** 2026-02-11  
**Author:** Subagent Research Cloud  
**Objective:** Design a smart orchestration and session queueing system for OpenClaw subagents with maxConcurrent=8

---

## Executive Summary

OpenClaw provides a solid foundation for agent orchestration with its session management, subagent spawning, and queueing infrastructure. However, the current system lacks explicit queueing for subagent spawns when at capacity. This report analyzes the current architecture, surveys best practices from other agent frameworks, and proposes implementation options for a production-grade orchestration system.

**Key Findings:**
- OpenClaw's queueing is designed for inbound channel messages, not subagent spawn coordination
- The `sessions_spawn` tool is non-blocking and returns immediately, but doesn't handle overflow gracefully
- A middleware queue service is the optimal approach for our needs
- We can leverage OpenClaw's existing session tracking for observability

---

## 1. Session Queueing Patterns

### Current State Analysis

OpenClaw has two distinct queueing systems:

1. **Inbound Message Queue** (`/concepts/queue`)
   - Serializes inbound auto-reply runs across channels
   - Lane-aware FIFO queue (main, cron, subagent lanes)
   - Per-session guarantee: only one active run per session
   - Max concurrency configured via `agents.defaults.maxConcurrent`

2. **Subagent Spawning** (`/tools/subagents`)
   - `sessions_spawn` is non-blocking: returns `{status: "accepted", runId, childSessionKey}`
   - No explicit queueing when at capacity
   - Uses dedicated subagent lane with default maxConcurrent=8
   - No backpressure mechanism when queue is full

### Queueing Patterns for Subagent Spawns

When we hit the `maxConcurrent=8` limit, we need to decide what happens to additional spawn requests:

| Pattern | Description | Pros | Cons | Suitability |
|---------|-------------|------|------|-------------|
| **Reject with Retry** | Return error + retry-after | Simple, stateless | Poor UX, client must handle retry | ❌ Low |
| **Drop New** | Discard overflow requests | Simple, protects system | Loses work | ❌ Low |
| **Drop Oldest** | Evict queued tasks | Prevents indefinite queuing | Loses oldest work | ⚠️ Medium |
| **FIFO Queue** | Wait in order | Fair, predictable | Potential indefinite wait | ✅ High |
| **Priority Queue** | Order by ticket priority | Respects Linear priorities | Complex implementation | ✅ High |

### Implementation Options

#### A. Agent-Level Orchestration

**Approach:** Orchestrator agent checks session count before spawning.

```typescript
// Orchestrator checks current state
const activeSubagents = await sessions_list({ kinds: ['subagent'], activeMinutes: 5 });
if (activeSubagents.length >= 8) {
  // Queue the spawn request
  await queue_add({
    task: request.task,
    priority: request.priority,
    timestamp: Date.now()
  });
}
```

**Pros:**
- No infrastructure changes
- Uses existing agent tooling
- Fast to prototype

**Cons:**
- Relies on agent memory (not persistent)
- No distributed coordination (multiple orchestrators)
- Race conditions when multiple spawns requested simultaneously
- No queue depth monitoring

#### B. Middleware Queue Service

**Approach:** Dedicated service manages spawn queue, communicates with Gateway.

```
┌─────────────┐    spawn request    ┌──────────────┐
│ Orchestrator ├───queued───────────▶│ Queue Service │
└─────────────┘                       └──────┬───────┘
                                            │
                                            │ spawn slot available
                                            ▼
┌─────────────┐    spawn command     ┌──────────────┐
│ Orchestrator ◀────ack──────────────│ OpenClaw GW  │
└─────────────┘                       └──────────────┘
```

**Pros:**
- Persistent queue (survives restarts)
- True FIFO/priority ordering
- Cross-orchestrator coordination
- Rich observability

**Cons:**
- Additional infrastructure
- Network latency (minimal)
- Development effort

#### C. Hook/Plugin-Based

**Approach:** OpenClaw hook intercepts `sessions_spawn`, routes through queue.

```javascript
// Pseudo-configuration
hooks: {
  sessions_spawn: {
    before: 'queue-intercept',
    queue: {
      mode: 'priority',
      capacity: 100,
      workers: 2
    }
  }
}
```

**Pros:**
- Native integration
- No external dependencies
- Guaranteed atomicity

**Cons:**
- Requires OpenClaw fork/modification
- Complex hook system
- Limited to single gateway instance

### Tradeoff Evaluation

| Factor | Agent-Level | Middleware | Hook/Plugin |
|--------|-------------|------------|-------------|
| **Complexity** | Low | Medium | High (fork needed) |
| **Reliability** | Medium | High | High |
| **Scalability** | Low | High | Medium (single GW) |
| **Observability** | Low | High | Medium |
| **Development Time** | 1-2 days | 1-2 weeks | 2-4 weeks |
| **Maintenance** | Low | Medium | High |

**Recommendation:** Middleware queue service (Option B)

---

## 2. Smart Orchestration Patterns

### Orchestrator Agent Design

The orchestrator acts as the central dispatch center for subagent work:

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                       │
│  (Opus model - cloud)                                       │
│  - Receives work from Linear tickets                       │
│  - Checks queue depth & capacity                            │
│  - Routes to appropriate subagent lane                     │
│  - Reports status to Slack/Linear                          │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Queue Depth  │  │  Priority     │  │  Backpressure │
│  Check        │  │  Queue        │  │  Handling     │
│  - sessions_  │  │  - Linear     │  │  - Queue full?│
│    list()     │  │    ticket     │  │  - Timeout    │
│  - Active     │  │    priority   │  │  - Retry      │
│    count      │  │    ordering   │  │  - Fallback   │
└───────────────┘  └───────────────┘  └───────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  Subagent Spawn   │
                    │  - Coder-Next     │
                    │  - Vision models  │
                    │  - Cloud models   │
                    └───────────────────┘
```

### Core Components

#### 1. Session Count Check

```typescript
async function getActiveSubagentCount() {
  const sessions = await sessions_list({
    kinds: ['subagent'],
    activeMinutes: 5  // Only count recently active
  });
  
  return sessions.filter(s => 
    !s.abortedLastRun && 
    s.totalTokens < 100000  // Exclude completed small tasks
  ).length;
}
```

#### 2. Priority Queue Implementation

```typescript
interface SpawnRequest {
  id: string;              // Linear ticket ID
  task: string;
  priority: 'urgent' | 'high' | 'normal' | 'low';
  blockedBy?: string[];    // Linear blocking relations
  timestamp: number;
  metadata?: Record<string, any>;
}

// Priority order: urgent > high > normal > low
const PRIORITY_ORDER = {
  'urgent': 0,
  'high': 1,
  'normal': 2,
  'low': 3
};

function sortByPriority(requests: SpawnRequest[]): SpawnRequest[] {
  return requests.sort((a, b) => {
    // First by priority
    const priorityDiff = PRIORITY_ORDER[a.priority] - PRIORITY_ORDER[b.priority];
    if (priorityDiff !== 0) return priorityDiff;
    
    // Then by timestamp (FIFO within same priority)
    return a.timestamp - b.timestamp;
  });
}
```

#### 3. Backpressure Handling

When queue is at capacity:

```typescript
async function handleBackpressure(request: SpawnRequest): Promise<void> {
  const queue = await getQueue();
  const activeCount = await getActiveSubagentCount();
  
  if (queue.length >= MAX_QUEUE_SIZE) {
    // Queue is full - decide what to do
    if (request.priority === 'urgent') {
      // Evict lowest priority task
      const lowPriorityTasks = queue.filter(r => r.priority === 'low');
      if (lowPriorityTasks.length > 0) {
        const evicted = lowPriorityTasks[0];
        await removeQueueItem(evicted.id);
        logger.warn(`Evicted low-priority task ${evicted.id} to make room for urgent request`);
      }
    } else {
      // Return error with retry-after
      throw new BackpressureError({
        message: 'Spawn queue full',
        retryAfter: Math.ceil(QUEUE_TIMEOUT_MS / 1000),
        queueDepth: queue.length,
        activeCount: activeCount
      });
    }
  }
}
```

#### 4. Failed Spawn Retry

```typescript
async function spawnWithRetry(request: SpawnRequest, maxRetries = 3): Promise<string> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await sessions_spawn({
        task: request.task,
        label: `${request.id}-${request.priority}`,
        model: determineModelForTask(request)
      });
      
      // Track spawn event
      await logSpawnEvent({
        requestId: request.id,
        sessionId: result.childSessionKey,
        status: 'spawned',
        timestamp: Date.now()
      });
      
      return result.childSessionKey;
    } catch (error) {
      if (attempt === maxRetries) {
        await logSpawnEvent({
          requestId: request.id,
          status: 'failed',
          error: error.message,
          retryCount: attempt,
          timestamp: Date.now()
        });
        throw error;
      }
      
      // Wait before retry (exponential backoff)
      const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
      await sleep(delay);
    }
  }
}
```

### Queue Metrics

Track these key metrics for observability:

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Queue Depth** | Number of pending spawn requests | > 50 |
| **Avg Wait Time** | Time from request to spawn | > 30 seconds |
| **Max Concurrency** | Active subagents / max allowed | > 90% |
| **Failed Spawns** | Spawns that couldn't execute | > 5/min |
| **Eviction Rate** | Queue evictions / total requests | > 10% |

---

## 3. Observability via LockN Logger

### Event Schema

All orchestration events should follow a consistent schema:

```typescript
interface OrchestrationEvent {
  // Core metadata
  eventId: string;              // UUID
  timestamp: number;            // Unix timestamp (ms)
  eventType: string;            // 'spawn_requested', 'queued', 'dispatched', etc.
  
  // Context
  agentId: string;              // OpenClaw agent ID
  requestId: string;            // External ID (Linear ticket)
  
  // Queue state
  queueDepthBefore: number;
  queueDepthAfter: number;
  activeCount: number;
  
  // Timing
  waitTimeMs?: number;
  totalTimeMs?: number;
  
  // Outcome
  status: 'success' | 'failed' | 'queued' | 'evicted' | 'timeout';
  errorMessage?: string;
  
  // Metadata
  priority?: string;
  model?: string;
  sessionId?: string;
  childSessionKey?: string;
}
```

### Event Types

| Event Type | When | Key Fields |
|------------|------|------------|
| `spawn_requested` | Orchestrator receives work | requestId, priority, queueDepthBefore |
| `queued` | Added to queue | queueDepthAfter, waitTimeMs (0) |
| `dispatched` | Spawn command sent | sessionId, waitTimeMs, model |
| `completed` | Subagent finished | totalTimeMs, tokens, cost |
| `failed` | Spawn or execution failed | errorMessage, retryCount |
| `evicted` | Queue overflow, task dropped | evictedPriority, queueDepth |
| `backpressure_applied` | Backpressure triggered | retryAfter, queueDepth |

### LockN Logger Integration

```typescript
async function logOrchestrationEvent(event: OrchestrationEvent) {
  // Enrich with additional context
  const enrichedEvent = {
    ...event,
    source: 'orchestration',
    service: 'subagent-queue',
    version: '1.0.0'
  };
  
  // Send to LockN Logger
  await locknLogger.log('orchestration', enrichedEvent);
  
  // Also emit to metrics pipeline
  emitMetrics(event);
}
```

### Dashboard Queries

**Queue Depth Over Time:**
```sql
SELECT 
  time_bucket('1m', timestamp) as minute,
  avg(queueDepthAfter) as avg_depth,
  max(queueDepthAfter) as max_depth
FROM orchestration_events
WHERE eventType = 'queued'
GROUP BY 1
ORDER BY 1 DESC
LIMIT 1440;  -- Last 24 hours
```

**Wait Time Percentiles:**
```sql
SELECT 
  percentile_cont(0.5) WITHIN GROUP (ORDER BY waitTimeMs) as p50,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY waitTimeMs) as p90,
  percentile_cont(0.95) WITHIN GROUP (ORDER BY waitTimeMs) as p95
FROM orchestration_events
WHERE eventType = 'dispatched'
  AND timestamp > now() - interval '1 hour';
```

**Concurrency Utilization:**
```sql
SELECT 
  time_bucket('5m', timestamp) as period,
  avg(activeCount) as avg_active,
  max(activeCount) as max_active,
  8 as max_capacity
FROM orchestration_events
WHERE eventType IN ('queued', 'dispatched')
GROUP BY 1
ORDER BY 1 DESC;
```

### Alerting Rules

```yaml
alerts:
  - name: Queue Depth High
    condition: avg(queueDepthAfter) > 50
    window: 5m
    severity: warning
    notify: ["slack-orchestration", "pager-urgent"]
  
  - name: High Wait Time
    condition: p95(waitTimeMs) > 30000
    window: 10m
    severity: warning
    notify: ["slack-orchestration"]
  
  - name: High Failure Rate
    condition: count(status='failed') / count(*) > 0.1
    window: 5m
    severity: critical
    notify: ["slack-orchestration", "pager-critical"]
  
  - name: Concurrency Saturation
    condition: avg(activeCount) / 8 > 0.9
    window: 15m
    severity: info
    notify: ["slack-orchestration"]
```

---

## 4. Existing Art: Agent Framework Comparison

### CrewAI

**Task Queueing:**
- Uses `max_passage` parameter to limit concurrent tasks
- Sequential vs parallel processing modes
- No explicit queueing for overflow tasks

**What We Can Steal:**
- Task abstraction with `Task` class
- Process patterns (sequential, hierarchical)
- Agent delegation patterns

**Limitations:**
- No built-in persistence
- No priority-based scheduling
- Not designed for distributed systems

### AutoGen

**Group Chat Concurrency:**
- `max_round` limits conversation turns
- `max_consecutive_auto_reply` limits agent responses
- No explicit task queueing

**What We Can Steal:**
- User proxy agent pattern
- Group chat manager abstraction
- Termination condition patterns

**Limitations:**
- In-memory state (no persistence)
- No queueing for overflow
- Single-threaded execution

### LangGraph

**State Management:**
- Reducers handle concurrent state updates
- Checkpointing for persistence
- Conditional edges for branching

**What We Can Steal:**
- State management with reducers
- Checkpointing for recovery
- Graph-based workflow definition

**Limitations:**
- Focus on state, not task scheduling
- No priority queueing
- Single-node execution

### comparison

| Feature | CrewAI | AutoGen | LangGraph | Our Solution |
|---------|--------|---------|-----------|--------------|
| Task Queueing | ❌ Basic | ❌ None | ❌ None | ✅ Priority FIFO |
| Persistence | ❌ None | ❌ None | ✅ Checkpoints | ✅ Queue DB |
| Priority | ❌ None | ❌ None | ❌ None | ✅ Linear priority |
| Distributed | ❌ Single node | ❌ Single node | ❌ Single node | ✅ Multi-orchestrator |
| Observability | ⚠️ Basic logs | ⚠️ Basic logs | ⚠️ Tracing | ✅ Full metrics |
| Retry/Failover | ❌ None | ❌ None | ❌ None | ✅ Exponential backoff |

### Key Insights

1. **All frameworks lack production-grade queueing** - This is an underserved problem
2. **State management is mature** - We can borrow patterns but need to add queueing
3. **Observability is often an afterthought** - We'll build it in from day one
4. **Persistence is critical for reliability** - Queue must survive restarts

---

## 5. Implementation Options

### Option A: Pure Agent-Level (Complexity: 1/5)

**Description:** Orchestrator uses prompt engineering and tool calls to manage queueing.

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│  Orchestrator Agent (Opus)                              │
│  - Maintains queue in memory (sessions_history)         │
│  - Checks capacity before spawning                      │
│  - Uses prompt instructions for ordering                │
└─────────────────────────────────────────────────────────┘
```

**Implementation:**

```typescript
// SKILL.md for orchestrator
/*
## Queue Management

When receiving new work:

1. Check current queue depth:
   - Call sessions_list with kinds=['subagent'] and activeMinutes=5
   - Filter for active (not aborted, recent activity)
   - Count = active count

2. If count < 8:
   - Spawn immediately via sessions_spawn

3. If count >= 8:
   - Add to queue (write to workspace/queue.json)
   - Include: id, task, priority, timestamp
   - Sort queue by: priority (urgent>high>normal>low), then timestamp
   - Report: "Queued task #LINEAR-123 (priority: normal, position: 3)"
*/

// Queue check before spawn
async function spawnIfCapacity(task, priority) {
  const active = await getActiveSubagents();
  
  if (active.length < 8) {
    return await sessions_spawn({ task, label: `direct-${Date.now()}` });
  } else {
    // Add to queue
    const queue = await loadQueue();
    queue.push({
      id: generateId(),
      task,
      priority,
      timestamp: Date.now()
    });
    
    // Sort by priority
    queue.sort((a, b) => {
      const priorityOrder = { urgent: 0, high: 1, normal: 2, low: 3 };
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    });
    
    await saveQueue(queue);
    
    const position = queue.findIndex(item => item.id === id) + 1;
    return { queued: true, position, total: queue.length };
  }
}
```

**Pros:**
- ✅ No infrastructure changes
- ✅ Fast to prototype (1-2 days)
- ✅ Uses existing agent tooling

**Cons:**
- ❌ Memory-only queue (lost on restart)
- ❌ No distributed coordination
- ❌ Race conditions
- ❌ Limited observability

**Effort:** 1-2 days  
**Reliability:** Medium  
**Limitations:** Single orchestrator, no persistence

---

### Option B: Lightweight Queue Service (Complexity: 3/5)

**Description:** Dedicated service manages spawn queue with database persistence.

**Architecture:**
```
┌─────────────┐     ┌──────────────────┐
│ Orchestrator│────▶│  Queue Service   │
│  (multiple) │     │  - PostgreSQL    │
└─────────────┘     │  - API endpoint  │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    │  OpenClaw Gateway│
                    └──────────────────┘
```

**Implementation:**

**1. Queue Database Schema:**

```sql
CREATE TABLE spawn_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  linear_ticket_id TEXT NOT NULL,
  task TEXT NOT NULL,
  priority TEXT NOT NULL CHECK (priority IN ('urgent', 'high', 'normal', 'low')),
  blocked_by TEXT[],  -- Array of blocking ticket IDs
  status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'dispatched', 'completed', 'failed', 'evicted')),
  model TEXT,
  session_id TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  dispatched_at TIMESTAMP,
  completed_at TIMESTAMP,
  error_message TEXT,
  priority_order INTEGER NOT NULL  -- 0=urgent, 1=high, 2=normal, 3=low
);

CREATE INDEX idx_spawn_status ON spawn_requests(status);
CREATE INDEX idx_spawn_priority ON spawn_requests(priority_order, created_at);
CREATE INDEX idx_spawn_linear ON spawn_requests(linear_ticket_id);
```

**2. Queue Service API:**

```typescript
// queue-service.ts
import express from 'express';
import { Pool } from 'pg';

const app = express();
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Add request to queue
app.post('/queue', async (req, res) => {
  const { linearTicketId, task, priority, blockedBy, model } = req.body;
  
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    
    const result = await client.query(
      `INSERT INTO spawn_requests 
       (linear_ticket_id, task, priority, blocked_by, model, priority_order)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING id, created_at`,
      [linearTicketId, task, priority, blockedBy || null, model, PRIORITY_MAP[priority]]
    );
    
    await client.query('COMMIT');
    
    res.status(201).json({
      id: result.rows[0].id,
      status: 'queued',
      position: await getQueuePosition(client, linearTicketId),
      queueDepth: await getQueueDepth(client)
    });
  } catch (error) {
    await client.query('ROLLBACK');
    res.status(500).json({ error: 'Failed to add to queue' });
  } finally {
    client.release();
  }
});

// Get next request to dispatch
app.get('/queue/next', async (req, res) => {
  const client = await pool.connect();
  try {
    const result = await client.query(
      `SELECT * FROM spawn_requests 
       WHERE status = 'queued' 
       ORDER BY priority_order, created_at 
       LIMIT 1 
       FOR UPDATE SKIP LOCKED`
    );
    
    if (result.rows.length === 0) {
      return res.json({ next: null });
    }
    
    const request = result.rows[0];
    
    // Mark as dispatched
    await client.query(
      `UPDATE spawn_requests 
       SET status = 'dispatched', dispatched_at = NOW()
       WHERE id = $1`,
      [request.id]
    );
    
    await client.query('COMMIT');
    
    res.json({
      id: request.id,
      linearTicketId: request.linear_ticket_id,
      task: request.task,
      priority: request.priority,
      model: request.model
    });
  } catch (error) {
    await client.query('ROLLBACK');
    res.status(500).json({ error: 'Failed to get next request' });
  } finally {
    client.release();
  }
});

// Report completion
app.post('/queue/:id/completed', async (req, res) => {
  const { id } = req.params;
  const { sessionId, tokens, cost } = req.body;
  
  const client = await pool.connect();
  try {
    await client.query(
      `UPDATE spawn_requests 
       SET status = 'completed', 
           session_id = $1,
           completed_at = NOW()
       WHERE id = $2`,
      [sessionId, id]
    );
    
    await client.query('COMMIT');
    res.json({ status: 'success' });
  } catch (error) {
    await client.query('ROLLBACK');
    res.status(500).json({ error: 'Failed to mark completed' });
  } finally {
    client.release();
  }
});

// Report failure
app.post('/queue/:id/failed', async (req, res) => {
  const { id } = req.params;
  const { error, retryCount } = req.body;
  
  const client = await pool.connect();
  try {
    await client.query(
      `UPDATE spawn_requests 
       SET status = 'failed', 
           error_message = $1,
           completed_at = NOW()
       WHERE id = $2`,
      [error, id]
    );
    
    await client.query('COMMIT');
    res.json({ status: 'success' });
  } catch (error) {
    await client.query('ROLLBACK');
    res.status(500).json({ error: 'Failed to mark failed' });
  } finally {
    client.release();
  }
});
```

**3. Worker Process:**

```typescript
// worker.ts
import fetch from 'node-fetch';

const QUEUE_SERVICE_URL = process.env.QUEUE_SERVICE_URL || 'http://localhost:3001';

async function dispatchLoop() {
  while (true) {
    try {
      // Get next request from queue
      const response = await fetch(`${QUEUE_SERVICE_URL}/queue/next`);
      const data = await response.json();
      
      if (!data.next) {
        // No work, wait before polling again
        await sleep(1000);
        continue;
      }
      
      // Check gateway capacity
      const activeCount = await getActiveSubagentCount();
      if (activeCount >= 8) {
        // Gateway at capacity, requeue
        await fetch(`${QUEUE_SERVICE_URL}/queue/${data.id}/requeue`, { method: 'POST' });
        await sleep(2000);  // Wait before retry
        continue;
      }
      
      // Spawn subagent
      try {
        const spawnResult = await sessions_spawn({
          task: data.task,
          label: data.linearTicketId,
          model: data.model
        });
        
        // Report success to queue
        await fetch(`${QUEUE_SERVICE_URL}/queue/${data.id}/completed`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            sessionId: spawnResult.childSessionKey,
            tokens: 0  // Will be updated when session completes
          })
        });
      } catch (spawnError) {
        // Report failure
        await fetch(`${QUEUE_SERVICE_URL}/queue/${data.id}/failed`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            error: spawnError.message,
            retryCount: 1
          })
        });
      }
      
    } catch (error) {
      console.error('Worker error:', error);
      await sleep(5000);  // Back off on error
    }
  }
}

async function getActiveSubagentCount() {
  const sessions = await sessions_list({
    kinds: ['subagent'],
    activeMinutes: 5
  });
  
  return sessions.filter(s => !s.abortedLastRun).length;
}

// Start worker
dispatchLoop();
```

**4. Orchestration Integration:**

```typescript
// orchestrator-skill.ts
async function handleNewWork(request) {
  // Add to queue
  const queueResponse = await fetch(`${QUEUE_SERVICE_URL}/queue`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      linearTicketId: request.id,
      task: request.task,
      priority: request.priority,
      blockedBy: request.blockedBy,
      model: determineModel(request)
    })
  });
  
  const queueData = await queueResponse.json();
  
  if (queueData.position === 1 && activeCount < 8) {
    // First in queue and capacity available, trigger immediate dispatch
    triggerWorker();
  }
  
  return {
    queued: true,
    position: queueData.position,
    total: queueData.queueDepth,
    ticketId: request.id
  };
}
```

**Pros:**
- ✅ Persistent queue (survives restarts)
- ✅ True FIFO/priority ordering
- ✅ Cross-orchestrator coordination
- ✅ Rich observability
- ✅ Scalable

**Cons:**
- ❌ Requires PostgreSQL setup
- ❌ Additional service to maintain
- ❌ Network latency (minimal)

**Effort:** 1-2 weeks  
**Reliability:** High  
**Limitations:** Single queue service (can add HA later)

---

### Option C: OpenClaw Hook/Plugin (Complexity: 4/5)

**Description:** Modify OpenClaw to intercept `sessions_spawn` with queueing logic.

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│  Orchestrator                                           │
│    ↓ sessions_spawn()                                   │
├─────────────────────────────────────────────────────────┤
│  OpenClaw Gateway                                       │
│    ↓ sessions_spawn() call                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Hook: queue-intercept                           │  │
│  │  - Check capacity                                │  │
│  │  - Add to queue if at limit                      │  │
│  │  - Dispatch when slot available                  │  │
│  └──────────────────────────────────────────────────┘  │
│    ↓                                                    │
│  sessions_spawn() (if capacity available)              │
└─────────────────────────────────────────────────────────┘
```

**Implementation:**

**1. Hook Configuration:**

```json
// openclaw.json
{
  "hooks": {
    "sessions_spawn": {
      "enabled": true,
      "queue": {
        "mode": "priority",
        "capacity": 100,
        "workers": 2,
        "database": {
          "type": "postgres",
          "connection": "postgresql://user:pass@localhost:5432/openclaw_queue"
        }
      }
    }
  }
}
```

**2. Hook Implementation (Pseudo-code):**

```typescript
// hooks/queue-intercept.ts
import { Hook } from '@openclaw/core';
import { Pool } from 'pg';

export class QueueInterceptHook implements Hook {
  private pool: Pool;
  private workerRunning = false;

  async init() {
    this.pool = new Pool({
      connectionString: this.config.database.connection
    });
    
    await this.createQueueTable();
    this.startWorker();
  }

  async beforeSessionsSpawn(params: SessionsSpawnParams) {
    const activeCount = await this.getActiveSubagentCount();
    
    if (activeCount >= 8) {
      // At capacity, queue the spawn
      return await this.queueSpawn(params);
    }
    
    // Capacity available, proceed normally
    return null;  // Continue with normal spawn
  }

  async afterSessionsSpawn(result: SessionsSpawnResult) {
    // Log successful spawn
    await this.logSpawn(result);
  }

  private async queueSpawn(params: SessionsSpawnParams) {
    const client = await this.pool.connect();
    
    try {
      await client.query('BEGIN');
      
      const result = await client.query(
        `INSERT INTO spawn_queue 
         (task, priority, params_json, created_at, status)
         VALUES ($1, $2, $3, NOW(), 'queued')
         RETURNING id`,
        [params.task, params.priority || 'normal', JSON.stringify(params)]
      );
      
      await client.query('COMMIT');
      
      return {
        queued: true,
        queueId: result.rows[0].id,
        message: 'Spawn queued - will be dispatched when capacity is available'
      };
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  private async startWorker() {
    if (this.workerRunning) return;
    this.workerRunning = true;
    
    setInterval(async () => {
      const client = await this.pool.connect();
      
      try {
        // Get next queued spawn
        const result = await client.query(
          `SELECT * FROM spawn_queue 
           WHERE status = 'queued' 
           ORDER BY priority, created_at 
           LIMIT 1 
           FOR UPDATE SKIP LOCKED`
        );
        
        if (result.rows.length === 0) return;
        
        const queuedSpawn = result.rows[0];
        
        // Check capacity again
        const activeCount = await this.getActiveSubagentCount();
        if (activeCount >= 8) return;
        
        // Mark as processing
        await client.query(
          `UPDATE spawn_queue SET status = 'processing' WHERE id = $1`,
          [queuedSpawn.id]
        );
        
        await client.query('COMMIT');
        
        // Execute spawn
        try {
          const spawnResult = await this.executeSpawn(queuedSpawn.params_json);
          
          await client.query(
            `UPDATE spawn_queue 
             SET status = 'completed', 
                 session_id = $1,
                 completed_at = NOW()
             WHERE id = $2`,
            [spawnResult.childSessionKey, queuedSpawn.id]
          );
        } catch (error) {
          await client.query(
            `UPDATE spawn_queue 
             SET status = 'failed', 
                 error = $1,
                 completed_at = NOW()
             WHERE id = $2`,
            [error.message, queuedSpawn.id]
          );
        } finally {
          client.release();
        }
      } catch (error) {
        client.release();
      }
    }, 1000);  // Poll every second
  }

  private async getActiveSubagentCount() {
    // Use sessions_list to check capacity
    const sessions = await sessions_list({
      kinds: ['subagent'],
      activeMinutes: 5
    });
    
    return sessions.filter(s => !s.abortedLastRun).length;
  }
}
```

**Pros:**
- ✅ Native integration
- ✅ No external dependencies
- ✅ Guaranteed atomicity
- ✅ Zero network latency

**Cons:**
- ❌ Requires OpenClaw fork
- ❌ Complex hook system
- ❌ Limited to single gateway
- ❌ Maintenance burden

**Effort:** 2-4 weeks  
**Reliability:** High  
**Limitations:** Requires fork, single GW only

---

## 6. Recommended Implementation Plan

### Phase 1: Quick Validation (1 week)

**Goal:** Prove the concept with minimal infrastructure

**Approach:** Option A (Agent-Level) + Simple File Queue

**Deliverables:**
- ✅ Working queue in `workspace/queue.json`
- ✅ Priority ordering (urgent > high > normal > low)
- ✅ Basic observability (queue depth metrics)
- ✅ Integration with Linear ticket priorities

**Implementation:**

```typescript
// workspace/orchestrator/skill.ts

interface SpawnRequest {
  id: string;              // Linear ticket ID
  task: string;
  priority: 'urgent' | 'high' | 'normal' | 'low';
  timestamp: number;
  metadata?: Record<string, any>;
}

// Load queue from file
async function loadQueue(): Promise<SpawnRequest[]> {
  const fs = require('fs');
  const path = require('path');
  
  const queuePath = path.join(__dirname, 'queue.json');
  
  try {
    const data = fs.readFileSync(queuePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    return [];
  }
}

// Save queue to file
async function saveQueue(queue: SpawnRequest[]): Promise<void> {
  const fs = require('fs');
  const path = require('path');
  
  const queuePath = path.join(__dirname, 'queue.json');
  fs.writeFileSync(queuePath, JSON.stringify(queue, null, 2));
}

// Add request to queue
async function queueSpawn(request: SpawnRequest): Promise<void> {
  const queue = await loadQueue();
  
  queue.push(request);
  
  // Sort by priority
  const priorityOrder = { urgent: 0, high: 1, normal: 2, low: 3 };
  queue.sort((a, b) => {
    const priorityDiff = priorityOrder[a.priority] - priorityOrder[b.priority];
    if (priorityDiff !== 0) return priorityDiff;
    return a.timestamp - b.timestamp;
  });
  
  await saveQueue(queue);
  
  // Log event
  await logOrchestrationEvent({
    eventType: 'queued',
    requestId: request.id,
    queueDepthAfter: queue.length,
    priority: request.priority,
    timestamp: Date.now()
  });
}

// Get next request to spawn
async function getNextSpawn(): Promise<SpawnRequest | null> {
  const queue = await loadQueue();
  
  if (queue.length === 0) return null;
  
  // Remove first item (highest priority)
  const next = queue.shift();
  await saveQueue(queue);
  
  return next;
}

// Main dispatch loop
async function dispatchLoop(): Promise<void> {
  while (true) {
    try {
      const nextSpawn = await getNextSpawn();
      
      if (!nextSpawn) {
        // No work, wait
        await sleep(1000);
        continue;
      }
      
      // Check capacity
      const activeCount = await getActiveSubagentCount();
      
      if (activeCount >= 8) {
        // At capacity, requeue
        await queueSpawn(nextSpawn);
        await sleep(2000);
        continue;
      }
      
      // Spawn subagent
      const result = await sessions_spawn({
        task: nextSpawn.task,
        label: nextSpawn.id,
        model: determineModel(nextSpawn)
      });
      
      // Log completion
      await logOrchestrationEvent({
        eventType: 'dispatched',
        requestId: nextSpawn.id,
        sessionId: result.childSessionKey,
        waitTimeMs: Date.now() - nextSpawn.timestamp,
        timestamp: Date.now()
      });
      
    } catch (error) {
      console.error('Dispatch error:', error);
      await sleep(5000);
    }
  }
}

// Helper: Get active subagent count
async function getActiveSubagentCount(): Promise<number> {
  const sessions = await sessions_list({
    kinds: ['subagent'],
    activeMinutes: 5
  });
  
  return sessions.filter(s => !s.abortedLastRun).length;
}
```

### Phase 2: Production-Grade Queue (3-4 weeks)

**Goal:** Replace file queue with database-backed service

**Approach:** Option B (Middleware Queue Service)

**Deliverables:**
- ✅ PostgreSQL queue database
- ✅ Queue service API
- ✅ Worker process
- ✅ Full observability with LockN Logger
- ✅ Scalable to multiple orchestrators

### Phase 3: Advanced Features (2-3 weeks)

**Goal:** Add priority handling, backpressure, and automation

**Deliverables:**
- ✅ Linear ticket priority integration
- ✅ blockedBy relation handling
- ✅ Automatic evictions for urgent tasks
- ✅ Backpressure alerts
- ✅ Retry logic with exponential backoff

---

## 7. Conclusion

**Summary:**
OpenClaw has a solid foundation for agent orchestration, but lacks explicit queueing for subagent spawns when at capacity. The current `sessions_spawn` tool is non-blocking but provides no backpressure mechanism.

**Recommended Approach:**
1. **Start with Option A** (Agent-Level) for rapid validation
2. **Migrate to Option B** (Middleware Queue Service) for production
3. **Avoid Option C** (Hook/Plugin) due to fork requirements

**Key Advantages of Middleware Queue Service:**
- Persistent queue (survives restarts)
- True FIFO/priority ordering
- Cross-orchestrator coordination
- Rich observability
- Scalable architecture

**Timeline:**
- Phase 1 (Validation): 1 week
- Phase 2 (Production): 3-4 weeks
- Phase 3 (Advanced): 2-3 weeks
- **Total: 6-8 weeks for full implementation**

**Risk Mitigation:**
- Start with simple file-based queue
- Incrementally add features
- Keep observability built-in
- Design for horizontal scaling from day one

---

## Appendix: Example Event Flow

```
┌─────────────────┐
│ Linear Ticket   │
│ "Implement API" │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ Orchestrator         │
│ Receives work        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Queue Service        │
│ POST /queue          │
│ - Add to PostgreSQL  │
│ - Return position: 3 │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Worker (polls)       │
│ GET /queue/next      │
│ - Returns request #3 │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Gateway Check        │
│ sessions_list()      │
│ - Active: 6/8        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ sessions_spawn()     │
│ - Creates subagent   │
│ - Returns sessionKey │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Worker Reports       │
│ POST /queue/:id/     │
│ completed            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ LockN Logger         │
│ - spawn_dispatched   │
│ - waitTime: 12s      │
│ - queueDepth: 2      │
└──────────────────────┘
```

---

*This report was generated by the orchestration-research subagent on 2026-02-11.*