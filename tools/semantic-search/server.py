#!/usr/bin/env python3
"""Semantic Code Search REST API for LockN repositories.

Endpoints:
  POST /search          - Search code with query, returns top-K results
  POST /index           - Trigger re-indexing (async)
  GET  /health          - Health check
  GET  /stats           - Collection stats
"""
import json
import subprocess
import sys
import threading
from pathlib import Path

import requests
from flask import Flask, jsonify, request
from qdrant_client import QdrantClient

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION = "lockn-code"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embeddings"
OLLAMA_MODEL = "qwen3-embedding"

app = Flask(__name__)
_index_lock = threading.Lock()
_indexing = False


def embed_query(query: str) -> list:
    r = requests.post(OLLAMA_EMBED_URL, json={"model": OLLAMA_MODEL, "prompt": query}, timeout=120)
    r.raise_for_status()
    data = r.json()
    emb = data.get("embedding")
    if not emb and isinstance(data.get("embeddings"), list) and data["embeddings"]:
        emb = data["embeddings"][0]
    if not emb:
        raise RuntimeError(f"No embedding returned: {list(data.keys())}")
    return emb


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/stats", methods=["GET"])
def stats():
    client = QdrantClient(url=QDRANT_URL, timeout=30)
    info = client.get_collection(COLLECTION)
    return jsonify({
        "collection": COLLECTION,
        "points_count": info.points_count,
        "indexed_vectors_count": info.indexed_vectors_count,
        "status": info.status.value if hasattr(info.status, 'value') else str(info.status),
    })


@app.route("/search", methods=["POST"])
def search():
    body = request.get_json(force=True)
    query = body.get("query", "").strip()
    if not query:
        return jsonify({"error": "query is required"}), 400

    limit = min(int(body.get("limit", 10)), 50)
    repo_filter = body.get("repo")  # optional filter by repo name
    language_filter = body.get("language")  # optional filter by language

    vector = embed_query(query)
    client = QdrantClient(url=QDRANT_URL, timeout=60)

    from qdrant_client.http import models
    must_conditions = []
    if repo_filter:
        must_conditions.append(models.FieldCondition(key="repo", match=models.MatchValue(value=repo_filter)))
    if language_filter:
        must_conditions.append(models.FieldCondition(key="language", match=models.MatchValue(value=language_filter)))

    search_filter = models.Filter(must=must_conditions) if must_conditions else None

    results_resp = client.query_points(
        collection_name=COLLECTION,
        query=vector,
        query_filter=search_filter,
        limit=limit,
        with_payload=True,
    )
    hits = results_resp.points if hasattr(results_resp, 'points') else results_resp

    results = []
    for hit in hits:
        p = hit.payload or {}
        results.append({
            "score": round(hit.score, 4),
            "repo": p.get("repo", ""),
            "file_path": p.get("file_path", ""),
            "start_line": p.get("start_line"),
            "end_line": p.get("end_line"),
            "language": p.get("language", ""),
            "content": p.get("content", ""),
        })

    return jsonify({"query": query, "count": len(results), "results": results})


@app.route("/index", methods=["POST"])
def trigger_index():
    global _indexing
    body = request.get_json(force=True) if request.data else {}
    full = body.get("full", False)

    if _indexing:
        return jsonify({"status": "already_running"}), 409

    def run_index():
        global _indexing
        with _index_lock:
            _indexing = True
            try:
                script = str(Path(__file__).parent / "index-repos.py")
                cmd = [sys.executable, script]
                if full:
                    cmd.append("--full")
                subprocess.run(cmd, check=True, timeout=3600)
            finally:
                _indexing = False

    threading.Thread(target=run_index, daemon=True).start()
    return jsonify({"status": "started", "full": full})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=False)
