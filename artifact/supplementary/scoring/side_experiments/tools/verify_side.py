"""verify_side.py -- the verifier ADDENDUM_SIDE.md (frozen e8b2630, baseline 35743cb) requires to
exist and pass before any S1 or S2 index exists. NO API CALLS.

Usage, from the repository root:  python side_experiments/tools/verify_side.py

Pre-index checks (always run):
  A  lineage -- prompts_e1 file and texts digests; sha256 of index_v2.py, two_channel.py,
     exp4_witnesses.py and common_e1r.py pinned at the freeze.
  B  RENDERER LOCK -- the identity mapping on FR-Bank reproduces indexes_v2.json
     ["frbank:<p>:FULL:TRUE"] byte for byte on all 40 personas; the BELIEVED states rendered at
     SLOT_CAP = 15 reproduce the committed BELIEVED text on all 661 items (the S2-U lock).
  C  the section C.1 census -- the two-channel entry map on Mem0 and A-MEM: mapped counts,
     channel split, index size, the descriptive ambiguity rates pinned in the registration, and
     the FROZEN slot_key ambiguity rate (ruling #3; computed here, ledgered under
     AUX-SIDE-S1-AMBIG-*); the Mem0 lexical-required fallback census (4,809 / 0.4939, ruling #2).
  D  the section C.2 gates -- names per item on the committed texts through NB-6's parser
     reproduce results/nb6.json (TRUE 1.7473524962, BELIEVED 15.0378214826) to 1e-9; the BR-A /
     BR-B table values as frozen.
  E  populations and positives (238 / 284 / 661; 94 / 126 / 104), committed row counts
     (elicitation_main.json BLIND 332, INDEXED-TRUE 1,183, INDEXED-BELIEVED 1,183).
  F  ledger keys already written (AUX-SIDE-S1-SPOTCHECK-*, -MULTI-AMEM, -FALLBACK-MEM0) present.
Post-index checks (skip with a printed reason until the artifact exists):
  G  leakage rows; H every section L key present once elicitation has happened;
  I  the S1 GT indexes (side_experiments/s1/indexes_gt.json, build_s1.py) reproduced byte for byte
     by the map each backend uses, no marker, the MAP-* and INDEXSIZE ledger keys written;
  J  the S2-U indexes (side_experiments/s2/indexes_s2u.json, build_s2u.py) reproduced byte for byte
     by the frozen render at the lifted cap, no "(+N more)", the section C.2 uncapped columns, the
     S2-CENSUS and S2-CAP-RECALL ledger keys written;
  K  NB-4 / NB-5 on the GT indexes (side_experiments/s1/nb_side.json, nb_side.py): NB-4 recomputed,
     NB-5 re-scored from the per-item artifact, the four NB ledger keys written;
  L  the mini lanes (side_experiments/run/, run_side.py): every AUROC, gain, difference, verdict and
     retention re-derived from rows_side.jsonl and the committed rows with the committed estimators;
     spend under the $2 line; the MINI, H45, SPEND and BUDGETRULE keys written.
Exit 0 iff every applicable check passes; a failure prints "FAIL <check>: <detail>", exit 1
(ADDENDUM_SIDE section STOP).
"""
from __future__ import annotations

import collections
import hashlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import (ROOT, E1, SIDE, S1, LEDGER, J, THRESH, C, IX,   # noqa: E402
                         parse_dt, load_state, ages, fr_states, render_true)
from index_features import parse as nb6_parse                    # noqa: E402
import prompts_e1 as P                                           # noqa: E402

FAILS: list[str] = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


# ------------------------------------------------------------------ A. lineage
PIN = {"prompts_e1 file": "337d37d3414c04823d28ad99eeab15c34e328e60198d68625452ebf330830b84",
       "prompts_e1 texts": "35d9b968ffc0b008289a59b06f10b7d23f71658c648dd2865a46e8da15d495f2"}
PIN_FILES = {
    "e1_metamemory/tools/index_v2.py":      "baeaab11e1b5e94d38809160d6ca0ca8041c00461fe0ad4f674ccc14bf5c94a9",
    "e1r_robustness/tools/common_e1r.py":    "ab3581f5b6ec2db2d7e1849b3a86d8ac8dd1e0137e515b87a8a89126335072b6",
}
PIN_FILES["e1_metamemory/tools/two_channel.py"] = "34692413f96a0252c8f9b556a809b0b24f7583b1dd5756089bdfbb776fdea2fb"
PIN_FILES["analysis/ontology_validation/exp4_witnesses.py"] = "4e9fb054a357cfa99121789fd2bbbf7a442d7a96f834ab4b0b357b0609c203dd"


def check_lineage():
    print("A. lineage")
    check("prompts_e1 file digest", P.file_sha256() == PIN["prompts_e1 file"], P.file_sha256())
    check("prompts_e1 texts digest", P.texts_sha256() == PIN["prompts_e1 texts"], P.texts_sha256())
    for rel, want in PIN_FILES.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        check(f"source pinned: {rel}", got == want, got)
    check("two_channel threshold 0.295 unchanged", getattr(__import__("two_channel"), "THRESH", None) == THRESH)


# ------------------------------------------------------------------ B. renderer locks
def check_locks(committed, rows_by, joins):
    print("B. RENDERER LOCK")
    bad = []
    for persona in sorted(joins):
        rows, (t_sup, t_ret, t_exp, t_ev) = fr_states(joins, rows_by, persona)
        ages(rows, joins[persona].t_now)
        if render_true(rows, (t_sup, t_ret, t_exp), t_ev)[0] != committed[f"frbank:{persona}:FULL:TRUE"]:
            bad.append(persona)
    check("identity mapping reproduces frbank:<p>:FULL:TRUE on 40/40 personas", not bad, str(bad))
    # S2-U lock: BELIEVED states at SLOT_CAP = 15 reproduce the committed BELIEVED text on all 661
    cell = J(ROOT / "r74/x4/cell_661.json")["items"]
    cat_plan = J(E1 / "build/variant_plan.json")["cat_ablation"]; slot_abl = J(E1 / "build/slot_ablations.json")
    per = {}
    for persona, Jn in joins.items():
        rows = sorted(rows_by["frbank"][persona], key=lambda r: r["entry_id"]); ages(rows, Jn.t_now)
        b_sup, b_ret, b_exp, b_ev = IX.believed_lifecycle("frbank", rows, Jn.cutoff)
        per[persona] = (rows, ((b_sup, b_ret, b_exp), b_ev), set(cat_plan[persona]["categories"]))
    nbad = 0
    for it in cell:
        rows, (bst, bev), cats = per[it["persona"]]
        v = it["variant"]
        removed = (None if v == "FULL" else {r["entry_id"] for r in rows if r["category"] in cats} if v == "CAT-ABLATED"
                   else set(slot_abl[f"{it['persona']}:{it['item_id'].split(':')[2]}"]))
        txt = IX.render(IX.view(rows, bst, removed), bev, IX.AVAIL[("frbank", "BELIEVED")])[0]
        nbad += txt != committed[it["index_key"].replace(":TRUE", ":BELIEVED")]
    check("BELIEVED states at SLOT_CAP=15 reproduce the committed BELIEVED text on 661/661 items", nbad == 0, f"{nbad} differ")
    return cell, per, slot_abl


# ------------------------------------------------------------------ C. section C.1 census
PIN_C1 = {"mem0": {"n_entries": 9736, "n_mapped": 9704, "lex": 0, "emb": 4895, "both": 4809, "unmapped": 32,
                   "amb_any": 0.341, "amb_scrub": 0.2461, "amb_slotkey": 0.2920, "gt_tokens": 918.8, "fr_tokens": 1074.1, "fallback_mapped": 4809,
                   "fallback_frac": 0.4939, "fallback_amb_slotkey": 0.252},
          "amem": {"n_entries": 11319, "n_mapped": 10974, "lex": 5, "emb": 4962, "both": 6007, "unmapped": 345,
                   "amb_any": 0.474, "amb_scrub": 0.3763, "amb_slotkey": 0.4344, "gt_tokens": 931.0, "fr_tokens": 1077.1}}


MAPS = {}   # (backend, lexical_required) -> per-persona map output, kept for check I


def census_backend(b, committed, rows_by, joins, lexical_required):
    """The section C.1 census through side_common.map_backend (the loop verify_side ran at the
    freeze, moved there verbatim); every quantity below is pinned, so the move is checked here."""
    MAPS[(b, lexical_required)] = SC.map_backend(b, committed, rows_by, joins, lexical_required)
    return SC.census(MAPS[(b, lexical_required)])


def check_census(committed, rows_by, joins):
    print("C. section C.1 census (two-channel map; Mem0 fallback)")
    out = {}
    for b in ("mem0", "amem"):
        r = census_backend(b, committed, rows_by, joins, lexical_required=False); pin = PIN_C1[b]; out[b] = r
        check(f"{b} entries / mapped / channels / unmapped", (r["n_entries"], r["n_mapped"], r["lex"], r["emb"], r["both"], r["unmapped"])
              == (pin["n_entries"], pin["n_mapped"], pin["lex"], pin["emb"], pin["both"], pin["unmapped"]),
              f"{r['n_entries']} {r['n_mapped']} {r['lex']}/{r['emb']}/{r['both']} {r['unmapped']}")
        check(f"{b} descriptive ambiguity, target band: any-second {pin['amb_any']:.3f}, scrubbed-name {pin['amb_scrub']:.4f} (D-SIDE-1)",
              abs(r["amb_any"] - pin["amb_any"]) < 5e-4 and abs(r["amb_scrub"] - pin["amb_scrub"]) < 5e-4,
              f"{r['amb_any']:.4f} {r['amb_scrub']:.4f}")
        check(f"{b} GT index tokens {pin['gt_tokens']} vs FR TRUE {pin['fr_tokens']}",
              abs(r["gt_tokens"] - pin["gt_tokens"]) < 0.05 and abs(r["fr_tokens"] - pin["fr_tokens"]) < 0.05,
              f"{r['gt_tokens']:.1f} {r['fr_tokens']:.1f}")
        check(f"{b} frozen slot_key ambiguity under the two-channel map {pin['amb_slotkey']:.4f} (target band; D-SIDE-1)",
              abs(r["amb_slotkey"] - pin["amb_slotkey"]) < 5e-4, f"{r['amb_slotkey']:.4f}")
    fb = census_backend("mem0", committed, rows_by, joins, lexical_required=True); out["mem0_fallback"] = fb
    pin = PIN_C1["mem0"]
    check("Mem0 lexical-required fallback: 4,809 mapped, 0.4939", fb["n_mapped"] == pin["fallback_mapped"] and abs(fb["frac"] - pin["fallback_frac"]) < 5e-5,
          f"{fb['n_mapped']} {fb['frac']:.4f}")
    check("Mem0 fallback frozen slot_key ambiguity 0.252", abs(fb["amb_slotkey"] - pin["fallback_amb_slotkey"]) < 5e-4, f"{fb['amb_slotkey']:.4f}")
    check("Mem0 fallback below the rule (c) floor -> descriptive row", fb["frac"] < 0.50)
    return out


# ------------------------------------------------------------------ D. section C.2 gates
PIN_C2 = {"TRUE": (1.7473524962178517, 1.0, 1.0), "BELIEVED": (15.037821482602117, 0.0348, 0.2996),
          "BR-A": (15.0378, 0.0348, 0.2996), "BR-B": (8.9592, 0.0618, 0.3169)}


def rule_sets(bank, gap_days):
    pointed = collections.defaultdict(list)
    for e in bank.values():
        if e.get("supersedes") and e["supersedes"] in bank:
            pointed[e["supersedes"]].append(e["id"])
    A, B, evA, evB = set(), set(), [], []
    for fid, f in bank.items():
        if f.get("is_active") or f.get("is_retracted") or fid not in pointed:
            continue
        A.add(fid); evA.append(set(pointed[fid]))
        gs = pointed[fid]; d0 = parse_dt(f.get("created_at"))
        newest = max(gs, key=lambda g: parse_dt(bank[g].get("created_at")) or d0)
        d1 = parse_dt(bank[newest].get("created_at"))
        if bank[newest].get("is_active") and d0 and d1 and (d1 - d0).days >= gap_days:
            B.add(fid); evB.append({newest})
    return A, B, evA, evB


def check_c2(committed, cell, per, slot_abl):
    print("D. section C.2 gates (names per item; BR-A / BR-B table)")
    nb6 = J(ROOT / "e1r_robustness/results/nb6.json")["rows"]
    ref_t, ref_b = nb6["R-NOK-FRB|TRUE"]["mean_names_per_item"], nb6["R-NOK-FRB|BELIEVED"]["mean_names_per_item"]
    check("results/nb6.json anchors are the frozen values", abs(ref_t - PIN_C2["TRUE"][0]) < 1e-9 and abs(ref_b - PIN_C2["BELIEVED"][0]) < 1e-9)
    acc = {k: collections.Counter() for k in PIN_C2}
    rules = {}
    for persona, (rows, (bst, bev), cats) in per.items():
        bank = {e["id"]: e for e in J(C.BANKS / f"{persona}.json")["entries"]}
        A, B, evA, evB = rule_sets(bank, C.EXPIRY_WINDOW.days)
        rules[persona] = {"BR-A": ((A, bst[1], bst[2]), evA), "BR-B": ((B, bst[1], bst[2]), evB)}
    names = lambda t: (list(nb6_parse(t)["superseded_attrs"]) if nb6_parse(t)["expressible"] else [])  # noqa: E731
    for it in cell:
        rows, (bst, bev), cats = per[it["persona"]]; v = it["variant"]
        removed = (None if v == "FULL" else {r["entry_id"] for r in rows if r["category"] in cats} if v == "CAT-ABLATED"
                   else set(slot_abl[f"{it['persona']}:{it['item_id'].split(':')[2]}"]))
        T = set(names(committed[it["index_key"]]))
        texts = {"TRUE": committed[it["index_key"]], "BELIEVED": committed[it["index_key"].replace(":TRUE", ":BELIEVED")]}
        for k in ("BR-A", "BR-B"):
            st, ev = rules[it["persona"]][k]
            texts[k] = IX.render(IX.view(rows, st, removed), ev, IX.AVAIL[("frbank", "BELIEVED")])[0]
        for k, t in texts.items():
            R = set(names(t)) if k != "TRUE" else T
            acc[k]["names"] += len(names(t)); acc[k]["inter"] += len(R & T); acc[k]["R"] += len(R); acc[k]["T"] += len(T)
    n = len(cell)
    for k, (pn, pp, pr) in PIN_C2.items():
        a = acc[k]; npi = a["names"] / n; prec = a["inter"] / a["R"] if a["R"] else 1.0; rec = a["inter"] / a["T"]
        tol = 1e-9 if k in ("TRUE", "BELIEVED") else 5e-5
        check(f"{k}: names/item {pn}, P {pp}, R {pr}", abs(npi - pn) < tol and abs(prec - pp) < 5e-5 and abs(rec - pr) < 5e-5,
              f"{npi:.10f} {prec:.4f} {rec:.4f}")


# ------------------------------------------------------------------ E. populations and rows
def check_populations():
    print("E. populations, positives, committed rows")
    items = J(E1 / "build/items_final.json")
    for b, n, pos in (("mem0", 238, 94), ("amem", 284, 126)):
        sc = [i for i in items if i["backend"] == b and i["label"] in ("PRESENT", "ABSENT")]
        check(f"{b} FOK population {n} with {pos} positives", (len(sc), sum(1 for i in sc if i["label"] == "PRESENT")) == (n, pos),
              f"{len(sc)} {sum(1 for i in sc if i['label'] == 'PRESENT')}")
    cell = J(ROOT / "r74/x4/cell_661.json")["items"]
    check("obligation population 661 with 104 PN", (len(cell), sum(i["y_nok"] for i in cell)) == (661, 104))
    main = J(E1 / "elicitation_main.json")
    c = collections.Counter(r["arm"] for r in main if r["status"] == "OK")
    check("elicitation_main.json BLIND 332 / INDEXED-TRUE 1,183 / INDEXED-BELIEVED 1,183",
          (c["BLIND"], c["INDEXED-TRUE"], c["INDEXED-BELIEVED"]) == (332, 1183, 1183), str(dict(c)))


# ------------------------------------------------------------------ F-H. ledger
KEYS_L = ["S1-MAP-MEM0", "S1-MAP-AMEM", "S1-AMBIG-MEM0", "S1-AMBIG-AMEM", "S1-AMBIG-ANY-MEM0", "S1-AMBIG-ANY-AMEM",
          "S1-INDEXSIZE", "S1-SPOTCHECK-MEM0", "S1-SPOTCHECK-AMEM", "S1-MULTI-AMEM", "S1-FALLBACK-MEM0",
          "S1-FALLBACK-AMEM", "S1-LEAK-MEM0", "S1-LEAK-AMEM", "S1-MINI-MEM0", "S1-MINI-AMEM", "S1-NB4-MEM0",
          "S1-NB4-AMEM", "S1-NB5-MEM0", "S1-NB5-AMEM", "S1-H45", "S2-CENSUS", "S2-CAP-RECALL", "S2-LEAK", "S2-MINI",
          "SPEND", "BUDGETRULE"]
WRITTEN = ["S1-SPOTCHECK-MEM0", "S1-SPOTCHECK-AMEM", "S1-MULTI-AMEM", "S1-FALLBACK-MEM0",
           "S1-AMBIG-MEM0", "S1-AMBIG-AMEM", "S1-AMBIG-ANY-MEM0", "S1-AMBIG-ANY-AMEM"]


GT_PIN = {"mem0": {"frac": 0.4939, "lines": 54.1, "tokens": 814.9, "n": 37, "lifecycle": (13, 3, 74)},
          "amem": {"frac": 0.9695, "lines": 57.8, "tokens": 931.0, "n": 40, "lifecycle": (40, 13, 123)}}


def check_gt_indexes():
    """I. SIDE-BUILD-1 step 1: side_experiments/s1/indexes_gt.json, once it exists, is reproduced byte
    for byte by the map each backend uses (Mem0 lexical-required, A-MEM two-channel), carries no
    marker and no ':' name, and its ledger keys (MAP-*, INDEXSIZE) are written with the built values."""
    print("I. S1 GT indexes (build_s1.py)")
    p = S1 / "indexes_gt.json"
    if not p.exists():
        print("  skip  no GT index exists yet (side_experiments/s1/indexes_gt.json absent)"); return
    art = J(p); idx = art["indexes"]
    check("77 GT indexes keyed <backend>:<persona>:GT (Mem0 37, A-MEM 40)",
          len(idx) == 77 and sum(k.startswith("mem0:") for k in idx) == 37 and all(k.endswith(":GT") for k in idx), str(len(idx)))
    check("meta records the map each backend uses (Mem0 lexical-required, A-MEM two-channel) and the freeze",
          art["meta"]["mapping"]["mem0"].startswith("lexical-required") and art["meta"]["mapping"]["amem"].startswith("two-channel")
          and art["meta"]["frozen"] == "e8b2630")
    check("no GT index carries the inexpressibility marker", not any(IX.MARKER in t for t in idx.values()))
    bad = []
    for b in SC.BACKENDS:
        per = MAPS[(b, SC.LEXICAL_REQUIRED[b])]
        bad += [SC.gt_key(b, q) for q, r in per.items() if idx.get(SC.gt_key(b, q)) != r["text"]]
        bad += [k for k in idx if k.startswith(b + ":") and k.split(":")[1] not in per]
        c = SC.census(per); pin = GT_PIN[b]
        check(f"{b} GT index census: {pin['n']} personas, mapped share {pin['frac']}, {pin['lines']} lines / {pin['tokens']} tokens, lifecycle {pin['lifecycle']}",
              c["n_personas"] == pin["n"] and abs(c["frac"] - pin["frac"]) < 5e-4 and abs(c["gt_lines"] - pin["lines"]) < 0.05
              and abs(c["gt_tokens"] - pin["tokens"]) < 0.05 and (c["superseded"], c["retracted"], c["expired"]) == pin["lifecycle"],
              f"{c['n_personas']} {c['frac']:.4f} {c['gt_lines']:.1f} / {c['gt_tokens']:.1f} {(c['superseded'], c['retracted'], c['expired'])}")
    check("every committed GT index is reproduced byte for byte by the map its backend uses", not bad, str(bad[:5]))
    t = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    for k in ("S1-MAP-MEM0", "S1-MAP-AMEM", "S1-INDEXSIZE"):
        check(f"AUX-SIDE-{k} written", f"**AUX-SIDE-{k}**" in t)
    check("MAP / INDEXSIZE rows carry the built values (4,809 / 0.4939; 10,974 / 0.970; 54.1 / 814.9; 57.8 / 931.0)",
          all(v in t for v in ("4,809", "0.4939", "10,974", "0.970", "54.1 lines / 814.9", "57.8 lines / 931.0")))


def check_s2u_indexes(committed, cell, per, slot_abl):
    """J. SIDE-BUILD-1 step 2: side_experiments/s2/indexes_s2u.json, once it exists, is reproduced byte
    for byte by the frozen render at the lifted cap on every item, carries no '(+N more)', no marker,
    and its rendered superseded list reproduces the section C.2 uncapped columns; ledger keys written."""
    print("J. S2-U indexes (build_s2u.py)")
    p = S1.parent / "s2" / "indexes_s2u.json"
    if not p.exists():
        print("  skip  no S2-U index exists yet (side_experiments/s2/indexes_s2u.json absent)"); return
    art = J(p); idx, items = art["indexes"], art["items"]; cap = art["meta"]["slot_cap_lifted"]
    check("S2-U: 661 items over 242 texts, keys carry :S2U, cap lifted to 100, freeze recorded",
          len(items) == 661 and len(idx) == 242 and all(k.endswith(":S2U") or ":SLOT:" in k for k in idx) and cap == 100
          and art["meta"]["frozen"] == "e8b2630")
    check("no S2-U text carries '(+N more)' or the inexpressibility marker", not any("(+" in t or IX.MARKER in t for t in idx.values()))
    bad = 0; old = IX.SLOT_CAP; IX.SLOT_CAP = cap
    names = lambda t: (list(nb6_parse(t)["superseded_attrs"]) if nb6_parse(t)["expressible"] else [])  # noqa: E731
    acc = collections.Counter()
    try:
        for it, rec in zip(cell, items):
            rows, (bst, bev), cats = per[it["persona"]]; v = it["variant"]
            removed = (None if v == "FULL" else {r["entry_id"] for r in rows if r["category"] in cats} if v == "CAT-ABLATED"
                       else set(slot_abl[f"{it['persona']}:{it['item_id'].split(':')[2]}"]))
            txt = IX.render(IX.view(rows, bst, removed), bev, IX.AVAIL[("frbank", "BELIEVED")])[0]
            bad += (rec["item_id"] != it["item_id"]) or (txt != idx.get(rec["index_key_s2u"]))
            R, T = set(names(txt)), set(names(committed[it["index_key"]]))
            acc["names"] += len(names(txt)); acc["inter"] += len(R & T); acc["R"] += len(R); acc["T"] += len(T)
    finally:
        IX.SLOT_CAP = old
    check("every S2-U item text is reproduced byte for byte by the frozen render at the lifted cap (661/661)", bad == 0, f"{bad} differ")
    npi, prec, rec_ = acc["names"] / len(cell), acc["inter"] / acc["R"], acc["inter"] / acc["T"]
    check("S2-U rendered superseded list: 32.55 names/item, P 0.0357, R 0.6658 (section C.2 uncapped columns)",
          abs(npi - 32.55) < 5e-3 and abs(prec - 0.0357) < 5e-5 and abs(rec_ - 0.6658) < 5e-5, f"{npi:.4f} {prec:.4f} {rec_:.4f}")
    t = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    for k in ("S2-CENSUS", "S2-CAP-RECALL"):
        check(f"AUX-SIDE-{k} written", f"**AUX-SIDE-{k}**" in t)
    check("S2-CAP-RECALL row carries 66.6% uncapped and 30.0% rendered", "66.6" in t and "30.0" in t and "0.6658" in t and "0.2996" in t)


def check_nb_side():
    """K. SIDE-BUILD-1 step 4: side_experiments/s1/nb_side.json, once it exists -- NB-4 recomputed from the
    committed GT indexes and populations, NB-5's AUROC recomputed from the artifact's per-item scores
    (the encoder ran in nb_side.py), the four NB ledger keys written with the artifact's values."""
    print("K. NB-4 / NB-5 on the GT indexes (nb_side.py)")
    p = S1 / "nb_side.json"
    if not p.exists():
        print("  skip  NB-4 / NB-5 have not run (side_experiments/s1/nb_side.json absent)"); return
    from common_e1r import POPULATIONS, auroc, load_e1
    from index_features import toks
    art = J(p)
    check("nb_side.json scored the committed GT index artifact", art["gt_indexes_sha256"] == hashlib.sha256((S1 / "indexes_gt.json").read_bytes()).hexdigest())
    gt = J(S1 / "indexes_gt.json")["indexes"]; items, blind, idxT, _ = load_e1()
    t = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    jac = lambda a, b: len(a & b) / len(a | b) if (a | b) else 0.0  # noqa: E731
    for b, rid in (("mem0", "R-FOK-MEM0"), ("amem", "R-FOK-AMEM")):
        spec = POPULATIONS[rid]; rows = []
        for it in items:
            if not spec["filt"](it) or it["question"] not in blind or it["item_id"] not in idxT:
                continue
            if blind[it["question"]].get("fok") is None or idxT[it["item_id"]].get("fok") is None:
                continue
            pp = nb6_parse(gt[SC.gt_key(b, it["persona"])]); attrs = [a for v in pp["attr_by_cat"].values() for a in v]
            qt = toks(it["question"])
            rows.append((it["item_id"], 0 if it.get("label", it["label_pre"]) == "ABSENT" else 1, max((jac(qt, toks(a.replace("_", " "))) for a in attrs), default=0.0)))
        r = art["rows"][b]; y = [x[1] for x in rows]
        check(f"{b}: NB-4 recomputed from the committed GT indexes equals the artifact ({r['nb4']['auroc']:.4f})",
              [x[0] for x in rows] == [i["item_id"] for i in r["items"]] and abs(auroc([x[2] for x in rows], y) - r["nb4"]["auroc"]) < 1e-9
              and all(abs(x[2] - i["nb4"]) < 1e-9 for x, i in zip(rows, r["items"])), f"{auroc([x[2] for x in rows], y):.4f}")
        check(f"{b}: NB-5 AUROC recomputed from the artifact's per-item scores ({r['nb5']['auroc']:.4f})",
              abs(auroc([i["nb5"] for i in r["items"]], [i["y"] for i in r["items"]]) - r["nb5"]["auroc"]) < 1e-9)
        for k in ("nb4", "nb5"):
            check(f"AUX-SIDE-S1-{k.upper()}-{b.upper()} written with AUROC {r[k]['auroc']:.4f}", f"**AUX-SIDE-S1-{k.upper()}-{b.upper()}** | **AUROC {r[k]['auroc']:.4f}**" in t)


def check_scores():
    """L. SIDE-BUILD-1 step 5: side_experiments/run/scores_side.json, once it exists -- every AUROC, gain,
    difference, verdict and retention re-derived from rows_side.jsonl and the committed rows with the
    committed estimators; the lane and lineage recorded; the MINI, H45, SPEND and BUDGETRULE keys
    written with the artifact's values; spend under the $2 line."""
    print("L. the mini lanes (run_side.py)")
    RUN = SIDE / "run"; p = RUN / "scores_side.json"
    if not p.exists():
        print("  skip  no elicitation has happened (side_experiments/run/scores_side.json absent)"); return
    import json
    from common_e1r import auroc, boot_item, boot_cluster, load_e1
    S = J(p); m = S["meta"]
    check("lane and lineage recorded: gpt-4.1-mini, temperature 0, seed 42, max_tokens 200, k 1, prompts digests as frozen, index digests as committed",
          (m["lane"], m["temperature"], m["seed"], m["max_tokens"], m["k"]) == ("gpt-4.1-mini", 0, 42, 200, 1)
          and m["prompts_file_sha256"] == PIN["prompts_e1 file"] and m["prompts_texts_sha256"] == PIN["prompts_e1 texts"]
          and m["gt_indexes_sha256"] == hashlib.sha256((S1 / "indexes_gt.json").read_bytes()).hexdigest()
          and m["s2u_indexes_sha256"] == hashlib.sha256((SIDE / "s2" / "indexes_s2u.json").read_bytes()).hexdigest())
    rows = [json.loads(l) for l in (RUN / "rows_side.jsonl").open(encoding="utf-8")]
    new = {}
    for r in rows:
        if r["status"] == "OK":
            new[(r["arm"], r["item_id"])] = r
    check("1,183 rows, one per item and arm, all OK, no Haiku or Opus row",
          len(rows) == 1183 and len(new) == 1183 and sum(r["arm"] == "INDEXED-GT" for r in rows) == 522 and sum(r["arm"] == "INDEXED-S2U" for r in rows) == 661
          and S["rows"]["INDEXED-GT"]["failed"] == 0 and S["rows"]["INDEXED-S2U"]["failed"] == 0, f"{len(rows)} {len(new)}")
    cell = J(RUN / "cell_side.json")["cell"]; items, blind, idxT, idxB = load_e1()
    for b in ("amem", "mem0"):
        rs = cell["s1"][b]; y = [r["y_fok"] for r in rs]; g = [r["persona"] for r in rs]
        bl = [blind[r["question"]]["fok"] for r in rs]; tr = [idxT[r["item_id"]]["fok"] for r in rs]; gt = [new[("INDEXED-GT", r["item_id"])]["fok"] for r in rs]
        a = S["S1"][b]; A = a["auroc"]
        X, Y = auroc(tr, y) - auroc(bl, y), auroc(gt, y) - auroc(bl, y); D = Y - X
        di, dc, yi = boot_item(tr, gt, y), boot_cluster(tr, gt, y, g), boot_item(bl, gt, y)
        check(f"{b}: blind / TRUE / GT AUROC, X, Y, D and the intervals re-derived ({A['blind']:.4f} / {A['true']:.4f} / {A['gt']:.4f}; D {D:+.4f} {'[%+.4f, %+.4f]' % (di['ci_lo'], di['ci_hi'])})",
              abs(auroc(bl, y) - A["blind"]) < 1e-9 and abs(auroc(tr, y) - A["true"]) < 1e-9 and abs(auroc(gt, y) - A["gt"]) < 1e-9
              and abs(D - a["difference_D"]) < 1e-9 and abs(di["ci_lo"] - a["D_interval_item"]["ci_lo"]) < 1e-9 and abs(dc["ci_hi"] - a["D_interval_clustered"]["ci_hi"]) < 1e-9
              and abs(yi["ci_lo"] - a["Y_interval_item"]["ci_lo"]) < 1e-9)
        if b == "amem":
            p1 = D > 0.05 and di["ci_lo"] > 0 and dc["ci_lo"] > 0; p2 = yi["ci_hi"] >= 0 and a["Y_interval_clustered"]["ci_hi"] >= 0
            check(f"A-MEM verdicts re-derived: S1-P1 {'HOLDS' if p1 else 'FAILS'}, S1-P2 {'HOLDS' if p2 else 'FAILS'}", p1 == a["S1-P1"]["holds"] and p2 == a["S1-P2"]["holds"])
    rs = cell["s2u"]; y = [r["y_nok"] for r in rs]; g = [r["persona"] for r in rs]
    bl = [blind[r["question"]]["nok"] for r in rs]; tr = [idxT[r["item_id"]]["nok"] for r in rs]; be = [idxB[r["item_id"]]["nok"] for r in rs]
    su = [new[("INDEXED-S2U", r["item_id"])]["nok"] for r in rs]; u = S["S2U"]; A = u["auroc"]
    ret = (auroc(su, y) - auroc(bl, y)) / (auroc(tr, y) - auroc(bl, y)); ret_b = (auroc(be, y) - auroc(bl, y)) / (auroc(tr, y) - auroc(bl, y))
    check(f"S2-U: blind / TRUE / BELIEVED / S2-U NOK AUROC and retention re-derived ({A['blind']:.4f} / {A['true']:.4f} / {A['believed']:.4f} / {A['s2u']:.4f}; retention {100 * ret:.1f}%, committed BELIEVED {100 * ret_b:.1f}%)",
          all(abs(auroc(v, y) - A[k]) < 1e-9 for v, k in ((bl, "blind"), (tr, "true"), (be, "believed"), (su, "s2u")))
          and abs(ret - u["retention_s2u"]) < 1e-9 and abs(ret_b - 0.4231) < 5e-4
          and abs(boot_item(bl, su, y)["ci_lo"] - u["s2u_gain_interval_item"]["ci_lo"]) < 1e-9 and abs(boot_item(be, su, y)["ci_lo"] - u["s2u_minus_believed_item"]["ci_lo"]) < 1e-9)
    check("S2-U branch follows the retention against the 60% line", u["branch"] == ("retention reaches 60% (not expected)" if ret >= 0.60 else "retention stays short of 60% (expected)"))
    sp = S["spend"]; leak = J(SIDE / "leak" / "leak_side.json")["cost"]["usd_with_probe"]
    check(f"spend re-derived: ${sp['total']:.4f} = leakage + probes + rows, under the $2 line",
          abs(sp["leakage_screens"] - leak) < 1e-9 and abs(sp["run"] - sum(r["usd"] for r in rows)) < 1e-9 and sp["total"] < 2.0)
    t = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    a = S["S1"]["amem"]
    check("MINI-AMEM row carries the AUROC triple and both verdicts",
          f"blind {a['auroc']['blind']:.4f}, INDEXED-TRUE {a['auroc']['true']:.4f}, INDEXED-GT {a['auroc']['gt']:.4f}" in t
          and f"**S1-P1 {'HOLDS' if a['S1-P1']['holds'] else 'FAILS'}**" in t and f"**S1-P2 {'HOLDS' if a['S1-P2']['holds'] else 'FAILS'}**" in t)
    check("MINI-MEM0 row carries the AUROC triple", f"INDEXED-GT {S['S1']['mem0']['auroc']['gt']:.4f}" in t and "**AUX-SIDE-S1-MINI-MEM0**" in t)
    check("S2-MINI row carries the retention and the branch", f"= {100 * u['retention_s2u']:.1f}%" in t and f"**Branch: {u['branch']}.**" in t)
    check("SPEND and BUDGETRULE rows carry the billed total", f"**${sp['total']:.4f} billed**" in t and "**AUX-SIDE-BUDGETRULE** | " in t and "**Held**" in t)
    check("H45 carries a dash with the October reason", "**AUX-SIDE-S1-H45** | — " in t and "October" in t)


def check_ledger():
    print("F. ledger keys already written")
    t = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
    check("NUMBERS_SIDE.md exists and names the frozen registration", "registrations/ADDENDUM_SIDE.md" in t)
    for k in WRITTEN:
        check(f"AUX-SIDE-{k} present", f"AUX-SIDE-{k}" in t)
    check("spot-check values as ruled (17/30, 0.567; 24/30, 0.800)", "17 / 30 correct, precision 0.567" in t and "24 / 30 correct, precision 0.800" in t)
    check("fallback figure 0.4939 ledgered", "0.4939" in t)
    check("AMBIG keys carry 0.252 (Mem0, lexical-required) and 0.4344 (A-MEM); D-SIDE-1 recorded",
          "**0.252**" in t and "**0.4344**" in t and (SIDE / "DEVIATIONS_SIDE.md").exists() and "D-SIDE-1" in (SIDE / "DEVIATIONS_SIDE.md").read_text(encoding="utf-8"))
    print("G. leakage rows")
    lp = SIDE / "leak" / "leak_side.json"
    if not lp.exists():
        print("  skip  no leakage screen has run (side_experiments/leak/leak_side.json absent)")
    else:
        L = J(lp); cells = L["cells"]
        check("leakage screen: three cells of 30, threshold 3, ladder level 0, prompts digests as frozen",
              set(cells) == {"mem0:GT", "amem:GT", "frbank:S2U"} and all(c["n"] == 30 and len(c["rows"]) == 30 and c["threshold"] == 3 for c in cells.values())
              and L["prompts_file_sha256"] == PIN["prompts_e1 file"] and L["prompts_texts_sha256"] == PIN["prompts_e1 texts"])
        check("no cell above 3 of 30 (section STOP)", all(c["n_correct"] <= 3 for c in cells.values()), str({k: c["n_correct"] for k, c in cells.items()}))
        lad = J(E1 / "ladder_L0.json")["cells"]
        check("each cell's 30 items are the committed screen's (ladder_L0.json)",
              all([r["item_id"] for r in cells[k]["rows"]] == [r["item_id"] for r in lad[f"{k.split(':')[0]}:TRUE"]["rows"]] for k in cells))
        check("screened index digests are the committed artifacts'",
              L["gt_indexes_sha256"] == hashlib.sha256((S1 / "indexes_gt.json").read_bytes()).hexdigest()
              and L["s2u_indexes_sha256"] == hashlib.sha256((SIDE / "s2" / "indexes_s2u.json").read_bytes()).hexdigest())
        for k, cell in (("S1-LEAK-MEM0", "mem0:GT"), ("S1-LEAK-AMEM", "amem:GT"), ("S2-LEAK", "frbank:S2U")):
            check(f"AUX-SIDE-{k} present with {cells[cell]['n_correct']} / 30", f"**AUX-SIDE-{k}** | **{cells[cell]['n_correct']} / 30 correct" in t)
    print("H. every section L key")
    if "**AUX-SIDE-SPEND**" not in t:
        print("  skip  no elicitation has happened (AUX-SIDE-SPEND not written)")
    else:
        missing = [k for k in KEYS_L if f"**AUX-SIDE-{k}**" not in t and f"AUX-SIDE-{k} (descriptive)" not in t]
        check("every section L key present", not missing, str(missing))


def main():
    print("verify_side -- ADDENDUM_SIDE.md (frozen e8b2630)")
    check_lineage()
    committed, rows_by, joins = load_state()
    cell, per, slot_abl = check_locks(committed, rows_by, joins)
    check_census(committed, rows_by, joins)
    check_c2(committed, cell, per, slot_abl)
    check_populations()
    check_ledger()
    check_gt_indexes()
    check_s2u_indexes(committed, cell, per, slot_abl)
    check_nb_side()
    check_scores()
    print()
    if FAILS:
        print(f"verify_side: {len(FAILS)} FAIL -- STOP (ADDENDUM_SIDE section STOP)")
        for f in FAILS:
            print("  " + f)
        return 1
    print("verify_side: PASS (all applicable checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
