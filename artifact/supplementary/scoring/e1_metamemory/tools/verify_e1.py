"""
verify_e1.py -- E1 PN verification pass, both halves, full coverage.

NO API CALLS. Detector proposes, YAML disposes.

SEMANTIC half, once per (question, YAML-record): does this record constitute a
negative obligation for this question UNDER ITS INTENT? Backend-independent.
CHANGE-AWARE and PAST-EVENT are structurally barred, so they never reach here.

MEMBERSHIP half, per (entry, record) at TAU_HI: does this entry assert the
superseded value AS CURRENT? Frozen criterion (PREREG_E1 3.1, verbatim from design
doc 3), with three named exclusions:
    decision-against      "considered X but decided against it"
    historically-framed   "the previous focus was X", "used to"
    token-collision       unrelated facts sharing tokens
Anything excluded for a reason OUTSIDE those three is tagged `other:<name>` and
reported in a dedicated edge-case table. It is never folded into the criterion.

Usage:
    python e1_metamemory/tools/verify_e1.py emit
    python e1_metamemory/tools/verify_e1.py apply
"""

from __future__ import annotations

import collections
import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
E1 = PROJECT_ROOT / "e1_metamemory"
sys.path.insert(0, str(PROJECT_ROOT / "e0_metamemory" / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from e0_common import SECTION_FIELDS, load_joins  # noqa: E402

ITEMS = E1 / "build" / "items_pre.json"
NAMED = {"decision-against", "historically-framed", "token-collision"}


def jload(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def collect():
    items = jload(ITEMS)
    joins = load_joins()
    pn = [i for i in items if i["label_pre"] == "PN-CANDIDATE"]
    sem, mem = {}, {}
    for i in pn:
        p, qid = i["persona"], i["question_id"]
        J = joins[p]
        q = next(x for x in J.questions if x["id"] == qid)
        sec, ridx = J.rec_of[qid]
        rec = [r for r in (J.y.get(sec) or []) if isinstance(r, dict)][ridx]
        gf, gs, sf, ss = SECTION_FIELDS[sec]
        sem.setdefault((p, qid), {
            "persona": p, "question_id": qid, "intent": i["intent"],
            "attack_vector": i["attack_vector"], "question": q["question"],
            "correct_answer": q.get("correct_answer", ""),
            "section": sec, "record_idx": ridx,
            "superseded": str(rec.get(sf)) if sf else None,
            "current": str(rec.get(gf)),
            "event_date": rec.get("event_date"), "yaml_status": rec.get("status"),
            "variants": [],
        })["variants"].append(i["variant"])
        for eid in i["pn_evidence"]:
            mem.setdefault((p, qid, eid), {
                "persona": p, "question_id": qid, "entry_id": eid,
                "signal": i["pn_evidence"][eid],
                "entry_text": J.by_id[eid]["text"] if eid in J.by_id else "(expired-route)",
                "is_active": bool(J.by_id[eid]["is_active"]) if eid in J.by_id else None,
                "superseded": str(rec.get(sf)) if sf else None,
                "current": str(rec.get(gf)),
            })
    return sem, mem, pn


def cmd_emit():
    sem, mem, pn = collect()
    L = ["# E1 PN VERIFICATION — SEMANTIC HALF", "",
         f"{len(sem)} (question, YAML-record) pairs. Backend-independent, read once each.",
         "",
         "**Question:** does this YAML record constitute a negative obligation for this question "
         "**under its intent**? CURRENT-STATE and UPCOMING only reach here; CHANGE-AWARE and "
         "PAST-EVENT are structurally barred. YAML `status` overrides any derived cutoff.", "",
         "| # | persona | qid | intent | question | superseded value | current value | status |",
         "|---|---|---|---|---|---|---|---|"]
    for n, (k, v) in enumerate(sorted(sem.items()), 1):
        esc = lambda s: (str(s) or "").replace("|", "\\|")[:88]
        L.append(f"| {n} | {v['persona']} | `{v['question_id']}` | {v['intent'][:7]} | "
                 f"{esc(v['question'])} | {esc(v['superseded'])} | {esc(v['current'])} | "
                 f"{v.get('yaml_status') or ''} |")
    io.open(E1 / "verify_semantic.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

    M = ["# E1 PN VERIFICATION — MEMBERSHIP HALF", "",
         f"{len(mem)} (entry, record) pairs at TAU_HI.", "",
         "**Criterion (frozen):** does this entry assert the superseded value **AS CURRENT**? "
         "Named exclusions: `decision-against`, `historically-framed`, `token-collision`. "
         "Anything else is tagged `other:<name>` and reported separately.", "",
         "| # | persona | entry | sig | act | entry text | superseded value |",
         "|---|---|---|---|---|---|---|"]
    for n, (k, v) in enumerate(sorted(mem.items()), 1):
        esc = lambda s: (str(s) or "").replace("|", "\\|")
        M.append(f"| {n} | {v['persona']} | `{v['entry_id']}` | {v['signal']:.2f} | "
                 f"{'' if v['is_active'] is None else int(v['is_active'])} | "
                 f"{esc(v['entry_text'])[:140]} | {esc(v['superseded'])[:80]} |")
    io.open(E1 / "verify_membership.md", "w", encoding="utf-8", newline="\n").write("\n".join(M) + "\n")

    jdump({"semantic": [{"key": list(k), **v} for k, v in sorted(sem.items())],
           "membership": [{"key": list(k), **v} for k, v in sorted(mem.items())],
           "n_pn_candidates": len(pn)}, E1 / "verify_pending.json")
    print(f"semantic pairs {len(sem)}  membership pairs {len(mem)}  "
          f"total {len(sem)+len(mem)}  (PN candidates {len(pn)})")
    print(f"wrote verify_semantic.md, verify_membership.md, verify_pending.json")


def cmd_apply():
    from verify_verdicts import SEMANTIC, MEMBERSHIP  # noqa: PLC0415
    sem, mem, _ = collect()
    missing_s = [k for k in sem if k not in SEMANTIC]
    missing_m = [k for k in mem if (k[0], k[1], k[2]) not in MEMBERSHIP]
    if missing_s or missing_m:
        raise SystemExit(f"unverified: {len(missing_s)} semantic, {len(missing_m)} membership; "
                         f"e.g. {(missing_s or missing_m)[:3]}")

    items = jload(ITEMS)
    edge = []
    kept_m = set()
    excl = collections.Counter()
    for k, v in mem.items():
        verdict, tag = MEMBERSHIP[(k[0], k[1], k[2])]
        if verdict == "MEMBER":
            kept_m.add(k)
        else:
            excl[tag] += 1
            if tag not in NAMED:
                edge.append({**v, "exclusion_tag": tag})

    sem_neg = {k for k, v in sem.items() if SEMANTIC[k][0] == "OBLIGATION"}
    counts = collections.Counter()
    for i in items:
        if i["label_pre"] != "PN-CANDIDATE":
            i.setdefault("label", i["label_pre"])
            continue
        p, qid = i["persona"], i["question_id"]
        surviving = [e for e in i["pn_evidence"] if (p, qid, e) in kept_m]
        if (p, qid) not in sem_neg:
            i["label"], i["subtype"] = "UNRESOLVED", "semantic-not-an-obligation"
        elif surviving:
            i["label"] = "PRESENT-NEGATIVE"
        else:
            i["label"], i["subtype"] = "UNRESOLVED", "no-member-survived"
        i["pn_members"] = surviving
        counts[i["label"]] += 1
    jdump(items, ITEMS)

    print("=" * 84)
    print("PN VERIFICATION OUTCOME")
    print("=" * 84)
    print(f"  semantic pairs {len(sem)}: OBLIGATION {len(sem_neg)}, "
          f"NOT-AN-OBLIGATION {len(sem)-len(sem_neg)}")
    print(f"  membership pairs {len(mem)}: MEMBER {len(kept_m)}, "
          f"excluded {len(mem)-len(kept_m)}")
    print(f"  exclusions by tag: {dict(excl)}")
    print(f"  edge cases outside the three named patterns: {len(edge)}")
    print(f"\n  PN candidates routed: {dict(counts)}")
    jdump({"semantic_total": len(sem), "semantic_obligation": len(sem_neg),
           "membership_total": len(mem), "membership_member": len(kept_m),
           "exclusions_by_tag": dict(excl), "edge_cases": edge,
           "routing": dict(counts)}, E1 / "verify_results.json")
    if edge:
        L = ["# MEMBERSHIP EDGE CASES — outside the three named exclusion patterns", "",
             f"{len(edge)} pairs. Tagged during the pass, reported here, **never folded into the "
             "frozen criterion**.", "",
             "| persona | entry | sig | tag | entry text | superseded value |",
             "|---|---|---|---|---|---|"]
        for e in edge:
            esc = lambda s: (str(s) or "").replace("|", "\\|")
            L.append(f"| {e['persona']} | `{e['entry_id']}` | {e['signal']:.2f} | "
                     f"**{e['exclusion_tag']}** | {esc(e['entry_text'])[:120]} | "
                     f"{esc(e['superseded'])[:70]} |")
        io.open(E1 / "MEMBERSHIP_EDGE_CASES.md", "w", encoding="utf-8",
                newline="\n").write("\n".join(L) + "\n")
        print(f"  wrote MEMBERSHIP_EDGE_CASES.md")


if __name__ == "__main__":
    {"emit": cmd_emit, "apply": cmd_apply}[sys.argv[1] if len(sys.argv) > 1 else "emit"]()
