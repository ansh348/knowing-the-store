# -*- coding: utf-8 -*-
"""robust_tex.py -- the robustness table of R135 (the brief 'R135: THE LAST CONTENT PASS ON v23', section 2): every number of tab:robust enters the paper
through this file, none by hand.

  reviews/v23/src/robust_table.tex      the table (three columns: what we tried to break / what it removes / what happened; ten rows; a superscript p on a
                                        row whose analysis is post hoc by the ledger's own status), spliced by build_v23.py at the %%ROBUST-TABLE%% marker
                                        port_r135.py writes into Section 5.2 of body_v23.tex
  reviews/v23/results/robust_printed.json  each two-decimal form beside its four-decimal source value and key (the convention of para_printed.json); the
                                        rows' metric, population and status

Sources (no model call): reviews/r125/results/r125_matched.json (rows 2, 5), r125_t4_sibling.json (row 3), r82_counterfactual/cf2/results/cf_scores_cf2.json
(row 4), cf_scores_nc.json and reviews/r125/results/r125_t5_nc.json (row 6), cf2_paraphrase/results/para_scores.json (row 7), reviews/r122/results/enc_lookup.json
(row 8), cf_pad/results/cf_pad_scores.json (row 9; R137, 2026-09-22: the long-list check on the counterfactual set, replacing the 661-set padding and the injection of pad_probe/results/pad_scores.json and contam_scores.json, which stay in Appendix C.2), the E1R / R74 / BELIEVED_H ledgers through r133_number_gate (row 10); row 1 is the
counterfactual identity (a question-only reader scores 0.5000 by construction: one score per question reused across its three versions).
Usage: python reviews/v23/tools/robust_tex.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r133_number_gate as G133  # noqa: E402  (e1r_row, R74, BH: the FR-Bank row)

OUT_TEX = ROOT / "reviews" / "v23" / "src" / "robust_table.tex"
OUT_JSON = ROOT / "reviews" / "v23" / "results" / "robust_printed.json"


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def r2(x):
    """Two decimals, half-up on the four-decimal recorded value (the R131 convention); the magnitude."""
    return str(abs(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))


def rel(d):
    return bool(d.get("both_exclude_zero"))


def main():
    M = J("reviews/r125/results/r125_matched.json"); RD, CT = M["readers"], M["paired"]["contrasts"]
    SB = J("reviews/r125/results/r125_t4_sibling.json")
    CF = J("r82_counterfactual/cf2/results/cf_scores_cf2.json")["lanes"]
    NC = J("r82_counterfactual/cf2/results/cf_scores_nc.json")["readers"]
    T5 = J("reviews/r125/results/r125_t5_nc.json")["readers"]
    PA = J("cf2_paraphrase/results/para_scores.json")
    EN = J("reviews/r122/results/enc_lookup.json")["predictions"]["P-E1"]["encoders"]
    PD = J("pad_probe/results/pad_scores.json")["readers"]
    CO = J("pad_probe/results/contam_scores.json")["readers"]
    P = {"rows": []}

    def row(n, tried, removes, happened, metric, population, status, source, values):
        P["rows"].append(dict(n=n, tried=tried, removes=removes, happened=happened, metric=metric, population=population, status=status, source=source, values=values))

    # 1. the counterfactual identity
    row(1, "One question, three store versions", "Question-wording leakage", "A question-only reader scores $0.50$ by construction",
        "pooled", "the counterfactual set", "by construction",
        "one score per question reused across its three versions (Table 1's caption; AUX-CF2-MINI-V2 'blind 0.5000 by identity')", {"0.50": 0.5})
    # 2. the random-token lookup (matched; R125, post hoc)
    rt = RD["RANDTOK_v2"]["pn_vs_present"]["whole"]["matched"]; c = CT["random-token minus name lookup (v2)"]["pn_vs_present"]["whole"]
    assert rel(c) and c["delta"] < 0
    row(2, "Random tokens for the names", "Name meaning, length kept", f"${r2(rt)}$; the real lookup is ${r2(c['delta'])}$ higher",
        "matched", "the counterfactual set", "post hoc",
        "r125_matched.json readers/RANDTOK_v2/pn_vs_present/whole/matched; paired/contrasts 'random-token minus name lookup (v2)' (AUX-CF2-R125-MATCHED-V2, -CONTRASTS)", {r2(rt): rt, r2(c["delta"]): c["delta"]})
    # 3. the sibling-name control (matched PN against the sibling; R125 Task 4, registered)
    lk = SB["readers"]["Name lookup"]["pn_vs_sibling"]["matched"]
    models = {k: v["pn_vs_sibling"]["matched"] for k, v in SB["readers"].items() if k not in ("Name lookup", "Random-token lookup", "Count reader, guessed category")}
    assert SB["predictions"]["P-SB4"]["verdict"] == "HELD" and not SB["predictions"]["P-SB4"]["reliably_above"]
    row(3, "Sibling-name control", "List length and counts", f"Lookup ${r2(lk)}$, models ${r2(min(models.values()))}$ to ${r2(max(models.values()))}$, none reliably above the lookup",
        "matched, the PN version against its sibling", "the 88 supersession pairs", "registered",
        "r125_t4_sibling.json readers/*/pn_vs_sibling/matched; predictions P-SB4 HELD (AUX-CF2-R125-SB-*)", {r2(lk): lk, r2(min(models.values())): min(models.values()), r2(max(models.values())): max(models.values())})
    # 4. the lifecycle totals permuted (pooled; the CF-2 registration's P5, held)
    eq = {m: CF[k]["equiv_v2r_minus_v2"] for m, k in (("mini", "gpt-4.1-mini"), ("Haiku", "claude-haiku-4-5-20251001"), ("Opus", "claude-opus-5"))}
    big = max(eq, key=lambda m: abs(eq[m]["delta"]))
    assert not any(rel(v) for v in eq.values())
    row(4, "Lifecycle totals permuted", "The summary's two totals", f"No model moves by more than ${r2(eq[big]['delta'])}$, none reliably",
        "pooled", "the counterfactual set", "registered",
        "cf_scores_cf2.json lanes/*/equiv_v2r_minus_v2 (AUX-CF2-EQUIV-V2R: mini +0.0011, Haiku 4.5 +0.0072, Opus 5 -0.0052; P5 held)", {r2(eq[big]["delta"]): eq[big]["delta"]})
    # 5. the moved count (matched, counted states; R125, post hoc)
    mc = {"Opus": CT["moved count Opus k5 minus sup-only k5"], "Luna": CT["moved count Luna k5 minus sup-only k5 (E9)"], "Sol": CT["moved count Sol k5 minus sup-only k5 (E9)"]}
    mc = {m: v["pn_vs_present"]["counted"] for m, v in mc.items()}
    small = {m: CT[k]["pn_vs_present"]["counted"] for m, k in (("mini", "moved count mini minus sup-only"), ("Haiku", "moved count Haiku minus sup-only"))}
    assert all(rel(v) and v["delta"] < 0 for v in mc.values()) and not any(rel(v) for v in small.values())
    lo, hi = min(abs(v["delta"]) for v in mc.values()), max(abs(v["delta"]) for v in mc.values())
    row(5, "Count moved to a sibling version", "Where the count sits", f"Luna, Sol, Opus fall ${r2(lo)}$ to ${r2(hi)}$; mini, Haiku no reliable change",
        "matched", "the counterfactual set, the 60 counted-state pairs", "post hoc",
        "r125_matched.json paired/contrasts 'moved count {Opus k5, Luna k5, Sol k5} minus sup-only k5' counted (AUX-CF2-R125-CONTRASTS); mini and Haiku counted, intervals include zero", {r2(lo): lo, r2(hi): hi})
    # 6. every count deleted (pooled; E2 and E2 Amendment 1, registered)
    mini_n, h45_n = NC["gpt-4.1-mini"]["arms"]["INDEXED-NAMES"]["vs_v2"], NC["claude-haiku-4-5-20251001"]["arms"]["INDEXED-NAMES"]["vs_v2"]
    luna_n, opus_n = T5["GPT-5.6 Luna (five draws)"]["names_only"]["minus_intact"], T5["Opus 5 (draw 1)"]["names_only"]["minus_intact"]
    assert abs(mini_n["delta"]) < 0.01 and abs(h45_n["delta"]) < 0.01 and rel(luna_n) and rel(opus_n)
    row(6, "Every count deleted", "The counts", f"Mini and Haiku within $0.01$; Luna loses ${r2(luna_n['delta'])}$, Opus ${r2(opus_n['delta'])}$",
        "pooled", "the counterfactual set", "registered",
        "cf_scores_nc.json readers/*/arms/INDEXED-NAMES/vs_v2 (AUX-CF2-NC-MINI-NAMES -0.0064, -H45-NAMES -0.0059; P-N1 held); r125_t5_nc.json readers/{Luna five draws, Opus draw 1}/names_only/minus_intact (AUX-CF2-R125-NC-*)",
        {"0.01": 0.01, r2(luna_n["delta"]): luna_n["delta"], r2(opus_n["delta"]): opus_n["delta"]})
    # 7. the paraphrases (pooled; ADDENDUM_PARA, registered, descriptive)
    lex = PA["lookups"]["lex_v2"]["paraphrase"]; emb = PA["lookups"]["emb_v2"]["paired"]; mini = PA["models"]["MINI"]["v2"]["paired"]; h45 = PA["models"]["H45"]["v2"]["paired"]
    assert lex == 0.5 and abs(mini["delta"]) > abs(emb["delta"]) and abs(h45["delta"]) > abs(emb["delta"])
    row(7, "Questions reworded, no shared word", "Word overlap with names", f"Word lookup at ${r2(lex)}$; embedding lookup loses ${r2(emb['delta'])}$; mini, Haiku lose more",
        "pooled", "the 115 reworded pairs", "registered",
        "para_scores.json lookups/lex_v2/paraphrase 0.5000, lookups/emb_v2/paired -0.0216, models/MINI/v2/paired -0.0326, models/H45/v2/paired -0.0642 (AUX-PARA-LOOKUP-LEX-V2, -EMB-V2, -MINI-V2, -H45-V2)", {r2(lex): lex, r2(emb["delta"]): emb["delta"]})
    # 8. two other encoders (pooled; the R122 encoder registration, P-E1 held)
    d8 = {k: EN[k]["delta"] for k in ("MPNET", "BGE")}
    assert all(abs(v) < 0.01 for v in d8.values())
    row(8, "Two other sentence encoders", "The choice of encoder", "Both within $0.01$ of the lookup",
        "pooled", "the counterfactual set", "registered",
        "enc_lookup.json predictions/P-E1/encoders/{MPNET -0.0059, BGE -0.0080}/delta (AUX-R122-ENC-*; P-E1 held)", {"0.01": 0.01})
    # 9. R137 (2026-09-22): the long-list check on the counterfactual set (ADDENDUM_CF_PAD, registered; cf_pad/results/cf_pad_scores.json), replacing the
    #    (the cell's comma form 'Luna, Sol lose ... , lead it by ...': the brief's 'Luna and Sol lose ... and lead' is the abstract's and 5.2's wording too, and repeat_scan bars a third place; REPORT_R137.md)
    #    661-set padding and the wrong-name injection (ADDENDUM_PAD and its Amendment 1), which stay in Appendix C.2's 'registered checks' paragraph and tab:pad.
    CP = J("cf_pad/results/cf_pad_scores.json")
    lk = CP["readers"]["LOOKUP"]["superseded"]["pooled"]; lk_d = lk["padded_minus_unpadded"]
    ml = {m: CP["minus_lookup"][m]["LOOKUP"]["superseded"]["padded"] for m in ("MINI", "H45", "OP5", "LUNA", "SOL")}
    loss = {m: CP["readers"][m]["superseded"]["pooled"]["padded_minus_unpadded"] for m in ("MINI", "H45", "OP5", "LUNA", "SOL")}
    assert rel(lk_d) and lk_d["delta"] < 0 and CP["census"]["OP5"]["k_new"] == 1 and CP["census"]["OP5"]["k_recorded"] == 5
    assert all(loss[m]["delta"] <= lk_d["delta"] + 0.05 and not (rel(ml[m]["pooled"]) and ml[m]["pooled"]["delta"] > 0) for m in ("MINI", "H45", "OP5"))   # fall with it: none reliably above the lookup
    assert all(rel(loss[m]) and loss[m]["delta"] < 0 and loss[m]["delta"] > lk_d["delta"] for m in ("LUNA", "SOL"))                                     # lose less than the lookup
    assert all(rel(ml[m]["pooled"]) and ml[m]["pooled"]["delta"] > 0 and rel(ml[m]["matched"]) and ml[m]["matched"]["delta"] > 0 for m in ("LUNA", "SOL"))  # lead it on both metrics
    lo_l, hi_l = sorted(abs(loss[m]["delta"]) for m in ("LUNA", "SOL"))
    lo_m, hi_m = sorted(ml[m]["pooled"]["delta"] for m in ("LUNA", "SOL"))
    row(9, "List padded to 60 names", "Short, clean lists", f"Lookup ${r2(lk['unpadded'])}$ to ${r2(lk['padded'])}$; mini, Haiku, Opus fall with it; Luna, Sol lose ${r2(lo_l)}$ to ${r2(hi_l)}$, lead it by ${r2(lo_m)}$ to ${r2(hi_m)}$",
        "pooled", "the counterfactual set, supersession (88 triples); Opus one draw against its recorded five-draw row", "registered",
        "cf_pad_scores.json readers/LOOKUP/superseded/pooled {unpadded 0.9223, padded 0.7416} (AUX-CFP-READERS-SUPERSEDED); readers/{LUNA,SOL}/superseded/pooled/padded_minus_unpadded (-0.0636, -0.0693, both reliable); "
        "minus_lookup/{LUNA,SOL}/LOOKUP/superseded/padded/pooled (+0.1375, +0.1274, both reliable on both metrics; AUX-CFP-MINUS-LOOKUP-SUPERSEDED); mini -0.0525, Haiku -0.0062, Opus -0.0336 minus the lookup, intervals including zero (P-L2 holds, P-L1 fails on Opus)",
        {r2(lk["unpadded"]): lk["unpadded"], r2(lk["padded"]): lk["padded"], r2(lo_l): lo_l, r2(hi_l): hi_l, r2(lo_m): lo_m, r2(hi_m): hi_m, "60": 60})
    # 10. FR-Bank's own metadata (pooled; the full obligation set; E1R BELIEVED and the BELIEVED_H registration)
    mini_t, lk_t = G133.e1r_row("| R-NOK-FRB | TRUE |"); mini_b, lk_b = G133.e1r_row("| R-NOK-FRB | BELIEVED |")
    h_t = float(re.search(r"^\| H45-NOK \| Haiku 4\.5 \| NOK \| (\d+) \| (\d\.\d{4}) \| (\d\.\d{4}) \|", G133.R74, flags=re.M).group(3))
    h_b = float(re.search(r"^\| INDEXED-BELIEVED-15 \| \*\*(\d\.\d{4})\*\* \|", G133.BH, flags=re.M).group(1))
    row(10, "The store's own metadata (FR-Bank)", "The ground-truth summary", f"Mini, Haiku, lookup: ${r2(mini_t)}$, ${r2(h_t)}$, ${r2(lk_t)}$ to ${r2(mini_b)}$, ${r2(h_b)}$, ${r2(lk_b)}$",
        "pooled", "the full obligation set", "registered",
        "NUMBERS_E1R.md section 11 R-NOK-FRB TRUE / BELIEVED (AUX-E1R-TRUE-NOK, -BELIEVED-NOK, -NB6); NUMBERS_R74.md AUX-R74-X4-H45-NOK; NUMBERS_BELIEVED_H.md AUX-BH-H45-15",
        {r2(mini_t): mini_t, r2(h_t): h_t, r2(lk_t): lk_t, r2(mini_b): mini_b, r2(h_b): h_b, r2(lk_b): lk_b})
    # ---- the table
    L = ["% ROBUST-TABLE (written by reviews/v23/tools/robust_tex.py from the artifacts named in its docstring; spliced at its marker by build_v23.py; do not edit by hand)",
         "\\begin{table}[t]",
         "\\caption{The checks we ran to break the lookup result, what each removes, and what happened. Pooled AUROC on the counterfactual set unless noted: "
         "rows 2 and 5 matched and post hoc ($^{p}$), row 5 on the $60$ counted-state pairs; row 3 the \\pn{} version against its sibling, matched, on the $88$ supersession pairs; row 7 the $115$ reworded pairs; "
         "row 9 the $88$ supersession triples, the lists padded to $60$ names, Opus at one draw against its five-draw row; row 10 the full obligation set. "
         "Short ground-truth lists do not establish robustness to longer store-written ones. (Appendices~\\ref{app:counterfactual} and~\\ref{app:census})}",
         "\\label{tab:robust}", "\\centering", "\\scriptsize", "\\setlength{\\tabcolsep}{3pt}", "\\renewcommand{\\arraystretch}{0.95}",
         "\\begin{tabular}{@{}p{0.255\\linewidth}p{0.19\\linewidth}p{0.525\\linewidth}@{}}", "\\toprule",
         "What we tried to break & What it removes & What happened \\\\", "\\midrule"]
    for r in P["rows"]:
        mark = "$^{p}$" if r["status"] == "post hoc" else ""
        L.append(f"{r['tried']}{mark} & {r['removes']} & {r['happened']} \\\\")
    L += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    OUT_TEX.write_text("\n".join(L), encoding="utf-8", newline="\n")
    OUT_JSON.write_text(json.dumps(P, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT_TEX.relative_to(ROOT).as_posix()} and {OUT_JSON.relative_to(ROOT).as_posix()}")
    for r in P["rows"]:
        print(f"  {r['n']:2d} [{r['status']:11s} {r['metric']:44s}] {r['happened']}")


if __name__ == "__main__":
    main()
