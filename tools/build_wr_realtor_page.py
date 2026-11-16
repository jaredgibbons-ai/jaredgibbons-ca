#!/usr/bin/env python3
"""White Rock realtor page (D-305). Search Console, 28 days to Nov 13 2026: "white rock realtor", "white rock real estate agent",
"realtor white rock" and "real estate agent white rock" bring about 350 impressions at positions 6.5 to 11.5, answered by the
homepage because no page targets them.

    python3 -I tools/build_wr_realtor_page.py   -> src/data/local/white-rock-realtor.json

Every fact is one already published on this site: the sold streets and buildings come from src/data/sold-streets.js (closed MLS
sales with Jared as listing agent; names only, no counts), the price table from the White Rock guide (Paragon, Nov 2025 to Oct 2026),
the recognition lines from the South Surrey agent page.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from build_wr_pages import P, H, L, T, GRID, SOLD, page, LOCAL  # noqa: E402

SLUG = 'white-rock-realtor'
STREETS = 'Buena Vista Avenue · Fir Street · Marine Drive · North Bluff Road · Parker Street · Royal Avenue · Russell Avenue · Thrift Avenue · Victoria Avenue'

BLOCKS = [
    P('I\'m Jared Gibbons, a REALTOR® with Royal LePage Little Oak Realty. I have sold homes in White Rock and South Surrey since 2015: condos in the Uptown towers, houses on the hillside and homes along Marine Drive. My office is on Croydon Drive in South Surrey, a short drive from Uptown White Rock.'),
    L('[What is my White Rock home worth?](/home-evaluation.html)', '[Call or text 604-928-1361](tel:+16049281361)', '[White Rock homes for sale](/white-rock.html)'),
    H('Why White Rock sellers and buyers hire me'),
    L('**#1 in South Surrey & White Rock** by FVREB Medallion Club points (2025 & 2026 YTD).',
      '**Top 1% of all REALTORS® in the Fraser Valley**, with 10 straight years in the FVREB Medallion Club.',
      '**94 Google reviews, 5.0 average.** [Read every one](/reviews.html).',
      '**REALTOR® since 2015** with Royal LePage Little Oak Realty, on Croydon Drive in South Surrey.'),
    H('Where I have sold in White Rock'),
    P('I have sold homes on these White Rock streets as the listing agent. If yours is one of them, I already know what buyers there pay for.'),
    P(STREETS),
    P('**Buildings and complexes:** Allure, Beachborough, [Belaire](/belaire-white-rock-condos.html), [Miramar Village](/miramar-village-white-rock-condos.html), The Arcadian, The Heritage, The Pauline, Victoria Terrace and Windermere.'),
    P('Closed MLS® sales with Jared as the listing agent, 2017 to November 2026. Street and building names only. [See the homes I have sold](/sold-properties.html).'),
    H('White Rock homes for sale now'),
    GRID,
    H('What White Rock homes sell for'),
    T('White Rock houses and condos sold, November 2025 to October 2026', ['Measure', 'Detached houses', 'Condos'],
      [['Sales', '95', '251'], ['Median price', '$1,565,000', '$542,000'], ['Middle half of prices', '$1,257,500 to $2,033,095', '$460,000 to $843,500'], ['Days to sell (median)', '39', '33']], SOLD),
    P('Condos are more than two thirds of White Rock sales, so most of my work here is strata: reading the minutes, the depreciation report and the bylaws before a price goes on a home or an offer goes in. Monthly numbers are on the [South Surrey and White Rock market stats](/south-surrey-white-rock-real-estate-market-stats.html) page.'),
    H('Selling a home in White Rock'),
    L('**Price from the nearest sales, not a city average.** A West Beach condo, a Town Centre tower unit and a hillside house with a view are three different markets.',
      '**The view is part of the price.** I check what can be built in front of it before we list. See [hillside and ocean view homes](/white-rock-hillside-homes-for-sale.html).',
      '**White Rock is its own city.** It has its own zoning bylaw, council and property tax, separate from Surrey. You can [check an address\'s zoning](/zonings.html#zd-lookup) in a few seconds.',
      '**Full marketing on every listing:** professional photos and drone, video, laser-measured floor plans, a 3D tour and paid advertising. [See the marketing plan](/selling.html).'),
    P('Start with a price range: [request a free home evaluation](/home-evaluation.html) and I reply the same day.'),
    H('Buying a home in White Rock'),
    L('[White Rock condo buildings, tower by tower](/white-rock-condo-buildings.html)',
      '[White Rock condos for sale](/white-rock-condos-for-sale.html), including [1 bedroom](/white-rock-1-bedroom-condos-for-sale.html) and [2 bedroom](/white-rock-2-bedroom-condos-for-sale.html) condos',
      '[Waterfront homes on Marine Drive](/white-rock-waterfront-homes-for-sale.html)',
      '[Hillside and ocean view homes](/white-rock-hillside-homes-for-sale.html)',
      '[Houses in White Rock and South Surrey](/white-rock-south-surrey-houses-for-sale.html)',
      '[Living in White Rock: the neighbourhood guide](/white-rock-guide.html)'),
    H('White Rock in four parts'),
    L('**West Beach:** the pier end of Marine Drive, with restaurants facing the water and the busiest stretch of the promenade.',
      '**East Beach:** the quieter end of the promenade toward the Semiahmoo First Nation lands and the Campbell River.',
      '**Town Centre and Uptown:** Johnston Road, Thrift Avenue and North Bluff Road, where the towers are.',
      '**The hillside:** the residential streets between the beach and Uptown, mostly houses on sloping lots facing Semiahmoo Bay.'),
    P('I work in both cities. See [South Surrey Realtor Jared Gibbons](/south-surrey-real-estate-agent-jared-gibbons-realtor.html).'),
]

FAQ = [
    {'q': 'Who is a top realtor in White Rock?', 'a': 'Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, is #1 in South Surrey & White Rock by FVREB Medallion Club points (2025 & 2026 YTD) and in the Top 1% of all REALTORS® in the Fraser Valley, with 10 straight years in the FVREB Medallion Club and 94 Google reviews.'},
    {'q': 'Does Jared Gibbons sell condos in White Rock?', 'a': 'Yes. Condos are more than two thirds of White Rock sales. Jared has sold in Allure, Beachborough, Belaire, Miramar Village, The Arcadian, The Heritage, The Pauline, Victoria Terrace and Windermere, and reviews the strata minutes, depreciation report and bylaws on every condo.'},
    {'q': 'Is White Rock part of Surrey?', 'a': 'No. The City of White Rock is a separate municipality with its own council, zoning bylaw and property tax. It is surrounded by South Surrey and shares Surrey Schools (School District 36).'},
    {'q': 'What do homes in White Rock sell for?', 'a': 'From November 2025 to October 2026 the median detached house in White Rock sold for $1,565,000 and the median condo for $542,000 (Paragon MLS® data). Prices vary a lot by view, building and distance from the beach.'},
    {'q': 'How do I find out what my White Rock home is worth?', 'a': 'Send the address through the home evaluation form or call or text 604-928-1361. Jared looks at the closest recent sales to your home, not a city average, and replies the same day with a price range.'},
]


def main():
    d = page(SLUG, 'White Rock Realtor Jared Gibbons | Top 1% Fraser Valley',
             'White Rock REALTOR® Jared Gibbons: condos, hillside and Marine Drive homes sold since 2015. 94 Google reviews, 5.0. Call or text 604-928-1361.',
             'White Rock Realtor Jared Gibbons', [('White Rock', '/white-rock.html')], BLOCKS, FAQ, 'White Rock realtor: your questions answered')
    d['updated'] = '2026-11-15'
    (LOCAL / f'{SLUG}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    print('wrote', SLUG)


if __name__ == '__main__':
    main()
