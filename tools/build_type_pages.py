"""House pages and condo-and-townhome pages for every community that has enough stock (Jared, 2026-11-01: "Do them for every area as long as
there's enough listings").  Enough = three-month average of at least 5 listed (the same line as the feed gate).

 - <community>-houses-for-sale            detached houses
 - <community>-condos-townhomes-for-sale  condos and townhomes together. The monthly reports publish them as one line, so they cannot be split
                                          until Jared's Paragon export arrives; the page says so. The title says both.
Each page is a new_page local (src/data/local/<slug>.json) built only from the SnapStats(R) figures for that one line, links to the community
page, the city's type page and its neighbours' pages of the same type. Communities that already have a page of that type are skipped.
Pages are rebuilt each run; "hand_edited": true stops a page being overwritten.

    python3 -I tools/build_type_pages.py        (after build_snapstats_layers.py / build_community_pages.py)
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend as TR
import build_snapstats_layers as L
import build_community_pages as C

ROOT = L.ROOT
MIN_AVG = 5
KINDS = {
    'detached': dict(suffix='houses-for-sale', noun='houses', title='Houses for Sale', h1='Houses for Sale', cityrole='houses', cross='condo_townhome', short='Houses'),
    'condo_townhome': dict(suffix='condos-townhomes-for-sale', noun='condos and townhomes', title='Condos & Townhomes for Sale', h1='Condos & Townhomes for Sale', cityrole='condos', cross='detached', short='Condos and townhomes'),
}
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
# existing typed pages use these stems for some communities
STEM_ALIAS = {'Langley City': 'city-of-langley', 'North Surrey': 'north-surrey'}


def title_of(name, city, kind):
    for head in (f'{name}, {city} {kind["title"]}', f'{name} {city} {kind["title"]}', f'{name} {kind["title"]}'):
        for tail in (BR, BS, ''):
            if len(head + tail) <= 66: return head + tail
    return head


def main():
    months = L.load_months(); keys = list(months); last, first = keys[-1], keys[0]; last3 = keys[-3:]
    mn = L.month_name(last)
    mapping = json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped']
    pages = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    locs = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}
    typed_exist = {s for s in pages | set(locs) if re.search(r'-(houses|condos|townhomes|condos-townhomes)-for-sale$', s) and not locs.get(s, {}).get('type_page')}
    # primary page for each community
    prim = {}
    for sl, v in mapping.items():
        if '+' in str(v[1]) or sl.endswith('-guide') or not isinstance(v[1], str): continue
        prim.setdefault((v[0], v[1]), sl)
    for sl, j in locs.items():
        if j.get('community'): prim.setdefault((j['community']['area'], j['community']['name']), sl)
    made, skipped = [], {'thin': 0, 'exists': 0, 'city': 0}
    plan = {}
    d_last = months[last]['areas']
    for (ak, nm), psl in sorted(prim.items()):
        city, cslug = C.CITY[ak]
        if L.norm(nm) in (cslug, L.norm(city)): skipped['city'] += 1; continue
        base = L.norm(C.DISPLAY.get(nm, nm).replace(' (Port Moody)', ''))
        base = base if any(w in base.split('-') for w in cslug.split('-')) else f'{base}-{cslug}'
        for t, kd in KINDS.items():
            ser = L.series(months, ak, t, nm)
            avg = sum((dict(ser)[m] or {}).get('inventory') or 0 for m in last3) / 3
            if avg < MIN_AVG: skipped['thin'] += 1; continue
            stem = STEM_ALIAS.get(nm, L.norm(nm)); alt = [stem, base, L.norm(nm)]
            if not locs.get(f'{base}-{kd["suffix"]}', {}).get('type_page') and (any(f'{a}-{kd["suffix"]}' in typed_exist or (t == 'condo_townhome' and any(f'{a}-{x}-for-sale' in typed_exist for x in ('condos', 'townhomes'))) for a in alt) or f'{L.norm(nm)}-condos-for-sale' in locs):
                skipped['exists'] += 1; continue
            plan[(ak, nm, t)] = (f'{base}-{kd["suffix"]}', psl, avg)
    slugs = {k: v[0] for k, v in plan.items()}
    for (ak, nm, t), (slug, psl, avg) in plan.items():
        kd = KINDS[t]; city, cslug = C.CITY[ak]; disp = C.DISPLAY.get(nm, nm)
        if slug in locs and (locs[slug].get('hand_edited') or not locs[slug].get('type_page')): continue
        S = L.series(months, ak, t, nm); D = dict(S); cur = D[last] or {'inventory': 0, 'sales': 0, 'ratio': None}
        area = d_last[ak]; tot = {m: months[m]['areas'][ak][t]['total'] for m in keys}
        ranked = sorted(((c['inventory'] or 0, c['name']) for c in area[t]['communities']), reverse=True)
        rank = [n for _, n in ranked].index(nm) + 1 if nm in [n for _, n in ranked] else None
        rows = []
        for m, r in S:
            si = '—' if not r or not tot[m]['inventory'] else f'{100 * (r["inventory"] or 0) / tot[m]["inventory"]:.1f}%'
            ss = '—' if not r or not tot[m]['sales'] else f'{100 * (r["sales"] or 0) / tot[m]["sales"]:.1f}%'
            rows.append([L.mlabel(m), L.num(r['inventory']) if r else '—', L.num(r['sales']) if r else '—', L.pct(r['ratio']) if r else '—', si, ss])
        k = L.kind(cur['ratio']) if cur['inventory'] >= 10 and cur['ratio'] is not None else None
        ratio_txt = (L.pct(cur['ratio']) + (f', which the reports’ scale reads as {k}' if k else f' on only {cur["inventory"]} listed, too few to read as a market type')) if cur['ratio'] is not None else 'not published for the month'
        tot_s = sum((r or {}).get('sales') or 0 for _, r in S)
        fr = D[first]; move = ''
        if fr and fr['inventory'] is not None and cur['inventory'] is not None:
            a, b = fr['inventory'], cur['inventory']
            move = f'Listings of {kd["noun"]} in {disp} ' + TR.count_move(a, b, L.month_name(first), mn) + f', and {tot_s} sold across the {len(keys)} months.'
        cross_t = kd['cross']; cx = D if False else dict(L.series(months, ak, cross_t, nm)); cx_cur = cx[last] or {}
        cross_slug = next((s for (a2, n2, t2), (s, _, _) in plan.items() if (a2, n2, t2) == (ak, nm, cross_t)), None)
        bl = [{'t': 'notice', 'text': f'Draft for Jared\'s approval. Built only from the monthly MLS® figures (SnapStats) for {kd["noun"]} in {disp}. No local notes, sold prices, building list or live listing feed yet; see the open items.'}]
        bl.append({'t': 'p', 'text': f'{disp}, {city}: {L.num(cur["inventory"])} {kd["noun"]} listed at the end of {mn} {last[:4]} and {L.num(cur["sales"])} sold in the month, a sales ratio of {ratio_txt}.' + (f' By listings that is number {rank} of {len(ranked)} {city} communities for {kd["noun"]}.' if rank else ''), 'gen': 'typepage'})
        bl.append({'t': 'grid'})
        bl.append({'t': 'h', 'level': 2, 'text': f'{disp} {kd["noun"]} listed and sold, {L.month_name(first)} to {mn} {last[:4]}', 'gen': 'typepage'})
        src = L.SRC + L.RATIO_NOTE + (' The reports count condos and townhomes together in one line, so this table cannot separate the two.' if t == 'condo_townhome' else '') + f' Shares are this community’s count divided by the {city} total for {kd["noun"]} that month.'
        bl.append({'t': 'table', 'caption': f'{disp} {kd["noun"]} by month, with share of {city}', 'head': ['Month', 'Listed', 'Sold', 'Sales ratio', f'Share of {city} listings', f'Share of {city} sales'], 'rows': rows, 'source': src, 'gen': 'typepage'})
        sh = f' In {mn} the community held {100 * cur["inventory"] / tot[last]["inventory"]:.1f}% of {city}’s {L.num(tot[last]["inventory"])} {kd["noun"]} listed.' if tot[last]['inventory'] else ''
        bl.append({'t': 'p', 'text': move + sh, 'gen': 'typepage'})
        if cx_cur and (cx_cur.get('inventory') or cx_cur.get('sales')):
            cnoun = KINDS[cross_t]['noun']
            bl.append({'t': 'h', 'level': 2, 'text': f'{kd["short"]} or {cnoun} in {disp}?', 'gen': 'typepage'})
            link = f' The {disp} {cnoun} page has those figures.' if cross_slug else ''
            bl.append({'t': 'p', 'text': f'{disp} also had {L.num(cx_cur.get("inventory"))} {cnoun} listed and {L.num(cx_cur.get("sales"))} sold in {mn}, against {L.num(cur["inventory"])} {kd["noun"]} listed.' + link, 'gen': 'typepage'})
        pre = C.CITY[ak][1] if ak != 'south-surrey-white-rock' else 'south-surrey'
        exists = lambda s: s in pages or s in locs or s in slugs.values()
        items = []
        def add(sl, text):
            if sl and exists(sl): items.append([{'t': text, 'h': f'/{sl}.html'}])
        add(psl, f'{disp} real estate (all home types)'); add(cross_slug, f'{disp} {KINDS[cross_t]["noun"]} for sale')
        add(f'{pre}-{kd["cityrole"]}-for-sale', f'{city} {kd["cityrole"]} for sale'); add(C.HUB[ak], f'{city} homes for sale'); add(f'{C.MARKET[ak]}-real-estate-market-stats', f'{city} real estate market stats')
        sibs = sorted([n for (a2, n, t2) in plan if a2 == ak and t2 == t]); n_sib = 0
        if nm in sibs:
            i = sibs.index(nm)
            for step in range(1, len(sibs)):
                o = sibs[(i + step) % len(sibs)]
                if n_sib >= 8: break
                add(slugs[(ak, o, t)], f'{C.DISPLAY.get(o, o)} {kd["noun"]} for sale'); n_sib += 1
        bl.append({'t': 'h', 'level': 2, 'text': f'More {city} {kd["noun"]}', 'gen': 'typepage', 'pos': 'end'})
        bl.append({'t': 'list', 'items': items, 'gen': 'typepage', 'pos': 'end'})
        faq = [{'q': f'How many {kd["noun"]} are for sale in {disp}?', 'a': f'At the end of {mn} {last[:4]} the {L.BOARD_NAME[area["board"]]} figures showed {L.num(cur["inventory"])} {kd["noun"]} listed in {disp}. That is a month-end count and it moves daily; ask Jared what is on the market today.'},
               {'q': f'Is {disp} a buyers’ or sellers’ market for {kd["noun"]}?', 'a': f'In {mn} {last[:4]}, {kd["noun"]} in {disp} had a sales ratio of {ratio_txt}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'},
               {'q': f'How many {kd["noun"]} sold in {disp} from {L.month_name(first)} to {mn} {last[:4]}?', 'a': f'{tot_s} {kd["noun"]} sold in {disp} over those {len(keys)} months, out of {L.num(sum(tot[m]["sales"] or 0 for m in keys))} in all of {city}.'}]
        if t == 'condo_townhome': faq.append({'q': 'Do these numbers separate condos from townhomes?', 'a': 'No. The monthly reports publish condos and townhomes as one line, so every count here includes both. Jared can pull the split for a specific building or street.'})
        else: faq.append({'q': f'Does this page include townhomes or duplexes in {disp}?', 'a': 'No. The figures are for detached houses only. Condos and townhomes are counted on their own page.'})
        data = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'type_page': {'area': ak, 'name': nm, 'type': t},
                'new_page': {'title': title_of(disp, city, kd), 'description': f'{disp}, {city} {kd["noun"]} for sale: {L.num(cur["inventory"])} listed in {mn} {last[:4]}, monthly sales and how {disp} compares with {city}. Jared Gibbons, REALTOR®.',
                             'h1': f'{disp} {kd["h1"]} | {city} Real Estate'},
                'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': city, 'href': f'/{C.HUB[ak]}.html'}, {'name': f'{disp} {kd["noun"]}', 'href': f'/{slug}.html'}],
                'faq_heading': f'{disp} {kd["noun"]}: your questions answered', 'blocks': bl, 'faq': faq,
                'needs_from_muse': [f'Sold prices, days on market and sale-to-list ratio for {nm} {kd["noun"]} (the reports give them for {city} as a whole)'] + ([f'Named buildings and complexes in {nm}, strata fee ranges, building ages, rental and pet rules', 'The split between condos and townhomes from the Paragon export'] if t == 'condo_townhome' else [f'Typical lot sizes and ages, and Jared\'s notes on the streets in {nm}']) + ['A live listing feed filtered to this type']}
        if len(data['new_page']['description']) > 158: data['new_page']['description'] = f'{disp}, {city} {kd["noun"]} for sale: listings, sales and sales ratio for {mn} {last[:4]}. Jared Gibbons, REALTOR®.'
        lf = os.path.join(ROOT, 'src/data/local', slug + '.json')
        json.dump(data, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); made.append(slug)
    # each community's own page links to its type pages
    by_prim = {}
    for (ak, nm, t), (slug, psl, avg) in plan.items(): by_prim.setdefault(psl, []).append((t, slug, nm))
    for psl, lst in by_prim.items():
        pf = os.path.join(ROOT, 'src/data/local', psl + '.json')
        if not os.path.exists(pf): continue
        j = json.load(open(pf, encoding='utf-8'))
        if j.get('hand_edited'): continue
        j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'typepage']
        nm = lst[0][2]; disp = C.DISPLAY.get(nm, nm)
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{disp} by home type', 'gen': 'typepage', 'pos': 'end'},
                        {'t': 'list', 'items': [[{'t': f'{disp} {KINDS[t]["noun"]} for sale', 'h': f'/{slug}.html'}] for t, slug, _ in sorted(lst, key=lambda x: x[0] != 'detached')], 'gen': 'typepage', 'pos': 'end'}]
        json.dump(j, open(pf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(pf, 'a').write('\n')
    print('type pages written:', len(made), '| houses', sum(1 for k in plan if k[2] == 'detached'), '| condos+townhomes', sum(1 for k in plan if k[2] == 'condo_townhome'), '| skipped', skipped)


if __name__ == '__main__':
    main()
