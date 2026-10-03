# -*- coding: utf-8 -*-
"""port_r137.py -- R137 (2026-09-22; the author's brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS') applied to the v23 sources on
top of the R135 close (port_r135.py --units=all, which regenerates the R134 and R133 closes underneath). Every edit is an asserted replacement; every number
the new texts print is read from cf_pad/results/cf_pad_printed.json (report_cf_pad.py) or cf_pad/results/cfpad_printed.json (cfpad_tex.py), the transcribed
Figure 1 lines from the artifact's manifest, and reviews/v23/tools/r137_number_gate.py checks each against its artifact. Units, in the brief's order of work (section 7):

  numbers   section 2 and 3.1: cfpad_tex.py (the C.2 fragments) and robust_tex.py (tab:robust row 9 from cf_pad_scores.json) re-run; the prediction recount in Section 4
            and Appendix F's count paragraph (98 / 31 -> 102 / 33); tab:registrations-e's caption and the long-list check's row (9 with 4)
  appendix  section 4: C.2's 'registered checks' paragraph (three checks) and the new subsection after the paraphrase check (procedure, predictions, the six tables
            through the %%CFPAD-TABLE:<name>%% markers, the counted states' sentence, Opus's draw 1, the seed check, the run notes); tab:setup's row and tab:runs'
            caption; tab:provenance's row; tab:registrations-e's pointer; E.11's spend; E.1's glossary row
  main      sections 3.2, 3.4, 3.5, 3.6: Section 5.2's lead and its long-list paragraph (its own paragraph), the Section 1 bullet, the Conclusion, the Limitations sentence
  abstract  section 3.3: the abstract's fifth sentence replaced by the brief's two, verbatim
  partb     section 5: Figure 1 as a rendered summary (5.1), the two thesis sentences rejoined to their paragraph (5.2), Table 1's dashes for the conditions
            Luna and Sol did not run (5.3)
  p1..p4    section 6, the payers, each applied only as far as needed: P1 5.2's long-list text folded into the opening paragraph and the retraction-and-expiry sentence
            moved to tab:robust's caption; P2 'The rewrites are also vaguer than the originals.' out of the body; P3 Section 8's repeated pointer; P4 the builders box's
            repeated numbers

Logged to reviews/v23/results/port_r137_log.json for OLD_BESIDE_NEW_R137.md (changes_r137.py).
Usage: python reviews/v23/tools/port_r137.py --units=numbers,appendix,...   [--no-refresh]   (--units=all applies numbers..partb; --units=close applies every unit that the close records)
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V23 = ROOT / "reviews" / "v23"
SRC = V23 / "src"
BODY, ABS, APPX = SRC / "body_v23.tex", SRC / "abstract_v23.tex", SRC / "appendix_v23.tex"
LOG = V23 / "results" / "port_r137_log.json"
CLOSE_UNITS = V23 / "results" / "r137_close_units.txt"          # written at the close: the units the close carries (the payers applied)
P = json.load(open(ROOT / "cf_pad" / "results" / "cf_pad_printed.json", encoding="utf-8"))
Q = json.load(open(ROOT / "cf_pad" / "results" / "cfpad_printed.json", encoding="utf-8"))
ORDER = ["numbers", "appendix", "main", "abstract", "partb", "p1", "p2", "p3", "p4"]

TEXT = {}
LOGGED = []


def rd(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def wr(p, t):
    p.write_text(t, encoding="utf-8", newline="\n")


def rep(which, old, new, n=1, unit="", section="", note=""):
    t = TEXT[which]
    c = t.count(old)
    assert c == n, f"[{unit}] {which}: expected {n} occurrence(s), found {c} of: {old[:90]!r}"
    TEXT[which] = t.replace(old, new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old=old, new=new, note=note))


def ins_after(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique ({t.count(anchor)}): {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, anchor + new)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


def ins_before(which, anchor, new, unit="", section="", note=""):
    t = TEXT[which]
    assert t.count(anchor) == 1, f"[{unit}] {which}: anchor not unique ({t.count(anchor)}): {anchor[:90]!r}"
    TEXT[which] = t.replace(anchor, new + anchor)
    LOGGED.append(dict(unit=unit, file=which, section=section, old="", new=new, note=note))


def m(key):
    """A two-decimal printed form from cf_pad_printed.json, in math mode (the magnitude; the direction is in words)."""
    return f"${P[key]['printed']}$"


def lo_hi(a, b):
    x, y = sorted([P[a]["printed"], P[b]["printed"]])
    return f"${x}$ to ${y}$"


# the brief's numbers, asserted against the printed forms before any text is written (section 3.2, 'Check before writing')
assert P["lookup_superseded_loss_pooled"]["printed"] == "0.18" and P["lookup_superseded_loss_pooled"]["reliable"]
assert P["lookup_superseded_pooled_unpadded"]["printed"] == "0.92" and P["lookup_superseded_pooled_padded"]["printed"] == "0.74"
assert {P["luna_superseded_loss_pooled"]["printed"], P["sol_superseded_loss_pooled"]["printed"]} == {"0.06", "0.07"}
assert {P["luna_minus_lookup_superseded_pooled_padded"]["printed"], P["sol_minus_lookup_superseded_pooled_padded"]["printed"]} == {"0.14", "0.13"}
assert {P["luna_minus_lookup_superseded_matched_padded"]["printed"], P["sol_minus_lookup_superseded_matched_padded"]["printed"]} == {"0.10", "0.09"}
assert all(P[k]["reliable"] for k in ("luna_minus_lookup_superseded_pooled_padded", "sol_minus_lookup_superseded_pooled_padded", "luna_minus_lookup_superseded_matched_padded", "sol_minus_lookup_superseded_matched_padded",
                                     "luna_superseded_loss_pooled", "sol_superseded_loss_pooled", "mini_superseded_loss_pooled", "h45_superseded_loss_pooled", "op5_superseded_loss_pooled"))
assert not any(P[k]["reliable"] for k in ("mini_minus_lookup_superseded_pooled_padded", "h45_minus_lookup_superseded_pooled_padded", "op5_minus_lookup_superseded_pooled_padded"))
assert P["predictions"] == {"P-L1": "FAILS", "P-L2": "HOLDS", "P-L3": "HOLDS", "P-L4": "FAILS"} and P["draws"]["OP5"] == 1 and P["draws"]["OP5_recorded"] == 5
LEAD_POOLED = lo_hi("luna_minus_lookup_superseded_pooled_padded", "sol_minus_lookup_superseded_pooled_padded")      # $0.13$ to $0.14$
LEAD_MATCHED = lo_hi("luna_minus_lookup_superseded_matched_padded", "sol_minus_lookup_superseded_matched_padded")   # $0.09$ to $0.10$
LOSS_LS = lo_hi("luna_superseded_loss_pooled", "sol_superseded_loss_pooled")                                        # $0.06$ to $0.07$
LOOKUP_LOSS = m("lookup_superseded_loss_pooled")                                                                    # $0.18$
N_LIST = f"${Q['list_pn']}$"                                                                                        # $60$
OPUS_DRAWS = "one draw; recorded row five draws" if (Q["draws"]["OP5"], Q["draws_recorded"]["OP5"]) == (1, 5) else f"{Q['draws']['OP5']} draws; recorded row {Q['draws_recorded']['OP5']} draws"


# ====================================================================================================================== numbers
def unit_numbers():
    u = "numbers"
    for tool in ("cf_pad/tools/cfpad_tex.py", "reviews/v23/tools/robust_tex.py"):
        r = subprocess.run([sys.executable, str(ROOT / tool)], cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0, r.stdout[-800:] + r.stderr[-800:]
    RB = json.load(open(V23 / "results" / "robust_printed.json", encoding="utf-8"))
    assert RB["rows"][8]["tried"] == "List padded to 60 names" and RB["rows"][8]["status"] == "registered"
    # the prediction recount (98 / 31 -> 102 / 33; r137_number_gate.py; reviews/NUMBERS_R137.md AUX-R137-COUNT)
    rep("body", "The predictions were registered with a bar, each before the run that tests it: $31$ of $98$ came out otherwise.",
        "The predictions were registered with a bar, each before the run that tests it: $33$ of $102$ came out otherwise.",
        unit=u, section="4, the predictions sentence", note="section 2 of the brief: M rises by 4 (P-L1 to P-L4), N by 2 (P-L1, P-L4); AUX-R137-COUNT")
    rep("appendix", "Table~\\ref{tab:registrations-d} $29$ with $11$ and Table~\\ref{tab:registrations-e} $5$ with $2$: $98$ predictions, $31$ of which came out otherwise, the count Section~\\ref{sec:setup} states.",
        "%% R137 (2026-09-22): the long-list check's four predictions (P-L1 and P-L4 failed, P-L2 and P-L3 held) join the count (AUX-R137-COUNT): 98 / 31 -> 102 / 33; tab:registrations-e 5 with 2 -> 9 with 4.\n"
        "Table~\\ref{tab:registrations-d} $29$ with $11$ and Table~\\ref{tab:registrations-e} $9$ with $4$: $102$ predictions, $33$ of which came out otherwise, the count Section~\\ref{sec:setup} states.",
        unit=u, section="F, the count paragraph", note="section 2 of the brief: the recount (AUX-R137-COUNT)")
    # tab:registrations-e: the caption and the row
    rep("appendix", "\\caption{The registration record, continued: the sibling-name control and the names-against-counts amendment on the three stronger models, both registered after the matched metric had been read; the Outcome column lists each prediction's outcome. Both rows were committed before their first call.}",
        "\\caption{The registration record, continued: the sibling-name control and the names-against-counts amendment on the three stronger models, both registered after the matched metric had been read, and the long-list check on the counterfactual set, registered after the paraphrase check had been read; the Outcome column lists each prediction's outcome. Every row was committed before its first call.}",
        unit=u, section="F, tab:registrations-e caption", note="section 4.2 of the brief: the third registration named")
    ins_after("appendix", "the third failed on both; not evaluable on Sol \\\\\n",
              f"%% R137 (2026-09-22): the long-list check (registrations/ADDENDUM_CF_PAD.md, registered text sha256 {Q['registration_sha256'][:8]}..., frozen alone at {Q['frozen_commit']} = day 43 before the first paid call; cf_pad/NUMBERS_CF_PAD.md AUX-CFP-P-L1 to -P-L4).\n"
              f"The long-list check on the counterfactual set & \\texttt{{{Q['frozen_commit']}}} & day 43 & the ${Q['n_items']}$ items' superseded-names lists padded to ${Q['list_pn']}$ names, one pad per triple drawn from the persona's own printed attribute names, the three lookups and the five models at their Table~\\ref{{tab:cf-main}} settings (Opus 5 at one draw against its recorded five-draw row), "
              "pooled AUROC primary and the matched score secondary on the supersession triples (Table~\\ref{tab:robust}); four predictions: each of GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 reliably above the lookup (P-L1), neither GPT-4.1 mini nor Haiku 4.5 reliably above it (P-L2), the lookup reliably losing more than $0.05$ against its unpadded row (P-L3), each of the three stronger models losing less than the lookup (P-L4) & "
              "P-L2 and P-L3 held; P-L1 and P-L4 failed on Opus 5 alone, Luna and Sol as predicted \\\\\n",
              unit=u, section="F, tab:registrations-e row", note="section 4.2 of the brief: the registration in the list with its hash and outcome (the pointer to the C.2 table is set by the appendix unit)")


# ====================================================================================================================== appendix
def unit_appendix():
    u = "appendix"
    D = Q["draws"]; R = Q["rows"]; SP = Q["spend"]; OD = Q["opus_d1"]
    assert Q["seed_reading_changes"] == [] and Q["seed_interval_moves"] == [["MINI_minus_LOOKUP", "45", "persona"]]
    assert sorted(map(tuple, Q["counted_reliable"])) == [("H45", "retracted", "matched"), ("OP5", "retracted", "pooled")]
    assert Q["rank_first"] == 0 and Q["pool_b_pairs"] == 0 and Q["leak_fails"] == 0 and Q["renderer_lock"] == Q["n_items"] == 444
    # (a) the 'Two registered checks' paragraph: three checks, one sentence for the third
    rep("appendix", "\\paragraph{Two registered checks on this set.}", "\\paragraph{Three registered checks on this set.}", unit=u, section="C.2, the registered checks paragraph", note="section 4.1 of the brief: the heading counts the long-list check")
    rep("appendix", "it is reported after Table~\\ref{tab:pad}.\n",
        f"it is reported after Table~\\ref{{tab:pad}}.\nThe long-list check pads the superseded-names lists of this set's own ${Q['n_items']}$ summaries to ${Q['list_pn']}$ names for the three lookups and all five models, with four predictions; it is reported after the paraphrase check.\n",
        unit=u, section="C.2, the registered checks paragraph", note="section 4.1 of the brief: one sentence and a pointer")
    # (b) the new subsection after the paraphrase check, items 1 to 11 of section 4.1
    dec = Q["rank_deciles"]
    block = (
        f"%% R137 (2026-09-22): the long-list check landed (registrations/ADDENDUM_CF_PAD.md, registered text sha256 {Q['registration_sha256'][:8]}..., frozen alone at {Q['frozen_commit']} before the first paid call; run at 6d7f224).\n"
        "%% The prose is written by reviews/v23/tools/port_r137.py from cf_pad/results/cfpad_printed.json and cf_pad_printed.json and the tables by cf_pad/tools/cfpad_tex.py (spliced at the per-table\n"
        "%% markers by build_v23.py); every number through r137_number_gate.py; ledgers cf_pad/NUMBERS_CF_PAD.md (AUX-CFP-*) and reviews/NUMBERS_R137.md (AUX-R137-PRINTED). Report reviews/r136/REPORT_R136.md.\n"
        "\\paragraph{The long-list check.}\n"
        f"The superseded-names list of each of this set's ${Q['n_items']}$ summaries was padded with attribute names drawn from the persona's own printed name map, the pool being the names printed in all three versions of the triple less every name in any version's superseded section, every name a scored question of the persona targets in either population, and the change set; the pool holds ${Q['pool_min']}$ to ${Q['pool_max']}$ names per triple (median ${int(Q['pool_median'])}$), so no pad draws on other personas' names.\n"
        f"One pad is drawn per triple under a recorded seed and the triple's three versions receive the identical pad, so the \\pn{{}} version's list has exactly ${Q['list_pn']}$ names and its siblings' lists are shorter by the committed section alone (${Q['list_min']}$ to ${Q['list_max']}$ names); the counts above the list are left as written, so the superseded total disagrees with the list length, as in the list-length check above.\n"
        f"The target is never in its own pad; its alphabetical rank in the \\pn{{}} list is never first and last on ${Q['rank_last']}$ of the ${Q['rank_n']}$ supersession triples (minimum ${Q['rank_min']}$, median ${Q['rank_median']}$, maximum ${Q['rank_max']}$; by tenths of the list, {', '.join(f'${d}$' for d in dec)}).\n"
        f"The renderer reproduces every committed text byte for byte over the committed names alone (${Q['renderer_lock']}$ of ${Q['n_items']}$), the leak scan reports ${Q['leak_fails']}$ failures, the lookups reproduce their recorded values on the committed lists at four decimals, and the registration was frozen and committed before the first call, with both endpoints, the pooled AUROC and the matched score on the supersession triples, fixed in it.\n"
        f"Caps of \\$${SP['anthropic']['cap']:g}$ (Anthropic) and \\$${SP['openai']['cap']:g}$ (OpenAI) were metered from the rows at the page prices; the run spent \\$${SP['anthropic']['usd']:.2f}$ and \\$${SP['openai']['usd']:.2f}$, no cap was reached, no draw was dropped, and no deviation was recorded.\n"
        "\n"
        "The four predictions, each read on the pooled AUROC of the supersession slice with the matched reading beside it:\n"
        f"P-L1, that each of GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 reliably exceeds the name lookup on the $60$-name list, {P['predictions']['P-L1'].lower()} on Opus 5 (Luna ${P['luna_minus_lookup_superseded_pooled_padded']['value']:+.4f}$ and Sol ${P['sol_minus_lookup_superseded_pooled_padded']['value']:+.4f}$ above it with both intervals, Opus 5 ${P['op5_minus_lookup_superseded_pooled_padded']['value']:+.4f}$ with both intervals including zero; Table~\\ref{{tab:cfpad-minus-lookup}}); "
        f"P-L2, that neither GPT-4.1 mini nor Haiku 4.5 reliably exceeds it, {P['predictions']['P-L2'].lower()} (${P['mini_minus_lookup_superseded_pooled_padded']['value']:+.4f}$ and ${P['h45_minus_lookup_superseded_pooled_padded']['value']:+.4f}$); "
        f"P-L3, that the lookup loses more than $0.05$ against its unpadded row with both intervals below zero, {P['predictions']['P-L3'].lower()} (${P['lookup_superseded_loss_pooled']['value']:+.4f}$; Table~\\ref{{tab:cfpad-sup}}); "
        f"P-L4, that each of the three stronger models loses less than the lookup at the point estimate, {P['predictions']['P-L4'].lower()} on Opus 5 (Luna ${P['luna_superseded_loss_pooled']['value']:+.4f}$ and Sol ${P['sol_superseded_loss_pooled']['value']:+.4f}$ lose less, Opus 5 ${P['op5_superseded_loss_pooled']['value']:+.4f}$ loses more).\n"
        "Luna and Sol are above the lookup on the matched metric as well, both intervals clear of zero (Table~\\ref{tab:cfpad-minus-lookup}).\n"
        "\n"
        "%%CFPAD-TABLE:sup%%\n"
        "%%CFPAD-TABLE:minus-lookup%%\n"
        "%%CFPAD-TABLE:whole%%\n"
        "%%CFPAD-TABLE:counted%%\n"
        "The padded list names neither retraction nor expiry and a triple's three versions carry identical padded lists, so no reader's change on those states is reliable except Haiku 4.5's matched fall on retraction and Opus 5's pooled fall on retraction (Table~\\ref{tab:cfpad-counted}).\n"
        "\n"
        "%%CFPAD-TABLE:other-lookups%%\n"
        "%%CFPAD-TABLE:position%%\n"
        f"Opus 5 ran the padded summaries once against a recorded five-draw row; its recorded draw 1 alone reads ${OD['superseded']['pooled_d1']}$ pooled and ${OD['superseded']['matched_d1']}$ matched on supersession (${OD['whole']['pooled_d1']}$ and ${OD['whole']['matched_d1']}$ on the whole set), and the padded draw minus that draw reads ${OD['superseded']['padded_minus_d1']}$ (${OD['superseded']['ci_item']}$; ${OD['superseded']['ci_persona']}$) on supersession and ${OD['whole']['padded_minus_d1']}$ (${OD['whole']['ci_item']}$; ${OD['whole']['ci_persona']}$) on the whole set, so the fall is not the draw count.\n"
        f"Under seeds ${Q['seeds'][0]}$ to ${Q['seeds'][-1]}$ every registered difference keeps its reading; one interval of one difference, GPT-4.1 mini minus the lookup at seed $45$, moves across zero on the persona side without changing the reading.\n"
        "\n"
        f"Draws: GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna and GPT-5.6 Sol ${D['MINI']}$, Opus 5 ${D['OP5']}$ against its recorded ${Q['draws_recorded']['OP5']}$, at the settings of their Table~\\ref{{tab:cf-main}} rows; the GPT-4.1 mini, Luna and Sol runs through the raw interface, draw by draw, and the Haiku 4.5 and Opus 5 runs through the batch interface; "
        f"${R['MINI']}$ rows per five-draw run and ${R['OP5']}$ for Opus 5, none unparseable.\n"
        "Every served model identifier was checked on a probe call before its run and on every row at scoring; no run reached its cap.\n"
        "\n")
    ins_after("appendix", "An interim aggregate read was taken with the Opus 5 and Sol lanes then pending; no lane or analysis changed after it.\n\n", block,
              unit=u, section="C.2, after the paraphrase check: the long-list check", note="section 4.1 of the brief, items 1 to 11; the tables through the markers; the rank's median printed as the ledger's 41.5 (the brief's 41)")
    # (c) Appendix A: tab:setup's row and tab:runs' caption
    ins_before("appendix", "the full obligation set & $661$ questions",
               f"the counterfactual set, lists padded to ${Q['list_pn']}$ names & ${Q['n_items']}$ items: the same ${Q['n_triples']}$ questions asked of the same three store versions with the superseded-names list padded to ${Q['list_pn']}$ names ({Q['n_triples']} obligations: ${Q['n_sup_triples']}$ supersession, ${Q['n_counted_triples']}$ retraction, ${Q['n_counted_triples']}$ expiry) & "
               f"GPT-4.1 mini ({D['MINI']}), Haiku 4.5 ({D['H45']}), Opus 5 ({D['OP5']}), GPT-5.6 Luna ({D['LUNA']}), GPT-5.6 Sol ({D['SOL']}); the default summary only \\\\\n",
               unit=u, section="A, tab:setup", note="section 4.2 of the brief: the five padded runs in the run coverage")
    rep("appendix", "and five ran its paraphrase set (Table~\\ref{tab:setup}): GPT-4.1 mini one call, Haiku 4.5 five, Opus 5 one, GPT-5.6 Luna and GPT-5.6 Sol five through the raw interface under the default summary only.",
        f"and five ran its paraphrase set (Table~\\ref{{tab:setup}}): GPT-4.1 mini one call, Haiku 4.5 five, Opus 5 one, GPT-5.6 Luna and GPT-5.6 Sol five through the raw interface under the default summary only; "
        f"the same five ran it again with the superseded-names list padded to ${Q['list_pn']}$ names, GPT-4.1 mini, Haiku 4.5, GPT-5.6 Luna and GPT-5.6 Sol at five calls and Opus 5 at one.",
        unit=u, section="A, tab:runs caption", note="section 4.2 of the brief: the five padded runs")
    # (d) tab:provenance's row
    ins_after("appendix", "descriptive registration, no prediction; readings as they came out; the matched metric and the supersession-only comparison post hoc \\\\\n",
              f"Long-list check, the lookup's loss of {LOOKUP_LOSS} and the two leads of {LEAD_POOLED} (Section~\\ref{{sec:lookup}}, Tables~\\ref{{tab:robust}} and~\\ref{{tab:cfpad-sup}}) & ${Q['n_items']}$ items, ${Q['n_triples']}$ triples, with ${Q['list_pn']}$-name lists; the ${Q['n_sup_triples']}$ supersession triples registered & manifest; labels unchanged, the store versions unchanged, the list lengthened with the persona's own names & not needed: versions built from the manifest & ground-truth summary, the superseded-names list padded & pooled AUROC primary and the matched score secondary, both fixed in advance; paired bootstrap (item and persona; triple and persona) & registration committed before the run; two of four predictions held; Opus 5 at one draw \\\\\n",
              unit=u, section="E.12, tab:provenance", note="section 4.2 of the brief: the provenance row")
    # (e) tab:registrations-e's pointer to the C.2 table
    rep("appendix", "pooled AUROC primary and the matched score secondary on the supersession triples (Table~\\ref{tab:robust}); four predictions:",
        "pooled AUROC primary and the matched score secondary on the supersession triples (Table~\\ref{tab:cfpad-sup}); four predictions:",
        unit=u, section="F, tab:registrations-e row", note="the pointer to the C.2 table, now that it exists")
    # (f) E.11: the spend list
    rep("appendix", "the paraphrase drafting run $0.12$ over $413$ calls;",
        f"the paraphrase drafting run $0.12$ over $413$ calls; the long-list check on the counterfactual set ${SP['anthropic']['usd']:.2f}$ of ${SP['anthropic']['cap']:g}$ (Anthropic) and ${SP['openai']['usd']:.2f}$ of ${SP['openai']['cap']:g}$ (OpenAI);",
        unit=u, section="E.11, the spend sentence", note="the run's spend in the list every capped run is in (AUX-CFP-SPEND; token-metered, not an invoice)")
    # (g) E.1: the glossary row
    rep("appendix", "name lookup & the similarity lookup over the summary's superseded-names list, the baseline with no generative-model call that every model is measured against \\\\\n",
        "name lookup & the similarity lookup over the summary's superseded-names list, the baseline with no generative-model call that every model is measured against \\\\\n"
        f"padded list & a superseded-names list lengthened to a fixed size (${Q['list_pn']}$ names) with correct attribute names of the same store that no scored question targets, the counts left as written \\\\\n",
        unit=u, section="E.1, the notation box", note="section 4.2 of the brief: 'padded list' in the glossary")


# ====================================================================================================================== main
LONG_LIST_COMMENT = (
    "%% R137 (2026-09-22), section 3.2: the long-list sentences at the end of the opening paragraph (the brief's first placement; its own paragraph would open with a numeral, q_scan Q-A);\n"
    "%% every number from cf_pad/results/cf_pad_printed.json through r137_number_gate.py (reviews/NUMBERS_R137.md AUX-R137-PRINTED). The ledger over the brief's wording: 'mini, Haiku and Opus lose\n"
    "%% as much or more' reads 'fall with it' (Haiku loses 0.15 against the lookup's 0.18); 'lead ... on both metrics' prints the matched lead too (0.09 to 0.10).\n")
LONG_LIST_A = (f"With the superseded-name list padded to {N_LIST} names (Table~\\ref{{tab:robust}}), the lookup loses {LOOKUP_LOSS} and mini, Haiku and Opus fall with it, ending level with it or below. "
               f"Luna and Sol lose {LOSS_LS} and lead the lookup by a reliable {LEAD_POOLED} pooled and {LEAD_MATCHED} within triples. ")
LONG_LIST_B = "Retraction and expiry do not move, since the list names neither. "
LONG_LIST_END = "(Appendix~\\ref{app:counterfactual})\n\n"
OPENING_END = "Table~\\ref{tab:robust} lists the checks we ran to break this result and what each removes."


def unit_main():
    u = "main"
    # 3.2 the lead and the long-list sentences at the end of the opening paragraph (the own-paragraph placement opens with a numeral and trips q_scan Q-A: gates_r137_main_a.txt)
    rep("body", "\\claim{On the named state, no model reliably beats the lookup.}", "\\claim{On the named state, no model reliably beats the lookup on the short list; on a long one, two do.}",
        unit=u, section="5.2, the opening paragraph", note="section 3.2 of the brief: the lead")
    rep("body", OPENING_END + "\n\n", LONG_LIST_COMMENT + OPENING_END + " " + LONG_LIST_A + LONG_LIST_B + LONG_LIST_END,
        unit=u, section="5.2, the opening paragraph", note="section 3.2 of the brief, at the end of the opening paragraph (the ledger over two phrases, listed in REPORT_R137.md)")
    # 3.4 the second contribution bullet (the brief's clause; the control clause kept with the short-list claim it qualifies)
    rep("body", "\\item Evidence about what readers read. On the named state no model reliably exceeds a name lookup, including under a control that holds counts and list length fixed, and the lookup loses $0.02$ when the questions are reworded to share no word with the names. ",
        f"\\item Evidence about what readers read. On the named state no model reliably exceeds a name lookup when the list is short, including under a control that holds counts and list length fixed, and two of five do when it is padded to {N_LIST} names; the lookup loses $0.02$ when the questions are reworded to share no word with the names. ",
        unit=u, section="1, the second contribution", note="section 3.4 of the brief: the clause added; the control clause stays beside the short-list claim it qualifies (REPORT_R137.md)")
    # 3.5 the Conclusion (two sentences: the brief's clause would take the sentence past prose rule L's 40 words)
    rep("body", "On a named state no model reliably exceeds the name lookup, with list length kept fixed or not, and when the questions are reworded only one stronger model edges past it. ",
        f"On a named state no model reliably exceeds the name lookup on the short list, with list length kept fixed or not, and when the questions are reworded only one stronger model edges past it. "
        f"On a {N_LIST}-name list Luna and Sol lead the lookup by {LEAD_POOLED} and the other three fall with it. ",
        unit=u, section="10, Conclusion", note="section 3.5 of the brief: the clause, as its own sentence (rule L)")
    # 3.6 Limitations
    rep("body", "The paraphrase check covers $115$ of the $148$ questions, its rewrites are vaguer than the originals, and Opus ran it with one draw. ",
        f"The paraphrase check covers $115$ of the $148$ questions, its rewrites are vaguer than the originals, and Opus ran it with one draw. On the {N_LIST}-name list Opus 5 ran one draw against its five-draw short-list row, and the two readers that keep their lead there are from one model family. ",
        unit=u, section="9, Limitations", note="section 3.6 of the brief, verbatim")


# ====================================================================================================================== abstract
OLD_ABS = "Where the summary names the affected attribute, none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length.\n"
NEW_ABS = ("Where the summary names the affected attribute and the list is short, none of five language models reliably beats a cosine-similarity lookup over the names, including under a control that fixes counts and list length.\n"
           f"Padded to {N_LIST} names, the lookup loses {LOOKUP_LOSS}; GPT-5.6 Luna and Sol lose {LOSS_LS} and lead it by {LEAD_POOLED}, while the other three fall with it.\n")


def unit_abstract():
    rep("abstract", OLD_ABS, NEW_ABS, unit="abstract", section="the abstract", note="section 3.3 of the brief, verbatim (numerals in math mode as the source's convention)")
    rep("abstract", "%% R135 (2026-09-21): the brief's abstract (section 3), verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted, 0.88 moved to tab:robust row 3.\n",
        "%% R135 (2026-09-21): the brief's abstract (section 3), verbatim but for the G2 ruling (option c): the parenthetical '(all readers at $0.88$ AUROC or higher)' deleted, 0.88 moved to tab:robust row 3.\n"
        "%% R137 (2026-09-22), section 3.3: the fifth sentence replaced by the brief's two (60 = the PN list length; 0.18 = AUX-CFP-LOOKUP superseded pooled padded minus unpadded -0.1807; 0.06 to 0.07 = AUX-CFP-LUNA/-SOL superseded pooled losses;\n"
        "%% 0.13 to 0.14 = AUX-CFP-MINUS-LOOKUP-SUPERSEDED Luna +0.1375, Sol +0.1274; r137_number_gate.py).\n",
        unit="abstract", section="the abstract", note="the source comment")


# ====================================================================================================================== Part B
def fig1_block():
    """Figure 1 as a rendered summary: the lines transcribed from the summary the E.1 excerpt was cut from (frbank:david:FULL:BELIEVED), abridged to the
    LIFECYCLE TOTALS block, the HOBBIES_RECREATION name line and the superseded-names line; the tag route's record is the store's own hiking_preference entry."""
    A = json.load(open(ROOT / "iclr2027_monitoring_submission" / "ARTIFACT" / "manifests" / "indexes_v2.json", encoding="utf-8"))["indexes"]["frbank:david:FULL:BELIEVED"]
    totals = {}
    for ln in A[A.index("LIFECYCLE TOTALS"):A.index("PER-CATEGORY BREAKDOWN")].splitlines()[1:]:
        mm = re.match(r"\s+([a-z ]+?)\s+(\d+)\s*$", ln)
        if mm:
            totals[mm.group(1)] = int(mm.group(2))
    names = A[A.index("ATTRIBUTE NAMES BY CATEGORY"):A.index("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")]
    mm = re.search(r"^HOBBIES_RECREATION: (.+?)(?=^\S)", names, flags=re.M | re.S)
    hobbies = [x.strip() for x in mm.group(1).replace("\n", " ").split(",") if x.strip()]
    sup = [x.strip() for x in A[A.index("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT"):].split("\n", 1)[1].replace("\n", " ").replace("(+31 more)", "").split(",") if x.strip()]
    assert "hiking_preference" in hobbies and "hiking_preference" in sup and "exam_date" in sup
    E = json.load(open(ROOT / "e1_metamemory" / "backend_entries" / "frbank.json", encoding="utf-8"))
    rec = [e for e in E if e["persona"] == "david" and e["slot"] == "hiking_preference" and e["category"] == "HOBBIES_RECREATION"]
    assert len(rec) == 1 and rec[0]["believed_superseded"]
    tx = lambda s: s.replace("_", "\\_")
    states = [("active", totals["active"]), ("superseded", totals["superseded"]), ("retracted", totals["retracted"]), ("expired", totals["expired"])]
    lines = ["LIFECYCLE TOTALS\\\\"] + [f"\\hspace*{{1em}}\\makebox[7em][l]{{{st}}}\\makebox[2em][r]{{{v}}}\\\\" for st, v in states]   # the summary's own column layout, in typewriter ems
    lines += ["ATTRIBUTE NAMES BY CATEGORY (names only; abridged)\\\\",
              f"\\hspace*{{2ex}}HOBBIES\\_RECREATION: {', '.join(tx(x) for x in hobbies[:3])}, ...\\\\",
              "ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT (abridged)\\\\",
              f"\\hspace*{{2ex}}..., {tx('exam_date')}, ..., {tx('hiking_preference')}, ..."]
    return (
        "\\begin{figure}[t]\n\\centering\n"
        "%% R137 (2026-09-22), Part B 5.1: Figure 1 as a rendered lifecycle summary in the old figure's footprint. The lines are transcribed by reviews/v23/tools/port_r137.py from the summary the E.1 excerpt\n"
        "%% was cut from (iclr2027_monitoring_submission/ARTIFACT/manifests/indexes_v2.json, frbank:david:FULL:BELIEVED; AUX-R86-INDEX-EXCERPT names the same summary), abridged to the LIFECYCLE TOTALS block,\n"
        "%% the HOBBIES_RECREATION name line and the superseded-names line; the tag route's record is e1_metamemory/backend_entries/frbank.json lb_00163 with FR-Bank's own tag (reviews/NUMBERS_R137.md AUX-R137-FIG1;\n"
        "%% r137_number_gate.py). The old schematic and its caption are in reviews/v23/REPORT_R137.md.\n"
        "\\scriptsize\n"
        "\\begin{minipage}[t]{0.625\\linewidth}\n"
        "\\textbf{Summary route}: read before retrieval\\par\\vspace{1pt}\n"
        "\\fbox{\\begin{minipage}{0.96\\linewidth}\\ttfamily\n" + "\n".join(lines) + "\n\\end{minipage}}\n"
        "\\end{minipage}\\hfill\n"
        "\\begin{minipage}[t]{0.36\\linewidth}\n"
        "\\textbf{Tag route}: read on returned records\\par\\vspace{1pt}\n"
        "\\fbox{\\begin{minipage}{0.94\\linewidth}\\ttfamily\n"
        f"{tx(rec[0]['slot'])} [superseded]\\\\\n"
        f"``{rec[0]['text']}''\n"
        "\\end{minipage}}\n"
        "\\end{minipage}\n"
        "\\caption{A lifecycle summary as a reader sees it: counts by state and attribute names with the values removed. The summary route reads this before retrieval; the tag route reads lifecycle tags on returned records. Section~\\ref{sec:framework} defines both.}\n"
        "\\label{fig:framework}\n\\end{figure}\n")


def unit_partb():
    u = "partb"
    # 5.1 Figure 1
    t = TEXT["body"]
    a = t.index("\\begin{figure}[t]\n\\centering\n%% R126 addendum A1 (2026-09-20): the inbox's three-box layout")
    b = t.index("\\label{fig:framework}\n\\end{figure}\n", a) + len("\\label{fig:framework}\n\\end{figure}\n")
    old = t[a:b]
    assert old.count("\\begin{figure}") == 1 and "Tagged store" in old
    new = fig1_block()
    TEXT["body"] = t[:a] + new + t[b:]
    LOGGED.append(dict(unit=u, file="body", section="Figure 1", old=old, new=new, note="section 5.1 of the brief: the schematic replaced by a rendered summary (transcribed lines; AUX-R137-FIG1)"))
    rep("body", "Figure~\\ref{fig:framework} distinguishes reading this summary before retrieval from reading tags on records already retrieved.",
        "Figure~\\ref{fig:framework} shows one such summary, abridged, beside a returned record with its tag.",
        unit=u, section="1, the lifecycle-summary paragraph", note="section 5.1 of the brief: the body sentence adjusted to the new figure")
    # 5.2 the two thesis sentences rejoined to the paragraph they follow (the blank line removed; no rewording)
    rep("body", "We then examine backend writing and retrieval.\n\n%% R131 E (2026-09-20): the author's findings paragraph.\n",
        "We then examine backend writing and retrieval.\n%% R137 (2026-09-22), Part B 5.2: the two thesis sentences rejoined to this paragraph (the figure floated between them and it); no rewording.\n%% R131 E (2026-09-20): the author's findings paragraph.\n",
        unit=u, section="1, the diagnostic-study paragraph", note="section 5.2 of the brief: the paragraph break removed")
    # 5.3 Table 1: a dash for the conditions Luna and Sol did not run
    rep("body", "Luna & superseded & $0.84$ & $[0.80,0.88]$ & $0.88$ & $129/2/17$ \\\\\nSol & superseded & $0.85$ & $[0.81,0.88]$ & $0.86$ & $126/2/20$ \\\\\n",
        "Luna & superseded & $0.84$ & $[0.80,0.88]$ & $0.88$ & $129/2/17$ \\\\\nLuna & all & -- & -- & -- & -- \\\\\nSol & superseded & $0.85$ & $[0.81,0.88]$ & $0.86$ & $126/2/20$ \\\\\nSol & all & -- & -- & -- & -- \\\\\n",
        unit=u, section="Table 1", note="section 5.3 of the brief: a dash where a model did not run a condition; no new column")
    rep("body", "$^{c}$The two read different quantities: the given-category reader ties every supersession triple and is perfect on the counted states by construction.\n",
        "$^{c}$The two read different quantities: the given-category reader ties every supersession triple and is perfect on the counted states by construction. A dash marks a condition the model did not run.\n",
        unit=u, section="Table 1, the note", note="section 5.3 of the brief: the dash explained")


# ====================================================================================================================== the payers (section 6)
def unit_p1():
    """P1: the retraction-and-expiry sentence moved from 5.2's opening paragraph to tab:robust's caption (the fold is the main unit's placement already)."""
    u = "p1"
    rep("body", LONG_LIST_A + LONG_LIST_B + LONG_LIST_END, LONG_LIST_A + LONG_LIST_END,
        unit=u, section="5.2, the opening paragraph", note="P1: the retraction-and-expiry sentence moved to Table 2's caption")
    tex = SRC / "robust_table.tex"
    t = rd(tex)
    old = "Short ground-truth lists do not establish robustness to longer store-written ones. (Appendices"
    new = "Short ground-truth lists do not establish robustness to longer store-written ones. In row 9 retraction and expiry do not move, since the list names neither. (Appendices"
    assert t.count(old) == 1
    wr(tex, t.replace(old, new))
    LOGGED.append(dict(unit=u, file="robust_table", section="Table 2's caption", old=old, new=new, note="P1: the retraction-and-expiry sentence, moved from 5.2 (robust_table.tex is regenerated by robust_tex.py in the numbers unit; the caption edit is re-applied here after it)"))


def unit_p2():
    rep("body", "Under the all-states summary the lookup loses $0.06$ pooled and $0.02$ within triples. The rewrites are also vaguer than the originals. (Appendix~\\ref{app:counterfactual})",
        "Under the all-states summary the lookup loses $0.06$ pooled and $0.02$ within triples. (Appendix~\\ref{app:counterfactual})",
        unit="p2", section="5.2, the rewording paragraph", note="P2: the vaguer sentence leaves the body (it stays in C.2 and tab:para-flags' caption)")


def unit_p3():
    """P3: Section 8's sentences that only repeat a pointer Section 7 already gives. Section 8's two paragraphs point to Appendices A (app:laddertable) and E.8
    (app:baselines); Section 7 points to E.10 (app:resp), G.4 (app:posthoc-graphiti) and its own tables: no pointer is repeated, so nothing is cut (asserted; REPORT_R137.md)."""
    t = TEXT["body"]
    s7 = t[t.index("\\section{At retrieval}"):t.index("\\section{Replication and the coverage judgment}")]
    s8 = t[t.index("\\section{Replication and the coverage judgment}"):t.index("\\section{Limitations}")]
    p7 = set(re.findall(r"\\(?:Appendix|Table|Section)~\\ref\{([^}]*)\}", s7))
    p8 = set(re.findall(r"\\(?:Appendix|Table|Section)~\\ref\{([^}]*)\}", s8))
    assert not (p7 & p8), p7 & p8
    LOGGED.append(dict(unit="p3", file="body", section="8", old="", new="", note=f"P3: Section 8 points to {sorted(p8)} and Section 7 to {sorted(p7)}; no pointer repeated, nothing cut"))


def unit_p4():
    rep("body", "in the all-states comparison and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup, and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).",
        "in the all-states comparison and under FR-Bank's store-written summary, where Haiku sits $0.12$ above the lookup, and in the scenario we priced, a model call before every query cost more than the retrieval it saved (Appendix~\\ref{app:utility-completion}).",
        unit="p4", section="the builders box", note="P4: no number already printed in Sections 5 to 6 is in the box beyond the Haiku 0.12 clause the brief keeps; nothing to cut")


UNITS = {"numbers": unit_numbers, "appendix": unit_appendix, "main": unit_main, "abstract": unit_abstract, "partb": unit_partb, "p1": unit_p1, "p2": unit_p2, "p3": unit_p3, "p4": unit_p4}


def main():
    units = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--units=")), "")
    if units == "all":
        units = ["numbers", "appendix", "main", "abstract", "partb"]
    elif units == "close":
        units = CLOSE_UNITS.read_text(encoding="utf-8").split() if CLOSE_UNITS.exists() else ["numbers", "appendix", "main", "abstract", "partb"]
    else:
        units = [u for u in units.split(",") if u]
    assert all(u in UNITS for u in units), f"unknown unit in {units}; known: {list(UNITS)}"
    assert units == [u for u in ORDER if u in units], f"units must be in the brief's order {ORDER}"
    if "--no-refresh" not in sys.argv:
        subprocess.run([sys.executable, str(V23 / "tools" / "port_r135.py"), "--units=all"], check=True, capture_output=True)
    if "p1" in units:
        assert "main" in units
    TEXT["body"], TEXT["abstract"], TEXT["appendix"] = rd(BODY), rd(ABS), rd(APPX)
    for u in units:
        UNITS[u]()
        print(f"unit {u}: applied ({sum(1 for r in LOGGED if r['unit'] == u)} edits)")
    wr(BODY, TEXT["body"]); wr(ABS, TEXT["abstract"]); wr(APPX, TEXT["appendix"])
    LOG.write_text(json.dumps(dict(units=units, edits=LOGGED), indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"-> {len(LOGGED)} edits logged to {LOG.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
