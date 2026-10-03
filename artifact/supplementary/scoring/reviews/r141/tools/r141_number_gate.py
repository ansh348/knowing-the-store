# -*- coding: utf-8 -*-
"""r141_number_gate.py -- the number gate of R141: R140's gate (R139, R137, R135, R134 underneath) plus every number and verdict the SB-60 landing prints, read
from reviews/r141/results/scores_sb60.json and nomodel_sb60.json and re-derived from their raw bounds (not from r141_printed.json, which port_r141.py fills its
texts from): the lookup's matched score, Sol's matched lead and its reliability, Luna's lead not reliable on the matched metric, the prediction verdicts and the
branch, the prediction count (106 / 34; tab:registrations-e 13 with 5), the freeze day (44), A2's comparison count, and the C.2 table's numerals. With --built,
the numeral-set checks with the R141 forms allowed.
Usage: python reviews/r141/tools/r141_number_gate.py [--built]
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r140" / "tools"))
sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
import r140_number_gate as R140  # noqa: E402  (it rebinds R139's checks139 to its own)

R = R140.R
G = R.G
_prev = R.checks139


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


SUPERSEDED = {"main text carries (R140): A list-length cue is uncontrolled there.":
              ("The lead holds for Sol against a sibling padded to the same length and counts.", "R141 B-ii replaces R140's abstract sentence (the fired branch, frozen f224177)")}


def checks141():
    chk = G.chk
    mt0 = R.main_text()

    def chk_prev(label, *a, **k):
        if label in SUPERSEDED:
            frag, why = SUPERSEDED[label]
            return chk(label.replace("(R140)", "(R140, superseded)") + f" -> '{frag[:40]}'", "present", "present" if frag in mt0 else "absent", why)
        return chk(label, *a, **k)
    G.chk = chk_prev
    try:
        _prev()
    finally:
        G.chk = chk
    S = J("reviews/r141/results/scores_sb60.json")
    NM = J("reviews/r141/results/nomodel_sb60.json")["readers"]
    ML, RD, P = S["minus_lookup"], S["readers"], S["predictions"]
    rel = lambda x: (x["ci_triple" if "ci_triple" in x else "ci_item"]["ci_lo"] > 0 or x["ci_triple" if "ci_triple" in x else "ci_item"]["ci_hi"] < 0) and (x["ci_persona"]["ci_lo"] > 0 or x["ci_persona"]["ci_hi"] < 0)
    mt = R.main_text()
    lk = RD["Name lookup"]["pn60_vs_sb60"]
    chk("5.2 (R141 B-ii): 'the lookup scores 0.82' (matched, PN-60 vs SB-60)", "0.82", lk["matched"], "scores_sb60.json readers/Name lookup/pn60_vs_sb60")
    rec = NM["Name lookup (embedding)"]["pn60_vs_sb60"]
    chk("C.2: the lookup reproduces its recorded W/T/L", f"{rec['W']}/{rec['T']}/{rec['L']}", f"{lk['W']}/{lk['T']}/{lk['L']}", "nomodel_sb60.json (recorded before the freeze)")
    sol = ML["GPT-5.6 Sol"]["matched"]
    chk("abstract / 5.2 / Conclusion: 'Sol leads it by a reliable 0.09' (matched)", "0.09", sol["delta"], "scores_sb60.json minus_lookup/GPT-5.6 Sol/matched", reliable=True, actual_reliable=rel(sol) and sol["delta"] > 0)
    luna = ML["GPT-5.6 Luna"]["matched"]
    chk("5.2 / Limitations: 'Luna's lead is not separated from the cue' (matched not reliable)", "not reliable", "not reliable" if not rel(luna) else "reliable", f"minus_lookup/GPT-5.6 Luna/matched {luna['delta']:+.4f}")
    chk("R141 predictions", "FAILS,HOLDS,HOLDS,HOLDS", ",".join("HOLDS" if P[k]["holds"] else "FAILS" for k in ("P-S1", "P-S2", "P-S3", "P-S4")), "scores_sb60.json predictions")
    chk("R141 branch", "B-ii", S["branch"], "scores_sb60.json branch")
    chk("P-S1 re-derived: Luna matched minus lookup not reliable", "False", str(rel(luna) and luna["delta"] > 0), "the raw bounds")
    chk("P-S2 re-derived: Sol matched minus lookup reliable and positive", "True", str(rel(sol) and sol["delta"] > 0), "the raw bounds")
    mini = ML["GPT-4.1 mini"]["matched"]
    chk("P-S3 re-derived: mini not reliably above", "True", str(not (rel(mini) and mini["delta"] > 0)), "the raw bounds")
    chk("P-S4 re-derived", "True", str(all(RD[n]["pn60_vs_sb60"]["matched"] >= 0.80 and RD[n]["pn60_vs_sb60"]["ci_persona"]["ci_lo"] > 0.50 for n in ("GPT-5.6 Luna", "GPT-5.6 Sol"))), "readers/*/pn60_vs_sb60")
    chk("the seed sensitivity changes no reading", "0", str(len(S["seed_reading_changes"])), "scores_sb60.json seed_reading_changes")
    # the count and the day
    chk("4 / F: 106 predictions, 34 otherwise (102 / 33 plus P-S1 to P-S4, P-S1 otherwise)", "106/34", f"{102 + 4}/{33 + sum(1 for k in P if not P[k]['holds'])}", "AUX-R137-COUNT plus the R141 predictions")
    chk("F: tab:registrations-e 13 with 5", "13 with 5", f"{9 + 4} with {4 + sum(1 for k in P if not P[k]['holds'])}", "AUX-R137-COUNT plus the R141 predictions")
    import subprocess
    # the freeze commit's date: recorded in results/freeze_r141.json (from git, at the close) so the check runs in the archive, which is not a git checkout;
    # where git is present the recorded date must equal git's
    FR = J("reviews/r141/results/freeze_r141.json")
    ci = FR["committer_date"]
    try:
        g = subprocess.run(["git", "log", "-1", "--format=%cs", FR["commit"]], cwd=ROOT, capture_output=True, text=True)
    except OSError:
        g = None
    if g is not None and g.returncode == 0 and g.stdout.strip():
        chk("F: the recorded freeze date equals git's", ci, g.stdout.strip(), f"git log {FR['commit'][:7]}")
    day = (datetime.date.fromisoformat(ci) - datetime.date(2026, 8, 10)).days
    chk("F: the freeze day of f224177", "44", str(day), f"freeze_r141.json {ci} against day 0 = 2026-08-10")
    NC = J("reviews/r139/results/n_count_r139.json")
    m = re.search(r"reliable describes each of the \$(\d+)\$ comparisons", mt)
    chk("4 A2: the comparison count printed", str(NC["n_distinct"]), m.group(1) if m else "absent", "n_count_r139.json (the SB-60 entry included)")
    for frag in ("The lead holds for Sol against a sibling padded to the same length and counts.", "Luna's lead is not separated from the cue"):
        chk(f"main text carries (R141): {frag[:50]}", "present", "present" if frag in mt else "absent", "the built main text")


def allowed141():
    S = J("reviews/r141/results/scores_sb60.json")
    NM = J("reviews/r141/results/nomodel_sb60.json")["readers"]
    B = J("reviews/r141/build/build_sb60.json")
    main = {"0.82", "0.09", "0.11", "+0.04", "0.04", "106", "34", str(J("reviews/r139/results/n_count_r139.json")["n_distinct"])}
    appx = {"44", "106", "34", "13", "5", "176", "88", "60", "30", "0", "0.80", "0.50", "43", "46", "95%", "90%", "0.05", "+0.05", "-0.05", "0.5000", str(B["meta"]["n_substituted"])}
    def add(d):
        nonlocal appx
        for k in ("W", "T", "L"):
            appx.add(str(d[k]))
        appx.add(f"{d['W']}/{d['T']}/{d['L']}")
        appx.add(f"{d['matched']:.4f}")
        for c in ("ci_triple", "ci_persona"):
            appx |= {f"{d[c]['ci_lo']:.4f}", f"{d[c]['ci_hi']:.4f}"}
    for r in S["readers"].values():
        add(r["pn60_vs_sb60"]); appx.add(f"{r['sb60_vs_present']['matched']:.4f}"); appx.add(f"{r['pooled_pn60_vs_sb60']['auroc']:.4f}")
    for r in NM.values():
        add(r["pn60_vs_sb60"]); appx.add(f"{r['sb60_vs_present']['matched']:.4f}"); appx.add(f"{r['pooled_pn60_vs_sb60']:.4f}")
    for d in S["minus_lookup"].values():
        for x in d.values():
            for v in [x["delta"]] + [x[c][e] for c in (("ci_triple", "ci_persona") if "ci_triple" in x else ("ci_item", "ci_persona")) for e in ("ci_lo", "ci_hi")]:
                appx |= {f"{v:+.4f}", f"{v:.4f}".lstrip("-")}
    return main, appx


R.checks139 = checks141
_af = R.allowed139


def allowed():
    m0, a0 = _af()
    m1, a1 = allowed141()
    return m0 | m1, a0 | a1


R.allowed139 = allowed

if __name__ == "__main__":
    R.main()
