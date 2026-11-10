"""Local copy that only one page carries (D-196): for the pages that sat just under the 0.70 unique-text bar after the research-wording clean-up.

Two kinds of section (gen 'story', pos 'end', placed before the page's "Sources" heading):
  - a sales story from Jared's Paragon closed-sales export (src/data/sold/sold-12m.json): the middle half of prices, the price path by quarter,
    typical bedrooms, build year and lot. Same publishing rules as the sold layer: a median needs 5 sales, a count needs 3.
  - hand-written local history and landmarks, each fact from the official or primary source added to the page's Sources list.
Idempotent: earlier 'story' blocks are replaced on every run.
python3 -I tools/build_local_story.py"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local')
SOLD = json.load(open(os.path.join(ROOT, 'src/data/sold/sold-12m.json'), encoding='utf-8'))['sub']
G = 'story'
Q = ['November to January', 'February to April', 'May to July', 'August to October']
NOUN = {'house': 'houses', 'condo': 'condos', 'townhome': 'townhomes', 'duplex': 'duplexes', 'acreage': 'houses on acreage'}


def money(v):
    return f'${v / 1e6:.2f}M'.replace('.00M', 'M') if v >= 1e6 else f'${v:,.0f}'


def path_sentence(name, g, s):
    qs = [(Q[i], q['price']) for i, q in enumerate(s.get('q', [])) if q.get('price')]
    if len(qs) < 2: return ''
    parts = [f'{money(p)} in {lab}' for lab, p in qs]
    lo, hi = min(qs, key=lambda x: x[1]), max(qs, key=lambda x: x[1])
    tail = f' {hi[0]} was the firmest stretch and {lo[0]} the softest.' if hi[1] != lo[1] else ''
    return f'Quarter by quarter, the typical {NOUN[g][:-1] if NOUN[g].endswith("s") else NOUN[g]} in {name} went for ' + ', '.join(parts[:-1]) + f' and {parts[-1]}.' + tail


def type_story(name, g, s):
    n = s.get('n', 0)
    if n < 3: return []
    if n < 5 or not s.get('price'):
        return [f'Only {n} {NOUN[g]} closed in {name} between November 2025 and October 2026, too few to quote a typical price without one sale setting it.']
    bits = []
    if s.get('p25') and s.get('p75'): bits.append(f'The middle half of the {n} {NOUN[g]} that closed in {name} sold between {money(s["p25"])} and {money(s["p75"])}')
    else: bits.append(f'{n} {NOUN[g]} closed in {name}, at a typical {money(s["price"])}')
    who = []
    if s.get('beds'): who.append(f'{s["beds"]} bedrooms')
    if s.get('yb'): who.append(f'a build year around {s["yb"]}')
    if g in ('house', 'acreage') and s.get('lot_sqft'): who.append(f'a lot of about {s["lot_sqft"]:,} square feet')
    if g in ('condo', 'townhome') and s.get('maint'): who.append(f'a strata fee near {money(s["maint"])} a month')
    first = bits[0] + '.'
    if who:
        lead = {'house': 'Typically they had', 'acreage': 'Typically they had', 'condo': 'The typical one had', 'townhome': 'The typical one had'}.get(g, 'Typically they had')
        first += f' {lead} ' + (', '.join(who[:-1]) + ' and ' + who[-1] if len(who) > 1 else who[0]) + '.'
    out = [first]
    speed = []
    if s.get('dom') is not None: speed.append(f'a median {s["dom"]} days on the market')
    if s.get('ratio'): speed.append(f'{s["ratio"]:.1f}% of the asking price')
    if s.get('over') is not None: speed.append(f'{s["over"]}% going over asking')
    if s.get('ppsf'): speed.append(f'about {money(s["ppsf"])} a square foot of living space')
    if len(speed) >= 2: out.append(f'{NOUN[g].capitalize()} in {name} took ' + ', '.join(speed[:-1]) + ' and ' + speed[-1] + ' to sell.' if False else f'For {NOUN[g]} in {name} that meant ' + ', '.join(speed[:-1]) + ' and ' + speed[-1] + '.')
    p = path_sentence(name, g, s)
    if p: out.append(p)
    return out


def sales_blocks(name, key, types, heading=None, path_only=False):
    s = SOLD.get(key)
    if not s: return []
    paras = []
    for g in types:
        if g not in s['groups']: continue
        if path_only:
            x = path_sentence(name, g, s['groups'][g])
            if x: paras.append(x)
        else: paras += type_story(name, g, s['groups'][g])
    if path_only and paras: heading = heading or f'{name} prices through the year (Paragon closed sales)'
    if not paras: return []
    return [{'t': 'h', 'level': 2, 'text': heading or f'What buyers paid in {name}, November 2025 to October 2026 (Paragon closed sales)', 'gen': G, 'pos': 'end'}] + \
           [{'t': 'p', 'text': x, 'gen': G, 'pos': 'end'} for x in paras]


def hand(heading, paras):
    return [{'t': 'h', 'level': 2, 'text': heading, 'gen': G, 'pos': 'end'}] + [{'t': 'p', 'text': x, 'gen': G, 'pos': 'end'} for x in paras]


SRC_BCGN_BF = ('BC Geographical Names · Bridal Falls', 'https://apps.gov.bc.ca/pub/bcgnws/names/34731.html')
SRC_BCGN_POP = ('BC Geographical Names · Popkum', 'https://apps.gov.bc.ca/pub/bcgnws/names/34730.html')
SRC_BCPARKS = ('BC Parks · Bridal Veil Falls Park', 'https://bcparks.ca/bridal-veil-falls-park/')
SRC_FVRD_D = ('FVRD · Electoral Area D', 'https://www.fvrd.ca/EN/main/about-the-fvrd/electoral-areas/electoral-area-d.html')
SRC_SUMAS = ('Heritage Abbotsford · Sumas Lake: a quick look at a long history', 'https://heritageabbotsford.ca/blog/2021/11/30/sumas-lake/')
SRC_BH = ('Fraser Health · Burnaby Hospital opens new health-care pavilion (March 12, 2026)', 'https://www.fraserhealth.ca/news/2026/Mar/Opening-doors-to-enhanced-modernized-patient-care-in-new-facilities')

PAGES = {
  'bridal-falls-guide': (hand('How Bridal Falls got its name, and what is here today', [
      'Bridal Falls takes its name from Bridal Veil Falls, but the post office could not. When the community asked for a "Bridal Veil Falls" post office, the name was already taken elsewhere in Canada, so the office that opened on November 1, 1937 was called Bridal Falls instead. The Province adopted the name for the post office in 1950 and has recognised Bridal Falls as an official community since July 15, 1983.',
      'The falls themselves sit in Bridal Veil Falls Park, a day-use provincial park on the south side of the Fraser River, 16 km east of Chilliwack, reached from exit 135 on Highway 1. The water drops 60 metres over a smooth rock face. In cold winters the falls can freeze into an unstable wall of ice, and BC Parks warns that the base becomes hazardous, with falling ice and rock, so a winter visit is a look from the viewing area rather than a walk to the bottom.',
      'The park is a day-use area with picnic tables, drinking water and toilets, and dogs are welcome on a leash. It is run for BC Parks by a private operator, Sea to Sky Park Services, which is who to call about closures or conditions.',
      'For a buyer, Bridal Falls is the highway-service end of Electoral Area D: the exit, the park, fuel, restaurants and tourist stops sit close to the homes. Owners get the scenery and quick access to Highway 1 and to the bridge north to Agassiz and Highway 9. Area D as a whole had 2,299 residents in the 2021 Census across 223 square kilometres, so homes here come up for sale only a few times a year.',
  ]), [SRC_BCGN_BF, SRC_BCPARKS, SRC_FVRD_D]),
  'popkum-guide': (hand('Popkum, the village under Mount Cheam', [
      'Popkum is the residential heart of FVRD Electoral Area D, the small rural district east of Chilliwack that it shares with Bridal Falls. The Province records Popkum as an official community on the south side of the Fraser River, and two reserves of the Popkum First Nation, Popkum 1 and Popkum 2, lie beside it. The village and the reserves are separate jurisdictions, so a property search here starts with confirming which side of that line a parcel sits on.',
      'Local volunteers wrote the area’s history in a book called "In the Shadow of Mt. Cheam", which the FVRD now hosts in four parts: reminiscences, community stories, family stories and the 1985 homecoming. It is the best single read for anyone who wants to know how the farms and families of this stretch of the valley came to be.',
      'Because Popkum is not a city, its services come from the FVRD, not from Chilliwack: Area D residents are served by FVRD community parks, fire protection, garbage collection, public transit, storm drainage, street lighting and water. The FVRD also posts a quarterly RCMP crime summary for Popkum on its Area D page, a quick way for a buyer to check the area before an offer.',
      'Popkum’s homes come to market rarely: 4 houses closed here between November 2025 and October 2026, too few for a reliable typical price. A buyer looking here is usually choosing a quiet rural lot within a few minutes of Highway 1, and should expect to compare against Chilliwack and Agassiz sales to judge value.',
  ]), [SRC_BCGN_POP, SRC_FVRD_D]),
  'sumas-prairie-guide': (hand('How a lake became Sumas Prairie', [
      'Sumas Prairie was a lake within living memory. Sumas Lake covered roughly 10,000 acres and often tripled in size during the May-to-July freshet; for the Semá:th people of the Stó:lō it was a source of food, a home and a waterway. Settlers farmed around its edge from the 1860s and 1870s, and after a severe flood in 1876 the Province passed a series of dyking and drainage acts, starting with the Sumas Dyking Act of 1878.',
      'The lake was drained under the Sinclair Plan, approved in March 1920. Engineers turned the Vedder River into a canal so it no longer emptied into the lake, built dykes and a dam, and installed pumps at Barrowtown. The first pumps started in July 1923, and by the summer of 1924 the old lake bottom was ready to farm. In 1926 the Canadian Hop Growers Association bought 600 acres of lake bottom and planted what were then the largest hop yards in the Commonwealth; tobacco was grown here too, and two tobacco kilns still stand on the prairie.',
      'A new pumphouse was built between 1980 and 1983, when the Sumas and Vedder dykes were also strengthened. That history is why a farm on the prairie is so productive and why flood protection is the first question to ask about any parcel here: the land sits on a former lake bed kept dry by pumps and dykes.',
  ]), [SRC_SUMAS]),
  'burnaby-hospital-condos-townhomes-for-sale': (hand('The new Burnaby Hospital, open since March 2026', [
      'The neighbourhood’s namesake changed this year. On March 10, 2026 Burnaby Hospital opened a new six-storey health-care pavilion with 83 beds, mostly single rooms with their own washrooms, holding mental-health, maternity, neonatal intensive care and medicine units. A larger emergency department with 23 more treatment spaces and six operating rooms in the Jim Pattison Surgery Centre opened in the expanded support building at the same time.',
      'Fraser Health puts the cost of this part of the redevelopment at about $633 million. The hospital first opened in 1952 and handled more than 75,000 emergency visits and 1,400 births in 2024-25. For condo and townhome owners nearby, a larger hospital can mean more staff looking to live close to work, and more traffic on the streets around the campus.',
  ]), [SRC_BH]),
  'college-park-port-moody-houses-for-sale': (hand('The road that opened up this side of Port Moody', [
      'The Barnet Highway, the main road west from this side of Port Moody to North Burnaby and Vancouver, began as a five-mile wagon road to a lumber mill at the foot of Burnaby Mountain, finished in 1903. It was fully paved around 1930 and widened to four lanes with HOV lanes in the 1990s, a $105 million project, so College Park’s houses, typically built in the 1970s, have always had a direct route into the city.',
  ]), [('Vancouver Is Awesome (Tri-City News) · How the Barnet Highway helped spark growth in Port Moody', 'https://www.vancouverisawesome.com/history/how-the-barnet-highway-helped-spark-growth-in-port-moody-and-the-tri-cities-5161768')]),
}
DATA = {
  'west-newton-guide': ('West Newton', 'Surrey|West Newton', ['house', 'townhome', 'condo']),
  'northwest-maple-ridge-guide': ('Northwest Maple Ridge', 'Maple Ridge|Northwest Maple Ridge', ['house', 'townhome', 'condo']),
  'chilliwack-proper-east-guide': ('Chilliwack Proper East', 'Chilliwack|Chilliwack Proper East', ['house', 'townhome', 'condo']),
  'heritage-woods-port-moody-condos-townhomes-for-sale': ('Heritage Woods', 'Port Moody|Heritage Woods PM', ['townhome', 'condo']),
  'southwest-maple-ridge-condos-townhomes-for-sale': ('Southwest Maple Ridge', 'Maple Ridge|Southwest Maple Ridge', ['townhome', 'condo']),
  'quay-new-westminster-condos-townhomes-for-sale': ('the Quay', 'New Westminster|Quay', ['condo', 'townhome']),
  'aberdeen-guide': ('Aberdeen', 'Abbotsford|Aberdeen', ['house', 'townhome']),
  'panorama-ridge-55-plus-homes-for-sale': ('Panorama Ridge', 'Surrey|Panorama Ridge', ['townhome', 'condo']),
}


def dump(d, t):
    lines = t.split('\n')
    m = re.match(r'^( +)\S', lines[1]) if len(lines) > 2 else None
    s = json.dumps(d, indent=len(m.group(1)), ensure_ascii=False) if m else json.dumps(d, separators=(',', ':'), ensure_ascii=False)
    return s + ('\n' if t.endswith('\n') else '')


def place(slug, blocks, sources):
    f = os.path.join(LOCAL, slug + '.json'); t = open(f, encoding='utf-8').read(); d = json.loads(t)
    B = [b for b in d['blocks'] if b.get('gen') != G]
    at = next((i for i, b in enumerate(B) if b.get('t') == 'h' and re.match(r'^Sources\b', b.get('text', ''))), None)
    if at is None: at = next((i for i, b in enumerate(B) if b.get('t') == 'h' and b.get('text', '') in ('Related pages',)), len(B))
    B = B[:at] + blocks + B[at:]
    if sources:
        si = next((i for i, b in enumerate(B) if b.get('t') == 'h' and re.match(r'^Sources\b', b.get('text', ''))), None)
        if si is not None and si + 1 < len(B) and B[si + 1].get('t') == 'list':
            have = {it[0].get('h') for it in B[si + 1]['items'] if it}
            B[si + 1]['items'] += [[{'t': a, 'h': u}] for a, u in sources if u not in have]
        else:
            B += [{'t': 'h', 'level': 2, 'text': 'Sources for this section', 'gen': G, 'pos': 'end'}, {'t': 'list', 'items': [[{'t': a, 'h': u}] for a, u in sources], 'gen': G, 'pos': 'end'}]
    d['blocks'] = B
    open(f, 'w', encoding='utf-8').write(dump(d, t))


# Paragraphs copied word for word from a sister page: the full text stays on that page and this page links to it (D-196).
L = lambda txt, href: {'t': txt, 'h': href}
POINT = {
  'southwest-maple-ridge-condos-townhomes-for-sale': [
    ('Buyer frame (applies to any townhouse purchase here)', [{'t': 'Buyer costs: the GST rebates, property transfer tax and the first-time buyer exemption are the same anywhere in BC; see '}, L('GST rebates in BC', '/gst-rebate-in-bc.html'), {'t': '.'}]),
    ("Lougheed Transit Corridor (the sub-area's north edge)", [{'t': 'Lougheed Transit Corridor (the north edge of this area): the plan and what it allows are set out in the '}, L('Southwest Maple Ridge guide', '/southwest-maple-ridge-guide.html'), {'t': '.'}]),
    ('Parks and facilities: Hammond Park', [{'t': 'Parks and facilities: Hammond Park and the other parks nearby are listed in the '}, L('Southwest Maple Ridge guide', '/southwest-maple-ridge-guide.html'), {'t': '.'}]),
    ('Health care: Ridge Meadows Hospital', [{'t': 'Health care: Ridge Meadows Hospital, 11666 Laity Street, Maple Ridge.'}]),
  ],
  'heritage-woods-port-moody-condos-townhomes-for-sale': [
    ('Both commute doors matter on this hillside', [{'t': 'Commuting: David Avenue runs both ways, into Coquitlam and into Port Moody; the routes are compared on the '}, L('Heritage Woods neighbourhood page', '/heritage-woods-port-moody.html'), {'t': '.'}]),
    ('Parks and recreation: Bert Flinn Park', [{'t': 'Parks and recreation: Bert Flinn Park borders the neighbourhood; trails and facilities are on the '}, L('Heritage Woods neighbourhood page', '/heritage-woods-port-moody.html'), {'t': '.'}]),
  ],
  'northwest-maple-ridge-guide': [
    ('Form B (SPA s.59)', [{'t': 'Strata paperwork (Form B, depreciation reports, rental and age bylaws): see '}, L('BC townhome buying rules', '/bc-townhome-buying-rules.html'), {'t': '.'}]),
    ('Suites / SSMUH (City)', [{'t': 'Suites and small-scale multi-unit housing follow Maple Ridge’s citywide rules; see the '}, L('Maple Ridge zoning guide', '/zonings.html#zd-mapleridge'), {'t': '.'}]),
    ('Floodplain sorts the low ground', [{'t': 'Floodplain: the Alouette and Fraser river floodplain maps that apply here are explained in the '}, L('North Maple Ridge guide', '/north-maple-ridge-guide.html'), {'t': '.'}]),
    ('Health care: Ridge Meadows Hospital', [{'t': 'Health care: Ridge Meadows Hospital, 11666 Laity Street, Maple Ridge.'}]),
  ],
  'popkum-guide': [('ALR frame: on ALR land', None)],
  'bridal-falls-guide': [('Local government: the FVRD is the local government', [{'t': 'Local government: the FVRD, as for all of Electoral Area D; how that works for owners is set out in the '}, L('Popkum guide', '/popkum-guide.html'), {'t': '.'}])],
  'west-newton-guide': [
    ('Secondary suites: one secondary suite may be permitted', [{'t': 'Secondary suites follow Surrey’s citywide rules; see the '}, L('Surrey zoning guide', '/zonings.html#zd-surrey'), {'t': '.'}]),
    ('A bare-land strata lot is strata tenure on the lot itself', None),
  ],
}


def point(slug, rules):
    f = os.path.join(LOCAL, slug + '.json'); t = open(f, encoding='utf-8').read(); d = json.loads(t); n = 0
    for b in d['blocks']:
        if b.get('t') != 'list': continue
        items = []
        for it in b['items']:
            txt = ''.join(p.get('t', '') for p in it if isinstance(p, dict))
            hit = next((r for r in rules if txt.startswith(r[0])), None)
            if hit: n += 1
            if hit and hit[1] is None: continue
            items.append(hit[1] if hit else it)
        b['items'] = items
    d['blocks'] = [b for b in d['blocks'] if not (b.get('t') == 'list' and not b['items'])]
    open(f, 'w', encoding='utf-8').write(dump(d, t)); return n


def main():
    for slug, rules in POINT.items(): print('point', slug, point(slug, rules))
    for slug, (blocks, src) in PAGES.items(): place(slug, blocks, src); print('hand', slug)
    for slug, v in DATA.items():
        if not v: continue
        bl = sales_blocks(*v, path_only=not (slug.endswith('-guide') or '55-plus' in slug))
        place(slug, bl, []); print('data', slug, max(0, len(bl) - 1), 'paragraphs')


if __name__ == '__main__': main()
