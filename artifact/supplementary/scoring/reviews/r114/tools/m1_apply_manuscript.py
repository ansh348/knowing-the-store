# -*- coding: utf-8 -*-
"""m1_apply_manuscript.py -- program R114 (2026-09-17): the composite's five-line proxy replaced by the actual-view results in tab:ds-a7
and its prose (ds_downstream/NUMBERS_DS.md section 14, AUX-DS-R114-COMPOSITE-ACTUAL / -ACTUAL-DIFF), and the Opus 5 moved-count row
(r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8, AUX-V2RCAT-OP5) in Section 5 and tab:v2rcat. Asserted replacements in
reviews/v19/src (LF files). Run from the repository root: python reviews/r114/tools/m1_apply_manuscript.py [--no-opus]
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
B, X = SRC / "body_v19.tex", SRC / "appendix_v19.tex"
E = []


def rep(f, old, new):
    E.append((f, old, new))


# ---------------------------------------------------------------- (1) tab:ds-a7, the twelve changed rows (AUX-DS-R114-COMPOSITE-ACTUAL)
ROWS = [
    ("GPT-4.1 mini & Literal rule (header) & $55$ & $4$ ($1$) & $241 = 0 + 241$ & $300$ & $58$ \\\\", "GPT-4.1 mini & Literal rule (header) & $55$ & $4$ ($1$) & $242 = 0 + 242$ & $301$ & $58$ \\\\"),
    ("GPT-4.1 mini & Literal rule (tagged) & $55$ & $4$ ($1$) & $241 = 0 + 241$ & $300$ & $58$ \\\\", "GPT-4.1 mini & Literal rule (tagged) & $55$ & $4$ ($1$) & $242 = 0 + 242$ & $301$ & $58$ \\\\"),
    ("GPT-4.1 mini & Model rule (header) & $53$ & $2$ ($1$) & $264 = 172 + 92$ & $319$ & $226$ \\\\", "GPT-4.1 mini & Model rule (header) & $53$ & $2$ ($1$) & $265 = 172 + 93$ & $320$ & $226$ \\\\"),
    ("GPT-4.1 mini & Model rule (tagged) & $53$ & $2$ ($1$) & $264 = 172 + 92$ & $319$ & $226$ \\\\", "GPT-4.1 mini & Model rule (tagged) & $53$ & $2$ ($1$) & $265 = 172 + 93$ & $320$ & $226$ \\\\"),
    ("Haiku 4.5 & Model rule (header) & $64$ & $16$ ($1$) & $291 = 172 + 119$ & $371$ & $251$ \\\\", "Haiku 4.5 & Model rule (header) & $64$ & $16$ ($1$) & $292 = 172 + 120$ & $372$ & $251$ \\\\"),
    ("Haiku 4.5 & Lookup rule (header) & $58$ & $17$ ($1$) & $304 = 174 + 130$ & $379$ & $248$ \\\\", "Haiku 4.5 & Lookup rule (header) & $58$ & $17$ ($1$) & $303 = 174 + 129$ & $378$ & $248$ \\\\"),
    ("Haiku 4.5 & Model rule, all states (header) & $64$ & $21$ ($2$) & $291 = 172 + 119$ & $376$ & $255$ \\\\", "Haiku 4.5 & Model rule, all states (header) & $64$ & $21$ ($2$) & $292 = 172 + 120$ & $377$ & $255$ \\\\"),
    ("Haiku 4.5 & Lookup rule, all states (header) & $58$ & $19$ ($2$) & $304 = 174 + 130$ & $381$ & $249$ \\\\", "Haiku 4.5 & Lookup rule, all states (header) & $58$ & $19$ ($2$) & $303 = 174 + 129$ & $380$ & $249$ \\\\"),
    ("Haiku 4.5 & Model rule (tagged) & $64$ & $22$ ($1$) & $291 = 172 + 119$ & $377$ & $257$ \\\\", "Haiku 4.5 & Model rule (tagged) & $64$ & $22$ ($1$) & $292 = 172 + 120$ & $378$ & $257$ \\\\"),
    ("Haiku 4.5 & Lookup rule (tagged) & $58$ & $22$ ($1$) & $304 = 174 + 130$ & $384$ & $253$ \\\\", "Haiku 4.5 & Lookup rule (tagged) & $58$ & $22$ ($1$) & $303 = 174 + 129$ & $383$ & $253$ \\\\"),
    ("Haiku 4.5 & Model rule, all states (tagged) & $64$ & $26$ ($2$) & $291 = 172 + 119$ & $381$ & $260$ \\\\", "Haiku 4.5 & Model rule, all states (tagged) & $64$ & $26$ ($2$) & $292 = 172 + 120$ & $382$ & $260$ \\\\"),
    ("Haiku 4.5 & Lookup rule, all states (tagged) & $58$ & $24$ ($2$) & $304 = 174 + 130$ & $386$ & $254$ \\\\", "Haiku 4.5 & Lookup rule, all states (tagged) & $58$ & $24$ ($2$) & $303 = 174 + 129$ & $385$ & $254$ \\\\"),
]
for old, new in ROWS:
    rep(X, old, new)
# the caption's proxy clause
rep(X, "(the Amendment 6 answers under the header; the absent items a gated rule answers on a longer view, ten under the model rule, seventeen under the lookup rule and seventy-two under the literal rule, are read on the five-line view as a proxy)",
    "(the Amendment 6 answers under the header; the absent items a gated rule answers on a longer view, ten under the model rule, seventeen under the lookup rule and seventy-two under the literal rule, are read on that longer view, answered under the same header prompt after the registration, $99$ distinct views per answerer; read on the five-line view as a proxy instead, every composite is within one of the value printed)")
# the table's header comment
rep(X, "%% R110: the obligation-reported detector and the composite (DS Amendment 7; reviews/v18/src/amend7_e10.tex; AUX-DS-A7-*; D-DS-A7-1).\n",
    "%% R110: the obligation-reported detector and the composite (DS Amendment 7; reviews/v18/src/amend7_e10.tex; AUX-DS-A7-*; D-DS-A7-1).\n"
    "%% R114 (2026-09-17): the absent items the gated rules answer on a longer view are read on that view's own answer (ds_downstream/NUMBERS_DS.md section 14, AUX-DS-R114-COMPOSITE-ACTUAL, -ACTUAL-DIFF; 99 distinct views per answerer); the five-line proxy (AUX-DS-A7-COMPOSITE-ANSWERED) stands in the ledger beside it, every composite within one.\n")
# the prose
rep(X, "Under the header prompt the composite under the model rule minus under retrieval alone is $+18$ of $661$ for GPT-4.1 mini, a rate difference of $+0.03$ with intervals $[+0.01,+0.04]$ at item level and $[+0.01,+0.04]$ grouped by persona, and $+2$ for Haiku~4.5 ($+0.00$, $[-0.01,+0.02]$ and $[-0.01,+0.02]$); the lookup rule reads $+25$ ($+0.04$, reliable) and $+10$ ($+0.02$, both intervals including zero).",
    "Under the header prompt the composite under the model rule minus under retrieval alone is $+19$ of $661$ for GPT-4.1 mini, a rate difference of $+0.03$ with intervals $[+0.01,+0.05]$ at item level and $[+0.01,+0.05]$ grouped by persona, and $+3$ for Haiku~4.5 ($+0.00$, $[-0.01,+0.02]$ and $[-0.01,+0.02]$); the lookup rule reads $+25$ ($+0.04$, reliable) and $+9$ ($+0.01$, both intervals including zero).")
rep(X, "the rule adds $23$ and $11$ to those, and the licensed component falls by $3$ and $9$ where the rule abstains on a licensed item.",
    "the rule adds $24$ and $12$ to those, and the licensed component falls by $3$ and $9$ where the rule abstains on a licensed item.")


# ---------------------------------------------------------------- (2) Opus 5 on the moved-count control (AUX-V2RCAT-OP5), filled from the scores file
def opus_edits():
    S = json.load(open(ROOT / "r82_counterfactual/v2rcat/results/scores_v2rcat_op5.json", encoding="utf-8"))["opus"]
    f2 = lambda x: f"{x:+.2f}"                                   # noqa: E731
    f4 = lambda x: f"{x:.4f}"                                    # noqa: E731
    s4 = lambda x: f"{x:+.4f}"                                   # noqa: E731
    def iv(d):
        return f"$[{d['item_ci']['ci_lo']:+.4f},{d['item_ci']['ci_hi']:+.4f}]$; $[{d['persona_ci']['ci_lo']:+.4f},{d['persona_ci']['ci_hi']:+.4f}]$"
    W, R, Ex = S["minus_v2"], S["per_state"]["RETRACTION"], S["per_state"]["EXPIRY"]
    ret_d, exp_d = R["delta"], Ex["delta"]

    def direction(R, Ex):
        def excl(d):
            return (d["item_ci"]["ci_hi"] < 0 and d["persona_ci"]["ci_hi"] < 0) or (d["item_ci"]["ci_lo"] > 0 and d["persona_ci"]["ci_lo"] > 0)
        down = ret_d < 0 and exp_d < 0; up = ret_d > 0 and exp_d > 0
        dirw = "downward, the direction a count reader falls" if down else ("upward" if up else "in opposite directions")
        if excl(R) and excl(Ex):
            return f"{dirw}, with each interval excluding zero" + (" but reaching the band" if not (R["beyond_band_both"] and Ex["beyond_band_both"]) else " and clearing the band")
        if not excl(R) and not excl(Ex):
            return f"{dirw}, with each interval including zero"
        return f"{dirw}, the intervals in the table"
    # body: Section 5's sentence
    rep(B, "GPT-4.1 mini moves $+0.06$ on expiry with interval $[-0.04,+0.16]$ and Haiku 4.5 stays within tolerance (Appendix~\\ref{app:counterfactual}); Opus 5 was not run on this control.",
        f"GPT-4.1 mini moves $+0.06$ on expiry with interval $[-0.04,+0.16]$ and Haiku 4.5 stays within tolerance (Appendix~\\ref{{app:counterfactual}}). Opus 5, run once per item after this draft against its five-draw row, moves ${f2(ret_d)}$ on retraction and ${f2(exp_d)}$ on expiry.")
    rep(B, "%% R112 (2026-09-16), review-2 item E (the author's form, one interval in prose under Q-B): AUX-V2RCAT-MINI expiry +0.0611 [-0.0404, +0.1641] / [-0.0217, +0.1417]; Haiku 4.5 -0.0072 / -0.0453; Opus 5 not run.\n",
        "%% R112 (2026-09-16), review-2 item E (the author's form, one interval in prose under Q-B): AUX-V2RCAT-MINI expiry +0.0611 [-0.0404, +0.1641] / [-0.0217, +0.1417]; Haiku 4.5 -0.0072 / -0.0453; Opus 5 not run.\n"
        f"%% R114 (2026-09-17): the optional Opus 5 lane run at k = 1 under the author's instruction (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 8, AUX-V2RCAT-OP5; D-V2RCAT-2): retraction {s4(ret_d)}, expiry {s4(exp_d)} against the recorded k = 5 row; the section 5 branch wording for three models is the author's.\n")
    # appendix: the prose and the rows
    rep(X, "Read after the fact against the direction a count reader falls, and labelled so: GPT-4.1 mini moves by $+0.0269$ on retraction and $+0.0611$ on expiry, upward, with both intervals including zero, and Haiku 4.5 by $-0.0072$ and $-0.0453$, so no model followed the count.",
        f"Read after the fact against the direction a count reader falls, and labelled so: GPT-4.1 mini moves by $+0.0269$ on retraction and $+0.0611$ on expiry, upward, with both intervals including zero, and Haiku 4.5 by $-0.0072$ and $-0.0453$, so no model followed the count. Opus 5, the optional lane, was run after this draft once per item ($k=1$, the registered default) against its recorded five-draw superseded-only row. It moves by ${s4(ret_d)}$ on retraction and ${s4(exp_d)}$ on expiry, {direction(R, Ex)}. The unchanged supersession texts move by ${s4(S['per_state']['SUPERSESSION']['delta'])}$ under the same single draw, which carries draw-count noise against the five-draw row that the two registered lanes did not.")
    rep(X, "Haiku 4.5 & expiry ($30$ pairs) & $0.5794$ & $0.5342$ & $-0.0453$ $[-0.0958,+0.0014]$; $[-0.0781,-0.0169]$ \\\\\n\\addlinespace",
        "Haiku 4.5 & expiry ($30$ pairs) & $0.5794$ & $0.5342$ & $-0.0453$ $[-0.0958,+0.0014]$; $[-0.0781,-0.0169]$ \\\\\n"
        f"Opus 5 ($k=1$ vs.\\ $k=5$) & whole set & ${f4(S['v2_recorded'])}$ & ${f4(S['v2rcat'])}$ & ${s4(W['delta'])}$ {iv(W)} \\\\\n"
        f"Opus 5 & retraction ($30$ pairs) & ${f4(R['v2'])}$ & ${f4(R['v2rcat'])}$ & ${s4(ret_d)}$ {iv(R)} \\\\\n"
        f"Opus 5 & expiry ($30$ pairs) & ${f4(Ex['v2'])}$ & ${f4(Ex['v2rcat'])}$ & ${s4(exp_d)}$ {iv(Ex)} \\\\\n"
        "\\addlinespace")
    # the spend sentence (Appendix E.11): the two runs this pass lands
    DOC = json.load(open(ROOT / "r82_counterfactual/v2rcat/results/scores_v2rcat_op5.json", encoding="utf-8"))
    usd_all = DOC["spend"]["total"]
    rep(X, "the forty-persona Graphiti ingestion $11.88$ of a $13.22$ stop, twelve aborted partial runs included (Appendix~\\ref{app:posthoc-graphiti}).",
        f"the forty-persona Graphiti ingestion $11.88$ of a $13.22$ stop, twelve aborted partial runs included (Appendix~\\ref{{app:posthoc-graphiti}}); two runs after this draft, the composite's answers on the actual expanded views $0.14$ and Opus 5 on the moved-count control ${usd_all:.2f}$, under a $40$ ceiling for that pass.")
    rep(X, "%% R110: ADDENDUM_V2R_CAT (frozen 257a090; r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md AUX-V2RCAT-LOCK, -REF, -LEAK, -MINI, -H45, -BRANCH, -POSTHOC; D-V2RCAT-1).\n",
        "%% R110: ADDENDUM_V2R_CAT (frozen 257a090; r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md AUX-V2RCAT-LOCK, -REF, -LEAK, -MINI, -H45, -BRANCH, -POSTHOC; D-V2RCAT-1).\n"
        "%% R114 (2026-09-17): the optional Opus 5 lane (k = 1, Batch; AUX-V2RCAT-OP5, D-V2RCAT-2) added to the prose and tab:v2rcat beside the two registered lanes; the recorded comparator is the k = 5 row.\n")


def main():
    if "--no-opus" not in sys.argv:
        opus_edits()
    files = {p: p.read_text(encoding="utf-8") for p in (B, X)}
    for f, old, new in E:
        n = files[f].count(old)
        if n != 1:
            print(f"ABORT {f.name}: {n} of {old[:120]!r}"); sys.exit(1)
        files[f] = files[f].replace(old, new)
    for p, t in files.items():
        p.write_text(t, encoding="utf-8", newline="\n")
    print(f"applied {len(E)}")


if __name__ == "__main__":
    main()
