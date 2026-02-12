#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embeddings"
OLLAMA_MODEL = "qwen3-embedding"
COLLECTION = "lockn-code"
VECTOR_SIZE = 4096

REPOS = [
    "/home/sean/.openclaw/workspace/lockn-logger",
    "/home/sean/.openclaw/workspace/lockn-speak",
    "/home/sean/.openclaw/workspace/lockn-listen",
    "/home/sean/.openclaw/workspace/lockn-ai-platform",
    "/home/sean/.openclaw/workspace/lockn-score",
    "/home/sean/.openclaw/workspace/lockn-gen",
    "/home/sean/.openclaw/workspace/lockn-infra",
    "/home/sean/.openclaw/workspace/lockn-apikeys",
]

INCLUDE_EXT = {".cs", ".ts", ".js", ".py", ".json", ".yaml", ".yml", ".md", ".sh", ".html", ".css"}
EXCLUDE_DIRS = {"node_modules", "bin", "obj", ".git", "dist", "build"}

BASE_DIR = Path(__file__).resolve().parent
STATE_DIR = BASE_DIR / "state"
STATE_FILE = STATE_DIR / "index-state.json"
TICKET_CACHE_FILE = STATE_DIR / "ticket-cache.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def is_boundary_line(line: str, ext: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if ext == ".py":
        return bool(re.match(r"^(def|class)\s+", s))
    if ext in {".js", ".ts"}:
        return bool(
            re.match(r"^(export\s+)?(async\s+)?function\s+", s)
            or re.match(r"^(export\s+)?class\s+", s)
            or re.match(r"^(const|let|var)\s+\w+\s*=\s*(async\s*)?\([^)]*\)\s*=>", s)
            or re.match(r"^\w+\s*\([^)]*\)\s*\{", s)
        )
    if ext == ".cs":
        return bool(
            re.match(r"^(public|private|internal|protected)\s+(static\s+)?(async\s+)?[\w<>,\[\]\.?]+\s+\w+\s*\(", s)
            or re.match(r"^(public|private|internal|protected)\s+(static\s+)?class\s+\w+", s)
            or re.match(r"^(class|interface|record|struct)\s+\w+", s)
        )
    if ext in {".java", ".go", ".rb"}:
        return bool(re.match(r"^(func|def|class)\s+", s))
    if ext in {".json", ".yaml", ".yml", ".md", ".sh", ".html", ".css"}:
        return bool(re.match(r"^(#|##|###|\{|\[|<\w|\w+\s*\{)", s))
    return False


def chunk_lines(lines: List[str], ext: str, target: int = 150, overlap: int = 20) -> List[Tuple[int, int, str]]:
    n = len(lines)
    if n == 0:
        return []

    boundaries = [i for i, l in enumerate(lines, start=1) if is_boundary_line(l, ext)]
    chunks = []
    start = 1

    while start <= n:
        end = min(start + target - 1, n)
        nearby = [b for b in boundaries if start + 50 <= b <= end + 80]
        if nearby:
            end = min(nearby[-1] - 1 if nearby[-1] > start else end, n)
            if end < start:
                end = min(start + target - 1, n)

        content = "".join(lines[start - 1:end])
        chunks.append((start, end, content))

        if end >= n:
            break
        start = max(end - overlap + 1, start + 1)

    return chunks


class Embedder:
    def __init__(self, workers: int = 6, timeout: int = 300):
        self.workers = workers
        self.timeout = timeout
        self.local = threading.local()

    def _session(self):
        if not hasattr(self.local, "session"):
            s = requests.Session()
            adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32)
            s.mount("http://", adapter)
            self.local.session = s
        return self.local.session

    def embed_one(self, text: str, retries: int = 6):
        session = self._session()
        payload = {"model": OLLAMA_MODEL, "prompt": text}
        delay = 1.0
        last_error = None
        for attempt in range(retries):
            try:
                r = session.post(OLLAMA_EMBED_URL, json=payload, timeout=self.timeout)
                if r.status_code in (429, 500, 502, 503, 504):
                    last_error = f"HTTP {r.status_code}: {r.text[:200]}"
                    print(f"    Retry {attempt+1}/{retries}: {last_error}", flush=True)
                    time.sleep(delay)
                    delay = min(delay * 2, 16)
                    continue
                r.raise_for_status()
                data = r.json()
                emb = data.get("embedding")
                if emb is None and isinstance(data.get("embeddings"), list) and data.get("embeddings"):
                    emb = data["embeddings"][0]
                if not isinstance(emb, list) or len(emb) == 0:
                    raise RuntimeError(f"No embedding in response: {list(data.keys())}")
                return emb
            except Exception as e:
                last_error = str(e)
                if attempt == retries - 1:
                    raise
                print(f"    Retry {attempt+1}/{retries}: {last_error}", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 16)
        raise RuntimeError(f"Failed after {retries} retries: {last_error}")

    def embed_many(self, texts: List[str]) -> List[List[float]]:
        out = [None] * len(texts)
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = {ex.submit(self.embed_one, t): i for i, t in enumerate(texts)}
            for fut in as_completed(futs):
                idx = futs[fut]
                try:
                    result = fut.result()
                    if result is None:
                        raise RuntimeError(f"embed_one returned None for chunk {idx}")
                    out[idx] = result
                except Exception as e:
                    print(f"  ERROR embedding chunk {idx}: {e}")
                    raise
        return out


def ensure_collection(client: QdrantClient):
    exists = client.collection_exists(COLLECTION)
    if not exists:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )


def load_state() -> Dict:
    if not STATE_FILE.exists():
        return {"version": 1, "files": {}}
    return json.loads(STATE_FILE.read_text())


def save_state(state: Dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def list_code_files(repo_path: Path) -> List[Path]:
    files = []
    for root, dirs, fnames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        root_p = Path(root)
        for f in fnames:
            p = root_p / f
            if p.suffix.lower() in INCLUDE_EXT:
                files.append(p)
    return files


def delete_existing_file_chunks(client: QdrantClient, repo: str, rel_path: str):
    client.delete(
        collection_name=COLLECTION,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(key="repo", match=models.MatchValue(value=repo)),
                    models.FieldCondition(key="file_path", match=models.MatchValue(value=rel_path)),
                ]
            )
        ),
        wait=True,
    )


def enrich_with_ticket_refs(text: str, ticket_titles: Dict[str, str]) -> Tuple[str, list]:
    """Enrich text with ticket references and return ticket refs found."""
    TICKET_PATTERN = re.compile(r'\b(LOC-\d+)\b', re.IGNORECASE)
    
    ticket_refs = []
    
    def replace_ticket(match):
        ticket_id = match.group(1).upper()
        if ticket_id not in ticket_refs:
            ticket_refs.append(ticket_id)
        
        title = ticket_titles.get(ticket_id)
        if title:
            return f"{ticket_id} ({title})"
        return ticket_id
    
    enriched_text = TICKET_PATTERN.sub(replace_ticket, text)
    return enriched_text, ticket_refs


def load_ticket_cache() -> Dict[str, str]:
    """Load ticket titles from cache file."""
    if not TICKET_CACHE_FILE.exists():
        return {}
    try:
        cache = json.loads(TICKET_CACHE_FILE.read_text())
        return cache.get("tickets", {})
    except Exception:
        return {}


def index_repos(full_reindex: bool = False, workers: int = 6, batch_size: int = 64):
    started = time.time()
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    ensure_collection(client)
    state = load_state()
    old_files = state.get("files", {})
    new_state_files = {}

    embedder = Embedder(workers=workers)
    
    # Load ticket cache for enrichment
    ticket_titles = load_ticket_cache()
    if ticket_titles:
        print(f"Loaded {len(ticket_titles)} ticket titles from cache")

    total_files_indexed = 0
    total_chunks = 0
    total_vectors = 0

    for repo_dir in REPOS:
        repo_path = Path(repo_dir)
        repo = repo_path.name
        print(f"\n== Repo: {repo} ==")
        files = list_code_files(repo_path)

        to_process = []
        seen_keys = set()

        for f in files:
            rel = str(f.relative_to(repo_path))
            key = f"{repo}/{rel}"
            seen_keys.add(key)
            h = sha256_file(f)
            new_state_files[key] = {"sha256": h, "updated_at": int(time.time())}
            if full_reindex or old_files.get(key, {}).get("sha256") != h:
                to_process.append((f, rel, h))

        removed = [k for k in old_files.keys() if k.startswith(f"{repo}/") and k not in seen_keys]
        for k in removed:
            rel = k.split("/", 1)[1]
            delete_existing_file_chunks(client, repo, rel)

        print(f"Files scanned: {len(files)} | changed/new: {len(to_process)} | removed: {len(removed)}")

        records = []
        for file_path, rel_path, _ in to_process:
            delete_existing_file_chunks(client, repo, rel_path)
            text = safe_read_text(file_path)
            lines = text.splitlines(keepends=True)
            ext = file_path.suffix.lower()
            chunks = chunk_lines(lines, ext)

            for start_line, end_line, content in chunks:
                if not content.strip():
                    continue
                # Truncate to ~8000 chars to stay within embedding model context
                if len(content) > 8000:
                    content = content[:8000]
                
                # Enrich with ticket references
                enriched_content, ticket_refs = enrich_with_ticket_refs(content, ticket_titles)
                
                payload = {
                    "repo": repo,
                    "file_path": rel_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "language": ext.lstrip("."),
                    "content": enriched_content,
                    "ticket_refs": ticket_refs if ticket_refs else None,
                }
                records.append(payload)

            total_files_indexed += 1

        print(f"Chunks to embed in {repo}: {len(records)}")
        total_chunks += len(records)

        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            texts = [r["content"] for r in batch]
            print(f"  Embedding batch {i // batch_size + 1} ({len(batch)} chunks)...", flush=True)
            vectors = embedder.embed_many(texts)

            points = []
            for rec, vec in zip(batch, vectors):
                if len(vec) != VECTOR_SIZE:
                    raise RuntimeError(f"Embedding size mismatch: expected {VECTOR_SIZE}, got {len(vec)}")
                points.append(
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vec,
                        payload=rec,
                    )
                )

            client.upsert(collection_name=COLLECTION, points=points, wait=True)
            total_vectors += len(points)
            print(f"  Upserted batch {i // batch_size + 1} ({len(points)} vectors)")

    state["files"] = new_state_files
    state["last_run"] = int(time.time())
    save_state(state)

    elapsed = time.time() - started
    print("\n=== INDEX COMPLETE ===")
    print(f"Files indexed: {total_files_indexed}")
    print(f"Chunks created: {total_chunks}")
    print(f"Vectors upserted: {total_vectors}")
    print(f"Time taken: {elapsed:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index LockN repos into Qdrant for semantic code search")
    parser.add_argument("--full", action="store_true", help="Force reindex of all files")
    parser.add_argument("--workers", type=int, default=6, help="Embedding worker threads (4-8 recommended)")
    parser.add_argument("--batch-size", type=int, default=64, help="Upsert batch size")
    args = parser.parse_args()

    index_repos(full_reindex=args.full, workers=max(1, min(args.workers, 16)), batch_size=max(1, args.batch_size))