#!/usr/bin/env bash
# Oracle run. Usage: local/run_oracle.sh <tag>   (tag e.g. r0, r1-after-h1)
set -euo pipefail
TASK="${TASK:-$(cd "$(dirname "$0")/.." && pwd)/task}"
TAG="${1:-r0}"
JOB="oracle-mic-audit-$TAG"
: "${OPENAI_API_KEY:?source glm.env first}"; : "${OPENAI_BASE_URL:?source glm.env first}"
harbor run -p "$TASK" -a oracle \
  --ve OPENAI_API_KEY="$OPENAI_API_KEY" --ve OPENAI_BASE_URL="$OPENAI_BASE_URL" \
  -o /tmp/harbor-jobs --job-name "$JOB" -n 1 -y
echo "=== oracle reward ($JOB) ==="
cat /tmp/harbor-jobs/"$JOB"/*/verifier/reward.txt
echo "(must be exactly 1.0; if not, read /tmp/harbor-jobs/$JOB/*/verifier/test-stdout.txt)"
