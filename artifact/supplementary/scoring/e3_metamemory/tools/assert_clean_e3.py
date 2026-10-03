"""
assert_clean_e3.py -- phase-boundary hygiene assertion for E3. NO API CALLS.

E2's `assert_clean.py` IMPORTED AND RUN, not re-implemented: its two checks, its
regenerable-hash device and its exit semantics are the ones ledger Incident 8 put
in force. The only things E3 changes are the guarded trees and the tool
directories, which are module constants.

  AN UNTRACKED FILE THAT A COMMITTED ARTIFACT READS FROM IS A STOP CONDITION.

Exit 0 = boundary may be crossed. Exit 1 = stop.

Usage:  python e3_metamemory/tools/assert_clean_e3.py [--boundary NAME]
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "e2_metamemory" / "tools"))

import assert_clean as AC                                          # noqa: E402

AC.GUARDED = ["e0_metamemory", "e1_metamemory", "e2_metamemory", "e3_metamemory",
              "HEADLINE.md", "LANDSCAPE.md", "SCOOP_RULE.md"]
AC.TOOL_DIRS = [ROOT / "e1_metamemory" / "tools",
                ROOT / "e2_metamemory" / "tools",
                ROOT / "e3_metamemory" / "tools"]

if __name__ == "__main__":
    AC.main()
