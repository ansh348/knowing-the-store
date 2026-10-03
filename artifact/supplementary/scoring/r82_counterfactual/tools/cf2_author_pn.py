"""cf2_author_pn.py -- CF-2 PN record authoring through the FROZEN CF-1 author_pn.py.

Imports author_pn.py unchanged and redirects only its three path constants: pairs from
cf2/cf_pairs_cf2.json, names from cf2/_names_cf2.json, output to cf2/cf_pn_texts_cf2.json.
Predicates, thresholds, retry rule and the embedding measurement are author_pn's own; a pair
failing twice is a STOP there. Asserts the authoring prompt sha CF-1 recorded before any call.
gpt-4.1-mini and text-embedding-3-small only.

  python cf2_author_pn.py                   author every pair in cf_pairs_cf2.json (Step 2)
  python cf2_author_pn.py --only <pair_id>  author one D-CF2-2 replacement through the same
        author_pn.main (temp pair file, seed 42, same predicates and single retry), append its
        record to cf_pn_texts_cf2.json, add the spend, and clear the pair from
        cf_pairs_cf2.json meta.pending_draft once its question row also exists.
"""
import io, json, pathlib, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import author_pn as A  # noqa: E402

CF1_SHA = "b6f53b1ab03fbd7124759fe19d875464f7e236a2df0a80a27f83c5277467a832"
assert A.prompt_sha256() == CF1_SHA, f"STOP: authoring prompt sha {A.prompt_sha256()} != CF-1's {CF1_SHA}"
assert (A.MODEL, A.EMBED_MODEL, A.TEMPERATURE, A.SEED, A.MAX_TOKENS, A.TAU_HI, A.COSINE_MIN) == ("gpt-4.1-mini", "text-embedding-3-small", 0, 42, 300, 0.80, 0.85)
CF2 = ROOT / "r82_counterfactual" / "cf2"
A.PAIRS = CF2 / "cf_pairs_cf2.json"
A.NAMES = CF2 / "_names_cf2.json"
A.OUT = CF2 / "cf_pn_texts_cf2.json"


def author_only(pair_id):
    pdoc = json.load(io.open(CF2 / "cf_pairs_cf2.json", encoding="utf-8"))
    sel = [p for p in pdoc["pairs"] if p["pair_id"] == pair_id]
    assert len(sel) == 1, f"STOP: {pair_id} not in the accepted draw"
    assert sel[0].get("replacement_under") == "D-CF2-2", f"STOP: {pair_id} is not a D-CF2-2 replacement"
    qdoc = json.load(io.open(CF2 / "cf_questions_cf2.json", encoding="utf-8"))
    assert any(r["pair_id"] == pair_id for r in qdoc["questions"]), f"STOP: {pair_id} has no question row yet"
    tmp = pathlib.Path(tempfile.mkdtemp()) / "pairs_one.json"
    A.jdump({"pairs": sel}, tmp)
    A.PAIRS, A.OUT = tmp, tmp.with_name("pn_one.json")
    A.main()                                             # a double predicate failure is author_pn's own STOP
    one = json.load(io.open(A.OUT, encoding="utf-8"))
    pn = json.load(io.open(CF2 / "cf_pn_texts_cf2.json", encoding="utf-8"))
    assert not any(r["pair_id"] == pair_id for r in pn["records"])
    new = one["records"][0]; new["appended_under"] = "D-CF2-2"; new["replaces"] = sel[0].get("replaces")
    pn["records"].append(new); pn["records"].sort(key=lambda r: r["pair_id"])
    m, m1 = pn["meta"], one["meta"]
    for k in ("retries", "tokens_in", "tokens_out", "embed_tokens"):
        m[k] = m[k] + m1[k]
    m["usd"] = round(m["usd"] + m1["usd"], 6)
    m.setdefault("appended", []).append({"pair_id": pair_id, "replaces": new["replaces"], "attempts": new["attempts"],
                                          "usd": m1["usd"], "deviation": "D-CF2-2"})
    A.jdump(pn, CF2 / "cf_pn_texts_cf2.json")
    pend = pdoc["meta"].get("pending_draft", [])
    if pair_id in pend:
        pend.remove(pair_id); pdoc["meta"]["pending_draft"] = pend
        A.jdump(pdoc, CF2 / "cf_pairs_cf2.json")
    print(f"\nappended {pair_id} (replaces {new['replaces']}); records {len(pn['records'])}; still awaiting drafting {len(pend)}; spend so far ${m['usd']:.4f}")


if __name__ == "__main__":
    if "--only" in sys.argv:
        author_only(sys.argv[sys.argv.index("--only") + 1])
    else:
        A.main()
