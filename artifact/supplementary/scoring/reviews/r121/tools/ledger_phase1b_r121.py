# -*- coding: utf-8 -*-
"""ledger_phase1b_r121.py -- program R121 Phase 1b (the author's three rulings on PHASE1_REPORT.md): append the second-lineage rows
to cf2/NUMBERS_CF2.md section 14 and fill the LINEAGE2_SHA placeholder of the registration draft. Every number read from the
artifacts. Idempotent. NO MODEL CALL."""
from __future__ import annotations

import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "r121" / "tools"))
import cue_list as C  # noqa: E402
import cross_questions as X  # noqa: E402

CF2 = ROOT / "r82_counterfactual" / "cf2"
LEDGER = CF2 / "NUMBERS_CF2.md"
BUILD = ROOT / "reviews" / "r121" / "build"
REG = ROOT / "reviews" / "r121" / "registrations_draft" / "ADDENDUM_CF2_INTENT_CROSSOVER.md"
MARK = "### 14b. Phase 1b"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    text = io.open(LEDGER, encoding="utf-8").read()
    assert MARK not in text, "14b already written"
    q = json.load(io.open(BUILD / "cross_questions.json", encoding="utf-8")); m = q["meta"]; rows = q["questions"]; l2 = m["lineage2"]
    assert l2["lineage_sha256"] == X.lineage2_sha256()
    wl = json.load(io.open(BUILD / "workbook_lock_r121.json", encoding="utf-8"))
    lk = json.load(io.open(CF2 / "results" / "leakscreen_ix.json", encoding="utf-8"))
    n_a = sum(r["population"] == "A" for r in rows); n_b = len(rows) - n_a
    cov = {pop: sum(C.matches(r["fallback"]["question"]) for r in rows if r["population"] == pop) for pop in "AB"}
    ident = {pop: sum(r["fallback_identical"] for r in rows if r["population"] == pop) for pop in "AB"}
    # the registration placeholder
    reg = io.open(REG, encoding="utf-8").read()
    assert reg.count("LINEAGE2_SHA") == 1
    io.open(REG, "w", encoding="utf-8", newline="\n").write(reg.replace("LINEAGE2_SHA", l2["lineage_sha256"]))
    cells = lk["cells"]; sup = lk.get("cells_superseded", {})
    L = [f"\n{MARK} — the author's three rulings on `reviews/r121/PHASE1_REPORT.md` (2026-09-19): P-I4 demoted to descriptive (the cue list identifies the intent of every crossed question by construction; a registered descriptive row adds each model under P1 beside the keyword-intent lookup on the pooled estimand); a registered second lineage replaces the temperature-0 fallback; a cue-free population is an open item for the rebuttal period, not an experiment here. Rows below from `cross_questions.py draft2`, `ix_leakscreen.py --lineage2`, `build_workbook_r121.py`.\n",
         "| Key | Value |", "|---|---|",
         f"| **AUX-CF2-IX-QUESTIONS** (lineage 2) | The registered second lineage: the same instruction and model (`gpt-4.1-mini`, served `{', '.join(l2['served'])}`, system fingerprints {', '.join('`' + f + '`' for f in l2['system_fingerprints'])}), **temperature {l2['temperature']}, seed {l2['seed']}**, one question per pair, {len(rows)} calls; lineage sha256 `{l2['lineage_sha256']}` (the renderer's seven fields with the temperature 0.7); questions sha256 `{l2['questions_sha256']}`. "
         f"Gate failures **{l2['gate_fail']}**. **Byte-identical to the seed-42 primary: {l2['identical_to_primary']} of {len(rows)}** (A {ident['A']} of {n_a}, B {ident['B']} of {n_b}; the temperature-0 fallback it supersedes was identical on {m['fallback_t0_superseded']['identical_to_primary']}), so the fallback offers a different question on {len(rows) - l2['identical_to_primary']} pairs; a failed primary with an identical fallback is a drop by rule. "
         f"Cue coverage of the lineage: A {cov['A']} of {n_a}, B {cov['B']} of {n_b} (cue-bearing on purpose; the population stays homogeneous). The superseded temperature-0 rows stay in `cross_questions.json` as `fallback_t0_superseded`. Tokens {l2['tokens_in']} in / {l2['tokens_out']} out; **${l2['usd']:.4f}**. |",
         f"| **AUX-CF2-IX-CHECK** (rebuilt) | `reviews/r121/build/AUTHOR_CHECK_R121.xlsx` **rebuilt: sha256 as built `{wl['sha256_as_built']}`** ({wl['built']}); the earlier build (`e2e6de67…`, 98 IDENTICAL rows greyed) is superseded and not sent. Tab `seed4242` now carries lineage 2 for all {wl['n_rows']} rows, no greying, the header kept (consult only for rows failed on `seed42`); {len(wl['locked_cells'])} locked cells hashed in `build/workbook_lock_r121.json`. The returned workbook's sha256, the verdict counts, the rows that used the second seed and the drops fill this row at Phase 2. |",
         f"| **AUX-CF2-IX-LEAK** (lineage 2) | `results/leakscreen_ix.json` (`--lineage2`): the registered cells carried unchanged from the first run (**A_primary {cells['A_primary']['n_correct']} of {cells['A_primary']['n']}, PASS; B_primary {cells['B_primary']['n_correct']} of {cells['B_primary']['n']}, PASS**); the lineage-2 cover cells on the sampled items whose fallback differs from the primary: "
         + "; ".join(f"**{k}** {c['n_correct']} of {c['n']} correct, {c['n_non_unknown']} non-UNKNOWN, {c['n_parse_failures']} parse failures" for k, c in cells.items() if not c["registered_cell"])
         + f". The temperature-0 cover cells ({', '.join(f'{k} {c['n_correct']} of {c['n']}' for k, c in sup.items())}) moved to `cells_superseded`. ${lk['meta']['usd_total']:.4f} this file (${lk['meta'].get('usd_total_including_superseded', lk['meta']['usd_total']):.4f} with the superseded cells). |",
         f"| **AUX-CF2-IX-SPEND** (Phase 1, cumulative) | OpenAI, token-metered at list price: drafting ${m['usd']:.4f} + lineage 2 ${l2['usd']:.4f} + leak screens ${lk['meta'].get('usd_total_including_superseded', lk['meta']['usd_total']):.4f} = **${m['usd'] + l2['usd'] + lk['meta'].get('usd_total_including_superseded', lk['meta']['usd_total']):.4f}** of the 4 USD cap; Anthropic $0. Not an invoice. |",
         ]
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
