#!/bin/bash
# Incremental re-index of LockN repos into Qdrant
# Add to crontab: */30 * * * * /home/sean/.openclaw/workspace/tools/semantic-search/reindex-cron.sh >> /tmp/semantic-search-reindex.log 2>&1
set -euo pipefail
cd "$(dirname "$0")"
LOCKFILE="/tmp/semantic-search-reindex.lock"

# Skip if already running
if [ -f "$LOCKFILE" ]; then
    pid=$(cat "$LOCKFILE" 2>/dev/null || true)
    if kill -0 "$pid" 2>/dev/null; then
        echo "$(date): Skipping, already running (pid $pid)"
        exit 0
    fi
fi

echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

echo "$(date): Starting incremental re-index"
python3 index-repos.py --workers 4
echo "$(date): Re-index complete"
