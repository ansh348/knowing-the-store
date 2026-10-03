# -*- coding: utf-8 -*-
"""claims_r133_block.py -- the R133 AUTHORIZATION BLOCK of CLAIMS.md (program R133, the readability pass, v23; 2026-09-21), written to
reviews/v23/claims_r133_block.md and appended to iclr2027_monitoring_submission/CLAIMS.md once (idempotent: the block is replaced in place when it already
exists, so a re-run after a further gate run refreshes the quoted list). Entries: one per unit of reviews/v23/tools/port_r133.py that has been applied
(read from reviews/v23/results/port_r133_log.json), the gate interactions, and R133-F, which quotes every frozen string of the v22 close that the pass
changed (from the frozen_<tag>.json named by --json=, written by frozen_list_wp.py), so frozen_diff --program=R133 reads each as CHANGED-AUTHORIZED. A quoted
string is a fragment between double quotes; where a frozen string itself carries a double quote, its longest quote-free fragment of 30+ characters is
quoted instead (frozen_diff authorizes a string when a quoted fragment is contained in it).
Usage: python reviews/v23/tools/claims_r133_block.py [--json=reviews/v23/results/frozen_<tag>.json]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
CLAIMS = SUB / "CLAIMS.md"
BLOCK = ROOT / "reviews" / "v23" / "claims_r133_block.md"
LOG = ROOT / "reviews" / "v23" / "results" / "port_r133_log.json"
HEAD = "## R133 AUTHORIZATION BLOCK — dated 2026-09-21"

ENTRIES = {
    "homes": ("R133-HOMES [section 4: the coverage homes]", "Appendix A gains the paragraph 'Coverage notes for the daggers in the main text' after tab:runs (five items, (i) to (v): "
              "mini's one-call row under the names-and-counts ablation; Luna five draws and Opus one draw under the count removal with Sol not run; the all-states summary on mini, Haiku and Opus only; "
              "the intent crossover's draw counts and Sol's later addition; the full obligation set completed by Haiku, Luna and Opus with Sol and Kimi stopped at the budget), each the facts of "
              "tab:runs, tab:setup, tab:cf-names-counts, tab:cf-nc-strong, tab:cf-matched, tab:cf-intent and tab:x4-expansion restated. Table 74 (tab:provenance), row 1: 'lookup $0.77$ and models $0.72$ to $0.84$' "
              "was stale against Table 1 as built (0.72 is mini's one-draw temperature-0 row of Table 1's note a; 0.84 omits Sol's 0.85) and reads 'lookup $0.77$ and models $0.76$ to $0.85$' "
              "(r125_matched.json readers/{MINI5_v2 0.7648, H45_v2 0.7566, LUNA_v2 0.8417, SOL_v2 0.8500, OP5_v2 0.8405}/gate; reviews/v23/tools/r133_number_gate.py). Nothing deleted from the appendix."),
    "swaps": ("R133-SWAPS [section 5: the author's verbatim swaps S1 to S11]", "Each swap verbatim from the brief, its numbers through r133_number_gate.py (32 checks, 0 mismatches; S3's Haiku pair on the same population and conditions as mini's and the lookup's: the 661, the ground-truth summary against FR-Bank's capped store-written summary, "
              "AUX-R74-X4-H45-NOK 0.8210 and AUX-BH-H45-15 0.7069 beside AUX-E1R-TRUE-NOK 0.7339 / AUX-E1R-BELIEVED-NOK 0.5959 and AUX-E1R-NB6 0.7484 / 0.5858; S2's 0.05 to 0.06 AUX-CF2-HYB-VS-MODELS +0.0540, +0.0553, +0.0635, each reliable). "
              "Old beside new for every swap is reviews/v23/OLD_BESIDE_NEW_V23.md (the swap unit). The abstract, Section 1 and the Conclusion change by these swaps only; no gate rewords a swap."),
    "s4": ("R133-S4 [section 6: Section 4 rewritten from its second paragraph]", "The models paragraph in the form of section 4.2 (the five models and their short names; Kimi K3 (open weights); the five-draw sentence; the one coverage sentence pointing to Appendix A and its daggers). Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s51": ("R133-S51 [section 6: Section 5.1 rewritten]", "The three paragraphs in the shape of section 6.1 (plain words first, at most three numbers in prose, the appendix pointer once at the end); the second paragraph is the brief's worked example (section 7) with its numbers through r133_number_gate.py; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s52": ("R133-S52 [section 6: Section 5.2 rewritten]", "The paragraphs in the shape of section 6.1; the count-feature paragraph is the brief's worked example (section 7) with its numbers through r133_number_gate.py; the pooled and matched split stated once at the top; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s53": ("R133-S53 [section 6: Section 5.3 rewritten; S10]", "The rubric point explicit in one sentence (S10); the paragraphs in the shape of section 6.1. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s6": ("R133-S6 [section 6: Section 6 rewritten]", "The paragraphs in the shape of section 6.1; Table 2's numbers not repeated in prose; the Mem0 and A-MEM paragraph keeps U5 and its four conditions verbatim; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s7": ("R133-S7 [section 6: Section 7 rewritten]", "The paragraphs in the shape of section 6.1; the inverted-tag bookkeeping to Appendix E.10's paragraph; the hike carried once. Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "s8": ("R133-S8 [section 6: Section 8 rewritten]", "The two paragraphs in the shape of section 6.1, the full-set comparison marked with a dagger resolving to Appendix A's note (v). Old beside new in reviews/v23/OLD_BESIDE_NEW_V23.md."),
    "rulings": ("R133-RULINGS [the author's R133 RULINGS of 2026-09-21]", "1: the abstract keeps S3; Section 1's thesis sentence reads \"In these tests, every reader we tried was held back by what the store had written down.\" "
                "and the Conclusion's first sentence \"In these tests, no reader we tried made up for what the store had failed to write down.\" (both verbatim from the ruling), so the thesis sentence no longer repeats; "
                "the repeat_scan EXEMPT and slogan_scan EXEMPT_S7 exemptions R133-G added are removed and both scans pass unexempted (gate_edits_r133.py --rulings); slogan_scan's EXEMPT_S9 entry for S2's abstract "
                "sentence stays (the abstract is unchanged and S9 would otherwise fail it); prose_scan's WHITELIST carries the two ruled sentences for rule V ('held', 'failed' in their ordinary senses; the R101 precedent). "
                "2: E.9's 'loss of content with over-marking' approved. 3: tab:routes (Appendix E.10) gains GPT-4.1 mini's per-state view-minus-summary rows for expiry and supersession with both intervals, "
                "from resp_review/run/scores_resp.json (AUX-RESP-L2-MINI-NOK; reviews/NUMBERS_R133.md AUX-R133-ROUTES-PERSTATE; r133_number_gate.py 47 checks, 0 mismatches), and Section 7 keeps the direction in prose and points to the table. "
                "4: H26 stays. 5: the three 'reliable' candidates of REPORT_R133.md section 9 dropped (5.2's random-token margin, Section 6's Mem0 and A-MEM losses, Section 8's cross-vendor gains); no further cuts. 6: no action, awaiting ruling."),
    "s12": ("R133-S12 [section 5, S12: the optional Limitations sentence]", "Added because the final slack was +3 or better: 'Counts cannot say which record changed: two stores that cancel different plans in one category can share a summary, so only a named state identifies the obligation.'"),
}


def quotable(text):
    if '"' not in text:
        return text
    parts = [p.strip() for p in text.split('"')]
    best = max(parts, key=len)
    assert len(best) >= 30, text
    return best


def flat(s):
    return s.strip().replace("\n\n", " [paragraph break] ").replace("\n", " ")


def main():
    js = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--json=")), None)
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {"units": [], "edits": []}
    units = log["units"]
    L = [HEAD, "",
         "Program R133: the v23 lineage, opened from the R131 close `b3cc631` (`reviews/v23/`, base tree `0ec9c4ad`; `reviews/v23/tools/bump_v23.py`), the readability pass of the author's brief "
         "'R133: V23 READABILITY PASS' (2026-09-21): bookkeeping hedges out of the running prose of Sections 4 to 8 into their appendix homes (`reviews/v23/HEDGE_LEDGER.md`), the author's "
         "claim-narrowing swaps S1 to S12, Sections 4 to 8 rewritten. No number changes value, population or condition; no new claims; nothing deleted from the appendix. The edits are "
         "`reviews/v23/tools/port_r133.py` (every edit asserted), the number gate `reviews/v23/tools/r133_number_gate.py`, the report `reviews/v23/REPORT_R133.md`, the sign-off file "
         "`reviews/v23/OLD_BESIDE_NEW_V23.md`. frozen_diff runs with `--program=R133` against the v23 base; v22 is frozen and is the fallback build.", ""]
    for u in units:
        title, text = ENTRIES[u]
        L.append(f"- **{title}** (recorded). {text}")
    if "swaps" in units:
      L.append("- **R133-G [the gate interactions]** (recorded). tools/slogan_scan.py: EXEMPT_S7 (new; the R131 close's B4 precedent) carries the thesis sentence the author's S3 and S4 put verbatim in the abstract and Section 1, "
             "and EXEMPT_S9 carries S2's abstract sentence ('but not when all items are pooled'); tools/prose_scan.py WHITELIST: the R131 close's B4 entry (the abstract's thesis sentence) is replaced by its S3 form, "
             "the rule D pair with Section 1 (S4, identical) and the Conclusion (S6) overridden by the author's swaps. G2 stands by pattern. code_scan's 'registered' collocations stand. "
             "Every rule V or D override inside Sections 4 to 8 is listed old beside new in REPORT_R133.md.")
    if js:
        rows = json.loads((ROOT / js).read_text(encoding="utf-8"))
        changed = [r for r in rows if r["status"] != "KEPT"]
        L.append(f"- **R133-F [the frozen strings of the v22 close that the pass changed; `{js}`]** (recorded). Each string below occurred in paper_v22.tex and occurs a different number of times in paper_v23.tex "
                 "(a count of zero means the sentence left the text; the sentence carrying the claim now, where one does, is in reviews/v23/OLD_BESIDE_NEW_V23.md). Every one is authorized as changed by the pass under the entries above.")
        for r in changed:
            L.append(f"  - {r['status']} [{r['tag']} {r['key']}] {r['base']} -> {r['new']}: \"{flat(quotable(r['text']))}\"")
    text = "\n".join(L) + "\n"
    BLOCK.write_text(text, encoding="utf-8", newline="\n")
    claims = CLAIMS.read_text(encoding="utf-8", errors="replace")
    crlf = "\r\n" in claims
    c = claims.replace("\r\n", "\n")
    if HEAD in c:
        i = c.index(HEAD)
        m = re.search(r"^## (?!R133 AUTHORIZATION)", c[i + len(HEAD):], flags=re.M)
        j = i + len(HEAD) + m.start() if m else len(c)
        c = c[:i] + text + ("\n" if m else "") + c[j:]
        what = "replaced"
    else:
        c = c.rstrip("\n") + "\n\n" + text
        what = "appended"
    CLAIMS.write_bytes((c.replace("\n", "\r\n") if crlf else c).encode("utf-8"))
    n = len([r for r in (json.loads((ROOT / js).read_text(encoding='utf-8')) if js else []) if r["status"] != "KEPT"])
    print(f"-> {BLOCK} (units {units}; {n} frozen strings quoted); CLAIMS.md block {what}")


if __name__ == "__main__":
    main()
