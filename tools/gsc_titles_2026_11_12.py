#!/usr/bin/env python3
"""D-232: titles for the pages that earn search clicks, written from their Search Console queries.

Jared chose the new (D-221) titles over the archived ones (Nov 12). Search Console (3 months to Nov 11, 2026, query report
filtered to each page; 152 of the 171 pages with clicks read, the rest hit Google's rate limit and have 1 click each)
shows which words each page is found by. Where a new title dropped those words ("manufactured homes", "court ordered
sales", "Ruskin Place", "Breakaway Bays", "ocean view"), the line below puts them back; otherwise the new title stands.
This replaces tools/protect_top_pages_2026_11_12.py (D-231), which had restored the archived titles.
python3 -I tools/gsc_titles_2026_11_12.py"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PAGES = {   # slug: title  (main search phrasing in the comment)
 'langley-mobile-homes': 'Langley Mobile & Manufactured Homes for Sale | Pad Rent',            # mobile homes for sale langley; manufactured homes for sale langley
 'mission-mobile-homes': 'Mission Mobile Homes for Sale | Ruskin Place & Parks',              # ruskin place mobile home park (8 clicks)
 'langley-foreclosures-court-ordered-sales': 'Langley Foreclosures & Court Ordered Sales | Homes for Sale',  # court ordered sale langley bc
 'abbotsford-mobile-homes': 'Abbotsford Mobile & Manufactured Homes for Sale | 55+ Parks',   # manufactured homes for sale (198 impr.)
 'langley-horse-properties-equestrian-farms-for-sale-mls-listings': 'Langley Horse Properties & Equestrian Farms for Sale',
 'our-listings': 'Jared Gibbons Listings | Active & Sold Homes',                             # jared gibbons
 'broiler-farms-for-sale-bc': 'Broiler & Chicken Farms for Sale BC | Quota & Barns',        # chicken farm for sale bc
 'abbotsford-farms': 'Abbotsford Farms for Sale | Small Farms & ALR Land',                  # farms for sale abbotsford; small farm for sale
 'surrey-mobile-homes': 'Surrey Mobile & Manufactured Homes for Sale | Parks',
 'campbell-valley-acreages-farms-for-sale': 'Campbell Valley Acreages & Farms for Sale | South Langley',  # south langley real estate
 'south-surrey-open-houses': 'South Surrey Open Houses This Weekend | Surrey & White Rock',  # open house surrey; open house near me
 'mobile-home-parks-fraser-valley': 'Fraser Valley Mobile Home Parks | Homes for Sale & Pad Rent',
 'zonings': 'Zoning Guide BC: A1, A2, RS3 | Langley, Surrey, Abbotsford',                  # a1/a2/rs3 zoning abbotsford
 'surreyforeclosuresandcourtsales': 'Surrey Foreclosures & Court Ordered Sales | Homes for Sale',
 'langley-farms-for-sale-acreages-agricultural-land-mls': 'Langley Farms for Sale | Acreages & Agricultural Land',
 'langley-poultry-farms-for-sale': 'Langley Poultry & Chicken Farms for Sale | Quota & Barns',
 'south-surrey-mobile-homes': 'South Surrey Mobile Homes for Sale | Breakaway Bays & Parks',
 'cost-of-mobile-home-pad-rental-fees-in-langley': 'Langley Mobile Home Pad Rent | Pad Rental Fees Explained',  # pad rental bc; what is pad rent
 'cloverale-foreclosures-court-ordered-sales': 'Cloverdale Foreclosures & Court Ordered Sales | Surrey',
 'poultry-farms-for-sale-bc': 'Poultry Farms for Sale BC | Chicken, Turkey & Egg Farms',
 'lake-errock': 'Lake Errock Homes & Cabins for Sale | Waterfront, Mission',
 'clayton-guide': 'Living in Clayton & East Clayton, Surrey: Plans & Schools',
 'murrayville': 'Murrayville Homes for Sale, Langley | Houses & Condos',
 'white-rock': 'White Rock Homes for Sale | Ocean View, Condos & Uptown',                 # ocean view homes white rock bc
 'maple-ridge-farms': 'Maple Ridge Farms & Acreage for Sale | ALR & Equestrian',
 'langley-farms': 'Langley Farms for Sale: ALR Rules & Farmland Buying Guide',
 'south-surrey-white-rock-55-plus-condos-for-sale': 'South Surrey & White Rock 55+ Condos for Sale | Updated Daily',
 'queensborough': 'Queensborough Real Estate | Homes for Sale, New Westminster',          # queensborough real estate (110 impr.)
 'surrey-farms': 'Surrey Farms & Agricultural Land for Sale | ALR Checks',
 'sold-properties': 'Recently Sold Homes in Surrey & Langley | Jared Gibbons',
 'thornhill-maple-ridge-guide': 'Thornhill, Maple Ridge Homes & Guide | Urban Reserve Rules',
 'langleycity': 'Langley City Development Map, OCP & Zoning Maps',
}
POSTS = {
 'how-poultry-quota-works-in-bc-chicken-egg-and-turkey-farms-explained-9126255': 'How Poultry Quota Works in BC: Chicken, Egg & Turkey',
 'guide-to-buying-land-in-bcs-alr-realtor-jared-gibbons-8864007': 'Buying ALR Land in BC: Agricultural Land Reserve Guide',
 '20-avenue-overpass-at-highway-99-major-south-surrey-traffic-upgrade--8895555': '20 Avenue Overpass at Highway 99 | South Surrey Traffic',
 'ocean-park-townhomes-89-new-units-at-128-street-24-avenue-surrey-8969237': 'Ocean Park Townhomes: 89 New Units at 128 St & 24 Ave',
 'sold-commercial-space-richmond-realtor---just-sold-thr-8485931': 'Sold: Richmond Coin Laundry & Laundromat Business',
}
# start from the D-221 titles (before the D-231 restore), then apply the lines above
def at(rev, path): return json.loads(subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True))
REV = '379b7cd8~1'
for path, table in (('src/data/seo-final.json', PAGES), ('src/data/post-listing-seo.json', POSTS)):
    cur = json.load(open(path)); base = at(REV, path); n = 0
    for k in cur:
        if k in base and cur[k].get('title') != base[k].get('title'): cur[k]['title'] = base[k]['title']; n += 1   # undo D-231
    for k, t in table.items():
        assert k in cur, k
        assert len(t) <= 66, (k, len(t))
        cur[k]['title'] = t
    json.dump(cur, open(path, 'w'), ensure_ascii=False, indent=1)
    print(path, 'D-231 restores undone', n, '| GSC titles set', len(table))
