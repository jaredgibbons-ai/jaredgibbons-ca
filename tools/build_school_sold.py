#!/usr/bin/env python3
"""Grouped sold figures within a radius of each school -> src/data/schools/radius-sold.json

Input: the Paragon exports Pete runs per school (Multi-Class > Map Search, radius from the school address, classes RD and RA, statuses Closed and Pending), one CSV per school,
named <school-slug>.csv (an 8-character upload prefix is ignored).  Rows are NEVER stored: only grouped figures (counts, medians, shares, sub-area and building counts).
Window: Sold Date November 1, 2025 to October 31, 2026 (Pending included, because a sale is made at acceptance and Closed lags).  A median is shown only where at least 5 sold.
   python3 -I tools/build_school_sold.py /path/to/csv/folder
"""
import csv, glob, json, os, re, statistics, string, sys, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
src = sys.argv[1] if len(sys.argv) > 1 else '/tmp/pilot'
LO, HI = dt.date(2025, 11, 1), dt.date(2026, 10, 31)
GROUPS = {'house': ['House/Single Family'], 'townhouse': ['Townhouse'], 'condo': ['Apartment/Condo']}
OUT = 'src/data/schools/radius-sold.json'
res = json.load(open(OUT)) if os.path.exists(OUT) else {}


def money(x):
    x = (x or '').replace('$', '').replace(',', '').strip()
    try: return float(x)
    except ValueError: return None


def med(v): return round(statistics.median(v)) if v else None


def stats(rows):
    n = len(rows); g = dict(n=n)
    if n < 5: return g
    pr = sorted(r['price'] for r in rows); g['price'] = med(pr)
    if n >= 10: g['p25'], g['p75'] = round(statistics.quantiles(pr, n=4)[0]), round(statistics.quantiles(pr, n=4)[2])
    pp = [r['price'] / r['sqft'] for r in rows if r['sqft'] and r['sqft'] > 200]; g['ppsf'] = med(pp) if len(pp) >= 5 else None
    dm = [r['dom'] for r in rows if r['dom'] is not None]; g['dom'] = med(dm) if len(dm) >= 5 else None
    rt = [100 * r['price'] / r['list'] for r in rows if r['list']]
    if len(rt) >= 5: g['ratio'] = round(statistics.median(rt), 1); g['over'] = round(100 * sum(1 for x in rt if x > 100.0) / len(rt))
    return g


for f in sorted(glob.glob(f'{src}/*.csv')):
    slug = re.sub(r'^[0-9a-f]{8}-', '', os.path.basename(f))[:-4]
    rows, total, inwin = [], 0, 0
    for r in csv.DictReader(open(f, encoding='utf-8-sig')):
        total += 1
        try: m, d, y = r['Sold Date'].split('/'); d0 = dt.date(int(y), int(m), int(d))
        except (ValueError, KeyError): continue
        if not (LO <= d0 <= HI) or r['Status'] not in ('Closed', 'Pending'): continue
        p = money(r['Sold Price'])
        if not p: continue
        inwin += 1
        try: sq = float(r['Floor Area -Grand Total'] or 0)
        except ValueError: sq = 0
        rows.append(dict(price=p, list=money(r['List Price']), sqft=sq, dom=int(r['Days On Market']) if (r['Days On Market'] or '').isdigit() else None,
                         t=r['Type of Dwelling'], sub=r['Sub-Area/Community'].strip(), cx=string.capwords(r['Complex/Subdivision Name'].strip())))
    o = dict(window=[LO.isoformat(), HI.isoformat()], rows=total, n=len(rows), all=stats(rows), groups={}, sub=[], complexes={})
    for k, ts in GROUPS.items(): o['groups'][k] = stats([r for r in rows if r['t'] in ts])
    o['groups']['other'] = dict(n=sum(1 for r in rows if not any(r['t'] in ts for ts in GROUPS.values())))
    subs = {}
    for r in rows: subs.setdefault(r['sub'], []).append(r)
    o['sub'] = sorted([[k, len(v)] + ([med([x['price'] for x in v])] if len(v) >= 5 else [None]) for k, v in subs.items() if k], key=lambda x: -x[1])[:6]
    for k in ('condo', 'townhouse'):
        cx = {}
        for r in rows:
            if r['t'] in GROUPS[k] and r['cx']: cx.setdefault(r['cx'], []).append(r['price'])
        o['complexes'][k] = sorted([[c, len(v), med(v) if len(v) >= 5 else None] for c, v in cx.items() if len(v) >= 3], key=lambda x: -x[1])[:5]
    res[slug] = o
    print(f'{slug:36} csv rows {total:4}  in window {len(rows):4}  house {o["groups"]["house"]["n"]} th {o["groups"]["townhouse"]["n"]} condo {o["groups"]["condo"]["n"]}')
json.dump(dict(sorted(res.items())), open(OUT, 'w'), indent=1, ensure_ascii=False)
