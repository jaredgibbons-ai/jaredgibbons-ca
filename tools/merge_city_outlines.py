"""Merge the per-half draft outline builders for Burnaby (North + South/East) and Vancouver (West + East) into src/data/maps/<city>.json.

Each half is drawn by its own builder (build_<city>_<part>_outlines.py) from the same Paragon screenshots and writes a part file; this tool runs them,
gives the later half way where a hand-read sliver overlaps the earlier half (overlaps over 4 % of an area are reported, not trimmed), renames the
two Mount Pleasant halves (they share one page) and writes the final map.  Every area stays draft.   Run: python3 -I tools/merge_city_outlines.py
"""
import json, os, subprocess, sys, tempfile
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(tempfile.gettempdir(), 'outline-parts')
CITIES = {'burnaby': ('Burnaby', ['burnaby_north', 'burnaby_south']), 'vancouver': ('Vancouver', ['vancouver_west', 'vancouver_east'])}
RENAME = {'Vancouver East|Mount Pleasant VE': ('mount-pleasant-ve', 'Mount Pleasant (east of Ontario St)'), 'Vancouver West|Mount Pleasant VW': ('mount-pleasant-vw', 'Mount Pleasant (west of Ontario St)')}
LIMIT = 0.04
# Where the later half draws a narrow polygon that sits inside the earlier half's wider one, the narrow (printed, white-lined) polygon wins and the wide one gives way.
WIDE_YIELDS = {'downtown-ve': 'downtown-vw'}

def geom(a): return unary_union([Polygon([(p[1], p[0]) for p in r]).buffer(0) for r in a['rings']])
def rings(g):
    ps = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    return [[[round(y, 5), round(x, 5)] for x, y in p.exterior.coords] for p in sorted(ps, key=lambda p: -p.area) if p.area > 0 and not p.is_empty]

def main():
    for city, (name, builders) in CITIES.items():
        areas, seen = [], None
        for b in builders:
            subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tools', f'build_{b}_outlines.py')], check=True, stdout=subprocess.DEVNULL)
            part = json.load(open(os.path.join(PARTS, b.replace('_', '-') + '.part.json')))
            for a in part['areas']:
                a = dict(a)
                if a.get('sold') in RENAME: a['id'], a['name'] = RENAME[a['sold']]
                g = geom(a)
                if seen is not None and g.intersects(seen):
                    cut = g.intersection(seen).area
                    if a['id'] in WIDE_YIELDS:
                        w = next(x for x in areas if x['id'] == WIDE_YIELDS[a['id']]); w['rings'] = rings(geom(w).difference(g)); print(f'  {w["id"]} gives way to {a["id"]} ({cut / geom(w).area:.1%} of it before)')
                    elif cut / g.area > LIMIT: print(f'  !! {a["id"]}: {cut / g.area:.1%} overlaps the earlier half, NOT trimmed')
                    else:
                        g = g.difference(seen.buffer(0)); a['rings'] = rings(g)
                areas.append(a)
            seen = unary_union([geom(a) for a in areas])
        ids = [a['id'] for a in areas]; assert len(ids) == len(set(ids)), 'duplicate ids'
        lats = [p[0] for a in areas for r in a['rings'] for p in r]; lngs = [p[1] for a in areas for r in a['rings'] for p in r]
        bbox = [round(min(lats) - 0.004, 4), round(min(lngs) - 0.004, 4), round(max(lats) + 0.004, 4), round(max(lngs) + 0.004, 4)]
        out = {'region': city, 'name': name, 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
        json.dump(out, open(os.path.join(ROOT, 'src/data/maps', city + '.json'), 'w'), separators=(',', ':'))
        print(city, len(areas), 'areas', bbox)

if __name__ == '__main__': main()
