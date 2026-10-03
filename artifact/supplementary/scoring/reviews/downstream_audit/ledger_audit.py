# -*- coding: utf-8 -*-
"""ledger_audit.py -- append to ds_downstream/NUMBERS_DS.md: section 9 (AUX-DS-AUDIT-*, every number read from the audit
artifacts under reviews/downstream_audit/) and section 10 (AUX-DS-A4-REG: the frozen sha256 of
registrations/ADDENDUM_DS_AMENDMENT_4.md, recorded before any call). Idempotent: the block between the AUDIT markers is
replaced on re-run; the ARTIFACT copy of the amendment is written beside. No model call.
python reviews/downstream_audit/ledger_audit.py
"""
import hashlib
import io
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "reviews" / "downstream_audit"
LEDGER = ROOT / "ds_downstream" / "NUMBERS_DS.md"
REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_4.md"
ART = ROOT / "iclr2027_monitoring_submission" / "ARTIFACT" / "registrations" / "ADDENDUM_DS_AMENDMENT_4.md"
BEGIN, END = "<!-- AUDIT-R109-BEGIN -->", "<!-- AUDIT-R109-END -->"


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def kn(r):
    return f"{r['k']} / {r['n']} = {r['rate']:.4f}"


def knw(r):
    return f"{r['k']} / {r['n']} = {r['rate']:.4f} [{r['wilson'][0]:.3f}, {r['wilson'][1]:.3f}]"


def main():
    V = J(OUT / "step8_verdicts.json"); s1 = J(OUT / "step1_synthetic.json"); s2 = J(OUT / "step2_rescore.json"); s3 = J(OUT / "step3_scored_text.json")
    s4 = J(OUT / "step4_counts.json"); s4b = J(OUT / "step4b_view_lines.json"); s5 = J(OUT / "step5_coverage.json"); rk = J(OUT / "step5_ranks.json"); s7 = J(OUT / "step7_length.json")
    gd = J(OUT / "gate_detector.json"); gr = J(OUT / "gate_retrieval.json"); gv = J(OUT / "gate_views.json"); man = J(OUT / "manifest.json")
    reg_sha = hashlib.sha256(REG.read_bytes()).hexdigest()
    a = V["a_flat_correct"]; b = V["b_stale_rising_with_reach"]; c = V["c_haiku_above_mini"]; d = V["d_inert_instruction"]
    o = s4b["oracle_summary"]; idn = s4b["identity"]; pa = s1["panel_a"]["counts"]; pb = s1["panel_b"]
    L = []
    w = L.append
    w(BEGIN)
    w("")
    w("## 9. The forensic audit of the downstream pipeline (descriptive; written 2026-09-14, R109; `reviews/DOWNSTREAM_AUDIT.md`)")
    w("")
    w("Every value in this section is read from an artifact under `reviews/downstream_audit/` written by `audit_ds.py` and `audit_step8.py` (input and output sha256s in `manifest.json`; "
      f"script sha256 `{man['script_sha256'][:16]}…`). No model call. The 15 expiry obligations are **unscorable** for every stale diagnostic (their YAML gold field is the expired fact, so the gold string equals the stale string); "
      "the registered columns above stand as registered and the diagnostic columns below run on the scorable (supersession + retraction) reached set. The step-4 classes are the auditor's read (`step4_labels.json`); the v12/v16 labeling sheets remain the human-validation instrument. "
      "**No bar, no prediction, no verdict re-adjudicated; DS-P1 to DS-P5 and Amendments 1 to 3 stand as printed.**")
    w("")
    w("### AUX-DS-AUDIT-GATES")
    w("")
    w(f"A verbatim replica of `run_ds.records` / `run_ds.score_answer` reproduces every registered per-row score: {gd['summary']['row_mismatches']} mismatches over {gd['summary']['rows_total']} rows (five lanes: D.4 mini incl. LOOKUP-LIT, D.4 Haiku, A3 mini, A3 Haiku, MODEL-ALL-V3) and "
      f"{gd['summary']['aggregate_mismatches']} of {gd['summary']['aggregate_cells']} registered per-policy cells differ. The retrieval replay (`LifecycleBank.cosine_search_all` over the pinned question and bank vectors) reproduces the ALWAYS top-5 and the L2 top-10 for {gr['n_ok']} / {gr['n_items']} items. "
      f"Every one of the {gv['n_lines']} view lines parses and equals the TRUE-join entry text ({gv['render_lock_failures']} failures); the ORACLE view equals the ALWAYS view for {gv['present_view_identity']['oracle_sha_equals_always']} / {gv['present_view_identity']['n_present']} PRESENT items (by construction; ORACLE fetches nothing on a PRESENT item). Prompt digests as `AUX-DS-PROMPT` and `AUX-DS-A3-PROMPT`.")
    w("")
    w("### AUX-DS-AUDIT-DETECTOR — validity by construction (`step1_synthetic.json`)")
    w("")
    w(f"On the YAML reference strings: gold → correct {pa['present.gold->correct']} / {pa['present.n']}; abstention string → correct {pa['present.abst->correct']}; stale string → stale use {pa['pn.stale->stale_tg']} / {pa['pn.n_scorable']} at TAU_GOLD and {pa['pn.stale->stale_hi']} at TAU_HI; "
      f"gold string → stale {pa['pn.gold->stale_tg']}; abstention → any flag {pa['pn.abst->any_flag']}; unscorable expiry {pa['pn.unscorable_expiry']}. "
      f"On the rendered store texts: a gold entry text passes `correct` for {pb['present']['any_pass']} / {pb['present']['n_with_gold']} PRESENT items with a licensed id (none for {', '.join(x['item_id'] for x in pb['present']['no_pass'])}); {len(pb['present']['no_licensed_id'])} PRESENT items have no licensed id. "
      f"A forbidding entry text fires stale use for {pb['pn']['any_tg']} / {pb['pn']['n_scorable']} scorable obligations at TAU_GOLD ({pb['pn']['any_hi']} at TAU_HI); none fires for {', '.join(x['item_id'] for x in pb['pn']['none_tg'])}. "
      f"{len(pb['pn']['successor_text_fires'])} of {pb['pn']['n_successor_texts']} successor entry texts fire stale use ({', '.join(sorted({x['item_id'] for x in pb['pn']['successor_text_fires']}))}). "
      f"On the 65 in-view licensed items Haiku 4.5's detector-correct count includes {a['in_view_65']['h45-D4']['correct_and_abstained']} abstentions whose explanation restates the gold line (GPT-4.1 mini {a['in_view_65']['mini-D4']['correct_and_abstained']}).")
    w("")
    w("### AUX-DS-AUDIT-RATES — stale use at TAU_GOLD as a rate on the reached set, registered (all states) beside scorable (expiry removed), Wilson 95% (`step2_rescore.json`)")
    w("")
    w("| answerer, prompt | policy | registered | scorable |")
    w("|---|---|---|---|")
    names = {"mini-D4": "GPT-4.1 mini, D.4", "h45-D4": "Haiku 4.5, D.4", "mini-A3": "GPT-4.1 mini + instruction", "h45-A3": "Haiku 4.5 + instruction"}
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE"):
            bb = s2["tables"][lid][p]["all"]["stale_use_tau_gold"]
            w(f"| {names[lid]} | {p} | {bb['registered']['k']} / {bb['registered']['n']} | {knw(bb['scorable'])} |")
    w("")
    w("### AUX-DS-AUDIT-PAIRED — the ALWAYS → ORACLE decomposition on the scorable obligations (`step8_verdicts.json`)")
    w("")
    w("| answerer, prompt | reached under ALWAYS | stale under ALWAYS | stale under ORACLE on the same items | identical views (n; stale) | extended views: F→F / T→T / F→T / T→F | newly reached under ORACLE | ORACLE, all scorable | not reached under ALWAYS but an active line of the top-5 asserts the stale value |")
    w("|---|---:|---|---|---|---|---|---|---:|")
    for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3"):
        m = b["decomposition"][lid]["ORACLE"]["stale_use_tau_gold"]; t = m["extended_view"]["trans"]
        w(f"| {names[lid]} | {m['always_rate']['n']} | {knw(m['always_rate'])} | {knw(m['policy_rate_on_always_set'])} | {m['identical_view']['n']}; {m['identical_view']['k']} | {t.get('False->False', 0)} / {t.get('True->True', 0)} / {t.get('False->True', 0)} / {t.get('True->False', 0)} | {knw(m['newly_reached_rate'])} | {knw(m['policy_rate_all'])} | {m['not_reached_under_always_but_active_stale_in_top5']} |")
    w("")
    w("### AUX-DS-AUDIT-SOURCE — what the view itself asserts (`step4b_view_lines.json`)")
    w("")
    w(f"Of the {o['n_scorable']} scorable obligations, the ORACLE view holds an **active** line whose text asserts the stale value (the item's own detector at TAU_GOLD on the line) for **{o['oracle_any_active_stale']}** (supersession {o['by_state_oracle_active_stale']['sup']}, retraction {o['by_state_oracle_active_stale']['ret']}); the same {o['always_any_active_stale']} under ALWAYS, since every fetched line is tagged; "
      f"no tagged line asserts the successor ({o['oracle_any_tagged_successor']}). Stale use at TAU_GOLD × an active stale line in the view, ORACLE (stale with such a line / stale without / not stale with / not stale without): "
      + "; ".join(f"{names[lid]} {x.get('stale=True|active_stale_line=True', 0)} / {x.get('stale=True|active_stale_line=False', 0)} / {x.get('stale=False|active_stale_line=True', 0)} / {x.get('stale=False|active_stale_line=False', 0)}" for lid, x in ((lid, s4b['crosstabs'][lid]['ORACLE']['stale_x_active_stale_line']) for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3")))
      + "; ALWAYS: " + "; ".join(f"{names[lid]} {x.get('stale=True|active_stale_line=True', 0)} / {x.get('stale=True|active_stale_line=False', 0)} / {x.get('stale=False|active_stale_line=True', 0)} / {x.get('stale=False|active_stale_line=False', 0)}" for lid, x in ((lid, s4b['crosstabs'][lid]['ALWAYS']['stale_x_active_stale_line']) for lid in ("mini-D4", "h45-D4"))) + ". "
      "Negation mis-tag (one item, both variants): `frbank:fatima:fatima_q06` — the retraction statement (\"decided not to launch a home fragrance line called Oud and Geometry ...\") carries the `retracted` tag because it covers 4 of the 5 original-plan tokens at TAU_HI and the join has no negation handling, while the plan records stay active (\"launching\" is not \"launch\").")
    w("")
    w("### AUX-DS-AUDIT-READ — the flagged answers classified (`step4_labels.json`, `step4_counts.json`; the auditor's read)")
    w("")
    w("| answerer, D.4 | flagged under ORACLE | unscorable expiry | gives the stale value | mentions it, states superseded / retracted / cancelled | partial-overlap artifact | other |")
    w("|---|---:|---:|---:|---:|---:|---:|")
    for lid in ("mini-D4", "h45-D4"):
        x = s4["stale"][lid]; lb = x["labels"]
        w(f"| {names[lid]} | {x['n_flagged']} | {x['n_unscorable_expiry']} | {lb.get('gives_stale_value', 0)} | {lb.get('mentions_but_superseded', 0)} | {lb.get('partial_overlap_artifact', 0)} | {lb.get('other', 0)} |")
    w("")
    w("| answerer, D.4 | in-view licensed items marked incorrect | abstained | correct value in a different format | wrong value | other |")
    w("|---|---:|---:|---:|---:|---:|")
    for lid in ("mini-D4", "h45-D4"):
        x = s4["present"][lid]; lb = x["labels"]
        w(f"| {names[lid]} | {x['n']} | {lb.get('abstained', 0)} | {lb.get('correct_different_format', 0)} | {lb.get('wrong_value', 0)} | {lb.get('other', 0)} |")
    w("")
    p = c["paired_oracle"]
    w(f"Paired on the {p['n_oracle_pn_scorable']} scorable ORACLE keys: both flagged {p['stale_use_tau_gold']['TT']}, GPT-4.1 mini only {p['stale_use_tau_gold']['TF']}, Haiku 4.5 only {p['stale_use_tau_gold']['FT']} (exact McNemar p = {p['stale_use_tau_gold']['mcnemar_p']}); by the read, 'gives the stale value': both {p['gives_stale_value_by_label']['TT']}, mini only {p['gives_stale_value_by_label']['TF']}, Haiku only {p['gives_stale_value_by_label']['FT']}. "
      f"Of the registered ORACLE flags, {p['expiry_flags_in_registered_oracle']['h45']} (Haiku) and {p['expiry_flags_in_registered_oracle']['mini']} (mini) are expiry items.")
    w("")
    w("### AUX-DS-AUDIT-LENGTH — answer length and the stale flag (`step7_length.json`, `step3_scored_text.json`)")
    w("")
    pl = s7["paired_lanes"]["h45-D4/mini-D4"]; cm = s7["correlation"]["mini-D4"]["PRESENT-NEGATIVE|stale_use_tau_gold"]; ch = s7["correlation"]["h45-D4"]["PRESENT-NEGATIVE|stale_use_tau_gold"]; po = s7["pooled_logistic"]["stale_use_tau_gold"]
    lc = s7["length_controls"]["h45-D4"]["ORACLE"]
    w(f"Median answer length on the same {pl['n']} views: Haiku 4.5 {pl['median_chars']['h45-D4']:.0f} characters, GPT-4.1 mini {pl['median_chars']['mini-D4']:.1f}; sentences per answer mini {s3['n_sentences']['mini-D4']}, Haiku {s3['n_sentences']['h45-D4']}. "
      f"Point-biserial r of stale use at TAU_GOLD with log length on the scorable obligation rows: mini {cm['pointbiserial_log_chars']['r']:.4f} (p = {cm['pointbiserial_log_chars']['p']:.4f}), Haiku {ch['pointbiserial_log_chars']['r']:.4f} (p = {ch['pointbiserial_log_chars']['p']:.4f}); odds ratio per doubling of length {cm['logistic_log_chars']['OR_per_doubling']:.4f} / {ch['logistic_log_chars']['OR_per_doubling']:.4f}. "
      f"Pooled logistic on {po['n']} rows, logit P(stale) = b0 + b1 log(chars) + b2 is_haiku: b1 = {po['fit']['coef'][1]:.4f} (z {po['fit']['z'][1]:.2f}), b2 = {po['fit']['coef'][2]:.4f} (z {po['fit']['z'][2]:.2f}). "
      f"ORACLE, scorable, stale at TAU_GOLD / TAU_HI: mini registered {kn(lc['stale_use_tau_gold']['registered_mini'])} / {kn(lc['stale_use']['registered_mini'])}; Haiku registered {kn(lc['stale_use_tau_gold']['registered_haiku'])} / {kn(lc['stale_use']['registered_haiku'])}; "
      f"Haiku first sentence {kn(lc['stale_use_tau_gold']['haiku_first_sentence'])} / {kn(lc['stale_use']['haiku_first_sentence'])}; Haiku cut to mini's length {kn(lc['stale_use_tau_gold']['haiku_trunc_to_mini_len'])} / {kn(lc['stale_use']['haiku_trunc_to_mini_len'])}. "
      f"First-sentence stale at TAU_GOLD under ORACLE, every lane: " + "; ".join(f"{names[lid]} {kn(s3['rescore'][lid]['ORACLE']['pn']['stale_use_tau_gold']['first_sentence'])}" for lid in ("mini-D4", "h45-D4", "mini-A3", "h45-A3")) + ".")
    w("")
    w("### AUX-DS-AUDIT-IDENTITY — the persona binding and the in-view abstentions (`step4b_view_lines.json`, `step8_verdicts.json`)")
    w("")
    w(f"The persona's name appears in {idn['persona_name_in_view']['present_views_with_persona_name']} / {idn['persona_name_in_view']['present_views']} PRESENT views and {idn['persona_name_in_view']['pn_views_with_persona_name']} / {idn['persona_name_in_view']['pn_views']} obligation views; {idn['present_questions_naming_persona']['k']} / {idn['present_questions_naming_persona']['n']} PRESENT questions name the persona. "
      f"PRESENT abstentions (rows): Haiku 4.5, D.4 {idn['per_lane']['h45-D4']['abstained']} / {idn['per_lane']['h45-D4']['present_rows']}, {idn['per_lane']['h45-D4']['abstained_identity_reason']} giving the identity reason in the answer text; GPT-4.1 mini, D.4 {idn['per_lane']['mini-D4']['abstained']} / {idn['per_lane']['mini-D4']['present_rows']} (the bare phrase). "
      "On the 65 licensed items whose gold record is in the retrieval view (ALWAYS = ORACLE view): " + "; ".join(f"{names[lid]} detector-correct {v['correct']} (of which {v['correct_and_abstained']} abstentions), abstained {v['abstained']}, answered wrongly {v['answered_incorrect']}, correct among the answered {v['correct_among_answered']['k']} / {v['correct_among_answered']['n']}" for lid, v in a["in_view_65"].items()) + ". "
      "Of GPT-4.1 mini's 15 in-view abstentions, 13 fall on a key where Haiku 4.5 states the identity reason; Haiku states it on 34 of its 38 (computed in the registration of Amendment 4).")
    w("")
    w("### AUX-DS-AUDIT-RANK — the licensed record under the unmasked top-5 retriever (`step5_ranks.json`, `step5_coverage.json`)")
    w("")
    w("| population | n | median best rank | q25 | q75 | share ≤ 5 | share ≤ 10 | share > 10 |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|")
    for k in ("PRESENT", "PRESENT-NEGATIVE", "PRESENT-NEGATIVE|sup", "PRESENT-NEGATIVE|ret", "PRESENT-NEGATIVE|exp"):
        x = rk["best_rank_per_item"][k]
        w(f"| {k} | {x['n']} | {x['median']} | {x['q25']} | {x['q75']} | {x['share_le5']:.4f} | {x['share_le10']:.4f} | {x['share_gt10']:.4f} |")
    w("")
    cv = s5["coverage"]["present"]["ALWAYS"]; pr = s5["coverage"]["pn_reach"]
    w(f"Licensed record in view by entry id / normalized text / MiniLM cosine ≥ 0.90: PRESENT {cv['id']['k']} / {cv['text']['k']} / {cv['emb_0.90']['k']} of 174 (cosine ≥ 0.80: {cv['emb_0.80']['k']}); obligations under ALWAYS {pr['ALWAYS']['id']['k']} / {pr['ALWAYS']['text']['k']} / {pr['ALWAYS']['emb_0.90']['k']} of 104, under ORACLE {pr['ORACLE']['id']['k']} / {pr['ORACLE']['text']['k']} / {pr['ORACLE']['emb_0.90']['k']}. "
      f"In-view correct under retrieval alone is the same under the three definitions ({s5['in_view_correct']['mini-D4']['ALWAYS']['id']['in_view']['k']} / 65 mini, {s5['in_view_correct']['h45-D4']['ALWAYS']['id']['in_view']['k']} / 65 Haiku). {rk['licensed_records_not_in_store_variant']['n_records']} licensed records are absent from their item's store variant; no item loses all of them.")
    w("")
    w("### AUX-DS-AUDIT-A3 — the D.4 → Amendment 3 transitions on the 452 views (`step8_verdicts.json`)")
    w("")
    for k, t in d["transitions"].items():
        w(f"- {names[k.split('->')[0]]} → + instruction: {t['answer_identical']} / {t['n_keys']} answers byte-identical; stale use at TAU_GOLD on the scorable obligations F→T {t['stale_use_tau_gold']['FT']}, T→F {t['stale_use_tau_gold']['TF']} (exact McNemar p = {t['stale_use_tau_gold']['mcnemar_p']}); at TAU_HI F→T {t['stale_use']['FT']}, T→F {t['stale_use']['TF']}; correct F→T {t['correct']['FT']}, T→F {t['correct']['TF']}; "
          f"PRESENT abstention {t['abstention_present']['D4']['k']} / {t['abstention_present']['D4']['n']} → {t['abstention_present']['A3']['k']} / {t['abstention_present']['A3']['n']}.")
    w("")
    w("### AUX-DS-AUDIT-PRINTED — the forms the paper prints (R109, Section 8 and Appendix E.10, the downstream appendix; F.10 before the R108 letter shift), each the two-decimal rounding of, or equal to, a value above")
    w("")
    w(f"Stale rate on the scorable reached set, GPT-4.1 mini: retrieval alone 0.19 (0.1905), oracle 0.19 (0.1882); Haiku 4.5: 0.26 (0.2619), 0.22 (0.2235). Odds ratio per doubling of answer length: 2.34 (2.3414), 2.99 (2.9928). "
      f"Counts: 89 scorable obligations; 35 views with an active stale line (21 supersession, 14 retraction); 16 of 16 (mini, oracle) and 14 of 19 (Haiku, oracle); 42 obligations reached under both, 8 -> 9 (mini) and 11 -> 11 (Haiku); 43 newly reached, 7 and 8; "
      f"first sentence 8 of 85 against 19 (Haiku) and 16 (mini), cut to mini's length 7; by the read 11 of 16 (mini) and 8 of 19 (Haiku); 310 of 452 answers byte-identical under the instruction; 65 in-view licensed items, mini 37 correct and 15 abstentions, Haiku 38 abstentions of which 12 counted correct; "
      f"28 in-view misses; persona name in 47 of 174 views, 172 of 174 questions name the persona; Haiku 94 of 145 abstentions with the identity reason; median best rank 8.5; 15 expiry obligations unscorable; five retraction obligations unflaggable, 6 successor texts flagged, 3 licensed items unmarkable; Amendment 4: +0.10, 15 -> 7, 38 -> 19, cap $8.00.")
    w("")
    w("### AUX-DS-AUDIT-VERDICTS — the author's rulings of 2026-09-14 (evening), as recorded in `reviews/DOWNSTREAM_AUDIT.md`")
    w("")
    w("(a) flat correct: construction for ALWAYS versus ORACLE; the gated drop is abstention, driven by the persona-binding gap and bounded by retrieval rank. "
      "(b) stale rising with reach: a reporting artifact — rates flat with Wilson intervals; stale answers arise only from active lines asserting the stale value (none from tagged lines for GPT-4.1 mini; five qualified mentions for Haiku 4.5). "
      "(c) Haiku above mini: instrument — unscorable expiry plus qualified mentions in second sentences; on 'gives the stale value' Haiku is at or below mini. "
      "(d) inert instruction: redundant for mini, mis-targeted for both, since the stale sources are untagged.")
    w("")
    w("## 10. Amendment 4 — a view header binding \"User\" to the persona and pinning the current date (two predictions; registered 2026-09-14, R109; NOT YET RUN)")
    w("")
    w("### AUX-DS-A4-REG")
    w("")
    w(f"Registration `registrations/ADDENDUM_DS_AMENDMENT_4.md`, frozen sha256 `{reg_sha}`, recorded here on 2026-09-14 **before any call** (copy in `iclr2027_monitoring_submission/ARTIFACT/registrations/`). "
      "Predictions A4-P1 (in-view correct on the 65 rises by at least +0.10 with both bootstrap intervals excluding zero, each answerer) and A4-P2 (in-view abstentions fall by more than half: GPT-4.1 mini 15 → 7 or fewer, Haiku 4.5 38 → 19 or fewer), failure texts written in §A4.4; "
      "stale use reported by first sentence and by active-versus-tagged source beside the registered column (descriptive); the 452 views, both answerers, cap $8.00 (projection ≈ $0.71 with the ×1.3 rule). "
      "The runner (`ds_downstream/tools/amend4_header.py`) is not yet written and no call has been made; the keys `AUX-DS-A4-LOCK`, `-PROMPT`, `-POP`, `-PROBE-MINI`, `-PROBE-H45`, `-PROJECTION`, `-P1`, `-P2`, `-STAGE2-MINI`, `-STAGE2-H45`, `-FIRSTSENT`, `-SOURCE`, `-PRESENT`, `-EXPIRY`, `-SPEND` are appended by it after the author's word.")
    w("")
    w(END)
    block = "\n".join(L) + "\n"
    txt = io.open(LEDGER, encoding="utf-8").read()
    if BEGIN in txt:
        i, j = txt.index(BEGIN), txt.index(END) + len(END) + 1
        txt = txt[:i] + block + txt[j:]
    else:
        txt = txt.rstrip("\n") + "\n\n" + block
    io.open(LEDGER, "w", encoding="utf-8", newline="\n").write(txt)
    ART.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(REG, ART)
    print("registration sha256", reg_sha); print("ARTIFACT copy equal:", hashlib.sha256(ART.read_bytes()).hexdigest() == reg_sha)
    print(f"-> {LEDGER} (sections 9 and 10 written between the AUDIT-R109 markers, {len(L)} lines)")


if __name__ == "__main__":
    main()
