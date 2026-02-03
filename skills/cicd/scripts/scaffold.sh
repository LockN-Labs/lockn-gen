#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scaffold.sh [--type node|dotnet] [--branch <name>] [--image <ghcr-image>] [--workflow <file>] [--dry-run]

Generates a GitHub Actions CI workflow (Node or .NET) with Docker publish + optional service containers.
EOF
}

TYPE=""
DEFAULT_BRANCH=""
DOCKER_IMAGE=""
WORKFLOW_FILE="ci.yml"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      TYPE="$2"; shift 2;;
    --branch)
      DEFAULT_BRANCH="$2"; shift 2;;
    --image)
      DOCKER_IMAGE="$2"; shift 2;;
    --workflow)
      WORKFLOW_FILE="$2"; shift 2;;
    --dry-run)
      DRY_RUN="true"; shift 1;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown argument: $1" >&2
      usage; exit 1;;
  esac
 done

repo_slug=""
origin_url="$(git config --get remote.origin.url || true)"
if [[ -n "$origin_url" ]]; then
  if [[ "$origin_url" =~ github.com[:/]+([^/]+)/([^/.]+)(\.git)?$ ]]; then
    owner="${BASH_REMATCH[1]}"
    repo="${BASH_REMATCH[2]}"
    repo_slug="$owner/$repo"
  fi
fi

if [[ -z "$DEFAULT_BRANCH" ]]; then
  DEFAULT_BRANCH="$(git remote show origin 2>/dev/null | awk '/HEAD branch/ {print $NF}')"
fi
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

if [[ -z "$DOCKER_IMAGE" ]]; then
  if [[ -n "$repo_slug" ]]; then
    DOCKER_IMAGE="ghcr.io/${repo_slug,,}"
  else
    DOCKER_IMAGE="ghcr.io/owner/repo"
  fi
fi

if [[ -z "$TYPE" ]]; then
  if find . -maxdepth 2 -name "*.csproj" -o -name "*.fsproj" | grep -q .; then
    TYPE="dotnet"
  elif [[ -f package.json ]]; then
    TYPE="node"
  else
    echo "Unable to detect project type. Use --type node|dotnet." >&2
    exit 1
  fi
fi

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../assets/workflows"
case "$TYPE" in
  node) TEMPLATE="$TEMPLATE_DIR/node.yml.tmpl";;
  dotnet) TEMPLATE="$TEMPLATE_DIR/dotnet.yml.tmpl";;
  *)
    echo "Unknown type: $TYPE (expected node|dotnet)" >&2
    exit 1;;
 esac

NODE_VERSION="${NODE_VERSION:-20}"
DOTNET_VERSION="${DOTNET_VERSION:-8.0.x}"

SERVICES_BLOCK=""
if [[ -f docker-compose.yml ]]; then
  while IFS='|' read -r svc img; do
    [[ -z "$img" ]] && continue
    if [[ -z "$SERVICES_BLOCK" ]]; then
      SERVICES_BLOCK="    services:"
    fi
    SERVICES_BLOCK+=$'\n'"      ${svc}:"
    SERVICES_BLOCK+=$'\n'"        image: ${img}"
  done < <(
    awk '
      $1=="services:" {in=1; next}
      in && /^[^[:space:]]/ {in=0}
      in && match($0,/^[[:space:]]{2}([A-Za-z0-9._-]+):/,m){svc=m[1]}
      in && svc!="" && match($0,/^[[:space:]]{4}image:[[:space:]]*(.+)$/,m){
        gsub(/["\x27 ]/,"",m[1]); print svc "|" m[1]; svc=""
      }
    ' docker-compose.yml
  )
fi

export DOCKER_IMAGE DEFAULT_BRANCH NODE_VERSION DOTNET_VERSION

output_dir=".github/workflows"
output_path="$output_dir/$WORKFLOW_FILE"

if [[ "$DRY_RUN" == "false" ]]; then
  mkdir -p "$output_dir"
fi

rendered="$(mktemp)"

envsubst < "$TEMPLATE" > "$rendered"

awk -v block="$SERVICES_BLOCK" '
  $0=="__SERVICES__" { if (length(block) > 0) print block; next }
  { print }
' "$rendered" > "${rendered}.out"

if [[ "$DRY_RUN" == "true" ]]; then
  cat "${rendered}.out"
else
  mv "${rendered}.out" "$output_path"
  echo "Generated workflow: $output_path"
fi

rm -f "$rendered"

if [[ "$DRY_RUN" == "false" && -n "$repo_slug" && -f README.md ]]; then
  badge_url="https://github.com/${repo_slug}/actions/workflows/${WORKFLOW_FILE}/badge.svg"
  badge="[![CI](${badge_url})](https://github.com/${repo_slug}/actions/workflows/${WORKFLOW_FILE})"
  if ! grep -q "${badge_url}" README.md; then
    awk -v badge="$badge" '
      !added && /^# / { print; print ""; print badge; added=1; next }
      { print }
      END { if (!added) print badge }
    ' README.md > README.md.tmp && mv README.md.tmp README.md
    echo "Inserted README badge"
  fi
fi

if [[ -z "$repo_slug" ]]; then
  echo "Warning: could not determine GitHub repo slug. Badge and default image may need manual updates." >&2
fi
