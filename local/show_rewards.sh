#!/usr/bin/env bash
# Print reward + failed checks per trial. Usage: local/show_rewards.sh /tmp/harbor-jobs/<job>
set -euo pipefail
JOBDIR="${1:?job dir}"
for t in "$JOBDIR"/*/; do
  [ -f "$t/verifier/reward.txt" ] || continue
  r=$(cat "$t/verifier/reward.txt")
  crash=""; [ -f "$t/exception.txt" ] && crash=" CRASH(exception.txt)"
  [ -f "$t/agent/trajectory.json" ] || crash="$crash NO-TRAJECTORY"
  fails=$(python3 -c "
import json,sys
try:
    s=json.load(open('$t/verifier/score.json'))
    print(', '.join(c['name'] for c in s['checks'] if not c['passed']) or '-')
except Exception as e: print('score.json unreadable')
")
  echo "$(basename "$t")  reward=$r$crash  failed: $fails"
done
