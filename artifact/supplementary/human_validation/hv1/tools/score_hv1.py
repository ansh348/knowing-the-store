"""score_hv1.py -- program R119, registration sections 5 and 7: everything in one run.

    python score_hv1.py                      reads results/labels_A1.json (and labels_A2.json if present), writes results/scores_hv1.json,
                                             results/tables_hv1.md (the appendix tables), HELD_TEXTS_HV1.md (both branches), claims_r119_block.md,
                                             and the ledger keys AUX-HV1-PC1..PC4, -KAPPA, -SENS-UNSURE, -SENS-A2, -RECALL-148, -HAIKU-PRECISION,
                                             -Q4-SUBSTITUTE, -PB1, -PB-TRIPLE, -CONFUSION-B, -DISAGREE-B.
    --dry-run <dir>                          reads labels_*.json from <dir>, writes there, touches nothing else (synthetic fills; numbers meaningless).

Runs once: a second run on the real files is refused unless --rerun is given, which records a deviation. A1's labels are the reference;
UNSURE counts as not ASSERTS and not ABSTAINS in the primary analysis; blanks are excluded from denominators and counted.
"""
from __future__ import annotations

import collections
import io
import pathlib
import random
import sys

import hv1_common as H
from hv1_common import J, ROOT, jdump, wilson

FOUR = ["ASSERTS", "MENTIONS", "CLEAN", "ABSTAINS"]
THREE = ["PRESENT", "PN", "ABSENT"]


# ----------------------------------------------------------------------------- helpers
def kappa(pairs, cats):
    """Cohen's kappa, unweighted, over (a, b) label pairs restricted to cats."""
    pairs = [(a, b) for a, b in pairs if a in cats and b in cats]
    n = len(pairs)
    if n == 0:
        return None, 0, None
    po = sum(a == b for a, b in pairs) / n
    ca = collections.Counter(a for a, _ in pairs); cb = collections.Counter(b for _, b in pairs)
    pe = sum(ca[c] * cb[c] for c in cats) / (n * n)
    k = (po - pe) / (1 - pe) if pe < 1 else None
    return (round(k, 4) if k is not None else None), n, round(po, 4)


def rate(k, n):
    return round(k / n, 4) if n else None


def bootstrap_paired(diffs_by_persona, seed=H.SEED_BOOT, draws=10000):
    """diffs_by_persona: persona -> list of per-view differences (after - before). Item-level and persona-grouped percentile intervals."""
    items = [d for v in diffs_by_persona.values() for d in v]; personas = sorted(diffs_by_persona)
    rng = random.Random(seed); n = len(items)
    it = []
    for _ in range(draws):
        s = [items[rng.randrange(n)] for _ in range(n)]; it.append(sum(s) / n)
    rng = random.Random(seed); gp = []
    for _ in range(draws):
        ps = [personas[rng.randrange(len(personas))] for _ in range(len(personas))]
        pool = [d for p in ps for d in diffs_by_persona[p]]; gp.append(sum(pool) / len(pool))
    q = lambda xs, f: sorted(xs)[min(len(xs) - 1, max(0, int(round(f * (len(xs) - 1)))))]
    return {"item": [round(q(it, 0.025), 4), round(q(it, 0.975), 4)], "persona": [round(q(gp, 0.025), 4), round(q(gp, 0.975), 4)],
            "draws": draws, "seed": seed, "personas": len(personas)}


# ----------------------------------------------------------------------------- HV-A
def hva_analysis(key, LA, LB, unsure_as_asserts=False, who="A1"):
    """P-C1 to P-C4 and the auxiliaries for one annotator's labels (LA: row -> {uid, label, note}); LB unused here."""
    items = key["hva"]["items"]
    lab = {v["uid"]: v["label"] for v in LA.values()}
    def is_asserts(u):
        l = lab.get(u); return l == "ASSERTS" or (unsure_as_asserts and l == "UNSURE")
    def is_abstains(u):
        return lab.get(u) == "ABSTAINS"
    prim = [u for u, it in items.items() if it["block"] == "primary"]
    labelled = [u for u in prim if lab.get(u) is not None]
    blanks = len(prim) - len(labelled)
    changed = key["hva"]["population"]["changed_keys"]
    # P-C1 precision on the 45 flagged answers
    flagged = [u for u in prim if items[u]["flag_gold"]]
    fl = [u for u in flagged if lab.get(u) is not None]
    pc1_k = sum(is_asserts(u) for u in fl); pc1 = {"flagged": len(flagged), "labelled": len(fl), "asserts": pc1_k, "precision": rate(pc1_k, len(fl)),
                                                   "wilson": wilson(pc1_k, len(fl)) if fl else None,
                                                   "holds": (pc1_k / len(fl) >= 0.50) if fl else None,
                                                   "before": {"flagged": sum(items[u]["cond"] == "before" for u in fl), "asserts": sum(is_asserts(u) for u in fl if items[u]["cond"] == "before")},
                                                   "after": {"flagged": sum(items[u]["cond"] == "after" for u in fl), "asserts": sum(is_asserts(u) for u in fl if items[u]["cond"] == "after")}}
    # P-C2 over the 74 (both answers labelled)
    pairs = [(f"MINI|before|{k}", f"MINI|after|{k}") for k in changed]
    pl = [(b, a) for b, a in pairs if lab.get(b) is not None and lab.get(a) is not None]
    b_n = sum(is_asserts(b) for b, a in pl); a_n = sum(is_asserts(a) for b, a in pl)
    diffs = collections.defaultdict(list)
    for b, a in pl:
        diffs[items[b]["persona"]].append(int(is_asserts(a)) - int(is_asserts(b)))
    boot = bootstrap_paired(diffs) if pl else None
    pc2 = {"views": len(pl), "asserts_before": b_n, "asserts_after": a_n, "rate_before": rate(b_n, len(pl)), "rate_after": rate(a_n, len(pl)),
           "holds": (2 * a_n < b_n) if (pl and b_n > 0) else None, "unscorable": bool(pl) and b_n == 0,
           "paired_difference": rate(a_n - b_n, len(pl)), "bootstrap": boot,
           "identical_twins_same_label": sum(lab.get(b) == lab.get(a) for b, a in pl if items[b]["identical_twin"]),
           "identical_twins_labelled": sum(1 for b, a in pl if items[b]["identical_twin"])}
    # P-C3 recall over the 198 labelled; sensitivity over the 148
    def recall(us):
        ass = [u for u in us if is_asserts(u)]; fl_ = sum(items[u]["flag_gold"] for u in ass)
        return {"asserts": len(ass), "flagged_among_them": fl_, "recall": rate(fl_, len(ass)), "wilson": wilson(fl_, len(ass)) if ass else None,
                "holds": (fl_ / len(ass) >= 0.80) if ass else None, "unscorable": not ass, "rows": len(us)}
    pc3 = recall(labelled)
    rec148 = recall([u for u in labelled if items[u]["cond"] != "control"])
    # P-C4 abstentions over the 74
    b_abs = sum(is_abstains(b) for b, a in pl); a_abs = sum(is_abstains(a) for b, a in pl)
    pc4 = {"views": len(pl), "abstains_before": b_abs, "abstains_after": a_abs, "difference": a_abs - b_abs, "holds": (abs(a_abs - b_abs) <= 3) if pl else None,
           "bound": "3 of 74 (0.041 <= 0.05; 4 of 74 = 0.054)"}
    # Haiku block precision
    hk = [u for u, it in items.items() if it["block"] == "haiku"]; hl = [u for u in hk if lab.get(u) is not None]
    hk_k = sum(is_asserts(u) for u in hl)
    haiku = {"rows": len(hk), "labelled": len(hl), "asserts": hk_k, "precision": rate(hk_k, len(hl)), "wilson": wilson(hk_k, len(hl)) if hl else None,
             "before": {"labelled": sum(items[u]["cond"] == "before" for u in hl), "asserts": sum(is_asserts(u) for u in hl if items[u]["cond"] == "before")},
             "after": {"labelled": sum(items[u]["cond"] == "after" for u in hl), "asserts": sum(is_asserts(u) for u in hl if items[u]["cond"] == "after")}}
    dist = collections.Counter(lab.get(u) or "BLANK" for u in prim)
    return {"who": who, "unsure_as_asserts": unsure_as_asserts, "primary_rows": len(prim), "labelled": len(labelled), "blank": blanks,
            "label_distribution": dict(dist), "PC1": pc1, "PC2": pc2, "PC3": pc3, "RECALL_148": rec148, "PC4": pc4, "HAIKU": haiku}


def q4_substitute(key, LA):
    """Registration 5.4: the reported-detector (names a state and not flagged at 0.50) against 'label is MENTIONS or ABSTAINS', 198 primary rows."""
    import amend7_reported as A7
    items = key["hva"]["items"]; lab = {v["uid"]: v["label"] for v in LA.values()}
    tab = collections.Counter(); pairs = []
    for u, it in items.items():
        if it["block"] != "primary" or lab.get(u) in (None, "UNSURE"):
            continue
        m, _ = A7.reports_obligation(it["answer"], {"stale_use_tau_gold": it["flag_gold"]})
        h = lab[u] in ("MENTIONS", "ABSTAINS")
        tab[(bool(m), h)] += 1; pairs.append(("R" if m else "N", "R" if h else "N"))
    n = sum(tab.values()); agree = tab[(True, True)] + tab[(False, False)]
    k, _, po = kappa(pairs, ["R", "N"])
    return {"population": "substitute: the 198 primary HV-A rows (obligation items), UNSURE and blanks excluded", "rows": n,
            "table": {"machine_reported&human_MENTIONS_or_ABSTAINS": tab[(True, True)], "machine_reported&human_other": tab[(True, False)],
                      "machine_not&human_MENTIONS_or_ABSTAINS": tab[(False, True)], "machine_not&human_other": tab[(False, False)]},
            "agreement": rate(agree, n), "kappa": k, "rule_sha256": A7.RULE_SHA, "not_AUX_DS_A7_Q4": True}


def reliability(key, LA, LB):
    items = key["hva"]["items"]
    la = {v["uid"]: v["label"] for v in LA.values()}; lb = {v["uid"]: v["label"] for v in LB.values()}
    out = {}
    for block in ("primary", "haiku"):
        us = [u for u, it in items.items() if it["block"] == block]
        both = [(la.get(u), lb.get(u)) for u in us if la.get(u) is not None and lb.get(u) is not None]
        excl_unsure = sum(1 for a, b in both if a == "UNSURE" or b == "UNSURE")
        k, n, po = kappa(both, FOUR)
        conf = collections.Counter(both)
        out[block] = {"rows": len(us), "both_labelled": len(both), "excluded_unsure": excl_unsure, "n_kappa": n, "kappa": k, "raw_agreement": po,
                      "confusion_A1_x_A2": {f"{a}|{b}": c for (a, b), c in sorted(conf.items(), key=lambda x: (str(x[0][0]), str(x[0][1])))}}
    return out


# ----------------------------------------------------------------------------- HV-B
def hvb_analysis(key, LT):
    """LT: row -> {pair_id, version, label, group, a1_label, note}."""
    rows = list(LT.values()); lab_rows = [r for r in rows if r["a1_label"] is not None]
    agree = sum(r["a1_label"] == r["label"] for r in lab_rows)
    conf = collections.Counter((r["label"], r["a1_label"]) for r in lab_rows)
    by_pair = collections.defaultdict(list)
    for r in rows:
        by_pair[r["pair_id"]].append(r)
    full = [p for p, rs in by_pair.items() if all(r["a1_label"] is not None for r in rs)]
    trip_ok = sum(all(r["a1_label"] == r["label"] for r in by_pair[p]) for p in full)
    tri = {t["pair_id"]: t for t in key["hvb"]["triples"]}
    per_state = {}
    for s in ("SUPERSESSION", "RETRACTION", "EXPIRY"):
        rs = [r for r in lab_rows if tri[r["pair_id"]]["state"] == s]
        per_state[s] = {"labelled": len(rs), "agree": sum(r["a1_label"] == r["label"] for r in rs), "rate": rate(sum(r["a1_label"] == r["label"] for r in rs), len(rs))}
    disagreements = []
    for r in lab_rows:
        if r["a1_label"] != r["label"]:
            t = tri[r["pair_id"]]; v = next(v for v in t["versions"] if v["version"] == r["version"])
            disagreements.append({"group": r["group"], "pair_id": r["pair_id"], "state": t["state"], "intent": t["intent"], "question": t["question"], "today": t["today"],
                                  "records_shown": [f"{x['text']} (recorded {x['created']}" + (f"; event {x['event']}" if x["event"] else "") + ")" for x in v["records"]],
                                  "constructed": r["label"], "A1": r["a1_label"], "note": r["note"]})
    return {"versions": len(rows), "labelled": len(lab_rows), "blank": len(rows) - len(lab_rows), "agree": agree, "rate": rate(agree, len(lab_rows)),
            "wilson": wilson(agree, len(lab_rows)) if lab_rows else None, "PB1_bar": "at least 0.90; at 135 versions at least 122",
            "PB1_holds": (agree / len(lab_rows) >= 0.90) if lab_rows else None,
            "triples": {"n": len(by_pair), "fully_labelled": len(full), "all_three_right": trip_ok, "rate": rate(trip_ok, len(full)), "wilson": wilson(trip_ok, len(full)) if full else None},
            "per_state": per_state,
            "confusion_constructed_x_A1": {c: {a: conf[(c, a)] for a in THREE} for c in ["PRESENT", "ABSENT", "PRESENT-NEGATIVE"]},
            "label_map_note": "constructed PRESENT-NEGATIVE corresponds to the annotator's PN",
            "disagreements": disagreements}


# ----------------------------------------------------------------------------- tables and texts
def fmt_ci(ci):
    return f"[{ci[0]:.2f}, {ci[1]:.2f}]" if ci else "--"


def pct(x):
    return "--" if x is None else f"{x:.2f}"


def verdict(v):
    return "holds" if v is True else ("does not hold" if v is False else "unscorable")


def tables(S):
    A, U, B, R, Q, HB = S["hva_A1"], S["hva_A1_unsure_as_asserts"], S["hvb"], S["reliability"], S["q4_substitute"], S.get("hva_A2")
    L = ["# HV1 appendix tables (program R119; A1 the reference; UNSURE not ASSERTS unless stated)", ""]
    L += ["## HV-A: the predictions", "", "| prediction | statistic | value | Wilson 95% | verdict |", "|---|---|---|---|---|"]
    c1 = A["PC1"]; L.append(f"| P-C1 precision at 0.50 | ASSERTS among flagged | {c1['asserts']} of {c1['labelled']} = {pct(c1['precision'])} (before {c1['before']['asserts']}/{c1['before']['flagged']}, after {c1['after']['asserts']}/{c1['after']['flagged']}) | {fmt_ci(c1['wilson'])} | {verdict(c1['holds'])} (bar 0.50) |")
    c2 = A["PC2"]; bt = c2["bootstrap"]
    L.append(f"| P-C2 retag effect | ASSERTS before -> after, of {c2['views']} | {c2['asserts_before']} -> {c2['asserts_after']} ({pct(c2['rate_before'])} -> {pct(c2['rate_after'])}); paired difference {pct(c2['paired_difference'])}, item {fmt_ci(bt['item']) if bt else '--'}, persona {fmt_ci(bt['persona']) if bt else '--'} | -- | {verdict(c2['holds'])} (bar 2a < b) |")
    c3 = A["PC3"]; L.append(f"| P-C3 recall | flagged among A1's ASSERTS, {c3['rows']} rows | {c3['flagged_among_them']} of {c3['asserts']} = {pct(c3['recall'])} | {fmt_ci(c3['wilson'])} | {verdict(c3['holds'])} (bar 0.80) |")
    r1 = A["RECALL_148"]; L.append(f"| recall, the 148 alone | sensitivity | {r1['flagged_among_them']} of {r1['asserts']} = {pct(r1['recall'])} | {fmt_ci(r1['wilson'])} | -- |")
    c4 = A["PC4"]; L.append(f"| P-C4 abstentions | ABSTAINS before -> after, of {c4['views']} | {c4['abstains_before']} -> {c4['abstains_after']} (difference {c4['difference']:+d}) | -- | {verdict(c4['holds'])} (bar 3) |")
    L += ["", f"Label distribution over the {A['primary_rows']} primary rows: {A['label_distribution']}; blanks {A['blank']}. Identical-text twins given the same label: {c2['identical_twins_same_label']} of {c2['identical_twins_labelled']}.", ""]
    L += ["## HV-A: sensitivity rows", "", "| row | P-C1 | P-C2 | P-C3 | P-C4 |", "|---|---|---|---|---|"]
    def row(name, X):
        return (f"| {name} | {X['PC1']['asserts']}/{X['PC1']['labelled']} = {pct(X['PC1']['precision'])}, {verdict(X['PC1']['holds'])} "
                f"| {X['PC2']['asserts_before']} -> {X['PC2']['asserts_after']}, {verdict(X['PC2']['holds'])} "
                f"| {X['PC3']['flagged_among_them']}/{X['PC3']['asserts']} = {pct(X['PC3']['recall'])}, {verdict(X['PC3']['holds'])} "
                f"| {X['PC4']['abstains_before']} -> {X['PC4']['abstains_after']}, {verdict(X['PC4']['holds'])} |")
    L.append(row("primary (A1)", A)); L.append(row("(i) UNSURE as ASSERTS (A1)", U))
    L.append(row("(ii) A2's labels", HB) if HB else "| (ii) A2's labels | -- | -- | -- | -- |")
    hk = A["HAIKU"]
    L += ["", "## HV-A: the secondary block (Haiku 4.5, flagged answers on the 74 views; precision only)", "",
          f"Labelled {hk['labelled']} of {hk['rows']}; ASSERTS {hk['asserts']} = {pct(hk['precision'])} {fmt_ci(hk['wilson'])}; before {hk['before']['asserts']}/{hk['before']['labelled']}, after {hk['after']['asserts']}/{hk['after']['labelled']}.", ""]
    L += ["## HV-A: reliability (A1 vs A2, four-way, UNSURE excluded, no adjudication)", ""]
    if R:
        for block, X in R.items():
            L.append(f"- {block}: both labelled {X['both_labelled']} of {X['rows']}, excluded for UNSURE {X['excluded_unsure']}, kappa {X['kappa']} on {X['n_kappa']}, raw agreement {X['raw_agreement']}; confusion (A1|A2): {X['confusion_A1_x_A2']}")
    else:
        L.append("- A2 did not return; kappa prints as a dash.")
    L += ["", "## HV-A: the descriptive substitute for the Table 50 sentence (NOT AUX-DS-A7-Q4)", "",
          f"Population: {Q['population']}; rows {Q['rows']}; table {Q['table']}; agreement {Q['agreement']}; kappa {Q['kappa']}.", ""]
    L += ["## HV-B: the gold audit", "", f"Per version: {B['agree']} of {B['labelled']} = {pct(B['rate'])} {fmt_ci(B['wilson'])}; P-B1 (bar 0.90) {verdict(B['PB1_holds'])}; blanks {B['blank']}.",
          f"Per triple (all three right): {B['triples']['all_three_right']} of {B['triples']['fully_labelled']} = {pct(B['triples']['rate'])} {fmt_ci(B['triples']['wilson'])}.",
          f"Per state: {B['per_state']}.", "", "| constructed \\ A1 | PRESENT | PN | ABSENT |", "|---|---|---|---|"]
    for c, rowd in B["confusion_constructed_x_A1"].items():
        L.append(f"| {c} | {rowd['PRESENT']} | {rowd['PN']} | {rowd['ABSENT']} |")
    L += ["", f"### Disagreements, verbatim ({len(B['disagreements'])})", ""]
    for d in B["disagreements"]:
        L.append(f"- Group {d['group']} ({d['state']}, {d['intent']}; today {d['today']}). Q: {d['question']} Constructed **{d['constructed']}**, A1 **{d['A1']}**" + (f"; note: {d['note']}" if d["note"] else "") + ".")
        for x in d["records_shown"]:
            L.append(f"    - {x}")
    return "\n".join(L) + "\n"


def held_texts(S):
    A, B = S["hva_A1"], S["hvb"]
    c1, c2, c3, c4 = A["PC1"], A["PC2"], A["PC3"], A["PC4"]
    R = S["reliability"]; kp = R["primary"]["kappa"] if R else None
    arr = ("A non-author annotator labelled all items blind to policy, model and condition. An author labelled the same answers under the same blinding; "
           "we report the non-author's labels and their agreement.")
    hold_all = all(x is True for x in (c1["holds"], c2["holds"], c3["holds"], c4["holds"]))
    L = ["# HELD_TEXTS_HV1 -- the paper sentences in both branches (program R119); nothing lands without a ruling", "",
         f"Verdicts: P-C1 {verdict(c1['holds'])}, P-C2 {verdict(c2['holds'])}, P-C3 {verdict(c3['holds'])}, P-C4 {verdict(c4['holds'])}, P-B1 {verdict(B['PB1_holds'])}. "
         f"The branch that applies is **{'predictions hold' if hold_all else 'at least one prediction fails'}** for HV-A.", "",
         "## The arrangement (fixed wording, both branches)", "", arr, "",
         "## Section 9, the retag sentence", "",
         f"**Branch: holds.** Under a non-author's labels, GPT-4.1 mini gives the stale value as the answer in {c2['asserts_before']} of the {c2['views']} changed views before the "
         f"reference-assisted retag and in {c2['asserts_after']} after it (paired difference {pct(c2['paired_difference'])}, interval grouped by persona {fmt_ci(c2['bootstrap']['persona']) if c2['bootstrap'] else '--'}); "
         f"the detector's flags at $0.50$ have precision {pct(c1['precision'])} ({c1['asserts']} of {c1['labelled']}) and recall {pct(c3['recall'])} against those labels.", "",
         f"**Branch: fails.** Under a non-author's labels, the retag moves GPT-4.1 mini's stale answers from {c2['asserts_before']} to {c2['asserts_after']} of the {c2['views']} changed views, "
         f"{'less than' if c2['holds'] else 'not'} the halving the registration predicted; the detector's flags at $0.50$ have precision {pct(c1['precision'])} and recall {pct(c3['recall'])} against those labels, "
         f"so the detector-flagged counts in Table 4 are read with that error in mind.", "",
         "## The Table 4 footnote", "",
         f"**Holds.** A non-author labelled the retag's 148 answers and 50 controls (Appendix, HV1): precision {pct(c1['precision'])}, recall {pct(c3['recall'])}; the retag effect holds under human labels; abstentions moved by {c4['difference']:+d} of {c4['views']}.", "",
         f"**Fails.** A non-author labelled the retag's 148 answers and 50 controls (Appendix, HV1): precision {pct(c1['precision'])}, recall {pct(c3['recall'])}; "
         f"{'the retag effect does not hold under human labels' if c2['holds'] is False else 'the recall or precision bar was missed'}; abstentions moved by {c4['difference']:+d} of {c4['views']}.", "",
         "## The abstract's last clause", "",
         f"**Holds.** ..., and a non-author's labels confirm the detector (precision {pct(c1['precision'])}, recall {pct(c3['recall'])}) and the retag effect.", "",
         f"**Fails.** ..., and a non-author's labels put the detector's precision at {pct(c1['precision'])} and its recall at {pct(c3['recall'])}, so the retag effect is reported under those labels.", "",
         "## The Limitations sentence", "",
         f"**Holds.** The stale-answer detector was validated by one non-author on the retag's population and 50 controls (kappa with an author {kp}); the counterfactual labels agree with the same reader on "
         f"{B['agree']} of {B['labelled']} store versions.", "",
         f"**Fails.** The stale-answer detector's human validation on the retag's population gives precision {pct(c1['precision'])} and recall {pct(c3['recall'])} (kappa with an author {kp}); the detector-flagged counts "
         f"are upper or lower bounds accordingly; the counterfactual labels agree with the same reader on {B['agree']} of {B['labelled']} store versions.", "",
         "## The AI-use statement (one sentence to add, both branches)", "",
         "No language model took part in the human validation: the annotators attested that they used no AI tool, the workbooks were built and scored by scripts from recorded answers, and the practice key was written by the authors' assistant and discarded.", ""]
    return "\n".join(L)


def claims_block(S):
    A, B = S["hva_A1"], S["hvb"]
    return ("# CLAIMS.md block for program R119 (held; the author folds it in)\n\n"
            f"- HV1-PC1 | detector precision at 0.50 vs a non-author's ASSERTS | {A['PC1']['asserts']}/{A['PC1']['labelled']} = {A['PC1']['precision']} | AUX-HV1-PC1 | {verdict(A['PC1']['holds'])}\n"
            f"- HV1-PC2 | retag effect under human labels | {A['PC2']['asserts_before']} -> {A['PC2']['asserts_after']} of {A['PC2']['views']} | AUX-HV1-PC2 | {verdict(A['PC2']['holds'])}\n"
            f"- HV1-PC3 | detector recall | {A['PC3']['flagged_among_them']}/{A['PC3']['asserts']} = {A['PC3']['recall']} | AUX-HV1-PC3 | {verdict(A['PC3']['holds'])}\n"
            f"- HV1-PC4 | abstentions before vs after | {A['PC4']['abstains_before']} -> {A['PC4']['abstains_after']} | AUX-HV1-PC4 | {verdict(A['PC4']['holds'])}\n"
            f"- HV1-PB1 | counterfactual gold vs a non-author, per version | {B['agree']}/{B['labelled']} = {B['rate']} | AUX-HV1-PB1 | {verdict(B['PB1_holds'])}\n"
            f"- HV1-KAPPA | A1 vs A2, four-way | {S['reliability']['primary']['kappa'] if S['reliability'] else '--'} | AUX-HV1-KAPPA | descriptive\n"
            f"- HV1-Q4-SUB | reported-detector vs MENTIONS-or-ABSTAINS, substitute population | agreement {S['q4_substitute']['agreement']} | AUX-HV1-Q4-SUBSTITUTE | descriptive, not AUX-DS-A7-Q4\n")


# ----------------------------------------------------------------------------- main
def main():
    H.assert_registration()
    dry = None
    if "--dry-run" in sys.argv:
        dry = pathlib.Path(sys.argv[sys.argv.index("--dry-run") + 1])
    indir = dry if dry else H.RES_DIR
    key = J(H.KEY_DIR / "key_hv1.json"); assert key["meta"]["registration_sha256"] == H.REG_SHA
    la = J(indir / "labels_A1.json"); assert la["meta"]["annotator"] == "A1" and not la["meta"]["problems"]
    lb = J(indir / "labels_A2.json") if (indir / "labels_A2.json").exists() else None
    if lb:
        assert lb["meta"]["annotator"] == "A2" and not lb["meta"]["problems"]
    if not dry and (H.RES_DIR / "scores_hv1.json").exists():
        assert "--rerun" in sys.argv, "scores_hv1.json exists; the scorer runs once (registration 9.4) -- STOP"
        H.append_deviation("Registration section 9.4: score_hv1.py re-run on the validated files (--rerun); the previous scores_hv1.json is overwritten; reason recorded by the author.")
    LA, LT = la["labels"]["ANSWERS"], la["labels"]["TRIPLES"]
    LB = lb["labels"]["ANSWERS"] if lb else None
    S = {"meta": {"program": H.PROGRAM, "registration_sha256": H.REG_SHA, "key_sha256": H.sha_file(H.KEY_DIR / "key_hv1.json"),
                  "labels_A1_sha256": H.sha_file(indir / "labels_A1.json"), "labels_A2_sha256": H.sha_file(indir / "labels_A2.json") if lb else None,
                  "returned_A1_sha256": la["meta"]["returned_sha256"], "returned_A2_sha256": lb["meta"]["returned_sha256"] if lb else None,
                  "attestation_A1": la["attestation"], "attestation_A2": lb["attestation"] if lb else None, "when": H.now(), "dry_run": bool(dry)},
         "hva_A1": hva_analysis(key, LA, LB, False, "A1"), "hva_A1_unsure_as_asserts": hva_analysis(key, LA, LB, True, "A1"),
         "hva_A2": hva_analysis(key, LB, None, False, "A2") if LB else None,
         "reliability": reliability(key, LA, LB) if LB else None, "q4_substitute": q4_substitute(key, LA), "hvb": hvb_analysis(key, LT)}
    outdir = dry if dry else H.RES_DIR
    jdump(S, outdir / "scores_hv1.json")
    io.open(outdir / "tables_hv1.md", "w", encoding="utf-8", newline="\n").write(tables(S))
    io.open((outdir if dry else H.HV1) / "HELD_TEXTS_HV1.md", "w", encoding="utf-8", newline="\n").write(held_texts(S))
    io.open((outdir if dry else H.HV1) / "claims_r119_block.md", "w", encoding="utf-8", newline="\n").write(claims_block(S))
    A, B, U, R, Q = S["hva_A1"], S["hvb"], S["hva_A1_unsure_as_asserts"], S["reliability"], S["q4_substitute"]
    if not dry:
        H.append_ledger("AUX-HV1-PC1, -PC2, -PC3, -PC4, -RECALL-148 (Phase 3, score; A1 the reference)",
                        f"Rows labelled {A['labelled']} of {A['primary_rows']} (blank {A['blank']}); distribution {A['label_distribution']}.\n\n"
                        f"- **PC1** precision {A['PC1']['asserts']}/{A['PC1']['labelled']} = {A['PC1']['precision']} {A['PC1']['wilson']} -> {verdict(A['PC1']['holds'])}; before {A['PC1']['before']}, after {A['PC1']['after']}.\n"
                        f"- **PC2** ASSERTS {A['PC2']['asserts_before']} -> {A['PC2']['asserts_after']} of {A['PC2']['views']} -> {verdict(A['PC2']['holds'])}; paired difference {A['PC2']['paired_difference']}, bootstrap {A['PC2']['bootstrap']}; identical twins same label {A['PC2']['identical_twins_same_label']}/{A['PC2']['identical_twins_labelled']}.\n"
                        f"- **PC3** recall {A['PC3']['flagged_among_them']}/{A['PC3']['asserts']} = {A['PC3']['recall']} {A['PC3']['wilson']} over {A['PC3']['rows']} rows -> {verdict(A['PC3']['holds'])}.\n"
                        f"- **RECALL-148** {A['RECALL_148']['flagged_among_them']}/{A['RECALL_148']['asserts']} = {A['RECALL_148']['recall']} {A['RECALL_148']['wilson']}.\n"
                        f"- **PC4** ABSTAINS {A['PC4']['abstains_before']} -> {A['PC4']['abstains_after']} (difference {A['PC4']['difference']:+d}; bound 3) -> {verdict(A['PC4']['holds'])}.")
        H.append_ledger("AUX-HV1-SENS-UNSURE, AUX-HV1-SENS-A2, AUX-HV1-HAIKU-PRECISION, AUX-HV1-KAPPA (Phase 3, score)",
                        f"- **SENS-UNSURE** (UNSURE as ASSERTS): PC1 {U['PC1']['asserts']}/{U['PC1']['labelled']} {verdict(U['PC1']['holds'])}; PC2 {U['PC2']['asserts_before']} -> {U['PC2']['asserts_after']} {verdict(U['PC2']['holds'])}; "
                        f"PC3 {U['PC3']['flagged_among_them']}/{U['PC3']['asserts']} {verdict(U['PC3']['holds'])}; PC4 {U['PC4']['abstains_before']} -> {U['PC4']['abstains_after']} {verdict(U['PC4']['holds'])}.\n"
                        + (f"- **SENS-A2**: PC1 {S['hva_A2']['PC1']['asserts']}/{S['hva_A2']['PC1']['labelled']} {verdict(S['hva_A2']['PC1']['holds'])}; PC2 {S['hva_A2']['PC2']['asserts_before']} -> {S['hva_A2']['PC2']['asserts_after']} {verdict(S['hva_A2']['PC2']['holds'])}; "
                           f"PC3 {S['hva_A2']['PC3']['flagged_among_them']}/{S['hva_A2']['PC3']['asserts']} {verdict(S['hva_A2']['PC3']['holds'])}; PC4 {S['hva_A2']['PC4']['abstains_before']} -> {S['hva_A2']['PC4']['abstains_after']} {verdict(S['hva_A2']['PC4']['holds'])}.\n"
                           if S["hva_A2"] else "- **SENS-A2**: -- (no A2 return).\n")
                        + f"- **HAIKU-PRECISION**: {A['HAIKU']}.\n"
                        + (f"- **KAPPA**: {R}." if R else "- **KAPPA**: -- (no A2 return)."))
        H.append_ledger("AUX-HV1-Q4-SUBSTITUTE (Phase 3, score; descriptive; NOT AUX-DS-A7-Q4)", f"{Q}")
        H.append_ledger("AUX-HV1-PB1, AUX-HV1-PB-TRIPLE, AUX-HV1-CONFUSION-B, AUX-HV1-DISAGREE-B (Phase 3, score)",
                        f"- **PB1** per version {B['agree']}/{B['labelled']} = {B['rate']} {B['wilson']} (blank {B['blank']}) -> {verdict(B['PB1_holds'])} (bar 0.90, 122 of 135).\n"
                        f"- **PB-TRIPLE** {B['triples']}.\n- per state {B['per_state']}.\n- **CONFUSION-B** (constructed x A1) {B['confusion_constructed_x_A1']}.\n"
                        f"- **DISAGREE-B**: {len(B['disagreements'])} versions, printed verbatim in `results/tables_hv1.md`.")
    print(f"{'[dry-run] ' if dry else ''}scored: PC1 {verdict(A['PC1']['holds'])} ({A['PC1']['precision']}), PC2 {verdict(A['PC2']['holds'])} ({A['PC2']['asserts_before']}->{A['PC2']['asserts_after']}), "
          f"PC3 {verdict(A['PC3']['holds'])} ({A['PC3']['recall']}), PC4 {verdict(A['PC4']['holds'])} ({A['PC4']['difference']:+d}), PB1 {verdict(B['PB1_holds'])} ({B['agree']}/{B['labelled']}); "
          f"kappa {R['primary']['kappa'] if R else '--'}; outputs in {outdir.relative_to(ROOT) if outdir.is_relative_to(ROOT) else outdir}")


if __name__ == "__main__":
    main()
