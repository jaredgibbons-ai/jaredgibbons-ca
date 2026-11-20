"""D-381: the 14 core pages that get 10+ Google views a week but had not been worked on (D-378 list).
Jared, Nov 20 2026: "For the 14 pages that are very good. What are they missing? How can we make them better".
Search Console (URL-prefix property, 28 days, bot searches removed) showed three problems, not missing content:
  1. Wrong page ranking. "condos for sale south surrey white rock" and its variants land on the 55+ condo page (45 imp.,
     positions 21-74); "condos for sale white rock" lands on the White Rock 2-bedroom page (11 imp., 49.8); "surrey bc
     neighbourhoods" lands on the South Surrey neighbourhoods page (47 imp., 29.6). Each page now points to the page that
     should rank, near the top, with the search's own words as the link text.
  2. The three Langley guides get "where is" and map searches ("where is aldergrove", "aldergrove map", "where is
     murrayville", "walnut grove langley bc") and had no map or location answer. Each gets a "Where is ...?" section with the
     area outline map and drive times, using Jared's own location sentence from his overviews (D-379/380); titles and
     descriptions say where the area is.
  3. The guides have 9-12 inbound links. Each area's house, townhome and condo pages now link to it.
Run once from the repo root: python3 tools/core_pages_7_2026_11_20.py
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

# 1. Titles, H1s, descriptions.
SF = 'src/data/seo-final.json'; sf = load(SF)
for slug, t, h, desc in [
    ('aldergrove-guide', 'Aldergrove BC Guide | Where It Is, Map, Schools & Parks', None,
     "Where is Aldergrove? On the Township of Langley's eastern border, toward Abbotsford. Map, drive times, schools, the community centre pools and regional park."),
    ('murrayville-guide', 'Murrayville, Langley BC Guide | Map, Hospital & Heritage', 'Murrayville, Langley: Neighbourhood Guide',
     'Where is Murrayville? Just east of Langley City on the Fraser Highway. Map, drive times, Langley Memorial Hospital, schools and the heritage area rules.'),
    ('walnut-grove-guide', 'Walnut Grove, Langley BC Guide | Map, Schools & Parks', 'Walnut Grove, Langley: Neighbourhood Guide',
     'Where is Walnut Grove? Northwest Langley, north of Highway 1 near the Golden Ears Bridge. Map, drive times, schools, the 50 m pool and parks.'),
    ('south-surrey-neighbourhoods', 'South Surrey & White Rock Neighbourhoods | Map & 9 Guides', None, None),
]:
    assert len(t) <= 60, (len(t), t); sf[slug]['title'] = t
    if h: sf[slug]['h1'] = h
    if desc: assert len(desc) <= 160, (len(desc), desc); sf[slug]['description'] = desc
save(SF, sf)

# 2. "Where is ...?" on the three guides: the area outline, drive times, and Jared's location sentence.
WHERE = {
    'aldergrove-guide': ('aldergrove', 'Where is Aldergrove?', [
        {'t': 'Aldergrove sits on the eastern border of the Township of Langley, toward Abbotsford, with a local main street along the '
               'Fraser Highway. Highway 13 (264 Street) runs south to the Aldergrove–Lynden border crossing, and Highway 1 is a short drive north. '},
        {'t': 'Homes for sale in Aldergrove', 'h': '/aldergrove.html'}, {'t': '.'}]),
    'murrayville-guide': ('murrayville', 'Where is Murrayville?', [
        {'t': 'Murrayville is in the Township of Langley, just east of the City of Langley, along the Fraser Highway. The Township calls it the '
               'traditional civic core, and the historic heart of the community grew up around Murray’s Corner. '},
        {'t': 'Homes for sale in Murrayville', 'h': '/murrayville.html'}, {'t': '.'}]),
    'walnut-grove-guide': ('walnut-grove', 'Where is Walnut Grove?', [
        {'t': 'Walnut Grove is in the northwest Township of Langley, north of Highway 1. The Golden Ears Bridge connects it to Maple Ridge and '
               'Pitt Meadows, and Carvolth Exchange, at 202 Street and 86 Avenue, sits at its south edge next to the highway. '},
        {'t': 'Homes for sale in Walnut Grove', 'h': '/walnut-grove.html'}, {'t': '.'}]),
}
for slug, (area, head, parts) in WHERE.items():
    p = f'src/data/local/{slug}.json'; d = load(p)
    if any(b.get('gen') == 'where1120' for b in d['blocks']): continue
    sec = [{'t': 'h', 'level': 2, 'text': head}, {'t': 'p', 'parts': parts},
           {'t': 'areamap', 'region': 'langley', 'mode': 'area', 'current': area}, {'t': 'commute', 'region': 'langley', 'current': area}]
    d['blocks'] = [dict(b, gen='where1120') for b in sec] + d['blocks']
    save(p, d); print('where section:', slug)

# 3. Point the misdirected searches at the right page (a line under the introduction, gen lnk1120).
LINES = {
    'south-surrey-white-rock-55-plus-condos-for-sale': [
        {'t': 'Not limited to 55+? See all '}, {'t': 'South Surrey & White Rock condos for sale', 'h': '/south-surrey-condos-for-sale.html'},
        {'t': ', or only '}, {'t': 'White Rock condos for sale', 'h': '/white-rock-condos-for-sale.html'}, {'t': '.'}],
    'white-rock-2-bedroom-condos-for-sale': [
        {'t': 'Any size will do? See all '}, {'t': 'White Rock condos for sale', 'h': '/white-rock-condos-for-sale.html'},
        {'t': ', or '}, {'t': 'South Surrey & White Rock condos for sale', 'h': '/south-surrey-condos-for-sale.html'}, {'t': '.'}],
    'south-surrey-neighbourhoods': [
        {'t': 'Looking at the rest of the city? Compare all '}, {'t': 'Surrey BC neighbourhoods', 'h': '/surrey-neighbourhood-guides.html'},
        {'t': ', from Cloverdale and Fleetwood to Newton and Guildford.'}],
}
for slug, parts in LINES.items():
    p = f'src/data/local/{slug}.json'; d = load(p)
    if any(b.get('gen') == 'lnk1120' for b in d['blocks']): continue
    d['blocks'].append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1120', 'parts': parts}); save(p, d); print('line:', slug)

# 4. Links to the guides from their area's house, townhome and condo pages (the D-374 "Also worth comparing:" line).
H1 = {'aldergrove-guide': 'Aldergrove neighbourhood guide', 'murrayville-guide': 'Murrayville neighbourhood guide', 'walnut-grove-guide': 'Walnut Grove neighbourhood guide'}
for guide in H1:
    area = guide[:-6]
    for kind in ('houses', 'townhomes', 'condos'):
        s = f'{area}-{kind}-for-sale'; p = f'src/data/local/{s}.json'
        if not os.path.exists(p): continue
        d = load(p); blocks = d['blocks']
        line = next((b for b in blocks if b.get('gen') == 'lnk1119'), None)
        have = {x.get('h') for x in (line or {}).get('parts', [])}
        if f'/{guide}.html' in have: continue
        items = ([(x['h'], x['t']) for x in line['parts'] if x.get('h')] if line else []) + [(f'/{guide}.html', H1[guide])]
        parts = [{'t': 'Also worth comparing: '}]
        for i, (h, label) in enumerate(items):
            if i: parts.append({'t': ' and ' if i == len(items) - 1 else ', '})
            parts.append({'t': label, 'h': h})
        parts.append({'t': '.'})
        if line: line['parts'] = parts
        else: blocks.append({'t': 'p', 'pos': 'after-intro', 'gen': 'lnk1119', 'parts': parts})
        save(p, d); print('guide link:', s, '->', guide)
