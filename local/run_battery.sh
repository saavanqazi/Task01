#!/usr/bin/env bash
# GLM-5.2 difficulty battery. Usage: local/run_battery.sh <job_name> [n_concurrent]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
JOB="${1:?job name, e.g. glm-mic-audit-r0}"
NCONC="${2:-2}"
: "${OPENAI_API_KEY:?source glm.env first}"
CFG="/tmp/$JOB.config.json"
python3 - "$HERE/glm-harbor-config.json" "$CFG" "$JOB" "$NCONC" <<'PY'
import json, sys
src, dst, job, n = sys.argv[1:]
c = json.load(open(src)); c["job_name"] = job; c["n_concurrent_trials"] = int(n)
json.dump(c, open(dst, "w"), indent=2)
PY
echo "running containers now: $(docker ps --format '{{.Names}}' | wc -l)"
harbor run -c "$CFG" -n "$NCONC" -k 4 -y
"$HERE/show_rewards.sh" "/tmp/harbor-jobs/$JOB"
