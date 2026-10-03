"""cf3_build.py -- ADDENDUM_CF3 §§1-3: the 14-pair expiry cell, built by the CF-2 modules with their path constants
re-pointed to r82_counterfactual/cf3/ and nothing else changed.

  pairs    the 14 pairs of §1 written in the CF-2 pair format (cf3/cf_pairs_cf2.json), _names_cf2.json copied,
           cf_pn_texts_cf2.json with the expiry placeholders; the locks of §6 (registration sha256, census sha256,
           every pair ELIGIBLE in cf2/adjudication_cf2.json, none in the 444).                        NO CALL
  draft    the questions through the frozen CF-1 renderer (draft_questions.py re-pointed, as cf2_draft_questions does):
           gpt-4.1-mini, temperature 0, seed 42 / 4242, three paraphrases, the intent gate.          ~14-28 calls
  build    cf2_build_cell.build() and add_v2r() on cf3/: the three versions, v2 / v3 / v2r, assertions A-E, the
           draw-time predicates and assertion C re-asserted; zero overlap with the 444 asserted.       NO CALL
  leak     cf2_leakscreen with N = 14 (every PRESENT item) and THRESHOLD = 1 (§3).                    42 calls

The CF-2 file names inside cf3/ are the CF-2 modules' expectations (cf2_build_cell reads CF2 / "cf_pairs_cf2.json"
and its siblings); cf3/README.md records this.
"""
from __future__ import annotations

import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
for p in ("e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual", "r82_counterfactual/tools"):
    sys.path.insert(0, str(ROOT / p))

CF2 = ROOT / "r82_counterfactual" / "cf2"
CF3 = ROOT / "r82_counterfactual" / "cf3"
REG = ROOT / "registrations" / "ADDENDUM_CF3.md"
REG_SHA = "2f555c1ac4c3018e66a0fc453be7c4c4d3ffd4e3a2f7ac63c5c7b3590ca4f910"
CENSUS_SHA = "b1c9cf1e292dfbb7"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."
INTENT = "UPCOMING"


def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=2, sort_keys=True, default=str)
        f.write("\n")


def sha_frozen(p):
    b = p.read_bytes(); i = b.find(FROZEN_END)
    return hashlib.sha256(b if i < 0 else b[:i]).hexdigest()


def locks():
    out = {"registration_sha256": sha_frozen(REG), "registration_ok": sha_frozen(REG) == REG_SHA,
           "census_sha256": hashlib.sha256((CF3 / "census_cf3.json").read_bytes()).hexdigest()}
    out["census_ok"] = out["census_sha256"].startswith(CENSUS_SHA)
    return out


def cmd_pairs():
    L = locks()
    assert L["registration_ok"] and L["census_ok"], L
    census = J(CF3 / "census_cf3.json")
    take = census["C_sizing"]["EXPIRY"]["no_relaxation"]["eligible_undrawn_fitting_list"]
    keys = [(t.split(" ")[0], t.split(" ")[1]) for t in take]
    assert len(keys) == 14, len(keys)
    rows = {(r["persona"], r["entry_id"]): r for r in census["B_predicates"]["EXPIRY"]}
    adj = {(v["persona"], v["entry_id"]): v for v in J(CF2 / "adjudication_cf2.json")["EXPIRY"]["verdicts"]}
    cf2pairs = J(CF2 / "cf_pairs_cf2.json")
    used = {(p["persona"], p["entry_id"]) for p in cf2pairs["pairs"]}
    banks = {}
    import select_pairs as SP
    pairs = []
    for persona, eid in keys:
        r = rows[(persona, eid)]
        v = adj[(persona, eid)]
        assert v["walk_status"] in ("ELIGIBLE", "REUSED") and v["verdict"] == "ELIGIBLE", (persona, eid, v["walk_status"])
        assert (persona, eid) not in used, (persona, eid, "in the 444")
        if persona not in banks:
            banks[persona] = J(SP.BANKS / f"{persona}.json")["entries"]
        e = next(x for x in banks[persona] if x["id"] == eid)
        t_now, cutoff = SP.persona_clock(banks[persona])
        pairs.append({"pair_id": f"cf3:{persona}:{e['slot_key'][1]}", "persona": persona, "state": "EXPIRY", "intent": INTENT,
                      "slot_key": list(e["slot_key"]), "slot_scrubbed": r["slot_scrubbed"], "entry_id": eid, "entry_text": e["text"],
                      "category": e["category"], "source_session": e.get("source_session"), "created_at": e.get("created_at"),
                      "event_time": e.get("event_time"), "t_now": t_now.isoformat(), "cutoff": cutoff.isoformat(),
                      "o3": e["category"] not in SP.EXP_CATS, "overlap_tag": r.get("readmit"), "overlap": r.get("overlap"),
                      "queue_position": r.get("queue_position"), "adjudication": "ELIGIBLE", "adjudication_source": v["source"],
                      "adjudication_reason": v.get("reason", ""), "n_candidates_this_persona_class": None})
    pairs.sort(key=lambda p: p["pair_id"])
    jdump({"meta": {"registration": "registrations/ADDENDUM_CF3.md", "registration_sha256": REG_SHA, "census_sha256": L["census_sha256"],
                    "quota": {"SUPERSESSION": 0, "RETRACTION": 0, "EXPIRY": 14}, "class_intent": {"EXPIRY": INTENT}, "n_items": 42,
                    "no_api_calls": True, "date": "2026-09-14", "locks": L,
                    "file_name_note": "CF-2 file names inside cf3/ so that cf2_build_cell, cf2_leakscreen and cf2_draft_questions' module read them unmodified"},
           "pairs": pairs}, CF3 / "cf_pairs_cf2.json")
    (CF3 / "_names_cf2.json").write_bytes((CF2 / "_names_cf2.json").read_bytes())
    jdump({"meta": {"note": "expiry pairs carry no authored record: the anchor moves and the status record is appended (ADDENDUM_CF2 section 2)"},
           "records": [{"pair_id": p["pair_id"], "state": "EXPIRY", "new_text": None, "note": "no expiry write path; the anchor moves and nothing else"} for p in pairs]},
          CF3 / "cf_pn_texts_cf2.json")
    (CF3 / "README.md").write_text(
        "# cf3/ — the CF-3 expiry cell (ADDENDUM_CF3.md)\n\nThe input files `cf_pairs_cf2.json`, `cf_questions_cf2.json`, `cf_pn_texts_cf2.json` and "
        "`_names_cf2.json` are the CF-3 cell's files under the CF-2 modules' expected names, so that `cf2_build_cell.py`, `cf2_leakscreen.py` and the "
        "drafting module read them with their path constant re-pointed and nothing else changed (`cf3_build.py`). `cf_cell.json`, `cf_indexes.json` "
        "and `rows/` are the cell, its summaries and the lanes' rows. `census_cf3.py` / `CF3_CENSUS.md` are the sizing census that fixed the 14 pairs.\n",
        encoding="utf-8", newline="\n")
    print(f"14 pairs written -> {CF3 / 'cf_pairs_cf2.json'}; locks {L}")


def cmd_draft():
    assert locks()["registration_ok"]
    import cf2_draft_questions as CD           # asserts the frozen prompt sha at import
    D = CD.D
    D.PAIRS, D.NAMES, D.OUT = CF3 / "cf_pairs_cf2.json", CF3 / "_names_cf2.json", CF3 / "cf_questions_cf2.json"
    D.main()
    q = J(D.OUT)
    print("questions sha256", q["meta"]["questions_sha256"], "usd", q["meta"]["usd"], "redrafts", q["meta"]["redrafts"], "substitutions", q["meta"]["substitutions"])


def cmd_build():
    assert locks()["registration_ok"]
    import cf2_build_cell as BC
    BC.CF2 = CF3
    BC.build()
    BC.add_v2r()
    cell = J(CF3 / "cf_cell.json"); idx = J(CF3 / "cf_indexes.json")
    used = {(p["persona"], p["entry_id"]) for p in J(CF2 / "cf_pairs_cf2.json")["pairs"]}
    pairs = J(CF3 / "cf_pairs_cf2.json")["pairs"]
    assert not ({(p["persona"], p["entry_id"]) for p in pairs} & used), "overlap with the 444"
    cf2_items = {it["item_id"] for it in J(CF2 / "cf_cell.json")["items"]}
    assert not ({it["item_id"] for it in cell["items"]} & cf2_items)
    print("cell", cell["meta"]["n"], "items; composition", cell["meta"]["composition"], "; indexes sha256", idx["meta"]["sha256"][:16], "; arms", idx["meta"]["arms"])


def cmd_leak():
    assert locks()["registration_ok"]
    import cf2_leakscreen as LS
    LS.CF2 = CF3
    LS.OUT = CF3 / "results" / "leakscreen_cf3.json"
    LS.N, LS.THRESHOLD = 14, 1
    (CF3 / "results").mkdir(exist_ok=True)
    LS.main()


if __name__ == "__main__":
    {"pairs": cmd_pairs, "draft": cmd_draft, "build": cmd_build, "leak": cmd_leak}[sys.argv[1]]()
