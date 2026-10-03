# -*- coding: utf-8 -*-
"""r139_number_gate.py -- the number gate of R139 (2026-09-23): every number and verdict the pass's new texts print, read from its artifact here,
independently of reviews/r139/results/r139_printed.json (which port_r139.py fills its texts from): the equivalence verdicts re-derived from the raw
90% / 95% bounds in equiv_r139.json (not from its 'reading' field), the pooled comparison beside the matched one (cf_pad_scores.json), the sibling
control's closest reader (reviews/r125/results/r125_t4_sibling.json), the crossover's cue list minus the best model (cf_scores_ix.json), the list
lengths and the length-only reader (length_r139.json), the comparison count (n_count_r139.json against the built text), Figure 3's bars
(r125_matched.json), and the words each sentence uses for them. Runs R134's, R135's and R137's checks first; with --built, the numeral-set checks
with this pass's printed forms and its C.2 tables allowed.
Usage: python reviews/r139/tools/r139_number_gate.py [--built]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402
import r135_number_gate as G135  # noqa: E402
import r137_number_gate as G137  # noqa: E402

RES = ROOT / "reviews" / "r139" / "results"
SUB = ROOT / "iclr2027_monitoring_submission"
TOL = 0.05
T1 = {"GPT-4.1 mini, five draws": "mini", "Haiku 4.5": "Haiku", "GPT-5.6 Luna": "Luna", "GPT-5.6 Sol": "Sol", "Opus 5": "Opus"}


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def verdict(r):
    rel = (r["ci95_a"][0] > 0 or r["ci95_a"][1] < 0) and (r["ci95_persona"][0] > 0 or r["ci95_persona"][1] < 0)
    eq = all(-TOL <= x <= TOL for x in r["ci90_a"] + r["ci90_persona"])
    if rel:
        return "reliably below" if r["delta"] < 0 else "reliably above"
    return "equivalent" if eq else "neither"


def signed(x):
    return ("+" if x >= 0 else "-") + G.r2(x)


def main_text():
    t = (SUB / "paper_v23.tex").read_text(encoding="utf-8", errors="replace")
    a, b = t.index("\\begin{abstract}"), t.rindex("\\label{main-text-end}")   # R140: rindex; a comment before the box names the label, so index() stopped short of the box
    s = "\n".join(l for l in t[a:b].split("\n") if not l.lstrip().startswith("%"))
    return " ".join(s.split())


# the main-text sentences that carry the E-iv groups; R140 (reviews/r140/tools/r140_number_gate.py) replaces the abstract's after its item 1
FRAGS139 = ["Within $0.05$, Luna, Sol and Opus are equivalent to the lookup on the short list; mini sits reliably below it on the matched metric only; for Haiku neither holds",
            "The three stronger ones are equivalent to it within $0.05$.", "the three stronger readers are equivalent to it within $0.05$"]


def checks139():
    chk = G.chk
    E = J("reviews/r139/results/equiv_r139.json")
    rows = E["rows"]
    mt = main_text()
    # ---- 1.1: the 90% bounds are the 5th / 95th percentiles of the printed draws: every row's 95% interval equals its stored source (equiv_r139.py's own checks)
    chk("C.2 / 1.1: the recomputed 95% intervals equal their stored sources", f"{E['checks']['n']}/{E['checks']['n']}", f"{E['checks']['ok']}/{E['checks']['n']}", "equiv_r139.json checks")
    chk("C.2 / 1.1: the tolerance", "0.05", E["tol"], "equiv_r139.json tol")
    for r in rows:
        v = verdict(r)
        assert r["reliable"] == v.startswith("reliably") and r["equivalent"] == (all(-TOL <= x <= TOL for x in r["ci90_a"] + r["ci90_persona"])), r
    # ---- E-iv: the groups, matched, short list, supersession, Table 1 settings; the pooled verdict beside
    pick = lambda cond, sc, met, rd: next(r for r in rows if (r["condition"], r["scope"], r["metric"], r["reader"]) == (cond, sc, met, rd))
    gm = {s: verdict(pick("default summary", "supersession", "matched", rd)) for rd, s in T1.items()}
    gp = {s: verdict(pick("default summary", "supersession", "pooled", rd)) for rd, s in T1.items()}
    chk("5.2 E-iv / abstract / Conclusion: the equivalent group (matched)", "Luna,Sol,Opus", ",".join(s for s in T1.values() if gm[s] == "equivalent"), "equiv_r139.json, re-derived from the bounds")
    chk("5.2 E-iv: reliably below (matched)", "mini", ",".join(s for s in T1.values() if gm[s] == "reliably below"), "as above")
    chk("5.2 E-iv: 'for Haiku neither holds' (matched)", "Haiku", ",".join(s for s in T1.values() if gm[s] == "neither"), "as above")
    chk("5.2 E-iv: mini 'on the matched metric only' (pooled: not reliable)", "neither", gp["mini"], "as above, pooled row")
    chk("5.2 E-iv: the three stronger readers are equivalent pooled too (no pooled verdict named for them)", "equivalent,equivalent,equivalent", ",".join(gp[s] for s in ("Luna", "Sol", "Opus")), "as above, pooled rows")
    for frag in FRAGS139:
        chk(f"main text carries: {frag[:70]}", "present", "present" if frag in mt else "absent", "the built main text")
    # ---- B6
    b6 = {r["reader"]: verdict(r) for r in rows if r["condition"].startswith("B6")}
    chk("5.2 B6: 'equivalence within 0.05 is neither shown nor excluded' (all three neither)", "neither,neither,neither", ",".join(b6.values()), f"equiv_r139.json B6 rows {list(b6)}")
    # ---- B1
    CP = J("cf_pad/results/cf_pad_scores.json")["readers"]
    three = [CP[m]["superseded"]["pooled"]["unpadded"] for m in ("LUNA", "SOL", "OP5")]
    chk("5.2 B1: 'Pooled, the lookup scores 0.92'", "0.92", CP["LOOKUP"]["superseded"]["pooled"]["unpadded"], "cf_pad_scores.json readers/LOOKUP/superseded/pooled/unpadded")
    chk("5.2 B1: 'the three 0.93'", "0.93", min(three), "readers/{LUNA,SOL,OP5}/superseded/pooled/unpadded")
    chk("5.2 B1: 'to 0.94'", "0.94", max(three), "as above")
    chk("5.2 B1: 'none reliably above it'", "none", "none" if not any(verdict(pick("default summary", "supersession", "pooled", rd)).startswith("reliably above") for rd in ("GPT-5.6 Luna", "GPT-5.6 Sol", "Opus 5")) else "some", "equiv_r139.json")
    # ---- B2
    SB = J("reviews/r125/results/r125_t4_sibling.json")["readers"]
    models = {k: v["minus_lookup_matched"] for k, v in SB.items() if k.startswith(("GPT", "Haiku", "Opus"))}
    closest = max(models, key=lambda k: models[k]["delta"])
    o = models[closest]
    chk("5.2 B2: the closest reader under the sibling control", "Opus 5 (draw 1)", closest, "r125_t4_sibling.json minus_lookup_matched")
    chk("5.2 B2: '+0.02'", "+0.02", signed(o["delta"]), "as above")
    chk("5.2 B2: '[-0.02, +0.07]' (the item-level interval, the wider)", "-0.02/+0.07", f"{signed(o['ci_triple']['ci_lo'])}/{signed(o['ci_triple']['ci_hi'])}", "as above ci_triple",
        reliable=False, actual_reliable=o["both_exclude_zero"])
    chk("5.2 B2: the item-level interval is the wider", "yes", "yes" if (o["ci_triple"]["ci_hi"] - o["ci_triple"]["ci_lo"]) >= (o["ci_persona"]["ci_hi"] - o["ci_persona"]["ci_lo"]) else "no", "as above")
    chk("main text carries B2's form", "present", "present" if "(Opus, the closest, $+0.02$ $[-0.02,+0.07]$)" in mt else "absent", "the built main text")
    # ---- B7
    IX = J("r82_counterfactual/cf2/results/cf_scores_ix.json")
    best = max(IX["readers"], key=lambda m: IX["readers"][m]["A"]["P1"]["same_store"]["auroc"])
    v = IX["readers"][best]["A"]["P1"]["vs_keyword_same"]
    pair = (-v["ci_pair"]["ci_hi"], -v["ci_pair"]["ci_lo"])
    chk("5.3 B7: the best model under the explicit rubric (crossover A, same store)", "OP5", best, "cf_scores_ix.json readers/*/A/P1/same_store")
    chk("5.3 B7: cue list minus the best model '+0.01'", "+0.01", signed(-v["delta"]), "the sign flip of readers/OP5/A/P1/vs_keyword_same")
    chk("5.3 B7: '[-0.02, +0.03]' (pair-clustered, the wider; not reliable)", "-0.02/+0.03", f"{signed(pair[0])}/{signed(pair[1])}", "as above ci_pair", reliable=False, actual_reliable=v["both_exclude_zero"])
    chk("main text carries B7's form", "present", "present" if "A fixed cue list is not reliably below the best model ($+0.01$ $[-0.02,+0.03]$)" in mt else "absent", "the built main text")
    # ---- the list lengths and the length-only reader
    L = J("reviews/r139/results/length_r139.json")
    u = L["unpadded_supersession_lists"]
    chk("abstract / C.2: '2.6 names on average' (PN, supersession, default summary)", "2.6", f"{u['pn_mean']:.1f}" if abs(u["pn_mean"] - 2.625) < 1e-9 else u["pn_mean"], "length_r139.json (2.625, one decimal half-up: 2.6)")
    chk("C.2: 'at most 6'", "6", u["pn_max"], "length_r139.json")
    chk("C.2: '24 of the 88 PRESENT lists are empty'", "24/88", f"{u['present_empty']}/{u['n']}", "length_r139.json (AUX-CF2-R125-T2-CENSUS agrees)")
    h = L["hist_pn_minus_sibling"]
    chk("5.2 B5: 'one to three names longer ... in every supersession triple, on the short list and the padded one alike'", "1-3 both", "1-3 both" if set(h["padded|supersession"]) == set(h["unpadded|supersession"]) == {"1", "2", "3"} else "other", "length_r139.json hist")
    chk("5.2 B5: 'separates them in every such triple' (both lists)", "88/0/0 88/0/0", f"{L['padded']['supersession']['W']}/{L['padded']['supersession']['T']}/{L['padded']['supersession']['L']} {L['unpadded']['supersession']['W']}/{L['unpadded']['supersession']['T']}/{L['unpadded']['supersession']['L']}", "length_r139.json")
    chk("C.2: the sibling control ties every triple", "0/88/0", f"{L['sibling']['supersession']['W']}/{L['sibling']['supersession']['T']}/{L['sibling']['supersession']['L']}", "length_r139.json")
    chk("C.2: 'perfect pooled' on the padded lists", "1.0000", f"{L['padded']['supersession']['pooled']:.4f}", "length_r139.json")
    chk("C.2: by one name on 81 triples, two on 6, three on 1", "81/6/1", "/".join(str(h["unpadded|supersession"][k] // 2) for k in ("1", "2", "3")), "length_r139.json hist (two siblings per triple)")
    # ---- A2: the comparison count in the built text
    NC = J("reviews/r139/results/n_count_r139.json")
    m = re.search(r"reliable describes each of the \$(\d+)\$ comparisons the main text makes on its own", mt)
    chk("4 A2: the comparison count printed", str(NC["n_distinct"]), m.group(1) if m else "absent", "n_count_r139.json (AUX-R139-N)")
    # ---- Figure 3's bars
    R = J("reviews/r125/results/r125_matched.json")["readers"]
    f3 = (ROOT / "reviews" / "v23" / "src" / "fig3_data_matched.tex").read_text(encoding="utf-8")
    if "miniP" in f3:
        bad = 0
        for blk, keys in (("figthreeSup", {"mini": "MINI5_v2", "haiku": "H45_v2", "luna": "LUNA_v2", "sol": "SOL_v2", "opus": "OP5_v2", "lookup": "LOOKUP_v2", "count": "CR-nb1_v2"}),
                          ("figthreeAll", {"mini": "MINI5_v3", "haiku": "H45_v3", "opus": "OP5_v3", "lookup": "ALLSTATES_v3"})):
            seg = f3[:f3.index("}\\" + blk)]
            seg = seg[seg.rindex("\\pgfplotstableread"):]
            lines = [l.split(",") for l in seg.splitlines()[1:] if l and l[0].isdigit()]
            hdr = seg.splitlines()[1].split(",")
            for i, st in enumerate(("SUPERSESSION", "RETRACTION", "EXPIRY")):
                for k, rk in keys.items():
                    b = R[rk]["pn_vs_present"]["per_state"][st]
                    val, up, dn = (float(lines[i][hdr.index(x)]) for x in (k, k + "P", k + "M"))
                    bad += not (abs(val - b["matched"]) < 5e-5 and abs(val + up - b["ci_persona"]["ci_hi"]) < 1e-4 and abs(val - dn - b["ci_persona"]["ci_lo"]) < 1e-4)
        chk("Figure 3: every point and persona-grouped bar against r125_matched.json", "0", str(bad), "reviews/r125/results/r125_matched.json readers/*/pn_vs_present/per_state/*/ci_persona")


def allowed139():
    """The numerals R139 prints: the main text's forms and the C.2 tables' and prose's (from the artifacts, in the formats port_r139.py writes)."""
    E = J("reviews/r139/results/equiv_r139.json")
    L = J("reviews/r139/results/length_r139.json")
    NC = J("reviews/r139/results/n_count_r139.json")
    main = {"0.92", "0.93", "0.94", "+0.02", "0.02", "-0.02", "+0.07", "0.07", "+0.01", "0.01", "+0.03", "0.03", "2.6", "6", "0.05", str(NC["n_distinct"]), "95%", "95"}
    R = J("reviews/r125/results/r125_matched.json")["readers"]
    for rk in ("MINI5_v2", "H45_v2", "LUNA_v2", "SOL_v2", "OP5_v2", "LOOKUP_v2", "CR-nb1_v2", "MINI5_v3", "H45_v3", "OP5_v3", "ALLSTATES_v3"):
        for st in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
            b = R[rk]["pn_vs_present"]["per_state"][st]
            main |= {f"{b['ci_persona']['ci_hi'] - b['matched']:.4f}", f"{b['matched'] - b['ci_persona']['ci_lo']:.4f}", f"{b['matched']:.4f}"}
    appx = {"5%", "90%", "95%", "1,000", "0.05", "+0.05", "-0.05", "60", "88", "81", "6", "1", "2", "3", "2.6", "24", "148", "0", "115", "5", "7", "9", "10"}
    for r in E["rows"]:
        for x in [r["delta"]] + r["ci95_a"] + r["ci95_persona"] + r["ci90_a"] + r["ci90_persona"]:
            appx |= {f"{x:+.4f}", f"{x:.4f}".lstrip("-"), f"{x:+.4f}".lstrip("+")}
    for summ in ("padded", "unpadded", "sibling"):
        for v in L[summ].values():
            appx |= {f"{v['pooled']:.4f}", f"{v['matched']:.4f}", str(v["n_items"]), str(v["n_triples"]), str(v["W"]), str(v["T"]), str(v["L"])}
            appx |= {f"{x:.4f}" for x in v["pooled_persona_ci"] + v["matched_triple_ci"] + v["matched_persona_ci"]}
            appx.add(f"{v['W']}/{v['T']}/{v['L']}")
    for hh in L["hist_pn_minus_sibling"].values():
        appx |= set(hh) | {str(n) for n in hh.values()}
    return main, appx


def main():
    G.checks()
    n134 = len(G.CHECKS)
    G135.checks135()
    G137.checks137()
    n137 = len(G.CHECKS)
    checks139()
    bad = [c for c in G.CHECKS if not c["ok"]]
    for c in G.CHECKS[n137:]:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rl = "" if c["reliable"] is None else f"  reliable claimed={c['reliable']} actual={c['actual_reliable']}"
        print(f"  [{'ok' if c['ok'] else 'MISMATCH'}] {c['where']}: printed {c['printed']} <- {vs}{rl}  ({c['source']})")
    print(f"r139_number_gate: {len(G.CHECKS)} checks (R134's {n134}, R135's and R137's {n137 - n134}, this pass's {len(G.CHECKS) - n137}), {len(bad)} mismatches")
    if "--built" in sys.argv:
        m139, a139 = allowed139()
        pf = G.printed_forms

        def printed_forms():
            main_, appx = pf()
            extra135 = {"0.65", "0.13", "0.95", "0.88", "0.97", "0.01", "0.28", "0.33", "0.06", "0.04", "0.50", "0.02", "0.67", "0.60", "0.14",
                        "0.73", "0.82", "0.75", "0.71", "0.59", "0.12", "90", "69", "2,333", "1", "452", "15", "35", "60", "88", "115", "10"}
            extra137 = {"0.92", "0.74", "0.18", "0.07", "0.09", "0.10", "102", "33", "377", "197", "49"}
            appx137 = {"0.18", "0.13", "0.14", "264", "57", "41.5", "71", "102", "121", "43", "8.11", "15.54", "2,220", "2220", "0.9317", "0.9716", "-0.2236", "-0.2776", "-0.1690", "-0.3416", "-0.1294",
                       "0.8400", "0.8682", "-0.1873", "-0.2277", "-0.1476", "-0.2569", "-0.1278", "45", "46", "0.05", "60", "20", "12", "5", "1", "4", "2", "0", "88", "444", "148",
                       "+0.1375", "+0.1274", "-0.0336", "-0.0062", "-0.0525", "-0.1807", "0.1375", "0.1274", "0.0336", "0.0062", "0.0525", "0.1807", "9", "33", "102", "30", "90"}
            return main_ | extra135 | extra137 | m139, appx | appx137 | a139
        G.printed_forms = printed_forms
        frag = set()
        for f in sorted((ROOT / "cf_pad" / "results").glob("cfpad_tab_*.tex")):
            frag |= G.numerals(f.read_text(encoding="utf-8"))
        frag = {t.lstrip("+") for t in frag} | frag
        pf2 = G.printed_forms

        def printed_forms2():
            main_, appx = pf2()
            return main_, appx | frag
        G.printed_forms = printed_forms2
        bad += G.built_checks()
    if bad:
        print("r139_number_gate: FAIL")
        sys.exit(1)
    print("r139_number_gate: PASS")


if __name__ == "__main__":
    main()
