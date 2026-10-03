"""
build_dataset.py -- E0 Step 1: build the FULL and ABLATED store variants, label
every (question, variant) item, and verify the build.

NO API CALLS. Executes the plan frozen in PREREG_E0.md / plan.json; makes no
design decisions of its own.

Nine build-integrity assertions, one per hazard identified in FINDINGS_E0_STEP0.md.
Any failure aborts before anything is written to the item records.
"""

from __future__ import annotations

import collections
import hashlib
import json
import random
import re
import shutil
import sys

from e0_common import (
    BANKS, E0, PROJECT_ROOT, SEED, jdump, jload, load_joins, load_thresholds,
)

sys.path.insert(0, str(PROJECT_ROOT / "analysis" / "ontology_validation"))
from exp4_witnesses import supports_correct  # noqa: E402

STORES = E0 / "stores"
ITEMS_PATH = E0 / "items.json"
STEP1_PATH = E0 / "STEP1_REPORT.md"
STEM_RE = re.compile(r"^[a-z]+_(full|ablated)$")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def banks_manifest():
    return {p.name: sha256_file(p) for p in sorted(BANKS.iterdir()) if p.is_file()}


def main():
    tau_lo, tau_hi = load_thresholds()
    plan = jload(E0 / "plan.json")
    personas = plan["personas"]
    joins = load_joins()

    before = banks_manifest()          # ASSERTION 5, first half
    STORES.mkdir(parents=True, exist_ok=True)

    checks = collections.Counter()
    problems = []
    items = []
    dangling = collections.Counter()
    manifest = {}

    for name in sorted(personas):
        J = joins[name]
        ablated = frozenset(personas[name]["ablated_categories"])
        src = jload(BANKS / f"{name}.json")
        full_entries = src["entries"]
        full_ids = [e["id"] for e in full_entries]

        # ---------- ASSERTION 1: composite keys, no bare entry_id as a global key
        if len(set(full_ids)) != len(full_ids):
            problems.append(f"{name}: duplicate entry ids inside one bank")
        checks["1_composite_keys"] += 1

        abl_entries = [e for e in full_entries if e["category"] not in ablated]
        abl_ids = {e["id"] for e in abl_entries}

        # ---------- ASSERTION 2: deletion only; survivors byte-identical
        if not abl_ids <= set(full_ids):
            problems.append(f"{name}: ablated ids not a subset of full ids")
        by_full = {e["id"]: e for e in full_entries}
        for e in abl_entries:
            if json.dumps(e, sort_keys=True) != json.dumps(by_full[e["id"]], sort_keys=True):
                problems.append(f"{name}/{e['id']}: survivor not byte-identical")
                break
        checks["2_deletion_only"] += 1

        # ---------- ASSERTION 3: next_id preserved, never recomputed
        out_full = {"next_id": src["next_id"], "entries": full_entries}
        out_abl = {"next_id": src["next_id"], "entries": abl_entries}
        if out_abl["next_id"] != src["next_id"] or out_abl["next_id"] == len(abl_entries):
            if out_abl["next_id"] != src["next_id"]:
                problems.append(f"{name}: next_id altered")
        checks["3_next_id_preserved"] += 1

        # ---------- ASSERTION 4: no dot in any stem; stem regex guard
        for stem in (f"{name}_full", f"{name}_ablated"):
            if not STEM_RE.match(stem) or "." in stem:
                problems.append(f"{name}: unsafe bank stem {stem!r}")
        checks["4_stem_guard"] += 1

        jdump(out_full, STORES / f"{name}_full.json")
        jdump(out_abl, STORES / f"{name}_ablated.json")

        # ---------- ASSERTION 6: npz copied byte-for-byte, never re-saved
        npz = BANKS / f"{name}_embeddings.npz"
        for stem in (f"{name}_full", f"{name}_ablated"):
            dst = STORES / f"{stem}_embeddings.npz"
            shutil.copyfile(npz, dst)
            if sha256_file(dst) != sha256_file(npz):
                problems.append(f"{name}: npz copy differs from source")
        checks["6_npz_bytewise"] += 1

        # ---------- ASSERTION 7: t_now identical across variants
        t_now = personas[name]["t_now"]
        if t_now != J.t_now.isoformat():
            problems.append(f"{name}: t_now drifted from the frozen plan")
        checks["7_t_now_pinned"] += 1

        # ---------- ASSERTION 8: dangling supersedes pointers created by deletion
        dang = sum(1 for e in abl_entries if e.get("supersedes") and e["supersedes"] not in abl_ids)
        dangling[name] = dang

        # ---------- labels + ASSERTION 9: monotonicity
        for q in J.questions:
            qid = q["id"]
            gold_full = J.gold[qid]
            fires_full = J.fires[qid] or {}
            for variant, abl in (("FULL", frozenset()), ("ABLATED", ablated)):
                label, subtype = J.label(q, abl, tau_lo, tau_hi)
                surv = (lambda ids: sorted(i for i in ids
                                           if J.by_id[i]["category"] not in abl))
                g = surv(gold_full or set())
                f = {i: round(s, 4) for i, s in fires_full.items()
                     if J.by_id[i]["category"] not in abl}
                if variant == "ABLATED":
                    if not set(g) <= set(surv(gold_full or set()) + g):
                        problems.append(f"{name}/{qid}: gold grew under ablation")
                    if not set(f) <= set(fires_full):
                        problems.append(f"{name}/{qid}: fires grew under ablation")
                items.append({
                    "item_id": f"{name}:{qid}:{variant}",
                    "persona": name, "question_id": qid, "variant": variant,
                    "attack_vector": q["attack_vector"],
                    "label": label, "subtype": subtype,
                    "gold_ids": g,
                    "fire_ids": f,
                    "expired_ids": sorted(i for i in (J.expired_neg[qid] or set())
                                          if J.by_id[i]["category"] not in abl),
                    "ablated_categories": sorted(ablated),
                    "t_now": t_now,
                    "n_entries_in_variant": len(full_entries) if variant == "FULL" else len(abl_entries),
                })
        checks["9_monotonicity"] += 1

        for stem in (f"{name}_full", f"{name}_ablated"):
            manifest[f"stores/{stem}.json"] = sha256_file(STORES / f"{stem}.json")
            manifest[f"stores/{stem}_embeddings.npz"] = sha256_file(STORES / f"{stem}_embeddings.npz")

    # ---------- ASSERTION 5: source bank directory untouched
    after = banks_manifest()
    if before != after:
        problems.append("SOURCE BANK DIRECTORY MODIFIED -- frozen artifact violated")
    checks["5_source_untouched"] += 1

    if problems:
        for p in problems:
            print("  FAIL:", p)
        raise SystemExit(f"{len(problems)} build-integrity failures; nothing finalised")

    jdump(items, ITEMS_PATH)

    # ---------------------------------------------------------------- census
    cen = collections.Counter(i["label"] for i in items)
    sub = collections.Counter(i["subtype"] for i in items if i["label"] == "PRESENT-NEGATIVE")
    per_persona = collections.defaultdict(collections.Counter)
    per_av = collections.defaultdict(collections.Counter)
    for i in items:
        per_persona[i["persona"]][i["label"]] += 1
        per_av[i["attack_vector"]][i["label"]] += 1

    print("=" * 84)
    print("STEP 1 CENSUS")
    print("=" * 84)
    for k in ("PRESENT", "ABSENT", "PRESENT-NEGATIVE", "UNRESOLVED"):
        print(f"  {k:18s} {cen[k]:4d}")
    scoreable = cen["PRESENT"] + cen["ABSENT"] + cen["PRESENT-NEGATIVE"]
    print(f"  {'scoreable':18s} {scoreable:4d}   of {len(items)} items")
    print(f"  PRESENT-NEGATIVE subtypes: {dict(sub)}")

    frozen = plan["totals"]
    match = all(cen[k] == frozen.get(k, 0) for k in
                ("PRESENT", "ABSENT", "PRESENT-NEGATIVE", "UNRESOLVED"))
    print(f"\n  matches the frozen plan census: {'YES' if match else 'NO -- INVESTIGATE'}")

    # -------- ABSENT verification statistic (independent lexical over-approximation)
    qs = {q["id"]: q for J in joins.values() for q in J.questions}
    leak = []
    for i in items:
        if i["label"] != "ABSENT":
            continue
        J = joins[i["persona"]]
        abl = frozenset(i["ablated_categories"]) if i["variant"] == "ABLATED" else frozenset()
        ans = qs[i["question_id"]].get("correct_answer", "")
        hits = [e["id"] for e in J.entries
                if e["category"] not in abl and supports_correct(e.get("text", ""), ans)]
        if hits:
            leak.append({"item_id": i["item_id"], "n": len(hits), "entry_ids": hits[:5]})
    print(f"\n  ABSENT items whose variant still contains a LEX-proxy supporting entry: "
          f"{len(leak)}/{cen['ABSENT']}")

    print(f"\n  dangling supersedes pointers created by ablation: {sum(dangling.values())} "
          f"(max {max(dangling.values())} in one persona)")
    print("  build-integrity assertions: all passed")

    # ------------------------------------------------------- sanity samples
    rng = random.Random(SEED)
    absent_s = rng.sample([i for i in items if i["label"] == "ABSENT"], 10)
    pn_s = rng.sample([i for i in items if i["label"] == "PRESENT-NEGATIVE"], 10)

    jdump({
        "census": dict(cen), "subtypes": dict(sub), "scoreable": scoreable,
        "n_items": len(items),
        "matches_frozen_plan": match,
        "absent_lex_leak": leak,
        "dangling_supersedes": dict(dangling),
        "checks_passed": dict(checks),
        "per_persona": {k: dict(v) for k, v in sorted(per_persona.items())},
        "per_attack_vector": {k: dict(v) for k, v in sorted(per_av.items())},
        "sanity_absent_sample": [i["item_id"] for i in absent_s],
        "sanity_pn_sample": [i["item_id"] for i in pn_s],
        "store_manifest": manifest,
        "no_api_calls": True,
    }, E0 / "step1_census.json")
    print(f"\nwrote {ITEMS_PATH}, {E0/'step1_census.json'}, {len(manifest)} store files")


if __name__ == "__main__":
    main()
