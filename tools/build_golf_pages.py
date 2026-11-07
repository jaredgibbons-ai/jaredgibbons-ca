#!/usr/bin/env python3
"""Six golf course home search pages from Pete's Paragon export (golf group in src/data/sold/sold-extras.json: Site Influences has Golf Course Nearby or Golf Course Dev.).

    south-surrey-white-rock, surrey, langley, abbotsford, tsawwassen, ladner     -> <city>-golf-course-homes-for-sale (draft, local layer with new_page header)

Figures are Paragon closed and pending sales, same rules as the suite pages.  No course names or distances are stated: the flag is the listing agent's, so the pages say what the flag covers and what to check.
The saved searches are Jerry's (keyword-golf-searches-2026-11-06.xlsx, wired by tools/build_idx_embeds.py).   python3 -I tools/build_golf_pages.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_extras_pages as X
from build_new_searches import P, H, L, tbl, money, num, sqft, EX
from build_extras_pages import cv, pc, band_tbl, quarter_tbl, sub_rows, link_for, cellname, fit, SRC, BANDS_H

G = 'golf'
CITY = {
 'south-surrey-white-rock': dict(name='South Surrey and White Rock', short='South Surrey and White Rock', hub='south-surrey-neighbourhood-guides', snap='south-surrey-white-rock', area='South Surrey and White Rock',
    links=[('South Surrey houses for sale', 'south-surrey-houses-for-sale'), ('South Surrey homes for sale', 'south-surrey-homes-for-sale'), ('White Rock homes for sale', 'white-rock-homes-for-sale'), ('Morgan Creek real estate', 'morgan-creek'), ('South Surrey houses with coach houses', 'south-surrey-houses-with-coach-houses-for-sale'), ('South Surrey houses with suites', 'south-surrey-houses-with-suites-for-sale')]),
 'surrey': dict(name='Surrey', short='Surrey', hub='surrey-neighbourhood-guides', snap='surrey', area='Surrey and North Surrey',
    links=[('Surrey houses for sale', 'surrey-houses-for-sale'), ('Surrey homes for sale', 'surrey-homes-for-sale'), ('Surrey houses with suites', 'surrey-houses-with-suites-for-sale'), ('Surrey houses with coach houses', 'surrey-houses-with-coach-houses-for-sale'), ('Surrey neighbourhood guides', 'surrey-neighbourhood-guides')]),
 'langley': dict(name='Langley', short='Langley', hub='langley-neighbourhood-guides', snap='langley', area='the City and Township of Langley',
    links=[('Langley houses for sale', 'langley-houses-for-sale'), ('Langley homes for sale', 'langley-homes-for-sale'), ('Langley houses with suites', 'langley-houses-with-suites-for-sale'), ('Langley houses with coach houses', 'langley-houses-with-coach-houses-for-sale'), ('Langley neighbourhood guides', 'langley-neighbourhood-guides')]),
 'abbotsford': dict(name='Abbotsford', short='Abbotsford', hub='abbotsford-neighbourhood-guides', snap='abbotsford', area='Abbotsford',
    links=[('Abbotsford houses for sale', 'abbotsford-houses-for-sale'), ('Abbotsford homes for sale', 'abbotsford-homes-for-sale'), ('Abbotsford houses with suites', 'abbotsford-houses-with-suites-for-sale'), ('Abbotsford neighbourhood guides', 'abbotsford-neighbourhood-guides')]),
 'tsawwassen': dict(name='Tsawwassen', short='Tsawwassen', hub='tsawwassen-neighbourhood-guides', snap=None, area='Tsawwassen',
    links=[('Tsawwassen houses for sale', 'tsawwassen-houses-for-sale'), ('Tsawwassen homes for sale', 'tsawwassen-homes-for-sale'), ('Ladner golf course homes', 'ladner-golf-course-homes-for-sale'), ('Delta homes for sale', 'delta-homes-for-sale')]),
 'ladner': dict(name='Ladner', short='Ladner', hub='ladner-neighbourhood-guides', snap=None, area='Ladner',
    links=[('Ladner houses for sale', 'ladner-houses-for-sale'), ('Ladner homes for sale', 'ladner-homes-for-sale'), ('Tsawwassen golf course homes', 'tsawwassen-golf-course-homes-for-sale'), ('Delta homes for sale', 'delta-homes-for-sale')]),
}
HOMES = {'south-surrey-white-rock': 'south-surrey-houses-for-sale', 'surrey': 'surrey-houses-for-sale', 'langley': 'langley-houses-for-sale', 'abbotsford': 'abbotsford-houses-for-sale', 'tsawwassen': 'tsawwassen-houses-for-sale', 'ladner': 'ladner-houses-for-sale'}
FLAG = ('A golf course home here is a detached house whose Paragon Site Influences field lists Golf Course Nearby or Golf Course Dev. The listing agent chooses the flag, and it covers homes near a course as well as on one, '
        'so treat the count as a floor and not a full list.')


def page(ck, order):
    c = CITY[ck]; nm = c['name']; g = EX['city'][ck]['groups']; go, ho = g['golf'], g['house']
    assert go['n'] >= 30 and ho['n'] >= 100, ck
    slug = f'{ck}-golf-course-homes-for-sale'
    share = round(100 * go['n'] / ho['n']); prem = round(100 * (go['price'] - ho['price']) / ho['price'])
    side = 'above' if prem >= 0 else 'below'
    sr = sub_rows(ck, 'golf', 3)
    top = [X.disp(n, a) for a, n, v in sr[:3]]
    title = next(t for t in (f'{nm} Golf Course Homes for Sale | Prices', f'{nm} Golf Course Homes for Sale') if 38 <= len(t) <= 60)
    seo = dict(title=title, h1=f'Golf Course Homes for Sale in {nm}', crumb='Golf course homes',
               description=fit(*[f'{x} {y}' for x in (f'Search {nm} golf course homes.', f'{nm} golf course homes for sale.', f'Search {nm} homes on or near a golf course.')
                                  for y in (f'{go["n"]} sold over twelve months at a median of {money(go["price"])}, with prices by neighbourhood and what to check.',
                                            f'{go["n"]} sold over twelve months at a median of {money(go["price"])}, with prices by area and what to check before you offer.',
                                            f'{go["n"]} sold in twelve months at a median of {money(go["price"])}. See prices by neighbourhood and what to check before you offer.',
                                            f'{go["n"]} sold in twelve months at a median of {money(go["price"])}. See prices by neighbourhood and what to check.',
                                            f'{go["n"]} sales in twelve months, median {money(go["price"])}, with prices by neighbourhood and what to check before you offer.',
                                            f'{go["n"]} sold in twelve months at a median of {money(go["price"])}, with prices by neighbourhood.')]),
               links_h=f'More {nm} house searches')
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures come from Paragon closed and pending sales to October 31, 2026. A pending sale is firm but has not completed, so its price can still change. The live search is not connected yet.', 'gen': G},
          P((f'This search lists detached houses for sale in {c["area"]} that the listing marks as on or near a golf course.', f'Use this search to see {nm} detached houses currently for sale where the listing flags a golf course on the street or nearby.', f'Every house in this {nm} search is a detached home that the listing agent has tagged as beside or close to a golf course.')[order % 3] + (f' The most golf course sales were in {top[0]} ({sr[0][2]["golf"]["n"]})' + (f', {top[1]} ({sr[1][2]["golf"]["n"]})' if len(top) > 1 else '') + (f' and {top[2]} ({sr[2][2]["golf"]["n"]})' if len(top) > 2 else '') + '.' if top else '')),
          P(f'' + (f'Of {ho["n"]:,} detached houses that sold in {nm} between November 1, 2025 and October 31, 2026, {go["n"]} ({share}%) carried a golf course flag. They sold for a median of {money(go["price"])}, {abs(prem)}% {side} the {money(ho["price"])} median for every {nm} house.', f'Between November 1, 2025 and October 31, 2026, {nm} recorded {ho["n"]:,} detached house sales, and {go["n"]} of them ({share}%) had the flag. The median was {money(go["price"])}, which is {abs(prem)}% {side} the {money(ho["price"])} median across all {nm} houses.')[order % 2]),
          {'t': 'grid', 'gen': G}, H(f'What {nm} golf course homes sold for')]
    rows = [['Sales', num(go['n']), num(ho['n'])], ['Median price', cv(go, 'price', money), cv(ho, 'price', money)]]
    if go.get('p25'): rows.append(['Middle half of prices', f'{money(go["p25"])} to {money(go["p75"])}', f'{money(ho["p25"])} to {money(ho["p75"])}' if ho.get('p25') else '—'])
    rows += [['Price per square foot', cv(go, 'ppsf', money), cv(ho, 'ppsf', money)], ['Median floor area', cv(go, 'sqft', sqft), cv(ho, 'sqft', sqft)],
             ['Median lot size', cv(go, 'lot_sqft', sqft), cv(ho, 'lot_sqft', sqft)], ['Median year built', cv(go, 'yb'), cv(ho, 'yb')], ['Median bedrooms', cv(go, 'beds'), cv(ho, 'beds')],
             ['Days to sell', cv(go, 'dom'), cv(ho, 'dom')], ['Sold price as a share of list price', cv(go, 'ratio', pc), cv(ho, 'ratio', pc)], ['Sales over the list price', cv(go, 'over', pc), cv(ho, 'over', pc)]]
    rows = [r for r in rows if any(x != '—' for x in r[1:])]
    bl.append(tbl(f'{nm} detached houses sold, golf course flag and all houses', ['Measure', 'Golf course flag', 'All detached houses'], rows, SRC + ' ' + FLAG))
    sen = []
    if go.get('sqft') and ho.get('sqft'): sen.append(f'The typical golf course house had {go["sqft"]:,} square feet of floor area, against {ho["sqft"]:,} for all {nm} houses.')
    if go.get('lot_sqft') and ho.get('lot_sqft'): sen.append(f'Its lot was {go["lot_sqft"]:,} square feet, against {ho["lot_sqft"]:,}.')
    if go.get('ppsf') and ho.get('ppsf'):
        pp = round(100 * (go['ppsf'] - ho['ppsf']) / ho['ppsf']); sen.append(f'Per square foot it cost {money(go["ppsf"])}, ' + ('about the same as' if abs(pp) < 2 else f'{abs(pp)}% {"more" if pp >= 0 else "less"} than') + f' the {money(ho["ppsf"])} for all houses.')
    if sen: bl.append(P(' '.join(sen) + ' Part of any price gap is size and age rather than the course.'))
    if go.get('q'): bl.append(quarter_tbl(f'{nm} golf course houses sold, by period', go, 'Sales'))
    if go.get('bands'): bl.append(band_tbl(f'{nm} houses sold, by price range', BANDS_H, (['Golf course flag', 'All detached houses'], [go, ho])))
    if go.get('bands'):
        a = round(100 * sum(go['bands'][3:]) / go['n']); b = round(100 * sum(ho['bands'][3:]) / ho['n'])
        bl.append(P(f'{a}% of {nm} golf course houses sold for $1,000,000 or more, against {b}% of all {nm} houses.'))
    r5 = [r for r in sr if r[2]['golf']['n'] >= 5][:12] or sr[:8]
    if len(r5) >= 3:
        rr = []
        for a, n, v in r5:
            h = v.get('house', {}); gg = v['golf']
            rr.append([cellname(a, n, link_for(c['hub'], a, n, c['snap'])), num(h.get('n', 0)), num(gg['n']), f'{round(100 * gg["n"] / h["n"])}%' if h.get('n') else '—', cv(gg, 'price', money), cv(h, 'price', money)])
        a0, n0_, v0 = r5[0]; g0, h0 = v0['golf'], v0.get('house', {})
        nb = f'In {X.disp(n0_, a0)}, {g0["n"]} golf course houses sold' + (f' at a median of {money(g0["price"])}' if g0.get('price') else '') + (f', against {money(h0["price"])} for all {h0["n"]} houses there' if h0.get('price') and h0.get('n') else '') + '.'
        bl += [H(f'{nm} neighbourhoods with golf course homes'), P(nb),
               tbl(f'{nm} detached houses with a golf course flag, by neighbourhood', ['Neighbourhood', 'House sales', 'Golf course sales', 'Share with the flag', 'Median price, golf course', 'Median price, all houses'], rr,
                   SRC + ' A neighbourhood is listed with 3 or more golf course sales, and a median price is shown at 5 or more.')]
    # what to check: wording rotates so the six pages do not repeat each other
    v = order % 3
    chk = [
        [f'Ask how close the lot is to the course, and which side of the house faces it. In {nm}, {go["n"]} sales carried the flag, and a house on a fairway is not the same as one a few blocks away.',
         f'Find out how far the house is from the course and whether the back or the side faces it. The flag showed up on {go["n"]} {nm} sales, so it covers a wide range of lots.',
         f'Measure the distance to the course and note which wall faces it. {go["n"]} {nm} houses were flagged, and the listings do not say how near each one sits.'][v],
        ['Look at the fence, windows and deck on the course side, and ask the seller about stray balls, netting or damage and whether insurance was involved.',
         'Check the windows, siding and fence on the course side for ball marks, and ask the seller whether there was damage, a claim or netting.',
         'Walk the course side of the lot for marks on windows and siding, and ask whether the seller ever had damage or an insurance claim.'][v],
        ['Pull the title. A right-of-way, covenant or setback can tie a lot to the course, and it shows on title, not on the listing.',
         'Order the title search to see whether a right-of-way, covenant or building setback is registered against the lot.',
         'Read the title for any covenant, right-of-way or setback that links the lot to the course.'][v],
        [f'Visit at more than one time of day. Mowing starts early and summer evenings are busy. Golf course houses took {go["dom"]} days to sell in {nm}, so there is time to go twice.',
         f'See the house early in the morning and again in the evening, since course maintenance and play change the noise. They took {go["dom"]} days to sell at a median, which leaves room for a second visit.',
         f'Go back at a different hour, because mowers and play change what the yard sounds like. The median time to sell was {go["dom"]} days here, so you rarely need to rush.'][v],
        [f'Compare the price with similar houses without the flag. The golf course median was {money(go["price"])} and the all-house median {money(ho["price"])}, so check whether size and age explain the gap.',
         f'Set the price against nearby houses with no flag. The medians were {money(go["price"])} with it and {money(ho["price"])} without, and floor area and age explain part of that.',
         f'Price it against similar unflagged houses: {money(go["price"])} for golf course homes and {money(ho["price"])} for all {nm} houses, before you decide the course adds anything.'][v]]
    t0 = top[0] if top else nm; n0 = sr[0][2]['golf']['n'] if top else go['n']
    lot = f' The typical lot was {go["lot_sqft"]:,} square feet, so the course side is often a large share of the yard.' if go.get('lot_sqft') else ''
    yb = f' The typical house was built in {go["yb"]}, which tells you how old the roof and windows facing the course may be.' if go.get('yb') else ''
    chk[0] += f' {t0} had the most flagged sales ({n0}).'
    chk[1] += yb
    chk[2] += f' The flag appeared on {share}% of {nm} house sales, so ask your agent which registered documents apply on {t0} streets.' if order % 2 else lot
    if order >= 3:  # pages 4-6 reuse the three base wordings, so reword them to keep each page distinct
        for k, (x, y) in enumerate([('Ask how close', 'Work out how close'), ('Find out how far', 'Establish how far'), ('Measure the distance', 'Pace out the distance'), ('Look at the fence', 'Inspect the fence'), ('Check the windows', 'Examine the windows'), ('Walk the course side', 'Stroll the course side'),
                                    ('Pull the title', 'Request the title'), ('Order the title search', 'Get a title search'), ('Read the title', 'Go through the title'), ('Visit at more', 'Tour at more'), ('See the house early', 'View the house early'), ('Go back at', 'Return at'),
                                    ('Compare the price', 'Weigh the price'), ('Set the price', 'Line the price up'), ('Price it against', 'Judge it against')]):
            chk = [i.replace(x, y) for i in chk]
    bl += [H(f'Before you offer on a {nm} golf course home'), L(chk),
           H(f'Estimate the payment on a {nm} golf course home'), P(f'The calculator starts at the {nm} golf course median of {money(go["price"])}.'), {'t': 'calc', 'which': 'mortgage', 'price': go['price'], 'gen': G}]
    faq = [(f'How much does a {nm} golf course home cost?', (f'The {go["n"]} golf course houses that sold between November 1, 2025 and October 31, 2026 had a median of {money(go["price"])}', f'Across {go["n"]} {nm} sales from November 2025 through October 2026, the golf course median came to {money(go["price"])}')[order % 2] + (f', with the middle half between {money(go["p25"])} and {money(go["p75"])}' if go.get('p25') else '') + f'. All {nm} detached houses had a median of {money(ho["price"])}.'),
           (f'What counts as a golf course home in {nm}?', (f'A detached house whose listing carries the Golf Course Nearby or Golf Course Dev. flag in Paragon. The listing agent enters it, so it covers homes near a course as well as on one.', f'In Paragon the agent who lists the house picks Golf Course Nearby or Golf Course Dev. under Site Influences, so {nm} homes beside a fairway and homes a short walk away can both appear.', f'It is a detached {nm} house with a golf course entry under Site Influences. The seller’s agent decides whether to tick it, which is why the {go["n"]} sales counted here are a minimum.')[order % 3]),
           (f'How fast do {nm} golf course homes sell?', (f'{go["dom"]} days at a median', f'The median was {go["dom"]} days on the market')[order % 2] + (f', closing at {go["ratio"]}% of list' if go.get('ratio') else '') + (f', with {go["over"]}% over the list price' if go.get('over') is not None else '') + f'. All {nm} houses took {ho["dom"]} days.')]
    if top: faq.append((f'Which {nm} neighbourhoods have the most golf course homes?', f'{top[0]} had {sr[0][2]["golf"]["n"]} sales with the flag' + (f', {top[1]} {sr[1][2]["golf"]["n"]}' if len(top) > 1 else '') + (f' and {top[2]} {sr[2][2]["golf"]["n"]}' if len(top) > 2 else '') + f' between November 1, 2025 and October 31, 2026.'))
    crumb = (f'{nm} houses', HOMES[ck])
    return N.finish(slug, seo, [crumb], faq, bl, f'{nm} golf course homes: your questions answered', c['links'], dict(search_page=dict(kind='golf', city=ck)))


def main():
    N.NEW.update([f'{k}-golf-course-homes-for-sale' for k in CITY])
    made = [page(ck, i) for i, ck in enumerate(CITY)]
    for j in made: N.TITLE[j['slug']] = j['new_page']['h1']
    N.write_seo(made)
    # inbound links on the city house hubs
    n = 0
    for j in made:
        ck = j['search_page']['city']
        for host in (HOMES[ck],):
            f = f'src/data/local/{host}.json'
            if not os.path.exists(f): continue
            raw = open(f).read(); d = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
            line2 = raw.split('\n')[1] if '\n' in raw else ''; ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
            d['blocks'] = [b for b in d['blocks'] if not (b.get('gen') == 'golflinks' and b.get('city') == ck)]
            d['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{CITY[ck]["name"]} golf course homes', 'gen': 'golflinks', 'pos': 'end', 'city': ck},
                            {'t': 'list', 'items': [[N.lk(j['new_page']['h1'], j['slug'])]], 'gen': 'golflinks', 'pos': 'end', 'city': ck}]
            open(f, 'w').write(json.dumps(d, indent=ind, ensure_ascii=asc) + nl); n += 1
    print(len(made), 'pages;', n, 'hub links')


if __name__ == '__main__': main()
