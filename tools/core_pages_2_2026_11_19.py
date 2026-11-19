"""D-370: second batch of core pages matched to their real searches (Search Console, URL-prefix property,
Oct 22-Nov 18, bot searches removed). Edits src/data/seo-final.json and post-listing-seo.json in place.
Run once from the repo root: python3 tools/core_pages_2_2026_11_19.py
"""
import json

SEO = {
    # "cloverdale homes for sale" 23.7, "cloverdale real estate" 27.6
    'cloverdale-bc': ('Cloverdale Homes for Sale | Cloverdale Real Estate, Surrey', 'Cloverdale Homes for Sale and Real Estate', None),
    # "condos for sale white rock" 45, "apartment(s) for sale white rock"
    'white-rock-condos-for-sale': ('Condos for Sale in White Rock BC | Apartments & Towers', 'Condos and Apartments for Sale in White Rock, BC', None),
    # "farms for sale in langley bc" 22.8, "acreage for sale langley" 41-58
    'langley-farms-for-sale-acreages-agricultural-land-mls': ('Langley Farms & Acreages for Sale | Agricultural Land BC', 'Langley Farms and Acreages for Sale', None),
    # the farmland guide also opened "Langley Farms for Sale"; it now says what it is
    'langley-farms': ('Buying Farmland in Langley BC: ALR Rules & Farm Status', None, None),
    # "land for sale in langley bc" went to the farm page at 76-83
    'langley-lots-land': ('Land for Sale in Langley BC | Lots & Building Sites', 'Land and Lots for Sale in Langley, BC', None),
    # "ocean park new home construction" 23 impressions at 32
    'new-construction-crescent-bch-ocean-pk': ('Ocean Park & Crescent Beach New Construction Homes', 'New Construction Homes in Ocean Park and Crescent Beach', None),
    # "ocean view homes white rock bc" 29 at 40.8, "homes for sale white rock bc" 34.9, "white rock real estate" 56.6
    'white-rock': ('White Rock Homes for Sale | Ocean View Homes & Real Estate', 'White Rock Homes for Sale and Real Estate', None),
    # "surrey bc neighbourhoods" (46 impressions) went to the South Surrey guide page at 29.7
    'surrey-neighbourhood-guides': ('Surrey BC Neighbourhoods | Guides to 14 Areas Compared', 'Surrey BC Neighbourhood Guides', None),
    # "homes for sale north surrey" 46, "north surrey real estate"
    'north-surrey-homes-for-sale': ('North Surrey Homes for Sale | Real Estate & MLS® Listings', 'North Surrey Homes for Sale and Real Estate', None),
    # "langley presale condos" 36 impressions at 50.5
    'new-construction-presales-in-langley-bc': (None, 'Langley Presale Condos, Townhomes and New Homes', None),
    # "crescent beach real estate" 17 at 41.9; "crescent beach homes for sale" belongs to crescent-beach-homes-for-sale
    'crescent-bch-ocean-pk': ('Crescent Beach & Ocean Park Real Estate | South Surrey', 'Crescent Beach and Ocean Park Real Estate', None),
    # "willoughby homes for sale" belongs to willoughby-homes-for-sale
    'willoughby-heights': ('Willoughby Heights Real Estate | Langley Homes & Townhomes', 'Willoughby Heights Real Estate, Langley', None),
    # "surrey homes for sale" went to the houses page at 49.8; the homes page owns it
    'surrey-houses-for-sale': ('Houses for Sale in Surrey BC | Detached Homes by Price', 'Houses for Sale in Surrey, BC', None),
    # "fort langley real estate" 32.2; "fort langley houses for sale" belongs to fort-langley-houses-for-sale
    'fort-langley': ('Fort Langley Homes for Sale | Village Real Estate, Langley', 'Fort Langley Homes for Sale and Real Estate', None),
    # "townhouses for sale langley" 79, "townhouse for sale in langley bc" 62
    'langley-townhomes-for-sale': ('Townhouses for Sale in Langley BC | Townhomes & Complexes', 'Townhouses and Townhomes for Sale in Langley, BC', None),
}
sf_path = 'src/data/seo-final.json'
raw = open(sf_path).read(); sf = json.loads(raw)
assert json.dumps(sf, ensure_ascii=False, indent=1) == raw
for slug, (t, h, d) in SEO.items():
    rec = sf[slug]
    if t: assert len(t) <= 60, (slug, len(t)); rec['title'] = t
    if h: rec['h1'] = h
    if d: assert len(d) <= 158, (slug, len(d)); rec['description'] = d
open(sf_path, 'w').write(json.dumps(sf, ensure_ascii=False, indent=1))

# Blog: "south surrey" (21 at 30), "is white rock part of surrey", "white rock boundaries"
p = 'src/data/post-listing-seo.json'
raw = open(p).read(); ps = json.loads(raw)
k = 'south-surrey-vs-white-rock-which-neighbourhood-is-right-for-you-in-202-8941189'
ps[k]['title'] = 'South Surrey vs White Rock: Is White Rock Part of Surrey?'
fmt = next((ind, ea, tail) for ind in (1, 2, None) for ea in (True, False) for tail in ('\n', '')
           if json.dumps(json.loads(raw), ensure_ascii=ea, indent=ind) + tail == raw)
open(p, 'w').write(json.dumps(ps, ensure_ascii=fmt[1], indent=fmt[0]) + fmt[2])

# The post's new title asks "Is White Rock part of Surrey?", so the post answers it (same facts as the
# South Surrey neighbourhoods FAQ: own city since 1957, own council and zoning bylaw, SD36 schools).
p = 'src/data/post-context.json'
raw = open(p).read(); pc = json.loads(raw)
fmt = next((ind, ea, tail) for ind in (1, 2, None) for ea in (True, False) for tail in ('\n', '')
           if json.dumps(pc, ensure_ascii=ea, indent=ind) + tail == raw)
pc[k] = {'words': 0, 'area': 'south-surrey', 'topic': 'neighbourhoods', 'manual': True, 'blocks': [
    {'t': 'h', 'level': 2, 'text': 'Is White Rock part of Surrey?'},
    {'t': 'p', 'parts': [{'t': 'No. White Rock has been its own city since 1957, with its own council, property tax rates and zoning bylaw, so City of White Rock rules apply to a White Rock address. South Surrey is part of the City of Surrey. Both are served by Surrey Schools (SD36), so a White Rock address still goes to a Surrey public school.'}]},
    {'t': 'p', 'parts': [{'t': 'For the areas on each side, see the '}, {'t': 'South Surrey and White Rock neighbourhood guides', 'h': '/south-surrey-neighbourhoods.html'},
                         {'t': ', '}, {'t': 'White Rock homes for sale', 'h': '/white-rock.html'}, {'t': ' and '}, {'t': 'South Surrey homes for sale', 'h': '/south-surrey-homes-for-sale.html'}, {'t': '.'}]},
]}
open(p, 'w').write(json.dumps(pc, ensure_ascii=fmt[1], indent=fmt[0]) + fmt[2])
