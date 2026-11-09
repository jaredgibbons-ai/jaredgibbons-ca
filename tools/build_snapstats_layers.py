"""Build community-level market sections from the parsed SnapStats(R) monthly data (src/data/snapstats/*.json).

For every neighbourhood page and neighbourhood guide that maps to a community in the reports, write generated blocks
(gen: "snapstats") into src/data/local/<slug>.json. Old generated blocks are removed first, so a new month refreshes everything.

Only figures are used, written up in our own words and our own tables. The reports themselves are not posted.
The area page and the guide for the same community carry different cuts of the numbers so they do not repeat each other.

    python3 -I tools/build_snapstats_layers.py [--report]
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend as TR

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MN = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
SRC = 'Source: MLS® data from the Greater Vancouver REALTORS® and the Fraser Valley Real Estate Board, compiled by SnapStats®.'
RATIO_NOTE = ' Sales ratio is homes sold divided by homes listed. On the reports’ own scale under 12% is a buyers’ market, 12% to 20% is balanced and over 20% is a sellers’ market. With fewer than ten homes listed, one sale moves the ratio a long way, so treat it as a rough signal.'
PRICE_NOTE = ' The reports give one sale-price figure a month and do not say whether it is an average or a median, so use it for direction, not as a valuation of your own home.'
BOARD_NAME = {'GVR': 'Greater Vancouver REALTORS®', 'FVR': 'Fraser Valley Real Estate Board'}

# slug base (after removing -guide) -> (area key, community name) where the slug is not just the community name
ALIAS = {
    'mission-west-mission': ('mission', 'Mission West'), 'steelhead-mission': ('mission', 'Steelhead'), 'durieu-mission': ('mission', 'Durieu'),
    'dewdney-deroche-mission': ('mission', 'Dewdney Deroche'), 'mission-bc-mission': ('mission', 'Mission'), 'mission-bc': ('mission', 'Mission'),
    'stave-falls-mission': ('mission', 'Stave Falls'), 'lake-errock-mission': ('mission', 'Lake Errock'), 'hatzic-mission': ('mission', 'Hatzic'),
    'hemlock-valley-mission': ('mission', 'Hemlock'),
    'central-meadows-pitt-meadows': ('pitt-meadows', 'Central Meadows'), 'mid-meadows-pitt-meadows': ('pitt-meadows', 'Mid Meadows'),
    'north-meadows-pitt-meadows': ('pitt-meadows', 'North Meadows'), 'south-meadows-pitt-meadows': ('pitt-meadows', 'South Meadows'),
    'west-meadows-pitt-meadows': ('pitt-meadows', 'West Meadows'),
    'thornhill-maple-ridge': ('maple-ridge', 'Thornhill'), 'thornhill-mr': ('maple-ridge', 'Thornhill'),
    'cottonwood-maple-ridge': ('maple-ridge', 'Cottonwood'), 'cottonwood-mr': ('maple-ridge', 'Cottonwood'),
    'northwest-maple-ridge': ('maple-ridge', 'Northwest'), 'southwest-maple-ridge': ('maple-ridge', 'Southwest'),
    'northeast-maple-ridge': ('maple-ridge', 'Northeast'), 'north-maple-ridge': ('maple-ridge', 'North'),
    'west-central-maple-ridge': ('maple-ridge', 'West Central'), 'east-central-maple-ridge': ('maple-ridge', 'East Central'),
    'eagle-ridge-cq': ('coquitlam', 'Eagle Ridge'), 'capitol-hill-bn': ('burnaby', 'Capitol Hill'), 'edmonds-be': ('burnaby', 'Edmonds'),
    'queen-mary-park-surrey': ('surrey', 'Queen Mary Park'), 'cloverdale-bc': ('cloverdale', 'Cloverdale'), 'downtown-nw': ('new-westminster', 'Downtown'),
    'langley-city': ('langley', 'Langley City'),
    # existing pages whose slugs carry a city code or a home-type suffix
    'central-bn': ('burnaby', 'Central'), 'central-park-bs': ('burnaby', 'Central Park'), 'forest-glen-bs': ('burnaby', 'Forest Glen'),
    'forest-hills-bn': ('burnaby', 'Forest Hills'), 'metrotown-homes-for-sale': ('burnaby', 'Metrotown'), 'fraserview-nw': ('new-westminster', 'Fraserview'),
    'anmore-homes-for-sale': ('port-moody', 'Anmore'), 'grandview-surrey': ('south-surrey-white-rock', 'Grandview'),
    'sunnyside-park-surrey': ('south-surrey-white-rock', 'Sunnyside Park'),
}
# the same community name exists under more than one area key: pin the area where the slug alone would be ambiguous
AMBIG = {'central': 'burnaby', 'downtown': 'new-westminster', 'north': 'maple-ridge'}


def norm(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def pct(v): return '—' if v is None else f'{v}%'
def num(v): return '—' if v is None else f'{v:,}'
def kind(r):  # the reports' own scale: under 12% buyers, 12-20% balanced, over 20% sellers
    return None if r is None else ('a buyers’ market' if r < 12 else 'a balanced market' if r <= 20 else 'a sellers’ market')


def load_months():
    return {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/snapstats/[0-9]*.json')))}


def series(months, ak, t, name):
    out = []
    for m, d in months.items():
        a = d['areas'].get(ak)
        if not a: out.append((m, None)); continue
        row = next((c for c in a[t]['communities'] if c['name'] == name), None)
        out.append((m, row))
    return out


def best_bet(months, ak, t, name):
    """Months in which the report named the community in its buyers / sellers best-bet bullets (a sellers' best bet means fast sales relative to listings)."""
    res = {'buyers': [], 'sellers': []}
    for m, d in months.items():
        a = d['areas'].get(ak)
        if not a: continue
        for b in a[t]['market_summary']:
            for k, key in (('Buyers Best Bet', 'buyers'), ('Sellers Best Bet', 'sellers')):
                if b.startswith(k) and re.search(r'(?<![A-Za-z])' + re.escape(name) + r'(?![A-Za-z])', b): res[key].append(m)
    return res


def mlabel(m): return MN[m[5:]] + ' ' + m[:4]
def month_name(m): return MN[m[5:]]


TL = {'detached': 'Detached houses', 'condo_townhome': 'Condos and townhomes'}


def build(slug, guide, ak, name, months, city_name):
    keys = list(months)
    last = keys[-1]; first = keys[0]
    S = {t: series(months, ak, t, name) for t in TL}
    have = {t: [r for _, r in S[t] if r] for t in TL}
    if not any(have.values()): return None
    if sum((r['inventory'] or 0) + (r['sales'] or 0) for t in TL for r in have[t]) == 0: return None  # nothing listed or sold in any month: a table of zeros helps nobody
    area = months[last]['areas'][ak]
    blocks = []
    cur = {t: dict(S[t])[last] for t in TL}
    act = {t: sum((r['inventory'] or 0) + (r['sales'] or 0) for r in have[t]) > 0 for t in TL}  # a home type with nothing listed or sold in any month is left out
    span = f'{month_name(first)} to {month_name(last)} {last[:4]}'
    # Template wording is identical on every page (search engines treat that as boilerplate); city names stay out of it so sibling pages in one city do not share phrases.

    def line(t):
        r = cur[t]
        if not act[t]: return f'No {TL[t].lower()} were listed or sold in {name} between {month_name(first)} and {month_name(last)}.'
        if r is None: return f'{TL[t]} did not appear as a separate line for {name} in {mlabel(last)}.'
        k = kind(r['ratio'])
        return (f'{TL[t]}: {num(r["inventory"])} listed at month end and {num(r["sales"])} sold in {month_name(last)}'
                + ('.' if r['ratio'] is None else f', a sales ratio of {pct(r["ratio"])}' + (f' ({k}).' if k and r['inventory'] >= 10 else '.')))
    if not guide:
        blocks.append({'t': 'h', 'level': 2, 'text': f'{name} homes listed and sold, {span}', 'gen': 'snapstats'})
        blocks.append({'t': 'p', 'text': f'{name}, {mlabel(last)}. ' + line('detached') + ' ' + line('condo_townhome'), 'gen': 'snapstats'})
        tl_ = [t for t in TL if act[t]]; short = {'detached': 'Houses', 'condo_townhome': 'Condos and townhomes'}
        head = ['Month']
        for t in tl_: head += [f'{short[t]} listed', f'{short[t]} sold', f'{short[t]} ratio']
        rows = []
        for m in keys:
            row = [mlabel(m)]
            for t in tl_:
                r_ = dict(S[t])[m]; row += [num(r_['inventory']) if r_ else '—', num(r_['sales']) if r_ else '—', pct(r_['ratio']) if r_ else '—']
            rows.append(row)
        blocks.append({'t': 'table', 'caption': f'{name} listings, sales and sales ratio by month', 'head': head, 'rows': rows, 'source': SRC + RATIO_NOTE, 'gen': 'snapstats'})
        bits = []
        for t in TL:
            hv = have[t]
            if not hv or not act[t]: continue
            sold = sum(r['sales'] or 0 for r in hv); inv = sum(r['inventory'] or 0 for r in hv) / len(hv)
            per = sold / len(hv)
            sent = f'{TL[t]}: {sold} sold over {len(hv)} months against an average of {inv:.1f} listed'
            if per > 0: sent += f', about {inv / per:.1f} months of listings at that pace'
            bits.append(sent)
            top = max(S[t], key=lambda x: (x[1]['sales'] if x[1] else -1))
            if top[1] and top[1]['sales']: bits[-1] += f'; the busiest month was {month_name(top[0])} with {top[1]["sales"]} sold'
        blocks.append({'t': 'p', 'text': 'Looking across the period, ' + '. '.join(bits) + '.', 'gen': 'snapstats'})
    else:
        blocks.append({'t': 'h', 'level': 2, 'text': f'How {name} compares with the rest of its city', 'gen': 'snapstats'})
        blocks.append({'t': 'p', 'text': f'{name} against its whole city, {mlabel(last)}: share of listings and sales, sales ratio and rank.', 'gen': 'snapstats'})
        rows = []; parts = []
        for t in TL:
            r = cur[t]; tot = area[t]['total']
            if not r or not tot['inventory'] or not act[t]: continue
            shareI = 100 * r['inventory'] / tot['inventory']; shareS = (100 * r['sales'] / tot['sales']) if tot['sales'] else None
            elig = sorted([c for c in area[t]['communities'] if (c['inventory'] or 0) >= 10 and c['ratio'] is not None], key=lambda c: -c['ratio'])
            rank = next((i + 1 for i, c in enumerate(elig) if c['name'] == name), None)
            rows.append([TL[t], f'{shareI:.1f}%', f'{shareS:.1f}%' if shareS is not None else '—', f'{pct(r["ratio"])} against {pct(tot["ratio"])}', f'{rank} of {len(elig)}' if rank else 'Under 10 listed'])
            fr = dict(S[t])[first]
            if fr:
                d = r['inventory'] - fr['inventory']
                parts.append(f'{TL[t].lower()}: listings ' + TR.count_move(fr['inventory'], r['inventory'], month_name(first), month_name(last)))
            cum = [(m, x) for m, x in S[t] if x]
            if cum:
                tsales = sum(x['sales'] or 0 for _, x in cum); csales = sum(sum(c['sales'] or 0 for c in months[m]['areas'][ak][t]['communities']) for m, _ in cum)
                if csales: parts[-1] += f', and it took {100 * tsales / csales:.1f}% of the city’s {csales} sales over the period' if parts else ''
        if rows:
            blocks.append({'t': 'table', 'caption': f'{name} against the whole city, {mlabel(last)}', 'head': ['Home type', 'Share of city listings', 'Share of city sales', 'Community sales ratio against city', 'Rank on sales ratio'], 'rows': rows, 'source': SRC + ' Rank counts only communities with at least ten homes listed. Falling listings with steady sales mean homes are being absorbed faster; rising listings with steady sales mean more choice for buyers. A sellers’ best bet is a community where homes sell quickly against the number listed; a buyers’ best bet is the reverse.' + RATIO_NOTE, 'gen': 'snapstats'})
        if parts:
            blocks.append({'t': 'p', 'text': f'Between {mlabel(first)} and {mlabel(last)}, ' + '; '.join(parts) + '.', 'gen': 'snapstats'})
        bb = {t: best_bet(months, ak, t, name) for t in TL}
        sent = []
        for t in TL:
            for key, lab in (('sellers', 'a sellers’ best bet'), ('buyers', 'a buyers’ best bet')):
                if bb[t][key]: sent.append(f'{TL[t].lower()} in {", ".join(month_name(m) for m in bb[t][key])} ({lab})')
        if sent:
            blocks.append({'t': 'p', 'text': f'The monthly write-ups singled out {name} for ' + '; '.join(sent) + '.', 'gen': 'snapstats'})
    return blocks



# ---- city / home-type pages: city-wide cuts of the reports, each cut used on exactly one page per city so sibling pages do not repeat each other
CITY_AREA = {'surrey': 'surrey', 'south-surrey': 'south-surrey-white-rock', 'langley': 'langley', 'abbotsford': 'abbotsford', 'cloverdale': 'cloverdale',
             'maple-ridge': 'maple-ridge', 'pitt-meadows': 'pitt-meadows', 'mission': 'mission', 'north-delta': 'north-delta', 'burnaby': 'burnaby',
             'coquitlam': 'coquitlam', 'new-westminster': 'new-westminster', 'port-coquitlam': 'port-coquitlam', 'port-moody': 'port-moody'}
ROLE_CUTS = {'houses': ['bands_d', 'beds_d'], 'homes': ['metrics_d', 'trend_d'], 'condos': ['bands_c', 'beds_c'], 'townhomes': ['metrics_c', 'trend_c']}
TYPE_LABEL = {'d': ('houses', 'detached'), 'c': ('condos and townhomes', 'condo_townhome')}


def city_cuts(pages):
    """pages: {'houses': slug, ...} existing for one city -> {slug: [cuts]}"""
    out = {}
    det = [r for r in ('houses', 'homes') if r in pages]; con = [r for r in ('condos', 'townhomes') if r in pages]
    dcuts = ROLE_CUTS['houses'] + ROLE_CUTS['homes']; ccuts = ROLE_CUTS['condos'] + ROLE_CUTS['townhomes']
    for r in det: out.setdefault(pages[r], []).extend(ROLE_CUTS[r] if len(det) == 2 else dcuts)
    for r in con: out.setdefault(pages[r], []).extend(ROLE_CUTS[r] if len(con) == 2 else ccuts)
    if not con and 'homes' in pages and not det[:1] == ['houses']: out[pages['homes']] += ['bands_c', 'metrics_c']
    if not con and 'homes' in pages and 'houses' in pages: out[pages['homes']] += ['bands_c', 'metrics_c']
    return out


def trend_labels(last):
    y, m = int(last[:4]), int(last[5:]); out = []
    for i in range(12, -1, -1):
        mm = m - i; yy = y
        while mm <= 0: mm += 12; yy -= 1
        out.append(f'{MN["%02d" % mm]} {yy}')
    return out



def band(label):
    l = label.replace('&', 'and')
    m = re.match(r'^\$?([\d,]+) - ([\d,]+)$', l)
    if m: return f'${m.group(1)} to ${m.group(2)}'
    m = re.match(r'^\$?([\d,]+) and Greater$', l)
    return f'${m.group(1)} and up' if m else l

def build_cut(cut, label, ak, months):
    keys = list(months); last = keys[-1]; area = months[last]['areas'][ak]
    t = 'detached' if cut.endswith('_d') else 'condo_townhome'; tl = TYPE_LABEL['d' if cut.endswith('_d') else 'c'][0]
    x = area[t]; kind_ = cut.split('_')[0]; b = []
    if kind_ == 'bands':
        rows = [r for r in x['price_bands'] if (r['inventory'] or 0) or (r['sales'] or 0)]
        tot = x['total']
        top_s = max(rows, key=lambda r: r['sales'] or 0)
        el = [r for r in rows if (r['inventory'] or 0) >= 10 and r['ratio'] is not None]
        top_r = max(el, key=lambda r: r['ratio']) if el else None
        b.append({'t': 'h', 'level': 2, 'text': f'{label} {tl} by price band, {mlabel(last)}', 'gen': 'snapstats'})
        sent = f'{num(tot["sales"])} {tl} sold in {month_name(last)} against {num(tot["inventory"])} listed. The price band with the most sales was {band(top_s["label"])}, with {top_s["sales"]} sold ({100 * top_s["sales"] / tot["sales"]:.0f}% of the month).' if tot['sales'] else f'{num(tot["inventory"])} {tl} were listed and none sold in {month_name(last)}.'
        if top_r: sent += f' Among bands with at least ten homes listed, the highest sales ratio was {band(top_r["label"])} at {pct(top_r["ratio"])}.'
        b.append({'t': 'p', 'text': sent + '', 'gen': 'snapstats'})
        b.append({'t': 'table', 'caption': f'{label} {tl}: listings and sales by price band, {mlabel(last)}', 'head': ['Price band', 'Listed', 'Sold', 'Sales ratio'], 'rows': [[band(r['label']), num(r['inventory']), num(r['sales']), pct(r['ratio'])] for r in rows], 'source': SRC + ' Bands with nothing listed and nothing sold are left out.' + RATIO_NOTE, 'gen': 'snapstats'})
    elif kind_ == 'beds':
        rows = x['bedrooms']; tot = x['total']
        top = max(rows, key=lambda r: r['sales'] or 0)
        b.append({'t': 'h', 'level': 2, 'text': f'{label} {tl} by bedroom count, {mlabel(last)}', 'gen': 'snapstats'})
        b.append({'t': 'p', 'text': f'Splitting {mlabel(last)} by size, the most sales came from the {top["label"].replace("&", "and").lower()} group, with {top["sales"]} of {num(tot["sales"])} sold, against {num(top["inventory"])} of {num(tot["inventory"])} listed.', 'gen': 'snapstats'})
        b.append({'t': 'table', 'caption': f'{label} {tl}: listings and sales by bedroom count, {mlabel(last)}', 'head': ['Size', 'Listed', 'Sold', 'Sales ratio'], 'rows': [[r['label'].replace('&', 'and'), num(r['inventory']), num(r['sales']), pct(r['ratio'])] for r in rows], 'source': SRC + RATIO_NOTE, 'gen': 'snapstats'})
    elif kind_ == 'metrics':
        rows = []; first = months[keys[0]]['areas'][ak][t]['summary']
        def get(sm, k, which): return sm.get(k, {}).get(which)
        series_ = [(prev_month(keys[0]), 'prev', first)] + [(m, 'cur', months[m]['areas'][ak][t]['summary']) for m in keys]
        for m, w, sm in series_:
            rows.append([mlabel(m), money(get(sm, 'Sale Price', w)), money(get(sm, 'Sale Price SQFT', w)), pct(get(sm, 'Sale to List Price Ratio', w)), f'{get(sm, "Days on Market", w)}', num(get(sm, 'Inventory', w)), num(get(sm, 'Solds', w))])
        lastsm = months[last]['areas'][ak][t]['summary']
        stl = get(lastsm, 'Sale to List Price Ratio', 'cur'); dom0, dom1 = get(first, 'Days on Market', 'prev'), get(lastsm, 'Days on Market', 'cur')
        rel = 'at list price' if stl == 100 else f'about {abs(100 - stl)}% {"above" if stl > 100 else "below"} list price'
        b.append({'t': 'h', 'level': 2, 'text': f'{label} {tl}: sale price, days on market and sale-to-list, {month_name(prev_month(keys[0]))} to {month_name(last)} {last[:4]}', 'gen': 'snapstats'})
        b.append({'t': 'p', 'text': f'In {mlabel(last)} {tl} in {label} sold {rel}, after {dom1} days on market on the reports’ measure ({"down" if dom1 < dom0 else "up" if dom1 > dom0 else "unchanged"} from {dom0} in {month_name(prev_month(keys[0]))}).', 'gen': 'snapstats'})
        b.append({'t': 'table', 'caption': f'{label} {tl}: monthly market figures', 'head': ['Month', 'Reported sale price', 'Per square foot', 'Sale-to-list ratio', 'Days on market', 'Listed', 'Sold'], 'rows': rows, 'source': SRC + PRICE_NOTE, 'gen': 'snapstats'})
    else:  # trend
        tr = x['trend']; labs = trend_labels(last)
        inv, sold, pr = tr['inventory'], tr['solds'], tr['price']
        hi = max(range(13), key=lambda i: inv[i]); lo = min(range(13), key=lambda i: inv[i]); ps = max(range(13), key=lambda i: sold[i])
        chg = 100 * (pr[-1] - pr[0]) / pr[0]
        b.append({'t': 'h', 'level': 2, 'text': f'{label} {tl}: 13 months of listings, sales and prices to {mlabel(last)}', 'gen': 'snapstats'})
        b.append({'t': 'p', 'text': f'Over the 13 months from {labs[0]} to {labs[-1]}, listings of {tl} in {label} peaked at {num(inv[hi])} in {labs[hi]} and bottomed at {num(inv[lo])} in {labs[lo]}. Sales were strongest in {labs[ps]} with {sold[ps]}. The reported sale price moved from {money(pr[0])} to {money(pr[-1])}, a change of {chg:+.1f}%.'.replace('-', '−'), 'gen': 'snapstats'})
        b.append({'t': 'table', 'caption': f'{label} {tl}: 13-month trend', 'head': ['Month', 'Reported sale price', 'Listed', 'Sold'], 'rows': [[labs[i], money(pr[i]), num(inv[i]), num(sold[i])] for i in range(13)], 'source': SRC + PRICE_NOTE, 'gen': 'snapstats'})
    return b


def money(v): return '—' if v is None else '${:,.0f}'.format(v)
def prev_month(m):
    y, mm = int(m[:4]), int(m[5:]) - 1
    if mm == 0: y, mm = y - 1, 12
    return f'{y}-{mm:02d}'


def city_pages(slugs):
    by = {}
    for sl in slugs:
        m = re.match(r'^(.+)-(houses|homes|condos|townhomes)-for-sale$', sl)
        if m and m.group(1) in CITY_AREA: by.setdefault(m.group(1), {})[m.group(2)] = sl
    return by


def main():
    months = load_months(); keys = list(months); last = keys[-1]
    d_last = months[last]
    comm = {}
    for ak, a in d_last['areas'].items():
        for t in TL:
            for c in a[t]['communities']: comm.setdefault(norm(c['name']), set()).add((ak, c['name']))
    n = 0; missing = []; used = set(); mapped = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))):
        slug = os.path.basename(f)[:-5]
        guide = slug.endswith('-guide'); base = slug[:-6] if guide else slug
        hit = ALIAS.get(base)
        if not hit and base in comm:
            cands = sorted(comm[base])
            hit = next((c for c in cands if AMBIG.get(base) == c[0]), None) if len(cands) > 1 else cands[0]
        if not hit: continue
        ak, name = hit
        mapped[slug] = hit; used.add(hit)
        lf = os.path.join(ROOT, 'src/data/local', slug + '.json')
        local = json.load(open(lf, encoding='utf-8')) if os.path.exists(lf) else {'status': 'generated', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
        local['blocks'] = [b for b in local.get('blocks', []) if b.get('gen') != 'snapstats']
        blocks = build(slug, guide, ak, name, months, d_last['areas'][ak]['name'])
        local['blocks'] += blocks or []; local['updated'] = '2026-11-01'
        json.dump(local, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); n += 1
    slugs = [os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))]
    cn = 0
    for city, pg in city_pages(slugs).items():
        ak = CITY_AREA[city]; label = d_last['areas'][ak]['name']
        for slug, cuts in city_cuts(pg).items():
            lf = os.path.join(ROOT, 'src/data/local', slug + '.json')
            local = json.load(open(lf, encoding='utf-8')) if os.path.exists(lf) else {'status': 'generated', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
            local['blocks'] = [b for b in local.get('blocks', []) if b.get('gen') != 'snapstats']
            for c in cuts: local['blocks'] += build_cut(c, label, ak, months)
            local['updated'] = '2026-11-01'
            json.dump(local, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); cn += 1; mapped[slug] = [ak, '+'.join(cuts)]
    print('city/home-type pages updated', cn)
    for lf in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):  # community pages generated by tools/build_community_pages.py
        l = json.load(open(lf, encoding='utf-8'))
        if l.get('community'): used.add((l['community']['area'], l['community']['name'])); mapped[os.path.basename(lf)[:-5]] = [l['community']['area'], l['community']['name']]
    allc = {(ak, c['name']) for ak, a in d_last['areas'].items() for t in TL for c in a[t]['communities']}
    json.dump({'mapped': mapped, 'communities_without_page': sorted(allc - used)}, open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json'), 'w'), indent=1)
    print('updated', n, 'pages;', len(used), 'communities matched;', len(allc - used), 'communities with no page')
    if '--report' in sys.argv:
        for ak, c in sorted(allc - used): print('  no page:', ak, c)


if __name__ == '__main__':
    main()
