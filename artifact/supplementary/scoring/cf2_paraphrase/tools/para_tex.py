"""para_tex.py -- the paraphrase check's paper fragments (R134, 2026-09-21: 'LAND THE PARAPHRASE CHECK IN v23', section 2): every PARA number enters the
paper through this file, none by hand.

  results/para_tab_<name>.tex  the Appendix C.2 tables (the registration's 'Appendix D.2' is today's C.2, app:counterfactual), four decimals, one file per
                             table, spliced by reviews/v23/tools/build_v23.py at the %%PARA-TABLE:<name>%% markers port_r134.py writes into appendix_v23.tex
                             (names: pooled, matched, minus-lookup, sup, sens, flags):
                               tab:para-pooled        D.2a  the 115, pooled AUROC: original, paraphrase, difference, both intervals, the branch reading, per-state paraphrase scores
                               tab:para-matched       D.2b  the 115, the matched metric with W/T/L (post hoc)
                               tab:para-minus-lookup  D.2c  model minus the embedding lookup, whole set, paraphrase set beside the original questions (pooled)
                               tab:para-sup           D.2d  supersession only, model minus the embedding lookup, paraphrase and original, pooled and matched (post hoc)
                               tab:para-sens          D.2e  the 124 sensitivity: difference and reading per reader and summary
                               tab:para-flags         the attribute-naming split under both column-two rules
  results/para_printed.json  the two-decimal forms the main text and the abstract print (half-up on the four-decimal recorded value, the convention of
                             reviews/NUMBERS_R131.md) and the counts and three-decimal descriptives the appendix prose prints, each beside its source key;
                             reviews/v23/tools/port_r134.py fills its texts from this file and reviews/v23/tools/r134_number_gate.py re-derives every
                             printed form from the artifacts independently.

Sources: results/para_scores.json (the 115; registered), results/para_scores_all124.json (sensitivity, not registered), results/lookups.json and
lookups_all124.json (through para_scores' 'lookups'), results/para_minus_lookup_posthoc.json (post hoc), sheet.json, para_questions.json.
No model call. Usage: python cf2_paraphrase/tools/para_tex.py
"""
from __future__ import annotations

import io
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import PARA, jload  # noqa: E402

RES = PARA / "results"
TABLE_NAMES = ("pooled", "matched", "minus-lookup", "sup", "sens", "flags")
OUT_JSON = RES / "para_printed.json"

READERS = [  # (key, label, named states); the order of the report's tables; the added readers below a rule
    ("emb_v2", "Name lookup", "superseded"), ("lex_v2", "Lexical lookup", "superseded"),
    ("emb_v3", "Name lookup", "all"), ("lex_v3", "Lexical lookup", "all"),
    ("MINI_v2", "GPT-4.1 mini", "superseded"), ("MINI_v3", "GPT-4.1 mini", "all"),
    ("H45_v2", "Haiku 4.5", "superseded"), ("H45_v3", "Haiku 4.5", "all"),
    ("OP5_v2", "Opus 5 (draw 1)$^{a}$", "superseded"), ("OP5_v3", "Opus 5 (draw 1)$^{a}$", "all"),
]
ADDED = [("LUNA_v2", "GPT-5.6 Luna$^{b}$", "superseded"), ("SOL_v2", "GPT-5.6 Sol$^{b}$", "superseded")]
MODELS = [("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5"), ("OP5", "Opus 5 (draw 1)$^{a}$")]
MODELS_ADDED = [("LUNA", "GPT-5.6 Luna$^{b}$"), ("SOL", "GPT-5.6 Sol$^{b}$")]
STATES = ("superseded", "retracted", "expired")


def r2(x):
    """Two decimals, half-up on the four-decimal recorded value (reviews/NUMBERS_R131.md; r131/r133_number_gate.r2), unsigned magnitude."""
    return str(abs(Decimal(str(round(x, 4))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))


def f4(x):
    return f"{x:.4f}"


def s4(x):
    return f"{x:+.4f}"


def ci(c, signed=True):
    return f"[{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}]" if signed else f"[{c['ci_lo']:.4f},{c['ci_hi']:.4f}]"


def star(d):
    return "$^{*}$" if d["both_exclude_zero"] else ""


def rec(SC, key):
    if key in SC["lookups"]:
        return SC["lookups"][key]
    code, sv = key.split("_")
    return SC["models"][code][sv]


def reading(pd, tol):
    if abs(pd["delta"]) <= tol:
        return "holds"
    if pd["delta"] < -tol and pd["both_exclude_zero"]:
        return "collapses"
    return "neither"


def table(caption, label, colspec, header, rows, notes=None, size="\\scriptsize", sep="2pt"):
    L = ["\\begin{table}[H]", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\centering", size, f"\\setlength{{\\tabcolsep}}{{{sep}}}",
         f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", header + " \\\\", "\\midrule"]
    L += rows
    L += ["\\bottomrule", "\\end{tabular}"]
    if notes:
        L += ["\\par\\smallskip", "\\begin{minipage}{0.97\\linewidth}\\scriptsize", notes, "\\end{minipage}"]
    L += ["\\end{table}", ""]
    return L


NOTE_AB = ("$^{a}$Opus 5 ran the paraphrases once, against its recorded five-draw rows on the original questions, so its paired row carries a draw-count difference as well; "
           "$^{b}$added after the registration, not registered, no prediction: GPT-5.6 Luna and GPT-5.6 Sol at five draws through the raw API under the summary naming superseded records only, "
           "because both summaries together exceeded that lane's budget.")


def main():
    SC = jload(RES / "para_scores.json")
    SCs = jload(RES / "para_scores_all124.json")
    PH = jload(RES / "para_minus_lookup_posthoc.json")
    sh = jload(PARA / "sheet.json")
    Q = jload(PARA / "para_questions.json")
    assert SC["population"] == "accepted" and SCs["population"] == "all124" and PH["population"] == "accepted"
    tol = SC["tol"]
    n, n_pos, n_pairs = SC["n"], SC["n_pos"], SC["n_pairs"]
    acc = [r for r in sh["rows"] if r["same_intent"] == "YES"]
    n_excluded = sh["n_excluded_by_author"]
    by_state = {"superseded": sh["by_state"]["SUPERSESSION"], "retracted": sh["by_state"]["RETRACTION"], "expired": sh["by_state"]["EXPIRY"]}
    n_screen = sum(1 for r in Q["rows"] if r["accepted"])
    n_failed_screen = len(Q["rows"]) - n_screen
    assert n_screen == sh["n_rows"] == 124 and n_pairs == 115 and n_excluded == 9 and len(Q["rows"]) == 148 and n_failed_screen == 24
    assert sum(by_state.values()) == n_pairs == len(acc)

    T = []          # every table, in order; each starts with \begin{table}[H] and the label inside names its file
    # ---------------------------------------------------------------- D.2a pooled
    rows = []
    for block in (READERS, ADDED):
        for key, name, states in block:
            r = rec(SC, key); pd = r["paired"]; ps = r["paraphrase_per_state"]
            rows.append(f"{name} & {states} & ${f4(r['original'])}$ & ${f4(r['paraphrase'])}$ & ${s4(pd['delta'])}${star(pd)} & ${ci(pd['ci_item'])}$ & ${ci(pd['ci_persona'])}$ & {reading(pd, tol)} & "
                        f"${f4(ps['superseded'])}$ / ${f4(ps['retracted'])}$ / ${f4(ps['expired'])}$ \\\\")
        if block is READERS:
            rows.append("\\midrule")
            rows.append("\\multicolumn{9}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
    T += table(f"The paraphrase check on the ${n_pairs}$ accepted pairs (${n}$ items, ${n_pos}$ obligations; registered, descriptive): obligation AUROC on the original questions and on the paraphrases under the same store versions, "
               f"the paired difference paraphrase minus original with the item-level and the persona-clustered interval, the registered reading at the $\\pm{tol}$ tolerance (a reader \\emph{{holds}} inside it and "
               f"\\emph{{collapses}} below $-{tol}$ with both intervals clear of zero), and the paraphrase-set AUROC per state (superseded / retracted / expired). "
               f"$^{{*}}$: both intervals exclude zero. The lexical lookup reads ${f4(SC['lookups']['lex_v2']['paraphrase'])}$ on every paraphrase set by construction: no content token is shared with any printed name.",
               "tab:para-pooled", "@{}llrrrllll@{}", "Reader & States & original & paraphrase & difference & item interval & persona interval & reading & per state, paraphrase", rows, NOTE_AB, size="\\tiny", sep="1.5pt")
    # ---------------------------------------------------------------- D.2b matched
    rows = []
    M = SC["matched"]
    for block in (READERS, ADDED):
        for key, name, states in block:
            w = M[key]["pn_vs_present"]; ow, pw, dw = w["original"]["whole"], w["paraphrase"]["whole"], w["paired"]["whole"]
            rows.append(f"{name} & {states} & ${ow['W']}/{ow['T']}/{ow['L']}$ & ${f4(ow['matched'])}$ & ${pw['W']}/{pw['T']}/{pw['L']}$ & ${f4(pw['matched'])}$ & ${s4(dw['delta'])}${star(dw)} & ${ci(dw['ci_triple'])}$ & ${ci(dw['ci_persona'])}$ \\\\")
        if block is READERS:
            rows.append("\\midrule")
            rows.append("\\multicolumn{9}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
    T += table(f"The same ${n_pairs}$ pairs under the matched metric (post hoc): within each triple the \\pn{{}} version against the \\present{{}} version, W/T/L and $(W+T/2)/{n_pairs}$, on the original questions and on the paraphrases, "
               "with the paired difference (the mean over triples of the per-triple outcome difference) and the triple-level and persona-grouped intervals. $^{*}$: both intervals exclude zero.",
               "tab:para-matched", "@{}llrrrrrll@{}", "Reader & States & original W/T/L & matched & paraphrase W/T/L & matched & difference & triple interval & persona interval", rows, NOTE_AB, size="\\tiny", sep="1.5pt")
    # ---------------------------------------------------------------- D.2c model minus lookup, whole set, paraphrase beside original
    rows = []
    for block in (MODELS, MODELS_ADDED):
        for code, name in block:
            for sv, states in (("v2", "superseded"), ("v3", "all")):
                if sv not in PH["models"][code]:
                    continue
                R = PH["models"][code][sv]["whole"]["pooled"]; p, o = R["paraphrase"], R["original"]
                rows.append(f"{name} & {states} & ${s4(p['delta'])}${star(p)} & ${ci(p['ci_item'])}$ & ${ci(p['ci_persona'])}$ & ${s4(o['delta'])}${star(o)} & ${ci(o['ci_item'])}$ & ${ci(o['ci_persona'])}$ \\\\")
        if block is MODELS:
            rows.append("\\midrule")
            rows.append("\\multicolumn{8}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
    T += table(f"Each model minus the name lookup under the same summary on the whole set of ${n_pairs}$ pairs, pooled AUROC with the item-level and the persona-clustered paired interval: on the paraphrase set (the registered row) "
               "and on the original questions of the same pairs beside it (post hoc), so that a lead can be read against the one it replaces. $^{*}$: both intervals exclude zero.",
               "tab:para-minus-lookup", "@{}llrllrll@{}", "Model & States & paraphrases & item & persona & originals & item & persona", rows, NOTE_AB, size="\\tiny", sep="1.5pt")
    # ---------------------------------------------------------------- D.2d supersession only: two panels (pooled; matched), each six columns, so the table fits the text width
    n_sup_pairs, n_sup_items = PH["n_pairs_superseded"], PH["n_items_superseded"]
    panels = []
    for met, c1, head in (("pooled", "ci_item", "Pooled AUROC & item interval & persona interval"), ("matched", "ci_triple", "Matched metric & triple interval & persona interval")):
        rows = []
        for block in (MODELS, MODELS_ADDED):
            for code, name in block:
                for sv, states in (("v2", "superseded"), ("v3", "all")):
                    if sv not in PH["models"][code]:
                        continue
                    R = PH["models"][code][sv]["superseded"][met]
                    for which, lab in (("paraphrase", "paraphrases"), ("original", "originals")):
                        d = R[which]
                        rows.append(f"{name if which == 'paraphrase' else ''} & {states if which == 'paraphrase' else ''} & {lab} & ${s4(d['delta'])}${star(d)} & ${ci(d[c1])}$ & ${ci(d['ci_persona'])}$ \\\\")
            if block is MODELS:
                rows.append("\\midrule")
                rows.append("\\multicolumn{6}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
        panels.append((f"Model & States & questions & {head}", rows))
    L = ["\\begin{table}[H]",
         f"\\caption{{Supersession only (post hoc): each model minus the name lookup under the same summary on the ${n_sup_pairs}$ supersession pairs (${n_sup_items}$ items), on the paraphrases and on the original questions of the same pairs; "
         "upper panel the pooled AUROC with the item-level and the persona-clustered paired intervals, lower panel the matched metric with the triple-level and the persona-grouped intervals. $^{*}$: both intervals clear of zero.}",
         "\\label{tab:para-sup}", "\\centering", "\\tiny", "\\setlength{\\tabcolsep}{2pt}"]
    for k, (head, rows) in enumerate(panels):
        if k:
            L.append("\\par\\vspace{3pt}")
        L += ["\\begin{tabular}{@{}lllrll@{}}", "\\toprule", head + " \\\\", "\\midrule"] + rows + ["\\bottomrule", "\\end{tabular}"]
    L += ["\\par\\smallskip", "\\begin{minipage}{0.97\\linewidth}\\scriptsize", NOTE_AB, "\\end{minipage}", "\\end{table}", ""]
    T += L
    # ---------------------------------------------------------------- D.2e the 124 sensitivity
    rows = []
    for block in (READERS, ADDED):
        for key, name, states in block:
            r = rec(SCs, key); pd = r["paired"]
            rows.append(f"{name} & {states} & ${f4(r['original'])}$ & ${f4(r['paraphrase'])}$ & ${s4(pd['delta'])}${star(pd)} & ${ci(pd['ci_item'])}$ & ${ci(pd['ci_persona'])}$ & {reading(pd, tol)} \\\\")
        if block is READERS:
            rows.append("\\midrule")
            rows.append("\\multicolumn{8}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
    T += table(f"Sensitivity, not registered: the same scoring on all ${SCs['n_pairs']}$ screen-passing pairs (${SCs['n']}$ items), the ${n_pairs}$ accepted and the ${n_excluded}$ an author's read excluded; "
               "original, paraphrase, the paired difference with both intervals and the reading at the same tolerance. $^{*}$: both intervals exclude zero.",
               "tab:para-sens", "@{}llrrrlll@{}", "Reader & States & original & paraphrase & difference & item interval & persona interval & reading", rows, NOTE_AB, size="\\tiny", sep="1.5pt")
    # ---------------------------------------------------------------- the attribute-naming split under both rules
    F1, F2 = SC["flags"]["author_column2_on_paraphrases"], SC["flags"]["token_rule_on_paraphrases"]
    rows = []
    for block in (READERS, ADDED):
        for key, name, states in block:
            a, b = F1[key], F2[key]
            rows.append(f"{name} & {states} & ${f4(a['paraphrase']['flagged'])}$ & ${f4(a['paraphrase']['unflagged'])}$ & ${f4(a['original']['flagged'])}$ & ${f4(a['original']['unflagged'])}$ & "
                        f"${f4(b['paraphrase']['flagged'])}$ & ${f4(b['paraphrase']['unflagged'])}$ \\\\")
        if block is READERS:
            rows.append("\\midrule")
            rows.append("\\multicolumn{8}{@{}l}{\\textit{Added after the registration, not registered}}\\\\")
    T += table(f"The attribute-naming split of Appendix~\\ref{{app:posthoc-flags}} recomputed on the paraphrase set (a disclosure; it excludes nothing), under two rules for the sheet's second column: "
               f"an author's read to that appendix's sentence, whether the rewrite names the plan or value its attribute is about (${F1['n_flagged_pairs']}$ flagged of the ${n_pairs}$, ${F1['n_unflagged_pairs']}$ not), "
               f"and the token rule of the original read, whether the rewrite carries a content token of the value part of the slot path (${F2['n_flagged_pairs']}$ flagged, ${F2['n_unflagged_pairs']}$ not). "
               "Pooled AUROC on each half; under the first rule the original questions' values on the same halves beside.",
               "tab:para-flags", "@{}llrrrrrr@{}", "Reader & States & rule 1, flagged & unflagged & originals, flagged & unflagged & rule 2, flagged & unflagged", rows, NOTE_AB, size="\\tiny", sep="1.5pt")
    # one file per table: split T at every \begin{table}[H]; the label inside names the file (tab:para-<name> -> para_tab_<name>.tex)
    blocks, cur = [], []
    for ln in T:
        if ln == "\\begin{table}[H]" and cur:
            blocks.append(cur); cur = []
        cur.append(ln)
    blocks.append(cur)
    assert len(blocks) == len(TABLE_NAMES), (len(blocks), TABLE_NAMES)
    written = []
    for name, block in zip(TABLE_NAMES, blocks):
        assert f"\\label{{tab:para-{name}}}" in block, (name, block[:3])
        text = (f"% PARA-TABLE {name} (written by cf2_paraphrase/tools/para_tex.py from cf2_paraphrase/results/*.json; spliced at its per-table marker by reviews/v23/tools/build_v23.py; do not edit by hand)\n"
                + "\n".join(block).rstrip("\n") + "\n")
        out = RES / f"para_tab_{name}.tex"
        io.open(out, "w", encoding="utf-8", newline="\n").write(text)
        written.append(out.name)

    # ---------------------------------------------------------------- the printed forms for the main text, the abstract and the appendix prose
    L = SC["lookups"]; Mo = SC["models"]; sup = {c: PH["models"][c]["v2"]["superseded"] for c in ("MINI", "H45", "OP5", "LUNA", "SOL")}
    ex = SC["extras"]["target_name_similarity"]
    xt = {"A": {30, 40, 77, 82, 28}, "B": {11, 46, 33, 79}, "C": {12, 27, 45, 49, 52, 57, 63, 68, 92, 94, 102, 112}}
    no_nums = {r["num"] for r in sh["rows"] if r["same_intent"] != "YES"}
    unflagged = set(range(1, 125)) - xt["A"] - xt["B"] - xt["C"]

    def two(x, src, reliable=None):
        return {"printed": r2(x), "value": x, "source": src, "reliable": reliable}

    P = {
        "n_pairs": n_pairs, "n_items": n, "n_questions": 148, "n_screen_passing": n_screen, "n_failed_screen": n_failed_screen, "n_excluded_by_read": n_excluded, "floor_registered": 120,
        "by_state": by_state, "n_sup_pairs": n_sup_pairs, "n_sup_items": n_sup_items, "n_sens_pairs": SCs["n_pairs"], "n_sens_items": SCs["n"],
        "flags_rule1": F1["n_flagged_pairs"], "flags_rule2": F2["n_flagged_pairs"], "flags_rule1_of124": sum(1 for r in sh["rows"] if r["names_value"] == "YES"),
        "flags_rule2_of124": sum(1 for r in Q["rows"] if r["accepted"] and r["value_tokens_in_paraphrase"]),
        "ai_flags": {k: {"excluded": len(s & no_nums), "of": len(s)} for k, s in (("A", xt["A"]), ("B", xt["B"]), ("C", xt["C"]), ("unflagged", unflagged))},
        "draws": {"MINI": 1, "H45": 5, "OP5": 1, "OP5_recorded": 5, "LUNA": 5, "SOL": 5},
        # the main text (two decimals; the paper's convention: magnitudes in prose with the direction in words)
        "lookup_loss_v2": two(L["emb_v2"]["paired"]["delta"], "AUX-PARA-LOOKUP-EMB-V2 paired delta", L["emb_v2"]["paired"]["both_exclude_zero"]),
        "mini_loss_v2": two(Mo["MINI"]["v2"]["paired"]["delta"], "AUX-PARA-MINI-V2 paired delta", Mo["MINI"]["v2"]["paired"]["both_exclude_zero"]),
        "haiku_loss_v2": two(Mo["H45"]["v2"]["paired"]["delta"], "AUX-PARA-H45-V2 paired delta", Mo["H45"]["v2"]["paired"]["both_exclude_zero"]),
        "opus_loss_v2": two(Mo["OP5"]["v2"]["paired"]["delta"], "AUX-PARA-OP5-V2 paired delta", Mo["OP5"]["v2"]["paired"]["both_exclude_zero"]),
        "luna_loss_v2": two(Mo["LUNA"]["v2"]["paired"]["delta"], "AUX-PARA-LUNA-V2 paired delta", Mo["LUNA"]["v2"]["paired"]["both_exclude_zero"]),
        "sol_loss_v2": two(Mo["SOL"]["v2"]["paired"]["delta"], "AUX-PARA-SOL-V2 paired delta", Mo["SOL"]["v2"]["paired"]["both_exclude_zero"]),
        "mini_minus_lookup_v2": two(Mo["MINI"]["v2"]["model_minus_emb"]["delta"], "AUX-PARA-MINI-V2 model minus embedding lookup", Mo["MINI"]["v2"]["model_minus_emb"]["both_exclude_zero"]),
        "sup_mini": two(sup["MINI"]["pooled"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-MINI-V2 supersession pooled paraphrase", sup["MINI"]["pooled"]["paraphrase"]["both_exclude_zero"]),
        "sup_haiku": two(sup["H45"]["pooled"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-H45-V2 supersession pooled paraphrase", sup["H45"]["pooled"]["paraphrase"]["both_exclude_zero"]),
        "sup_opus": two(sup["OP5"]["pooled"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-OP5-V2 supersession pooled paraphrase", sup["OP5"]["pooled"]["paraphrase"]["both_exclude_zero"]),
        "sup_sol": two(sup["SOL"]["pooled"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-SOL-V2 supersession pooled paraphrase", sup["SOL"]["pooled"]["paraphrase"]["both_exclude_zero"]),
        "sup_luna": two(sup["LUNA"]["pooled"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2 supersession pooled paraphrase", sup["LUNA"]["pooled"]["paraphrase"]["both_exclude_zero"]),
        "sup_luna_matched": two(sup["LUNA"]["matched"]["paraphrase"]["delta"], "AUX-PARA-POSTHOC-MINUS-LOOKUP-LUNA-V2 supersession matched paraphrase", sup["LUNA"]["matched"]["paraphrase"]["both_exclude_zero"]),
        "sup_luna_item_lo": {"printed": f"{sup['LUNA']['pooled']['paraphrase']['ci_item']['ci_lo']:.3f}", "value": sup["LUNA"]["pooled"]["paraphrase"]["ci_item"]["ci_lo"], "source": "the same row, item interval, lower bound"},
        "sup_luna_persona_lo": {"printed": f"{sup['LUNA']['pooled']['paraphrase']['ci_persona']['ci_lo']:.3f}", "value": sup["LUNA"]["pooled"]["paraphrase"]["ci_persona"]["ci_lo"], "source": "the same row, persona interval, lower bound"},
        "sup_original_none_above": bool(all(not (sup[c]["pooled"]["original"]["delta"] > 0 and sup[c]["pooled"]["original"]["both_exclude_zero"]) for c in sup)),
        "sup_haiku_matched_reliable": sup["H45"]["matched"]["paraphrase"]["both_exclude_zero"],
        "lookup_loss_v3_pooled": two(L["emb_v3"]["paired"]["delta"], "AUX-PARA-LOOKUP-EMB-V3 paired delta", L["emb_v3"]["paired"]["both_exclude_zero"]),
        "lookup_loss_v3_matched": two(M["emb_v3"]["pn_vs_present"]["paired"]["whole"]["delta"], "AUX-PARA-MATCHED-EMB_V3 paired delta", M["emb_v3"]["pn_vs_present"]["paired"]["whole"]["both_exclude_zero"]),
        "lex_para": f4(L["lex_v2"]["paraphrase"]),
        # the appendix prose: the genericity descriptives at three decimals (the report's forms; AUX-PARA-GENERIC)
        "cos_orig": f"{ex['cosine_original_mean']:.3f}", "cos_para": f"{ex['cosine_paraphrase_mean']:.3f}", "ov_orig": f"{ex['token_overlap_original_mean']:.3f}", "ov_para": f"{ex['token_overlap_paraphrase_mean']:.3f}",
        "branches": {sv: SC["branches"][sv] for sv in ("v2", "v3")}, "branches_sens": {sv: SCs["branches"][sv] for sv in ("v2", "v3")},
        "sens_lower_for_every_reader": bool(all(rec(SCs, k)["paraphrase"] <= rec(SC, k)["paraphrase"] for k, _, _ in READERS + ADDED)),
    }
    io.open(OUT_JSON, "w", encoding="utf-8", newline="\n").write(json.dumps(P, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {', '.join(written)} ({len(T)} lines) and {OUT_JSON.relative_to(PARA.parent).as_posix()}")
    for k, v in P.items():
        if isinstance(v, dict) and "printed" in v:
            print(f"  {k:24s} {v['printed']:>6s}  <- {v['value']:+.4f}  reliable={v.get('reliable')}  ({v['source']})")


if __name__ == "__main__":
    main()
