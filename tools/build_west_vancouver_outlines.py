"""Draft outlines for West Vancouver (the District: 34 sold keys, 32 drawn) -> src/data/maps/west-vancouver.json

Source: Jared's Paragon screenshots of 2026-11-05 (GVR SUB AREAS 2022 layer, code labels on, 1920 x 878).  Frames 07 (east) and 08 (central) are the same zoom
(about 6.2 m per pixel); SIFT registration (shared/register.py) puts 07 at (+775.2, +553.0) in frame 08's pixels.  Frame 06 (overview) is exactly half that zoom: it
registers to the same pixel grid at 2x (x = 2 * x06 - 1450.6, y = 2 * y06 - 145), so the Howe Sound strip, Cypress Park Estates, Glenmore and the south tip of Caulfeild
were read from it (about 12 m per pixel) and everything else from the close-ups.  Frame 09 has no polygons (the layer had not loaded) and is not used.  Polygon vertices were
read by eye from gridded 2x to 5x crops (saturation-boosted copies show the white polygon boundaries; the fills are NOT boundaries, Paragon's tint over Google's parks and
water changes the shade inside one polygon).  All coordinates below are pixels of frame 08 (the 'mosaic').
Names: codes follow shared/pk2 NOTES.md; the 34 sold keys and the 32 visible codes pair one to one once CP = Chelsea Park, WE = Westhill, WM = Westmount, DR = Deer Ridge,
CE = Cypress Park Estates, PR = Park Royal, RR = Rockridge, BR = Bayridge, OC = Olde Caulfeild, QU = Queens, CY = Cypress are accepted (see the report for how sure each is).
Calibration: Web Mercator fit (separate x and y scale) to the landmark icons in LAND below, coordinates from OpenStreetMap (Nominatim; Google Maps is CAPTCHA-blocked).
Icons are anchored at the TIP of Google's pin, about 14.5 px below the circle centre (the same icons read in the 2x zoomed-out overview differ from the close-up by exactly
that, which settles it), so LAND uses the tip.  Nine icons were matched, OpenStreetMap coordinates through Nominatim's data (read via the Photon geocoder, because Nominatim itself
returned 429 to the shared IP for the whole session): Cypress Lookout (OSM 'High View Lookout' viewpoint), West Bay Park, Susu Bend Park (OSM 'Suicide Bend Park' viewpoint),
Capilano Suspension Bridge Park (OSM bridge footway), Cleveland Dam, Bowen Lookout (viewpoint on Cypress Mountain), Vancouver Aquarium, Cates Bay Beach (Bowen Island); the last
three are read from the overview and the west frame 09 (same zoom as the overview), which is why the fit spans 3,200 px.  `--check` prints the misses: worst 43 m.
Dropped as outliers: Cypress Falls Park (-237 m; the OSM park centroid is not where Google puts the icon), Cypress Provincial Park Picnic Area (-71 m, an OSM locality node),
Capilano Suspension Bridge Park centroid (+103 m, used the bridge footway instead), Mt Gardner (+193 m, Google's lookout pin is not the OSM summit), Prospect Point (-68 m).
Clipped / not drawn: Howe Sound (HS) and Cypress Park Estates (CE) are cut flat at the top of the overview frame (y06 = 35); Lions Bay and Furry Creek are not on any frame
(the strip north of that edge) and are not drawn.  The east edge of British Properties and Glenmore (x = 2158) is the District line at the Capilano River as Paragon draws it.
Park Royal (PR) is one polygon on the layer that also covers the Capilano Indian Reserve east of the river.  19 areas have no page and are kept out of the JSON (HELD).
Every area stays 'draft'.
  python3 -I tools/build_west_vancouver_outlines.py [--check]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MAPS = os.path.join(ROOT, 'src/data/maps')
LAND = [  # (pixel x, pixel y of the pin TIP in frame-08 pixels, lat, lng, name)
    (1458, 545.5, 49.35296, -123.17811, 'Cypress Lookout (OSM High View Lookout)'), (1060, 761.3, 49.34086, -123.21208, 'West Bay Park'),
    (978.8, 807, 49.33828, -123.21904, 'Susu Bend Park (OSM Suicide Bend viewpoint)'), (2193.8, 727.3, 49.34290, -123.11510, 'Capilano Suspension Bridge Park (footway)'),
    (2241, 412, 49.36016, -123.11052, 'Cleveland Dam'), (1043.4, -412.5, 49.40640, -123.21372, 'Bowen Lookout'), (2009.4, 1483.6, 49.30052, -123.13122, 'Vancouver Aquarium'),
    (-130.6, -568.5, 49.41433, -123.31494, 'Cates Bay Beach (Bowen Island)')]
HAVE_PAGE = {'altamont', 'ambleside', 'bayridge', 'british-properties', 'canterbury-wv', 'caulfeild', 'cedardale', 'chartwell', 'chelsea-park', 'cypress-park-estates',
             'dundarave-west-vancouver-guide', 'park-royal-west-vancouver-guide', 'whitby-estates-west-vancouver-guide'}   # the others are HELD: drawn, kept out of the JSON
AREAS = [  # (code, sold key, page slug, name, [pixel rings]); order = priority (earlier areas win overlaps)
 ('WC', 'West Vancouver|Whytecliff', 'whytecliff-west-vancouver', 'Whytecliff',
  [[(157, 115), (161, 128), (157, 137), (175, 144), (200, 128), (218, 108), (236, 99), (266, 92), (277, 87), (261, 142), (248, 167), (230, 201), (218, 235), (214, 203), (200, 215), (175, 222), (150, 219), (127, 205), (116, 196), (114, 180), (127, 170), (139, 155), (145, 144), (141, 133), (136, 118)]]),
 ('HB', 'West Vancouver|Horseshoe Bay WV', 'horseshoe-bay-west-vancouver', 'Horseshoe Bay',
  [[(277, 87), (295, 68), (314, 57), (334, 52), (338, 70), (338, 92), (339, 117), (359, 122), (370, 125), (375, 145), (372, 180), (357, 237), (332, 259), (325, 254), (302, 257), (275, 243), (259, 245), (236, 270), (221, 271), (221, 245), (218, 235), (230, 201), (248, 167), (261, 142)]]),
 ('HS', 'West Vancouver|Howe Sound', 'howe-sound-west-vancouver', 'Howe Sound',
  [[(332, 259), (357, 237), (372, 180), (375, 145), (385, 127), (400, 100), (417, 55), (427, 31), (450, 4), (476, -20), (495, -52), (504, -72), (642, -72), (640, -70), (600, -25), (560, 15), (525, 60), (500, 97), (487, 125), (465, 210), (447, 266)]]),
 ('GL', 'West Vancouver|Gleneagles', 'gleneagles-west-vancouver', 'Gleneagles',
  [[(221, 271), (236, 271), (259, 245), (275, 243), (302, 257), (325, 254), (320, 300), (315, 345), (306, 362), (300, 385), (292, 420), (281, 452), (272, 475), (257, 466), (232, 461), (217, 452), (215, 437), (220, 425), (232, 412), (237, 397), (225, 390), (200, 380), (187, 365), (181, 347), (184, 335), (186, 312), (200, 294)]]),
 ('ER', 'West Vancouver|Eagleridge', 'eagleridge-west-vancouver', 'Eagleridge',
  [[(306, 362), (315, 380), (325, 395), (340, 404), (360, 404), (390, 404), (425, 406), (400, 425), (390, 437), (395, 442), (424, 434), (407, 461), (400, 459), (372, 462), (365, 475), (347, 482), (337, 490), (327, 502), (317, 510), (295, 502), (277, 492), (272, 475), (281, 452), (292, 420), (300, 385)]]),
 ('EH', 'West Vancouver|Eagle Harbour', 'eagle-harbour-west-vancouver', 'Eagle Harbour',
  [[(425, 406), (450, 392), (490, 394), (520, 400), (545, 415), (565, 432), (577, 455), (581, 480), (575, 500), (560, 512), (555, 513), (545, 527), (532, 542), (527, 552), (525, 572), (495, 585), (470, 593), (430, 590), (402, 592), (385, 575), (390, 565), (387, 545), (372, 540), (370, 507), (380, 502), (395, 495), (405, 480), (405, 462), (407, 461), (424, 434), (397, 428)], [(335, 505), (347, 505), (355, 520), (365, 535), (368, 547), (360, 555), (342, 560), (327, 557), (322, 545), (325, 530), (329, 515)]]),
 ('UC', 'West Vancouver|Upper Caulfeild', 'upper-caulfeild-west-vancouver', 'Upper Caulfeild',
  [[(555, 512), (565, 522), (572, 535), (585, 555), (602, 569), (625, 575), (650, 582), (646, 585), (640, 617), (620, 642), (605, 640), (576, 635), (577, 649), (535, 669), (522, 660), (475, 667), (477, 617), (492, 610), (522, 580), (525, 572), (527, 552), (532, 542), (545, 527)]]),
 ('OC', 'West Vancouver|Olde Caulfeild', 'olde-caulfeild-west-vancouver', 'Olde Caulfeild',
  [[(460, 767), (467, 758), (493, 751), (517, 758), (533, 770), (567, 768), (600, 759), (633, 755), (675, 755), (679, 763), (657, 772), (633, 777), (627, 793), (613, 817), (590, 821), (575, 810), (567, 803), (570, 827), (575, 860), (572, 877), (560, 892), (540, 901), (517, 910), (502, 907), (493, 923), (490, 923), (483, 907), (477, 873), (473, 840), (470, 810), (460, 783)]]),
 ('CA', 'West Vancouver|Caulfeild', 'caulfeild', 'Caulfeild',
  [[(393, 587), (400, 592), (467, 594), (495, 582), (520, 580), (585, 565), (650, 582), (665, 587), (682, 597), (690, 610), (680, 617), (702, 649), (712, 675), (717, 691), (722, 702), (715, 708), (695, 712), (677, 721), (675, 757), (633, 755), (600, 759), (567, 768), (533, 770), (517, 758), (493, 751), (467, 758), (460, 767), (460, 783), (470, 810), (473, 840), (477, 873), (483, 907), (490, 923), (489, 940), (473, 954), (448, 961), (433, 950), (421, 928), (423, 907), (413, 879), (401, 857), (393, 840), (379, 822), (393, 807), (399, 780), (398, 750), (408, 723), (417, 703), (411, 683), (393, 660), (371, 652), (361, 644), (371, 637), (393, 623), (397, 603)]]),
 ('RR', 'West Vancouver|Rockridge', 'rockridge-west-vancouver', 'Rockridge',
  [[(696, 606), (725, 612), (758, 620), (765, 631), (773, 647), (777, 656), (775, 681), (769, 693), (768, 716), (766, 729), (754, 725), (717, 712), (719, 700), (712, 681), (704, 655), (698, 650), (679, 620), (685, 616)]]),
 ('CY', 'West Vancouver|Cypress', 'cypress-west-vancouver', 'Cypress',
  [[(677, 726), (687, 716), (717, 712), (754, 725), (767, 729), (769, 737), (777, 744), (778, 768), (786, 769), (800, 769), (809, 774), (815, 776), (812, 784), (800, 791), (784, 798), (776, 803), (750, 808), (740, 807), (724, 801), (708, 791), (692, 777), (681, 762), (676, 739)]]),
 ('SC', 'West Vancouver|Sandy Cove', 'sandy-cove-west-vancouver', 'Sandy Cove',
  [[(777, 744), (779, 746), (796, 732), (804, 726), (816, 720), (828, 715), (840, 715), (852, 717), (870, 723), (888, 721), (900, 712), (912, 706), (919, 711), (917, 722), (919, 737), (929, 747), (942, 745), (939, 705), (955, 711), (966, 715), (970, 727), (965, 745), (955, 757), (942, 769), (927, 762), (917, 761), (900, 762), (883, 757), (867, 757), (846, 760), (829, 764), (817, 775), (815, 776), (778, 768)]]),
 ('BR', 'West Vancouver|Bayridge', 'bayridge', 'Bayridge',
  [[(757, 620), (788, 616), (825, 618), (858, 627), (900, 641), (942, 657), (963, 663), (983, 669), (987, 679), (985, 690), (979, 697), (976, 705), (972, 712), (966, 715), (955, 711), (939, 705), (942, 745), (929, 747), (919, 737), (917, 722), (919, 711), (912, 706), (900, 712), (888, 721), (870, 723), (852, 717), (840, 715), (828, 715), (816, 720), (804, 726), (796, 732), (778, 740), (775, 732), (768, 716), (769, 693), (775, 681), (777, 656), (773, 647), (765, 631)]]),
 ('WB', 'West Vancouver|West Bay', 'west-bay-west-vancouver', 'West Bay',
  [[(900, 762), (917, 761), (927, 762), (942, 769), (955, 757), (965, 745), (970, 727), (992, 727), (1002, 725), (1015, 727), (1017, 740), (1025, 745), (1034, 744), (1035, 731), (1050, 730), (1065, 735), (1080, 739), (1097, 745), (1112, 747), (1127, 750), (1153, 756), (1170, 769), (1170, 808), (1162, 813), (1148, 789), (1133, 781), (1122, 772), (1107, 776), (1092, 776), (1085, 770), (1077, 765), (1062, 762), (1057, 762), (1054, 775), (1050, 782), (1040, 785), (1030, 787), (1020, 795), (1005, 802), (990, 807), (977, 809), (965, 806), (955, 800), (945, 795), (927, 790), (912, 782), (902, 770)]]),
 ('WM', 'West Vancouver|Westmount WV', 'westmount-wv', 'Westmount',
  [[(990, 677), (1010, 671), (1030, 669), (1055, 667), (1080, 668), (1115, 666), (1149, 661), (1177, 663), (1176, 731), (1168, 736), (1170, 769), (1153, 756), (1127, 750), (1112, 747), (1097, 745), (1080, 739), (1065, 735), (1050, 730), (1035, 731), (1034, 744), (1025, 745), (1017, 740), (1015, 727), (1002, 725), (992, 727), (968, 724), (966, 716), (972, 712), (976, 705), (979, 697), (985, 690), (987, 680)]]),
 ('DR', 'West Vancouver|Deer Ridge WV', 'deer-ridge-wv', 'Deer Ridge',
  [[(1149, 619), (1165, 617), (1180, 619), (1204, 623), (1233, 626), (1248, 629), (1256, 635), (1254, 639), (1239, 644), (1215, 646), (1198, 648), (1177, 653), (1151, 659), (1146, 656), (1136, 639), (1139, 629)]]),
 ('AL', 'West Vancouver|Altamont', 'altamont', 'Altamont',
  [[(1177, 658), (1198, 656), (1221, 653), (1245, 652), (1268, 657), (1283, 664), (1292, 656), (1309, 653), (1309, 760), (1317, 792), (1315, 804), (1309, 819), (1301, 831), (1298, 841), (1309, 856), (1283, 858), (1265, 851), (1256, 840), (1248, 831), (1236, 822), (1224, 816), (1212, 810), (1198, 805), (1177, 808), (1170, 808), (1170, 769), (1168, 736), (1176, 731)]]),
 ('CP', 'West Vancouver|Chelsea Park', 'chelsea-park', 'Chelsea Park',
  [[(1307, 595), (1315, 588), (1323, 586), (1338, 587), (1360, 592), (1365, 597), (1370, 608), (1383, 622), (1397, 628), (1427, 633), (1429, 647), (1431, 667), (1430, 683), (1426, 697), (1407, 694), (1390, 694), (1375, 690), (1360, 683), (1345, 673), (1330, 662), (1313, 652), (1310, 650), (1302, 623), (1303, 612)]]),
 ('PV', 'West Vancouver|Panorama Village', 'panorama-village-west-vancouver', 'Panorama Village',
  [[(1429.3, 634.0), (1453.3, 630.7), (1496.7, 629.3), (1507.3, 630.0), (1507.3, 636.7), (1500.7, 643.3), (1490.0, 646.7), (1493.3, 653.3), (1526.7, 651.7), (1541.7, 651.7), (1543.3, 655.0), (1556.7, 663.3), (1570.0, 676.7), (1575.0, 693.3), (1576.7, 700.0), (1576.7, 705.0), (1570.0, 710.0), (1546.7, 711.7), (1526.7, 713.3), (1513.3, 710.7), (1496.7, 706.7), (1473.3, 705.0), (1453.3, 700.0), (1433.3, 698.3), (1426.7, 696.7), (1430.0, 683.3), (1430.7, 666.7), (1429.3, 646.7)]]),
 ('WE', 'West Vancouver|Westhill', 'westhill-west-vancouver', 'Westhill',
  [[(1320.0, 536.7), (1343.3, 535.0), (1363.3, 538.3), (1386.7, 540.0), (1413.3, 546.7), (1436.7, 548.7), (1453.3, 557.3), (1471.7, 560.0), (1493.3, 548.3), (1526.7, 539.3), (1555.0, 535.0), (1554.3, 568.3), (1556.7, 590.0), (1561.7, 604.0), (1566.0, 610.7), (1540.0, 615.0), (1531.7, 621.7), (1528.3, 626.7), (1535.0, 640.0), (1541.7, 651.7), (1526.7, 651.7), (1493.3, 653.3), (1490.0, 646.7), (1500.7, 643.3), (1506.7, 636.7), (1507.3, 630.0), (1496.7, 629.3), (1453.3, 630.7), (1429.3, 633.3), (1406.7, 631.7), (1390.0, 626.7), (1380.0, 620.0), (1367.3, 606.7), (1365.0, 596.7), (1360.0, 591.7), (1338.3, 587.3), (1323.3, 586.0), (1316.7, 588.7), (1318.3, 580.0), (1315.0, 566.7), (1317.3, 551.7)]]),
 ('WH', 'West Vancouver|Whitby Estates', 'whitby-estates-west-vancouver-guide', 'Whitby Estates',
  [[(1537, 615), (1573, 615), (1600, 617), (1610, 623), (1642, 624), (1665, 627), (1669, 640), (1673, 645), (1673, 680), (1663, 684), (1662, 699), (1663, 708), (1640, 706), (1600, 704), (1577, 701), (1575, 693), (1570, 677), (1557, 663), (1542, 652), (1535, 640), (1528, 627)]]),
 ('CB', 'West Vancouver|Canterbury WV', 'canterbury-wv', 'Canterbury',
  [[(1556, 537), (1580, 530), (1613, 525), (1640, 522), (1677, 514), (1681, 534), (1687, 548), (1690, 558), (1663, 562), (1663, 607), (1643, 615), (1642, 623), (1610, 623), (1600, 617), (1573, 615), (1566, 610), (1555, 597), (1556, 570)]]),
 ('CW', 'West Vancouver|Chartwell', 'chartwell', 'Chartwell',
  [[(1699, 484), (1748, 520), (1751, 537), (1769, 532), (1800, 523), (1810, 538), (1815, 551), (1821, 568), (1824, 586), (1830, 609), (1837, 634), (1843, 650), (1847, 665), (1831, 668), (1819, 678), (1808, 693), (1792, 707), (1773, 716), (1746, 721), (1725, 723), (1688, 717), (1654, 712), (1663, 710), (1662, 699), (1663, 685), (1673, 681), (1673, 645), (1669, 634), (1666, 626), (1663, 595), (1662, 573), (1663, 561), (1673, 570), (1691, 568), (1692, 555), (1687, 548), (1681, 534), (1678, 514)]]),
 ('QU', 'West Vancouver|Queens', 'queens-west-vancouver', 'Queens',
  [[(1312, 652), (1323, 655), (1347, 673), (1363, 687), (1380, 693), (1397, 697), (1427, 698), (1453, 700), (1473, 705), (1497, 707), (1513, 711), (1527, 713), (1547, 712), (1570, 710), (1577, 705), (1600, 707), (1638, 709), (1663, 713), (1673, 715), (1673, 730), (1669, 745), (1654, 761), (1632, 758), (1597, 763), (1577, 760), (1574, 757), (1448, 756), (1358, 756), (1311, 756)]]),
 ('DU', 'West Vancouver|Dundarave', 'dundarave-west-vancouver-guide', 'Dundarave',
  [[(1311, 756), (1358, 756), (1448, 756), (1574, 757), (1577, 795), (1576, 953), (1578, 985), (1581, 1005), (1553, 1000), (1527, 977), (1506, 950), (1490, 932), (1464, 916), (1427, 908), (1403, 916), (1400, 906), (1380, 885), (1343, 866), (1311, 864), (1308, 864), (1303, 816), (1311, 800)]]),
 ('AM', 'West Vancouver|Ambleside', 'ambleside', 'Ambleside',
  [[(1577, 757), (1597, 763), (1632, 758), (1664, 743), (1670, 722), (1706, 732), (1743, 745), (1785, 769), (1816, 793), (1835, 808), (1833, 993), (1827, 1011), (1839, 1014), (1839, 1082), (1829, 1099), (1807, 1089), (1786, 1068), (1768, 1054), (1761, 1021), (1743, 1014), (1700, 1008), (1658, 1006), (1611, 1007), (1581, 1005), (1578, 985), (1576, 953), (1577, 795)]]),
 ('SH', 'West Vancouver|Sentinel Hill', 'sentinel-hill-west-vancouver', 'Sentinel Hill',
  [[(1833, 806), (1876, 809), (1922, 813), (1963, 822), (1962, 941), (1935, 947), (1913, 956), (1885, 975), (1858, 990), (1833, 993)]]),
 ('CD', 'West Vancouver|Cedardale', 'cedardale', 'Cedardale',
  [[(1963, 822), (1995, 823), (2022, 825), (2035, 829), (2058, 845), (2081, 865), (2104, 888), (2126, 902), (2146, 911), (2147, 918), (2131, 927), (2104, 939), (2085, 943), (2031, 943), (1995, 943), (1962, 941)]]),
 ('PR', 'West Vancouver|Park Royal', 'park-royal-west-vancouver-guide', 'Park Royal',
  [[(1833, 993), (1858, 990), (1885, 975), (1913, 956), (1935, 947), (1962, 941), (1995, 943), (2031, 943), (2085, 943), (2089, 1007), (2096, 1054), (2104, 1071), (2132, 1073), (2136, 1100), (2127, 1143), (2121, 1168), (2104, 1193), (2086, 1229), (2073, 1255), (2050, 1263), (2021, 1244), (1986, 1214), (1970, 1196), (1977, 1180), (1971, 1163), (1957, 1154), (1936, 1139), (1929, 1123), (1887, 1121), (1882, 1091), (1839, 1082), (1839, 1014), (1827, 1011)]]),
 ('GM', 'West Vancouver|Glenmore', 'glenmore-west-vancouver', 'Glenmore',
  [[(1917, 372), (1950, 340), (1983, 293), (2007, 270), (2043, 257), (2097, 237), (2130, 230), (2158, 226), (2158, 425), (2103, 427), (2063, 433), (2017, 429), (1963, 423), (1937, 403), (1917, 383)]]),
 ('BP', 'West Vancouver|British Properties', 'british-properties', 'British Properties',
  [[(1703, 480), (1750, 458), (1817, 430), (1870, 403), (1910, 383), (1917, 383), (1937, 403), (1963, 423), (2017, 429), (2063, 433), (2103, 427), (2150, 423), (2158, 425), (2158, 911), (2147, 909), (2126, 898), (2104, 884), (2081, 861), (2058, 841), (2035, 825), (2022, 821), (1995, 819), (1963, 818), (1922, 809), (1876, 805), (1833, 803), (1816, 788), (1785, 764), (1743, 740), (1725, 725), (1746, 721), (1773, 716), (1792, 707), (1808, 693), (1819, 678), (1831, 668), (1847, 665), (1843, 650), (1837, 634), (1830, 609), (1824, 586), (1821, 568), (1815, 551), (1810, 538), (1800, 523), (1769, 532), (1751, 537), (1748, 520), (1699, 484)]]),
 ('CE', 'West Vancouver|Cypress Park Estates', 'cypress-park-estates', 'Cypress Park Estates',
  [[(447, 266), (465, 210), (487, 125), (500, 97), (525, 60), (560, 15), (600, -25), (640, -70), (642, -72), (2158, -75), (2158, 226), (2130, 230), (2097, 237), (2043, 257), (2007, 270), (1983, 293), (1950, 340), (1917, 372), (1910, 383), (1870, 403), (1817, 430), (1750, 458), (1703, 480), (1699, 484), (1678, 514), (1640, 522), (1613, 525), (1580, 530), (1556, 537), (1555, 535), (1527, 539), (1493, 548), (1472, 560), (1453, 557), (1437, 549), (1413, 547), (1387, 540), (1363, 538), (1343, 535), (1320, 537), (1317, 552), (1315, 567), (1318, 580), (1317, 589), (1307, 595), (1303, 612), (1302, 623), (1310, 650), (1309, 653), (1292, 656), (1283, 664), (1268, 657), (1245, 652), (1221, 653), (1198, 656), (1177, 658), (1177, 663), (1149, 661), (1115, 666), (1080, 668), (1055, 667), (1030, 669), (1010, 671), (990, 677), (983, 669), (963, 663), (942, 657), (900, 641), (858, 627), (825, 618), (788, 616), (757, 620), (725, 612), (696, 606), (690, 610), (682, 597), (665, 587), (650, 582), (625, 575), (602, 569), (585, 555), (572, 535), (565, 522), (555, 512), (560, 512), (575, 500), (581, 480), (577, 455), (565, 432), (545, 415), (520, 400), (490, 394), (450, 392), (425, 406), (390, 404), (360, 404), (340, 404), (325, 395), (315, 380), (306, 362), (315, 345), (320, 300), (325, 260), (332, 259)]]),
]
def merc(l): return math.log(math.tan(math.pi / 4 + math.radians(l) / 2))
def ls(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n; a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return a, my - a * mx
LX, LB = ls([p[0] for p in LAND], [p[3] for p in LAND]); MY, MB = ls([p[1] for p in LAND], [merc(p[2]) for p in LAND])
def ll(px, py): return round(math.degrees(2 * math.atan(math.exp(MY * py + MB)) - math.pi / 2), 5), round(LX * px + LB, 5)
def residuals(): return [(p[4], round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 72490)) for p in LAND]
HELD = {a[2] for a in AREAS if a[2] not in HAVE_PAGE}
def build():
    from shapely.geometry import Polygon
    from shapely.validation import make_valid
    others = []; new = []
    for code, key, slug, nm, rings_px in AREAS:
        g = None
        for ring_px in rings_px:
            p = Polygon([(ll(x, y)[1], ll(x, y)[0]) for x, y in ring_px])
            if not p.is_valid: p = make_valid(p).buffer(0)
            g = p if g is None else g.union(p)
        a0 = g.area
        for eid, h in others:
            if g.intersects(h):
                ov = g.intersection(h).area
                if ov > 0.003 * a0: print(f'  {slug}: trimmed {100 * ov / a0:.1f}% against {eid}')
                g = g.difference(h)
        parts = [g] if g.geom_type == 'Polygon' else sorted([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: -x.area)
        rings = []
        for part in parts:
            if part.area < 0.02 * a0: continue
            c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        others.append((slug, g))
        if slug in HELD: print('  HELD (no page):', slug, key); continue
        new.append({'id': slug, 'name': nm, 'href': f'/{slug}.html', 'status': 'draft', 'sold': key, 'rings': rings})
    pts = [p for a in new for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data = {'region': 'west-vancouver', 'name': 'West Vancouver', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': new}
    out = os.path.join(MAPS, 'west-vancouver.json')
    json.dump(data, open(out, 'w'), separators=(',', ':'))
    print(out.split('/')[-1], len(new), 'areas in JSON,', len(HELD), 'held', bbox)
def main():
    if '--check' in sys.argv: print('landmark residuals (name, m north, m east):', residuals())
    build()
if __name__ == '__main__': main()
