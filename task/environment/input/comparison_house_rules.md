# Kilnworth Mix Rooms — house rules for checking a gear comparison

These rules settle every cell of a feature comparison before the studio buys or retires
anything. The comparison under check is Theo's `draft_comparison.md`. Where two documents
disagree, these rules say which one wins, so each cell has one answer.

## Rule 1 — what a cell asks

A cell asks one thing: does that product, at its current release, have the feature named on
that row? The rack chain means the Racklane host with its Capsule and Valve Stage modules at
Racklane 4.3, the release the studio runs. Micaform means Micaform 1.1, the release on sale.

## Rule 2 — which documents decide, and in what order

Three documents can decide a cell, each known here by a short name:

- `racklane_manual` — Tarnwell's Racklane module reference, `racklane_manual.html`;
- `micaform_page` — Tarnwell's Micaform product page, `micaform_page.html`;
- `review` — the Mixbench Monthly review excerpt, `mixbench_review.pdf`.

For each product, the vendor's own document outranks the review, whatever either one is
dated: `racklane_manual` for the rack chain and `micaform_page` for Micaform. A vendor document speaks only
for its own product; the review may speak for either. Theo's draft is the thing being
checked, and it never decides a cell.

## Rule 3 — older and newer inside one vendor document

Inside one vendor document, an entry in its release history outranks the document's undated
control or feature lists, and a later release's entry outranks an earlier one's. The Racklane
reference's module sections describe Racklane 4.0, and its release history runs on from
there. A release history is read only as far as the release the studio runs (rule 1): an
entry for a later release describes software the studio does not have, and it says nothing
about any cell. A control lives on the stage that carries it, so an entry that retires a
stage retires the controls that stage carried, and the document speaks to each of them.

## Rule 4 — silence

A document speaks to a feature only where it names that feature and says the product has it
or lacks it. A list that leaves a feature out says nothing about it either way. A vendor
document's preview of a release not yet on sale — a "coming in" list or a roadmap — says
nothing about the release that is on sale. Where a
product's vendor document says nothing about a feature, the review decides that cell if it
says whether that product has the feature. What the review says the earlier Racklane software had counts as the rack chain having it at its current release, unless the Racklane release history
records the feature's removal.

## Rule 5 — cells nothing decides

A cell that no document speaks to cannot be verified, whatever the draft says in it.

## Rule 6 — verdicts and the deciding document

Each cell gets one verdict:

- `STANDS` — the draft's entry agrees with the answer the deciding document gives;
- `OVERTURNED` — the draft's entry contradicts that answer;
- `UNVERIFIABLE` — no document speaks to the cell (rule 5).

The deciding document is the highest-ranked document that speaks to the cell under rules 2
to 4, and it is named even where a lower-ranked document agrees with it. An `UNVERIFIABLE`
cell's deciding document is `none`.

## Rule 7 — counting what a move gains and what it loses

Once every cell has its verdict, a feature is *in common* — the two share it — when both
products are decided to have it, and *Micaform only* — only in Micaform — when Micaform is
decided to have it and the rack chain is decided to lack it. An `UNVERIFIABLE` cell counts
as neither having nor lacking the feature, so a row carrying one counts towards neither
figure.
