#!/usr/bin/env python3
"""34 neighbourhood house and condo-townhome pages (D-316): the pages on Pete's list that the site did not have (Tsawwassen, Ladner,
Chilliwack and three in South Surrey / White Rock). Gerry saved one MyRealPage search per page (sheet returned 2026-11-16).

    python3 -I tools/build_nb34_pages.py /path/to/gerry-34-done.xlsx   -> src/data/local/<slug>.json, idx-embeds, nb-type-links.json

Built from figures already in the repo: the Paragon closed-sales aggregate (src/data/sold/sold-12m.json, grouped figures only, the same
5-sale minimum as every other page) for the sub-area and its city. Links to the neighbourhood page and guide, the city's type page and
the other new page for the same neighbourhood. Rebuilt each run; "hand_edited": true stops a page being overwritten.
"""
import json, os, re, sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import build_sold_layer as S  # noqa: E402

LOCAL = ROOT / 'src/data/local'
G = 'nb34'
DAY = '2026-11-16'
# MLS area -> (sold aggregate prefix, city key in the aggregate, display city, hub page, city type pages)
CITY = {
    'Tsawwassen': ('Tsawwassen', 'tsawwassen', 'Tsawwassen', 'tsawwassen-homes-for-sale', {'houses': 'tsawwassen-houses-for-sale', 'condos': 'tsawwassen-condos-for-sale', 'townhomes': 'tsawwassen-townhomes-for-sale'}),
    'Ladner': ('Ladner', 'ladner', 'Ladner', 'ladner-homes-for-sale', {'houses': 'ladner-houses-for-sale', 'condos': 'ladner-condos-for-sale', 'townhomes': 'ladner-townhomes-for-sale'}),
    'Chilliwack': ('Chilliwack', 'chilliwack', 'Chilliwack', 'chilliwack-homes-for-sale', {'houses': 'chilliwack-houses-for-sale', 'condos': 'chilliwack-condos-for-sale', 'townhomes': 'chilliwack-townhomes-for-sale'}),
    'South Surrey White Rock': ('South Surrey White Rock', 'south-surrey', 'South Surrey', 'south-surrey-homes-for-sale', {'houses': 'south-surrey-houses-for-sale', 'condos': 'south-surrey-condos-for-sale', 'townhomes': 'south-surrey-townhomes-for-sale'}),
}
DISPLAY = {'Crescent Bch Ocean Pk.': 'Crescent Beach and Ocean Park'}
NBPAGE = {'Crescent Bch Ocean Pk.': 'crescent-bch-ocean-pk', 'White Rock': 'white-rock'}
GUIDE = {'Crescent Bch Ocean Pk.': 'crescent-beach-ocean-park-guide', 'White Rock': 'white-rock-guide'}


ONE = {'houses': 'house', 'townhomes': 'townhome', 'condos-townhomes': 'condo and townhome'}


def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def P(t): return {'t': 'p', 'text': t, 'gen': G}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': G, **k}
def regen(blocks): return [dict(b, gen=G) for b in blocks]


def kinds(ptype, slug):
    if ptype.startswith('House'): return 'houses', ['house'], 'Houses', 'houses'
    if ptype == 'Townhouse': return 'townhomes', ['townhome'], 'Townhomes', 'townhomes'
    return 'condos-townhomes', ['condo', 'townhome'], 'Condos & Townhomes', 'condos and townhomes'


def main(src):
    agg = S.load()
    wb = openpyxl.load_workbook(src, data_only=True); ws = wb.worksheets[0]
    hdr = [c.value for c in ws[1]]
    rows = [dict(zip(hdr, [c.value for c in r])) for r in ws.iter_rows(min_row=2) if r[0].value]
    exists = {p.stem for p in LOCAL.glob('*.json')} | {p.stem for p in (ROOT / 'src/data/pages').glob('*.json')}
    new = {r['Page to build'] for r in rows}
    idx = json.loads((ROOT / 'src/data/idx-embeds.json').read_text())
    links = {}
    made = []
    for r in rows:
        slug, area, sub, sid = r['Page to build'], r['MLS area'], r['Sub-area'], str(r['Search ID (Gerry fills)']).strip()
        assert re.fullmatch(r'\d{7}', sid), (slug, sid)
        pref, ck, city, hub, ctype = CITY[area]
        if sub == 'White Rock':   # its own city, not part of South Surrey
            city, hub = 'White Rock', 'white-rock'
        kslug, groups, Kind, noun = kinds(r['Property type'], slug)
        disp = DISPLAY.get(sub, sub)
        key = f'{pref}|{sub}'
        sd = agg['sub'][key]; g = sd['groups']; cd = agg['city'].get(ck) if sub != 'White Rock' else None
        main_g = max([x for x in groups if x in g] or groups, key=lambda x: g.get(x, {}).get('n', 0))
        nb = NBPAGE.get(sub, slugify(sub)); guide = GUIDE.get(sub, f'{slugify(sub)}-guide')
        cityname = '' if city.lower() in disp.lower() or disp.lower() in city.lower() else city
        where = f'{disp}, {cityname}' if cityname else disp
        base = lambda x: re.sub(r'-(houses|condos-townhomes|townhomes)-for-sale$', '', x)
        twin = next((x for x in new if x != slug and base(x) == base(slug)), None)
        # ---- blocks
        s0 = g.get(main_g, {})
        lead = (f'In the last year {s0["n"]} {S.GL[main_g]} sold here at a median {S.money(s0["price"])}, half of them within {s0["dom"]} days.'
                if s0.get('n', 0) >= S.MIN_MED and 'price' in s0 else f'Few {noun} sold here in the last year, so ask me for the sales behind any listing you like.')
        bl = [P(f'Every {ONE[kslug]} for sale in {where}, live from the MLS®, and what they actually sold for. {lead}')]
        items = []
        def add(s, text):
            if s and (s in exists or s in new): items.append([{'t': text, 'h': f'/{s}.html'}])
        add(nb, f'{disp} real estate, all home types'); add(guide, f'Living in {disp}: the neighbourhood guide'); add(twin, f'{disp} {"condos and townhomes" if kslug == "houses" else "houses"} for sale')
        for k in (['houses'] if kslug == 'houses' else ['townhomes'] if kslug == 'townhomes' else ['condos', 'townhomes']):
            add(ctype[k], f'All {"South Surrey and White Rock" if sub == "White Rock" else city} {k} for sale')
        bl.append({'t': 'list', 'items': items, 'gen': G})
        bl += [H(f'{disp} {noun} for sale now'), {'t': 'grid', 'gen': G}]
        sold = [x for x in groups if x in g and g[x]['n'] >= S.MIN_MENTION]
        bl.append(H(f'What {disp} {noun} sold for, {S.WINDOW}'))
        if sold:
            bl.append(P(' '.join(S.one_line(disp, g[x], x) for x in sorted(sold, key=lambda x: -g[x]['n']))))
            if len(groups) > 1: bl += regen(S.mix_table(disp, g, groups))
            if g[main_g]['n'] >= 12: bl += regen(S.quarter_table(disp, g[main_g], main_g))
            for x in ('condo', 'townhome'):
                if x in groups and sd.get('complexes', {}).get(x): bl += regen(S.bldg_table(disp, sd['complexes'][x], x))
        else:
            bl.append(P(f'Fewer than {S.MIN_MENTION} {noun} sold in {disp} between {S.WINDOW}, too few to describe. Ask me for the sales behind any listing you like.'))
        # compare with the city
        if cd and main_g in cd['groups'] and cd['groups'][main_g]['n'] >= S.MIN_MED:
            c = cd['groups'][main_g]; s = g.get(main_g, {})
            bl.append(H(f'How {disp} compares with the rest of {city}'))
            if s.get('n', 0) >= S.MIN_MED and 'price' in s:
                diff = s['price'] - c['price']; pct = round(100 * abs(diff) / c['price'])
                rel = 'about the same as' if pct < 3 else f'{pct}% {"above" if diff > 0 else "below"}'
                bl.append(P(f'The median {S.GL[main_g][:-1]} in {disp} sold for {S.money(s["price"])}, {rel} the {city} median of {S.money(c["price"])} across {c["n"]:,} sales. '
                            f'{disp} {S.GL[main_g]} took a median {s["dom"]} days to sell, against {c["dom"]} days for {city} as a whole.'))
            bl += regen(S.sub_table(city, cd['subs'], main_g, agg))
        bl.append(P(f'Thinking of buying in {disp}? I can pull the sales behind any listing on this page, book a private showing, and set up an email alert for new {noun} here. Call or text 604-928-1361.'))
        faq = []
        if main_g in g and g[main_g]['n'] >= S.MIN_MED:
            faq = S.sold_faq(disp, noun, g[main_g], main_g) + S.sold_faq_more(disp, noun, g[main_g], main_g, None, agg)
        faq = [dict(q, gen=G) for q in faq] + [{'q': 'Can I book a private showing with Jared?', 'a': 'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.', 'gen': G}]
        # ---- meta
        h1 = f'{disp} {Kind} for Sale' + (f' | {city} Real Estate' if cityname else '')
        title = next(t for t in (f'{disp}, {cityname} {Kind} for Sale' if cityname else '', f'{disp} {Kind} for Sale | {city}' if cityname else '', f'{disp} {Kind} for Sale') if t and len(t) <= 60)
        if len(title) <= 44: title += ' | Jared Gibbons'
        desc = f'{disp} {noun} for sale, live from the MLS®, and what they sold for: ' + (f'{s0["n"]} sales at a median {S.money(s0["price"])}, {s0["dom"]} days to sell.' if s0.get('n', 0) >= S.MIN_MED and 'price' in s0 else 'recent sales and prices.')
        if len(desc) > 155: desc = f'{disp} {noun} for sale, live from the MLS®, with what they sold for in the last year. Jared Gibbons, REALTOR®.'
        assert len(desc) <= 155, (slug, len(desc))
        f = LOCAL / f'{slug}.json'
        if f.exists() and json.loads(f.read_text()).get('hand_edited'): continue
        data = {'status': 'draft', 'slug': slug, 'updated': DAY, 'nb34_page': {'area': area, 'sub': sub, 'type': kslug},
                'new_page': {'title': title, 'description': desc, 'h1': h1},
                'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': city, 'href': f'/{hub}.html'}, {'name': f'{disp} {noun}', 'href': f'/{slug}.html'}],
                'faq_heading': f'{disp} {noun}: your questions answered', 'faq': faq, 'blocks': bl}
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n'); made.append(slug)
        idx['pages'][slug] = sid
        # links to the new page from its neighbourhood page and the city type page (added at build time, GenericPage.astro)
        links.setdefault(nb, []).append([f'{disp} {noun} for sale', f'/{slug}.html'])
        for k in (['houses'] if kslug == 'houses' else ['townhomes'] if kslug == 'townhomes' else ['condos', 'townhomes']):
            links.setdefault(ctype[k], []).append([f'{disp} {noun}', f'/{slug}.html'])
    idx['pages'] = dict(sorted(idx['pages'].items()))
    (ROOT / 'src/data/idx-embeds.json').write_text(json.dumps(idx, ensure_ascii=False, indent=1) + '\n')
    links = {k: sorted(v, key=lambda x: (not x[0].endswith('houses for sale'), x[0])) for k, v in sorted(links.items()) if k in exists or k in new}
    (ROOT / 'src/data/nb-type-links.json').write_text(json.dumps({'_note': 'Links to the D-316 neighbourhood pages, added at build time (tools/build_nb34_pages.py).', 'links': links}, ensure_ascii=False, indent=1) + '\n')
    print(len(made), 'pages;', len(links), 'pages get links')


if __name__ == '__main__':
    main(sys.argv[1])
