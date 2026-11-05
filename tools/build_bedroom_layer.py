"""Bedroom-count aggregates for condos and townhomes (Jared, 2026-11-04: bedroom pages for his nine cities plus White Rock).

  python3 -I tools/build_bedroom_layer.py --csv <Paragon closed-sales export.csv>   ->  src/data/sold/sold-beds.json

Same rules as the sold layer: closed sales only, the saved window's last day, grouped figures only (raw rows carry MLS numbers and never enter the repo),
a median needs 5 sales, a name 3 sales.  Studios (0 bedrooms) are left out; "3 bedroom" means 3 or more.
"""
import argparse, collections, csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sold_layer as S

ROOT = S.ROOT
OUT = os.path.join(ROOT, 'src/data/sold/sold-beds.json')
# city key -> (display, [(Paragon area, only sub-areas or None, excluded sub-areas)], how the page describes the area)
CITIES = {
 'surrey': ('Surrey', [('Surrey', None, ()), ('North Surrey', None, ())], 'the Surrey and North Surrey board areas (Cloverdale and South Surrey have their own pages)'),
 'south-surrey': ('South Surrey', [('South Surrey White Rock', None, ('White Rock',))], 'the South Surrey and White Rock board area without White Rock itself'),
 'white-rock': ('White Rock', [('South Surrey White Rock', ('White Rock',), ())], 'White Rock'),
 'cloverdale': ('Cloverdale', [('Cloverdale', None, ())], 'the Cloverdale board area'),
 'north-delta': ('North Delta', [('N. Delta', None, ())], 'the North Delta board area'),
 'ladner': ('Ladner', [('Ladner', None, ())], 'the Ladner board area'),
 'tsawwassen': ('Tsawwassen', [('Tsawwassen', None, ())], 'the Tsawwassen board area'),
 'langley': ('Langley', [('Langley', None, ())], 'the Langley board area (City and Township)'),
 'abbotsford': ('Abbotsford', [('Abbotsford', None, ())], 'the Abbotsford board area'),
 'chilliwack': ('Chilliwack', [('Chilliwack', None, ()), ('Sardis', None, ())], 'the Chilliwack and Sardis board areas'),
}
BEDS = {'1': lambda b: b == 1, '2': lambda b: b == 2, '3': lambda b: b >= 3}


def bedn(a):
    try: return int(float(a['Total Bedrooms']))
    except (ValueError, TypeError): return None


def pick(rows, sel):
    out = []
    for a in rows:
        for ar, only, ex in sel:
            if a['Area'] != ar: continue
            sub = a['Sub-Area/Community']
            if only is not None and sub not in only: continue
            if sub in ex: continue
            out.append(a); break
    return out


def entry(rows, g):
    s = S.stats(rows, g)
    o = {k: v for k, v in s.items()}
    o['bands'] = S.band_counts(rows)
    subs = collections.defaultdict(list)
    for a in rows: subs[a['Sub-Area/Community']].append(a)
    o['subs'] = sorted(({'name': k, **{x: v for x, v in S.stats(v, g).items() if x in ('n', 'price', 'ppsf', 'dom')}, 'top': [{y: z for y, z in c.items() if y in ('name', 'n', 'price', 'yb')} for c in S.complexes(v)[:3]]} for k, v in subs.items() if len(v) >= S.MIN_MED), key=lambda x: -x['n'])
    o['complexes'] = S.complexes(rows)[:12]
    fa = [(S.num(r['Floor Area -Grand Total'].replace(',', '')) if r['Floor Area -Grand Total'] else None, S.num(r['Sold Price']), r) for r in rows]
    sq = [x for x in (f for f, _, _ in fa) if x and x > 200]
    if len(sq) >= S.MIN_MED: o['sqft'] = round(S.med(sq))
    SZ = [(0, 600, 'Under 600 sq ft'), (600, 800, '600 to 799 sq ft'), (800, 1000, '800 to 999 sq ft'), (1000, 1300, '1,000 to 1,299 sq ft'), (1300, 10 ** 9, '1,300 sq ft and over')] if g == 'condo' else \
         [(0, 1000, 'Under 1,000 sq ft'), (1000, 1300, '1,000 to 1,299 sq ft'), (1300, 1600, '1,300 to 1,599 sq ft'), (1600, 10 ** 9, '1,600 sq ft and over')]
    o['size'] = [{'label': lab, 'n': len(v), 'price': round(S.med([p for _, p, _ in v if p])) if len(v) >= S.MIN_MED else None} for lo, hi, lab in SZ for v in [[x for x in fa if x[0] and lo <= x[0] < hi]] if v]
    AG = [(0, 1990, 'Built before 1990'), (1990, 2000, 'Built 1990 to 1999'), (2000, 2010, 'Built 2000 to 2009'), (2010, 2020, 'Built 2010 to 2019'), (2020, 3000, 'Built 2020 or later')]
    ya = [(S.num(r['Approx. Year Built']), S.num(r['Sold Price'])) for r in rows]
    o['age'] = [{'label': lab, 'n': len(v), 'price': round(S.med([p for _, p in v if p])) if len(v) >= S.MIN_MED else None} for lo, hi, lab in AG for v in [[x for x in ya if x[0] and lo <= x[0] < hi]] if v]
    return o


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--csv', required=True); a = ap.parse_args()
    last = json.load(open(S.AGG, encoding='utf-8'))['meta']['last']
    rows = [r for r in csv.DictReader(open(a.csv, encoding='utf-8-sig')) if r['Status'] == 'Closed' and S.group_of(r) in ('condo', 'townhome') and r['Sold Date'] <= last]
    out = {'meta': {'window': S.WINDOW, 'last': last, 'note': 'Closed sales only; grouped figures; studios excluded; 3 means 3 or more bedrooms.'}, 'cities': {}}
    for ck, (disp, sel, desc) in CITIES.items():
        cr = pick(rows, sel); c = {'name': disp, 'desc': desc, 'groups': {}}
        for g in ('condo', 'townhome'):
            gr = [r for r in cr if S.group_of(r) == g]; c['groups'][g] = {}
            for bk, fn in BEDS.items():
                br = [r for r in gr if bedn(r) is not None and fn(bedn(r))]
                if br: c['groups'][g][bk] = entry(br, g)
        out['cities'][ck] = c
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('rows used', len(rows))
    for ck, c in out['cities'].items():
        print(f"{c['name']:14}", ' '.join(f"{g[0]}{bk}:{c['groups'][g].get(bk, {}).get('n', 0):<4}" for g in ('condo', 'townhome') for bk in BEDS))


if __name__ == '__main__':
    main()
