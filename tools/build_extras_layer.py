#!/usr/bin/env python3
"""Extras layer from Pete's Paragon sold export (Closed only, Nov 1, 2025 to Nov 6, 2026): suites, coach houses and penthouses.

    python3 -I tools/build_extras_layer.py --dir <folder with the RD_/RA_ csv files> [--dir <second folder>] [--status Closed,<other status>] [--end 2026-10-31]
                                                                                writes src/data/sold/sold-extras.json
    With the September-to-today re-pull: pass both folders, the extra status Pete pulled it under, and the new --end date. Rows are matched on ML # so a sale in both folders counts once.

Window: November 1, 2025 to August 31, 2026.  The export only has sales Paragon had marked Closed, and sales thin out after August (803 detached in September, 111 in October),
so later months are left out until Pete re-pulls them.  Rules are the same as the main sold layer: grouped figures only (the raw rows carry MLS numbers and never enter the repo),
a median needs 5 sales, a count is mentioned at 3, a building is named at 3 and priced at 5.  Map columns by header name.

Groups
  house        House/Single Family (the base for the others)
  legal        house with Legal Suite or Licensed Suite in the Suite field
  unauth       house whose only suite is marked Unauthorized
  coach        house, acreage house or half duplex with Carriage/Coach House or Laneway House in Style of Home (the only coach house flag Paragon has)
  lane         house with Lane Access in Site Influences
  second       house with a floor area in Det'd 2nd Residence
  condo        Apartment/Condo (the base for penthouses)
  pent         Apartment/Condo with Penthouse in Style of Home
"""
import argparse, collections, csv, datetime, glob, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_sold_layer as S

OUT = 'src/data/sold/sold-extras.json'
END = datetime.date(2026, 8, 31)
CITY = {
    'surrey': [('Surrey', ()), ('North Surrey', ())], 'cloverdale': [('Cloverdale', ())], 'south-surrey': [('South Surrey White Rock', ('White Rock',))],
    'white-rock': [('South Surrey White Rock', 'ONLY:White Rock')], 'south-surrey-white-rock': [('South Surrey White Rock', ())], 'langley': [('Langley', ())], 'abbotsford': [('Abbotsford', ())],
    'burnaby': [('Burnaby North', ()), ('Burnaby South', ()), ('Burnaby East', ())], 'coquitlam': [('Coquitlam', ())], 'richmond': [('Richmond', ())],
    'vancouver': [('Vancouver West', ()), ('Vancouver East', ())], 'north-delta': [('N. Delta', ())], 'ladner': [('Ladner', ())], 'tsawwassen': [('Tsawwassen', ())],
    'maple-ridge': [('Maple Ridge', ())], 'chilliwack': [('Chilliwack', ()), ('Sardis', ())], 'port-coquitlam': [('Port Coquitlam', ())], 'port-moody': [('Port Moody', ())],
    'new-westminster': [('New Westminster', ())], 'mission': [('Mission', ())], 'pitt-meadows': [('Pitt Meadows', ())], 'north-vancouver': [('North Vancouver', ())],
}
HOUSE_T = ('House/Single Family',)
Q = [('2025-11', '2025-12', '2026-01'), ('2026-02', '2026-03', '2026-04'), ('2026-05', '2026-06', '2026-07'), ('2026-08',)]
BANDS_H = [0, 600e3, 800e3, 1e6, 1.2e6, 1.5e6, 1.8e6, 1e12]
BANDS_C = [0, 500e3, 750e3, 1e6, 1.5e6, 2e6, 1e12]


def toks(s): return [t.strip() for t in (s or '').split(',') if t.strip()]
def sold_date(a):
    m, d, y = a['Sold Date'].split('/'); return datetime.date(int(y), int(m), int(d))
def ym(a): d = sold_date(a); return f'{d.year}-{d.month:02d}'


def tags(a):
    t = a['Type of Dwelling']; su = toks(a.get('Suite')); st_ = toks(a.get('Style of Home')); si = toks(a.get('Site Influences'))
    g = set()
    if t in HOUSE_T:
        g.add('house')
        if 'Legal Suite' in su or 'Licensed Suite' in su: g.add('legal')
        elif 'Unauthorized Suite' in su: g.add('unauth')
        if 'Lane Access' in si: g.add('lane')
        if (S.num((a.get("Floor Area - Det'd 2nd Residence") or '').replace(',', '')) or 0) > 0: g.add('second')
    if t in HOUSE_T + ('House with Acreage', '1/2 Duplex') and any(x in ('Carriage/Coach House', 'Laneway House') for x in st_): g.add('coach')
    if t == 'Apartment/Condo':
        g.add('condo')
        if 'Penthouse' in st_: g.add('pent')
    return g


def bandcounts(p, edges): return [sum(1 for x in p if lo <= x < hi) for lo, hi in zip(edges, edges[1:])]


def stats(rows, kind):
    """kind 'h' for houses, 'c' for condos."""
    n = len(rows); o = {'n': n}
    if n < S.MIN_MENTION: return o
    p = [S.num(a['Sold Price']) for a in rows]; lp = [S.num(a['List Price']) for a in rows]
    o['dom'] = round(S.med([S.num(a['Days On Market']) for a in rows]))
    if n >= S.MIN_MED:
        o['price'] = round(S.med(p))
        rat = [100 * s / l for s, l in zip(p, lp) if s and l]
        o['ratio'] = round(S.med(rat), 1) if rat else None
        o['over'] = round(100 * sum(1 for s, l in zip(p, lp) if s and l and s > l) / n)
        if n >= 8: o['p25'] = round(S.pctile(p, .25)); o['p75'] = round(S.pctile(p, .75))
    fa = [(S.num(a['Sold Price']), S.num((a['Floor Area -Grand Total'] or '').replace(',', ''))) for a in rows]
    ppsf = [s / f for s, f in fa if s and f and f > 200]
    if len(ppsf) >= S.MIN_MED: o['ppsf'] = round(S.med(ppsf))
    fl = [f for s, f in fa if f and f > 200]
    if len(fl) >= S.MIN_MED: o['sqft'] = round(S.med(fl))
    yb = [S.num(a['Approx. Year Built']) for a in rows]; yb = [y for y in yb if y and 1850 < y < 2030]
    if len(yb) >= S.MIN_MENTION: o['yb'] = round(S.med(yb))
    bd = [S.num(a['Total Bedrooms']) for a in rows]; bd = [b for b in bd if b is not None]
    if len(bd) >= S.MIN_MED: o['beds'] = round(S.med(bd))
    if kind == 'h':
        ls = [S.num((a['Lot Sz (Sq.Ft.)'] or '').replace(',', '')) for a in rows]; ls = [x for x in ls if x]
        if len(ls) >= S.MIN_MED: o['lot_sqft'] = round(S.med(ls))
        ks = [S.num(a['# of Kitchens']) for a in rows]; ks = [k for k in ks if k is not None]
        if len(ks) >= S.MIN_MENTION: o['kitchens2'] = round(100 * sum(1 for k in ks if k >= 2) / len(ks))
    else:
        mf = [S.num(a['Maintenance Fee']) for a in rows]; mf = [m for m in mf if m and m > 0]
        if len(mf) >= S.MIN_MED: o['maint'] = round(S.med(mf))
    if n >= S.MIN_MED:
        o['bands'] = bandcounts(p, BANDS_H if kind == 'h' else BANDS_C)
        o['q'] = [{'n': len(qq), 'price': round(S.med([S.num(a['Sold Price']) for a in qq])) if len(qq) >= S.MIN_MED else None}
                  for qq in ([a for a in rows if ym(a) in ms] for ms in Q)]
    return o


def pick(rows, sel):
    out = []
    for a in rows:
        for area, ex in sel:
            if a['Area'] != area: continue
            sub = a['Sub-Area/Community']
            if isinstance(ex, str):
                if sub != ex.split(':')[1]: continue
            elif sub in ex: continue
            out.append(a); break
    return out


def buildings(rows):
    by = collections.defaultdict(list)
    for a in rows:
        nm = (a.get('Complex/Subdivision Name') or '').strip()
        if nm: by[S.ckey(nm)].append((nm, a))
    out = []
    for k, v in by.items():
        if len(v) < S.MIN_MENTION: continue
        nm = collections.Counter(x[0] for x in v).most_common(1)[0][0]
        e = stats([a for _, a in v], 'c'); e['name'] = S.nice(nm)
        sub = collections.Counter(a['Sub-Area/Community'] for _, a in v).most_common(1)[0][0]; e['sub'] = sub
        out.append(e)
    out.sort(key=lambda e: -e['n'])
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dir', required=True, action='append'); ap.add_argument('--status', default='Closed'); ap.add_argument('--end', default=END.isoformat()); a = ap.parse_args()
    end = datetime.date.fromisoformat(a.end); statuses = {x.strip() for x in a.status.split(',') if x.strip()}
    seen, rows = set(), []
    for d in a.dir:
        for f in sorted(glob.glob(os.path.join(d, 'R[AD]_*.csv'))):
            for r in csv.DictReader(open(f, encoding='utf-8-sig', errors='replace')):
                k = r.get('ML #')
                if k and k in seen: continue
                seen.add(k); rows.append(r)
    rows = [r for r in rows if sold_date(r) <= end and r['Status'] in statuses]
    print(len(rows), 'sales to', end, 'statuses', sorted(statuses))
    window = f"November 1, 2025 to {end.strftime('%B')} {end.day}, {end.year}"
    out = {'meta': {'window': window, 'first': '2025-11-01', 'last': end.isoformat(), 'closed': len(rows),
                    'source': f"Paragon sold export supplied by Pete ({', '.join(sorted(statuses))} status), window {window}. Raw rows are not stored."},
           'city': {}, 'sub': {}}
    for ck, sel in CITY.items():
        R = pick(rows, sel); tg = [(a, tags(a)) for a in R]
        ent = {'groups': {}}
        for g in ('house', 'legal', 'unauth', 'coach', 'lane', 'second', 'condo', 'pent'):
            gr = [a for a, t in tg if g in t]
            ent['groups'][g] = stats(gr, 'c' if g in ('condo', 'pent') else 'h')
        ent['pent_buildings'] = buildings([a for a, t in tg if 'pent' in t])
        out['city'][ck] = ent
        subs = collections.defaultdict(list)
        for a, t in tg: subs[a['Area'] + '|' + a['Sub-Area/Community']].append((a, t))
        for k, v in subs.items():
            e = {}
            for g in ('house', 'legal', 'coach', 'condo', 'pent'):
                gr = [a for a, t in v if g in t]
                if gr: e[g] = stats(gr, 'c' if g in ('condo', 'pent') else 'h')
            if any(x['n'] >= S.MIN_MENTION for g, x in e.items() if g in ('legal', 'coach', 'pent')):
                out['sub'].setdefault(ck + '#' + k, e)
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, separators=(',', ':'))
    print('wrote', OUT, os.path.getsize(OUT), 'bytes')
    for ck, e in out['city'].items():
        g = e['groups']; print(f"{ck:16}", {k: (v['n'], v.get('price')) for k, v in g.items()})


if __name__ == '__main__': main()
