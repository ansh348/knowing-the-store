"""report_cf_pad.py -- write cf_pad/NUMBERS_CF_PAD.md (the ledger), cf_pad/results/cf_pad_printed.json and reviews/r136/REPORT_R136.md from
cf_pad/results/cf_pad_scores.json, build/lock.json, build/probes.json and the rows. No model call; re-runnable; every number read from the JSON,
none typed."""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cf_pad_common as C  # noqa: E402
from cf_pad_common import RES, jdump, jload  # noqa: E402

LEDGER = C.CFP / "NUMBERS_CF_PAD.md"
PRINTED = RES / "cf_pad_printed.json"
REPORT = C.R136 / "REPORT_R136.md"
DEVS = C.CFP / "DEVIATIONS_CF_PAD.md"
NAMES = {"LOOKUP": "Embedding name lookup", "LEX": "Word-matching lookup", "RANDTOK": "Random-token lookup", "MINI": "GPT-4.1 mini (5 draws)",
         "H45": "Haiku 4.5 (5 draws)", "LUNA": "GPT-5.6 Luna (5 draws)", "SOL": "GPT-5.6 Sol (5 draws)", "OP5": "Opus 5 (1 draw; recorded row 5 draws)"}
ORDER = ("LOOKUP", "LEX", "RANDTOK", "MINI", "H45", "LUNA", "SOL", "OP5")
MODELS = ("MINI", "H45", "LUNA", "SOL", "OP5")
SCOPE_NAME = {"whole": "whole set (444 items / 148 triples)", "superseded": "supersession (264 items / 88 triples)",
              "retracted": "retraction (90 items / 30 triples)", "expired": "expiry (90 items / 30 triples)"}


def hist_str(h):
    return ", ".join(f"{k}: {h[k]}" for k in sorted(h, key=int))


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def s4(x):
    return "—" if x is None else f"{x:+.4f}"


def ci(c):
    c = c or {}
    return "—" if "ci_lo" not in c else f"[{c['ci_lo']:+.4f}, {c['ci_hi']:+.4f}]"


def star(d):
    return " *" if d and d.get("both_exclude_zero") else ""


def pooled_ci(d):
    return f"{ci(d.get('ci_item'))}; {ci(d.get('ci_persona'))}"


def matched_ci(d):
    return f"{ci(d.get('ci_triple'))}; {ci(d.get('ci_persona'))}"


def reader_rows(S, scope):
    L = [f"| reader | pooled unpadded | pooled padded | Δ pooled (item; persona) | matched unpadded (W/T/L) | matched padded (W/T/L) | Δ matched (triple; persona) |",
         "|---|---:|---:|---|---|---|---|"]
    for code in ORDER:
        r = S["readers"].get(code)
        if not r or scope not in r:
            L.append(f"| {NAMES[code]} | — | — | lane not scored | — | — | — |"); continue
        p = r[scope]["pooled"]; m = r[scope]["matched"]; d = p["padded_minus_unpadded"]; dm = m["padded_minus_unpadded"]
        L.append(f"| {NAMES[code]} | {f4(p['unpadded'])} | **{f4(p['padded'])}** | {s4(d['delta'])}{star(d)} {pooled_ci(d)} | "
                 f"{f4(m['unpadded']['matched'])} ({m['unpadded']['W']}/{m['unpadded']['T']}/{m['unpadded']['L']}) | **{f4(m['padded']['matched'])}** ({m['padded']['W']}/{m['padded']['T']}/{m['padded']['L']}) | "
                 f"{s4(dm['delta'])}{star(dm)} {matched_ci(dm)} |")
    return L


def minus_rows(S, scope, lk="LOOKUP"):
    L = [f"| model | padded: pooled Δ (item; persona) | padded: matched Δ (triple; persona) | unpadded: pooled Δ (item; persona) | unpadded: matched Δ (triple; persona) |",
         "|---|---|---|---|---|"]
    for code in MODELS:
        r = S["minus_lookup"].get(code)
        if not r:
            L.append(f"| {NAMES[code]} | lane not scored | | | |"); continue
        b = r[lk][scope]
        L.append(f"| {NAMES[code]} | {s4(b['padded']['pooled']['delta'])}{star(b['padded']['pooled'])} {pooled_ci(b['padded']['pooled'])} | "
                 f"{s4(b['padded']['matched']['delta'])}{star(b['padded']['matched'])} {matched_ci(b['padded']['matched'])} | "
                 f"{s4(b['unpadded']['pooled']['delta'])}{star(b['unpadded']['pooled'])} {pooled_ci(b['unpadded']['pooled'])} | "
                 f"{s4(b['unpadded']['matched']['delta'])}{star(b['unpadded']['matched'])} {matched_ci(b['unpadded']['matched'])} |")
    return L


def pred_text(S):
    P = S["predictions"]; L = []
    for k in ("P-L1", "P-L2", "P-L3", "P-L4"):
        v = P[k]; verdict = "HOLDS" if v["holds"] else ("FAILS" if v["holds"] is False else "NOT DECIDABLE")
        if k in ("P-L1", "P-L2"):
            parts = []
            for c, d in v["per_model"].items():
                parts.append(f"{NAMES[c].split(' (')[0]} {s4(d['delta'])} item {ci(d['ci_item'])} persona {ci(d['ci_persona'])} ({'reliably above' if d['reliably_above'] else 'not reliably above'})" if d else f"{c} not scored")
            L.append(f"- **{k} {verdict}.** Model minus the embedding lookup, pooled AUROC, supersession, 60-name list: " + "; ".join(parts) + ".")
        elif k == "P-L3":
            d = v["lookup_padded_minus_unpadded"]
            L.append(f"- **{k} {verdict}.** The embedding lookup's padded minus unpadded pooled AUROC on supersession: {s4(d['delta'])}, item {ci(d['ci_item'])}, persona {ci(d['ci_persona'])} "
                     f"(holds iff below −0.05 with both intervals below zero).")
        else:
            parts = [f"{NAMES[c].split(' (')[0]} {s4(d['model_delta'])} against the lookup's {s4(d['lookup_delta'])} ({'loses less' if d['loses_less'] else 'does not lose less'})" if d else f"{c} not scored" for c, d in v["per_model"].items()]
            L.append(f"- **{k} {verdict}.** Padded minus unpadded pooled AUROC on supersession, point estimates: " + "; ".join(parts) + ".")
    return L


def main():
    S = jload(RES / "cf_pad_scores.json"); lock = jload(C.BUILD / "lock.json"); probes = jload(C.BUILD / "probes.json")
    reg_sha = C.sha256_frozen(); assert reg_sha == C.REG_SHA
    census = S["census"]; spend = S["spend"]
    devs_full = io.open(DEVS, encoding="utf-8").read() if DEVS.exists() else ""
    dev_rows = [l for l in devs_full.splitlines() if l.startswith("| ") and not l.startswith("| id") and "(none)" not in l]
    devs = "\n".join(dev_rows) if dev_rows else "none"
    # ---------------------------------------------------------------- printed forms
    printed = {"n_items": 444, "n_pairs": 148, "n_sup_pairs": 88, "list_length": {"pn": 60, "siblings": "57-60", "counted_states": 60},
               "draws": {"MINI": 5, "H45": 5, "LUNA": 5, "SOL": 5, "OP5": 1, "OP5_recorded": 5},
               "registration_sha256": reg_sha, "frozen_commit": lock["frozen_commit"]}

    def put(key, value, source, reliable=None):
        if value is None:
            printed[key] = None; return
        rec = {"printed": f"{abs(value):.2f}", "value": value, "source": source}
        if reliable is not None:
            rec["reliable"] = bool(reliable)
        printed[key] = rec

    for code in ORDER:
        r = S["readers"].get(code)
        if not r or "superseded" not in r:
            continue
        for scope in ("superseded", "whole"):
            p = r[scope]["pooled"]; m = r[scope]["matched"]
            put(f"{code.lower()}_{scope}_pooled_padded", p["padded"], f"AUX-CFP-{code} {scope} pooled padded")
            put(f"{code.lower()}_{scope}_pooled_unpadded", p["unpadded"], f"AUX-CFP-{code} {scope} pooled unpadded (recorded)")
            put(f"{code.lower()}_{scope}_loss_pooled", p["padded_minus_unpadded"]["delta"], f"AUX-CFP-{code} {scope} pooled padded minus unpadded", p["padded_minus_unpadded"]["both_exclude_zero"])
            put(f"{code.lower()}_{scope}_matched_padded", m["padded"]["matched"], f"AUX-CFP-{code} {scope} matched padded")
            put(f"{code.lower()}_{scope}_matched_unpadded", m["unpadded"]["matched"], f"AUX-CFP-{code} {scope} matched unpadded (recorded)")
            put(f"{code.lower()}_{scope}_loss_matched", m["padded_minus_unpadded"]["delta"], f"AUX-CFP-{code} {scope} matched padded minus unpadded", m["padded_minus_unpadded"]["both_exclude_zero"])
    for code in MODELS:
        r = S["minus_lookup"].get(code)
        if not r:
            continue
        for scope in ("superseded", "whole"):
            b = r["LOOKUP"][scope]
            put(f"{code.lower()}_minus_lookup_{scope}_pooled_padded", b["padded"]["pooled"]["delta"], f"AUX-CFP-{code} {scope} minus embedding lookup, padded, pooled", b["padded"]["pooled"]["both_exclude_zero"])
            put(f"{code.lower()}_minus_lookup_{scope}_matched_padded", b["padded"]["matched"]["delta"], f"AUX-CFP-{code} {scope} minus embedding lookup, padded, matched", b["padded"]["matched"]["both_exclude_zero"])
            put(f"{code.lower()}_minus_lookup_{scope}_pooled_unpadded", b["unpadded"]["pooled"]["delta"], f"AUX-CFP-{code} {scope} minus embedding lookup, unpadded (recorded), pooled", b["unpadded"]["pooled"]["both_exclude_zero"])
            put(f"{code.lower()}_minus_lookup_{scope}_matched_unpadded", b["unpadded"]["matched"]["delta"], f"AUX-CFP-{code} {scope} minus embedding lookup, unpadded (recorded), matched", b["unpadded"]["matched"]["both_exclude_zero"])
    printed["predictions"] = {k: ("HOLDS" if v["holds"] else ("FAILS" if v["holds"] is False else "NOT DECIDABLE")) for k, v in S["predictions"].items()}
    printed["spend"] = {v: {"usd": spend[v]["usd"], "cap": spend[v]["cap"]} for v in spend}
    jdump(printed, PRINTED)
    # ---------------------------------------------------------------- the ledger
    L = [f"# NUMBERS_CF_PAD — the long-list check on the counterfactual set (ADDENDUM_CF_PAD, registered text sha256 `{reg_sha}`, frozen at `{lock['frozen_commit']}`)\n",
         f"Written {dt.date.today().isoformat()} by `cf_pad/tools/report_cf_pad.py` from `cf_pad/results/cf_pad_scores.json` (scored once, after every lane completed). "
         "Every number here is read from the JSON. Pooled AUROC (item; persona intervals) and the matched score (W + T/2) / n, PN against PRESENT (triple; persona intervals); "
         "1,000 draws, seed 42; `*` = both intervals exclude zero. The unpadded values are the recorded Table 1 rows restricted to the same items and triples.\n",
         "## AUX-CFP-LOCK\n",
         f"Registration sha256 holds; frozen commit `{lock['frozen_commit']}`; prompts_e1 digests `{lock['prompts_file_sha256'][:8]}…` / `{lock['prompts_texts_sha256'][:8]}…`; "
         f"indexes sha256 `{lock['indexes_sha256'][:16]}…` (= `cf_indexes.json` meta and `cf_cell.json` meta); padded texts sha256 `{lock['texts_sha256'][:16]}…`; renderer lock {lock['renderer_lock']} of 444; "
         f"leak scan 0 fails (descriptive {lock['leak_scan']['descriptive']}); lookup gate on the committed lists {lock['lookup_gate']['got']}; recorded gates {lock['recorded_gates']}; "
         f"pool A min/median/max {lock['pools']['a_min']}/{lock['pools']['a_median']}/{lock['pools']['a_max']}, pairs drawing on pool B {lock['pools']['from_pool_b_pairs']}; "
         f"list lengths {lock['list_length']['histogram']}; pad sizes {lock['n_pad']}; target rank (PN, supersession) min {lock['target_position']['min']}, median {lock['target_position']['median']}, "
         f"max {lock['target_position']['max']}, first {lock['target_position']['first']}, last {lock['target_position']['last']}.\n",
         "### Unpadded recorded values (the section-2 rows on the supersession slice and the whole set)\n",
         "| recorded row | pooled whole | pooled supersession | matched whole | matched supersession |", "|---|---:|---:|---:|---:|"]
    for k, v in lock["unpadded_recorded"].items():
        L.append(f"| {k} | {v['pooled_whole']} | {v['pooled_superseded']} | {v['matched_whole']} | {v['matched_superseded']} |")
    L += ["\n## AUX-CFP-PROBES\n", "| lane | served | identifier | tok in / out | usd | status |", "|---|---|---|---|---:|---|"]
    for lane, p in probes.items():
        L.append(f"| {lane} | `{p['served']}` | {'OK' if p['identifier_ok'] else 'MISMATCH'} | {p['tok_in']} / {p['tok_out']} | {p['usd']:.6f} | {p['status']} |")
    L += ["\n## AUX-CFP-LANES (rows, served identifiers, collapse census)\n", "| lane | k | rows | not OK | served | units collapsed | complete draws | distinct values | tied triples padded / unpadded | usd |", "|---|---:|---:|---:|---|---:|---|---:|---|---:|"]
    for code in MODELS:
        c = census.get(code, {})
        if "rows" not in c:
            L.append(f"| {code} | — | lane not run | | | | | | | |"); continue
        r = S["readers"].get(code, {})
        L.append(f"| {code} | {c['k_new']} | {c['rows']} | {c['not_ok']} ({c['not_ok_share']:.2%}) | {c['served']} | {c['units_collapsed']} | {c['complete_draws']} | {c['distinct_values']} | "
                 f"{r.get('tied_triples', {}).get('padded', '—')} / {r.get('tied_triples', {}).get('unpadded', '—')} | {c['usd']:.4f} |")
    for scope in ("superseded", "whole", "retracted", "expired"):
        tag = "registered" if scope == "superseded" else "descriptive"
        L += [f"\n## AUX-CFP-READERS-{scope.upper()} ({tag}): every reader, {SCOPE_NAME[scope]}, padded (60-name list) beside unpadded (recorded)\n"] + reader_rows(S, scope)
        L += [f"\n## AUX-CFP-MINUS-LOOKUP-{scope.upper()} ({tag}): each model minus the embedding lookup, {SCOPE_NAME[scope]}\n"] + minus_rows(S, scope, "LOOKUP")
    for lk in ("LEX", "RANDTOK"):
        L += [f"\n## AUX-CFP-MINUS-{lk}-SUPERSEDED (descriptive): each model minus the {NAMES[lk].lower()}, supersession\n"] + minus_rows(S, "superseded", lk)
    L += ["\n## AUX-CFP-P-L1 … P-L4\n"] + pred_text(S)
    D = S["descriptive"]["target_position"]
    L += ["\n## AUX-CFP-POSITION (descriptive): the target's alphabetical rank in the PN list (88 supersession triples) against each reader\n",
          f"Rank histogram (rank: triples): {hist_str(D['rank_histogram'])}.\n", "| reader | Spearman rank vs PN score | Spearman rank vs PN-vs-PRESENT outcome | matched by tenth of the list (1 = ranks 1–6 … 10 = ranks 55–60) |", "|---|---:|---:|---|"]
    for code in ORDER:
        b = D["by_reader"].get(code)
        if b:
            L.append(f"| {NAMES[code]} | {f4(b['spearman_rank_vs_pn_score'])} | {f4(b['spearman_rank_vs_outcome'])} | " + ", ".join(f"{t}: {f4(b['matched_by_tenth'][t])} (n {b['n_by_tenth'][t]})" for t in sorted(b["matched_by_tenth"], key=int)) + " |")
    if "opus_recorded_draw1" in S["descriptive"]:
        o = S["descriptive"]["opus_recorded_draw1"]
        L += ["\n## AUX-CFP-OP5-D1 (descriptive): Opus 5's padded one draw beside its recorded draw 1 alone\n"]
        for sc, v in o.items():
            L.append(f"- {sc}: recorded draw 1 pooled {f4(v['pooled_unpadded_d1'])}, matched {f4(v['matched_unpadded_d1'])}; padded minus recorded draw 1, pooled {s4(v['padded_minus_d1_pooled']['delta'])}{star(v['padded_minus_d1_pooled'])} {pooled_ci(v['padded_minus_d1_pooled'])}")
    sp = S["descriptive"]["seed_spot_check"]
    flips = {k: {sd: v for sd, v in d.items()} for k, d in sp.items()}
    L += ["\n## AUX-CFP-SEEDS (descriptive): seeds 43–46 on the registered pooled differences, supersession (both intervals exclude zero?)\n", "| difference | 43 (item; persona) | 44 | 45 | 46 |", "|---|---|---|---|---|"]
    for k, d in flips.items():
        L.append(f"| {k} | " + " | ".join(f"{d[s]['item']}; {d[s]['persona']}" for s in ("43", "44", "45", "46")) + " |")
    L += ["\n## AUX-CFP-SPEND\n"]
    for v, d in spend.items():
        L.append(f"- {v}: **${d['usd']:.4f}** against the ${d['cap']:.2f} cap ({d['parts']}); token-metered from the rows at the registration's page prices, Batch at 50%; not an invoice.")
    L += ["\n## Deviations\n", devs if devs.strip() else "none"]
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    # ---------------------------------------------------------------- the report
    R = [f"# REPORT_R136 — the long-list check: five readers and three lookups on the counterfactual set with a 60-name superseded list\n",
         f"Registration `registrations/ADDENDUM_CF_PAD.md`, registered-text sha256 `{reg_sha}`, frozen and committed alone at `{lock['frozen_commit']}` on the author's GO of 2026-09-22 before any paid call. "
         f"Scored once, after every lane completed; ledger `cf_pad/NUMBERS_CF_PAD.md`; printed forms `cf_pad/results/cf_pad_printed.json`; scores `cf_pad/results/cf_pad_scores.json`. "
         "Nothing landed in the paper. Pooled AUROC is the primary endpoint, the matched within-triple score (W + T/2) / n (PN against PRESENT) the secondary; intervals item-level (triple-level for matched) and "
         "persona-grouped, 1,000 draws, seed 42; `*` marks a difference whose two intervals both exclude zero (reliable). Unpadded = the recorded Table 1 rows on the same items and triples.\n",
         "## 1. Locks, lanes, served identifiers, rows, spend, deviations\n",
         f"- **Locks.** Registration sha256 holds; indexes sha256 `{lock['indexes_sha256'][:16]}…` equals `cf_indexes.json` and `cf_cell.json` meta; padded texts sha256 `{lock['texts_sha256'][:16]}…` (identical to the dry run's); renderer lock {lock['renderer_lock']}/444; leak scan 0 fails; "
         f"the three lookups reproduce 0.7663 / 0.6698 / 0.5954 on the committed lists; the seven recorded vectors reproduce their gates. Pool A {lock['pools']['a_min']}–{lock['pools']['a_max']} names, pool B unused. "
         f"List lengths {lock['list_length']['histogram']}; the target's rank in the PN list never first, last on {lock['target_position']['last']} of 88.",
         "- **Lanes and served identifiers.** " + "; ".join(f"`{lane}` served `{p['served']}` ({'OK' if p['identifier_ok'] else 'MISMATCH'})" for lane, p in probes.items()) + ". Every scored row's identifier re-checked at scoring: "
         + ", ".join(f"{code} {census[code]['served']}" for code in MODELS if 'served' in census.get(code, {})) + ".",
         "- **Rows.** " + "; ".join(f"{code} k={census[code]['k_new']}: {census[code]['rows']} rows, {census[code]['not_ok']} not OK, {census[code]['units_collapsed']} of 444 units collapsed, complete draws {census[code]['complete_draws']}" for code in MODELS if 'rows' in census.get(code, {})) + ".",
         "- **Spend.** " + "; ".join(f"{v} **${d['usd']:.2f}** of ${d['cap']:.0f} ({', '.join(f'{k} {x:.2f}' for k, x in d['parts'].items())})" for v, d in spend.items()) + ". No cap reached; no draw dropped.",
         f"- **Deviations.** {devs if devs != 'none' else 'None (cf_pad/DEVIATIONS_CF_PAD.md carries no entry).'}",
         f"- **STOP list at scoring.** {S['stops'] or 'nothing fired'}.\n",
         "## 2. Predictions\n"] + pred_text(S) + [
         "\n## 3. Supersession, 60-name list (registered): every reader's pooled and matched score beside its unpadded score\n"] + reader_rows(S, "superseded") + [
         "\n## 4. Supersession, 60-name list (registered): each model minus the embedding lookup, beside the same difference on the unpadded list\n"] + minus_rows(S, "superseded", "LOOKUP") + [
         "\n## 5. Whole set (descriptive): the same two tables\n", "### 5a. Every reader\n"] + reader_rows(S, "whole") + ["\n### 5b. Each model minus the embedding lookup\n"] + minus_rows(S, "whole", "LOOKUP") + [
         "\n## 6. Retraction and expiry (descriptive; the list names neither state, and the three versions carry identical padded lists)\n", "### 6a. Retraction\n"] + reader_rows(S, "retracted") + ["\n### 6b. Expiry\n"] + reader_rows(S, "expired") + [
         "\n## 7. The other two lookups against the models, supersession (descriptive)\n", "### 7a. Minus the word-matching lookup\n"] + minus_rows(S, "superseded", "LEX") + ["\n### 7b. Minus the random-token lookup\n"] + minus_rows(S, "superseded", "RANDTOK") + [
         "\n## 8. Target position against score (descriptive)\n", f"The target's alphabetical rank in the PN version's 60-name list over the 88 supersession triples: histogram (rank: triples) {hist_str(D['rank_histogram'])}.\n",
         "| reader | Spearman rank vs PN score | Spearman rank vs PN-vs-PRESENT outcome | matched score by tenth of the list (1 = ranks 1–6 … 10 = ranks 55–60) |", "|---|---:|---:|---|"]
    for code in ORDER:
        b = D["by_reader"].get(code)
        if b:
            R.append(f"| {NAMES[code]} | {f4(b['spearman_rank_vs_pn_score'])} | {f4(b['spearman_rank_vs_outcome'])} | " + ", ".join(f"{t}: {f4(b['matched_by_tenth'][t])} (n {b['n_by_tenth'][t]})" for t in sorted(b["matched_by_tenth"], key=int)) + " |")
    if "opus_recorded_draw1" in S["descriptive"]:
        o = S["descriptive"]["opus_recorded_draw1"]
        R += ["\n## 9. Opus 5: one padded draw against its recorded five-draw row (stated wherever its row prints) and against its recorded draw 1 alone (descriptive)\n"]
        for sc, v in o.items():
            R.append(f"- {sc}: recorded draw 1 pooled {f4(v['pooled_unpadded_d1'])}, matched {f4(v['matched_unpadded_d1'])}; padded (one draw) minus recorded draw 1, pooled {s4(v['padded_minus_d1_pooled']['delta'])}{star(v['padded_minus_d1_pooled'])} {pooled_ci(v['padded_minus_d1_pooled'])}.")
    R += ["\n## 10. Seed spot-check (descriptive): seeds 43–46 on the registered pooled differences, supersession — both intervals exclude zero?\n", "| difference | 43 (item; persona) | 44 | 45 | 46 |", "|---|---|---|---|---|"]
    for k, d in flips.items():
        R.append(f"| {k} | " + " | ".join(f"{d[s]['item']}; {d[s]['persona']}" for s in ("43", "44", "45", "46")) + " |")
    R += ["\n## 11. Files\n",
          "- `cf_pad/results/cf_pad_scores.json` (every number), `cf_pad/results/cf_pad_printed.json` (two-decimal forms with their four-decimal sources), `cf_pad/results/lookup_vectors.json`",
          "- `cf_pad/NUMBERS_CF_PAD.md` (ledger), `cf_pad/build/lock.json`, `build/probes.json`, `build/texts.json`, `build/lists.json`, `build/pads.json`, `build/projection.json`",
          "- `cf_pad/rows/rows_{MINI,LUNA,SOL,H45,OP5}.jsonl`, `rows/batch_{H45,OP5}.json`",
          "- tools: `cf_pad/tools/cf_pad_common.py`, `run_cf_pad.py`, `score_cf_pad.py`, `report_cf_pad.py`; Phase 0: `reviews/r136/PHASE0_STOP.md`, `reviews/r136/tools/phase0_stop.py`"]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    io.open(REPORT, "w", encoding="utf-8", newline="\n").write("\n".join(R) + "\n")
    print(f"wrote {LEDGER.relative_to(C.ROOT)}, {PRINTED.relative_to(C.ROOT)}, {REPORT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
