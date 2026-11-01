"""Schools layer: turn the Muse education rollup into per-page 'Schools in <area>' sections.

Input:  docs/research/education-inventory-2026-11-01.csv  (Muse; K-12 from the BC Ministry of Education and Child Care school list,
        post-secondary from the Province's institution locations file; area placement from Muse's research files)
Output: src/data/schools/placements-<date>.json   (tiered placements, flags, pending pages)
        'gen: schools' blocks inside src/data/local/<slug>.json (created if absent; rebuilt on every run)

Publishing gate (Jared's rule: publish only what a source supports):
  city gate: the school's city (from its street address in the CSV) must match a city named on the page. Quilchena Elementary is in Vancouver, so it cannot sit on Quilchena, Richmond.
  tier 1  published  school is named for the area it is placed in (distinctive word shared), or a post-secondary campus that the
          Muse notes call unambiguous. The name itself supports the placement.
  tier 2  staged     placement rests only on Muse's reading of a research file. Held until each school's street address from
          education-inventory.csv confirms it (the CSV has not been supplied; see OI-33).
  flagged known-wrong or conflicting placements, never published.
Category labels in the rollup are NOT trusted (secondary schools appear under 'Elementary'); level is read from the school name.

    python3 -I tools/build_schools.py
"""
import glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = os.path.join(ROOT, 'docs/research/education-inventory-2026-11-01.csv')
OUT = os.path.join(ROOT, 'src/data/schools/placements-2026-11-01.json')

STOP = {'elementary', 'secondary', 'school', 'community', 'middle', 'annex', 'the', 'ecole', 'école', 'academy', 'neighbourhood', 'traditional',
        'fundamental', 'program', 'centre', 'education', 'learning', 'center', 'sda', 'for', 'campus', 'university', 'college', 'institute'}
GENERIC = {'heights', 'hill', 'hills', 'park', 'forest', 'mountain', 'lake', 'east', 'west', 'north', 'south', 'central', 'beach', 'creek', 'ridge', 'valley',
           'village', 'point', 'grove', 'city', 'town', 'downtown', 'maple', 'mission', 'woods', 'place', 'estates', 'little', 'poplar_', 'great', 'new'}
SUFFIX = r'-(guide|vw|ve|be|bn|bs|nv|nw|ri|cq|mr|pm|pq|wv|pi|surrey|langley|mission)$'

# Known-wrong or conflicting placements (never published). Reason is kept in the output file.
FLAGGED = {}  # city mismatches are now flagged automatically from the CSV address (King George Secondary was one; Muse corrected the CSV)
HOLD_PAGES = {}  # downtown-vw released 2026-11-01: Muse confirmed the area is downtown Vancouver; archive title corrected (D-50)
# Non-geographic or city-listing pages: not an area, no schools section.
NOT_AREA = {'mission-homes-for-sale', 'ladner-elementary-guide'}  # city listing page; area defined by the school itself
# Name matches the area only by a person's name or a wider place name: not a namesake placement, so staged.
TIER2_OVERRIDE = {('boyd-park', 'Hugh Boyd Secondary'): 'Hugh Boyd is a person; the match to Boyd Park may be coincidence',
                  ('mackenzie-heights', 'Sir Alexander Mackenzie Elementary'): 'named for a person, not the neighbourhood',
                  ('east-newton-guide', 'Newton Elementary'): 'Newton is wider than East Newton'}
NAMES = {'ladner-elementary-guide': 'the Ladner Elementary area', 'bradner-guide': 'Bradner', 'aberdeen-guide': 'Aberdeen', 'poplar-guide': 'Poplar',
         'mackenzie-heights': 'MacKenzie Heights', 'sunshine-hills-woods': 'Sunshine Hills Woods', 'east-newton-guide': 'East Newton',
         'english-bluff-guide': 'English Bluff', 'panorama-ridge-guide': 'Panorama Ridge', 'holly-guide': 'Holly', 'hawthorne-guide': 'Hawthorne',
         'neilsen-grove-guide': 'Neilsen Grove', 'port-guichon-guide': 'Port Guichon', 'fort-langley-guide': 'Fort Langley'}
CATCHMENT_LINK = {'sunnyside-park-surrey': '/south-surrey-school-catchments.html'}


def toks(s):
    return {t for t in re.findall(r"[a-zç']+", s.lower().replace('-', ' ')) if t not in STOP and len(t) > 2}


def parse():
    """area_slug -> [(category, name)], and (area_slug, name) -> csv row. Daycares are read but never published."""
    import csv
    areas, rows = {}, {}
    for r in csv.DictReader(open(SRC, encoding='utf-8')):
        if r['area_slug'].startswith('unassigned') : continue
        cat = {'elementary': 'Elementary schools', 'middle': 'Middle schools', 'secondary': 'Secondary / high schools', 'private': 'Private / independent schools',
               'college': 'Colleges', 'university': 'Universities', 'daycare': 'Licensed daycares / childcare'}.get(r['category'], 'Elementary+secondary schools')
        areas.setdefault(r['area_slug'], []).append((cat, r['name']))
        rows[(r['area_slug'], r['name'])] = r
    return areas, rows


CITY_FOLD = {'Fort Langley': 'Langley', 'Aldergrove': 'Langley', 'Dewdney': 'Mission', 'Deroche': 'Mission', 'Cultus Lake': 'Chilliwack', 'Rosedale': 'Chilliwack'}
PAGE_CITY_KEYS = [('north vancouver', 'North Vancouver'), ('west vancouver', 'West Vancouver'), ('new westminster', 'New Westminster'), ('port coquitlam', 'Port Coquitlam'),
                  ('port moody', 'Port Moody'), ('maple ridge', 'Maple Ridge'), ('pitt meadows', 'Pitt Meadows'), ('white rock', 'White Rock'),
                  ('vancouver', 'Vancouver'), ('burnaby', 'Burnaby'), ('richmond', 'Richmond'), ('surrey', 'Surrey'), ('coquitlam', 'Coquitlam'),
                  ('abbotsford', 'Abbotsford'), ('chilliwack', 'Chilliwack'), ('mission', 'Mission'), ('delta', 'Delta'), ('ladner', 'Delta'),
                  ('tsawwassen', 'Delta'), ('langley', 'Langley'), ('aldergrove', 'Langley'), ('agassiz', 'Agassiz'), ('hope', 'Hope')]


def page_cities(page):
    seo = page.get('seo', {})
    h1 = next((b['text'] for b in page['blocks'] if b.get('t') == 'h' and b.get('level') == 1), '')
    text = ' '.join([h1, seo.get('Title', ''), seo.get('Meta description', '')]).lower()
    found = set()
    for k, v in PAGE_CITY_KEYS:
        if k in text: found.add(v); text = text.replace(k, ' ')
    return found


def level(name, cat):
    n = name.lower()
    if cat in ('Colleges', 'Universities'): return 'campus'
    if 'secondary' in n: return 'secondary'
    if 'middle' in n: return 'middle'
    if 'elementary' in n or 'annex' in n: return 'elementary'
    return 'school'


def clean(name):
    name = re.sub(r'^Ecole ', 'École ', name)
    return re.sub(r'^(.+?) — (.+)$', lambda m: m.group(1) if m.group(1) in m.group(2) or 'Campus' in m.group(2) or 'Main' in m.group(2) else f'{m.group(1)} ({m.group(2)})', name)


def tier(slug, cat, name, city=None, page_cities_=None):
    if cat.startswith('Licensed daycares'): return 'excluded', 'childcare placements are not usable (3 of 3,462 placed)'
    if (slug, name) in FLAGGED: return 'flagged', FLAGGED[(slug, name)]
    if (slug, name) in TIER2_OVERRIDE: return 'tier2', TIER2_OVERRIDE[(slug, name)]
    if page_cities_ is not None and city is not None:
        if not page_cities_: return 'tier2', 'page names no city; address check not possible'
        if CITY_FOLD.get(city, city) not in page_cities_: return 'flagged', f'school is in {city} (street address) but the page is for {", ".join(sorted(page_cities_))}'
    if cat in ('Colleges', 'Universities'): return 'tier1', 'post-secondary campus placement called unambiguous in Muse coverage notes'
    base = re.sub(SUFFIX, '', slug)
    shared = (toks(base.replace('-', ' ')) & toks(name)) - GENERIC
    if shared: return 'tier1', 'named for the area (' + ', '.join(sorted(shared)) + ')'
    return 'tier2', 'placement from a research-file reading only; address check pending'


def area_name(slug, h1):
    if slug in NAMES: return NAMES[slug]
    n = re.split(r' Homes for Sale| Condos for Sale| Real Estate| \| |, |:', re.sub(r'^(Living in|Homes for Sale in) ', '', h1))[0].strip()
    return n


def oxford(ns):
    return ns[0] if len(ns) == 1 else ' and '.join(ns) if len(ns) == 2 else ', '.join(ns[:-1]) + ' and ' + ns[-1]


KIND = {'elementary': 'an elementary school', 'middle': 'a middle school', 'secondary': 'a secondary school', 'school': 'a school'}


def addr(a):
    a = (a or '').strip()
    return '' if not a or a.upper().startswith('PO BOX') or not re.search(r'[A-Za-z]', a) or not re.match(r'^[0-9#]', a) else a


def blocks_for(slug, area, items):
    """items: [(level, name, street_address)]"""
    def lab(n, a): return f'{clean(n)} ({addr(a)})' if addr(a) else clean(n)
    schools = [lab(n, a) for lv, n, a in items if lv != 'campus']
    campus = list(dict.fromkeys(re.sub(r' \(.*\)$', '', clean(n)) for lv, n, a in items if lv == 'campus'))
    sents = []
    if len(schools) == 1:
        lv = next(l for l, n, a in items if l != 'campus')
        sents.append(f'{schools[0]} is {KIND[lv]} in {area}.')
    elif schools:
        sents.append(f'Schools in {area} include {oxford(schools)}.')
    if campus:
        sents.append(f'{oxford(campus)} {"has a campus" if len(campus) == 1 else "have campuses"} in {area}.')
    sents.append('This is not a complete list of the schools nearby.')
    caveat = ('Living near a school does not mean a place at it. Your child\'s school comes from the district\'s catchment boundaries, and those change, '
              'so confirm the address with the district before you write an offer.')
    out = [{'t': 'h', 'level': 2, 'text': f'Schools in {area}', 'gen': 'schools'},
           {'t': 'p', 'text': ' '.join(sents), 'gen': 'schools'},
           {'t': 'p', 'text': caveat, 'gen': 'schools'}]
    if slug in CATCHMENT_LINK:
        out.append({'t': 'p', 'text': 'Read how South Surrey school catchments work', 'h': CATCHMENT_LINK[slug], 'gen': 'schools'})
    out.append({'t': 'p', 'text': 'Source: BC Ministry of Education and Child Care school list (2025/26, updated July 2026) and the Province\'s post-secondary locations list. Neighbourhood placement is from our own area research.', 'gen': 'schools'})
    return out


def main():
    areas, rows = parse()
    pages = {os.path.basename(p)[:-5]: json.load(open(p, encoding='utf-8')) for p in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    plc = {'tier1': [], 'tier2': [], 'flagged': [], 'excluded': []}
    for slug, lst in areas.items():
        for cat, name in lst:
            r = rows[(slug, name)]
            t, why = tier(slug, cat, name, r['city'], page_cities(pages[slug]) if slug in pages else None)
            plc[t].append({'area_key': slug, 'name': name, 'street_address': r['street_address'], 'city': r['city'], 'muse_category': cat, 'level_from_name': level(name, cat), 'reason': why, 'page_exists': slug in pages})
    # one page per place: a namesake school on a pair (poplar / poplar-guide) goes on the guide page only
    pub = {}
    for p in plc['tier1']:
        s = p['area_key']
        if s in NOT_AREA or s in HOLD_PAGES or not p['page_exists']: continue
        pub.setdefault(s, []).append((p['level_from_name'], p['name'], p['street_address']))
    for s in list(pub):
        if not s.endswith('-guide') and s + '-guide' in pub: del pub[s]
    # remove every previous generated schools block, then write fresh ones
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if any(b.get('gen') == 'schools' for b in d.get('blocks', [])):
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'schools']
            if not d['blocks'] and d.get('status') == 'generated': os.remove(f); continue
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
    for s, items in sorted(pub.items()):
        h1 = next((b['text'] for b in pages[s]['blocks'] if b.get('t') == 'h' and b.get('level') == 1), s)
        new = blocks_for(s, area_name(s, h1), items)
        f = os.path.join(ROOT, f'src/data/local/{s}.json')
        if os.path.exists(f):
            d = json.load(open(f, encoding='utf-8')); d['blocks'] += new
        else:
            d = {'status': 'generated', 'slug': s, 'updated': '2026-11-01', 'blocks': new}
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
    plc['pending_pages'] = sorted({p['area_key'] for p in plc['tier1'] + plc['tier2'] if not p['page_exists']})
    plc['held_pages'] = HOLD_PAGES
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(plc, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(OUT, 'a').write('\n')
    print('published on', len(pub), 'pages;', {k: len(v) for k, v in plc.items() if isinstance(v, list)}, '; pending new pages:', len(plc['pending_pages']))


if __name__ == '__main__':
    main()
