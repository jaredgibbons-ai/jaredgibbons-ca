#!/usr/bin/env python3
"""Publish the held school placements whose MLS® sub-area is now confirmed (D-392; OI-33).

The 116 staged placements (src/data/schools/placements-2026-11-01.json, tier 2) waited for each school's Paragon sub-area. Jared's
team filled the lookup by address (docs/research/school-subarea-lookup-filled-2026-11-20.csv). A school is published on a page only when
its Paragon sub-area is the page's own sub-area (docs/review/idx/subarea-page-map-2026-11-04.csv, or the page key is the sub-area name).
Schools in a different sub-area, with no sub-area (Chilliwack tax records, PO boxes) or whose area has no page stay unpublished and are
listed in the placements file with the reason.

Schools a page already names are not added twice. Pages that already have a "Schools in <area>" section get one added sentence; pages without one get the section build_schools.py writes.
Nothing else on the page is touched (build_schools.py itself is not re-run: later tools have edited its blocks). Idempotent.

    python3 -I tools/school_subareas_2026_11_20.py
"""
import csv, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_schools as B

PLC = 'src/data/schools/placements-2026-11-01.json'
P = json.load(open(PLC))
rows = list(csv.reader(open('docs/research/school-subarea-lookup-filled-2026-11-20.csv')))[1:]
SUB = {(r[0], r[1]): r[7].strip() for r in rows}
MAP, BYSUB = {}, {}
for r in csv.DictReader(open('docs/review/idx/subarea-page-map-2026-11-04.csv')):
    for s in r['our pages that match (slug)'].split(' | '):
        if s.strip(): MAP[s.strip()] = r['board sub-area']; BYSUB.setdefault(r['board sub-area'].lower(), []).append(s.strip())
def page_for_sub(sub, city):
    # the sub-area's own area page (its guide if there is one), named for the sub-area, in the school's city
    k = slugify(sub.rstrip('.'))
    c = [x for x in BYSUB.get(sub.lower(), []) if (x == k or x.startswith(k + '-')) and not re.search(r'-(for-sale|homes|houses|condos|townhomes)', x)]
    for x in sorted(set(c) | {k, k + '-guide'}, key=lambda x: (not x.endswith('-guide'), len(x))):
        if not exists(x): continue
        cities = B.page_cities(json.load(open(f'src/data/pages/{x}.json')))
        if cities and B.CITY_FOLD.get(city, city) not in cities: continue
        return x
    return None
REDIRECT = {'aldergrove-langley': 'aldergrove', 'brookswood-langley': 'brookswood', 'fort-langley': 'fort-langley-guide', 'surrey-city-centre': 'surrey-city-centre-guide'}
slugify = lambda x: re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')
exists = lambda s: os.path.exists(f'src/data/pages/{s}.json')
TAG = 'MLS® sub-area confirmed in Paragon by address, November 20, 2026.'

def target(key):
    base = REDIRECT.get(key, key[:-6] if key.endswith('-guide') else key)
    for s in (base + '-guide', base):     # one page per place: the guide when there is one
        if exists(s): return s
    return None

pub, keep2 = {}, []
for p in P['tier2']:
    key, name = p['area_key'], p['name']
    sub = SUB.get((key, name), '')
    base = key[:-6] if key.endswith('-guide') else key
    page_sub = MAP.get(key) or MAP.get(base) or MAP.get(base + '-guide')
    t = target(key)
    if not sub or sub == '-':
        p['reason'] = 'no Paragon sub-area for this address (PO box or no tax record); stays unpublished'; keep2.append(p); continue
    if not ((page_sub and page_sub.lower() == sub.lower()) or slugify(sub) == slugify(base)):
        other = page_for_sub(sub, p['city'])
        if not other:
            p['reason'] = f'Paragon sub-area is {sub}, not the page\'s area, and {sub} has no area page; stays unpublished'; keep2.append(p); continue
        p['reason'] = f'Paragon sub-area is {sub}, so it is published on that area\'s page instead of {key} (lookup filled Nov 20, 2026)'; p['published_on'] = other
        pub.setdefault(other, []).append(p); continue
    if not t:
        p['reason'] = f'Paragon sub-area {sub} confirmed, but there is no page for this area yet'; keep2.append(p); continue
    p['reason'] = f'Paragon sub-area {sub} matches the page (lookup filled Nov 20, 2026)'; p['published_on'] = t
    pub.setdefault(t, []).append(p)

promoted = [p for v in pub.values() for p in v]
P['tier1'] = P['tier1'] + promoted
P['tier2'] = keep2
def area_of(slug):
    pg = json.load(open(f'src/data/pages/{slug}.json'))
    h1 = next((b['text'] for b in pg['blocks'] if b.get('t') == 'h' and b.get('level') == 1), slug)
    return B.area_name(slug, h1)

def has_other_school_section(slug):
    # a guide's own "Schools in / Schools for <area>" section (not this layer's): a second schools heading would repeat it
    for x in (f'src/data/local/{slug}.json', f'src/data/pages/{slug}.json'):
        if os.path.exists(x):
            for b in json.load(open(x, encoding='utf-8')).get('blocks', []):
                if b.get('t') == 'h' and b.get('gen') != 'schools' and re.match(r'Schools (in|for) ', b.get('text') or ''): return True
    return False

def named_on(slug, name):
    # a school the page already names (in its guide, its local sections or the archive text) is not added again
    txt = ''.join(open(x, encoding='utf-8').read() for x in (f'src/data/local/{slug}.json', f'src/data/pages/{slug}.json') if os.path.exists(x))
    return re.sub(r'^(École|Ecole) ', '', name) in txt

for slug, items in sorted(pub.items()):
    items = [p for p in items if not named_on(slug, p['name'])]
    if not items: continue
    if has_other_school_section(slug):
        for p in items: p['reason'] += '; not added: the page already has its own schools section (add it there by hand if wanted)'
        continue
    f = f'src/data/local/{slug}.json'
    d = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {'status': 'generated', 'slug': slug, 'updated': '2026-11-20', 'blocks': []}
    raw = open(f).read() if os.path.exists(f) else ''
    lab = [f'{B.clean(p["name"])} ({B.addr(p["street_address"])})' if B.addr(p['street_address']) else B.clean(p['name']) for p in items]
    sch = [b for b in d['blocks'] if b.get('gen') == 'schools']
    if any(TAG in (b.get('text') or '') for b in sch): continue     # already done
    area = area_of(slug)
    if sch:
        para = next(b for b in sch if b.get('t') == 'p' and 'not a complete list' in (b.get('text') or ''))
        add = f'{lab[0]} is also in {area}.' if len(lab) == 1 else f'Other schools in {area} include {B.oxford(lab)}.'
        para['text'] = para['text'].replace(' This is not a complete list', f' {add} This is not a complete list')
        srcb = next((b for b in sch if (b.get('text') or '').startswith('Source:')), None)
        if srcb: srcb['text'] += ' ' + TAG
        else: d['blocks'].insert(d['blocks'].index(para) + 1, {'t': 'p', 'text': TAG, 'gen': 'schools'})
    else:
        new = B.blocks_for(slug, area, [(B.level(p['name'], p['muse_category']), p['name'], p['street_address']) for p in items])
        new[-1]['text'] += ' ' + TAG
        d['blocks'] += new
    ind = 2 if raw.startswith('{\n  ') or not raw else 1
    json.dump(d, open(f, 'w', encoding='utf-8'), indent=ind, ensure_ascii=False); open(f, 'a').write('\n')
json.dump(P, open(PLC, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(PLC, 'a').write('\n')
print('published', len(promoted), 'schools on', len(pub), 'pages; still held', len(keep2))
