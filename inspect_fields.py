"""
inspect_fields.py
Purdue Women's Soccer – Local inspector for Dominant Foot / Primary Position

Shows, for every email, what was detected and the exact line it came from, so
you can check the extractor against real emails and find phrasings it misses.

Usage:
    python inspect_fields.py                              # every email under test_emails/
    python inspect_fields.py test_emails/2026-09-23       # one folder
    python inspect_fields.py test_emails/2026-09-23/4812.txt
    python inspect_fields.py --text "I'm a left-footed CB"
    python inspect_fields.py --misses                     # only emails with a blank field + hint lines
    python inspect_fields.py --field position --verbose   # every candidate and its score
    python inspect_fields.py --csv field_check.csv        # spreadsheet for review
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

from player_attributes import (
    explain_dominant_foot, explain_primary_position,
    extract_dominant_foot, extract_primary_position,
)
from testing_main import _read_file_as_text

FIELDS = {
    "foot":     ("Dominant Foot",    extract_dominant_foot,    explain_dominant_foot),
    "position": ("Primary Position", extract_primary_position, explain_primary_position),
}

# Loose keyword net used to suggest lines worth reading when nothing was detected
HINT_RES = {
    "foot":     re.compile(r"(?i)\bfoot|\bfeet\b|footed|\blefty\b|\brighty\b|\bdominant\b"),
    "position": re.compile(r"(?i)position|keeper|goalie|\bback\b|defen|\bmid|wing|striker|forward|attack|"
                           r"\b(?:GK|CB|LB|RB|CM|CDM|CAM|LM|RM|LW|RW|ST|CF)\b"),
}


def _collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            files.extend(sorted(f for ext in ("*.txt", "*.eml") for f in p.rglob(ext)))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"[error] Not found: {p.resolve()}")
    return files


def _fmt(c) -> str:
    line = c.line if len(c.line) <= 110 else c.line[:107] + "..."
    return f'L{c.line_no:<4} score {c.score:<4} {c.reason:<32} "{c.match}"  |  {line}'


def inspect(name: str, text: str, fields: list[str], verbose: bool, misses_only: bool) -> dict:
    row = {"file": name}
    report: list[str] = []
    any_missing = False

    for key in fields:
        col, extract, explain = FIELDS[key]
        value = extract(text)
        cands = explain(text)
        row[col] = value or ""
        row[f"{col} evidence"] = " || ".join(
            f"L{c.line_no} [{c.value} {c.score}] {c.line}" for c in cands if c.value == value)[:500]

        report.append(f"  {col:<17}: {value or '-- not found --'}")
        shown = cands if verbose else [c for c in cands if c.value == value][:2]
        for c in shown:
            tag = "" if c.value == value else f"   (candidate {c.value})"
            report.append(f"      {_fmt(c)}{tag}")

        if value is None:
            any_missing = True
            used = {c.line_no for c in cands}
            hints = [(i, ln.strip()) for i, ln in enumerate(text.splitlines(), 1)
                     if i not in used and HINT_RES[key].search(ln)]
            for i, ln in hints[:5]:
                report.append(f"      hint L{i:<4} {ln[:120]}")

    if not misses_only or any_missing:
        print(f"\n== {name}")
        print("\n".join(report))
    return row


def main():
    parser = argparse.ArgumentParser(description="Inspect Dominant Foot / Primary Position extraction.")
    parser.add_argument("paths", nargs="*", default=["test_emails"],
                        help="Email files or folders (searched recursively). Default: test_emails/")
    parser.add_argument("--text", help="Check a single snippet of text instead of files.")
    parser.add_argument("--field", choices=["foot", "position", "both"], default="both")
    parser.add_argument("--misses", action="store_true",
                        help="Only print emails where a field was not found, with hint lines to review.")
    parser.add_argument("--verbose", action="store_true", help="Print every candidate, not just the winner.")
    parser.add_argument("--csv", help="Also write one row per email (value + evidence) to this CSV.")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    fields = ["foot", "position"] if args.field == "both" else [args.field]

    if args.text is not None:
        inspect("--text", args.text.replace("\\n", "\n"), fields, verbose=True, misses_only=False)
        return

    files = _collect_files(args.paths)
    if not files:
        sys.exit(f"[error] No .txt/.eml files found in: {', '.join(args.paths)}")

    rows = [inspect(str(f), _read_file_as_text(f), fields, args.verbose, args.misses) for f in files]

    print(f"\n{'=' * 60}\nEmails inspected: {len(rows)}")
    for key in fields:
        col = FIELDS[key][0]
        counts = Counter(r[col] or "(blank)" for r in rows)
        found = len(rows) - counts.get("(blank)", 0)
        print(f"\n{col}: found in {found}/{len(rows)} ({found / len(rows):.0%})")
        for value, n in counts.most_common():
            print(f"    {value:<22} {n}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig opens cleanly in Excel
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"\nCSV -> {Path(args.csv).resolve()}")


if __name__ == "__main__":
    main()
