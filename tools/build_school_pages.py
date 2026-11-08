#!/usr/bin/env python3
"""Homes-for-sale-near-a-school pages (wave 1) -> src/data/local/homes-near-<school>.json (draft, new_page header).

Inputs
  docs/review/idx/school-radius-searches-2026-11-07-DONE.xlsx   Jerry's saved searches (one per school; MyRealPage has no radius option, so each search matches the school name in the listing remarks)
  src/data/schools/facts.json          official school facts (tools/build_school_facts.py)
  src/data/schools/radius-sold.json    grouped sold figures within the radius (tools/build_school_sold.py, Pete's exports); a page without it has no sold section yet
  src/data/area-coordinates.csv        neighbourhood guide points, used to find the guide a school sits in
Rules
  - 18 searches with 0 listings are HELD (no page) until they have results.  The 6 learning centres were skipped by Jerry.
  - The listing search is described honestly: homes whose description names the school.  The distance figures (sold prices) are the only radius-based part.
  - No school ratings, rankings or catchment claims.  Catchment is the district's, linked.
  - Inbound links: the city schools hub, the neighbourhood guide, and the three nearest school pages (each page links to its three nearest, so inbound links come from neighbours too).
python3 -I tools/build_school_pages.py
"""
import csv, json, math, os, re, sys, collections
import openpyxl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
from build_new_searches import P, H, L, tbl, money, num, lk

G = 'school'
XLSX = 'docs/review/idx/school-radius-searches-2026-11-07-DONE.xlsx'
FACTS = json.load(open('src/data/schools/facts.json'))
SOLD = json.load(open('src/data/schools/radius-sold.json')) if os.path.exists('src/data/schools/radius-sold.json') else {}
AREAS = list(csv.DictReader(open('src/data/area-coordinates.csv')))
WIN = 'November 1, 2025 to October 31, 2026'

HUB = {'surrey': ('schools-in-surrey-bc', 'Schools in Surrey'), 'south-surrey': ('schools-in-south-surrey-white-rock-bc', 'Schools in South Surrey and White Rock'),
       'delta': ('schools-in-delta-bc', 'Schools in Delta'), 'langley': ('schools-in-langley-bc', 'Schools in Langley'), 'abbotsford': ('schools-in-abbotsford-bc', 'Schools in Abbotsford')}
SEARCHES = {  # candidate city search pages, kept if they exist
    'surrey': [('Surrey houses for sale', 'surrey-houses-for-sale'), ('Surrey condos for sale', 'surrey-condos-for-sale'), ('Surrey townhomes for sale', 'surrey-townhomes-for-sale')],
    'south-surrey': [('South Surrey houses for sale', 'south-surrey-houses-for-sale'), ('South Surrey condos for sale', 'south-surrey-condos-for-sale'), ('South Surrey townhomes for sale', 'south-surrey-townhomes-for-sale')],
    'delta': [('Delta homes for sale', 'delta-homes-for-sale'), ('Ladner houses for sale', 'ladner-houses-for-sale'), ('Tsawwassen houses for sale', 'tsawwassen-houses-for-sale')],
    'langley': [('Langley houses for sale', 'langley-houses-for-sale'), ('Langley condos for sale', 'langley-condos-for-sale'), ('Langley townhomes for sale', 'langley-townhomes-for-sale')],
    'abbotsford': [('Abbotsford houses for sale', 'abbotsford-houses-for-sale'), ('Abbotsford condos for sale', 'abbotsford-condos-for-sale'), ('Abbotsford townhomes for sale', 'abbotsford-townhomes-for-sale')],
}
LEVEL = {'elementary': 'elementary school', 'middle': 'middle school', 'secondary': 'secondary school'}


def nz(s): return re.sub(r'[^a-z0-9]', '', s.lower().replace('saint', 'st'))
def km_str(r): return f'{r:g} km'
def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    y = math.sin(lo2 - lo1) * math.cos(la2); x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'][round(((math.degrees(math.atan2(y, x)) + 360) % 360) / 45) % 8]


def fit(*c):
    for x in c:
        if 135 <= len(x) <= 158 and x.endswith('.'): return x
    raise AssertionError(('no description fits', [(len(x), x) for x in c]))


def load_rows():
    ws = openpyxl.load_workbook(XLSX, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True)); head = [str(h or '') for h in rows[0]]
    ix = lambda k: next(i for i, h in enumerate(head) if h.startswith(k))
    c = dict(slug=ix('Page slug'), h1=ix('Page heading'), school=ix('School'), city=ix('City'), addr=ix('School address'), rad=ix('Radius'), pri=ix('Priority'), sid=ix('Search ID'), cnt=ix('Count'), note=ix('Notes'))
    out = []
    for r in rows[1:]:
        if not r[c['slug']]: continue
        cnt = re.match(r'\d+', str(r[c['cnt']] or ''))
        out.append(dict(slug=r[c['slug']], h1=r[c['h1']], school=r[c['school']], city=r[c['city']], addr=r[c['addr']], rad=float(r[c['rad']]), pri=str(r[c['pri']]),
                        sid=str(r[c['sid']] or '').strip(), count=int(cnt.group()) if cnt else None, note=r[c['note']] or ''))
    return out


def fact_for(r):
    idx = [f for f in FACTS if nz(f['name']) == nz(r['school'])]
    if len(idx) > 1:
        a = [f for f in idx if nz(r['addr'] or '')[:8] and nz(r['addr'] or '').startswith(nz(f['address'])[:6])] or [f for f in idx if nz(f['city']) == nz(r['city'])]
        idx = a or idx
    return idx[0] if idx else None


def main():
    rows = load_rows(); built, held, skipped = [], [], []
    for r in rows:
        if r['sid'].isdigit() and ((r['count'] or 0) > 0 or r['slug'][len('homes-near-'):] in SOLD): built.append(r)   # a search with no results yet still gets a page when Pete's sold figures exist
        elif r['sid'].isdigit(): held.append(r)
        else: skipped.append(r)
    names = collections.Counter(r['school'] for r in built)
    for r in built:
        f = fact_for(r); assert f, r['school']
        r['f'] = f; r['dup'] = names[r['school']] > 1; r['approx'] = not f['lat']
        if f['lat']: r['ll'] = (f['lat'], f['lon'])
        else:  # no official coordinates: use the centre of the other schools in the same postal district (V4N etc.), for linking only, never for a stated distance
            same = [x for x in FACTS if x['lat'] and x['postal'][:3] == f['postal'][:3]]
            assert same, ('no coordinates and no neighbours in postal district', r['school'], f['postal'])
            r['ll'] = (sum(x['lat'] for x in same) / len(same), sum(x['lon'] for x in same) / len(same))
        # neighbourhood guide the school sits in (nearest guide point, within 3 km)
        best = min(AREAS, key=lambda a: hav(r['ll'], (float(a['lat']), float(a['lon']))))
        d = hav(r['ll'], (float(best['lat']), float(best['lon'])))
        r['area'] = best if d <= 3.0 and N.exists(best['page']) else None
        dist = f['district']
        r['hubkey'] = 'delta' if dist == 37 else 'langley' if dist == 35 else 'abbotsford' if dist == 34 else ('south-surrey' if best['city'] == 'South Surrey' else 'surrey')
    slugs = {r['slug'] for r in built}
    N.NEW.update(slugs)
    for r in built: N.TITLE[r['slug']] = r['h1']
    # nearest three other pages
    for r in built:
        near = sorted(((hav(r['ll'], o['ll']), o) for o in built if o is not r), key=lambda x: x[0])
        r['near'] = [(None if (r['approx'] or o['approx']) else d, o) for d, o in near[:3] if d <= 6.0]
    # every page needs at least 3 inbound links: hub + guide + neighbours.  A page short of that is added to the "other schools near" list of its next-nearest schools (a list holds at most 5).
    def inb(x): return 1 + (1 if x['area'] else 0) + sum(1 for o in built if any(y is x for _, y in o['near']))
    for r in sorted(built, key=inb):
        if inb(r) >= 3: continue
        for d, o in sorted(((hav(r['ll'], o['ll']), o) for o in built if o is not r), key=lambda x: x[0]):
            if inb(r) >= 3: break
            if len(o['near']) < 5 and not any(y is r for _, y in o['near']) and d <= 8.0:
                o['near'].append((None if (r['approx'] or o['approx']) else d, r))
        assert inb(r) >= 3, ('too few inbound links', r['school'])
    made = [page(r) for r in built]
    N.write_seo(made)
    inbound(built)
    sold = sum(1 for r in built if r['slug'][11:] in SOLD)
    print(f'{len(made)} pages built; {len(held)} held (0 listings); {len(skipped)} skipped; {sold} with sold figures; {len(made) - sold} waiting for Pete')
    json.dump(dict(built=[r['slug'] for r in built], held=[dict(slug=r['slug'], school=r['school'], city=r['city'], note=r['note']) for r in held], skipped=[r['school'] for r in skipped]),
              open('src/data/schools/wave1-pages.json', 'w'), indent=1, ensure_ascii=False)


def page(r):
    f, nm, slug, city = r['f'], r['school'], r['slug'], r['city']
    key = slug[len('homes-near-'):]
    sd = SOLD.get(key); rad = r['rad']; rk = km_str(rad)
    order = sum(map(ord, slug)) % 3
    indep = f['independent']; lvl = LEVEL.get(f['level'], 'school')
    place = f['city'] if f['city'] and f['city'].lower() != 'delta' else city
    # titles and description
    nmc = f'{nm} in {place}' if r['dup'] else nm
    title = next(t for t in (f'Homes for Sale Near {nmc} | Prices', f'Homes for Sale Near {nmc}', f'Homes for Sale Near {nmc}, {place}') if 38 <= len(t) <= 60)
    h1 = f'Homes for Sale Near {nm}' + (f', {place}' if r['dup'] else '')
    assert 20 <= len(h1) <= 60, h1
    if r['dup']: nm = nmc   # two schools share a name (Holly, Walnut Road...): the body names the place too, so the pages do not read as copies
    n = sd['n'] if sd else None
    if sd and n >= 10:
        desc = fit(*[f'{a} {b}' for a in (f'Search homes for sale near {nm} in {place}.', f'Homes for sale near {nm} in {place}.', f'See homes for sale near {nm}.')
                     for b in (f'{n} sold within {rk} in twelve months. See prices for houses, townhomes and condos, nearby schools and catchment checks.',
                               f'{n} homes sold within {rk} in twelve months. See prices by home type, nearby schools and catchment checks.',
                               f'{n} sold within {rk} in a year, with prices by home type, nearby schools and what to check on the catchment.',
                               f'{n} sold within {rk} in twelve months, with prices by home type, nearby schools and catchment checks.')])
    else:
        desc = fit(*[f'{a} {b}' for a in (f'Search homes for sale near {nm} in {place}.', f'Homes for sale near {nm} in {place}.', f'See homes for sale near {nm}.')
                     for b in ('See listings that name the school, nearby schools and what to check on the catchment before you offer.',
                               'Find listings that name the school, plus nearby schools and what to check on the catchment.',
                               'See listings that name the school, nearby schools and catchment checks.')])
    hub, hubname = HUB[r['hubkey']]
    seo = dict(title=title, h1=h1, crumb=f'Near {nm}', description=desc, links_h=f'More searches near {nm}')
    # intro
    who = (f'{nm} is an independent school in {place}' if indep else f'{nm} is an {lvl} in {place}' if lvl.startswith(('e',)) else f'{nm} is a {lvl} in {place}')
    if not indep: who += f' ({f["district_name"]} School District)'
    bits = [who + f', at {f["address"]}.' if not f['address'].upper().startswith('PO BOX') else who + '.']
    if f['grades']: bits.append(f'It teaches grades {f["grades"].replace("-", " to ")}.' if f['grades'] not in ('K-12',) else 'It teaches kindergarten to grade 12.')
    if f['programs']: bits.append(f'Programs listed: {f["programs"]}.')
    intro = ' '.join(bits)
    has = bool(sd and sd.get('all', {}).get('n', 0) >= 10)
    bl = [{'t': 'notice', 'text': ('Draft for Jared’s approval. Sold figures come from Paragon closed and pending sales, ' + WIN + f', within {rk} of the school address. A pending sale is firm but has not completed, so its price can still change. The live search is not connected yet.') if has else 'Draft for Jared’s approval. The live search is not connected yet, and sold prices for this school will be added when the sold export arrives.', 'gen': G},
          P(intro),
          P((f'The search below lists homes for sale whose listing names {nm}.' + (f' Under it are the prices homes sold for within {rk} of the school.' if has else ''),
             f'Below are the homes currently for sale whose listing mentions {nm}' + (f', followed by what homes within {rk} of the school sold for.' if has else '.'),
             f'Use the search below to see homes for sale that name {nm} in the listing' + (f', then check the sold prices within {rk} of the school.' if has else '.'))[order]),
          {'t': 'grid', 'gen': G},
          H(f'How the {nm} search works'),
          P(f'MLS® listings are not tagged by school. This search finds houses, townhomes and condos whose description names {nm}, so a home close to the school whose listing leaves the name out will not appear, '
            + (f'and a listing that names the school can sit farther than {rk} away. Use the sold prices below for the distance-based picture, and ask Jared to watch for homes near the school that the search misses.' if has else
               'and a listing that names the school can sit some distance away. Ask Jared to watch for homes near the school that the search misses.'))]
    gdef = [('house', 'Houses'), ('townhouse', 'Townhomes'), ('condo', 'Condos')]
    mid = None
    if sd and n >= 10:
        gs = sd['groups']; al = sd['all']
        parts = [f'{gs[k]["n"]} {lab.lower()}' for k, lab in gdef if gs[k]['n']]
        big = max(gdef, key=lambda x: gs[x[0]]['n'])
        mid = gs[big[0]].get('price') or al.get('price'); midlab = big[1].lower()
        bl += [H(f'What homes within {rk} of {nm} sold for'),
               P(f'Between {WIN.replace(" to ", " and ")}, {n} homes sold within {rk} of {nm}: ' + (', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1] if parts else f'{n} homes') + '.'
                 + (f' The largest group was {big[1].lower()}, at a median of {money(gs[big[0]]["price"])}.' if gs[big[0]].get('price') else ''))]
        def cv(g, k, fmt=lambda x: f'{x:,}'): return fmt(g[k]) if g.get(k) is not None else '—'
        cols = [('Houses', gs['house']), ('Townhomes', gs['townhouse']), ('Condos', gs['condo']), ('All homes', al if al.get('price') else {'n': n})]
        trs = [['Sales'] + [num(g['n']) for _, g in cols], ['Median price'] + [cv(g, 'price', money) for _, g in cols]]
        if any(g.get('p25') for _, g in cols): trs.append(['Middle half of prices'] + [f'{money(g["p25"])} to {money(g["p75"])}' if g.get('p25') else '—' for _, g in cols])
        trs += [['Median days to sell'] + [cv(g, 'dom') for _, g in cols], ['Sold price as a share of list price'] + [f'{g["ratio"]}%' if g.get('ratio') else '—' for _, g in cols],
                ['Sales over the list price'] + [f'{g["over"]}%' if g.get('over') is not None else '—' for _, g in cols]]
        bl.append(tbl(f'Homes sold within {rk} of {nm}, by type', ['Measure'] + [c for c, _ in cols], trs,
                      f'Source: Paragon closed and pending sales, {WIN}, within {rk} of the school address (straight-line distance). A pending sale is firm but not completed. A figure is shown only where at least 5 homes sold. Duplexes and row houses count in All homes only.'))
        mh = [f'{lab.lower()} between {money(g["p25"])} and {money(g["p75"])}' for lab, g in cols[:3] if g.get('p25')]
        if mh:
            bl.append(P(f'The middle half of sales within {rk} of {nm} went for ' + ('; '.join(mh)) + f'. Half of the {n} homes sold at or below {money(al["price"])}' + (f', {al["ratio"]}% of the list price at the median' if al.get('ratio') else '') + '.' if al.get('price') else f'The middle half of sales within {rk} of {nm} went for ' + ('; '.join(mh)) + '.'))
        if sd.get('q') and n >= 12:
            bl.append(tbl(f'Homes sold within {rk} of {nm}, by quarter', ['Quarter', 'Sales', 'Median price'], [[a, num(b), money(c) if c else '—'] for a, b, c in sd['q']],
                          f'Source: Paragon closed and pending sales, {WIN}, within {rk} of the school address. A median is shown only where at least 5 homes sold.'))
        subs = [s for s in sd['sub'] if s[1] >= 3]
        if subs:
            bl.append(P(f'Where the {n} sales within {rk} of {nm} were: ' + ', '.join(f'{N.disp(s[0])} ({s[1]} sales' + (f', median {money(s[2])}' if s[2] else '') + ')' for s in subs[:4]) + '.'))
        for k, lab in (('condo', 'condo'), ('townhouse', 'townhome')):
            cx = [c for c in sd['complexes'].get(k, []) if c[2]]
            if len(cx) >= 2:
                bl.append(tbl(f'{lab.capitalize()} buildings and complexes near {nm} with the most sales', ['Building or complex', 'Sales', 'Median price'], [[c[0], num(c[1]), money(c[2])] for c in cx],
                              f'Source: Paragon closed and pending sales, {WIN}. A building is listed with 5 or more sales.'))
    # school facts
    srows = [['Type', 'Independent school' if indep else f'Public school, {f["district_name"]} School District'], ['Level', lvl.capitalize() if f['level'] else '—'], ['Grades', f['grades'] or '—'],
             ['Programs listed', f['programs'] or '—'], ['Address', f'{f["address"]}, {f["city"]} {(f["postal"][:3] + " " + f["postal"][3:]) if len(f["postal"] or "") == 6 else (f["postal"] or "")}'.strip()]]
    if f['url']: srows.append(['School website', {'t': re.sub(r'^https?://(www\.)?', '', f['url']).rstrip('/'), 'h': f['url']}])
    srows = [x for x in srows if x[1] != '—']
    bl += [H(f'About {nm}'), tbl(f'{nm} facts', ['Item', 'Detail'], srows, 'Source: BC Data Catalogue, BC Schools - School Locations (Open Government Licence - BC), and the school and district websites, retrieved November 2026.')]
    if indep:
        bl.append(P(f'{nm} is an independent school and sets its own admission, so living near it does not decide whether a child gets a place. Ask the school about applications and wait lists.'))
    else:
        cp = [{'t': f'{f["district_name"]} School District sets each school’s catchment, and a home near {nm} may sit in another school’s catchment. Confirm the exact address with the district before you offer'}]
        if f['catchment_url']:
            cp += [{'t': ' using its', }, {'t': 'school catchment finder', 'h': f['catchment_url']}, {'t': '.'}]
        else: cp[0]['t'] += '.'
        bl.append({'t': 'p', 'parts': cp, 'gen': G})
    if r['near']:
        bl += [H(f'Other schools near {nm}'),
               {'t': 'list', 'items': [[lk(f'Homes for sale near {o["school"]} ({LEVEL.get(o["f"]["level"], "school")}' + (f', about {d:.1f} km {bearing(r["ll"], o["ll"])})' if d is not None else ')'), o['slug'])] for d, o in r['near']], 'gen': G}]
    # every school within a few km (official coordinates, straight line): a table that is different on every page
    if not r['approx']:
        me = (f['lat'], f['lon']); R = 3
        cand = sorted(((hav(me, (x['lat'], x['lon'])), x) for x in FACTS if x['lat'] and x is not f and not (x['name'] == f['name'] and x['address'] == f['address'])), key=lambda t: t[0])
        cand = [(d, x) for d, x in cand if d >= 0.02]   # programs run from the same building (online, alternate, continuing ed) are not 'nearby schools'
        within = [(d, x) for d, x in cand if d <= R]
        if len(within) < 4: R = 5; within = [(d, x) for d, x in cand if d <= R]
        if len(within) >= 4:
            kinds = collections.Counter(x['level'] or 'other' for _, x in within); ind = sum(1 for _, x in within if x['independent'])
            parts = ', '.join(f'{c} {k}' for k, c in sorted(kinds.items(), key=lambda t: -t[1]))
            near1 = within[0]
            txt = (f'{len(within)} schools in the provincial school list sit within {R} km of {nm} in a straight line ({parts}; {ind} independent). The closest is {near1[1]["name"]}, {near1[0]:.1f} km away'
                   + (f', and the farthest on this list is {within[min(len(within), 25) - 1][1]["name"]}, {within[min(len(within), 25) - 1][0]:.1f} km away.' if len(within) > 1 else '.'))
            def nearest(pred, label):
                m = next(((d, x) for d, x in within if pred(x)), None)
                return f'the nearest {label} is {m[1]["name"]} ({m[0]:.1f} km)' if m else None
            bits = [b for b in (nearest(lambda x: x['level'] == 'elementary', 'elementary school'), nearest(lambda x: x['level'] == 'secondary', 'secondary school'), nearest(lambda x: x['independent'], 'independent school'),
                                nearest(lambda x: 'french' in (x['programs'] or '').lower(), 'school listing a French Immersion program')) if b]
            bits = [b for b in bits if near1[1]['name'] not in b][:3] if len(bits) > 2 else bits
            if bits: txt += ' By type, ' + '; '.join(bits) + '.'
            peers = [(d, x) for d, x in within if f['level'] and x['level'] == f['level']][:5]
            if len(peers) >= 2: txt += f' Other {f["level"]} schools close by: ' + ', '.join(f'{x["name"]} ({d:.1f} km {bearing(me, (x["lat"], x["lon"]))})' for d, x in peers) + '.'
            same = next(((d, x) for d, x in within if f['grades'] and x['grades'] == f['grades']), None)
            if same: txt += f' The nearest school teaching the same grades ({f["grades"]}) is {same[1]["name"]}, {same[0]:.1f} km {bearing(me, (same[1]["lat"], same[1]["lon"]))} of {nm}.'
            rows_n = [[x['name'], (x['level'] or 'other').capitalize(), x['grades'] or '—', 'Independent' if x['independent'] else 'Public', f'{d:.1f} km {bearing(me, (x["lat"], x["lon"]))}'] for d, x in within[:25]]
            bl += [H(f'Schools within {R} km of {nm}'), P(txt), tbl(f'Schools within {R} km of {nm}', ['School', 'Type', 'Grades', 'Public or independent', 'Distance and direction'], rows_n,
                   'Source: BC Data Catalogue, BC Schools - School Locations (Open Government Licence - BC). Distances are straight-line from the school coordinates, not walking or driving routes.')]
    # sparse areas: the next ring of schools, so the page still shows where a family has more choice
    if not r['approx'] and len([1 for d, x in cand if d <= R]) < 14:
        ring = [(d, x) for d, x in cand if R < d <= R + 4][:12]
        if len(ring) < 8: ring = [(d, x) for d, x in cand if R < d <= R + 8][:12]
        if len(ring) >= 4:
            bl += [H(f'More schools beyond {R} km from {nm}'),
                   tbl(f'Schools beyond {R} km from {nm}', ['School', 'Type', 'Grades', 'Public or independent', 'Distance and direction'],
                       [[x['name'], (x['level'] or 'other').capitalize(), x['grades'] or '—', 'Independent' if x['independent'] else 'Public', f'{d:.1f} km {bearing(me, (x["lat"], x["lon"]))}'] for d, x in ring],
                       'Source: BC Data Catalogue, BC Schools - School Locations (Open Government Licence - BC). Distances are straight-line from the school coordinates.')]
    # what to check
    chk = [f'Confirm the catchment for the exact address on the {f["district_name"]} school finder. A home a few blocks from {nm} can sit in a different catchment.' if not indep else f'Ask {nm} how admission works. A short distance does not give a child a place.',
           (f'Visit on a school day at drop-off and pick-up. Traffic and parking near {nm} are very different at 8:30 am and 3 pm than on a Sunday viewing.',
            f'Go past {nm} on a school morning and again mid-afternoon to see the traffic, parking and noise before you offer.',
            f'View the home on a school day. Drop-off and pick-up near {nm} change the street more than a weekend viewing shows.')[order]]
    if sd and n >= 10 and mid: chk.append(f'Compare price with similar homes farther from the school. The median {midlab[:-1] if midlab.endswith("s") else midlab} within {rk} of {nm} was {money(mid)}, so check whether size and age explain a gap before you pay for the location.')
    if not r['approx'] and 'within' in dir() and within:
        pr = next(((d, x) for d, x in within if f['level'] and x['level'] == f['level']), None)
        if pr: chk.append(f'Look at {pr[1]["name"]}, the nearest other {f["level"]} school, {pr[0]:.1f} km {bearing(me, (pr[1]["lat"], pr[1]["lon"]))} of {nm}. Compare the two when you check which school serves the address.')
    bl += [H(f'Before you offer on a home near {nm}'), L(chk)]
    if mid:
        bl += [H(f'Estimate the payment on a home near {nm}'), P(f'The calculator starts at the {midlab[:-1] if midlab.endswith("s") else midlab} median within {rk} of {nm}, {money(mid)}, and you can change the price, down payment and rate.'), {'t': 'calc', 'which': 'mortgage', 'price': mid, 'gen': G}]
    # FAQ
    faq = []
    if indep:
        faq.append((f'Does living near {nm} get a child a place?', f'No. {nm} is an independent school and sets its own admission, so distance does not decide it. Ask the school how applications and wait lists work.'))
    else:
        faq.append((f'Are the homes on this page in the {nm} catchment?', f'Not necessarily. The search finds homes whose listing names the school' + (', and the sold prices are measured by distance' if has else '') + f'. {f["district_name"]} School District sets the catchment' +
                    (' and shows it on a ' + ('map only' if f['catchment'] == 'map only' else 'page') + ' on its website' if f['catchment_url'] else '') + ', so confirm the exact address with the district before you offer.'))
    faq.append((f'How does the {nm} home search find homes?', f'It lists active homes whose listing text names {nm}, so a nearby home that leaves the name out will not show.'))
    if sd and n >= 10:
        gs = sd['groups']; ps = [f'{lab.lower()} {money(gs[k]["price"])}' for k, lab in gdef if gs[k].get('price')]
        if ps: faq.append((f'How much do homes near {nm} sell for?', f'Within {rk} of the school, {n} homes sold between {WIN.replace(" to ", " and ")}. Medians were ' + ', '.join(ps) + '. A median is the middle price and is shown where at least 5 homes sold.'))
        al = sd['all']
        if al.get('dom'): faq.append((f'How fast do homes sell near {nm}?', f'Within {rk} of {nm} the median was {al["dom"]} days on the market' + (f', closing at {al["ratio"]}% of the list price' if al.get('ratio') else '') + (f', with {al["over"]}% of sales above the list price' if al.get('over') is not None else '') + f' for the {n} homes within {rk}.'))
    # links
    links = []
    if r['area']: links.append((f'{r["area"]["area"]} neighbourhood guide', r['area']['page']))
    links.append((hubname, hub))
    if not r['approx'] and 'within' in dir() and len(within) >= 3:
        top3 = within[:3]
        faq.append((f'Which schools are closest to {nm}?', f'In a straight line, the closest schools in the provincial list are ' + ', '.join(f'{x["name"]} ({d:.1f} km {bearing(me, (x["lat"], x["lon"]))})' for d, x in top3[:-1]) + f' and {top3[-1][1]["name"]} ({top3[-1][0]:.1f} km {bearing(me, (top3[-1][1]["lat"], top3[-1][1]["lon"]))}).'))
    links += SEARCHES[r['hubkey']] + [('Recently sold homes', 'sold-properties'), ('Find out what your home is worth', 'home-evaluation'), ('First-time home buyer program', 'first-time-home-buyer-program'), ('Home buyer questions in BC', 'faq-for-home-buyers-in-bc')]
    seen = set(); links = [x for x in links if not (x[1] in seen or seen.add(x[1]))]
    return N.finish(slug, seo, [(hubname, hub)], faq, bl, f'Homes near {nm}: your questions answered', links, dict(search_page=dict(kind='school', school=nm, city=r['hubkey'], radius=rad, sold=bool(sd and n >= 10))))


def add_blocks(host, gen, blocks, key):
    f = f'src/data/local/{host}.json'
    if os.path.exists(f):
        raw = open(f).read(); d = json.loads(raw); nl = '\n' if raw.endswith('\n') else ''
        line2 = raw.split('\n')[1] if '\n' in raw else ''; ind = len(line2) - len(line2.lstrip(' ')) or 1; asc = '\\u' in raw
    else:
        if not os.path.exists(f'src/data/pages/{host}.json'): return False
        d = dict(status='generated', slug=host, updated=N.UPDATED, blocks=[], faq=[]); ind, asc, nl = 1, False, ''
    d['blocks'] = [b for b in d['blocks'] if not (b.get('gen') == gen and b.get('hubkey') == key)]
    d['blocks'] += [dict(b, gen=gen, pos='end', hubkey=key) for b in blocks]
    open(f, 'w').write(json.dumps(d, indent=ind, ensure_ascii=asc) + nl); return True


def inbound(built):
    byhub, byarea = collections.defaultdict(list), collections.defaultdict(list)
    for r in built:
        byhub[HUB[r['hubkey']][0]].append(r)
        if r['area']: byarea[r['area']['page']].append(r)
    nh = na = 0
    for host, rs in byhub.items():
        rs = sorted(rs, key=lambda x: x['school'])
        nh += add_blocks(host, 'schoollinks', [{'t': 'h', 'level': 2, 'text': 'Homes for sale near each school'},
                                               {'t': 'p', 'text': 'Each page lists homes for sale whose listing names the school, with school facts and the schools nearby. Where enough homes sold close to the school, it also shows what they sold for.'},
                                               {'t': 'list', 'items': [[lk(f'Homes for sale near {x["school"]}' + (f' ({x["city"]})' if x['dup'] else ''), x['slug'])] for x in rs]}], 'hub')
    for host, rs in byarea.items():
        rs = sorted(rs, key=lambda x: x['school'])
        na += add_blocks(host, 'schoollinks', [{'t': 'h', 'level': 2, 'text': 'Homes for sale near schools here'},
                                               {'t': 'list', 'items': [[lk(f'Homes for sale near {x["school"]}', x['slug'])] for x in rs]}], 'area')
    print(nh, 'hub blocks;', na, 'area guide blocks')


if __name__ == '__main__': main()
