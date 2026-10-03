# -*- coding: utf-8 -*-
"""report_r131_close.py -- writes reviews/v22/REPORT_R131_CLOSE.md: the checkpoint report of the R131 close (2026-09-20). Every old / new pair is read from
the landing tools' own constants (port_r131_close.py, appendix_r131_close.py), the numbers from r131_close_gate.py, the costed table from
reviews/v22/results/cost_payers_r131_close.md, the gate readings from reviews/v22/gates_r131_close_c.txt; the paragraph census of Sections 2 and 7 and
the float spans are the hand count from the built PDF's margin rows recorded here (2026-09-20 22:40, paper_v22.pdf 9d584193c00c4985).
Usage: python reviews/v22/tools/report_r131_close.py [--hash=<checkpoint commit>]
"""
from __future__ import annotations

import contextlib
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
V22 = ROOT / "reviews" / "v22"
OUT = V22 / "REPORT_R131_CLOSE.md"
sys.path.insert(0, str(V22 / "tools"))
import port_r131_close as C  # noqa: E402
import appendix_r131_close as A  # noqa: E402
import r131_close_gate as G  # noqa: E402


def flat(t):
    return " ".join(l for l in t.strip().split("\n") if not l.startswith("%%")).replace("\n", " ")


def main():
    h = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--hash=")), "(this commit)")
    with contextlib.redirect_stdout(io.StringIO()):
        bad = G.main()
    assert not bad
    P = G.PROV
    gates = (V22 / "gates_r131_close_c.txt").read_text(encoding="utf-8")
    cost = (V22 / "results" / "cost_payers_r131_close.md").read_text(encoding="utf-8")
    table = cost[cost.index("| variant (cumulative)"):cost.index("\n## The probes")].strip()
    L = []
    L.append("# REPORT_R131_CLOSE — the R131 close (2026-09-20; offline, $0, no model call) — BUILT AND STOPPED AT THE PAGE GATE: a checkpoint, not a close\n")
    L.append("Base: the R131 checkpoint `9b1b1ed` / `a78f4b6` (page 10, fine number 495, −10 lines by the slack probe). The author's four blocks landed in one pass: "
             "R131 CONSOLIDATED ADDITIONS (L, A, P, O), ABSTRACT SWAP + ITS PAYER (B1 to B5), R131 MERGED RULINGS (1A, 1B, 1C, 2, 3, 4, 5) and R131 FINAL RULINGS (1 to 8). "
             "The number gate ran first (`reviews/v22/tools/r131_close_gate.py`: 37 checks, 0 mismatches); every gate but the page gate passes on the final build; "
             "**the page gate does not hold: the main text ends on page 10 with every payer applied (fine number 492 against 485), 5 lines short by the slack probe**, so the STOP branch of the close rule applies and the built state is committed as a checkpoint "
             f"(`{h}`, explicit pathspecs). Nothing beyond the ruled payers was cut; O1 did not land (slack below +5).\n")
    L.append(f"Build: tex sha256 `963a19c822b79755`, pdf `9d584193c00c4985`, 83 pages; the main text ends on page 10, the builders box at the top of page 10 (label page 10; the AI-use statement on the same page). "
             "Pages 9 and 10 rasterized and checked: no two word boxes overlap on either page (`page9.png`, `page10.png` in the session scratchpad); the build is clean, no probe residue "
             "(`\\vspace` count in body_v22.tex 0; the fine number 492 equals the k = 0 reading of the last costed variant). `reviews/v22/gates_r131_close_c.txt`:\n")
    L.append("```\n" + "\n".join(gates.strip().split("\n")[1:]) + "\n```\n")
    L.append("Regeneration from scratch: `cp reviews/v21/src/appendix_v21.tex reviews/v22/src/appendix_v22.tex && python reviews/v22/tools/appendix_r126.py && python reviews/v22/tools/appendix_r128.py && "
             "python reviews/v22/tools/appendix_r129.py && python reviews/v22/tools/appendix_r131.py && python reviews/v22/tools/appendix_r131_close.py && python reviews/v22/tools/fig3_data.py && "
             "python reviews/v22/tools/fig3_data_r131.py && python reviews/v22/tools/port_v22.py && python reviews/v22/tools/port_r131.py --payers=1,2,3,4 && "
             "python reviews/v22/tools/port_r131_close.py --payers=5,5b,6,7,8,B2 && python reviews/v22/tools/run_gates.py <tag>`.\n")

    L.append("## The number gate: 0 of 37 fail\n")
    L.append("`r131_close_gate.py` reads every number of the new texts from its artifact and rounds half-up at the printed precision (the convention of every R131 check, so Sol's $-0.3250$ prints 0.33, confirmed as ruled in 1A); "
             "the provenance counts are counted from the tree. The table is `reviews/NUMBERS_R131.md` AUX-R131-CLOSE-PRINTED and AUX-R131-CLOSE-PROV. The rows the abstract rests on:\n")
    L.append("| claim | value | source |\n|---|---|---|\n")
    for c in G.CHECKS[:11]:
        v = c["value"]; vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        L.append(f"| {c['where']} | {c['printed']} <- {vs} | {c['source']} |\n")
    d_mini, d_lookup = P["drops"]
    L.append(f"\nCheck 1 of ABSTRACT SWAP B3: 0.73 / 0.75 and 0.60 / 0.59 are mini and the lookup on the same population and condition (the full obligation set, 661 questions and 104 obligations; the ground-truth summary against FR-Bank's capped store-written summary; tab:levels and tab:levels-strata's 'all 104' row). "
             f"Check 2: 0.08 to 0.10 is the matched metric, reader minus lookup, whole set (Luna +0.1014, Sol +0.0811, Opus +0.0980, each reliable). Check 3: on supersession no stronger model is reliably above the lookup (−0.0057, −0.0057, +0.0114; intervals include zero) and every retraction and expiry lead is positive "
             "(Luna +0.1500 / +0.3667, Sol +0.0833 / +0.3333, Opus +0.2667 / +0.1833; the expiry leads of Luna and Sol and the retraction lead of Opus reliable, the other three not), so the whole-set lead decomposes to the counted states as the abstract says. "
             f"Check 4: G2's pattern does not fire on 'drop from $0.73$ and $0.75$ to $0.60$ and $0.59$'; the pattern reading governs (FINAL RULINGS 3); the drops, for the record, {d_mini:.4f} and {d_lookup:.4f}.\n")

    L.append("## A4': the provenance, verified against the tree\n")
    v = P["fr_released_by_variant"]
    L.append(f"From the FR-Bank release (freeze `5b097fb`, Zenodo 10.5281/zenodo.20067778): {P['personas']} personas, {P['manifests']} human-written manifests, {P['sessions']:,} sessions (35 each), the three stores the main study reads "
             f"(`LifeMemEval/artifacts/lifecycle_banks`, `mem0_41mini_banks`, `amem_banks`; `e1_metamemory/tools/backends.py:59-61`), and {P['released_total']} questions, of which {P['fr_released_distinct']} are asked on the full store and its two ablated variants "
             f"({v['FULL']} / {v['CAT-ABLATED']} / {v['SLOT-ABLATED']}) for {P['fr_items_released']} of the {P['fr_items']} items. This study added the {P['fr_probes']} natural-absent probes ({P['fr_probe_texts']} distinct texts; drafted by a language model and verified against the manifests) and, drafted by GPT-4.1 mini through frozen renderers, the {P['cf_questions']} counterfactual questions with their three versions ({P['cf_items']} items), "
             f"the expiry extension ({P['ext_pairs']} pairs, {P['ext_items']} items), the {P['crossed_asked']} crossed intent questions of {P['crossed_drafted']} drafted, and {P['paraphrases']} paraphrases; it built the {P['graphs']} Graphiti graphs from {P['episodes']:,} episodes rendered from FR-Bank's store records "
             "(`r85_graphiti/render_episodes.py`: one episode per session, every lifecycle field removed), **not from the session transcripts** (the correction of FINAL RULINGS 1). "
             f"The cross-vendor set is {P['xv_items']} of the 661 items ({P['xv_released']} with a released question, {P['xv_probes']} probes) and the question-only probes are classifiers over the existing question strings; neither adds a question (FINAL RULINGS 2).\n")

    L.append("## The cumulative costed table (`reviews/v22/results/cost_payers_r131_close.md`; the R131 instrument, the deficit probed before the Conclusion heading)\n")
    L.append(table + "\n")
    L.append("\nWhat the table says: on the R131 checkpoint's −10, the close's non-payer text costs 6 lines (the abstract is 71 words longer, 210 to 281; A1' adds two lines to Section 4; L1 one line to the Limitations). "
             "Payers 5 and 5b pay nothing by this instrument (the three lines freed on page 5 are absorbed by the float packing; 5b's sentence is four words longer than the one it replaces), payer 6 pays 2, payer 7 pays 4, payer 8 nothing, B2 pays 5. "
             "**The landing with every payer is 5 lines short.** The costing was interrupted once by the harness (a system-memory kill during the seventh variant) and resumed for that variant alone in the foreground; the six recorded variants were not re-run.\n")

    L.append("## Every changed sentence, old beside new, with its reason\n")
    L.append("### The abstract (B1, verbatim; hand-tuned, B4)\n")
    L.append("Before: \"" + flat(ABS_OLD) + "\"\n\nAfter: \"" + flat(C.ABS_NEW) + "\"\n\n"
             "Sentence by sentence: the opener reworded (the cancelled-plan example); the test sentence split in two, the second stating the counterfactual design; finding 1 'rely on the attribute names alone / also use the state counts' for 'read only the names / also read the counts and follow one when it is moved'; "
             "finding 2 'for superseded records, the one state whose names the summary lists' for 'on the state a summary names', the control sentence 'pick the correct name over a similar one at an AUROC of $0.88$ or higher (chance $0.50$)', the lead sentence with its decomposition to retracted and expired records; "
             "finding 3 split in two with the levels 0.73 and 0.75 added; the thesis sentence added; the fetch sentence (0.52 to 0.82) dropped from the abstract (Section 7 and Table 3 keep it); the closing sentence reworded, its last clause a placeholder (B5).\n")
    L.append("### The body and the statements (port_r131_close.py)\n")
    L.append("| item | where | before | after | reason |\n|---|---|---|---|---|\n")
    rows = [
        ("L4", "Section 4", C.L4_OLD, C.L4_NEW, "'(open weights)' at the first mention (CONSOLIDATED ADDITIONS L4; the authors' assertion, FINAL RULINGS 4)"),
        ("A1'", "Section 4", C.A1_OLD, flat(C.A1_NEW), "the provenance sentences (FINAL RULINGS 1; the Graphiti clause as verified)"),
        ("L1", "Limitations", C.L1_OLD, C.L1_NEW, "the author's two sentences; 40 verified against the bank"),
        ("L2", "Limitations", C.L2_OLD, C.L2_NEW, "'completed only' (FINAL RULINGS 4): Kimi ran the cross-model set and was stopped at the budget on the full populations (tab:runs)"),
        ("L3", "Limitations", C.L3_OLD, C.L3_NEW, "cut; C.2 prints within 0.02 (0.8531 / 0.8417, 0.7253 / 0.7167) and Luna's reliable margin +0.0867"),
        ("A2'", "AI-use statement", flat(C.A2_OLD), flat(C.A2_NEW), "the author's statement with the verified Graphiti clause (MERGED RULINGS 2, FINAL RULINGS 1)"),
        ("A5", "AI-use statement", C.A5_OLD, C.A5_NEW, "the word 'preregistered,' dropped (FINAL RULINGS 6)"),
        ("1A", "Table 1's caption", C.TAB1_CAP_OLD.rstrip("}"), C.TAB1_CAP_NEW.rstrip("}"), "the four-word note on the four-decimal difference sub-table"),
        ("1B", "the builders box", C.BOX_OLD, C.BOX_NEW, "the author's words (FINAL RULINGS 4); deletion alone would omit the pooled reliable lead"),
        ("payer 5", "Section 5.1", flat(C.P5_PAR), "(deleted)", "the target-name paragraph out; E.10 tab:resp-l1 prints 0.8572 -> 0.5310 and 0.8897 -> 0.6759, both reliable"),
        ("payer 5", "Section 5.1", C.P5_PTR_OLD.strip(), C.P5_PTR_NEW.strip(), "the pointer of at most six words in the adjacent paragraph"),
        ("payer 5b", "Conclusion", C.P5B_OLD, C.P5B_NEW, "the author's sentence (Luna 0.96, Sol 0.88, Opus 0.99; mini 0.48, Haiku 0.55; the cue list 0.9943)"),
        ("payer 6, P6a", "Section 5.3", C.P6A_OLD.strip(), "(deleted)", "tab:cf-intent's caption already says the body reads the draw-1 column; no caption addition (accepted)"),
        ("payer 6, P6b", "Section 5.3", flat(C.P6B_OLD), flat(C.P6B_NEW), "the Sol sentence deleted; the caption says 9 of its 11 losses score both questions 0.96 or higher"),
        ("payer 6, P6c", "Section 5.3", flat(C.P6C_OLD), flat(C.P6C_NEW), "the author's one sentence for two"),
        ("payer 6, P6d", "Section 5.3", flat(C.P6D_OLD), flat(C.P6D_NEW), "the tolerance sentence deleted; the caption prints the largest fall −0.0458"),
        ("payer 7", "Figure 3", C.P7_OLD, C.P7_NEW, "height −10 percent; width, markers, fonts unchanged; rendered check below"),
        ("payer 8", "Section 5.2", flat(C.P8_OLD), flat(C.P8_NEW), "two sentences after the lead (the lead keeps its run-in form with the author's verb 'lift'); 0.60 / 0.65 and 24 of 88 stay in tab:cf-emptiness and tab:cf-matched"),
        ("payer B2", "Section 1", flat(C.B2_OLD), flat(C.B2_NEW), "the findings paragraph cut to its first sentence and the intent sentence; every deleted claim is in bullets 2 and 3 or Section 5; no number leaves"),
    ]
    for item, where, old, new, why in rows:
        L.append(f"| {item} | {where} | {old.replace('|', chr(92) + '|')} | {new.replace('|', chr(92) + '|')} | {why} |\n")
    L.append("\n### The appendix (appendix_r131_close.py; build_v22.py REPAIRS_R131CLOSE_BLOCK)\n")
    L.append("| item | where | before | after | reason |\n|---|---|---|---|---|\n")
    prov = " ".join(l for l in A.prov_paragraph(P).strip().split("\n") if not l.startswith("%%"))
    arows = [
        ("A1''", "E.3", "(none)", prov, "the provenance paragraph after the section's opening paragraph; third person for the release; every count from the tree"),
        ("A3 follow-up", "E.9", A.E9_OLD, flat(A.E9_NEW), "the earlier ingestion attributed to the release in the third person (it vendors graphiti/ 0.28.1 and graphiti_patches/; the FR paper's FR-Graphiti row); FINAL RULINGS 5"),
        ("A5", "B", A.B_OLD, A.B_NEW, "'registered' (the section is not pinned; code_scan does not gate the appendix, so the plain word is the smallest change)"),
        ("A5", "E.4", A.E4_OLD, A.E4_NEW, "as above"),
        ("A5", "E.4, tab:cluster-sensitivity's caption (carried)", "reports the preregistered item-level interval", "reports the registered item-level interval", "REPAIRS_R131CLOSE_BLOCK (1443, 1462)"),
    ]
    for item, where, old, new, why in arows:
        L.append(f"| {item} | {where} | {old.replace('|', chr(92) + '|')} | {new.replace('|', chr(92) + '|')} | {why} |\n")
    L.append("\nA5, left as ruled: the pinned sections' hits, A (tex 959, 995), E.3 (2845, 2865), E.7 (3212), E.10 (3693, 4102), F (4442); the four artifact names in tab:registrations (4303 to 4314). "
             "'one name longer' in C.2 (two sentences): left, the section is pinned; tab:cf-emptiness prints 81 / 6 / 1 beside them (FINAL RULINGS 3). tex 4565 stays.\n")

    L.append("## Gate trips and rulings\n")
    L.append("- Rule D fired once on the first pass (`gates_r131_close_a.txt`): the abstract's last-but-one sentence against Section 1's thesis sentence, 85%. Overridden as ruled (B4): `tools/prose_scan.py` WHITELIST gains the abstract's sentence with CLAIMS entry R131-CLOSE-B4 as its authority; no word of the abstract changed.\n"
             "- Rule V on 'holds ... fixed': did not fire (the rule bars 'held'); the override is recorded anyway.\n"
             "- G2: no trip under the pattern reading; kept as ruled.\n"
             "- No other prose gate fired on any new text (L, Q-A, S17, slogan, repeat, code_scan all pass; the AI-use statement's 'registered' hits are gone with the word).\n"
             "- frozen_diff: one frozen string left the body, \"were ingested into that backend earlier under a copy\" (E.9's disclosure, replaced), authorized under R131-CLOSE-F.\n"
             "- numeric_diff: one new token, `1,400`, with its disposition in NUMBER_MOVES_V22.md; trace_scan: the new counts ledgered under AUX-R131-CLOSE-PROV.\n"
             "- appendix_identity: B, E.3, E.4 and E.9 pinned under `pin_appendix_r126.py r131close` with their reasons.\n"
             "- Readability: 264 body sentences, 2 over 35 words (report only): Section 5.1's category-reader sentence (36) and Section 5.2's padding sentence (40), both carried from the R131 checkpoint. Overfull boxes: the inherited three.\n")
    L.append("## Payer 7 by render\n")
    L.append("Figure 3 rendered standalone at 5.0cm and 4.5cm (same width, markers, fonts). The only markers near the 0.86 to 0.88 band are Luna 0.8667 and Sol 0.8333 at expiry (left panel, 3pt apart in x): their boxes do not overlap at either height. "
             "Marker-box census: 8 overlapping pairs at 5.0cm, 9 at 4.5cm; the new one is a 0.26pt corner touch between mini 0.9205 and Haiku 0.8920 in the right panel's supersession cluster, outside the band. The pairs that overlap at both heights are readers with equal or near-equal values in one cluster (mini and Haiku at 0.9333 on retraction, all states; the supersession cluster's 0.96 to 0.98 values), unchanged by the cut.\n")

    L.append("## The remaining page budget, for the ruling: the five longest paragraphs of Sections 2 and 7, the evidence table, Table 2's caption, Figure 1 (counted by hand from the built PDF's margin rows; a body line is 11pt)\n")
    L.append("| lines | words | where | paragraph |\n|---:|---:|---|---|\n"
             "| 8 | 60 | Section 2, p2 margin 96 to 103 | Adaptive retrieval decides whether to query a static corpus ... they inspect a bounded view of content. (payer 3's neighbour; the citation-heavy paragraph) |\n"
             "| 7 | 66 | Section 2, p2 margin 104 to p3 109 | Memory systems train or implement writing, updating and querying ... a judgment before retrieval. |\n"
             "| 6 | 32 | Section 2, p3 margin 111 to 116 | Lifecycle information also appears in temporal databases ... (payer 3 as applied: one sentence carrying fourteen citation keys, then the target sentence) |\n"
             "| 6 | 85 | Section 7, p8 margin 398 to 402 | The tagged view complements the summary for mini. |\n"
             "| 5 | 65 | Section 7, p8 margin 404 to 407 | FR-Bank's own tags help mini despite over-marking. (payer 2 as applied) |\n"
             "| 5 | 75 | Section 7, p8 margin 431 to p9 434 | Active copies complicate the use of tagged records. |\n"
             "| 5 | 73 | Section 7, p9 margin 436 to 440 | The tested rule cannot repair copies under different attribute keys. |\n"
             "| 4 | 54 | Section 7, p8 margin 409 to 412 | The lifecycle fetch supplies the added reach, gated or not. |\n"
             "| 3 | 36 | Section 2, p2 margin 93 to 95 | Metamemory separates monitoring a memory state from controlling its use ... |\n"
             "| 3 | 31 | Section 7, p8 margin 424 to 426 | Gating trades budget against licensed-record reach. (payer 1 as applied) |\n"
             "| 3 | 41 | Section 7, p8 margin 427 to 430 | Keeping the newest record misses every tested retraction obligation. |\n")
    L.append("\nThe five longest: 8, 7, 6, 6, and three paragraphs tied at 5 (listed). Section 7 here is 'At retrieval' (the paper's Section 7; Section 6 is 'What backends write').\n\n"
             "- The evidence table (Section 3, page 4): 10 lines (the header row, four two-line rows, the source note 'Evidence condensed from Appendix E.12.'), plus its one-line lead-in sentence at the foot of page 3 ('What kind of evidence supports each result?'); about 110pt from its top rule to the note.\n"
             "- Table 2's caption (page 7): 3 lines ('Table 2: Backend census: ... (Appendices E.7 and E.9)').\n"
             "- Figure 1 with its caption (page 2, a [t] float): the drawing 129pt tall (y 82 to 211) plus the two-line masked-retrieval note under the tag route and the 3-line caption; the float occupies about 200pt, 18 body lines (the margin numbers 55 to 70 fall inside it; the body resumes at 72).\n")

    L.append("## Beside\n")
    L.append("- `reviews/v22/HOUSEKEEPING_24SEP.md` opened with the seven items of FINAL RULINGS 7; nothing else is added to it without asking.\n"
             "- The A3 census (we / our / an agentless passive on creating personas, sessions or manifests) found the two replaced sentences and the AI-use opener; the borderline pair, E.9's disclosure (now attributed) and G.4's 'episodes rendered from FR-Bank's persona banks' (stays), as ruled.\n"
             "- Ledger: `reviews/NUMBERS_R131.md` AUX-R131-CLOSE-PRINTED (37 rows) and AUX-R131-CLOSE-PROV (18 rows); `reviews/v22/NUMBER_MOVES_V22.md` regenerated (ADDED 957, VANISHED 21, 0 unaccounted); CLAIMS.md entries R131-CLOSE-B1, -B4, -B2, -L, -A, -1, -P, -G, -F inside the R126 block (`claims_r126_block.py`).\n"
             "- Tools: `r131_close_gate.py`, `port_r131_close.py`, `appendix_r131_close.py`, `ledger_r131_close.py`, `cost_payers_r131_close.py`, `report_r131_close.py`; `build_v22.py` (REPAIRS_R131CLOSE_BLOCK), `number_moves_wp.py`, `pin_appendix_r126.py` (step r131close), `claims_r126_block.py`, `tools/prose_scan.py` (the B4 whitelist entry), `tools/appendix_identity.py` (the four pins).\n"
             "- Gate runs: `gates_r131_close_a.txt` (all payers, before the bookkeeping), `gates_r131_close_b.txt` (the clean rebuild), `gates_r131_close_c.txt` (the bookkeeping landed; every gate but the page gate passes).\n")
    L.append("## Commits\n")
    L.append(f"The checkpoint commit: `{h}` (explicit pathspecs; the other session's staged `paper_v22_body.tex` and r122 deletions untouched). The follow-up commit records the hash.\n")
    wcost = V22 / "results" / "cost_payers_r131_w.md"
    if wcost.exists():
        wt = wcost.read_text(encoding="utf-8")
        wtable = wt[wt.index("| variant (cumulative)"):wt.index("\n## The probes")].strip()
        gf = V22 / "gates_r131_close_f.txt"
        L.append("\n## The page 8-9 payers W1 to W7 (the author's block 'R131 CLOSE: PAGE 8-9 PAYERS'; `port_r131_w.py`, `cost_payers_r131_w.py`)\n")
        L.append("The number gate first (`r131_w_gate`: 9 checks, 0 mismatches; 30 / 30 pairs, 26 and 15 obligations, the 22 and mini's 0.5210, from r125_matched.json and r125_t3_frbank.json; C.2 prints the coverage intervals (tab:cf-fok) and the one-rewording design). "
                 "Applied in order and costed cumulatively; the +2 target was not reached before W7, so W6 and W7 were used:\n\n" + wtable + "\n\n"
                 "W1: after W1a the '(Appendix A)' pointer joined the line above, so W1b ('Kimi included') was not needed. **The gate trip: W3.** The author's one-sentence form opens its paragraph on the numeral 22 and trips q_scan rule Q-A "
                 "(the R131 checkpoint had split the sentence for that reason); gates may not reword the W texts, so W3 is withdrawn pending the ruling and the R131 split stands meanwhile. W3 bought no line (−3 to −3), and W1 to W7 without it read **+1** (page 9, fine 485). "
                 "Every gate passes on that state (`gates_r131_close_f.txt`); pages 9 and 10 rasterized, no overlap; the builders box closes page 9. "
                 "By the close rule (+1 closes with a note) this state closes once W3 is ruled: either the split stands (nothing further to build) or Q-A is exempted for W3 by ruling and W3 lands (+1 by the costing without W3; W3 changes two words and drops one). "
                 "The consolidated old-beside-new file for everything since `9b1b1ed` is `reviews/v22/R131_CLOSE_CHANGES.md` (34 rows).\n")
    OUT.write_text("".join(L), encoding="utf-8", newline="\n")
    print("->", OUT)


ABS_OLD = ("An agent with persistent memory must judge whether its store holds content it should no longer use. "
           "We test that judgment before retrieval on $148$ questions, each asked of three versions of one store, through summaries that list counts and attribute names with values removed. "
           "First, GPT-4.1 mini and Haiku 4.5 read only the names; GPT-5.6 Luna, GPT-5.6 Sol and Opus 5 also read the counts and follow one when it is moved. "
           "Second, on the state a summary names, no model reliably beats a cosine lookup over the names. With counts and list length kept fixed, the lookup and every model separate the right name from a sibling at or above $0.88$, while meaningless tokens and counts fall to chance. "
           "The three stronger models lead the lookup by $0.08$ to $0.10$ within matched triples, and a lookup given one count feature closes that lead. "
           "Third, the backends we tested omit or misstate this information: under FR-Bank's own metadata, GPT-4.1 mini and the lookup fall to $0.60$ and $0.59$. "
           "At retrieval, a fetch keyed on the names raises reach from $0.52$ to $0.82$, gated by a model or always on, with a budget trade-off. "
           "These synthetic-store tests establish neither better answers nor a validated answer-stage detector; human validation remains pending.")

if __name__ == "__main__":
    main()
