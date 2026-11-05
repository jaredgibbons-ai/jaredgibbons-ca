"""Bedroom pages (D-101): "2 bedroom condos for sale in Langley" and the like, from src/data/sold/sold-beds.json (tools/build_bedroom_layer.py).

Rule (Jared, 2026-11-04): condos get 1, 2 and 3 bedroom pages and townhomes get 2 bedroom pages; no 1 bedroom townhome pages and no 3 bedroom townhome pages
(those are most of the townhome market and the city townhome page already covers them). A page is made only where 5 or more of that type sold in the past year.
Each page has a live-listings placeholder (a bedroom-filtered MyRealPage search, worksheet docs/review/idx/bedroom-searches-*.xlsx), its own sold tables by
neighbourhood and building, a bedroom comparison, the mortgage calculator at the median price, FAQ and links. Idempotent; writes src/data/local/<slug>.json.

    python3 -I tools/build_bedroom_pages.py
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'bed'; LG = 'bedlinks'
SB = json.load(open('src/data/sold/sold-beds.json')); WINDOW = SB['meta']['window']
BANDS = ['Under $600,000', '$600,000 to $799,999', '$800,000 to $999,999', '$1,000,000 to $1,199,999', '$1,200,000 to $1,499,999', '$1,500,000 to $1,799,999', '$1,800,000 and over']
MIN_PAGE = 30   # fewer sales cannot carry its own tables, and every page of this kind scored under 70% unique below 27 sales (D-101); the held combinations are listed in docs/review/bedroom-pages-held.csv
PLAN = {'condo': ['1', '2', '3'], 'townhome': ['2']}
TYPEP = {'condo': 'condos', 'townhome': 'townhomes'}; TYPES = {'condo': 'condo', 'townhome': 'townhome'}
BEDW = {'1': '1 bedroom', '2': '2 bedroom', '3': '3 bedroom'}
BEDROW = {'1': '1 bedroom', '2': '2 bedroom', '3': '3 bedrooms or more'}
NEAR = {'surrey': ['cloverdale', 'south-surrey', 'north-delta', 'langley'], 'south-surrey': ['white-rock', 'surrey', 'cloverdale', 'langley'], 'white-rock': ['south-surrey', 'surrey'],
        'cloverdale': ['surrey', 'langley', 'south-surrey'], 'north-delta': ['surrey', 'ladner', 'tsawwassen'], 'ladner': ['tsawwassen', 'north-delta'], 'tsawwassen': ['ladner', 'north-delta', 'south-surrey'],
        'langley': ['cloverdale', 'surrey', 'abbotsford'], 'abbotsford': ['langley', 'chilliwack'], 'chilliwack': ['abbotsford']}
CITYWORD = re.compile(r'\s+(Surrey|Langley|Abbotsford|Chilliwack|Delta|Tsawwassen|Ladner|White Rock)$')


def exists(s): return os.path.exists(f'src/data/pages/{s}.json') or os.path.exists(f'src/data/local/{s}.json')
def money(v): return '—' if v is None else f'${v:,.0f}'
def nm(s):
    s = s.strip()
    return s if s in ('Fort Langley', 'Langley City') else (CITYWORD.sub('', s) or s)
def slug_of(ck, g, bk): return f'{ck}-{bk}-bedroom-{TYPEP[g]}-for-sale'
def P(t): return {'t': 'p', 'text': t, 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def tbl(cap, head, rows, src=None):
    b = {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'gen': G}
    if src: b['source'] = src
    return b
def lk(t, s): return {'t': t, 'h': f'/{s}.html'}


def pages():
    out = []
    for ck, c in SB['cities'].items():
        for g, bks in PLAN.items():
            for bk in bks:
                e = c['groups'].get(g, {}).get(bk)
                if e and e['n'] >= MIN_PAGE: out.append((ck, g, bk))
    return out


def lead(i, e, bed, types, city):
    p, d = e.get('price'), e.get('dom')
    mid = f", with the middle half between {money(e['p25'])} and {money(e['p75'])}" if e.get('p25') else ''
    pp = f" at {money(e['ppsf'])} a square foot" if e.get('ppsf') else ''
    r = f" and sold for {e['ratio']}% of the asking price at a median" if e.get('ratio') else ''
    V = [f"The median price of a {bed} {types[:-1] if types.endswith('s') else types} in {city} was {money(p)}{mid}. They took {d} days to sell at a median.",
         f"A typical {bed} {types[:-1]} in {city} sold for {money(p)} after {d} days on the market{pp}.",
         f"{e['n']} sold in {city} at a median of {money(p)}{pp}, taking {d} days{r}.",
         f"Across {e['n']} sales the median was {money(p)}{mid}, and the median time to sell was {d} days.",
         f"In {city}, {bed} {types} sold for a median of {money(p)}{pp}{r}."]
    return V[i % 5]


def build():
    plan = pages(); slugs = {(a, b, c): slug_of(a, b, c) for a, b, c in plan}
    for s in slugs.values(): assert not os.path.exists(f'src/data/pages/{s}.json'), s
    made = []
    for i, (ck, g, bk) in enumerate(plan):
        c = SB['cities'][ck]; city = c['name']; e = c['groups'][g][bk]; types = TYPEP[g]; typ = TYPES[g]; bed = BEDW[bk]; slug = slugs[(ck, g, bk)]
        Types = types.capitalize(); n = e['n']; k3 = ' (3 or more)' if bk == '3' else ''
        title = f"{bed.title()} {Types} for Sale in {city} BC | Jared Gibbons"
        if len(title) > 62: title = f"{bed.title()} {Types} for Sale in {city} | Jared Gibbons"
        if len(title) > 62: title = f"{bed.title()} {Types} for Sale in {city}"
        desc = f"{bed.capitalize()} {types} for sale in {city}: live MLS® listings, plus what {n} sold for over the past year, typical price and strata fee."
        if len(desc) > 158: desc = f"{bed.capitalize()} {types} for sale in {city}: live MLS® listings and what {n} sold for over the past year."
        INTRO = [f"The search below shows {bed} {types} for sale in {city} from the MLS®. Under it are the prices {n} of them sold for over the past year, by neighbourhood and building.",
                 f"Looking for a {bed} {typ} in {city}? The search below lists the ones on the MLS® now, and the tables under it show what {n} sold for in the past year and where.",
                 f"{city} {bed} {types}: live MLS® listings in the search below, then sold prices from the past year, {n} sales in all.",
                 f"These are {bed} {types} in {city} on the MLS®, with what {n} sold for over the past year underneath, split by neighbourhood and building.",
                 f"Browse {bed} {types} for sale in {city} below. The tables that follow come from the {n} that sold over the past year."]
        bl = [P(INTRO[i % 5]), P(lead(i, e, bed, types, city)), {'t': 'grid', 'gen': G}]
        # --- measures
        rows = [['Sales', str(n)], ['Median price', money(e['price'])]]
        if e.get('p25'): rows.append(['Middle half of prices', f"{money(e['p25'])} to {money(e['p75'])}"])
        if e.get('ppsf'): rows.append(['Price per square foot', money(e['ppsf'])])
        rows.append(['Days to sell', str(e['dom'])])
        if e.get('ratio'): rows.append(['Sold price as a share of list price', f"{e['ratio']}%"])
        rows.append(['Sales over the list price', f"{e['over']}%"])
        if e.get('sqft'): rows.append(['Median size', f"{e['sqft']:,} sq ft"])
        if e.get('yb'): rows.append(['Median year built', str(e['yb'])])
        if e.get('maint'): rows.append(['Strata fee a month', money(e['maint'])])
        src = f"Source: Paragon closed sales, {WINDOW}, {c['desc']}" + ('; 3 bedroom means 3 or more.' if bk == '3' else '.')
        bl += [H(f"{bed.capitalize()} {types} in {city}: what sold over the past year"), tbl(f"{bed.capitalize()} {types} sold in {city}", ['Measure', f'{bed.capitalize()} {types}'], rows, src)]
        # --- quarters
        q = e.get('q') or []; labs = ['November 2025 to January 2026', 'February to April 2026', 'May to July 2026', 'August to October 2026']
        qr = [[labs[j], str(x['n']), money(x['price'])] for j, x in enumerate(q) if x['n']]
        if sum(1 for x in q if x['price']) >= 2: bl.append(tbl(f"Median price by quarter, {bed} {types} in {city}", ['Quarter', 'Sales', 'Median price'], qr))
        # --- neighbourhoods
        subs = e.get('subs') or []
        if subs:
            bl.append(H(f"{bed.capitalize()} {types} by neighbourhood in {city}"))
            if len(subs) >= 2:
                pr = sorted([s for s in subs if s.get('price')], key=lambda s: s['price'])
                bl.append(P(f"Of the {len(subs)} neighbourhoods with 5 or more sales, {nm(pr[-1]['name'])} had the highest median at {money(pr[-1]['price'])} and {nm(pr[0]['name'])} the lowest at {money(pr[0]['price'])}. {nm(subs[0]['name'])} had the most sales, {subs[0]['n']}."))
            else:
                bl.append(P(f"{nm(subs[0]['name'])} had {subs[0]['n']} of the {n} sales."))
            bl.append(tbl(f"{bed.capitalize()} {types} sold by neighbourhood, {city}", ['Neighbourhood', 'Sales', 'Median price', 'Price per sq ft', 'Days to sell'],
                          [[nm(s['name']), str(s['n']), money(s.get('price')), money(s.get('ppsf')), str(s['dom']) if s.get('dom') is not None else '—'] for s in subs[:12]]))
        tops = [x for x in subs if x.get('top')][:8]
        if tops:
            bl.append(P(f"Which buildings sit behind those neighbourhood figures:"))
            bl.append({'t': 'list', 'items': [[{'t': f"{nm(x['name'])}: " + '; '.join(f"{c['name']}, {c['n']} sales" + (f" at a median of {money(c['price'])}" if c['n'] >= 5 and c.get('price') else '') + (f", built {c['yb']}" if c.get('yb') else '') for c in x['top'])}] for x in tops], 'gen': G})
        # --- buildings
        cx_all = [x for x in (e.get('complexes') or []) if x['n'] >= 3]; cx = cx_all[:8]
        if cx:
            bl.append(H(f"Buildings with {bed} sales in {city}"))
            bl.append(P(f"{len(cx_all)} {'building or complex' if len(cx_all) == 1 else 'buildings and complexes'} had 3 or more {bed} {typ} sales: " + ', '.join(x['name'] for x in cx[:3]) + ('.' if len(cx_all) <= 3 else ' and others.')))
            bl.append(tbl(f"Buildings and complexes, {bed} {types} sold in {city}", ['Building', 'Sales', 'Median price', 'Year built', 'Strata fee a month'],
                          [[x['name'], str(x['n']), money(x['price']) if x['n'] >= 5 else '—', str(x['yb']) if x.get('yb') else '—', money(x['maint']) if x['n'] >= 5 and x.get('maint') else '—'] for x in cx]))
        else:
            bl.append(P(f"No single building or complex had 3 or more {bed} {typ} sales in {city}, so none is named."))
        # --- compare bedrooms and cities
        grp = c['groups'][g]
        bl.append(H(f"How {bed} {types} in {city} compare"))
        sents = []
        for nxt in [x for x in ('1', '2', '3') if x != bk and x in grp and abs(int(x) - int(bk)) == 1]:
            o = grp[nxt]
            if o['n'] >= 5 and o.get('price'):
                d = e['price'] - o['price']; word = 'more' if d > 0 else 'less'
                t = f"A {bed} {typ} in {city} sold for {money(abs(d))} {word} at the median than a {BEDW[nxt]}{' or larger' if nxt == '3' else ''} one ({money(e['price'])} against {money(o['price'])}, {o['n']} sales)."
                if e.get('maint') and o.get('maint'): t += f" The strata fee was {money(e['maint'])} a month against {money(o['maint'])}."
                sents.append(t)
        if g == 'townhome' and '3' in grp and grp['3']['n'] >= 5 and not sents:
            o = grp['3']; d = e['price'] - o['price']; sents.append(f"{bed.capitalize()} townhomes in {city} sold for {money(abs(d))} {'more' if d > 0 else 'less'} at the median than townhomes with 3 or more bedrooms ({money(e['price'])} against {money(o['price'])}).")
        for t in sents: bl.append(P(t))
        peers = [(ck2, c2['groups'][g][bk]) for ck2, c2 in SB['cities'].items() if g in c2['groups'] and bk in c2['groups'][g] and c2['groups'][g][bk]['n'] >= MIN_PAGE and c2['groups'][g][bk].get('price')]
        if len(peers) >= 3:
            rk = sorted(peers, key=lambda x: -x[1]['price']); pos = [x[0] for x in rk].index(ck) + 1
            ordn = {1: 'highest', 2: 'second highest', 3: 'third highest'}.get(pos, f'{pos}th highest')
            if pos == len(rk): ordn = 'lowest'
            elif pos == len(rk) - 1: ordn = 'second lowest'
            lo, hi = rk[-1], rk[0]
            bl.append(P(f"Of the {len(rk)} cities with {bed} {typ} pages, {city} has the {ordn} median price. {SB['cities'][lo[0]]['name']} is lowest at {money(lo[1]['price'])} and {SB['cities'][hi[0]]['name']} highest at {money(hi[1]['price'])}."))
        near = [(ck, e)] + [(nk, SB['cities'][nk]['groups'][g][bk]) for nk in NEAR.get(ck, []) if g in SB['cities'][nk]['groups'] and bk in SB['cities'][nk]['groups'][g] and SB['cities'][nk]['groups'][g][bk]['n'] >= 5]
        if len(near) >= 2:
            bl.append(tbl(f"{bed.capitalize()} {types}: {city} and nearby", ['City', 'Sales', 'Median price', 'Price per sq ft', 'Days to sell', 'Strata fee a month'],
                          [[SB['cities'][k2]['name'] + (' (this page)' if k2 == ck else ''), str(x['n']), money(x.get('price')), money(x.get('ppsf')), str(x['dom']), money(x.get('maint')) if x.get('maint') else '—'] for k2, x in near]))
        # --- size and age
        sz = [x for x in (e.get('size') or [])]
        if len(sz) >= 2: bl.append(tbl(f"{bed.capitalize()} {types} sold in {city} by size", ['Size', 'Sales', 'Median price'], [[x['label'], str(x['n']), money(x['price'])] for x in sz]))
        ag = [x for x in (e.get('age') or [])]
        if len(ag) >= 2: bl.append(tbl(f"{bed.capitalize()} {types} sold in {city} by age of building", ['Building age', 'Sales', 'Median price'], [[x['label'], str(x['n']), money(x['price'])] for x in ag]))
        # --- bands
        br = [[BANDS[j], str(x)] for j, x in enumerate(e.get('bands') or []) if x]
        if br: bl.append(tbl(f"{bed.capitalize()} {types} sold in {city} by price range", ['Price range', 'Sales'], br))
        # --- calculator
        bl += [H(f"Estimate the payment on a {bed} {typ} in {city}"), P(f"The calculator starts at the median price of {money(e['price'])}."), {'t': 'calc', 'which': 'mortgage', 'price': e['price'], 'gen': G}]
        # --- links
        city_pages = [(f"{city} {types} for sale", f'{ck}-{types}-for-sale'), (f"{city} {'townhomes' if g == 'condo' else 'condos'} for sale", f"{ck}-{'townhomes' if g == 'condo' else 'condos'}-for-sale")]
        pairs = [(t, s) for t, s in city_pages if exists(s)]
        for b2 in PLAN['condo'] + ['t2']:
            gg, bb = ('townhome', '2') if b2 == 't2' else ('condo', b2)
            if (gg, bb) != (g, bk) and (ck, gg, bb) in slugs: pairs.append((f"{BEDW[bb].capitalize()} {TYPEP[gg]} in {city}", slugs[(ck, gg, bb)]))
        for nk in NEAR.get(ck, []):
            if (nk, g, bk) in slugs: pairs.append((f"{bed.capitalize()} {types} in {SB['cities'][nk]['name']}", slugs[(nk, g, bk)]))
        for sfx in ('condos-under-800k', 'townhomes-under-1-2m'):
            if sfx.startswith(types) and exists(f'{ck}-{sfx}'): pairs.append((f"{city} {types} under {'$800,000' if 'condos' in sfx else '$1.2 million'}", f'{ck}-{sfx}'))
        pairs += [('Mortgage calculator for BC', 'mortgage-calculator'), ('First-time buyer calculator', 'first-time-buyer-calculator'), ('BC condo buying rules', 'bc-condo-buying-rules'), ('First-time home buyer program in BC', 'first-time-home-buyer-program')]
        bl += [{'t': 'h', 'level': 2, 'text': f"More {city} {types} and buying guides", 'gen': G, 'pos': 'end'}, {'t': 'list', 'items': [[lk(t, s)] for t, s in pairs if exists(s)], 'gen': G, 'pos': 'end'}]
        # --- FAQ
        QA = [f"How much does a {bed} {typ} cost in {city}?", f"What do {bed} {types} sell for in {city}?", f"What is the price of a {bed} {typ} in {city} right now?"][i % 3]
        QB = [f"How long does a {bed} {typ} take to sell in {city}?", f"How fast do {bed} {types} sell in {city}?", f"Are {bed} {types} in {city} selling quickly?"][i % 3]
        QC = [f"Which {city} neighbourhood has the most {bed} {types} sales?", f"Where in {city} do most {bed} {types} sell?", f"Which parts of {city} sell the most {bed} {types}?"][i % 3]
        faq = [dict(q=QA, a=f"Of the {bed} {types} in {city}, {n} sold over the past year at a median of {money(e['price'])}" + (f", with the middle half between {money(e['p25'])} and {money(e['p75'])}." if e.get('p25') else '.'), gen=G),
               dict(q=QB, a=f"The median was {e['dom']} days" + (f", and homes sold for {e['ratio']}% of the list price at a median." if e.get('ratio') else '.'), gen=G)]
        if subs: faq.append(dict(q=QC, a=f"{nm(subs[0]['name'])}, with {subs[0]['n']} of the {n} sales" + (f" at a median of {money(subs[0]['price'])}." if subs[0].get('price') else '.'), gen=G))
        if cx: faq.append(dict(q=f"Which buildings in {city} have {bed} {types} for sale most often?", a=f"By sales over the past year: " + '; '.join(f"{x['name']} ({x['n']} sales" + (f", median {money(x['price'])}" if x['n'] >= 5 else '') + ')' for x in cx[:4]) + '.', gen=G))
        if e.get('maint'): faq.append(dict(q=f"What is the strata fee on a {bed} {typ} in {city}?", a=f"The median strata fee on the {bed} {types} that sold in {city} was {money(e['maint'])} a month. Fees vary by building, so check the building's own figure.", gen=G))
        parent = next((s for t, s in pairs if exists(s) and s.startswith(f'{ck}-{types}')), None)
        crumbs = [{'name': 'Home', 'href': '/index.html'}] + ([{'name': f"{city} {types}", 'href': f'/{parent}.html'}] if parent else []) + [{'name': f"{bed.capitalize()} {types}", 'href': f'/{slug}.html'}]
        j = dict(status='generated', slug=slug, updated='2026-11-04', new_page=dict(title=title, description=desc, h1=f"{bed.title()} {Types} for Sale in {city}"), breadcrumbs=crumbs,
                 faq_heading=f"{bed.capitalize()} {types} in {city}: your questions answered", faq=faq, blocks=bl, bedroom_page=dict(city=ck, type=g, beds=bk))
        json.dump(j, open(f'src/data/local/{slug}.json', 'w'), indent=1, ensure_ascii=False); made.append(slug)
    return plan, slugs, made


def inbound(plan, slugs):
    def patch(host, heading, pairs):
        f = f'src/data/local/{host}.json'
        j = json.load(open(f)) if os.path.exists(f) else {'status': 'generated', 'slug': host, 'updated': '2026-11-04', 'blocks': []}
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != LG]
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': heading, 'gen': LG, 'pos': 'end'}, {'t': 'list', 'items': [[lk(t, s)] for t, s in pairs], 'gen': LG, 'pos': 'end'}]
        json.dump(j, open(f, 'w'), indent=1, ensure_ascii=False)
    n = 0
    for ck in SB['cities']:
        city = SB['cities'][ck]['name']
        for g in ('condo', 'townhome'):
            pairs = [(f"{BEDW[bk].capitalize()} {TYPEP[gg]} in {city}", slugs[(ck, gg, bk)]) for (c2, gg, bk) in plan if c2 == ck and (gg == g or (g == 'condo' and False))]
            host = f'{ck}-{TYPEP[g]}-for-sale'
            if pairs and exists(host): patch(host, f"{city} {TYPEP[g]} by number of bedrooms", pairs); n += 1
            elif os.path.exists(f'src/data/local/{host}.json'):
                jj = json.load(open(f'src/data/local/{host}.json')); jj['blocks'] = [b for b in jj['blocks'] if b.get('gen') != LG]; json.dump(jj, open(f'src/data/local/{host}.json', 'w'), indent=1, ensure_ascii=False)
    return n


def held_and_clean(made):
    import csv, glob
    keep = set(made)
    for f in glob.glob('src/data/local/*.json'):
        j = json.load(open(f))
        if j.get('bedroom_page') and os.path.basename(f)[:-5] not in keep: os.remove(f)
    rows = []
    for ck, c in SB['cities'].items():
        for g, bks in PLAN.items():
            for bk in bks:
                e = c['groups'].get(g, {}).get(bk)
                if e and 5 <= e['n'] < MIN_PAGE: rows.append([slug_of(ck, g, bk), c['name'], f'{bk} bedroom {TYPEP[g]}', e['n'], e.get('price')])
    os.makedirs('docs/review', exist_ok=True)
    with open('docs/review/bedroom-pages-held.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['slug that would be used', 'city', 'type', 'sales in the past year', 'median price']); w.writerows(sorted(rows, key=lambda r: -r[3]))
    return len(rows)


if __name__ == '__main__':
    plan, slugs, made = build()
    print(held_and_clean(made), 'held (5 to 29 sales)')
    print(len(made), 'bedroom pages;', inbound(plan, slugs), 'inbound link blocks')
