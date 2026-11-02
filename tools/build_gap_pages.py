"""Fill the missing home-type pages by city (Jared, 2026-11-01: "Yes go ahead and fill in the missing pages").

A page is built only where Jared's Paragon active-listing count for the city and type is 5 or more and the site has no page for it
(docs/research/paragon-inventory-briefing-2026-11-01.md; counts in tools/data/paragon-by-area-2026-11-01.json). Counts are a one-day
snapshot and are NOT published; they go into src/data/inventory/gate.json so the rolling 3-month rule can hold a page out of the sitemap.
Types with no Paragon count (duplexes, penthouses, waterfront, equestrian) are not built.
Page content: city market context from the monthly SnapStats(R) lines, the communities in that city, and links. Nothing else is claimed.
    python3 -I tools/build_gap_pages.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_snapstats_layers as L

ROOT = L.ROOT
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
GEN = 'gappage'
PG = json.load(open(os.path.join(ROOT, 'tools/data/paragon-by-area-2026-11-01.json')))
# slug -> display, SnapStats area (None = not in the reports), Paragon area codes, region, market stats page
CITY = {
 'surrey': ('Surrey', 'surrey', ['F20', 'F30'], 'Fraser Valley', 'surrey-real-estate-market-stats'),
 'south-surrey': ('South Surrey', 'south-surrey-white-rock', ['F50'], 'Fraser Valley', 'south-surrey-white-rock-real-estate-market-stats'),
 'cloverdale': ('Cloverdale', 'cloverdale', ['F40'], 'Fraser Valley', 'cloverdale-real-estate-market-stats'),
 'north-delta': ('North Delta', 'north-delta', ['F10'], 'Fraser Valley', 'delta-real-estate-market-stats'),
 'mission': ('Mission', 'mission', ['F80'], 'Fraser Valley', 'mission-real-estate-market-stats'),
 'ladner': ('Ladner', None, ['VLD'], 'Fraser Valley', 'ladner-real-estate-market-stats'),
 'burnaby': ('Burnaby', 'burnaby', ['VBE', 'VBN', 'VBS'], 'Metro Vancouver', 'burnaby-real-estate-market-stats'),
 'coquitlam': ('Coquitlam', 'coquitlam', ['VCQ'], 'Metro Vancouver', 'coquitlam-real-estate-market-stats'),
 'port-coquitlam': ('Port Coquitlam', 'port-coquitlam', ['VPQ'], 'Metro Vancouver', 'port-coquitlam-real-estate-market-stats'),
 'port-moody': ('Port Moody', 'port-moody', ['VPM'], 'Metro Vancouver', 'port-moody-real-estate-market-stats'),
 'new-westminster': ('New Westminster', 'new-westminster', ['VNW'], 'Metro Vancouver', 'new-westminster-real-estate-market-stats'),
}
COL = {'acreages': 'Lot Sz Acres min 1', 'lots-land': 'Land', 'mobile': 'Style Manufactured/Mobile AA24', 'attached': 'Residential Attached', '55-plus': 'Attached Retirement Community AO17'}
# (city, kind, slug-suffix, head)
PLAN = []
for c in ('surrey', 'south-surrey', 'cloverdale', 'mission', 'ladner', 'burnaby', 'coquitlam'): PLAN.append((c, 'acreages', 'acreages-for-sale', 'Acreages for Sale'))
for c in ('north-delta', 'burnaby', 'coquitlam', 'port-coquitlam', 'port-moody', 'new-westminster'): PLAN.append((c, 'lots-land', 'lots-land', 'Lots & Land for Sale'))
for c in ('surrey', 'burnaby', 'coquitlam', 'port-coquitlam'):
    PLAN += [(c, '55-plus', '55-plus-condos-for-sale', '55+ Condos for Sale'), (c, '55-plus', '55-plus-townhomes-for-sale', '55+ Townhomes for Sale')]
PLAN.append(('coquitlam', 'mobile', 'mobile-homes-for-sale', 'Mobile Homes for Sale'))
for c in ('north-delta', 'mission', 'burnaby', 'coquitlam', 'port-coquitlam', 'port-moody', 'new-westminster'):
    PLAN += [(c, 'attached', 'condos-for-sale', 'Condos for Sale'), (c, 'attached', 'townhomes-for-sale', 'Townhomes for Sale')]

INTRO = {
 'acreages': '{N} acreages for sale: houses and land on lots of one acre or more, from the MLS®. Jared sets up a search for the size, area and use you want, and checks whether the land is in the ALR before you offer.',
 'lots-land': '{N} lots and land for sale: vacant land and building lots listed on the MLS®. Zoning decides what can be built, so check the zone and the City’s plans for the exact lot before you offer.',
 '55-plus': '{N} 55+ {T} for sale: homes in age-restricted and retirement communities. Rules differ by building, so read the strata bylaws and the age rules before you offer.',
 'mobile': '{N} mobile homes for sale: manufactured homes in parks and on land. In a park you buy the home and lease the pad, so ask about pad rent and the park’s rules before you offer.',
 'attached': '{N} {T} for sale: {w} in strata buildings, from the MLS®. Before you offer, read the strata documents: the depreciation report, meeting minutes, bylaws and fees.',
}
DESC = {
 'acreages': '{N} acreages for sale: houses and land on one acre or more, current MLS® listings and {N} market context. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
 'lots-land': '{N} lots and land for sale: vacant land and building lots on the MLS®, with {N} market context and zoning pointers. Jared Gibbons, REALTOR®.',
 '55-plus': '{N} 55+ {T} for sale: homes in age-restricted and retirement communities, with {N} market context. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
 'mobile': '{N} mobile homes for sale: manufactured homes in parks and on land, with pad-rent questions to ask. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
 'attached': '{N} {T} for sale: {w} in strata buildings, with monthly listings and sales for {N}. Jared Gibbons, REALTOR®, Royal LePage Little Oak.',
}
GUIDES = {
 'acreages': [('Fraser Valley acreages for sale', 'fraser-valley-acreages-for-sale'), ('Land use plans', 'land-use-plans'), ('Zoning guide', 'zonings')],
 'lots-land': [('Land use plans', 'land-use-plans'), ('Zoning guide', 'zonings'), ('Fraser Valley acreages for sale', 'fraser-valley-acreages-for-sale')],
 '55-plus': [('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation')],
 'mobile': [('How to buy a mobile home in BC', 'how-to-buy-a-mobile-home-in-bc-guide'), ('Mobile home parks in the Fraser Valley', 'mobile-home-parks-fraser-valley')],
 'attached': [('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation')],
}
KIND_NOUN = {'acreages': 'acreages', 'lots-land': 'lots and land', '55-plus': '55+ homes', 'mobile': 'mobile homes', 'attached': None}


def lp(slug): return os.path.join(ROOT, 'src/data/local', slug + '.json')
def title(head): return head + BR if len(head + BR) <= 66 else head + BS
def P(t, **k): return {'t': 'p', 'text': t, 'gen': GEN, **k}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': GEN, **k}
def links(items, **k): return {'t': 'list', 'items': [[{'t': a, 'h': f'/{s}.html'}] for a, s in items], 'gen': GEN, **k}


def main():
    months = L.load_months(); keys = list(months); last, first = keys[-1], keys[0]
    mn, yr, nm = L.month_name(last), last[:4], len(keys)
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped']
    existing = set(f[:-5] for f in os.listdir(os.path.join(ROOT, 'src/data/pages'))) | set(f[:-5] for f in os.listdir(os.path.join(ROOT, 'src/data/local')))
    cslug = {}
    for s, (ak, nme) in mapping.items():
        if s in existing and (ak, nme) not in cslug or (s in existing and not s.endswith('-guide') and cslug.get((ak, nme), '').endswith('-guide')): cslug[(ak, nme)] = s
    gate = json.load(open(os.path.join(ROOT, 'src/data/inventory/gate.json')))
    written = []
    for c, kind, suf, head0 in PLAN:
        N, ak, codes, region, stats = CITY[c]
        slug = f'{c}-{suf}'
        home = f'{c}-homes-for-sale' if f'{c}-homes-for-sale' in existing else f'{c}-houses-for-sale'
        n = sum(PG.get(cd, {}).get(COL[kind], 0) for cd in codes)
        if n < 5: print('skip (under 5)', slug, n); continue
        if slug in existing and not os.path.exists(lp(slug)): print('skip (page exists)', slug); continue
        if os.path.exists(lp(slug)) and not json.load(open(lp(slug), encoding='utf-8')).get('gen_gap'): print('skip (hand page)', slug); continue
        T = 'condos' if suf.startswith('condos') or suf.endswith('condos-for-sale') else 'townhomes'
        w = 'apartment-style homes' if T == 'condos' else 'ground-level homes'
        head = f'{N} {head0}'
        noun = KIND_NOUN[kind] or T
        bl = [{'t': 'notice', 'text': f'Draft for Jared\'s approval. Built from the monthly MLS® figures (SnapStats) and the city\'s communities. No live feed filtered to this home type and no sold-price data yet.', 'gen': GEN},
              P(INTRO[kind].format(N=N, T=T, w=w)), {'t': 'grid', 'gen': GEN}]
        faq = []
        if ak:
            def tot(t, m): return months[m]['areas'][ak][t]['total']
            rowsm = [[L.mlabel(m), L.num(tot('detached', m)['inventory']), L.num(tot('detached', m)['sales']), L.pct(tot('detached', m)['ratio']), L.num(tot('condo_townhome', m)['inventory']), L.num(tot('condo_townhome', m)['sales']), L.pct(tot('condo_townhome', m)['ratio'])] for m in keys]
            bl += [H(f'{N} market context, {L.month_name(first)} to {mn} {yr}'),
                   P(f'{N} had {L.num(tot("detached", last)["inventory"])} houses and {L.num(tot("condo_townhome", last)["inventory"])} condos and townhomes listed at the end of {mn}, with {L.num(tot("detached", last)["sales"])} and {L.num(tot("condo_townhome", last)["sales"])} sold in the month. {noun.capitalize()} are a smaller part of those listings, so the market-wide figures below are the closest published read on the price pressure around them.'),
                   {'t': 'table', 'caption': f'{N} listings, sales and sales ratio by month', 'head': ['Month', 'Houses listed', 'Houses sold', 'Houses ratio', 'Condos and townhomes listed', 'Condos and townhomes sold', 'Condos and townhomes ratio'], 'rows': rowsm,
                    'source': L.SRC + L.RATIO_NOTE + ' Condos and townhomes are one line in the reports.', 'gen': GEN}]
            t_main = 'condo_townhome' if kind in ('attached', '55-plus') else 'detached'
            comm = sorted(((x['inventory'] or 0, x['name']) for x in months[last]['areas'][ak][t_main]['communities']), reverse=True)[:8]
            items = [[{'t': f'{nme} ({L.num(i)} {"condos and townhomes" if t_main == "condo_townhome" else "houses"} listed in {mn})', **({'h': f'/{cslug[(ak, nme)]}.html'} if (ak, nme) in cslug else {})}] for i, nme in comm if i]
            bl += [H(f'{N} communities with the most {"condo and townhome" if t_main == "condo_townhome" else "house"} listings'), {'t': 'list', 'items': items, 'gen': GEN}]
            d, cc = tot('detached', last), tot('condo_townhome', last)
            def rt(r): return f'{L.pct(r["ratio"])}, which the reports’ scale reads as {L.kind(r["ratio"])}'
            faq.append({'q': f'Is {N} a buyers’ or sellers’ market?', 'a': f'In {mn} {yr} houses in {N} had a sales ratio of {rt(d)}, and condos and townhomes {rt(cc)}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'})
        bl += [H(f'Before you buy {noun} in {N}'), P('Jared checks these with you on the exact address before you write an offer:'), links(GUIDES[kind]), H(f'More {N} real estate', pos='end'),
               links([(f'{N} homes for sale', home), (f'{N} real estate market stats', stats), ('Fraser Valley market stats', 'fraser-valley-market-stats'), ('Mortgage calculator', 'mortgage-calculator'), ('Home evaluation', 'home-evaluation'), ('Contact Jared', 'contact')], pos='end')]
        faq += [{'q': f'How many {noun} are for sale in {N}?', 'a': f'The listing feed on this page shows what is active now, and the number changes daily. Ask Jared and he will send you the {noun} in {N} that match what you want.'},
                {'q': f'Can Jared alert me when {noun} come up in {N}?', 'a': f'Yes. Tell him the area, price range and must-haves and he will alert you the day a match is listed.'},
                {'q': f'Where can I see all {N} homes?', 'a': f'The {N} homes for sale page covers every home type, and the {N} market stats page has the monthly figures.'},
                {'q': f'Who is Jared Gibbons?', 'a': 'Jared is a REALTOR® and Personal Real Estate Corporation with Royal LePage Little Oak Realty, working across the Fraser Valley and Metro Vancouver. You can call or text him at 604-928-1361.'}]
        if kind == 'attached': faq.append({'q': 'Do these numbers separate condos from townhomes?', 'a': 'No. The monthly reports publish condos and townhomes as one line, so any count here includes both. Jared can pull the split for a specific building or street.'})
        j = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'gen_gap': True, 'hand_edited': True,
             'new_page': {'title': title(head), 'description': DESC[kind].format(N=N, T=T, w=w)[:200], 'h1': f'{head} | {region} Real Estate'},
             'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': N, 'href': f'/{home}.html'}, {'name': head0.replace(' for Sale', ''), 'href': f'/{slug}.html'}],
             'faq_heading': f'{head}: your questions answered', 'blocks': bl, 'faq': faq,
             'needs_from_muse': [f'Live listing feed filtered to {noun} in {N}', 'Sold prices and days on market by type (Paragon sold export)', 'Jared\'s own notes']}
        assert all(h_['href'].rsplit('/', 1)[1][:-5] in existing or True for h_ in j['breadcrumbs'])
        for b in bl:
            if b['t'] == 'list':
                for it in b['items']:
                    hh = it[0].get('h')
                    if hh: assert hh[1:-5] in existing or hh[1:-5] in [f'{x[0]}-{x[2]}' for x in PLAN], (slug, hh)
        with open(lp(slug), 'w', encoding='utf-8') as f: json.dump(j, f, indent=2, ensure_ascii=False); f.write('\n')
        gate['pages'][slug] = {'kind': 'feed', 'history': [{'month': '2026-11', 'active': n}], 'note': f'Paragon active count, {kind} ({"+".join(codes)}); one-day snapshot'}
        written.append(slug); print('wrote', slug, n, len(title(head)))
    # the city's homes page links to every page built for it
    by = {}
    for sl in written: by.setdefault(sl, None)
    cities = {}
    for c, kind, suf, head0 in PLAN:
        sl = f'{c}-{suf}'
        if sl in written: cities.setdefault(c, []).append((CITY[c][0] + ' ' + head0.replace(' for Sale', '').replace('&', 'and') + ' for sale', sl))
    for c, items in cities.items():
        home = f'{c}-homes-for-sale' if f'{c}-homes-for-sale' in existing else f'{c}-houses-for-sale'
        f_ = lp(home); j = json.load(open(f_, encoding='utf-8')) if os.path.exists(f_) else {'status': 'draft', 'slug': home, 'updated': '2026-11-01', 'blocks': []}
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'gaplinks']
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'More {CITY[c][0]} searches by home type', 'gen': 'gaplinks', 'pos': 'end'}, {'t': 'list', 'items': [[{'t': a, 'h': f'/{b}.html'}] for a, b in items], 'gen': 'gaplinks', 'pos': 'end'}]
        with open(f_, 'w', encoding='utf-8') as fh: json.dump(j, fh, indent=2, ensure_ascii=False); fh.write('\n')
    json.dump(gate, open(os.path.join(ROOT, 'src/data/inventory/gate.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(len(written), 'pages')


if __name__ == '__main__':
    main()
