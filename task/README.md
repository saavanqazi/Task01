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

Verification of the round: engine replay of `tests/score.py` on the new gold → 1.0, 17/17; note
regexes re-probed on the six paraphrases (all pass) and three wrong notes (all fail). Oracle and the
fresh GLM battery are recorded below once run.

`consistency/requirements.json` census updated for 12 rows / 17 checks. The other files under
`consistency/` (mutations, attacks, envelope, readers, preflight) are the mining pipeline's record of
the baseline and were not regenerated.

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
| Round 1 | _pending_ | _pending_ | |

## QC flags left unfixed

- Delivery Gate R3 (stability evidence): Turing runs stability since 25 Aug 2026; no `stability/` shipped.
