#!/usr/bin/env bash
# Phase 5: build task/evaluations/{difficulty,solvability} from a finished battery job dir.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TASK="${TASK:-$(cd "$HERE/.." && pwd)/task}"
JOBDIR="${1:?job dir, e.g. /tmp/harbor-jobs/glm-mic-audit-r2}"
EV="$TASK/evaluations"
rm -rf "$EV/difficulty" "$EV/solvability"; mkdir -p "$EV/difficulty" "$EV/solvability"
i=0; pass=""
for t in "$JOBDIR"/*/; do
  [ -f "$t/verifier/reward.txt" ] || continue
  i=$((i+1)); [ $i -le 4 ] || break
  cp -r "$t" "$EV/difficulty/r$i"
  rm -f "$EV/difficulty/r$i/lock.json" "$EV/difficulty/r$i/job.log"
  [ "$(cat "$t/verifier/reward.txt")" = "1.0" ] && [ -z "$pass" ] && pass="r$i"
done
python3 "$HERE/normalize_results.py" "$EV"/difficulty/r*
if [ -n "$pass" ]; then
  cp -r "$EV/difficulty/$pass" "$EV/solvability/r1"; echo "solvability/r1 <- difficulty/$pass"
else
  echo "WARNING: no 1.0 run in this battery — solvability needs a passing non-oracle run from elsewhere"
fi
# never ship job-level files or anything loose under evaluations/
rm -f "$JOBDIR"/config.json.tmp 2>/dev/null || true
echo "difficulty rewards:"; for r in "$EV"/difficulty/r*; do echo "  $(basename "$r") $(cat "$r/verifier/reward.txt")"; done
ls -1 "$EV"
