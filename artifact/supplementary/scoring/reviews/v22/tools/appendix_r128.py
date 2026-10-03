# -*- coding: utf-8 -*-
"""appendix_r128.py -- program R128 (2026-09-20; the Program Chairs' LLM feedback filtered against v22, the author's brief reviews/v22/R128_BRIEF.md),
sections B and C on the appendix. Runs after appendix_r126.py on reviews/v22/src/appendix_v22.tex; every edit is an asserted replacement (OLD occurs
exactly once); idempotent through a marker. The carried v11 blocks are repaired in build_v22.py (REPAIRS_R128_BLOCK). Items:
  B1  E.3: the coverage half of the rubric and the reply schema, verbatim from the frozen prompts_e1.py (PREREG_E1 records its hash)
  B2  E.7: the below-chance rows explained by what tab:dist shows (a collapse onto few values with positives slightly below negatives), not by compression
  B3  E.7: the pooled 66's sampling (AUX-R128-POOLED66)
  B5  tab:destruction's caption: a carried block (build_v22.py)      B4: tab:q4-marker's paragraph, a carried block (build_v22.py)
  B7  tab:ds-body prints both denominators (AUX-R128-DS-DENOM); its caption says the gated policies abstain on some reached obligations
  B8  tab:cf3-expiry gains Opus 5's draw-1 rows (AUX-R128-CF3-DRAW1); its caption says so
  B10 Appendix F: GR-1 to GR-5 beside P1 to P4 on the Graphiti rows
  C   the punch list that lives in the prose tables: 1,273 / 3,305 spacing; the moved-count draw-1 rows labelled and noted; 0.75 said to be rounded;
      pairs -> triples for the three-version items; tab:bh-split's lookup interval moved to its persona row; tab:ds's header spacing; tab:ds-body-lower's
      dash filled; E.11's currency signs; G.4's +0.1014 and the 784 / 72 edges; tab:marker's h defined; tab:baselines' NB-6 bridged
Usage: python reviews/v22/tools/appendix_r128.py [--check]
"""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
DEN = ROOT / "reviews" / "v22" / "results" / "r128_ds_denoms.json"
CF3 = ROOT / "reviews" / "v22" / "results" / "r128_cf3_draw1.json"


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:100])
    return t.replace(old, new)


def main():
    check = "--check" in sys.argv
    t = APPX.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "%% R126 (2026-09-20), Phase 4.2(a)" in t, "run appendix_r126.py first"
    if "%% R128 B1" in t:
        print("appendix_r128.py: already applied"); return

    # ---- B1: the coverage half of the rubric, verbatim from the frozen prompt
    t = rep(t, "The obligation half of the elicitation rubric, which Section~\\ref{sec:setup} points to, read in full:\n",
            "%% R128 B1 (2026-09-20): the coverage half and the reply schema, verbatim from e1_metamemory/tools/prompts_e1.py (frozen; PREREG_E1.md records its sha256); one call elicits both judgments.\n"
            "One call elicits both judgments. The coverage half of the rubric read in full: ``FOK (feeling of knowing): the probability, 0 to 100, that the store contains content relevant to this question -- anything that should shape the answer.'' The reply is one JSON object, \\texttt{\\{\"fok\": <0-100>, \"nok\\_candidates\\_found\": <true|false>, \"nok\": <0-100>, \"would\\_search\": <true|false>\\}}, and the system text adds that the two judgments are independent (``A store can hold plenty of relevant content with nothing stale in it, and it can hold stale content on a topic it otherwise covers poorly.'') and that the model must not attempt to answer the question; \\texttt{would\\_search} is not scored.\n"
            "The obligation half of the elicitation rubric, which Section~\\ref{sec:setup} points to, read in full:\n")

    # ---- B2: E.7's explanation of the below-chance rows
    t = rep(t, "What the summary does to the score is compression, the indexed monitor answering almost every question with the same low value.\n",
            "%% R128 B2 (2026-09-20): the explanation corrected to what tab:dist shows; compression alone cannot move an AUROC (an order-preserving transform).\n"
            "What the summary does to the score is a collapse onto a few low values, with the positives averaging slightly below the negatives (Table~\\ref{tab:dist}).\n")
    t = rep(t, "What triggers the compression is unresolved, and the ablations that narrowed it follow.\n",
            "What triggers the collapse is unresolved, and the ablations that narrowed it follow.\n")
    t = rep(t, "The indexed monitor therefore compresses every question toward one low value rather than reordering the questions by anything it reads.\n"
               "Which line of the summary produces the compression is the question the ablations above leave open; the marker's wording is not it (Table~\\ref{tab:marker}).\n",
            "Compression alone cannot lower an AUROC below $0.50$, because AUROC is unchanged by any order-preserving transform; what the rows show is a collapse onto five values in which the positives average slightly below the negatives ($0.1617$ against $0.1688$ on Mem0, $0.1544$ against $0.1658$ on A-MEM), and that ordering is the inversion.\n"
            "The store-written summaries, which carry no not-expressible line, show no loss (within tolerance of blind, above), and the name-bearing summary rebuilt from ground truth restores coverage (Table~\\ref{tab:s1-names}), so the loss belongs to the constrained rendering; which line of it produces the collapse is the question the ablations above leave open, and the marker's wording is not it (Table~\\ref{tab:marker}).\n")
    t = rep(t, "The summary compresses the score toward a low value on both stores. Descriptive.}", "The summary collapses the score onto a few low values on both stores, the positives slightly below the negatives. Descriptive.}")

    # ---- B3: the pooled 66's sampling, beside the paragraph that first names the pooled 66 rows (the tab:inversion lead-in)
    d = json.loads(DEN.read_text(encoding="utf-8"))
    p66 = d["pooled66"]
    t = rep(t, "and $-0.0313$ on A-MEM, $[-0.0983,+0.0400]$ and $[-0.0798,+0.0208]$ (Table~\\ref{tab:baselines}).\n",
            "and $-0.0313$ on A-MEM, $[-0.0983,+0.0400]$ and $[-0.0798,+0.0208]$ (Table~\\ref{tab:baselines}).\n"
            "%% R128 B3 (2026-09-20): the pooled 66's sampling (reviews/NUMBERS_R128.md AUX-R128-POOLED66; ADDENDUM_E1_5.md Run A).\n"
            f"The pooled $66$ external questions of its GPT-5.6 rows are the Mem0 and A-MEM part of a $150$-item stratified subsample of the main study's universe (seed $42$; quota $50$ present, $60$ absent, $40$ obligations, which resolves by backend to FR-Bank $84$, Mem0 $29$, A-MEM $37$): "
            f"${p66['mem0|PRESENT']}$ Mem0 and ${p66['amem|PRESENT']}$ A-MEM questions on the full stores, all \\present{{}}, and ${p66['mem0|ABSENT']}$ and ${p66['amem|ABSENT']}$ natural-absent probes, all \\absent{{}}; ${p66['mem0|PRESENT'] + p66['amem|PRESENT']}$ positives and ${p66['mem0|ABSENT'] + p66['amem|ABSENT']}$ negatives over ${d['pooled66_personas']}$ personas; no obligation, since the obligation labels are FR-Bank's.\n")

    # ---- B7: tab:ds-body with both denominators
    rows = {r["policy"]: r for r in d["ds_rows"]}
    old_hdr = "Policy & \\hd{Forbidding records}{in view (of $104$)} & \\hd{Stale answers}{(of $104$)} & \\hdl{Stale rate over the}{reached, scorable} & \\hdl{Wilson}{interval} & \\hd{Correct}{(of $174$)} \\\\"
    new_hdr = "Policy & \\hd{Forbidding records}{in view (of $104$)} & \\hd{Stale answers}{(of $104$)} & \\hdl{Stale, of the reached}{scorable obligations} & \\hdl{Stale, of the answered}{subset; Wilson} & \\hd{Correct}{(of $174$)} \\\\"
    t = rep(t, old_hdr, new_hdr)
    t = rep(t, "\\begin{tabular}{@{}lrrllr@{}}\n\\toprule\n" + new_hdr, "\\begin{tabular}{@{}lrrllr@{}}\n\\toprule\n" + new_hdr)
    for pol, old_cell in (("Top-5 retrieval", "$8$ of $42$, $0.19$ & $[0.10,0.33]$"), ("Model rule", "$8$ of $62$, $0.13$ & $[0.07,0.23]$"), ("Lookup rule", "$6$ of $58$, $0.10$ & $[0.05,0.21]$"),
                          ("Model rule, all states named and scored", "$11$ of $65$, $0.17$ & $[0.10,0.28]$"), ("Literal lookup rule (descriptive)", "$13$ of $82$, $0.16$ & $[0.10,0.25]$"), ("Oracle", "$16$ of $85$, $0.19$ & $[0.12,0.28]$")):
        r = rows[pol]
        new_cell = (f"${r['stale']}$ of ${r['reached_scorable']}$, ${r['rate_reached']:.2f}$ & ${r['stale']}$ of ${r['answered_scorable']}$, ${r['rate_answered']:.2f}$ $[{r['wilson_answered'][0]:.2f},{r['wilson_answered'][1]:.2f}]$")
        t = rep(t, old_cell, new_cell, 1, pol)
    t = rep(t, "The stale and correct counts are a token detector's, read by one of us where flagged, with its limits in Appendix~\\ref{app:resp}; its human validation is pending.",
            "%% R128 B7 (2026-09-20): both denominators (AUX-R128-DS-DENOM).\n"
            "The stale and correct counts are a token detector's, read by one of us where flagged, with its limits in Appendix~\\ref{app:resp}; its human validation is pending. The stale rate is printed over two denominators, every reached obligation the detector can score (supersession and retraction in view; expiry is unscorable) and the subset the policy answered, because the gated policies abstain on some reached obligations (the model rule answers $62$ of its $73$ reached scorable obligations, the lookup rule $58$; the top-five, literal and oracle policies abstain on none).")
    # tab:ds-body-lower: the missing Wilson interval
    lo, hi = d["wilson_11_65"]
    t = rep(t, "Model rule, all states named and scored & $110$ & $0.8558$; -- & $11.42$ & $72$ & $60$ \\\\", f"Model rule, all states named and scored & $110$ & $0.8558$; $[{lo:.3f},{hi:.3f}]$ & $11.42$ & $72$ & $60$ \\\\")
    # tab:ds's second header block: space between the licensed total and the correct count
    t = rep(t, "\\begin{tabular}{@{}lrrlrl@{}}\\toprule\nPolicy & answered & stale at $0.80$ & stale at $0.50$, tagged / untagged & present answered & correct at $0.50$ \\\\ \\midrule",
            "\\begin{tabular}{@{}lrrlr@{\\hspace{10pt}}l@{}}\\toprule\nPolicy & answered & stale at $0.80$ & stale at $0.50$, tagged / untagged & present answered & correct at $0.50$ \\\\ \\midrule", 2)

    # ---- B8: tab:cf3-expiry gains Opus 5's draw-1 rows
    c = json.loads(CF3.read_text(encoding="utf-8"))
    def cell(k, arm):
        a = c[k]["opus"][arm]
        return f"${a['indexed']:.4f}$ $[{a['item_ci']['ci_lo']:+.4f},{a['item_ci']['ci_hi']:+.4f}]$"
    ext = {"v2": "$0.5638$ $[-0.0867,+0.2840]$", "v3": "$0.9452$ $[+0.2593,+0.6318]$", "v2r": "$0.6084$ $[-0.0830,+0.2792]$"}
    new_rows = "".join(f"Opus 5, draw 1 & {s} & {cell('draw1_cf2_expiry', arm)} & {ext[arm]} & {cell('draw1', arm)} \\\\\n"
                       for arm, s in (("v2", "sup.\\ only"), ("v3", "all three"), ("v2r", "totals rand.")))
    t = rep(t, "Opus 5 & totals rand. & $0.6092$ $[+0.0008,+0.2140]$ & $0.6084$ $[-0.0830,+0.2792]$ & $0.6068$ $[+0.0115,+0.1974]$ \\\\\n\\bottomrule",
            "Opus 5 & totals rand. & $0.6092$ $[+0.0008,+0.2140]$ & $0.6084$ $[-0.0830,+0.2792]$ & $0.6068$ $[+0.0115,+0.1974]$ \\\\\n"
            "%% R128 B8 (2026-09-20): Opus 5 read at draw 1 on every pair (reviews/v22/results/r128_cf3_draw1.json; AUX-R128-CF3-DRAW1), beside the recorded rows.\n" + new_rows + "\\bottomrule")
    t = rep(t, "Opus 5's rows are five-call averages on the $444$ and single calls on the extension, so its pooled row mixes the two.",
            "Opus 5's rows are five-call averages on the $444$ and single calls on the extension, so its pooled row mixes the two; the rows below them read Opus 5 at its first draw on every pair, so the pooled value there mixes nothing.")
    # the lookups' persona intervals without leading plus signs (an AUROC, not a difference)
    t = rep(t, "Name lookup & sup.\\ only & $0.5000$ $[+0.5000,+0.5000]$ & $0.5000$ $[+0.5000,+0.5000]$ & $0.5000$ $[+0.5000,+0.5000]$ \\\\",
            "Name lookup & sup.\\ only & $0.5000$ $[0.5000,0.5000]$ & $0.5000$ $[0.5000,0.5000]$ & $0.5000$ $[0.5000,0.5000]$ \\\\")
    t = rep(t, "All-states lookup & all three & $0.8711$ $[+0.7864,+0.9424]$ & $0.9694$ $[+0.9475,+1.0000]$ & $0.8977$ $[+0.8376,+0.9477]$ \\\\",
            "All-states lookup & all three & $0.8711$ $[0.7864,0.9424]$ & $0.9694$ $[0.9475,1.0000]$ & $0.8977$ $[0.8376,0.9477]$ \\\\")

    # ---- B10: GR-1 to GR-5 beside P1 to P4 in Appendix F
    t = rep(t, "& P1 failed on recall, held on precision; P2 held, P3 failed, P4 held on the corrected full-store population (Appendix~\\ref{app:posthoc-graphiti}) \\\\",
            "& P1 failed on recall, held on precision; P2 held, P3 failed, P4 held on the corrected full-store population; the three-persona readings read here: GR-1 failed, GR-2 not computable, GR-3 held, GR-4 and GR-5 descriptive (Appendix~\\ref{app:posthoc-graphiti}) \\\\")
    t = rep(t, "& the gain reading failed, the lookup reading held; the coverage reading not computable \\\\",
            "& GR-1 (the gain) failed, GR-2 (coverage) not computable, GR-3 (the lookup) held, GR-4 and GR-5 descriptive, all read at forty personas \\\\")

    # ---- C: the punch list in the prose tables
    t = rep(t, "change the tag on $1,273$ of the $3,305$ lines shown", "change the tag on $1{,}273$ of the $3{,}305$ lines shown")
    t = rep(t, "Opus 5, draw 1 ($k=1$) & whole set & $0.8405$ & $0.8049$ &", "Opus 5, draw 1 ($k=1$)$^{d}$ & whole set & $0.8405$ & $0.8049$ &")
    t = rep(t, "Name lookup & whole set & $0.7663$ & $0.7663$ & the name sections are unchanged \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}",
            "Name lookup & whole set & $0.7663$ & $0.7663$ & the name sections are unchanged \\\\\n\\bottomrule\n\\end{tabular}\n"
            "\\par\\smallskip\\begin{minipage}{0.97\\linewidth}\\tiny\n"
            "%% R128 C (2026-09-20): the draw-1 rows compare the registered single-draw run with the recorded five-draw row (AUX-V2RCAT-OP5); the first draw alone reads $0.8400$ on the whole set (Appendix C.2), a comparison the registration did not make.\n"
            "$^{d}$The draw-1 rows are the registered comparison of the single-draw moved-count run with the recorded five-draw row ($0.8405$); against Opus 5's first draw alone ($0.8400$, Appendix~\\ref{app:counterfactual}) the whole-set difference would read $-0.0351$, a comparison the registration did not make. Amendment 1's $k=5$ rows above remove the mismatch.\n"
            "\\end{minipage}\n\\end{table}")
    t = rep(t, "{\\textbf{NOK by model, FR-Bank}; the name lookup scores $0.75$ on the same $661$ questions}", "{\\textbf{NOK by model, FR-Bank}; the name lookup scores $0.75$ (rounded from $0.7484$) on the same $661$ questions}")
    t = rep(t, "The $30$ expiry pairs show why, because the three versions of each pair can be read side by side.", "The $30$ expiry triples show why, because the three versions of each triple can be read side by side.")
    t = rep(t, " & item & & & & $[0.6722,0.8992]$ & $[-0.4288,-0.0430]$ & $[-0.3613,+0.1503]$ \\\\\n & persona & & & & & $[-0.6568,+0.0182]$ & $[-0.5208,+0.4381]$ \\\\",
            " & item & & & & & $[-0.4288,-0.0430]$ & $[-0.3613,+0.1503]$ \\\\\n & persona & & & & $[0.6722,0.8992]$ & $[-0.6568,+0.0182]$ & $[-0.5208,+0.4381]$ \\\\")
    t = rep(t, "views $0.14$ and Opus 5 on the moved-count control $4.52$, under a $40$ ceiling", "views \\$$0.14$ and Opus 5 on the moved-count control \\$$4.52$, under a \\$$40$ ceiling")
    t = rep(t, "Store's superseded-name lookup & $0.6780$ & Minus capped monitor $+0.1014$: $[+0.0102,+0.2086]$; $[+0.0094,+0.1988]$. P3 fails; GR-3 holds. \\\\",
            "Store's superseded-name lookup & $0.6780$ & Minus capped monitor $+0.1014$ (from the unrounded scores): $[+0.0102,+0.2086]$; $[+0.0094,+0.1988]$. P3 fails; GR-3 holds. \\\\")
    t = rep(t, "$8{,}382$ edges are active, $130$ superseded and $677$ expired; $784$ carry no validity time and $72$ are dated after the persona's clock.",
            "$8{,}382$ edges are active, $130$ superseded and $677$ expired (the three sum to the $9{,}189$); inside those counts, $784$ carry no validity time and $72$ are dated after the persona's clock, an undated edge that no invalidation touches counting as active.")
    t = rep(t, "GPT-5.6 Luna on the pooled $66$ questions through the raw API at five calls, with its recorded harness rows beside.",
            "GPT-5.6 Luna on the pooled $66$ questions through the raw API at five calls, with its recorded harness rows beside ($^{h}$: elicited through the vendor's agent harness, Appendix~\\ref{app:laddertable}).")

    if check:
        print("appendix_r128.py --check: every OLD found; nothing written"); return
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(t)
    print(f"-> {APPX}")


if __name__ == "__main__":
    main()
