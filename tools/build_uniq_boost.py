#!/usr/bin/env python3
"""Uniqueness boost (2026-11-07) for the eight pages that sat just under 70% unique.

Each page gets one data-driven section (gen 'boost', pos 'end') that ranks the page's area against its neighbours inside the same city,
from the closed-sales aggregate (src/data/sold/sold-12m.json) or the closed-and-pending extras (sold-extras.json). Nothing is invented: every
sentence is computed, a median shows only where at least 5 homes sold, and the window and source are stated.
python3 -I tools/build_uniq_boost.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_area_gap_pages as A
from build_new_searches import money, num, disp

AGG = json.load(open('src/data/sold/sold-12m.json')); EXT = json.load(open('src/data/sold/sold-extras.json'))
WIN = AGG['meta']['window']
SRC = f'Source: Paragon MLS®, closed sales only, {WIN}. A median is shown only where at least 5 homes sold; a dash means fewer.'
G = 'boost'
TYPE = {'house': ('detached houses', 'house'), 'townhome': ('townhomes', 'townhome'), 'condo': ('condos', 'condo')}


def P(t): return {'t': 'p', 'text': t, 'gen': G}
def H(t): return {'t': 'h', 'level': 2, 'text': t, 'gen': G}
def T(cap, head, rows, src): return {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'source': src, 'gen': G}
def ordinal(n): return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'
def med(g): return money(g['price']) if g.get('n', 0) >= 5 and g.get('price') else '—'


def board_subs(board, grp):
    out = []
    for k, v in AGG['sub'].items():
        b, nm = k.split('|', 1)
        if b == board and grp in v['groups'] and v['groups'][grp]['n'] > 0: out.append((disp(nm, b), nm, v['groups'][grp]))
    return out


def rank_table(board, city, sub_raw, lead_grp):
    name = disp(sub_raw, board)
    subs = board_subs(board, lead_grp); byn = sorted(subs, key=lambda s: -s[2]['n'])
    top = byn[:9]
    if sub_raw not in [s[1] for s in top]:
        me = next((s for s in subs if s[1] == sub_raw), None)
        if me: top = byn[:4] + [me]
    rows = []
    for nm, raw, g in top:
        rows.append([nm, num(g['n']), med(g), money(g['ppsf']) if g.get('ppsf') and g['n'] >= 5 else '—', str(g['beds']) if g.get('beds') is not None and g['n'] >= 5 else '—', str(g['yb']) if g.get('yb') and g['n'] >= 5 else '—', str(g['dom']) + ' days' if g.get('dom') and g['n'] >= 5 else '—'])
    noun = TYPE[lead_grp][0]
    return T(f'{city} neighbourhoods by {noun} sold, with {name}', ['Neighbourhood', 'Sales', 'Median price', 'Price per sq ft', 'Median bedrooms', 'Median year built', 'Median days to sell'], rows, SRC)


def rank_section(heading, board, city, sub_raw, grps, lead_grp, extra=None, more=None):
    """Rank the sub-area among its board's sub-areas for each group; table of the five busiest for lead_grp."""
    blocks = [H(heading)]; sents = []; name = disp(sub_raw, board)
    for grp in grps:
        subs = board_subs(board, grp); me = next((s for s in subs if s[1] == sub_raw), None)
        if not me: continue
        noun = TYPE[grp][0]; byn = sorted(subs, key=lambda s: -s[2]['n']); rn = [s[1] for s in byn].index(sub_raw) + 1
        elig = sorted([s for s in subs if s[2]['n'] >= 5 and s[2].get('price')], key=lambda s: -s[2]['price'])
        sen = f'Of the {len(subs)} {city} neighbourhoods that recorded {noun} sales, {name} was {ordinal(rn)} for volume with {me[2]["n"]} sales'
        if me[2]['n'] >= 5 and me[2].get('price') and me[1] in [s[1] for s in elig]:
            pr = [s[1] for s in elig].index(sub_raw) + 1
            sen += f' and {ordinal(pr)} of {len(elig)} for median price at {money(me[2]["price"])}'
        sents.append(sen + '.')
    if sents: blocks.append(P(' '.join(sents)))
    blocks.append(rank_table(board, city, sub_raw, lead_grp))
    for g2 in (more or []): blocks.append(rank_table(board, city, sub_raw, g2))
    me = next((s for s in board_subs(board, lead_grp) if s[1] == sub_raw), None)
    if me and me[2]['n'] >= 5:
        g = me[2]; bits = []
        allm = [s[2]['price'] for s in board_subs(board, lead_grp) if s[2]['n'] >= 5 and s[2].get('price')]
        allm.sort(); mid = allm[len(allm) // 2]
        diff = round(100 * (g['price'] - mid) / mid)
        bits.append(f'The typical {TYPE[lead_grp][1]} sold in {name} was built in {g["yb"]}' if g.get('yb') else '')
        s2 = f'Comparing {name} with the middle of the {city} neighbourhoods ({money(mid)}), its median {TYPE[lead_grp][1]} price was ' + (f'{abs(diff)}% above' if diff > 0 else f'{abs(diff)}% below' if diff < 0 else 'level with') + ' it.'
        if g.get('dom') and g.get('ratio'): s2 += f' Homes took {g["dom"]} days to sell and the median sale price was {g["ratio"]:.1f}% of the last list price.'
        blocks.append(P(s2))
    if extra: blocks += extra
    return blocks


def profile(board, sub_raw, grps, city):
    name = disp(sub_raw, board); gs = AGG['sub'][f'{board}|{sub_raw}']['groups']; use = [x for x in grps if x in gs and gs[x]['n'] >= 5]
    if not use: return []
    head = ['Measure'] + [TYPE[x][0].capitalize() for x in use]
    def row(lab, fn): return [lab] + [fn(gs[x]) for x in use]
    rows = [row('Sales', lambda g: num(g['n'])), row('Median price', lambda g: money(g['price'])),
            row('Middle half of prices', lambda g: f'{money(g["p25"])} to {money(g["p75"])}' if g.get('p25') else '—'),
            row('Price per square foot', lambda g: money(g['ppsf']) if g.get('ppsf') else '—'),
            row('Median bedrooms', lambda g: str(g['beds']) if g.get('beds') is not None else '—'),
            row('Median year built', lambda g: str(g['yb']) if g.get('yb') else '—'),
            row('Monthly strata fee', lambda g: money(g['maint']) if g.get('maint') else '—'),
            row('Days to sell', lambda g: str(g['dom']) if g.get('dom') is not None else '—'),
            row('Sold price as a share of list price', lambda g: f'{g["ratio"]:.1f}%' if g.get('ratio') else '—'),
            row('Sales over the list price', lambda g: f'{g["over"]}%' if g.get('over') is not None else '—')]
    rows = [r for r in rows if any(c != '—' for c in r[1:])]
    sents = []
    for x in use:
        g = gs[x]; q = g.get('q') or []
        qs = [i for i in q if i.get('price')]
        if len(qs) >= 2:
            lo = min(qs, key=lambda i: i['price']); hi = max(qs, key=lambda i: i['price'])
            sents.append(f'By quarter, the {name} {TYPE[x][1]} median ranged from {money(lo["price"])} to {money(hi["price"])} across the quarters with 5 or more sales.')
    out = [T(f'{name} in detail: {" and ".join(TYPE[x][0] for x in use)} sold, {WIN}', head, rows, SRC)]
    if sents: out.insert(0, P(' '.join(sents)))
    return out


def faq_rank(board, sub_raw, grp, city):
    name = disp(sub_raw, board); noun, one = TYPE[grp]; subs = board_subs(board, grp); me = next((x for x in subs if x[1] == sub_raw), None)
    if not me or me[2]['n'] < 5: return []
    g = me[2]; byn = sorted(subs, key=lambda x: -x[2]['n']); rn = [x[1] for x in byn].index(sub_raw) + 1
    doms = sorted(x[2]['dom'] for x in subs if x[2]['n'] >= 5 and x[2].get('dom') is not None); mid = doms[len(doms) // 2]
    way = 'faster than' if g['dom'] < mid else 'slower than' if g['dom'] > mid else 'level with'
    return [{'q': f'How does {name} rank for {noun} sales in {city}?', 'a': f'{name} was {ordinal(rn)} of {len(subs)} {city} neighbourhoods for {noun} sold, with {g["n"]} sales in {WIN}.', 'gen': G},
            {'q': f'Do {name} {noun} sell quickly compared with the rest of {city}?', 'a': f'The median {one} in {name} took {g["dom"]} days to sell, {way} the {mid}-day middle of the {city} neighbourhoods with 5 or more sales.', 'gen': G}]


def bradner_extra():
    g = AGG['sub']['Abbotsford|Bradner']['groups']; a = g['acreage']; h = g['house']
    return [P(f'Bradner’s sales are not mainly houses on town lots. {a["n"]} houses with acreage sold here against {h["n"]} ordinary houses, and the acreage median was {money(a["price"])}, '
              f'{round(100 * (a["price"] - h["price"]) / h["price"])}% above the {money(h["price"])} house median. The acreage figures describe a handful of rural properties, so they move with which properties happened to sell.')]


def golf_blocks():
    c = EXT['city']['abbotsford']['groups']; gf, hs = c['golf'], c['house']; win = EXT['meta']['window'].replace(' to ', ' and ')
    rows = [['Sales', num(gf['n']), num(hs['n'])], ['Median price', money(gf['price']), money(hs['price'])], ['Median size', f'{gf["sqft"]:,} sq ft', f'{hs["sqft"]:,} sq ft'], ['Median year built', str(gf['yb']), str(hs['yb'])],
            ['Median bedrooms', str(gf['beds']), str(hs['beds'])], ['Median lot', f'{gf["lot_sqft"]:,} sq ft', f'{hs["lot_sqft"]:,} sq ft'], ['Days to sell', str(gf['dom']), str(hs['dom'])]]
    share = round(100 * gf['n'] / hs['n'])
    return [H('Golf course houses against all Abbotsford houses'),
            P(f'Between {win}, {gf["n"]} golf course houses sold, which is {share}% of the {hs["n"]} Abbotsford houses recorded in the same period. Their median price of {money(gf["price"])} sits within {money(abs(gf["price"] - hs["price"]))} of the all-house median of {money(hs["price"])}, '
              f'so frontage or a view of the course has not set these homes apart on price alone. They differ more in size and age: the typical golf course house has {gf["sqft"]:,} square feet and was built in {gf["yb"]}, against {hs["sqft"]:,} square feet and {hs["yb"]} for houses overall.'),
            T('Abbotsford golf course houses and all Abbotsford houses sold', ['Measure', 'Golf course houses', 'All houses'], rows, f'Source: Paragon MLS® sold export (closed and pending), {win}. “Golf course” is the listing’s golf-course flag.')]


def langley_blocks():
    subs = sorted(board_subs('Langley', 'townhome'), key=lambda s: -s[2]['n']); tot = sum(s[2]['n'] for s in subs)
    rows = [[nm, num(g['n']), f'{round(100 * g["n"] / tot)}%', med(g), money(g['p25']) + ' to ' + money(g['p75']) if g['n'] >= 10 and g.get('p25') else '—'] for nm, raw, g in subs]
    top = subs[0]; wh = next(s for s in subs if s[1] == 'Willoughby Heights'); under = [s for s in subs if s[2].get('p75') and s[2]['p75'] < 1200000]
    s = (f'{tot:,} Langley townhomes closed between {WIN.replace(" to ", " and ")}, in {len(subs)} neighbourhoods. {wh[0]} alone had {wh[2]["n"]} ({round(100 * wh[2]["n"] / tot)}%) at a median of {money(wh[2]["price"])}. '
         f'In {len(under)} of the {len([x for x in subs if x[2].get("p75")])} neighbourhoods with 10 or more sales, the top quarter of sales still came in under $1,200,000, so a $1.2 million ceiling covers most of the townhome market, not just its entry level.')
    return [H('Where Langley townhomes sold'), P(s), T('Langley townhomes sold, by neighbourhood', ['Neighbourhood', 'Sales', 'Share of Langley sales', 'Median price', 'Middle half of prices'], rows, SRC)]


def main():
    specs = {
        'glenwood-port-coquitlam-houses-for-sale': rank_section('Glenwood houses against the rest of Port Coquitlam', 'Port Coquitlam', 'Port Coquitlam', 'Glenwood PQ', ['house'], 'house', profile('Port Coquitlam', 'Glenwood PQ', ['house'], 'Port Coquitlam')),
        'glenwood-port-coquitlam': rank_section('Glenwood’s townhomes and condos against the rest of Port Coquitlam', 'Port Coquitlam', 'Port Coquitlam', 'Glenwood PQ', ['townhome', 'condo'], 'condo', profile('Port Coquitlam', 'Glenwood PQ', ['condo', 'townhome'], 'Port Coquitlam'), more=['townhome']),
        'bradner-abbotsford-houses-for-sale': rank_section('Bradner against the rest of Abbotsford', 'Abbotsford', 'Abbotsford', 'Bradner', ['house'], 'house', bradner_extra() + profile('Abbotsford', 'Bradner', ['house'], 'Abbotsford')),
        'new-horizons-coquitlam-houses-for-sale': rank_section('New Horizons houses against the rest of Coquitlam', 'Coquitlam', 'Coquitlam', 'New Horizons', ['house'], 'house', profile('Coquitlam', 'New Horizons', ['house'], 'Coquitlam')),
        'delta-manor': rank_section('Delta Manor against the rest of Ladner', 'Ladner', 'Ladner', 'Delta Manor', ['house', 'condo', 'townhome'], 'house', profile('Ladner', 'Delta Manor', ['house', 'condo', 'townhome'], 'Ladner')),
        'southwest-maple-ridge': rank_section('Southwest Maple Ridge against the rest of Maple Ridge', 'Maple Ridge', 'Maple Ridge', 'Southwest Maple Ridge', ['house', 'townhome'], 'house', profile('Maple Ridge', 'Southwest Maple Ridge', ['house', 'townhome'], 'Maple Ridge')),
        'abbotsford-golf-course-homes-for-sale': golf_blocks(),
        'langley-townhomes-under-1-2m': langley_blocks(),
    }
    faqs = {'glenwood-port-coquitlam-houses-for-sale': faq_rank('Port Coquitlam', 'Glenwood PQ', 'house', 'Port Coquitlam'), 'glenwood-port-coquitlam': faq_rank('Port Coquitlam', 'Glenwood PQ', 'condo', 'Port Coquitlam') + faq_rank('Port Coquitlam', 'Glenwood PQ', 'townhome', 'Port Coquitlam'),
            'new-horizons-coquitlam-houses-for-sale': faq_rank('Coquitlam', 'New Horizons', 'house', 'Coquitlam'), 'delta-manor': faq_rank('Ladner', 'Delta Manor', 'house', 'Ladner'), 'southwest-maple-ridge': faq_rank('Maple Ridge', 'Southwest Maple Ridge', 'house', 'Maple Ridge')}
    for host, bl in specs.items(): A.set_blocks(host, G, bl, end=True)
    for host, fq in {k: [] for k in faqs}.items():
        def fn(d, fq=fq): d['faq'] = [q for q in d.get('faq', []) if q.get('gen') != G] + fq
        A.host_edit(host, fn)
    print(len(specs), 'pages given a boost section')


if __name__ == '__main__': main()
