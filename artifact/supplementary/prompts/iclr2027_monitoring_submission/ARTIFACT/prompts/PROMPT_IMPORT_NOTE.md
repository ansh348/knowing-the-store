# Prompt provenance note

`prompts_e1.py` is the frozen file of record for every E1, ladder, and cross-vendor
monitor call. Its identity is hash-pinned twice:

- `registrations/PREREG_E1.md` (line 11) records the frozen file sha256 (`ce5911e6…`)
  and texts sha256 (`f6a97e45…`).
- `manifests/cell_84.json` records `prompts_file_sha256` and `prompts_texts_sha256` for
  the cross-vendor cell.

The cross-vendor elicitation harness (`e1xv_crossvendor/tools/elicit_e1xv.py` in the
repository) does not carry its own prompt text: it imports `prompts_e1` and uses
`P.SYSTEM` / the frozen user prompts verbatim. That import is what backs the paper's
"same frozen prompts" claim (§5.2). If you relocate files, verify the hashes above
against `prompts_e1.py` rather than trusting any copy's path.

`prompts_e0.py` (pilot) is deliberately different from E1 — the pilot prompt assumed
lifecycle structure two backends do not expose (§4.1), which is why E0 and E1 values are
not comparable. `prompts_e2.py` contains the 2³ NOK-factorial prompt variants (App F.5).
