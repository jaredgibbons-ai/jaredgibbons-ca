"""Insert (or refresh) generated market sections in src/data/local/<slug>.json from src/data/market/<month>.json.

A local file opts in with a top-level "market_spec":
    {"board": "gvr", "area": "Maple Ridge", "label": "Maple Ridge"}                           # GVR HPI only
    {"board": "fvreb", "area": "Abbotsford", "summary": "Abbotsford", "label": "Abbotsford"}   # HPI + MLS summary
Optional "at": N puts the section after the first N hand-written blocks (default: end).
Generated blocks carry "gen": "market"; they are removed and rebuilt on every run, so a new month's file refreshes every page.
    python3 -I tools/apply_market.py [--month 2026-09]
"""
import argparse, glob, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
TYPES = [('composite', 'All home types'), ('detached', 'Detached'), ('townhouse', 'Townhouse'), ('apartment', 'Apartment')]


def money(v): return '${:,.0f}'.format(v)
def pct(v): return ('+' if v > 0 else '') + ('{:.1f}%'.format(v)).replace('-', '−') if v != 0 else '0.0%'
def move(v): return ('up ' if v > 0 else 'down ') + '{:.1f}%'.format(abs(v)) if v != 0 else 'unchanged'


def build(spec, data, month):
    y, m = month.split('-'); when = f'{MONTHS[int(m) - 1]} {y}'; label = spec['label']
    if spec['board'] == 'gvr':
        hpi = data['gvr']['hpi'][spec['area']]; src = data['gvr']['source']; summ = None
    else:
        hpi = data['fvreb']['hpi'][spec['area']]; src = data['fvreb']['source']; summ = data['fvreb']['summary'].get(spec.get('summary', ''))
    c, d, t, a = (hpi[k] for k in ('composite', 'detached', 'townhouse', 'apartment'))
    intro = (f'The MLS® Home Price Index benchmark for a typical {label} home was {money(c["benchmark"])} in {when}, '
             f'{move(c["chg_1y"])} from a year earlier. Detached homes were {money(d["benchmark"])} ({move(d["chg_1y"])} over the year), '
             f'townhouses {money(t["benchmark"])} ({move(t["chg_1y"])}) and apartments {money(a["benchmark"])} ({move(a["chg_1y"])}).')
    head = ['Home type', 'Benchmark price', 'Change in 1 month', 'Change in 1 year', 'Change in 3 years']
    rows = [[lab, money(hpi[k]['benchmark']), pct(hpi[k]['chg_1m']), pct(hpi[k]['chg_1y']), pct(hpi[k]['chg_3y'])] for k, lab in TYPES]
    blocks = [{'t': 'h', 'level': 2, 'text': f'{label} home prices, {when}', 'gen': 'market'},
              {'t': 'p', 'text': intro, 'gen': 'market'},
              {'t': 'table', 'caption': f'{label} MLS® benchmark prices, {when}', 'head': head, 'rows': rows, 'source': 'Source: ' + src + '.', 'gen': 'market'}]
    if summ:
        h2 = ['Home type', 'Sales', 'Active listings', 'Median sale price', 'Sales vs a year ago']
        r2 = []
        for k, lab in TYPES[1:]:
            s = summ.get(k, {})
            if 'sales' in s and 'active' in s and 'median' in s:
                r2.append([lab, str(s['sales']['now']), '{:,}'.format(s['active']['now']), money(s['median']['now']) if s['median']['now'] else 'n/a', pct(s['sales']['chg_year'])])
        if r2:
            blocks.append({'t': 'p', 'text': f'Sales activity in {label} for {when}, from the board\'s own monthly package: sales are the homes that sold in the month and active listings are the homes for sale at month end. Small counts make the median price jump around, so lean on the benchmark for the trend.', 'gen': 'market'})
            blocks.append({'t': 'table', 'caption': f'{label} MLS® sales activity, {when}', 'head': h2, 'rows': r2, 'source': 'Source: ' + data['fvreb']['source'] + '.', 'gen': 'market'})
    return blocks


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--month', default=None); a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, 'src/data/market/*.json')))
    month = a.month or os.path.basename(files[-1])[:-5]
    data = json.load(open(os.path.join(ROOT, 'src/data/market', month + '.json'), encoding='utf-8'))
    n = 0
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if 'market_spec' not in d: continue
        keep = [b for b in d['blocks'] if b.get('gen') != 'market']
        at = d['market_spec'].get('at', len(keep))  # number of hand-written blocks that come before the market section
        d['blocks'] = keep[:at] + build(d['market_spec'], data, month) + keep[at:]
        json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n'); n += 1
    print('updated', n, 'local files for', month)


if __name__ == '__main__':
    main()
