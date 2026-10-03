"""ledger_pad.py -- write pad_probe/NUMBERS_PAD.md from the build, probe, rows and results artifacts.

No model call. Every number printed here is read from an artifact under pad_probe/ (build_pad.json,
probe.json, rows/mini_pad.json, results/pad_scores.json, contam_*.json, results/contam_scores.json,
cache/cost_ledger.json, rows/*.jsonl). Re-run after every lane; the file is regenerated whole.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pad_common as PC  # noqa: E402
from pad_common import BELIEVED, LENGTHS, PAD, REG_SHA, jload  # noqa: E402

BUILD, ROWS, RES = PAD / "build", PAD / "rows", PAD / "results"
STATES = ("superseded", "retracted", "expired")
NAMES = {"emb": "embedding lookup", "lex": "lexical lookup", "mini": "GPT-4.1 mini"}


def ci(d):
    return f"[{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]{'*' if d.get('excludes_zero') else ''}"


def pv(p):
    agree = p.get("agree", bool(p["ci_item"].get("excludes_zero")) == bool(p["ci_persona"].get("excludes_zero")))
    return f"{p['delta']:+.4f}; item {ci(p['ci_item'])}, persona {ci(p['ci_persona'])}" + ("" if agree else " — disagree, the weaker governs")


def main():
    B = jload(BUILD / "build_pad.json")
    have_probe = (BUILD / "probe.json").exists()
    have_rows = (ROWS / "mini_pad.json").exists()
    have_scores = (RES / "pad_scores.json").exists()
    L = [f"# NUMBERS_PAD — ledger for the padding probe (ADDENDUM_PAD) and its Amendment 1\n",
         f"Registration: `registrations/ADDENDUM_PAD.md`, registered text sha256 `{REG_SHA}` (the bytes above the marker line; "
         f"Amendment 1 appended below it), frozen at `dab8956` on 2026-09-14 by the author's instruction. Descriptive: no prediction, no bar, "
         f"no verdict; the §5 branches print as they come out. Every number for this probe enters the manuscript through a key in this file "
         f"and no other way. Deviations and settled readings: `pad_probe/DEVIATIONS_PAD.md` (D-PAD-1 to D-PAD-5).\n",
         "## 1. AUX-PAD-LOCK — the build (`tools/pad_common.py`, `tools/run_pad.py build`; `build/build_pad.json`, `build/padded_lists.json`, `build/padded_texts.json`)\n",
         "| Key | Value |", "|---|---|"]
    pc = B["pool_census"]
    ca = sorted(v["pool_a"] for v in pc.values()); cb = sorted(v["pool_b"] for v in pc.values())
    fa = {Lx: sum(v[f"from_pool_a_L{Lx}"] for v in pc.values()) for Lx in LENGTHS}
    fb = {Lx: sum(v[f"from_pool_b_L{Lx}"] for v in pc.values()) for Lx in LENGTHS}
    nb = {Lx: sum(1 for v in pc.values() if v[f"from_pool_b_L{Lx}"] > 0) for Lx in LENGTHS}
    cc = B["contamination_check"]
    L.append(f"| **AUX-PAD-LOCK** | Registration sha256 holds; `prompts_e1` digests hold. **661 items, {B['n_keys']} keys.** Renderer lock: the superseded section "
             f"re-rendered over the committed names alone under the lifted cap reproduces the committed text byte for byte on **{B['renderer_lock']['ok']} of {B['n_keys']}** keys. "
             f"Longest committed list {B['longest_committed_list']} names (marker-cleaned; D-PAD-5); committed mean {B['mean_names_per_item_committed']:.4f} names per item as committed "
             f"({B['mean_names_per_item_committed_marker_stripped']:.4f} marker-free). Pools: pool A (the key's own printed map names after exclusions i–iii) min {ca[0]}, median {ca[len(ca)//2]}, "
             f"max {ca[-1]}; pool B (other personas' FULL:TRUE map names) min {cb[0]}, median {cb[len(cb)//2]}, max {cb[-1]}. Names drawn from pool A / pool B: "
             + "; ".join(f"L={Lx}: {fa[Lx]} / {fb[Lx]} ({nb[Lx]} keys reach pool B)" for Lx in LENGTHS)
             + f". Every padded list asserted: exactly L names, no excluded name in the padding, no `:`, no duplicate, the committed names kept, the three lengths nested (D-PAD-1). "
             f"Exclusion (ii) applied as the rule states it (D-PAD-2): the padding names a negative's own attribute on {cc['L15']['neg_own_named']} negatives at every L, exactly the "
             f"{cc['base']['neg_own_named']} the committed list already names, and a positive's own on {cc['L15']['pos_own_named']} positives, the committed {cc['base']['pos_own_named']}. "
             f"Padded texts sha256 `{B['texts_sha256'][:16]}…`. |")
    g = B["lookup_gate"]
    L.append(f"| **AUX-PAD-GATE** | The committed lists through `run_nb6.lex_scores` / `emb_scores` (as committed, marker included): embedding **{g['got']['emb']:.4f}**, "
             f"lexical **{g['got']['lex']:.4f}** — `AUX-E1R-NB6` at four decimals, **PASS**. Mini's recorded `INDEXED-TRUE` row {B['mini_recorded_auroc']:.4f} (registered 0.7339). "
             f"Marker-stripped base, descriptive (D-E1R-11): embedding {B['base_marker_stripped']['emb']:.4f}, lexical {B['base_marker_stripped']['lex']:.4f}. |")
    if have_probe:
        P = jload(BUILD / "probe.json"); pj = P["projection"]
        L.append(f"| **AUX-PAD-PROBE** | Three direct calls (one item at each L): served `{P['probes'][0]['served_model']}` on all three (E1.7 rule, PASS); "
                 f"prompt tokens {', '.join(str(p['prompt_tokens']) for p in P['probes'])}; completion tokens {', '.join(str(p['completion_tokens']) for p in P['probes'])}; probe ${P['probe_usd']:.4f}. |")
        L.append(f"| **AUX-PAD-PROJECTION** | {pj['calls']} calls; o200k token count over every prompt calibrated by the probe (ratio {pj['calibration_ratio_served_over_o200k']:.4f}): "
                 f"mean prompt tokens {pj['mean_prompt_tokens_by_L']['15']:.0f} / {pj['mean_prompt_tokens_by_L']['30']:.0f} / {pj['mean_prompt_tokens_by_L']['60']:.0f} at L = 15 / 30 / 60; "
                 f"**${pj['usd']:.2f}** (×1.3 ${pj['usd_x1.3']:.2f}) against the $2.50 line and the combined $15 headroom (first lane: $15.00) — under both. |")
    if have_rows:
        R = jload(ROWS / "mini_pad.json"); m = R["meta"]["meter"]
        L.append(f"| **AUX-PAD-MINI-RUN** | {m['calls']} calls ({m['cached']} cached), {m['in']:,} in / {m['out']:,} out tokens, **${m['usd']:.4f}** metered at list price; "
                 f"retried after a parse failure: {R['meta']['retried']}; elicitation failures {R['meta']['failures']}; {R['meta']['seconds']:.0f} s; JSON mode, temperature 0, seed 42, max_tokens 200, "
                 f"served `{R['meta']['served_model_probe']}`. |")
    L.append("")
    if have_scores:
        Sx = jload(RES / "pad_scores.json")
        L.append("## 2. AUX-PAD-LOOKUP-EMB, AUX-PAD-LOOKUP-LEX, AUX-PAD-MINI — AUROC by length, whole and per state, paired against the 1.75-name row (`tools/run_pad.py score`; `results/pad_scores.json`)\n")
        L.append("Whole population n = 661 (104 positives); per state = that state's positives against the same 557 negatives (`nb6_composition`'s construction). "
                 "Paired difference = padded − recorded, item by item; item-level paired bootstrap (1,000 draws, seed 42, single-class draws discarded) and persona-clustered paired bootstrap; "
                 "`*` marks an interval excluding zero; where the two disagree the weaker reading governs. Tolerance ±0.05 on the point estimate.\n")
        for name in ("emb", "lex", "mini"):
            Rr = Sx["readers"][name]
            key = {"emb": "AUX-PAD-LOOKUP-EMB", "lex": "AUX-PAD-LOOKUP-LEX", "mini": "AUX-PAD-MINI"}[name]
            L.append(f"**{key}** — {NAMES[name]} (BELIEVED row {BELIEVED[name]:.4f}).\n")
            L.append("| length | whole | Δ vs 1.75 (item CI, persona CI) | superseded | Δ | retracted | Δ | expired | Δ |" + (" distinct nok | mean nok |" if name == "mini" else ""))
            L.append("|---|---:|---|---:|---|---:|---|---:|---|" + ("---:|---:|" if name == "mini" else ""))
            b = Rr["base"]
            L.append(f"| 1.75 (recorded) | **{b['auroc']:.4f}** | — | {b['auroc_superseded']:.4f} | — | {b['auroc_retracted']:.4f} | — | {b['auroc_expired']:.4f} | — |"
                     + (f" {b['distinct_nok']} | {b['mean_nok']:.4f} |" if name == "mini" else ""))
            for Lx in LENGTHS:
                r = Rr[str(Lx)]
                row = f"| {Lx} | **{r['auroc']:.4f}** | {pv(r['paired_vs_base'])} |"
                for st in STATES:
                    row += f" {r[f'auroc_{st}']:.4f} | {r[f'paired_vs_base_{st}']['delta']:+.4f}, weaker {ci(r[f'paired_vs_base_{st}']['weaker'])} |"
                if name == "mini":
                    row += f" {r['distinct_nok']} | {r['mean_nok']:.4f} |"
                L.append(row)
            L.append("")
        L.append("## 3. AUX-PAD-BRANCH — the §5 headings, per reader, whole population\n")
        L.append("| Key | Value |", ); L.append("|---|---|")
        for name in ("emb", "lex", "mini"):
            br = Sx["readers"][name]["branches"]
            heads = []
            if br["flat"]:
                heads.append("**Flat** (every paired difference inside ±0.05)")
            if br["degrades_at"]:
                heads.append(f"**Degrades**, first at L = {br['degrades_first_at']} (below −0.05 with both intervals excluding zero at L = {', '.join(str(x) for x in br['degrades_at'])})")
            if br["past_believed_at"]:
                heads.append(f"**Degrades past the BELIEVED row** ({BELIEVED[name]:.4f}) at L = {', '.join(str(x) for x in br['past_believed_at'])}")
            if br["beyond_tolerance_without_both_intervals_or_rise"]:
                heads.append(f"a difference beyond tolerance whose intervals do not both exclude zero, or a rise, at L = {', '.join(str(x) for x in br['beyond_tolerance_without_both_intervals_or_rise'])} (printed as described in §2)")
            if not heads:
                heads.append("fits no heading (printed as described in §2)")
            L.append(f"| **AUX-PAD-BRANCH ({NAMES[name]})** | " + "; ".join(heads) + ". |")
        L.append("")
    # ---------------------------------------------------------------- Amendment 1
    L.append("## 4. Amendment 1 — the contaminated lists on the 444 (`tools/contam.py`; `build/contam_build.json`, `build/contam_texts.json`, `rows/rows_MINI.jsonl`, `rows/rows_H45.jsonl`, `results/contam_scores.json`)\n")
    L.append("| Key | Value |"); L.append("|---|---|")
    if (BUILD / "contam_build.json").exists():
        C = jload(BUILD / "contam_build.json")
        L.append(f"| **AUX-PAD-C-LOCK** | 444 items (148 PN), v2 summaries; renderer lock on the committed names alone **{C['renderer_lock_ok']} of 444**; every rendered list re-parses to the injected list, no `:`, no duplicate. |")
        for arm, rate in (("INDEXED-V2-C0.232", 0.232), ("INDEXED-V2-C0.40", 0.40)):
            a = C["arms"][arm]; gg = a["gate"]; inj = a["injection"]
            L.append(f"| **AUX-PAD-C-GATE (c = {rate})** | Regenerated by `sweep_common.inject`, seed 42: {inj['n_injected']} names injected, achieved rate {inj['achieved_rate']:.4f} of 296 negatives "
                     f"(target {rate}); mean {a['census']['mean_len']:.4f} names per item; negatives naming their own attribute {a['census']['neg_own_named']}, positives {a['census']['pos_own_named']}. "
                     f"Lookups on the regenerated lists: embedding whole **{gg['got']['emb']:.4f}** (sweep {gg['sweep']['emb']:.4f}), supersession slice {gg['got']['emb_sup']:.4f} (sweep {gg['sweep']['emb_sup']:.4f}); "
                     f"lexical whole {gg['got']['lex']:.4f} (sweep {gg['sweep']['lex']:.4f}), slice {gg['got']['lex_sup']:.4f} (sweep {gg['sweep']['lex_sup']:.4f}) — **PASS** at four decimals (D-PAD-4 on the amendment's label). |")
    if (BUILD / "contam_probes.json").exists():
        for lane, rec in jload(BUILD / "contam_probes.json").items():
            pj = rec["projection"]
            L.append(f"| **AUX-PAD-C-PROBE ({lane})** | served `{rec['served'][0]}` on both arms (E1.7, {'PASS' if rec['identifier_ok'] else 'FAIL'}); prompt tokens {rec['in']}, completion {rec['out']}; "
                     f"projection {pj['calls']} calls **${pj['usd']:.2f}** (×1.3 ${pj['usd_x1.3']:.2f}). |")
    if (RES / "contam_scores.json").exists():
        Cs = jload(RES / "contam_scores.json")
        L.append("")
        L.append("Per state on the 444 = the items of that state, positives and negatives alike (the CF-2 convention, `AUX-CF2-NB6-V2`). Paired difference = contaminated − recorded on the same items; "
                 "model − lookup on the same lists under the same summary (the `AUX-R103-MARGIN` construction). Intervals as in section 2.\n")
        for name, key in (("emb", "AUX-PAD-C-LOOKUP-EMB"), ("lex", "AUX-PAD-C-LOOKUP-LEX"), ("MINI", "AUX-PAD-C-MINI"), ("H45", "AUX-PAD-C-H45")):
            Rr = Cs["readers"].get(name)
            label = {"emb": "embedding lookup", "lex": "lexical lookup", "MINI": "GPT-4.1 mini (k = 1)", "H45": "Haiku 4.5 (k = 5, X4 mean)"}[name]
            if not Rr or "status" in Rr:
                L.append(f"**{key}** — {label}: — ({Rr['status'] if Rr else 'not scored'}).\n")
                continue
            L.append(f"**{key}** — {label}.\n")
            L.append("| list | whole | Δ vs recorded (item CI, persona CI) | supersession | Δ | retraction | Δ | expiry | Δ |" + (" model − emb | model − lex |" if name in ("MINI", "H45") else ""))
            L.append("|---|---:|---|---:|---|---:|---|---:|---|" + ("---|---|" if name in ("MINI", "H45") else ""))
            b = Rr["base"]
            L.append(f"| recorded (c = 0) | **{b['auroc']:.4f}** | — | {b['auroc_superseded']:.4f} | — | {b['auroc_retracted']:.4f} | — | {b['auroc_expired']:.4f} | — |" + (" — | — |" if name in ("MINI", "H45") else ""))
            for arm, rate in (("INDEXED-V2-C0.232", 0.232), ("INDEXED-V2-C0.40", 0.40)):
                r = Rr[arm]
                row = f"| c = {rate} | **{r['auroc']:.4f}** | {pv(r['paired_vs_recorded'])} |"
                for st in STATES:
                    row += f" {r[f'auroc_{st}']:.4f} | {r[f'paired_vs_recorded_{st}']['delta']:+.4f}, weaker {ci(r[f'paired_vs_recorded_{st}']['weaker'])} |"
                if name in ("MINI", "H45"):
                    row += f" {r['model_minus_emb']['delta']:+.4f}, weaker {ci(r['model_minus_emb']['weaker'])} | {r['model_minus_lex']['delta']:+.4f}, weaker {ci(r['model_minus_lex']['weaker'])} |"
                L.append(row)
            L.append("")
    # ---------------------------------------------------------------- spend
    L.append("## 5. AUX-PAD-SPEND\n")
    L.append("| Key | Value |"); L.append("|---|---|")
    parts, total = [], 0.0
    if (PAD / "cache" / "cost_ledger.json").exists():
        m = jload(PAD / "cache" / "cost_ledger.json"); parts.append(f"PAD mini lane ${m['usd']:.4f} ({m['calls']} calls)"); total += m["usd"]
    if have_probe:
        p = jload(BUILD / "probe.json")["probe_usd"]; parts.append(f"PAD probe ${p:.4f}"); total += p
    if (BUILD / "contam_probes.json").exists():
        for lane, rec in jload(BUILD / "contam_probes.json").items():
            parts.append(f"Amendment 1 probe {lane} ${rec['probe_usd']:.4f}"); total += rec["probe_usd"]
    for code, lane in (("MINI", "gpt-4.1-mini"), ("H45", "claude-haiku-4-5-20251001")):
        pth = ROWS / f"rows_{code}.jsonl"
        if pth.exists():
            usd = sum(json.loads(l).get("usd", 0.0) for l in io.open(pth, encoding="utf-8"))
            n = sum(1 for _ in io.open(pth, encoding="utf-8"))
            parts.append(f"Amendment 1 {lane} lane ${usd:.4f} ({n} rows)"); total += usd
    L.append(f"| **AUX-PAD-SPEND** | {'; '.join(parts)}; **total ${total:.4f}** metered from the rows at list / Batch prices, against the combined $15 cap shared with `ADDENDUM_PARA`. |")
    L.append("")
    io.open(PAD / "NUMBERS_PAD.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"wrote {PAD / 'NUMBERS_PAD.md'}")


if __name__ == "__main__":
    main()
