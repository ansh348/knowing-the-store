# -*- coding: utf-8 -*-
"""r137_number_gate.py -- the number gate of R137 (2026-09-22; the brief 'R137: LAND THE LONG-LIST CHECK, PLUS THE LAST TWO READABILITY ITEMS'): every
number the pass's new texts print is read from its artifact here, independently of cf_pad/results/cf_pad_printed.json and cfpad_printed.json (which
port_r137.py fills its texts from) and of reviews/v23/results/robust_printed.json (which robust_tex.py writes tab:robust from), and compared at the printed
precision (two decimals half-up on the four-decimal recorded value in the body; four decimals in the appendix; the R131 convention) with the reliability or
direction each sentence claims: tab:robust row 9, Section 5.2's long-list sentences, the abstract's, the Section 1 bullet's, the Conclusion's and the
Limitations' clauses, the prediction recount (Section 4, Appendix F), Figure 1's transcribed summary lines, Appendix C.2's prose, tab:setup's row, the
provenance row, tab:registrations-e's row and the spend sentence. Runs R135's checks first (R134's inside), then its own; with --built, the numeral-set
checks with this pass's printed forms and the CFPAD fragments allowed.
Usage: python reviews/v23/tools/r137_number_gate.py [--built]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "reviews" / "v23" / "tools"))
import r134_number_gate as G  # noqa: E402
import r135_number_gate as G135  # noqa: E402

MODELS = ("MINI", "H45", "OP5", "LUNA", "SOL")
FAMILY = {"MINI": "OpenAI", "H45": "Anthropic", "OP5": "Anthropic", "LUNA": "OpenAI", "SOL": "OpenAI"}
DAY0 = (2026, 8, 10)     # day 0 of the registration record (reviews/NUMBERS_R126.md AUX-R126-DAYS: 2026-08-10 -> day 0)


def J(rel):
    return json.load(open(ROOT / rel, encoding="utf-8"))


def rel(d):
    return bool(d.get("both_exclude_zero"))


def fig1_lines():
    """Figure 1's transcribed lines from the summary the E.1 excerpt was cut from (frbank:david:FULL:BELIEVED; AUX-R86-INDEX-EXCERPT): the LIFECYCLE TOTALS
    block's four states, the HOBBIES_RECREATION name line and the superseded-names line, read from the artifact's manifest and asserted equal to the study's copy."""
    A = J("iclr2027_monitoring_submission/ARTIFACT/manifests/indexes_v2.json")["indexes"]["frbank:david:FULL:BELIEVED"]
    B = J("e1_metamemory/indexes_v2.json")["indexes"]["frbank:david:FULL:BELIEVED"]
    assert A == B, "the artifact's manifest and the study's copy differ"
    totals = {}
    blk = A[A.index("LIFECYCLE TOTALS"):A.index("PER-CATEGORY BREAKDOWN")]
    for ln in blk.splitlines()[1:]:
        m = re.match(r"\s+([a-z ]+?)\s+(\d+)\s*$", ln)
        if m:
            totals[m.group(1)] = int(m.group(2))
    names = A[A.index("ATTRIBUTE NAMES BY CATEGORY"):A.index("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")]
    m = re.search(r"^HOBBIES_RECREATION: (.+?)(?=^\S)", names, flags=re.M | re.S)
    hobbies = [x.strip() for x in m.group(1).replace("\n", " ").split(",") if x.strip()]
    sup = A[A.index("ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT"):]
    sup_names = [x.strip() for x in sup.split("\n", 1)[1].replace("\n", " ").replace("(+31 more)", "").split(",") if x.strip()]
    return totals, hobbies, sup_names


def tag_route_record():
    """The tag route's one returned record: David's HOBBIES_RECREATION hiking_preference entry and the tag FR-Bank's own metadata gives it."""
    E = J("e1_metamemory/backend_entries/frbank.json")
    rows = [e for e in E if e["persona"] == "david" and e["slot"] == "hiking_preference" and e["category"] == "HOBBIES_RECREATION"]
    assert len(rows) == 1, rows
    e = rows[0]
    tag = "superseded" if e["believed_superseded"] else ("retracted" if e["believed_retracted"] else "active")
    return e, tag


def checks137():
    chk, r2 = G.chk, G.r2
    S = J("cf_pad/results/cf_pad_scores.json")
    K = J("cf_pad/build/lock.json")
    RD, ML, PR = S["readers"], S["minus_lookup"], S["predictions"]
    lk = RD["LOOKUP"]["superseded"]["pooled"]; lkd = lk["padded_minus_unpadded"]
    lkm = RD["LOOKUP"]["superseded"]["matched"]["padded_minus_unpadded"]
    loss = {m: RD[m]["superseded"]["pooled"]["padded_minus_unpadded"] for m in MODELS}
    mlp = {m: ML[m]["LOOKUP"]["superseded"]["padded"]["pooled"] for m in MODELS}
    mlm = {m: ML[m]["LOOKUP"]["superseded"]["padded"]["matched"] for m in MODELS}
    # ---- tab:robust row 9 / 5.2 / the abstract / the Conclusion: the lookup's fall and the readers' falls
    chk("tab:robust row 9: 'Lookup 0.92' (supersession, pooled, unpadded)", "0.92", lk["unpadded"], "cf_pad_scores.json readers/LOOKUP/superseded/pooled/unpadded (AUX-CFP-READERS-SUPERSEDED; the recorded Table 1 row on the slice)")
    chk("tab:robust row 9: 'to 0.74' (padded)", "0.74", lk["padded"], "readers/LOOKUP/superseded/pooled/padded")
    chk("5.2 / abstract: 'the lookup loses 0.18' (padded minus unpadded, pooled, supersession; reliable; P-L3)", "0.18", lkd["delta"], f"readers/LOOKUP/superseded/pooled/padded_minus_unpadded {lkd['delta']:+.4f} [{lkd['ci_item']['ci_lo']:+.4f},{lkd['ci_item']['ci_hi']:+.4f}]; [{lkd['ci_persona']['ci_lo']:+.4f},{lkd['ci_persona']['ci_hi']:+.4f}] (AUX-CFP-P-L3 HOLDS)",
        reliable=True, actual_reliable=rel(lkd) and lkd["delta"] < 0)
    chk("5.2: P-L3 holds", "HOLDS", "HOLDS" if PR["P-L3"]["holds"] else "FAILS", "predictions/P-L3")
    for m, nm in (("MINI", "mini"), ("H45", "Haiku"), ("OP5", "Opus")):
        chk(f"tab:robust row 9 / 5.2 / abstract: '{nm} falls with it' (padded minus unpadded reliable and below zero; not reliably above the lookup)", "falls",
            "falls" if rel(loss[m]) and loss[m]["delta"] < 0 and not (rel(mlp[m]) and mlp[m]["delta"] > 0) else "does not",
            f"readers/{m}/superseded/pooled/padded_minus_unpadded {loss[m]['delta']:+.4f}; minus_lookup/{m}/LOOKUP/superseded/padded/pooled {mlp[m]['delta']:+.4f} (intervals including zero)")
        chk(f"5.2: '{nm} ends level with the lookup or below' (padded minus lookup at or below zero at the point)", "at or below", "at or below" if mlp[m]["delta"] <= 0 else "above", f"minus_lookup/{m}/LOOKUP/superseded/padded/pooled {mlp[m]['delta']:+.4f}")
    chk("5.2: 'mini and Opus lose more than the lookup' (the brief's 'as much or more' corrected: Haiku loses less at the point)", "more", "more" if all(loss[m]["delta"] < lkd["delta"] for m in ("MINI", "OP5")) else "not more",
        f"mini {loss['MINI']['delta']:+.4f}, Opus {loss['OP5']['delta']:+.4f} against the lookup's {lkd['delta']:+.4f}")
    chk("5.2: Haiku loses less than the lookup at the point (why the brief's 'as much or more' is not printed; 'fall with it' is)", "less", "less" if lkd["delta"] < loss["H45"]["delta"] < 0 else "not less", f"Haiku {loss['H45']['delta']:+.4f} against the lookup's {lkd['delta']:+.4f}")
    lo_l, hi_l = sorted(abs(loss[m]["delta"]) for m in ("LUNA", "SOL"))
    chk("tab:robust row 9 / 5.2 / abstract: 'Luna and Sol lose 0.06' (the smaller of the two falls; both reliable)", "0.06", lo_l, f"readers/LUNA/superseded/pooled/padded_minus_unpadded {loss['LUNA']['delta']:+.4f}, SOL {loss['SOL']['delta']:+.4f}",
        reliable=True, actual_reliable=all(rel(loss[m]) and loss[m]["delta"] < 0 for m in ("LUNA", "SOL")))
    chk("tab:robust row 9 / 5.2 / abstract: 'to 0.07' (the larger)", "0.07", hi_l, "as above")
    chk("5.2 / P-L4: 'Luna and Sol lose less than the lookup' (point estimates)", "less", "less" if all(loss[m]["delta"] > lkd["delta"] for m in ("LUNA", "SOL")) else "not less", f"Luna {loss['LUNA']['delta']:+.4f}, Sol {loss['SOL']['delta']:+.4f} against the lookup's {lkd['delta']:+.4f}")
    chk("Limitations / P-L4: Opus loses more than the lookup (P-L4 fails on Opus alone)", "FAILS on Opus", "FAILS on Opus" if (not PR["P-L4"]["holds"]) and (not PR["P-L4"]["per_model"]["OP5"]["loses_less"]) and PR["P-L4"]["per_model"]["LUNA"]["loses_less"] and PR["P-L4"]["per_model"]["SOL"]["loses_less"] else "other",
        f"predictions/P-L4 per_model: Luna loses_less {PR['P-L4']['per_model']['LUNA']['loses_less']}, Sol {PR['P-L4']['per_model']['SOL']['loses_less']}, Opus {PR['P-L4']['per_model']['OP5']['loses_less']} (Opus {loss['OP5']['delta']:+.4f})")
    lo_m, hi_m = sorted(mlp[m]["delta"] for m in ("LUNA", "SOL"))
    chk("tab:robust row 9 / 5.2 / abstract / Conclusion: 'lead the lookup by 0.13' (the smaller pooled lead; both reliable)", "0.13", lo_m, f"minus_lookup/LUNA/LOOKUP/superseded/padded/pooled {mlp['LUNA']['delta']:+.4f}, SOL {mlp['SOL']['delta']:+.4f} (AUX-CFP-MINUS-LOOKUP-SUPERSEDED; P-L1 fails on Opus alone)",
        reliable=True, actual_reliable=all(rel(mlp[m]) and mlp[m]["delta"] > 0 for m in ("LUNA", "SOL")))
    chk("tab:robust row 9 / 5.2 / abstract / Conclusion: 'to 0.14' (the larger pooled lead)", "0.14", hi_m, "as above")
    lo_mm, hi_mm = sorted(mlm[m]["delta"] for m in ("LUNA", "SOL"))
    chk("5.2: 'and 0.09 within triples' (the smaller matched lead; both reliable; the brief's 'on both metrics' made explicit)", "0.09", lo_mm, f"minus_lookup/LUNA/LOOKUP/superseded/padded/matched {mlm['LUNA']['delta']:+.4f}, SOL {mlm['SOL']['delta']:+.4f}",
        reliable=True, actual_reliable=all(rel(mlm[m]) and mlm[m]["delta"] > 0 for m in ("LUNA", "SOL")))
    chk("5.2: 'to 0.10 within triples' (the larger matched lead)", "0.10", hi_mm, "as above")
    chk("5.2 / 1 / Conclusion: 'two of five' reliably above the lookup on the padded list (pooled; P-L1 fails on Opus, P-L2 holds)", "2", sum(1 for m in MODELS if rel(mlp[m]) and mlp[m]["delta"] > 0), "minus_lookup/*/LOOKUP/superseded/padded/pooled, both intervals above zero")
    chk("5.2 / 1: the two are Luna and Sol", "LUNA,SOL", ",".join(sorted(m for m in MODELS if rel(mlp[m]) and mlp[m]["delta"] > 0)), "as above")
    chk("5.2 / 1: the same two on the matched metric", "LUNA,SOL", ",".join(sorted(m for m in MODELS if rel(mlm[m]) and mlm[m]["delta"] > 0)), "minus_lookup/*/LOOKUP/superseded/padded/matched")
    chk("5.2: P-L1 fails and P-L2 holds", "FAILS,HOLDS", ("FAILS" if not PR["P-L1"]["holds"] else "HOLDS") + "," + ("HOLDS" if PR["P-L2"]["holds"] else "FAILS"), "predictions/P-L1, P-L2")
    # ---- 5.2: 'Retraction and expiry do not move' (no reader's change reliable there except Haiku matched and Opus pooled on retraction; the lookups tie by construction)
    rel_counted = sorted((c, sl, met) for c in RD for sl in ("retracted", "expired") for met in ("pooled", "matched") if rel(RD[c][sl][met]["padded_minus_unpadded"]))
    chk("5.2 / C.2: 'Retraction and expiry do not move' (the reliable changes there: Haiku matched and Opus pooled on retraction only)", "H45 retracted matched; OP5 retracted pooled", "; ".join(" ".join(x) for x in rel_counted),
        "readers/*/{retracted,expired}/{pooled,matched}/padded_minus_unpadded both_exclude_zero")
    for c in ("LOOKUP", "LEX", "RANDTOK"):
        for sl in ("retracted", "expired"):
            chk(f"C.2: the {c} lookup at chance on {sl}, padded and unpadded", "0.50/0.50", f"{r2(RD[c][sl]['pooled']['padded'])}/{r2(RD[c][sl]['pooled']['unpadded'])}", f"readers/{c}/{sl}/pooled")
    # ---- Limitations: Opus one draw against five; the two leading readers from one family
    chk("Limitations / tab:robust caption / C.2: 'Opus 5 ran one draw against its five-draw row'", "1 / 5", f"{S['census']['OP5']['k_new']} / {S['census']['OP5']['k_recorded']}", "census/OP5 k_new, k_recorded")
    chk("Limitations: 'the two readers that keep their lead there are from one model family'", "one family", "one family" if len({FAMILY[m] for m in MODELS if rel(mlp[m]) and mlp[m]["delta"] > 0}) == 1 else "two families", "GPT-5.6 Luna and GPT-5.6 Sol: OpenAI")
    # ---- the abstract / Section 1: 60 names
    chk("abstract / 1 / 5.2 / tab:robust: 'padded to 60 names' (every PN list exactly 60)", "60/60", f"{K['list_length']['by_state_version']['superseded|PN']['min']}/{K['list_length']['by_state_version']['superseded|PN']['max']}", "build/lock.json list_length by_state_version superseded|PN")
    # ---- the prediction recount (Section 4, Appendix F)
    R131 = (ROOT / "reviews" / "NUMBERS_R131.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"With them: (\d+) predictions, (\d+) otherwise; the new tab:registrations-e carries (\d+) with (\d+)", R131)
    base_n, base_k, e_n, e_k = (int(x) for x in m.groups())
    new = len(PR); otherwise = sum(1 for v in PR.values() if not v["holds"])
    chk("4 / F: the prediction count, M (98 + the four P-L predictions)", "102", base_n + new, f"NUMBERS_R131.md AUX-R131-COUNT {base_n} + cf_pad_scores.json predictions {new}")
    chk("4 / F: the prediction count, N (31 + the two that came out otherwise)", "33", base_k + otherwise, f"NUMBERS_R131.md AUX-R131-COUNT {base_k} + {otherwise} (P-L1, P-L4)")
    chk("F: tab:registrations-e carries 9 with 4", "9 with 4", f"{e_n + new} with {e_k + otherwise}", f"AUX-R131-COUNT {e_n} with {e_k}, plus {new} with {otherwise}")
    chk("F: the registration's four predictions, P-L1 to P-L4", "P-L1,P-L2,P-L3,P-L4", ",".join(sorted(PR)), "predictions")
    chk("F: outcomes", "FAILS,HOLDS,HOLDS,FAILS", ",".join("HOLDS" if PR[k]["holds"] else "FAILS" for k in sorted(PR)), "predictions/*/holds")
    # ---- tab:registrations-e's row: the frozen commit and the freeze day
    chk("F: the frozen commit", "06c611f", S["lock"]["frozen_commit"], "cf_pad_scores.json lock/frozen_commit (registrations/ADDENDUM_CF_PAD.md frozen alone before the first paid call)")
    import datetime
    day = (datetime.date(2026, 9, 22) - datetime.date(*DAY0)).days
    chk("F: the freeze day (2026-09-22 against day 0 = 2026-08-10)", "43", day, "reviews/NUMBERS_R126.md AUX-R126-DAYS; cf_pad/build/lock.json 'when' 2026-09-22")
    assert K["when"].startswith("2026-09-22")
    chk("F: the registered text's sha256 prefix", "a84dac1a", S["registration_sha256"][:8], "cf_pad_scores.json registration_sha256")
    # ---- C.2's prose: the construction, the lock, the lanes, the spend
    tp = K["target_position"]; ll = K["list_length"]; po = K["pools"]
    chk("C.2: the population (items / triples / supersession items / supersession triples)", "444/148/264/88", f"{K['n_rows']}/{K['n_pairs']}/{lkd['n']}/{lkm['n']}", "lock.json n_rows, n_pairs; readers/LOOKUP/superseded n")
    chk("C.2: the counted states (items / triples each)", "90/30", f"{RD['LOOKUP']['retracted']['pooled']['padded_minus_unpadded']['n']}/{RD['LOOKUP']['retracted']['matched']['padded']['n']}", "readers/LOOKUP/retracted n")
    chk("C.2: lists 57 to 60 names long", "57-60", f"{ll['min']}-{ll['max']}", "lock.json list_length min, max")
    chk("C.2: pool A 71 to 121 names, median 102; no pad on pool B", "71/102/121/0", f"{po['a_min']}/{int(po['a_median'])}/{po['a_max']}/{po['from_pool_b_pairs']}", "lock.json pools")
    chk("C.2: the target's rank: min 2, median 41.5, max 60, never first, last on 4 of 88 (the brief's 'median 41' corrected to the ledger's 41.5)", "2/41.5/60/0/4/88", f"{tp['min']}/{tp['median']}/{tp['max']}/{tp['first']}/{tp['last']}/{tp['n']}", "lock.json target_position")
    chk("C.2: the rank by tenths of the list", "5/3/2/5/8/12/12/9/9/23", "/".join(str(tp["deciles"][str(i)]) for i in range(1, 11)), "lock.json target_position deciles")
    chk("C.2: renderer lock 444 of 444; leak scan 0 fails", "444/0", f"{K['renderer_lock']}/{K['leak_scan']['fails']}", "lock.json renderer_lock, leak_scan")
    chk("C.2 / tab:setup: draws (mini, Haiku, Luna, Sol, Opus)", "5/5/5/5/1", "/".join(str(S["census"][c]["k_new"]) for c in ("MINI", "H45", "LUNA", "SOL", "OP5")), "census/*/k_new")
    chk("C.2: rows per five-draw lane / Opus; not-OK rows", "2220/444/0", f"{S['census']['MINI']['rows']}/{S['census']['OP5']['rows']}/{sum(S['census'][c]['not_ok'] for c in S['census'])}", "census/*/rows, not_ok")
    chk("C.2 / E.11: Anthropic spend of the cap", "8.11 of 12", f"{S['spend']['anthropic']['usd']:.2f} of {S['spend']['anthropic']['cap']:g}", "spend/anthropic (token-metered, not an invoice)")
    chk("C.2 / E.11: OpenAI spend of the cap", "15.54 of 20", f"{S['spend']['openai']['usd']:.2f} of {S['spend']['openai']['cap']:g}", "spend/openai")
    chk("C.2: no cap reached, no draw dropped, no STOP fired, no deviation", "clean", "clean" if not S["stops"] and all(S["census"][c]["complete_draws"] == list(range(1, S["census"][c]["k_new"] + 1)) for c in S["census"]) and "none" in (ROOT / "cf_pad" / "DEVIATIONS_CF_PAD.md").read_text(encoding="utf-8").lower() else "not clean",
        "cf_pad_scores.json stops, census/*/complete_draws; cf_pad/DEVIATIONS_CF_PAD.md")
    chk("C.2: the tolerance", "0.05", S["tol"], "cf_pad_scores.json tol")
    # the P-L sentences (four decimals)
    for m in ("LUNA", "SOL", "OP5"):
        d = PR["P-L1"]["per_model"][m]
        chk(f"C.2 P-L1: {m} minus the lookup {d['delta']:+.4f} (reliably above: {d['reliably_above']})", f"{d['delta']:+.4f}", f"{mlp[m]['delta']:+.4f}", "predictions/P-L1 per_model against minus_lookup")
        assert d["reliably_above"] == (rel(mlp[m]) and mlp[m]["delta"] > 0)
    for m in ("MINI", "H45"):
        d = PR["P-L2"]["per_model"][m]
        chk(f"C.2 P-L2: {m} minus the lookup {d['delta']:+.4f} (reliably above: {d['reliably_above']})", f"{d['delta']:+.4f}", f"{mlp[m]['delta']:+.4f}", "predictions/P-L2 per_model against minus_lookup")
    # Opus's recorded draw 1 (descriptive)
    D1 = S["descriptive"]["opus_recorded_draw1"]
    for sl in ("superseded", "whole"):
        d = D1[sl]["padded_minus_d1_pooled"]
        chk(f"C.2: Opus's recorded draw 1 alone, {sl}, pooled", f"{D1[sl]['pooled_unpadded_d1']:.4f}", f"{d['b_auroc']:.4f}", f"descriptive/opus_recorded_draw1/{sl}")
        chk(f"C.2: Opus padded minus its recorded draw 1, {sl} (reliable)", f"{d['delta']:+.4f}", f"{d['a_auroc'] - d['b_auroc']:+.4f}", "the same block: a_auroc - b_auroc", reliable=True, actual_reliable=rel(d) and d["delta"] < 0)
    chk("C.2: 'the fall is not the draw count' (the one-draw padded row minus the recorded draw 1 is reliable and as large as minus the five-draw row, within 0.01)", "not the draw count",
        "not the draw count" if rel(D1["superseded"]["padded_minus_d1_pooled"]) and abs(D1["superseded"]["padded_minus_d1_pooled"]["delta"] - loss["OP5"]["delta"]) < 0.01 else "unclear",
        f"padded minus draw 1 {D1['superseded']['padded_minus_d1_pooled']['delta']:+.4f} against padded minus the five-draw row {loss['OP5']['delta']:+.4f}")
    # the seed spot-check
    SS = S["descriptive"]["seed_spot_check"]
    def reg(k):
        mm = k.split("_")[0]
        return rel(ML[mm]["LOOKUP"]["superseded"]["padded"]["pooled"]) if k.endswith("_minus_LOOKUP") else rel(RD[mm]["superseded"]["pooled"]["padded_minus_unpadded"])
    changes = [(k, s) for k, v in SS.items() for s, r in v.items() if (r["item"] and r["persona"]) != reg(k)]
    moves = [(k, s, w) for k, v in SS.items() for s, r in v.items() for w in ("item", "persona") if r[w] != reg(k)]
    chk("C.2: seeds 43 to 46 change no registered reading", "0", len(changes), f"descriptive/seed_spot_check: {changes}")
    chk("C.2: one interval of one difference moves (mini minus the lookup, seed 45, persona)", "MINI_minus_LOOKUP/45/persona", "; ".join("/".join(x) for x in moves), "descriptive/seed_spot_check")
    chk("C.2: the seeds", "43-46", f"{min(int(s) for v in SS.values() for s in v)}-{max(int(s) for v in SS.values() for s in v)}", "descriptive/seed_spot_check keys")
    # the served identifiers
    served = {c: list(S["census"][c]["served"].keys()) for c in S["census"]}
    chk("C.2: every lane served one identifier and every row was OK", "one each, 0 not OK", "one each, 0 not OK" if all(len(v) == 1 and S["census"][c]["served_ok"] for c, v in served.items()) and all(S["census"][c]["not_ok"] == 0 for c in S["census"]) else "other", f"census/*/served {served}")
    # ---- Figure 1: the transcribed summary lines and the tag route's record
    totals, hobbies, sup_names = fig1_lines()
    for st, v in (("active", 377), ("superseded", 197), ("retracted", 1), ("expired", 49)):
        chk(f"Figure 1: LIFECYCLE TOTALS {st}", str(v), totals[st], "ARTIFACT/manifests/indexes_v2.json frbank:david:FULL:BELIEVED, LIFECYCLE TOTALS (transcribed, as AUX-R86-INDEX-EXCERPT transcribes the same summary's category rows)")
    chk("Figure 1: HOBBIES_RECREATION's first names", "current_reading_list, hiking_experience, hiking_preference, hiking_preference_scenery", ", ".join(hobbies[:4]), "the same summary, ATTRIBUTE NAMES BY CATEGORY")
    chk("Figure 1: the superseded-names line carries hiking_preference and exam_date", "yes", "yes" if "hiking_preference" in sup_names and "exam_date" in sup_names else "no", "the same summary, ATTRIBUTE NAMES CARRYING SUPERSEDED CONTENT")
    e, tag = tag_route_record()
    chk("Figure 1: the tag route's returned record (David's HOBBIES_RECREATION hiking_preference) carries FR-Bank's own superseded tag", "superseded", tag, f"e1_metamemory/backend_entries/frbank.json {e['entry_id']} believed_superseded {e['believed_superseded']}")
    chk("Figure 1: the record's text", "User prefers moderate difficulty hikes in the six to ten mile range.", e["text"], f"frbank.json {e['entry_id']} text")


def main():
    G.checks()
    n134 = len(G.CHECKS)
    G135.checks135()
    n135 = len(G.CHECKS)
    checks137()
    bad = [c for c in G.CHECKS if not c["ok"]]
    for c in G.CHECKS[n135:]:
        v = c["value"]
        vs = f"{v:.4f}" if isinstance(v, float) else str(v)
        rl = "" if c["reliable"] is None else f"  reliable claimed={c['reliable']} actual={c['actual_reliable']}"
        print(f"  [{'ok' if c['ok'] else 'MISMATCH'}] {c['where']}: printed {c['printed']} <- {vs}{rl}  ({c['source']})")
    print(f"r137_number_gate: {len(G.CHECKS)} checks (R134's {n134}, R135's {n135 - n134} and this pass's {len(G.CHECKS) - n135}), {len(bad)} mismatches")
    if "--built" in sys.argv:
        pf = G.printed_forms

        def printed_forms():
            main, appx = pf()
            extra135 = {"0.65", "0.13", "0.95", "0.88", "0.97", "0.01", "0.28", "0.33", "0.06", "0.04", "0.50", "0.02", "0.67", "0.60", "0.14",
                        "0.73", "0.82", "0.75", "0.71", "0.59", "0.12", "90", "69", "2,333", "1", "452", "15", "35", "60", "88", "115", "10"}
            extra137 = {"0.92", "0.74", "0.18", "0.07", "0.09", "0.10", "102", "33",          # row 9, 5.2, the abstract, the recount
                        "377", "197", "49"}                                                  # Figure 1's LIFECYCLE TOTALS (transcribed)
            appx137 = {"0.18", "0.13", "0.14",            # tab:provenance's row prints the body's two-decimal forms, as the paraphrase row prints 0.02
                       "264", "57", "41.5", "71", "102", "121", "43", "8.11", "15.54", "2,220", "2220", "0.9317", "0.9716", "-0.2236", "-0.2776", "-0.1690", "-0.3416", "-0.1294",
                       "0.8400", "0.8682", "-0.1873", "-0.2277", "-0.1476", "-0.2569", "-0.1278", "45", "46", "0.05", "60", "20", "12", "5", "1", "4", "2", "0", "88", "444", "148",
                       "+0.1375", "+0.1274", "-0.0336", "-0.0062", "-0.0525", "-0.1807", "0.1375", "0.1274", "0.0336", "0.0062", "0.0525", "0.1807", "9", "33", "102", "30", "90"}
            return main | extra135 | extra137, appx | appx137
        G.printed_forms = printed_forms
        # the CFPAD fragments' numerals join the PARA fragments' in built_checks (RES.glob('para_tab_*.tex')): read here and added through the prose set
        frag = set()
        for f in sorted((ROOT / "cf_pad" / "results").glob("cfpad_tab_*.tex")):
            frag |= G.numerals(f.read_text(encoding="utf-8"))
        frag = {t.lstrip("+") for t in frag} | frag
        pf2 = G.printed_forms

        def printed_forms2():
            main, appx = pf2()
            return main, appx | frag
        G.printed_forms = printed_forms2
        bad += G.built_checks()
    if bad:
        print("r137_number_gate: FAIL")
        sys.exit(1)
    print("r137_number_gate: PASS")


if __name__ == "__main__":
    main()
