#!/usr/bin/env python3
"""Mobile home park type and 55+ (D-315), from Pete's "Mobile home park rules" workbook (Paragon sales and active listings,
park websites and municipal records, checked 2026-11-16). The workbook stays out of this repository:
    python3 -I tools/build_park_rules.py /path/to/mh-rules.xlsx   -> src/data/park-rules.json

Kept: how you own the home's spot (pad rental, co-op shares, strata lot, own the land) and 55+ only where every MLS® listing that
fills the age field says 55+ (at least two), or the park's own documents say so. Pad rents, buy-in fees and pet rules are left out:
most are unconfirmed listing marketing and they change.
"""
import json, re, sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent


def kind(own):
    o = str(own).lower()
    if o.startswith('mixed'): return ''
    if o.startswith('leasehold pad rental'): return 'Pad rental'
    if o.startswith('co-op'): return 'Co-op shares'
    if 'freehold strata' in o or 'bare land strata' in o: return 'Strata lot'
    if 'freehold nonstrata' in o: return 'Own the land'
    return ''


def senior(age, active):
    a, act = str(age), str(active)
    if re.search(r'Official rule[^.]*55', a): return '55+'
    tagged = total = 0
    m = re.search(r'55\+ on (?:all )?(\d+|both|the 1)(?: of (\d+))? (?:matched )?sales?', a)
    if m:
        n = {'both': 2, 'the 1': 1}.get(m.group(1)) or int(m.group(1))
        tagged += n; total += int(m.group(2)) if m.group(2) else n
    m = re.search(r'(\d+) of (\d+) tagged 55\+', act)
    if m: tagged += int(m.group(1)); total += int(m.group(2))
    return '55+' if total >= 2 and tagged == total else ''


def keys(addr):
    """'26892 Fraser Highway' -> ['26892 fraser']; '9080 / 9098 198 Street' -> ['9080 198', '9098 198']."""
    m = re.match(r'\s*(\d+(?:\s*/\s*\d+)*)\s+(\w+)', str(addr))
    return [f'{n} {m.group(2).lower()}' for n in re.findall(r'\d+', m.group(1))] if m else []


def main(src):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    rows = [r for r in wb['All parks'].iter_rows(values_only=True) if any(c is not None for c in r)]
    H = rows[0]
    parks = {}
    for r in rows[2:]:
        d = dict(zip(H, r))
        if not d['Park name'] or 'not a named park' in str(d['Park name']) or 'not a park' in str(d['Park name']): continue
        ks = keys(d['Park address (no unit #)'])
        rec = {'name': str(d['Park name']).strip(), 'type': kind(d['Ownership type']),
                    'age': senior(d['Age restriction'], d['Active Restricted Age 55+ (n) and other age tags'])}
        for k in ks: parks[k] = rec
    out = {'_note': 'Mobile home park type and 55+ (where every listing agrees), keyed by civic number and street. Built by tools/build_park_rules.py (D-315).',
           'checked': 'November 2026', 'parks': parks}
    (ROOT / 'src/data/park-rules.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(len(parks), 'parks;', sum(1 for p in parks.values() if p['age']), '55+;', {t: sum(1 for p in parks.values() if p['type'] == t) for t in {p['type'] for p in parks.values()}})


if __name__ == '__main__':
    main(sys.argv[1])
