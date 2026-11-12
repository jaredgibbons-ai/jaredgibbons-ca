#!/usr/bin/env python3
"""Local snapshot on price-range, bedroom, new-listing and market-stats pages (D-228, Nov 11, 2026).

These generated pages were the ones still under 0.76 unique when the built pages are measured (tools/uniqueness_rendered.py): their
tables and sentences share wording with their sibling pages. Each now gets a short "at a glance" section only it can have, from the
12-month sales layers already on the site (Paragon closed and pending sales, Nov 1, 2025 to Oct 31, 2026: src/data/sold/sold-extras.json,
sold-12m.json, sold-beds.json): on price-range pages, what the page's budget buys at the city's median price per square foot and which
neighbourhoods it fits; on bedroom pages, the middle half, size, strata fee, building age, quarters and pace for that bedroom count; on
new-listing pages, the fastest- and slowest-selling neighbourhoods; on market-stats pages, the city medians and quarters. Nothing is estimated; a figure needs 5 sales.
Idempotent (replaces its own blocks, gen 'snap'). python3 -I tools/build_local_snapshots_2026_11_11.py"""
import csv, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
EX = json.load(open('src/data/sold/sold-extras.json'))['city']
S12 = json.load(open('src/data/sold/sold-12m.json'))['city']
BEDS = json.load(open('src/data/sold/sold-beds.json'))['cities']
SUB = json.load(open('src/data/sold/sold-12m.json'))['sub']
BOARDS = {'surrey': ['Surrey', 'North Surrey'], 'chilliwack': ['Chilliwack', 'Sardis'], 'north-delta': ['N. Delta'], 'burnaby': ['Burnaby North', 'Burnaby South', 'Burnaby East'],
          'vancouver': ['Vancouver West', 'Vancouver East'], 'south-surrey-white-rock': ['South Surrey White Rock'], 'south-surrey': ['South Surrey White Rock'],
          'white-rock': ['South Surrey White Rock']}
def subs(city, t, minn=5):
    bs = BOARDS.get(city, [cname(city)])
    out = []
    for k, v in SUB.items():
        b, nm = k.split('|', 1)
        g = v['groups'].get(t)
        if b in bs and g and g.get('n', 0) >= minn and g.get('p25') and g.get('p75'): out.append((nm if nm in ('Fort Langley', 'Langley City') else re.sub(r'\s+(PM|MR|PC|BN|BS|BE|NW|NV|VW|VE|RI|CQ|PQ|LA|SR|AB|MI|CH|PI|Langley|Surrey)$', '', nm), g))
    return out
def names(xs):
    xs = list(xs); return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]
NAME = {'south-surrey-white-rock': 'South Surrey and White Rock', 'north-delta': 'North Delta', 'maple-ridge': 'Maple Ridge', 'new-westminster': 'New Westminster',
        'port-coquitlam': 'Port Coquitlam', 'port-moody': 'Port Moody', 'south-surrey': 'South Surrey', 'white-rock': 'White Rock', 'pitt-meadows': 'Pitt Meadows',
        'north-vancouver': 'North Vancouver'}
cname = lambda c: NAME.get(c, c.replace('-', ' ').title())
TYPE = {'homes': 'house', 'houses': 'house', 'condos': 'condo', 'townhomes': 'townhome'}
PLUR = {'house': 'houses', 'condo': 'condos', 'townhome': 'townhomes'}
money = lambda v: '$' + f'{v / 1e6:.2f}'.rstrip('0').rstrip('.') + 'M' if v >= 1e6 else f'${v:,.0f}'


def group(city, t):
    g = (EX.get(city, {}).get('groups', {}).get(t) if t in ('house', 'condo') else None) or S12.get(city, {}).get('groups', {}).get(t)
    return g if g and g.get('n', 0) >= 5 else None


def cap_of(s):
    m = re.match(r'^(\d+)(?:-(\d))?m$', s)
    if m: return int(m.group(1)) * 1_000_000 + (int(m.group(2)) * 100_000 if m.group(2) else 0)
    m = re.match(r'^(\d+)k$', s); return int(m.group(1)) * 1000 if m else None


def quarter_line(g, noun):
    q = g.get('q') or []
    if len(q) != 4 or any((x.get('n') or 0) < 5 or not x.get('price') for x in q): return ''
    a, b = q[0]['price'], q[3]['price']; ch = (b - a) / a * 100
    word = 'held near' if abs(ch) < 1.5 else ('rose from' if ch > 0 else 'eased from')
    mid = f'{money(a)}' if word == 'held near' else f'{money(a)} to {money(b)}'
    return f'Quarter by quarter, the median {noun} price {word} {mid} between November–January and August–October ({q[0]["n"]} and {q[3]["n"]} sales).'


def pace_line(g):
    if not all(k in g for k in ('dom', 'ratio', 'over')): return ''
    return f'Half sold within {g["dom"]} days, at a median {g["ratio"]}% of the last list price, and {g["over"]}% went for more than list.'


def typical(g, t):
    bits = []
    if g.get('yb'): bits.append(f'built in {g["yb"]}')
    if g.get('beds'): bits.append(f'{g["beds"]} bedrooms')
    if t == 'house' and g.get('lot_sqft'): bits.append(f'a {g["lot_sqft"]:,} sq ft lot')
    if g.get('sqft'): bits.append(f'{g["sqft"]:,} sq ft of living space')
    if t != 'house' and g.get('maint'): bits.append(f'a ${g["maint"]:,} monthly strata fee')
    if not bits: return ''
    return f'The typical {t} that sold was {bits[0]}' + (', with ' + ', '.join(bits[1:-1]) + (' and ' if len(bits) > 2 else '') + bits[-1] if len(bits) > 1 else '') + '.'


def band_blocks(city, t, d, cap):
    """Only what depends on this page's price: the floor area it buys and the neighbourhoods it fits (sibling pages for other prices
    in the same city get different lines, so the snapshot never repeats between them)."""
    g = group(city, t)
    if not g: return None
    C = cname(city); tp = PLUR[t]; out = []
    if g.get('ppsf'):
        out.append(f'At {C}’s median of ${g["ppsf"]:,} a square foot, {money(cap)} {"buys" if d == "under" else "is"} about {round(cap / g["ppsf"], -1):,.0f} sq ft of {t}.')
    sb = subs(city, t)
    if d == 'under':
        most = sorted([(nm, x) for nm, x in sb if x['p75'] <= cap], key=lambda z: -z[1]['n'])[:4]
        mid = sorted([(nm, x) for nm, x in sb if x['p25'] <= cap < x['p75']], key=lambda z: -z[1]['n'])[:4]
        if most: out.append(f'Three quarters or more of the {tp} that sold in {names(n for n, _ in most)} went for {money(cap)} or less (' + '; '.join(f'{n}: {x["n"]} sales, median {money(x["price"])}' for n, x in most) + ').')
        if mid: out.append(f'In {names(n for n, _ in mid)}, {money(cap)} sits inside the middle half of sales, so it buys an ordinary {t} there rather than the cheapest one (' + '; '.join(f'{n}: {money(x["p25"])} to {money(x["p75"])}' for n, x in mid) + ').')
        if not most and not mid: out.append(f'No {C} neighbourhood had a quarter of its {tp} sell for {money(cap)} or less in the past year.')
    else:
        above = sorted([(nm, x) for nm, x in sb if x['p25'] >= cap], key=lambda z: -z[1]['n'])[:4]
        mid = sorted([(nm, x) for nm, x in sb if x['p25'] < cap <= x['p75']], key=lambda z: -z[1]['n'])[:4]
        if above: out.append(f'In {names(n for n, _ in above)}, three quarters or more of the {tp} that sold went for {money(cap)} or more (' + '; '.join(f'{n}: median {money(x["price"])}' for n, x in above) + ').')
        if mid: out.append(f'In {names(n for n, _ in mid)}, the top quarter of sales passed {money(cap)} (' + '; '.join(f'{n}: {money(x["p25"])} to {money(x["p75"])}' for n, x in mid) + ').')
    return f'Where {money(cap)} fits in {C}', [x for x in out if x]


def bed_blocks(city, n, t):
    g = BEDS.get(city, {}).get('groups', {}).get(t, {}).get(n)
    if not g or g.get('n', 0) < 5: return None
    C = cname(city); lab = f'{n}-bedroom {t}'
    out = [f'{g["n"]} {lab}s sold in {C} over the past year; the middle half went for {money(g["p25"])} to {money(g["p75"])}.']
    if g.get('sqft') and g.get('ppsf'): out.append(f'The median {lab} had {g["sqft"]:,} sq ft, about ${g["ppsf"]:,} a square foot' + (f', with a ${g["maint"]:,} monthly strata fee.' if g.get('maint') else '.'))
    age = [a for a in (g.get('age') or []) if a.get('n', 0) >= 5 and a.get('price')]
    if len(age) >= 2:
        lo, hi = min(age, key=lambda a: a['price']), max(age, key=lambda a: a['price'])
        out.append(f'By building age, the median ran from {money(lo["price"])} ({lo["label"].lower()}) to {money(hi["price"])} ({hi["label"].lower()}).')
    out += [quarter_line(g, lab), pace_line(g)]
    return f'{C} {lab}s at a glance', [x for x in out if x]


def fast_blocks(city):
    """New-listing pages: where homes sold fastest and slowest, by neighbourhood (the market-stats page for the city carries the city medians)."""
    C = cname(city); rows = []
    for t in ('house', 'condo', 'townhome'):
        for nm, x in subs(city, t, 10):
            if x.get('dom') is not None: rows.append((x['dom'], nm, PLUR[t], x['n']))
    if len(rows) < 4: return None
    rows.sort()
    fast = ', '.join(f'{nm} {tp} ({d} days, {n} sales)' for d, nm, tp, n in rows[:3]); slow = ', '.join(f'{nm} {tp} ({d} days)' for d, nm, tp, n in rows[-3:][::-1])
    return f'How fast new {C} listings sell', [f'A new listing’s first days matter most where homes sell quickly. Over the past year the fastest-selling {C} groups (median days to sell, at least 10 sales) were {fast}. The slowest were {slow}.']


def city_blocks(city):
    C = cname(city); h, c = group(city, 'house'), group(city, 'condo')
    if not h and not c: return None
    out = []
    if h: out.append(f'Over the past year, {h["n"]:,} {C} houses sold at a median of {money(h["price"])} (middle half {money(h["p25"])} to {money(h["p75"])}), half of them within {h["dom"]} days.')
    if c: out.append(f'{c["n"]:,} condos sold at a median of {money(c["price"])} (middle half {money(c["p25"])} to {money(c["p75"])}), half within {c["dom"]} days.')
    if h: out.append(quarter_line(h, 'house'))
    return f'{C} sales at a glance, past 12 months', [x for x in out if x]


BAND_AND_BEDS = False   # D-228: tried on price-range and bedroom pages; their sibling pages share the same city data, so the lines
                        # repeated between siblings and lowered uniqueness (−0.013 and −0.008 on average). Kept off; blocks are removed there.


def plan(slug):
    if not BAND_AND_BEDS and (re.search(r'-(under|over)-\d', slug) or re.search(r'-\d-bedroom-', slug)): return 'drop'
    m = re.match(r'^([a-z-]+?)-(homes|condos|townhomes)-(under|over)-(\d+(?:-\d)?[mk])$', slug)
    if m and cap_of(m.group(4)): return band_blocks(m.group(1), TYPE[m.group(2)], m.group(3), cap_of(m.group(4)))
    m = re.match(r'^([a-z-]+?)-(\d)-bedroom-(condos|townhomes)-for-sale$', slug)
    if m: return bed_blocks(m.group(1), m.group(2), TYPE[m.group(3)])
    m = re.match(r'^new-listings-this-week-([a-z-]+)$', slug)
    if m: return fast_blocks(m.group(1))
    m = re.match(r'^([a-z-]+?)-real-estate-market-stats$', slug)
    if m: return city_blocks(m.group(1))
    return None


def main():
    made = skipped = 0
    for f in sorted(os.listdir('src/data/local')):
        slug = f[:-5]; p = plan(slug)
        if p is None: continue
        if p == 'drop':
            lf = f'src/data/local/{f}'; raw = open(lf).read(); l = json.loads(raw)
            if any(b.get('gen') == 'snap' for b in l.get('blocks', [])):
                l['blocks'] = [b for b in l['blocks'] if b.get('gen') != 'snap']
                ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
                open(lf, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
            continue
        if not p: skipped += 1; continue
        head, lines = p
        lf = f'src/data/local/{f}'; raw = open(lf).read(); l = json.loads(raw)
        bl = [b for b in l.get('blocks', []) if b.get('gen') != 'snap']
        new = [{'t': 'h', 'level': 2, 'text': head, 'gen': 'snap'}, {'t': 'p', 'gen': 'snap', 'text': ' '.join(lines)},
               {'t': 'p', 'gen': 'snap', 'parts': [{'t': 'Source: Paragon closed and pending sales, November 1, 2025 to October 31, 2026 ('}, {'t': 'how these figures work', 'h': '/data-and-methodology.html'}, {'t': ').'}], 'cls': 'muted'}]
        at = next((i for i, b in enumerate(bl) if b.get('t') == 'h' and re.match(r'^More .+ (real estate|homes|pages)', b.get('text', ''))), None)
        if at is None: at = next((i for i, b in enumerate(bl) if b.get('t') == 'h' and b.get('level') == 2 and i > 2), len(bl))
        bl[at:at] = new; l['blocks'] = bl
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(lf, 'w').write((json.dumps(l, ensure_ascii=False, indent=ind) if ind else json.dumps(l, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
        made += 1
    print('pages with a snapshot:', made, '| no data for:', skipped)


if __name__ == '__main__': main()
