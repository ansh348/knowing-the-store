# -*- coding: utf-8 -*-
"""appendix_r129.py -- program R129 (2026-09-20; the author's rulings on R127b and R128's held items, brief 'KtS R129'): the appendix edits,
applied to reviews/v22/src/appendix_v22.tex after appendix_r126.py and appendix_r128.py (regeneration order: cp v21 -> appendix_r126.py ->
appendix_r128.py -> appendix_r129.py -> fig3_data.py -> port_v22.py). Every edit asserted (rep); every number read from its artifact or ledger.
  B1  C.2: E9's rows (GPT-5.6 Luna and GPT-5.6 Sol at five draws, AUX-V2RCAT-A2-*) join tab:v2rcat; two sentences of prose; the caption's sentence
  B2  C.2: tab:cf-hybrid gains GPT-4.1 mini's five-draw row minus the hybrid (AUX-R129-HYB-MINI5)
  A2  E.10: the inverted tag's paragraph (AUX-R129-B9: 35 -> 34, 14 -> 13, the oracle split both ways); the eight answer-stage captions say the
      tables were scored with the tag as joined
  B1  F: E9's row in tab:registrations-d; the count paragraph (AUX-R129-COUNT: 93 predictions, 29 otherwise; -d 29 with 11)
  D   E.3: tab:e3-groups (AUX-R129-GROUPS) with four sentences
Usage: python reviews/v22/tools/appendix_r129.py [--check]
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
RES = ROOT / "reviews" / "v22" / "results"
V2R = json.load(open(ROOT / "r82_counterfactual" / "v2rcat" / "results" / "scores_v2rcat_openai.json", encoding="utf-8"))
HYB5 = json.load(open(RES / "r129_hybrid_mini5.json", encoding="utf-8"))
B9 = json.load(open(RES / "r129_b9.json", encoding="utf-8"))
G127 = json.load(open(RES / "r127_groups.json", encoding="utf-8"))["readers"]
G127B = json.load(open(RES / "r127b_groups.json", encoding="utf-8"))["readers"]


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:100])
    return t.replace(old, new)


def f4(x):
    return f"${x:.4f}$"


def s4(x):
    return f"${x:+.4f}$"


def ival(d, signed=True):
    return f"$[{d['ci_lo']:+.4f},{d['ci_hi']:+.4f}]$" if signed else f"$[{d['ci_lo']:.4f},{d['ci_hi']:.4f}]$"


def e9_rows():
    rows = []
    for reader, key in (("GPT-5.6 Luna", "gpt-5.6-luna"), ("GPT-5.6 Sol", "gpt-5.6-sol")):
        m = V2R["models"][key]; w = m["minus_v2"]
        rows.append(f"{reader} ($k=5$) & whole set & {f4(m['v2_recorded_k5'])} & {f4(m['v2rcat'])} & {s4(w['delta'])} {ival(w['item_ci'])}; {ival(w['persona_ci'])} \\\\\n")
        for state, k2 in (("retraction", "RETRACTION"), ("expiry", "EXPIRY")):
            p = m["per_state"][k2]
            rows.append(f"{reader} & {state} ($30$ pairs) & {f4(p['v2'])} & {f4(p['v2rcat'])} & {s4(p['delta'])} {ival(p['item_ci'])}; {ival(p['persona_ci'])} \\\\\n")
    return "".join(rows)


def groups_table():
    R = [("GPT-4.1 mini", "GPT-4.1 mini (INDEXED-TRUE, one call)", "GPT-4.1 mini"), ("Haiku 4.5", "Haiku 4.5 (five calls)", "Haiku 4.5"),
         ("GPT-5.6 Luna", "GPT-5.6 Luna (five calls)", "GPT-5.6 Luna"), ("Opus 5", "Opus 5 (five calls)", "Opus 5")]
    up, low = [], []
    for name, k1, k2 in R:
        a = G127[k1]; b = G127B[k2]
        up.append(f"{name} & obligations & $104$ & {f4(b['means']['pn']['blind'])} & {f4(b['means']['pn']['indexed'])} & & & \\\\\n")
        for g in ("a", "b", "c"):
            up.append(f" & ({g}) & ${a[g]['n_group']}$ & {f4(b['means'][g]['blind'])} & {f4(b['means'][g]['indexed'])} & {f4(a[g]['auroc'])} & {ival(a[g]['item_ci'], False)} & {ival(a[g]['persona_ci'], False)} \\\\\n")
            low.append(f"{name if g == 'a' else ''} & ({g}) & {f4(b[g]['blind_auroc'])} & {s4(b[g]['gain'])} & {ival(b[g]['item_ci'])} & {ival(b[g]['persona_ci'])} \\\\\n")
    a = G127["name lookup (superseded section, embedding)"]
    up.append(f"Name lookup & obligations & $104$ & -- & {f4(a['mean_pn'])} & & & \\\\\n")
    for g in ("a", "b", "c"):
        up.append(f" & ({g}) & ${a[g]['n_group']}$ & -- & {f4(a[g]['mean_group'])} & {f4(a[g]['auroc'])} & {ival(a[g]['item_ci'], False)} & {ival(a[g]['persona_ci'], False)} \\\\\n")
    return ("%% R129 D (2026-09-20): tab:e3-groups, written by reviews/v22/tools/appendix_r129.py from reviews/v22/results/r127_groups.json and r127b_groups.json\n"
            "%% (reviews/NUMBERS_R129.md AUX-R129-GROUPS); do not edit by hand.\n"
            "\\begin{table}[H]\n"
            "\\caption{The $104$ obligations against the three \\present{} groups of Table~\\ref{tab:e3-intent}: (a) the $33$ whose own attribute holds a non-active record under current or upcoming intent, (b) the $11$ under change intent, (c) the remaining $130$. "
            "Upper panel: the mean score question only and with the summary, and the AUROC of the obligations against the group with the summary, with the item-level and persona-grouped intervals ($1{,}000$ draws). "
            "Lower panel: the question-only AUROC and the paired gain from adding the summary, with both intervals. GPT-4.1 mini's rows are one call; Haiku 4.5, Opus 5 and GPT-5.6 Luna the five-call collapse; the name lookup reads the superseded section and has no question-only form. Descriptive; read after the results were known.}\n"
            "\\label{tab:e3-groups}\n"
            "\\centering\\tiny\\setlength{\\tabcolsep}{3pt}\n"
            "\\begin{tabular}{@{}llrrrrll@{}}\n\\toprule\n"
            "Reader & group & $n$ & mean, question only & mean, with summary & AUROC, with summary & item interval & persona interval \\\\\n\\midrule\n"
            + "".join(up) +
            "\\bottomrule\n\\end{tabular}\\\\[4pt]\n"
            "\\begin{tabular}{@{}llrrll@{}}\n\\toprule\n"
            "Reader & group & AUROC, question only & gain from the summary & item interval & persona interval \\\\\n\\midrule\n"
            + "".join(low) +
            "\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def main():
    check = "--check" in sys.argv
    t = APPX.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "%% R128 B1" in t, "run appendix_r128.py first"
    if "%% R129" in t:
        print("appendix_r129.py: already applied"); return

    # ---- B1: E9's rows in tab:v2rcat, the caption's sentence, two sentences of prose
    t = rep(t, "Opus 5, draw 1 & expiry ($30$ pairs) & $0.6150$ & $0.4914$ & $-0.1236$ $[-0.2165,-0.0374]$; $[-0.2598,-0.0118]$ \\\\\n",
            "Opus 5, draw 1 & expiry ($30$ pairs) & $0.6150$ & $0.4914$ & $-0.1236$ $[-0.2165,-0.0374]$; $[-0.2598,-0.0118]$ \\\\\n"
            "%% R129 B1 (2026-09-20): E9, the second amendment (AUX-V2RCAT-A2-LUNA-K5, -SOL-K5; r82_counterfactual/v2rcat/results/scores_v2rcat_openai.json), written by appendix_r129.py.\n"
            + e9_rows(), where="tab:v2rcat rows")
    t = rep(t, "which predicted that the one-draw movement on retraction and expiry would replicate at five draws with both intervals excluding zero; it did.}",
            "which predicted that the one-draw movement on retraction and expiry would replicate at five draws with both intervals excluding zero; it did. "
            "GPT-5.6 Luna and GPT-5.6 Sol ran at five draws under the second amendment, whose one prediction, that each falls reliably on both counted states, failed on retraction for both.}", where="tab:v2rcat caption")
    luna, sol = V2R["models"]["gpt-5.6-luna"], V2R["models"]["gpt-5.6-sol"]
    t = rep(t, "which carries draw-count noise against the five-draw row that the two registered runs did not.\n",
            "which carries draw-count noise against the five-draw row that the two registered runs did not.\n"
            "%% R129 B1 (2026-09-20): E9 in two sentences (AUX-V2RCAT-A2-P-M2).\n"
            f"GPT-5.6 Luna and GPT-5.6 Sol, run at five draws on the same texts through the raw API against their recorded five-draw rows under the second amendment, fall reliably on expiry, by {s4(luna['per_state']['EXPIRY']['delta'])} and {s4(sol['per_state']['EXPIRY']['delta'])}, "
            f"and on retraction by {s4(luna['per_state']['RETRACTION']['delta'])} and {s4(sol['per_state']['RETRACTION']['delta'])} with both intervals including zero.\n"
            "The amendment's one prediction, that each falls reliably on both counted states, failed for both models.\n", where="C.2 prose")

    # ---- B2: tab:cf-hybrid's five-draw row
    m5 = HYB5["mini_k5"]; d5 = m5["minus_hybrid"]
    t = rep(t, "GPT-4.1 mini & $0.7167$ & $-0.0698$ & $[-0.1187,-0.0192]$ & $[-0.1094,-0.0316]$ \\\\\n",
            "GPT-4.1 mini & $0.7167$ & $-0.0698$ & $[-0.1187,-0.0192]$ & $[-0.1094,-0.0316]$ \\\\\n"
            "%% R129 B2 (2026-09-20): the five-draw row of Table 1 minus the hybrid (reviews/v22/results/r129_hybrid_mini5.json; AUX-R129-HYB-MINI5).\n"
            f"GPT-4.1 mini, five draws & {f4(m5['model'])} & {s4(d5['delta'])} & {ival(d5['item_ci'])} & {ival(d5['persona_ci'])} \\\\\n", where="tab:cf-hybrid row")
    t = rep(t, "Lower panel: each model's recorded row minus the hybrid.", "Lower panel: each model's recorded row minus the hybrid, and GPT-4.1 mini's five-draw row (Table~\\ref{tab:cf-main}) beside its one-draw row.", where="tab:cf-hybrid caption")

    # ---- A2: E.10's inverted-tag paragraph and the answer-stage captions
    v = B9["views_with_active_stale_line"]; s = B9["oracle_split"]; mi, ha = s["GPT-4.1 mini"], s["Haiku 4.5"]
    assert mi["stale_on_the_corrected_view"] and ha["stale_on_the_corrected_view"]
    t = rep(t, "The tagged and untagged split of Table~\\ref{tab:ds} counts the item's own forbidding records and does not see these duplicates.\n",
            "The tagged and untagged split of Table~\\ref{tab:ds} counts the item's own forbidding records and does not see these duplicates.\n\n"
            "%% R129 A2 (2026-09-20): the inverted tag corrected on paper (reviews/v22/results/r129_b9.json; AUX-R129-B9); nothing re-answered.\n"
            f"The negation case is one of the $26$ retraction obligations, the full-store view of that question, carrying an inverted tag because the ground-truth join reads no negation; its slot-ablated view carries the same tag but holds no line asserting the stale value, so it is outside the $35$ either way. "
            f"Correcting the tag, the retraction statement active and the plan records retracted, moves the $35$ of $89$ to ${v['corrected']['total']}$ and the retraction count from $14$ to ${v['corrected']['ret']}$. "
            f"The oracle's stale answers split by whether the view holds an active line asserting the stale value ${mi['as_joined']['stale_with_active_stale_line']}$ against ${mi['as_joined']['stale_without']}$ for GPT-4.1 mini and ${ha['as_joined']['stale_with_active_stale_line']}$ against ${ha['as_joined']['stale_without']}$ for Haiku 4.5 as joined, "
            f"and ${mi['corrected']['stale_with_active_stale_line']}$ against ${mi['corrected']['stale_without']}$ and ${ha['corrected']['stale_with_active_stale_line']}$ against ${ha['corrected']['stale_without']}$ with the tag corrected, both answerers having answered that question from the plan lines the view showed as active. "
            "Every answer-stage table was scored with the tag as joined and says so in its caption; nothing was re-answered.\n\n", where="E.10 paragraph")
    NOTE = " Scored with the store's tags as joined, one retraction tag inverted (the negation paragraph).}"
    for lab, tail in (("tab:ds", "and the all-states fetch set, so that the counted-state gate can fire.}"),
                      ("tab:ds-h45", "as not to be used (Amendment 3). Descriptive; both registered after the first draft.}"),
                      ("tab:ds-a5", "reads Amendment 4 (recorded) to Amendment 5; mini is GPT-4.1 mini and Haiku is Haiku 4.5.}"),
                      ("tab:ds-a6", "persona-grouped bootstraps ($10{,}000$ draws, the three policies resampled together).}"),
                      ("tab:ds-a7", "are $174$ licensed items, $104$ obligations, $383$ absent items and $661$ in all.}"),
                      ("tab:ds-a8", "the re-answers under own tags are descriptive, no prediction was registered on them.}"),
                      ("tab:ds-body", "untagged duplicates are retagged (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).}"),
                      ("tab:ds-body-lower", "and coverage of the $174$ licensed items (record in view without abstention).}")):
        t = rep(t, tail + "\n\\label{" + lab + "}", tail[:-1] + NOTE + "\n\\label{" + lab + "}", where=lab)

    # ---- B1: E9's row in tab:registrations-d and the count paragraph
    t = rep(t, "Moved-count control, Amendment 1: Opus 5 at five draws & \\texttt{177697a4ae} & day 40 & Opus 5 at five draws on the moved-count texts against its recorded five-draw row; one prediction, that the one-draw movement on retraction and expiry replicates reliably (Table~\\ref{tab:v2rcat}) & held \\\\\n",
            "Moved-count control, Amendment 1: Opus 5 at five draws & \\texttt{177697a4ae} & day 40 & Opus 5 at five draws on the moved-count texts against its recorded five-draw row; one prediction, that the one-draw movement on retraction and expiry replicates reliably (Table~\\ref{tab:v2rcat}) & held \\\\\n"
            "%% R129 B1 (2026-09-20): E9's row (registrations/ADDENDUM_V2R_CAT_AMENDMENT_2.md, frozen b0bee9329d, 2026-09-19 = day 40; AUX-V2RCAT-A2-P-M2).\n"
            f"Moved-count control, Amendment 2 & \\texttt{{b0bee9329d}} & day 40 & GPT-5.6 Sol and GPT-5.6 Luna at five draws against their five-draw rows; one prediction, that each falls reliably on both counted states (Table~\\ref{{tab:v2rcat}}) & failed for both on retraction \\\\\n", where="tab:registrations-d row")
    t = rep(t, "the pending answer-stage predictions of Graphiti Amendment 2 and the moved-count control's second amendment are not yet in the count.",
            "the pending answer-stage predictions of Graphiti Amendment 2 are not yet in the count.", where="count paragraph, pending")
    t = rep(t, "Table~\\ref{tab:registrations-d} $28$ with $10$: $92$ predictions, $28$ of which came out otherwise, the count Section~\\ref{sec:setup} states.",
            "%% R129 B1 (2026-09-20): E9's one prediction (P-M2, failed) in the count (AUX-R129-COUNT): 92 / 28 -> 93 / 29; tab:registrations-d 28 with 10 -> 29 with 11.\n"
            "Table~\\ref{tab:registrations-d} $29$ with $11$: $93$ predictions, $29$ of which came out otherwise, the count Section~\\ref{sec:setup} states.", where="count paragraph, total")

    # ---- D: E.3's group table and its sentences, after tab:e3-intent
    t = rep(t, "\\end{tabular}\n\\end{table}\n\n%%V11:1379-1408%%\n",
            "\\end{tabular}\n\\end{table}\n\n"
            "%% R129 D (2026-09-20): the R127 / R127b group readings (AUX-R129-GROUPS), the author's four sentences; no body text yet.\n"
            "Table~\\ref{tab:e3-groups} scores the $104$ obligations against each of the three \\present{} groups.\n"
            "Group (a)'s non-active record is an unrelated fact under the same broad key, so the labels stand: for ``Does Bruna have any upcoming events or deadlines?'' the expired record under \\texttt{event} is a marathon she had already run, while the conference she is to present at is active, and for ``What's Elena's family background?'' the expired record under \\texttt{family\\_member} is a sister's birthday reminder, while the family facts are active.\n"
            "Every model separates the obligations from group (a) less well than from group (c), $0.57$ to $0.68$ against $0.69$ to $0.83$ with the summary.\n"
            "Question only, the three models that score anything without a summary already rank group (a) above the obligations ($0.29$ to $0.40$, below chance), and the summary reverses that reliably without closing the gap; the name lookup, which reads no question, separates the obligations from each group about equally ($0.74$, $0.69$ and $0.74$).\n\n"
            + groups_table() + "\n%%V11:1379-1408%%\n", where="E.3 after tab:e3-intent")

    if check:
        print("appendix_r129.py --check: would write", APPX); return
    APPX.write_text(t, encoding="utf-8", newline="\n")
    print("->", APPX)


if __name__ == "__main__":
    main()
