#!/usr/bin/env python3
"""Sub-area new-construction pages (gen 'ncs'): one live MyRealPage search per board sub-area with 5 or more new listings.

Source worksheet: docs/review/idx/new-construction-subarea-searches-2026-11-04.xlsx (tab Counts: rows with Status 'Built'; each has a search id and a page address
/new-construction-<slug>.html). The other 200 sub-areas (under 5) are listed on tab Skipped and get no page.
Numbers come only from the repo's Paragon aggregate (src/data/sold/sold-12m.json; a median only where 5 or more sold, a name only where 3 or more) -
no MLS numbers, addresses or remarks, and no live listing counts. These pages do not replace the regular sub-area pages and link to them where one exists.
Idempotent: rewrites only its own files and its own gen blocks.   python3 -I tools/build_new_construction_subareas.py
"""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import build_new_construction as N
ROOT = N.ROOT; os.chdir(ROOT)
G = 'ncs'; LG = 'ncslinks'
XLSX = 'docs/review/idx/new-construction-subarea-searches-2026-11-04.xlsx'
SD, WINDOW, money, TN, TYPES = N.SD, N.WINDOW, N.money, N.TN, N.TYPES
W = 'November 2025 to October 2026'
N_T1 = {'house': 'house', 'townhome': 'townhome', 'condo': 'condo', 'duplex': 'duplex'}

# Board area -> (label used in text, parent page for breadcrumbs and a link)
AREA = {
 'Abbotsford': ('Abbotsford', 'abbotsford-presale-condos-and-townhomes'), 'Cloverdale': ('Cloverdale', 'new-construction-cloverdale'),
 'Langley': ('Langley', 'new-construction-presales-in-langley-bc'), 'South Surrey White Rock': ('South Surrey and White Rock', 'south-surrey-presale-condos'),
 'Surrey': ('Surrey', 'surrey-presale-condos-and-townhomes'), 'North Surrey': ('North Surrey', 'surrey-presale-condos-and-townhomes'),
 'Burnaby North': ('Burnaby North', 'burnaby-presale-condos-and-townhomes'), 'Burnaby South': ('Burnaby South', 'burnaby-presale-condos-and-townhomes'),
 'Chilliwack': ('Chilliwack', 'new-construction-chilliwack'), 'Sardis': ('Sardis', 'new-construction-sardis'),
 'Coquitlam': ('Coquitlam', 'coquitlam-presale-condos-and-townhomes'), 'Ladner': ('Ladner', 'new-construction-ladner'),
 'Maple Ridge': ('Maple Ridge', 'new-construction-maple-ridge'), 'Mission': ('Mission', 'new-construction-mission'),
 'New Westminster': ('New Westminster', 'new-construction-new-westminster'), 'North Vancouver': ('North Vancouver', 'new-construction-north-vancouver'),
 'Port Coquitlam': ('Port Coquitlam', 'new-construction-port-coquitlam'), 'Port Moody': ('Port Moody', 'new-construction-port-moody'),
 'Richmond': ('Richmond', 'new-construction-richmond'), 'Tsawwassen': ('Tsawwassen', 'new-construction-tsawwassen'),
 'Vancouver East': ('Vancouver East', 'vancouver-presale-condos-and-townhomes'), 'Vancouver West': ('Vancouver West', 'vancouver-presale-condos-and-townhomes'),
 'West Vancouver': ('West Vancouver', 'new-construction-west-vancouver'),
}
# Board sub-area names that read badly or are ambiguous on their own -> display name
DISP = {
 'Aldergrove Langley': 'Aldergrove', 'Brookswood Langley': 'Brookswood', 'Crescent Bch Ocean Pk.': 'Crescent Beach and Ocean Park', 'Grandview Surrey': 'Grandview, Surrey',
 'Central Pt Coquitlam': 'Central Port Coquitlam', 'Glenwood PQ': 'Glenwood, Port Coquitlam', 'Downtown NW': 'Downtown New Westminster', 'Downtown VW': 'Downtown Vancouver',
 'Collingwood VE': 'Collingwood, Vancouver', 'Fraser VE': 'Fraser, Vancouver', 'Killarney VE': 'Killarney, Vancouver', 'Fairview VW': 'Fairview, Vancouver',
 'University VW': 'University, Vancouver', 'Oakridge VW': 'Oakridge, Vancouver', 'West End VW': 'West End, Vancouver', 'Cottonwood MR': 'Cottonwood, Maple Ridge',
 'Thornhill MR': 'Thornhill, Maple Ridge', 'Quilchena RI': 'Quilchena, Richmond', 'Forest Glen BS': 'Forest Glen, Burnaby', 'Pemberton NV': 'Pemberton, North Vancouver',
 'Sperling-Duthie': 'Sperling-Duthie, Burnaby', 'Vancouver Heights': 'Vancouver Heights, Burnaby', 'Willingdon Heights': 'Willingdon Heights, Burnaby',
 'Maillardville': 'Maillardville, Coquitlam', 'Sapperton': 'Sapperton, New Westminster', 'Brighouse': 'Brighouse, Richmond', 'Shaughnessy': 'Shaughnessy, Vancouver',
 'South Granville': 'South Granville, Vancouver', 'Central Lonsdale': 'Central Lonsdale, North Vancouver', 'Cloverdale BC': 'Cloverdale', 'Mission BC': 'Mission',
 'Hastings': 'Hastings, Vancouver', 'Knight': 'Knight, Vancouver', 'Arbutus': 'Arbutus, Vancouver', 'Cambie': 'Cambie, Vancouver', 'South Cambie': 'South Cambie, Vancouver',
 'Kitsilano': 'Kitsilano, Vancouver', 'Grandview Woodland': 'Grandview-Woodland, Vancouver', 'Holly': 'Holly, Ladner', 'Clayton': 'Clayton, Cloverdale',
 'Albion': 'Albion, Maple Ridge', 'Silver Valley': 'Silver Valley, Maple Ridge', 'West Central': 'West Central, Maple Ridge', 'Cape Horn': 'Cape Horn, Coquitlam',
 'North Coquitlam': 'North Coquitlam', 'West Cambie': 'West Cambie, Richmond', 'Little Mountain': 'Little Mountain, Chilliwack', 'Lower Landing': 'Lower Landing, Chilliwack',
 'Sardis South': 'South Sardis', 'Vedder Crossing': 'Vedder Crossing, Chilliwack', 'Cypress Park Estates': 'Cypress Park Estates, West Vancouver', 'Parkcrest': 'Parkcrest, Burnaby',
 'Downtown VW ': 'Downtown Vancouver',
}
CITY = {'Cloverdale': 'Surrey', 'South Surrey White Rock': 'South Surrey', 'North Surrey': 'Surrey', 'Burnaby North': 'Burnaby', 'Burnaby South': 'Burnaby', 'Sardis': 'Chilliwack', 'Vancouver East': 'Vancouver', 'Vancouver West': 'Vancouver'}
def with_city(c):
    n = c['name']; city = CITY.get(c['area'], c['area'])
    return n if (',' in n or city.lower() in n.lower() or n in ('White Rock',)) else f'{n}, {city}'
SHORT = {k: re.sub(r',.*$', '', v) for k, v in DISP.items()}   # name without the place, used mid-sentence once the place is already named

def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def load():
    rows = [r for r in openpyxl.load_workbook(XLSX, read_only=True)['Counts'].iter_rows(min_row=2, values_only=True) if r[3] == 'Built']
    out = []
    for a, s, c, st, sid, addr in rows:
        out.append(dict(area=a, sub=s, count=int(c), sid=str(sid), slug=re.sub(r'\.html$', '', addr.strip().lstrip('/')), name=DISP.get(s, s)))
    return out

def regular_page(c, mp):
    """The regular sub-area page for this board sub-area (from the reviewed map), or None."""
    cands = [x.strip() for x in mp.get((c['area'], c['sub']), '').split('|') if x.strip()]
    base = slugify(re.sub(r'\.$', '', c['sub'])); alt = {slugify(c['name']), slugify(SHORT.get(c['sub'], c['sub']))}
    for sl in cands:
        if not N.exists(sl): continue
        if sl in alt or sl == base or re.sub(r'-(guide|homes-for-sale)$', '', sl) in alt | {base}:
            if not sl.endswith('-guide') and 'for-sale' not in sl: return sl
    for sl in sorted(cands, key=len):
        if N.exists(sl) and not sl.endswith('-guide') and 'for-sale' not in sl and any(sl.startswith(x) for x in alt | {base}): return sl
    return None

# ----------------------------------------------------------------------------- sentences
INTRO = [
 "The search above lists active MLS® listings in {n} where the board's age field reads 0 or less: homes finished this year, and homes listed ahead of completion. Houses, townhomes and condos are in; land and income properties are not.",
 "Every listing in the search above is active in {n} and carries an age of 0 or less in the board's records, meaning completed this year or listed before completion. Land and income properties are left out.",
 "What you see above is a live MLS® search for {n}: active houses, townhomes and condos with an age of 0 or less, so this year's completions and homes still being built.",
 "The listings above are the active new-construction listings in {n}, picked by setting the MLS® age field to 0 or less. That catches homes completed this year and homes listed before they are finished.",
 "This search shows active {n} listings that the MLS® records with an age of 0 or less: homes completed this year and homes listed before completion, across houses, townhomes and condos.",
]
LIM = N.V_LIMIT

def group_rows(key):
    v = SD['sub'][key]; out = []
    for t, tn in TYPES:
        g = v['groups'].get(t)
        if g and g.get('n', 0) >= 5 and g.get('price') and g.get('p25') and g.get('p75') and g.get('dom') is not None and g.get('ratio'):
            out.append(dict(sub='', t=t, n=g['n'], price=g['price'], p25=g['p25'], p75=g['p75'], dom=g['dom'], ratio=g['ratio'], yb=g.get('yb') or 0, beds=g.get('beds'), ppsf=g.get('ppsf'),
                            maint=g.get('maint') if g.get('maint_n', 0) >= 5 else None, over=g.get('over'), q=g.get('q'), lot=g.get('lot_sqft')))
    return out

SOLD = [
 "{n_}: {n} {type} sold at a median of {price}, with the middle half between {p25} and {p75}. The median {t1} took {dom} days to sell and closed at {ratio}% of list.",
 "{n} {type} sold in {n_} at a median of {price} (middle half {p25} to {p75}). A typical {t1} in {n_} spent {dom} days on the market and closed at {ratio}% of the asking price.",
 "In {n_}, {type} sold at a median of {price} across {n} sales, and the middle half closed between {p25} and {p75}. The median {t1} sat {dom} days and sold for {ratio}% of list.",
]
T1 = {'house': 'house', 'townhome': 'townhome', 'condo': 'condo', 'duplex': 'duplex'}

def lead(name, rows):
    if not rows: return ''
    r = max(rows, key=lambda x: x['n'])
    return f" Over {W}, the busiest home type in {name} was {TN[r['t']]}: {r['n']} sales at a median of {money(r['price'])}, and {len(rows)} {'type' if len(rows) == 1 else 'types'} had 5 or more sales."

def sold_section(name, sub_short, rows, key, vi):
    items = []
    for i, r in enumerate(rows):
        items.append(SOLD[(i + vi) % 3].format(type=TN[r['t']], t1=T1[r['t']], n_=name, n=r['n'], price=money(r['price']), p25=money(r['p25']), p75=money(r['p75']), dom=r['dom'], ratio=r['ratio']).replace('..', '.'))
    small = []
    for t, tn in TYPES:
        g = SD['sub'][key]['groups'].get(t)
        if g and 3 <= g.get('n', 0) < 5: small.append(f"{g['n']} {tn}")
    bl = [N.H(f'What sold in {name} over the past year')]
    head = ['Type', 'Sales', 'Median price', 'Lower quarter', 'Upper quarter', 'Days to sell', '% of list', 'Median year built']
    trs = [[TN[r['t']].capitalize(), str(r['n']), money(r['price']), money(r['p25']), money(r['p75']), str(r['dom']), f"{r['ratio']}%", str(r['yb'] or '—')] for r in rows]
    bl.append(N.tbl(f'Sold homes in {name}, {W}', head, trs))
    drows = []
    for r in rows:
        lot = r['lot'] if (r['lot'] and r['t'] in ('house', 'duplex')) else None
        drows.append([TN[r['t']].capitalize(), (str(r['beds']) if r['beds'] else '—'), (f"${r['ppsf']:,}" if r['ppsf'] else '—'), (f"${r['maint']:,}" if r['maint'] else '—'), (f"{lot:,}" if lot else '—'), (f"{r['over']}%" if r['over'] is not None else '—')])
    bl.append(N.tbl(f'The typical home sold in {name}', ['Type', 'Bedrooms', 'Price per sq ft', 'Strata fee a month', 'Lot size (sq ft)', 'Sold over list'], drows))
    qrows = []
    for r in rows:
        q = r.get('q') or []
        if len(q) == 4 and all(x.get('n', 0) >= 5 and x.get('price') for x in q): qrows.append([TN[r['t']].capitalize()] + [money(x['price']) for x in q])
    if qrows: bl.append(N.tbl(f'Median price by quarter in {name}', ['Type', 'November to January', 'February to April', 'May to July', 'August to October'], qrows))
    bl.append({'t': 'list', 'items': [[{'t': x}] for x in items], 'gen': G})
    if small: bl.append({'t': 'p', 'text': f"{' and '.join(small)} also sold in {name}, too few for a median to mean anything, so no price is shown for them.", 'gen': G})
    bl.append({'t': 'notice', 'text': f'Source: Paragon closed sales, {WINDOW}; medians need 5 or more sales.', 'gen': G})
    return bl

def compare_section(c, rows, vi):
    area = c['area']; label = AREA[area][0]; items = []
    sibs = [(k.split('|', 1)[1], v) for k, v in SD['sub'].items() if k.split('|', 1)[0] == area]
    for r in rows:
        peers = sorted([(s, g['price'], g['dom']) for s, v in sibs for g in [v['groups'].get(r['t'])] if g and g.get('n', 0) >= 5 and g.get('price') and g.get('dom') is not None], key=lambda x: x[1])
        k = len(peers)
        if k < 3: continue
        names = [p[0] for p in peers]; me = names.index(c['sub']); rank = k - me   # 1 = most expensive
        lo, hi = peers[0], peers[-1]; doms = [p[2] for p in peers]
        nb = []
        if me > 0: nb.append(f"{SHORT.get(peers[me-1][0], peers[me-1][0])} ({money(peers[me-1][1])}) sits just below")
        if me < k - 1: nb.append(f"{SHORT.get(peers[me+1][0], peers[me+1][0])} ({money(peers[me+1][1])}) sits just above")
        tail = (' ' + ' and '.join(nb) + '.') if nb else ''
        ordn = {1: 'highest', 2: 'second highest'}.get(rank, f'{rank}th highest' if rank > 3 else 'third highest')
        if rank == k: ordn = 'lowest'
        elif rank == k - 1: ordn = 'second lowest'
        nm = SHORT.get(c['sub'], c['sub']); tn = TN[r['t']]; t1 = N_T1[r['t']]
        if me == k - 1: A = [f"{tn.capitalize()} in {nm} have the highest median of the {k} {label} sub-areas, {money(r['price'])}, ahead of {SHORT.get(peers[me-1][0], peers[me-1][0])} at {money(peers[me-1][1])}; the lowest is {SHORT.get(lo[0], lo[0])} at {money(lo[1])}."] * 2
        elif me == 0: A = [f"{tn.capitalize()} in {nm} have the lowest median of the {k} {label} sub-areas, {money(r['price'])}, below {SHORT.get(peers[1][0], peers[1][0])} at {money(peers[1][1])}; the highest is {SHORT.get(hi[0], hi[0])} at {money(hi[1])}."] * 2
        else: A = [
         f"{tn.capitalize()} in {nm} have the {ordn} median of {k} {label} sub-areas, {money(r['price'])}. {SHORT.get(lo[0], lo[0])} is lowest at {money(lo[1])} and {SHORT.get(hi[0], hi[0])} highest at {money(hi[1])}.{tail}",
         f"Of {k} {label} sub-areas with 5 or more {t1} sales, {nm} ranks {ordn} at {money(r['price'])}; the range is {money(lo[1])} ({SHORT.get(lo[0], lo[0])}) to {money(hi[1])} ({SHORT.get(hi[0], hi[0])}).{tail}",
        ]
        items.append(A[(vi + len(items)) % 2])
    if not items: return []
    return [N.H(f"How {SHORT.get(c['sub'], c['sub'])} compares with the rest of {AREA[area][0]}"), {'t': 'list', 'items': [[{'t': x}] for x in items], 'gen': G}]

def buildings_section(name, key):
    v = SD['sub'][key]; allb = []
    for t in ('condo', 'townhome'):
        for x in (v.get('complexes') or {}).get(t, []):
            if x['n'] >= 3 and x.get('yb'): allb.append(dict(name=x['name'], t=t, n=x['n'], price=x['price'] if x['n'] >= 5 else None, dom=x.get('dom') if x['n'] >= 5 else None, yb=x['yb'], maint=x.get('maint') if x['n'] >= 5 else None, ratio=x.get('ratio') if x['n'] >= 5 else None))
    if not allb:
        return [N.P(f"No single {name} condo building or townhome complex had 3 or more resales over the past year, so none is named here.")]
    allb.sort(key=lambda x: (-x['yb'], -x['n']))
    top = allb[:8]; k = len(allb); newest = allb[0]
    bl = [N.H(f'Newest buildings in {name} that have resold')]
    bl.append(N.P(f"{k} {'building or complex' if k == 1 else 'buildings and complexes'} here had 3 or more resales in the past year. The newest is {newest['name']}, built in {newest['yb']}, with {newest['n']} resales."))
    rows = [[x['name'], TN[x['t']].capitalize(), str(x['n']), money(x['price']), str(x['yb']), (str(x['dom']) if x['dom'] is not None else '—'), (f"${x['maint']:,}" if x['maint'] else '—')] for x in top]
    bl.append(N.tbl(f'Buildings and complexes with resales, {name}, newest first', ['Building', 'Type', 'Resales', 'Median price', 'Year built', 'Median days to sell', 'Median strata fee'], rows)); bl[-1]['gen'] = G
    return bl

def newness(name, rows):
    ys = sorted([r for r in rows if r['yb']], key=lambda r: -r['yb'])
    if len(ys) < 2: return []
    a, b = ys[0], ys[-1]
    return [N.P(f"By build year, {TN[a['t']]} are the newest homes selling in {name} (median {a['yb']}) and {TN[b['t']]} the oldest (median {b['yb']}), a gap of {a['yb'] - b['yb']} years.")]

def faqs(name, rows, vi):
    f = []
    if rows:
        r = max(rows, key=lambda x: x['n'])
        f.append(dict(q=f'What have {TN[r["t"]]} in {name} sold for?', a=f"{r['n']} {TN[r['t']]} sold in {name} at a median of {money(r['price'])}, with the middle half between {money(r['p25'])} and {money(r['p75'])}.", gen=G))
        fast = min(rows, key=lambda x: x['dom']); slow = max(rows, key=lambda x: x['dom'])
        if fast is not slow:
            f.append(dict(q=f'How long do homes take to sell in {name}?', a=f"In {name}, {TN[fast['t']]} were quickest at {fast['dom']} days at a median, and {TN[slow['t']]} slowest at {slow['dom']} days.", gen=G))
        else:
            f.append(dict(q=f'How long do homes take to sell in {name}?', a=f"{TN[fast['t']].capitalize()} in {name} took {fast['dom']} days at a median to sell.", gen=G))
        ys = [x for x in rows if x['yb']]
        if ys:
            n = max(ys, key=lambda x: x['yb'])
            f.append(dict(q=f'Which homes in {name} are the newest?', a=f"Of the homes that resold in {name}, {TN[n['t']]} had the newest median build year, {n['yb']}.", gen=G))
    return f

def links(c, near, reg):
    pairs = []
    parent = AREA[c['area']][1]
    if N.exists(parent): pairs.append((f"New construction in {AREA[c['area']][0] if parent.startswith('new-construction-') else AREA[c['area']][0] + ' and presales'}", parent))
    if reg: pairs.append((f"{c['name']} homes for sale and market figures" if not reg.startswith('new-') else c['name'], reg))
    for s, nm in near: pairs.append((f'New construction in {nm}', s))
    pairs += [('Presale projects across the Fraser Valley and Metro Vancouver', 'presale-projects-fraser-valley-and-metro-vancouver'), ('How presales and new-home taxes work in BC', 'new-construction-presales-in-langley-bc'), ('GST rebate in BC', 'gst-rebate-in-bc'), ('BC condo buying rules', 'bc-condo-buying-rules')]
    return pairs

def build(cs):
    mp = {(r['board area'], r['board sub-area']): r['our pages that match (slug)'] for r in csv.DictReader(open('docs/review/idx/subarea-page-map-2026-11-04.csv'))}
    by_area = {}
    for c in cs: by_area.setdefault(c['area'], []).append(c)
    regs = {}
    for i, c in enumerate(cs):
        key = f"{c['area']}|{c['sub']}"; name = c['name']; reg = regular_page(c, mp); regs[c['slug']] = reg
        rows = group_rows(key)
        wc = with_city(c)
        title = f"New Construction in {wc} | New Homes for Sale | Jared Gibbons"
        if len(title) > 62: title = f"New Construction in {wc} | Jared Gibbons"
        if len(title) > 62: title = f"New Construction in {wc}"
        desc = f"New construction homes for sale in {wc}: live MLS® listings of new and newly built homes, plus what homes there sold for over the past year."
        h1 = f"New Construction Homes for Sale in {wc}"
        bl = [N.P(INTRO[i % 5].format(n=name) + lead(name, rows)), {'t': 'grid', 'gen': G}]
        bl += sold_section(name, SHORT.get(c['sub'], c['sub']), rows, key, i) if rows else [N.P(f"Fewer than 5 homes of any one type sold in {name} over the past year, so no median is shown for it.")]
        bl += compare_section(c, rows, i)
        bl += newness(name, rows)
        bl += buildings_section(name, key)
        near = [(x['slug'], x['name']) for x in by_area[c['area']] if x['slug'] != c['slug']][:6]
        bl.append(N.H(f'More new construction and {name} real estate', 2)); bl[-1]['pos'] = 'end'; bl[-1]['gen'] = G
        bl.append(N.list_of_links(links(c, near, reg))); bl[-1]['gen'] = G
        for b in bl: b['gen'] = G
        parent = AREA[c['area']][1]
        crumbs = [{'name': 'Home', 'href': '/'}] + ([{'name': 'New construction: ' + AREA[c['area']][0], 'href': f'/{parent}.html'}] if N.exists(parent) else [{'name': 'Presale and new construction', 'href': '/presale-projects-fraser-valley-and-metro-vancouver.html'}]) + [{'name': name, 'href': f"/{c['slug']}.html"}]
        j = dict(status='generated', slug=c['slug'], updated='2026-11-04', new_page=dict(title=title, description=desc, h1=h1), breadcrumbs=crumbs,
                 faq_heading=f'New construction in {name}: your questions answered', faq=faqs(name, rows, i), blocks=bl)
        json.dump(j, open(f"src/data/local/{c['slug']}.json", 'w'), indent=1, ensure_ascii=False)
    return regs, by_area

def inbound(cs, regs, by_area):
    """City new-construction pages and the matching regular sub-area pages link to the sub-area pages (end-of-page link lists)."""
    def patch(host, block_h, pairs, tag):
        f = f'src/data/local/{host}.json'
        if not os.path.exists(f): return 0
        raw = open(f).read(); j = json.loads(raw)
        j['blocks'] = [b for b in j['blocks'] if not (b.get('gen') == LG and b.get('_for') == tag)]
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': block_h, 'gen': LG, 'pos': 'end', '_for': tag}, {'t': 'list', 'items': [[N.lk(t, s)] for t, s in pairs], 'gen': LG, 'pos': 'end', '_for': tag}]
        ind = (len(raw.split('\n')[1]) - len(raw.split('\n')[1].lstrip())) if raw.count('\n') > 1 else 1
        json.dump(j, open(f, 'w'), indent=ind or 1, ensure_ascii='\\u' in raw); return 1
    n = 0; seen = {}
    for c in cs:   # parent (city) pages: one list per parent
        seen.setdefault(AREA[c['area']][1], []).append(c)
    for parent, lst in seen.items():
        nm = ' and '.join(sorted({AREA[x['area']][0] for x in lst}))
        n += patch(parent, f'New construction by neighbourhood in {nm}', [(f"New construction in {x['name']}", x['slug']) for x in sorted(lst, key=lambda x: x['name'])], 'ncs-parent')
    for c in cs:   # regular sub-area page: one link
        reg = regs.get(c['slug'])
        if reg and reg != AREA[c['area']][1]:
            n += patch(reg, f"New construction in {c['name']}", [(f"New construction homes for sale in {c['name']}", c['slug'])], c['slug'])
    print(n, 'inbound link blocks')

def main():
    cs = load()
    taken = [c['slug'] for c in cs if os.path.exists(f"src/data/pages/{c['slug']}.json")]
    assert not taken, taken
    regs, by_area = build(cs)
    inbound(cs, regs, by_area)
    print(len(cs), 'sub-area pages;', sum(1 for v in regs.values() if v), 'link to a regular sub-area page')

if __name__ == '__main__':
    main()
