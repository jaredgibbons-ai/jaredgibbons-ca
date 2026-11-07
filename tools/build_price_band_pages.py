#!/usr/bin/env python3
"""Price-band search pages (2026-11-07), lead-machine item 2: "<City> homes under $1 million", "under $1.2 million", "<City> condos under $600,000".

20 new draft pages. Figures come from the closed and pending extras layer (price bands per city, Pete's export to October 31, 2026) and the 12-month neighbourhood layer.
Each page has its own band table, neighbourhood table and quarter table, so the pages do not repeat each other.  The searches are Jerry's: docs/review/idx/price-band-searches-2026-11-07.xlsx,
returned as ...-DONE.xlsx and wired by tools/build_idx_embeds.py.
python3 -I tools/build_price_band_pages.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_extras_pages as X
import build_area_gap_pages as A
from build_new_searches import money, num, lk, subrows

G = 'band'
EXW = X.EXW
P = lambda t: {'t': 'p', 'text': t, 'gen': G}
H = lambda t, l=2: {'t': 'h', 'level': l, 'text': t, 'gen': G}
def tbl(cap, head, rows, src=None):
    b = {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'gen': G}
    if src: b['source'] = src
    return b
BANDL = N.BANDS
UP = [599999, 799999, 999999, 1199999]   # top of the first four price bands
SRC = lambda nm, noun, n: f'Source: Paragon MLS®, {n:,} {nm} {noun} in closed and pending sales, {EXW}. A pending sale is firm but has not completed, so its price can still change. Medians use at least 5 sales.'

# key -> (display, MLS area for the saved search, boards for the neighbourhood table, hub page)
CITY = {
    'surrey': ('Surrey', 'Surrey + North Surrey', ['Surrey', 'North Surrey'], 'surrey-homes-for-sale'),
    'langley': ('Langley', 'Langley', ['Langley'], 'langley-homes-for-sale'),
    'abbotsford': ('Abbotsford', 'Abbotsford', ['Abbotsford'], 'abbotsford-homes-for-sale'),
    'chilliwack': ('Chilliwack', 'Chilliwack + Sardis', ['Chilliwack', 'Sardis'], 'chilliwack-homes-for-sale'),
    'mission': ('Mission', 'Mission', ['Mission'], 'mission-homes-for-sale'),
    'maple-ridge': ('Maple Ridge', 'Maple Ridge', ['Maple Ridge'], 'maple-ridge-homes-for-sale'),
    'north-delta': ('North Delta', 'N. Delta', ['N. Delta'], 'north-delta-homes-for-sale'),
    'burnaby': ('Burnaby', 'Burnaby North + Burnaby South + Burnaby East', ['Burnaby North', 'Burnaby South', 'Burnaby East'], 'burnaby-homes-for-sale'),
    'richmond': ('Richmond', 'Richmond', ['Richmond'], 'richmond-homes-for-sale'),
    'coquitlam': ('Coquitlam', 'Coquitlam', ['Coquitlam'], 'coquitlam-homes-for-sale'),
    'new-westminster': ('New Westminster', 'New Westminster', ['New Westminster'], 'new-westminster-homes-for-sale'),
    'vancouver': ('Vancouver', 'Vancouver West + Vancouver East', ['Vancouver West', 'Vancouver East'], 'vancouver-homes-for-sale'),
}
# (slug suffix, type, cap, number of price bands under the cap, cap in words, short cap, noun)
KINDS = {
    'h1m': ('homes-under-1m', 'house', 1000000, 3, '$1 million', '$1,000,000', 'houses'),
    'h12': ('homes-under-1-2m', 'house', 1200000, 4, '$1.2 million', '$1,200,000', 'houses'),
    'c600': ('condos-under-600k', 'condo', 600000, 1, '$600,000', '$600,000', 'condos'),
}
PAGES = [(c, 'h1m') for c in ('abbotsford', 'chilliwack', 'mission', 'maple-ridge', 'surrey', 'langley')] + \
        [(c, 'h12') for c in ('surrey', 'langley', 'maple-ridge', 'north-delta')] + \
        [(c, 'c600') for c in ('surrey', 'langley', 'abbotsford', 'chilliwack', 'maple-ridge', 'burnaby', 'richmond', 'coquitlam', 'new-westminster', 'vancouver')]
QLAB = ['November 2025 to January 2026', 'February to April 2026', 'May to July 2026', 'August to October 2026']


def build(ck, kk):
    nm, mls, boards, hub = CITY[ck]; suf, typ, cap, k, capw, caps, noun = KINDS[kk]
    slug = f'{ck}-{suf}'
    g = N.EX['city'][ck]['groups'][typ]; bd = g['bands']; n = g['n']; under = sum(bd[:k]); sh = round(100 * under / n)
    rows = [r for r in subrows(boards, typ, 5) if r['price']]
    rows.sort(key=lambda r: r['price']); below = [r for r in rows if r['price'] < cap]
    half = max(4, (len(rows) + 1) // 2)
    base = rows[:min(8, half)]
    if kk == 'h12':   # the other half of the city's neighbourhoods, nearest the cap first, so the table never repeats the $1 million page of the same city
        names1 = {r['name'] for r in base}
        rest = [r for r in rows if r['name'] not in names1]
        cheap = sorted(rest, key=lambda r: abs(r['price'] - cap))[:10]; cheap.sort(key=lambda r: r['price'])
        if len(cheap) < 3: cheap = rows[:10]
    else:
        cheap = base if typ == 'house' else rows[:10]
    busy = sorted(rows, key=lambda r: -r['n'])[:8]
    hs = 'house' if typ == 'house' else 'condo'
    seo_t = {'house': f'{nm} Homes Under {capw.replace(" million", "M") if "million" in capw else capw} | Houses for Sale', 'condo': f'{nm} Condos Under {capw} | Apartments for Sale'}[typ]
    h1 = f'{nm} Homes for Sale Under {capw}' if typ == 'house' else f'{nm} Condos for Sale Under {capw}'
    d1 = f'Search {nm} {noun} for sale under {caps}. {sh}% of the {n:,} {noun} that sold here in the past year went for less. See the median price, the areas and how fast they sold.'
    d2 = f'Search {nm} {noun} for sale under {caps}. {sh}% of the {n:,} sold in the past year went for less. See the median price, the areas and how fast they sold.'
    d3 = f'Search {nm} {noun} for sale under {caps}. See what share sold below that price, the median, the areas that sell for less and how fast homes sold.'
    seo = dict(title=A.title_of(seo_t, f'{nm} {noun.title()} Under {capw}', f'{nm} Homes Under {capw}'), h1=h1, crumb=f'{nm} {noun} under {capw}', links_h=f'More {nm} real estate by price and type',
               description=A.fit(d1, d2, d3, f'Search {nm} {noun} for sale under {caps}. See what share sold below that price, the median, which areas sell for less and how long homes took to sell.'))
    ratio = f'{g["ratio"]}%' if g.get('ratio') else None
    dom = g.get('dom'); over = g.get('over')
    cheapest, dearest = (cheap[0], cheap[-1]) if cheap else (None, None)
    src = lambda what: f'Source: Paragon MLS®, {what}, closed and pending, {EXW}, with the price cut-off at {caps}.'
    srcn = lambda what, who: f'Source: Paragon MLS®, {what} {who}, closed sales, {N.WINDOW}, compared with {caps}.'
    h1m_n = sum(bd[:3]); step = under - h1m_n
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Figures are Paragon closed and pending sales to October 31, 2026. A pending sale is firm but has not completed, so its price can still change. A median is shown only where at least 5 homes sold. The live search is not connected yet (Jerry’s saved search, price filter ' + caps + ').', 'gen': G}]
    # opening
    top = BANDL[max(range(len(bd)), key=lambda i: bd[i])].lower()
    if kk == 'h12':
        bl += [P(f'In {nm}, {under:,} of the {n:,} {noun} ({sh}%) sold under {caps}: {h1m_n:,} for less than $1,000,000 and {step:,} more between $1,000,000 and {money(cap - 1)}. '
                  f'The busiest price range, {top}, had {max(bd):,} sales.')]
    else:
        bl += [P(f'In {nm}, {under:,} of the {n:,} {noun} ({sh}%) sold under {caps}. The median was {money(g["price"])}'
                 + (f', with the middle half between {money(g["p25"])} and {money(g["p75"])}' if g.get('p25') else '') + '. '
                 + f'The busiest price range, {top}, had {max(bd):,} sales.')]
    if kk == 'h12' and g.get('p25'):
        bl += [P(f'The lower quarter of {nm} {noun} sold at {money(g["p25"])} or less, {money(abs(cap - g["p25"]))} {"under" if g["p25"] < cap else "over"} {caps}, and the upper quarter at {money(g["p75"])} or more, {money(abs(g["p75"] - cap))} {"above" if g["p75"] > cap else "below"} it. '
                  + ('A house at the cap would sit in the lower quarter of the market.' if cap < g['p25'] else ('A house at the cap would sit below the median.' if cap < g['price'] else 'A house at the cap would sit above the median.')))]
    bl += [{'t': 'grid', 'gen': G}, H(f'How {nm} {hs} sales split by price')]
    if kk == 'h12':
        bl += [tbl(f'{nm} {noun} sold at or below each price', ['Sold at or below', 'Sales', 'Share of all sales'], [[money(UP[j]), num(sum(bd[:j + 1])), f'{100 * sum(bd[:j + 1]) / n:.0f}%'] for j in range(k)], src(f'{n:,} {nm} {noun}'))]
    else:
        bl += [tbl(f'{nm} {noun} sold, by price range', ['Price range', 'Sales', 'Share of sales'], [[BANDL[j] + (' (under the cap)' if j < k else ''), num(x), f'{100 * x / n:.0f}%'] for j, x in enumerate(bd) if x], src(f'{n:,} {nm} {noun}'))]
    if cheap:
        bl += [H(f'Which {nm} areas sell for less?' if kk != 'h12' else f'Which {nm} areas sit near {caps}?'),
               P((f'{len(below)} of the {len(rows)} {nm} neighbourhoods with a median had a {hs} median under {caps}' + ((', including ' if len(below) > 6 else ': ') + ', '.join(f'{r["name"]} ({money(r["price"])})' for r in below[:6]) + '.' if below else '.')
                  if kk != 'h12' else
                  f'The table lists the {len(cheap)} {nm} neighbourhoods whose {hs} median is closest to {caps}. {(str(len([r for r in cheap if r["price"] < cap])) + (" of them is" if len([r for r in cheap if r["price"] < cap]) == 1 else " of them are") + " under it, led by") if any(r["price"] < cap for r in cheap) else "None is under it. The closest is"} {cheapest["name"]} at {money(cheapest["price"])}, and the top of the list is {dearest["name"]} at {money(dearest["price"])}.')),
               tbl(f'{nm} neighbourhoods with the {"lowest " + hs + " medians" if kk != "h12" else hs + " medians closest to " + caps}', ['Neighbourhood', 'Sales', 'Median price', f'Against {caps}', 'Price per sq ft', 'Median year built', 'Days to sell'],
                   [[r['name'], str(r['n']), money(r['price']), (f'{money(cap - r["price"])} under' if r['price'] < cap else ('At the cap' if r['price'] == cap else f'{money(r["price"] - cap)} over')), money(r['ppsf']), str(r['yb']) if r['yb'] else '—', str(r['dom']) if r['dom'] is not None else '—'] for r in cheap],
                   srcn(f'{sum(r["n"] for r in cheap):,} {nm} {noun} in', f'{len(cheap)} neighbourhoods, all sold at any price'))]
    q = g.get('q') or []
    if kk != 'h12' and len(q) == 4 and all(x.get('n') for x in q):
        bl += [H(f'{nm} {hs} sales by quarter'),
               tbl(f'{nm} {noun} sold, by quarter', ['Period', 'Sales', 'Median price'], [[QLAB[i], num(x['n']), money(x['price']) if x.get('price') else '—'] for i, x in enumerate(q)], src(f'{n:,} {nm} {noun}'))]
    if kk != 'h12' and len(busy) >= 4:
        bl += [H(f'Where most {nm} {hs} sales happen'),
               P(f'{busy[0]["name"]} had the most {hs} sales in {nm} ({busy[0]["n"]}, median {money(busy[0]["price"])}), followed by {busy[1]["name"]} ({busy[1]["n"]}, median {money(busy[1]["price"])}) and {busy[2]["name"]} ({busy[2]["n"]}, median {money(busy[2]["price"])}).'),
               tbl(f'Busiest {nm} neighbourhoods for {noun}', ['Neighbourhood', 'Sales', 'Median price', 'Days to sell'], [[r['name'], str(r['n']), money(r['price']), str(r['dom']) if r['dom'] is not None else '—'] for r in busy],
                   srcn(f'{sum(r["n"] for r in busy):,} {nm} {noun} in', f'the {len(busy)} busiest neighbourhoods'))]
    # the same cap across every property type in the city, so the page shows how far the budget goes in each
    gx = N.EX['city'][ck]['groups']
    kinds = [(lab, gx[key]) for lab, key in (('Houses', 'house'), ('Condos', 'condo'), ('Houses with a legal suite', 'legal'), ('Coach and laneway houses', 'coach')) if key in gx and gx[key].get('n', 0) >= 5 and gx[key].get('bands')]
    if len(kinds) >= 2 and kk != 'h12':
        def share(x): return f'{100 * sum(x["bands"][:k]) / x["n"]:.0f}%'
        bl += [H(f'What {caps} buys in {nm} by property type'),
               P(f'Against {nm} houses, where {sh}% of sales were under {caps}, ' + '; '.join(f'{lab.lower()} had {share(x)} under it ({num(sum(x["bands"][:k]))} of {num(x["n"])} sales)' for lab, x in kinds if lab != ('Houses' if typ == 'house' else 'Condos')) + '.'),
               tbl(f'{nm} sales by property type and the share under {caps}', [f'Sold under {caps}', 'Property type', 'Sales', 'Median price', 'Days to sell'],
                   [[f'{num(sum(x["bands"][:k]))} ({share(x)})', lab, num(x['n']), money(x['price']), str(x['dom']) if x.get('dom') is not None else '—'] for lab, x in kinds], src(f'{sum(x["n"] for _, x in kinds):,} {nm} sales across {len(kinds)} property types'))]
    bl += [H(f'Buying a {hs} under {caps} in {nm}')]
    if cheap and kk == 'h12':
        pc = round(100 * (g['price'] - cap) / g['price'])
        bl += [P(f'The {nm} median {hs} was {money(g["price"])}, so {caps} sits {abs(pc)}% {"below" if pc > 0 else "above"} it. '
                 + ' '.join(f'{r["name"]}: {money(r["ppsf"])} a square foot, built {r["yb"] or "year not recorded"}, {r["n"]} sales.' for r in cheap[:5])
                 + ' Check the roof age and foundation.')]
    elif cheap:
        bl += [P(f'In {cheapest["name"]} the median {hs} sold for {money(cheapest["price"])} across {cheapest["n"]} sales, {money(abs(cap - cheapest["price"]))} {"under" if cheapest["price"] < cap else "over"} {caps}. '
                 + (f'Across {nm} the median {hs} took {dom} days to sell' + (f' and closed at {ratio} of the last list price' if ratio else '') + (f', with {over}% of the {n:,} sales above list.' if over is not None else '.') if dom else '')
                 + (' Check the roof age and foundation.' if typ == 'house' else ' Check the strata fee and depreciation report.'))]
    if kk == 'h12':
        faq = [(f'How many {nm} {noun} sell for under {caps}?', f'{under:,} of {n:,}, or {sh}%. {step:,} of them sold between $1,000,000 and {money(cap - 1)}.'),
               (f'How much more does {caps} buy than $1,000,000 in {nm}?', f'{step:,} more sales, {step * 100 / n:.0f}% of the market. The share under the cap rises from {round(100 * h1m_n / n)}% to {sh}%.')]
        if cheap: faq.append((f'Which {nm} areas have {hs} medians near {caps}?', f'{cheapest["name"]} ({money(cheapest["price"])}, {cheapest["n"]} sales) to {dearest["name"]} ({money(dearest["price"])}, {dearest["n"]} sales) are the {len(cheap)} closest, for sales {N.WINDOW}.'))
        faq.append((f'Is {caps} enough for a house in {nm}?', f'The median was {money(g["price"])}, so {caps} is {abs(round(100 * (g["price"] - cap) / g["price"]))}% {"below" if cap < g["price"] else "above"} it, and {sh}% of {n:,} sales closed under it.'))
    else:
        faq = [(f'How many {nm} {noun} sell for under {caps}?', f'{under:,} of {n:,}, or {sh}%. A further {num(bd[k])} sold in the next range up, {BANDL[k].lower()}.'),
               (f'What is the median price of a {hs} in {nm}?', f'{money(g["price"])} from {EXW}, so {caps} is {"below" if cap < g["price"] else "above"} the middle of the market.' + (f' The middle half sold between {money(g["p25"])} and {money(g["p75"])}.' if g.get('p25') else ''))]
        if cheap: faq.append((f'Which {nm} area has the lowest {hs} prices?', f'{cheapest["name"]}, at {money(cheapest["price"])} across {cheapest["n"]} sales at {money(cheapest["ppsf"])} a square foot, median year built {cheapest["yb"] or "not recorded"}. The highest of the {len(cheap)} lowest was {dearest["name"]} at {money(dearest["price"])}.'))
        if dom: faq.append((f'How fast do {nm} {noun} sell?', f'{dom} days at the median' + (f', closing at {ratio} of the last list price' if ratio else '') + (f', with {over}% above list' if over is not None else '') + '.'))
    links = [(f'{nm} homes for sale', hub), (f'{nm} condos for sale', f'{ck}-condos-for-sale'), (f'{nm} neighbourhood guides', f'{ck}-neighbourhood-guides'), (f'{nm} market stats', f'{ck}-real-estate-market-stats'),
             (f'{nm} townhomes under $1.2M', f'{ck}-townhomes-under-1-2m'), (f'{nm} homes under $1.8M', f'{ck}-homes-under-1-8m'), (f'{nm} condos under $800K', f'{ck}-condos-under-800k'),
             ('Homes under $1.5 million', 'homes-under-1500000'), ('Home evaluation', 'home-evaluation'), ('Mortgage calculator for BC', 'mortgage-calculator'), ('First-time home buyer programs in BC', 'first-time-home-buyer-program')]
    crumb = [(f'{nm} homes', hub)]
    j = N.finish(slug, seo, crumb, faq, bl, f'{nm} {noun} under {capw}: your questions answered', links, dict(search_page=dict(kind='price', city=ck)))
    return j, (mls, typ, cap, caps, noun)


def write_xlsx(made):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Price band searches'
    ws.append(['Page slug', 'Page heading', 'Page URL', 'Search name to save in MyRealPage', 'MLS area', 'Property type (Type of Dwelling)', 'Max price', 'Status', 'Count (Jerry fills, date)', 'Search ID', 'Embed code'])
    for j, (mls, typ, cap, caps, noun) in made:
        sl = j['slug']; ck = j['search_page']['city']
        ws.append([sl, j['new_page']['h1'], f'https://jaredgibbons.ca/{sl}.html', f'PRICE {CITY[ck][0]} {noun.title()} Under {caps}', mls, 'House/Single Family' if typ == 'house' else 'Apartment/Condo', cap, 'Active', '', '', ''])
        for c in ws[ws.max_row]: c.alignment = Alignment(wrap_text=True, vertical='top')
    for c in ws[1]: c.font = Font(bold=True); c.alignment = Alignment(wrap_text=True, vertical='top')
    for col, w in zip('ABCDEFGHIJK', (38, 42, 44, 40, 34, 24, 14, 10, 18, 18, 40)): ws.column_dimensions[col].width = w
    nt = wb.create_sheet('Notes'); nt.column_dimensions['A'].width = 150
    for t in ['One saved MyRealPage search per row, noframe template, Max price only (no minimum), active listings only (the default), no bedroom or age filter. Send back the count, the search ID and the embed code, same as before.',
              'The MLS area on each row is the same area definition used on that city’s other search pages (for example Surrey = Surrey + North Surrey, Chilliwack = Chilliwack + Sardis).',
              'COUNT ONLY (no pages yet, so I can decide which are worth building). Please run each as a saved search named “KEY …”, active listings, and tell me the result count. Use the Internet Remarks keyword field. '
              'HORSE: keyword “horse” OR “equestrian”, all property types, in Langley, Abbotsford and Maple Ridge (three counts). '
              'POOL: keyword “pool”, House/Single Family, in Surrey, Langley and South Surrey White Rock (three counts). '
              'BLUEBERRY: keyword “blueberry” OR “blueberries”, all property types, in Pitt Meadows, Langley and Abbotsford (three counts).']:
        nt.append([t])
        nt[nt.max_row][0].alignment = Alignment(wrap_text=True, vertical='top')
    f = 'docs/review/idx/price-band-searches-2026-11-07.xlsx'; wb.save(f); print('worksheet written:', f)


def main():
    made = [build(ck, kk) for ck, kk in PAGES]
    N.write_seo([j for j, _ in made])
    write_xlsx(made)
    # inbound links from each city's hub page
    by = {}
    for j, _ in made: by.setdefault(j['search_page']['city'], []).append(j)
    for ck, js in by.items():
        hub = CITY[ck][3]; nm = CITY[ck][0]
        A.end_link(hub, 'bandlinks', f'{nm} homes by price', [(j['new_page']['h1'], j['slug']) for j in js])
    # and from the regional $1.5 million page
    A.end_link('homes-under-1500000', 'bandlinks', 'Homes under $1 million, $1.2 million and condos under $600,000, by city', [(j['new_page']['h1'], j['slug']) for j, _ in made])
    print(len(made), 'pages written')


if __name__ == '__main__':
    main()
