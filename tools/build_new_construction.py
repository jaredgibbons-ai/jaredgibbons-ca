#!/usr/bin/env python3
"""New-construction pages (gen 'nc'): one live MyRealPage search per city, filter "Age 0 or less" (worksheet 'New construction searches', Nov 4 2026).

 * 13 new pages /new-construction-<city>.html  (new_page header, own copy)
 * 7 existing presale pages + the hub get a short "New homes on the MLS® now" section with the search, plus the two data tables.
Numbers come only from files in the repo: Paragon closed-sales aggregate (src/data/sold/sold-12m.json, aggregates only, a figure only where 5 or more sold, a name
only where 3 or more) and the presale list (src/data/presale/2026-11-01.json, prices only where the source dates them within three months).
Live listing counts are NOT published on pages (they change daily). Tax thresholds are not repeated here; pages link to the guides that carry the sourced figures.
Idempotent: removes only its own gen blocks.   python3 -I tools/build_new_construction.py
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'nc'; LG = 'nclinks'
SD = json.load(open('src/data/sold/sold-12m.json')); WINDOW = SD['meta']['window']
PRE = json.load(open('src/data/presale/2026-11-01.json'))['projects']
PAR_SRC = f'Source: Paragon closed sales, {WINDOW}; medians need 5 or more sales.'
TYPES = [('house', 'Houses'), ('townhome', 'Townhomes'), ('condo', 'Condos'), ('duplex', 'Duplexes')]
TN = {'house': 'houses', 'townhome': 'townhomes', 'condo': 'condos', 'duplex': 'duplexes'}

def exists(s): return os.path.exists(f'src/data/pages/{s}.json') or os.path.exists(f'src/data/local/{s}.json')
def money(v): return '—' if v is None else f'${v:,.0f}'
def first(*c):
    for s in c:
        if exists(s): return s

# ----------------------------------------------------------------------------- configuration
# slug, display name, sold-layer areas, search id, nearby new-construction pages, local planning notes (only facts read on official pages, docs/research/verified-local-facts-2026-11-01.md)
NEW = [
 dict(slug='new-construction-cloverdale', name='Cloverdale', areas=['Cloverdale'], pre=['Cloverdale'], near=['surrey', 'langley'], pk='cloverdale', ck='cloverdale'),
 dict(slug='new-construction-mission', name='Mission', areas=['Mission'], pre=['Mission'], near=['abbotsford', 'maple-ridge'], pk='mission', ck='mission',
      rules=["The City of Mission's small-scale multi-unit housing zoning was Zoning Amending Bylaw 6299-2024-5949(163), amending Zoning Bylaw 5949-2020. Council adopted it on July 17, 2024, at a special meeting by a vote of 4 to 2, after an adoption motion had been defeated 3 to 3 on July 15."]),
 dict(slug='new-construction-chilliwack', name='Chilliwack', areas=['Chilliwack'], pre=['Chilliwack'], near=['sardis', 'abbotsford'], pk='chilliwack', ck='chilliwack',
      rules=["Chilliwack's small-scale multi-unit housing amendment is Zoning Bylaw Amendment Bylaw 2024, No. 5395. It had first, second and third reading on June 4, 2024. The City says it allows up to four units on single-detached or duplex lots over 280 m² inside the urban growth boundary, and keeps two parking spaces per unit."]),
 dict(slug='new-construction-sardis', name='Sardis', areas=['Sardis'], pre=[], near=['chilliwack', 'abbotsford'], pk='sardis'),
 dict(slug='new-construction-maple-ridge', name='Maple Ridge', areas=['Maple Ridge'], pre=['Maple Ridge'], near=['port-coquitlam', 'mission'], pk='maple-ridge', ck='maple-ridge',
      rules=["Maple Ridge adopted Zone Amending Bylaw No. 7998-2024 on June 25, 2024. It amends Zoning Bylaw 7600-2019."]),
 dict(slug='new-construction-ladner', name='Ladner', areas=['Ladner'], pre=['Ladner'], near=['tsawwassen', 'richmond'], pk='ladner', ck='ladner'),
 dict(slug='new-construction-tsawwassen', name='Tsawwassen', areas=['Tsawwassen'], pre=['Tsawwassen'], near=['ladner', 'cloverdale'], pk='tsawwassen', ck='tsawwassen',
      rules=["Delta's Official Community Plan is Bylaw No. 8400 (2024). It folded the former area plans, including the Tsawwassen Area Plan from the previous OCP (Bylaw No. 3950), into a single Land Use Plan.",
             "Delta Zoning Bylaw No. 7600, section 6.2.3, sets a waterfront setback for lots on Boundary Bay along Beach Grove Road south of 16 Avenue; it lets a seawall extend into the minimum front setback."]),
 dict(slug='new-construction-port-coquitlam', name='Port Coquitlam', areas=['Port Coquitlam'], pre=['Port Coquitlam'], near=['coquitlam', 'port-moody'], pk='port-coquitlam', ck='port-coquitlam',
      rules=["Port Coquitlam's Official Community Plan (Bylaw 3838) plans the Dominion Riverfront for townhouses and low-rise apartments. It names Lincoln Park and Mary Hill as neighbourhoods developed from the 1950s, and Riverwood and Citadel Heights as 1980s and 1990s neighbourhoods."]),
 dict(slug='new-construction-port-moody', name='Port Moody', areas=['Port Moody'], pre=['Port Moody'], near=['coquitlam', 'port-coquitlam'], pk='port-moody', ck='port-moody'),
 dict(slug='new-construction-new-westminster', name='New Westminster', areas=['New Westminster'], pre=['New Westminster'], near=['burnaby', 'coquitlam'], pk='new-westminster', ck='new-westminster'),
 dict(slug='new-construction-richmond', name='Richmond', areas=['Richmond'], pre=['Richmond'], near=['vancouver', 'burnaby'], pk='richmond'),
 dict(slug='new-construction-north-vancouver', name='North Vancouver', areas=['North Vancouver'], pre=['North Vancouver'], near=['west-vancouver', 'vancouver'], pk='north-vancouver'),
 dict(slug='new-construction-west-vancouver', name='West Vancouver', areas=['West Vancouver'], pre=['West Vancouver'], near=['north-vancouver', 'vancouver'], pk='west-vancouver'),
]
EXISTING = {  # slug -> (display name, sold-layer areas, nearby)
 'south-surrey-presale-condos': ('South Surrey and White Rock', ['South Surrey White Rock']),
 'surrey-presale-condos-and-townhomes': ('Surrey', ['Surrey', 'North Surrey']),
 'new-construction-presales-in-langley-bc': ('Langley', ['Langley']),
 'abbotsford-presale-condos-and-townhomes': ('Abbotsford', ['Abbotsford']),
 'coquitlam-presale-condos-and-townhomes': ('Coquitlam', ['Coquitlam']),
 'burnaby-presale-condos-and-townhomes': ('Burnaby', ['Burnaby North', 'Burnaby South', 'Burnaby East']),
 'vancouver-presale-condos-and-townhomes': ('Vancouver', ['Vancouver East', 'Vancouver West']),
}
PAGE_OF = {  # city key used in 'near' -> page for a link
 'surrey': ('Surrey', 'surrey-presale-condos-and-townhomes'), 'langley': ('Langley', 'new-construction-presales-in-langley-bc'), 'abbotsford': ('Abbotsford', 'abbotsford-presale-condos-and-townhomes'),
 'coquitlam': ('Coquitlam', 'coquitlam-presale-condos-and-townhomes'), 'burnaby': ('Burnaby', 'burnaby-presale-condos-and-townhomes'), 'vancouver': ('Vancouver', 'vancouver-presale-condos-and-townhomes'),
}
for n in NEW: PAGE_OF[n['pk']] = (n['name'], n['slug'])
IDS = {}   # filled from the worksheet in build_idx_embeds; pages do not print ids

# ----------------------------------------------------------------------------- data helpers
def subs_of(areas):
    for k, v in SD['sub'].items():
        a, s = k.split('|', 1)
        if a in areas: yield a, s, v

def rows_newest(areas, limit=8):
    out = []
    for a, s, v in subs_of(areas):
        for t, tn in TYPES:
            g = v['groups'].get(t)
            if g and g.get('n', 0) >= 5 and g.get('yb') and g.get('price'):
                out.append(dict(sub=s, area=a, t=t, n=g['n'], price=g['price'], dom=g.get('dom'), yb=g['yb'], ratio=g.get('ratio'), over=g.get('over'), p25=g.get('p25'), p75=g.get('p75'), ppsf=g.get('ppsf'), beds=g.get('beds'), maint=g.get('maint') if g.get('maint_n', 0) >= 5 else None, q=g.get('q')))
    out.sort(key=lambda r: (-r['yb'], -r['n']))
    return out[:limit], out

def newer_buildings(areas, since=2022, limit=10):
    out = []
    for a, s, v in subs_of(areas):
        for t in ('condo', 'townhome'):
            for x in (v.get('complexes') or {}).get(t, []):
                if (x.get('yb') or 0) >= since and x['n'] >= 3:
                    out.append(dict(name=x['name'], sub=s, t=t, n=x['n'], price=x['price'] if x['n'] >= 5 else None, dom=x.get('dom') if x['n'] >= 5 else None, yb=x['yb'], ratio=x.get('ratio') if x['n'] >= 5 else None, maint=x.get('maint') if x['n'] >= 5 else None))
    out.sort(key=lambda r: (-r['n'], -r['yb']))
    return out[:limit], out

def projects(cities):
    out = []
    for p in PRE:
        if p['city'] in cities or (p['city'] == 'Delta' and any(x in p['address'] for x in cities)): out.append(p)
    return out

def tbl(caption, head, rows): return {'t': 'table', 'caption': caption, 'head': head, 'rows': rows, 'gen': G}
def H(text, level=2): return {'t': 'h', 'level': level, 'text': text, 'gen': G}
def P(text): return {'t': 'p', 'text': text, 'gen': G}
def LI(items): return {'t': 'list', 'items': [[{'t': x}] for x in items], 'gen': G}
def lk(text, slug): return {'t': text, 'h': f'/{slug}.html'}
def list_of_links(pairs): return {'t': 'list', 'items': [[lk(t, s)] for t, s in pairs if exists(s)], 'gen': G, 'pos': 'end'}

# ----------------------------------------------------------------------------- shared section builders
V_INTRO = [
 "The search above lists active MLS® listings in {C} where the board's age field reads 0 or less. In practice that is a home finished this year, or one listed with a year built still to come. It covers houses, townhomes and condos; land and income properties are left out.",
 "Every listing in the search above is an active MLS® listing in {C} with the board's age field set to 0 or less, meaning completed this year or listed ahead of completion. Houses, townhomes and condos are included, and land and income properties are not.",
 "The listings above are the active MLS® new-construction listings in {C}, picked by setting the board's age field to 0 or less: homes completed this year and homes listed before they are finished. Land and income properties are excluded; houses, townhomes and condos are in.",
 "What you see above is a live MLS® search for {C}: active houses, townhomes and condos with an age of 0 or less in the board's records, so this year's completions and homes still being built. Land and income properties do not appear.",
 "The search above shows active {C} listings that the MLS® records with an age of 0 or less. That picks up homes completed this year and homes listed before completion, in three types (houses, townhomes and condos), with land and income properties left out.",
]
V_LIMIT = [
 "Many presale projects are sold directly by the developer and only reach the MLS® close to completion, so this search is shorter than the full presale market.",
 "A lot of presale homes are sold by the developer and do not appear on the MLS® until near completion, which means the search is a part of the new-home market, not all of it.",
 "Developers sell most presale homes themselves and list them on the MLS® late, if at all. Treat the search as the MLS® slice of new construction.",
 "Presales are often sold by the developer's own team and reach the MLS® only near completion, so this search will not show every project that is selling.",
 "The MLS® carries only part of the new-home market: developers sell many presale homes directly and list them late.",
]
V_NEWEST = [
 "Over {W}, the newest homes to close in {C} were {type} in {sub}: a median build year of {yb}, {n} sales and a median price of {price}.",
 "The most recently built homes that sold in {C} from {W} were {type} in {sub}. Their median build year was {yb}; {n} sold at a median of {price}.",
 "In {W}, {type} in {sub} had the newest stock of any {C} sub-area with enough sales to measure: median build year {yb}, {n} sales, median price {price}.",
 "Looking at {W}, {sub} had the newest sold {type} in {C}, built in {yb} at the median, with {n} sales at a median of {price}.",
 "{sub} led {C} for newness over {W}. {type} that sold there had a median build year of {yb} ({n} sales, median price {price}).",
]


def _qtr(q):
    """Direction of the median price across the four quarters, only where the first and last quarter each have 5 or more sales."""
    if not q or len(q) < 4 or not q[0].get('price') or not q[-1].get('price') or q[0]['n'] < 5 or q[-1]['n'] < 5: return ''
    a, b = q[0]['price'], q[-1]['price']
    if abs(b - a) / a < 0.02: return f" The median held near {money(b)} from the first quarter to the last."
    return f" The median moved from {money(a)} (November to January) to {money(b)} (August to October)."

PROF = [
 "{sub} {type}: {n} sold at a median of {price} (middle half between {p25} and {p75}), taking {dom} days at {ratio}% of the list price, with a median build year of {yb}.{extra}{q}",
 "In {sub}, the {n} {type} that sold had a median build year of {yb} and a median price of {price}; the middle half closed between {p25} and {p75}, after {dom} days on the market at {ratio}% of list.{extra}{q}",
 "{n} {type} sold in {sub} at a median {price}, built {yb} at the median. They took {dom} days and closed at {ratio}% of the list price, with the middle half between {p25} and {p75}.{extra}{q}",
]

def profiles_section(name, allr, limit=14):
    rows = [r for r in allr if r['p25'] and r['p75'] and r['dom'] is not None and r['ratio']][:limit]
    if not rows: return []
    items = []
    for i, r in enumerate(rows):
        ex = []
        if r['beds']: ex.append(f"the typical home had {r['beds']} bedrooms")
        if r['ppsf']: ex.append(f"it sold for about ${r['ppsf']:,} per square foot")
        if r['maint']: ex.append(f"strata fees were a median ${r['maint']:,} a month")
        if r['over'] is not None and r['n']: ex.append(f"{r['over']}% of the sales closed over the list price")
        extra = (' ' + ex[0][0].upper() + ex[0][1:] + (', ' + ', '.join(ex[1:-1]) if len(ex) > 2 else '') + (' and ' + ex[-1] if len(ex) > 1 else '') + '.') if ex else ''
        items.append(PROF[i % 3].format(sub=r['sub'], type=TN[r['t']], n=r['n'], price=money(r['price']), p25=money(r['p25']), p75=money(r['p75']), dom=r['dom'], ratio=r['ratio'], yb=r['yb'], extra=extra, q=_qtr(r['q'])).replace('..', '.'))
    return [H(f'Sold homes in {name}, sub-area by sub-area, newest first'), LI(items)]

BLD = [
 "{name} ({sub}, built {yb}): {n} {type} resold. {tail}",
 "{name} in {sub} was built in {yb}; {n} of its {type} resold. {tail}",
]
def building_notes(allb, limit=8):
    items = []
    for i, x in enumerate(allb[:limit]):
        if x['price']:
            tail = f"The median price was {money(x['price'])}, taking {x['dom']} days at {x['ratio']}% of the list price" + (f", with strata fees around ${x['maint']:,} a month." if x['maint'] else '.')
        else:
            tail = 'Too few sold to show a price.'
        items.append(BLD[i % 2].format(name=x['name'], sub=x['sub'], yb=x['yb'], n=x['n'], type=TN[x['t']], tail=tail))
    return items


CITY_T = [
 "Across {name}, {n} {type} sold at a median of {price}, with the middle half between {p25} and {p75}. They took {dom} days and closed at {ratio}% of the list price, and the median build year was {yb}.{lot}{q}",
 "{name} {type} over the past year: {n} sales, a median of {price}, and a middle half from {p25} to {p75}. The median home was built in {yb}, took {dom} days to sell and closed at {ratio}% of list.{lot}{q}",
]
def city_summary(name, ck):
    g = SD['city'].get(ck, {}).get('groups', {}) if ck else {}
    items = []
    for i, (t, tn) in enumerate(TYPES):
        x = g.get(t)
        if not x or x.get('n', 0) < 5 or not x.get('price') or not x.get('p25'): continue
        lot = f" The typical house sat on a lot of about {x['lot_sqft']:,} square feet." if t == 'house' and x.get('lot_sqft') else (f" Strata fees were a median ${x['maint']:,} a month." if x.get('maint') and x.get('maint_n', 0) >= 5 else '')
        items.append(CITY_T[i % 2].format(name=name, n=x['n'], type=TN[t], price=money(x['price']), p25=money(x['p25']), p75=money(x['p75']), dom=x['dom'], ratio=x['ratio'], yb=x['yb'], lot=lot, q=_qtr(x.get('q'))))
    return [H(f'{name} overall: what sold over the past year'), LI(items)] if items else []

def newest_section(name, areas, vi, profiles=False):
    top, allr = rows_newest(areas)
    if not top: return [], None
    bl = [H(f'What newer homes in {name} have sold for')]
    r = top[0]
    bl.append(P(V_NEWEST[vi % 5].format(C=name, W=WINDOW.replace('November 1, 2025 to October 22, 2026', 'November 2025 to October 2026'), type=TN[r['t']], sub=r['sub'], yb=r['yb'], n=r['n'], price=money(r['price']))))
    recent = [x for x in allr if x['yb'] >= 2020]
    if recent:
        names = []
        for x in recent[:4]: names.append(f"{x['sub']} {TN[x['t']]} (built {x['yb']})")
        bl.append(P(f"{len(recent)} of {len(allr)} sub-area and home-type groups with 5 or more sales had a median build year of 2020 or later. The newest were " + ', '.join(names[:-1]) + (' and ' if len(names) > 1 else '') + names[-1] + '.'))
    else:
        bl.append(P(f"None of the {len(allr)} sub-area and home-type groups with 5 or more sales had a median build year of 2020 or later, so most of what sold was older stock; newer homes here are mostly first sales that never reach the resale shelf."))
    rows = [[x['sub'], TN[x['t']].capitalize(), str(x['n']), money(x['price']), str(x['yb']), (str(x['dom']) if x['dom'] is not None else '—')] for x in top]
    bl.append(tbl(f'Newest sold homes by sub-area, {name}', ['Sub-area', 'Type', 'Sales', 'Median price', 'Median year built', 'Median days to sell'], rows))
    bl.append({'t': 'notice', 'text': PAR_SRC, 'gen': G})
    if profiles: bl += profiles_section(name, allr)
    return bl, (top, allr)

def buildings_section(name, areas, notes=False):
    top, allb = newer_buildings(areas)
    if not top:
        return [P(f"No single {name} condo building or townhome complex built in 2022 or later had 3 or more resales over the past year, so none is named here. Brand-new homes in {name} are usually first sales from the developer, which do not show up in resale figures.")]
    bl = [H(f'Newer buildings in {name} that have resold')]
    k = len(allb)
    bl.append(P(f"{k} {'building' if k == 1 else 'buildings and complexes'} built in 2022 or later had 3 or more sales in the past year. The median price and days to sell appear only where 5 or more sold."))
    rows = [[x['name'], x['sub'], TN[x['t']].capitalize(), str(x['n']), money(x['price']), str(x['yb']), (str(x['dom']) if x['dom'] is not None else '—')] for x in top]
    bl.append(tbl(f'Buildings built 2022 or later with resales, {name}', ['Building', 'Sub-area', 'Type', 'Sales', 'Median price', 'Year built', 'Median days to sell'], rows))
    if notes: bl.append(LI(building_notes(allb)))
    return bl

def presale_section(name, cities, vi):
    ps = projects(cities)
    hub = 'presale-projects-fraser-valley-and-metro-vancouver'
    if name == 'Cloverdale':
        return [H('Presale projects near Cloverdale'), {'t': 'p', 'parts': [{'t': 'My presale list files projects by city, and Cloverdale projects sit under Surrey. See the '}, {'t': 'Surrey presale page', 'h': '/surrey-presale-condos-and-townhomes.html'}, {'t': ' for the full table.'}], 'gen': G}]
    if not ps:
        return [H(f'Presale projects in {name}'), {'t': 'p', 'parts': [{'t': f"The presale list I keep (read November 1, 2026) has no projects in {name} right now, so this page leans on the MLS® search and the sold figures. For projects across the region, see "}, {'t': 'the presale hub', 'h': f'/{hub}.html'}, {'t': '.'}], 'gen': G}]
    yrs = sorted({p['year'] for p in ps})
    bl = [H(f'Presale projects in {name}')]
    bl.append(P(f"My presale list, read November 1, 2026, holds {len(ps)} {name} {'project' if len(ps) == 1 else 'projects'} completing {yrs[0] if len(yrs) == 1 else str(yrs[0]) + ' to ' + str(yrs[-1])}. A price is shown only where the source dates it within three months."))
    rows = []
    for p in ps:
        h = p['homes']; pr = p['price']
        rows.append([p['name'], p['address'].split(',')[0], p['developer'] or '—', p['type'], (f"{h['n']:,}" if h and h['exact'] else (f"{h['n']:,}+" if h else '—')), str(p['year']), (f"{pr['text']} ({pr['asof']})" if pr else 'Ask for current pricing')])
    bl.append(tbl(f'{name} presale projects, snapshot 2026-11-01', ['Project', 'Address', 'Developer', 'Type', 'Homes', 'Completion', 'Published price'], rows))
    return bl

TAX = [
 "New homes can carry different tax rules from resales. BC's property transfer tax has a newly built home exemption, and the federal government has a first-time buyers' GST rebate on new homes; the figures and conditions are on the BC and Canada Revenue Agency pages, and I summarize them on the guides below.",
 "Buying new changes the tax picture: the province offers a property transfer tax exemption for newly built homes and the federal government a GST rebate for first-time buyers of new homes. The current limits are on the official BC and CRA pages, and my guides below set them out in plain language.",
 "Taxes work differently on a new home than on a resale. There is a BC property transfer tax exemption for newly built homes and a federal first-time buyers' GST rebate on new homes. Check the dollar limits on the official pages; the guides below walk through them.",
 "A newly built home can qualify for a BC property transfer tax exemption, and a first-time buyer may also get the federal GST rebate on a new home. Both have price limits and conditions, which the official pages state and the guides below explain.",
 "New homes come with their own tax rules: a property transfer tax exemption in BC for newly built homes, plus a GST rebate for first-time buyers from the federal government. I keep the current limits in the guides below, drawn from the official pages.",
]

def faqs(name, vi, top, ps, rules):
    f = [dict(q='What counts as new construction on this page?', a=f"Active MLS® listings in {name} where the board's age field is 0 or less: homes finished this year and homes listed before completion, in houses, townhomes and condos.", gen=G)]
    if top:
        r = top[0]
        f.append(dict(q=f'Where are the newest homes in {name}?', a=f"Over the past year the newest sold homes were {TN[r['t']]} in {r['sub']}: median build year {r['yb']}, {r['n']} sales, median price {money(r['price'])}.", gen=G))
        fast = sorted([x for x in ps_all(top) if x['dom'] is not None], key=lambda x: x['dom'])[:1]
        if fast:
            x = fast[0]; f.append(dict(q=f'How fast do newer homes sell in {name}?', a=f"The quickest group among the newer ones was {TN[x['t']]} in {x['sub']}: {x['dom']} days to sell at a median, closing at {x['ratio']}% of the list price.", gen=G))
    return f

def ps_all(top): return top
def links_block(name, slug, near, vi):
    pairs = []
    for suf, lab in (('houses-for-sale', 'houses'), ('condos-for-sale', 'condos'), ('townhomes-for-sale', 'townhomes')):
        s = first(f'{slug_city(name)}-{suf}')
        if s: pairs.append((f'{name} {lab} for sale', s))
    pairs += [('Presale projects across the Fraser Valley and Metro Vancouver', 'presale-projects-fraser-valley-and-metro-vancouver'), ('How presales and new-home taxes work in BC', 'new-construction-presales-in-langley-bc'), ('GST rebate in BC', 'gst-rebate-in-bc'), ('BC condo buying rules', 'bc-condo-buying-rules')]
    for n in near:
        if n in PAGE_OF: pairs.append((f'New construction in {PAGE_OF[n][0]}', PAGE_OF[n][1]))
    return pairs

def slug_city(name):
    return {'Chilliwack and Sardis': 'chilliwack', 'North Vancouver': 'north-vancouver', 'West Vancouver': 'west-vancouver', 'New Westminster': 'new-westminster', 'Port Coquitlam': 'port-coquitlam', 'Port Moody': 'port-moody', 'Maple Ridge': 'maple-ridge'}.get(name, name.lower())

# ----------------------------------------------------------------------------- pages
def build_new(i, c):
    name, vi = c['name'], i
    title = f"New Construction in {name} | New Homes for Sale | Jared Gibbons"
    if len(title) > 62: title = f"New Construction in {name} | Jared Gibbons"
    desc = f"New construction homes for sale in {name}: live MLS® listings of new and newly built houses, townhomes and condos, plus what newer homes there have sold for."
    h1 = f"New Construction Homes for Sale in {name}"
    extra_i = ' The search also includes Sardis, which has its own page with its own sold figures.' if c['slug'] == 'new-construction-chilliwack' else ''
    bl = [P(V_INTRO[vi % 5].format(C=name) + extra_i + ' ' + V_LIMIT[vi % 5]), {'t': 'grid', 'gen': G}]
    nb, nd = newest_section(name, c['areas'], vi, profiles=True)
    bl += nb
    bl += buildings_section(name, c['areas'], notes=True)
    bl += city_summary(name, c.get('ck'))
    bl += presale_section(name, c['pre'], vi)
    if c.get('rules'):
        bl += [H(f'Planning and zoning notes for {name}'), LI(c['rules']), {'t': 'notice', 'text': 'Read on the municipality\'s own documents, November 2026. Confirm zoning with the municipality.', 'gen': G}]
    bl.append(H(f'New-home taxes, presale rules and more {name} real estate', 2)); bl[-1]['pos'] = 'end'
    bl.append(list_of_links(links_block(name, c['slug'], c['near'], vi)))
    faq = faqs(name, vi, nd[0] if nd else None, None, c.get('rules'))
    return c['slug'], dict(status='generated', slug=c['slug'], updated='2026-11-04', new_page=dict(title=title, description=desc, h1=h1),
        breadcrumbs=[{'name': 'Home', 'href': '/'}, {'name': 'Presale and new construction', 'href': '/presale-projects-fraser-valley-and-metro-vancouver.html'}, {'name': h1, 'href': f"/{c['slug']}.html"}],
        faq_heading=f'New construction in {name}: your questions answered', faq=faq, blocks=bl)

def patch_existing(slug, name, areas, vi):
    f = f'src/data/local/{slug}.json'; raw = open(f).read(); j = json.loads(raw)
    j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]
    bl = [H(f'New homes listed on the MLS® now in {name}'), P(V_INTRO[vi % 5].format(C=name) + ' ' + V_LIMIT[vi % 5]), {'t': 'grid', 'gen': G}]
    nb, _ = newest_section(name, areas, vi) if areas else ([], None)
    bl += nb
    if areas: bl += buildings_section(name, areas)
    at = 2 if (j['blocks'] and j['blocks'][0].get('t') == 'notice' and len(j['blocks']) > 1 and j['blocks'][1].get('t') == 'p' and j.get('new_page')) else (1 if (j['blocks'] and j['blocks'][0].get('t') == 'notice') else 0)
    j['blocks'][at:at] = bl
    ind = (len(raw.split('\n')[1]) - len(raw.split('\n')[1].lstrip())) if raw.count('\n') > 1 else 1
    json.dump(j, open(f, 'w'), indent=ind or 1, ensure_ascii='\\u' in raw)

def inbound():
    n = 0
    for c in NEW:
        slug = slug_city(c['name']) if c['slug'] != 'new-construction-sardis' else 'sardis'
        hosts = [first(f'{slug}-{x}') for x in ('houses-for-sale', 'condos-for-sale', 'townhomes-for-sale', 'homes-for-sale')]
        for host in [h for h in hosts if h]:
            f = f'src/data/local/{host}.json'; raw = open(f).read() if os.path.exists(f) else ''
            j = json.loads(raw) if raw else {'status': 'generated', 'slug': host, 'updated': '2026-11-04', 'blocks': []}
            j['blocks'] = [b for b in j.get('blocks', []) if not (b.get('gen') == LG and b.get('_for') == c['slug'])]
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': f"New construction in {c['name']}", 'gen': LG, 'pos': 'end', '_for': c['slug']},
                            {'t': 'list', 'items': [[lk(f"New construction homes for sale in {c['name']}", c['slug'])]], 'gen': LG, 'pos': 'end', '_for': c['slug']}]
            ind = (len(raw.split('\n')[1]) - len(raw.split('\n')[1].lstrip())) if raw.count('\n') > 1 else 1
            json.dump(j, open(f, 'w'), indent=ind or 1, ensure_ascii='\\u' in raw); n += 1
    print(n, 'inbound link blocks')

def main():
    for i, c in enumerate(NEW):
        s, j = build_new(i, c)
        json.dump(j, open(f'src/data/local/{s}.json', 'w'), indent=1, ensure_ascii=False)
    for i, (s, (name, areas)) in enumerate(EXISTING.items()):
        patch_existing(s, name, areas, i + 3)
    patch_existing('presale-projects-fraser-valley-and-metro-vancouver', 'the Fraser Valley and Metro Vancouver', [], 0)
    # hub gets links to every new-construction page; city pages get one link each (links-only lists keep uniqueness unchanged)
    hub = 'src/data/local/presale-projects-fraser-valley-and-metro-vancouver.json'; j = json.load(open(hub))
    j['blocks'] = [b for b in j['blocks'] if b.get('gen') != LG]
    pairs = [(f'New construction in {n}', s) for n, s in PAGE_OF.values()]
    j['blocks'] += [{'t': 'h', 'level': 2, 'text': 'New construction by city', 'gen': LG, 'pos': 'end'}, {'t': 'list', 'items': [[lk(t, s)] for t, s in pairs if exists(s)], 'gen': LG, 'pos': 'end'}]
    json.dump(j, open(hub, 'w'), indent=1, ensure_ascii=False)
    print(len(NEW), 'new pages;', len(EXISTING) + 1, 'existing pages patched')
    inbound()

if __name__ == '__main__':
    main()
