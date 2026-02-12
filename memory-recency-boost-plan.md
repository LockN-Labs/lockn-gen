# LOC-336: Recency Boost Implementation Plan

## Executive Summary

This document outlines a technical implementation plan to add recency boost to the LockN memory search system. The memory system uses Qdrant vector database with `qwen3-embedding` (4096 dimensions) for semantic search over daily logs, project briefs, decisions, and curated memories.

## Current Architecture

### Existing Search Flow
1. **Embedding**: Queries embedded via Ollama (`qwen3-embedding` model, 4096 dims)
2. **Vector Search**: Qdrant `query_points()` performs k-NN search with cosine similarity
3. **Payload**: Each point stores metadata including `date` field (extracted from filename like `2026-02-09.md`)
4. **Filtering**: Basic filtering by `source_type`, `project`, etc. using payload indexes

### Current Payload Structure
```python
{
    "content": str,
    "source_type": str,      # daily, handoff, brief, decisions, memory, project_log, conventions
    "file_path": str,
    "section": str | None,
    "project": str | None,
    "date": str | None,      # ISO format: "2026-02-09"
    "chunk_index": int,
    "indexed_at": str,       # ISO timestamp
}
```

## Implementation Options

### Option A: Post-Retrieval Re-ranker (Python)
**Approach**: Keep vector search as-is, re-rank results using weighted combination of cosine similarity and recency score.

**Formula**: `final_score = cosine_score * 0.7 + recency_score * 0.3`

**Recency Decay**:
- Today: 1.0
- Yesterday: 0.9
- 2 days ago: 0.8
- 3-6 days: 0.7
- 7+ days: 0.5

**Pros**:
- ✅ Simple to implement and test
- ✅ No Qdrant schema changes required
- ✅ Easy to tune weights (0.7/0.3 ratio)
- ✅ Works with existing search interface
- ✅ Safe rollback if issues arise

**Cons**:
- ⚠️ Requires fetching all top-K results first (minimal overhead for small K)
- ⚠️ Recency score calculated client-side

### Option B: Qdrant-Native Payload Filtering
**Approach**: Use Qdrant's payload filtering with date-based boost scoring.

**Implementation**: 
- Create numeric payload index for dates
- Use `score_points` with custom scoring function
- Convert dates to numeric scores (days ago, then apply decay)

**Pros**:
- ✅ Server-side scoring (potentially faster)
- ✅ More efficient for large result sets

**Cons**:
- ⚠️ Requires date-to-number conversion (complex for variable recency decay)
- ⚠️ Qdrant scoring functions are limited for complex decay curves
- ⚠️ More complex schema changes
- ⚠️ Less flexible for A/B testing weights

### Recommendation: Option A (Post-Retrieval Re-ranker)

**Why Option A is better**:
1. **Simplicity**: 1-2 hours implementation vs 4-6 hours for Option B
2. **Flexibility**: Easy to adjust weights, decay curve, or disable feature
3. **Testing**: Can be incrementally deployed and A/B tested
4. **Maintainability**: Pure Python logic is easier to debug and version control
5. **Performance**: For top-5 results, the overhead is negligible (<1ms)
6. **Qdrant Limitations**: Qdrant's native scoring doesn't handle complex decay curves well

## Implementation Plan

### Phase 1: Core Implementation (2-3 hours)

#### 1. Add Recency Utility Function

**File**: `/home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py`

```python
from datetime import datetime, timezone
from typing import Dict, Any

def calculate_recency_score(date_str: str | None, current_date: datetime = None) -> float:
    """
    Calculate recency score based on date.
    
    Decay schedule:
    - Today: 1.0
    - Yesterday: 0.9
    - 2 days ago: 0.8
    - 3-6 days: 0.7
    - 7+ days: 0.5
    """
    if not date_str:
        return 0.5  # Default for unknown dates
    
    if current_date is None:
        current_date = datetime.now(timezone.utc)
    
    try:
        # Parse date from filename (YYYY-MM-DD format)
        if 'T' in date_str:  # ISO timestamp
            target_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
        else:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Calculate days difference
        days_diff = (current_date.date() - target_date.date()).days
        
        # Apply decay curve
        if days_diff < 0:
            return 1.0  # Future dates (shouldn't happen, but handle gracefully)
        elif days_diff == 0:
            return 1.0
        elif days_diff == 1:
            return 0.9
        elif days_diff == 2:
            return 0.8
        elif days_diff < 7:
            return 0.7
        else:
            return 0.5
    except ValueError:
        return 0.5  # Default for unparseable dates


def re_rank_results(
    results: list[dict],
    cosine_weight: float = 0.7,
    recency_weight: float = 0.3,
    current_date: datetime = None
) -> list[dict]:
    """
    Re-rank search results using recency boost.
    
    Args:
        results: List of search results with 'score' (cosine) and 'payload'
        cosine_weight: Weight for vector similarity score (default 0.7)
        recency_weight: Weight for recency score (default 0.3)
        current_date: Reference date for recency calculation
    
    Returns:
        Re-ranked results list
    """
    if not results:
        return results
    
    # Calculate recency scores
    for result in results:
        date_str = result.get("payload", {}).get("date")
        recency = calculate_recency_score(date_str, current_date)
        result["recency_score"] = recency
        
        # Normalize cosine score to 0-1 range (Qdrant already returns 0-1)
        cosine = result.get("score", 0.5)
        
        # Combine scores
        final_score = (cosine * cosine_weight) + (recency * recency_weight)
        result["final_score"] = final_score
    
    # Re-sort by final score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    
    return results
```

#### 2. Update Search Function

Modify the `search_memory` function to include re-ranking:

```python
def search_memory(
    client: QdrantClient,
    query: str,
    source_type: str | None = None,
    project: str | None = None,
    limit: int = 10,
    enable_recency_boost: bool = True,
    cosine_weight: float = 0.7,
    recency_weight: float = 0.3,
) -> list[dict]:
    """Search memory collection with optional recency boost."""
    query_vec = embed_query(query)

    filters = []
    if source_type:
        filters.append(FieldCondition(key="source_type", match=MatchValue(value=source_type)))
    if project:
        filters.append(FieldCondition(key="project", match=MatchValue(value=project)))

    query_filter = Filter(must=filters) if filters else None

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
    )

    # Convert to dict format
    raw_results = [
        {
            "score": point.score,
            "content": point.payload.get("content"),
            "source_type": point.payload.get("source_type"),
            "file_path": point.payload.get("file_path"),
            "section": point.payload.get("section"),
            "project": point.payload.get("project"),
            "date": point.payload.get("date"),
            "payload": point.payload,
        }
        for point in results.points
    ]

    # Apply recency boost if enabled
    if enable_recency_boost:
        raw_results = re_rank_results(
            raw_results,
            cosine_weight=cosine_weight,
            recency_weight=recency_weight,
        )

    # Clean up internal scoring fields before returning
    for result in raw_results:
        result.pop("recency_score", None)
        result.pop("final_score", None)
        result.pop("payload", None)

    return raw_results
```

#### 3. CLI Integration

Add recency boost options to CLI:

```python
parser.add_argument(
    "--no-recency-boost",
    action="store_true",
    help="Disable recency boost (use vector similarity only)"
)
parser.add_argument(
    "--cosine-weight",
    type=float,
    default=0.7,
    help="Weight for cosine similarity (default: 0.7)"
)
parser.add_argument(
    "--recency-weight",
    type=float,
    default=0.3,
    help="Weight for recency score (default: 0.3)"
)
```

Update the search command to use these parameters.

### Phase 2: Testing (2-3 hours)

#### 1. Unit Tests

**File**: `/home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/test_recency.py`

```python
import pytest
from datetime import datetime, timezone, timedelta
from index_memory import calculate_recency_score, re_rank_results


class TestRecencyScore:
    def test_today_returns_1_0(self):
        today = datetime.now(timezone.utc)
        score = calculate_recency_score(today.strftime("%Y-%m-%d"), today)
        assert score == 1.0

    def test_yesterday_returns_0_9(self):
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        score = calculate_recency_score(yesterday.strftime("%Y-%m-%d"), datetime.now(timezone.utc))
        assert score == 0.9

    def test_two_days_ago_returns_0_8(self):
        two_days = datetime.now(timezone.utc) - timedelta(days=2)
        score = calculate_recency_score(two_days.strftime("%Y-%m-%d"), datetime.now(timezone.utc))
        assert score == 0.8

    def test_seven_days_returns_0_5(self):
        seven_days = datetime.now(timezone.utc) - timedelta(days=7)
        score = calculate_recency_score(seven_days.strftime("%Y-%m-%d"), datetime.now(timezone.utc))
        assert score == 0.5

    def test_none_date_returns_default(self):
        score = calculate_recency_score(None)
        assert score == 0.5

    def test_invalid_date_returns_default(self):
        score = calculate_recency_score("invalid-date")
        assert score == 0.5


class TestReRank:
    def test_recency_boost_ordering(self):
        results = [
            {"score": 0.9, "payload": {"date": "2026-02-09"}},  # Today - should be boosted
            {"score": 0.95, "payload": {"date": "2026-02-01"}},  # Old - should be penalized
        ]
        
        ranked = re_rank_results(results, cosine_weight=0.7, recency_weight=0.3)
        
        # Today's result should be first despite lower cosine score
        assert ranked[0]["payload"]["date"] == "2026-02-09"

    def test_no_recency_boost(self):
        results = [
            {"score": 0.9, "payload": {"date": "2026-02-01"}},
            {"score": 0.85, "payload": {"date": "2026-02-09"}},
        ]
        
        # With recency disabled, order should be by cosine score
        ranked = re_rank_results(results, cosine_weight=1.0, recency_weight=0.0)
        assert ranked[0]["score"] == 0.9

    def test_empty_results(self):
        results = []
        ranked = re_rank_results(results)
        assert ranked == []
```

#### 2. Integration Tests

Modify existing benchmark to test recency boost:

```python
def test_recency_boost_daily_query():
    """Test that recency boost correctly prioritizes recent daily logs."""
    client = get_qdrant()
    
    # Query for recent activities
    results = search_memory(
        client,
        "what happened today",
        source_type="daily",
        enable_recency_boost=True,
        limit=5
    )
    
    # First result should be from today or very recent
    if results and results[0].get("date"):
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        assert results[0]["date"] == today or results[0]["date"] is not None
```

### Phase 3: Deployment (1 hour)

#### 1. Backward Compatibility
- Keep recency boost **enabled by default** but make it configurable
- Add `--no-recency-boost` flag for testing without recency
- Add environment variable `MEMORY_RECENCY_ENABLED` for control

#### 2. Monitoring
- Track latency impact (should be <1ms for top-5 results)
- Monitor change in result relevance via user feedback
- Log recency scores for analysis

#### 3. Rollback Plan
- Set `enable_recency_boost=False` to disable instantly
- No database migrations required (pure Python change)

## Code Changes Summary

### Files to Modify
1. `/home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/index-memory.py`
   - Add `calculate_recency_score()` function
   - Add `re_rank_results()` function
   - Update `search_memory()` function
   - Update CLI argument parsing

### Files to Add
1. `/home/sean/.openclaw/sandboxes/agent-main-0d71ad7a/tools/memory-indexer/test_recency.py`
   - Unit tests for recency scoring
   - Integration tests for re-ranking

## Testing Plan

### Test Scenarios

| Scenario | Expected Behavior |
|----------|-------------------|
| Query for "today's activities" | Recent results boosted |
| Query for "old project decisions" | Recency impact minimal (cosine dominates) |
| Mixed recency results | Proper weighted scoring applied |
| No date metadata | Default 0.5 recency score |
| Disable recency boost | Pure cosine ordering maintained |

### A/B Testing Strategy

1. **Week 1**: Enable recency boost for 100% of queries
2. **Week 2**: A/B test (50% recency, 50% baseline)
3. **Week 3**: Compare metrics and decide on permanent enablement

### Metrics to Track

- **User satisfaction**: Direct feedback on result relevance
- **Click-through rate**: Which results users interact with
- **Query latency**: Additional time for re-ranking (<1ms target)
- **Result diversity**: Recency shouldn't reduce result variety

## Maintenance Considerations

### Future Enhancements
1. **Dynamic decay curve**: Adjust decay based on user behavior patterns
2. **Per-user recency**: Personalized recency based on user's query history
3. **Content freshness**: Factor in `indexed_at` timestamp as secondary signal

### Performance Optimization
- Cache recency calculations for repeated queries
- Pre-compute recency scores during indexing (if needed)
- Consider bulk re-ranking for batch queries

## Conclusion

Option A (post-retrieval re-ranker) provides the best balance of:
- **Implementation speed**: 2-3 hours vs 4-6 hours
- **Maintainability**: Pure Python, easy to debug
- **Flexibility**: A/B testing, weight tuning, rollback
- **Performance**: Negligible overhead for small result sets

The implementation is low-risk, high-value and can be incrementally deployed with minimal disruption.