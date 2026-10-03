# -*- coding: utf-8 -*-
"""claims_r110_pass2.py -- write the Pass 2 entries of the R110 AUTHORIZATION BLOCK (CC_PASS_v18; paper_v18.tex against the v17 base).

Reads the changed frozen strings that frozen_list.py reports (the Q CLAIMS quotes, the U-blocks, the registration fragments), pairs each
with its disposition in v18, and appends the entries to reviews/v18/claims_r110_block.md (the copy) and to the R110 block in
iclr2027_monitoring_submission/CLAIMS.md (the authority frozen_diff reads). Every Before is quoted in full (or, where the string
carries a double quote of its own, by the prefix before that quote, which frozen_diff matches as a substring); every After names the
v18 text or the deletion. Usage: python reviews/v18/tools/claims_r110_pass2.py <base tree>
"""
from __future__ import annotations

import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
COPY = ROOT / "reviews" / "v18" / "claims_r110_block.md"
MARK = "<!-- R110 PASS 2 ENTRIES -->"

# disposition by a distinctive prefix of the normalized string; "deleted" means nothing stands in its place
DISP = {
    "Knowing the Store: What a Memory Backend": "count: the title now also appears in the running head of the ICLR style (1 to 2); unchanged text.",
    "always-reasoning configuration": "count 1 to 2: the phrase now appears in Table 1's run-coverage note and the appendix; unchanged text.",
    "with questions grouped by user profile": "count 6 to 7: the phrase is used once more in Appendix E.10's retagging sentence; unchanged text.",
    "not expressible by this backend": "count 9 to 8: Section 7's marker sentence moved to Appendix E.7 with the structureless-store ablations (the spine's one-paragraph rule); the appendix mentions stand.",
    "(Appendix \\ref{app:registration})": "count 1 to 4: the pointer is used in Sections 1, 3, 4 and 8 of v18.",
    "Appendix \\ref{app:registration} lists every prediction fixed before data collection": "Section 4 now ends: \"Every preregistered text, prediction and outcome is in Appendix~\\ref{app:registration}.\" (P3: no bookkeeping phrases in the body).",
    "global counts may make the store look better covered": "deleted from Section 7 (the mechanism hunt is sent to Appendix E.7 in one sentence; the two hypotheses stand there).",
    "disagreement between the summary and the retrieved view may compress": "deleted from Section 7 (the same move).",
    "the matcher, in the preregistered texts": "deleted: the lookup is defined once in Section 4 (\"The similarity lookup scores each question by its maximum cosine similarity ...\"); the alias lives in the glossary (P1).",
    "on the conflict questions of a recent benchmark": "kept in Section 1 in the same words after a semicolon; the sentence it joins was reworded.",
    "We measure both judgments on stores we built, so that every label is exact.": "Section 1: \"We measure both judgments on stores we built, so that every label is exact, across three memory backends and language models from three vendors.\"",
    "Coverage is the judgment on which the model earns its call": "Section 8: \"The coverage margin lives on ordinary records, and on the hard tier the coverage result is the obligation result restated.\" (A5_EDITS.md item 3).",
    "such an item is expected to shrink measured gains": "Section 4: \"... a mislabeled \\absent{} item is unlikely ($5.2\\%$ at the observed base rate; Appendix~\\ref{app:construction}) and would shrink measured gains rather than inflate them.\"",
    "Of the 58 predictions fixed before data collection, 16 did not hold": "Section 1: \"Of the $58$ predictions preregistered before data collection, $16$ came out otherwise (Appendix~\\ref{app:registration}).\" (P3: \"held\" is a barred outcome word).",
    "Its name map carries only superseded content": "Section 3: \"The name map carries only superseded content, so an entry that expires or is retracted reaches the summary as a count and is never named.\"",
    "Every paired obligation gain excludes zero where the blind score varies": "Section 8: the same clause opens a longer sentence (\"..., and on the cross-model set the five models with a varying blind score gain $+0.15$ to $+0.45$\").",
    "No backend we tested writes the list the obligation judgment needs.": "Section 7 opens: \"No tested backend writes the list.\"",
    "A name-bearing summary rebuilt from ground truth": "Section 7: \"A name-bearing summary rebuilt from ground truth for the entries each store holds restores coverage from $0.45$ to $0.90$ on A-MEM and from $0.48$ to $0.88$ on Mem0, so the loss belongs to the summary these stores can write.\" (\"inversion\" replaced by \"loss\" in this sentence; U1 stands in the paragraph).",
    "The boundary between the named state and the counted states": "deleted with nothing in its place (rule G; READER_CLAIM.md section 2).",
    "The score ranks well and calibrates badly, with an ECE": "Section 8: \"The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\" (the ECE values stay in Appendix G).",
    "The lifted list's precision stays at 0.04": "deleted from Section 7 (the cap paragraph moved to Section 4 and Appendix E.9, which carries the precision).",
    "This section establishes a second route to the obligation.": "Section 6 opens: \"Retrieval that keeps the lifecycle tag on every returned record is a second route to the obligation, and it carries the states the list leaves uncounted.\" (P8).",
    "Naming those states in the all-states summary lifts the lookup to 0.88": "Section 5: \"The all-states lookup reads $0.88$ on the whole set, and Haiku 4.5's paired gain on the two counted states is $+0.30$ with both intervals excluding zero.\"",
    "On the metadata FR-Bank exposes, lookup and model both fall near chance": "Section 7: \"FR-Bank's own metadata leaves the smallest model and the lookup close to chance and costs the larger model about a quarter of its gain.\" (the R-A result: Haiku 4.5 keeps 72%).",
    "Calibration work scores confidence in an answer": "Section 2: folded into one sentence with the adaptive-retrieval and abstention lines (the trim order's first cut); the citations stand.",
    "Where a store exposes no field for a line of the summary": "moved to Appendix E.7 (the structureless-store paragraph of Section 7 is one paragraph, led by the recovery).",
    "Removing the store-wide entry count and those markers together": "moved to Appendix E.7 (the same move).",
    "For a per-item score \\sigma and budget k": "deleted: the $k$-bounded monitor is referenced nowhere in v18's body (the mask argument is stated in prose without it).",
    "Appendix \\ref{app:glossary} reproduces an abridged real one.": "Section 3 now prints the abridged real summary itself after Definition 2 (eight lines from the E.1 excerpt); E.1 keeps the fuller excerpt.",
    "FR-Bank overstates: it marks 5,968 of its 18,936 entries inactive": "Section 7: the same sentence with \"about sixtyfold\" replaced by \"about $58\\times$\" (A5_EDITS.md item 2) and \"In entries, ...\" split into its own sentence.",
    "The tagged route is measured with tags from the ground-truth join, and under the store's own tags it is unmeasured.": "Section 9: \"The tagged route is measured with tags from the ground-truth join and, descriptively, with the store's own marks.\" followed by the own-marks sentence (A5_EDITS.md item 1).",
    "The obligation judgment is bounded by what the store writes about itself": "deleted with nothing in its place (rule G); Section 10 restates the thesis in different words (the author's instruction of 2026-09-15).",
    "An inversion is an indexed score below the blind score": "deleted from Section 7 (the definition lives in the glossary); U1 stands in the paragraph.",
    "Each measures a different observable at a different time, after memory has been consulted.": "Section 2: \"Long-term stores ... and remembered-answer benchmarks ... measure what is retrieved or answered after memory has been consulted; Mem0 (\\texttt{mem0ai} 1.0.5) is the production layer evaluated here. The closest, STALE, scores whether an agent recognizes a memory it holds as no longer valid; ...\"",
    "whereas NOK's obligation comes from": "Section 2: \"NOK's obligation comes from the content's own lifecycle state and is judged before content retrieval.\" (its own sentence).",
    "both intervals excluding zero (Table \\ref{tab:cf-main})": "Section 5: \"Opus 5 reads $+0.07$ more with both intervals excluding zero, a margin its first call alone keeps (Table~\\ref{tab:cf-main}; Appendix~\\ref{app:counterfactual}).\"",
    "against a retention bar of 60% set before scoring": "deleted from Section 7: the line's provenance is stated once in Section 4 (\"The sixty-percent retention line was fixed before the main study, on 10 August 2026, ...\"); Table 4 carries the retention.",
    "an excess over 100% that is not a finding": "deleted from Section 7 (the 101.4% coverage retention sentence; the value stays in Appendix E.9 and the derived-ratio check).",
    "Appendix \\ref{app:counterfactual} holds the wording fixed before scoring": "deleted (P3: no registration bookkeeping in the body; Appendix C.2 keeps the registered texts under \"The registered texts for this set\").",
    "Haiku 4.5's paired gain on those two states under that summary is +0.3": "Section 5: \"... Haiku 4.5's paired gain on the two counted states is $+0.30$ with both intervals excluding zero.\" (the pre-scoring pointer dropped, P3).",
    "The model scores 0.60 on that row and the lookup 0.59, inside tolerance": "Section 7: \"GPT-4.1 mini and the lookup read $0.60$ and $0.59$ capped and $0.65$ and $0.66$ lifted on the obligation judgment, while Haiku 4.5 reads $0.71$ capped and $0.74$ lifted.\" (Table 4).",
    "The larger models score higher than the lookup on the states the summary only counts": "deleted: Section 5 and Table 1 now state the counted-state levels directly (the models at $0.53$ to $0.62$ against the category-aware reader).",
    "The two bars fixed before scoring were a reach gain of 0.50": "Appendix E.10: \"The two registered bars were a reach gain of $0.50$ ...\" (A5_EDITS.md item 8).",
    "A maintained summary escapes the bound by one route": "deleted from Section 3 (the two routes are stated in Section 1 and Figure 1; the sentence repeated them).",
    "A summary names a state when it lists the attribute names in that state.": "Definition 3 returns to vocabulary (rule G3): Section 3 reads \"A summary names a state when it lists the attribute names in that state, and counts it when it gives only a tally of it.\" and Appendix E.1 carries the glossary sentence.",
    "A summary counts a state when it gives only a tally of it.": "the same (Section 3 and Appendix E.1).",
    "A reader reads a state when its score separates that state's items from the rest.": "Section 3: \"A reader reads a state when its score separates that state's items from the rest (Appendix~\\ref{app:glossary}).\"",
    "Three failed predictions changed the reading": "deleted from Section 1 with its paragraph (the spine's Section 1 carries the four findings; Appendix F lists every outcome).",
    "The lifecycle summary of Definition \\ref{def:index} is what the indexed monitor is shown": "Section 3: \"This abridged real summary is what the indexed monitor reads: counts per category and state, and names with no values.\" (the alias \"the index\" lives in the glossary, P1).",
    "Kimi K3 completed the cross-model set in full and stopped at the budget": "Table~\\ref{tab:runs} (the run-coverage table) carries the two budget stops in the ledgers' words; the sentence is retired.",
    "NOK is measured on one lifecycle store, the only backend that retains superseded content.": "Section 9: \"The stores are synthetic because temporal ground truth is unobservable without controlled construction, and NOK is measured on one lifecycle store, the only backend that retains superseded content, whose schema is the prior store's \\citep{fr}.\"",
    "The three versions of a counted-state store have identical name maps": "deleted from Section 5; Figure 2's row two shows the fact on a real triple and its caption states it.",
    "What triggers the compression is unresolved on both stores.": "Section 7: \"What triggers the compression is unresolved, and the ablations that narrowed it are in Appendix~\\ref{app:inversion}.\"",
    "Two hypotheses remain: global counts may make the store look better covered": "moved to Appendix E.7 (the mechanism hunt in one body sentence).",
    "On the two structureless stores the summary hurts coverage at every scale tested": "Section 7 opens the paragraph on the recovery: \"On the two structureless stores a summary that names what they hold restores coverage, and the summary they can write loses it at every scale.\"",
    "Under the one lifecycle store's own metadata, both readers fall near chance.": "deleted (rule G; the R-A result contradicts \"both\"): Section 10 reads \"The one lifecycle store's own metadata is enough for the larger model wherever it still writes the name, and not enough for the smallest model or the lookup anywhere.\"",
    "Agents with persistent memory decide, before retrieving anything": "the abstract is replaced whole by the author's abstract v7 (reviews/v18/src/abstract_v18.tex; CLAIMS.md rows S1 to S9 of reviews/v18/CLAIMS.md); its first sentence is unchanged and the rest is the author's text.",
    "The 5% retrieval pass rate cited for its mask was measured on the 40 retraction questions": "Section 4: \"The $5\\%$ pass rate cited for its mask was measured on the prior store's own $40$ retraction questions with the mask in place.\"",
    "Every model except it was scored by averaging five calls per question": "Section 4: \"GPT-4.1 mini is scored from one call at temperature $0$ and every other model from five calls averaged (Table~\\ref{tab:runs}).\" with the resolution note (A3) beside it.",
    "The list-length check pads the 661 summaries' superseded-names lists": "Section 5: \"Padding those lists with correct names moves the embedding lookup from $0.75$ to $0.73$, $0.72$ and $0.67$ at $15$, $30$ and $60$ names.\" preceded by \"The truthful summary's superseded-names list averages $1.75$ names on the full obligation set.\" (P2: the population by name).",
    "The lexical lookup stays flat, and GPT-4.1 mini degrades first at 15 names": "moved to Appendix C.2 (the trim under the page gate; the values stand in Table 16).",
    "The counted-state evidence rests on 30 retraction and 44 expiry pairs": "Section 5: \"The counted-state evidence rests on $30$ retraction and $44$ expiry pairs, and on the full obligation set ($661$ questions) the counted-state rows give only a direction (Section~\\ref{sec:populations}).\" (P2).",
    "An after-the-fact decomposition puts most of the lookup's loss on missing names": "deleted from Section 7 (the trim under the page gate; Appendix G.3 carries the decomposition).",
    "the author's label-transfer read is in progress": "Appendix C.2: \"the author's label-transfer read had not been made at this build, so no paraphrase row is printed\" (P12).",
    "The padding check, the expiry extension and the two later downstream amendments have run": "Table 40's caption: \"Every one has run except the paraphrase check, which waits on the author's read.\"",
    "seven descriptive registrations": "Table 40's caption: \"twelve descriptive registrations\" (the five rows added: Haiku 4.5 under the store's own metadata, the increment moved within the triple, DS Amendments 5 to 7).",
    "Reach is not use, and a forensic audit of the answer stage shows where the use comes from.": "Section 8 is written as the chain reach, tags respected, the duplicate fault, the repair, depth, the composite (OUTLINE.md section 8); the sentence is retired.",
    "Both readings were fixed before scoring": "Appendix E.7: \"Both readings were registered, ...\" (A5_EDITS.md item 8).",
    "A later descriptive draw extends the expiry pairs to 44": "Section 9: \"The counted-state groups are small: $30$ retraction and $30$ expiry pairs on the counterfactual set, $44$ expiry with the extension, ...\"",
    "and the outcome sentence written before scoring for the neutral-slice prediction": "Appendix E.10: \"and the registered outcome sentence for the neutral-slice prediction is in its Section S.9\" (A5_EDITS.md item 8).",
    "The answer-stage detector is a token-overlap rule whose limits": "Section 8: \"the stale and correct counts are a token detector's, read by hand where flagged, with its limits in Appendix~\\ref{app:resp}.\" (P12: no \"pending\").",
    "That difference of +0.13 has both intervals excluding zero, and against the summary alone": "Section 6: \"With FR-Bank's own marks in place of the join, the view reads the obligation at $0.81$ against $0.69$ for the smallest model, a difference of $+0.13$ with both intervals excluding zero.\" (the +0.08 against the summary stays in Appendix E.10).",
    ", so the gain isolates the summary.": "Section 4 (the author's trim order of 2026-09-15): \"..., and the two prompts differ only in whether the summary precedes the question, so the gain isolates the summary (Appendix~\ref{app:construction}).\" (the pointer moved inside the sentence).",
    "the automatic intent classifier that proposed the candidates": "deleted from Section 4 under its 500-word ceiling (the author's trim order of 2026-09-15); Appendix E.4 keeps the classifier's precision.",
    "The pilot preceded the main study with a different prompt": "Appendix E.2 opens on the same sentence split in two (the author's Pass 2 rule: a subsection opens with a plain sentence carrying no numeral): \"... cannot be compared numerically with the main study.\" then \"Its estimands and their table are in the supplement (Section~S.7).\"",
    "Monitoring runs before every query, so its cost turns on prompt caching": "Appendix E.11 (Spend and caching) opens on the same sentence split in two: \"Monitoring runs before every query, so its cost turns on prompt caching.\" then \"The projection and the billed micro-run are in the supplement (Section~S.8).\"",
    "A deployed monitor therefore thresholds at the base rate of positives": "Section 8: \"The score ranks well and calibrates badly (Appendix~\\ref{app:posthoc}), so a deployed monitor thresholds at the base rate of positives.\"",
}


def main():
    base = sys.argv[1]
    # regenerate from scratch: strip an earlier Pass 2 block from CLAIMS.md first, so every changed string is listed, not only the unauthorized remainder
    claims0 = CLAIMS.read_text(encoding="utf-8")
    if MARK in claims0:
        CLAIMS.write_text(claims0[:claims0.index(MARK)].rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    out = subprocess.run([sys.executable, str(ROOT / "reviews" / "v18" / "tools" / "frozen_list.py"), base, "--json=" + str(ROOT / "reviews" / "v18" / "frozen_rows.json")], capture_output=True, text=True, cwd=ROOT)
    rows = json.loads((ROOT / "reviews" / "v18" / "frozen_rows.json").read_text(encoding="utf-8"))
    rows = [r for r in rows if r["status"] == "UNAUTHORIZED"]
    entries, missing = [], []
    for n, r in enumerate(rows, 1):
        t = r["text"]
        disp = next((v for k, v in DISP.items() if t.startswith(k)), None)
        if disp is None:
            missing.append(t); continue
        before = t.split('"')[0].rstrip() if '"' in t else t
        entries.append(f"- **R110-P2-{n} [{r['tag']} {r['key']}]** ({r['base']} to {r['new']}). Before: \"{before}\". After: {disp}\n")
    if missing:
        for t in missing:
            print("NO DISPOSITION:", t[:120])
        sys.exit(1)
    block = (f"\n{MARK}\n\n**Pass 2 (2026-09-15): the body rewritten from reviews/v18/OUTLINE.md under the author's rules (the reader claim first; each paragraph opening with a plain sentence carrying no numeral; at most one interval in prose per paragraph; terms defined on first use; the sentence-length, vocabulary and near-duplicate rules of prose_scan; rule G with no allowlist). "
             f"The appendix is derived from v17 by reviews/v18/tools/appendix_v18.py (28 asserted edits). `paper_v18.tex` is built by reviews/v18/tools/build_v18.py; the base for the diff gates is the tree object in reviews/v18/base_tree.txt (paper_v17.tex sha256 4f5b5d91..., the rebuilt v17 of the W commit). "
             f"Each entry quotes the v17 string frozen_diff tracks and states what stands in its place; every number printed in v18 enters through a ledger key (reviews/NUMBERS_R110.md section 6 lists the printed forms).**\n\n" + "".join(entries))
    claims = CLAIMS.read_text(encoding="utf-8")
    if MARK in claims:
        i = claims.index(MARK); claims = claims[:i].rstrip("\n") + "\n"
    assert claims.rstrip().endswith("verify_pending.json and verify_results.json for the artifact.") or "## R110 AUTHORIZATION BLOCK" in claims
    # the R110 block is the last block in CLAIMS.md; append inside it
    assert claims.rfind("## R110 AUTHORIZATION BLOCK") > claims.rfind("## R109 AUTHORIZATION BLOCK")
    CLAIMS.write_text(claims.rstrip("\n") + "\n" + block, encoding="utf-8", newline="\n")
    copy = COPY.read_text(encoding="utf-8")
    if MARK in copy:
        copy = copy[:copy.index(MARK)].rstrip("\n") + "\n"
    COPY.write_text(copy.rstrip("\n") + "\n" + block, encoding="utf-8", newline="\n")
    print(f"{len(entries)} entries written to CLAIMS.md (R110 block) and {COPY.name}")


if __name__ == "__main__":
    main()
