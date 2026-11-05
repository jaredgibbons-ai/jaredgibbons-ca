"""Draft outlines for the City and District of North Vancouver -> src/data/maps/north-vancouver.json  (34 sold areas drawn, 15 published, 19 HELD)

Source: five Paragon screenshots of 2026-11-05 (GVR Sub Areas 2022 layer, code labels on, 1920 x 878; map pane y 38 to 856): 01 overview (Google zoom 13) and 02 west, 03 central,
04 east, 05 north-east (02, 04 and 05 are zoom 14; 03 is zoom 15).  They were joined by SIFT feature matching into ONE mosaic in the pixel space of frame 02 ("mosaic units", about
6.2 m each): 04 at (+1571.8, +158.1), 05 at (+2179.4, -175.1), 03 at 0.49994 x + (958.3, 271.0), the overview at 2 x + (23.5, -695.8).  Vertices below are read by eye from gridded crops
of that mosaic (3x to 5x for the busy parts) and are in mosaic units (x right, y down).  The colours are NOT boundaries (Paragon tints the basemap's parks and water); only the white lines are.
Calibration: Web Mercator with the exact zoom-14 scale (8.5831e-5 deg lon per unit, square pixels; a free least-squares scale came out within 0.25% of it), offsets fitted to eleven landmark ICONS whose
coordinates come from OpenStreetMap (Nominatim; Google Maps is CAPTCHA-blocked).  `--check` prints the misses: 8 to 52 m on the eleven used.  Dropped as outliers (OSM point is not where Google puts the icon):
Cleveland Dam (+147 m N, long dam way), Prospect Point (+144 m N, cafe not lookout), Tempe Heights Park (119 m E, park centroid), Carson Graham Secondary (100 m), Lucas Centre (96 m), Thwaytes Landing and
Buntzen Lake (nature-reserve centroids, 170 m and 900 m).  All landmarks lie in the west and middle of the mosaic (Capilano to Jug Island), so the far north and the Indian Arm shore rest on the scale, not on a landmark.
Clipped on purpose: Canyon Heights NV and Grouse Woods run on north past the top of the overview (mosaic y -620), as does the Grouse Mountain / Mt Fromme country; both stop at the frame edge.
Not drawn: Hamilton (HS on the layer is read as Harbourside, see below), Capilano reserve (PR), Cypress Provincial Park (CE), Indian Arm (AN), the unlabelled catch-all (ZZ), Glenmore (GM) and the West Vancouver codes.
Code reading (the notes' code list is a best reading): CA Capilano NV, PN Pemberton NV, PH Pemberton Heights, NG Norgate, MC Mosquito Creek, ED Edgemont, DE Delbrook, UD Upper Delbrook, FH Forest Hills NV, UL Upper Lonsdale,
CL Central Lonsdale, LL Lower Lonsdale, BD Boulevard, QU Queensbury, CV Calverhall, TE Tempe, PP Princess Park, BR Braemar, CY Canyon Heights NV, GW Grouse Woods (two label spots, one polygon: the lake and the slope above it),
LV Lynn Valley, WL Westlynn, WT Westlynn Terrace, LY Lynnmour (one long polygon from the Capilano University area up the Lynn Creek valley to the catch-all line), SY Seymour NV (Maplewood flats and the Seymour River strip),
BL Blueridge NV, WP Windsor Park NV, RP Roche Point, DO Dollarton, DC Deep Cove, IR Indian River (the stepped Cove Forest polygon), NL Northlands, WS Woodlands-Sunshine-Cascade.  HS (grey, Marine Dr / W 1st / Fell Ave, between Norgate and
Lower Lonsdale) is called Hamilton in the notes, but 'Harbourside' is the only sold key left over and Harbourside Drive is at its east end, so it is drawn as Harbourside; there is no Hamilton key.
HELD (drawn, kept out of the JSON because the site has no page for the area): Forest Hills NV, Grouse Woods, Harbourside, Indian River, Lower Lonsdale, Lynn Valley, Mosquito Creek, Northlands, Pemberton NV, Princess Park,
Queensbury, Roche Point, Seymour NV, Tempe, Upper Delbrook, Westlynn, Westlynn Terrace, Windsor Park NV, Woodlands-Sunshine-Cascade (ids are the slugs a page should use).  Edgemont, Lynnmour, Norgate, Pemberton Heights and
Upper Lonsdale link to their -guide pages (no plain page).  Every area stays 'draft'.
  python3 -I tools/build_north_vancouver_outlines.py [--check] [--held-to PATH]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'src/data/maps/north-vancouver.json')
LX = 360 / (256 * 2 ** 14)          # degrees of longitude per mosaic unit (Google zoom 14)
MY = -math.radians(LX)              # Mercator-y per mosaic unit (square pixels, y down)
LAND = [  # (mosaic x, mosaic y, lat, lng, name): OpenStreetMap coordinates, icon centres read on the mosaic
    (1583.75, 512.5, 49.3209784, -123.0676719, 'Lions Gate Hospital'), (1041.8, 113, 49.3429014, -123.1151049, 'Capilano Suspension Bridge'),
    (2156.8, 556, 49.3179806, -123.0194770, 'Capilano University'), (1848, 336, 49.3305938, -123.0459196, 'Karen Magnussen CRC'),
    (3366.4, 344.9, 49.3299725, -122.9148784, 'Jug Island Beach'), (1443.5, 683.5, 49.3112814, -123.0804810, 'Museum of North Vancouver'),
    (1180.75, 324.5, 49.3313053, -123.1031830, 'Sowden Park'), (1419, 457.5, 49.3241289, -123.0818544, 'Fen Burdett Stadium'),
    (1912.3, 440.9, 49.3248743, -123.0400113, 'Eastview Elementary'), (1750.5, 511.8, 49.3209427, -123.0541672, 'North Shore Christian Centre'),
    (1126.5, 427, 49.3256208, -123.1075893, 'Ashdown Park')]
def merc(l): return math.log(math.tan(math.pi / 4 + math.radians(l) / 2))
LB = sum(p[3] - LX * p[0] for p in LAND) / len(LAND)
MB = sum(merc(p[2]) - MY * p[1] for p in LAND) / len(LAND)
def ll(x, y): return round(math.degrees(2 * math.atan(math.exp(MY * y + MB)) - math.pi / 2), 5), round(LX * x + LB, 5)
def residuals(): return [(p[4], round((ll(p[0], p[1])[0] - p[2]) * 111200), round((ll(p[0], p[1])[1] - p[3]) * 72430)) for p in LAND]
# (sold key, id, name, page slug or None = HELD, outline in mosaic units).  Order matters: each outline gives way to the ones before it.
AREAS = [
 ('Forest Hills NV', 'forest-hills-nv', 'Forest Hills', None,
  [(1224,-21.7),(1274,-48),(1328,-48),(1343.5,-37),(1369.6,-13),(1368.7,28),(1363,50),(1348,63),(1348.7,110),(1343.5,109),(1261,97),(1230,100),(1202,102),(1201,93.5),(1239,80.4),(1242.6,74),(1241,19.6),(1228,-4)]),
 ('Princess Park', 'princess-park', 'Princess Park', None,
  [(1670,87.5),(1750,85),(1800,104),(1817.5,105),(1817.5,130),(1800,145),(1777.5,156),(1782.5,190),(1786,235),(1770,255),(1675,256),(1675,142.5),(1664,130),(1659,110)]),
 ('Braemar', 'braemar', 'Braemar', 'braemar',
  [(1712,-127),(1880,-127),(1880,5),(1882.5,37.5),(1860,47.5),(1832.5,62.5),(1840,80),(1842.5,105),(1800,104),(1750,85),(1670,87.5),(1640,92.5),(1637.5,85),(1640,55),(1712.5,1)]),
 ('Tempe', 'tempe', 'Tempe', None,
  [(1718,258),(1765,257),(1764.4,281),(1763.6,351),(1761.6,363),(1760,373),(1750,361),(1736,345),(1718,333),(1700,323),(1679,321),(1689,301),(1700,290),(1721.6,267)]),
 ('Westlynn Terrace', 'westlynn-terrace', 'Westlynn Terrace', None,
  [(1997.7,247.7),(2122.7,251),(2153.6,270.5),(2148.6,285.5),(2127,302),(2107,317),(2100,341),(2101.8,377),(2108,404.5),(2100,418),(2072.7,441),(2059,452),(2047.7,443),(2033,436),(2031,395.5),(2027,368),(2036,341),(2042,322.7),(2036,300),(2016,288.6),(1993,272.7)]),
 ('Westlynn', 'westlynn', 'Westlynn', None,
  [(1764,366),(1811,334),(1918,402),(1940,386),(1942,245),(1993,252),(1998,277),(2036,295),(2043,323),(2032,355),(2029.5,386),(2032,427),(2039,445),(2057,452),(2050,473),(2032,527),(2009,564),(1998,582),(1995,640),(1963,637),(1938,617),(1936,609),(1916,564),(1893,525),(1886,509),(1868,464),(1845,445),(1795,414),(1761,369)]),
 ('Calverhall', 'calverhall', 'Calverhall', 'calverhall',
  [(1777,612),(1800,598),(1889,526),(1916,564),(1937,620),(1934,660),(1931,715),(1929,765),(1882,765),(1882,716),(1845,714),(1776,725)]),
 ('Boulevard', 'boulevard', 'Boulevard', 'boulevard',
  [(1678,321),(1700,327),(1732,348),(1761,369),(1795,414),(1845.5,445.5),(1868,463.6),(1884,504.5),(1895,527),(1800,598),(1777,611),(1777,652),(1681.5,651.5),(1684,430),(1672,426),(1661,409),(1653.6,382),(1653.6,361),(1660,353),(1669,339)]),
 ('Queensbury', 'queensbury', 'Queensbury', None,
  [(1681.5,651.5),(1777,652),(1776,725),(1845,714),(1882,716),(1882,765),(1928,765),(1925,910),(1900,901),(1892,874),(1817,852),(1802,840),(1830,817),(1750,817),(1737,805),(1732,786),(1685,791)]),
 ('Lower Lonsdale', 'lower-lonsdale', 'Lower Lonsdale', None,
  [(1318,534),(1442,537),(1499,570),(1550,612),(1605,648),(1681,651),(1681,792),(1630,802),(1600,810),(1570,805),(1550,800),(1520,780),(1505,770),(1470,740),(1440,715),(1402,722),(1370,668),(1322,660),(1337,625),(1342,605),(1332,592),(1319,586)]),
 ('Harbourside', 'harbourside', 'Harbourside', None,
  [(1191.9,467.5),(1317.8,534.4),(1318.8,586.2),(1331.9,591.6),(1341.2,607.2),(1335.6,624.4),(1320.9,658.8),(1317.8,662.5),(1195.9,656.2),(1191.9,586.9),(1189.7,571.2),(1190.6,533.8)]),
 ('Norgate', 'norgate-north-vancouver-guide', 'Norgate', 'norgate-north-vancouver-guide',
  [(983.4,465.6),(1191.2,467.5),(1190.6,533.8),(1188.8,571.2),(1186.6,596.2),(1183.4,641.6),(1185,705),(1175.6,704.1),(1175,665),(1174.1,644.7),(1135,644.7),(1131.2,665),(1131.2,699.4),(1060,699.4),(1050.6,738.4),(1039.7,741.6),(1010,722.8),(985,702.5),(963.1,696.2),(916.2,663.4),(935,627.5),(960,593.1),(967.8,580.6),(980.3,565),(982.5,533.8),(981.9,494.7)]),
 ('Mosquito Creek', 'mosquito-creek', 'Mosquito Creek', None,
  [(1197.5,316),(1354.5,321),(1354,360),(1350,371),(1340,397.5),(1339,442.5),(1320,457.5),(1319,480),(1317.5,532.5),(1192,467.5),(1217.5,440),(1222,430),(1226,400),(1214,355),(1211,331)]),
 ('Pemberton Heights', 'pemberton-heights-north-vancouver-guide', 'Pemberton Heights', 'pemberton-heights-north-vancouver-guide',
  [(1041.2,315),(1197.5,315),(1211.2,331.2),(1213.8,355),(1226.2,400),(1222.5,430),(1208,443),(1123.8,448.8),(1066.2,412.5),(1022.5,402.5),(1022.5,333.8),(1038.8,330),(1041.2,323.8)]),
 ('Pemberton NV', 'pemberton-nv', 'Pemberton', None,
  [(1000,313.8),(1041.2,315),(1041.2,323.8),(1038.8,330),(1022.5,333.8),(1022.5,402.5),(1066.2,412.5),(1123.8,448.8),(1208,443),(1217.5,440),(1192,467.5),(983.4,465.6),(957.5,476.2),(953.8,462.5),(932.5,452.5),(932.5,341.2),(1000,336.2)]),
 ('Capilano NV', 'capilano-nv', 'Capilano', 'capilano-nv',
  [(1006.5,170),(1017,170),(1065,187),(1139,202),(1135,228),(1139,272),(1182.6,276),(1198,311),(1006.5,303)]),
 ('Edgemont', 'edgemont-north-vancouver-guide', 'Edgemont', 'edgemont-north-vancouver-guide',
  [(1063,85),(1102,65),(1143.5,49),(1150,50),(1191,80.4),(1201,93.5),(1202,102),(1230,100),(1261,97),(1343.5,109),(1350,110),(1337,130),(1319.6,163),(1304,180),(1299,206),(1290,246),(1295.6,285),(1301,317),(1198,311),(1182.6,276),(1139,272),(1135,228),(1139,202),(1065,187),(1017,170),(1043.5,141)]),
 ('Delbrook', 'delbrook', 'Delbrook', 'delbrook',
  [(1350,110),(1365,117),(1430,119),(1454,123),(1454,206.5),(1389,206.5),(1389,256.5),(1291,256.5),(1290,246),(1299,206),(1304,180),(1319.6,163),(1337,130)]),
 ('Upper Delbrook', 'upper-delbrook', 'Upper Delbrook', None,
  [(1372,-20),(1400,-63),(1435,-98),(1478,-150),(1517,-186),(1630,-186),(1585,-76),(1548,6.5),(1543.5,35),(1528,50),(1500,68),(1456.5,77),(1452,98),(1435,117),(1430,120),(1365,117),(1350,110),(1348.7,110),(1348,63),(1363,50),(1368.7,28),(1369.6,-13)]),
 ('Upper Lonsdale', 'upper-lonsdale-north-vancouver-guide', 'Upper Lonsdale', 'upper-lonsdale-north-vancouver-guide',
  [(1630,-186),(1680,-136),(1713,-130),(1712.5,1),(1640,55),(1637.5,85),(1640,92.5),(1670,87.5),(1659,110),(1664,130),(1675,142.5),(1675,256),(1718,258),(1722,267),(1700,290),(1689,301),(1679,321),(1301,317),(1295.6,285),(1291,256.5),(1389,256.5),(1389,206.5),(1454,206.5),(1454,123),(1430,120),(1435,117),(1452,98),(1456.5,77),(1500,68),(1528,50),(1543.5,35),(1548,6.5),(1585,-76)]),
 ('Central Lonsdale', 'central-lonsdale', 'Central Lonsdale', 'central-lonsdale',
  [(1354.5,321),(1678,321),(1669,339),(1660,353),(1653.6,361),(1653.6,382),(1661,409),(1672,426),(1684,430),(1684,652),(1681.5,651.5),(1605,648),(1550,612),(1499,570),(1442,537),(1318,534),(1317.5,532.5),(1319,480),(1320,457.5),(1339,442.5),(1340,397.5),(1350,371),(1354,360)]),
 ('Lynn Valley', 'lynn-valley', 'Lynn Valley', None,
  [(1772,-548),(1950,-484.5),(1952,-430),(1968,-394),(1975,-339),(1993,-303),(2002,-266),(2027,-230),(2054.5,-198),(2086,-153),(2095,-130),(2100,-112),(2120,-100),(2150,-55),(2157,-25),(2142,-2.5),(2136,35),(2137.5,62.5),(2170,85),(2190,120),(2187.5,147.5),(2197.5,175),(2205,205),(2202.5,235),(2190,250),(2154,269),(2122,251),(1993,252),(1942,245),(1940,386),(1918,402),(1811,334),(1761,366),(1761.6,363),(1763.6,351),(1764.4,281),(1765,257),(1770,255),(1786,235),(1782.5,190),(1777.5,156),(1800,145),(1817.5,130),(1817.5,105),(1842.5,105),(1840,80),(1832.5,62.5),(1860,47.5),(1882.5,37.5),(1880,5),(1880,-127),(1713,-130),(1680,-136),(1633,-186),(1650,-244),(1677,-303),(1709,-394),(1752,-494)]),
 ('Lynnmour', 'lynnmour-north-vancouver-guide', 'Lynnmour', 'lynnmour-north-vancouver-guide',
  [(1950,-484.5),(2400,-371),(2407,-344),(2404.5,-325),(2386,-312),(2359,-305),(2341,-293.6),(2341,-284.5),(2377,-257),(2395,-234.5),(2399,-180),(2386,-148),(2359,-130),(2341,-125.5),(2339,-122.6),(2365,-75),(2326,21),(2369.6,55.6),(2361,99),(2368,150),(2370,170),(2359,200),(2348,241),(2334,300),(2327,332),(2248,313),(2236,345.5),(2218,400),(2200,468),(2191,498),(2193,527),(2188.6,559),(2177,604.5),(2173,629),(2130,643),(2110,660),(2087,677),(2062,697),(2060,713),(2058,747),(2060,780),(2065,813),(2073,847),(2072,903),(2033,903),(2035,945),(2030,945),(1925,923),(1930,880),(1930,813),(1925,793),(1923,777),(1930,737),(1931.7,713),(1933,680),(1935,647),(1938,617),(1963,637),(1995,640),(1998,582),(2009,564),(2032,527),(2050,473),(2059,452),(2072.7,441),(2100,418),(2108,404.5),(2101.8,377),(2100,341),(2107,317),(2127,302),(2148.6,285.5),(2153.6,270.5),(2154,269),(2190,250),(2202.5,235),(2205,205),(2197.5,175),(2187.5,147.5),(2190,120),(2170,85),(2137.5,62.5),(2136,35),(2142,-2.5),(2157,-25),(2150,-55),(2120,-100),(2100,-112),(2095,-130),(2086,-153),(2054.5,-198),(2027,-230),(2002,-266),(1993,-303),(1975,-339),(1968,-394),(1952,-430)]),
 ('Seymour NV', 'seymour-nv', 'Seymour', None,
  [(2248,313),(2327,332),(2347.7,329.5),(2343,363.6),(2313.6,395.5),(2293,422.7),(2273.6,459),(2279.5,481.8),(2281,513.6),(2279.5,604.5),(2277,643),(2259,672),(2279.5,678),(2332,646),(2393,749),(2382,779.5),(2352,798),(2350,850),(2300,868),(2300,900),(2282,923),(2257,945),(2200,950),(2135,925),(2090,945),(2072,905),(2072,903),(2073,847),(2065,813),(2060,780),(2058,747),(2060,713),(2062,697),(2087,677),(2110,660),(2130,643),(2173,629),(2177,604.5),(2188.6,559),(2193,527),(2191,498),(2200,468),(2218,400),(2236,345.5)]),
 ('Blueridge NV', 'blueridge-nv', 'Blueridge', 'blueridge-nv',
  [(2366,314.5),(2511,320.5),(2511,457),(2461,455.5),(2454.5,463.6),(2450,486),(2445.5,509),(2445.5,611.4),(2393,613),(2332,646),(2279.5,678),(2259,672),(2277,643),(2279.5,604.5),(2281,513.6),(2279.5,481.8),(2273.6,459),(2293,422.7),(2313.6,395.5),(2343,363.6),(2347.7,329.5)]),
 ('Windsor Park NV', 'windsor-park-nv', 'Windsor Park', None,
  [(2393,613),(2602.5,615),(2606,617.5),(2597.5,665),(2586,705),(2570,722.5),(2550,740),(2527,741),(2509,759),(2486,757),(2468,736),(2427,734),(2393,749),(2332,646)]),
 ('Roche Point', 'roche-point', 'Roche Point', None,
  [(2602.5,615),(2870,610),(2872.5,710),(2870,737.5),(2844,740),(2843,775),(2865,795),(2865,810),(2825,827.5),(2802.5,837.5),(2800,845),(2745,836),(2710,825),(2680,800),(2650,770),(2610,755),(2550,740),(2570,722.5),(2586,705),(2597.5,665),(2606,617.5)]),
 ('Dollarton', 'dollarton', 'Dollarton', 'dollarton',
  [(2871,611),(2982.5,609),(2985,650),(2990,700),(2994,730),(2987.5,780),(2982.5,800),(2955,815),(2935,840),(2915,870),(2897.5,885),(2880,880),(2850,865),(2825,840),(2822.5,830),(2825,827.5),(2865,810),(2865,795),(2843,775),(2844,740),(2870,737.5),(2872.5,710)]),
 ('Deep Cove', 'deep-cove', 'Deep Cove', 'deep-cove',
  [(2897.9,351.7),(2960.4,305),(2981.2,287.1),(3066.7,285.4),(3093.8,296.7),(3100,311.2),(3066.7,318.3),(3033.3,330),(3008.3,338.3),(2991.7,355),(2975,371.7),(2975,388.3),(2983.3,409.2),(2991.7,425.8),(3008.3,432.1),(3033.3,421.7),(3066.7,425.8),(3095.8,438.3),(3114.6,446.7),(3118.8,475.8),(3120.8,496.7),(3108.3,521.7),(3100,542.5),(3070.8,559.2),(3050,563.3),(3033.3,575.8),(3027.1,588.3),(3012.5,607.1),(2983.3,617.5),(2920.8,607.1),(2910.4,600.8),(2910.4,502.9),(2895.8,475.8),(2895,388.3)]),
 ('Indian River', 'indian-river', 'Indian River', None,
  [(2745,607.1),(2745,507.1),(2754.2,507.1),(2754.2,480),(2745,477.9),(2745,446.7),(2782.5,446.7),(2782.5,432.1),(2797.9,427.9),(2799.2,392.5),(2803.3,375.8),(2814.6,373.8),(2814.6,346.7),(2822.9,344.6),(2822.9,294.6),(2838.3,292.5),(2838.3,285),(2881.2,284.2),(2883.3,230.8),(2962.5,194.6),(2962.5,169.6),(2971.7,168.8),(2971.7,161.2),(3066.7,160.4),(3066.7,284.2),(2981.2,287.1),(2960.4,305),(2897.9,351.7),(2895,388.3),(2895.8,475.8),(2910.4,502.9),(2910.4,600.8)]),
 ('Woodlands-Sunshine-Cascade', 'woodlands-sunshine-cascade', 'Woodlands-Sunshine-Cascade', None,
  [(3067,209),(3100,204),(3160,190),(3171,178),(3198,134),(3210,117.5),(3237,80),(3270,31),(3385,3),(3430,-55),(3474,-118),(3456,-79),(3446,-31),(3410,8),(3371,31),(3335,86),(3302,140),(3287,159),(3275,167),(3250,180),(3233,192),(3208,230),(3196,249),(3162,284),(3146,297),(3137,305),(3100,310),(3094,297),(3067,285)]),
 ('Grouse Woods', 'grouse-woods', 'Grouse Woods', None,
  [(941.8,-620),(1456,-620),(1298,-296),(1251,-255),(1212,-228),(1192,-228),(1192,-181),(1006.5,-181),(1006.5,-449),(941.8,-566.5)]),
 ('Canyon Heights NV', 'canyon-heights-nv', 'Canyon Heights', 'canyon-heights-nv',
  [(1456,-620),(1588,-620),(1650,-596),(1772,-548),(1752,-494),(1709,-394),(1677,-303),(1650,-244),(1633,-186),(1517,-186),(1478,-150),(1435,-98),(1400,-63),(1372,-20),(1370,-13),(1343.5,-37),(1328,-48),(1274,-48),(1224,-22),(1228,-4),(1241,20),(1243,74),(1239,80),(1201,93.5),(1191,80),(1150,50),(1143.5,49),(1102,65),(1063,85),(1043.5,141),(1017,170),(1006.5,166),(1006.5,-181),(1098,-182),(1192,-181),(1192,-228),(1212,-228),(1251,-255),(1298,-296)]),
 ('Northlands', 'northlands', 'Northlands', None,
  [(2400,-371),(2670,-361),(2850,-357),(3000,-355),(3220,-353),(3498,-355),(3498,-436),(3465,-436),(3465,-562),(3504,-562),(3504,-549),(3596,-549),(3596,-566),(3778,-566),(3787,-553),(3735,-527),(3683,-501),(3661,-466),(3670,-414),(3675,-336),(3674,-309),(3665,-266),(3622,-188),(3561,-166),(3509,-144),(3474,-118),(3430,-55),(3385,3),(3270,31),(3237,80),(3210,117.5),(3198,134),(3171,178),(3160,190),(3100,204),(3067,209),(3067,160.4),(2972,161),(2971.7,168.8),(2962.5,169.6),(2962.5,194.6),(2883,230.8),(2881,284),(2838,285),(2838,292.5),(2823,294.6),(2823,344.6),(2814.6,346.7),(2814.6,373.7),(2803,376),(2799,392.5),(2798,428),(2782.5,432),(2782.5,447),(2745,447),(2745,478),(2754,480),(2754,507),(2745,507),(2745,607),(2445.5,611),(2445.5,509),(2450,486),(2454.5,463.6),(2461,455.5),(2511,457),(2511,320.5),(2366,314.5),(2347.7,329.5),(2327,332),(2334,300),(2348,241),(2359,200),(2370,170),(2368,150),(2361,99),(2369.6,55.6),(2326,21),(2365,-75),(2339,-122.6),(2341,-125.5),(2359,-130),(2386,-148),(2399,-180),(2395,-234.5),(2377,-257),(2341,-284.5),(2341,-293.6),(2359,-305),(2386,-312),(2404.5,-325),(2407,-344)]),
]
def build(held_to=None):
    from shapely.geometry import Polygon
    from shapely.validation import make_valid
    placed = []; out = []; held = []
    for key, aid, nm, slug, poly in AREAS:
        g = Polygon([ll(x, y)[::-1] for x, y in poly])
        if not g.is_valid: g = make_valid(g).buffer(0)
        a0 = g.area
        for oid, h in placed:
            if g.intersects(h):
                ov = g.intersection(h).area
                if ov > 0.003 * a0: print(f'  {aid}: trimmed {100 * ov / a0:.1f}% against {oid}')
                g = g.difference(h)
        placed.append((aid, g))
        parts = [g] if g.geom_type == 'Polygon' else sorted([x for x in g.geoms if x.geom_type == 'Polygon'], key=lambda x: -x.area)
        rings = []
        for part in parts:
            if part.area < 0.02 * a0: continue
            c = list(part.exterior.coords); rings.append([[round(y, 5), round(x, 5)] for x, y in c[:-1]] + [[round(c[0][1], 5), round(c[0][0], 5)]])
        rec = {'id': aid, 'name': nm, 'href': f'/{slug or aid}.html', 'status': 'draft', 'sold': 'North Vancouver|' + key, 'rings': rings}
        (out if slug else held).append(rec)
    pts = [p for a in out for r in a['rings'] for p in r]; pad = 0.004
    bbox = [round(min(p[0] for p in pts) - pad, 4), round(min(p[1] for p in pts) - pad, 4), round(max(p[0] for p in pts) + pad, 4), round(max(p[1] for p in pts) + pad, 4)]
    data = {'region': 'north-vancouver', 'name': 'North Vancouver', 'center': {'lat': round((bbox[0] + bbox[2]) / 2, 4), 'lng': round((bbox[1] + bbox[3]) / 2, 4)}, 'bbox': bbox, 'areas': out}
    json.dump(data, open(OUT, 'w'), separators=(',', ':'))
    print(os.path.basename(OUT), len(out), 'areas', bbox, '| HELD (no page):', ', '.join(a['id'] for a in held))
    if held_to:
        json.dump({'region': 'north-vancouver', 'name': 'North Vancouver (held)', 'areas': held}, open(held_to, 'w'), separators=(',', ':'))
def main():
    if '--check' in sys.argv: print('landmark residuals (name, m north, m east):', residuals())
    held_to = sys.argv[sys.argv.index('--held-to') + 1] if '--held-to' in sys.argv else None
    build(held_to)
if __name__ == '__main__': main()
