r"""_secdiff.py -- show what differs in one appendix section between a revision and now."""
import difflib
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]
                       / "iclr2027_monitoring_submission" / "tools"))
from appendix_identity import REL, TEX, sections  # noqa: E402

rev = sys.argv[1]
want = sys.argv[2]
root = pathlib.Path(__file__).resolve().parents[2]
old = sections(subprocess.run(["git", "show", f"{rev}:{REL}"], capture_output=True,
                              check=True, cwd=root).stdout.decode("utf-8", "replace"))
cur = sections(TEX.read_text(encoding="utf-8", errors="replace"))
a = old.get(want, "").replace("\r\n", "\n").split("\n")
b = cur.get(want, "").replace("\r\n", "\n").split("\n")
print(f"{want}: {len(a)} lines at {rev} -> {len(b)} now")
n = 0
for line in difflib.unified_diff(a, b, lineterm="", n=0):
    if line.startswith(("---", "+++")):
        continue
    print("  " + line[:150])
    n += 1
    if n > 24:
        print("  ...")
        break
if n == 0:
    print("  (identical)")
