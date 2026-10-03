"""build_v22.py -- assemble iclr2027_monitoring_submission/paper_v22.tex from the v22 sources (R126; the v21 builder retargeted by bump_v22.py).

  reviews/v22/src/body_v22.tex      the preamble, Sections 1 to 10, the box (the readable body ported by port_v22.py), the statements; %%ABSTRACT%% and %%FIG3-DATA%% markers
  reviews/v22/src/abstract_v22.tex  the abstract, spliced at %%ABSTRACT%%
  reviews/v22/src/fig3_data.tex     Figure 3's data (fig3_data.py), spliced at %%FIG3-DATA%%
  reviews/v22/src/appendix_v22.tex  the appendices' prose (repaired by appendix_r126.py), with %%V11:a-b%% markers

  reviews/v18/src/body_v18.tex      the preamble, Sections 1 to 10, the box, the statements (new text); %%ABSTRACT%% and %%A6-SLOT%% markers
  reviews/v18/src/abstract_v18.tex  the abstract (rule G passing), spliced at %%ABSTRACT%%
  reviews/v18/src/amend6_e10.tex    the Section 8 depth sentence, spliced at %%A6-SLOT%% (its table is in the appendix)
  reviews/v18/src/appendix_v18.tex  the appendices' prose, derived from v17 by reviews/v18/tools/appendix_v18.py, with %%V11:a-b%% markers
  paper_v11.tex                     every table, box, figure and verbatim block, carried by line range (1-indexed, inclusive)

Inside carried blocks the v17 repairs apply unchanged (the tab typo of the authorship-matched table's header; the v18 W wording
repairs carrying AUX-CF2-V2R-DEF), and one v18 repair: the coverage table's row label "counts rand." reads "totals rand.". Every
other carried line is byte-identical to v11. The script prints each marker with the first and last line it resolved to.
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
SRC = ROOT / "reviews" / "v22" / "src"
V11 = SUB / "paper_v11.tex"
OUT = SUB / "paper_v22.tex"


REPAIRS = [  # v18 W: wording corrections inside carried blocks (reviews/v18/tools/wording_v17.py), carried forward
    ('and the first with its retracted and expired counts randomized across store versions.',
     'and the first with its two lifecycle totals, retracted and expired, permuted across store versions (the per-category counts untouched).'),
    ('it had no count-randomized summary',
     'it had no totals-randomized summary'),
    ('the first form has no count-randomized value',
     'the first form has no totals-randomized value'),
    ('\\textit{Counts randomized minus superseded only, whole set (band $\\pm0.05$)}',
     '\\textit{Totals randomized minus superseded only, whole set (band $\\pm0.05$)}'),
]
REPAIRS_V18 = [  # R110: row labels inside carried tables that name the totals-randomized summary
    (', counts rand.\\ &', ', totals rand.\\ &'),
    ('& all three & counts rand. & first: sup.', '& all three & totals rand. & first: sup.'),
]

# R111 (2026-09-15, the writing pass, Phase 2; paper_v18_writing_prompt.md items 34, 35, 61, 80): the renames inside carried v11 blocks,
# each (old, new, count) asserted over all carried lines together; a carried line that is frozen registered text (FROZEN_V11_HEADS) is
# never touched, so the Mem0 SIDE sentence keeps its \trueidx{}. The numbers in every line are untouched.
FROZEN_V11_HEADS = ["On Mem0 the name-bearing index could be built for $49.4$ percent"]
REPAIRS_R111 = [
    # item 34: TRUE / BELIEVED -> ground-truth / store-written (the macros stay defined for the frozen texts)
    ('\\trueidx{} / \\believed{} & summary built from ground truth / from the fields the backend itself exposes',
     'ground-truth / store-written summary & built from ground truth / from the fields the backend itself exposes', 1),
    ('Under \\trueidx{} the marker occupies', 'Under the ground-truth summary the marker occupies', 1),
    ('Under \\believed{} it occupies', 'Under the store-written summary it occupies', 1),
    ('otherwise unchanged \\trueidx{} summary', 'otherwise unchanged ground-truth summary', 1),
    ('the blind and \\trueidx{} rows', 'the blind and ground-truth rows', 1),
    ('blind and \\trueidx{} are the recorded rows', 'blind and ground-truth are the recorded rows', 1),
    ('Blind & \\trueidx{} & Names & Names $-$ blind ($95\\%$ CI) & Names $-$ \\trueidx{} ($95\\%$ CI)',
     'Blind & Ground-truth & Names & Names $-$ blind ($95\\%$ CI) & Names $-$ ground-truth ($95\\%$ CI)', 1),
    ('for the difference from \\trueidx{};', 'for the difference from the ground-truth summary;', 1),
    ('& \\trueidx{} &', '& ground-truth &', 5),
    ('& \\believed{} &', '& store-written &', 5),
    ('the \\trueidx{} obligation row', 'the ground-truth obligation row', 1),
    ('obligation population under \\trueidx{},', 'obligation population under the ground-truth summary,', 1),
    ('The superseded-names section of the truthful summary is re-rendered', 'The superseded-names section of the ground-truth summary is re-rendered', 1),
    ('Truthful & Own name removed', 'Ground-truth & Own name removed', 1),
    ('Lookup, truthful & Lookup, removed', 'Lookup, ground-truth & Lookup, removed', 1),
    # item 61: the smallest model -> GPT-4.1 mini; the superseded-names lookup -> the name lookup; individuated -> identified
    ("the smallest model's obligation discrimination", "GPT-4.1 mini's obligation discrimination", 1),
    ('The smallest model is absent because', 'GPT-4.1 mini is absent because', 1),
    ('failed on the smallest model while holding on the largest', 'failed on GPT-4.1 mini while holding on the largest', 1),
    ('Superseded-names lookup (sup.\\ only)', 'Name lookup (sup.\\ only)', 2),
    ('Superseded-names lookup &', 'Name lookup &', 1),
    ('the superseded-names lookup', 'the name lookup', 4),
    ('The superseded-names lookup was not scored', 'The name lookup was not scored', 1),
    ('whose attribute name individuated the pair', 'whose attribute name identified the pair', 1),
    # item 61: user profile -> persona
    ('grouped by user profile', 'grouped by persona', 1),
    ('Grouped by user profile', 'Grouped by persona', 1),
    ('by user profile &', 'by persona &', 1),
    ('profile interval', 'persona interval', 6),
    # item 80: the author -> we
    ("The flags are the author's read of 2026-09-12", "The flags are our read of 2026-09-12", 1),
]

# R112 (2026-09-15, review-2 A1, the author's ruling): on Mem0 and A-MEM the TRUE index is the manifest rendered under the
# backend's constraints (e1_metamemory/indexes_v2.json meta.availability: lifecycle totals exact, the three name sections
# printed as not expressible), so item 34's rename put "ground-truth" on that meaning inside the carried blocks. These rules
# run on the R111 output, one per site of reviews/v19/A1_CONSTRAINED_RENDERING.md section 2, each asserted to its count;
# "the constrained rendering" is defined once in Section 4. FR-Bank's "ground-truth" uses are untouched. The tab:baselines
# rows take the footnote form (the ruling), the pooled hard row keeps "ground-truth" with the dagger note extended.
REPAIRS_R112 = [
    ('Under the ground-truth summary the marker occupies', 'Under the constrained rendering the marker occupies', 1),
    ('otherwise unchanged ground-truth summary', 'otherwise unchanged constrained rendering', 1),
    ('blind and ground-truth are the recorded rows', 'blind and constrained are the recorded rows', 1),
    ('Blind & Ground-truth & Names & Names $-$ blind ($95\\%$ CI) & Names $-$ ground-truth ($95\\%$ CI)',
     'Blind & Constrained & Names & Names $-$ blind ($95\\%$ CI) & Names $-$ constrained ($95\\%$ CI)', 1),
    ('for the difference from the ground-truth summary;', 'for the difference from the constrained rendering;', 1),
    ('Mem0 FOK & ground-truth &', 'Mem0 FOK & constrained$^{\\ddagger}$ &', 1),
    ('A-MEM FOK & ground-truth &', 'A-MEM FOK & constrained$^{\\ddagger}$ &', 1),
    ('so the one-bit is-FR-Bank rule scores $0.7541$. Paired deltas are unaffected.',
     'so the one-bit is-FR-Bank rule scores $0.7541$, and its Mem0 and A-MEM items are under the constrained rendering. Paired deltas are unaffected.', 1),
    ('where NB-6 leads by $0.0145$ inside the tolerance.}\\\\',
     "where NB-6 leads by $0.0145$ inside the tolerance. $^{\\ddagger}$Ground truth, rendered under the backend's constraints: the lifecycle totals exact, every name section printed as not expressible (Appendix~\\ref{app:inversion}).}\\\\", 1),
    # R112 (2026-09-16), the integration pass, item 73 of the checklist: the carried E.7 marker paragraph's "reviewer" token.
    ('A reviewer asked whether the marker itself carries the inversion.', 'A review asked whether the marker itself carries the inversion.', 1),
    # R112 (2026-09-16), v19_prompt.md R8: the carried appendix tables' row labels name the models as the body does (line-initial labels only;
    # the registered prediction rows "P1: luna ..." are quoted registration text and stay).
    ('luna & ', 'GPT-5.6 Luna & ', 11),
    ('sol & FOK & ', 'GPT-5.6 Sol & FOK & ', 1),
    ('sol & NOK & ', 'GPT-5.6 Sol & NOK & ', 1),
    ('sol & external pooled & ', 'GPT-5.6 Sol & external pooled & ', 1),
]

# R115 (2026-09-18, the Knowing-the-Store patch): one placement repair keyed to its carried block. Removing the nine uncited
# bibliography entries pulled Appendix B up by a third of a page; Table tab:crossvendor-predictions no longer fits "here" at
# the foot of its page, is deferred to the top of the next page, and the float barrier before Appendix C then ends that page
# after two lines (page 16 of the first build of 18 September was mostly blank). Placed [H] the table stays in the text flow
# and the pagination of the 17 September build returns. Keyed by the marker's line range so no other carried [h] table is
# touched; asserted to its count.
REPAIRS_R115_BLOCK = {
    (1004, 1020): [('\\begin{table}[h]', '\\begin{table}[H]', 1)],
}

# R116 (2026-09-18, the provenance fix; reviews/r115/PROVENANCE_AUDIT.md section 2): the R81 row of the carried registration table a
# cites a commit prefix that does not exist (2bb7fd97... is the R79 clarity-report commit and holds no R81 text); the registration file's
# first commit is 5c3621b75e (2026-08-29 17:11 +05:30), before the first NB-6 output. Keyed to the table's block; asserted to its count.
REPAIRS_R116_BLOCK = {
    (2084, 2118): [('\\texttt{2bb7fd9dc4}', '\\texttt{5c3621b75e}', 1)],
    # R116 (2026-09-19, the author's ruling on the harness rows): the marker $^{h}$ on every GPT-5.6 Luna / Sol row elicited through the
    # vendor's agent harness (the August ladder runs), defined in the Appendix B paragraph before tab:ladder-exact. These rules run on the
    # R112 output (the row labels already read 'GPT-5.6 Luna' / 'GPT-5.6 Sol').
    (913, 943): [('GPT-5.6 Luna & FOK & $84$', 'GPT-5.6 Luna$^{h}$ & FOK & $84$', 1), ('GPT-5.6 Luna & NOK & $84$', 'GPT-5.6 Luna$^{h}$ & NOK & $84$', 1),
                 ('GPT-5.6 Sol & FOK & $84$', 'GPT-5.6 Sol$^{h}$ & FOK & $84$', 1), ('GPT-5.6 Sol & NOK & $84$', 'GPT-5.6 Sol$^{h}$ & NOK & $84$', 1),
                 ('while mini is the original primary elicitation.', "while mini is the original primary elicitation; $^{h}$ marks the rows elicited through the vendor's agent harness (the paragraph above).", 1)],
    (980, 997): [('stratified set, $n=150$ per model', 'stratified set$^{h}$, $n=150$ per model', 1), ('stratified set, $n=150$ & failed', 'stratified set$^{h}$, $n=150$ & failed', 1),
                 ('cross-model set, $n=84$', 'cross-model set$^{h}$, $n=84$', 3)],
    (1575, 1766): [('GPT-5.6 Sol & external pooled & $66$', 'GPT-5.6 Sol$^{h}$ & external pooled & $66$', 1), ('GPT-5.6 Luna & external pooled & $66$', 'GPT-5.6 Luna$^{h}$ & external pooled & $66$', 1)],
}

# R123 (2026-09-19, the v21 update and writing pass, Phase D; the author's brief): repairs inside carried blocks, each keyed to its block and asserted to
# its count, applied after the R112 renames (so the E.7 sentence is matched in its 'A review asked' form). No number changes except the two rows added.
REPAIRS_R123_BLOCK = {
    # E.7: the review's marker question as plain motivation
    (1575, 1766): [('A review asked whether the marker itself carries the inversion. A descriptive probe registered after the review therefore left every summary byte-identical',
                    'Whether the marker itself carries the inversion is a separate question. A descriptive probe left every summary byte-identical', 1)],
    # Appendix A captions: 'the expansion' and 'the ladder run' in plain words
    (956, 978): [('\\caption{The full-population expansion:', '\\caption{The full-population runs:', 1)],
    (980, 997): [('Five capability items were registered before the ladder run.', 'Five capability items were registered before the cross-model run.', 1)],
    # C.2, tab:counterfactual: the GPT-5.6 Sol and Luna paired rows (model minus the lookup on the default summary; r82_counterfactual/cf2/NUMBERS_CF2.md
    # section 13, AUX-CF2-OAI-P-S1 +0.0836 [+0.0401,+0.1315]; [+0.0544,+0.1163], AUX-CF2-OAI-P-S2 +0.0754 [+0.0339,+0.1216]; [+0.0450,+0.1090])
    (1191, 1268): [('Opus 5, all three & $+0.0323$ & $[+0.0060,+0.0617]$ & $[+0.0077,+0.0608]$ & $0.9079$ & $0.8756$ \\\\',
                    'Opus 5, all three & $+0.0323$ & $[+0.0060,+0.0617]$ & $[+0.0077,+0.0608]$ & $0.9079$ & $0.8756$ \\\\\n'
                    'GPT-5.6 Sol, superseded only & $+0.0836$ & $[+0.0401,+0.1315]$ & $[+0.0544,+0.1163]$ & $0.8500$ & $0.7663$ \\\\\n'
                    'GPT-5.6 Luna, superseded only & $+0.0754$ & $[+0.0339,+0.1216]$ & $[+0.0450,+0.1090]$ & $0.8417$ & $0.7663$ \\\\', 1)],
    # R124 D2 (2026-09-19): the program code in the question-signal table's note (Appendix C)
    (1054, 1074): [('the registered R74 FOK-target probe re-derives', 'the registered coverage-target probe re-derives', 1)],
    # G.2, tab:flag-split's note: a pooled AUROC is not a weighted average of the halves
    (2194, 2215): [('the whole-set values of Table~\\ref{tab:counterfactual} are the weighted combination of the two halves.',
                    'the whole-set values of Table~\\ref{tab:counterfactual} are computed on the pooled items; a pooled AUROC also orders positives of one half against negatives of the other, so it is not a weighted average of the halves.', 1)],
}

# R126 (2026-09-20, the readable body; the brief's Phase 4; reviews/v22/tools/appendix_r126.py carries the prose edits): repairs inside carried blocks, each keyed
# to its block and asserted to its count, applied after the R123 rules (so E.7's captions are matched in their R111 / R112 form). No number changes.
REPAIRS_R126_BLOCK = {
    # Phase 4.4, anonymity: the registration record's calendar dates become the day index of the registration order (day 0 = the first freeze;
    # reviews/NUMBERS_R126.md AUX-R126-DAYS); the hashes stay. The caption and the column header say so.
    (2084, 2118): [('lists each frozen monitoring artifact, commit, date, scope, and outcome.', 'lists each frozen monitoring artifact, commit, freeze day (day 0 is the first freeze), scope, and outcome.', 1),
                   ('Artifact & Commit hash & Freeze date & What it froze & Outcome', 'Artifact & Commit hash & Freeze day & What it froze & Outcome', 1),
                   ('& 2026-08-10 &', '& day 0 &', 7), ('& 2026-08-11 &', '& day 1 &', 3), ('& 2026-08-14 &', '& day 4 &', 2),
                   ('& 2026-08-24 &', '& day 14 &', 7), ('& 2026-08-29 &', '& day 19 &', 2), ('& 2026-08-30 &', '& day 20 &', 1)],
    # Phase 4.2(c): E.7's captions in the body's terms (question only / with the summary), the old term kept in parentheses beside its column
    (1575, 1766): [('while only some indexed scores fall below chance.', 'while only some scores under the summary (the indexed rows) fall below chance.', 1),
                   ('beside the recorded blind and intact rows.', 'beside the recorded question-only (blind) and intact rows.', 1),
                   ('without lifting either above blind.', 'without lifting either above question only.', 1),
                   ('blind and constrained are the recorded rows of Table', 'question only (blind) and constrained are the recorded rows of Table', 1)],
}


# R128 (2026-09-20, the Program Chairs' feedback filtered against v22; reviews/v22/R128_BRIEF.md sections B and C; the prose edits are
# reviews/v22/tools/appendix_r128.py): repairs inside carried blocks, keyed to their line ranges and asserted to their counts, applied after
# the R126 rules (so E.7's captions are matched in their R126 form). No number changes.
REPAIRS_R128_BLOCK = {
    # C: the prompt template's delimiters print as the backticks the prompt uses. In T1 slot 96 is the opening quotation mark and slot 0 the
    # grave; \textasciigrave would go to the TS1 typewriter font, which MiKTeX has only as a bitmap (a Type 3 font, hygiene_scan F476).
    (1359, 1373): [('\\char96\\char96\\char96\\{summary\\}\\char96\\char96\\char96', '\\char0\\char0\\char0\\{summary\\}\\char0\\char0\\char0', 1)],
    # C: the cross-model predictions table's fifth row labelled; the harness marker defined in the table's own note
    (980, 997): [('Sol blind FOK remains below $0.75$ & $0.8131>0.75$', 'P5: Sol blind FOK remains below $0.75$ & $0.8131>0.75$', 1),
                 ('\\bottomrule', '\\bottomrule\n\\multicolumn{4}{@{}p{0.96\\linewidth}@{}}{\\footnotesize $^{h}$Rows elicited through the vendor\'s agent harness (Appendix~\\ref{app:laddertable}).}\\\\', 1)],
    # C: the counterfactual sub-analysis table's header and the lookups' persona intervals (an AUROC, not a difference: no leading plus)
    (1191, 1268): [('persona interval & first & first gain \\\\', 'persona interval & first draw & first-draw gain \\\\', 1),
                   ('$[+0.7226,+0.8051]$', '$[0.7226,0.8051]$', 1), ('$[+0.8391,+0.9111]$', '$[0.8391,0.9111]$', 1), ('$[+0.5587,+0.5981]$', '$[0.5587,0.5981]$', 1)],
    # B5: the pooled count-destruction table's caption carries the pooled tier's qualification and points to the within-store table
    (1467, 1484): [('a different names-only result driven by the structureless external stores.}',
                    'a different names-only result driven by the structureless external stores. Every positive of the pooled tier is an FR-Bank item and every Mem0 and A-MEM item a negative, so the pooled level reflects cross-store differences; Table~\\ref{tab:destruction-fr} is the controlled within-store comparison.}', 1)],
    # B4: the marker-read-as-absence probe's word 'absent' is also a label's name; the inversion table's harness marker defined in its caption
    (1575, 1766): [('It does not resolve the mechanism, because the score stays below blind at the point estimate on both stores.',
                    'It does not resolve the mechanism, because the score stays below blind at the point estimate on both stores. The instruction\'s word ``absent\'\' is also the name of a label, so the probe cannot separate a reading of the marker from a reading of the label.', 1),
                   ('while only some scores under the summary (the indexed rows) fall below chance.}',
                    'while only some scores under the summary (the indexed rows) fall below chance. $^{h}$ marks rows elicited through the vendor\'s agent harness (Appendix~\\ref{app:laddertable}).}', 1)],
    # C: NB-6 bridged to the body's term in the baseline table's caption (the body points to Appendix E.8)
    (1780, 1806): [('The NB-6 column is filled on the obligation rows only:', 'The NB-6 column (the name lookup) is filled on the obligation rows only:', 1)],
}


# R131 close (2026-09-20; FINAL RULINGS 6, A5): the carried caption of tab:cluster-sensitivity (Appendix E.4, v11 lines 1443-1462) reads
# 'registered' for 'preregistered'; keyed to its block and asserted to its count. No number changes.
REPAIRS_R131CLOSE_BLOCK = {
    (1443, 1462): [('reports the preregistered item-level interval', 'reports the registered item-level interval', 1)],
}


def read(p):
    return io.open(p, encoding="utf-8").read().replace("\r\n", "\n")


def main():
    v11 = read(V11).split("\n")
    body = read(SRC / "body_v22.tex")
    abstract = re.search(r"\\begin\{abstract\}.*?\\end\{abstract\}\n", read(SRC / "abstract_v22.tex"), flags=re.S).group(0)
    # the Section 8 depth sentence is written in body_v18.tex in the author's words of 2026-09-15 (amend6_e10.tex keeps the table)
    assert body.count("%%ABSTRACT%%\n") == 1
    body = body.replace("%%ABSTRACT%%\n", abstract)
    # R126 (2026-09-19), Phase 3: Figure 3's data file (reviews/v22/src/fig3_data.tex, written by fig3_data.py from the artifacts) spliced at %%FIG3-DATA%%
    # R131 (2026-09-20): Figure 3 is drawn on the matched metric from reviews/v22/src/fig3_data_matched.tex (fig3_data_r131.py), spliced at
    # %%FIG3-DATA-MATCHED%%; the pooled data file is spliced in Appendix C.2 at %%FIG3-DATA-POOLED%% with its table macros renamed, for the pooled figure there.
    assert body.count("%%FIG3-DATA%%\n") + body.count("%%FIG3-DATA-MATCHED%%\n") == 1
    body = body.replace("%%FIG3-DATA%%\n", read(SRC / "fig3_data.tex"))
    body = body.replace("%%FIG3-DATA-MATCHED%%\n", read(SRC / "fig3_data_matched.tex"))
    appx = read(SRC / "appendix_v22.tex")
    if "%%FIG3-DATA-POOLED%%\n" in appx:
        assert appx.count("%%FIG3-DATA-POOLED%%\n") == 1
        pooled = read(SRC / "fig3_data.tex").replace("\\figthreeSup", "\\figthreeSupPooled").replace("\\figthreeAll", "\\figthreeAllPooled")
        appx = appx.replace("%%FIG3-DATA-POOLED%%\n", pooled)
    text = body + appx
    n_typo = 0
    n_repair = [0]
    n_repair18 = [0]
    n_r111 = {o: 0 for o, _, _ in REPAIRS_R111}
    n_r112 = {o: 0 for o, _, _ in REPAIRS_R112}
    n_r115 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R115_BLOCK.items() for o, _, _ in rules}
    n_r116 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R116_BLOCK.items() for o, _, _ in rules}
    n_r123 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R123_BLOCK.items() for o, _, _ in rules}
    n_r126 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R126_BLOCK.items() for o, _, _ in rules}
    n_r128 = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R128_BLOCK.items() for o, _, _ in rules}
    n_r131c = {(lo, hi, o): 0 for (lo, hi), rules in REPAIRS_R131CLOSE_BLOCK.items() for o, _, _ in rules}

    def repl(m):
        nonlocal n_typo
        a, b = int(m.group(1)), int(m.group(2))
        block = v11[a - 1:b]
        fixed = []
        for ln in block:
            for o, n_ in REPAIRS:
                if o in ln:
                    ln = ln.replace(o, n_); n_repair[0] += 1
            for o, n_ in REPAIRS_V18:
                if o in ln:
                    ln = ln.replace(o, n_); n_repair18[0] += 1
            if not any(h in ln for h in FROZEN_V11_HEADS):
                for o, n_, _ in REPAIRS_R111:
                    k = ln.count(o)
                    if k:
                        ln = ln.replace(o, n_); n_r111[o] += k
                for o, n_, _ in REPAIRS_R112:      # on the R111 output
                    k = ln.count(o)
                    if k:
                        ln = ln.replace(o, n_); n_r112[o] += k
            for o, n_, _ in REPAIRS_R115_BLOCK.get((a, b), []):   # R115: keyed to this block's line range
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r115[(a, b, o)] += k
            for o, n_, _ in REPAIRS_R116_BLOCK.get((a, b), []):   # R116: the R81 hash in the carried table a
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r116[(a, b, o)] += k
            for o, n_, _ in REPAIRS_R123_BLOCK.get((a, b), []):   # R123: Phase D repairs inside carried blocks
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r123[(a, b, o)] += k
            for o, n_, _ in REPAIRS_R126_BLOCK.get((a, b), []):   # R126: the readable body's appendix repairs inside carried blocks
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r126[(a, b, o)] += k
            for o, n_, _ in REPAIRS_R128_BLOCK.get((a, b), []):   # R128: the feedback's appendix repairs inside carried blocks
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r128[(a, b, o)] += k
            for o, n_, _ in REPAIRS_R131CLOSE_BLOCK.get((a, b), []):   # R131 close: A5 inside the carried E.4 caption
                k = ln.count(o)
                if k:
                    ln = ln.replace(o, n_); n_r131c[(a, b, o)] += k
            if "\textit{Monitors}" in ln:            # the literal tab + "extit" of the v11 file
                ln = ln.replace("\textit{Monitors}", "\\textit{Monitors}"); n_typo += 1
            fixed.append(ln)
        print(f"  %%V11:{a}-{b}%%  {len(block):4d} lines  first: {block[0][:60]!r}  last: {block[-1][:60]!r}")
        return "\n".join(fixed)

    out = re.sub(r"%%V11:(\d+)-(\d+)%%", repl, text)
    assert "%%V11:" not in out, "unresolved marker"
    assert "%%ABSTRACT%%" not in out and "%%A6-SLOT%%" not in out and "%%TAIL%%" not in out and "%%FIG3-DATA" not in out
    assert "\u2014" not in out, "em dash"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    print(f"typo repairs applied inside carried blocks: {n_typo}")
    print(f"v18 W wording repairs applied inside carried blocks: {n_repair[0]} (expected {len(REPAIRS)})")
    print(f"R110 row-label repairs applied inside carried blocks: {n_repair18[0]}")
    assert n_repair[0] == len(REPAIRS), "a carried-block repair did not apply exactly once"
    bad = [(o, n_r111[o], k) for o, _, k in REPAIRS_R111 if n_r111[o] != k]
    print(f"R111 renames applied inside carried blocks: {sum(n_r111.values())} substitutions over {len(REPAIRS_R111)} rules" + (f"; COUNT MISMATCH {bad}" if bad else ""))
    assert not bad, bad
    bad112 = [(o, n_r112[o], k) for o, _, k in REPAIRS_R112 if n_r112[o] != k]
    print(f"R112 renames applied inside carried blocks: {sum(n_r112.values())} substitutions over {len(REPAIRS_R112)} rules" + (f"; COUNT MISMATCH {bad112}" if bad112 else ""))
    assert not bad112, bad112
    bad115 = [(key, n_r115[key], k) for (lo, hi), rules in REPAIRS_R115_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r115[key] != k]
    print(f"R115 block repairs applied inside carried blocks: {sum(n_r115.values())} substitutions over {len(n_r115)} rules" + (f"; COUNT MISMATCH {bad115}" if bad115 else ""))
    assert not bad115, bad115
    bad116 = [(key, n_r116[key], k) for (lo, hi), rules in REPAIRS_R116_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r116[key] != k]
    print(f"R116 block repairs applied inside carried blocks: {sum(n_r116.values())} substitutions over {len(n_r116)} rules" + (f"; COUNT MISMATCH {bad116}" if bad116 else ""))
    assert not bad116, bad116
    bad123 = [(key, n_r123[key], k) for (lo, hi), rules in REPAIRS_R123_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r123[key] != k]
    print(f"R123 block repairs applied inside carried blocks: {sum(n_r123.values())} substitutions over {len(n_r123)} rules" + (f"; COUNT MISMATCH {bad123}" if bad123 else ""))
    assert not bad123, bad123
    bad126 = [(key, n_r126[key], k) for (lo, hi), rules in REPAIRS_R126_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r126[key] != k]
    print(f"R126 block repairs applied inside carried blocks: {sum(n_r126.values())} substitutions over {len(n_r126)} rules" + (f"; COUNT MISMATCH {bad126}" if bad126 else ""))
    assert not bad126, bad126
    bad128 = [(key, n_r128[key], k) for (lo, hi), rules in REPAIRS_R128_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r128[key] != k]
    print(f"R128 block repairs applied inside carried blocks: {sum(n_r128.values())} substitutions over {len(n_r128)} rules" + (f"; COUNT MISMATCH {bad128}" if bad128 else ""))
    assert not bad128, bad128
    bad131c = [(key, n_r131c[key], k) for (lo, hi), rules in REPAIRS_R131CLOSE_BLOCK.items() for o, _, k in rules for key in [(lo, hi, o)] if n_r131c[key] != k]
    print(f"R131 close block repairs applied inside carried blocks: {sum(n_r131c.values())} substitutions over {len(n_r131c)} rules" + (f"; COUNT MISMATCH {bad131c}" if bad131c else ""))
    assert not bad131c, bad131c
    print(f"-> {OUT} ({len(out.splitlines())} lines)")


if __name__ == "__main__":
    main()
