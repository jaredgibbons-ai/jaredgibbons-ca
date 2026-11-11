#!/usr/bin/env python3
"""Jared's notes on the 17 small areas (D-216, Nov 11, 2026).

Jared sent two things the same morning:
  - Full notes (suits / works / doesn't / catch) for Port Kells, Barnston Island, Mt Lehman, Lindell Beach, Kent, Mount Currie,
    Whitby Estates and Brunette. Used as his words (tagged "Jared"), lightly tidied, each claim checked against the sourced text
    already on that guide. Changes: Port Kells, a broken sentence ("There is some farm land and The village…") joined, and
    "about six minutes" to Walnut Grove made "a few minutes" (measured 7 to 8 off-peak). Lindell Beach, "Cultus Lake Holiday Park
    offers seasonal occupancy through membership" dropped (not on the guide or a source found), and the lots' FVRD water and sewer
    kept with "confirm the connection lot by lot" (the guide's FVRD source says so). Kent, "municipal water and sewer" dropped
    (not on the guide). Mt Lehman, "bus service is limited" made "no bus route runs through the village" (the guide's TransLink
    source). Brunette and Port Kells sales figures are SnapStats September 2026, already on those guides.
  - Short descriptions for the other nine. Where they say something about living there, it is used as his line; the rest of each
    list comes from facts already sourced on the guide (not tagged "Jared"). Westham Island's note repeated the Ladner Rural text,
    so its lines come from his own Nov 9 take and the guide. West Meadows' note carried links to other agents' pages; not used.
Writes src/data/guide-plus.json (works/doesn't lists, and a verdict for the eight new ones) and his take for the eight into
docs/research/jared-voice/core-tidied.json (run tools/build_jared_voice.py after). Idempotent.
python3 -I tools/build_small_areas_2026_11_11.py && python3 -I tools/build_jared_voice.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
J = 'jared'
def j(t): return {'t': t, 'by': J}
def f(t): return {'t': t}

# ------------------------------------------------------------------------------------------------ the nine with his take on file
NINE = {
    'serpentine-guide': ([j('Commercial and industrial listings come up around 184 Street and 32 Avenue.'), j('A mix of farmland and work land that suits farmers and industrial companies.')],
                         [f('Much of the lowland is floodplain close to sea level, managed by sea dams, dikes and pump stations.'), j('Ground that is soggy half the year is worth less than its acreage suggests.')]),
    'ladner-rural-guide': ([j('Working farms and waterfront along the Fraser River and River Road West.'), j('Quiet country living, a few minutes from Ladner Village.')],
                           [f('The lowland is diked floodplain, and the flood construction level is set parcel by parcel.'), f('ALR rules decide what you can build, split or run on the land.')]),
    'east-delta-guide': ([j('Open farm country between the south arm of the Fraser and Boundary Bay, right next to Surrey.'), j('Wide open, especially along 104 Street.')],
                         [j('Farm roads come with trucks, equipment and neighbours who start work early.'), f('It is diked floodplain: ask what dike protects the property and get insurance quotes early.')]),
    'westham-island-guide': ([j('Farm fields and marsh out toward the Reifel bird sanctuary.'), f('More than 700 hectares of ALR farmland: a real farming setting.')],
                             [j('The bridge is part of every trip into town.'), f('It sits on the Fraser estuary: check flood status and insurance before you remove subjects.')]),
    'west-meadows-pitt-meadows-guide': ([j('A quiet residential area on the west side of Pitt Meadows, with detached homes, townhouses and estate properties.'), j('More room and open views.')],
                                        [j('Aircraft noise from the airport, easy to miss on a quiet showing.'), f('City transit centres on the West Coast Express station in the urban core, not the rural areas.')]),
    'sumas-mountain-guide': ([j('Trails at your door: the hike past Chadsey Lake to the top looks out over the Fraser Valley.'), j('Trees, and a bit of separation from town.')],
                             [j('The hill is part of the routine, from steep driveways to finding a flat spot for the kids to play.'), f('Gravel trucks from the mountain’s quarries use an access road to Highway 1.')]),
    'hemlock-valley-mission-guide': ([j('A mountain resort community: weekends at Sasquatch Mountain.'), f('35 named trails on the south and southwest slopes.')],
                                     [j('Getting up there on a snowy Friday night.'), f('One road in and out: the road up from Harrison Mills is also the evacuation route.')]),
    'west-chilliwack-guide': ([j('Rural property on the agricultural west side of the city, from Village West to Chilliwack Mountain.'), j('Popular with 55+ downsizers from the Valley and the coast.')],
                              [j('The Agricultural Area Plan and the ALR decide what you can do with the land.'), f('Flood setbacks: buildings must sit 60 m from the Fraser and 75 m from the Vedder River.')]),
    'bridal-falls-guide': ([j('Bridal Veil Falls Provincial Park next door, with its 60 m waterfall.'), f('Quick access to Highway 1 and the bridge north to Agassiz.')],
                           [j('At the RV resort, what you can put on a lot and how you can use it are limited.'), f('Transit is on request only (route 71).')]),
}

# ------------------------------------------------------------------------------------------------ the eight with full notes
EIGHT = {
    'barnston-island-surrey-guide': ('Barnston Island', 'Farmers and buyers who want privacy on large rural parcels.',
        [j('Farmland and quiet: most of the island is in the Agricultural Land Reserve.'), j('The ferry lands at Port Kells, close to Highway 1.')],
        [j('The free ferry is the only access. It carries five vehicles at a time and runs within set hours.'), j('School and shopping mean a crossing.')],
        'The catch is that the island is low Fraser floodplain behind a dike. Check the flood construction level, insurance, ALR rules, the well and septic and the land tenure. It has a Surrey mailing address but sits in Metro Vancouver’s Electoral Area A.'),
    'mt-lehman-abbotsford-guide': ('Mt Lehman', 'Acreage, hobby-farm and equestrian buyers who want a rural community with an elementary school.',
        [j('An upland setting with a village core and Highway 1 access.'), j('It sits above the Matsqui Prairie floodplain. Check parcels on the plateau edge one by one.')],
        [j('No bus route runs through the village, and you drive to shop.'), j('Water and sewer vary by property.')],
        'The catch is that ALR and local zoning rules can limit subdivision, suites and extra homes, and farm tax class has its own test tied to selling farm products.'),
    'lindell-beach-bc-guide': ('Lindell Beach', 'Recreational and second-home buyers who want the quieter south end of Cultus Lake.',
        [j('Freehold options near the lake.'), j('The original lots are fee simple, in the regional district’s water and sewer service areas. Confirm the connection lot by lot.')],
        [j('No shops, schools or transit nearby.'), j('Columbia Valley Road is the only way in and out, with summer traffic and the risk of flooding in heavy rain.')],
        'The catch is tenure. The original lots are freehold, while The Cottages, Aquadel Crossing and Creekside Mills are bare-land strata. Confirm the tenure before you compare prices.'),
    'kent-bc-guide': ('Kent', 'Buyers who want a small town with schools and recreation, and farmland nearby.',
        [j('Everyday needs in Agassiz: schools from kindergarten to grade 12, the recreation and aquatic centre and the library.'), j('Harrison Hot Springs is next door.')],
        [j('Not much transit, and not a wide range of shops.'), j('Most major shopping means a drive to Chilliwack.')],
        'The catch is that the Agassiz townsite sits on Fraser floodplain behind dikes and pumps. Check the flood construction level and insurance before you make an offer.'),
    'mount-currie-bc-guide': ('Mount Currie', 'Líl̓wat Nation members looking for housing through the Nation. Open-market buyers look at fee-simple homes in Pemberton or Pemberton Meadows.',
        [j('The mountain setting, close to Pemberton.'), j('The Nation runs its own school and learning centre.')],
        [j('No full-service shopping or hospital in the community.'), j('Pemberton is the nearest service centre.')],
        'The catch is tenure. Mount Currie is federal reserve land, and housing follows the Nation’s own approval and financing process. A listing that says “Mount Currie” may mean the view, or a manufactured home on a rented pad elsewhere in the valley.'),
    'whitby-estates-west-vancouver-guide': ('Whitby Estates', 'Luxury buyers who want privacy, a large home and panoramic views.',
        [j('Views over Burrard Inlet, downtown and Stanley Park.'), j('Chartwell Elementary and Sentinel Secondary are close by. Confirm the catchment for the address.')],
        [j('Not walkable, and little transit: shopping is a drive.'), j('Few sales, which makes pricing and resale timing harder to judge.')],
        'The catch is that covenants on title can require British Pacific Properties’ approval to build or alter, on top of District permits. The MLS® area has both freehold homes and strata townhomes, so confirm the tenure and fees.'),
    'brunette-new-westminster-guide': ('Brunette', 'Detached-home buyers who want parks and SkyTrain close by and are fine living near industry.',
        [j('Hume Park and the Brunette–Fraser Greenway.'), j('Sapperton and Braid stations, Royal Columbian Hospital and Highway 1 are close.')],
        [j('Warehouses, trucks and rail traffic shape the area.'), j('Few listings: September 2026 had none listed and none sold.')],
        'The catch is that lots by the river can face flood construction and stream setback rules. Confirm both before you remove subjects, and check the city for the address: Brunette Avenue carries on into Coquitlam.'),
}

PK_WORKS = [j('Highway 1 and the Golden Ears Bridge are close by.'), j('There’s some farmland, and the village has an elementary school and a park with an outdoor pool. Walnut Grove’s shops are a few minutes away.')]
PK_DOESNT = [j('Not much choice: four detached listings and no sales in September 2026.'), j('Expect truck and rail traffic, and use 200 Street to get onto Highway 1 eastbound.')]
PK_TAKE = {'name': 'Port Kells', 'suits': 'Buyers and business owners who want to live close to the industrial district.',
           'friend': 'The catch is flood exposure along the undiked Fraser riverfront. Check each lot and base your offer on what it is used for today. Long-term planning for South Port Kells is still pending.'}


def main():
    p = 'src/data/guide-plus.json'; gp = json.load(open(p, encoding='utf-8'))
    for slug, (w, d) in NINE.items():
        g = gp[slug]; g['works'], g['doesnt'] = w, d
    for slug, (name, suits, w, d, catch) in EIGHT.items():
        s = suits.rstrip('.'); s = s if s.startswith(('Líl̓wat',)) else s[0].lower() + s[1:]
        verdict = f'{name} suits {s}. {catch.split(". ")[0].rstrip(".")}.'   # the take box carries the rest of the catch
        gp[slug] = {'status': 'approved', 'lite': True, 'name': name, 'sub': None, 'summary': None, 'verdict': verdict, 'vibe': None,
                    'commute': None, 'works': w, 'doesnt': d, 'fit': [], 'faq': [], 'video': None}
    pk = gp['port-kells-surrey-guide']
    keep_w = [x for x in pk['works'] if not x.get('by') and not x['t'].startswith(('Highway 1 runs through it', 'A quiet village'))]
    keep_d = [x for x in pk['doesnt'] if not x.get('by') and not x['t'].startswith(('Hardly any homes sell', 'Freight trains', 'The 192 Street ramps'))]
    pk['works'] = PK_WORKS + keep_w; pk['doesnt'] = PK_DOESNT + keep_d
    open(p, 'w', encoding='utf-8').write(json.dumps(gp, ensure_ascii=False, indent=1) + '\n')
    c = 'docs/research/jared-voice/core-tidied.json'; core = json.load(open(c, encoding='utf-8'))
    for slug, (name, suits, w, d, catch) in EIGHT.items(): core[slug] = {'name': name, 'suits': suits, 'friend': catch}
    core['port-kells-surrey-guide'] = PK_TAKE
    open(c, 'w', encoding='utf-8').write(json.dumps(core, ensure_ascii=False, indent=1) + '\n')
    print('lists:', len(NINE) + len(EIGHT) + 1, '| takes:', len(EIGHT) + 1)


if __name__ == '__main__': main()
