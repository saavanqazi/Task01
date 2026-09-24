# Change summary — tech-mg-it-b10-a5-mic-modelling-feature-matrix-audit

Reviewer's cumulative record of what changed from the mined baseline and why.

## Baseline as mined (2026-09-22 bundle)

- 11 feature rows, 3 source documents, 15 deterministic verifiers (13 core, 2 incidental), no LLM judge.
- Oracle 1.0 (re-run twice locally, 2026-09-24). Verifier fairness probed with six value-correct
  paraphrases of the note (all 1.0) and three wrong notes (all 0.0).
- GLM-5.2 difficulty battery, terminus-2 harness, 4 attempts: **4/4 at 1.0**. Too easy; rejected band.
- Package defects fixed before any run: `evaluations/nop/` and `evaluations/oracle/` removed (not
  allowed delivery folders; an oracle run is never solvability evidence).

## Hardening round 1 (2026-09-24)

Goal: difficulty from coupled reasoning across documents, never from ambiguity. Every new trap is
settled by an explicit clause in the house rules so each cell still has exactly one answer.

| Change | File(s) | What it forces |
|---|---|---|
| Racklane release history gains a **4.4** entry (2026-08-04) that brings the Tape stage back with its Wow control and retires the Valve Stage sidechain key. The studio runs 4.3 (rule 1). | `environment/input/racklane_manual.html`; rule 3 now says the history is read only as far as the release the studio runs | A naive "latest entry wins" reading flips FT-6 (rack has tape again), FT-10 (rack loses sidechain) and FT-12. The model has to take the version cap from rule 1 and apply it inside the manual. |
| Micaform page gains a **"Coming in 1.2"** preview (sidechain key input, low cut filter); the FAQ now says "Not in 1.1 ... planned for 1.2". | `environment/input/micaform_page.html`; rule 4 now says a preview of a release not on sale says nothing about the one that is | Keyword matching on the page flips FT-10 Micaform (OVERTURNED stays) and FT-5 Micaform (UNVERIFIABLE stays). |
| New draft row **FT-12 Tape wow control** (Theo: rack Yes, Micaform No). The 4.1 entry adds Wow to the Tape stage, the 4.2 entry retires the stage; the review says Micaform's tape stage has no wow control. | `environment/input/draft_comparison.md`, `mixbench_review.pdf` (regenerated with reportlab), rule 3 clause "a control lives on the stage that carries it" | Rack cell: 4.1 + 4.2 + the stage clause → lacks → OVERTURNED on `racklane_manual` (the review's mention does not outrank the vendor). Micaform cell: page silent → review decides → STANDS on `review`. First cell in the task where the review decides the Micaform side. |
| Instruction: removed "some of his rack entries do not match what I remember" | `instruction.md` | A directional hint towards the rack column, no longer given. |

Gold after round 1: 12 rows; overturned 8, unverifiable 3, in common 5, Micaform only 2.
`solution/files/*`, `solution/golden_trajectory.json` and `tests/verifier.json` updated together:
`matrix_table` row set is now FT-1..FT-12; new per-row traps `matrix_table_trap_ft10` and
`matrix_table_trap_ft12`; `results_figures` expects 8 overturned. 17 verifiers (15 core, 2 incidental).

Verification of the round: engine replay of `tests/score.py` on the new gold → 1.0, 17/17; oracle
1.0 on two fresh runs; the nine note probes replayed in the task image (six correct wordings 1.0,
three wrong notes 0.0); fresh 4-run GLM-5.2 battery → 3/4 (see Results log).

Packaging: `tests/verifier.json` carries the 17 verifiers in the engine's `{task_id, verifiers[]}`
shape and is what `tests/score.py` and `tests/test_outputs.py` load. `tests/manifest.json` is the
delivery-format object the platform's upload validation asks for (`verifier_configs[]` optional);
assertions are not duplicated into it. Oracle re-run after the change. The base image is pinned to the immutable digest its tag resolved to
(`python@sha256:392307d2…`), and `.gitattributes` keeps every script LF, both Delivery Gate
findings (QC1-2, QC1-3) seen on an earlier bundle. The mining pipeline's `consistency/` folder was
dropped because it describes the pre-hardening gold.

## Why the task is hard

Correctness depends on interactions, not on independent rules: which document ranks first for a
cell depends on which product the cell is about and whether the vendor document actually speaks;
whether a release-history entry counts depends on a version cap stated in a different rule; a
control's presence depends on the fate of the stage that carries it two entries later; and the
review's date (Micaform 1.0) and the page's preview (1.2) both have to be discounted against the
release on sale (1.1). A per-rule script gets the easy cells and fails on the coupled ones, and any
core miss zeroes the run.

## Results log

| Round | Oracle | GLM-5.2 (terminus-2) rewards | Verdict |
|---|---|---|---|
| Baseline | 1.0, 1.0 | 1.0, 1.0, 1.0, 1.0 (job `glm-mic-audit-r0-t2`) | 4/4, too easy |
| Round 1 | 1.0, 1.0 (jobs `oracle-r1`, `oracle-r1b`); 1.0 again after the manifest rename (`oracle-r1-manifest`) | 1.0, 0.0, 1.0, 1.0 (job `glm-mic-audit-r1-t2`, trials CwyDXsG, iRPbaaP, Kp4Xjwu, sdgoqtb) | 3/4, in band |

Failing run (trial iRPbaaP, `evaluations/difficulty/r2`): every one of the 24 matrix cells correct. The agent
first wrote 5 in common, then on a self-check revised it to 4, listing FT-1, FT-2, FT-3 and FT-8 as the
only shared rows and dropping FT-4. Theo's draft has Micaform lacking the valve drive; the audit
overturns that on the Micaform page, so Micaform has it and the row is in common (rule 7). The slip is
in translating a verdict back into has/lacks before counting — the coupled step the task is built
around — and rule 7 admits no other reading. Classified MODEL; `note_in_common` and `results_figures`
failed together, exactly the checks that carry that figure.

## Rollouts shipped

| rollout | harbor trial | reward | outcome |
|---|---|---|---|
| difficulty/r1 | task__CwyDXsG | 1.0 | all 24 cells and all four counts correct |
| difficulty/r2 | task__iRPbaaP | 0.0 | MODEL: all 24 cells correct; in-common revised from 5 to 4 on a self-check, dropping FT-4 |
| difficulty/r3 | task__Kp4Xjwu | 1.0 | correct |
| difficulty/r4 | task__sdgoqtb | 1.0 | correct |

`evaluations/solvability/r1` is a copy of difficulty/r1, trial task__CwyDXsG (a GLM-5.2 run on the
terminus-2 harness, not the oracle). Zero exceptions; every run wrote all three deliverables.

**Evidence format note.** This harbor build writes `verifier/reward.txt` and `verifier/score.json`;
the bundle's `verifier/reward.json` and `verifier/verifier_summary.json` were derived from those two
files by the packaging script (a format conversion, no new facts), which also added `model`,
`overall_pass`, `final_answer`, `reward` and `judge` to each `result.json`.

## Scoring shape

Fifteen core checks gate the reward and two incidental hedging guards cost 1/17 each, so a run
scores 1.0, 0.933, 0.867 or 0.0. The difficulty signal is the count of runs at exactly 1.0.

## QC flags left unfixed

- Delivery Gate R3 (stability evidence): Turing runs stability since 25 Aug 2026; no `stability/` shipped.
