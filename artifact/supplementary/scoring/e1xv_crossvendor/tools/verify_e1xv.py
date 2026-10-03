"""verify_e1xv.py -- two-direction verifier over the E1-XV rows. NO API CALLS.

Direction A — REDERIVE. Every headline figure in `results/e1xv_scores.json` is
recomputed from the raw JSONL by an INDEPENDENT path: the per-item collapse is
rebuilt from scratch, and AUROC is computed by BRUTE-FORCE PAIRWISE CONCORDANCE
(count every positive/negative pair, half-credit on ties) rather than the committed
scorer's rank-sum form. Two different algorithms agreeing to 1e-9 is evidence the
number is right, not merely reproducible.

Direction B — ACCOUNT. Every decimal that appears in `NUMBERS_E1XV.md` must exist
in the scores JSON, so the write-up cannot carry a figure the scoring did not
produce. Legitimate outside references must be DECLARED, not tolerated by loosening
the regex.

Exits non-zero on any mismatch.
"""
from __future__ import annotations

import io
import json
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
XV = ROOT / "e1xv_crossvendor"

TOL = 1e-9
MIN_DRAWS, K = 3, 5
ARMS = ["BLIND", "INDEXED-TRUE"]
fails, checks = [], 0


def chk(name, got, want, tol=TOL):
    global checks
    checks += 1
    ok = (got is None and want is None) or abs(float(got) - float(want)) <= tol
    if not ok:
        fails.append(f"{name}: rederived {got} != reported {want}")
    g = "None" if got is None else f"{float(got):>10.6f}"
    w = "None" if want is None else f"{float(want):>10.6f}"
    print(f"  {'ok  ' if ok else 'FAIL'} {name:56s} {g} vs {w}")


def chk_eq(name, got, want):
    global checks
    checks += 1
    ok = got == want
    if not ok:
        fails.append(f"{name}: rederived {got!r} != reported {want!r}")
    print(f"  {'ok  ' if ok else 'FAIL'} {name:56s} {str(got):>10s} vs {str(want):>10s}")


def auroc_bruteforce(s, y):
    """Independent path: every pos/neg pair, half-credit on ties."""
    pos = [a for a, b in zip(s, y) if b == 1]
    neg = [a for a, b in zip(s, y) if b == 0]
    if not pos or not neg:
        return float("nan")
    tot = 0.0
    for p in pos:
        for n in neg:
            tot += 1.0 if p > n else (0.5 if p == n else 0.0)
    return tot / (len(pos) * len(neg))


def main():
    S = json.load(io.open(XV / "results" / "e1xv_scores.json", encoding="utf-8"))

    print("DIRECTION A -- rederive from raw rows, independent collapse + brute-force AUROC")
    for model, rep in S["lineages"].items():
        print(f"\n  [{model}]")
        seen, rows = set(), []
        for ln in io.open(XV / "rows" / f"elicitation_{model}.jsonl", encoding="utf-8"):
            if not ln.strip():
                continue
            r = json.loads(ln)
            k = (r["item_id"], r["arm"], r["draw"], r["prompt_hash"])
            if k in seen:
                continue
            seen.add(k); rows.append(r)
        chk_eq(f"{model} n_rows", len(rows), rep["n_rows"])

        # every row must carry the model it claims
        bad = {r["served_model"] for r in rows if r["served_model"]
               and r["served_model"] != model}
        chk_eq(f"{model} no foreign served_model", bad, set())

        # parse counts per arm
        for arm in ARMS:
            rs = [r for r in rows if r["arm"] == arm]
            f = sum(1 for r in rs if not r["parsed"])
            chk_eq(f"{model} {arm} parse_fail", f, rep["parse"][arm]["parse_fail"])
            chk(f"{model} {arm} fail_rate", f / len(rs) if rs else None,
                rep["parse"][arm]["fail_rate"], 1e-12)
            chk_eq(f"{model} {arm} FLAGGED(>5%)",
                   (f / len(rs) > 0.05) if rs else False, rep["parse"][arm]["FLAGGED"])

        # independent collapse
        acc, meta = {}, {}
        for r in rows:
            meta[r["item_id"]] = (r["y_fok"], r["y_nok"])
            if r["parsed"] and r["fok"] is not None:
                acc.setdefault((r["item_id"], r["arm"]), []).append(r)
        keep = {k: v for k, v in acc.items() if len(v) >= MIN_DRAWS}
        chk_eq(f"{model} n_excluded (arm-cells below MIN_DRAWS)",
               len(meta) * 2 - len(keep), rep["n_excluded"])

        for j, yi in (("fok", 0), ("nok", 1)):
            c = rep[j.upper()]
            if "note" in c:
                continue
            tags = sorted({t for (t, a) in keep
                           if (t, "BLIND") in keep and (t, "INDEXED-TRUE") in keep})
            def m(t, arm):
                vals = [x[j] for x in keep[(t, arm)] if x[j] is not None]
                return st.mean(vals) if vals else None
            tags = [t for t in tags
                    if m(t, "BLIND") is not None and m(t, "INDEXED-TRUE") is not None]
            y = [meta[t][yi] for t in tags]
            b = [m(t, "BLIND") for t in tags]
            i = [m(t, "INDEXED-TRUE") for t in tags]
            chk_eq(f"{model} {j.upper()} n", len(tags), c["n"])
            chk_eq(f"{model} {j.upper()} n_pos", int(sum(y)), c["n_pos"])
            chk(f"{model} {j.upper()} blind AUROC", auroc_bruteforce(b, y), c["blind"], 1e-9)
            chk(f"{model} {j.upper()} indexed AUROC", auroc_bruteforce(i, y), c["indexed"], 1e-9)
            chk(f"{model} {j.upper()} delta",
                auroc_bruteforce(i, y) - auroc_bruteforce(b, y), c["delta"], 1e-9)
            chk_eq(f"{model} {j.upper()} tie_degenerate",
                   len(set(b)) == 1, c["tie_degenerate"])
            # CI consistency: the reported point must sit inside its own interval
            for nm, pt, ci in ((f"{j.upper()} blind", c["blind"], c["blind_ci"]),
                               (f"{j.upper()} indexed", c["indexed"], c["indexed_ci"]),
                               (f"{j.upper()} delta", c["delta"], c["delta_ci"])):
                global checks
                checks += 1
                ok = ci[0] - 1e-9 <= pt <= ci[1] + 1e-9
                if not ok:
                    fails.append(f"{model} {nm}: point {pt} outside CI {ci}")
                print(f"  {'ok  ' if ok else 'FAIL'} {model} {nm} point inside its CI"
                      f"{'':10s} {pt:+.4f} in [{ci[0]:+.4f}, {ci[1]:+.4f}]")

    # ---- the registered gates must follow mechanically from the numbers
    print("\n  [registered gates read mechanically]")
    L, PR = S["lineages"], S["predictions"]
    for mdl, v in PR["XV-1"]["per_model"].items():
        chk_eq(f"XV-1 {mdl} = blind NOK CI includes 0.50",
               bool(L[mdl]["NOK"]["blind_includes_0.50"]), v)
    for mdl, v in PR["XV-2"]["per_model"].items():
        chk_eq(f"XV-2 {mdl} = delta>0 and CI excludes 0",
               bool(L[mdl]["NOK"]["delta"] > 0 and L[mdl]["NOK"]["delta_excludes_zero"]), v)
    chk_eq("XV-3 = opus5 blind FOK > haiku blind FOK",
           L["claude-opus-5"]["FOK"]["blind"] > L["claude-haiku-4-5-20251001"]["FOK"]["blind"],
           PR["XV-3"]["HOLDS"])
    lo, hi = S["xv4_window"]
    for mdl, v in PR["XV-4"]["per_model"].items():
        chk_eq(f"XV-4 {mdl} in window", bool(lo <= L[mdl]["FOK"]["indexed"] <= hi), v)
    chk_eq("XV-5 reports iff XV-1 holds on kimi-k3",
           bool(PR["XV-1"]["per_model"]["kimi-k3"]), PR["XV-5"]["reports"])
    chk_eq("paper pre-commitment = XV-1 and XV-2 on both frontier lineages",
           bool(all(PR["XV-1"]["per_model"][m] for m in ("claude-opus-5", "kimi-k3"))
                and all(PR["XV-2"]["per_model"].values())),
           S["paper_precommitment_met"])

    # ---- Direction B
    print("\nDIRECTION B -- every figure in NUMBERS_E1XV.md is accounted for")
    nums = XV / "NUMBERS_E1XV.md"
    if nums.exists():
        flat = set()

        def walk(o):
            if isinstance(o, dict):
                [walk(v) for v in o.values()]
            elif isinstance(o, list):
                [walk(v) for v in o]
            elif isinstance(o, (int, float)) and not isinstance(o, bool):
                for x in (float(o), abs(float(o)), float(o) * 100, abs(float(o)) * 100):
                    flat.add(round(x, 4)); flat.add(round(x, 2))
        walk(S)
        # Declared cross-references: figures the write-up legitimately cites that this
        # run did not produce. Named with their source so they stay visible.
        CROSSREF = {
            0.4488: "NUMBERS.md 9, gpt-4.1-mini blind FOK",
            0.7090: "NUMBERS.md 9, gpt-4.1-mini indexed FOK (also the XV-4 band floor)",
            0.5735: "NUMBERS.md 9, luna blind FOK", 0.7417: "NUMBERS.md 9, luna indexed FOK",
            0.7099: "NUMBERS.md 9, sol blind FOK", 0.7463: "NUMBERS.md 9, sol indexed FOK",
            0.5585: "NUMBERS.md 9, luna blind NOK", 0.8526: "NUMBERS.md 9, luna indexed NOK",
            0.5290: "NUMBERS.md 9, sol blind NOK", 0.8588: "NUMBERS.md 9, sol indexed NOK",
            0.7139: "NUMBERS.md 9, mini indexed NOK", 0.2139: "NUMBERS.md 9, mini NOK delta",
            0.2940: "NUMBERS.md 9, luna NOK delta", 0.3298: "NUMBERS.md 9, sol NOK delta",
            0.2602: "NUMBERS.md 9, mini FOK delta", 0.1682: "NUMBERS.md 9, luna FOK delta",
            0.0364: "NUMBERS.md 9, sol FOK delta",
            386.0: "PREREG_E1XV.md sha256 prefix 386d334",
            22.02: "PREREG_E1XV.md 7, projected run cost",
            28.00: "SP-0 ruling 1 cap", 1.1220: "billed before STEP 2",
            0.01197: "PREREG 7, opus-5 $/call", 0.00167: "PREREG 7, haiku $/call",
            0.01940: "PREREG 7, kimi-k3 $/call",
            # Model VERSION strings in prose, not measurements. Declared rather than
            # excused by loosening the regex, so they stay visible in the audit.
            4.1: "version string in the model name gpt-4.1-mini",
            4.5: "version string in the model name Claude Haiku 4.5",
            5.6: "version string in the model names gpt-5.6-luna / gpt-5.6-sol",
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
            fails.append(f"NUMBERS_E1XV.md cites {u}, absent from e1xv_scores.json")
        print(f"  cited decimals {len(cited)}   from this run "
              f"{len(cited) - len(crossed) - len(unacc)}   declared cross-refs "
              f"{len(crossed)}   unaccounted {len(unacc)}")
        if unacc:
            print(f"    UNACCOUNTED -> {unacc}")
    else:
        print("  NUMBERS_E1XV.md not present yet -- direction B skipped")

    print(f"\n{checks} checks, {len(fails)} failures")
    if fails:
        for f in fails:
            print("  FAIL:", f)
        raise SystemExit(1)
    print("VERIFIER PASSES -- both directions clean.")


if __name__ == "__main__":
    main()
