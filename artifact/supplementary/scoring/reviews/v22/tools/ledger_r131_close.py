# -*- coding: utf-8 -*-
"""ledger_r131_close.py -- the R131 close's rows of reviews/NUMBERS_R131.md (2026-09-20): every number the close's new texts print beside its artifact
value and source (the checks of reviews/v22/tools/r131_close_gate.py), the provenance counts of Appendix E.3's paragraph (AUX-R131-CLOSE-PROV, each
counted from the tree), the abstract's two drops, and the rulings recorded with numbers in them (G2; Sol's 0.33 under half-up). Idempotent: the
'## AUX-R131-CLOSE' sections are replaced in place when they exist. No number is typed by hand. trace_scan_v13 reads the file (LEDGERS).
Usage: python reviews/v22/tools/ledger_r131_close.py
"""
from __future__ import annotations

import contextlib
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "reviews" / "NUMBERS_R131.md"
sys.path.insert(0, str(ROOT / "reviews" / "v22" / "tools"))
import r131_close_gate as G  # noqa: E402

MARK = "\n## AUX-R131-CLOSE-PRINTED"


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        bad = G.main()
    assert not bad, bad
    P = G.PROV
    L = [MARK + " — the R131 close (2026-09-20; CONSOLIDATED ADDITIONS, ABSTRACT SWAP, MERGED RULINGS, FINAL RULINGS): every number the close's new texts print, "
         f"beside its artifact value and source (`reviews/v22/tools/r131_close_gate.py`: {len(G.CHECKS)} checks, 0 mismatches; rounding half-up on the recorded four-decimal value, as AUX-R131-PRINTED)\n\n",
         "| where | printed | artifact value | reliability, claimed / artifact | source |\n|---|---|---|---|---|\n"]
    for c in G.CHECKS:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rel = "" if c["reliable"] is None else f"{'reliable' if c['reliable'] else 'not reliable'} / {'reliable' if c['actual_reliable'] else 'not reliable'}"
        L.append(f"| {c['where']} | {c['printed']} | {vs} | {rel} | {c['source']} |\n")
    d_mini, d_lookup = P["drops"]
    L.append(f"\nThe abstract's third finding prints the levels (0.73 and 0.75 to 0.60 and 0.59; G2 under its pattern reading, the author's ruling of the FINAL RULINGS 3: G2 concerns the lookup's level on the "
             f"counterfactual set, where the level depends on the metric; the full-set numbers have one metric). The drops, for the record: mini {d_mini:.4f} (0.14), the lookup {d_lookup:.4f} (0.16); "
             "R124 block C states no reason contradicting the ruling, so the level form stands.\n")
    L.append("\nSol's counted-state fall under the moved count, $-0.3250$ exactly (AUX-CF2-R125-CONTRASTS), prints 0.33 in the body: the number gate rounds every body number half-up on the recorded four-decimal value "
             "(`Decimal ... ROUND_HALF_UP`), so 0.33 is the convention applied to every other body number (MERGED RULINGS 1A, confirmed); the appendix row prints $-0.3250$.\n")
    v = P["fr_released_by_variant"]
    L.append("\n## AUX-R131-CLOSE-PROV — the provenance counts of Appendix E.3's paragraph (A1''), each counted from the tree by `r131_close_gate.py`; the release is the FR-Bank freeze `5b097fb` "
             "(audit/FREEZE_MANIFEST.md; Zenodo 10.5281/zenodo.20067778)\n\n| quantity | value | source |\n|---|---:|---|\n")
    rows = [("personas", P["personas"], "LifeMemEval/<n>_<name>/ numbered directories"),
            ("human-written manifests", P["manifests"], "LifeMemEval/<n>_<name>/persona_*.yaml"),
            ("sessions per persona", P["sessions"] // P["personas"], "session_*.json per directory (every persona 35)"),
            ("sessions, all personas (1,400 = 1400)", f"{P['sessions']:,} ({P['sessions']})", "LifeMemEval/<n>_<name>/sessions/session_*.json"),
            ("stores of the release read by the main study", P["stores_in_freeze"], "git ls-tree 5b097fb LifeMemEval/artifacts/: lifecycle_banks, mem0_41mini_banks, amem_banks (e1_metamemory/tools/backends.py:59-61)"),
            ("released questions", P["released_total"], "LifeMemEval/lifemembench_questions.json"),
            ("full obligation set, FR-Bank items", P["fr_items"], "e1_metamemory/build/items_final.json (backend frbank; ABSENT / PRESENT / PRESENT-NEGATIVE)"),
            ("of them asked with a released question", P["fr_items_released"], "items_final.json question_id in the released ids"),
            ("distinct released questions among them", P["fr_released_distinct"], "as above, distinct question_id"),
            ("released questions on the full store / category-removed / slot-removed variants", f"{v['FULL']} / {v['CAT-ABLATED']} / {v['SLOT-ABLATED']}", "items_final.json by variant"),
            ("natural-absent probe items (distinct texts)", f"{P['fr_probes']} ({P['fr_probe_texts']})", "items_final.json question_id probe_*"),
            ("distinct released questions used across the three backends", P["released_distinct_all"], "items_final.json, scored labels"),
            ("counterfactual questions / items", f"{P['cf_questions']} / {P['cf_items']}", "r82_counterfactual/cf2/cf_questions_cf2.json; 3 versions each"),
            ("expiry extension pairs / items", f"{P['ext_pairs']} / {P['ext_items']}", "r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3"),
            ("crossed intent questions drafted / asked / dropped", f"{P['crossed_drafted']} / {P['crossed_asked']} / {P['crossed_dropped']}", "r82_counterfactual/cf2/results/cf_scores_ix.json lock/counts (A 88 -> 87, B 30 -> 26)"),
            ("paraphrases drafted (GPT-4.1 mini)", P["paraphrases"], "cf2_paraphrase/para_questions.json rows"),
            ("cross-vendor set items / with a released question / probes", f"{P['xv_items']} / {P['xv_released']} / {P['xv_probes']}", "e1xv_crossvendor/manifests/cell_84.json"),
            ("Graphiti graphs / episodes (1,365 = 1365)", f"{P['graphs']} / {P['episodes']:,} ({P['episodes']})", "r85_graphiti/g10/ingest_all_status.json; r85_graphiti/NUMBERS_R85.md AUX-R85-G10-INGEST")]
    for q, val, src in rows:
        L.append(f"| {q} | {val} | {src} |\n")
    L.append("\nThe question-only probes (e1qp_questionprior/PREREG_E1QP.md) are classifiers over the existing question strings and the cross-vendor set is a subset of the 661, so neither adds a question; "
             "the Graphiti graphs were built from FR-Bank's store records rendered one episode per session with every lifecycle field removed (r85_graphiti/render_episodes.py), not from the session transcripts.\n")
    text = OUT.read_text(encoding="utf-8").replace("\r\n", "\n")
    if MARK in text:
        text = text[:text.index(MARK)]
    text = text.rstrip("\n") + "\n" + "".join(L)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print("->", OUT, len(G.CHECKS), "checks;", len(rows), "provenance rows")


if __name__ == "__main__":
    main()
