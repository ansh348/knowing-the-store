# -*- coding: utf-8 -*-
"""build_views_g10.py -- R85 Amendment 1 Step 5 (section 4 C), the tag-route views on the 323 (D-R85-17). NO API CALL. NO WRITE TO THE GRAPH.

From g10/retrieval_raw_g10.json (stock Graphiti.search, ten edges per item) and the persona's whole edge set (census.read_edges,
RULE 1 states by census.derive, RULE 2 names, D-R85-10 ages): every retrieved edge's state and its rendered line in Amendment 1's
format; the untagged line = the tagged line with the `lifecycle:` field removed and nothing else (asserted); all ten lines kept per
item with each edge's state (Amendment 2 section 4's build requirement); the VIEW-UNTAGGED / VIEW-TAGGED blocks (ranks 1 to 5).
FR-Bank VIEW-UNTAGGED (D-R85-14): resp_review/l2/retrieval.json top5_ids re-rendered by resp_common.render_line over the join's flags
(asserted equal to the recorded RETRIEVED block) with the field removed. Reach (census_forbidding.py's matcher on the retrieved edges),
the tag census, the prompt variant (one asserted str.replace) and its digests, the seeded ten-view checkpoint draw.

Writes g10/retrieval_g10.json, g10/views_g10.json, g10/checkpoint_views.md; appends AUX-R85-G10-RETRIEVE, -REACH, -TAGS, -PROMPTS,
-CHECK (the assertions; the reading by eye is recorded by the session in the same key) to NUMBERS_R85.md.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R85 = HERE.parent
ROOT = R85.parent
sys.path.insert(0, str(ROOT / "reviews" / "r114" / "tools"))
from r114_common import assert_spec, J, jdump  # noqa: E402
sys.path.insert(0, str(R85)); sys.path.insert(0, str(HERE))
import census as C                                                           # noqa: E402
import graphiti_index as G                                                   # noqa: E402
import census_forbidding as CF                                               # noqa: E402
import resp_common as RC                                                     # noqa: E402
import prompts_resp as PR                                                    # noqa: E402
from index_v2 import MARKER, true_lifecycle                                  # noqa: E402
from e0_common import load_joins, parse_dt, toks, cov, MIN_SHARED, MIN_DISCR  # noqa: E402

RAW = HERE / "retrieval_raw_g10.json"
OUT_RET = HERE / "retrieval_g10.json"
OUT_VIEWS = HERE / "views_g10.json"
OUT_CHECK = HERE / "checkpoint_views.md"
LEDGER = R85 / "NUMBERS_R85.md"
K_USE = 5
PHRASE_OLD, PHRASE_NEW = "each with the lifecycle metadata the store records", "each with the metadata the store records"
SEED = 42


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def line_tagged(rank, state, slot, age, fact):
    a = "unknown" if age is None else f"{age} days"
    return f"[{rank}] lifecycle: {state} | category: {MARKER} | attribute: {slot} | age: {a} | text: {fact}"


def untag(line):
    """The tagged line with the lifecycle field removed and nothing else changed."""
    head, rest = line.split("] ", 1)
    assert rest.startswith("lifecycle: "), line
    field, rest2 = rest.split(" | ", 1)
    out = head + "] " + rest2
    assert out.count(" | ") == line.count(" | ") - 1 and "lifecycle:" not in out
    return out


def frbank_untag(line):
    head, rest = line.split("] ", 1)
    assert rest.startswith("lifecycle: "), line
    return head + "] " + rest.split(" | ", 1)[1]


def prompt_variant():
    assert PR.SYSTEM_RETRIEVED.count(PHRASE_OLD) == 1 and PR.USER_RETRIEVED.count(PHRASE_OLD) == 1
    s = PR.SYSTEM_RETRIEVED.replace(PHRASE_OLD, PHRASE_NEW); u = PR.USER_RETRIEVED.replace(PHRASE_OLD, PHRASE_NEW)
    assert s != PR.SYSTEM_RETRIEVED and u != PR.USER_RETRIEVED and "lifecycle metadata" not in s and "lifecycle metadata" not in u
    return s, u


def main():
    assert_spec(); sys.stdout.reconfigure(encoding="utf-8")
    raw = J(RAW); items = raw["items"]; assert len(items) == 323 and raw["meta"]["llm_calls"] == 0
    joins = load_joins(); sub = RC.load_cell(); byid = {it["item_id"]: it for it in sub}
    tf = RC.true_flags(); ret_fr = J(ROOT / "resp_review" / "l2" / "retrieval.json")["items"]
    cens = {r["item_id"]: r for r in J(HERE / "census_forbidding_g10.json")["obligations"]}
    # per-persona edge sets, states, names, ages
    per = {}
    for p in sorted({v["persona"] for v in items.values()}):
        edges = C.read_edges(f"r85stock_{p}_g10"); states = C.derive(edges); Jp = joins[p]
        info = {}
        for e in edges:
            d = parse_dt(e["valid_at"]) or parse_dt(e["created_at"])
            age = max((Jp.t_now - d).days, 0) if (d and Jp.t_now) else None
            info[e["uuid"]] = {"state": states[e["uuid"]], "slot": G.attribute_name(e["name"], C.label_of(e)), "age": age, "fact": e["fact"], "edge": e}
        sup, rexp, exp, _ = true_lifecycle(Jp, Jp.etoks)
        per[p] = {"edges": edges, "states": states, "info": info, "events": CF.join_events(Jp), "join": {"superseded": sup, "retracted": rexp, "expired": exp}}
    # ---------------------------------------------------------------- Graphiti views
    rec, views = {}, {}
    n_lines, n_states, short = 0, collections.Counter(), collections.Counter()
    for iid, v in items.items():
        p = v["persona"]; P_ = per[p]; it = byid[iid]
        assert len(v["edges"]) <= 10, (iid, len(v["edges"]))
        short[len(v["edges"])] += 1                      # the stock config's sim_min_score 0.6 can return fewer than ten (D-R85-20)
        lines = []
        for r, e in enumerate(v["edges"], 1):
            inf = P_["info"].get(e["uuid"]); assert inf is not None, (iid, e["uuid"], "retrieved edge not in the persona's graph")
            same_t = lambda a, b: (parse_dt(a) is None and parse_dt(b) is None) or (parse_dt(a) is not None and parse_dt(b) is not None and abs((parse_dt(a) - parse_dt(b)).total_seconds()) < 1)   # noqa: E731
            assert inf["fact"] == e["fact"] and same_t(inf["edge"]["invalid_at"], e["invalid_at"]) and same_t(inf["edge"]["expired_at"], e["expired_at"]) and same_t(inf["edge"]["valid_at"], e["valid_at"]), (iid, r)
            tl = line_tagged(r, inf["state"], inf["slot"], inf["age"], e["fact"]); ul = untag(tl)
            lines.append({"rank": r, "uuid": e["uuid"], "state": inf["state"], "slot": inf["slot"], "age": inf["age"], "fact": e["fact"], "tagged": tl, "untagged": ul,
                          "valid_at": e["valid_at"], "invalid_at": e["invalid_at"], "expired_at": e["expired_at"]})
            n_lines += 1; n_states[inf["state"]] += 1
        rec[iid] = {"item_id": iid, "persona": p, "question": v["question"], "label": it["label"], "state": it["state"], "group_id": v["group_id"], "lines": lines,
                    "embed_tokens": v["embed_tokens"], "embed_calls": v["embed_calls"]}
        views[iid] = {"item_id": iid, "persona": p, "question": v["question"], "label": it["label"], "state": it["state"],
                      "graphiti_tagged": "\n".join(l["tagged"] for l in lines[:K_USE]), "graphiti_untagged": "\n".join(l["untagged"] for l in lines[:K_USE]),
                      "graphiti_states_top5": [l["state"] for l in lines[:K_USE]], "graphiti_states_top10": [l["state"] for l in lines]}
    # ---------------------------------------------------------------- FR-Bank untagged (D-R85-14)
    n_lock = 0
    for iid in views:
        it = byid[iid]; r = ret_fr[iid]; ids = r["top5_ids"]; assert len(ids) == 5
        tagged = "\n".join(RC.render_line(k + 1, tf[it["persona"]][e]) for k, e in enumerate(ids))
        assert tagged == r["block"], (iid, "the re-rendered RETRIEVED block differs from the record")
        n_lock += 1
        views[iid]["frbank_tagged_true"] = tagged
        views[iid]["frbank_untagged"] = "\n".join(frbank_untag(l) for l in tagged.split("\n"))
        views[iid]["frbank_top5_ids"] = ids
    # ---------------------------------------------------------------- reach and the tag census
    reach = {"k5": 0, "k10": 0, "n": 0, "per_state": collections.defaultdict(lambda: [0, 0, 0]), "by_join_state": collections.Counter(), "unflagged": 0, "retracted_by_retraction_event": 0}
    tags_view = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}; tags_all = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    reach_rows = {}
    for iid, v in views.items():
        it = byid[iid]
        if it["label"] != "PRESENT-NEGATIVE":
            continue
        p = it["persona"]; P_ = per[p]; Jp = joins[p]; members = it["pn_members"]; cr = cens[iid]
        reach["n"] += 1; reach["by_join_state"][cr["join_state"]] += 1
        marked_sup = [m for m in members if m in P_["join"]["superseded"] or m in P_["join"]["expired"]]
        marked_ret = [m for m in members if m in P_["join"]["retracted"]]
        evs = [(k, o, n) for (k, o, n) in P_["events"] if (k != "retraction" and any(CF.marks_record(k, o, n, Jp, m) for m in marked_sup)) or (k == "retraction" and any(CF.marks_record(k, o, n, Jp, m) for m in marked_ret))]
        if not evs:
            reach["unflagged"] += 1
        edges10 = [l["uuid"] for l in rec[iid]["lines"]]; ed = {u: P_["info"][u]["edge"] for u in edges10}
        fired = {}
        for k, o, n in evs:
            fired.update(CF.fires_on_edges(k, o, n, Jp, [ed[u] for u in edges10]))
        r5 = any(u in fired for u in edges10[:K_USE]); r10 = bool(fired)
        reach["k5"] += int(r5); reach["k10"] += int(r10)
        reach["per_state"][it["state"]][0] += 1; reach["per_state"][it["state"]][1] += int(r5); reach["per_state"][it["state"]][2] += int(r10)
        best = min((edges10.index(u) + 1 for u in fired), default=None)
        reach_rows[iid] = {"join_state": cr["join_state"], "state": it["state"], "marking_events": len(evs), "reach_k5": r5, "reach_k10": r10, "best_rank": best,
                           "firing_ranks": sorted(edges10.index(u) + 1 for u in fired), "firing_non_active_in_top5": sum(1 for u in edges10[:K_USE] if u in fired and P_["states"][u] != "active")}
        # the tag census over the forbidding records in view (ranks 1 to 5 that fire): store non-active against the join's mark (the members are join-marked non-active when evs is non-empty)
        for u in edges10[:K_USE]:
            if u in fired:
                store_na = P_["states"][u] != "active"; join_na = bool(evs)
                tags_view[("tp" if store_na else "fn") if join_na else ("fp" if store_na else "tn")] += 1
    # over every retrieved line of the 323 (ranks 1 to 5): store non-active against "fires on any join event of the persona"
    for iid, v in rec.items():
        p = v["persona"]; P_ = per[p]; Jp = joins[p]
        fired_any = set()
        ed = [P_["info"][l["uuid"]]["edge"] for l in v["lines"][:K_USE]]
        for k, o, n in P_["events"]:
            fired_any |= set(CF.fires_on_edges(k, o, n, Jp, ed))
        for l in v["lines"][:K_USE]:
            store_na = l["state"] != "active"; join_na = l["uuid"] in fired_any
            tags_all[("tp" if store_na else "fn") if join_na else ("fp" if store_na else "tn")] += 1
    # ---------------------------------------------------------------- prompts
    s_u, u_u = prompt_variant()
    prompts = {"SYSTEM_RETRIEVED": sha(PR.SYSTEM_RETRIEVED), "USER_RETRIEVED": sha(PR.USER_RETRIEVED), "USER_HYBRID": sha(PR.USER_HYBRID),
               "SYSTEM_RETRIEVED_UNTAGGED": sha(s_u), "USER_RETRIEVED_UNTAGGED": sha(u_u), "replace": [PHRASE_OLD, PHRASE_NEW], "texts": {"SYSTEM_RETRIEVED_UNTAGGED": s_u, "USER_RETRIEVED_UNTAGGED": u_u}}
    # ---------------------------------------------------------------- the checkpoint draw
    rng = random.Random(SEED); ids_sorted = sorted(views)
    draw_g = sorted(rng.sample(ids_sorted, 5)); draw_f = sorted(rng.sample(ids_sorted, 5))
    fmt_ok = 0
    for iid in ids_sorted:
        v = views[iid]
        for tl, ul in zip(v["graphiti_tagged"].split("\n"), v["graphiti_untagged"].split("\n")):
            if not tl:
                assert not ul and not rec[iid]["lines"]; continue          # the one item the stock search returned nothing for (D-R85-20)
            assert tl.split(" | ")[1] == f"category: {MARKER}" and tl.split(" | ")[0].split("] ")[1].startswith("lifecycle: ") and untag(tl) == ul
            st = tl.split(" | ")[0].split("lifecycle: ")[1]; assert st in ("active", "superseded", "expired")
        for tl, ul in zip(v["frbank_tagged_true"].split("\n"), v["frbank_untagged"].split("\n")):
            assert frbank_untag(tl) == ul and "lifecycle:" not in ul
        fmt_ok += 1
    L = [f"# The Step 5 checkpoint draw (seed {SEED}; Amendment 1 section 4 C): five Graphiti views and five FR-Bank untagged views, to be checked by eye against build_l2.py's format\n\n",
         f"Assertions on every one of the 323 items passed ({fmt_ok} of 323): field order `[r] lifecycle | category | attribute | age | text`; the marker on category on every Graphiti line; the untagged line equal to the tagged line with exactly the `lifecycle:` field removed; the state one of active / superseded / expired; the FR-Bank re-render equal to the recorded RETRIEVED block.\n\n"]
    for iid in draw_g:
        v = views[iid]; p = v["persona"]; tn = joins[p].t_now.date().isoformat()
        L.append(f"## Graphiti {iid} (label {v['label']}, persona t_now {tn})\n\nQuestion: {v['question']}\n\n### tagged\n```\n{v['graphiti_tagged']}\n```\n### untagged\n```\n{v['graphiti_untagged']}\n```\n### age arithmetic (valid_at -> days before t_now)\n")
        for l in rec[iid]["lines"][:K_USE]:
            L.append(f"- [{l['rank']}] valid_at {l['valid_at']} invalid_at {l['invalid_at']} expired_at {l['expired_at']} -> age {l['age']} state {l['state']}\n")
        L.append("\n")
    for iid in draw_f:
        v = views[iid]
        L.append(f"## FR-Bank {iid} (label {v['label']})\n\nQuestion: {v['question']}\n\n### tagged (the recorded RETRIEVED block, the join's tags)\n```\n{v['frbank_tagged_true']}\n```\n### untagged\n```\n{v['frbank_untagged']}\n```\n\n")
    io.open(OUT_CHECK, "w", encoding="utf-8", newline="\n").write("".join(L))
    # ---------------------------------------------------------------- write
    meta = {"script": "r85_graphiti/g10/build_views_g10.py", "source": str(RAW.relative_to(ROOT)), "search": raw["meta"], "k_take": 10, "k_use": K_USE, "line_format": "[r] lifecycle: <state> | category: " + MARKER + " | attribute: <RULE 2 name> | age: <days before t_now, D-R85-10> | text: <edge.fact>",
            "population": "the 323 FULL-variant items (D-R85-17)", "frbank_lock": f"{n_lock} of 323 re-rendered RETRIEVED blocks equal to the record", "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump({"meta": meta, "items": rec}, OUT_RET)
    jdump({"meta": {**meta, "prompts": {k: v for k, v in prompts.items() if k != "texts"}}, "prompts": prompts, "checkpoint_draw": {"graphiti": draw_g, "frbank": draw_f}, "items": views}, OUT_VIEWS)
    reach["per_state"] = dict(reach["per_state"]); reach["by_join_state"] = dict(reach["by_join_state"])
    jdump({"reach": reach, "rows": reach_rows, "tags_forbidding_in_view": tags_view, "tags_all_lines_top5": tags_all}, HERE / "results" / "reach_g10.json")
    st_top5 = collections.Counter(s for v in views.values() for s in v["graphiti_states_top5"])
    tv, ta = tags_view, tags_all
    prec = lambda t: (t["tp"] / (t["tp"] + t["fp"])) if (t["tp"] + t["fp"]) else None      # noqa: E731
    recl = lambda t: (t["tp"] / (t["tp"] + t["fn"])) if (t["tp"] + t["fn"]) else None      # noqa: E731
    txt = (f"\n### AUX-R85-G10-RETRIEVE — Step 5, the tag-route retrieval on the 323 (2026-09-17, program R114; `g10/retrieve.py` in the stock venv, `g10/build_views_g10.py`; `g10/retrieval_raw_g10.json`, `g10/retrieval_g10.json`, `g10/views_g10.json`)\n\n"
           f"Stock `Graphiti.search(question, group_ids=[r85stock_<persona>_g10], num_results=10)` (`EDGE_HYBRID_SEARCH_RRF`, default `SearchFilters()`), graphiti-core 0.28.1 from site-packages, one `text-embedding-3-small` call per question: 323 calls, {raw['meta']['embed_tokens']} tokens, ${raw['meta']['usd']:.5f}, 0 LLM calls; edges returned per item {dict(sorted(short.items()))} (the stock recipe's cosine leg carries `sim_min_score` 0.6 and BM25 may return nothing, so three items return fewer than ten and one returns none, D-R85-20; {n_lines} lines; states over the ten {dict(n_states)}; over ranks 1 to 5 {dict(st_top5)}). "
           f"Every retrieved edge found in the persona's whole edge set with equal fact and temporal fields; RULE 1 states by `census.derive` over the whole graph, RULE 2 names, D-R85-10 ages; all ten rendered lines and states kept per item (Amendment 2 section 4). FR-Bank VIEW-UNTAGGED (D-R85-14): the recorded `top5_ids` re-rendered over the join's flags reproduce the recorded RETRIEVED block on {n_lock} of 323, the `lifecycle:` field then removed.\n\n"
           f"### AUX-R85-G10-REACH — the forbidding record among the retrieved edges (`census_forbidding.py`'s matcher, tau 0.80, on the ten edges), the 47 FULL obligations\n\n"
           f"Reached in ranks 1 to 5: **{reach['k5']} of 47**; in ranks 1 to 10: **{reach['k10']} of 47**; per state (n, k5, k10) {reach['per_state']}; by the join's state {reach['by_join_state']}; obligations with no marking event ({reach['unflagged']}) count as unreached. FR-Bank's recorded reach by identifier on the same 47: 26 / 34 (AUX-R113-Z3-REACH).\n\n"
           f"### AUX-R85-G10-TAGS — the store's non-active mark against the join's, the analogue of AUX-RESP-A1-TAGS\n\n"
           f"Over the forbidding records in view (ranks 1 to 5 of the 47 obligations that fire): tp {tv['tp']} / fp {tv['fp']} / fn {tv['fn']} / tn {tv['tn']}; recall {recl(tv) if recl(tv) is None else round(recl(tv), 4)}, precision {prec(tv) if prec(tv) is None else round(prec(tv), 4)}. Over every line of the 323 views (ranks 1 to 5, {sum(ta.values())} lines; the join's mark = the edge fires on any join event of the persona): tp {ta['tp']} / fp {ta['fp']} / fn {ta['fn']} / tn {ta['tn']}; precision {prec(ta) if prec(ta) is None else round(prec(ta), 4)}, recall {recl(ta) if recl(ta) is None else round(recl(ta), 4)}. FR-Bank's own marks on the recorded views (AUX-RESP-A1-TAGS): recall 0.7833 / precision 0.6714 in view; precision 0.1353 over all lines.\n\n"
           f"### AUX-R85-G10-PROMPTS — the untagged variant by one asserted `str.replace` (\"{PHRASE_OLD}\" -> \"{PHRASE_NEW}\") on `SYSTEM_RETRIEVED` and `USER_RETRIEVED`: sha256 `{prompts['SYSTEM_RETRIEVED_UNTAGGED'][:16]}…` / `{prompts['USER_RETRIEVED_UNTAGGED'][:16]}…`; the frozen `SYSTEM_RETRIEVED` `{prompts['SYSTEM_RETRIEVED'][:16]}…`, `USER_RETRIEVED` `{prompts['USER_RETRIEVED'][:16]}…`, `USER_HYBRID` `{prompts['USER_HYBRID'][:16]}…` (AUX-RESP-L2-PROMPTS).\n\n"
           f"### AUX-R85-G10-CHECK — the Step 5 checkpoint (registered for 22 September; performed 2026-09-17 by the executing session under the author's instruction of that day, not by the author): the format assertions hold on all 323 items (field order, the marker on category, the untagged line differing from the tagged in exactly the `lifecycle:` field, the FR-Bank re-render equal to the record); the seeded draw (seed 42) of five Graphiti and five FR-Bank untagged views is `g10/checkpoint_views.md` (Graphiti {', '.join(draw_g)}; FR-Bank {', '.join(draw_f)}), read by eye before Step 6 (the reading recorded below this key).\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
