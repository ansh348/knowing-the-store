# Adaptations to the staged copies

Every script here is the repository's own, byte for byte, except for the edits below.
They exist because the archive is not a git checkout and carries no provider keys.
Each is printed old beside new. Nothing else in any shipped script was altered.

## `reviews/v23/tools/r134_number_gate.py`

**Why.** the gate reads the previous paper from git to know which numerals are new. An unpacked archive is not a git checkout, and paper_v22.tex does not ship: it is half a megabyte of superseded draft and it carries two further copies of the FR-Bank citation. The two numeral sets the check actually reads are derived from it by the packager, with this file's own split() and numerals(), and travel as data/iclr2027_monitoring_submission/v22_numerals.json (57 KB). Inside a checkout the git path still runs and nothing changes.

Old:

```python
    old = subprocess.run(["git", "show", f"{BASE}:iclr2027_monitoring_submission/paper_v22.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8", errors="replace")
    nm, na = split(new)
    om, oa = split(old)
    new_main = numerals(nm) - numerals(om)
    new_appx = numerals(na) - numerals(oa)
```

New:

```python
    old = subprocess.run(["git", "show", f"{BASE}:iclr2027_monitoring_submission/paper_v22.tex"], cwd=ROOT, capture_output=True).stdout.decode("utf-8", errors="replace")
    nm, na = split(new)
    if "\\begin{abstract}" in old:
        om, oa = split(old)
        om_nums, oa_nums = numerals(om), numerals(oa)
    else:
        # R138: an unpacked archive is neither a git checkout nor a place the previous draft
        # belongs. The packager derived these two sets from paper_v22.tex with the split()
        # and numerals() above, so this is the same check on the same input, reduced to the
        # only part of it the check reads.
        import json as _json
        _base = _json.loads((SUB / "v22_numerals.json").read_text(encoding="utf-8"))
        om_nums, oa_nums = set(_base["main"]), set(_base["appendix"])
    new_main = numerals(nm) - om_nums
    new_appx = numerals(na) - oa_nums
```

## Files deliberately removed

Two kinds of script are kept out of this archive rather than redacted into it. The redaction pass rewrites names in text; a script whose *purpose* is to carry those names as match patterns cannot survive that pass as a working script, and a broken one is worse than an absent one.

### `iclr2027_monitoring_submission/tools/hygiene_scan.py`

This is the anonymity gate itself, so its pattern list IS the identity: both surnames in three encodings each, the given name, the institution and the code-hosting handle prefix, written as live regexes. The text scrub rewrote the two plain-text entries and could not touch the encoded ones, which left the file both leaking and half-broken. A fully redacted copy would be worse than no copy: it would look like a working identity gate and report clean on anything. Nothing in reproduce_all.py calls it; its gates are r137_number_gate, trace_scan_v13 and refcheck_v11. run_gates.py, which does call it, is the paper-build battery and needs pdflatex and a git checkout, neither of which this archive is.

### `reviews/v23/tools/close_checks_r134.py, close_checks_r135.py, close_checks_r137.py`

The per-pass close checks grep the built PDF for the author strings. The scrub turned each pattern into the literal placeholder, which as a regex is a character class matching any of its letters, so the shipped copies would have reported nonsense rather than a result. They are close-read bookkeeping, not part of any printed number.

### `reviews/r141/tools/sweep_repo_r141.py, reviews/r141/results/sweep_repo_r141.json`

R141's sweep of the whole repository for identity strings, run before this archive was built. It imports this builder's own term list and records, per file, which identity terms it found, so it carries the identity for the same reason hygiene_scan.py does. It is pre-upload bookkeeping and feeds no printed number.
