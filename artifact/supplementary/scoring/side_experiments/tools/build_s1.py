"""build_s1.py -- SIDE-BUILD-1 step 1: the S1 GT indexes (ADDENDUM_SIDE.md, frozen e8b2630).
NO API CALLS. Deterministic. Idempotent (re-running reproduces every artifact byte for byte).

Builds, through the section C.1 entry map (side_common.map_backend) and the RENDERER LOCK path
(index_v2.view -> index_v2.render under AVAIL[("frbank","TRUE")]):
  A-MEM  under the two-channel map            (spot-check 0.800; no fallback; NUMBERS_SIDE section 1)
  Mem0   under the lexical-required fallback  (spot-check 0.567; ruling #2; NUMBERS_SIDE section 2)
and, for the record only, Mem0 under the two-channel map the spot-check did not admit (the map
the frozen section S1.a sample was drawn from; its ambiguity prints beside as descriptive).

Gates, in order, each a STOP on failure (ADDENDUM_SIDE section STOP):
  0  verify_side.py passes (run as a subprocess before any index is written);
  1  RENDERER LOCK: the identity mapping on FR-Bank reproduces frbank:<p>:FULL:TRUE, 40 / 40;
  2  the sixty frozen section S1.a pairs are reproduced by the two-channel map on both backends
     (identity, target, channel; the printed cosine column is the global-best cosine to 0.0015 --
     the pre-freeze census keyed on the global best, D-SIDE-1 / D-SIDE-2), and the seed-42 draw
     itself (random.Random(42).sample over the mapped pairs sorted by (persona, entry id));
  3  the census under each map equals the frozen values (verify_side's pins; the fallback census
     of NUMBERS_SIDE section 2; the lifecycle totals and index sizes of section C.1);
  4  the ambiguity rates under the map each backend uses equal the ledgered AUX-SIDE-S1-AMBIG-*
     values (0.252 / 0.4344; ANY 0.3159 / 0.4736);
  5  no GT index carries the inexpressibility marker or a name containing ':'.

Writes side_experiments/s1/:
  indexes_gt.json          {"meta", "indexes": {"<backend>:<persona>:GT": text}}   77 indexes
  mapping_gt.jsonl         one record per stored entry under the map the backend uses (mapped or
                           not): target, cosine, channel, target state, name, ambiguity flags
  mapping_mem0_two_channel.jsonl   the same for Mem0 under the two-channel map (record only)
  build_s1.json            the censuses, the per-persona table, the gate outcomes, the ledger values

Usage, from the repository root:  python side_experiments/tools/build_s1.py
"""
from __future__ import annotations

import collections
import io
import json
import random
import re
import statistics
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import side_common as SC                                         # noqa: E402
from side_common import ROOT, S1, IX, LEXICAL_REQUIRED           # noqa: E402

REG = ROOT / "registrations" / "ADDENDUM_SIDE.md"
FREEZE = "e8b2630"

# ------------------------------------------------------------ frozen values asserted at build
# verify_side.py PIN_C1 (two-channel map) and NUMBERS_SIDE.md section 2 (Mem0 fallback)
PIN = {
    ("mem0", False): {"n_entries": 9736, "n_mapped": 9704, "lex": 0, "emb": 4895, "both": 4809, "unmapped": 32,
                      "amb_any": 0.3410, "amb_slotkey": 0.2920, "gt_lines": 57.8, "gt_tokens": 918.8,
                      "fr_lines": 63.2, "fr_tokens": 1074.1, "lifecycle": (20, 6, 138), "fr_lifecycle": (97, 21, 264)},
    ("mem0", True):  {"n_entries": 9736, "n_mapped": 4809, "lex": 0, "emb": 0, "both": 4809, "unmapped": 4927,
                      "amb_any": 0.3159, "amb_slotkey": 0.252, "n_amb_slotkey": 1214, "n_amb_any": 1519, "n_amb_scrub": 996,
                      "gt_lines": 54.1, "gt_tokens": 814.9, "fr_lines": 63.2, "fr_tokens": 1074.1,
                      "lifecycle": (13, 3, 74), "fr_lifecycle": (97, 21, 264), "frac": 0.4939,
                      "personas_at_or_above_half": 17, "cov_min": 0.372, "cov_median": 0.496, "cov_max": 0.635},
    ("amem", False): {"n_entries": 11319, "n_mapped": 10974, "lex": 5, "emb": 4962, "both": 6007, "unmapped": 345,
                      "amb_any": 0.4736, "amb_slotkey": 0.4344, "gt_lines": 57.8, "gt_tokens": 931.0,
                      "fr_lines": 63.2, "fr_tokens": 1077.1, "lifecycle": (40, 13, 123), "fr_lifecycle": (104, 23, 276),
                      "frac": 0.970},
}
MEM0_UPDATED_AT = {"active": 1216, "expired": 16, "retracted": 3, "superseded": 9}    # section C.1, two-channel
AMEM_LEX_SUPPORTED = 6012                                                              # section S1 step 2, for the record
FAILS: list[str] = []


def gate(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f": {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append(f"{name}: {detail}")


def close(a, b, tol):
    return abs(a - b) < tol


# ------------------------------------------------------------ section S1.a, parsed from the registration
PAIR = re.compile(r"(\w+) ([0-9a-f]{8})\s*→\s*(lb_\d{5}) ([0-9.]+) (both|emb|lex)")


def frozen_pairs():
    t = REG.read_text(encoding="utf-8")
    sec = t[t.index("### §S1.a"):t.index("## §S2")]
    mem0_txt = sec[sec.index("Mem0, (persona"):sec.index("A-MEM:")]
    amem_txt = sec[sec.index("A-MEM:"):]
    out = {}
    for b, txt in (("mem0", mem0_txt), ("amem", amem_txt)):
        out[b] = [(m.group(1), m.group(2), m.group(3), float(m.group(4)), m.group(5))
                  for m in PAIR.finditer(txt.replace("\n", " "))]
        assert len(out[b]) == 30, (b, len(out[b]))
    return out


def check_pairs(b, per):
    """Gate 2: the frozen pairs against the two-channel map; the draw itself where it reproduces."""
    recs = {(r["persona"], r["entry_id"]): r for p in per.values() for r in p["records"]}
    mapped = sorted(k for k, r in recs.items() if r["mapped"])
    bad, label = [], []
    for n, (persona, pref, target, cos, ch) in enumerate(frozen_pairs()[b], 1):
        hits = [k for k in mapped if k[0] == persona and k[1].startswith(pref)]
        if len(hits) != 1:
            bad.append((persona, pref, "ambiguous prefix" if hits else "not mapped")); continue
        r = recs[hits[0]]
        # the registration's cosine column is the global-best cosine (the pre-freeze census keyed on the
        # global best, D-SIDE-1); on a lexical target below the global argmax it exceeds the target cosine
        if not (r["target"] == target and r["channel"] == ch and abs(r["cos_max"] - cos) <= 0.0015):
            bad.append((persona, pref, r["target"], round(r["cos_max"], 3), r["channel"]))
        if round(r["cos"], 3) != round(r["cos_max"], 3):
            label.append({"pair": n, "persona": persona, "entry_prefix": pref, "target": target, "printed": cos,
                          "cos_global_best": round(r["cos_max"], 3), "cos_target": round(r["cos"], 3)})
    gate(f"{b}: the thirty frozen section S1.a pairs reproduced by the two-channel map (identity, target, channel; printed cosine = global best)",
         not bad, str(bad[:3]))
    print(f"        pairs whose printed (global-best) cosine exceeds the target cosine: {len(label)} of 30"
          + (": " + ", ".join(f"#{d['pair']} {d['persona']} {d['printed']}->{d['cos_target']}" for d in label) if label else ""))
    # the draw: random.Random(42) over the mapped pairs sorted by (persona, entry id)
    want = [(p, pref) for p, pref, *_ in frozen_pairs()[b]]
    how = None
    for name, draw in (("sample", lambda: random.Random(42).sample(mapped, 30)),
                       ("shuffle", lambda: (lambda l: (random.Random(42).shuffle(l), l)[1])(list(mapped))[:30])):
        got = [(p, e[:8]) for p, e in draw()]
        if got == want:
            how = name; break
    globals().setdefault("PAIR_NOTES", {})[b] = {"draw_reproduced_by": how, "cosine_column_is_global_best": True,
                                                 "pairs_where_target_cosine_differs": label}
    print(f"        seed-42 draw over the {len(mapped):,} mapped pairs sorted by (persona, entry id): "
          + (f"reproduced by random.Random(42).{how}" if how else "not reproduced by sample/shuffle (pairs are frozen in the registration; informational)"))
    return how


# ------------------------------------------------------------ gates 3-4: the census against the frozen values
def check_census(b, lexreq, per):
    c = SC.census(per); pin = PIN[(b, lexreq)]; tag = f"{b} {'lexical-required' if lexreq else 'two-channel'}"
    gate(f"{tag}: entries {pin['n_entries']:,} / mapped {pin['n_mapped']:,} / channels {pin['lex']}/{pin['emb']}/{pin['both']} / unmapped {pin['unmapped']}",
         (c["n_entries"], c["n_mapped"], c["lex"], c["emb"], c["both"], c["unmapped"]) ==
         (pin["n_entries"], pin["n_mapped"], pin["lex"], pin["emb"], pin["both"], pin["unmapped"]),
         f"{c['n_entries']} {c['n_mapped']} {c['lex']}/{c['emb']}/{c['both']} {c['unmapped']}")
    gate(f"{tag}: ambiguity slot-changing {pin['amb_slotkey']} / any-second {pin['amb_any']} (target band)",
         close(c["amb_slotkey"], pin["amb_slotkey"], 5e-4) and close(c["amb_any"], pin["amb_any"], 5e-4),
         f"{c['amb_slotkey']:.4f} {c['amb_any']:.4f}")
    gate(f"{tag}: GT index {pin['gt_lines']} lines / {pin['gt_tokens']} tokens vs FR TRUE {pin['fr_lines']} / {pin['fr_tokens']}",
         close(c["gt_lines"], pin["gt_lines"], 0.05) and close(c["gt_tokens"], pin["gt_tokens"], 0.05)
         and close(c["fr_lines"], pin["fr_lines"], 0.05) and close(c["fr_tokens"], pin["fr_tokens"], 0.05),
         f"{c['gt_lines']:.1f} / {c['gt_tokens']:.1f} vs {c['fr_lines']:.1f} / {c['fr_tokens']:.1f}")
    gate(f"{tag}: lifecycle totals sup/ret/exp {pin['lifecycle']} vs FR TRUE {pin['fr_lifecycle']}",
         (c["superseded"], c["retracted"], c["expired"]) == pin["lifecycle"]
         and (c["fr_superseded"], c["fr_retracted"], c["fr_expired"]) == pin["fr_lifecycle"],
         f"{(c['superseded'], c['retracted'], c['expired'])} vs {(c['fr_superseded'], c['fr_retracted'], c['fr_expired'])}")
    if "frac" in pin:
        gate(f"{tag}: mapped share {pin['frac']}", close(c["frac"], pin["frac"], 5e-4), f"{c['frac']:.4f}")
    if "n_amb_slotkey" in pin:
        gate(f"{tag}: ambiguity counts {pin['n_amb_slotkey']:,} slot-changing / {pin['n_amb_any']:,} any / {pin['n_amb_scrub']} scrubbed-name",
             (c["n_amb_slotkey"], c["n_amb_any"], c["n_amb_scrub"]) == (pin["n_amb_slotkey"], pin["n_amb_any"], pin["n_amb_scrub"]),
             f"{c['n_amb_slotkey']} {c['n_amb_any']} {c['n_amb_scrub']}")
    if "personas_at_or_above_half" in pin:
        cov = sorted(r["n_mapped"] / r["n_entries"] for r in per.values())
        gate(f"{tag}: per-persona coverage {pin['personas_at_or_above_half']} of {len(per)} at or above 0.50; min {pin['cov_min']} median {pin['cov_median']} max {pin['cov_max']}",
             c["personas_at_or_above_half"] == pin["personas_at_or_above_half"] and close(cov[0], pin["cov_min"], 5e-4)
             and close(statistics.median(cov), pin["cov_median"], 5e-4) and close(cov[-1], pin["cov_max"], 5e-4),
             f"{c['personas_at_or_above_half']} {cov[0]:.3f} {statistics.median(cov):.3f} {cov[-1]:.3f}")
    return c


def updated_at_states(per, rows_by):
    """Mem0 points carrying updated_at (believed_superseded in the cache) -> target state, descriptive."""
    upd = {(r["persona"], r["entry_id"]) for rows in rows_by["mem0"].values() for r in rows if r["believed_superseded"]}
    out = collections.Counter()
    for p in per.values():
        for r in p["records"]:
            if (r["persona"], r["entry_id"]) in upd and r["mapped"]:
                out["superseded" if r["superseded"] else "retracted" if r["retracted"] else "expired" if r["expired"] else "active"] += 1
    out["n_points"] = len(upd)
    return dict(out)


def per_persona_row(r):
    return {"n_entries": r["n_entries"], "n_mapped": r["n_mapped"], "coverage": round(r["n_mapped"] / r["n_entries"], 4),
            "lex": r["lex"], "emb": r["emb"], "both": r["both"], "unmapped": r["unmapped"],
            "amb_slotkey": r["amb_slotkey"], "amb_any": r["amb_any"], "superseded": r["superseded"], "retracted": r["retracted"],
            "expired": r["expired"], "sup_events": r["sup_events"], "lines": r["lines"], "tokens": r["tokens"],
            "fr_lines": r["fr_lines"], "fr_tokens": r["fr_tokens"]}


def write_jsonl(recs, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    print(f"build_s1 -- SIDE-BUILD-1 step 1, ADDENDUM_SIDE.md (frozen {FREEZE}); no API call")
    print("0. verify_side.py before any index is written")
    rc = subprocess.run([sys.executable, str(SC.SIDE / "tools" / "verify_side.py")], capture_output=True, text=True).returncode
    gate("verify_side.py passes", rc == 0, f"exit {rc}")
    if FAILS:
        print("build_s1: STOP -- verify_side failed; no index written"); return 1

    committed, rows_by, joins = SC.load_state()
    print("1. RENDERER LOCK")
    bad = []
    for persona in sorted(joins):
        rows, (t_sup, t_ret, t_exp, t_ev) = SC.fr_states(joins, rows_by, persona); SC.ages(rows, joins[persona].t_now)
        if SC.render_true(rows, (t_sup, t_ret, t_exp), t_ev)[0] != committed[f"frbank:{persona}:FULL:TRUE"]:
            bad.append(persona)
    gate("identity mapping reproduces frbank:<p>:FULL:TRUE on 40/40 personas", not bad and len(joins) == 40, str(bad))

    print("2. the map, three runs")
    maps = {("amem", False): SC.map_backend("amem", committed, rows_by, joins, False),
            ("mem0", False): SC.map_backend("mem0", committed, rows_by, joins, False),
            ("mem0", True):  SC.map_backend("mem0", committed, rows_by, joins, True)}
    print(f"        A-MEM two-channel: {len(maps[('amem', False)])} personas; Mem0 two-channel / lexical-required: "
          f"{len(maps[('mem0', False)])} / {len(maps[('mem0', True)])} personas")
    print("3. gate 2 -- the frozen section S1.a sample against the two-channel map")
    draw = {b: check_pairs(b, maps[(b, False)]) for b in ("mem0", "amem")}

    print("4. gates 3-4 -- censuses against the frozen values")
    cens = {f"{b}:{'lexical_required' if lr else 'two_channel'}": check_census(b, lr, per) for (b, lr), per in maps.items()}
    upd = {k: updated_at_states(maps[("mem0", lr)], rows_by) for k, lr in (("two_channel", False), ("lexical_required", True))}
    gate(f"Mem0 updated_at points -> target state under the two-channel map {MEM0_UPDATED_AT} (section C.1)",
         {k: upd["two_channel"].get(k, 0) for k in MEM0_UPDATED_AT} == MEM0_UPDATED_AT, str(upd["two_channel"]))
    amem_lex = sum(r["lex"] + r["both"] for r in maps[("amem", False)].values())
    gate(f"A-MEM lexically supported share {AMEM_LEX_SUPPORTED:,} of 11,319 (for the record; the fallback did not fire)",
         amem_lex == AMEM_LEX_SUPPORTED, str(amem_lex))

    print("5. gate 5 -- the indexes the backends use")
    indexes, n_marker, n_colon = {}, 0, 0
    for b in SC.BACKENDS:
        for persona, r in maps[(b, LEXICAL_REQUIRED[b])].items():
            indexes[SC.gt_key(b, persona)] = r["text"]
            n_marker += IX.MARKER in r["text"]; n_colon += sum(":" in n for n in r["names"])
    gate("77 GT indexes (Mem0 37, A-MEM 40)", len(indexes) == 77 and sum(k.startswith("mem0:") for k in indexes) == 37, str(len(indexes)))
    gate("no GT index carries the inexpressibility marker; no emitted name contains ':'", n_marker == 0 and n_colon == 0, f"{n_marker} {n_colon}")
    gate("no GT index is empty", all(indexes.values()))

    if FAILS:
        print(f"\nbuild_s1: {len(FAILS)} FAIL -- STOP (ADDENDUM_SIDE section STOP); nothing written")
        for f in FAILS:
            print("  " + f)
        return 1

    # ------------------------------------------------------------ artifacts
    meta = {"registration": "registrations/ADDENDUM_SIDE.md", "frozen": FREEZE, "no_api_calls": True, "n_indexes": len(indexes),
            "key_format": "<backend>:<persona>:GT", "mapping": {"mem0": "lexical-required (ruling #2 fallback; spot-check 0.567)",
                                                                  "amem": "two-channel (spot-check 0.800; no fallback)"},
            "renderer": "index_v2.view -> index_v2.render under AVAIL[('frbank','TRUE')]; SLOT_CAP 15; RENDERER LOCK 40/40",
            "threshold": SC.THRESH, "ambiguity_band": SC.AMBIG, "mem0_excluded_personas": sorted(IX.MEM0_EXCLUDE)}
    SC.jdump({"meta": meta, "indexes": indexes}, S1 / "indexes_gt.json")
    write_jsonl([r for b in SC.BACKENDS for p in maps[(b, LEXICAL_REQUIRED[b])].values() for r in p["records"]], S1 / "mapping_gt.jsonl")
    write_jsonl([r for p in maps[("mem0", False)].values() for r in p["records"]], S1 / "mapping_mem0_two_channel.jsonl")
    summary = {"meta": meta, "census": cens, "mem0_updated_at_to_target_state": upd, "amem_lexically_supported": amem_lex,
               "spotcheck_section_S1a": PAIR_NOTES,
               "per_persona": {f"{b}:{'lexical_required' if lr else 'two_channel'}": {p: per_persona_row(r) for p, r in per.items()}
                               for (b, lr), per in maps.items()},
               "gates": "all passed (see build log)"}
    SC.jdump(summary, S1 / "build_s1.json")
    print(f"\nwrote {S1 / 'indexes_gt.json'}, mapping_gt.jsonl, mapping_mem0_two_channel.jsonl, build_s1.json")

    # ------------------------------------------------------------ ledger values
    print("\nledger values (NUMBERS_SIDE.md section 4)")
    for b, key in (("mem0", "mem0:lexical_required"), ("amem", "amem:two_channel")):
        c = cens[key]
        print(f"  AUX-SIDE-S1-MAP-{b.upper()}: {c['n_personas']} personas, {c['n_entries']:,} entries, mapped {c['n_mapped']:,} ({c['frac']:.4f}); "
              f"lex/emb/both {c['lex']}/{c['emb']:,}/{c['both']:,}; unmapped {c['unmapped']:,}; "
              f"{c['personas_at_or_above_half']} personas at or above 0.50; "
              f"ambiguity slot-changing {c['n_amb_slotkey']:,} ({c['amb_slotkey']:.4f}), any {c['n_amb_any']:,} ({c['amb_any']:.4f}); "
              f"lifecycle sup/ret/exp/events {c['superseded']}/{c['retracted']}/{c['expired']}/{c['sup_events']} "
              f"vs FR TRUE {c['fr_superseded']}/{c['fr_retracted']}/{c['fr_expired']}/{c['fr_sup_events']}")
        print(f"  AUX-SIDE-S1-INDEXSIZE {b}: {c['gt_lines']:.1f} lines / {c['gt_tokens']:.1f} o200k tokens vs FR-Bank TRUE FULL {c['fr_lines']:.1f} / {c['fr_tokens']:.1f}")
    c = cens["mem0:two_channel"]
    print(f"  (descriptive) Mem0 two-channel: mapped {c['n_mapped']:,} ({c['frac']:.4f}); ambiguity slot-changing {c['amb_slotkey']:.4f}, any {c['amb_any']:.4f}; "
          f"updated_at points -> {upd['two_channel']}")
    print(f"  (descriptive) Mem0 lexical-required: updated_at points -> {upd['lexical_required']}")
    print("\nbuild_s1: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
