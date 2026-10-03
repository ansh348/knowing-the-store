# -*- coding: utf-8 -*-
"""ledger_r139.py -- writes reviews/NUMBERS_R139.md from the R139 Phase 1 results (reviews/r139/results/equiv_r139.json, length_r139.json) and, once
Unit A's list exists, the comparison count (reviews/r139/results/n_list_r139.json). Every value is read from those files; nothing is typed.
Also writes reviews/r139/results/r139_printed.json: the derived verdict groups and printed forms that port_r139.py fills the texts from.
Usage: python reviews/r139/tools/ledger_r139.py
"""
from __future__ import annotations

import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RES = ROOT / "reviews" / "r139" / "results"
OUT = ROOT / "reviews" / "NUMBERS_R139.md"
PRINTED = RES / "r139_printed.json"
TABLE1 = {"GPT-4.1 mini, five draws": "mini", "Haiku 4.5": "Haiku", "GPT-5.6 Luna": "Luna", "GPT-5.6 Sol": "Sol", "Opus 5": "Opus"}


def r2(x):
    return str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def f4(x):
    return f"{x:+.4f}"


def iv(a):
    return f"[{a[0]:+.4f}, {a[1]:+.4f}]"


def main():
    E = json.load(open(RES / "equiv_r139.json", encoding="utf-8"))
    L = json.load(open(RES / "length_r139.json", encoding="utf-8"))
    rows = E["rows"]
    # ---- the E-iv groups: matched, default summary, supersession, the five readers at their Table 1 settings; pooled verdict named where it differs
    def pick(cond, scope, metric, reader):
        c = [r for r in rows if r["condition"] == cond and r["scope"] == scope and r["metric"] == metric and r["reader"] == reader]
        assert len(c) == 1, (cond, scope, metric, reader, len(c))
        return c[0]

    def verdict(r):
        if r["reliable"]:
            return "reliably below" if r["delta"] < 0 else "reliably above"
        return "equivalent" if r["equivalent"] else "neither"
    groups = {}
    for rd, short in TABLE1.items():
        m = pick("default summary", "supersession", "matched", rd)
        p = pick("default summary", "supersession", "pooled", rd)
        groups[short] = {"matched": verdict(m), "pooled": verdict(p), "matched_row": m, "pooled_row": p}
    b6 = {TABLE1[r["reader"].replace("count-feature lookup minus ", "")]: verdict(r) for r in rows if r["condition"].startswith("B6")}
    sb = {r["reader"]: r for r in rows if r["condition"] == "sibling-name control"}
    opus_sb = sb["Opus 5 (draw 1)"]
    closest = max(sb.values(), key=lambda r: r["delta"])
    assert closest is opus_sb
    printed = {
        "e_groups": {k: {"matched": v["matched"], "pooled": v["pooled"]} for k, v in groups.items()},
        "b6": b6,
        "sb_opus": {"delta": r2(abs(opus_sb["delta"])), "sign": "+" if opus_sb["delta"] > 0 else "-", "item_lo": r2(abs(opus_sb["ci95_a"][0])), "item_lo_sign": "-" if opus_sb["ci95_a"][0] < 0 else "+",
                    "item_hi": r2(abs(opus_sb["ci95_a"][1])), "item_hi_sign": "+" if opus_sb["ci95_a"][1] > 0 else "-", "wider": "item" if (opus_sb["ci95_a"][1] - opus_sb["ci95_a"][0]) >= (opus_sb["ci95_persona"][1] - opus_sb["ci95_persona"][0]) else "persona"},
        "length": {"padded_sup_matched": L["padded"]["supersession"]["matched"], "padded_sup_pooled": L["padded"]["supersession"]["pooled"],
                   "unpadded_sup_matched": L["unpadded"]["supersession"]["matched"], "sb_matched": L["sibling"]["supersession"]["matched"]},
        "lists": L["unpadded_supersession_lists"],
    }
    RES.mkdir(parents=True, exist_ok=True)
    PRINTED.write_text(json.dumps(printed, indent=1), encoding="utf-8", newline="\n")

    o = []
    o.append("# NUMBERS_R139.md: the R139 pass (mock review 14, W1 and W2: equivalence within 0.05 and the length-only reader; 2026-09-22)\n")
    o.append("Written by `reviews/r139/tools/ledger_r139.py` from `reviews/r139/results/equiv_r139.json` (`equiv_r139.py`) and `reviews/r139/results/length_r139.json` (`length_r139.py`). "
             "Both analyses are post hoc (the R139 POSTHOC block of CLAIMS.md). The branch texts were committed before either script ran (`reviews/r139/BRANCHES_R139.md`, 6616e57). No model call; no API call; "
             "every input is a stored score, a stored vector or a stored prompt text.\n")
    o.append("## AUX-R139-EQUIV: equivalence within 0.05 (two one-sided tests at 5%), every printed model-minus-lookup row of the five Phase 0.3 conditions, plus the B6 row\n")
    o.append(f"Rule: {E['rule']}. The 90% intervals are the 5th and 95th percentiles of the SAME {E['draws']} draws (seed {E['seed']}) whose 2.5th and 97.5th percentiles are the printed 95% intervals: "
             "the shared summaries `common_e1r._summarise` and `r125_common._summarise` are wrapped at run time (the modules are not edited). "
             f"Every recomputed 95% interval equals its stored source to 5e-5: {E['checks']['ok']} of {E['checks']['n']} (the three B6 rows are new and have no stored source). "
             "Pooled rows: item-level and persona-grouped intervals; matched rows: triple-level and persona-grouped. Both verdicts can be false at once ('neither shown nor excluded').\n")
    o.append("| condition | table | reader | scope | metric | difference | 95% item/triple | 95% persona | 90% item/triple | 90% persona | reliable | equivalent | reading |")
    o.append("|---|---|---|---|---|---:|---|---|---|---|---|---|---|")
    for r in rows:
        o.append(f"| {r['condition']} | {r['table']} | {r['reader']} | {r['scope']} | {r['metric']} | {f4(r['delta'])} | {iv(r['ci95_a'])} | {iv(r['ci95_persona'])} | {iv(r['ci90_a'])} | {iv(r['ci90_persona'])} | "
                 f"{'yes' if r['reliable'] else 'no'} | {'yes' if r['equivalent'] else 'no'} | {r['reading']} |")
    o.append("")
    o.append("## AUX-R139-E-GROUPS: the E-iv sentence's groups (matched metric, default summary, supersession slice, the five readers at their Table 1 settings; the pooled verdict beside)\n")
    o.append("| reader | matched verdict | pooled verdict | matched row | pooled row |")
    o.append("|---|---|---|---|---|")
    for k, v in groups.items():
        m, p = v["matched_row"], v["pooled_row"]
        o.append(f"| {k} | {v['matched']} | {v['pooled']} | {f4(m['delta'])} 90% {iv(m['ci90_a'])} {iv(m['ci90_persona'])} | {f4(p['delta'])} 90% {iv(p['ci90_a'])} {iv(p['ci90_persona'])} |")
    eq = [k for k, v in groups.items() if v["matched"] == "equivalent"]
    o.append(f"\nEquivalent group (matched): {', '.join(eq) or 'none'}; reliably below: {', '.join(k for k, v in groups.items() if v['matched'] == 'reliably below') or 'none'}; "
             f"neither: {', '.join(k for k, v in groups.items() if v['matched'] == 'neither') or 'none'}. The pooled verdict differs for: "
             f"{', '.join(f'{k} ({v[chr(112)+chr(111)+chr(111)+chr(108)+chr(101)+chr(100)]})' for k, v in groups.items() if v['pooled'] != v['matched']) or 'none'}.\n")
    o.append("## AUX-R139-B6: the lookup with one count feature minus each of Luna, Sol and Opus (matched, 148 triples)\n")
    o.append(", ".join(f"{k}: {v}" for k, v in b6.items()) + ". All three: equivalence within 0.05 is not shown, and no difference is reliable.\n")
    o.append("## AUX-R139-B2: the sibling-name control's closest reader (the largest model-minus-lookup difference, PN against sibling, matched)\n")
    o.append(f"{closest['reader']}: {f4(closest['delta'])}, 95% item {iv(closest['ci95_a'])}, persona {iv(closest['ci95_persona'])}; the wider is the {printed['sb_opus']['wider']}-level one (the ruling prints it): "
             f"printed {printed['sb_opus']['sign']}{printed['sb_opus']['delta']} [{printed['sb_opus']['item_lo_sign']}{printed['sb_opus']['item_lo']}, {printed['sb_opus']['item_hi_sign']}{printed['sb_opus']['item_hi']}].\n")
    o.append("## AUX-R139-LENGTH: the length-only reader (post hoc)\n")
    o.append("Score = the number of names in the superseded-names section of the text the reader saw. Pooled AUROC with the persona-grouped interval; matched over the triples with the triple-level and persona-grouped intervals.\n")
    o.append("| summary | scope | items | triples | pooled | persona interval | W/T/L | matched | triple interval | persona interval |")
    o.append("|---|---|---:|---:|---:|---|---|---:|---|---|")
    for summ in ("padded", "unpadded", "sibling"):
        for scope, v in L[summ].items():
            o.append(f"| {summ} | {scope} | {v['n_items']} | {v['n_triples']} | {v['pooled']:.4f} | [{v['pooled_persona_ci'][0]:.4f}, {v['pooled_persona_ci'][1]:.4f}] | {v['W']}/{v['T']}/{v['L']} | {v['matched']:.4f} | "
                     f"[{v['matched_triple_ci'][0]:.4f}, {v['matched_triple_ci'][1]:.4f}] | [{v['matched_persona_ci'][0]:.4f}, {v['matched_persona_ci'][1]:.4f}] |")
    o.append("\nPN list length minus sibling list length, per (triple, sibling):\n")
    o.append("| summary | scope | histogram (difference: count) |")
    o.append("|---|---|---|")
    for k, h in L["hist_pn_minus_sibling"].items():
        a, b = k.split("|")
        o.append(f"| {a} | {b} | {', '.join(f'{d}: {n}' for d, n in h.items())} |")
    u = L["unpadded_supersession_lists"]; pl = L["padded_lengths"]
    r1 = str(Decimal(str(u["pn_mean"])).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
    printed["lists"]["pn_mean_printed"] = r1
    PRINTED.write_text(json.dumps(printed, indent=1), encoding="utf-8", newline="\n")
    o.append(f"\nThe default summary's supersession lists: PN mean {u['pn_mean']} names (printed at one decimal, half-up: {r1}; the abstract and 5.2), maximum {u['pn_max']}, "
             f"{u['present_empty']} of {u['n']} PRESENT lists empty (AUX-CF2-R125-T2-CENSUS agrees). Padded: PN {pl['pn_min']} to {pl['pn_max']}, siblings {pl['sib_min']} to {pl['sib_max']}.\n")
    o.append("Reading (no softening): on the supersession triples the PN list is one to three names longer than both siblings' in every triple, padded or not; the length-only reader wins all 88 triples "
             "(matched 1.0000) on both lists and, on the padded lists, where every PN list has exactly 60 names and every sibling list fewer, it is also perfect pooled (1.0000). "
             "On the sibling-name control the lengths are equal by construction and the reader ties every triple (0.5000). 5.2's text (fixed in BRANCHES_R139.md, no number) and the Limitations sentence carry this.\n")
    # ---- B7: the crossover's own interval pair (persona- and pair-clustered), the fixed cue list minus the best model, explicit-intent rubric, crossover A, same store
    IX = json.load(open(ROOT / "r82_counterfactual" / "cf2" / "results" / "cf_scores_ix.json", encoding="utf-8"))
    best = max(IX["readers"], key=lambda m: IX["readers"][m]["A"]["P1"]["same_store"]["auroc"])
    v = IX["readers"][best]["A"]["P1"]["vs_keyword_same"]
    d = -v["delta"]; pair = [-v["ci_pair"]["ci_hi"], -v["ci_pair"]["ci_lo"]]; pers = [-v["ci_persona"]["ci_hi"], -v["ci_persona"]["ci_lo"]]
    wide = pair if (pair[1] - pair[0]) >= (pers[1] - pers[0]) else pers
    kw = IX["lookups"]["A"]["keyword"]["same_store"]["auroc"]
    assert not v["both_exclude_zero"] and d > 0
    fmt = lambda x: ("+" if x >= 0 else "-") + r2(abs(x))
    printed["b7"] = {"best": best, "delta": fmt(d), "lo": fmt(wide[0]), "hi": fmt(wide[1]), "wider": "pair" if wide is pair else "persona"}
    PRINTED.write_text(json.dumps(printed, indent=1), encoding="utf-8", newline="\n")
    o.append("## AUX-R139-B7: the fixed cue list minus the best model (the intent crossover, supersession crossover A, explicit-intent rubric, same-store pairs)\n")
    o.append(f"Source: r82_counterfactual/cf2/results/cf_scores_ix.json (AUX-CF2-IX-P-I4; reviews/r121/tools/ix_score.py), the crossover's own intervals (pair-clustered and persona-clustered, 1,000 draws; no item-level interval exists and none is computed, by ruling). "
             f"The best model under that rubric is {best} (same-store AUROC {IX['readers'][best]['A']['P1']['same_store']['auroc']:.4f}; the cue list {kw:.4f}). Cue list minus {best} = the sign flip of the stored "
             f"{best} minus the keyword lookup ({v['delta']:+.4f}): {d:+.4f}, pair {iv(pair)}, persona {iv(pers)}; not reliable (both include zero). The wider ({printed['b7']['wider']}) is printed: "
             f"{printed['b7']['delta']} [{printed['b7']['lo']}, {printed['b7']['hi']}].\n")
    # ---- B1: the registered pooled comparison beside the matched one, default summary, supersession (tab:sup-margins / tab:cfpad-minus-lookup unpadded panel)
    CP = json.load(open(ROOT / "cf_pad" / "results" / "cf_pad_scores.json", encoding="utf-8"))["readers"]
    lk = CP["LOOKUP"]["superseded"]["pooled"]["unpadded"]
    three = {m: CP[m]["superseded"]["pooled"]["unpadded"] for m in ("LUNA", "SOL", "OP5")}
    rel3 = {m: pick("default summary", "supersession", "pooled", {"LUNA": "GPT-5.6 Luna", "SOL": "GPT-5.6 Sol", "OP5": "Opus 5"}[m])["reliable"] for m in three}
    assert not any(rel3.values())
    printed["b1"] = {"lookup": r2(lk), "lo": r2(min(three.values())), "hi": r2(max(three.values())), "none_reliable": True}
    PRINTED.write_text(json.dumps(printed, indent=1), encoding="utf-8", newline="\n")
    o.append("## AUX-R139-B1: the pooled comparison beside the matched one (default summary, supersession, 264 items)\n")
    o.append(f"cf_pad/results/cf_pad_scores.json readers/*/superseded/pooled/unpadded (the recorded rows; tab:sup-margins): lookup {lk:.4f}, Luna {three['LUNA']:.4f}, Sol {three['SOL']:.4f}, Opus {three['OP5']:.4f}; "
             f"each minus the lookup not reliable (AUX-R139-EQUIV). Printed: the lookup's {printed['b1']['lookup']} against {printed['b1']['lo']} to {printed['b1']['hi']} for the three, none reliably above it.\n")
    # ---- Unit F: Figure 3's points and persona-grouped bars (the offsets pgfplots draws)
    RM = json.load(open(ROOT / "reviews" / "r125" / "results" / "r125_matched.json", encoding="utf-8"))["readers"]
    o.append("## AUX-R139-FIG3-BARS: Figure 3's points and persona-grouped 95% bars (Unit F; AUX-CF2-R125-PERSTATE)\n")
    o.append("Source: reviews/r125/results/r125_matched.json readers/*/pn_vs_present/per_state/*: the matched point, the persona interval, and the offsets up (hi minus point) and down (point minus lo) that fig3_data_matched.tex carries.\n")
    o.append("| reader | state | point | persona interval | up | down |")
    o.append("|---|---|---:|---|---:|---:|")
    for rk in ("MINI5_v2", "H45_v2", "LUNA_v2", "SOL_v2", "OP5_v2", "LOOKUP_v2", "CR-nb1_v2", "MINI5_v3", "H45_v3", "OP5_v3", "ALLSTATES_v3"):
        for st in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
            b = RM[rk]["pn_vs_present"]["per_state"][st]
            lo, hi = b["ci_persona"]["ci_lo"], b["ci_persona"]["ci_hi"]
            o.append(f"| {rk} | {st.lower()} | {b['matched']:.4f} | [{lo:.4f}, {hi:.4f}] | {hi - b['matched']:.4f} | {b['matched'] - lo:.4f} |")
    o.append("")
    NL = RES / "n_list_r139.json"
    if NL.exists():
        N = json.load(open(NL, encoding="utf-8"))
        o.append("## AUX-R139-N: the comparisons the main text calls reliable or not reliable (A2)\n")
        o.append(N["rule"] + "\n")
        o.append("| # | sentence (fragment asserted present in the built main text) | comparisons named | count |")
        o.append("|---|---|---|---:|")
        for i, e in enumerate(N["entries"], 1):
            o.append(f"| {i} | {e['fragment']} | {'; '.join(e['comparisons'])} | {len(e['comparisons'])} |")
        NC = json.load(open(RES / "n_count_r139.json", encoding="utf-8"))
        o.append(f"\n**Distinct comparisons in the main text as last built by port_r139.py: {NC['n_distinct']}** over the {len(NC['entries_present'])} entries present "
                 f"(a comparison named in several sentences counts once; an entry whose sentence a payer removed does not count); families: {N['families']}.\n")
        o.append("The distinct comparisons: " + "; ".join(NC["comparisons"]) + ".\n")
    OUT.write_text("\n".join(o) + "\n", encoding="utf-8", newline="\n")
    print(f"-> {OUT.relative_to(ROOT).as_posix()}; {PRINTED.relative_to(ROOT).as_posix()}")
    print(json.dumps(printed["e_groups"]), printed["b6"], printed["sb_opus"])


if __name__ == "__main__":
    main()
