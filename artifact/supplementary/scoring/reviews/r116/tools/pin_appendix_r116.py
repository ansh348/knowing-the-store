# -*- coding: utf-8 -*-
"""pin_appendix_r116.py -- program R116 (2026-09-18, the provenance fix; reviews/r115/PROVENANCE_AUDIT.md; the author's Appendix R):
run appendix_identity against the v19 base tree and append the R116 pins (EXEMPT basis + PINS hash) for the appendix sections the
fix changed, each with its reason. Idempotent per hash. The same shape as reviews/r115/tools/pin_appendix_r115.py.
Usage: python reviews/r116/tools/pin_appendix_r116.py
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SUB = ROOT / "iclr2027_monitoring_submission"
TOOL = SUB / "tools" / "appendix_identity.py"
BASE = (ROOT / "reviews" / "v19" / "base_tree.txt").read_text().strip()
HEAD = ("R116 (2026-09-18, the provenance fix: reviews/r115/PROVENANCE_AUDIT.md, the author's Appendix R of 18 September; "
        "reviews/r116/tools/r116_apply.py, every edit asserted; CLAIMS.md R116 block): ")
REASONS = {
    "E.10": "Appendix R item 3: the sentence 'Each was preregistered with its texts written before any call (Table b)' gains 'by commit except DS Amendment 4 and Graphiti Amendment 2, which hold by the runner's record'.",
    "F": "Appendix R item 2: (a) the carried table a's R81 row cites the registration file's first commit 5c3621b75e in place of a prefix no commit has (build_v19.py REPAIRS_R116_BLOCK, keyed to the carried block 2084-2118, asserted once); (b) table b labels DS Amendment 4's fb4b2ca8c8 '(file hash)' as Graphiti Amendment 2's is; (c) table c's caption reads 'hashed by the runner before its first call (the commits of 18 September do not date them)'; (d) one paragraph after table c states the lock mechanism and names the lock-attested set (CF-3; DS Amendments 1 to 4, Q4, RESP Amendment 1, Graphiti Amendment 2).",
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
    return HEAD + r + " No number, n, interval or population changed."


src = TOOL.read_text(encoding="utf-8")
block = "\n# R116 (2026-09-18): pins for the provenance fix (reviews/r116/tools/pin_appendix_r116.py wrote this block from the tool's own report).\n"
block += "EXEMPT.update({\n" + "".join(f"    {k!r}: {reason(k)!r},\n" for k, _ in entries) + "})\n"
block += "PINS.update({\n" + "".join(f"    {k!r}: {h!r},\n" for k, h in entries) + "})\n"
marker = "\n\ndef sections(text):"
assert marker in src
src = src.replace(marker, block + marker, 1)
TOOL.write_text(src, encoding="utf-8")
print(f"pinned {len(pins)} sections, {len(removed)} removed: {[k for k, _ in entries]}")
print(subprocess.run([sys.executable, str(TOOL)] + ARGS, cwd=SUB, capture_output=True, text=True).stdout[-600:])
