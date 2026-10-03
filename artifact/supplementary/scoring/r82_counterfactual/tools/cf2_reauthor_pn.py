"""cf2_reauthor_pn.py -- D-CF2-3: re-author the PN records the author read as NO, once, through the
FROZEN author_pn.py at seed 4242 (the question redraft's alternate seed). Prompt, predicates,
thresholds and the single frozen retry are author_pn's own; the seed is the only patched constant.

Input : cf2/pn_read_verdicts.json (the NO rows), cf2/cf_pairs_cf2.json
Output: cf2/cf_pn_texts_cf2_reauthor_4242.json  -- for each NO pair: the first record (seed 42,
        verdict, category) beside the re-authored record (seed 4242, predicates, attempts)
A predicate STOP inside author_pn.py is a STOP here too and falls to D-CF2-2.
"""
import io, json, pathlib, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "r82_counterfactual" / "tools"))
import author_pn as A  # noqa: E402

CF1_SHA = "b6f53b1ab03fbd7124759fe19d875464f7e236a2df0a80a27f83c5277467a832"
assert A.prompt_sha256() == CF1_SHA, f"STOP: authoring prompt sha {A.prompt_sha256()} != CF-1's {CF1_SHA}"
assert (A.MODEL, A.EMBED_MODEL, A.TEMPERATURE, A.MAX_TOKENS, A.TAU_HI, A.COSINE_MIN) == ("gpt-4.1-mini", "text-embedding-3-small", 0, 300, 0.80, 0.85)
CF2 = ROOT / "r82_counterfactual" / "cf2"
J = lambda p: json.load(io.open(p, encoding="utf-8"))  # noqa: E731

REAUTHOR_SEED = 4242


def main():
    pv = J(CF2 / "pn_read_verdicts.json"); pairs = {p["pair_id"]: p for p in J(CF2 / "cf_pairs_cf2.json")["pairs"]}
    first = {r["pair_id"]: r for r in J(CF2 / "cf_pn_texts_cf2.json")["records"]}
    no = [v for v in pv["verdicts"] if not v["pass"]]
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    sel = [pairs[v["pair_id"]] for v in no if only is None or v["pair_id"] in only]
    print(f"re-authoring {len(sel)} NO records at seed {REAUTHOR_SEED} (author_pn unchanged)")
    tmp = pathlib.Path(tempfile.mkdtemp())
    A.jdump({"pairs": sel}, tmp / "pairs_no.json")
    A.PAIRS, A.NAMES, A.OUT, A.SEED = tmp / "pairs_no.json", CF2 / "_names_cf2.json", tmp / "reauthored.json", REAUTHOR_SEED
    A.main()                                   # a predicate STOP raises SystemExit here
    new = J(A.OUT)
    outp = CF2 / "cf_pn_texts_cf2_reauthor_4242.json"
    prev = J(outp) if outp.exists() else {"records": []}
    keep = {r["pair_id"]: r for r in prev["records"]}
    for r in new["records"]:
        v = next(x for x in no if x["pair_id"] == r["pair_id"]); f = first[r["pair_id"]]
        keep[r["pair_id"]] = {"pair_id": r["pair_id"], "state": r["state"], "persona": pairs[r["pair_id"]]["persona"],
                              "entry_id": pairs[r["pair_id"]]["entry_id"], "slot": pairs[r["pair_id"]]["slot_key"][1],
                              "original_text": pairs[r["pair_id"]]["entry_text"],
                              "first": {"seed": 42, "new_text": f["new_text"], "predicates": f["predicates"], "attempts": f["attempts"],
                                        "read_verdict": v["verdict"], "read_category": v["category"]},
                              "reauthored": {"seed": REAUTHOR_SEED, "new_text": r["new_text"], "predicates": r["predicates"], "attempts": r["attempts"]},
                              "same_text_as_first": r["new_text"].strip() == (f["new_text"] or "").strip(),
                              "deviation": "D-CF2-3"}
    recs = sorted(keep.values(), key=lambda r: (r["state"], r["persona"], r["pair_id"]))
    meta = {"no_api_calls": False, "deviation": "D-CF2-3", "seed": REAUTHOR_SEED, "prompt_sha256": new["meta"]["prompt_sha256"],
            "retries": new["meta"]["retries"] + prev.get("meta", {}).get("retries", 0),
            "tokens_in": new["meta"]["tokens_in"] + prev.get("meta", {}).get("tokens_in", 0),
            "tokens_out": new["meta"]["tokens_out"] + prev.get("meta", {}).get("tokens_out", 0),
            "embed_tokens": new["meta"]["embed_tokens"] + prev.get("meta", {}).get("embed_tokens", 0),
            "usd": round(new["meta"]["usd"] + prev.get("meta", {}).get("usd", 0), 6), "n": len(recs)}
    A.jdump({"meta": meta, "records": recs}, outp)
    print(f"\n{len(recs)} re-authored records -> {outp}\n  retries {meta['retries']}   identical to the first attempt: "
          f"{sum(r['same_text_as_first'] for r in recs)}   spend ${meta['usd']:.4f}")


if __name__ == "__main__":
    main()
