#!/usr/bin/env bash
# Phase 2 step 1: remove mined evaluation artefacts that must never ship.
set -euo pipefail
TASK="${TASK:-$(cd "$(dirname "$0")/.." && pwd)/task}"
for d in nop oracle; do
  if [ -d "$TASK/evaluations/$d" ]; then
    rm -rf "$TASK/evaluations/$d"; echo "removed evaluations/$d"
  fi
done
find "$TASK" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$TASK" -name '.DS_Store' -delete 2>/dev/null || true
echo "evaluations/ now contains:"; ls -1 "$TASK/evaluations" 2>/dev/null || echo "(empty)"
