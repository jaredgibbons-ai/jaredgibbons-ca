#!/usr/bin/env python3
"""Area gap pages (2026-11-07), from the Google-visibility review of a competing agent's site.

New pages (draft, local layer with new_page header; searches are Jerry's, wired by tools/build_idx_embeds.py once the worksheet comes back):
    north-vancouver-condos-for-sale   from sold-12m.json (closed sales) and the GVR apartment benchmark
    furry-creek-homes-for-sale        search-style page next to the Furry Creek guide (sold counts too small for medians)
    ocean-park-homes-for-sale         MLS sub-area F53 covers Crescent Beach and Ocean Park together, so the figures are for both and the page says so
    crescent-beach-homes-for-sale     same
Refreshed pages (a "what homes sold for" block from src/data/sold/neighbourhood-2026-11-07.json, Jared's Paragon pull of November 7, 2026, closed and pending):
    morgan-creek, grandview-surrey, crescent-beach-ocean-park-guide
Added to the existing White Rock page (the White Rock hub): sold prices from the closed and pending extras (src/data/sold/sold-extras.json).
python3 -I tools/build_area_gap_pages.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_extras_pages as X
from build_new_searches import P, H, L, tbl, money, num, lk, pct, subrows, total, qsum, hpi, hpi_table, subtable, buildings, qcounts, LAST, SRC_GVR, EX

G = 'areagap'
NB = json.load(open('src/data/sold/neighbourhood-2026-11-07.json'))
D12, D6 = 'November 7, 2025 and November 6, 2026', 'May 7 to November 6, 2026'
NBSRC = ('Source: Paragon MLS®, Fraser Valley Real Estate Board, closed and pending sales by sold date, pulled November 7, 2026. A pending sale is firm but has not completed, so its price can still change. '
         'A median is the middle price and is shown only where at least 5 homes sold. Detached means a single-family house; half duplexes are counted separately.')
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def dstr(iso): y, m, d = iso.split('-'); return f'{MONTHS[int(m) - 1]} {int(d)}, {y}'
def fit(*c):
    for x in c:
        if 135 <= len(x) <= 158 and x.endswith('.'): return x
    raise AssertionError(('no description fits', [(len(x), x) for x in c]))
def title_of(*c):
    for x in c:
        if 38 <= len(x) <= 60: return x
    raise AssertionError(('no title fits', [(len(x), x) for x in c]))


# ---------------------------------------------------------------- the sold block (three refreshed pages and the two new Crescent Beach / Ocean Park pages)
def nb_blocks(key, label=None, together=False, gen=G):
    a = NB['areas'][key]; g = a['groups']; nm = label or a['name']
    lab = {'detached': 'Detached houses', 'townhouse': 'Townhomes', 'condo': 'Condos', 'duplex': 'Half duplexes'}
    rows = []
    for k in ('detached', 'townhouse', 'condo', 'duplex'):
        if k not in g: continue
        (n12, m12), (n6, m6) = g[k]['12'], g[k]['6']
        rows.append([lab[k], num(n12), money(m12) if n12 >= 5 else '—', num(n6), money(m6) if n6 >= 5 else '—'])
    d, t, c = g['detached']['12'], g['townhouse']['12'], g['condo']['12']
    s = f'Between {D12}, {d[0]} detached houses sold in {nm} at a median of {money(d[1])}, {t[0]} townhomes at {money(t[1])}' + (f' and {c[0]} condos at {money(c[1])}.' if c[0] >= 5 else f' and {c[0]} condos.')
    if together: s += f' MLS® sub-area {a["code"]} covers Crescent Beach and Ocean Park together, so these figures are for both.'
    d6 = g['detached']['6']
    s2 = f'In the last six months ({D6}), {d6[0]} detached houses sold at a median of {money(d6[1])}. The latest sale in the pull was on {dstr(a["latest"])}.'
    sen = f'The typical detached house that sold was built in {a["detached_yb"]} on a lot of {a["detached_lot"]:,} square feet.'
    return [{'t': 'h', 'level': 2, 'text': f'What {nm} homes sold for', 'gen': gen}, {'t': 'p', 'text': s + ' ' + s2, 'gen': gen},
            dict(tbl(f'{nm} homes sold, by type', ['Home type', 'Sales, 12 months', 'Median, 12 months', 'Sales, 6 months', 'Median, 6 months'], rows, NBSRC), gen=gen),
            {'t': 'p', 'text': sen, 'gen': gen}]


def host_edit(host, fn):
    f = f'src/data/local/{host}.json'
    raw = open(f).read(); d = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
    line2 = raw.split('\n')[1] if '\n' in raw else ''; ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
    fn(d); compact = raw.count('\n') <= 1
    open(f, 'w').write(json.dumps(d, separators=(',', ':') if compact else None, indent=None if compact else ind, ensure_ascii=asc) + nl)


def set_blocks(host, gen, blocks, end=False):
    def fn(d):
        d['blocks'] = [b for b in d['blocks'] if b.get('gen') != gen]
        d['blocks'] += [dict(b, gen=gen, **({'pos': 'end'} if end else {})) for b in blocks]
    host_edit(host, fn)


def end_link(host, gen, heading, items):
    ok = [(t, s) for t, s in items if N.exists(s)]
    if os.path.exists(f'src/data/local/{host}.json') and ok:
        set_blocks(host, gen, [{'t': 'h', 'level': 2, 'text': heading}, {'t': 'list', 'items': [[lk(t, s)] for t, s in ok]}], end=True)


# ---------------------------------------------------------------- North Vancouver condos
def nv_condos():
    slug = 'north-vancouver-condos-for-sale'; NVB = ['North Vancouver']
    rows = subrows(NVB, 'condo'); tot = total(NVB, 'condo'); qs = qsum(NVB, 'condo'); h = hpi('gvr', 'North Vancouver', 'apartment')
    for r in rows:
        if r['raw'] == 'Pemberton NV': r['name'] = 'Pemberton'
    by = {r['raw']: r for r in rows}
    ll, cl, lv, ly, pb, rp = (by[k] for k in ('Lower Lonsdale', 'Central Lonsdale', 'Lynn Valley', 'Lynnmour', 'Pemberton NV', 'Roche Point'))
    btab, allc = buildings('North Vancouver condo buildings with the most sales', NVB, 'condo')
    top10 = rows[:10]; fmin, fmax = min(top10, key=lambda r: r['maint']), max(top10, key=lambda r: r['maint'])
    seo = dict(title='North Vancouver Condos for Sale | Prices by Area', h1='North Vancouver Condos for Sale', crumb='North Vancouver condos', links_h='More North Vancouver real estate',
               description=fit('Search North Vancouver condos for sale. See what Lower Lonsdale, Central Lonsdale and Lynn Valley condos sold for, plus strata fees and the benchmark price.'))
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures are Paragon closed sales to October 22, 2026 and the benchmark is the Greater Vancouver REALTORS® price for September 2026. The live search is connected.', 'gen': G},
          P('This search lists condos for sale in North Vancouver: apartment-style homes in strata buildings, from the Lonsdale corridor to Lynn Valley, Lynnmour and Roche Point. Townhomes and houses are separate searches. '
            'North Vancouver is two municipalities, the City and the District, and the MLS® neighbourhoods below cross both.'),
          P(f'{tot:,} North Vancouver condos closed in the year to {LAST}, in {len(rows)} neighbourhoods with 5 or more sales. {ll["name"]} led with {ll["n"]} ({100 * ll["n"] / tot:.0f}% of the total) at a median of {money(ll["price"])}, '
            f'then {cl["name"]} with {cl["n"]} at {money(cl["price"])} and {lv["name"]} with {lv["n"]} at {money(lv["price"])}. The sold records report North Vancouver by neighbourhood, so there is no single city median on this page.'),
          {'t': 'grid', 'gen': G},
          H('What North Vancouver condos sold for'),
          subtable('Condos sold in North Vancouver, by neighbourhood', rows, strata=True, lim=10),
          P(f'Age explains much of the spread. {pb["name"]}’s median condo was built in {pb["yb"]} and sold at {money(pb["price"])} ({money(pb["ppsf"])} a square foot). {lv["name"]}’s was built in {lv["yb"]} and sold at {money(lv["price"])} ({money(lv["ppsf"])} a square foot), '
            f'and {ly["name"]}’s, built in {ly["yb"]}, sold at {money(ly["price"])}.'),
          P(f'Median strata fees among the ten busiest neighbourhoods ran from {money(fmin["maint"])} a month in {fmin["name"]} to {money(fmax["maint"])} in {fmax["name"]}. {rp["name"]} was {money(rp["maint"])} and {ll["name"]} {money(ll["maint"])}. '
            'The fee shows what the building covers, so compare it alongside the price.'),
          qcounts('North Vancouver condos sold, by period', qs),
          P(f'Sales ran {qs[0]} in November to January, {qs[1]} in February to April and {qs[2]} in May to July. The latest period, to {LAST}, shows {qs[3]} and is not a full quarter.'),
          hpi_table('Apartment benchmark price in North Vancouver', [('North Vancouver', h)], 'gvr', SRC_GVR),
          P(f'The apartment benchmark was {money(h["benchmark"])} in September 2026, which moved {pct(h["chg_1y"])} over one year and {pct(h["chg_3y"])} over three years.')]
    if len(allc) >= 3: bl += [H('Buildings that sold most'), btab, P('A building appears with 5 or more sales, because one or two sales is not a price.')]
    bl += [H('Buying a North Vancouver condo'),
           P(f'Check the building before the unit. The older buildings in the sold records, such as {pb["name"]} (median built {pb["yb"]}), raise different questions from the newer ones in {lv["name"]} and {ly["name"]}.'),
           L(['Ask for the strata minutes and the depreciation report, and read the last two years of minutes for special levies and repair plans.',
              f'Check what the monthly fee includes. The ten busiest neighbourhoods ran from {money(fmin["maint"])} to {money(fmax["maint"])} a month.',
              'For a building from before 2000, ask whether the building envelope has been repaired and what the engineer’s report said.',
              'Check rental and pet bylaws before you offer, and whether the building limits short-term rentals.'])]
    faq = [('How much is a condo in North Vancouver?', f'Over the year to {LAST}, the median North Vancouver condo sold for {money(ll["price"])} in Lower Lonsdale, {money(cl["price"])} in Central Lonsdale and {money(lv["price"])} in Lynn Valley. The apartment benchmark was {money(h["benchmark"])} in September 2026.'),
           ('Where do most North Vancouver condos sell?', f'Lower Lonsdale, with {ll["n"]} of {tot:,} sales, then Central Lonsdale with {cl["n"]} and Lynn Valley with {lv["n"]}.'),
           ('What are strata fees for a North Vancouver condo?', f'Median monthly fees by neighbourhood ran from {money(fmin["maint"])} in {fmin["name"]} to {money(fmax["maint"])} in {fmax["name"]} among the ten busiest. The building decides, so check the fee in the listing.'),
           ('Which North Vancouver condo neighbourhoods are newest?', f'Among the busier neighbourhoods, {ly["name"]} (median built {ly["yb"]}) and {lv["name"]} ({lv["yb"]}) have the newest condos, and {pb["name"]} ({pb["yb"]}) the oldest.'),
           ('Did North Vancouver condo prices fall?', f'The apartment benchmark price moved {pct(h["chg_1y"])} over one year and {pct(h["chg_3y"])} over three years, to {money(h["benchmark"])} in September 2026.')]
    links = [('North Vancouver homes for sale', 'north-vancouver-homes-for-sale'), ('New construction in North Vancouver', 'new-construction-north-vancouver'), ('North Vancouver market stats', 'north-vancouver-real-estate-market-stats'),
             ('Schools in North Vancouver', 'schools-in-north-vancouver-bc'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Vancouver condos for sale', 'vancouver-condos-for-sale'), ('Burnaby condos for sale', 'burnaby-condos-for-sale'),
             ('West Vancouver homes for sale', 'west-vancouver-homes-for-sale'), ('First-time home buyer program', 'first-time-home-buyer-program'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return N.finish(slug, seo, [('North Vancouver homes', 'north-vancouver-homes-for-sale')], faq, bl, 'North Vancouver condos: your questions answered', links, dict(search_page=dict(kind='type', city='north-vancouver')))


# ---------------------------------------------------------------- Furry Creek
def furry_creek():
    slug = 'furry-creek-homes-for-sale'
    sub = json.load(open('src/data/sold/sold-12m.json'))['sub']['West Vancouver|Furry Creek']['groups']
    hn, tn = sub['house']['n'], sub['townhome']['n']; n = hn + tn
    seo = dict(title='Furry Creek Homes for Sale | Howe Sound Townhomes & Land', h1='Furry Creek Homes for Sale', crumb='Furry Creek homes', links_h='More Furry Creek and Howe Sound real estate',
               description=fit('Search Furry Creek homes for sale on Howe Sound. See the townhomes and land that trade here, how few homes sell each year and the local rules to check.',
                               'Search Furry Creek homes for sale on Howe Sound. See the townhomes and land that trade, how few homes sell each year and the local rules to check.'))
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Written from the Furry Creek guide (checked November 1, 2026) and Paragon closed sales to October 22, 2026. The live search is connected.', 'gen': G},
          P('Furry Creek is a master-planned community on the east shore of Howe Sound along Highway 99, between Lions Bay and Squamish. It is unincorporated and sits in Electoral Area D of the Squamish-Lillooet Regional District (SLRD), '
            'so there is no city hall: the SLRD sets the zoning and runs the local services.'),
          P(f'This search lists homes for sale in Furry Creek. Very few sell. Between {N.WINDOW.replace(" to ", " and ")}, the MLS® recorded {n} sales here ({hn} house and {tn} townhomes), so the search often shows only a few homes at a time, and '
            'no median price is shown on this page because a median needs at least 5 sales.'),
          {'t': 'grid', 'gen': G},
          H('What trades in Furry Creek'),
          L(['Townhomes. Oliver’s Landing, the waterfront strata on Beach Drive, Whitecap Court and Point Terrace, is the main townhome complex, and its last phase was still going through development permits in 2025.',
             'Land. Lots and land trade here under the SLRD’s Furry Creek zones. The land buying rules page explains the checks.',
             'Condos. Furry Creek has no apartment-condo buildings, so a condo search here will usually be empty.']),
          H('Rules that apply in Furry Creek'),
          L(['There is no municipal bylaw set. Zoning is the SLRD Electoral Area D Zoning Bylaw No. 1350-2016, and the Furry Creek zones include CD3 and the FCR residential zones.',
             'The extra 3 to 6 unit densities allowed elsewhere in BC do not apply. The Province determined that Furry Creek is not within an urban containment boundary, and SLRD Amendment Bylaw No. 1887-2025 removed the extra densities that had briefly been added.',
             'Water, sewer, dyking, fire and street lighting are SLRD local services, so ask what each costs and who provides it before you offer.']),
          P('The Furry Creek real estate guide covers the condo, townhome and land notes in full, with the sources for each.')]
    faq = [('Where is Furry Creek?', 'On the east shore of Howe Sound along the Sea-to-Sky Highway (Highway 99), between Lions Bay and Squamish. The MLS® files it under West Vancouver, but it is not part of the District of West Vancouver. It sits in the Squamish-Lillooet Regional District.'),
           ('How many homes sell in Furry Creek?', f'Very few. The MLS® recorded {n} sales between {N.WINDOW.replace(" to ", " and ")}: {hn} house and {tn} townhomes. With so few sales a price from one year says little, so look at the listings in front of you.'),
           ('What kinds of homes are in Furry Creek?', 'Townhomes, mainly at Oliver’s Landing, and land. There are no apartment-condo buildings.'),
           ('Who provides services in Furry Creek?', 'The Squamish-Lillooet Regional District. Water, sewer, dyking, fire and street lighting are SLRD local services rather than a city’s.')]
    links = [('Furry Creek real estate guide', 'furry-creek-bc-guide'), ('West Vancouver homes for sale', 'west-vancouver-homes-for-sale'), ('West Vancouver market stats', 'west-vancouver-real-estate-market-stats'),
             ('BC land buying rules', 'bc-land-buying-rules'), ('BC townhome buying rules', 'bc-townhome-buying-rules'), ('North Vancouver homes for sale', 'north-vancouver-homes-for-sale'), ('Mortgage calculator for BC', 'mortgage-calculator')]
    return N.finish(slug, seo, [('West Vancouver homes', 'west-vancouver-homes-for-sale')], faq, bl, 'Furry Creek homes: your questions answered', links, dict(search_page=dict(kind='area', city='furry-creek')))


# ---------------------------------------------------------------- Ocean Park and Crescent Beach (one MLS sub-area, two pages)
def coast(which):
    a = NB['areas']['crescent-beach-ocean-park']; g = a['groups']; d, d6, t, c = g['detached']['12'], g['detached']['6'], g['townhouse']['12'], g['condo']['12']
    op = which == 'ocean-park'; nm = 'Ocean Park' if op else 'Crescent Beach'; other = 'Crescent Beach' if op else 'Ocean Park'
    slug = f'{which}-homes-for-sale'
    seo = dict(title=title_of(f'{nm} Homes for Sale | South Surrey Houses & Condos', f'{nm} Homes for Sale | South Surrey') if op else title_of('Crescent Beach Homes for Sale | Houses, Condos & Lots', 'Crescent Beach Homes for Sale | South Surrey'),
               h1=f'{nm} Homes for Sale in South Surrey', crumb=f'{nm} homes', links_h=f'More {nm} and South Surrey real estate',
               description=fit(*([f'Search {nm} homes for sale in South Surrey. See what homes sold for, the schools, the hall and library, and what to check on slopes and old houses.'] if op else
                               [f'Search {nm} homes for sale in South Surrey. See what homes sold for, the beach and Blackie Spit, and flood rules, dykes and insurance to check.'])))
    intro = ('Ocean Park is the settled residential community on the east side of Boundary Bay, in the southwest corner of South Surrey. The Multiple Listing Service files it with Crescent Beach under one sub-area, “Crescent Bch Ocean Pk.” (F53), '
             'so the board reports the two together. Near the water, coastal flood rules shape a home; up on the bluffs and the upland streets, slope and drainage do.') if op else (
            'Crescent Beach is a low seaside village at the mouth of the Nicomekl River, below the Crescent Heights bluff. The Multiple Listing Service files it with Ocean Park under one sub-area, “Crescent Bch Ocean Pk.” (F53), '
            'so the board reports the two together. The village plan aims to keep a semi-rural beach village, with its shops along Beecher Street.')
    how = (f'The search below picks up homes for sale in F53 whose listing text mentions {nm}. Listings are not tagged by neighbourhood inside the sub-area, so a home whose description leaves the name out will not appear, '
           f'and one that mentions {nm} can sit closer to {other}. The Crescent Beach and Ocean Park search shows every home in both.')
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures are Jared’s Paragon pull of November 7, 2026 (closed and pending). The live search is connected.', 'gen': G},
          P(intro), P(how), {'t': 'grid', 'gen': G}]
    if op:
        sold = f'{nm} home prices'
        txt = (f'Sales here are reported with Crescent Beach, so the numbers describe both. From November 7, 2025 to November 6, 2026, {d[0]} detached houses sold at a median of {money(d[1])}. '
               f'In the most recent six months ({D6}) there were {d6[0]} sales at {money(d6[1])}, a little under the full-year median. Townhomes ({t[0]} sales, {money(t[1])}) and condos ({c[0]} sales, {money(c[1])}) are small groups next to houses.')
        txt2 = f'The typical house in these sales was built in {a["detached_yb"]} on a lot of about {a["detached_lot"]:,} square feet, so a typical sale is an older house on a mid-sized lot.'
    else:
        sold = f'{nm} home prices'
        txt = (f'The board does not split Crescent Beach from Ocean Park, so these are figures for both. In the year ending November 6, 2026, {d[0]} detached houses sold at a median of {money(d[1])}, '
               f'and {t[0]} townhomes at {money(t[1])}. Condos are a small group: {c[0]} sales at a median of {money(c[1])}. Over the latest six months ({D6}), detached sales numbered {d6[0]} at a median of {money(d6[1])}.')
        txt2 = f'The median detached sale was a house built in {a["detached_yb"]} on a {a["detached_lot"]:,} square foot lot. The most recent sale in the pull closed on {dstr(a["latest"])}.'
    bl += [H(sold), P(txt), P(txt2),
           {'t': 'p', 'parts': [{'t': 'Source: Paragon MLS®, Fraser Valley Real Estate Board, closed and pending sales, pulled November 7, 2026. Medians are shown only where at least 5 homes sold. The full table by home type is in the '}, lk('Crescent Beach and Ocean Park guide', 'crescent-beach-ocean-park-guide'), {'t': '.'}], 'gen': G}]
    if op:
        bl += [H('Ocean Park landmarks and getting around'),
               L(['Ocean Park Community Hall, at 1577 128 Street, dates from 1925, and the Ocean Park Branch library, a 6,500 square foot branch, is at 12854 17 Avenue.',
                  'Crescent Park Annex, at 2378 124 Street, opened in 1918 and is described as the only one-room schoolhouse in Surrey still standing on its original site.',
                  'TransLink route 361 serves Ocean Park.',
                  'Kwomais Point Park, at 1367 128 Street, has a viewing platform over Semiahmoo Bay and a forest path between 126A and 128 Street.']),
               H('Schools near Ocean Park'),
               P('Surrey Schools (SD36) elementary schools with addresses in the area include Crescent Park (2440 128 Street), Ocean Cliff (12550 20 Avenue), Ray Shepherd (1650 136 Street) and Laronde (1880 Laronde Drive). Elgin Park Secondary is at 13484 24 Avenue. Confirm the catchment with the district before you offer.'),
               {'t': 'list', 'items': [[lk('Homes for sale near Crescent Park Elementary', 'homes-near-crescent-park-elementary')], [lk('Homes for sale near Ocean Cliff Elementary', 'homes-near-ocean-cliff-elementary')],
                                      [lk('Homes for sale near Ray Shepherd Elementary', 'homes-near-ray-shepherd-elementary')], [lk('Homes for sale near Elgin Park Secondary', 'homes-near-elgin-park-secondary')]], 'gen': G},
               H('What to check on an Ocean Park home'),
               L(['On the older upland streets, look at the age of the house, the drainage and the lot width, and ask what the zone allows if you plan to rebuild or add on. A new house next door does not show what your lot allows.',
                  'On the slopes, look at retaining walls, stairs and where storm water goes, and ask whether a geotechnical report exists and whether the City holds slope notes for the lot.',
                  'If a tree on a slope needs to come out, ask whether a permit is required first.'])]
    else:
        bl += [H('The village, the beach and the parks'),
               L(['Crescent Beach, at 12160 Beecher Street, is open from dawn to dusk. It has two roped swim areas, summer lifeguards at Sullivan Point, a pier, and a beachfront path along dykes built in 1913.',
                  'Blackie Spit Park, at 3136 McBride Avenue, has two fenced off-leash areas, the Surrey Sailing Club and the Dunsmuir Community Gardens. It is part of the Fraser River Estuary Important Bird Area.',
                  'The plan area is about 91 hectares, with water on the north, west and north-east sides. TransLink route 350 serves the village.']),
               H('Flood rules, dykes and insurance'),
               P('The village floor lies 0 to 3 metres above sea level behind a dyke system. A storm surge in 1982 heavily damaged frontage properties, and the City’s Coastal Flood Adaptation Strategy, approved in November 2019, covers Crescent Beach.'),
               L(['Compare the home’s floor height with the dyke, and find out whether it sits on a slab or over a crawlspace.',
                  'Ask what flood construction level a rebuild would need, and what the 1999 Crescent Beach Land Use Plan allows on the lot.',
                  'Get an insurance quote before you offer and ask about the limits that apply to storm surge.']),
               H('Schools near Crescent Beach'),
               P('Crescent Park Elementary, at 2440 128 Street, is the Surrey Schools (SD36) elementary school closest to the village, and Elgin Park Secondary is at 13484 24 Avenue. Confirm the catchment with the district before you offer.'),
               {'t': 'list', 'items': [[lk('Homes for sale near Crescent Park Elementary', 'homes-near-crescent-park-elementary')], [lk('Homes for sale near Elgin Park Secondary', 'homes-near-elgin-park-secondary')]], 'gen': G}]
    if op:
        faq = [('Does Ocean Park have its own sold-price figures?', f'Not from the board. Ocean Park shares MLS® sub-area F53 with Crescent Beach, so any sold figure for the sub-area describes both. This page does not try to split them.'),
               ('What does a house in Ocean Park cost?', f'In F53 the median detached house sold for {money(d[1])} over the year to November 6, 2026 ({d[0]} sales). Ocean Park and Crescent Beach are in that number together.'),
               ('Why might a home I know is in Ocean Park be missing from the search?', 'The search finds listings that mention Ocean Park in their text. If the agent’s description does not use the name, the home will not show here, but it will appear in the Crescent Beach and Ocean Park search.'),
               ('What is there to do in Ocean Park?', 'The Community Hall (1925), the Ocean Park Branch library, Kwomais Point Park and the Crescent Park Annex schoolhouse (1918) are the local landmarks, with Crescent Park, Ocean Cliff, Ray Shepherd and Laronde elementary schools nearby.')]
    else:
        faq = [('Does Crescent Beach have separate sold prices?', 'No. The board reports Crescent Beach and Ocean Park as one sub-area (F53), so the sold figures on this page describe both.'),
               ('How much is a house in Crescent Beach?', f'Across F53 the median detached sale was {money(d[1])} in the year to November 6, 2026, from {d[0]} sales. That includes Ocean Park, so a village home can sit above or below it.'),
               ('Why would a Crescent Beach home not appear in this search?', 'The search looks for the name Crescent Beach in the listing text. A home whose description leaves it out will be missing here, though it shows in the Crescent Beach and Ocean Park search.'),
               ('Is Crescent Beach a flood area?', 'The village floor is 0 to 3 metres above sea level behind a dyke system, and Surrey’s Coastal Flood Adaptation Strategy covers it. Check floor height, the flood construction level for a rebuild and insurance limits for storm surge before you offer.')]
    links = [(f'{other} homes for sale', 'crescent-beach-homes-for-sale' if op else 'ocean-park-homes-for-sale'), ('Crescent Beach and Ocean Park guide', 'crescent-beach-ocean-park-guide'), ('Ocean view homes in Crescent Beach and Ocean Park', 'ocean-view-homes-crescent-beach-ocean-park'),
             ('White Rock homes for sale', 'white-rock'), ('South Surrey homes for sale', 'south-surrey-homes-for-sale'), ('South Surrey waterfront homes', 'south-surrey-white-rock-waterfront-homes-for-sale'), ('Schools in South Surrey and White Rock', 'schools-in-south-surrey-white-rock-bc'),
             ('Mortgage calculator for BC', 'mortgage-calculator')]
    return N.finish(slug, seo, [('South Surrey homes', 'south-surrey-homes-for-sale')], faq, bl, f'{nm} homes: your questions answered', links, dict(search_page=dict(kind='area', city='crescent-beach-ocean-park')))


# ---------------------------------------------------------------- White Rock: sold prices on the existing hub
def white_rock_block():
    g = EX['city']['white-rock']['groups']; h, c = g['house'], g['condo']; win = EX['meta']['window'].replace(' to ', ' and ')
    rows = [['Sales', num(h['n']), num(c['n'])], ['Median price', X.cv(h, 'price', money), X.cv(c, 'price', money)]]
    if h.get('p25') or c.get('p25'): rows.append(['Middle half of prices', f'{money(h["p25"])} to {money(h["p75"])}' if h.get('p25') else '—', f'{money(c["p25"])} to {money(c["p75"])}' if c.get('p25') else '—'])
    rows += [['Price per square foot', X.cv(h, 'ppsf', money), X.cv(c, 'ppsf', money)], ['Days to sell', X.cv(h, 'dom'), X.cv(c, 'dom')],
             ['Sold price as a share of list price', X.cv(h, 'ratio', X.pc), X.cv(c, 'ratio', X.pc)], ['Sales over the list price', X.cv(h, 'over', X.pc), X.cv(c, 'over', X.pc)]]
    rows = [r for r in rows if any(x != '—' for x in r[1:])]
    return [{'t': 'h', 'level': 2, 'text': 'What White Rock homes sold for', 'gen': G},
            {'t': 'p', 'text': f'Between {win}, {h["n"]} detached houses sold in White Rock at a median of {money(h["price"])}, and {c["n"]} condos at {money(c["price"])}. Condos are more than two thirds of White Rock sales, so the city-wide picture depends on which you are buying.', 'gen': G},
            dict(tbl('White Rock houses and condos sold', ['Measure', 'Detached houses', 'Condos'], rows, X.SRC), gen=G)]


def write_xlsx(made):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'New searches'
    ws.append(['Page slug', 'Page heading', 'Page URL', 'Search name to save in MyRealPage', 'MLS area', 'Sub-area filter', 'Property type (Type of Dwelling)', 'Other filters', 'Price filter', 'Status', 'Search ID (Jerry fills)', 'Embed code (Jerry fills)'])
    kw = lambda nm: f'Keyword search for “{nm}” in the listing remarks (public remarks), same method as the school searches. Keep the sub-area filter so it stays inside the Crescent Beach and Ocean Park sub-area. Also tell me the result count.'
    spec = {'north-vancouver-condos-for-sale': ('TYPE North Vancouver Condos', 'North Vancouver', '(none)', 'Apartment/Condo', '(none)'),
            'furry-creek-homes-for-sale': ('AREA Furry Creek', 'West Vancouver', 'Furry Creek', '(none: leave the type open, so houses, townhomes and land all show)', '(none)'),
            'ocean-park-homes-for-sale': ('AREA Ocean Park', 'South Surrey White Rock', 'Crescent Bch Ocean Pk. (F53)', 'House/Single Family + Apartment/Condo + Townhouse (all residential)', kw('Ocean Park')),
            'crescent-beach-homes-for-sale': ('AREA Crescent Beach', 'South Surrey White Rock', 'Crescent Bch Ocean Pk. (F53)', 'House/Single Family + Apartment/Condo + Townhouse (all residential)', kw('Crescent Beach'))}
    for j in made:
        sl = j['slug']; nm, area, sub, typ, other = spec[sl]
        ws.append([sl, j['new_page']['h1'], f'https://jaredgibbons.ca/{sl}.html', nm, area, sub, typ, other, '(none)', 'Active', '', ''])
        for c in ws[ws.max_row]: c.alignment = Alignment(wrap_text=True, vertical='top')
    for c in ws[1]: c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical='top')
    for col, w in zip('ABCDEFGHIJKL', (34, 36, 40, 30, 24, 28, 30, 60, 12, 10, 18, 40)): ws.column_dimensions[col].width = w
    nt = wb.create_sheet('Notes')
    for t in ['One saved MyRealPage search per row, noframe template, then send the search ID and embed code back, same as the school searches.',
              'Status Active. No price, age or bedroom filter.',
              'Ocean Park and Crescent Beach are one MLS sub-area, so both rows use the sub-area filter plus a keyword in the remarks. Please tell me how many results each one returns.',
              'EXTRA, count only (no page yet): West Vancouver houses on a golf course. In MyRealPage, West Vancouver area, House/Single Family, Active, keyword “golf” in the remarks. Tell me the result count and save it as “KEY West Vancouver Golf”, so I can decide whether a page is worth building.']:
        nt.append([t])
    nt.column_dimensions['A'].width = 140
    f = 'docs/review/idx/area-gap-searches-2026-11-07.xlsx'; wb.save(f); print('worksheet written:', f)


def main():
    made = [nv_condos(), furry_creek(), coast('ocean-park'), coast('crescent-beach')]
    N.NEW.update(j['slug'] for j in made)
    for j in made: N.TITLE[j['slug']] = j['new_page']['h1']
    N.write_seo(made)
    # refreshed pages
    set_blocks('morgan-creek', 'nbsold', nb_blocks('morgan-creek'))
    set_blocks('grandview-surrey', 'nbsold', nb_blocks('grandview-surrey'))
    set_blocks('crescent-beach-ocean-park-guide', 'nbsold', nb_blocks('crescent-beach-ocean-park', together=True))
    set_blocks('white-rock', 'wrsold', white_rock_block())
    # inbound links
    end_link('north-vancouver-homes-for-sale', 'nvcondolink', 'North Vancouver condos', [('North Vancouver condos for sale', 'north-vancouver-condos-for-sale')])
    end_link('north-vancouver-real-estate-market-stats', 'nvcondolink', 'North Vancouver condos', [('North Vancouver condos for sale', 'north-vancouver-condos-for-sale')])
    end_link('new-construction-north-vancouver', 'nvcondolink', 'North Vancouver condos', [('North Vancouver condos for sale', 'north-vancouver-condos-for-sale')])
    end_link('furry-creek-bc-guide', 'fchublink', 'Furry Creek homes for sale', [('Furry Creek homes for sale', 'furry-creek-homes-for-sale')])
    end_link('west-vancouver-homes-for-sale', 'fchublink', 'Furry Creek', [('Furry Creek homes for sale', 'furry-creek-homes-for-sale')])
    end_link('west-vancouver-real-estate-market-stats', 'fchublink', 'Furry Creek', [('Furry Creek homes for sale', 'furry-creek-homes-for-sale')])
    coastlinks = [('Ocean Park homes for sale', 'ocean-park-homes-for-sale'), ('Crescent Beach homes for sale', 'crescent-beach-homes-for-sale')]
    for host in ('crescent-beach-ocean-park-guide', 'ocean-view-homes-crescent-beach-ocean-park', 'south-surrey-homes-for-sale', 'white-rock', 'white-rock-guide', 'south-surrey-white-rock-waterfront-homes-for-sale'):
        end_link(host, 'coastlinks', 'Ocean Park and Crescent Beach homes', coastlinks)
    write_xlsx(made)
    print(len(made), 'new pages; 4 pages given sold blocks; inbound links added')


if __name__ == '__main__': main()
