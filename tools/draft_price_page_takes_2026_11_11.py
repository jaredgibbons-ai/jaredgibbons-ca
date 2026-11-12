#!/usr/bin/env python3
"""Draft one-line takes for the 89 price-range and bedroom pages, for Jared to approve or rewrite (D-229, Nov 11, 2026).

These pages slice one city's sales, so data alone cannot make them unique; Jared's own line can. Each draft is built only from the
12-month sales layers (which neighbourhoods the budget fits, the typical age and lot there, the cheapest and dearest areas for a bedroom
count) plus a practical check that fits the stock. Nothing is published in his voice until he approves it in the sheet.
Writes docs/review/price-page-takes-for-jared-2026-11-11.csv. python3 -I tools/draft_price_page_takes_2026_11_11.py"""
import csv, glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SUB = json.load(open('src/data/sold/sold-12m.json'))['sub']
EX = json.load(open('src/data/sold/sold-extras.json'))['city']; S12 = json.load(open('src/data/sold/sold-12m.json'))['city']
BEDS = json.load(open('src/data/sold/sold-beds.json'))['cities']
NAME = {'south-surrey-white-rock': 'South Surrey and White Rock', 'north-delta': 'North Delta', 'maple-ridge': 'Maple Ridge', 'new-westminster': 'New Westminster',
        'port-coquitlam': 'Port Coquitlam', 'south-surrey': 'South Surrey', 'white-rock': 'White Rock'}
cname = lambda c: NAME.get(c, c.replace('-', ' ').title())
BOARDS = {'surrey': ['Surrey', 'North Surrey'], 'chilliwack': ['Chilliwack', 'Sardis'], 'north-delta': ['N. Delta'], 'burnaby': ['Burnaby North', 'Burnaby South', 'Burnaby East'],
          'vancouver': ['Vancouver West', 'Vancouver East'], 'south-surrey': ['South Surrey White Rock'], 'white-rock': ['South Surrey White Rock'], 'south-surrey-white-rock': ['South Surrey White Rock']}
TYPE = {'homes': 'house', 'condos': 'condo', 'townhomes': 'townhome'}
money = lambda v: '$' + f'{v / 1e6:.2f}'.rstrip('0').rstrip('.') + 'M' if v >= 1e6 else f'${round(v, -3) / 1e3:,.0f}K'
PREVIEW = 'https://jaredgibbons-ca.jaredgibbons.workers.dev/'


def clean(nm):
    nm = nm.replace('Crescent Bch Ocean Pk.', 'Crescent Beach and Ocean Park')
    return nm if nm in ('Fort Langley', 'Langley City') else re.sub(r'\s+(PM|MR|PC|BN|BS|BE|NW|NV|VW|VE|RI|CQ|PQ|LA|SR|AB|MI|CH|PI|Langley|Surrey)$', '', nm)


def subs(city, t, minn=5):
    bs = BOARDS.get(city, [cname(city)])
    return [(clean(k.split('|', 1)[1]), v['groups'][t]) for k, v in SUB.items() if k.split('|')[0] in bs and v['groups'].get(t, {}).get('n', 0) >= minn and v['groups'][t].get('p25')]


def names(xs): xs = list(xs); return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def tip(t, yb):
    if t == 'house': return 'Check the roof, windows and drainage before you fall for the new kitchen.' if yb and yb < 1990 else 'Compare lot size and parking: newer lots are smaller.'
    if t == 'condo': return 'In the older buildings, read the depreciation report and ask about special levies.' if yb and yb < 2000 else 'Compare strata fees, parking and storage between buildings, not just the unit.'
    return 'Look at the strata’s repair plan and how many parking spots come with the unit.'


EDGES = [0, 600000, 800000, 1000000, 1200000, 1500000, 1800000, float('inf')]   # the price bands in the sales layers (build_new_searches.BANDS)
SIBS = {}


def band(city, t, d, cap):
    """Each sibling page (same city and type, other prices) gets its own slice: under $1.2M looks at $1M-$1.2M when a $1M page exists."""
    C = cname(city); tp = {'house': 'houses', 'condo': 'condos', 'townhome': 'townhomes'}[t]; sb = subs(city, t)
    cg = (EX.get(city, {}).get('groups', {}).get(t) if t in ('house', 'condo') else None) or S12.get(city, {}).get('groups', {}).get(t) or {}
    bands, n = cg.get('bands') or [], cg.get('n') or 0
    share = lambda lo_, hi_: round(100 * sum(c for c, a_, b_ in zip(bands, EDGES, EDGES[1:]) if a_ >= lo_ and b_ <= hi_) / n) if bands and n and lo_ in EDGES and hi_ in EDGES else None
    if d == 'over':
        pct = share(cap, float('inf')); top = sorted([(nm, x) for nm, x in sb if x['p75'] >= cap], key=lambda z: -z[1]['price'])[:3]
        ac = S12.get(city, {}).get('groups', {}).get('acreage') if t == 'house' else None
        line = (f'About {pct}% of {C} {tp} sold for {money(cap)} or more last year' if pct is not None else f'Over {money(cap)} is a small part of the {C} market')
        line += (f', mostly in {names(nm for nm, _ in top)}.' if top else '.')
        if ac and ac.get('n', 0) >= 5: line += f' At this price, acreage is part of the picture: {ac["n"]} acreages sold at a median of {money(ac["price"])}.'
        line += ' Ask what the land and zoning allow before you pay for the view.'
        return line, (f'{pct}% of {n} sales at {money(cap)}+; ' if pct is not None else '') + '; '.join(f'{nm}: median {money(x["price"])}, top quarter from {money(x["p75"])}' for nm, x in top)
    lo = max([c for c in SIBS.get((city, t), []) if c < cap], default=0)
    pct = share(lo, cap)
    inslice = sorted([(nm, x) for nm, x in sb if lo < x['price'] <= cap], key=lambda z: -z[1]['n'])[:3]
    cheaper = sorted([(nm, x) for nm, x in sb if x['p25'] <= cap < x['price']], key=lambda z: -z[1]['n'])[:2] if not inslice else []
    rng = f'between {money(lo)} and {money(cap)}' if lo else f'under {money(cap)}'
    R = rng[0].upper() + rng[1:]
    line = f'About {pct}% of {C} {tp} sold {rng} last year. ' if pct is not None else ''
    if inslice:
        yb = round(sum(x.get('yb') or 0 for _, x in inslice) / len(inslice)) if all(x.get('yb') for _, x in inslice) else None
        line += (f'That’s a typical {t}' if line else f'{R}, you’re looking at a typical {t}') + f' in {names(nm for nm, _ in inslice)}' + (f', usually built around {yb}' if yb else '') + '.'
    elif cheaper:
        yb = cheaper[0][1].get('yb')
        line += (f'At this price you’re shopping' if line else f'{R}, you’re shopping') + f' the cheaper end of {names(nm for nm, _ in cheaper)}.'
    else:
        yb = cg.get('yb'); cheap = min(sb, key=lambda z: z[1]['price'])[0] if sb else C
        line += f'{R} is a thin slice in {C}: most buyers widen to townhomes or start in {cheap}.'
    line += ' ' + tip(t, yb)
    facts = (f'{pct}% of {n} sales {rng}; ' if pct is not None else '') + '; '.join(f'{nm}: median {money(x["price"])}, middle half {money(x["p25"])}–{money(x["p75"])}, built {x.get("yb", "?")}' for nm, x in (inslice or cheaper))
    return line, facts


def beds(city, n, t):
    g = BEDS.get(city, {}).get('groups', {}).get(t, {}).get(n)
    C = cname(city)
    if not g: return ('', 'no data')
    sb = [s for s in (g.get('subs') or []) if s.get('n', 0) >= 5 and s.get('price')]
    cx = [c for s in sb for c in (s.get('top') or [])]
    busiest = max(cx, key=lambda c: c['n']) if cx else None
    if len(sb) >= 2:
        lo, hi = min(sb, key=lambda s: s['price']), max(sb, key=lambda s: s['price'])
        lo, hi = {**lo, 'name': clean(lo['name'])}, {**hi, 'name': clean(hi['name'])}
        if hi['price'] - lo['price'] < 0.05 * lo['price']:
            line = f'For a {n}-bedroom {t} in {C}, prices are close across {lo["name"]} and {hi["name"]} (medians {money(lo["price"])} and {money(hi["price"])}), so the building matters more than the area.'
        else:
            line = f'For a {n}-bedroom {t} in {C}, {lo["name"]} is where the value is (median {money(lo["price"])}); {hi["name"]} costs the most ({money(hi["price"])}).'
    else:
        line = f'A {n}-bedroom {t} in {C} sold for a median of {money(g["price"])} over the past year.'
    if busiest: line += f' {busiest["name"]} had the most sales.'
    line += ' ' + tip(t, g.get('yb'))
    return (line, f'{g["n"]} sales, median {money(g["price"])}, middle half {money(g["p25"])}–{money(g["p75"])}, {g.get("sqft", "?")} sq ft, built {g.get("yb", "?")}' + (f', strata ${g["maint"]}/mo' if g.get('maint') else ''))


def main():
    rows = []
    for f in glob.glob('src/data/local/*.json'):
        m = re.match(r'^([a-z-]+?)-(homes|condos|townhomes)-under-(\d+)(?:-(\d))?([mk])$', os.path.basename(f)[:-5])
        if m: SIBS.setdefault((m.group(1), TYPE[m.group(2)]), []).append(int(m.group(3)) * (10 ** 6 if m.group(5) == 'm' else 1000) + (int(m.group(4)) * 100000 if m.group(4) else 0))
    for f in sorted(glob.glob('src/data/local/*.json')):
        s = os.path.basename(f)[:-5]
        m = re.match(r'^([a-z-]+?)-(homes|condos|townhomes)-(under|over)-(\d+)(?:-(\d))?([mk])$', s)
        mb = re.match(r'^([a-z-]+?)-(\d)-bedroom-(condos|townhomes)-for-sale$', s)
        if m:
            cap = int(m.group(4)) * (10 ** 6 if m.group(6) == 'm' else 1000) + (int(m.group(5)) * 100000 if m.group(5) else 0)
            draft, facts = band(m.group(1), TYPE[m.group(2)], m.group(3), cap)
        elif mb: draft, facts = beds(mb.group(1), mb.group(2), TYPE[mb.group(3)])
        else: continue
        pf = f'src/data/pages/{s}.json'
        title = (json.load(open(f)).get('new_page') or {}).get('h1') or (re.sub(r'\s*\|.*$', '', json.load(open(pf)).get('title', '')) if os.path.exists(pf) else s)
        rows.append([title, PREVIEW + s + '.html', facts, draft, '', ''])
    os.makedirs('docs/review', exist_ok=True)
    with open('docs/review/price-page-takes-for-jared-2026-11-11.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['Page', 'Preview', 'What the sales data says (12 months)', 'Draft line (in your voice)', 'Your line (leave blank if the draft is right)', 'OK? (yes / no / skip)'])
        w.writerows(rows)
    print('rows', len(rows), '| empty drafts', sum(1 for r in rows if not r[3]))


if __name__ == '__main__': main()
