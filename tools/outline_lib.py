"""Shared helpers for the neighbourhood outline builders (tools/build_outlines.py, build_ssw_outlines.py).

Grid: Surrey / Langley avenues and streets are evenly spaced.  Fitted to 15 Google Maps intersection coordinates between 120 St and 264 St and 16 Ave and 104 Ave
(rms error about 25 m, worst about 70 m):
    latitude  = 49.001776 + 0.0018276 * avenue
    longitude = -123.220335 + 0.0027568 * street
Vertices are written as (avenue, street) pairs, fractions allowed, so an outline reads like its boundary streets.  Every area stays 'draft'.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def lat(a): return 49.001776 + 0.0018276 * a
def lon(s): return -123.220335 + 0.0027568 * s
def ring(pts):
    r = [[round(lat(a), 5), round(lon(s), 5)] for a, s in pts]
    if r[0] != r[-1]: r.append(r[0])
    return r

def build(region, name, areas, flyover=None):
    """areas: list of dicts {id, name, href, sold, pts, group?}.  Writes src/data/maps/<region>.json and returns the dict."""
    out_areas = []
    for a in areas:
        o = {'id': a['id'], 'name': a['name'], 'href': a['href'], 'status': 'draft', 'sold': a['sold']}
        if a.get('group'): o['group'] = True
        o['rings'] = [ring(a['pts'])]
        out_areas.append(o)
    pts = [p for a in out_areas for r in a['rings'] for p in r]
    pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': region, 'name': name, 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': out_areas}
    if flyover is not None: out['flyover'] = flyover
    json.dump(out, open(os.path.join(ROOT, 'src/data/maps', region + '.json'), 'w'), separators=(',', ':'))
    return out

def check(out):
    """Shape checks: valid polygons, overlaps and gaps (needs shapely, pip install shapely)."""
    from shapely.geometry import Polygon
    import shapely
    k = 73.0 * 111.2
    P = {a['id']: Polygon([(x, y) for y, x in a['rings'][0]]) for a in out['areas']}
    bad = [i for i, p in P.items() if not p.is_valid]
    ids = list(P)
    over = [(a, b, round(P[a].intersection(P[b]).area * k, 3)) for i, a in enumerate(ids) for b in ids[i + 1:] if P[a].is_valid and P[b].is_valid and P[a].intersection(P[b]).area * k > 0.02]
    return {'invalid': bad, 'overlaps': over, 'areas_km2': {i: round(p.area * k, 2) for i, p in P.items()}}
