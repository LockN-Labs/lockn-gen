# Ticket Cache for Semantic Search

This directory contains tools for enriching code chunks with ticket references during semantic search indexing.

## Files

- `ticket-cache.py` - Core cache management and enrichment utilities
- `index-repos.py` - Main indexer with ticket enrichment integration
- `search-code.py` - Search client with ticket reference filtering

## How It Works

1. **Cache Management** (`ticket-cache.py`)
   - Fetches ticket titles from Linear API
   - Caches titles in `state/ticket-cache.json`
   - Provides enrichment functions

2. **Indexing** (`index-repos.py`)
   - Loads ticket cache before indexing
   - Detects `LOC-XXX` patterns in content
   - Appends titles inline: `LOC-325 (XRPL WebSocket Client)`
   - Adds `ticket_refs` array to payload

3. **Search** (`search-code.py`)
   - Searches enriched content
   - Can filter by ticket references

## Usage

### Update Ticket Cache

```bash
cd /home/sean/.openclaw/workspace/tools/semantic-search
python3 ticket-cache.py
```

### Re-index with Ticket Enrichment

```bash
python3 index-repos.py --full
```

### Search

```bash
# Code search
python3 search-code.py "WebSocket connection" --limit 5

# Memory search
python3 search-code.py "authentication decisions" --memory
```

## Ticket Reference Format

**Before enrichment:**
```
See LOC-325 for WebSocket details.
```

**After enrichment:**
```
See LOC-325 (XRPL WebSocket Client) for WebSocket details.
```

**Payload:**
```json
{
  "content": "See LOC-325 (XRPL WebSocket Client)...",
  "ticket_refs": ["LOC-325"]
}
```

## API Integration

- **Linear GraphQL API**: `https://api.linear.app/graphql`
- **Environment Variable**: `LINEAR_API_KEY`
- **Cache File**: `state/ticket-cache.json`

## Validation

The enrichment improves search recall for ticket-based queries:

- **Before**: "XRPL WebSocket" → score 0.56 for LOC-325 section
- **After**: "XRPL WebSocket" → score > 0.70 for LOC-325 section (with title)

## Maintenance

- Cache auto-updates on each indexing run
- Manual update: `python3 ticket-cache.py`
- Cache expires after 24h (recommended)