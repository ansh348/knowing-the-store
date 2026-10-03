# -*- coding: utf-8 -*-
"""r125_t23_report.py -- Tasks 2 and 3: the tables and the ledger blocks, from reviews/r125/results/r125_t2_emptiness.json, r125_t3_frbank.json,
r125_t3_graphiti.json and r125_t3_sheet.json. No computation beyond formatting. NO MODEL CALL.

Writes reviews/r125/T2_T3_TABLES.md and the blocks R125-T2 / R125-T3 of section 15 of r82_counterfactual/cf2/NUMBERS_CF2.md (between markers; idempotent).
"""
from __future__ import annotations

import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import r125_common as C  # noqa: E402
from r125_common import STATES  # noqa: E402

OUT = C.R125 / "T2_T3_TABLES.md"
B2, E2 = "<!-- R125-T2 BEGIN (written by reviews/r125/tools/r125_t23_report.py; do not edit by hand) -->", "<!-- R125-T2 END -->"
B3, E3 = "<!-- R125-T3 BEGIN (written by reviews/r125/tools/r125_t23_report.py; do not edit by hand) -->", "<!-- R125-T3 END -->"


def f4(x):
    return "—" if x is None else f"{x:.4f}"


def sci(d):
    return f"[{d['ci_lo']:.4f}, {d['ci_hi']:.4f}]"


def dci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]"


def pr(p, a="ci_triple", b="ci_persona"):
    return f"{p['delta']:+.4f} {dci(p[a])} {dci(p[b])}{' **reliable**' if p['both_exclude_zero'] else ''}"


def prp(p):
    return pr(p, "item_ci", "persona_ci")


def t2_block(t2):
    L = ["### AUX-CF2-R125-T2-CENSUS — the superseded-names list per version (v2; the all-states lists under v3)", "",
         "| pairs | version | empty lists | length histogram | mean length |", "|---|---|---:|---|---:|"]
    for state in ("SUPERSESSION", "RETRACTION", "EXPIRY", "ALL"):
        c = t2["census_444"][state]
        for ver in ("PN", "PRESENT", "ABSENT"):
            d = c[f"v2_superseded_list/{ver}"]
            L.append(f"| {state} ({c['n_pairs']}) | {ver} | {d['empty']} | {d['length_hist']} | {d['mean_length']:.4f} |")
        L.append(f"| {state} ({c['n_pairs']}) | PN minus PRESENT | | {c['v2_superseded_list/PN_minus_PRESENT_length']} | pairs with PRESENT empty and PN not: {c['v2_pairs_where_PRESENT_empty_and_PN_nonempty']} |")
    L += ["", "Under the all-states summary (v3), the counted-state pairs' own lists:", "", "| pairs | section | version | empty | length histogram |", "|---|---|---|---:|---|"]
    for state, sec in (("RETRACTION", "retracted"), ("EXPIRY", "expired"), ("SUPERSESSION", "superseded")):
        c = t2["census_444"][state]
        for ver in ("PN", "PRESENT", "ABSENT"):
            d = c[f"v3_{sec}_list/{ver}"]
            L.append(f"| {state} | {sec} | {ver} | {d['empty']} | {d['length_hist']} |")
    L += ["", "### AUX-CF2-R125-T2-RANDOM — the random-token control per state and under the matched metric (444), per state on the 661", "",
          "| population | reader | pooled whole | pooled sup / ret / exp | matched PN vs PRESENT whole (W/T/L) | triple | persona | matched sup / ret / exp | matched PN vs ABSENT whole |", "|---|---|---:|---|---|---|---|---|---:|"]
    for tag in ("v2", "v3"):
        for who in ("random_token", "lookup"):
            b = t2["cf444"][tag][who]; m = b["matched_pn_vs_present"]
            ab = b.get("matched_pn_vs_absent", {}).get("whole", {}).get("matched")
            L.append(f"| 444 {tag} | {who.replace('_', ' ')} | {b['pooled']['whole']:.4f} | {' / '.join(f4(b['pooled']['per_state'][s]) for s in STATES)} | {m['whole']['matched']:.4f} ({m['whole']['W']}/{m['whole']['T']}/{m['whole']['L']}) | "
                     f"{sci(m['whole']['ci_triple'])} | {sci(m['whole']['ci_persona'])} | {' / '.join(f4(m['per_state'][s]['matched']) for s in STATES)} | {f4(ab)} |")
    for form in ("committed", "marker_free"):
        b = t2["obl661"][form]
        for who in ("random_token", "lookup"):
            d = b[who]
            L.append(f"| 661 {form} | {who.replace('_', ' ')} | {d['whole']:.4f} | {' / '.join(f4(d[s]['auroc']) for s in STATES)} (positives of one state against all 557 negatives) | not defined (no triples) | | | | |")
        L.append(f"| 661 {form} | census | empty lists {b['census']['items_with_empty_list']} of 661 ({b['census']['positives_with_empty_list']} positives); mean length {b['census']['mean_length']:.4f} | | | | | | |")
    L += ["", "### AUX-CF2-R125-T2-DIFF — the name lookup minus the random-token control, paired, both intervals, under both metrics", "",
          "| population | scope | pooled Δ (item; persona) | matched PN vs PRESENT Δ (triple; persona) | matched PN vs ABSENT Δ |", "|---|---|---|---|---|"]
    for tag in ("v2", "v3"):
        b = t2["cf444"][tag]
        L.append(f"| 444 {tag} | whole | {prp(b['lookup_minus_random_pooled']['whole'])} | {pr(b['lookup_minus_random_matched']['pn_vs_present']['whole'])} | {pr(b['lookup_minus_random_matched']['pn_vs_absent']['whole'])} |")
        for s in STATES:
            L.append(f"| 444 {tag} | {s.lower()} | {prp(b['lookup_minus_random_pooled']['per_state'][s])} | {pr(b['lookup_minus_random_matched']['pn_vs_present']['per_state'][s])} | {pr(b['lookup_minus_random_matched']['pn_vs_absent']['per_state'][s])} |")
    for form in ("committed", "marker_free"):
        b = t2["obl661"][form]["lookup_minus_random_pooled"]
        L.append(f"| 661 {form} | whole | {prp(b['whole'])} | not defined | |")
        for s in STATES:
            L.append(f"| 661 {form} | {s.lower()} | {prp(b[s])} | | |")
    return L


def t3_block(fr, gr, sh):
    L = ["### AUX-CF2-R125-T3-FRBANK — FR-Bank's 104 obligations relative to what the store retains (the join at three bars; the store's own marks)", "",
         f"Members stored for {fr['counts']['members_stored']} of 104 (by construction). Join-marked: " + "; ".join(f"{b}: {v['n']} {v['by_state']}" for b, v in fr["counts"]["join_marked"].items()) +
         f". Own-marked (FR-Bank's own non-active mark on a member): {fr['counts']['own_marked']['n']} {fr['counts']['own_marked']['by_state']}. Cross (join at 0.80, own): {fr['counts']['cross_join080_own']}.", "",
         "| stratum (positives; the 557 negatives unchanged) | n_pos | by state | mini GT | mini capped | mini lifted | Haiku GT | Haiku capped | Haiku lifted | lookup GT | lookup capped | lookup lifted | mini blind |", "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    keys = ["mini_true", "mini_capped", "mini_lifted", "haiku_true", "haiku_capped", "haiku_lifted", "lookup_true", "lookup_capped", "lookup_lifted", "mini_blind"]
    for name, b in fr["rescored"].items():
        L.append(f"| {name} | {b['n_pos']} | {b['by_state']} | " + " | ".join(f4(b["readers"][k]["auroc"]) for k in keys) + " |")
    L += ["", "The same rows with both single-arm intervals (item; persona) and, for the store-written rows, the paired store-written-minus-ground-truth difference (item; persona):", "",
          "| stratum | reader | AUROC | item interval | persona interval | minus ground truth |", "|---|---|---:|---|---|---|"]
    for name, b in fr["rescored"].items():
        for k in keys:
            d = b["readers"][k]
            L.append(f"| {name} | {d['label']} | {d['auroc']:.4f} | {sci(d['ci_item'])} | {sci(d['ci_persona'])} | {prp(d['minus_ground_truth']) if 'minus_ground_truth' in d else ''} |")
    L += ["", "### AUX-CF2-R125-T3-GRAPHITI — Graphiti's 47 full-store obligations relative to what the graph retains (the census join at three bars)", "",
          f"Recorded buckets at 0.80 reproduced from the edge export: {gr['recorded_buckets_080']}. Per band, the 34 join-marked superseded-or-expired obligations: " +
          "; ".join(f"{b}: {v['sup_or_exp_34']} (retained {v['retained']}; the 4 join-retracted, content retained {v['retracted_content_retained']})" for b, v in gr["counts"].items()) + ".", "",
          "| stratum (positives; the 276 negatives unchanged) | n_pos | by state | store-written capped | lifted | GT on Graphiti's schema | schema lifted | store's superseded-name lookup | whole-map lookup capped | lifted | five edges untagged | native tags | tagged + summary | FR-Bank top-5 untagged | FR-Bank GT summary | question only |",
          "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    gk = ["G10-BELIEVED", "G10-LIFTED", "G10-TRUEPROJ", "G10-TRUEPROJ-LIFTED", "NB6-emb-capped", "NB5-emb-capped", "NB5-emb-lifted", "G10-VIEW-UNTAGGED", "G10-VIEW-TAGGED", "G10-HYBRID", "FRB-VIEW-UNTAGGED", "TRUE", "BLIND"]
    for name, b in gr["rescored"].items():
        if b.get("n_pos", 0) == 0:
            L.append(f"| {name} | 0 | empty | " + " | ".join("—" for _ in gk) + " |"); continue
        L.append(f"| {name} | {b['n_pos']} | {b['by_state']} | " + " | ".join(f4(b["readers"][k]["auroc"]) for k in gk) + " |")
    L += ["", "The same rows with both single-arm intervals and the paired difference against the FR-Bank ground-truth summary on the same items (item; persona):", "",
          "| stratum | reader | AUROC | item interval | persona interval | minus ground-truth summary |", "|---|---|---:|---|---|---|"]
    for name, b in gr["rescored"].items():
        if b.get("n_pos", 0) == 0:
            continue
        for k in gk:
            d = b["readers"][k]
            L.append(f"| {name} | {k} | {d['auroc']:.4f} | {sci(d['ci_item'])} | {sci(d['ci_persona'])} | {prp(d['minus_true']) if 'minus_true' in d else ''} |")
    L += ["", "### AUX-CF2-R125-T3-SHEET — the author's read sheet", "",
          f"`{sh['xlsx']}` sha256 `{sh['xlsx_sha256']}`; key `{sh['key']}` sha256 `{sh['key_sha256']}`; {sh['n_rows']} rows = {sh['n_unmarked']} unmarked + {sh['n_controls']} controls (seed {sh['seed']}; pool {sh['control_pool']}); {sh['protection']}.", "",
          "| unmarked obligation | state | nearest stored record (within its store variant) | overlap | a member of the label's records | the store's own mark |", "|---|---|---|---:|---|---|"]
    for r in sh["unmarked_nearest"]:
        L.append(f"| {r['item_id']} | {r['state']} | {r['nearest_entry']} | {f4(r['cov'])} | {'yes' if r['entry_is_member'] else 'no'} | {r['own_mark']} |")
    return L


def main():
    t2 = C.jload(C.RESULTS / "r125_t2_emptiness.json"); fr = C.jload(C.RESULTS / "r125_t3_frbank.json"); gr = C.jload(C.RESULTS / "r125_t3_graphiti.json"); sh = C.jload(C.RESULTS / "r125_t3_sheet.json")
    b2 = t2_block(t2); b3 = t3_block(fr, gr, sh)
    OUT.write_text("\n".join(["# R125 Tasks 2 and 3 — tables (post hoc, offline, $0)", "", "## Task 2. How much of the lookup is list emptiness", ""] + b2 + ["", "## Task 3. Labels relative to what each backend retains", ""] + b3) + "\n", encoding="utf-8", newline="\n")
    text = C.LEDGER.read_text(encoding="utf-8")
    for bb, ee, body, title in ((B2, E2, b2, "## 15b. AUX-CF2-R125-T2 — how much of the lookup is list emptiness (program R125, Task 2; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_t2_emptiness.py`; `reviews/r125/results/r125_t2_emptiness.json`)"),
                                (B3, E3, b3, "## 15c. AUX-CF2-R125-T3 — labels relative to what each backend retains (program R125, Task 3; 2026-09-20; post hoc, offline, no model call; `reviews/r125/tools/r125_t3_frbank.py`, `r125_t3_graphiti.py`, `r125_t3_sheet.py`; `reviews/r125/results/r125_t3_*.json`; the Graphiti edges exported once from the local neo4j-r85 container to `reviews/r125/build/graphiti_edges_g10.json`)")):
        block = "\n".join([bb, "", title, ""] + body + ["", ee]) + "\n"
        if bb in text:
            text = re.sub(re.escape(bb) + r".*?" + re.escape(ee) + r"\n?", lambda m: block, text, flags=re.S)
        else:
            text = text.rstrip("\n") + "\n\n" + block
    C.LEDGER.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(C.ROOT)} and the R125-T2 / R125-T3 blocks of {C.LEDGER.relative_to(C.ROOT)}")


if __name__ == "__main__":
    main()
