#!/usr/bin/env python3
"""Eleven new search pages (Jared, 2026-11-06): three coach house searches and eight house, condo and townhome searches for Burnaby, Coquitlam, Richmond and Vancouver.

    surrey-houses-with-coach-houses-for-sale, cloverdale-houses-with-coach-houses-for-sale, south-surrey-houses-with-coach-houses-for-sale
    burnaby-houses-for-sale, coquitlam-houses-for-sale
    richmond-houses-for-sale, richmond-condos-for-sale, richmond-townhomes-for-sale
    vancouver-houses-for-sale, vancouver-condos-for-sale, vancouver-townhomes-for-sale

Numbers come only from files already in the repo: the Paragon closed-sales aggregate (src/data/sold/sold-12m.json), SnapStats (src/data/snapstats/2026-10.json) and the
MLS(R) Home Price Index (src/data/market/2026-09.json). Rules come from the city research notes in docs/research (only lines with a source and no open question).
The raw Paragon rows are not in the repo, so the coach house pages cannot show coach-house sales: they say what the city allows and show the detached-house market around them.
Pages are src/data/local/<slug>.json with a new_page header, status draft, and the same listings placeholder (grid) as the bedroom pages; the MyRealPage search id arrives
from docs/review/idx/new-searches-*.xlsx once Jerry has built the searches.  Idempotent.

    python3 -I tools/build_new_searches.py            pages, inbound links, SEO entries (tools/seo_final/fix_02.json)
    python3 -I tools/build_new_searches.py --xlsx     also (re)writes docs/review/idx/new-searches-2026-11-06.xlsx
"""
import datetime, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'nsrch'; LG = 'nslinks'; UPDATED = '2026-11-06'
SD = json.load(open('src/data/sold/sold-12m.json'))
_d = datetime.date.fromisoformat(SD['meta']['last'])
LAST = f'{_d.strftime("%B")} {_d.day}, {_d.year}'
WINDOW = f'November 1, 2025 to {LAST}'
MK = json.load(open('src/data/market/2026-09.json'))
EX = json.load(open('src/data/sold/sold-extras.json'))     # coach house, suite and penthouse figures (Pete's export, closed and pending sales to October 31, 2026)
EXW = EX['meta']['window']
SN = json.load(open('src/data/snapstats/2026-10.json'))['areas']
MAPPED = json.load(open('src/data/snapstats/_mapping.json'))['mapped']
QLAB = ['November 2025 to January 2026', 'February to April 2026', 'May to July 2026', f'August 1 to {LAST}']
BANDS = ['Under $600,000', '$600,000 to $799,999', '$800,000 to $999,999', '$1,000,000 to $1,199,999', '$1,200,000 to $1,499,999', '$1,500,000 to $1,799,999', '$1,800,000 and over']
PAR_SRC = f'Source: Paragon closed sales, {WINDOW}. Pending sales are not counted. Median means the middle price. A figure is shown only where at least 5 homes sold.'
HPI_NOTE = 'The benchmark is the price of a typical home in the area, not a median of sales.'
SRC_GVR = f'Source: Greater Vancouver REALTORS® MLS® Home Price Index, September 2026. {HPI_NOTE}'
SRC_FV = f'Source: Fraser Valley Real Estate Board MLS® Home Price Index, September 2026. {HPI_NOTE}'

DISP = {'Hamilton RI': 'Hamilton', 'Renfrew VE': 'Renfrew', 'Victoria VE': 'Victoria', 'West End VW': 'West End', 'Downtown VW': 'Downtown', 'Downtown VE': 'Downtown Eastside area',
        'Fraser VE': 'Fraser', 'Collingwood VE': 'Collingwood', 'Fraserview VE': 'Fraserview', 'Killarney VE': 'Killarney', 'Fairview VW': 'Fairview', 'Oakridge VW': 'Oakridge',
        'Mount Pleasant VE': 'Mount Pleasant (East)', 'Mount Pleasant VW': 'Mount Pleasant (West)', 'University VW': 'University', 'Quilchena RI': 'Quilchena', 'Riverdale RI': 'Riverdale',
        'Bridgeport RI': 'Bridgeport', 'Central BN': 'Central Burnaby', 'Simon Fraser Univer.': 'Simon Fraser University', 'Eagle Ridge CQ': 'Eagle Ridge', 'Westwood Summit CQ': 'Westwood Summit',
        'Capitol Hill BN': 'Capitol Hill', 'Forest Hills BN': 'Forest Hills', 'Westridge BN': 'Westridge', 'Edmonds BE': 'Edmonds', 'Central Park BS': 'Central Park', 'Forest Glen BS': 'Forest Glen',
        'Cloverdale BC': 'Cloverdale', 'Crescent Bch Ocean Pk.': 'Crescent Beach and Ocean Park', 'Grandview Surrey': 'Grandview', 'Sunnyside Park Surrey': 'Sunnyside Park',
        'Queen Mary Park Surrey': 'Queen Mary Park', 'Quilchena|Vancouver West': 'Quilchena (Vancouver)', 'S.W. Marine': 'South West Marine', 'Summitt View': 'Summit View'}
LINKALIAS = {'Crescent Bch Ocean Pk.': 'Crescent Beach Ocean Park', 'Cloverdale BC': 'Cloverdale', 'Sunnyside Park Surrey': 'Sunnyside Park', 'Grandview Surrey': 'Grandview',
             'Queen Mary Park Surrey': 'Queen Mary Park'}


NEW = {'surrey-houses-with-coach-houses-for-sale', 'cloverdale-houses-with-coach-houses-for-sale', 'south-surrey-houses-with-coach-houses-for-sale', 'burnaby-houses-for-sale', 'coquitlam-houses-for-sale',
       'richmond-houses-for-sale', 'richmond-condos-for-sale', 'richmond-townhomes-for-sale', 'vancouver-houses-for-sale', 'vancouver-condos-for-sale', 'vancouver-townhomes-for-sale'}
def exists(s): return s in NEW or os.path.exists(f'src/data/pages/{s}.json') or os.path.exists(f'src/data/local/{s}.json')
def money(v): return '—' if v is None else f'${v:,.0f}'
def num(v): return '—' if v is None else f'{v:,}'
def sqft(v): return '—' if not v else f'{v:,} sq ft'
def pct(x): return f'{x:.1f}%'
def nz(s): return re.sub(r'[^a-z0-9]+', '', s.lower())
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def L(items): return {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': G}
def tbl(cap, head, rows, src=None):
    b = {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'gen': G}
    if src: b['source'] = src
    return b
def lk(t, s): return {'t': t, 'h': f'/{s}.html'}
def disp(raw, board=None):
    if board and f'{raw}|{board}' in DISP: return DISP[f'{raw}|{board}']
    return DISP.get(raw) or re.sub(r'\s+(RI|VE|VW|BN|BS|BE|CQ|NW)$', '', raw)


# ------------------------------------------------------------------ data
def group(city, g): return SD['city'][city]['groups'][g]
def subrows(boards, g, minn=5, exclude=()):
    out = []
    for k, v in SD['sub'].items():
        b, n = k.split('|')
        if b not in boards or n in exclude or g not in v['groups']: continue
        e = v['groups'][g]
        if e['n'] < minn: continue
        out.append(dict(raw=n, board=b, name=disp(n, b), n=e['n'], price=e.get('price'), ppsf=e.get('ppsf'), dom=e.get('dom'), yb=e.get('yb'), lot=e.get('lot_sqft'), maint=e.get('maint'),
                        p25=e.get('p25'), p75=e.get('p75'), q=e.get('q') or [], cx=(v.get('complexes') or {}).get(g, [])))
    out.sort(key=lambda r: -r['n'])
    return out
def total(boards, g, exclude=()): return sum(r['n'] for r in subrows(boards, g, 0, exclude))
def priced(rows, minn=10): return sorted([r for r in rows if r['n'] >= minn and r['price']], key=lambda r: r['price'])
def qsum(boards, g):
    s = [0, 0, 0, 0]
    for r in subrows(boards, g, 0):
        for i, x in enumerate(r['q'][:4]): s[i] += x['n']
    return s
def snap(area, kind='detached'):
    a = SN[area][kind]; sm = a['summary']
    return dict(inv=sm['Inventory']['cur'], sold=sm['Solds']['cur'], price=sm['Sale Price']['cur'], dom=sm['Days on Market']['cur'], ratio=a['total']['ratio'], ll=sm['Sale to List Price Ratio']['cur'], comms=a['communities'])
def hpi(src, area, typ): return MK[src]['hpi'][area][typ]
def hpi_table(cap, rows, src, srcnote):
    head = ['Area', 'Benchmark price', '1 month', '3 months', '1 year', '3 years', '5 years']
    rr = [[lab, money(e['benchmark']), pct(e['chg_1m']), pct(e['chg_3m']), pct(e['chg_1y']), pct(e['chg_3y']), pct(e['chg_5y'])] for lab, e in rows]
    return tbl(cap, head, rr, srcnote)

_hubs = {}
def hubmap(hub):
    if hub not in _hubs:
        m = {}
        f = f'src/data/local/{hub}.json'
        if os.path.exists(f):
            for b in json.load(open(f))['blocks']:
                if b.get('t') == 'table':
                    for r in b['rows']:
                        if isinstance(r[0], dict) and r[0].get('h'): m[nz(r[0]['t'])] = r[0]['h']
        _hubs[hub] = m
    return _hubs[hub]
_snapmap = None
def snaplink(area, raw):
    global _snapmap
    if _snapmap is None:
        _snapmap = {}
        for s, (c, n) in MAPPED.items():
            if not isinstance(n, str) or '+' in n or not exists(s): continue
            k = (c, nz(n))
            if k not in _snapmap or (_snapmap[k].endswith('-guide') and not s.endswith('-guide')): _snapmap[k] = s
    s = _snapmap.get((area, nz(LINKALIAS.get(raw, raw))))
    return f'/{s}.html' if s else None
def cell(name, href): return {'t': name, 'h': href} if href else name


# ------------------------------------------------------------------ shared tables
def measures(cap, e, noun, extra=None):
    rows = [['Sales', num(e['n'])], ['Median price', money(e['price'])]]
    if e.get('p25'): rows.append(['Middle half of prices', f"{money(e['p25'])} to {money(e['p75'])}"])
    if e.get('ppsf'): rows.append(['Price per square foot', money(e['ppsf'])])
    rows.append(['Days to sell', str(e['dom'])])
    if e.get('ratio'): rows.append(['Sold price as a share of list price', f"{e['ratio']}%"])
    rows.append(['Sales over the list price', f"{e['over']}%"])
    if e.get('lot_sqft'): rows.append(['Median lot size', sqft(e['lot_sqft'])])
    if e.get('yb'): rows.append(['Median year built', str(e['yb'])])
    if e.get('beds'): rows.append(['Median bedrooms', str(e['beds'])])
    if e.get('maint'): rows.append(['Strata fee a month', money(e['maint'])])
    rows += extra or []
    return tbl(cap, ['Measure', noun], rows, PAR_SRC)
def quarters(cap, e):
    q = e.get('q') or []
    rr = [[QLAB[i], num(x['n']), money(x['price'])] for i, x in enumerate(q) if x['n']]
    return tbl(cap, ['Period', 'Sales', 'Median price'], rr, PAR_SRC)
def qcounts(cap, qs):
    return tbl(cap, ['Period', 'Sales'], [[QLAB[i], num(x)] for i, x in enumerate(qs)], f'Source: Paragon closed sales, {WINDOW}. Each period adds up the sales in every neighbourhood.')
def bands(cap, e, noun):
    br = [[BANDS[j], num(x), f'{100 * x / e["n"]:.0f}%'] for j, x in enumerate(e.get('bands') or []) if x]
    return tbl(cap, ['Price range', noun, 'Share'], br, PAR_SRC)
def subtable(cap, rows, hub=None, snapcity=None, strata=False, lim=14, lotcol=True):
    head = ['Neighbourhood', 'Sales', 'Median price', 'Price per sq ft'] + ([] if strata else (['Median lot size'] if lotcol else [])) + ['Median year built'] + (['Strata fee a month'] if strata else []) + ['Days to sell']
    out = []
    for r in rows[:lim]:
        href = hubmap(hub).get(nz(r['name'])) if hub else snaplink(snapcity, r['raw'])
        row = [cell(r['name'], href), str(r['n']), money(r['price']), money(r['ppsf'])]
        if not strata and lotcol: row.append(sqft(r['lot']))
        row.append(str(r['yb']) if r['yb'] else '—')
        if strata: row.append(money(r['maint']))
        row.append(str(r['dom']) if r['dom'] is not None else '—')
        out.append(row)
    return tbl(cap, head, out, PAR_SRC)
def buildings(cap, boards, g, hub=None, lim=10):
    allc = []
    for r in subrows(boards, g, 0):
        for c in r['cx']:
            if c['n'] >= 5: allc.append((c, r['name']))
    allc.sort(key=lambda x: -x[0]['n'])
    rows = [[c['name'], area, str(c['n']), money(c['price']) if c['n'] >= 5 else '—', str(c['yb']) if c.get('yb') else '—', money(c['maint']) if c['n'] >= 5 and c.get('maint') else '—'] for c, area in allc[:lim]]
    return tbl(cap, ['Building', 'Neighbourhood', 'Sales', 'Median price', 'Year built', 'Strata fee a month'], rows, PAR_SRC + ' A building appears here only with 5 or more sales.'), allc


def finish(slug, seo, crumbs, faq, bl, faq_heading, links, extra=None):
    pairs = [(t, s) for t, s in links if exists(s)]
    bl = bl + [{'t': 'h', 'level': 2, 'text': seo['links_h'], 'gen': G, 'pos': 'end'}, {'t': 'list', 'items': [[lk(t, s)] for t, s in pairs], 'gen': G, 'pos': 'end'}]
    j = dict(status='draft', slug=slug, updated=UPDATED, new_page=dict(title=seo['title'], description=seo['description'], h1=seo['h1']),
             breadcrumbs=[{'name': 'Home', 'href': '/index.html'}] + [{'name': n, 'href': f'/{s}.html'} for n, s in crumbs] + [{'name': seo['crumb'], 'href': f'/{slug}.html'}],
             faq_heading=faq_heading, faq=[dict(q=q, a=a, gen=G) for q, a in faq], blocks=bl)
    if extra: j.update(extra)
    json.dump(j, open(f'src/data/local/{slug}.json', 'w'), indent=1, ensure_ascii=False)
    return j


NOTICE_COACH = ('Draft for Jared’s approval. Coach house figures come from the Carriage/Coach House and Laneway House style flags in Paragon closed and pending sales, which the listing agent fills in, so the counts are small and will miss some. '
                'The live search is not connected yet.')


def coach_part(city, name):
    """Paragraph, table and FAQ answer built from the coach house flags in the extras layer."""
    g = EX['city'][city]['groups']; co, ho, la = g['coach'], g['house'], g['lane']
    assert co['n'] >= 5 and ho['n'] >= 30
    prem = 100 * (co['price'] - ho['price']) / ho['price']
    side = f'above' if co['price'] >= ho['price'] else 'below'
    para = (f'Paragon marks {co["n"]} of the {ho["n"]} {name} detached houses that sold from {EXW} as a coach house or laneway house. They sold at a median of {money(co["price"])}, '
            f'{abs(prem):.0f}% {side} the {money(ho["price"])} median for all {name} houses in the same months. The flag is typed in by the listing agent, so treat the count as a floor and not a census.' + (f' With only {co["n"]} sales the price gap is a rough sign, not a trend.' if co['n'] < 15 else ''))
    rows = [['Sales', num(co['n']), num(la['n']), num(ho['n'])], ['Median price', money(co['price']), money(la['price']), money(ho['price'])],
            ['Days to sell', str(co['dom']), str(la['dom']), str(ho['dom'])]]
    if co.get('ratio') and la.get('ratio') and ho.get('ratio'): rows.append(['Sold price as a share of list price', f'{co["ratio"]}%', f'{la["ratio"]}%', f'{ho["ratio"]}%'])
    if co.get('lot_sqft') and la.get('lot_sqft') and ho.get('lot_sqft'): rows.append(['Median lot size', sqft(co['lot_sqft']), sqft(la['lot_sqft']), sqft(ho['lot_sqft'])])
    if co.get('yb') and la.get('yb') and ho.get('yb'): rows.append(['Median year built', str(co['yb']), str(la['yb']), str(ho['yb'])])
    t = tbl(f'{name} detached houses sold with a coach house or laneway house flag', ['Measure', 'Coach or laneway house', 'Lane access', 'All detached houses'], rows,
            f'Source: Paragon closed and pending sales, {EXW}. A pending sale is firm but has not completed, so its price can still change. Lane access is the Site Influences field. A figure is shown only where at least 5 homes sold.')
    faq = (f'About {abs(prem):.0f}% {side} the all-house median. {co["n"]} {name} houses marked as a coach or laneway house sold from {EXW} at a median of {money(co["price"])}, against {money(ho["price"])} for all {name} detached houses. '
           f'The flag is entered by the listing agent, so the true number is higher.' + (f' With only {co["n"]} sales the gap is a rough sign, not a trend.' if co['n'] < 15 else ''))
    return para, t, faq


# ================================================================== COACH HOUSES
def surrey_coach():
    slug = 'surrey-houses-with-coach-houses-for-sale'
    c = group('surrey', 'house'); boards = ['Surrey', 'North Surrey']
    rows = subrows(boards, 'house'); tot = total(boards, 'house')
    hl = priced(rows); hi, lo = hl[-1], hl[0]
    small = min([r for r in rows if r['lot'] and r['n'] >= 20], key=lambda r: r['lot'])
    big = max([r for r in rows if r['lot'] and r['n'] >= 20], key=lambda r: r['lot'])
    sn = snap('surrey')
    seo = dict(title='Surrey Houses with Coach Houses for Sale | Size Rules', h1='Houses with Coach Houses for Sale in Surrey', crumb='Houses with coach houses',
               description='Search Surrey houses with a coach house, then check the 35 to 75 m² size limit, lane and parking rules, and what Fleetwood and Newton houses sold for.',
               links_h='More Surrey houses, suites and coach house searches')
    bl = [{'t': 'notice', 'text': NOTICE_COACH, 'gen': G},
          P('This search lists detached houses for sale in Surrey and North Surrey that come with a coach house: a second, smaller home on the same lot, usually built over a garage at the back. '
            'It runs from Fleetwood and Newton across to Guildford and Fraser Heights. Cloverdale and South Surrey have their own coach house searches, linked at the bottom.'),
          P(coach_part('surrey', 'Surrey and North Surrey')[0] + f' Across the whole City of Surrey the median detached house price was {money(c["price"])} in the year to {LAST}.'),
          {'t': 'grid', 'gen': G},
          H('What Surrey allows for a coach house'),
          P('Surrey puts coach houses and garden suites under one rule. Each has to be at least 35 and at most 75 square metres, and any residential zone that allows detached houses, duplexes or houseplexes also allows one.'),
          P('The cap rises to 120 square metres on lots zoned RA, R2, R2-O or R3, but only where the existing house or duplex is below its maximum floor area ratio. A coach house on a smaller R3 to R6 lot needs lane access, and the lot must have one extra parking space.'),
          P('A secondary suite cannot go inside a coach house or garden suite. Surrey allows one suite per single-family, semi-detached or duplex unit, at most 40% of the main unit’s habitable floor area, and a suite cannot be sold as its own strata lot.'),
          P('On July 8, 2024 Surrey folded 20 single-family and duplex zones into nine small-scale zones, and the old codes such as RF-12C and RF-13 went with them. A listing or a seller who quotes an old zone name is working from an out-of-date map.'),
          H('When a lot could hold more than a coach house'),
          P('The same July 2024 changes let a lot take 3 units when it is under 280 square metres and 4 when it is larger, and up to 6 on an eligible lot of at least 281 square metres within 400 metres of a frequent bus stop. '
            'They reach more than 72,000 lots under 4,050 square metres inside the urban containment boundary. A buyer who wants a houseplex rather than a single coach house should price both routes before choosing the lot.'),
          H('Surrey and North Surrey neighbourhoods: lot size comes first'),
          P(f'A coach house needs room behind or beside the main house, and on smaller lots a lane, so I read the lot size before the price. Among neighbourhoods with 20 or more house sales, {small["name"]} has the smallest median lot at {sqft(small["lot"])} '
            f'and {big["name"]} the largest at {sqft(big["lot"])}. {hi["name"]} is the dearest at a {money(hi["price"])} median and {lo["name"]} the cheapest at {money(lo["price"])}.'),
          subtable('Detached houses sold in the Surrey and North Surrey board areas, by neighbourhood', rows, snapcity='surrey'),
          P('A City planning report on a West Newton application describes the lots across 128 Street as small single-family lots with coach houses and a lane. '
            'That is a useful picture of the pattern: narrow lots, a lane behind, and a second home over the garage.'),
          P('About one-third of Surrey is designated Agriculture in the Official Community Plan, and 95% of that land is inside the Agricultural Land Reserve. The small-scale rules above are for urban lots, not a route to extra homes on Reserve land. '
            'Bridgeview sits behind dikes. Confirm Reserve and floodplain status before you count on a second home.'),
          coach_part('surrey', 'Surrey and North Surrey')[1],
          H('Detached houses in the City of Surrey: what sold'),
          measures('Detached houses sold in the City of Surrey (including Cloverdale and South Surrey)', c, 'Detached houses'),
          P(f'In the City of Surrey houses took {c["dom"]} days to sell at a median and closed at {c["ratio"]}% of the list price, and {c["over"]}% sold over it. The year-built median is {c["yb"]}, so a typical Surrey house is older than a lot of buyers expect before they start adding a second home.'),
          quarters('Detached houses sold in the City of Surrey, by period', c),
          hpi_table('Detached benchmark price, Surrey and North Surrey', [('Surrey', hpi('fvreb', 'Surrey', 'detached')), ('North Surrey', hpi('fvreb', 'North Surrey', 'detached'))], 'fvreb', SRC_FV),
          P(f'The October 2026 monthly report counts {sn["inv"]:,} detached houses for sale in Surrey and {sn["sold"]} sold in the month, a sales ratio of {sn["ratio"]}%, with a median of {money(sn["price"])} after {sn["dom"]} days.'),
          H('Costs that come with a second home'),
          P('Surrey’s 2026 residential property tax rate is $3.42731 per $1,000 of assessed value. A legal secondary suite in the main house adds $454.00 for water and $821.71 for sewer in 2026, $1,275.71 in all, plus $172.04 for garbage. '
            'Flat-rate utilities for a house without a suite are $1,195 for water and $1,661 for sewer, and $344.08 for waste.'),
          H('Before you make an offer on a house with a coach house'),
          L(['Ask for the building permit and the final inspection for the coach house itself, not just for the garage under it.',
             'Measure it against the 35 to 75 square metre range, or the 120 square metre range if the lot is RA, R2, R2-O or R3.',
             'Check where the second home is reached from. A coach house on a smaller R3 to R6 lot is a lane-access building.',
             'Count the parking. The rule asks for one extra space for the coach house.',
             'Ask the City whether any suite in the main house is registered. Surrey says its 2024 changes do not make an unpermitted suite legal after the fact.']),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a Surrey house', 'gen': G}, P(f'The calculator starts at the City of Surrey median of {money(c["price"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': c['price'], 'gen': G}]
    faq = [('How big can a coach house be in Surrey?', 'Between 35 and 75 square metres. On lots zoned RA, R2, R2-O or R3 it can reach 120 square metres where the existing house or duplex is below its maximum floor area ratio.'),
           ('Can a Surrey coach house have a secondary suite in it?', 'No. Surrey does not allow a secondary suite inside a coach house or garden suite. A suite is allowed in the main house, one per unit, up to 40% of the principal unit’s habitable floor area.'),
           ('Does a Surrey lot need a lane for a coach house?', 'On smaller R3 to R6 lots, yes: the rules require lane access for a coach house. The lot also needs one extra parking space.'),
           ('How much does a Surrey house with a coach house cost?', coach_part('surrey', 'Surrey and North Surrey')[2] + f' Across all of Surrey the median was {money(c["price"])} in the year to {LAST}.'),
           ('Is a coach house the same as a garden suite in Surrey?', 'Surrey’s rule covers both in one sentence: a coach house or garden suite is 35 to 75 square metres, allowed in any zone that allows detached houses, duplexes or houseplexes.'),
           ('Do these rules apply in White Rock, Langley or Delta?', 'No. They are Surrey’s. White Rock, the Township of Langley, the City of Langley and Delta each have their own bylaws, so confirm the city before you read a listing.')]
    links = [('Surrey houses for sale', 'surrey-houses-for-sale'), ('Surrey homes for sale', 'surrey-homes-for-sale'), ('Surrey half duplexes for sale', 'surrey-duplexes-for-sale'),
             ('South Surrey duplexes with suites', 'south-surrey-duplexes-with-suites-for-sale'), ('Cloverdale houses with coach houses', 'cloverdale-houses-with-coach-houses-for-sale'),
             ('South Surrey houses with coach houses', 'south-surrey-houses-with-coach-houses-for-sale'), ('Langley houses with coach houses', 'langley-houses-with-coach-houses-for-sale'),
             ('Surrey neighbourhood guides', 'surrey-neighbourhood-guides'), ('Sell my house in Surrey', 'sell-my-house-in-surrey'), ('Surrey market stats', 'surrey-real-estate-market-stats'),
             ('Homes with multiplex potential', 'homes-with-multiplex-potential-fraser-valley'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'),
             ('Schools in Surrey', 'schools-in-surrey-bc'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Surrey houses', 'surrey-houses-for-sale')], faq, bl, 'Surrey coach houses: your questions answered', links, dict(search_page=dict(kind='coach', city='surrey')))


def cloverdale_coach():
    slug = 'cloverdale-houses-with-coach-houses-for-sale'
    c = group('cloverdale', 'house'); boards = ['Cloverdale']
    rows = subrows(boards, 'house'); cl, cy = rows[0], rows[1]
    assert cl['raw'] == 'Cloverdale BC' and cy['raw'] == 'Clayton'
    sn = snap('cloverdale'); h = hpi('fvreb', 'Cloverdale', 'detached')
    q = c['q']; bd = c['bands']
    seo = dict(title='Cloverdale Houses with Coach Houses for Sale | Prices', h1='Houses with Coach Houses for Sale in Cloverdale', crumb='Houses with coach houses',
               description='Cloverdale and Clayton houses with a coach house for sale, with Surrey’s 35 to 75 m² limit, the R4 zone that replaced RF-12C, and what houses sold for.',
               links_h='More Cloverdale houses and coach house searches')
    assert sn['comms'][0]['name'] == 'Clayton' and sn['comms'][1]['name'] == 'Cloverdale'
    bl = [{'t': 'notice', 'text': NOTICE_COACH, 'gen': G},
          P('These are detached houses for sale in Cloverdale and Clayton with a coach house on the lot. The two parts of this search look very different from each other: Cloverdale town has older and larger lots, and Clayton is the newer small-lot neighbourhood.'),
          P(coach_part('cloverdale', 'Cloverdale')[0] + f' Over the year to {LAST} all {c["n"]} Cloverdale and Clayton houses in the main sold file had a median of {money(c["price"])}, about {money(h["benchmark"])} on the Home Price Index benchmark, and {c["dom"]} days was the median wait.'),
          {'t': 'grid', 'gen': G},
          H('Clayton and Cloverdale are two different lots'),
          P(f'Clayton’s houses that sold had a median lot of just {sqft(cy["lot"])}, built around {cy["yb"]}, and a median price of {money(cy["price"])}. In Cloverdale town the median lot was {sqft(cl["lot"])}, the median house was built in {cl["yb"]} and the median price was {money(cl["price"])}. '
            f'A Clayton lot is {100 * cy["lot"] / cl["lot"]:.0f}% the size of a typical lot in town, so a coach house there has to be planned in from the first day: the second home takes the place of a back yard.'),
          subtable('Detached houses sold in Cloverdale, by neighbourhood', rows, snapcity='cloverdale'),
          H('The zone names changed in 2024'),
          P('Older Cloverdale listings can still talk about RF-12C or RF-13 coach-home zoning. Those names are gone. Surrey’s July 8, 2024 changes replaced RF-12, RF-12C and RF-13 with the R4 Small Lot Residential zone, and RF-SD became R6 Semi-Detached. '
            'Read the lot’s current zone in Zoning By-law No. 12000 before anyone quotes you coach house potential.'),
          P('What a coach house can be today is set city-wide. It has to be between 35 and 75 square metres, up to 120 on RA, R2, R2-O and R3 lots below their maximum floor area ratio, with lane access for a coach house on smaller lots and one added parking space. '
            'A suite cannot sit inside a coach house or garden suite.'),
          H('Town centre and farmland edges'),
          P('Cloverdale’s town centre has its own plan. The Cloverdale Town Centre Plan was approved on November 18, 2019 and an update was authorized in October 2023, so the plan map for the exact address is worth checking, and the City’s heritage inventory is the first check for an older house near the main street.'),
          P('Cloverdale also has working farmland. Surrey’s small-scale housing rules are for urban lots; they are not a way to add a second home on a parcel in the Agricultural Land Reserve, where the Agricultural Land Commission sets what extra housing is allowed. '
            'Farm and acreage lots are covered in the buying rules for acreage on this site.'),
          P('Two big projects are worth knowing about. The new Surrey Hospital and BC Cancer Centre at 5500 180 Street started construction in September 2023, with completion expected in 2030, and the Surrey-Langley SkyTrain, 16 kilometres long with a station at Clayton, is under construction and expected in late 2029.'),
          coach_part('cloverdale', 'Cloverdale')[1],
          H('Cloverdale houses: what sold'),
          measures('Detached houses sold in Cloverdale', c, 'Cloverdale houses'),
          quarters('Cloverdale houses sold, by period', c),
          P(f'The median price slipped from {money(q[0]["price"])} in the first period to {money(q[3]["price"])} in the latest one, which covers sales only to {LAST}. The most common price range was $1,200,000 to $1,499,999 with {bd[4]} sales, then $1,000,000 to $1,199,999 with {bd[3]}.'),
          bands('Cloverdale houses sold, by price range', c, 'Sales'),
          hpi_table('Detached benchmark price, Cloverdale', [('Cloverdale', h)], 'fvreb', SRC_FV),
          P(f'In October 2026 the monthly report counted {sn["inv"]} detached houses for sale in Cloverdale and {sn["sold"]} sold, a sales ratio of {sn["ratio"]}%. The median was {money(sn["price"])} and houses took {sn["dom"]} days. '
            f'Clayton had {sn["comms"][0]["inventory"]} for sale and {sn["comms"][0]["sales"]} sold, Cloverdale town {sn["comms"][1]["inventory"]} and {sn["comms"][1]["sales"]}.'),
          H('Before you make an offer'),
          L(['Find the coach house’s own permit and final inspection. A garage with a loft is not a coach house.',
             'Check the lot’s current zone, and ask what the old RF-12C or RF-13 label on the listing means for this lot now.',
             'Confirm lane access and where the second home’s parking goes.',
             'For a lot at the farm edge, look up Agricultural Land Reserve status first.']),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a Cloverdale house', 'gen': G}, P(f'The calculator starts at the Cloverdale median of {money(c["price"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': c['price'], 'gen': G}]
    faq = [('Are RF-12C and RF-13 still zones in Cloverdale?', 'No. Surrey replaced RF-12, RF-12C and RF-13 with the R4 Small Lot Residential zone on July 8, 2024. A listing that still uses the old names is out of date, so check the lot’s current zone.'),
           ('How big can a Cloverdale coach house be?', 'Between 35 and 75 square metres. The limit is 120 on RA, R2, R2-O and R3 lots where the existing house is below its maximum floor area ratio.'),
           ('How much does a Cloverdale house with a coach house cost?', coach_part('cloverdale', 'Cloverdale')[2]),
           ('What do Cloverdale houses sell for?', f'The median was {money(c["price"])} over the year to {LAST}, from {c["n"]} sales. Clayton houses had a median of {money(cy["price"])} and Cloverdale town houses {money(cl["price"])}.'),
           ('Can I add a coach house to a farm lot near Cloverdale?', 'Not under Surrey’s small-scale rules. Those cover urban lots. A parcel in the Agricultural Land Reserve is governed by the Agricultural Land Commission, so check the Reserve first.'),
           ('How fast do Cloverdale houses sell?', f'The median was {c["dom"]} days, and homes closed at {c["ratio"]}% of list price at a median. {c["over"]}% sold over the list price.'),
           ('Which Cloverdale area has the smallest lots?', f'Clayton, at a median lot of {sqft(cy["lot"])} against {sqft(cl["lot"])} in Cloverdale town.')]
    links = [('Cloverdale houses for sale', 'cloverdale-houses-for-sale'), ('Cloverdale homes under $1.8 million', 'cloverdale-homes-under-1-8m'), ('Cloverdale half duplexes', 'cloverdale-duplexes-for-sale'),
             ('Cloverdale acreages', 'cloverdale-acreages-for-sale'), ('Cloverdale neighbourhood guides', 'cloverdale-neighbourhood-guides'), ('Cloverdale real estate guide', 'cloverdale-bc'),
             ('Surrey houses with coach houses', 'surrey-houses-with-coach-houses-for-sale'), ('South Surrey houses with coach houses', 'south-surrey-houses-with-coach-houses-for-sale'),
             ('Langley houses with coach houses', 'langley-houses-with-coach-houses-for-sale'), ('Sell my house in Surrey and Cloverdale', 'sell-my-house-in-surrey'),
             ('Cloverdale market stats', 'cloverdale-real-estate-market-stats'), ('BC acreage buying rules', 'bc-acreage-buying-rules'), ('New construction in Cloverdale', 'new-construction-cloverdale'),
             ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Cloverdale houses', 'cloverdale-houses-for-sale')], faq, bl, 'Cloverdale coach houses: your questions answered', links, dict(search_page=dict(kind='coach', city='cloverdale')))


def n_sales(e): return f'{e["n"]} sales'


def south_surrey_coach():
    slug = 'south-surrey-houses-with-coach-houses-for-sale'
    c = group('south-surrey', 'house'); boards = ['South Surrey White Rock']
    rows = subrows(boards, 'house', exclude=('White Rock',)); wr = [r for r in subrows(boards, 'house') if r['raw'] == 'White Rock'][0]
    sn = snap('south-surrey-white-rock'); h = hpi('fvreb', 'South Surrey & White Rock', 'detached')
    by = {r['raw']: r for r in rows}
    ec, gr, pdg, cb = by['Elgin Chantrell'], by['Grandview Surrey'], by['Pacific Douglas'], by['Crescent Bch Ocean Pk.']
    q = c['q']; bd = c['bands']
    seo = dict(title='South Surrey Houses with Coach Houses for Sale | Rules', h1='Houses with Coach Houses for Sale in South Surrey', crumb='Houses with coach houses',
               description='South Surrey houses with a coach house for sale. See Surrey’s size and lane rules, the Crescent Beach flood level, and sold prices in Grandview and Elgin.',
               links_h='More South Surrey houses, suites and coach house searches')
    bl = [{'t': 'notice', 'text': NOTICE_COACH, 'gen': G},
          P('This search lists detached houses for sale in South Surrey with a coach house on the lot. It covers Crescent Beach and Ocean Park, Elgin Chantrell, Grandview, King George Corridor, Morgan Creek, Pacific Douglas, Sunnyside Park and Hazelmere. '
            'White Rock is a separate city with its own bylaws and is not part of this search.'),
          P(coach_part('south-surrey', 'South Surrey')[0] + f' South Surrey as a whole is the market around it: its median is {money(c["price"])} in the year to {LAST}, which is {money(c["price"] - group("surrey", "house")["price"])} above the City of Surrey median.'),
          {'t': 'grid', 'gen': G},
          H('Surrey’s rules, as they apply in South Surrey'),
          P('South Surrey is part of the City of Surrey, so one set of coach house rules covers it. A coach house or garden suite is between 35 and 75 square metres. Any residential zone that allows a detached house, a duplex or a houseplex also allows one. '
            'Smaller R3 to R6 lots need lane access for a coach house, and the lot has to carry one extra parking space.'),
          P('Lots zoned RA, R2, R2-O or R3 get more room: up to 120 square metres where the existing house is below its maximum floor area ratio. Elgin Chantrell has the largest lots in South Surrey, with a median house lot of '
            f'{sqft(ec["lot"])}, so check each lot’s zone before assuming its limit.'),
          P('The one-suite-per-unit rule still applies. A secondary suite is allowed in the main house, capped at 40% of its habitable floor area, and not inside the coach house.'),
          H('Crescent Beach is its own case'),
          P('Crescent Beach has a flood construction level of 3.30 metres above Geodetic Survey of Canada datum. Building below it needs a Development Variance Permit, floodplain construction calls for a geotechnical engineer, '
            'and most Crescent Beach properties cannot connect to the City storm sewer. A second home on a Crescent Beach lot is a different project from one in Sunnyside Park.'),
          H('South Surrey neighbourhoods: where lots are small and where they are large'),
          P(f'The median lot of a house that sold in Grandview was {sqft(gr["lot"])} and in Pacific Douglas {sqft(pdg["lot"])}, both newer neighbourhoods (median built {gr["yb"]} and {pdg["yb"]}). '
            f'Elgin Chantrell sits at the other end with {sqft(ec["lot"])} and a {money(ec["price"])} median price, the highest of any South Surrey neighbourhood. Crescent Beach and Ocean Park had the most sales, {cb["n"]}, at {money(cb["price"])}.'),
          subtable('Detached houses sold in South Surrey, by neighbourhood', rows, snapcity='south-surrey-white-rock'),
          P(f'For contrast, White Rock’s {wr["n"]} house sales had a median price of {money(wr["price"])} on a median lot of {sqft(wr["lot"])}. Its coach house rules are the City of White Rock’s and I have not covered them on this page.'),
          coach_part('south-surrey', 'South Surrey')[1],
          H('South Surrey houses: what sold'),
          measures('Detached houses sold in South Surrey', c, 'South Surrey houses'),
          quarters('South Surrey houses sold, by period', c),
          P(f'The median fell from {money(q[0]["price"])} in November to January to {money(q[3]["price"])} in the latest period (to {LAST}). {bd[6]} of the {c["n"]} sales, or {100 * bd[6] / c["n"]:.0f}%, were $1,800,000 or more, and {bd[4]} fell between $1,200,000 and $1,499,999.'),
          hpi_table('Detached benchmark price, South Surrey and White Rock', [('South Surrey and White Rock', h)], 'fvreb', SRC_FV),
          P(f'The October 2026 report counted {sn["inv"]} detached houses for sale across South Surrey and White Rock and {sn["sold"]} sold, a sales ratio of {sn["ratio"]}%. Houses took {sn["dom"]} days at a median.'),
          H('What to ask on a South Surrey listing'),
          L(['Which city is the lot in? A White Rock address follows White Rock’s bylaws, not Surrey’s.',
             'Does the coach house have its own permit and final inspection, and is it the size the listing says?',
             'For Crescent Beach, ask for the flood construction level and the geotechnical report on the house.',
             'If the lot is an acreage, ask whether it is inside the Agricultural Land Reserve.']),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a South Surrey house', 'gen': G}, P(f'The calculator starts at the South Surrey median of {money(c["price"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': c['price'], 'gen': G}]
    faq = [('Do Surrey’s coach house rules apply in White Rock?', 'No. White Rock is its own city. Surrey’s limits, 35 to 75 square metres and lane access on smaller lots, apply to South Surrey, Crescent Beach and Ocean Park, Elgin Chantrell, Grandview and the other Surrey neighbourhoods.'),
           ('Can I build a coach house in Crescent Beach?', 'Possibly, but the lot is in a floodplain. The flood construction level is 3.30 metres above Geodetic Survey of Canada datum, a floodplain build needs a geotechnical engineer, and building below that level needs a Development Variance Permit.'),
           ('How much do South Surrey houses with a coach house cost?', coach_part('south-surrey', 'South Surrey')[2] + f' The median for all South Surrey detached houses was {money(c["price"])} in the year to {LAST}, with the middle half between {money(c["p25"])} and {money(c["p75"])}.'),
           ('Which South Surrey area has the biggest lots?', f'Elgin Chantrell, with a median lot of {sqft(ec["lot"])}. Grandview and Pacific Douglas are the smallest at {sqft(gr["lot"])} and {sqft(pdg["lot"])}.'),
           ('How long do South Surrey houses take to sell?', f'{c["dom"]} days at a median, and houses closed at {c["ratio"]}% of list price. {c["over"]}% sold over the list price.'),
           ('Can a South Surrey duplex have a suite as well?', 'Yes, one suite per half of a duplex, up to 40% of that unit’s habitable floor area. I list them on the South Surrey duplexes with suites page.')]
    links = [('South Surrey houses for sale', 'south-surrey-houses-for-sale'), ('South Surrey homes for sale', 'south-surrey-homes-for-sale'), ('South Surrey duplexes with suites', 'south-surrey-duplexes-with-suites-for-sale'),
             ('South Surrey half duplexes', 'south-surrey-duplexes-for-sale'), ('South Surrey neighbourhoods', 'south-surrey-neighbourhoods'), ('South Surrey school catchments', 'south-surrey-school-catchments'),
             ('Surrey houses with coach houses', 'surrey-houses-with-coach-houses-for-sale'), ('Cloverdale houses with coach houses', 'cloverdale-houses-with-coach-houses-for-sale'),
             ('Langley houses with coach houses', 'langley-houses-with-coach-houses-for-sale'), ('Sell my house in South Surrey and White Rock', 'sell-my-house-in-south-surrey-white-rock'),
             ('South Surrey and White Rock market stats', 'south-surrey-white-rock-real-estate-market-stats'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'),
             ('Homes with multiplex potential', 'homes-with-multiplex-potential-fraser-valley'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('South Surrey houses', 'south-surrey-houses-for-sale')], faq, bl, 'South Surrey coach houses: your questions answered', links, dict(search_page=dict(kind='coach', city='south-surrey')))


# ================================================================== BURNABY AND COQUITLAM HOUSES
def burnaby_houses():
    slug = 'burnaby-houses-for-sale'
    c = group('burnaby', 'house'); boards = ['Burnaby North', 'Burnaby South', 'Burnaby East']
    rows = subrows(boards, 'house'); sn = snap('burnaby'); q = c['q']; bd = c['bands']
    by = {r['raw']: r for r in rows}
    cap, vh, ss, gr, hg = by['Capitol Hill BN'], by['Vancouver Heights'], by['South Slope'], by['Government Road'], by['Highgate']
    hl = priced(rows, 10); hi, lo = hl[-1], hl[0]
    seo = dict(title='Burnaby Houses for Sale | Sold Prices by Area', h1='Burnaby Houses for Sale', crumb='Burnaby houses',
               description='Search Burnaby detached houses for sale. Compare Capitol Hill, Vancouver Heights, South Slope and Government Road sold prices, and see how R1 zoning works.',
               links_h='More Burnaby real estate')
    comm = sorted(sn['comms'], key=lambda x: -x['inventory'])[:6]
    bl = [P('This search lists detached houses for sale in Burnaby, from the north slope above Hastings Street to the lots around Deer Lake and the east side. It leaves out condos, townhomes and half duplexes, which have their own searches.'),
          P(f'{c["n"]} Burnaby houses closed in the year to {LAST} at a median of {money(c["price"])}. {bd[6]} of them, {100 * bd[6] / c["n"]:.0f}%, sold for $1,800,000 or more. That puts Burnaby well above Surrey, where the City median was {money(group("surrey", "house")["price"])}.'),
          {'t': 'grid', 'gen': G},
          H('What Burnaby houses sold for'),
          measures('Detached houses sold in Burnaby', c, 'Burnaby houses'),
          P(f'A typical Burnaby house that sold was built in {c["yb"]} on a lot of {sqft(c["lot_sqft"])}, which is why the price per square foot of {money(c["ppsf"])} is the number to hold up against other cities. Houses took {c["dom"]} days and closed at {c["ratio"]}% of list.'),
          quarters('Burnaby houses sold, by period', c),
          P(f'The median price moved from {money(q[0]["price"])} in the first period to {money(q[3]["price"])} in the latest, a drop of {abs(100 * (q[3]["price"] - q[0]["price"]) / q[0]["price"]):.0f}%. The latest period only runs to {LAST}.'),
          bands('Burnaby houses sold, by price range', c, 'Sales'),
          H('Burnaby neighbourhoods compared'),
          P(f'{hi["name"]} had the highest median among neighbourhoods with 10 or more sales at {money(hi["price"])}, and {lo["name"]} the lowest at {money(lo["price"])}. '
            f'{cap["name"]} led North Burnaby with {cap["n"]} sales, and {ss["name"]} led South Burnaby with {ss["n"]}. {gr["name"]} has the biggest lots, with a median of {sqft(gr["lot"])}.'),
          subtable('Detached houses sold in Burnaby, by neighbourhood', rows, hub='burnaby-neighbourhood-guides', lim=16),
          P(f'Capitol Hill, the hill north of Hastings Street, and Vancouver Heights have median lots of about {sqft(cap["lot"])} and {sqft(vh["lot"])}. Vancouver Heights is a Burnaby neighbourhood, not part of Vancouver, with Boundary Road as the city line. '
            f'South Slope, between Rumble Street and Marine Drive, is covered by the Royal Oak Community Plan adopted in March 2025, and its median house sold for {money(ss["price"])}.'),
          hpi_table('Detached benchmark price in Burnaby, by board area', [('Burnaby North', hpi('gvr', 'Burnaby North', 'detached')), ('Burnaby South', hpi('gvr', 'Burnaby South', 'detached')), ('Burnaby East', hpi('gvr', 'Burnaby East', 'detached'))], 'gvr', SRC_GVR),
          P(f'The October 2026 monthly report counted {sn["inv"]} detached houses for sale in Burnaby and {sn["sold"]} sold, a sales ratio of {sn["ratio"]}%. The median was {money(sn["price"])} and houses closed at {sn["ll"]}% of list.'),
          tbl('Burnaby neighbourhoods with the most detached listings, October 2026', ['Neighbourhood', 'For sale', 'Sold', 'Sales ratio'], [[x['name'], str(x['inventory']), str(x['sales']), (f'{x["ratio"]}%' if x['ratio'] is not None else '—')] for x in comm],
              'Source: SnapStats® monthly report for October 2026, built on MLS® data from the Greater Vancouver REALTORS®.'),
          H('Burnaby’s house-lot rules'),
          P('Since July 1, 2024 nearly every Burnaby house lot sits in the R1 Small-Scale Multi-Unit Housing District. A lot of 280 square metres (3,014 square feet) or less can take 3 units, a larger lot 4, and 5 to 6 units are possible only in a Frequent Transit Neighbourhood Area. '
            'Laneway homes, duplexes, multiplexes and cottage courts are all on the list.'),
          P('A secondary suite counts toward the lot’s unit total, you get one suite per primary unit, and the suite stays on the same title as the house. Burnaby also has a new Zoning Bylaw 2026, adopted June 9, 2026 and effective July 1, 2026, '
            'and the Burnaby 2050 Official Community Plan, adopted December 9, 2025. Trees are protected by Tree Bylaw 10482, so check before you plan to clear a lot.'),
          P('Slope and water decide a lot of Burnaby building. The City’s application checklist, effective August 1, 2026, asks for a geotechnical report and, on steep sites, slope stability and hydrogeological reports. Lots beside a creek fall under the Streamside Protection and Enhancement Development Permit Area.'),
          H('Costs of owning a Burnaby house'),
          P('Burnaby’s 2026 municipal residential rate is $1.72223 per $1,000 of assessed value, plus a Metro Vancouver rate of $0.05440. A detached house pays $652.33 for 2026 water and $159 for the default garbage toter. '
            'Renting a suite adds $326.17 for water and $403.00 for sewer. Burnaby is a Speculation and Vacancy Tax area.'),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a Burnaby house', 'gen': G}, P(f'The calculator starts at the Burnaby median of {money(c["price"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': c['price'], 'gen': G}]
    faq = [('How much does a house cost in Burnaby?', f'The median Burnaby house sold for {money(c["price"])} in the year to {LAST}, with the middle half between {money(c["p25"])} and {money(c["p75"])}. That is {money(c["ppsf"])} a square foot.'),
           ('Which Burnaby neighbourhood has the most house sales?', f'{cap["name"]}, with {cap["n"]} sales and a median of {money(cap["price"])}. South Slope was next with {ss["n"]}.'),
           ('How many units can a Burnaby house lot take?', 'Three on a lot of 280 square metres or less, four on a larger lot, and five or six only in a Frequent Transit Neighbourhood Area. Suites count toward the total.'),
           ('Is Vancouver Heights in Vancouver?', 'No. It is a Burnaby neighbourhood. Boundary Road is the line with Vancouver, and property taxes are Burnaby’s.'),
           ('How fast do Burnaby houses sell?', f'{c["dom"]} days at a median, and houses closed at {c["ratio"]}% of list. {c["over"]}% went over the list price.'),
           ('Do I need a geotechnical report to build on a Burnaby slope?', 'Burnaby’s application checklist, effective August 1, 2026, asks for a geotechnical report, and for steep-slope sites slope stability and hydrogeological reports as well.')]
    links = [('Burnaby homes for sale', 'burnaby-homes-for-sale'), ('Burnaby condos for sale', 'burnaby-condos-for-sale'), ('Burnaby townhomes for sale', 'burnaby-townhomes-for-sale'),
             ('Burnaby neighbourhood guides', 'burnaby-neighbourhood-guides'), ('Burnaby market stats', 'burnaby-real-estate-market-stats'), ('Vancouver Heights houses', 'vancouver-heights-burnaby-houses-for-sale'),
             ('Burnaby Lake houses', 'burnaby-lake-houses-for-sale'), ('Burnaby Hospital area houses', 'burnaby-hospital-houses-for-sale'), ('Burnaby lots and land', 'burnaby-lots-land'),
             ('Burnaby presale condos and townhomes', 'burnaby-presale-condos-and-townhomes'), ('Schools in Burnaby', 'schools-in-burnaby-bc'), ('Coquitlam houses for sale', 'coquitlam-houses-for-sale'),
             ('Selling a home', 'selling'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Burnaby homes', 'burnaby-homes-for-sale')], faq, bl, 'Burnaby houses: your questions answered', links, dict(search_page=dict(kind='type', city='burnaby')))


def coquitlam_houses():
    slug = 'coquitlam-houses-for-sale'
    c = group('coquitlam', 'house'); boards = ['Coquitlam']
    rows = subrows(boards, 'house'); sn = snap('coquitlam'); q = c['q']; bd = c['bands']; h = hpi('gvr', 'Coquitlam', 'detached')
    by = {r['raw']: r for r in rows}
    cc, bm, wp, ce, nh = by['Central Coquitlam'], by['Burke Mountain'], by['Westwood Plateau'], by['Coquitlam East'], by['New Horizons']
    hl = priced(rows, 10); hi, lo = hl[-1], hl[0]; fast = min(rows[:5], key=lambda r: r['dom'])
    seo = dict(title='Coquitlam Houses for Sale | Burke Mountain & More', h1='Coquitlam Houses for Sale', crumb='Coquitlam houses',
               description='Search Coquitlam detached houses for sale. Compare Burke Mountain, Westwood Plateau and Central Coquitlam sold prices, and check the city’s R-1 to R-4 zones.',
               links_h='More Coquitlam real estate')
    comm = sorted(sn['comms'], key=lambda x: -x['inventory'])[:6]
    bl = [P('This search lists detached houses for sale in Coquitlam, from Coquitlam West and Central Coquitlam to Burke Mountain. Condos, townhomes and half duplexes are separate searches.'),
          P(f'{c["n"]} Coquitlam houses sold in the year to {LAST}, with a median price of {money(c["price"])}. Newer Burke Mountain houses were built around {bm["yb"]}, against {cc["yb"]} for Central Coquitlam, and the price gap between the two is {money(bm["price"] - cc["price"])}.'),
          {'t': 'grid', 'gen': G},
          H('How Coquitlam houses have sold'),
          measures('Detached houses sold in Coquitlam', c, 'Coquitlam houses'),
          P(f'Coquitlam houses closed at {c["ratio"]}% of the list price at a median and {c["over"]}% went over it, against {group("burnaby", "house")["over"]}% in Burnaby. The middle half of prices ran from {money(c["p25"])} to {money(c["p75"])}.'),
          quarters('Coquitlam houses sold, by period', c),
          P(f'Prices held between {money(q[0]["price"])} and {money(q[2]["price"])} for three periods, then the latest period, which runs only to {LAST}, came in at {money(q[3]["price"])} from {q[3]["n"]} sales.'),
          bands('Coquitlam houses sold, by price range', c, 'Sales'),
          hpi_table('Detached benchmark price, Coquitlam', [('Coquitlam', h)], 'gvr', SRC_GVR),
          H('Coquitlam neighbourhoods side by side'),
          P(f'Central Coquitlam had the most house sales, {cc["n"]}, followed by Burke Mountain with {bm["n"]} and Westwood Plateau with {wp["n"]}. Among neighbourhoods with 10 or more sales, {hi["name"]} had the highest median at {money(hi["price"])} and {lo["name"]} the lowest at {money(lo["price"])}. '
            f'{nh["name"]}, at a median lot of {sqft(nh["lot"])}, is the compact end of the market.'),
          subtable('Detached houses sold in Coquitlam, by neighbourhood', rows, hub='coquitlam-neighbourhood-guides', lim=16),
          P(f'Burke Mountain’s newer streets carry minimum subdivision sizes of 650 square metres and 18.5 metres of frontage in the R-1 and R-3 zones, and 465 square metres and 12.5 metres in R-2. Westwood Plateau is a master-planned community of 2,309 hectares and about 19,775 people. '
            f'Coquitlam East had {ce["n"]} sales at {money(ce["price"])}, and the quickest sale among the five busiest neighbourhoods was {fast["name"]}, at {fast["dom"]} days.'),
          P(f'The October 2026 monthly report counted {sn["inv"]} detached houses for sale in Coquitlam and {sn["sold"]} sold, a sales ratio of {sn["ratio"]}%. The median was {money(sn["price"])}.'),
          tbl('Coquitlam neighbourhoods with the most detached listings, October 2026', ['Neighbourhood', 'For sale', 'Sold', 'Sales ratio'], [[x['name'], str(x['inventory']), str(x['sales']), (f'{x["ratio"]}%' if x['ratio'] is not None else '—')] for x in comm],
              'Source: SnapStats® monthly report for October 2026, built on MLS® data from the Greater Vancouver REALTORS®.'),
          H('Coquitlam’s small-scale housing rules'),
          P('Coquitlam’s zoning bylaw is No. 3000, and Council adopted the small-scale multi-unit housing changes on June 9, 2025. A lot of 280 square metres or smaller can take up to 3 units; a lot over 280 and under 4,050 square metres can take up to 4. '
            'The 6-unit tier near frequent buses does not apply, because the City says Coquitlam has no bus stops that meet the provincial frequent-service rule.'),
          P('Most low-density lots now sit in R-1, R-2, R-3 or R-4, each with its own minimum lot size for adding units, from 465 square metres in R-2 to 930 square metres in R-4. The forms allowed include secondary suites, carriage houses, laneway homes, garden cottages, duplexes, triplexes and fourplexes.'),
          P('Talk to the City’s Development Services before you design anything if there is a creek on or next to the lot, a steep slope, or a house built before 1945. A Watercourse Protection Development Permit applies within 30 metres of the top of bank. '
            'The Interim Official Community Plan, Bylaw No. 5511, was adopted April 27, 2026.'),
          P('Coquitlam’s 2026 municipal residential rate is $2.2756 per $1,000 of assessed value, $3.8520 with the other taxing authorities. Taxes were due July 2, 2026. Coquitlam is a Speculation and Vacancy Tax area.'),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a Coquitlam house', 'gen': G}, P(f'The calculator starts at the Coquitlam median of {money(c["price"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': c['price'], 'gen': G}]
    faq = [('What does a house cost in Coquitlam?', f'The median was {money(c["price"])} over the year to {LAST}, at {money(c["ppsf"])} a square foot. The middle half of sales ran from {money(c["p25"])} to {money(c["p75"])}.'),
           ('Is Burke Mountain more expensive than Central Coquitlam?', f'Yes. Burke Mountain’s median was {money(bm["price"])} against {money(cc["price"])} in Central Coquitlam, on a smaller median lot ({sqft(bm["lot"])} against {sqft(cc["lot"])}).'),
           ('How many units can a Coquitlam lot take?', 'Up to 3 on a lot of 280 square metres or less and up to 4 on a larger lot under 4,050 square metres. There is no 6-unit tier because the City has no bus stops that meet the frequent-service rule.'),
           ('Can I build a carriage house in Coquitlam?', 'Carriage houses are one of the forms the City’s small-scale rules allow, along with laneway homes, garden cottages and secondary suites, in the R-1 to R-4 zones. Check the lot’s zone and minimum lot size.'),
           ('How fast do Coquitlam houses sell?', f'{c["dom"]} days at a median. The sold price was {c["ratio"]}% of list at a median.'),
           ('Which Coquitlam lots have creek rules?', 'Lots within 30 metres of the top of bank of a watercourse need a Watercourse Protection Development Permit. If there is a creek on or next to the lot, call Development Services before you design.')]
    links = [('Coquitlam homes for sale', 'coquitlam-homes-for-sale'), ('Coquitlam condos for sale', 'coquitlam-condos-for-sale'), ('Coquitlam townhomes for sale', 'coquitlam-townhomes-for-sale'),
             ('Coquitlam neighbourhood guides', 'coquitlam-neighbourhood-guides'), ('Coquitlam market stats', 'coquitlam-real-estate-market-stats'), ('Coquitlam East houses', 'coquitlam-east-houses-for-sale'),
             ('Coquitlam West houses', 'coquitlam-west-houses-for-sale'), ('Coquitlam lots and land', 'coquitlam-lots-land'), ('Coquitlam presale condos and townhomes', 'coquitlam-presale-condos-and-townhomes'),
             ('Schools in Coquitlam', 'schools-in-coquitlam-bc'), ('Burnaby houses for sale', 'burnaby-houses-for-sale'), ('Selling a home', 'selling'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Coquitlam homes', 'coquitlam-homes-for-sale')], faq, bl, 'Coquitlam houses: your questions answered', links, dict(search_page=dict(kind='type', city='coquitlam')))


# ================================================================== RICHMOND
RB = ['Richmond']; VB = ['Vancouver West', 'Vancouver East']


def richmond_houses():
    slug = 'richmond-houses-for-sale'
    rows = subrows(RB, 'house'); tot = total(RB, 'house'); qs = qsum(RB, 'house'); h = hpi('gvr', 'Richmond', 'detached')
    by = {r['raw']: r for r in rows}
    sea, gra, ss, sn_, br, quil, ham, tn, sv = by['Seafair'], by['Granville'], by['Steveston South'], by['Steveston North'], by['Broadmoor'], by['Quilchena RI'], by['Hamilton RI'], by['Terra Nova'], by['Steveston Village']
    hl = priced(rows, 10); hi, lo = hl[-1], hl[0]; slow = max(rows[:16], key=lambda r: r['dom'])
    seo = dict(title='Richmond Houses for Sale | Seafair to Steveston', h1='Richmond Houses for Sale', crumb='Richmond houses',
               description='Search Richmond detached houses for sale. Compare Seafair, Steveston, Broadmoor and Granville sold prices, and see what the 2024 RSM rezoning changed.',
               links_h='More Richmond real estate')
    bl = [P('This search lists detached houses for sale across Richmond, from Steveston in the south-west to Hamilton in the east. Condos and townhomes have their own searches, linked at the bottom of the page.'),
          P(f'{tot} Richmond houses closed in the year to {LAST}, spread over {len(rows)} neighbourhoods. The sold records I use report Richmond by neighbourhood, so there is no single city median here: the table below gives each neighbourhood’s own figure, '
            f'and the Home Price Index benchmark for a typical Richmond detached home was {money(h["benchmark"])} in September 2026.'),
          {'t': 'grid', 'gen': G},
          H('Where Richmond houses sold, and how fast'),
          P(f'{hi["name"]} had the highest median price among neighbourhoods with 10 or more sales, {money(hi["price"])}, and {lo["name"]} the lowest, {money(lo["price"])}. '
            f'The gap between them is {money(hi["price"] - lo["price"])}. The most active neighbourhood was {sea["name"]} with {sea["n"]} sales, ahead of {gra["name"]} with {gra["n"]}.'),
          subtable('Detached houses sold in Richmond, by neighbourhood', rows, hub='richmond-neighbourhood-guides', lim=16),
          P(f'Speed varies as much as price. Steveston South houses took {ss["dom"]} days at a median and Steveston North {sn_["dom"]}. {slow["name"]} took {slow["dom"]} days, the slowest in the table. '
            f'Steveston Village is the small-lot end of the Steveston area at {sv["n"]} sales and {money(sv["ppsf"])} a square foot, against {money(sea["ppsf"])} in Seafair.'),
          P(f'Lot size explains a lot of the price. The median Steveston South house sat on {sqft(ss["lot"])}, against {sqft(br["lot"])} in Broadmoor and {sqft(gra["lot"])} in Granville. Seafair, at {sqft(sea["lot"])}, has newer homes (median built {sea["yb"]}) than Granville ({gra["yb"]}).'),
          qcounts('Richmond houses sold, by period', qs),
          P(f'Counts rose from {qs[0]} in the first period to {qs[2]} in May to July, then {qs[3]} in the part-period to {LAST}. Treat the last figure as a partial count, not a drop.'),
          hpi_table('Detached benchmark price in Richmond', [('Richmond', h)], 'gvr', SRC_GVR),
          H('Richmond’s 2024 house-lot rezoning'),
          P('On June 24, 2024 Richmond Council rezoned almost 27,000 single-family and duplex lots into four new zones: RSM/S, RSM/M, RSM/L and RSM/XL. About 84% of those lots had been RS1/A, RS1/B or RS1/E, the city’s standard single-family lots. '
            'The City’s zoning bylaw is No. 8500.'),
          P('Five transit-oriented areas, around the Bridgeport, Capstan, Aberdeen, Lansdowne and Brighouse stations, were left out of that rezoning because they have their own plans. If a house you like is close to one of those stations, ask which rules apply before you count on extra units.'),
          H('Dikes, soil and farmland'),
          P('Richmond is an island city and 49 kilometres of dikes protect it. Richmond Fire-Rescue says pockets of liquefaction are possible in a significant earthquake, so a geotechnical question is a fair one to ask about any older house on soft ground. '
            'East of No. 4 Road the land falls into the Agricultural Land Reserve, which includes the Garden City Lands, and those parcels follow Reserve rules rather than the city’s house-lot zones.'),
          H('Questions to ask before you offer on a Richmond house'),
          L(['What is the lot’s zone now? Many former RS1 lots became one of the four RSM zones in 2024.',
             'Is the house inside one of the five station areas that were left out of the rezoning?',
             'Is the lot east of No. 4 Road? If so, check Agricultural Land Reserve status.',
             'Has the house had a geotechnical or foundation report? Ask, especially for homes near the dikes.']),
          {'t': 'h', 'level': 2, 'text': 'Estimate the payment on a Richmond house', 'gen': G}, P(f'The calculator starts at the September 2026 benchmark price for a Richmond detached home, {money(h["benchmark"])}.'),
          {'t': 'calc', 'which': 'mortgage', 'price': h['benchmark'], 'gen': G}]
    faq = [('How much does a house cost in Richmond?', f'It depends on the neighbourhood. Among neighbourhoods with 10 or more sales, medians ran from {money(lo["price"])} in {lo["name"]} to {money(hi["price"])} in {hi["name"]}. The benchmark price for a typical Richmond detached home was {money(h["benchmark"])} in September 2026.'),
           ('Which Richmond neighbourhood has the most house sales?', f'{sea["name"]}, with {sea["n"]} sales and a median of {money(sea["price"])}. {gra["name"]} was second with {gra["n"]}.'),
           ('What are the RSM zones in Richmond?', 'RSM/S, RSM/M, RSM/L and RSM/XL are the four zones Richmond Council created on June 24, 2024 for almost 27,000 former single-family and duplex lots. Check the lot’s current zone on the City’s map.'),
           ('Does the 2024 rezoning apply around the five station areas?', 'No. The areas around the Bridgeport, Capstan, Aberdeen, Lansdowne and Brighouse stations are excluded from it and have their own rules.'),
           ('Are Richmond houses at risk of flooding?', 'The city is protected by 49 kilometres of dikes. The City also notes pockets of liquefaction are possible in a significant earthquake. Ask for the foundation report on an older house.'),
           ('How long does it take to sell a house in Richmond?', f'It varies by neighbourhood: {sn_["dom"]} days in Steveston North, {ss["dom"]} in Steveston South and {quil["dom"]} in Quilchena at a median.')]
    links = [('Richmond homes for sale', 'richmond-homes-for-sale'), ('Richmond condos for sale', 'richmond-condos-for-sale'), ('Richmond townhomes for sale', 'richmond-townhomes-for-sale'),
             ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'), ('Richmond market stats', 'richmond-real-estate-market-stats'), ('Schools in Richmond', 'schools-in-richmond-bc'),
             ('Vancouver houses for sale', 'vancouver-houses-for-sale'), ('Burnaby houses for sale', 'burnaby-houses-for-sale'), ('Selling a home', 'selling'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Richmond homes', 'richmond-homes-for-sale')], faq, bl, 'Richmond houses: your questions answered', links, dict(search_page=dict(kind='type', city='richmond')))


def richmond_condos():
    slug = 'richmond-condos-for-sale'
    rows = subrows(RB, 'condo'); tot = total(RB, 'condo'); qs = qsum(RB, 'condo'); h = hpi('gvr', 'Richmond', 'apartment')
    by = {r['raw']: r for r in rows}
    bh, wc, bs, ss, mn, ham, ir, bp, br_ = by['Brighouse'], by['West Cambie'], by['Brighouse South'], by['Steveston South'], by['McLennan North'], by['Hamilton RI'], by['Ironwood'], by['Boyd Park'], by['Bridgeport RI']
    btab, allc = buildings('Richmond condo buildings with the most sales', RB, 'condo')
    seo = dict(title='Richmond Condos for Sale | Prices by Neighbourhood', h1='Richmond Condos for Sale', crumb='Richmond condos',
               description='Search Richmond condos for sale. See what Brighouse, West Cambie and Steveston condos sold for, with strata fees by building and the benchmark price.',
               links_h='More Richmond real estate')
    bl = [P('This search lists condos for sale in Richmond: apartment-style homes in strata buildings, from the towers around Richmond Centre to the low-rises in Steveston. Houses and townhomes are separate searches.'),
          P(f'{tot:,} Richmond condos closed in the year to {LAST}, in {len(rows)} neighbourhoods. {bh["name"]} alone had {bh["n"]} of them, {100 * bh["n"] / tot:.0f}% of the city, at a median of {money(bh["price"])}. '
            f'The sold records report Richmond by neighbourhood, so I give neighbourhood medians instead of one city number.'),
          {'t': 'grid', 'gen': G},
          H('What Richmond condos sold for'),
          subtable('Condos sold in Richmond, by neighbourhood', [r for r in rows], hub='richmond-neighbourhood-guides', strata=True, lim=8),
          P(f'Age matters as much as location. West Cambie’s condos were built around {wc["yb"]} and sold at a median of {money(wc["price"])}, which is {money(wc["ppsf"])} a square foot. Brighouse South’s were built around {bs["yb"]} and sold at {money(bs["price"])}, or {money(bs["ppsf"])} a square foot. '
            f'Hamilton’s median year built is {ham["yb"]}, which means a lot of those sales were in new buildings.'),
          P(f'Strata fees run from {money(ham["maint"])} a month in Hamilton to {money(ss["maint"])} in Steveston South and {money(ir["maint"])} in Ironwood. Brighouse sits at {money(bh["maint"])}. Fees tell you what the building covers, so compare them alongside price, not after.'),
          qcounts('Richmond condos sold, by period', qs),
          P(f'Sales ran {qs[0]} in November to January, {qs[1]} in February to April and {qs[2]} in May to July. The latest period, to {LAST}, shows {qs[3]} and is not a full quarter.'),
          hpi_table('Apartment benchmark price in Richmond', [('Richmond', h)], 'gvr', SRC_GVR),
          H('Buildings that sold most'),
          btab,
          P('A building’s price here comes from its own closed sales, so a tower with 20 sales says more than one with 5. Buildings with fewer than 5 sales are left out, because one or two sales is not a price.'),
          H('Buying a Richmond condo'),
          P('Richmond is protected by 49 kilometres of dikes, and Richmond Fire-Rescue says pockets of liquefaction are possible in a significant earthquake. Ask the strata about building insurance, the depreciation report and any past water damage before you offer. '
            'The BC condo buying rules page covers the strata documents.'),
          L(['Ask for the strata minutes and the depreciation report, and read the last two years of minutes for special levies.',
             f'Check what the monthly fee includes. Ironwood ({money(ir["maint"])}) and Steveston South ({money(ss["maint"])}) sit above Brighouse ({money(bh["maint"])}).',
             'Check whether the building allows rentals and pets before you offer.',
             'For a new building in Hamilton, ask for the occupancy date and the status of the common areas.'])]
    faq = [('How much is a condo in Richmond?', f'The median Richmond condo sold for about {money(bh["price"])} in Brighouse, {money(wc["price"])} in West Cambie and {money(ss["price"])} in Steveston South over the year to {LAST}. The apartment benchmark for the city was {money(h["benchmark"])} in September 2026.'),
           ('Where do most Richmond condos sell?', f'Brighouse, with {bh["n"]} of {tot:,} sales, then West Cambie with {wc["n"]} and Brighouse South with {bs["n"]}.'),
           ('What are strata fees for a Richmond condo?', f'Median monthly fees by neighbourhood ran from {money(ham["maint"])} in Hamilton to {money(ir["maint"])} in Ironwood, with {money(bh["maint"])} in Brighouse. The building decides, so check the fee in the listing.'),
           ('Which Richmond condo neighbourhoods are newest?', f'Hamilton (median built {ham["yb"]}), Bridgeport ({br_["yb"]}) and West Cambie ({wc["yb"]}).'),
           ('Did Richmond condo prices fall?', f'The apartment benchmark price moved {pct(h["chg_1y"])} over one year and {pct(h["chg_3y"])} over three years, to {money(h["benchmark"])} in September 2026.'),
           ('Where do I find the rules for buying a strata?', 'On the BC condo buying rules page. It covers the strata documents you are entitled to and what to read before you remove subjects.')]
    links = [('Richmond homes for sale', 'richmond-homes-for-sale'), ('Richmond houses for sale', 'richmond-houses-for-sale'), ('Richmond townhomes for sale', 'richmond-townhomes-for-sale'),
             ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'), ('Richmond market stats', 'richmond-real-estate-market-stats'), ('BC condo buying rules', 'bc-condo-buying-rules'),
             ('Vancouver condos for sale', 'vancouver-condos-for-sale'), ('Burnaby condos for sale', 'burnaby-condos-for-sale'), ('Schools in Richmond', 'schools-in-richmond-bc'),
             ('First-time home buyer programs', 'first-time-home-buyer-program'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Richmond homes', 'richmond-homes-for-sale')], faq, bl, 'Richmond condos: your questions answered', links, dict(search_page=dict(kind='type', city='richmond')))


def richmond_townhomes():
    slug = 'richmond-townhomes-for-sale'
    rows = subrows(RB, 'townhome'); tot = total(RB, 'townhome'); qs = qsum(RB, 'townhome'); h = hpi('gvr', 'Richmond', 'townhouse')
    by = {r['raw']: r for r in rows}
    mn, bs, wc, ham, ec, ss, sa, bm, tn, bp, wd = by['McLennan North'], by['Brighouse South'], by['West Cambie'], by['Hamilton RI'], by['East Cambie'], by['Steveston South'], by['Saunders'], by['Broadmoor'], by['Terra Nova'], by['Bridgeport RI'], by['Woodwards']
    btab, allc = buildings('Richmond townhome complexes with the most sales', RB, 'townhome')
    fmin, fmax = min(rows[:12], key=lambda r: r['maint']), max(rows[:12], key=lambda r: r['maint'])
    seo = dict(title='Richmond Townhomes for Sale | McLennan to Steveston', h1='Richmond Townhomes for Sale', crumb='Richmond townhomes',
               description='Search Richmond townhomes for sale. Compare McLennan North, West Cambie, Hamilton and Steveston sold prices, strata fees and complexes with the most sales.',
               links_h='More Richmond real estate')
    bl = [P('This search lists townhomes for sale in Richmond: ground-oriented homes in strata complexes, usually with a garage and two or three floors. Houses and condos are separate searches.'),
          P(f'{tot} Richmond townhomes closed in the year to {LAST} across {len(rows)} neighbourhoods. McLennan North led with {mn["n"]} sales, {100 * mn["n"] / tot:.0f}% of the total, at a median of {money(mn["price"])}. '
            f'The sold records report Richmond by neighbourhood, so there is no one city median on this page.'),
          {'t': 'grid', 'gen': G},
          H('Richmond townhome prices by neighbourhood'),
          subtable('Townhomes sold in Richmond, by neighbourhood', rows, hub='richmond-neighbourhood-guides', strata=True, lim=12),
          P(f'Prices cluster in three tiers. Brighouse South ({money(bs["price"])}), Hamilton ({money(ham["price"])}), Saunders ({money(sa["price"])}) and Granville ({money(by["Granville"]["price"])}) sit below $900,000. East Cambie ({money(ec["price"])}) and Broadmoor ({money(bm["price"])}) sit near $950,000. '
            f'McLennan North ({money(mn["price"])}), West Cambie ({money(wc["price"])}), Bridgeport ({money(bp["price"])}), Steveston South ({money(ss["price"])}), Terra Nova ({money(tn["price"])}) and Woodwards ({money(wd["price"])}) run above $1,000,000.'),
          P(f'Hamilton is the fast one. Its townhomes took a median of {ham["dom"]} days to sell, built around {ham["yb"]}, at {money(ham["ppsf"])} a square foot. Broadmoor took {bm["dom"]} days. Median strata fees ranged from {money(fmin["maint"])} a month in {fmin["name"]} to {money(fmax["maint"])} in {fmax["name"]}, and McLennan North was {money(mn["maint"])}.'),
          qcounts('Richmond townhomes sold, by period', qs),
          P(f'The busiest period was May to July with {qs[2]} sales, against {qs[0]} in November to January. The last period to {LAST} has {qs[3]}.'),
          hpi_table('Townhouse benchmark price in Richmond', [('Richmond', h)], 'gvr', SRC_GVR),
          *([H('Complexes that sold most'), btab] if len(allc) >= 3 else []),
          P(f'Age shows in the price. Bridgeport’s townhomes, built around {bp["yb"]}, sold at {money(bp["price"])}, and Brighouse South’s, built around {bs["yb"]}, at {money(bs["price"])}. The year built and fee columns help you place a complex.'),
          H('Buying a Richmond townhome'),
          P('A townhome is usually a strata lot, so read the bylaws and the depreciation report. The BC townhome buying rules page lists what to ask for.'),
          L(['Ask who pays for roof and exterior repairs, and whether the strata has set money aside.',
             'Check pet, rental and parking bylaws before you offer.',
             'Compare complexes inside the same neighbourhood, using the fee and year built.',
             'For a newer unit, ask what is left of the new-home warranty.'])]
    faq = [('How much is a townhome in Richmond?', f'The median Richmond townhome sold for {money(mn["price"])} in McLennan North, {money(ham["price"])} in Hamilton and {money(ss["price"])} in Steveston South over the year to {LAST}. The townhouse benchmark was {money(h["benchmark"])} in September 2026.'),
           ('Where are most townhomes sold in Richmond?', f'McLennan North, with {mn["n"]} of {tot} sales, then Brighouse South with {bs["n"]} and West Cambie with {wc["n"]}.'),
           ('Which Richmond townhome area is the cheapest?', f'Hamilton and Granville sit lowest among the larger areas, at {money(ham["price"])} and {money(by["Granville"]["price"])}. Brighouse South is {money(bs["price"])}.'),
           ('What are strata fees for a Richmond townhome?', f'Median fees ranged from {money(fmin["maint"])} a month in {fmin["name"]} to {money(fmax["maint"])} in {fmax["name"]}, among the 12 busiest neighbourhoods.'),
           ('How fast do Richmond townhomes sell?', f'Hamilton took {ham["dom"]} days at a median and Broadmoor {bm["dom"]}. McLennan North took {mn["dom"]}.'),
           ('How have townhome prices changed?', f'The Richmond townhouse benchmark moved {pct(h["chg_1y"])} over one year and {pct(h["chg_3y"])} over three.')]
    links = [('Richmond homes for sale', 'richmond-homes-for-sale'), ('Richmond houses for sale', 'richmond-houses-for-sale'), ('Richmond condos for sale', 'richmond-condos-for-sale'),
             ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'), ('Richmond market stats', 'richmond-real-estate-market-stats'), ('BC townhome buying rules', 'bc-townhome-buying-rules'),
             ('Vancouver townhomes for sale', 'vancouver-townhomes-for-sale'), ('Burnaby townhomes for sale', 'burnaby-townhomes-for-sale'), ('Schools in Richmond', 'schools-in-richmond-bc'),
             ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Richmond homes', 'richmond-homes-for-sale')], faq, bl, 'Richmond townhomes: your questions answered', links, dict(search_page=dict(kind='type', city='richmond')))


# ================================================================== VANCOUVER
def vancouver_houses():
    slug = 'vancouver-houses-for-sale'
    rw = subrows(['Vancouver West'], 'house'); re_ = subrows(['Vancouver East'], 'house'); rows = subrows(VB, 'house')
    tot = total(VB, 'house'); tw, te = total(['Vancouver West'], 'house'), total(['Vancouver East'], 'house'); qs = qsum(VB, 'house')
    hw, he = hpi('gvr', 'Vancouver West', 'detached'), hpi('gvr', 'Vancouver East', 'detached')
    by = {(r['raw'], r['board']): r for r in rows}
    g = lambda n, b: by[(n, b)]
    dun, kit, pg, ker, mac, shaw = g('Dunbar', 'Vancouver West'), g('Kitsilano', 'Vancouver West'), g('Point Grey', 'Vancouver West'), g('Kerrisdale', 'Vancouver West'), g('MacKenzie Heights', 'Vancouver West'), g('Shaughnessy', 'Vancouver West')
    ren, gw, kn, kil, sv = g('Renfrew VE', 'Vancouver East'), g('Grandview Woodland', 'Vancouver East'), g('Knight', 'Vancouver East'), g('Killarney VE', 'Vancouver East'), g('South Vancouver', 'Vancouver East')
    ee = priced([r for r in re_ if r['n'] >= 20], 20); elo, ehi = ee[0], ee[-1]
    seo = dict(title='Vancouver Houses for Sale | West Side & East Side', h1='Vancouver Houses for Sale', crumb='Vancouver houses',
               description='Search Vancouver detached houses for sale. Compare Dunbar, Kerrisdale, Renfrew and Grandview sold prices, and see what the R1-1 zone allows on a house lot.',
               links_h='More Vancouver real estate')
    bl = [P('This search lists detached houses for sale across the city of Vancouver, on the West Side and the East Side. Condos and townhomes have their own searches, and the North Shore and Burnaby are not included.'),
          P(f'{tot:,} Vancouver houses closed in the year to {LAST}: {tw} in Vancouver West and {te} in Vancouver East. The sold records report Vancouver by neighbourhood, so you get a median per neighbourhood instead of one city number. '
            f'The Home Price Index benchmark for a typical detached home was {money(hw["benchmark"])} in Vancouver West and {money(he["benchmark"])} in Vancouver East in September 2026.'),
          {'t': 'grid', 'gen': G},
          H('The West Side: Vancouver West neighbourhoods'),
          P(f'West Side houses start high. {shaw["name"]} had the highest median, {money(shaw["price"])}, and took {shaw["dom"]} days to sell. {mac["name"]} ({money(mac["price"])}), {ker["name"]} ({money(ker["price"])}) and {pg["name"]} ({money(pg["price"])}) all sit above $3,000,000. '
            f'{dun["name"]} had the most sales, {dun["n"]}, at {money(dun["price"])}, and {kit["name"]} had {kit["n"]} at {money(kit["price"])}.'),
          subtable('Detached houses sold in Vancouver West, by neighbourhood', rw, hub='vancouver-neighbourhood-guides', lim=12),
          H('The East Side: Vancouver East neighbourhoods'),
          P(f'East Side medians run from {money(elo["price"])} in {elo["name"]} to {money(ehi["price"])} in {ehi["name"]}, among neighbourhoods with 20 or more sales. {ren["name"]} had {ren["n"]} sales at {money(ren["price"])}, {kn["name"]} {kn["n"]} at {money(kn["price"])} and {sv["name"]} {sv["n"]} at {money(sv["price"])}. '
            f'{gw["name"]} is the one to watch: {gw["n"]} sales, a median of {money(gw["price"])} and just {gw["dom"]} days to sell, in houses with a median build year of {gw["yb"]}. {kil["name"]} sold at {money(kil["price"])} on {sqft(kil["lot"])}.'),
          subtable('Detached houses sold in Vancouver East, by neighbourhood', re_, hub='vancouver-neighbourhood-guides', lim=12),
          qcounts('Vancouver houses sold, by period', qs),
          P(f'Sales ran {qs[0]} in November to January, {qs[1]} in February to April and {qs[2]} in May to July. The last period, to {LAST}, has {qs[3]}.'),
          hpi_table('Detached benchmark price in Vancouver', [('Vancouver West', hw), ('Vancouver East', he)], 'gvr', SRC_GVR),
          H('What the R1-1 zone allows on a Vancouver house lot'),
          P('On October 17, 2023 Vancouver replaced nine RS zones with a single R1-1 zone for about 65,000 lots. R1-1 allows a house with a secondary suite or a laneway house, a duplex, character retention, and multiplexes of 3 to 6 strata units or up to 8 rental units.'),
          P('The multiple-dwelling option is conditional. It needs rear-lane access, a site outside a designated flood plain, and a lot that was a single lot of record before October 17, 2023. New houses, duplexes and multiplexes also need a detention tank for stormwater from July 1, 2025.'),
          P('The Vancouver Plan became part of the Official Development Plan on March 12, 2026. In the Renfrew area, the Rupert and Renfrew Station Area Plan was approved on July 8, 2025.'),
          H('Costs and rules that follow a Vancouver house'),
          P('Vancouver’s Empty Homes Tax is 3% of assessed value for a home that is not occupied or rented. The City’s Tenant Relocation and Protection Policy applies citywide when a rented house is redeveloped.'),
          L(['Check the lot’s zone, and the lane, before counting on a laneway house or multiplex.',
             'Ask whether a house is a character house with retention incentives.',
             'Add the detention tank to a redevelopment budget.',
             'Confirm tenant rules if the house is rented.'])]
    faq = [('How much does a house cost in Vancouver?', f'It depends on the side. Vancouver West neighbourhoods like Dunbar ({money(dun["price"])}) and Kerrisdale ({money(ker["price"])}) are near $3,000,000, while Renfrew ({money(ren["price"])}) and Knight ({money(kn["price"])}) are on the East Side. The September 2026 benchmark was {money(hw["benchmark"])} West and {money(he["benchmark"])} East.'),
           ('Which Vancouver neighbourhood has the most house sales?', f'{dun["name"]}, with {dun["n"]} sales, then {ren["name"]} with {ren["n"]} and {kit["name"]} with {kit["n"]}.'),
           ('Which Vancouver houses sell the fastest?', f'{gw["name"]} had a median of {gw["dom"]} days. Renfrew took {ren["dom"]} and Kitsilano {kit["dom"]}. Shaughnessy took {shaw["dom"]}.'),
           ('What is the R1-1 zone?', 'It is the zone that replaced nine RS zones on October 17, 2023, for about 65,000 lots. It allows a house with a suite or laneway house, a duplex, character retention and multiplexes.'),
           ('Can I build a multiplex on a Vancouver house lot?', 'Sometimes. It needs rear-lane access, a site outside a designated flood plain and a lot that was a single lot of record before October 17, 2023.'),
           ('Is there a vacancy tax in Vancouver?', 'The City’s Empty Homes Tax is 3% of assessed value for a home that is not occupied or rented.')]
    links = [('Vancouver homes for sale', 'vancouver-homes-for-sale'), ('Vancouver condos for sale', 'vancouver-condos-for-sale'), ('Vancouver townhomes for sale', 'vancouver-townhomes-for-sale'),
             ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'), ('Vancouver market stats', 'vancouver-real-estate-market-stats'), ('Vancouver presale condos and townhomes', 'vancouver-presale-condos-and-townhomes'),
             ('Schools in Vancouver', 'schools-in-vancouver-bc'), ('Richmond houses for sale', 'richmond-houses-for-sale'), ('Burnaby houses for sale', 'burnaby-houses-for-sale'), ('Selling a home', 'selling'),
             ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Vancouver homes', 'vancouver-homes-for-sale')], faq, bl, 'Vancouver houses: your questions answered', links, dict(search_page=dict(kind='type', city='vancouver')))


def vancouver_condos():
    slug = 'vancouver-condos-for-sale'
    rw = subrows(['Vancouver West'], 'condo'); re_ = subrows(['Vancouver East'], 'condo'); rows = subrows(VB, 'condo')
    tot = total(VB, 'condo'); tw, te = total(['Vancouver West'], 'condo'), total(['Vancouver East'], 'condo'); qs = qsum(VB, 'condo')
    hw, he = hpi('gvr', 'Vancouver West', 'apartment'), hpi('gvr', 'Vancouver East', 'apartment')
    by = {(r['raw'], r['board']): r for r in rows}
    g = lambda n, b='Vancouver West': by[(n, b)]
    dt, yal, we, kit, fv, fc, uni, ch = g('Downtown VW'), g('Yaletown'), g('West End VW'), g('Kitsilano'), g('Fairview VW'), g('False Creek'), g('University VW'), g('Coal Harbour')
    mp, col, sm = g('Mount Pleasant VE', 'Vancouver East'), g('Collingwood VE', 'Vancouver East'), g('South Marine', 'Vancouver East')
    btab, allc = buildings('Vancouver condo buildings with the most sales', VB, 'condo')
    assert ch['maint'] == max(r['maint'] for r in rw[:12])
    seo = dict(title='Vancouver Condos for Sale | Downtown to East Van', h1='Vancouver Condos for Sale', crumb='Vancouver condos',
               description='Search Vancouver condos for sale. See Downtown, Yaletown, Kitsilano and Mount Pleasant sold prices, strata fees by building and the apartment benchmark.',
               links_h='More Vancouver real estate')
    bl = [P('This search lists condos for sale in the city of Vancouver, from Coal Harbour and Yaletown to Collingwood and South Marine. Houses and townhomes have their own searches.'),
          P(f'{tot:,} Vancouver condos closed in the year to {LAST}: {tw:,} in Vancouver West and {te:,} in Vancouver East. {dt["name"]} led with {dt["n"]} sales at a median of {money(dt["price"])}. '
            f'The sold records report Vancouver by neighbourhood, so each neighbourhood has its own median.'),
          {'t': 'grid', 'gen': G},
          H('West Side and downtown condos'),
          P(f'Downtown peninsula neighbourhoods have the volume. {dt["name"]} had {dt["n"]} sales, {yal["name"]} {yal["n"]} at {money(yal["price"])}, the West End {we["n"]} at {money(we["price"])}, and Kitsilano {kit["n"]} at {money(kit["price"])}. '
            f'Coal Harbour is the premium end: {ch["n"]} sales at {money(ch["price"])} and a strata fee of {money(ch["maint"])} a month, the highest in the West table below.'),
          subtable('Condos sold in Vancouver West, by neighbourhood', rw, hub='vancouver-neighbourhood-guides', strata=True, lim=12),
          H('East Side condos'),
          P(f'East of Main Street prices fall quickly. {mp["name"]} had {mp["n"]} sales at {money(mp["price"])}, {col["name"]} {col["n"]} at {money(col["price"])} and {sm["name"]} {sm["n"]} at {money(sm["price"])}. '
            f'Collingwood’s median strata fee is {money(col["maint"])} a month, well below Coal Harbour’s {money(ch["maint"])}. South Marine is newer (median built {sm["yb"]}) at {money(sm["ppsf"])} a square foot.'),
          subtable('Condos sold in Vancouver East, by neighbourhood', re_, hub='vancouver-neighbourhood-guides', strata=True, lim=9),
          qcounts('Vancouver condos sold, by period', qs),
          P(f'Sales ran {qs[0]} in November to January, {qs[1]} in February to April and {qs[2]} in May to July. The last period, to {LAST}, has {qs[3]}.'),
          hpi_table('Apartment benchmark price in Vancouver', [('Vancouver West', hw), ('Vancouver East', he)], 'gvr', SRC_GVR),
          H('Buildings that sold most'),
          btab,
          H('Rules and risks that apply to Vancouver condos'),
          P('Yaletown is on the Canada Line at Yaletown-Roundhouse station, and the Yaletown Historic Area (HA-3) caps building height at 21.4 metres. Parts of False Creek North are exposed to flooding from sea-level rise, so ask what the strata has planned.'),
          P('Vancouver’s Empty Homes Tax is 3% of assessed value for a home that is neither occupied nor rented. The Tenant Relocation and Protection Policy applies citywide if a rented building is redeveloped. For the strata documents you should read before you buy, see the BC condo buying rules.'),
          P('If you want a new building rather than a resale, the presale condos and townhomes page lists the Vancouver projects. The downtown condo search is a narrower view of the peninsula.')]
    faq = [('How much is a condo in Vancouver?', f'It varies by neighbourhood: {money(col["price"])} in Collingwood, {money(dt["price"])} Downtown, {money(we["price"])} in the West End and {money(yal["price"])} in Yaletown, over the year to {LAST}. The apartment benchmark was {money(hw["benchmark"])} West and {money(he["benchmark"])} East in September 2026.'),
           ('Where do most Vancouver condos sell?', f'Downtown ({dt["n"]} sales), Yaletown ({yal["n"]}), the West End ({we["n"]}), Kitsilano ({kit["n"]}) and Mount Pleasant East ({mp["n"]}).'),
           ('What are strata fees in Vancouver?', f'Median fees run from {money(col["maint"])} in Collingwood to {money(ch["maint"])} in Coal Harbour. Yaletown is {money(yal["maint"])} and Downtown {money(dt["maint"])}.'),
           ('Is Yaletown on the Canada Line?', 'Yes, Yaletown-Roundhouse station. The Yaletown Historic Area (HA-3) also caps building height at 21.4 metres.'),
           ('Did Vancouver condo prices fall?', f'Over one year the apartment benchmark moved {pct(hw["chg_1y"])} in Vancouver West and {pct(he["chg_1y"])} in Vancouver East, to {money(hw["benchmark"])} and {money(he["benchmark"])} in September 2026.'),
           ('Does Vancouver have a tax on empty condos?', 'Yes. The Empty Homes Tax is 3% of assessed value for a home that is not occupied or rented.')]
    links = [('Vancouver homes for sale', 'vancouver-homes-for-sale'), ('Vancouver houses for sale', 'vancouver-houses-for-sale'), ('Vancouver townhomes for sale', 'vancouver-townhomes-for-sale'),
             ('Downtown Vancouver condos', 'downtown-vancouver-condos-for-sale'), ('Vancouver presale condos and townhomes', 'vancouver-presale-condos-and-townhomes'),
             ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'), ('Vancouver market stats', 'vancouver-real-estate-market-stats'), ('BC condo buying rules', 'bc-condo-buying-rules'),
             ('Richmond condos for sale', 'richmond-condos-for-sale'), ('Burnaby condos for sale', 'burnaby-condos-for-sale'), ('First-time home buyer programs', 'first-time-home-buyer-program'),
             ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Vancouver homes', 'vancouver-homes-for-sale')], faq, bl, 'Vancouver condos: your questions answered', links, dict(search_page=dict(kind='type', city='vancouver')))


def vancouver_townhomes():
    slug = 'vancouver-townhomes-for-sale'
    rw = subrows(['Vancouver West'], 'townhome'); re_ = subrows(['Vancouver East'], 'townhome'); rows = subrows(VB, 'townhome')
    tot = total(VB, 'townhome'); tw, te = total(['Vancouver West'], 'townhome'), total(['Vancouver East'], 'townhome'); qs = qsum(VB, 'townhome')
    hw, he = hpi('gvr', 'Vancouver West', 'townhouse'), hpi('gvr', 'Vancouver East', 'townhouse')
    by = {(r['raw'], r['board']): r for r in rows}
    g = lambda n, b='Vancouver West': by[(n, b)]
    kit, fv, cam, uni = g('Kitsilano'), g('Fairview VW'), g('Cambie'), g('University VW')
    mp, col, gw, chm = g('Mount Pleasant VE', 'Vancouver East'), g('Collingwood VE', 'Vancouver East'), g('Grandview Woodland', 'Vancouver East'), g('Champlain Heights', 'Vancouver East')
    btab, allc = buildings('Vancouver townhome complexes with the most sales', VB, 'townhome')
    seo = dict(title='Vancouver Townhomes for Sale | Kitsilano to Cambie', h1='Vancouver Townhomes for Sale', crumb='Vancouver townhomes',
               description='Search Vancouver townhomes for sale. Compare Kitsilano, Fairview, Cambie and Collingwood sold prices, days to sell and strata fees by complex.',
               links_h='More Vancouver real estate')
    bl = [P('This search lists townhomes for sale in the city of Vancouver: strata homes with their own front door, from Kitsilano and Fairview to Cambie and the East Side complexes. Houses and condos are separate searches.'),
          P(f'{tot} Vancouver townhomes closed in the year to {LAST}: {tw} in Vancouver West and {te} in Vancouver East, across {len(rows)} neighbourhoods. Kitsilano led with {kit["n"]} at {money(kit["price"])}, Fairview had {fv["n"]} at {money(fv["price"])}. '
            f'There is no one city median in the sold records, so each neighbourhood is shown on its own.'),
          {'t': 'grid', 'gen': G},
          H('Vancouver West townhomes'),
          P(f'These sell fast. Kitsilano townhomes took {kit["dom"]} days at a median and Fairview {fv["dom"]}, both under two weeks. Cambie is the newest and dearest of the larger groups: {cam["n"]} sales at {money(cam["price"])}, median built {cam["yb"]}, in {cam["dom"]} days. '
            f'University is the exception on fees at {money(uni["maint"])} a month.'),
          subtable('Townhomes sold in Vancouver West, by neighbourhood', rw, hub='vancouver-neighbourhood-guides', strata=True, lim=10),
          H('Vancouver East townhomes'),
          P(f'Prices on the East Side start near {money(chm["price"])} in Champlain Heights, where the median complex was built in {chm["yb"]} and homes took {chm["dom"]} days. Collingwood sold at {money(col["price"])} ({col["n"]} sales, built {col["yb"]}), Grandview Woodland at {money(gw["price"])} and Mount Pleasant East at {money(mp["price"])} in {mp["dom"]} days.'),
          subtable('Townhomes sold in Vancouver East, by neighbourhood', re_, hub='vancouver-neighbourhood-guides', strata=True, lim=9),
          qcounts('Vancouver townhomes sold, by period', qs),
          P(f'Sales ran {qs[0]} in November to January, {qs[1]} in February to April and {qs[2]} in May to July. The latest period to {LAST} has {qs[3]}.'),
          hpi_table('Townhouse benchmark price in Vancouver', [('Vancouver West', hw), ('Vancouver East', he)], 'gvr', SRC_GVR),
          *([H('Complexes that sold most'), btab] if len(allc) >= 3 else []),
          H('Buying a Vancouver townhome'),
          P('Most Vancouver townhomes are strata lots, so the strata’s minutes and depreciation report matter as much as the unit. The BC townhome buying rules page lists the documents. The Tenant Relocation and Protection Policy applies citywide to rented buildings that are redeveloped, and the Empty Homes Tax is 3% of assessed value for a home that is not occupied or rented.'),
          L([f'Check the age of the complex. Champlain Heights townhomes were built around {chm["yb"]} and Cambie around {cam["yb"]}.',
             f'Compare fees inside the same neighbourhood. The median ran from {money(col["maint"])} a month in Collingwood to {money(uni["maint"])} in University.',
             'Ask what parking comes with the unit.',
             'For a new complex, ask for the warranty details and the completion date.'])]
    faq = [('How much is a townhome in Vancouver?', f'Over the year to {LAST} the median was {money(kit["price"])} in Kitsilano, {money(fv["price"])} in Fairview, {money(cam["price"])} in Cambie and {money(col["price"])} in Collingwood. The townhouse benchmark was {money(hw["benchmark"])} in Vancouver West and {money(he["benchmark"])} in Vancouver East.'),
           ('Which Vancouver neighbourhood sells the most townhomes?', f'Kitsilano ({kit["n"]} sales), Fairview ({fv["n"]}), Mount Pleasant East ({mp["n"]}) and Cambie ({cam["n"]}).'),
           ('How fast do Vancouver townhomes sell?', f'Quickly on the West Side: {kit["dom"]} days in Kitsilano and {fv["dom"]} in Fairview. Champlain Heights is slower at {chm["dom"]}.'),
           ('What are strata fees for Vancouver townhomes?', f'Median fees ran from {money(col["maint"])} in Collingwood to {money(uni["maint"])} in University.'),
           ('How have townhome prices moved?', f'Over one year the benchmark moved {pct(hw["chg_1y"])} in Vancouver West and {pct(he["chg_1y"])} in Vancouver East.'),
           ('Are there new townhomes in Vancouver?', 'Yes. Cambie and Collingwood medians were built in 2024 and 2023. For projects not yet built, see the presale condos and townhomes page.')]
    links = [('Vancouver homes for sale', 'vancouver-homes-for-sale'), ('Vancouver houses for sale', 'vancouver-houses-for-sale'), ('Vancouver condos for sale', 'vancouver-condos-for-sale'),
             ('Vancouver presale condos and townhomes', 'vancouver-presale-condos-and-townhomes'), ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'),
             ('Vancouver market stats', 'vancouver-real-estate-market-stats'), ('BC townhome buying rules', 'bc-townhome-buying-rules'), ('Richmond townhomes for sale', 'richmond-townhomes-for-sale'),
             ('Burnaby townhomes for sale', 'burnaby-townhomes-for-sale'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return finish(slug, seo, [('Vancouver homes', 'vancouver-homes-for-sale')], faq, bl, 'Vancouver townhomes: your questions answered', links, dict(search_page=dict(kind='type', city='vancouver')))


# ================================================================== INBOUND, SEO, WORKSHEET
PAGES = [surrey_coach, cloverdale_coach, south_surrey_coach, burnaby_houses, coquitlam_houses, richmond_houses, richmond_condos, richmond_townhomes, vancouver_houses, vancouver_condos, vancouver_townhomes]
COACH = ['surrey-houses-with-coach-houses-for-sale', 'cloverdale-houses-with-coach-houses-for-sale', 'south-surrey-houses-with-coach-houses-for-sale']
RICH = ['richmond-houses-for-sale', 'richmond-condos-for-sale', 'richmond-townhomes-for-sale']
VAN = ['vancouver-houses-for-sale', 'vancouver-condos-for-sale', 'vancouver-townhomes-for-sale']
TITLE = {}
INBOUND = {
    'surrey-houses-for-sale': ('Surrey houses with a coach house', [(None, COACH[0]), (None, COACH[1]), (None, COACH[2])]),
    'cloverdale-houses-for-sale': ('Cloverdale houses with a coach house', [(None, COACH[1]), (None, COACH[0])]),
    'south-surrey-houses-for-sale': ('South Surrey houses with a coach house', [(None, COACH[2]), (None, COACH[0])]),
    'south-surrey-duplexes-with-suites-for-sale': ('Houses with a second home on the lot', [(None, COACH[2])]),
    'langley-houses-with-coach-houses-for-sale': ('Coach house searches in Surrey', [(None, c) for c in COACH]),
    'burnaby-homes-for-sale': ('Burnaby houses', [(None, 'burnaby-houses-for-sale')]),
    'coquitlam-homes-for-sale': ('Coquitlam houses', [(None, 'coquitlam-houses-for-sale')]),
    'richmond-homes-for-sale': ('Richmond by home type', [(None, s) for s in RICH]),
    'vancouver-homes-for-sale': ('Vancouver by home type', [(None, s) for s in VAN]),
    'richmond-neighbourhood-guides': ('Search all of Richmond by home type', [(None, s) for s in RICH]),
    'vancouver-neighbourhood-guides': ('Search all of Vancouver by home type', [(None, s) for s in VAN]),
    'burnaby-neighbourhood-guides': ('Search all Burnaby houses', [(None, 'burnaby-houses-for-sale')]),
    'coquitlam-neighbourhood-guides': ('Search all Coquitlam houses', [(None, 'coquitlam-houses-for-sale')]),
    'burnaby-condos-for-sale': ('Burnaby houses', [(None, 'burnaby-houses-for-sale')]),
    'coquitlam-condos-for-sale': ('Coquitlam houses', [(None, 'coquitlam-houses-for-sale')]),
}


def inbound():
    n = 0
    for host, (heading, pairs) in INBOUND.items():
        f = f'src/data/local/{host}.json'
        if not os.path.exists(f) and not os.path.exists(f'src/data/pages/{host}.json'): continue
        ind, asc, nl = 1, False, ''
        if os.path.exists(f):
            raw = open(f).read(); j = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
            line2 = raw.split('\n')[1] if '\n' in raw else ''
            ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
        else: j = {'status': 'generated', 'slug': host, 'updated': UPDATED, 'blocks': []}
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != LG]
        links = [[lk(TITLE[s], s)] for _, s in pairs if os.path.exists(f'src/data/local/{s}.json')]
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': heading, 'gen': LG, 'pos': 'end'}, {'t': 'list', 'items': links, 'gen': LG, 'pos': 'end'}]
        out = json.dumps(j, indent=ind, ensure_ascii=asc)
        open(f, 'w').write(out + nl); n += 1
    return n


BANNED_SEO = re.compile(r'sales ratio|snapstats|muse|top 1%|#1|!|…|604\.|\b(best|leading|trusted)\b', re.I)
def write_seo(made):
    f = 'tools/seo_final/fix_02.json'
    cur = json.load(open(f)) if os.path.exists(f) else {}
    for j in made:
        s, np_ = j['slug'], j['new_page']
        e = dict(title=np_['title'], h1=np_['h1'], description=np_['description'])
        assert 38 <= len(e['title']) <= 60, (s, 'title', len(e['title']), e['title'])
        assert 20 <= len(e['h1']) <= 60 and '|' not in e['h1'], (s, 'h1', len(e['h1']))
        assert 135 <= len(e['description']) <= 158 and e['description'].endswith('.'), (s, 'description', len(e['description']), e['description'])
        assert not BANNED_SEO.search(e['title'] + e['description']) and 'REALTOR' not in e['title'], s
        cur[s] = e
    assert len({v['title'] for v in cur.values()}) == len(cur) and len({v['description'] for v in cur.values()}) == len(cur)
    json.dump(cur, open(f, 'w'), indent=1, ensure_ascii=False)


def write_xlsx(made):
    import openpyxl
    from openpyxl.styles import Font, Alignment
    AREA = {'surrey': 'Surrey + North Surrey', 'cloverdale': 'Cloverdale', 'south-surrey': 'South Surrey White Rock', 'burnaby': 'Burnaby North + Burnaby South + Burnaby East', 'coquitlam': 'Coquitlam',
            'richmond': 'Richmond', 'vancouver': 'Vancouver West + Vancouver East'}
    TYPE = {'houses': 'House/Single Family', 'condos': 'Apartment/Condo', 'townhomes': 'Townhouse'}
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'New searches'
    head = ['Page slug', 'Page heading', 'Page URL', 'Search name to save in MyRealPage', 'MLS area', 'Sub-area filter', 'Property type (Type of Dwelling)', 'Other filters', 'Price filter', 'Status', 'Search ID (Jerry fills)', 'Embed code (Jerry fills)']
    ws.append(head)
    for j in made:
        s = j['slug']; sp = j['search_page']; city = sp['city']
        if sp['kind'] == 'coach':
            cityname = {'surrey': 'Surrey', 'cloverdale': 'Cloverdale', 'south-surrey': 'South Surrey'}[city]
            name = f'COACH {cityname} House with Coach House'; typ = TYPE['houses']
            other = 'Coach house / carriage house feature: copy the saved search "Langley Houses with Coach Houses for Sale" (search ID 1450209) and change only the area. Confirm the field name in MyRealPage.'
        else:
            kind = s.split('-')[1]; cityname = city.capitalize(); name = f'TYPE {cityname} {kind.capitalize()}'; typ = TYPE[kind]; other = '(none)'
        sub = 'Exclude sub-area: White Rock' if city == 'south-surrey' else '(none)'
        ws.append([s, j['new_page']['h1'], f'https://jaredgibbons.ca/{s}.html', name, AREA[city], sub, typ, other, '(none)', 'Active', '', ''])
    for c in ws[1]: c.font = Font(bold=True)
    for col, w in zip('ABCDEFGHIJKL', (46, 44, 56, 38, 40, 28, 28, 70, 12, 10, 22, 60)): ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes = 'A2'
    nt = wb.create_sheet('Notes')
    for line in ['Same set-up as the bedroom searches: one saved MyRealPage search per row, noframe template, then send the search ID and embed code back.',
                 'Filters: Status Active. Type of Dwelling as shown. No price filter, no age filter, no bedroom filter.',
                 'Surrey = the Surrey and North Surrey board areas only; Cloverdale and South Surrey have their own rows.',
                 'South Surrey = South Surrey White Rock without the White Rock sub-area.',
                 'Burnaby = Burnaby North, Burnaby South and Burnaby East together. Vancouver = Vancouver West and Vancouver East together.',
                 'Coach house rows: the old Langley coach house search (ID 1450209) already has the filter. Clone it and change the area. I could not confirm the exact field name from the repo, so please check it on the first one.',
                 f'{len(made)} searches. All pages stay in draft until the search IDs are in.']:
        nt.append([line])
    nt.column_dimensions['A'].width = 150
    os.makedirs('docs/review/idx', exist_ok=True)
    wb.save('docs/review/idx/new-searches-2026-11-06.xlsx')


if __name__ == '__main__':
    made = [f() for f in PAGES]
    for j in made: TITLE[j['slug']] = j['new_page']['h1']
    print(len(made), 'pages;', inbound(), 'inbound link blocks')
    write_seo(made)
    if '--xlsx' in sys.argv: write_xlsx(made); print('worksheet written')
