#!/usr/bin/env python3
"""Builds the 18 new search pages (price reduced, new this week, ocean/mountain view) as src/data/local/<slug>.json with a new_page header.

Numbers come only from the files already in the repo: SnapStats monthly figures (src/data/snapstats/<month>.json) and the Paragon closed-sales
aggregate (src/data/sold/sold-12m.json). Nothing is typed in by hand except the sourced geography notes in VIEWS. Each page carries one live
search (the id sits in src/data/idx-embeds.json 'pending' and is moved to 'pages' by build_idx_embeds.py once the page exists).
Idempotent: rewrites the whole file for each slug it owns (gen = 'srch').
"""
import json, os, re, glob, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
G = 'srch'
MONTH = '2026-10'
SN = json.load(open(f'src/data/snapstats/{MONTH}.json'))['areas']
SD = json.load(open('src/data/sold/sold-12m.json'))
WINDOW = SD['meta']['window']
MON = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
FULL = {'JAN':'January','FEB':'February','MAR':'March','APR':'April','MAY':'May','JUN':'June','JUL':'July','AUG':'August','SEP':'September','OCT':'October','NOV':'November','DEC':'December'}
SNAP_SRC = 'Source: SnapStats® monthly report for October 2026, built on MLS® data from the Greater Vancouver REALTORS® and the Fraser Valley Real Estate Board. Sales ratio is sales divided by active listings in the month.'
PAR_SRC = f'Source: Paragon closed sales, {WINDOW}. Pending sales are not counted. Median means the middle price. Sold vs list is the sale price as a percentage of the last list price. A figure is shown only where at least 5 homes sold.'

def exists(slug):
    return os.path.exists(f'src/data/pages/{slug}.json') or os.path.exists(f'src/data/local/{slug}.json')
def money(v): return '—' if v is None else f'${v:,.0f}'
def read(r):
    if r is None: return 'no sales ratio (too few sales)'
    return "buyer's market" if r < 12 else ('balanced market' if r <= 20 else "seller's market")
VAR = {
 'lead': ["A cut is easiest to judge against the market around it.", "Whether a cut is large or small depends on what the rest of the market is doing.", "The size of a price drop only makes sense next to the prices homes are actually closing at.", "Read each reduction against recent sales, not against the old asking price alone.", "To weigh a reduced price, start with how the surrounding market has been behaving."],
 'seller': ["A seller who has already cut the price is usually responding to that gap, so a drop of a few percent mostly puts the home where recent buyers have been paying; a larger one is worth asking about.",
            "Sellers who have already lowered their price are generally reacting to that gap, so a few percent off usually just brings a home level with recent sales, while a bigger cut deserves a question about why.",
            "A reduction of a few percent generally moves a home to where buyers have been paying, whereas a deeper one tells you the first price missed, and it is fair to ask by how much.",
            "Most small drops simply close the distance to recent sale prices. A large one means the home started well above the market, and the history of its price changes is worth asking for.",
            "In practice a modest cut aligns a home with what buyers have recently paid; a steep cut points to an early price that did not hold, which your agent can confirm from the listing history."],
 'areas': ["The areas where unsold detached homes are building up are the places price cuts show up first.", "Price cuts tend to appear first in the areas with the most unsold detached homes.", "Where stock is building up faster than it sells, sellers tend to reduce first.", "Reductions cluster in the areas where detached listings outnumber buyers.", "The areas holding the most unsold detached homes are where you are most likely to see a reduced price."],
 'ranges': ["Those are the ranges where a negotiated price below the list price is least surprising.", "In those ranges, an offer under the list price is the least likely to be a surprise to the seller.", "Buyers in those ranges have the most reason to expect room on price.", "Expect the most flexibility from sellers in those ranges.", "Offers below asking are most common in ranges like these."],
 'scale': ["{pick('scale', c)}", "SnapStats calls a sales ratio under 12% a buyer's market, 12% to 20% balanced and over 20% a seller's market.", "The scale runs from a buyer's market under 12%, through balanced at 12% to 20%, to a seller's market above 20%.", "A ratio of 12% to 20% counts as balanced; lower favours buyers and higher favours sellers.", "Ratios below 12% favour buyers, those from 12% to 20% are balanced, and anything higher favours sellers."],
}
def pick(k, c): return VAR[k][c['vi'] % 5]
def mos(inv, sold): return f'{inv / sold:.1f}' if sold else '—'
def lk(text, slug):
    return {'t': text, 'h': f'/{slug}.html'} if exists(slug) else {'t': text}
def linklist(pairs):
    items = [[{'t': t, 'h': f'/{s}.html'}] for t, s in pairs if exists(s)]
    return {'t': 'list', 'items': items, 'gen': G, 'pos': 'end'} if items else None
def mlabel(i, months):  # trend lists run Oct 2025 .. Oct 2026
    return f"{FULL[months[i]]} {2025 if i <= 2 else 2026}"

# ---------------------------------------------------------------- city configuration
CITIES = [
    dict(key='south-surrey-white-rock', snap='south-surrey-white-rock', name='South Surrey and White Rock', short='South Surrey/White Rock', tail='south-surrey-white-rock', where='South Surrey and White Rock',
         ids=('1450590', '1450596'), houses='south-surrey-houses-for-sale', condos='south-surrey-condos-for-sale', th='south-surrey-townhomes-for-sale', stats='south-surrey-white-rock-real-estate-market-stats', open='south-surrey-open-houses', sold='south-surrey'),
    dict(key='langley', snap='langley', name='Langley', short='Langley', tail='langley', where='Langley', ids=('1450591', '1450597'),
         houses='langley-houses-for-sale', condos='langley-condos-for-sale', th='langley-townhomes-for-sale', stats='langley-real-estate-market-stats', open='langley-open-houses'),
    dict(key='surrey', snap='surrey', name='Surrey', short='Surrey', tail='surrey', where='Surrey', ids=('1450592', '1450598'),
         houses='surrey-houses-for-sale', condos='surrey-condos-for-sale', th='surrey-townhomes-for-sale', stats='surrey-real-estate-market-stats', open='surrey-open-houses'),
    dict(key='abbotsford', snap='abbotsford', name='Abbotsford', short='Abbotsford', tail='abbotsford', where='Abbotsford', ids=('1450593', '1450599'),
         houses='abbotsford-houses-for-sale', condos='abbotsford-condos-for-sale', th='abbotsford-townhomes-for-sale', stats='abbotsford-real-estate-market-stats', open='abbotsford-open-houses'),
    dict(key='chilliwack', snap=None, name='Chilliwack', short='Chilliwack', tail='chilliwack', where='Chilliwack', ids=('1450594', '1450600'),
         houses='chilliwack-houses-for-sale', condos='chilliwack-condos-for-sale', th='chilliwack-townhomes-for-sale', stats='fraser-valley-market-stats', open='chilliwack-open-houses', sold='chilliwack'),
    dict(key='maple-ridge', snap='maple-ridge', name='Maple Ridge', short='Maple Ridge', tail='maple-ridge', where='Maple Ridge', ids=('1450595', '1450601'),
         houses='maple-ridge-houses-for-sale', condos='maple-ridge-condos-for-sale', th='maple-ridge-townhomes-for-sale', stats='maple-ridge-real-estate-market-stats', open='maple-ridge-open-houses'),
]
for i, c in enumerate(CITIES):
    c['vi'] = {'chilliwack': 0, 'maple-ridge': 4}.get(c['key'], i)
    c['pr'] = f'price-reduced-homes-{c["tail"]}'; c['nl'] = f'new-listings-this-week-{c["tail"]}'

def comm_slug(city, name):
    m = json.load(open('src/data/snapstats/_mapping.json'))['mapped']
    for s, (cc, nn) in m.items():
        if cc == city and nn == name and exists(s) and not s.endswith('-guide'): return s
    for s, (cc, nn) in m.items():
        if cc == city and nn == name and exists(s): return s
    return None

# ---------------------------------------------------------------- SnapStats-based pages
def best(bands, key, n=1, minsales=0, mininv=0, rev=False):
    xs = [b for b in bands if b['inventory'] >= mininv and b['sales'] >= minsales and b['ratio'] is not None]
    return sorted(xs, key=lambda b: (b[key], b['inventory']), reverse=rev)[:n]
def band_label(l):
    lo, hi = [x.strip().replace(',', '') for x in l.replace('$', '').split(' - ')] if ' - ' in l else (None, None)
    if lo is None: return l
    f = lambda v: f'${int(v):,}'
    return f'{f(lo)} to {f(hi)}' if lo != '0' else f'Up to {f(hi)}'
def top_inventory_bands(bands, n):
    return sorted([b for b in bands if b['inventory'] > 0], key=lambda b: -b['inventory'])[:n]

def snap_numbers(c):
    a = SN[c['snap']]; d, t = a['detached'], a['condo_townhome']
    o = dict(a=a, d=d, t=t)
    for k, s in (('d', d), ('t', t)):
        sm = s['summary']; tr = s['trend']
        o[k + 'price'], o[k + 'inv'], o[k + 'sold'] = sm['Sale Price']['cur'], sm['Inventory']['cur'], sm['Solds']['cur']
        o[k + 'ratio_ll'], o[k + 'dom'] = sm['Sale to List Price Ratio']['cur'], sm['Days on Market']['cur']
        o[k + 'sr'] = s['total']['ratio']
        o[k + 'mos'] = round(s['total']['inventory'] / s['total']['sales'], 1) if s['total']['sales'] else None
        o[k + 'inv_yoy'] = round((tr['inventory'][-1] / tr['inventory'][0] - 1) * 100) if tr['inventory'][0] else None
        o[k + 'sold_yoy'] = round((tr['solds'][-1] / tr['solds'][0] - 1) * 100) if tr['solds'][0] else None
        o[k + 'price_yoy'] = round((tr['price'][-1] / tr['price'][0] - 1) * 100) if tr['price'][0] else None
    return o

def pr_snap(c):
    n = snap_numbers(c); C = c['name']; d, t = n['d'], n['t']
    gap_d, gap_t = 100 - n['dratio_ll'], 100 - n['tratio_ll']
    bl = []
    bl.append({'t': 'p', 'text': f"This search lists {C} homes where the asking price has come down, pulled live from the MLS®. {pick('lead', c)} In October 2026 a typical {C} detached home sold for {money(n['dprice'])}, took {n['ddom']} days and closed at {n['dratio_ll']}% of its list price, with {n['dinv']} detached homes for sale and {n['dsold']} sold in the month.", 'gen': G})
    bl.append({'t': 'grid', 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': f"What a price drop means in {C} right now", 'gen': G})
    bl.append({'t': 'p', 'text': f"Detached homes in {C} have been selling about {gap_d}% under list price, and condos and townhomes {'about the same' if gap_t == gap_d else f'about {gap_t}% under'}. On the detached side the sales ratio was {n['dsr']}%, which SnapStats reads as a {read(n['dsr'])}. For condos and townhomes it was {n['tsr']}%, {'also' if read(n['tsr']) == read(n['dsr']) else 'which is'} a {read(n['tsr'])}. {pick('seller', c)}", 'gen': G})
    if n['dmos'] and n['tmos']:
        bl.append({'t': 'p', 'text': f"Supply is the other half. At October's pace the {n['dinv']} detached listings would take {n['dmos']} months to sell, and the {n['t']['total']['inventory']} condo and townhome listings {n['tmos']} months. Against October 2025, detached listings are {abs(n['dinv_yoy'])}% {'fewer' if n['dinv_yoy'] < 0 else 'more'} and detached sales {abs(n['dsold_yoy'])}% {'fewer' if n['dsold_yoy'] < 0 else 'more'}, which is the backdrop for how many price changes you will see.", 'gen': G})
    # communities table (detached)
    comms = [x for x in d['communities'] if x['inventory'] > 0 or x['sales'] > 0]
    comms.sort(key=lambda x: -x['inventory'])
    rows = [[x['name'], str(x['inventory']), str(x['sales']), (f"{x['ratio']}%" if x['ratio'] is not None else '—'), read(x['ratio']).replace(' (too few sales)', '')] for x in comms]
    if rows:
        slow = [x for x in comms if x['inventory'] >= 15 and x['ratio'] is not None and x['ratio'] < 12]
        slow.sort(key=lambda x: (x['ratio'], -x['inventory']))
        fast = [x for x in comms if x['sales'] >= 3 and x['ratio'] is not None]
        fast.sort(key=lambda x: -x['ratio'])
        bl.append({'t': 'h', 'level': 2, 'text': f"{C} detached homes by area: where buyers have room", 'gen': G})
        s1 = f"{pick('areas', c)} " + (f"In October that was {', '.join(f'{x['name']} ({x['inventory']} listings, {x['ratio']}% sales ratio)' for x in slow[:3])}." if slow else f"No area with 15 or more listings sold under a 12% ratio in October.")
        s2 = (f" The fastest-moving area was {fast[0]['name']}, at a {fast[0]['ratio']}% ratio on {fast[0]['sales']} sales, so cuts there tend to be small or short-lived." if fast else '')
        bl.append({'t': 'p', 'text': s1 + s2, 'gen': G})
        bl.append({'t': 'table', 'caption': f"{C} detached homes, October 2026, by area", 'head': ['Area', 'For sale', 'Sold in month', 'Sales ratio', 'Reading'], 'rows': rows, 'source': SNAP_SRC, 'gen': G})
    # price bands
    topinv = top_inventory_bands(d['price_bands'], 5)
    bl.append({'t': 'h', 'level': 2, 'text': f"Price ranges with the most unsold {C} detached homes", 'gen': G})
    sl = best(d['price_bands'], 'ratio', 3, mininv=20)
    bl.append({'t': 'p', 'text': f"The busiest price range for listings was {band_label(topinv[0]['label'])}, with {topinv[0]['inventory']} homes for sale and {topinv[0]['sales']} sold." + (f" The slowest of the well-stocked ranges were {'; '.join(f'{band_label(x['label'])} ({x['inventory']} for sale, {x['sales']} sold)' for x in sl)}. {pick('ranges', c)}" if sl else ''), 'gen': G})
    bl.append({'t': 'table', 'caption': f"{C} detached homes, October 2026, by price range", 'head': ['Price range', 'For sale', 'Sold in month', 'Months of supply', 'Sales ratio'],
               'rows': [[band_label(x['label']), str(x['inventory']), str(x['sales']), mos(x['inventory'], x['sales']), (f"{x['ratio']}%" if x['ratio'] is not None else '—')] for x in sorted(topinv, key=lambda b: int(b['label'].replace(',', '').split(' ')[0].replace('$','')))], 'source': SNAP_SRC + ' The five price ranges with the most listings are shown.', 'gen': G})
    # bedrooms + attached
    br = d['bedrooms']
    bl.append({'t': 'h', 'level': 2, 'text': f"Condos and townhomes in {C}", 'gen': G})
    tc = [x for x in t['communities'] if x['inventory'] >= 10]; tc.sort(key=lambda x: -x['inventory'])
    tb = top_inventory_bands(t['price_bands'], 1)[0]
    s = f"Condos and townhomes sold at a median {money(n['tprice'])} in {C}, after {n['tdom']} days. The most crowded price range was {band_label(tb['label'])}, with {tb['inventory']} for sale and {tb['sales']} sold."
    if tc: s += f" By area, {tc[0]['name']} had the most listings ({tc[0]['inventory']}, {tc[0]['sales']} sold)" + (f", then {tc[1]['name']} ({tc[1]['inventory']}, {tc[1]['sales']} sold)." if len(tc) > 1 else '.')
    bl.append({'t': 'p', 'text': s, 'gen': G})
    bl.append({'t': 'table', 'caption': f"{C} detached homes, October 2026, by bedroom count", 'head': ['Bedrooms', 'For sale', 'Sold in month', 'Months of supply', 'Sales ratio'],
               'rows': [[x['label'].replace('&', 'and'), str(x['inventory']), str(x['sales']), mos(x['inventory'], x['sales']), (f"{x['ratio']}%" if x['ratio'] is not None else '—')] for x in br], 'source': SNAP_SRC, 'gen': G})
    top_br = max(br, key=lambda x: x['inventory'])
    bl.append({'t': 'p', 'text': f"The largest group of detached listings in {C} by size was {top_br['label'].replace('&', 'and').lower()}, at {top_br['inventory']} for sale against {top_br['sales']} sold.", 'gen': G})
    faq = [
        dict(q=f"How much below asking are homes selling for in {C}?", a=f"SnapStats puts October 2026 at {n['dratio_ll']}% of list price for {C} detached homes ({gap_d}% below) and {n['tratio_ll']}% for condos and townhomes ({gap_t}% below)."),
        dict(q=f"Is {C} a buyer's market or a seller's market?", a=f"By the SnapStats reading, October 2026 was a {read(n['dsr'])} for detached homes ({n['dsr']}% sales ratio) and a {read(n['tsr'])} for condos and townhomes ({n['tsr']}%). {pick('scale', c)}"),
        dict(q=f"How long do {C} homes take to sell?", a=f"The typical {C} detached home took {n['ddom']} days to sell in October 2026, and a condo or townhome {n['tdom']} days."),
        dict(q=f"Which price range has the most unsold detached homes in {C}?", a=f"{band_label(topinv[0]['label'])}, with {topinv[0]['inventory']} detached homes for sale and {topinv[0]['sales']} sold in October 2026."),
    ]
    return bl, faq, n

def nl_snap(c):
    n = snap_numbers(c); C = c['name']; d, t = n['d'], n['t']
    dt, tt = d['trend'], t['trend']; months = dt['months']
    bl = []
    peak = max(range(13), key=lambda i: dt['solds'][i]); low = min(range(13), key=lambda i: dt['solds'][i])
    bl.append({'t': 'p', 'text': f"New listings in {C} come on the MLS® every day. This search shows the ones listed in the past week, live. To judge a fresh listing, it helps to know how quickly the market is clearing: in October 2026, {n['dsold']} detached homes and {n['t']['total']['sales']} condos and townhomes sold in {C}, and the typical detached home sold in {n['ddom']} days.", 'gen': G})
    bl.append({'t': 'grid', 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': f"How fast {C} homes sold over the past year", 'gen': G})
    bl.append({'t': 'p', 'text': f"Detached sales in {C} peaked at {dt['solds'][peak]} in {mlabel(peak, months)} and were lowest at {dt['solds'][low]} in {mlabel(low, months)}. Active detached listings moved between {min(dt['inventory'])} and {max(dt['inventory'])} over the same 13 months. In October 2026 the median detached sale price was {money(n['dprice'])}, which is {abs(n['dprice_yoy'])}% {'below' if n['dprice_yoy'] < 0 else 'above'} October 2025.", 'gen': G})
    rows = [[mlabel(i, months), str(dt['solds'][i]), str(dt['inventory'][i]), money(dt['price'][i]), str(tt['solds'][i]), str(tt['inventory'][i])] for i in range(12, -1, -1)]
    bl.append({'t': 'table', 'caption': f"{C}: sales and listings by month, detached and condos/townhomes", 'head': ['Month', 'Detached sold', 'Detached for sale', 'Detached median price', 'Condo/townhome sold', 'Condo/townhome for sale'], 'rows': rows, 'source': SNAP_SRC, 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': f"How long a new {C} listing may sit", 'gen': G})
    fast = best(d['price_bands'], 'ratio', 3, minsales=5, rev=True)
    fastT = best(t['price_bands'], 'ratio', 2, minsales=5, rev=True)
    bl.append({'t': 'p', 'text': f"Months of supply is the number of months it would take to sell today's listings at the current pace. For {C} detached homes it was {n['dmos']} months in October 2026 and for condos and townhomes {n['tmos']}. The fastest detached price ranges were " + '; '.join(f"{band_label(x['label'])} ({x['ratio']}% sales ratio on {x['sales']} sales)" for x in fast) + ". " + (f"For condos and townhomes the quickest were " + ' and '.join(f"{band_label(x['label'])} ({x['ratio']}%)" for x in fastT) + '.' if fastT else ''), 'gen': G})
    ac = [x for x in d['communities'] if x['sales'] >= 3 and x['ratio'] is not None]; ac.sort(key=lambda x: -x['ratio'])
    sl = [x for x in d['communities'] if x['inventory'] >= 15 and x['ratio'] is not None]; sl.sort(key=lambda x: x['ratio'])
    if ac and sl:
        bl.append({'t': 'p', 'text': f"By area, new detached listings met the strongest demand in {', '.join(f'{x['name']} ({x['ratio']}%)' for x in ac[:3])}. The areas with the most stock relative to sales were {', '.join(f'{x['name']} ({x['ratio']}%)' for x in sl[:3])}, so a fresh listing there is likely to have company.", 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': f"{C} against last year", 'gen': G})
    bl.append({'t': 'p', 'text': f"Compared with October 2025, October 2026 had {abs(n['dinv_yoy'])}% {'fewer' if n['dinv_yoy'] < 0 else 'more'} detached homes for sale in {C} and {abs(n['dsold_yoy'])}% {'fewer' if n['dsold_yoy'] < 0 else 'more'} detached sales. Condos and townhomes had {abs(n['tinv_yoy'])}% {'fewer' if n['tinv_yoy'] < 0 else 'more'} for sale and {abs(n['tsold_yoy'])}% {'fewer' if n['tsold_yoy'] < 0 else 'more'} sales. The detached sale price moved {abs(n['dprice_yoy'])}% {'down' if n['dprice_yoy'] < 0 else 'up'} and the condo and townhome price {abs(n['tprice_yoy'])}% {'down' if n['tprice_yoy'] < 0 else 'up'}.", 'gen': G})
    faq = [
        dict(q=f"How many homes sold in {C} last month?", a=f"In October 2026, {n['dsold']} detached homes and {n['t']['total']['sales']} condos and townhomes sold in {C} (SnapStats)."),
        dict(q=f"How many months of supply does {C} have?", a=f"About {n['dmos']} months for detached homes and {n['tmos']} months for condos and townhomes in October 2026, measured as homes for sale divided by homes sold in the month."),
        dict(q=f"What was the busiest month for {C} home sales this past year?", a=f"For detached homes it was {mlabel(peak, months)}, with {dt['solds'][peak]} sales; the quietest was {mlabel(low, months)}, with {dt['solds'][low]}."),
        dict(q=f"Which {C} price range sells fastest?", a=f"For detached homes, {band_label(fast[0]['label'])}, with a {fast[0]['ratio']}% sales ratio on {fast[0]['sales']} sales in October 2026."),
    ]
    return bl, faq, n

# ---------------------------------------------------------------- Paragon-based pages (Chilliwack has no SnapStats report)
TYPES = [('house', 'houses'), ('townhome', 'townhomes'), ('condo', 'condos'), ('duplex', 'duplexes'), ('mobile', 'manufactured homes')]
BANDS = ['Under $600,000', '$600,000 to $799,999', '$800,000 to $999,999', '$1,000,000 to $1,199,999', '$1,200,000 to $1,499,999', '$1,500,000 to $1,799,999', '$1,800,000 and over']
QUARTERS = ['Nov 2025 to Jan 2026', 'Feb to Apr 2026', 'May to Jul 2026', 'Aug to Oct 2026']

def sold_rows(entries):
    rows = []
    for label, s in entries:
        for g, gl in TYPES[:3]:
            x = s['groups'].get(g)
            if x and x['n'] >= 5 and x.get('price'):
                rows.append([label, gl.capitalize(), str(x['n']), money(x['price']), str(x['dom']), f"{x['ratio']:.1f}%"])
    return rows

def pr_sold(c):
    city = SD['city'][c['sold']]; g = city['groups']; C = c['name']
    h, tw, co = g['house'], g.get('townhome'), g.get('condo')
    bl = [{'t': 'p', 'text': f"This search lists {C} homes where the asking price has come down, pulled live from the MLS®. To read a cut, compare it with what {C} homes actually sell for. From {WINDOW}, {h['n']} {C} houses sold at a median {money(h['price'])} after {h['dom']} days, and they closed at {h['ratio']:.1f}% of the last list price, with {h['over']}% selling above it.", 'gen': G},
          {'t': 'grid', 'gen': G},
          {'t': 'h', 'level': 2, 'text': f"What a price drop means in {C}", 'gen': G}]
    gaps = {k: round(100 - g[k]['ratio'], 1) for k, _ in TYPES if k in g and g[k].get('ratio') and g[k]['n'] >= 5}
    bl.append({'t': 'p', 'text': f"{C} homes have been closing close to their last list price: {', '.join(f'{gl} {100 - gaps[k]:.1f}%' for k, gl in TYPES if k in gaps)} of it. So the gap between asking and selling is small, about {gaps['house']} percentage points for houses, and a listing that has already dropped is competing with sales that closed within a few percent of the price they last carried. A cut of more than that is a sign the first price was out of line, and it is worth asking what happened between the first price and the current one.", 'gen': G})
    rows = []
    for k, gl in TYPES:
        x = g.get(k)
        if x and x['n'] >= 5: rows.append([gl.capitalize(), str(x['n']), money(x['price']), str(x['dom']), f"{x['ratio']:.1f}%", f"{x['over']}%"])
    bl.append({'t': 'table', 'caption': f"{C}: what sold, by home type", 'head': ['Home type', 'Sold', 'Median price', 'Days to sell', 'Sold vs list', 'Sold over list'], 'rows': rows, 'source': PAR_SRC, 'gen': G})
    slow = max([(k, gl) for k, gl in TYPES if k in g and g[k]['n'] >= 5], key=lambda kg: g[kg[0]]['dom'])
    quick = min([(k, gl) for k, gl in TYPES if k in g and g[k]['n'] >= 5], key=lambda kg: g[kg[0]]['dom'])
    bl.append({'t': 'p', 'text': f"{slow[1].capitalize()} took the longest to sell, at {g[slow[0]]['dom']} days, and {quick[1]} the shortest at {g[quick[0]]['dom']} days. Home types that sit longer are where a price drop is more common and a lower offer more likely to be heard.", 'gen': G})
    subs = city['subs']
    srows = []
    for key in subs:
        s = SD['sub'][key]; x = s['groups'].get('house')
        if x and x['n'] >= 5 and x.get('price'): srows.append((key.split('|')[1], x))
    srows.sort(key=lambda r: -r[1]['n'])
    bl.append({'t': 'h', 'level': 2, 'text': f"{C} houses by neighbourhood", 'gen': G})
    if srows:
        lo = min(srows, key=lambda r: r[1]['dom']); hi = max(srows, key=lambda r: r[1]['dom'])
        bl.append({'t': 'p', 'text': f"Neighbourhoods with at least 5 house sales are listed below. {hi[0]} houses were slowest, at {hi[1]['dom']} days, and {lo[0]} the quickest at {lo[1]['dom']}. Where the days to sell run longer, buyers have had more time and more room to negotiate.", 'gen': G})
        bl.append({'t': 'table', 'caption': f"{C} houses sold, by neighbourhood", 'head': ['Neighbourhood', 'Sold', 'Median price', 'Days to sell', 'Sold vs list'], 'rows': [[n, str(x['n']), money(x['price']), str(x['dom']), f"{x['ratio']:.1f}%"] for n, x in srows], 'source': PAR_SRC, 'gen': G})
    faq = [dict(q=f"How much below asking are {C} homes selling for?", a=f"From {WINDOW}, {C} houses closed at a median {h['ratio']:.1f}% of the last list price, townhomes at {tw['ratio']:.1f}% and condos at {co['ratio']:.1f}%." if tw and co else f"{C} houses closed at a median {h['ratio']:.1f}% of the last list price."),
           dict(q=f"How long do {C} houses take to sell?", a=f"The median was {h['dom']} days for houses, {tw['dom']} for townhomes and {co['dom']} for condos, for sales from {WINDOW}." if tw and co else f"The median was {h['dom']} days for houses."),
           dict(q=f"How many {C} houses sell above the list price?", a=f"{h['over']}% of {C} houses sold above their last list price from {WINDOW}, against {tw['over']}% of townhomes and {co['over']}% of condos." if tw and co else f"{h['over']}% sold above their last list price.")]
    return bl, faq, g

def nl_sold(c):
    city = SD['city'][c['sold']]; g = city['groups']; C = c['name']; h = g['house']
    qs = h['q']; bands = h['bands']; tot = sum(bands)
    bl = [{'t': 'p', 'text': f"New listings in {C} come on the MLS® every day, and this search shows the ones listed in the past week. How fast a fresh listing sells depends on its price and type. From {WINDOW}, {h['n']} {C} houses sold in a median {h['dom']} days, {g['townhome']['n']} townhomes in {g['townhome']['dom']} and {g['condo']['n']} condos in {g['condo']['dom']}.", 'gen': G},
          {'t': 'grid', 'gen': G},
          {'t': 'h', 'level': 2, 'text': f"Where {C} house sales have been priced", 'gen': G}]
    big = max(range(7), key=lambda i: bands[i]); sm = [i for i in range(7) if bands[i]]
    bl.append({'t': 'p', 'text': f"The largest group of {C} house sales, {bands[big]} of {tot}, closed in the {BANDS[big].lower() if BANDS[big][0] != '$' else BANDS[big]} range, and {sum(bands[:3])} of {tot} closed under $1,000,000. At the other end, {bands[6]} sold at $1,800,000 or more.", 'gen': G})
    bl.append({'t': 'table', 'caption': f"{C} houses sold, by price range", 'head': ['Price range', 'Houses sold', 'Share of sales'], 'rows': [[BANDS[i], str(bands[i]), f"{bands[i] * 100 / tot:.0f}%"] for i in range(7)], 'source': PAR_SRC, 'gen': G})
    if all(x['n'] >= 5 for x in qs):
        bl.append({'t': 'h', 'level': 2, 'text': f"{C} house sales through the year", 'gen': G})
        mx = max(range(4), key=lambda i: qs[i]['n']); mn = min(range(4), key=lambda i: qs[i]['n'])
        bl.append({'t': 'p', 'text': f"House sales were busiest from {QUARTERS[mx]}, at {qs[mx]['n']}, and quietest from {QUARTERS[mn]}, at {qs[mn]['n']}. The median price over those quarters ran from {money(min(x['price'] for x in qs))} to {money(max(x['price'] for x in qs))}. This is a count of closed sales, so it trails what is being listed today.", 'gen': G})
        bl.append({'t': 'table', 'caption': f"{C} houses sold, by quarter", 'head': ['Period', 'Sold', 'Median price'], 'rows': [[QUARTERS[i], str(qs[i]['n']), money(qs[i]['price'])] for i in range(4)], 'source': PAR_SRC, 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': f"How long each {C} home type takes to sell", 'gen': G})
    rows = [[gl.capitalize(), str(g[k]['n']), str(g[k]['dom']), f"{g[k]['over']}%"] for k, gl in TYPES if k in g and g[k]['n'] >= 5]
    srt = sorted([(g[k]['dom'], gl) for k, gl in TYPES if k in g and g[k]['n'] >= 5])
    bl.append({'t': 'p', 'text': f"{srt[0][1].capitalize()} were the quickest to sell in {C}, at a median {srt[0][0]} days, and {srt[-1][1]} the slowest at {srt[-1][0]}. Compare a new listing with sales of its own type, not just its neighbourhood.", 'gen': G})
    bl.append({'t': 'table', 'caption': f"{C}: days to sell and share sold over list, by home type", 'head': ['Home type', 'Sold', 'Days to sell', 'Sold over list'], 'rows': rows, 'source': PAR_SRC, 'gen': G})
    faq = [dict(q=f"How fast do new listings sell in {C}?", a=f"From {WINDOW}, the median was {h['dom']} days for {C} houses, {g['townhome']['dom']} for townhomes and {g['condo']['dom']} for condos."),
           dict(q=f"What price range sells the most houses in {C}?", a=f"{BANDS[big]}, with {bands[big]} of {tot} house sales from {WINDOW}."),
           dict(q=f"How many {C} houses sold this past year?", a=f"{h['n']} houses sold from {WINDOW}, plus {g['townhome']['n']} townhomes and {g['condo']['n']} condos.")]
    return bl, faq, g

# ---------------------------------------------------------------- page assembly (market pages)
def assemble(c, kind):
    snap = c['snap'] is not None
    bl, faq, _ = (pr_snap(c) if kind == 'pr' else nl_snap(c)) if snap else (pr_sold(c) if kind == 'pr' else nl_sold(c))
    C = c['name']; slug = c[kind]
    first = next(b for b in bl if b['t'] == 'p')
    if kind == 'pr':
        title = f"Price Reduced Homes in {c['short']} | Jared Gibbons"; h1 = f"Price Reduced Homes for Sale in {c['short']}"
        if snap:
            n = snap_numbers(c)
            desc = f"Price reduced homes for sale in {C}: live MLS® price drops, plus how {C} detached homes sold at {n['dratio_ll']}% of list in October 2026."
        else:
            g = SD['city'][c['sold']]['groups']['house']; desc = f"Price reduced homes for sale in {C}: live MLS® price drops, plus how {C} houses sold at {g['ratio']:.1f}% of list over the past year."
    else:
        title = f"New Listings This Week in {c['short']} | Jared Gibbons"; h1 = f"New Listings This Week in {c['short']}"
        if snap:
            n = snap_numbers(c); desc = f"New listings this week in {C}, live from the MLS®, with the numbers behind them: {n['dsold']} detached sales and {n['ddom']} days to sell in October 2026."
        else:
            g = SD['city'][c['sold']]['groups']['house']; desc = f"New listings this week in {C}, live from the MLS®, with the numbers behind them: houses sold in {g['dom']} days over the past year."
    other = c['nl'] if kind == 'pr' else c['pr']
    pairs = [(h1 if False else (f"New listings this week in {c['short']}" if kind == 'pr' else f"Price reduced homes in {c['short']}"), other),
             (f"{C} houses for sale", c['houses']), (f"{C} condos for sale", c['condos']), (f"{C} townhomes for sale", c['th']),
             (f"{C} real estate market stats", c['stats']), (f"{C} open houses", c['open'])]
    sibs = [(f"{'Price reduced homes' if kind == 'pr' else 'New listings this week'} in {x['short']}", x[kind]) for x in CITIES if x is not c]
    end = [{'t': 'h', 'level': 2, 'text': f"More {C} searches", 'gen': G, 'pos': 'end'}, linklist(pairs),
           {'t': 'h', 'level': 2, 'text': f"{'Price reduced homes' if kind == 'pr' else 'New listings this week'} in nearby cities", 'gen': G, 'pos': 'end'}, linklist(sibs)]
    bl += [b for b in end if b]
    if snap: bl.append({'t': 'notice', 'text': f"Market figures are SnapStats® numbers for October 2026 and update monthly. The listings above update live from the MLS®.", 'gen': G, 'pos': 'end'})
    return slug, dict(status='generated', slug=slug, updated='2026-11-04', new_page=dict(title=title, description=desc, h1=h1),
                      breadcrumbs=[{'name': 'Home', 'href': '/index.html'}, {'name': f'{C} homes', 'href': f'/{c["houses"]}.html'}, {'name': h1, 'href': f'/{slug}.html'}],
                      faq_heading=f"{h1}: your questions answered", faq=[dict(f, gen=G) for f in faq], blocks=bl)

# ---------------------------------------------------------------- view pages (sourced geography + Paragon sub-area numbers)
def find_sub(name, area=None):
    for k in SD['sub']:
        a, n = k.split('|')
        if n == name and (area is None or a == area): return k
    return None

VIEWS = json.load(open('tools/data/view-pages.json'))

def view_page(v):
    bl = []
    bl.append({'t': 'p', 'text': v['intro'], 'gen': G})
    bl.append({'t': 'grid', 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': v['h_place'], 'gen': G})
    for ptxt in v['place']: bl.append({'t': 'p', 'text': ptxt, 'gen': G})
    bl.append({'t': 'list', 'items': [[{'t': x}] for x in v['facts']], 'gen': G})
    # numbers
    entries, links = [], []
    for nm, disp, slug in v['subs']:
        k = find_sub(nm, v.get('area_of', {}).get(nm))
        if k: entries.append((disp, SD['sub'][k]))
        if slug and exists(slug): links.append((disp, slug))
    rows = sold_rows(entries)
    bl.append({'t': 'h', 'level': 2, 'text': v['h_sold'], 'gen': G})
    if rows:
        by = {}
        for r in rows:
            if r[1] == 'Houses': by[r[0]] = r
        pr = sorted(by.values(), key=lambda r: -int(r[3].replace('$', '').replace(',', '')))
        txt = v['sold_intro']
        if pr: txt += f" Among the houses, the highest median was {pr[0][3]} in {pr[0][0]} ({pr[0][2]} sold) and the lowest {pr[-1][3]} in {pr[-1][0]} ({pr[-1][2]} sold)."
        bl.append({'t': 'p', 'text': txt, 'gen': G})
        bl.append({'t': 'table', 'caption': v['table_caption'], 'head': ['Area', 'Type', 'Sold', 'Median price', 'Days to sell', 'Sold vs list'], 'rows': rows, 'source': PAR_SRC, 'gen': G})
    if v.get('snap'):
        a, nm = v['snap']; comm = next((x for x in SN[a]['detached']['communities'] if x['name'] == nm), None)
        if comm:
            bl.append({'t': 'p', 'text': f"On SnapStats' October 2026 count, {nm} had {comm['inventory']} detached homes for sale and {comm['sales']} sold, a sales ratio of {comm['ratio']}%, which reads as a {read(comm['ratio'])}." if comm['ratio'] is not None else f"On SnapStats' October 2026 count, {nm} had {comm['inventory']} detached homes for sale and {comm['sales']} sold.", 'gen': G})
    bl.append({'t': 'p', 'text': v['sold_caveat'], 'gen': G})
    bl.append({'t': 'h', 'level': 2, 'text': v['h_check'], 'gen': G})
    bl.append({'t': 'p', 'text': v['check_intro'], 'gen': G})
    bl.append({'t': 'list', 'items': [[{'t': x}] for x in v['checks']], 'gen': G})
    ll = [(t, s) for t, s in links] + [(t, s) for t, s in v.get('more', [])]
    end = [{'t': 'h', 'level': 2, 'text': v['h_links'], 'gen': G, 'pos': 'end'}, linklist(ll)]
    bl += [b for b in end if b]
    slug = v['slug']
    faq = list(v['faq'])
    if entries:
        disp, s0 = entries[0]; h0 = s0['groups'].get('house')
        if h0 and h0['n'] >= 5 and h0.get('price'):
            faq.insert(0, dict(q=f"What do houses in {disp} sell for?", a=f"{h0['n']} houses sold in {disp} from {WINDOW}, at a median {money(h0['price'])} after {h0['dom']} days and {h0['ratio']:.1f}% of the last list price. That covers every house in the area, not only those with a view."))
    return slug, dict(status='generated', slug=slug, updated='2026-11-04', new_page=dict(title=v['title'], description=v['description'], h1=v['h1']),
                      breadcrumbs=[{'name': 'Home', 'href': '/index.html'}, {'name': v['crumb'][0], 'href': f"/{v['crumb'][1]}.html"}, {'name': v['h1'], 'href': f'/{slug}.html'}],
                      faq_heading=f"{v['h1']}: your questions answered", faq=[dict(f, gen=G) for f in faq], blocks=bl)

def inbound():
    """Links from existing pages to the new ones (links-only lists, so they do not change a page's uniqueness)."""
    T = {}
    for c in CITIES:
        for host in (c['houses'], c['condos'], c['th'], c['open']):
            T.setdefault(host, []).extend([(f"Price reduced homes in {c['short']}", c['pr']), (f"New listings this week in {c['short']}", c['nl'])])
    V = {'crescent-bch-ocean-pk': [('Ocean view homes in Crescent Beach and Ocean Park', 'ocean-view-homes-crescent-beach-ocean-park')],
         'crescent-beach-ocean-park-guide': [('Ocean view homes in Crescent Beach and Ocean Park', 'ocean-view-homes-crescent-beach-ocean-park')],
         'south-surrey-white-rock-ocean-view-homes-for-sale': [('Ocean view homes in Crescent Beach and Ocean Park', 'ocean-view-homes-crescent-beach-ocean-park')],
         'tsawwassen-houses-for-sale': [('Ocean view homes in Tsawwassen', 'ocean-view-homes-tsawwassen')], 'tsawwassen-homes-for-sale': [('Ocean view homes in Tsawwassen', 'ocean-view-homes-tsawwassen')],
         'cliff-drive': [('Ocean view homes in Tsawwassen', 'ocean-view-homes-tsawwassen')], 'burke-mountain-homes-for-sale': [('Mountain view homes on Burke Mountain', 'mountain-view-homes-burke-mountain')],
         'burke-mountain': [('Mountain view homes on Burke Mountain', 'mountain-view-homes-burke-mountain')],
         'silver-valley': [('Mountain view homes in Maple Ridge', 'mountain-view-homes-maple-ridge')], 'eastern-hillsides': [('Mountain view homes in Chilliwack', 'mountain-view-homes-chilliwack')],
         'promontory': [('Mountain view homes in Chilliwack', 'mountain-view-homes-chilliwack')], 'abbotsford-east': [('Mountain view homes in Abbotsford', 'mountain-view-homes-abbotsford')]}
    for h, l in V.items(): T.setdefault(h, []).extend(l)
    V2 = {'maple-ridge-houses-for-sale': ('Mountain view homes in Maple Ridge', 'mountain-view-homes-maple-ridge'), 'chilliwack-houses-for-sale': ('Mountain view homes in Chilliwack', 'mountain-view-homes-chilliwack'),
          'abbotsford-houses-for-sale': ('Mountain view homes in Abbotsford', 'mountain-view-homes-abbotsford')}
    for h, l in V2.items(): T.setdefault(h, []).append(l)
    n = 0
    for host, pairs in T.items():
        if not os.path.exists(f'src/data/pages/{host}.json') and not os.path.exists(f'src/data/local/{host}.json'): continue
        f = f'src/data/local/{host}.json'
        raw = open(f).read() if os.path.exists(f) else ''
        j = json.loads(raw) if raw else {'status': 'generated', 'slug': host, 'updated': '2026-11-04', 'blocks': []}
        j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'srchlinks']
        seen, items = set(), []
        for t, sl in pairs:
            if sl in seen or not exists(sl): continue
            seen.add(sl); items.append([{'t': t, 'h': f'/{sl}.html'}])
        if not items: continue
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Price reductions, new listings and views', 'gen': 'srchlinks', 'pos': 'end'}, {'t': 'list', 'items': items, 'gen': 'srchlinks', 'pos': 'end'}]
        ind = (len(raw.split('\n')[1]) - len(raw.split('\n')[1].lstrip())) if raw.count('\n') > 1 else 1
        json.dump(j, open(f, 'w'), indent=ind or 1, ensure_ascii='\\u' in raw); n += 1
    print(n, 'pages link to the new searches')

def main():
    out = {}
    for c in CITIES:
        for kind in ('pr', 'nl'):
            s, j = assemble(c, kind); out[s] = j
    for v in VIEWS:
        s, j = view_page(v); out[s] = j
    for s, j in out.items():
        json.dump(j, open(f'src/data/local/{s}.json', 'w'), indent=1, ensure_ascii=False)
    print(len(out), 'pages written')
    inbound()

if __name__ == '__main__':
    main()
