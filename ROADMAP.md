# Roadmap — `tech-mg-it-b10-a5-mic-modelling-feature-matrix-audit`

Task under review: Rack chain (Racklane 4.3) vs Micaform 1.1 feature-matrix audit.
Package type: **non-connector, offline, file-deliverable** (`tests/verifier.json`, no `_app/` mirror, no MCP, no LLM judge).
Goal of this roadmap: take the mined bundle to a submittable ZIP that clears both gates (Oracle = 1.0, GLM-5.2 passes 1–3 of 4) with `review.csv`, `README.md` and `qc_report.html` at the root.

---

## 0. What the task actually asks (problem statement, decoded)

Rafa (studio owner) wants Theo's 11-row draft comparison checked **cell by cell** (11 features × 2 products = 22 cells) against three source documents, ranked by a house-rules file, and then wants four counts and a note to Maren.

| Input file | Role | Key facts inside |
|---|---|---|
| `draft_comparison.md` | The thing being audited. Never decides a cell. | 11 rows FT-1..FT-11, Yes/No per product |
| `comparison_house_rules.md` | The ranking / decision rules (7 rules) | Vendor doc > review; release history > undated 4.0 lists; later release > earlier; silence ≠ absence; review fills vendor silence; UNVERIFIABLE counts to neither figure |
| `racklane_manual.html` | Vendor doc for the rack chain (written for 4.0 + release history 4.1/4.2/4.3) | Has: model selector, low cut, tape (4.0), valve drive, bias, sidechain. Lacks: dual blend (explicit). 4.2 retires tape. 4.3 adds zero-latency tracking mode. |
| `micaform_page.html` | Vendor doc for Micaform 1.1 | Has: selector, Proximity, Intensity, valve drive, tape, dual blend, tracking mode, oversampling (new in 1.1). Lacks: sidechain (explicit). Silent: low cut, bias. |
| `mixbench_review.pdf` | Review of Micaform **1.0** (April 2026) | Earlier Racklane Capsule had Proximity + Intensity; Micaform 1.0 had no oversampling; earlier Racklane had no low cut of its own |
| `submission_format.md` | Exact output contract | CSV header, allowed values, note rules, results.json key set |

**Deliverables** (written to `/app`): `feature_matrix_audit.csv`, `micaform_switch_note.md`, `results.json`.

### Independent re-derivation (my own, done cold, then compared to gold — they agree)

| Row | Feature | Rack verdict / decided_by | Why | Micaform verdict / decided_by | Why |
|---|---|---|---|---|---|
| FT-1 | Capsule model selector | STANDS / racklane_manual | Model control listed | STANDS / micaform_page | Listed |
| FT-2 | Proximity | **OVERTURNED / review** | Manual silent → review says earlier Racklane had it; no removal in history → rack has it; draft said No | STANDS / micaform_page | Listed |
| FT-3 | Intensity | **OVERTURNED / review** | Same as FT-2 | STANDS / micaform_page | Listed |
| FT-4 | Valve drive stage | STANDS / racklane_manual | Drive control | **OVERTURNED / micaform_page** | Page lists valve drive; draft said No |
| FT-5 | Low cut | STANDS / racklane_manual | Manual has Low cut; review's "no low cut" is outranked by vendor | **UNVERIFIABLE / none** | Page silent; review speaks only about Racklane's low cut |
| FT-6 | Tape stage | **OVERTURNED / racklane_manual** | 4.0 lists Tape, but 4.2 history entry retires it → rack lacks it; draft said Yes | **OVERTURNED / micaform_page** | Page lists tape stage; draft said No |
| FT-7 | Dual capsule blend | STANDS / racklane_manual | Manual explicitly says no blend | STANDS / micaform_page | Listed |
| FT-8 | Zero-latency tracking | **OVERTURNED / racklane_manual** | 4.3 history entry adds tracking mode; draft said No | STANDS / micaform_page | Listed |
| FT-9 | Oversampling | **UNVERIFIABLE / none** | Manual silent; review says nothing about Racklane oversampling | STANDS / micaform_page | 1.1 page lists it; review's 1.0 "none" is outranked |
| FT-10 | Sidechain key | STANDS / racklane_manual | Listed | **OVERTURNED / micaform_page** | Page FAQ says no sidechain; draft said Yes |
| FT-11 | Valve bias | STANDS / racklane_manual | Bias control | **UNVERIFIABLE / none** | Page silent, review silent |

Counts: overturned = 7, unverifiable = 3, in common (both decided-have) = FT-1,2,3,4,8 = **5**, Micaform only (M has, R lacks) = FT-6, FT-7 = **2**. Gold `results.json` matches.

The **reasoning traps already built in** (these are what make it non-trivial):
1. Review fills vendor silence on the rack side (FT-2/3) but must not outrank the vendor (FT-5 rack, FT-9 Micaform).
2. Release history overrides the 4.0 list (FT-6 removal, FT-8 addition) → state across documents.
3. The review is about Micaform **1.0**; the page is **1.1** (FT-9 oversampling flips).
4. A review sentence about product A does not speak for product B (FT-5 Micaform cell stays UNVERIFIABLE).
5. UNVERIFIABLE rows drop out of both feature counts (Rule 7).

---

## 1. Static review findings (already done in this session — carry into `review.csv`)

### 1.1 Package consistency
- Core pieces present: `task.toml`, `instruction.md`, `tests/`, `environment/`, `solution/` ✔. `solution/golden_trajectory.json` present ✔.
- Deliverable names agree across `instruction.md`, `submission_format.md`, `tests/verifier.json`, `solution/files/` ✔.
- **Non-connector layout**: verifiers live in `tests/verifier.json`; `test.sh`/`score.py`/`test_outputs.py` read that file. Must be rewritten to `tests/manifest.json` at packaging (Phase 5) — the guideline requires it and the harness code must be repointed so the Oracle still runs.
- **`evaluations/` is wrong for delivery**: it contains `nop/` and `oracle/`. Neither is an allowed folder name (R17 allows only `solvability/`, `difficulty/`, `stability/`). Both must be **deleted** before zipping (an oracle run must never ship as evidence; a folder the gate cannot name scores as a failed run).
- `consistency/` at the root is mining-pipeline provenance (preflight, mutations, attacks, envelope). Not in the delivery spec but not forbidden. **Decision: keep for the first Delivery Gate run; remove only if the gate flags it.** Note that its `requirements.json` census will go stale after any hardening — either regenerate or state in README that it describes the mined baseline.
- `task.toml`: `network_mode = "public"` for an offline task. Dockerfile comment says agents bootstrap node via nvm, so leave it, but record it in the Layer 4 row.

### 1.2 Clarity and scope
- Ambiguity hunt (guesses I had to make while reading cold): (a) does "release history outranks" also mean a later *addition* counts — yes, Rule 3 + FT-8; (b) does the review's 1.0 statement about Micaform apply to 1.1 — no, vendor page outranks (Rule 2); (c) does the review's Racklane low-cut remark change FT-5 — no, vendor outranks. All three are resolved by the house rules text, so no defensible second answer exists. **No ambiguity fix needed at baseline.**
- `instruction.md` human paragraph is ~190 words (guideline 90–150). The rest is harness boilerplate (deliverables list + working environment). Acceptable, but trim if a rewrite happens in hardening anyway.
- Boilerplate mentions `/app/input` — harness-generated, standard across bundles; note it, do not fight it.

### 1.3 Realism and leakage
- No totals/counts leaked. Theo's "which the rack never had" note is the realistic wrong claim that the audit overturns — fine.
- Rafa's "some of his rack entries do not match what I remember" mildly hints the rack column is where errors are. Mild; acceptable, but consider softening during hardening.
- Fictional vendor/products (Tarnwell, Racklane, Micaform, Mixbench) — no real-world citation to validate. Record as PASS with that reason.

### 1.4 Verifier coverage and fairness (forward + backward)
Forward list from the instruction → 15 verifiers cover: CSV exists/header/every cell (3 table checks), note exists/60 words/3 sentences/in-common/Micaform-only/FT-6+4.2, results exists/4 figures closed key set. **No coverage gap.**
Backward: the two `incidental` verifiers (`note_*_exactly_one`) are anti-hedging guards. They map to the contract sentence "stated as the finding — not offered as one of two candidates", so they are instruction-backed. **Keep.** There are no `"category": "secondary"` verifiers in this schema (tags are `core`/`incidental`) — nothing to delete, record that.
Scoring: any core failure → 0.0; each incidental failure → −0.0667. So a GLM run can only land on 0.0, 0.867, 0.933 or 1.0. "Fully pass" = 1.0 only.
- **Regex risk (client call-out):** the three note regexes are long but value-based (digits or words, `share` ≡ `in common`, `only in Micaform` ≡ `Micaform only`, 48-char window, denial guards). They are tolerant on paper; **must be probed in Phase 2** with 6–8 paraphrased correct notes to prove they do not reject defensible wording (e.g. "the two setups share five features", "Micaform-only: two (FT-6 and FT-7)", label-before-count orderings, FT-6 written near "4.2" with a comma between).

### 1.5 Reward hacking
- `consistency/attacks.json`: label soup, hedging, duplicate rows, cross-product all caught by the engine ✔. `mutations.json`: 51 semantic mutants all caught, 3 incomplete + 2 hollow → reward 0 ✔. Extra JSON key caught by closed `object_equals` ✔. Header pinned, extra CSV columns forbidden ✔.

### 1.6 Difficulty signal available before running
- `consistency/envelope.json`: GLM-5.2 rendered the gold values correctly 3/3 (that is a *rendering* test, not a solve). `readers.json`: 4/4 GLM comprehension reads describe the right method. **Expect the baseline battery to pass 4/4 or 3/4.** Plan for at least one hardening round.

---

## 2. Phase plan

### Phase 0 — Environment and intake (your machine; ~30 min)
1. `source ~/.config/harbor/env` (every session). Confirm `OPENAI_API_KEY`, `OPENAI_BASE_URL=http://34.41.10.8:4000/v1`, `JUDGE_MODEL=openai/glm-5.2` are set (no judge here, but set it anyway).
2. Docker running; `harbor --version`; `docker ps --format '{{.Names}}'` for the budget check.
3. Unzip the mined package to a working folder, e.g. `~/work/mic-audit/task/` (rename the inner folder to `task/` or keep the long name — the ZIP must contain exactly one task folder at top level).
4. `git init` (or use this repo) so every hardening round is a commit you can diff and revert.
5. Create `glm-harbor-config.json` with `tasks[0].path` → the task folder and a `job_name` like `glm-mic-audit-r0`.
6. Sign in to the QC platform (https://qc-api-713053229214.us-central1.run.app/) and check the header says *glm access ready*.

**Exit criterion:** `harbor run -a oracle` command from Phase 2 can start (image builds).

### Phase 1 — Cold read and static review (~1 h; findings above pre-filled)
1. Re-read `instruction.md` cold, list your own guesses, compare with §0 table. Add anything I missed to the ambiguity list.
2. Write your own 22-cell answer (use the §0 table as the check).
3. Forward/backward verifier mapping (§1.4). Confirm no `secondary` verifiers.
4. Start `review.csv` notes now in a scratch file — every observation above becomes a sentence in `review_notes` later.

**Exit criterion:** ambiguity list is empty or every item has a planned fix; verifier map closed both directions.

### Phase 2 — Oracle baseline + fairness probes (~45 min)
1. Delete `evaluations/nop/` and `evaluations/oracle/` (they are mined artefacts, not delivery evidence). Commit.
2. Oracle:
   ```bash
   harbor run -p "$TASK" -a oracle \
     --ve OPENAI_API_KEY="$OPENAI_API_KEY" --ve OPENAI_BASE_URL="$OPENAI_BASE_URL" \
     -o /tmp/harbor-jobs --job-name oracle-mic-audit-r0 -n 1 -y
   cat /tmp/harbor-jobs/oracle-mic-audit-r0/*/verifier/reward.txt   # must print 1.0
   ```
   Run it **twice** (the gate says "holds on repeated runs").
3. Fairness probes (regex tolerance): copy the gold workspace, swap in 6–8 hand-written correct notes with different phrasings/orderings, and replay `tests/score.py` inside the task image:
   ```bash
   docker build -t mic-audit-env environment/
   docker run --rm -v "$PWD/tests:/tests:ro" -v "$PWD/probes/note_v3:/app" mic-audit-env \
     bash -c 'cp -r /app/input /app/ 2>/dev/null; python3 /tests/score.py'
   ```
   Every value-correct note must score 1.0. Any that fails is a verifier-fairness bug → loosen that regex (value match, not phrasing), re-run Oracle. Also probe two *wrong* notes (swapped counts, "4.1" instead of "4.2") and confirm they score 0.0.
4. Keep the Oracle reward files; they are not shipped but go in your notes with the trial IDs.

**Exit criterion:** Oracle 1.0 twice; all correct-paraphrase probes 1.0; wrong-value probes 0.0.

### Phase 3 — Baseline GLM-5.2 battery (~1.5 h wall clock)
1. `docker ps --format '{{.Names}}'` → budget.
2. Smoke test: `harbor run -c glm-harbor-config.json -n 1 -y`. Confirm `agent/trajectory.json` exists, no `exception.txt`, reward is one of {0, 0.867, 0.933, 1.0}.
3. Full battery: `harbor run -c glm-harbor-config.json -n <3-minus-running> -k 4 -y` (or reuse the smoke run as r1 and run `-k 3`).
4. Read: `cat /tmp/harbor-jobs/<job>/*/verifier/reward.txt`; open each `verifier/verifier_summary.json` / `score.json` and read whole `checks[]` entries (do not grep "passed").
5. Classify each non-1.0 run: **MODEL** (wrong cell / wrong count — good), **ambiguity** (two defensible readings — fix prompt/rules), **verifier bug** (correct answer rejected — fix grader, exclude run), **infra** (crash, 0.0 with no trajectory — re-run).
6. Record per-run: which cells were wrong. Expect misses to cluster on FT-2/3 (review on silence), FT-6/FT-8 (release history), FT-9 (1.0 vs 1.1), FT-5 Micaform cell.

**Decision point:**
- 1/4, 2/4, 3/4 with all failures MODEL → skip to Phase 5.
- 4/4 → Phase 4 (expected).
- 0/4 → look for unfairness first; only if the failures are genuinely MODEL is 0/4 submittable (with the one-third acceptance caveat).
- Bimodal or any verifier-bug failures → fix, re-Oracle, re-run.

### Phase 4 — Hardening loop (expect 1–3 rounds; ~2–3 h each)
Rule: difficulty from **coupled reasoning**, never from ambiguity, hidden info, or brittle tolerances. Lever order: `instruction.md` / house rules → input data → `tests/verifier.json`.

Candidate hardenings, ranked by leverage (pick one or two per round, not all at once):

| # | Lever | Change | Why it is coupled reasoning | Files to touch |
|---|---|---|---|---|
| H1 | Input data (release history) | Add a **4.4** entry dated after 4.3 (e.g. "4.4 — 2026-07-xx — Tape stage returns as a Valve Stage module") and make Rule 1/3 say the history counts **only up to the release the studio runs (4.3)**. | Model must cap the release history at the studio's release before applying "later outranks earlier" — a threshold derived from one document and applied to another. Naive "latest entry wins" flips FT-6 and the Micaform-only count. | `racklane_manual.html`, `comparison_house_rules.md` (make the cap explicit — no ambiguity), gold unchanged if 4.4 is excluded correctly |
| H2 | Input data (Micaform versions) | Add a "Coming in 1.2" section to the Micaform page listing e.g. a sidechain key input and a low cut filter. Rule 1 already pins Micaform 1.1 on sale. | Model must not read a roadmap as a current feature; FT-10 Micaform stays OVERTURNED and FT-5 Micaform stays UNVERIFIABLE. Naive keyword scan says "page mentions low cut → STANDS". | `micaform_page.html`; sharpen Rule 4 to say a preview of a future release does not speak for the release on sale |
| H3 | Input data (review scope) | Add a review sentence about the rack chain that the **manual contradicts** on a second feature (already have low cut); and one where the review speaks for Racklane on a feature the manual is silent about **and** the release history records its removal (Rule 4's exception clause), e.g. review: "the old Capsule module had a Wow control on the tape stage"; history 4.1 adds Wow, 4.2 retires the tape stage. Add FT-12 "Tape wow control" to the draft. | Three-hop chain: review speaks → vendor silent → but the history's removal of the parent stage removes the control. Must be stated explicitly in the 4.2 entry ("…and its Wow control") to stay unambiguous. | `draft_comparison.md` (+1 row), `mixbench_review.pdf` (regenerate with reportlab — pinned in the Dockerfile), `racklane_manual.html`, gold CSV/JSON/note, `verifier.json` expected tables, `golden_trajectory.json` |
| H4 | Draft data shape | Add a near-duplicate row (e.g. FT-12 "Capsule selector (18 models)") whose feature is the *same* as FT-1 but the draft claims Racklane has 18 models. Only add if the house rules make count-of-models irrelevant to "has the feature" — otherwise it is ambiguity, not difficulty. **Lower priority; skip unless H1–H3 are insufficient.** | Forces reading "has the feature" as presence, not spec parity | draft, gold, verifier |
| H5 | Instruction | Remove the hint "some of his rack entries do not match what I remember" → "I am not spending money on a table nobody has checked". Trim to ≤150 words. | Removes a directional hint toward the rack column | `instruction.md` |
| H6 | Verifier (last resort, fairly) | None needed today; the table checks already pin every cell. Do **not** tighten the note regexes. | — | — |

Per round procedure:
1. Apply the chosen change(s). Update **every** dependent file: input docs → gold `solution/files/*` → the heredocs inside `solution/golden_trajectory.json` → `tests/verifier.json` expected rows/figures (and the `results_figures` discrimination note) → `consistency/requirements.json` census if you keep that folder.
2. Re-derive the full 22(+)-cell table by hand and confirm the gold; check that no cell now has two defensible answers.
3. Rebuild the PDF if the review changed (reportlab 4.5.1 is pinned in the Dockerfile; keep the same layout so PyMuPDF/pypdf extraction stays clean).
4. Oracle ×2 → must be 1.0.
5. Fairness probes from Phase 2 again (the note regex for the release number stays `4.2`; if H1 adds 4.4, confirm a note mentioning both 4.2 and 4.4 near FT-6 still passes).
6. Fresh 4-run GLM battery; classify; check the band. A change to `instruction.md` or the inputs **invalidates** the previous battery — a verifier-only change may be re-graded against existing runs.
7. Commit with a message naming the round and the rewards.

**Exit criterion:** four fresh GLM runs, 1–3 of them exactly 1.0, every failure classified MODEL, Oracle 1.0 on the same package revision.

### Phase 5 — Packaging (~1 h)
1. **verifier.json → manifest.json rewrite** (non-connector rule): copy `tests/verifier.json` to `tests/manifest.json`, repoint `score.py` and `test_outputs.py` (`"verifier.json"` → `"manifest.json"`), remove `verifier.json` (or keep it identical — but one source of truth is safer). **Re-run the Oracle after this step.** Confirm each manifest entry has `name`, `source`, `assertion` and a `metadata.tag` of `core`/`incidental`.
2. Build `evaluations/`:
   - `difficulty/r1..r4/` ← the four trial folders from the final battery, copied **unflattened** (`agent/trajectory.json`, `result.json`, `verifier/reward.json`, `verifier/verifier_summary.json` or `score.json`, trial `config.json` OK).
   - `solvability/r1/` ← a copy of one difficulty run that scored 1.0 (never the oracle). If no GLM run hit 1.0 (0/4 case), use a passing run from another non-oracle model if you can get one.
   - No `stability/` (Turing runs it), no `platform/` (gate not updated yet), no job-level `config.json`, `lock.json`, `job.log`, or job-root `result.json`, nothing loose directly under `evaluations/`.
3. Normalise each rollout `result.json`: add/confirm `"model": "GLM-5.2"` (exact string), boolean `overall_pass` (reward == 1.0), `final_answer` (the results.json figures or the agent's final message), `reward`, and judge provenance (state `"judge": "deterministic — no LLM judge"` or the JUDGE_MODEL string used by the harness). Write a tiny script for this so all four are identical in shape.
4. Delete anything left from mining: `evaluations/nop/`, `evaluations/oracle/`, stray `.DS_Store`, `__pycache__`.
5. `README.md` at the task root: cumulative change summary — what changed from mined baseline and why, why the task is hard (name the coupled traps), rewards of the final battery (all four), and a justification for any Delivery Gate flag left unfixed (e.g. R3 stability: "Turing runs stability").
6. Zip **only** the task folder: `cd ~/work/mic-audit && zip -r mic-audit-v1.zip task/`.

**Exit criterion:** ZIP contains one folder with `task.toml`, `instruction.md`, `README.md`, `tests/manifest.json`, `environment/`, `solution/golden_trajectory.json`, `evaluations/{solvability,difficulty}` only.

### Phase 6 — Delivery Gate, review.csv, qc_report.html, submit (~1–1.5 h, mostly waiting)
1. Upload `mic-audit-v1.zip` to the QC platform; run the Delivery Gate (5–10 min, silent). Meanwhile do the manual checklist in the right pane.
2. Read the report card. Fix real findings in the bundle (loop back to Phase 5, or Phase 4 if a finding touches difficulty/gold). Mark the expected R3 stability finding as reviewed with "Turing runs stability".
3. Open the **review form**, paste the Drive link to the extracted task folder (folder, not zip), fill the 12 rows you own (leave `Layer 2 Stability` and `Cross-trial · Calibration` blank or one-line "Turing runs this"). Statuses only PASS / FIXED_AND_VERIFIED / N/A. Pre-drafted content per row is in §3 below. Download `review.csv` into the task root.
4. Download `qc_report.html` from the gate run and drop it at the task root next to `review.csv`.
5. Re-zip as `mic-audit-v2.zip`, upload as a **new version of the same task**, run the Delivery Gate again, and **submit that version**. (The shipped report describes v1 — expected.)
6. Submit refuses in fixed order: Harbor-bundle check → gate PASS → score at/above floor → review.csv present and resolved → not already submitted. If greyed out, read which.

**Exit criterion:** task shows *Queued in pipeline*.

### Phase 7 — After submission
- Watch states: Queued → Running → Accepted / Rejected · N findings / Pipeline error (re-run, not a rejection).
- On rejection: read findings, fix in bundle, refresh `qc_report.html` (Phase 6 steps 1–5), flip affected `review.csv` rows to FIXED_AND_VERIFIED with the recheck recorded, upload as a new version, gate, submit. Never edit a submitted version in place.

---

## 3. `review.csv` — draft content per row (write it through the form; this is the source text)

Header must be exactly: `review_check,status,review_notes,change_made,what_to_record`

| review_check | status (expected) | review_notes (seed) | what_to_record (seed) |
|---|---|---|---|
| Layer 1 · Package consistency | FIXED_AND_VERIFIED | Deliverable names agree across task.toml, instruction.md, submission_format.md, tests, solution/files. Mined bundle shipped evaluations/nop and evaluations/oracle (not allowed under R17) and tests/verifier.json (non-connector) | Deleted nop/ and oracle/; rewrote verifier.json → manifest.json and repointed score.py/test_outputs.py; Oracle re-run 1.0 |
| Layer 1 · Clarity and scope | PASS (or FIXED if H5 applied) | Cold-read guess list: release-history additions, 1.0 vs 1.1 review scope, review remark on rack low cut — all settled by house rules 2–4; no second defensible answer | Read instruction + house rules + submission_format side by side; own 22-cell derivation matched gold |
| Layer 1 · Realism and leakage | PASS | No totals/counts in prompt; fictional vendors so no external citations; Theo's wrong "never had" claim is realistic | Read instruction.md and draft for stated figures/method; none |
| Layer 2 Difficulty | FIXED_AND_VERIFIED | Baseline battery N/4 (state actual); cause; hardening applied (name H#) | Fresh 4-run battery from clean containers; rewards r1..r4 (list all four); paths evaluations/difficulty/r*/verifier/reward.json; harbor trial IDs |
| Layer 2 Solvability | PASS | evaluations/solvability/r1 is GLM-5.2 run <trial id> at reward 1.0, copied from difficulty/rX; not an oracle | Checked result.json model field and reward.json |
| Layer 2 Stability | (blank / "Turing runs this") | | |
| Layer 3 Oracle Mode | PASS | Oracle 1.0 on two consecutive runs on the final revision (job names) | harbor run -a oracle twice; reward.txt 1.0 both |
| Layer 4 · Environment and files | PASS | Dockerfile copies input/ only; PDF/HTML readable in-container (PyMuPDF, pypdf, lxml pinned); network_mode public needed for agent bootstrap | Built image, replayed score.py on gold inside it |
| Layer 4 · Connectors, MCPs, and CLIs | N/A | Native offline file task: mcp_servers = [], no connector manifest, no _app/ mirror | |
| Layer 4 · Deliverables and artifact quality | PASS | Three deliverables, exact filenames, contract in submission_format.md; gold note is real prose | Read gold files against submission_format.md |
| Layer 5 · Verifier coverage and fairness | PASS or FIXED | Forward/backward map closed (15 checks ↔ instruction items); no secondary category; note regexes probed with 6–8 paraphrases — all 1.0 | List probe files and their score.json rewards |
| Layer 5 · LLM judge consistency | N/A | No LLM judge; all 15 checks deterministic | |
| Layer 5 · Reward hacking and exploitability | PASS | Closed key set, pinned header, per-cell table_equals, hedging guards; attacks.json shows 4 attack shapes caught | Replayed hollow/incomplete/extra-key lanes via test_outputs.py |
| Cross-trial · Calibration | (blank / "Turing runs this") | | |

Quote every cell containing a comma; double any literal quote.

---

## 4. Gotchas checklist (read before each phase)

- [ ] Re-run Oracle after **every** change to gold, verifiers, inputs or instruction. Twice on the final revision.
- [ ] Gold lives in three places: `solution/files/*`, the heredocs inside `solution/golden_trajectory.json`, and `tests/verifier.json` expected values. Change all three together.
- [ ] Non-connector: no `_app/` mirror, no `sync_app_mirror.sh`. Iterate on `tests/verifier.json`; rename to `manifest.json` last, then Oracle again.
- [ ] Never ship `evaluations/oracle/`, `evaluations/nop/`, job-level files, or anything loose under `evaluations/`.
- [ ] `solvability/` must be a non-oracle run at exactly 1.0.
- [ ] Rewards can only be 0 / 0.867 / 0.933 / 1.0 here; only 1.0 is a pass. Report all four.
- [ ] A 0.0 run: check for a crash (`exception.txt`, missing trajectory) before calling it difficulty.
- [ ] 4/4 is rejected; 5/5 minus one is still 4/4.
- [ ] `review.csv` header exactly five columns; only PASS / FIXED_AND_VERIFIED / N/A; N/A only on connectors and judge rows here.
- [ ] `qc_report.html` must be **inside** the zip; the platform never injects it.
- [ ] Don't add `evaluations/platform/` yet.
- [ ] No model identifiers in commit messages or pushed files other than the `"model": "GLM-5.2"` field the spec requires.

## 5. Rough timeline

| Phase | Effort |
|---|---|
| 0 Setup | 0.5 h |
| 1 Static review | 1 h (findings pre-filled here) |
| 2 Oracle + probes | 0.75 h |
| 3 Baseline battery | 1.5 h wall clock |
| 4 Hardening | 2–3 h per round × 1–3 rounds |
| 5 Packaging | 1 h |
| 6 Gate + review + submit | 1–1.5 h |
| **Total** | **~1.5–2 working days** |
