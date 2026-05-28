"""
audit_integrity.py
==================

Standing integrity checks for the manuscript and dataset. Run this
script after any iteration that edits main.tex, supplementary.tex,
references.bib, or corpus_d1d7.csv. Exits 0 on clean, 1 on any
mismatch.

Checks performed:

  1. Bib hygiene
     - Every \cite key in main.tex and supplementary.tex resolves in
       references.bib (no broken citations).
     - Every entry in references.bib is cited somewhere (no orphans).
     - No duplicate bib keys.

  2. Corpus dataset integrity
     - corpus_d1d7.csv has exactly 152 rows with IDs 1-152.
     - The "Comprehensive Per-Paper Mapping" appendix in
       supplementary.tex lists the same 152 IDs.
     - Per-row D1-D7 codings in the supplement match the CSV exactly.

  3. Cross-reference integrity
     - Every "Appendix~X" reference in main.tex resolves to a defined
       \section{...}\label{app:...} in supplementary.tex (after
       accounting for ordering: 1st section -> A, 2nd -> B, ...).

Reports counts and exits non-zero on any defect.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MAIN = (ROOT / "main.tex").read_text(encoding="utf-8")
SUP = (ROOT / "supplementary.tex").read_text(encoding="utf-8")
BIB = (ROOT / "references.bib").read_text(encoding="utf-8")

failures: list[str] = []


def section(name: str) -> None:
    print()
    print(f"=== {name} ===")


# --- 1. Bib hygiene --------------------------------------------------
section("1. Bib hygiene")

bib_keys = re.findall(r"@\w+\{([^,]+),", BIB)
bib_set = set(bib_keys)
print(f"references.bib entries: {len(bib_keys)}")

cite_pattern = re.compile(r"\\cite[a-z]*\{([^}]+)\}")
cite_main: set[str] = set()
cite_sup: set[str] = set()
for m in cite_pattern.finditer(MAIN):
    for k in m.group(1).split(","):
        cite_main.add(k.strip())
for m in cite_pattern.finditer(SUP):
    for k in m.group(1).split(","):
        cite_sup.add(k.strip())
all_cited = cite_main | cite_sup
print(f"Cited in main: {len(cite_main)}")
print(f"Cited in supplement: {len(cite_sup)}")
print(f"Union: {len(all_cited)}")

orphans = bib_set - all_cited
broken = all_cited - bib_set
counts: dict[str, int] = {}
for k in bib_keys:
    counts[k] = counts.get(k, 0) + 1
dups = {k: v for k, v in counts.items() if v > 1}

if orphans:
    failures.append(f"{len(orphans)} orphan bib entries")
    for k in sorted(orphans):
        print(f"  ORPHAN: {k}")
if broken:
    failures.append(f"{len(broken)} broken citations")
    for k in sorted(broken):
        print(f"  BROKEN: {k}")
if dups:
    failures.append(f"{len(dups)} duplicate bib keys")
    for k, v in dups.items():
        print(f"  DUP: {k} ({v} times)")
if not (orphans or broken or dups):
    print("clean: 0 orphans, 0 broken, 0 duplicates")


# --- 2. Corpus dataset integrity -------------------------------------
section("2. Corpus dataset integrity")

with open(ROOT / "corpus_d1d7.csv", encoding="utf-8") as f:
    csv_rows = {int(r["ID"]): r for r in csv.DictReader(f)}

print(f"corpus_d1d7.csv rows: {len(csv_rows)}")
if len(csv_rows) != 152:
    failures.append(f"corpus_d1d7.csv has {len(csv_rows)} rows, expected 152")
csv_ids = set(csv_rows.keys())
if csv_ids != set(range(1, 153)):
    missing = sorted(set(range(1, 153)) - csv_ids)
    extra = sorted(csv_ids - set(range(1, 153)))
    failures.append(f"corpus IDs: missing {missing}, extra {extra}")


def split_amp(s: str) -> list[str]:
    sentinel = "\x00AMP\x00"
    s = s.replace(r"\&", sentinel)
    return [p.replace(sentinel, r"\&").strip() for p in s.split("&")]


sup_rows: dict[int, dict[str, str]] = {}
for line in SUP.splitlines():
    s = line.strip()
    s = re.sub(r"^\\rowcolor\{[^}]*\}\s*", "", s)
    m = re.match(r"^(\d{1,3})\s*&\s*(.*?)\\\\\s*$", s)
    if not m:
        continue
    rid = int(m.group(1))
    if rid < 1 or rid > 152:
        continue
    fields = split_amp(m.group(2))
    if len(fields) < 9:
        continue
    paper, system, d1, d2, d3, d4, d5, d6, d7 = fields[:9]
    sup_rows[rid] = {
        "D1": d1, "D2": d2, "D3": d3, "D4": d4,
        "D5": d5, "D6": d6, "D7": d7,
    }

print(f"supplement Appendix C rows: {len(sup_rows)}")
if len(sup_rows) != 152:
    failures.append(f"supplement Appendix C has {len(sup_rows)} rows, expected 152")

mism = 0
for rid in csv_rows:
    if rid not in sup_rows:
        mism += 1
        print(f"  MISSING in supplement: ID {rid}")
        continue
    for dim in ("D1", "D2", "D3", "D4", "D5", "D6", "D7"):
        if csv_rows[rid][dim].strip() != sup_rows[rid][dim].strip():
            mism += 1
            print(
                f"  ID {rid} {dim}: CSV={csv_rows[rid][dim]!r}"
                f" vs SUP={sup_rows[rid][dim]!r}"
            )
if mism:
    failures.append(f"{mism} per-row D1-D7 mismatches between supplement and CSV")
else:
    print("clean: 152 IDs match; all 152 x 7 codings agree")


# --- 3. Cross-reference integrity ------------------------------------
section("3. Appendix cross-references")

sup_apps = re.findall(
    r"\\section\{([^}]+)\}\s*\\label\{(app:[^}]+)\}",
    SUP,
)
print(f"supplement defines {len(sup_apps)} appendices")
available_letters = {chr(ord("A") + i) for i in range(len(sup_apps))}
for i, (title, _) in enumerate(sup_apps):
    print(f"  {chr(ord('A') + i)} = {title}")

ref_pattern = re.compile(r"Appendix~?([A-Z])\b")
bad_refs = []
for m in ref_pattern.finditer(MAIN):
    if m.group(1) not in available_letters:
        line_no = MAIN[: m.start()].count("\n") + 1
        bad_refs.append((line_no, m.group(1)))
if bad_refs:
    failures.append(f"{len(bad_refs)} appendix references with no target")
    for line_no, letter in bad_refs:
        print(f"  L{line_no}: Appendix~{letter} -> no such appendix")
else:
    print("clean: all Appendix~X references resolve")


# --- summary ---------------------------------------------------------
section("SUMMARY")
if failures:
    print(f"FAILED with {len(failures)} defect group(s):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("PASS: all integrity checks clean")
    sys.exit(0)
