"""D-374: fourth batch of core pages. Chrome was not reachable, so there is no per-page Search Console query data; the changes follow
what D-366 to D-372 measured across 40 pages (people search "townhouse(s)", "real estate", "for sale" with the city name).
Run once from the repo root: python3 tools/core_pages_4_2026_11_19.py
"""
import json
SEO = {
    'city-of-langley-townhomes-for-sale': ('Townhouses for Sale in Langley City | City of Langley Homes', 'City of Langley Townhouses and Townhomes for Sale'),
    'cloverdale-townhomes-under-1-2m': ('Cloverdale Townhouses Under $1.2M | Clayton & Town Centre', 'Cloverdale Townhouses for Sale Under $1.2M'),
    'south-surrey-duplexes-with-suites-for-sale': ('South Surrey Duplexes with Suites for Sale | Suite Rules', None),
    'cedar-hills-surrey-houses-for-sale': ('Cedar Hills Houses for Sale, North Surrey | R3 Lots & Suites', 'Cedar Hills, Surrey Houses for Sale'),
    'fraser-heights-surrey-houses-for-sale': ('Fraser Heights Houses for Sale, Surrey | Abbey Ridge Lots', 'Fraser Heights, Surrey Houses for Sale'),
    'salmon-river-houses-for-sale': ('Salmon River Houses for Sale, Langley | Rural Homes & Wells', 'Salmon River, Langley Houses for Sale'),
}
p = 'src/data/seo-final.json'
raw = open(p).read(); sf = json.loads(raw)
assert json.dumps(sf, ensure_ascii=False, indent=1) == raw
for slug, (t, h) in SEO.items():
    assert len(t) <= 60, (slug, len(t)); sf[slug]['title'] = t
    if h: sf[slug]['h1'] = h
open(p, 'w').write(json.dumps(sf, ensure_ascii=False, indent=1))

# Blog: name the plan the way the Township does
p = 'src/data/post-listing-seo.json'
raw = open(p).read(); ps = json.loads(raw)
fmt = next((ind, ea, tail) for ind in (1, 2, None) for ea in (True, False) for tail in ('\n', '')
           if json.dumps(ps, ensure_ascii=ea, indent=ind) + tail == raw)
ps['langleys-future-fraser-hwy-employment-lands-plan-explained-8713026']['title'] = 'Fraser Highway Employment Lands Area Plan, Langley Explained'
open(p, 'w').write(json.dumps(ps, ensure_ascii=fmt[1], indent=fmt[0]) + fmt[2])
