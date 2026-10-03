"""
verify_pn.py -- Amendment 1 change 3: full per-item verification of every admitted
PRESENT-NEGATIVE item, under a DETECTOR-PROPOSES, YAML-DISPOSES rule.

NO API CALLS. The detector (and the expiry date comparison) only nominates
evidence; whether that evidence really establishes a negative obligation is
settled by reading the YAML record. Items whose every piece of admitting evidence
fails verification route to UNRESOLVED.

Instrument: identical to the committed 30-fire tau audit. For an admitting entry e
nominated for question q against YAML record R:

    TRUE   e asserts the value R marks as superseded / retracted / expired, so
           e's correct influence on an answer to q is SUPPRESSION.
    FALSE  it does not -- incidental token overlap, entries already tense-marked
           as past, entries that assert the CURRENT value, entries asserting a
           part of R that was not the thing superseded, or (for expiry) entries
           that do not bear on q at all.

Verdicts are recorded per (persona, question_id, entry_id) -- the composite key --
and an ITEM is verified iff at least one of its SURVIVING admitting entries is
TRUE. That makes the FULL and ABLATED variants of one question inherit the same
per-entry readings without being read twice, while still differing when the
ablation removes the entry that carried the verdict.

Usage:
    python e0_metamemory/tools/verify_pn.py emit    # writes pn_verification_worksheet.md
    python e0_metamemory/tools/verify_pn.py apply   # reads verdicts, writes pn_verification.json
"""

from __future__ import annotations

import collections
import io
import sys

from e0_common import E0, SECTION_FIELDS, jdump, jload, load_joins, load_thresholds

WORKSHEET = E0 / "pn_verification_worksheet.md"
OUT = E0 / "pn_verification.json"


def admitted(item, tau_hi):
    """The evidence that admitted this item to PRESENT-NEGATIVE, in its variant."""
    fires = [(e, s) for e, s in item["fire_ids"].items() if s >= tau_hi]
    exp = [(e, None) for e in item["expired_ids"]]
    return fires + exp


def groups(tau_hi):
    """(persona, question_id) -> {record context, entry evidence, items}."""
    items = jload(E0 / "items.json")
    joins = load_joins()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}
    g = collections.OrderedDict()
    for it in items:
        if it["label"] != "PRESENT-NEGATIVE":
            continue
        key = (it["persona"], it["question_id"])
        J = joins[it["persona"]]
        if key not in g:
            sec, ridx = J.rec_of[it["question_id"]]
            rec = [r for r in (J.y.get(sec) or []) if isinstance(r, dict)][ridx]
            g[key] = {"persona": it["persona"], "question_id": it["question_id"],
                      "q": qs[it["question_id"]], "section": sec, "rec": rec,
                      "J": J, "items": [], "evidence": {}}
        g[key]["items"].append(it)
        for eid, sig in admitted(it, tau_hi):
            prev = g[key]["evidence"].get(eid)
            g[key]["evidence"][eid] = sig if prev is None else (prev if sig is None else max(prev, sig))
    return g


def cmd_emit():
    _, tau_hi = load_thresholds()
    g = groups(tau_hi)
    L = ["# PRESENT-NEGATIVE verification worksheet",
         "",
         "Amendment 1, change 3. Detector proposes, YAML disposes. Every admitted "
         "PRESENT-NEGATIVE item is read against the YAML record that nominated it.",
         "",
         f"{len(g)} distinct questions, "
         f"{sum(len(v['evidence']) for v in g.values())} (question, entry) pairs, "
         f"{sum(len(v['items']) for v in g.values())} items.",
         "",
         "**TRUE** = the entry asserts the superseded / retracted / expired value, so its "
         "correct influence on an answer is suppression. **FALSE** otherwise.",
         ""]
    for (p, qid), v in g.items():
        sec, rec, J = v["section"], v["rec"], v["J"]
        gf, gs, sf, ss = SECTION_FIELDS[sec]
        L.append(f"\n---\n\n## `{p}` / `{qid}` — {v['q']['attack_vector']}\n")
        L.append(f"- **Question:** {v['q']['question']}")
        L.append(f"- **Gold answer:** {v['q']['correct_answer']}")
        L.append(f"- **YAML `{sec}`:**")
        if sf:
            L.append(f"  - superseded (s{rec.get(ss)}): **\"{rec.get(sf)}\"**")
            L.append(f"  - current (s{rec.get(gs)}): \"{rec.get(gf)}\"")
        else:
            L.append(f"  - fact (s{rec.get(gs)}): **\"{rec.get(gf)}\"**")
            L.append(f"  - event_date {rec.get('event_date')} · YAML status "
                     f"{rec.get('status')} · cutoff {J.cutoff.date()}")
        L.append(f"- **Items:** {', '.join(i['item_id'].rsplit(':', 1)[1] for i in v['items'])}")
        L.append("")
        L.append("| entry | signal | category | active | event_time | text | verdict |")
        L.append("|---|---|---|---|---|---|---|")
        for eid, sig in sorted(v["evidence"].items(), key=lambda t: (t[1] is None, -(t[1] or 0), t[0])):
            e = J.by_id[eid]
            s = "expiry" if sig is None else f"{sig:.2f}"
            L.append(f"| `{eid}` | {s} | {e['category']} | {int(e['is_active'])} | "
                     f"{str(e.get('event_time'))[:10]} | "
                     f"{e['text'].replace('|', chr(92)+'|')} |  |")
    with io.open(WORKSHEET, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote {WORKSHEET}: {len(g)} questions, "
          f"{sum(len(v['evidence']) for v in g.values())} pairs")


def cmd_apply():
    from pn_verdicts import VERDICTS
    _, tau_hi = load_thresholds()
    g = groups(tau_hi)
    rows, missing = [], []
    for (p, qid), v in g.items():
        for eid in v["evidence"]:
            if (p, qid, eid) not in VERDICTS:
                missing.append((p, qid, eid))
    if missing:
        raise SystemExit(f"{len(missing)} unverified pairs, e.g. {missing[:3]}")

    item_verdict, per_item = {}, []
    for (p, qid), v in g.items():
        J = v["J"]
        for it in v["items"]:
            ev = [e for e, _ in admitted(it, tau_hi)]
            true_ev = [e for e in ev if VERDICTS[(p, qid, e)][0] == "TRUE"]
            ok = bool(true_ev)
            item_verdict[it["item_id"]] = ok
            per_item.append({
                "item_id": it["item_id"], "persona": p, "question_id": qid,
                "variant": it["variant"], "attack_vector": it["attack_vector"],
                "subtype": it["subtype"],
                "n_admitting": len(ev), "n_verified_true": len(true_ev),
                "verified": ok,
                "new_label": "PRESENT-NEGATIVE" if ok else "UNRESOLVED",
                "evidence": [{"entry_id": e, "signal": v["evidence"][e],
                              "verdict": VERDICTS[(p, qid, e)][0],
                              "note": VERDICTS[(p, qid, e)][1],
                              "text": J.by_id[e]["text"]} for e in sorted(ev)],
            })
        for eid, sig in v["evidence"].items():
            rows.append({"persona": p, "question_id": qid, "entry_id": eid,
                         "signal": sig, "verdict": VERDICTS[(p, qid, eid)][0],
                         "note": VERDICTS[(p, qid, eid)][1],
                         "text": J.by_id[eid]["text"],
                         "attack_vector": v["q"]["attack_vector"],
                         "section": v["section"]})

    kept = sum(1 for x in per_item if x["verified"])
    dropped = len(per_item) - kept
    tp = sum(1 for r in rows if r["verdict"] == "TRUE")
    print(f"(question, entry) pairs : {len(rows)}  TRUE {tp}  FALSE {len(rows)-tp} "
          f"({tp/len(rows):.1%} precision of the admitted set)")
    print(f"PN items                : {len(per_item)}  verified {kept}  "
          f"-> UNRESOLVED {dropped}")

    # precision of tau_hi as a candidate filter, by signal band
    band = collections.Counter()
    for r in rows:
        if r["signal"] is None:
            band[("expiry", r["verdict"])] += 1
        else:
            b = "1.00" if r["signal"] >= 0.999 else ("0.80-0.99" if r["signal"] >= 0.80 else "<0.80")
            band[(b, r["verdict"])] += 1
    print("\n  admitted-evidence precision by band:")
    for b in ("1.00", "0.80-0.99", "<0.80", "expiry"):
        t, f = band[(b, "TRUE")], band[(b, "FALSE")]
        if t + f:
            print(f"    {b:10s} {t:3d}/{t+f:3d} = {t/(t+f):.1%}")

    jdump({
        "meta": {
            "rule": "detector proposes, YAML disposes; item verified iff >=1 surviving "
                    "admitting entry reads TRUE against the YAML record",
            "instrument": "identical to the committed 30-fire tau audit",
            "tau_hi_status": "candidate filter only; superseded by per-item verification",
            "no_api_calls": True,
        },
        "pairs": sorted(rows, key=lambda r: (r["persona"], r["question_id"], r["entry_id"])),
        "items": sorted(per_item, key=lambda r: r["item_id"]),
        "summary": {"n_pairs": len(rows), "n_pairs_true": tp,
                    "n_items": len(per_item), "n_verified": kept, "n_to_unresolved": dropped},
    }, OUT)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    {"emit": cmd_emit, "apply": cmd_apply}[sys.argv[1] if len(sys.argv) > 1 else "emit"]()
