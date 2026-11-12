"""Condo-only pages for communities whose main page is the houses page (Jared, 2026-11-01: "Brentwood, Cariboo and Edmonds should have their own").

Each page is a new_page local (src/data/local/<slug>.json) built only from the monthly SnapStats(R) figures for the
"Condos and townhomes" line of one Burnaby community. The reports combine condos and townhomes in one line, so the page says so.
The existing community page keeps the houses; both pages link to each other.   python3 -I tools/build_condo_pages.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trend as TR
import build_snapstats_layers as L

ROOT = L.ROOT
AK, CITY, T = 'burnaby', 'Burnaby', 'condo_townhome'
# (houses-page slug, community name in the report, new condo slug, display name)
PAGES = [('cariboo', 'Cariboo', 'cariboo-condos-for-sale', 'Cariboo'),
         ('edmonds-be', 'Edmonds', 'edmonds-condos-for-sale', 'Edmonds')]
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'


def title(name):
    head = f'{name} Burnaby Condos for Sale'
    return head + BR if len(head + BR) <= 66 else head + BS


def main():
    months = L.load_months(); keys = list(months); last, first = keys[-1], keys[0]
    mn, mo = L.month_name(last), L.mlabel(last)
    d = months[last]['areas'][AK]
    allc = sorted({c['name'] for t in L.TL for c in d[t]['communities']})
    ranked = sorted(((c['inventory'] or 0, c['name']) for c in d[T]['communities']), reverse=True)
    tot = {m: months[m]['areas'][AK][T]['total'] for m in keys}
    for houses_slug, name, slug, disp in PAGES:
        S = L.series(months, AK, T, name); H = dict(L.series(months, AK, 'detached', name))
        cur = dict(S)[last]; hc = H[last] or {}
        rank = [n for _, n in ranked].index(name) + 1
        rows = []
        for m, r in S:
            sh_i = '—' if not r or not tot[m]['inventory'] else f'{100 * (r["inventory"] or 0) / tot[m]["inventory"]:.1f}%'
            sh_s = '—' if not r or not tot[m]['sales'] else f'{100 * (r["sales"] or 0) / tot[m]["sales"]:.1f}%'
            rows.append([L.mlabel(m), L.num(r['inventory']) if r else '—', L.num(r['sales']) if r else '—', L.pct(r['ratio']) if r else '—', sh_i, sh_s])
        k = L.kind(cur['ratio']) if cur and cur['inventory'] >= 10 else None
        first_r = dict(S)[first]
        move = ''
        if first_r and cur:
            a, b = first_r['inventory'], cur['inventory']
            move = f'Condo and townhome listings in {disp} ' + TR.count_move(a, b, L.month_name(first), mn) + f', while {L.num(sum((r["sales"] or 0) for _, r in S if r))} sold across the {len(keys)} months.'
        ratio_txt = f'{L.pct(cur["ratio"])}' + (f', which the reports’ scale reads as {k}' if k else f' on only {cur["inventory"]} listed, too few to read as a market type')
        bl = [{'t': 'notice', 'text': f'Draft for Jared\'s approval. Built only from the monthly MLS® figures (SnapStats) for condos and townhomes in {disp}. No building list, strata fees, street boundaries or live listing feed yet; see the open items.'}]
        bl.append({'t': 'p', 'text': f'{disp} condos and townhomes in {CITY}: {L.num(cur["inventory"])} listed at the end of {mn} {last[:4]} and {L.num(cur["sales"])} sold in the month, a sales ratio of {ratio_txt}. That makes {disp} number {rank} of {len(ranked)} {CITY} communities by condo and townhome listings. Houses in {disp} have their own page; this page is only about attached homes.', 'gen': 'condopage'})
        bl.append({'t': 'grid'})
        bl.append({'t': 'h', 'level': 2, 'text': f'{disp} condos and townhomes listed and sold, {L.month_name(first)} to {mn} {last[:4]}', 'gen': 'condopage'})
        bl.append({'t': 'table', 'caption': f'{disp} condos and townhomes by month, with share of {CITY}', 'head': ['Month', 'Listed', 'Sold', 'Sales ratio', f'Share of {CITY} condo listings', f'Share of {CITY} condo sales'], 'rows': rows,
                   'source': L.SRC + L.RATIO_NOTE + ' The reports count condos and townhomes together in one line, so this table cannot separate the two. Shares are this community’s count divided by the {0} total for condos and townhomes that month.'.format(CITY), 'gen': 'condopage'})
        bl.append({'t': 'p', 'text': move + f' In {mn} the community held {100 * cur["inventory"] / tot[last]["inventory"]:.1f}% of {CITY}’s {L.num(tot[last]["inventory"])} condo and townhome listings.', 'gen': 'condopage'})
        if hc and (hc.get('inventory') or hc.get('sales')):
            hs = f'{hc["inventory"]} houses listed and {hc["sales"]} sold in {mn}' 
            bl.append({'t': 'h', 'level': 2, 'text': f'Condos or houses in {disp}?', 'gen': 'condopage'})
            bl.append({'t': 'p', 'text': f'{disp} also had {hs}, against {L.num(cur["inventory"])} condos and townhomes listed. If you are weighing a house, the {disp} homes page has the detached figures and the feed for houses.', 'gen': 'condopage'})
        items = [[{'t': f'{disp} homes for sale (houses)', 'h': f'/{houses_slug}.html'}], [{'t': f'{CITY} homes for sale', 'h': '/burnaby-homes-for-sale.html'}], [{'t': f'{CITY} real estate market stats', 'h': '/burnaby-real-estate-market-stats.html'}]]
        for _, o_slug, o_slug2, o_disp in [(p[0], p[0], p[2], p[3]) for p in PAGES if p[2] != slug]: items.append([{'t': f'{o_disp} condos for sale', 'h': f'/{o_slug2}.html'}])
        bl.append({'t': 'h', 'level': 2, 'text': f'More {CITY} real estate', 'gen': 'condopage', 'pos': 'end'})
        bl.append({'t': 'list', 'items': items, 'gen': 'condopage', 'pos': 'end'})
        tot_s = sum((r['sales'] or 0) for _, r in S if r)
        faq = [
            {'q': f'How many condos are for sale in {disp}?', 'a': f'At the end of {mn} {last[:4]} the {L.BOARD_NAME["GVR"]} figures showed {L.num(cur["inventory"])} condos and townhomes listed in {disp}. That is a month-end count and moves daily; ask Jared for what is on the market today.'},
            {'q': f'Is {disp} a buyers’ or sellers’ market for condos?', 'a': f'In {mn} {last[:4]}, condos and townhomes in {disp} had a sales ratio of {ratio_txt}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'},
            {'q': f'How many condos sold in {disp} from {L.month_name(first)} to {mn} {last[:4]}?', 'a': f'{tot_s} condos and townhomes sold in {disp} over those {len(keys)} months, out of {L.num(sum(tot[m]["sales"] or 0 for m in keys))} in all of {CITY}.'},
            {'q': f'Do these numbers separate condos from townhomes?', 'a': 'No. The monthly reports publish condos and townhomes as one line, so any count here includes both. Jared can pull the split for a specific building or street.'}]
        data = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'condo_page_for': houses_slug,
                'new_page': {'title': title(disp), 'description': f'{disp}, {CITY} condos for sale: {L.num(cur["inventory"])} condos and townhomes listed in {mn} {last[:4]}, monthly sales and how {disp} compares with {CITY}. Jared Gibbons, REALTOR®.',
                             'h1': f'{disp} Condos for Sale | {CITY} Real Estate'},
                'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': CITY, 'href': '/burnaby-homes-for-sale.html'}, {'name': f'{disp} condos', 'href': f'/{slug}.html'}],
                'faq_heading': f'{disp} condos: your questions answered', 'blocks': bl, 'faq': faq,
                'needs_from_muse': [f'Named condo buildings and townhome complexes in {name}, confirmed on strata or developer sources', f'Strata fee ranges, building ages and rental/pet rules', f'Sold prices and days on market for {name} condos (the reports give them for {CITY} as a whole)', f'Street boundaries of {name} from the Paragon sub-area map', f'A condo-filtered live listing feed for {name}', 'Jared\'s own notes on these buildings and who buys them']}
        json.dump(data, open(os.path.join(ROOT, 'src/data/local', slug + '.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(os.path.join(ROOT, 'src/data/local', slug + '.json'), 'a').write('\n')
        # the houses page links across to the condo page
        hf = os.path.join(ROOT, 'src/data/local', houses_slug + '.json'); h = json.load(open(hf, encoding='utf-8'))
        h['blocks'] = [b for b in h['blocks'] if b.get('gen') != 'condopage']
        h['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{disp} condos and townhomes', 'gen': 'condopage', 'pos': 'end'},
                        {'t': 'list', 'items': [[{'t': f'{disp} condos for sale', 'h': f'/{slug}.html'}]], 'gen': 'condopage', 'pos': 'end'}]
        json.dump(h, open(hf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(hf, 'a').write('\n')
        print('wrote', slug, title(disp), len(title(disp)))


if __name__ == '__main__':
    main()
