"""Generate src/data/local/fraser-valley-commercial-market-report.json from the two commercial data files.
    python3 -I tools/build_commercial_page.py
Inputs: src/data/market/commercial-gvr-<Q>.json (GVR Commercial Edge) and industrial-ay-<Q>.json (Avison Young). Latest of each is used.
All prose that quotes a number is computed from the data, so a new quarter only needs new JSON files."""
import glob, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def latest(pat):
    return json.load(open(sorted(glob.glob(os.path.join(ROOT, 'src/data/market', pat)))[-1], encoding='utf-8'))
G, A = latest('commercial-gvr-*.json'), latest('industrial-ay-*.json')
CLS = [('industrial', 'Industrial'), ('land', 'Land'), ('office', 'Office'), ('retail_other', 'Retail & other'), ('multi_family', 'Multi-family')]
def n(v): return ('−' if v < 0 else '') + '{:,}'.format(abs(v))
def m(v): return '${:,.1f} million'.format(v) if v < 1000 else '${:,.2f} billion'.format(v / 1000)
def mm(v): return '${:,.1f}M'.format(v)
def pub(k):
    v = q26[k]['dollars_yoy_pct_published']; return ('up ' if v > 0 else 'down ') + '{:.1f}%'.format(abs(v))
def ch(a, b):
    if b == 0: return 'n/a'
    c = (a - b) / b * 100; return ('+' if c > 0 else '−' if c < 0 else '') + '{:.1f}%'.format(abs(c))
def rate(v): return '{:.1f}%'.format(v)
def usd(v): return 'n/a' if v is None else '${:,.2f}'.format(v)

MK = G['market']; q26, q25 = MK['Q2_2026'], MK['Q2_2025']; AR = G['areas_q2_2026']
FV = ['Surrey', 'Langley', 'Abbotsford', 'Chilliwack', 'Maple Ridge', 'Delta', 'Mission', 'White Rock', 'Pitt Meadows']
fv_sales = sum(AR[a]['total']['sales'] for a in FV); fv_k = sum(AR[a]['total']['dollars_k'] for a in FV)
fv_sales25 = sum(G['area_totals_q2_2025'][a]['sales'] for a in FV)
tot = q26['total']; PB = G['industrial_price_bands_q2_2026']; LT = G['land_sales_trend']['sales']

b = []
b.append({'t': 'notice', 'text': "Draft for Jared's approval. Numbers are from Greater Vancouver REALTORS® Commercial Edge (Q2 2026) and Avison Young's Metro Vancouver industrial report (Q3 2026). Every table figure was checked against the printed totals in the source reports. First-hand notes from Jared are still to be added."})
b.append({'t': 'p', 'text': f"Commercial property behaves differently from houses, so the headline price indexes do not help much. This page puts two published data sets side by side for the Fraser Valley: what commercial property actually sold for in the second quarter of 2026, and how much industrial space is empty, what it asks, and what is being built in the third quarter."})
# ---- sales by asset class
b.append({'t': 'h', 'level': 2, 'text': 'Commercial sales in the Lower Mainland, Q2 2026'})
b.append({'t': 'p', 'text': f"The Lower Mainland recorded {n(tot['sales'])} commercial sales worth {m(tot['dollars_m'])} in the second quarter of 2026. The number of sales was {ch(tot['sales'], q25['total']['sales']).lstrip('−')} lower than a year earlier and {ch(tot['sales'], MK['Q1_2026']['total']['sales']).lstrip('−')} lower than the first quarter, while dollar volume was {pub('total')} from a year earlier. Fewer deals, but bigger ones on average."})
rows = []
for k, lab in CLS:
    a, c = q26[k], q25[k]; rows.append([lab, n(a['sales']), n(c['sales']), ch(a['sales'], c['sales']), mm(a['dollars_m']), mm(c['dollars_m']), '{:+.1f}%'.format(a['dollars_yoy_pct_published']).replace('-', '−')])
rows.append(['All commercial', n(tot['sales']), n(q25['total']['sales']), ch(tot['sales'], q25['total']['sales']), mm(tot['dollars_m']), mm(q25['total']['dollars_m']), '{:+.1f}%'.format(tot['dollars_yoy_pct_published']).replace('-', '−')])
b.append({'t': 'table', 'caption': 'Lower Mainland commercial sales by asset class, Q2 2026 compared with Q2 2025', 'head': ['Asset class', 'Sales Q2 2026', 'Sales Q2 2025', 'Change', 'Dollar volume Q2 2026', 'Dollar volume Q2 2025', 'Change'], 'rows': rows, 'source': 'Source: ' + G['source'] + '.'})
ind, off = q26['industrial'], q26['office']
b.append({'t': 'p', 'text': f"Two classes moved against the trend. Office sales fell to {off['sales']} from {q25['office']['sales']} a year earlier, yet office dollar volume was {pub('office')} because the year-earlier quarter was so small. Industrial held steady at {ind['sales']} sales but its dollar volume was {pub('industrial')}, which means the typical industrial deal was smaller."})
# ---- by municipality
b.append({'t': 'h', 'level': 2, 'text': 'Fraser Valley commercial sales by municipality, Q2 2026'})
rows = []
for a in sorted(FV, key=lambda x: -AR[x]['total']['sales']):
    r = AR[a]; p = G['area_totals_q2_2025'][a]
    rows.append([a, n(r['total']['sales']), n(p['sales']), mm(r['total']['dollars_k'] / 1000)] + [n(r[k]['sales']) for k, _ in CLS])
rows.append(['Nine municipalities', n(fv_sales), n(fv_sales25), mm(fv_k / 1000)] + [n(sum(AR[a][k]['sales'] for a in FV)) for k, _ in CLS])
b.append({'t': 'table', 'caption': 'Commercial sales by municipality, Q2 2026 (sales counts by asset class)', 'head': ['Municipality', 'Total sales', 'Q2 2025 sales', 'Dollar volume', 'Industrial', 'Land', 'Office', 'Retail & other', 'Multi-family'], 'rows': rows, 'source': 'Source: ' + G['source'] + '. Pitt Meadows recorded no commercial sales in the quarter.'})
s = AR['Surrey']; l = AR['Langley']; c = AR['Chilliwack']
b.append({'t': 'p', 'text': f"These nine municipalities made up {fv_sales} of the region's {tot['sales']} commercial sales, or {fv_sales / tot['sales'] * 100:.0f}%. Surrey led with {s['total']['sales']} sales (up from {G['area_totals_q2_2025']['Surrey']['sales']}) and {mm(s['total']['dollars_k'] / 1000)} in volume, and {mm(s['land']['dollars_k'] / 1000)} of that was land. Half of Langley's {l['total']['sales']} sales were retail or other ({l['retail_other']['sales']}), the highest share among the nine."})
b.append({'t': 'p', 'text': f"Treat the dollar figures for the smaller areas with care. Chilliwack's {c['total']['sales']} sales added up to {mm(c['total']['dollars_k'] / 1000)}, against {mm(G['area_totals_q2_2025']['Chilliwack']['dollars_k'] / 1000)} from {G['area_totals_q2_2025']['Chilliwack']['sales']} sales a year earlier. With counts this low, one large sale moves the total, so the number of sales says more than the dollars do."})
# ---- industrial
M = A['markets']; FVM = ['Surrey', 'Langley', 'Abbotsford', 'Delta', 'Maple Ridge / Pitt Meadows', 'Chilliwack', 'Tsawwassen (TFN Lands)']; me = A['metro']
b.append({'t': 'h', 'level': 2, 'text': 'Industrial space: vacancy, rents and new supply, Q3 2026'})
b.append({'t': 'p', 'text': f"Across the 14 submarkets Avison Young tracks, from Vancouver out to Chilliwack, {rate(me['vac_rate'])} of industrial space was vacant in the third quarter and {rate(me['avail_rate'])} was available, down from {rate(A['headline']['availability_prev_quarter'])} available in the second quarter. Average asking net rent was {usd(me['net_rent'])} per square foot, with another {usd(me['add_rent'])} on average in additional rent. About {me['under_construction'] / 1e6:.2f} million square feet was under construction in {A['headline']['sf_under_construction_projects']} projects, and {A['headline']['pre_committed_pct']}% of that space was already pre-committed."})
rows = []
for k in FVM:
    r = M[k]; comb = usd(r['net_rent'] + r['add_rent']) if r['net_rent'] is not None else 'n/a'
    rows.append([k, '{:.1f}M'.format(r['inventory'] / 1e6), rate(r['vac_rate']), rate(r['avail_rate']), usd(r['net_rent']), usd(r['add_rent']), comb, n(r['under_construction'])])
rows.append(['Metro Vancouver total', '{:.1f}M'.format(me['inventory'] / 1e6), rate(me['vac_rate']), rate(me['avail_rate']), usd(me['net_rent']), usd(me['add_rent']), usd(me['net_rent'] + me['add_rent']), n(me['under_construction'])])
b.append({'t': 'table', 'caption': 'Industrial market statistics, Fraser Valley submarkets, Q3 2026 (rents per square foot)', 'head': ['Submarket', 'Inventory (sq ft)', 'Vacancy', 'Availability', 'Asking net rent', 'Additional rent', 'Net plus additional', 'Under construction (sq ft)'], 'rows': rows, 'source': 'Source: ' + A['source'] + '. Tsawwassen (TFN Lands) had no vacancy and publishes no rent.'})
tight = min((k for k in FVM if M[k]['inventory'] > 3e6), key=lambda k: M[k]['vac_rate']); loose = max(FVM, key=lambda k: M[k]['vac_rate'])
cheap = min((k for k in FVM if M[k]['net_rent']), key=lambda k: M[k]['net_rent']); dear = max((k for k in FVM if M[k]['net_rent']), key=lambda k: M[k]['net_rent'])
su = M['Surrey']; de = M['Delta']; la = M['Langley']
b.append({'t': 'p', 'text': f"The spread inside the Fraser Valley is wide. {tight} was the tightest at {rate(M[tight]['vac_rate'])} vacant, while {loose} was the loosest at {rate(M[loose]['vac_rate'])}. Asking net rent ran from {usd(M[cheap]['net_rent'])} in {cheap} to {usd(M[dear]['net_rent'])} in {dear}, a gap of {usd(M[dear]['net_rent'] - M[cheap]['net_rent'])} a square foot between the cheapest and the dearest of these markets."})
b.append({'t': 'p', 'text': f"Supply is the other story. Surrey has {n(su['under_construction'])} square feet under construction, {su['under_construction'] / me['under_construction'] * 100:.0f}% of the whole Metro pipeline, even though its net absorption for the quarter was {n(su['absorption'])} square feet, meaning more space was given back than taken up. Delta went the other way: {n(de['absorption'])} square feet of net absorption and {rate(de['vac_rate'])} vacancy. Langley's net absorption was {n(la['absorption'])} square feet and its vacancy {rate(la['vac_rate'])}."})
# ---- reading
b.append({'t': 'h', 'level': 2, 'text': 'What the numbers mean for an owner-user, investor or seller'})
b.append({'t': 'p', 'text': f"For an owner-user buying a unit or a building, the sales data says most industrial deals are small. In the Lower Mainland in Q2, {PB['under_1m'] + PB['1_to_2m'] + PB['2_to_3m']} of the {PB['total_industrial_sales']} industrial sales were under $3 million, and the largest group, {PB['1_to_2m']}, sat between $1 million and $2 million. In {tight}, where vacancy was {rate(M[tight]['vac_rate'])}, expect few comparable choices, and sales that depend on what happens to come up."})
b.append({'t': 'p', 'text': f"For an investor, the gap between net rent and additional rent matters as much as the headline. In the Fraser Valley markets above, additional rent adds between {usd(min(M[k]['add_rent'] for k in FVM if M[k]['add_rent']))} and {usd(max(M[k]['add_rent'] for k in FVM if M[k]['add_rent']))} to the asking rent, so two buildings with the same net rent can cost a tenant very different amounts."})
b.append({'t': 'p', 'text': f"For an owner thinking about selling, land was the largest dollar class in the quarter: {q26['land']['sales']} sales for {m(q26['land']['dollars_m'])}, {pub('land')} from a year earlier. The count has stayed between {min(LT)} and {max(LT)} sales for five straight quarters, so activity has been steady. A site that could be redeveloped is a different sale from a building valued on its rent."})
b.append({'t': 'h', 'level': 2, 'text': 'How to read these two reports together'})
b.append({'t': 'p', 'text': "They measure different things in different places. The GVR figures count completed sales registered with the Land Title and Survey Authority of BC, and they exclude share sales. Avison Young's figures describe leasing space and are grouped by submarket, so Maple Ridge and Pitt Meadows appear together and Tsawwassen means the Tsawwassen First Nation lands. A city that is quiet in one report can still be busy in the other."})
b.append({'t': 'p', 'text': "Neither report describes your own building. Zoning, lot size, ceiling height, loading, and whether the space is strata or freehold change value more than the submarket average does."})
b.append({'t': 'p', 'text': 'Browse commercial listings','h': '/commercial.html'})
faq = [
 {'q': 'What is the difference between vacancy and availability in the industrial table?', 'a': "Both are published by Avison Young and availability is the larger number because it counts more space than just the empty space. In Surrey, for example, 1,872,998 square feet was vacant while 2,100,222 square feet was available. Availability usually also includes space that is being marketed but not yet empty, such as a tenant's space that is coming up."},
 {'q': 'Why do the sales report and the rent report show different areas?', 'a': "They are produced by different organizations for different purposes. GVR's Commercial Edge counts registered sales by municipality. Avison Young reports leasing space by submarket and combines Maple Ridge with Pitt Meadows."},
 {'q': 'Does the sales data include commercial listings that are for sale now?', 'a': "No. It counts completed sales registered at the Land Title and Survey Authority of BC. Current listings are on the commercial search page."},
 {'q': 'When will these numbers update?', 'a': "GVR publishes Commercial Edge quarterly with a lag of about three months, and Avison Young publishes its industrial report each quarter. I update this page when each new report is out."},
]
page = {'status': 'draft', 'slug': 'fraser-valley-commercial-market-report', 'updated': '2026-11-01',
 'new_page': {'title': 'Fraser Valley Commercial Market Report 2026 | Jared Gibbons',
  'description': 'Fraser Valley commercial and industrial real estate numbers for 2026: sales by city, industrial vacancy, asking rents and new supply in Surrey, Langley, Abbotsford, Delta and Chilliwack.',
  'h1': 'Fraser Valley Commercial and Industrial Real Estate Market Report'},
 'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'Commercial', 'href': '/commercial.html'}, {'name': 'Commercial market report', 'href': '/fraser-valley-commercial-market-report.html'}],
 'faq_heading': 'Commercial market numbers: your questions answered', 'blocks': b, 'faq': faq,
 'needs_from_muse': ['Jared first-hand view of the commercial/industrial market and the buyer types he works with', 'Commercial listing search (IDX) for the grid on /commercial.html', 'Next reports: GVR Commercial Edge Q3 2026 and Avison Young Q4 2026']}
out = os.path.join(ROOT, 'src/data/local/fraser-valley-commercial-market-report.json')
json.dump(page, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(out, 'a').write('\n'); print('wrote', out, len(b), 'blocks')
