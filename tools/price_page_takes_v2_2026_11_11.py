#!/usr/bin/env python3
"""Second round of the price and bedroom page lines (D-229, Nov 11, 2026).

Jared's review (docs/review/price-page-takes-review-2026-11-11.xlsx) checked all 85 drafts: 10 right, 75 with a suggested line. Its
corrections are adopted as the recommended line: "under $X" pages quote the share of all sales under $X (not one slice), no "thin
slice", no city acreage figures on the over-$1.8M pages, no single build year averaged across areas years apart, White Rock as its own
city, no 55+ leasehold complex on a general page. For the 24 bedroom pages the review could not check the area medians and building
names because the sheet did not show them; they come from src/data/sold/sold-beds.json, so the data column now lists them and the
recommended line adds the cheapest and dearest area back (retirement and 55+ complexes excluded). Writes
docs/review/price-page-takes-v2-2026-11-11.csv. python3 -I tools/price_page_takes_v2_2026_11_11.py <review.xlsx>"""
import csv, json, os, re, sys
import openpyxl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
BEDS = json.load(open('src/data/sold/sold-beds.json'))['cities']
money = lambda v: '$' + f'{v / 1e6:.2f}'.rstrip('0').rstrip('.') + 'M' if v >= 1e6 else f'${round(v, -3) / 1e3:,.0f}K'
NAME = {'south-surrey': 'South Surrey', 'white-rock': 'White Rock', 'north-delta': 'North Delta', 'maple-ridge': 'Maple Ridge'}
SKIP_COMPLEX = re.compile(r'Retirement|Senior|55|Leasehold|Lifestyle Village', re.I)
OWN_WORDS = {'Homes for Sale Over $1.8M in South Surrey, BC', 'South Surrey Homes for Sale Under $1.8M', '2 Bedroom Townhomes for Sale in South Surrey',
             '2 Bedroom Condos for Sale in White Rock', 'Langley Luxury Homes Over $1.8M'}


def clean(n): return re.sub(r'\s+(Surrey|Langley)$', '', n.replace('Crescent Bch Ocean Pk.', 'Crescent Beach and Ocean Park').replace('Cloverdale BC', 'Cloverdale')) if n not in ('Fort Langley', 'Langley City') else n


def bed_detail(url):
    """Bedroom pages, round 2b (the second review): areas only when the listed areas cover 80%+ of sales; the cheapest and dearest area
    are always named, with "slightly" when close; the top building comes from the city-wide building list (a building split across
    two areas is counted once) and needs 5+ sales; the data column lists every area, the sales in smaller areas and every building
    with 3+ sales."""
    m = re.search(r'/([a-z-]+?)-(\d)-bedroom-(condos|townhomes)-for-sale\.html', url or '')
    if not m: return None
    city, n, t = m.group(1), m.group(2), {'condos': 'condo', 'townhomes': 'townhome'}[m.group(3)]
    g = BEDS.get(city, {}).get('groups', {}).get(t, {}).get(n) or {}
    sb = [s for s in (g.get('subs') or []) if s.get('n', 0) >= 5 and s.get('price')]
    covered = sum(s['n'] for s in sb); total = g.get('n') or 0
    cx = sorted(g.get('complexes') or [], key=lambda c: -c['n'])
    data = '; '.join(f'{clean(s["name"])}: {s["n"]} sales, median {money(s["price"])}' for s in sb)
    if total > covered: data += f'; smaller areas (under 5 sales each): {total - covered} sales'
    if cx: data += ' | Buildings with 3+ sales: ' + ', '.join(f'{c["name"]} {c["n"]}' for c in cx)
    area = ''
    if len(sb) >= 2 and total and covered / total >= 0.8:
        lo, hi = min(sb, key=lambda s: s['price']), max(sb, key=lambda s: s['price'])
        if hi['price'] - lo['price'] < 0.05 * lo['price']:
            area = f'By area, {clean(lo["name"])} was slightly less expensive (median {money(lo["price"])}) than {clean(hi["name"])} ({money(hi["price"])}).'
        else:
            area = f'By area, {clean(lo["name"])} was the least expensive (median {money(lo["price"])}) and {clean(hi["name"])} the most ({money(hi["price"])}).'
    bad = {c['name'].split()[0] for c in cx if SKIP_COMPLEX.search(c['name'])}
    ok = [c for c in cx if c['n'] >= 5 and not SKIP_COMPLEX.search(c['name']) and c['name'].split()[0] not in bad]
    bld = ''
    if ok:
        top = ok[0]['n']; best = [c['name'] for c in ok if c['n'] == top]
        bld = f'{best[0]} had the most sales ({top}).' if len(best) == 1 else f'{", ".join(best[:-1])} and {best[-1]} had the most sales ({top} each).'
    q = 'The area and building figures are from the bedroom sales data (column C). Change anything that does not match what you see on the ground.'
    if bad: q += f' Is {", ".join(sorted(c["name"] for c in cx if c["name"].split()[0] in bad and not SKIP_COMPLEX.search(c["name"])))} part of the 55+ complex? It is left out until you say.'
    return data, area, bld, q


def main():
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
    rows = list(wb['Review'].iter_rows(values_only=True))
    H = rows[0]; R = [dict(zip(H, r)) for r in rows[1:]]
    out = []
    for r in R:
        line = r['Draft'] if r['Recommendation'] == 'yes' else r['Suggested line']
        data = r['Sales data (12 months)'] or ''
        bd = bed_detail(r['Preview'])
        if bd:
            extra_data, area, bld, q = bd
            data = data + ' | By area: ' + extra_data
            sents = re.split(r'(?<=\.)\s+(?=[A-Z])', line)
            first = next((x for x in sents if 'median' in x), sents[0]); advice = sents[-1] if sents[-1] != first and 'had the most sales' not in sents[-1] else ''
            line = ' '.join(x for x in (first, area, bld, advice) if x)
            r['Question for Jared'] = q
        own = r['Page'] in OWN_WORDS
        out.append([r['Page'], r['Preview'], data, line, ('Please write this one in your own words. ' if own else '') + (r['Question for Jared'] or ''), '', ''])
    with open('docs/review/price-page-takes-v2-2026-11-11.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['Page', 'Preview', 'Sales data (12 months)', 'Recommended line', 'Question for you', 'Your line (leave blank to use the recommended line)', 'OK? (yes / no / skip)'])
        w.writerows(out)
    print('rows', len(out), '| own-words rows', sum(1 for o in out if o[4].startswith('Please write')))


if __name__ == '__main__': main()
