"""Replace archive sections that repeat word for word across sibling pages (Jared, 2026-11-01: "can you add all these pages?").

Archive records are never edited. A repeated section is switched off on a page through the page's local file (`suppress`, which
hides every block under that level-2 heading except listing feeds, forms and reviews), so removing the page's entry brings the archived
wording back. Where the section is real advice, its one copy moves to a hub page and each page links to it.
Not touched: tools and forms (ALR address checker, "Looking at a home in X?"), and the region-specific "Before you buy in X" / "Planning in X" lists.
    python3 -I tools/replace_repeats.py     (then: link_pages.py, build, assign_reviews.py, uniqueness.py)
"""
import glob, json, os, re, sys, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uniqueness import text_of
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
GEN = 'repeatfix'
HUBS_KEEP_GUIDES = {'maple-ridge-neighbourhood-guides', 'pitt-meadows-neighbourhood-guides', 'chilliwack-neighbourhood-guides', 'langley-neighbourhood-guides', 'abbotsford-houses-for-sale', 'chilliwack-houses-for-sale'}
KEEP = {'Farm Markets': {'langley-farms'}, 'Explore the Area': {'city-of-langley-homes-for-sale'}, 'Langley Sub-Areas': {'city-of-langley-homes-for-sale'}}
# heading -> kept on these pages only (None = nowhere)
HEAD_RULES = {'Related guides': HUBS_KEEP_GUIDES, 'Related Abbotsford Real Estate Searches & Guides': HUBS_KEEP_GUIDES, 'Associated Pages': HUBS_KEEP_GUIDES,
              'Explore Associated Chilliwack & Sardis Real Estate Searches & Guides': HUBS_KEEP_GUIDES, 'Current MLS® Availability & Unit Alerts': set(), **KEEP}
STARTS = ('Buying or Selling at ',)
CHECK = re.compile(r'^What to look at in an? (.+) home$')
HUB = {'surrey': ('surrey-home-buyer-checklist', 'Surrey Home Buyer Checklist: What to Check', 'Surrey home buyer checklist', 'fleetwood-tynehead-guide'),
       'tsawwassen': ('tsawwassen-home-buyer-checklist', 'Tsawwassen Home Buyer Checklist: What to Check', 'Tsawwassen home buyer checklist', 'tsawwassen-central-guide')}
TSAW = {'Tsawwassen Central', 'Tsawwassen East', 'Tsawwassen North'}


def lp(slug): return os.path.join(ROOT, 'src/data/local', slug + '.json')
def load(slug): return json.load(open(lp(slug), encoding='utf-8')) if os.path.exists(lp(slug)) else {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
def save(slug, j):
    with open(lp(slug), 'w', encoding='utf-8') as f: json.dump(j, f, indent=2, ensure_ascii=False); f.write('\n')


def sections(blocks):
    out, cur, buf = [], None, []
    for i, b in enumerate(blocks):
        if b['t'] == 'h' and b['level'] <= 2:
            if cur: out.append((cur, buf))
            cur, buf = (b['text'], i) if b['level'] == 2 else None, []
        elif cur: buf.append(b)
    if cur: out.append((cur, buf))
    return out


def main():
    pages = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    # which headings repeat (same text on 2+ pages), so a unique section with a common title is left alone
    h = collections.defaultdict(set)
    for s, p in pages.items():
        for (t, _), buf in sections(p['blocks']):
            h[(t, hashlib.md5(' '.join(text_of(b) for b in buf).encode()).hexdigest())].add(s)
    plan = collections.defaultdict(lambda: {'suppress': set(), 'checks': []})
    for s, p in pages.items():
        for (t, _), buf in sections(p['blocks']):
            sig = (t, hashlib.md5(' '.join(text_of(b) for b in buf).encode()).hexdigest())
            if len(h[sig]) < 2: continue
            if t in HEAD_RULES and s not in HEAD_RULES[t]: plan[s]['suppress'].add(t)
            elif t.startswith(STARTS): plan[s]['suppress'].add(t)
            elif (m := CHECK.match(t)):
                plan[s]['suppress'].add(t); plan[s]['checks'].append(m.group(1))
    # hub pages hold the one copy of the checklist (same facts as the archive cards, set out as plain lists)
    def sec(title, look, ask, watch): return [{'t': 'h', 'level': 2, 'text': title, 'gen': GEN}, {'t': 'list', 'items': [[{'t': 'Look at: ' + look}], [{'t': 'Ask: ' + ask}], [{'t': 'Watch for: ' + watch}]], 'gen': GEN}]
    STRATA = ('Strata fees, the depreciation report (the plan for future repairs), meeting minutes and bylaws', 'About upcoming special levies (extra one-time charges) and what the fees include')
    HUBS = {
     'surrey': dict(intro='These are the questions I go through with buyers before they write an offer. Ask Jared about any item that applies to the home you are looking at.',
        secs=[('Detached houses', 'Lot size, the age of the roof, furnace, plumbing and wiring, and drainage', 'What the zone allows, and whether any suite was built with a permit', 'Assuming you can add a suite or rebuild just because a neighbour did'),
              ('Townhomes and condos (strata living)', *STRATA, 'Pet, rental or age rules that don’t fit your plans'),
              ('Acreage and large rural lots', 'ALR status, well water if there is no city water, septic, and how the land drains in winter', 'What the zone allows for a second home, outbuildings and animals', 'Streams and ravines that limit where you can build')],
        faq=[('What should I check on a Surrey house?', 'Lot size, the age of the roof, furnace, plumbing and wiring, and drainage. Ask what the zone allows and whether any suite was built with a permit.'),
             ('What should I check before buying a Surrey townhome or condo?', 'Strata fees, the depreciation report (the plan for future repairs), meeting minutes and bylaws. Ask about upcoming special levies (extra one-time charges) and what the fees include, and watch for pet, rental or age rules that don’t fit your plans.'),
             ('Can I add a suite or rebuild because my neighbour did?', 'Not necessarily. Ask what the zone allows on your lot and whether any existing suite was built with a permit.'),
             ('What matters on a large or rural lot in Surrey?', 'ALR status, well water if there is no city water, septic, and how the land drains in winter. Ask what the zone allows for a second home, outbuildings and animals, and watch for streams and ravines that limit where you can build.'),
             ('Who can help me check a specific address?', 'Send Jared the address and he will go through these points with you before you write an offer.')],
        more=('More Surrey real estate', [('Surrey homes for sale', '/surrey-homes-for-sale.html'), ('Surrey real estate market stats', '/surrey-real-estate-market-stats.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Home evaluation', '/home-evaluation.html'), ('Contact Jared', '/contact.html')])),
     'tsawwassen': dict(intro='These are the questions I go through with buyers before they write an offer. Ask Jared about any item that applies to the home you are looking at.',
        secs=[('Detached houses', 'Lot size, the age of the roof, furnace, plumbing and wiring, and the street', 'What the zone allows, and whether any suite was permitted', 'Assuming you can rebuild or add a suite just because a neighbour did'),
              ('Townhomes (strata living)', *STRATA, 'Pet or age rules that don’t fit your plans'),
              ('Shoreline, low and waterfront lots', 'How high the lot sits, drainage, and any rules on the title (covenants)', 'How high the living space must be built, and whether work on the shore needs a seawall designed by an engineer', 'Insurance costs or limits. Get a quote before you remove subjects (the conditions in your offer).')],
        faq=[('What should I check on a Tsawwassen house?', 'Lot size, the age of the roof, furnace, plumbing and wiring, and the street. Ask what the zone allows and whether any suite was permitted.'),
             ('What should I check before buying a Tsawwassen townhome?', 'Strata fees, the depreciation report (the plan for future repairs), meeting minutes and bylaws. Ask about upcoming special levies (extra one-time charges) and what the fees include, and watch for pet or age rules that don’t fit your plans.'),
             ('What matters on a low or waterfront lot?', 'How high the lot sits, drainage, and any rules on the title (covenants). Ask how high the living space must be built and whether work on the shore needs a seawall designed by an engineer.'),
             ('Should I get an insurance quote before I buy near the water?', 'Yes. Insurance costs or limits can apply, so get a quote before you remove subjects (the conditions in your offer).'),
             ('Who can help me check a specific address?', 'Send Jared the address and he will go through these points with you before you write an offer.')],
        more=('More Delta real estate', [('Tsawwassen homes for sale', '/tsawwassen-homes-for-sale.html'), ('Delta homes for sale', '/delta-homes-for-sale.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Home evaluation', '/home-evaluation.html'), ('Contact Jared', '/contact.html')]))}
    for key, (slug, ttl, label, src) in HUB.items():
        d = HUBS[key]; hub = load(slug)
        hub['blocks'] = [{'t': 'p', 'text': d['intro'], 'gen': GEN}] + [x for sc in d['secs'] for x in sec(*sc)]
        hub['blocks'] += [{'t': 'h', 'level': 2, 'text': d['more'][0], 'gen': GEN, 'pos': 'end'}, {'t': 'list', 'items': [[{'t': a, 'h': h_}] for a, h_ in d['more'][1]], 'gen': GEN, 'pos': 'end'}]
        hub['faq'] = [{'q': q, 'a': a} for q, a in d['faq']]; hub['faq_heading'] = f'{label.capitalize()}: your questions answered'
        hub.update({'status': 'draft', 'new_page': {'title': ttl + ' | Jared Gibbons', 'description': f'{label.capitalize()}: what to look at in a house, a townhome or condo, and a larger lot, and what to ask before you write an offer. Jared Gibbons, REALTOR®.', 'h1': 'What to Look at When Buying a ' + ('Surrey' if key == 'surrey' else 'Tsawwassen') + ' Home'},
                    'hand_edited': True, 'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': label, 'href': f'/{slug}.html'}]})
        save(slug, hub)
    n = 0
    for s, pl in plan.items():
        j = load(s)
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != GEN]
        old = [x for x in j.get('suppress', []) if x not in j.get('suppress_gen', [])]
        j['suppress_gen'] = sorted(pl['suppress']); j['suppress'] = old + [x for x in j['suppress_gen'] if x not in old]
        for name in pl['checks']:
            slug, _, label, _ = HUB['tsawwassen' if name in TSAW else 'surrey']
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'Before you buy in {name}', 'gen': GEN, 'pos': 'end'},
                            {'t': 'p', 'parts': [{'t': f'What to look at in a house, a townhome or condo, and a larger lot, and what to ask before you write an offer, is in the '}, {'t': label, 'h': f'/{slug}.html'}, {'t': f'. Send Jared the address in {name} and he will check it with you.'}], 'gen': GEN, 'pos': 'end'}]
        save(s, j); n += 1
    print('pages changed', n, '| sections switched off', sum(len(p['suppress']) for p in plan.values()))


if __name__ == '__main__':
    main()
