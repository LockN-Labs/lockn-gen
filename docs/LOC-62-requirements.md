# LOC-62: CI/CD Pipeline — Requirements

## Overview
GitHub Actions CI/CD workflows for LockN Gen with automated build, test, and deployment to GHCR.

## Functional Requirements

### FR-1: PR Build & Test Workflow
- Trigger on pull request to main
- Build .NET 9 solution
- Run unit tests
- Report test results in PR check
- Fail on any build error or test failure

### FR-2: Docker Image Build
- Multi-stage Dockerfile (already exists)
- Build on main branch push
- Tag with commit SHA and "latest"
- Cache Docker layers for faster builds

### FR-3: GHCR Push
- Authenticate with GITHUB_TOKEN
- Push to ghcr.io/lockn-ai/lockn-gen
- Clean up old images (keep last 5 versions)

### FR-4: Release Workflow
- Trigger on tag push (v*)
- Build and tag with version
- Create GitHub release with changelog
- Generate release notes from commits

## Non-Functional Requirements

### NFR-1: Build Performance
- Full CI run < 5 minutes
- Docker cache hit rate > 80%

### NFR-2: Security
- No secrets in workflow logs
- Minimal required permissions
- Dependabot for action updates

## Files to Create/Modify
- `.github/workflows/ci.yml` — PR build/test
- `.github/workflows/release.yml` — Tag release + GHCR push
- `Dockerfile` — Verify multi-stage is optimal

## Out of Scope
- Kubernetes deployment manifests
- Production environment setup
- Secret rotation automation

## Acceptance Criteria
- [ ] PR triggers build + test workflow
- [ ] Main branch push builds and pushes Docker image
- [ ] Tagged releases create GitHub releases
- [ ] All secrets handled securely
