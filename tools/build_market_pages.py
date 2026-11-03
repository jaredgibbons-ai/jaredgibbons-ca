"""City market-stats pages, one per city, rebuilt in full each month from src/data/market/<month>.json (board HPI; FVREB summary where it has counts).

Every sentence is computed from the month's numbers, so each page is different and nothing is estimated. Pages are 'generated' status new pages
(slug <city>-real-estate-market-stats) and a link block (gen 'marketlink') is added to each city's hub pages.
    python3 -I tools/build_market_pages.py [--month 2026-09]
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_market as AM

ROOT = AM.ROOT
UPDATED = '2026-11-01'
# slug, display, [(board, hpi area, label, fvreb summary key)], hubs that get a link, sibling links (slug, text)
CITIES = [
    ('surrey', 'Surrey', [('fvreb', 'Surrey', 'Surrey (board area)', 'City of Surrey - Combined'), ('fvreb', 'North Surrey', 'North Surrey', 'Surrey - North'), ('fvreb', 'Cloverdale', 'Cloverdale', 'Surrey - Cloverdale', 'summary')], ['surrey-homes-for-sale', 'surrey-neighbourhood-guides', 'surrey-townhomes-for-sale', 'surrey-condos-for-sale']),
    ('south-surrey-white-rock', 'South Surrey and White Rock', [('fvreb', 'South Surrey & White Rock', 'South Surrey and White Rock', 'White Rock / South Surrey')], ['south-surrey-homes-for-sale', 'white-rock', 'south-surrey-townhomes-for-sale']),
    ('langley', 'Langley', [('fvreb', 'Langley', 'Langley', 'Langley')], ['langley-homes-for-sale', 'langley-neighbourhood-guides']),
    ('abbotsford', 'Abbotsford', [('fvreb', 'Abbotsford', 'Abbotsford', 'Abbotsford')], ['abbotsford-homes-for-sale', 'abbotsford-neighbourhood-guides']),
    ('mission', 'Mission', [('fvreb', 'Mission', 'Mission', 'Mission')], ['mission-homes-for-sale', 'mission-neighbourhood-guides']),
    ('cloverdale', 'Cloverdale', [('fvreb', 'Cloverdale', 'Cloverdale', 'Surrey - Cloverdale')], ['cloverdale-neighbourhood-guides', 'cloverdale-townhomes-for-sale']),
    ('delta', 'Delta', [('gvr', 'Tsawwassen', 'Tsawwassen', None, 'summary'), ('gvr', 'Ladner', 'Ladner', None, 'summary'), ('fvreb', 'North Delta', 'North Delta', 'Delta - North')], ['delta-homes-for-sale', 'delta-neighbourhood-guides']),
    ('tsawwassen', 'Tsawwassen', [('gvr', 'Tsawwassen', 'Tsawwassen', None)], ['tsawwassen-homes-for-sale', 'tsawwassen-townhomes-for-sale']),
    ('ladner', 'Ladner', [('gvr', 'Ladner', 'Ladner', None)], ['ladner-homes-for-sale', 'ladner-townhomes-for-sale']),
    ('maple-ridge', 'Maple Ridge', [('gvr', 'Maple Ridge', 'Maple Ridge', None)], ['maple-ridge-homes-for-sale', 'maple-ridge-neighbourhood-guides']),
    ('pitt-meadows', 'Pitt Meadows', [('gvr', 'Pitt Meadows', 'Pitt Meadows', None)], ['pitt-meadows-homes-for-sale', 'pitt-meadows-neighbourhood-guides']),
    ('burnaby', 'Burnaby', [('gvr', 'Burnaby East', 'Burnaby East', None), ('gvr', 'Burnaby North', 'Burnaby North', None), ('gvr', 'Burnaby South', 'Burnaby South', None)], ['burnaby-homes-for-sale']),
    ('richmond', 'Richmond', [('gvr', 'Richmond', 'Richmond', None)], ['richmond-homes-for-sale']),
    ('coquitlam', 'Coquitlam', [('gvr', 'Coquitlam', 'Coquitlam', None)], ['coquitlam-homes-for-sale']),
    ('port-coquitlam', 'Port Coquitlam', [('gvr', 'Port Coquitlam', 'Port Coquitlam', None)], ['port-coquitlam-homes-for-sale']),
    ('port-moody', 'Port Moody', [('gvr', 'Port Moody', 'Port Moody', None)], ['port-moody-homes-for-sale']),
    ('new-westminster', 'New Westminster', [('gvr', 'New Westminster', 'New Westminster', None)], ['new-westminster-homes-for-sale']),
    ('north-vancouver', 'North Vancouver', [('gvr', 'North Vancouver', 'North Vancouver', None)], ['north-vancouver-homes-for-sale']),
    ('west-vancouver', 'West Vancouver', [('gvr', 'West Vancouver', 'West Vancouver', None)], ['west-vancouver-homes-for-sale']),
    ('vancouver', 'Vancouver', [('gvr', 'Vancouver East', 'Vancouver East', None), ('gvr', 'Vancouver West', 'Vancouver West', None)], ['vancouver-homes-for-sale']),
    ('squamish', 'Squamish', [('gvr', 'Squamish', 'Squamish', None)], ['squamish-homes-for-sale']),
    ('whistler', 'Whistler', [('gvr', 'Whistler', 'Whistler', None)], ['whistler-homes-for-sale']),
]
SUMMARY_LINK = {'Cloverdale': 'cloverdale-real-estate-market-stats', 'Tsawwassen': 'tsawwassen-real-estate-market-stats', 'Ladner': 'ladner-real-estate-market-stats'}
TY = [('composite', 'all home types', 'All home types'), ('detached', 'a detached home', 'Detached'), ('townhouse', 'a townhouse', 'Townhouse'), ('apartment', 'an apartment', 'Apartment')]
money = AM.money
def pc(v): return AM.pct(v)
def mv(v): return AM.move(v)
def save(f, d): json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')


def regional(data, board):
    h = data['gvr']['hpi'] if board == 'gvr' else data['fvreb']['hpi']
    return ('Greater Vancouver', h['Greater Vancouver']) if board == 'gvr' else ('the Fraser Valley Board area', h['Fraser Valley Board'])


def area_blocks(data, month, board, area, label, summ_key, when):
    hpi = (data['gvr'] if board == 'gvr' else data['fvreb'])['hpi'][area]
    src = data['gvr']['source'] if board == 'gvr' else data['fvreb']['source']
    reg_name, reg = regional(data, board)
    out = [{'t': 'h', 'level': 2, 'text': f'{label} benchmark prices and trends, {when}'}]
    c = hpi['composite']
    ps = []
    mov = sorted([(hpi[k]['chg_1y'], lab) for k, lab, _ in TY[1:] if k in hpi], key=lambda x: x[0])
    ps.append(f'A typical {label} home carried an MLS® Home Price Index benchmark of {money(c["benchmark"])} in {when}. That is {mv(c["chg_1m"])} on the month, {mv(c["chg_3m"])} over three months, {mv(c["chg_6m"])} over six months and {mv(c["chg_1y"])} over the year. '
              f'Over three years it is {mv(c["chg_3y"])}, and over five years {mv(c["chg_5y"])}.')
    lo, hi = mov[0], mov[-1]
    ps.append(f'The weakest one-year move in {label} was for {lo[1].lower()} homes at {pc(lo[0])}; the strongest was {hi[1].lower()} at {pc(hi[0])}.')
    d = hpi['detached']; a = hpi['apartment']; t = hpi.get('townhouse')
    gap = d['benchmark'] - a['benchmark']
    if not t:
        ps.append(f'The board reports no townhouse benchmark for {label}. The gap between a detached home ({money(d["benchmark"])}) and an apartment ({money(a["benchmark"])}) is {money(gap)}.')
    else:
        side = 'above' if t['benchmark'] >= a['benchmark'] else 'below'
        ps.append(f'The gap between a detached home ({money(d["benchmark"])}) and an apartment ({money(a["benchmark"])}) is {money(gap)}, and a townhouse ({money(t["benchmark"])}) sits {money(abs(t["benchmark"] - a["benchmark"]))} {side} the apartment benchmark.')
    rc = reg['composite']
    rel = (c['benchmark'] / rc['benchmark'] - 1) * 100
    ps.append(f'Against {reg_name}, where the all-home benchmark was {money(rc["benchmark"])}, {label} is {abs(rel):.1f}% {"above" if rel > 0 else "below"}. '
              f'Over the year {reg_name} moved {mv(rc["chg_1y"])} against {mv(c["chg_1y"])} here.')
    board_h = (data['gvr'] if board == 'gvr' else data['fvreb'])['hpi']
    AGG = {'Lower Mainland', 'Greater Vancouver', 'Fraser Valley Board'}
    ranked = sorted([(v['composite']['benchmark'], k) for k, v in board_h.items() if k not in AGG and 'composite' in v], reverse=True)
    pos = [k for _, k in ranked].index(area) + 1
    nb = []
    if pos > 1: nb.append(f'{ranked[pos - 2][1]} above it at {money(ranked[pos - 2][0])}')
    if pos < len(ranked): nb.append(f'{ranked[pos][1]} below it at {money(ranked[pos][0])}')
    ps.append(f'Of the {len(ranked)} areas this board reports, {label} ranks {pos} by all-home benchmark' + (', with ' + ' and '.join(nb) if nb else '') + '.')
    out += [{'t': 'p', 'text': t_} for t_ in ps]
    for k, lab, _ in TY[1:]:
        if k not in hpi: continue
        h_ = hpi[k]; r_ = reg.get(k)
        txt = (f'{_} homes in {label}: benchmark {money(h_["benchmark"])}, {mv(h_["chg_1m"])} in a month, {mv(h_["chg_3m"])} in three months, {mv(h_["chg_6m"])} in six months, {mv(h_["chg_1y"])} in a year, {mv(h_["chg_3y"])} in three years and {mv(h_["chg_5y"])} in five.')
        if r_:
            dif = (h_['benchmark'] / r_['benchmark'] - 1) * 100
            txt += f' That is {abs(dif):.1f}% {"above" if dif > 0 else "below"} the {_.lower()} benchmark for {reg_name} ({money(r_["benchmark"])}).'
        out.append({'t': 'p', 'text': txt})
    head = ['Home type', 'Benchmark price', '1 month', '3 months', '6 months', '1 year', '3 years', '5 years']
    rows = [[lab, money(hpi[k]['benchmark']), pc(hpi[k]['chg_1m']), pc(hpi[k]['chg_3m']), pc(hpi[k]['chg_6m']), pc(hpi[k]['chg_1y']), pc(hpi[k]['chg_3y']), pc(hpi[k]['chg_5y'])] for k, _, lab in TY if k in hpi]
    out.append({'t': 'table', 'caption': f'{label} MLS® benchmark prices and changes, {when}', 'head': head, 'rows': rows, 'source': 'Source: ' + src + '.'})
    summ = data['fvreb']['summary'].get(summ_key) if (board == 'fvreb' and summ_key) else None
    if summ:
        r2 = []
        for k, lab, _ in [(k, l, x) for k, l, x in TY[1:]]:
            s = summ.get(k, {})
            if 'sales' in s and 'active' in s and 'median' in s:
                r2.append([_, str(s['sales']['now']), '{:,}'.format(s['active']['now']), money(s['median']['now']) if s['median']['now'] else 'n/a', pc(s['sales']['chg_year'])])
        if r2:
            tot = sum(int(r[1]) for r in r2)
            out.append({'t': 'p', 'text': f'The board counted {tot} detached, townhouse and apartment sales in {label} in {when}, against active listings of ' + ', '.join(f'{r[2]} {r[0].lower()}' for r in r2) + ' at month end.'})
            out.append({'t': 'table', 'caption': f'{label} MLS® sales activity, {when}', 'head': ['Home type', 'Sales', 'Active listings', 'Median sale price', 'Sales vs a year ago'], 'rows': r2, 'source': 'Source: ' + src + '.'})
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--month', default=None); a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, 'src/data/market/[0-9][0-9][0-9][0-9]-[0-9][0-9].json')))
    month = a.month or os.path.basename(files[-1])[:-5]
    data = json.load(open(os.path.join(ROOT, 'src/data/market', month + '.json'), encoding='utf-8'))
    y, m = month.split('-'); when = f'{AM.MONTHS[int(m) - 1]} {y}'
    # remove old generated links
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if any(b.get('gen') == 'marketlink' for b in d.get('blocks', [])):
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'marketlink']
            if not d['blocks'] and d.get('status') == 'generated': os.remove(f); continue
            save(f, d)
    n = 0
    for slug, disp, areas, hubs in CITIES:
        page = f'{slug}-real-estate-market-stats'
        blocks = []
        first = areas[0]
        hpi0 = (data['gvr'] if first[0] == 'gvr' else data['fvreb'])['hpi'][first[1]]
        for board, area, label, sk, *rest in areas:
            if rest and rest[0] == 'summary':
                hp_ = (data['gvr'] if board == 'gvr' else data['fvreb'])['hpi'][area]; cc = hp_['composite']
                blocks += [{'t': 'h', 'level': 2, 'text': f'{label} at a glance, {when}'}, {'t': 'p', 'text': f'{label} had an all-home benchmark of {money(cc["benchmark"])} ({mv(cc["chg_1y"])} over the year), with detached at {money(hp_["detached"]["benchmark"])}, townhouses at {money(hp_["townhouse"]["benchmark"]) if "townhouse" in hp_ else "n/a"} and apartments at {money(hp_["apartment"]["benchmark"])}.'}, {'t': 'p', 'text': f'{label} market stats in full', 'h': f'/{SUMMARY_LINK[label]}.html'}]
            else:
                blocks += area_blocks(data, month, board, area, label, sk, when)
        if len(areas) > 1:
            names = ' and '.join([', '.join(x[2] for x in areas[:-1]), areas[-1][2]]) if len(areas) > 2 else f'{areas[0][2]} and {areas[1][2]}'
            hp = [(x[2], (data['gvr'] if x[0] == 'gvr' else data['fvreb'])['hpi'][x[1]]['composite']) for x in areas]
            top = max(hp, key=lambda x: x[1]['benchmark']); low = min(hp, key=lambda x: x[1]['benchmark'])
            blocks.insert(0, {'t': 'p', 'text': f'The boards report {disp} in {len(areas)} parts: {names}. In {when}, {top[0]} had the highest all-home benchmark at {money(top[1]["benchmark"])} and {low[0]} the lowest at {money(low[1]["benchmark"])}, a gap of {money(top[1]["benchmark"] - low[1]["benchmark"])}. Over twelve months the three-part spread runs ' + ', '.join(f'{n_} {mv(c_["chg_1y"])}' for n_, c_ in hp) + '.'})
        else:
            c = hpi0['composite']
            blocks.insert(0, {'t': 'p', 'text': f'This page tracks the {disp} MLS® Home Price Index benchmark for {when}: {money(c["benchmark"])} for a typical home, {mv(c["chg_1y"])} over twelve months.'})
        board_name = 'Greater Vancouver REALTORS®' if first[0] == 'gvr' else 'Fraser Valley Real Estate Board'
        blocks.append({'t': 'h', 'level': 2, 'text': f'What the {disp} figure is'})
        cc = hpi0['composite']
        blocks.append({'t': 'p', 'text': f'The {money(cc["benchmark"])} {first[2]} figure is a modelled price for a typical home, not a median, and it comes from {board_name} for {when}.'})
        sell = os.path.exists(os.path.join(ROOT, f'src/data/local/sell-my-house-in-{slug}.json')) and slug not in ('cloverdale', 'tsawwassen', 'ladner')
        sell_slug = {'delta': 'sell-my-house-in-delta', 'tsawwassen': 'sell-my-house-in-delta', 'ladner': 'sell-my-house-in-delta', 'south-surrey-white-rock': 'sell-my-house-in-south-surrey-white-rock'}.get(slug, f'sell-my-house-in-{slug}')
        if os.path.exists(os.path.join(ROOT, f'src/data/local/{sell_slug}.json')):
            blocks.append({'t': 'p', 'text': f'Selling in {disp}? See the rules and prices that matter to a seller', 'h': f'/{sell_slug}.html'})
        blocks.append({'t': 'p', 'text': f'Request your free home evaluation', 'h': '/home-evaluation.html'})
        for h in hubs[:2]:
            if os.path.exists(os.path.join(ROOT, f'src/data/pages/{h}.json')):
                nm = ''.join(w.capitalize() + ' ' for w in h.replace('-', ' ').split()).strip()
                blocks.append({'t': 'p', 'text': nm, 'h': f'/{h}.html'})
        c = hpi0['composite']
        faq = [{'q': f'What is the benchmark price of a home in {disp}?', 'a': ' '.join(f'In {when}, a typical {x[2]} home was {money((data["gvr"] if x[0] == "gvr" else data["fvreb"])["hpi"][x[1]]["composite"]["benchmark"])}, with detached at {money((data["gvr"] if x[0] == "gvr" else data["fvreb"])["hpi"][x[1]]["detached"]["benchmark"])}.' for x in areas)},
               {'q': f'Are {disp} home prices rising or falling?', 'a': ' '.join(f'{x[2]} is {mv((data["gvr"] if x[0] == "gvr" else data["fvreb"])["hpi"][x[1]]["composite"]["chg_1y"])} over twelve months and {mv((data["gvr"] if x[0] == "gvr" else data["fvreb"])["hpi"][x[1]]["composite"]["chg_3m"])} over three months.' for x in areas)},
               ]
        title = next(x for x in (f'{disp} Real Estate Market Stats {when} | Jared Gibbons', f'{disp} Market Stats {when} | Jared Gibbons', f'{disp} Market Stats {when}') if len(x) <= 66 or x.count('|') == 0 and len(x) <= 80)
        desc = f'{disp} MLS® benchmark prices for {when}: {money(c["benchmark"])} for a typical {first[2]} home, {mv(c["chg_1y"])} in a year, with detached, townhouse and apartment trends.'[:158]
        d = {'status': 'generated', 'slug': page, 'updated': UPDATED, 'new_page': {'title': title, 'description': desc, 'h1': f'{disp} Real Estate Market Stats, {when}'},
             'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': f'{disp} market stats', 'href': f'/{page}.html'}],
             'faq_heading': f'{disp} market stats: your questions answered', 'blocks': blocks, 'faq': faq}
        save(os.path.join(ROOT, f'src/data/local/{page}.json'), d); n += 1
        for h in hubs:
            if not os.path.exists(os.path.join(ROOT, f'src/data/pages/{h}.json')): continue
            f = os.path.join(ROOT, f'src/data/local/{h}.json')
            dd = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {'status': 'generated', 'slug': h, 'updated': UPDATED, 'blocks': []}
            dd['blocks'].append({'t': 'p', 'text': f'{disp} real estate market stats for {when}: benchmark prices and trends', 'h': f'/{page}.html', 'gen': 'marketlink'}); save(f, dd)
    print('built', n, 'market stats pages for', month)


if __name__ == '__main__':
    main()
