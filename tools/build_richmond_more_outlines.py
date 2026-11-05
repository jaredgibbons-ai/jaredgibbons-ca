"""Draft outlines for five more Richmond sub-areas -> src/data/maps/richmond.json (ADDITIVE; the 23 areas already there are untouched)

Source: Jared's Paragon map search, GVR Sub Areas 2022 layer (number codes, no names) in `7-Richmond/01-overview.webp` (frame R1, all of Lulu Island, about 18.7 m per pixel) and
`03-south.webp` (frame R3, about 14.4 m per pixel), both 1280 x 800, map pane y 190 to 750, of 2026-11-04.  Each frame has its OWN Web Mercator fit to landmark icons whose Google
Maps coordinates the earlier Richmond builder already holds (Richmond Hospital, Nanaksar Gurdwara, International Buddhist Temple, Gulf of Georgia Cannery, London Farm; R1 also
Terra Nova Viewpoint, which R3 does not show as an icon).  --check prints the residuals.
Identification (codes are NOT in Closeups/GVR-code-names.csv; by position, with the 23 areas already drawn used up first):
  10 Sea Island        sure.  The airport island, with Swishwash Island and a second islet also labelled 10.
  11 Bridgeport RI     fairly sure.  North of Bridgeport Rd with Mitchell Island, between Oak St and Hwy 99 / No 6 Rd.
  72 East Richmond     fairly sure.  The one polygon east of Hwy 99 / No 5 Rd (Hwy 91 corridor, Nanaksar temple), plus two river islets also labelled 72.
  90 Hamilton RI       less sure.  Small polygon in the north-east corner, east of the long 72 polygon; picked by elimination and because Hamilton Elementary (5180 Smith Dr) lies just past the frame edge.
  70 Gilmore           least sure.  Farmland south of Steveston Hwy and the river islands; the only code left, and Gilmore listings sit on Steveston Hwy, Finn Rd, No 4 Rd and Gilbert Rd.
Not drawn: the river-island pieces labelled 70 (Shady, Kirkland, Barber islands and the south-arm foreshore); they are faint and may belong to the same polygon or not.  McLennan (71, no page) was left out.
Clipped on purpose: Sea Island runs north past the top of R1 (airport, y 190), Hamilton runs east past its right edge (x 1280); Mitchell Island touches the top edge.
The 72 polygon is read from R1; 70 is read from R3 (R1 cuts its south bank).  Straight road edges are good to about 100 m, river banks to a block or two.  Every area stays 'draft'.
  python3 -I tools/build_richmond_more_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'src/data/maps/richmond.json')
G = {  # landmark name -> (lat, lng)  Google Maps coordinates (from build_richmond_outlines.py)
    'Terra Nova Viewpoint': (49.174324, -123.1892853), 'Richmond Hospital': (49.1688371, -123.1468284), 'Nanaksar Gurdwara': (49.1704449, -123.0160006),
    'International Buddhist Temple': (49.133252, -123.1234303), 'Gulf of Georgia Cannery': (49.1251976, -123.1868307), 'London Farm': (49.1146447, -123.1519032)}
PIX = {  # icon centres read off each frame: name -> (x, y)
    'R1': {'Terra Nova Viewpoint': (432.7, 379.7), 'Richmond Hospital': (598.0, 412.5), 'Nanaksar Gurdwara': (1107.7, 402.5), 'International Buddhist Temple': (688.8, 623.0),
           'Gulf of Georgia Cannery': (444.2, 669.2), 'London Farm': (578.3, 734.2)},
    'R3': {'Richmond Hospital': (685.7, 252.3), 'Nanaksar Gurdwara': (1195.5, 241.3), 'International Buddhist Temple': (775.2, 464.2), 'Gulf of Georgia Cannery': (529.2, 508.3),
           'London Farm': (665.3, 573.2)}}
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
FIT = {}
for fr, d in PIX.items():
    names = list(d); FIT[fr] = (ls([d[n][0] for n in names], [G[n][1] for n in names]), ls([d[n][1] for n in names], [merc(G[n][0]) for n in names]))
def ll(fr, px, py):
    (LX, LB), (MY, MB) = FIT[fr]; return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
def residuals():
    out = {}
    for fr, d in PIX.items(): out[fr] = [(n, round((ll(fr, *p)[0] - G[n][0]) * 111200), round((ll(fr, *p)[1] - G[n][1]) * 73000)) for n, p in d.items()]
    return out
def S(px, py): return (330 + px / 2.5, 190 + py / 2.5)             # R1 crop at 2.5x from (330,190)
def E(px, py): return (1100 + px / 3.5, 260 + py / 3.5)            # R1 crop at 3.5x from (1100,260)
# --- outlines in frame pixels: (sold key, id, display name, frame, [rings]) ---
SEA = [S(*p) for p in [(120, 0), (600, 0), (640, 40), (690, 85), (740, 105), (775, 140), (778, 165), (765, 190), (750, 225), (765, 240), (740, 262), (730, 300), (700, 350), (650, 385),
                       (600, 410), (550, 430), (480, 445), (430, 448), (400, 440), (350, 430), (300, 405), (260, 380), (215, 350), (165, 330), (110, 310), (62, 300), (60, 260), (65, 200),
                       (70, 150), (75, 100), (95, 50)]]
SWISH = [S(*p) for p in [(30, 368), (80, 360), (150, 372), (205, 396), (232, 420), (205, 420), (150, 405), (100, 392), (55, 380)]]
ISLET = [S(*p) for p in [(250, 420), (272, 414), (290, 432), (285, 447), (262, 443)]]
BRIDGEPORT = [(645, 284), (645, 277), (650, 266), (667, 257), (680, 250), (697, 239), (710, 234), (723, 232), (740, 237), (760, 246), (780, 252), (803, 255), (830, 252), (857, 245), (880, 233),
              (907, 223), (943, 218), (943, 252), (899, 253), (899, 284)]
MITCHELL = [(718, 214), (740, 212), (770, 211), (803, 207), (830, 201), (863, 194), (893, 193), (904, 203), (897, 211), (880, 222), (863, 232), (845, 240), (815, 244), (790, 243), (761, 235), (741, 228), (722, 219)]
EAST = [(899, 285), (899, 252), (941, 252), (945, 241), (981, 237), (1020, 240), (1064, 246), (1103, 259), (1137, 279), (1170, 301), (1198, 326), (1226, 343), (1246, 357), (1247, 414), (1250, 440),
        (1225, 442), (1195, 455), (1165, 472), (1140, 487), (1115, 497), (1090, 510), (1060, 520), (1030, 530), (1005, 545), (985, 560), (965, 580), (946, 603), (930, 623), (914, 640), (901, 657),
        (888, 674), (868, 688), (863, 685), (834, 650), (831, 632), (831, 415), (899, 415)]
EAST_I1 = [E(*p) for p in [(232, 795), (255, 770), (300, 735), (285, 760), (250, 790)]]
EAST_I2 = [E(*p) for p in [(308, 778), (340, 745), (425, 710), (400, 735), (350, 765)]]
HAMILTON = [(1247, 358), (1280, 357), (1280, 429), (1250, 440), (1247, 414)]
GILMORE = [(639, 472), (919, 472), (922, 489), (937, 508), (952, 529), (940, 534), (930, 536), (922, 522), (916, 524), (916, 540), (905, 546), (895, 557), (875, 574), (855, 589), (835, 599),
           (805, 608), (760, 611), (715, 607), (682, 600), (672, 585), (652, 557), (640, 537)]
AREAS = [
 ('Richmond|Sea Island', 'seaisland', 'Sea Island', 'R1', [SEA, SWISH, ISLET]),
 ('Richmond|Bridgeport RI', 'bridgeport-ri', 'Bridgeport', 'R1', [BRIDGEPORT, MITCHELL]),
 ('Richmond|East Richmond', 'east-richmond', 'East Richmond', 'R1', [EAST, EAST_I1, EAST_I2]),
 ('Richmond|Hamilton RI', 'hamilton-richmond', 'Hamilton', 'R1', [HAMILTON]),
 ('Richmond|Gilmore', 'gilmore-richmond', 'Gilmore', 'R3', [GILMORE]),
]
# East Richmond and Gilmore are drawn but held back from the map: the site has no page for either sold area yet, and a map link must land on a page. Remove from HELD when the pages exist.
HELD = {'east-richmond', 'gilmore-richmond'}
def main():
    from shapely.geometry import Polygon
    if '--check' in sys.argv: print('landmark residuals (name, m north, m east):', residuals())
    data = json.load(open(OUT)); mine = {a[1] for a in AREAS}
    keep = [a for a in data['areas'] if a['id'] not in mine]
    existing = [(a['id'], [Polygon([(p[1], p[0]) for p in r]) for r in a['rings']]) for a in keep]
    new = []
    for key, slug, name, fr, rings_px in AREAS:
        if slug in HELD: continue
        rings = []
        for poly in rings_px:
            g = Polygon([(ll(fr, x, y)[1], ll(fr, x, y)[0]) for x, y in poly]); a0 = g.area
            for eid, polys in existing:
                for h in polys:
                    if g.intersects(h):
                        ov = g.intersection(h).area
                        if ov > 0: print(f'  {slug}: trimmed {100 * ov / a0:.1f}% of a ring against {eid}')
                        g = g.difference(h)
            for part in ([g] if g.geom_type == 'Polygon' else sorted(g.geoms, key=lambda x: -x.area)):
                if part.area < 0.02 * a0: continue
                c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        new.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    areas = keep + new
    pts = [p for a in areas for r in a['rings'] for p in r]
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data['areas'] = areas; data['bbox'] = bbox; data['center'] = {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
    json.dump(data, open(OUT, 'w'), separators=(',', ':'))
    print(len(areas), 'areas', bbox)
if __name__ == '__main__': main()
