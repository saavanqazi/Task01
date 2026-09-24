# Submission format

Deliver exactly these files, in your working directory:

- `feature_matrix_audit.csv` — One row per feature row of Theo's draft: a verdict and a deciding document for each product's cell.
- `micaform_switch_note.md` — The short note to Maren on where the move to Micaform stands.
- `results.json` — a JSON object; see below.

## `feature_matrix_audit.csv`

Header, exactly: `feature_id,racklane_verdict,racklane_decided_by,micaform_verdict,micaform_decided_by`
One row per record, keyed by `feature_id`.
One row per feature row in `draft_comparison.md` and no other rows, in any order, with `feature_id` exactly as the draft writes it. Each row carries two cells for each product. `racklane_verdict` and `micaform_verdict` each take exactly one of `STANDS`, `OVERTURNED` or `UNVERIFIABLE`: whether Theo's entry for that product on that row survives the documents. `racklane_decided_by` and `micaform_decided_by` name the one document that decides that cell, by its short name in the house rules — `racklane_manual`, `micaform_page` or `review` — or `none` where the verdict is `UNVERIFIABLE`. Which document decides a cell is not a judgement call: the house rules rank the documents, say what counts as a document speaking to a feature, and name the deciding document even where another one agrees with it, so every cell has one answer.

Example (placeholder values):

```
feature_id,racklane_verdict,racklane_decided_by,micaform_verdict,micaform_decided_by
FT-0,STANDS,racklane_manual,UNVERIFIABLE,none
```

## `micaform_switch_note.md`

A note to Maren, written as prose. Lay it out however you like — wrapped, one sentence to a
line, or bulleted — and nothing about its wording is graded beyond the facts listed here. The
note says what the move buys and what it costs: it names every feature that is `Micaform only`
and every feature that is `rack only`, counted the way the house rules count them. A feature is
named by the distinctive word of its row in Theo's draft — `selector`, `Proximity`, `Intensity`,
`drive`, `low cut`, `tape`, `blend`, `tracking`, `oversampling`, `sidechain`, `bias`, `wow` —
in any wording around it, in any case, hyphenated or not; mentioning other features as well
costs nothing, and a feature named as something Micaform lacks or the rack lacks still counts
as named. The note states how many features the two setups have `in common` and how many are `Micaform only`, each once, as a figure beside its label, in figures or spelled out in words, counted the way the house rules count them; `share` reads as the same label as `in common`, and `only in Micaform` as the same label as `Micaform only`. Beside means in the same sentence and close: the check allows about 48 characters between a count and its label, with no other number between them when the count comes first. Both counts are required on the note: a note that leaves either out, swaps them or states either wrongly fails. The note also names the tape stage row by its feature id — that id is required, exactly as the draft writes it — together with the number of the Racklane release that settles whether the rack chain still has a tape stage, in figures as the release history writes it; the two sit in the same paragraph, within about nine hundred characters of each other, and the check reads them as named together rather than as one attributed to the other. Every one of those figures is STATED, and a figure written as a denial does not count: a `no` or `not` directly in front of a figure refuses it; so does a `no` or `not` earlier in the figure's own clause whenever the figure comes before its label or id; and so does a `no` or `not` standing between the release number and the id inside one clause. A clause ends at a full stop, a question or exclamation mark, a comma, semicolon, colon or dash, or at the word `and`, `but`, `yet` or `so`. Denying a WRONG figure in a clause of its own is free. Nothing else about the note is graded — not its tone, its recommendation, or the order it takes. Each of the two counts stands beside its label once, stated as the finding — not offered as one of two candidates. That last rule is checked beside `in common` and `Micaform only` only, so a hedge beside `share` or `only in Micaform` costs nothing. The release number is not guarded that way: it is graded as the figure it stands beside, and a note that hedges it loses nothing.
How long the note runs is presentation and earns nothing; the reference note is a few short paragraphs, because a note that tells a business partner where a purchase stands says why as well as what.

## `results.json`

A JSON object with exactly these keys and nothing else:

- `overturned_cell_count` — number
- `unverifiable_cell_count` — number
- `in_common_feature_count` — number
- `micaform_only_feature_count` — number

Shape example (placeholder values):

```json
{
  "overturned_cell_count": 0,
  "unverifiable_cell_count": 0,
  "in_common_feature_count": 0,
  "micaform_only_feature_count": 0
}
```

`overturned_cell_count` is the number of cells in the audit whose verdict is `OVERTURNED`, counting both products' cells on every row; `unverifiable_cell_count` is the number of cells whose verdict is `UNVERIFIABLE`, counted the same way; `in_common_feature_count` is the number of feature rows that are in common and `micaform_only_feature_count` the number that are Micaform only, both as the house rules count them.
