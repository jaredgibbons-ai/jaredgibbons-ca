#!/usr/bin/env python3
"""Freshness fixes of 2026-11-16 (weekly freshness check).

Edits the raw file text, so each JSON file keeps its own format. Safe to rerun:
a replacement is skipped when the old text is gone.

1. Foreign buyers / farmland post: the BC election wording said a government
   "is forming". The final count is complete.
   Source: Elections BC results, GE 2026-10-24, party summary
   https://results.elections.bc.ca/Results_11684_GE-2026-10-24_Party.html
   (final count complete as of November 9, 2026: BC Conservatives 64 of 93 seats).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FIXES = [
    (
        "src/data/posts/can-foreigners-buy-farmland-in-bc-fraser-valley-rules-9186434.json",
        "BC held a provincial election on October 24, 2026, and a Conservative majority government is forming.",
        "BC held a provincial election on October 24, 2026. The final count, completed November 9, gave the BC Conservatives 64 of 93 seats.",
    ),
]


def main():
    changed = 0
    for rel, old, new in FIXES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if old not in text:
            print(f"skip (already fixed or gone): {rel}")
            continue
        text = text.replace(old, new)
        json.loads(text)  # still valid JSON
        path.write_text(text, encoding="utf-8")
        changed += 1
        print(f"fixed: {rel}")
    print(f"{changed} file(s) changed")


if __name__ == "__main__":
    main()
