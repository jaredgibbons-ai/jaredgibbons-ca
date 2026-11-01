#!/usr/bin/env python3
"""Writes src/data/seo-overrides.json: approved keyword titles (and matching H1 / description) for archive pages.
Archive JSON in src/data/pages is never edited; [...slug].astro applies these on top, so each change is reversible
by deleting its entry. Approved by Jared 2026-11-01 (D-60). Search volumes are unverified (Muse), so nothing here
quotes one; wording follows how the place is actually searched, not Muse's abbreviations."""
import json, sys
sys.dont_write_bytecode = True
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
def t(head):
    full = head + BR
    return full if len(full) <= 66 else head + BS
TAIL = ' View current MLS® listings, market data, and neighbourhood details. Contact Jared Gibbons, Top 1% REALTOR® — 604.928.1361.'
def d(what, where): return f'Explore {what} in {where}.' + TAIL

# slug: (title head, h1 or None, description or None)
ROWS = {
 'arbutus': ('Arbutus Ridge, Vancouver Homes for Sale', 'Arbutus Ridge Homes for Sale | Vancouver Real Estate', d('homes for sale', 'Arbutus Ridge, Vancouver')),
 'bc-landlord-tenant-resources': ('BC Landlord & Tenant Resources: RTB Forms Guide', None, None),
 'cheap-mobile-homes-langley-under-500k': ('Cheap Mobile Homes for Sale in Langley Under $500K', None, None),
 'chilliwack-condos-under-800k': ('Chilliwack Condos for Sale Under $800K', None, None),
 'cloverdale-condos-under-800k': ('Cloverdale Condos for Sale Under $800K', None, None),
 'commercial': ('Fraser Valley Commercial Real Estate for Sale', None, None),
 'downtown-vw': ('Downtown Vancouver Condos for Sale', 'Downtown Vancouver Condos for Sale | Vancouver Real Estate',
                 'Browse condos for sale in Downtown Vancouver. Updated MLS® listings and neighbourhood guidance — Jared Gibbons REALTOR®.'),
 'fraser-ve': ('Fraser Street Vancouver Homes for Sale', None, d('homes for sale', 'Fraser Street, Vancouver')),
 'homes-under-1500000': ('Homes for Sale Under $1.5 Million, South Surrey', None, None),
 'knight': ('Knight Street Vancouver Homes for Sale', 'Knight Street Homes for Sale | Vancouver Real Estate', d('homes for sale', 'Knight Street, Vancouver')),
 'ladner-townhomes-under-1-2m': ('Ladner Townhomes for Sale Under $1.2M', None, None),
 'main': ('Main Street Vancouver Homes for Sale', None, d('homes for sale', 'Main Street, Vancouver')),
 'maple-ridge-homes-over-1-8m': ('Maple Ridge Homes for Sale Over $1.8M', None, None),
 'mobile-home-parks-fraser-valley': ('Mobile Home Parks in the Fraser Valley', 'Mobile Home Parks in the Fraser Valley', None),
 'subscribe-to-our-newsletter': ('Real Estate Newsletter: South Surrey & Langley', None, None),
 'tsawwassen-homes-over-1-8m': ('Tsawwassen Homes for Sale Over $1.8M', None, None),
 'central-lonsdale': ('Central Lonsdale Condos for Sale, North Vancouver', 'Central Lonsdale Condos for Sale | North Vancouver Real Estate',
                      'Explore condos for sale in Central Lonsdale, North Vancouver. View current MLS® listings, market data, and neighbourhood details.'),
 'coal-harbour': ('Coal Harbour Condos for Sale, Vancouver', None, d('condos for sale', 'Coal Harbour, Vancouver')),
 'downtown-nw': ('Downtown New Westminster Condos for Sale', None, d('condos for sale', 'Downtown New Westminster')),
 'false-creek': ('False Creek Condos for Sale, Vancouver', 'False Creek Condos for Sale | Vancouver Real Estate', d('condos for sale', 'False Creek, Vancouver')),
 'quay': ('Quay New Westminster Condos for Sale', None, d('condos for sale', 'Quay, New Westminster')),
 'big-bend': ('Big Bend, Burnaby Land, Farms & Homes for Sale', 'Big Bend Land, Farms & Homes for Sale | Burnaby Real Estate', d('land, farms and homes for sale', 'Big Bend, Burnaby')),
 'brownstones-at-morgan-crossing': ('Brownstones at Morgan Crossing Townhomes for Sale', None, None),
 'greentree-village': ('Greentree Village Burnaby Townhomes for Sale', 'Greentree Village Townhomes for Sale | Burnaby Real Estate', d('townhomes for sale', 'Greentree Village, Burnaby')),
}

# ---- second batch (wording-only rows), chosen by judgment; Muse is reference only (Jared, 2026-11-01) ----
def band(city, kind, op, price):  # "Surrey Homes for Sale Under $1.8M"
    return f'{city} {kind} for Sale {op} {price}'
PRICE = [('chilliwack-homes-over-1-8m','Chilliwack','Homes','Over','$1.8M'),('chilliwack-homes-under-1-8m','Chilliwack','Homes','Under','$1.8M'),
 ('cloverdale-homes-over-1-8m','Cloverdale','Homes','Over','$1.8M'),('cloverdale-homes-under-1-8m','Cloverdale','Homes','Under','$1.8M'),('cloverdale-townhomes-under-1-2m','Cloverdale','Townhomes','Under','$1.2M'),
 ('ladner-homes-over-1-8m','Ladner','Homes','Over','$1.8M'),('ladner-homes-under-1-8m','Ladner','Homes','Under','$1.8M'),
 ('langley-condos-under-499k','Langley','Condos','Under','$499K'),('langley-homes-over-1-8m','Langley Luxury','Homes','Over','$1.8M'),('langley-homes-under-1-8m','Langley','Homes','Under','$1.8M'),('langley-townhomes-under-1-2m','Langley','Townhomes','Under','$1.2M'),
 ('mission-condos-under-800k','Mission','Condos','Under','$800K'),('mission-homes-over-1-8m','Mission','Homes','Over','$1.8M'),('mission-homes-under-1-8m','Mission','Homes','Under','$1.8M'),('mission-townhomes-under-1-2m','Mission','Townhomes','Under','$1.2M'),
 ('surrey-homes-over-1-8m','Surrey','Homes','Over','$1.8M'),('surrey-homes-under-1-8m','Surrey','Homes','Under','$1.8M'),('surrey-townhomes-under-1-2m','Surrey','Townhomes','Under','$1.2M'),
 ('tsawwassen-condos-under-800k','Tsawwassen','Condos','Under','$800K'),('tsawwassen-homes-under-1-8m','Tsawwassen','Homes','Under','$1.8M'),('tsawwassen-townhomes-under-1-2m','Tsawwassen','Townhomes','Under','$1.2M')]
for slug, city, kind, op, price in PRICE: ROWS[slug] = (band(city, kind, op, price), None, None)
FORECLOSE = [('chilliwackforeclosuresandcourtsales','Chilliwack'),('ladnerforeclosuresandcourtsales','Ladner'),('mapleridgeforeclosuresandcourtsales','Maple Ridge'),('missionforeclosuresandcourtsales','Mission'),
 ('southsurrey-foreclosures-court-ordered-sales','South Surrey'),('surreyforeclosuresandcourtsales','Surrey'),('tsawwassen-foreclosures-court-ordered-sales','Tsawwassen')]
for slug, city in FORECLOSE:
    for tail in (' Foreclosures for Sale & Court-Ordered Sales', ' Foreclosures for Sale & Court Sales'):
        if len(city + tail + BS) <= 66: ROWS[slug] = (city + tail, None, None); break
ROWS.update({
 'arista-townhomes': ('Arista Townhomes for Sale, Grandview Heights', None, None),
 'county-line-glen-valley': ('County Line Glen Valley, Langley Homes for Sale', None, None),
 'otter-district': ('Otter District, Langley Homes for Sale', None, None),
 'hatzic': ('Hatzic Homes for Sale: Lake, Lots & Acreages', None, None),
 'ladner-elementary': ('Homes for Sale in the Ladner Elementary Catchment', None, None),
 'langley-city': ('Langley City Homes for Sale & Neighbourhood Guide', None, None),
 'maple-ridge-mobile-homes': ('Maple Ridge Mobile & Manufactured Homes for Sale', None, None),
 'port-guichon': ('Port Guichon Homes for Sale, Ladner BC', None, None),
 'west-meadows-pitt-meadows-guide': ('West Meadows Pitt Meadows Homes for Sale & Guide', None, None),
 'north-maple-ridge-guide': ('North Maple Ridge Homes for Sale & Rural Guide', None, None),
 'westham-island-guide': ('Westham Island Delta Farms & Homes for Sale', None, None),
})
# Held unchanged on purpose (D-60, D-61): fraserview-nw, downtown-ve, gst-rebate-in-bc, privacy; brentwood-park, cariboo and edmonds-be keep their archived houses titles;
# guide pages with a matching homes page, burnaby-hospital, cityofmapleridge, mission-bc, land, zonings, recip, sold-properties, resources, GIS, granville, lower-landing.
out = {}
for slug, (head, h1, desc) in ROWS.items():
    e = {'title': t(head)}
    if h1: e['h1'] = h1
    if desc: e['description'] = desc
    out[slug] = e
    assert len(e['title']) <= 66, (slug, len(e['title']))
json.dump(out, open('src/data/seo-overrides.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'overrides')
