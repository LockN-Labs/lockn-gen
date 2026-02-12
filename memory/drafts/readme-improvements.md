# README Improvements Draft

## Target Repo: `lockn-code-search` (worst README: missing `README.md` entirely)

```markdown
# lockn-code-search

![CI](https://img.shields.io/badge/CI-not%20configured-lightgrey)

Semantic code search service for LockN repositories.

`lockn-code-search` indexes source code into Qdrant using embeddings from Ollama, then exposes both CLI and REST API search interfaces for agents and developers.

## Features

- Repository discovery for local `lockn-*` repos
- Language-aware chunking (Python, JS/TS, generic fallback)
- Embedding generation via Ollama (`qwen3-embedding`)
- Vector storage + filtering in Qdrant
- FastAPI endpoints for health, search, and indexing
- Incremental indexing support

## Architecture Overview

High-level components:

- **Discovery** (`discovery.py`): finds repos/files to index
- **Chunker** (`chunker.py`): breaks code into semantic chunks
- **Embeddings** (`embeddings.py`): calls Ollama `/api/embed`
- **Vector Store** (`qdrant_store.py`): creates collection, upserts/searches vectors
- **Indexer** (`indexer.py`): orchestrates end-to-end indexing
- **API** (`api.py`): REST endpoints for search and indexing control
- **CLI** (`cli.py`): commands for indexing/search/serving API

Runtime dependencies:

- **Ollama** (default `http://localhost:11434`)
- **Qdrant** (default `http://localhost:6333`)

For deeper design details, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Setup

### Prerequisites

- Python 3.11+
- Ollama running with embedding model available
- Qdrant running on port 6333 (or custom via env)

### Local install

```bash
cd /home/sean/repos/lockn-code-search
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configuration

Environment variables (optional):

- `OLLAMA_URL` (default: `http://localhost:11434`)
- `QDRANT_URL` (default: `http://localhost:6333`)
- `COLLECTION_NAME` (if configurable in `config.py`)

### Run with Docker Compose

```bash
docker compose up --build
```

This starts:

- `lockn-code-search` API on `http://localhost:8890`
- `qdrant` on `http://localhost:6333`

## Usage

### CLI

```bash
# Full index
lockn-search index

# Incremental index
lockn-search index --incremental

# Search
lockn-search search "how does auth token refresh work" --repo lockn-auth --limit 5

# Serve API
lockn-search serve --host 0.0.0.0 --port 8890
```

### REST API

Base URL: `http://localhost:8890`

#### Health

```bash
curl http://localhost:8890/health
```

#### Search

```bash
curl -X POST http://localhost:8890/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "where is audio transcription implemented",
    "repo": "lockn-listen",
    "language": "python",
    "limit": 5
  }'
```

#### Trigger indexing

```bash
curl -X POST http://localhost:8890/index \
  -H "Content-Type: application/json" \
  -d '{"repos": ["lockn-logger"], "incremental": true}'
```

#### Index status

```bash
curl http://localhost:8890/index/status
```

## API Docs

Interactive docs are available when the service is running:

- Swagger UI: `http://localhost:8890/docs`
- ReDoc: `http://localhost:8890/redoc`

Core endpoints:

- `GET /health`
- `POST /search`
- `POST /index`
- `GET /index/status`

## Testing

```bash
pytest -q
```

## CI

CI is currently not configured in this repository (`.github/workflows` not present at audit time).

Recommended next step:

1. Add GitHub Actions workflow for lint + tests
2. Replace placeholder badge with real workflow badge URL

## Contributing

1. Create feature branch
2. Add/adjust tests with changes
3. Run `pytest`
4. Open PR

## License

Add project license information here.
```
