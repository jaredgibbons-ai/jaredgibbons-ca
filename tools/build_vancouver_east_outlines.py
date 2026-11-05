"""Draft outlines for the Vancouver East sub-areas -> part file (default /tmp/.../scratchpad/vancouver-e/part.json; the lead merges it with the Vancouver West part)

Source: Jared's Paragon map search (GVR Sub Areas 2022 layer, codes shown), screenshots of 2026-11-04 in pk/Paragon-Sub-Area-Boundaries/screenshots/9-Vancouver:
frame 03 (east of Main, E 15th to E 40th, about 4.7 m per pixel) and frame 01 (overview, exactly one quarter of that scale, about 18.8 m per pixel).  Frame 01 was tied to
frame 03 by template matching (scale 4.00, frame-01 pixel = (618.2 + x3 / 4, 423.5 + (y3 - 192) / 4)); every outline below is in "frame 03 pixels" (a mosaic that is frame 03
where it exists and the overview enlarged four times elsewhere), so neighbouring areas share their vertices and cannot leave gaps.
Pixels are turned into latitude and longitude with a Web Mercator fit to seven Google Maps landmark coordinates seen in frame 03 (Lord Beaconsfield, Windermere, John
Norquay and Sir Richard McBride schools, Sir Charles Tupper Secondary, Joyce-Collingwood and Nanaimo stations).  The school icons are map pins whose coordinate is the pin tip,
10 pixels below the circle centre (the two station icons are flat and anchored at their centre; the fit was best at 10 px: 4 m rms); the fit misses the landmarks by 8 m at worst.
Cross-check outside frame 03: Langara College and Science World (pins in frame 01) land within 1 pixel of frame 01 (about 15 m) when run through the same fit and the 4.00 scale.
Straight road edges are good to about 50 m in frame 03 and about 100 m where only the overview shows the edge (Hastings, Hastings Sunrise, Strathcona, Downtown VE, Grandview
Woodland north of E 16th, Killarney, Fraserview, South Vancouver, Champlain Heights, South Marine); shorelines and the Fraser River edges to a block or two.
Clipped on purpose: South Marine is cut at the bottom of the overview frame (its east end runs on south); every area's east edge is Boundary Rd (a straight line here).
Not drawn: nothing; all 18 Vancouver East sold keys are drawn.  Downtown VE has no code in the csv: it is the narrow polygon that carries a second 'DT' label between Gastown's
Downtown VW and Strathcona (Beatty/Main St, BC Place to Science World).  Every area stays 'draft'.
  python3 -I tools/build_vancouver_east_outlines.py [--check] [out.json]"""
import json, math, os, sys
import os, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(tempfile.gettempdir(), 'outline-parts', 'vancouver-east.part.json')   # scratch part file; tools/merge_city_outlines.py merges the parts
# (frame-03 x, y of the coordinate point, lat, lng); pins use circle centre + 10 px
LAND = [(835.4, 309.9, 49.2520099, -123.052713), (1059.9, 441.8, 49.2463931, -123.0381322), (855.0, 541.0, 49.2422144, -123.0513705), (1158.75, 632.4, 49.2383732, -123.0317578),
        (783.6, 396.75, 49.2482782, -123.0559173), (163.25, 366.9, 49.2495512, -123.0958226), (436.6, 490.9, 49.2443169, -123.078232)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
def residuals(): return [(round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
def overview_check():
    """Langara College and Science World through the fit and the 4.00 overview scale -> frame-01 pixel, against the measured pin tips (613.0, 613.5) and (628.5, 326.5)."""
    out = []
    for lat, lng in ((49.2249723, -123.1076016), (49.273376, -123.103834)):
        x3 = (lng - LB) / LX; y3 = (merc(lat) - MB) / MY; out.append((round(618.2 + x3 / 4, 1), round(423.5 + (y3 - 192) / 4, 1)))
    return out
def BX(y): return round(1288 - 0.0054 * (y + 680))     # Boundary Rd (east edge of every area), mosaic x at mosaic y
# --- shared edges (frame-03 pixels) ---
MP_ST = [(100, -97), (122, -72), (161, -47), (211, -44), (267, -44), (306, -30), (378, -9), (452, 0)]           # Strathcona / Mount Pleasant VE edge, west to east
KN_E = [(565, 203), (566, 250), (574, 253), (567, 258), (562, 275), (561, 338), (548, 347), (544, 400), (543, 430), (543, 507), (553, 510), (553, 589), (547, 589), (547, 640),
        (542, 680), (539, 762)]                                                                                  # Knight / Victoria VE edge, north to south
FR_KN = [(381, 199), (380, 330), (378, 400), (366, 480), (362, 540), (356, 575), (355, 675), (374, 680), (375, 855), (356, 858), (356, 940)]  # Fraser VE / Knight edge, north to south
VI_E = [(740, 762), (741, 600), (743, 566), (750, 548), (761, 537), (770, 512), (771, 500), (772, 470), (772, 401)]   # Victoria VE / Collingwood VE edge, south to north
GW_S = [(773, 388), (736, 372), (700, 350), (671, 334), (653, 327), (636, 305), (625, 284), (626, 205)]               # Grandview Woodland south edge, east to west
RH_CO = [(772, 401), (792, 409), (822, 426), (850, 447), (872, 467), (883, 486)]                                                   # Renfrew Heights / Collingwood VE edge, west to east
SHORE_SU = [(BX(-681), -681), (1237, -669), (1187, -637), (1150, -622), (1100, -622), (1031, -638), (987, -656), (937, -672), (875, -691), (812, -653), (775, -641)]
SM_S = [(1277, 1508), (1218, 1500), (1166, 1489), (1134, 1476), (1103, 1458), (1050, 1447), (1029, 1431), (945, 1424), (850, 1424), (780, 1423), (730, 1418), (690, 1408),
        (640, 1397), (595, 1400), (570, 1380), (530, 1362), (480, 1355), (430, 1352), (350, 1373), (275, 1391), (200, 1424), (120, 1445), (40, 1437), (2, 1428)]
SV_S = [(2, 1248), (60, 1262), (120, 1272), (200, 1280), (450, 1278)]                                                  # Marine Dr, west to east
FV_S = [(450, 1278), (500, 1279), (571, 1306), (643, 1329), (700, 1354), (750, 1372), (871, 1361), (1003, 1351)]
CH_S = [(1003, 1351), (1030, 1350), (1060, 1366), (1075, 1375), (BX(1375), 1375)]
# --- polygons ---
SU = [(775, -392), (BX(-392), -392), *SHORE_SU]
RE = [(773, -392), (BX(-392), -392), (BX(-16), -16), (1248, 8), (1212, 52), (1180, 72), (773, 70)]
HA = [(453, -285), (775, -285), (775, -641), (717, -606), (692, -597), (674, -553), (642, -541), (588, -520), (567, -553), (455, -588)]
ST = [(100, -585), (160, -560), (200, -545), (230, -585), (300, -560), (303, -505), (340, -515), (400, -540), (430, -580), (453, -588), (453, -2), *MP_ST[::-1]]
DT = [(33, -503), (100, -498), (100, -190), (33, -190)]
MP = [(27, -170), (61, -190), (100, -190), *MP_ST, (452, 199), (23, 199), (26, 0)]
GW = [(453, -285), (774, -285), *GW_S, (625, 205), (565, 204), (565, 199), (453, 199)]
MN = [(23, 199), (148, 199), (146, 500), (145, 750), (146, 940), (3, 940), (5, 800), (12, 700), (20, 500)]
FR = [(148, 199), *FR_KN, (146, 940), (145, 750), (146, 500)]
KN = [(381, 199), (565, 199), *KN_E, (539, 1058), (450, 1058), (450, 940), *FR_KN[::-1][:-1]]
VI = [*KN_E, *VI_E[:-1], (772, 401), (773, 388), *GW_S[1:]]
CO = [*RH_CO, (BX(486), 486), (BX(785), 785), (1200, 776), (1140, 763), *VI_E[:-1]]
RH = [(773, 70), (1180, 72), (1212, 52), (1248, 8), (BX(-16), -16), (BX(486), 486), (882, 486), *RH_CO[::-1][1:], (773, 388)]
KL = [(539, 762), (741, 762), (1140, 763), (1200, 776), (BX(785), 785), (BX(1058), 1058), (539, 1058)]
SV = [(3, 940), (450, 940), *SV_S[::-1]]
FV = [(450, 1058), (1003, 1058), *FV_S[::-1]]
CH = [(1003, 1058), (BX(1058), 1058), *CH_S[::-1]]
SM = [*SV_S, *FV_S[1:], *CH_S[1:], *SM_S]
AREAS = [  # sold key, page slug, display name, polygon (frame-03 pixels); earlier areas keep their ground where outlines overlap by hand-reading error
 ('Vancouver East|Downtown VE', 'downtown-ve', 'Downtown VE', DT),
 ('Vancouver East|Strathcona', 'strathcona-vancouver', 'Strathcona', ST),
 ('Vancouver East|Hastings', 'hastings', 'Hastings', HA),
 ('Vancouver East|Hastings Sunrise', 'hastings-sunrise-vancouver', 'Hastings Sunrise', SU),
 ('Vancouver East|Mount Pleasant VE', 'mount-pleasant-vancouver-guide', 'Mount Pleasant (East)', MP),
 ('Vancouver East|Grandview Woodland', 'grandview-woodland', 'Grandview Woodland', GW),
 ('Vancouver East|Renfrew VE', 'renfrew-vancouver', 'Renfrew', RE),
 ('Vancouver East|Renfrew Heights', 'renfrew-heights-vancouver', 'Renfrew Heights', RH),
 ('Vancouver East|Main', 'main', 'Main', MN),
 ('Vancouver East|Fraser VE', 'fraser-ve', 'Fraser', FR),
 ('Vancouver East|Knight', 'knight', 'Knight', KN),
 ('Vancouver East|Victoria VE', 'victoria-vancouver', 'Victoria', VI),
 ('Vancouver East|Collingwood VE', 'collingwood-ve', 'Collingwood', CO),
 ('Vancouver East|Killarney VE', 'killarney-ve', 'Killarney', KL),
 ('Vancouver East|South Vancouver', 'south-vancouver-vancouver', 'South Vancouver', SV),
 ('Vancouver East|Fraserview VE', 'fraserview-ve', 'Fraserview', FV),
 ('Vancouver East|Champlain Heights', 'champlain-heights', 'Champlain Heights', CH),
 ('Vancouver East|South Marine', 'south-marine-vancouver', 'South Marine', SM),
]
def trimmed(rows):
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any overlap (under 6000 px2, about 13 ha) with an earlier one."""
    from shapely.geometry import Polygon
    done = []; out = []
    for key, slug, name, ring in rows:
        g = Polygon(ring)
        if not g.is_valid: g = g.buffer(0)
        for h in done:
            if g.intersects(h) and g.intersection(h).area < 6000: g = g.difference(h)
        done.append(g)
        gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
        out.append((key, slug, name, list(gg.exterior.coords)[:-1]))
    return out
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--check' in sys.argv: print('landmark residuals (m north, m east):', residuals(), '| overview check (frame-01 px; measured (613.0, 613.5), (628.5, 326.5)):', overview_check())
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    pts = []; areas = []
    for key, slug, name, ring in trimmed(AREAS):
        r = [list(ll(x, y)) for x, y in ring]; r.append(r[0]); pts += r
        assert key in sold, key
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': [r]})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'vancouver', 'name': 'Vancouver', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    path = args[0] if args else OUT
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, 'w'), separators=(',', ':')); print('vancouver (east part)', len(areas), 'areas', bbox, '->', path)
if __name__ == '__main__': main()
