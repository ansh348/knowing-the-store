# -*- coding: utf-8 -*-
"""r133_number_gate.py -- the number gate of the R133 readability pass (2026-09-21; the author's brief 'R133: V23 READABILITY PASS', sections 2, 5 and 7):
every number the pass's new texts print (the abstract swaps S2 and S3, the Section 1 bullet S5, the Section 5 leads S7, the two worked examples of
section 7, Table 74's corrected first row) read from its artifact and compared at the printed precision (half-up on the recorded four-decimal value,
the convention of r131_number_gate.py), with the reliability each sentence claims; and, on a built paper_v23.tex, the pass's rule that no number
changes: every numeral of the v23 main text occurs in the v22 main text (nothing new is printed there) and the appendix's new numerals are exactly
the two of Table 74's corrected range. A mismatch is listed; nothing is adjusted; exit 1 on any mismatch (the hard stop of section 9).
Usage: python reviews/v23/tools/r133_number_gate.py [--built]     (--built adds the numeral-set checks on iclr2027_monitoring_submission/paper_v23.tex)
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
R125 = ROOT / "reviews" / "r125" / "results"
M = json.load(open(R125 / "r125_matched.json", encoding="utf-8"))
RD, PD, CT = M["readers"], M["paired"], M["paired"]["contrasts"]
E1R = (ROOT / "e1r_robustness" / "NUMBERS_E1R.md").read_text(encoding="utf-8", errors="replace")
R74 = (ROOT / "r74" / "NUMBERS_R74.md").read_text(encoding="utf-8", errors="replace")
BH = (ROOT / "believed_h" / "NUMBERS_BELIEVED_H.md").read_text(encoding="utf-8", errors="replace")
CF2 = (ROOT / "r82_counterfactual" / "cf2" / "NUMBERS_CF2.md").read_text(encoding="utf-8", errors="replace")
BASE = (ROOT / "reviews" / "v23" / "base_tree.txt").read_text().strip()
RESP = json.load(open(ROOT / "resp_review" / "run" / "scores_resp.json", encoding="utf-8"))["L2"]["arms"]["RETRIEVED"]   # AUX-RESP-L2-MINI-NOK


def r2s(x):
    """A signed two-decimal form (half-up on the four-decimal recorded value), as tab:routes prints its differences and intervals."""
    v = Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return ("+" if v >= 0 else "") + str(v)


def routes_rows():
    """The two per-state rows of tab:routes (R133 RULINGS 3): the tagged view under ground-truth tags minus the summary alone on that state's items
    (resp_review/run/scores_resp.json L2/arms/RETRIEVED/{expiry,supersession}; resp_review/NUMBERS_RESP.md AUX-RESP-L2-MINI-NOK), printed at two decimals.
    Returns (rows, tokens): the LaTeX rows and every printed numeral."""
    rows, toks = [], set()
    for state, label in (("expiry", "expiry"), ("supersession", "supersession")):
        d = RESP[state]
        arm, base, D = r2(d["arm"]), r2(d["base"]), r2s(d["D"])
        it = f"[{r2s(d['item']['ci_lo'])},{r2s(d['item']['ci_hi'])}]"
        pe = f"[{r2s(d['cluster']['ci_lo'])},{r2s(d['cluster']['ci_hi'])}]"
        rows.append(f"\\quad on {label}, {d['n_pos']} obligations & ${arm}$ & ${D}$ (the summary alone, ${base}$) & ${it}$ & ${pe}$ \\\\")
        toks |= {arm, base, D, r2s(d['item']['ci_lo']), r2s(d['item']['ci_hi']), r2s(d['cluster']['ci_lo']), r2s(d['cluster']['ci_hi']), str(d["n_pos"])}
    return rows, toks


CHECKS = []


def r2(x):
    return str(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def chk(where, printed, value, source, reliable=None, actual_reliable=None):
    ok = (r2(value) == printed) if isinstance(value, float) else (str(value) == str(printed))
    if reliable is not None:
        ok = ok and (bool(actual_reliable) == reliable)
    CHECKS.append(dict(where=where, printed=str(printed), value=value, source=source, reliable=reliable, actual_reliable=actual_reliable, ok=bool(ok)))


def e1r_row(label):
    """A row of NUMBERS_E1R.md section 11 (AUX-E1R-NB6): '| R-NOK-FRB | TRUE | 661 | 0.7339 | ... | **0.7484** | ...' -> (monitor, NB-6)."""
    sec = E1R[E1R.index("## 11. `AUX-E1R-NB6`"):E1R.index("## 12. ")]
    for ln in sec.splitlines():
        if ln.startswith(label) and "**" in ln:
            nums = [float(x) for x in re.findall(r"\d\.\d{4}", ln)]
            return nums[0], float(re.search(r"\*\*(\d\.\d{4})\*\*", ln).group(1))
    raise KeyError(label)


def hyb_vs_models():
    """AUX-CF2-HYB-VS-MODELS: 'Opus 5 (0.8405) minus the hybrid: +0.0540 ([+0.0061, +0.1004]; [+0.0188, +0.0888])' -> {model: (delta, both exclude zero)}."""
    sec = CF2[CF2.index("### AUX-CF2-HYB-VS-LOOKUP, AUX-CF2-HYB-VS-NB1, AUX-CF2-HYB-VS-MODELS"):CF2.index("### AUX-CF2-HYB-COEF")]
    out = {}
    for m in re.finditer(r"- (GPT-4\.1 mini|Haiku 4\.5|Opus 5|GPT-5\.6 Sol|GPT-5\.6 Luna) \([0-9.]+\) minus the hybrid: ([+-]\d\.\d{4}) \(\[([+-]\d\.\d{4}), ([+-]\d\.\d{4})\]; \[([+-]\d\.\d{4}), ([+-]\d\.\d{4})\]\)", sec):
        d, a, b, c, e = (float(x) for x in m.groups()[1:])
        out[m.group(1)] = (d, (a > 0 and c > 0) or (b < 0 and e < 0))
    assert len(out) == 5, out
    return out


def main():
    # ------------------------------------------------------------------ S3 (the abstract) and S5 (the third bullet): three readers under FR-Bank's metadata
    mini_true, lookup_true = e1r_row("| R-NOK-FRB | TRUE |")
    mini_bel, lookup_bel = e1r_row("| R-NOK-FRB | BELIEVED |")
    chk("S3/S5: mini under the ground-truth summary, full obligation set", "0.73", mini_true, "e1r_robustness/NUMBERS_E1R.md section 11 (AUX-E1R-TRUE-NOK) R-NOK-FRB TRUE, 661, monitor")
    chk("S3/S5: mini under FR-Bank's capped store-written summary", "0.60", mini_bel, "e1r_robustness/NUMBERS_E1R.md section 11 (AUX-E1R-BELIEVED-NOK) R-NOK-FRB BELIEVED, 661, monitor")
    chk("S3/S5: the lookup under the ground-truth summary", "0.75", lookup_true, "e1r_robustness/NUMBERS_E1R.md section 11 (AUX-E1R-NB6) R-NOK-FRB TRUE, NB-6")
    chk("S3/S5: the lookup under the capped store-written summary", "0.59", lookup_bel, "e1r_robustness/NUMBERS_E1R.md section 11 (AUX-E1R-NB6) R-NOK-FRB BELIEVED, NB-6")
    m = re.search(r"^\| H45-NOK \| Haiku 4\.5 \| NOK \| (\d+) \| (\d\.\d{4}) \| (\d\.\d{4}) \|", R74, flags=re.M)
    h_n, h_blind, h_true = int(m.group(1)), float(m.group(2)), float(m.group(3))
    chk("S3/S5: Haiku under the ground-truth summary, full obligation set (n = 661)", "0.82", h_true, f"r74/NUMBERS_R74.md AUX-R74-X4-H45-NOK (k = 5, temperature 0; n = {h_n})")
    m = re.search(r"^\| INDEXED-BELIEVED-15 \| \*\*(\d\.\d{4})\*\* \|", BH, flags=re.M)
    h_bel = float(m.group(1))
    chk("S3/S5: Haiku under FR-Bank's capped store-written summary", "0.71", h_bel, "believed_h/NUMBERS_BELIEVED_H.md section 5 AUX-BH-H45-15 (k = 5; the committed BELIEVED texts, cap 15; 661 items, 104 positives)")
    # the population and conditions of the three pairs are the same: the 661 (104 obligations), the ground-truth summary against FR-Bank's capped store-written summary
    same = (h_n == 661) and ("661 items, 104 positives" in BH) and ("Capped texts" in BH and "cap 15" in BH)
    chk("S3 hard-stop check: Haiku's pair is on the same population and conditions as mini's and the lookup's (661; ground truth against the capped store-written summary)",
        "same", "same" if same else "DIFFERENT", "r74/NUMBERS_R74.md X4 H45-NOK n = 661 (the full obligation set); believed_h/NUMBERS_BELIEVED_H.md: 661 items, 104 positives, the committed BELIEVED texts, cap 15")
    # ------------------------------------------------------------------ S2 (the abstract): the models 0.05 to 0.06 ahead of the count-feature lookup on the pooled metric
    hv = hyb_vs_models()
    strong = {k: hv[k] for k in ("Opus 5", "GPT-5.6 Sol", "GPT-5.6 Luna")}
    lo, hi = min(v[0] for v in strong.values()), max(v[0] for v in strong.values())
    chk("S2: 'the models stay 0.05 to 0.06 ahead' (pooled; lower end)", "0.05", lo, "r82_counterfactual/cf2/NUMBERS_CF2.md AUX-CF2-HYB-VS-MODELS (Opus +0.0540, Luna +0.0553, Sol +0.0635)",
        reliable=True, actual_reliable=all(v[1] for v in strong.values()))
    chk("S2: 'the models stay 0.05 to 0.06 ahead' (upper end)", "0.06", hi, "as above")
    # S2's first clause: the count-feature lookup closes the lead within triples: no stronger model reliably above the hybrid on the matched metric
    closes = all(not CT[n]["pn_vs_present"]["whole"]["both_exclude_zero"] for n in ("Luna minus hybrid", "Sol minus hybrid (P-H2)", "Opus minus hybrid"))
    chk("S2: 'closes that lead when a question's three store versions are compared with each other' (no stronger model reliably above the count-feature lookup, matched)",
        "holds", "holds" if closes else "fails", "r125_matched.json paired/contrasts 'Luna minus hybrid' -0.0068, 'Sol minus hybrid (P-H2)' -0.0270, 'Opus minus hybrid' -0.0101, none with both intervals clear of zero")
    # ------------------------------------------------------------------ S7 and the 5.2 worked example: the three models' matched values beside the count-feature lookup's
    mv = {k: RD[k]["pn_vs_present"]["whole"]["matched"] for k in ("LUNA_v2", "SOL_v2", "OP5_v2")}
    chk("S7 / 5.2 example: 'the three models' 0.86 to 0.88' (matched; lower end)", "0.86", min(mv.values()), "r125_matched.json readers/{LUNA_v2 0.8784, SOL_v2 0.8581, OP5_v2 0.8750}/pn_vs_present/whole/matched")
    chk("S7 / 5.2 example: 'the three models' 0.86 to 0.88' (upper end)", "0.88", max(mv.values()), "as above")
    chk("S7 / 5.2 example: the count-feature lookup scores 0.89 (matched)", "0.89", RD["HYBRID_v2"]["pn_vs_present"]["whole"]["matched"], "r125_matched.json readers/HYBRID_v2/pn_vs_present/whole/matched 0.8851")
    chk("5.2 example: 'Across all 148 triples'", "148", RD["LOOKUP_v2"]["pn_vs_present"]["whole"]["n"], "r125_matched.json readers/LOOKUP_v2/pn_vs_present/whole/n")
    leads = {k: PD["vs_lookup"][k]["pn_vs_present"] for k in ("LUNA_v2", "SOL_v2", "OP5_v2")}
    chk("5.2 example: 'a reliable 0.08 to 0.10 above the lookup' (lower end)", "0.08", min(v["whole"]["delta"] for v in leads.values()),
        "r125_matched.json paired/vs_lookup/{LUNA_v2 +0.1014, SOL_v2 +0.0811, OP5_v2 +0.0980}/pn_vs_present/whole", reliable=True, actual_reliable=all(v["whole"]["both_exclude_zero"] for v in leads.values()))
    chk("5.2 example: 'a reliable 0.08 to 0.10 above the lookup' (upper end)", "0.10", max(v["whole"]["delta"] for v in leads.values()), "as above")
    sup_ok = all(not v["per_state"]["SUPERSESSION"]["both_exclude_zero"] for v in leads.values())
    ctd_ok = all(v["per_state"][s]["delta"] > 0 for v in leads.values() for s in ("RETRACTION", "EXPIRY"))
    chk("5.2 example: 'all of that comes from retraction and expiry' (no stronger model reliably above the lookup on supersession; every counted-state lead positive)",
        "holds", "holds" if (sup_ok and ctd_ok) else "fails", "r125_matched.json paired/vs_lookup/*/pn_vs_present/per_state")
    ties = {s: (RD["LOOKUP_v2"]["pn_vs_present"]["per_state"][s]["W"], RD["LOOKUP_v2"]["pn_vs_present"]["per_state"][s]["T"], RD["LOOKUP_v2"]["pn_vs_present"]["per_state"][s]["L"]) for s in ("RETRACTION", "EXPIRY")}
    chk("5.2 example: 'where ... the lookup ties every triple' (retraction and expiry W/T/L)", "0/30/0; 0/30/0", "; ".join(f"{w}/{t}/{l}" for w, t, l in ties.values()), "r125_matched.json readers/LOOKUP_v2/pn_vs_present/per_state")
    chk("5.2 example: 'the same reader scores 0.79' (pooled)", "0.79", RD["HYBRID_v2"]["gate"], "r125_matched.json readers/HYBRID_v2/gate 0.7865 (AUX-CF2-HYB-WHOLE)")
    chk("5.2 example: 'the models stay a reliable 0.05 to 0.06 above it' (pooled)", "0.05 / 0.06", f"{r2(lo)} / {r2(hi)}", "AUX-CF2-HYB-VS-MODELS, as S2", reliable=True, actual_reliable=all(v[1] for v in strong.values()))
    # ------------------------------------------------------------------ the 5.1 worked example
    for who, name in (("mini", "E2 mini names-only minus intact"), ("Haiku", "E2 Haiku names-only minus intact")):
        d = abs(CT[name]["pn_vs_present"]["whole"]["delta"])
        chk(f"5.1 example: with every count deleted {who} stays within 0.01 (matched)", "within", "within" if d <= 0.01 else f"{d:.4f}", f"r125_matched.json paired/contrasts '{name}' whole delta {CT[name]['pn_vs_present']['whole']['delta']:+.4f}")
    for who, name in (("mini", "E2 mini counts-only minus names-only"), ("Haiku", "E2 Haiku counts-only minus names-only")):
        c = CT[name]["pn_vs_present"]["whole"]
        chk(f"5.1 example: given the counts alone {who} falls by 0.14 (matched, counts only minus names only)", "0.14", abs(c["delta"]), f"r125_matched.json paired/contrasts '{name}' whole delta {c['delta']:+.4f}", reliable=True, actual_reliable=c["both_exclude_zero"])
    vc = PD["vs_count_readers"]
    for who, key in (("mini (one draw)", "MINI1_v2"), ("Haiku", "H45_v2")):
        for s in ("RETRACTION", "EXPIRY"):
            d = vc[key]["CR-nb1"]["pn_vs_present"][s]
            chk(f"5.1 example: on {s.lower()} {who} stays reliably below the guessing count reader (matched)", "below", "below" if (d["delta"] < 0 and d["both_exclude_zero"]) else f"{d['delta']:+.4f}, reliable={d['both_exclude_zero']}", f"r125_matched.json paired/vs_count_readers/{key}/CR-nb1/pn_vs_present/{s} delta {d['delta']:+.4f}")
    # ------------------------------------------------------------------ Table 74's first row: the lookup and the models of Table 1 under the default summary
    chk("Table 74 row 1: the lookup 0.77 (Table 1, pooled)", "0.77", RD["LOOKUP_v2"]["gate"], "r125_matched.json readers/LOOKUP_v2/gate 0.7663 (AUX-CF2-NB6-V2)")
    tab1 = {k: RD[k]["gate"] for k in ("MINI5_v2", "H45_v2", "LUNA_v2", "SOL_v2", "OP5_v2")}
    chk("Table 74 row 1: the models 0.76 to 0.85 (Table 1's superseded-only rows, pooled; lower end)", "0.76", min(tab1.values()), "r125_matched.json readers/{MINI5_v2 0.7648, H45_v2 0.7566, LUNA_v2 0.8417, SOL_v2 0.8500, OP5_v2 0.8405}/gate (the recorded pooled rows Table 1 prints)")
    chk("Table 74 row 1: the models 0.76 to 0.85 (upper end)", "0.85", max(tab1.values()), "as above")
    stale = ("0.72" != r2(min(tab1.values()))) or ("0.84" != r2(max(tab1.values())))
    chk("Table 74 row 1 as built ('0.72 to 0.84') is stale against Table 1", "stale", "stale" if stale else "current", "0.72 is mini's one-draw temperature-0 row (Table 1's note a), no longer a row of Table 1; 0.84 omits Sol's 0.85")

    # ------------------------------------------------------------------ R133 RULINGS 3: tab:routes' two per-state rows (the tagged view minus the summary alone)
    for state, printed in (("expiry", ("0.75", "0.51", "+0.24", "[+0.11,+0.38]", "[+0.06,+0.40]", "15")), ("supersession", ("0.69", "0.86", "-0.17", "[-0.26,-0.07]", "[-0.28,-0.07]", "63"))):
        d = RESP[state]
        chk(f"tab:routes {state}: the tagged view's AUROC", printed[0], d["arm"], f"scores_resp.json L2/arms/RETRIEVED/{state}/arm (AUX-RESP-L2-MINI-NOK 'RETRIEVED, {state}')")
        chk(f"tab:routes {state}: the summary alone", printed[1], d["base"], f"scores_resp.json L2/arms/RETRIEVED/{state}/base")
        chk(f"tab:routes {state}: the difference", printed[2], r2s(d["D"]), f"scores_resp.json L2/arms/RETRIEVED/{state}/D {d['D']:+.4f}", reliable=(state == "expiry" or state == "supersession"),
            actual_reliable=d["item"]["excludes_zero"] and d["cluster"]["excludes_zero"])
        chk(f"tab:routes {state}: the item interval", printed[3], f"[{r2s(d['item']['ci_lo'])},{r2s(d['item']['ci_hi'])}]", f"scores_resp.json L2/arms/RETRIEVED/{state}/item")
        chk(f"tab:routes {state}: the persona interval", printed[4], f"[{r2s(d['cluster']['ci_lo'])},{r2s(d['cluster']['ci_hi'])}]", f"scores_resp.json L2/arms/RETRIEVED/{state}/cluster")
        chk(f"tab:routes {state}: the obligations", printed[5], d["n_pos"], f"scores_resp.json L2/arms/RETRIEVED/{state}/n_pos (n {d['n']}: the state's obligations against the 557 negatives)")
        chk(f"tab:routes {state}: n minus positives is the 557 negatives", "557", d["n"] - d["n_pos"], "scores_resp.json n - n_pos")
    chk("Section 7: 'the view helps mini on expiry ... and hurts it on supersession, both effects reliable'", "holds",
        "holds" if (RESP["expiry"]["D"] > 0 and RESP["supersession"]["D"] < 0 and all(RESP[s][k]["excludes_zero"] for s in ("expiry", "supersession") for k in ("item", "cluster"))) else "fails", "as above")

    bad = [c for c in CHECKS if not c["ok"]]
    for c in CHECKS:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rel = "" if c["reliable"] is None else f"  reliable claimed={c['reliable']} actual={c['actual_reliable']}"
        print(f"  [{'ok' if c['ok'] else 'MISMATCH'}] {c['where']}: printed {c['printed']} <- {vs}{rel}  ({c['source']})")
    print(f"r133_number_gate: {len(CHECKS)} checks, {len(bad)} mismatches")
    if "--built" in sys.argv:
        bad += built_checks()
    if bad:
        print("r133_number_gate: FAIL")
        sys.exit(1)
    print("r133_number_gate: PASS")


NUM = re.compile(r"(?<![\w.])[+-]?\d[\d,]*(?:\.\d+)?%?")


def numerals(text):
    text = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in text.replace("\r\n", "\n").split("\n"))
    text = re.sub(r"\\(ref|label|cite[pt]?|eqref|hd|vspace|hspace|setlength|includegraphics)\{[^}]*\}", " ", text)
    text = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    return set(NUM.findall(text))


def split(tex):
    a = tex.index("\\begin{abstract}")
    b = tex.index("\\label{main-text-end}")
    c = tex.index("\\appendix")
    return tex[a:b], tex[c:]


def built_checks():
    new = (SUB / "paper_v23.tex").read_text(encoding="utf-8", errors="replace")
    old = subprocess.run(["git", "show", f"{BASE}:iclr2027_monitoring_submission/paper_v22.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8", errors="replace")
    nm, na = split(new)
    om, oa = split(old)
    new_main = numerals(nm) - numerals(om)
    new_appx = numerals(na) - numerals(oa)
    allowed_appx = {"0.76", "0.85"} | routes_rows()[1] | {"557"}   # Table 74's corrected range; tab:routes' two per-state rows (R133 RULINGS 3), every numeral from scores_resp.json
    out = []
    print(f"  built: main-text numerals new against the v22 main text: {sorted(new_main) or 'none'}")
    print(f"  built: appendix numerals new against the v22 appendix: {sorted(new_appx) or 'none'} (allowed: {sorted(allowed_appx)})")
    if new_main:
        out.append(dict(where="built main text", printed=sorted(new_main), ok=False))
        print("  [MISMATCH] a numeral of the v23 main text does not occur in the v22 main text")
    if new_appx - allowed_appx:
        out.append(dict(where="built appendix", printed=sorted(new_appx - allowed_appx), ok=False))
        print("  [MISMATCH] a numeral of the v23 appendix does not occur in the v22 appendix and is not Table 74's corrected range")
    return out


if __name__ == "__main__":
    main()
