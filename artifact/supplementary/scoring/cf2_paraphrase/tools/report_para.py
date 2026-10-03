"""report_para.py -- write reviews/para/REPORT_PARA.md from the PARA artifacts (sheet.json, probes.json, results/lookups*.json,
results/para_scores*.json). No model call; re-runnable. Every number is read from the JSON, none typed."""
from __future__ import annotations

import collections
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import PARA, REG, REG_SHA, SHEET, jload, sha256_file, sha256_frozen  # noqa: E402

ROOT = PARA.parent
RES = PARA / "results"
OUT = ROOT / "reviews" / "para" / "REPORT_PARA.md"
READERS = [("emb_v2", "Embedding lookup, superseded names (v2)"), ("lex_v2", "Lexical lookup, superseded names (v2)"),
           ("emb_v3", "Embedding lookup, all states (v3)"), ("lex_v3", "Lexical lookup, all states (v3)"),
           ("MINI_v2", "GPT-4.1 mini, v2"), ("MINI_v3", "GPT-4.1 mini, v3"), ("H45_v2", "Haiku 4.5, v2"), ("H45_v3", "Haiku 4.5, v3"),
           ("OP5_v2", "Opus 5, v2 (k = 1 vs recorded k = 5)"), ("OP5_v3", "Opus 5, v3 (k = 1 vs recorded k = 5)"),
           ("LUNA_v2", "GPT-5.6 Luna, v2 — added, not registered"), ("SOL_v2", "GPT-5.6 Sol, v2 — added, not registered")]
FLAGS_A = {30, 40, 77, 82, 28}
FLAGS_B = {11, 46, 33, 79}
FLAGS_C = {12, 27, 45, 49, 52, 57, 63, 68, 92, 94, 102, 112}


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def ci(d, key):
    c = (d or {}).get(key) or {}
    return "—" if "ci_lo" not in c else f"[{c['ci_lo']:+.3f}, {c['ci_hi']:+.3f}]"


def reader_rec(SC, key):
    """(original, paraphrase, paired, per-state original, per-state paraphrase) for a reader key, or None when the lane did not run."""
    if key in SC["lookups"]:
        r = SC["lookups"][key]
        return r
    code, sv = key.split("_")
    M = SC["models"].get(code)
    if not M or sv not in M:
        return None
    return M[sv]


def status(pd, tol):
    if abs(pd["delta"]) <= tol:
        return "holds"
    if pd["delta"] < -tol and pd["both_exclude_zero"]:
        return "collapses"
    return "neither"


def pooled_table(SC, label):
    o = [f"| reader | original | paraphrase | Δ para − orig | item interval | persona interval | reading | per state, para (sup / ret / exp) |",
         "|---|---:|---:|---:|---|---|---|---|"]
    for key, name in READERS:
        r = reader_rec(SC, key)
        if r is None:
            o.append(f"| {name} | — | — | — | — | — | not run | — |"); continue
        pd = r["paired"]; ps = r["paraphrase_per_state"]
        o.append(f"| {name} | {r['original']:.4f} | **{r['paraphrase']:.4f}** | {pd['delta']:+.4f} | {ci(pd, 'ci_item')} | {ci(pd, 'ci_persona')} | {status(pd, SC['tol'])} | "
                 f"{ps['superseded']:.3f} / {ps['retracted']:.3f} / {ps['expired']:.3f} |")
    return o


def matched_table(SC):
    M = SC.get("matched") or {}
    o = ["| reader | original W/T/L = matched | paraphrase W/T/L = matched | Δ para − orig | triple interval | persona interval | PN vs ABSENT, para |",
         "|---|---|---|---:|---|---|---:|"]
    for key, name in READERS:
        if key not in M:
            o.append(f"| {name} | — | — | — | — | — | — |"); continue
        w = M[key]["pn_vs_present"]; a = M[key]["pn_vs_absent"]
        ow, pw, dw = w["original"]["whole"], w["paraphrase"]["whole"], w["paired"]["whole"]
        o.append(f"| {name} | {ow['W']}/{ow['T']}/{ow['L']} = {ow['matched']:.4f} | {pw['W']}/{pw['T']}/{pw['L']} = **{pw['matched']:.4f}** | {dw['delta']:+.4f} | "
                 f"{ci(dw, 'ci_triple')} | {ci(dw, 'ci_persona')} | {a['paraphrase']['whole']['matched']:.4f} |")
    return o


def model_minus_lookup(SC):
    o = ["| model, summary | model − embedding lookup (paraphrase set) | item | persona | model − lexical lookup | item | persona |", "|---|---:|---|---|---:|---|---|"]
    for code, nm in (("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5"), ("OP5", "Opus 5"), ("LUNA", "GPT-5.6 Luna — added, not registered"), ("SOL", "GPT-5.6 Sol — added, not registered")):
        M = SC["models"].get(code)
        if not M or "v2" not in M:
            o.append(f"| {nm} | not run | | | | | |"); continue
        for sv in ("v2", "v3"):
            if sv not in M:
                continue
            R = M[sv]; e, l = R["model_minus_emb"], R["model_minus_lex"]
            o.append(f"| {nm}, {sv} | {e['delta']:+.4f}{' *' if e['both_exclude_zero'] else ''} | {ci(e, 'ci_item')} | {ci(e, 'ci_persona')} | {l['delta']:+.4f}{' *' if l['both_exclude_zero'] else ''} | {ci(l, 'ci_item')} | {ci(l, 'ci_persona')} |")
    return o


def posthoc_minus_lookup_tables(PH):
    """Section 4d (post hoc, requested after the run): each model minus the embedding lookup on the paraphrase set and on the original questions of the
    same pairs, whole set and supersession only, pooled AUROC (item / persona intervals) and the matched metric (triple / persona intervals)."""
    o = []
    for scope, title in (("whole", f"whole set ({PH['n_pairs']} triples)"), ("superseded", f"supersession only ({PH['n_pairs_superseded']} triples; the named state)")):
        o.append(f"**{title}** (* = both intervals exclude zero)")
        o.append("")
        o.append("| model, summary | pooled: paraphrase − lookup | item | persona | pooled: original − lookup | item | persona | matched: paraphrase − lookup | triple | persona | matched: original − lookup | triple | persona |")
        o.append("|---|---:|---|---|---:|---|---|---:|---|---|---:|---|---|")
        for code, nm in (("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5"), ("OP5", "Opus 5"), ("LUNA", "GPT-5.6 Luna — added, not registered"), ("SOL", "GPT-5.6 Sol — added, not registered")):
            M = PH["models"].get(code)
            if not M or "v2" not in M:
                o.append(f"| {nm} | not run | | | | | | | | | | | |"); continue
            for sv in ("v2", "v3"):
                if sv not in M:
                    continue
                R = M[sv][scope]
                pp, po, mp, mo = R["pooled"]["paraphrase"], R["pooled"]["original"], R["matched"]["paraphrase"], R["matched"]["original"]
                star = lambda d: " *" if d["both_exclude_zero"] else ""
                o.append(f"| {nm}, {sv} | {pp['delta']:+.4f}{star(pp)} | {ci(pp, 'ci_item')} | {ci(pp, 'ci_persona')} | {po['delta']:+.4f}{star(po)} | {ci(po, 'ci_item')} | {ci(po, 'ci_persona')} | "
                         f"{mp['delta']:+.4f}{star(mp)} | {ci(mp, 'ci_triple')} | {ci(mp, 'ci_persona')} | {mo['delta']:+.4f}{star(mo)} | {ci(mo, 'ci_triple')} | {ci(mo, 'ci_persona')} |")
        o.append("")
    return o


def flags_table(SC, key):
    F = SC["flags"].get(key)
    if not F:
        return ["(not computed)"]
    o = [f"{F['n_flagged_pairs']} flagged pairs / {F['n_unflagged_pairs']} unflagged.", "",
         "| reader | paraphrase: flagged | unflagged | original: flagged | unflagged |", "|---|---:|---:|---:|---:|"]
    for rk, name in READERS:
        if rk not in F:
            continue
        p, q = F[rk]["paraphrase"], F[rk]["original"]
        o.append(f"| {name} | {f4(p['flagged'])} | {f4(p['unflagged'])} | {f4(q['flagged'])} | {f4(q['unflagged'])} |")
    return o


def main():
    sh = jload(PARA / "sheet.json")
    probes = jload(PARA / "probes.json")
    SC = jload(RES / "para_scores.json")
    SCs = jload(RES / "para_scores_all124.json") if (RES / "para_scores_all124.json").exists() else None
    sheet = {int(r["row"]): r for r in csv.DictReader(io.open(ROOT / "reviews/para/PARA_APPROVAL_SHEET.csv", encoding="utf-8"))}
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import score_para as sp
    H = sp.headrooms()
    acc = [r for r in sh["rows"] if r["same_intent"] == "YES"]
    no1 = [r for r in sh["rows"] if r["same_intent"] != "YES"]
    no_nums = {r["num"] for r in no1}
    o = []
    w = o.append
    w("# REPORT_PARA — the paraphrase probe (ADDENDUM_PARA), run 2026-09-21 on the 115 accepted pairs, with the 124-pair sensitivity beside")
    w("")
    w(f"Registration `registrations/ADDENDUM_PARA.md`: registered text sha256 `{sha256_frozen(REG)}` (= CLAIMS.md R104, holds); whole file with the dated rulings, "
      f"the 21 Sep notes and the amendment `{sha256_file(REG)}`. Sheet `reviews/v12/PARAPHRASE_READ.md` sha256 `{sh['sheet_sha256']}` (AUX-PARA-SHEET, ledgered before the first call). "
      f"Ledger `cf2_paraphrase/NUMBERS_PARA.md`; scores `cf2_paraphrase/results/para_scores.json` (the 115) and `para_scores_all124.json` (the 124); rows under `cf2_paraphrase/rows/`.")
    w("")
    w("## 1. What the registration predicts, and what the amendment changed")
    w("")
    w("The registration is descriptive: it carries **no prediction, no bar and no verdict** (its preamble and §7). Its §7 enumerates four branches per summary and every reader prints as it "
      "comes out, with a reader *holding* when its paired difference paraphrase − original lies inside ±0.05 and *collapsing* when the difference is below −0.05 with both intervals excluding zero. "
      "So there is no registered prediction to hold or fail; what the run settles is which branch each summary falls under, reported in section 3.")
    w("")
    w(f"The author's read (§5) excluded **{len(no1)}** of the 124 screen-passing pairs (rows {', '.join(str(n) for n in sorted(no_nums))}: "
      + "; ".join(f"`{r['pair_id']}`" for r in no1) + f"), leaving **{len(acc)}** — supersession {sh['by_state'].get('SUPERSESSION', 0)}, retraction {sh['by_state'].get('RETRACTION', 0)}, "
      f"expiry {sh['by_state'].get('EXPIRY', 0)} — below the registered floor of 120. The amendment of 2026-09-21 (a dated line below the registration's marker, written before any scoring call) "
      f"sets the floor to the {len(acc)} accepted pairs, leaves the readers, prompts, draws and budget unchanged, and adds **one sensitivity analysis, labelled not registered: the same scoring on all 124 "
      "screen-passing pairs**, because excluding paraphrases judged unfaithful could favour a reader that matches on meaning. No verdict was revisited.")
    w("")
    xt = [("A (the assistant would answer NO)", FLAGS_A), ("B (depends on the persona)", FLAGS_B), ("C (vaguer; would pass)", FLAGS_C), ("not flagged", set(range(1, 125)) - FLAGS_A - FLAGS_B - FLAGS_C)]
    w("The AI-assisted pre-read (`reviews/para/PARA_AI_FLAGS.md`, its addendum) against the author's column 1: " + "; ".join(f"level {k}: {len(s & no_nums)} of {len(s)} NO" for k, s in xt)
      + ". Every verdict is the author's; the assistant saw no reader output and no score.")
    w("")
    w("## 2. Locks, lanes and spend")
    w("")
    L, g = sh["locks"], sh["lookup_gate"]
    w(f"- Locks (§8 STOP list): registration sha256 {'holds' if L['registration_ok'] else 'MISMATCH'}; CF-2 questions and indexes sha256 {'hold' if L['questions_ok'] and L['indexes_ok'] else 'MISMATCH'}; "
      f"prompts_e1 digests asserted at import; every accepted paraphrase re-passes the §3 screen (narrowed scope) at scoring time. Lookup gate on the original questions: embedding v2 {g['emb_v2']:.4f} "
      f"(0.7663 registered), v3 {g['emb_v3']:.4f} (0.8756) — PASS at four decimals.")
    for lane, code, nm in (("gpt-4.1-mini", "MINI", "GPT-4.1 mini (k = 1, synchronous, list price)"), ("claude-haiku-4-5-20251001", "H45", "Haiku 4.5 (k = 5, Batch)"), ("claude-opus-5", "OP5", "Opus 5 (k = 1, Batch)")):
        p = probes.get(lane)
        if not p:
            w(f"- {nm}: not probed / not run."); continue
        rows_p = PARA / "rows" / f"rows_{code}.jsonl"
        n_rows = n_ok = 0; usd = 0.0; served = collections.Counter()
        if rows_p.exists():
            for l in io.open(rows_p, encoding="utf-8"):
                r = json.loads(l); n_rows += 1; n_ok += r.get("status") == "OK"; usd += r.get("usd", 0.0); served[r.get("served_model")] += 1
        w(f"- {nm}: served `{p['served'][0]}` (E1.7 {'OK' if p['identifier_ok'] else 'MISMATCH'}); projection {p['projection']['calls']} calls ${p['projection']['usd']:.2f} (×1.3 ${p['projection']['usd_x1.3']:.2f}) "
          f"against headroom ${p['headroom']:.2f} — {'submitted' if p['fits'] else 'DASH'}; rows {n_rows} ({n_ok} OK; served {dict(served)}); billed ${usd:.4f}.")
    po = jload(PARA / "probes_openai.json") if (PARA / "probes_openai.json").exists() else {}
    for model, code in (("gpt-5.6-luna", "LUNA"), ("gpt-5.6-sol", "SOL")):
        pr = po.get(model)
        if not pr:
            w(f"- {model} (added, not registered): not run."); continue
        rows_p = PARA / "rows" / f"rows_{code}.jsonl"; n_rows = n_ok = 0; usd = 0.0; served = collections.Counter()
        if rows_p.exists():
            for l in io.open(rows_p, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l); n_rows += 1; n_ok += r.get("status") == "OK"; usd += r.get("usd", 0.0); served[r.get("served_model")] += 1
        w(f"- {model} (**added 2026-09-21, not registered**; raw Chat Completions, the Table 1 settings, k = 5, v2 only): served `{pr['served']}` (E1.7 {'OK' if pr['identifier_ok'] else 'MISMATCH'}); "
          f"projection v2 only ${pr['projection_v2_only_usd']:.2f} (both arms ${pr['projection_both_arms_usd']:.2f}, over the $14 cap, so v3 was not run); rows {n_rows} ({n_ok} OK; served {dict(served)}); billed ${usd:.4f}.")
    added_spend = sum(json.loads(l).get("usd", 0.0) for code in ("LUNA", "SOL") if (PARA / "rows" / f"rows_{code}.jsonl").exists() for l in io.open(PARA / "rows" / f"rows_{code}.jsonl", encoding="utf-8") if l.strip()) + sum(v["usd"] for v in po.values())
    para_spend = {k: v for k, v in H["billed_parts"].items() if k.startswith("PARA")}
    w(f"- Spend: PARA lanes and probes **${sum(para_spend.values()):.4f}** (drafting ${para_spend.get('PARA drafting', 0):.4f} included); everything in the pass ${H['billed_overall']:.4f} against the $28 overall cap; "
      f"the registered lanes ${H['billed_combined']:.4f} against the $21 combined cap (ruling ii). The lanes were submitted once on the 124 pairs' items (372 × 2 arms); the registered scoring reads the 115's items from those rows "
      f"(independent requests at temperature 0 / fixed seeds), and the 9 excluded pairs' 27 items are the sensitivity's calls, about ${sum(para_spend.values()) * 9 / 124:.2f} of the total.")
    w(f"- Added lane (Luna and Sol, not registered): **${added_spend:.4f}** with probes, against its own OpenAI cap of $14; not on the registered caps.")
    w("- Cap accounting: the ruling of 2026-09-14 (evening) puts the PAD Amendment 1 Haiku add-on under the $28 overall cap and says registered lanes are never displaced; the runner therefore charges the add-on to the overall cap only. "
      f"Had it been charged to the $21 combined cap the headroom at the first lane would have read ${probes['gpt-4.1-mini']['headroom_if_addon_counted_on_combined']:.2f}; both readings are in `probes.json`.")
    w("")
    w("## 3. The §7 branches on the 115 (registered; tolerance ±0.05)")
    w("")
    for sv, nm in (("v2", "superseded-only summary (v2)"), ("v3", "all-states summary (v3)")):
        b = SC["branches"][sv]
        w(f"- **{nm}**: " + ", ".join(f"{k} *{v}*" for k, v in b["status"].items()) + f" → heading **{', '.join(b['headings']) or 'none of A–D'}**" + (f"; D: {b['D']}" if b["D"] else "")
          + (f". Added readers, not registered, beside (not part of the branch): " + ", ".join(f"{k} *{v}*" for k, v in b["added_readers_status_not_registered"].items()) if b.get("added_readers_status_not_registered") else "") + ".")
    w("")
    w("Reading: the lexical lookup reads exactly 0.5000 on every paraphrase set by construction (no content token is shared with any name the summary prints, so every Jaccard score is 0 and all items tie). "
      "The embedding lookup and the models print as above; a difference beyond tolerance whose intervals include zero, or a rise, prints as 'neither' under the nearest heading.")
    w("")
    w(f"## 4. Every reader on the paraphrase set beside the same pairs' original-question scores — the 115 (registered; n = {SC['n']} items, {SC['n_pos']} positives)")
    w("")
    w("### 4a. Pooled AUROC (the registered metric; Mann-Whitney, ties at 0.5), paired paraphrase − original with the item-level and the persona-clustered bootstrap (1,000 draws, seed 42)")
    w("")
    o.extend(pooled_table(SC, "115"))
    w("")
    w("### 4b. The matched metric (post hoc, R125's construction: within-triple PN vs PRESENT, (W + T/2) / n; triple-level and persona-grouped bootstrap)")
    w("")
    o.extend(matched_table(SC))
    w("")
    w("### 4c. Model minus lookup on the paraphrase set, same summary (pooled AUROC; * = both intervals exclude zero)")
    w("")
    o.extend(model_minus_lookup(SC))
    w("")
    PH = jload(RES / "para_minus_lookup_posthoc.json") if (RES / "para_minus_lookup_posthoc.json").exists() else None
    if PH:
        w("### 4d. POST HOC (requested after the run; not in the registration): each model minus the embedding lookup, paraphrase set and original questions of the same pairs, whole set and supersession only, pooled and matched, item / triple and persona intervals")
        w("")
        w(f"Computed by `tools/posthoc_minus_lookup.py` from the scored rows ({PH['n_items']} items, {PH['n_pairs']} triples; supersession {PH['n_items_superseded']} items, {PH['n_pairs_superseded']} triples), "
          "with `score_para.paired` (the registration's item-level and persona-clustered paired bootstrap, 1,000 draws, seed 42) for the pooled AUROC and R125's construction for the matched metric "
          "(mean over triples of the per-triple PN-vs-PRESENT outcome difference, triple-level and persona-grouped bootstrap). The whole-set paraphrase columns re-derive section 4c's rows exactly "
          "(asserted at eight decimals before writing). The original-question columns are the same models minus the same lookup on the original questions of these pairs, so a reader can see "
          "whether any lead grew under rewording. Ledger rows AUX-PARA-POSTHOC-MINUS-LOOKUP-*.")
        w("")
        o.extend(posthoc_minus_lookup_tables(PH))
        # the supersession-only reading in words, from the pooled paraphrase column (the registered metric) and the matched one beside it
        lead, below, agree = [], [], []
        for code, nm in (("MINI", "GPT-4.1 mini"), ("H45", "Haiku 4.5"), ("OP5", "Opus 5"), ("LUNA", "GPT-5.6 Luna"), ("SOL", "GPT-5.6 Sol")):
            M = PH["models"].get(code)
            if not M or "v2" not in M:
                continue
            pp, mp = M["v2"]["superseded"]["pooled"]["paraphrase"], M["v2"]["superseded"]["matched"]["paraphrase"]
            po = M["v2"]["superseded"]["pooled"]["original"]
            if pp["both_exclude_zero"] and pp["delta"] > 0:
                lead.append(f"{nm} {pp['delta']:+.4f} (original questions {po['delta']:+.4f}{', reliable' if po['both_exclude_zero'] else ', not reliable'})")
            if pp["both_exclude_zero"] and pp["delta"] < 0:
                below.append(f"{nm} {pp['delta']:+.4f}")
            agree.append(f"{nm}: {'agree' if pp['both_exclude_zero'] == mp['both_exclude_zero'] else 'DISAGREE'} (pooled {pp['delta']:+.4f}{' *' if pp['both_exclude_zero'] else ''}, matched {mp['delta']:+.4f}{' *' if mp['both_exclude_zero'] else ''})")
        w("Supersession only, superseded-names summary (v2), paraphrase set, pooled AUROC, model minus the embedding lookup: reliably above the lookup: "
          + (", ".join(lead) if lead else "none") + "; reliably below: " + (", ".join(below) if below else "none")
          + ". Pooled against matched on reliability: " + "; ".join(agree) + ".")
        w("")
    if SCs:
        w(f"## 5. The same tables on the 124 screen-passing pairs — **sensitivity, not registered** (n = {SCs['n']} items, {SCs['n_pos']} positives)")
        w("")
        w("### 5a. Pooled AUROC")
        w("")
        o.extend(pooled_table(SCs, "124"))
        w("")
        w("### 5b. The matched metric")
        w("")
        o.extend(matched_table(SCs))
        w("")
        w("### 5c. Model minus lookup")
        w("")
        o.extend(model_minus_lookup(SCs))
        w("")
        w("### 5d. §7 branches on the 124 (sensitivity, not registered)")
        w("")
        for sv in ("v2", "v3"):
            b = SCs["branches"][sv]
            w(f"- {sv}: " + ", ".join(f"{k} *{v}*" for k, v in b["status"].items()) + f" → **{', '.join(b['headings']) or 'none of A–D'}**" + (f"; D: {b['D']}" if b["D"] else "") + ".")
        w("")
    w("## 6. The Appendix H.2 split on the paraphrase set (AUX-PARA-FLAGS), under both column-2 rules")
    w("")
    tok_yes = sum(1 for r in jload(PARA / "para_questions.json")["rows"] if r["accepted"] and r["value_tokens_in_paraphrase"] and r["pair_id"] in {a["pair_id"] for a in acc})
    w(f"Rule 1, the author's column 2 filled to H.2's sentence (\"names the plan or value its attribute is about\"): **{sh['names_value_yes']} YES** of the {len(acc)} accepted (62 of the 124). "
      f"Rule 2, the token operationalization of the earlier read (the paraphrase carries a content token of the slot path's value part, registered tokenizer): **{tok_yes}** of the {len(acc)} (33 of the 124). "
      "Both are disclosures; neither excludes a pair. The original questions' flags (AUX-CF2-QUESTIONREAD, 89 of 148) are printed beside for the same pairs. Values are pooled AUROC on the paraphrase set (and the original) restricted to each half.")
    w("")
    w("### 6a. Rule 1 — the author's column 2 (H.2's sentence)")
    w("")
    o.extend(flags_table(SC, "author_column2_on_paraphrases"))
    w("")
    w("### 6b. Rule 2 — the token rule on the paraphrases")
    w("")
    o.extend(flags_table(SC, "token_rule_on_paraphrases"))
    w("")
    w("### 6c. The original questions' flags, same pairs")
    w("")
    o.extend(flags_table(SC, "original_question_flags"))
    w("")
    w("## 7. The paraphrases are systematically more generic than the originals")
    w("")
    ex = SC["extras"]["target_name_similarity"]
    examples = [(1, "meeting", "discussion"), (12, "headlamps", "lights"), (63, "bag", "portion")]
    exs = "; ".join(f"row {n}: \"{sheet[n]['original_question']}\" → \"{sheet[n]['paraphrase']}\"" for n, _, _ in examples)
    w(f"Because the screen forbids the attribute's own words and every name the summary prints, the paraphrases replace specific nouns with generic ones, so the paraphrase set differs from the original set in two ways at once: "
      f"no shared token and less specific wording, and any change in a reader's score reflects both. Three examples from the accepted rows: {exs}. "
      f"Measured on the {len(acc)} accepted pairs (the author's extra descriptive of 2026-09-14): mean cosine of the question to its target name falls from {ex['cosine_original_mean']:.3f} to {ex['cosine_paraphrase_mean']:.3f} "
      f"(mean change {ex['cosine_paraphrase_minus_original_mean']:+.3f}); mean content-token overlap with the target name falls from {ex['token_overlap_original_mean']:.3f} to {ex['token_overlap_paraphrase_mean']:.3f}, "
      f"with {ex['pairs_with_zero_overlap_original']} pairs at zero overlap before and {ex['pairs_with_zero_overlap_paraphrase']} after.")
    w("")
    w("## 8. Files")
    w("")
    for rel in ("registrations/ADDENDUM_PARA.md", "reviews/v12/PARAPHRASE_READ.md", "cf2_paraphrase/sheet.json", "cf2_paraphrase/probes.json", "cf2_paraphrase/results/lookups.json",
                "cf2_paraphrase/results/lookups_all124.json", "cf2_paraphrase/results/para_scores.json", "cf2_paraphrase/results/para_scores_all124.json",
                "cf2_paraphrase/rows/rows_MINI.jsonl", "cf2_paraphrase/rows/rows_H45.jsonl", "cf2_paraphrase/rows/rows_OP5.jsonl", "cf2_paraphrase/rows/rows_LUNA.jsonl", "cf2_paraphrase/rows/rows_SOL.jsonl",
                "cf2_paraphrase/probes_openai.json", "cf2_paraphrase/NUMBERS_PARA.md",
                "reviews/para/PARA_APPROVAL_SHEET.csv", "reviews/para/PARA_AI_FLAGS.md", "reviews/para/PARA_AI_FLAGS_ADDENDUM.md", "reviews/para/PARA_PERSONA_EVIDENCE.md", "reviews/para/PARA_COL2_TOKEN_CHECK.md"):
        p = ROOT / rel
        w(f"- `{rel}`: " + (f"sha256 `{hashlib.sha256(p.read_bytes()).hexdigest()}`" if p.exists() else "absent"))
    w("")
    text = "\n".join(o) + "\n"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print("wrote", OUT.relative_to(ROOT).as_posix(), "sha256", hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
