"""D-387 (part 3): beds, baths, floor area and lot size on the sold and purchased listing pages that had none.
110 of the 190 sold/purchased pages showed only a status, an MLS® number and a year. These pages rank for address searches, and a
page with the home's basic facts answers that search. The facts come from Pete's Paragon exports of Jared's own deals (listing side
and buyer side, Nov 15-16 2026), matched by MLS® number and checked against the page's street number. No prices (D-318).
The exports are client records and stay outside the repo (/home/claude/private-sales); only the public MLS® facts land on the pages.
Run once from the repo root: python3 tools/sold_listing_facts_2026_11_20.py <paragon.json> <paragon-buyer-commercial.xlsx>
"""
import glob, json, re, sys
import openpyxl

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    raise SystemExit(f'format not matched: {p}')
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

P = {r['MLS #']: r for r in json.load(open(sys.argv[1]))}
wb = openpyxl.load_workbook(sys.argv[2], read_only=True)
for name in ('Listing side (residential)', 'Buyer side (residential)'):
    rows = list(wb[name].iter_rows(values_only=True)); h = rows[0]
    for r in rows[1:]:
        rec = {h[i]: ('' if v is None else str(v)) for i, v in enumerate(r)}
        P.setdefault(rec['MLS #'], rec)

def num(x):
    try: return float(str(x).replace(',', ''))
    except ValueError: return 0
done = skipped = 0
for f in sorted(glob.glob('src/data/listings/*.json')):
    d = load(f)
    if d.get('status') != 'Sold': continue
    facts = [b for b in d['blocks'] if b['t'] == 'facts']
    have = {it['k'].rstrip(':') for b in facts for it in b['items']}
    if 'Bedrooms' in have: continue
    mls = next((it['v'][0] for b in facts for it in b['items'] if it['k'].startswith('MLS')), None)
    r = P.get(mls)
    if not r: continue
    # the page's street number must appear in the export's address
    h1 = next(b['text'] for b in d['blocks'] if b['t'] == 'h' and b.get('level') == 1)
    nums = re.findall(r'\d+', h1.split(' ', 2)[0] + ' ' + h1.split(' ', 2)[1] if len(h1.split()) > 1 else h1)[:2]
    if not all(n in re.findall(r'\d+', r['Address']) for n in nums): skipped += 1; print('address mismatch, skipped:', mls, h1, '|', r['Address']); continue
    beds, baths, area = int(num(r['Beds'])), num(r['Baths']), int(num(r['Floor Area (sq ft)']))
    lot_sf, lot_ac = num(r['Lot Size (sq ft)']), num(r['Lot Size (acres)'])
    strata = re.search(r'apartment|condo|townhouse', r['Type of Dwelling'], re.I)
    add = []
    if r['Type of Dwelling'] and 'Dwelling Type' not in have: add.append({'k': 'Dwelling Type:', 'v': [r['Type of Dwelling']]})
    if beds: add.append({'k': 'Bedrooms:', 'v': [str(beds)]})
    if baths: add.append({'k': 'Bathrooms:', 'v': [str(int(baths)) if baths == int(baths) else str(baths)]})
    if area: add.append({'k': 'Floor Area:', 'v': [f'{area:,} sq. ft.']})
    if not strata and (lot_ac >= 1 or lot_sf > 0):
        add.append({'k': 'Lot Size:', 'v': [f'{lot_ac:g} acres' if lot_ac >= 1 else f'{int(lot_sf):,} sq. ft.']})
    if r['Year Built'] and 'Year Built' not in have: add.append({'k': 'Year Built:', 'v': [r['Year Built']]})
    if not add: continue
    first = facts[0]['items']
    at = next((i + 1 for i, it in enumerate(first) if it['k'].startswith('Prop')), len(first))
    first[at:at] = add
    # the summary line under the address: beds, baths and area before "built:"
    s = next((b for b in d['blocks'] if b['t'] == 'summary'), None)
    if s:
        ins = (['beds:', str(beds)] if beds else []) + (['baths:', f'{baths:.1f}'] if baths else []) + ([f'{area:,} sq. ft.'] if area else [])
        lines = s['lines']; hn = s.get('heading_n') or len(lines)
        pos = next((i for i, l in enumerate(lines[:hn]) if l == 'built:'), hn)
        s['lines'] = lines[:pos] + ins + lines[pos:]
        if s.get('heading_n'): s['heading_n'] = hn + len(ins)
    d['facts_source'] = 'Paragon export of Jared\'s deals (D-387)'
    save(f, d); done += 1
print('pages given facts:', done, '| skipped on address check:', skipped)
