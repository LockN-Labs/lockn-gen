#!/usr/bin/env bash
set -euo pipefail

LINEAR_API_URL="https://api.linear.app/graphql"
TEAM_ID_DEFAULT="f37ff2bb-141f-421a-9401-fb0008bfb67f"

require_env() {
  if [[ -z "${LINEAR_API_KEY:-}" ]]; then
    echo "LINEAR_API_KEY is not set" >&2
    exit 1
  fi
}

linear_gql() {
  local query="$1"
  require_env
  curl -sS "$LINEAR_API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: ${LINEAR_API_KEY}" \
    -d "{\"query\":$(jq -Rs . <<<"$query")}"
}

create_issue() {
  local title="$1"
  local description="$2"
  local priority="${3:-2}"
  local team_id="${4:-$TEAM_ID_DEFAULT}"
  local parent_id="${5:-}"

  local parent_fragment=""
  if [[ -n "$parent_id" ]]; then
    parent_fragment=", parentId: \"$parent_id\""
  fi

  local q
  q=$(cat <<EOF
mutation {
  issueCreate(input: { teamId: "$team_id", title: "$title", description: "$description", priority: $priority${parent_fragment} }) {
    issue { id identifier url }
  }
}
EOF
)
  linear_gql "$q"
}

list_issues() {
  local team_id="${1:-$TEAM_ID_DEFAULT}"
  local q
  q=$(cat <<EOF
{
  team(id: "$team_id") {
    issues(first: 20, filter: { state: { name: { in: ["Todo", "In Progress"] } } }) {
      nodes { id identifier title state { name } priority }
    }
  }
}
EOF
)
  linear_gql "$q"
}

update_issue_state() {
  local issue_id="$1"
  local state_id="$2"

  local q
  q=$(cat <<EOF
mutation {
  issueUpdate(id: "$issue_id", input: { stateId: "$state_id" }) {
    issue { id state { name } }
  }
}
EOF
)
  linear_gql "$q"
}

get_issue_by_identifier() {
  local identifier="$1"
  local q
  q=$(cat <<EOF
{
  issue(identifier: "$identifier") {
    id
    identifier
    title
    description
    state { name }
    url
  }
}
EOF
)
  linear_gql "$q"
}

usage() {
  cat <<EOF
Usage: linear-api.sh <command> [args]

Commands:
  create-issue <title> <description> [priority] [team_id] [parent_id]
  list-issues [team_id]
  update-issue-state <issue_id> <state_id>
  get-issue <identifier>

GraphQL examples:
  mutation { issueCreate(input: { teamId: "...", title: "...", description: "...", priority: 2 }) { issue { id identifier url } } }
  { team(id: "...") { issues(first: 20, filter: { state: { name: { in: ["Todo", "In Progress"] } } }) { nodes { id identifier title state { name } priority } } } }
  mutation { issueUpdate(id: "...", input: { stateId: "..." }) { issue { id state { name } } } }
EOF
}

main() {
  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    create-issue)
      create_issue "$@" ;;
    list-issues)
      list_issues "$@" ;;
    update-issue-state)
      update_issue_state "$@" ;;
    get-issue)
      get_issue_by_identifier "$@" ;;
    -h|--help|help|"")
      usage ;;
    *)
      echo "Unknown command: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
