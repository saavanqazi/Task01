# review.csv — row text to paste into the review form

Header the form writes: `review_check,status,review_notes,change_made,what_to_record`
Statuses: PASS / FIXED_AND_VERIFIED / N/A only. Leave the two "Turing runs this" rows blank or one line.
Adjust job/trial names if yours differ. Keep the facts; reword freely.

---

**Layer 1 · Package consistency** — FIXED_AND_VERIFIED
- review_notes: task.toml, instruction.md, input/submission_format.md, tests/manifest.json and solution/files name the same three deliverables (feature_matrix_audit.csv, micaform_switch_note.md, results.json). Mined bundle shipped evaluations/nop and evaluations/oracle, which are not delivery folders (R17), and carried the verifier spec as tests/verifier.json (non-connector layout).
- change_made: Deleted evaluations/nop and evaluations/oracle. Renamed tests/verifier.json to tests/manifest.json and repointed tests/score.py and tests/test_outputs.py. After hardening, updated solution/files/*, solution/golden_trajectory.json heredocs and tests/manifest.json together (12 rows, 17 checks).
- what_to_record: Oracle re-run after the rename: reward 1.0 (job oracle-r1-manifest). Read all files side by side; row set FT-1..FT-12 identical in draft, gold CSV and manifest.

**Layer 1 · Clarity and scope** — FIXED_AND_VERIFIED
- review_notes: Cold read produced three guesses (do later release entries count as additions; does the 1.0 review bind 1.1; does the review's rack low-cut remark move FT-5). All three are settled by house rules 2–4, so no second defensible answer. Hardening added three traps (release history beyond the studio's 4.3; a Micaform 1.2 preview; a control on a retired stage) and each got an explicit clause in comparison_house_rules.md so every cell keeps one answer. Prompt hint "some of his rack entries do not match what I remember" removed as a directional hint.
- change_made: environment/input/comparison_house_rules.md: rule 3 gains the version cap and the stage-carries-control clause; rule 4 gains the preview clause. instruction.md: hint sentence removed.
- what_to_record: Re-derived all 24 cells by hand against the new rules and matched the gold. Three GLM-5.2 runs at 1.0 on the hardened package show the rules are followable; the one miss was a counting slip, not a rule reading.

**Layer 1 · Realism and leakage** — PASS
- review_notes: No counts, totals or method in instruction.md; deliverable names only. Theo's "which the rack never had" is the realistic wrong claim the audit overturns. Vendors and products are fictional, so no external citation to validate. Dockerfile copies input/ only; tests/ and solution/ never enter the image.
- what_to_record: Read instruction.md, draft_comparison.md and submission_format.md for stated figures or recipes; none. Checked environment/Dockerfile COPY lines.

**Layer 2 Difficulty** — FIXED_AND_VERIFIED
- review_notes: Baseline GLM-5.2 battery (terminus-2, job glm-mic-audit-r0-t2) passed 4/4: the eleven rows were all settled by single-hop lookups once the rules were read. Cause: no trap required composing two documents with a rule. Rewards after hardening in evaluations/difficulty/r1..r4/verifier/reward.json (job glm-mic-audit-r1-t2, trials CwyDXsG, iRPbaaP, Kp4Xjwu, sdgoqtb).
- change_made: racklane_manual.html gains a 4.4 entry beyond the studio's 4.3 (tape stage returns, sidechain retired); micaform_page.html gains a "Coming in 1.2" preview and a version-scoped FAQ; draft_comparison.md gains FT-12 tape wow control; mixbench_review.pdf regenerated with the review speaking to Micaform's wow control; house rules gain the three clauses; gold and manifest updated.
- what_to_record: Oracle 1.0 twice, then a fresh 4-run GLM-5.2 battery from clean containers: 1.0, 0.0, 1.0, 1.0 — 3 of 4. The 0.0 run had all 24 cells right and miscounted in-common as 4 (dropped FT-4 after overturning Theo's No on Micaform's valve drive); classified MODEL.

**Layer 2 Solvability** — PASS
- review_notes: evaluations/solvability/r1 is a copy of difficulty/r1 (GLM-5.2, terminus-2, trial CwyDXsG), reward 1.0, model field "GLM-5.2". Not an oracle run.
- what_to_record: Checked result.json model/reward/overall_pass and verifier/reward.json in solvability/r1.

**Layer 2 Stability** — (leave blank, or: Turing runs this.)

**Layer 3 Oracle Mode** — PASS
- review_notes: Oracle at 1.0 on the baseline (oracle-r0, oracle-r0b), after hardening (oracle-r1, oracle-r1b) and after the manifest rename (oracle-r1-manifest). Engine replay of tests/score.py on the gold also 1.0, 17/17.
- what_to_record: harbor run -a oracle, five runs across the three package revisions, reward.txt 1.0 each time.

**Layer 4 · Environment and files** — PASS
- review_notes: python:3.12-slim image with pinned engine deps and document readers (PyMuPDF for the PDF). All five inputs readable in-container; regenerated PDF extracts cleanly via PyMuPDF. network_mode public is needed for agent bootstrap only; the task itself is offline.
- what_to_record: Built the image, replayed score.py and the nine note probes inside it; opened every input file's extracted text.

**Layer 4 · Connectors, MCPs, and CLIs** — N/A
- review_notes: Native offline file task: task.toml mcp_servers = [], no connector manifest, no environment/_app mirror. Nothing to review.

**Layer 4 · Deliverables and artifact quality** — PASS
- review_notes: Three deliverables at exact filenames; contract in input/submission_format.md (header, allowed values, closed JSON key set, note rules). Gold note is written prose that a partner could read; gold CSV and JSON conform to the contract.
- what_to_record: Read solution/files/* against submission_format.md line by line; oracle 1.0 confirms the verifiers accept them.

**Layer 5 · Verifier coverage and fairness** — PASS
- review_notes: Forward map from instruction to checks and backward map from the 17 checks to instruction items both close: every ask has a check, every check follows from an ask. No "secondary" category present (tags are core/incidental; the two incidental anti-hedging checks follow from the contract sentence "stated as the finding — not offered as one of two candidates"). Note regexes are value-based (digits or words, share ≡ in common, only in Micaform ≡ Micaform only).
- what_to_record: Replayed six value-correct note wordings (label-first, "share", bullets, denial of a wrong figure, one sentence per line) in the task image: all 1.0. Three wrong notes (swapped counts, wrong release, hedged count): all 0.0.

**Layer 5 · LLM judge consistency** — N/A
- review_notes: No LLM judge: all 17 checks are deterministic file assertions (tests/manifest.json).

**Layer 5 · Reward hacking and exploitability** — PASS
- review_notes: CSV header pinned and column set closed; every cell graded by table_equals with a row-set population lock (no extra or duplicate rows); results.json key set closed; hedging guards on both note counts; denial guards on every figure. Any core failure zeroes the run. consistency/attacks.json records label soup, hedging, duplicate rows and cross-product all caught.
- what_to_record: Ran tests/test_outputs.py negative lanes (deleted deliverable, corrupted figure, extra key) via the oracle's pytest step; each drives reward to 0.

**Cross-trial · Calibration** — (leave blank, or: Turing runs this.)
