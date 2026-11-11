#!/usr/bin/env python3
"""Three-year closed sales for the small areas (D-222, Nov 11, 2026).

17 guides had too few sales in 12 months to show a typical price. Pete pulled Paragon closed sales for November 1, 2023 to
October 8, 2026 (small-areas-3yr-closed.xlsx, sent by Jared). This writes src/data/sold/sold-3yr-small.json: per guide, sales by home
type with the median price (5 sales needed, as on the 12-month layer), median year built, lot, bedrooms and days on market.
Raw rows are not stored. Mt Lehman's rows are marked unconfirmed in the export and are left out until Jerry's saved search confirms the area.
build_guide_facts.py and GenericPage.astro use it only where the 12-month layer has no price.
python3 -I tools/build_sold_3yr_small.py <path to small-areas-3yr-closed.xlsx>"""
import datetime, json, os, re, statistics, sys
import openpyxl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
GUIDE = {'Port Kells': 'port-kells-surrey-guide', 'Serpentine': 'serpentine-guide', 'Ladner Rural': 'ladner-rural-guide', 'East Delta': 'east-delta-guide',
         'Westham Island': 'westham-island-guide', 'West Meadows': 'west-meadows-pitt-meadows-guide', 'Sumas Mountain': 'sumas-mountain-guide',
         'Hemlock Valley': 'hemlock-valley-mission-guide', 'West Chilliwack': 'west-chilliwack-guide', 'Bridal Falls': 'bridal-falls-guide',
         'Lindell Beach (Cultus Lake South)': 'lindell-beach-bc-guide', 'Kent (Agassiz)': 'kent-bc-guide', 'Mount Currie': 'mount-currie-bc-guide',
         'Whitby Estates': 'whitby-estates-west-vancouver-guide'}
NAME = {'Lindell Beach (Cultus Lake South)': 'Lindell Beach', 'Kent (Agassiz)': 'Kent'}


def kind(r):
    t, p = r['Type of Dwelling'] or '', r['Prop Type'] or ''
    if p == 'Land Only': return 'land'
    if t == 'House with Acreage': return 'acreage'
    if t.startswith('Manufactured'): return 'mobile'
    if t == 'Apartment/Condo': return 'condo'
    if t == '1/2 Duplex': return 'duplex'
    if t in ('Townhouse', 'Row House (Non-Strata)'): return 'townhome'
    return 'house'


num = lambda v: float(re.sub(r'[^\d.]', '', str(v))) if v not in (None, '') and re.search(r'\d', str(v)) else None
med = lambda xs: (lambda ys: statistics.median(ys) if ys else None)([x for x in xs if x is not None])


def main():
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
    rows = list(wb['Closed sales'].iter_rows(values_only=True)); H = rows[0]; R = [dict(zip(H, r)) for r in rows[1:]]
    dates = [datetime.datetime.strptime(r['Sold Date'], '%m/%d/%Y').date() for r in R]
    out = {'meta': {'window': 'November 2023 to October 2026', 'first': str(min(dates)), 'last': str(max(dates)),
                    'source': 'Paragon closed sales pulled by Pete for 17 small areas, sent by Jared 2026-11-11. Raw rows are not stored.'}, 'guides': {}}
    for area, slug in GUIDE.items():
        rs = [r for r in R if r['Site area'] == area]
        g = {}
        for r in rs: g.setdefault(kind(r), []).append(r)
        groups = {}
        for k, v in g.items():
            e = {'n': len(v)}
            if len(v) >= 5:
                e['price'] = int(round(med(num(r['Sold Price']) for r in v), -3))
                yb = med(num(r['Approx. Year Built']) for r in v); e['yb'] = int(yb) if yb else None
                e['lot_sqft'] = int(med(num(r['Lot Sz (Sq.Ft.)']) for r in v) or 0) or None
                e['acres'] = round(med(num(r['Lot Sz (Acres)']) for r in v) or 0, 2) or None
                b = med(num(r['Total Bedrooms']) for r in v); e['beds'] = int(round(b)) if b else None
                e['dom'] = int(med(num(r['Days On Market']) for r in v))
            groups[k] = {x: y for x, y in e.items() if y is not None}
        out['guides'][slug] = {'area': NAME.get(area, area), 'n': len(rs), 'groups': groups}
    json.dump(out, open('src/data/sold/sold-3yr-small.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for s, v in out['guides'].items(): print(s, v['n'], {k: (x['n'], x.get('price')) for k, x in v['groups'].items()})


if __name__ == '__main__': main()
