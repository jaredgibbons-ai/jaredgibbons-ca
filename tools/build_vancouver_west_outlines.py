"""Draft outlines for Vancouver West (GVR layer) -> PART file /tmp/claude-0/-home-claude/09e1e130-90ed-5dc5-8543-375e6a966ec4/scratchpad/vancouver-w/part.json
(the lead merges this with the Vancouver East part into src/data/maps/vancouver.json; this script does not touch src/data/maps).

Source: Jared's Paragon map search (GVR sub-area layer, letter codes on, all 23 'Vancouver West' codes CONFIRMED in Closeups/GVR-code-names.csv), screenshots of 2026-11-04
in Paragon-Sub-Area-Boundaries/screenshots/9-Vancouver/: 02-west-of-main (1280x800, map rows 190-752) and 01-overview (same size, half the zoom of 02, so it reaches
the south end and the east edge).  SIFT could not register them (the basemap looks too different at the two zooms), so the zoom-out was fixed by hand:
overview pixel (x, y) = frame-02 pixel ((x - 4) / 2, (y + 354) / 2), taken from Oak/Ontario/16th Ave street edges and the Science World and BC Children's icons (about 4 px of
slack at 02 scale).  All polygons below are in 'frame-02 pixels' (VIRTUAL mosaic; west and north-west part read from the sharp frame 02, the south, Marpole/South Cambie/Oakridge
and the top (Stanley Park, Coal Harbour, West End north) read from the upscaled overview, so those edges are good to about 150 m, not 100 m).
Pixels become latitude/longitude with a Web Mercator fit (one shared scale for both axes, because the map is a Mercator tile view) to seven landmark coordinates from Google Maps:
Museum of Vancouver, Vancouver Maritime Museum, Science World, BC Children's Hospital (pin tip), Point Grey Secondary School (pin tip), Beaty Biodiversity Museum (the map-centre of
a single-result Google search, not a !3d value) and Langara College (read on the overview, mapped through the 2x relation).  Google began serving a CAPTCHA page to the shared browser
after about 15 lookups, so no further landmarks (UBC, Marpole, Southlands) could be fetched; --check prints the residuals (worst about 40 m); the south and the UBC end are an
extrapolation of the same fit.
Water is not drawn: every polygon stops at the shore (False Creek, Burrard Inlet, English Bay, Fraser River); Paragon's polygons for Southlands also cover river parts (labels 'SL'
sit in the river), those are left out.
Clipped on purpose, because the screenshot stops there: West End (Stanley Park runs on north past the top of the screenshot), Coal Harbour (same), University (the west tip of
Point Grey touches the left edge), Marpole (its south end runs past the bottom edge to the Fraser River).  Downtown VW's east edge is the Main St line (x about 1293); the
Mount Pleasant VW / VE split is at Ontario St (frame x 1252), one block west of Main St.  Every area stays 'draft'.
  python3 -I tools/build_vancouver_west_outlines.py [--check]"""
import json, math, os, sys
import os, tempfile
import numpy as np
OUT = os.path.join(tempfile.gettempdir(), 'outline-parts', 'vancouver-west.part.json')   # scratch part file; tools/merge_city_outlines.py merges the parts
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# (x, y, lat, lng) in frame-02 pixels; the Langara point was read on the overview and mapped with x2+4, y2-354
LAND = [(947, 244.3, 49.2762785, -123.1443725), (926.7, 229, 49.277517, -123.147183), (1260, 278, 49.273376, -123.103834), (1092, 631, 49.2444764, -123.1256816),
        (876.7, 708, 49.2378073, -123.1533586), (118, 404, 49.2633425, -123.2505979), (2 * 613.3 + 4, 2 * 606 - 354, 49.2249723, -123.1076016)]
def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def fit(L):
    """x = cx + s*lon(rad); y = cy - s*mercator(lat): one scale for both axes."""
    A = []; b = []
    for x, y, lat, lon in L:
        A.append([1, 0, math.radians(lon)]); b.append(x); A.append([0, 1, -merc(lat)]); b.append(y)
    cx, cy, s = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)[0]
    def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(-(py - cy) / s)) - math.pi / 2), 5), round(math.degrees((px - cx) / s), 5)
    return ll
ll = fit(LAND)
def residuals(): return [(round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
# --- polygons, frame-02 pixels (a ring is listed once; shared edges are repeated so neighbours meet) ---
POINT_GREY = [(342, 232), (390, 239), (417, 250), (437, 261), (467, 257), (498, 251), (513, 261), (537, 268), (560, 280), (583, 292), (605, 284), (618, 287), (627, 292),
              (626, 428), (634, 445), (638, 469), (396, 466), (398, 361), (363, 359), (362, 344), (340, 342), (336, 330), (321, 311), (318, 298), (321, 273), (327, 250)]
KITSILANO = [(627, 291), (650, 293), (683, 302), (710, 305), (733, 304), (760, 298), (780, 290), (797, 279), (820, 276), (840, 280), (853, 281), (863, 277), (880, 253), (893, 237),
             (913, 228), (927, 224), (940, 222), (955, 223), (966, 227), (978, 238), (984, 250), (985, 268), (992, 274), (976, 276), (960, 282), (948, 290), (941, 298), (938, 308),
             (937, 373), (936, 481), (880, 480), (767, 476), (668, 473), (638, 469), (634, 445), (626, 428)]
UNIVERSITY = [(342, 232), (333, 232), (300, 223), (267, 217), (250, 215), (233, 220), (210, 213), (197, 210), (180, 208), (160, 220), (147, 228), (133, 235), (117, 243), (100, 252), (88, 262),
              (72, 270), (53, 290), (40, 303), (28, 317), (20, 330), (15, 347), (8, 356), (4, 368), (4, 380), (10, 388), (20, 420), (33, 433), (50, 450), (60, 460), (77, 493), (100, 540),
              (110, 555), (140, 580), (173, 597), (200, 613), (233, 637), (267, 666), (300, 688), (330, 707), (349, 725), (372, 749), (399, 770), (424, 793), (441, 807), (455, 834),
              (469, 857), (480, 873), (497, 887), (502, 901), (519, 909), (538, 915), (552, 921), (580, 923), (582, 913), (583, 829), (572, 817), (540, 803), (537, 773), (539, 753),
              (539, 748), (528, 727), (527, 703), (539, 700), (538, 613), (480, 577), (542, 563), (542, 503), (540, 488), (492, 487), (490, 470), (396, 466), (398, 361), (363, 359),
              (362, 344), (340, 342), (336, 330), (321, 311), (318, 298), (321, 273), (327, 250)]
DUNBAR = [(490, 470), (668, 473), (682, 497), (695, 510), (701, 525), (715, 542), (727, 562), (732, 569), (680, 568), (680, 753), (539, 753), (539, 748), (528, 727), (527, 703),
          (539, 700), (538, 613), (480, 577), (542, 563), (542, 503), (540, 488), (492, 487)]
ARBUTUS = [(669, 474), (767, 476), (880, 480), (880, 546), (871, 546), (857, 552), (840, 562), (825, 572), (810, 581), (797, 587), (785, 590), (767, 591), (775, 612), (765, 612),
           (762, 606), (750, 590), (732, 569), (727, 562), (715, 542), (701, 525), (695, 510), (682, 497)]
MACKENZIE = [(680, 568), (732, 569), (750, 590), (762, 606), (765, 612), (775, 612), (780, 610), (790, 617), (800, 625), (806, 630), (806, 704), (681, 704)]
QUILCHENA = [(765, 592), (785, 590), (797, 587), (810, 581), (825, 572), (840, 562), (857, 552), (871, 546), (879, 546), (890, 555), (902, 567), (912, 572), (912, 610), (929, 647),
             (929, 662), (949, 663), (949, 707), (806, 704), (806, 630), (800, 625), (790, 617), (780, 610), (775, 600)]
SHAUGHNESSY = [(880, 480), (936, 481), (990, 483), (997, 477), (1007, 473), (1023, 473), (1040, 478), (1053, 482), (1078, 483), (1078, 771), (905, 772), (888, 772), (888, 730),
               (900, 729), (900, 708), (949, 707), (949, 663), (929, 662), (929, 647), (912, 610), (912, 572), (902, 567), (890, 555), (879, 546)]
KERRISDALE = [(681, 704), (900, 707), (900, 729), (888, 730), (888, 772), (905, 772), (905, 900), (884, 873), (868, 847), (740, 847), (703, 825), (680, 808), (678, 753)]
SOUTHLANDS = [(539, 753), (678, 753), (680, 808), (703, 825), (740, 847), (763, 865), (787, 880), (813, 897), (833, 910), (837, 937), (850, 960), (870, 993), (893, 1023), (910, 1068),
              (903, 1085), (898, 1102), (887, 1083), (867, 1057), (847, 1033), (820, 1013), (800, 1000), (780, 997), (753, 987), (733, 978), (700, 975), (687, 977), (673, 970),
              (657, 960), (633, 948), (610, 940), (580, 922), (582, 913), (583, 829), (572, 817), (540, 803), (537, 773)]
SW_MARINE = [(740, 847), (868, 847), (884, 873), (905, 900), (908, 925), (911, 975), (913, 1012), (973, 1013), (973, 1068), (910, 1068), (893, 1023), (870, 993), (850, 960),
             (837, 937), (833, 910), (813, 897), (787, 880), (763, 865)]
SOUTH_GRANVILLE = [(905, 771), (1078, 771), (1073, 853), (1070, 927), (1065, 953), (1060, 980), (1055, 998), (977, 965), (974, 1013), (913, 1012), (911, 975), (908, 925), (905, 900), (905, 847)]
CAMBIE = [(1078, 483), (1252, 483), (1252, 770), (1078, 771)]
OAKRIDGE = [(1073, 771), (1252, 770), (1247, 855), (1073, 853)]
SOUTH_CAMBIE = [(1073, 853), (1247, 855), (1245, 967), (1063, 967), (1065, 953), (1070, 927)]
MARPOLE = [(977, 965), (1055, 998), (1060, 980), (1063, 967), (1245, 967), (1247, 1108), (1213, 1105), (1180, 1112), (1147, 1127), (1100, 1148), (967, 1147), (947, 1140), (923, 1127),
           (900, 1112), (898, 1102), (903, 1085), (910, 1068), (973, 1068), (974, 1013)]
FAIRVIEW = [(936, 373), (1176, 373), (1176, 483), (1078, 483), (1053, 482), (1040, 478), (1023, 473), (1007, 473), (997, 477), (990, 483), (936, 481)]
MOUNT_PLEASANT = [(1176, 380), (1252, 381), (1252, 483), (1176, 483)]
FALSE_CREEK = [(938, 373), (938, 308), (941, 298), (948, 290), (960, 282), (976, 276), (992, 274), (985, 281), (983, 290), (985, 300), (995, 311), (1005, 321), (1013, 332), (1025, 344),
               (1038, 353), (1048, 358), (1060, 353), (1076, 349), (1102, 349), (1120, 350), (1147, 342), (1160, 337), (1180, 328), (1200, 318), (1213, 308), (1233, 303), (1252, 303),
               (1252, 381), (1177, 380), (1176, 373)]
GRANVILLE_ISLAND = [(1010, 291), (1020, 292), (1033, 306), (1045, 325), (1054, 343), (1050, 353), (1040, 350), (1027, 338), (1012, 326), (1004, 318), (1003, 305)]
YALETOWN = [(1016, 256), (1050, 249), (1052, 252), (1062, 264), (1070, 276), (1078, 284), (1140, 220), (1160, 231), (1177, 251), (1179, 275), (1181, 275), (1205, 261), (1222, 250),
            (1241, 243), (1242, 244), (1241, 250), (1225, 262), (1210, 272), (1195, 279), (1180, 281), (1177, 283), (1170, 290), (1160, 300), (1150, 310), (1140, 322), (1120, 318),
            (1095, 312), (1075, 300), (1050, 290), (1035, 280)]
DOWNTOWN = [(1160, 127), (1200, 145), (1222, 150), (1292, 151), (1293, 303), (1270, 301), (1268, 280), (1255, 268), (1242, 257), (1242, 244), (1222, 250), (1205, 261), (1181, 275),
            (1179, 275), (1177, 251), (1160, 231), (1140, 220), (1078, 284), (1070, 276), (1062, 264), (1052, 252), (1050, 250), (1062, 230), (1077, 208), (1095, 192), (1112, 182),
            (1116, 165), (1115, 147), (1135, 142), (1150, 137)]
COAL_HARBOUR = [(1001, 42), (1015, 50), (1030, 61), (1042, 64), (1060, 58), (1070, 64), (1075, 72), (1085, 80), (1100, 90), (1110, 86), (1120, 91), (1135, 95), (1150, 100), (1163, 113),
                (1172, 121), (1160, 127), (1150, 137), (1135, 142), (1115, 147), (1097, 132), (1075, 110), (1050, 87), (1025, 65)]
WEST_END = [(904, 32), (1005, 28), (1001, 42), (1025, 65), (1050, 87), (1075, 110), (1097, 132), (1115, 147), (1116, 165), (1112, 182), (1095, 192), (1077, 208), (1062, 230), (1050, 250),
            (1016, 256), (1010, 250), (1002, 240), (989, 227), (979, 212), (968, 200), (948, 160), (930, 112), (930, 76)]
# sold key, slug (page in src/data/local), name, rings; an earlier area keeps its ground where outlines overlap by hand-reading error
VW = [
 ('Vancouver West|Point Grey', 'point-grey-vancouver', 'Point Grey', [POINT_GREY]),
 ('Vancouver West|Kitsilano', 'kitsilano', 'Kitsilano', [KITSILANO]),
 ('Vancouver West|Dunbar', 'dunbar', 'Dunbar', [DUNBAR]),
 ('Vancouver West|Arbutus', 'arbutus', 'Arbutus', [ARBUTUS]),
 ('Vancouver West|MacKenzie Heights', 'mackenzie-heights', 'MacKenzie Heights', [MACKENZIE]),
 ('Vancouver West|Quilchena', 'quilchena-vancouver', 'Quilchena', [QUILCHENA]),
 ('Vancouver West|Shaughnessy', 'shaughnessy-vancouver-guide', 'Shaughnessy', [SHAUGHNESSY]),
 ('Vancouver West|Kerrisdale', 'kerrisdale-vancouver-guide', 'Kerrisdale', [KERRISDALE]),
 ('Vancouver West|S.W. Marine', 'sw-marine-vancouver-guide', 'S.W. Marine', [SW_MARINE]),
 ('Vancouver West|South Granville', 'south-granville-vancouver-guide', 'South Granville', [SOUTH_GRANVILLE]),
 ('Vancouver West|Cambie', 'cambie', 'Cambie', [CAMBIE]),
 ('Vancouver West|Oakridge VW', 'oakridge-vancouver-guide', 'Oakridge', [OAKRIDGE]),
 ('Vancouver West|South Cambie', 'south-cambie-vancouver-guide', 'South Cambie', [SOUTH_CAMBIE]),
 ('Vancouver West|Marpole', 'marpole-vancouver', 'Marpole', [MARPOLE]),
 ('Vancouver West|Southlands', 'southlands-vancouver', 'Southlands', [SOUTHLANDS]),
 ('Vancouver West|Fairview VW', 'fairview-vw', 'Fairview', [FAIRVIEW]),
 ('Vancouver West|Mount Pleasant VW', 'mount-pleasant-vancouver-guide', 'Mount Pleasant (west of Ontario St)', [MOUNT_PLEASANT]),
 ('Vancouver West|False Creek', 'false-creek', 'False Creek', [FALSE_CREEK, GRANVILLE_ISLAND]),
 ('Vancouver West|Yaletown', 'yaletown-vancouver', 'Yaletown', [YALETOWN]),
 ('Vancouver West|Downtown VW', 'downtown-vw', 'Downtown', [DOWNTOWN]),
 ('Vancouver West|Coal Harbour', 'coal-harbour', 'Coal Harbour', [COAL_HARBOUR]),
 ('Vancouver West|West End VW', 'west-end-vancouver', 'West End', [WEST_END]),
 ('Vancouver West|University VW', 'university-endowment-lands-vancouver-guide', 'University (UBC and Pacific Spirit)', [UNIVERSITY]),
]
def trimmed(rows):
    """Hand-read edges leave slivers where two outlines meet; the later area gives up any overlap (under 1500 px2, about 13 ha) with an earlier one."""
    from shapely.geometry import Polygon
    done = []; out = []
    for key, slug, name, rings in rows:
        newr = []
        for ring in rings:
            g = Polygon(ring)
            if not g.is_valid: g = g.buffer(0)
            for h in done:
                if g.intersects(h) and g.intersection(h).area < 1500: g = g.difference(h)
            done.append(g)
            if g.is_empty: continue
            gg = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
            newr.append(list(gg.exterior.coords)[:-1])
        out.append((key, slug, name, newr))
    return out
def main():
    if '--check' in sys.argv: print('landmark residuals (m north, m east):', residuals())
    sold = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json')))['sub']
    pts = []; areas = []
    for key, slug, name, rings in trimmed(VW):
        rr = []
        for ring in rings:
            r = [list(ll(x, y)) for x, y in ring]; r.append(r[0]); rr.append(r); pts += r
        assert key in sold, key
        areas.append({'id': slug, 'name': name, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rr})
    pad = 0.004; bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    out = {'region': 'vancouver', 'name': 'Vancouver', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': areas}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), separators=(',', ':')); print('vancouver (west part)', len(areas), 'areas', bbox, '->', OUT)
if __name__ == '__main__': main()
