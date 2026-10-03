# -*- coding: utf-8 -*-
"""r131_number_gate.py -- program R131 (2026-09-20; the author's brief 'KtS R131: land R125 in the body'): the number gate. Every number the
author's texts print (sections A to G of the brief) is read from its artifact (reviews/r125/results/*.json; r82_counterfactual/cf2/NUMBERS_CF2.md
section 14e for the hybrid's pooled rows; the recorded body values for the carried numbers), rounded to the printed precision, and compared with
the printed form. A mismatch is listed; nothing is adjusted. Exit 1 on any mismatch. The same table is the basis of reviews/NUMBERS_R131.md
(ledger_r131.py reads CHECKS).
Usage: python reviews/v22/tools/r131_number_gate.py
"""
from __future__ import annotations

import json
import pathlib
import sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[3]
R125 = ROOT / "reviews" / "r125" / "results"
M = json.load(open(R125 / "r125_matched.json", encoding="utf-8"))
T2 = json.load(open(R125 / "r125_t2_emptiness.json", encoding="utf-8"))
T3F = json.load(open(R125 / "r125_t3_frbank.json", encoding="utf-8"))
T3G = json.load(open(R125 / "r125_t3_graphiti.json", encoding="utf-8"))
T4 = json.load(open(R125 / "r125_t4_sibling.json", encoding="utf-8"))
T5 = json.load(open(R125 / "r125_t5_nc.json", encoding="utf-8"))
RD = M["readers"]
PD = M["paired"]


def r2(x):
    """Round half up at two decimals on the four-decimal value the ledger prints (Decimal, not binary float rounding)."""
    return str(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def rel(d):
    return bool(d["both_exclude_zero"])


def matched(key, scope="whole", side="pn_vs_present"):
    r = RD[key][side]
    return r["whole"]["matched"] if scope == "whole" else r["per_state"][scope]["matched"]


def wtl(key, scope="whole", side="pn_vs_present"):
    r = RD[key][side]
    x = r["whole"] if scope == "whole" else r["per_state"][scope]
    return f"{x['W']}/{x['T']}/{x['L']}"


def vs_lookup(key, scope="whole"):
    v = PD["vs_lookup"][key]["pn_vs_present"]
    return v["whole"] if scope == "whole" else v["per_state"][scope]


def contrast(name, scope="whole"):
    return PD["contrasts"][name]["pn_vs_present"][scope]


def vs_count(key, cr, state):
    return PD["vs_count_readers"][key][cr]["pn_vs_present"][state]


# (where, printed, artifact value (four decimals), reliability claim or None, the source key)
CHECKS = []


def chk(where, printed, value, source, reliable=None, actual_reliable=None, fmt=r2):
    ok = fmt(value) == printed if isinstance(value, float) else str(value) == printed
    if reliable is not None:
        ok = ok and (actual_reliable == reliable)
    CHECKS.append(dict(where=where, printed=printed, value=value, source=source, reliable=reliable, actual_reliable=actual_reliable, ok=ok))


def main():
    # ---------------------------------------------------------------- B. Section 5.1
    cra = RD["CR-oracle-a_v2"]["pn_vs_present"]["per_state"]
    chk("5.1 p1: category-given count reader wins every retraction triple", "30/0/0", f"{cra['RETRACTION']['W']}/{cra['RETRACTION']['T']}/{cra['RETRACTION']['L']}", "AUX-CF2-R125-PERSTATE CR-oracle-a_v2 RETRACTION")
    chk("5.1 p1: ... and every expiry triple", "30/0/0", f"{cra['EXPIRY']['W']}/{cra['EXPIRY']['T']}/{cra['EXPIRY']['L']}", "AUX-CF2-R125-PERSTATE CR-oracle-a_v2 EXPIRY")
    chk("5.1 p1: the name lookup wins 82 of the 88 supersession triples and loses none", "82/6/0", wtl("LOOKUP_v2", "SUPERSESSION"), "AUX-CF2-R125-PERSTATE LOOKUP_v2 SUPERSESSION")
    # p2
    c = contrast("E2 mini names-only minus intact"); chk("5.1 p2: removing counts leaves mini within 0.01 (matched; mini one draw)", "0.00", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'E2 mini names-only minus intact' whole", None)
    c = contrast("E2 Haiku names-only minus intact"); chk("5.1 p2: ... Haiku within 0.01 (matched)", "0.00", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'E2 Haiku names-only minus intact' whole")
    c = contrast("E2 mini counts-only minus names-only"); chk("5.1 p2: counts alone below names alone by 0.14, mini (matched)", "0.14", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'E2 mini counts-only minus names-only' whole", True, rel(c))
    c = contrast("E2 Haiku counts-only minus names-only"); chk("5.1 p2: ... 0.14, Haiku (matched)", "0.14", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'E2 Haiku counts-only minus names-only' whole", True, rel(c))
    chk("5.1 p2: (0.12 pooled, mini) carried: AUX-CF2-NC-MINI counts only minus names only -0.1242", "0.12", 0.1242, "tab:cf-names-counts (AUX-CF2-NC-*), the body's recorded value")
    chk("5.1 p2: (0.16 pooled, Haiku) carried: AUX-CF2-NC-H45 -0.1562", "0.16", 0.1562, "tab:cf-names-counts (AUX-CF2-NC-*), the body's recorded value")
    c = contrast("E2 mini counts-only minus names-only", "counted"); chk("5.1 p2: the whole loss falls on supersession: mini counted-state difference not reliable", "not reliable", "not reliable" if not rel(c) else "reliable", "AUX-CF2-R125-CONTRASTS mini counts-only minus names-only, counted")
    c = contrast("E2 Haiku counts-only minus names-only", "counted"); chk("5.1 p2: ... Haiku counted-state difference not reliable", "not reliable", "not reliable" if not rel(c) else "reliable", "AUX-CF2-R125-CONTRASTS Haiku counts-only minus names-only, counted")
    chk("5.1 p2: guessing count reader 0.77 on retraction (matched)", "0.77", matched("CR-nb1_v2", "RETRACTION"), "AUX-CF2-R125-PERSTATE CR-nb1_v2 RETRACTION")
    chk("5.1 p2: ... 0.75 on expiry", "0.75", matched("CR-nb1_v2", "EXPIRY"), "AUX-CF2-R125-PERSTATE CR-nb1_v2 EXPIRY")
    for key, name in (("MINI5_v2", "mini five draws"), ("MINI1_v2", "mini one draw"), ("H45_v2", "Haiku")):
        for st in ("RETRACTION", "EXPIRY"):
            d = vs_count(key, "CR-nb1", st)
            chk(f"5.1 p2: {name} reliably below the guessing reader on {st.lower()}", "reliable", "reliable" if rel(d) else "not reliable", f"AUX-CF2-R125-VS-COUNT {key} minus CR-nb1 {st}")
    # p3 (carried: AUX-RESP own-name ablation)
    chk("5.1 p3: mini 0.86 to 0.53 (carried, Appendix E.10)", "0.86 / 0.53", "0.86 / 0.53", "the body's recorded values (Appendix E.10, the own-name ablation)")
    chk("5.1 p3: Haiku 0.89 to 0.68 (carried)", "0.89 / 0.68", "0.89 / 0.68", "the body's recorded values (Appendix E.10)")
    # p4
    vals = [matched(k, st) for k in ("LUNA_v2", "SOL_v2", "OP5_v2") for st in ("RETRACTION", "EXPIRY")]
    chk("5.1 p4: Luna, Sol, Opus on retraction and expiry, matched, low end 0.58", "0.58", min(vals), "AUX-CF2-R125-PERSTATE SOL_v2 RETRACTION 0.5833")
    chk("5.1 p4: ... high end 0.87", "0.87", max(vals), "AUX-CF2-R125-PERSTATE LUNA_v2 EXPIRY 0.8667")
    for key in ("LUNA_v2", "SOL_v2", "OP5_v2"):
        for st in ("RETRACTION", "EXPIRY"):
            d = vs_count(key, "CR-nb1", st)
            below_rel = rel(d) and d["delta"] < 0
            chk(f"5.1 p4: {key} not reliably below the guessing reader on {st.lower()}", "not reliably below", "not reliably below" if not below_rel else "reliably below", f"AUX-CF2-R125-VS-COUNT {key} minus CR-nb1 {st} ({d['delta']:+.4f})")
    c = contrast("moved count Opus k5 minus sup-only k5", "counted"); chk("5.1 p4: Opus falls by 0.28 across the two counted states (matched)", "0.28", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'moved count Opus k5 minus sup-only k5' counted", True, rel(c))
    c = contrast("moved count Sol k5 minus sup-only k5 (E9)", "counted"); chk("5.1 p4: Sol by 0.33 (matched, counted)", "0.33", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'moved count Sol k5 minus sup-only k5 (E9)' counted", True, rel(c))
    c = contrast("moved count Luna k5 minus sup-only k5 (E9)", "ret"); chk("5.1 p4: Luna falls by 0.32 on retraction (matched)", "0.32", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'moved count Luna k5 minus sup-only k5 (E9)' ret", True, rel(c))
    c = contrast("moved count Luna k5 minus sup-only k5 (E9)", "exp"); chk("5.1 p4: ... 0.27 on expiry", "0.27", abs(c["delta"]), "AUX-CF2-R125-CONTRASTS 'moved count Luna k5 minus sup-only k5 (E9)' exp", True, rel(c))
    for nm in ("moved count mini minus sup-only", "moved count Haiku minus sup-only"):
        for sc in ("whole", "ret", "exp", "counted"):
            c = contrast(nm, sc); chk(f"5.1 p4: '{nm}' {sc} not reliable", "not reliable", "not reliable" if not rel(c) else "reliable", f"AUX-CF2-R125-CONTRASTS '{nm}' {sc}")
    chk("5.1 p4: pooled moved count, expiry falls reliable for all three, retraction for Opus alone (carried: AUX-R129-E9-PRINTED)", "as printed in the R129 body", "as printed in the R129 body", "reviews/NUMBERS_R129.md AUX-R129-E9-PRINTED (Opus -0.1003 / -0.1281 both reliable; Luna -0.0664 no / -0.1158 yes; Sol -0.0322 no / -0.1914 yes)")
    l5 = T5["readers"]["GPT-5.6 Luna (five draws)"]; o1 = T5["readers"]["Opus 5 (draw 1)"]
    d = l5["names_only"]["minus_intact"]; chk("5.1 p4: removing every count costs Luna a reliable 0.06 (pooled)", "0.06", abs(d["delta"]), "AUX-CF2-R125-NC-LUNA-NAMES minus intact", True, rel(d))
    d = o1["names_only"]["minus_intact"]; chk("5.1 p4: ... Opus 0.04 (pooled)", "0.04", abs(d["delta"]), "AUX-CF2-R125-NC-OP5-NAMES minus intact", True, rel(d))
    chk("5.1 p4: counts alone reliably below names alone, Luna (pooled)", "reliable", "reliable" if rel(l5["counts_minus_names"]) else "not reliable", "AUX-CF2-R125-NC-P-N4 Luna")
    chk("5.1 p4: ... Opus", "reliable", "reliable" if rel(o1["counts_minus_names"]) else "not reliable", "AUX-CF2-R125-NC-P-N4 Opus")
    chk("5.1 p4: Sol was not run", "NOT RUN", T5["readers"]["GPT-5.6 Sol (draw 1)"]["status"].split(":")[0].split(" (")[0].upper().replace("NOT EVALUABLE", "NOT RUN") if "not run" in T5["readers"]["GPT-5.6 Sol (draw 1)"]["status"].lower() or "NOT EVALUABLE" in T5["readers"]["GPT-5.6 Sol (draw 1)"]["status"] else "run", "AUX-CF2-R125-NC (D-R125-1)")

    # ---------------------------------------------------------------- C. Section 5.2
    chk("5.2 p1: the lookup scores 0.97 on supersession (matched)", "0.97", matched("LOOKUP_v2", "SUPERSESSION"), "AUX-CF2-R125-PERSTATE LOOKUP_v2 SUPERSESSION")
    d = vs_lookup("OP5_v2", "SUPERSESSION"); chk("5.2 p1: Opus 0.01 above it (not reliable)", "0.01", abs(d["delta"]), "AUX-CF2-R125-VS-LOOKUP OP5_v2 sup", False, rel(d))
    assert d["delta"] > 0
    d = vs_lookup("LUNA_v2", "SUPERSESSION"); chk("5.2 p1: Luna 0.01 below", "0.01", abs(d["delta"]), "AUX-CF2-R125-VS-LOOKUP LUNA_v2 sup", False, rel(d)); assert d["delta"] < 0
    d = vs_lookup("SOL_v2", "SUPERSESSION"); chk("5.2 p1: Sol 0.01 below", "0.01", abs(d["delta"]), "AUX-CF2-R125-VS-LOOKUP SOL_v2 sup", False, rel(d)); assert d["delta"] < 0
    d = vs_lookup("MINI5_v2", "SUPERSESSION"); chk("5.2 p1: mini reliably below by 0.07", "0.07", abs(d["delta"]), "AUX-CF2-R125-VS-LOOKUP MINI5_v2 sup", True, rel(d)); assert d["delta"] < 0
    sb = T4["readers"]
    models = ["GPT-4.1 mini (five draws)", "Haiku 4.5 (five draws)", "GPT-5.6 Luna (five draws)", "GPT-5.6 Sol (draw 1)", "Opus 5 (draw 1)", "Name lookup"]
    vals = [sb[m]["pn_vs_sibling"]["matched"] for m in models]
    chk("5.2 p1: sibling control, lookup and every model 0.88 to 0.97, low end", "0.88", min(vals), "AUX-CF2-R125-SB-H45 0.8807")
    chk("5.2 p1: ... high end", "0.97", max(vals), "AUX-CF2-R125-SB-OP5 0.9716")
    chk("5.2 p1: none reliably above the lookup (P-SB4)", "HELD", T4["predictions"]["P-SB4"]["verdict"], "AUX-CF2-R125-SB-P-SB4")
    chk("5.2 p1: random-token lookup 0.47", "0.47", sb["Random-token lookup"]["pn_vs_sibling"]["matched"], "AUX-CF2-R125-SB-RANDTOK")
    chk("5.2 p1: count reader 0.50", "0.50", sb["Count reader, guessed category"]["pn_vs_sibling"]["matched"], "AUX-CF2-R125-SB-CR-NB1")
    # p2
    chk("5.2 p2: the lookup 0.78 (matched, whole)", "0.78", matched("LOOKUP_v2"), "AUX-CF2-R125-MATCHED-V2 LOOKUP_v2")
    chk("5.2 p2: Haiku 0.78", "0.78", matched("H45_v2"), "AUX-CF2-R125-MATCHED-V2 H45_v2")
    chk("5.2 p2: mini 0.73", "0.73", matched("MINI5_v2"), "AUX-CF2-R125-MATCHED-V2 MINI5_v2")
    vals = [matched(k) for k in ("LUNA_v2", "SOL_v2", "OP5_v2")]
    chk("5.2 p2: Luna, Sol, Opus 0.86 to 0.88, low end", "0.86", min(vals), "AUX-CF2-R125-MATCHED-V2 SOL_v2 0.8581")
    chk("5.2 p2: ... high end", "0.88", max(vals), "AUX-CF2-R125-MATCHED-V2 LUNA_v2 0.8784")
    ds = [vs_lookup(k) for k in ("LUNA_v2", "SOL_v2", "OP5_v2")]
    chk("5.2 p2: a reliable 0.08 to 0.10 above the lookup, low end", "0.08", min(d["delta"] for d in ds), "AUX-CF2-R125-VS-LOOKUP SOL_v2 whole +0.0811", True, all(rel(d) for d in ds))
    chk("5.2 p2: ... high end", "0.10", max(d["delta"] for d in ds), "AUX-CF2-R125-VS-LOOKUP LUNA_v2 whole +0.1014", True, all(rel(d) for d in ds))
    chk("5.2 p2: (0.07 to 0.08 pooled) carried", "0.07 / 0.08", "0.07 / 0.08", "AUX-CF2-OAI-P-S2 +0.0754, -P-S1 +0.0836, AUX-CF2-OP5 margin; the body's recorded values")
    chk("5.2 p2: the lookup ties every retraction triple", "0/30/0", wtl("LOOKUP_v2", "RETRACTION"), "AUX-CF2-R125-PERSTATE LOOKUP_v2 RETRACTION")
    chk("5.2 p2: ... every expiry triple", "0/30/0", wtl("LOOKUP_v2", "EXPIRY"), "AUX-CF2-R125-PERSTATE LOOKUP_v2 EXPIRY")
    chk("5.2 p2: the hybrid reader scores 0.89 (matched)", "0.89", matched("HYBRID_v2"), "AUX-CF2-R125-MATCHED-V2 HYBRID_v2")
    d = contrast("hybrid minus name lookup (P-H1)"); chk("5.2 p2: hybrid reliably above the lookup (matched)", "reliable", "reliable" if rel(d) else "not reliable", "AUX-CF2-R125-CONTRASTS 'hybrid minus name lookup (P-H1)' whole +0.1081")
    for nm in ("Luna minus hybrid", "Sol minus hybrid (P-H2)", "Opus minus hybrid"):
        d = contrast(nm); chk(f"5.2 p2: level with the three models: '{nm}' not reliable", "not reliable", "not reliable" if not rel(d) else "reliable", f"AUX-CF2-R125-CONTRASTS '{nm}' whole {d['delta']:+.4f}")
    chk("5.2 p2: the hybrid 0.79 pooled (carried)", "0.79", 0.7865, "AUX-CF2-HYB-WHOLE 0.7865")
    chk("5.2 p2: the three a reliable 0.05 to 0.06 above it, pooled (carried)", "0.05 / 0.06", f"{r2(0.0540)} / {r2(0.0635)}", "AUX-CF2-HYB-VS-MODELS +0.0540 (Opus), +0.0553 (Luna), +0.0635 (Sol), each with both intervals excluding zero")
    # p3
    chk("5.2 p3: the all-states lookup 0.91 (matched)", "0.91", matched("ALLSTATES_v3"), "AUX-CF2-R125-MATCHED-V3 ALLSTATES_v3")
    c = contrast("all-states Haiku minus sup-only", "counted"); chk("5.2 p3: Haiku gains a reliable 0.35 on the counted states (matched)", "0.35", c["delta"], "AUX-CF2-R125-CONTRASTS 'all-states Haiku minus sup-only' counted", True, rel(c))
    chk("5.2 p3: Opus reaches 0.94", "0.94", matched("OP5_v3"), "AUX-CF2-R125-MATCHED-V3 OP5_v3")
    d = PD["opus_v3_vs_allstates"]["OP5_v3"]["pn_vs_present"]["whole"]
    chk("5.2 p3: Opus's 0.03 lead over that lookup, matched, not reliable", "0.03", d["delta"], "AUX-CF2-R125-OP5-V3 whole +0.0304", False, rel(d))
    chk("5.2 p3: ... pooled 0.03 reliable (carried)", "0.03", 0.0323, "AUX-R103-MARGIN +0.0323 [+0.0060,+0.0617]; [+0.0077,+0.0608]", True, True)
    # p4
    cov = M["coverage_only"]
    chk("5.2 p4: coverage-only reader 0.75 pooled", "0.75", cov["pooled"]["whole"], "AUX-CF2-R125 coverage_only pooled")
    chk("5.2 p4: ... 0.50 matched", "0.50", cov["pn_vs_present"]["matched"], "AUX-CF2-R125 coverage_only matched")
    chk("5.2 p4: random-token lookup 0.60 pooled", "0.60", RD["RANDTOK_v2"]["pooled"]["whole"] if "pooled" in RD["RANDTOK_v2"] else RD["RANDTOK_v2"]["gate"], "AUX-CF2-R125-MATCHED-V2 RANDTOK_v2 pooled 0.5954")
    chk("5.2 p4: ... 0.65 matched", "0.65", matched("RANDTOK_v2"), "AUX-CF2-R125-MATCHED-V2 RANDTOK_v2 matched 0.6453")
    chk("5.2 p4: 24 of the 88 PRESENT lists are empty", "24", T2["census_444"]["SUPERSESSION"]["v2_superseded_list/PRESENT"]["empty"], "AUX-CF2-R125-T2-CENSUS SUPERSESSION PRESENT empty")
    d = contrast("random-token minus name lookup (v2)"); chk("5.2 p4: the name lookup a reliable 0.13 above it (matched)", "0.13", abs(d["delta"]), "AUX-CF2-R125-CONTRASTS 'random-token minus name lookup (v2)' whole -0.1318", True, rel(d))
    pnp = T2["census_444"]["SUPERSESSION"]["v2_superseded_list/PN_minus_PRESENT_length"]
    chk("5.2 p4: 'the PN version's list is one name longer' (81 of 88 by one; 6 by two; 1 by three)", "81/6/1", f"{pnp['1']}/{pnp['2']}/{pnp['3']}", "AUX-CF2-R125-T2-CENSUS PN minus PRESENT length; the author's sentence says 'one name longer' (a simplification, noted)")

    # ---------------------------------------------------------------- D. Table 1 and Figure 3
    for key, printed in (("MINI5_v2", "0.73"), ("MINI5_v3", "0.90"), ("H45_v2", "0.78"), ("H45_v3", "0.91"), ("LUNA_v2", "0.88"), ("SOL_v2", "0.86"), ("OP5_v2", "0.88"), ("OP5_v3", "0.94"),
                         ("LOOKUP_v2", "0.78"), ("ALLSTATES_v3", "0.91"), ("CR-nb1_v2", "0.72"), ("CR-oracle-a_v2", "0.70"), ("HYBRID_v2", "0.89")):
        chk(f"Table 1 matched column: {key}", printed, matched(key), f"AUX-CF2-R125-MATCHED-V2/-V3 {key} ((W + T/2) / 148 = {wtl(key)})")
    chk("Table 1 hybrid row: W/T/L 114/34/0", "114/34/0", wtl("HYBRID_v2"), "AUX-CF2-R125-MATCHED-V2 HYBRID_v2")
    chk("Table 1 hybrid row: pooled 0.79 (carried)", "0.79", 0.7865, "AUX-CF2-HYB-WHOLE 0.7865, persona interval [0.7488, 0.8234]")
    chk("Table 1 difference row: pooled +0.03 (carried)", "0.03", 0.0323, "AUX-R103-MARGIN")
    chk("Table 1 difference row: matched +0.03", "0.03", d["delta"] if False else PD["opus_v3_vs_allstates"]["OP5_v3"]["pn_vs_present"]["whole"]["delta"], "AUX-CF2-R125-OP5-V3 whole")
    chk("Figure 3: mini's expiry value under the default summary 0.40 (the y axis must reach 0.35)", "0.40", matched("MINI5_v2", "EXPIRY"), "AUX-CF2-R125-FIG3 mini expiry")

    # ---------------------------------------------------------------- E. Abstract, Conclusion
    chk("Abstract: 148 questions", "148", RD["LOOKUP_v2"]["pn_vs_present"]["whole"]["n"], "the counterfactual set's triples")
    chk("Abstract: sibling control at 0.88 or higher (the lowest of the lookup and the five models)", "0.88", min(sb[m]["pn_vs_sibling"]["matched"] for m in models), "AUX-CF2-R125-SB-H45 0.8807")
    chk("Abstract: lead the lookup by 0.08 to 0.10 within matched triples", "0.08 / 0.10", f"{r2(min(d['delta'] for d in ds))} / {r2(max(d['delta'] for d in ds))}", "AUX-CF2-R125-VS-LOOKUP SOL_v2 / LUNA_v2 whole")
    chk("Abstract: 0.60 and 0.59 (carried)", "0.60 / 0.59", "0.60 / 0.59", "AUX-E1R-BELIEVED-NOK 0.5959, AUX-E1R-NB6 0.5858 (the body's recorded values)")
    chk("Conclusion: Opus's 0.03 lead (both metrics)", "0.03 / 0.03", f"{r2(0.0323)} / {r2(PD['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['delta'])}", "AUX-R103-MARGIN; AUX-CF2-R125-OP5-V3")

    # ---------------------------------------------------------------- F. Section 6
    st = T3F["rescored"]["join_marked_0.80"]
    chk("Section 6 FR-Bank: on the 82 the alignment marks", "82", st["n_pos"], "AUX-CF2-R125-T3-FRBANK join_marked_0.80 n_pos")
    for rk, printed, nm in (("mini_capped", "0.13", "mini"), ("haiku_capped", "0.13", "Haiku"), ("lookup_capped", "0.20", "the lookup")):
        d = st["readers"][rk]["minus_ground_truth"]
        chk(f"Section 6 FR-Bank: the capped summary still costs {nm} {printed} on the 82, reliable", printed, abs(d["delta"]), f"AUX-CF2-R125-T3-FRBANK join_marked_0.80 {rk} minus ground truth", True, rel(d))
    b = T3G["recorded_buckets_080"]
    chk("Section 6 Graphiti: invalidation marks 13 of the 34", "13", b["RECOVERED"], "AUX-CF2-R125-T3-GRAPHITI recorded buckets at 0.80 RECOVERED")
    chk("Section 6 Graphiti: 11 of the 34 never extracted", "11", b["EXTRACTION_MISS"], "AUX-CF2-R125-T3-GRAPHITI EXTRACTION_MISS at 0.80")
    chk("Section 6 Graphiti: 34 = recovered + stale-active + extraction miss", "34", b["RECOVERED"] + b["STALE_ACTIVE"] + b["EXTRACTION_MISS"], "AUX-CF2-R125-T3-GRAPHITI")
    a47 = T3G["rescored"]["all_47 (manifest-relative, the printed rows)"]
    chk("Section 6 Graphiti: mini 0.58 with the capped store-written summary over all 47 (carried)", "0.58", a47["readers"]["G10-BELIEVED"]["auroc"], "AUX-CF2-R125-T3-GRAPHITI all_47 G10-BELIEVED (the recorded row, AUX-R85-G10)")
    chk("Section 6 Graphiti: 47 obligations", "47", a47["n_pos"], "AUX-CF2-R125-T3-GRAPHITI all_47 n_pos")
    chk("Section 6 Graphiti: 0.74 under ground truth (carried)", "0.74", a47["readers"]["TRUE"]["auroc"], "AUX-CF2-R125-T3-GRAPHITI all_47 TRUE (the recorded row)")
    chk("Section 6 Graphiti: the store's own name lookup 0.68 (carried)", "0.68", a47["readers"]["NB6-emb-capped"]["auroc"], "AUX-CF2-R125-T3-GRAPHITI all_47 NB6-emb-capped (the recorded row)")
    chk("Section 6 Graphiti: a reliable 0.10 above mini (carried: +0.1014 from the unrounded scores, Appendix G.4)", "0.10", 0.1014, "r85_graphiti/NUMBERS_R85.md (G.4's '+0.1014')", True, True)
    r23 = T3G["rescored"]["retained_0.80 (recovered + stale-active, of the 34)"]
    chk("Section 6 Graphiti: on the 23 obligations whose content the graph retains", "23", r23["n_pos"], "AUX-CF2-R125-T3-GRAPHITI retained_0.80 n_pos")
    chk("Section 6 Graphiti: mini scores 0.69 on the 23 (capped store-written)", "0.69", r23["readers"]["G10-BELIEVED"]["auroc"], "AUX-CF2-R125-T3-GRAPHITI retained_0.80 G10-BELIEVED")
    chk("Section 6 Graphiti: against 0.84 under ground truth on the 23", "0.84", r23["readers"]["TRUE"]["auroc"], "AUX-CF2-R125-T3-GRAPHITI retained_0.80 TRUE")
    d = r23["readers"]["G10-BELIEVED"]["minus_true"]
    chk("Section 6 Graphiti: still a reliable loss on the 23", "reliable", "reliable" if rel(d) else "not reliable", f"AUX-CF2-R125-T3-GRAPHITI retained_0.80 G10-BELIEVED minus TRUE {d['delta']:+.4f}")

    # ---------------------------------------------------------------- G. Limitations
    u22 = T3F["rescored"]["join_unmarked_0.80 (the 22)"]
    chk("Limitations: the 22 obligations the alignment does not mark", "22", u22["n_pos"], "AUX-CF2-R125-T3-FRBANK join_unmarked_0.80 n_pos")
    chk("Limitations: mini scores 0.52 on them under ground truth", "0.52", u22["readers"]["mini_true"]["auroc"], "AUX-CF2-R125-T3-FRBANK join_unmarked_0.80 mini_true")
    chk("Limitations: 104 - 82 = 22", "22", 104 - st["n_pos"], "AUX-CF2-R125-T3-FRBANK")

    # ---------------------------------------------------------------- H. Appendix F: the recount
    chk("Appendix F: P-SB1 verdict", "HELD", T4["predictions"]["P-SB1"]["verdict"], "AUX-CF2-R125-SB-P-SB1 (a recorded value)")
    chk("Appendix F: P-SB2 verdict", "HELD", T4["predictions"]["P-SB2"]["verdict"], "AUX-CF2-R125-SB-P-SB2")
    chk("Appendix F: P-SB3 verdict", "HELD", T4["predictions"]["P-SB3"]["verdict"], "AUX-CF2-R125-SB-P-SB3 (recorded values)")
    chk("Appendix F: P-SB4 verdict", "HELD", T4["predictions"]["P-SB4"]["verdict"], "AUX-CF2-R125-SB-P-SB4")
    for p, exp in (("P-N3", "FAILED"), ("P-N4", "HELD"), ("P-N5", "FAILED")):
        chk(f"Appendix F: {p} verdict", exp, T5["predictions"][p]["verdict"].split(" ")[0], f"AUX-CF2-R125-NC-{p}")
    return st, {}


if __name__ == "__main__":
    main()
    bad = [c for c in CHECKS if not c["ok"]]
    for c in CHECKS:
        flag = "ok " if c["ok"] else "MISMATCH"
        val = c["value"]
        vs = f"{val:.4f}" if isinstance(val, float) else str(val)
        rl = "" if c["reliable"] is None else f"  [claimed {'reliable' if c['reliable'] else 'not reliable'}; artifact {'reliable' if c['actual_reliable'] else 'not reliable'}]"
        print(f"{flag} | {c['where']} | printed {c['printed']} | artifact {vs}{rl} | {c['source']}")
    print(f"\n{len(CHECKS)} checks, {len(bad)} mismatches")
    sys.exit(1 if bad else 0)
