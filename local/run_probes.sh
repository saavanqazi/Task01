#!/usr/bin/env bash
# Verifier fairness probes: replay tests/score.py in the task image against each probe workspace.
# Each local/probes/<name>/ holds the three deliverables. EXPECT file in the folder says 1.0 or 0.0.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TASK="${TASK:-$(cd "$HERE/.." && pwd)/task}"
docker build -q -t mic-audit-env "$TASK/environment" >/dev/null
for p in "$HERE"/probes/*/; do
  name=$(basename "$p"); expect=$(cat "$p/EXPECT" 2>/dev/null || echo "?")
  got=$(docker run --rm -e HARBOR_TASK_WORKSPACE=/work \
        -v "$TASK/tests:/tests:ro" -v "$p:/work:ro" mic-audit-env \
        python3 /tests/score.py | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['reward'], '|', ', '.join(d['core_failures']) or '-')")
  echo "$name  expect=$expect  got=$got"
done
