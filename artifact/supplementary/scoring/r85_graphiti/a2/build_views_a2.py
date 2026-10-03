# -*- coding: utf-8 -*-
"""build_views_a2.py -- R85 Amendment 2 Step 1: the U / T / M views on both stores, the prompt variants and digests, the view census,
the section 5 quantities, the evidence-in-view flags, the by-eye draw. NO MODEL CALL. $0. Frozen text: AUX-R85-A2-FREEZE (asserted).

Populations (section 3): primary the 178 FULL non-ABSENT items (47 obligations / 131 licensed) on both stores; the FR-Bank-only block
the 100 ablated-variant non-ABSENT items. Sources: Graphiti r85_graphiti/g10/retrieval_g10.json (Step 5's ten rendered lines with RULE 1
states, AUX-R85-G10-RETRIEVE); FR-Bank resp_review/l2/retrieval.json top10_ids with FR-Bank's own marks (amend1_resp.believed_flags,
resp_common.render_line). Conditions (section 4): U ranks 1-5 with the lifecycle field removed under the U prompts; T ranks 1-5 with the
store's state under SYSTEM_ANSWER / USER_ANSWER_A4; M the active lines of ranks 1-10, the first five, renumbered from [1] (the freeze's
item 5), under the T prompts. Answer sharing: one call per distinct complete input (system, user) keyed by sha256.

Writes r85_graphiti/a2/views_a2.json (every cell's lines, prompts, flags, the job table) and a2/census_a2.json; appends AUX-R85-A2-PROMPTS,
-VIEWS, -RESOLUTION, -CHECK (assertions; the reading by eye recorded below the key) to r85_graphiti/NUMBERS_R85.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump, r4  # noqa: E402
sys.path.insert(0, str(R85 / "g10"))
import resp_common as RC                                                     # noqa: E402
import amend1_resp as A1                                                     # noqa: E402
import run_ds as RD                                                          # noqa: E402
import prompts_ds as PD                                                      # noqa: E402
import amend4_header as A4                                                   # noqa: E402
from e0_common import toks, cov, MIN_SHARED, TAU_GOLD, load_joins           # noqa: E402

REG = ROOT / "registrations" / "ADDENDUM_R85_GRAPHITI_AMENDMENT_2.md"
REG_SHA = "b87401f3604fed8d4db3e2fa20d758b274748374f876374321880e674c2fab92"
LEDGER = R85 / "NUMBERS_R85.md"
OUT_VIEWS = HERE / "views_a2.json"
OUT_CENSUS = HERE / "census_a2.json"
OUT_CHECK = HERE / "checkpoint_views_a2.md"
LIFE_RE = re.compile(r"^\[(\d+)\] lifecycle: [^|]*? \| ")
RANK_RE = re.compile(r"^\[(\d+)\] ")
SEED = 42
# the U prompt: SYSTEM_ANSWER's lifecycle sentences removed and the phrase changed; USER_ANSWER_A4's phrase changed
SYS_OLD_SENTENCES = (" An entry marked active is what the store currently holds as true. An entry marked superseded has been replaced by a later entry; "
                     "one marked retracted was withdrawn by the user; one marked expired describes an arrangement whose date has passed. Superseded, "
                     "retracted and expired entries do not state the user's current situation and must not be given as the answer.")
SYS_PHRASE_OLD, SYS_PHRASE_NEW = "each entry carries the lifecycle metadata the store records for it.", "each entry carries the metadata the store records for it."
USER_PHRASE_OLD, USER_PHRASE_NEW = "each with the lifecycle metadata the store records for it", "each with the metadata the store records for it"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def assert_lineage():
    assert_spec()
    h = hashlib.sha256(REG.read_bytes()).hexdigest(); assert h == REG_SHA, f"Amendment 2 sha256 {h} != the freeze -- STOP"
    assert "AUX-R85-A2-FREEZE" in LEDGER.read_text(encoding="utf-8") and REG_SHA in LEDGER.read_text(encoding="utf-8"), "the freeze is not ledgered -- STOP"
    lk4 = J(ROOT / "ds_downstream" / "run" / "lock_amend4.json")
    assert sha(A4.USER_ANSWER_A4) == lk4["user_answer_a4_sha256"] and PD.digests() == lk4["prompts_ds"], "the A4 prompts differ from AUX-DS-A4-LOCK -- STOP"


def prompts():
    assert PD.SYSTEM_ANSWER.count(SYS_OLD_SENTENCES) == 1 and PD.SYSTEM_ANSWER.count(SYS_PHRASE_OLD) == 1
    s_u = PD.SYSTEM_ANSWER.replace(SYS_OLD_SENTENCES, "").replace(SYS_PHRASE_OLD, SYS_PHRASE_NEW)
    assert "lifecycle" not in s_u.split("\n")[0] and "marked" not in s_u and "store does not currently contain the answer" in s_u
    assert A4.USER_ANSWER_A4.count(USER_PHRASE_OLD) == 1
    u_u = A4.USER_ANSWER_A4.replace(USER_PHRASE_OLD, USER_PHRASE_NEW)
    assert "lifecycle" not in u_u and "{name}" in u_u and "{date}" in u_u and "{view}" in u_u and "{question}" in u_u
    return {"SYSTEM_ANSWER": PD.SYSTEM_ANSWER, "USER_ANSWER_A4": A4.USER_ANSWER_A4, "SYSTEM_ANSWER_U": s_u, "USER_ANSWER_A4_U": u_u}


def untag(line):
    u = LIFE_RE.sub(r"[\1] ", line, count=1)
    assert u != line and u.startswith("[") and "lifecycle:" not in u, line
    return u


def renumber(line, r):
    return RANK_RE.sub(f"[{r}] ", line, count=1)


def state_of(line):
    m = re.match(r"^\[\d+\] lifecycle: ([^|]*?) \| ", line); assert m, line
    return m.group(1)


def covers(field, drop, text):
    if not field:
        return False
    ft = toks(field, drop); A = toks(text or "", drop)
    return bool(len(ft & A) >= MIN_SHARED and cov(ft, A) >= TAU_GOLD)


def line_text(line):
    return line.split(" | text: ", 1)[1]


def main():
    assert_lineage(); sys.stdout.reconfigure(encoding="utf-8")
    PR = prompts(); pdig = {k: sha(v) for k, v in PR.items()}
    sub = RC.load_cell(); byid = {it["item_id"]: it for it in sub}; rec = RD.records(sub); pf = A4.persona_fields()
    ret_fr = J(ROOT / "resp_review/l2/retrieval.json")["items"]; bf = A1.believed_flags()
    g10 = J(R85 / "g10" / "retrieval_g10.json")["items"]; reach_g = J(R85 / "g10" / "results" / "reach_g10.json")["rows"]
    z4 = J(ROOT / "reviews/r113/results/z4_a2_frbank_views.json")["views"]
    pops = {"primary_178": [it for it in sub if it["variant"] == "FULL" and it["label"] != "ABSENT"], "frbank_only_100": [it for it in sub if it["variant"] != "FULL" and it["label"] != "ABSENT"]}
    assert len(pops["primary_178"]) == 178 and len(pops["frbank_only_100"]) == 100
    cells = {}          # (store, population) -> {item: {U, T, M lines, flags}}
    jobs = {}           # input sha -> job
    rows = []           # (store, population, condition, item) -> job key
    n_z4_equal = 0

    def make_views(store, ten_tagged, tags10):
        T = ten_tagged[:5]; U = [untag(l) for l in T]
        assert all(t.split(" | ", 1)[1] == u.split("] ", 1)[1] for t, u in zip(T, U))
        act = [r for r in range(len(ten_tagged)) if tags10[r] == "active"][:5]
        M = [renumber(ten_tagged[r], k + 1) for k, r in enumerate(act)]
        assert all(state_of(l) == "active" for l in M)
        n_na5 = sum(1 for r in range(min(5, len(ten_tagged))) if tags10[r] != "active")
        assert (n_na5 == 0) == ("\n".join(T) == "\n".join(M)) or (len(ten_tagged) < 5)
        return U, T, M, act, n_na5

    for pname, pop in pops.items():
        stores = ("frbank", "graphiti") if pname == "primary_178" else ("frbank",)
        for store in stores:
            cell = {}
            for it in pop:
                iid, per = it["item_id"], it["persona"]; rc = rec.get(iid)
                if store == "frbank":
                    ids = ret_fr[iid]["top10_ids"]; assert len(ids) == 10
                    own = [bf[per][e] for e in ids]; tags10 = [RC.lifecycle_tag(f) for f in own]
                    ten = [RC.render_line(r + 1, own[r]) for r in range(10)]; ten_ids = ids
                else:
                    L = g10[iid]["lines"]; ten = [l["tagged"] for l in L]; tags10 = [l["state"] for l in L]; ten_ids = [l["uuid"] for l in L]
                U, T, M, act, n_na5 = make_views(store, ten, tags10)
                if store == "frbank":
                    z = z4[iid]; assert z["U"] == U and z["T"] == T and z["M"] == M, (iid, "differs from the R113 pre-freeze build"); n_z4_equal += 1
                # evidence-in-view flags per condition (section 6): licensed -> gold; with-replacement obligation -> successor (the record's gold field)
                ev = {}
                for cond, lines in (("U", U), ("T", T), ("M", M)):
                    texts = [line_text(l) for l in lines]
                    if it["label"] == "PRESENT":
                        ev[cond] = any(covers(rc["gold_field"], rc["drop"], t) for t in texts) if (rc and rc.get("gold_field")) else None
                    elif it["subtype"] == "with-replacement":
                        ev[cond] = any(covers(rc["gold_field"], rc["drop"], t) for t in texts) if (rc and rc.get("gold_field")) else None
                    else:
                        ev[cond] = None
                # mechanism sets (section 5 (ii))
                fl = {"tags_1_10": tags10, "n_non_active_1_5": n_na5, "M_ids": [ten_ids[r] for r in act], "M_ranks": [r + 1 for r in act], "evidence_in_view": ev}
                if it["y_nok"]:
                    pm = set(it.get("pn_members") or [])
                    if store == "frbank":
                        fire5 = [r for r in range(5) if ten_ids[r] in pm]; fire10 = [r for r in range(10) if ten_ids[r] in pm]
                    else:
                        rr = reach_g[iid]; fire10 = [r - 1 for r in rr["firing_ranks"]]; fire5 = [r for r in fire10 if r < 5]
                    reached = bool(fire5)
                    fl.update({"a_reached": reached, "b_reached_marked": bool(reached and any(tags10[r] != "active" for r in fire5)),
                               "c_reached_unmarked": bool(reached and all(tags10[r] == "active" for r in fire5)),
                               "e_imported": any((r in fire10) and tags10[r] == "active" for r in act if r >= 5), "g_unreached_10": not bool(fire10), "firing_ranks": [r + 1 for r in fire10]})
                else:
                    cover = [covers(rc["gold_field"], rc["drop"], line_text(l)) for l in T] if (rc and rc.get("gold_field")) else []
                    fl.update({"gold_covered_1_5": cover, "f_evidence_removed": any(cover[r] and tags10[r] != "active" for r in range(len(cover))), "evidence_in_view_T": any(cover)})
                cell[iid] = {"item_id": iid, "persona": per, "question": it["question"], "label": it["label"], "state": it["state"], "intent": it["intent"], "subtype": it["subtype"], "attack_vector": it["attack_vector"],
                             "U": U, "T": T, "M": M, "flags": fl}
                name, date = pf[per]
                for cond, lines in (("U", U), ("T", T), ("M", M)):
                    sysm = PR["SYSTEM_ANSWER_U"] if cond == "U" else PR["SYSTEM_ANSWER"]
                    user = (PR["USER_ANSWER_A4_U"] if cond == "U" else PR["USER_ANSWER_A4"]).format(name=name, date=date, view="\n".join(lines), question=it["question"])
                    key = sha(sysm + "\n\x00\n" + user)
                    j = jobs.setdefault(key, {"key": key, "system": sysm, "user": user, "system_sha256": sha(sysm), "user_sha256": sha(user), "persona": per, "question": it["question"], "n_lines": len(lines), "members": []})
                    j["members"].append({"store": store, "population": pname, "condition": cond, "item_id": iid})
                    rows.append({"store": store, "population": pname, "condition": cond, "item_id": iid, "key": key, "label": it["label"], "state": it["state"], "intent": it["intent"], "subtype": it["subtype"]})
            cells[f"{store}|{pname}"] = cell
    # ---------------------------------------------------------------- census and the section 5 quantities
    census = {}
    for ck, cell in cells.items():
        store, pname = ck.split("|"); pop = pops[pname]
        keys = {c: {sha((PR["SYSTEM_ANSWER_U"] if c == "U" else PR["SYSTEM_ANSWER"]) + "\n\x00\n" + (PR["USER_ANSWER_A4_U"] if c == "U" else PR["USER_ANSWER_A4"]).format(name=pf[v["persona"]][0], date=pf[v["persona"]][1], view="\n".join(v[c]), question=v["question"])) for v in cell.values()} for c in ("U", "T", "M")}
        t_eq_m = sum(1 for v in cell.values() if "\n".join(v["T"]) == "\n".join(v["M"]))
        n_tm = len(cell) - t_eq_m
        obl = [v for v in cell.values() if v["label"] == "PRESENT-NEGATIVE"]; lic = [v for v in cell.values() if v["label"] == "PRESENT"]
        n_tm_o = sum(1 for v in obl if "\n".join(v["T"]) != "\n".join(v["M"])); n_tm_l = n_tm - n_tm_o
        short = collections.Counter(len(v["M"]) for v in cell.values() if len(v["M"]) < 5)
        sets = {k: sum(1 for v in obl if v["flags"].get(k)) for k in ("a_reached", "b_reached_marked", "c_reached_unmarked", "e_imported", "g_unreached_10")}
        f_removed = collections.Counter(v["intent"] for v in lic if v["flags"].get("f_evidence_removed")); f_inview = collections.Counter(v["intent"] for v in lic if v["flags"].get("evidence_in_view_T"))
        census[ck] = {"n": len(cell), "n_obligations": len(obl), "n_licensed": len(lic), "distinct_inputs": {c: len(keys[c]) for c in keys}, "distinct_inputs_all": len(set().union(*keys.values())),
                      "T_equals_M": t_eq_m, "n_TM": n_tm, "bound_T_vs_M": r4(n_tm / len(cell)), "n_TM_obligations": n_tm_o, "bound_obligations": r4(n_tm_o / len(obl)), "n_TM_licensed": n_tm_l, "bound_licensed": r4(n_tm_l / len(lic)),
                      "M_short_views": sum(short.values()), "M_short_lengths": dict(sorted(short.items())), "lines_removed_T_to_M": sum(v["flags"]["n_non_active_1_5"] for v in cell.values()),
                      "sets": sets, "f_evidence_removed_by_intent": dict(f_removed), "f_evidence_in_view_T_by_intent": dict(f_inview), "licensed_by_intent": dict(collections.Counter(v["intent"] for v in lic)),
                      "evidence_in_view": {c: {"licensed_yes": sum(1 for v in lic if v["flags"]["evidence_in_view"][c]), "with_replacement_yes": sum(1 for v in obl if v["subtype"] == "with-replacement" and v["flags"]["evidence_in_view"][c]), "with_replacement_n": sum(1 for v in obl if v["subtype"] == "with-replacement")} for c in ("U", "T", "M")},
                      "reading_rule_A2_P2": ("HOLDS structurally (bound below 0.05)" if n_tm_o / len(obl) < 0.05 else "empirical (bound at or above 0.05)")}
    # the R113 gate on the FR-Bank primary cell
    c = census["frbank|primary_178"]; assert (c["n_TM"], c["M_short_views"], c["sets"]["a_reached"], c["sets"]["b_reached_marked"], c["sets"]["c_reached_unmarked"], c["sets"]["e_imported"], c["sets"]["g_unreached_10"]) == (163, 63, 26, 23, 3, 10, 13), c
    # ---------------------------------------------------------------- the by-eye draw (seed 42; five per store; at least one per condition)
    rng = random.Random(SEED)
    draw = {}
    for store in ("graphiti", "frbank"):
        ids_ = sorted(cells[f"{store}|primary_178"]); picks = rng.sample(ids_, 5); conds = ["U", "T", "M", "T", "M"]
        draw[store] = [(i, c) for i, c in zip(picks, conds)]
    fmt_ok = 0
    for ck, cell in cells.items():
        store = ck.split("|")[0]
        for v in cell.values():
            for l in v["U"]:
                assert "lifecycle:" not in l
            for l in v["T"]:
                assert state_of(l) == "active" or (set(state_of(l).split(", ")) <= {"superseded", "expired", "retracted"} and state_of(l)), l   # resp_common.lifecycle_tag's order (retracted, superseded, expired) or RULE 1's single state
                if store == "graphiti":
                    assert " | category: not expressible by this backend | " in l
            assert [int(RANK_RE.match(l).group(1)) for l in v["M"]] == list(range(1, len(v["M"]) + 1))
            assert v["flags"]["M_ranks"] == sorted(v["flags"]["M_ranks"]) and all(state_of(l) == "active" for l in v["M"])
            fmt_ok += 1
    L = [f"# The Amendment 2 by-eye draw (seed {SEED}; section 4): five Graphiti and five FR-Bank views on the 178, at least one per condition\n\n",
         f"Assertions on every view of every cell passed ({fmt_ok} item-cells): U carries no `lifecycle:` field; every T state is a store state; the marker on category on every Graphiti line; M renumbered [1]..[n] in rank order with every line `active`.\n\n"]
    for store, picks in draw.items():
        for iid, cnd in picks:
            v = cells[f"{store}|primary_178"][iid]; name, date = pf[v["persona"]]
            L.append(f"## {store} {iid} condition {cnd} (label {v['label']}, intent {v['intent']}, {name}, t_now {date})\n\nQuestion: {v['question']}\n\n### U\n```\n" + "\n".join(v["U"]) + "\n```\n### T\n```\n" + "\n".join(v["T"]) + "\n```\n### M (ranks kept " + str(v["flags"]["M_ranks"]) + ")\n```\n" + "\n".join(v["M"]) + "\n```\n\n")
    io.open(OUT_CHECK, "w", encoding="utf-8", newline="\n").write("".join(L))
    # ---------------------------------------------------------------- write
    meta = {"script": "r85_graphiti/a2/build_views_a2.py", "registration_sha256": REG_SHA, "prompts_sha256": pdig, "M_rule": "active lines of ranks 1 to 10 in rank order, the first five, renumbered from [1] (the freeze's item 5)",
            "answer_sharing": "one call per distinct complete input (system, user), keyed by sha256", "frbank_r113_equal": n_z4_equal, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump({"meta": meta, "prompts": PR, "cells": cells, "jobs": list(jobs.values()), "rows": rows, "draw": draw}, OUT_VIEWS)
    jdump({"meta": meta, "census": census, "n_jobs": len(jobs), "n_rows": len(rows)}, OUT_CENSUS)
    nj = collections.Counter(m["store"] + "|" + m["population"] for j in jobs.values() for m in j["members"][:1])
    txt = [f"\n### AUX-R85-A2-PROMPTS — the four prompt texts (Step 1, 2026-09-17; `a2/build_views_a2.py`): `SYSTEM_ANSWER` `{pdig['SYSTEM_ANSWER'][:16]}…`, `USER_ANSWER_A4` `{pdig['USER_ANSWER_A4'][:16]}…` (AUX-DS-A4-LOCK); `SYSTEM_ANSWER_U` `{pdig['SYSTEM_ANSWER_U'][:16]}…` (the lifecycle sentences from \"An entry marked active\" to \"must not be given as the answer.\" removed and \"each entry carries the lifecycle metadata\" -> \"each entry carries the metadata\", two asserted replaces), `USER_ANSWER_A4_U` `{pdig['USER_ANSWER_A4_U'][:16]}…` (\"each with the lifecycle metadata the store records for it\" -> \"each with the metadata the store records for it\", one asserted replace). The abstention instruction stays in both system prompts.\n\n",
           f"### AUX-R85-A2-VIEWS — the view census (`a2/views_a2.json`, `a2/census_a2.json`); FR-Bank's views equal the R113 pre-freeze build on {n_z4_equal} of 278 items\n\n",
           "| cell | n (obl. / lic.) | distinct inputs U / T / M (all) | T = M | n_TM (bound) | obligations n_TM (bound) | licensed n_TM (bound) | M short views (lengths) | lines removed T -> M | A2-P2 reading rule |\n|---|---|---|---:|---|---|---|---|---:|---|\n"]
    for ck, c in census.items():
        txt.append(f"| {ck} | {c['n']} ({c['n_obligations']} / {c['n_licensed']}) | {c['distinct_inputs']['U']} / {c['distinct_inputs']['T']} / {c['distinct_inputs']['M']} ({c['distinct_inputs_all']}) | {c['T_equals_M']} | **{c['n_TM']}** ({c['bound_T_vs_M']}) | {c['n_TM_obligations']} ({c['bound_obligations']}) | {c['n_TM_licensed']} ({c['bound_licensed']}) | {c['M_short_views']} ({c['M_short_lengths']}) | {c['lines_removed_T_to_M']} | {c['reading_rule_A2_P2']} |\n")
    txt.append(f"\nDistinct complete inputs over every cell: **{len(jobs)}** (nominal {len(rows)} rows); per cell {dict(nj)}.\n\n### AUX-R85-A2-RESOLUTION — section 5 (ii) the mechanism sets and the evidence-in-view flags (section 6), per cell\n\n| cell | (a) reached | (b) reached, marked | (c) reached, unmarked | (e) imported | (g) unreached in 10 | (f) evidence removed by intent (of licensed with evidence in T) | evidence in view, licensed U / T / M (of n) | evidence in view, with-replacement U / T / M (of n) |\n|---|---:|---:|---:|---:|---:|---|---|---|\n")
    for ck, c in census.items():
        s = c["sets"]; e = c["evidence_in_view"]
        txt.append(f"| {ck} | {s['a_reached']} | {s['b_reached_marked']} | {s['c_reached_unmarked']} | {s['e_imported']} | {s['g_unreached_10']} | {c['f_evidence_removed_by_intent']} (of {c['f_evidence_in_view_T_by_intent']}) | {e['U']['licensed_yes']} / {e['T']['licensed_yes']} / {e['M']['licensed_yes']} (of {c['n_licensed']}) | {e['U']['with_replacement_yes']} / {e['T']['with_replacement_yes']} / {e['M']['with_replacement_yes']} (of {e['T']['with_replacement_n']}) |\n")
    txt.append(f"\nThe structural bound (section 5 (i)) is n_TM / n; U against T and U against M carry no bound (the prompts differ on every item). On Graphiti set (a) uses `census_forbidding.py`'s matcher on the retrieved edges (AUX-R85-G10-REACH); on FR-Bank the member identifier.\n\n### AUX-R85-A2-CHECK — the by-eye check (section 4; performed 2026-09-17 by the executing session under the author's instruction, not by the author): the assertions hold on every view of every cell ({fmt_ok} item-cells); the seeded draw is `a2/checkpoint_views_a2.md` (Graphiti {', '.join(i + ':' + c for i, c in draw['graphiti'])}; FR-Bank {', '.join(i + ':' + c for i, c in draw['frbank'])}), read by eye before Step 2 (the reading recorded below this key).\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write("".join(txt))
    print("".join(txt))


if __name__ == "__main__":
    main()
