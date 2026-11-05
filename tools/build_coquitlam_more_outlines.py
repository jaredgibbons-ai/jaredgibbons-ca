"""Draft outlines for three more Coquitlam sub-areas -> src/data/maps/coquitlam.json (ADDITIVE; the 17 areas already there are untouched)

Source: Jared's Paragon map search, GVR Sub Areas 2022 layer with labels on, screenshot `burnaby-east-lougheed-coquitlam-west.jpg` (1920 x 1072; map pane y 200 to 1038) of 2026-11-05.
It shows the west edge of Coquitlam: Central Coquitlam (CC), Coquitlam West (CW) and Maillardville (ML), codes from Closeups/GVR-code-names.csv.  The earlier builder
(build_coquitlam_outlines.py) used other frames of the same Paragon session; this frame does not overlap them, so it has its OWN calibration: a Web Mercator fit to four
landmark icons read off the frame (Burquitlam and Lougheed Town Centre stations, Roy Stibbs Elementary, Our Lady of Lourdes).  Google Maps was
rate-limiting every agent (CAPTCHA wall), so the landmark coordinates come from OpenStreetMap (Nominatim), not Google; --check prints the residuals.  The frame has the same
zoom as the earlier one (about 3.1 m per pixel), which the fit confirms.
Clipped on purpose: the screenshot cuts all three off.  CW and CC run north past the top edge (y 200) and CC, ML run east past the right edge; CW and ML run south past the bottom edge.
Their west edge (North Rd, the Burnaby line, for CW) and the CC/CW (Blue Mountain St) and CC/ML (Rochester Ave) lines are real boundaries; every other side is the screenshot edge.
Not drawn: Coquitlam East (CE).  The polygon coded CE in the Coquitlam town-centre screenshot sits east of Westwood St, south of Lougheed Hwy, among Davies Ave, Gordon Ave, Raleigh St,
Jervis St: those are Port Coquitlam streets, so that CE looks like Central Port Coquitlam, and the real Coquitlam East (Riverview / Colony Farm, along Lougheed Hwy) is south of any frame.
Cape Horn: no polygon is visible in any Coquitlam screenshot (it lies south of this frame, below Hwy 1).  Every area stays 'draft'.
  python3 -I tools/build_coquitlam_more_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'src/data/maps/coquitlam.json')
LAND = [  # (pixel x, pixel y, lat, lng, name)  icon centres in the 1920 x 1072 screenshot; coordinates from OpenStreetMap (Nominatim)
    (1098.8, 225.5, 49.2613584, -122.8898923, 'Burquitlam station'), (933.3, 683.5, 49.2484558, -122.8968482, 'Lougheed Town Centre station'),
    (1229.2, 475.0, 49.2539031, -122.8842884, 'Roy Stibbs Elementary'), (1863.3, 933.3, 49.2411348, -122.8575052, 'Our Lady of Lourdes')]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
(LX, LB) = ls([p[0] for p in LAND], [p[3] for p in LAND]); (MY, MB) = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py):
    lat = math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2); return round(lat, 5), round(LX * px + LB, 5)
def residuals():
    return [(p[4], round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
TOP, BOT, RIGHT = 200, 1038, 1916
AREAS = [  # sold key, page slug, display name, outline in screenshot pixels
 ('Coquitlam|Coquitlam West', 'coquitlam-west', 'Coquitlam West',
  [(1025, TOP), (1586, TOP), (1584, 657), (1499, 771), (1499, 798), (1499, BOT), (1033, BOT)]),
 ('Coquitlam|Central Coquitlam', 'central-coquitlam', 'Central Coquitlam',
  [(1586, TOP), (RIGHT, TOP), (RIGHT, 807), (1744, 807), (1744, 798), (1499, 798), (1499, 771), (1584, 657)]),
 ('Coquitlam|Maillardville', 'maillardville-coquitlam', 'Maillardville',
  [(1499, 798), (1744, 798), (1744, 807), (RIGHT, 807), (RIGHT, BOT), (1499, BOT)]),
]
def main():
    from shapely.geometry import Polygon
    if '--check' in sys.argv: print('landmark residuals (name, m north, m east):', residuals())
    data = json.load(open(OUT)); mine = {a[1] for a in AREAS}
    keep = [a for a in data['areas'] if a['id'] not in mine]
    existing = [(a['id'], [Polygon([(p[1], p[0]) for p in r]) for r in a['rings']]) for a in keep]
    new = []
    for key, slug, name, poly in AREAS:
        ring = [list(ll(x, y)) for x, y in poly]
        g = Polygon([(p[1], p[0]) for p in ring])
        area0 = g.area
        for eid, polys in existing:
            for h in polys:
                if g.intersects(h):
                    ov = g.intersection(h).area
                    if ov > 0: print(f'  {slug}: trimmed {100 * ov / area0:.1f}% overlap with {eid}')
                    g = g.difference(h)
        parts = [g] if g.geom_type == 'Polygon' else sorted(g.geoms, key=lambda x: -x.area)
        rings = []
        for part in parts:
            if part.area < 0.02 * area0: continue
            c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        new.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    areas = keep + new
    pts = [p for a in areas for r in a['rings'] for p in r]
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data['areas'] = areas; data['bbox'] = bbox; data['center'] = {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
    json.dump(data, open(OUT, 'w'), separators=(',', ':'))
    print(len(areas), 'areas', bbox)
if __name__ == '__main__': main()
