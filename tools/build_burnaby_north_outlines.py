"""Draft outlines for Burnaby North (Paragon / GVR sub-area layer) -> a PART file (scratchpad/burnaby-n/part.json) that the lead merges with the Burnaby South + East part.

Source: Jared's Paragon map screenshots of 2026-11-05, four of the six frames in screenshots/10-Burnaby (all four are the same Paragon zoom, 4.29e-5 deg of longitude per pixel, but they
do not overlap enough to register, so every frame has its OWN pixel -> lat/lng fit and the polygons are combined in lat/lng):
  A burnaby-north-capitol-hill.jpg  (Vancouver Heights, Capitol Hill, Sperling-Duthie, Westridge, Willingdon Heights, Brentwood Park, Parkcrest, top strip of Central BN, strip of Simon Fraser Univer.)
  B burnaby-central-deer-lake.jpg   (Central BN, Government Road, Montecito north of Lougheed Hwy, southern tips of Brentwood Park)
  C burnaby-east-sfu.jpg            (Simon Fraser Univer., west edge of Westridge, Montecito's southern lens, Forest Hills tip)
  D burnaby-east-lougheed-coquitlam-west.jpg (Forest Hills, Simon Fraser Hills, Oakdale (the 'OK' label, UNCONFIRMED in GVR-code-names.csv), Sullivan Heights, Government Road, Cariboo)
Codes: VH CH WR SD WH BP PC CB GR MO SF FH SI SH CA OK read from the labels over the polygons (names from Closeups/GVR-code-names.csv; CB, SF, SI, OK are UNCONFIRMED there).
Calibration.  A: 10 Google Maps landmarks (Burnaby North Secondary, Westridge Elementary, Confederation Park, McGill library, Capitol Hill Reservoir Park, Lou Moro Park, Lochdale Community School,
Willingdon Heights Park tennis courts, Railway Beach, Burnaby Central Railway), free linear fit, worst miss 11 m.  B: 7 Google Maps landmarks (Burnaby Hospital, Cascade Heights Elementary, Deer Lake
School, Burnaby Central Secondary, Burnaby Village Museum, Scotia Barn, Burnaby Lake Archery Range; Sperling-Burnaby Lake station dropped, 49 m off), fixed scale, worst miss 5 m.
C and D: Google Maps started returning CAPTCHAs to every agent, so their landmarks are OpenStreetMap (Nominatim) coordinates of the same icons (school/park polygon centres, so a little coarser).
C: Harry Jerome Sports Centre, W.A.C. Bennett Library (Google), Fraser International College (Google), Ecole Glenayre, Greater Heights Learning Academy; free fit, worst miss 43 m (Squint Lake Park
dropped, 240 m off: its OSM centre is not where Paragon's icon sits).  D: Production Way-University, Seaforth Elementary, Lougheed Town Centre, Roy Stibbs, Burquitlam station; frame-A scale kept and
only the offset fitted, worst miss 37 m (Burnaby Mountain Secondary and Stoney Creek Community School dropped, 89 and 62 m off; large school sites).  Frames B and D meet within 10 m on the Government Road
edges, A and B agree on Willingdon Ave within 25 m, A and C agree on Phillips Ave within 75 m.
Edges read off the screenshots are good to ~100 m on straight roads and a block or two on creek, lake and shore edges.
Clipped on purpose (the screenshots stop there): Oakdale and Simon Fraser Hills run north past the top of frame D; Forest Hills past the top and left of D; Simon Fraser Univer. past the bottom of C;
Capitol Hill, Willingdon Heights, Brentwood Park, Parkcrest, Sperling-Duthie, Central BN, Montecito run on past the bottom of A / the top of B; Sullivan Heights and Cariboo past D's right and bottom;
Government Road past the left edge of D (it joins B; B's piece is extended 55 px, ~160 m, to meet D's edge) and past B's lake edge.
Gaps between frames (not drawn, no invention): A's bottom and B's top are 1.1 km apart (Willingdon Heights, Brentwood Park, Central BN, Parkcrest continue through it) and C's bottom and D's top 0.5 km
apart.  Only Forest Hills is bridged across that second gap (straight sides, both ends show the same two edges); Montecito, Brentwood Park and Central BN stay as separate pieces (rings).
Central BN's west edge (Boundary Rd) is extended 45 px past frame B's left edge because frame A shows Boundary Rd there.
Every area stays 'draft'.  Overlaps between neighbours (hand-read slivers) are cut from the later area in the order below.
  python3 -I tools/build_burnaby_north_outlines.py [--check]"""
import json, math, os, sys
import os, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(tempfile.gettempdir(), 'outline-parts', 'burnaby-north.part.json')   # scratch part file; tools/merge_city_outlines.py merges the parts
# (x, y, lat, lng, label) in frame pixels
LA = [(1338, 775, 49.2778053, -122.9728477, 'Burnaby North Secondary'), (1597, 729, 49.2790799, -122.9617344, 'Westridge Elementary'), (708, 567, 49.2836569, -122.9998757, 'Confederation Park'),
      (690, 607, 49.2826196, -123.0005824, 'McGill library'), (924, 458, 49.2867017, -122.9906262, 'Capitol Hill Reservoir Park'), (1678, 650, 49.281323, -122.958251, 'Lou Moro Park'),
      (1623, 938, 49.2732089, -122.9605883, 'Lochdale Community School'), (424, 933, 49.2733765, -123.0120147, 'Willingdon Heights Park tennis'), (1151, 275, 49.2918021, -122.9808682, 'Railway Beach'),
      (677, 488, 49.2858584, -123.0012116, 'Burnaby Central Railway')]
LB = [(133, 574, 49.2497113, -123.0158866, 'Burnaby Hospital'), (33, 722, 49.2454949, -123.0201963, 'Cascade Heights Elementary'), (893, 869, 49.2414337, -122.9832758, 'Deer Lake School'),
      (1092, 802, 49.2433009, -122.9747465, 'Burnaby Central Secondary'), (1298, 943, 49.2393853, -122.9658755, 'Burnaby Village Museum'), (1192, 514, 49.2513781, -122.9704314, 'Scotia Barn'),
      (1305, 411, 49.2542083, -122.9655806, 'Burnaby Lake Archery Range')]
LC = [(205, 264, 49.2890565, -122.9405192, 'Harry Jerome Sports Centre'), (718, 587, 49.2796599, -122.9188558, 'WAC Bennett Library'), (881, 796, 49.2738527, -122.9118691, 'Fraser International College'),
      (1441, 787, 49.2734794, -122.8882111, 'Ecole Glenayre (OSM)'), (1372, 1003, 49.2677132, -122.8905900, 'Greater Heights Learning Academy (OSM)')]
LD = [(438, 507, 49.2534219, -122.9181460, 'Production Way-University (OSM)'), (18, 543, 49.2519051, -122.9361017, 'Seaforth Elementary (OSM)'), (933, 684, 49.2484558, -122.8968482, 'Lougheed Town Centre (OSM)'),
      (1228, 476, 49.2539031, -122.8842884, 'Roy Stibbs (OSM)'), (1098, 225, 49.2613584, -122.8898923, 'Burquitlam (OSM)')]
S = 4.2895e-5; M = -S * math.pi / 180
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def unmerc(m): return math.degrees(2 * math.atan(math.exp(m)) - math.pi / 2)
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def free(L):
    LX, LB_ = ls([p[0] for p in L], [p[3] for p in L]); MY, MB = ls([p[1] for p in L], [merc(p[2]) for p in L])
    return lambda px, py: (unmerc(MY * py + MB), LX * px + LB_)
def fixed(L):
    LB_ = sum(p[3] - S * p[0] for p in L) / len(L); MB = sum(merc(p[2]) - M * p[1] for p in L) / len(L)
    return lambda px, py: (unmerc(M * py + MB), S * px + LB_)
FR = {'A': free(LA), 'B': fixed(LB), 'C': free(LC), 'D': fixed(LD)}
LAND = {'A': LA, 'B': LB, 'C': LC, 'D': LD}
def residuals(L, f): return [(p[4], round((f(p[0], p[1])[0] - p[2]) * 111200), round((f(p[0], p[1])[1] - p[3]) * 72700)) for p in L]
# ---- polygons in frame pixels ----
VH = [(152, 228), (212, 228), (300, 224), (350, 234), (400, 241), (450, 253), (500, 266), (525, 284), (544, 300), (587, 316), (634, 325), (634, 670), (152, 670)]
CH = [(634, 325), (639, 319), (732, 306), (764, 294), (801, 259), (839, 244), (882, 219), (901, 205), (905, 200), (1082, 200), (1151, 237), (1207, 262), (1245, 300), (1264, 325), (1301, 350), (1345, 336),
      (1301, 512), (1301, 525), (1298, 656), (1294, 674), (1280, 683), (1277, 697), (1275, 738), (1152, 741), (1150, 808), (634, 808), (634, 670)]
SD = [(1345, 336), (1401, 366), (1439, 400), (1489, 419), (1532, 410), (1570, 400), (1582, 397), (1620, 406), (1650, 416), (1649, 681), (1670, 697), (1792, 698), (1792, 1040), (1403, 1040), (1403, 882),
      (1189, 879), (1150, 870), (1150, 741), (1275, 738), (1277, 697), (1280, 683), (1294, 674), (1298, 656), (1301, 525), (1301, 512)]
WR_A = [(1650, 416), (1682, 400), (1720, 394), (1764, 369), (1801, 347), (1845, 341), (1920, 339), (1920, 698), (1667, 697), (1649, 681)]
WR_C = [(0, 217), (42, 219), (79, 383), (77, 577), (0, 578)]
WH = [(155, 670), (634, 670), (634, 1040), (352, 1040), (340, 1026), (155, 1026)]
BP_A = [(634, 808), (988, 807), (988, 1040), (634, 1040)]
BP_B1 = [(222, 200), (237, 217), (250, 233), (267, 247), (287, 251), (307, 245), (327, 233), (343, 217), (353, 200)]
BP_B2 = [(410, 200), (422, 215), (465, 215), (467, 200)]
PC = [(988, 808), (1150, 808), (1150, 870), (1189, 879), (1403, 882), (1403, 1040), (988, 1040)]
CB_A = [(155, 1026), (340, 1026), (352, 1040), (155, 1040)]
CB_B = [(-45, 200), (1247, 200), (1231, 228), (1240, 269), (1253, 317), (1278, 407), (1282, 476), (1281, 581), (1283, 700), (1280, 790), (1255, 840), (1240, 871), (1095, 737), (1065, 712), (1045, 700),
        (1025, 672), (1000, 652), (975, 635), (955, 620), (932, 590), (905, 580), (840, 577), (780, 576), (760, 567), (760, 540), (760, 475), (757, 446), (736, 425), (643, 414), (600, 410), (-45, 409)]
GR_B = [(1247, 200), (1322, 234), (1467, 265), (1633, 286), (1674, 310), (1771, 365), (1843, 398), (1915, 421), (1975, 440), (1975, 985), (1918, 971), (1865, 959), (1827, 952), (1752, 946), (1696, 927),
        (1640, 915), (1609, 896), (1590, 871), (1540, 852), (1515, 821), (1490, 809), (1487, 790), (1490, 756), (1456, 737), (1434, 734), (1427, 696), (1412, 659), (1421, 627), (1424, 612), (1446, 599),
        (1474, 583), (1281, 581), (1282, 476), (1278, 407), (1253, 317), (1240, 269), (1231, 228)]
GR_D = [(0, 478), (250, 481), (437, 509), (569, 540), (650, 556), (656, 559), (811, 603), (917, 681), (900, 698), (889, 714), (883, 742), (883, 759), (869, 773), (833, 764), (750, 751), (714, 731),
        (700, 687), (661, 631), (572, 609), (561, 687), (553, 714), (533, 759), (511, 792), (503, 799), (406, 787), (375, 751), (350, 775), (300, 785), (269, 802), (238, 827), (200, 858), (165, 875),
        (131, 898), (85, 914), (63, 918), (52, 929), (58, 941), (77, 948), (123, 968), (129, 979), (112, 1002), (96, 1000), (50, 983), (23, 985), (27, 1002), (37, 1016), (23, 1027), (0, 1034)]
MO_B = [(1247, 200), (1917, 200), (1891, 241), (1867, 303), (1850, 359), (1843, 398), (1771, 365), (1674, 310), (1633, 286), (1467, 265), (1322, 234)]
MO_C = [(103, 937), (175, 942), (219, 956), (262, 981), (294, 1031), (295, 1040), (61, 1040), (62, 1031), (75, 1006), (100, 956)]
SF_A = [(1792, 698), (1920, 698), (1920, 1040), (1792, 1040)]
SF_C = [(42, 219), (62, 212), (100, 207), (125, 205), (150, 200), (652, 200), (696, 244), (727, 262), (752, 244), (796, 231), (846, 222), (890, 225), (915, 244), (940, 269), (990, 278), (1040, 281),
        (1077, 294), (1115, 284), (1152, 272), (1190, 266), (1202, 247), (1227, 237), (1252, 219), (1265, 200), (1293, 200), (1296, 400), (1300, 600), (1305, 720), (1308, 736), (1313, 780), (1313, 1040),
        (780, 1040), (700, 969), (650, 947), (609, 906), (587, 869), (569, 895), (462, 892), (337, 1040), (295, 1040), (294, 1031), (262, 981), (219, 956), (175, 942), (103, 937), (100, 956), (75, 1006),
        (62, 1031), (61, 1040), (0, 1040), (0, 578), (77, 577), (79, 383)]
FH_C = [(337, 1040), (462, 892), (569, 895), (587, 869), (609, 906), (650, 947), (700, 969), (780, 1040)]
FH_D = [(0, 200), (750, 200), (725, 217), (675, 250), (640, 280), (600, 317), (577, 353), (217, 349), (217, 240), (0, 240)]
SI = [(750, 200), (845, 200), (845, 292), (856, 306), (820, 332), (775, 387), (735, 435), (710, 472), (685, 520), (665, 550), (650, 557), (572, 541), (577, 353), (600, 317), (640, 280), (675, 250), (725, 217)]
OK = [(845, 200), (1023, 200), (1023, 311), (858, 310), (856, 306), (845, 292)]
SH = [(856, 306), (1025, 311), (1025, 600), (1033, 775), (978, 726), (917, 681), (811, 603), (656, 559), (650, 557), (665, 550), (685, 520), (710, 472), (735, 435), (775, 387), (820, 332)]
CA = [(572, 609), (661, 631), (700, 687), (714, 731), (750, 751), (833, 764), (869, 773), (883, 759), (883, 742), (889, 714), (900, 698), (917, 681), (978, 726), (1033, 775), (1033, 909), (1036, 1040),
      (1003, 1040), (1006, 998), (994, 959), (972, 942), (939, 928), (911, 909), (889, 887), (878, 870), (844, 858), (811, 853), (789, 848), (778, 837), (744, 828), (717, 823), (689, 809), (678, 795),
      (661, 787), (628, 798), (578, 837), (517, 884), (506, 853), (506, 799), (511, 792), (533, 759), (553, 714), (561, 687)]
# sold key, page slug, display name, [(frame, ring)]; earlier areas keep their ground where outlines overlap
AREAS = [
 ('Burnaby North|Vancouver Heights', 'vancouver-heights-burnaby', 'Vancouver Heights', [('A', VH)]),
 ('Burnaby North|Capitol Hill BN', 'capitol-hill-bn', 'Capitol Hill', [('A', CH)]),
 ('Burnaby North|Westridge BN', 'westridge-burnaby', 'Westridge', [('A', WR_A), ('C', WR_C)]),
 ('Burnaby North|Sperling-Duthie', 'sperling-duthie-burnaby', 'Sperling-Duthie', [('A', SD)]),
 ('Burnaby North|Willingdon Heights', 'willingdon-heights-burnaby', 'Willingdon Heights', [('A', WH)]),
 ('Burnaby North|Brentwood Park', 'brentwood-park', 'Brentwood Park', [('A', BP_A), ('B', BP_B1), ('B', BP_B2)]),
 ('Burnaby North|Parkcrest', 'parkcrest', 'Parkcrest', [('A', PC)]),
 ('Burnaby North|Central BN', 'central-bn', 'Central Burnaby', [('A', CB_A), ('B', CB_B)]),
 ('Burnaby North|Government Road', 'government-road', 'Government Road', [('B', GR_B), ('D', GR_D)]),
 ('Burnaby North|Montecito', 'montecito', 'Montecito', [('B', MO_B), ('C', MO_C)]),
 ('Burnaby North|Simon Fraser Univer.', 'simon-fraser-university-area-burnaby', 'Simon Fraser University', [('A', SF_A), ('C', SF_C)]),
 ('Burnaby North|Simon Fraser Hills', 'simon-fraser-hills-burnaby', 'Simon Fraser Hills', [('D', SI)]),
 ('Burnaby North|Forest Hills BN', 'forest-hills-bn', 'Forest Hills', [('C', FH_C), ('D', FH_D), ('BRIDGE', None)]),
 ('Burnaby North|Sullivan Heights', 'sullivan-heights-burnaby', 'Sullivan Heights', [('D', SH)]),
 ('Burnaby North|Cariboo', 'cariboo', 'Cariboo', [('D', CA)]),
 ('Burnaby North|Oakdale', 'oakdale', 'Oakdale', [('D', OK)]),
]
KX = 72700.0; KY = 111200.0   # metres per degree (lng, lat) at 49.26 N
def geoms():
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    out = []
    for key, slug, name, parts in AREAS:
        gs = []
        for fr, ring in parts:
            if fr == 'BRIDGE':   # Forest Hills, across the 0.5 km gap between frame C's bottom and frame D's top
                ring_ll = [FR['C'](337, 1040), FR['C'](780, 1040), FR['D'](750, 200), FR['D'](0, 200)]
            else:
                ring_ll = [FR[fr](x, y) for x, y in ring]
            g = Polygon([(lng * KX, lat * KY) for lat, lng in ring_ll])
            if not g.is_valid: g = g.buffer(0)
            gs.append(g)
        out.append((key, slug, name, unary_union(gs)))
    return out
def trimmed(rows):
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any overlap (under 15 ha) with an earlier one."""
    done = []; res = []
    for key, slug, name, g in rows:
        for h in done:
            if g.intersects(h) and g.intersection(h).area < 150000: g = g.difference(h)
        done.append(g); res.append((key, slug, name, g))
    return res
def main():
    if '--check' in sys.argv:
        for k in 'ABCD':
            used = LAND[k]; print(k, 'residuals (label, m north, m east):', residuals(used, FR[k]))
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    areas = []; pts = []
    for key, slug, name, g in trimmed(geoms()):
        assert key in sold, key
        polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
        rings = []
        for p in sorted(polys, key=lambda p: -p.area):
            if p.area < 3000: continue   # sub-hectare crumbs left by trimming
            r = [[round(y / KY, 5), round(x / KX, 5)] for x, y in list(p.exterior.coords)[:-1]]; r.append(r[0]); rings.append(r); pts += r
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'burnaby', 'name': 'Burnaby', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), separators=(',', ':')); print('burnaby north', len(areas), 'areas', bbox, '->', OUT)
if __name__ == '__main__': main()
