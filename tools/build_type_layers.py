"""Data layer for city + home-type pages (condos, townhomes, houses, 55+, penthouses ...), built only from the board's monthly HPI/summary file.

For each archive page whose slug is <area>-<type>-for-sale, this replaces the neighbourhood-guide and FAQ sections that are word-for-word the same on
every sibling page (via the local file's `suppress` list; the archive file is untouched) with sections computed from that month's numbers for that
area and that home type, and adds a matching FAQ. Blocks carry gen 'typelayer' and are rebuilt each run.
    python3 -I tools/build_type_layers.py [--month 2026-09] [--only slug,slug]
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_market as AM

ROOT = AM.ROOT
UPDATED = '2026-11-01'
AREAS = {  # slug prefix -> (board, hpi area, label)
    'surrey': ('fvreb', 'Surrey', 'Surrey'), 'north-surrey': ('fvreb', 'North Surrey', 'North Surrey'), 'cloverdale': ('fvreb', 'Cloverdale', 'Cloverdale'),
    'south-surrey-white-rock': ('fvreb', 'South Surrey & White Rock', 'South Surrey and White Rock'), 'south-surrey': ('fvreb', 'South Surrey & White Rock', 'South Surrey and White Rock'),
    'white-rock': ('fvreb', 'South Surrey & White Rock', 'South Surrey and White Rock'), 'langley': ('fvreb', 'Langley', 'Langley'), 'city-of-langley': ('fvreb', 'Langley', 'Langley'),
    'abbotsford': ('fvreb', 'Abbotsford', 'Abbotsford'), 'mission': ('fvreb', 'Mission', 'Mission'), 'north-delta': ('fvreb', 'North Delta', 'North Delta'),
    'maple-ridge': ('gvr', 'Maple Ridge', 'Maple Ridge'), 'pitt-meadows': ('gvr', 'Pitt Meadows', 'Pitt Meadows'), 'ladner': ('gvr', 'Ladner', 'Ladner'), 'tsawwassen': ('gvr', 'Tsawwassen', 'Tsawwassen'),
    'richmond': ('gvr', 'Richmond', 'Richmond'), 'coquitlam': ('gvr', 'Coquitlam', 'Coquitlam'), 'port-coquitlam': ('gvr', 'Port Coquitlam', 'Port Coquitlam'), 'port-moody': ('gvr', 'Port Moody', 'Port Moody'),
    'new-westminster': ('gvr', 'New Westminster', 'New Westminster'), 'north-vancouver': ('gvr', 'North Vancouver', 'North Vancouver'), 'west-vancouver': ('gvr', 'West Vancouver', 'West Vancouver'),
}
# slug type suffix -> (hpi key, plural phrase, noun)
TYPES = {'condos': ('apartment', 'condos', 'condo'), 'townhomes': ('townhouse', 'townhomes', 'townhome'), 'townhouses': ('townhouse', 'townhouses', 'townhouse'),
         'houses': ('detached', 'houses', 'house'), 'homes': ('detached', 'homes', 'home'), '55-plus-condos': ('apartment', '55+ condos', 'condo'), '55-plus-townhomes': ('townhouse', '55+ townhomes', 'townhome'),
         'penthouses': ('apartment', 'penthouses', 'penthouse'), 'ocean-view-homes': ('detached', 'ocean-view homes', 'home'), 'waterfront-homes': ('detached', 'waterfront homes', 'home')}
money, pc, mv = AM.money, AM.pct, AM.move
AGG = {'Lower Mainland', 'Greater Vancouver', 'Fraser Valley Board'}


def save(f, d): json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')


def parse(slug):
    m = re.match(r'^(.*)-(condos|townhomes|townhouses|houses|homes|55-plus-condos|55-plus-townhomes|penthouses|ocean-view-homes|waterfront-homes)-for-sale$', slug)
    if not m: return None
    pre = m.group(1)
    if pre.startswith('south-surrey-white-rock') and m.group(2) in ('55-plus-condos', '55-plus-townhomes', 'penthouses', 'ocean-view-homes', 'waterfront-homes'): pre = 'south-surrey-white-rock'
    elif m.group(2).endswith('homes') and m.group(2) not in ('homes', 'townhomes', 'ocean-view-homes', 'waterfront-homes', '55-plus-townhomes'): pass
    if pre not in AREAS: return None
    return pre, m.group(2)


def layer(data, when, pre, ty, page_title):
    board, area, label = AREAS[pre]
    hk, plural, noun = TYPES[ty]
    B = data['gvr'] if board == 'gvr' else data['fvreb']
    hpi = B['hpi']; h = hpi[area]
    if hk not in h: return None
    x = h[hk]; c = h['composite']
    reg_key = 'Greater Vancouver' if board == 'gvr' else 'Fraser Valley Board'
    reg = hpi[reg_key].get(hk)
    ranked = sorted([(v[hk]['benchmark'], k) for k, v in hpi.items() if k not in AGG and hk in v], reverse=True)
    pos = [k for _, k in ranked].index(area) + 1
    nb = []
    if pos > 1: nb.append(f'{ranked[pos - 2][1]} above at {money(ranked[pos - 2][0])}')
    if pos < len(ranked): nb.append(f'{ranked[pos][1]} below at {money(ranked[pos][0])}')
    tname = {'apartment': 'apartment', 'townhouse': 'townhouse', 'detached': 'detached home'}[hk]
    art = 'an' if tname[0] in 'aeiou' else 'a'
    blocks = [{'t': 'h', 'level': 2, 'text': f'{label} {plural} {tname} prices, {when}'.replace(f'{plural} {tname}', plural)},
              {'t': 'p', 'text': f'The MLS® Home Price Index benchmark for {art} {tname} in {label} was {money(x["benchmark"])} in {when}. That is {mv(x["chg_1m"])} on the month, {mv(x["chg_3m"])} over three months, {mv(x["chg_6m"])} over six months and {mv(x["chg_1y"])} over the year. Over three years it is {mv(x["chg_3y"])} and over five years {mv(x["chg_5y"])}.'}]
    if reg:
        dif = (x['benchmark'] / reg['benchmark'] - 1) * 100
        blocks.append({'t': 'p', 'text': f'{"The Fraser Valley Board" if board == "fvreb" else "Greater Vancouver"} {tname} benchmark was {money(reg["benchmark"])}, so {label} sits {abs(dif):.1f}% {"above" if dif > 0 else "below"} it. Among the {len(ranked)} areas this board reports, {label} ranks {pos} for {tname} prices' + (', with ' + ' and '.join(nb) if nb else '') + '.'})
    blocks.append({'t': 'table', 'caption': f'{label} {tname} benchmark, {when}', 'head': ['Measure', 'Value'],
                   'rows': [['Benchmark price', money(x['benchmark'])], ['Change in 1 month', pc(x['chg_1m'])], ['Change in 3 months', pc(x['chg_3m'])], ['Change in 6 months', pc(x['chg_6m'])], ['Change in 1 year', pc(x['chg_1y'])], ['Change in 3 years', pc(x['chg_3y'])], ['Change in 5 years', pc(x['chg_5y'])],
                            ['All home types, benchmark', money(c['benchmark'])]],
                   'source': 'Source: ' + B['source'] + '.'})
    summ = {'fvreb': {'North Delta': 'Delta - North', 'Surrey': 'City of Surrey - Combined', 'North Surrey': 'Surrey - North', 'Cloverdale': 'Surrey - Cloverdale', 'South Surrey & White Rock': 'White Rock / South Surrey'}.get(area, area)}.get(board)
    s = data['fvreb']['summary'].get(summ) if board == 'fvreb' and summ else None
    if s and hk in s and 'sales' in s[hk] and 'active' in s[hk] and 'median' in s[hk]:
        t = s[hk]
        blocks.append({'t': 'p', 'text': f'The board counted {t["sales"]["now"]} {tname} sales in {label} in {when}, {mv(t["sales"]["chg_year"])} in sales from a year earlier, with {t["active"]["now"]:,} active listings at month end and a median sale price of {money(t["median"]["now"]) if t["median"]["now"] else "n/a"}.'})
    faq = [{'q': f'How much does a {noun} cost in {label}?', 'a': f'The MLS® benchmark for {art} {tname} in {label} was {money(x["benchmark"])} in {when}, {mv(x["chg_1y"])} from a year earlier.'},
           {'q': f'Are {label} {plural} getting cheaper?', 'a': f'Over three months the {tname} benchmark moved {mv(x["chg_3m"])}, over six months {mv(x["chg_6m"])} and over a year {mv(x["chg_1y"])}.'},
           {'q': f'How do {label} {plural} compare with other areas?', 'a': f'{label} ranks {pos} of {len(ranked)} areas on this board for {tname} prices' + (', with ' + ' and '.join(nb) if nb else '') + '.'}]
    return blocks, faq


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--month', default=None); ap.add_argument('--only', default=''); a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(ROOT, 'src/data/market/[0-9][0-9][0-9][0-9]-[0-9][0-9].json')))
    month = a.month or os.path.basename(files[-1])[:-5]
    data = json.load(open(os.path.join(ROOT, 'src/data/market', month + '.json'), encoding='utf-8'))
    y, m = month.split('-'); when = f'{AM.MONTHS[int(m) - 1]} {y}'
    only = set(a.only.split(',')) if a.only else None
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))):
        pg = json.load(open(f, encoding='utf-8')); slug = pg['slug']
        lf = os.path.join(ROOT, 'src/data/local', slug + '.json')
        loc = json.load(open(lf, encoding='utf-8')) if os.path.exists(lf) else None
        if loc and any(b.get('gen') == 'typelayer' for b in loc['blocks']):  # rebuild from scratch
            loc['blocks'] = [b for b in loc['blocks'] if b.get('gen') != 'typelayer']; loc.pop('faq', None); loc.pop('suppress', None)
            loc.pop('faq_heading', None); loc['_t'] = 1
        p = parse(slug)
        if not p or (only and slug not in only):
            if loc and loc.pop('_t', None): (save(lf, loc) if loc['blocks'] else os.remove(lf))
            continue
        res = layer(data, when, p[0], p[1], pg['title'])
        if not res:
            if loc and loc.pop('_t', None): (save(lf, loc) if loc['blocks'] else os.remove(lf))
            continue
        blocks, faq = res
        sup = [b['text'] for b in pg['blocks'] if b['t'] == 'h' and b['level'] == 2 and (b['text'].endswith('Neighbourhood Guide') or b['text'] == 'Frequently Asked Questions')]
        loc = loc or {'status': 'generated', 'slug': slug, 'updated': UPDATED, 'blocks': []}
        loc.pop('_t', None)
        loc['blocks'] = [dict(b, gen='typelayer') for b in blocks] + loc['blocks']
        loc['faq'] = faq; loc['faq_heading'] = 'Your questions answered'
        loc['suppress'] = sup
        save(lf, loc); n += 1
    print('type layers on', n, 'pages for', month)


if __name__ == '__main__':
    main()
