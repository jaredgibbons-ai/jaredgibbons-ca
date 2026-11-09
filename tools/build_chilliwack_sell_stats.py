"""Chilliwack sell page market section from the CADREB detailed sheet (src/data/market/cadreb-2026-10.json), added 2026-11-09.

CADREB publishes counts and dollar volume by property type, not a benchmark price, so the table shows sales, average sale price (dollar value sold divided by units sold),
days to sell and listings. Every number below is computed from the sheet; the sheet's own totals are checked first. Blocks carry gen 'cadreb' and are rebuilt on every run.
    python3 -I tools/build_chilliwack_sell_stats.py
"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'src/data/local/sell-my-house-in-chilliwack.json')
D = json.load(open(os.path.join(ROOT, 'src/data/market/cadreb-2026-10.json'), encoding='utf-8'))
G = 'cadreb'
m = lambda v: '${:,.0f}'.format(v)
def pc(a, b): return (a - b) / b * 100
def chg(a, b):
    v = pc(a, b)
    return 'little changed' if abs(v) < 0.5 else ('up ' if v > 0 else 'down ') + '{:.1f}%'.format(abs(v))

T = D['types']; TOT = D['total_residential']
# the sheet's totals include a multi-family (plex) row with no sales, 1 new listing and 9 (1 in 2025) listings at month end
for k, plex in (('new', (1, 1)), ('listings', (9, 1))):
    for i in (0, 1): assert sum(t[k][i] for t in T.values()) + plex[i] == TOT[k][i], k
assert sum(t['value'][0] for t in T.values()) == TOT['value'][0] and sum(t['sales'][0] for t in T.values()) == TOT['sales'][0]
bands = D['price_bands_all_residential_sales_oct_2026']; assert sum(n for _, n in bands) == TOT['sales'][0]
EDGE = lambda lab: (0 if lab.startswith('Under') else (2000000 if lab.startswith('over') else int(lab.split(' - ')[0].replace('K', '').replace(',', '')) * (1000 if lab.split(' - ')[0].endswith('K') else 1)))
def g(lo, hi): return sum(n for lab, n in bands if lo <= EDGE(lab) < hi)
rows_band = [['Under $500,000', g(0, 500000)], ['$500,000 to $749,999', g(500000, 750000)], ['$750,000 to $999,999', g(750000, 1000000)], ['$1,000,000 to $1,499,999', g(1000000, 1500000)], ['$1,500,000 and over', g(1500000, 10**9)]]
assert sum(n for _, n in rows_band) == TOT['sales'][0], rows_band
top = max(bands, key=lambda x: x[1])
topl = '$' + top[0].replace(' - ', ' to $').replace(',', ',')

det, th, ap = T['Single family (detached)'], T['Townhouses (attached)'], T['Apartments']
avg = lambda t, i: t['value'][i] / t['sales'][i]
head = ['Home type', 'Sales, Oct 2026', 'Sales, Oct 2025', 'Average sale price, Oct 2026', 'Average sale price, Oct 2025', 'Days to sell, Oct 2026', 'Listings at month end, Oct 2026']
rows = []
for name, t in T.items():
    rows.append([name, str(t['sales'][0]), str(t['sales'][1]), m(avg(t, 0)), m(avg(t, 1)), str(t['days']), '{:,}'.format(t['listings'][0])])
rows.append(['All residential', str(TOT['sales'][0]), str(TOT['sales'][1]), m(TOT['value'][0] / TOT['sales'][0]), m(TOT['value'][1] / TOT['sales'][1]), '', '{:,}'.format(TOT['listings'][0])])
ratio = TOT['sales'][0] / TOT['listings'][0] * 100

blocks = [
    {'t': 'h', 'level': 2, 'text': 'Chilliwack market, October 2026', 'gen': G},
    {'t': 'p', 'text': f'The Chilliwack and District Real Estate Board recorded {TOT["sales"][0]} residential sales in October 2026, {chg(TOT["sales"][0], TOT["sales"][1])} from {TOT["sales"][1]} a year earlier. Detached sales were {det["sales"][0]} against {det["sales"][1]}, townhouse sales {th["sales"][0]} against {th["sales"][1]} and apartment sales {ap["sales"][0]} against {ap["sales"][1]}.', 'gen': G},
    {'t': 'p', 'text': f'Sellers had {TOT["listings"][0]:,} residential listings on the board at month end, {chg(TOT["listings"][0], TOT["listings"][1])} on October 2025, with {TOT["new"][0]} new listings in the month ({TOT["new"][1]} a year ago). Against {TOT["sales"][0]} sales that is about {ratio:.1f} sales for every 100 listings. A detached house took {det["days"]:.0f} days to sell on average, a townhouse {th["days"]:.0f} and an apartment {ap["days"]:.0f}.', 'gen': G},
    {'t': 'table', 'caption': 'Chilliwack and District board, residential sales by home type, October 2026 against October 2025', 'head': head, 'rows': rows,
     'source': 'Source: Chilliwack & District Real Estate Board, MLS® detailed sheet, October 2026. Average sale price is the dollar value of units sold divided by units sold, so it moves with the mix of homes that sold; the board does not publish a benchmark price. A type with fewer than 10 sales in the month (mobile homes, house and acreage) is not read as a trend. All residential also counts the board’s multi-family (plex) category: no sales, 1 new listing and 9 listings at month end.', 'gen': G},
    {'t': 'p', 'text': f'By price, the busiest band in October was {topl} with {top[1]} sales. {rows_band[0][1]} of the {TOT["sales"][0]} residential sales were under $500,000, {rows_band[1][1]} were from $500,000 to $749,999, {rows_band[2][1]} from $750,000 to $999,999 and {rows_band[3][1] + rows_band[4][1]} at $1,000,000 or more.', 'gen': G},
    {'t': 'table', 'caption': 'Chilliwack and District board, residential sales by price band, October 2026', 'head': ['Sale price', 'Sales'], 'rows': [[a, str(b)] for a, b in rows_band],
     'source': 'Source: Chilliwack & District Real Estate Board, MLS® detailed sheet, October 2026. All residential sales, grouped here from the board’s $50,000 and $100,000 bands. The board covers Chilliwack, Agassiz-Harrison, Hope and Cultus Lake, not the City of Chilliwack alone.', 'gen': G},
]
d = json.load(open(P, encoding='utf-8'))
d['blocks'] = [b for b in d['blocks'] if b.get('gen') != G]
at = next(i for i, b in enumerate(d['blocks']) if b.get('t') == 'p' and b.get('text', '').startswith('This page covers')) + 1
d['blocks'][at:at] = blocks
d['blocks'][0]['text'] = d['blocks'][0]['text'].replace('There is no benchmark price table because Chilliwack is reported by a different real estate board whose statistics I do not yet have.', 'The market table is from the Chilliwack and District board’s October 2026 detailed sheet; the board publishes no benchmark prices and no sub-area figures.')
d['faq'] = [q for q in d['faq'] if not q['q'].startswith(('Why is there no price table', 'How is the Chilliwack market', 'Does Chilliwack have a benchmark'))]
d['faq'] += [
    {'q': 'How is the Chilliwack housing market doing right now?', 'a': f'In October 2026 the Chilliwack and District board recorded {TOT["sales"][0]} residential sales against {TOT["sales"][1]} a year earlier and {TOT["listings"][0]:,} listings at month end. Detached homes took {det["days"]:.0f} days to sell on average, townhouses {th["days"]:.0f} and apartments {ap["days"]:.0f}.'},
    {'q': 'Does Chilliwack have a benchmark price like Surrey or Vancouver?', 'a': 'Not from its board. The Chilliwack and District board publishes sales, listings, days to sell and the dollar value sold by home type, so this page shows average sale prices, which move with the mix of homes that sold. Jared can pull recent sales near your address for a closer number.'}]
d['needs_from_muse'] = [x for x in d.get('needs_from_muse', []) if not x.startswith('Chilliwack and District real estate board monthly statistics')]
d['updated'] = '2026-11-09'
raw = open(P, encoding='utf-8').read()
json.dump(d, open(P, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(P, 'a').write('\n')
print('Chilliwack sell page: market section added;', rows_band, topl, top)
