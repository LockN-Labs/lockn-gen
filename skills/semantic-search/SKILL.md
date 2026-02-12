---
name: semantic-search
description: Search LockN codebase and memory semantically. Use when you need to find code by description, find implementations of concepts, locate relevant files across all LockN repositories, or search workspace memory (decisions, daily logs, project briefs, handoffs).
---

# Semantic Search (Code + Memory)

Search all LockN repositories and workspace memory using vector embeddings (qwen3-embedding + Qdrant).

## Quick Usage (CLI)

```bash
# Search
python3 /home/sean/.openclaw/workspace/tools/semantic-search/search-code.py "WebSocket connection handling"

# Search with limit
python3 /home/sean/.openclaw/workspace/tools/semantic-search/search-code.py "authentication middleware" --limit 5
```

## REST API (port 8899)

Start server:
```bash
python3 /home/sean/.openclaw/workspace/tools/semantic-search/server.py --port 8899
```

### Endpoints

**POST /search** — Search code
```json
{"query": "WebSocket connection handling", "limit": 10, "repo": "lockn-listen", "language": "cs"}
```
Returns: `{query, count, results: [{score, repo, file_path, start_line, end_line, language, content}]}`

**POST /index** — Trigger re-indexing
```json
{"full": false}
```

**GET /health** — Health check
**GET /stats** — Collection statistics


## Memory Search

Search workspace memory (daily logs, handoffs, project briefs, decisions, AGENTS.md):

```bash
# Search memory
python3 /home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py --search "auth decisions" --limit 5

# Filter by source type (daily, handoff, brief, decisions, project_log, memory, conventions)
python3 /home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py --search "XRPL architecture" --source-type decisions

# Filter by project
python3 /home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py --search "voice synthesis" --project speak
```

### Direct Qdrant Query (from any container)

```bash
# Any session can query Qdrant directly — no file system needed
curl -s http://localhost:6333/collections/lockn-memory/points/search \
  -H "Content-Type: application/json" \
  -d '{"vector": [EMBEDDING], "limit": 5, "with_payload": true}'
```

### Memory Collection: `lockn-memory` (133 vectors)
- **Sources:** daily logs, handoffs, project briefs, decisions, project logs, AGENTS.md
- **Privacy:** USER.md excluded, personal sections of MEMORY.md filtered
- **Chunking:** Section headers (##) for markdown, per-row for decision tables
- **Incremental:** Cron re-indexes every 30 min (tracks file hashes)

## Re-indexing

Incremental re-index runs via cron every 30 minutes:
```
*/30 * * * * /home/sean/.openclaw/workspace/tools/semantic-search/reindex-cron.sh
```

Force full re-index:
```bash
python3 /home/sean/.openclaw/workspace/tools/semantic-search/index-repos.py --full
```

## Indexed Repos
lockn-logger, lockn-speak, lockn-listen, lockn-ai-platform, lockn-score, lockn-gen, lockn-infra, lockn-apikeys

## Tech Stack
- **Embeddings:** qwen3-embedding via Ollama (:11434), 4096-dim vectors
- **Vector DB:** Qdrant (:6333), collection `lockn-code`
- **Chunking:** Function/class-level with ~150-line target, 20-line overlap
