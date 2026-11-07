#!/usr/bin/env python3
"""Site-wide gap fixes (2026-11-07), from the page-by-page audit.

  FAQ with FAQPage schema   abbotsford-townhomes-for-sale (its seven archive questions move into the schema list, plus data questions),
                            lower-landing, new-construction-lower-landing
  Thin pages expanded       homes-under-1500000, sold-properties, new-construction-lower-landing (tables from the 12-month closed-sales file)
  Links                     gst-rebate-in-bc (it had none), with the two pages that explain the same new-home taxes
Every block carries gen 'gapfix' and is rebuilt on each run.
python3 -I tools/build_gap_fixes.py
"""
import json, os, sys, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_area_gap_pages as A
import build_sold_layer as S

G = 'gapfix'
AGG = json.load(open('src/data/sold/sold-12m.json'))
WIN = S.WINDOW
money, num = N.money, N.num
P = lambda t: {'t': 'p', 'text': t}
H = lambda t, l=2: {'t': 'h', 'level': l, 'text': t}
def tbl(cap, head, rows, src=None):
    b = {'t': 'table', 'caption': cap, 'head': head, 'rows': rows}
    if src: b['source'] = src
    return b
SRC = f'Source: Paragon MLS®, closed sales only, {WIN}. A median is the middle price and is shown only where at least 5 homes sold.'

CITY = {'surrey': 'Surrey', 'south-surrey': 'South Surrey', 'cloverdale': 'Cloverdale', 'north-delta': 'North Delta', 'ladner': 'Ladner', 'tsawwassen': 'Tsawwassen',
        'mission': 'Mission', 'burnaby': 'Burnaby', 'coquitlam': 'Coquitlam', 'port-coquitlam': 'Port Coquitlam', 'port-moody': 'Port Moody',
        'new-westminster': 'New Westminster', 'maple-ridge': 'Maple Ridge', 'chilliwack': 'Chilliwack'}
TYPES = [('house', 'Houses'), ('townhome', 'Townhomes'), ('condo', 'Condos')]


def faq_edit(slug, faqs, extra=None):
    """Replace this generator's FAQ entries (gen gapfix) on a local layer; existing questions from other generators stay."""
    def fn(d):
        keep = [q for q in d.get('faq', []) if q.get('gen') != G]
        have = {q['q'].strip().lower() for q in keep}
        d['faq'] = keep + [dict(q, gen=G) for q in faqs if q['q'].strip().lower() not in have]
        if extra: extra(d)
    A.host_edit(slug, fn)


# ------------------------------------------------------------------ abbotsford-townhomes-for-sale
def abbotsford_townhomes():
    slug = 'abbotsford-townhomes-for-sale'
    subs = []
    for k, v in AGG['sub'].items():
        if k.startswith('Abbotsford|') and 'townhome' in v['groups']:
            g = v['groups']['townhome']
            if g['n'] >= 5 and 'price' in g: subs.append((k.split('|')[1], g))
    subs.sort(key=lambda x: -x[1]['n'])
    tot = sum(g['n'] for _, g in subs)
    top = subs[0]; cheap = min(subs, key=lambda x: x[1]['price']); dear = max(subs, key=lambda x: x[1]['price'])
    fast = min(subs, key=lambda x: x[1]['dom']); slow = max(subs, key=lambda x: x[1]['dom'])
    oldest = min(subs, key=lambda x: x[1]['yb']); newest = max(subs, key=lambda x: x[1]['yb'])
    cheapfee = min(subs, key=lambda x: x[1].get('maint') or 10 ** 9); dearfee = max(subs, key=lambda x: x[1].get('maint') or 0)
    # the seven questions the archive page carried as plain text, so they now sit in the FAQPage schema as well
    src = json.load(open(f'src/data/pages/{slug}.json'))['blocks']
    txt = lambda b: ''.join(x['t'] for x in b.get('parts', [])) if b.get('parts') else b.get('text', '')
    arch = []
    i = next(i for i, b in enumerate(src) if b.get('t') == 'h' and b.get('id') == 'jg-faq') + 1
    while i + 1 < len(src) and src[i].get('t') == 'p' and src[i].get('parts') and txt(src[i]).endswith('?') and src[i + 1].get('t') == 'p':
        arch.append({'q': txt(src[i]), 'a': txt(src[i + 1])}); i += 2
    assert len(arch) == 7, len(arch)
    data = [
        {'q': 'What did townhomes in Abbotsford sell for over the past year?',
         'a': f'{tot:,} townhomes sold in the five Abbotsford areas that had enough sales for a median between {WIN}. The middle price ran from {money(cheap[1]["price"])} in {cheap[0]} to {money(dear[1]["price"])} in {dear[0]}.'},
        {'q': 'Which part of Abbotsford sells the most townhomes?',
         'a': f'{top[0]} had the most closed sales, {top[1]["n"]}, with a median of {money(top[1]["price"])}. ' + ', '.join(f'{n} had {g["n"]}' for n, g in subs[1:]) + f'. Sales are for {WIN}.'},
        {'q': 'How fast do Abbotsford townhomes sell?',
         'a': f'Medians run from {fast[1]["dom"]} days in {fast[0]} to {slow[1]["dom"]} days in {slow[0]}. Sale price was a median {min(g["ratio"] for _, g in subs):.1f}% to {max(g["ratio"] for _, g in subs):.1f}% of the last list price across the five areas.'},
        {'q': 'How old are the townhomes that sell in Abbotsford?',
         'a': f'The median year built was {oldest[1]["yb"]} in {oldest[0]} and {newest[1]["yb"]} in {newest[0]}. The older end is where the strata paperwork (depreciation report, past special levies) matters most.'},
        {'q': 'What are strata fees for an Abbotsford townhome?',
         'a': f'Of the listings that stated a monthly fee, the median was {money(cheapfee[1]["maint"])} in {cheapfee[0]} and {money(dearfee[1]["maint"])} in {dearfee[0]}. Fees vary by complex, so check the fee against what it covers.'},
    ]
    def extra(d):
        d['faq_heading'] = 'Abbotsford townhomes: your questions answered'
        d['suppress'] = d.get('suppress', []) + [x for x in ['7 Common Questions About Abbotsford Townhomes for Sale'] if x not in d.get('suppress', [])]
        d['hide'] = d.get('hide', []) + [x for x in ['Frequently Asked Questions'] if x not in d.get('hide', [])]
    faq_edit(slug, data + arch, extra)


# ------------------------------------------------------------------ lower-landing
def lower_landing():
    s = AGG['sub']['Chilliwack|Lower Landing']['groups']; ch = AGG['city']['chilliwack']['groups']
    th, ho = s['townhome'], s['house']; cth, cho = ch['townhome'], ch['house']
    faqs = S.sold_faq('Lower Landing', 'townhomes', th, 'townhome') + S.sold_faq('Lower Landing', 'houses', ho, 'house')
    faqs += [
        {'q': 'How much do Lower Landing homes cost compared with the rest of Chilliwack?',
         'a': f'The median Lower Landing townhome sold for {money(th["price"])} against {money(cth["price"])} across Chilliwack, and the median house for {money(ho["price"])} against {money(cho["price"])}. Lower Landing figures rest on {th["n"]} townhome and {ho["n"]} house sales, Chilliwack figures on {cth["n"]:,} and {cho["n"]:,}, for {WIN}.'},
        {'q': 'How new are the homes in Lower Landing?',
         'a': f'The median year built was {th["yb"]} for townhomes and {ho["yb"]} for houses, so most sales were of homes finished in the past two years. The typical townhome had {th["beds"]} bedrooms and the typical house {ho["beds"]}.'},
        {'q': 'What is the strata fee for a Lower Landing townhome?',
         'a': f'All {th["maint_n"]} townhome sales reported a monthly fee and the median was {money(th["maint"])}. Ask for the strata documents on any complex, since a low fee in a new complex can rise once the reserve fund is set by the owners.'},
        {'q': 'Are there new homes still being sold in Lower Landing?',
         'a': 'Yes, the new-construction page for Lower Landing lists the active new and newly built homes from the MLS® system, and it updates as listings change. Builders may also sell homes that are not on the MLS® system, so ask Jared if you want a project checked.'},
    ]
    faq_edit('lower-landing', faqs, lambda d: d.update(faq_heading='Lower Landing real estate: your questions answered'))


# ------------------------------------------------------------------ new-construction-lower-landing
def ncs_lower_landing():
    s = AGG['sub']['Chilliwack|Lower Landing']['groups']; cb = AGG['sub']['Chilliwack|Lower Landing']['complexes']['townhome'][0]
    th, ho = s['townhome'], s['house']
    faqs = [
        {'q': 'What have new homes in Lower Landing sold for?',
         'a': f'The {th["n"]} townhomes that sold in Lower Landing had a median price of {money(th["price"])} and a median year built of {th["yb"]}. The {ho["n"]} houses had a median of {money(ho["price"])} and were also built in {ho["yb"]}. Sales are for {WIN}.'},
        {'q': 'How long do newly built Lower Landing townhomes take to sell?',
         'a': f'The median was {th["dom"]} days on the market at {th["ratio"]:.1f}% of the last list price, against {ho["dom"]} days and {ho["ratio"]:.1f}% for houses. Newly built townhomes took about twice as long as the houses.'},
        {'q': 'Which Lower Landing complex has resold the most?',
         'a': f'{cb["name"]}, built in {cb["yb"]}, had {cb["n"]} resales at a median of {money(cb["price"])}, taking a median of {cb["dom"]} days, with a strata fee of {money(cb["maint"])} a month.'},
        {'q': 'Do I pay GST on a new home in Lower Landing?',
         'a': 'Yes. A new or substantially renovated home carries 5% GST, and first-time buyers can get that back in full on homes up to $1 million, with a partial rebate up to $1.5 million. Resale homes carry no GST.'},
        {'q': 'What warranty comes with a new home in BC?',
         'a': 'A builder in BC has to provide third-party home warranty insurance: 2 years on labour and materials, 5 years on the building envelope and 10 years on the structure. Ask for the warranty certificate before you remove subjects.'},
    ]
    blocks = [
        H('What newly built homes in Lower Landing have sold for'),
        P(f'Nearly every home that sold in Lower Landing over the past year was built in {th["yb"]} or {ho["yb"]}, so the sales figures are a fair guide to what new construction here costs once it is finished and resold. '
          f'The {th["n"]} townhomes sold at a median {money(th["price"])} (${th["ppsf"]} per square foot), taking {th["dom"]} days. '
          f'The {ho["n"]} houses sold at a median {money(ho["price"])}, about ${ho["ppsf"]} per square foot, on lots of a median {ho["lot_sqft"]:,} square feet, in {ho["dom"]} days. Neither group sold above list price.'),
        tbl('Lower Landing, Chilliwack: newly built homes that sold', ['Home type', 'Sold', 'Median price', 'Price per sq ft', 'Median bedrooms', 'Median days to sell', 'Sale price vs list'],
            [['Townhomes', num(th['n']), money(th['price']), f'${th["ppsf"]}', str(th['beds']), str(th['dom']), f'{th["ratio"]:.1f}%'],
             ['Houses', num(ho['n']), money(ho['price']), f'${ho["ppsf"]}', str(ho['beds']), str(ho['dom']), f'{ho["ratio"]:.1f}%']], SRC),
        H('Buying new in Lower Landing: taxes and protection'),
        P('A new home is taxed differently from a resale. The seller adds 5% GST to the price, a first-time buyer can recover it under the federal rebate (full rebate up to $1 million, partial up to $1.5 million), and BC property transfer tax is charged on the purchase price. '
          'The home also carries the builder warranty in BC: 2 years on labour and materials, 5 on the building envelope and 10 on the structure. The pages linked below explain each rule with the dates and limits.'),
    ]
    A.set_blocks('new-construction-lower-landing', G, blocks, end=True)
    faq_edit('new-construction-lower-landing', faqs)


# ------------------------------------------------------------------ homes-under-1500000
def homes_under_1_5m():
    rows = []; tot = {'house': [0, 0], 'townhome': [0, 0], 'condo': [0, 0]}
    for k, nm in CITY.items():
        if k in ('south-surrey', 'cloverdale'): continue   # inside the Surrey row
        g = AGG['city'][k]['groups']; r = [nm]
        for t, _ in TYPES:
            x = g.get(t)
            if not x or x['n'] < 5 or 'bands' not in x: r += ['—', '—']; continue
            b = x['bands']; u = sum(b[:5]); r += [num(x['n']), f'{round(100 * u / x["n"])}%']
            tot[t][0] += x['n']; tot[t][1] += u
        rows.append(r)
    share = {t: round(100 * v[1] / v[0]) for t, v in tot.items()}
    # where a house still costs under $1.5 million
    hm = sorted(((AGG['city'][k]['groups']['house']['price'], CITY[k], AGG['city'][k]['groups']['house']['n']) for k in CITY if 'house' in AGG['city'][k]['groups'] and AGG['city'][k]['groups']['house']['n'] >= 5 and k not in ('south-surrey', 'cloverdale')))
    under = [x for x in hm if x[0] < 1500000]; over = [x for x in hm if x[0] >= 1500000]
    rtab = [[nm, num(n), money(p), 'Yes' if p < 1500000 else 'No'] for p, nm, n in hm]
    bl = [
        H('How much of the market is under $1.5 million?'),
        P(f'Most of what sells in Metro Vancouver and the Fraser Valley sits under this price, but the share depends on the type of home. Across the cities in the table, {share["condo"]}% of condos, {share["townhome"]}% of townhomes and {share["house"]}% of houses closed under $1,500,000 between {WIN}. '
          f'Condos and townhomes make up almost all of the supply in the band; houses under $1.5 million are mostly in {under[0][1]}, {under[1][1]} and the other eastern and southern cities.'),
        tbl('Share of closed sales under $1,500,000, by city and home type', ['City', 'Houses sold', 'Under $1.5M', 'Townhomes sold', 'Under $1.5M', 'Condos sold', 'Under $1.5M'], rows,
            SRC + ' Surrey includes South Surrey and Cloverdale. A dash means fewer than 5 sales.'),
        H('Which cities have a median house price under $1.5 million?'),
        P(f'{len(under)} of {len(hm)} cities had a median house sale under $1,500,000: ' + ', '.join(f'{nm} ({money(p)})' for p, nm, _ in under) + '. '
          + ('In ' + ', '.join(nm for _, nm, _ in over) + ' the middle house sale was above the line, so a house under $1.5 million there is usually an older or smaller one.' if over else '')),
        tbl('Median house price by city', ['City', 'Houses sold', 'Median price', 'Under $1.5M'], rtab, SRC),
        H('Using the $1.5 million search'),
        P('The search above lists every active home at or under $1,500,000 across the cities Jared covers. Narrow it by city, type and bedrooms, and save it to get an email when a new home matches. '
          'Under $1.5 million the price is high enough that the home type matters more than the city: a new townhome and an older house can cost the same, with very different upkeep. Jared can show you both and the sold prices behind them.'),
    ]
    A.set_blocks('homes-under-1500000', G, bl, end=True)


# ------------------------------------------------------------------ sold-properties
def sold_properties():
    rows = []
    for k, nm in CITY.items():
        g = AGG['city'][k]['groups']
        for t, tl in TYPES:
            x = g.get(t)
            if x and x['n'] >= 5 and 'price' in x and k not in ('south-surrey', 'cloverdale'):
                rows.append((x['n'], nm, tl, x))
    rows.sort(key=lambda r: -r[0])
    tbl_rows = [[nm, tl, num(x['n']), money(x['price']), str(x['dom']), f'{x["ratio"]:.1f}%', f'{x["over"]}%'] for _, nm, tl, x in rows[:24]]
    qs = {t: sum(AGG['city'][k]['groups'][t]['n'] for k in CITY if k not in ('south-surrey', 'cloverdale') and t in AGG['city'][k]['groups']) for t, _ in TYPES}
    fastest = min(rows, key=lambda r: r[3]['dom']); slowest = max(rows, key=lambda r: r[3]['dom'])
    highest = max(rows, key=lambda r: r[3]['over'])
    bl = [
        H('What sold in the past year'),
        P(f'Between {WIN}, {sum(qs.values()):,} homes closed in the 12 cities and communities Jared tracks: {qs["condo"]:,} condos, {qs["house"]:,} houses and {qs["townhome"]:,} townhomes. '
          f'Prices and speed differ a lot by city and type. The quickest group in the table is {fastest[1]} {fastest[2].lower()}, with a median of {fastest[3]["dom"]} days to sell. The slowest is {slowest[1]} {slowest[2].lower()} at {slowest[3]["dom"]} days. '
          f'{highest[1]} {highest[2].lower()} had the largest share sold above the last list price, {highest[3]["over"]}%.'),
        tbl('Sold prices by city and home type, largest groups first', ['City', 'Type', 'Sold', 'Median price', 'Median days to sell', 'Sale price vs list', 'Sold above list'], tbl_rows,
            SRC + ' Surrey includes South Surrey and Cloverdale. Only the 24 largest groups are shown.'),
        H('How to read these figures'),
        P('A median is the middle sale price, so half the homes sold for more and half for less. Sale price versus list compares the closing price with the last list price. '
          'Neither figure says what a particular home would sell for, because condition, lot, floor plan and the strata building change the price a lot. A home evaluation from Jared uses the closest recent sales to yours, not a city average.'),
        P('For one neighbourhood or building, open that area page, which has its own sold-price tables. For your own home, the free evaluation page asks a few questions and Jared follows up with the sales that match it.'),
    ]
    A.set_blocks('sold-properties', G, bl, end=True)
    A.end_link('sold-properties', G + '-l', 'Sold prices by city', [(f'{nm} homes for sale and sold prices', f'{k}-homes-for-sale') for k, nm in CITY.items() if k not in ('south-surrey', 'cloverdale')])


# ------------------------------------------------------------------ gst-rebate-in-bc
def gst():
    items = [('First-time home buyer programs in BC', 'first-time-home-buyer-program'), ('How presales and new-home taxes work in BC', 'new-construction-presales-in-langley-bc'),
             ('Presale projects across the Fraser Valley and Metro Vancouver', 'presale-projects-fraser-valley-and-metro-vancouver'),
             ('South Surrey new construction and presales', 'south-surrey-new-construction-presales'), ('BC condo buying rules', 'bc-condo-buying-rules'),
             ('FAQ for home buyers in BC', 'faq-for-home-buyers-in-bc'), ('Free home evaluation', 'home-evaluation')]
    ok = [(t, s) for t, s in items if N.exists(s)]
    bl = [H('Where to use the GST rebate'), P('The rebate applies only to new or substantially renovated homes. These pages cover the first-time buyer programs, the presale projects the rebate most often applies to, and the rules for buying a condo in BC:'),
          {'t': 'list', 'items': [[N.lk(t, s)] for t, s in ok]}]
    A.set_blocks('gst-rebate-in-bc', G, bl, end=True)


def main():
    abbotsford_townhomes(); lower_landing(); ncs_lower_landing(); homes_under_1_5m(); sold_properties(); gst()
    print('gap fixes written')


if __name__ == '__main__':
    main()
