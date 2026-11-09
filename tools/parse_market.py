"""Board statistics packages (text from `pdftotext -layout`) -> src/data/market/<yyyy-mm>.json

    pdftotext -layout GVR-Stats-Package-2026-09.pdf gvr.txt ; pdftotext -layout FVREB-Package-2026-09.pdf fvreb.txt
    python3 -I tools/parse_market.py --gvr gvr.txt --fvreb fvreb.txt --month 2026-09 --out src/data/market/2026-09.json

GVR: MLS HPI benchmark price, index and changes by area x property type (published October 2, 2026).
FVREB: MLS HPI by community x property type, and the MLS Summary pages (sales, new/active listings, benchmark, median,
average, with last-year and last-month comparisons) per community (published October 5, 2026).
Nothing is estimated; a value is stored only when the text row parses completely.
"""
import argparse, json, re

NUM = r'\$?\s?-?[\d,]+(?:\.\d+)?%?'


def n(s):
    s = s.replace('$', '').replace(',', '').replace('%', '').strip()
    return float(s) if '.' in s else int(s)


def parse_gvr(path):
    types = {'Residential / Composite': 'composite', 'Single Family Detached': 'detached', 'Townhouse': 'townhouse', 'Apartment': 'apartment'}
    out, cur = {}, None
    for line in open(path, encoding='utf-8'):
        s = line.rstrip()
        for label, key in types.items():
            if s.strip().startswith(label):
                cur = key; s = s.replace(label, '', 1)
        m = re.match(r'^\s*([A-Za-z][A-Za-z ./&-]+?)\s{2,}\$([\d,]+)\s+([\d.]+)((?:\s+-?[\d.]+%){5,7})\s*$', s)
        if m and cur:
            ch = [float(x.strip('% ')) for x in m.group(4).split()]
            area = m.group(1).strip()
            out.setdefault(area, {})[cur] = {'benchmark': n(m.group(2)), 'index': float(m.group(3)), 'chg_1m': ch[0], 'chg_3m': ch[1], 'chg_6m': ch[2], 'chg_1y': ch[3], 'chg_3y': ch[4], **({'chg_5y': ch[5]} if len(ch) > 5 else {}), **({'chg_10y': ch[6]} if len(ch) > 6 else {})}
    return out


def parse_fvreb(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    hpi, summary = {}, {}
    # HPI table
    cur = None
    for s in lines:
        m = re.match(r'^(RESIDENTIAL|DETACHED|TOWNHOUSE|APARTMENT)?\s*(COMBINED)?\s*([A-Z][A-Z &]+?)\s{2,}([\d,]+)\s+([\d.]+)((?:\s+-?[\d.]+){6,7})\s*$', s)
        if m:
            if m.group(1): cur = {'RESIDENTIAL': 'composite', 'DETACHED': 'detached', 'TOWNHOUSE': 'townhouse', 'APARTMENT': 'apartment'}[m.group(1)]
            area = m.group(3).strip()
            ch = [float(x) for x in m.group(6).split()]
            if cur:
                hpi.setdefault(area.title().replace('Fraser Valley Board', 'Fraser Valley Board'), {})[cur] = {'benchmark': n(m.group(4)), 'index': float(m.group(5)), 'chg_1m': ch[0], 'chg_3m': ch[1], 'chg_6m': ch[2], 'chg_1y': ch[3], 'chg_3y': ch[4], 'chg_5y': ch[5]}
    # MLS summary blocks: header line "<Community>  <Mon>-26 ..." followed by metric rows (3 property types x 5 columns)
    comm = None
    ptypes = ['detached', 'townhouse', 'apartment']
    for s in lines:
        h = re.match(r'^(All Areas Combined|[A-Z][A-Za-z .&/*-]+?)\s{2,}[A-Z][a-z]{2}-\d\d\s', s)
        if h and 'Grand Totals' not in s:
            comm = h.group(1).strip().rstrip('*').strip(); summary.setdefault(comm, {}); 
        row = re.match(r'^(Sales|New Listings|Active Listings|Benchmark Price|Median Price|Average Price)\s+(.*)$', s)
        if row and comm:
            toks = re.findall(r'\$?\s?-?[\d,]+(?:\.\d+)?%?|0%', row.group(2))
            toks = [t.replace(' ', '') for t in toks]
            if len(toks) != 15: continue
            metric = {'Sales': 'sales', 'New Listings': 'new_listings', 'Active Listings': 'active', 'Benchmark Price': 'benchmark', 'Median Price': 'median', 'Average Price': 'average'}[row.group(1)]
            for i, pt in enumerate(ptypes):
                a = toks[i * 5:(i + 1) * 5]
                summary[comm].setdefault(pt, {})[metric] = {'now': n(a[0]), 'last_year': n(a[1]), 'chg_year': n(a[2]), 'last_month': n(a[3]), 'chg_month': n(a[4])}
    return hpi, summary


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--gvr'); ap.add_argument('--fvreb'); ap.add_argument('--month'); ap.add_argument('--out'); ap.add_argument('--gvr-date', default='October 2, 2026'); ap.add_argument('--fvreb-date', default='October 5, 2026')
    a = ap.parse_args()
    gvr = parse_gvr(a.gvr); hpi, summ = parse_fvreb(a.fvreb)
    y, mo = a.month.split('-'); mname = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][int(mo) - 1]
    data = {'month': a.month,
            'gvr': {'source': f'Greater Vancouver REALTORS® MLS® Home Price Index, {mname} {y} (released {a.gvr_date})', 'hpi': gvr},
            'fvreb': {'source': f'Fraser Valley Real Estate Board Statistics Package, {mname} {y} (released {a.fvreb_date})', 'hpi': hpi, 'summary': summ}}
    json.dump(data, open(a.out, 'w'), indent=1, ensure_ascii=False)
    print(len(gvr), 'GVR areas;', len(hpi), 'FVREB HPI areas;', len(summ), 'FVREB summary communities')
