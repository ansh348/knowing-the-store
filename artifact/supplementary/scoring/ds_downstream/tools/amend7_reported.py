# -*- coding: utf-8 -*-
"""amend7_reported.py -- ADDENDUM_DS Amendment 7 (registrations/ADDENDUM_DS_AMENDMENT_7.md, frozen at 12c63f9; registered text
sha256 6566bf09... over the bytes above the marker): an obligation-reported detector scored on every recorded answer under every
policy and amendment, its agreement with the annotators' Q4 once labeled, and a composite per policy over the 661.
NO MODEL CALL. $0. Descriptive: no prediction, no bar, no verdict. Written from amend5_tagdup.py (its lineage checks and
ledger discipline); the committed detector is run_ds.score_answer through amend2_lit.score_rows, unchanged.

Subcommands:
  lock     registration sha256 (frozen bytes); the word list and its sha256; the rows files and their counts; the reproduction
           gates (the Amendment 4 and 5 rows reproduce AUX-DS-A4-STAGE2 / AUX-DS-A5-STAGE2 stale counts) -> run/lock_amend7.json;
           NUMBERS_DS.md section 13 opened with AUX-DS-A7-REG and AUX-DS-A7-RULE
  score    the detector on every recorded answer; the split; the composite per policy over the 661 (absent abstention in two
           readings: the recorded coverage-gate decision; the answered abstention where Amendment 6 rows exist); Q4 agreement
           a dash until the sheet is labeled (reviews/v18/annotator_agreement.py carries the detector's Q4 counterpart)
           -> run/scores_amend7.json; NUMBERS_DS.md section 13 (AUX-DS-A7-*)
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import io
import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import ds_common as DC                                                       # noqa: E402
from ds_common import ROOT, DS, RUN, J, jdump, POLICIES                     # noqa: E402
import run_ds as RD                                                          # noqa: E402
import amend2_lit as A2                                                      # noqa: E402
import amend4_header as A4                                                   # noqa: E402

REG = ROOT / "registrations" / "ADDENDUM_DS_AMENDMENT_7.md"
REG_SHA = "6566bf097f41ccd289c888f4c467d64786eea3230b7f23f279377b6c8a1a7201"
FROZEN_AT = "12c63f9"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
LEDGER = DS / "NUMBERS_DS.md"

# The closed list of section A7.2, not revised after the sheet is read. "previous" / "former" count only beside a state word.
STATE_WORDS = ("superseded", "retracted", "expired", "no longer", "not current", "outdated", "out of date", "cancelled", "canceled",
               "replaced", "withdrawn", "discontinued", "past")
CONDITIONAL_WORDS = ("previous", "previously", "former", "formerly")
STATE_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in STATE_WORDS) + r")\b|\b(is|was|has|had) passed\b", re.IGNORECASE)
COND_RE = re.compile(r"\b(" + "|".join(CONDITIONAL_WORDS) + r")\b", re.IGNORECASE)
RULE_SHA = hashlib.sha256(("|".join(STATE_WORDS) + "||" + "|".join(CONDITIONAL_WORDS) + "||" + STATE_RE.pattern).encode("utf-8")).hexdigest()

# every recorded answer file: (variant, answerer, path[s]); the D.4 mini rows are rows_ds.jsonl plus the LOOKUP-LIT views of amend2
FILES = [
    ("D4", "MINI", [RUN / "rows_ds.jsonl", RUN / "rows_ds_amend2.jsonl"]),
    ("A1-allstates-gate", "MINI", [RUN / "rows_ds_amend1.jsonl"]),
    ("D4", "H45", [RUN / "rows_ds_amend2_h45.jsonl"]),
    ("A3-instruction", "MINI", [RUN / "rows_ds_amend3_mini.jsonl"]),
    ("A3-instruction", "H45", [RUN / "rows_ds_amend3_h45.jsonl"]),
    ("A4-header", "MINI", [RUN / "rows_ds_amend4_mini.jsonl"]),
    ("A4-header", "H45", [RUN / "rows_ds_amend4_h45.jsonl"]),
    ("A5-duplicates-tagged", "MINI", [RUN / "rows_ds_amend5_merged_mini.jsonl"]),
    ("A5-duplicates-tagged", "H45", [RUN / "rows_ds_amend5_merged_h45.jsonl"]),
]


def registration_ok():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    return i > 0 and hashlib.sha256(b[:i]).hexdigest() == REG_SHA


def names_state(answer):
    """Condition (a): the answer names the lifecycle state (a state word on a word boundary; previous / former only in a sentence
    that also carries a state word)."""
    a = answer or ""
    if STATE_RE.search(a):
        return True
    for sent in A4.SENT_RE.split(a):
        if COND_RE.search(sent) and STATE_RE.search(sent):
            return True
    return False


def reports_obligation(answer, scored):
    """Condition (a) and (b): names the state, and the committed detector's stale flag at TAU_GOLD is false. For an expiry
    obligation (unscorable by the detector) condition (a) alone, returned with the flag 'a_only'."""
    a = names_state(answer)
    if scored.get("expiry_unscorable"):
        return a, "a_only"
    return bool(a and not scored.get("stale_use_tau_gold")), "a_and_b"


def load_rows(paths):
    rows = {}
    for p in paths:
        if not p.exists():
            continue
        for l in io.open(p, encoding="utf-8"):
            r = json.loads(l); rows.setdefault(r["key"], r)
    return rows


def score_file(paths, sub, rec, byid):
    """rows (deduped by key), per-row committed detector output, per-row reported flag."""
    import tempfile
    rows = load_rows(paths)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8")
    for r in rows.values():
        tmp.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.close()
    rows2, per, _ = A2.score_rows(tmp.name, sub, rec)
    rep = {}
    for k, r in rows.items():
        p = per[k]
        if r["label"] != "PRESENT-NEGATIVE" or not p.get("scored"):
            continue
        p2 = dict(p); p2["expiry_unscorable"] = byid[r["item_id"]]["state"] == "exp"
        flag, mode = reports_obligation(r["answer"], p2)
        rep[k] = {"reported": flag, "mode": mode, "names_state": names_state(r["answer"]), "stale_gold": bool(p.get("stale_use_tau_gold")),
                  "successor_use": p.get("successor_use"), "abstains": A4.is_abst(r["answer"]), "state": byid[r["item_id"]]["state"]}
    return rows, per, rep


def cmd_lock():
    assert registration_ok(), "ADDENDUM_DS_AMENDMENT_7.md frozen bytes sha256 != 6566bf09 -- STOP"
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    counts = {}
    for variant, code, paths in FILES:
        rows = load_rows(paths); counts[f"{variant}|{code}"] = {"rows": len(rows), "files": [str(p.relative_to(ROOT)) for p in paths if p.exists()]}
    # reproduction gates: the Amendment 4 and 5 rows reproduce the ledgered stale counts at TAU_GOLD per policy (pn_all)
    gates = {}
    for tag, key_s, paths in (("A4", "scores_amend4.json", {"MINI": [RUN / "rows_ds_amend4_mini.jsonl"], "H45": [RUN / "rows_ds_amend4_h45.jsonl"]}),
                              ("A5", "scores_amend5.json", {"MINI": [RUN / "rows_ds_amend5_merged_mini.jsonl"], "H45": [RUN / "rows_ds_amend5_merged_h45.jsonl"]})):
        sc = J(RUN / key_s)
        for code, pp in paths.items():
            rows, per, _ = score_file(pp, sub, rec, byid)
            got = {p: sum(1 for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and per[k].get("scored") and per[k]["stale_use_tau_gold"]) for p in POLICIES}
            want = {p: sc["stage2"][code][p]["pn_all"]["stale_use_tau_gold"] for p in POLICIES}
            gates[f"{tag}|{code}"] = {"got": got, "want": want, "ok": got == want}
    ok = all(g["ok"] for g in gates.values())
    out = {"registration": str(REG.relative_to(ROOT)), "registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "rule": {"state_words": list(STATE_WORDS), "conditional_words": list(CONDITIONAL_WORDS), "regex": STATE_RE.pattern, "sha256": RULE_SHA},
           "files": counts, "gates": gates, "gates_ok": ok, "when": dt.datetime.now().isoformat(timespec="seconds")}
    jdump(out, RUN / "lock_amend7.json"); print(json.dumps({k: v for k, v in out.items() if k != "gates"}, indent=1)); print("gates ok:", ok, {k: g["ok"] for k, g in gates.items()})
    if not ok:
        sys.exit("STOP: the committed detector does not reproduce the ledgered stale counts on the recorded rows")
    txt = LEDGER.read_text(encoding="utf-8")
    if "AUX-DS-A7-REG" not in txt:
        with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
            f.write(f"\n## 13. DS Amendment 7: an obligation-reported detector and a composite per policy (registrations/ADDENDUM_DS_AMENDMENT_7.md; descriptive; $0)\n\n"
                    f"### AUX-DS-A7-REG\n\nRegistered text sha256 **`{REG_SHA}`** (the bytes above the marker line), frozen at `{FROZEN_AT}` on 2026-09-15, recorded here before any scoring. Descriptive: no prediction, no bar, no verdict; no model call. Runner `tools/amend7_reported.py`.\n\n"
                    f"### AUX-DS-A7-RULE\n\nAn answer reports the obligation iff (a) it names the lifecycle state, a word-boundary match on the closed list {', '.join(STATE_WORDS)} (or 'is / was / has / had passed'), with previous / previously / former / formerly counting only in a sentence that also carries one of those, and (b) the committed detector's stale flag at TAU_GOLD on the whole answer is false; on an expiry obligation (b) is unscorable and (a) alone prints, marked. Word list and pattern sha256 `{RULE_SHA}`; not revised after the sheet is read.\n")
    print("section 13 opened with AUX-DS-A7-REG and AUX-DS-A7-RULE")


def wilson(k, n):
    return A4.wilson(k, n)


def cmd_score():
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok() and J(RUN / "lock_amend7.json")["gates_ok"], "STOP: lock first"
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    st1 = J(DS / "stage1.json")["per_item"]
    n_lic = sum(1 for it in sub if it["label"] == "PRESENT"); n_obl = sum(1 for it in sub if it["label"] == "PRESENT-NEGATIVE"); n_abs = sum(1 for it in sub if it["label"] == "ABSENT")
    absent_ids = [it["item_id"] for it in sub if it["label"] == "ABSENT"]
    # Amendment 6 rows, if present: the answered abstention on absent items per depth policy (the second reading)
    a6 = {}
    for code, p in (("MINI", RUN / "rows_ds_amend6_mini.jsonl"), ("H45", RUN / "rows_ds_amend6_h45.jsonl")):
        if p.exists():
            a6[code] = [json.loads(l) for l in io.open(p, encoding="utf-8")]
    S = {"registration_sha256": REG_SHA, "frozen_at": FROZEN_AT, "rule_sha256": RULE_SHA, "n": {"licensed": n_lic, "obligations": n_obl, "absent": n_abs}, "variants": {}, "q4": "dash: the second annotator's sheet is not yet labeled (reviews/v18/annotator_agreement.py carries the detector's Q4 counterpart)"}
    for variant, code, paths in FILES:
        rows, per, rep = score_file(paths, sub, rec, byid)
        V = {"rows": len(rows), "policies": {}}
        pols = sorted({p for r in rows.values() for p in r["policies"]}, key=lambda p: (POLICIES.index(p) if p in POLICIES else 99, p))
        for p in pols:
            keys = [k for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep]
            reached = len(keys); reported = sum(1 for k in keys if rep[k]["reported"])
            sc_keys = [k for k in keys if rep[k]["mode"] == "a_and_b"]; exp_keys = [k for k in keys if rep[k]["mode"] == "a_only"]
            split = {"reported_and_abstaining": sum(1 for k in keys if rep[k]["reported"] and rep[k]["abstains"]),
                     "reported_and_answering": sum(1 for k in keys if rep[k]["reported"] and not rep[k]["abstains"]),
                     "reported_with_successor": sum(1 for k in keys if rep[k]["reported"] and rep[k]["successor_use"]),
                     "names_state_but_gives_stale": sum(1 for k in sc_keys if rep[k]["names_state"] and rep[k]["stale_gold"]),
                     "stale_without_naming": sum(1 for k in sc_keys if rep[k]["stale_gold"] and not rep[k]["names_state"]),
                     "neither": sum(1 for k in keys if not rep[k]["reported"] and not rep[k]["stale_gold"])}
            lic_keys = [k for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT" and per[k].get("scored")]
            lic_correct = sum(1 for k in lic_keys if per[k]["correct"])
            abs_gate = sum(1 for i in absent_ids if st1[i].get(p, {}).get("abstain"))
            comp = {"licensed_correct": lic_correct, "of_licensed": n_lic, "obligation_reported": reported, "of_obligations": n_obl,
                    "absent_abstained_gate": abs_gate, "of_absent": n_abs, "composite_gate_reading": lic_correct + reported + abs_gate, "of_661": 661}
            V["policies"][p] = {"reached_obligations": reached, "reported": reported, "rate": (reported / reached) if reached else None, "wilson": wilson(reported, reached) if reached else None,
                                "scorable_reached": len(sc_keys), "reported_scorable": sum(1 for k in sc_keys if rep[k]["reported"]), "expiry_a_only_reached": len(exp_keys), "expiry_a_only_reported": sum(1 for k in exp_keys if rep[k]["reported"]),
                                "stale_gold_beside": sum(1 for k in sc_keys if rep[k]["stale_gold"]), "split": split, "composite": comp}
        S["variants"][f"{variant}|{code}"] = V
    # the second absent reading, from Amendment 6 rows where they exist (per depth policy)
    if a6:
        S["absent_answered_abstention_amend6"] = {code: collections.Counter() for code in a6}
        for code, rows6 in a6.items():
            cnt = collections.Counter(); n = collections.Counter()
            for r in rows6:
                if r.get("label") == "ABSENT" and r.get("status") == "OK":
                    for p in r["policies"]:
                        n[p] += 1; cnt[p] += int(A4.is_abst(r["answer"]))
            S["absent_answered_abstention_amend6"][code] = {p: {"abstained": cnt[p], "answered": n[p]} for p in n}
    S["when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend7.json")
    txt = ledger_text(S)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


def ledger_text(S):
    L = [f"\n### AUX-DS-A7-REPORTED, AUX-DS-A7-SPLIT, AUX-DS-A7-COMPOSITE (appended by `tools/amend7_reported.py score`; rule sha256 `{S['rule_sha256'][:16]}...`)\n\n",
         "Obligation reported per answerer, prompt variant and policy: the count and rate over the reached and answered obligations (all states; the expiry obligations by condition (a) alone), Wilson interval; beside it the registered stale flag at TAU_GOLD on the scorable set; the split; and the composite over the 661 in the coverage-gate reading (a licensed item counts if correct at 0.50; an obligation if reached, answered and reported; an absent item if the registered coverage gate abstained on it under that policy: zero under ALWAYS, which has no gate, and 383 of 383 under ORACLE, whose gate is the label itself, a settled reading recorded as D-DS-A7-1 against section A7.4's 'zero under ALWAYS and ORACLE').\n\n",
         "| variant | answerer | policy | reached | reported (rate; Wilson) | of which expiry by (a) alone | stale at 0.50 (scorable) | reported and abstaining / answering / with successor | names the state but gives the stale value | stale without naming | neither | composite: licensed correct + reported + absent abstained = of 661 |\n|---|---|---|---:|---|---|---:|---|---:|---:|---:|---|\n"]
    for vk, V in S["variants"].items():
        variant, code = vk.split("|")
        for p, d in V["policies"].items():
            sp, c = d["split"], d["composite"]
            L.append(f"| {variant} | {code} | {p} | {d['reached_obligations']} | {d['reported']} ({d['rate']:.4f}; {[round(x, 4) for x in d['wilson']]}) | {d['expiry_a_only_reported']} / {d['expiry_a_only_reached']} | {d['stale_gold_beside']} / {d['scorable_reached']} | {sp['reported_and_abstaining']} / {sp['reported_and_answering']} / {sp['reported_with_successor']} | {sp['names_state_but_gives_stale']} | {sp['stale_without_naming']} | {sp['neither']} | {c['licensed_correct']} of {c['of_licensed']} + {c['obligation_reported']} of {c['of_obligations']} + {c['absent_abstained_gate']} of {c['of_absent']} = **{c['composite_gate_reading']}** of 661 |\n"
                     if d["reached_obligations"] else f"| {variant} | {code} | {p} | 0 | | | | | | | | |\n")
    if "absent_answered_abstention_amend6" in S:
        L.append("\nThe second absent reading (Amendment 6, the answered abstention per depth policy): " + json.dumps(S["absent_answered_abstention_amend6"]) + "\n")
    L.append(f"\n### AUX-DS-A7-Q4: {S['q4']}\n")
    return "".join(L)


# ------------------------------------------------------------------ the composite's paired difference (the author's addition of 2026-09-15)
def composite_items(rows, per, rep, sub, st1, p):
    """Per-item composite indicator over the 661 under policy p: a licensed item correct at 0.50, an obligation reached, answered and
    reported, an absent item on which the recorded coverage rule abstained (the oracle's rule is the label itself, D-DS-A7-1)."""
    ind = {}
    lic = {r["item_id"]: bool(per[k]["correct"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT" and per[k].get("scored")}
    obl = {r["item_id"]: bool(rep[k]["reported"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep}
    for it in sub:
        i = it["item_id"]
        if it["label"] == "PRESENT":
            ind[i] = int(lic.get(i, False))
        elif it["label"] == "PRESENT-NEGATIVE":
            ind[i] = int(obl.get(i, False))
        else:
            ind[i] = int(bool(st1[i].get(p, {}).get("abstain")))
    return ind


def cmd_composite_diff():
    """AUX-DS-A7-COMPOSITE-DIFF: the composite under each gated rule minus under retrieval alone, per answerer and prompt variant, as a paired
    difference of rates over the 661 with the item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42); the oracle is
    excluded from every comparison (its absent component is the label itself, D-DS-A7-1). Descriptive; ordered by the author on
    2026-09-15 after the registration; not a registered analysis."""
    import numpy as np
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok() and J(RUN / "lock_amend7.json")["gates_ok"], "STOP: lock first"
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    st1 = J(DS / "stage1.json")["per_item"]
    ids = [it["item_id"] for it in sub]; pers = np.array([byid[i]["persona"] for i in ids]); groups = np.unique(pers); by = {u: np.flatnonzero(pers == u) for u in groups}
    N_BOOT, SEED = 10000, 42
    out = {}
    base = {}
    for variant, code, paths in FILES:
        if variant not in ("A4-header", "A5-duplicates-tagged"):
            continue
        rows, per, rep = score_file(paths, sub, rec, byid)
        inds = {p: composite_items(rows, per, rep, sub, st1, p) for p in ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT")}
        if variant == "A4-header":
            base[code] = inds["ALWAYS"]
        for p in ("MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT"):
            for label, ref in ((f"{p} minus ALWAYS, same prompt", inds["ALWAYS"]), (f"{p} minus ALWAYS under the header", base[code])):
                if variant == "A4-header" and label.endswith("under the header"):
                    continue
                a = np.array([ref[i] for i in ids], float); b = np.array([inds[p][i] for i in ids], float); d = b - a
                rng = np.random.default_rng(SEED); n = len(d)
                di = [d[rng.integers(0, n, n)].mean() for _ in range(N_BOOT)]
                dc = [d[np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))])].mean() for _ in range(N_BOOT)]
                out[f"{variant}|{code}|{label}"] = {"variant": variant, "answerer": code, "comparison": label, "composite_policy": int(b.sum()), "composite_always": int(a.sum()),
                                                    "difference_count": int(b.sum() - a.sum()), "difference_rate": round(float(d.mean()), 4),
                                                    "ci_item": [round(float(np.percentile(di, 2.5)), 4), round(float(np.percentile(di, 97.5)), 4)],
                                                    "ci_persona": [round(float(np.percentile(dc, 2.5)), 4), round(float(np.percentile(dc, 97.5)), 4)], "n": n, "n_boot": N_BOOT, "seed": SEED}
    S = J(RUN / "scores_amend7.json"); S["composite_diff"] = out; S["composite_diff_when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend7.json")
    L = ["\n### AUX-DS-A7-COMPOSITE-DIFF: the composite under each gated rule minus under retrieval alone (the author's addition of 2026-09-15, after the registration; descriptive, no bar): a paired difference of rates over the 661 items, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas). The oracle is excluded from every comparison: its absent component is the label itself (D-DS-A7-1). Retrieval alone and the literal rule have no coverage rule, so their absent component is 0 of 383 and the difference is carried mostly by the absent items.\n\n",
         "| answerer | prompt | comparison | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |\n|---|---|---|---|---|---|---|\n"]
    for k, v in out.items():
        L.append(f"| {v['answerer']} | {v['variant']} | {v['comparison']} | {v['composite_policy']}; {v['composite_always']} of 661 | {v['difference_count']:+d}; {v['difference_rate']:+.4f} | [{v['ci_item'][0]:+.4f}, {v['ci_item'][1]:+.4f}] | [{v['ci_persona'][0]:+.4f}, {v['ci_persona'][1]:+.4f}] |\n")
    txt = "".join(L)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


# ------------------------------------------------------------------ the composite in the answered reading (the author's instruction of 2026-09-15, evening)
def reported_answered(rep_row):
    """Reports the obligation: the registered rule (names the state, no stale value), or, on a supersession item, the answer gives the successor
    (the committed detector's successor_use at TAU_HI), which reports the obligation by using the current value."""
    return bool(rep_row["reported"]) or (rep_row["state"] == "sup" and bool(rep_row.get("successor_use")))


def absent_answered_abstention(code):
    """Per absent item: did the answerer abstain on the recorded five-line view (Amendment 6's FLAT-5 rows, answered under the header)?"""
    out = {}
    for l in io.open(RUN / f"rows_ds_amend6_{code.lower()}.jsonl", encoding="utf-8"):
        r = json.loads(l)
        if r["label"] == "ABSENT" and "FLAT-5" in r["policies"] and r["status"] == "OK":
            out[r["item_id"]] = A4.is_abst(r["answer"])
    return out


def cmd_composite_answered():
    """AUX-DS-A7-COMPOSITE-ANSWERED and -ANSWERED-DIFF: the composite per policy with (i) the licensed item correct at 0.50, (ii) the obligation reached,
    answered and reported in the answered reading (the registered rule, or the successor given on a supersession item), (iii) the absent item
    abstained on, by the coverage rule or by the answerer on its recorded five-line view (Amendment 6's FLAT-5 answers under the header; the
    absent items the gated rules answer on a longer view, 10 under the model rule, 17 under the lookup rule and 72 under the literal rule, are
    read on that five-line view as a proxy, stated). The oracle prints and enters no comparison (D-DS-A7-1). Paired differences against
    retrieval alone under the same prompt with both bootstraps (10,000 draws, seed 42). Descriptive; ordered by the author after the registration."""
    import numpy as np
    sys.stdout.reconfigure(encoding="utf-8")
    assert registration_ok() and J(RUN / "lock_amend7.json")["gates_ok"], "STOP: lock first"
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    st1 = J(DS / "stage1.json")["per_item"]
    ids = [it["item_id"] for it in sub]; pers = np.array([byid[i]["persona"] for i in ids]); groups = np.unique(pers); by = {u: np.flatnonzero(pers == u) for u in groups}
    n_lic = sum(1 for it in sub if it["label"] == "PRESENT"); n_obl = sum(1 for it in sub if it["label"] == "PRESENT-NEGATIVE"); n_abs = sum(1 for it in sub if it["label"] == "ABSENT")
    N_BOOT, SEED = 10000, 42
    POLS = ("ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-ALL", "LOOKUP-LIT", "ORACLE")
    out, diffs = {}, {}
    for variant, code, paths in FILES:
        if variant not in ("A4-header", "A5-duplicates-tagged"):
            continue
        rows, per, rep = score_file(paths, sub, rec, byid)
        abst5 = absent_answered_abstention(code)
        inds = {}
        for p in POLS:
            lic = {r["item_id"]: bool(per[k]["correct"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT" and per[k].get("scored")}
            obl = {r["item_id"]: reported_answered(rep[k]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep}
            obl_reg = {r["item_id"]: bool(rep[k]["reported"]) for k, r in rows.items() if p in r["policies"] and r["label"] == "PRESENT-NEGATIVE" and k in rep}
            ind, comp = {}, {"licensed_correct": 0, "reported_answered": 0, "reported_registered_rule": 0, "successor_on_sup": 0, "absent_rule": 0, "absent_answerer": 0, "absent_proxy_longer_view": 0}
            for it in sub:
                i = it["item_id"]
                if it["label"] == "PRESENT":
                    v = int(lic.get(i, False)); comp["licensed_correct"] += v
                elif it["label"] == "PRESENT-NEGATIVE":
                    v = int(obl.get(i, False)); comp["reported_answered"] += v; comp["reported_registered_rule"] += int(obl_reg.get(i, False))
                    comp["successor_on_sup"] += int(v and not obl_reg.get(i, False))
                else:
                    rule = bool(st1[i][p]["abstain"])
                    if rule:
                        v = 1; comp["absent_rule"] += 1
                    else:
                        v = int(abst5.get(i, False)); comp["absent_answerer"] += v
                        comp["absent_proxy_longer_view"] += int(st1[i][p]["view_size"] > 5)
                ind[i] = v
            inds[p] = ind
            comp["absent_abstained"] = comp["absent_rule"] + comp["absent_answerer"]
            comp["composite"] = comp["licensed_correct"] + comp["reported_answered"] + comp["absent_abstained"]
            comp["of"] = {"licensed": n_lic, "obligations": n_obl, "absent": n_abs, "all": 661}
            out[f"{variant}|{code}|{p}"] = comp
        for p in POLS[1:-1]:
            a = np.array([inds["ALWAYS"][i] for i in ids], float); b = np.array([inds[p][i] for i in ids], float); d = b - a; n = len(d)
            rng = np.random.default_rng(SEED)
            di = [d[rng.integers(0, n, n)].mean() for _ in range(N_BOOT)]
            dc = [d[np.concatenate([by[groups[t]] for t in rng.integers(0, len(groups), len(groups))])].mean() for _ in range(N_BOOT)]
            diffs[f"{variant}|{code}|{p}"] = {"composite_policy": int(b.sum()), "composite_always": int(a.sum()), "difference_count": int(b.sum() - a.sum()), "difference_rate": round(float(d.mean()), 4),
                                              "ci_item": [round(float(np.percentile(di, 2.5)), 4), round(float(np.percentile(di, 97.5)), 4)],
                                              "ci_persona": [round(float(np.percentile(dc, 2.5)), 4), round(float(np.percentile(dc, 97.5)), 4)], "n_boot": N_BOOT, "seed": SEED}
    S = J(RUN / "scores_amend7.json"); S["composite_answered"] = out; S["composite_answered_diff"] = diffs; S["composite_answered_when"] = dt.datetime.now().isoformat(timespec="seconds")
    jdump(S, RUN / "scores_amend7.json")
    L = ["\n### AUX-DS-A7-COMPOSITE-ANSWERED: the composite per policy in the answered reading (the author's instruction of 2026-09-15, evening; descriptive, after the registration). A licensed item counts when correct at 0.50; an obligation when reached, answered and reported, where reported is the registered rule (names the state, no stale value) or, on a supersession item, the successor given (the committed detector's successor_use at TAU_HI); an absent item when the coverage rule abstained on it or the answerer abstained on its recorded five-line view (Amendment 6's FLAT-5 answers under the header, the same for both prompt variants; the absent items a gated rule answers on a longer view, 10 under the model rule, 17 under the lookup rule and 72 under the literal rule, are read on the five-line view as a proxy). The oracle's absent component is the label itself (D-DS-A7-1); it prints and enters no comparison. The rule-only reading is AUX-DS-A7-COMPOSITE above.\n\n",
         "| prompt | answerer | policy | licensed correct (of 174) | reported, answered reading (of 104) | of which by the successor alone | reported, registered rule | absent abstained (of 383) = by the rule + by the answerer | absent read on a five-line proxy | composite (of 661) |\n|---|---|---|---:|---:|---:|---:|---|---:|---:|\n"]
    for k, c in out.items():
        variant, code, p = k.split("|")
        L.append(f"| {variant} | {code} | {p} | {c['licensed_correct']} | {c['reported_answered']} | {c['successor_on_sup']} | {c['reported_registered_rule']} | {c['absent_abstained']} = {c['absent_rule']} + {c['absent_answerer']} | {c['absent_proxy_longer_view']} | **{c['composite']}** |\n")
    L.append("\n### AUX-DS-A7-COMPOSITE-ANSWERED-DIFF: each gated rule minus retrieval alone under the same prompt, the answered reading; a paired difference of rates over the 661 items, item-level and persona-grouped percentile bootstraps (10,000 draws, seed 42, 40 personas); the oracle excluded\n\n| prompt | answerer | policy | composite (rule; retrieval alone) | difference (count; rate) | item 95% | persona 95% |\n|---|---|---|---|---|---|---|\n")
    for k, v in diffs.items():
        variant, code, p = k.split("|")
        L.append(f"| {variant} | {code} | {p} | {v['composite_policy']}; {v['composite_always']} | {v['difference_count']:+d}; {v['difference_rate']:+.4f} | [{v['ci_item'][0]:+.4f}, {v['ci_item'][1]:+.4f}] | [{v['ci_persona'][0]:+.4f}, {v['ci_persona'][1]:+.4f}] |\n")
    txt = "".join(L)
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    {"lock": cmd_lock, "score": cmd_score, "composite-diff": cmd_composite_diff, "composite-answered": cmd_composite_answered}[sys.argv[1]]()
