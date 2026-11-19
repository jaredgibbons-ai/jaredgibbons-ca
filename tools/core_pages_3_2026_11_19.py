"""D-372: third batch of core pages matched to their real searches (Search Console, URL-prefix property,
Oct 22-Nov 18, bot searches removed). Edits src/data/seo-final.json in place.
Run once from the repo root: python3 tools/core_pages_3_2026_11_19.py
"""
import json

SEO = {
    # "notary public surrey prices" 16 impressions at 29.6; the page's table gives the published prices
    'real-estate-lawyer-notary-fees-langley-surrey-white-rock': (
        'Notary & Lawyer Fees in Surrey & Langley | Prices Compared', 'Notary and Lawyer Fees in Surrey, Langley and White Rock',
        'Notary and lawyer fees in Surrey, Langley and White Rock: published prices from $995 to $1,475 for a purchase with a mortgage, plus disbursements.'),
    # "house for sale in north surrey" 43.7, "houses for sale north surrey" 21.7
    'north-surrey-houses-for-sale': ('Houses for Sale in North Surrey | Fraser Heights & Guildford', 'Houses for Sale in North Surrey, BC', None),
    # "south surrey townhouses for sale", "townhouses for sale in south surrey", "rancher townhomes south surrey"
    'south-surrey-townhomes-for-sale': ('Townhouses for Sale in South Surrey BC | Townhomes & Strata', 'Townhouses and Townhomes for Sale in South Surrey, BC', None),
    # "townhouse for sale cloverdale" 66.4
    'cloverdale-townhomes-for-sale': ('Townhouses for Sale in Cloverdale BC | Clayton Townhomes', 'Townhouses and Townhomes for Sale in Cloverdale', None),
    # "townhouse for sale in surrey", "guildford townhouses for sale"
    'north-surrey-townhomes-for-sale': ('Townhouses for Sale in North Surrey | Guildford & Whalley', 'Townhouses and Townhomes for Sale in North Surrey', None),
    # "panorama surrey bc" (9 impressions at 45.6 on the guide, 8 at 44.8 on the condo page)
    'panorama-ridge-guide': ('Panorama Ridge, Surrey BC: Living in Panorama & Schools', 'Living in Panorama Ridge (Panorama), Surrey BC', None),
    # "buy new apartments in panorama ridge surrey" 16.7
    'panorama-ridge-surrey-condos-townhomes-for-sale': ('Panorama Ridge Condos, Apartments & Townhomes | Surrey', 'Panorama Ridge Condos, Apartments and Townhomes for Sale', None),
    # "houses for sale clayton heights", "clayton townhouses for sale"
    'clayton': ('Clayton Heights Homes for Sale | Surrey Houses & Townhouses', 'Clayton Heights Homes for Sale, Surrey', None),
    # "luxury real estate surrey" 16 at 36.4, "luxury homes in surrey bc" 28
    'south-surrey-luxury-homes': ('South Surrey Luxury Homes & Real Estate | Surrey BC Estates', 'Luxury Homes and Real Estate in South Surrey, BC', None),
    # "walnut grove real estate" 30, "walnut grove langley homes for sale" 19.5
    'walnut-grove': ('Walnut Grove Homes for Sale, Langley | Real Estate & Schools', None, None),
    # "new presale developments surrey", "home builders south surrey", "surrey new construction"
    'south-surrey-new-construction-presales': ('South Surrey Presales & New Construction | Homes & Townhomes', None, None),
}
p = 'src/data/seo-final.json'
raw = open(p).read(); sf = json.loads(raw)
assert json.dumps(sf, ensure_ascii=False, indent=1) == raw
for slug, (t, h, d) in SEO.items():
    rec = sf[slug]
    if t: assert len(t) <= 60, (slug, len(t)); rec['title'] = t
    if h: rec['h1'] = h
    if d: assert len(d) <= 158, (slug, len(d)); rec['description'] = d
open(p, 'w').write(json.dumps(sf, ensure_ascii=False, indent=1))
