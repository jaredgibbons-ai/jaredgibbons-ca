"""D-377: batch 6 of the core pages that rank below position 20 (Search Console, URL-prefix property, last 28 days, bot searches removed).
Jared, Nov 19 2026: "ok thanks can you work on the next batch of pages".

What the searches showed, and what changes:
  fleetwood-tynehead-...condos-townhomes  "fleetwood condos for sale" 25.5      -> title/H1 lead with "Fleetwood Condos & Townhouses"
  campbell-valley                         "south langley real estate" 20,
                                          "homes for sale in south langley" 5   -> title names South Langley
  sell-my-house-in-surrey                 "sell my home surrey bc" 47           -> "Surrey BC" and the free evaluation in the title
  langley-city-guide                      "langley city map", "city of langley zoning map", "langley zip code"
                                                                                -> new section: the Langley City map, the zoning map and
                                                                                   the postal code, sourced to the City; 3 more inbound links
  guildford-townhomes-for-sale            "townhouses for sale guildford" 18    -> "Townhouses" (D-372 wording)
  murrayville-condos-for-sale             "condos for sale murrayville bc" 26.8 -> "Langley BC" in the title
  surrey-farms                            "farms for sale surrey" lands on cloverdale-farms at 79-95
                                                                                -> surrey-farms leads with "Farms for Sale in Surrey BC";
                                                                                   4 more inbound links from the Surrey acreage pages
  surrey-homes-under-1m                   -> "Affordable" in the title
Run once from the repo root: python3 tools/core_pages_6_2026_11_19.py
"""
import json, os

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

# 1. Titles, H1s and descriptions.
SF = 'src/data/seo-final.json'
sf = load(SF)
for slug, t, h, desc in [
    ('fleetwood-tynehead-surrey-condos-townhomes-for-sale', 'Fleetwood Condos & Townhouses for Sale | Fleetwood Tynehead',
     'Fleetwood Condos and Townhouses for Sale, Surrey',
     'Fleetwood condos and townhouses for sale in Surrey, from Fleetwood Town Centre to Tynehead. Review condo buildings, townhouse complexes and buyer FAQs.'),
    ('campbell-valley', 'South Langley Acreages & Homes for Sale | Campbell Valley',
     'Campbell Valley Acreages & Homes for Sale, South Langley', None),
    ('sell-my-house-in-surrey', 'Sell My House in Surrey BC | Free Evaluation & Zoning Rules', 'Sell My House in Surrey, BC',
     'Selling a house in Surrey BC? Get a free home evaluation, see what your old RF or RH zone is now (R1 to R7), and check suite, coach house and Airbnb rules.'),
    ('langley-city-guide', 'Langley City Guide | Map, Zoning, Parks & SkyTrain', 'Living in Langley City, BC',
     'Langley City guide: area map, zoning map and postal code, condo buildings near 205 Street, City Park, Nicomekl Elementary and the SkyTrain extension.'),
    ('guildford-townhomes-for-sale', 'Guildford Townhouses for Sale | North Surrey Strata', 'Guildford Townhouses for Sale', None),
    ('murrayville-condos-for-sale', 'Murrayville Condos for Sale | Langley BC, Near Hospital', 'Murrayville Condos for Sale, Langley', None),
    ('surrey-farms', 'Farms for Sale in Surrey BC | Agricultural Land & ALR Checks', 'Farms & Acreages for Sale in Surrey, BC', None),
    ('surrey-homes-under-1m', 'Affordable Surrey Homes Under $1M | Houses for Sale', None, None),
]:
    assert len(t) <= 60, (len(t), t)
    sf[slug]['title'] = t
    if h: sf[slug]['h1'] = h
    if desc:
        assert len(desc) <= 158, (len(desc), desc); sf[slug]['description'] = desc
save(SF, sf)

# 2. Langley City guide: what people searching for a Langley City map, zoning map or postal code came for (City sources only).
G = 'src/data/local/langley-city-guide.json'
g = load(G)
if not any(b.get('gen') == 'map1119' for b in g['blocks']):
    sec = [
        {'t': 'h', 'level': 2, 'text': 'Langley City map, zoning map and postal code'},
        {'t': 'areamap', 'region': 'langley', 'mode': 'area', 'current': 'langley-city'},
        {'t': 'p', 'text': 'Langley City (the City of Langley) and Langley Township are separate municipalities, each with its own zoning bylaw '
                           'and zoning map. In the City, Zoning Bylaw No. 3300 (2025) applies. The City’s Interactive Map lets you search an '
                           'address and see properties, streets, parks, utilities and air photos, and the City posts free PDF maps, including a '
                           'Langley City Map and a Map of the Langleys showing the City and the Township.'},
        {'t': 'p', 'text': 'Downtown Langley postal codes start with V3A. A postal code does not settle whether a home is in the City or the '
                           'Township; the property tax notice does, and so does the address search on the City’s Interactive Map.'},
        {'t': 'list', 'items': [
            [{'t': 'City of Langley: maps and open data (Interactive Map and PDF maps)', 'h': 'https://langleycity.ca/ourcommunity/maps-and-open-data'}],
            [{'t': 'City of Langley: Zoning Bylaw', 'h': 'https://langleycity.ca/business-development/zoning-bylaw'}],
            [{'t': 'geocoder.ca: postal code V3A 3V3, Downtown Langley', 'h': 'https://geocoder.ca/V3A3V3'}],
        ]},
    ]
    g['blocks'] = [dict(b, gen='map1119') for b in sec] + g['blocks']
    save(G, g)

# 3. Inbound links: one "Also worth comparing:" line under the introduction (gen lnk1119, the D-373/374 pattern).
H1 = {s: sf[s]['h1'] for s in ('langley-city-guide', 'surrey-farms')}
ADD = {
    'city-of-langley-houses-for-sale': ['langley-city-guide'],
    'langley-homes-for-sale': ['langley-city-guide'],
    'surrey-acreages-for-sale': ['surrey-farms'],
    'cloverdale-acreages-for-sale': ['surrey-farms'],
    'south-surrey-acreages-for-sale': ['surrey-farms'],
    'hazelmere': ['surrey-farms'],
}
for s, ts in ADD.items():
    p = f'src/data/local/{s}.json'
    if not os.path.exists(p): print('no local file, skipped:', s); continue
    d = load(p); blocks = d.setdefault('blocks', [])
    line = next((b for b in blocks if b.get('gen') == 'lnk1119'), None)
    have = {x.get('h') for x in (line or {}).get('parts', [])}
    new = [(t, H1[t]) for t in ts if f'/{t}.html' not in have]
    if not new: continue
    items = ([(x['h'][1:-5], x['t']) for x in line['parts'] if x.get('h')] if line else []) + new
    parts = [{'t': 'Also worth comparing: '}]
    for i, (t, label) in enumerate(items):
        if i: parts.append({'t': ' and ' if i == len(items) - 1 else ', '})
        parts.append({'t': label, 'h': f'/{t}.html'})
    parts.append({'t': '.'})
    if line: line['parts'] = parts
    else: blocks.append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1119', 'parts': parts})
    save(p, d); print('linked', s, '->', ts)
