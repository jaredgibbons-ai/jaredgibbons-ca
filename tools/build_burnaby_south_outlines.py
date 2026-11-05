"""Draft outlines for Burnaby South + Burnaby East (GVR layer, two-letter codes) -> PART file (the lead merges it into src/data/maps/burnaby.json)

Source: Jared's Paragon map search (GVR sub-area layer), six Burnaby screenshots of 2026-11-05 (src: Paragon-Sub-Area-Boundaries/screenshots/10-Burnaby).  Codes read
(GVR-code-names.csv): BH Burnaby Hospital, GT Greentree Village, GV Garden Village, DP Deer Lake Place, DL Deer Lake, FG Forest Glen BS, CP Central Park BS, OL Oaklands,
UD Upper Deer Lake, BL Burnaby Lake, ME Metrotown, HG Highgate, SC Suncrest, SS South Slope, BB Big Bend, ED Edmonds BE, BE East Burnaby, CR The Crest (code unconfirmed).
Three frames (south-metrotown, central-deer-lake, southeast-edmonds) are the same zoom panned around; they were registered to the Metrotown frame by SIFT matching
(shift (x, y) in OFF below, full-screenshot pixels, frame pixel + shift = mosaic pixel) and read off one mosaic.  The Lougheed frame (burnaby-east-lougheed-coquitlam-west)
overlaps none of them; it is the same zoom (3.13 m per pixel, confirmed from four landmarks) and has its own fit; The Crest and the east end of Burnaby Lake are read on it and
combined with the mosaic in latitude/longitude.  The other two frames (north-capitol-hill, east-sfu) show none of these areas.
Calibration: mosaic = ten landmark icons (Swangard Stadium, Bonsor Recreation Complex, Burnaby Village Museum, Clinton Elementary, Burnaby City Hall, Burnaby Hospital,
Burnaby Central Secondary, Marlborough Elementary, Deer Lake School, St. Thomas More Collegiate) from Google Maps, worst miss 6 m.  Lougheed frame = four landmarks (Cariboo Dam,
Revive City Church, Seaforth Elementary, Lougheed Town Centre station) whose coordinates are OpenStreetMap (Nominatim), because Google Maps put every browser session behind a
CAPTCHA while this was being drawn; worst miss 36 m (the station node, the other three are within 16 m).  Edges read off the screenshots are good to about 100 m on straight roads.
Clipped on purpose (the screenshots stop there): East Burnaby (top and right edges of the Edmonds frame), Highgate (top edge), Upper Deer Lake (right edge of the Metrotown frame and
top edge of the Edmonds frame), Deer Lake (east side runs past the Metrotown frame), Burnaby Lake (bottom edges of the Central and Lougheed frames, so its south side is cut), The Crest (bottom of the Lougheed
frame), South Slope and Big Bend (left edge of the Edmonds frame; Big Bend also its bottom edge).  Inferred beyond the frames: the Boundary Rd edge of Burnaby Hospital (46 px off the left of the
Central frame, straight road) and the Rumble St edge of Suncrest and Metrotown (40 px below the Metrotown frame; the street is seen at the same height further east).
Not drawn: Buckingham Heights (no code and no polygon seen on any frame).  Every area stays 'draft'.
  python3 -I tools/build_burnaby_south_outlines.py [--check]"""
import json, math, os, sys
import os, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(tempfile.gettempdir(), 'outline-parts', 'burnaby-south.part.json')   # scratch part file; tools/merge_city_outlines.py merges the parts
LAND = [(633, 490, 49.2308474, -123.0214483), (1217, 729, 49.2241922, -122.9964086), (1928, 187, 49.2393853, -122.9658755), (1648, 1135, 49.2127617, -122.9779668),
        (1760, 46, 49.243335, -122.9730257), (763, -182, 49.2497113, -123.0158866), (1723, 45, 49.2433009, -122.9747465), (1300, 560, 49.2289135, -122.9928665),
        (1524, 114, 49.2414337, -122.9832758), (2566, 1050, 49.2151708, -122.9384946)]
LANDL = [(466, 690, 49.2479199, -122.9169521), (655, 815, 49.2443704, -122.9088126), (18, 543, 49.2519051, -122.9361017), (933, 684, 49.2484558, -122.8968482)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def mk(L):
    LX, LB = ls([p[0] for p in L], [p[3] for p in L]); MY, MB = ls([p[1] for p in L], [merc(p[2]) for p in L])
    def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
    return ll
ll = mk(LAND); llL = mk(LANDL)
def residuals(L, f): return [(round((f(p[0], p[1])[0] - p[2]) * 111200), round((f(p[0], p[1])[1] - p[3]) * 73000)) for p in L]
# frame pixel + OFF = mosaic pixel (reference = the Metrotown frame); the mosaic covers x -50..3098, y -556..1584 (y 200..1038 of each frame is map)
OFF = {'south-metrotown': (0, 0), 'central-deer-lake': (630, -756), 'southeast-edmonds': (1128, 546)}
# --- polygons in mosaic pixels ---
BH = [(584, -344), (1032, -344), (1032, -236), (1036, -156), (1050, -106), (1055, -36), (1055, 72), (584, 72)]
GT = [(1032, -344), (1330, -334), (1370, -328), (1387, -311), (1392, -256), (1391, -195), (1391, 186), (1372, 175), (1330, 155), (1285, 137), (1230, 125), (1160, 118), (1100, 100),
      (1056, 75), (1055, 72), (1055, -36), (1050, -106), (1036, -156), (1032, -236)]
GV = [(765, 72), (1055, 72), (1055, 287), (765, 287)]
CP = [(584, 72), (765, 72), (765, 287), (1055, 287), (1056, 474), (1022, 525), (841, 441), (843, 822), (584, 822)]
FG = [(1055, 72), (1056, 75), (1100, 100), (1160, 118), (1230, 125), (1285, 137), (1330, 155), (1372, 175), (1391, 186), (1402, 300), (1415, 378), (1411, 403), (1407, 435), (1400, 489),
      (1394, 537), (1507, 548), (1584, 566), (1584, 805), (1494, 764), (1394, 717), (1200, 614), (1022, 525), (1056, 474)]
OL = [(1415, 378), (1468, 382), (1500, 398), (1541, 421), (1564, 448), (1571, 466), (1572, 502), (1525, 502), (1507, 516), (1507, 548), (1394, 537), (1400, 489), (1407, 435), (1411, 403)]
DP = [(1391, -195), (1430, -176), (1535, -178), (1590, -146), (1640, -96), (1690, -56), (1725, -16), (1735, 34), (1715, 94), (1680, 144), (1640, 174), (1580, 187), (1480, 190), (1391, 186)]
DL = [(1391, 186), (1480, 190), (1580, 187), (1640, 174), (1680, 144), (1715, 94), (1735, 34), (1725, -16), (1750, 0), (1800, 40), (1845, 80), (1872, 110), (2155, 284), (1921, 284),
      (1921, 557), (1850, 555), (1850, 486), (1794, 486), (1798, 370), (1750, 355), (1700, 352), (1663, 344), (1654, 330), (1630, 292), (1540, 262), (1480, 217)]
UD = [(1391, 186), (1480, 217), (1540, 262), (1630, 292), (1654, 330), (1663, 344), (1700, 352), (1750, 355), (1798, 370), (1794, 486), (1850, 486), (1850, 555), (1921, 557), (1921, 746),
      (2135, 746), (2090, 793), (2045, 819), (1618, 819), (1584, 805), (1584, 566), (1507, 548), (1507, 516), (1525, 502), (1572, 502), (1571, 466), (1564, 448), (1541, 421), (1500, 398),
      (1468, 382), (1415, 378), (1402, 300)]
HG = [(1618, 819), (2045, 819), (2090, 793), (2135, 746), (2500, 746), (2100, 1098), (2058, 1068), (2040, 1080), (1787, 1078), (1785, 893), (1768, 886), (1723, 870), (1650, 836)]
ME = [(841, 441), (1022, 525), (1200, 614), (1394, 717), (1494, 764), (1584, 805), (1618, 819), (1650, 836), (1723, 870), (1768, 886), (1785, 893), (1787, 1078), (845, 1078), (843, 822)]
SC = [(584, 822), (843, 822), (845, 1078), (584, 1078)]
SS = [(1128, 1078), (1787, 1078), (2040, 1080), (2058, 1068), (2100, 1098), (2140, 1150), (2190, 1200), (2215, 1250), (2225, 1290), (2232, 1350), (2250, 1397), (2185, 1445), (2100, 1530),
      (2065, 1560), (2040, 1530), (1950, 1480), (1860, 1450), (1780, 1432), (1700, 1425), (1645, 1412), (1600, 1390), (1500, 1378), (1400, 1365), (1300, 1358), (1200, 1335), (1128, 1318)]
BB = [(1128, 1318), (1200, 1335), (1300, 1358), (1400, 1365), (1500, 1378), (1600, 1390), (1645, 1412), (1700, 1425), (1780, 1432), (1860, 1450), (1950, 1480), (2040, 1530), (2065, 1560),
      (2045, 1584), (1128, 1584)]
ED = [(2500, 746), (2520, 746), (2560, 790), (2620, 850), (2680, 925), (2715, 1000), (2250, 1397), (2232, 1350), (2225, 1290), (2215, 1250), (2190, 1200), (2140, 1150), (2100, 1098)]
BE = [(2520, 746), (3046, 746), (2832, 930), (2715, 1000), (2680, 925), (2620, 850), (2560, 790)]
# Burnaby Lake: mosaic part (west end, down the lake's west shore, then along its south shore to the Central frame's right edge) + Lougheed-frame part (east end)
BL_M1 = [(1913, -175), (2075, -172), (2105, -174), (2055, -155), (2045, -110), (2048, -70), (2065, -20), (2080, -12), (2120, -2), (2140, 55), (2205, 110), (2250, 145), (2300, 170), (2400, 195), (2545, 198)]
BL_L = [(0, 1035), (18, 1030), (30, 1026), (36, 1015), (26, 1006), (26, 994), (17, 991), (26, 984), (36, 983), (48, 983), (111, 1005), (117, 1003), (129, 976), (127, 965), (91, 953),
        (56, 941), (53, 929), (65, 917), (91, 913), (121, 903), (152, 888), (194, 862), (212, 848), (239, 827), (279, 800), (323, 783), (377, 752), (404, 788), (492, 798), (504, 800),
        (504, 860), (512, 883), (492, 906), (415, 983), (362, 1035), (0, 1038)]
BL_M2 = [(2550, 284), (2155, 284), (1872, 110), (1885, 85), (1900, -5), (1910, -100), (1913, -175)]
CR_L = [(668, 791), (700, 805), (738, 829), (815, 852), (885, 875), (954, 929), (992, 960), (1004, 1014), (1000, 1038), (358, 1038), (362, 1035), (415, 983), (492, 906), (512, 885), (538, 868),
        (592, 825)]
# (sold key, page slug, name, [(pixel ring, fit)])
AREAS = [
 ('Burnaby South|Burnaby Hospital', 'burnaby-hospital', 'Burnaby Hospital', [(BH, ll)]),
 ('Burnaby South|Greentree Village', 'greentree-village', 'Greentree Village', [(GT, ll)]),
 ('Burnaby South|Garden Village', 'garden-village', 'Garden Village', [(GV, ll)]),
 ('Burnaby South|Central Park BS', 'central-park-bs', 'Central Park', [(CP, ll)]),
 ('Burnaby South|Forest Glen BS', 'forest-glen-bs', 'Forest Glen', [(FG, ll)]),
 ('Burnaby South|Oaklands', 'oaklands-burnaby', 'Oaklands', [(OL, ll)]),
 ('Burnaby South|Deer Lake Place', 'deer-lake-place', 'Deer Lake Place', [(DP, ll)]),
 ('Burnaby South|Deer Lake', 'deer-lake', 'Deer Lake', [(DL, ll)]),
 ('Burnaby South|Upper Deer Lake', 'upper-deer-lake-burnaby', 'Upper Deer Lake', [(UD, ll)]),
 ('Burnaby South|Highgate', 'highgate-burnaby', 'Highgate', [(HG, ll)]),
 ('Burnaby South|Metrotown', 'metrotown-homes-for-sale', 'Metrotown', [(ME, ll)]),
 ('Burnaby South|Suncrest', 'suncrest-burnaby', 'Suncrest', [(SC, ll)]),
 ('Burnaby South|South Slope', 'south-slope-burnaby', 'South Slope', [(SS, ll)]),
 ('Burnaby South|Big Bend', 'big-bend', 'Big Bend', [(BB, ll)]),
 ('Burnaby East|Edmonds BE', 'edmonds-be', 'Edmonds', [(ED, ll)]),
 ('Burnaby East|East Burnaby', 'east-burnaby', 'East Burnaby', [(BE, ll)]),
 ('Burnaby South|Burnaby Lake', 'burnaby-lake', 'Burnaby Lake', [(BL_M1, ll), (BL_L, llL), (BL_M2, ll)]),   # one ring: the three pieces are joined in order
 ('Burnaby East|The Crest', 'the-crest', 'The Crest', [(CR_L, llL)]),
]
SQ = 4000 * (3.13 ** 2)     # an overlap smaller than this (m2, about 4 ha) between two hand-read outlines is trimmed off the later one
def ring_ll(pieces):
    r = []
    for ring, f in pieces: r += [list(f(x, y)) for x, y in ring]
    return r
def trimmed(rows):
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any small overlap with an earlier one (metric space)."""
    from shapely.geometry import Polygon
    k = (73000.0, 111200.0)
    done = []; out = []
    for key, slug, name, pieces in rows:
        r = ring_ll(pieces)
        g = Polygon([(p[1] * k[0], p[0] * k[1]) for p in r])
        if not g.is_valid: g = g.buffer(0)
        for h in done:
            if g.intersects(h) and g.intersection(h).area < SQ: g = g.difference(h)
        done.append(g)
        gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
        out.append((key, slug, name, [[round(y / k[1], 5), round(x / k[0], 5)] for x, y in list(gg.exterior.coords)[:-1]]))
    return out
def main():
    if '--check' in sys.argv: print('mosaic residuals (m north, m east):', residuals(LAND, ll), '| Lougheed frame:', residuals(LANDL, llL))
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    pts = []; areas = []
    for key, slug, name, ring in trimmed(AREAS):
        r = list(ring); r.append(r[0]); pts += r
        assert key in sold, key
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': [r]})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'burnaby', 'name': 'Burnaby', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), separators=(',', ':')); print('burnaby part', len(areas), 'areas', bbox, '->', OUT)
if __name__ == '__main__': main()
