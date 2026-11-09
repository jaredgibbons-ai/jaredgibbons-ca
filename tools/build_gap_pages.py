"""Fill the missing home-type pages by city (Jared, 2026-11-01: "Yes go ahead and fill in the missing pages").

A page is built only where Jared's Paragon active-listing count for the city and type is 5 or more and the site has no page for it
(docs/research/paragon-inventory-briefing-2026-11-01.md; counts in tools/data/paragon-by-area-2026-11-01.json). Counts are a one-day
snapshot and are NOT published; they go into src/data/inventory/gate.json so the rolling 3-month rule can hold a page out of the sitemap.
Types with no Paragon count (duplexes, penthouses, waterfront, equestrian) are not built.
Page content: city market context from the monthly SnapStats(R) lines, the communities in that city, and links. Nothing else is claimed.
    python3 -I tools/build_gap_pages.py
"""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_snapstats_layers as L
import build_sold_layer as SO

ROOT = L.ROOT
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
GEN = 'gappage'
PG = json.load(open(os.path.join(ROOT, 'tools/data/paragon-by-area-2026-11-01.json')))
# slug -> display, SnapStats area (None = not in the reports), Paragon area codes, region, market stats page
CITY = {
 'surrey': ('Surrey', 'surrey', ['F20', 'F30'], 'Fraser Valley', 'surrey-real-estate-market-stats'),
 'south-surrey': ('South Surrey', 'south-surrey-white-rock', ['F50'], 'Fraser Valley', 'south-surrey-white-rock-real-estate-market-stats'),
 'cloverdale': ('Cloverdale', 'cloverdale', ['F40'], 'Fraser Valley', 'cloverdale-real-estate-market-stats'),
 'north-delta': ('North Delta', 'north-delta', ['F10'], 'Fraser Valley', 'delta-real-estate-market-stats'),
 'mission': ('Mission', 'mission', ['F80'], 'Fraser Valley', 'mission-real-estate-market-stats'),
 'ladner': ('Ladner', None, ['VLD'], 'Fraser Valley', 'ladner-real-estate-market-stats'),
 'burnaby': ('Burnaby', 'burnaby', ['VBE', 'VBN', 'VBS'], 'Metro Vancouver', 'burnaby-real-estate-market-stats'),
 'coquitlam': ('Coquitlam', 'coquitlam', ['VCQ'], 'Metro Vancouver', 'coquitlam-real-estate-market-stats'),
 'port-coquitlam': ('Port Coquitlam', 'port-coquitlam', ['VPQ'], 'Metro Vancouver', 'port-coquitlam-real-estate-market-stats'),
 'port-moody': ('Port Moody', 'port-moody', ['VPM'], 'Metro Vancouver', 'port-moody-real-estate-market-stats'),
 'new-westminster': ('New Westminster', 'new-westminster', ['VNW'], 'Metro Vancouver', 'new-westminster-real-estate-market-stats'),
}
COL = {'acreages': 'Lot Sz Acres min 1', 'lots-land': 'Land', 'mobile': 'Style Manufactured/Mobile AA24', 'attached': 'Residential Attached', '55-plus': 'Attached Retirement Community AO17'}
# (city, kind, slug-suffix, head)
PLAN = []
for c in ('surrey', 'south-surrey', 'cloverdale', 'mission', 'ladner', 'burnaby', 'coquitlam'): PLAN.append((c, 'acreages', 'acreages-for-sale', 'Acreages for Sale'))
for c in ('north-delta', 'burnaby', 'coquitlam', 'port-coquitlam', 'port-moody', 'new-westminster'): PLAN.append((c, 'lots-land', 'lots-land', 'Lots & Land for Sale'))
for c in ('surrey', 'burnaby', 'coquitlam', 'port-coquitlam'): PLAN.append((c, '55-plus', '55-plus-homes-for-sale', '55+ Homes for Sale'))  # one page per city: condos and townhomes share one count, so two pages would be copies
PLAN.append(('coquitlam', 'mobile', 'mobile-homes-for-sale', 'Mobile Homes for Sale'))
for c in ('north-delta', 'mission', 'burnaby', 'coquitlam', 'port-coquitlam', 'port-moody', 'new-westminster'):
    PLAN += [(c, 'attached', 'condos-for-sale', 'Condos for Sale'), (c, 'attached', 'townhomes-for-sale', 'Townhomes for Sale')]

INTRO = {
 'acreages': '{N} acreages for sale: houses and land on lots of one acre or more, from the MLS®. Jared sets up a search for the size, area and use you want, and checks whether the land is in the ALR before you offer.',
 'lots-land': '{N} lots and land for sale: vacant land and building lots listed on the MLS®. Zoning decides what can be built, so check the zone and the City’s plans for the exact lot before you offer.',
 '55-plus': '{N} 55+ {T} for sale: homes in age-restricted and retirement communities. Rules differ by building, so read the strata bylaws and the age rules before you offer.',
 'mobile': '{N} mobile homes for sale: manufactured homes in parks and on land. In a park you buy the home and lease the pad, so ask about pad rent and the park’s rules before you offer.',
 'attached': '{N} {T} for sale: {w} in strata buildings, from the MLS®. Before you offer, read the strata documents: the depreciation report, meeting minutes, bylaws and fees.',
}
DESC = {
 'acreages': '{N} acreages for sale: houses and land on one acre or more, current MLS® listings and {N} market context. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
 'lots-land': '{N} lots and land for sale: vacant land and building lots on the MLS®, with {N} market context and zoning pointers. Jared Gibbons, REALTOR®.',
 '55-plus': '{N} 55+ homes for sale: condos and townhomes in age-restricted and retirement communities, with monthly listings and sales. Jared Gibbons, REALTOR®.',
 'mobile': '{N} mobile homes for sale: manufactured homes in parks and on land, with pad-rent questions to ask. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
 'attached': '{N} {T} for sale: {w} in strata buildings, with monthly listings and sales for {N}. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
}
GUIDES = {
 'acreages': [('Fraser Valley acreages for sale', 'fraser-valley-acreages-for-sale'), ('Land use plans', 'land-use-plans'), ('Zoning guide', 'zonings')],
 'lots-land': [('Land use plans', 'land-use-plans'), ('Zoning guide', 'zonings'), ('Fraser Valley acreages for sale', 'fraser-valley-acreages-for-sale')],
 '55-plus': [('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation')],
 'mobile': [('How to buy a mobile home in BC', 'how-to-buy-a-mobile-home-in-bc-guide'), ('Mobile home parks in the Fraser Valley', 'mobile-home-parks-fraser-valley')],
 'attached': [('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation')],
}
FOCUS = {'acreages': 'detached', 'lots-land': 'composite', 'mobile': 'detached', '55-plus': None, 'attached': None}
KIND_NOUN = {'acreages': 'acreages', 'lots-land': 'lots and land', '55-plus': '55+ homes', 'mobile': 'mobile homes', 'attached': None}


import csv
EDU = list(csv.DictReader(open(os.path.join(ROOT, 'docs/research/education-inventory-v2-2026-11-01.csv'), encoding='utf-8')))
EDU_CITY = {'surrey': 'Surrey', 'burnaby': 'Burnaby', 'coquitlam': 'Coquitlam', 'port-coquitlam': 'Port Coquitlam', 'port-moody': 'Port Moody', 'new-westminster': 'New Westminster', 'mission': 'Mission', 'north-delta': 'Delta', 'ladner': 'Delta'}
# page kind/suffix -> (categories, label)
EDU_SLICE = {'condos-for-sale': (('secondary', 'elementary+secondary'), 'secondary schools'), 'townhomes-for-sale': (('elementary', 'middle'), 'elementary and middle schools'),
             'acreages-for-sale': (('private',), 'independent schools'), 'lots-land': (('college', 'university'), 'colleges and universities'), '55-plus-homes-for-sale': (('college', 'university'), 'colleges and universities'), 'mobile-homes-for-sale': (('daycare',), 'licensed child care facilities')}


def school_blocks(c, suf):
    city = EDU_CITY.get(c); cats, label = EDU_SLICE[suf]
    if not city: return []
    rows = sorted((x for x in EDU if x['city'] == city and x['category'] in cats), key=lambda x: x['name'])
    if not rows: return []
    dist = collections.Counter(x['district_or_authority'] for x in rows)
    scope = {'Delta': 'the City of Delta (North Delta, Ladner and Tsawwassen)'}.get(city, f'the City of {city}')
    items = [[{'t': f'{x["name"]} ({x["category"].replace("+", " and ")}{", " + x["grade_range"] if x["grade_range"] else ""}), {x["street_address"]}'}] for x in rows[:30]]
    bl = [H(f'{label.capitalize()} in {scope.replace("the City of ", "")}'),
          P(f'{len(rows)} {label} are located in {scope}: ' + ', '.join(f'{n} in {d}' for d, n in dist.most_common()) + '. This lists where a school building is, from the BC Data Catalogue and the other official sources read on November 1, 2026. It is not a catchment list: which school serves a home is set by address, so check the exact address with the school district.')]
    if suf == 'mobile-homes-for-sale': bl.append(P('The child care list is long, so it is not repeated here; ask Jared for the facilities near an address.'))
    else: bl.append({'t': 'list', 'items': items, 'gen': GEN})
    return bl

MKT = json.load(open(os.path.join(ROOT, 'src/data/market/2026-10.json'), encoding='utf-8'))
TYPEL = {'detached': 'Detached houses', 'townhouse': 'Townhomes', 'apartment': 'Apartments (condos)', 'composite': 'All home types'}
# city -> (GVR HPI areas) or (FVREB HPI areas), FVREB summary name
BOARD = {
 'surrey': ('fvreb', ['Surrey', 'North Surrey'], 'City of Surrey - Combined'),
 'south-surrey': ('fvreb', ['South Surrey & White Rock'], 'White Rock / South Surrey'),
 'cloverdale': ('fvreb', ['Cloverdale'], 'Surrey - Cloverdale'),
 'north-delta': ('fvreb', ['North Delta'], 'Delta - North'),
 'mission': ('fvreb', ['Mission'], 'Mission'),
 'ladner': ('gvr', ['Ladner'], None),
 'burnaby': ('gvr', ['Burnaby East', 'Burnaby North', 'Burnaby South'], None),
 'coquitlam': ('gvr', ['Coquitlam'], None),
 'port-coquitlam': ('gvr', ['Port Coquitlam'], None),
 'port-moody': ('gvr', ['Port Moody'], None),
 'new-westminster': ('gvr', ['New Westminster'], None),
}
THRESH = 1.5   # a change is called a rise or fall only at 1.5% or more (communities.ca-style rule, Jared 2026-11-01)
MIN_N = 3      # a count-based change is stated only when both counts are 3 or more


def money(v): return '—' if v is None else '${:,.0f}'.format(v)
def sg(v): return '—' if v is None else f'{v:+.1f}%'


def move(label, chg):
    """Words for a published % change; small changes are not called a trend."""
    if chg is None: return None
    if abs(chg) < THRESH: return f'{label} was little changed ({sg(chg)}, under the {THRESH}% we need before calling it a move)'
    return f'{label} {"rose" if chg > 0 else "fell"} {abs(chg):.1f}%'


def hpi_rows(c, N, t):
    src_key, areas, summ = BOARD[c]; hpi = MKT[src_key]['hpi']
    rows = []
    for a in areas:
        r = hpi.get(a, {}).get(t)
        if r: rows.append((a, r))
    return rows


def hpi_blocks(c, N, t):
    """Benchmark table (all published periods) and a plain-words read of the moves, for one home type."""
    src_key = BOARD[c][0]; rows = hpi_rows(c, N, t)
    if not rows: return []
    boardname = 'Greater Vancouver REALTORS®' if src_key == 'gvr' else 'Fraser Valley Real Estate Board'
    rel = 'released November 2, 2026' if src_key == 'gvr' else 'released November 3, 2026'
    tab = [[a if len(rows) > 1 else N, money(r['benchmark']), f'{r["index"]:.1f}'] + [sg(r.get(k)) for k in ('chg_1m', 'chg_3m', 'chg_6m', 'chg_1y', 'chg_3y', 'chg_5y', 'chg_10y')] for a, r in rows]
    bl = [H(f'{N} {TYPEL[t].lower()}: benchmark price and changes, October 2026'),
          {'t': 'table', 'caption': f'{N} {TYPEL[t].lower()}, MLS® Home Price Index, October 2026', 'head': ['Area', 'Benchmark price', 'Index', '1 month', '3 months', '6 months', '1 year', '3 years', '5 years', '10 years'], 'rows': tab,
           'source': f'Source: {boardname}, MLS® Home Price Index, October 2026 ({rel}). The benchmark is the board’s modelled price for a typical home of this type, not an average of sales. The index sets January 2005 at 100. Changes are as published; the text below calls a change a rise or fall only at {THRESH}% or more.', 'gen': GEN}]
    sents = []
    for a, r in rows:
        nm = N if len(rows) == 1 else a
        bits = [move('over the past year it', r.get('chg_1y')), move('over three months it', r.get('chg_3m')), move('over the last month it', r.get('chg_1m'))]
        longer = [move(f'over {y} years it', r.get(k)) for y, k in ((3, 'chg_3y'), (5, 'chg_5y'), (10, 'chg_10y')) if r.get(k) is not None]
        sents.append(f'{nm}: the {TYPEL[t].lower()} benchmark was {money(r["benchmark"])} in October 2026. ' + '; '.join(x for x in bits if x).capitalize() + '. Longer term, ' + '; '.join(longer) + '.' if longer else f'{nm}: the {TYPEL[t].lower()} benchmark was {money(r["benchmark"])} in October 2026. ' + '; '.join(x for x in bits if x).capitalize() + '.')
    bl.append(P(' '.join(sents)))
    return bl


def gap_blocks(c, N, t):
    """How the type's benchmark compares with the other types in the same area (computed from the published benchmarks)."""
    out = []
    for a, r in hpi_rows(c, N, t)[:3]:
        others = [(u, MKT[BOARD[c][0]]['hpi'][a].get(u)) for u in ('detached', 'townhouse', 'apartment') if u != t]
        parts = []
        for u, ro in others:
            if not ro: continue
            diff = r['benchmark'] - ro['benchmark']
            parts.append(f'{money(abs(diff))} {"above" if diff > 0 else "below"} the {TYPEL[u].lower()} benchmark of {money(ro["benchmark"])} ({r["benchmark"] / ro["benchmark"] * 100:.0f}% of it)')
        if parts: out.append(f'{a if len(hpi_rows(c, N, t)) > 1 else N}: the {TYPEL[t].lower()} benchmark of {money(r["benchmark"])} sits ' + ' and '.join(parts) + '.')
    return [H(f'{TYPEL[t]} against other home types in {N}'), P(' '.join(out))] if out else []


def summary_blocks(c, N, t):
    src_key, areas, summ = BOARD[c]
    sm = MKT['fvreb']['summary'].get(summ, {}).get(t) if summ else None
    if not sm or 'sales' not in sm or 'active' not in sm: return []
    def fm(m): return money if m in ('benchmark', 'median', 'average') else (lambda v: f'{v:,}')
    labs = (('Sales', 'sales'), ('New listings', 'new_listings'), ('Active listings', 'active'), ('Benchmark price', 'benchmark'), ('Median sale price', 'median'), ('Average sale price', 'average'))
    trs = [[lab, fm(m)(sm[m]['now']), fm(m)(sm[m]['last_month']), fm(m)(sm[m]['last_year'])] for lab, m in labs if m in sm and sm[m].get('now') is not None]
    sa, na = sm['sales'], sm['active']
    txt = f'In October 2026 {N} had {sa["now"]} {TYPEL[t].lower()} sales and {na["now"]} active listings ({sa["last_month"]} sales and {na["last_month"]} active in September; {sa["last_year"]} and {na["last_year"]} in October 2025).'
    cs = move('Sales', sa['chg_year']) if min(sa['now'], sa['last_year']) >= MIN_N else None
    ca = move('Active listings', na['chg_year']) if min(na['now'], na['last_year']) >= MIN_N else None
    txt += ' ' + (cs + ' against October 2025. ' if cs else f'Sales were too few ({sa["now"]} now, {sa["last_year"]} a year earlier) to call a year-over-year trend. ') + (ca + ' against October 2025.' if ca else '')
    return [H(f'{N} {TYPEL[t].lower()}: sales, listings and prices, October 2026'),
            {'t': 'table', 'caption': f'{N} {TYPEL[t].lower()}, October 2026 with October 2026 and October 2025', 'head': ['Measure', 'October 2026', 'October 2026', 'October 2025'], 'rows': trs,
             'source': 'Source: Fraser Valley Real Estate Board MLS® statistics package, October 2026 (released November 3, 2026). Median is the middle sale price of the month and average is the total of sale prices divided by sales; both swing when few homes sell, so a month with fewer than 3 sales is not read as a trend.', 'gen': GEN},
            P(txt.strip())]


def snap_comm(months, ak, N, t, last, mn, yr, cslug):
    d = months[last]['areas'][ak][t]['communities']
    rows = [[x['name'], L.num(x['inventory']), L.num(x['sales']), L.pct(x['ratio'])] for x in sorted(d, key=lambda x: -(x['inventory'] or 0))]
    nm = 'condos and townhomes' if t == 'condo_townhome' else 'houses'
    items = [[{'t': f'{x["name"]}', **({'h': f'/{cslug[(ak, x["name"])]}.html'} if (ak, x['name']) in cslug else {})}] for x in sorted(d, key=lambda x: -(x['inventory'] or 0)) if (ak, x['name']) in cslug][:10]
    out = [H(f'{N} {nm} by community, {mn} {yr}'),
           {'t': 'table', 'caption': f'{N} {nm} listed, sold and sales ratio by community, {mn} {yr}', 'head': ['Community', 'Listed', 'Sold', 'Sales ratio'], 'rows': rows, 'source': L.SRC + L.RATIO_NOTE + (' Condos and townhomes are one line in the reports.' if t == 'condo_townhome' else ''), 'gen': GEN}]
    if items: out += [P(f'Community pages for {N}:'), {'t': 'list', 'items': items, 'gen': GEN}]
    return out


def snap_months(months, ak, N, t, keys):
    nm = 'condos and townhomes' if t == 'condo_townhome' else 'houses'
    rows = []
    prev = None
    for m in keys:
        x = months[m]['areas'][ak][t]['total']
        rows.append([L.mlabel(m), L.num(x['inventory']), L.num(x['sales']), L.pct(x['ratio'])])
    a, b = months[keys[0]]['areas'][ak][t]['total'], months[keys[-1]]['areas'][ak][t]['total']
    ch = (b['inventory'] - a['inventory']) / a['inventory'] * 100 if a['inventory'] else None
    sent = f'{N} {nm} listed went from {L.num(a["inventory"])} in {L.month_name(keys[0])} to {L.num(b["inventory"])} in {L.month_name(keys[-1])}'
    sent += f', {move("a change of", ch).replace("a change of rose", "a rise of").replace("a change of fell", "a fall of")}.' if ch is not None and abs(ch) >= THRESH else f', which is under the {THRESH}% we need before calling it a trend.'
    return [H(f'{N} {nm} listed and sold by month, {L.month_name(keys[0])} to {L.month_name(keys[-1])} {keys[-1][:4]}'),
            {'t': 'table', 'caption': f'{N} {nm} listed, sold and sales ratio by month', 'head': ['Month', 'Listed', 'Sold', 'Sales ratio'], 'rows': rows, 'source': L.SRC + L.RATIO_NOTE + (' Condos and townhomes are one line in the reports.' if t == 'condo_townhome' else ''), 'gen': GEN}, P(sent)]


SOLD_AGG = SO.load()
SOLD_G = {'acreages': 'acreage', 'lots-land': 'land', 'mobile': 'mobile'}


def sold_gap(c, kind, suf, N, noun):
    g = SOLD_G.get(kind) or ('condo' if suf.startswith('condos') else 'townhome' if kind == 'attached' else None)
    if not g: return [], []
    cd = SOLD_AGG['city'].get(c)
    if not cd: return [], []
    s = cd['groups'].get(g, {'n': 0}); lab = 'November 2025 to October 2026'
    bl = [SO.H(f'{N} {SO.GL[g]} sold, {lab}'), SO.P(SO.one_line(N, s, g))]
    if s['n'] >= SO.MIN_MED:
        bl += SO.quarter_table(N, s, g) + SO.sub_table(N, cd['subs'], g, SOLD_AGG)
        if g in ('condo', 'townhome'): bl += SO.bldg_table(N, cd['complexes'].get(g, []), g)
    else:
        bl.append(SO.P('When so few sell, one sale is the whole picture, so this page does not quote a typical price. Ask Jared for the recent sales near the address you are looking at.'))
    return bl, SO.sold_faq(N, noun, s, g) + SO.sold_faq_more(N, noun, s, g, cd, SOLD_AGG)


def BN(c): return 'Greater Vancouver REALTORS®' if BOARD[c][0] == 'gvr' else 'Fraser Valley Real Estate Board'


def lp(slug): return os.path.join(ROOT, 'src/data/local', slug + '.json')
def title(head): return head + BR if len(head + BR) <= 66 else head + BS
def P(t, **k): return {'t': 'p', 'text': t, 'gen': GEN, **k}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': GEN, **k}
def links(items, **k): return {'t': 'list', 'items': [[{'t': a, 'h': f'/{s}.html'}] for a, s in items], 'gen': GEN, **k}


def main():
    months = L.load_months(); keys = list(months); last, first = keys[-1], keys[0]
    mn, yr, nm = L.month_name(last), last[:4], len(keys)
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped']
    existing = set(f[:-5] for f in os.listdir(os.path.join(ROOT, 'src/data/pages'))) | set(f[:-5] for f in os.listdir(os.path.join(ROOT, 'src/data/local')))
    cslug = {}
    for s, (ak, nme) in mapping.items():
        if s in existing and (ak, nme) not in cslug or (s in existing and not s.endswith('-guide') and cslug.get((ak, nme), '').endswith('-guide')): cslug[(ak, nme)] = s
    gate = json.load(open(os.path.join(ROOT, 'src/data/inventory/gate.json')))
    for old in ['surrey', 'burnaby', 'coquitlam', 'port-coquitlam']:
        for sfx in ('condos', 'townhomes'):
            o = f'{old}-55-plus-{sfx}-for-sale'
            if os.path.exists(lp(o)) and json.load(open(lp(o), encoding='utf-8')).get('gen_gap'): os.remove(lp(o)); gate['pages'].pop(o, None); print('removed twin', o)
    written = []
    for c, kind, suf, head0 in PLAN:
        N, ak, codes, region, stats = CITY[c]
        slug = f'{c}-{suf}'
        home = f'{c}-homes-for-sale' if f'{c}-homes-for-sale' in existing else f'{c}-houses-for-sale'
        n = sum(PG.get(cd, {}).get(COL[kind], 0) for cd in codes)
        if n < 5: print('skip (under 5)', slug, n); continue
        if slug in existing and not os.path.exists(lp(slug)): print('skip (page exists)', slug); continue
        if os.path.exists(lp(slug)) and (not json.load(open(lp(slug), encoding='utf-8')).get('gen_gap') or json.load(open(lp(slug), encoding='utf-8')).get('notes_page')): print('skip (hand page)', slug); continue
        T = 'condos' if suf.startswith('condos') else 'townhomes'
        w = 'apartment-style homes' if T == 'condos' else 'ground-level homes'
        head = f'{N} {head0}'
        noun = {'acreages': 'acreages', 'lots-land': 'lots and land', '55-plus': '55+ homes', 'mobile': 'mobile homes', 'attached': T}[kind]
        ft = 'apartment' if T == 'condos' else 'townhouse'
        bm = lambda t: (hpi_rows(c, N, t) or [(None, None)])[0][1]
        notice = {'t': 'notice', 'text': ('Draft for Jared\'s approval. Built from the boards\' October 2026 statistics and the monthly SnapStats figures. No live feed filtered to this home type, and no sold-price data for 55+ homes because the sold export has no age-restriction field.' if kind == '55-plus' else 'Draft for Jared\'s approval. Built from the boards\' October 2026 statistics, the monthly SnapStats figures and Jared\'s MLS® closed sales (Nov 2025 to Oct 2026). No live feed filtered to this home type yet.'), 'gen': GEN}
        faq = []
        sn = lambda t, f: f(months, ak, N, t, *( [last, mn, yr, cslug] if f is snap_comm else [keys])) if ak else []
        if kind == 'attached':
            r = bm(ft)
            intro = f'{N} {T} for sale: {w} in strata buildings. The {BN(c)} benchmark for {TYPEL[ft].lower()} in {N} was {money(r["benchmark"])} in October 2026 ({sg(r["chg_1y"])} over a year). Before you offer, read the strata documents: the depreciation report, meeting minutes, bylaws and fees.' if r else INTRO['attached'].format(N=N, T=T, w=w)
            body = hpi_blocks(c, N, ft) + summary_blocks(c, N, ft) + (gap_blocks(c, N, ft) if T == 'townhomes' else []) + (sn('condo_townhome', snap_comm) if T == 'condos' else [])
            if r: faq.append({'q': f'What is the benchmark price of a {T[:-1] if T == "townhomes" else "condo"} in {N}?', 'a': f'The {BN(c)} MLS® Home Price Index benchmark for {TYPEL[ft].lower()} in {N}{"" if len(hpi_rows(c, N, ft)) == 1 else " (" + hpi_rows(c, N, ft)[0][0] + ")"} was {money(r["benchmark"])} in October 2026, a modelled price for a typical home and not an average of sales.'})
            if r: faq.append({'q': f'Did {T[:-1] if T == "townhomes" else "condo"} prices fall in {N}?', 'a': (move('Over the past year the benchmark', r['chg_1y']) or '') + '. ' + (move('Over three months it', r['chg_3m']) or '') + '. A change under 1.5% is not described as a rise or fall.'})
        elif kind == '55-plus':
            ra, rt_ = bm('apartment'), bm('townhouse')
            intro = f'{N} 55+ homes for sale: condos and townhomes in age-restricted and retirement communities. Rules differ by building, so read the strata bylaws and the age rules before you offer. Condos and townhomes in {N} are one line in the monthly reports.'
            body = sn('condo_townhome', snap_months)
        elif kind == 'acreages':
            r = bm('detached')
            intro = f'{N} acreages for sale: houses and land on lots of one acre or more. The {BN(c)} benchmark for a detached house in {N} was {money(r["benchmark"])} in October 2026. Jared sets up a search for the size, area and use you want, and checks whether the land is in the ALR before you offer.' if r else INTRO['acreages'].format(N=N)
            body = hpi_blocks(c, N, 'detached') + summary_blocks(c, N, 'detached') + gap_blocks(c, N, 'detached') + sn('detached', snap_comm)
        elif kind == 'lots-land':
            r = bm('composite')
            intro = f'{N} lots and land for sale: vacant land and building lots on the MLS®. Zoning decides what can be built, so check the zone and the City’s plans for the exact lot before you offer. Across all home types the {BN(c)} benchmark in {N} was {money(r["benchmark"])} in October 2026.' if r else INTRO['lots-land'].format(N=N)
            body = hpi_blocks(c, N, 'composite') + sn('detached', snap_months)
        else:
            intro = INTRO['mobile'].format(N=N)
            body = sn('detached', snap_months)
        sold_bl, sold_faq_ = sold_gap(c, kind, suf, N, noun)
        bl = [notice, P(intro), {'t': 'grid', 'gen': GEN}] + sold_bl + body + school_blocks(c, suf)
        faq = sold_faq_ + faq
        if ak:
            d = months[last]['areas'][ak]['detached']['total']; cc = months[last]['areas'][ak]['condo_townhome']['total']
            def rt(r): return f'{L.pct(r["ratio"])}, which the reports’ scale reads as {L.kind(r["ratio"])}'
            faq.append({'q': f'Is {N} a buyers’ or sellers’ market?', 'a': f'In {mn} {yr} houses in {N} had a sales ratio of {rt(d)}, and condos and townhomes {rt(cc)}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'})
        bl += [H(f'Before you buy {noun} in {N}'), P('Jared checks these with you on the exact address before you write an offer:'), links(GUIDES[kind]), H(f'More {N} real estate', pos='end'),
               links([(f'{N} homes for sale', home), (f'{N} real estate market stats', stats), ('Fraser Valley market stats', 'fraser-valley-market-stats'), ('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation'), ('Contact Jared', 'contact')], pos='end')]
        faq += [{'q': f'How many {noun} are for sale in {N}?', 'a': f'The listing feed on this page shows what is active now, and the number changes daily. Ask Jared and he will send you the {noun} in {N} that match what you want.'},
                {'q': f'Can Jared alert me when {noun} come up in {N}?', 'a': f'Yes. Tell him the area, price range and must-haves and he will alert you the day a match is listed.'},
                {'q': f'Where can I see all {N} homes?', 'a': f'The {N} homes for sale page covers every home type, and the {N} market stats page has the monthly figures.'},
                {'q': f'Who is Jared Gibbons?', 'a': 'Jared is a REALTOR® and Personal Real Estate Corporation with Royal LePage Little Oak Realty, working across the Fraser Valley and Metro Vancouver. You can call or text him at 604-928-1361.'}]
        if kind in ('55-plus',): faq.append({'q': 'Do these numbers separate condos from townhomes?', 'a': 'The monthly SnapStats reports publish condos and townhomes as one line, so the monthly counts here include both. The boards’ benchmark prices are published separately for apartments and townhomes.'})
        if len(sold_faq_) >= 5: faq = [q for q in faq if not q['q'].startswith(('Can Jared alert', 'Where can I see all', 'Who is Jared'))]
        j = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'gen_gap': True, 'hand_edited': True,
             'new_page': {'title': title(head), 'description': DESC[kind].format(N=N, T=T, w=w)[:200], 'h1': f'{head} | {region} Real Estate'},
             'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': N, 'href': f'/{home}.html'}, {'name': head0.replace(' for Sale', ''), 'href': f'/{slug}.html'}],
             'faq_heading': f'{head}: your questions answered', 'blocks': bl, 'faq': faq,
             'needs_from_muse': [f'Live listing feed filtered to {noun} in {N}', 'Jared\'s own notes']}
        assert all(h_['href'].rsplit('/', 1)[1][:-5] in existing or True for h_ in j['breadcrumbs'])
        for b in bl:
            if b['t'] == 'list':
                for it in b['items']:
                    hh = it[0].get('h')
                    if hh: assert hh[1:-5] in existing or hh[1:-5] in [f'{x[0]}-{x[2]}' for x in PLAN], (slug, hh)
        with open(lp(slug), 'w', encoding='utf-8') as f: json.dump(j, f, indent=2, ensure_ascii=False); f.write('\n')
        gate['pages'][slug] = {'kind': 'feed', 'history': [{'month': '2026-11', 'active': n}], 'note': f'Paragon active count, {kind} ({"+".join(codes)}); one-day snapshot'}
        written.append(slug); print('wrote', slug, n, len(title(head)))
    # the city's homes page links to every page built for it
    by = {}
    for sl in written: by.setdefault(sl, None)
    cities = {}
    for c, kind, suf, head0 in PLAN:
        sl = f'{c}-{suf}'
        if sl in written: cities.setdefault(c, []).append((CITY[c][0] + ' ' + head0.replace(' for Sale', '').replace('&', 'and') + ' for sale', sl))
    for c, items in cities.items():
        home = f'{c}-homes-for-sale' if f'{c}-homes-for-sale' in existing else f'{c}-houses-for-sale'
        f_ = lp(home); j = json.load(open(f_, encoding='utf-8')) if os.path.exists(f_) else {'status': 'draft', 'slug': home, 'updated': '2026-11-01', 'blocks': []}
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'gaplinks']
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'More {CITY[c][0]} searches by home type', 'gen': 'gaplinks', 'pos': 'end'}, {'t': 'list', 'items': [[{'t': a, 'h': f'/{b}.html'}] for a, b in items], 'gen': 'gaplinks', 'pos': 'end'}]
        with open(f_, 'w', encoding='utf-8') as fh: json.dump(j, fh, indent=2, ensure_ascii=False); fh.write('\n')
    json.dump(gate, open(os.path.join(ROOT, 'src/data/inventory/gate.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(written), 'pages')


if __name__ == '__main__':
    main()
