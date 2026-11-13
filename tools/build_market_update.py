#!/usr/bin/env python3
"""Monthly market update page from the Fraser Valley Real Estate Board statistics package (D-257).

    python3 -I tools/build_market_update.py            # writes src/data/local/october-2026-market-update-....json

Numbers:
  * area and home-type rows (sales, active listings, benchmarks, changes) are read from src/data/market/<month>.json,
    which tools/parse_market.py reads out of the board's PDF (checked line by line, D-169);
  * the board-wide totals, the ratio, days to sell and year-to-date lines are on the news release and the first MLS® Summary
    page only. They are keyed in below (RELEASE) and every one of them is checked against the PDF text before anything is written;
  * "derived" ratios are sales divided by active listings, worked out here.
Every comparative sentence ("the tightest", "the smallest drop", "every area is lower") is asserted against the data,
so a month where it stops being true fails loudly instead of printing a wrong claim. The wording is written per month.
"""
import json, os, re, subprocess, sys
sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTH = '2026-10'
SLUG = 'october-2026-market-update-south-surrey-white-rock-langley'
PREV = ('September 2026 market update', '/september-2026-market-update-south-surrey-white-rock-langley.html')
PDF = f'{ROOT}/docs/research/market-data/FVREB-Package-{MONTH}.pdf'
PACKAGE_URL = 'https://www.fvreb.bc.ca/statistics/Package202610.pdf'
BOC_URL = 'https://www.bankofcanada.ca/2026/10/fad-press-release-2026-10-28/'
GEN = 'mktupdate'

# From the news release and "MLS® Summary - Fraser Valley, All Property Types" (package pages 1-3). Checked against the PDF below.
RELEASE = {
    'released': 'November 3, 2026',
    'sales': (1051, 14.0, -6.4), 'new': (2551, -9.5, -14.0), 'active': (9164, -6.1, -9.5), 'avg': (936748, -1.9, -5.1),   # now, vs last month, vs last year
    'ytd_sales': (9765, 10371, -5.8),
    'ratio': 11, 'days': {'detached': 50, 'townhouse': 37, 'apartment': 44},
}
PDF_CHECK = ['For Immediate Release: November 3, 2026', 'recorded 1,051 sales', 'A total of 2,551 new listings', '9,164 active listings',
             'sales-to-active listings ratio of 11 per cent', 'ratio between 12 and 20 per cent', '50 days', 'a condo was 44 days', '37 days to sell',
             '1,051', '1,123', '-6.4%', '922', '14.0%', '2,551', '2,967', '-14.0%', '2,818', '-9.5%', '9,164', '10,121', '9,763', '-6.1%',
             '936,748', '987,199', '-5.1%', '954,833', '-1.9%', '9,765', '10,371', '-5.8%', 'best level in five years',
             'interest rates recently moving higher']


def main():
    txt = subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', '3', PDF, '-'], capture_output=True, text=True, check=True).stdout
    flat = re.sub(r'\s+', ' ', txt)
    missing = [s for s in PDF_CHECK if s not in flat]
    assert not missing, f'not found in the package text: {missing}'

    d = json.load(open(f'{ROOT}/src/data/market/{MONTH}.json'))['fvreb']
    assert 'October 2026' in d['source'] and 'November 3, 2026' in d['source'], d['source']
    S, H = d['summary'], d['hpi']
    money = lambda n: f'${n:,.0f}'
    pct = lambda x: f'{x:+.1f}%'.replace('+0.0%', '0.0%')
    down = lambda x: f'{abs(x):.1f}%'
    ROWS = [('Fraser Valley', 'All Areas Combined'), ('White Rock / South Surrey', 'White Rock / South Surrey'), ('Langley', 'Langley'),
            ('Surrey combined', 'City of Surrey - Combined'), ('Surrey - Central', 'Surrey - Central'), ('Surrey - North', 'Surrey - North'),
            ('Cloverdale', 'Surrey - Cloverdale'), ('Abbotsford', 'Abbotsford'), ('North Delta', 'Delta - North'), ('Mission', 'Mission')]
    TYPES = [('Detached', 'detached'), ('Townhouse', 'townhouse'), ('Apartment', 'apartment')]

    def cell(area, t):
        x = S[area][t]; s = x['sales']['now']; a = x.get('active', {}).get('now')
        return {'s': s, 'a': a, 'r': round(100 * s / a, 1) if a else None, 'b': x['benchmark']['now'], 'by': x['benchmark']['chg_year'], 'bm': x['benchmark']['chg_month'],
                'sy': x['sales']['last_year'], 'syc': x['sales']['chg_year'], 'sm': x['sales']['last_month'], 'ay': x.get('active', {}).get('chg_year')}
    C = {(a, t): cell(a, t) for _, a in ROWS for _, t in TYPES}
    comp = {a: H[a]['composite'] for a in H}

    def table(label, t):
        rows = []
        for name, a in ROWS:
            c = C[(a, t)]
            few = c['s'] < 10
            rows.append([name + ('*' if few else ''), money(c['b']), pct(c['by']), f"{c['s']:,}", f"{c['a']:,}" if c['a'] else 'n/a', f"{c['r']:.1f}%" if c['r'] is not None else 'n/a'])
        return {'t': 'table', 'caption': f'{label}, October 2026', 'head': ['Area', 'Benchmark', '1 year', 'Sales', 'Active', 'Ratio (derived)'], 'rows': rows, 'gen': GEN}

    # ---- claims, each asserted ------------------------------------------------------------------------------------------------
    assert all(v['chg_1y'] < 0 for a, x in H.items() for v in x.values()), 'a benchmark is no longer lower than a year ago'
    ranked = sorted([(c['r'], a, t) for (a, t), c in C.items() if c['r'] is not None and c['s'] >= 10 and a != 'All Areas Combined'], reverse=True)
    assert [(a, t) for _, a, t in ranked[:2]] == [('Langley', 'townhouse'), ('Delta - North', 'detached')], ranked[:3]
    fv_areas = [a for a in comp if a not in ('Lower Mainland', 'Fraser Valley Board')]
    assert max(fv_areas, key=lambda a: comp[a]['chg_1y']) == 'Cloverdale' and min(fv_areas, key=lambda a: comp[a]['chg_1y']) == 'Mission'
    det_drop = sorted((C[(a, 'detached')]['by'], a) for _, a in ROWS if a not in ('All Areas Combined', 'City of Surrey - Combined'))
    assert {det_drop[0][1], det_drop[1][1]} == {'Abbotsford', 'Mission'} and det_drop[0][0] == det_drop[1][0] == -13.1, det_drop[:3]
    det_rise = max((C[(a, 'detached')]['syc'], a) for _, a in ROWS if a not in ('All Areas Combined', 'City of Surrey - Combined'))
    assert det_rise == (33.3, 'Abbotsford'), det_rise
    slowest = min((c['r'], a) for (a, t), c in C.items() if t == 'detached' and c['r'] is not None and a != 'All Areas Combined')
    assert slowest[1] == 'Mission', slowest
    up_from_sep = [(a, t) for (a, t), c in C.items() if c['bm'] > 0]
    assert len(up_from_sep) >= 3
    F = {t: S['All Areas Combined'][t] for _, t in TYPES}
    assert F['detached']['sales']['now'] > F['townhouse']['sales']['now'] > F['apartment']['sales']['now']
    R = RELEASE
    assert abs(R['sales'][0] / R['active'][0] * 100 - R['ratio']) < 0.6            # the board's own 11% is its total sales over total active listings
    assert comp['Fraser Valley Board']['benchmark'] == 860000 and comp['Fraser Valley Board']['chg_1m'] == -0.1 and comp['Fraser Valley Board']['chg_1y'] == -6.4

    ws, la, su, sc, sn, cl, ab, nd, mi = ('White Rock / South Surrey', 'Langley', 'City of Surrey - Combined', 'Surrey - Central', 'Surrey - North', 'Surrey - Cloverdale', 'Abbotsford', 'Delta - North', 'Mission')
    c = lambda a, t: C[(a, t)]
    # Rich.astro puts one space between fragments (none before punctuation), so fragments are stored trimmed
    P = lambda *parts: {'t': 'p', 'parts': [({'t': x.strip()} if isinstance(x, str) else {'t': x[0], 'h': x[1]}) for x in parts], 'gen': GEN}
    Hd = lambda lv, text: {'t': 'h', 'level': lv, 'text': text, 'gen': GEN}
    L = lambda *items: {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': GEN}
    fv = comp['Fraser Valley Board']

    blocks = [
        P(f"The Fraser Valley Real Estate Board (FVREB) published its October numbers in a release dated November 3. Sales rose from September, fewer new listings came on, and prices slipped again."),
        P('Below: the Fraser Valley overall, then the areas I work in, as far as FVREB publishes them. Every figure comes from the board\'s October 2026 statistics package. Anything marked "derived" is my own math.'),
        {'t': 'updated', 'gen': GEN},

        Hd(2, 'The short version'),
        {'t': 'stats', 'small': True, 'gen': GEN, 'items': [
            {'label': 'Sales', 'value': f"{R['sales'][0]:,}", 'delta': pct(R['sales'][1]), 'sub': 'from September'},
            {'label': 'Active listings', 'value': f"{R['active'][0]:,}", 'delta': pct(R['active'][1]), 'sub': 'from September'},
            {'label': 'Composite benchmark', 'value': money(fv['benchmark']), 'delta': pct(fv['chg_1y']), 'sub': 'from October 2025'},
            {'label': 'Sales-to-active ratio', 'value': f"{R['ratio']}%", 'sub': 'Balanced is 12% to 20%'}]},
        L(f"The board recorded {R['sales'][0]:,} sales, up {down(R['sales'][1])} from September and down {down(R['sales'][2])} from last October.",
          f"Active listings fell to {R['active'][0]:,}, down {down(R['active'][1])} in a month and {down(R['active'][2])} in a year. New listings were {R['new'][0]:,}, down {down(R['new'][1])} from September.",
          f"The board-wide sales-to-active ratio was {R['ratio']}%. FVREB says a balanced market is typically 12% to 20%, and it still calls this a buyer's market.",
          f"The composite benchmark price is {money(fv['benchmark'])}, down {down(fv['chg_1m'])} from September and {down(fv['chg_1y'])} in a year. Every area and home type below is lower than a year ago.",
          f"Among rows with 10 or more sales, the tightest segments (derived) are Langley townhouses at {c(la, 'townhouse')['r']:.1f}% and North Delta detached homes at {c(nd, 'detached')['r']:.1f}%.",
          'The Bank of Canada raised its policy rate to 2.5% on October 28, its first increase in more than three years.'),

        Hd(2, 'Fraser Valley overall'),
        {'t': 'table', 'caption': 'All property types, October 2026', 'head': ['Measure', 'October 2026', 'From September', 'From October 2025'], 'gen': GEN, 'rows': [
            ['Sales', f"{R['sales'][0]:,}", pct(R['sales'][1]), pct(R['sales'][2])], ['New listings', f"{R['new'][0]:,}", pct(R['new'][1]), pct(R['new'][2])],
            ['Active listings', f"{R['active'][0]:,}", pct(R['active'][1]), pct(R['active'][2])], ['Average price', money(R['avg'][0]), pct(R['avg'][1]), pct(R['avg'][2])]]},
        {'t': 'table', 'caption': 'Benchmark price by home type, October 2026', 'head': ['Home type', 'Benchmark', '1 month', '1 year'], 'gen': GEN, 'rows':
            [[n, money(F[t]['benchmark']['now']), pct(F[t]['benchmark']['chg_month']), pct(F[t]['benchmark']['chg_year'])] for n, t in TYPES]
            + [['All types', money(fv['benchmark']), pct(fv['chg_1m']), pct(fv['chg_1y'])]],
         'source': 'Source: Fraser Valley Real Estate Board statistics package, October 2026 (released November 3, 2026).'},
        P(f"Detached homes led the month: {F['detached']['sales']['now']} detached sales, against {F['townhouse']['sales']['now']} townhouses and {F['apartment']['sales']['now']} apartments. "
          f"Detached sales were up {down(F['detached']['sales']['chg_year'])} from last October, while townhouse sales were down {down(F['townhouse']['sales']['chg_year'])} and apartment sales down {down(F['apartment']['sales']['chg_year'])}."),
        P(f"Homes took {R['days']['detached']} days to sell on average for detached, {R['days']['townhouse']} for townhouses and {R['days']['apartment']} for condos. "
          f"Year to date, the board has {R['ytd_sales'][0]:,} sales against {R['ytd_sales'][1]:,} at this point last year ({pct(R['ytd_sales'][2])})."),
        P('Average price is what homes actually sold for, so it shifts with the mix of homes that sold. The benchmark tracks a typical home, which is why I use it for trends.'),
        P("The Bank of Canada raised its policy rate by a quarter point to 2.5% on October 28. The next announcement is December 9. FVREB's CEO said buyers will need to consider how borrowing costs factor into their decisions."),

        Hd(2, 'By area and home type'),
        P('Price is FVREB\'s MLS® HPI benchmark for a typical home, and 1 year is its change from October 2025. Sales and active listings are October figures. Ratio is derived: sales divided by active listings. '
          'The Fraser Valley row covers every area FVREB reports. An asterisk means fewer than 10 sales, so the ratio and percentages swing a lot.'),
        table('Detached', 'detached'), table('Townhouse', 'townhouse'), table('Apartment', 'apartment'),
        P("FVREB reports White Rock and South Surrey as one area, so there is no South Surrey-only line. Its Surrey combined line covers North, Central, Cloverdale and South Surrey (excluding White Rock) and has no listings count. "
          "Because it includes part of South Surrey, don't add it to the White Rock / South Surrey row."),

        Hd(2, 'Area by area'),
        Hd(3, 'White Rock / South Surrey'),
        P(f"FVREB reports the two as one area. Detached sales were {c(ws, 'detached')['s']}, down from {c(ws, 'detached')['sy']} a year ago ({pct(c(ws, 'detached')['syc'])}) and from {c(ws, 'detached')['sm']} in September. "
          f"Townhouse sales fell from {c(ws, 'townhouse')['sy']} to {c(ws, 'townhouse')['s']} ({pct(c(ws, 'townhouse')['syc'])}). Apartment sales held up better: {c(ws, 'apartment')['s']}, against {c(ws, 'apartment')['sy']} last October."),
        P(f"Benchmarks: detached {money(c(ws, 'detached')['b'])} ({pct(c(ws, 'detached')['by'])} on the year), townhouse {money(c(ws, 'townhouse')['b'])} ({pct(c(ws, 'townhouse')['by'])}) and apartment {money(c(ws, 'apartment')['b'])} ({pct(c(ws, 'apartment')['by'])}). "
          f"The townhouse and apartment benchmarks both rose from September, by {down(c(ws, 'townhouse')['bm'])} and {down(c(ws, 'apartment')['bm'])}. "
          f"The detached derived ratio is {c(ws, 'detached')['r']:.1f}%, with {c(ws, 'detached')['a']} homes active. The all-types benchmark is {money(comp['South Surrey & White Rock']['benchmark'])}, down {down(comp['South Surrey & White Rock']['chg_1y'])} in a year."),
        Hd(3, 'Langley'),
        P(f"Townhouses are the tight spot again. {c(la, 'townhouse')['s']} sales on {c(la, 'townhouse')['a']} active listings is {c(la, 'townhouse')['r']:.1f}% (derived), well above FVREB's balanced range, and townhouse sales were up {down(c(la, 'townhouse')['syc'])} from last October. "
          f"The townhouse benchmark is {money(c(la, 'townhouse')['b'])} ({pct(c(la, 'townhouse')['by'])})."),
        P(f"Detached sales fell from {c(la, 'detached')['sy']} to {c(la, 'detached')['s']} ({pct(c(la, 'detached')['syc'])}). The detached benchmark is {money(c(la, 'detached')['b'])} ({pct(c(la, 'detached')['by'])}), down {down(c(la, 'detached')['bm'])} from September. "
          f"Apartments sit at {c(la, 'apartment')['r']:.1f}% (derived), with active listings down {down(c(la, 'apartment')['ay'])} from a year ago to {c(la, 'apartment')['a']}."),
        Hd(3, 'Surrey'),
        P(f"Surrey combined had {c(su, 'detached')['s']} detached sales, up from {c(su, 'detached')['sy']} ({pct(c(su, 'detached')['syc'])}). Townhouse sales fell from {c(su, 'townhouse')['sy']} to {c(su, 'townhouse')['s']} ({pct(c(su, 'townhouse')['syc'])}) "
          f"and apartment sales from {c(su, 'apartment')['sy']} to {c(su, 'apartment')['s']} ({pct(c(su, 'apartment')['syc'])}). "
          f"Benchmarks: detached {money(c(su, 'detached')['b'])} ({pct(c(su, 'detached')['by'])}), townhouse {money(c(su, 'townhouse')['b'])} ({pct(c(su, 'townhouse')['by'])}), apartment {money(c(su, 'apartment')['b'])} ({pct(c(su, 'apartment')['by'])})."),
        P(f"The areas differ. Surrey Central detached sales rose from {c(sc, 'detached')['sy']} to {c(sc, 'detached')['s']}, and its detached ratio is {c(sc, 'detached')['r']:.1f}% (derived). "
          f"Surrey North has {c(sn, 'apartment')['a']} active apartments against {c(sn, 'apartment')['s']} sales ({c(sn, 'apartment')['r']:.1f}%, derived), with the apartment benchmark at {money(c(sn, 'apartment')['b'])} ({pct(c(sn, 'apartment')['by'])})."),
        Hd(3, 'Cloverdale'),
        P(f"Cloverdale's all-types benchmark is {money(comp['Cloverdale']['benchmark'])}, down {down(comp['Cloverdale']['chg_1y'])} on the year. That is the smallest drop of any area FVREB reports. "
          f"Detached is {money(c(cl, 'detached')['b'])} ({pct(c(cl, 'detached')['by'])}) with {c(cl, 'detached')['s']} sales on {c(cl, 'detached')['a']} active ({c(cl, 'detached')['r']:.1f}%, derived)."),
        P(f"Townhouses are {money(c(cl, 'townhouse')['b'])} ({pct(c(cl, 'townhouse')['by'])}) with {c(cl, 'townhouse')['s']} sales on {c(cl, 'townhouse')['a']} active ({c(cl, 'townhouse')['r']:.1f}%, derived). "
          f"Apartments had only {c(cl, 'apartment')['s']} sales, too few to read much into."),
        Hd(3, 'Abbotsford'),
        P(f"Abbotsford's detached sales rose the most of any area here: {c(ab, 'detached')['s']}, up from {c(ab, 'detached')['sy']} last October ({pct(c(ab, 'detached')['syc'])}) and from {c(ab, 'detached')['sm']} in September. "
          f"With {c(ab, 'detached')['a']} detached homes active, the derived ratio is {c(ab, 'detached')['r']:.1f}%."),
        P(f"Prices are still lower. The detached benchmark is {money(c(ab, 'detached')['b'])}, down {down(c(ab, 'detached')['by'])} in a year, which ties Mission for the largest annual detached drop here. "
          f"Townhouses are {money(c(ab, 'townhouse')['b'])} ({pct(c(ab, 'townhouse')['by'])}) at {c(ab, 'townhouse')['r']:.1f}% (derived), and apartments are {money(c(ab, 'apartment')['b'])} ({pct(c(ab, 'apartment')['by'])}). "
          f"The all-types benchmark is {money(comp['Abbotsford']['benchmark'])} ({pct(comp['Abbotsford']['chg_1y'])})."),
        Hd(3, 'North Delta'),
        P("FVREB covers North Delta only. It publishes no Ladner or Tsawwassen figures, so I can't report those from this package."),
        P(f"Detached sales were {c(nd, 'detached')['s']}, up from {c(nd, 'detached')['sy']} ({pct(c(nd, 'detached')['syc'])}), while detached active listings fell {down(c(nd, 'detached')['ay'])} to {c(nd, 'detached')['a']}. "
          f"That puts the derived ratio at {c(nd, 'detached')['r']:.1f}%, just above FVREB's balanced range. The detached benchmark is {money(c(nd, 'detached')['b'])} ({pct(c(nd, 'detached')['by'])}). "
          f"Townhouses and apartments had {c(nd, 'townhouse')['s']} and {c(nd, 'apartment')['s']} sales, so skip the percentages there. The all-types benchmark is {money(comp['North Delta']['benchmark'])} ({pct(comp['North Delta']['chg_1y'])})."),
        Hd(3, 'Mission'),
        P(f"Mission had the slowest detached market here. Detached sales fell from {c(mi, 'detached')['sy']} to {c(mi, 'detached')['s']} ({pct(c(mi, 'detached')['syc'])}), with {c(mi, 'detached')['a']} homes active ({c(mi, 'detached')['r']:.1f}%, derived). "
          f"The detached benchmark is {money(c(mi, 'detached')['b'])} ({pct(c(mi, 'detached')['by'])}) and the all-types benchmark is {money(comp['Mission']['benchmark'])} ({pct(comp['Mission']['chg_1y'])}), the largest annual drop of any area. "
          f"Townhouses and apartments had {c(mi, 'townhouse')['s']} and {c(mi, 'apartment')['s']} sales."),

        Hd(2, 'What this means for buyers'),
        P(f"Sales picked up, but this is still a buyer's market. There are {R['active'][0]:,} active listings, the board-wide ratio is {R['ratio']}%, and prices are lower than a year ago in every area and home type above. "
          "FVREB's CEO said affordability is at its best level in five years."),
        P('Two things to watch. Where the ratio is higher, like Langley townhouses and North Delta detached homes, a well-priced home can draw competition. And borrowing costs just went up, with the Bank of Canada raising its rate on October 28. Run your budget with the ',
          ('first-time buyer calculator', '/first-time-buyer-calculator.html'), ' before you write an offer.'),

        Hd(2, 'What this means for sellers'),
        P("Price to today's sales, not last year's. Benchmarks are lower than a year ago in every area and type above, though a few ticked up from September."),
        P(f"Fewer new listings came on in October ({R['new'][0]:,}, down {down(R['new'][1])} from September). That is normal for the season, and it means less competition for a home that is priced right. Detached homes are leading sales. A ",
          ('home evaluation', '/home-evaluation.html'), ' shows where your home sits, and my ', ('marketing plan', '/selling.html'), ' shows how I would sell it.'),
        P('Benchmarks describe what happened, not what will happen. This is general information, not advice for your situation.'),

        Hd(2, 'Where these numbers come from'),
        P('Market figures: ', ('FVREB October 2026 statistics package', PACKAGE_URL), ' (news release dated November 3, 2026): news release, MLS® Summary and MLS® Home Price Index pages. Policy rate: ',
          ('Bank of Canada, October 28, 2026', BOC_URL), '. Derived ratios are October sales divided by October active listings, calculated from the package figures. FVREB reports White Rock and South Surrey as one area.'),
        P('Want numbers for your street or complex? Call or text me at 604-928-1361.'),
        P('Last month: ', PREV, '. Monthly figures by area: ', ('Fraser Valley market stats', '/fraser-valley-market-stats.html'), '.'),

        {'t': 'h', 'level': 2, 'text': 'More local reading', 'gen': GEN, 'pos': 'end'},
        {'t': 'list', 'gen': GEN, 'pos': 'end', 'items': [[{'t': t, 'h': h}] for t, h in [
            ('South Surrey homes for sale', '/south-surrey-homes-for-sale.html'), ('White Rock homes for sale', '/white-rock.html'), ('Langley homes for sale', '/langley-homes-for-sale.html'),
            ('Surrey homes for sale', '/surrey-homes-for-sale.html'), ('Cloverdale homes for sale', '/cloverdale-bc.html'), ('Abbotsford homes for sale', '/abbotsford-homes-for-sale.html'),
            ('North Delta homes for sale', '/north-delta-homes-for-sale.html'), ('Mission homes for sale', '/mission-homes-for-sale.html'),
            ('South Surrey and White Rock guides', '/south-surrey-neighbourhoods.html'), ('Langley guides', '/langley-neighbourhood-guides.html'), ('Surrey guides', '/surrey-neighbourhood-guides.html'),
            ('All blog posts', '/blog.html')]]},
    ]
    faq = [
        {'q': "Is the Fraser Valley a buyer's market in October 2026?", 'a': f"Yes. The board-wide sales-to-active listings ratio was {R['ratio']}%, and FVREB defines a balanced market as 12% to 20%. There were {R['active'][0]:,} active listings and {R['sales'][0]:,} sales in the month.", 'gen': GEN},
        {'q': 'How many homes sold in the Fraser Valley in October 2026?', 'a': f"{R['sales'][0]:,} on the board's MLS®, up {down(R['sales'][1])} from September and down {down(R['sales'][2])} from October 2025, according to the Fraser Valley Real Estate Board.", 'gen': GEN},
        {'q': 'What is the benchmark price of a detached home in the Fraser Valley?', 'a': f"{money(F['detached']['benchmark']['now'])} in October 2026, down {down(F['detached']['benchmark']['chg_month'])} from September and {down(F['detached']['benchmark']['chg_year'])} from October 2025. Townhouses are {money(F['townhouse']['benchmark']['now'])} and apartments {money(F['apartment']['benchmark']['now'])}.", 'gen': GEN},
        {'q': 'What are benchmark prices in South Surrey and White Rock?', 'a': f"{money(c(ws, 'detached')['b'])} for a detached home, {money(c(ws, 'townhouse')['b'])} for a townhouse and {money(c(ws, 'apartment')['b'])} for an apartment in October 2026. FVREB reports the two as one area.", 'gen': GEN},
        {'q': 'What did the Bank of Canada do in October 2026?', 'a': 'It raised its policy rate by a quarter point to 2.5% on October 28, 2026, its first increase in more than three years. The next announcement is December 9, 2026.', 'gen': GEN},
    ]
    title = 'October 2026 Market Update: Fraser Valley, Surrey, Langley'
    h1 = 'October 2026 Market Update: Fraser Valley, Surrey & Langley'
    desc = (f"FVREB October 2026 numbers: {R['sales'][0]:,} Fraser Valley sales, an {money(fv['benchmark'])} benchmark and {R['active'][0]:,} listings, plus South Surrey, Langley, Surrey and Abbotsford.")
    assert len(title) <= 60 and len(h1) <= 60 and 135 <= len(desc) <= 158, (len(title), len(h1), len(desc))
    page = {'status': 'draft', 'slug': SLUG, 'updated': '2026-11-12', 'hand_edited': True,
            'new_page': {'title': title, 'description': desc, 'h1': h1},
            'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Blog', 'href': '/blog.html'}, {'name': 'October 2026 Market Update', 'href': f'/{SLUG}.html'}],
            'published': '2026-11-12', 'market_update': MONTH,
            'blocks': blocks, 'faq': faq, 'faq_heading': 'October 2026 market questions'}
    out = f'{ROOT}/src/data/local/{SLUG}.json'
    open(out, 'w').write(json.dumps(page, indent=2, ensure_ascii=False) + '\n')
    print('wrote', os.path.relpath(out, ROOT), len(blocks), 'blocks;', 'title', len(title), 'h1', len(h1), 'desc', len(desc))


# ---------------------------------------------------------------------------------------------------------------------------
# September 2026 (the archived post). Its wording is kept as archived; only its tables are rebuilt. The archive capture had
# flattened every table into a list of single numbers, with the area names mixed in as headings (D-257).
SEP_SLUG = 'september-2026-market-update-south-surrey-white-rock-langley'
SEP_TOTALS = {'sales': (922, -2.0, -4.2), 'new': (2818, 18.8, -18.2), 'active': (9763, -0.2, -7.7), 'avg': (954833, 1.1, -3.2)}   # now, vs August, vs September 2025
SEP_PDF_CHECK = ['For Immediate Release: October 5, 2026', '922', '962', '-4.2%', '941', '-2.0%', '2,818', '3,447', '-18.2%', '2,373', '18.8%',
                 '9,763', '10,583', '-7.7%', '9,787', '-0.2%', '954,833', '986,674', '-3.2%', '944,900', '1.1%']


def september():
    flat = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', '3', f'{ROOT}/docs/research/market-data/FVREB-Package-2026-09.pdf', '-'], capture_output=True, text=True, check=True).stdout)
    missing = [x for x in SEP_PDF_CHECK if x not in flat]
    assert not missing, f'not found in the September package text: {missing}'
    S = json.load(open(f'{ROOT}/src/data/market/2026-09.json'))['fvreb']['summary']
    A = json.load(open(f'{ROOT}/src/data/pages/{SEP_SLUG}.json'))['blocks']
    txt = lambda b: ' '.join(x['t'] for x in b.get('parts', [])) if b['t'] == 'p' else b.get('text', '') if b['t'] == 'h' else ' '.join(x['t'] for it in b.get('items', []) for x in it)
    money = lambda n: f'${n:,.0f}'
    pct = lambda x: f'{x:+.1f}%'.replace('+0.0%', '0.0%')

    def keep(i, starts):          # an archived block, word for word; the opening words are checked so a changed record stops the build
        assert txt(A[i]).startswith(starts), (i, txt(A[i])[:60])
        b = dict(A[i]); b['gen'] = GEN
        if b['t'] == 'p': b['parts'] = [{**x, **({'h': x['h'].replace('https://jaredgibbons.ca', '')} if x.get('h') else {})} for x in b['parts']]
        return b
    Hd = lambda lv, text: {'t': 'h', 'level': lv, 'text': text, 'gen': GEN}

    ROWS = [('Fraser Valley', 'All Areas Combined'), ('White Rock / South Surrey', 'White Rock / South Surrey'), ('Langley', 'Langley'), ('Surrey combined', 'City of Surrey - Combined'),
            ('Surrey - Central', 'Surrey - Central'), ('Surrey - North', 'Surrey - North'), ('Cloverdale', 'Surrey - Cloverdale'), ('Abbotsford', 'Abbotsford'), ('North Delta', 'Delta - North')]
    archived = ' | '.join(txt(b) for b in A[18:40])        # the flattened tables: every number rebuilt below must be one the old page printed

    def table(label, t):
        rows = []
        for name, a in ROWS:
            x = S[a][t]; s = x['sales']['now']; act = x.get('active', {}).get('now'); r = f'{100 * s / act:.1f}%' if act else 'n/a'
            row = [name + ('*' if s < 10 else ''), money(x['benchmark']['now']), pct(x['benchmark']['chg_year']), f'{s:,}', f'{act:,}' if act else 'n/a', r]
            for v in (row[1], row[3], row[4], row[5]):
                assert v in archived, f'{label} {name}: {v} is not on the archived page'
            rows.append(row)
        return {'t': 'table', 'caption': f'{label}, September 2026', 'head': ['Area', 'Price', 'y/y', 'Sales', 'Active', 'Ratio (derived)'], 'rows': rows, 'gen': GEN}

    T = SEP_TOTALS
    for v in ('922', '2,818', '+18.8%', '9,763', '$954,833', '+1.1%'): assert v in txt(A[11]), v
    blocks = [
        keep(1, 'The Fraser Valley Real Estate Board (FVREB) published its September numbers'), keep(2, 'Below: the Fraser Valley overall'),
        keep(3, 'The short version'), keep(4, 'The board recorded 922 sales'), keep(5, 'The board-wide sales-to-active ratio was 9%'), keep(6, 'The composite benchmark price is $861,300'), keep(7, 'Among rows with 10 or more sales'),
        keep(8, 'Fraser Valley overall'),
        {'t': 'table', 'caption': 'All property types, September 2026', 'head': ['Measure', 'September 2026', 'From August', 'From September 2025'], 'gen': GEN, 'rows': [
            ['Sales', f"{T['sales'][0]:,}", pct(T['sales'][1]), pct(T['sales'][2])], ['New listings', f"{T['new'][0]:,}", pct(T['new'][1]), pct(T['new'][2])],
            ['Active listings', f"{T['active'][0]:,}", pct(T['active'][1]), pct(T['active'][2])], ['Average price', money(T['avg'][0]), pct(T['avg'][1]), pct(T['avg'][2])]],
         'source': 'Source: Fraser Valley Real Estate Board statistics package, September 2026 (released October 5, 2026).'},
        keep(12, 'The composite benchmark fell 1.0% from August'), keep(13, 'Homes took 45 days to sell'), keep(14, 'Average price is what homes actually sold for'), keep(15, 'The Bank of Canada held its policy rate at 2.25%'),
        keep(16, 'By area and home type'), keep(17, "Price is FVREB's MLS HPI benchmark"),
        table('Detached', 'detached'), table('Townhouse', 'townhouse'), table('Apartment', 'apartment'),
        keep(40, 'FVREB reports White Rock and South Surrey as one area'),
        Hd(2, 'Area by area'),
        Hd(3, txt(keep(41, 'White Rock / South Surrey (reported as one area)'))), keep(42, 'Sales are up while prices are down'), keep(43, 'The benchmarks fell anyway'),
        Hd(3, txt(keep(44, 'Langley'))), keep(45, "Langley's detached and townhouse benchmarks"), keep(46, 'Townhouses are the tight spot'),
        Hd(3, txt(keep(47, 'Surrey'))), keep(48, 'Surrey combined had 166 detached sales'), keep(49, 'The areas differ'),
        Hd(3, txt(keep(50, 'Cloverdale'))), keep(51, "Cloverdale's all-types benchmark is $921,900"), keep(52, 'Townhouses are $754,300'),
        Hd(3, txt(keep(53, 'Abbotsford'))), keep(54, 'Abbotsford had the largest annual detached drop'), keep(55, 'Townhouse sales fell from 37 to 27'),
        Hd(3, txt(keep(56, 'North Delta'))), keep(57, 'FVREB covers North Delta only'), keep(58, 'Detached sales were 24'),
        keep(59, 'What this means for buyers'), keep(60, 'Inventory is 31% above'), keep(61, 'Where the ratio is higher'),
        keep(62, 'What this means for sellers'), keep(63, "Price to today's sales"), keep(64, 'With 9,763 homes competing'), keep(65, 'Benchmarks describe what happened'),
        keep(66, 'Where these numbers come from'),
        # the archive had split this sentence in three and lost its links; same words, the monthly-report aside (a link with nowhere to go) left out
        {'t': 'p', 'gen': GEN, 'parts': [{'t': 'Market figures:'}, {'t': 'FVREB September 2026 statistics package', 'lead': True},
            {'t': '(news release dated October 5, 2026): news release, MLS Summary and MLS Home Price Index pages. Policy rate:'},
            {'t': 'Bank of Canada', 'h': 'https://www.bankofcanada.ca/rates/interest-rates/canadian-interest-rates/'},
            {'t': '. Derived ratios are September sales divided by September active listings, calculated from the package figures. FVREB reports White Rock and South Surrey as one area.'}]},
        keep(70, 'Want numbers for your street or complex?'), keep(71, 'Jared Gibbons PREC'),
        {'t': 'p', 'gen': GEN, 'parts': [{'t': 'Next month:'}, {'t': 'October 2026 market update', 'h': f'/{SLUG}.html'}, {'t': '.'}]},
        {'t': 'h', 'level': 2, 'text': 'More local reading', 'gen': GEN, 'pos': 'end'},
        {'t': 'list', 'gen': GEN, 'pos': 'end', 'items': [[{'t': t, 'h': h}] for t, h in [
            ('South Surrey homes for sale', '/south-surrey-homes-for-sale.html'), ('White Rock homes for sale', '/white-rock.html'), ('Langley homes for sale', '/langley-homes-for-sale.html'),
            ('Surrey homes for sale', '/surrey-homes-for-sale.html'), ('Cloverdale homes for sale', '/cloverdale-bc.html'), ('Abbotsford homes for sale', '/abbotsford-homes-for-sale.html'),
            ('North Delta homes for sale', '/north-delta-homes-for-sale.html'),
            ('Surrey guides', '/surrey-neighbourhood-guides.html'), ('South Surrey and White Rock guides', '/south-surrey-neighbourhoods.html'), ('Langley guides', '/langley-neighbourhood-guides.html'),
            ('Abbotsford guides', '/abbotsford-neighbourhood-guides.html'), ('Delta guides', '/delta-neighbourhood-guides.html'), ('Cloverdale guides', '/cloverdale-neighbourhood-guides.html'),
            ('All blog posts', '/blog.html')]]},
    ]
    assert txt(A[69]).startswith('Bank of Canada . Derived ratios are September sales') or txt(A[69]).startswith('Bank of Canada'), txt(A[69])[:60]
    out = f'{ROOT}/src/data/local/{SEP_SLUG}.json'
    cur = json.load(open(out))
    page = {'status': cur.get('status', 'draft'), 'slug': SEP_SLUG, 'updated': '2026-11-12', 'hand_edited': True, 'replace_body': True,
            'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Blog', 'href': '/blog.html'}, {'name': 'September 2026 Market Update', 'href': f'/{SEP_SLUG}.html'}],
            'blocks': blocks, 'faq': cur.get('faq', [])}
    open(out, 'w').write(json.dumps(page, indent=2, ensure_ascii=False) + '\n')
    print('wrote', os.path.relpath(out, ROOT), len(blocks), 'blocks (archived wording, tables rebuilt)')


def link_from_stats_page():
    """The market-stats hub points at the newest written update (one paragraph after its introduction)."""
    f = f'{ROOT}/src/data/local/fraser-valley-market-stats.json'
    raw = open(f).read(); d = json.loads(raw)
    indent = 2 if raw.startswith('{\n  "') else 1
    d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'mktupdate-link']
    d['blocks'].insert(0, {'t': 'p', 'gen': 'mktupdate-link', 'parts': [{'t': 'The numbers in words:'}, {'t': 'October 2026 market update for the Fraser Valley, Surrey and Langley', 'h': f'/{SLUG}.html'}, {'t': '.'}]})
    open(f, 'w').write(json.dumps(d, indent=indent, ensure_ascii=False) + ('\n' if raw.endswith('\n') else ''))
    print('linked from', os.path.relpath(f, ROOT))


if __name__ == '__main__':
    main()
    september()
    link_from_stats_page()
