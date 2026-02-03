# LOC-62: CI/CD Pipeline — Architecture

## Overview
Two GitHub Actions workflows: CI for pull requests, Release for tags and main branch.

## Workflow Design

### ci.yml — Continuous Integration
```
Trigger: pull_request (main)
Jobs:
  build-test:
    - Checkout code
    - Setup .NET 9
    - Restore dependencies (cached)
    - Build solution
    - Run tests with coverage
    - Upload test results
```

### release.yml — Release & Deploy
```
Trigger: push (main, tags/v*)
Jobs:
  docker:
    - Checkout code
    - Setup Docker Buildx
    - Login to GHCR
    - Build & push image
    - Tag: sha-short, latest (main), version (tags)
  
  release (tags only):
    - Create GitHub release
    - Auto-generate release notes
```

## Docker Image Strategy

### Tags
- `ghcr.io/lockn-ai/lockn-gen:latest` — Latest main build
- `ghcr.io/lockn-ai/lockn-gen:sha-abc1234` — Commit SHA
- `ghcr.io/lockn-ai/lockn-gen:v1.0.0` — Release version

### Caching
- GitHub Actions cache for NuGet packages
- Docker layer caching via actions/cache

## Security

### Permissions
- `contents: read` for checkout
- `packages: write` for GHCR push
- `pull-requests: write` for PR comments

### Secrets
- Uses `GITHUB_TOKEN` (automatic)
- No external secrets required

## File Structure
```
.github/
  workflows/
    ci.yml          # PR build/test
    release.yml     # Main/tag deployment
```

## Dependencies
- actions/checkout@v4
- actions/setup-dotnet@v4
- docker/setup-buildx-action@v3
- docker/login-action@v3
- docker/build-push-action@v5
- docker/metadata-action@v5
