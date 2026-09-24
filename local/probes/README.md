Probe workspaces for local/run_probes.sh. Each folder = gold CSV + gold results.json + one note variant.
EXPECT holds the reward the verifier must return:
  p01..p06  value-correct notes in different wordings/layouts -> must all be 1.0 (else a regex is unfair)
  n01       counts swapped                                      -> 0.0
  n02       wrong release number beside FT-6                    -> 0.0
  n03       Micaform-only count hedged "2 or 3"                 -> 0.0 (the hedge breaks the core count match and fires the incidental guard)
If a p-probe scores below 1.0, loosen the regex that failed (value match, not phrasing), re-run the Oracle.
If an n-probe scores higher than EXPECT, the verifier is exploitable — tighten it and re-run the Oracle.
