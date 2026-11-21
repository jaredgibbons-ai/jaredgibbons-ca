#!/usr/bin/env python3
"""Commercial real estate by city, and by category in four areas (D-389).

Jared, Nov 20 2026: "commercial should just be metro vancouver and the fraser valley, can we do each city for commercial? and then south surrey and
langley cloverdale and abbotsford we can ... break it down into categories" -> categories "industrial, office, retail, land and business".
Lease listings are left out (for sale only), an assumption Jared was told about.

    python3 -I tools/build_commercial_pages.py      -> src/data/local/<slug>.json (new pages) + docs/review/idx/commercial-searches-2026-11-20.xlsx

Facts on the pages come only from data already on the site, each with its source:
  - commercial sales by municipality and by asset class, Q2 2026: Greater Vancouver REALTORS® Commercial Edge (the table on
    /fraser-valley-commercial-market-report.html, read from its local file so the two pages never disagree)
  - industrial vacancy, rents and new supply by submarket, Q3 2026: Avison Young Metro Vancouver industrial report (same page)
  - zones: the municipal zoning bylaw summaries behind /zonings.html (dist/zoning-zones.json is built from the same data; this reads the build)
Every page has a listings grid; until Gerry's saved search comes back the launch gate holds the page (empty listings box), as for other new pages.
"""
import json, os, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
G = 'comm'; DAY = '2026-11-20'
ZONES = json.load(open('dist/zoning-zones.json'))
REP = json.load(open('src/data/local/fraser-valley-commercial-market-report.json'))
T = [b for b in REP['blocks'] if b.get('t') == 'table']
ASSET = {r[0]: r for r in T[0]['rows']}
MUNI = {r[0]: r for r in T[1]['rows']}
IND = {r[0]: r for r in T[2]['rows']}
SRC_GVR = 'Greater Vancouver REALTORS® Commercial Edge, Q2 2026 (as reported on [the Fraser Valley commercial market report](/fraser-valley-commercial-market-report.html))'
SRC_AY = 'Avison Young, Metro Vancouver industrial market report, Q3 2026 (as reported on [the Fraser Valley commercial market report](/fraser-valley-commercial-market-report.html))'

def P(t): return {'t': 'p', 'text': t, 'gen': G}
def H(t, l=2): return {'t': 'h', 'level': l, 'text': t, 'gen': G}
def L(items):
    out = []
    for i in items:
        m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', i)
        out.append([{'t': m.group(1), 'h': m.group(2)}] if m else [{'t': i}])
    return {'t': 'list', 'items': out, 'gen': G}
def TB(cap, head, rows, src): return {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, 'source': src, 'gen': G}
def chk_title(t): assert 30 <= len(t) <= 60, (len(t), t); return t
def chk_desc(d): assert 110 <= len(d) <= 160, (len(d), d); return d

# ------------------------------------------------------------------ cities (Metro Vancouver and the Fraser Valley)
# key: (name, MLS areas for Gerry, municipality row in the GVR table, Avison Young submarket, zoning keys)
CITIES = {
    'surrey': ('Surrey', 'Surrey + North Surrey + Cloverdale + South Surrey White Rock (exclude the White Rock sub-area)', 'Surrey', 'Surrey', ['surrey']),
    'south-surrey-white-rock': ('South Surrey and White Rock', 'South Surrey White Rock', 'Surrey', 'Surrey', ['surrey', 'whiterock']),
    'cloverdale': ('Cloverdale', 'Cloverdale', 'Surrey', 'Surrey', ['surrey']),
    'langley': ('Langley', 'Langley', 'Langley', 'Langley', ['langley', 'langleycity']),
    'abbotsford': ('Abbotsford', 'Abbotsford', 'Abbotsford', 'Abbotsford', ['abbotsford']),
    'chilliwack': ('Chilliwack', 'Chilliwack + Sardis + Yarrow', 'Chilliwack', 'Chilliwack', []),
    'mission': ('Mission', 'Mission', 'Mission', None, []),
    'maple-ridge': ('Maple Ridge', 'Maple Ridge', 'Maple Ridge', 'Maple Ridge / Pitt Meadows', []),
    'pitt-meadows': ('Pitt Meadows', 'Pitt Meadows', 'Pitt Meadows', 'Maple Ridge / Pitt Meadows', ['pittmeadows']),
    'delta': ('Delta', 'Ladner + Tsawwassen + North Delta', 'Delta', 'Delta', ['delta']),
    'vancouver': ('Vancouver', 'Vancouver West + Vancouver East', None, None, ['vancouver']),
    'burnaby': ('Burnaby', 'Burnaby North + Burnaby South + Burnaby East', None, None, ['burnaby']),
    'richmond': ('Richmond', 'Richmond', None, None, []),
    'coquitlam': ('Coquitlam', 'Coquitlam', None, None, ['coquitlam']),
    'port-coquitlam': ('Port Coquitlam', 'Port Coquitlam', None, None, []),
    'port-moody': ('Port Moody', 'Port Moody', None, None, []),
    'new-westminster': ('New Westminster', 'New Westminster', None, None, []),
    'north-vancouver': ('North Vancouver', 'North Vancouver', None, None, []),
    'west-vancouver': ('West Vancouver', 'West Vancouver', None, None, []),
}
FV = ['surrey', 'south-surrey-white-rock', 'cloverdale', 'langley', 'abbotsford', 'chilliwack', 'mission', 'maple-ridge', 'pitt-meadows', 'delta']
MV = ['vancouver', 'burnaby', 'richmond', 'coquitlam', 'port-coquitlam', 'port-moody', 'new-westminster', 'north-vancouver', 'west-vancouver']
MUNI_LABEL = {'surrey': 'City of Surrey', 'langley': 'Township of Langley', 'langleycity': 'City of Langley', 'abbotsford': 'Abbotsford', 'whiterock': 'White Rock',
              'pittmeadows': 'Pitt Meadows', 'delta': 'Delta', 'vancouver': 'Vancouver', 'burnaby': 'Burnaby', 'coquitlam': 'Coquitlam'}

# ------------------------------------------------------------------ categories (four areas)
CATS = {
    'industrial': dict(slug='industrial-property-for-sale', label='Industrial Property', short='industrial', mls='Industrial', asset='Industrial'),
    'office': dict(slug='office-space-for-sale', label='Office Space', short='office', mls='Office', asset='Office'),
    'retail': dict(slug='retail-space-for-sale', label='Retail Space', short='retail', mls='Retail', asset='Retail & other'),
    'land': dict(slug='commercial-land-for-sale', label='Commercial Land', short='commercial land', mls='Land (commercial / industrial)', asset='Land'),
    'business': dict(slug='businesses-for-sale', label='Businesses', short='business', mls='Business (with or without property)', asset=None),
}
AREAS = {'south-surrey': ('South Surrey', 'south-surrey-white-rock', 'South Surrey White Rock'), 'langley': ('Langley', 'langley', 'Langley'),
         'cloverdale': ('Cloverdale', 'cloverdale', 'Cloverdale'), 'abbotsford': ('Abbotsford', 'abbotsford', 'Abbotsford')}

SKIP = re.compile(r'Cemetery|Assembly|Institutional|Child Care|Golf|Marina|Campground|Gas|Service Station|Car Wash|Recreation|Park, Open|School|Health Campus|University|'
                  r'Shelter|River Zone|Fraser River|Butcher|Game Farm|Forces|Farm Auction|Liquor Primary|Pub|Customs|Civic|Church|Community Care|Special Housing|Entertainment|Tourist|Casino|Cannabis', re.I)
def zones(mkeys):
    out = []
    for k, v in ZONES.items():
        m = k.split('-')[1]
        if m not in mkeys or v['t'] != 'Other' or SKIP.search(v['n']) or re.search(r'Comprehensive Development', v['n']): continue
        f = dict(v['f'])
        out.append(dict(id=k, code=k[len(f'zd-{m}-'):].upper(), name=v['n'], muni=m, uses=f.get('Main uses', ''), lot=f.get('Min. new lot', '') or f.get('Min. lot', '')))
    return out
def is_ind(z): return bool(re.search(r'Industrial|Business Park|Employment|Airport|Warehouse|Storage', z['name']))
def is_office(z): return bool(re.search(r'\boffices?\b', z['uses'], re.I)) or bool(re.search(r'Office|Employment|Business District|City Centre|Downtown|Town Centre|Regional Commercial', z['name']))
def is_retail(z): return bool(re.search(r'Commercial', z['name'])) and not re.search(r'Industrial', z['name']) or bool(re.search(r'\bretail\b', z['uses'], re.I))
def first(s, n=230):
    s = re.sub(r'\s+', ' ', s).strip(); m = re.match(r'(.+?[.])(\s|$)', s); s = m.group(1) if m else s
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + '…'
def munis_of(mk):
    labs = [MUNI_LABEL.get(m, m) for m in mk]
    return labs[0] if len(labs) == 1 else ' and '.join([', '.join(labs[:-1]), labs[-1]])
def zlist(zs): return {'t': 'list', 'items': [[{'t': f'{z["code"]} {z["name"]}' + (f' ({MUNI_LABEL.get(z["muni"], z["muni"])})' if z['muni'] in ('whiterock', 'langleycity') else ''), 'h': f'/zonings.html#{z["id"]}'}] for z in zs], 'gen': G}
def zone_rows(zs, with_lot=False):
    rows = []
    for z in zs:
        r = [f'[{z["code"]} {z["name"]}](/zonings.html#{z["id"]})', MUNI_LABEL.get(z['muni'], z['muni'])]
        r.append(first(z['lot'], 80) if with_lot else first(z['uses']))
        rows.append(r)
    return rows

def sales_line(row, where, label=None):
    m = MUNI[row]; nm = label or row
    s = (f'In the second quarter of 2026, {m[1]} commercial properties sold in {nm} (against {m[2]} a year earlier), worth {m[3]} in all: '
         f'{m[4]} industrial, {m[5]} land, {m[6]} office, {m[7]} retail and other, and {m[8]} multi-family.')
    return s
def ind_line(sub, nm):
    r = IND[sub]
    return (f'Industrial space in the {sub} submarket ({r[1]} sq ft) was {r[2]} vacant in the third quarter of 2026, asking {r[4]} per sq ft net plus {r[5]} in additional rent, '
            f'with {r[7]} sq ft under construction. Across Metro Vancouver vacancy was {IND["Metro Vancouver total"][2]}.')

def page(slug, title, desc, h1, crumbs, blocks, faq, faqh):
    return dict(status='draft', slug=slug, updated=DAY, new_page=dict(title=chk_title(title), description=chk_desc(desc), h1=h1), breadcrumbs=crumbs,
                faq_heading=faqh, blocks=[{'t': 'notice', 'text': 'Draft for Jared’s approval. Commercial figures are from GVR Commercial Edge (Q2 2026) and Avison Young (Q3 2026); zones are the municipal bylaw summaries on the zoning guide. For sale listings only.', 'gen': G}] + blocks,
                faq=[dict(q=q, a=a, gen=G) for q, a in faq])

def city_slug(k): return f'{k}-commercial-real-estate-for-sale'
def cat_slug(a, c): return f'{a}-{CATS[c]["slug"]}'

sys.path.insert(0, os.path.join(ROOT, 'tools'))
import commercial_facts_2026_11_20 as FACTS
def FL(items): return {'t': 'list', 'items': [[{'t': f'{t} ([{lab}]({url}), read November 20, 2026)'}] for t, lab, url in items], 'gen': G}

made, sheet = [], []
# ------------------------------------------------------------------ city pages
for key, (nm, mls, row, sub, mk) in CITIES.items():
    slug = city_slug(key); fv = key in FV
    region = 'the Fraser Valley' if fv else 'Metro Vancouver'
    b = [P(f'Commercial property for sale in {nm}: industrial buildings and strata units, offices, retail space, commercial land and businesses listed on the MLS®. '
           f'This search shows properties for sale only; spaces for lease are not included. Call or text Jared Gibbons at 604-928-1361 for a property that is not listed, or to value one you own.'),
         {'t': 'grid', 'gen': G}]
    area = next((a for a, v in AREAS.items() if v[1] == key), None)
    if area:
        b += [H(f'{AREAS[area][0]} commercial property by type'),
              L([f'[{AREAS[area][0]} {CATS[c]["label"].lower() if c != "business" else "businesses"} for sale](/{cat_slug(area, c)}.html)' for c in CATS])]
    if key in FACTS.CITY:
        b += [H(f'Commercial and industrial areas in {nm}'), FL(FACTS.CITY[key])]
    if row:
        lab = 'the City of Surrey as a whole' if key in ('south-surrey-white-rock', 'cloverdale') else row
        b += [H(f'What sold in {nm}'), P(sales_line(row, nm, lab) + (' Commercial Edge reports Surrey as one city, so these figures include South Surrey, Cloverdale, Newton, Guildford and Whalley.' if lab.startswith('the City') else '')
              + (f' White Rock, reported separately, had {MUNI["White Rock"][1]} sales worth {MUNI["White Rock"][3]}.' if key == 'south-surrey-white-rock' else '')),
              P(f'Source: {SRC_GVR}.')]
    if sub:
        b += [H(f'Industrial space in {nm}'), P(ind_line(sub, nm)), P(f'Source: {SRC_AY}.')]
    if not row:
        a = ASSET['All commercial']
        b += [H('What sold across the Lower Mainland'),
              P(f'Commercial Edge does not break out {nm} in the figures published on this site. Across the Lower Mainland, {a[1]} commercial properties sold in the second quarter of 2026, worth {a[4]}: '
                f'{ASSET["Industrial"][1]} industrial, {ASSET["Land"][1]} land, {ASSET["Office"][1]} office, {ASSET["Retail & other"][1]} retail and other, and {ASSET["Multi-family"][1]} multi-family.'),
              P(f'Source: {SRC_GVR}.')]
    zs = zones(mk)
    if zs:
        ind = [z for z in zs if is_ind(z)]; com = [z for z in zs if not is_ind(z)]
        b += [H(f'{munis_of(mk)} commercial and industrial zones'),
              P(f'Zoning decides what a commercial property can be used for. These are the {munis_of(mk)} zones on the zoning guide' + (f' (they apply across the whole municipality, not only {nm})' if key in ('south-surrey-white-rock', 'cloverdale') else '') + '; each links to its permitted uses, smallest new lot and height limits. Check the zone of a specific address before you buy.')]
        if com: b += [H('Commercial zones', 3), zlist(com)]
        if ind: b += [H('Industrial and business park zones', 3), zlist(ind)]
    others = [k for k in (FV if fv else MV) if k != key]
    b += [H(f'Commercial real estate in other {"Fraser Valley" if fv else "Metro Vancouver"} cities'), L([f'[{CITIES[k][0]}](/{city_slug(k)}.html)' for k in others]),
          P('See also [all commercial listings](/commercial.html) and the [Fraser Valley commercial market report](/fraser-valley-commercial-market-report.html).')]
    faq = []
    if row: faq.append((f'How many commercial properties sold in {nm} recently?', sales_line(row, nm, 'the City of Surrey' if key in ('south-surrey-white-rock', 'cloverdale') else row)))
    if sub: faq.append((f'What is industrial vacancy in {nm}?', ind_line(sub, nm)))
    t = f'{nm} Commercial Real Estate for Sale'
    title = t if len(t) <= 60 else f'{nm} Commercial Property for Sale'
    if len(title) < 30: title = f'{title} | MLS®'
    desc = f'Commercial real estate for sale in {nm}: industrial, office, retail, land and businesses on the MLS®, with recent sales and zoning.' if row or zs else f'Commercial real estate for sale in {nm}, BC: industrial, office, retail, commercial land and businesses for sale on the MLS®.'
    made.append(page(slug, title, desc, f'{nm} Commercial Real Estate for Sale',
                     [{'name': 'Home', 'href': '/'}, {'name': 'Commercial', 'href': '/commercial.html'}, {'name': f'{nm} commercial', 'href': f'/{slug}.html'}],
                     b, faq, f'{nm} commercial real estate: your questions answered'))
    sheet.append([slug, f'{nm} Commercial Real Estate for Sale', f'https://jaredgibbons.ca/{slug}.html', f'COMM {nm}', mls, '(none)', 'All commercial types', 'For sale only (no leases)', '(none)', 'Active', '', '', ''])

# ------------------------------------------------------------------ category pages
BUSINESS_TIPS = ['Business only or with the property: many MLS® business listings sell the business and its lease, not the building. The listing says which.',
                 'The lease: its remaining term, renewal options and whether the landlord must approve an assignment to you.',
                 'The numbers: at least two or three years of financial statements and tax returns, and what is included (equipment, stock, name, website, phone number).',
                 'Licences and permits: the municipal business licence and any provincial licence the business needs, and whether they transfer.',
                 'Staff and suppliers: who stays, and which contracts carry over.']
for akey, (anm, ckey, amls) in AREAS.items():
    nm, mlsfull, row, sub, mk = CITIES[ckey]
    zs = zones(mk)
    for c, cd in CATS.items():
        slug = cat_slug(akey, c); lab = cd['label']
        noun = 'businesses' if c == 'business' else lab.lower()
        b = [P({'industrial': f'Industrial property for sale in {anm}: warehouses, industrial buildings, shop condos and industrial strata units listed on the MLS®.',
                'office': f'Office space for sale in {anm}: office buildings and office strata units listed on the MLS®.',
                'retail': f'Retail space for sale in {anm}: storefronts, retail strata units and retail buildings listed on the MLS®.',
                'land': f'Commercial and industrial land for sale in {anm}: lots and development sites listed on the MLS® as commercial land.',
                'business': f'Businesses for sale in {anm}, with or without the real estate, listed on the MLS®.'}[c]
               + ' For sale only; space for lease is not included. Call or text Jared Gibbons at 604-928-1361 to ask about one of these, or about something not listed.'),
             {'t': 'grid', 'gen': G}]
        if c in FACTS.AREA.get(akey, {}):
            fh, fi = FACTS.AREA[akey][c]
            b += [H(fh), FL(fi)]
        if row and cd['asset']:
            m = MUNI[row]; idx = {'Industrial': 4, 'Land': 5, 'Office': 6, 'Retail & other': 7}[cd['asset']]
            whole = row == 'Surrey'
            b += [H(f'What sold: {cd["short"]} in {"Surrey" if whole else anm}'),
                  P(f'In the second quarter of 2026, {m[idx]} of the {m[1]} commercial sales in {"the City of Surrey" if whole else row} were {cd["asset"].lower()} properties, '
                    f'against {ASSET[cd["asset"]][1]} across the Lower Mainland.' + (' Commercial Edge reports Surrey as one city, so the figure covers all of Surrey, not only ' + anm + '.' if whole else '')),
                  P(f'Source: {SRC_GVR}.')]
        if c == 'industrial' and sub:
            b += [H(f'Industrial vacancy and rents, {sub}'), P(ind_line(sub, anm)), P(f'Source: {SRC_AY}.')]
        pick = {'industrial': is_ind, 'office': is_office, 'retail': lambda z: is_retail(z) and not is_ind(z), 'land': lambda z: bool(z['lot'])}.get(c)
        if pick:
            sel = [z for z in zs if pick(z)]
            if c == 'land' and akey == 'cloverdale':   # the same Surrey table is on the South Surrey land page; link to it instead of repeating it
                b += [H('Smallest new lot by zone'), P('Cloverdale uses the City of Surrey zoning bylaw. The smallest new lot in each Surrey commercial and industrial zone is listed on the [South Surrey commercial land page](/south-surrey-commercial-land-for-sale.html), and every zone is on the [zoning guide](/zonings.html).')]
                sel = []
            if sel:
                b += [H(f'{munis_of(mk)} zones that allow {cd["short"]} uses' if c != 'land' else f'Smallest new lot by zone, {munis_of(mk)}'),
                      P('Each zone links to its full summary on the zoning guide.' + (f' These are municipal zones, so some apply to parts of {"Surrey" if "surrey" in mk else "the municipality"} outside {anm}.' if akey in ('south-surrey', 'cloverdale') else '') + ' A zone that allows a use may still need a permit or a rezoning for a specific site, so check the address with the municipality before you buy.'),
                      (TB(f'{munis_of(mk)}: commercial and industrial zones and their smallest new lot', ['Zone', 'Municipality', 'Smallest new lot'], zone_rows(sel, with_lot=True), 'Municipal zoning bylaws, as summarised on the zoning guide.') if c == 'land' else zlist(sel))]
        if c == 'business':
            b += [H(f'What to ask for before you buy a business'), L(BUSINESS_TIPS)]
        b += [H(f'More {anm} commercial property'),
              L([f'[{anm} {CATS[o]["label"].lower() if o != "business" else "businesses"} for sale](/{cat_slug(akey, o)}.html)' for o in CATS if o != c] + [f'[All {nm} commercial real estate](/{city_slug(ckey)}.html)'])]
        faq = []
        if row and cd['asset']:
            m = MUNI[row]; idx = {'Industrial': 4, 'Land': 5, 'Office': 6, 'Retail & other': 7}[cd['asset']]
            faq.append((f'How many {cd["short"]} properties sold in {"Surrey" if row == "Surrey" else anm} recently?', f'{m[idx]} in the second quarter of 2026, out of {m[1]} commercial sales in {"the City of Surrey" if row == "Surrey" else row} (GVR Commercial Edge).'))
        h1 = f'{anm} {lab} for Sale' if c != 'business' else f'Businesses for Sale in {anm}'
        title = h1 if len(h1) >= 30 else f'{h1} | MLS® Listings'
        desc = {'industrial': f'Industrial property for sale in {anm}: warehouses, shop condos and industrial strata on the MLS®, with vacancy, rents and industrial zones.',
                'office': f'Office space for sale in {anm}: office buildings and strata units on the MLS®, with recent office sales and the zones that allow offices.',
                'retail': f'Retail space for sale in {anm}: storefronts and retail strata units on the MLS®, with recent sales and the zones that allow retail.',
                'land': f'Commercial and industrial land for sale in {anm} on the MLS®, with recent land sales and the smallest new lot in each zone.',
                'business': f'Businesses for sale in {anm} on the MLS®, with or without the real estate, plus what to ask for before you buy a business.'}[c]
        made.append(page(slug, title, desc, h1,
                         [{'name': 'Home', 'href': '/'}, {'name': 'Commercial', 'href': '/commercial.html'}, {'name': f'{nm} commercial', 'href': f'/{city_slug(ckey)}.html'}, {'name': h1, 'href': f'/{slug}.html'}],
                         b, faq, f'{h1}: your questions answered'))
        sheet.append([slug, h1, f'https://jaredgibbons.ca/{slug}.html', f'COMM {anm} {lab}', amls, '(none)', cd['mls'], 'For sale only (no leases)', '(none)', 'Active', '', '', ''])

taken = {f[:-5] for f in os.listdir('src/data/pages')}
for j in made:
    assert j['slug'] not in taken, j['slug']
    p = f'src/data/local/{j["slug"]}.json'
    if os.path.exists(p) and json.load(open(p)).get('hand_edited'): print('kept hand-edited', p); continue
    json.dump(j, open(p, 'w'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
print(len(made), 'pages')

# ------------------------------------------------------------------ worksheet for Gerry
wb = Workbook(); ws = wb.active; ws.title = 'Commercial searches'
ws.append(['Page slug', 'Page heading', 'Page URL', 'Search name to save in MyRealPage', 'MLS area', 'Sub-area filter', 'Commercial type', 'Other filters', 'Price filter', 'Status', 'Search ID (Gerry fills)', 'Embed code (Gerry fills)', 'Notes'])
ws.append(['commercial', 'Fraser Valley Commercial Real Estate for Sale (existing page, search 1450191)', 'https://jaredgibbons.ca/commercial.html', 'COMM Metro Vancouver + Fraser Valley (edit 1450191)',
           'Metro Vancouver and Fraser Valley areas only: Vancouver West, Vancouver East, Burnaby North/South/East, New Westminster, Richmond, Ladner, Tsawwassen, Coquitlam, Port Coquitlam, Port Moody, North Vancouver, West Vancouver, Maple Ridge, Pitt Meadows, Surrey, North Surrey, South Surrey White Rock, Cloverdale, North Delta, Langley, Abbotsford, Mission, Chilliwack, Sardis, Yarrow, Agassiz, Harrison, Hope. Leave out Sunshine Coast, Squamish, Whistler, Pemberton, the Islands and anything outside these.',
           '(none)', 'All commercial types', 'For sale only (no leases)', '(none)', 'Active', '1450191', '(no change if you edit the existing search)', 'Edit the existing search rather than making a new one, so the page keeps working.'])
for r in sheet: ws.append(r)
for c in ws[1]: c.font = Font(bold=True)
for col, w in zip('ABCDEFGHIJKLM', [42, 44, 60, 40, 50, 16, 30, 24, 12, 10, 18, 30, 40]): ws.column_dimensions[col].width = w
ws.freeze_panes = 'A2'
n = wb.create_sheet('Notes')
for line in ['One saved MyRealPage search per page, noframe template, same set-up as the earlier searches (Status Active, no price filter).',
             'All of these are FOR SALE only: please exclude lease listings in every search.',
             'Commercial type: use the MLS® commercial property type (Industrial, Office, Retail, Land, Business). If Business has "with property" and "without property", include both.',
             'City searches use all commercial types. Surrey = the four Surrey board areas without the White Rock sub-area; South Surrey and White Rock together = South Surrey White Rock.',
             'Row 2 is an edit to the existing commercial search (1450191), which today returns listings from across BC.',
             'Pages are held from Google until their search ID is filled in; send the sheet back with column K filled and the pages go live.']:
    n.append([line])
n.column_dimensions['A'].width = 140
wb.save('docs/review/idx/commercial-searches-2026-11-20.xlsx')
print('sheet rows', len(sheet) + 1)
