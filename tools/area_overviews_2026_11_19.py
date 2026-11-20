"""D-379: Jared's area overviews (area-overviews-seo.docx, sent Nov 19 2026) published on the five area hub pages.
Jared: "Is there anything we can add to those core pages to make them better? Here are some notes for you."

His words are kept as written. Each fact was checked against the sources the site's own guides cite (and, for Costco,
Superstore and the Newton wave pool, the stores' and City's own pages). One change: in North Surrey, Bolivar Heights
"near Highway 1 and the Port Mann, between Guildford and the freeway" became "just north of City Centre, around Bolivar
Park and Invergarry Park", which is what the North Surrey page already sources.

Each overview goes on the area's hub page as the first section under the H1, with links to the area guide and the school
district's catchment locator. On North Surrey it replaces the shorter "The eight North Surrey sub-areas" section (same
links kept); on East Newton it replaces the old "Surrey's Family Hub" text, whose claims (schools that "consistently rank
well", "convenient access to Highway 1") had no source.
Run once from the repo root: python3 tools/area_overviews_2026_11_19.py
"""
import json

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    raise SystemExit(f'format not matched: {p}')
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

SD35 = 'https://www.sd35.bc.ca/school-locator'
SD36 = 'https://www.surreyschools.ca/page/78827/school-catchment-locator'
P = lambda t: {'t': 'p', 'text': t}
def L(*parts): return {'t': 'p', 'parts': [{'t': x} if isinstance(x, str) else {'t': x[0], 'h': x[1]} for x in parts]}
H = lambda t: {'t': 'h', 'level': 2, 'text': t}

OV = {
'murrayville': [
    H('Living in Murrayville, Langley'),
    P("Murrayville is an established neighbourhood in the Township of Langley, just east of the City of Langley, along the Fraser Highway. "
      "The Township calls it the traditional civic core. If you are browsing homes for sale in Murrayville, you will find a settled mix of "
      "family houses on mature streets, townhouses, and condos, with only a few larger properties on the edge. It feels convenient and "
      "established, rather than like a brand-new suburb."),
    P("Everyday life here is close to Langley Memorial Hospital, the W.C. Blair Recreation Centre, the Murrayville Library, and the Langley "
      "RCMP’s main detachment. Langley Regional Airport is in the neighbourhood as well. The historic heart of the community grew up around "
      "Murray’s Corner, and Murrayville includes one of only two heritage conservation areas in the Township (the other is in Fort Langley). "
      "That designation applies to the historic core and comes with rules for changes to properties. Confirm the details with the Township if "
      "you are buying or renovating there."),
    L("Parks and local shops are close at hand. Fraser Highway is the main route in and out, with bus service along the corridor. Nearby public "
      "schools include James Hill Elementary and Langley Fundamental Elementary. Catchments are set by address, so check the ",
      ('SD35 school locator', SD35), " for the home you have in mind."),
    L("Murrayville Langley real estate is a good fit if you want a central Township location, everyday services close by, and a choice of "
      "houses, townhouses, or condos. For schools, parks and the heritage area in more detail, see my ", ('Murrayville guide', '/murrayville-guide.html'), "."),
],
'salmon-river': [
    H('Living in Salmon River, Langley'),
    P("Salmon River is a rural and semi-rural part of the Township of Langley, along the river of the same name, east of Willoughby and within "
      "easy reach of Highway 1 and the Fraser Highway. People look here for acreages, larger lots, and a quieter setting. Many properties have "
      "room for a shop or workshop, and some suit a hobby farm or horses. It is not, though, a typical riverfront neighbourhood. A few homes sit "
      "along the water, but most are simply in the Salmon River area, on private, usable land."),
    P("Homes for sale in Salmon River range from older ranchers and family houses to custom builds, with a small number of condos and "
      "manufactured homes as well. Servicing can vary from one property to the next. Some lots are on municipal water; others use a well or "
      "septic. Some are in the Agricultural Land Reserve, and some are not. Check zoning, ALR status, and servicing with the Township — and "
      "with the Agricultural Land Commission if the land is in the ALR — before you write an offer."),
    L("Highway 1 is the usual route toward Vancouver and the rest of the Fraser Valley. Fort Langley and everyday shopping in the Township are a "
      "short drive. Nearby public schools include D.W. Poppy Secondary and Peterson Road Elementary. Confirm the catchment for the exact address "
      "with ", ('SD35', SD35), "."),
    L("Living in Salmon River, Langley, suits buyers who want space, privacy, and a country feel, without being far from the Township’s main "
      "roads. For the Uplands plan, servicing and ALR detail, see my ", ('Salmon River guide', '/salmon-river-guide.html'), "."),
],
'royal-heights': [
    H('Living in Royal Heights, Surrey'),
    P("Royal Heights is a small, mostly residential pocket in northwest Surrey, near 96 Avenue and Scott Road, on a hill above the Fraser. "
      "People looking at homes for sale in Royal Heights often come for the quiet streets, the views toward New Westminster, the North Shore "
      "mountains, and the river, and the short hop to the bridges and major roads."),
    P("The City of Surrey says that around Royal Heights Park, most homes were built from the late 1950s to the early 1970s. You will see "
      "basement-entry, split-level, and rancher-style houses, with some newer homes and townhouses mixed in. The park was established in the "
      "mid-1960s, with a forested side, an open field, and looping trails. A group of lots beside the park was rezoned in 2026 — confirm "
      "the current zone with the City."),
    L("Living in Royal Heights often means a house with a yard. Many homes have a secondary suite, or room for one; always confirm that any "
      "suite was built with a permit. Nearby public schools include Royal Heights Elementary and L.A. Matheson Secondary. Check the ",
      ('Surrey Schools locator', SD36), " for the exact address."),
    L("Scott Road, Highway 17, and the Alex Fraser and Pattullo bridges are close. Buses serve the area; SkyTrain is a short trip rather than a "
      "walk from most streets. Royal Heights real estate is a fit if you want an established North Surrey neighbourhood with a view, without "
      "living in the City Centre towers. The 2026 rezoning and the park are covered in my ", ('Royal Heights guide', '/royal-heights-guide.html'), "."),
],
'east-newton': [
    H('Living in East Newton, Surrey'),
    P("East Newton is an MLS area in the Newton part of Surrey. The City uses the name for the neighbourhoods around Chimney Hill, east of "
      "144 Street, north of 64 Avenue and Hyland Creek, and south of Bear Creek. On the map it runs roughly from King George Boulevard to "
      "152 Street. Those edges are approximate, so ask if a specific address is included."),
    P("You will find a mix of family houses and older townhouses and condos, including some adult-oriented or 55+ complexes (confirm the "
      "bylaws). Pockets such as Chimney Hill and Hyland Creek have their own feel. Living in East Newton, Surrey, often appeals to families "
      "who want a house, to buyers looking at townhomes, and to people who want daily shopping close by."),
    P("Costco and Superstore are nearby. Newton Recreation Centre, home of the wave pool, and Newton Exchange sit just to the west. The R1 "
      "RapidBus runs along King George Boulevard, and regular buses serve the area. This is not a SkyTrain neighbourhood, but the bus "
      "connection toward King George Station is straightforward."),
    L("Public schools in the area include Chimney Hill Elementary and T.E. Scott Elementary. Catchments can include other nearby schools and "
      "they split by address, so check the ", ('Surrey Schools locator', SD36), ". If you are looking at homes for sale in East Newton, treat "
      "houses and townhouses as two different kinds of purchase, and read a strata package carefully on the older attached homes. More in my ",
      ('East Newton guide', '/east-newton-guide.html'), "."),
],
'north-surrey-homes-for-sale': [
    H('Living in North Surrey'),
    P("North Surrey is a broad board area, not a single neighbourhood. It stretches from the Fraser River and Surrey City Centre out toward "
      "Guildford, Fraser Heights, and the Langley border. North Surrey homes for sale include new condos beside SkyTrain, older houses, "
      "townhouses, and a few larger lots. Fleetwood is a neighbouring part of Surrey, but it is not one of the board’s North Surrey sub-areas."),
    P("The Expo Line (Scott Road, Gateway, Surrey Central, and King George stations) and Highway 1 are the main ways in and out, depending on "
      "which pocket you choose. Schools, shopping, and the daily commute feel different from one community to the next, so it pays to look at "
      "the specific area, not a single picture of living in North Surrey."),
    {'t': 'list', 'items': [
        [{'t': 'Whalley and City Centre', 'h': '/whalley.html'}, {'t': '. This is the urban core, with new condos, SkyTrain, Central City, SFU’s '
         'Surrey campus, and Holland Park. It suits people who want to walk to transit and shops.'}],
        [{'t': 'Guildford', 'h': '/guildford.html'}, {'t': '. A mix of houses, townhouses, and condos, known for Guildford Town Centre and nearby '
         'Green Timbers Urban Forest. Highway 1 is close; SkyTrain is farther than it is in Whalley.'}],
        [{'t': 'Fraser Heights', 'h': '/fraser-heights.html'}, {'t': '. A family house neighbourhood with parks, the Fraser Heights Recreation '
         'Centre, and schools such as Fraser Heights Secondary (check the catchment). Highway 1 is the usual commute. It is not a SkyTrain community.'}],
        [{'t': 'Cedar Hills', 'h': '/cedar-hills.html'}, {'t': '. Established streets of older houses, closer to Scott Road and with easier access '
         'to SkyTrain than Fraser Heights, plus some newer townhouses and duplexes.'}],
        [{'t': 'Bolivar Heights', 'h': '/bolivar-heights.html'}, {'t': '. Older family homes just north of City Centre, around Bolivar Park and '
         'Invergarry Park, with a quieter suburban feel.'}],
        [{'t': 'Bridgeview', 'h': '/bridgeview.html'}, {'t': '. A smaller, river-adjacent pocket near the Pattullo Bridge, with older houses and '
         'some newer townhouses, mixed in with industrial land. Check zoning and flood mapping with the City.'}],
        [{'t': 'Royal Heights', 'h': '/royal-heights.html'}, {'t': '. A hillside pocket of mostly houses, described on the Royal Heights page.'}],
        [{'t': 'Port Kells', 'h': '/port-kells-acreages-for-sale.html'}, {'t': '. A small, more rural corner of northeast Surrey, near Highway 1 '
         'and the Langley border, with larger lots and some acreages. It has a very different feel from City Centre.'}],
    ]},
    P("North Surrey real estate can mean a condo by the station or a house by the highway. The right choice depends on which of these "
      "communities you actually want to live in."),
],
}

for slug, blocks in OV.items():
    p = f'src/data/local/{slug}.json'; d = load(p)
    if any(b.get('gen') == 'ov1119' for b in d['blocks']): continue
    d['blocks'] = [dict(b, gen='ov1119') for b in blocks] + d['blocks']
    if slug == 'north-surrey-homes-for-sale':
        d['suppress'] = sorted(set(d.get('suppress') or []) | {'The eight North Surrey sub-areas'})
    save(p, d); print('overview added:', slug)

# East Newton: the old unsourced "Family Hub" text in the archive page goes (H3 plus its paragraphs).
p = 'src/data/pages/east-newton.json'; d = load(p); out, skip = [], False
for b in d['blocks']:
    if b['t'] == 'h': skip = b.get('text') == "East Newton: Surrey's Family Hub"
    if not skip: out.append(b)
if len(out) != len(d['blocks']): d['blocks'] = out; save(p, d); print('removed Family Hub text from', p)
