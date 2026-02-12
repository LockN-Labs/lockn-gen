#!/bin/bash
# LockN Score Integration Check
echo "=== LockN Score Integration Status ==="
echo ""

echo "📁 Workspace structure:"
find lockn-score -type f -name "*.py" 2>/dev/null | head -20

echo ""
echo "📁 Repo structure:"
find ~/repos/lockn-score -type f \( -name "*.py" -o -name "*.tsx" -o -name "*.ts" \) 2>/dev/null | head -30

echo ""
echo "📦 Dependencies check:"
if [ -f lockn-score/requirements.txt ]; then
    echo "workspace requirements.txt:"
    cat lockn-score/requirements.txt
fi
if [ -f ~/repos/lockn-score/requirements.txt ]; then
    echo ""
    echo "repo requirements.txt:"
    cat ~/repos/lockn-score/requirements.txt
fi

echo ""
echo "🔗 Missing imports check:"
grep -r "^from\|^import" lockn-score/**/*.py 2>/dev/null | grep -v "__pycache__" | sort -u | head -20
