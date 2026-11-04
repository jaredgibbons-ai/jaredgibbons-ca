"""Sold-price layer from Jared's Paragon closed-sales export (Nov 1, 2025 to Oct 29, 2026; 30,250 closed sales).

  python3 -I tools/build_sold_layer.py --csv <export.csv>   re-aggregate into src/data/sold/sold-12m.json, then write blocks
  python3 -I tools/build_sold_layer.py                      write blocks from the saved aggregate

Rules: closed sales only (pending rows are not sales); the raw rows (which carry MLS numbers) never enter the repo, only grouped figures;
a group needs 5 sales before a median is published and 3 before it is mentioned at all; a building needs 5 sales before it is named with a price.
Blocks carry gen 'sold' and are rebuilt every run.  Library functions are used by build_gap_pages.py and build_brentwood.py."""
import argparse, collections, csv, glob, json, os, re, statistics as st, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
AGG = os.path.join(ROOT, 'src/data/sold/sold-12m.json')
MIN_MED, MIN_MENTION, MIN_BLDG = 5, 3, 5
G = 'sold'
GROUPS = {'house': 'Houses', 'condo': 'Condos', 'townhome': 'Townhomes', 'duplex': 'Duplexes (half and full)', 'acreage': 'Houses with acreage', 'mobile': 'Manufactured homes', 'land': 'Vacant land'}
GL = {'house': 'houses', 'condo': 'condos', 'townhome': 'townhomes', 'duplex': 'duplexes', 'acreage': 'houses with acreage', 'mobile': 'manufactured homes', 'land': 'lots and land'}
QUARTERS = [('Nov 2025 to Jan 2026', ('2025-11', '2025-12', '2026-01')), ('Feb to Apr 2026', ('2026-02', '2026-03', '2026-04')), ('May to Jul 2026', ('2026-05', '2026-06', '2026-07')), ('Aug to Oct 2026', ('2026-08', '2026-09', '2026-10'))]
import datetime
WINDOW = 'November 1, 2025 to October 22, 2026'
if os.path.exists(AGG):  # the window always ends on the last closed sale actually in the file
    _l = json.load(open(AGG, encoding='utf-8'))['meta']['last']; _d = datetime.date.fromisoformat(_l)
    WINDOW = f'November 1, 2025 to {_d.strftime("%B")} {_d.day}, {_d.year}'
# our city keys -> Paragon (Area, sub-areas to leave out)
CITYSEL = {
 'surrey': [('Surrey', ()), ('North Surrey', ()), ('Cloverdale', ()), ('South Surrey White Rock', ('White Rock',))],
 'south-surrey': [('South Surrey White Rock', ('White Rock',))], 'cloverdale': [('Cloverdale', ())], 'north-delta': [('N. Delta', ())], 'ladner': [('Ladner', ())],
 'mission': [('Mission', ())], 'burnaby': [('Burnaby North', ()), ('Burnaby South', ()), ('Burnaby East', ())], 'coquitlam': [('Coquitlam', ())],
 'port-coquitlam': [('Port Coquitlam', ())], 'port-moody': [('Port Moody', ())], 'new-westminster': [('New Westminster', ())],
 'tsawwassen': [('Tsawwassen', ())], 'maple-ridge': [('Maple Ridge', ())], 'chilliwack': [('Chilliwack', ())],
}
# SnapStats area key -> Paragon areas (for community and type pages)
SNAP_AREAS = {'abbotsford': ['Abbotsford'], 'surrey': ['Surrey', 'North Surrey'], 'south-surrey-white-rock': ['South Surrey White Rock'], 'north-delta': ['N. Delta'], 'cloverdale': ['Cloverdale'],
              'langley': ['Langley'], 'mission': ['Mission'], 'burnaby': ['Burnaby North', 'Burnaby South', 'Burnaby East'], 'new-westminster': ['New Westminster'], 'coquitlam': ['Coquitlam'],
              'port-coquitlam': ['Port Coquitlam'], 'port-moody': ['Port Moody'], 'pitt-meadows': ['Pitt Meadows'], 'maple-ridge': ['Maple Ridge'], 'chilliwack': ['Chilliwack', 'East Chilliwack']}
ALIAS = {'central port coquitlam': 'central pt coquitlam', 'simon fraser university sfu': 'simon fraser univer'}


def nz(s):
    s = ALIAS.get(s.lower(), s.lower()).replace('&', 'and')
    s = re.sub(r'\b(bn|bs|be|pq|pm|cq|nw|bc|mr|surrey|langley|burnaby|coquitlam)\b', '', s)
    return re.sub(r'[^a-z0-9]+', '', s)


def num(s):
    s = (s or '').replace('$', '').replace(',', '').strip()
    try: return float(s)
    except ValueError: return None


def group_of(a):
    if a['Prop Type'] == 'Land Only': return 'land'
    t = a['Type of Dwelling']
    return {'Apartment/Condo': 'condo', 'Townhouse': 'townhome', 'House/Single Family': 'house', 'House with Acreage': 'acreage', '1/2 Duplex': 'duplex', 'Duplex': 'duplex', 'Triplex': 'duplex', 'Fourplex': 'duplex',
            'Manufactured': 'mobile', 'Manufactured with Land': 'mobile'}.get(t)


def med(v): v = [x for x in v if x is not None]; return st.median(v) if v else None
def pctile(v, p):
    v = sorted(x for x in v if x is not None)
    if not v: return None
    k = (len(v) - 1) * p; f = int(k); c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def stats(rows, g):
    n = len(rows); o = {'n': n}
    if n < MIN_MENTION: return o
    p = [num(a['Sold Price']) for a in rows]; lp = [num(a['List Price']) for a in rows]
    o['price'] = round(med(p)); o['dom'] = round(med([num(a['Days On Market']) for a in rows]))
    rat = [100 * s / l for s, l in zip(p, lp) if s and l]
    o['ratio'] = round(med(rat), 1) if rat else None
    o['over'] = round(100 * sum(1 for s, l in zip(p, lp) if s and l and s > l) / n)
    if n >= 8: o['p25'] = round(pctile(p, .25)); o['p75'] = round(pctile(p, .75))
    fa = [(num(a['Sold Price']), num((a['Floor Area -Grand Total'] or '').replace(',', ''))) for a in rows]
    ppsf = [s / f for s, f in fa if s and f and f > 200]
    if len(ppsf) >= MIN_MENTION and g in ('condo', 'townhome', 'house', 'duplex'): o['ppsf'] = round(med(ppsf))
    yb = [num(a['Approx. Year Built']) for a in rows]; yb = [y for y in yb if y and 1850 < y < 2030]
    if len(yb) >= MIN_MENTION: o['yb'] = round(med(yb))
    mf = [num(a['Maintenance Fee']) for a in rows]; mf = [m for m in mf if m and m > 0]
    if len(mf) >= MIN_MENTION and g in ('condo', 'townhome', 'duplex'): o['maint'] = round(med(mf)); o['maint_n'] = len(mf)
    if g in ('condo', 'townhome', 'house', 'duplex'):
        bd = [num(a['Total Bedrooms']) for a in rows]; bd = [b for b in bd if b is not None]
        if len(bd) >= MIN_MED: o['beds'] = round(med(bd))
    if g in ('house', 'acreage', 'land', 'mobile'):
        ls = [num((a['Lot Sz (Sq.Ft.)'] or '').replace(',', '')) for a in rows]; ls = [x for x in ls if x]
        if len(ls) >= MIN_MENTION: o['lot_sqft'] = round(med(ls))
        ac = [num(a['Lot Sz (Acres)']) for a in rows]; ac = [x for x in ac if x]
        if len(ac) >= MIN_MENTION: o['acres'] = round(med(ac), 2)
    q = []
    for lab, ms in QUARTERS:
        qq = [a for a in rows if a['Sold Date'][:7] in ms]
        q.append({'n': len(qq), 'price': round(med([num(a['Sold Price']) for a in qq])) if len(qq) >= MIN_MED else None})
    o['q'] = q
    return o


SUFFIX = r'\s+(TOWER|BUILDING|BLDG|PHASE)\s+[0-9A-Z]{1,2}$'


def ckey(name):
    k = re.sub(r'[^A-Z0-9]+', ' ', name.upper()).strip()
    return re.sub(r'^THE\s+', '', re.sub(SUFFIX, '', k))


def nice(name):
    n = re.sub(SUFFIX, '', name.strip(), flags=re.I)
    if n.isupper() or n.islower(): n = re.sub(r"(?<=[A-Za-z])'S\b", "'s", n.title())
    n = re.sub(r'\b(Of|The|And|At|On)\b', lambda m: m.group(1).lower(), n)
    n = re.sub(r'^the\b', 'The', n)
    return re.sub(r'^The\s+(?=City of Lougheed)', '', n)


def complexes(rows):
    by = collections.defaultdict(list)
    for a in rows:
        if a['Complex/Subdivision Name'].strip(): by[ckey(a['Complex/Subdivision Name'])].append(a)
    out = []
    for k, v in by.items():
        if len(v) < MIN_MENTION: continue
        names = collections.Counter(a['Complex/Subdivision Name'].strip() for a in v)
        disp = nice(names.most_common(1)[0][0])
        s = stats(v, group_of(v[0]))
        out.append({'name': disp, 'n': len(v), **{x: s[x] for x in ('price', 'dom', 'yb', 'maint', 'ratio') if x in s}})
    return sorted(out, key=lambda x: -x['n'])


BANDS = [(0, 600000, 'Under $600,000'), (600000, 800000, '$600,000 to $799,999'), (800000, 1000000, '$800,000 to $999,999'), (1000000, 1200000, '$1,000,000 to $1,199,999'),
         (1200000, 1500000, '$1,200,000 to $1,499,999'), (1500000, 1800000, '$1,500,000 to $1,799,999'), (1800000, 10 ** 12, '$1,800,000 and over')]


def band_counts(rows):
    p = [num(a['Sold Price']) for a in rows]
    return [sum(1 for x in p if x is not None and lo <= x < hi) for lo, hi, _ in BANDS]


def city_entry(rows, bysub, sel):
    v = [a for a in rows if any(a['Area'] == ar and a['Sub-Area/Community'] not in ex for ar, ex in sel)]
    d = {g: stats([a for a in v if group_of(a) == g], g) for g in GROUPS if any(group_of(a) == g for a in v)}
    for g in d: d[g]['bands'] = band_counts([a for a in v if group_of(a) == g])
    cx = {g: complexes([a for a in v if group_of(a) == g]) for g in ('condo', 'townhome')}
    return {'groups': d, 'complexes': {g: c[:40] for g, c in cx.items() if c}, 'subs': sorted(f'{ar}|{sb}' for ar, ex in sel for (a2, sb) in bysub if a2 == ar and sb not in ex)}


def add_cities(csv_path, keys):
    """Add city keys (and price bands for every city) to the saved aggregate from the same export, using only sales up to the saved window's last day. Existing figures are not recomputed."""
    agg = json.load(open(AGG, encoding='utf-8')); last = agg['meta']['last']
    rows = [a for a in csv.DictReader(open(csv_path, encoding='utf-8-sig')) if a['Status'] == 'Closed' and group_of(a) and a['Sold Date'] <= last]
    bysub = collections.defaultdict(list)
    for a in rows: bysub[(a['Area'], a['Sub-Area/Community'])].append(a)
    for ck in keys:
        agg['city'][ck] = city_entry(rows, bysub, CITYSEL[ck])
    for ck, sel in CITYSEL.items():           # bands for the cities that already existed
        if ck in agg['city'] and ck not in keys:
            e = city_entry(rows, bysub, sel)
            for g, grp in agg['city'][ck]['groups'].items():
                if g in e['groups'] and e['groups'][g]['n'] == grp['n']: grp['bands'] = e['groups'][g]['bands']
                elif g in e['groups']: print('count differs for', ck, g, grp['n'], e['groups'][g]['n'])
    json.dump(agg, open(AGG, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('added', keys, 'rows used', len(rows))


def aggregate(csv_path):
    rows = [a for a in csv.DictReader(open(csv_path, encoding='utf-8-sig')) if a['Status'] == 'Closed' and group_of(a)]
    dates = [a['Sold Date'] for a in rows]
    out = {'meta': {'window': WINDOW, 'first': min(dates), 'last': max(dates), 'closed': len(rows), 'source': 'Paragon closed-sales export supplied by Jared, 2026-11-01. Pending sales excluded. Raw rows are not stored.'}, 'sub': {}, 'city': {}}
    bysub = collections.defaultdict(list)
    for a in rows: bysub[(a['Area'], a['Sub-Area/Community'])].append(a)
    for (ar, sb), v in bysub.items():
        d = {}
        for g in GROUPS:
            r = [a for a in v if group_of(a) == g]
            if r: d[g] = stats(r, g)
        cx = {g: complexes([a for a in v if group_of(a) == g]) for g in ('condo', 'townhome')}
        out['sub'][f'{ar}|{sb}'] = {'groups': d, 'complexes': {g: c for g, c in cx.items() if c}}
    for ck, sel in CITYSEL.items(): out['city'][ck] = city_entry(rows, bysub, sel)
    os.makedirs(os.path.dirname(AGG), exist_ok=True)
    json.dump(out, open(AGG, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return out


def load(): return json.load(open(AGG, encoding='utf-8'))


# ---------- wording ----------
def money(v): return '—' if v is None else f'${v:,.0f}'
def P(t, **k): return {'t': 'p', 'text': t, 'gen': G, **k}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': G, **k}
SRC = f'Source: Paragon, the MLS® system used by Jared’s office, closed sales from {WINDOW}. Pending sales are not counted. Median means the middle price, so half sold for more and half for less. Sold vs list is the sale price as a percentage of the last list price.'
SRC_MIN = f' A figure is shown only where at least {MIN_MED} homes sold, and a community is listed only with {MIN_MED} or more sales; with fewer, one sale would be the whole figure.'


def row(label, s, g):
    n = s['n']
    if n < MIN_MED or 'price' not in s: return [label, str(n), 'Too few sales for a typical price', '—', '—', '—']
    return [label, f'{n:,}', money(s['price']), f'{s["dom"]} days', f'{s["ratio"]:.1f}%' if s.get('ratio') else '—', money(s['ppsf']) if s.get('ppsf') else '—']


def one_line(label, s, g, extra=True):
    """Sentence for one group: only what n supports."""
    n = s['n']
    if n < MIN_MENTION: return f'Fewer than {MIN_MENTION} {GL[g]} sold in {label}, too few to describe.'
    if n < MIN_MED: return f'{n} {GL[g]} sold in {label}, too few ({MIN_MED} needed) to give a typical price.'
    t = f'{n:,} {GL[g]} sold in {label} with a median price of {money(s["price"])}'
    if 'p25' in s: t += f' (the middle half sold between {money(s["p25"])} and {money(s["p75"])})'
    t += f', taking a median of {s["dom"]} days to sell at {s["ratio"]:.1f}% of the last list price'
    if s.get('over') is not None: t += f'; {s["over"]}% sold above list'
    t += '.'
    if extra:
        bits = []
        if s.get('ppsf'): bits.append(f'a median {money(s["ppsf"])} per square foot')
        if s.get('yb'): bits.append(f'a median year built of {s["yb"]}')
        if s.get('maint'): bits.append(f'a median strata fee of {money(s["maint"])} a month')
        if s.get('acres') and g in ('acreage', 'land'): bits.append(f'a median lot of {s["acres"]} acres')
        elif s.get('lot_sqft') and g in ('house', 'mobile'): bits.append(f'a median lot of {s["lot_sqft"]:,} square feet')
        if bits: t += ' They had ' + ', '.join(bits[:-1]) + (' and ' if len(bits) > 1 else '') + bits[-1] + '.'
    return t


def quarter_table(label, s, g):
    q = s.get('q')
    if not q or any(x['n'] < MIN_MED or x['price'] is None for x in q): return []
    return [{'t': 'table', 'caption': f'{label}: {GL[g]} sold by quarter', 'head': ['Period', 'Sold', 'Median price'], 'rows': [[lab, str(x['n']), money(x['price'])] for (lab, _), x in zip(QUARTERS, q)],
             'source': SRC + ' A quarter is shown only when each of the four has 5 or more sales, and the table does not call the change a trend.', 'gen': G}]


LABEL = {'Simon Fraser Univer.': 'Simon Fraser University', 'Central Pt Coquitlam': 'Central Port Coquitlam', 'Crescent Bch Ocean Pk.': 'Crescent Beach and Ocean Park', 'Glenwood PQ': 'Glenwood', 'Citadel PQ': 'Citadel', 'Lincoln Park PQ': 'Lincoln Park'}


def clean_label(nm):
    return LABEL.get(nm) or re.sub(r'\s+(BN|BS|BE|PQ|PM|CQ|NW|BC)$', '', nm)


def sub_table(label, subs, g, agg, limit=14):
    rows = []
    for k in subs:
        s = agg['sub'].get(k, {}).get('groups', {}).get(g)
        if s and s['n'] >= MIN_MED and 'price' in s: rows.append((s['n'], k.split('|')[1], s))
    rows.sort(key=lambda x: -x[0]); rows = rows[:limit]
    if len(rows) < 2: return []
    return [{'t': 'table', 'caption': f'{label}: {GL[g]} sold by community', 'head': ['Community', 'Sold', 'Median price', 'Median days to sell', 'Sold vs list', 'Median per sq ft'],
             'rows': [row(clean_label(nm), s, g) for _, nm, s in rows], 'source': SRC + SRC_MIN, 'gen': G}]


def bldg_table(label, cx, g, limit=12):
    rows = [c for c in cx if c['n'] >= MIN_BLDG and 'price' in c][:limit]
    if len(rows) < 3: return []
    return [{'t': 'table', 'caption': f'{label}: buildings and complexes with the most {GL[g]} sold', 'head': ['Building or complex', 'Sold', 'Median price', 'Median days to sell', 'Median year built', 'Median strata fee'],
             'rows': [[c['name'], str(c['n']), money(c['price']), f'{c["dom"]} days', str(c['yb']) if c.get('yb') else '—', (money(c['maint']) + ' a month') if c.get('maint') else '—'] for c in rows],
             'source': SRC + f' Names are as entered in the MLS® listings; a building is listed only with {MIN_BLDG} or more sales, and its price is the median of those sales, not any one home.', 'gen': G}]


def mix_table(label, groups, order):
    rows = [row(GROUPS[g], groups[g], g) for g in order if g in groups and groups[g]['n'] >= MIN_MENTION]
    if not rows: return []
    return [{'t': 'table', 'caption': f'{label}: what sold, by home type', 'head': ['Home type', 'Sold', 'Median price', 'Median days to sell', 'Sold vs list', 'Median per sq ft'], 'rows': rows, 'source': SRC + SRC_MIN.replace('a community is listed only with', 'a row is shown only with'), 'gen': G}]


def sold_faq(label, noun, s, g):
    n = s['n']
    if n < MIN_MED or 'price' not in s: return []
    return [{'gen': G, 'q': f'What did {noun} in {label} sell for?', 'a': f'{n:,} {GL[g]} sold in {label} between {WINDOW}, with a median price of {money(s["price"])}.'},
            {'gen': G, 'q': f'How long do {noun} take to sell in {label}?', 'a': f'The median was {s["dom"]} days from listing to sale, and homes sold at a median {s["ratio"]:.1f}% of the last list price ({s["over"]}% sold above list), for sales {WINDOW}.'}]



def sold_faq_more(label, noun, s, g, cd, agg):
    """More questions answered from the same figures; each answer carries this page's own numbers."""
    n = s['n']
    if n < MIN_MED or 'price' not in s: return []
    f = lambda q, a: {'gen': G, 'q': q, 'a': a}; out = []
    if 'p25' in s: out.append(f(f'What price range do most {noun} in {label} sell in?', f'The middle half of the {n:,} {GL[g]} that sold in {label} went for between {money(s["p25"])} and {money(s["p75"])}, around a median of {money(s["price"])}.'))
    out.append(f(f'Do {noun} in {label} sell above asking price?', f'{s["over"]}% of the {n:,} {GL[g]} sold for more than the last list price, and the median sale was {s["ratio"]:.1f}% of it.'))
    if s.get('maint'): out.append(f(f'What is a typical strata fee for {noun} in {label}?', f'Of the {n:,} sales, {s["maint_n"]} listings gave a monthly fee and the median was {money(s["maint"])}.'))
    if s.get('yb'): out.append(f(f'How old are the {noun} that sold in {label}?', f'The median year built was {s["yb"]} for the {n:,} {GL[g]} sold in {label}.'))
    if s.get('beds') is not None and g in ('condo', 'townhome', 'house'): out.append(f(f'How many bedrooms do {noun} in {label} usually have?', f'The median {GL[g][:-1] if GL[g].endswith("s") else GL[g]} that sold in {label} had {s["beds"]} bedrooms, from the {n:,} sales between {WINDOW}.'))
    if cd:
        best = sorted(((agg['sub'].get(k, {}).get('groups', {}).get(g, {}).get('n', 0), k.split('|')[1]) for k in cd.get('subs', [])), reverse=True)[:3]
        if best and best[0][0] >= MIN_MED: out.append(f(f'Which {label} communities sold the most {noun}?', 'By number sold: ' + ', '.join(f'{nm} ({c:,})' for c, nm in best if c >= MIN_MED) + f', for {WINDOW}.'))
        bl = [c for c in cd.get('complexes', {}).get(g, []) if c['n'] >= MIN_BLDG][:3]
        if len(bl) >= 3: out.append(f(f'Which {label} buildings sold the most {noun}?', 'By number sold: ' + ', '.join(f'{c["name"]} ({c["n"]})' for c in bl) + f', for {WINDOW}.'))
    return out


# ---------- community and type pages ----------
def sub_key(agg, ak, name):
    want = nz(name)
    for ar in SNAP_AREAS.get(ak, []):
        for k in agg['sub']:
            if k.startswith(ar + '|') and nz(k.split('|', 1)[1]) == want: return k
    return None


def page_blocks(agg, k, disp, types):
    d = agg['sub'][k]; g = d['groups']; order = [x for x in types if x in g and g[x]['n'] >= MIN_MENTION]
    if not order: return []
    big = max(order, key=lambda x: g[x]['n'])
    label = disp
    bl = [H(f'{disp} home prices: what sold, November 2025 to October 2026')]
    bl.append(P(' '.join(one_line(disp, g[x], x) for x in sorted(order, key=lambda x: -g[x]['n'])[:2])))
    bl += mix_table(disp, g, types)
    bl += quarter_table(disp, g[big], big) if g[big]['n'] >= 12 else []
    for x in ('condo', 'townhome'):
        if x in types and d['complexes'].get(x): bl += bldg_table(disp, d['complexes'][x], x)
    return bl


def city_blocks(agg, ck, label, types, band=None):
    cd = agg['city'].get(ck)
    if not cd: return [], []
    g = cd['groups']; order = [x for x in types if x in g and g[x]['n'] >= MIN_MENTION]
    if not order: return [], []
    big = max(order, key=lambda x: g[x]['n']); noun = GL[big]
    if band:
        bl = [H(f'{label} {noun} sold: price bands, {WINDOW}')]
        idx = [i for i, (lo, hi, _) in enumerate(BANDS) if hi <= band]; parts = []
        for x in order:
            bc = g[x].get('bands'); tot = g[x]['n']
            if not bc: continue
            under = sum(bc[i] for i in idx)
            parts.append(f'{under:,} of {tot:,} {GL[x]} ({round(100 * under / tot)}%)')
        if parts: bl.append(P(f'In {label}, the sales at {money(band)} or less were ' + ', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1] + f', for sales {WINDOW}. The table shows how many sold in each price band.'))
        rows = []
        for i, (lo, hi, nm) in enumerate(BANDS):
            r = [nm]
            for x in order:
                bc = g[x].get('bands'); r.append(('Fewer than 5' if bc[i] < MIN_MED else str(bc[i])) if bc else '—')
            rows.append(r)
        bl.append({'t': 'table', 'caption': f'{label}: how many sold in each price band', 'head': ['Price band'] + [GROUPS[x] for x in order], 'rows': rows, 'source': SRC + ' A count under 5 is shown as "Fewer than 5".', 'gen': G})
        for x in sorted(order, key=lambda y: -g[y]['n']): bl.append(P(one_line(label, g[x], x)))
        hx = g.get('house')
        if hx and hx['n'] >= MIN_MED and 'p25' in hx:
            bl.append(P(f'These are closed-sale prices, so they show what {label} homes actually sold for, not what they were listed at. A {label} house listed today at {money(band)} or less can be measured against them: the middle half of the {hx["n"]:,} houses sold between {money(hx["p25"])} and {money(hx["p75"])}, and half of them sold in {hx["dom"]} days or fewer.'))
    else:
        bl = [H(f'{label} {noun}: what sold, {WINDOW}')]
        bl.append(P(' '.join(one_line(label, g[x], x) for x in sorted(order, key=lambda x: -g[x]['n'])[:2])))
    bl += mix_table(label, g, types) + (quarter_table(label, g[big], big) if g[big]['n'] >= 12 else [])
    for x in (sorted(order, key=lambda y: -g[y]['n']) if band else [big]): bl += sub_table(label, cd['subs'], x, agg)
    for x in ('condo', 'townhome'):
        if x in types and cd['complexes'].get(x): bl += bldg_table(label, cd['complexes'][x], x)
    faq = (sold_faq(label, noun, g[big], big) + sold_faq_more(label, noun, g[big], big, cd, agg)) if g[big]['n'] >= MIN_MED else []
    return bl, faq


def apply_pages():
    agg = load(); changed = 0; hit = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
        j = json.load(open(f, encoding='utf-8')); slug = os.path.basename(f)[:-5]
        before = json.dumps(j, sort_keys=True)
        tp = j.get('type_page'); cm = j.get('community') or j.get('sold_sub')   # sold_sub: link a page to a sold sub-area without the side effects of 'community' (community lists, snapstats mapping)
        if (tp or cm) and not slug.startswith('brentwood') and not j.get('gen_gap'):
            j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != G]
            ak, name = (tp['area'], tp['name']) if tp else (cm['area'], cm['name'])
            k = sub_key(agg, ak, name)
            if k:
                disp = name
                types = {'detached': ['house'], 'condo_townhome': ['condo', 'townhome']}.get(tp['type'] if tp else '', ['house', 'condo', 'townhome', 'duplex'])
                new = page_blocks(agg, k, disp, types)
                if new:
                    j['blocks'] += new; hit += 1
                    if j.get('faq') is not None:
                        j['faq'] = [q for q in j['faq'] if q.get('gen') != G and 'November 1, 2025 to' not in q.get('a', '')]
                        g = agg['sub'][k]['groups']; ex = [x for x in types if x in g and g[x]['n'] >= MIN_MED]
                        if ex:
                            x = max(ex, key=lambda y: g[y]['n']); qs = {q['q'] for q in j['faq']}
                            j['faq'] += [q for q in sold_faq(disp, GL[x], g[x], x) if q['q'] not in qs]
            j['needs_from_muse'] = [n for n in j.get('needs_from_muse', []) if not re.search(r'sold (prices|listings)|days on market', n, re.I)] if j.get('needs_from_muse') else j.get('needs_from_muse')
        cp = j.get('city_page')              # {'city': 'ladner', 'label': 'Ladner', 'types': ['house'], 'band': 1800000?}
        if cp:
            j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != G]
            bl, fq = city_blocks(agg, cp['city'], cp['label'], cp['types'], cp.get('band'))
            if bl:
                j['blocks'] += bl; hit += 1
                j['faq'] = [q for q in j.get('faq', []) if q.get('gen') != G]
                qs = {q['q'] for q in j['faq']}; j['faq'] += [q for q in fq if q['q'] not in qs]
        if json.dumps(j, sort_keys=True) != before:
            with open(f, 'w', encoding='utf-8') as fh: json.dump(j, fh, indent=2, ensure_ascii=False); fh.write('\n')
            changed += 1
    print('pages with sold blocks', hit, '| files changed', changed)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--csv'); ap.add_argument('--add-cities', nargs='+', metavar='CSV_THEN_KEYS', help='CSV path followed by city keys to add to the saved aggregate'); a = ap.parse_args()
    if a.add_cities: add_cities(a.add_cities[0], a.add_cities[1:])
    if a.csv:
        o = aggregate(a.csv); print('aggregated', o['meta'], len(o['sub']), 'sub-areas')
    apply_pages()
