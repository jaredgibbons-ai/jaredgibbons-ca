#!/usr/bin/env python3
"""Port Kells, Surrey guide (D-212, Nov 10, 2026), commercial-first, in guide format v2 (D-205).

Jared, Nov 10: "do a Port Kells guide, mostly commercial if you want to focus it around that". So the page leads with the industrial
district north of Highway 1 (what's there, the Surrey industrial numbers, what to check before you buy) and covers the village south
of the highway second. Built from Jared's Port Kells pack (area-guide-packs-2026-11-10) with these checks and changes:
  - Re-read on the City's own PDFs, Nov 10: Corporate Report R179 (2007): 192 Street is "the main north south arterial road serving
    the Port Kells industrial area" and the October 2006 ramps are west-facing, "creating a half-interchange". Report R032 (2019) still
    lists a 192 Street and Highway 1 interchange as a City priority, so the half-interchange stands. R267 (2006): no dyke east of
    132 Street to the Langley border; owners of the industry along that frontage "were required to build to flood protection levels".
    R067 (April 13, 2026): Council authorized preliminary planning studies ahead of a South Port Kells NCP; owners of 94 of the 192
    lots answered the City's survey (October 2025 to March 2026). Port Kells Park page: 19340 88 Avenue, west of the village centre.
  - Drive times re-measured (OSRM, Nov 10, 2026) from 19150 96 Avenue in the industrial area: Walnut Grove 8 min (the pack's 6 used a
    different end point), Maple Ridge 13, Langley City 14, Surrey Central 16, downtown Vancouver 42. Labelled off-peak.
  - Prices: SnapStats has no Port Kells median, and the MLS® sub-area had 6 residential sales in a year, so no median is shown.
    The industrial numbers are Surrey-wide and say so (GVR Commercial Edge Q2 2026; Avison Young Q3 2026, both already on the
    Fraser Valley commercial market report page).
  - Added for the commercial angle, each from a primary source: the Canada Energy Regulator's 30 m prescribed area around a federally
    regulated pipeline (Trans Mountain crosses the district), BC's Site Disclosure Statement rules for sites with past industrial use,
    and Surrey's Port Kells-specific development cost charges.
  - Left out: the pack's 388 bus and 501 frequency (not re-checked), "one of Surrey's main industrial districts" (Invest Surrey's own
    wording is attributed instead), Wikipedia and transit fan sites as sources. Jared's verdict is left for him.
python3 -I tools/build_port_kells_guide_2026_11_10.py"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'portkells'
SLUG = 'port-kells-surrey-guide'
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def PP(*parts): return {'t': 'p', 'parts': [({'t': x[0], 'h': x[1]} if isinstance(x, tuple) else {'t': x}) for x in parts], 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def L(items): return {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': G}
def LINKS(pairs): return {'t': 'list', 'items': [[{'t': t, 'h': h if h.startswith('http') else f'/{h}.html'}] for t, h in pairs], 'gen': G}
def TBL(cap, head, rows, src): return {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'source': src, 'gen': G}

SUB = json.load(open('src/data/sold/sold-12m.json'))['sub']['North Surrey|Port Kells']['groups']
N = {k: SUB.get(k, {}).get('n', 0) for k in ('house', 'acreage', 'land')}
assert sum(N.values()) == 6, N   # the copy below says six

PAGE = {
    'slug': SLUG, 'status': 'draft', 'updated': '2026-11-10',
    'new_page': {'h1': 'Port Kells, Surrey: Industrial Area and Village Guide',
                 'title': 'Port Kells Surrey Industrial Property and Area Guide',
                 'description': 'Port Kells, Surrey: the industrial area north of Highway 1 and the village south of it. Zoning, flood, pipelines, access and what to check before you buy.'},
    'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Surrey', 'href': '/surrey-homes-for-sale.html'},
                    {'name': 'Neighbourhood guides', 'href': '/surrey-neighbourhood-guides.html'}, {'name': 'Port Kells', 'href': f'/{SLUG}.html'}],
    'blocks': [
        {'t': 'notice', 'text': 'Draft for Jared’s approval. Written November 10, 2026 from City of Surrey, provincial and federal sources and the market reports listed on the page. Jared’s verdict is still to come.', 'gen': G},
        H('Where Port Kells is'),
        P('Port Kells is the north-east corner of Surrey, on the south bank of the Fraser River at the Langley border, east of 176 Street. Highway 1 '
          'splits it in two. North of the highway, down to the river, is the Port Kells industrial area: warehouses, distribution, trucking and light '
          'industry along 96 Avenue and 192 Street. South of the highway is the original village, with a school, a park and homes on large rural lots.'),
        P('The name goes back to two settlers, both called Henry Kells, who laid out a townsite on the river around 1889 and 1890 and expected a port '
          'to follow. It never did. The 1907 schoolhouse and St. Oswald’s Anglican Church (1911) are what is left of the old village.'),
        H('Industrial and commercial property in Port Kells'),
        P('Invest Surrey, the City’s business arm, describes Port Kells as one of Surrey’s major industrial areas: about 781 acres and roughly 610 '
          'businesses, mostly on light industrial (IL) zoning, with manufacturing, construction and wholesale and distribution the main uses. The City '
          'calls 192 Street the main north-south road serving the industrial area.'),
        P('There is no published price or rent for Port Kells on its own, so these are the Surrey-wide numbers. In the second quarter of 2026 Surrey had '
          '53 commercial sales, more than any other Fraser Valley city, 19 of them industrial, for $249.9 million in all. In the third quarter, 4.2% of Surrey’s '
          'industrial space was vacant, against 5.7% in Langley, and asking rents averaged $19.66 a square foot net plus $6.95 in additional rent.'),
        TBL('Surrey industrial market, third quarter of 2026', ['Measure', 'Surrey', 'Metro Vancouver'],
            [['Industrial space (sq ft)', '45.1M', '246.0M'], ['Vacant', '4.2%', '4.0%'], ['Available', '4.7%', '4.9%'],
             ['Asking net rent, per sq ft', '$19.66', '$19.40'], ['Additional rent, per sq ft', '$6.95', '$7.27'],
             ['Under construction (sq ft)', '1,628,917', '3,562,952']],
            'Source: Avison Young, Metro Vancouver industrial market report, Q3 2026. Surrey is the whole City of Surrey submarket, not Port Kells alone.'),
        P('Two things to take from that. Surrey has 46% of all the industrial space being built across Metro Vancouver, and in the third quarter more '
          'Surrey space was given back than leased (net absorption of −220,336 sq ft). That gives a business looking to buy or lease more choice, and '
          'gives a landlord more competition for tenants.'),
        PP('Browse current listings on the ', ('Fraser Valley commercial property search', '/commercial.html'), ', and read the full numbers in the ',
           ('Fraser Valley commercial market report', '/fraser-valley-commercial-market-report.html'), '.'),
        H('Before you buy industrial property in Port Kells'),
        L(['Zoning and permitted uses. Most of the area is IL, but some sites carry their own comprehensive development (CD) zoning. Check that your exact '
           'use is permitted on the exact property with the City of Surrey before you firm up.',
           'Development cost charges. Surrey sets Port Kells-specific charges for industrial and commercial development, separate from its city-wide '
           'rates. If you plan to build or expand, put them in the numbers early.',
           'Flood. The Fraser River frontage east of 132 Street has no dyke, and the City requires development there to be built to flood protection '
           'levels. Ask the City for the flood construction level and check title for a floodplain covenant.',
           'Pipelines. Trans Mountain’s pipeline and a pump station sit in the district. Digging or building within 30 metres of a federally regulated '
           'pipeline, or driving equipment across one, needs the pipeline company’s written consent first.',
           'Site history. If a site has had certain industrial uses, BC’s contaminated sites rules can require a Site Disclosure Statement before a rezoning, '
           'subdivision or permit that disturbs soil. Ask what the site has been used for, and get an environmental professional’s advice before you firm up.',
           'Rail. CN owns most of the river frontage, and its main line runs along it. Expect trains as background, and confirm any rail access with CN, '
           'not the listing.',
           'GST. GST usually applies when you buy commercial or industrial property, on top of property transfer tax. Get your accountant’s advice on it '
           'before you write the offer.']),
        PP('More on zoning types: ', ('zoning guide', '/zonings.html'), '. Land for sale across the city: ', ('Surrey lots and land', '/surrey-lots-land.html'), '.'),
        H('The village: South Port Kells'),
        P('South of the highway, the old village sits around 88 Avenue, with homes on large lots and farmland in the Agricultural Land '
          'Reserve along its southern edge. The City’s South Port Kells plan (2005) covers about 608 hectares from the highway down to the ALR. In April '
          '2026 Council authorized planning studies ahead of a neighbourhood plan for the rest of South Port Kells, after the Port Kells Community '
          'Association asked for one and owners of 94 of the 192 lots answered the City’s survey. No plan has been drawn yet, so buy a property for what '
          'it is today.'),
        P(f"Very little sells here. In the twelve months to October 22, 2026 the MLS® sub-area recorded {sum(N.values())} home and land sales: "
          f"{N['acreage']} acreages, {N['land']} lots and {N['house']} house. That is too few for a fair median, so ask me for the sold list."),
        LINKS([('Port Kells homes for sale', 'port-kells-surrey'), ('Port Kells houses for sale', 'port-kells-surrey-houses-for-sale'),
               ('Port Kells acreages for sale', 'port-kells-acreages-for-sale'), ('Surrey acreages for sale', 'surrey-acreages-for-sale')]),
        PP('The rules for suites, ALR land, wells and septic: ', ('buying a home in Surrey: the rules', '/surrey-home-buying-rules.html'), ' and ',
           ('BC acreage buying rules', '/bc-acreage-buying-rules.html'), '.'),
        H('Schools in Port Kells'),
        P('Port Kells Elementary, kindergarten to grade 7, is in the village at 19076 88 Avenue, in the schoolhouse that opened in 1907. There is no '
          'secondary school in Port Kells. Surrey Schools sets catchments by address, so check the exact property in the district’s school locator.'),
        PP('Find the catchment school for an address: ', ('SD36 school locator', 'https://mybaragar.com/index.cfm?event=page.SchoolLocatorPublic&DistrictCode=BC36'),
           '. More: ', ('Schools in Surrey', '/schools-in-surrey-bc.html'), '.'),
        H('Parks near Port Kells'),
        L(['Port Kells Park, 19340 88 Avenue, just west of the village centre: an outdoor pool, softball diamonds, a playground, outdoor fitness equipment '
           'and the Latimer Creek wetland.',
           'Tynehead Regional Park, about 260 hectares of forest and meadow at the head of the Serpentine River, with the Tynehead Hatchery, a few minutes '
           'west along 96 Avenue.']),
        H('Getting around Port Kells'),
        L(['The 192 Street ramps on Highway 1 face west only: on toward Vancouver, off from Vancouver. Heading east to Langley and the valley, you use the '
           '200 Street interchange.',
           'North across the Fraser, 96 Avenue runs into Golden Ears Way and the Golden Ears Bridge, toll-free since September 2017. Maple Ridge is about '
           '13 minutes off-peak.',
           'TransLink’s 501 bus runs along 96 Avenue between Surrey Central Station and Langley Centre. Nothing runs on the village streets.',
           'The nearest SkyTrain will be Clayton Station, at 190 Street and Fraser Highway, when the Surrey Langley line opens (expected late 2029). It is a '
           'drive, not a walk.']),
        H('Nearby neighbourhood guides'),
        LINKS([('Barnston Island', 'barnston-island-surrey-guide'), ('Fleetwood and Tynehead', 'fleetwood-tynehead-guide'), ('Clayton', 'clayton-guide'),
               ('Guildford', 'guildford-guide'), ('Walnut Grove, Langley', 'walnut-grove-guide'), ('All Surrey guides', 'surrey-neighbourhood-guides')]),
        H('Sources for the Port Kells guide'),
        LINKS([('Invest Surrey: Port Kells industrial area profile', 'https://investsurrey.ca/media/23791'),
               ('City of Surrey: Corporate Report R179 (2007), 192 Street and Highway 1', 'https://www.surrey.ca/sites/default/files/corporate-reports/RPT_2007_R179.pdf'),
               ('City of Surrey: Corporate Report R267 (2006), Fraser River dykes', 'https://www.surrey.ca/sites/default/files/corporate-reports/RPT_2006_R267.pdf'),
               ('City of Surrey: Corporate Report R067 (2026), South Port Kells background studies', 'https://www.surrey.ca/sites/default/files/corporate-reports/CR_2026-R067.pdf'),
               ('City of Surrey: South Port Kells Land Use Plan', 'https://www.surrey.ca/sites/default/files/media/documents/ADOPTEDSOUTHPORTKELLSLANDUSEPLAN.pdf'),
               ('City of Surrey: Port Kells development cost charges (2025–2029 Financial Plan)', 'https://flipbook-surrey-ca.cld.bz/2025-2029-Surrey-Financial-Plan/43/'),
               ('City of Surrey: Port Kells Park', 'https://www.surrey.ca/parks-recreation/parks/port-kells-park'),
               ('Canada Energy Regulator: working near federally regulated pipelines', 'https://www.cer-rec.gc.ca/en/safety-environment/damage-prevention/conducting-activities-near-pipelines/'),
               ('Province of BC: identifying and disclosing sites that may be contaminated', 'https://www2.gov.bc.ca/gov/content/environment/air-land-water/site-remediation/identifying-and-disclosing-sites-that-may-be-contaminated'),
               ('Canada’s Historic Places: Port Kells Elementary School', 'https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=11415'),
               ('Canada’s Historic Places: St. Oswald’s Anglican Church', 'https://www.historicplaces.ca/en/rep-reg/place-lieu.aspx?id=2594'),
               ('Metro Vancouver: Tynehead Regional Park', 'https://metrovancouver.org/services/regional-parks/park/tynehead-regional-park'),
               ('Surrey Langley SkyTrain: stations', 'https://surreylangleyskytrain.gov.bc.ca/stations/'),
               ('BC school directory, School District 36', 'https://studentsuccess.gov.bc.ca/schools/in-school-district/036'),
               ('Fraser Valley commercial market report (GVR Commercial Edge Q2 2026 and Avison Young Q3 2026 figures)', 'fraser-valley-commercial-market-report')]),
    ],
    'faq': [
        {'q': 'What is the zoning in Port Kells?', 'a': 'North of Highway 1 it is mostly light industrial (IL), with some sites on their own comprehensive development (CD) zoning. South of the highway it is rural and residential land under the South Port Kells plan, with ALR land along the southern edge. Check the exact property with the City.'},
        {'q': 'Can I live on an industrial property in Port Kells?', 'a': 'Don’t plan on it. The industrial zones are for business, and the homes are south of the highway. Check the permitted uses for the exact property with the City before you buy.'},
        {'q': 'How do trucks get onto Highway 1 east from Port Kells?', 'a': 'Through the 200 Street interchange. The 192 Street ramps only face west, toward Vancouver.'},
        {'q': 'Is there a school in Port Kells?', 'a': 'Yes. Port Kells Elementary, kindergarten to grade 7, at 19076 88 Avenue. There is no secondary school in Port Kells, so check the catchment for the exact address.'},
    ],
}

PLUS = {
    'status': 'draft', 'name': 'Port Kells', 'sub': 'North Surrey|Port Kells',
    'summary': 'Port Kells is Surrey’s north-east corner, on the Fraser River at the Langley border. North of Highway 1 it is an established industrial area of about 781 acres and roughly 610 businesses, mostly light industrial. South of the highway is the original village: a school, a park with an outdoor pool and homes on large rural lots.',
    'verdict': None,
    'vibe': 'Warehouses, truck yards and freight trains north of the highway; a quiet village with big treed lots and farmland south of it.',
    'commute': {'from': '19150 96 Avenue, in the industrial area', 'measured': 'November 10, 2026',
                'rows': [['Walnut Grove', 8, 5.6], ['Maple Ridge', 13, 11.4], ['Langley City', 14, 10.5],
                         ['Surrey Central SkyTrain', 16, 13.0], ['Downtown Vancouver', 42, 38.9]]},
    'works': [
        {'t': 'Highway 1 runs through it, and the Golden Ears Bridge, toll-free since 2017, puts Maple Ridge about 13 minutes north.'},
        {'t': 'An established industrial area: about 781 acres and roughly 610 businesses, so your suppliers, trades and customers are close by.'},
        {'t': 'Surrey had more commercial sales than any other Fraser Valley city in the second quarter of 2026 (53, 19 of them industrial).'},
        {'t': 'Surrey’s industrial vacancy was 4.2% in the third quarter, lower than Langley’s 5.7%.'},
        {'t': 'A bus for staff: TransLink’s 501 runs along 96 Avenue to Surrey Central and Langley Centre.'},
        {'t': 'A quiet village south of the highway, with a school, a park and an outdoor pool.'},
    ],
    'doesnt': [
        {'t': 'The 192 Street ramps face west only. For Langley and the valley, trucks go round to 200 Street.'},
        {'t': 'The river frontage has no dyke, so flood construction levels apply to building there.'},
        {'t': 'Trans Mountain’s pipeline and pump station are in the district: work within 30 m of the pipeline needs the company’s written consent.'},
        {'t': 'Freight trains along the river, and truck traffic on 96 Avenue and 192 Street.'},
        {'t': 'Lots of new supply: Surrey has 1.6 million sq ft of industrial space under construction, so landlords compete for tenants.'},
        {'t': 'Port Kells-specific development cost charges if you build or expand.'},
        {'t': 'Hardly any homes sell: 6 home and land sales in the sub-area in a year, and no condos or townhomes at all.'},
        {'t': 'No SkyTrain until late 2029, and then Clayton Station is a drive away.'},
    ],
    'fit': [
        {'q': 'Are you buying a building for your own business?', 'a': 'Port Kells is built for it: highway access, other industrial businesses around you and a bus for staff. Before you firm up, check that your use is permitted on the exact property, the flood construction level, the site’s past uses and any pipeline or rail line nearby.', 'links': [['Fraser Valley commercial property search', '/commercial.html'], ['Zoning guide', '/zonings.html']]},
        {'q': 'Are you buying to lease it out?', 'a': 'Look hard at the supply. Surrey vacancy was 4.2% in the third quarter, but 1.6 million sq ft is under construction and more space was given back than leased, so price the rent you expect against new buildings nearby.', 'links': [['Fraser Valley commercial market report', '/fraser-valley-commercial-market-report.html']]},
        {'q': 'Do your trucks run east and west on Highway 1?', 'a': 'Westbound is easy from 192 Street. Eastbound goes through the 200 Street interchange, a few minutes further. North over the Golden Ears Bridge is straight up 96 Avenue and Golden Ears Way.'},
        {'q': 'Do you want to live near your work?', 'a': 'Then look south of the highway, in the village, where homes sit on large lots. The industrial lots are for business. Very little comes up for sale, so tell me early and I’ll watch for it.', 'links': [['Port Kells homes for sale', '/port-kells-surrey.html']]},
        {'q': 'Do you want a regular neighbourhood with shops and listings to choose from?', 'a': 'Then Port Kells isn’t it. Clayton, Fleetwood and Walnut Grove are close and have the choice.', 'links': [['Clayton guide', '/clayton-guide.html'], ['Fleetwood and Tynehead guide', '/fleetwood-tynehead-guide.html'], ['Walnut Grove guide', '/walnut-grove-guide.html']]},
    ],
    'faq': [
        {'q': 'Is Port Kells industrial or residential?', 'a': 'Both, split by Highway 1. North of the highway it is an industrial area of about 781 acres and roughly 610 businesses, mostly light industrial. South of it is the old village and rural homes on large lots, with ALR farmland along the southern edge.'},
        {'q': 'Is Port Kells in a floodplain?', 'a': 'The river frontage is. The City says the Fraser River frontage east of 132 Street to the Langley border has no dyke, and development there had to be built to flood protection levels. Ask the City for the flood construction level for the exact property.'},
        {'q': 'How much does industrial property cost in Port Kells?', 'a': 'No one publishes a Port Kells price on its own. Across Surrey, asking industrial rents averaged $19.66 a square foot net plus $6.95 additional rent in the third quarter of 2026. Sale prices depend on the building, the land and the zoning, so ask Jared for recent comparable sales.'},
    ],
    'video': None,
}

LINKS_IN = {   # slug -> (lead text, label)
    'port-kells-surrey': ('For the industrial area, the village, schools and what to check before you buy, see the ', 'Port Kells area guide'),
    'barnston-island-surrey-guide': ('Port Kells, on the Surrey shore across from the island, has its own guide: ', 'Port Kells area guide'),
    'fraser-valley-commercial-market-report': ('For one Surrey industrial area up close (zoning, flood, pipelines and access), see the ', 'Port Kells industrial area guide'),
}


def dump(path, d, raw=None):
    raw = raw if raw is not None else (open(path, encoding='utf-8').read() if os.path.exists(path) else '\n  "')
    ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
    s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
    open(path, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') or not raw.strip('\n "') else ''))


def main():
    nb = PAGE['new_page']
    assert 38 <= len(nb['title']) <= 60, len(nb['title'])
    assert 135 <= len(nb['description']) <= 158 and nb['description'].endswith('.'), len(nb['description'])
    open(f'src/data/local/{SLUG}.json', 'w', encoding='utf-8').write(json.dumps(PAGE, ensure_ascii=False, indent=2) + '\n')
    p = 'src/data/guide-plus.json'; d = json.load(open(p, encoding='utf-8')); d[SLUG] = PLUS
    open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    for slug, (lead, label) in LINKS_IN.items():
        f = f'src/data/local/{slug}.json'; raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
        d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'pklink']
        at = 1 if d['blocks'] and d['blocks'][0].get('t') == 'notice' else 0
        d['blocks'].insert(at, {'t': 'p', 'parts': [{'t': lead}, {'t': label, 'h': f'/{SLUG}.html'}, {'t': '.'}], 'gen': 'pklink'})
        dump(f, d, raw)
    h = 'src/data/local/surrey-neighbourhood-guides.json'; raw = open(h, encoding='utf-8').read(); hub = json.loads(raw)
    hub['blocks'] = [b for b in hub['blocks'] if b.get('gen') != 'pklink']
    hub['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Industrial and rural areas', 'gen': 'pklink', 'pos': 'end'},
                      {'t': 'list', 'items': [[{'t': 'Port Kells area guide', 'h': f'/{SLUG}.html'}, {'t': ' (the industrial area north of Highway 1 and the village south of it)'}]], 'gen': 'pklink', 'pos': 'end'}]
    dump(h, hub, raw)
    print('written', SLUG, '| links in:', len(LINKS_IN) + 1)


if __name__ == '__main__': main()
