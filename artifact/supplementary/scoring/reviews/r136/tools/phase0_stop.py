"""phase0_stop.py -- R136 Phase 0: write reviews/r136/PHASE0_STOP.md (the verbatim quotes with file and line numbers, the
1.2 answer, the draft registration and its sha256, the dry-run checks, the projection). Read-only; $0."""
from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "cf_pad" / "tools"))
import cf_pad_common as C  # noqa: E402

OUT = ROOT / "reviews" / "r136" / "PHASE0_STOP.md"
QUOTES = [
    ("registrations/ADDENDUM_PAD.md", 35, 71, "the registered construction (§3): the padded section, the pools, the draw, the assertions, the renderer lock"),
    ("pad_probe/DEVIATIONS_PAD.md", 10, 12, "D-PAD-1 (one seed per key, nested lengths), D-PAD-2 (exclusion (ii) wide), D-PAD-3 (overflow fragments, the one name with a space)"),
    ("pad_probe/DEVIATIONS_PAD.md", 14, 14, "D-PAD-5 (the longest committed list is 5; the marker is not a name)"),
    ("pad_probe/tools/pad_common.py", 57, 64, "constants: the frozen sha, LENGTHS, SLOT_CAP_LIFTED = 100, the marker, the gates"),
    ("pad_probe/tools/pad_common.py", 88, 98, "render_section_lifted: how the fifteen-name cap is lifted (index_v3.SLOT_CAP set to 100 around _name_block)"),
    ("pad_probe/tools/pad_common.py", 118, 122, "poolable: no ':', no overflow fragment, no whitespace"),
    ("pad_probe/tools/pad_common.py", 169, 197, "build_pools: pool A (own printed map less committed, targeted slots, ':') and pool B (other personas' FULL:TRUE maps)"),
    ("pad_probe/tools/pad_common.py", 200, 230, "draw_order (random.Random(f'42:{key}'), pool A then pool B) and padded_lists (committed names kept, pad = order[:L - len(com)], the assertions, nesting)"),
    ("pad_probe/tools/pad_common.py", 233, 238, "padded_text: the prefix above the header byte-identical, the tail re-rendered"),
    ("r82_counterfactual/index_v3.py", 35, 46, "_name_block: sorted set, SLOT_CAP, '(+N more)', wrap at WRAP with indents two and four (how the list is ordered)"),
    ("e1_metamemory/tools/index_v2.py", 105, 109, "SLOT_CAP = 15 and WRAP = 150 (the cap that is lifted)"),
    ("pad_probe/tools/contam.py", 76, 82, "Amendment 1 on the 444: the renderer lock on the committed v2 texts (444 of 444 or STOP)"),
    ("pad_probe/tools/contam.py", 95, 100, "Amendment 1 on the 444: padded_text over the v2 text, the re-parsed list asserted"),
]


def quote(path, a, b):
    lines = io.open(ROOT / path, encoding="utf-8").read().split("\n")
    return "\n".join(f"{n:5d}  {lines[n - 1]}" for n in range(a, min(b, len(lines)) + 1))


def main():
    B = C.jload(C.BUILD / "dryrun_build.json"); cen = B["census"]
    P = C.jload(C.BUILD / "projection.json")
    log = io.open(C.BUILD / "dryrun_log.txt", encoding="utf-8").read()
    triple = log[log.index("===== one rendered triple"):log.index("\nwrote ")]
    reg = io.open(C.REG, encoding="utf-8").read()
    reg_text = reg[:reg.index("<!-- REGISTERED TEXT ENDS ABOVE THIS LINE.")]
    sha = C.sha256_frozen()
    L = []
    L.append("# R136 Phase 0 — STOP (read-only, $0; 2026-09-22)\n")
    L.append(f"Draft registration `registrations/ADDENDUM_CF_PAD.md`, **registered-text sha256 `{sha}`** (the bytes above the marker line; "
             f"whole file `{hashlib.sha256(reg.encode('utf-8')).hexdigest()}`). Not frozen. No score computed, printed or stored. "
             "Waiting for the author's written GO quoting the sha256.\n")
    L.append("## 1.1 The registered padding rule of the existing padding experiment, verbatim (file, line numbers)\n")
    L.append("The experiment behind `tab:pad`'s upper block and the sentence \"padding ... to 60 names lowers the lookup to 0.67\" (0.7484 → 0.6696) is "
             "`registrations/ADDENDUM_PAD.md` (registered text sha256 `93e33022…`, frozen at `dab8956`), built by `pad_probe/tools/pad_common.py` / `run_pad.py`. "
             "Its Amendment 1 (`contam.py`) rendered lists into the 444 v2 texts with the same renderer. In short: pad names come from the persona's own printed name map "
             "(pool A) and then other personas' FULL:TRUE maps (pool B); one shuffle per summary key under `random.Random(f\"42:{key}\")`, pool A first, taken in order "
             "(nested across 15/30/60); the committed names are kept (the target's own name among them) and the pad fills to exactly L; the section is re-rendered as a "
             "**sorted set** (alphabetical), wrapped at 150 with indents two and four; the fifteen-name cap (`index_v2.SLOT_CAP = 15`) is lifted to 100 by setting "
             "`index_v3.SLOT_CAP` around `_name_block`; the text above the section header — the lifecycle totals, the per-category counts, the name map — is "
             "byte-identical, so **the counts do not change** and the `superseded` total disagrees with the list's length in every padded summary.\n")
    for path, a, b, why in QUOTES:
        L.append(f"**`{path}` lines {a}–{b}** — {why}\n\n```\n{quote(path, a, b)}\n```\n")
    L.append("## 1.2 Can the rule be applied unchanged to the 444 under the three constraints?\n")
    L.append("**No.** Four things must differ; everything else carries over unchanged (the renderer and the lifted cap, the sorted rendering, D-PAD-3's fragment rule, "
             "the byte-identical prefix, the counts left as committed, D-PAD-2's wide exclusion).\n")
    L.append("1. **Same pad within a triple → seed per triple, not per summary key.** The rule seeds `42:{key}` and the three versions are three keys "
             "(`cf2:<pair>|PN`, `|PRESENT`, `|ABSENT`), so they would draw three different pads. The pad is drawn once per `pair_id` (`random.Random(f\"42:{pair_id}\")`) "
             "and every version's list is its own committed names plus that pad, in that draw order (the section then prints them sorted, identically for the shared names).\n")
    L.append("2. **The target stays out of the pad → pool A from the intersection of the three versions' maps, and the change set excluded.** The rule takes pool A from one "
             "text's printed map. Across a triple the maps differ: the target sits in the PN and PRESENT maps and not in the ABSENT map, and when the target enters a "
             f"15-name category it displaces the alphabetically last name (symmetric difference across the three maps: {cen['map_symdiff']} triples by size). A name printed in one "
             "version and not another cannot be a shared pad name and would be a name the change adds or removes. Pool A is therefore the names printed in **all three** maps, "
             "less (i) every name in **any** version's committed section, less (ii) the persona's targets — in the counterfactual set its pairs' target slots and every slot the "
             f"PN versions add (23 triples add a second slot beside the target, e.g. `health_condition` beside `health_metric`; 7 of those print it in the PN committed list), "
             "in the main study D-PAD-2's wide set — less (iii) `:`/whitespace names, less (iv) the change set (map symmetric difference ∪ PN-added slots ∪ target), asserted "
             "explicitly. Exclusion (ii) over both populations is what `nb6_sweep.pools` did for the injection amendment on the same 444 ('in either population'). "
             f"Pool A then holds {cen['pool_a']['min']}–{cen['pool_a']['max']} names (median {cen['pool_a']['median']}), so no triple reaches pool B and every pad name is a name the "
             "committed summary already prints in its map.\n")
    L.append("3. **Pad size fixed by the PN version and shared.** The rule fills each list to exactly L. Filling each version to 60 separately would give the siblings one "
             "pad name the PN version lacks (its slot is taken by the target), breaking constraint 1. The pad has 60 − |committed(PN)| names; the PN list has exactly 60, "
             f"a sibling's list is shorter by the names only the PN committed section carries: list lengths over the 444 are {cen['list_length']['histogram']} "
             "(59 on the siblings of 81 supersession triples, 58 on those of 6, 57 on those of 1; 60 on every PN item and every counted-state item, whose three committed lists coincide). "
             "This keeps the brief's reading: the versions differ only in what the store's change adds, as the unpadded lists do (1 or 2 names against `(none)`). "
             "*Alternative the author may prefer:* pad every list to 60 by giving the siblings one extra pad name (then length carries no signal at all, but the siblings hold a name the "
             "PN version does not); not implemented, one switch if ruled.\n")
    L.append("4. **Target position is not informative → nothing to change; printed.** The registered ordering is the sorted set, so the target's position is its alphabetical rank "
             f"among the 60. Over the 88 supersession PN lists: min {cen['target_position_pn_supersession']['min']}, median {cen['target_position_pn_supersession']['median']}, "
             f"max {cen['target_position_pn_supersession']['max']}, mean {cen['target_position_pn_supersession']['mean']:.1f}; first position {cen['target_position_pn_supersession']['first']} times, "
             f"last position {cen['target_position_pn_supersession']['last']} times; by tenths of the list (six positions each) "
             f"{' / '.join(str(cen['target_position_pn_supersession']['deciles'][str(d)]) for d in range(1, 11))}. The last tenth is heavier (targets beginning with late letters); "
             "the rank is never first and is last on 4 of 88. Full histogram: "
             f"{cen['target_position_pn_supersession']['histogram']}.\n")
    L.append("Also carried over from the 661 rule and worth the author's eye: **the counts are not touched** (the `superseded` total reads 1 in a PN summary that lists 60 names, "
             "0 in its siblings that list 59) — the same disagreement the registered probe on the 661 carried; the brief's \"Nothing else in the summary changes\" is read as keeping it.\n")
    L.append("## 1.3 Draft registration\n")
    L.append(f"`registrations/ADDENDUM_CF_PAD.md`, registered-text sha256 **`{sha}`**. Full text at the end of this file (§A).\n")
    L.append("## 1.4 Dry run ($0; `cf_pad/tools/run_cf_pad.py dryrun`; `cf_pad/build/dryrun_build.json`, `dryrun_texts.json`, `dryrun_log.txt`)\n")
    L.append("The three lookups (embedding, word-matching, random-token) were run on the 444 padded lists and discarded: 444 finite scores each, nothing printed or stored. "
             "The three on the **committed** lists reproduce the recorded gates 0.7663 / 0.6698 / 0.5954 at four decimals (PASS ×3), and the seven recorded Table 1 vectors "
             "reproduce their gates (PASS ×7).\n")
    L.append(f"- renderer lock on the committed v2 texts: **{cen['renderer_lock']} of 444**\n"
             f"- list lengths: min {cen['list_length']['min']}, median {cen['list_length']['median']}, max {cen['list_length']['max']} (mean {cen['list_length']['mean']:.2f}); "
             f"by state and version: " + "; ".join(f"{k} {v['min']}–{v['max']} (n {v['n']})" for k, v in cen['list_length']['by_state_version'].items()) + "\n"
             f"- pad sizes (60 − |committed(PN)|): {cen['n_pad']}; triples drawing on pool B: **{cen['from_pool_b_pairs']}**; pool A min/median/max "
             f"{cen['pool_a']['min']}/{cen['pool_a']['median']}/{cen['pool_a']['max']}; pool B {cen['pool_b']['min']}/{cen['pool_b']['median']}/{cen['pool_b']['max']}\n"
             f"- change-set sizes: {cen['change_set']}; names excluded from the intersections by (ii): {cen['excluded_by_ii']['from_intersection_total']} "
             f"({cen['excluded_by_ii']['cf2_only_total']} by the counterfactual pairs' targets and PN-added slots, {cen['excluded_by_ii']['e1_only_total']} by the 661-cell targets alone)\n"
             f"- target position (PN, supersession): see 1.2 item 4\n"
             f"- **leak scan: {cen['leak_scan']['n_fails']} fails** (every pad name a scrubbed slot name of the persona's store; no `:` or whitespace; no pad name equal to a stored entry's text; "
             f"no target and no PN-added slot in any PRESENT or ABSENT list beyond what its committed section already lists; pads identical across each triple's versions; no `(+N more)`); "
             f"descriptive: {cen['leak_scan']['descriptive']} — the substring cases are ordinary words (`rent` inside `current`, `age` inside `associates`, `friend`, `business`, `budget`), "
             "listed in the dry-run log\n"
             f"- prompt sizes (o200k, system + user): committed mean {cen['prompt_tokens_o200k']['committed_mean']:.0f}, padded mean {cen['prompt_tokens_o200k']['padded_mean']:.0f} "
             f"(max {cen['prompt_tokens_o200k']['padded_max']}), ratio {cen['prompt_tokens_o200k']['ratio_mean']:.3f}, +{cen['prompt_tokens_o200k']['extra_mean']:.0f} tokens per prompt\n"
             f"- padded texts sha256 `{cen['texts_sha256']}`; indexes sha256 `{cen['indexes_sha256']}`\n")
    L.append("### One rendered triple in full\n\n```\n" + triple.strip() + "\n```\n")
    L.append("## 1.5 Cost projection (`cf_pad/tools/run_cf_pad.py project`; `cf_pad/build/projection.json`)\n")
    L.append("Per lane: the recorded Table 1 lane's own rows (arm INDEXED-V2), each row's prompt-side tokens scaled by its item's padded/committed o200k ratio, completion tokens "
             "kept, priced at the page prices (OpenAI: plain input, cache writes at 1.25× for Luna/Sol, cached reads at the cached rate, output; draw 1 as the recorded draw 1, "
             "later draws as the mean of the recorded later draws, which ran 99.8% cached; Anthropic: input and output at Batch's 50%) — the 'anchored' column — beside a plain "
             "price formula; the planning figure is the larger, ×1.3 against the cap.\n")
    L.append("| lane | k | calls | prompt/call | out/call | formula | anchored | planning | ×1.3 | no cache | 3 draws |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lane, r in P["lanes"].items():
        L.append(f"| {lane} | {r['k']} | {r['calls']} | {r['prompt_tokens_mean']:.0f} | {r['recorded']['tok_out_mean']:.1f} | ${r['usd_expected']:.2f} | ${r['usd_anchored']:.2f} | "
                 f"${r['usd_planning']:.2f} | ${r['usd_planning_x1.3']:.2f} | {('$%.2f' % r['usd_no_cache']) if 'usd_no_cache' in r else '—'} | "
                 f"{('$%.2f' % r['usd_anchored_3_draws']) if r.get('usd_anchored_3_draws') else '—'} |")
    t = P["totals"]
    L.append(f"\n- **Anthropic:** planning ${t['anthropic']:.2f}, ×1.3 **${t['anthropic_x1.3']:.2f}** against the $12 cap — fits.\n"
             f"- **OpenAI:** planning ${t['openai']:.2f}, ×1.3 **${t['openai_x1.3']:.2f}** against the $18 cap — **the margin figure exceeds the cap by ${t['openai_x1.3'] - 18:.2f}**; "
             f"the planning figure sits ${18 - t['openai']:.2f} under it. With Sol at three draws the OpenAI planning figure is "
             f"${t['openai'] - P['lanes']['gpt-5.6-sol']['usd_planning'] + P['lanes']['gpt-5.6-sol']['usd_anchored_3_draws']:.2f} "
             f"(×1.3 ${(t['openai'] - P['lanes']['gpt-5.6-sol']['usd_planning'] + P['lanes']['gpt-5.6-sol']['usd_anchored_3_draws']) * 1.3:.2f}). Sol is the last OpenAI lane, so the "
             "registration's cap rule (Sol to three draws first) is what a breach would truncate. If the OpenAI cache did not engage, Sol alone would project $23.23; the draw-major "
             "order engages it and the metering halts at the cap.\n")
    L.append("## Points for the author's ruling (none blocks the GO; each is a one-line answer)\n")
    L.append("1. **The OpenAI cap.** Keep $18 and accept that Sol may complete three or four whole draws (the registered fallback, a dated deviation), or raise the OpenAI cap to "
             "$20 so the ×1.3 figure fits with Sol at five. The registration is drafted at $18.\n"
             "2. **Sibling list length.** Drafted as the brief reads (identical pads; siblings 58–60 names, the PN list 60). The alternative (every list 60, the siblings holding one "
             "extra pad name) is one switch.\n"
             "3. **Counts untouched** (the `superseded` total disagrees with the list length, as in the 661 probe). Drafted as untouched (\"Nothing else in the summary changes\").\n"
             "4. **Where `cf_pad_printed.json` lives.** Drafted as `reviews/r136/results/` (beside the report); `cf_pad/results/` is the `para_printed.json` analogue if preferred.\n"
             "5. **Prediction reading.** Each prediction is read on the primary endpoint (pooled AUROC, supersession slice) with the matched reading printed beside; P-L4 on point "
             "estimates with a gain counting as losing less. Say if any should read differently.\n")
    L.append("## §A — The draft registration, verbatim (registered text; sha256 `" + sha + "`)\n")
    L.append("```markdown\n" + reg_text.rstrip("\n") + "\n```\n")
    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print(f"wrote {OUT.relative_to(ROOT)}  registered-text sha256 {sha}")


if __name__ == "__main__":
    main()
