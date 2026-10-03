# -*- coding: utf-8 -*-
"""gate_edits_r137.py -- the gate and tool changes R137 needs, each asserted and idempotent; listed in reviews/v23/REPORT_R137.md and CLAIMS.md R137-G.

  reviews/v23/tools/build_v23.py        the six CFPAD tables (cf_pad/results/cfpad_tab_<name>.tex, cfpad_tex.py) spliced at the %%CFPAD-TABLE:<name>%% markers port_r137.py writes into Appendix C.2
  reviews/v23/tools/run_gates.py        r137_number_gate.py in place of r135_number_gate.py (it runs R135's and R134's checks first)
  reviews/v23/tools/number_moves_wp.py  cf_pad/results/cf_pad_scores.json walked for the appendix tables' tokens; Figure 1's transcribed LIFECYCLE TOTALS dispositioned (ADDED); the tokens the
                                        old row 9 carried that leave the body dispositioned where numeric_diff reports them
  tools/trace_scan_v13.py               LEDGERS gains cf_pad/NUMBERS_CF_PAD.md and reviews/NUMBERS_R137.md
  tools/prose_scan.py                   an AUTHOR-RULING entry for the abstract's own sentence only if a prose rule fires inside it (--abstract-entries; the brief's rule)
Usage: python reviews/v23/tools/gate_edits_r137.py [--abstract-entries]
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "iclr2027_monitoring_submission" / "tools"
V23T = ROOT / "reviews" / "v23" / "tools"


def edit(path, pairs):
    raw = path.read_bytes()
    crlf = b"\r\n" in raw
    t = raw.decode("utf-8").replace("\r\n", "\n")
    for old, new in pairs:
        if new in t:
            continue   # already applied (the new text may begin with the old line)
        assert t.count(old) == 1, (path.name, old[:80])
        t = t.replace(old, new)
    path.write_bytes((t.replace("\n", "\r\n") if crlf else t).encode("utf-8"))


def main():
    # build_v23.py: the CFPAD markers
    edit(V23T / "build_v23.py", [(
        '    assert "%%PARA-TABLE" not in appx, "unresolved PARA marker"\n',
        '    assert "%%PARA-TABLE" not in appx, "unresolved PARA marker"\n'
        '    # R137 (2026-09-22): the long-list check\'s tables (cf_pad/results/cfpad_tab_<name>.tex, written by cf_pad/tools/cfpad_tex.py from cf_pad_scores.json, one file per table)\n'
        '    # spliced in Appendix C.2 at the %%CFPAD-TABLE:<name>%% markers (written by reviews/v23/tools/port_r137.py); no table value is typed in a source.\n'
        '    for name in ("sup", "minus-lookup", "whole", "counted", "other-lookups", "position"):\n'
        '        mk = f"%%CFPAD-TABLE:{name}%%\\n"\n'
        '        if mk in appx:\n'
        '            assert appx.count(mk) == 1, mk\n'
        '            appx = appx.replace(mk, read(ROOT / "cf_pad" / "results" / f"cfpad_tab_{name}.tex"))\n'
        '    assert "%%CFPAD-TABLE" not in appx, "unresolved CFPAD marker"\n')])
    # run_gates.py: the number gate
    edit(V23T / "run_gates.py", [(
        '    out, rc = run([PY, str(TOOLS / "r135_number_gate.py"), "--built"], cwd=ROOT)\n    L.append(f"r135_number_gate (R134\'s checks included; --built): {last(out, 2)}")\n',
        '    # R137 (2026-09-22): r137_number_gate.py runs R134\'s and R135\'s checks and the pass\'s own, then the numeral-set checks with the pass\'s printed forms and the CFPAD fragments allowed\n'
        '    out, rc = run([PY, str(TOOLS / "r137_number_gate.py"), "--built"], cwd=ROOT)\n    L.append(f"r137_number_gate (R134\'s and R135\'s checks included; --built): {last(out, 2)}")\n')])
    # number_moves_wp.py: the CF_PAD scores walked; Figure 1's transcribed totals
    edit(V23T / "number_moves_wp.py", [(
        '                      ("ds_downstream/run/lock_amend8.json", "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP (DS Amendment 8; Section 7, Appendix E.10 tab:ds-a8)")):\n',
        '                      ("ds_downstream/run/lock_amend8.json", "ds_downstream/NUMBERS_DS.md section 15, AUX-DS-A8-RULE-CENSUS, -DUP35, -FALSEPROP (DS Amendment 8; Section 7, Appendix E.10 tab:ds-a8)"),\n'
        '                      # R137 (2026-09-22), the long-list check landed (cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*; the printed forms reviews/NUMBERS_R137.md AUX-R137-PRINTED)\n'
        '                      ("cf_pad/results/cf_pad_scores.json", "cf_pad/NUMBERS_CF_PAD.md AUX-CFP-READERS-*, -MINUS-LOOKUP-*, -MINUS-LEX-*, -MINUS-RANDTOK-*, -POSITION, -OP5-D1, -P-L1 to -P-L4, -SPEND (the 60-name lists; Section 5.2, the abstract, Sections 1 and 10, tab:robust row 9, Appendix C.2 tab:cfpad-*, Appendix F)"),\n'
        '                      ("cf_pad/build/lock.json", "cf_pad/NUMBERS_CF_PAD.md AUX-CFP-LOCK (the build census: list lengths, pools, the target\'s rank; Appendix C.2)")):\n'),
        ('    **{k: "tab:routes (Appendix E.10), the per-state rows added by R133 RULINGS 3: " + v for k, v in (\n',
         '    # R137 (2026-09-22), Part B 5.1: Figure 1\'s rendered summary transcribes the LIFECYCLE TOTALS block of the summary the E.1 excerpt was cut from (ARTIFACT/manifests/indexes_v2.json\n'
         '    # frbank:david:FULL:BELIEVED; AUX-R86-INDEX-EXCERPT names the same summary; reviews/NUMBERS_R137.md AUX-R137-FIG1, through r137_number_gate.py)\n'
         '    \'377\': "Figure 1: the summary\'s LIFECYCLE TOTALS, active (frbank:david:FULL:BELIEVED, transcribed; AUX-R137-FIG1)",\n'
         '    \'197\': "Figure 1: the summary\'s LIFECYCLE TOTALS, superseded (AUX-R137-FIG1)",\n'
         '    \'49\': "Figure 1: the summary\'s LIFECYCLE TOTALS, expired (AUX-R137-FIG1)",\n'
         '    # R137: Appendix C.2\'s long-list paragraph prints the target\'s median rank in the PN list as the ledger records it (cf_pad/build/lock.json target_position median 41.5; AUX-CFP-LOCK)\n'
         '    \'41.5\': "Appendix C.2, the long-list check: the target\'s median alphabetical rank in the 60-name PN list over the 88 supersession triples (cf_pad/build/lock.json target_position; AUX-CFP-LOCK)",\n'
         '    **{k: "tab:routes (Appendix E.10), the per-state rows added by R133 RULINGS 3: " + v for k, v in (\n')])
    # number_moves_wp.py: the old Figure 1's tikz coordinate token (Part B 5.1)
    edit(V23T / "number_moves_wp.py", [(
        "VANISHED = {\n    # R135 (2026-09-21), section 2.1:",
        "VANISHED = {\n"
        "    # R137 (2026-09-22), Part B 5.1: the schematic Figure 1 replaced by the rendered summary; its tikz coordinate '(0,-3.5mm)' carried the bare token\n"
        "    '0': \"the old Figure 1's tikz coordinate (0,-3.5mm), a layout constant, removed with the schematic (R137 Part B 5.1); not a research number (the W/T/L zeros and the counts print as before)\",\n"
        "    # R135 (2026-09-21), section 2.1:")])
    # r134_number_gate.py numerals(): minipage widths and makebox lengths are layout, as the p{} column specs are (R135)
    edit(V23T / "r134_number_gate.py", [(
        '    text = re.sub(r"p\\{[^}]*\\}", " ", text)          # R135: tabular column specs (p{0.255\\linewidth}) are layout, as trace_scan_v13 drops them\n',
        '    text = re.sub(r"p\\{[^}]*\\}", " ", text)          # R135: tabular column specs (p{0.255\\linewidth}) are layout, as trace_scan_v13 drops them\n'
        '    text = re.sub(r"\\\\begin\\{minipage\\}(\\[[^\\]]*\\])?\\{[^}]*\\}", " ", text)   # R137: minipage widths (0.625\\linewidth) are layout (Figure 1\'s rendered summary)\n'
        '    text = re.sub(r"\\\\makebox\\[[^\\]]*\\](\\[[^\\]]*\\])?", " ", text)              # R137: makebox lengths (7em) are layout\n')])
    # trace_scan_v13.py: the two ledgers
    edit(TOOLS / "trace_scan_v13.py", [(
        '    pathlib.Path("../reviews/NUMBERS_R135.md"),\n]\n',
        '    pathlib.Path("../reviews/NUMBERS_R135.md"),\n'
        '    # R137 (2026-09-22, the long-list check landed): the six C.2 tables (tab:cfpad-*) print four-decimal values of cf_pad/results/cf_pad_scores.json (cf_pad/NUMBERS_CF_PAD.md AUX-CFP-*,\n'
        '    # written by cf_pad/tools/report_cf_pad.py); the two-decimal forms of tab:robust row 9, Section 5.2, the abstract, Sections 1 and 10, the recount, Figure 1\'s transcribed totals and the\n'
        '    # appendix prose\'s counts are reviews/NUMBERS_R137.md AUX-R137-* (reviews/v23/tools/ledger_r137.py, from the checks of r137_number_gate.py), each beside its source.\n'
        '    pathlib.Path("../cf_pad/NUMBERS_CF_PAD.md"),\n'
        '    pathlib.Path("../reviews/NUMBERS_R137.md"),\n]\n')])
    print("gate edits applied: build_v23.py (CFPAD markers), run_gates.py (r137_number_gate), number_moves_wp.py (cf_pad_scores.json, lock.json; Figure 1's totals), trace_scan_v13.py (NUMBERS_CF_PAD.md, NUMBERS_R137.md)")
    if "--abstract-entries" in sys.argv:
        raise SystemExit("no abstract entry defined yet: add it here if a prose rule fires inside the abstract's own sentence (REPORT_R137.md lists it)")


if __name__ == "__main__":
    main()
