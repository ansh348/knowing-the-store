# -*- coding: utf-8 -*-
"""ix_ledger.py -- program R121: from cf2/results/cf_scores_ix.json write ledger section 14d of cf2/NUMBERS_CF2.md and
reviews/r121/HELD_TEXTS_R121.md (the registered held texts of section 9 with their numbers filled, for the main session to land on
the author's ruling). Every number is read from the scores file; nothing typed. Idempotent. NO MODEL CALL."""
from __future__ import annotations

import datetime as dt
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CF2 = ROOT / "r82_counterfactual" / "cf2"
LEDGER = CF2 / "NUMBERS_CF2.md"
SCORES = CF2 / "results" / "cf_scores_ix.json"
HELD = ROOT / "reviews" / "r121" / "HELD_TEXTS_R121.md"
MARK = "### 14d. Phase 2"
READERS = ("MINI", "H45", "LUNA", "OP5", "SOL")
NAMES = {"MINI": "GPT-4.1 mini", "H45": "Haiku 4.5", "LUNA": "GPT-5.6 Luna", "OP5": "Opus 5", "SOL": "GPT-5.6 Sol (Amendment 1)"}


def ci(c):
    return f"[{c['ci_lo']:.4f}, {c['ci_hi']:.4f}]"


def ss_cell(e):
    s = e["same_store"]
    return f"**{s['auroc']:.4f}** {ci(s['ci_persona'])} {ci(s['ci_pair'])} · {s['wtl'][0]}/{s['wtl'][1]}/{s['wtl'][2]}"


def inter_cell(e):
    i = e["interaction"]
    return f"{i['mean']:+.4f} {ci(i['ci_persona'])} {ci(i['ci_pair'])}"


def pooled_cell(e):
    p = e["pooled"]
    return f"{p['auroc']:.4f} {ci(p['ci_persona'])} {ci(p['ci_pair'])}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    res = json.load(io.open(SCORES, encoding="utf-8"))
    text = io.open(LEDGER, encoding="utf-8").read()
    assert MARK not in text, "14d already written"
    P = res["predictions"]; sp = res["spend"]; lock = res["lock"]; pr = res["probes"]
    L = [f"\n{MARK} — the run and the scores (registered text sha256 `{res['registration_sha256'][:16]}…`, frozen at `{res['frozen_at']}`; `reviews/r121/tools/ix_run.py`, `ix_score.py`; `rows/rows_IX_MINI.jsonl`, `rows_IX_LUNA.jsonl`, `rows_IX_H45.jsonl`, `rows_IX_OP5.jsonl`, `rows/lock_ix.json`, `rows/probes_ix.json`, `rows/batch_IX_H45.json`, `batch_IX_OP5.json`; `results/cf_scores_ix.json`; scored {res['when'][:10]})\n",
         "### AUX-CF2-IX-LOCK, AUX-CF2-IX-PROBES\n",
         f"Registration sha256 holds; P0 digests, P1 sha256 `{lock['p1_system_sha256'][:16]}…`, cue list `{lock['cue_list_sha256'][:16]}…`, questions `{lock['questions_sha256']['primary'][:16]}…` / `{lock['questions_sha256']['lineage2'][:16]}…`, returned workbook `{lock['workbook_returned_sha256'][:16]}…` asserted at start; {lock['pairs_in_scope']} pairs, {lock['units_total']} units of the design, new units per lane {json.dumps(lock['units_per_lane'])}. "
         "Probes (E1.7 rule): " + "; ".join(f"`{l}` served `{', '.join(pr[l]['served'])}`, P0 {pr[l]['p0_in']} / P1 {pr[l]['p1_in']} in, out {pr[l]['out']}, ${pr[l]['usd']:.6f}" for l in READERS) + ".\n",
         "### AUX-CF2-IX-CENSUS\n", "| lane | rows | not OK | units | draws per unit | identical across draws | median range | usd |", "|---|---:|---:|---:|---|---:|---|---:|"]
    for l in READERS:
        c = res["census"][l]
        L.append(f"| {l} | {c['rows']} | {c['not_ok']} | {c['units']} | {c['draws_per_unit']} | {c['identical_across_draws']} | {c['median_range']} | ${c['usd']:.4f} |")
    L += ["\n### AUX-CF2-IX-<READER>-<A|B>-<P0|P1> — the primary and secondary estimands (same-store AUROC of cell 1 against cell 3 with the persona-grouped then the pair-clustered interval, W/T/L; the interaction mean with both intervals; the pooled AUROC of cell 1 against cells 2 to 4 with both intervals)\n",
          "| reader | pop | arm | same-store AUROC [persona] [pair] · W/T/L | interaction | pooled | cells 1 vs 2 |", "|---|---|---|---|---|---|---|"]
    for l in READERS:
        for pop in ("A", "B"):
            for arm in ("P0", "P1"):
                e = res["readers"][l][pop][arm]
                L.append(f"| {NAMES[l]} | {pop} | {arm} | {ss_cell(e)} | {inter_cell(e)} | {pooled_cell(e)} | {e['cell1_vs_cell2']['auroc']:.4f} |")
                if "draw1" in e:
                    d = e["draw1"]
                    L.append(f"| {NAMES[l]} (draw 1 only, the comparable column) | {pop} | {arm} | {ss_cell(d)} | {inter_cell(d)} | {pooled_cell(d)} | {d['cell1_vs_cell2']['auroc']:.4f} |")
            if "P0_sensitivity_five_draw_cells12" in res["readers"][l][pop]:
                e = res["readers"][l][pop]["P0_sensitivity_five_draw_cells12"]
                L.append(f"| {NAMES[l]} (sensitivity: recorded five-draw means for cells 1, 2) | {pop} | P0 | {ss_cell(e)} | {inter_cell(e)} | {pooled_cell(e)} | {e['cell1_vs_cell2']['auroc']:.4f} |")
    sl = res["readers"]["SOL"]["A"].get("sol_losses_P1")
    if sl:
        L.append(f"\nGPT-5.6 Sol on population A under P1, within-pair counts {sl['wtl'][0]}/{sl['wtl'][1]}/{sl['wtl'][2]}: of its {sl['n']} losses, **{sl['n_both_at_least_0_96']} have both questions scored 0.96 or higher**; a CHANGE question licenses the old value, so a correct reading is low, and those pairs are failures to apply the intent rule (the author's reading, 14d-interim-3). Pairs: " + "; ".join(f"`{x['pair_id']}` ({x['nok_cell1']:.2f} / {x['nok_cell3']:.2f})" for x in sl["losses"]) + ".")
    L += ["\n### AUX-CF2-IX-LOOKUPS (no model call; the name lookup, the keyword-intent lookup, the oracle-intent lookup; the cue share by cell; the question-length difference of ruling 8)\n",
          "| lookup | pop | same-store AUROC [persona] [pair] · W/T/L | interaction | pooled |", "|---|---|---|---|---|"]
    for pop in ("A", "B"):
        for name in ("name", "keyword", "oracle"):
            e = res["lookups"][pop][name]
            L.append(f"| {name} | {pop} | {ss_cell(e)} | {inter_cell(e)} | {pooled_cell(e)} |")
    for pop in ("A", "B"):
        q = res["lookups"][pop]["question_length"]; cs = res["lookups"][pop]["cue_fired_share_by_cell"]
        L.append(f"\nPopulation {pop}: cue share by cell {json.dumps(cs)}; crossed minus original question length **{q['tokens_mean_delta']:+.2f} content tokens** (original {q['tokens_original_mean']:.2f}, crossed {q['tokens_crossed_mean']:.2f}) and {q['chars_mean_delta']:+.1f} characters on average.")
    L += ["\n### AUX-CF2-IX-P-I4 (descriptive): each model under P1 minus the keyword-intent lookup, same-store and pooled, [persona] [pair]\n",
          "| reader | pop | same-store Δ | pooled Δ |", "|---|---|---|---|"]
    for l in READERS:
        for pop in ("A", "B"):
            e = res["readers"][l][pop]["P1"]
            L.append(f"| {NAMES[l]} | {pop} | {e['vs_keyword_same']['delta']:+.4f} {ci(e['vs_keyword_same']['ci_persona'])} {ci(e['vs_keyword_same']['ci_pair'])} | {e['vs_keyword_pooled']['delta']:+.4f} {ci(e['vs_keyword_pooled']['ci_persona'])} {ci(e['vs_keyword_pooled']['ci_pair'])} |")
    L += ["\n### AUX-CF2-IX-P-I5 (descriptive): cells 1 vs 2 on the original questions, P1 minus P0, [persona] [pair]\n", "| reader | pop | P0 | P1 | Δ |", "|---|---|---|---|---|"]
    for l in READERS:
        for pop in ("A", "B"):
            e = res["readers"][l][pop]["p1_minus_p0_cell1_vs_cell2"]
            L.append(f"| {NAMES[l]} | {pop} | {e['p0']:.4f} | {e['p1']:.4f} | {e['delta']:+.4f} {ci(e['ci_persona'])} {ci(e['ci_pair'])} |")
    L += [f"\nNo model lowered by more than 0.05: **{P['P-I5']['no_model_lowered_by_more_than_tol']}**.\n",
          "### AUX-CF2-IX-P-I1\n", f"**{P['P-I1']['text']}**\n", "### AUX-CF2-IX-P-I2\n", f"**{P['P-I2']['text']}**\n", "### AUX-CF2-IX-P-I2B (Amendment 1; a prediction made after the interim read)\n", f"**{P['P-I2b']['text']}**\n", "### AUX-CF2-IX-P-I3\n", f"**{P['P-I3']['text']}**\n",
          "### AUX-CF2-IX-SPEND\n",
          f"Token-metered from the rows (Anthropic Batch at the 0.5 multiplier; OpenAI at the page prices of 2026-09-18 with the cache fields): MINI ${sp['MINI']:.4f}, LUNA ${sp['LUNA']:.4f}, H45 ${sp['H45']:.4f}, OP5 ${sp['OP5']:.4f}; probes {json.dumps(sp['probes'])}; **Anthropic ${sp['anthropic']:.4f} of the 15 USD cap; OpenAI ${sp['openai_run']:.4f} for the run, ${sp['openai_with_phase1']:.4f} with Phase 1, of the 4 USD cap; the Sol lane (Amendment 1) ${sp['sol_amend1']:.4f} of its own {sp['sol_cap']:.0f} USD cap.** Not an invoice.\n"]
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")

    print("\n".join(L)); print("(held texts: ix_held_texts.py)")


if __name__ == "__main__":
    main()
