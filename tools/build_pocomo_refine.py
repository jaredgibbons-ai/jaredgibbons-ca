"""REFINED outlines for Port Moody (10 areas, Belcarra added) and Port Coquitlam (10 areas), plus two Coquitlam corrections -> src/data/maps/port-moody.json,
src/data/maps/port-coquitlam.json (both rewritten) and src/data/maps/coquitlam.json (ADDITIVE: only river-springs-coquitlam and meadow-brook-coquitlam get new rings;
the other 20 areas are left byte-identical).  Supersedes the Port Moody / Port Coquitlam part of build_pocomo_outlines.py: run THAT script first (it still owns the Coquitlam
West / Central / Maillardville / Cape Horn / East slices), then this one:
  python3 -I tools/build_pocomo_outlines.py && python3 -I tools/build_pocomo_refine.py [--check]

Source: six Paragon screenshots of 2026-11-05 (GVR Sub Areas 2022, code labels on, 1920 x 880, map pane y 37 to 858): 04 = Port Moody overview (reference mosaic, 6.26 m/pixel),
02 and 06 = same zoom, panned (SIFT-registered to 04: 02 + (898.2, 406.3), 06 + (-205.1, -352.4)); 05 and 03 = twice that zoom (3.13 m/pixel; fitted to the mosaic from
street-intersection landmarks, 05 as a scale/offset chain with ~12 m residual); 01 = half zoom, used only for the far south of Port Coquitlam (Citadel / Mary Hill bottoms,
good to ~50 m).  Paragon's polygon boundaries are 2-pixel white lines; they were extracted from the frames by flood-filling between the lines (seeded at each area's label),
simplified to ~12 m and closed over label halos.  Where a boundary line is missing (frame edge, a river crossing) the fill was cut with a hand-drawn clip (Central Port Coquitlam
at the Pitt River) or the label-halo notch was removed by hand (Mountain Meadows).  Colours are NOT boundaries.  Vertices below are in the 04-mosaic pixel frame (x, y).
Calibration (mosaic pixel -> lat/lng): Web Mercator fit (longitude vs x, Mercator latitude vs y) to 12 landmarks whose coordinates come from OpenStreetMap (Overpass; Google
Maps is CAPTCHA-blocked): ten street intersections in Port Coquitlam, Barnet Hwy x Albert St, Guildford Way x Johnson St, Lafarge Lake and Port Coquitlam stations.  Worst
residual about 10 m (`--check`).  Dropped: Moody Centre and Inlet Centre station icons (icon is not at the OSM node, -110 m).  West of the landmarks (Belcarra) the fit is
extrapolated; checked against OSM Sasamat Lake (centre within ~45 m) and Admiralty Point (on the right shore).
Clipped on purpose: Anmore and Belcarra run north past the top of the frames (mosaic y -315).  Not drawn: Ioco (code IO, no sold key).  Westwood Summit CQ is not in these files.
Every area stays 'draft'.
"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MAPS = os.path.join(ROOT, 'src/data/maps')
LAND = [  # (mosaic x, mosaic y, lat, lng, name)
    (1470, 573, 49.28546, -122.79171, 'Lafarge Lake station'), (1674, 1004, 49.26148, -122.77409, 'Port Coquitlam station'),
    (1753.2, 699.5, 49.27839, -122.76725, 'Lincoln Av x Oxford St'), (1883.2, 699.5, 49.27848, -122.7561, 'Lincoln Av x Coast Meridian Rd'),
    (1753.2, 830.5, 49.27117, -122.76718, 'Oxford St x Prairie Av'), (1883.2, 830.5, 49.27118, -122.75613, 'Coast Meridian Rd x Prairie Av'),
    (2141.8, 829.1, 49.2713, -122.73379, 'Fremont St x Prairie Av'), (2141.8, 1058.6, 49.2584, -122.73406, 'Fremont St x Dominion Av'),
    (2203.2, 1058.6, 49.2584, -122.72866, 'Burns Rd x Dominion Av'), (1883.2, 897.7, 49.26744, -122.75612, 'Coast Meridian Rd x Coquitlam Av'),
    (592.7, 732.3, 49.27663, -122.86681, 'Barnet Hwy x Albert St'), (1352, 579, 49.2852, -122.80166, 'Guildford Wy x Johnson St')]
def merc(l): return math.log(math.tan(math.pi / 4 + math.radians(l) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
def residuals(): return [(p[4], round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 73000)) for p in LAND]
# ---------------- outlines: (sold key, page slug, name, ring in mosaic pixels) ----------------
PORT_MOODY = [
 ('Port Moody|Anmore', 'anmore-homes-for-sale', 'Anmore',
  [(453.5, -315.5), (454.5, -221), (672, -217), (686.5, -161.5), (687, -115.5), (628.5, -114.5), (628, -93.5), (585.5, -93.5), (585, 38.5), (465.5, 39.5), (465.5, 75.5), (518.5, 76), (517.5, 205.5), (591, 205.5), (599, 204), (599.5, 201), (611, 201), (613.5, 205.5), (692, 205.5), (719, 172), (790.5, 173.5), (796.5, 209.5), (890.5, 212.5), (887.5, 322), (957, 323.5), (960, 318), (955, 212.5), (983, 211.5), (985, 48), (1054.5, 46), (1110, -84), (1110, -315.5)]),
 ('Port Moody|Belcarra', 'belcarra-port-moody', 'Belcarra',
  [(671, -213.5), (452.5, -218.5), (451, -315.5), (344.5, -315.5), (341, -312.5), (322.5, -312.5), (307.5, -293.5), (296.5, -272), (278.5, -258.5), (275.5, -246), (269.5, -243.5), (249.5, -215), (237.5, -205.5), (222.5, -184), (195.5, -156.5), (184.5, -123), (175, -114.5), (140.5, -96.5), (119.5, -78.5), (102.5, -57.5), (94.5, -42), (83.5, -29.5), (73.5, -8), (56.5, 9.5), (48, 25.5), (40.5, 27.5), (-1, 62.5), (-19, 73.5), (-27.5, 74.5), (-37, 66), (-37, 59.5), (-18, 30), (-16, 8.5), (-6, -1), (1, -21.5), (8.5, -29), (18, -33), (24, -55), (22, -70.5), (12, -89.5), (6, -94), (4, -112.5), (21, -130), (22, -146.5), (29, -154), (33.5, -173), (55, -172), (75.5, -188), (91, -186), (92, -202.5), (100, -208), (100, -210.5), (79.5, -212.5), (67, -224), (67, -232.5), (37, -217.5), (-9.5, -217.5), (-11.5, -207), (-9.5, -201), (-2.5, -195.5), (-2.5, -182), (-38.5, -147.5), (-74.5, -105), (-83.5, -101.5), (-106.5, -75.5), (-110.5, -65), (-102, -62), (-101.5, -57), (-118.5, -44.5), (-121.5, -35), (-130.5, -32.5), (-145, -12.5), (-153.5, -12.5), (-166.5, -6.5), (-163.5, 19), (-153, 20), (-141, 12), (-129.5, -6), (-110, -8), (-108.5, 6), (-104.5, 8.5), (-103.5, 20), (-97.5, 33.5), (-105.5, 57.5), (-105.5, 69), (-115.5, 77.5), (-108.5, 85.5), (-102.5, 102), (-117.5, 117.5), (-113.5, 135), (-120.5, 145.5), (-122.5, 159), (-118.5, 165.5), (-118.5, 179), (-133.5, 230.5), (-132.5, 242), (-126.5, 248.5), (-112.5, 299), (-95.5, 316.5), (-96.5, 338), (-108.5, 346.5), (-110.5, 352), (-96, 358), (-80, 348), (-67.5, 357), (-57, 358), (-45.5, 371.5), (-35.5, 414), (-27.5, 426), (-1.5, 437), (13, 432), (34.5, 430), (37, 424), (21, 382), (22.5, 364.5), (51.5, 342), (203, 247.5), (277, 169.5), (276, 152.5), (285.5, 135.5), (514, 147.5), (515, 80.5), (463.5, 78.5), (463, 36.5), (583, 36), (583, -94.5), (626, -96), (627.5, -117), (685, -118), (684, -161.5)]),
 ('Port Moody|Barber Street', 'barber-street-port-moody', 'Barber Street',
  [(719, 175.5), (684, 215.5), (639.5, 234.5), (601.5, 280), (593.5, 285.5), (585.5, 297.5), (585, 303.5), (617.5, 328.5), (619.5, 341.5), (630, 347.5), (681.5, 404), (693, 410), (720, 417), (754.5, 443.5), (754.5, 406), (766.5, 388.5), (735, 354), (747, 294), (788.5, 259.5), (792.5, 199.5), (788, 176.5)]),
 ('Port Moody|Heritage Mountain', 'heritage-mountain-port-moody', 'Heritage Mountain',
  [(795.5, 212.5), (791.5, 260), (749.5, 295.5), (740, 353), (771, 387), (820, 419.5), (871.5, 439.5), (908, 493), (925.5, 505), (951.5, 505.5), (951.5, 498), (955, 493.5), (973.5, 494.5), (975, 499.5), (978.5, 499.5), (979, 494.5), (996, 498.5), (997, 507.5), (987, 509), (987.5, 528.5), (994.5, 542.5), (1012.5, 554.5), (1012.5, 512), (1022, 499.5), (1055.5, 474.5), (1058.5, 461), (1076.5, 437), (1076.5, 426.5), (1080.5, 426), (1084.5, 415.5), (1092.5, 369.5), (1077.5, 369.5), (1044, 381.5), (982, 373.5), (960.5, 374.5), (956, 370), (957, 327.5), (884.5, 324), (887, 214.5)]),
 ('Port Moody|Heritage Woods PM', 'heritage-woods-port-moody', 'Heritage Woods',
  [(1110, -74.5), (1107.5, -74.5), (1056.5, 49), (987.5, 51.5), (985.5, 215), (958.5, 214.5), (963, 318), (959.5, 321.5), (960, 367.5), (963, 370), (1044.5, 378), (1077.5, 366), (1106, 366)]),
 ('Port Moody|Mountain Meadows', 'mountain-meadows-port-moody', 'Mountain Meadows',
  [(1097, 369.5), (1087, 415), (1082, 426), (1078, 438), (1062, 462), (1058, 476), (1084, 483.5), (1100.5, 482.5), (1102.5, 487.5), (1111, 491.5), (1112, 496.5), (1123.5, 497.5), (1124.5, 408.5), (1107, 408), (1106, 369.5)]),
 ('Port Moody|North Shore Pt Moody', 'north-shore-port-moody', 'North Shore',
  [(517.5, 208.5), (517.5, 268), (521.5, 272.5), (521.5, 288), (536.5, 281.5), (547.5, 288.5), (562.5, 314.5), (576.5, 353), (584, 361), (594.5, 361.5), (599, 353.5), (599, 346), (603, 343.5), (609.5, 345.5), (635, 370.5), (659.5, 401.5), (689, 420), (713, 424.5), (720, 434.5), (733, 441.5), (742, 454.5), (756, 460), (764.5, 471.5), (773.5, 472), (796.5, 485.5), (822.5, 493.5), (830.5, 507.5), (840.5, 506), (855, 515.5), (866.5, 517.5), (875, 535.5), (887.5, 542), (883, 550.5), (870.5, 550), (871.5, 561.5), (913.5, 580.5), (913.5, 555), (918.5, 551.5), (944.5, 569.5), (959, 575.5), (966.5, 597.5), (995.5, 598.5), (1000, 591.5), (1007.5, 591.5), (1008, 588.5), (1019.5, 588.5), (1023, 591), (1023, 598.5), (1039.5, 596.5), (1046, 603.5), (1047, 626), (1050, 629.5), (1059, 673.5), (1059.5, 715.5), (1092.5, 710.5), (1093.5, 663), (1124.5, 660.5), (1123.5, 501.5), (1108.5, 501.5), (1106.5, 494.5), (1097, 486.5), (1084.5, 488.5), (1056, 479.5), (1023.5, 504.5), (1018.5, 511.5), (1017, 546.5), (1020, 566.5), (987, 539.5), (982.5, 528.5), (981.5, 509), (978.5, 506), (971, 509), (970.5, 505.5), (964.5, 503.5), (964.5, 497.5), (958, 497.5), (956.5, 508.5), (923.5, 508), (902.5, 493.5), (895, 478.5), (868, 442), (817.5, 421.5), (772, 391.5), (758.5, 405.5), (759, 446.5), (754.5, 449.5), (737.5, 438), (723, 422.5), (677.5, 406), (631, 354.5), (617, 343), (615, 329.5), (581, 304), (587, 288.5), (599, 279.5), (607, 264.5), (641, 230), (659.5, 220), (678, 215.5), (684.5, 211.5), (684.5, 208.5), (614.5, 208.5), (614.5, 213), (611, 215.5), (591.5, 215.5), (591, 208.5)]),
 ('Port Moody|College Park PM', 'college-park-port-moody', 'College Park',
  [(275, 501.5), (281.5, 743.5), (297, 736), (431, 736), (433.5, 744.5), (435.5, 835.5), (573, 836), (573, 762.5), (565, 754.5), (560.5, 754), (563, 742), (562.5, 694.5), (569, 686), (564.5, 675.5), (564.5, 660.5), (580.5, 643.5), (580.5, 618.5), (588.5, 613.5), (584.5, 566.5), (580.5, 552.5), (568.5, 528.5), (554.5, 510), (508, 480.5), (485, 475.5), (453.5, 478.5), (421.5, 490.5), (421.5, 493), (431.5, 495.5), (431.5, 503.5), (424.5, 500.5), (424, 505.5), (409.5, 505.5), (408, 495.5), (357.5, 498.5), (322, 491.5), (296.5, 492.5)]),
 ('Port Moody|Glenayre', 'glenayre-port-moody', 'Glenayre',
  [(281.5, 746.5), (285, 843.5), (433, 840), (429, 738.5), (297, 738.5)]),
 ('Port Moody|Port Moody Centre', 'port-moody-centre', 'Port Moody Centre',
  [(275.5, 463.5), (274.5, 498), (301.5, 488), (322.5, 488), (357.5, 495), (413, 491.5), (449, 476), (485, 472), (506.5, 476), (524.5, 485), (550.5, 504), (567, 520.5), (584, 551), (588.5, 568), (592, 614), (584.5, 619), (585, 642.5), (568.5, 661), (568, 674), (574, 684.5), (566, 696), (566, 752), (575.5, 762), (575.5, 836), (831, 838), (831, 804.5), (951.5, 803.5), (953, 793.5), (1092.5, 792.5), (1093.5, 718.5), (1091.5, 715), (1061, 720), (1055.5, 718.5), (1052.5, 711.5), (1053.5, 671), (1039.5, 600.5), (1008, 603), (1006.5, 600), (1002.5, 603), (971.5, 600.5), (955, 615.5), (955, 621.5), (960, 624), (960.5, 631.5), (964, 634), (963.5, 642), (957, 651.5), (947, 652.5), (937, 648), (933.5, 630.5), (927, 629), (891.5, 652.5), (878.5, 652), (843, 676), (827.5, 674), (811, 666), (807, 662), (804.5, 650.5), (793, 640.5), (785.5, 640.5), (783, 645), (781, 668), (777.5, 672), (771, 671.5), (771, 662.5), (757.5, 660.5), (752.5, 648), (750, 665), (741, 665.5), (739, 651), (695, 652.5), (698, 687), (694, 692.5), (685, 692), (649, 673.5), (648.5, 668.5), (654.5, 663.5), (655, 658.5), (643, 648), (680.5, 631.5), (680.5, 626), (613, 547.5), (609, 538), (604.5, 535.5), (604.5, 526.5), (569, 484.5), (561.5, 487.5), (523.5, 466.5), (519, 458.5), (514, 456.5), (463.5, 458.5), (440, 463.5), (396.5, 463.5), (382, 475.5), (353.5, 469.5), (349, 464.5), (333.5, 468.5), (323, 461.5), (305.5, 463.5), (285.5, 460.5)]),
]
PORT_COQ = [
 ('Port Coquitlam|Woodland Acres PQ', 'woodland-acres-port-coquitlam', 'Woodland Acres',
  [(1485, 702), (1485, 788), (1542, 825.5), (1554, 825.5), (1557, 835.5), (1562.5, 836), (1564, 839.5), (1607.5, 865.5), (1628.5, 802), (1639.5, 791.5), (1643.5, 778.5), (1646.5, 702.5)]),
 ('Port Coquitlam|Glenwood PQ', 'glenwood-port-coquitlam', 'Glenwood',
  [(1651, 702.5), (1647, 783.5), (1641, 795.5), (1631.5, 802.5), (1627.5, 810.5), (1623, 837.5), (1613, 859), (1612, 869.5), (1742, 956.5), (1830, 1011.5), (1839, 1012.5), (1841, 1018.5), (1874, 1040.5), (1880.5, 1040.5), (1882.5, 947), (1890.5, 946.5), (1890.5, 935), (1882.5, 934.5), (1881.5, 778.5), (1875.5, 778), (1872.5, 772), (1867, 770), (1864.5, 758.5), (1867, 748.5), (1872.5, 747.5), (1873.5, 742), (1881.5, 740), (1882.5, 702)]),
 ('Port Coquitlam|Oxford Heights', 'oxford-heights-port-coquitlam', 'Oxford Heights',
  [(1755.5, 699.5), (1884.5, 698.5), (1912, 733.5), (1931.5, 737.5), (1957.5, 715.5), (1966.5, 693), (1993, 649.5), (2014, 637.5), (2036, 631.5), (2066.5, 629.5), (2077.5, 624.5), (2082, 617.5), (2096.5, 612.5), (2138.5, 576.5), (2139.5, 570), (1819.5, 572), (1818.5, 508), (1757.5, 506.5)]),
 ('Port Coquitlam|Lincoln Park PQ', 'lincoln-park-port-coquitlam', 'Lincoln Park',
  [(1885.5, 780), (1885, 828.5), (2144.5, 826.5), (2147.5, 823.5), (2147.5, 702), (2141.5, 698.5), (2141.5, 578), (2102.5, 611), (2082, 620), (2077.5, 627), (2069.5, 631), (2036, 634), (2014, 640), (1993, 652), (1969, 693), (1960, 715.5), (1931.5, 740), (1913.5, 738.5), (1885.5, 706.5), (1885.5, 740), (1889, 740), (1889, 750), (1884, 754), (1884, 765.5), (1889, 768.5), (1889, 778.5)]),
 ('Port Coquitlam|Birchland Manor', 'birchland-manor-port-coquitlam', 'Birchland Manor',
  [(1885, 831), (1885, 846), (1889, 846.5), (1889.5, 858), (1885, 858), (1885, 940.5), (1892.5, 940.5), (1893, 946.5), (1971.5, 932.5), (2015.5, 918.5), (2052, 880.5), (2052, 893.5), (2080.5, 892.5), (2080.5, 838), (2073.5, 837.5), (2073.5, 830)]),
 ('Port Coquitlam|Riverwood', 'riverwood-port-coquitlam', 'Riverwood',
  [(2415.5, 697), (2150, 699), (2150, 823.5), (2144.5, 829), (2083, 830), (2082.5, 895), (2050, 896), (2049.5, 892), (2043, 892), (2015.5, 921), (1971.5, 935), (1894, 950), (1891.5, 945), (1885, 945), (1883, 1045.5), (2119, 1198.5), (2167, 1225.5), (2174.5, 1225.5), (2187.5, 1210.5), (2193.5, 1193), (2217.5, 1168.5), (2236.5, 1139), (2260.5, 1112.5), (2263.5, 1094), (2273.5, 1068.5), (2274.5, 1050), (2296.5, 994), (2308.5, 974.5), (2328.5, 919), (2344.5, 898.5), (2351.5, 880), (2358.5, 873.5), (2361.5, 858), (2378.5, 829.5), (2377.5, 820), (2392.5, 767), (2415.5, 706.5)]),
 ('Port Coquitlam|Central Pt Coquitlam', 'central-port-coquitlam', 'Central Port Coquitlam',
  [(1485, 792), (1480, 1010.5), (1456.5, 1018), (1420, 1020), (1411, 1026), (1403, 1038), (1398, 1052), (1403, 1095.5), (1393, 1121), (1393, 1143.5), (1404, 1189.5), (1413.5, 1198.5), (1411.5, 1193), (1438, 1168.5), (1475.5, 1161.5), (1500, 1132.5), (1514, 1124.5), (1596.5, 1125.5), (1624, 1135.5), (1646.5, 1135.5), (1680.5, 1145.5), (1681, 1148.5), (1759.5, 1148.5), (1761, 1222.5), (1812, 1223), (1812, 1363.5), (1818, 1375), (1795, 1395), (1797.5, 1399), (1789.5, 1411.5), (1789.5, 1443), (1785.5, 1445.5), (1785.5, 1453), (1789, 1453), (1831.5, 1415.5), (1878.5, 1383), (1951, 1326), (2000.5, 1309), (2018, 1306), (2028.5, 1300), (2027, 1304), (2086, 1294), (2106, 1284), (2099.5, 1282), (2109, 1273.5), (2126.5, 1267.5), (2135, 1255.5), (2148.5, 1251.5), (2169.5, 1232.5), (2169.5, 1229), (2103, 1191), (1840.5, 1020), (1832.5, 1019.5), (1831, 1014), (1647, 898), (1606.5, 868), (1561, 840), (1543.5, 840), (1539, 835.5), (1540.5, 827)]),
 ('Port Coquitlam|Mary Hill', 'mary-hill-port-coquitlam', 'Mary Hill',
  [(1511, 1128), (1500, 1135), (1489, 1148), (1490, 1171.5), (1530, 1173), (1530, 1238.5), (1568.5, 1238.5), (1575, 1245), (1575, 1263.5), (1570.5, 1286), (1544, 1327.5), (1518, 1351.5), (1497.5, 1395.5), (1500, 1401), (1496, 1405.5), (1496, 1415), (1639, 1415), (1639, 1398), (1641.5, 1397.5), (1642.5, 1387), (1676.5, 1387.5), (1676.5, 1371), (1682.5, 1344), (1680, 1290), (1684.5, 1269.5), (1698.5, 1243.5), (1698.5, 1222), (1687.5, 1167), (1678.5, 1148), (1646.5, 1138), (1624, 1138), (1596.5, 1128)]),
 ('Port Coquitlam|Lower Mary Hill', 'lower-mary-hill-port-coquitlam', 'Lower Mary Hill',
  [(1683, 1151), (1696, 1187), (1701, 1243.5), (1686, 1269.5), (1681.5, 1290), (1684, 1344), (1678, 1371), (1678, 1385.5), (1691.5, 1397.5), (1693.5, 1403), (1783, 1403), (1791.5, 1387.5), (1813.5, 1371.5), (1810.5, 1363.5), (1809.5, 1225), (1759, 1225), (1758.5, 1221), (1742.5, 1222.5), (1743, 1212.5), (1750.5, 1212.5), (1753, 1208.5), (1758.5, 1210.5), (1757.5, 1151)]),
 ('Port Coquitlam|Citadel PQ', 'citadel-port-coquitlam', 'Citadel',
  [(1296, 1365), (1294.5, 1429), (1302.5, 1439), (1322.5, 1447), (1361.5, 1449), (1374, 1457.5), (1376, 1465.5), (1374, 1491), (1338.5, 1563), (1322, 1581.5), (1316.5, 1583.5), (1308.5, 1607.5), (1308.5, 1619), (1316.5, 1634.5), (1324.5, 1646.5), (1332.5, 1648.5), (1397.5, 1646.5), (1418, 1636.5), (1438, 1632.5), (1503.5, 1628.5), (1510, 1624.5), (1531.5, 1623), (1540, 1617), (1553.5, 1619), (1580, 1613), (1595.5, 1613), (1625.5, 1603), (1659, 1597), (1677, 1585), (1695, 1553.5), (1743, 1505), (1745, 1497.5), (1765, 1487), (1789, 1465), (1785, 1455.5), (1779, 1451), (1785, 1443), (1787, 1407.5), (1691.5, 1407.5), (1689, 1401.5), (1684, 1401.5), (1684, 1395.5), (1675.5, 1389), (1643, 1388.5), (1643, 1419.5), (1574, 1419.5), (1571, 1432.5), (1567.5, 1419.5), (1494, 1419.5), (1489.5, 1409.5), (1516.5, 1351.5), (1542, 1327), (1569, 1286), (1572.5, 1272.5), (1572.5, 1246.5), (1567.5, 1241), (1527.5, 1240.5), (1527.5, 1175), (1488, 1174), (1487, 1153), (1473.5, 1165), (1442, 1169), (1415, 1192), (1431, 1216), (1432, 1226.5), (1428, 1234.5), (1421.5, 1239), (1398, 1236), (1397, 1258.5), (1392.5, 1266), (1387, 1269.5), (1356.5, 1273.5), (1345.5, 1281), (1345, 1289.5), (1355.5, 1313.5), (1356, 1321.5), (1332.5, 1348), (1307.5, 1352.5), (1300, 1357.5)]),
]
# Coquitlam: only these two outlines are redrawn (same id/href/sold as the existing records)
COQ_REDRAW = {
 'river-springs-coquitlam': [(1671.5, 392.5), (1669.5, 417.5), (1683, 423.5), (1683, 430), (1697, 458.5), (1699, 510), (1711.5, 525.5), (1734.5, 526), (1736, 540), (1721.5, 540), (1719, 536), (1711.5, 540), (1705, 557.5), (1697.5, 562.5), (1681.5, 582.5), (1649.5, 640), (1647, 658), (1651, 699.5), (1752.5, 699.5), (1754.5, 505), (1791.5, 503.5), (1791.5, 443), (1799, 441.5), (1799, 438), (1793, 432.5), (1751, 413.5), (1739, 395.5), (1736.5, 372.5), (1732.5, 366.5), (1727.5, 368.5), (1725, 383.5), (1712.5, 390.5), (1690.5, 388.5), (1691.5, 392)],
 'meadow-brook-coquitlam': [(1405, 742), (1397.5, 752.5), (1389.5, 778), (1388, 918.5), (1391, 959.5), (1394, 973.5), (1439.5, 973.5), (1478.5, 935.5), (1480.5, 788)],
}
def build(areas, existing, region, name, out, keep_existing=None):
    from shapely.geometry import Polygon
    from shapely.validation import make_valid
    mine = {a[1] for a in areas}
    keep = [a for a in (keep_existing or []) if a['id'] not in mine]
    others = [(a['id'], [Polygon([(p[1], p[0]) for p in r]) for r in a['rings']]) for a in keep]
    new = []
    for key, slug, nm, poly in areas:
        ring = [list(ll(x, y)) for x, y in poly]
        g = Polygon([(p[1], p[0]) for p in ring])
        if not g.is_valid: g = make_valid(g).buffer(0)
        a0 = g.area
        for eid, polys in others:
            for h in polys:
                if g.intersects(h):
                    ov = g.intersection(h).area
                    if ov > 0.003 * a0: print(f'  {slug}: trimmed {100 * ov / a0:.1f}% against {eid}')
                    g = g.difference(h)
        parts = [g] if g.geom_type == 'Polygon' else sorted([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: -x.area)
        rings = []
        for part in parts:
            if part.area < 0.02 * a0: continue
            c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        others.append((slug, [g]))
        new.append({'id': slug, 'name': nm, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    allareas = keep + new
    write(allareas, existing, region, name, out)
def write(allareas, existing, region, name, out):
    pts = [p for a in allareas for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data = dict(existing or {}); data.update({'region': region, 'name': name, 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': allareas})
    data = {k: data[k] for k in ('region', 'name', 'center', 'bbox', 'areas') if k in data} | {k: v for k, v in data.items() if k not in ('region', 'name', 'center', 'bbox', 'areas')}
    json.dump(data, open(out, 'w'), separators=(',', ':'))
    print(out.split('/')[-1], len(allareas), 'areas', bbox)
def redraw_coquitlam(cq):
    """Replace only the rings of the two flagged areas; every other area record is kept as loaded (byte-identical on dump)."""
    from shapely.geometry import Polygon
    ex = json.load(open(cq)); areas = ex['areas']
    polys = {a['id']: [Polygon([(p[1], p[0]) for p in r]) for r in a['rings']] for a in areas}
    for i, a in enumerate(areas):
        if a['id'] not in COQ_REDRAW: continue
        g = Polygon([(ll(x, y)[1], ll(x, y)[0]) for x, y in COQ_REDRAW[a['id']]]).buffer(0); a0 = g.area
        for eid, ps in polys.items():
            if eid == a['id']: continue
            for h in ps:
                if g.intersects(h):
                    ov = g.intersection(h).area
                    if ov > 0.003 * a0: print(f'  {a["id"]}: trimmed {100 * ov / a0:.1f}% against {eid}')
                    g = g.difference(h)
        if g.geom_type != 'Polygon': g = max([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: x.area)
        c = list(g.exterior.coords)
        b = dict(a); b['rings'] = [[[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]]]
        areas[i] = b; polys[a['id']] = [g]
    write(areas, ex, ex.get('region', 'coquitlam'), ex.get('name', 'Coquitlam'), cq)
def main():
    if '--check' in sys.argv:
        r = residuals(); print('landmark residuals (name, m north, m east):', r); print('worst', max(max(abs(a), abs(b)) for _, a, b in r), 'm')
    build(PORT_MOODY, None, 'port-moody', 'Port Moody', os.path.join(MAPS, 'port-moody.json'))
    build(PORT_COQ, None, 'port-coquitlam', 'Port Coquitlam', os.path.join(MAPS, 'port-coquitlam.json'))
    redraw_coquitlam(os.path.join(MAPS, 'coquitlam.json'))
if __name__ == '__main__': main()
