"""ledger_nb6sweep.py -- NUMBERS_NB6SWEEP.md: the ledger keys the paper prints from the post hoc nb6 sweep
(nb6_sweep/REPORT.md sections 6 and 7; results/step4_recall.json). NO MODEL CALL, NO RECOMPUTATION: every value is
read from the committed artifact and printed at four decimals, with the two-decimal and tenths forms the paper uses
listed beside their sources (the R97/R102 printed-forms convention).

Keys
  AUX-NB6SWEEP-DECOMP-444   the three-factor Shapley decomposition of the superseded-names lookup's loss on the
                            counterfactual set (v2 summary, embedding, whole set), faults at the real backend's measured
                            rates: length 15, contamination 0.232, TRUE-name recall 0.3604 (marker-corrected) and 0.2996
  AUX-NB6SWEEP-DECOMP-661   the same on the 661 obligation questions (TRUE summary), where the real backend's row lives
  AUX-NB6SWEEP-BELIEVED     the measured properties of the real backend's list the corners were set from
  AUX-NB6SWEEP-PRINTED      the printed forms

Usage: python nb6_sweep/tools/ledger_nb6sweep.py   -> nb6_sweep/NUMBERS_NB6SWEEP.md
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
NB6 = ROOT / "nb6_sweep"
SRC = NB6 / "results" / "step4_recall.json"
OUT = NB6 / "NUMBERS_NB6SWEEP.md"
MEASURES = (("emb", "embedding lookup, whole set"), ("emb_sup", "embedding lookup, supersession slice"),
            ("lex", "lexical lookup, whole set"), ("lex_sup", "lexical lookup, supersession slice"))
BELIEVED = {"length_rendered": 15.04, "length_uncapped": 32.55, "recall_marker_corrected": 0.3604, "recall_ledger": 0.2996,
            "contamination": 0.232, "emb": 0.5858, "lex": 0.4718}   # nb6_sweep/REPORT.md section 7, the measured BELIEVED list


def tenths(x):
    """A share as 'about N tenths' (rounded to the nearest tenth); negative shares print as a credit."""
    W = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    n = round(x * 10)
    if n < 0:
        return f"a credit of about {W[-n]} tenth{'s' if -n != 1 else ''}"
    return f"about {W[n]} tenth{'s' if n != 1 else ''}"


def main():
    d = json.load(io.open(SRC, encoding="utf-8"))
    sha = hashlib.sha256(SRC.read_bytes()).hexdigest()[:16]
    L = ["# NUMBERS_NB6SWEEP.md — the post hoc nb6 sweep's ledger keys (written 2026-09-14, R106; `tools/ledger_nb6sweep.py`)\n",
         f"\nSource `results/step4_recall.json` (sha256 `{sha}…`; seed {d['seed']}), the artifact `nb6_sweep/REPORT.md` sections 6 and 7 print. "
         "Post hoc: the sweep was run after every registered result was known and carries no prediction (its section 0 prediction concerned the "
         "reconstruction cell and is reported in the REPORT). Four decimals here; the paper's two-decimal and tenths forms are in AUX-NB6SWEEP-PRINTED.\n",
         "\nThe decomposition: eight corners on each population, length in {base, 15}, contamination in {base, 0.232}, TRUE-name recall in {1.0, r}; "
         "the Shapley value of each factor averages its marginal contribution over the six orderings and the three sum to the total gap; the share is the "
         "Shapley value over the total gap. Inside a cell the order is recall drop, then injection, then padding.\n"]
    for pop, key, title in (("cf2", "AUX-NB6SWEEP-DECOMP-444", "the counterfactual set, 444 items, v2 summary"),
                            ("661", "AUX-NB6SWEEP-DECOMP-661", "the 661 obligation questions, TRUE summary")):
        P = d["cells"][pop]["partition"]
        L.append(f"\n## {key} — {title}\n")
        for r in ("0.3604", "0.2996"):
            L.append(f"\n**r = {r}** ({'marker-corrected BELIEVED recall' if r == '0.3604' else 'the ledger recall, marker in the denominator'}).\n\n")
            L.append("| measure | base → full | total gap | Δ length alone | Δ contamination alone | Δ recall alone | interaction | Shapley L | Shapley c | Shapley r | share L | share c | share r |\n"
                     "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
            for m, name in MEASURES:
                x = P[r][m]; s, sh, ss = x["single_factor_deltas"], x["shapley"], x["shapley_share"]
                L.append(f"| {name} | {x['base']:.4f} → {x['full']:.4f} | {x['total_gap']:+.4f} | {s['L']:+.4f} | {s['c']:+.4f} | {s['r']:+.4f} | {x['interaction']:+.4f} | "
                         f"{sh['L']:+.4f} | {sh['c']:+.4f} | {sh['r']:+.4f} | {ss['L']:.4f} | {ss['c']:.4f} | {ss['r']:.4f} |\n")
    L.append("\n## AUX-NB6SWEEP-BELIEVED — the measured properties of the real backend's superseded-names list (REPORT section 7)\n\n")
    L.append("| property | value |\n|---|---:|\n")
    for k, v in BELIEVED.items():
        L.append(f"| {k} | {v} |\n")
    e444 = d["cells"]["cf2"]["partition"]["0.3604"]["emb"]["shapley_share"]; e661 = d["cells"]["661"]["partition"]["0.3604"]["emb"]["shapley_share"]
    L.append("\n## AUX-NB6SWEEP-PRINTED — the printed forms\n\n| printed | source |\n|---|---|\n")
    L.append(f"| missing names {tenths(e444['r'])}, wrong names {tenths(e444['c'])}, list length {tenths(e444['L'])} of the lookup's loss | "
             f"AUX-NB6SWEEP-DECOMP-444, r = 0.3604, embedding whole set: shares r {e444['r']:.4f}, c {e444['c']:.4f}, L {e444['L']:.4f} |\n")
    L.append(f"| on the 661: missing names {tenths(e661['r'])}, wrong names {tenths(e661['c'])}, length {tenths(e661['L'])} | "
             f"AUX-NB6SWEEP-DECOMP-661, r = 0.3604, embedding whole set: shares r {e661['r']:.4f}, c {e661['c']:.4f}, L {e661['L']:.4f} |\n")
    x = d["cells"]["cf2"]["partition"]["0.3604"]["emb"]
    L.append(f"| $0.77$ to $0.50$ | {x['base']:.4f} → {x['full']:.4f} (AUX-NB6SWEEP-DECOMP-444, embedding whole set, the base corner and the full-fault corner) |\n")
    y = d["cells"]["661"]["partition"]["0.3604"]["emb"]
    L.append(f"| $0.74$ to $0.61$ | {y['base']:.4f} → {y['full']:.4f} (AUX-NB6SWEEP-DECOMP-661, embedding whole set) |\n")
    L.append("| $15$ names, recall $0.36$, contamination $0.23$ | AUX-NB6SWEEP-BELIEVED: 15.04, 0.3604, 0.232 |\n")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("".join(L))
    print("wrote", OUT)
    print("444 shares", {k: round(v, 4) for k, v in e444.items()}, "661 shares", {k: round(v, 4) for k, v in e661.items()})


if __name__ == "__main__":
    main()
