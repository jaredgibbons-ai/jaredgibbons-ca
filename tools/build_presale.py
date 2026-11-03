"""Build presale pages from the researcher's master list.
    python3 -I tools/build_presale.py [--csv docs/research/presale-master-list-2026-11-01.csv] [--asof 2026-11-01]
Writes src/data/presale/<asof>.json (cleaned rows) and src/data/local/<slug>.json for the hub, city pages and two layers on existing pages.
Rules (D-47): a price is shown only if the source dates it within 3 months of the snapshot; otherwise 'Ask for current pricing'.
Deposit wording is shown as published; blanks stay blank. No developer or sales-centre claims are added. Source URLs stay in the data file, not on pages."""
import argparse, csv, json, os, re, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ap = argparse.ArgumentParser(); ap.add_argument('--csv', default='docs/research/presale-master-list-2026-11-01.csv'); ap.add_argument('--asof', default='2026-11-01'); a = ap.parse_args()
MON = ['January','February','March','April','May','June','July','August','September','October','November','December']
asof_y, asof_m = int(a.asof[:4]), int(a.asof[5:7]); ASOF = f'{MON[asof_m-1]} {asof_y}'
rows = list(csv.DictReader(open(os.path.join(ROOT, a.csv), encoding='utf-8')))
NP = {'', 'not published'}

def price(s):
    seg = s.split(';')[0]
    m = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*(?:\d{1,2},\s*)?(\d{4})', seg)
    d = re.search(r'\$\s?[\d,]+(?:\.\d+)?\s?[Kk]?', seg)
    if not (m and d): return None
    mi = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(m.group(1)); y = int(m.group(2))
    if (asof_y - y) * 12 + (asof_m - 1 - mi) > 2: return None   # older than ~3 months
    raw = d.group(0).strip(); num = re.sub(r'[^\d.]', '', raw.rstrip('Kk'))
    amt = '$' + ('{:,.0f}'.format(float(num) * (1000 if raw.upper().endswith('K') else 1)) if '.' not in num or num.replace('.', '').isdigit() else num)
    after = seg[d.end():d.end() + 1]
    gst = ' + GST' if re.search(r'\+\s*GST', seg) else ''
    q = re.match(r'\s*(\d)[\s-]*bed(?:room)?s?(?:\s+homes)?\s+(?:from|start(?:s|ing)?(?:\s+at|\s+for)?)\b', seg, re.I)
    qual = f'{q.group(1)}-bedroom homes ' if q else ''
    if after == 's':   # "$400,000s" means a range starting in the $400,000s
        return {'text': f'{qual}Priced in the {amt}s', 'asof': f'{MON[mi]} {y}'}
    return {'text': f'{qual}From {amt}{gst}' if not qual else f'{qual}from {amt}{gst}', 'asof': f'{MON[mi]} {y}'}

def homes(s):
    s = s.strip()
    if not s or s == 'not published': return None
    n = re.match(r'\d[\d,]*', s)
    if not n: return None
    return {'n': int(n.group(0).replace(',', '')), 'exact': bool(re.fullmatch(r'\d[\d,]*', s))}

def ptype(t):
    t = t.lower()
    if 'single' in t or 'duplex' in t: return 'Houses and duplexes' if 'single' in t else 'Duplexes'
    if 'townhome' in t and 'condo' in t: return 'Condo and townhome'
    if 'townhome' in t: return 'Townhome'
    return 'Condo'

def short(s, n=120):
    s = s.strip()
    if s in NP: return ''
    s = re.sub(r'\s*\((?:per [^)]*|Stewart[^)]*|source[^)]*)\)', '', s)
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0].rstrip(',;:') + '…'

P = []
for r in rows:
    h = homes(r['Total homes']); pr = price(r['Pricing'])
    P.append({'name': r['Project name'].strip(), 'address': r['Address'].strip(), 'city': r['City'].strip(), 'board': r['Board area'].strip(),
              'developer': '' if r['Developer'].strip() in NP else r['Developer'].strip(), 'type': ptype(r['Type']), 'type_source': r['Type'].strip(),
              'homes': h, 'year': int(r['Completion year']), 'completion_source': r['Completion estimate (source wording)'].strip(), 'status': r['Status'].strip(),
              'price': pr, 'deposit': short(r['Deposit structure']), 'incentive': short(r['Assignment/incentives'], 140), 'sources': [u.strip() for u in re.findall(r'https?://[^\s;()]+', r['Source URLs'])]})
os.makedirs(os.path.join(ROOT, 'src/data/presale'), exist_ok=True)
json.dump({'asof': a.asof, 'note': 'Compiled by Muse from REW, developer pages and other public presale pages, read 2026-11-01. Prices shown on pages only when dated within 3 months of the snapshot.', 'projects': P}, open(os.path.join(ROOT, f'src/data/presale/{a.asof}.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

def table(ps, caption):
    body = []
    for p in sorted(ps, key=lambda x: (x['year'], x['name'].lower())):
        hs = '' if not p['homes'] else ('{:,}'.format(p['homes']['n']) + ('' if p['homes']['exact'] else '*'))
        body.append([p['name'], p['address'], p['developer'] or 'not published', p['type'], hs or 'n/p', str(p['year']),
                     (p['price']['text'] + f" ({p['price']['asof']})") if p['price'] else 'Ask for current pricing', p['deposit'] or 'not published'])
    return {'t': 'table', 'caption': caption, 'head': ['Project', 'Address', 'Developer', 'Type', 'Homes', 'Completion', 'Published price', 'Deposit (as published)'], 'rows': body,
            'source': f"Compiled from public presale listings and developers' own project pages, read {a.asof}. Completion years are estimates from the sources. n/p = not published. * the sources give a different count or a breakdown. Prices and availability are set by developers and change without notice; this is not an offer to sell."}

def stats(ps):
    n = len(ps); yr = collections.Counter(p['year'] for p in ps); ty = collections.Counter(p['type'] for p in ps)
    priced = [p for p in ps if p['price']]; dep = sum(1 for p in ps if p['deposit']); dev = collections.Counter(p['developer'] for p in ps if p['developer'])
    return n, yr, ty, priced, dep, dev

PL = {'Condo': ('condo project', 'condo projects'), 'Townhome': ('townhome project', 'townhome projects'), 'Condo and townhome': ('mixed condo and townhome project', 'mixed condo and townhome projects'), 'Duplexes': ('duplex project', 'duplex projects'), 'Houses and duplexes': ('house project', 'house projects')}
def lead(city, ps):
    n, yr, ty, priced, dep, dev = stats(ps)
    ys = ', '.join(f"{yr[y]} in {y}" for y in sorted(yr))
    tys = ', '.join(f"{c} {PL[k][0] if c == 1 else PL[k][1]}" for k, c in ty.most_common())
    out = [f"The list holds {n} presale projects in {city} with estimated completion between {min(yr)} and {max(yr)}: {ys}. By type, that is {tys}."]
    if priced:
        low = min(priced, key=lambda p: float(re.sub(r'[^\d.]', '', re.sub(r'[Kk]$', '000', p['price']['text'].split('$')[1].split(' ')[0]))))
        out.append(f"{len(priced)} of the {n} have a price published and dated within the last three months. The lowest published starting price is at {low['name']}: {low['price']['text'][0].lower() + low['price']['text'][1:]}. For the other {n - len(priced)}, the price is either not published or the price I have is too old to show, so ask me for the current list.")
    else:
        out.append(f"None of the {n} has a price I can show with a recent date, so ask me for the current price list.")
    out.append(f"A deposit structure is published for {dep} of the {n}.")
    top = [(d, c) for d, c in dev.most_common() if c >= 2]
    if top: out.append('Developers with more than one project here: ' + ', '.join(f'{d} ({c})' for d, c in top) + '.')
    big = [p for p in ps if p['homes'] and p['homes']['exact']]
    if big:
        b = max(big, key=lambda p: p['homes']['n']); out.append(f"The largest project with a confirmed home count is {b['name']} at {b['homes']['n']:,} homes.")
    return out

def faq(city, ps):
    n, yr, ty, priced, dep, dev = stats(ps); y1 = sorted(yr)[0]
    return [{'q': f'How many presale projects are completing in {city} between {min(yr)} and {max(yr)}?', 'a': f"{n} projects are on my list as of {ASOF}: " + ', '.join(f"{yr[y]} completing in {y}" for y in sorted(yr)) + ". The list covers projects marketed publicly. Projects sold only through private channels may be missing."},
            {'q': f'What kinds of presale homes are being built in {city}?', 'a': 'The mix is ' + ', '.join(f"{c} {PL[k][0] if c == 1 else PL[k][1]}" for k, c in ty.most_common()) + '.'}]

def notice(): return {'t': 'notice', 'text': f"Draft for Jared's approval. Built from Muse's presale list ({a.asof}). Prices appear only where the source dates them within three months. Paragon presale data is still to be merged, and projects sold through private channels may be missing."}
CTA = {'t': 'p', 'text': 'Ask Jared about a presale project', 'h': '/contact.html'}
HOW = {'t': 'p', 'text': 'How presales work in BC: tax, deposits and the 7-day rescission period', 'h': '/new-construction-presales-in-langley-bc.html'}

def write(slug, d):
    p = os.path.join(ROOT, 'src/data/local', slug + '.json'); json.dump(d, open(p, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(p, 'a').write('\n'); print('wrote', slug)

def city_page(slug, city, hub_href, hub_name, ps, extra_intro=''):
    n, yr, ty, priced, dep, dev = stats(ps)
    b = [notice(), {'t': 'p', 'text': f"Presale means you buy a home before it is built, and you take possession when it completes. This page lists every {city} presale project on my list that is scheduled to complete between {min(yr)} and {max(yr)}, with the developer, type, size and deposit where the sources publish them." + extra_intro}]
    b += [{'t': 'h', 'level': 2, 'text': f'{city} presale projects at a glance'}] + [{'t': 'p', 'text': t} for t in lead(city, ps)]
    b += [{'t': 'h', 'level': 2, 'text': f'All {city} presale projects completing {min(yr)}–{max(yr)}'}, table(ps, f'{city} presale projects, snapshot {a.asof}'), HOW, CTA]
    write(slug, {'status': 'draft', 'slug': slug, 'updated': a.asof,
      'new_page': {'title': f'{city} Presale Condos & Townhomes {min(yr)}–{max(yr)} | Jared Gibbons',
                   'description': f'{n} {city} presale projects completing {min(yr)}–{max(yr)}: developers, home types, deposit structures and current published prices. Updated {ASOF}.',
                   'h1': f'{city} Presale Condos and Townhomes Completing {min(yr)}–{max(yr)}'},
      'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': hub_name, 'href': hub_href}, {'name': f'{city} presales', 'href': f'/{slug}.html'}],
      'faq_heading': f'{city} presales: your questions answered', 'blocks': b, 'faq': faq(city, ps),
      'needs_from_muse': ['Paragon presale records for ' + city, 'Jared first-hand view of the projects he has toured or sold', 'Neighbourhood for each project (sources give addresses only)']})

by = collections.defaultdict(list)
for p in P: by[p['city']].append(p)
HUB = '/presale-projects-fraser-valley-and-metro-vancouver.html'; HUBN = 'Presale projects'
for city, slug, hubh, hubn in [('Surrey', 'surrey-presale-condos-and-townhomes', '/surrey-homes-for-sale.html', 'Surrey'), ('Abbotsford', 'abbotsford-presale-condos-and-townhomes', '/abbotsford-homes-for-sale.html', 'Abbotsford'),
                               ('Burnaby', 'burnaby-presale-condos-and-townhomes', '/burnaby-homes-for-sale.html', 'Burnaby'), ('Coquitlam', 'coquitlam-presale-condos-and-townhomes', '/coquitlam-homes-for-sale.html', 'Coquitlam'),
                               ('Vancouver', 'vancouver-presale-condos-and-townhomes', '/vancouver-homes-for-sale.html', 'Vancouver')]:
    city_page(slug, city, hubh, hubn, by[city])

# hub: everything, Fraser Valley first
order = ['Surrey', 'Langley', 'Abbotsford', 'Delta', 'Maple Ridge', 'Burnaby', 'Coquitlam', 'Vancouver', 'Port Coquitlam', 'Port Moody', 'New Westminster', 'Richmond', 'North Vancouver', 'West Vancouver', 'Squamish']
assert set(order) == set(by), set(by) ^ set(order)
n, yr, ty, priced, dep, dev = stats(P); fvn = [p for p in P if p['board'] == 'Fraser Valley']
hb = [notice(), {'t': 'p', 'text': f"This is my working list of publicly marketed presale projects in the Fraser Valley and Metro Vancouver that are scheduled to complete between {min(yr)} and {max(yr)}. It starts with the Fraser Valley, where I work, and then covers Metro Vancouver. Each table shows the developer, home type, size, estimated completion year, a published price where one is current, and the deposit as published."},
      {'t': 'h', 'level': 2, 'text': 'The list at a glance'},
      {'t': 'p', 'text': f"The list holds {n} projects: " + ', '.join(f"{yr[y]} completing in {y}" for y in sorted(yr)) + f". {len(fvn)} fall in the Fraser Valley Real Estate Board area and {n - len(fvn)} in the Greater Vancouver REALTORS® area. Of the {n}, {len(priced)} have a price published within the last three months and {dep} have a deposit structure published."},
      {'t': 'p', 'text': 'By city: ' + ', '.join(f"{c} {len(by[c])}" for c in order if len(by[c]) >= 3) + ', and the rest in smaller numbers.'}]
OWN = {'Surrey': '/surrey-presale-condos-and-townhomes.html', 'Abbotsford': '/abbotsford-presale-condos-and-townhomes.html', 'Burnaby': '/burnaby-presale-condos-and-townhomes.html',
       'Coquitlam': '/coquitlam-presale-condos-and-townhomes.html', 'Vancouver': '/vancouver-presale-condos-and-townhomes.html', 'Langley': '/new-construction-presales-in-langley-bc.html'}
# A city that has its own presale page shows its full table there, not here (a repeated table makes both pages weaker); the hub links to it.
hb += [{'t': 'table', 'caption': f'Presale projects by city, snapshot {a.asof}', 'head': ['City', 'Projects', 'Completing', 'Types on the list', 'Full list'],
        'rows': [[c, str(len(by[c])), f"{min(p['year'] for p in by[c])}–{max(p['year'] for p in by[c])}" if min(p['year'] for p in by[c]) != max(p['year'] for p in by[c]) else str(by[c][0]['year']),
                  ', '.join(f"{k.lower()} ({v})" for k, v in collections.Counter(p['type'] for p in by[c]).most_common()), 'Own page' if c in OWN else 'Table below'] for c in order],
        'source': f'Compiled from public presale listings, read {a.asof}.'}]
hb += [{'t': 'p', 'text': f'{c} presale projects: full table, {len(by[c])} projects', 'h': OWN[c]} for c in order if c in OWN]
for c in order:
    if c in OWN: continue
    ps = by[c]; hb += [{'t': 'h', 'level': 2, 'text': f'{c} presale projects ({len(ps)})'}, table(ps, f'{c} presale projects, snapshot {a.asof}')]
hb += [HOW, CTA]
write('presale-projects-fraser-valley-and-metro-vancouver', {'status': 'draft', 'slug': 'presale-projects-fraser-valley-and-metro-vancouver', 'updated': a.asof,
  'new_page': {'title': f'Fraser Valley & Metro Vancouver Presales {min(yr)}–{max(yr)} | Jared Gibbons', 'description': f'{n} presale condo and townhome projects completing {min(yr)}–{max(yr)} across the Fraser Valley and Metro Vancouver, with developers, deposits and current published prices. Updated {ASOF}.',
                'h1': f'Presale Projects in the Fraser Valley and Metro Vancouver, Completing {min(yr)}–{max(yr)}'},
  'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': HUBN, 'href': HUB}], 'faq_heading': 'Presale list: your questions answered', 'blocks': hb,
  'faq': [{'q': 'Is this every presale project in the region?', 'a': f"No. It covers projects marketed publicly through presale listings and developers' own pages as of {ASOF}. Projects sold only through private or brokerage-exclusive channels may be missing, and Paragon presale data is still to be added."},
          {'q': 'Why do some projects say to ask for current pricing?', 'a': 'A price is shown only when its source dates it within the last three months. Presale prices change often, and an older price can mislead, so I give the current list on request.'},
          {'q': 'Where do the completion dates come from?', 'a': "From the developers' own pages and public presale listings. Completion estimates move, so treat them as targets and confirm with the developer."}],
  'needs_from_muse': ['Paragon presale records to merge', 'Appendix A/B projects (completion not stated; unconfirmed in-window)', 'Chilliwack, Mission, White Rock and Hope projects, none are on the list yet']})

# layers on existing archive pages (blocks only; archive text untouched)
lg = by['Langley']; n2, yr2, *_ = stats(lg)
write('new-construction-presales-in-langley-bc', {'status': 'draft', 'slug': 'new-construction-presales-in-langley-bc', 'updated': a.asof,
  'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'Langley', 'href': '/langley-homes-for-sale.html'}, {'name': 'Langley presales', 'href': '/new-construction-presales-in-langley-bc.html'}],
  'blocks': [notice(), {'t': 'h', 'level': 2, 'text': f'Langley presale projects completing {min(yr2)}–{max(yr2)}'}] + [{'t': 'p', 'text': t} for t in lead('Langley', lg)] + [table(lg, f'Langley presale projects, snapshot {a.asof}')]})
ss = [p for p in by['Surrey'] if p['name'] in ('Calais', 'Rockford', 'Harlowe')]
write('south-surrey-new-construction-presales', {'status': 'draft', 'slug': 'south-surrey-new-construction-presales', 'updated': a.asof,
  'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'South Surrey', 'href': '/south-surrey-homes-for-sale.html'}, {'name': 'South Surrey presales', 'href': '/south-surrey-new-construction-presales.html'}],
  'blocks': [notice(), {'t': 'h', 'level': 2, 'text': 'South Surrey presale projects on my list'},
             {'t': 'p', 'text': f"Three projects on my list sit in the South Surrey area, going by the locations the sources give: Calais at Semiahmoo Town Centre, Rockford at 128 Street and 17 Avenue in Ocean Park, and Harlowe at 16485 18 Avenue, described by its sources as Sunnyside Heights and Grandview Heights. All three are scheduled to complete between {min(p['year'] for p in ss)} and {max(p['year'] for p in ss)}."},
             table(ss, f'South Surrey presale projects, snapshot {a.asof}')]})
