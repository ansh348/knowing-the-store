# -*- coding: utf-8 -*-
"""appendix_r131_close.py -- the R131 close (2026-09-20; 'R131 MERGED RULINGS' 2, A3 follow-up, A5; 'R131 FINAL RULINGS' 2, 3, 5, 6): the appendix
edits, applied to reviews/v22/src/appendix_v22.tex after appendix_r131.py (regeneration order: cp v21 -> appendix_r126.py -> appendix_r128.py ->
appendix_r129.py -> appendix_r131.py -> appendix_r131_close.py -> fig3_data.py -> fig3_data_r131.py -> port_v22.py -> port_r131.py -> port_r131_close.py).
Every edit is asserted (rep); every count of the E.3 provenance paragraph is read from reviews/v22/tools/r131_close_gate.py (PROV), which counted it
from the tree; the paragraph is written in the third person for the release.
  E.3  the provenance paragraph (A1'') after the section's opening paragraph
  E.9  the Graphiti disclosure sentence in the third person (A3 follow-up; FINAL RULINGS 5)
  B    'preregistered primary endpoint' -> 'registered primary endpoint' (A5; the section is not pinned)
  E.4  'The preregistered item-level interval' -> 'The registered item-level interval' (A5; not pinned); the carried caption of tab:cluster-sensitivity
       is repaired by build_v22.py REPAIRS_R131CLOSE_BLOCK
  C.2  'one name longer' (two sentences) is LEFT: C.2 is pinned (FINAL RULINGS 3); the table beside prints 81 / 6 / 1
Usage: python reviews/v22/tools/appendix_r131_close.py [--check]
"""
from __future__ import annotations

import contextlib
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
APPX = ROOT / "reviews" / "v22" / "src" / "appendix_v22.tex"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
import r131_close_gate as G  # noqa: E402

CHANGES = []


def rep(t, old, new, n=1, where=""):
    assert t.count(old) == n, (where, t.count(old), n, old[:100])
    return t.replace(old, new)


def change(item, section, t, old, new, reason):
    CHANGES.append((item, section, old, new, reason))
    return rep(t, old, new, 1, item + " " + section)


def num(x):
    """A count in math mode, the thousands separator as the paper prints it ($1{,}400$)."""
    return "$" + f"{x:,}".replace(",", "{,}") + "$"


def prov_paragraph(P):
    per = P["sessions"] // P["personas"]
    assert per * P["personas"] == P["sessions"]
    v = P["fr_released_by_variant"]
    n = num
    L = ["%% R131 close, A1'' (2026-09-20): the provenance paragraph, every count from reviews/v22/tools/r131_close_gate.py (PROV; counted from the tree: LifeMemEval/, the freeze 5b097fb,",
         "%% e1_metamemory/build/items_final.json, r82_counterfactual/cf2 and cf3, cf_scores_ix.json, cf2_paraphrase, e1xv_crossvendor/manifests/cell_84.json, r85_graphiti); reviews/NUMBERS_R131.md AUX-R131-CLOSE-PROV.",
         "\\paragraph{Provenance of the personas, the stores and the questions.}",
         "The persona bank, the three main stores and the questions of the main study come from the FR-Bank release \\citep{fr}; the question sets this study added were drafted by language models.",
         f"The release holds {n(P['personas'])} personas, each with a human-written manifest and {n(per)} language-model-generated sessions ({n(P['sessions'])} in all), the FR-Bank, Mem0 and A-MEM stores built from those sessions, and {n(P['released_total'])} questions.",
         f"This study asks {n(P['fr_released_distinct'])} of those questions of the full FR-Bank store and its two ablated variants, the category-removed and the slot-removed store ({n(v['FULL'])}, {n(v['CAT-ABLATED'])} and {n(v['SLOT-ABLATED'])} questions; {n(P['fr_items_released'])} of the {n(P['fr_items'])} items of the full obligation set).",
         f"It adds the {n(P['fr_probes'])} natural-absent probes, drafted by a language model and verified against the manifests.",
         f"GPT-4.1 mini drafted, through frozen renderers, the counterfactual set's {n(P['cf_questions'])} questions with their three store versions ({n(P['cf_items'])} items) and the expiry extension ({n(P['ext_pairs'])} pairs, {n(P['ext_items'])} items).",
         f"It also drafted the {n(P['crossed_asked'])} crossed intent questions asked of {n(P['crossed_drafted'])} drafted and the {n(P['paraphrases'])} paraphrases.",
         f"The cross-vendor set is {n(P['xv_items'])} of the {n(P['fr_items'])} items ({n(P['xv_released'])} with a released question, {n(P['xv_probes'])} probes) and the question-only probes are classifiers over the existing question strings, so neither adds a question.",
         f"The Graphiti graphs, one per persona, were built by the unmodified release from {n(P['episodes'])} episodes rendered from the FR-Bank store's records, one per session, with every lifecycle field removed (Appendix~\\ref{{app:posthoc-graphiti}}).",
         ""]
    return "\n".join(L) + "\n"


E3_ANCHOR = ("This appendix carries the two user prompts, the obligation half of the rubric, and the construction record of the main study, because every reported estimate is bounded by one of them.\n"
             "Listing~\\ref{lst:summary} is the abridged summary the indexed monitor sees, rendered from the store of one persona.\n")
E9_OLD = "Disclosure, because it bears on independence: the personas and episodes used here were ingested into that backend earlier under a copy carrying four documented numeric-preservation modifications."
E9_NEW = ("%% R131 close, A3 follow-up (2026-09-20): the earlier ingestion attributed in the third person to the release, which vendors that copy (graphiti/ and graphiti_patches/ in the freeze 5b097fb; FINAL RULINGS 5).\n"
          "Disclosure, because it bears on independence: the FR-Bank release \\citep{fr} built an earlier version of its store on a copy of this backend carrying four documented numeric-preservation modifications and ingested these personas into it.")
B_OLD = "The item-level interval is the preregistered primary endpoint and the persona-clustered interval is the sensitivity, because that is the convention everywhere in this paper."
B_NEW = "The item-level interval is the registered primary endpoint and the persona-clustered interval is the sensitivity, because that is the convention everywhere in this paper."
E4_OLD = "The preregistered item-level interval remains the primary endpoint."
E4_NEW = "The registered item-level interval remains the primary endpoint."


def main():
    check = "--check" in sys.argv
    with contextlib.redirect_stdout(io.StringIO()):
        bad = G.main()
    assert not bad, bad
    t = APPX.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "%% R131 (2026-09-20)" in t and "%% R131 close" not in t, "appendix_r131_close.py: run after appendix_r131.py (and not twice)"
    para = prov_paragraph(G.PROV)
    assert "$1{,}400$" in para and "$1{,}365$" in para, para
    t = change("A1''", "E.3", t, E3_ANCHOR, E3_ANCHOR + "\n" + para, "the provenance paragraph, third person for the release, every count from the tree (FINAL RULINGS 2)")
    t = change("A3 follow-up", "E.9", t, E9_OLD, E9_NEW, "the earlier modified-copy ingestion attributed to the release in the third person (FINAL RULINGS 5)")
    t = change("A5", "B", t, B_OLD, B_NEW, "'preregistered' -> 'registered' (FINAL RULINGS 6; the section is not pinned; code_scan does not gate the appendix)")
    t = change("A5", "E.4", t, E4_OLD, E4_NEW, "'preregistered' -> 'registered' (FINAL RULINGS 6; not pinned)")
    assert "—" not in t
    if check:
        print("appendix_r131_close.py --check: would write", APPX)
        print(para)
        return
    io.open(APPX, "w", encoding="utf-8", newline="\n").write(t)
    print(f"-> {APPX} ({len(t.splitlines())} lines); {len(CHANGES)} edits")
    print(para)


if __name__ == "__main__":
    main()
