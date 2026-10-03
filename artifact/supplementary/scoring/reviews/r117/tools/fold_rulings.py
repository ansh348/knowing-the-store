# -*- coding: utf-8 -*-
"""fold_rulings.py -- program R117: fold the author's rulings of 2026-09-19 (reviews/r116/RULINGS_R116.md) into the five registration
drafts of reviews/r117/registrations_draft/ before the freeze. Each replacement is asserted to occur exactly once; idempotent (a second
run finds every NEW present). Run once, then the drafts move to registrations/ for the freeze commit.
"""
import io
import pathlib

D = pathlib.Path(__file__).resolve().parents[1] / "registrations_draft"


def edit(fn, pairs):
    p = D / fn
    t = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if t.count(new) == 1 and t.count(old) == 0:
            continue
        assert t.count(old) == 1, (fn, old[:60], t.count(old))
        t = t.replace(old, new)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("folded", fn)


# E1: cap 22; Batch exactly like the recorded draw
edit("ADDENDUM_V2R_CAT_AMENDMENT_1.md", [
    ("DRAFT for the author's freeze (program R117, Phase 0, 2026-09-18; drafted BEFORE any call; not frozen, not run).",
     "Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: cap 22 USD, draws 2 to 5 through Batch exactly like the recorded draw, max_tokens 1024, temperature unset)."),
    ("the repo's ×1.3 launch margin gives **$21.0 against the $20 cap**, so the lane launches only on a ruling (cap raised to $22, or the expected reading accepted as the test). Hard stop in the runner at the cap.",
     "the repo's ×1.3 launch margin gives $21.0 against the **cap of $22** (the author's ruling of 2026-09-19). Hard stop in the runner at the cap."),
])

# E2: line removal primary; the committed A3 dash rule a secondary arm for mini only; counts only by line removal
edit("ADDENDUM_CF2_NAMES_COUNTS.md", [
    ("DRAFT for the author's freeze (program R117, Phase 0, 2026-09-18; drafted BEFORE any call; not frozen, not run).",
     "Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: names only by line removal is the primary form for both readers, the committed A3 dash rule a secondary arm for GPT-4.1 mini only, counts only by line removal)."),
    ("**Author's decision at the freeze:** this line-removal form (the prompt's words), or the committed E1.8 A3 form (`e1_metamemory/tools/mechanism_arms.py`: every count replaced by `-`, structure kept), which is the \"names-only\" the paper already prints for the pooled hard tier (0.8516, Table 28). The two are not the same rendering; the draft takes the line-removal form.",
     "This line-removal form is the **primary** names-only arm (the author's ruling). **NAMES-DASH (secondary, GPT-4.1 mini only):** the committed E1.8 A3 rule (`e1_metamemory/tools/mechanism_arms.py`, `rewrite` with `a3`: every count replaced by `-`, structure kept), the rendering the paper already calls names-only on the pooled hard tier (0.8516, Table 28), applied unchanged to the v2 text; it prints beside the primary arm and carries no prediction."),
    ("Arms `INDEXED-NAMES` and `INDEXED-COUNTS`, 444 items each. GPT-4.1 mini: k = 1,",
     "Arms `INDEXED-NAMES` and `INDEXED-COUNTS`, 444 items each, for both readers; `INDEXED-NAMES-DASH`, 444 items, GPT-4.1 mini only. GPT-4.1 mini: k = 1,"),
    ("Projected from the recorded CF-2 rows and the offline token count of the two renderings (o200k_base plus the constant 11-token template offset; NAMES-ONLY 1,181 tokens mean, COUNTS-ONLY 1,009, against v2's 1,616): GPT-4.1 mini 888 calls **$0.43**;",
     "Projected from the recorded CF-2 rows and the offline token count of the renderings (o200k_base plus the constant 11-token template offset; NAMES-ONLY 1,181 tokens mean, COUNTS-ONLY 1,009, NAMES-DASH about 1,616, against v2's 1,616): GPT-4.1 mini 1,332 calls **$0.74**;"),
    ("**$5.06 against the $10 cap (×1.3: $6.6)**", "**$5.37 against the $10 cap (×1.3: $7.0)**"),
    ("`-NC-MINI-NAMES`, `-NC-MINI-COUNTS`,", "`-NC-MINI-NAMES`, `-NC-MINI-NAMES-DASH`, `-NC-MINI-COUNTS`,"),
    ("Locks asserted per version before any call: NAMES-ONLY carries no digit outside the RECENCY block and the age sentence;",
     "Locks asserted per version before any call: NAMES-ONLY carries no digit outside the RECENCY block and the age sentence; NAMES-DASH reproduces `mechanism_arms`' own assertions (only counts moved, every count a dash, ages byte-identical);"),
])

# E3: Run B reused; P-X1 dropped; the Neutral wording fixed; the wrapper's quoted marker replaced; Luna four raw-API arms
edit("ADDENDUM_MARKER_ABLATION.md", [
    ("DRAFT for the author's freeze (program R117, Phase 0, 2026-09-18; drafted BEFORE any call; not frozen, not run). Carries one prediction (P-X2) with its failure text and two readings that are already on the record or descriptive (P-X1, P-X3).",
     "Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: E1.5 Run B reused as the mini Omitted arm and reported as a recorded result, P-X1 dropped for mini, P-X2 kept for the Neutral arm, the Neutral wording fixed, the wrapper's quoted marker string replaced by the same text, Luna on four raw-API arms). Carries one prediction (P-X2) with its failure text and one descriptive reading (P-X3)."),
    ("- **NEUTRAL** (new): each of the three marker bodies `not expressible by this backend` becomes **`This store does not record this. Judge it from the question alone.`** (the author may edit this wording before the freeze; fixed after it); the section headers stay; every other line byte-identical to the intact text. Wrapper: **author's decision at the freeze** — `USER_INDEXED` verbatim (its sentence then explains a marker phrase that no longer appears) or `USER_INDEXED_NOMARKER` (the draft's default: the neutral sentence carries what the wrapper's sentence said). Built by a committed pure function, `e1_metamemory/tools/marker_arms.py`, lock asserted per key: exactly three replaced lines, nothing else changed.",
     "- **NEUTRAL** (new): each of the three marker bodies `not expressible by this backend` becomes **`This store does not record this. Judge it from the question alone.`** (fixed by the author's ruling of 2026-09-19); the section headers stay; every other line byte-identical to the intact text. Wrapper: `prompts_e1.USER_INDEXED` with its quoted marker string `\"not expressible by this backend\"` replaced by the same text, `\"This store does not record this. Judge it from the question alone.\"`, and nothing else in the wrapper changed (the ruling); the variant is built at run time from the frozen text by that one substitution, asserted, and its sha256 recorded. Built by a committed pure function, `e1_metamemory/tools/marker_arms.py`, lock asserted per key: exactly three replaced lines, nothing else changed."),
    ("- Blind and intact: the recorded rows.",
     "- **STRUCTURAL** (the intact constrained rendering, `indexes_v2.json` `...:TRUE`, the recorded arm) and **BLIND**: recorded rows for GPT-4.1 mini; run through the raw API for Luna (below)."),
    ("GPT-5.6 Luna on the pooled 66, k = 5, raw Chat Completions API, effort and temperature unset, `max_completion_tokens` 2048 (the R74 X4 settings), MIN_DRAWS 3, **four arms: BLIND, INTACT, OMITTED, NEUTRAL** (1,320 calls).",
     "GPT-5.6 Luna on the pooled 66, k = 5, raw Chat Completions API, effort and temperature unset, `max_completion_tokens` 2048 (the R74 X4 settings), MIN_DRAWS 3, **four arms: BLIND, STRUCTURAL, OMITTED, NEUTRAL** (1,320 calls; the ruling)."),
    ("- **P-X1 (on the record, reported, not predicted).** Under OMITTED the paired loss against blind shrinks by at least half on both backends for GPT-4.1 mini. The recorded Run B rows already decide it: A-MEM $-0.1065 \\to -0.0378$ (shrinks by 65%), Mem0 $-0.0969 \\to -0.0865$ (11%). **The reading FAILS on Mem0 and holds on A-MEM**; it prints as a recorded result, and the registration does not re-predict it.",
     "- **The Omitted arm for GPT-4.1 mini is a recorded result, not a prediction** (the ruling; P-X1 dropped): the E1.5 Run B rows print as they stand, A-MEM $-0.1065 \\to -0.0378$ (the loss shrinks by 65%), Mem0 $-0.0969 \\to -0.0865$ (11%), with both intervals recomputed by this addendum's scorer beside the recorded ones."),
    ("- **P-X3 (descriptive).** The share of items at the modal score falls under both new arms against intact, on each backend and for Luna on the 66.",
     "- **P-X3 (descriptive).** The share of items at the modal score falls under OMITTED and under NEUTRAL against STRUCTURAL, on each backend for GPT-4.1 mini and on the 66 for Luna."),
    ("`e1_metamemory/NUMBERS.md` section 12: `AUX-MARKER-LOCK`, `-OMITTED-MINI` (from the Run B rows), `-NEUTRAL-MINI`, `-LUNA-66` (four arms), `-MODAL`, `-P-X1`, `-P-X2`, `-P-X3`, `-SPEND`.",
     "`e1_metamemory/NUMBERS.md` section 12: `AUX-MARKER-LOCK`, `-OMITTED-MINI` (from the Run B rows, a recorded result), `-NEUTRAL-MINI`, `-LUNA-66` (four arms), `-MODAL`, `-P-X2`, `-P-X3`, `-SPEND`."),
    ("(the tie census).\n",
     "(the tie census). The Luna comparisons (OMITTED and NEUTRAL against BLIND and STRUCTURAL) are read within the raw-API transport; the recorded harness rows on the 66 print beside as the rows they are, marked as Appendix B marks them.\n"),
])

# E4: matching by the census function unchanged; the age-field ordering; a secondary offline arm without the ordering
edit("ADDENDUM_DS_AMENDMENT_8.md", [
    ("DRAFT for the author's freeze (program R117, Phase 0, 2026-09-18; drafted BEFORE any call; not frozen, not run).",
     "Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call, the author's rulings of 2026-09-19 folded in: matching by the census function unchanged, the age-field ordering, one secondary offline arm without the ordering condition)."),
    ("2. Untagged line $u$ **matches** tagged line $s$ when $a_u = a_s$, $|\\mathrm{toks}(x_s) \\cap \\mathrm{toks}(x_u)| \\ge 2$ (`MIN_SHARED`) and $\\mathrm{cov}(\\mathrm{toks}(x_s), \\mathrm{toks}(x_u)) \\ge 0.80$ (the census threshold `TAU_HI`, the coverage of the tagged line's content tokens by the untagged line's). **Author's decision at the freeze:** coverage of all of $s$'s content tokens (the draft), or of the tokens of $s$ not shared with the newest active non-matching line of the slot (the census's discriminative form, `index_v2.detect`), which needs such a line to exist.\n"
     "3. **Ordering.** $u$ receives $s$'s tag only if $u$ was written before the slot's value changed. The event time is not on the line, so: let $m$ be the newest active line of attribute $a_u$ that does **not** match $s$ (the smallest age among such lines); $u$ propagates iff no such $m$ exists or $g_u > g_m$. A line with $g_u \\le g_m$ is a return to the old value and stays active.",
     "2. **Matching (the ruling: same attribute, the census function unchanged).** For a tagged line $s$, its **successor candidate** $m$ is the newest active line (smallest age) with $a_m = a_s$ whose text does not repeat $s$'s at the census threshold ($\\mathrm{cov}(\\mathrm{toks}(x_s), \\mathrm{toks}(x_m)) < 0.80$). Where $m$ exists, the untagged lines of attribute $a_s$ are scored by `index_v2.detect(old_fact = x_s, new_fact = x_m, etoks, drop)` exactly as the census scores an entry against a manifest pair: $u$ matches iff $|D_{old} \\cap \\mathrm{toks}(x_u)| \\ge 2$ (`MIN_SHARED`), $\\mathrm{cov}(D_{new}, \\mathrm{toks}(x_u)) < 0.34$ (`CROSS_GUARD`) and $\\mathrm{cov}(D_{old}, \\mathrm{toks}(x_u)) \\ge 0.80$ (`TAU_HI`), with $D_{old} = \\mathrm{toks}(x_s) \\setminus \\mathrm{toks}(x_m)$, $D_{new} = \\mathrm{toks}(x_m) \\setminus \\mathrm{toks}(x_s)$ and `MIN_DISCR` 3 on both sides (a pair the function declares unresolvable propagates nothing and is counted). Where no $m$ exists there is no new value: $D_{old} = \\mathrm{toks}(x_s)$, $D_{new} = \\emptyset$, the cross guard vacuous, the same two thresholds.\n"
     "3. **Ordering (the ruling, on the age field).** Where $m$ exists, $u$ propagates only if it is older than the newest such line: $g_u > g_m$. Where no $m$ exists, $u$ propagates only if it is no newer than its tagged line: $g_u \\ge g_s$. A line failing the condition is a return to the old value and stays active."),
    ("Locks asserted before any call: the rule reproduces itself on a second pass (idempotent); no line changes except its lifecycle field; the count of changed views and lines per policy and tag source is recorded before answering.",
     "**Secondary arm (registered, offline only; the ruling):** the same rule with no ordering condition (step 3 dropped), scored for measures (i) and (ii) only, never re-answered; it prints beside the primary as the catch and false-propagation ceiling of the matching step.\n\nLocks asserted before any call: the rule reproduces itself on a second pass (idempotent); no line changes except its lifecycle field; the count of changed views and lines per policy, tag source and arm is recorded before answering."),
    ("`-A8-RULE-CENSUS` (changed views and lines per policy and tag source), `-A8-DUP35`, `-A8-FALSEPROP`,",
     "`-A8-RULE-CENSUS` (changed views and lines per policy, tag source and arm), `-A8-DUP35`, `-A8-FALSEPROP` (both arms),"),
])

# E5: as drafted
edit("ADDENDUM_CF2_OPENAI.md", [
    ("DRAFT for the author's freeze (program R117, Phase 0, 2026-09-18; drafted BEFORE any call; not frozen, not run).",
     "Registration for the author's freeze (program R117; drafted 2026-09-18 BEFORE any call; accepted as drafted by the author's ruling of 2026-09-19)."),
])
print("rulings folded")
