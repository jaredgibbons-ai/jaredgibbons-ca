#!/usr/bin/env python3
"""Neighbourhood guides for areas people search by name that had no page (D-203, Nov 10, 2026).

Gap check: Google's autocomplete (gl=ca) for "<area> homes / real estate / houses for sale / condos / townhomes", run for 47
neighbourhood names that had no guide. The ones with real-estate suggestions and no page here:
    Rosemary Heights (South Surrey)   7 / 1 / 2 / 3 / 3 suggestions, and Jared named it     -> rosemary-heights-guide
    Yorkson (Willoughby, Langley)     3 / 0 / 1 / 10 / 9                                    -> yorkson-langley-guide
    Auguston (Abbotsford)             4 / 3 / 3 / 2 / 2                                     -> auguston-abbotsford-guide
Not built: Semiahmoo (suggestions are mostly the US resort, the mall and the secondary school; the town-centre area is covered by
the King George Corridor and Sunnyside Park guides), Latimer and Carvolth (condo searches only, covered by the Willoughby pages),
Campbell Heights (industrial). See docs/04-decisions-and-exceptions.md D-203.

Facts and where they come from
  Rosemary Heights: City of Surrey Rosemary Heights NCPs page and park pages (fetched Nov 10, 2026); school facts from
    src/data/schools/facts.json; sales within 1 km of Rosemary Heights Elementary from src/data/schools/radius-sold.json (Pete's Paragon
    exports, closed and pending, Nov 1, 2025 to Oct 31, 2026); the Morgan Creek sub-area from src/data/sold/sold-12m.json; buildings and
    the 55+ community from the existing Morgan Creek pages; Jared's take from docs/research/jared-voice (his Nov 9 answer).
  Yorkson: Township of Langley Yorkson Neighbourhood Plan, Bylaw 4030 (redlined OCP-update version, Aug 27, 2025); sales within 1 km of
    Willoughby Elementary (20766 80 Ave, the plan's Town Centre corner); the Willoughby Heights sub-area; parks, transit and schools
    already sourced on the Willoughby guide.
  Auguston: Abbotsford School District, Auguston Traditional Elementary name history page; the Abbotsford East sub-area; schools, parks,
    transit and Sage at Auguston already sourced on the Abbotsford East and Sumas Mountain pages.
Pages are drafts (status draft, a "Draft for Jared" notice that the launch build hides). Idempotent.
python3 -I tools/build_gap_guides_2026_11_10.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'gap'
RAD = json.load(open('src/data/schools/radius-sold.json'))
SUB = json.load(open('src/data/sold/sold-12m.json'))['sub']
RAD_SRC = ('Source: Paragon MLS®, closed and pending sales by sold date, November 1, 2025 to October 31, 2026, within 1 km of the school '
           'in a straight line. A pending sale is firm but has not completed. Medians are shown where at least 5 homes of a type sold.')
SUB_SRC = ('Source: Paragon MLS® closed sales supplied by Jared, November 1, 2025 to October 22, 2026, for the whole MLS® sub-area. '
           'Medians are shown where at least 5 homes of a type sold.')


def money(v): return '—' if not v else f'${v:,.0f}'
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def PP(*parts): return {'t': 'p', 'parts': [({'t': x[0], 'h': x[1]} if isinstance(x, tuple) else {'t': x}) for x in parts], 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def L(items): return {'t': 'list', 'items': [[({'t': i[0], 'h': i[1]} if isinstance(i, tuple) else {'t': i})] for i in items], 'gen': G}
def LINKS(pairs): return {'t': 'list', 'items': [[{'t': t, 'h': h if h.startswith('http') else f'/{h}.html'}] for t, h in pairs], 'gen': G}
def TBL(cap, head, rows, src): return {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'source': src, 'gen': G}
def NOTICE(t): return {'t': 'notice', 'text': t, 'gen': G}


def radius_rows(key):
    g = RAD[key]['groups']; rows = []
    for k, lab in (('house', 'Detached houses'), ('townhouse', 'Townhomes'), ('condo', 'Condos')):
        x = g.get(k) or {}
        if not x.get('n'): continue
        ok = x['n'] >= 5
        rows.append([lab, f"{x['n']:,}", money(x['price']) if ok else '—', f"{money(x['p25'])} to {money(x['p75'])}" if ok and x.get('p25') else '—',
                     str(x['dom']) if ok else '—', f"{x['ratio']:.1f}%" if ok else '—'])
    return rows


def sub_rows(key):
    g = SUB[key]['groups']; rows = []
    for k, lab in (('house', 'Detached houses'), ('townhome', 'Townhomes'), ('condo', 'Condos'), ('duplex', 'Duplexes')):
        x = g.get(k) or {}
        if not x.get('n'): continue
        ok = x['n'] >= 5 and x.get('price')
        rows.append([lab, f"{x['n']:,}", money(x['price']) if ok else '—', f"{money(x['p25'])} to {money(x['p75'])}" if ok and x.get('p25') and x.get('p75') else '—',
                     str(x['yb']) if x.get('yb') else '—'])
    return rows


RH = ['Home type', 'Sales', 'Median price', 'Middle half of prices', 'Median days to sell', 'Sold price vs list']
SH = ['Home type', 'Sales', 'Median price', 'Middle half of prices', 'Typical year built']
CRUMB_HOME = {'name': 'Home', 'href': '/'}

# ------------------------------------------------------------------------------------------------ Rosemary Heights
r = RAD['rosemary-heights-elementary']; rg = r['groups']; mc = SUB['South Surrey White Rock|Morgan Creek']['groups']
rq = r['q']
ROSEMARY = {
    'slug': 'rosemary-heights-guide', 'status': 'draft', 'updated': '2026-11-10', 'lead': 'homevalue', 'lead_place': 'Rosemary Heights',
    'new_page': {'h1': 'Rosemary Heights, South Surrey: Neighbourhood Guide',
                 'title': 'Rosemary Heights South Surrey Homes and Neighbourhood Guide',
                 'description': 'Rosemary Heights in South Surrey: what homes near the school sold for, the condos, townhomes and 55+ homes, schools, parks and Jared’s tips.'},
    'breadcrumbs': [CRUMB_HOME, {'name': 'South Surrey and White Rock', 'href': '/south-surrey-homes-for-sale.html'},
                    {'name': 'Neighbourhood guides', 'href': '/south-surrey-neighbourhoods.html'}, {'name': 'Rosemary Heights', 'href': '/rosemary-heights-guide.html'}],
    'blocks': [
        NOTICE('Draft for Jared’s approval. Written November 10, 2026 from City of Surrey, Surrey School District and MLS® sources listed on the page.'),
        P('Rosemary Heights is the planned neighbourhood on the east side of Highway 99 in South Surrey, between the Nicomekl River to the north and Titman Creek '
          'to the south, with the Morgan Creek golf course on its east side. The City laid it out in the 1990s: a local area plan in 1994, then neighbourhood '
          'plans for Rosemary Heights Central (1996), Rosemary Heights West (1997) and the Rosemary Heights Business Park (2000). The City now calls all three '
          'areas largely built out, so almost every home that comes up for sale here is a resale.'),
        P('You will not find Rosemary Heights as an area on MLS®. The board files its listings under Morgan Creek, the sub-area named after the golf course '
          'community next door, which is why searches and market reports blend the two. This guide looks at Rosemary Heights on its own: the condo buildings '
          'along 36 Avenue and at Harvard Gardens, the 55+ community on Rosemary Heights Crescent, and the family streets around Rosemary Heights Elementary.'),
        H('Homes for sale in Rosemary Heights'),
        PP('Because the board files Rosemary Heights under Morgan Creek, the live listings for both are on one search: ', ('Morgan Creek homes for sale', '/morgan-creek.html'),
           '. To narrow it to listings that name the neighbourhood school, use ', ('homes for sale near Rosemary Heights Elementary', '/homes-near-rosemary-heights-elementary.html'), '.'),
        LINKS([('Morgan Creek and Rosemary Heights condos and townhomes', 'morgan-creek-south-surrey-condos-townhomes-for-sale'),
               ('Morgan Creek and Rosemary Heights houses', 'morgan-creek-south-surrey-houses-for-sale'),
               ('55+ homes in Morgan Creek and Rosemary Heights', 'morgan-creek-55-plus-homes-for-sale'),
               ('South Surrey townhomes for sale', 'south-surrey-townhomes-for-sale')]),
        H('What homes near Rosemary Heights Elementary sold for'),
        P(f"The board publishes nothing for Rosemary Heights alone, so the closest local measure is a 1 km circle around its school, which sits in the middle "
          f"of the neighbourhood at 15516 36 Avenue. In the twelve months to October 31, 2026, {r['n']} homes sold inside that circle: {rg['condo']['n']} condos, "
          f"{rg['townhouse']['n']} townhomes and {rg['house']['n']} detached houses. {r['sub'][0][1]} of those sales were in the Morgan Creek sub-area and "
          f"{r['sub'][1][1]} in the neighbouring Grandview sub-area to the south, which the circle reaches."),
        TBL('Homes sold within 1 km of Rosemary Heights Elementary, by type', RH, radius_rows('rosemary-heights-elementary'), RAD_SRC),
        P(f"Detached houses near the school sold at a median of {money(rg['house']['price'])}, a little under the {money(mc['house']['price'])} median for the whole "
          f"Morgan Creek sub-area, which includes the larger golf-course estates. Townhomes ({money(rg['townhouse']['price'])}) and condos ({money(rg['condo']['price'])}) "
          f"were close to the sub-area medians of {money(mc['townhome']['price'])} and {money(mc['condo']['price'])}. Houses took longest to sell, at "
          f"{rg['house']['dom']} days at the median, and sold for {rg['house']['ratio']:.1f}% of the asking price."),
        P(f"Quarter by quarter, the median for all home types together went {money(rq[0][2])} (November to January), {money(rq[1][2])} (February to April), "
          f"{money(rq[2][2])} (May to July) and {money(rq[3][2])} (August to October). Those figures mix condos and houses, so a quarter with more condo sales "
          f"reads lower. Price a home from the by-type rows instead."),
        H('Condos, townhomes and 55+ homes in Rosemary Heights'),
        P('The apartment buildings sit on the west side of the neighbourhood, in two groups. Along 36 Avenue west of 152 Street are Edgewater, a gated community '
          'at 15195 36 Avenue built in 2013 above the Nicomekl River, and Tehama, at 3355 Rosemary Heights Drive, built in 2008. Near 32 Avenue and 151 Street '
          'is Harvard Gardens, which includes Kingston House and Prescott Commons.'),
        P('Within the 1 km circle, Edgewater had the most condo sales over the year (13, at a median of $678,000), followed by Headwaters (8, $578,500), Prescott '
          'Commons (5, $525,000) and Harvard Gardens (5, $555,000). On the townhome side, Sundance led with 8 sales at a median of $681,950.'),
        PP('The 55+ homes you can buy are in the Carrington community on Rosemary Heights Crescent: The Carrington at 15500, Carrington at 15450 and Braemore at '
           'Carrington at 15425. Rosemary Heights Seniors Village, at 15240 34 Avenue, is a different kind of place: a seniors campus with independent living, '
           'assisted living and long-term care that you rent or are placed in, not a strata you buy into. Both are covered on the ',
           ('Morgan Creek 55+ homes page', '/morgan-creek-55-plus-homes-for-sale.html'), '.'),
        H('Schools in Rosemary Heights'),
        P('The City lists two elementary schools for Rosemary Heights: Rosemary Heights Elementary (kindergarten to grade 7, 15516 36 Avenue) and Morgan '
          'Elementary (kindergarten to grade 7, 3366 156A Street), about half a kilometre apart. Addresses checked on Rosemary Heights Crescent and Morgan Creek '
          'Way were in the Grandview Heights Secondary catchment (16987 25 Avenue) for grades 8 to 12. The nearest independent school is Southridge School, '
          'kindergarten to grade 12, at 2656 160 Street, about 2 km away.'),
        PP('Surrey Schools sets the catchments and they can change, so check the exact address in the ', ('district’s school locator', 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC36'),
           ' before you offer. More on the area’s schools: ', ('Schools in South Surrey and White Rock', '/schools-in-south-surrey-white-rock-bc.html'), '.'),
        H('Parks in Rosemary Heights'),
        L(['Rosemary Heights Park, 3501 154 Street: wide lawns and paths laid out like a traditional British common, with a picnic area. Its paths carry on east '
           'through Blumsen Park.',
           'Blumsen Park, 15473 34 Avenue: a playground and a large wooded area with forest trails, between Rosemary Heights Drive and 34 Avenue, just south of '
           'Rosemary Heights Elementary. It is named after Blumsen Avenue, the old name for 34 Avenue.',
           'Nicomekl Riverfront Park: a 3 km, 80-acre linear park the City is building along the south bank of the Nicomekl River, from Elgin Road to 40 Avenue. '
           'Most of it is still being designed and is closed. The fenced Nicomekl Dog Off-Leash Park, about an acre at 3435 150 Street, is open and is reached on '
           'foot from the pathway, with no parking.',
           'Morgan Creek Park, 3302 156A Street, on the golf-course side.']),
        H('Getting around Rosemary Heights', 3),
        L(['Route 354 (TransLink) runs between White Rock South and Bridgeport Station on the Canada Line, via 32 Avenue and 160 Street.',
           'Route 363 runs from Peace Arch Hospital to King George Boulevard at 32 Avenue, via 160 Street and 24 Avenue.',
           'Highway 99 runs along the west edge of the neighbourhood. Morgan Crossing and Grandview Corners, the main shopping areas, are a short drive south-east.']),
        TBL('Measured from Rosemary Heights Elementary, 15516 36 Avenue', ['To', 'How', 'Minutes', 'Distance (km)'],
            [['Morgan Elementary', 'Walk', '11', '0.8'], ['Morgan Creek Park', 'Walk', '12', '0.9'], ['Walmart Supercentre, 2355 160 Street', 'Drive', '7', '3.6'],
             ['White Rock Centre', 'Drive', '9', '5.0'], ['Grandview Heights Secondary', 'Drive', '10', '6.0']],
            'Measured November 2, 2026 with OpenStreetMap routing (OSRM for driving, routed foot paths for walking).'),
        H('Before you buy in Rosemary Heights'),
        L(['Walk the street at school drop-off or pickup. The streets beside Rosemary Heights Elementary and Blumsen Park are busy for half an hour twice a day, '
           'and a block or two away they are quiet.',
           'Look at what is behind the lot. The City notes a river, fish-bearing creeks and rare wetland habitat in Rosemary Heights, and a home that backs onto '
           'a creek or the Nicomekl can have setbacks that limit fences, decks and additions. Ask the City before you plan a project.',
           'If the home is close to Highway 99, go back at rush hour to hear it.',
           'For a townhome or condo, read the strata minutes, Form B and depreciation report before you remove subjects, and compare fees by strata plan, '
           'since some complexes share a name across several plans.',
           'The Rosemary Heights neighbourhood plans were rescinded when the Surrey 2050 Official Community Plan came in, so a rezoning nearby is now judged '
           'against the OCP. Check for development applications near the address.']),
        PP('The Surrey-wide rules on property tax, zoning, suites and flood mapping are on one page: ', ('buying a home in Surrey: the rules', '/surrey-home-buying-rules.html'),
           '. Strata checks are in ', ('BC townhome buying rules', '/bc-townhome-buying-rules.html'), ' and ', ('BC condo buying rules', '/bc-condo-buying-rules.html'), '.'),
        H('Nearby neighbourhood guides'),
        LINKS([('Morgan Creek', 'morgan-creek-guide'), ('Grandview Heights', 'grandview-heights-guide'), ('Elgin Chantrell', 'elgin-chantrell-guide'),
               ('Crescent Beach and Ocean Park', 'crescent-beach-ocean-park-guide'), ('All South Surrey and White Rock guides', 'south-surrey-neighbourhoods')]),
        H('Sources for the Rosemary Heights guide'),
        LINKS([('City of Surrey: Rosemary Heights neighbourhood plans', 'https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning/south-surrey-land-use-plans/rosemary-heights-ncps'),
               ('City of Surrey: Rosemary Heights Park', 'https://www.surrey.ca/parks-recreation/parks/rosemary-heights-park'),
               ('City of Surrey: Blumsen Park', 'https://www.surrey.ca/parks-recreation/parks/blumsen-park'),
               ('City of Surrey: Nicomekl Riverfront Park', 'https://www.surrey.ca/parks-recreation/parks/nicomekl-riverfront-park'),
               ('Surrey Schools: Rosemary Heights Elementary', 'https://www.surreyschools.ca/rosemaryheights'),
               ('TransLink route 354 timetable', 'https://infomaps.translink.ca/Public_Timetables/221/tt354.pdf'),
               ('TransLink route 363 timetable', 'https://infomaps.translink.ca/Public_Timetables/214/tt363.pdf')]),
    ],
    'faq': [
        {'q': 'Is Rosemary Heights part of Morgan Creek?', 'a': 'On MLS®, yes: the board files Rosemary Heights listings under the Morgan Creek sub-area. The City of Surrey treats Rosemary Heights as its own planned neighbourhood, west of the Morgan Creek golf course.'},
        {'q': 'Where are the edges of Rosemary Heights?', 'a': 'The City describes Rosemary Heights as south of the Nicomekl River, east of Highway 99 and north of Titman Creek, with the golf course on its east side.'},
        {'q': 'Are new homes being built in Rosemary Heights?', 'a': 'Very few. The City calls the neighbourhood largely built out, so most homes for sale are resales. Newer townhomes and condos nearby are mostly in Grandview Heights, to the south-east.'},
        {'q': 'Is Rosemary Heights Seniors Village a 55+ strata?', 'a': 'No. It is a seniors campus with independent living, assisted living and long-term care that you rent or are placed in. The 55+ homes you can buy are in the Carrington community on Rosemary Heights Crescent.'},
    ],
}

# ------------------------------------------------------------------------------------------------ Yorkson
w = RAD['willoughby-elementary']; wg = w['groups']; wh = SUB['Langley|Willoughby Heights']['groups']
YORKSON = {
    'slug': 'yorkson-langley-guide', 'status': 'draft', 'updated': '2026-11-10', 'lead': 'homevalue', 'lead_place': 'Yorkson',
    'new_page': {'h1': 'Yorkson, Langley: Neighbourhood Guide',
                 'title': 'Yorkson Langley Homes for Sale and Neighbourhood Guide',
                 'description': 'Yorkson in Willoughby, Langley: where it starts and ends, what the plan builds, what townhomes, condos and houses sold for, schools and parks.'},
    'breadcrumbs': [CRUMB_HOME, {'name': 'Langley', 'href': '/langley-homes-for-sale.html'}, {'name': 'Neighbourhood guides', 'href': '/langley-neighbourhood-guides.html'},
                    {'name': 'Yorkson', 'href': '/yorkson-langley-guide.html'}],
    'blocks': [
        NOTICE('Draft for Jared’s approval. Written November 10, 2026 from the Township of Langley’s Yorkson Neighbourhood Plan, Langley School District and MLS® sources listed on the page.'),
        P('Yorkson is the north-east corner of Willoughby, in the Township of Langley. Its neighbourhood plan draws the edges: Highway 1 on the north, 212 Street '
          'on the east, 74B and 76 Avenues on the south, and 203 and 204 Streets on the west, about 330 hectares (815 acres) in all. Council first adopted the '
          'plan in July 2001 as Bylaw 4030 and updated it in 2008, and the current version was adopted on December 1, 2025 with the Township’s new Official '
          'Community Plan.'),
        P('The plan is written for about 28,000 people in roughly 11,800 homes once the area is built out, which is why so much of Yorkson is townhomes and '
          'low-rise condos rather than detached lots, and why construction is still going on in places. Its centre is the Town Centre at 208 Street and 80 '
          'Avenue. On MLS® Yorkson is not an area of its own: listings sit in the Willoughby Heights sub-area with the rest of Willoughby.'),
        H('Homes for sale in Yorkson'),
        PP('The live searches cover all of Willoughby, Yorkson included: ', ('Willoughby homes for sale', '/willoughby-homes-for-sale.html'), '. For listings that name a '
           'Yorkson school, try ', ('homes near Willoughby Elementary', '/homes-near-willoughby-elementary.html'), ' and ', ('homes near Lynn Fripps Elementary', '/homes-near-lynn-fripps-elementary.html'), '.'),
        LINKS([('Willoughby townhomes for sale', 'willoughby-townhomes-for-sale'), ('Willoughby condos for sale', 'willoughby-condos-for-sale'),
               ('Willoughby houses for sale', 'willoughby-houses-for-sale'), ('New construction in Willoughby Heights', 'new-construction-willoughby-heights')]),
        H('What homes sold for in and around Yorkson'),
        P(f"Willoughby Elementary sits on the Town Centre corner, at 20766 80 Avenue, so a 1 km circle around it is a fair picture of central Yorkson, though it "
          f"also reaches a little past the plan’s west and south edges. In the twelve months to October 31, 2026, {w['n']} homes sold inside it: "
          f"{wg['townhouse']['n']} townhomes, {wg['condo']['n']} condos, {wg['house']['n']} detached houses and {wg['other']['n']} other homes, mostly duplexes."),
        TBL('Homes sold within 1 km of Willoughby Elementary, by type', RH, radius_rows('willoughby-elementary'), RAD_SRC),
        P(f"Townhomes are the main market here, at a median of {money(wg['townhouse']['price'])} and {wg['townhouse']['dom']} days to sell. By complex, Heath West "
          f"had the most townhome sales (23, median $959,900), then Griffon (20, $939,900) and Townside Village (11, $1,029,900). Among condo buildings, The Hive 2 "
          f"led (27 sales, $464,900), ahead of Walnut Park (16, $484,950), Union Park (15, $595,000) and The Commons (14, $469,995)."),
        P(f"Across the whole Willoughby Heights sub-area, detached houses sold at a median of {money(wh['house']['price'])} (the typical one built in "
          f"{wh['house']['yb']} on a {wh['house']['lot_sqft']:,} square foot lot), townhomes at {money(wh['townhome']['price'])}, condos at "
          f"{money(wh['condo']['price'])} and duplexes at {money(wh['duplex']['price'])}."),
        TBL('Willoughby Heights sub-area, homes sold by type', SH, sub_rows('Langley|Willoughby Heights'), SUB_SRC),
        H('What the Yorkson plan sets out'),
        L(['A Town Centre at 208 Street and 80 Avenue, split into a core and an outer ring, with a high street of shops facing the anchor stores.',
           'Smaller commercial spots: low-density mixed use at 208 Street and 83 Avenue, and neighbourhood shops at the north-west corner of 204 Street and 80 Avenue.',
           'Four elementary schools and one more secondary school over time. The plan marks the Willoughby Elementary site for redevelopment as part of the '
           'Town Centre, with a replacement school required.',
           'Yorkson Creek, the main fish-bearing stream, with its streamside area protected, and a network of greenways along creeks, streets, 212 Street '
           'and the highway.',
           'A 15 metre natural buffer along Highway 1 on the north edge.',
           'Two protected heritage buildings: the 1931 Willoughby School at 208 Street and 80 Avenue and the 1937 Willoughby Community Hall.',
           '208 Street and 80 Avenue as major arterial roads, with a fence along the 208 Street median to stop mid-block crossings.']),
        H('Schools in Yorkson'),
        L(['Willoughby Elementary, kindergarten to grade 5, 20766 80 Avenue.', 'Lynn Fripps Elementary, kindergarten to grade 5, 21020 83 Avenue.',
           'Yorkson Creek Middle School, grades 6 to 8, 20686 84 Avenue.',
           'R.E. Mountain Secondary, grades 9 to 12, 7633 202A Street, west of Yorkson. The plan expects it to take Yorkson’s secondary students in the short to medium term.']),
        PP('Langley Schools sets the catchments. Check the exact address in the ', ('district’s school locator', 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC35'),
           ' before you offer. More: ', ('Schools in Langley', '/schools-in-langley-bc.html'), '.'),
        H('Parks, shopping and getting around'),
        L(['Yorkson Community Park, at 84 Avenue and 206 Street: a playground, a spray park and a synthetic sports field.',
           'Willoughby Community Park, 7782 200 Street, and the Langley Events Centre, 7888 200 Street, just west of Yorkson: sports fields, a stadium, an arena and gyms.',
           'Groceries: Hakam’s Your Independent Grocer, 20678 Willoughby Town Centre Drive.',
           'Route 595 (TransLink) runs along 208 Street and 88 Avenue to Langley Centre and Maple Meadows Station. Route 562 uses 88 Avenue, and Carvolth '
           'Exchange to the west has route 501 to Surrey Central Station.',
           'Highway 1 forms the north edge of the neighbourhood.']),
        H('Before you buy in Yorkson'),
        L(['Ask what is planned next door. The plan is far from built out, so a vacant lot or older house beside a new townhome can become a building site.',
           'On the east side, check creek and greenway setbacks. Yorkson Creek runs through it, and the Township flags hazards around its creeks and greenways.',
           'If the home backs onto Highway 1, visit at rush hour. The plan’s 15 metre buffer is trees, not a sound wall.',
           'Compare strata fees and reports by strata plan, not by project name. Some complexes are split across several plans and addresses.',
           'For a new or nearly new home, confirm the home warranty and who pays GST, and read the disclosure statement for a presale.']),
        PP('Township-wide rules on property tax, zoning, suites and servicing are on one page: ', ('buying a home in the Township of Langley: the rules', '/langley-home-buying-rules.html'),
           '. Strata checks are in ', ('BC townhome buying rules', '/bc-townhome-buying-rules.html'), '.'),
        H('Nearby neighbourhood guides'),
        LINKS([('Willoughby Heights', 'willoughby-guide'), ('Walnut Grove', 'walnut-grove-guide'), ('Langley City', 'langley-city-guide'),
               ('Murrayville', 'murrayville-guide'), ('All Langley guides', 'langley-neighbourhood-guides')]),
        H('Sources for the Yorkson guide'),
        LINKS([('Township of Langley: Yorkson Neighbourhood Plan, Bylaw 4030 (OCP update version)', 'https://www.tol.ca/en/connect/resources/get-involved/ocp-update/ATT-J-Redlined-Bylaw-4030-Yorkson-Neighbourhood-Plan---Aug-27-2025.pdf'),
               ('Township of Langley: Yorkson Community Park north campus', 'https://www.tol.ca/en/news/yorkson-community-park-north-campus-opens.aspx'),
               ('Langley Schools: Willoughby Elementary', 'https://www.sd35.bc.ca/willoughby'),
               ('Langley Schools: Yorkson Creek Middle School', 'https://www.sd35.bc.ca/ycms'),
               ('TransLink route 595 timetable', 'https://infomaps.translink.ca/Public_Timetables/214/tt595.pdf'),
               ('TransLink route 501 timetable', 'https://infomaps.translink.ca/Public_Timetables/221/tt501.pdf')]),
    ],
    'faq': [
        {'q': 'Is Yorkson the same as Willoughby?', 'a': 'Yorkson is one of the neighbourhoods inside Willoughby, in its north-east corner. On MLS® all of Willoughby, Yorkson included, is the Willoughby Heights sub-area.'},
        {'q': 'Where does Yorkson start and end?', 'a': 'The Township’s plan puts it between Highway 1 on the north, 212 Street on the east, 74B and 76 Avenues on the south, and 203 and 204 Streets on the west.'},
        {'q': 'Is Yorkson finished?', 'a': 'No. The plan is written for about 28,000 people in roughly 11,800 homes, and building is still going on, so check what is planned near any address.'},
        {'q': 'Is Yorkson the same as Latimer?', 'a': 'No. Latimer is a separate Willoughby neighbourhood with its own Township neighbourhood plan.'},
    ],
}

# ------------------------------------------------------------------------------------------------ Auguston
ae = SUB['Abbotsford|Abbotsford East']['groups']
AUGUSTON = {
    'slug': 'auguston-abbotsford-guide', 'status': 'draft', 'updated': '2026-11-10', 'lead': 'homevalue', 'lead_place': 'Auguston',
    'new_page': {'h1': 'Auguston, Abbotsford: Neighbourhood Guide',
                 'title': 'Auguston Abbotsford Homes for Sale and Neighbourhood Guide',
                 'description': 'Auguston on Sumas Mountain, Abbotsford: how the planned village came about, what homes in Abbotsford East sold for, the school, parks and bus.'},
    'breadcrumbs': [CRUMB_HOME, {'name': 'Abbotsford', 'href': '/abbotsford-homes-for-sale.html'}, {'name': 'Neighbourhood guides', 'href': '/abbotsford-neighbourhood-guides.html'},
                    {'name': 'Auguston', 'href': '/auguston-abbotsford-guide.html'}],
    'blocks': [
        NOTICE('Draft for Jared’s approval. Written November 10, 2026 from Abbotsford School District, BC Transit and MLS® sources listed on the page.'),
        P('Auguston is a planned neighbourhood on the lower slopes of Sumas Mountain, on Abbotsford’s east side. Its developers bought more than 1,000 acres '
          'from Clayburn Industries, started planning in 1988 and began building in 1998. The name joins “august”, meaning grand, with “ton”, an old English '
          'word for town, according to the Abbotsford School District’s history of the neighbourhood school.'),
        P('It was designed as a self-contained village where children could walk to school, and its streets are named after Canadian artists and writers: '
          'Stephen Leacock Drive, Tom Thomson Crescent, Emily Carr Terrace. When the school opened in 2000 the plan was for up to 6,000 residents in about 2,000 '
          'homes. Because building only began in 1998, Auguston’s houses are newer than most of east Abbotsford. On MLS® Auguston is part of the Abbotsford '
          'East sub-area.'),
        H('Homes for sale in Auguston'),
        PP('Auguston listings show up in the Abbotsford East searches: ', ('Abbotsford East houses for sale', '/abbotsford-east-houses-for-sale.html'), ' and ',
           ('Abbotsford East condos and townhomes', '/abbotsford-east-condos-townhomes-for-sale.html'), '.'),
        LINKS([('Abbotsford East homes for sale', 'abbotsford-east'), ('Sumas Mountain homes for sale', 'sumas-mountain'),
               ('Abbotsford houses for sale', 'abbotsford-houses-for-sale'), ('Abbotsford townhomes for sale', 'abbotsford-townhomes-for-sale')]),
        H('What homes sold for in Abbotsford East'),
        P(f"The board does not report Auguston separately, so the nearest figures are for the Abbotsford East sub-area it belongs to. From November 1, 2025 to "
          f"October 22, 2026, {ae['house']['n']} detached houses sold there at a median of {money(ae['house']['price'])}, with the middle half between "
          f"{money(ae['house']['p25'])} and {money(ae['house']['p75'])}. Townhomes ({ae['townhome']['n']} sales) went for a median of "
          f"{money(ae['townhome']['price'])} and condos ({ae['condo']['n']} sales) for {money(ae['condo']['price'])}."),
        TBL('Abbotsford East sub-area, homes sold by type', SH, sub_rows('Abbotsford|Abbotsford East'), SUB_SRC),
        P(f"The typical detached house that sold in Abbotsford East was built in {ae['house']['yb']} on a {ae['house']['lot_sqft']:,} square foot lot. Auguston "
          f"homes all date from 1998 or later, so expect a house here to be newer than that typical sale, and price it against other Auguston and Sumas "
          f"Mountain sales rather than the sub-area median."),
        H('The homes in Auguston'),
        P('Most of Auguston is detached family houses on serviced hillside lots, many of them two storeys over a basement, and some were built with a '
          'basement suite. The main strata complex is Sage at Auguston, at 4401 Blauson Boulevard beside the school: 120 homes in three storeys, built in '
          '2007, with no age restriction on record.'),
        H('Schools in Auguston'),
        P('Auguston Traditional Elementary, at 36367 Stephen Leacock Drive, teaches kindergarten to grade 5. It opened in 2000 as the district’s second '
          'traditional school, a model built around structure and basic skills, and it was the first school in BC built as a joint project with a private '
          'company, which is why the district leases the building rather than owning it. Registration was in such demand when it opened that some parents '
          'camped out for days to get a place.'),
        P('A school locator check at 36367 Stephen Leacock Drive returned Auguston Traditional Elementary, Clayburn Middle School and Robert Bateman Secondary '
          '(35045 Exbury Avenue). Enrolment at a traditional school can work differently from a regular catchment school, so ask the district how a place '
          'is assigned for the exact address before you rely on it.'),
        PP('More: ', ('Schools in Abbotsford', '/schools-in-abbotsford-bc.html'), '.'),
        H('Parks and getting around'),
        L(['Mathers Park, beside the school on Stephen Leacock Drive, a two-minute walk from the school door.',
           'Lower Sumas Mountain Park, 2850 Whatcom Road, about an 11-minute drive.',
           'Sumas Mountain Regional Park, higher up the mountain, with the Chadsey Lake Trail.',
           'BC Transit route 15 (Auguston/Montrose) runs from Montrose Exchange via McKee Road to Auguston Parkway South at Stephen Leacock Drive.',
           'Highway 1 is reached at Whatcom Road. Shopping is at Sumas Mountain Village, 2310 Whatcom Road, and the Walmart at 1812 Vedder Way.']),
        TBL('Measured from Auguston Traditional Elementary, 36367 Stephen Leacock Drive', ['To', 'How', 'Minutes', 'Distance (km)'],
            [['Mathers Park', 'Walk', '2', '0.2'], ['Sandy Hill Elementary', 'Drive', '9', '5.4'], ['Lower Sumas Mountain Park', 'Drive', '11', '6.2'],
             ['Montrose Exchange', 'Drive', '15', '8.7']],
            'Measured November 2, 2026 with OpenStreetMap routing (OSRM for driving, routed foot paths for walking).'),
        H('Before you buy in Auguston'),
        L(['Hillside lots need a closer look: ask about retaining walls, drainage and any geotechnical covenant on title, and get a survey if the yard is terraced.',
           'If the house has a suite, confirm with the City of Abbotsford that it is permitted, and check what the suite adds to your property taxes and utilities.',
           'Drive the route you will use every day. Everything off the mountain goes down to Whatcom Road, so time the trip at rush hour.',
           'For Sage at Auguston or any townhome, read the strata minutes, Form B and depreciation report before you remove subjects.']),
        PP('Abbotsford-wide rules on property tax, zoning, suites and flood mapping are on one page: ', ('buying a home in Abbotsford: the rules', '/abbotsford-home-buying-rules.html'), '.'),
        H('Nearby neighbourhood guides'),
        LINKS([('Abbotsford East', 'abbotsford-east-guide'), ('Sumas Mountain', 'sumas-mountain-guide'), ('Central Abbotsford', 'central-abbotsford-guide'),
               ('All Abbotsford guides', 'abbotsford-neighbourhood-guides')]),
        H('Sources for the Auguston guide'),
        LINKS([('Auguston Traditional Elementary: the school’s name and history', 'https://auguston.abbyschools.ca/school-name-history-3'),
               ('Auguston Traditional Elementary', 'https://auguston.abbyschools.ca'),
               ('BC Transit Central Fraser Valley: riders guide', 'https://www.bctransit.com/central-fraser-valley/schedules-and-maps/riders-guide/'),
               ('City of Abbotsford: parks and playgrounds', 'https://www.abbotsford.ca/parks-playgrounds')]),
    ],
    'faq': [
        {'q': 'Is Auguston part of Sumas Mountain?', 'a': 'Yes. Auguston sits on the lower slopes of Sumas Mountain, in the City of Abbotsford. On MLS® its listings are in the Abbotsford East sub-area.'},
        {'q': 'How old are the homes in Auguston?', 'a': 'Building started in 1998, so Auguston’s homes date from then on, newer than most of east Abbotsford.'},
        {'q': 'Is there a bus to Auguston?', 'a': 'Yes. BC Transit route 15 runs between Montrose Exchange and Auguston Parkway South at Stephen Leacock Drive.'},
        {'q': 'Does every Auguston home go to Auguston Traditional Elementary?', 'a': 'Not automatically. It is a traditional school, so ask the Abbotsford School District how a place is assigned for the exact address.'},
    ],
}

GUIDES = [ROSEMARY, YORKSON, AUGUSTON]

# ------------------------------------------------------------------------------------------------ links in from parent guides and hubs
PARENT = {
    'morgan-creek-guide': ('Rosemary Heights, the planned neighbourhood on the west side of this sub-area, has its own guide: ', 'Rosemary Heights neighbourhood guide', 'rosemary-heights-guide'),
    'morgan-creek': ('Rosemary Heights listings are filed under Morgan Creek. For the neighbourhood itself, see the ', 'Rosemary Heights neighbourhood guide', 'rosemary-heights-guide'),
    'willoughby-guide': ('Yorkson, the north-east corner of Willoughby, has its own guide: ', 'Yorkson neighbourhood guide', 'yorkson-langley-guide'),
    'abbotsford-east-guide': ('Auguston, the planned village on the lower slopes of Sumas Mountain, has its own guide: ', 'Auguston neighbourhood guide', 'auguston-abbotsford-guide'),
    'sumas-mountain-guide': ('Auguston, on the mountain’s lower slopes, has its own guide: ', 'Auguston neighbourhood guide', 'auguston-abbotsford-guide'),
}
HUB = {
    'south-surrey-neighbourhoods': [('Rosemary Heights', 'rosemary-heights-guide', 'inside the Morgan Creek sub-area')],
    'langley-neighbourhood-guides': [('Yorkson', 'yorkson-langley-guide', 'inside the Willoughby Heights sub-area')],
    'abbotsford-neighbourhood-guides': [('Auguston', 'auguston-abbotsford-guide', 'inside the Abbotsford East sub-area')],
}


def save(path, d):
    if os.path.exists(path):
        raw = open(path, encoding='utf-8').read()
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        nl = '\n' if raw.endswith('\n') else ''
    else: ind, nl = 2, '\n'
    s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
    open(path, 'w', encoding='utf-8').write(s + nl)


def main():
    for g in GUIDES:
        nb = g['new_page']
        assert 38 <= len(nb['title']) <= 60, (g['slug'], len(nb['title']))
        assert 135 <= len(nb['description']) <= 158 and nb['description'].endswith('.'), (g['slug'], len(nb['description']))
        save(f"src/data/local/{g['slug']}.json", g)
    for slug, (lead, label, target) in PARENT.items():
        p = f'src/data/local/{slug}.json'; d = json.load(open(p, encoding='utf-8'))
        d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'gaplink']
        d['blocks'].insert(0, {'t': 'p', 'parts': [{'t': lead}, {'t': label, 'h': f'/{target}.html'}, {'t': '.'}], 'gen': 'gaplink'})
        save(p, d)
    for slug, items in HUB.items():
        p = f'src/data/local/{slug}.json'; d = json.load(open(p, encoding='utf-8'))
        d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'gaplink']
        d['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Neighbourhoods inside a sub-area', 'gen': 'gaplink', 'pos': 'end'},
                        {'t': 'p', 'text': 'These neighbourhoods are searched by name but share an MLS® sub-area with a larger one, so they have a guide of their own.', 'gen': 'gaplink', 'pos': 'end'},
                        {'t': 'list', 'items': [[{'t': f'{n} neighbourhood guide', 'h': f'/{s}.html'}, {'t': f' ({why})'}] for n, s, why in items], 'gen': 'gaplink', 'pos': 'end'}]
        save(p, d)
    print('guides written:', [g['slug'] for g in GUIDES], '| parent links:', len(PARENT), '| hubs:', len(HUB))


if __name__ == '__main__': main()
