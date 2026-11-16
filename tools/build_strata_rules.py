#!/usr/bin/env python3
"""Pets and age rules by complex, South Surrey / White Rock and Langley (D-313).

Input: Pete's workbook "Condo and Townhouse Complex Rules - South Surrey and Langley" (Paragon Residential Attached listings,
active and sold, researched 2026-11-16). It is an MLS® export, so it stays out of this repository:
    python3 -I tools/build_strata_rules.py /path/to/complex-rules.xlsx /path/to/complex-rules-delta-chilliwack.xlsx   -> src/data/strata-rules.json

Only facts that rarely change are kept, so the tables do not need updating: year built, number of homes, pets (dogs, cats, how many), age.
Rentals are left out: since November 24, 2022 a BC strata cannot ban or cap long-term rentals, so the listing field is out of date (D-314).
Strata fees, prices and listing counts are left out. Each rule is what the listings in that complex say, not the bylaws:
  - every listing that states it agrees -> Yes / Yes, with limits / No / 55+ / No age limit (a blank field says nothing)
  - the listings disagree               -> Ask me
  - no listing states it            -> Not stated
"""
import json, re, sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
# Workbook tab -> (home type, region). The first workbook covers Langley and South Surrey / White Rock; the second (D-319)
# Tsawwassen, Ladner and Chilliwack. Tabs a workbook does not have are skipped.
TABS = {'South Surrey White Rock condos': ('Condo', 'ss'), 'South Surrey townhomes': ('Townhome', 'ss'), 'Langley condos': ('Condo', 'lan'), 'Langley townhomes': ('Townhome', 'lan'),
        'Tsawwassen condos': ('Condo', 'tsa'), 'Tsawwassen townhomes': ('Townhome', 'tsa'), 'Ladner condos': ('Condo', 'lad'), 'Ladner townhomes': ('Townhome', 'lad'),
        'Chilliwack condos': ('Condo', 'chw'), 'Chilliwack townhomes': ('Townhome', 'chw')}
SUB = {'Crescent Bch Ocean Pk.': 'Crescent Beach & Ocean Park', 'Aldergrove Langley': 'Aldergrove', 'Grandview Surrey': 'Grandview', 'Sunnyside Park Surrey': 'Sunnyside Park', 'Brookswood Langley': 'Brookswood'}
PETPAGES = {'south-surrey-white-rock-pet-friendly-condos-for-sale': ('ss', 'Condo'), 'south-surrey-white-rock-pet-friendly-townhomes-for-sale': ('ss', 'Townhome'),
            'langley-pet-friendly-condos-for-sale': ('lan', 'Condo'), 'langley-pet-friendly-townhomes-for-sale': ('lan', 'Townhome'),
            'chilliwack-pet-friendly-condos-for-sale': ('chw', 'Condo'), 'chilliwack-pet-friendly-townhomes-for-sale': ('chw', 'Townhome')}
TSA = ['Beach Grove', 'Boundary Beach', 'Cliff Drive', 'English Bluff', 'Pebble Hill', 'Tsawwassen Central', 'Tsawwassen East', 'Tsawwassen North']
LAD = ['Delta Manor', 'East Delta', 'Hawthorne', 'Holly', 'Ladner Elementary', 'Ladner Rural', 'Neilsen Grove', 'Port Guichon', 'Westham Island']
CHW = ['Chilliwack Downtown', 'Chilliwack Mountain', 'Chilliwack Proper East', 'Chilliwack Proper South', 'Chilliwack Proper West', 'Cultus Lake North', 'Eastern Hillsides',
       'Garrison Crossing', 'Little Mountain', 'Lower Landing', 'Promontory', 'Sardis East Vedder', 'Sardis South', 'Sardis West Vedder', 'Vedder Crossing', 'Vedder Mountain', 'Yarrow']
# Which pages show which complexes: MLS® sub-areas and home types.
PAGES = {
    'aldergrove-condos-for-sale': (['Aldergrove'], ['Condo']), 'aldergrove-townhomes-for-sale': (['Aldergrove'], ['Townhome']),
    'city-of-langley-condos-for-sale': (['Langley City'], ['Condo']), 'city-of-langley-townhomes-for-sale': (['Langley City'], ['Townhome']),
    'murrayville-condos-for-sale': (['Murrayville'], ['Condo']), 'murrayville-townhomes-for-sale': (['Murrayville'], ['Townhome']),
    'walnut-grove-condos-for-sale': (['Walnut Grove'], ['Condo']), 'walnut-grove-townhomes-for-sale': (['Walnut Grove'], ['Townhome']),
    'willoughby-condos-for-sale': (['Willoughby Heights'], ['Condo']), 'willoughby-townhomes-for-sale': (['Willoughby Heights'], ['Townhome']),
    'willoughby-heights-langley-condos-townhomes-for-sale': (['Willoughby Heights'], ['Condo', 'Townhome']),
    'white-rock-condos-for-sale': (['White Rock'], ['Condo']),
    'white-rock-townhomes-for-sale': (['White Rock'], ['Townhome']), 'crescent-beach-ocean-park-condos-townhomes-for-sale': (['Crescent Beach & Ocean Park'], ['Condo', 'Townhome']),
    'grandview-south-surrey-condos-townhomes-for-sale': (['Grandview'], ['Condo', 'Townhome']), 'grandview-surrey-townhomes-for-sale': (['Grandview'], ['Townhome']),
    'king-george-corridor-south-surrey-condos-townhomes-for-sale': (['King George Corridor'], ['Condo', 'Townhome']),
    'morgan-creek-south-surrey-condos-townhomes-for-sale': (['Morgan Creek'], ['Condo', 'Townhome']),
    'pacific-douglas-south-surrey-condos-townhomes-for-sale': (['Pacific Douglas'], ['Condo', 'Townhome']),
    'sunnyside-park-south-surrey-condos-townhomes-for-sale': (['Sunnyside Park'], ['Condo', 'Townhome']),
    'elgin-chantrell-south-surrey-condos-townhomes-for-sale': (['Elgin Chantrell'], ['Condo', 'Townhome']),
    'crescent-bch-ocean-pk': (['Crescent Beach & Ocean Park'], ['Condo', 'Townhome']),
    # 55+ pages: only the complexes whose listings all say 55+ (or 19+)
    'south-surrey-white-rock-55-plus-condos-for-sale': ('SSWR55', ['Condo']), 'south-surrey-white-rock-55-plus-townhomes-for-sale': ('SSWR55', ['Townhome']),
    'langley-55-plus-condos-for-sale': ('LAN55', ['Condo']), 'langley-55-plus-townhomes-for-sale': ('LAN55', ['Townhome']),
    'boundary-beach-tsawwassen-condos-townhomes-for-sale': (['Boundary Beach'], ['Condo', 'Townhome']),
    'chilliwack-downtown-condos-townhomes-for-sale': (['Chilliwack Downtown'], ['Condo', 'Townhome']),
    'chilliwack-mountain-condos-townhomes-for-sale': (['Chilliwack Mountain'], ['Condo', 'Townhome']),
    'chilliwack-proper-east-condos-townhomes-for-sale': (['Chilliwack Proper East'], ['Condo', 'Townhome']),
    'chilliwack-proper-south-condos-townhomes-for-sale': (['Chilliwack Proper South'], ['Condo', 'Townhome']),
    'chilliwack-proper-west-condos-townhomes-for-sale': (['Chilliwack Proper West'], ['Condo', 'Townhome']),
    'cliff-drive-tsawwassen-condos-townhomes-for-sale': (['Cliff Drive'], ['Condo', 'Townhome']),
    'delta-manor-ladner-condos-townhomes-for-sale': (['Delta Manor'], ['Condo', 'Townhome']),
    'hawthorne-ladner-condos-townhomes-for-sale': (['Hawthorne'], ['Condo', 'Townhome']),
    'ladner-elementary-condos-townhomes-for-sale': (['Ladner Elementary'], ['Condo', 'Townhome']),
    'neilsen-grove-ladner-condos-townhomes-for-sale': (['Neilsen Grove'], ['Condo', 'Townhome']),
    'tsawwassen-central-condos-townhomes-for-sale': (['Tsawwassen Central'], ['Condo', 'Townhome']),
    'tsawwassen-north-condos-townhomes-for-sale': (['Tsawwassen North'], ['Condo', 'Townhome']),
    'tsawwassen-condos-for-sale': (TSA, ['Condo']), 'tsawwassen-townhomes-for-sale': (TSA, ['Townhome']),
    'ladner-condos-for-sale': (LAD, ['Condo']), 'ladner-townhomes-for-sale': (LAD, ['Townhome']),
    'chilliwack-condos-for-sale': (CHW, ['Condo']), 'chilliwack-townhomes-for-sale': (CHW, ['Townhome']),
    'sardis-condos-for-sale': (['Sardis West Vedder', 'Sardis East Vedder', 'Sardis South'], ['Condo']), 'sardis-townhomes-for-sale': (['Sardis West Vedder', 'Sardis East Vedder', 'Sardis South'], ['Townhome']),
    'chilliwack-55-plus-condos-for-sale': ('CHW55', ['Condo']), 'chilliwack-55-plus-townhomes-for-sale': ('CHW55', ['Townhome']),
}
AGE55 = {'SSWR55': ('ss',), 'LAN55': ('lan',), 'CHW55': ('chw',)}
LANGLEY = {'Aldergrove', 'Langley City', 'Murrayville', 'Walnut Grove', 'Willoughby Heights', 'Fort Langley', 'Salmon River', 'Brookswood', 'Brookswood Langley'}


def parts(s):
    """'Pets allowed with restrictions on 3 of 3; # of Pets field: 2: 2' -> [('Pets allowed with restrictions', 3, 3)]"""
    return [(m.group(1).strip(), int(m.group(2)), int(m.group(3))) for m in re.finditer(r'([A-Za-z][A-Za-z ()+\d-]*?) on (\d+) of (\d+)', str(s))]


def rule(s, table):
    ps = [(table(lab), a, b) for lab, a, b in parts(s)]
    ps = [p for p in ps if p[0]]
    if not ps:
        return 'Not stated'
    vals = {p[0] for p in ps}
    if vals == {'Yes', 'Yes, with limits'}:
        return 'Yes, with limits'   # some listings mention the limits, some do not: both allow it
    if len(vals) > 1:
        return 'Ask me'
    return ps[0][0]          # every listing that states it agrees (listings that leave the field blank say nothing either way)


def pets(lab):
    l = lab.lower()
    if 'not allowed' in l: return 'No'
    if 'with restriction' in l: return 'Yes, with limits'
    if 'allowed' in l or 'no restrictions' in l: return 'Yes'
    return ''


def dogs_cats(s):
    """'# of Pets field: (blank): 2; 2: 1; Dogs Yes 2 / No 0; Cats Yes 2 / No 0' -> dogs Yes, cats Yes, number 2 (only when every
    listing that fills the field gives the same number)."""
    s = str(s); out = {}
    for k in ('Dogs', 'Cats'):
        m = re.search(k + r' Yes (\d+) / No (\d+)', s)
        y, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        out[k.lower()] = 'Yes' if y and not n else 'No' if n and not y else 'Ask me' if y and n else ''
    m = re.search(r'# of Pets field: ([^;]*(?:; (?:\(blank\)|\d+): \d+)*)', s)
    nums = set(re.findall(r'(?:^|; )(\d+): \d+', m.group(1))) if m else set()
    out['npets'] = nums.pop() if len(nums) == 1 else ''
    return out


def age(s):
    s = str(s)
    if s.startswith('No age restriction tagged'): return 'No age limit'
    # "Restricted Age 55+ on 3 of 3; blank on 1 of 4; Bylaw Restrictions field includes Age Restrictions on 3 of 4": the age tags only
    ps = [(re.search(r'(\d+)\+', lab).group(1) + '+' if re.search(r'\d+\+', lab) else 'other', a, b) for lab, a, b in parts(s)
          if re.search(r'\d+\+', lab) or lab.strip().lower() == 'other']
    if not ps: return 'Not stated'
    if len({p[0] for p in ps}) > 1 or ps[0][0] == 'other': return 'Ask me'
    return ps[0][0]


def main(srcs):
    rows = []
    for tab, (kind, region) in TABS.items():
        wb = next((w for w in (openpyxl.load_workbook(p, read_only=True, data_only=True) for p in srcs) if tab in w.sheetnames), None)
        if wb is None: continue
        r = [x for x in wb[tab].iter_rows(values_only=True) if any(c is not None for c in x)]
        H = r[1]
        for x in r[2:]:
            if not x[0]: continue
            d = dict(zip(H, x))
            t = str(d['Type'])
            if t not in ('Condo', 'Townhouse'): continue          # half duplexes and non-strata row houses have no strata rules
            sub = re.sub(r'\s*\(\d+\).*$', '', str(d['Sub-area']))  # "Willoughby Heights (7); Langley City (1)" -> the main one
            sub = SUB.get(sub, sub)
            built = (re.match(r'^(\d{4})', str(d['Year built'])) or [None, ''])[1]
            homes = (re.match(r'^(\d+) \(stated on', str(d['Total units in strata plan (as stated in listings)'])) or [None, ''])[1]
            rows.append({'name': str(d['Complex / building name']).strip(), 'sub': sub, 'type': kind, 'region': region, 'addr': str(d['Street address (no unit #)'] or '').strip(),
                         'built': built, 'homes': homes,
                         'pets': rule(d['Pets (per MLS listings, not the strata bylaws)'], pets),
                         **dogs_cats(d['Pets (per MLS listings, not the strata bylaws)']),
                         'age': age(d['Age restriction (per MLS listings, not the strata bylaws)'])})
    # Names as listings spell them: "NEWPORT at WEST BEACH" -> "Newport at West Beach", "Luxia AT Yorkson" -> "Luxia at Yorkson".
    def tidy(n):
        n = re.sub(r'\bAT\b', 'at', n)
        return ' '.join(w.title() if w.isupper() and len(w) > 3 and not re.search(r'\d', w) else w for w in n.split(' '))
    FIX = {'Cambrige': 'Cambridge'}   # listing typos
    for r in rows: r['name'] = FIX.get(tidy(r['name']), tidy(r['name']))
    # One row per complex: the same first street address and type under several names ("Altus", "Altus White Rock",
    # "Unnamed complex at 1526 Finlay Street") keeps the plain name. Different buildings sharing an address keep their own rows.
    groups = {}
    for r in rows: groups.setdefault((r['addr'].split(';')[0].strip().lower(), r['type'], r['region']), []).append(r)
    keep = []
    for (addr, _, _), g in groups.items():
        if not addr: keep += g; continue
        named = [r for r in g if not r['name'].startswith('Unnamed complex')] or g[:1]
        names = [r['name'].lower() for r in named]
        keep += [r for r in named if not any(r['name'].lower().startswith(o + ' ') for o in names if o != r['name'].lower())]
    # Same complex spelled two ways ("Dawson's Creek" / "Dawsons Creek", "Chelsea - The Boroughs" / "Chelsea @ The Boroughs"):
    # one row, addresses joined, and a disagreement on a rule becomes "Ask me" (Yes + Yes, with limits stays "Yes, with limits").
    def both(a, b):
        if a == b: return a
        if {a, b} == {'Yes', 'Yes, with limits'}: return 'Yes, with limits'
        if 'Not stated' in (a, b): return b if a == 'Not stated' else a
        return 'Ask me'
    seen = {}
    rows = []
    for r in keep:
        k = (re.sub(r'[^a-z0-9]', '', r['name'].lower()), r['type'], r['sub'])
        if k not in seen: seen[k] = r; rows.append(r); continue
        o = seen[k]
        for f in ('pets', 'age'): o[f] = both(o[f], r[f])
        for f in ('dogs', 'cats'): o[f] = o[f] if o[f] == r[f] or not r[f] else r[f] if not o[f] else 'Ask me'
        o['npets'] = o['npets'] if o['npets'] == r['npets'] or not r['npets'] else r['npets'] if not o['npets'] else ''
        if r['addr'] and r['addr'] not in o['addr']: o['addr'] = (o['addr'] + '; ' + r['addr']).strip('; ')
        for f in ('built', 'homes'): o[f] = o[f] or r[f]
    rows.sort(key=lambda r: r['name'].lower())
    pages = {}
    for slug, (subs, types) in PAGES.items():
        if isinstance(subs, str) and subs in AGE55:
            pick = [i for i, r in enumerate(rows) if r['type'] in types and r['age'] == '55+' and r['region'] in AGE55[subs]]
        else:
            pick = [i for i, r in enumerate(rows) if r['sub'] in subs and r['type'] in types]
        if pick: pages[slug] = {'rows': pick, 'mixed': len(types) > 1}
    # Pet-friendly pages (D-314): every condo or townhouse complex in the region, by type.
    petpages = {}
    for slug, (reg, typ) in PETPAGES.items():
        petpages[slug] = [i for i, r in enumerate(rows) if r['type'] == typ and r['region'] == reg]
    # Building pages (src/data/local/*-condos.json with a "<name> building facts" table): matched by name, else by street address.
    buildings = {}
    for f in sorted((ROOT / 'src/data/local').glob('*-condos.json')):
        d = json.loads(f.read_text())
        t = next((b for b in d.get('blocks', []) if b.get('t') == 'table' and str(b.get('caption', '')).endswith('building facts')), None)
        if not d.get('new_page') or not t: continue
        nm = t['head'][1].lower(); addr = next((r[1] for r in t['rows'] if str(r[0]).lower().startswith('address')), '').split(',')[0].lower()
        i = next((i for i, r in enumerate(rows) if r['name'].lower() == nm), None)
        if i is None and addr: i = next((i for i, r in enumerate(rows) if addr in r['addr'].lower()), None)
        if i is not None: buildings[f.stem] = i
    out = {'_note': 'Pets and age rules by complex, from the MLS® listings in each complex (Paragon, active and sold, checked November 2026), not the strata bylaws. Built by tools/build_strata_rules.py (D-313).',
           'checked': 'November 2026', 'rows': rows, 'pages': pages, 'buildings': buildings, 'petpages': petpages}
    (ROOT / 'src/data/strata-rules.json').write_text(json.dumps(out, ensure_ascii=False, indent=0) + '\n')
    print(len(rows), 'complexes;', {k: len(v['rows']) for k, v in pages.items()})


if __name__ == '__main__':
    main(sys.argv[1:])
