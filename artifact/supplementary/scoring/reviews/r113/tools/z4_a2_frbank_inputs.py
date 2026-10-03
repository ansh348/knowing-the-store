# -*- coding: utf-8 -*-
"""z4_a2_frbank_inputs.py -- SPEC_R113 section Z4: the FR-Bank side of R85 Amendment 2's views (U / T / M) and its section 5
quantities, built from the UNFROZEN draft's definitions before its freeze. NO MODEL CALL. $0. Nothing is answered; no prompt
is sent. Inputs: resp_review/l2/retrieval.json (top10_ids), amend1_resp.believed_flags() (FR-Bank's own marks), resp_common
render_line / true_flags, run_ds.records + e0_common toks / cov for the evidence-in-view flag, ds_downstream/run/scores_amend4.json
for the reference row (read, never re-run). Writes reviews/r113/results/z4_a2_frbank_views.json (the views and the flags) and
z4_a2_frbank_counts.json; appends AUX-R113-Z4-* to NUMBERS_R113.md.
Line rule for M (a build choice recorded for the author): the active lines of ranks 1 to 10 in rank order, the first five, renumbered
[1].. consecutively, so that where ranks 1 to 5 hold no non-active line M is byte-identical to T (the draft's shared-answer case).
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import re

from r113_common import ROOT, RESULTS, J, jdump, assert_spec, ledger_append, r4

import resp_common as RC          # noqa: E402
import amend1_resp as A1          # noqa: E402
import run_ds as RD               # noqa: E402
from e0_common import toks, cov, MIN_SHARED, TAU_GOLD   # noqa: E402

DRAFT = ROOT / "registrations" / "ADDENDUM_R85_GRAPHITI_AMENDMENT_2.md"
LIFE_RE = re.compile(r"^\[(\d+)\] lifecycle: [^|]*? \| ")
RANK_RE = re.compile(r"^\[(\d+)\] ")


def untag(line):
    u = LIFE_RE.sub(r"[\1] ", line, count=1)
    assert u != line and u.startswith("[") and "lifecycle:" not in u, line
    return u


def renumber(line, r):
    return RANK_RE.sub(f"[{r}] ", line, count=1)


def main():
    assert_spec()
    draft_sha = hashlib.sha256(DRAFT.read_bytes()).hexdigest()
    sub = RC.load_cell(); ret = J(ROOT / "resp_review/l2/retrieval.json")["items"]
    bf = A1.believed_flags(); tf = RC.true_flags(); rec = RD.records(sub)
    a4 = J(ROOT / "ds_downstream/run/scores_amend4.json"); views_ds = J(ROOT / "ds_downstream/views.json")["items"]
    pops = {"primary_178": [it for it in sub if it["variant"] == "FULL" and it["label"] != "ABSENT"],
            "frbank_only_100": [it for it in sub if it["variant"] != "FULL" and it["label"] != "ABSENT"]}
    assert len(pops["primary_178"]) == 178 and len(pops["frbank_only_100"]) == 100
    views, counts = {}, {}
    for pname, pop in pops.items():
        c = {"n": len(pop), "n_obligations": sum(it["y_nok"] for it in pop), "n_licensed": sum(1 - it["y_nok"] for it in pop),
             "distinct_inputs": {"U": 0, "T": 0, "M": 0}, "T_equals_M": 0, "n_TM": 0, "M_short_views": 0, "M_lines_removed_total": 0, "U_T_lines_changed_total": 0,
             "sets": {k: 0 for k in ("a_reached", "b_reached_marked", "c_reached_unmarked", "e_imported", "g_unreached")},
             "f_evidence_removed_by_intent": collections.Counter(), "licensed_by_intent": collections.Counter(), "f_evidence_in_view_by_intent": collections.Counter(),
             "M_short_lengths": collections.Counter()}
        shas = {"U": set(), "T": set(), "M": set()}
        for it in pop:
            per = it["persona"]; ids = ret[it["item_id"]]["top10_ids"]; assert len(ids) == 10
            own = [bf[per][e] for e in ids]; tags = [RC.lifecycle_tag(f) for f in own]
            T = [RC.render_line(r + 1, own[r]) for r in range(5)]
            U = [untag(l) for l in T]
            assert all(t.split(" | ", 1)[1] == u.split("] ", 1)[1] for t, u in zip(T, U))
            act = [(r, ids[r]) for r in range(10) if tags[r] == "active"][:5]
            M = [renumber(RC.render_line(r + 1, own[r]), k + 1) for k, (r, _) in enumerate(act)]
            assert all(" lifecycle: active | " in l for l in M)
            n_na5 = sum(1 for r in range(5) if tags[r] != "active")
            t_eq_m = (n_na5 == 0); assert t_eq_m == ("\n".join(T) == "\n".join(M))
            c["T_equals_M"] += t_eq_m; c["n_TM"] += (not t_eq_m); c["M_short_views"] += (len(M) < 5); c["M_lines_removed_total"] += n_na5; c["U_T_lines_changed_total"] += 5
            if len(M) < 5:
                c["M_short_lengths"][len(M)] += 1
            for k, L in (("U", U), ("T", T), ("M", M)):
                shas[k].add(hashlib.sha256("\n".join(L).encode()).hexdigest())
            pm = set(it.get("pn_members") or [])
            flags = {"pn_in_1_5": sorted(pm & set(ids[:5])), "pn_in_6_10": sorted(pm & set(ids[5:10])), "pn_in_M": sorted(pm & {e for _, e in act}),
                     "own_tags_1_10": tags, "join_tags_1_10": [RC.lifecycle_tag(tf[per][e]) for e in ids]}
            if it["y_nok"]:
                reached = bool(flags["pn_in_1_5"])
                if reached:
                    c["sets"]["a_reached"] += 1
                    marked = any(tags[r] != "active" for r in range(5) if ids[r] in pm)
                    c["sets"]["b_reached_marked" if marked else "c_reached_unmarked"] += 1
                if any(e in pm and tags[r] == "active" for r, e in act if r >= 5):
                    c["sets"]["e_imported"] += 1
                if not (pm & set(ids[:10])):
                    c["sets"]["g_unreached"] += 1
                flags.update({"reached": reached, "imported": any(e in pm and tags[r] == "active" for r, e in act if r >= 5), "unreached_10": not bool(pm & set(ids[:10]))})
            else:
                c["licensed_by_intent"][it["intent"]] += 1
                rc = rec.get(it["item_id"]); cover = []
                if rc and rc.get("gold_field"):
                    gt = toks(rc["gold_field"], rc["drop"])
                    for r in range(5):
                        A = toks(own[r]["text"] or "", rc["drop"]); cv = cov(gt, A)
                        cover.append(bool(len(gt & A) >= MIN_SHARED and cv >= TAU_GOLD))
                ev_in_view = any(cover); removed = any(cover[r] and tags[r] != "active" for r in range(len(cover)))
                if ev_in_view:
                    c["f_evidence_in_view_by_intent"][it["intent"]] += 1
                if removed:
                    c["f_evidence_removed_by_intent"][it["intent"]] += 1
                flags.update({"gold_covered_1_5": cover, "evidence_in_view": ev_in_view, "evidence_removed_by_M": removed, "gold_record_known": bool(rc and rc.get("gold_field"))})
            views[it["item_id"]] = {"population": pname, "label": it["label"], "state": it["state"], "intent": it["intent"], "persona": per, "question": it["question"],
                                    "top10_ids": ids, "U": U, "T": T, "M": M, "M_ids": [e for _, e in act], "flags": flags}
        c["distinct_inputs"] = {k: len(v) for k, v in shas.items()}
        c["structural_bound_T_vs_M"] = r4(c["n_TM"] / c["n"]); c["structural_bound_T_vs_M_obligations"] = None
        # the bound on the obligation rows alone and on the licensed rows alone
        nTM_o = sum(1 for it in pop if it["y_nok"] and any(t != "active" for t in views[it["item_id"]]["flags"]["own_tags_1_10"][:5]))
        nTM_l = c["n_TM"] - nTM_o
        c["n_TM_obligations"] = nTM_o; c["n_TM_licensed"] = nTM_l
        c["structural_bound_T_vs_M_obligations"] = r4(nTM_o / c["n_obligations"]); c["structural_bound_T_vs_M_licensed"] = r4(nTM_l / c["n_licensed"])
        for k in ("f_evidence_removed_by_intent", "licensed_by_intent", "f_evidence_in_view_by_intent", "M_short_lengths"):
            c[k] = dict(c[k])
        counts[pname] = c
    # ---- the reference row: DS Amendment 4's ALWAYS row (header prompt), restricted to the 178, read from the record
    ref = {}
    for code in ("MINI", "H45"):
        pr = a4["per_row"][code]; rows_path = ROOT / "ds_downstream/run" / f"rows_ds_amend4_{code.lower()}.jsonl"
        ans = {}
        for l in io.open(rows_path, encoding="utf-8"):
            r = json.loads(l); ans[r["key"]] = r
        R = {"licensed": {"n": 0, "answered": 0, "abstained": 0, "correct_050": 0, "correct_080": 0, "in_view": 0},
             "obligations": {"n": 0, "reached_k5": 0, "reached_answered": 0, "reached_abstained": 0, "scorable_reached_answered": 0, "stale_050_scorable": 0, "stale_080_scorable": 0, "successor_use_sup": 0, "expiry_unscorable_reached": 0, "not_reached_no_row": 0}}
        st1 = J(ROOT / "ds_downstream/stage1.json")["per_item"]
        for it in pops["primary_178"]:
            key = f"{it['item_id']}|{views_ds[it['item_id']]['ALWAYS']['sha']}"; row = pr.get(key); a = ans.get(key)
            if it["label"] == "PRESENT":
                R["licensed"]["n"] += 1; R["licensed"]["in_view"] += bool(st1[it["item_id"]]["ALWAYS"]["gold_in_view"])
                assert row is not None and a is not None, key
                ab = A1_is_abst(a["answer"]); R["licensed"]["abstained"] += ab; R["licensed"]["answered"] += (not ab)
                R["licensed"]["correct_050"] += bool(row.get("correct")); R["licensed"]["correct_080"] += bool(row.get("correct_tau_hi"))
            else:
                R["obligations"]["n"] += 1
                if not st1[it["item_id"]]["ALWAYS"]["reach"]:
                    R["obligations"]["not_reached_no_row"] += 1; continue
                R["obligations"]["reached_k5"] += 1; assert row is not None and a is not None, key
                ab = A1_is_abst(a["answer"]); R["obligations"]["reached_abstained"] += ab; R["obligations"]["reached_answered"] += (not ab)
                if it["state"] == "exp":
                    R["obligations"]["expiry_unscorable_reached"] += 1
                elif not ab:
                    R["obligations"]["scorable_reached_answered"] += 1
                    R["obligations"]["stale_050_scorable"] += bool(row.get("stale_use_tau_gold")); R["obligations"]["stale_080_scorable"] += bool(row.get("stale_use"))
                    R["obligations"]["successor_use_sup"] += bool(row.get("successor_use"))
        ref[code] = R
    res = {"meta": {"script": "reviews/r113/tools/z4_a2_frbank_inputs.py", "spec": "SPEC_R113 Z4", "model_calls": 0, "draft": str(DRAFT.relative_to(ROOT)), "draft_sha256_at_this_pass": draft_sha,
                    "draft_status": "UNFROZEN; these views are a pre-freeze build from its section 4 definitions and are superseded by the amendment's own Step 1 under its frozen text",
                    "M_line_rule": "active lines of ranks 1 to 10 in rank order, the first five, renumbered consecutively from [1]", "when": dt.datetime.now().isoformat(timespec="seconds")},
           "counts": counts, "reference_row_a4_always_on_178": ref}
    jdump(res, RESULTS / "z4_a2_frbank_counts.json")
    jdump({"meta": res["meta"], "views": views}, RESULTS / "z4_a2_frbank_views.json")
    L = [f"\n## 4. AUX-R113-Z4: R85 Amendment 2's FR-Bank inputs, built from the unfrozen draft (SPEC_R113 Z4; draft sha256 `{draft_sha[:16]}...`; no call; nothing answered)\n\n",
         "Views per item from `resp_review/l2/retrieval.json` `top10_ids` rendered with FR-Bank's own marks (`amend1_resp.believed_flags`, `resp_common.render_line`): T ranks 1 to 5 with the store's state; U the same lines with the `lifecycle:` field removed (asserted: exactly that field differs on every line); M the active lines of ranks 1 to 10 in rank order, the first five, renumbered from [1] (every M line reads `active`, asserted; T = M byte-identically where ranks 1 to 5 hold no non-active line, asserted). The views: `reviews/r113/results/z4_a2_frbank_views.json`. The graph side is not built: `neo4j-r85` is down at this pass and the stock retrieval needs Graphiti's embedding call (AUX-R113-Z5).\n\n",
         "### AUX-R113-Z4-VIEWS and AUX-R113-Z4-RESOLUTION: the view census and the section 5 quantities on FR-Bank\n\n| population | n (obl. / lic.) | distinct inputs U / T / M | T = M | n_TM (bound n_TM / n) | n_TM obligations (bound) | n_TM licensed (bound) | M short views (lengths) | lines removed T -> M | (a) reached | (b) reached, marked | (c) reached, unmarked | (e) imported | (g) unreached in 10 | (f) evidence removed by intent (licensed with evidence in ranks 1 to 5, by intent) |\n|---|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---|\n"]
    for pname, c in counts.items():
        s = c["sets"]
        L.append(f"| {pname} | {c['n']} ({c['n_obligations']} / {c['n_licensed']}) | {c['distinct_inputs']['U']} / {c['distinct_inputs']['T']} / {c['distinct_inputs']['M']} | {c['T_equals_M']} | **{c['n_TM']}** ({c['structural_bound_T_vs_M']}) | {c['n_TM_obligations']} ({c['structural_bound_T_vs_M_obligations']}) | {c['n_TM_licensed']} ({c['structural_bound_T_vs_M_licensed']}) | {c['M_short_views']} ({c['M_short_lengths']}) | {c['M_lines_removed_total']} | {s['a_reached']} | {s['b_reached_marked']} | {s['c_reached_unmarked']} | {s['e_imported']} | {s['g_unreached']} | {c['f_evidence_removed_by_intent']} (of {c['f_evidence_in_view_by_intent']}; licensed {c['licensed_by_intent']}) |\n")
    L.append("\nThe structural bound is the draft's quantity (i): the paired T-versus-M difference in any endpoint cannot exceed n_TM / n because identical complete inputs share one answer. Sets (a) to (g) are the draft's descriptive mechanism sets and bound nothing. Set (f) uses the gold field's token coverage of the line text at TAU_GOLD with MIN_SHARED (`run_ds.records`, `e0_common.toks` / `cov`).\n\n")
    L.append("### AUX-R113-Z4-REFERENCE: DS Amendment 4's ALWAYS row (the header prompt; the join's tags; the recorded top-5) restricted to the 178 from `ds_downstream/run/scores_amend4.json` `per_row` (read, never re-run)\n\n| answerer | licensed: n, gold in view, answered / abstained, correct at 0.50 / 0.80 | obligations: n, reached at k = 5 (no row otherwise), answered / abstained, scorable answered, stale at 0.50 / 0.80, successor use (supersession), expiry reached (unscorable) |\n|---|---|---|\n")
    for code, R in ref.items():
        l, o = R["licensed"], R["obligations"]
        L.append(f"| {code} | {l['n']}, {l['in_view']}, {l['answered']} / {l['abstained']}, **{l['correct_050']}** / {l['correct_080']} | {o['n']}, {o['reached_k5']} ({o['not_reached_no_row']} unreached), {o['reached_answered']} / {o['reached_abstained']}, {o['scorable_reached_answered']}, **{o['stale_050_scorable']}** / {o['stale_080_scorable']}, {o['successor_use_sup']}, {o['expiry_unscorable_reached']} |\n")
    ledger_append("".join(L))


def A1_is_abst(a):
    import amend4_header as A4
    return bool(A4.is_abst(a))


if __name__ == "__main__":
    main()
