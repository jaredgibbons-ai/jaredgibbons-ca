#!/usr/bin/env python3
"""Breadcrumb trails for every page that has none in its local layer -> src/data/breadcrumbs.json {slug: [{name, href}]}.
Basis (real structure only, nothing invented):
  1. community pages and guides: Home > city hub > (community page, for a guide) > page, from src/data/snapstats/_mapping.json
  2. pages under a parent in the main navigation (src/data/nav.json): Home > parent > page
  3. everything else: Home > page
Pages whose local layer already has `breadcrumbs` are left alone. Blog posts and own listings get theirs in their templates.
    python3 -I tools/build_breadcrumbs.py"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_community_pages as C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = lambda s: f'/{s}.html'

def h1_of(d):
    for b in d.get('blocks', []):
        if b.get('t') == 'h' and b.get('level') == 1:
            return (b.get('text') or '').strip()
    return ''

pages, names = {}, {}
for f in glob.glob(f'{ROOT}/src/data/pages/*.json'):
    d = json.load(open(f)); s = d['slug']; pages[s] = d
    names[s] = h1_of(d) or re.split(r'\s*[|–-]\s*Jared', d.get('title', ''))[0].strip()
local = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f'{ROOT}/src/data/local/*.json')}
for s, l in local.items():
    if l.get('new_page'): names[s] = l['new_page'].get('h1') or names.get(s, s)
    elif s not in names: names[s] = names.get(s, '')
exist = set(pages) | {s for s, l in local.items() if l.get('new_page')}
mapping = json.load(open(f'{ROOT}/src/data/snapstats/_mapping.json'))['mapped']
prim = {(v[0], v[1]): s for s, v in mapping.items() if '+' not in str(v[1]) and not s.endswith('-guide')}

# nav parents
nav = json.load(open(f'{ROOT}/src/data/nav.json')); navpar = {}
def walk(items, parent):
    for it in items:
        h = it.get('href', '')
        m = re.match(r'^/([^/]+)\.html$', h)
        if m and parent and m.group(1) not in navpar: navpar[m.group(1)] = parent
        if it.get('children'): walk(it['children'], (m.group(1), it['label']) if m else parent)
walk(nav, None)

hubs = {k[:-len('-homes-for-sale')]: k for k in exist if k.endswith('-homes-for-sale')}
hubs['cloverdale'] = 'cloverdale-houses-for-sale'; hubs['south-surrey'] = 'south-surrey-homes-for-sale'
def title_of(s):
    return pages[s].get('title', '') if s in pages else (local.get(s, {}).get('new_page') or {}).get('title', '')
def title_city(s):
    t = title_of(s)
    if '|' not in t: return None
    cands = [t.split('|')[1]]
    hd = t.split('|')[0]
    if ',' in hd: cands.insert(0, hd.rsplit(',', 1)[1])
    for tl in cands:
        r = _tc(tl, s)
        if r: return r
    return None
def _tc(tl, s):
    tail = re.sub(r'\b(BC|Real Estate|Near|Guide|Homes for Sale|MLS|Rural|Village|Acreages|Farmland)\b|[&®]', '', tl, flags=re.I)
    tail = ' '.join(tail.split()).strip(' ,-')
    ws = tail.split()
    for n in range(len(ws), 0, -1):
        k = re.sub(r'[^a-z0-9]+', '-', ' '.join(ws[:n]).lower()).strip('-')
        if k in hubs and hubs[k] in exist and hubs[k] != s: return (k, ' '.join(ws[:n]))
    return None
def head(s):
    t = title_of(s)
    return re.sub(r'\s*(Homes|Houses|Real Estate)( for Sale)?\s*$', '', t.split('|')[0]).strip() or None

def short(s):
    n = names.get(s) or head(s) or s.replace('-', ' ').title()
    n = re.sub(r'\s*\|.*$', '', n).strip()
    return n.title() if n.isupper() else n

# Area and complex pages that none of the rules above place under their city (D-247): the city each one is in, by geography.
HUB_NAME = {'south-surrey': 'South Surrey', 'north-surrey': 'North Surrey', 'west-vancouver': 'West Vancouver', 'north-vancouver': 'North Vancouver'}
AREA_PARENT = {}
for _city, _slugs in {
    'langley': 'aldergrove-condos-for-sale aldergrove-houses-for-sale aldergrove-mobile-homes-for-sale aldergrove-townhomes-for-sale brookswood-houses-for-sale brookswood-mobile-homes-for-sale brookswood-real-estate-development-guide campbell-valley-acreages-farms-for-sale campbell-valley-houses-for-sale cheap-mobile-homes-langley-under-500k cost-of-mobile-home-pad-rental-fees-in-langley fort-langley-acreages-for-sale fort-langley-houses-for-sale murrayville-condos-for-sale murrayville-houses-for-sale murrayville-townhomes-for-sale salmon-river-acreages-farms-for-sale salmon-river-houses-for-sale walnut-grove-condos-for-sale walnut-grove-houses-for-sale walnut-grove-townhomes-for-sale willoughby-homes-for-sale city-of-langley-homes-for-sale sell-my-house-fast-in-langley-bc',
    'south-surrey': 'morgan-crossing-homes-for-sale brownstones-at-morgan-crossing enclave-at-grandview grandview-corners-condos-townhomes-for-sale grandview-heights-guide grandview-surrey-duplexes-for-sale grandview-surrey-townhomes-for-sale greenway-townhomes-south-surrey hyde-park-south-surrey jacobsen-townhomes-south-surrey soho-townhomes-south-surrey south-village-grandview-townhomes the-heights-townhomes-south-surrey luxury-homes-for-sale-in-white-rock-south-surrey pacific-douglas-duplexes-for-sale crescent-bch-ocean-pk southsurrey-foreclosures-court-ordered-sales',
    'north-surrey': 'guildford-condos-for-sale guildford-townhomes-for-sale whalley-condos-for-sale whalley-townhomes-for-sale',
    'surrey': 'port-kells-acreages-for-sale surreyforeclosuresandcourtsales',
    'cloverdale': 'cloverale-foreclosures-court-ordered-sales',
    'chilliwack': 'bridal-falls bridal-falls-guide chilliwack-downtown-guide chilliwack-mountain-guide chilliwack-proper-east-guide chilliwack-proper-west-guide chilliwackforeclosuresandcourtsales columbia-valley-guide cultus-lake cultus-lake-guide east-chilliwack east-chilliwack-guide greendale-guide majuba-hill-guide popkum popkum-guide rosedale-guide rosedale-homes-for-sale ryder-lake-guide vedder-crossing-guide vedder-mountain-guide west-chilliwack-guide yarrow-guide',
    'abbotsford': 'abbotsfordforeclosuresandcourtsales',
    'mission': 'missionforeclosuresandcourtsales',
    'maple-ridge': 'mapleridgeforeclosuresandcourtsales',
    'delta': 'east-delta-guide',
    'ladner': 'holly-guide',
    'tsawwassen': 'english-bluff tsawwassen-central-guide',
    'west-vancouver': 'british-properties cypress-park-estates',
    'north-vancouver': 'canyon-heights-nv central-lonsdale',
    'vancouver': 'downtown-ve downtown-vw',
}.items():
    for _s in _slugs.split(): AREA_PARENT[_s] = _city

out, kinds = {}, {'community': 0, 'guide': 0, 'nav': 0, 'flat': 0}
for s in sorted(exist):
    if s in ('index', '404') or local.get(s, {}).get('breadcrumbs'): continue
    home = {'name': 'Home', 'href': '/'}
    me = lambda n=None: {'name': n or short(s), 'href': H(s)}
    v = mapping.get(s)
    if v and '+' not in str(v[1]) and C.HUB.get(v[0]) in exist and C.HUB[v[0]] != s:
        ak, nm = v; city = {'name': C.CITY[ak][0] if ak in C.CITY else short(C.HUB[ak]), 'href': H(C.HUB[ak])}
        disp = C.DISPLAY.get(nm, nm)
        if s.endswith('-guide'):
            p = prim.get((ak, nm)); trail = [home, city] + ([{'name': disp, 'href': H(p)}] if p in exist and p != s else []) + [me(f'{disp} guide')]
            kinds['guide'] += 1
        else:
            trail = [home, city, me(disp)]; kinds['community'] += 1
    elif not s.endswith('-guide') and (pre := max((k for k in hubs if s.startswith(k + '-') and hubs[k] != s), key=len, default=None)):
        trail = [home, {'name': pre.replace('-', ' ').title(), 'href': H(hubs[pre])}, me()]; kinds['prefix'] = kinds.get('prefix', 0) + 1
    elif title_city(s) and not s.endswith('-for-sale'):
        k, tail = title_city(s); trail = [home, {'name': tail, 'href': H(hubs[k])}, me(re.sub(r',\s*' + re.escape(tail) + r'$', '', head(s) or short(s)))]; kinds['title'] = kinds.get('title', 0) + 1
    elif s in navpar and navpar[s][0] in exist and navpar[s][0] != s:
        trail = [home, {'name': navpar[s][1], 'href': H(navpar[s][0])}, me()]; kinds['nav'] += 1
    elif s in AREA_PARENT and hubs.get(AREA_PARENT[s]) in exist:
        k = AREA_PARENT[s]; trail = [home, {'name': HUB_NAME.get(k, k.replace('-', ' ').title()), 'href': H(hubs[k])}, me()]; kinds['area'] = kinds.get('area', 0) + 1
    else:
        trail = [home, me()]; kinds['flat'] += 1
    out[s] = trail
json.dump(out, open(f'{ROOT}/src/data/breadcrumbs.json', 'w'), ensure_ascii=False, indent=0)
print(len(out), kinds)
