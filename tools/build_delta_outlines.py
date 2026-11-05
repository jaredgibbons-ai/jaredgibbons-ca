"""Draft outlines for the Tsawwassen and Ladner areas that were still undrawn -> ADDED to src/data/maps/delta.json (additive and idempotent).

Source: Jared's Paragon map search (GVR sub-area layer, codes BB CD BG CT PH TE EB TN PG LA EA), Delta closeups of 2026-11-05:
  Tsawwassen: five 2x frames (TN-north, CD-BG, CT, PH-TE-EB, BB; registered by SIFT, shifts in T_OFF) plus the two 1x frames Overview and TN-2 (TN-2 is the Overview shifted
  419 px) which show the north end (Deltaport Way) that the 2x frames cut off.  1x pixel (x, y in Overview coordinates) = 2x mosaic pixel ((x*2)-960, (y*2)-420); the TN polygon is read at 1x.
  Ladner: Ladner-1 and Ladner-HO-1 (2x, registered, HO-1 + (957, 0) = Ladner-1) for Port Guichon and the north edge of Ladner Rural; the Paragon 02-ladner-tsawwassen screenshot ("02" below,
  about 19 m per pixel, 6 times coarser than Ladner-1) for the whole of East Delta and the south of Ladner Rural.  East Delta's north rim (stepped Tilbury edge) is only on the 01 overview, which is
  clipped into 02 pixels with x02 = 2.06*x01 - 694.3, y02 = 2.06*y01 - 503.6 (two tie points: the Tilbury corner and the Hwy 99/91 tip), so that rim is good to about 200 m.
Calibration (pixel -> lat/lng, Web Mercator linear fit as in build_chilliwack_outlines.py):
  Tsawwassen mosaic: 15 landmarks, OpenStreetMap coordinates (Nominatim) matched to the Google icon positions in the frames: Fred Gingell Park, Pebble Hill Park, Tsawwassen Tennis Club,
  Southpointe Academy, South Delta Recreation Centre, Beach Grove Park, St David's Anglican Church, Benediction Lutheran Church, Ecole du Bois-Joli, South Delta Secondary School, Osprey Park,
  Tsawwassen First Nation Longhouse, Boardwalk Salmon Park, Monument Park, Boundary Beach Park Reserve (about 2.8 m per pixel).  English Bluff Elementary and Pebble Hill Elementary were dropped
  (school-site centroids 80 to 95 m from the icons).  Google Maps was not usable for the landmark lookups (it served a robot check to every agent), so OSM stood in; centroids of big parks and school
  sites sit up to ~60 m from Google's icons, which is the residual seen with --check.  The Canada-US border line in the screenshots is NOT used as 49.000 N (it sits ~160 m north of that on this map).
  Ladner mosaic: 9 landmarks (Delta Secondary, Ladner Leisure Centre, Hawthorne Elementary, Kirkland Mini Park, Port Guichon Elementary, Ladner Christian Reformed Church, Hawthorne Park,
  Delta Manor Education Centre, Ladner Elementary), worst residual about 85 m (school and park centroids, not the fit); Wellington Point Park was dropped (200 m).
  Screenshot 02: tied to the Ladner fit at the Ladner Trunk Rd / 17A corner (the corner of Hawthorne, Holly and Delta Manor) and to the Surrey West Newton corner (120 St and 64 Ave, taken from
  src/data/maps/surrey.json) for the scale; checked against the Gulf of Georgia Cannery and London Farm (60 m and 20 m east-west, 120 to 195 m north-south because those are pin tips).
Not drawn: Westham Island, Tilbury (TB), Tilbury/Annacis.  Clipped where the screenshots stop: none of the drawn areas is cut off.  Every area stays 'draft'.
  python3 -I tools/build_delta_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'src/data/maps/delta.json')
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
def mk(L):
    LX, LB = ls([p[0] for p in L], [p[3] for p in L]); MY, MB = ls([p[1] for p in L], [merc(p[2]) for p in L])
    def ll(px, py): return math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), LX * px + LB
    return ll
def residuals(L, f): return [(p[4], round((f(p[0], p[1])[0] - p[2]) * 111200), round((f(p[0], p[1])[1] - p[3]) * 73000)) for p in L]
# (mosaic x, y, lat, lng, name)
T_LAND = [(758, 778, 49.0076116, -123.0910523, 'Fred Gingell Park'), (964, 716, 49.0086751, -123.0815175, 'Pebble Hill Park'), (813, 766, 49.0081125, -123.0888219, 'Tsawwassen Tennis Club'),
          (1281, -272, 49.0371552, -123.0680138, 'Southpointe Academy'), (1311, -208, 49.0355524, -123.0664735, 'South Delta Recreation Centre'), (1538, -197, 49.0355649, -123.0559306, 'Beach Grove Park'),
          (989, 233, 49.023059, -123.0804804, "St David's Anglican"), (1252, 551, 49.0140144, -123.0692319, 'Benediction Lutheran'), (801, 437, 49.0172007, -123.0891095, 'Ecole du Bois-Joli'),
          (1093, 456, 49.0164159, -123.0755008, 'South Delta Secondary'), (684, -207, 49.0351722, -123.0935138, 'Osprey Park'), (524, -436, 49.0416567, -123.1006527, 'TFN Longhouse'),
          (404, -647, 49.0477272, -123.1058317, 'Boardwalk Salmon Park'), (776, 976, 49.0015196, -123.0896167, 'Monument Park'), (1873, 942, 49.00287, -123.04257, 'Boundary Beach Park Reserve')]
T_DROPPED = [(789, 681, 49.0106649, -123.0880034, 'English Bluff Elementary'), (1047, 795, 49.007057, -123.0765797, 'Pebble Hill Elementary')]
L_LAND = [(911, 564, 49.0862938, -123.0848662, 'Delta Secondary'), (1498, 534, 49.0863292, -123.0583847, 'Ladner Leisure Centre'), (1186, 187, 49.096863, -123.071304, 'Hawthorne Elementary'),
          (966, 748, 49.0804977, -123.0816056, 'Kirkland Mini Park'), (581, 656, 49.0836502, -123.0982146, 'Port Guichon Elementary'), (1192, 550, 49.0861192, -123.0717462, 'Ladner CRC'),
          (1257, 177, 49.09646, -123.06889, 'Hawthorne Park'), (1353, 436, 49.08858, -123.06421, 'Delta Manor Education Centre'), (897, 676, 49.08211, -123.08568, 'Ladner Elementary')]
llT = mk(T_LAND); llL = mk(L_LAND)
# screenshot 02: scale from the Ladner corner (563.8, 471) and Surrey's 120 St / 64 Ave corner (1211, 298.5) = (49.11874, -122.88952) in surrey.json
_A = llL(1537, 415); _S = (-122.88952 - _A[1]) / (1211 - 563.8)
def ll02(x, y):
    m = merc(_A[0]) - (y - 471) * _S * math.pi / 180
    return math.degrees(2 * math.atan(math.exp(m)) - math.pi / 2), _A[1] + (x - 563.8) * _S
def llL_from02(x, y): return llL(6.0 * x - 1845.8, 6.0 * y - 2411)   # not used for output; kept for the check
def c1x(pts): return [(2 * x - 960, 2 * y - 420) for x, y in pts]
def c01(pts): return [(2.06 * x - 694.3, 2.06 * y - 503.6) for x, y in pts]
# ---------------- Tsawwassen (2x mosaic pixels = CT frame pixels) ----------------
T_OFF = {'CD-BG': (0, -420), 'TN-north': (0, -839), 'PH-TE-EB': (0, 419), 'BB': (957, 419)}
TN_1X = [(636, -317), (1245, -317), (1246, -270), (1239, -180), (1217, -124), (1167, -64), (1130, -30), (1111, -14), (1042, 45), (981, 76), (981, 226), (854, 266), (800, 277), (760, 285), (744, 290),
         (730, 270), (720, 251), (730, 214), (739, 176), (749, 145), (755, 126), (742, 108), (711, 89), (686, 70), (658, 39), (642, -17), (627, -61), (614, -89), (605, -102), (574, -121),
         (542, -136), (511, -149), (510, -180), (520, -211), (555, -249), (605, -292)]
TN = c1x(TN_1X)
BG = [(1530, -1054), (1790, -1054), (1798, -621), (1804, -567), (1800, -542), (1771, -508), (1733, -462), (1704, -417), (1687, -375), (1677, -308), (1668, -250), (1654, -200), (1629, -133),
      (1592, -67), (1567, -17), (1550, 50), (1548, 79), (1575, 125), (1617, 167), (1654, 192), (1263, 190), (1262, -448), (1300, -480), (1374, -548), (1474, -668), (1518, -780), (1532, -960)]
CD = [(1002, -268), (1124, -330), (1262, -448), (1263, 185), (750, 185), (748, 112), (1004, 33)]
CT = [(750, 185), (1262, 185), (1262, 577), (735, 577), (722, 500), (745, 455), (750, 440)]
TE = [(1263, 190), (1505, 190), (1508, 300), (1523, 380), (1538, 420), (1540, 719), (1548, 989), (1263, 989)]
BB = [(1505, 190), (1650, 194), (1700, 226), (1750, 262), (1830, 318), (1900, 375), (1937, 419), (1949, 489), (1967, 539), (1987, 589), (2005, 649), (2022, 719), (2035, 779), (2045, 839), (2045, 889),
      (2046, 989), (1548, 989), (1540, 719), (1538, 420), (1523, 380), (1508, 300)]
PH = [(733, 579), (1262, 579), (1262, 991), (797, 991), (790, 899), (780, 839), (775, 759), (770, 719), (748, 634)]
EB = [(748, 112), (700, 126), (640, 138), (580, 148), (545, 150), (528, 162), (526, 200), (535, 260), (545, 310), (556, 316), (580, 345), (600, 395), (612, 420), (640, 499), (670, 589), (700, 669),
      (712, 719), (715, 800), (716, 859), (730, 919), (747, 989), (797, 991), (790, 899), (780, 839), (775, 759), (770, 719), (748, 634), (733, 579), (735, 577), (722, 500), (745, 455), (750, 440), (750, 185)]
# ---------------- Ladner (Ladner-1 mosaic pixels) and screenshot 02 ----------------
PG = [(656.8, 437), (609, 462), (564, 487), (518, 505), (473, 525), (427, 544), (391, 559), (354, 576), (341, 582), (339, 600), (339, 621), (354, 623), (400, 621), (427, 605), (459, 594), (482, 598),
      (527, 619), (527, 680), (650, 684), (654.5, 682)]
PG_I1 = [(400, 355), (382, 369), (355, 394), (332, 416), (320, 432), (307, 453), (291, 471), (245, 482), (243, 489), (264, 494), (305, 482), (350, 478), (391, 469), (423, 450), (432, 414), (455, 407),
         (482, 375), (487, 374), (473, 387), (441, 396), (418, 394), (400, 382)]
PG_I2 = [(584, 355), (577, 371), (559, 394), (546, 414), (527, 426), (491, 437), (482, 453), (486, 466), (500, 471), (518, 462), (546, 446), (573, 430), (586, 414), (586, 380), (585, 357)]
# mixed rings: ('L', x, y) Ladner-1 pixels, ('2', x, y) screenshot-02 pixels
def L(pts): return [('L', x, y) for x, y in pts]
def S2(pts): return [('2', x, y) for x, y in pts]
LA = (S2([(301.4, 501.4), (304.5, 498.6), (326, 499.5), (350, 500.6)]) +
      L([(341, 582), (339, 600), (339, 621), (354, 623), (400, 621), (427, 605), (459, 594), (482, 598), (527, 619), (527, 680), (650, 684), (655, 683), (758, 676), (758, 797), (1010, 797), (1030, 770),
         (1050, 720), (1062, 680), (1537, 676), (1540, 683), (1737, 683), (1737, 742), (1787, 742), (1787, 712), (1829, 683), (2019, 683)]) +
      S2([(645.5, 600), (657, 613), (657.8, 700), (650, 706), (636, 721), (621, 731), (610, 729), (607, 726), (605.5, 655), (561.4, 654), (450, 653.5), (361.4, 653), (350, 663), (336, 677), (321, 690),
          (318.6, 697), (310, 703), (301, 700), (279, 689), (250, 674), (221, 654), (193, 640), (173, 629), (172, 617), (178.6, 605.7), (207, 598.6), (236, 588.6), (270, 574), (284, 556), (293, 537),
          (300, 517)]))
EA_MAIN = (S2([(657.8, 700), (660, 698), (670, 687), (690, 670), (710, 660), (730, 640), (753, 632), (783, 627), (800, 622), (853, 607), (900, 595), (950, 583), (1000, 568), (1050, 548), (1100, 522),
               (1123, 510), (1153, 503), (1173, 498), (1183, 482), (1197, 470), (1182, 450), (1171, 401), (1152, 352), (1125, 326), (1100, 319), (1077, 306), (1069, 290), (1064, 265), (1064, 240),
               (1060, 220)]) +
           [('2', x, y) for x, y in c01([(850, 340), (838, 325), (796, 325), (796, 305), (775, 305), (775, 308.6), (754, 308.6), (754, 314), (741, 315), (740, 335)])] +
           S2([(766.7, 194.4), (755.6, 203), (744.4, 211), (737.8, 223), (739, 232), (735.6, 243), (725.6, 248.9), (713, 254.4), (700, 261), (693.3, 272), (693, 253), (655, 253), (655, 203.6), (651, 203.6),
               (640, 208), (618, 220), (600, 236), (593, 242), (585, 247), (580, 255), (577, 260), (576, 265), (574, 271), (570, 278), (566, 286), (562, 294), (558, 302), (552, 310), (546, 318),
               (540, 324), (534, 327.5), (532, 331), (533, 338), (528, 348), (520, 362), (512, 374), (504, 388), (563.8, 433), (563.8, 372), (569.6, 368), (657.5, 429), (650.3, 436), (650.3, 466),
               (644.8, 472), (644.8, 515.6), (645.5, 600), (657, 613)]))
EA_DEAS = S2([(471.5, 319), (480, 313), (490, 305), (500, 299.5), (510, 294), (520, 289), (530, 281), (540, 272), (550, 265), (560, 259), (568, 253.5), (570, 251.5), (571, 256), (567, 265), (563, 273),
              (559, 280), (554, 287), (548, 294), (541, 302), (536, 309), (530, 315), (522, 318), (516, 318.5), (500, 318), (490, 319), (480, 320.5)])
AREAS = [  # id, name, sold key, [rings]; ring = list of (x, y) in a single frame (frame tag) or mixed list of (tag, x, y)
 ('beach-grove', 'Beach Grove', 'Tsawwassen|Beach Grove', [('T', BG)]),
 ('boundary-beach', 'Boundary Beach', 'Tsawwassen|Boundary Beach', [('T', BB)]),
 ('cliff-drive', 'Cliff Drive', 'Tsawwassen|Cliff Drive', [('T', CD)]),
 ('english-bluff', 'English Bluff', 'Tsawwassen|English Bluff', [('T', EB)]),
 ('pebble-hill', 'Pebble Hill', 'Tsawwassen|Pebble Hill', [('T', PH)]),
 ('tsawwassen-central', 'Tsawwassen Central', 'Tsawwassen|Tsawwassen Central', [('T', CT)]),
 ('tsawwassen-east', 'Tsawwassen East', 'Tsawwassen|Tsawwassen East', [('T', TE)]),
 ('tsawwassen-north', 'Tsawwassen North', 'Tsawwassen|Tsawwassen North', [('T', TN)]),
 ('port-guichon', 'Port Guichon', 'Ladner|Port Guichon', [('L', PG), ('L', PG_I1), ('L', PG_I2)]),
 ('ladner-rural', 'Ladner Rural', 'Ladner|Ladner Rural', [('M', LA)]),
 ('east-delta', 'East Delta', 'Ladner|East Delta', [('M', EA_MAIN), ('M', EA_DEAS)]),
]
FN = {'T': llT, 'L': llL, '2': ll02}
def ring_ll(tag, pts):
    if tag == 'M': r = [FN[t](x, y) for t, x, y in pts]
    else: r = [FN[tag](x, y) for x, y in pts]
    r = [[round(a, 5), round(b, 5)] for a, b in r]; r.append(r[0]); return r
def mxy(r):  # metres, local equirectangular around Delta
    return [((b + 123.0) * 73000.0, (a - 49.05) * 111200.0) for a, b in r]
def trimmed(new, old):
    """My hand-read slivers give way to every neighbour (the existing areas first, then the areas drawn earlier in this run) when the overlap is under 25 percent of my area.
    Returns [(area, clash report)]."""
    from shapely.geometry import Polygon, MultiPolygon
    from shapely.ops import unary_union
    done = [(a['id'], unary_union([Polygon(mxy(r)).buffer(0) for r in a['rings']])) for a in old]
    out = []; rep = []
    for a in new:
        parts = []
        for r in a['rings']:
            g = Polygon(mxy(r)).buffer(0); mine = g.area
            for oid, h in done:
                if g.intersects(h):
                    ov = g.intersection(h).area
                    if ov > 0.0 and mine: rep.append((a['id'], oid, round(ov / 1e4) / 100, round(100 * ov / mine, 1)))
                    if ov < 0.25 * mine: g = g.difference(h)
            parts.append(g)
        done.append((a['id'], unary_union(parts)))
        rings = []
        for g, r0 in zip(parts, a['rings']):
            if g.is_empty: continue
            gs = [g] if g.geom_type == 'Polygon' else sorted([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: -x.area)[:1]
            for x in gs:
                c = list(x.exterior.coords)
                rr = [[round(y / 111200.0 + 49.05, 5), round(xx / 73000.0 - 123.0, 5)] for xx, y in c]
                rr[-1] = rr[0]; rings.append(rr)
        b = dict(a); b['rings'] = rings; out.append(b)
    return out, rep
def main():
    if '--check' in sys.argv:
        print('Tsawwassen residuals (m north, m east):', residuals(T_LAND, llT)); print('dropped:', residuals(T_DROPPED, llT))
        print('Ladner residuals:', residuals(L_LAND, llL))
        print('02 scale m/px:', round(_S * 73000, 2), '| 02 vs Cannery/London Farm/Leisure Centre (m N, m E):',
              [(n, round((ll02(x, y)[0] - la) * 111200), round((ll02(x, y)[1] - lo) * 73000)) for n, x, y, la, lo in
               (('Cannery', 60.8, 254.5, 49.1247253, -123.1869461), ('London Farm', 194.5, 318, 49.114679, -123.1519259), ('Leisure Centre', 557.1, 483.5, 49.0863292, -123.0583847))])
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    d = json.load(open(OUT)); mine = {a[0] for a in AREAS}
    old = [a for a in d['areas'] if a['id'] not in mine]
    new = []
    for aid, name, key, rings in AREAS:
        assert key in sold, key
        new.append({'id': aid, 'name': name, 'href': f'/{aid}.html', 'status': 'draft', 'sold': key, 'rings': [ring_ll(t, p) for t, p in rings]})
    new, rep = trimmed(new, old)
    if '--check' in sys.argv:
        print('overlaps before trimming (area, neighbour, km2, % of mine):')
        for r in rep: print('  ', r)
    d['areas'] = old + new
    pts = [p for a in d['areas'] for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    d['bbox'] = bbox; d['center'] = {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}
    json.dump(d, open(OUT, 'w'), separators=(',', ':')); print('delta', len(d['areas']), 'areas', bbox)
if __name__ == '__main__': main()
