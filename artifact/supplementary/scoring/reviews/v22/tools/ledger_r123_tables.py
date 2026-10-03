# -*- coding: utf-8 -*-
"""ledger_r123_tables.py -- program R123 (the v21 update and writing pass, 2026-09-19): the tables and table rows of the R121 and R122
results, written from the result artifacts (never typed by hand):
  tab:cf-intent    the intent crossover (R121), from r82_counterfactual/cf2/results/cf_scores_ix.json (AUX-CF2-IX-*)
  tab:cf-p1        the counterfactual set under the intent-explicit rubric (R122 T4), from reviews/r122/results/scores_r122_oai.json (AUX-R122-P1-*)
  tab:mini-k5      GPT-4.1 mini at five draws (R122 T3), from the same file (AUX-R122-K5-*)
  tab:enc-lookup   the lookup under two further encoders and the random-token control (R122 T1), from reviews/r122/results/enc_lookup.json (AUX-R122-ENC-*)
  tab:gatereach   what the gate buys, reach only (R122 T5), from reviews/r122/results/gate_reach.json (AUX-R122-GATE-*)
  tab:sup-margins  each model's supersession-only margin over the name lookup, from reviews/r117/results/sup_margins.json and the five-draw
                   GPT-4.1 mini row of scores_r122_oai.json (the amendment's recomputation; reviews/NUMBERS_R123.md AUX-R123-SUP-MARGINS)
  tab:reach        the Section 9 reach table, from reviews/v21/results/reach_rows_r123.json (the recorded policies) and gate_reach.json (the matched rows)
  cf_main_mini     Table 1's GPT-4.1 mini rows at five draws, and the note giving the recorded one-draw rows
Wide tables are set as two stacked panels so every row fits the text width. Writes reviews/v21/src/r123_tables_v21.tex (the record;
r123_apply.py splices its blocks at the anchors). No model call.
"""
from __future__ import annotations

import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "v21" / "src" / "r123_tables_v21.tex"
STATES = ("SUPERSESSION", "RETRACTION", "EXPIRY")


def J(p):
    return json.load(io.open(ROOT / p, encoding="utf-8"))


def ci(d):
    return f"$[{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]$"


def cia(d):
    return f"$[{d['ci_lo']:.4f},{d['ci_hi']:.4f}]$"


def f4(x):
    return f"${x:.4f}$"


def s4(x):
    return f"${x:+.4f}$"


def table(label, caption, panels, size="\\tiny", sep="1.5pt", spec="[H]"):
    """One table: a caption, a label, and one or more tabular panels ((colspec, header, rows) each), stacked with a small gap."""
    L = [f"\\begin{{table}}{spec}", f"\\caption{{{caption}}}", f"\\label{{{label}}}", f"\\centering{size}\\setlength{{\\tabcolsep}}{{{sep}}}"]
    for i, (colspec, header, rows) in enumerate(panels):
        L += [f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", header, "\\midrule"] + rows + ["\\bottomrule", "\\end{tabular}" + ("\\\\[4pt]" if i + 1 < len(panels) else "")]
    L.append("\\end{table}")
    return "\n".join(L)


def wtl(w):
    return f"{w[0]}/{w[1]}/{w[2]}" if isinstance(w, list) else f"{w['wins']}/{w['ties']}/{w['losses']}"


# ----------------------------------------------------------------------------------------------------------------------------- the crossover
def tab_cf_intent(B):
    d = J("r82_counterfactual/cf2/results/cf_scores_ix.json")
    R, LK = d["readers"], d["lookups"]
    order = [("MINI", "GPT-4.1 mini ($k=1$)"), ("H45", "Haiku 4.5 ($k=5$)"), ("LUNA", "GPT-5.6 Luna ($k=5$)"), ("OP5", "Opus 5 ($k=1$)"), ("SOL", "GPT-5.6 Sol ($k=1$; Amendment 1)")]
    rows_a, rows_b = [], []

    def add(name, pop, lab, blk):
        ss, it, po = blk["same_store"], blk["interaction"], blk["pooled"]
        rows_a.append(f"{name} & {pop} & {lab} & {f4(ss['auroc'])} & {cia(ss['ci_persona'])} & {cia(ss['ci_pair'])} & {wtl(ss['wtl'])} \\\\")
        rows_b.append(f"{name} & {pop} & {lab} & {s4(it['mean'])} & {ci(it['ci_persona'])} & {ci(it['ci_pair'])} & {f4(po['auroc'])} \\\\")
    for key, name in order:
        for pop in ("A", "B"):
            for rub, lab in (("P0", "main-study"), ("P1", "intent-explicit")):
                blk = R[key][pop][rub]
                add(name if (pop == "A" and rub == "P0") else "", pop, lab, blk)
                if "draw1" in blk:
                    add("\\quad draw 1 only", pop, lab, blk["draw1"])
        rows_a.append("\\addlinespace[1pt]"); rows_b.append("\\addlinespace[1pt]")
    rows_a.append("\\multicolumn{7}{@{}l}{\\textit{Readers with no generative-model call}}\\\\")
    rows_b.append("\\multicolumn{7}{@{}l}{\\textit{Readers with no generative-model call}}\\\\")
    for lk, name in (("name", "Name lookup"), ("keyword", "Keyword-intent lookup (fixed cue list)"), ("oracle", "Oracle-intent lookup")):
        for pop in ("A", "B"):
            add(name if pop == "A" else "", pop, "--", LK[pop][lk])
    cap = ("The intent crossover on the counterfactual set (registered; ADDENDUM\\_CF2\\_INTENT\\_CROSSOVER and its Amendment 1). Each supersession pair of the set is asked its recorded present-tense question and a second question about how the attribute has changed, of the same two store versions (\\pn{} and \\present{}) under the default summary (population A, $87$ of the $88$ pairs); each expiry pair is asked its recorded upcoming-intent question and a question about the past event under the all-states summary (population B, $26$ of the $30$ pairs); our read of the crossed questions dropped five pairs before any call. "
           "The crossed question makes the same stale record licensed, so a reader that conditions on intent scores the \\pn{} version of the original question above the same version under the crossed question. Upper panel: that same-store AUROC, chance $0.50$, with the persona-grouped and the pair-clustered interval and the within-pair W/T/L. Lower panel: the interaction, the mean of the two-by-two contrast, with both intervals, and the pooled AUROC of the original question's \\pn{} version against the other three cells. "
           "Each reader ran under the main-study rubric and under a rubric that states the intent rule. GPT-5.6 Luna and Haiku 4.5 ran five draws; their draw-1 rows are the column comparable with the one-draw readers, and the body reads that column. GPT-5.6 Sol was added after an interim read of three models' rows, and its prediction is labelled so in Appendix~\\ref{app:registration}; under the intent-explicit rubric it counts $76/0/11$ within pairs on population A, and in $9$ of its $11$ losses both questions score $0.96$ or higher, so the rule was not applied on those pairs. "
           "Under the intent-explicit rubric no model's discrimination on its original questions falls by more than $0.05$ (the largest fall $-0.0458$, Haiku 4.5 on population A; the largest rise $+0.1716$, GPT-4.1 mini on population B).")
    cap = cap.replace("Upper panel: that same-store AUROC", "This table: that same-store AUROC").replace("Lower panel: the interaction", "Table~\\ref{tab:cf-intent-b}: the interaction")
    cap_b = ("The intent crossover, continued from Table~\\ref{tab:cf-intent}: the interaction, the mean of the two-by-two contrast (the original question's \\pn{} version minus its \\present{} version, minus the same difference under the crossed question), "
             "with the persona-grouped and the pair-clustered interval, and the pooled AUROC of the original question's \\pn{} version against the other three cells, with the same readers, populations and rubrics.")
    B["cf_intent"] = ("%% R123: tab:cf-intent and tab:cf-intent-b, written by reviews/v21/tools/ledger_r123_tables.py from r82_counterfactual/cf2/results/cf_scores_ix.json (r82_counterfactual/cf2/NUMBERS_CF2.md section 14d, AUX-CF2-IX-*); do not edit by hand.\n"
                      + table("tab:cf-intent", cap, [("@{}lllrllr@{}", "Reader & pop. & rubric & same-store AUROC & persona interval & pair interval & W/T/L \\\\", rows_a)])
                      + "\n\n" + table("tab:cf-intent-b", cap_b, [("@{}lllrllr@{}", "Reader & pop. & rubric & interaction & persona interval & pair interval & pooled AUROC \\\\", rows_b)]))
    chk = {"mini_A_P0": R["MINI"]["A"]["P0"]["same_store"]["auroc"], "h45_A_P0": R["H45"]["A"]["P0"]["same_store"]["auroc"],
           "luna_A_P0": R["LUNA"]["A"]["P0"]["same_store"]["auroc"], "sol_A_P0": R["SOL"]["A"]["P0"]["same_store"]["auroc"],
           "op5_A_P0": R["OP5"]["A"]["P0"]["same_store"]["auroc"], "op5_B_P0": R["OP5"]["B"]["P0"]["same_store"]["auroc"],
           "sol_B_P0": R["SOL"]["B"]["P0"]["same_store"]["auroc"], "op5_A_P1": R["OP5"]["A"]["P1"]["same_store"]["auroc"],
           "luna_A_P1_d1": R["LUNA"]["A"]["P1"]["draw1"]["same_store"]["auroc"], "sol_A_P1": R["SOL"]["A"]["P1"]["same_store"]["auroc"],
           "cue_A": LK["A"]["keyword"]["same_store"]["auroc"], "mini_A_P1": R["MINI"]["A"]["P1"]["same_store"]["auroc"],
           "h45_A_P1": R["H45"]["A"]["P1"]["same_store"]["auroc"], "name_A": LK["A"]["name"]["same_store"]["auroc"], "name_B": LK["B"]["name"]["same_store"]["auroc"],
           "p_i5_h45_A": d["predictions"]["P-I5"]["readings"]["H45"]["A"], "p_i5_mini_B": d["predictions"]["P-I5"]["readings"]["MINI"]["B"]}
    want = {"mini_A_P0": "0.40", "h45_A_P0": "0.38", "luna_A_P0": "0.35", "sol_A_P0": "0.44", "op5_A_P0": "0.90", "op5_B_P0": "0.85", "sol_B_P0": "0.64",
            "op5_A_P1": "0.99", "luna_A_P1_d1": "0.96", "sol_A_P1": "0.88", "cue_A": "0.99", "mini_A_P1": "0.48", "h45_A_P1": "0.55", "name_A": "0.47", "name_B": "0.45",
            "p_i5_h45_A": "-0.05", "p_i5_mini_B": "0.17"}
    for k, v in want.items():
        assert f"{chk[k]:.2f}" == v, (k, chk[k], v)
    assert wtl(R["SOL"]["A"]["P1"]["same_store"]["wtl"]) == "76/0/11"
    return chk


# ---------------------------------------------------------------------------------------------- the two 'new row against recorded row' tables
def two_row_panels(T, entries, row_labels, diff_label):
    """entries: (key, name); row_labels: (recorded label, new label). Panel a: whole set and the lookup contrast; panel b: per state and post hoc."""
    rows_a, rows_b = [], []
    for c, name in entries:
        for key, lab in (("recorded", row_labels[0]), ("new", row_labels[1])):
            r = T[c][key]; o = r["posthoc"]["whole"]["ordering"]; v = r["vs_lookup"]
            nm = name if key == "recorded" else ""
            rows_a.append(f"{nm} & {lab} & {f4(r['whole'])} & {cia(r['whole_ci_persona'])} & {s4(v['delta'])} & {ci(v['item_ci'])} & {ci(v['persona_ci'])} \\\\")
            rows_b.append(f"{nm} & {lab} & " + " & ".join(f4(r['per_state'][s]['auroc']) for s in STATES) + f" & {f4(r['posthoc']['whole']['pn_vs_present'])} & {o['wins']}/{o['ties']}/{o['losses']} & {r['distinct_values']} & {r['tied_triples']} \\\\")
        d = T[c]["new_minus_recorded"]
        rows_a.append(f" & {diff_label} & {s4(d['whole']['delta'])} & & & {ci(d['whole']['item_ci'])} & {ci(d['whole']['persona_ci'])} \\\\")
        rows_b.append(f" & {diff_label} & " + " & ".join(s4(d['per_state'][s]['delta']) for s in STATES) + " & & & & \\\\")
        rows_a.append("\\addlinespace[1pt]"); rows_b.append("\\addlinespace[1pt]")
    return [("@{}llrlrll@{}", "Reader & row & whole set & persona interval & minus the lookup & item interval & persona interval \\\\", rows_a),
            ("@{}llrrrrrrr@{}", "Reader & row & supersession & retraction & expiry & PN vs PRESENT & W/T/L & distinct values & tied triples \\\\", rows_b)]


def tab_cf_p1(B):
    T = J("reviews/r122/results/scores_r122_oai.json")["T4"]
    cap = ("The counterfactual set under the intent-explicit rubric (registered; ADDENDUM\\_R122\\_CF2\\_P1): GPT-5.6 Luna at five draws and GPT-4.1 mini at one, each against its recorded row under the main-study rubric. Upper panel: whole set with the persona interval, and the margin over the name lookup with both intervals. Lower panel: the per-state values and the post hoc columns. "
           "Predicted before the run: each reader within $0.05$ of its recorded row (both readers, as predicted), the same per-state order (GPT-5.6 Luna as predicted; GPT-4.1 mini's two counted states swap, neither move reliable, a failed prediction), and Luna's margin over the lookup reliable (as predicted).")
    panels = two_row_panels(T, (("LUNA", "GPT-5.6 Luna ($k=5$)"), ("MINI", "GPT-4.1 mini ($k=1$)")), ("main-study (recorded)", "intent-explicit"), "intent-explicit minus main-study")
    B["cf_p1"] = ("%% R123: tab:cf-p1, written by reviews/v21/tools/ledger_r123_tables.py from reviews/r122/results/scores_r122_oai.json (reviews/r122/NUMBERS_R122.md, AUX-R122-P1-*); do not edit by hand.\n"
                  + table("tab:cf-p1", cap, panels, sep="1pt"))
    lu = T["LUNA"]; mi = T["MINI"]; vl = lu["new"]["vs_lookup"]
    assert f"{vl['delta']:+.2f}" == "+0.09" and vl["both_exclude_zero"], vl
    assert abs(lu["new_minus_recorded"]["whole"]["delta"]) < 0.02 and abs(mi["new_minus_recorded"]["whole"]["delta"]) < 0.02
    assert T["predictions"]["P-R2"]["verdict"] == "FAILS" and T["predictions"]["P-R1"]["verdict"] == "HOLDS" and T["predictions"]["P-R3"]["verdict"] == "HOLDS"
    return {"luna_p1": lu["new"]["whole"], "luna_p0": lu["recorded"]["whole"], "mini_p1": mi["new"]["whole"], "mini_p0": mi["recorded"]["whole"], "luna_margin": vl["delta"]}


def tab_mini_k5(B):
    T = J("reviews/r122/results/scores_r122_oai.json")["T3"]
    cap = ("GPT-4.1 mini at five draws on the counterfactual set (registered; ADDENDUM\\_R122\\_MINI\\_K5), under the default and the all-states summary, beside its recorded one-draw rows at temperature $0$. Upper panel: whole set with the persona interval, and the margin over the same summary's lookup with both intervals. Lower panel: per state, and the post hoc columns. "
           "The five-draw run used the provider's default temperature, so two things changed between the rows. Predicted before the run: the five-draw row within $0.05$ of the one-draw row and fewer tied triples, under both summaries (as predicted). Table~\\ref{tab:cf-main} prints the five-draw rows; the names-against-counts comparison of Table~\\ref{tab:cf-names-counts} keeps the one-draw row as its comparator.")
    panels = two_row_panels(T, (("INDEXED-V2", "default (superseded-only)"), ("INDEXED-V3", "all-states")), ("one draw, temperature $0$ (recorded)", "five draws, provider default"), "five minus one")
    B["mini_k5"] = ("%% R123: tab:mini-k5, written by reviews/v21/tools/ledger_r123_tables.py from reviews/r122/results/scores_r122_oai.json (reviews/r122/NUMBERS_R122.md, AUX-R122-K5-*); do not edit by hand.\n"
                    + table("tab:mini-k5", cap, panels, sep="1pt"))
    v2, v3 = T["INDEXED-V2"], T["INDEXED-V3"]
    assert T["predictions"]["P-K1"]["verdict"] == "HOLDS"
    n2, n3 = v2["new"], v3["new"]; r2, r3 = v2["recorded"], v3["recorded"]

    def two(r):
        o = r["posthoc"]["whole"]["ordering"]
        return (f"{r['whole']:.2f}", f"[{r['whole_ci_persona']['ci_lo']:.2f},{r['whole_ci_persona']['ci_hi']:.2f}]", f"{r['posthoc']['whole']['pn_vs_present']:.2f}", f"{o['wins']}/{o['ties']}/{o['losses']}")
    a2, a3 = two(n2), two(n3)
    assert two(r2)[0] == "0.72" and two(r3)[0] == "0.80" and r2["whole"] == 0.7167 and r3["whole"] == 0.7967
    B["cf_main_mini"] = "\n".join([
        f"GPT-4.1 mini, sup.\\ only$^{{a}}$ & ${a2[0]}$ & ${a2[1]}$ & ${a2[2]}$ & ${a2[3]}$ \\\\",
        f"GPT-4.1 mini, all three$^{{a}}$ & ${a3[0]}$ & ${a3[1]}$ & ${a3[2]}$ & ${a3[3]}$ \\\\"])
    B["cf_main_note"] = (f"$^{{a}}$GPT-4.1 mini's rows are its five-draw run at the provider's default temperature; its recorded one-draw rows at temperature $0$ read "
                         f"${r2['whole']:.2f}$ and ${r3['whole']:.2f}$ (Table~\\ref{{tab:mini-k5}}, Appendix~\\ref{{app:counterfactual}}).")
    sup = n2["per_state"]["SUPERSESSION"]["vs_lookup"]
    return {"k5_v2": n2["whole"], "k5_v3": n3["whole"], "k1_v2": r2["whole"], "k1_v3": r3["whole"], "tied_k1": r2["tied_triples"], "tied_k5": n2["tied_triples"],
            "sup_k5": n2["per_state"]["SUPERSESSION"]["auroc"], "sup_margin_k5": sup["delta"], "sup_item": (sup["item_ci"]["ci_lo"], sup["item_ci"]["ci_hi"]),
            "sup_persona": (sup["persona_ci"]["ci_lo"], sup["persona_ci"]["ci_hi"]), "sup_reliable": bool(sup["both_exclude_zero"])}


# ------------------------------------------------------------------------------------------------------------------------------ the encoders
def tab_enc_lookup(B):
    E = J("reviews/r122/results/enc_lookup.json")
    enc, rt = E["encoders"], E["random_token"]
    codes = [d["code"] for d in E["loaded"]]
    POPS = (("v2", "$444$, default"), ("v3", "$444$, all-states"), ("661", "$661$, committed"), ("661_clean", "$661$, marker-free"))
    rows = []
    for c in ["MINILM"] + codes:
        Bc = enc[c]
        nm = f"\\texttt{{{Bc['model'].split('/')[-1]}}}" + (" (recorded)" if c == "MINILM" else "")
        for i, (pop, plab) in enumerate(POPS):
            b = Bc[pop]
            cip = cia(b["ci_persona"]) if "ci_persona" in b else "--"
            if c == "MINILM" or "vs_minilm" not in b:
                rows.append(f"{nm if i == 0 else ''} & {plab} & {f4(b['whole'])} & {cip} & -- & -- & -- \\\\")
            else:
                p = b["vs_minilm"]
                rows.append(f"{nm if i == 0 else ''} & {plab} & {f4(b['whole'])} & {cip} & {s4(p['delta'])} & {ci(p['item_ci'])} & {ci(p['persona_ci'])} \\\\")
        rows.append("\\addlinespace[1pt]")
    rows.append("\\multicolumn{7}{@{}l}{\\textit{Random tokens in place of every name}}\\\\")
    for c in ["MINILM"] + codes:
        Bc = rt[c]
        nm = f"\\texttt{{{enc[c]['model'].split('/')[-1]}}}"
        for i, (pop, plab) in enumerate(POPS):
            b = Bc[pop]
            cip = cia(b["ci_persona"]) if "ci_persona" in b else "--"
            rows.append(f"{nm if i == 0 else ''} & {plab} & {f4(b['whole'])} & {cip} & -- & -- & -- \\\\")
        rows.append("\\addlinespace[1pt]")
    cap = ("The name lookup under two further sentence encoders, and the random-token control (registered; ADDENDUM\\_R122\\_ENCODERS): the same lookup code with the encoder swapped, on the counterfactual set under the default and the all-states summary and on the full obligation set, AUROC with the persona interval where recorded and the difference from the recorded \\texttt{all-MiniLM-L6-v2} lookup with both intervals. "
           "The full-obligation-set rows as committed read the summaries where an empty section's \\texttt{(none)} marker is encoded as a name; the marker-free rows drop the marker and are the fair cross-encoder comparison there. The control replaces every name by a random token, so what it scores comes from the list's length and from whether it is empty. "
           "Predicted before the run: both encoders within $0.05$ of MiniLM on the counterfactual set under the default summary (as predicted).")
    B["enc_lookup"] = ("%% R123: tab:enc-lookup, written by reviews/v21/tools/ledger_r123_tables.py from reviews/r122/results/enc_lookup.json (reviews/r122/NUMBERS_R122.md, AUX-R122-ENC-*); do not edit by hand.\n"
                       + table("tab:enc-lookup", cap, [("@{}llrlrll@{}", "Encoder & population, summary & AUROC & persona interval & minus MiniLM & item interval & persona interval \\\\", rows)], sep="1pt"))
    assert E["predictions"]["P-E1"]["verdict"] == "HOLDS"
    a = {c: enc[c]["v2"]["whole"] for c in codes}
    assert all(abs(enc[c]["v2"]["vs_minilm"]["delta"]) < 0.01 for c in codes), a
    return {"names": {c: enc[c]["model"].split("/")[-1] for c in codes}, "v2": a, "rt_v2": rt["MINILM"]["v2"]["whole"], "minilm_v2": enc["MINILM"]["v2"]["whole"]}


# ----------------------------------------------------------------------------------------------------------------------------- the gate's reach
def tab_gate_reach(B):
    G = J("reviews/r122/results/gate_reach.json")
    P = G["predictions"]; R = G["rows"]; M = G["matched"]
    af, rc, tg = M["AF"], M["RECENCY"], M["TAGGED"]
    rows_a, rows_b = [], []

    def row(name, Bk):
        r = Bk["reach"]; ps = " / ".join(f"{r['per_state'][s]['reached']}" for s in ("sup", "ret", "exp"))
        rows_a.append(f"{name} & ${r['reached']}$ = {f4(r['rate'])} & $[{r['wilson'][0]:.3f},{r['wilson'][1]:.3f}]$ & {ps} & {s4(r['minus_model']['D'])} & {ci(r['minus_model']['item'])} & {ci(r['minus_model']['persona'])} \\\\")
        rows_b.append(f"{name} & ${Bk['licensed_in_view']['in_view']}$ = {f4(Bk['licensed_in_view']['rate'])} & -- & -- & -- & ${Bk['lines']['mean_661']:.2f}$ & ${Bk['lines']['mean_104']:.2f}$ \\\\")

    def mrow(name, m):
        r = m["reach"]; lv = m["licensed_in_view"]
        nm = f"{name}, matched"
        rows_a.append(f"{nm} & {f4(r['rate'])} & -- & -- & {s4(r['minus_model']['D'])} & {ci(r['minus_model']['item'])} & {ci(r['minus_model']['persona'])} \\\\")
        rows_b.append(f"{nm} & {f4(lv['rate'])} & {s4(lv['minus_model']['D'])} & {ci(lv['minus_model']['item'])} & {ci(lv['minus_model']['persona'])} & ${m['achieved_mean']:.2f}$ & -- \\\\")
    rows_a.append(f"Model rule (recorded) & ${G['meta']['model_reach']}$ = {f4(G['meta']['model_reach'] / 104)} & -- & 53 / 20 / 12 & -- & -- & -- \\\\")
    rows_b.append(f"Model rule (recorded) & ${G['meta']['model_gold_in_view']}$ = {f4(G['meta']['model_gold_in_view'] / 174)} & -- & -- & -- & ${G['meta']['target_mean_661']:.2f}$ & ${G['meta']['target_mean_104']:.2f}$ \\\\")
    row("Always-open fetch, five lines plus the fetch", R["AF"]["5"]); mrow("Always-open fetch", af)
    row("Similarity view, seven lines (recorded rows)", R["TAGGED"]["7"]); mrow("Similarity view", tg)
    row("Recency-aware view, seven lines", R["RECENCY"]["7"]); mrow("Recency-aware view", rc)
    cap = ("What the gate buys, reach only (registered; ADDENDUM\\_R122\\_GATE\\_REACH): three policies assembled from the recorded ranking and the store's records with no monitor call and no answer call, against the recorded model rule. The always-open fetch keys the lifecycle fetch on the name the lookup matches best and never abstains; the similarity view is the recorded top-$k$ retrieval; the recency-aware view keeps the newest record of each attribute and fills to $k$. Each is read at its named depth and budget-matched to the model rule's mean view over the $661$ questions ($5.43$ lines) by interpolating between the two bracketing depths (the always-open fetch between $k=3$ and $4$ with weight $0.91$ on the deeper, the similarity and recency-aware views between $k=5$ and $6$ with weight $0.43$). "
           "Upper panel: the forbidding record in view over the $104$ obligations with the Wilson interval and the per-state census, and the difference from the model rule with both intervals. Lower panel: the licensed record in view over the $174$ licensed items with its difference from the model rule, and the mean lines per question over the $661$ and over the $104$. "
           "The fetch keyed on the best-matched name at four similarity lines reaches $85$ of $104$ at $5.53$ lines; the matched always-open row loses licensed records reliably because the truncated fill drops them; the recency-aware view reaches no retraction obligation because the retracted record is never the newest of its attribute. All three predictions came out as written: the ungated fetch within $0.05$ of the model rule at the matched budget, its unmatched form spending more lines, and the recency-aware view below the rule by more than $0.05$.")
    B["gate_reach"] = ("%% R123: tab:gatereach, written by reviews/v21/tools/ledger_r123_tables.py from reviews/r122/results/gate_reach.json (reviews/r122/NUMBERS_R122.md, AUX-R122-GATE-*); do not edit by hand.\n"
                       + table("tab:gatereach", cap, [("@{}p{0.2\\linewidth}llllll@{}", "Policy & in view (of $104$) & Wilson & sup.\\ / retr.\\ / exp.\\ & minus the model rule & item interval & persona interval \\\\", rows_a),
                                                       ("@{}p{0.2\\linewidth}llllrr@{}", "Policy & licensed (of $174$) & minus the model rule & item interval & persona interval & lines, $661$ & lines, $104$ \\\\", rows_b)]))
    assert all(P[k]["verdict"] == "HOLDS" for k in ("P-G1", "P-G2", "P-G3"))
    assert R["AF"]["4"]["reach"]["reached"] == 85 and f"{R['AF']['4']['lines']['mean_661']:.2f}" == "5.53"
    assert R["RECENCY"]["7"]["reach"]["per_state"]["ret"]["reached"] == 0
    return {"af_matched": af["reach"]["rate"], "model": G["meta"]["model_reach"] / 104, "ratio": P["P-G2"]["ratio"], "af5_lines": R["AF"]["5"]["lines"]["mean_661"],
            "rec_matched": rc["reach"]["rate"], "af_lic_loss": af["licensed_in_view"]["minus_model"]["D"], "af_lic_reliable": bool(af["licensed_in_view"]["minus_model"]["item"]["excludes_zero"] and af["licensed_in_view"]["minus_model"]["persona"]["excludes_zero"]),
            "tg_matched": tg["reach"]["rate"], "af_lic_rate": af["licensed_in_view"]["rate"], "tg_lic_rate": tg["licensed_in_view"]["rate"], "rec_lic_rate": rc["licensed_in_view"]["rate"],
            "matched_mean": af["achieved_mean"]}


# ------------------------------------------------------------------------------------------------------------- the supersession-only margins
def tab_sup_margins(B, k5):
    S = J("reviews/r117/results/sup_margins.json")
    rows = []

    def row(name, whole, sup, v):
        rows.append(f"{name} & {f4(whole)} & {f4(sup)} & {s4(v['delta'])} & {ci(v['item_ci'])} & {ci(v['persona_ci'])} & {'yes' if (v['item_ci']['excludes_zero'] and v['persona_ci']['excludes_zero']) else 'no'} \\\\")
    m = S["GPT-4.1 mini"]
    row("GPT-4.1 mini, one draw (recorded)", m["whole"], m["supersession"]["auroc"], m["supersession"]["vs_lookup"])
    T = J("reviews/r122/results/scores_r122_oai.json")["T3"]["INDEXED-V2"]["new"]
    sup = T["per_state"]["SUPERSESSION"]
    row("GPT-4.1 mini, five draws (provider default)", T["whole"], sup["auroc"], sup["vs_lookup"])
    for name in ("Haiku 4.5", "Opus 5", "GPT-5.6 Sol", "GPT-5.6 Luna"):
        s = S[name]
        row(name + " (five draws)", s["whole"], s["supersession"]["auroc"], s["supersession"]["vs_lookup"])
    cap = ("Each model's supersession-only margin over the name lookup on the counterfactual set under the default summary ($88$ pairs, $264$ items; the lookup reads $0.9223$ there): the model's whole-set and supersession AUROC, the paired difference from the lookup with the item-level and the persona-grouped interval, and whether both intervals exclude zero. Descriptive; computed on the recorded rows after the fact. At one draw GPT-4.1 mini is reliably below the lookup; at five draws its interval includes zero; no model is reliably above it.")
    B["sup_margins"] = ("%% R123: tab:sup-margins, written by reviews/v21/tools/ledger_r123_tables.py from reviews/r117/results/sup_margins.json (the recorded rows through cf2_reader_score, 1,000 draws, seed 42) and, for the five-draw row, reviews/r122/results/scores_r122_oai.json (reviews/NUMBERS_R123.md AUX-R123-SUP-MARGINS); do not edit by hand.\n"
                        + table("tab:sup-margins", cap, [("@{}lrrrlll@{}", "Model & whole set & supersession & minus the lookup & item interval & persona interval & both exclude zero \\\\", rows)], size="\\tiny", sep="1pt"))
    assert m["reliable_sup_margin"] is True and m["supersession"]["vs_lookup"]["delta"] < 0
    assert not (sup["vs_lookup"]["item_ci"]["excludes_zero"] and sup["vs_lookup"]["persona_ci"]["excludes_zero"])
    assert all(not S[n]["reliable_sup_margin"] for n in ("Haiku 4.5", "Opus 5", "GPT-5.6 Sol", "GPT-5.6 Luna"))
    return {n: S[n]["supersession"]["vs_lookup"]["delta"] for n in S}


# ------------------------------------------------------------------------------------------------------------------ the Section 9 reach table
def tab_reach(B, gr):
    RR = J("reviews/v21/results/reach_rows_r123.json")["policies"]
    G = J("reviews/r122/results/gate_reach.json"); M = G["matched"]
    rows = []

    def rec(name, key):
        r = RR[key]
        rows.append(f"{name} & ${r['reach']}$ & ${r['rate']:.2f}$ & ${r['mean_lines_661']:.2f}$ & ${r['licensed_rate']:.2f}$ \\\\")

    def mat(name, key):
        m = M[key]
        rows.append(f"{name} & -- & ${m['reach']['rate']:.2f}$ & ${m['achieved_mean']:.2f}$ & ${m['licensed_in_view']['rate']:.2f}$ \\\\")
    rec("Top-five retrieval", "ALWAYS")
    mat("Similarity retrieval at the matched budget", "TAGGED")
    mat("Recency-aware retrieval at the matched budget", "RECENCY")
    mat("Always-open fetch at the matched budget", "AF")
    rec("Lookup rule", "LOOKUP")
    rec("Model rule", "MODEL")
    rec("Oracle", "ORACLE")
    cap = ("Reach on the full obligation set: records in view, no answer scored. Lines are the mean per question over all $661$ questions (about seven over the $104$ obligations alone); the three matched rows interpolate between two depths to the model rule's budget (Table~\\ref{tab:gatereach}, Appendix~\\ref{app:resp}).")   # R124 A1, the author's caption
    body = table("tab:reach", cap, [("@{}lrrrr@{}", "Policy & \\hd{Forbidding records}{in view (of $104$)} & rate & \\hd{Mean lines}{per question} & \\hd{Licensed record}{in view (of $174$)} \\\\", rows)],
                 size="\\scriptsize", sep="4pt", spec="[h]")
    body = body.replace("\\centering\\scriptsize\\setlength{\\tabcolsep}{4pt}", "\\centering\\scriptsize\\setlength{\\tabcolsep}{4pt}\\renewcommand{\\arraystretch}{0.9}")
    B["reach"] = ("%% R123: tab:reach (the Section 9 reach table), written by reviews/v21/tools/ledger_r123_tables.py from reviews/v21/results/reach_rows_r123.json (the recorded policies; reviews/NUMBERS_R123.md AUX-R123-REACH-ROWS) and reviews/r122/results/gate_reach.json (the matched rows; AUX-R122-GATE-*); do not edit by hand.\n" + body)
    return RR


def main():
    B = {}
    ix = tab_cf_intent(B)
    p1 = tab_cf_p1(B)
    k5 = tab_mini_k5(B)
    enc = tab_enc_lookup(B)
    gr = tab_gate_reach(B)
    sm = tab_sup_margins(B, k5)
    rr = tab_reach(B, gr)
    text = "\n\n".join(f"%%BLOCK {k}%%\n{v}\n%%END {k}%%" for k, v in B.items()) + "\n"
    assert "\u2014" not in text
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print(f"-> {OUT} ({len(B)} blocks: {', '.join(B)})")
    print("amendment 2 (the supersession-only margin over the name lookup from the five-draw rows):")
    print(f"  GPT-4.1 mini five draws: supersession {k5['sup_k5']:.4f} against the lookup 0.9223, margin {k5['sup_margin_k5']:+.4f}, "
          f"item [{k5['sup_item'][0]:+.4f}, {k5['sup_item'][1]:+.4f}], persona [{k5['sup_persona'][0]:+.4f}, {k5['sup_persona'][1]:+.4f}], reliable {k5['sup_reliable']}")
    print("  one-draw margins (reviews/r117/results/sup_margins.json):", {n: f"{v:+.4f}" for n, v in sm.items()})
    print("gate reach:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in gr.items()})
    print("cf-p1:", {k: round(v, 4) for k, v in p1.items()})
    print("encoders:", enc)


if __name__ == "__main__":
    main()
