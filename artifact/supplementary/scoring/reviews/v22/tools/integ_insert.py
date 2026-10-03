# -*- coding: utf-8 -*-
"""integ_insert.py -- the integration pass of 2026-09-16 (program R112): the appendix insertions (asserted anchors, idempotent).
(1) C.2: the PN-versus-PRESENT paragraph and Table tab:pnpresent (from reviews/v19/src/posthoc_tables_v19.tex, generated) and the
    intent note (B4), before the score-resolution paragraph;
(2) E.11: the forty-persona Graphiti ingestion in the spend sentence;
(3) E.12 (new): the provenance table of the headline numbers (review-2 F5);
(4) G.4 (new): the fourth backend at forty personas (r85_graphiti/NUMBERS_R85.md AUX-R85-G10-*; D-R85-16).
Run from the repository root: python reviews/v19/tools/integ_insert.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / "reviews" / "v19" / "src"
X = SRC / "appendix_v19.tex"
TAB = (SRC / "posthoc_tables_v19.tex").read_text(encoding="utf-8")

C2 = r"""%% R112 (2026-09-16), post hoc B1 to B4, specified before recomputation (reviews/integration/POSTHOC_SPEC_R112.md, sha256 ae2600fc; reviews/NUMBERS_WP.md sections 8 and 9;
%% reviews/v19/tools/posthoc_b_pnpresent.py, posthoc_b4_intent.py; reviews/v19/results/posthoc_b.json, posthoc_b4.json). No model call.
\paragraph{PN versus PRESENT, and the ordering within triples (post hoc, specified before recomputation).}
The pooled obligation AUROC of Table~\ref{tab:cf-main} scores the \pn{} versions against both other versions, so it mixes two distinctions: \pn{} against \present{}, where both versions hold relevant content, and \pn{} against \absent{}.
A reader that only knows whether the store covers the question scores $1$ on \pn{} and \present{} and $0$ on \absent{}, which gives $0.75$ pooled on this set and $0.5000$ on the \pn{}-versus-\present{} comparison, because it ties every triple.
Table~\ref{tab:pnpresent} separates the two for every reader, summary and state, with the pooled value equal to the mean of the two (asserted to four decimals, the negative groups being equal in size), and counts, per triple, whether the reader scores the \pn{} version above, equal to, or below the \present{} version.
The largest move from the pooled value on the whole set, any reader, is $0.0230$, so the model-versus-lookup comparison of Section~\ref{sec:counterfactual} is the same on the harder comparison: the name lookup reads $0.7663$, GPT-4.1 mini $0.7056$, Haiku 4.5 $0.7493$ and Opus 5 $0.8370$.
The strict-win fraction counts ties as failures and is not a tie-adjusted ranking accuracy; GPT-4.1 mini's single call returns coarse probabilities, so its tie count is large ($57$ of $148$ triples on the whole set), and the interval to read is the persona-grouped one, since triples share personas.
Where the summary only counts a state, the two lookups tie every retraction and expiry triple under the superseded-only summary (their lists do not differ), the count readers win most of them, and the models split between ties and small numbers of wins and losses; naming the states turns most of those ties into wins for every reader.
The expected outcomes written before the run held for the name lookup and GPT-4.1 mini (supersession above $0.85$ and $0.70$; retraction and expiry within tolerance of $0.50$ under the superseded-only summary) and for the all-states lookup (above $0.70$ on both counted states); they did not hold for Opus 5, which reads $0.5689$ on retraction and $0.6128$ on expiry against the \present{} versions, nor for Haiku 4.5 on expiry ($0.5544$), nor for the count readers, which the pooled result had already shown to separate the counted states.

""" + TAB + r"""
The test the review asked for on intent, the same store history judged under two intents, cannot be built from the recorded rows: each question carries one constructed intent and the \textsc{change} intent is never \pn{}, so any comparison across intents would vary intent with the label.
Two things can be read instead (post hoc, specified before recomputation).
An intent-aware name lookup, whose score is set to zero on the $105$ \textsc{change}-intent questions of the full obligation set (superseded content is licensed under that intent), reads $0.7957$ against the plain lookup's $0.7484$, $+0.0473$ with intervals $[+0.0331,+0.0654]$ and $[+0.0284,+0.0689]$; the all-states lookup moves from $0.7806$ to $0.8255$ under the same rule plus a zero on the $9$ past-intent questions whose best match is an expired name.
The items on which intent alone decides the label, \textsc{change}-intent licensed questions whose own slot holds a superseded record, number $4$ of the $45$ on the full obligation set, below the floor of five the specification set for a reading, so no monitor comparison is printed on them.

"""

E11_OLD = "Haiku 4.5 under the store's own metadata $9.36$ of $12$; the increment moved within the triple $3.23$ of $4$."
E11_NEW = "Haiku 4.5 under the store's own metadata $9.36$ of $12$; the increment moved within the triple $3.23$ of $4$; the forty-persona Graphiti ingestion $11.88$ of a $13.22$ stop, twelve aborted partial runs included (Appendix~\\ref{app:posthoc-graphiti})."

E12 = r"""
%% R112 (2026-09-16), review-2 F5: the provenance table, one row per headline number of the abstract and Sections 5 to 9; every cell names a source the artifact carries.
\subsection{Provenance of the headline numbers}\label{app:provenance}

Each headline number rests on a population, a label source, a record alignment, a tag source and an evaluator, and they are not the same across the paper.
Table~\ref{tab:provenance} lists them in one place, with the validation status of each evaluator, so that a number is never read with a stronger warrant than its row gives it.

\begin{table}[H]
\caption{Provenance of the headline numbers: the population, the label source, how records are aligned to labels, the tag source the reader saw, the evaluator, and its validation status. ``Manifest'' is the human-written persona manifest; ``join'' is the token-overlap alignment of manifest events to stored records at the $0.80$ bar; ``hand-verified'' means every \pn{} label was checked by hand from its constituent judgments.}
\label{tab:provenance}
\centering
\scriptsize
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{0.95}
\begin{tabular}{@{}p{0.19\linewidth}p{0.13\linewidth}p{0.14\linewidth}p{0.13\linewidth}p{0.13\linewidth}p{0.12\linewidth}p{0.12\linewidth}@{}}
\toprule
Number (where) & Population & Label source & Record alignment & Tag source & Evaluator & Validation \\
\midrule
Counterfactual NOK AUROC, lookup $0.77$ and models $0.72$ to $0.84$ (Section~\ref{sec:counterfactual}, Table~\ref{tab:cf-main}) & $444$ items, $148$ triples & manifest; \pn{} labels hand-verified; question fixed across versions & not needed: versions built from the manifest & ground-truth summary & AUROC, persona-grouped bootstrap & registered predictions held; PN-vs-PRESENT decomposition post hoc \\
Own-name ablation, $0.86$ to $0.53$ (Section~\ref{sec:counterfactual}) & $661$, $63$ supersession obligations & manifest; hand-verified & join, for the names removed & ground-truth summary, edited & AUROC, paired bootstrap & registered prediction held \\
Moved-count control (Section~\ref{sec:counterfactual}) & $60$ counted-state triples & manifest & not needed & ground-truth summary, one count moved & AUROC, paired bootstrap; band reading & descriptive; fired as neither \\
Tagged view $0.69$, $0.83$, $0.81$ (Section~\ref{sec:routes}, Table~\ref{tab:routes}) & $661$, $104$ obligations & manifest; hand-verified & join (ground-truth tags: $82$ of $104$ forbidding records marked); the store's own tags for the $0.81$ row & ground-truth tags; FR-Bank's own tags & AUROC, paired bootstrap & L2 predictions failed; the own-tags row descriptive \\
Census of the stores (Section~\ref{sec:backends}, Table~\ref{tab:census}) & every entry of each store; forty personas & manifest & join at $0.80$ (FR-Bank, Graphiti); the store's own fields (Mem0, A-MEM) & the store's own marks & counts & no sampling interval; Graphiti's population restricted to FULL-variant obligations (Appendix~\ref{app:posthoc-graphiti}) \\
Store-written summary, retention $72\%$ (Section~\ref{sec:backends}, Table~\ref{tab:levels}) & $661$ & manifest; hand-verified & join, for the summary; the store's fields for the store-written one & FR-Bank's own metadata & AUROC; ratio of paired differences & descriptive; the sixty-percent line conventional \\
Coverage FOK, easy tier $0.78$ (Section~\ref{sec:populations}) & $354$, $243$ positives & manifest; presence control & join & ground-truth summary & AUROC, paired bootstrap & the margin over the whole-map lookup not reliable (post hoc, Appendix~\ref{app:baselines}) \\
Downstream reach, flagged stale answers, retagging (Section~\ref{sec:downstream}, Table~\ref{tab:ds-body}) & $104$ obligations, $174$ licensed; $89$ scorable & manifest; hand-verified & join; the audit's read of the views & ground-truth tags in the view; reference-assisted retags & token detector at $0.50$; one reader's classification of flags & the two-annotator validation registered, not labelled; the retagging diagnostic, not a deployable repair \\
\bottomrule
\end{tabular}
\end{table}
"""

G4 = r"""
%% R112 (2026-09-16): the forty-persona Graphiti census (registrations/ADDENDUM_R85_GRAPHITI_AMENDMENT_1.md frozen 43132a3; r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST, -CENSUS, -REPEAT, -CENSUS-FORBIDDING, -CENSUS-FORBIDDING-FULL, -PRINTED; DEVIATIONS_R85.md D-R85-12, -15, -16). No obligation judgment is scored on this backend.
\subsection{The fourth backend at forty personas}\label{app:posthoc-graphiti}

The three-persona trial of Appendix~\ref{app:census} was extended to every persona after the main results were known, under predictions written before the ingestion, and the reading of its population was fixed before any number here was printed.
The unmodified release (\texttt{graphiti-core} 0.28.1) ingested all forty personas at one episode per session: $1{,}365$ episodes rendered from FR-Bank's persona banks with every lifecycle field, status marker and supersession pointer removed, so the graph holds the same conversations FR-Bank holds and nothing of FR-Bank's own marks, and the ground truth is the persona manifest as everywhere in this paper.
The result is one graph per persona, $7{,}096$ entity nodes and $9{,}189$ edges; under the mapping of Appendix~\ref{app:census} (an invalidated edge with a successor is superseded, invalidated without one is expired, retraction inexpressible) $8{,}382$ edges are active, $130$ superseded and $677$ expired; $784$ carry no validity time and $72$ are dated after the persona's clock.
Every graph is the full store of its persona: the store variants of the main study, with categories or the successor removed, do not exist on it, so a Graphiti reading is valid only on the obligations of the full store, and the main text reports that population; the reading over all $104$ obligation rows, which repeats the same forbidding records on the same graph for the $57$ variant rows, prints below beside it because the prediction was written on it.

\begin{table}[H]
\caption{The forty-persona Graphiti census against the manifests. Recall is the share of ground-truth events, or forbidding records, on which some Graphiti edge asserting the old content carries a non-active state under the mapping above; stale-active means such an edge exists and every one is active; extraction miss means no edge asserts the content at the $0.80$ overlap bar. Precision is over all $807$ non-active edges of the forty graphs and is unchanged by the population. Retraction is inexpressible on this backend, so the eight obligations the ground truth marks retracted enter no recall.}
\label{tab:graphiti-g10}
\centering
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}p{0.34\linewidth}rrrrll@{}}
\toprule
Census & $n$ & recovered & stale-active & extraction miss & recall (bands $0.50$ / $0.75$) & precision \\
\midrule
Manifest supersession events & $109$ & $20$ & $12$ & $77$ & $0.1835$ ($57$ / $35$ of $109$) & $35$ of $807$, $0.0434$ \\
Forbidding records, obligations of the full store (the main-text reading) & $34$ of $47$ & $13$ & $10$ & $11$ & $0.3824$ & $54$ of $807$, $0.0669$ \\
\quad the same over distinct forbidding-record sets & $39$ of $56$ & $16$ & $11$ & $12$ & $0.4103$ & the same \\
Forbidding records, all $104$ obligation rows (the prediction's population) & $74$ of $104$ & $30$ & $21$ & $23$ & $0.4054$ ($48$ / $36$ of $74$); $0.3846$ over the $78$ by attack vector & the same \\
\bottomrule
\end{tabular}
\end{table}

By state on the full-store obligations, superseded preferences are recovered in $7$ of $16$, multi-version facts in $5$ of $11$ and expired arrangements in $1$ of $7$; over all $104$ rows the same three read $0.47$, $0.44$ and $0.09$, so expiry is the weak state on this backend under both readings.
The failure mode is extraction: of the $565$ manifest facts the graph asserts $134$ at the overlap bar, $77$ of the $109$ supersession events have no edge asserting the old value at all, and the user is split across two to four entity nodes in every persona, so a later fact about the same slot does not meet the earlier one.
The three trial personas, re-ingested into the forty-persona graphs, give the same recall on both graphs (elena $0.33$, tom $0.00$, yoli $0.25$) at $237$, $213$ and $224$ edges against the trial's $242$, $221$ and $222$.

The prediction fixed before the ingestion put the recall on the forbidding records at or below $0.25$ and the precision at or below $0.10$, the direction of the three-persona trial; the precision held and the recall did not, under the prediction's population and under both re-aggregations above.
Its outcome text, quoted verbatim with the artifact's names (Appendix~\ref{app:glossary}), reads: ``Over the forty personas Graphiti reaches 30 of the 74 forbidding records (the join's count; 30 of the attack-vector 78), above the registered quarter, at precision 0.0669.''
What the census establishes is therefore narrower than the trial suggested: some of the records the agent must not use are recovered by this backend's own invalidation, most are not, and almost every non-active mark it writes falls on a record the ground truth calls active.
The summary route and the tag route registered for this backend, and the answer-stage comparison drafted after them, have not been run; no obligation judgment is scored on Graphiti in this paper, and no row for those routes prints here.
"""


def insert_before(t, anchor, block):
    n = t.count(anchor)
    assert n == 1, f"anchor {anchor[:60]!r} found {n} times"
    return t.replace(anchor, block + anchor)


def main():
    t = X.read_text(encoding="utf-8")
    if "label{app:posthoc-graphiti}" in t and "label{tab:pnpresent}" in t and "label{app:provenance}" in t:
        print("already inserted"); return
    t = insert_before(t, "\\paragraph{Score resolution.}", C2)
    assert t.count(E11_OLD) == 1
    t = t.replace(E11_OLD, E11_NEW)
    t = insert_before(t, "\\section{Registration record}\\label{app:registration}", E12 + "\n")
    t = t.replace("\\end{document}", G4 + "\n\\end{document}")
    X.write_text(t, encoding="utf-8", newline="\n")
    print("inserted C.2 paragraph + tab:pnpresent, E.11 spend, E.12 provenance, G.4 Graphiti")


if __name__ == "__main__":
    main()
