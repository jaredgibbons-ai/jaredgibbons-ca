"""Draft outlines for the Richmond sub-areas -> src/data/maps/richmond.json

Source: Jared's Paragon map search, GVR Sub Areas 2022 layer, screenshot of 2026-11-05 (Richmond at the zoom where all of Lulu Island fits), read by eye; sub-area names from
Paragon's own Sub-Area/Community lookup (codes VRI10 to VRI90, which settles the numbered layer). Pixels are turned into latitude and longitude with a Web Mercator fit to six
Google Maps landmark coordinates (Terra Nova Viewpoint, Richmond Hospital, Nanaksar Gurdwara, International Buddhist Temple, Gulf of Georgia Cannery, London Farm).
Straight road edges are good to about 80 m; the river shore, the Fraser bank strip to London Farm and the diagonals are good to a block or two. Every area stays 'draft'.
Not drawn (need a closer screenshot or Jared's boundary): Sea Island, Bridgeport, Gilmore, East Richmond, Hamilton (islands, river edges and the cut-off north of the screenshot).
  python3 -I tools/build_richmond_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LAND = [  # (pixel x, pixel y, lat, lng)  icon positions in the 1562 x 784 screenshot
    (494, 193, 49.174324, -123.1892853), (684, 231, 49.1688371, -123.1468284), (1266, 220, 49.1704449, -123.0160006),
    (788, 470, 49.133252, -123.1234303), (505, 527, 49.1251976, -123.1868307), (660, 599, 49.1146447, -123.1519032)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def fit(pts):
    n = len(pts)
    def ls(xs, ys):
        mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
    return ls([p[0] for p in pts], [p[3] for p in pts]), ls([p[1] for p in pts], [merc(p[2]) for p in pts])
(LX, LB), (MY, MB) = fit(LAND)
def ll(px, py):
    lat = math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2); return round(lat, 5), round(LX * px + LB, 5)
def residuals():
    return [(round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
X0, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10 = 466, 530, 582, 630, 680, 730, 780, 830, 880, 950, 1030
Y1, Y2, Y3, Y4, Y5 = 283, 330, 381, 430, 480
AREAS = [  # key in the sold aggregate, page slug, outline in screenshot pixels
 ('Richmond|Terra Nova', 'terra-nova', [(450, 215), (485, 205), (X1, 205), (X1, Y1), (X0, Y1), (448, 262)]),
 ('Richmond|Riverdale RI', 'riverdale-ri', [(X1, 205), (X4, 205), (X4, 235), (X3, 235), (X3, Y1), (X1, Y1)]),
 ('Richmond|Quilchena RI', 'quilchena-ri', [(X0, Y1), (X2, Y1), (X2, Y2), (X0, Y2)]),
 ('Richmond|Granville', 'granville', [(X3, 235), (X4, 235), (X4, Y2), (X2, Y2), (X2, Y1), (X3, Y1)]),
 ('Richmond|Brighouse', 'brighouse-richmond-guide', [(X4, 205), (712, 170), (712, 195), (X6, 195), (X6, Y1), (X4, Y1)]),
 ('Richmond|Brighouse South', 'brighouse-south-richmond', [(X4, Y1), (X6, Y1), (X6, Y2), (X4, Y2)]),
 ('Richmond|McLennan North', 'mclennan-north-richmond', [(X6, 232), (X7, 232), (X7, Y2), (X6, Y2)]),
 ('Richmond|McLennan', None, [(X7, 232), (X9, 232), (X9, Y3), (X7, Y3)]),
 ('Richmond|West Cambie', 'west-cambie', [(738, 88), (X8, 88), (X8, 232), (X6, 232), (X6, 195), (712, 195), (712, 170)]),
 ('Richmond|East Cambie', 'east-cambie', [(X8, 88), (X10, 88), (X10, 232), (X8, 232)]),
 ('Richmond|Seafair', 'seafair', [(468, Y2), (X1, Y2), (X1, Y4), (468, Y4)]),
 ('Richmond|Boyd Park', 'boyd-park', [(X1, Y2), (X2, Y2), (X2, Y4), (X1, Y4)]),
 ('Richmond|Lackner', 'lackner-richmond', [(X2, Y2), (X3, Y2), (X3, Y4), (X2, Y4)]),
 ('Richmond|Woodwards', 'woodwards-richmond', [(X3, Y2), (X4, Y2), (X4, Y5), (X3, Y5)]),
 ('Richmond|Broadmoor', 'broadmoor-richmond', [(X4, Y2), (X5, Y2), (X5, Y5), (X4, Y5)]),
 ('Richmond|Garden City', 'garden-city-richmond', [(X5, Y2), (X7, Y2), (X7, Y3), (X5, Y3)]),
 ('Richmond|Saunders', 'saunders-richmond', [(X5, Y3), (X7, Y3), (X7, Y4), (X5, Y4)]),
 ('Richmond|South Arm', 'south-arm-richmond-guide', [(X5, Y4), (X7, Y4), (X7, Y5), (X5, Y5)]),
 ('Richmond|McNair', 'mcnair-richmond', [(X7, Y3), (X8, Y3), (X8, Y5), (X7, Y5)]),
 ('Richmond|Ironwood', 'ironwood-richmond', [(X8, Y3), (X9, Y3), (X9, Y5), (X8, Y5)]),
 ('Richmond|Steveston North', 'steveston-north-richmond', [(470, Y4), (X3, Y4), (X3, Y5), (468, Y5)]),
 ('Richmond|Steveston Village', 'steveston-village-richmond', [(468, Y5), (X1, Y5), (X1, 545), (505, 545), (470, 520)]),
 ('Richmond|Steveston South', 'steveston-south-richmond', [(X1, Y5), (X2, Y5), (X2, 540), (X3, 540), (632, 555), (648, 585), (670, 615), (680, 630), (650, 615), (620, 590), (585, 572), (545, 558), (X1, 548)]),
 ('Richmond|Westwind', 'westwind-richmond', [(X2, Y5), (X3, Y5), (X3, 540), (X2, 540)]),
]
def main():
    if '--check' in sys.argv: print('landmark residuals (m north, m east):', residuals())
    pts = []; areas = []
    for key, slug, poly in AREAS:
        if slug is None: continue    # McLennan has fewer than 10 sales and no page; drawn for the gap check only
        r = [list(ll(x, y)) for x, y in poly]; r.append(r[0]); pts += r
        name = key.split('|')[1]; areas.append({'id': slug, 'name': {'Hamilton RI': 'Hamilton', 'Quilchena RI': 'Quilchena', 'Riverdale RI': 'Riverdale'}.get(name, name), 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': [r]})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'richmond', 'name': 'Richmond', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    json.dump(out, open(os.path.join(ROOT, 'src/data/maps/richmond.json'), 'w'), separators=(',', ':'))
    print(len(areas), 'areas', bbox)
if __name__ == '__main__': main()
