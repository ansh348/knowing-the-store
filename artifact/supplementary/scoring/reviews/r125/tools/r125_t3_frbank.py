# -*- coding: utf-8 -*-
"""r125_t3_frbank.py -- Task 3, FR-Bank: the obligation labels relative to what the store retains (offline, post hoc). NO MODEL CALL. $0.

The store S in the scored store-written condition is FR-Bank's own persona bank (e0's frozen banks, one per persona; 536 entries for aisha,
18,936 over the forty), rendered by the one renderer from the store's own fields (`index_v2.believed_lifecycle`: is_active, is_retracted,
supersedes) into the store-written summary, capped at fifteen names per category (the committed INDEXED-BELIEVED texts) or with the cap
lifted (the S2-U texts). The PN labels come from the manifest (hand-verified), and each obligation's forbidding records are its
`pn_members`, entry identifiers of that same bank, so the forbidding content is stored by construction for every one of the 104
obligations; what varies is whether the ground-truth join (`index_v2.true_lifecycle`, manifest events aligned to entries at the 0.80 bar)
marks one of them, and whether FR-Bank's own metadata marks one of them non-active.

Counts, over the 104 obligations (and by state):
  A. join-marked at the 0.80 bar (the recorded alignment: 82 = 63 / 8 / 11, AUX-DS-FLAGCENSUS), and at the two bands the census already
     uses, 0.75 and 0.50 (the supersession / retraction detector's threshold lowered; the expiry rule is the join's own TAU_GOLD 0.50 at
     every band, so expiry marks do not move);
  B. own-marked: a member carries FR-Bank's own non-active mark (believed_superseded = not is_active, or believed_retracted);
  C. the cross-tabulation, and the 22 unmarked obligations with the nearest stored record (the best token coverage of the manifest's
     forbidding fact over every entry of the persona's bank) and its overlap score, for the author's sheet.
Re-scoring: the store-written rows of tab:levels (GPT-4.1 mini, Haiku 4.5, the name lookup; ground truth, capped, lifted) with the
positives restricted to each stratum and the 557 negatives unchanged: AUROC with the item-level and the persona-grouped single-arm
bootstrap, and the store-written-minus-ground-truth paired difference with both intervals (cf2_score.paired), n printed.
Gates: mini TRUE 0.7339 / BELIEVED 0.5959 / lifted 0.6513; Haiku TRUE 0.8210 / capped 0.7069 / lifted 0.7364; lookup 0.7484 / 0.5858 / 0.6588.
Writes reviews/r125/results/r125_t3_frbank.json.
"""
from __future__ import annotations

import collections
import json
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import auroc, r4  # noqa: E402
sys.path.insert(0, str(C.ROOT / "resp_review" / "tools")); sys.path.insert(0, str(C.ROOT / "e0_metamemory" / "tools")); sys.path.insert(0, str(C.ROOT / "e1_metamemory" / "tools"))
import resp_common as RC  # noqa: E402
from e0_common import MIN_DISCR, MIN_SHARED, TAU_GOLD, cov, load_joins, toks  # noqa: E402
from index_v2 import TAU_HI, detect, true_lifecycle  # noqa: E402
from common_e1r import POPULATIONS, boot_cluster_single, load_e1  # noqa: E402
from run_nb6 import build as nb6_build, emb_scores  # noqa: E402
from index_v3 import named_sections  # noqa: E402
from cf2_score import paired  # noqa: E402
from a1_count_readers import boot_item_single  # noqa: E402

OUT = C.RESULTS / "r125_t3_frbank.json"
BANDS = (0.80, 0.75, 0.50)
STATE = {"sup": "SUPERSESSION", "ret": "RETRACTION", "exp": "EXPIRY"}
GATES = {"mini_true": 0.7339, "mini_capped": 0.5959, "mini_lifted": 0.6513, "haiku_true": 0.8210, "haiku_capped": 0.7069, "haiku_lifted": 0.7364,
         "lookup_true": 0.7484, "lookup_capped": 0.5858, "lookup_lifted": 0.6588}
RECORDED_JOIN = {"n": 82, "sup": 63, "ret": 8, "exp": 11}


def lifecycle_at(J, tau):
    """index_v2.true_lifecycle with the supersession / retraction threshold at `tau` (0.80 reproduces the committed function; expiry at TAU_GOLD)."""
    if tau == TAU_HI:
        s, r, e, _ = true_lifecycle(J, J.etoks)
        return s, r, e
    superseded, retracted, expired = set(), set(), set()
    for sec in ("supersession_events", "contradictions"):
        for rec in (J.y.get(sec) or []):
            if not isinstance(rec, dict):
                continue
            d = detect(rec.get("old_fact"), rec.get("new_fact"), J.etoks, J.drop)
            if d is None:
                continue
            superseded |= {i for i, s in d.items() if s >= tau}
    for rec in (J.y.get("retractions") or []):
        if not isinstance(rec, dict):
            continue
        d = detect(rec.get("original_fact"), rec.get("retraction"), J.etoks, J.drop)
        if d:
            retracted |= {i for i, s in d.items() if s >= tau}
    for rec in (J.y.get("expiring_logistics") or []):
        if not isinstance(rec, dict) or str(rec.get("status") or "").strip().lower() != "expired":
            continue
        ft = toks(rec.get("fact"), J.drop)
        if len(ft) < MIN_DISCR:
            continue
        expired |= {i for i, t in J.etoks.items() if len(ft & t) >= MIN_SHARED and cov(ft, t) >= TAU_GOLD}
    return superseded, retracted, expired


def forbidding_events(J, state):
    """The manifest's forbidding facts of the obligation's state: (label, fact, counterpart)."""
    ev = []
    if state == "sup":
        for sec in ("supersession_events", "contradictions"):
            for rec in (J.y.get(sec) or []):
                if isinstance(rec, dict) and rec.get("old_fact") and rec.get("new_fact"):
                    ev.append((sec, rec["old_fact"], rec["new_fact"]))
    elif state == "ret":
        for rec in (J.y.get("retractions") or []):
            if isinstance(rec, dict) and rec.get("original_fact"):
                ev.append(("retraction", rec["original_fact"], rec.get("retraction")))
    else:
        for rec in (J.y.get("expiring_logistics") or []):
            if isinstance(rec, dict) and str(rec.get("status") or "").strip().lower() == "expired" and rec.get("fact"):
                ev.append(("expiry", rec["fact"], None))
    return ev


def nearest(J, fact, counterpart, members):
    """Over every entry of the persona's bank: the best coverage of the forbidding fact's tokens (the detector's discriminative coverage where a
    counterpart exists, else plain coverage), the best entry, and the best coverage over the obligation's own members."""
    ft = toks(fact, J.drop)
    if counterpart:
        nt = toks(counterpart, J.drop); do = ft - nt
        base = do if len(do) >= MIN_DISCR else ft
    else:
        base = ft
    best = (0.0, None); best_m = (0.0, None)
    for eid, t in J.etoks.items():
        if len(base & t) < MIN_SHARED:
            continue
        c = cov(base, t)
        if c > best[0]:
            best = (c, eid)
        if eid in members and c > best_m[0]:
            best_m = (c, eid)
    return best, best_m, len(base)


def collapse_h45(path, arm, key="item_id"):
    per = collections.defaultdict(dict)
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("arm") == arm and r.get("status") == "OK" and r.get("nok") is not None:
            per[r[key]][int(r["draw"])] = float(r["nok"])
    return {u: float(np.mean(list(d.values()))) for u, d in per.items() if len(d) >= 3}


def main():
    sub = RC.load_cell()                                   # the 661 with state, pn_members, blind / true (mini) rows
    ids = [it["item_id"] for it in sub]; y = np.array([it["y_nok"] for it in sub], int); g = np.array([it["persona"] for it in sub])
    st = np.array([it["state"] for it in sub]); pos = [k for k in range(661) if y[k] == 1]
    joins = load_joins()
    bank = {(e["persona"], e["entry_id"]): e for e in C.jload(C.ROOT / "e1_metamemory" / "backend_entries" / "frbank.json")}
    # ---- A, B: the marks per obligation
    life = {tau: {p: lifecycle_at(joins[p], tau) for p in joins} for tau in BANDS}
    obl = []
    for k in pos:
        it = sub[k]; p = it["persona"]; members = list(it["pn_members"]); J = joins[p]
        row = {"item_id": it["item_id"], "persona": p, "state": it["state"], "variant": it["variant"], "members": members, "question": it["question"]}
        for tau in BANDS:
            s_, r_, e_ = life[tau][p]
            row[f"join_marked_{tau:.2f}"] = bool(any(m in s_ or m in r_ or m in e_ for m in members))
            row[f"join_state_{tau:.2f}"] = ("ret" if any(m in r_ for m in members) else "sup" if any(m in s_ for m in members) else "exp" if any(m in e_ for m in members) else None)
        own = [(m, bank[(p, m)]["believed_superseded"] == "True" or bank[(p, m)]["believed_superseded"] is True, bank[(p, m)]["believed_retracted"] == "True" or bank[(p, m)]["believed_retracted"] is True) for m in members if (p, m) in bank]
        row["own_marked"] = bool(any(a or b for _, a, b in own)); row["own_marks"] = {m: ("superseded" if a else "") + ("retracted" if b else "") or "active" for m, a, b in own}
        row["members_stored"] = bool(all((p, m) in bank for m in members)) and len(members) > 0
        # the nearest stored record of the manifest's forbidding facts of this state (the best over the persona's events)
        best_ev = None
        for lab, fact, cp in forbidding_events(J, it["state"]):
            (c, eid), (cm, em), nt = nearest(J, fact, cp, set(members))
            cand = {"event": lab, "fact": fact, "counterpart": cp, "best_entry": eid, "best_cov": r4(c), "best_entry_text": (J.by_id[eid]["text"] if eid else None),
                    "best_entry_is_member": bool(eid in members), "best_member": em, "best_member_cov": r4(cm), "n_tokens": nt,
                    "best_entry_own_mark": (("superseded" if not J.by_id[eid]["is_active"] else "active") + ("; retracted" if J.by_id[eid].get("is_retracted") else "")) if eid else None}
            if best_ev is None or (cand["best_member_cov"] or 0) > (best_ev["best_member_cov"] or 0) or ((cand["best_member_cov"] or 0) == (best_ev["best_member_cov"] or 0) and (cand["best_cov"] or 0) > (best_ev["best_cov"] or 0)):
                best_ev = cand
        row["nearest"] = best_ev
        row["member_texts"] = {m: J.by_id[m]["text"] for m in members if m in J.by_id}
        obl.append(row)
    n_join = {tau: sum(r[f"join_marked_{tau:.2f}"] for r in obl) for tau in BANDS}
    by_state = {tau: dict(collections.Counter(r["state"] for r in obl if r[f"join_marked_{tau:.2f}"])) for tau in BANDS}
    got = {"n": n_join[0.80], **by_state[0.80]}
    assert got == RECORDED_JOIN, ("the recorded alignment does not reproduce", got, RECORDED_JOIN)
    n_own = sum(r["own_marked"] for r in obl); own_state = dict(collections.Counter(r["state"] for r in obl if r["own_marked"]))
    cross = collections.Counter((r["join_marked_0.80"], r["own_marked"]) for r in obl)
    unmarked = [r for r in obl if not r["join_marked_0.80"]]
    assert len(unmarked) == 22
    print(f"A. join-marked: " + "; ".join(f"{tau:.2f}: {n_join[tau]} of 104 {by_state[tau]}" for tau in BANDS))
    print(f"B. own-marked (FR-Bank's own non-active mark on a member): {n_own} of 104 {own_state}; members stored for {sum(r['members_stored'] for r in obl)} of 104")
    print(f"C. cross (join 0.80, own): {dict(cross)}; the 22 unmarked: " + ", ".join(f"{r['item_id']} ({r['state']}; own {'marked' if r['own_marked'] else 'active'}; nearest cov {r['nearest']['best_cov'] if r['nearest'] else None})" for r in unmarked))

    # ---- the readers on the 661
    items, blind, idxT, idxB = load_e1()
    src = [it for it in items if POPULATIONS["R-NOK-FRB"]["filt"](it)]
    rows_t = {r["item_id"]: r for r in nb6_build(src, blind, idxT, "nok", "TRUE")}; rows_b = {r["item_id"]: r for r in nb6_build(src, blind, idxB, "nok", "BELIEVED")}
    s2 = C.jload(C.ROOT / "side_experiments" / "s2" / "indexes_s2u.json"); s2map = {it["item_id"]: it for it in s2["items"]}
    lifted_lists = {i: named_sections(s2["indexes"][s2map[i]["index_key_s2u"]])["superseded"] for i in ids}
    V = {}
    V["mini_true"] = np.array([it["true"]["nok"] for it in sub], float); V["mini_blind"] = np.array([it["blind"]["nok"] for it in sub], float)
    V["mini_capped"] = np.array([idxB[i]["nok"] for i in ids], float)
    side = {}
    for line in open(C.ROOT / "side_experiments" / "run" / "rows_side.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if r["arm"] == "INDEXED-S2U" and r["status"] == "OK":
            side[r["item_id"]] = float(r["nok"])
    V["mini_lifted"] = np.array([side[i] for i in ids], float)
    h_true = collapse_h45(C.ROOT / "r74" / "x4" / "rows_H45.jsonl", "INDEXED-TRUE"); V["haiku_true"] = np.array([h_true[i] for i in ids], float)
    h_cap = collapse_h45(C.ROOT / "believed_h" / "rows" / "INDEXED-BELIEVED-15" / "rows_H45.jsonl", "INDEXED-BELIEVED-15", "unit_id"); V["haiku_capped"] = np.array([h_cap[i] for i in ids], float)
    h_lift = collapse_h45(C.ROOT / "believed_h" / "rows" / "INDEXED-BELIEVED-LIFTED" / "rows_H45.jsonl", "INDEXED-BELIEVED-LIFTED", "unit_id"); V["haiku_lifted"] = np.array([h_lift[i] for i in ids], float)
    V["lookup_true"] = np.array(emb_scores([rows_t[i] for i in ids], "sup"), float)
    V["lookup_capped"] = np.array(emb_scores([rows_b[i] for i in ids], "sup"), float)
    V["lookup_lifted"] = np.array(emb_scores([{"question": sub[k]["question"], "sup": lifted_lists[ids[k]]} for k in range(661)], "sup"), float)
    gates = {k: r4(auroc(V[k], y)) for k in GATES}
    for k, want in GATES.items():
        assert gates[k] == want, (k, gates[k], want)
    print("gates", gates, "PASS")

    # ---- the strata: positives restricted, negatives unchanged
    strata = {"all_104 (manifest-relative, the printed rows)": [k for k in pos]}
    for tau in BANDS:
        strata[f"join_marked_{tau:.2f}"] = [k for k, r in zip(pos, obl) if r[f"join_marked_{tau:.2f}"]]
    strata["join_unmarked_0.80 (the 22)"] = [k for k, r in zip(pos, obl) if not r["join_marked_0.80"]]
    strata["own_marked"] = [k for k, r in zip(pos, obl) if r["own_marked"]]
    strata["own_active (no store mark on any member)"] = [k for k, r in zip(pos, obl) if not r["own_marked"]]
    strata["join_marked_0.80_and_own_marked"] = [k for k, r in zip(pos, obl) if r["join_marked_0.80"] and r["own_marked"]]
    strata["join_marked_0.80_and_own_active"] = [k for k, r in zip(pos, obl) if r["join_marked_0.80"] and not r["own_marked"]]
    for s in ("sup", "ret", "exp"):
        strata[f"state_{s}_join_marked_0.80"] = [k for k, r in zip(pos, obl) if r["join_marked_0.80"] and r["state"] == s]
        strata[f"state_{s}_own_marked"] = [k for k, r in zip(pos, obl) if r["own_marked"] and r["state"] == s]
    neg = [k for k in range(661) if y[k] == 0]; assert len(neg) == 557
    READERS = [("mini_true", "GPT-4.1 mini, ground truth"), ("mini_capped", "GPT-4.1 mini, store-written capped"), ("mini_lifted", "GPT-4.1 mini, store-written lifted"),
               ("haiku_true", "Haiku 4.5, ground truth"), ("haiku_capped", "Haiku 4.5, store-written capped"), ("haiku_lifted", "Haiku 4.5, store-written lifted"),
               ("lookup_true", "Name lookup, ground-truth list"), ("lookup_capped", "Name lookup, store-written capped list"), ("lookup_lifted", "Name lookup, store-written lifted list"),
               ("mini_blind", "GPT-4.1 mini, question only")]
    rescored = {}
    for name, kp in strata.items():
        keep = sorted(kp + neg); yy = y[keep]; gg = g[keep]
        blk = {"n_pos": len(kp), "n": len(keep), "by_state": dict(collections.Counter(st[k] for k in kp)), "readers": {}}
        for key, label in READERS:
            v = V[key][keep]
            d = {"label": label, "auroc": r4(auroc(v, yy)), "ci_item": boot_item_single(v, yy), "ci_persona": boot_cluster_single(v, yy, gg)}
            if key.endswith("_capped") or key.endswith("_lifted"):
                base = V[key.split("_")[0] + "_true"][keep]
                d["minus_ground_truth"] = paired(base, v, yy, gg)
            blk["readers"][key] = d
        rescored[name] = blk
        print(f"  {name:48s} n_pos {len(kp):3d} " + " ".join(f"{key.split('_')[0][:2]}{key.split('_')[1][:3]} {blk['readers'][key]['auroc']:.4f}" for key, _ in READERS[:9]))
    res = {"meta": {"script": "reviews/r125/tools/r125_t3_frbank.py", "model_calls": 0, "status": "post hoc, offline", "bands": list(BANDS), "n_boot": C.N_BOOT, "seed": C.SEED,
                    "join": "index_v2.true_lifecycle (supersession / retraction detector at the band; expiry at TAU_GOLD 0.50 at every band)", "own_mark": "FR-Bank believed_superseded (not is_active) or believed_retracted on a pn_member",
                    "store": "FR-Bank's persona bank (e1_metamemory/backend_entries/frbank.json; e0's frozen banks through e0_common.load_joins)"},
           "gates": gates, "counts": {"join_marked": {f"{tau:.2f}": {"n": n_join[tau], "by_state": by_state[tau]} for tau in BANDS}, "own_marked": {"n": n_own, "by_state": own_state},
                                      "cross_join080_own": {f"join={a},own={b}": n for (a, b), n in cross.items()}, "members_stored": sum(r["members_stored"] for r in obl), "unmarked_22": [r["item_id"] for r in unmarked]},
           "obligations": obl, "strata": {k: len(v) for k, v in strata.items()}, "rescored": rescored}
    C.jdump(res, OUT)
    print(f"-> {OUT.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
