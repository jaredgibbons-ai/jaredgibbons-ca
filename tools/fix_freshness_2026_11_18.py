#!/usr/bin/env python3
"""Freshness fixes of 2026-11-18 (follow-up to the 2026-11-16 check; Jared: "keep going").

Edits the raw file text, so each JSON file keeps its own format. Safe to rerun: a replacement is skipped when its old
text is gone. Sources were opened on 2026-11-18.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L = 'src/data/local/'

# Township of Langley, "2026 PROPERTY TAX RATES per $1000 of Assessed Value":
#   Class 01 Residential "TOTAL 2026 TAX RATE 3.61686"; "TOTAL MUNICIPAL PURPOSE Bylaw 6213 2.00540"
TOL_25_URL = 'https://www.tol.ca/en/services/resources/property-taxes/document-feed/2025-Tax-Rates.pdf'
TOL_26_URL = 'https://www.tol.ca/en/services/resources/property-taxes/document-feed/2026-Tax-Rates.pdf'

FIXES = [
    (L + 'langley-farms-for-sale-acreages-agricultural-land-mls.json',
     'The 2025 total tax rate a Langley buyer can verify is 3.34910 per $1,000 for Class 1 Residential, with the municipal portion at 1.87580, per the Township 2025 tax rates sheet.',
     'The 2026 total tax rate a Langley buyer can verify is 3.61686 per $1,000 for Class 1 Residential, with the municipal portion at 2.00540, per the Township 2026 tax rates sheet.'),
    (L + 'langley-farms.json',
     "The Township's total 2025 tax rate for Class 1 Residential was 3.34910 per $1,000 of assessed value, of which the total municipal rate was 1.87580, per the Township 2025 tax rates sheet.",
     "The Township's total 2026 tax rate for Class 1 Residential is 3.61686 per $1,000 of assessed value, of which the total municipal rate is 2.00540, per the Township 2026 tax rates sheet."),
    (L + 'salmon-river.json',
     "The Township of Langley's total 2025 residential tax rate was 3.34910 per $1,000 of assessed value, of which the total municipal rate under Bylaw 6128 was 1.87580 per $1,000 — the Township's own 2025 Property Tax Rates table.",
     "The Township of Langley's total 2026 residential tax rate is 3.61686 per $1,000 of assessed value, of which the total municipal rate under Bylaw 6213 is 2.00540 per $1,000 — the Township's own 2026 Property Tax Rates table."),
    # salmon-river's comparison table is headed "Fact (2025)"; its tax row is marked 2026 now that it shows 2026.
    (L + 'salmon-river.json', '"3.34910"', '"3.61686 (2026)"'),
    (L + 'cloverdale-farms.json', '"1.87580 municipal portion (2025)"', '"2.00540 municipal portion (2026)"'),
    (L + 'campbell-valley-houses-for-sale.json', '"Total 2025 residential tax rate"', '"Total 2026 residential tax rate"'),
    (L + 'campbell-valley-houses-for-sale.json', '"3.34910 per $1,000"', '"3.61686 per $1,000"'),

    # Moved link: Surrey Schools now serves Cedar Hills Elementary at /cedarhill (old /schools/cedarhill shows an empty
    # directory). Checked 2026-11-18.
    (L + 'cedar-hills-surrey-houses-for-sale.json', 'https://www.surreyschools.ca/schools/cedarhill', 'https://www.surreyschools.ca/cedarhill'),
    (L + 'north-delta-townhomes-for-sale.json', 'https://www.surreyschools.ca/schools/cedarhill', 'https://www.surreyschools.ca/cedarhill'),
    # Wrong page: the "Maple Ridge Secondary School" link opened a 2019 annex news post. The school's own site is
    # https://secondary.sd42.ca/mrss/ ("MRSS – Maple Ridge Secondary School"), linked from sd42.ca's secondary schools list.
    ('src/data/posts/sold-renovated-3-bed-townhome-in-maple-ridge-8673946.json', 'https://www.sd42.ca/school/mrss/', 'https://secondary.sd42.ca/mrss/'),
]

# source links swapped everywhere in these files
SWAPS = [(L + f, [(TOL_25_URL, TOL_26_URL), ('tol.ca · 2025 Tax Rates', 'tol.ca · 2026 Tax Rates')])
         for f in ('campbell-valley-houses-for-sale.json', 'cloverdale-farms.json', 'langley-farms.json',
                   'langley-farms-for-sale-acreages-agricultural-land-mls.json', 'salmon-river.json')]


def main():
    edits = {}
    for rel, old, new in FIXES:
        edits.setdefault(rel, []).append((old, new))
    for rel, pairs in SWAPS:
        edits.setdefault(rel, []).extend(pairs)
    changed = 0
    for rel, pairs in edits.items():
        path = ROOT / rel
        text = orig = path.read_text(encoding='utf-8')
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
            elif new not in text:
                print(f'WARNING: not found in {rel}: {old[:70]}')
        if text != orig:
            json.loads(text)
            path.write_text(text, encoding='utf-8')
            changed += 1
            print(f'fixed: {rel}')
    print(f'{changed} file(s) changed')


if __name__ == '__main__':
    main()
