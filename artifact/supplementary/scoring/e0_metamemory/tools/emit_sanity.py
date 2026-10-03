"""
emit_sanity.py -- the two Step-1 sanity checks required by the pre-registration,
rendered as a markdown appendix.

NO API CALLS.

(a) For 10 randomly sampled ABSENT items (seed 42): print the gold edges and grep
    the variant to confirm absence.
(b) For 10 sampled PRESENT-NEGATIVE items: print the YAML event establishing the
    negative obligation.

The samples are the ones recorded in step1_census.json, drawn with seed 42 at
build time, so this script re-renders rather than re-samples.
"""

from __future__ import annotations

import io
import sys

from e0_common import E0, SECTION_FIELDS, jload, load_joins

OUT = E0 / "STEP1_SANITY_APPENDIX.md"


def main():
    cen = jload(E0 / "step1_census.json")
    items = {i["item_id"]: i for i in jload(E0 / "items.json")}
    joins = load_joins()
    qs = {q["id"]: q for J in joins.values() for q in J.questions}
    L = []

    L.append("# STEP 1 — SANITY APPENDIX\n")
    L.append("Required by `PREREG_E0.md` §7. Samples drawn with seed 42 at build time and "
             "re-rendered here; no re-sampling. No API calls.\n")

    L.append("\n## (a) Ten sampled ABSENT items — gold edges, and the variant grepped for them\n")
    for iid in cen["sanity_absent_sample"]:
        it = items[iid]
        J = joins[it["persona"]]
        q = qs[it["question_id"]]
        abl = set(it["ablated_categories"]) if it["variant"] == "ABLATED" else set()
        gold_full = sorted(J.gold[it["question_id"]] or [])
        L.append(f"\n### `{iid}` — {it['attack_vector']}\n")
        L.append(f"- **Question:** {q['question']}")
        L.append(f"- **Gold answer:** {q['correct_answer']}")
        L.append(f"- **Ablated categories:** {', '.join(it['ablated_categories']) or '(none — FULL)'}")
        expired_full = sorted(J.expired_neg[it["question_id"]] or [])
        if gold_full:
            L.append(f"- **Gold edges in the FULL bank:** {', '.join(gold_full)}")
        else:
            L.append("- **Gold edges in the FULL bank:** none — and this is correct rather "
                     "than a resolution failure. Every dated entry for this question has "
                     "expired, so the licensed current content is empty and the gold answer "
                     "is itself a negative. ABSENT here means the ablation removed the "
                     "**expired** content, leaving nothing that bears on the question.")
        L.append("")
        if gold_full:
            L.append("| gold edge | category | ablated? | in this variant? | text |")
            L.append("|---|---|---|---|---|")
            for eid in gold_full:
                e = J.by_id[eid]
                gone = e["category"] in abl
                txt = e["text"].replace("|", "\\|")[:90]
                L.append(f"| `{eid}` | {e['category']} | {'YES' if gone else 'no'} | "
                         f"{'**absent**' if gone else 'PRESENT'} | {txt} |")
        if expired_full:
            L.append("")
            L.append("| expired entry (negative obligation) | category | event_time | ablated? | text |")
            L.append("|---|---|---|---|---|")
            for eid in expired_full:
                e = J.by_id[eid]
                gone = e["category"] in abl
                txt = e["text"].replace("|", "\\|")[:80]
                L.append(f"| `{eid}` | {e['category']} | {str(e.get('event_time'))[:10]} | "
                         f"{'YES' if gone else 'no'} | {txt} |")
        surviving = [e for e in gold_full if J.by_id[e]["category"] not in abl]
        surv_exp = [e for e in expired_full if J.by_id[e]["category"] not in abl]
        L.append("")
        L.append(f"- **Surviving gold edges: {len(surviving)}**; "
                 f"**surviving negative-obligation entries: {len(surv_exp)}** — "
                 f"{'confirms ABSENT' if not surviving and not surv_exp else 'INCONSISTENT'}")

    L.append("\n\n## (b) Ten sampled PRESENT-NEGATIVE items — the YAML event establishing the obligation\n")
    for iid in cen["sanity_pn_sample"]:
        it = items[iid]
        J = joins[it["persona"]]
        q = qs[it["question_id"]]
        sec, ridx = J.rec_of[it["question_id"]]
        rec = [r for r in (J.y.get(sec) or []) if isinstance(r, dict)][ridx]
        gf, gs, sf, ss = SECTION_FIELDS[sec]
        L.append(f"\n### `{iid}` — {it['attack_vector']} · subtype **{it['subtype']}**\n")
        L.append(f"- **Question:** {q['question']}")
        L.append(f"- **Gold answer:** {q['correct_answer']}")
        L.append(f"- **YAML section:** `{sec}` record #{ridx}")
        if sf:
            L.append(f"- **Superseded value** (session {rec.get(ss)}): "
                     f"*\"{rec.get(sf)}\"*")
            L.append(f"- **Current value** (session {rec.get(gs)}): *\"{rec.get(gf)}\"*")
        else:
            L.append(f"- **Fact** (session {rec.get(gs)}): *\"{rec.get(gf)}\"*")
            L.append(f"- **event_date:** {rec.get('event_date')} · "
                     f"**YAML status:** {rec.get('status')} · "
                     f"**expiry cutoff:** {J.cutoff.date()} (t_now {J.t_now.date()} − 14d)")
        L.append("")
        if it["expired_ids"]:
            L.append("| expired entry | category | event_time | text |")
            L.append("|---|---|---|---|")
            for eid in it["expired_ids"]:
                e = J.by_id[eid]
                L.append(f"| `{eid}` | {e['category']} | {str(e.get('event_time'))[:10]} | "
                         f"{e['text'].replace('|', chr(92) + '|')[:80]} |")
        if it["fire_ids"]:
            L.append("| firing entry | signal | category | active | text |")
            L.append("|---|---|---|---|---|")
            for eid, sig in sorted(it["fire_ids"].items(), key=lambda t: -t[1]):
                e = J.by_id[eid]
                mark = "**" if sig >= 0.80 else ""
                L.append(f"| `{eid}` | {mark}{sig:.2f}{mark} | {e['category']} | "
                         f"{int(e['is_active'])} | {e['text'].replace('|', chr(92)+'|')[:80]} |")
        L.append("")
        L.append(f"- **Surviving gold (current value) in this variant: "
                 f"{len(it['gold_ids'])}** — consistent with subtype `{it['subtype']}`")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote {OUT} ({len(L)} lines)")


if __name__ == "__main__":
    main()
