# -*- coding: utf-8 -*-
"""held_texts_r122.py -- R122: write HELD_TEXTS.md from the result artifacts (enc_lookup.json, scores_r122_oai.json, gate_reach.json). Both branches
of every task are written (the registrations' section 5/6 texts with the numbers filled), the branch the verdict selects marked. No number is typed
by hand; the paper prints two decimals in the body and the appendix tables carry four. Nothing lands by this file.
"""
from __future__ import annotations

import io
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r122_common as C  # noqa: E402

STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")


def f2(x):
    return f"{x:.2f}"


def s2(x):
    return f"{x:+.2f}"


def ci2(d):
    return f"[{d['ci_lo']:+.2f}, {d['ci_hi']:+.2f}]"


def ci4(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def t1(E):
    enc = E["encoders"]; rt = E["random_token"]; P = E["predictions"]["P-E1"]
    codes = [d["code"] for d in E["loaded"]]
    names = {c: enc[c]["model"].split("/")[-1] for c in codes}
    a = {c: enc[c]["v2"]["whole"] for c in codes}
    hold = P["verdict"] == "HOLDS"
    L = ["## T1. Lookup encoders (ADDENDUM_R122_ENCODERS.md) — P-E1 **" + P["verdict"] + "**", "",
         "### Branch: P-E1 holds" + ("  ← selected" if hold else ""), "",
         f"Appendix C.2, after the sentence naming `all-MiniLM-L6-v2`: \"Two further encoders, `{names[codes[0]]}` and `{names[codes[1]]}`, score the same lookup at "
         f"${f2(a[codes[0]])}$ and ${f2(a[codes[1]])}$ on the counterfactual set, within $0.05$ of MiniLM; replacing every name by a random token scores ${f2(rt['MINILM']['v2']['whole'])}$ "
         f"(Table~\\ref{{tab:enc-lookup}}).\" No body sentence changes.", "",
         "### Branch: P-E1 fails" + ("  ← selected" if not hold else ""), ""]
    worst = max(codes, key=lambda c: abs(enc[c]["v2"]["vs_minilm"]["delta"]))
    d = enc[worst]["v2"]["vs_minilm"]
    L += [f"Appendix C.2: \"`{names[worst]}` scores the lookup at ${f2(a[worst])}$, ${s2(d['delta'])}$ from MiniLM (intervals ${ci2(d['item_ci'])}$; ${ci2(d['persona_ci'])}$).\" "
          f"Limitations, on the sentence naming the lookup: \"and the lookup's level moves by ${s2(d['delta'])}$ under a second encoder\".", "",
          "### Appendix table `tab:enc-lookup` (both branches)", "",
          "| encoder | 444, v2 [persona CI] | minus MiniLM (item; persona) | 444, v3 [persona CI] | minus MiniLM | 661 [persona CI] | minus MiniLM | 661, marker-free |", "|---|---|---|---|---|---|---|---|"]
    for c in ["MINILM"] + codes:
        B = enc[c]
        def cell(pop):
            b = B[pop]; return f"${b['whole']:.4f}$ $[{b['ci_persona']['ci_lo']:.4f}, {b['ci_persona']['ci_hi']:.4f}]$"
        def mm(pop):
            if c == "MINILM":
                return "—"
            p = B[pop]["vs_minilm"]; return f"${p['delta']:+.4f}$ ${ci4(p['item_ci'])}$; ${ci4(p['persona_ci'])}$"
        L.append(f"| {B['model'].split('/')[-1]}{' (recorded)' if c == 'MINILM' else ''} | {cell('v2')} | {mm('v2')} | {cell('v3')} | {mm('v3')} | {cell('661')} | {mm('661')} | ${B['661_clean']['whole']:.4f}$ |")
    for c in ["MINILM"] + codes:
        B = rt[c]
        L.append(f"| random tokens, {enc[c]['model'].split('/')[-1]} | ${B['v2']['whole']:.4f}$ $[{B['v2']['ci_persona']['ci_lo']:.4f}, {B['v2']['ci_persona']['ci_hi']:.4f}]$ | — | ${B['v3']['whole']:.4f}$ | — | ${B['661']['whole']:.4f}$ | — | ${B['661_clean']['whole']:.4f}$ |")
    L += ["", f"Note for the table's caption: the 661 column is the committed form (an empty section's `(none)` marker encoded as a name); the marker-free column is the fair cross-encoder comparison on the 661 "
          f"(`bge-small` reads ${enc['BGE']['661']['whole']:.4f}$ committed and ${enc['BGE']['661_clean']['whole']:.4f}$ marker-free)." if "BGE" in enc else ""]
    return L


def t3(T):
    P = T["predictions"]["P-K1"]; hold = P["verdict"] == "HOLDS"; v2, v3 = T["INDEXED-V2"], T["INDEXED-V3"]
    L = ["## T3. GPT-4.1 mini at five draws (ADDENDUM_R122_MINI_K5.md) — P-K1 **" + P["verdict"] + "**", "",
         "### Branch: P-K1 holds" + ("  ← selected" if hold else ""), "",
         f"Appendix C.2, after the single-draw note: \"At five draws with the provider's default temperature GPT-4.1 mini reads ${f2(v2['new']['whole'])}$ under the superseded-only summary and "
         f"${f2(v3['new']['whole'])}$ under the all-states summary, within $0.05$ of its one-draw rows, with the tied triples falling from ${v2['recorded']['tied_triples']}$ to ${v2['new']['tied_triples']}$ "
         f"(Table~\\ref{{tab:mini-k5}}).\" The single-draw qualification in `tab:runs` and the body's \"run once per item\" stand, the five-draw row cited beside them.", "",
         "### Branch: P-K1 fails" + ("  ← selected" if not hold else ""), ""]
    for arm, name in (("INDEXED-V2", "superseded-only"), ("INDEXED-V3", "all-states")):
        d = T[arm]["new_minus_recorded"]["whole"]; a, b = T[arm]["new"], T[arm]["recorded"]
        L.append(f"- {name}: \"moves by ${s2(d['delta'])}$ at five draws (intervals ${ci2(d['item_ci'])}$; ${ci2(d['persona_ci'])}$); the tied triples move from ${b['tied_triples']}$ to ${a['tied_triples']}$\"; "
                 f"on the AUROC clause the body's Table 1 note on mini's single draw gains \"a five-draw run moves it by ${s2(d['delta'])}$ (Appendix C.2)\"; on the tie clause only, nothing in the body changes.")
    d2 = v2["new_minus_recorded"]["whole"]; d3 = v3["new_minus_recorded"]["whole"]; l2 = v2["new"]["vs_lookup"]
    L += ["", "### Rider for the author's ruling (not in the registered text; the numbers as they came out)", "",
          f"The five-draw row is above the one-draw row reliably on both summaries (${s2(d2['delta'])}$, ${ci2(d2['item_ci'])}$; ${ci2(d2['persona_ci'])}$ under the superseded-only summary; "
          f"${s2(d3['delta'])}$, ${ci2(d3['item_ci'])}$; ${ci2(d3['persona_ci'])}$ under the all-states summary), and at five draws GPT-4.1 mini sits within tolerance of the name lookup "
          f"(${s2(l2['delta'])}$, ${ci2(l2['item_ci'])}$; ${ci2(l2['persona_ci'])}$) where the recorded one-draw row is below it by $-0.05$ with the persona interval excluding zero. "
          f"Two things changed between the rows, the draws and the temperature (D-R122-1), so the appendix sentence should say \"at five draws with the provider's default temperature\", as the registered text does; "
          f"Section 5's \"The lookup is not exceeded on the whole set by GPT-4.1 mini or Haiku 4.5\" stands on either row (the five-draw margin is not reliably positive).",
          "", "### Appendix table `tab:mini-k5` (both branches)", "",
          "| summary | row | whole [persona CI] | minus the lookup (item; persona) | sup. / retr. / exp. | PN vs PRESENT | W/T/L | distinct values | tied triples |", "|---|---|---|---|---|---|---|---:|---:|"]
    for arm, name in (("INDEXED-V2", "superseded-only"), ("INDEXED-V3", "all-states")):
        for key, lab in (("recorded", "one draw, temperature 0 (recorded)"), ("new", "five draws, provider default")):
            r = T[arm][key]; o = r["posthoc"]["whole"]["ordering"]; vl = r["vs_lookup"]
            L.append(f"| {name} | {lab} | ${r['whole']:.4f}$ $[{r['whole_ci_persona']['ci_lo']:.4f}, {r['whole_ci_persona']['ci_hi']:.4f}]$ | ${vl['delta']:+.4f}$ ${ci4(vl['item_ci'])}$; ${ci4(vl['persona_ci'])}$ | "
                     + " / ".join(f"${r['per_state'][s]['auroc']:.4f}$" for s in STATES) + f" | ${r['posthoc']['whole']['pn_vs_present']:.4f}$ | {o['wins']}/{o['ties']}/{o['losses']} | {r['distinct_values']} | {r['tied_triples']} |")
        d = T[arm]["new_minus_recorded"]["whole"]
        L.append(f"| {name} | five minus one | ${d['delta']:+.4f}$ ${ci4(d['item_ci'])}$; ${ci4(d['persona_ci'])}$ | | " + " / ".join(f"${T[arm]['new_minus_recorded']['per_state'][s]['delta']:+.4f}$" for s in STATES) + " | | | | |")
    return L


def t4(T):
    P = T["predictions"]; hold = all(P[k]["verdict"] == "HOLDS" for k in ("P-R1", "P-R2", "P-R3"))
    lu, mi = T["LUNA"], T["MINI"]; vl = lu["new"]["vs_lookup"]
    L = ["## T4. The counterfactual set under the intent-explicit rubric (ADDENDUM_R122_CF2_P1.md) — P-R1 **" + P["P-R1"]["verdict"] + "**, P-R2 **" + P["P-R2"]["verdict"] + "**, P-R3 **" + P["P-R3"]["verdict"] + "**", "",
         "### Branch: all three hold" + ("  ← selected" if hold else ""), "",
         f"Limitations (replacing R121's \"The main study was not rerun under the intent-explicit rubric.\" if landed; else Appendix C.2 after the intent-crossover paragraph): "
         f"\"Under the intent-explicit rubric the counterfactual set reads within $0.05$ of the frozen rubric for GPT-5.6 Luna and GPT-4.1 mini (${f2(lu['new']['whole'])}$ against ${f2(lu['recorded']['whole'])}$; "
         f"${f2(mi['new']['whole'])}$ against ${f2(mi['recorded']['whole'])}$), with the same per-state order, and Luna keeps a reliable margin over the name lookup (${s2(vl['delta'])}$, intervals ${ci2(vl['item_ci'])}$; "
         f"${ci2(vl['persona_ci'])}$; Appendix C.2).\"", "",
         "### Branch: a prediction fails" + ("  ← selected" if not hold else ""), ""]
    for c, name in (("LUNA", "GPT-5.6 Luna"), ("MINI", "GPT-4.1 mini")):
        d = T[c]["new_minus_recorded"]["whole"]; r1 = P["P-R1"]["per_reader"][c]; r2 = P["P-R2"]["per_reader"][c]
        L.append(f"- P-R1 on {name}{' (fails)' if not r1['within'] else ''}: \"the intent-explicit rubric moves {name} by ${s2(d['delta'])}$ on the counterfactual set (intervals ${ci2(d['item_ci'])}$; ${ci2(d['persona_ci'])}$)\".")
        L.append(f"- P-R2 on {name}{' (fails)' if not r2['same'] else ''}: P0 order {' > '.join(s.lower() for s in r2['order_p0'])}, P1 order {' > '.join(s.lower() for s in r2['order_p1'])}; per state P1 / P0: "
                 + ", ".join(f"{s.lower()} ${T[c]['new']['per_state'][s]['auroc']:.4f}$ / ${T[c]['recorded']['per_state'][s]['auroc']:.4f}$" for s in STATES) + ".")
    L.append(f"- P-R3{' (fails)' if not P['P-R3']['holds'] else ''}: \"and Luna's margin over the name lookup is ${s2(vl['delta'])}$ (intervals ${ci2(vl['item_ci'])}$; ${ci2(vl['persona_ci'])}$), "
             f"{'reliable' if vl['both_exclude_zero'] else 'not reliable'}, under it\"; on a failure Section 5's \"exceed it by $0.07$ to $0.08$\" sentence gains \"under the frozen rubric\".")
    mr2 = P["P-R2"]["per_reader"]
    failing = [c for c in ("LUNA", "MINI") if not mr2[c]["same"]]
    if failing:
        parts = []
        for c in failing:
            nm = "GPT-5.6 Luna" if c == "LUNA" else "GPT-4.1 mini"; n_, r_ = T[c]["new"]["per_state"], T[c]["recorded"]["per_state"]
            parts.append(f"{nm}'s two counted states swap (expiry ${f2(r_['EXPIRY']['auroc'])}$ to ${f2(n_['EXPIRY']['auroc'])}$, retraction ${f2(r_['RETRACTION']['auroc'])}$ to ${f2(n_['RETRACTION']['auroc'])}$, "
                         f"both moves' intervals including zero)")
        keep = [c for c in ("LUNA", "MINI") if mr2[c]["same"]]
        L += ["", "### Assembled sentence for the selected branch (the registered clauses joined; for the author's ruling)", "",
              f"\"Under the intent-explicit rubric the counterfactual set reads within $0.05$ of the frozen rubric for GPT-5.6 Luna and GPT-4.1 mini (${f2(lu['new']['whole'])}$ against ${f2(lu['recorded']['whole'])}$; "
              f"${f2(mi['new']['whole'])}$ against ${f2(mi['recorded']['whole'])}$); " + ("Luna keeps its per-state order and " if "LUNA" in keep else "") +
              f"{'Luna keeps ' if 'LUNA' not in keep else ''}a reliable margin over the name lookup (${s2(vl['delta'])}$, intervals ${ci2(vl['item_ci'])}$; ${ci2(vl['persona_ci'])}$), while " + "; ".join(parts) + " (Appendix C.2).\""]
    L += ["", "### Appendix table `tab:cf-p1` (both branches)", "",
          "| reader | rubric | whole [persona CI] | minus the lookup (item; persona) | sup. / retr. / exp. | PN vs PRESENT | W/T/L | distinct values | tied triples |", "|---|---|---|---|---|---|---|---:|---:|"]
    for c, name in (("LUNA", "GPT-5.6 Luna (k = 5)"), ("MINI", "GPT-4.1 mini (k = 1)")):
        for key, lab in (("recorded", "P0, frozen (recorded)"), ("new", "P1, intent-explicit")):
            r = T[c][key]; o = r["posthoc"]["whole"]["ordering"]; v = r["vs_lookup"]
            L.append(f"| {name} | {lab} | ${r['whole']:.4f}$ $[{r['whole_ci_persona']['ci_lo']:.4f}, {r['whole_ci_persona']['ci_hi']:.4f}]$ | ${v['delta']:+.4f}$ ${ci4(v['item_ci'])}$; ${ci4(v['persona_ci'])}$ | "
                     + " / ".join(f"${r['per_state'][s]['auroc']:.4f}$" for s in STATES) + f" | ${r['posthoc']['whole']['pn_vs_present']:.4f}$ | {o['wins']}/{o['ties']}/{o['losses']} | {r['distinct_values']} | {r['tied_triples']} |")
        d = T[c]["new_minus_recorded"]["whole"]
        L.append(f"| {name} | P1 minus P0 | ${d['delta']:+.4f}$ ${ci4(d['item_ci'])}$; ${ci4(d['persona_ci'])}$ | | " + " / ".join(f"${T[c]['new_minus_recorded']['per_state'][s]['delta']:+.4f}$" for s in STATES) + " | | | | |")
    return L


def t5(G):
    P = G["predictions"]; hold = all(P[k]["verdict"] == "HOLDS" for k in ("P-G1", "P-G2", "P-G3"))
    af, rc, tg = G["matched"]["AF"], G["matched"]["RECENCY"], G["matched"]["TAGGED"]; R = G["rows"]
    L = ["## T5. What the gate buys, reach only (ADDENDUM_R122_GATE_REACH.md) — P-G1 **" + P["P-G1"]["verdict"] + "**, P-G2 **" + P["P-G2"]["verdict"] + "**, P-G3 **" + P["P-G3"]["verdict"] + "**", "",
         "### Branch: all three hold" + ("  ← selected" if hold else ""), "",
         f"Section 8, after \"The lookup rule reaches the same $0.82$ and the oracle $0.95$\": \"The gate itself buys little reach: a fetch keyed on the best-matched name with no gate reaches ${f2(af['reach']['rate'])}$ at the same mean view, "
         f"spending ${f2(P['P-G2']['ratio'])}$ times the lines before matching, while a retrieval over the newest record per attribute reaches ${f2(rc['reach']['rate'])}$ (Appendix E.10).\"", "",
         "### Branch: a prediction fails" + ("  ← selected" if not hold else ""), "",
         f"- P-G1{' (fails)' if P['P-G1']['verdict'] != 'HOLDS' else ''}: \"The gate buys reach at the matched view: a fetch keyed on the best-matched name with no gate reaches ${f2(af['reach']['rate'])}$ against the rule's $0.82$ at the same mean view "
         f"(difference ${s2(af['reach']['minus_model']['D'])}$, intervals ${ci2(af['reach']['minus_model']['item'])}$; ${ci2(af['reach']['minus_model']['persona'])}$; Appendix E.10).\"",
         f"- P-G2{' (fails)' if P['P-G2']['verdict'] != 'HOLDS' else ''}: the cost clause is dropped and the appendix states the ratio ${P['P-G2']['ratio']:.4f}$ (${P['P-G2']['af5_mean_661']:.4f}$ against $5.43$ lines).",
         f"- P-G3{' (fails)' if P['P-G3']['verdict'] != 'HOLDS' else ''}: \"and a retrieval over the newest record per attribute reaches ${f2(rc['reach']['rate'])}$, within $0.05$ of the rule\" "
         f"(difference ${s2(rc['reach']['minus_model']['D'])}$, intervals ${ci2(rc['reach']['minus_model']['item'])}$; ${ci2(rc['reach']['minus_model']['persona'])}$).", "",
         "### Appendix table `tab:gate-reach` (both branches)", "",
         "| policy | forbidding record in view (of 104) | Wilson | sup. / retr. / exp. | minus MODEL (item; persona) | licensed record in view (of 174) | mean lines, 661 | mean lines, 104 |", "|---|---|---|---|---|---|---:|---:|"]
    def row(name, B):
        r = B["reach"]; ps = " / ".join(f"{r['per_state'][s]['reached']}/{r['per_state'][s]['n']}" for s in ("sup", "ret", "exp"))
        return (f"| {name} | ${r['reached']}$ = ${r['rate']:.4f}$ | $[{r['wilson'][0]:.3f}, {r['wilson'][1]:.3f}]$ | {ps} | ${r['minus_model']['D']:+.4f}$ ${ci4(r['minus_model']['item'])}$; ${ci4(r['minus_model']['persona'])}$ | "
                f"${B['licensed_in_view']['in_view']}$ = ${B['licensed_in_view']['rate']:.4f}$ | ${B['lines']['mean_661']:.2f}$ | ${B['lines']['mean_104']:.2f}$ |")
    def mrow(name, m):
        r = m["reach"]
        return (f"| {name} (matched: k = {m['k_lo']} and {m['k_hi']}, weight ${m['weight_hi']:.2f}$) | ${r['rate']:.4f}$ | — | — | ${r['minus_model']['D']:+.4f}$ ${ci4(r['minus_model']['item'])}$; ${ci4(r['minus_model']['persona'])}$ | "
                f"${m['licensed_in_view']['rate']:.4f}$ | ${m['achieved_mean']:.2f}$ | — |")
    L.append(f"| MODEL rule (recorded) | ${G['meta']['model_reach']}$ = ${G['meta']['model_reach'] / 104:.4f}$ | — | 53/63 / 20/26 / 12/15 | — | ${G['meta']['model_gold_in_view']}$ = ${G['meta']['model_gold_in_view'] / 174:.4f}$ | ${G['meta']['target_mean_661']:.2f}$ | ${G['meta']['target_mean_104']:.2f}$ |")
    L.append(row("ALWAYS-FETCH, five lines plus the fetch", R["AF"]["5"] if "5" in R["AF"] else R["AF"][5]))
    L.append(mrow("ALWAYS-FETCH", af))
    L.append(row("TAGGED-7 (recorded rows)", R["TAGGED"]["7"] if "7" in R["TAGGED"] else R["TAGGED"][7]))
    L.append(mrow("TAGGED", tg))
    L.append(row("RECENCY-7", R["RECENCY"]["7"] if "7" in R["RECENCY"] else R["RECENCY"][7]))
    L.append(mrow("RECENCY", rc))
    L += ["", f"Caption note: the fetch keyed on the best-matched name at four similarity lines reaches ${R['AF']['4' if '4' in R['AF'] else 4]['reach']['reached']}$ of 104 at ${R['AF']['4' if '4' in R['AF'] else 4]['lines']['mean_661']:.2f}$ lines; "
          f"the matched ALWAYS-FETCH row loses licensed records reliably (${af['licensed_in_view']['minus_model']['D']:+.4f}$, ${ci4(af['licensed_in_view']['minus_model']['item'])}$; ${ci4(af['licensed_in_view']['minus_model']['persona'])}$) because the truncated fill drops them; "
          f"RECENCY reaches no retraction obligation ({R['RECENCY']['7' if '7' in R['RECENCY'] else 7]['reach']['per_state']['ret']['reached']} of 26) because the retracted record is never the newest of its attribute."]
    return L


def main():
    E = C.jload(C.RESULTS / "enc_lookup.json"); G = C.jload(C.RESULTS / "gate_reach.json")
    S = C.jload(C.RESULTS / "scores_r122_oai.json") if (C.RESULTS / "scores_r122_oai.json").exists() else {}
    L = ["# HELD_TEXTS_R122 — one sentence per task for the body or Limitations, plus one appendix table each; both branches written; nothing landed (2026-09-19)", "",
         "Every number is read from `reviews/r122/results/*.json` by `tools/held_texts_r122.py`; the body prints two decimals, the tables four. The branch each verdict selects is marked. "
         "T2 (the hybrid reader) has no text here: it is R120's (`reviews/r120/registrations_draft/ADDENDUM_CF2_HYBRID_READER.md`).", ""]
    L += t1(E) + [""]
    if "T3" in S:
        L += t3(S["T3"]) + [""]
    else:
        L += ["## T3. GPT-4.1 mini at five draws — not yet scored", ""]
    if "T4" in S:
        L += t4(S["T4"]) + [""]
    else:
        L += ["## T4. The counterfactual set under P1 — not yet scored", ""]
    L += t5(G) + [""]
    io.open(C.R122 / "HELD_TEXTS.md", "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("wrote HELD_TEXTS.md:", len(L), "lines")


if __name__ == "__main__":
    main()
