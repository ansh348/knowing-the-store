"""cfpad_tex.py -- the long-list check's paper fragments (R137, 2026-09-22: 'LAND THE LONG-LIST CHECK', section 1): every CF_PAD number the
appendix prints enters the paper through this file, none by hand.

  results/cfpad_tab_<name>.tex  the Appendix C.2 tables, four decimals, one file per table, spliced by reviews/v23/tools/build_v23.py at the
                               %%CFPAD-TABLE:<name>%% markers reviews/v23/tools/port_r137.py writes into appendix_v23.tex:
                                 tab:cfpad-sup           supersession (registered): every reader's pooled and matched score, padded beside unpadded, W/T/L, both differences with both intervals
                                 tab:cfpad-minus-lookup  supersession (registered): each model minus the embedding lookup, padded beside unpadded, pooled and matched; reliable cells bold
                                 tab:cfpad-whole         whole set (descriptive): the same two views, two panels
                                 tab:cfpad-counted       retraction and expiry (descriptive): padded beside unpadded, pooled and matched, compact
                                 tab:cfpad-other-lookups the other two lookups against the models, supersession (descriptive), point estimates with stars
                                 tab:cfpad-position      the target's rank in the PN list against each reader (descriptive): the two Spearman columns
  results/cfpad_printed.json    the counts, run notes and descriptive values the appendix prose prints, each beside its source key (the two-decimal forms the
                               main text prints are results/cf_pad_printed.json, written by report_cf_pad.py); port_r137.py fills its texts from both files and
                               reviews/v23/tools/r137_number_gate.py re-derives every printed form from results/cf_pad_scores.json independently.

Sources: results/cf_pad_scores.json (scored once), build/lock.json (the build census). No model call. Usage: python cf_pad/tools/cfpad_tex.py
"""
from __future__ import annotations

import io
import json
from pathlib import Path

PAD = Path(__file__).resolve().parents[1]
RES = PAD / "results"
TABLE_NAMES = ("sup", "minus-lookup", "whole", "counted", "other-lookups", "position")
OUT_JSON = RES / "cfpad_printed.json"

READERS = [("LOOKUP", "Name lookup"), ("LEX", "Lexical lookup"), ("RANDTOK", "Random-token lookup"),
           ("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5"), ("LUNA", "GPT-5.6 Luna"), ("SOL", "GPT-5.6 Sol"), ("OP5", "Opus 5$^{a}$")]
MODELS = [r for r in READERS if r[0] in ("MINI", "H45", "LUNA", "SOL", "OP5")]
NOTE_A = "$^{a}$Opus 5: one draw; recorded row five draws."


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def f4(x):
    return f"{x:.4f}"


def s4(x):
    return f"{x:+.4f}"


def ci(c, signed=True):
    return f"[{c['ci_lo']:+.4f},{c['ci_hi']:+.4f}]" if signed else f"[{c['ci_lo']:.4f},{c['ci_hi']:.4f}]"


def star(d):
    return "$^{*}$" if d["both_exclude_zero"] else ""


def bold(s, d):
    """A signed four-decimal value in math mode, bold when the difference is reliable (\\mathbf: \\textbf does not reach math digits)."""
    return f"$\\mathbf{{{s}}}$" if d["both_exclude_zero"] else f"${s}$"


def table(caption, label, colspec, header, rows, notes=None, size="\\tiny", sep="1.5pt"):
    L = ["\\begin{table}[H]", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\centering", size, f"\\setlength{{\\tabcolsep}}{{{sep}}}",
         f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", header + " \\\\", "\\midrule"]
    L += rows
    L += ["\\bottomrule", "\\end{tabular}"]
    if notes:
        L += ["\\par\\smallskip", "\\begin{minipage}{0.97\\linewidth}\\scriptsize", notes, "\\end{minipage}"]
    L += ["\\end{table}", ""]
    return L


def reader_rows(S, sl, met):
    """One panel of the readers' table: pooled (unpadded, padded, the difference, item and persona intervals) or matched (with W/T/L, triple and persona intervals)."""
    rows = []
    for code, name in READERS:
        R = S["readers"][code][sl]
        if met == "pooled":
            p = R["pooled"]; d = p["padded_minus_unpadded"]
            rows.append(f"{name} & ${f4(p['unpadded'])}$ & ${f4(p['padded'])}$ & ${s4(d['delta'])}${star(d)} & ${ci(d['ci_item'])}$ & ${ci(d['ci_persona'])}$ \\\\")
        else:
            m = R["matched"]; d = m["padded_minus_unpadded"]; up, pa = m["unpadded"], m["padded"]
            rows.append(f"{name} & ${f4(up['matched'])}$ ({up['W']}/{up['T']}/{up['L']}) & ${f4(pa['matched'])}$ ({pa['W']}/{pa['T']}/{pa['L']}) & ${s4(d['delta'])}${star(d)} & ${ci(d['ci_triple'])}$ & ${ci(d['ci_persona'])}$ \\\\")
        if code == "RANDTOK":
            rows.append("\\midrule")
    return rows


def minus_rows(S, sl, which, lk="LOOKUP"):
    """One panel of the minus-lookup table: padded or unpadded lists; pooled (item, persona) and matched (triple, persona) differences, the reliable ones bold."""
    rows = []
    for code, name in MODELS:
        M = S["minus_lookup"][code][lk][sl][which]
        pp, pm = M["pooled"], M["matched"]
        rows.append(f"{name} & {bold(s4(pp['delta']), pp)}{star(pp)} & ${ci(pp['ci_item'])}$ & ${ci(pp['ci_persona'])}$ & "
                    f"{bold(s4(pm['delta']), pm)}{star(pm)} & ${ci(pm['ci_triple'])}$ & ${ci(pm['ci_persona'])}$ \\\\")
    return rows


def panels(spec):
    """Stacked panels inside one table: spec = [(title, colspec, header, rows), ...]."""
    L = []
    for k, (title, colspec, header, rows) in enumerate(spec):
        if k:
            L.append("\\par\\vspace{3pt}")
        n = colspec.count("l") + colspec.count("r")
        L += [f"\\begin{{tabular}}{{{colspec}}}", "\\toprule", f"\\multicolumn{{{n}}}{{@{{}}l}}{{\\textit{{{title}}}}}\\\\", header + " \\\\", "\\midrule"] + rows + ["\\bottomrule", "\\end{tabular}"]
    return L


def ptable(caption, label, spec, notes=None, size="\\tiny", sep="1.5pt"):
    L = ["\\begin{table}[H]", f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\centering", size, f"\\setlength{{\\tabcolsep}}{{{sep}}}"]
    L += panels(spec)
    if notes:
        L += ["\\par\\smallskip", "\\begin{minipage}{0.97\\linewidth}\\scriptsize", notes, "\\end{minipage}"]
    L += ["\\end{table}", ""]
    return L


POOLED_HEAD = "Reader & unpadded & padded & difference & item interval & persona interval"
MATCHED_HEAD = "Reader & unpadded (W/T/L) & padded (W/T/L) & difference & triple interval & persona interval"
MINUS_HEAD = "Model & pooled & item interval & persona interval & matched & triple interval & persona interval"
RSPEC, MSPEC = "@{}lrrrll@{}", "@{}lrllrll@{}"


def reader_spec(S, sl):
    return [("Pooled AUROC", RSPEC, POOLED_HEAD, reader_rows(S, sl, "pooled")), ("Matched score, \\pn{} against \\present{}", RSPEC, MATCHED_HEAD, reader_rows(S, sl, "matched"))]


def minus_spec(S, sl):
    return [("Padded lists", MSPEC, MINUS_HEAD, minus_rows(S, sl, "padded")), ("Unpadded lists (the recorded rows)", MSPEC, MINUS_HEAD, minus_rows(S, sl, "unpadded"))]


def main():
    S = jload(RES / "cf_pad_scores.json")
    K = jload(PAD / "build" / "lock.json")
    assert S["arm"] == "INDEXED-V2-PAD60" and S["registration_sha256"] == K["registration_sha256"]
    n_sup = S["readers"]["LOOKUP"]["superseded"]["pooled"]["padded_minus_unpadded"]["n"]
    n_sup_t = S["readers"]["LOOKUP"]["superseded"]["matched"]["padded"]["n"]
    n_all = S["readers"]["LOOKUP"]["whole"]["pooled"]["padded_minus_unpadded"]["n"]
    n_all_t = S["readers"]["LOOKUP"]["whole"]["matched"]["padded"]["n"]
    n_ret = S["readers"]["LOOKUP"]["retracted"]["pooled"]["padded_minus_unpadded"]["n"]
    n_ret_t = S["readers"]["LOOKUP"]["retracted"]["matched"]["padded"]["n"]
    assert (n_sup, n_sup_t, n_all, n_all_t, n_ret, n_ret_t) == (264, 88, 444, 148, 90, 30)
    T = []
    # ---------------------------------------------------------------- supersession, every reader (two panels: pooled; matched)
    T += ptable(f"The long-list check, supersession (registered): the ${n_sup}$ items of the ${n_sup_t}$ supersession triples with the superseded-names list padded to $60$ names, every reader's pooled AUROC (upper panel) and matched score (lower panel, with W/T/L) "
                "beside its recorded unpadded value on the same items, and the paired difference padded minus unpadded with the item-level and the persona-grouped interval (pooled) or the triple-level and the persona-grouped interval (matched). "
                "The three lookups read the padded lists as printed; the models ran the padded summaries at the settings of their Table~\\ref{tab:cf-main} rows. $^{*}$: both intervals exclude zero.",
                "tab:cfpad-sup", reader_spec(S, "superseded"), NOTE_A)
    # ---------------------------------------------------------------- supersession, each model minus the embedding lookup (two panels: padded; unpadded)
    T += ptable("The long-list check, supersession (registered): each model minus the name lookup on the same lists, pooled (item-level and persona-grouped intervals) and matched (triple-level and persona-grouped), "
                "on the padded lists (upper panel) and on the unpadded lists (lower panel: the recorded model minus the recorded lookup). A difference in bold is reliable (both intervals exclude zero, $^{*}$).",
                "tab:cfpad-minus-lookup", minus_spec(S, "superseded"), NOTE_A)
    # ---------------------------------------------------------------- whole set, four panels
    T += ptable(f"The long-list check on the whole counterfactual set, ${n_all}$ items and ${n_all_t}$ triples (descriptive; the registered comparisons are the supersession slice): every reader's padded and unpadded scores as in Table~\\ref{{tab:cfpad-sup}} (the first two panels), "
                "then each model minus the name lookup as in Table~\\ref{tab:cfpad-minus-lookup} (the last two). $^{*}$: both intervals exclude zero; bold: reliable.",
                "tab:cfpad-whole", reader_spec(S, "whole") + minus_spec(S, "whole"), NOTE_A)
    # ---------------------------------------------------------------- retraction and expiry, compact
    rows = []
    for code, name in READERS:
        cells = []
        for sl in ("retracted", "expired"):
            R = S["readers"][code][sl]
            p, m = R["pooled"], R["matched"]
            dp, dm = p["padded_minus_unpadded"], m["padded_minus_unpadded"]
            cells.append(f"${f4(p['unpadded'])}$/${f4(p['padded'])}$/${s4(dp['delta'])}${star(dp)}")
            cells.append(f"${f4(m['unpadded']['matched'])}$/${f4(m['padded']['matched'])}$/${s4(dm['delta'])}${star(dm)}")
        rows.append(f"{name} & " + " & ".join(cells) + " \\\\")
        if code == "RANDTOK":
            rows.append("\\midrule")
    T += table(f"The long-list check on retraction and expiry, ${n_ret}$ items and ${n_ret_t}$ triples each (descriptive): unpadded/padded/the paired difference, pooled and matched, per state. "
               "The padded list names neither state and a triple's three versions carry identical padded lists, so the lookups tie every triple on both states by construction. $^{*}$: both intervals exclude zero.",
               "tab:cfpad-counted", "@{}lllll@{}", "Reader & retraction, pooled & retraction, matched & expiry, pooled & expiry, matched", rows, NOTE_A, sep="1pt")
    # ---------------------------------------------------------------- the other two lookups against the models (point estimates with stars)
    rows = []
    for code, name in MODELS:
        cells = []
        for lk in ("LEX", "RANDTOK"):
            M = S["minus_lookup"][code][lk]["superseded"]
            for which in ("padded", "unpadded"):
                for met in ("pooled", "matched"):
                    d = M[which][met]
                    cells.append(f"${s4(d['delta'])}${star(d)}")
        rows.append(f"{name} & " + " & ".join(cells) + " \\\\")
    T += table("The long-list check, supersession (descriptive): each model minus the lexical lookup and minus the random-token lookup on the same lists, padded and unpadded, pooled and matched; point estimates, "
               "$^{*}$ where both intervals exclude zero (the intervals are in the artifact's ledger).",
               "tab:cfpad-other-lookups", "@{}lrrrrrrrr@{}",
               "& \\multicolumn{4}{c}{minus the lexical lookup} & \\multicolumn{4}{c@{}}{minus the random-token lookup} \\\\\n"
               "Model & padded, pooled & matched & unpadded, pooled & matched & padded, pooled & matched & unpadded, pooled & matched", rows, NOTE_A)
    # ---------------------------------------------------------------- the target's position
    TP = S["descriptive"]["target_position"]
    rows = []
    for code, name in READERS:
        b = TP["by_reader"][code]
        rows.append(f"{name} & ${s4(b['spearman_rank_vs_pn_score'])}$ & ${s4(b['spearman_rank_vs_outcome'])}$ \\\\")
        if code == "RANDTOK":
            rows.append("\\midrule")
    T += table(f"The target's alphabetical rank in the \\pn{{}} version's $60$-name list over the ${TP['n_triples']}$ supersession triples against each reader (descriptive): Spearman correlation of the rank with the reader's \\pn{{}} score and with its \\pn{{}}-against-\\present{{}} outcome.",
               "tab:cfpad-position", "@{}lrr@{}", "Reader & rank against \\pn{} score & rank against outcome", rows, NOTE_A, size="\\scriptsize", sep="4pt")
    # one file per table
    blocks, cur = [], []
    for ln in T:
        if ln == "\\begin{table}[H]" and cur:
            blocks.append(cur); cur = []
        cur.append(ln)
    blocks.append(cur)
    assert len(blocks) == len(TABLE_NAMES), (len(blocks), TABLE_NAMES)
    written = []
    for name, block in zip(TABLE_NAMES, blocks):
        assert f"\\label{{tab:cfpad-{name}}}" in block, (name, block[:3])
        text = (f"% CFPAD-TABLE {name} (written by cf_pad/tools/cfpad_tex.py from cf_pad/results/cf_pad_scores.json; spliced at its per-table marker by reviews/v23/tools/build_v23.py; do not edit by hand)\n"
                + "\n".join(block).rstrip("\n") + "\n")
        out = RES / f"cfpad_tab_{name}.tex"
        io.open(out, "w", encoding="utf-8", newline="\n").write(text)
        written.append(out.name)
    # ---------------------------------------------------------------- the prose values (counts, run notes, descriptives), each beside its source
    tp = K["target_position"]; ll = K["list_length"]; pools = K["pools"]
    d1 = S["descriptive"]["opus_recorded_draw1"]
    seeds = S["descriptive"]["seed_spot_check"]
    # a seed's reading is 'reliable' iff both intervals exclude zero; the registered reading under seed 42 for each difference:
    def reg(k):
        m = k.split("_")[0]
        if k.endswith("_minus_LOOKUP"):
            return S["minus_lookup"][m]["LOOKUP"]["superseded"]["padded"]["pooled"]["both_exclude_zero"]
        return S["readers"][m]["superseded"]["pooled"]["padded_minus_unpadded"]["both_exclude_zero"]
    seed_changes = [(k, s) for k, v in seeds.items() for s, r in v.items() if (r["item"] and r["persona"]) != reg(k)]
    seed_interval_moves = [(k, s, w) for k, v in seeds.items() for s, r in v.items() for w in ("item", "persona") if r[w] != reg(k)]
    cen = S["census"]
    P = {
        "n_items": n_all, "n_triples": n_all_t, "n_sup_items": n_sup, "n_sup_triples": n_sup_t, "n_counted_items": n_ret, "n_counted_triples": n_ret_t,
        "list_pn": 60, "list_min": ll["min"], "list_max": ll["max"], "list_histogram": ll["histogram"],
        "pool_min": pools["a_min"], "pool_median": pools["a_median"], "pool_max": pools["a_max"], "pool_b_pairs": pools["from_pool_b_pairs"],
        "rank_min": tp["min"], "rank_median": tp["median"], "rank_max": tp["max"], "rank_first": tp["first"], "rank_last": tp["last"], "rank_n": tp["n"],
        "rank_deciles": [tp["deciles"][str(i)] for i in range(1, 11)],
        "renderer_lock": K["renderer_lock"], "leak_fails": K["leak_scan"]["fails"],
        "draws": {c: cen[c]["k_new"] for c in cen}, "draws_recorded": {c: cen[c]["k_recorded"] for c in cen},
        "rows": {c: cen[c]["rows"] for c in cen}, "not_ok": {c: cen[c]["not_ok"] for c in cen}, "served": {c: list(cen[c]["served"].keys()) for c in cen},
        "usd": {c: round(cen[c]["usd"], 2) for c in cen},
        "spend": {v: {"usd": round(S["spend"][v]["usd"], 2), "cap": S["spend"][v]["cap"]} for v in S["spend"]},
        "predictions": {k: v["text"] for k, v in S["predictions"].items()},
        "opus_d1": {sl: {"pooled_d1": f4(d1[sl]["pooled_unpadded_d1"]), "matched_d1": f4(d1[sl]["matched_unpadded_d1"]),
                         "padded_minus_d1": s4(d1[sl]["padded_minus_d1_pooled"]["delta"]), "ci_item": ci(d1[sl]["padded_minus_d1_pooled"]["ci_item"]),
                         "ci_persona": ci(d1[sl]["padded_minus_d1_pooled"]["ci_persona"]), "reliable": d1[sl]["padded_minus_d1_pooled"]["both_exclude_zero"]} for sl in ("superseded", "whole")},
        "seed_reading_changes": seed_changes, "seed_interval_moves": seed_interval_moves, "seeds": sorted({s for v in seeds.values() for s in v}),
        "counted_reliable": [(c, sl, met) for c, _ in READERS for sl in ("retracted", "expired") for met in ("pooled", "matched")
                             if S["readers"][c][sl][met]["padded_minus_unpadded"]["both_exclude_zero"]],
        "tol": S["tol"], "stops": S["stops"], "frozen_commit": S["lock"]["frozen_commit"], "registration_sha256": S["registration_sha256"],
    }
    io.open(OUT_JSON, "w", encoding="utf-8", newline="\n").write(json.dumps(P, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {', '.join(written)} ({len(T)} lines) and {OUT_JSON.relative_to(PAD.parent).as_posix()}")
    print(f"  seed reading changes: {seed_changes}; interval moves: {seed_interval_moves}; counted-state reliable: {P['counted_reliable']}")


if __name__ == "__main__":
    main()
