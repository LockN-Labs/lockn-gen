#!/usr/bin/env python3
"""Search code via the semantic search server."""

import argparse
import json
import sys

import requests

SERVER_URL = "http://127.0.0.1:8899"


def search_code(query: str, limit: int = 10, repo: str = None, language: str = None):
    """Search code via REST API."""
    payload = {"query": query, "limit": limit}
    if repo:
        payload["repo"] = repo
    if language:
        payload["language"] = language

    resp = requests.post(f"{SERVER_URL}/search", json=payload)
    resp.raise_for_status()
    return resp.json()


def search_memory(query: str, limit: int = 10, source_type: str = None, project: str = None):
    """Search memory via REST API."""
    payload = {"query": query, "limit": limit}
    if source_type:
        payload["source_type"] = source_type
    if project:
        payload["project"] = project

    resp = requests.post(f"{SERVER_URL}/memory/search", json=payload)
    resp.raise_for_status()
    return resp.json()


def index_data(full: bool = False):
    """Trigger re-indexing."""
    resp = requests.post(f"{SERVER_URL}/index", json={"full": full})
    resp.raise_for_status()
    return resp.json()


def get_health():
    """Get server health."""
    resp = requests.get(f"{SERVER_URL}/health")
    resp.raise_for_status()
    return resp.json()


def get_stats():
    """Get collection statistics."""
    resp = requests.get(f"{SERVER_URL}/stats")
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search LockN codebase via semantic search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--repo", help="Filter by repo")
    parser.add_argument("--language", help="Filter by language")
    parser.add_argument("--memory", action="store_true", help="Search memory instead of code")
    parser.add_argument("--source-type", help="Memory source type filter")
    parser.add_argument("--project", help="Memory project filter")
    parser.add_argument("--index", action="store_true", help="Trigger re-indexing")
    parser.add_argument("--health", action="store_true", help="Show health")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    args = parser.parse_args()

    if args.health:
        print(json.dumps(get_health(), indent=2))
    elif args.stats:
        print(json.dumps(get_stats(), indent=2))
    elif args.index:
        print(json.dumps(index_data(full=True), indent=2))
    elif args.memory:
        result = search_memory(
            args.query,
            limit=args.limit,
            source_type=args.source_type,
            project=args.project
        )
        print(json.dumps(result, indent=2))
    else:
        result = search_code(
            args.query,
            limit=args.limit,
            repo=args.repo,
            language=args.language
        )
        print(json.dumps(result, indent=2))