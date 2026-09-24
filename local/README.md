# Local run kit (Windows cmd)

Layout on your machine:

```
C:\Users\amitb\Task01\            <- this repo clone
├── glm.env                       <- OPENAI_API_KEY / OPENAI_BASE_URL / JUDGE_MODEL (git-ignored, never commit)
├── task\                         <- the unzipped task folder (rename the long inner folder to task)
├── jobs\                         <- harbor output (git-ignored)
└── local\                        <- kit.py, probes\, glm-harbor-config.json
```

All commands run from `C:\Users\amitb\Task01` in cmd. `--env-file glm.env` hands the key and proxy to
harbor for every run, so nothing needs sourcing.

## Phase 2 — clean, oracle, fairness probes

```bat
python local\kit.py clean
harbor run -p task -a oracle -k 1 -n 1 --env-file glm.env -o jobs --job-name oracle-r0 -y
type jobs\oracle-r0\*\verifier\reward.txt
```
Must print `1.0`. Run it a second time (`--job-name oracle-r0b`) — the gate wants it to hold on repeat.
If it is below 1.0 read `jobs\oracle-r0\<trial>\verifier\test-stdout.txt` for the failing assertion.

```bat
python local\kit.py probes
```
Builds the task image and replays `tests\score.py` against each folder in `local\probes\`.
`p01..p06` must show `1.0`, `n01..n03` must show `0.0`. A line starting with `!!` is a verifier problem.

## Phase 3 — the 4-run GLM-5.2 battery

```bat
docker ps --format "{{.Names}}"
harbor run -c local\glm-harbor-config.json -n 2 -k 4 --env-file glm.env -y
python local\kit.py rewards jobs\glm-mic-audit-r0
```
`-k 4` is the total attempts, `-n 2` how many run at once. Edit `job_name` in the config for each round
(`glm-mic-audit-r1`, ...). If your harbor prefers flags over a config file, the equivalent is:

```bat
harbor run -p task -a opencode -m openai/glm-5.2 -k 4 -n 2 --env-file glm.env -o jobs --job-name glm-mic-audit-r0 -y
```

Read whole `checks[]` entries in `jobs\<job>\<trial>\verifier\score.json`; do not grep for "passed".

## Phase 5 — package the final battery

```bat
python local\kit.py package jobs\glm-mic-audit-r2
```
Copies the four trials unflattened into `task\evaluations\difficulty\r1..r4`, normalises each
`result.json` (`"model": "GLM-5.2"`, `overall_pass`, `final_answer`, `reward`, judge provenance) and
copies the first 1.0 run into `solvability\r1`. Never an oracle run.

Then zip **only** the task folder (right-click `task` → Send to → Compressed folder, or
`tar -a -cf mic-audit-v1.zip task`).

`glm-harbor-config.json` — compare its field names with the team's template before the first battery;
only `tasks[0].path` and `job_name` are meant to change per task.
