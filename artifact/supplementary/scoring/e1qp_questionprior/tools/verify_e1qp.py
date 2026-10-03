"""verify_e1qp.py -- two-direction verifier over E1-QP. NO API CALLS.

Direction A — REDERIVE: recompute the probe AUROCs and every matched-contrast cell
from the committed artifacts by an INDEPENDENT path (brute-force pairwise
concordance, and a collapse rebuilt from raw rows), and check the gates follow
mechanically.

Direction B — ACCOUNT: every decimal in NUMBERS_E1QP.md must exist in the scores
JSON or be a DECLARED cross-reference.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
QP = ROOT / "e1qp_questionprior"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from qp_common import population, matched_slice, strict_slice, model_scores  # noqa: E402

fails, checks = [], 0


def chk(name, got, want, tol=1e-9):
    global checks
    checks += 1
    ok = (got is None and want is None) or abs(float(got) - float(want)) <= tol
    if not ok:
        fails.append(f"{name}: rederived {got} != reported {want}")
    print(f"  {'ok  ' if ok else 'FAIL'} {name:54s} "
          f"{('None' if got is None else f'{float(got):>10.6f}')} vs "
          f"{('None' if want is None else f'{float(want):>10.6f}')}")


def chk_eq(name, got, want):
    global checks
    checks += 1
    ok = got == want
    if not ok:
        fails.append(f"{name}: rederived {got!r} != reported {want!r}")
    print(f"  {'ok  ' if ok else 'FAIL'} {name:54s} {str(got):>10s} vs {str(want):>10s}")


def auroc_bf(s, y):
    pos = [a for a, b in zip(s, y) if b == 1]
    neg = [a for a, b in zip(s, y) if b == 0]
    if not pos or not neg:
        return float("nan")
    return sum(1.0 if p > n else (0.5 if p == n else 0.0)
               for p in pos for n in neg) / (len(pos) * len(neg))


def main():
    S = json.load(io.open(QP / "results" / "e1qp_scores.json", encoding="utf-8"))
    T = json.load(io.open(QP / "results" / "probe_tfidf.json", encoding="utf-8"))["probes"]
    L = json.load(io.open(QP / "results" / "probe_llm.json", encoding="utf-8"))["probes"]

    print("DIRECTION A -- rederive")
    # populations
    P1, P2 = population("P1"), population("P2")
    chk_eq("P1 size", len(P1), 84)
    chk_eq("P2 size", len(P2), 307)
    chk_eq("P1 PN count", sum(r["y_nok"] for r in P1), 40)
    chk_eq("P2 PN count", sum(r["y_nok"] for r in P2), 35)
    chk_eq("P2 is PN-vs-ABSENT only (no other label)",
           {r["label"] for r in P2}, {"ABSENT", "PRESENT-NEGATIVE"})
    chk_eq("P2 matched slice size", len(matched_slice(P2)), 162)
    chk_eq("P1 matched slice size", len(matched_slice(P1)), 49)
    chk_eq("P1 strict slice size", len(strict_slice(P1)), 21)
    # every probe input is a question string only
    chk_eq("no probe input carries store text (all inputs are questions)",
           all(isinstance(r["question"], str) and r["question"] for r in P1 + P2), True)

    # LLM probe AUROC rederived from the raw jsonl
    vals = {}
    for ln in io.open(QP / "results" / "probe_llm_raw.jsonl", encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            vals[r["item_id"]] = r.get("pn_likelihood")
    for pn, pop in (("P1", P1), ("P2", P2)):
        rs = [r for r in pop if vals.get(r["item_id"]) is not None]
        chk(f"LLM {pn} full y_nok AUROC",
            auroc_bf([vals[r["item_id"]] for r in rs], [r["y_nok"] for r in rs]),
            L[f"{pn}:full:y_nok"]["auroc"], 1e-9)

    # ceilings follow mechanically
    for pn in ("P1", "P2"):
        c = S["ceilings"][pn]
        chk(f"CEILING({pn}) = max(tfidf, llm)", max(c["tfidf"], c["llm"]), c["ceiling"])
        chk(f"  tfidf({pn}) matches probe file", T[f"{pn}:full:PN-vs-rest"]["auroc"], c["tfidf"])
        chk(f"  llm({pn}) matches probe file", L[f"{pn}:full:y_nok"]["auroc"], c["llm"])

    # matched contrast rederived by an independent path
    M = model_scores()
    slices = {"P1:matched": matched_slice(P1), "P2:matched": matched_slice(P2)}
    for m, cells in S["matched_contrast"].items():
        for nm, rows in slices.items():
            c = cells.get(nm)
            if not c or "note" in c:
                continue
            tags = [r["item_id"] for r in rows
                    if (r["item_id"], "BLIND") in M[m] and (r["item_id"], "INDEXED-TRUE") in M[m]
                    and M[m][(r["item_id"], "BLIND")].get("nok") is not None
                    and M[m][(r["item_id"], "INDEXED-TRUE")].get("nok") is not None]
            idx = {r["item_id"]: r for r in rows}
            y = [idx[t]["y_nok"] for t in tags]
            b = [M[m][(t, "BLIND")]["nok"] for t in tags]
            i = [M[m][(t, "INDEXED-TRUE")]["nok"] for t in tags]
            chk_eq(f"{m[:18]} {nm} n", len(tags), c["n"])
            chk(f"{m[:18]} {nm} blind", auroc_bf(b, y), c["blind"], 1e-9)
            chk(f"{m[:18]} {nm} indexed", auroc_bf(i, y), c["indexed"], 1e-9)
            chk_eq(f"{m[:18]} {nm} distinct_blind", len(set(b)), c["distinct_blind"])

    print("\n  [gates read mechanically]")
    C1 = S["ceilings"]["P1"]["ceiling"]
    for m, v in S["QP-1"]["per_model"].items():
        chk_eq(f"QP-1 {m[:22]} holds iff not entirely above ceiling",
               not (v["blind_nok"] > C1 and v["ci"] is not None and v["ci"][0] > C1),
               v["HOLDS"])
    chk_eq("QP-2 holds iff powered-population CI includes 0.50",
           bool(T["P2:matched:PN-vs-slotablated"]["includes_0.50"]), S["QP-2"]["HOLDS"])
    q3 = S["QP-3"]["cell"]
    chk_eq("QP-3 holds iff indexed excludes 0.50 and blind includes it",
           bool(q3["indexed_includes_0.50"] is False and q3["blind_includes_0.50"] is True),
           S["QP-3"]["HOLDS"])
    chk_eq("QP-3 degeneracy flag is carried",
           bool(q3["distinct_blind"] <= 2 or q3["blind_modal_share"] >= 0.95),
           S["QP-3"]["blind_near_degenerate"])

    print("\nDIRECTION B -- every figure in NUMBERS_E1QP.md is accounted for")
    nums = QP / "NUMBERS_E1QP.md"
    flat = set()

    def walk(o):
        if isinstance(o, dict):
            [walk(v) for v in o.values()]
        elif isinstance(o, list):
            [walk(v) for v in o]
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            for x in (float(o), abs(float(o)), float(o) * 100, abs(float(o)) * 100):
                flat.add(round(x, 4)); flat.add(round(x, 2))
    walk(S); walk(T); walk(L)
    CROSSREF = {
        4.1: "version string in the model name gpt-4.1-mini",
        4.5: "version string in the model name Claude Haiku 4.5",
        5.6: "version string in the model names gpt-5.6-luna / gpt-5.6-sol",
        2.0: "the $2 cap on the LLM classifier arm, PREREG section 8",
    }
    txt = io.open(nums, encoding="utf-8").read()
    cited = {round(abs(float(m.group())), 4)
             for m in re.finditer(r"(?<![\w.])[-+]?\d+\.\d+(?![\w])", txt)}
    unacc, crossed = [], []
    for x in sorted(cited):
        if any(abs(x - f) <= 1e-4 for f in flat):
            continue
        (crossed if any(abs(x - c) <= 1e-4 for c in CROSSREF) else unacc).append(x)
    for u in unacc:
        fails.append(f"NUMBERS_E1QP.md cites {u}, absent from the scores")
    print(f"  cited decimals {len(cited)}   from this run "
          f"{len(cited) - len(crossed) - len(unacc)}   declared cross-refs {len(crossed)}"
          f"   unaccounted {len(unacc)}")
    if unacc:
        print(f"    UNACCOUNTED -> {unacc}")

    print(f"\n{checks} checks, {len(fails)} failures")
    if fails:
        for f in fails:
            print("  FAIL:", f)
        raise SystemExit(1)
    print("VERIFIER PASSES -- both directions clean.")


if __name__ == "__main__":
    main()
