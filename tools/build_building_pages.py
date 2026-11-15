#!/usr/bin/env python3
"""Condo building pages, White Rock and South Surrey (D-282). One page per building, written from the sources named on each page.

    python3 -I tools/build_building_pages.py   -> src/data/local/<slug>.json (+ a "Building pages" list on white-rock-condo-buildings)

Facts come from the City of White Rock development info sheets (storeys, homes, builder, street level for the newer towers) and the
MLS® strata building records (strata plan, year built, levels, amenities, bylaw flags), read November 14, 2026. Where the two disagree
the City figure is used. Anything not confirmed is left out. Listing boxes use Gerry's MyRealPage searches 1452096-1452120
(docs/review/idx/building-searches-2026-11-14-DONE.xlsx); pages whose search still needs fixing get no box until it is fixed.
Sand Dollar, Ocean Wynd, Gateway and Elgin Creek Estates were on the first list but are small townhouse or detached-strata
complexes, not condo buildings, so they have no page.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from build_post_rewrites import parts  # noqa: E402

LOCAL = ROOT / 'src/data/local'
DAY = '2026-11-14'
G = 'bldg'
READ = 'November 14, 2026'


def P(text):
    return {'t': 'p', 'parts': parts(text), 'gen': G} if ('[' in text or '**' in text) else {'t': 'p', 'text': text, 'gen': G}


def H(text, level=2):
    return {'t': 'h', 'level': level, 'text': text, 'gen': G}


def L(*items):
    return {'t': 'list', 'items': [parts(i) for i in items], 'gen': G}


FAQ_SHOW = {'q': 'Can I book a private showing with Jared?', 'a': 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings of any listing in the building. Call or text 604-928-1361 or email jaredgibbons@royallepage.ca.', 'gen': G}

WR = 'White Rock'
SS = 'South Surrey'

# name, slug, city, addresses, facts{built, storeys, homes, builder, plan, street}, amenities, intro, living, extra cautions, has_search
B = [
    dict(name='Soleil', slug='soleil-white-rock-condos', city=WR, addr='1588 Johnston Road',
         built='2023', storeys='26', homes='178 apartments', builder='RDG', plan='EPS10169', street='About 24,600 sq ft of shops',
         amen='About 8,000 sq ft of indoor and outdoor amenity space: a fitness room and yoga studio, steam room and sauna, a rooftop deck with a hot tub, barbecue kitchen and gas fire pits, a children’s play area, a car wash bay, two study rooms and two guest suites. Three elevators serve the tower.',
         intro='Soleil is the tallest building on the City of White Rock’s list of new major developments: 26 storeys and 178 apartments at the top of Johnston Road, built by RDG and finished in 2023, with shops at street level.',
         living='Soleil sits at the north end of White Rock’s Town Centre, near North Bluff Road, so groceries, cafés and services are a short walk. Upper floors facing south look over the Town Centre toward Semiahmoo Bay.'),
    dict(name='Foster Martin', slug='foster-martin-white-rock-condos', city=WR, addr='1500 Martin Street, 1501 Foster Street and 1475 Foster Street',
         built='2021 onward, in stages', storeys='25, 25 and 24 (three towers)', homes='345 apartments', builder='Landmark Premiere Properties', plan='EPS7665 (The Martin) and others by tower', street='About 56,000 sq ft, 8 shops',
         amen='Indoor and outdoor pool, hot tub, sauna and steam room, a fitness room with yoga space, a party room, games room, a multi-purpose room with a kitchen, concierge, secured underground parking with electric car charging, and a resident shuttle.',
         intro='Foster Martin is three towers of 24 and 25 storeys between Foster Street and Martin Street, with 345 apartments built by Landmark Premiere Properties and shops along the street. The towers are The Martin (1500 Martin Street), The Foster (1501 Foster Street) and The Landmark (1475 Foster Street).',
         living='The towers are in the middle of White Rock’s Town Centre, a block off Johnston Road. Each tower has its own strata, so compare the fees, rules and reserve fund of the tower you are buying in, not the project as a whole.'),
    dict(name='Miramar Village', slug='miramar-village-white-rock-condos', city=WR, addr='1473 Johnston Road, 1441 Johnston Road, 15152 Russell Avenue and 15177 Thrift Avenue',
         built='2008 onward, in stages', storeys='From 15 to 21, by tower', homes='96 at 1473 Johnston Road; 229 in the later towers', builder='Bosa', plan='BCS3237 (1473 Johnston Road) and others by tower', street='About 50,000 sq ft, 14 shops',
         amen='At 1473 Johnston Road: a residents’ club with a barbecue terrace, library and great room, a guest room, a full-time on-site manager and water-source heat pump cooling. Amenities differ by tower.',
         intro='Miramar Village is Bosa’s group of towers on Johnston Road and Thrift Avenue in White Rock’s Town Centre, built in stages from 2008, with shops and services at street level. The 17-storey tower at 1473 Johnston Road has 96 homes; the later towers at Thrift Avenue add 229 more.',
         living='Miramar Village is next to the Town Centre’s shops, a short walk to Johnston Road’s cafés and down the hill to the beach. Each tower has its own strata plan, so the fees and bylaws vary.'),
    dict(name='The Semiah', slug='semiah-white-rock-condos', city=WR, addr='1439 George Street (project address 15241 Thrift Avenue)',
         built='2021', storeys='14', homes='88 apartments', builder='Marcon', plan='EPS7071', street='Residential only',
         amen='Central air conditioning, a ground-floor fitness room, bike storage, a playground and a storage locker for each home.',
         intro='The Semiah is a 14-storey concrete tower with 88 homes on George Street in White Rock’s Town Centre, built by Marcon in 2021 and designed by Arno Matis Architecture. It is residential only, with no shops below.',
         living='The building is a block from Johnston Road and Thrift Avenue. Homes are numbered on George Street even though the City lists the project at 15241 Thrift Avenue, so search both addresses.'),
    dict(name='Altus', slug='altus-white-rock-condos', city=WR, addr='1526 Finlay Street',
         built='2022', storeys='13', homes='126 apartments (16 rental)', builder='Oviedo Developments', plan='EPS7717', street='About 47,500 sq ft, 9 shops',
         amen='A clubhouse, exercise room, bike room and concierge.',
         intro='Altus is a 13-storey concrete building at 1526 Finlay Street with 126 homes, 16 of them kept as rentals, built by Oviedo Developments and finished in 2022, with shops at street level.',
         living='Altus is at the north edge of the Town Centre, close to North Bluff Road. The strata allows up to two pets, and short-term rentals under 30 days are not allowed, per the strata record.'),
    dict(name='The Beverley', slug='beverley-white-rock-condos', city=WR, addr='1501 Vidal Street',
         built='2017', storeys='13', homes='88 apartments', builder='Cressey', plan='EPS4111', street='Residential only',
         amen='A pool, sauna and steam room, fitness centre, rooftop deck, garden, playground, guest suite and concierge.',
         intro='The Beverley is a 13-storey concrete tower with 88 homes at 1501 Vidal Street, built by Cressey in 2017 and designed by Bingham Hill Architects. It is residential only.',
         living='Vidal Street is a quieter street on the west side of the Town Centre, uphill from West Beach. Ask which homes face south; those look toward Semiahmoo Bay.'),
    dict(name='Monaco', slug='monaco-white-rock-condos', city=WR, addr='1342 Johnston Road (project address 1350 Johnston Road)',
         built='2025', storeys='12', homes='97 apartments', builder='Solterra', plan='EPS11179', street='About 10,000 sq ft, 6 shops',
         amen='A clubhouse, exercise room, bike room and concierge.',
         intro='Monaco is one of White Rock’s newest towers: 12 storeys and 97 homes at 1342 Johnston Road, built by Solterra and finished in 2025, with six shops at street level.',
         living='Monaco is on the lower part of Johnston Road, closer to the beach than the Town Centre towers. The strata allows up to two pets.'),
    dict(name='Fantom', slug='fantom-white-rock-condos', city=WR, addr='14825 Thrift Avenue',
         built='2020', storeys='10', homes='25 apartments', builder='Forge Properties', plan='EPP5044', street='Residential only',
         amen='A lounge with an outdoor terrace, fitness room, sauna and steam room, media lounge, shared barbecue, car wash station, bike room and parking with charging outlets.',
         intro='Fantom is a small luxury building: 10 storeys and only 25 homes at 14825 Thrift Avenue, built by Forge Properties in 2020 and designed by Ankenman Associates.',
         living='Fantom is on Thrift Avenue on the west side of White Rock, a few blocks from the Town Centre. With 25 homes, listings are rare and strata costs are shared by fewer owners.'),
    dict(name='Avra', slug='avra-white-rock-condos', city=WR, addr='1455 George Street',
         built='2013', storeys='17', homes='94 apartments', builder='Epta Properties', plan='EPS226', street='Residential only',
         amen='Concierge, a wellness centre, an entertainment room with a full kitchen, a covered outdoor space, a guest suite and a live-in resident manager.',
         intro='Avra is a 17-storey concrete tower with 94 homes at 1455 George Street in White Rock’s Town Centre, built by Epta Properties in 2013 and designed by CDA Architects.',
         living='Avra is a block from Johnston Road and next to The Semiah. Upper floors on the south side look over the Town Centre toward the bay.'),
    dict(name='Belaire', slug='belaire-white-rock-condos', city=WR, addr='14824 North Bluff Road',
         built='2007', storeys='11', homes='48 apartments', builder='Marcon', plan='BCS2206', street='Residential only',
         amen='Central air conditioning, a bike room, storage and wheelchair access.',
         intro='Belaire is an 11-storey concrete building with 48 homes at 14824 North Bluff Road, built by Marcon in 2007.',
         living='Belaire is on North Bluff Road, the city’s northern edge, west of the Town Centre. The strata allows pets and rentals with restrictions; ask for the current bylaws.'),
    dict(name='Sussex House', slug='sussex-house-white-rock-condos', city=WR, addr='1551 Foster Street, 1581 Foster Street, 1550 Martin Street and 1580 Martin Street',
         built='2004–2005', storeys='8', homes='150 in the strata', builder='Rykon Group', plan='BCS698', street='Residential only',
         amen='Secured underground parking, elevators, an exercise centre, a garden and a guest suite.',
         intro='Sussex House is a concrete and brick complex of 150 homes on Foster Street and Martin Street in White Rock’s Town Centre, built by Rykon Group in 2004 and 2005.',
         living='The complex runs between Foster and Martin streets, near Foster Martin and a short walk to Johnston Road. Listings can carry any of four street addresses.'),
    dict(name='Pacific Terrace', slug='pacific-terrace-white-rock-condos', city=WR, addr='15111 Russell Avenue',
         built='1988', storeys='9', homes='84 apartments', builder='', plan='LMS1991', street='Residential only',
         amen='Concierge, an indoor pool, hot tub and sauna, exercise equipment, a library, workshop, guest suite and a rooftop lounge and sundeck.',
         intro='Pacific Terrace is a 9-storey concrete building with 84 homes at 15111 Russell Avenue, built in 1988, with an indoor pool and a rooftop lounge.',
         living='Russell Avenue is in the Town Centre, near Miramar Village. The strata record lists no pets; check the current bylaws before you buy if you have one.'),
    dict(name='Bayview Place', slug='bayview-place-white-rock-condos', city=WR, addr='1521 George Street',
         built='1977', storeys='6', homes='30 apartments', builder='', plan='NWS883', street='Residential only',
         amen='An elevator, in-suite laundry, storage lockers, secured and visitor parking, and wheelchair access.',
         intro='Bayview Place is a 6-storey concrete building with 30 homes at 1521 George Street, built in 1977. It has an age restriction and no pets, per the strata record.',
         living='George Street is in the Town Centre, near Avra and The Semiah. Age-restricted buildings can keep their rental limits, so ask for the current bylaws.'),
    dict(name='White Rock Square', slug='white-rock-square-condos', city=WR, addr='1480 Foster Street (White Rock Square I) and 1442 Foster Street (White Rock Square II)',
         built='1977–1978 and 1986', storeys='4 to 7', homes='About 100 in two buildings', builder='', plan='NWS885 (White Rock Square I)', street='Residential only',
         amen='A fitness room, rooftop garden, sauna, in-suite laundry and underground parking.',
         intro='White Rock Square is two concrete buildings on Foster Street with about 100 homes: White Rock Square I at 1480 Foster (built 1977–1978) and White Rock Square II at 1442 Foster (built 1986). The strata record describes them as adult-oriented, with no pets.',
         living='The buildings are on Foster Street in the Town Centre, near Foster Martin. Many homes have large balconies, and some upper homes have ocean views.'),
    dict(name='The Summit', slug='summit-white-rock-condos', city=WR, addr='15466 North Bluff Road',
         built='1995', storeys='7', homes='42 apartments', builder='', plan='LMS2140', street='Residential only',
         amen='A recreation centre, library, billiard room, garden, bike storage and secured underground parking.',
         intro='The Summit is a 7-storey concrete building with 42 homes at 15466 North Bluff Road, built in 1995. It is a 19+ building that allows one cat, per the strata record.',
         living='The Summit is on North Bluff Road at the east end of White Rock, close to the shops at Semiahmoo Town Centre. Age-restricted buildings can keep their rental limits, so ask for the current bylaws.'),
    dict(name='King + Crescent', slug='king-crescent-south-surrey-condos', city=SS, addr='146A Street and King George Boulevard (3438 146A Street and neighbouring buildings)',
         built='2024–2025', storeys='6 (four buildings)', homes='411 homes', builder='Zenterra Developments', plan='', street='Next to shops on King George Boulevard',
         amen='A gym and yoga room, theatre, games room, playground, guest suite and electric car charging. Each home comes with a parking stall and a storage locker.',
         intro='King + Crescent is Zenterra’s group of four 6-storey buildings with 411 homes off King George Boulevard in South Surrey’s King George Corridor, finished in 2024 and 2025.',
         living='The buildings are near the shops along King George Boulevard and a short drive to Highway 99. Being new, they carry the remaining BC new home warranty; ask the seller for the warranty documents.'),
    dict(name='The Heights', slug='heights-grandview-south-surrey-condos', city=SS, addr='2855 156 Street and 2845 156 Street',
         built='2014–2015', storeys='5', homes='Two buildings', builder='Lakewood', plan='EPS1140', street='Residential only',
         amen='A clubhouse, garden, playground, storage and elevators.',
         intro='The Heights is a pair of 5-storey wood-frame condo buildings by Lakewood at 2845 and 2855 156 Street in Grandview Heights, South Surrey, built in 2014 and 2015.',
         living='The Heights is in Grandview Heights, close to the shops at Grandview Corners and Morgan Crossing and to Highway 99. The strata allows two pets and rentals, per the strata record.'),
    dict(name='Southaven', slug='southaven-south-surrey-condos', city=SS, addr='3315, 3317 and 3319 148 Street',
         built='2023–2024', storeys='5 and 6', homes='About 163 condos plus nine townhomes', builder='Park Ridge Homes', plan='EPS9809 (3317 148 Street)', street='Residential only',
         amen='A fitness centre, games room with billiards and ping pong, a social lounge with a kitchenette, a meeting room and more than 7,000 sq ft of outdoor space with a barbecue area.',
         intro='Southaven is Park Ridge Homes’ group of three 5- and 6-storey condo buildings and two townhouse buildings on 148 Street, off King George Boulevard in South Surrey, finished in 2023 and 2024.',
         living='Southaven is in the King George Corridor, near Southpoint and Highway 99. Being new, the homes carry the remaining BC new home warranty; ask the seller for the warranty documents.'),
    dict(name='Morgan Crossing', slug='morgan-crossing-south-surrey-condos', city=SS, addr='15735 to 15795 Croydon Drive and 15850 26 Avenue',
         built='2009–2010', storeys='4, above shops', homes='Several buildings above the shopping village', builder='Larco Investments', plan='BCS3659 (15775 Croydon Drive)', street='Over 60 shops, a grocer and restaurants',
         amen='Rooftop gardens, a lounge and meeting room with a kitchen, gated underground parking and bike storage; a fitness centre is part of the village.',
         intro='The condos at Morgan Crossing sit above the shops of the Morgan Crossing village in Grandview Heights, South Surrey: 4-storey buildings by Larco on Croydon Drive and 26 Avenue, built in 2009 and 2010.',
         living='You walk downstairs to a grocer, restaurants and more than 60 shops, and Highway 99 is a few minutes away. Jared’s office is on Croydon Drive too.'),
    dict(name='Forest Ridge', slug='forest-ridge-south-surrey-condos', city=SS, addr='14588 McDougall Drive, 3535 146A Street and 3585 146A Street',
         built='About 2020', storeys='5 (three buildings)', homes='177 homes', builder='Quadra Homes', plan='EPS7011 (14588 McDougall Drive)', street='Residential only',
         amen='A guest suite; ask the strata for the full list.',
         intro='Forest Ridge is Quadra Homes’ group of three 5-storey buildings with 177 homes on McDougall Drive and 146A Street in South Surrey’s King George Corridor, finished around 2020.',
         living='The buildings are in the King George Corridor, near the shops on King George Boulevard and close to Highway 99.'),
    dict(name='HALVÖ', slug='halvo-south-surrey-condos', city=SS, addr='15341 and 15353 17 Avenue',
         built='2023–2025', storeys='5', homes='52 homes (15341 17 Avenue)', builder='Landcraft Homes', plan='EPS11580 (15353 17 Avenue)', street='Residential only',
         amen='A clubhouse, exercise room and bike room.',
         intro='HALVÖ is Landcraft Homes’ 5-storey wood-frame condo project on 17 Avenue in South Surrey, east of 152 Street, finished between 2023 and 2025.',
         living='17 Avenue is close to Semiahmoo Town Centre and the shops on 152 Street, a short drive to White Rock beach. Short-term rentals are not allowed, per the strata record.'),
]

SEARCH = {'soleil-white-rock-condos': '1452096', 'foster-martin-white-rock-condos': '1452097', 'miramar-village-white-rock-condos': '1452098',
          'semiah-white-rock-condos': '1452099', 'altus-white-rock-condos': '1452100', 'beverley-white-rock-condos': '1452101',
          'monaco-white-rock-condos': '1452102', 'fantom-white-rock-condos': '1452103', 'avra-white-rock-condos': '1452104',
          'belaire-white-rock-condos': '1452106', 'sussex-house-white-rock-condos': '1452107', 'pacific-terrace-white-rock-condos': '1452108',
          'bayview-place-white-rock-condos': '1452110', 'white-rock-square-condos': None, 'summit-white-rock-condos': '1452112',
          'king-crescent-south-surrey-condos': '1452114', 'heights-grandview-south-surrey-condos': '1452116', 'southaven-south-surrey-condos': '1452117',
          'morgan-crossing-south-surrey-condos': '1452118', 'forest-ridge-south-surrey-condos': '1452119', 'halvo-south-surrey-condos': '1452120'}

NAV = {WR: ('White Rock condos', '/white-rock-condos-for-sale.html'), SS: ('South Surrey condos', '/south-surrey-condos-for-sale.html')}


def short(addr):
    return addr.split(' (')[0].split(',')[0].replace(' and ', ' & ')


def build(b):
    name, slug, city = b['name'], b['slug'], b['city']
    area = 'White Rock' if city == WR else 'South Surrey'
    title = f'{name} Condos for Sale | {area}'
    single = not any(k in b['addr'] for k in (' and ', ',', ' to '))
    if single and len(f'{name} Condos for Sale | {short(b["addr"])}, {area}') <= 60:
        title = f'{name} Condos for Sale | {short(b["addr"])}, {area}'
    if len(title) > 60:
        title = f'{name} Condos for Sale | {area}'
    desc = f'{name} condos for sale in {area}: {b["storeys"]} storeys, {b["homes"].split(" (")[0]}, built {b["built"]}. Live MLS® listings, building facts and strata tips.'
    if len(desc) > 155 or not b['storeys'].isdigit() or not b['homes'][:1].isdigit():
        desc = f'{name} condos for sale in {area}: live MLS® listings, building facts, amenities and strata tips from Jared Gibbons.'
    h1 = f'{name} Condos for Sale, {area}'
    has = bool(SEARCH.get(slug))
    rows = [['Address', b['addr']], ['Built', b['built']], ['Storeys', b['storeys']], ['Homes', b['homes']]]
    if b['builder']: rows.append(['Builder', b['builder']])
    if b['plan']: rows.append(['Strata plan', b['plan']])
    rows.append(['Street level', b['street']])
    others = [x for x in B if x['city'] == city and x['slug'] != slug][:8]
    blocks = [
        {'t': 'notice', 'text': f'Draft for Jared’s approval. Building facts from the City of White Rock info sheets and the MLS® strata building records, read {READ}. '
                                + (f'Live search: Gerry’s {SEARCH[slug]}.' if has else 'Listing box waits on a fixed MyRealPage search.'), 'gen': G},
        P(b['intro']),
    ]
    if has:
        blocks += [H(f'{name} condos for sale now'), {'t': 'grid', 'gen': G}]
    else:
        blocks += [H(f'{name} condos for sale now'),
                   P(f'Live listings for this building are being set up. Until then, see [{NAV[city][0]} for sale]({NAV[city][1]}) or call or text Jared at 604-928-1361 and he will send you every {name} listing as it comes up.')]
    blocks += [
        H(f'{name} at a glance'),
        {'t': 'table', 'caption': f'{name} building facts', 'head': ['', name], 'rows': rows,
         'source': f'Sources: City of White Rock development info sheets (newer White Rock towers) and MLS® strata building records, read {READ}. Confirm with the strata documents.', 'gen': G},
        H('Amenities'),
        P(b['amen']),
        H(f'Living at {name}'),
        P(b['living']),
        H(f'Before you buy at {name}'),
        L(f'**Read the strata package:** the Form B, two years of minutes, the bylaws, the depreciation report and the contingency reserve fund balance. They show what {name} owners are planning to fix and pay for.',
          '**Rentals:** since November 24, 2022, BC stratas cannot ban owners from renting, except in age-restricted buildings. Short-term rental limits can still apply.',
          '**Pets and parking:** pet limits, parking stalls, storage lockers and electric car charging are set by the bylaws and the title, home by home. Check them for the exact home you are buying.',
          '**Price it on recent sales in the building:** Jared pulls the sold prices for the building and the homes that compete with it before you write an offer.'),
        H('More condo buildings nearby'),
        L(*[f'[{x["name"]} condos]({"/" + x["slug"] + ".html"})' for x in others],
          '[White Rock condo buildings, tower by tower](/white-rock-condo-buildings.html)',
          f'[{NAV[city][0]} for sale]({NAV[city][1]})'),
    ]
    faq = [
        {'q': f'When was {name} built?', 'a': f'{name} at {b["addr"]} was built {b["built"]}' + (f' by {b["builder"]}' if b['builder'] else '') + f', per the MLS® strata building record.'},
        {'q': f'How big is {name}?', 'a': f'{name} is {b["storeys"]} storeys with {b["homes"]}.'},
        {'q': f'What amenities does {name} have?', 'a': b['amen']},
    ]
    faq = [dict(f, gen=G) for f in faq] + [FAQ_SHOW]
    assert len(title) <= 60, (slug, title)
    assert len(desc) <= 155, (slug, len(desc))
    return {'status': 'draft', 'slug': slug, 'updated': DAY, 'hand_edited': True, 'bldg_page': True,
            'new_page': {'title': title, 'description': desc, 'h1': h1},
            'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': NAV[city][0], 'href': NAV[city][1]},
                            {'name': 'Condo buildings', 'href': '/white-rock-condo-buildings.html'}, {'name': name, 'href': f'/{slug}.html'}],
            'faq_heading': f'{name}: your questions answered', 'faq': faq, 'blocks': blocks}


def main():
    for b in B:
        d = build(b)
        (LOCAL / f'{d["slug"]}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
        print('wrote', d['slug'], '|', d['new_page']['title'])
    # hub: one list of every building page on white-rock-condo-buildings
    f = LOCAL / 'white-rock-condo-buildings.json'
    g = json.loads(f.read_text())
    g['blocks'] = [x for x in g['blocks'] if x.get('gen') != G]
    i = next(k for k, x in enumerate(g['blocks']) if x.get('t') == 'h' and x.get('text', '').startswith('Which White Rock building'))
    g['blocks'][i:i] = [H('Building pages: White Rock and South Surrey'),
                        P('Each page has the building’s facts, amenities, strata tips and its own live listings.'),
                        L(*[f'[{x["name"]}]({"/" + x["slug"] + ".html"}), {short(x["addr"])}, {x["city"]}' for x in B])]
    f.write_text(json.dumps(g, ensure_ascii=False, indent=1) + '\n')
    print('updated white-rock-condo-buildings')


if __name__ == '__main__':
    main()
