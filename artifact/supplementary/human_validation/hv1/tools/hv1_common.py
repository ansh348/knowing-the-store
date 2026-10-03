"""hv1_common.py -- program R119 (human validation, HV-A and HV-B): paths, the registration assertion, the pinned inputs,
the seeds, and the loaders every tool of the program shares.

Every tool calls assert_registration() and assert_inputs() first. Nothing here makes a model call.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
HV1 = ROOT / "human_validation" / "hv1"
KEY_DIR, INPUTS_DIR, WB_DIR, RES_DIR = HV1 / "key", HV1 / "inputs", HV1 / "workbooks", HV1 / "results"
REG = HV1 / "REGISTRATION_HV1.md"
LEDGER = HV1 / "NUMBERS_HV1.md"
DEVIATIONS = HV1 / "DEVIATIONS_HV1.md"
for p in ("ds_downstream/tools", "e0_metamemory/tools", "e1_metamemory/tools", "r82_counterfactual", "r82_counterfactual/tools",
          "e1r_robustness/tools"):
    sys.path.insert(0, str(ROOT / p))

PROGRAM = "R119"
REG_SHA = "34d6fa098661f1ee991639dc532e89731116f1bd688fcb4db362098c7b06e0d5"      # registered text, frozen at 4f10aa2
FREEZE_COMMIT = "4f10aa2"
FROZEN_END = b"<!-- REGISTERED TEXT ENDS ABOVE THIS LINE."

# seeds, as registered (section 2, 3.2, 6.2, 6.3, 6.4, 8)
SEED_CONTROLS, SEED_ORDER_A1, SEED_ORDER_A2 = 11901, 11902, 11903
SEED_TRIPLES, SEED_DISTRACTORS, SEED_WITHIN = 11904, 11905, 11906
SEED_HAIKU_A1, SEED_HAIKU_A2, SEED_PRACTICE = 11907, 11908, 11909
SEED_BOOT = 42
MIN_GAP = 10                     # rows between the two answers of one view
N_CONTROLS, N_PER_STATE, N_DISTRACTORS, MAX_SLOT_RECORDS = 50, 15, 6, 10
TAU_NEIGHBOUR = 0.503637         # registrations/ADDENDUM_RESP.md section C.2
SIX_POLICIES = ["ALWAYS", "MODEL", "LOOKUP", "MODEL-ALL", "LOOKUP-LIT", "ORACLE"]     # Table 4's rows, in its order
LABELS_A = ["ASSERTS", "MENTIONS", "CLEAN", "ABSTAINS", "UNSURE"]
LABELS_B = ["PRESENT", "PN", "ABSENT"]
ABSTAIN_TEXT = "does not currently contain"

# pinned inputs: path -> (sha256 of the working bytes, sha256 with CRLF normalised to LF); either is accepted, both are recorded
INPUTS = {
    "ds_downstream/run/rows_ds_amend4_mini.jsonl": ("9ddc9f2638b6a29759c0aa5f7c34b27a3a6a95bb7da56d5d97620dd92af58b24", "36e80b0fd6975c640d0eb3c1b57b5fe561266991923a42b728d619377c491b2c"),
    "ds_downstream/run/rows_ds_amend5_merged_mini.jsonl": ("b96ddcb2c52256e69ecbe0e87f0dd130075e2559408dbc289e3d35d86f8f65c9", "b96ddcb2c52256e69ecbe0e87f0dd130075e2559408dbc289e3d35d86f8f65c9"),
    "ds_downstream/run/rows_ds_amend4_h45.jsonl": ("2f26e9332c7594cdb92f19af303f157f2608a83a3ea12f664524976b63008ec8", "330abc63433dfb67a364eb3c0da74b779667fa35b4aedbea62f64afc9814fc5b"),
    "ds_downstream/run/rows_ds_amend5_merged_h45.jsonl": ("4d34ad8f53c51a1e2618ad87dcefb31593f86ce3ad43c95e723ab82985b68d37", "4d34ad8f53c51a1e2618ad87dcefb31593f86ce3ad43c95e723ab82985b68d37"),
    "ds_downstream/run/scores_amend4.json": ("a28a58595d8de7f47db93f91c30e8b73be1a1569c2a5d81645a7f12ce042b661", "a28a58595d8de7f47db93f91c30e8b73be1a1569c2a5d81645a7f12ce042b661"),
    "ds_downstream/run/scores_amend5.json": ("64cfb720d5a8dee158d216abfabdefd96eb6caa65bec7357a9f831b1225dd443", "64cfb720d5a8dee158d216abfabdefd96eb6caa65bec7357a9f831b1225dd443"),
    "ds_downstream/run/views_amend5.json": ("db120fef3cb452d13eb8bfc1e175b9dc580f42298b3196048199f560acc17d1d", "db120fef3cb452d13eb8bfc1e175b9dc580f42298b3196048199f560acc17d1d"),
    "r82_counterfactual/cf2/cf_cell.json": ("b0a42c1e0b996019130b42972a29e51f4fc0856854a019cb7f7d52cdb8874035", "b0a42c1e0b996019130b42972a29e51f4fc0856854a019cb7f7d52cdb8874035"),
    "r82_counterfactual/cf2/cf_pairs_cf2.json": ("460eb05f19b229f55979c289f896e2c7b400f85d01771a710a4da557c54d61f3", "460eb05f19b229f55979c289f896e2c7b400f85d01771a710a4da557c54d61f3"),
    "r82_counterfactual/cf2/cf_pn_texts_cf2.json": ("b605ec6b62ee26f7a44ae379045b23f5e57c933024eea433c6bbe8c2128f5e62", "b605ec6b62ee26f7a44ae379045b23f5e57c933024eea433c6bbe8c2128f5e62"),
    "r82_counterfactual/cf2/cf_questions_cf2.json": ("d81d59ab1e927bdf1fa7d3a82127f8c6c1395bbbfce1bb33ea5bb4d205232bde", "d81d59ab1e927bdf1fa7d3a82127f8c6c1395bbbfce1bb33ea5bb4d205232bde"),
    "r82_counterfactual/cf2/cf_indexes.json": ("09c897b8703dd5ff01e67a89a0f68ce14b5af3bbd3b8f0b48ed77fabb833d8e2", "09c897b8703dd5ff01e67a89a0f68ce14b5af3bbd3b8f0b48ed77fabb833d8e2"),
    "r82_counterfactual/cf_cell.json": ("496b66ca149b7816a522dd299ed23ebc4548e229553f9dd3814436405420a3c1", "496b66ca149b7816a522dd299ed23ebc4548e229553f9dd3814436405420a3c1"),
    "r82_counterfactual/cf_pairs.json": ("576a43c1e2fbbee8abcb34261467d56ed72f5eaf0afd31c0eb252ac8e6c57654", "576a43c1e2fbbee8abcb34261467d56ed72f5eaf0afd31c0eb252ac8e6c57654"),
    "r82_counterfactual/cf_pn_texts.json": ("e135d62d1918455accbfe289593f6d7e8be0adde0f5315fb44e5bce78196eb46", "e135d62d1918455accbfe289593f6d7e8be0adde0f5315fb44e5bce78196eb46"),
    "r82_counterfactual/cf_questions.json": ("c4c2f249be657403380099f6d4ca09e6504afad9889885f9cc41f478e40aa1c0", "c4c2f249be657403380099f6d4ca09e6504afad9889885f9cc41f478e40aa1c0"),
    "registrations/ADDENDUM_RESP.md": ("ad4a90ebfe36d9439fb7d3fec5297ec67b1419312b18376828bf0fca39357f30", "ad4a90ebfe36d9439fb7d3fec5297ec67b1419312b18376828bf0fca39357f30"),
    "registrations/ADDENDUM_DS_AMENDMENT_7.md": ("6fa6155ae965af154b4be9fba52ede4c5c664ffa5f22fb5574dfa1029408d487", "6fa6155ae965af154b4be9fba52ede4c5c664ffa5f22fb5574dfa1029408d487"),
}
BANKS_COMBINED = "319dd64a018cabf0539cb745fcc9b5cc8e7308d0a85e42cab4571d2dc3701481"     # 40 files; sha256 over sorted "name sha256" lines
BANKS = ROOT / "LifeMemEval" / "artifacts" / "lifecycle_banks"


# ------------------------------------------------------------------ hashing and assertions
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    return sha_bytes(pathlib.Path(p).read_bytes())


def sha_file_lf(p) -> str:
    return sha_bytes(pathlib.Path(p).read_bytes().replace(b"\r\n", b"\n"))


def sha_text(s: str) -> str:
    return sha_bytes(s.encode("utf-8"))


def banks_combined() -> str:
    files = sorted(BANKS.glob("*.json"))
    return sha_bytes("\n".join(f"{b.name} {sha_file(b)}" for b in files).encode("utf-8"))


def assert_registration():
    b = REG.read_bytes(); i = b.find(FROZEN_END)
    assert i > 0, "REGISTRATION_HV1.md has no marker line -- STOP"
    got = sha_bytes(b[:i])
    assert got == REG_SHA, f"REGISTRATION_HV1.md registered bytes sha256 {got[:16]} != {REG_SHA[:16]} -- STOP"
    return got


def assert_inputs():
    """Every pinned input matches by working bytes or by LF-normalised bytes; returns the digests found."""
    out = {}
    for rel, (raw, lf) in INPUTS.items():
        p = ROOT / rel
        assert p.exists(), f"pinned input missing: {rel} -- STOP"
        g_raw, g_lf = sha_file(p), sha_file_lf(p)
        assert g_raw in (raw, lf) or g_lf in (raw, lf), f"pinned input changed: {rel} {g_raw[:16]} -- STOP"
        out[rel] = {"sha256": g_raw, "sha256_lf": g_lf}
    got = banks_combined()
    assert got == BANKS_COMBINED, f"lifecycle banks changed: {got[:16]} -- STOP"
    out["LifeMemEval/artifacts/lifecycle_banks/*.json"] = {"sha256_combined": got, "files": len(list(BANKS.glob("*.json")))}
    return out


# ------------------------------------------------------------------ io
def J(p):
    return json.load(io.open(p, encoding="utf-8"))


def jdump(o, p):
    p = pathlib.Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")


def load_rows(rel):
    return [json.loads(l) for l in io.open(ROOT / rel, encoding="utf-8") if l.strip()]


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return [round(c - h, 4), round(c + h, 4)]


def append_ledger(title: str, body: str):
    """Append one dated section to NUMBERS_HV1.md (created with its header on first use)."""
    if not LEDGER.exists():
        LEDGER.write_text(f"# NUMBERS_HV1.md -- the R119 ledger (human validation, HV-A and HV-B)\n\n"
                          f"Every number this program prints resolves to a key here. Registration of record: "
                          f"`human_validation/hv1/REGISTRATION_HV1.md`, registered-text sha256 `{REG_SHA}`, frozen at `{FREEZE_COMMIT}`. "
                          f"Zero model calls.\n", encoding="utf-8", newline="\n")
    with io.open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n## {title}\n\n{body.rstrip()}\n")


def append_deviation(text: str):
    if not DEVIATIONS.exists():
        DEVIATIONS.write_text("# DEVIATIONS_HV1.md -- program R119\n\nEvery departure from `REGISTRATION_HV1.md`, dated, "
                              "written before the workbook is sent or, after sending, before scoring (registration section 10).\n",
                              encoding="utf-8", newline="\n")
    with io.open(DEVIATIONS, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"\n- **{now()}** {text.strip()}\n")


# ------------------------------------------------------------------ HV-A loaders
def load_hva_sources():
    """The four row files keyed by view key, the two score files, and the item records (stale / gold fields)."""
    import ds_common as DC
    import run_ds as RD
    rows = {("MINI", "before"): {r["key"]: r for r in load_rows("ds_downstream/run/rows_ds_amend4_mini.jsonl")},
            ("MINI", "after"): {r["key"]: r for r in load_rows("ds_downstream/run/rows_ds_amend5_merged_mini.jsonl")},
            ("H45", "before"): {r["key"]: r for r in load_rows("ds_downstream/run/rows_ds_amend4_h45.jsonl")},
            ("H45", "after"): {r["key"]: r for r in load_rows("ds_downstream/run/rows_ds_amend5_merged_h45.jsonl")}}
    scores = {"before": J(ROOT / "ds_downstream/run/scores_amend4.json")["per_row"],
              "after": J(ROOT / "ds_downstream/run/scores_amend5.json")["per_row"]}
    sub = DC.load_cell(); rec = RD.records(sub); byid = {it["item_id"]: it for it in sub}
    return rows, scores, rec, byid


def is_abstention(answer: str) -> bool:
    return ABSTAIN_TEXT in (answer or "")
