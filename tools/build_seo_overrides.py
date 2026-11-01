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
                 'Browse condos and homes for sale in Downtown Vancouver. Updated MLS® listings and neighbourhood guidance — Jared Gibbons REALTOR®.'),
 'fraser-ve': ('Fraser Street Vancouver Homes for Sale', None, d('homes for sale', 'Fraser Street, Vancouver')),
 'homes-under-1500000': ('Homes for Sale Under $1.5 Million, South Surrey', None, None),
 'knight': ('Knight Street Vancouver Homes for Sale', 'Knight Street Homes for Sale | Vancouver Real Estate', d('homes for sale', 'Knight Street, Vancouver')),
 'ladner-townhomes-under-1-2m': ('Ladner Townhomes for Sale Under $1.2M', None, None),
 'main': ('Main Street Vancouver Homes for Sale', None, d('homes for sale', 'Main Street, Vancouver')),
 'maple-ridge-homes-over-1-8m': ('Maple Ridge Homes for Sale Over $1.8M', None, None),
 'mobile-home-parks-fraser-valley': ('Mobile Home Parks in the Fraser Valley', 'Mobile Home Parks in the Fraser Valley', None),
 'subscribe-to-our-newsletter': ('Real Estate Newsletter: South Surrey & Langley', None, None),
 'tsawwassen-homes-over-1-8m': ('Tsawwassen Homes for Sale Over $1.8M', None, None),
 'brentwood-park': ('Brentwood Park Burnaby Condos & Homes for Sale', 'Brentwood Park Condos & Homes for Sale | Burnaby Real Estate', d('condos and homes for sale', 'Brentwood Park, Burnaby')),
 'cariboo': ('Cariboo Burnaby Condos & Homes for Sale', 'Cariboo Condos & Homes for Sale | Burnaby Real Estate', d('condos and homes for sale', 'Cariboo, Burnaby')),
 'central-lonsdale': ('Central Lonsdale Condos for Sale, North Vancouver', 'Central Lonsdale Condos for Sale | North Vancouver Real Estate',
                      'Explore condos and homes for sale in Central Lonsdale, North Vancouver. View current MLS® listings, market data, and neighbourhood details.'),
 'coal-harbour': ('Coal Harbour Condos for Sale, Vancouver', None, d('condos and homes for sale', 'Coal Harbour, Vancouver')),
 'downtown-nw': ('Downtown New Westminster Condos for Sale', None, d('condos and homes for sale', 'Downtown New Westminster')),
 'edmonds-be': ('Edmonds Burnaby Condos & Homes for Sale', 'Edmonds Condos & Homes for Sale | Burnaby Real Estate', d('condos and homes for sale', 'Edmonds, Burnaby')),
 'false-creek': ('False Creek Condos for Sale, Vancouver', 'False Creek Condos for Sale | Vancouver Real Estate', d('condos and homes for sale', 'False Creek, Vancouver')),
 'quay': ('Quay New Westminster Condos for Sale', None, d('condos and homes for sale', 'Quay, New Westminster')),
 'big-bend': ('Big Bend, Burnaby Land, Farms & Homes for Sale', 'Big Bend Land, Farms & Homes for Sale | Burnaby Real Estate', d('land, farms and homes for sale', 'Big Bend, Burnaby')),
 'brownstones-at-morgan-crossing': ('Brownstones at Morgan Crossing Townhomes for Sale', None, None),
 'greentree-village': ('Greentree Village Burnaby Townhomes for Sale', 'Greentree Village Townhomes for Sale | Burnaby Real Estate', d('townhomes for sale', 'Greentree Village, Burnaby')),
}
# Held unchanged on purpose (see D-60): fraserview-nw, downtown-ve, gst-rebate-in-bc, privacy.
out = {}
for slug, (head, h1, desc) in ROWS.items():
    e = {'title': t(head)}
    if h1: e['h1'] = h1
    if desc: e['description'] = desc
    out[slug] = e
    assert len(e['title']) <= 66, (slug, len(e['title']))
json.dump(out, open('src/data/seo-overrides.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'overrides')
