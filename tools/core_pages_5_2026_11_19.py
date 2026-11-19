"""D-375: fifth batch. (1) Six of Jared's own area notes (Area Thoughts PDF, 2026-11-03) that were held for a fact check are checked
against the facts the site's guides already source, edited only where a fact did not hold, and published as "Jared's take" on the
page build_area_thoughts.py chose for each. (2) Titles and H1s on 11 more core pages, following what D-366 to D-372 measured.
Run once from the repo root: python3 tools/core_pages_5_2026_11_19.py
"""
import json, os

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    _FMT[p] = (dict(indent=1), False, ''); return d
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

# name -> (checked text, what the check found)
TAKES = {
    'Walnut Grove': (None, 'Walnut Grove Community Plan adopted November 26, 1979 (walnut-grove-guide, Township OCP Schedule 6).'),
    'Murrayville, Langley': ('Around the historic Five Corners at Fraser Highway and 216 Street, Murrayville is the Township’s traditional civic core and an established central neighbourhood. It’s also one of only two heritage conservation areas in the Township.',
                             'Heritage conservation area: one of two in the Township (murrayville-guide). The PDF text ended mid-sentence ("in the"); completed with the guide’s wording.'),
    'Salmon River': ('Salmon River, along the river of the same name, is a rural acreage and farm district. Its Salmon River Uplands designation is there to protect the rural residential character.',
                     'Uplands: the Rural Plan keeps the Salmon River Uplands for rural residential and agricultural uses (salmon-river-guide, Bylaw 5983). "Named for the river" reworded to what the guide supports.'),
    'Royal Heights, Surrey': ('Small and self-contained, Royal Heights is an enclave whose story is elevation and views over the lowland. Most of the houses around the park date from the late 1950s to the early 1970s, when the streets were first built.',
                              'Age: the City says most homes there were built from the late 1950s to the early 1970s; the typical house sold was built in 1960 (royal-heights-guide). "Mid-1960s" was when the park was set up.'),
    'East Newton': ('Single-family subdivision houses close to SD36 schools like Chimney Hill Elementary and Frank Hurt Secondary make East Newton the family end of the Surrey market. Locals call one part of it Chimney Hill.',
                    'Schools: the guide lists more than four SD36 schools in and near the area (Chimney Hill, T.E. Scott, M B Sanford and Georges Vanier elementaries, Frank Hurt and Tamanawis secondaries), so "four" became two named ones.'),
    'North Surrey': ('North Surrey isn’t really one neighbourhood. It’s Surrey’s urban north, from Whalley and Guildford to Fraser Heights, Cedar Hills and Port Kells. People come here for the City Centre towers and Holland Park more than a village feel.',
                     'Areas: FVREB’s North Surrey is eight sub-areas (Bridgeview, Bolivar Heights, Fraser Heights, Royal Heights, Cedar Hills, Whalley, Guildford, Port Kells); Fleetwood is not one of them, so it was swapped for sub-areas that are.'),
}
p = 'src/data/area-thoughts.json'; at = load(p)
for e in at['entries']:
    if e['name'] in TAKES and e['status'] == 'verify':
        text, note = TAKES[e['name']]
        if text: e['text'] = text
        e['status'] = 'ready'; e['flags'] = []; e['checked'] = f'2026-11-19: {note}'
        lp = f"src/data/local/{e['page']}.json"; d = load(lp)
        d['blocks'] = [b for b in d.get('blocks', []) if b.get('gen') != 'jtake']
        d['blocks'] += [{'t': 'h', 'level': 2, 'text': f"Jared's take on {e['name'].split(',')[0]}", 'gen': 'jtake'}, {'t': 'p', 'text': e['text'], 'gen': 'jtake'}]
        save(lp, d)
save(p, at)

SEO = {
    'surrey-townhomes-under-1-2m': ('Surrey Townhouses Under $1.2M | Fleetwood to Guildford', 'Surrey Townhouses Under $1.2M'),
    'walnut-grove-townhomes-for-sale': ('Walnut Grove Townhouses for Sale, Langley | Complexes', 'Walnut Grove Townhouses and Townhomes for Sale'),
    'willoughby-townhomes-for-sale': ('Willoughby Townhouses for Sale, Langley | Strata Checks', 'Willoughby Townhouses and Townhomes for Sale'),
    'south-surrey-townhomes-under-1-2m': ('South Surrey Townhouses Under $1.2M | Compare Complexes', 'South Surrey Townhouses Under $1.2M'),
    'cedar-hills-surrey-condos-townhomes-for-sale': ('Cedar Hills Condos & Townhouses for Sale | North Surrey', 'Cedar Hills Condos and Townhouses for Sale'),
    'langley-houses-for-sale': ('Houses for Sale in Langley BC | Detached Homes & Lot Rules', 'Houses for Sale in Langley, BC'),
    'walnut-grove-houses-for-sale': ('Walnut Grove Houses for Sale, Langley | Suites & Lots', None),
    'murrayville-houses-for-sale': ('Murrayville Houses for Sale, Langley | Suites & Lot Checks', None),
    'morgan-creek-south-surrey-houses-for-sale': ('Morgan Creek Houses for Sale, South Surrey | Lots & Rules', None),
    'grandview-south-surrey-houses-for-sale': ('Grandview Heights Houses for Sale | South Surrey Trends', 'Grandview Heights Houses for Sale, South Surrey'),
    'langley-golf-course-homes-for-sale': ('Langley Golf Course Homes for Sale | Courses & Prices', None),
}
p = 'src/data/seo-final.json'; sf = load(p)
for slug, (t, h) in SEO.items():
    assert len(t) <= 60, (slug, len(t)); sf[slug]['title'] = t
    if h: sf[slug]['h1'] = h
save(p, sf)
print('ok')
