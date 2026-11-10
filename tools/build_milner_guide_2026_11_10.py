#!/usr/bin/env python3
"""Milner, Langley guide (D-206, Nov 10, 2026), from Jared's Milner content pack, in guide format v2 (D-205).

What changed from the pack, and why
  - No SnapStats prices: SnapStats has no Milner line, and the Langley community median is not a Milner price. The page says there is
    no published Milner figure and offers the sold list instead. (Paragon sub-areas don't include Milner either.)
  - Sources swapped for primary ones: TransLink stop list (not the CPTDB fan wiki), BC Gov News for the 216 Street interchange, the
    Langley Retired Teachers' Association history and Canada's Historic Places for history, the ALC's own housing page for ALR homes.
    Our own zoning page and a contractor's site are not used as sources.
  - Bus frequency dropped (the pack's "every 30 minutes" did not match the trip planner's "every 20 minutes"); "Fort Langley" dropped
    from the 562 description (the route leaves Glover Road at 88 Avenue, south of the village).
  - ALR housing corrected: besides a suite inside the main house, the ALC now allows one additional residence (90 m² on parcels of
    40 ha or less, 186 m² on larger ones) without an application, if the Township's zoning allows it.
  - "Truck route" not stated (not re-checked); "closed December 2004" softened to "has since closed" (the source gives no year).
  - Jared's verdict is left out until he writes it; the quick answer runs without it.
Drive times: the pack's OSRM run, Nov 10, 2026, from 49.1277, -122.6231 on Glover Road (free-flow, labelled off-peak).
python3 -I tools/build_milner_guide_2026_11_10.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'milner'
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def PP(*parts): return {'t': 'p', 'parts': [({'t': x[0], 'h': x[1]} if isinstance(x, tuple) else {'t': x}) for x in parts], 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def L(items): return {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': G}
def LINKS(pairs): return {'t': 'list', 'items': [[{'t': t, 'h': h if h.startswith('http') else f'/{h}.html'}] for t, h in pairs], 'gen': G}

SLUG = 'milner-langley-guide'
PAGE = {
    'slug': SLUG, 'status': 'draft', 'updated': '2026-11-10', 'lead': 'homevalue', 'lead_place': 'Milner',
    'new_page': {'h1': 'Milner, Langley: Neighbourhood Guide', 'title': 'Milner Langley Acreages, Homes and Rural Living Guide',
                 'description': 'Milner in the Township of Langley: the farm village at Glover Road and 216 Street, five minutes from Highway 1. What works, what doesn’t, and ALR rules.'},
    'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'Langley', 'href': '/langley-homes-for-sale.html'},
                    {'name': 'Neighbourhood guides', 'href': '/langley-neighbourhood-guides.html'}, {'name': 'Milner', 'href': f'/{SLUG}.html'}],
    'blocks': [
        {'t': 'notice', 'text': 'Draft for Jared’s approval. Written November 10, 2026 from Jared’s Milner notes and the official sources listed on the page. Jared’s verdict is still to come.', 'gen': G},
        H('Where Milner is'),
        P('Milner is the small farm village at the old crossroads of Glover Road and 216 Street, in the Township of Langley, between Langley City to the '
          'south-west and Fort Langley to the north-east. The crossroads became Milner Station in 1910, when the BC Electric interurban line came through, '
          'and the name, which honours Lord Alfred Milner, won a local vote over “Berry’s Station”. The railway gave local farms a way to ship to New '
          'Westminster and Vancouver, and by 1925 the village had shops, homes, a church and a school around the station.'),
        P('It is still farm country. Most of what sells here is acreage, hobby farms and older rural houses along Glover Road and the side roads, with '
          'Trinity Western University’s campus (22500 University Drive) just to the east and Milner Valley Cheese, a farm cheesemaker, on Smith Crescent.'),
        H('Homes for sale in Milner'),
        P('There is no Milner area on MLS®, so its listings are filed under the neighbouring Langley sub-areas, and the board publishes no Milner price. '
          'Ask me for the recent Milner-area sold list before you set a budget: acreage prices swing with the land, the house and the ALR status more than '
          'with the neighbourhood.'),
        LINKS([('Langley acreages for sale', 'langley-acreages-for-sale'), ('Langley farms for sale', 'langley-farms'),
               ('Langley horse properties', 'langley-horse-properties-equestrian-farms-for-sale-mls-listings'), ('Langley houses for sale', 'langley-houses-for-sale')]),
        H('Schools near Milner'),
        P('The village had its own school from 1913, on Glover Road, and Langley High School even ran out of it from 1922 to 1924. The buildings later became '
          'the Milner Education Centre, which has since closed, so there is no public school in the village today. Langley Schools assigns each address '
          'to a catchment school, so check the exact address in the district’s school locator. The King’s School, an independent kindergarten to grade 12 '
          'school, has a Milner address.'),
        PP('Find the catchment school for an address: ', ('SD35 school locator', 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC35'),
           '. More: ', ('Schools in Langley', '/schools-in-langley-bc.html'), '.'),
        H('Getting around Milner'),
        L(['Highway 1 is about 5 minutes away off-peak, at the 216 Street interchange, which opened in September 2020.',
           'TransLink route 562 runs along Glover Road between Langley Centre and Carvolth Exchange, with a stop at Trinity Western University.',
           'The nearest SkyTrain will be Langley City Centre Station, east of 203 Street and Industrial Avenue, when the Surrey Langley line opens '
           '(expected late 2029). Until then the closest station is King George in Surrey.']),
        H('Rules that come with a Milner acreage'),
        L(['About three-quarters of the Township is in the Agricultural Land Reserve, and ALR status is set parcel by parcel. Check the exact property on '
           'the ALC’s ALR map.',
           'On ALR land, the ALC allows one main house of up to 500 m² of floor area, a secondary suite only inside it, and one additional residence '
           '(up to 90 m² on parcels of 40 hectares or less) without an application, as long as the Township’s zoning allows it. Subdivision and '
           'non-farm uses need ALC approval.',
           'Many rural properties here run on a well and a septic system rather than Township water and sewer. Get the well tested and the septic '
           'inspected, and check septic capacity before you plan to add bedrooms or a suite.']),
        PP('The Township-wide rules for zoning, suites, taxes and servicing are on one page: ', ('buying a home in the Township of Langley: the rules', '/langley-home-buying-rules.html'),
           '. ALR, farm tax class, wells and septic are covered in ', ('BC acreage buying rules', '/bc-acreage-buying-rules.html'), '.'),
        H('Nearby neighbourhood guides'),
        LINKS([('Fort Langley', 'fort-langley-guide'), ('Murrayville', 'murrayville-guide'), ('Salmon River', 'salmon-river-guide'),
               ('Walnut Grove', 'walnut-grove-guide'), ('Langley City', 'langley-city-guide'), ('All Langley guides', 'langley-neighbourhood-guides')]),
        H('Sources for the Milner guide'),
        LINKS([('Langley Retired Teachers’ Association: the history of Milner schools', 'https://www.langleyrta.ca/history-of-langley-schools/elementary-before-2004/elementary-schools-group-2/milner-schools/the-history-of-milner-schoo.html'),
               ('Canada’s Historic Places: Moir Residence, 6840 Glover Road', 'https://historicplaces.ca/en/rep-reg/place-lieu.aspx?id=1858'),
               ('BC Gov News: 216 Street interchange opens', 'https://news.gov.bc.ca/releases/2020TRAN0140-001664'),
               ('Agricultural Land Commission: housing in the ALR', 'https://www.alc.gov.bc.ca/use-of-alr-land/housing-in-the-alr/'),
               ('Surrey Langley SkyTrain: stations', 'https://surreylangleyskytrain.gov.bc.ca/stations/'),
               ('Trinity Western University: directions', 'https://www.twu.ca/visit/directions-twu'),
               ('BC school directory, School District 35', 'https://studentsuccess.gov.bc.ca/schools/in-school-district/035')]),
    ],
    'faq': [
        {'q': 'How much do homes cost in Milner?', 'a': 'There is no published Milner figure: Milner is not an MLS® sub-area, so its sales are counted with neighbouring areas. Most homes here are acreages and rural houses, where the land and ALR status set the price, so ask Jared for the recent Milner-area sold list.'},
        {'q': 'Is Milner in the Agricultural Land Reserve?', 'a': 'Much of the land around Milner is, and about three-quarters of the Township of Langley is in the ALR, but status is set parcel by parcel. Check the specific property on the ALC’s ALR map.'},
        {'q': 'Is there a bus in Milner?', 'a': 'Yes. TransLink route 562 runs along Glover Road between Langley Centre and Carvolth Exchange, with a stop at Trinity Western University.'},
        {'q': 'How far is Milner from Fort Langley?', 'a': 'About 8 minutes’ drive off-peak, 6 km north-east along Glover Road.'},
    ],
}

PLUS = {
    'status': 'draft', 'name': 'Milner', 'sub': None,
    'summary': 'Milner is the small farm village at Glover Road and 216 Street in the Township of Langley, between Langley City and Fort Langley. It grew up around a 1910 interurban station and is still acreages, hobby farms and older rural homes, about five minutes from Highway 1.',
    'verdict': None,
    'vibe': 'A farm-belt crossroads: fields, acreages and a few heritage buildings, with Trinity Western University next door.',
    'commute': {'from': 'Glover Road in Milner (49.1277, -122.6231)', 'measured': 'November 10, 2026',
                'rows': [['Highway 1', 5, 4.4], ['Fort Langley', 8, 6.0], ['Surrey Central SkyTrain', 22, 20.7], ['Downtown Vancouver', 46, 45.9]]},
    'works': [
        {'t': 'Quick highway access: Highway 1 is about 5 minutes away at the 216 Street interchange.'},
        {'t': 'Fort Langley is about 8 minutes’ drive, and Langley City’s shops are a few minutes the other way.'},
        {'t': 'Room for a farm, horses or a big garden, with Milner Valley Cheese and other farms as neighbours.'},
        {'t': 'A bus on Glover Road: route 562 runs to Langley Centre, Trinity Western University and Carvolth Exchange.'},
        {'t': 'Real history: Milner Station dates to 1910, and the Moir Residence (6840 Glover Road, 1909) is a designated heritage home.'},
    ],
    'doesnt': [
        {'t': 'No public school in the village. The old Milner school has closed, so children go to schools in neighbouring areas.'},
        {'t': 'No SkyTrain until the Surrey Langley line opens (expected late 2029), and then the nearest station is Langley City Centre.'},
        {'t': 'Many properties run on a well and septic, which need testing and can limit adding bedrooms or a suite.'},
        {'t': 'ALR rules limit subdivision, extra homes and non-farm uses on farm parcels.'},
        {'t': 'Car-first: there is one bus route, and everything else is a drive.'},
    ],
    'fit': [
        {'q': 'Do you want acreage or a small farm?', 'a': 'That’s what Milner is for. If the parcel is in the ALR, farming comes first, and subdividing or running a non-farm business needs ALC approval.', 'links': [['Langley acreages for sale', '/langley-acreages-for-sale.html']]},
        {'q': 'Do you need a mortgage-helper suite?', 'a': 'It depends on the lot. On ALR land a suite has to be inside the main house, though one small additional residence can be allowed, and a septic system has to handle it. For an easy suite, a serviced in-town street is simpler.', 'links': [['Willoughby guide', '/willoughby-guide.html'], ['Walnut Grove guide', '/walnut-grove-guide.html']]},
        {'q': 'Do you commute to Surrey or Vancouver?', 'a': 'The highway part is easy: about 5 minutes to Highway 1, 22 minutes to Surrey Central and 46 minutes to downtown Vancouver off-peak. There’s no rapid transit until late 2029.'},
        {'q': 'Do your kids need to walk to school?', 'a': 'Then look in town. Milner has no public school, so check the catchment for the exact address, or look at Murrayville or Langley City.', 'links': [['Murrayville guide', '/murrayville-guide.html']]},
    ],
    'faq': [
        {'q': 'Is Milner a good place to live?', 'a': 'For buyers who want space, quiet and a farm-belt setting five minutes from Highway 1, yes. Buyers who want walkable shops, transit and a neighbourhood school are better served in town, in Murrayville, Walnut Grove or Langley City.'},
        {'q': 'What are the downsides of living in Milner?', 'a': 'No public school in the village, no SkyTrain until late 2029, one bus route, many properties on a well and septic, and ALR rules that limit what you can build or subdivide on farm parcels.'},
    ],
    'video': None,
}


def main():
    open(f'src/data/local/{SLUG}.json', 'w', encoding='utf-8').write(json.dumps(PAGE, ensure_ascii=False, indent=2) + '\n')
    p = 'src/data/guide-plus.json'; d = json.load(open(p, encoding='utf-8')); d[SLUG] = PLUS
    open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    h = 'src/data/local/langley-neighbourhood-guides.json'; hub = json.load(open(h, encoding='utf-8'))
    for b in hub['blocks']:
        if b.get('gen') == 'gaplink' and b.get('t') == 'list':
            if not any(it[0].get('h') == f'/{SLUG}.html' for it in b['items']):
                b['items'].append([{'t': 'Milner neighbourhood guide', 'h': f'/{SLUG}.html'}, {'t': ' (the farm village at Glover Road and 216 Street)'}])
    raw = open(h, encoding='utf-8').read(); ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    open(h, 'w', encoding='utf-8').write(json.dumps(hub, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
    for slug, lead in (('fort-langley-guide', 'Milner, the farm village a few minutes south-west on Glover Road, has its own guide: '),
                       ('salmon-river-guide', 'Milner, the farm village at Glover Road and 216 Street, has its own guide: ')):
        f = f'src/data/local/{slug}.json'; raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
        d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'milnerlink']
        d['blocks'].insert(0, {'t': 'p', 'parts': [{'t': lead}, {'t': 'Milner neighbourhood guide', 'h': f'/{SLUG}.html'}, {'t': '.'}], 'gen': 'milnerlink'})
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(f, 'w', encoding='utf-8').write((json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
    print('written', SLUG)


if __name__ == '__main__': main()
