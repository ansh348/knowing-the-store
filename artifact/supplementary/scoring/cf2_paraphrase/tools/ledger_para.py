"""ledger_para.py -- regenerate sections 3 and 4 of cf2_paraphrase/NUMBERS_PARA.md (AUX-PARA-SHEET, AUX-PARA-LOCK,
AUX-PARA-PROBE-* / -PROJECTION-*, AUX-PARA-LOOKUP-*, AUX-PARA-{MINI,H45,OP5}-V2/V3, AUX-PARA-FLAGS, AUX-PARA-BRANCH,
AUX-PARA-SPEND, and beside them AUX-PARA-MATCHED (both metrics), AUX-PARA-SENS-* (the 124, sensitivity, not registered), AUX-PARA-GENERIC (the author's
extra descriptive) and AUX-PARA-POSTHOC-MINUS-LOOKUP-* (post hoc, requested after the run: model minus lookup on both question sets, whole and supersession only))
from the JSON artifacts. No model call; re-runnable; the two sections are regenerated whole between the '## 3.' heading and
the '## Additions requested' heading, the rest of the file is kept. Parts whose artifact is missing print as pending."""
from __future__ import annotations

import collections
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from para_common import PARA, REG_SHA, SHEET, jload, sha256_file  # noqa: E402

LEDGER = PARA / "NUMBERS_PARA.md"
RES = PARA / "results"
FLAGS_A = {30, 40, 77, 82, 28}
FLAGS_B = {11, 46, 33, 79}
FLAGS_C = {12, 27, 45, 49, 52, 57, 63, 68, 92, 94, 102, 112}
LANE = {"MINI": ("gpt-4.1-mini", "k = 1, synchronous, list price"), "H45": ("claude-haiku-4-5-20251001", "k = 5, Batch"), "OP5": ("claude-opus-5", "k = 1, Batch"),
        "LUNA": ("gpt-5.6-luna", "ADDED 2026-09-21, NOT REGISTERED; k = 5, raw Chat Completions, Table 1 settings, v2 only"), "SOL": ("gpt-5.6-sol", "ADDED 2026-09-21, NOT REGISTERED; k = 5, raw Chat Completions, Table 1 settings, v2 only")}
ADDED = ("LUNA", "SOL")


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def ci(d, key="ci_item"):
    c = d.get(key) or {}
    return "[—]" if "ci_lo" not in c else f"[{c['ci_lo']:+.4f}, {c['ci_hi']:+.4f}]"


def paired_str(pd):
    return (f"Δ {pd['delta']:+.4f}, item {ci(pd, 'ci_item')}, persona {ci(pd, 'ci_persona')}"
            f"{' *' if pd.get('both_exclude_zero') else ''}{'' if pd.get('agree', True) else ' (intervals disagree; the weaker reading is ' + pd['weaker']['which'] + ')'}")


def sheet_section(sh, sens):
    rows = sh["rows"]
    acc = [r for r in rows if r["same_intent"] == "YES"]
    no1 = [r for r in rows if r["same_intent"] != "YES"]
    num = {r["pair_id"]: r["num"] for r in rows}
    c2_all = sum(1 for r in rows if r["names_value"] == "YES")
    tok = jload(PARA / "para_questions.json")["rows"]
    tok_yes = {r["pair_id"] for r in tok if r["accepted"] and r["value_tokens_in_paraphrase"]}
    no_nums = {r["num"] for r in no1}
    xt = {"A (would answer NO)": (FLAGS_A, len(FLAGS_A & no_nums)), "B (depends on the persona)": (FLAGS_B, len(FLAGS_B & no_nums)),
          "C (vaguer, would pass)": (FLAGS_C, len(FLAGS_C & no_nums)),
          "not flagged": (set(range(1, 125)) - FLAGS_A - FLAGS_B - FLAGS_C, len((set(range(1, 125)) - FLAGS_A - FLAGS_B - FLAGS_C) & no_nums))}
    o = []
    o.append("## 3. AUX-PARA-SHEET — the author's read (2026-09-21; `reviews/v12/PARAPHRASE_READ.md`; `tools/score_para.py sheet` → `sheet.json`)")
    o.append("")
    o.append("| key | value |")
    o.append("|---|---|")
    o.append(f"| **AUX-PARA-SHEET** | Sheet sha256 **`{sh['sheet_sha256']}`** (ledgered before any scoring call; §5). {sh['n_rows']} rows read; "
             f"column 1 YES on **{len(acc)}**, NO on **{len(no1)}** (rows {', '.join(str(r['num']) for r in no1)}): "
             + "; ".join(f"`{r['pair_id']}`" for r in no1) + ". Accepted by state: supersession {sup}, retraction {ret}, expiry {exp}. "
             .format(sup=sh['by_state'].get('SUPERSESSION', 0), ret=sh['by_state'].get('RETRACTION', 0), exp=sh['by_state'].get('EXPIRY', 0))
             + f"The registered floor of 120 is not met; **the amendment of 2026-09-21** (dated line below the registration's marker; whole file `968f9e13…`) "
             f"sets the floor to the {len(acc)} accepted pairs and adds one sensitivity analysis, labelled not registered, on all {sh['n_rows']} screen-passing pairs. No verdict revisited. |")
    o.append(f"| **AUX-PARA-SHEET (column 2)** | Filled to Appendix H.2's sentence (\"names the plan or value its attribute is about\"): YES on **{c2_all}** of the {sh['n_rows']} "
             f"(**{sh['names_value_yes']}** of the {len(acc)} accepted). The token operationalization of the earlier read (`reviews/CF2_QUESTION_READ.md`; the paraphrase carries a "
             f"content token of the slot path's value part, registered tokenizer; `reviews/para/PARA_COL2_TOKEN_CHECK.md`): **{len(tok_yes)}** of the {sh['n_rows']} "
             f"(**{sum(1 for r in acc if r['pair_id'] in tok_yes)}** of the {len(acc)}). AUX-PARA-FLAGS is reported under both rules. |")
    o.append(f"| **AUX-PARA-SHEET (screen)** | Every accepted paraphrase re-passes the §3 screen at scoring time under the narrowed scope (§3(a) = the scrubbed slot name; §3(b) unchanged): "
             f"{sh['screen_rerun_ok']}; {sh['n_accepted_passing_registered_screen']} of the {len(acc)} also pass the registered (unnarrowed) screen. |")
    o.append("| **AUX-PARA-SHEET (the assistant's flags)** | The AI-assisted pre-read (`reviews/para/PARA_AI_FLAGS.md`, `PARA_AI_FLAGS_ADDENDUM.md`; the dated notes of 21 Sep below the registration's marker) against the author's column 1: "
             + "; ".join(f"level {k}: {n} of {len(s)} answered NO" for k, (s, n) in xt.items())
             + ". Of the addendum's revised view of nine rows: its two 'NO, wrong referent' (11, 77) and two 'NO, leaning' (40, 46) are NO; of its five 'author's call' rows, 28, 30, 79, 82 are NO and 33 is YES; row 68 (level C) is NO. Every verdict is the author's. |")
    if sens:
        o.append(f"| **AUX-PARA-SENS-POP** | The sensitivity population: all {sh['n_rows']} screen-passing pairs ({sens['n']} items), the {len(acc)} accepted plus the 9 excluded; not registered, reported beside the {len(acc)}. |")
    o.append("")
    return o


def lock_section(sh, probes):
    L, g = sh["locks"], sh["lookup_gate"]
    o = ["## 4. AUX-PARA-LOCK, AUX-PARA-PROBE-* / -PROJECTION-*, AUX-PARA-LOOKUP-*, AUX-PARA-{MINI,H45,OP5}-V2/V3, AUX-PARA-FLAGS, AUX-PARA-BRANCH, AUX-PARA-SPEND (2026-09-21; `tools/score_para.py`)", "",
         "| key | value |", "|---|---|",
         f"| **AUX-PARA-LOCK** | Registration sha256 `{L['registration_sha256'][:16]}…` = `{REG_SHA[:16]}…` ({L['registration_ok']}); CF-2 questions sha256 `{L['questions_sha256'][:16]}…` = ledgered ({L['questions_ok']}); "
         f"indexes sha256 `{L['indexes_sha256'][:16]}…` = ledgered ({L['indexes_ok']}); {L['n_questions']} questions. Lookup gate on the original questions at four decimals: embedding v2 **{g['emb_v2']:.4f}** (AUX-CF2-NB6-V2 0.7663), "
         f"v3 **{g['emb_v3']:.4f}** (AUX-CF2-ALLSTATES-V3 0.8756) — PASS; lexical v2 {g['lex_v2']:.4f}, v3 {g['lex_v3']:.4f}. prompts_e1 digests asserted at import (`run_cf`). |"]
    for lane, code in (("gpt-4.1-mini", "MINI"), ("claude-haiku-4-5-20251001", "H45"), ("claude-opus-5", "OP5")):
        p = (probes or {}).get(lane)
        if not p:
            o.append(f"| **AUX-PARA-PROBE-{code}** / **-PROJECTION-{code}** | pending |"); continue
        pj = p["projection"]
        o.append(f"| **AUX-PARA-PROBE-{code}** / **-PROJECTION-{code}** | Served `{p['served'][0]}` on both arms (E1.7 identifier {'OK' if p['identifier_ok'] else 'MISMATCH'}); probe ${p['probe_usd']:.4f}. "
                 f"Projection for {p['n_units']} units × 2 arms × k = {p['k']}: **{pj['calls']} calls, ${pj['usd']:.2f}** (×1.3 ${pj['usd_x1.3']:.2f}) against the headroom ${p['headroom']:.2f} "
                 f"(combined ${p['cap']:.0f} cap less the registered lanes billed, ${p['headroom_combined']:.2f}; overall ${p['overall_cap']:.0f} cap less everything billed, ${p['headroom_overall']:.2f}) — "
                 f"{'fits, submitted' if p['fits'] else 'DASH'}. Had the PAD Amendment 1 Haiku add-on been counted on the combined cap the headroom would read ${p['headroom_if_addon_counted_on_combined']:.2f} "
                 f"({'fits' if p['fits_if_addon_counted_on_combined'] else 'would not fit'}). Population at submission: {p['population']}. |")
    return o


def lookup_rows(LK, LKs, tag=""):
    o = []
    names = {"emb_v2": "LOOKUP-EMB-V2", "lex_v2": "LOOKUP-LEX-V2", "emb_v3": "LOOKUP-EMB-V3", "lex_v3": "LOOKUP-LEX-V3"}
    for k in ("emb_v2", "lex_v2", "emb_v3", "lex_v3"):
        r = LK["rows"][k]
        ps = r["paired_per_state"]
        cell = (f"Original {r['original']:.4f} (sup {r['original_per_state']['superseded']:.4f} / ret {r['original_per_state']['retracted']:.4f} / exp {r['original_per_state']['expired']:.4f}) → "
                f"paraphrase **{r['paraphrase']:.4f}** (sup {r['paraphrase_per_state']['superseded']:.4f} / ret {r['paraphrase_per_state']['retracted']:.4f} / exp {r['paraphrase_per_state']['expired']:.4f}); "
                f"paired paraphrase − original {paired_str(r['paired'])}; per state Δ sup {ps['superseded']['delta']:+.4f} / ret {ps['retracted']['delta']:+.4f} / exp {ps['expired']['delta']:+.4f}")
        if LKs:
            s = LKs["rows"][k]
            cell += f". Sensitivity, not registered (the 124): original {s['original']:.4f} → paraphrase {s['paraphrase']:.4f}, {paired_str(s['paired'])}"
        o.append(f"| **AUX-PARA-{names[k]}{tag}** | {cell} |")
    return o


def model_rows(SC, SCs):
    o = []
    for code in ("MINI", "H45", "OP5", "LUNA", "SOL"):
        M = SC["models"].get(code)
        if not M or "v2" not in M:
            o.append(f"| **AUX-PARA-{code}-V2** / **-V3** | {(M or {}).get('status', 'pending')} |"); continue
        for sv in ("v2", "v3"):
            if sv not in M:
                o.append(f"| **AUX-PARA-{code}-{sv.upper()}** (added, not registered) | not run: the added readers ran under v2 only (their Table 1 arm, the only one with recorded originals; both arms projected over the $14 cap) |"); continue
            R = M[sv]; ps = R["paired_per_state"]
            cell = (f"{LANE[code][0]} ({LANE[code][1]}; recorded rows k = {M['k_recorded']}, new rows k = {M['k_new']}; {R['n_scored']} items scored, {M['n_bad_rows']} bad rows). "
                    f"Original {R['original']:.4f} (sup {R['original_per_state']['superseded']:.4f} / ret {R['original_per_state']['retracted']:.4f} / exp {R['original_per_state']['expired']:.4f}) → "
                    f"paraphrase **{R['paraphrase']:.4f}** (sup {R['paraphrase_per_state']['superseded']:.4f} / ret {R['paraphrase_per_state']['retracted']:.4f} / exp {R['paraphrase_per_state']['expired']:.4f}); "
                    f"paired paraphrase − original {paired_str(R['paired'])}; per state Δ sup {ps['superseded']['delta']:+.4f} / ret {ps['retracted']['delta']:+.4f} / exp {ps['expired']['delta']:+.4f}. "
                    f"Model − embedding lookup on the paraphrase set {paired_str(R['model_minus_emb'])}; model − lexical lookup {paired_str(R['model_minus_lex'])}")
            if code == "OP5":
                cell += ". Opus 5's new rows are k = 1 against k = 5 on the recorded CF-2 rows (§6): a draw-count difference, disclosed, not a registered comparison"
            if SCs and code in SCs["models"] and sv in SCs["models"][code]:
                S = SCs["models"][code][sv]
                cell += f". Sensitivity, not registered (the 124): original {S['original']:.4f} → paraphrase {S['paraphrase']:.4f}, {paired_str(S['paired'])}"
            o.append(f"| **AUX-PARA-{code}-{sv.upper()}**{' (added, not registered)' if code in ADDED else ''} | {cell} |")
    return o


def flags_rows(SC, SCs):
    o = []
    for label, key in (("the author's column 2 (H.2's sentence)", "author_column2_on_paraphrases"), ("the original questions' flags (AUX-CF2-QUESTIONREAD, the token rule)", "original_question_flags"),
                       ("the token rule on the paraphrases (registered tokenizer)", "token_rule_on_paraphrases")):
        F = SC["flags"].get(key)
        if not F:
            continue
        parts = []
        for rk in ("emb_v2", "lex_v2", "emb_v3", "lex_v3", "MINI_v2", "MINI_v3", "H45_v2", "H45_v3", "OP5_v2", "OP5_v3", "LUNA_v2", "SOL_v2"):
            if rk in F:
                p = F[rk]["paraphrase"]; q = F[rk]["original"]
                parts.append(f"{rk}: paraphrase flagged {f4(p['flagged'])} / unflagged {f4(p['unflagged'])} (original {f4(q['flagged'])} / {f4(q['unflagged'])})")
        o.append(f"| **AUX-PARA-FLAGS** ({label}) | {F['n_flagged_pairs']} flagged pairs / {F['n_unflagged_pairs']} unflagged. " + "; ".join(parts) + ". |")
    return o


def branch_rows(SC):
    o = []
    for sv in ("v2", "v3"):
        b = SC["branches"][sv]
        o.append(f"| **AUX-PARA-BRANCH-{sv.upper()}** | Status per reader (tolerance ±0.05 on the paired difference; 'collapses' needs both intervals below zero): "
                 + ", ".join(f"{k} {v}" for k, v in b["status"].items()) + f". Headings: **{', '.join(b['headings']) or 'none'}**"
                 + (f"; D names {b['D']}" if b["D"] else "") + ". No prediction and no bar; prints as it comes out."
                 + (f" Added readers, not registered, beside: {b['added_readers_status_not_registered']}." if b.get("added_readers_status_not_registered") else "") + " |")
    return o


def matched_rows(SC, SCs):
    o = []
    M = SC.get("matched")
    if not M:
        return o
    for k in ("emb_v2", "lex_v2", "emb_v3", "lex_v3", "MINI_v2", "MINI_v3", "H45_v2", "H45_v3", "OP5_v2", "OP5_v3", "LUNA_v2", "SOL_v2"):
        if k not in M:
            continue
        w = M[k]["pn_vs_present"]; a = M[k]["pn_vs_absent"]
        ow, pw, dw = w["original"]["whole"], w["paraphrase"]["whole"], w["paired"]["whole"]
        cell = (f"PN vs PRESENT: original {ow['W']}/{ow['T']}/{ow['L']} = {ow['matched']:.4f} → paraphrase **{pw['W']}/{pw['T']}/{pw['L']} = {pw['matched']:.4f}** "
                f"(triple {ci(pw, 'ci_triple')}, persona {ci(pw, 'ci_persona')}); paired Δ {dw['delta']:+.4f}, triple {ci(dw, 'ci_triple')}, persona {ci(dw, 'ci_persona')}{' *' if dw['both_exclude_zero'] else ''}; "
                f"per state paraphrase sup {w['paraphrase']['per_state']['superseded']['matched']} / ret {w['paraphrase']['per_state']['retracted']['matched']} / exp {w['paraphrase']['per_state']['expired']['matched']}. "
                f"PN vs ABSENT: original {a['original']['whole']['matched']:.4f} → paraphrase {a['paraphrase']['whole']['matched']:.4f}, Δ {a['paired']['whole']['delta']:+.4f}")
        if SCs and SCs.get("matched", {}).get(k):
            s = SCs["matched"][k]["pn_vs_present"]
            cell += f". Sensitivity (the 124): original {s['original']['whole']['matched']:.4f} → paraphrase {s['paraphrase']['whole']['matched']:.4f}, Δ {s['paired']['whole']['delta']:+.4f}, triple {ci(s['paired']['whole'], 'ci_triple')}, persona {ci(s['paired']['whole'], 'ci_persona')}"
        o.append(f"| **AUX-PARA-MATCHED-{k.upper()}** (post hoc, beside the registered pooled AUROC{'; added reader, not registered' if k.split('_')[0] in ADDED else ''}) | {cell} |")
    return o


def posthoc_rows(PH):
    """AUX-PARA-POSTHOC-MINUS-LOOKUP-* (post hoc, 2026-09-21, requested after the run; tools/posthoc_minus_lookup.py): each model minus the embedding
    lookup, paraphrase set and original questions of the same pairs, whole set and supersession only, pooled AUROC and the matched metric."""
    o = []
    if not PH:
        return o

    def cell(d, met):
        c1 = "ci_item" if met == "pooled" else "ci_triple"
        return f"{d['delta']:+.4f} ({'item' if met == 'pooled' else 'triple'} {ci(d, c1)}, persona {ci(d, 'ci_persona')}){' *' if d['both_exclude_zero'] else ''}"

    for code in ("MINI", "H45", "OP5", "LUNA", "SOL"):
        M = PH["models"].get(code)
        if not M or "v2" not in M:
            continue
        for sv in ("v2", "v3"):
            if sv not in M:
                continue
            R = M[sv]
            parts = []
            for scope, nm in (("whole", f"whole set ({R['n_scored']} items, {PH['n_pairs']} triples)"), ("superseded", f"supersession only ({R['n_scored_superseded']} items, {PH['n_pairs_superseded']} triples)")):
                for met in ("pooled", "matched"):
                    P_, O_ = R[scope][met]["paraphrase"], R[scope][met]["original"]
                    parts.append(f"{nm}, {met}: paraphrase {cell(P_, met)}; original {cell(O_, met)}")
            o.append(f"| **AUX-PARA-POSTHOC-MINUS-LOOKUP-{code}-{sv.upper()}** (post hoc, not registered{'; added reader, not registered' if code in ADDED else ''}) | "
                     f"Model − embedding lookup under the {sv} summary. " + ". ".join(parts) + ". * = both intervals exclude zero. |")
    return o


def generic_row(SC):
    """AUX-PARA-GENERIC: the author's extra descriptive of 2026-09-14 (cosine and content-token overlap of the question to its target name, before and after)."""
    ex = (SC or {}).get("extras", {}).get("target_name_similarity")
    if not ex:
        return []
    return [f"| **AUX-PARA-GENERIC** (the author's extra descriptive of 2026-09-14; `score_para.py score`, `extras.target_name_similarity`) | Mean cosine of the question to its target name "
            f"(the pair's `slot_scrubbed`; the registered encoder): original **{ex['cosine_original_mean']:.4f}** → paraphrase **{ex['cosine_paraphrase_mean']:.4f}** "
            f"(mean change {ex['cosine_paraphrase_minus_original_mean']:+.4f}); mean content-token overlap with the target name: original **{ex['token_overlap_original_mean']:.4f}** → "
            f"paraphrase **{ex['token_overlap_paraphrase_mean']:.4f}**; pairs at zero overlap {ex['pairs_with_zero_overlap_original']} before, {ex['pairs_with_zero_overlap_paraphrase']} after "
            f"(of {len(ex['per_pair'])}). Printed at three decimals in the report ({ex['cosine_original_mean']:.3f} → {ex['cosine_paraphrase_mean']:.3f}; "
            f"{ex['token_overlap_original_mean']:.3f} → {ex['token_overlap_paraphrase_mean']:.3f}). |"]


def spend_row():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import score_para as sp
    H = sp.headrooms()
    para = {k: v for k, v in H["billed_parts"].items() if k.startswith("PARA")}
    added = {}
    for code in ADDED:
        rp = PARA / "rows" / f"rows_{code}.jsonl"
        if rp.exists():
            added[code] = sum(json.loads(l).get("usd", 0.0) for l in io.open(rp, encoding="utf-8") if l.strip())
    if (PARA / "probes_openai.json").exists():
        added["probes"] = sum(v["usd"] for v in jload(PARA / "probes_openai.json").values())
    return [f"| **AUX-PARA-SPEND** | PARA registered lanes billed: " + "; ".join(f"{k} ${v:.4f}" for k, v in para.items()) + f"; PARA registered total **${sum(para.values()):.4f}**. "
            + (f"Added lane (Luna and Sol, not registered; OpenAI cap $14): " + "; ".join(f"{k} ${v:.4f}" for k, v in added.items()) + f"; total **${sum(added.values()):.4f}**. " if added else "")
            + f"Everything in the pass (PAD, its Amendment 1, PARA): ${H['billed_overall']:.4f} against the $28 overall cap; the registered lanes ${H['billed_combined']:.4f} against the $21 combined cap (ruling ii). "
            f"Prices: list per lane as `run_cf.LANES`; Batch lanes at the 0.5 multiplier. |"]


def main():
    sh = jload(PARA / "sheet.json")
    probes = jload(PARA / "probes.json") if (PARA / "probes.json").exists() else None
    LK = jload(RES / "lookups.json") if (RES / "lookups.json").exists() else None
    LKs = jload(RES / "lookups_all124.json") if (RES / "lookups_all124.json").exists() else None
    SC = jload(RES / "para_scores.json") if (RES / "para_scores.json").exists() else None
    SCs = jload(RES / "para_scores_all124.json") if (RES / "para_scores_all124.json").exists() else None
    out = sheet_section(sh, LKs) + lock_section(sh, probes)
    if LK:
        out += lookup_rows(LK, LKs)
    else:
        out.append("| **AUX-PARA-LOOKUP-\\*** | pending |")
    PH = jload(RES / "para_minus_lookup_posthoc.json") if (RES / "para_minus_lookup_posthoc.json").exists() else None
    if SC:
        out += model_rows(SC, SCs) + flags_rows(SC, SCs) + branch_rows(SC) + matched_rows(SC, SCs) + generic_row(SC) + posthoc_rows(PH)
    else:
        out.append("| **AUX-PARA-{MINI,H45,OP5}-V2/V3**, **AUX-PARA-FLAGS**, **AUX-PARA-BRANCH**, **AUX-PARA-MATCHED** | pending (no scoring call before AUX-PARA-SHEET is ledgered — it is, above) |")
    out += spend_row()
    out.append("")
    if SCs:
        out.append(f"_Sensitivity rows (the 124 screen-passing pairs, {SCs['n']} items) are printed beside their registered counterparts above and are not registered; "
                   f"the lanes were submitted once on the 124 pairs' items and the registered scoring reads the 115's items from those rows (identical calls: temperature 0 / fixed seeds, independent requests)._")
        out.append("")
    text = io.open(LEDGER, encoding="utf-8", newline="").read()
    a = text.index("## 3. AUX-PARA-SHEET")
    b = text.index("## Additions requested by the author")
    new = text[:a] + "\n".join(out) + "\n" + text[b:]
    io.open(LEDGER, "w", encoding="utf-8", newline="").write(new)
    print("ledger sections 3-4 regenerated;", "lookups" if LK else "no lookups", "|", "scores" if SC else "no scores", "|", "sensitivity" if SCs else "no sensitivity")


if __name__ == "__main__":
    main()
