#!/usr/bin/env python3
"""D-387 (part 4): East Clayton page. Search Console (URL-prefix property, 90 days to Nov 20 2026): "east clayton" 97 impressions
(11.5), "east clayton north" 25 (8.3), "east clayton bc" 20 (12.0), "where is east clayton" 6, all answered by /clayton-guide.html.
The searches are about the place, so the page answers where it is, what "East Clayton North" means, schools, parks and SkyTrain,
then shows the listings.
Sources: Jared's East Clayton paragraph (area overviews batch 2, docs/research/area-overviews/batch2-2026-11-20.md) and facts the
Clayton pages already cite (City plan areas, Corporate Report R156, school and park addresses, Clayton Community Centre, the
Surrey Langley SkyTrain stations). Nothing new is claimed.
    python3 tools/build_east_clayton_page.py   -> src/data/local/east-clayton.json
"""
import json
SLUG = 'east-clayton'
SD36 = 'https://www.surreyschools.ca/page/78827/school-catchment-locator'
P = lambda t: {'t': 'p', 'text': t, 'gen': 'ecl'}
H = lambda t: {'t': 'h', 'level': 2, 'text': t, 'gen': 'ecl'}
def L(*parts): return {'t': 'p', 'parts': [{'t': x} if isinstance(x, str) else {'t': x[0], 'h': x[1]} for x in parts], 'gen': 'ecl'}
def LIST(*items): return {'t': 'list', 'items': [[{'t': it}] if isinstance(it, str) else [{'t': it[0], 'h': it[1]}] for it in items], 'gen': 'ecl'}

BLOCKS = [
    P('East Clayton is the first urban neighbourhood that was developed in Clayton Heights. It sits north of Fraser Highway, along the '
      'Langley border. The City notes that the area was once rural acreage and farmland; it is now a compact residential community of '
      'houses and townhouses, with parks, schools, and local shops. Hazelgrove Elementary and Katzie Elementary are in this part of '
      'Clayton, and Hazelgrove Park is a central green space. Planning along Fraser Highway is intended to tie East Clayton to future rapid transit.'),
    LIST(('What is my East Clayton home worth?', '/home-evaluation.html'), ('Call or text 604-928-1361', 'tel:+16049281361'), ('All Clayton homes for sale', '/clayton.html')),
    H('East Clayton homes for sale'),
    P('The real estate board does not list East Clayton on its own: its homes are part of the board’s Clayton sub-area, so the live '
      'listings below are for Clayton, East Clayton included. Ask me for East Clayton only and I will send you those as they come up.'),
    {'t': 'grid', 'gen': 'ecl'},
    H('Where is East Clayton?'),
    P('East Clayton is the eastern part of Clayton Heights, in Surrey’s Cloverdale community: about 314 hectares (776 acres) north of '
      'Fraser Highway and west of the Langley border. Homes east of that border are in the Township of Langley, not in Surrey. The map '
      'shows Clayton as a whole; East Clayton is its Langley side.'),
    {'t': 'areamap', 'region': 'cloverdale', 'mode': 'area', 'current': 'clayton', 'gen': 'ecl'},
    H('East Clayton North and the other plan areas'),
    P('The City planned East Clayton in four parts: the main East Clayton Neighbourhood Concept Plan (endorsed in 2003), an extension '
      'west of 188 Street, an extension north of 72 Avenue (the City’s “East Clayton Extension North of 72 Avenue”, which '
      'is what “East Clayton North” usually means), and a transit-oriented area on Fraser Highway. The four went through separate '
      'plans, so house form changes from one part to the next.'),
    P('Those plan designations have since been superseded by the Surrey 2050 Official Community Plan, which now guides development. '
      'Check the zoning of a specific lot with the City before you count on a suite, a coach house or more units.'),
    H('Schools, parks and the community centre'),
    LIST('Hazelgrove Elementary, 7057 191 Street, and Katzie Elementary are in East Clayton.',
         'Clayton Heights Secondary and École Salish Secondary are the nearby secondary schools.',
         'Hazelgrove Park, 7080 190 Street, is the central green space.',
         'Clayton Community Centre, 7155 187A Street (opened October 2021), has recreation, arts and the Clayton branch of Surrey Libraries.'),
    L('Catchments in this area split by address and have changed as new schools opened, so check the ', ('Surrey Schools locator', SD36),
      ' for the home you have in mind, or see ', ('homes near Clayton Heights Secondary', '/homes-near-clayton-heights-secondary.html'), '.'),
    H('SkyTrain and getting around'),
    P('Fraser Highway is the main route. East Clayton is not a SkyTrain neighbourhood yet: the Surrey Langley SkyTrain project will add '
      'Clayton Station at Fraser Highway and 190 Street, and Hillcrest–184 Street Station to the west. The East Clayton transit-oriented '
      'area plan is meant to tie the neighbourhood to that line.'),
    H('Homes in East Clayton'),
    L('Most East Clayton homes are houses and townhouses on a compact street grid. Compare ', ('Clayton houses for sale', '/clayton-cloverdale-houses-for-sale.html'),
      ', ', ('Clayton condos and townhouses', '/clayton-cloverdale-condos-townhomes-for-sale.html'), ' and ', ('new construction in Clayton', '/new-construction-clayton.html'),
      ', or read the ', ('Clayton Heights guide', '/clayton-guide.html'), ' for the whole area.'),
]
FAQ = [
    {'q': 'Where is East Clayton?', 'a': 'East Clayton is in Surrey, BC, in the eastern part of Clayton Heights: north of Fraser Highway and west of the Township of Langley border, in the Cloverdale community.'},
    {'q': 'Is East Clayton in Surrey or Langley?', 'a': 'Surrey. It runs up to the Langley border, and homes east of that border are in the Township of Langley.'},
    {'q': 'What is East Clayton North?', 'a': 'Usually the East Clayton Extension North of 72 Avenue, one of the four parts the City planned East Clayton in. The others are the main East Clayton plan, an extension west of 188 Street and a transit-oriented area on Fraser Highway.'},
    {'q': 'Which schools serve East Clayton?', 'a': 'Hazelgrove Elementary and Katzie Elementary are in East Clayton; Clayton Heights Secondary and École Salish Secondary are nearby. Catchments split by address, so check the Surrey Schools locator.'},
    {'q': 'Will SkyTrain come to East Clayton?', 'a': 'The Surrey Langley SkyTrain project will add Clayton Station at Fraser Highway and 190 Street. East Clayton has no SkyTrain station today.'},
]
T = 'East Clayton, Surrey BC | Where It Is, Homes for Sale & Map'
D = 'Where is East Clayton? North of Fraser Highway on Surrey’s Langley border. Homes for sale, East Clayton North, schools, parks and Clayton Station.'
assert len(T) <= 60 and len(D) <= 158, (len(T), len(D))
page = {'status': 'draft', 'slug': SLUG, 'updated': '2026-11-20', 'hand_edited': True,
        'new_page': {'title': T, 'description': D, 'h1': 'East Clayton, Surrey'},
        'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Cloverdale', 'href': '/cloverdale-bc.html'}, {'name': 'Clayton', 'href': '/clayton.html'}, {'name': 'East Clayton, Surrey', 'href': f'/{SLUG}.html'}],
        'faq_heading': 'East Clayton: your questions answered', 'faq': [dict(f, gen='ecl') for f in FAQ], 'blocks': BLOCKS}
open(f'src/data/local/{SLUG}.json', 'w').write(json.dumps(page, ensure_ascii=False, indent=1) + '\n')
print('wrote', SLUG)
