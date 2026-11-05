"""Draft outlines for four Maple Ridge / Pitt Meadows sub-areas, ADDED to the existing maps
src/data/maps/maple-ridge.json (Northeast, Silver Valley, Websters Corners) and src/data/maps/pitt-meadows.json (North Meadows PI).

Source: Jared's Paragon map search, GVR Sub Areas layer with its labels switched on (codes NE, SV, WB, NM), screenshots of 2026-11-05 in
Closeups/MapleRidge-PittMeadows-NorthDelta (03_maple_ridge_north_rural.jpg) and Paragon-Sub-Area-Boundaries/screenshots/3-MapleRidge-PittMeadows
(02-closeup.webp, 01-overview.webp).  Code -> name from Closeups/GVR-code-names.csv (all four CONFIRMED).
Frames, all read in "frame B" pixels (= 03_maple_ridge_north_rural.jpg, 1920 px wide, about 12.5 m per pixel):
  * 02-closeup.webp is the same zoom as frame 03 panned 302 px west (SIFT, used only for context here);
  * 01-overview.webp is exactly half that zoom (checked on the NO, Websters Corners and Cottonwood corners): overview-upscaled-to-1920 pixel (x, y) = frame B pixel
    ((x + 1264) / 2, (y + 696) / 2), written O(x, y) below.  It reaches about 5 km further north than frame 03 and supplies the north ends of Silver Valley, Websters
    Corners, Northeast and North Meadows.
Calibration: frames 04 + 01 + 02 of the closeup set are the same zoom (3.13 m per pixel), registered by SIFT, and fitted (Web Mercator, longitude vs x, Mercator
latitude vs y) to eight Google Maps landmarks (Ridge Meadows Hospital, Pitt Meadows Family Recreation Centre, Pitt Meadows Secondary, Maple Ridge Secondary, Golden Ears
Elementary, Thomas Haney School, Pazarena Park, Kanaka Creek Park Fish Fence); the fit misses them by 5 m at worst.  Frame B is four times lower zoom, so it is tied to
that mosaic by four boundary / road corners seen in both (the Lougheed Hwy bend, the West Central / East Central corner on the Fraser, the Cottonwood north-west
corner and the Cottonwood / Albion / Thornhill junction; shared-feature misfit 7 px of the close zoom = about 22 m).  Landmark icons were NOT used on frame B: Google
nudges icons at lower zoom (the hospital H sits 120 m off its true spot there).  Overall these outlines are good to about 100 m on straight edges and 100 to 300 m
on river banks and bush edges (the Pitt River bank, the Alouette / Kanaka boundary lines).
Clipped on purpose, because the screenshots stop there: Silver Valley, Websters Corners, Northeast and North Meadows all run on north past the top of the
overview screenshot (about 49.30 N), so each is drawn up to that edge (a flat top, not a real boundary).  North Meadows is the whole lavender block between the Pitt River,
Hwy 7 and Silver Valley.  Not drawn: Whonnock, Thornhill and the other Maple Ridge / Pitt Meadows areas already in the files (left exactly as they were).
The Paragon boundaries shared by neighbours (Silver Valley / Websters Corners, Websters Corners / Northeast, North Maple Ridge / Silver Valley / North Meadows) use one vertex
list each, then every new area is trimmed against the areas already in the file so slivers do not overlap; --check prints every overlap with an existing neighbour and
only slivers (under 3 percent of the new area) are cut.  Every area stays 'draft'.  Re-running replaces these four areas and touches nothing else.
  python3 -I tools/build_maple_ridge_pitt_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# mosaic A (frames 04, 01, 02 registered to frame 01; pixel, pixel, lat, lng)
LAND = [(237, 825, 49.2155103, -122.6300219), (-1193, 637, 49.2207858, -122.6913766), (-1001, 874, 49.2141378, -122.6831491), (583, 477, 49.225267, -122.615205),
        (1369, 819, 49.215732, -122.5814371), (1365, 953, 49.211981, -122.5815976), (1299, 1122, 49.2071951, -122.5844236), (1902, 1396, 49.1995063, -122.5585031)]
# the same features read in mosaic A and in frame B (A px, B px)
TIE = [((771, 788), (603, 736)), ((897, 982), (636, 786)), ((1421, 666), (768.5, 706)), ((2465, 1253), (1029, 851))]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def llA(px, py): return math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), LX * px + LB
_Bm = [sum(t[1][i] for t in TIE) / len(TIE) for i in (0, 1)]; _Am = [sum(t[0][i] for t in TIE) / len(TIE) for i in (0, 1)]
S = sum((t[1][i] - _Bm[i]) * (t[0][i] - _Am[i]) for t in TIE for i in (0, 1)) / sum((t[1][i] - _Bm[i]) ** 2 for t in TIE for i in (0, 1))
TX = _Am[0] - S * _Bm[0]; TY = _Am[1] - S * _Bm[1]
def ll(bx, by):
    lat, lng = llA(S * bx + TX, S * by + TY); return round(lat, 5), round(lng, 5)
def O(x, y): return ((2 * x - 1264), (2 * y - 696))          # overview (upscaled to 1920) pixel -> frame B pixel
def residuals():
    la = [(round((llA(p[0], p[1])[0] - p[2]) * 111200), round((llA(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
    tie = [(round(S * b[0] + TX - a[0]), round(S * b[1] + TY - a[1])) for a, b in TIE]
    return la, tie
# ---------------- shared boundary vertex lists (frame B pixels) ----------------
XW = 642                                                                      # Silver Valley / North Maple Ridge / North Meadows line
SVWB = [O(1408, 285), O(1406, 293), O(1400, 310), O(1387, 322), O(1367, 337), O(1346, 358), O(1331, 366), O(1308, 385), O(1294, 400), O(1281, 406), O(1283, 422),
        O(1275, 435), O(1258, 443), O(1237, 460), O(1212, 477), O(1208, 489), O(1200, 502), (1136, 340), (1134, 346), (1119, 365), (1075, 399), (1056, 421), (1019, 474),
        (1031, 503), (994, 518), (975, 537), (944, 571), (931, 593), (897, 609)]                    # top -> bottom, Silver Valley on the west
WBNE = [O(1510, 285), O(1475, 318), O(1450, 347), O(1425, 377), O(1400, 410), O(1375, 439), (1353, 400), (1350, 520), (1350, 600), (1353, 641), (1334, 669), (1331, 706),
        (1319, 722), (1319, 747), (1316, 765)]                                                   # top -> bottom, Websters Corners on the west
# ---------------- polygons ----------------
SV = [O(954, 285)] + SVWB + [(881, 585), (870, 570), (850, 550), (819, 537), (780, 525), (765, 509), (750, 509), (XW, 508), (XW, 392), (XW, 314), (586, 314), (586, 248), (XW, 208)]
WB = [SVWB[0]] + WBNE + [(1313, 793), (1300, 808), (1298, 817), (1287, 820), (1288, 828), (1279, 838), (1275, 845), (1261, 846), (1260, 840), (1243, 830), (1236, 822),
                          (1236, 817), (1230, 810), (1220, 798), (1212, 791), (1187, 784), (1150, 781), (1125, 780), (1118, 780), (1100, 786), (1089, 794), (1079, 794), (1073, 783),
                          (1068, 780), (1044, 779), (1029, 777), (1028, 706), (897, 706), (897, 609)] + SVWB[::-1][1:-1]
NE = [WBNE[0], (1768, -126), (1768, 314), (1678, 314), (1678, 708), (1457, 708), (1457, 750), (1412, 750), (1409, 752), (1381, 756), (1344, 761), (1316, 765)] + WBNE[::-1][1:-1]
NM = ([O(739, 285), O(954, 285), (XW, 208), (586, 248), (586, 314), (XW, 314), (XW, 392), (518, 386), (518, 442), (387, 436), (387, 508), (320, 510), (320, 603), (266, 603), (266, 696)]
      + [O(660, 637), O(583, 581), O(589, 576), O(605, 560), O(621, 541), O(627, 516), O(643, 485), O(658, 460), O(674, 441), O(696, 426), O(718, 413), O(743, 405), O(768, 402),
         O(780, 391), O(793, 376), O(788, 357), O(780, 343), O(755, 332), O(743, 313)])
AREAS = {'maple-ridge': [('northeast', 'Northeast', 'Maple Ridge|Northeast', [NE]), ('silver-valley', 'Silver Valley', 'Maple Ridge|Silver Valley', [SV]),
                         ('websters-corners', 'Websters Corners', 'Maple Ridge|Websters Corners', [WB])],
         'pitt-meadows': [('north-meadows-pitt-meadows', 'North Meadows', 'Pitt Meadows|North Meadows PI', [NM])]}
def proj(r): return [(lng * 0.6537, lat) for lat, lng in r]          # planar-ish (cos 49.2 deg) for area tests
def poly(r):
    from shapely.geometry import Polygon
    g = Polygon(proj(r))
    return g if g.is_valid else g.buffer(0)
def build(region, name, check):
    from shapely.geometry import Polygon
    path = os.path.join(ROOT, f'src/data/maps/{region}.json'); data = json.load(open(path)); sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    mine = {a[0] for a in AREAS[region]}; data['areas'] = [a for a in data['areas'] if a['id'] not in mine]
    others = [(a['id'], poly(a['rings'][0])) for a in data['areas']]
    # neighbours drawn in the other region's file (the Pitt Meadows / Maple Ridge border area) also count for the clash report
    other_region = 'pitt-meadows' if region == 'maple-ridge' else 'maple-ridge'
    for a in json.load(open(os.path.join(ROOT, f'src/data/maps/{other_region}.json')))['areas']:
        if a['id'] not in {x[0] for x in AREAS[other_region]}: others.append((a['id'] + ' (' + other_region + ')', poly(a['rings'][0])))
    done = []; pts = []; new = []
    for slug, nm, key, rings in AREAS[region]:
        assert key in sold, key
        rr = []
        for ring in rings:
            r = [ll(x, y) for x, y in ring]; g = poly(r)
            for oid, h in others + done:
                if g.intersects(h):
                    ia = g.intersection(h).area
                    if check: print(f'  {slug} overlaps {oid}: {100 * ia / g.area:.1f}% of {slug} ({ia * 111.2 * 111.2:.1f} km2)')
                    if ia < 0.03 * g.area: g = g.difference(h)
            done.append((slug, g))
            gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
            rl = [(round(y, 5), round(x / 0.6537, 5)) for x, y in list(gg.exterior.coords)]
            if rl[0] != rl[-1]: rl.append(rl[0])
            rr.append([list(p) for p in rl]); pts += rl
        new.append({'id': slug, 'name': nm, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rr})
    data['areas'] += new
    allp = [p for a in data['areas'] for rg in a['rings'] for p in rg]
    pad = 0.004; bbox = [round(min(p[0] for p in allp) - pad, 4), round(min(p[1] for p in allp) - pad, 4), round(max(p[0] for p in allp) + pad, 4), round(max(p[1] for p in allp) + pad, 4)]
    data['bbox'] = bbox; data['center'] = {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
    json.dump(data, open(path, 'w'), separators=(',', ':')); print(region, len(data['areas']), 'areas', bbox)
def main():
    check = '--check' in sys.argv
    if check: print('landmark residuals (m north, m east):', residuals()[0], '| tie misfit (px of mosaic A):', residuals()[1], '| scale B->A', round(S, 3))
    build('maple-ridge', 'Maple Ridge', check); build('pitt-meadows', 'Pitt Meadows', check)
if __name__ == '__main__': main()
