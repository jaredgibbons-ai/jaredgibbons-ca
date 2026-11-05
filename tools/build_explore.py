#!/usr/bin/env python3
"""Explore-links block for every listing-search page -> src/data/explore.json {slug: {cols: [{h, links:[[text, href]], more:[[text, href]]}]}}.
Rendered by src/components/ExploreLinks.astro at the end of the page (template output, not page content; the main menu is unchanged).
Columns: 1 'Explore <place> real estate' (the same place's other searches, guide and new construction), 2 'Popular <city> searches' (other searches in the city),
3 'Nearby cities' (city page + new-construction page of each neighbour), 4 'New construction in <city>'.
City membership comes from the breadcrumb trails (src/data/breadcrumbs.json and each page's own local trail); neighbours are plain geography.
    python3 -I tools/build_explore.py"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
import build_new_construction_subareas as S

pages, local = {}, {}
for f in glob.glob('src/data/pages/*.json'):
    d = json.load(open(f)); pages[d['slug']] = d
for f in glob.glob('src/data/local/*.json'):
    local[os.path.basename(f)[:-5]] = json.load(open(f))
BC = json.load(open('src/data/breadcrumbs.json'))
exist = set(pages) | {s for s, l in local.items() if l.get('new_page')}
def has_grid(s):
    bl = (pages[s]['blocks'] if s in pages else []) + (local.get(s, {}).get('blocks', []))
    return any(b.get('t') == 'grid' for b in bl)
grid = sorted(s for s in exist if has_grid(s))

# ---- cities
HUBS = {k[:-len('-homes-for-sale')]: k for k in exist if k.endswith('-homes-for-sale') and k.count('-') <= 5}
HUBS.update({'cloverdale': 'cloverdale-houses-for-sale', 'south-surrey': 'south-surrey-homes-for-sale'})
HUBS = {k: v for k, v in HUBS.items() if v in exist}
CITYKEYS = ['abbotsford', 'burnaby', 'chilliwack', 'cloverdale', 'coquitlam', 'langley', 'ladner', 'maple-ridge', 'mission', 'new-westminster', 'north-delta', 'north-vancouver', 'pitt-meadows', 'port-coquitlam', 'port-moody',
            'richmond', 'sardis', 'south-surrey', 'surrey', 'tsawwassen', 'vancouver', 'west-vancouver', 'white-rock', 'delta']
CITYKEYS = [k for k in CITYKEYS if k in HUBS]
CITYKEYS.sort(key=len, reverse=True)
NAME = lambda k: k.replace('-', ' ').title()
NEAR = {'south-surrey': ['surrey', 'langley', 'cloverdale', 'north-delta'], 'surrey': ['south-surrey', 'cloverdale', 'langley', 'north-delta', 'new-westminster'],
        'cloverdale': ['surrey', 'langley', 'south-surrey'], 'langley': ['surrey', 'cloverdale', 'abbotsford', 'maple-ridge', 'south-surrey'], 'abbotsford': ['langley', 'mission', 'chilliwack'],
        'mission': ['abbotsford', 'maple-ridge'], 'chilliwack': ['sardis', 'abbotsford'], 'sardis': ['chilliwack', 'abbotsford'], 'maple-ridge': ['pitt-meadows', 'mission', 'langley', 'port-coquitlam'],
        'pitt-meadows': ['maple-ridge', 'port-coquitlam', 'coquitlam'], 'port-coquitlam': ['coquitlam', 'pitt-meadows', 'maple-ridge', 'port-moody'], 'coquitlam': ['port-coquitlam', 'port-moody', 'burnaby', 'new-westminster'],
        'port-moody': ['coquitlam', 'port-coquitlam', 'burnaby'], 'burnaby': ['new-westminster', 'coquitlam', 'vancouver', 'richmond', 'port-moody'], 'new-westminster': ['burnaby', 'coquitlam', 'surrey'],
        'richmond': ['vancouver', 'burnaby', 'ladner', 'new-westminster'], 'vancouver': ['burnaby', 'richmond', 'north-vancouver', 'west-vancouver'], 'north-vancouver': ['west-vancouver', 'vancouver', 'burnaby'],
        'west-vancouver': ['north-vancouver', 'vancouver'], 'ladner': ['tsawwassen', 'richmond', 'north-delta'], 'tsawwassen': ['ladner', 'north-delta', 'south-surrey'], 'north-delta': ['surrey', 'ladner', 'tsawwassen', 'new-westminster'],
        'white-rock': ['south-surrey', 'surrey'], 'delta': ['north-delta', 'ladner', 'tsawwassen']}
NCPAGE = {k: f'new-construction-{k}' for k in CITYKEYS if f'new-construction-{k}' in exist}
NCPAGE.update({'surrey': 'surrey-presale-condos-and-townhomes', 'langley': 'new-construction-presales-in-langley-bc', 'abbotsford': 'abbotsford-presale-condos-and-townhomes', 'coquitlam': 'coquitlam-presale-condos-and-townhomes',
               'burnaby': 'burnaby-presale-condos-and-townhomes', 'vancouver': 'vancouver-presale-condos-and-townhomes', 'south-surrey': 'south-surrey-presale-condos'})
NCPAGE = {k: v for k, v in NCPAGE.items() if v in exist}
HUB_TO_CITY = {v: k for k, v in HUBS.items()}
AREA2CITY = {'Abbotsford': 'abbotsford', 'Cloverdale': 'cloverdale', 'Langley': 'langley', 'South Surrey White Rock': 'south-surrey', 'Surrey': 'surrey', 'North Surrey': 'surrey', 'Burnaby North': 'burnaby', 'Burnaby South': 'burnaby',
             'Chilliwack': 'chilliwack', 'Sardis': 'sardis', 'Coquitlam': 'coquitlam', 'Ladner': 'ladner', 'Maple Ridge': 'maple-ridge', 'Mission': 'mission', 'New Westminster': 'new-westminster', 'North Vancouver': 'north-vancouver',
             'Port Coquitlam': 'port-coquitlam', 'Port Moody': 'port-moody', 'Richmond': 'richmond', 'Tsawwassen': 'tsawwassen', 'Vancouver East': 'vancouver', 'Vancouver West': 'vancouver', 'West Vancouver': 'west-vancouver'}

def crumbs(s): return (local.get(s, {}).get('breadcrumbs')) or BC.get(s) or []
SUB_NC = {c['slug']: AREA2CITY[c['area']] for c in S.load()}

def city_of(s):
    if s in SUB_NC: return SUB_NC[s]
    if s in HUB_TO_CITY: return HUB_TO_CITY[s]
    for k in ['new-construction-' + k for k in CITYKEYS]:
        if s == k: return k[len('new-construction-'):]
    cr = crumbs(s)
    if len(cr) >= 3:
        h = re.sub(r'^/|\.html$', '', cr[1]['href'])
        if h in HUB_TO_CITY: return HUB_TO_CITY[h]
    for k in CITYKEYS:
        if s.startswith(k + '-'): return k
    return None

# ---- place and type
TYPES = [  # (regex of the suffix, key, label)
 (r'-55-plus-homes-for-sale$', '55', '{P} 55+ homes for sale'), (r'-55-plus-condos-for-sale$', '55', '{P} 55+ condos for sale'), (r'-55-plus-townhomes-for-sale$', '55', '{P} 55+ townhomes for sale'),
 (r'-condos-townhomes-for-sale$', 'ct', '{P} condos and townhomes for sale'), (r'-condos-and-townhomes$', 'ct', '{P} condos and townhomes for sale'),
 (r'-houses-with-coach-houses-for-sale$', 'house', '{P} houses with coach houses'), (r'-houses-for-sale$', 'house', '{P} houses for sale'), (r'-houses$', 'house', '{P} houses for sale'),
 (r'-condos-under-[0-9a-z]+$', 'condo', None), (r'-condos-for-sale$', 'condo', '{P} condos for sale'), (r'-townhomes-under-[0-9a-z-]+$', 'town', None), (r'-townhomes-for-sale$', 'town', '{P} townhomes for sale'),
 (r'-duplexes-with-suites-for-sale$', 'duplex', '{P} duplexes with suites'), (r'-duplexes-for-sale$', 'duplex', '{P} duplexes for sale'),
 (r'-acreages-farms-for-sale$', 'acre', '{P} acreages and farms'), (r'-acreages-for-sale$', 'acre', '{P} acreages for sale'), (r'-lots-land$', 'land', '{P} lots and land'),
 (r'-mobile-homes-for-sale$', 'mobile', '{P} mobile homes for sale'), (r'-mobile-homes$', 'mobile', '{P} mobile homes for sale'),
 (r'-homes-(under|over)-[0-9a-z-]+$', 'home', None), (r'-homes-for-sale$', 'home', '{P} homes for sale'), (r'-guide$', 'guide', '{P} neighbourhood guide'),
]
ORDER = ['home', 'house', 'ct', 'condo', 'town', 'duplex', '55', 'acre', 'land', 'mobile', 'nc', 'base', 'guide', 'other']

def strip_city(x):
    if x in HUBS: return x
    for k in CITYKEYS:
        if x.endswith('-' + k) and x != k and x[:-len(k) - 1] not in ('fort', 'south', 'north', 'east', 'west', 'white', 'new', 'port', 'pitt', 'maple', 'mount', 'lower', 'upper'): return x[:-len(k) - 1]
    return x

def split(s):
    """-> (place key, type key, label template or None)"""
    if s in SUB_NC or (s.startswith('new-construction-') and s in exist): return strip_city(s[len('new-construction-'):]), 'nc', 'New construction in {P}'
    for rx, key, lab in TYPES:
        if re.search(rx, s): return strip_city(re.sub(rx, '', s)), key, lab
    return strip_city(s), 'base', '{P} homes for sale'

placename = {}
def pname(place):
    if place in placename: return placename[place]
    if place in HUBS: n = NAME(place)
    else:
        cands = [s for s in (place, ) if s in exist]
        n = None
        for s in cands:
            cr = crumbs(s)
            n = cr[-1]['name'] if cr else None
            if n and ('Homes for Sale' in n or '|' in n): n = re.sub(r'\s*(Homes|Houses|Real Estate)( for Sale)?.*$', '', n).strip()
        n = n or NAME(place)
    placename[place] = n
    return n

def price(x):
    m = re.fullmatch(r'(\d+)-(\d)m', x)
    if m: return f'${m.group(1)}.{m.group(2)}M'
    m = re.fullmatch(r'(\d+)m', x)
    if m: return f'${m.group(1)}M'
    m = re.fullmatch(r'(\d+)k', x)
    if m: return f'${m.group(1)}K'
    m = re.fullmatch(r'\d+', x)
    return f'${int(x):,}' if m else x

def label(s):
    place, ty, lab = split(s)
    if lab is None:
        m = re.search(r'-(homes|condos|townhomes)-(under|over)-([0-9a-z-]+)$', s)
        if m: return f"{pname(place)} {m.group(1)} {m.group(2)} {price(m.group(3))}"
        cr = crumbs(s); return cr[-1]['name'] if cr else NAME(s)
    return lab.format(P=pname(place))

def build():
    info = {s: (city_of(s),) + split(s) for s in sorted(exist)}
    pc = {}
    for s, (c, pl, ty, _) in info.items():
        if c: pc.setdefault(pl, {}).setdefault(c, 0); pc[pl][c] += 1
    for s, (c, pl, ty, lab) in list(info.items()):
        if not c and pl in pc and pl not in HUBS: info[s] = (max(pc[pl], key=pc[pl].get), pl, ty, lab)
    by_place = {}
    for s, (c, pl, ty, _) in info.items(): by_place.setdefault((c, pl), []).append(s)
    out = {}
    for s in grid:
        city, pl, ty, _ = info[s]
        if not city: continue
        seen = {s}; cols = []
        def take(slugs, cap, more_cap=0):
            vis, more = [], []
            for x in slugs:
                if x in seen: continue
                seen.add(x)
                (vis if len(vis) < cap else more).append([label(x), f'/{x}.html'])
            return vis, more[:more_cap]
        # 1 same place
        sibs = sorted([x for x in by_place.get((city, pl), []) if x != s], key=lambda x: (ORDER.index(info[x][2]) if info[x][2] in ORDER else 99, x))
        nc_self = [x for x in sibs if info[x][2] == 'nc']
        v, m = take(sibs, 10, 10)
        if v: cols.append(dict(h=f'Explore {pname(pl)} real estate', links=v, more=m))
        # 2 city searches
        csl = sorted([x for x in grid if info[x][0] == city and x not in seen and info[x][2] != 'nc' and 'open-houses' not in x], key=lambda x: (0 if info[x][1] in HUBS else 1, ORDER.index(info[x][2]) if info[x][2] in ORDER else 99, x))
        csl = [x for x in csl if info[x][2] not in ('guide',)] + [x for x in csl if info[x][2] == 'guide']
        v, m = take(csl, 8, 32)
        if v: cols.append(dict(h=f'Popular {NAME(city)} searches', links=v, more=m))
        # 3 nearby cities
        nl = []
        for n in NEAR.get(city, []):
            if n in HUBS: nl.append([f'{NAME(n)} homes for sale', f'/{HUBS[n]}.html'])
            if n in NCPAGE and NCPAGE[n] != s: nl.append([f'New construction in {NAME(n)}', f'/{NCPAGE[n]}.html'])
        nl = [x for x in nl if x[1] != f'/{s}.html']
        if nl: cols.append(dict(h='Nearby cities', links=nl[:8], more=nl[8:]))
        # 4 new construction in the city
        ncs = ([NCPAGE[city]] if city in NCPAGE else []) + sorted([x for x in grid if info[x][0] == city and info[x][2] == 'nc' and x != NCPAGE.get(city)])
        v = [[label(x) if x in SUB_NC or (x.startswith('new-construction-') and x != NCPAGE.get(city)) else f'New construction in {NAME(city)}', f'/{x}.html'] for x in ncs if x != s and f'/{x}.html' not in {l[1] for c in cols for l in c['links'] + c['more']}]
        if v: cols.append(dict(h=f'New construction in {NAME(city)}', links=v[:8], more=v[8:24]))
        if cols: out[s] = dict(cols=cols)
    return out

if __name__ == '__main__':
    out = build()
    json.dump(out, open('src/data/explore.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print(len(grid), 'listing-search pages;', len(out), 'get an explore block;', sum(len(c['links']) + len(c['more']) for v in out.values() for c in v['cols']) // max(len(out), 1), 'links on average')
