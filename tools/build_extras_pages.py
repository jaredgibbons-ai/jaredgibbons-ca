#!/usr/bin/env python3
"""Houses-with-suites and penthouse searches from Pete's Paragon export (src/data/sold/sold-extras.json; Closed sales, November 1, 2025 to August 31, 2026).

    houses with suites  surrey, cloverdale, south-surrey, langley, abbotsford, burnaby, coquitlam, richmond, vancouver, north-delta, maple-ridge, chilliwack   (12 new draft pages)
    penthouses          vancouver, burnaby, richmond, surrey, coquitlam, new-westminster   (6 new draft pages)  + sold figures added to the Langley, Abbotsford and South Surrey/White Rock penthouse drafts

Same pattern as build_new_searches.py: src/data/local/<slug>.json with a new_page header and status draft, a listings placeholder (grid), SEO entries in tools/seo_final/fix_02.json,
inbound links on the city hubs, and one row per page appended to docs/review/idx/new-searches-2026-11-06.xlsx for Jerry.  Rules text comes only from the sourced city notes in
docs/research.  Idempotent.

    python3 -I tools/build_extras_pages.py [--xlsx]
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
from build_new_searches import P, H, L, tbl, money, num, sqft, lk, hpi, hpi_table, hubmap, nz, disp, EX, EXW, SRC_GVR, SRC_FV

G = 'xtra'; LG = 'xtralinks'
QL = ['November 2025 to January 2026', 'February to April 2026', 'May to July 2026', 'August 2026']
BANDS_H = N.BANDS
BANDS_C = ['Under $500,000', '$500,000 to $749,999', '$750,000 to $999,999', '$1,000,000 to $1,499,999', '$1,500,000 to $1,999,999', '$2,000,000 and over']
SRC = (f'Source: Paragon closed sales, {EXW}. Pending sales are not counted, and the export is incomplete after August 2026, so later months are left out. '
       'Median means the middle price. A figure is shown only where at least 5 homes sold.')
SUITE_NOTE = ('A legal suite here means Paragon lists the suite as Legal Suite or Licensed Suite. An unauthorized suite is one the listing marks Unauthorized Suite. Houses with no suite, or with the suite field left blank, are not counted in either column.')

# ---------------------------------------------------------------------------- city config
SUITE = {
 'surrey': dict(name='Surrey', ex='surrey', area='Surrey and North Surrey', hub='surrey-neighbourhood-guides', hpi=[('fvreb', 'Surrey'), ('fvreb', 'North Surrey')], hpi_src=SRC_FV, snap='surrey',
    desc='Fleetwood, Newton, Guildford, Whalley and Fraser Heights', mls='Surrey + North Surrey',
    rules=[
      'Surrey allows one secondary suite per single-family, semi-detached or duplex unit, up to 40% of the main unit’s habitable floor area, under Zoning Bylaw No. 12000. A suite cannot go inside a coach house or garden suite, and it cannot be sold as its own strata lot.',
      'Surrey says its July 2024 small-scale zoning changes do not make an unpermitted suite legal after the fact. A suite that was built without a permit stays unauthorized until the owner legalizes it, which is why the two columns above are kept apart.',
      'The same changes let a lot under 280 square metres take 3 units and a larger lot 4, and up to 6 on an eligible lot of at least 281 square metres within 400 metres of a frequent bus stop. A house with a suite on a lot that size may be worth more as a site than as a house.'],
    costs='Surrey’s 2026 residential property tax rate is $3.42731 per $1,000 of assessed value. A legal secondary suite in the main house adds $454.00 for water and $821.71 for sewer in 2026, $1,275.71 in all, plus $172.04 for garbage. Flat-rate utilities for a house without a suite are $1,195 for water and $1,661 for sewer, and $344.08 for waste.',
    ask='Ask whether the suite is on the City’s utility account. Surrey adds water, sewer and garbage charges for a legal suite.',
    links=[('Surrey houses for sale', 'surrey-houses-for-sale'), ('Surrey houses with coach houses', 'surrey-houses-with-coach-houses-for-sale'), ('Surrey homes for sale', 'surrey-homes-for-sale'), ('Surrey half duplexes for sale', 'surrey-duplexes-for-sale'), ('Surrey neighbourhood guides', 'surrey-neighbourhood-guides'), ('Surrey market stats', 'surrey-real-estate-market-stats'), ('South Surrey duplexes with suites', 'south-surrey-duplexes-with-suites-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Sell my house in Surrey', 'sell-my-house-in-surrey'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'cloverdale': dict(name='Cloverdale', ex='cloverdale', area='Cloverdale and Clayton', hub='cloverdale-neighbourhood-guides', hpi=[('fvreb', 'Cloverdale')], hpi_src=SRC_FV, snap='cloverdale',
    desc='Cloverdale town, Clayton and the farmland edges', mls='Cloverdale',
    rules=[
      'Cloverdale is part of the City of Surrey, so Surrey’s suite rules apply. One secondary suite is allowed per single-family, semi-detached or duplex dwelling, and its habitable floor area may not exceed 40% of the principal dwelling unit.',
      'A suite is not permitted inside a coach house or garden suite. Clayton’s small lots are where that matters most: a house there can have a suite in the main house or a coach house over the garage, but the suite and the coach house are separate decisions.',
      'On farmland the Agricultural Land Commission’s rules sit on top of the City’s. A parcel in the Reserve may have a secondary suite only inside the principal residence, so a suite listed in a separate building on acreage needs a closer look.'],
    costs=None,
    ask='Ask whether the suite is on the City’s utility account. Surrey adds water, sewer and garbage charges for a legal suite.',
    links=[('Cloverdale houses for sale', 'cloverdale-houses-for-sale'), ('Cloverdale houses with coach houses', 'cloverdale-houses-with-coach-houses-for-sale'), ('Cloverdale homes under $1.8 million', 'cloverdale-homes-under-1-8m'), ('Cloverdale half duplexes', 'cloverdale-duplexes-for-sale'), ('Cloverdale neighbourhood guides', 'cloverdale-neighbourhood-guides'), ('Surrey houses with suites', 'surrey-houses-with-suites-for-sale'), ('Surrey houses for sale', 'surrey-houses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'south-surrey': dict(name='South Surrey', ex='south-surrey', area='South Surrey', hub='south-surrey-neighbourhood-guides', hpi=[('fvreb', 'South Surrey & White Rock')], hpi_src=SRC_FV, snap='south-surrey-white-rock',
    desc='Crescent Beach, Ocean Park, Grandview, Morgan Creek and the King George corridor', mls='South Surrey White Rock, without the White Rock sub-area',
    rules=[
      'South Surrey is in the City of Surrey, so one secondary suite is allowed per single-family, semi-detached or duplex dwelling, capped at 40% of the principal dwelling unit’s habitable area under Bylaw No. 12000.',
      'White Rock is a separate city with its own rules and is not in these figures. Its Zoning Bylaw 2024, No. 2506 allows no more than one of a list of accessory uses with a one-unit residential use, and a registered secondary suite is on that list next to boarding and a bed and breakfast. Surrey’s rule is different, so confirm the city before you read a listing.',
      'Large South Surrey lots are where suites meet the small-scale multi-unit rules. A lot of at least 281 square metres within 400 metres of a frequent bus stop can take up to 6 units, so a suite house on a big lot is worth pricing as a site too.'],
    costs=None,
    ask='Confirm the lot is on the Surrey side of the line. A listing with a White Rock mailing address can still sit in South Surrey, and the reverse is true too.',
    links=[('South Surrey houses for sale', 'south-surrey-houses-for-sale'), ('South Surrey houses with coach houses', 'south-surrey-houses-with-coach-houses-for-sale'), ('South Surrey duplexes with suites', 'south-surrey-duplexes-with-suites-for-sale'), ('South Surrey homes for sale', 'south-surrey-homes-for-sale'), ('South Surrey neighbourhood guides', 'south-surrey-neighbourhood-guides'), ('Surrey houses with suites', 'surrey-houses-with-suites-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'langley': dict(name='Langley', ex='langley', area='the City and Township of Langley', hub='langley-neighbourhood-guides', hpi=[('fvreb', 'Langley')], hpi_src=SRC_FV, snap='langley',
    desc='Willoughby, Walnut Grove, Murrayville, Brookswood and Aldergrove', mls='Langley',
    rules=[
      '“Langley” is two municipalities, and their suite rules differ. In the City of Langley, Bylaw No. 3300 caps a secondary suite at the lesser of 100 square metres and 40% of the building’s gross floor area. The owner must live on the lot, there must be at least one extra off-street parking space, and the suite must be inspected, approved through a building permit and recorded in the City’s secondary suites registry.',
      'In the Township of Langley, Zoning Bylaw No. 2500, section 102, caps a secondary suite at 120 square metres of gross floor area, allows up to one suite per principal dwelling unit, and requires a building permit for every suite. Listings in Willoughby often describe a suite as legal, so ask for the permit and not just the wording.',
      'The Township’s small-scale multi-unit rules arrived in Zoning Bylaw 6020, adopted November 18, 2024, which allows 3 to 4 units on eligible lots. The Township expected about 55% of its single-family and duplex lots, roughly 15,000 properties, to qualify. There is no 6-unit tier in the Township.'],
    costs=None,
    ask='Find out which municipality the house is in before you read the suite rules. The City of Langley keeps a registry of secondary suites, so ask whether this one is recorded in it.',
    links=[('Langley houses for sale', 'langley-houses-for-sale'), ('Langley houses with coach houses', 'langley-houses-with-coach-houses-for-sale'), ('Langley homes for sale', 'langley-homes-for-sale'), ('City of Langley homes for sale', 'city-of-langley-homes-for-sale'), ('Langley neighbourhood guides', 'langley-neighbourhood-guides'), ('Langley penthouses', 'langley-penthouses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Schools in Langley', 'schools-in-langley-bc'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'abbotsford': dict(name='Abbotsford', ex='abbotsford', area='Abbotsford', hub='abbotsford-neighbourhood-guides', hpi=[('fvreb', 'Abbotsford')], hpi_src=SRC_FV, snap='abbotsford',
    desc='West Abbotsford, Central Abbotsford, Aberdeen, Eagle Mountain and Abbotsford East', mls='Abbotsford',
    rules=[
      'Abbotsford’s Zoning Bylaw No. 2400-2014 (section 140.3.8) permits one secondary suite in every single detached dwelling. The suite must be smaller than 50% of the principal unit, a rule that replaced an older 100 square metre cap.',
      'City council reports describe the lot tests a suite has to meet: a lot of at least 400 square metres, frontage of at least 12.0 metres, a Collector or Local road, and not a cul-de-sac bulb. A house that fails a test may still have a suite in the listing, so ask the City about the lot, not just the house.',
      'A coach house or garden suite is a separate matter. Abbotsford allows one to occupy up to 15% of the lot area, to a maximum of 100 square metres. That is Abbotsford’s rule alone and does not carry into Mission, Chilliwack or the Langleys. The City adopted its small-scale multi-unit amendments in June 2024.'],
    costs=None,
    ask='Ask whether the lot meets the City’s suite tests (400 square metres, 12.0 metres of frontage, a Collector or Local road, not a cul-de-sac bulb). A suite that was permitted on a lot that no longer meets them is worth a call to the City.',
    links=[('Abbotsford houses for sale', 'abbotsford-houses-for-sale'), ('Abbotsford homes for sale', 'abbotsford-homes-for-sale'), ('Abbotsford penthouses', 'abbotsford-penthouses-for-sale'), ('Abbotsford neighbourhood guides', 'abbotsford-neighbourhood-guides'), ('West Abbotsford houses', 'abbotsford-west-houses-for-sale'), ('Abbotsford East houses', 'abbotsford-east-houses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'burnaby': dict(name='Burnaby', ex='burnaby', area='Burnaby North, Burnaby South and Burnaby East', hub='burnaby-neighbourhood-guides', hpi=[('gvr', 'Burnaby North'), ('gvr', 'Burnaby South'), ('gvr', 'Burnaby East')], hpi_src=SRC_GVR, snap='burnaby',
    desc='Capitol Hill, Vancouver Heights, South Slope, Deer Lake and Edmonds', mls='Burnaby North + Burnaby South + Burnaby East',
    rules=[
      'Since July 1, 2024 nearly every Burnaby house lot sits in the R1 Small-Scale Multi-Unit Housing District. A lot of 280 square metres (3,014 square feet) or less can take 3 units and a larger lot 4, and 5 to 6 units are possible only in a Frequent Transit Neighbourhood Area.',
      'A secondary suite counts toward the lot’s unit total, you get one suite per primary unit, and the suite stays on the same title as the house. Burnaby has a new Zoning Bylaw 2026, adopted June 9, 2026 and effective July 1, 2026.',
      'Lots beside a creek fall under the Streamside Protection and Enhancement Development Permit Area, and the City’s application checklist, effective August 1, 2026, asks for a geotechnical report on sloped sites. On a sloped lot, ask whether the suite was built with the permit and the engineering that goes with it.'],
    costs='Burnaby’s 2026 municipal residential rate is $1.72223 per $1,000 of assessed value, plus a Metro Vancouver rate of $0.05440. A detached house pays $652.33 for 2026 water and $159 for the default garbage toter. Renting a suite adds $326.17 for water and $403.00 for sewer. Burnaby is a Speculation and Vacancy Tax area.',
    ask='Ask whether the extra water and sewer charge for a rented suite is being billed. Burnaby adds $326.17 for water and $403.00 for sewer when a suite is rented.',
    links=[('Burnaby houses for sale', 'burnaby-houses-for-sale'), ('Burnaby homes for sale', 'burnaby-homes-for-sale'), ('Burnaby condos for sale', 'burnaby-condos-for-sale'), ('Burnaby neighbourhood guides', 'burnaby-neighbourhood-guides'), ('Burnaby market stats', 'burnaby-real-estate-market-stats'), ('Burnaby penthouses', 'burnaby-penthouses-for-sale'), ('Burnaby lots and land', 'burnaby-lots-land'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'coquitlam': dict(name='Coquitlam', ex='coquitlam', area='Coquitlam', hub='coquitlam-neighbourhood-guides', hpi=[('gvr', 'Coquitlam')], hpi_src=SRC_GVR, snap='coquitlam',
    desc='Burke Mountain, Westwood Plateau, Eagle Ridge, Ranch Park and Maillardville', mls='Coquitlam',
    rules=[
      'Coquitlam’s zoning bylaw is No. 3000, and Council adopted the small-scale multi-unit housing changes on June 9, 2025. A lot of 280 square metres or smaller can take up to 3 units, and a lot over 280 and under 4,050 square metres can take up to 4. The 6-unit tier does not apply, because the City says Coquitlam has no bus stops that meet the provincial frequent-service rule.',
      'Most low-density lots sit in R-1, R-2, R-3 or R-4, each with its own minimum lot size for adding units, from 465 square metres in R-2 to 930 square metres in R-4. The forms allowed include secondary suites, carriage houses, laneway homes, garden cottages, duplexes, triplexes and fourplexes.',
      'Lots that are not connected to municipal water or sewer fall outside the small-scale rules. Talk to the City’s Development Services before you plan around a suite if there is a creek on or next to the lot, a steep slope, or a house built before 1945.'],
    costs='Coquitlam’s 2026 municipal residential rate is $2.2756 per $1,000 of assessed value, $3.8520 with the other taxing authorities. Taxes were due July 2, 2026. Coquitlam is a Speculation and Vacancy Tax area.',
    ask='Check for a creek, a steep slope or a pre-1945 house before you buy for the suite. A Watercourse Protection Development Permit applies within 30 metres of the top of bank.',
    links=[('Coquitlam houses for sale', 'coquitlam-houses-for-sale'), ('Coquitlam homes for sale', 'coquitlam-homes-for-sale'), ('Coquitlam condos for sale', 'coquitlam-condos-for-sale'), ('Coquitlam neighbourhood guides', 'coquitlam-neighbourhood-guides'), ('Coquitlam penthouses', 'coquitlam-penthouses-for-sale'), ('Burke Mountain houses', 'burke-mountain-coquitlam-houses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'richmond': dict(name='Richmond', ex='richmond', area='Richmond', hub='richmond-neighbourhood-guides', hpi=[('gvr', 'Richmond')], hpi_src=SRC_GVR, snap=None,
    desc='Steveston, Broadmoor, Seafair, Blundell and Westwind', mls='Richmond',
    rules=[
      'Richmond’s Zoning Bylaw No. 8500 lists a secondary suite as a secondary use in the RS1 and RS2 single detached zones. Under section 5.4 a suite must be at least 33.0 square metres and no more than the lesser of 40% of the dwelling’s floor area or 110 square metres.',
      'The City states that it allows at least one secondary suite or accessory dwelling unit per lot, and the provincial small-scale multi-unit housing minimums of 3 units on a lot of 280 square metres or less and 4 units on a larger lot apply.',
      'Richmond is protected by 49 kilometres of dikes, and Richmond Fire-Rescue says pockets of liquefaction are possible in a significant earthquake. Ask for the age and permit of any below-grade suite, and whether the lot has had water problems.'],
    costs=None,
    ask='Ask for the building permit and the final inspection for the suite, and confirm the suite is within the 110 square metre and 40% limits in Zoning Bylaw No. 8500.',
    links=[('Richmond houses for sale', 'richmond-houses-for-sale'), ('Richmond homes for sale', 'richmond-homes-for-sale'), ('Richmond condos for sale', 'richmond-condos-for-sale'), ('Richmond townhomes for sale', 'richmond-townhomes-for-sale'), ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'), ('Richmond penthouses', 'richmond-penthouses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'vancouver': dict(name='Vancouver', ex='vancouver', area='Vancouver West and Vancouver East', hub='vancouver-neighbourhood-guides', hpi=[('gvr', 'Vancouver West'), ('gvr', 'Vancouver East')], hpi_src=SRC_GVR, snap=None,
    desc='Kitsilano, Dunbar, Kerrisdale, Hastings-Sunrise, Renfrew and Kensington', mls='Vancouver West + Vancouver East',
    rules=[
      'On October 17, 2023 Vancouver replaced nine RS zones with a single R1-1 zone for about 65,000 lots. R1-1 allows a house with a secondary suite or a laneway house, a duplex, character retention, and multiplexes of 3 to 6 strata units or up to 8 rental units.',
      'Under the R1-1 schedule the minimum site area is 306 square metres for a single detached house or duplex, with larger minimums of 464 square metres for 5 units and 557 square metres for 6 to 8 units. A lot that meets those can carry a multiplex as well as a suite and a laneway house in the forms the schedule states.',
      'Vancouver’s Empty Homes Tax is 3% of assessed value for a home that is neither occupied nor rented, and the Tenant Relocation and Protection Policy applies citywide if a rented building is redeveloped. A suite that is rented matters to both.'],
    costs=None,
    ask='If the suite is rented, ask for the tenancy agreement and the rent. The Tenant Relocation and Protection Policy applies if a rented building is redeveloped, which matters on a lot that could carry a multiplex.',
    links=[('Vancouver houses for sale', 'vancouver-houses-for-sale'), ('Vancouver homes for sale', 'vancouver-homes-for-sale'), ('Vancouver condos for sale', 'vancouver-condos-for-sale'), ('Vancouver townhomes for sale', 'vancouver-townhomes-for-sale'), ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'), ('Vancouver penthouses', 'vancouver-penthouses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'north-delta': dict(name='North Delta', ex='north-delta', area='North Delta', hub='north-delta-neighbourhood-guides', hpi=[('fvreb', 'North Delta')], hpi_src=SRC_FV, snap='north-delta',
    desc='Sunshine Hills, Annieville, Nordel, Scottsdale and Sungod', mls='N. Delta',
    rules=[
      'Delta adopted its small-scale multi-unit housing zoning on June 24, 2024 (Bylaws 8394 and 8395). It allows combinations of single detached dwellings, duplexes, secondary suites, coach houses and garden suites where the zoning applies.',
      'Delta’s published guidance permits registered secondary suites and detached garden suites or coach houses on qualifying lots, subject to floodplain, coverage and parking rules. The wording for a specific lot depends on its zone, so confirm it with the Corporation of Delta before you price a suite as a feature.',
      'Delta is its own municipality, and rules from Surrey, which borders North Delta along the Scott Road side, do not carry across. A listing that quotes a Surrey suite limit is quoting the wrong city.'],
    costs=None,
    ask='Ask whether the suite is registered with Delta and whether the lot is in a floodplain, since floodplain, coverage and parking rules all apply to suites there.',
    links=[('North Delta houses for sale', 'north-delta-houses-for-sale'), ('North Delta homes for sale', 'north-delta-homes-for-sale'), ('North Delta neighbourhood guides', 'north-delta-neighbourhood-guides'), ('Ladner homes for sale', 'ladner-homes-for-sale'), ('Delta homes for sale', 'delta-homes-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'maple-ridge': dict(name='Maple Ridge', ex='maple-ridge', area='Maple Ridge', hub='maple-ridge-neighbourhood-guides', hpi=[('gvr', 'Maple Ridge')], hpi_src=SRC_GVR, snap='maple-ridge',
    desc='Albion, Cottonwood, Haney, Thornhill and Websters Corners', mls='Maple Ridge',
    rules=[
      'In Maple Ridge one secondary suite per lot is permitted in the zones the City lists, including A-1, A-2 and A-3. The suite has to be contained within the single detached building, can be up to 40% of the gross floor area, and is not permitted in the Floodplain Area.',
      'On parcels in the Agricultural Land Reserve the Agricultural Land Commission’s rules govern as well. They allow one secondary suite in the principal residence, and an additional residence only when the Commission’s conditions are met.',
      'A suite in a separate building on acreage is not a secondary suite under these rules, so ask what the listing is describing.'],
    costs=None,
    ask='Check the floodplain map for the lot. A suite is not permitted in the Floodplain Area, so a suite in a low-lying house needs the permit history to be clear.',
    links=[('Maple Ridge houses for sale', 'maple-ridge-houses-for-sale'), ('Maple Ridge homes for sale', 'maple-ridge-homes-for-sale'), ('Maple Ridge neighbourhood guides', 'maple-ridge-neighbourhood-guides'), ('Albion houses', 'albion-maple-ridge-houses-for-sale'), ('Thornhill houses', 'thornhill-maple-ridge-houses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'chilliwack': dict(name='Chilliwack', ex='chilliwack', area='Chilliwack and Sardis', hub='chilliwack-neighbourhood-guides', hpi=[], hpi_src=None, snap=None,
    desc='Sardis, Vedder, Promontory, Chilliwack Mountain and Chilliwack Proper', mls='Chilliwack + Sardis',
    rules=[
      'Chilliwack allows one accessory dwelling unit per lot where the zone permits, and that unit can be a secondary suite, a coach house or a garden suite. A legal suite therefore rules out a coach house on the same lot.',
      'A secondary suite is capped at the lesser of 90 square metres and 40% of the building’s habitable floor space, inside a building that has only one principal dwelling unit. It is a “lesser of” test, so a small house can fail the 40% limit well before it reaches 90 square metres. Garden suites are capped at 100 square metres.',
      'The City’s Secondary Suites Policy permits rental of a suite within any single detached dwelling regardless of zone. A suite must be built with a building permit, meet the BC Building and Fire Code and current flood protection requirements, and new suites are not permitted below the flood construction level. Bylaw 5395, adopted June 18, 2024, allows 3 to 4 units inside the urban growth boundary.'],
    costs=None,
    ask='Ask where the suite sits against the flood construction level. New suites below it are not permitted under the Floodplain Regulation Bylaw, so a basement suite built before the current rules needs its history checked.',
    links=[('Chilliwack houses for sale', 'chilliwack-houses-for-sale'), ('Chilliwack homes for sale', 'chilliwack-homes-for-sale'), ('Chilliwack neighbourhood guides', 'chilliwack-neighbourhood-guides'), ('Sardis houses for sale', 'sardis-houses-for-sale'), ('Suite and short-term rental rules', 'fraser-valley-short-term-rental-and-suite-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
}

PENT = {
 'vancouver': dict(name='Vancouver', ex='vancouver', area='Vancouver West and Vancouver East', hub='vancouver-neighbourhood-guides', hpi=[('gvr', 'Vancouver West'), ('gvr', 'Vancouver East')], hpi_src=SRC_GVR, mls='Vancouver West + Vancouver East',
    desc='the downtown peninsula, Kitsilano, Fairview, Mount Pleasant and the east side',
    facts=['In Yaletown the Canada Line stops at Yaletown-Roundhouse, and the Yaletown Historic Area (HA-3) limits building height to 21.4 metres. Parts of False Creek North are exposed to flooding as sea level rises, so ask a strata in that area what it has planned.', 'The Empty Homes Tax charges 3% of assessed value on a home that is neither occupied nor rented.'],
    links=[('Vancouver condos for sale', 'vancouver-condos-for-sale'), ('Vancouver homes for sale', 'vancouver-homes-for-sale'), ('Vancouver townhomes for sale', 'vancouver-townhomes-for-sale'), ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'), ('Vancouver presale condos and townhomes', 'vancouver-presale-condos-and-townhomes'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'burnaby': dict(name='Burnaby', ex='burnaby', area='Burnaby North, Burnaby South and Burnaby East', hub='burnaby-neighbourhood-guides', hpi=[('gvr', 'Burnaby North'), ('gvr', 'Burnaby South'), ('gvr', 'Burnaby East')], hpi_src=SRC_GVR, mls='Burnaby North + Burnaby South + Burnaby East',
    desc='Metrotown, Brentwood, Lougheed and the Edmonds and Royal Oak corridors',
    facts=['Burnaby’s 2026 municipal residential rate is $1.72223 per $1,000 of assessed value, with a Metro Vancouver rate of $0.05440 on top, and the city is inside the Speculation and Vacancy Tax area.', 'The Burnaby 2050 Official Community Plan was adopted on December 9, 2025, and the new Zoning Bylaw 2026 took effect July 1, 2026.'],
    links=[('Burnaby condos for sale', 'burnaby-condos-for-sale'), ('Burnaby homes for sale', 'burnaby-homes-for-sale'), ('Burnaby townhomes for sale', 'burnaby-townhomes-for-sale'), ('Burnaby neighbourhood guides', 'burnaby-neighbourhood-guides'), ('Burnaby market stats', 'burnaby-real-estate-market-stats'), ('Burnaby presale condos and townhomes', 'burnaby-presale-condos-and-townhomes'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'richmond': dict(name='Richmond', ex='richmond', area='Richmond', hub='richmond-neighbourhood-guides', hpi=[('gvr', 'Richmond')], hpi_src=SRC_GVR, mls='Richmond',
    desc='the City Centre towers, Brighouse, West Cambie, Steveston and Hamilton',
    facts=['Richmond’s 49 kilometres of dikes protect the city, and Richmond Fire-Rescue says pockets of liquefaction are possible in a significant earthquake. Before you offer, ask the strata about building insurance, the depreciation report and any past water damage.'],
    links=[('Richmond condos for sale', 'richmond-condos-for-sale'), ('Richmond homes for sale', 'richmond-homes-for-sale'), ('Richmond townhomes for sale', 'richmond-townhomes-for-sale'), ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'surrey': dict(name='Surrey', ex='surrey', area='Surrey and North Surrey', hub='surrey-neighbourhood-guides', hpi=[('fvreb', 'Surrey'), ('fvreb', 'North Surrey')], hpi_src=SRC_FV, mls='Surrey + North Surrey',
    desc='Surrey City Centre, Guildford, Fleetwood and Newton',
    facts=['For 2026 Surrey’s residential property tax rate is $3.42731 per $1,000 of assessed value. The Surrey 2050 Official Community Plan, Bylaw No. 21900, was adopted on June 15, 2026.'],
    links=[('Surrey condos for sale', 'surrey-condos-for-sale'), ('Surrey homes for sale', 'surrey-homes-for-sale'), ('Surrey houses with suites', 'surrey-houses-with-suites-for-sale'), ('Surrey neighbourhood guides', 'surrey-neighbourhood-guides'), ('Surrey market stats', 'surrey-real-estate-market-stats'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'coquitlam': dict(name='Coquitlam', ex='coquitlam', area='Coquitlam', hub='coquitlam-neighbourhood-guides', hpi=[('gvr', 'Coquitlam')], hpi_src=SRC_GVR, mls='Coquitlam',
    desc='Coquitlam Centre, Burquitlam, Maillardville and the Evergreen Line stations',
    facts=['Coquitlam’s 2026 residential rate is $2.2756 per $1,000 of assessed value for the municipality, or $3.8520 with the other taxing authorities, and taxes fell due on July 2, 2026. The city is inside the Speculation and Vacancy Tax area.', 'Coquitlam adopted its Interim Official Community Plan, Bylaw No. 5511, on April 27, 2026.'],
    links=[('Coquitlam condos for sale', 'coquitlam-condos-for-sale'), ('Coquitlam homes for sale', 'coquitlam-homes-for-sale'), ('Coquitlam houses for sale', 'coquitlam-houses-for-sale'), ('Coquitlam neighbourhood guides', 'coquitlam-neighbourhood-guides'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
 'new-westminster': dict(name='New Westminster', ex='new-westminster', area='New Westminster', hub='new-westminster-neighbourhood-guides', hpi=[('gvr', 'New Westminster')], hpi_src=SRC_GVR, mls='New Westminster',
    desc='Downtown, Uptown, Quay, Sapperton and the Brow of the Hill',
    facts=['New Westminster’s Official Community Plan is “Our City 2041,” Bylaw No. 7925, 2017, and Uptown is a Frequent Transit Development Area, where the City directs higher-density, transit-supportive growth. Zoning is Zoning Bylaw No. 6680, 2001.',
           'Ask what the zoning allows on the sites around the building. A view is only as safe as the neighbouring lots, and a nearby site that can still be built higher can change it.'],
    links=[('New Westminster condos for sale', 'new-westminster-condos-for-sale'), ('New Westminster homes for sale', 'new-westminster-homes-for-sale'), ('New Westminster neighbourhood guides', 'new-westminster-neighbourhood-guides'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('Mortgage calculator for BC', 'mortgage-calculator')]),
}


# Rules, costs and the two city-specific questions for each suite page.  Worded fresh so they do not repeat the paragraphs on the house and coach house searches.
SUITE['surrey'].update(
    rules=['Under Surrey’s Zoning Bylaw No. 12000, each single-family, semi-detached or duplex unit may have one secondary suite, and the suite’s habitable floor area cannot pass 40% of the principal unit. A suite is not allowed inside a coach house or garden suite, and it can’t be strata-titled on its own.',
           'A suite built without a permit does not become legal because Surrey changed its zoning in July 2024. The City has said the new rules do not legalize unpermitted suites after the fact, and that is the line between the two columns in the table above.',
           'The same July 2024 rules changed what a lot can hold. A lot under 280 square metres can take 3 units and a larger one 4, and an eligible lot of 281 square metres or more within 400 metres of a frequent bus stop can take as many as 6, so some suite houses are worth comparing as building sites.'],
    costs='Surrey’s 2026 property tax rate is $3.42731 per $1,000 of assessed value. A legal suite adds $454.00 for water and $821.71 for sewer over the year, $1,275.71 together, and $172.04 for garbage. A house with no suite pays flat rates of $1,195 for water, $1,661 for sewer and $344.08 for waste.',
    faqs=[('How big can a suite be in Surrey?', 'Up to 40% of the principal unit’s habitable floor area, with one suite for each single-family, semi-detached or duplex unit. It can’t be inside a coach house or garden suite.'),
          ('Does a legal suite change a Surrey utility bill?', 'Yes. In 2026 a legal secondary suite adds $454.00 for water, $821.71 for sewer and $172.04 for garbage. A house without one pays flat rates of $1,195 for water and $1,661 for sewer.')])
SUITE['cloverdale'].update(
    rules=['Cloverdale sits inside the City of Surrey, so Surrey’s Zoning Bylaw No. 12000 decides what a suite can be: one per single-family, semi-detached or duplex unit, using no more than 40% of the principal unit’s habitable area.',
           'Clayton’s small lots bring the coach house question up often, and the rule is that a suite must be in the main house, not inside a coach house or garden suite.',
           'On farmland the Agricultural Land Commission’s rules sit on top of the City’s. For a parcel in the Reserve, a secondary suite is allowed only inside the principal residence, so a suite described as a separate building on acreage deserves a closer look.'],
    faqs=[('Can a Cloverdale farm have a suite in a separate building?', 'On Reserve land the Commission allows a secondary suite only inside the principal residence. A separate building counts as an additional residence, which has its own conditions.'),
          ('Is a Clayton house with a suite the same as one in Cloverdale town?', 'The suite rules are the same because both are in the City of Surrey. The lots are not: Clayton’s are small and newer, and Cloverdale town has older, larger ones.')])
SUITE['south-surrey'].update(
    rules=['South Surrey follows the City of Surrey’s Bylaw No. 12000: one suite for each single-family, semi-detached or duplex dwelling, with its habitable area held to 40% of the principal unit.',
           'White Rock, next door, writes its own rules and is outside these figures. Its Zoning Bylaw 2024, No. 2506 lets a one-unit residential lot have no more than one of several accessory uses, and a registered secondary suite is on that list beside boarding and a bed and breakfast.',
           'Some South Surrey lots are large enough for the multi-unit rules to matter. An eligible lot of 281 square metres or more within 400 metres of a frequent bus stop can hold up to 6 units, which changes how a suite house on one is priced.'],
    faqs=[('Can a White Rock lot have a suite and a bed and breakfast?', 'Not under the rule as the City writes it. Bylaw 2506 permits no more than one of the listed accessory uses with a one-unit residential use, and both are on the list.'),
          ('Does Surrey’s 40% suite limit apply to South Surrey?', 'Yes, because South Surrey is part of the City of Surrey. It does not apply in White Rock.')])
SUITE['langley'].update(
    rules=['“Langley” is two municipalities with different suite rules. The City of Langley’s Bylaw No. 3300 limits a secondary suite to the lesser of 100 square metres and 40% of the building’s gross floor area, wants the owner living on the lot and one extra off-street parking space, and requires an inspection, a building permit and an entry in the City’s secondary suites registry.',
           'The Township of Langley’s Zoning Bylaw No. 2500, section 102, caps a suite at 120 square metres of gross floor area and allows one for each principal dwelling unit, with a building permit for every suite. Willoughby listings often call a suite legal, so ask for the permit rather than relying on the word.',
           'Zoning Bylaw 6020, adopted November 18, 2024, brought small-scale multi-unit housing to the Township, with 3 to 4 units on eligible lots and no 6-unit tier. The Township estimated about 55% of its single-family and duplex lots, roughly 15,000 properties, would qualify.'],
    faqs=[('Who must live on the lot with a suite in the City of Langley?', 'The registered owner. Bylaw No. 3300 also asks for one extra off-street parking space and records approved suites in the City’s registry.'),
          ('How large can a Township of Langley suite be?', 'Up to 120 square metres of gross floor area, with one suite allowed for each principal dwelling unit and a building permit required for every suite.')])
SUITE['abbotsford'].update(
    rules=['Abbotsford’s Zoning Bylaw No. 2400-2014, section 140.3.8, allows one secondary suite in every single detached dwelling. A suite has to be under 50% of the principal unit’s size, a rule that replaced an older 100 square metre cap.',
           'Council reports describe the lot tests a suite must meet: at least 400 square metres of lot, at least 12.0 metres of frontage, a Collector or Local road, and not a cul-de-sac bulb. A listing can call a suite legal on a lot that fails one of these, so check the lot with the City as well as the house.',
           'A coach house or garden suite is a separate rule. Abbotsford lets one cover up to 15% of the lot, to a maximum of 100 square metres, and that figure belongs to Abbotsford alone. The City adopted its small-scale multi-unit changes in June 2024.'],
    faqs=[('What size can an Abbotsford secondary suite be?', 'Less than 50% of the principal unit. That replaced a 100 square metre cap, and one suite is allowed in each single detached dwelling.'),
          ('What lot tests does an Abbotsford suite have to meet?', 'Council reports describe a lot of at least 400 square metres, frontage of at least 12.0 metres, a Collector or Local road, and a lot that is not on a cul-de-sac bulb.')])
SUITE['burnaby'].update(
    rules=['Burnaby moved almost every house lot into its R1 Small-Scale Multi-Unit Housing District on July 1, 2024. A lot of 280 square metres (3,014 square feet) or less can take 3 units, a larger one 4, and 5 to 6 units only in a Frequent Transit Neighbourhood Area.',
           'Each primary unit gets one secondary suite, the suite counts toward the lot’s unit total, and it stays on the same title as the house. The new Zoning Bylaw 2026 was adopted June 9, 2026 and took effect July 1, 2026.',
           'Slopes and creeks shape Burnaby building. A lot beside a creek falls under the Streamside Protection and Enhancement Development Permit Area, and the City’s checklist effective August 1, 2026 asks for a geotechnical report on sloped sites, so ask what engineering stands behind a suite on a hillside.'],
    costs='For 2026 Burnaby charges $1.72223 per $1,000 of assessed value, with a Metro Vancouver rate of $0.05440 added. A detached house pays $652.33 for water and $159 for the default garbage toter. Renting out a suite adds $326.17 for water and $403.00 for sewer. The city is inside the Speculation and Vacancy Tax area.',
    faqs=[('Does a suite count toward the number of units on a Burnaby lot?', 'Yes. Under the R1 district a secondary suite counts toward the lot’s unit total, and each primary unit may have one.'),
          ('What does renting a suite add to a Burnaby utility bill?', 'In 2026 it adds $326.17 for water and $403.00 for sewer, on top of the $652.33 water charge for a detached house.')])
SUITE['coquitlam'].update(
    rules=['Coquitlam’s zoning bylaw is No. 3000, and Council adopted its small-scale multi-unit changes on June 9, 2025. A lot of 280 square metres or less can have up to 3 units, and one over 280 and under 4,050 square metres up to 4. There is no 6-unit tier, because the City says no Coquitlam bus stop meets the provincial frequent-service test.',
           'Low-density lots sit mostly in R-1, R-2, R-3 or R-4, and each zone sets a minimum lot size for added units, from 465 square metres in R-2 to 930 square metres in R-4. A suite is one of the forms allowed, next to carriage houses, laneway homes, garden cottages, duplexes, triplexes and fourplexes.',
           'A lot that is not connected to municipal water or sewer falls outside the small-scale rules. If there is a creek on or beside the lot, a steep slope, or a house built before 1945, speak to the City’s Development Services before you plan around a suite.'],
    costs='Coquitlam’s 2026 municipal residential rate is $2.2756 per $1,000 of assessed value, or $3.8520 together with the other taxing authorities. Taxes were due July 2, 2026, and the city is inside the Speculation and Vacancy Tax area.',
    faqs=[('How many units can a Coquitlam lot hold?', 'Up to 3 on a lot of 280 square metres or less and up to 4 on a lot over 280 and under 4,050 square metres. There is no 6-unit tier in Coquitlam.'),
          ('What is Coquitlam’s 2026 property tax rate?', '$2.2756 per $1,000 of assessed value for the municipality, and $3.8520 per $1,000 with the other taxing authorities included.')])
SUITE['richmond'].update(
    rules=['Richmond’s Zoning Bylaw No. 8500 lists a secondary suite as a secondary use in the single detached zones RS1 and RS2. Section 5.4 sets the size window: at least 33.0 square metres, and at most the lesser of 40% of the dwelling’s floor area or 110 square metres.',
           'The City says it allows at least one secondary suite or accessory dwelling unit on each lot, and the provincial minimums for small-scale multi-unit housing apply: 3 units on a lot of 280 square metres or less, and 4 on a larger one.',
           'Richmond sits behind 49 kilometres of dikes, and Richmond Fire-Rescue notes that pockets of liquefaction are possible in a significant earthquake. For a below-grade suite, ask for its permit and age and whether the lot has had water problems.'],
    faqs=[('How big can a suite be in Richmond?', 'At least 33.0 square metres and no more than the lesser of 40% of the dwelling’s floor area or 110 square metres, under section 5.4 of Zoning Bylaw No. 8500.'),
          ('Which Richmond zones list a secondary suite?', 'RS1 and RS2, the single detached zones, list a secondary suite as a secondary use.')])
SUITE['vancouver'].update(
    rules=['Vancouver replaced nine RS zones with one R1-1 zone on October 17, 2023, covering about 65,000 lots. On an R1-1 lot an owner can have a house with a suite or a laneway house, a duplex, a character-retention project, or a multiplex of 3 to 6 strata units or up to 8 rental units.',
           'Minimum site area under the schedule is 306 square metres for a house, a duplex or a 3 to 4 unit multiple dwelling, 464 square metres for 5 units, and 557 square metres for 6 to 8 units. A lot that clears those can carry a multiplex as well as a suite and a laneway house in the forms the schedule states.',
           'The Empty Homes Tax charges 3% of assessed value on a home that is neither lived in nor rented, and the Tenant Relocation and Protection Policy applies across the city when a rented building is redeveloped. A rented suite touches both.'],
    faqs=[('What lot size does a Vancouver multiplex need?', 'R1-1 sets the minimum site area at 306 square metres for a house, duplex or 3 to 4 unit multiple dwelling, 464 square metres for 5 units, and 557 square metres for 6 to 8 units.'),
          ('When did Vancouver switch to the R1-1 zone?', 'On October 17, 2023, when it replaced nine RS zones with one for about 65,000 lots.')])
SUITE['north-delta'].update(
    rules=['Delta adopted its small-scale multi-unit housing zoning on June 24, 2024, through Bylaws 8394 and 8395. Where the zoning applies, it allows combinations of single detached dwellings, duplexes, secondary suites, coach houses and garden suites.',
           'Delta’s published guidance permits registered secondary suites and detached garden suites or coach houses on qualifying lots, subject to floodplain, coverage and parking rules. What applies to one lot depends on its zone, so confirm it with the Corporation of Delta before you price a suite as a feature.',
           'Surrey borders North Delta, but its suite limits do not carry across the line. A listing that quotes a Surrey percentage for a Delta house is quoting the wrong city.'],
    faqs=[('When did Delta adopt its small-scale housing rules?', 'On June 24, 2024, through Bylaws 8394 and 8395.'),
          ('Can a North Delta lot have a suite and a coach house?', 'Delta’s 2024 rules allow combinations of secondary suites, coach houses and garden suites where the zoning applies, within floodplain, coverage and parking limits. The answer depends on the lot’s zone.')])
SUITE['maple-ridge'].update(
    rules=['Maple Ridge permits one secondary suite per lot in the zones the City lists, A-1, A-2 and A-3 among them. The suite must be inside the single detached building, may take up to 40% of the gross floor area, and is not permitted in the Floodplain Area.',
           'On parcels in the Agricultural Land Reserve, the Agricultural Land Commission’s rules apply as well. They allow one secondary suite in the principal residence and an additional residence only when the Commission’s conditions are met.',
           'A suite in a separate building on acreage is not a secondary suite under these rules, so ask what the listing is describing and which zone the parcel is in.'],
    faqs=[('How big can a Maple Ridge suite be?', 'Up to 40% of the gross floor area, one per lot, inside the single detached building, and not in the Floodplain Area, in the zones the City lists.'),
          ('What applies to a Maple Ridge suite on Reserve land?', 'The Commission’s rules allow one secondary suite in the principal residence, and an additional residence only if its conditions are met.')])
SUITE['chilliwack'].update(
    rules=['Chilliwack allows one accessory dwelling unit on each lot where the zone permits, and that unit can be a secondary suite, a coach house or a garden suite. A legal suite therefore rules out a coach house on the same lot.',
           'A suite has to be under both 90 square metres and 40% of the building’s habitable floor space, inside a building with one principal dwelling unit. Because both limits apply, a small house can reach the 40% ceiling long before 90 square metres. Garden suites go up to 100 square metres.',
           'Under the Secondary Suites Policy a suite can be rented in any single detached dwelling regardless of zone, provided it has a building permit, meets the BC Building and Fire Code and current flood protection rules, and does not sit below the flood construction level. Bylaw 5395, adopted June 18, 2024, allows 3 to 4 units inside the urban growth boundary.'],
    faqs=[('Can a Chilliwack lot have a suite and a coach house?', 'No. The City allows one accessory dwelling unit per lot, so a legal suite leaves no room for a coach house or garden suite on the same lot.'),
          ('How is a Chilliwack suite measured?', 'It has to be under both 90 square metres and 40% of the building’s habitable floor space, inside a building with a single principal dwelling unit.')])

SIZE = {  # (limit text, sq ft cap fraction/area) used to turn the suite size rule into a number for the median house
 'surrey': ('40% of the principal unit’s habitable area', 0.40), 'cloverdale': ('40% of the principal unit’s habitable area', 0.40), 'south-surrey': ('40% of the principal unit’s habitable area', 0.40),
 'langley': ('the City’s lesser of 100 square metres (1,076 square feet) and 40%, or the Township’s 120 square metres (1,292 square feet)', None),
 'abbotsford': ('50% of the principal unit', 0.50), 'burnaby': None, 'coquitlam': None,
 'richmond': ('the lesser of 40% of the dwelling and 110 square metres (1,184 square feet)', 0.40), 'vancouver': None, 'north-delta': None,
 'maple-ridge': ('40% of the gross floor area', 0.40), 'chilliwack': ('the lesser of 40% of the habitable space and 90 square metres (969 square feet)', 0.40)}

# ---------------------------------------------------------------------------- helpers
def fit(*variants):
    for v in variants:
        if 135 <= len(v) <= 158: return v
    raise AssertionError((len(variants[-1]), variants[-1]))

def cv(e, k, fmt=str):
    v = e.get(k) if e else None
    return '—' if v in (None, '') else fmt(v)
def pc(x): return f'{x}%'
def exists(s): return N.exists(s)
def band_tbl(cap, edges, cols, src=SRC):
    labs = edges; rows = []
    for j, lab in enumerate(labs):
        vals = [(c.get('bands') or [None] * len(labs))[j] if c and c.get('bands') else None for c in cols[1]]
        if any(vals): rows.append([lab] + [str(v) if v is not None else '—' for v in vals])
    return tbl(cap, ['Price range'] + cols[0], rows, src)
def quarter_tbl(cap, e, noun):
    q = e.get('q') or []
    rows = [[QL[i], num(x['n']), money(x['price']) if x['price'] else '—'] for i, x in enumerate(q)]
    return tbl(cap, ['Period', noun, 'Median price'], rows, SRC)
def sub_rows(ck, g, minn=3):
    out = []
    for k, v in EX['sub'].items():
        c, rest = k.split('#', 1)
        if c != ck or g not in v or v[g]['n'] < minn: continue
        area, name = rest.split('|', 1)
        out.append((area, name, v))
    out.sort(key=lambda r: -r[2][g]['n'])
    return out
def link_for(hub, area, name, snapcity):
    h = hubmap(hub).get(nz(disp(name, area)))
    if not h and snapcity: h = N.snaplink(snapcity, name)
    return h
def cellname(area, name, href):
    d = disp(name, area); return {'t': d, 'h': href} if href else d


def suite_page(ck):
    c = SUITE[ck]; nm = c['name']; X = EX['city'][c['ex']]; g = X['groups']; ho, le, un = g['house'], g['legal'], g['unauth']
    assert le['n'] >= 30 and ho['n'] >= 100, ck
    slug = f'{ck}-houses-with-suites-for-sale'
    tot = le['n'] + un['n']; share = round(100 * tot / ho['n'])
    prem = round(100 * (le['price'] - ho['price']) / ho['price'])
    sr = sub_rows(c['ex'], 'legal', 3)
    top = [disp(n, a) for a, n, v in sr[:3]]
    big = sorted([(v['house']['n'], disp(n, a)) for k, v in EX['sub'].items() if k.split('#')[0] == c['ex'] and 'house' in v for a, n in [k.split('#', 1)[1].split('|', 1)]], reverse=True)[:5]
    seo = dict(title=f'{nm} Houses with Suites for Sale | Prices and Rules', h1=f'Houses with Suites for Sale in {nm}', crumb='Houses with suites',
               description=fit(f'Search {nm} houses with a suite. {le["n"]} homes with a legal suite sold over the past ten months at a median of {money(le["price"])}, with suite rules and area prices.',
                               f'Search {nm} houses with a suite. {le["n"]} with a legal suite sold over the past ten months at a median of {money(le["price"])}, plus suite rules and prices.',
                               f'Search {nm} houses with a suite. {le["n"]} with a legal suite sold over the past ten months at a median of {money(le["price"])}, plus suite rules.',
                               f'Houses with a suite for sale in {nm}. {le["n"]} with a legal suite sold over ten months at a median of {money(le["price"])}, plus suite rules and prices.',
                               f'{nm} houses with a legal suite sold at a median of {money(le["price"])} over ten months ({le["n"]} sales). Search them, with suite rules and area prices.'),
               links_h=f'More {nm} houses and suite searches')
    dword = 'more' if prem >= 0 else 'less'
    hp = [(b, hpi(src, b, 'detached')) for src, b in c['hpi']]
    bl = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures come from Paragon closed sales to August 31, 2026, because the export is incomplete after that. The live search is not connected yet.', 'gen': G},
          P(f'This search lists detached houses for sale in {c["area"]} that have a suite, legal or marked unauthorized. The busiest areas by house sales were {big[0][1]} ({big[0][0]}), ' + (', '.join(f'{x[1]} ({x[0]})' for x in big[1:4]) + f' and {big[4][1]} ({big[4][0]})' if len(big) > 4 else ', '.join(f'{x[1]} ({x[0]})' for x in big[1:])) + '. Condos, townhomes and half duplexes are separate searches.'),
          P(f'Of {ho["n"]:,} detached houses that closed in {nm} between November 1 and August 31, {tot} ({share}%) had a suite: {le["n"]} legal and {un["n"]} unauthorized. '
            f'The legal-suite houses sold for a median of {money(le["price"])}, {abs(prem)}% {dword} than the {money(ho["price"])} median for every {nm} house.'),
          {'t': 'grid', 'gen': G},
          H(f'What {nm} houses with suites sold for')]
    rows = [['Sales', num(le['n']), num(un['n']), num(ho['n'])],
            ['Median price', cv(le, 'price', money), cv(un, 'price', money), cv(ho, 'price', money)]]
    if le.get('p25'): rows.append(['Middle half of prices', f'{money(le["p25"])} to {money(le["p75"])}', f'{money(un["p25"])} to {money(un["p75"])}' if un.get('p25') else '—', f'{money(ho["p25"])} to {money(ho["p75"])}'])
    rows += [['Price per square foot', cv(le, 'ppsf', money), cv(un, 'ppsf', money), cv(ho, 'ppsf', money)],
             ['Median floor area', cv(le, 'sqft', sqft), cv(un, 'sqft', sqft), cv(ho, 'sqft', sqft)],
             ['Median lot size', cv(le, 'lot_sqft', sqft), cv(un, 'lot_sqft', sqft), cv(ho, 'lot_sqft', sqft)],
             ['Median year built', cv(le, 'yb'), cv(un, 'yb'), cv(ho, 'yb')],
             ['Median bedrooms', cv(le, 'beds'), cv(un, 'beds'), cv(ho, 'beds')],
             ['Houses with two or more kitchens', cv(le, 'kitchens2', pc), cv(un, 'kitchens2', pc), cv(ho, 'kitchens2', pc)],
             ['Days to sell', cv(le, 'dom'), cv(un, 'dom'), cv(ho, 'dom')],
             ['Sold price as a share of list price', cv(le, 'ratio', pc), cv(un, 'ratio', pc), cv(ho, 'ratio', pc)],
             ['Sales over the list price', cv(le, 'over', pc), cv(un, 'over', pc), cv(ho, 'over', pc)]]
    rows = [r for r in rows if any(x != '—' for x in r[1:])]
    bl.append(tbl(f'{nm} detached houses sold, by suite', ['Measure', 'Legal suite', 'Unauthorized suite', 'All detached houses'], rows, SRC + ' ' + SUITE_NOTE))
    sen = []
    if le.get('lot_sqft') and ho.get('lot_sqft'): sen.append(f'The typical legal-suite house sits on {sqft(le["lot_sqft"])}, against {sqft(ho["lot_sqft"])} for all {nm} houses.')
    if le.get('sqft') and ho.get('sqft'): sen.append(f'It has {le["sqft"]:,} square feet of floor area, against {ho["sqft"]:,}.')
    if le.get('kitchens2') is not None and ho.get('kitchens2') is not None: sen.append(f'{le["kitchens2"]}% of legal-suite houses have two or more kitchens, compared with {ho["kitchens2"]}% of all houses.')
    if le.get('sqft') and un.get('sqft'): sen.append(f'Unauthorized-suite houses were smaller at {un["sqft"]:,} square feet and a median {money(un["price"])}.' if un['sqft'] < le['sqft'] and un.get('price') else f'Unauthorized-suite houses had {un["sqft"]:,} square feet.')
    if sen: bl.append(P(' '.join(sen)))
    la, co_, se = g['lane'], g['coach'], g['second']
    ex = []
    if la['n'] >= 5: ex.append(f'{la["n"]} {nm} houses had lane access, at a median of {money(la["price"])}')
    if co_['n'] >= 3: ex.append(f'{co_["n"]} were marked as a coach or laneway house' + (f' at {money(co_["price"])}' if co_.get('price') else ''))
    if se['n'] >= 3: ex.append(f'{se["n"]} had a second residence on the lot')
    if ex: bl.append(P('Alongside suites, ' + '; '.join(ex) + '. These are separate flags in the same Paragon records, and a house can carry more than one.'))
    if le.get('q'): bl.append(quarter_tbl(f'{nm} houses with a legal suite, by period', le, 'Sales'))
    if le.get('bands'): bl.append(band_tbl(f'{nm} houses with a suite, by price range', BANDS_H, (['Legal suite', 'Unauthorized suite'], [le, un])))
    if le.get('bands'):
        top2 = sum(le['bands'][5:]); top1 = sum(le['bands'][3:])
        sh = [f'{round(100 * sum(le["bands"][3:]) / le["n"])}% of {nm} legal-suite houses sold for $1,000,000 or more']
        if top2: sh.append(f'{round(100 * sum(le["bands"][5:]) / le["n"])}% for $1,500,000 or more')
        ush = f', against {round(100 * sum(un["bands"][3:]) / un["n"])}% of unauthorized-suite houses at $1,000,000 or more' if un.get('bands') else ''
        tr = ''
        q = le.get('q') or []
        if len(q) >= 3 and q[0].get('price') and q[2].get('price'): tr = f' The legal-suite median moved from {money(q[0]["price"])} in the first period to {money(q[2]["price"])} in May to July.'
        bl.append(P(', and '.join(sh) + ush + '.' + tr))
    r5 = [r for r in sr if r[2]['legal']['n'] >= 5][:14]
    if len(r5) < 3: r5 = sr[:10]
    if len(r5) >= 3:
        rr = []
        for a, n, v in r5:
            h = v.get('house', {}); l = v['legal']
            href = link_for(c['hub'], a, n, c['snap'])
            rr.append([cellname(a, n, href), num(h.get('n', 0)), num(l['n']), f'{round(100 * l["n"] / h["n"])}%' if h.get('n') else '—', cv(l, 'price', money), cv(h, 'price', money)])
        bl += [H(f'{nm} neighbourhoods with the most legal suites'),
               P(f'{top[0]} had the most legal-suite sales ({r5[0][2]["legal"]["n"]})' + (f', then {top[1]} ({r5[1][2]["legal"]["n"]})' if len(top) > 1 else '') + (f' and {top[2]} ({r5[2][2]["legal"]["n"]})' if len(top) > 2 else '') + '. Where a median price is missing, fewer than 5 legal-suite houses sold.'),
               tbl(f'{nm} detached houses with a legal suite, by neighbourhood', ['Neighbourhood', 'House sales', 'Legal suite sales', 'Share with a legal suite', 'Median price with a legal suite', 'Median price, all houses'], rr,
                   SRC + ' A neighbourhood is listed here with 3 or more legal-suite sales.')]
    bl.append(H(f'{nm} suite rules'))
    bl += [P(t) for t in c['rules']]
    if hp:
        e = hp[0][1]
        bl.append(P(f'The MLS® Home Price Index benchmark for a detached house in {hp[0][0]} was {money(e["benchmark"])} in September 2026, {abs(e["chg_1y"]):.1f}% {"down" if e["chg_1y"] < 0 else "up"} over twelve months.' + (f' In {hp[1][0]} it was {money(hp[1][1]["benchmark"])}.' if len(hp) > 1 else '') + ' The benchmark is the price of a typical house, not a median of sales.'))
    if c['costs']: bl += [H(f'Costs of a {nm} house with a suite'), P(c['costs'])]
    sz = SIZE.get(ck)
    if sz and sz[1] and le.get('sqft'):
        sizeb = f'Measure the suite against the limit of {sz[0]}. On the median {nm} legal-suite house of {le["sqft"]:,} square feet, {int(sz[1] * 100)}% comes to about {round(le["sqft"] * sz[1], -1):,.0f} square feet.'
    elif sz:
        sizeb = f'Measure the suite against the limit of {sz[0]}, and ask for the floor plan that was approved with the permit.'
    else:
        sizeb = {'burnaby': 'Count the units. Burnaby gives each primary unit one suite and counts it toward the lot’s total of 3 or 4, so check how many units the lot already carries.',
                 'coquitlam': 'Count the units. Coquitlam allows up to 3 on a lot of 280 square metres or less and up to 4 on a larger one, and each zone sets its own minimum lot size for added units.',
                 'vancouver': 'Check the lot against the R1-1 schedule. A house with a suite or a laneway house needs less than a multiplex, and a multiplex needs 306 to 557 square metres depending on the number of units.',
                 'north-delta': 'Ask which Delta zone the lot is in. The 2024 rules allow suites, coach houses and garden suites in combinations that depend on the zone, the floodplain, coverage and parking.'}[ck]
    ub = [f'Ask for the {nm} permit and final inspection for the suite. {un["n"]} of the {tot} suite houses sold here were unauthorized, so the paperwork comes first.',
          c['ask'], sizeb,
          f'If a tenant lives in the suite, ask for the tenancy agreement and the rent; a tenancy usually carries on after a sale. Legal-suite houses took {le["dom"]} days to sell, so there is time to ask.',
          (f'If the listing says unauthorized, compare the price with the {money(un["price"])} median for unauthorized-suite houses and the {money(le["price"])} median for legal ones, then decide whether to legalize the suite or remove it.' if un.get('price') else 'If the listing says unauthorized, decide whether you would legalize the suite or remove it, and price the house on that basis.')]
    bl += [H(f'Before you offer on a {nm} house with a suite'), L(ub),
           {'t': 'h', 'level': 2, 'text': f'Estimate the payment on a {nm} house with a suite', 'gen': G}, P(f'The calculator starts at the {nm} legal-suite median of {money(le["price"])}.'),
           {'t': 'calc', 'which': 'mortgage', 'price': le['price'], 'gen': G}]
    nbq = []
    if len(top) >= 3: nbq = [(f'Which {nm} neighbourhoods have the most houses with legal suites?', f'{top[0]} had {r5[0][2]["legal"]["n"]} legal-suite sales, {top[1]} {r5[1][2]["legal"]["n"]} and {top[2]} {r5[2][2]["legal"]["n"]} between November 1, 2025 and August 31, 2026.')]
    faq = [(f'How much does a {nm} house with a suite cost?', f'The {le["n"]} houses with a legal suite that closed between November 1, 2025 and August 31, 2026 had a median of {money(le["price"])}' + (f', with the middle half between {money(le["p25"])} and {money(le["p75"])}' if le.get('p25') else '') + f'. Every {nm} detached house had a median of {money(ho["price"])}.'),
           (f'What is the difference between a legal and an unauthorized suite in {nm}?', f'A legal suite is listed as Legal Suite or Licensed Suite, and an unauthorized one as Unauthorized Suite. {le["n"]} {nm} houses sold with a legal suite and {un["n"]} with an unauthorized one' + (f', which had a median of {money(un["price"])}' if un.get('price') else '') + '.'),
           ] + c['faqs'] + nbq + [
           (f'How fast do {nm} houses with a legal suite sell?', f'{le["dom"]} days at a median' + (f', closing at {le["ratio"]}% of list' if le.get('ratio') else '') + (f', with {le["over"]}% over the list price.' if le.get('over') is not None else '.'))]
    crumb = next(((l, x) for l, x in ((f'{nm} houses', f'{ck}-houses-for-sale'), (f'{nm} homes', f'{ck}-homes-for-sale')) if exists(x)))
    return N.finish(slug, seo, [crumb], faq, bl, f'{nm} houses with suites: your questions answered', c['links'], dict(search_page=dict(kind='suite', city=ck))), c


def pent_blocks(ck, existing=False):
    c = PENT.get(ck) or PENT_EXIST[ck]; nm = c['name']; X = EX['city'][c['ex']]; g = X['groups']
    if c.get('ex2'):  # south surrey + white rock: merge by re-reading both
        pass
    pe, co = g['pent'], g['condo']
    prem = round(100 * (pe['price'] - co['price']) / co['price'])
    sr = sub_rows(c['ex'], 'pent', 3)
    bl = []
    bl.append(H(f'{nm} penthouses: what sold') if existing else H(f'What {nm} penthouses sold for'))
    rows = [['Sales', num(pe['n']), num(co['n'])], ['Median price', cv(pe, 'price', money), cv(co, 'price', money)]]
    if pe.get('p25'): rows.append(['Middle half of prices', f'{money(pe["p25"])} to {money(pe["p75"])}', f'{money(co["p25"])} to {money(co["p75"])}' if co.get('p25') else '—'])
    rows += [['Price per square foot', cv(pe, 'ppsf', money), cv(co, 'ppsf', money)], ['Median floor area', cv(pe, 'sqft', sqft), cv(co, 'sqft', sqft)],
             ['Median bedrooms', cv(pe, 'beds'), cv(co, 'beds')], ['Median year built', cv(pe, 'yb'), cv(co, 'yb')], ['Strata fee a month', cv(pe, 'maint', money), cv(co, 'maint', money)],
             ['Days to sell', cv(pe, 'dom'), cv(co, 'dom')], ['Sold price as a share of list price', cv(pe, 'ratio', pc), cv(co, 'ratio', pc)], ['Sales over the list price', cv(pe, 'over', pc), cv(co, 'over', pc)]]
    rows = [r for r in rows if any(x != '—' for x in r[1:])]
    bl.append(tbl(f'{nm} condos sold, penthouses and all condos', ['Measure', 'Penthouses', 'All condos'], rows, SRC + ' A penthouse here is a condo whose Paragon style field includes Penthouse.'))
    bits = []
    if pe.get('ppsf') and co.get('ppsf'):
        pp = round(100 * (pe['ppsf'] - co['ppsf']) / co['ppsf']); bits.append(f'Per square foot a penthouse cost {money(pe["ppsf"])}, which is {abs(pp)}% {"more" if pp >= 0 else "less"} than the {money(co["ppsf"])} for condos as a whole')
    if pe.get('sqft') and co.get('sqft'): bits.append(f'The typical penthouse was {pe["sqft"]:,} square feet, against {co["sqft"]:,} for all condos')
    if pe.get('maint') and co.get('maint'): bits.append(f'its strata fee ran {money(pe["maint"])} a month against {money(co["maint"])}')
    if bits:
        tail = ' The penthouses were larger, so part of the price gap is size.' if pe.get('sqft') and co.get('sqft') and pe['sqft'] > co['sqft'] * 1.05 else ''
        bl.append(P('. '.join(bits[:2]) + ('; ' + bits[2] if len(bits) > 2 else '') + '.' + tail))
    if pe.get('q'): bl.append(quarter_tbl(f'{nm} penthouses sold, by period', pe, 'Sales'))
    if pe.get('bands'): bl.append(band_tbl(f'{nm} penthouses sold, by price range', BANDS_C, (['Penthouses', 'All condos'], [pe, co])))
    if len(sr) >= 3:
        rr = []
        for a, n, v in sr[:12]:
            p = v['pent']; k = v.get('condo', {})
            href = link_for(c['hub'], a, n, None)
            rr.append([cellname(a, n, href), num(p['n']), cv(p, 'price', money), cv(p, 'ppsf', money), cv(p, 'maint', money), cv(k, 'price', money)])
        bl += [H(f'{nm} neighbourhoods with penthouse sales'),
               P(f'{disp(sr[0][1], sr[0][0])} had the most penthouse sales' + (f', then {disp(sr[1][1], sr[1][0])}' if len(sr) > 1 else '') + (f' and {disp(sr[2][1], sr[2][0])}' if len(sr) > 2 else '') + '. Where a median price is missing, fewer than 5 penthouses sold.'),
               tbl(f'{nm} penthouses sold, by neighbourhood', ['Neighbourhood', 'Penthouse sales', 'Median price', 'Price per sq ft', 'Strata fee a month', 'Median price, all condos'], rr, SRC + ' A neighbourhood is listed here with 3 or more penthouse sales.')]
    bd = [b for b in X.get('pent_buildings', []) if b['n'] >= 3][:10]
    if len(bd) >= 3:
        br = [[b['name'], disp(b['sub']), num(b['n']), money(b['price']) if b.get('price') else '—', str(b['yb']) if b.get('yb') else '—', money(b['maint']) if b.get('maint') else '—'] for b in bd]
        bl += [H(f'{nm} buildings with the most penthouse sales'),
               tbl(f'{nm} buildings with 3 or more penthouse sales', ['Building', 'Neighbourhood', 'Penthouse sales', 'Median price', 'Year built', 'Strata fee a month'], br, SRC + ' A building is named here with 3 or more penthouse sales and priced with 5 or more.')]
    if c['hpi']:
        hp = [(b, hpi(src, b, 'apartment')) for src, b in c['hpi']]; e = hp[0][1]
        bl.append(P(f'The MLS® Home Price Index benchmark for an apartment in {hp[0][0]} was {money(e["benchmark"])} in September 2026, {abs(e["chg_1y"]):.1f}% {"down" if e["chg_1y"] < 0 else "up"} over twelve months.' + (f' In {hp[1][0]} it was {money(hp[1][1]["benchmark"])}.' if len(hp) > 1 else '') + ' The benchmark is the price of a typical apartment, not a median of sales.'))
    if pe.get('bands') and co.get('bands'):
        k = 3 if len(pe['bands']) == 6 else 3
        pm = round(100 * sum(pe['bands'][k:]) / pe['n']); cm = round(100 * sum(co['bands'][k:]) / co['n'])
        bl.append(P(f'{pm}% of {nm} penthouses sold for $1,000,000 or more, compared with {cm}% of all condos in the same months.'))
    bd0 = [b for b in X.get('pent_buildings', []) if b['n'] >= 5]
    if bd0:
        b0 = bd0[0]
        bl.append(P(f'{b0["name"]} had the most penthouse sales of any building, with {b0["n"]}' + (f' at a median of {money(b0["price"])}' if b0.get('price') else '') + (f', and it was built in {b0["yb"]}' if b0.get('yb') else '') + '.'))
    return bl, pe, co, prem, sr


def pent_page(ck):
    c = PENT[ck]; nm = c['name']; X = EX['city'][c['ex']]; pe = X['groups']['pent']; co = X['groups']['condo']
    assert pe['n'] >= 30, ck
    slug = f'{ck}-penthouses-for-sale'
    blocks, pe, co, prem, sr = pent_blocks(ck)
    dword = 'more' if prem >= 0 else 'less'
    seo = dict(title=f'{nm} Penthouses for Sale | Prices and Buildings', h1=f'Penthouses for Sale in {nm}', crumb='Penthouses',
               description=fit(f'Search {nm} penthouses for sale. {pe["n"]} sold over the past ten months at a median of {money(pe["price"])}, with prices by neighbourhood and the buildings that sell most.',
                               f'Search {nm} penthouses for sale. {pe["n"]} sold over the past ten months at a median of {money(pe["price"])}, with prices by neighbourhood and building.',
                               f'{nm} penthouses for sale. {pe["n"]} sold over the past ten months at a median of {money(pe["price"])}, with prices by neighbourhood and building.',
                               f'Search {nm} penthouses for sale. {pe["n"]} sold over the past ten months at a median of {money(pe["price"])}, plus prices by area and top buildings.'),
               links_h=f'More {nm} condo and home searches')
    intro = [{'t': 'notice', 'text': 'Draft for Jared’s approval. Sold figures come from Paragon closed sales to August 31, 2026, because the export is incomplete after that. The live search is not connected yet.', 'gen': G},
             P(f'This search lists penthouses for sale in {c["area"]}: top-floor condos that the listing marks as a penthouse. It covers {c["desc"]}. Other condos, townhomes and houses are separate searches.'),
             P(f'{pe["n"]} {nm} penthouses closed from {EXW}, out of {co["n"]:,} condo sales in the same area and months. The median penthouse sold for {money(pe["price"])}, {abs(prem)}% {dword} than the {money(co["price"])} median for all condos' + (f', in {pe["dom"]} days at a median.' if pe.get('dom') else '.')),
             {'t': 'grid', 'gen': G}]
    mid = [H(f'About buying a top-floor home in {nm}')] + [P(t) for t in c['facts']]
    yb_t = f'The median {nm} penthouse sold was built in {pe["yb"]}' if pe.get('yb') else f'Check the year the {nm} building was built'
    vi = list(PENT).index(ck)
    R = ['Ask when the building last replaced its roof, and read the depreciation report for the cost of the next one.', 'Find out the roof’s age from the strata minutes. A depreciation report shows when a replacement is expected and how it will be paid for.',
         'Request the depreciation report and look at the roof line first, because a top-floor owner shares that bill before anyone else sees the effects.', 'Check the strata’s contingency reserve fund against the roof’s age. The depreciation report is where the next replacement is costed.',
         'The roof is the first big shared expense for a top floor, so ask when it was done and read what the depreciation report says comes next.', 'Before you offer, read the last two years of strata minutes for roof repairs, and ask whether a replacement is scheduled.']
    W = ['Ask about water-ingress claims and envelope repairs from the past ten years, and what the strata’s insurance deductible is.', 'Look for building-envelope work in the minutes, and ask whether any water-damage claim has been filed against the strata’s policy.',
         'Ask whether the building has had leaks through the roof or windows, and what deductible the strata’s insurance carries.', 'Check the Form B information certificate for claims, special levies and the insurance deductible before you remove subjects.',
         'A top-floor unit is the first to show a roof leak, so ask for the claims history and the insurance deductible in writing.', 'Ask the strata for any envelope-repair history, and how the insurance deductible would be split if a leak started above you.']
    D = ['Confirm whether a roof deck or terrace is part of your strata lot, limited common property or common property, since that decides who may build, repair and use it.', 'Ask how the terrace is classed under the strata plan. An owned lot and limited common property carry different repair duties.',
         'If the home comes with outdoor space on the roof, check the strata plan to see whether it is yours, limited common property, or common.', 'Find out who pays to repair the terrace membrane. The answer follows from whether the space is owned, limited common property or common property.',
         'Read the strata bylaws on roof access, barbecues and furniture. They differ from building to building and often limit what a terrace owner can do.', 'Get the strata plan and confirm the status of any roof space: owned, limited common property or common property.']
    Hh = ['Visit at different hours. Mechanical rooms and elevator machinery above a top floor can be loud, and afternoon sun heats some suites.', 'Ask about air conditioning rules. Many top floors run warm in summer, and strata bylaws may limit where a unit can go.',
          'Stand in the unit on a hot afternoon. A top floor with a south or west exposure can run warm, and some stratas restrict air conditioners.', 'Ask what sits on the roof above the unit, such as rooftop equipment or an elevator housing, and listen for it at night.',
          f'Check the sun and the sound on a second visit. Penthouses here took {pe["dom"]} days to sell, so a return trip at another hour is realistic.', 'Ask what is directly above the unit and how the building handles summer heat on the top floor.']
    feeb = (f'Compare the building’s fee with the {money(pe["maint"])} a month median for {nm} penthouses and {money(co["maint"])} for all condos. A fee well above that deserves a look at what it covers.' if pe.get('maint') and co.get('maint') else 'Compare the building’s strata fee with others nearby, and ask what it covers.')
    chk = [R[vi], W[vi], D[vi], Hh[vi], feeb + (f' {yb_t}.' if pe.get('yb') else '')]
    mid += [H(f'Before you offer on a {nm} penthouse'), L(chk),
            {'t': 'h', 'level': 2, 'text': f'Estimate the payment on a {nm} penthouse', 'gen': G}, P(f'The calculator starts at the {nm} penthouse median of {money(pe["price"])}.'),
            {'t': 'calc', 'which': 'mortgage', 'price': pe['price'], 'gen': G}]
    nbh = f'{disp(sr[0][1], sr[0][0])} ({sr[0][2]["pent"]["n"]} sales)' if sr else None
    faq = [(f'How much does a penthouse cost in {nm}?', f'The {pe["n"]} penthouses that closed between November 1, 2025 and August 31, 2026 had a median of {money(pe["price"])}' + (f', with the middle half between {money(pe["p25"])} and {money(pe["p75"])}' if pe.get('p25') else '') + f'. All {nm} condos had a median of {money(co["price"])}.'),
           (f'How does a {nm} penthouse compare in price with other condos?', f'A penthouse cost {abs(prem)}% {dword} at the median' + (f', or {money(pe["ppsf"])} a square foot against {money(co["ppsf"])} for all condos' if pe.get('ppsf') and co.get('ppsf') else '') + '. Compare the floor area, the strata fee and the roof or terrace before you decide.'),
           (f'How fast do {nm} penthouses sell?', f'{pe["dom"]} days at a median' + (f', closing at {pe["ratio"]}% of list' if pe.get('ratio') else '') + (f', with {pe["over"]}% over the list price.' if pe.get('over') is not None else '.')),
           (f'What counts as a penthouse in {nm}?', f'{pe["n"]} of the {co["n"]:,} {nm} condo sales carried Penthouse in the style field' + (f', most of them in {nbh}' if nbh else '') + '. The listing agent enters that, so some top-floor homes are unmarked and a marked one is not always on the very top floor.'),
           (f'Do {nm} penthouses have higher strata fees?', (f'The median strata fee was {money(pe["maint"])} a month for penthouses and {money(co["maint"])} for all condos.' if pe.get('maint') and co.get('maint') else 'Fees depend on the building more than the floor, so compare the building’s fee against its neighbours.'))]
    seo_ = seo
    crumb = next(((l, x) for l, x in ((f'{nm} condos', f'{ck}-condos-for-sale'), (f'{nm} homes', f'{ck}-homes-for-sale')) if exists(x)))
    j = N.finish(slug, seo_, [crumb], faq, intro + blocks[:0] + blocks + mid, f'{nm} penthouses: your questions answered', c['links'], dict(search_page=dict(kind='penthouse', city=ck)))
    return j


# existing penthouse drafts: add sold figures
PENT_EXIST = {
 'langley': dict(name='Langley', ex='langley', area='Langley', hub='langley-neighbourhood-guides', hpi=[('fvreb', 'Langley')], hpi_src=SRC_FV, slug='langley-penthouses-for-sale'),
 'abbotsford': dict(name='Abbotsford', ex='abbotsford', area='Abbotsford', hub='abbotsford-neighbourhood-guides', hpi=[('fvreb', 'Abbotsford')], hpi_src=SRC_FV, slug='abbotsford-penthouses-for-sale'),
 'south-surrey-white-rock': dict(name='South Surrey and White Rock', ex='south-surrey-white-rock', area='South Surrey and White Rock', hub='south-surrey-neighbourhood-guides', hpi=[('fvreb', 'South Surrey & White Rock')], hpi_src=SRC_FV, slug='south-surrey-white-rock-penthouses-for-sale'),
}


def add_existing(ck):
    c = PENT_EXIST[ck]; f = f'src/data/local/{c["slug"]}.json'; j = json.load(open(f))
    blocks, pe, co, prem, sr = pent_blocks(ck, existing=True)
    dword = 'more' if prem >= 0 else 'less'
    intro = P(f'{pe["n"]} {c["name"]} penthouses closed from {EXW}, out of {co["n"]:,} condo sales in the same area and months. The median penthouse sold for {money(pe["price"])}, {abs(prem)}% {dword} than the {money(co["price"])} median for all condos.')
    new = [dict(b, pos='end') for b in [intro] + blocks]
    for b in new: b['gen'] = G
    j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]
    at = next((i for i, b in enumerate(j['blocks']) if b.get('pos') == 'end'), 0)
    j['blocks'] = j['blocks'][:at] + new + j['blocks'][at:]
    j['updated'] = N.UPDATED
    json.dump(j, open(f, 'w'), indent=1, ensure_ascii=False)


def main():
    made = []; cfg = {}
    N.NEW.update([f'{k}-houses-with-suites-for-sale' for k in SUITE] + [f'{k}-penthouses-for-sale' for k in PENT])
    for ck in SUITE:
        j, c = suite_page(ck); made.append(j); cfg[j['slug']] = c
    for ck in PENT: made.append(pent_page(ck))
    for ck in PENT_EXIST: add_existing(ck)
    for j in made: N.TITLE[j['slug']] = j['new_page']['h1']
    # SEO entries
    N.write_seo(made)
    # inbound links on the hubs
    n = inbound(made)
    print(len(made), 'pages;', n, 'inbound link blocks')
    if '--xlsx' in sys.argv: write_xlsx(made)
    return made


def inbound(made):
    by_city = {}
    for j in made:
        sp = j['search_page']; by_city.setdefault(sp['city'], []).append(j['slug'])
    HUB = {'surrey': ['surrey-houses-for-sale', 'surrey-homes-for-sale', 'surrey-condos-for-sale'], 'cloverdale': ['cloverdale-houses-for-sale'], 'south-surrey': ['south-surrey-houses-for-sale', 'south-surrey-homes-for-sale'],
           'langley': ['langley-houses-for-sale', 'langley-homes-for-sale'], 'abbotsford': ['abbotsford-houses-for-sale', 'abbotsford-homes-for-sale'], 'burnaby': ['burnaby-homes-for-sale', 'burnaby-condos-for-sale', 'burnaby-houses-for-sale'],
           'coquitlam': ['coquitlam-homes-for-sale', 'coquitlam-condos-for-sale', 'coquitlam-houses-for-sale'], 'richmond': ['richmond-homes-for-sale', 'richmond-condos-for-sale', 'richmond-houses-for-sale'],
           'vancouver': ['vancouver-homes-for-sale', 'vancouver-condos-for-sale', 'vancouver-houses-for-sale'], 'north-delta': ['north-delta-houses-for-sale', 'north-delta-homes-for-sale'],
           'maple-ridge': ['maple-ridge-houses-for-sale', 'maple-ridge-homes-for-sale'], 'chilliwack': ['chilliwack-houses-for-sale', 'chilliwack-homes-for-sale'], 'new-westminster': ['new-westminster-condos-for-sale', 'new-westminster-homes-for-sale']}
    n = 0
    for ck, slugs in by_city.items():
        for host in HUB.get(ck, []):
            f = f'src/data/local/{host}.json'
            if not os.path.exists(f) and not os.path.exists(f'src/data/pages/{host}.json'): continue
            ind, asc, nl = 1, False, ''
            if os.path.exists(f):
                raw = open(f).read(); j = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
                line2 = raw.split('\n')[1] if '\n' in raw else ''
                ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
            else: j = {'status': 'generated', 'slug': host, 'updated': N.UPDATED, 'blocks': []}
            j['blocks'] = [b for b in j['blocks'] if not (b.get('gen') == LG and b.get('city') == ck)]
            items = [[lk(N.TITLE[s], s)] for s in slugs if s != host]
            if not items: continue
            nmz = (SUITE.get(ck) or PENT.get(ck))['name']
            kinds = {'suite' if 'suites' in x else 'pent' for x in slugs}
            heading = f'{nmz} ' + ('houses with suites and penthouses' if len(kinds) == 2 else 'houses with suites' if 'suite' in kinds else 'penthouses')
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': heading, 'gen': LG, 'pos': 'end', 'city': ck}, {'t': 'list', 'items': items, 'gen': LG, 'pos': 'end', 'city': ck}]
            open(f, 'w').write(json.dumps(j, indent=ind, ensure_ascii=asc) + nl); n += 1
    return n


def write_xlsx(made):
    import openpyxl
    from openpyxl.styles import Alignment
    f = 'docs/review/idx/new-searches-2026-11-06.xlsx'
    wb = openpyxl.load_workbook(f); ws = wb['New searches']
    mine = {j['slug'] for j in made}
    for r in range(ws.max_row, 1, -1):
        if ws.cell(r, 1).value in mine: ws.delete_rows(r)
    AREA = {k: v.get('mls') for k, v in {**SUITE, **PENT}.items()}
    for j in made:
        sp = j['search_page']; s = j['slug']; ck = sp['city']; nm = (SUITE.get(ck) or PENT.get(ck))['name']
        if sp['kind'] == 'suite':
            name = f'SUITE {nm} House with Suite'; typ = 'House/Single Family'
            other = 'Suite field: Legal Suite, Licensed Suite or Unauthorized Suite (any of the three). In MyRealPage use the Suite / Secondary Suite feature, and confirm the field name on the first one.'
        else:
            name = f'PENT {nm} Penthouse'; typ = 'Apartment/Condo'
            other = 'Style of Home includes Penthouse.'
        sub = 'Exclude sub-area: White Rock' if ck == 'south-surrey' else '(none)'
        ws.append([s, j['new_page']['h1'], f'https://jaredgibbons.ca/{s}.html', name, AREA[ck], sub, typ, other, '(none)', 'Active', '', ''])
        for c in ws[ws.max_row]: c.alignment = Alignment(wrap_text=True, vertical='top')
    nt = wb['Notes']
    nt.append([f'Added {len(made)} more searches on 2026-11-06 from Pete’s sold export: houses with a suite (12 cities) and penthouses (6 cities). Same set-up as the rows above. The three older penthouse drafts keep their existing searches.'])
    wb.save(f)
    print('worksheet updated:', ws.max_row - 1, 'rows')


if __name__ == '__main__': main()
