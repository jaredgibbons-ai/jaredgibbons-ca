#!/usr/bin/env python3
"""Pets, rentals and age rules by complex, South Surrey / White Rock and Langley (D-313).

Input: Pete's workbook "Condo and Townhouse Complex Rules - South Surrey and Langley" (Paragon Residential Attached listings,
active and sold, researched 2026-11-16). It is an MLS® export, so it stays out of this repository:
    python3 -I tools/build_strata_rules.py /path/to/complex-rules.xlsx   -> src/data/strata-rules.json

Only facts that rarely change are kept, so the tables do not need updating: year built, number of homes, pets, rentals, age.
Strata fees, prices and listing counts are left out. Each rule is what the listings in that complex say, not the bylaws:
  - every listing that states it agrees -> Yes / Yes, with limits / No / 55+ / 19+ / No age limit (a blank field says nothing)
  - the listings disagree               -> Ask me
  - no listing states it            -> Not stated
"""
import json, re, sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
TABS = {'South Surrey White Rock condos': 'Condo', 'South Surrey townhomes': 'Townhome', 'Langley condos': 'Condo', 'Langley townhomes': 'Townhome'}
SUB = {'Crescent Bch Ocean Pk.': 'Crescent Beach & Ocean Park', 'Aldergrove Langley': 'Aldergrove', 'Grandview Surrey': 'Grandview', 'Sunnyside Park Surrey': 'Sunnyside Park'}
# Which pages show which complexes: MLS® sub-areas and home types.
PAGES = {
    'aldergrove-condos-for-sale': (['Aldergrove'], ['Condo']), 'aldergrove-townhomes-for-sale': (['Aldergrove'], ['Townhome']),
    'city-of-langley-condos-for-sale': (['Langley City'], ['Condo']), 'city-of-langley-townhomes-for-sale': (['Langley City'], ['Townhome']),
    'murrayville-condos-for-sale': (['Murrayville'], ['Condo']), 'murrayville-townhomes-for-sale': (['Murrayville'], ['Townhome']),
    'walnut-grove-condos-for-sale': (['Walnut Grove'], ['Condo']), 'walnut-grove-townhomes-for-sale': (['Walnut Grove'], ['Townhome']),
    'willoughby-condos-for-sale': (['Willoughby Heights'], ['Condo']), 'willoughby-townhomes-for-sale': (['Willoughby Heights'], ['Townhome']),
    'willoughby-heights-langley-condos-townhomes-for-sale': (['Willoughby Heights'], ['Condo', 'Townhome']),
    'white-rock-condos-for-sale': (['White Rock'], ['Condo']),
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
}
LANGLEY = {'Aldergrove', 'Langley City', 'Murrayville', 'Walnut Grove', 'Willoughby Heights', 'Fort Langley', 'Salmon River', 'Brookswood'}


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


def rentals(lab):
    l = lab.lower()
    if 'not allowed' in l: return 'No'
    if 'with restriction' in l: return 'Yes, with limits'
    if 'allowed' in l: return 'Yes'
    return ''


def age(s):
    s = str(s)
    if s.startswith('No age restriction tagged'): return 'No age limit'
    # "Restricted Age 55+ on 3 of 3; blank on 1 of 4; Bylaw Restrictions field includes Age Restrictions on 3 of 4": the age tags only
    ps = [(re.search(r'(\d+)\+', lab).group(1) + '+' if re.search(r'\d+\+', lab) else 'other', a, b) for lab, a, b in parts(s)
          if re.search(r'\d+\+', lab) or lab.strip().lower() == 'other']
    if not ps: return 'Not stated'
    if len({p[0] for p in ps}) > 1 or ps[0][0] == 'other': return 'Ask me'
    return ps[0][0]


def main(src):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    rows = []
    for tab, kind in TABS.items():
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
            rows.append({'name': str(d['Complex / building name']).strip(), 'sub': sub, 'type': kind, 'addr': str(d['Street address (no unit #)'] or '').strip(),
                         'built': built, 'homes': homes,
                         'pets': rule(d['Pets (per MLS listings, not the strata bylaws)'], pets),
                         'rentals': rule(d['Rentals (per MLS listings, not the strata bylaws)'], rentals),
                         'age': age(d['Age restriction (per MLS listings, not the strata bylaws)'])})
    # Names as listings spell them: "NEWPORT at WEST BEACH" -> "Newport at West Beach", "Luxia AT Yorkson" -> "Luxia at Yorkson".
    def tidy(n):
        n = re.sub(r'\bAT\b', 'at', n)
        return ' '.join(w.title() if w.isupper() and len(w) > 3 and not re.search(r'\d', w) else w for w in n.split(' '))
    for r in rows: r['name'] = tidy(r['name'])
    # One row per complex: the same first street address and type under several names ("Altus", "Altus White Rock",
    # "Unnamed complex at 1526 Finlay Street") keeps the plain name. Different buildings sharing an address keep their own rows.
    groups = {}
    for r in rows: groups.setdefault((r['addr'].split(';')[0].strip().lower(), r['type']), []).append(r)
    keep = []
    for (addr, _), g in groups.items():
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
        for f in ('pets', 'rentals', 'age'): o[f] = both(o[f], r[f])
        if r['addr'] and r['addr'] not in o['addr']: o['addr'] = (o['addr'] + '; ' + r['addr']).strip('; ')
        for f in ('built', 'homes'): o[f] = o[f] or r[f]
    rows.sort(key=lambda r: r['name'].lower())
    pages = {}
    for slug, (subs, types) in PAGES.items():
        if subs in ('SSWR55', 'LAN55'):
            pick = [i for i, r in enumerate(rows) if r['type'] in types and r['age'] in ('55+', '19+') and ((r['sub'] in LANGLEY) == (subs == 'LAN55'))]
        else:
            pick = [i for i, r in enumerate(rows) if r['sub'] in subs and r['type'] in types]
        if pick: pages[slug] = {'rows': pick, 'mixed': len(types) > 1}
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
    out = {'_note': 'Pets, rentals and age rules by complex, from the MLS® listings in each complex (Paragon, active and sold, checked November 2026), not the strata bylaws. Built by tools/build_strata_rules.py (D-313).',
           'checked': 'November 2026', 'rows': rows, 'pages': pages, 'buildings': buildings}
    (ROOT / 'src/data/strata-rules.json').write_text(json.dumps(out, ensure_ascii=False, indent=0) + '\n')
    print(len(rows), 'complexes;', {k: len(v['rows']) for k, v in pages.items()})


if __name__ == '__main__':
    main(sys.argv[1])
