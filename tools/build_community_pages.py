"""Draft pages for every community in the SnapStats(R) reports that has no page on the site (src/data/snapstats/_mapping.json).

Each page is a new_page local (src/data/local/<slug>.json) built only from the monthly figures: a snapshot table, monthly listings and
sales for houses and for condos and townhomes, the community against its whole city, FAQ answers computed from the same numbers, and
links to the city hub, market-stats page, home-type pages and neighbouring communities. Nothing is claimed that the figures do not show.
Pages are rebuilt on every run. Set "hand_edited": true in a page's JSON to stop a run from overwriting it.

    python3 -I tools/build_snapstats_layers.py      # refreshes the mapping of communities without a page
    python3 -I tools/build_community_pages.py
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend as TR
import build_snapstats_layers as L

ROOT = L.ROOT
CITY = {
    'burnaby': ('Burnaby', 'burnaby'), 'coquitlam': ('Coquitlam', 'coquitlam'), 'new-westminster': ('New Westminster', 'new-westminster'),
    'port-coquitlam': ('Port Coquitlam', 'port-coquitlam'), 'port-moody': ('Port Moody', 'port-moody'), 'pitt-meadows': ('Pitt Meadows', 'pitt-meadows'),
    'maple-ridge': ('Maple Ridge', 'maple-ridge'), 'surrey': ('Surrey', 'surrey'), 'south-surrey-white-rock': ('South Surrey and White Rock', 'south-surrey'),
    'north-delta': ('North Delta', 'north-delta'), 'cloverdale': ('Cloverdale', 'cloverdale'), 'langley': ('Langley', 'langley'),
    'abbotsford': ('Abbotsford', 'abbotsford'), 'mission': ('Mission', 'mission')}
HUB = {'burnaby': 'burnaby-homes-for-sale', 'coquitlam': 'coquitlam-homes-for-sale', 'new-westminster': 'new-westminster-homes-for-sale',
       'port-coquitlam': 'port-coquitlam-homes-for-sale', 'port-moody': 'port-moody-homes-for-sale', 'pitt-meadows': 'pitt-meadows-homes-for-sale',
       'maple-ridge': 'maple-ridge-homes-for-sale', 'surrey': 'surrey-homes-for-sale', 'south-surrey-white-rock': 'south-surrey-homes-for-sale',
       'north-delta': 'north-delta-homes-for-sale', 'cloverdale': 'cloverdale-houses-for-sale', 'langley': 'langley-homes-for-sale',
       'abbotsford': 'abbotsford-homes-for-sale', 'mission': 'mission-homes-for-sale'}
MARKET = {'burnaby': 'burnaby', 'coquitlam': 'coquitlam', 'new-westminster': 'new-westminster', 'port-coquitlam': 'port-coquitlam', 'port-moody': 'port-moody',
          'pitt-meadows': 'pitt-meadows', 'maple-ridge': 'maple-ridge', 'surrey': 'surrey', 'south-surrey-white-rock': 'south-surrey-white-rock',
          'north-delta': 'delta', 'cloverdale': 'cloverdale', 'langley': 'langley', 'abbotsford': 'abbotsford', 'mission': 'mission'}
SELL = {'surrey': 'sell-my-house-in-surrey', 'south-surrey-white-rock': 'sell-my-house-in-south-surrey-white-rock', 'langley': 'sell-my-house-in-langley',
        'abbotsford': 'sell-my-house-in-abbotsford', 'mission': 'sell-my-house-in-mission', 'pitt-meadows': 'sell-my-house-in-pitt-meadows',
        'maple-ridge': 'sell-my-house-in-maple-ridge', 'north-delta': 'sell-my-house-in-delta'}
TYPE_PAGES = [('houses', 'houses for sale'), ('condos', 'condos for sale'), ('townhomes', 'townhomes for sale')]
DISPLAY = {'Simon Fraser University SFU': 'Simon Fraser University Area', 'North Shore': 'North Shore (Port Moody)', 'Central': 'Central'}


def slug_of(name, ak, taken):
    base = L.norm(DISPLAY.get(name, name).replace(' (Port Moody)', ''))
    suffix = CITY[ak][1]
    s = base if any(w in base.split('-') for w in suffix.split('-')) else f'{base}-{suffix}'
    return s if s not in taken else f'{s}-community'


def title_for(name, city):
    # same pattern as the archived area pages ("Edmonds, Burnaby Homes for Sale | Jared Gibbons REALTOR®"), which is also Muse's primary keyword form
    for t in (f'{name}, {city} Homes for Sale | Jared Gibbons REALTOR®', f'{name}, {city} Homes for Sale | Jared Gibbons', f'{name}, {city} Homes for Sale'):
        if len(t) <= 66: return t
    return t


def main():
    months = L.load_months(); keys = list(months); last = keys[-1]; first = keys[0]
    d_last = months[last]
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))
    pages = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    locals_ = {os.path.basename(f)[:-5]: f for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}
    taken = pages | set(locals_)
    # communities that already have a generated page keep their slug
    have = {}
    for sl, f in locals_.items():
        j = json.load(open(f, encoding='utf-8'))
        if j.get('community'): have[(j['community']['area'], j['community']['name'])] = (sl, j)
    todo = [tuple(x) for x in mapping['communities_without_page']] + [k for k in have if tuple(k) not in {tuple(x) for x in mapping['communities_without_page']}]
    exists = lambda s: s in pages or s in locals_
    made = []
    # siblings per city (every community with a page or planned page), in alphabetical order
    sib = {}
    for ak, a in d_last['areas'].items():
        names = sorted({c['name'] for t in L.TL for c in a[t]['communities']})
        sib[ak] = names
    slug_for = {}
    for ak, nm in todo:
        slug_for[(ak, nm)] = have[(ak, nm)][0] if (ak, nm) in have else slug_of(nm, ak, taken)
        taken.add(slug_for[(ak, nm)])
    mp = mapping['mapped']
    for ak, nm in todo:
        slug = slug_for[(ak, nm)]
        if (ak, nm) in have and have[(ak, nm)][1].get('hand_edited'): continue
        city, _ = CITY[ak]; disp = DISPLAY.get(nm, nm)
        S = {t: L.series(months, ak, t, nm) for t in L.TL}
        have_rows = {t: [r for _, r in S[t] if r] for t in L.TL}
        if sum((r['inventory'] or 0) + (r['sales'] or 0) for t in L.TL for r in have_rows[t]) == 0: continue  # nothing to say
        cur = {t: dict(S[t])[last] for t in L.TL}
        act = {t: sum((r['inventory'] or 0) + (r['sales'] or 0) for r in have_rows[t]) > 0 for t in L.TL}
        area = d_last['areas'][ak]
        ncom = len(sib[ak]); board = L.BOARD_NAME[area['board']]
        ih, ic = (cur['detached'] or {}).get('inventory'), (cur['condo_townhome'] or {}).get('inventory')
        sh, sc = (cur['detached'] or {}).get('sales'), (cur['condo_townhome'] or {}).get('sales')
        mo = L.mlabel(last); mn = L.month_name(last)
        blocks = [{'t': 'notice', 'text': f'Draft for Jared\'s approval. Built only from the monthly MLS® figures (SnapStats) for {disp}. It has no local notes, street boundaries, schools or listing feed yet; see the open items below.'}]
        blocks.append({'t': 'p', 'text': f'{disp}, {city}: {L.num(ih)} houses and {L.num(ic)} condos and townhomes listed at the end of {mn}, with {L.num(sh)} and {L.num(sc)} sold in the month. It is one of {ncom} communities the {board} figures break out for {city}.', 'gen': 'community'})
        blocks.append({'t': 'grid'})  # listing feed slot, same as the archived area pages; the preview shows the not-connected notice
        blocks += L.build(slug, False, ak, nm, months, area['name']) or []
        blocks += L.build(slug, True, ak, nm, months, area['name']) or []
        # --- monthly share of the city (decimals make this the most community-specific table on the page)
        def mshare(m, t, key):
            r = dict(S[t])[m]; tot = months[m]['areas'][ak][t]['total']
            return None if (not r or not tot[key]) else 100 * (r[key] or 0) / tot[key]
        sr = []; tl_ = [t for t in L.TL if act[t]]; nm_ = {'detached': 'houses', 'condo_townhome': 'condos and townhomes'}
        for m in keys:
            row = [L.mlabel(m)]
            for t in tl_:
                for key in ('inventory', 'sales'):
                    v = mshare(m, t, key); row.append('—' if v is None else f'{v:.1f}%')
            sr.append(row)
        blocks.append({'t': 'h', 'level': 2, 'text': f'{disp} share of {city} listings and sales by month', 'gen': 'community'})
        fi, li = mshare(first, 'detached', 'inventory'), mshare(last, 'detached', 'inventory'); fc, lc = mshare(first, 'condo_townhome', 'inventory'), mshare(last, 'condo_townhome', 'inventory')
        sent = []
        if act['detached'] and fi is not None and li is not None: sent.append(f'its share of the houses listed in {city} went from {fi:.1f}% in {L.month_name(first)} to {li:.1f}% in {mn}')
        if act['condo_townhome'] and fc is not None and lc is not None: sent.append(f'its share of the condos and townhomes listed went from {fc:.1f}% to {lc:.1f}%')
        blocks.append({'t': 'p', 'text': f'In {disp}, ' + ' and '.join(sent) + '. A share that holds steady while the city moves means the community is following the city; a share that drifts means it is moving differently.' if sent else f'{disp} did not appear in the {city} figures for every month.', 'gen': 'community'})
        blocks.append({'t': 'table', 'caption': f'{disp} as a share of {city}, by month', 'head': ['Month'] + [f'Share of city {nm_[t]} {w}' for t in tl_ for w in ('listed', 'sold')], 'rows': sr, 'source': L.SRC + ' Shares are the community’s count divided by the city total for the same month and home type.', 'gen': 'community'})
        # --- links
        items = []
        def add(sl, text):
            if exists(sl) or sl in slug_for.values(): items.append([{'t': text, 'h': f'/{sl}.html'}])
        add(HUB[ak], f'{city} homes for sale')
        add(f'{MARKET[ak]}-real-estate-market-stats', f'{city} real estate market stats')
        pre = CITY[ak][1] if ak not in ('south-surrey-white-rock',) else 'south-surrey'
        for role, label in TYPE_PAGES: add(f'{pre}-{role}-for-sale', f'{city} {label}')
        if ak in SELL: add(SELL[ak], f'Sell my house in {city}')
        add(f'schools-in-{CITY[ak][1]}-bc', f'Schools in {city}')
        names = sib[ak]; i = names.index(nm); n_sib = 0
        for k in range(1, len(names)):
            o = names[(i + k) % len(names)]
            osl = slug_for.get((ak, o)) or next((sl for sl, v in mp.items() if v[0] == ak and v[1] == o and not sl.endswith('-guide') and '_' not in str(v[1])), None)
            if osl and n_sib < 10 and (exists(osl) or osl in slug_for.values()): items.append([{'t': f'{DISPLAY.get(o, o)} real estate', 'h': f'/{osl}.html'}]); n_sib += 1
        blocks.append({'t': 'h', 'level': 2, 'text': f'More {city} real estate', 'gen': 'community', 'pos': 'end'})
        blocks.append({'t': 'list', 'items': items, 'gen': 'community', 'pos': 'end'})
        # --- FAQ, all computed
        faq = []
        parts = [f'{L.num(ih)} houses' if ih is not None and act['detached'] else None, f'{L.num(ic)} condos and townhomes' if ic is not None and act['condo_townhome'] else None]
        faq.append({'q': f'How many homes are for sale in {disp}?', 'a': f'At the end of {mn} {last[:4]} the {board} figures showed ' + ' and '.join(x for x in parts if x) + f' listed in {disp}. Those are month-end counts and they move daily, so ask Jared for a current list.'})
        r = cur['detached']; r2 = cur['condo_townhome']
        def kd(rr):
            if not rr or rr['ratio'] is None: return None
            return f'{L.pct(rr["ratio"])} ({L.kind(rr["ratio"])})' if rr['inventory'] >= 10 else f'{L.pct(rr["ratio"])} on only {rr["inventory"]} listed, too few to read as a market type'
        bits = []
        if kd(r) and act['detached']: bits.append(f'houses had a sales ratio of {kd(r)}')
        if kd(r2) and act['condo_townhome']: bits.append(f'condos and townhomes had {kd(r2)}')
        if bits: faq.append({'q': f'Is {disp} a buyers’ or sellers’ market?', 'a': f'In {mn} {last[:4]}, ' + '; '.join(bits) + '. The sales ratio is homes sold divided by homes listed; on the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers. One month in one community is a small sample, so look at the monthly table above before you decide.'})
        tot_s = {t: sum(x['sales'] or 0 for x in have_rows[t]) for t in L.TL}
        busiest = []
        for t in L.TL:
            if have_rows[t]:
                top = max(S[t], key=lambda x: (x[1]['sales'] if x[1] else -1))
                if top[1] and top[1]['sales']: busiest.append(f'{L.TL[t].lower()} peaked in {L.month_name(top[0])} with {top[1]["sales"]} sold')
        faq.append({'q': f'How many homes sold in {disp} from {L.month_name(first)} to {mn} {last[:4]}?', 'a': f'{tot_s["detached"]} houses and {tot_s["condo_townhome"]} condos and townhomes sold in {disp} over those {len(keys)} months' + (f'; ' + ' and '.join(busiest) if busiest else '') + '.'})
        shares = []
        for t in L.TL:
            rr = cur[t]; tot = area[t]['total']
            if act[t] and rr and tot['inventory']: shares.append(f'{100 * rr["inventory"] / tot["inventory"]:.1f}% of the {L.num(tot["inventory"])} {L.TL[t].lower()} listed in {city}')
        if shares: faq.append({'q': f'How big is {disp} compared with the rest of {city}?', 'a': f'In {mn} {last[:4]}, {disp} held ' + ' and ' .join(shares) + '.'})
        mix = []
        if act['detached'] and act['condo_townhome'] and (ih + ic):
            mix.append(f'In {mn} {last[:4]}, houses made up {100 * ih / (ih + ic):.1f}% of the {L.num(ih + ic)} homes listed in {disp} and condos and townhomes made up {100 * ic / (ih + ic):.1f}%')
            if (sh + sc): mix[-1] += f'; of the {L.num(sh + sc)} that sold, houses were {100 * sh / (sh + sc):.1f}% and condos and townhomes {100 * sc / (sh + sc):.1f}%'
            faq.append({'q': f'What mix of houses and condos is for sale in {disp}?', 'a': mix[0] + '.'})
        ch = []
        for t in L.TL:
            fr = dict(S[t])[first]; cu = cur[t]
            if act[t] and fr and cu and fr['inventory']: ch.append(f'{L.TL[t].lower()} ' + TR.count_move(fr['inventory'], cu['inventory'], L.month_name(first), mo))
        if ch: faq.append({'q': f'Are there more or fewer homes for sale in {disp} than in {L.month_name(first)}?', 'a': f'Listings of ' + '; '.join(ch) + '.'})
        data = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01',
                'community': {'area': ak, 'name': nm},
                'new_page': {'title': title_for(disp, city), 'description': '', 'h1': f'{disp}, {city} Homes for Sale'},
                'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': city, 'href': f'/{HUB[ak]}.html'}, {'name': f'{disp} real estate', 'href': f'/{slug}.html'}],
                'faq_heading': f'{disp} real estate: your questions answered', 'blocks': blocks, 'faq': faq,
                'needs_from_muse': [f'Street boundaries of {nm} from the Paragon sub-area map, and its neighbouring communities',
                                    f'Sold prices, days on market and sale-to-list ratio for {nm} itself (the reports give them for {city} as a whole, not per community)',
                                    f'Schools for {nm}, placed by street address', f'Jared\'s own notes on {nm}: housing stock, who buys here, what to watch', f'A live listing feed for {nm}']}
        desc_bits = []
        if ih is not None: desc_bits.append(f'{L.num(ih)} houses')
        if ic is not None: desc_bits.append(f'{L.num(ic)} condos and townhomes')
        desc = f'{disp}, {city} homes for sale: ' + ' and '.join(desc_bits) + f' listed in {mn} {last[:4]}, monthly sales, and how it compares with {city}. Jared Gibbons, REALTOR®.'
        if len(desc) > 158: desc = f'{disp}, {city} homes for sale: listings, sales and sales ratio for {mn} {last[:4]} and how it compares with {city}. Jared Gibbons, REALTOR®.'
        if len(desc) > 158: desc = f'{disp}, {city} homes for sale and market figures for {mn} {last[:4]}. Jared Gibbons, REALTOR®.'
        data['new_page']['description'] = desc
        lf = os.path.join(ROOT, 'src/data/local', slug + '.json')
        json.dump(data, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); made.append(slug)
    print('community pages written:', len(made))


if __name__ == '__main__':
    main()
