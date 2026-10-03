# -*- coding: utf-8 -*-
"""cf2_names_counts_score.py -- ADDENDUM_CF2_NAMES_COUNTS (E2): the scorer. No model call. Reads the rows of cf2_names_counts.py, scores
every arm with the CF-2 conventions (cf2_reader_score), the paired differences against the recorded v2 rows and COUNTS minus NAMES,
the per-state P-N3 reading, P-N1 and P-N2; writes cf2/results/cf_scores_nc.json and appends section 12 to cf2/NUMBERS_CF2.md.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cf2_names_counts as N  # noqa: E402
import cf2_reader_score as R  # noqa: E402
import score_cf as S  # noqa: E402
from cf2_score import paired  # noqa: E402
from common_e1r import auroc  # noqa: E402

TOL = 0.05
REC = {"gpt-4.1-mini": ("MINI", 0.7167, {"RETRACTION": 0.5283, "EXPIRY": 0.5489}),
       "claude-haiku-4-5-20251001": ("H45", 0.7566, {"RETRACTION": 0.5433, "EXPIRY": 0.5794})}


def main():
    sys.stdout.reconfigure(encoding="utf-8"); N.setup()
    items, idx = R.cell(); look = R.lookup_v2(items, idx)
    y = np.array([it["y_nok"] for it in items], int); g = np.array([it["persona"] for it in items]); st = np.array([it["state"] for it in items])
    lock = json.load(io.open(N.LOCK, encoding="utf-8")); probes = json.load(io.open(N.PROBES, encoding="utf-8"))
    res = {"registration_sha256": N.REG_SHA, "frozen_at": N.FROZEN_AT, "build": lock["build"]["arms"], "probes": probes, "readers": {}, "when": dt.datetime.now().isoformat(timespec="seconds")}
    for lane, (code, gate, per_state_gate) in REC.items():
        rec = S.load_lane(code)
        v2 = np.array([rec[(it["item_id"], "INDEXED-V2")] for it in items], float)
        assert round(float(auroc(v2, y)), 4) == gate, ("GATE: the recorded v2 row", lane)
        for s_, gv in per_state_gate.items():
            assert round(float(auroc(v2[st == s_], y[st == s_])), 4) == gv, ("GATE per state", lane, s_)
        out = {"v2_recorded": gate, "arms": {}}; vecs = {}
        for arm in N.ARMS[lane]:
            r = R.score_lane(N.rows_path(lane), arm, items, look)
            assert r["missing_items"] == 0, (lane, arm, r["missing_items"])
            col, _ = R.collapse(N.rows_path(lane), arm)
            v = np.array([col[it["item_id"]] for it in items], float); vecs[arm] = v
            r["vs_v2"] = paired(v2, v, y, g); r["within_tolerance_of_v2"] = bool(abs(r["vs_v2"]["delta"]) <= TOL)
            r["per_state_vs_v2"] = {s_: paired(v2[st == s_], v[st == s_], y[st == s_], g[st == s_]) for s_ in R.STATES}
            out["arms"][arm] = r
        cm = paired(vecs["INDEXED-NAMES"], vecs["INDEXED-COUNTS"], y, g)
        cm["counts_below_names_reliably"] = bool(cm["delta"] < 0 and cm["both_exclude_zero"])
        out["counts_minus_names"] = cm
        if "INDEXED-NAMES-DASH" in vecs:
            out["dash_minus_names"] = paired(vecs["INDEXED-NAMES"], vecs["INDEXED-NAMES-DASH"], y, g)
        out["names_only_counted_identity"] = {s_: out["arms"]["INDEXED-NAMES"]["posthoc"]["per_state"][s_]["pn_vs_present"] for s_ in ("RETRACTION", "EXPIRY")}
        res["readers"][lane] = out
    n1 = {lane: res["readers"][lane]["arms"]["INDEXED-NAMES"]["within_tolerance_of_v2"] for lane in REC}
    n2 = {lane: res["readers"][lane]["counts_minus_names"]["counts_below_names_reliably"] for lane in REC}
    dn = {lane: res["readers"][lane]["arms"]["INDEXED-NAMES"]["vs_v2"]["delta"] for lane in REC}
    res["P-N1"] = {"holds": all(n1.values()), "per_reader": n1,
                   "text": ("P-N1 HOLDS: names only is within tolerance of the intact summary on the whole set for both readers (" + "; ".join(f"{l} {dn[l]:+.4f}" for l in REC) + ")."
                            if all(n1.values()) else "P-N1 FAILS on " + ", ".join(l for l, ok in n1.items() if not ok) + ": the names-only summary moves the whole-set AUROC by " + "; ".join(f"{dn[l]:+.4f}" for l, ok in n1.items() if not ok) + " from the intact summary, outside tolerance.")}
    res["P-N2"] = {"holds": all(n2.values()), "per_reader": n2,
                   "text": ("P-N2 HOLDS: counts only is reliably below names only on the whole set for both readers (" + "; ".join(f"{l} {R.fmt_paired(res['readers'][l]['counts_minus_names'])}" for l in REC) + ")."
                            if all(n2.values()) else "P-N2 FAILS on " + ", ".join(l for l, ok in n2.items() if not ok) + ": counts only is not reliably below names only (" + "; ".join(f"{l} {R.fmt_paired(res['readers'][l]['counts_minus_names'])}" for l, ok in n2.items() if not ok) + ").")}
    res["P-N3"] = {lane: {s_: {"recorded_v2": REC[lane][2][s_], "counts_only": res["readers"][lane]["arms"]["INDEXED-COUNTS"]["per_state"][s_]["auroc"],
                               "vs_v2": res["readers"][lane]["arms"]["INDEXED-COUNTS"]["per_state_vs_v2"][s_],
                               "within_tolerance": bool(abs(res["readers"][lane]["arms"]["INDEXED-COUNTS"]["per_state_vs_v2"][s_]["delta"]) <= TOL)} for s_ in ("RETRACTION", "EXPIRY")} for lane in REC}
    res["spend"] = {"mini": round(sum(json.loads(l).get("usd", 0.0) for l in io.open(N.rows_path("gpt-4.1-mini"), encoding="utf-8")), 4),
                    "h45": round(sum(json.loads(l).get("usd", 0.0) for l in io.open(N.rows_path("claude-haiku-4-5-20251001"), encoding="utf-8")), 4),
                    "probes": round(sum(sum(p["usd"]) for p in probes.values()), 4), "cap": N.CAP}
    io.open(N.C2.CF2 / "results" / "cf_scores_nc.json", "w", encoding="utf-8", newline="\n").write(json.dumps(res, indent=1, sort_keys=True, default=float) + "\n")
    L = [f"\n## 12. ADDENDUM_CF2_NAMES_COUNTS (E2, program R117): names against counts on the 444 (registered text sha256 `{N.REG_SHA[:16]}...`, frozen at `{N.FROZEN_AT}`; `tools/cf2_names_counts.py`, `tools/cf2_names_counts_score.py`; `rows/rows_MINI_nc.jsonl`, `rows/rows_H45_nc.jsonl`, `rows/batch_H45_nc.json`, `rows/lock_nc.json`, `build_nc.json`; `results/cf_scores_nc.json`; scored {dt.date.today().isoformat()})\n",
         "### AUX-CF2-NC-LOCK, AUX-CF2-NC-TOKENS\n",
         "Registration sha256 holds. Renderings, pure functions of the recorded v2 text, locks asserted on every version: " + "; ".join(f"`{a}` {v['prompt_tokens_mean']} prompt tokens mean (max {v['prompt_tokens_max']}), texts sha256 `{v['texts_sha256'][:16]}...`" for a, v in lock["build"]["arms"].items()) +
         ". D-NC-1: the registered lock wording (no digit outside the RECENCY block and the age sentence) is over-strict as written, because the name-block header reads max 15 per category and attribute names carry digits; the lock enforced is its intent: every kept line is a v2 line, byte-identical or with its overflow marker removed (the marker also when the 150-column wrap splits it), and no count line survives.\n",
         "### AUX-CF2-NC-MINI-NAMES, -MINI-NAMES-DASH, -MINI-COUNTS, -H45-NAMES, -H45-COUNTS\n",
         "| reader | arm | rows (not OK) | whole AUROC [persona CI] | minus recorded v2 (item; persona) | minus lookup (item; persona) | SUP | RET | EXP | distinct values |", "|---|---|---|---|---|---|---|---|---|---:|"]
    for lane, out in res["readers"].items():
        for arm, r in out["arms"].items():
            c = r["census"]; ps = r["per_state"]
            L.append(f"| {lane} | {arm} | {c['rows']} ({c['not_ok']}) | **{r['whole']:.4f}** [{r['whole_ci_persona']['ci_lo']:.4f}, {r['whole_ci_persona']['ci_hi']:.4f}] | {R.fmt_paired(r['vs_v2'])} | {R.fmt_paired(r['vs_lookup'])} | {ps['SUPERSESSION']['auroc']:.4f} | {ps['RETRACTION']['auroc']:.4f} | {ps['EXPIRY']['auroc']:.4f} | {r['distinct_values']} |")
        L.append(f"| {lane} | COUNTS minus NAMES | | | {R.fmt_paired(out['counts_minus_names'])} | | | | | |")
        if "dash_minus_names" in out:
            L.append(f"| {lane} | NAMES-DASH minus NAMES | | | {R.fmt_paired(out['dash_minus_names'])} | | | | | |")
    L += ["\n### AUX-CF2-NC-PERSTATE (counts only on the counted states against the reader's recorded v2 row; P-N3, descriptive)\n", "| reader | state | recorded v2 | counts only | difference (item; persona) | within tolerance |", "|---|---|---|---|---|---|"]
    for lane, d in res["P-N3"].items():
        for s_, v in d.items():
            L.append(f"| {lane} | {s_} | {v['recorded_v2']:.4f} | {v['counts_only']:.4f} | {R.fmt_paired(v['vs_v2'])} | {v['within_tolerance']} |")
    L += ["\nIdentity (disclosed at the freeze): under NAMES-ONLY the retraction and expiry PN and PRESENT versions are byte-identical, so PN versus PRESENT on those states is 0.5 by construction: " + "; ".join(f"{l} {res['readers'][l]['names_only_counted_identity']}" for l in REC) + ".\n",
          f"### AUX-CF2-NC-P-N1\n\n**{res['P-N1']['text']}**\n", f"### AUX-CF2-NC-P-N2\n\n**{res['P-N2']['text']}**\n",
          f"### AUX-CF2-NC-SPEND\n\nmini ${res['spend']['mini']:.4f} (1,332 calls), Haiku 4.5 ${res['spend']['h45']:.4f} (4,440 Batch calls), probes ${res['spend']['probes']:.4f}, against the cap of ${N.CAP:.0f}.\n"]
    with io.open(N.C2.CF2 / "NUMBERS_CF2.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
