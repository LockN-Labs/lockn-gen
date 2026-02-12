#!/usr/bin/env python3
"""
Ticket cache manager for semantic search indexing.
Maintains a local cache of Linear ticket titles for enrichment.
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Dict, Optional

import requests

LINEAR_API_URL = "https://api.linear.app/graphql"
LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
CACHE_FILE = Path(__file__).resolve().parent / "state" / "ticket-cache.json"

# Regex pattern for LOC-XXX ticket references
TICKET_PATTERN = re.compile(r'\b(LOC-\d+)\b', re.IGNORECASE)


def load_cache() -> Dict[str, Dict]:
    """Load ticket cache from file."""
    if not CACHE_FILE.exists():
        return {"version": 1, "tickets": {}, "last_updated": 0}
    return json.loads(CACHE_FILE.read_text())


def save_cache(cache: Dict):
    """Save ticket cache to file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def fetch_ticket_titles(limit: int = 100) -> Dict[str, str]:
    """Fetch ticket titles from Linear API."""
    if not LINEAR_API_KEY:
        print("⚠️  LINEAR_API_KEY not set. Skipping ticket fetch.")
        return {}
    
    tickets = {}
    after = None
    page = 0
    
    while page < 5:  # Max 5 pages
        query = """
        query Issues($first: Int, $after: String) {
            issues(first: $first, after: $after) {
                pageInfo { hasNextPage, endCursor }
                nodes { id, identifier, title }
            }
        }
        """
        
        variables = {"first": limit}
        if after:
            variables["after"] = after
            
        headers = {"Authorization": LINEAR_API_KEY}
        
        try:
            response = requests.post(
                LINEAR_API_URL,
                json={"query": query, "variables": variables},
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            issues = data.get("data", {}).get("issues", {})
            nodes = issues.get("nodes", [])
            
            for node in nodes:
                identifier = node.get("identifier", "")
                title = node.get("title", "")
                if identifier and title:
                    tickets[identifier] = title
            
            page_info = issues.get("pageInfo", {})
            if not page_info.get("hasNextPage", False):
                break
                
            after = page_info.get("endCursor")
            page += 1
            
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            break
    
    return tickets


def update_cache() -> Dict[str, str]:
    """Update ticket cache from Linear API."""
    print("Updating ticket cache from Linear API...")
    tickets = fetch_ticket_titles()
    
    cache = load_cache()
    cache["tickets"] = tickets
    cache["last_updated"] = int(time.time())
    save_cache(cache)
    
    print(f"✓ Updated {len(tickets)} tickets")
    return tickets


def get_ticket_title(ticket_id: str) -> Optional[str]:
    """Get ticket title from cache."""
    cache = load_cache()
    return cache["tickets"].get(ticket_id.upper())


def enrich_text(text: str, append_title: bool = True) -> str:
    """Enrich text with ticket references."""
    def replace_ticket(match):
        ticket_id = match.group(1).upper()
        title = get_ticket_title(ticket_id)
        
        if title and append_title:
            return f"{ticket_id} ({title})"
        return ticket_id
    
    return TICKET_PATTERN.sub(replace_ticket, text)


def find_ticket_refs(text: str) -> list:
    """Find all ticket references in text."""
    return TICKET_PATTERN.findall(text)


def is_ticket_reference(text: str) -> bool:
    """Check if text contains ticket references."""
    return bool(TICKET_PATTERN.search(text))


if __name__ == "__main__":
    # Update cache
    tickets = update_cache()
    
    # Test enrichment
    test_text = "See LOC-325 for WebSocket details and LOC-339 for chunk enrichment."
    enriched = enrich_text(test_text)
    print(f"\nOriginal:  {test_text}")
    print(f"Enriched:  {enriched}")
    
    # Find refs
    refs = find_ticket_refs(test_text)
    print(f"References: {refs}")