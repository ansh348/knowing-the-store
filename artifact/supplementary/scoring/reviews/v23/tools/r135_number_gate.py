# -*- coding: utf-8 -*-
"""r135_number_gate.py -- the number gate of R135 (2026-09-21; the brief 'R135: THE LAST CONTENT PASS ON v23' and 'R135 ADDENDUM'; the author's ruling on
ADDENDUM 2): every number the pass's new texts print is read from its artifact here, independently of reviews/v23/results/robust_printed.json (which
robust_tex.py writes the table from), and compared at the printed precision (two decimals half-up on the four-decimal recorded value; the R131 convention)
with the reliability or direction each cell claims: the ten rows of tab:robust, the abstract's numerals, the Section 5.1 trims' remaining numeral, the
builders box's 0.12, and ADDENDUM 2's Section 7 numerals. Runs R134's 62 checks first (unchanged texts), then its own; with --built, R134's numeral-set
checks with this pass's main-text numerals allowed.
Usage: python reviews/v23/tools/r135_number_gate.py [--built]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402
import r133_number_gate as G133  # noqa: E402


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def rel(d):
    return bool(d.get("both_exclude_zero"))


def checks135():
    chk, r2 = G.chk, G.r2
    M = J("reviews/r125/results/r125_matched.json"); RD, CT = M["readers"], M["paired"]["contrasts"]
    SB = J("reviews/r125/results/r125_t4_sibling.json")
    CF = J("r82_counterfactual/cf2/results/cf_scores_cf2.json")["lanes"]
    NC = J("r82_counterfactual/cf2/results/cf_scores_nc.json")["readers"]
    T5 = J("reviews/r125/results/r125_t5_nc.json")["readers"]
    PA = J("cf2_paraphrase/results/para_scores.json")
    EN = J("reviews/r122/results/enc_lookup.json")["predictions"]["P-E1"]["encoders"]
    PD = J("pad_probe/results/pad_scores.json")["readers"]
    CO = J("pad_probe/results/contam_scores.json")["readers"]
    BH = (ROOT / "believed_h" / "NUMBERS_BELIEVED_H.md").read_text(encoding="utf-8", errors="replace")
    # ---- tab:robust
    blind = re.search(r"AUX-CF2-MINI-V2\*\* \| \*\*[0-9.]+\*\* \(blind (0\.5000) by identity", (ROOT / "r82_counterfactual" / "cf2" / "NUMBERS_CF2.md").read_text(encoding="utf-8", errors="replace"))
    chk("tab:robust row 1: a question-only reader scores 0.50 by construction", "0.50", float(blind.group(1)), "NUMBERS_CF2.md AUX-CF2-MINI-V2 'blind 0.5000 by identity' (one score per question across its three versions)")
    rt = RD["RANDTOK_v2"]["pn_vs_present"]["whole"]["matched"]; c = CT["random-token minus name lookup (v2)"]["pn_vs_present"]["whole"]
    chk("tab:robust row 2: the random-token lookup 0.65 (matched)", "0.65", rt, "r125_matched.json readers/RANDTOK_v2/pn_vs_present/whole/matched (post hoc)")
    chk("tab:robust row 2: 'the real lookup is 0.13 higher' (matched, reliable)", "0.13", c["delta"], f"r125_matched.json contrasts 'random-token minus name lookup (v2)' whole {c['delta']:+.4f}", reliable=True, actual_reliable=rel(c) and c["delta"] < 0)
    lk = SB["readers"]["Name lookup"]["pn_vs_sibling"]["matched"]
    models = {k: v["pn_vs_sibling"]["matched"] for k, v in SB["readers"].items() if k not in ("Name lookup", "Random-token lookup", "Count reader, guessed category")}
    chk("tab:robust row 3 / abstract: the lookup 0.95 against its sibling (matched; the 88 supersession pairs)", "0.95", lk, "r125_t4_sibling.json readers/Name lookup/pn_vs_sibling/matched (AUX-CF2-R125-SB-*)")
    chk("tab:robust row 3 / abstract: models 0.88 (the floor; Haiku 4.5)", "0.88", min(models.values()), "r125_t4_sibling.json readers/*/pn_vs_sibling/matched, the minimum")
    chk("tab:robust row 3: models to 0.97 (Opus 5)", "0.97", max(models.values()), "as above, the maximum")
    chk("tab:robust row 3 / abstract: 'none reliably above the lookup' (P-SB4)", "HELD", SB["predictions"]["P-SB4"]["verdict"], f"r125_t4_sibling.json predictions/P-SB4 reliably_above {SB['predictions']['P-SB4']['reliably_above']}")
    chk("tab:robust row 3: every reader, the lookup included, at 0.88 or higher against the sibling (the abstract's parenthetical, deleted by the G2 ruling; 0.88 moved to the row)", "0.88", min([lk] + list(models.values())), "r125_t4_sibling.json, the minimum over the lookup and the five models")
    eq = {m: CF[k]["equiv_v2r_minus_v2"] for m, k in (("mini", "gpt-4.1-mini"), ("Haiku", "claude-haiku-4-5-20251001"), ("Opus", "claude-opus-5"))}
    big = max(abs(v["delta"]) for v in eq.values())
    chk("tab:robust row 4: 'No model moves by more than 0.01' (totals permuted, pooled; the largest |delta|)", "0.01", big, "cf_scores_cf2.json lanes/*/equiv_v2r_minus_v2 delta: mini +0.0011, Haiku +0.0072, Opus -0.0052 (AUX-CF2-EQUIV-V2R; P5 held)",
        reliable=False, actual_reliable=any(rel(v) for v in eq.values()))
    mc = {m: CT[k]["pn_vs_present"]["counted"] for m, k in (("Opus", "moved count Opus k5 minus sup-only k5"), ("Luna", "moved count Luna k5 minus sup-only k5 (E9)"), ("Sol", "moved count Sol k5 minus sup-only k5 (E9)"))}
    chk("tab:robust row 5: 'fall 0.28 to 0.33 on the counted states' (lower end; matched)", "0.28", min(abs(v["delta"]) for v in mc.values()), "r125_matched.json contrasts moved count {Opus -0.2833, Luna -0.2917, Sol -0.3250} counted (AUX-CF2-R125-CONTRASTS)",
        reliable=True, actual_reliable=all(rel(v) and v["delta"] < 0 for v in mc.values()))
    chk("tab:robust row 5: upper end", "0.33", max(abs(v["delta"]) for v in mc.values()), "as above")
    small = {m: CT[k]["pn_vs_present"]["counted"] for m, k in (("mini", "moved count mini minus sup-only"), ("Haiku", "moved count Haiku minus sup-only"))}
    chk("tab:robust row 5 / 5.1: 'mini and Haiku show no reliable change' (counted states, matched)", "not reliable", "not reliable" if not any(rel(v) for v in small.values()) else "reliable", f"r125_matched.json contrasts moved count mini {small['mini']['delta']:+.4f}, Haiku {small['Haiku']['delta']:+.4f} counted")
    mini_n, h45_n = NC["gpt-4.1-mini"]["arms"]["INDEXED-NAMES"]["vs_v2"], NC["claude-haiku-4-5-20251001"]["arms"]["INDEXED-NAMES"]["vs_v2"]
    chk("tab:robust row 6 / 5.1: 'Mini and Haiku within 0.01' with every count deleted (pooled)", "within", "within" if abs(mini_n["delta"]) < 0.01 and abs(h45_n["delta"]) < 0.01 else "beyond", f"cf_scores_nc.json readers/*/arms/INDEXED-NAMES/vs_v2 delta: mini {mini_n['delta']:+.4f}, Haiku {h45_n['delta']:+.4f} (AUX-CF2-NC-*-NAMES; P-N1 held)")
    luna_n, opus_n = T5["GPT-5.6 Luna (five draws)"]["names_only"]["minus_intact"], T5["Opus 5 (draw 1)"]["names_only"]["minus_intact"]
    chk("tab:robust row 6: 'Luna loses 0.06' (pooled, reliable)", "0.06", luna_n["delta"], f"r125_t5_nc.json readers/GPT-5.6 Luna (five draws)/names_only/minus_intact {luna_n['delta']:+.4f} (AUX-CF2-R125-NC-LUNA-NAMES)", reliable=True, actual_reliable=rel(luna_n) and luna_n["delta"] < 0)
    chk("tab:robust row 6 / 5.1: 'Opus 0.04' (pooled, reliable)", "0.04", opus_n["delta"], f"r125_t5_nc.json readers/Opus 5 (draw 1)/names_only/minus_intact {opus_n['delta']:+.4f} (AUX-CF2-R125-NC-OP5-NAMES)", reliable=True, actual_reliable=rel(opus_n) and opus_n["delta"] < 0)
    chk("tab:robust row 7: 'A word-matching lookup falls to 0.50'", "0.50", PA["lookups"]["lex_v2"]["paraphrase"], "para_scores.json lookups/lex_v2/paraphrase (AUX-PARA-LOOKUP-LEX-V2)")
    emb = PA["lookups"]["emb_v2"]["paired"]
    chk("tab:robust row 7 / 5.2 / abstract: 'the embedding lookup loses 0.02'", "0.02", emb["delta"], f"para_scores.json lookups/emb_v2/paired {emb['delta']:+.4f} (AUX-PARA-LOOKUP-EMB-V2)", reliable=False, actual_reliable=rel(emb))
    more = abs(PA["models"]["MINI"]["v2"]["paired"]["delta"]) > abs(emb["delta"]) and abs(PA["models"]["H45"]["v2"]["paired"]["delta"]) > abs(emb["delta"])
    chk("tab:robust row 7 / 5.2: 'mini and Haiku lose more' (than the embedding lookup)", "holds", "holds" if more else "fails", "para_scores.json models/MINI/v2/paired -0.0326, models/H45/v2/paired -0.0642 against -0.0216")
    chk("tab:robust row 8: 'Both within 0.01 of the lookup' (encoders, pooled)", "within", "within" if all(abs(EN[k]["delta"]) < 0.01 for k in ("MPNET", "BGE")) else "beyond", f"enc_lookup.json predictions/P-E1/encoders MPNET {EN['MPNET']['delta']:+.4f}, BGE {EN['BGE']['delta']:+.4f} (AUX-R122-ENC-*; P-E1 held)")
    chk("tab:robust row 9: 'Padded, the lookup falls to 0.67' (60 names; the full obligation set)", "0.67", PD["emb"]["60"]["auroc"], "pad_scores.json readers/emb/60/auroc (AUX-PAD-LOOKUP-EMB)")
    chk("tab:robust row 9: 'with wrong names it falls to 0.67' (c = 0.232; the counterfactual set)", "0.67", CO["emb"]["INDEXED-V2-C0.232"]["auroc"], "contam_scores.json readers/emb/INDEXED-V2-C0.232/auroc (AUX-PAD-C-LOOKUP-EMB)")
    chk("tab:robust row 9: '... and 0.60' (c = 0.40)", "0.60", CO["emb"]["INDEXED-V2-C0.40"]["auroc"], "contam_scores.json readers/emb/INDEXED-V2-C0.40/auroc")
    within = max(abs(CO[m][k]["model_minus_emb"]["delta"]) for m in ("MINI", "H45") for k in ("INDEXED-V2-C0.232", "INDEXED-V2-C0.40"))
    chk("tab:robust row 9: 'mini and Haiku fall with it, within 0.02 of it' (the largest model minus lookup on the injected lists; intervals include zero)", "within",
        "within" if within < 0.02 and not any(rel(CO[m][k]["model_minus_emb"]) for m in ("MINI", "H45") for k in ("INDEXED-V2-C0.232", "INDEXED-V2-C0.40")) else "beyond", f"contam_scores.json readers/{{MINI,H45}}/*/model_minus_emb, largest |delta| {within:.4f} (AUX-PAD-C-MINI, -C-H45)")
    mini_t, lk_t = G133.e1r_row("| R-NOK-FRB | TRUE |"); mini_b, lk_b = G133.e1r_row("| R-NOK-FRB | BELIEVED |")
    h_t = float(re.search(r"^\| H45-NOK \| Haiku 4\.5 \| NOK \| (\d+) \| (\d\.\d{4}) \| (\d\.\d{4}) \|", G133.R74, flags=re.M).group(3))
    h_b = float(re.search(r"^\| INDEXED-BELIEVED-15 \| \*\*(\d\.\d{4})\*\* \|", G133.BH, flags=re.M).group(1))
    for nm, printed, v, src in (("mini, ground truth", "0.73", mini_t, "AUX-E1R-TRUE-NOK"), ("Haiku, ground truth", "0.82", h_t, "AUX-R74-X4-H45-NOK"), ("the lookup, ground truth", "0.75", lk_t, "AUX-E1R-NB6"),
                                ("mini, FR-Bank's metadata", "0.60", mini_b, "AUX-E1R-BELIEVED-NOK"), ("Haiku, FR-Bank's metadata", "0.71", h_b, "AUX-BH-H45-15"), ("the lookup, FR-Bank's metadata", "0.59", lk_b, "AUX-E1R-NB6 BELIEVED")):
        chk(f"tab:robust row 10 / abstract: {nm}", printed, v, src)
    # ---- the builders box (R135 section 5.1): Haiku 0.12 above the lookup under FR-Bank's store-written summary
    row = next(ln for ln in BH.splitlines() if ln.startswith("| INDEXED-BELIEVED-15 | **"))     # section 5's scored row (section 4's submission row shares the label)
    cell = [c.strip() for c in row.split("|")][8]            # the 'Haiku minus lookup (item; persona)' column of AUX-BH-H45-15
    m = re.match(r"([+-]\d\.\d{4}) \(\[([+-]\d\.\d{4}), ([+-]\d\.\d{4})\]; \[([+-]\d\.\d{4}), ([+-]\d\.\d{4})\]\)", cell)
    d, a, b, c2, e = (float(x) for x in m.groups())
    chk("builders box: 'under FR-Bank's store-written summary, where Haiku sits 0.12 above the lookup'", "0.12", d, f"NUMBERS_BELIEVED_H.md AUX-BH-H45-15 'Haiku minus lookup' {d:+.4f} ([{a:+.4f}, {b:+.4f}]; [{c2:+.4f}, {e:+.4f}]): reliable, both intervals above zero",
        reliable=True, actual_reliable=(a > 0 and c2 > 0))
    # ---- the abstract's other numerals (R134's checks cover 148, 0.02, 0.04; the sibling floor above)
    d4 = G.SUP["LUNA"]["pooled"]["paraphrase"]
    chk("abstract: 'one stronger model edges 0.04 ahead' (Luna, the named state, reworded, pooled)", "0.04", d4["delta"], "para_minus_lookup_posthoc.json LUNA v2 superseded pooled paraphrase (AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2)", reliable=True, actual_reliable=rel(d4) and d4["delta"] > 0)
    # ---- Section 5.1 after the ADDENDUM's trims: the one numeral kept, 'given the counts alone, they fall by 0.14' (matched; R133's worked example)
    for who, name in (("mini", "E2 mini counts-only minus names-only"), ("Haiku", "E2 Haiku counts-only minus names-only")):
        cc = CT[name]["pn_vs_present"]["whole"]
        chk(f"5.1: 'given the counts alone, they fall by 0.14' ({who}; matched, counts only minus names only)", "0.14", abs(cc["delta"]), f"r125_matched.json contrasts '{name}' whole {cc['delta']:+.4f}", reliable=True, actual_reliable=rel(cc))
    # ---- ADDENDUM 2, item 2 (Section 7): the propagation sentences (lock_amend8.json; AUX-DS-A8-*)
    A8 = J("ds_downstream/run/lock_amend8.json")
    cg, co, dd, ff = A8["census"]["gt"]["primary"], A8["census"]["own"]["primary"], A8["dup35"]["own/primary"], A8["false_propagation"]["own/primary"]
    chk("Section 7: 'changes 1 of 452 assembled views under the reference tags'", "1 / 452", f"{cg['changed']} / {cg['views']}", "lock_amend8.json census/gt/primary (AUX-DS-A8-RULE-CENSUS)")
    chk("Section 7: 'the same rule changes 90 views' (own tags, primary)", "90", co["changed"], "lock_amend8.json census/own/primary changed")
    chk("Section 7: 'fully tags 15 of the 35 duplicate views'", "15 / 35", f"{dd['items_fully_tagged']} / {dd['items']}", "lock_amend8.json dup35/own/primary (AUX-DS-A8-DUP35)")
    chk("Section 7: 'propagates falsely (69 of 2,333 licensed active lines)'", "69 / 2333", f"{ff['false_propagations']} / {ff['active_lines_gt']}", f"lock_amend8.json false_propagation/own/primary (AUX-DS-A8-FALSEPROP; share {ff['share']})")


def main():
    G.checks()
    n134 = len(G.CHECKS)
    checks135()
    bad = [c for c in G.CHECKS if not c["ok"]]
    for c in G.CHECKS[n134:]:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rl = "" if c["reliable"] is None else f"  reliable claimed={c['reliable']} actual={c['actual_reliable']}"
        print(f"  [{'ok' if c['ok'] else 'MISMATCH'}] {c['where']}: printed {c['printed']} <- {vs}{rl}  ({c['source']})")
    print(f"r135_number_gate: {len(G.CHECKS)} checks (R134's {n134} and this pass's {len(G.CHECKS) - n134}), {len(bad)} mismatches")
    if "--built" in sys.argv:
        pf = G.printed_forms

        def printed_forms():
            main, appx = pf()
            extra = {"0.65", "0.13", "0.95", "0.88", "0.97", "0.01", "0.28", "0.33", "0.06", "0.04", "0.50", "0.02", "0.67", "0.60", "0.14",   # tab:robust and 5.1
                     "0.73", "0.82", "0.75", "0.71", "0.59", "0.12",                                                                       # row 10 and the box
                     "90", "69", "2,333", "1", "452", "15", "35", "60", "88", "115", "10"}                                                  # ADDENDUM 2; the caption's counts and row index
            return main | extra, appx
        G.printed_forms = printed_forms
        bad += G.built_checks()
    if bad:
        print("r135_number_gate: FAIL")
        sys.exit(1)
    print("r135_number_gate: PASS")


if __name__ == "__main__":
    main()
