#!/usr/bin/env python3
"""Derive the gold audit from an evidence model of the input documents under the house rules.

Run from the task root:  python3 solution/compute_gold.py
Writes solution/files/feature_matrix_audit.csv, results.json, updates the manifest expected values
in tests/verifier.json and the heredocs in solution/golden_trajectory.json. The note is kept as
written in solution/files/micaform_switch_note.md (its figures are checked against the results).

The evidence model is the reviewer's transcription of what each document says; the documents in
environment/input are the source of truth and this file must be kept in step with them.
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAIN_RELEASE = (4, 2, 10)          # studio_inventory.csv: the TM-9 rig is held at Racklane 4.2.10
MICAFORM_RELEASE = (1, 1)           # micaform_page.html: the release on sale

def ver(s): return tuple(int(x) for x in s.split("."))

# ---- Theo's draft: (feature_id, feature, rack_entry, micaform_entry); the duplicated line is one feature
DRAFT = [
 ("FT-1",  "Capsule model selector",          "Yes", "Yes"),
 ("FT-2",  "Proximity control",               "No",  "Yes"),
 ("FT-3",  "Intensity control",               "No",  "Yes"),
 ("FT-4",  "Valve drive stage",               "Yes", "No"),
 ("FT-5",  "Low cut filter",                  "Yes", "Yes"),
 ("FT-6",  "Tape stage",                      "Yes", "No"),
 ("FT-7",  "Dual capsule blend in one instance","No", "Yes"),
 ("FT-8",  "Zero latency tracking mode",      "No",  "Yes"),
 ("FT-9",  "Oversampling",                    "No",  "Yes"),
 ("FT-10", "Sidechain key input",             "Yes", "Yes"),
 ("FT-11", "Valve bias control",              "Yes", "No"),
 ("FT-12", "Tape wow control",                "Yes", "No"),
 ("FT-13", "Polarity flip",                   "No",  "Yes"),
 ("FT-14", "Preset browser",                  "Yes", "Yes"),
 ("FT-15", "Resizable window",                "No",  "Yes"),
 ("FT-16", "Room reverb",                     "No",  "No"),
]

# ---- What the documents say. Each statement: (doc, product, feature_id, has, release)
#  doc: racklane_manual | micaform_page | review ; product: rack | micaform
#  release: None for an undated list; a version tuple for a release-history entry (rule 3).
#  The vendor documents' cross-product remarks (sidebar, "never offered") are NOT statements (rule 2).
#  Previews of unsold releases are NOT statements (rule 4).
S = []
def say(doc, product, fid, has, release=None): S.append((doc, product, fid, has, release))

# racklane_manual.html — module sections written for 4.0
for fid in ("FT-1", "FT-5", "FT-6", "FT-4", "FT-11", "FT-10"): say("racklane_manual", "rack", fid, True)
say("racklane_manual", "rack", "FT-7", False)                      # "has no dual capsule blend"
# release history (the chain runs 4.2.10; later entries say nothing)
say("racklane_manual", "rack", "FT-12", True,  ver("4.1"))         # Tape stage gains a Wow control
say("racklane_manual", "rack", "FT-6",  False, ver("4.2"))         # Tape stage retired ...
say("racklane_manual", "rack", "FT-12", False, ver("4.2"))         # ... with the controls it carried (rule 3)
say("racklane_manual", "rack", "FT-5",  False, ver("4.2.3"))       # Low cut moves to the Room module (outside the chain)
say("racklane_manual", "rack", "FT-16", False, ver("4.2.3"))       # Room reverb lives only on the Room module (outside the chain)
say("racklane_manual", "rack", "FT-3",  False, ver("4.2.7"))       # Intensity retired
say("racklane_manual", "rack", "FT-5",  True,  ver("4.2.10"))      # Low cut returns to the Capsule module
say("racklane_manual", "rack", "FT-13", True,  ver("4.2.10"))      # Polarity flip added to the Capsule module
say("racklane_manual", "rack", "FT-2",  False, ver("4.2.11"))      # Proximity retired  (beyond the chain's release)
say("racklane_manual", "rack", "FT-8",  True,  ver("4.3"))         # Tracking mode        (beyond)
say("racklane_manual", "rack", "FT-6",  True,  ver("4.4"))         # Tape returns         (beyond)
say("racklane_manual", "rack", "FT-12", True,  ver("4.4"))         # ... with its Wow     (beyond)
say("racklane_manual", "rack", "FT-10", False, ver("4.4"))         # Sidechain retired    (beyond)

# micaform_page.html — describes 1.1; "Changes in 1.1" is its release entry; "Coming in 1.2" says nothing
for fid in ("FT-1", "FT-2", "FT-3", "FT-4", "FT-6", "FT-7", "FT-8"): say("micaform_page", "micaform", fid, True)
say("micaform_page", "micaform", "FT-9",  True,  ver("1.1"))       # Oversampling
say("micaform_page", "micaform", "FT-15", True,  ver("1.1"))       # Resizable window
say("micaform_page", "micaform", "FT-13", False, ver("1.1"))       # Polarity flip removed
say("micaform_page", "micaform", "FT-10", False)                   # FAQ: no sidechain input in 1.1

# mixbench_review.pdf — reviews Micaform 1.0; may speak for either product
say("review", "rack", "FT-2", True); say("review", "rack", "FT-3", True)     # earlier Capsule module had both
say("review", "micaform", "FT-4", True); say("review", "micaform", "FT-6", True)
say("review", "micaform", "FT-12", False)                                     # tape stage has no wow control
say("review", "micaform", "FT-7", True); say("review", "rack", "FT-7", False)
say("review", "micaform", "FT-9", False)                                      # 1.0: no oversampling (outranked by the 1.1 page)
say("review", "micaform", "FT-10", False)
say("review", "rack", "FT-5", False)                                          # earlier chain had no low cut (outranked)
say("review", "micaform", "FT-13", True)                                      # 1.0 puts a polarity flip on the panel (outranked)
say("review", "micaform", "FT-14", True); say("review", "rack", "FT-14", False)  # preset browser the chain never had

VENDOR = {"rack": "racklane_manual", "micaform": "micaform_page"}
CAP = {"rack": CHAIN_RELEASE, "micaform": MICAFORM_RELEASE}

def vendor_says(product, fid):
    """Rule 3: the latest release entry at or below the cap outranks the undated list; both outrank silence."""
    doc = VENDOR[product]
    entries = [(rel, has) for d, p, f, has, rel in S if d == doc and p == product and f == fid and rel is not None and rel <= CAP[product]]
    if entries:
        return max(entries)[1]
    lists = [has for d, p, f, has, rel in S if d == doc and p == product and f == fid and rel is None]
    return lists[0] if lists else None

def review_says(product, fid):
    r = [has for d, p, f, has, rel in S if d == "review" and p == product and f == fid]
    if not r: return None
    has = r[0]
    if product == "rack" and has:  # rule 4: what the earlier software had counts unless the history records removal
        removed = [rel for d, p, f, h, rel in S if d == VENDOR["rack"] and p == "rack" and f == fid and rel is not None and rel <= CAP["rack"] and not h]
        if removed: return None    # the manual speaks (vendor_says handles it)
    return has

def decide(product, fid):
    v = vendor_says(product, fid)
    if v is not None: return v, VENDOR[product]
    r = review_says(product, fid)
    if r is not None: return r, "review"
    return None, "none"

def verdict(entry, has):
    if has is None: return "UNVERIFIABLE"
    return "STANDS" if (entry == "Yes") == has else "OVERTURNED"

rows, poss = [], {}
for fid, name, re_, me in DRAFT:
    rh, rd = decide("rack", fid); mh, md = decide("micaform", fid)
    rows.append({"feature_id": fid, "racklane_verdict": verdict(re_, rh), "racklane_decided_by": rd,
                 "micaform_verdict": verdict(me, mh), "micaform_decided_by": md})
    poss[fid] = (rh, mh)

overturned = sum(r[k] == "OVERTURNED" for r in rows for k in ("racklane_verdict", "micaform_verdict"))
unverifiable = sum(r[k] == "UNVERIFIABLE" for r in rows for k in ("racklane_verdict", "micaform_verdict"))
in_common = [f for f, (r, m) in poss.items() if r is True and m is True]
mic_only = [f for f, (r, m) in poss.items() if m is True and r is False]
rack_only = [f for f, (r, m) in poss.items() if r is True and m is False]
results = {"overturned_cell_count": overturned, "unverifiable_cell_count": unverifiable,
           "in_common_feature_count": len(in_common), "micaform_only_feature_count": len(mic_only)}

if __name__ == "__main__":
    print(f"chain at {'.'.join(map(str, CHAIN_RELEASE))}, Micaform {'.'.join(map(str, MICAFORM_RELEASE))}")
    for r in rows: print(f"  {r['feature_id']:6s} {r['racklane_verdict']:12s} {r['racklane_decided_by']:16s} {r['micaform_verdict']:12s} {r['micaform_decided_by']}")
    print("results", results); print("in common", in_common, "| Micaform only", mic_only, "| rack only", rack_only)
    if "--write" in sys.argv:
        files = ROOT / "solution" / "files"
        with open(files / "feature_matrix_audit.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["feature_id", "racklane_verdict", "racklane_decided_by", "micaform_verdict", "micaform_decided_by"], lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        (files / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        print("wrote solution/files/feature_matrix_audit.csv and results.json")
