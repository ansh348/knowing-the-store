# -*- coding: utf-8 -*-
"""r118_apply.py -- program R118: the v21 lineage's edits, each an asserted replacement in reviews/v21/src (OLD occurs exactly once; LF
preserved; idempotent; --check reports without writing). Edits are grouped by the ruling that authorised them; `--only g1,g2` applies the
named groups; `--src <dir>` applies to a copy of the sources (the scratch build that costs a landing before it is ruled on). The
CLAIMS.md R118 block records each landed edit (reviews/v21/claims_r118_block.md is the working copy of that block).

  pointer       the Section 4 harness pointer (landed, R118-1)
  e5            the R117 E5 landing (ruling 3): abstract, Section 1 (thesis sentence and bullet), Section 5, Table 1 rows, Conclusion,
                Limitations, tab:runs, tab:pnpresent rows                                                     -- drafted, not landed
  e5_perstate   one optional Section 5 sentence on where the margin lies (the per-state reading of ruling 2)   -- drafted, not landed
  e2            the E2 landing: one Section 5 sentence after the own-name ablation; tab:cf-names-counts in C.2  -- drafted, not landed
  e3            the E3 landing: Section 7's pooled-66 sentence on the raw-API reading, one sentence on the marker; tab:marker in E.7
  e3_u5         the Limitations sentence (U5, pinned byte-identical: needs the author's ruling on that string)  -- drafted, not landed
  e4            the E4 landing: one negative Section 9 sentence; tab:ds-a8 in E.10                              -- drafted, not landed
  payer_e4      Section 9's "Two further results" paragraph moved whole to E.10 (the landing map's payer)       -- drafted, not landed
  sec8          the author's ruling 4 of 19 September (page space): Section 8 cut to four sentences (the replication opener, the
                cross-model gains, the indexed levels against the lookup on the 661 questions with the question-signal caveat, one
                coverage sentence pointing at tab:cov-lookup and tab:cf-fok); tab:e1 moved whole to Appendix A after the expansion
                table; the coverage paragraph (the detection floor) moved whole to E.8 after tab:cov-lookup       -- drafted, not landed
  notation      the same ruling's notation-box proposal: the row "named state; counted state" dropped (0 and 2 uses in the body
                prose), "reads" dropped from the verbs row (0 uses in the defined sense), "all-states lookup" dropped from the
                lookup row (1 use, which now carries the definition inline)                                       -- proposed, not landed
"""
from __future__ import annotations

import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
DEFAULT_SRC = ROOT / "reviews" / "v21" / "src"
TABLES = ROOT / "reviews" / "v21" / "src" / "r117_tables_v21.tex"


def block(name):
    t = TABLES.read_text(encoding="utf-8")
    m = re.search(r"%%BLOCK " + re.escape(name) + r"%%\n(.*?)\n%%END " + re.escape(name) + r"%%", t, flags=re.S)
    assert m, name
    return m.group(1)


SEC8_HEAD = "%% Writing pass Phase 1 (2026-09-15), item 2: the old Section 8 split; this section keeps the replication and the coverage result.\n"
SEC8_TAIL = "The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\n"
SEC8_NEW = (
    "%% R118 ruling 4 (2026-09-19, page space): Section 8 cut to four sentences; Table tab:e1 moved whole to Appendix A after the expansion table\n"
    "%% and the coverage paragraph moved whole to Appendix E.8 after tab:cov-lookup (reviews/v21/tools/r118_apply.py, group sec8). No number changes.\n"
    "The obligation gain replicates across six models from three vendors.\n"
    "Every paired gain excludes zero where the blind score varies, the five such models on the cross-model set gaining $+0.15$ to $+0.45$, Kimi K3 among them at $+0.26$ (Table~\\ref{tab:ladder-exact}, Appendix~\\ref{app:laddertable}).\n"
    "Haiku 4.5, Opus 5 and GPT-5.6 Luna score $0.82$ to $0.83$ indexed on the full obligation set against the name lookup's $0.75$ on the same $661$ questions (Table~\\ref{tab:e1}), levels that include what the question wording gives away (Section~\\ref{sec:setup}).\n"
    "On coverage the easy-tier margin over the name lookup does not survive a lookup over the whole name map (Table~\\ref{tab:cov-lookup}, Appendix~\\ref{app:baselines}), and on the counterfactual set every model's coverage interval excludes chance (Table~\\ref{tab:cf-fok}, Appendix~\\ref{app:counterfactual}).\n"
)
SEC8_TABLE_LEAD = ("%% R118 ruling 4 (2026-09-19): Table tab:e1 moved whole from Section 8 (its float specifier [h] to [H], the appendix's convention); the words and values are unchanged.\n"
                   "Table~\\ref{tab:e1}, from Section~\\ref{sec:populations}, gives the two-decimal reading of the obligation rows beside the name lookup's level on the same questions, and the coverage judgment by backend for GPT-4.1 mini.\n\n")
SEC8_COVERAGE_HEAD = ("\\paragraph{The coverage judgment against its floor.}\n"
                      "%% R118 ruling 4 (2026-09-19): Section 8's coverage paragraph moved whole from the body; its pointer to this appendix now names the table. No number changes.\n")


def sec8_span(body_path):
    """The current Section 8 text between its Phase 1 comment and its last sentence, or None once the group has been applied."""
    t = body_path.read_text(encoding="utf-8")
    if SEC8_HEAD not in t:
        return None
    i = t.index(SEC8_HEAD); j = t.index(SEC8_TAIL, i) + len(SEC8_TAIL)
    return t[i:j]


def sec8_edits(BODY, APPX):
    old = sec8_span(BODY)
    if old is None:                       # applied already: anchor checks only
        return [(BODY, SEC8_NEW, SEC8_NEW)]
    assert old.count("\\begin{table}[h]") == 1 and old.count("\\end{table}\n") == 1, "Section 8 carries one table"
    a = old.index("\\begin{table}[h]"); b = old.index("\\end{table}\n", a) + len("\\end{table}\n")
    table = "\\begin{table}[H]" + old[a + len("\\begin{table}[h]"):b]
    cov = old[b:].lstrip("\n")
    assert cov.startswith("The coverage margin over the name lookup does not survive a lookup over the whole name map.\n"), cov[:80]
    cov = cov.replace("which is not a reliable one (Appendix~\\ref{app:baselines}).", "which is not a reliable one (Table~\\ref{tab:cov-lookup}).")
    assert "Table~\\ref{tab:cov-lookup})." in cov
    return [
        (BODY, old, SEC8_NEW),
        (APPX, "%%V11:956-978%%\n", "%%V11:956-978%%\n\n" + SEC8_TABLE_LEAD + table),
        (APPX, "\n\\subsection{Census of the store-written state}\\label{app:census}\n",
               "\n" + SEC8_COVERAGE_HEAD + cov + "\n\\subsection{Census of the store-written state}\\label{app:census}\n"),
    ]


def groups(src):
    BODY, APPX, ABS = src / "body_v21.tex", src / "appendix_v21.tex", src / "abstract_v21.tex"
    return {
        "sec8": sec8_edits(BODY, APPX),
        "cr": [   # ruling 2 of 19 September: the count readers' descriptions (reviews/r117/COUNT_READERS_NOTE.md; reviews/NUMBERS_R110.md AUX-R110-A1-CR; reviews/NUMBERS_WP.md AUX-WP-B-ORDERING)
            (BODY,
             "the other is a count reader that guesses the question's category from its text and reads that category's retracted and expired \\emph{counts}.\nA category-aware count reader, which takes the category from the manifest, is that reader's upper bound on the two counted states.\n",
             "the other is a count reader that guesses the question's category from its text and reads the share of that category's entries that are no longer active.\nA category-aware count reader takes the category from the manifest instead and reads that category's retracted-plus-expired \\emph{count}.\n"),
            (BODY,
             "($30$ pairs each), its category-aware oracle at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$.",
             "($30$ pairs each), the category-aware count reader at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$."),
            (APPX,
             "The category-aware count reader knows the question's category from the manifest and reads that category's retracted-plus-expired count; the category-guessing reader assigns the category from the question by the recorded rule of the question-only baseline suite and reads the same count; a state-aware reader, an upper bound that knows the state as well as the category, reads the state's own cell.\n",
             "%% R118 (ruling 2 of 2026-09-19; reviews/r117/COUNT_READERS_NOTE.md): the two readers read different quantities; the descriptions corrected, the definitions made exact.\n"
             "The category-aware count reader knows the question's category from the manifest and reads that category's retracted-plus-expired count, a count.\n"
             "The category-guessing reader assigns the category from the question by the recorded rule of the question-only baseline suite and reads a different quantity at that category, the share of its entries that are superseded, retracted or expired.\n"
             "A state-aware reader, which knows the state as well as the category, reads the state's own cell.\n"),
            (APPX,
             "so the present-negative version's increment reads against zero within its triple.\n",
             "so the present-negative version's increment reads against zero within its triple.\n"
             "%% AUX-WP-B-ORDERING (reviews/NUMBERS_WP.md section 8): category-aware reader 0 / 88 / 0 and category-guessing reader 34 / 54 / 0 on the supersession triples.\n"
             "Within a supersession triple the count table differs only in the superseded column of the target's category, which the category-aware reader does not read, so it ties all $88$ supersession triples; the category-guessing reader's share includes that column, so it orders the $34$ triples whose assigned category is the target's and ties the other $54$.\n"
             "Read at the manifest category, that share scores $0.8473$ on the whole set ($0.8981$ on supersession, $0.7336$ on retraction, $0.8528$ on expiry): a reader given the question's category, computed after the fact, above GPT-4.1 mini, Haiku 4.5 and Opus 5 on the whole set (Table~\\ref{tab:cf-cr}).\n"),
            (APPX,
             "the totals reader the two lifecycle totals, and the category-guessing reader the count at the category the question-only suite's rule assigns. The category-aware reader separates the versions on the counted states; every model is below it on both.",
             "the totals reader the two lifecycle totals, and the category-guessing reader the share of superseded, retracted and expired entries at the category the question-only suite's rule assigns. The last reader row reads that share at the manifest category: privileged, since the category is given, and added after the fact. The category-aware reader separates the versions on the counted states; every model is below it on both."),
            (APPX,
             "State-aware reader (an upper bound) & $0.8580$ & $0.9006$ & $0.8944$ & $0.7778$ & $[0.8150,0.8998]$ \\\\\n",
             "State-aware reader & $0.8580$ & $0.9006$ & $0.8944$ & $0.7778$ & $[0.8150,0.8998]$ \\\\\n"),
            (APPX,
             "Category-guessing reader & $0.6623$ & $0.6573$ & $0.6669$ & $0.6872$ & $[0.6273,0.6991]$ \\\\\n",
             "Category-guessing reader & $0.6623$ & $0.6573$ & $0.6669$ & $0.6872$ & $[0.6273,0.6991]$ \\\\\n"
             "%% R118 (ruling 2): CR-oracle-share, reviews/NUMBERS_R110.md AUX-R110-A1-CR (v2 row); privileged and post hoc.\n"
             "\\addlinespace\n"
             "\\multicolumn{6}{@{}l}{\\textit{Post hoc and privileged: the category-guessing reader's share read at the manifest category}}\\\\\n"
             "Category-given share reader & $0.8473$ & $0.8981$ & $0.7336$ & $0.8528$ & $[0.8071,0.8873]$ \\\\\n"),
        ],
        "cr_clause": [   # ruling 2: the Section 5 clause, drafted for its page cost only (not landed without a ruling)
            (BODY,
             "where every model scores $0.53$ to $0.62$.\n",
             "where every model scores $0.53$ to $0.62$.\n"
             "A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual}).\n"),
        ],
        "fig3": [   # ruling 3 of 19 September: Sol and Luna markers on Figure 3's left panel (AUX-CF2-OAI-SOL-V2, -LUNA-V2 per state), caption note
            (BODY,
             "      \\addplot[draw=black, fill=black] coordinates {(Whole,0.8405) (Sup.,0.9325) (Retr.,0.5872) (Exp.,0.6150)};\n  \\nextgroupplot[title={all-states summary}]\n",
             "      \\addplot[draw=black, fill=black] coordinates {(Whole,0.8405) (Sup.,0.9325) (Retr.,0.5872) (Exp.,0.6150)};\n"
             "      %% R118 (ruling 3 of 2026-09-19): GPT-5.6 Sol and GPT-5.6 Luna as markers, not bars (they ran the superseded-only summary only; r82_counterfactual/cf2/results/cf_scores_openai.json).\n"
             "      \\addplot[ybar=0pt, bar shift=0pt, only marks, mark=diamond*, mark size=2.4pt, mark options={fill=white, draw=black, line width=0.5pt}, xshift=11.5pt] coordinates {(Whole,0.8500) (Sup.,0.9383) (Retr.,0.5322) (Exp.,0.6403)};\n"
             "      \\addplot[ybar=0pt, bar shift=0pt, only marks, mark=triangle*, mark size=2.4pt, mark options={fill=black, draw=black}, xshift=15.5pt] coordinates {(Whole,0.8417) (Sup.,0.9426) (Retr.,0.5458) (Exp.,0.6167)};\n"
             "  \\nextgroupplot[title={all-states summary}]\n"),
            (BODY,
             "      \\addlegendimage{draw=black, fill=black!45, pattern=crosshatch dots, pattern color=black}\n      \\legend{lookup (name; all-states), GPT-4.1 mini, Haiku 4.5, Opus 5, count reader (left)}\n",
             "      \\addlegendimage{draw=black, fill=black!45, pattern=crosshatch dots, pattern color=black}\n"
             "      \\addlegendimage{only marks, mark=diamond*, mark size=2.4pt, mark options={fill=white, draw=black, line width=0.5pt}, legend image post style={mark repeat=2, mark phase=2}}\n"
             "      \\addlegendimage{only marks, mark=triangle*, mark size=2.4pt, mark options={fill=black, draw=black}, legend image post style={mark repeat=2, mark phase=2}}\n"
             "      \\legend{lookup (name; all-states), GPT-4.1 mini, Haiku 4.5, Opus 5, count reader (left), GPT-5.6 Sol (left), GPT-5.6 Luna (left)}\n"),
            (BODY,
             "legend style={at={(-0.05,-0.34)}, anchor=north, legend columns=5, font=\\scriptsize, draw=none, fill=none, column sep=5pt}]",
             "legend style={at={(-0.05,-0.34)}, anchor=north, legend columns=4, font=\\scriptsize, draw=none, fill=none, column sep=5pt}]"),
            (BODY,
             "On the state the summary names the lookup and the models are high together; on the states it only counts, every model discriminates more weakly than the count reader, and naming those states lifts every reader.}",
             "On the state the summary names the lookup and the models are high together; on the states it only counts, every model discriminates more weakly than the count reader, and naming those states lifts every reader. The two markers on the left are GPT-5.6 Sol and GPT-5.6 Luna, which ran the default summary only.}"),
        ],
        "e1": [   # E1 (Amendment 1), P-M1 HELD (r82_counterfactual/v2rcat/NUMBERS_V2RCAT.md section 9, AUX-V2RCAT-A1-*): the registration's held branch;
                  # the author's ruling 4 on REPORT_R118_A: every site names the three models given the moved-count control; L111 takes the landing map's sentence
            (BODY,
             "Opus 5, run once per item against its five-draw row, moves $-0.10$ on retraction and $-0.12$ on expiry, both intervals excluding zero.\nNames carry most of the observed signal; Opus 5 also responds to moved counts.\n",
             "Opus 5, at five draws against its five-draw row, moves $-0.10$ on retraction and $-0.13$ on expiry, both intervals excluding zero.\nNames carry most of the observed signal; of the three models given the moved-count control, only Opus 5 responds to it.\n"),
            (BODY,
             "Only Opus 5 responds to a moved count.\n",
             "Of GPT-4.1 mini, Haiku 4.5 and Opus 5, the three given the moved-count control, only Opus 5 responds.\n"),
            (BODY,   # L111 after the E5 landing ("five models"); the landing map's candidate sentence
             "For the five models tested on the summary alone, the attribute names carry most of the signal, and no count intervention establishes consistent count use (Section~\\ref{sec:counterfactual}).",
             "The summary carries each label twice, as a name or as a count; the models read the names and barely read the counts, and the states they miss when counted they detect once named (Section~\\ref{sec:counterfactual})."),
            (BODY,   # L122, the bullet: the count interventions name the three models that received them
             "The count interventions do not establish count use for retracted and expired content.",
             "The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content."),
            (APPX,
             "Opus 5 ($k=1$ vs.\\ $k=5$) & whole set & $0.8405$ & $0.8049$ & $-0.0357$ $[-0.0543,-0.0206]$; $[-0.0617,-0.0169]$ \\\\\n"
             "Opus 5 & retraction ($30$ pairs) & $0.5872$ & $0.4861$ & $-0.1011$ $[-0.1700,-0.0435]$; $[-0.2145,-0.0211]$ \\\\\n"
             "Opus 5 & expiry ($30$ pairs) & $0.6150$ & $0.4914$ & $-0.1236$ $[-0.2165,-0.0374]$; $[-0.2598,-0.0118]$ \\\\\n",
             "%% R118 (E1, Amendment 1; AUX-V2RCAT-A1-OP5-K5): Opus 5 at five draws is the row; the recorded draw-1 row kept beside it (the registration's held branch).\n"
             "Opus 5 ($k=5$) & whole set & $0.8405$ & $0.8075$ & $-0.0330$ $[-0.0496,-0.0196]$; $[-0.0592,-0.0142]$ \\\\\n"
             "Opus 5 & retraction ($30$ pairs) & $0.5872$ & $0.4869$ & $-0.1003$ $[-0.1612,-0.0472]$; $[-0.2079,-0.0317]$ \\\\\n"
             "Opus 5 & expiry ($30$ pairs) & $0.6150$ & $0.4869$ & $-0.1281$ $[-0.2127,-0.0517]$; $[-0.2651,-0.0095]$ \\\\\n"
             "Opus 5, draw 1 ($k=1$) & whole set & $0.8405$ & $0.8049$ & $-0.0357$ $[-0.0543,-0.0206]$; $[-0.0617,-0.0169]$ \\\\\n"
             "Opus 5, draw 1 & retraction ($30$ pairs) & $0.5872$ & $0.4861$ & $-0.1011$ $[-0.1700,-0.0435]$; $[-0.2145,-0.0211]$ \\\\\n"
             "Opus 5, draw 1 & expiry ($30$ pairs) & $0.6150$ & $0.4914$ & $-0.1236$ $[-0.2165,-0.0374]$; $[-0.2598,-0.0118]$ \\\\\n"),
            (APPX,
             "with the paired difference and both intervals, beside the reference readers on the same text. Descriptive; no prediction was registered.}",
             "with the paired difference and both intervals, beside the reference readers on the same text. Descriptive; no prediction was registered on the first three readers' rows. Opus 5's five-draw row was registered before its four added draws (Amendment 1), which predicted that the one-draw movement on retraction and expiry would replicate at five draws with both intervals excluding zero; it did.}"),
        ],
        "read1": [   # the author's read of paper_v21.pdf (fc42d2d), 19 September: five items and the Limitations payers of the landing map
            (BODY,   # 1. contribution 3: "is not exceeded by two of five"; the last sentence names the three models given the count interventions
             "the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions, run on GPT-4.1 mini, Haiku 4.5 and Opus 5, do not establish count use for retracted and expired content.",
             "the name lookup is not exceeded by two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. Of the three models given the count interventions, only Opus 5 responds to a moved count."),
            (BODY,   # 1. Section 5, first sentence, second clause
             "the models' judgment tracks the attribute names in the summary; the count interventions do not establish that it tracks the counts.",
             "the models' judgment tracks the attribute names in the summary; of the three models given the count interventions, only Opus 5 tracks the counts."),
            (BODY,   # 2. the Section 4 roster (two sentences for rule L) and the harness sentence; the disclosure paragraph sits in Appendix A (app:laddertable)
             "GPT-4.1 mini ran the main study at one call per question, Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls, and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}).\nThe GPT-5.6 cross-model rows are harness rows (Appendix~\\ref{app:laddertable}).",
             "GPT-4.1 mini ran the main study at one call per question, and Opus 5, Haiku 4.5 and GPT-5.6 Luna ran every population at five calls (Table~\\ref{tab:setup}).\nGPT-5.6 Sol ran the cross-model set and, through the raw API, the counterfactual set; Kimi K3 ran the cross-model set only.\nThe GPT-5.6 cross-model rows are harness rows; their counterfactual rows are raw-API (Appendix~\\ref{app:laddertable})."),
            (BODY,   # 3. the range over the five models on retraction and expiry (AUX-CF2-PERSTATE; AUX-CF2-OAI-SOL-V2, -LUNA-V2): 0.5283 (GPT-4.1 mini, retraction) to 0.6403 (GPT-5.6 Sol, expiry)
             "the category-aware count reader at $0.73$ and $0.78$, where every model scores $0.53$ to $0.62$.",
             "the category-aware count reader at $0.73$ and $0.78$, where every model scores $0.53$ to $0.64$."),
            (BODY,   # 4. the privileged reader sentence says what it reads
             "A count reader given the question's category, a privileged reader computed post hoc, scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual}).",
             "A reader given the question's category that reads the share of its entries no longer active, superseded included (privileged, post hoc), scores $0.85$ on the whole set from the count table alone (Appendix~\\ref{app:counterfactual})."),
            (BODY,   # 5. the E2 sentence names the two readers
             "Removing every count from the summary leaves both readers within tolerance of the intact summary,",
             "Removing every count from the summary leaves GPT-4.1 mini and Haiku 4.5 within tolerance of the intact summary,"),
            (BODY,   # payer: the "mean of 99 names" sentence to C.2 (the landing map); the paraphrase sentence stays
             "Beyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names. ",
             ""),
            (APPX,
             "so a longer list of the store's own names is untested.\n",
             "so a longer list of the store's own names is untested.\n%% R118 (the author's read of 19 September; the landing map's Limitations payer): the Limitations sentence moved here whole.\nBeyond the store's own name pool, a mean of $99$ names, the lookup is tested only with other personas' names.\n"),
            (BODY,   # the Limitations opening from the landing map (the two sentences are not frozen fragments: no CLAIMS quote, registration, U block or slogan pin carries them)
             "The primary evidence comes from synthetic stores and FR-Bank, the benchmark's lifecycle backend \\citep{fr}.\nThe added Graphiti evaluation extends implementation coverage using the same synthetic personas.\n",
             "Lifecycle ground truth (which record replaced which, what was never stored) is unobservable in real user data, so the stores are synthetic.\nThe counterfactual test scores ground-truth summaries and depends on no backend's write path; FR-Bank and Graphiti are scored on the same personas.\n"),
        ],
        "m_box": [   # R120 item m (proposal, costed): the builders box says retention does not override deletion or access-revocation requirements
            (BODY,
             "Keep non-active records reachable with their lifecycle tags; under FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).\n",
             "Keep non-active records reachable with their lifecycle tags where retention is permitted; retention does not override a deletion or access-revocation requirement.\nUnder FR-Bank's own tags the tagged view scored higher than under ground-truth tags (Section~\\ref{sec:routes}).\n"),
        ],
        "notation": [
            (BODY,
             "named state; counted state & a state whose attribute names the summary lists (superseded, by default); a state the summary only counts (retracted, expired) \\\\\n",
             ""),
            (BODY,
             "names, counts, reads & a summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it; a reader \\emph{reads} a state when its score separates that state's items from the rest \\\\",
             "names, counts & a summary \\emph{names} a state when it lists the attribute names in that state and \\emph{counts} it when it gives only a count of it \\\\"),
            (BODY,
             "name lookup; all-states lookup & the similarity lookup over the summary's superseded-names list, the no-model baseline every model is measured against; the same over a list that names all three non-active states \\\\",
             "name lookup & the similarity lookup over the summary's superseded-names list, the no-model baseline every model is measured against \\\\"),
            (BODY,
             "The all-states lookup scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named.",
             "The same lookup over a list naming all three non-active states scores $0.88$ on the whole set, and Haiku 4.5 gains a reliable $+0.30$ on the two counted states once they are named."),
        ],
        "pointer": [
            (BODY,
             "and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}).",
             "and GPT-5.6 Sol and Kimi K3 ran the cross-model set only (Table~\\ref{tab:setup}).\nThe GPT-5.6 cross-model rows are harness rows (Appendix~\\ref{app:laddertable})."),
        ],
        "e5": [
            # ruling 3 of 19 September: directions (i) and (ii), gap form, models named; no model reliably exceeds the lookup on supersession
            # (reviews/r117/results/sup_margins.json: mini -0.0915 reliable below, Haiku -0.0347, Opus +0.0102, Sol +0.0161, Luna +0.0204, intervals including zero)
            (ABS,
             "With one question asked of three store versions, GPT-4.1 mini and Haiku 4.5 do not exceed a similarity lookup over the list, and Opus 5 exceeds it by $0.07$.",
             "With one question asked of three store versions, no model reliably exceeds a similarity lookup over the list on the state the list names. On the whole set GPT-4.1 mini and Haiku 4.5 do not exceed that lookup, and Opus 5, GPT-5.6 Sol and GPT-5.6 Luna do, by $0.07$ to $0.08$, a margin that comes from the states the summary only counts."),
            (BODY,
             "For the three models tested on the summary alone, the attribute names carry most of the signal,",
             "For the five models tested on the summary alone, the attribute names carry most of the signal,"),
            (BODY,
             "the name lookup matches two of three models, and the count interventions do not establish count use for retracted and expired content.",
             "the name lookup matches two of five models, and three exceed it by $0.07$ to $0.08$ through the states the summary only counts. The count interventions do not establish count use for retracted and expired content."),
            (BODY,
             "On the counterfactual set, GPT-4.1 mini and Haiku 4.5 do not exceed the name lookup and Opus 5 exceeds it by $0.07$ (Table~\\ref{tab:cf-main}).",
             "On the counterfactual set no model reliably exceeds the name lookup on supersession, the state the list names (Appendix~\\ref{app:counterfactual}).\nThe lookup is not exceeded on the whole set by GPT-4.1 mini or Haiku 4.5, while Opus 5, GPT-5.6 Sol and GPT-5.6 Luna exceed it by $0.07$ to $0.08$, a margin on the states the summary only counts (Table~\\ref{tab:cf-main})."),
            (BODY,
             "Opus 5, all three & $0.91$ & $[0.88,0.94]$ & $0.91$ & $139/0/9$ \\\\\n",
             "Opus 5, all three & $0.91$ & $[0.88,0.94]$ & $0.91$ & $139/0/9$ \\\\\n" + block("e5_table1_rows") + "\n"),
            (BODY,
             "The models draw most of their signal from a lifecycle summary's attribute names, and a name lookup over a clean list is not exceeded by two of the three.",
             "The models draw most of their signal from a lifecycle summary's attribute names.\nOn the state a clean list names, no model reliably exceeds a name lookup over it.\nOver the whole set two of the five, GPT-4.1 mini and Haiku 4.5, do not exceed that lookup; GPT-5.6 Sol, GPT-5.6 Luna and Opus 5 are above it by $0.07$ to $0.08$, on the states the summary only counts."),
            (BODY,
             "One closed model family supplies the primary capability comparison, and two runs stopped at the budget on the full populations.",
             "Two closed vendors supply the capability comparison, no open-weights model was run on the counterfactual set, and two runs stopped at the budget on the full populations."),
            (APPX,
             "GPT-5.6 Luna & OpenAI & not run & ran & ran & ran$^{h}$ &",
             "GPT-5.6 Luna & OpenAI & ran & ran & ran & ran$^{h}$ &"),
            (APPX,
             "GPT-5.6 Sol & OpenAI & not run & stopped at the budget & stopped at the budget & ran$^{h}$ &",
             "GPT-5.6 Sol & OpenAI & ran & stopped at the budget & stopped at the budget & ran$^{h}$ &"),
            (APPX,
             "so their complete rows are on the cross-model set; three models ran on the counterfactual set.",
             "so their complete rows are on the cross-model set; five models ran on the counterfactual set."),
            (APPX,
             "Name lookup, sup.\\ only & whole & $0.7663$ & $[0.7226,0.8051]$ & $0.7663$ & $82/66/0$ & $0.5541$ & $[0.4691,0.6377]$ \\\\",
             block("e5_pnpresent_rows") + "\nName lookup, sup.\\ only & whole & $0.7663$ & $[0.7226,0.8051]$ & $0.7663$ & $82/66/0$ & $0.5541$ & $[0.4691,0.6377]$ \\\\"),
        ],
        "e5_perstate": [
            (BODY,
             "Opus 5's first draw alone keeps that margin (Appendix~\\ref{app:counterfactual}).",
             "Opus 5's first draw alone keeps that margin (Appendix~\\ref{app:counterfactual}).\nThe three margins lie on the counted states and across states; on supersession, the state the summary names, each of the three sits within $0.02$ of the lookup (Appendix~\\ref{app:counterfactual})."),
        ],
        "e2": [
            (BODY,
             "The same edit drops Haiku 4.5's reliably from $0.89$ to $0.68$, while Haiku 4.5 keeps $0.69$ on the whole population (Appendix~\\ref{app:resp}).",
             "The same edit drops Haiku 4.5's reliably from $0.89$ to $0.68$, while Haiku 4.5 keeps $0.69$ on the whole population (Appendix~\\ref{app:resp}).\nRemoving every count from the summary leaves both readers within tolerance of the intact summary, and removing the names instead puts both a reliable $0.12$ and $0.16$ below the names-only summary (Appendix~\\ref{app:counterfactual})."),
            (APPX,
             "\\label{tab:v2rcat}",
             "\\label{tab:v2rcat}"),   # anchor check only; the table goes after that table's end (AFTER_TABLE)
        ],
        "e3": [
            (BODY,
             "GPT-5.6 Luna loses $0.34$ and GPT-5.6 Sol $0.10$, every interval excluding zero$^{h}$.",
             "GPT-5.6 Luna loses $0.29$ through the raw API and GPT-5.6 Sol $0.10$$^{h}$, every interval excluding zero.\nThe loss survives omitting or rewording the marker on Mem0, and for GPT-5.6 Luna it appears under every rendering, $0.27$ to $0.34$, so the marker's wording is not the cause (Appendix~\\ref{app:inversion})."),
            (APPX,
             "Which line of the summary produces the compression is the question the ablations above leave open.\n",
             "Which line of the summary produces the compression is the question the ablations above leave open; the marker's wording is not it (Table~\\ref{tab:marker}).\n"),
            (APPX,
             "\\label{tab:dist}",
             "\\label{tab:dist}"),
        ],
        "e3_u5": [
            (BODY,
             # the author's ruling 3 on REPORT_R118_A: the inversion claim kept; omitting or rewording the marker does not remove the Mem0 loss; Luna's raw-API range; no cause beyond the marker's wording (AUX-MARKER-*)
             "The structureless-store inversion is measured across scales, but its below-chance mechanism remains unresolved.",
             "The structureless-store inversion is measured across scales, and neither omitting the marker nor rewording it removes the Mem0 loss; GPT-5.6 Luna, through the raw API, loses $0.27$ to $0.34$ under every rendering.\nThe marker's wording is therefore not the cause, and the below-chance mechanism remains unresolved."),
        ],
        "e4": [
            (BODY,
             "Haiku~4.5's residual comes from tagged lines, mostly a mention of the tagged content beyond the answer's first sentence (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).",
             "Haiku~4.5's residual comes from tagged lines, mostly a mention of the tagged content beyond the answer's first sentence (Table~\\ref{tab:ds-a5}, Appendix~\\ref{app:resp}).\nA view-only rule propagating a line's tag to same-attribute lines that repeat it at the census threshold changes $1$ of $452$ views: $187$ of the $272$ stale lines sit under a different attribute key from their tagged twin (Appendix~\\ref{app:resp})."),
            (APPX,
             "\\label{tab:ds-a7}",
             "\\label{tab:ds-a7}"),
        ],
        "payer_c2": [   # the landing map's E2 payer (the first-draw sentence to C.2) and the post-hoc sentence beside it
            (BODY,
             "\nOpus 5's first draw alone keeps that margin (Appendix~\\ref{app:counterfactual}).\n",
             "\n"),
            (BODY,
             "\nScored post hoc against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal.\n",
             "\n"),
            (APPX,
             "\\subsection{Store-counterfactual set}\\label{app:counterfactual}\n",
             "\\subsection{Store-counterfactual set}\\label{app:counterfactual}\n\n%% R118: two Section 5 sentences moved here whole under the landing map (the payer for the R117 landings); their numbers unchanged (AUX-R104-MARGIN; reviews/NUMBERS_WP.md section 8).\nOpus 5's first draw alone keeps its margin over the name lookup on the whole set.\nScored post hoc against the PRESENT versions alone, which also hold relevant content, every reader moves by at most $0.03$ from its whole-set value, so the comparison stands where coverage is equal.\n"),
        ],
        "newpage_ai": [
            (BODY,
             "\\label{main-text-end}\n\n\\subsection*{AI use statement}",
             "\\label{main-text-end}\n\n\\newpage\n\\subsection*{AI use statement}"),
        ],
        "payer_e4": [
            (BODY,
             "\nTwo further results are in Appendix~\\ref{app:resp}.\nA header naming the persona and the date raises in-view correct answers reliably for both answerers.\n% AUX-DS-AUDIT-RANK, AUX-DS-AUDIT-IDENTITY, AUX-DS-A4-STAGE2-*\nA composite over all three jobs rises under the model rule by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}).\n",
             "\n"),
        ],
    }


# the appendix tables that go after a named table's end: (group, label of the table they follow, block)
AFTER_TABLE = {"e2": ("tab:v2rcat", "e2"), "e3": ("tab:dist", "e3"), "e4": ("tab:ds-a7", "e4")}
PAYER_TEXT = ("\\noindent A header naming the persona and the date raises in-view correct answers reliably for both answerers.\n"
              "% AUX-DS-AUDIT-RANK, AUX-DS-AUDIT-IDENTITY, AUX-DS-A4-STAGE2-* (moved whole from Section 9 under the R117 landing map; the pointer sentence \"Two further results are in Appendix E.10\" dropped as self-referential here)\n"
              "A composite over all three jobs rises under the model rule by a reliable $+0.03$ for GPT-4.1 mini and stays level for Haiku 4.5 (Table~\\ref{tab:ds-a7}).\n")


def insert_after_table(text, label, addition):
    i = text.index("\\label{" + label + "}")
    j = text.index("\\end{table}", i) + len("\\end{table}")
    if addition in text:
        return text
    return text[:j] + "\n\n" + addition + text[j:]


def n_old_del(t, old):
    """A deletion (NEW of one character or less): 'applied' means OLD is gone."""
    return t.count(old) == 1


def apply(edits, check):
    texts = {}
    for p, old, new in edits:
        t = texts.get(p)
        if t is None:
            raw = p.read_bytes(); assert b"\r\n" not in raw, f"{p}: CRLF source, refusing"
            t = raw.decode("utf-8")
        if old == new:
            assert t.count(old) == 1, ("anchor", old[:60]); texts[p] = t; continue
        n_old, n_new = t.count(old), (t.count(new) if len(new) > 1 else (0 if n_old_del(t, old) else 1))
        if n_new == 1:
            print(f"  already applied : {p.name}: {new[:70]!r}")
        elif n_new == 0 and n_old == 1:
            print(f"  {'would apply' if check else 'applied'}     : {p.name}: {old[:70]!r}")
            if not check:
                t = t.replace(old, new)
        else:
            raise SystemExit(f"ANCHOR NOT UNIQUE ({n_old} old, {n_new} new) in {p}: {old[:90]!r}")
        texts[p] = t
    return texts


def main():
    check = "--check" in sys.argv
    src = pathlib.Path(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else DEFAULT_SRC
    G = groups(src)
    names = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else ["pointer"]
    edits = [e for g in names for e in G[g]]
    texts = apply(edits, check)
    appx = src / "appendix_v21.tex"
    if not check:
        for g in names:
            if g in AFTER_TABLE:
                label, blk = AFTER_TABLE[g]
                t = texts.get(appx) or appx.read_text(encoding="utf-8")
                texts[appx] = insert_after_table(t, label, block(blk))
            if g == "payer_e4":
                t = texts.get(appx) or appx.read_text(encoding="utf-8")
                texts[appx] = insert_after_table(t, "tab:ds-a7", PAYER_TEXT)
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("r118_apply:", "check only" if check else "written", f"({len(edits)} edits, groups {names}, src {src})")


if __name__ == "__main__":
    main()
