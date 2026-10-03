"""cf2_draft_questions.py -- CF-2 question drafting through the FROZEN CF-1 renderer.

Imports draft_questions.py unchanged (sha pinned in verify_cf2.py) and redirects only its three
path constants: pairs from cf2/cf_pairs_cf2.json, display names for all 40 personas from
cf2/_names_cf2.json (equal to _names.json on CF-1's 30), output to cf2/cf_questions_cf2.json.
Asserts the frozen prompt sha (all seven bound fields) before any call. gpt-4.1-mini only.

  python cf2_draft_questions.py                  draft every pair in cf_pairs_cf2.json (Step 1)
  python cf2_draft_questions.py --only <pair_id> [--exclude <pair_id>]
        draft one replacement pair (D-CF2-2) through the same renderer and gate, append its row
        to cf_questions_cf2.json, move the excluded pair's row to meta.excluded_questions (omit
        --exclude when the batch path already moved it), and recompute the questions sha256 over
        the accepted rows (sorted by pair_id, as draft_questions does). Pairs listed in
        cf_pairs_cf2.json meta.pending_draft may still lack a row until they are drafted.
"""
import hashlib, io, json, pathlib, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import draft_questions as D  # noqa: E402

FROZEN_SHA = "b748247b3ff380d8c24a3e142e2c37c12718942438c3a96cce476531692a8c7f"
assert D.prompt_sha256() == FROZEN_SHA, f"STOP: drafting prompt sha {D.prompt_sha256()} != frozen {FROZEN_SHA}"
assert (D.MODEL, D.TEMPERATURE, D.SEED, D.ALT_SEED, D.MAX_TOKENS, D.N_PARAPHRASES) == ("gpt-4.1-mini", 0, 42, 4242, 400, 3)
CF2 = ROOT / "r82_counterfactual" / "cf2"
D.PAIRS = CF2 / "cf_pairs_cf2.json"
D.NAMES = CF2 / "_names_cf2.json"
D.OUT = CF2 / "cf_questions_cf2.json"


def draft_only(pair_id, exclude):
    pairs = json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))["pairs"]
    sel = [p for p in pairs if p["pair_id"] == pair_id]
    assert len(sel) == 1, f"STOP: {pair_id} not in the accepted draw"
    tmp = pathlib.Path(tempfile.mkdtemp()) / "pairs_one.json"
    D.jdump({"pairs": sel}, tmp)
    D.PAIRS, D.OUT = tmp, tmp.with_name("questions_one.json")
    D.main()
    one = json.load(io.open(D.OUT, encoding="utf-8"))
    qdoc = json.load(io.open(CF2 / "cf_questions_cf2.json", encoding="utf-8"))
    rows = qdoc["questions"]
    if exclude:
        ex = [r for r in rows if r["pair_id"] == exclude]
        assert len(ex) == 1, f"STOP: excluded pair {exclude} has no question row"
        rows = [r for r in rows if r["pair_id"] != exclude]
        qdoc["meta"].setdefault("excluded_questions", []).extend({**r, "excluded_under": "D-CF2-2"} for r in ex)
    assert not any(r["pair_id"] == pair_id for r in rows)
    new = one["questions"][0]; new["appended_under"] = "D-CF2-2"; new["replaces"] = exclude
    rows.append(new); rows.sort(key=lambda r: r["pair_id"])
    m, m1 = qdoc["meta"], one["meta"]
    m["n"] = len(rows)
    for k in ("substitutions", "redrafts", "tokens_in", "tokens_out"):
        m[k] = m[k] + m1[k]
    m["usd"] = round(m["usd"] + m1["usd"], 6)
    m["questions_sha256"] = hashlib.sha256("\x1f".join(r["question"] for r in rows).encode("utf-8")).hexdigest()
    m.setdefault("appended", []).append({"pair_id": pair_id, "replaces": exclude, "attempt": new["attempt"],
                                          "usd": m1["usd"], "deviation": "D-CF2-2"})
    # every accepted pair not still awaiting drafting (meta.pending_draft, D-CF2-2 batch) has exactly one row
    pdoc = json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))
    pend = set(pdoc["meta"].get("pending_draft", [])) - {pair_id}
    ids = {p["pair_id"] for p in pairs}
    assert len(rows) == len({r["pair_id"] for r in rows}) and ids - pend <= {r["pair_id"] for r in rows} <= ids, (len(rows), len(ids), len(pend))
    qdoc["questions"] = rows
    D.jdump(qdoc, CF2 / "cf_questions_cf2.json")
    print(f"\nappended {pair_id} (replaces {exclude}); n={m['n']}; questions sha256 {m['questions_sha256']}; spend so far ${m['usd']:.4f}")


if __name__ == "__main__":
    if "--only" in sys.argv:
        a = sys.argv
        draft_only(a[a.index("--only") + 1], a[a.index("--exclude") + 1] if "--exclude" in a else None)
    else:
        D.main()
