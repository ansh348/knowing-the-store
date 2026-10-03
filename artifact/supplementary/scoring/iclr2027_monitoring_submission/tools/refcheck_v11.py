"""refcheck_v11 = refcheck_v10 + explicit coverage + a coverage gate.

WHY THIS VERSION EXISTS (D-R74-15). v10 prints two adjacent, unlabelled lines:
`bibitem count: 26` (the whole bibliography) and, further down, `ALL VERIFIED` (scoped
only to the 16 keys that have an `official` metadata record). Reading them together
yields "26 bibitems ALL VERIFIED", which is false: 10 entries carry no metadata record
and are never checked by the tool at all. The R75-V report line made exactly that
conflation. v10's verdict logic was never wrong -- its REPORTING invited a false
coverage claim, and `REFCHECK_V10.md` had to carry the coverage split in prose to
compensate.

WHAT CHANGED. No verdict logic changes: the same 16 records, the same five fields
(id/venue, title, year, lead author, et-al guard), the same MISMATCH rule. v11 adds:
  1. an explicit COVERAGE block -- bibitems / checked / declared-out-of-scope;
  2. an OUT_OF_SCOPE registry, transcribed from REFCHECK_V10.md's own table, so every
     unchecked entry names its verification basis in the tool rather than only in prose;
  3. THE STRICTER GATE: a bibitem that is in neither `official` nor `OUT_OF_SCOPE` is a
     FAILURE. Under v10 a newly added citation with no metadata record passed silently;
     under v11 it cannot. This is the gate pinned going forward.
  4. a summary line that always states its own scope, so it cannot be quoted as coverage
     it does not have.

Usage: python tools/refcheck_v11.py paper.tex
Exit 0 only if every checked record VERIFIES and every bibitem is accounted for.

R78 REGISTRY NOTE. Two records were added for the paper_v2 lineage after both
reviewer-supplied citations were verified on their arXiv abstract pages (2026-08-24):
`hushbench` (2606.06055) and `statemembench` (2608.19652). The frozen paper.tex does
not cite them, so running THIS file against paper.tex correctly fails with two ORPHAN
records — that is the gate doing its job, not a defect. To regression-check the frozen
lineage, run the v11 at commit 0684fdd:
  git show 0684fdd:iclr2027_monitoring_submission/tools/refcheck_v11.py > /tmp/refcheck_v11_frozen.py
  python /tmp/refcheck_v11_frozen.py paper.tex

R93 REGISTRY NOTE (2026-09-11). Thirty-five reviewer-relayed references enter paper_v5.tex.
Two are arXiv-only and join `official` (kadavath2022, packer2023); the other 33 are venue,
journal or book records and join OUT_OF_SCOPE, each basis string naming the DOI, anthology id
or listing it was VERIFIED against (REFCHECK_V12.md; raw fetch reviews/R93_refcheck_raw.json).
Running this file against paper_v4.tex now fails with 35 ORPHAN records, which is the gate
doing its job for the frozen lineage; run `git show fdd34c8:...refcheck_v11.py` for v4.
"""
import re, pathlib, sys

tex = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
bib = tex[tex.index(r"\begin{thebibliography}"):tex.index(r"\end{thebibliography}")]
items = bib.split(r"\bibitem")[1:]

# ---- the checked population: full metadata records (identical to v10) ---------------
official = {
    "mem0": ("2504.19413", "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory", "2025", "P.~Chhikara"),
    "knowact": ("2607.29433", "Know It, Act on It: Investigating Memory Utilization in LLM Personalization", "2026", "Z.~Feng"),
    "knowbutnotact": ("2605.14186", "LLMs Know When They Know, but Do Not Act on It: A Metacognitive Harness for Test-time Scaling", "2026", "Q.~Cao"),
    "memgate": ("2606.06054", "Beyond Similarity: Trustworthy Memory Search for Personal AI Agents", "2026", "J.~Zhang"),
    "seakr": ("2406.19215", "SeaKR: Self-aware Knowledge Retrieval for Adaptive Retrieval Augmented Generation", "2024", "Z.~Yao"),
    "stale": ("2605.06527", "STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?", "2026", "H.~Chao"),
    "verbrouting": ("2607.25600", "Beyond Self-Knowledge: Propagating Uncertainty Across Reasoning and Retrieval in LLMs", "2026", "C.~K. Sah"),
    "memoryagentbench": ("ICLR", "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions", "2026", "Y.~Hu, Y.~Wang, and J.~McAuley"),
    "abstentionbench": ("2506.09038", "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions", "2025", "P.~Kirichenko, M.~Ibrahim, K.~Chaudhuri, and S.~J. Bell"),
    "pmbench": ("2607.12385", "PM-Bench: Evaluating Prospective Memory in LLM Agents", "2026", "G.~Liu and S.~Gabriel"),
    "cimemories": ("2511.14937", "CIMemories: A Compositional Benchmark for Contextual Integrity of Persistent Memory in LLMs", "2025", "N.~Mireshghallah"),
    "supersede": ("2606.27472", "Supersede: Diagnosing and Training the Memory-Update Gap in LLM Agents", "2026", "V.~Patel"),
    "gatemem": ("2606.18829", "GateMem: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents", "2026", "Z.~Ren"),
    "memora": ("2604.20006", "From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents", "2026", "M.~N. Uddin"),
    "automem": ("2607.01224", "AutoMem: Automated Learning of Memory as a Cognitive Skill", "2026", "S.~Wu"),
    "metamem": ("2602.11182", "MetaMem: Evolving Meta-Memory for Knowledge Utilization through Self-Reflective Symbolic Optimization", "2026", "H.~Xin"),
    # R78 additions (A1 REFCHECK-FIRST, both VERIFIED on arXiv abs pages 2026-08-24):
    "hushbench": ("2606.06055", "HUSH-Bench: Measuring Memory-Use Boundaries for Sensitive History in Conversational Agents", "2026", "L.~Xu"),
    "statemembench": ("2608.19652", "Can Agent Memory Systems Track Evolving State?", "2026", "X.~Fan"),
    # R87 Phase A (R86-5 item 7): Appendix F.9 names the fourth backend. Record VERIFIED by
    # arXiv API in reviews/R80_CITATIONS.md (rasmussen2025).
    "zep": ("2501.13956", "Zep: A Temporal Knowledge Graph Architecture for Agent Memory", "2025", "P.~Rasmussen"),
    # R89 (2026-09-11), BRANCH A of the W1 gate: the prior-store preprint is public. Title and
    # both authors verified against the arXiv API and abs page on 2026-09-11 (published
    # 2026-09-09, cs.AI). The lead-author string is the two-author body form the gate expects.
    "fr": ("2609.10413", "Fortunate Recall: Ontology-Driven Memory Lifecycle Management for Persistent Coherence in LLMs", "2026", "A.~Mullick and E.~T"),
    # R93 (2026-09-11): the two arXiv-only records among the 35 reviewer-relayed references, both
    # fetched from the arXiv API (REFCHECK_V12.md; raw record reviews/R93_refcheck_raw.json).
    "kadavath2022": ("2207.05221", "Language Models (Mostly) Know What They Know", "2022", "S.~Kadavath"),
    "packer2023": ("2310.08560", "MemGPT: Towards LLMs as Operating Systems", "2023", "C.~Packer"),
}
SINGLE_AUTHOR = {"supersede"}
TWO_AUTHOR = {"pmbench", "fr"}
THREE_AUTHOR = {"memoryagentbench"}

# ---- the declared-unchecked population, transcribed from REFCHECK_V10.md -------------
# Entries outside the arXiv-record discipline. Naming them here is what lets the gate
# distinguish "deliberately out of scope" from "silently uncovered".
OUT_OF_SCOPE = {
    "amem":          "NeurIPS 2025 venue citation; venue metadata, no arXiv ID printed",
    "flare":         "EMNLP 2023 venue citation; venue metadata, no arXiv ID printed",
    "locomo":        "ACL 2024 venue citation; venue metadata, no arXiv ID printed",
    "longmemeval":   "ICLR 2025 venue citation; venue metadata, no arXiv ID printed",
    "selfrag":       "ICLR 2024 venue citation; venue metadata, no arXiv ID printed",
    "koriat1996":    "Psychological Review 103(3):490-517; journal metadata",
    "nelson1990":    "Psychology of Learning and Motivation 26:125-173; journal metadata",
    "openaimemory":  "product note; VERIFIED 2026-08-30 from the vendor page, dated 4 June 2026 (REFCHECK_V11 section 3)",
    # R93 (2026-09-11): the 33 venue, journal and book records among the reviewer-relayed references.
    # Each names the primary record it was VERIFIED against on 2026-09-11 (REFCHECK_V12.md section 1).
    "hart1965":        "J. Educational Psychology 56(4):208-216; VERIFIED Crossref DOI 10.1037/h0022263",
    "koriat1993":      "Psychological Review 100(4):609-639; VERIFIED Crossref DOI 10.1037/0033-295X.100.4.609",
    "metcalfe1994":    "MIT Press edited volume, 1994; VERIFIED Crossref DOI 10.7551/mitpress/4561.001.0001 + Open Library ISBN 9780262132985",
    "dunlosky2009":    "Sage Publications textbook, 2009; VERIFIED Open Library ISBN 9781412939720 (single source, noted in REFCHECK_V12)",
    "lin2022":         "TMLR 2022 venue citation; VERIFIED jmlr.org/tmlr/papers listing + arXiv 2205.14334",
    "tian2023":        "EMNLP 2023 venue citation; VERIFIED Crossref DOI 10.18653/v1/2023.emnlp-main.330",
    "xiong2024":       "ICLR 2024 venue citation; VERIFIED iclr.cc/virtual/2024 listing + arXiv 2306.13063 comment",
    "mallen2023":      "ACL 2023 venue citation; VERIFIED Crossref DOI 10.18653/v1/2023.acl-long.546",
    "ren2025":         "COLING 2025 venue citation; VERIFIED ACL Anthology 2025.coling-main.250 (pp. 3697-3715)",
    "wang2023":        "Findings of EMNLP 2023 venue citation; VERIFIED Crossref DOI 10.18653/v1/2023.findings-emnlp.691",
    "su2024":          "ACL 2024 venue citation; VERIFIED Crossref DOI 10.18653/v1/2024.acl-long.702 (camera-ready title, 'Real-time')",
    "lewis2020":       "NeurIPS 2020 venue citation; VERIFIED proceedings.neurips.cc 6b493230205f780e1bc26945df7481e5 (NeurIPS 33, pp. 9459-9474)",
    "rajpurkar2018":   "ACL 2018 venue citation; VERIFIED Crossref DOI 10.18653/v1/P18-2124",
    "kamath2020":      "ACL 2020 venue citation; VERIFIED Crossref DOI 10.18653/v1/2020.acl-main.503",
    "yang2024":        "NeurIPS 2024 venue citation; VERIFIED Crossref DOI 10.52202/079017-2030 + proceedings.neurips.cc 2024 listing",
    "zhong2024":       "AAAI 2024 venue citation; VERIFIED Crossref DOI 10.1609/aaai.v38i17.29946",
    "zhang2025survey": "ACM TOIS 43(6):1-47, 2025; VERIFIED Crossref DOI 10.1145/3748302",
    "nissenbaum2004":  "Washington Law Review 79(1):119-158, 2004; VERIFIED bepress record (first page 119; last page bounded by article 11's first page 159)",
    "maini2024":       "COLM 2024 venue citation; VERIFIED colmweb.org/2024/AcceptedPapers.html + arXiv 2401.06121 (R80: OpenReview API)",
    "xu2024conflicts": "EMNLP 2024 venue citation; VERIFIED Crossref DOI 10.18653/v1/2024.emnlp-main.486",
    "longpre2021":     "EMNLP 2021 venue citation; VERIFIED Crossref DOI 10.18653/v1/2021.emnlp-main.565",
    "dhingra2022":     "TACL 10:257-273, 2022; VERIFIED Crossref DOI 10.1162/tacl_a_00459",
    "hanley1982":      "Radiology 143(1):29-36; VERIFIED Crossref DOI 10.1148/radiology.143.1.7063747",
    "naeini2015":      "AAAI 2015 venue citation; VERIFIED Crossref DOI 10.1609/aaai.v29i1.9602",
    "guo2017":         "ICML 2017 venue citation; VERIFIED proceedings.mlr.press/v70/guo17a (PMLR 70:1321-1330) + arXiv 1706.04599",
    "zadrozny2002":    "KDD 2002 venue citation; VERIFIED Crossref DOI 10.1145/775047.775151",
    "platt2000":       "MIT Press chapter, Advances in Large-Margin Classifiers pp. 61-74, 2000; VERIFIED Crossref DOI 10.7551/mitpress/1113.003.0008 (chapter title 'Probabilities for SV Machines')",
    "geifman2017":     "NeurIPS 2017 venue citation; VERIFIED proceedings.neurips.cc 4a8423d5e91fda00bb7e46540e2b0cf1 + arXiv 1705.08500",
    "brier1950":       "Monthly Weather Review 78(1):1-3; VERIFIED Crossref DOI 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2",
    "efron1993":       "Chapman & Hall book, 1993; VERIFIED Open Library ISBN 9780412042317 + Crossref DOI 10.1007/978-1-4899-4541-9",
    "cameron2008":     "Review of Economics and Statistics 90(3):414-427; VERIFIED Crossref DOI 10.1162/rest.90.3.414",
    "nosek2018":       "PNAS 115(11):2600-2606; VERIFIED Crossref DOI 10.1073/pnas.1708274114",
    "pineau2021":      "JMLR 22(164):1-20, 2021; VERIFIED jmlr.org/papers/v22/20-303 + arXiv 2003.12206",
    # R123 (2026-09-19, the v21 update and writing pass, Phase D): the three references of the Related Work sentence on precedents of lifecycle
    # tags, each VERIFIED against its Crossref DOI record on 2026-09-19 (reviews/NUMBERS_R123.md AUX-R123-REFS).
    "doyle1979":       "Artificial Intelligence 12(3):231-272, 1979; VERIFIED Crossref DOI 10.1016/0004-3702(79)90008-0",
    "snodgrass1986":   "Computer 19(9):35-42, 1986; VERIFIED Crossref DOI 10.1109/MC.1986.1663327",
    "shapiro2011":     "SSS 2011, LNCS, pages 386-400, Springer; VERIFIED Crossref DOI 10.1007/978-3-642-24550-3_29",
}

found = {}
for it in items:
    m = re.search(r"\]\{([^}]+)\}", it)
    if not m:
        continue
    found[m.group(1)] = re.sub(r"\s+", " ", it[m.end():]).strip()

fails = []

# R115 (2026-09-18): the nine bibitems no citation reached (Cao 2026, Dunlosky & Metcalfe 2009, Feng 2026, Metcalfe & Shimamura 1994,
# Naeini 2015, Nosek 2018, Pineau 2021, OpenAI 2026, Zhang 2026) were removed from the bibliography under the author's ruling; their
# records stay above for the history and are not orphans.
# R139 (2026-09-22), sweep S2: the five bibitems no citation reached (Ren 2025, Sah 2026, Wang 2023, Xin 2026, Yao 2024) removed from the bibliography; their records stay above.
RETIRED = {'knowbutnotact', 'dunlosky2009', 'knowact', 'metcalfe1994', 'naeini2015', 'nosek2018', 'pineau2021', 'openaimemory', 'memgate',
           'ren2025', 'verbrouting', 'wang2023', 'metamem', 'seakr'}

# ---- direction 1: every checked record verifies (v10 logic, unchanged) --------------
print(f"bibitem count: {len(found)}")
print()
print(f"CHECKED against a full metadata record ({len(official)} of {len(found)}):")
for k in sorted(official):
    if k in RETIRED:
        continue                    # R115: the bibitem was removed; the record stays for the history
    aid, title, yr, lead = official[k]
    b = found.get(k, "")
    plain = b.replace("\\emph{", "").replace("}", "").replace("{", "")
    ok_id, ok_title = aid in b, title in plain
    ok_yr = re.search(r"\b" + yr + r"\b", b) is not None
    ok_lead = plain.startswith(lead)
    ok_etal = not ((k in SINGLE_AUTHOR or k in (TWO_AUTHOR | THREE_AUTHOR)) and "et al" in plain)
    ok = ok_id and ok_title and ok_yr and ok_lead and ok_etal
    if not ok:
        fails.append(f"MISMATCH {k}: id={ok_id} title={ok_title} year={ok_yr} "
                     f"lead={ok_lead} etal={ok_etal}")
    print(f"  {k:17s} id={ok_id} title={ok_title} year={ok_yr} lead={ok_lead} "
          f"etal={ok_etal} -> {'VERIFIED' if ok else 'MISMATCH'}")
    if not ok:
        print("     TEX:", plain[:160])

# ---- direction 2: coverage is explicit, and nothing is silently uncovered -----------
checked, declared = set(official), set(OUT_OF_SCOPE)
present = set(found)
uncovered = present - checked - declared
orphan_records = (checked | declared) - present
orphan_records -= RETIRED          # R115: removed bibitems whose records stay for the history

print()
print(f"DECLARED OUT OF SCOPE ({len(declared & present)} of {len(found)}) -- not verified "
      f"against an arXiv record; basis named per entry:")
for k in sorted(declared & present):
    print(f"  {k:17s} {OUT_OF_SCOPE[k]}")

for k in sorted(uncovered):
    fails.append(f"UNCOVERED {k}: bibitem has neither a metadata record nor an "
                 f"OUT_OF_SCOPE declaration (v11 gate; v10 passed this silently)")
for k in sorted(orphan_records):
    fails.append(f"ORPHAN {k}: a record/declaration exists but no bibitem cites it")

print()
print("COVERAGE")
print(f"  bibitems                  : {len(found)}")
print(f"  checked (full metadata)   : {len(checked & present)}")
print(f"  declared out of scope     : {len(declared & present)}")
print(f"  silently uncovered        : {len(uncovered)}   <- must be 0")
print()
n_ok = len(checked & present) - sum(1 for f in fails if f.startswith("MISMATCH"))
if fails:
    print(f"FAILURES PRESENT ({len(fails)})")
    for f in fails:
        print("  ", f)
else:
    print(f"PASS -- {n_ok}/{len(checked & present)} full-metadata records VERIFIED; "
          f"{len(declared & present)} entries declared out of scope; "
          f"0 silently uncovered of {len(found)} bibitems.")
    print("NOTE: this is NOT a claim that all "
          f"{len(found)} bibitems were verified against an official record.")
sys.exit(1 if fails else 0)
