# -*- coding: utf-8 -*-
"""pin_appendix_int.py -- the integration pass (R112, 2026-09-16): run appendix_identity against the v19 base tree and append the R112 pins
(EXEMPT basis + PINS hash) for every appendix section the pass changed, each with its reason. Idempotent per hash. The same shape as
reviews/v19/tools/pin_appendix_a1.py. Usage: python reviews/v19/tools/pin_appendix_int.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R112 (2026-09-16, the integration pass; the author's instruction and six corrections of that day; CLAIMS.md R112 block, the R112-INT entries; "
        "reviews/integration/INTEGRATION_REPORT.md; reviews/v19/tools/integ_apply.py, integ_insert.py, integ_cuts.py, integ_fix1.py, every edit asserted): ")
REASONS = {
    "A": "Table tab:setup moved here verbatim from Section 4 (the page-budget step); tab:populations and tab:runs define the same populations in full. The carried tables' row labels luna / sol read GPT-5.6 Luna / GPT-5.6 Sol (v19_prompt.md R8; REPAIRS_R112, asserted counts).",
    "C.2": "the PN-versus-PRESENT paragraph and Table tab:pnpresent (post hoc, specified before recomputation; AUX-WP-B-*), the intent note (AUX-WP-B4-INTENT), 'the gain is the AUROC minus 0.5000' (review-2 F3), 'reliably' for 'both intervals excluding zero' in editable lines (item 26).",
    "E.1": "the EXPIRED-column sentence restated under the primary-tag / derived-expiry formalism of Section 3 (review-2 F2).",
    "E.5": "the count-destruction caption's ledger path replaced by 'the artifact's R108 ledger' (item 73).",
    "E.7": "the carried marker paragraph's 'A reviewer asked' reads 'A review asked' (item 73; REPAIRS_R112 in build_v19.py, asserted once). The carried tables' row labels luna / sol read GPT-5.6 Luna / GPT-5.6 Sol (v19_prompt.md R8; REPAIRS_R112, asserted counts).",
    "E.8": "the whole-map lookup on the easy tier (post hoc F1, AUX-WP-F1-WHOLEMAP): one row added to tab:cov-lookup, its caption extended, one sentence added; 'reliably' for 'both intervals excluding zero' in editable lines. The carried tables' row labels luna / sol read GPT-5.6 Luna / GPT-5.6 Sol (v19_prompt.md R8; REPAIRS_R112, asserted counts).",
    "E.9": "Table tab:levels moved here verbatim from Section 7 (the page-budget step); the trial paragraph's last sentence replaced by the pointer to the forty-persona census (Appendix G.4) and the statement that the summary and tag routes on this backend have not been run; 'both reliable' for 'both intervals excluding zero'.",
    "E.10": "Table tab:routes moved here verbatim from Section 6 (the page-budget step); the audit's read stated as one reader's, not an independent validation (review-2 W1); the ledger paths of the audit sentence replaced (item 73); 'reliable' for 'both intervals excluding zero' in editable lines. The carried tables' row labels luna / sol read GPT-5.6 Luna / GPT-5.6 Sol (v19_prompt.md R8; REPAIRS_R112, asserted counts).",
    "E.11": "the forty-persona Graphiti ingestion added to the spend sentence (AUX-R85-G10-INGEST, $11.88 of a $13.22 stop).",
    "E.12": "new subsection: the provenance table of the headline numbers (review-2 F5).",
    "F": "the registration record gains the R85 Amendment 1 row (frozen 43132a3; P1 failed on recall, held on precision; P2 to P4 not run).",
    "G": "the opener gains the 'specified before recomputation' convention with the spec file's sha256 (ae2600fc).",
    "G.3": "content unchanged; the section's span no longer runs to the end of the document because G.4 follows it.",
    "G.4": "new subsection: the fourth backend at forty personas (AUX-R85-G10-*; D-R85-16; the registered P1 text quoted verbatim).",
}
ARGS = [BASE, "--tex=paper_v19.tex", "--base=iclr2027_monitoring_submission/paper_v18.tex"]
out = subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout
pins = re.findall(r"to authorize this state, add to PINS:\s+(['\"])(.+?)\1: '([0-9a-f]{64})'", out)
removed = re.findall(r"REMOVED\s+UNLISTED\s+(.+?)\n", out)
entries = [(k, h) for _, k, h in pins] + [(k.strip(), "REMOVED") for k in removed]
if not entries:
    print("nothing to pin\n", out[-800:]); sys.exit(0)


def reason(k):
    key = k.split(":")[0].strip()
    r = REASONS.get(key)
    assert r, f"no reason recorded for the changed section {k!r}"
    return HEAD + r + " No number, n, interval or population changed except the new ledgered post-hoc and census rows."


src = TOOL.read_text(encoding="utf-8")
block = "\n# R112 (2026-09-16): pins for the integration pass (reviews/v19/tools/pin_appendix_int.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
