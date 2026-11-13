#!/usr/bin/env python3
"""White Rock pages (D-273; the Princeton pages were removed in D-274: no MyRealPage search can cover the Interior board).

Three new pages and a stronger White Rock guide, written by hand from the sources listed on each page (read November 13, 2026):

    python3 -I tools/build_wr_pages.py   -> src/data/local/<slug>.json

White Rock: condo buildings (tower by tower), waterfront (Marine Drive) and hillside / ocean view homes, plus new sections on
white-rock-guide (its archive body stays). The live listing box on each new page
is empty until Gerry's MyRealPage saved search is wired in src/data/idx-embeds.json (docs/review/idx/wr-searches-2026-11-13.xlsx).
Text uses the post-rewrite markup: [text](url) is a link and **text** is bold.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from build_post_rewrites import parts  # noqa: E402

LOCAL = ROOT / 'src/data/local'
DAY = '2026-11-13'
G = 'wrp'


def P(text):
    return {'t': 'p', 'parts': parts(text), 'gen': G} if ('[' in text or '**' in text) else {'t': 'p', 'text': text, 'gen': G}


def H(text, level=2):
    return {'t': 'h', 'level': level, 'text': text, 'gen': G}


def L(*items):
    return {'t': 'list', 'items': [parts(i) for i in items], 'gen': G}


def T(caption, head, rows, source):
    return {'t': 'table', 'caption': caption, 'head': head, 'rows': rows, 'source': source, 'gen': G}


def NOTE(text):
    return {'t': 'notice', 'text': 'Draft for Jared’s approval. ' + text, 'gen': G}


GRID = {'t': 'grid', 'gen': G}
SOLD = 'Source: Paragon closed and pending sales, November 1, 2025 to October 31, 2026.'
WR_INFO = 'https://www.whiterockcity.ca/390/Info-on-New-Major-Developments'
FAQ_SHOW = {'q': 'Can I book a private showing with Jared?', 'a': 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.', 'gen': G}


def page(slug, title, desc, h1, crumbs, blocks, faq, faq_heading):
    assert len(title) <= 60, (slug, len(title))
    assert len(desc) <= 155, (slug, len(desc))
    return {'status': 'draft', 'slug': slug, 'updated': DAY, 'hand_edited': True, 'wrp_page': True,
            'new_page': {'title': title, 'description': desc, 'h1': h1},
            'breadcrumbs': [{'name': 'Home', 'href': '/'}] + [{'name': n, 'href': h} for n, h in crumbs] + [{'name': h1.split(',')[0] if len(h1) > 40 else h1, 'href': f'/{slug}.html'}],
            'faq_heading': faq_heading, 'faq': [dict(f, gen=G) for f in faq] + [FAQ_SHOW], 'blocks': blocks}


PAGES = []

# ---------------------------------------------------------------- White Rock: condo buildings
PAGES.append(page(
    'white-rock-condo-buildings',
    'White Rock Condo Buildings: Tower-by-Tower Guide',
    'White Rock condo towers compared: storeys, homes and builders at Soleil, Foster Martin, Miramar Village, Altus, Semiah, Monaco and The Beverley.',
    'White Rock Condo Buildings, Tower by Tower',
    [('White Rock condos', '/white-rock-condos-for-sale.html')],
    [
        NOTE('Building figures are from the City of White Rock’s development info sheets, read November 13, 2026. The live search is not connected yet.'),
        P('Most of White Rock’s newer condos are in a few blocks of the Town Centre, around Johnston Road, Thrift Avenue, Foster Street and Martin Street, uphill from the beach. The City publishes an info sheet for each major project with its height, number of homes and shop space. Here is what each tower is, side by side, so you can narrow the search before a showing.'),
        GRID,
        H('White Rock’s condo towers at a glance'),
        T('White Rock condo towers from the City’s development info sheets',
          ['Building', 'Address', 'Storeys', 'Homes', 'Builder', 'Street level'],
          [['Soleil', '1588 Johnston Road', '26', '178 apartments', 'RDG', '24,600 sq ft of shops'],
           ['Foster Martin (three towers)', '1484 Martin Street', '25, 25 and 24', '345 apartments', 'Landmark Premiere Properties', 'About 56,000 sq ft, 8 shops'],
           ['Miramar Village (later towers)', '15177 Thrift Avenue', '15 and 16', '229 apartments', 'Bosa Properties', 'About 50,000 sq ft, 14 shops'],
           ['Semiah', '15241 Thrift Avenue', '14', '88 apartments', 'Marcon', 'Residential only'],
           ['Altus', '1556 Finlay Street', '13', '126 apartments (16 rental)', 'Oviedo Developments', 'About 47,500 sq ft, 9 shops'],
           ['The Beverley', '1501 Vidal Street', '13', '88 apartments', 'Cressey', 'Residential only'],
           ['Monaco', '1350 Johnston Road', '12', '97 apartments', 'Solterra', 'About 10,000 sq ft, 6 shops'],
           ['Fantom', '14825 Thrift Avenue', '10', '25 apartments', 'Forge Properties', 'Residential only']],
          'Source: City of White Rock, Info on New Major Developments, info sheets 1 to 5. Strata addresses can differ from the project address (Semiah units are numbered on George Street, for example).'),
        P('Two more towers are rentals, so their homes are not sold one by one: Oceana PARC at 1575 George Street (23 storeys, 198 rental apartments, opened September 2019) and Verve at 1456 Johnston Road (6 storeys, 29 rental apartments). The City also lists Nautilus at 1454 Oxford Street, approved at 21 and 24 storeys with 121 apartments; ask the City for its current status.'),
        H('Which White Rock building fits you'),
        L('**Height and views:** Soleil (26 storeys) and the three Foster Martin towers (24 to 25) are the tallest on the City’s list. Upper floors facing south look over Semiahmoo Bay.',
          '**A smaller building:** Fantom has 25 homes on 10 storeys; The Beverley and Semiah have 88 each and no shops below.',
          '**Shops downstairs:** Soleil, Foster Martin, Miramar Village, Altus and Monaco have retail at street level. Handy for errands; ask how costs are split between the residential and commercial parts of the strata.',
          '**Rentals in the building:** Altus set aside 16 rental homes. Since November 24, 2022, BC stratas can no longer ban owners from renting, so any building may have tenants.'),
        H('What White Rock condos sell for'),
        P('Between November 1, 2025 and October 31, 2026, 251 condos sold in White Rock at a median of $542,000; the middle half sold between $460,000 and $843,500, at a median of $512 a square foot and 33 days on the market. Tower suites with views and new-build finishes sit at the top of that range. For prices by size, see [1 bedroom condos](/white-rock-1-bedroom-condos-for-sale.html) and [2 bedroom condos](/white-rock-2-bedroom-condos-for-sale.html) in White Rock.'),
        H('Before you buy in a White Rock tower'),
        L('**Read the strata package:** the Form B, two years of minutes, the bylaws, the depreciation report and the contingency reserve fund. They show levies coming and what the fee covers.',
          '**Check parking and storage:** confirm which stall and locker belong to the unit, and whether they are limited common property or assigned by the strata.',
          '**Look at what is approved nearby:** a view can change when the next tower goes up. The City lists approved projects on its [major developments page](' + WR_INFO + ').',
          '**Age and pets:** the only age rule a BC strata can now set is 55 and over. Pet limits are allowed, so read the bylaws if you have a dog.'),
        H('More White Rock homes'),
        L('[White Rock condos for sale](/white-rock-condos-for-sale.html)',
          '[White Rock waterfront homes on Marine Drive](/white-rock-waterfront-homes-for-sale.html)',
          '[White Rock hillside and ocean view homes](/white-rock-hillside-homes-for-sale.html)',
          '[Penthouses in White Rock and South Surrey](/south-surrey-white-rock-penthouses-for-sale.html)',
          '[Living in White Rock: the guide](/white-rock-guide.html)'),
        H('Sources'),
        L('[City of White Rock: Info on New Major Developments](' + WR_INFO + ')',
          '[BC Financial Services Authority: BC ends rental and age restrictions in strata properties](https://bcfsa.ca/about-us/news/news-release/bc-government-ends-rental-and-age-restrictions-strata-properties)',
          SOLD.replace('Source: ', '')),
    ],
    [{'q': 'What is the tallest building in White Rock?', 'a': 'Of the projects on the City of White Rock’s development info sheets, Soleil at 1588 Johnston Road is the tallest at 26 storeys, followed by the three Foster Martin towers at 25, 25 and 24 storeys.'},
     {'q': 'How many homes are in Foster Martin?', 'a': 'The City’s info sheet lists 345 apartments in three towers of 25, 25 and 24 storeys at 1484 Martin Street, built by Landmark Premiere Properties, with about 56,000 sq ft of shops.'},
     {'q': 'Can a White Rock strata ban rentals?', 'a': 'No. Since November 24, 2022, BC strata corporations cannot have bylaws that stop owners renting their units, and the only age restriction allowed is 55 and over.'},
     {'q': 'What do White Rock condos sell for?', 'a': 'From November 2025 to October 2026, 251 White Rock condos sold at a median of $542,000, with the middle half between $460,000 and $843,500.'}],
    'White Rock condo buildings: your questions answered'))

# ---------------------------------------------------------------- White Rock: waterfront
PAGES.append(page(
    'white-rock-waterfront-homes-for-sale',
    'White Rock Waterfront Homes for Sale | Marine Drive',
    'White Rock waterfront homes on Marine Drive, East Beach and West Beach: the rail line, flood levels, the pier and what to check before you buy.',
    'White Rock Waterfront Homes for Sale',
    [('White Rock homes', '/white-rock.html')],
    [
        NOTE('Facts are from the City of White Rock, read November 13, 2026. The live search is not connected yet.'),
        P('White Rock’s waterfront is Marine Drive: about two kilometres of road between East Beach and West Beach, with the promenade and the sandy beach of Semiahmoo Bay below it and homes stepping up the slope behind. This search covers White Rock homes on and just above Marine Drive. For Crescent Beach and Ocean Park in Surrey, see [waterfront homes in White Rock and South Surrey](/south-surrey-white-rock-waterfront-homes-for-sale.html).'),
        GRID,
        H('East Beach, West Beach and the pier'),
        L('**The pier** splits the two beaches. It is 470 metres long, first built in 1914/15, and a December 20, 2018 storm destroyed a third of it; the repaired section reopened in 2019. The federal government has approved in principle $25,935,000 toward replacing the rest.',
          '**The promenade** runs about 2.19 km, almost the length of the beach. Biking, skating and smoking are not allowed on it, and dogs on leash are allowed only from October 1 to March 31.',
          '**West Beach** is the busier end, with restaurants along Marine Drive near the pier. **East Beach** runs toward the Semiahmoo First Nation lands, which are governed separately and sit inside Surrey’s borders.'),
        H('The railway in front of every Marine Drive home'),
        P('A single BNSF track runs between Marine Drive and the beach. It operates 24 hours a day and carries freight and Amtrak passenger trains. People reach the beach at eight gated crossings: Bay, Anderson, Oxford and the Pier on West Beach, and Cypress, Balsam, Ash and Finlay on East Beach. Since January 29, 2020, after 16 safety gates went in, BNSF crews have been under an order not to sound horns at those crossings, except for people or animals on the tracks. Listen for trains at a showing, day and night.'),
        H('Flood levels and rules'),
        L('White Rock sets its own rules, separate from Surrey: **Zoning Bylaw 2024, No. 2506** (adopted June 27, 2024) and **Official Community Plan Bylaw 2017, No. 2220**, which includes a Waterfront Development Permit Area.',
          'A City report describes an **ocean floodplain level of 3.9 m geodetic** and a Campbell River floodplain level of 4.6 m, overlapping in the city’s southeast corner. Ask the City how either applies before you plan to rebuild or add on.',
          'Most Marine Drive lots are on a slope, so check retaining walls, drainage and the stairs from the road as closely as the view.'),
        H('What White Rock homes sell for'),
        P('Between November 1, 2025 and October 31, 2026, 95 detached houses sold in White Rock at a median of $1,565,000 (middle half $1,257,500 to $2,033,095), and 251 condos at $542,000. Waterfront and view homes sell at the top of those ranges, and few come up in a year, so it pays to have a search saved before one lists.'),
        H('More White Rock homes'),
        L('[White Rock hillside and ocean view homes](/white-rock-hillside-homes-for-sale.html)',
          '[White Rock condo buildings, tower by tower](/white-rock-condo-buildings.html)',
          '[Waterfront homes in White Rock and South Surrey](/south-surrey-white-rock-waterfront-homes-for-sale.html)',
          '[Crescent Beach homes for sale](/crescent-beach-homes-for-sale.html)',
          '[Living in White Rock: the guide](/white-rock-guide.html)'),
        H('Sources'),
        L('[City of White Rock: Pier and Promenade](https://www.whiterockcity.ca/401/Pier-Promenade)',
          '[City of White Rock: Rail in White Rock](https://www.whiterockcity.ca/408/Rail-in-White-Rock)',
          '[City of White Rock: Zoning Bylaw 2024, No. 2506](https://whiterockcity.ca/DocumentCenter/View/8003/Zoning-Bylaw-2024-No-2506-Adopted-June-27-2024)',
          SOLD.replace('Source: ', '')),
    ],
    [{'q': 'Will trains sound their horns outside a Marine Drive home?', 'a': 'Not routinely at the promenade crossings. Since January 29, 2020, BNSF crews have been under an order not to sound horns at White Rock’s eight crossings, after 16 safety gates were installed. They still sound the horn for people or animals on the tracks.'},
     {'q': 'Is White Rock’s waterfront in a floodplain?', 'a': 'Parts of it. A City of White Rock report describes an ocean floodplain level of 3.9 m geodetic and a Campbell River floodplain level of 4.6 m in the southeast corner. Check the lot with the City before you plan to build.'},
     {'q': 'Can I walk my dog on the White Rock promenade?', 'a': 'On a leash from October 1 to March 31 only. Dogs are never allowed on the pier.'},
     {'q': 'What do houses in White Rock sell for?', 'a': 'From November 2025 to October 2026, 95 detached houses sold in White Rock at a median of $1,565,000; the middle half sold between $1,257,500 and $2,033,095.'}],
    'White Rock waterfront homes: your questions answered'))

# ---------------------------------------------------------------- White Rock: hillside / ocean view
PAGES.append(page(
    'white-rock-hillside-homes-for-sale',
    'White Rock Hillside & Ocean View Homes for Sale',
    'Ocean view homes on White Rock’s hillside, between Marine Drive and Uptown: prices, slopes, views, trees and what the zoning lets you build.',
    'White Rock Hillside and Ocean View Homes',
    [('White Rock homes', '/white-rock.html')],
    [
        NOTE('Facts are from the City of White Rock, read November 13, 2026. The live search is not connected yet.'),
        P('White Rock climbs from the beach to North Bluff Road, so most of the city’s houses sit on a slope facing Semiahmoo Bay. This search covers White Rock houses and townhomes listed with an ocean or water view, from the streets just above Marine Drive up to Uptown. For Ocean Park and the Surrey bluff, see [ocean view homes in White Rock and South Surrey](/south-surrey-white-rock-ocean-view-homes-for-sale.html).'),
        GRID,
        H('What you get on the hillside'),
        L('**The view is the price.** Two houses a street apart can differ by hundreds of thousands of dollars for what is in front of them. Stand in each main room and on the deck, not just at the front door.',
          '**Steep lots** mean stairs, retaining walls and steep driveways. Check the drainage and who owns and maintains each wall.',
          '**Walking distance** to both the beach and the Uptown shops on Johnston Road is the draw; walking back up the hill is the trade-off.'),
        H('What can be built in front of your view'),
        L('**Zoning:** White Rock’s Zoning Bylaw 2024, No. 2506 governs, not Surrey’s. The bylaw lists rezonings since adoption, including several RS-1 lots rezoned to RS-2 to allow two-lot subdivisions, so the lot below may not stay one house.',
          '**More homes per lot:** the single-family zones carry the Province’s small-scale multi-unit housing rules, so a neighbour may add a suite or units. Read the zone for the lot below as well as your own.',
          '**The plan is changing:** White Rock’s Official Community Plan is being updated (draft amending Bylaw No. 2511, and Bylaw 2593 in September 2026 with a North Bluff Corridor Plan update). Ask what is proposed near the house.',
          '**There is no general legal right to a view** in BC. Only a covenant or easement registered on title protects one, so check the title search.'),
        H('What White Rock houses sell for'),
        P('Between November 1, 2025 and October 31, 2026, 95 detached houses sold in White Rock at a median of $1,565,000, or $595 a square foot, after a median of 39 days on the market. The middle half sold between $1,257,500 and $2,033,095; view homes are mostly in the upper half.'),
        H('More White Rock homes'),
        L('[White Rock waterfront homes on Marine Drive](/white-rock-waterfront-homes-for-sale.html)',
          '[White Rock condo buildings, tower by tower](/white-rock-condo-buildings.html)',
          '[White Rock and South Surrey houses for sale](/white-rock-south-surrey-houses-for-sale.html)',
          '[Luxury homes in White Rock and South Surrey](/luxury-homes-for-sale-in-white-rock-south-surrey.html)',
          '[Living in White Rock: the guide](/white-rock-guide.html)'),
        H('Sources'),
        L('[City of White Rock: Zoning Bylaw 2024, No. 2506](https://whiterockcity.ca/DocumentCenter/View/8003/Zoning-Bylaw-2024-No-2506-Adopted-June-27-2024)',
          '[City of White Rock: Official Community Plan Bylaw 2017, No. 2220 (consolidated)](https://www.whiterockcity.ca/DocumentCenter/View/276/Consolidated---Official-Community-Plan-Bylaw-2017-Number-2220-PDF)',
          SOLD.replace('Source: ', '')),
    ],
    [{'q': 'Can my ocean view be protected?', 'a': 'Only by something registered on title, such as a view covenant or easement. BC law gives no general right to a view, so check the title search and ask what the zoning allows on the lots below.'},
     {'q': 'What can my neighbour build below me in White Rock?', 'a': 'Whatever their zone allows under White Rock Zoning Bylaw 2024, No. 2506, including the small-scale multi-unit housing provisions and any rezoning. Several RS-1 lots have been rezoned to RS-2 for two-lot subdivisions.'},
     {'q': 'What does an ocean view house cost in White Rock?', 'a': 'From November 2025 to October 2026, White Rock’s 95 detached sales had a median of $1,565,000 and a middle half of $1,257,500 to $2,033,095. View homes are mostly in the upper half.'}],
    'White Rock hillside homes: your questions answered'))

# ---------------------------------------------------------------- white-rock-guide: new sections on the archive page
WR_GUIDE_BLOCKS = [
    H('White Rock in four parts'),
    L('**West Beach:** the pier end of Marine Drive, with restaurants facing the water and the busiest stretch of the promenade.',
      '**East Beach:** the quieter end of the promenade toward the Semiahmoo First Nation lands and the Campbell River.',
      '**Town Centre and Uptown:** Johnston Road, Thrift Avenue and North Bluff Road, where the towers are: Soleil, Foster Martin, Miramar Village and others. See the [condo buildings guide](/white-rock-condo-buildings.html).',
      '**The hillside:** the residential streets between the beach and Uptown, mostly houses on sloping lots facing Semiahmoo Bay. See [hillside and ocean view homes](/white-rock-hillside-homes-for-sale.html).'),
    H('What White Rock homes sold for'),
    T('White Rock houses and condos sold, November 2025 to October 2026', ['Measure', 'Detached houses', 'Condos'],
      [['Sales', '95', '251'], ['Median price', '$1,565,000', '$542,000'], ['Middle half of prices', '$1,257,500 to $2,033,095', '$460,000 to $843,500'], ['Days to sell (median)', '39', '33']], SOLD),
    P('Condos are more than two thirds of White Rock sales. For the waterfront, see [White Rock waterfront homes on Marine Drive](/white-rock-waterfront-homes-for-sale.html).'),
]


def main():
    for d in PAGES:
        (LOCAL / f"{d['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
        print('wrote', d['slug'])
    f = LOCAL / 'white-rock-guide.json'
    g = json.loads(f.read_text())
    g['blocks'] = [b for b in g['blocks'] if b.get('gen') != G] + []
    # new sections go before the generated ones (the loader puts local blocks without pos ahead of the archive's first h2)
    g['blocks'] = WR_GUIDE_BLOCKS + g['blocks']
    g['updated'] = DAY
    f.write_text(json.dumps(g, ensure_ascii=False, indent=1) + '\n')
    print('updated white-rock-guide')


if __name__ == '__main__':
    main()
