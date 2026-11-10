#!/usr/bin/env python3
"""Guide format v2 (D-205) for the rural Langley ring, from Jared's Nov 10 area-guide packs (D-207).

Packs: Salmon River, Otter District, Campbell Valley, County Line / Glen Valley. What was kept, changed or dropped, and why:
  - Prices: the packs used SnapStats' Langley-wide median (SnapStats has no sub-area medians). We have Jared's own Paragon closed
    sales for each MLS sub-area (src/data/sold/sold-12m.json, board data), so the quick answer and quick facts use those, computed at
    build time; SnapStats listing counts for one month are not used.
  - Drive times re-measured: the Salmon River pack's start point (49.1430, -122.6720) is in Willoughby, not Salmon River, and the
    Otter start point sits north of Fraser Highway. All four are now measured from the middle of each MLS sub-area outline
    (src/data/maps/langley.json) on OpenStreetMap routing (OSRM, no traffic), November 10, 2026.
  - Location fixes: Otter District is the south-east corner of the Township (232 to 272 Street, Fraser Highway to the border), not the
    south-west; Salmon River is the rural middle, between Highway 1 and Fraser Highway east of Murrayville, not "northwest Langley".
  - Sources: other agents' listing pages, a councillor's blog, Wikipedia and a fan transit wiki are not used; listing-level property
    examples are left out. "No school inside Salmon River" is dropped (Coghlan Fundamental, 4452 256 Street, sits inside the outline).
  - ALR housing as the ALC states it now: a suite only inside the main house, plus one additional residence (90 m² on parcels of
    40 ha or less) without an application, if Township zoning allows.
  - Verified and used: the Province's $5M Glen Valley and Salmon River flood mitigation (BC Gov News, April 19, 2024: pumps, dike
    banks, culverts, ditches; expected complete December 2025); TransLink's summer weekend and holiday route to Campbell Valley
    Regional Park (from June 8, 2026); the Otter Co-op's 1922 farmers' institute roots.
  - Not used (couldn't confirm): the 2018 freshet property count, park hectares and trail lengths differing from the existing guide,
    route frequencies, winery addresses.
  - Verdicts: Jared's Nov 10 edits of the drafts (one-acre communities; more land by the Co-op; close to the park's horse trails; more hills,
    closer to Fort Langley). His Nov 9 words stay in his card and supply the lines marked "Jared".
python3 -I tools/build_rural_plus_2026_11_10.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
M = 'November 10, 2026'
J = 'jared'
E = {
 'salmon-river-guide': {
  'status': 'draft', 'name': 'Salmon River', 'sub': 'Langley|Salmon River', 'verdict': 'Pick Salmon River for elbow room: one-acre communities and bigger lots with room for a shop. Look at Fort Langley instead if you want to walk to the village.', 'video': None,
  'summary': 'Salmon River is the rural middle of the Township of Langley, between Highway 1 and Fraser Highway from Murrayville east toward Aldergrove, named for the salmon-bearing river that runs north through it to the Fraser at Fort Langley. It is larger-lot houses, acreages and hobby farms on quiet rural roads.',
  'vibe': 'Elbow room: big yards, shops and paddocks on quiet rural roads, with nothing commercial in the middle of it.',
  'commute': {'from': 'the middle of the Salmon River MLS® area', 'measured': M, 'rows': [['Highway 1', 12, 7.6], ['Fort Langley', 18, 11.4], ['Surrey Central SkyTrain', 32, 28.2], ['Downtown Vancouver', 57, 53.8]]},
  'works': [
   {'t': 'One-acre communities as well as bigger acreages.', 'by': J},
   {'t': 'Room to use the land: big yards, space for a shop, and more distance from the neighbours.', 'by': J},
   {'t': 'Houses sold for about the same median as Fort Langley, but here you are buying the lot, not the walk to the village.', 'by': J},
   {'t': 'Highway 1 is about 12 minutes from the middle of the area off-peak, and Fort Langley, Murrayville and Aldergrove are the nearby hubs.'},
   {'t': 'Flood works are being upgraded: the Province put $5 million into the Township’s Glen Valley and Salmon River flood project, with more pumping capacity and fish-friendly pumps.'},
  ],
  'doesnt': [
   {'t': 'You drive for most things, and a bigger property takes more work.', 'by': J},
   {'t': 'Buses run on the edges, not through it: route 562 on Glover Road and route 503 on Fraser Highway.'},
   {'t': 'Many properties run on a well and septic, so testing the well and inspecting the septic are part of every offer.'},
   {'t': 'Creek-side land carries streamside setbacks, and ALR parcels limit subdivision, extra homes and non-farm uses.'},
   {'t': 'Low fields along the river can stay wet after heavy rain; look at the lot in a wet week.'},
  ],
  'fit': [
   {'q': 'Do you want a big yard, a shop or a few animals?', 'a': 'That’s what Salmon River is for. Check the zoning and ALR status for what you plan to build or keep before you offer.', 'links': [['Langley acreages for sale', '/langley-acreages-for-sale.html']]},
   {'q': 'Do you want to walk to coffee and shops?', 'a': 'Then look at Fort Langley village. Salmon River costs about the same for a house, but you’ll drive for errands.', 'links': [['Fort Langley guide', '/fort-langley-guide.html']]},
   {'q': 'Do you commute to Surrey or Vancouver?', 'a': 'About 12 minutes to Highway 1, 32 to Surrey Central and 57 to downtown Vancouver off-peak, from the middle of the area. There’s no rapid transit until the Langley SkyTrain opens (expected late 2029).'},
   {'q': 'Do you need a mortgage-helper suite?', 'a': 'It depends on the lot. On ALR land a suite has to be inside the main house, though one small additional residence can be allowed, and the septic has to handle it. Walnut Grove and Willoughby make a suite simpler.', 'links': [['Walnut Grove guide', '/walnut-grove-guide.html']]},
  ],
  'faq': [
   {'q': 'Is Salmon River a good place to live?', 'a': 'For buyers who want a big yard, room for a shop or more space between neighbours, yes. Houses sold for about the same median as Fort Langley over the last year. The trade-off is that you drive for most things, and a bigger property takes more work.'},
   {'q': 'What are the downsides of living in Salmon River?', 'a': 'You drive for most errands, buses only run on the edges, many properties are on a well and septic, creek-side and ALR land come with rules, and low fields can stay wet after heavy rain.'},
  ],
 },
 'otter-district-guide': {
  'status': 'draft', 'name': 'Otter District', 'sub': 'Langley|Otter District', 'verdict': 'Pick Otter District for more land, close to the Otter Co-op, with room for horses, a shop or a big garden. Look elsewhere if you don’t want weekends of upkeep.', 'video': None,
  'summary': 'Otter District is the south-east corner of the Township of Langley, from Fraser Highway south to the US border between Campbell Valley and Aldergrove. It is working farm country: acreages, horse properties and farms, with the Otter Co-op at 248 Street and Fraser Highway as its local hub.',
  'vibe': 'Flat, open farm country: barns, paddocks and fields on two-lane roads, with the Co-op as the landmark.',
  'commute': {'from': 'the middle of the Otter District MLS® area', 'measured': M, 'rows': [['Aldergrove', 6, 4.1], ['Highway 1', 9, 8.2], ['Surrey Central SkyTrain', 36, 36.3], ['Downtown Vancouver', 60, 61.9]]},
  'works': [
   {'t': 'More land, and close to the Otter Co-op.', 'by': J},
   {'t': 'This is where to look if you want to use the land: a few acres for horses, a shop or a big garden.', 'by': J},
   {'t': 'The Otter Co-op at 248 Street and Fraser Highway, which grew out of the farmers’ institute local farmers formed in 1922, sells groceries, hardware, feed and fuel.'},
   {'t': 'Aldergrove is about 6 minutes away and Highway 1 about 9, from the middle of the district off-peak.'},
   {'t': 'Campbell Valley Regional Park and its horse trails are on the west side of the district.'},
  ],
  'doesnt': [
   {'t': 'A place can look like the perfect horse property until you see what the back field does in November.', 'by': J},
   {'t': 'Very little comes up for sale: about 20 acreages and manufactured homes sold in a year.'},
   {'t': 'No bus south of Fraser Highway. Route 503 on Fraser Highway is the nearest.'},
   {'t': 'Most properties run on a well and septic, and most of the land is in the ALR, which limits subdivision, extra homes and non-farm uses.'},
   {'t': 'Downtown Vancouver is about an hour off-peak.'},
  ],
  'fit': [
   {'q': 'Are you bringing horses or planning to farm?', 'a': 'Then Otter is the right search. Walk the back field after a few days of rain, and check where a dry turnout and hay storage would go.', 'links': [['Langley horse properties', '/langley-horse-properties-equestrian-farms-for-sale-mls-listings.html']]},
   {'q': 'Can you wait for the right property?', 'a': 'You may have to. Only a couple of dozen properties sell here in a year, so set up a search and be ready to move.'},
   {'q': 'Do you commute west every day?', 'a': 'Allow about 36 minutes to Surrey Central and an hour to downtown Vancouver off-peak. Abbotsford and Aldergrove are the easy directions.'},
   {'q': 'Do you need a mortgage-helper suite?', 'a': 'On ALR land a suite has to be inside the main house, though one small additional residence can be allowed if the Township agrees and the septic can handle it.'},
  ],
  'faq': [
   {'q': 'Is Otter District a good place to live?', 'a': 'For buyers who want a few acres for horses, a shop or a big garden and are happy to spend weekends looking after it, yes. Aldergrove is about 6 minutes away and Highway 1 about 9. For transit, walkable shops or plenty of listings to choose from, look in town.'},
   {'q': 'What are the downsides of living in Otter District?', 'a': 'Wet fields in winter on some properties, very few homes for sale in a year, no bus south of Fraser Highway, wells and septic, ALR rules on most land, and about an hour’s drive to downtown Vancouver.'},
  ],
 },
 'campbell-valley-guide': {
  'status': 'draft', 'name': 'Campbell Valley', 'sub': 'Langley|Campbell Valley', 'verdict': 'Pick Campbell Valley to be close to the horse trails at Campbell Valley Park, with privacy and room for animals. Look elsewhere if you don’t want the upkeep.', 'video': None,
  'summary': 'Campbell Valley is south Langley’s valley district, from the Surrey border east to about 232 Street and down to the US border, around Campbell Valley Regional Park and the Little Campbell River. It is acreages, horse properties, vineyards and newer estate houses, with Brookswood at its north edge.',
  'vibe': 'Private and green: horse country, farm stands and wineries around a big regional park.',
  'commute': {'from': 'the middle of the Campbell Valley MLS® area', 'measured': M, 'rows': [['Highway 1', 16, 13.3], ['Peace Arch border crossing', 21, 15.0], ['Surrey Central SkyTrain', 34, 30.4], ['Downtown Vancouver', 59, 56.1]]},
  'works': [
   {'t': 'Close to the horse trails in Campbell Valley Park.', 'by': J},
   {'t': 'Land is the point: fields and animals, without neighbours right on top of you.', 'by': J},
   {'t': 'Wineries are part of the valley, including Township 7, Chaberton Estate and Vista D’oro.'},
   {'t': 'The Peace Arch crossing is about 21 minutes away off-peak, and White Rock is the nearest beach.'},
   {'t': 'TransLink runs a summer weekend and holiday bus from Langley Centre to the regional park.'},
  ],
  'doesnt': [
   {'t': 'The upkeep. Land takes work.', 'by': J},
   {'t': 'Groceries are a slightly longer drive, though no worse than from Fort Langley.', 'by': J},
   {'t': 'Highway 1 is about 16 minutes away off-peak, and there is no weekday bus into the valley.'},
   {'t': 'Very little sells here: about 30 houses and acreages in a year.'},
   {'t': 'Wells and septic on most properties, ALR rules on farm parcels, and streamside setbacks along the Little Campbell River.'},
  ],
  'fit': [
   {'q': 'Do you ride, or want room for animals?', 'a': 'This is the valley for it, with the regional park’s horse trails right there. Check the parcel’s ALR status and zoning for barns and arenas.', 'links': [['Langley horse properties', '/langley-horse-properties-equestrian-farms-for-sale-mls-listings.html']]},
   {'q': 'Do you cross the border or head to White Rock often?', 'a': 'Then the south end works well: the Peace Arch crossing is about 21 minutes off-peak from the middle of the valley.'},
   {'q': 'Do you commute north to Surrey or Vancouver?', 'a': 'Allow about 16 minutes to Highway 1, 34 to Surrey Central and 59 to downtown Vancouver off-peak.'},
   {'q': 'Would you rather have a yard than acreage?', 'a': 'Brookswood, at the valley’s north edge, gives you big lots with Township services.', 'links': [['Brookswood guide', '/brookswood-guide.html']]},
  ],
  'faq': [
   {'q': 'Is Campbell Valley a good place to live?', 'a': 'For acreage buyers who want privacy and room for horses, a shop or a big garden, yes, with the regional park at its heart. The trade-offs are the upkeep, a longer drive for groceries and Highway 1, and very few homes for sale.'},
   {'q': 'What are the downsides of living in Campbell Valley?', 'a': 'Land takes upkeep, groceries and Highway 1 are a longer drive, there is no weekday bus, very little comes up for sale, and wells, septic, ALR rules and river setbacks apply to many properties.'},
  ],
 },
 'county-line-glen-valley-guide': {
  'status': 'draft', 'name': 'County Line / Glen Valley', 'sub': 'Langley|County Line Glen Valley', 'verdict': 'Pick Glen Valley for more hills and privacy, closer to Fort Langley. Look elsewhere if a low, wet lot or a steep driveway would bother you.', 'video': None,
  'summary': 'County Line / Glen Valley is the north-east corner of the Township of Langley, from east of Fort Langley to the Abbotsford line, with farm flats along the Fraser River and higher land on the slope behind. It is farms and acreages, most of it in the ALR, with Glen Valley Regional Park on the river.',
  'vibe': 'Quiet farm country toward the Fraser: river flats, berry fields and acreages on the slope.',
  'commute': {'from': 'the middle of the County Line Glen Valley MLS® area', 'measured': M, 'rows': [['Highway 1', 9, 6.0], ['Fort Langley', 15, 9.9], ['Surrey Central SkyTrain', 30, 26.6], ['Downtown Vancouver', 54, 52.3]]},
  'works': [
   {'t': 'More hills, and closer to Fort Langley.', 'by': J},
   {'t': 'Privacy, and the river side is beautiful.', 'by': J},
   {'t': 'Glen Valley Regional Park is on the Fraser, with river fishing and riverside trails.'},
   {'t': 'Highway 1 is about 9 minutes from the middle of the area off-peak, and Fort Langley about 15.'},
   {'t': 'The Province put $5 million into the Township’s Glen Valley and Salmon River flood project: pump capacity, dike bank repairs, culverts and ditches.'},
  ],
  'doesnt': [
   {'t': 'Low, wet land on the flats and higher land with a steeper driveway are two very different places to live.', 'by': J},
   {'t': 'The flats sit beside the Fraser, which rises in the spring freshet. Check the flood mapping for the address and get an insurance quote early.'},
   {'t': 'Very little sells: about 17 acreages in a year.'},
   {'t': 'No bus in the valley, and no shops or school in it; Fort Langley and Aldergrove are the hubs.'},
   {'t': 'Wells, septic and ALR rules on most properties, and farm traffic on the roads.'},
  ],
  'fit': [
   {'q': 'Do you want land near the river?', 'a': 'Then drive down toward Glen Valley Regional Park first, and decide between the flats and the slope before you look at houses.'},
   {'q': 'Would a flood risk keep you up at night?', 'a': 'Then stay on the higher ground on the slope, and check the flood mapping and insurance for any address on the flats.'},
   {'q': 'Do you commute to Surrey or Vancouver?', 'a': 'About 9 minutes to Highway 1, 30 to Surrey Central and 54 to downtown Vancouver off-peak, from the middle of the area.'},
   {'q': 'Do you want to walk to a village?', 'a': 'Then look at Fort Langley itself, about 15 minutes west.', 'links': [['Fort Langley guide', '/fort-langley-guide.html']]},
  ],
  'faq': [
   {'q': 'Is County Line / Glen Valley a good place to live?', 'a': 'For acreage buyers who want privacy and like being out toward the Fraser River, yes. Highway 1 is about 9 minutes away. The big choice is between the low river flats and the higher land on the slope, which live very differently.'},
   {'q': 'What are the downsides of living in Glen Valley?', 'a': 'The river flats can flood in a big spring freshet, very little comes up for sale, there is no bus, shop or school in the valley, and wells, septic and ALR rules apply to most properties.'},
  ],
 },
}


def main():
    p = 'src/data/guide-plus.json'; d = json.load(open(p, encoding='utf-8'))
    for k, v in E.items():
        assert os.path.exists(f'src/data/pages/{k}.json'), k
        d[k] = v
    open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    print('guide-plus entries:', [k for k in d if not k.startswith('_')])


if __name__ == '__main__': main()
