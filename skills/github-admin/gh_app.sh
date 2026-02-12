#!/bin/bash
# GitHub App authentication helpers for LockN agents

KEYS_DIR="/home/sean/keys"
SKILL_DIR="$(dirname "${BASH_SOURCE[0]}")"

# App IDs
declare -A APP_IDS=(
    [coder]=2816646
    [qa]=2816677
    [architect]=2816706
    [devops]=2816768
    [orchestrator]=2816797
)

# Get JWT for an app
gh_app_jwt() {
    local app_name="${1:-orchestrator}"
    local app_id="${APP_IDS[$app_name]}"
    local key_file="$KEYS_DIR/lockn-${app_name}.2026-02-07.private-key.pem"
    
    if [[ ! -f "$key_file" ]]; then
        echo "Error: Key file not found: $key_file" >&2
        return 1
    fi
    
    python3 "$SKILL_DIR/gh_admin.py" jwt "$app_id" "$key_file"
}

# Get installation token for an app
gh_app_token() {
    local app_name="${1:-orchestrator}"
    local org="${2:-LockN-Labs}"
    local app_id="${APP_IDS[$app_name]}"
    local key_file="$KEYS_DIR/lockn-${app_name}.2026-02-07.private-key.pem"
    
    python3 "$SKILL_DIR/gh_admin.py" token "$app_id" "$key_file" "$org"
}

# List installations for an app
gh_app_installations() {
    local app_name="${1:-orchestrator}"
    local app_id="${APP_IDS[$app_name]}"
    local key_file="$KEYS_DIR/lockn-${app_name}.2026-02-07.private-key.pem"
    
    python3 "$SKILL_DIR/gh_admin.py" installations "$app_id" "$key_file"
}

# Open installation URL in browser
gh_app_install() {
    local app_name="${1:-orchestrator}"
    echo "Open this URL to install $app_name:"
    echo "https://github.com/apps/lockn-${app_name}/installations/select_target"
}

# Post a status check
gh_app_status() {
    local app_name="$1"
    local repo="$2"
    local sha="$3"
    local state="$4"  # success, failure, pending
    local description="$5"
    local context="${6:-LockN $app_name}"
    
    local token=$(gh_app_token "$app_name")
    
    curl -s -X POST "https://api.github.com/repos/$repo/statuses/$sha" \
        -H "Authorization: token $token" \
        -H "Accept: application/vnd.github+json" \
        -d "{\"state\":\"$state\",\"description\":\"$description\",\"context\":\"$context\"}"
}

# Export functions
export -f gh_app_jwt gh_app_token gh_app_installations gh_app_install gh_app_status
