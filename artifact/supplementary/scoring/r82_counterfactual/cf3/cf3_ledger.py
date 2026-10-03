"""cf3_ledger.py -- write NUMBERS_CF3.md (sections 1-4) and the LaTeX table for Appendix D.2 from the CF-3 artifacts.
No model call. Re-runnable: the sections below '## 1.' are regenerated whole; section 0 is kept as written before the first call."""
from __future__ import annotations

import io
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
CF3 = ROOT / "r82_counterfactual" / "cf3"
LED = CF3 / "NUMBERS_CF3.md"
LANES = {"gpt-4.1-mini": "GPT-4.1 mini", "claude-haiku-4-5-20251001": "Haiku 4.5", "claude-opus-5": "Opus 5"}


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]{'*' if d.get('excludes_zero') else ''}"


def usd_rows(code):
    p = CF3 / "rows" / f"rows_{code}.jsonl"
    if not p.exists():
        return None, 0, 0
    rows = [json.loads(l) for l in io.open(p, encoding="utf-8")]
    return sum(r.get("usd", 0.0) for r in rows), len(rows), sum(1 for r in rows if r.get("status") != "OK")


def main():
    pairs = J(CF3 / "cf_pairs_cf2.json"); q = J(CF3 / "cf_questions_cf2.json"); cell = J(CF3 / "cf_cell.json"); idx = J(CF3 / "cf_indexes.json")
    leak = J(CF3 / "results" / "leakscreen_cf3.json") if (CF3 / "results" / "leakscreen_cf3.json").exists() else None
    probes = J(CF3 / "probes.json") if (CF3 / "probes.json").exists() else {}
    sc = J(CF3 / "results" / "cf_scores_cf3.json") if (CF3 / "results" / "cf_scores_cf3.json").exists() else None
    census = J(CF3 / "census_cf3.json")
    A = census["A_manifests"]
    tot = {k: sum(r[k] for r in A) for k in ("manifest_retractions", "retraction_records_resolving_to_an_entry", "entries_retracted_under_TRUE", "store_flag_is_retracted",
                                            "manifest_expiring_logistics", "expiring_status_expired", "expired_records_resolving_to_an_entry", "entries_expired_under_TRUE")}
    adjR = J(ROOT / "r82_counterfactual" / "cf2" / "adjudication_cf2.json")["RETRACTION"]
    L = ["## 1. AUX-CF3-LOCK, AUX-CF3-QUESTIONS, AUX-CF3-CELL, AUX-CF3-LEAK — the build (`cf3_build.py`)", "", "| Key | Value |", "|---|---|",
         f"| **AUX-CF3-LOCK** | Registration sha256 holds; census sha256 `{pairs['meta']['census_sha256'][:16]}…` holds; 14 pairs, every one ELIGIBLE in `cf2/adjudication_cf2.json` "
         f"({sum(1 for p in pairs['pairs'] if p['adjudication_source'] == 'CF-1 reused')} CF-1 reused, {sum(1 for p in pairs['pairs'] if p['adjudication_source'] != 'CF-1 reused')} author 2026-09-12); none in the 444 by (persona, entry id); "
         f"overlap tags as CF-2 admitted them: {', '.join(p['pair_id'] + ' ' + p['overlap_tag'] for p in pairs['pairs'] if p['overlap_tag'])}. |",
         f"| **AUX-CF3-QUESTIONS** | The frozen CF-1 renderer (prompt sha256 `{q['meta']['prompt_sha256'][:16]}…`, `gpt-4.1-mini`, temperature 0, seed 42): {q['meta']['n']} questions, "
         f"{q['meta']['redrafts']} redrafts, {q['meta']['substitutions']} substitution, questions sha256 **`{q['meta']['questions_sha256']}`**, ${q['meta']['usd']:.4f}. |",
         f"| **AUX-CF3-CELL** | {cell['meta']['n']} items ({cell['meta']['composition']} = supersession / retraction / expiry pairs), 14 PN positives; assertions A–E, the draw-time predicates and assertion C hold on 14 of 14; "
         f"indexes sha256 `{idx['meta']['sha256'][:16]}…`, v2r sha256 `{idx['meta']['sha256_v2r'][:16]}…` (a derangement within the cell's 42 versions, rotation k = {idx['meta']['v2r']['rotation_k']}, {idx['meta']['v2r']['distinct_values']} distinct (retracted, expired) values, 0 versions keeping their own pair); "
         f"summaries {cell['meta']['index_size']['v2']['lines_min']}–{cell['meta']['index_size']['v2']['lines_max']} lines (v2). |"]
    if leak:
        cells = leak["cells"] if "cells" in leak else leak
        L.append("| **AUX-CF3-LEAK** | " + "; ".join(f"{arm}: {c['n_correct']} of {c['n']} correct (leaks iff more than {c['threshold']}) — {'LEAK' if c['leaked'] else 'PASS'}"
                                                   for arm, c in cells.items() if isinstance(c, dict) and "n_correct" in c) + f"; served `{', '.join(leak['meta'].get('served_models') or [])}`; ${leak['meta'].get('usd_total', 0):.4f}. |")
    L += ["", "## 2. AUX-CF3-PROBE-*, AUX-CF3-PROJECTION — the lanes before submission (`cf3_run.py probe / project`)", "", "| Key | Value |", "|---|---|"]
    for lane, rec in probes.items():
        L.append(f"| **AUX-CF3-PROBE-{LANES[lane].split()[0].upper()}** | served `{rec['served']}` ({'PASS' if rec['identifier_ok'] else 'FAIL'}); prompt tokens blind {rec['blind_in']}, v2 {rec['v2_in']}, v3 {rec['v3_in']}; completion {rec['out']}. |")
    L.append("| **AUX-CF3-PROJECTION** | mini 140 calls $0.09, Haiku 4.5 700 calls $0.83, Opus 5 140 calls $1.08 — $2.00 (×1.3 $2.60) against the $5 line (`cf3_run.py project`). |")
    if sc:
        L += ["", "## 3. AUX-CF3-LOOKUP-*, AUX-CF3-{MINI,H45,OP5}-*, AUX-CF3-POOLED-* — the scores (`cf3_score.py`; `results/cf_scores_cf3.json`)", "",
              "Blind is one call per question, reused across its three versions, so blind AUROC is 0.5000 by identity on every set and each AUROC is also a gain. Intervals: item-level paired bootstrap (1,000 draws, seed 42) and persona-clustered, `*` excludes zero; the weaker reading governs. "
              "Model − lookup: the model's row minus the embedding lookup on the same summary (v2 and v2r against the superseded-names lookup, v3 against the all-states lookup), same construction as `AUX-R103-MARGIN`. "
              f"Gate: the CF-2 expiry slice's lookups reproduce `AUX-CF2-NB6-V2` / `AUX-CF2-ALLSTATES-V3` per state (embedding v2 {sc['gate']['cf2_expiry_emb_v2']:.4f}, v3 {sc['gate']['cf2_expiry_emb_v3']:.4f}: {'PASS' if sc['gate']['ok'] else 'FAIL'}).", ""]
        for name, c in sc["cells"].items():
            key = {"cf3": "AUX-CF3", "cf2_expiry": "AUX-CF3-CF2SLICE", "pooled": "AUX-CF3-POOLED"}[name]
            L += [f"**{key}** — {c['label']} ({c['n']} items, {c['pos']} positives, {c['personas']} personas).", "",
                  "| reader | summary | AUROC | Δ vs blind (item CI; persona CI) | model − embedding lookup (weaker CI) | model − lexical lookup (weaker CI) |", "|---|---|---:|---|---|---|"]
            for lk, lab in (("emb_v2", "embedding lookup, superseded names (v2)"), ("lex_v2", "lexical lookup, superseded names (v2)"), ("emb_v3", "embedding lookup, all states (v3)"), ("lex_v3", "lexical lookup, all states (v3)")):
                v = c["lookups"][lk]
                L.append(f"| {lab} | — | **{v['auroc']:.4f}** | persona CI of the AUROC [{v['persona_ci'].get('ci_lo', float('nan')):.4f}, {v['persona_ci'].get('ci_hi', float('nan')):.4f}] | — | — |")
            for model, row in c["models"].items():
                if "status" in row:
                    L.append(f"| {LANES[model]} | — | — | {row['status']} | — | — |"); continue
                for tag in ("v2", "v3", "v2r"):
                    r = row[tag]
                    L.append(f"| {LANES[model]}{' (k = 5 on the CF-2 rows, k = 1 on the CF-3 rows)' if model == 'claude-opus-5' and name == 'pooled' else ''} | {tag} | **{r['indexed']:.4f}** | {r['delta']:+.4f}; item {ci(r['item_ci'])}; persona {ci(r['persona_ci'])} | "
                             f"{r['model_minus_emb_lookup']['delta']:+.4f} {ci(r['model_minus_emb_lookup']['weaker'])} | {r['model_minus_lex_lookup']['delta']:+.4f} {ci(r['model_minus_lex_lookup']['weaker'])} |")
                if "v2r_minus_v2" in row:
                    e = row["v2r_minus_v2"]
                    L.append(f"| {LANES[model]} | v2r − v2 | — | {e['delta']:+.4f}; item {ci(e['item_ci'])}; persona {ci(e['persona_ci'])} | — | — |")
            L.append("")
    if sc:
        c3 = sc["cells"]["cf3"]
        L += ["**AUX-CF3-PRINTED** — the two-decimal forms Appendix D.2's prose prints, against their four-decimal sources in this file (the R97/R102 printed-forms convention):", "",
              "| printed | source |", "|---|---|",
              f"| 0.97 | {c3['lookups']['emb_v3']['auroc']:.4f} (AUX-CF3, all-states lookup, v3) |",
              f"| 0.68 | {c3['models']['gpt-4.1-mini']['v3']['indexed']:.4f} (AUX-CF3, GPT-4.1 mini, v3) |", ""]
    L += ["## 4. AUX-CF3-CENSUS — the sizing census the population rests on (`census_cf3.py`, `CF3_CENSUS.md`; no call)", "", "| Key | Value |", "|---|---|",
          f"| **AUX-CF3-CENSUS-MANIFEST** | The 40 manifests record **{tot['manifest_retractions']} retraction events** (one per persona), **{tot['retraction_records_resolving_to_an_entry']}** of which resolve to a retracted entry under the truthful join (index_v2.true_lifecycle, TAU_HI; {tot['entries_retracted_under_TRUE']} entries in all), against {tot['store_flag_is_retracted']} entries the store marks retracted; "
          f"{tot['expiring_status_expired']} expired logistics records, {tot['expired_records_resolving_to_an_entry']} resolving ({tot['entries_expired_under_TRUE']} entries). |",
          f"| **AUX-CF3-CENSUS-RETRACTION** | Under the CF-2 predicates 1,018 retraction candidates entered the queue; the author's eligibility read (ADDENDUM_CF2 §3.1) left **{adjR['walk_status_counts']['ELIGIBLE'] + adjR['walk_status_counts']['REUSED']} ELIGIBLE among the {adjR['verdict_reads'] + adjR['walk_status_counts']['REUSED']} candidates carrying a verdict** ({adjR['walk_status_counts']['ELIGIBLE']} of the {adjR['verdict_reads']} the author read plus one CF-1 verdict reused; rate {adjR['eligibility_rate_new_over_verdict_reads']}, about one in ten; {adjR['walk_status_counts']['UNREAD']} unread); 30 used; the name rule (`project` on 336 of the 578 unread) bounds any extension more than the predicates do. Retraction stays at 30 by the author's ruling of 2026-09-14. |",
          f"| **AUX-CF3-CENSUS-EXPIRY** | 70 expiry candidates entered the queue and every one was read: 49 ELIGIBLE, 30 used, 19 undrawn, **14 fitting the cap and the name rule** — the population of this addendum. |", ""]
    L += ["## 5. AUX-CF3-SPEND", "", "| Key | Value |", "|---|---|"]
    parts, total = [], 0.0
    parts.append(f"drafting ${q['meta']['usd']:.4f}"); total += q["meta"]["usd"]
    if leak:
        lu = leak["meta"].get("usd_total", 0.0)
        parts.append(f"leakage screen ${lu:.4f}"); total += lu or 0
    for lane, rec in probes.items():
        pu = 0.0
        parts.append(f"probe {LANES[lane]} (3 calls)")
    for code, lane in (("MINI", "gpt-4.1-mini"), ("H45", "claude-haiku-4-5-20251001"), ("OP5", "claude-opus-5")):
        u, n, bad = usd_rows(code)
        if u is not None:
            parts.append(f"{LANES[lane]} lane ${u:.4f} ({n} rows, {bad} not OK)"); total += u
    L.append(f"| **AUX-CF3-SPEND** | {'; '.join(parts)}; **total ${total:.4f}** metered from the rows at list / Batch prices against the $5 line (probes metered in the lanes' probe files). |")
    s = io.open(LED, encoding="utf-8").read()
    head = s.split("\n## 1. ")[0].rstrip("\n") + "\n\n"
    io.open(LED, "w", encoding="utf-8", newline="\n").write(head + "\n".join(L) + "\n")
    print("wrote", LED)


if __name__ == "__main__":
    main()


# ------------------------------------------------------------------------------------------ the Appendix D.2 table
def paper_table():
    """tab:cf3-expiry: the CF-3 cell beside the 444's expiry slice and the pooled row, per reader and summary; four
    decimals in the cells, as every appendix table prints."""
    sc = J(CF3 / "results" / "cf_scores_cf3.json")
    c2, c3, cp = sc["cells"]["cf2_expiry"], sc["cells"]["cf3"], sc["cells"]["pooled"]

    def cell(c, model, tag):
        row = c["models"].get(model)
        if not row or "status" in row:
            return "--"
        r = row[tag]
        return f"${r['indexed']:.4f}$ $[{r['weaker']['ci_lo']:+.4f},{r['weaker']['ci_hi']:+.4f}]$"

    def lk(c, k):
        v = c["lookups"][k]
        return f"${v['auroc']:.4f}$ $[{v['persona_ci']['ci_lo']:+.4f},{v['persona_ci']['ci_hi']:+.4f}]$"
    BS = "\\"
    L = [BS + "begin{table}[H]",
         "% R105 (2026-09-14): the CF-3 expiry extension (registrations/ADDENDUM_CF3.md, sha256 2f555c1a...; r82_counterfactual/cf3/NUMBERS_CF3.md AUX-CF3-*, AUX-CF3-POOLED-*).",
         BS + "caption{The expiry state of the counterfactual set extended by a third descriptive draw: the $444$'s $30$ expiry pairs ($90$ items), the $14$ eligible pairs the first draw left undrawn ($42$ items, built by the same construction with questions written before any store version existed), and the two pooled ($44$ pairs, $132$ items). "
         "Obligation AUROC per reader and summary; blind is $0.5000$ by construction on every set, so each value is also a gain. Intervals are the weaker of the item-level and profile-grouped paired intervals for the models and the profile interval of the AUROC for the lookups. "
         "The pooled row joins two cells scored on different dates under two registrations with the same prompts, models and construction; Opus 5's rows are five-call averages on the $444$ and single calls on the extension, so its pooled row mixes the two. Descriptive; no prediction was registered.}",
         BS + "label{tab:cf3-expiry}", BS + "centering", BS + "scriptsize", BS + "setlength{" + BS + "tabcolsep}{2.5pt}",
         BS + "begin{tabular}{@{}llrrr@{}}", BS + "toprule",
         "Reader & summary & $444$ expiry ($30$ pairs) & extension ($14$ pairs) & pooled ($44$ pairs) " + BS + BS, BS + "midrule",
         f"Superseded-names lookup & sup.{BS} only & {lk(c2, 'emb_v2')} & {lk(c3, 'emb_v2')} & {lk(cp, 'emb_v2')} " + BS + BS,
         f"All-states lookup & all three & {lk(c2, 'emb_v3')} & {lk(c3, 'emb_v3')} & {lk(cp, 'emb_v3')} " + BS + BS]
    for model, name in LANES.items():
        for tag, lab in (("v2", "sup." + BS + " only"), ("v3", "all three"), ("v2r", "counts rand.")):
            L.append(f"{name} & {lab} & {cell(c2, model, tag)} & {cell(c3, model, tag)} & {cell(cp, model, tag)} " + BS + BS)
    L += [BS + "bottomrule", BS + "end{tabular}", BS + "end{table}"]
    (CF3 / "paper_table.tex").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("wrote", CF3 / "paper_table.tex")


if __name__ == "__main__" and "--table" in __import__("sys").argv:
    paper_table()
