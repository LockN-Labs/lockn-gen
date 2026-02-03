---
name: cicd
description: Generate GitHub Actions CI/CD workflows and branch protection for Node or .NET repos, including Docker publish to GHCR, docker-compose service containers, and README CI badge insertion.
---

# CI/CD Scaffold

## Quick start

1. Generate a workflow:

```bash
./skills/cicd/scripts/scaffold.sh
```

2. (Optional) Override defaults:

```bash
./skills/cicd/scripts/scaffold.sh --type node --branch main --workflow ci.yml --image ghcr.io/org/repo
```

3. (Optional) Apply branch protection (requires `gh` auth):

```bash
./skills/cicd/scripts/branch-protection.sh --branch main --checks "CI"
```

## What scaffold.sh does

- Detects project type (Node if `package.json`, .NET if `*.csproj`/`*.fsproj`).
- Generates `.github/workflows/<workflow>` from templates in `assets/workflows/`.
- Adds GHCR Docker build/publish steps.
- If `docker-compose.yml` exists, injects service containers (image-only services).
- Inserts a GitHub Actions badge into `README.md` when the repo slug is discoverable.

### Defaults and overrides

- `--type node|dotnet` to override detection.
- `--branch <name>` for the default branch (auto-detected via git if omitted).
- `--image <ghcr-image>` for Docker image (defaults to `ghcr.io/<owner>/<repo>` when possible).
- `NODE_VERSION` env var defaults to `20` for Node template.
- `DOTNET_VERSION` env var defaults to `8.0.x` for .NET template.

## Resources

- `scripts/scaffold.sh` — generator script.
- `scripts/branch-protection.sh` — GitHub branch protection helper.
- `assets/workflows/node.yml.tmpl` — Node CI/CD workflow template.
- `assets/workflows/dotnet.yml.tmpl` — .NET CI/CD workflow template.
