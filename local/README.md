# Local run kit (your machine, WSL2 / Git Bash)

Layout this expects on your machine:

```
C:\Users\amitb\Task01\            <- this repo clone
├── glm.env                       <- your key file (git-ignored, never commit)
├── task\                         <- the unzipped task folder (rename the long folder to task/)
└── local\                        <- these helpers
```

Every session, from a bash shell (WSL2 or Git Bash) in the repo root:

```bash
set -a; source glm.env; set +a     # exports OPENAI_API_KEY, OPENAI_BASE_URL, JUDGE_MODEL
export TASK="$PWD/task"
docker ps --format '{{.Names}}'    # budget check before every battery
```

`set -a` makes `source` export the variables so harbor and docker see them.
If you use PowerShell instead, run the commands inside `wsl` or Git Bash — the scripts here are bash.

## Scripts

| Script | Phase | What it does |
|---|---|---|
| `clean_mined_evaluations.sh` | 2 | Deletes `task/evaluations/nop` and `task/evaluations/oracle` (mined artefacts that must not ship). |
| `run_oracle.sh <tag>` | 2, 4, 5 | Runs `harbor run -a oracle` on `$TASK` and prints the reward. Must print `1.0`. |
| `run_probes.sh` | 2, 4 | Replays `tests/score.py` inside the task image against each folder in `local/probes/` (correct paraphrases must score 1.0, wrong ones 0.0). |
| `run_battery.sh <job_name> [n_concurrent]` | 3, 4 | Runs the 4-attempt GLM-5.2 battery from `glm-harbor-config.json` and prints the four rewards. |
| `show_rewards.sh <job_dir>` | 3, 4 | Prints per-trial reward and the names of failed checks from `score.json`. |
| `normalize_results.py <trial_dir>...` | 5 | Adds `model`, `overall_pass`, `final_answer`, `reward`, judge provenance to each rollout `result.json`. |
| `package_evaluations.sh <job_dir>` | 5 | Copies the four trials into `task/evaluations/difficulty/r1..r4`, picks a 1.0 run for `solvability/r1`, strips job-level files. |

`glm-harbor-config.json` is the battery config. Check its field names against the team's own
template before the first run — only `tasks[0].path` and `job_name` are meant to change per task.
