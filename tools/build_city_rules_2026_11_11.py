#!/usr/bin/env python3
"""The eight city rules pages, rewritten (D-214, Nov 11, 2026).

D-202 built /<city>-home-buying-rules.html by moving the city-wide rules paragraphs out of the guides word for word. Read as pages, they
did not hold up: titles and meta descriptions cut off mid-word, rules filed under the wrong heading (suites under "Floodplain", ALR
under "Property taxes"), one neighbourhood's facts presented as city-wide (Barnston Island's rural taxes and Douglas's plan on the
Surrey page, Marble Hill on Chilliwack's), the same rule three times, researchers' notes ("never borrowed", "ESTABLISHED", "stated so
it is not misapplied here"), and source lists of 50 to 110 links that included listing portals and other agents' pages.

Each page is now written by hand from the facts those paragraphs already carried (each one researched and sourced for the guides),
in plain words, under the right heading, city-wide rules only, with a short "before you remove subjects" list, links to the
neighbourhoods that have their own rules, the BC-wide rules pages, and a short list of the official sources behind what is said.
Nothing new is claimed. Pages carry "curated" so tools/trim_guides.py no longer rewrites them.
python3 -I tools/build_city_rules_2026_11_11.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'rules'
TODAY = '2026-11-11'


def parts(x):
    if isinstance(x, str): return [{'t': x}]
    return [({'t': y[0], 'h': y[1] if y[1].startswith('http') else f'/{y[1]}.html'} if isinstance(y, tuple) else {'t': y}) for y in x]


BC = [('Buying a condo in BC: Form B, depreciation reports and strata rules', 'bc-condo-buying-rules'),
      ('Buying a townhome in BC', 'bc-townhome-buying-rules'),
      ('Buying a lot or land in BC', 'bc-land-buying-rules'),
      ('Buying an acreage in BC: ALR, farm class, wells and septic', 'bc-acreage-buying-rules'),
      ('Buying a mobile or manufactured home in BC', 'bc-mobile-home-buying-rules'),
      ('55+ strata rules in BC', 'bc-55-plus-strata-rules'),
      ('Short-term rentals and suites in the Fraser Valley', 'fraser-valley-short-term-rental-and-suite-rules')]

CITIES = {
# ------------------------------------------------------------------------------------------------------------------------- Maple Ridge
'maple-ridge': {
    'title': 'Maple Ridge Home Buying Rules: Zoning, Suites and Taxes',
    'h1': 'Buying a Home in Maple Ridge: The Rules',
    'desc': 'Maple Ridge rules for home buyers: zoning lot sizes, the suite rule, small-scale housing, floodplain, rural servicing and tax dates, with City sources.',
    'intro': 'Maple Ridge runs from the Lougheed Highway town centre out to acreages and farmland in the north and east, so the rule that matters depends on where the lot is. These are the City-wide ones, in plain words, with the official source for each at the bottom.',
    'sections': [
        ('Zoning and lot sizes', [
            'Zoning Bylaw No. 7600-2019 sets what each lot can be used for and built on. Look up the exact parcel’s zone with the City before you count on anything.',
            'A typical urban house lot is zoned RS-1 (Single Detached Residential): at least 668 m² in area, 18 m wide and 27 m deep, with up to 40% lot coverage.',
            'Rural and farm zones need far more land to subdivide: A-1 2.0 ha, A-2 4.0 ha, A-3 8.0 ha, RS-2 0.4 ha, and RS-3 0.8 ha or 2.0 ha depending on the zone.',
            'Subdivision servicing runs under the Subdivision and Development Servicing Bylaw No. 4800-1993.']),
        ('Suites and small-scale housing', [
            'One secondary suite is allowed per lot, inside the house, up to 40% of its gross floor area. A suite is not allowed in the floodplain area.',
            'Under the City’s small-scale multi-unit housing (SSMUH) bylaws, eligible single-detached and duplex lots can have three, four or six units, depending on the lot and its servicing.']),
        ('Floodplain, farmland and rural servicing', [
            'The City sets floodplain construction rules for low-lying land near the Fraser and its rivers. Ask for the flood construction level for the exact lot.',
            'Parts of rural Maple Ridge are in the Agricultural Land Reserve. ALR status is set parcel by parcel on the ALC’s map.',
            'Some rural properties run on a well and septic system instead of City water and sewer. Get the well record and a septic inspection before you firm up.']),
        ('Property taxes', [
            'Maple Ridge’s 2026 property taxes were due July 2, 2026. A 5% penalty applied to any balance left on July 3, and another 5% on September 2.']),
        ('Mobile homes and growth plans', [
            'If a manufactured home park is redeveloped, the City’s Manufactured Home Park Redevelopment Tenant Assistance Policy (No. 627) applies.',
            'Along Lougheed Highway, the Lougheed Transit Corridor Area Plan guides denser, transit-oriented housing. Check it for any lot near the corridor.',
            'TransLink’s Langley to Haney Place bus rapid transit line (22 km from Willowbrook) is still in planning, so price a home on today’s bus service.']),
    ],
    'check': ['The parcel’s zone, and whether its lot size allows what you plan.', 'Any suite’s permit, and that the lot is outside the floodplain area.',
              'ALR status, the well record and the septic report on a rural lot.', 'The flood construction level if the land is low.'],
    'own': [('Albion', 'albion-guide', 'Albion Area Plan'), ('Southwest Maple Ridge (Hammond)', 'southwest-maple-ridge-guide', 'Hammond Area Plan'),
            ('Silver Valley', 'silver-valley-guide', 'hillside lots'), ('North Maple Ridge', 'north-maple-ridge-guide', 'acreage and ALR land')],
    'auth': ('City of Maple Ridge', 'https://www.mapleridge.ca/'),
    'faq': [{'q': 'Can I add a suite to a house in Maple Ridge?', 'a': 'One secondary suite per lot is allowed inside the house, up to 40% of its gross floor area, but not in the floodplain area. Check the lot’s zone and get a permit.'},
            {'q': 'How many units can I build on a Maple Ridge lot?', 'a': 'Under the City’s small-scale housing bylaws, eligible single-detached and duplex lots can have three, four or six units, depending on the lot and servicing.'}],
    'sources': [('City of Maple Ridge: Zoning Bylaw', 'https://www.mapleridge.ca/build-do-business/community-planning/zoning-bylaw'),
                ('City of Maple Ridge: secondary suites', 'https://www.mapleridge.ca/build-do-business/planning-land-use/community-planning/housing-ready/secondary-suites'),
                ('City of Maple Ridge: floodplain construction', 'https://www.mapleridge.ca/media/file/floodplain-construction-0'),
                ('City of Maple Ridge: Subdivision and Development Servicing Bylaw No. 4800-1993', 'https://www.mapleridge.ca/media/file/subdivision-development-bylaw-no-4800-1993'),
                ('City of Maple Ridge: property tax due dates and penalties', 'https://mapleridge.ca/2329/Due-Dates-and-Penalties-Late-Payments'),
                ('City of Maple Ridge: Official Community Plan', 'https://www.mapleridge.ca/your-government/plans-strategies/official-community-plan-area-plans/official-community-plan'),
                ('City of Maple Ridge: Lougheed Transit Corridor Area Plan', 'https://engage.mapleridge.ca/LTCAP'),
                ('City of Maple Ridge: Manufactured Home Park Redevelopment Tenant Assistance Policy 6.27', 'https://www.mapleridge.ca/media/file/manufactured-home-park-redevelopment-tenant-assistance-policy-627'),
                ('TransLink: bus rapid transit', 'https://www.translink.ca/plans-and-projects/projects/rapid-transit-projects/bus-rapid-transit'),
                ('Agricultural Land Commission: ALR maps', 'https://www.alc.gov.bc.ca/alr-maps'),
                ('Province of BC: well records', 'https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/groundwater-wells-aquifers/information-for-well-owners/well-records-registration')],
},
# -------------------------------------------------------------------------------------------------------------------------- Chilliwack
'chilliwack': {
    'title': 'Chilliwack Home Buying Rules: Zoning, Floodplain, Hillsides',
    'h1': 'Buying a Home in Chilliwack: The Rules',
    'desc': 'Chilliwack rules for home buyers: floodplain setbacks and dikes, hillside permits, suites and small-scale housing, farm zoning and tax dates, with sources.',
    'intro': 'In Chilliwack the rule that catches buyers depends on the ground: river setbacks and dikes on the flats, development permits on the hillsides, and farm zoning across the Agricultural Land Reserve. Here are the City-wide ones in plain words, with the City’s own sources at the bottom.',
    'sections': [
        ('Plans and zoning', [
            'The current plan is the Chilliwack 2050 Official Community Plan, Bylaw No. 5500. Its schedules include the Agricultural Area Plan (B1), the Downtown Neighbourhood Plan (B3) and the Sardis plan (B5).',
            'Zoning is Zoning Bylaw 2020, No. 5000. On SHR hillside lots the minimum lot area rises with the slope, from 360 m² to 990 m², so a big hillside lot may not split the way its size suggests.',
            'In the AL (Agricultural Lowland) zone, a new lot needs 7.5 ha where subdivision is allowed, 1 ha for a boundary adjustment and 0.2 ha for a homesite severance the ALC has approved, with a 25 m minimum width.',
            'Subdivision goes through the City’s Approving Officer and the Preliminary Layout Approval process. Confirm zone, servicing and frontage for the exact parcel before you value a split.']),
        ('Floodplain and dikes', [
            'The Floodplain Regulation Bylaw 2018, No. 4519 sets minimum building setbacks of 60 m from the Fraser River, 75 m from the Vedder River and 30 m from the Chilliwack River and the Vedder Canal.',
            'The City maintains dikes on the Fraser and Vedder systems and charges drainage and dyking taxes on top of the general rate.',
            'Ask the City for the flood construction level and floodplain position of the exact lot before you remove subjects.']),
        ('Hillside development', [
            'Development Permit Area 2 (Hillside and Upland Areas) needs a geotechnical report from a qualified professional with each application.',
            'Development Permit Area 5 (Hillside Development) covers every City lot with a slope of 20% or more. A permit is needed before subdividing, building, adding on or altering the land, unless an exemption applies.',
            'That is the rule behind every deck, addition or rebuild on the mountain, in a strata or not. Get the property’s geotechnical reports and check title for covenants.']),
        ('Suites and small-scale housing', [
            'A secondary suite is capped at the lesser of 90 m² and 40% of the house. One accessory dwelling unit is allowed per lot, and a garden suite is capped at 100 m².',
            'Bylaw 5395, adopted June 18, 2024, allows three to four units on lots inside the urban growth boundary zoned for single-detached or duplex housing. It does not apply to lots inside an existing strata, where the strata’s bylaws come first.',
            'Short-term rentals need a licence under the Short-Term Rental Bylaw 2021, No. 5141. Check that a property qualifies before you count on rental income.']),
        ('Property taxes', [
            'Notices go out at the end of May and taxes are due the first working day after July 1. For 2026, 5% was added to taxes unpaid after July 2 and another 5% after August 4.']),
    ],
    'check': ['The flood construction level and river setbacks for the lot.', 'Whether the lot is in a hillside development permit area, and its geotechnical reports.',
              'Any suite or garden suite against the size caps.', 'ALR status on any farm or rural parcel.'],
    'own': [('Eastern Hillsides', 'eastern-hillsides-guide', 'Marble Hill slide areas and the moratorium area'), ('Little Mountain', 'little-mountain-guide', 'hillside lots'),
            ('Chilliwack Mountain', 'chilliwack-mountain-guide', 'hillside strata'), ('East Chilliwack', 'east-chilliwack-guide', 'farm zoning'),
            ('Fairfield Island', 'fairfield-island-guide', 'floodplain')],
    'auth': ('City of Chilliwack', 'https://www.chilliwack.com/'),
    'faq': [{'q': 'Can I put a suite in a Chilliwack house?', 'a': 'Yes, where the zone allows it. A secondary suite is capped at the lesser of 90 m² and 40% of the house, and one accessory dwelling unit is allowed per lot.'},
            {'q': 'Do I need a permit to build on a Chilliwack hillside?', 'a': 'Usually. Development Permit Area 5 covers every lot with a slope of 20% or more, and a permit with a geotechnical report is needed before you subdivide, build, add on or alter the land, unless an exemption applies.'}],
    'sources': [('City of Chilliwack: Official Community Plan', 'https://www.chilliwack.com/ocp'),
                ('City of Chilliwack: Zoning Bylaw 2020, No. 5000', 'https://www.chilliwack.com/main/attachments/Files/377/ZBA%5F5000%5F%2D%5FZoning%5FBylaw%5F2020%2Epdf'),
                ('City of Chilliwack: Development Permit Area 2 guide (March 2026)', 'https://www.chilliwack.com/main/attachments/Files/2881/DP2%5FGuide%5F%2D%5FMar%5F2026%2Epdf'),
                ('City of Chilliwack: Agricultural Area Plan', 'https://www.chilliwack.com/main/attachments/Files/2387/SB1%5FAgricultural%5FArea%5FPlan%5F1%2Epdf'),
                ('City of Chilliwack: Short-Term Rental Bylaw 2021, No. 5141', 'https://www.chilliwack.com/main/attachments/Files/363/BL51411.pdf'),
                ('Agricultural Land Commission: ALR maps', 'https://www.alc.gov.bc.ca/alr-maps')],
},
# ------------------------------------------------------------------------------------------------------------------------- Cultus Lake
'cultus-lake': {
    'title': 'Cultus Lake Home Buying Rules: Leases, Zoning and Septic',
    'h1': 'Buying a Home at Cultus Lake: The Rules',
    'desc': 'Cultus Lake rules for buyers: Park Board lease lots, FVRD freehold lots, rented pads, rural taxes, sewer or septic, ALR and local hazards, with sources.',
    'intro': 'Cultus Lake is not part of the City of Chilliwack, and three kinds of ownership sit side by side here: leased lots inside Cultus Lake Park, freehold lots at the south end under the Fraser Valley Regional District (FVRD), and manufactured homes on rented pads. The rules differ for each, so work out which one you are buying first.',
    'sections': [
        ('Which rules apply to the lot', [
            'Inside Cultus Lake Park, on the north and east shores, homes sit on lots leased from the Cultus Lake Park Board. PlanCultus (Bylaw No. 1080, 2016) and the FVRD Cultus Lake Park Zoning Bylaw No. 1375, 2016 apply there.',
            'At the south end, around Lindell Beach, homes are freehold lots and bare-land strata outside the Park. The FVRD Official Community Plan for Electoral Areas E and H (Bylaw No. 1115, amended by Bylaw No. 1533, 2019) and the FVRD Consolidated Zoning Bylaw No. 1638, 2021 apply there.',
            'Chilliwack’s bylaws don’t apply anywhere at the lake.']),
        ('Taxes and lease charges', [
            'Park lease lots pay lease charges to the Park Board rather than a normal municipal tax bill.',
            'Freehold lots in Electoral Area H pay provincial rural taxes under the Taxation (Rural Area) Act, plus FVRD service-area levies. Taxes are due July 2, with 5% added to any amount unpaid after July 2 and another 5% after October 31.']),
        ('Sewer or septic', [
            'The FVRD runs a sewer system for Cultus Lake and publishes a service area map. Lots outside it use private septic systems regulated by Fraser Health, so confirm which one the lot has.']),
        ('Farmland and hazards', [
            'Much of the flat land in Electoral Area H west of Lindell Beach is in the Agricultural Land Reserve. Check the parcel on the ALC’s map.',
            'The FVRD’s Area H evacuation guide lists flooding, landslide and slope stability, interface fire, debris slides and flash flooding as local hazards, and the FVRD runs a flood and debris control service here. Read it and get insurance quotes early.']),
        ('Lease lots and rented pads', [
            'Lenders and insurers treat Park Board leasehold homes differently from freehold. Confirm financing against the lease before you write an offer.',
            'A manufactured home on a rented pad is a home on rented land, not land you own. The Manufactured Home Park Tenancy Act governs the site, and a 55+ park can refuse a buyer who doesn’t meet its age rule.',
            'Pad rent can rise once every 12 months, with three full months’ written notice: by up to 2.3% in 2026 and 2.2% in 2027, plus a share of changes in local government levies and regulated utility fees.']),
    ],
    'check': ['Whether the lot is Park Board leasehold, freehold or a rented pad.', 'Financing and insurance against the lease, if it is leasehold.',
              'Sewer or septic, from the FVRD’s service area map.', 'Hazards and ALR status for the exact lot.'],
    'own': [('Cultus Lake', 'cultus-lake-guide', 'the Park and the lease lots'), ('Lindell Beach', 'lindell-beach-bc-guide', 'the freehold south end')],
    'auth': ('Fraser Valley Regional District', 'https://www.fvrd.ca/EN/main/about-the-fvrd/electoral-areas/electoral-area-h.html'),
    'faq': [{'q': 'Do I own the land under a Cultus Lake Park home?', 'a': 'No. Homes inside Cultus Lake Park sit on lots leased from the Cultus Lake Park Board. The freehold lots are at the south end, around Lindell Beach, outside the Park.'},
            {'q': 'Is Cultus Lake on sewer?', 'a': 'Partly. The FVRD runs a sewer system for a mapped service area; lots outside it are on private septic systems regulated by Fraser Health.'}],
    'sources': [('FVRD: Electoral Area H', 'https://www.fvrd.ca/EN/main/about-the-fvrd/electoral-areas/electoral-area-h.html'),
                ('FVRD: sewer and septic', 'https://www.fvrd.ca/EN/main/services/sewer-septic.html'),
                ('FVRD: zoning', 'https://haveyoursay.fvrd.ca/zoning'),
                ('Province of BC: rural property tax', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/rural-area'),
                ('Province of BC: rent increases for manufactured home sites', 'https://www2.gov.bc.ca/gov/content/housing-tenancy/residential-tenancies/manufactured-homes/rent-increases-for-manufactured-homes'),
                ('Agricultural Land Commission: ALR maps', 'https://www.alc.gov.bc.ca/alr-maps')],
},
# -------------------------------------------------------------------------------------------------------------------------- Abbotsford
'abbotsford': {
    'title': 'Abbotsford Home Buying Rules: Zoning, Suites, Floodplain',
    'h1': 'Buying a Home in Abbotsford: The Rules',
    'desc': 'Abbotsford rules for home buyers: zoning and lot sizes, suites and coach houses, farm zones, floodplain, steep slopes, airport height limits and tax dates.',
    'intro': 'Abbotsford takes in Sumas Prairie’s floodplain, the slopes of Sumas Mountain, the airport and a lot of farmland, so the same house can come with very different rules depending on the street. These are the City-wide rules, with the City’s own sources at the bottom.',
    'sections': [
        ('Plans and zoning', [
            'The current Official Community Plan is Abbotsforward 2050, adopted in December 2025. The 2016 plan is no longer in force.',
            'Zoning is Zoning Bylaw No. 2400-2014. City reports give minimum interior lots of 540 m² in RS3 and 420 m² in RS5. Rural RR lots need 4.0 ha and farm A1 lots 8.0 ha to subdivide.',
            'Under the bylaw’s small-scale housing section, lots of 280 m² or less can have three units and larger lots four, where the conditions are met.']),
        ('Suites and coach houses', [
            'One secondary suite is allowed in a single detached house. City reports list a 400 m² minimum lot and 12.0 m frontage, and the suite must be under 50% of the house.',
            'A coach house or garden suite is capped at 15% of the lot area, to a maximum of 100 m².',
            'On RR rural lots, a coach house needs a lot over 0.4 ha, and a coach house or suite is limited to one per lot at the lesser of 90 m² and 40% of the house.',
            'On A1 farm lots, a secondary suite can be up to 100 m², and one accessory farm dwelling may be allowed under the ALR rules on lots of at least 0.4 ha. None of these extra homes gets its own title.']),
        ('Floodplain and steep slopes', [
            'Low land toward Sumas Prairie and the Sumas River is floodplain. The plan’s Drainage and Flood Control map (Map 12) and the City’s WebMap show where a parcel sits.',
            'Steep land is in the Steep Slope Development Permit Area, and the McKee Neighbourhood Plan keeps unstable areas and slopes over 40% as open space.',
            'Clayburn Village is a Heritage Conservation Area. Check its rules before you plan exterior changes.']),
        ('Airport height limits', [
            'Inside the Airport Zoning Regulations area (City drawing M-500), buildings can’t rise above the airport’s approach and transition surfaces, and NAV CANADA and Transport Canada must approve before the City issues a building permit. Check before you plan a tall shop or barn.']),
        ('Property taxes', [
            'City of Abbotsford 2026 taxes were due July 2, with 5% added on July 3 and a second 5% on September 16.',
            'Parcels in the Fraser Valley Regional District pay provincial rural taxes to the Province instead: due July 2, with 5% added to any amount unpaid on July 2 and a further 5% on October 31.']),
    ],
    'check': ['The parcel’s zone and lot size against what you plan.', 'Floodplain position on the City’s WebMap.', 'Any suite or coach house against the size caps.',
              'Whether the land is City or FVRD, which changes the tax bill.'],
    'own': [('Sumas Prairie', 'sumas-prairie-guide', 'floodplain and farmland'), ('Sumas Mountain', 'sumas-mountain-guide', 'City and FVRD parcels side by side'),
            ('Abbotsford East', 'abbotsford-east-guide', 'the McKee plan and steep slopes')],
    'auth': ('City of Abbotsford', 'https://www.abbotsford.ca/'),
    'faq': [{'q': 'How big can a coach house be in Abbotsford?', 'a': 'A coach house or garden suite is capped at 15% of the lot area, up to 100 m². On RR rural lots the cap is the lesser of 90 m² and 40% of the house, and the lot must be over 0.4 ha.'},
            {'q': 'Which Abbotsford plan is current?', 'a': 'Abbotsforward 2050, adopted in December 2025. The 2016 Official Community Plan is no longer in force.'}],
    'sources': [('City of Abbotsford: Zoning Bylaw 2014', 'https://www.abbotsford.ca/city-services/bylaw-services/bylaw-listings/zoning-bylaw-2014'),
                ('City of Abbotsford: Abbotsforward 2050', 'https://www.abbotsford.ca/business-development/community-planning/abbotsforward'),
                ('City of Abbotsford: neighbourhood plans', 'https://www.abbotsford.ca/business-development/community-planning/neighbourhood-plans'),
                ('City of Abbotsford: WebMap', 'https://www.abbotsford.ca/city-services/mapping-data-analytics/webmap'),
                ('City of Abbotsford: development guidelines for the airport (YXX)', 'https://www.abbotsford.ca/sites/default/files/docs/business-development/Development%20Guidlines%20for%20YXX%202020.pdf'),
                ('City of Abbotsford: your tax notice', 'https://www.abbotsford.ca/city-services/property-taxes/your-current-tax-notice'),
                ('Province of BC: rural property tax', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/rural-area'),
                ('Agricultural Land Commission: housing in the ALR', 'https://www.alc.gov.bc.ca/use-of-alr-land/housing-in-the-alr/')],
},
# ------------------------------------------------------------------------------------------------------------------------------ Surrey
'surrey': {
    'title': 'Surrey Home Buying Rules: Zoning, Suites and Multiplexes',
    'h1': 'Buying a Home in Surrey: The Rules',
    'desc': 'Surrey rules for home buyers: the 2050 plan and zoning, small-scale housing unit counts, suites and coach houses, streams, dikes and short-term rentals.',
    'intro': 'Surrey is one City with very different ground, from SkyTrain towers to farmland, and many of its neighbourhoods have their own plans on top of the City-wide rules. These are the City-wide ones, with the City’s sources at the bottom and links to the areas that add their own.',
    'sections': [
        ('Plans and zoning', [
            'The current plan is the Surrey 2050 Official Community Plan, Bylaw No. 21900, adopted June 15, 2026. It replaces the 2013 plan (Bylaw No. 18020), and some older neighbourhood plan designations that listings still quote have been superseded.',
            'Zoning is Surrey Zoning Bylaw, 1993, No. 12000. Look up the parcel’s zone in the City’s mapping before you count on anything.',
            'Subdivision and servicing run under the Subdivision and Development Bylaw, 1986, No. 8830.']),
        ('Small-scale housing', [
            'Since July 8, 2024, eligible lots can have up to three units on lots under 280 m², four units on larger lots, and up to six on lots of at least 281 m² within 400 m of a frequent bus stop.',
            'Lots not connected to City water and sewer are among the exemptions. The new rules don’t make an existing unpermitted suite legal, so check its permit before you count on the rent.']),
        ('Suites, coach houses and garden suites', [
            'One secondary suite is allowed in a single detached house, a semi-detached house or a duplex unit, up to 40% of the main home’s habitable floor area. It can’t be in a coach house or garden suite, and it can never be sold as its own strata lot.',
            'Coach houses and garden suites are allowed in zones that allow houses, duplexes and houseplexes, from 35 m² to 75 m², or up to 120 m² on RA, R2, R2-O and R3 lots where the main house hasn’t used its full floor area.',
            'On ALR land, a suite has to be inside the main house.']),
        ('Streams, floodplain and dikes', [
            'Streamside setbacks are in Part 7A of the zoning bylaw and change with the stream’s class, so the setback for a creek-side lot is read from its own stream.',
            'On the Fraser, a formal dike protects South Westminster and Bridgeview. East of 132 Street to the Langley border there is no dike, and development there had to be built to flood protection levels.',
            'The Serpentine and Nicomekl lowlands have their own flood control system. Check the floodplain map for any low-lying lot.']),
        ('Short-term rentals', [
            'Only the owner can run a short-term rental (under 90 days in a row per guest), only in their own principal residence, and only with a City business licence, listed at $358 a year. Tenants can’t run one, and a strata can ban them too.']),
    ],
    'check': ['The parcel’s 2050 plan designation and zone, not the old plan a listing quotes.', 'Any suite’s permit and its size against the 40% cap.',
              'Stream setbacks and floodplain status on low or creek-side land.', 'Your unit count under the small-scale housing rules, if you plan to build.'],
    'own': [('Barnston Island', 'barnston-island-surrey-guide', 'Metro Vancouver Electoral Area A, not the City: rural taxes and the island ferry'),
            ('Port Kells', 'port-kells-surrey-guide', 'industrial zoning and the undiked river frontage'),
            ('Pacific Douglas', 'pacific-douglas-guide', 'the Douglas plan'), ('Crescent Beach and Ocean Park', 'crescent-beach-ocean-park-guide', 'the Crescent Beach Local Area Plan'),
            ('Fleetwood and Tynehead', 'fleetwood-tynehead-guide', 'the Fleetwood Plan along the SkyTrain line'),
            ('King George Corridor', 'king-george-corridor-guide', 'the heritage Semiahmoo Trail')],
    'auth': ('City of Surrey', 'https://www.surrey.ca/'),
    'faq': [{'q': 'How many units can I build on a Surrey lot?', 'a': 'Since July 8, 2024: up to three on lots under 280 m², four on larger lots, and up to six on lots of at least 281 m² within 400 m of a frequent bus stop, if the lot is eligible and on City water and sewer.'},
            {'q': 'How big can a suite be in Surrey?', 'a': 'Up to 40% of the main home’s habitable floor area, one per house, semi-detached house or duplex unit.'}],
    'sources': [('City of Surrey: Official Community Plan', 'https://www.surrey.ca/renovating-building-development/land-planning-development/official-community-plan'),
                ('City of Surrey: Zoning Bylaw No. 12000', 'https://www.surrey.ca/city-government/bylaws/12000'),
                ('City of Surrey: small-scale multi-unit housing', 'https://www.surrey.ca/renovating-building-development/land-planning-development/provincial-housing-financial-regulations/zoning-small-scale-multi-unit-housing'),
                ('City of Surrey: building or legalizing a secondary suite', 'https://www.surrey.ca/renovating-building-development/building/building-or-legalizing-secondary-suite'),
                ('City of Surrey: coach houses and garden suites', 'https://www.surrey.ca/renovating-building-development/building/residential-building/residential-building-permits/coach-houses-garden-suites'),
                ('City of Surrey: short-term rentals', 'https://www.surrey.ca/renovating-building-development/land-planning-development/provincial-housing-financial-regulations/short-term-rentals'),
                ('City of Surrey: Serpentine and Nicomekl lowlands', 'https://www.surrey.ca/services-payments/water-drainage-sewer/flood-control/lowlands-floodplains/serpentine-nicomekl-lowlands'),
                ('City of Surrey: Corporate Report R267 (2006), Fraser River dikes', 'https://www.surrey.ca/sites/default/files/corporate-reports/RPT_2006_R267.pdf'),
                ('City of Surrey: paying your property taxes', 'https://www.surrey.ca/services-payments/property-taxes/paying-your-property-taxes')],
},
# ------------------------------------------------------------------------------------------------------------------- Township of Langley
'langley': {
    'title': 'Township of Langley Home Buying Rules: Zoning and Suites',
    'h1': 'Buying a Home in the Township of Langley: The Rules',
    'desc': 'Township of Langley rules for buyers: zoning, small-scale housing, the 120 m² suite cap, coach houses, community plans, servicing and tax dates, with sources.',
    'intro': 'The Township of Langley runs from Willoughby’s new streets to farms in the Agricultural Land Reserve. Langley City, in the middle, is a separate municipality with its own bylaws. These are the Township-wide rules, with the Township’s sources at the bottom.',
    'sections': [
        ('Zoning and plans', [
            'Zoning is Township of Langley Zoning Bylaw No. 2500. Get the parcel’s zone from the Township or its GeoSource map first.',
            'The Official Community Plan and the community plans sit on top. The Willoughby Community Plan is now Schedule 6 to Bylaw 6200 (adopted December 1, 2025), and updates to it went to Council in 2026, so check where they stand for a Willoughby lot. Rural land is under the Rural Plan.',
            'Subdivision goes through the Township’s Approving Officer, under Subdivision and Development Servicing Bylaw 2019, No. 5382. Confirm roads, water, sewer or septic and drainage for the specific application.']),
        ('Small-scale housing, suites and coach houses', [
            'Bylaw No. 6020 (adopted November 18, 2024) allows three units on eligible lots of 280 m² or less and four units on larger eligible lots up to 4,050 m². Lots over 4,050 m² aren’t eligible, and there is no six-unit tier in the Township.',
            'A secondary suite in the Township can be up to 120 m².',
            'A coach house is a second home on the same fee-simple lot and title as the main house. It is not a strata lot and can’t be sold on its own.']),
        ('Floodplain and farmland', [
            'On low-lying land, flood status affects insurance and lending. Ask the Township about the lot before you remove subjects.',
            'ALR status is set parcel by parcel on the ALC’s map, and it decides what you can build or split on a rural lot.']),
        ('Co-ops', [
            'In a housing co-op, the co-op approves the buyer and you buy a share, not a strata lot. Its own rules decide who can live there; the strata 55+ exemptions don’t automatically apply.']),
        ('Property taxes', [
            'Township 2026 taxes and utility fees were due July 2, 2026, with 5% added to current-year taxes unpaid at midnight July 2 and another 5% at midnight September 3. Utility fees are now billed separately from taxes.']),
    ],
    'check': ['The parcel’s zone and community plan designation.', 'The unit count you plan against Bylaw 6020 and the lot size.',
              'Any suite against the 120 m² cap, and its permit.', 'Servicing, flood status and ALR status on a rural or edge lot.'],
    'own': [('Willoughby', 'willoughby-guide', 'the Willoughby Community Plan'), ('Fort Langley', 'fort-langley-guide', 'the heritage village'),
            ('Salmon River', 'salmon-river-guide', 'acreage, wells and septic'), ('Milner', 'milner-langley-guide', 'ALR and new development')],
    'auth': ('Township of Langley', 'https://www.tol.ca/'),
    'faq': [{'q': 'How big can a suite be in the Township of Langley?', 'a': 'Up to 120 m².'},
            {'q': 'How many units can I build on a Township of Langley lot?', 'a': 'Under Bylaw 6020, three units on eligible lots of 280 m² or less and four on larger eligible lots up to 4,050 m². Bigger lots aren’t eligible, and there is no six-unit tier.'}],
    'sources': [('Township of Langley: Zoning Bylaw', 'https://www.tol.ca/en/building-development/zoning-bylaw.aspx'),
                ('Township of Langley: small-scale multi-unit housing', 'https://www.tol.ca/en/the-township/small-scale-multi-unit-housing.aspx'),
                ('Township of Langley: community planning', 'https://www.tol.ca/en/the-township/community-planning.aspx'),
                ('Township of Langley: subdivision', 'https://www.tol.ca/en/building-development/subdivision.aspx'),
                ('Township of Langley: property taxes', 'https://www.tol.ca/en/services/property-taxes.aspx'),
                ('Agricultural Land Commission: ALR maps', 'https://www.alc.gov.bc.ca/alr-maps')],
},
# ------------------------------------------------------------------------------------------------------------------------------- Delta
'delta': {
    'title': 'Delta Home Buying Rules: Flood, Farm Zoning and Suites',
    'h1': 'Buying a Home in Delta: The Rules',
    'desc': 'Delta rules for buyers in Ladner, Tsawwassen and North Delta: dikes and flood levels, farm zoning, small-scale housing, lot sizes, taxes and the vacancy tax.',
    'intro': 'One City sets the rules for Ladner, Tsawwassen and North Delta, and on Delta’s low ground the flood rules come first. These are the City-wide rules, with Delta’s own sources at the bottom.',
    'sections': [
        ('Plans and zoning', [
            'The plan is Official Community Plan Bylaw No. 8400, adopted July 8, 2024. Zoning is Zoning Bylaw No. 7600, assigned parcel by parcel on the City’s zoning maps.',
            'Minimum lot sizes on the zone sheets: RS5 550 m² (460 m² outside the single-family designation), RS6 390 m², RS7 335 m², RD1 duplex 836 m², RD4 duplex 504 m², and 4,000 m² for RS1, RS2, RS3, RD2 and RD3 in lower-density areas.',
            'Older condo buildings sit in site-specific or multi-family zones set when they were built, so read the zone off the map rather than assume it.']),
        ('Small-scale housing and suites', [
            'Bylaws No. 8394 and 8395, adopted June 24, 2024, allow small-scale housing on properties zoned for single detached or duplex homes: four units on residential properties, and six within 400 m of frequent transit on Scott Road in North Delta.',
            'The combinations can include a house, a duplex, secondary suites, coach houses and garden suites, where the zone applies. The RS1 zone lists a secondary suite as an accessory use.']),
        ('Flood, dikes and the shoreline', [
            'The City is the diking authority. It runs more than 63 km of flood protection, 31 drainage pump stations and about 538 km of drainage, and is raising sections of the Boundary Bay dike between 72 and 88 Street.',
            'In the Boundary Bay foreshore and Southlands hazard area (SD3), habitable floors must be at least 2.9 m above datum, the ground around new building at least 2.3 m, and nothing can be built within 7.5 m of the tidal boundary.',
            'In the SD2 hazard area, floors must be above the flood construction level, nothing can be built within 7.5 m of the sea or of a dike’s inboard toe, and a covenant acknowledging the flood risk goes on title.',
            'On river-side lots in Ladner, the City has required flood-proofing covenants and rights-of-way so the dike can be raised to 5.5 m. Search title for both.',
            'The Fraser River escarpment in North Delta (ND1) is a hazard area for mud flows, erosion, land slip and subsidence. A geotechnical review belongs in your subjects there.',
            'Any property within 30 m of a stream is in the streamside protection permit area, which can limit additions, coach houses and rebuilds.',
            'The Province owns almost all of the saltwater foreshore. A dock or moorage is held by lease or licence through FrontCounter BC, not with the lot.']),
        ('Farmland', [
            'In the A1 zone a new lot needs 8 ha, except a home site severance under ALC policy. One farm house of up to 500 m² is allowed, on a home plate of up to 3,600 m², with one suite inside it and one accessory farm dwelling of 90 m² (lots of 40 ha or less) or 186 m² (larger lots). A2 also needs 8 ha; A3 doesn’t allow subdivision.']),
        ('Taxes and utilities', [
            'Delta’s 2026 property taxes were due July 2, with 5% added to balances after July 2 and another 5% after September 2. The 2026 flat-rate utility fee for a single-family home is $1,658.',
            'Delta is on the Province’s list of speculation and vacancy tax areas. Tsawwassen First Nation lands aren’t.']),
    ],
    'check': ['The flood construction level, dike rights-of-way and flood covenants on title.', 'The parcel’s zone off the City’s map, and its minimum lot size.',
              'Stream and escarpment permit areas on a creek-side or bluff lot.', 'Any dock or moorage claim, against a provincial tenure.'],
    'own': [('Ladner Rural', 'ladner-rural-guide', 'farmland and dikes'), ('Ladner Elementary', 'ladner-elementary-guide', 'the river-side lots')],
    'auth': ('City of Delta', 'https://www.delta.ca/'),
    'faq': [{'q': 'How many units can I build on a Delta lot?', 'a': 'Under Bylaws 8394 and 8395 (June 24, 2024): four units on residential properties zoned for single detached or duplex homes, and six within 400 m of frequent transit on Scott Road.'},
            {'q': 'Does a Delta waterfront home come with the foreshore?', 'a': 'No. The Province owns almost all of the saltwater foreshore. A dock or moorage is held by lease or licence through FrontCounter BC.'}],
    'sources': [('City of Delta: Housing Our Future (OCP)', 'https://www.delta.ca/building-development/housing-our-future'),
                ('City of Delta: development considerations', 'https://www.delta.ca/building-development/development-planning-approvals/development-considerations'),
                ('City of Delta: A1 zone sheet', 'https://maps.delta.ca/Utilities/ZoningPDF/A1.pdf'),
                ('City of Delta: streamside protection permit guide', 'https://www.delta.ca/sites/default/files/2023-06/Form%20T1%20-%20SPEA%20DPA%20Application%20Guide%20-%20May%202023.pdf'),
                ('City of Delta: small-scale housing notice to the Province (June 26, 2024)', 'https://www.delta.ca/sites/default/files/2024-06/Ravi%20Kahlon_Small-Scale%20Multi-Unit%20Housing_June%2026%2C%202024.pdf'),
                ('City of Delta: property taxes', 'https://www.delta.ca/services/property-taxes-utilities/property-taxes'),
                ('City of Delta: utilities', 'https://www.delta.ca/services/property-taxes-utilities/utilities'),
                ('City of Delta: sanitary sewer and drainage', 'https://www.delta.ca/services/water-sewer-drainage/sanitary-sewer-drainage')],
},
# ------------------------------------------------------------------------------------------------------------------------ Pitt Meadows
'pitt-meadows': {
    'title': 'Pitt Meadows Home Buying Rules: Dikes, Farmland and Suites',
    'h1': 'Buying a Home in Pitt Meadows: The Rules',
    'desc': 'Pitt Meadows rules for home buyers: dikes and pump stations, ALR farmland, farm and rural zoning, suites and garden suites, the rental ban and tax rates.',
    'intro': 'Most of Pitt Meadows is farmland in the Agricultural Land Reserve, and almost all of it sits behind dikes, so farm and flood rules come up here more than in most cities. These are the City-wide rules, with the City’s sources at the bottom.',
    'sections': [
        ('Dikes and drainage', [
            'The City is almost entirely protected by 60 km of dikes. The low northern areas, around the Alouette pump station, Fenton and the Pitt Polder, are drained by floodboxes and pump stations, and the Codd Island wetlands are undiked floodplain.']),
        ('Farmland and rural zoning', [
            'About 78% of the City’s land is in the ALR. Check the parcel on the ALC’s map.',
            'Under Zoning Bylaw No. 2505, 2011: A-1 General Agricultural needs 8 ha and allows one farm house up to 500 m²; A-2 needs 16 ha; rural residential lots outside the ALR need 4 ha (RR-2), 2 ha (RR-3) or 1 ha (RR-4); RS Large Lot Residential needs 0.2 ha.',
            'In A-1 and A-2, buildings must be 15 m back from watercourses and key ditches.']),
        ('Suites, garden suites and small-scale housing', [
            'One secondary suite per house, 33 to 90 m², inside the house, where the zone allows it. Or one garden suite per lot, 33 to 90 m², in the A-1, A-2, RR and RS zones, but not both.',
            'On ALR land, the ALC allows one additional detached home of up to 90 m² on parcels of 40 ha or less, without an application, where its conditions are met.',
            'Small-scale housing unit counts (three, four or six) turn on the 280 m² lot size and the 400 m frequent-transit test. OCP Amendment Bylaw No. 3034, 2025 covers two to six units through suites, garden suites, duplexes, triplexes, townhomes and small apartment buildings.']),
        ('Short-term rentals', [
            'Short-term rental accommodation is not a permitted use under the City’s zoning bylaw, and Pitt Meadows is on the Province’s principal-residence requirement list. A strata’s long-term rental ban is void, but that doesn’t open the door to short-term rentals.']),
        ('Property taxes', [
            'Under the 2026 Annual Tax Rates Bylaw No. 3047, the farm class pays $48.6824 per $1,000 plus a $1.8524 drainage levy, against $2.8438 plus $0.1082 for residential. Check a farm parcel’s BC Assessment class before you budget.',
            '2026 taxes were due July 2, with 5% added after July 2 and another 5% after August 1.']),
        ('Growth plans', [
            'The plan is “I See Pitt Meadows 2040”. The North Lougheed Area Plan, adopted by OCP Amendment Bylaw No. 3060, 2026, covers about 50 ha for gradual development, with more approvals still to come.']),
    ],
    'check': ['ALR status and the zone’s minimum lot size.', 'The farm or residential tax class on the BC Assessment notice.',
              'A suite or a garden suite, not both, and the size limits.', 'Drainage and dike position for low northern land.'],
    'own': [('Central Meadows', 'central-meadows-pitt-meadows-guide', 'town centre'), ('North Meadows', 'north-meadows-pitt-meadows-guide', 'farmland and the polder')],
    'auth': ('City of Pitt Meadows', 'https://www.pittmeadows.ca/'),
    'faq': [{'q': 'Can I run a short-term rental in Pitt Meadows?', 'a': 'No. Short-term rental accommodation is not a permitted use under the City’s zoning bylaw.'},
            {'q': 'Can I have both a suite and a garden suite in Pitt Meadows?', 'a': 'No. A lot can have one secondary suite or one garden suite, each 33 to 90 m², not both.'}],
    'sources': [('City of Pitt Meadows: Zoning Bylaw No. 2505 (consolidated)', 'https://www.pittmeadows.ca/sites/default/files/2025-04/Zoning%20Bylaw%20No.%202505%2C%202011%20-%20Consolidated%20Version_0.pdf'),
                ('City of Pitt Meadows: garden suites', 'https://www.pittmeadows.ca/sites/default/files/docs/homes-development/information_sheet_-_planning_-_garden_suitesv4.pdf'),
                ('City of Pitt Meadows: 2026 Annual Tax Rates Bylaw No. 3047', 'https://www.pittmeadows.ca/sites/default/files/2026-05/2026-Annual-Tax-Rates-Bylaw-No-3047%2C-2026.pdf'),
                ('City of Pitt Meadows: Official Community Plan', 'https://www.pittmeadows.ca/ocp'),
                ('City of Pitt Meadows: North Lougheed Area Plan', 'https://www.pittmeadows.ca/homes-development/zoning-land-use/north-lougheed-area-plan'),
                ('City of Pitt Meadows: SSMUH and transit-oriented areas update (Dec 2, 2025)', 'https://www.pittmeadows.ca/sites/default/files/2025-12/Dec_2_2025_SSMUH_Transit_Oriented_Areas_Implementation_Update.pdf'),
                ('City of Pitt Meadows: Business Plan 2020', 'https://www.pittmeadows.ca/sites/default/files/2022-03/pitt-meadows_business-plan_2020-web-full02.pdf'),
                ('Agricultural Land Commission: housing in the ALR', 'https://www.alc.gov.bc.ca/use-of-alr-land/housing-in-the-alr/')],
},
}

NAME = {'maple-ridge': 'Maple Ridge', 'chilliwack': 'Chilliwack', 'cultus-lake': 'Cultus Lake', 'abbotsford': 'Abbotsford', 'surrey': 'Surrey',
        'langley': 'the Township of Langley', 'delta': 'Delta', 'pitt-meadows': 'Pitt Meadows'}


def build(slug, c, old):
    nm = NAME[slug]; short = nm.replace('the ', '')
    B = [{'t': 'notice', 'text': f'Draft for Jared’s approval. Rewritten November 11, 2026 in plain words from the sourced rules on the {short} guides; the official sources are listed at the bottom.', 'gen': G},
         {'t': 'p', 'text': c['intro'], 'gen': G}]
    for h, items in c['sections']:
        B.append({'t': 'h', 'level': 2, 'text': h, 'gen': G})
        B.append({'t': 'list', 'items': [parts(i) for i in items], 'gen': G})
    B.append({'t': 'h', 'level': 2, 'text': f'Before you remove subjects in {short}', 'gen': G})
    B.append({'t': 'list', 'items': [parts(i) for i in c['check']], 'gen': G})
    B.append({'t': 'p', 'parts': parts(['Rules change, so confirm anything that matters for your purchase with the ', (c['auth'][0], c['auth'][1]), ' and your lawyer.']), 'gen': G})
    B.append({'t': 'h', 'level': 2, 'text': 'Areas with their own rules', 'gen': G})
    B.append({'t': 'list', 'items': [[{'t': f'{n} guide', 'h': f'/{s}.html'}, {'t': f': {why}'}] for n, s, why in c['own']], 'gen': G})
    B.append({'t': 'h', 'level': 2, 'text': 'Rules that are the same everywhere in BC', 'gen': G})
    B.append({'t': 'list', 'items': [[{'t': t, 'h': f'/{s}.html'}] for t, s in BC], 'gen': G})
    B.append({'t': 'h', 'level': 2, 'text': 'Sources', 'gen': G})
    B.append({'t': 'list', 'items': [[{'t': t, 'h': u}] for t, u in c['sources']], 'gen': G})
    guides = next((b for b in old['blocks'] if b.get('t') == 'list' and any(it and str(it[0].get('h', '')).endswith('-guide.html') for it in b['items'])
                   and old['blocks'][old['blocks'].index(b) - 1].get('text') == 'Neighbourhood guides that use this page'), None)
    if guides:
        B.append({'t': 'h', 'level': 2, 'text': 'Neighbourhood guides that use this page', 'gen': G}); B.append({**guides, 'gen': G})
    return {'status': 'draft', 'slug': f'{slug}-home-buying-rules', 'updated': TODAY, 'curated': TODAY, 'guides': old.get('guides', []),
            'new_page': {'h1': c['h1'], 'title': c['title'], 'description': c['desc']},
            'breadcrumbs': old['breadcrumbs'], 'blocks': B, 'faq': c['faq']}


def main():
    for slug, c in CITIES.items():
        assert 38 <= len(c['title']) <= 60, (slug, len(c['title']))
        assert 135 <= len(c['desc']) <= 158 and c['desc'].endswith('.'), (slug, len(c['desc']))
        for _, s, _ in c['own']: assert os.path.exists(f'dist/{s}.html'), (slug, s)
        f = f'src/data/local/{slug}-home-buying-rules.json'; old = json.load(open(f, encoding='utf-8'))
        open(f, 'w', encoding='utf-8').write(json.dumps(build(slug, c, old), ensure_ascii=False, indent=2) + '\n')
    print('rules pages rewritten:', len(CITIES))


if __name__ == '__main__': main()
