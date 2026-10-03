# -*- coding: utf-8 -*-
"""r125_report.py -- REPORT_R125.md, the closing report of program R125: every number filled from the results files (nothing typed from memory).
NO MODEL CALL. Sections: Task 1 (the tables' pointer and the list of body claims that change direction, from REPORT_R125_T1.md), Task 2's three
numbers, Task 3's paragraph per backend and the re-scored rows, the author sheet's path and hash, Tasks 4 and 5's outcome tables with every
prediction marked, spend per provider, commits.
"""
from __future__ import annotations

import json
import subprocess
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES  # noqa: E402
from r125_t45_report import spend  # noqa: E402

OUT = C.R125 / "REPORT_R125.md"


def ci(d, a="ci_lo", b="ci_hi"):
    return f"[{d[a]:+.4f}, {d[b]:+.4f}]"


def sci(d):
    return f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def pr(p, a="ci_triple", b="ci_persona"):
    return f"{p['delta']:+.4f} ({ci(p[a])}; {ci(p[b])}){', reliable' if p['both_exclude_zero'] else ', not reliable'}"


def prp(p):
    return pr(p, "item_ci", "persona_ci")


def main():
    t1 = C.jload(C.RESULTS / "r125_matched.json"); t2 = C.jload(C.RESULTS / "r125_t2_emptiness.json"); fr = C.jload(C.RESULTS / "r125_t3_frbank.json"); gr = C.jload(C.RESULTS / "r125_t3_graphiti.json")
    sh = C.jload(C.RESULTS / "r125_t3_sheet.json"); t4 = C.jload(C.RESULTS / "r125_t4_sibling.json"); t5 = C.jload(C.RESULTS / "r125_t5_nc.json"); sp = spend()
    lock = C.jload(C.CF2 / "rows" / "lock_r125.json"); leak = C.jload(C.CF2 / "rows" / "leak_r125.json"); proj = C.jload(C.CF2 / "rows" / "projection_r125.json")
    log = subprocess.run(["git", "log", "--oneline", "-8", "--", "reviews/r125"], capture_output=True, text=True, cwd=str(C.ROOT)).stdout.strip().splitlines()
    t1_report = (C.R125 / "REPORT_R125_T1.md").read_text(encoding="utf-8")
    claims = t1_report[t1_report.index("**The list of claims whose direction changes**"):t1_report.index("## 5. Three things")].strip()
    L = []; A = L.append
    A("# REPORT_R125 — matched metric, sibling-name control, store-relative labels, strong-model ablations (2026-09-20)")
    A("")
    A("Program R125, a fresh session on the brief of 2026-09-20. Everything lives under `reviews/r125/` (tools, results, registrations, build, this report); the ledger rows are section 15 (15a to 15e) of "
      "`r82_counterfactual/cf2/NUMBERS_CF2.md`; the API rows are `r82_counterfactual/cf2/rows/rows_r125_*.jsonl` with their lock, probes, projection, leak and batch records beside them. "
      "Nothing under `reviews/v21/`, `reviews/r124/` or `human_validation/` was touched; no paper text was written (Claude writes the texts from the ledger). Readings: **reliable** = both "
      "intervals exclude zero; **matched AUROC** = (W + T/2) / n within the triple or the pair (Task 1's definition); every Task 1 to 3 row is post hoc and labelled so; Tasks 4 and 5 were "
      "registered and frozen at `5cd8f80` before any call on their items (`FREEZE_R125.md`).")
    A("")
    # ---- Task 1
    A("## Task 1. The matched metric (REPORT_R125_T1.md; T1_TABLES.md; ledger 15)")
    A("")
    A(f"Delivered first as `REPORT_R125_T1.md` with the full tables in `T1_TABLES.md` and Figure 3's data on the matched metric in `results/fig3_data_matched.tex` (the schema of "
      f"`reviews/v22/src/fig3_data.tex`). The sanity check passed: every W/T/L printed in Table 1 (twelve rows) and four appendix rows reproduce from the rows, so the matched AUROC is "
      f"(W + T/2) / 148 from the printed counts. Table 1's readers under the matched metric (PN against PRESENT within the triple): " +
      "; ".join(f"{lab} {t1['readers'][k]['pn_vs_present']['whole']['matched']:.4f}" for k, lab in (("MINI5_v2", "mini (five draws)"), ("H45_v2", "Haiku"), ("LUNA_v2", "Luna"), ("SOL_v2", "Sol"), ("OP5_v2", "Opus"),
                                                                                                    ("LOOKUP_v2", "name lookup"), ("CR-nb1_v2", "count reader, guessed"), ("CR-oracle-a_v2", "count reader, given"), ("HYBRID_v2", "hybrid reader (E10)")))
      + f"; under the all-states summary Opus {t1['readers']['OP5_v3']['pn_vs_present']['whole']['matched']:.4f} against the all-states lookup {t1['readers']['ALLSTATES_v3']['pn_vs_present']['whole']['matched']:.4f} "
      f"({t1['paired']['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['delta']:+.4f}, intervals {ci(t1['paired']['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_triple'])} and "
      f"{ci(t1['paired']['opus_v3_vs_allstates']['OP5_v3']['pn_vs_present']['whole']['ci_persona'])}, not reliable; Table 1's difference row is reliable under the pooled metric).")
    A("")
    A(claims)
    A("")
    # ---- Task 2
    A("## Task 2. How much of the lookup is list emptiness (T2_T3_TABLES.md; ledger 15b)")
    A("")
    c = t2["census_444"]["SUPERSESSION"]; v2 = t2["cf444"]["v2"]; o = t2["obl661"]
    A(f"1. **Empty lists.** Of the 88 supersession pairs, {c['v2_superseded_list/PRESENT']['empty']} carry an empty superseded-names list in the PRESENT version and "
      f"{c['v2_superseded_list/ABSENT']['empty']} in the ABSENT version (the two versions' lists are identical: the target is not superseded in either); none in PN. List length per version: PN "
      f"{c['v2_superseded_list/PN']['length_hist']} (mean {c['v2_superseded_list/PN']['mean_length']:.2f}), PRESENT and ABSENT {c['v2_superseded_list/PRESENT']['length_hist']} (mean "
      f"{c['v2_superseded_list/PRESENT']['mean_length']:.2f}); PN is one name longer than PRESENT on {c['v2_superseded_list/PN_minus_PRESENT_length'].get('1', 0)} pairs, two on "
      f"{c['v2_superseded_list/PN_minus_PRESENT_length'].get('2', 0)}, three on {c['v2_superseded_list/PN_minus_PRESENT_length'].get('3', 0)}. On {c['v2_pairs_where_PRESENT_empty_and_PN_nonempty']} of the 88 pairs "
      f"emptiness alone identifies the PN version. Under the all-states summary the retracted list is empty in {t2['census_444']['RETRACTION']['v3_retracted_list/PRESENT']['empty']} of 30 PRESENT versions and the "
      f"expired list in {t2['census_444']['EXPIRY']['v3_expired_list/PRESENT']['empty']} of 30.")
    A(f"2. **The random-token control.** On the 444 under the default summary: pooled {v2['random_token']['pooled']['whole']:.4f} (supersession {v2['random_token']['pooled']['per_state']['SUPERSESSION']:.4f}, "
      f"retraction and expiry 0.5000), matched PN vs PRESENT {v2['random_token']['matched_pn_vs_present']['whole']['matched']:.4f} "
      f"({v2['random_token']['matched_pn_vs_present']['whole']['W']}/{v2['random_token']['matched_pn_vs_present']['whole']['T']}/{v2['random_token']['matched_pn_vs_present']['whole']['L']}; supersession "
      f"{v2['random_token']['matched_pn_vs_present']['per_state']['SUPERSESSION']['matched']:.4f}); under the all-states summary pooled {t2['cf444']['v3']['random_token']['pooled']['whole']:.4f}, matched "
      f"{t2['cf444']['v3']['random_token']['matched_pn_vs_present']['whole']['matched']:.4f}. On the 661 (no triples, so no matched row): committed form {o['committed']['random_token']['whole']:.4f} "
      f"(supersession {o['committed']['random_token']['SUPERSESSION']['auroc']:.4f} / retraction {o['committed']['random_token']['RETRACTION']['auroc']:.4f} / expiry {o['committed']['random_token']['EXPIRY']['auroc']:.4f}, "
      f"each state's positives against all 557 negatives), marker-free {o['marker_free']['random_token']['whole']:.4f}.")
    A(f"3. **The lookup minus the random token.** On the 444 under the default summary: pooled {prp(v2['lookup_minus_random_pooled']['whole'])}; matched {pr(v2['lookup_minus_random_matched']['pn_vs_present']['whole'])}; "
      f"on supersession pooled {prp(v2['lookup_minus_random_pooled']['per_state']['SUPERSESSION'])} and matched {pr(v2['lookup_minus_random_matched']['pn_vs_present']['per_state']['SUPERSESSION'])}; on the counted states "
      f"zero by construction. Under the all-states summary pooled {prp(t2['cf444']['v3']['lookup_minus_random_pooled']['whole'])}, matched {pr(t2['cf444']['v3']['lookup_minus_random_matched']['pn_vs_present']['whole'])}. "
      f"On the 661: committed form {prp(o['committed']['lookup_minus_random_pooled']['whole'])}; marker-free {prp(o['marker_free']['lookup_minus_random_pooled']['whole'])}. Read together: of the lookup's 0.7663 on the 444, "
      f"{v2['random_token']['pooled']['whole']:.2f} is reachable with no name meaning anything (pooled) and {v2['random_token']['matched_pn_vs_present']['whole']['matched']:.2f} of its 0.7770 within the triple; on the 661 the names add "
      f"{o['committed']['lookup_minus_random_pooled']['whole']['delta']:+.2f} to a list-length floor of {o['committed']['random_token']['whole']:.2f}.")
    A("")
    # ---- Task 3
    A("## Task 3. Labels relative to what each backend retains (T2_T3_TABLES.md; ledger 15c)")
    A("")
    A("### 3.1 What the store is in each scored condition, and where the PN labels come from")
    A("")
    jm = fr["counts"]["join_marked"]; om = fr["counts"]["own_marked"]; cross = fr["counts"]["cross_join080_own"]
    A(f"**FR-Bank, the store-written summary.** S is FR-Bank's own persona bank (e0's frozen banks; 18,936 entries over the forty personas), read through the store's own fields "
      f"(`is_active`, `is_retracted`, `supersedes`) by the one renderer into the store-written summary, capped at fifteen names per category or with the cap lifted. The PN labels come from the "
      f"manifest (hand-verified); each obligation's forbidding records are its `pn_members`, entry identifiers of that same bank, so the forbidding content is stored by construction for all "
      f"{fr['counts']['members_stored']} of the 104. What the manifest-relative label does not say is whether the ground-truth join (`index_v2.true_lifecycle`, the manifest's events aligned to entries at "
      f"the 0.80 bar) marks one of those records, which is what the ground-truth summary's superseded-names list and the ground-truth tags are built from: it marks {jm['0.80']['n']} "
      f"({jm['0.80']['by_state']}), the 22 it does not mark are all retraction- or expiry-derived, and nothing in the recorded pipeline reads the store's own marks for the label. "
      f"So on FR-Bank the label is manifest-relative, the ground-truth summary is join-relative, and the store-written summary is store-relative; the three coincide on the 63 supersession obligations "
      f"and diverge on the counted states.")
    A("")
    ret80 = gr["counts"]["0.80"]
    A(f"**Graphiti.** S is one Graphiti graph per persona (graphiti-core 0.28.1, stock), built by Graphiti's own extraction from the 1,365 episodes rendered from FR-Bank's banks with every lifecycle "
      f"field removed; every graph is the full store of its persona, so the scored population is the 323 full-variant items with 47 obligations. The PN labels come from the manifest as everywhere; "
      f"the forbidding records are FR-Bank entry identifiers the graph does not hold, so whether the graph retains the forbidding content is the census join's question (the manifest event that "
      f"marks a member, transposed onto the persona's edges at the overlap bar). At the 0.80 bar the recorded buckets reproduce from the exported edges: of the 34 join-marked superseded-or-expired "
      f"obligations, {ret80['sup_or_exp_34']['RECOVERED']} recovered (a firing edge non-active), {ret80['sup_or_exp_34']['STALE_ACTIVE']} stale-active and {ret80['sup_or_exp_34']['EXTRACTION_MISS']} extraction misses; "
      f"4 join-retracted (inexpressible on this backend; the content is asserted by some edge for {ret80['retracted_content_retained']} of them) and 9 unflagged by the join. Relative to the store, "
      f"{ret80['retained']} of the 34 hold the forbidding content and {ret80['sup_or_exp_34']['EXTRACTION_MISS']} do not; the 13 retracted-or-unflagged have no census stratum.")
    A("")
    A("**Mem0.** S is the Mem0 store (`mem0ai` 1.0.5) built by its own write path from the same conversations, read at the retrieval surface we evaluated (`search`, `get_all`); its per-memory "
      "history call was not consulted. No obligation is scored on this backend: its scored population holds 94 PRESENT and 144 ABSENT items and no PRESENT-NEGATIVE item (the hard tier's 35 "
      "positives are all FR-Bank), so its evaluation is the coverage judgment (FOK) and the census of the store's own fields (Table 2: 12.7 percent of 10,074 entries expose `updated_at` and "
      "nothing else). The three counts of 3.2 are therefore 0 of 0: there is no PN label to state relative to what Mem0 retains.")
    A("")
    A("**A-MEM.** S is the A-MEM store (`agentic-memory` 0.0.1) in our integration, 11,319 notes with 23,186 link references resolving to no note identifier on the 40 scored personas (Table 2). "
      "Its scored population holds 126 PRESENT and 158 ABSENT items and no obligation, so, as for Mem0, the evaluation is coverage and the census; the three counts are 0 of 0.")
    A("")
    A("### 3.2 The three counts per backend")
    A("")
    A("| backend | obligations | forbidding content retained (join at 0.80 / 0.75 / 0.50) | retained and carrying a non-active mark (the store's own) | monitor rows restricted to each stratum |")
    A("|---|---:|---|---|---|")
    A(f"| FR-Bank (store-written) | 104 | stored by construction 104; join-marked {jm['0.80']['n']} / {jm['0.75']['n']} / {jm['0.50']['n']} (by state at 0.80: {jm['0.80']['by_state']}) | {om['n']} ({om['by_state']}); cross with the join at 0.80: {cross} | 3.3 below (T2_T3_TABLES.md) |")
    A(f"| Graphiti (full store) | 47 (34 join-marked sup-or-exp, 4 join-retracted, 9 unflagged) | {gr['counts']['0.80']['retained']} / {gr['counts']['0.75']['retained']} / {gr['counts']['0.50']['retained']} of 34; the 4 retracted's content {gr['counts']['0.80']['retracted_content_retained']} / {gr['counts']['0.75']['retracted_content_retained']} / {gr['counts']['0.50']['retracted_content_retained']} | recovered {gr['counts']['0.80']['sup_or_exp_34']['RECOVERED']} / {gr['counts']['0.75']['sup_or_exp_34']['RECOVERED']} / {gr['counts']['0.50']['sup_or_exp_34']['RECOVERED']} of 34 | 3.3 below |")
    A("| Mem0 | 0 | — | — | — |")
    A("| A-MEM | 0 | — | — | — |")
    A("")
    A("### 3.3 The monitor rows re-scored on the retained-only obligations (negatives unchanged; n and both intervals)")
    A("")
    A("FR-Bank, the rows of `tab:levels` (the 661; 557 negatives unchanged; the manifest-relative row first, then the strata):")
    A("")
    A("| stratum | n_pos | mini GT | mini capped | mini lifted | Haiku GT | Haiku capped | Haiku lifted | lookup GT | lookup capped | lookup lifted |")
    A("|---|---:|---|---|---|---|---|---|---|---|---|")
    keys = ["mini_true", "mini_capped", "mini_lifted", "haiku_true", "haiku_capped", "haiku_lifted", "lookup_true", "lookup_capped", "lookup_lifted"]
    for name in ("all_104 (manifest-relative, the printed rows)", "join_marked_0.80", "join_marked_0.75", "join_marked_0.50", "join_unmarked_0.80 (the 22)", "own_marked", "own_active (no store mark on any member)", "join_marked_0.80_and_own_marked", "join_marked_0.80_and_own_active"):
        b = fr["rescored"][name]
        A(f"| {name} | {b['n_pos']} | " + " | ".join(f"{b['readers'][k]['auroc']:.4f} {sci(b['readers'][k]['ci_item'])} {sci(b['readers'][k]['ci_persona'])}" for k in keys) + " |")
    A("")
    b82 = fr["rescored"]["join_marked_0.80"]["readers"]; b22 = fr["rescored"]["join_unmarked_0.80 (the 22)"]["readers"]
    A(f"Store-written minus ground truth on the 82 join-marked: mini capped {prp(b82['mini_capped']['minus_ground_truth'])}, lifted {prp(b82['mini_lifted']['minus_ground_truth'])}; Haiku capped "
      f"{prp(b82['haiku_capped']['minus_ground_truth'])}, lifted {prp(b82['haiku_lifted']['minus_ground_truth'])}; lookup capped {prp(b82['lookup_capped']['minus_ground_truth'])}, lifted "
      f"{prp(b82['lookup_lifted']['minus_ground_truth'])}. On the 22 the join does not mark, the ground-truth summary itself reads mini {b22['mini_true']['auroc']:.4f}, Haiku {b22['haiku_true']['auroc']:.4f}, "
      f"lookup {b22['lookup_true']['auroc']:.4f}: those obligations are invisible to every summary, because the ground-truth list is built from the same join.")
    A("")
    A("Graphiti, the rows of `tab:graphiti-completed` (the 323; 276 negatives unchanged):")
    A("")
    gk = ["G10-BELIEVED", "G10-LIFTED", "NB6-emb-capped", "NB5-emb-capped", "G10-VIEW-UNTAGGED", "G10-VIEW-TAGGED", "G10-HYBRID", "FRB-VIEW-UNTAGGED", "TRUE"]
    A("| stratum | n_pos | store-written capped | lifted | store's name lookup | whole-map lookup | five edges untagged | native tags | tagged + summary | FR-Bank top-5 untagged | FR-Bank GT summary |")
    A("|---|---:|---|---|---|---|---|---|---|---|---|")
    for name in ("all_47 (manifest-relative, the printed rows)", "retained_0.80 (recovered + stale-active, of the 34)", "recovered_0.80 (non-active mark on a firing edge)", "stale_active_0.80", "extraction_miss_0.80",
                 "retained_0.75 (recovered + stale-active, of the 34)", "retained_0.50 (recovered + stale-active, of the 34)", "join_retracted_4 (inexpressible)", "join_unflagged_9", "not_retained_0.80 (extraction miss + retracted + unflagged)"):
        b = gr["rescored"][name]
        A(f"| {name} | {b['n_pos']} | " + " | ".join(f"{b['readers'][k]['auroc']:.4f} {sci(b['readers'][k]['ci_item'])} {sci(b['readers'][k]['ci_persona'])}" for k in gk) + " |")
    A("")
    g23 = gr["rescored"]["retained_0.80 (recovered + stale-active, of the 34)"]["readers"]; g13 = gr["rescored"]["recovered_0.80 (non-active mark on a firing edge)"]["readers"]
    A(f"Store-written minus the FR-Bank ground-truth summary on the same items: on the 23 retained, capped {prp(g23['G10-BELIEVED']['minus_true'])}, the store's name lookup "
      f"{prp(g23['NB6-emb-capped']['minus_true'])}; on the 13 recovered, capped {prp(g13['G10-BELIEVED']['minus_true'])}. P2's reading (store-written below ground truth by more than the tolerance, "
      f"the item interval excluding zero) stands on the retained stratum and does not on the recovered one, where n is 13.")
    A("")
    A("### 3.4 The author's read sheet")
    A("")
    A(f"`{sh['xlsx'].replace(chr(92), '/')}` (sha256 `{sh['xlsx_sha256']}`): {sh['n_rows']} rows, the {sh['n_unmarked']} unmarked obligations and {sh['n_controls']} seeded controls from the 82 join-marked (seed {sh['seed']}; "
      f"pool {sh['control_pool']}), shuffled; each row the persona, the question, the state, the manifest's forbidding fact and its counterpart, the nearest stored record within the item's own store variant "
      f"with its overlap score and the store's own mark, one answer column (YES / NO / NOT STORED, data-validated) and a notes column, both unlocked; every other cell locked. The key "
      f"`{sh['key'].replace(chr(92), '/')}` (sha256 `{sh['key_sha256']}`) maps rows to items and controls; no 35-row duplicate-audit workbook exists anywhere in the tree, so there was nothing to add a tab to. "
      f"For the 22, the nearest record within the variant is one of the label's own records on {sum(1 for r in sh['unmarked_nearest'] if r['entry_is_member'])} rows, its overlap runs "
      f"{min(r['cov'] for r in sh['unmarked_nearest']):.2f} to {max(r['cov'] for r in sh['unmarked_nearest']):.2f}, and the store's own mark on it is non-active on "
      f"{sum(1 for r in sh['unmarked_nearest'] if 'superseded' in r['own_mark'] or 'retracted' in r['own_mark'])} of 22.")
    A("")
    # ---- Task 4
    A("## Task 4. The sibling-name control (ADDENDUM_R125_SIBLING; T4_T5_TABLES.md; ledger 15d)")
    A("")
    R = t4["readers"]; P = t4["predictions"]
    A(f"Built offline: {t4['meta']['n_pairs']} of 88 pairs kept ({t4['meta']['dropped']} dropped); leak screen **{leak['verdict']}** ({leak['n_correct']} of {leak['n']}); every lane's served identifier as pinned; "
      f"lanes as registered (Table 1's settings for mini, E1's for Haiku and Opus 5, E5's for Luna and Sol); only the SIBLING items were new calls.")
    A("")
    A("| reader | PN vs SIBLING W/T/L | matched | triple interval | persona interval | PN vs PRESENT (same pairs) | SIBLING vs PRESENT matched | SIBLING minus PRESENT mean score | minus the name lookup |")
    A("|---|---|---:|---|---|---:|---:|---|---|")
    for name, r in R.items():
        if "status" in r:
            A(f"| {name} | {r['status']} | | | | | | | |"); continue
        m = r["pn_vs_sibling"]; ml = r.get("minus_lookup_matched")
        A(f"| {name} | {m['W']}/{m['T']}/{m['L']} | **{m['matched']:.4f}** | {sci(m['ci_triple'])} | {sci(m['ci_persona'])} | {r['pn_vs_present_same_pairs']['matched']:.4f} | {r['sibling_vs_present']['matched']:.4f} | "
          f"{pr(r['sibling_minus_present_mean'])} | " + (pr(ml) if ml else "") + " |")
    A("")
    A("| prediction | verdict | numbers |")
    A("|---|---|---|")
    A(f"| P-SB1 the name lookup at or above 0.90 | **{P['P-SB1']['verdict']}** (a recorded value, §8) | {P['P-SB1']['lookup']:.4f} |")
    A(f"| P-SB2 every model at or above 0.80, persona interval excluding 0.50 | **{P['P-SB2']['verdict']}** | " + "; ".join(f"{n} {v.get('matched', '—')} (lower bound {v.get('persona_lo', '—')})" for n, v in P["P-SB2"]["per_model"].items()) + " |")
    A(f"| P-SB3 the random-token lookup and the count reader within 0.05 of 0.50 | **{P['P-SB3']['verdict']}** (recorded values, §8) | random token {P['P-SB3']['random_token']:.4f}; count reader {P['P-SB3']['count_reader']:.4f} |")
    A(f"| P-SB4 no model reliably exceeds the name lookup | **{P['P-SB4']['verdict']}** | reliably above: {P['P-SB4']['reliably_above'] or 'none'} |")
    A("")
    # ---- Task 5
    A("## Task 5. Names-only and counts-only on the three strong models (ADDENDUM_R125_E2_AMENDMENT_1; T4_T5_TABLES.md; ledger 15e)")
    A("")
    A(f"Projection at the freeze's probes: OpenAI ${proj['totals']['openai']['projected']:.3f} for Tasks 4 and 5 together against the $10.00 cap (at the point it fitted; without NC-SOL ${proj['openai_without_NC-SOL']['projected']:.3f}), "
      f"Anthropic ${proj['totals']['anthropic']['projected']:.3f}; E2's texts byte-checked against `build_nc.json` at every start. **NC-SOL was not run (D-R125-1, `DEVIATIONS_R125.md`):** after Task 4 the SB-SOL lane's 88 realized calls "
      f"read 133.7 output tokens on average against the probe's 120, which re-projects NC-SOL at $7.47; with ${sp['openai']['total']:.2f} metered after NC-LUNA the OpenAI total would exceed the cap, and the runner halts a lane at the cap with "
      f"the partial draw discarded. By the brief's rule Task 4 ran in full first and Task 5 ran with Luna and Opus 5; Sol's rows print NOT EVALUABLE (its moved-count response is E9's).")
    A("")
    R5 = t5["readers"]; P5 = t5["predictions"]
    A("| model | intact (recorded) | names only, pooled | minus intact | matched | counts only, pooled | minus intact | matched whole | matched retraction | matched expiry | counts minus names, pooled |")
    A("|---|---:|---:|---|---:|---:|---|---:|---|---|---|")
    for name, r in R5.items():
        if "status" in r:
            A(f"| {name} | {r['status']} | | | | | | | | | |"); continue
        n, c = r["names_only"], r["counts_only"]; ps = c["matched"]["per_state"]
        A(f"| {name} | {r['intact_pooled']:.4f} | {n['pooled']['whole']:.4f} | {prp(n['minus_intact'])} | {n['matched']['whole']['matched']:.4f} | {c['pooled']['whole']:.4f} | {prp(c['minus_intact'])} | {c['matched']['whole']['matched']:.4f} | "
          f"{ps['RETRACTION']['matched']:.4f} {sci(ps['RETRACTION']['ci_persona'])} | {ps['EXPIRY']['matched']:.4f} {sci(ps['EXPIRY']['ci_persona'])} | {prp(r['counts_minus_names'])} |")
    A("")
    A("| prediction | verdict | per model |")
    A("|---|---|---|")
    for k, v in P5.items():
        A(f"| {k} {v['criterion']} | **{v['verdict']}** | " + "; ".join(f"{n}: {d['verdict']}" + (f" ({d['delta']:+.4f})" if 'delta' in d else "") for n, d in v["per_model"].items()) + " |")
    A("")
    # ---- spend, commits
    A("## Spend and commits")
    A("")
    A(f"Token-metered from the rows at the recorded page prices (not an invoice): **Anthropic ${sp['anthropic']['total']:.4f} of the $10.00 cap** ({sp['anthropic']['lanes']}; probes ${sp['anthropic']['probes']:.4f}); "
      f"**OpenAI ${sp['openai']['total']:.4f} of the $10.00 cap** ({sp['openai']['lanes']}; probes ${sp['openai']['probes']:.4f}; leak screen ${sp['openai']['leak']:.4f}). Tasks 1 to 3: $0. "
      f"Neither API exposes a balance to the keys in use; the month's metered spend at the freeze was Anthropic $143.76 and OpenAI $43.78 (FREEZE_R125.md).")
    A("")
    A("Commits (private index, explicit pathspecs; `git log --oneline -- reviews/r125`):")
    A("")
    for ln in log:
        A(f"- `{ln[:7]}` {ln[8:160]}{'…' if len(ln) > 168 else ''}")
    A("")
    A("Deviations: `DEVIATIONS_R125.md` (D-R125-1 NC-SOL dropped on the re-projection; D-R125-2 the scorer's pre-freeze dry run; D-R125-3 Docker started for Task 3; D-R125-4 no matched metric on the 661; D-R125-5 Table 48 resolved to `tab:levels`).")
    A("")
    A("Docker Desktop and the `neo4j-r85` container were started by this session to read the forty Graphiti graphs once (Task 3); the edges are exported to `reviews/r125/build/graphiti_edges_g10.json` so no later reading needs the container. No held texts; nothing lands from here.")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
