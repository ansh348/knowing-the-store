# -*- coding: utf-8 -*-
"""port_r141.py -- R141 Phase 3 (the landing of ADDENDUM_R141_SB60's fired branch, B-ii with Sol named) on top of the R140 close (port_r140.py --units=close
underneath). Every edit is an asserted replacement; the numbers are read from reviews/r141/results/scores_sb60.json and r141_printed.json (ledger
reviews/NUMBERS_R141.md AUX-R141-RESULTS) and checked by reviews/r141/tools/r141_number_gate.py.

Units (in order): l0 (the line-623 source comment carrying the author's given name removed), l1 (the B-ii sentences, verbatim with Sol named), l2 (C.2: the
SB-60 paragraph and table after tab:length), l3 (Table 2 row 9's cell, only if it fits), l4 (Appendix A's population row; Appendix F's registration row, caption
and the prediction count; Section 4's count), l5 (Table 1's count-reader row names), pa, pb, pc (B-i's landing payers, which B-ii applies; only as needed).
Usage: python reviews/r141/tools/port_r141.py --units=l0,l1,...   (--units=close reads reviews/r141/results/r141_close_units.txt)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v23" / "src"
RES = ROOT / "reviews" / "r141" / "results"
BODY, ABS, APPX, ROBUST = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex", SRC / "robust_table.tex"
ORDER = ["l0", "l1", "l2", "l3", "l4", "l5", "pa", "pb", "pc"]
S = json.load(open(RES / "scores_sb60.json", encoding="utf-8"))
PR = json.load(open(RES / "r141_printed.json", encoding="utf-8"))
AC2 = "(Appendix~\\ref{app:counterfactual})"
TEXT, LOG = {}, []
assert S["branch"] == "B-ii" and PR["predictions"] == {"P-S1": False, "P-S2": True, "P-S3": True, "P-S4": True}
X, D = PR["lookup_sb60_matched"], PR["sol_lead_matched"]      # 0.82, 0.09


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def rep(which, old, new, unit, note=""):
    t = TEXT[which]
    assert t.count(old) == 1, f"[{unit}] {which}: expected 1, found {t.count(old)}: {old[:100]!r}"
    TEXT[which] = t.replace(old, new)
    LOG.append(dict(unit=unit, file=which, old=old, new=new, note=note))


def unit_l0():
    t = TEXT["body"]
    lines = t.split("\n")
    hit = [i for i, l in enumerate(lines) if l.startswith("% [AUTHOR-1] 2026-09-09:")]
    assert len(hit) == 1
    old = lines[hit[0]]
    del lines[hit[0]]
    TEXT["body"] = "\n".join(lines)
    LOG.append(dict(unit="l0", file="body", old=old, new="", note="L0: the source comment carrying the author's given name removed (it never reached the PDF)"))


OLD_ABS = ("On lists longer than the stores we tested write, padded to $60$ names, the lookup loses $0.18$; \\mbox{GPT-5.6} Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, "
           "while the other three fall with it. A list-length cue is uncontrolled there.")
LIM_ANCHOR = "and the two readers that keep their lead there are from one model family. "
LIM_FULL = ("The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it, and the padded lists' counts stay as written, so the superseded total "
            "disagrees with the list length in both versions alike. Luna's lead is not separated from the cue. ")
# The author's ruling of 23 Sep on the B-ii stop: Luna's clause names the pooled reading beside the matched one (the registration promised it and the paper
# names the pooled metric where the two disagree); a wording deviation from the frozen B-ii clause, recorded in the ledger and in C.2.
LP = PR["luna_lead_pooled"] if "luna_lead_pooled" in PR else None
SENT_52 = (f". A sibling padded to the same length and counts, run on Luna, Sol and mini, removes that cue: the length-only reader ties every pair, the lookup scores ${X}$, "
           f"and Sol leads it by a reliable ${D}$. Luna's lead holds on the pooled metric only (${LP}$, reliable) and not within triples ($+{PR['luna_lead_matched']}$; Appendix~\\ref{{app:counterfactual}}).")


def unit_l1():
    u = "l1"
    rep("abstract", OLD_ABS, "On lists longer than the stores we tested write, padded to $60$ names, the lookup loses $0.18$; \\mbox{GPT-5.6} Luna and Sol lose $0.06$ to $0.07$ and lead it by $0.13$ to $0.14$, "
                             "while the other three fall with it. The lead holds for Sol against a sibling padded to the same length and counts.", u, "B-ii abstract, Sol named")
    rep("body", f"; the padded set has no such control {AC2}.", SENT_52, u, "B-ii 5.2: B-i's sentence with Sol named, and Luna's clause")
    rep("body", LIM_ANCHOR, LIM_ANCHOR + LIM_FULL, u, "B-ii Limitations: an addition (the length-cue sentence it was to replace never landed; AUX-R141-ERRATUM-R139), with Luna's clause kept")
    rep("body", "On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$ and the other three fall with it. ",
        f"On a $60$-name list Luna and Sol lead the lookup by $0.13$ to $0.14$ and, with list length and counts fixed, Sol by ${D}$; the other three fall with it. ", u, "B-ii Conclusion, Sol named")


def sb60_table():
    R, ML = S["readers"], S["minus_lookup"]
    ci = lambda d: f"$[{d['ci_lo']:.4f},{d['ci_hi']:.4f}]$"
    sci = lambda d: f"$[{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]$"
    NM = json.load(open(RES / "nomodel_sb60.json", encoding="utf-8"))["readers"]
    rows = []
    for name, key in (("Name lookup (embedding)", None), ("Lexical lookup", "Lexical lookup"), ("Random-token lookup", "Random-token lookup"), ("Length-only reader", "Length-only reader"),
                      ("Count reader, guessed category (share)", "Count reader, guessed category")):
        r = R["Name lookup"] if key is None else NM[key]
        m = r["pn60_vs_sb60"]
        pooled = r["pooled_pn60_vs_sb60"]["auroc"] if key is None else r["pooled_pn60_vs_sb60"]
        rows.append(f"{name} & ${m['W']}/{m['T']}/{m['L']}$ & ${m['matched']:.4f}$ & {ci(m['ci_triple'])} & {ci(m['ci_persona'])} & ${pooled:.4f}$ & ${r['sb60_vs_present']['matched']:.4f}$ \\\\")
    for name in ("GPT-5.6 Luna", "GPT-5.6 Sol", "GPT-4.1 mini"):
        r = R[name]; m = r["pn60_vs_sb60"]
        rows.append(f"{name} (five draws) & ${m['W']}/{m['T']}/{m['L']}$ & ${m['matched']:.4f}$ & {ci(m['ci_triple'])} & {ci(m['ci_persona'])} & ${r['pooled_pn60_vs_sb60']['auroc']:.4f}$ & ${r['sb60_vs_present']['matched']:.4f}$ \\\\")
    diff = []
    for name in ("GPT-5.6 Luna", "GPT-5.6 Sol", "GPT-4.1 mini"):
        for met in ("matched", "pooled"):
            x = ML[name][met]; a = x["ci_triple"] if met == "matched" else x["ci_item"]
            mark = "$^{*}$" if x["reliable"] else ""
            diff.append(f"{name} & {met} & ${x['delta']:+.4f}${mark} & {sci(a)} & {sci(x['ci_persona'])} & {'yes' if x['equivalent'] else 'no'} \\\\")
    return ("\\begin{table}[H]\n\\caption{The sibling-name control at $60$ names (registered; ADDENDUM\\_R141\\_SB60): the \\pn{} version with its list padded to $60$ names against a fourth version with one name "
            "swapped for a same-category sibling, identical pad and counts, on the $88$ supersession pairs. Upper panel: each reader's matched score (W + T/2)/88 with the triple-level and "
            "persona-grouped intervals, the pooled AUROC over the $176$ items, and the sibling against the padded \\present{} version (descriptive). The no-model rows were recorded before the "
            "freeze. Lower panel: each model minus the name lookup, paired; $^{*}$: both $95\\%$ intervals exclude zero; equivalent: both $90\\%$ intervals inside $[-0.05,+0.05]$. "
            "Haiku 4.5 and Opus 5 were not run on this control.}\n\\label{tab:sb60}\n\\centering\\tiny\\setlength{\\tabcolsep}{2pt}\n"
            "\\begin{tabular}{@{}lrrllrr@{}}\n\\toprule\nReader & W/T/L & matched & triple interval & persona interval & pooled & sibling vs \\present{} \\\\\n\\midrule\n"
            + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\\\\[4pt]\n\\begin{tabular}{@{}llrllr@{}}\n\\toprule\nModel minus the name lookup & metric & difference & triple / item interval & persona interval & equivalent \\\\\n\\midrule\n"
            + "\n".join(diff) + "\n\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def unit_l2():
    B = json.load(open(ROOT / "reviews" / "r141" / "build" / "build_sb60.json", encoding="utf-8"))
    P = S["predictions"]; ML = S["minus_lookup"]; R = S["readers"]
    n_sub = B["meta"]["n_substituted"]
    fmt = lambda x: f"${x:+.4f}$"
    para = (
        "%% R141 (2026-09-24): the sibling-name control at 60 names (registrations: reviews/r141/registrations/ADDENDUM_R141_SB60.md, frozen alone at f224177 before the first call; the run 2588717; "
        "scored 7a62892; reviews/NUMBERS_R141.md AUX-R141-*), written by reviews/r141/tools/port_r141.py; every number through r141_number_gate.py.\n"
        "\\paragraph{The sibling-name control at $60$ names.}\\label{app:sb60}\n"
        "A fourth version of each of the $88$ supersession pairs takes the padded \\pn{} text and swaps the target's name for a same-category sibling, so the two lists hold the same $60$ names but one, "
        "under an identical pad and an identical count table (Table~\\ref{tab:sb60}). The sibling is the pair's sibling from the short-list control; where that name was already in the pad, "
        f"which happened on ${n_sub}$ pairs, a substitute was drawn from the pair's remaining eligible names under a recorded seed. "
        "The renderer reproduces every text byte for byte, every list holds $60$ distinct names, and the leak screen found $0$ of $30$ answers correct. "
        f"Before the freeze the name lookup was recorded at ${R['Name lookup']['pn60_vs_sb60']['matched']:.4f}$ matched and the length-only reader, the count reader and the random-token lookup at $0.5000$. "
        f"Of the four predictions, Luna reliably above the lookup came out otherwise (matched {fmt(ML['GPT-5.6 Luna']['matched']['delta'])}, the persona interval reaching below zero; pooled "
        f"{fmt(ML['GPT-5.6 Luna']['pooled']['delta'])}, reliable); Sol reliably above it held ({fmt(ML['GPT-5.6 Sol']['matched']['delta'])} matched, {fmt(ML['GPT-5.6 Sol']['pooled']['delta'])} pooled); "
        f"GPT-4.1 mini not reliably above it held ({fmt(ML['GPT-4.1 mini']['matched']['delta'])} matched); and Luna and Sol at or above $0.80$ with the persona interval above $0.50$ held "
        f"(${R['GPT-5.6 Luna']['pn60_vs_sb60']['matched']:.4f}$ and ${R['GPT-5.6 Sol']['pn60_vs_sb60']['matched']:.4f}$). Seeds $43$ to $46$ change no reading. "
        "Luna, Sol and mini ran five draws each through the raw interface; Haiku 4.5 and Opus 5 were not run. "
        "Section~\\ref{sec:lookup} words Luna's result as holding on the pooled metric only, a wording deviation from the registered branch clause (\\emph{Luna's lead is not separated from the cue}): "
        "the registration promised the pooled reading beside the matched one, and the paper names the pooled metric wherever the two disagree.\n\n" + sb60_table() + "\n")
    t = TEXT["appendix"]
    i = t.index("\\label{tab:length}")
    j = t.index("\\end{table}\n", i) + len("\\end{table}\n")
    TEXT["appendix"] = t[:j] + "\n" + para + t[j:]
    LOG.append(dict(unit="l2", file="appendix", old="", new=para, note="L2: the SB-60 paragraph and table after tab:length"))


def unit_l3():
    t = TEXT["robust"]
    old = "lead it by $0.13$ to $0.14$ \\\\"
    assert t.count(old) == 1
    TEXT["robust"] = t.replace(old, f"lead it by $0.13$ to $0.14$; sibling at equal length: Sol leads a reliable ${D}$ \\\\")
    LOG.append(dict(unit="l3", file="robust_table", old=old, new="", note="L3 (applied only if it fits the existing lines)"))


def unit_l4():
    u = "l4"
    rep("appendix", "the full obligation set & $661$ questions",
        "the supersession pairs, a sibling padded to $60$ names & $176$ items: the $88$ supersession pairs' padded \\pn{} version against a fourth version with one name swapped for a same-category sibling "
        "(identical pad and counts) & GPT-4.1 mini (5), GPT-5.6 Luna (5), GPT-5.6 Sol (5); Haiku 4.5 and Opus 5 not run \\\\\n"
        "the full obligation set & $661$ questions", u, "L4: Appendix A's population row")
    rep("appendix", "and the long-list check on the counterfactual set, registered after the paraphrase check had been read; the Outcome column",
        "the long-list check on the counterfactual set, registered after the paraphrase check had been read, and the sibling-name control at $60$ names, registered after the long-list check had been read; the Outcome column",
        u, "L4: tab:registrations-e's caption")
    t = TEXT["appendix"]
    i = t.index("The long-list check on the counterfactual set & \\texttt{06c611f}")
    j = t.index("\\\\\n", i) + 3
    row = ("%% R141 (2026-09-24): ADDENDUM_R141_SB60, registered text sha256 4fc25a8b..., frozen alone at f224177 (2026-09-23 12:23 +0300 = day 44) before the first call; reviews/NUMBERS_R141.md.\n"
           "The sibling-name control at $60$ names & \\texttt{f224177} & day 44 & the $88$ supersession pairs' padded \\pn{} version against a fourth version with one name swapped (identical pad and counts), "
           "the no-model readers recorded before the freeze, GPT-5.6 Luna, GPT-5.6 Sol and GPT-4.1 mini at five draws (Table~\\ref{tab:sb60}); four predictions: Luna reliably above the name lookup (P-S1), "
           "Sol reliably above it (P-S2), mini not reliably above it (P-S3), Luna and Sol at or above $0.80$ matched with the persona interval above $0.50$ (P-S4) & P-S2, P-S3 and P-S4 held; P-S1 failed \\\\\n")
    TEXT["appendix"] = t[:j] + row + t[j:]
    LOG.append(dict(unit=u, file="appendix", old="", new=row, note="L4: Appendix F's registration row (day 44: the freeze commit's own date)"))
    rep("appendix", "Table~\\ref{tab:registrations-e} $9$ with $4$: $102$ predictions, $33$ of which came out otherwise",
        "Table~\\ref{tab:registrations-e} $13$ with $5$: $106$ predictions, $34$ of which came out otherwise", u, "L4: the count (P-S1 to P-S4, one failed)")
    rep("body", "each before the run that tests it: $33$ of $102$ came out otherwise.", "each before the run that tests it: $34$ of $106$ came out otherwise.", u, "L4: Section 4's count")


def unit_l5():
    rep("body", "Count reader, guessed category & superseded", "Count reader, guessed category (share) & superseded", "l5", "L5")
    rep("body", "Count reader, given category & superseded", "Count reader, given category (count) & superseded", "l5", "L5")


def unit_pa():
    rep("body", "The sibling-name control removed that cue on the short list, where readers still picked the \\pn{} version at $0.88$ or higher.",
        "The sibling-name control removed that cue on the short list.", "pa", "payer a")


def unit_pb():
    rep("body", "removes that cue: the length-only reader ties every pair, the lookup scores", "removes that cue: the lookup scores", "pb", "payer b")


def unit_pc():
    rep("body", LIM_FULL, "The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it. Luna's lead is not separated from the cue. ", "pc", "payer c (Luna's clause kept)")


def unit_r8():
    """The author's R139 ruling R8 (22 Sep, not needed then): S6's \\mbox guards removed except the one that fixed the 'GPT-' / '4.1 mini' break in Limitations.
    No word changes."""
    keep = "\\mbox{GPT-4.1} mini drafted the questions"
    n = 0
    for which in ("abstract", "body"):
        t = TEXT[which]
        if which == "body":
            assert t.count(keep) == 1
            t = t.replace(keep, "@@KEEP@@")
        a, b = (0, len(t)) if which == "abstract" else (t.index("\\section{Introduction}"), t.rindex("\\label{main-text-end}"))
        seg = t[a:b]
        n += seg.count("\\mbox{GPT-4.1}") + seg.count("\\mbox{GPT-5.6}")
        seg = seg.replace("\\mbox{GPT-4.1}", "GPT-4.1").replace("\\mbox{GPT-5.6}", "GPT-5.6")
        t = t[:a] + seg + t[b:]
        TEXT[which] = t.replace("@@KEEP@@", keep)
    LOG.append(dict(unit="r8", file="abstract+body", old="", new="", note=f"R139 ruling R8: {n} \\mbox guards removed, the Limitations one kept"))


def unit_r1():
    """The author's R139 payer R1 (23 Sep; ruled, not needed then): Section 1 drops "Models differ further when the rubric states the intent rule." (5.3 has it)."""
    rep("body", "Models differ further when the rubric states the intent rule.\n", "", "r1", "R139 payer R1, applied after a, b, c left the probe at +0")


def unit_r2():
    rep("body", " The default name lookup reads the superseded list, so it ties the versions.", "", "r2", "R139 payer R2 (Figure 2 caption)")


def unit_r3():
    rep("body", "{\\scriptsize The \\textsc{change} intent is never \\pn{}, because both the old and the new value are licensed; n.a.\\ means a combination the question construction never produces.}",
        "{\\scriptsize \\textsc{change} is never \\pn{}, since both values are licensed; n.a.: a combination the question construction never produces.}", "r3", "R139 payer R3 (Definition 1's note)")


def unit_r4():
    rep("body", "and only mini reliably below. Pooled, the lookup scores $0.92$ and the three $0.93$ to $0.94$, none reliably above it.",
        "and only mini reliably below (pooled: $0.92$ against $0.93$ to $0.94$, none reliable; Appendix~\\ref{app:counterfactual}).", "r4", "R139 payer R4 (B1 as a clause)")


def unit_r5():
    rep("body", "For Mem0 and A-MEM we also render the manifest under each backend's constraints; this constrained rendering is ours and differs from a summary built from their own fields.",
        "For Mem0 and A-MEM we also render the manifest under each backend's constraints; that rendering is ours, not theirs.", "r5", "R139 payer R5")


def unit_r6():
    rep("body", " What differs across readers is which of the two they use.", "", "r6", "R139 payer R6")


def unit_r7():
    rep("body", "Cancelling the hike can therefore move a retraction count from zero to one without placing the hike's name in a retracted-name list. Naming that state exposes which attribute the count concerns.",
        "Cancelling the hike therefore moves a retraction count without naming the hike; naming the state exposes which attribute the count concerns.", "r7", "R139 payer R7")


def unit_q1():
    rep("body", " On Graphiti, native tags on the same retrieved edges bring no reliable improvement. (Appendix~\\ref{app:posthoc-graphiti})", " (Appendix~\\ref{app:posthoc-graphiti})",
        "q1", "the ruling of 23 Sep, payer (i): the Graphiti sentence to G.4, the pointer kept")


def unit_q2():
    rep("body", " The cancelled hike shows why: its cancellation is not the newest record of the attribute it cancels.", "", "q2", "payer (ii)")


def unit_q3():
    rep("body", "Missing or wrong names weaken the summaries agents actually receive. At retrieval, the fetch keyed on the names reaches as far ungated as gated, at a budget trade-off.",
        "Missing or wrong names weaken the summaries agents actually receive, and at retrieval the fetch keyed on the names reaches as far ungated as gated, at a budget trade-off.", "q3", "payer (iii)")


def unit_q4():
    rep("body", "Keep non-active records reachable with their lifecycle tags where deletion or access revocation is not required.",
        "Keep non-active records reachable with their lifecycle tags unless deletion or access revocation is required.", "q4", "payer (iv)")


def unit_s5():
    rep("body", "The ground-truth name lists are built through the manifest-to-record alignment. The $22$ obligations it does not mark are therefore invisible to every summary (mini scores $0.52$ on them under ground truth).",
        "The $22$ obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth).", "s5", "the ruling of 23 Sep on the last line, payer (v)")
    rep("body", "The $22$ obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth). Control is outside this paper's scope. ",
        "Control is outside this paper's scope. The $22$ obligations the manifest-to-record alignment does not mark are invisible to every summary (mini scores $0.52$ on them under ground truth). ", "s5",
        "q_scan Q-A: the merged sentence carries numerals and would open the paragraph; the paragraph's own plain sentence moved first, no word changed (a departure in order, recorded)")


def unit_s6():
    rep("body", "On the $60$-name list Opus 5 ran one draw against its five-draw short-list row, and the two readers that keep their lead there are from one model family. The padded sibling control ran on Luna, Sol and mini; Haiku and Opus were not run on it.",
        "On the $60$-name list Opus 5 ran one draw against its five-draw row; the padded sibling control ran on Luna, Sol and mini only, the first two from one model family.", "s6",
        "payer (vi); payer c as built read 'ran on Luna, Sol and mini; Haiku and Opus were not run on it', the ruled merge's 'only' replaces that clause")


def unit_s7():
    rep("body", "On the full obligation set, no completed model reliably beats the lookup. Haiku, Luna and Opus score $0.82$ to $0.83$ against the lookup's $0.75$, but their margins fail the persona-grouped interval.",
        "On the full obligation set no completed model reliably beats the lookup: Haiku, Luna and Opus score $0.82$ to $0.83$ against its $0.75$, but their margins fail the persona-grouped interval.", "s7", "payer (vii)")


def unit_s8():
    rep("body", "though not under the control that fixes list length. When the questions are reworded only one stronger reader edges past it.",
        "though not under the control that fixes list length, and only one stronger reader edges past it when the questions are reworded.", "s8", "payer (viii)")


def unit_s9():
    rep("body", "mini drafted the questions and is also a reader; it is the weakest reader.", "mini drafted the questions and is also a reader, the weakest.", "s9", "payer (ix)")


ORDER.insert(ORDER.index("pa"), "r8")
ORDER += ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "q1", "q2", "q3", "q4", "s5", "s6", "s7", "s8", "s9"]
UNITS = {k: globals()[f"unit_{k}"] for k in ORDER}


def main():
    arg = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    units = (RES / "r141_close_units.txt").read_text(encoding="utf-8").split() if arg == "close" else [u for u in arg.split(",") if u]
    assert units == [u for u in ORDER if u in units], units
    r = subprocess.run([sys.executable, str(ROOT / "reviews" / "r140" / "tools" / "port_r140.py"), "--units=close"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-500:] + r.stderr[-500:]
    TEXT.update(body=rd(BODY), abstract=rd(ABS), appendix=rd(APPX), robust=rd(ROBUST))
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied")
    # A2's comparison count, recomputed on the final main text through R139's own list and function (the SB-60 sentence adds its comparisons)
    sys.path.insert(0, str(ROOT / "reviews" / "r139" / "tools"))
    import port_r139 as P139
    P139.TEXT.update(body=TEXT["body"], abstract=TEXT["abstract"])
    n = P139.count_n()
    old = "reliable describes each of the $68$ comparisons the main text makes on its own."
    if n != 68:
        rep("body", old, f"reliable describes each of the ${n}$ comparisons the main text makes on its own.", "N", f"A2's count recomputed: {n} (AUX-R139-N list with the SB-60 entry)")
    for k, p in (("body", BODY), ("abstract", ABS), ("appendix", APPX), ("robust", ROBUST)):
        p.write_text(TEXT[k], encoding="utf-8", newline="\n")
    (RES / "port_r141_log.json").write_text(json.dumps(dict(units=units, edits=LOG), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOG)} edits")


if __name__ == "__main__":
    main()
