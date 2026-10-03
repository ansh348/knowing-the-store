"""audit_step8.py -- step 8 of the downstream audit: the paired ALWAYS -> ORACLE decomposition, the D.4 -> A3 transitions,
the mini-vs-Haiku pairing, the verdicts as the author ruled them (2026-09-14, evening), and the report
reviews/DOWNSTREAM_AUDIT.md rendered from the step artifacts. Imports audit_ds (gates re-run; no API path).

Run after audit_ds.py: python reviews/downstream_audit/audit_step8.py
"""
from __future__ import annotations

import collections
import io
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import audit_ds as A                                                          # noqa: E402
from scipy import stats as SS                                                 # noqa: E402

OUT, REPORT = A.OUT, A.REPORT
J, jdump, rate, r4 = A.J, A.jdump, A.rate, A.r4


def mcnemar(b, c):
    """Exact two-sided McNemar on the discordant pair counts (b: yes->no, c: no->yes)."""
    n = b + c
    return None if n == 0 else r4(min(1.0, 2 * SS.binom.cdf(min(b, c), n, 0.5)))


def transitions(flag_a, flag_b, keys):
    c = collections.Counter()
    for k in keys:
        c[f"{bool(flag_a(k))}->{bool(flag_b(k))}"] += 1
    return {"FF": c["False->False"], "TT": c["True->True"], "FT": c["False->True"], "TF": c["True->False"], "mcnemar_p": mcnemar(c["True->False"], c["False->True"])}


# ------------------------------------------------------------------ (b) paired ALWAYS -> policy decomposition
def decompose(C, L, policy, flag="stale_use_tau_gold"):
    """PN scorable items: reached under ALWAYS (identical view under `policy` / extended view) vs newly reached under `policy`;
    flags and rates on each part; plus items whose ALWAYS top-5 already carries an ACTIVE line asserting the stale value."""
    V = C.views; st1 = C.st1; lines = C.step4b["view_lines"]
    out = {"identical_view": {"n": 0, "k": 0}, "extended_view": {"n": 0, "trans": collections.Counter()}, "newly_reached": {"n": 0, "k": 0},
           "always_rate": None, "policy_rate_on_always_set": None, "newly_reached_rate": None, "policy_rate_all": None,
           "not_reached_under_always_but_active_stale_in_top5": 0, "abstained_under_policy": 0}
    kA_always = kA_policy = nA = 0
    for it in C.pn:
        if it["state"] == "exp":
            continue
        iid = it["item_id"]; sA, sP = st1[iid]["ALWAYS"], st1[iid][policy]
        keyA, keyP = f"{iid}|{V[iid]['ALWAYS']['sha']}", f"{iid}|{V[iid][policy]['sha']}"
        if sP["abstain"]:
            out["abstained_under_policy"] += 1
        if sA["reach"]:
            if sP["abstain"] or not sP["reach"]:
                continue
            nA += 1
            fA = bool(L.reg[keyA].get(flag)) if keyA in L.reg else False
            fP = bool(L.reg[keyP].get(flag)) if keyP in L.reg else False
            kA_always += fA; kA_policy += fP
            if keyA == keyP:
                out["identical_view"]["n"] += 1; out["identical_view"]["k"] += fA
            else:
                out["extended_view"]["n"] += 1; out["extended_view"]["trans"][f"{fA}->{fP}"] += 1
        else:
            if lines.get(f"{iid}|ALWAYS", {}).get("any_active_stale"):
                out["not_reached_under_always_but_active_stale_in_top5"] += 1
            if sP["reach"] and not sP["abstain"] and keyP in L.reg:
                out["newly_reached"]["n"] += 1; out["newly_reached"]["k"] += bool(L.reg[keyP].get(flag))
    out["extended_view"]["trans"] = dict(out["extended_view"]["trans"])
    out["always_rate"] = rate(kA_always, nA); out["policy_rate_on_always_set"] = rate(kA_policy, nA)
    out["newly_reached_rate"] = rate(out["newly_reached"]["k"], out["newly_reached"]["n"])
    out["policy_rate_all"] = rate(kA_policy + out["newly_reached"]["k"], nA + out["newly_reached"]["n"])
    return out


def step8(C):
    # ---- (b) decomposition for every lane and every gated policy vs ALWAYS
    dec = {}
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        L = C.lanes[lid]; dec[lid] = {}
        for p in ("ORACLE", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT"):
            dec[lid][p] = {"stale_use_tau_gold": decompose(C, L, p, "stale_use_tau_gold"), "stale_use": decompose(C, L, p, "stale_use")}
    # sanity: ORACLE all == registered scorable count from step 2
    s2 = J(OUT / "step2_rescore.json")["tables"]
    for lid in dec:
        a = dec[lid]["ORACLE"]["stale_use_tau_gold"]["policy_rate_all"]; b = s2[lid]["ORACLE"]["all"]["stale_use_tau_gold"]["scorable"]
        assert (a["k"], a["n"]) == (b["k"], b["n"]), (lid, a, b)
    # ---- (d) D.4 -> A3 transitions per answerer on the shared keys
    a3 = {}
    for base, inst in (("mini-D4", "mini-A3"), ("h45-D4", "h45-A3")):
        B, I = C.lanes[base], C.lanes[inst]; keys = sorted(set(B.rows) & set(I.rows))
        ident = sum(1 for k in keys if (B.rows[k]["answer"] or "") == (I.rows[k]["answer"] or ""))
        ident_cf = sum(1 for k in keys if A.norm(B.rows[k]["answer"]) == A.norm(I.rows[k]["answer"]))
        jac = 0
        for k in keys:
            d = C.rec[B.rows[k]["item_id"]]["drop"]; ta, tb = A.toks(B.rows[k]["answer"] or "", d), A.toks(I.rows[k]["answer"] or "", d)
            jac += (len(ta & tb) / len(ta | tb) if (ta | tb) else 1.0) >= 0.9
        pn = [k for k in keys if B.rows[k]["label"] == "PRESENT-NEGATIVE" and C.scorable(k, B)]
        pr = [k for k in keys if B.rows[k]["label"] == "PRESENT"]
        pn_inview = [k for k in pr if C.st1[B.rows[k]["item_id"]]["ORACLE"]["gold_in_view"]]
        a3[f"{base}->{inst}"] = {
            "n_keys": len(keys), "answer_identical": ident, "answer_identical_casefold": ident_cf, "answer_token_jaccard_ge_0.9": jac,
            "identical_pn": sum(1 for k in pn if (B.rows[k]["answer"] or "") == (I.rows[k]["answer"] or "")), "n_pn_scorable": len(pn),
            "identical_present": sum(1 for k in pr if (B.rows[k]["answer"] or "") == (I.rows[k]["answer"] or "")), "n_present": len(pr),
            "stale_use_tau_gold": transitions(lambda k: B.reg[k].get("stale_use_tau_gold"), lambda k: I.reg[k].get("stale_use_tau_gold"), pn),
            "stale_use": transitions(lambda k: B.reg[k].get("stale_use"), lambda k: I.reg[k].get("stale_use"), pn),
            "correct": transitions(lambda k: B.reg[k].get("correct"), lambda k: I.reg[k].get("correct"), pr),
            "abstention_present": {"D4": rate(sum(1 for k in pr if A.is_abst(B.rows[k]["answer"])), len(pr)), "A3": rate(sum(1 for k in pr if A.is_abst(I.rows[k]["answer"])), len(pr))},
            "abstention_present_in_view": {"D4": rate(sum(1 for k in pn_inview if A.is_abst(B.rows[k]["answer"])), len(pn_inview)), "A3": rate(sum(1 for k in pn_inview if A.is_abst(I.rows[k]["answer"])), len(pn_inview))},
            "abstention_pn": {"D4": rate(sum(1 for k in pn if A.is_abst(B.rows[k]["answer"])), len(pn)), "A3": rate(sum(1 for k in pn if A.is_abst(I.rows[k]["answer"])), len(pn))},
        }
    # ---- (c) mini vs Haiku paired on the ORACLE scorable PN keys and on the PRESENT keys
    M, H = C.lanes["mini-D4"], C.lanes["h45-D4"]
    orc = sorted(k for k, r in M.rows.items() if "ORACLE" in M.policies_of(k) and r["label"] == "PRESENT-NEGATIVE" and C.scorable(k, M) and k in H.rows)
    pres = sorted(k for k, r in M.rows.items() if "ORACLE" in M.policies_of(k) and r["label"] == "PRESENT" and k in H.rows)
    labs = J(OUT / "step4_labels.json")
    gives = lambda lid, k: (labs["stale"][lid].get(k) or {}).get("label") == "gives_stale_value"        # noqa: E731
    pair = {"n_oracle_pn_scorable": len(orc),
            "stale_use_tau_gold": transitions(lambda k: M.reg[k].get("stale_use_tau_gold"), lambda k: H.reg[k].get("stale_use_tau_gold"), orc),
            "stale_use": transitions(lambda k: M.reg[k].get("stale_use"), lambda k: H.reg[k].get("stale_use"), orc),
            "gives_stale_value_by_label": transitions(lambda k: gives("mini-D4", k), lambda k: gives("h45-D4", k), orc),
            "n_present": len(pres), "correct": transitions(lambda k: M.reg[k].get("correct"), lambda k: H.reg[k].get("correct"), pres),
            "registered_oracle_all_states": {"mini": J(OUT / "step2_rescore.json")["tables"]["mini-D4"]["ORACLE"]["all"]["stale_use_tau_gold"]["registered"],
                                             "h45": J(OUT / "step2_rescore.json")["tables"]["h45-D4"]["ORACLE"]["all"]["stale_use_tau_gold"]["registered"]},
            "expiry_flags_in_registered_oracle": {"mini": sum(1 for k, r in M.rows.items() if "ORACLE" in M.policies_of(k) and r["label"] == "PRESENT-NEGATIVE" and not C.scorable(k, M) and M.reg[k].get("stale_use_tau_gold")),
                                                  "h45": sum(1 for k, r in H.rows.items() if "ORACLE" in H.policies_of(k) and r["label"] == "PRESENT-NEGATIVE" and not C.scorable(k, H) and H.reg[k].get("stale_use_tau_gold"))}}
    # ---- (a) construction and the abstention decomposition on the 65 in-view PRESENT items (ALWAYS view)
    gv = J(OUT / "gate_views.json"); s5 = J(OUT / "step5_coverage.json"); s4 = J(OUT / "step4_counts.json"); s4b = C.step4b; s1 = J(OUT / "step1_synthetic.json"); rk = J(OUT / "step5_ranks.json")
    inview = [it for it in C.present if C.st1[it["item_id"]]["ALWAYS"]["gold_in_view"]]
    a_part = {}
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        L = C.lanes[lid]; c = collections.Counter()
        for it in inview:
            k = f"{it['item_id']}|{C.views[it['item_id']]['ALWAYS']['sha']}"; r = L.rows[k]; s = L.reg[k]
            ab = A.is_abst(r["answer"]); co = bool(s.get("correct"))
            c["n"] += 1; c["correct"] += co; c["abstained"] += ab; c["answered_incorrect"] += (not co) and not ab
            c["correct_and_abstained"] += co and ab; c["correct_not_abstained"] += co and not ab
        c["correct_among_answered"] = rate(c["correct_not_abstained"], c["n"] - c["abstained"])
        a_part[lid] = dict(c)
    verd = {
        "a_flat_correct": {
            "verdict": "construction (ALWAYS vs ORACLE) + abstention over a persona-binding gap, bounded by retrieval rank",
            "construction": {"oracle_sha_equals_always_present": gv["present_view_identity"]["oracle_sha_equals_always"], "n_present": gv["present_view_identity"]["n_present"],
                             "present_views_differing_from_always_by_policy": gv["present_view_identity"]["present_views_differing_from_always_by_policy"],
                             "reading": "ORACLE never fetches on a PRESENT item, so its view is ALWAYS's byte for byte; 'correct stays flat' between them is an identity. The gated policies change the PRESENT view only by abstention (fewer answered) and by tagged fetched lines."},
            "in_view_65": a_part,
            "identity_gap": {"per_lane": s4b["identity"]["per_lane"], "persona_name_in_view": s4b["identity"]["persona_name_in_view"], "questions_naming_persona": s4b["identity"]["present_questions_naming_persona"]},
            "labels_28": s4["present"]["mini-D4"], "labels_27_h45": s4["present"]["h45-D4"],
            "retrieval_rank": {k: rk["best_rank_per_item"][k] for k in ("PRESENT", "PRESENT-NEGATIVE", "PRESENT-NEGATIVE|sup", "PRESENT-NEGATIVE|ret", "PRESENT-NEGATIVE|exp")},
            "coverage_by_definition": s5["coverage"]["present"]["ALWAYS"], "in_view_correct_by_definition": {lid: s5["in_view_correct"][lid]["ALWAYS"] for lid in ("mini-D4", "h45-D4")},
            "detector_ceiling_present": {"any_gold_entry_text_passes": s1["panel_b"]["present"]["any_pass"], "n_with_gold": s1["panel_b"]["present"]["n_with_gold"], "no_pass_items": [x["item_id"] for x in s1["panel_b"]["present"]["no_pass"]]}},
        "b_stale_rising_with_reach": {
            "verdict": "reporting artifact: counts over a growing denominator; rates flat with overlapping Wilson intervals; stale answers arise only from active lines asserting the stale value (mini), plus five qualified mentions (Haiku)",
            "decomposition": dec, "rates_scorable": {lid: {p: s2[lid][p]["all"]["stale_use_tau_gold"]["scorable"] for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE")} for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3")},
            "registered_counts": {lid: {p: s2[lid][p]["all"]["stale_use_tau_gold"]["registered"] for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE")} for lid in ("mini-D4", "h45-D4")},
            "active_stale_source": {"oracle_summary": s4b["oracle_summary"], "crosstabs_oracle": {lid: s4b["crosstabs"][lid]["ORACLE"] for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3")},
                                    "crosstabs_always": {lid: s4b["crosstabs"][lid]["ALWAYS"] for lid in ("mini-D4", "h45-D4")}}},
        "c_haiku_above_mini": {
            "verdict": "instrument: unscorable expiry (8 vs 1 of the registered 27 vs 17) plus qualified mentions in second sentences scored by a one-directional coverage detector; on 'gives the stale value' Haiku is at or below mini",
            "paired_oracle": pair, "labels": {"mini": s4["stale"]["mini-D4"], "h45": s4["stale"]["h45-D4"], "cross": s4["cross"]},
            "length": {k: J(OUT / "step7_length.json")[k] for k in ("paired_lanes", "pooled_logistic")},
            "length_controls_oracle": J(OUT / "step7_length.json")["length_controls"]["h45-D4"]["ORACLE"],
            "first_sentence": {lid: J(OUT / "step3_scored_text.json")["rescore"][lid]["ORACLE"]["pn"]["stale_use_tau_gold"] for lid in ("mini-D4", "h45-D4")}},
        "d_inert_instruction": {
            "verdict": "redundant for mini (answers byte-identical), mis-targeted for both: the instruction addresses tagged lines and the stale sources are active (untagged) lines",
            "transitions": a3, "active_stale_source_a3": {lid: s4b["crosstabs"][lid]["ORACLE"]["stale_x_active_stale_line"] for lid in ("mini-A3", "h45-A3")}},
        "disclosures": {
            "detector_step1": {"expiry_unscorable": s1["panel_a"]["counts"].get("pn.unscorable_expiry"), "pn_member_text_never_fires": [(x["item_id"], x["state"]) for x in s1["panel_b"]["pn"]["none_tg"]],
                               "pn_any_member_text_fires": [s1["panel_b"]["pn"]["any_tg"], s1["panel_b"]["pn"]["n_scorable"]], "successor_text_fires": [(x["item_id"], x["entry"]) for x in s1["panel_b"]["pn"]["successor_text_fires"]],
                               "present_gold_text_never_passes": [x["item_id"] for x in s1["panel_b"]["present"]["no_pass"]], "present_any_gold_text_passes": [s1["panel_b"]["present"]["any_pass"], s1["panel_b"]["present"]["n_with_gold"]],
                               "present_no_licensed_id": len(s1["panel_b"]["present"]["no_licensed_id"]), "old_fact_read_as_correct_present": s1["panel_a"]["informational"]},
            "view_step4b": {"oracle_views_with_active_stale_line": [s4b["oracle_summary"]["oracle_any_active_stale"], s4b["oracle_summary"]["n_scorable"]], "by_state": s4b["oracle_summary"]["by_state_oracle_active_stale"],
                            "negation_mistag_example": "frbank:fatima:fatima_q06:FULL -- the retraction statement ('decided not to launch ... Oud and Geometry') carries the retracted tag (covers 4 of 5 original-plan tokens at 0.80; the join has no negation handling) while the plan records stay active ('launching' is not 'launch')",
                            "identity": s4b["identity"]},
            "retrieval_rank": rk["best_rank_per_item"], "retrieval_config": rk["config"]}}
    jdump(verd, OUT / "step8_verdicts.json")
    return verd


# ------------------------------------------------------------------ the report
def f_rate(r):
    return f"{r['k']}/{r['n']} = {r['rate']:.3f} [{r['wilson'][0]:.2f}, {r['wilson'][1]:.2f}]" if r and r.get("n") else "n/a"


def f_kn(r):
    return f"{r['k']}/{r['n']}" if r and r.get("n") is not None else "n/a"


def write_report(C, V):
    s1 = J(OUT / "step1_synthetic.json"); s2 = J(OUT / "step2_rescore.json"); s2o = J(OUT / "step2_overlap.json"); s3 = J(OUT / "step3_scored_text.json")
    s4 = J(OUT / "step4_counts.json"); s4b = J(OUT / "step4b_view_lines.json"); s5 = J(OUT / "step5_coverage.json"); rk = J(OUT / "step5_ranks.json")
    s6 = J(OUT / "step6_render.json"); s7 = J(OUT / "step7_length.json"); gd = J(OUT / "gate_detector.json"); gr = J(OUT / "gate_retrieval.json"); gv = J(OUT / "gate_views.json")
    L = []
    w = L.append
    w("# Forensic audit of the downstream pipeline (`ds_downstream/`)")
    w("")
    w("Auditor: Claude (this session), 2026-09-14. Scope: the brief of 2026-09-14 (eight steps) with the author's three additions at approval and the step-8 rulings of the same evening. "
      "No paper edit, no registration edit, no model call in this audit; every number below is read from an artifact under `reviews/downstream_audit/` written by `audit_ds.py` / `audit_step8.py` (`manifest.json` holds the input and output sha256s). "
      "The 15 expiry obligations are unscorable for every stale diagnostic (the YAML gold field is the expired fact, so the gold string equals the stale string); the registered column is left as registered and diagnostic columns run on the scorable (supersession + retraction) reached set. "
      "Step-4 classifications are the auditor's read (`step4_labels.json`); the v12/v16 labeling sheets remain the human-validation instrument.")
    w("")
    w("## Verdicts")
    w("")
    w("| anomaly | registered | diagnostic beside it | verdict |")
    w("|---|---|---|---|")
    a = V["a_flat_correct"]; b = V["b_stale_rising_with_reach"]; c = V["c_haiku_above_mini"]; d = V["d_inert_instruction"]
    mo = b["decomposition"]["mini-D4"]["ORACLE"]["stale_use_tau_gold"]; ho = b["decomposition"]["h45-D4"]["ORACLE"]["stale_use_tau_gold"]
    w(f"| (a) flat correct | 46/174 under every mini policy; 48/174 Haiku | ORACLE view = ALWAYS view for {a['construction']['oracle_sha_equals_always_present']}/{a['construction']['n_present']} PRESENT items; on the 65 in-view items mini abstains on {a['in_view_65']['mini-D4']['abstained']} and Haiku on {a['in_view_65']['h45-D4']['abstained']}; "
      f"Haiku names the persona-binding gap in {a['identity_gap']['per_lane']['h45-D4']['abstained_identity_reason']} of {a['identity_gap']['per_lane']['h45-D4']['abstained']} abstentions; persona name in {a['identity_gap']['persona_name_in_view']['present_views_with_persona_name']}/174 views, in {a['identity_gap']['questions_naming_persona']['k']}/174 questions; licensed record median best rank {a['retrieval_rank']['PRESENT']['median']} | "
      "**construction** for ALWAYS vs ORACLE; the gated drop is **abstention** driven by the persona-binding gap and bounded by retrieval rank |")
    w(f"| (b) stale rising with reach | counts 9 → 17 (mini), 19 → 27 (Haiku) | rates on the scorable reached set: mini {f_rate(b['rates_scorable']['mini-D4']['ALWAYS'])} → {f_rate(b['rates_scorable']['mini-D4']['ORACLE'])}; Haiku {f_rate(b['rates_scorable']['h45-D4']['ALWAYS'])} → {f_rate(b['rates_scorable']['h45-D4']['ORACLE'])}; "
      f"paired on the items reached under ALWAYS: mini {f_kn(mo['always_rate'])} → {f_kn(mo['policy_rate_on_always_set'])}, newly reached {f_kn(mo['newly_reached_rate'])}; Haiku {f_kn(ho['always_rate'])} → {f_kn(ho['policy_rate_on_always_set'])}, newly reached {f_kn(ho['newly_reached_rate'])}; "
      f"mini's stale answers: {s4b['crosstabs']['mini-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=True', 0)} with an active line asserting the stale value, {s4b['crosstabs']['mini-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=False', 0)} without | **reporting artifact** |")
    w(f"| (c) Haiku above mini | ORACLE 27 vs 17 at 0.50 | expiry flags {c['paired_oracle']['expiry_flags_in_registered_oracle']['h45']} vs {c['paired_oracle']['expiry_flags_in_registered_oracle']['mini']}; scorable {c['paired_oracle']['registered_oracle_all_states']['h45']['k'] - c['paired_oracle']['expiry_flags_in_registered_oracle']['h45']} vs {c['paired_oracle']['registered_oracle_all_states']['mini']['k'] - c['paired_oracle']['expiry_flags_in_registered_oracle']['mini']} of 85; "
      f"first sentence {f_kn(c['first_sentence']['h45-D4']['first_sentence'])} vs {f_kn(c['first_sentence']['mini-D4']['first_sentence'])}; cut to mini's length {f_kn(c['length_controls_oracle']['stale_use_tau_gold']['haiku_trunc_to_mini_len'])}; "
      f"'gives the stale value' by read: mini {c['labels']['mini']['labels'].get('gives_stale_value', 0)}, Haiku {c['labels']['h45']['labels'].get('gives_stale_value', 0)} | **instrument** |")
    t = d["transitions"]
    w(f"| (d) inert instruction | ≤3 moves | answers byte-identical D.4 → A3: mini {t['mini-D4->mini-A3']['answer_identical']}/{t['mini-D4->mini-A3']['n_keys']}, Haiku {t['h45-D4->h45-A3']['answer_identical']}/{t['h45-D4->h45-A3']['n_keys']}; stale transitions (scorable PN) mini F→T {t['mini-D4->mini-A3']['stale_use_tau_gold']['FT']} / T→F {t['mini-D4->mini-A3']['stale_use_tau_gold']['TF']}, Haiku {t['h45-D4->h45-A3']['stale_use_tau_gold']['FT']} / {t['h45-D4->h45-A3']['stale_use_tau_gold']['TF']}; "
      f"the stale sources are active lines in {s4b['oracle_summary']['oracle_any_active_stale']}/{s4b['oracle_summary']['n_scorable']} scorable views, which the instruction does not address | **redundant** for mini, **mis-targeted** for both |")
    w("")
    # ---- gates
    w("## Gates")
    w("")
    w(f"- Detector replica (verbatim `records` + `score_answer`): {gd['summary']['row_mismatches']} mismatches over {gd['summary']['rows_total']} rows in five lanes; {gd['summary']['aggregate_mismatches']} of {gd['summary']['aggregate_cells']} registered per-policy cells differ (`gate_detector.json`).")
    w(f"- Retrieval replay (`LifecycleBank.cosine_search_all` over pinned vectors): top-5 = ALWAYS ids and top-10 = L2 for {gr['n_ok']}/{gr['n_items']} items; store sizes {gr['store_size']['min']}–{gr['store_size']['max']} (`gate_retrieval.json`).")
    w(f"- Views: {gv['n_lines']} lines parse; `n_lines == len(ids)`; every line's text equals the TRUE-join entry text ({gv['render_lock_failures']} failures); tag vocabulary {gv['tag_vocabulary']} (`gate_views.json`).")
    w(f"- Prompts: `SYSTEM_ANSWER`/`USER_ANSWER` digests as ledgered (AUX-DS-PROMPT); `SYSTEM_ANSWER_A3` as locked (`gate_prompts.json`).")
    w(f"- ORACLE and ALWAYS share the PRESENT view for {gv['present_view_identity']['oracle_sha_equals_always']}/{gv['present_view_identity']['n_present']} items (by construction).")
    w("")
    # ---- step 1
    pa = s1["panel_a"]["counts"]; pb = s1["panel_b"]
    w("## Step 1 — detector validity by construction (`step1_synthetic.json`)")
    w("")
    w(f"Panel A (the YAML strings the detector uses as reference): gold → correct {pa['present.gold->correct']}/{pa['present.n']}; abstention → correct {pa['present.abst->correct']}; stale string → stale {pa['pn.stale->stale_tg']}/{pa['pn.n_scorable']} at 0.50 and {pa['pn.stale->stale_hi']} at 0.80; gold string → stale {pa['pn.gold->stale_tg']}; abstention → any flag {pa['pn.abst->any_flag']}. "
      f"Unscorable: {pa['pn.unscorable_expiry']} expiry obligations (gold ≡ stale). Informational: {s1['panel_a']['informational']['present.old_fact->correct']} of the {s1['panel_a']['informational']['present.has_old_fact']} PRESENT items with an old fact would read that old fact as correct.")
    w("")
    w(f"Panel B (the rendered store texts the model can echo): a licensed gold entry text passes `correct` for {pb['present']['any_pass']}/{pb['present']['n_with_gold']} PRESENT items (all entries {pb['present']['all_pass']}); none passes for {', '.join(x['item_id'] for x in pb['present']['no_pass'])}; {len(pb['present']['no_licensed_id'])} PRESENT items have no licensed id (all `expiring_logistics`). "
      f"A forbidding entry text fires the stale flag for {pb['pn']['any_tg']}/{pb['pn']['n_scorable']} scorable obligations at 0.50 ({pb['pn']['any_hi']} at 0.80); none fires for {', '.join(x['item_id'] for x in pb['pn']['none_tg'])} — these cannot be flagged even if the store line is echoed verbatim. "
      f"{len(pb['pn']['successor_text_fires'])} of {pb['pn']['n_successor_texts']} successor entry texts fire the stale flag ({', '.join(sorted({x['item_id'] for x in pb['pn']['successor_text_fires']}))}). Metadata tokens on the rendered line flip no verdict ({pb['present']['line_with_metadata_flips']}/{pb['pn']['line_with_metadata_flips']}).")
    w("")
    # ---- step 2
    w("## Step 2 — old-versus-new overlap (`step2_overlap.json`, `step2_rescore.json`)")
    w("")
    w(f"`fwd = cov(toks(gold), toks(stale))` ≥ 0.50 for {s2o['set_sizes']['E_fwd']} of {s2o['n_scorable']} scorable obligations ({', '.join(s2o['exclusion_sets']['E_fwd'])}); structurally unflaggable (MIN_DISCR) {s2o['set_sizes']['E_none']}; smallest discriminative set (|old-only| = 3) {s2o['set_sizes']['E_small']}. "
      "Because the stale flag is computed on old-only tokens with a cross-guard, high overlap is not the false-positive mechanism (Panel A: 0 of 89); the mechanism the sheets show is a small old-only set whose members the answer shares while restating the question (kofi_q01).")
    w("")
    w("Stale at 0.50, all states registered / scorable (expiry removed) / excluding `E_fwd`; rates with Wilson 95% on the reached set:")
    w("")
    w("| lane | policy | registered | scorable | excl. E_fwd |")
    w("|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE"):
            bb = s2["tables"][lid][p]["all"]["stale_use_tau_gold"]
            w(f"| {lid} | {p} | {f_kn(bb['registered'])} | {f_rate(bb['scorable'])} | {f_rate(bb['E_fwd'])} |")
    w("")
    # ---- step 3
    w("## Step 3 — what was scored (`step3_scored_text.json`)")
    w("")
    w(f"{s3['protocol']['scored_text']}. The brief's re-extraction branch does not apply. Per lane: " + "; ".join(f"{lid}: raws complete {v['raw_complete']}/{v['n']}, re-parse equal {v.get('reparse_equal', 0)}, fenced {v['fenced']}, preamble {v['preamble']}, max-token hits {v['hit_max_tokens']}, retries {v['retries']}" for lid, v in s3["per_lane"].items()) + ".")
    w(f"Sentences per answer: {s3['n_sentences']}.")
    w("")
    w("Diagnostic re-scores, ORACLE, scorable PN (stale at 0.50) and PRESENT (correct):")
    w("")
    w("| lane | registered (all states) | scorable | first sentence | last sentence | minus question tokens | raw reply (complete raws) | correct: registered | first sentence | minus question |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        t = s3["rescore"][lid]["ORACLE"]["pn"]["stale_use_tau_gold"]; u = s3["rescore"][lid]["ORACLE"]["present"]["correct"]
        w(f"| {lid} | {f_kn(t['registered'])} | {f_kn(t['scorable'])} | {f_kn(t['first_sentence'])} | {f_kn(t['last_sentence'])} | {f_kn(t['minus_question'])} | {f_kn(t['raw_full'])} | {f_kn(u['registered'])} | {f_kn(u['first_sentence'])} | {f_kn(u['minus_question'])} |")
    w("")
    # ---- step 4
    w("## Step 4 — the flagged answers read (`step4_sheets_stale.md`, `step4_sheets_present.md`, `step4_labels.json`, `step4_counts.json`)")
    w("")
    w(f"Source of the counts: {s4['source']}.")
    w("")
    w("| lane | flagged (ORACLE) | unscorable expiry | gives the stale value | mentions it, states superseded/retracted/cancelled | partial-overlap artifact | other (hedge / abstains yet restates) |")
    w("|---|---|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4"):
        x = s4["stale"][lid]; lb = x["labels"]
        w(f"| {lid} | {x['n_flagged']} | {x['n_unscorable_expiry']} | {lb.get('gives_stale_value', 0)} | {lb.get('mentions_but_superseded', 0)} | {lb.get('partial_overlap_artifact', 0)} | {lb.get('other', 0)} |")
    w("")
    w("By tagged reach (mini / Haiku): " + "; ".join(f"{k}: {v}" for k, v in s4["stale"]["mini-D4"]["by_tagged"].items()) + " / " + "; ".join(f"{k}: {v}" for k, v in s4["stale"]["h45-D4"]["by_tagged"].items()) + ".")
    w(f"On the same ORACLE keys: {s4['cross']['stale_mini_vs_h45_same_keys']}.")
    w("")
    w("| lane | in-view licensed items marked incorrect | abstained | correct value in a different format | wrong value | other | truncated in view |")
    w("|---|---|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4"):
        x = s4["present"][lid]; lb = x["labels"]
        w(f"| {lid} | {x['n']} | {lb.get('abstained', 0)} | {lb.get('correct_different_format', 0)} | {lb.get('wrong_value', 0)} | {lb.get('other', 0)} | {lb.get('truncated_in_view', 0)} |")
    w("")
    w("Notes from the read. kofi_q01 (both variants) answers the gold value and is flagged stale: the answer's three old-only tokens are the question's words, and the one new-only token it carries is below the cross-guard. "
      "fatima_q06: the store's `retracted` tag sits on the retraction statement ('decided not to launch ... Oud and Geometry'), which covers 4 of the 5 original-plan tokens at 0.80 with no negation handling, while the plan records stay active ('launching' is not 'launch'); Haiku reads the tag as the withdrawal being withdrawn and concludes the launch is on. "
      "Four of Haiku's flagged answers are literal abstentions that name the superseded content only to say it is superseded; three of them fire at 0.80. "
      "Haiku states the reason for its in-view PRESENT abstentions: the entries say 'User' (or a third party's name) and nothing binds that to the persona named in the question; mini abstains on the same items with the bare phrase.")
    w("")
    # ---- step 4b
    o = s4b["oracle_summary"]; idn = s4b["identity"]
    w("## Step 4b — what the view itself asserts; the persona binding (`step4b_view_lines.json`; added beyond the brief)")
    w("")
    w(f"Of the {o['n_scorable']} scorable obligations, the ORACLE view carries an **active** line whose text asserts the stale value (the item's own detector at 0.50) for {o['oracle_any_active_stale']} (supersession {o['by_state_oracle_active_stale']['sup']}, retraction {o['by_state_oracle_active_stale']['ret']}); the same {o['always_any_active_stale']} under ALWAYS, since every fetched line is tagged. "
      f"No tagged line asserts the successor ({o['oracle_any_tagged_successor']}). Stale flag × active-stale-line, ORACLE:")
    w("")
    w("| lane | stale, active stale line present | stale, none present | not stale, present | not stale, none |")
    w("|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        x = s4b["crosstabs"][lid]["ORACLE"]["stale_x_active_stale_line"]
        w(f"| {lid} | {x.get('stale=True|active_stale_line=True', 0)} | {x.get('stale=True|active_stale_line=False', 0)} | {x.get('stale=False|active_stale_line=True', 0)} | {x.get('stale=False|active_stale_line=False', 0)} |")
    w("")
    w(f"Persona binding: the persona's name appears in {idn['persona_name_in_view']['present_views_with_persona_name']}/{idn['persona_name_in_view']['present_views']} PRESENT views and {idn['persona_name_in_view']['pn_views_with_persona_name']}/{idn['persona_name_in_view']['pn_views']} obligation views; {idn['present_questions_naming_persona']['k']}/{idn['present_questions_naming_persona']['n']} PRESENT questions name the persona. "
      "PRESENT abstentions per lane (rows; identity reason by regex on the answer text): " + "; ".join(f"{lid}: {v['abstained']}/{v['present_rows']} abstained, {v['abstained_identity_reason']} with the identity reason, {v['abstained_in_view']} with the gold line in view" for lid, v in idn["per_lane"].items()) + ".")
    w("")
    # ---- step 5
    cv = s5["coverage"]["present"]["ALWAYS"]; pnr = s5["coverage"]["pn_reach"]
    w("## Step 5 — coverage validity and retrieval rank (`step5_coverage.json`, `step5_ranks.json`)")
    w("")
    w(f"Licensed record in view, PRESENT, ALWAYS view: by id {f_kn(cv['id'])}, by normalized text {f_kn(cv['text'])}, by MiniLM cosine ≥ 0.80 / 0.90 / 0.95 {f_kn(cv['emb_0.80'])} / {f_kn(cv['emb_0.90'])} / {f_kn(cv['emb_0.95'])}. "
      f"In-view correct rate (mini / Haiku) under id: {f_kn(s5['in_view_correct']['mini-D4']['ALWAYS']['id']['in_view'])} / {f_kn(s5['in_view_correct']['h45-D4']['ALWAYS']['id']['in_view'])}; under text and cosine ≥ 0.90 identical; not-in-view correct {f_kn(s5['in_view_correct']['mini-D4']['ALWAYS']['id']['not_in_view'])} / {f_kn(s5['in_view_correct']['h45-D4']['ALWAYS']['id']['not_in_view'])}. "
      f"Obligation reach by id / text / cosine ≥ 0.90: ALWAYS {f_kn(pnr['ALWAYS']['id'])} / {f_kn(pnr['ALWAYS']['text'])} / {f_kn(pnr['ALWAYS']['emb_0.90'])}; ORACLE {f_kn(pnr['ORACLE']['id'])} / {f_kn(pnr['ORACLE']['text'])} / {f_kn(pnr['ORACLE']['emb_0.90'])}. Id-based membership equals `stage1.json` for all {s5['id_vs_stage1']['agree']} item × policy cells.")
    w("")
    w(f"Retrieval configuration: {rk['config']['retriever']}; lifecycle mask: {rk['config']['lifecycle_mask']}; query: {rk['config']['query']}; k = {rk['config']['k_use']} of {rk['config']['k_take']}.")
    w("")
    w("Best rank of a licensed record per item under that retriever (full ranking replayed):")
    w("")
    w("| population | n | median | q25 | q75 | share ≤ 5 | share ≤ 10 | share > 10 |")
    w("|---|---|---|---|---|---|---|---|")
    for k in ("PRESENT", "PRESENT-NEGATIVE", "PRESENT-NEGATIVE|sup", "PRESENT-NEGATIVE|ret", "PRESENT-NEGATIVE|exp", "PRESENT|FULL", "PRESENT|CAT-ABLATED"):
        x = rk["best_rank_per_item"][k]
        w(f"| {k} | {x['n']} | {x['median']} | {x['q25']} | {x['q75']} | {x['share_le5']} | {x['share_le10']} | {x['share_gt10']} |")
    w("")
    w(f"The licensed record of a PRESENT item has median best rank {rk['best_rank_per_item']['PRESENT']['median']} (> 5: a finding under the brief's criterion) and of a supersession obligation {rk['best_rank_per_item']['PRESENT-NEGATIVE|sup']['median']}; retraction and expiry records sit at {rk['best_rank_per_item']['PRESENT-NEGATIVE|ret']['median']} and {rk['best_rank_per_item']['PRESENT-NEGATIVE|exp']['median']}. "
      f"{rk['licensed_records_not_in_store_variant']['n_records']} licensed records are absent from their item's store variant (ablated); no item loses all of them. Successor ranked above the stale record: {f_kn(rk['successor_above_stale']['sup'])} supersession, {f_kn(rk['successor_above_stale']['ret'])} retraction items with both in store.")
    w("")
    # ---- step 6
    w("## Step 6 — render check (`step6_render.md`, `step6_render.json`)")
    w("")
    w(f"Three complete prompts are printed in `step6_render.md` ({', '.join(f'{k}: {v}' for k, v in s6['selected_items'].items())}). Tags present: {s6['tags_present_in_views']}; explained in the system prompt: {s6['tags_explained_in_system_prompt']}; format: {s6['tag_format']}. "
      f"Pinned time or current date given: {s6['pinned_time_or_current_date_given']} ({s6['time_information_per_line']}); Haiku says so on marcus_q10 ('cannot confirm this delivery is still upcoming without knowing the current date'). "
      f"Truncation: `n_lines == len(ids)` for every view ({s6['truncation']['views_n_lines_equals_ids']}), max {s6['truncation']['max_view_lines']} lines, '(+N more)' fragments {s6['truncation']['plus_more_fragments']}, no answer at the token cap. Question present: {s6['question_present']}. Parse failures {s6['parse_failures_total']}; the 'Final answer:' re-run is not triggered.")
    w("")
    # ---- step 7
    w("## Step 7 — length (`step7_length.json`)")
    w("")
    pl = s7["paired_lanes"]["h45-D4/mini-D4"]; cm = s7["correlation"]["mini-D4"]["PRESENT-NEGATIVE|stale_use_tau_gold"]; ch = s7["correlation"]["h45-D4"]["PRESENT-NEGATIVE|stale_use_tau_gold"]; po = s7["pooled_logistic"]["stale_use_tau_gold"]
    w(f"Median answer length on the same {pl['n']} views: Haiku {pl['median_chars']['h45-D4']} characters, mini {pl['median_chars']['mini-D4']} (median ratio {pl['median_char_ratio']}). Within scorable obligation rows, the stale flag against log length: mini r = {cm['pointbiserial_log_chars']['r']} (p = {cm['pointbiserial_log_chars']['p']}), Haiku r = {ch['pointbiserial_log_chars']['r']} (p = {ch['pointbiserial_log_chars']['p']}); "
      f"odds ratio per doubling of length {cm['logistic_log_chars']['OR_per_doubling']} (mini) and {ch['logistic_log_chars']['OR_per_doubling']} (Haiku); flagged answers are longer (medians {cm['mannwhitney_chars']['median_flagged']} vs {cm['mannwhitney_chars']['median_unflagged']} mini, {ch['mannwhitney_chars']['median_flagged']} vs {ch['mannwhitney_chars']['median_unflagged']} Haiku). "
      f"Pooled logit P(stale) = b0 + b1·log(chars) + b2·is_haiku on {po['n']} rows: b1 = {po['fit']['coef'][1]} (z {po['fit']['z'][1]}), b2 = {po['fit']['coef'][2]} (z {po['fit']['z'][2]}) — conditioned on length, Haiku is less likely to be flagged.")
    w("")
    w("Length controls, ORACLE, scorable obligations (stale at 0.50 / at 0.80):")
    w("")
    lc = s7["length_controls"]["h45-D4"]["ORACLE"]
    w("| column | 0.50 | 0.80 |")
    w("|---|---|---|")
    for k, lab in (("registered_mini", "mini, registered"), ("registered_haiku", "Haiku, registered"), ("haiku_first_sentence", "Haiku, first sentence"), ("haiku_trunc_to_mini_len", "Haiku cut to mini's length")):
        w(f"| {lab} | {f_kn(lc['stale_use_tau_gold'][k])} | {f_kn(lc['stale_use'][k])} |")
    w("")
    # ---- step 8 detail
    w("## Step 8 — verdicts in detail (`step8_verdicts.json`)")
    w("")
    w("### (a) Flat correct")
    w("")
    w(f"ORACLE and ALWAYS share the PRESENT view for all {a['construction']['oracle_sha_equals_always_present']} of {a['construction']['n_present']} items by construction (ORACLE fetches nothing on a PRESENT item), so 'correct stays flat across policies' is an identity for those two; only the gated policies' abstentions can move it "
      f"(PRESENT views differing from ALWAYS: {a['construction']['present_views_differing_from_always_by_policy']}). On the 65 items whose licensed record is in view: " + "; ".join(f"{lid}: detector-correct {v['correct']} (of which {v['correct_and_abstained']} are abstentions whose explanation restates the gold content), abstained {v['abstained']}, answered wrongly {v['answered_incorrect']}, correct among the answered {f_kn(v['correct_among_answered'])}" for lid, v in a["in_view_65"].items()) + ". "
      f"The abstentions are driven by the persona-binding gap: the view prints 'User' and never binds it to the name in the question (name in {a['identity_gap']['persona_name_in_view']['present_views_with_persona_name']}/174 views, in {a['identity_gap']['questions_naming_persona']['k']}/174 questions; Haiku says so in {a['identity_gap']['per_lane']['h45-D4']['abstained_identity_reason']} of its {a['identity_gap']['per_lane']['h45-D4']['abstained']} PRESENT abstentions). "
      f"The level is bounded by retrieval: the licensed record's median best rank is {a['retrieval_rank']['PRESENT']['median']} under the unmasked top-5 retriever, so {a['coverage_by_definition']['id']['k']} of 174 have it in view under any content definition (text and cosine ≥ 0.90 give the same {a['coverage_by_definition']['text']['k']}). "
      f"Of mini's 28 in-view misses: {a['labels_28']['labels']}; of Haiku's 27: {a['labels_27_h45']['labels']}. Detector ceiling: a gold entry text passes for {a['detector_ceiling_present']['any_gold_entry_text_passes']}/{a['detector_ceiling_present']['n_with_gold']} items (none for {', '.join(a['detector_ceiling_present']['no_pass_items'])}).")
    w("")
    w("**Verdict: construction for ALWAYS versus ORACLE; the gated drop is abstention, driven by the persona-binding gap and bounded by retrieval rank.**")
    w("")
    w("### (b) Stale rising with reach")
    w("")
    w("Paired decomposition on the scorable obligations reached under ALWAYS (identical view: the same call serves both policies; extended view: ORACLE appends tagged lines) and the obligations reached only under ORACLE:")
    w("")
    w("| lane | reached under ALWAYS: n | ALWAYS flags | ORACLE flags on the same items | identical views (n, flags) | extended views (transitions) | newly reached: flags / n | ORACLE rate, all | items not reached under ALWAYS whose top-5 already asserts the stale value on an active line |")
    w("|---|---|---|---|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        m = b["decomposition"][lid]["ORACLE"]["stale_use_tau_gold"]
        w(f"| {lid} | {m['always_rate']['n']} | {f_rate(m['always_rate'])} | {f_rate(m['policy_rate_on_always_set'])} | {m['identical_view']['n']}, {m['identical_view']['k']} | {m['extended_view']['trans']} | {f_rate(m['newly_reached_rate'])} | {f_rate(m['policy_rate_all'])} | {m['not_reached_under_always_but_active_stale_in_top5']} |")
    w("")
    w("The same for the gated policies against ALWAYS (stale at 0.50, scorable):")
    w("")
    w("| lane | policy | ALWAYS rate on items reached under both | policy rate on the same items | newly reached | policy rate, all |")
    w("|---|---|---|---|---|---|")
    for lid in ("mini-D4", "h45-D4"):
        for p in ("MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE"):
            m = b["decomposition"][lid][p]["stale_use_tau_gold"]
            w(f"| {lid} | {p} | {f_rate(m['always_rate'])} | {f_rate(m['policy_rate_on_always_set'])} | {f_rate(m['newly_reached_rate'])} | {f_rate(m['policy_rate_all'])} |")
    w("")
    w(f"The registered counts (9 → 17 mini, 19 → 27 Haiku) are counts over a denominator that grows from 54 to 99; as rates on the reached set they are flat with overlapping Wilson intervals (table above and Step 2). "
      f"Source of the stale answers (Step 4b): mini's flags fall only on views where an active line asserts the stale value ({s4b['crosstabs']['mini-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=True', 0)} of {s4b['crosstabs']['mini-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=True', 0) + s4b['crosstabs']['mini-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=False', 0)}), none where the stale content is only on tagged lines; "
      f"Haiku's {s4b['crosstabs']['h45-D4']['ORACLE']['stale_x_active_stale_line'].get('stale=True|active_stale_line=False', 0)} flags without such a line are the qualified mentions of Step 4. The 'tagged reach' quantity counts the item's own forbidding records; it does not see the active duplicates of the same content that sit in the top-5 for {o['oracle_any_active_stale']} of {o['n_scorable']} scorable obligations.")
    w("")
    w("**Verdict: reporting artifact.**")
    w("")
    w("### (c) Haiku above mini")
    w("")
    p = c["paired_oracle"]
    w(f"Registered ORACLE: Haiku {p['registered_oracle_all_states']['h45']['k']}/99 vs mini {p['registered_oracle_all_states']['mini']['k']}/99 at 0.50. Of these, {p['expiry_flags_in_registered_oracle']['h45']} (Haiku) and {p['expiry_flags_in_registered_oracle']['mini']} (mini) are expiry items, unscorable (Haiku names the expired arrangement while saying it is expired). "
      f"On the {p['n_oracle_pn_scorable']} scorable keys, paired: both flagged {p['stale_use_tau_gold']['TT']}, mini only {p['stale_use_tau_gold']['TF']}, Haiku only {p['stale_use_tau_gold']['FT']} (McNemar p = {p['stale_use_tau_gold']['mcnemar_p']}); by the read, 'gives the stale value': both {p['gives_stale_value_by_label']['TT']}, mini only {p['gives_stale_value_by_label']['TF']}, Haiku only {p['gives_stale_value_by_label']['FT']}. "
      f"Haiku's flags fall to {f_kn(c['first_sentence']['h45-D4']['first_sentence'])} on the first sentence and to {f_kn(c['length_controls_oracle']['stale_use_tau_gold']['haiku_trunc_to_mini_len'])} when cut to mini's length, against mini's {f_kn(c['first_sentence']['mini-D4']['first_sentence'])}; the one-directional coverage detector rewards length (Step 7), and Haiku's second sentences carry the qualifications ('marked as superseded', 'no longer current') whose tokens the detector counts as use.")
    w("")
    w("**Verdict: instrument — unscorable expiry plus qualified mentions in second sentences; on 'gives the stale value' Haiku is at or below mini.**")
    w("")
    w("### (d) Inert instruction")
    w("")
    for k, t in d["transitions"].items():
        w(f"- {k}: {t['answer_identical']}/{t['n_keys']} answers byte-identical ({t['answer_identical_casefold']} casefold; {t['answer_token_jaccard_ge_0.9']} token-Jaccard ≥ 0.9); stale at 0.50 on scorable obligations F→T {t['stale_use_tau_gold']['FT']}, T→F {t['stale_use_tau_gold']['TF']} (McNemar p {t['stale_use_tau_gold']['mcnemar_p']}); at 0.80 F→T {t['stale_use']['FT']}, T→F {t['stale_use']['TF']}; correct F→T {t['correct']['FT']}, T→F {t['correct']['TF']}; "
          f"PRESENT abstention {f_kn(t['abstention_present']['D4'])} → {f_kn(t['abstention_present']['A3'])} (with the gold line in view {f_kn(t['abstention_present_in_view']['D4'])} → {f_kn(t['abstention_present_in_view']['A3'])}); obligation abstention {f_kn(t['abstention_pn']['D4'])} → {f_kn(t['abstention_pn']['A3'])}.")
    w("")
    w(f"The instruction addresses tagged lines. The stale sources are active lines ({o['oracle_any_active_stale']}/{o['n_scorable']} scorable ORACLE views; Step 4b), which the instruction does not touch, and under the D.4 prompt mini already gave no stale value from a tagged-only view. For mini the answers are largely byte-identical; for Haiku the wording changes and the flags move both ways.")
    w("")
    w("**Verdict: redundant for mini, mis-targeted for both, since the stale sources are untagged.**")
    w("")
    # ---- disclosures
    D = V["disclosures"]
    w("## Disclosures for the paper (detector, view, retrieval)")
    w("")
    w(f"1. Expiry obligations are unscorable for stale use: the gold field is the expired fact ({D['detector_step1']['expiry_unscorable']} items); the registered column counts them.")
    w(f"2. Five retraction obligations cannot be flagged even when the store line is echoed verbatim ({', '.join(f'{i} ({s})' for i, s in D['detector_step1']['pn_member_text_never_fires'])}); a forbidding entry text fires for {D['detector_step1']['pn_any_member_text_fires'][0]} of {D['detector_step1']['pn_any_member_text_fires'][1]}.")
    w(f"3. Six successor entry texts fire the stale flag ({', '.join(sorted({i for i, _ in D['detector_step1']['successor_text_fires']}))}): echoing the current record verbatim would be counted as stale use.")
    w(f"4. Three PRESENT items cannot be marked correct even when the gold line is echoed verbatim ({', '.join(D['detector_step1']['present_gold_text_never_passes'])}); {D['detector_step1']['present_no_licensed_id']} PRESENT items have no licensed record id.")
    w(f"5. The stale flag is one-directional token coverage and rewards length (odds ratio per doubling {cm['logistic_log_chars']['OR_per_doubling']} / {ch['logistic_log_chars']['OR_per_doubling']}); a first-sentence column and a source column (active vs tagged line) should print beside it.")
    w(f"6. Active duplicates: for {D['view_step4b']['oracle_views_with_active_stale_line'][0]} of {D['view_step4b']['oracle_views_with_active_stale_line'][1]} scorable obligations the view carries an active line asserting the stale value (supersession {D['view_step4b']['by_state']['sup']}, retraction {D['view_step4b']['by_state']['ret']}); every stale answer of GPT-4.1 mini under the oracle is on such a view. This is a write-path fault of the store (the same content ingested more than once, only one copy joined to the lifecycle event), distinct from the 22 unflagged forbidding records already censused.")
    w(f"7. Negation: {D['view_step4b']['negation_mistag_example']}.")
    w(f"8. Persona binding: the view prints 'User'; the persona's name appears in {D['view_step4b']['identity']['persona_name_in_view']['present_views_with_persona_name']}/174 PRESENT views and the question names the persona in {D['view_step4b']['identity']['present_questions_naming_persona']['k']}/174; Haiku abstains on {D['view_step4b']['identity']['per_lane']['h45-D4']['abstained']}/221 PRESENT rows, {D['view_step4b']['identity']['per_lane']['h45-D4']['abstained_identity_reason']} for that reason.")
    w(f"9. Retrieval rank: the licensed record's median best rank is {D['retrieval_rank']['PRESENT']['median']} for PRESENT items and {D['retrieval_rank']['PRESENT-NEGATIVE|sup']['median']} for supersession obligations under the unmasked top-5 retriever.")
    w(f"10. Correct-by-mention: on the 65 in-view PRESENT items Haiku's detector-correct count includes {a['in_view_65']['h45-D4']['correct_and_abstained']} abstentions whose explanation restates the gold line (mini {a['in_view_65']['mini-D4']['correct_and_abstained']}); the coverage detector does not read the abstention.")
    w("")
    w("## What follows")
    w("")
    w("DS Amendment 4 (registered after this report, before any call): a view header binding 'User' to the persona's name and pinning the current date; mini and Haiku on the same 452 views; predictions on in-view correct and in-view abstention; stale reported by first sentence and by source (active vs tagged) beside the registered column; cap $8. Section 8 of paper_v17 is rewritten around the active-duplicate result (reviews/v17/REPORT.md); the active-duplicate and negation faults enter the write-path census in the downstream appendix (E.10 in paper_v17; F.10 before the R108 letter shift).")
    w("")
    a4 = OUT.parent.parent / "ds_downstream" / "run" / "scores_amend4.json"
    if a4.exists():
        T = J(a4); pm, ph = T["predictions"]["MINI"]["A4-P1"], T["predictions"]["H45"]["A4-P1"]; qm, qh = T["predictions"]["MINI"]["A4-P2"], T["predictions"]["H45"]["A4-P2"]
        cm, ch = T["columns"]["MINI"]["ORACLE"], T["columns"]["H45"]["ORACLE"]
        w("## Amendment 4 outcome (run after this report; `ds_downstream/run/scores_amend4.json`, `NUMBERS_DS.md` section 10)")
        w("")
        w(f"A4-P1 {'HOLDS' if pm['holds'] else 'FAILS'} for GPT-4.1 mini ({pm['k_d4']} → {pm['k_a4']} of {pm['n']}, Δ₁ {pm['delta']:+.4f}, item [{pm['ci_item'][0]:+.4f}, {pm['ci_item'][1]:+.4f}], persona [{pm['ci_cluster'][0]:+.4f}, {pm['ci_cluster'][1]:+.4f}]) "
          f"and {'HOLDS' if ph['holds'] else 'FAILS'} for Haiku 4.5 ({ph['k_d4']} → {ph['k_a4']}, Δ₁ {ph['delta']:+.4f}, [{ph['ci_item'][0]:+.4f}, {ph['ci_item'][1]:+.4f}], [{ph['ci_cluster'][0]:+.4f}, {ph['ci_cluster'][1]:+.4f}]). "
          f"A4-P2 {'HOLDS' if qm['holds'] else 'FAILS'} / {'HOLDS' if qh['holds'] else 'FAILS'}: in-view abstentions {qm['k_d4']} → {qm['k_a4']} and {qh['k_d4']} → {qh['k_a4']}. "
          f"Correct over the 174: mini {T['present']['MINI']['always_correct']}, Haiku {T['present']['H45']['always_correct']}. Stale under the oracle on the scorable obligations: "
          f"mini {cm['registered_scorable']['k']}/{cm['registered_scorable']['n']} (all on active-stale views; tagged-only {cm['source_tagged_only']['stale']}), Haiku {ch['registered_scorable']['k']}/{ch['registered_scorable']['n']} "
          f"(first sentence {ch['first_sentence']['k']}; tagged-only {ch['source_tagged_only']['stale']}). Spend ${T['spend']['total']:.4f}.")
        w("")
    A.wtext(REPORT, "\n".join(L) + "\n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    C = A.load_ctx()
    ok = A.gate_detector(C) & A.gate_retrieval(C) & A.gate_views(C) & A.gate_prompts(C)
    if not ok:
        print("GATES FAILED -- STOP"); sys.exit(2)
    C.step4b = J(OUT / "step4b_view_lines.json")
    V = step8(C)
    write_report(C, V)
    A.write_manifest(C)
    m = V["b_stale_rising_with_reach"]["decomposition"]
    for lid in ("mini-D4", "h45-D4"):
        x = m[lid]["ORACLE"]["stale_use_tau_gold"]
        print(f"      step 8 {lid} ORACLE: ALWAYS {x['always_rate']['k']}/{x['always_rate']['n']} -> same items {x['policy_rate_on_always_set']['k']}/{x['policy_rate_on_always_set']['n']}; newly reached {x['newly_reached_rate']['k']}/{x['newly_reached_rate']['n']}; identical {x['identical_view']}; extended {x['extended_view']['trans']}; not-reached-but-active-stale-in-top5 {x['not_reached_under_always_but_active_stale_in_top5']}")
    for k, t in V["d_inert_instruction"]["transitions"].items():
        print(f"      step 8 {k}: identical {t['answer_identical']}/{t['n_keys']}; stale_tg {t['stale_use_tau_gold']}; correct {t['correct']}")
    p = V["c_haiku_above_mini"]["paired_oracle"]
    print(f"      step 8 mini vs h45 ORACLE scorable {p['n_oracle_pn_scorable']}: flags {p['stale_use_tau_gold']}; gives {p['gives_stale_value_by_label']}; expiry flags {p['expiry_flags_in_registered_oracle']}")
    print(f"-> {REPORT}")


if __name__ == "__main__":
    main()
