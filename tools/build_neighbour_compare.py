#!/usr/bin/env python3
"""'How X compares with nearby areas' block (gen 'ncmp') for pages that are still close to the 70% line.

Nearest neighbourhoods come from src/data/area-coordinates.csv (same precise-points rule as build_area_near.py); their prices come from the Paragon
closed-sales aggregate (src/data/sold/sold-12m.json). A neighbour is listed only with 5 or more sales of the type. Numbers are the page's own, so no
other page repeats them. Re-runnable.   python3 -I tools/build_neighbour_compare.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_area_near as N
ROOT = N.ROOT; G = 'ncmp'
SD = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))
SUB = SD['sub']; WINDOW = SD['meta']['window']
# For the two Burnaby pages the neighbours are the areas each page itself names as neighbours or landmarks (no precise centre point exists for Sperling-Duthie).
FIXED = {
    'burnaby-hospital-condos-townhomes-for-sale': ['Burnaby South|Deer Lake', 'Burnaby South|Burnaby Lake', 'Burnaby South|Forest Glen BS', 'Burnaby South|Metrotown', 'Burnaby North|Sperling-Duthie', 'Burnaby South|Buckingham Heights'],
    'sperling-duthie-burnaby-houses-for-sale': ['Burnaby South|Deer Lake', 'Burnaby South|Buckingham Heights', 'Burnaby South|Burnaby Lake', 'Burnaby South|Burnaby Hospital', 'Burnaby South|Forest Glen BS', 'Burnaby South|Metrotown'],
}
TARGETS = {  # page slug -> (centre name in the coordinates file, sold key, [(group, label)])
    'burnaby-hospital-condos-townhomes-for-sale': ('burnaby-hospital', 'Burnaby South|Burnaby Hospital', [('condo', 'condos'), ('townhome', 'townhomes')]),
    'sperling-duthie-burnaby-houses-for-sale': ('sperling-duthie', 'Burnaby North|Sperling-Duthie', [('house', 'houses'), ('duplex', 'duplexes')]),
    'websters-corners': ('websters-corners', 'Maple Ridge|Websters Corners', [('house', 'houses'), ('acreage', 'houses with acreage')]),
}
SRC = f'Source: Paragon closed sales, {WINDOW}. Pending sales are not counted. Median means the middle price. Sold vs list is the sale price as a percentage of the last list price. An area is listed only where at least 5 homes of that type sold. Distances are straight line between centre points (OpenStreetMap contributors and Wikipedia).'
def money(v): return f'${v:,.0f}'
def keyfor(name):
    base = re.sub(r'\s+(CQ|MR|Surrey|Burnaby|Maple Ridge|Port Moody)$', '', name).strip().lower()
    hits = [k for k in SUB if re.sub(r'\s+(CQ|MR|Surrey|Burnaby|Maple Ridge|Port Moody)\.?$', '', k.split('|')[1]).strip().lower() == base]
    return hits[0] if len(hits) == 1 else None

def main():
    P = N.load(); by_page = {r['page']: r for r in P}
    for slug, (pkey, skey, groups) in TARGETS.items():
        fixed = FIXED.get(slug)
        me = next((r for r in P if r['page'] in (pkey, pkey + '-guide') or N.clean(r['area'], r['city']).lower().replace(' ', '-') == pkey), None)
        if not me and not fixed: print('NO POINT', slug); continue
        mine = SUB[skey]['groups']
        rows, seen = [], set()
        if fixed:
            me = {'name': skey.split('|')[1]}
            for k in fixed:
                nm = k.split('|')[1]; nm = re.sub(r' (BS|BN|CQ|MR)$', '', nm); g = SUB[k]['groups']; ok = False
                for gk, gl in groups:
                    x = g.get(gk)
                    if x and x['n'] >= 5 and x.get('price'): rows.append((None, {'name': nm}, gl, x, None, k)); ok = True
                if ok: seen.add(k)
        else:
          near = sorted(((N.hav(me['pt'], o['pt']), o) for o in P if o['pt'] != me['pt']), key=lambda x: x[0])
          for d, o in near:
            if d > 14 or len(seen) >= 7: break
            k = keyfor(o['name'])
            if not k or k == skey or k in seen: continue
            g = SUB[k]['groups']
            ok = False
            for gk, gl in groups:
                x = g.get(gk)
                if x and x['n'] >= 5 and x.get('price'):
                    rows.append((d, o, gl, x, N.bearing(me['pt'], o['pt']), k)); ok = True
            if ok: seen.add(k)
        if len(seen) < 3: print('too few neighbours', slug, len(seen)); continue
        p = os.path.join(ROOT, 'src/data/local', slug + '.json')
        j = json.load(open(p, encoding='utf-8')); raw = open(p, encoding='utf-8').read()
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]
        name = me['name']
        # own medians for comparison
        parts = []
        for gk, gl in groups:
            x = mine.get(gk); nb = [r for r in rows if r[2] == gl]
            if x and x['n'] >= 5 and x.get('price') and nb:
                hi = max(nb, key=lambda r: r[3]['price']); lo = min(nb, key=lambda r: r[3]['price'])
                cheaper = sum(1 for r in nb if r[3]['price'] < x['price'])
                parts.append(f"For {gl}, {name} sits at {money(x['price'])}, {'below all ' + str(len(nb)) if cheaper == 0 else ('above all ' + str(len(nb)) if cheaper == len(nb) else 'above ' + str(cheaper) + ' of the ' + str(len(nb)))} nearby areas that can be compared. The highest of them is {hi[1]['name']} at {money(hi[3]['price'])}{f', {hi[0]:.1f} km to the {hi[4]},' if hi[0] is not None else ','} and the lowest {lo[1]['name']} at {money(lo[3]['price'])}.")
            elif nb:
                lo = min(nb, key=lambda r: r[3]['price']); hi = max(nb, key=lambda r: r[3]['price'])
                parts.append(f"{name} did not have 5 sales of {gl} in the period, so it cannot be placed by price, but nearby {gl} sold from {money(lo[3]['price'])} in {lo[1]['name']} to {money(hi[3]['price'])} in {hi[1]['name']}.")
        intro = (f"A price is easier to read next to the areas this page names as its neighbours and landmarks. These are the ones with at least 5 sales of the same type between {WINDOW}." if fixed else f"A price is easier to read next to the areas around it. These are the nearby areas with at least 5 sales of the same type between {WINDOW}, nearest first.")
        table = {'t': 'table', 'caption': f"{name} and nearby areas: what sold", 'head': ['Area'] + (['Distance'] if not fixed else []) + ['Type', 'Sold', 'Median price', 'Days to sell', 'Sold vs list'],
                 'rows': [[o['name']] + ([f"{N.km(d)} {b}"] if not fixed else []) + [gl.capitalize(), str(x['n']), money(x['price']), str(x['dom']), f"{x['ratio']:.1f}%"] for d, o, gl, x, b, k in rows], 'source': SRC, 'gen': G}
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f"How {name} compares with nearby areas", 'gen': G, 'pos': 'end'}, {'t': 'p', 'text': intro, 'gen': G, 'pos': 'end'}]
        j['blocks'] += [{'t': 'p', 'text': t, 'gen': G, 'pos': 'end'} for t in parts] + [dict(table, pos='end')]
        ind = (len(raw.split('\n')[1]) - len(raw.split('\n')[1].lstrip())) or 1
        json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii='\\u' in raw, indent=ind)
        print(slug, 'rows', len(rows), 'areas', len(seen))

if __name__ == '__main__':
    main()
