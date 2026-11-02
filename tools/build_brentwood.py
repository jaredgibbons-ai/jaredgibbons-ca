"""Brentwood Park, split by search intent (Jared, 2026-11-01: "Brentwood Park should be the guide, then homes is for homes/houses,
condo page for condos and townhouse page for townhouse").

  brentwood-park                    the neighbourhood guide (all home types at a glance, links to the three pages below)
  brentwood-homes-for-sale          houses (detached) only
  brentwood-park-condos-for-sale    condos
  brentwood-park-townhomes-for-sale townhomes

The monthly reports (SnapStats) publish condos and townhomes as ONE line, so the condo and townhome pages cannot show separate
counts until Jared's Paragon export arrives; both say so. Run after build_snapstats_layers.py (it rewrites the guide's snapstats blocks).
    python3 -I tools/build_brentwood.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_snapstats_layers as L

ROOT = L.ROOT
AK, CITY, NAME = 'burnaby', 'Burnaby', 'Brentwood Park'
GUIDE, HOMES, CONDO, TOWN = 'brentwood-park', 'brentwood-homes-for-sale', 'brentwood-park-condos-for-sale', 'brentwood-park-townhomes-for-sale'
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
GEN = 'brentwood'
# archive text on the houses page that is about towers and the Town Centre; it moves to the guide unchanged
MOVED_P = ['Brentwood represents Burnaby', 'Residents love walkability']
MOVED_H = 'Brentwood Homes for Sale: Urban Energy with Convenience'
HIDE = ['Brentwood homes for sale feature modern high-rise', MOVED_H] + MOVED_P


def lp(slug): return os.path.join(ROOT, 'src/data/local', slug + '.json')
def load(slug): return json.load(open(lp(slug), encoding='utf-8')) if os.path.exists(lp(slug)) else {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
def save(slug, j):
    with open(lp(slug), 'w', encoding='utf-8') as f: json.dump(j, f, indent=2, ensure_ascii=False); f.write('\n')
def title(head):
    return head + BR if len(head + BR) <= 66 else head + BS
def P(t, **k): return {'t': 'p', 'text': t, 'gen': GEN, **k}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': GEN, **k}
def links(items, **k): return {'t': 'list', 'items': [[{'t': a, 'h': h}] for a, h in items], 'gen': GEN, **k}


def main():
    months = L.load_months(); keys = list(months); last, first = keys[-1], keys[0]
    mn, yr, nm = L.month_name(last), last[:4], len(keys)
    S = {t: dict(L.series(months, AK, t, NAME)) for t in ('detached', 'condo_townhome')}
    tot = {t: {m: months[m]['areas'][AK][t]['total'] for m in keys} for t in S}
    cur = {t: S[t][last] for t in S}
    def rows(t):
        out = []
        for m in keys:
            r = S[t][m]
            if not r: out.append([L.mlabel(m), '—', '—', '—', '—']); continue
            sh = '—' if not tot[t][m]['inventory'] else f'{100 * (r["inventory"] or 0) / tot[t][m]["inventory"]:.1f}%'
            out.append([L.mlabel(m), L.num(r['inventory']), L.num(r['sales']), L.pct(r['ratio']), sh])
        return out
    def ratio_txt(r, what):
        k = L.kind(r['ratio']) if r['inventory'] >= 10 else None
        return f'{L.pct(r["ratio"])}' + (f', which the reports’ scale reads as {k}' if k else f' on only {r["inventory"]} listed, too few to read as a market type')
    def sold(t): return sum((S[t][m]['sales'] or 0) for m in keys if S[t][m])
    h, c = cur['detached'], cur['condo_townhome']
    all_listed = h['inventory'] + c['inventory']
    pct_h = 100 * h['inventory'] / all_listed
    notice = lambda what: {'t': 'notice', 'text': f'Draft for Jared\'s approval. {what} Built only from the monthly MLS® figures (SnapStats). No building list, strata fees, street boundaries or live listing feed filtered to this home type yet.', 'gen': GEN}
    pages = {}

    # ---------- houses ----------
    hb = [notice('Houses (detached) in Brentwood Park only.'),
          P(f'Houses in {NAME}, {CITY}: {L.num(h["inventory"])} listed at the end of {mn} {yr} and {L.num(h["sales"])} sold in the month, a sales ratio of {ratio_txt(h, "houses")}. Houses are the smaller part of {NAME}: {pct_h:.0f}% of its {L.num(all_listed)} listings. Condos and townhomes have their own pages, and the {NAME} guide covers the neighbourhood.'),
          {'t': 'h', 'level': 2, 'text': f'{NAME} houses listed and sold, {L.month_name(first)} to {mn} {yr}', 'gen': GEN},
          {'t': 'table', 'caption': f'{NAME} houses by month, with share of {CITY}', 'head': ['Month', 'Listed', 'Sold', 'Sales ratio', f'Share of {CITY} house listings'], 'rows': rows('detached'),
           'source': L.SRC + L.RATIO_NOTE + f' Shares are this community’s count divided by the {CITY} total for detached houses that month.', 'gen': GEN},
          P(f'Over {nm} months {L.num(sold("detached"))} houses sold in {NAME} against an average of {sum((S["detached"][m]["inventory"] or 0) for m in keys) / nm:.1f} listed at month end. In {mn} the community held {100 * h["inventory"] / tot["detached"][last]["inventory"]:.1f}% of {CITY}’s {L.num(tot["detached"][last]["inventory"])} house listings.'),
          H('Houses, condos or townhomes in Brentwood Park?'),
          P(f'Most of {NAME} is attached housing: {L.num(c["inventory"])} condos and townhomes were listed in {mn} against {L.num(h["inventory"])} houses. If you are looking at towers near the SkyTrain, start with the condo page; for ground-level homes in a complex, the townhome page.'),
          H(f'More {NAME} real estate', pos='end'),
          links([(f'{NAME} neighbourhood guide', f'/{GUIDE}.html'), (f'{NAME} condos for sale', f'/{CONDO}.html'), (f'{NAME} townhomes for sale', f'/{TOWN}.html'), (f'{CITY} homes for sale', '/burnaby-homes-for-sale.html'), (f'{CITY} real estate market stats', '/burnaby-real-estate-market-stats.html'), ('Metrotown homes for sale', '/metrotown-homes-for-sale.html')], pos='end')]
    hf = [{'q': f'How many houses are for sale in {NAME}?', 'a': f'At the end of {mn} {yr} the reports showed {L.num(h["inventory"])} houses listed in {NAME}. That is a month-end count and moves daily; ask Jared what is on the market today.'},
          {'q': f'Is {NAME} a buyers’ or sellers’ market for houses?', 'a': f'In {mn} {yr} houses in {NAME} had a sales ratio of {ratio_txt(h, "houses")}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'},
          {'q': f'How many houses sold in {NAME} from {L.month_name(first)} to {mn} {yr}?', 'a': f'{L.num(sold("detached"))} houses sold over those {nm} months, out of {L.num(sum(tot["detached"][m]["sales"] or 0 for m in keys))} house sales in all of {CITY}.'},
          {'q': f'Why are there so few houses for sale in {NAME}?', 'a': f'Most of the community is condos and townhomes. In {mn} {yr}, houses were {pct_h:.0f}% of the {L.num(all_listed)} listings in {NAME}.'},
          {'q': 'Where are the Brentwood condos and townhomes?', 'a': f'They have their own pages: the {NAME} condo page and the {NAME} townhome page. The neighbourhood guide covers the area as a whole.'}]
    pages[HOMES] = dict(blocks=hb, faq=hf, faq_heading=f'{NAME} houses: your questions answered', hide=HIDE, hand_edited=True)

    # ---------- condos / townhomes (one line in the reports) ----------
    rk = sorted(((x['inventory'] or 0, x['name']) for x in months[last]['areas'][AK]['condo_townhome']['communities']), reverse=True)
    rank = [n for _, n in rk].index(NAME) + 1
    both = 'The monthly reports publish condos and townhomes as one line, so the figures on this page cover both and cannot be split until Jared’s sold-listing export is added.'
    move = ''
    a, b = S['condo_townhome'][first]['inventory'], c['inventory']
    move = f'Condo and townhome listings in {NAME} {"rose" if b > a else "fell" if b < a else "held"} from {L.num(a)} in {L.month_name(first)} to {L.num(b)} in {mn}, while {L.num(sold("condo_townhome"))} sold across the {nm} months.'
    cb = [notice('Condos in Brentwood Park.'),
          P(f'{NAME} condos in {CITY}: {both} {L.num(c["inventory"])} condos and townhomes were listed at the end of {mn} {yr} and {L.num(c["sales"])} sold in the month, a sales ratio of {ratio_txt(c, "condos")}. That makes {NAME} number {rank} of {len(rk)} {CITY} communities by condo and townhome listings.'),
          {'t': 'grid', 'gen': GEN},
          {'t': 'h', 'level': 2, 'text': f'{NAME} condos and townhomes listed and sold, {L.month_name(first)} to {mn} {yr}', 'gen': GEN},
          {'t': 'table', 'caption': f'{NAME} condos and townhomes by month, with share of {CITY}', 'head': ['Month', 'Listed', 'Sold', 'Sales ratio', f'Share of {CITY} condo and townhome listings'], 'rows': rows('condo_townhome'),
           'source': L.SRC + L.RATIO_NOTE + f' Condos and townhomes are one line in the reports. Shares are this community’s count divided by the {CITY} total for condos and townhomes that month.', 'gen': GEN},
          P(move + f' In {mn} the community held {100 * c["inventory"] / tot["condo_townhome"][last]["inventory"]:.1f}% of {CITY}’s {L.num(tot["condo_townhome"][last]["inventory"])} condo and townhome listings.'),
          H(f'Condos or houses in {NAME}?'),
          P(f'{NAME} also had {L.num(h["inventory"])} houses listed and {L.num(h["sales"])} sold in {mn}, against {L.num(c["inventory"])} condos and townhomes listed. The houses page has the detached figures and the guide covers the neighbourhood.'),
          H(f'More {CITY} real estate', pos='end'),
          links([(f'{NAME} neighbourhood guide', f'/{GUIDE}.html'), (f'{NAME} houses for sale', f'/{HOMES}.html'), (f'{NAME} townhomes for sale', f'/{TOWN}.html'), (f'{CITY} homes for sale', '/burnaby-homes-for-sale.html'), (f'{CITY} real estate market stats', '/burnaby-real-estate-market-stats.html'), ('Cariboo condos for sale', '/cariboo-condos-for-sale.html'), ('Edmonds condos for sale', '/edmonds-condos-for-sale.html')], pos='end')]
    cf = [{'q': f'How many condos are for sale in {NAME}?', 'a': f'At the end of {mn} {yr} the reports showed {L.num(c["inventory"])} condos and townhomes listed in {NAME}. That is a month-end count and moves daily; ask Jared what is on the market today.'},
          {'q': f'Is {NAME} a buyers’ or sellers’ market for condos?', 'a': f'In {mn} {yr} condos and townhomes in {NAME} had a sales ratio of {ratio_txt(c, "condos")}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'},
          {'q': f'How many condos sold in {NAME} from {L.month_name(first)} to {mn} {yr}?', 'a': f'{L.num(sold("condo_townhome"))} condos and townhomes sold over those {nm} months, out of {L.num(sum(tot["condo_townhome"][m]["sales"] or 0 for m in keys))} in all of {CITY}.'},
          {'q': 'Do these numbers separate condos from townhomes?', 'a': both},
          {'q': f'Where are the {NAME} houses and townhomes?', 'a': f'Houses and townhomes each have their own page, and the {NAME} guide covers the neighbourhood as a whole.'}]
    pages[CONDO] = dict(blocks=cb, faq=cf, faq_heading=f'{NAME} condos: your questions answered', hand_edited=True,
                        new_page={'title': title(f'{NAME} Burnaby Condos for Sale'), 'description': f'{NAME}, {CITY} condos for sale: condos near Brentwood Town Centre, monthly listings and sales, and how {NAME} compares with {CITY}. Jared Gibbons, REALTOR®.', 'h1': f'{NAME} Condos for Sale | {CITY} Real Estate'})

    # townhome page: same combined line, a different cut (how Brentwood Park ranks among Burnaby communities)
    top = rk[:8]
    trs = []
    for n_, nme in [(i, nme) for i, (_, nme) in enumerate(top)]:
        r = next(x for x in months[last]['areas'][AK]['condo_townhome']['communities'] if x['name'] == nme)
        trs.append([nme, L.num(r['inventory']), L.num(r['sales']), L.pct(r['ratio'])])
    if NAME not in [r[0] for r in trs]:
        r = next(x for x in months[last]['areas'][AK]['condo_townhome']['communities'] if x['name'] == NAME); trs.append([NAME, L.num(r['inventory']), L.num(r['sales']), L.pct(r['ratio'])])
    tb = [notice('Townhomes in Brentwood Park.'),
          P(f'{NAME} townhomes in {CITY}: {both} The combined line showed {L.num(c["inventory"])} condos and townhomes listed at the end of {mn} {yr}, {'the most of any ' + CITY + ' community' if rank == 1 else 'number ' + str(rank) + ' of ' + str(len(rk)) + ' ' + CITY + ' communities'}, and {L.num(c["sales"])} sold in the month.'),
          {'t': 'grid', 'gen': GEN},
          {'t': 'h', 'level': 2, 'text': f'Where {NAME} sits among {CITY} communities', 'gen': GEN},
          {'t': 'table', 'caption': f'{CITY} communities with the most condo and townhome listings, {mn} {yr}', 'head': ['Community', 'Listed', 'Sold', 'Sales ratio'], 'rows': trs,
           'source': L.SRC + L.RATIO_NOTE + ' Condos and townhomes are one line in the reports.', 'gen': GEN},
          P(f'A townhome is a ground-level home that is part of a complex, and in BC it is usually owned within a strata. What is on offer in {NAME} at any moment depends on the live listings, which is where Jared starts when he sets up a search.'),
          H(f'Townhomes or condos in {NAME}?'),
          P(f'Most of the attached homes in {NAME} are listed in the condo and townhome line together. The condo page has the month-by-month table; the houses page has the {L.num(h["inventory"])} detached listings.'),
          H(f'More {CITY} real estate', pos='end'),
          links([(f'{NAME} neighbourhood guide', f'/{GUIDE}.html'), (f'{NAME} houses for sale', f'/{HOMES}.html'), (f'{NAME} condos for sale', f'/{CONDO}.html'), (f'{CITY} homes for sale', '/burnaby-homes-for-sale.html'), (f'{CITY} real estate market stats', '/burnaby-real-estate-market-stats.html'), ('Cariboo condos for sale', '/cariboo-condos-for-sale.html')], pos='end')]
    tf = [{'q': f'How many townhomes are for sale in {NAME}?', 'a': f'The reports count townhomes and condos together: {L.num(c["inventory"])} listed in {NAME} at the end of {mn} {yr}. A townhome-only count needs the sold and active listing export from Jared’s board system, so ask him for what is on the market today.'},
          {'q': f'Is {NAME} a buyers’ or sellers’ market for townhomes?', 'a': f'For condos and townhomes together the sales ratio in {mn} {yr} was {ratio_txt(c, "townhomes")}. On the reports’ scale under 12% favours buyers, 12% to 20% is balanced and over 20% favours sellers.'},
          {'q': f'How does {NAME} compare with other {CITY} communities for attached homes?', 'a': f'It ranked number {rank} of {len(rk)} {CITY} communities by condo and townhome listings in {mn} {yr}.'},
          {'q': 'Do these numbers separate townhomes from condos?', 'a': both},
          {'q': f'Where are the {NAME} houses and condos?', 'a': f'Houses and condos each have their own page, and the {NAME} guide covers the neighbourhood as a whole.'}]
    pages[TOWN] = dict(blocks=tb, faq=tf, faq_heading=f'{NAME} townhomes: your questions answered', hand_edited=True,
                       new_page={'title': title(f'{NAME} Burnaby Townhomes for Sale'), 'description': f'{NAME}, {CITY} townhomes for sale: attached homes near Brentwood Town Centre, how {NAME} ranks among {CITY} communities, and market figures. Jared Gibbons, REALTOR®.', 'h1': f'{NAME} Townhomes for Sale | {CITY} Real Estate'})

    for slug, spec in pages.items():
        j = load(slug)
        keep = [b for b in j.get('blocks', []) if b.get('gen') in ('musefaq', 'relatedlinks')]  # sources list / related links rebuilt by their own scripts
        for k in ('condo_page_for', 'needs_from_muse', 'breadcrumbs'): j.pop(k, None)
        j.update({k: v for k, v in spec.items() if k != 'blocks'})
        j['blocks'] = spec['blocks'] + keep
        j['status'] = 'draft'; j['updated'] = '2026-11-01'
        j['breadcrumbs'] = [{'name': 'Home', 'href': '/index.html'}, {'name': CITY, 'href': '/burnaby-homes-for-sale.html'}, {'name': NAME, 'href': f'/{GUIDE}.html'}, {'name': {HOMES: 'Houses', CONDO: 'Condos', TOWN: 'Townhomes'}[slug], 'href': f'/{slug}.html'}]
        j['needs_from_muse'] = [f'Separate condo and townhome counts, sold prices and days on market for {NAME} (Paragon sold export)', 'Named buildings and townhome complexes, strata fee ranges and building ages', 'A feed filtered to this home type', 'Jared\'s own notes']
        save(slug, j)
        print('wrote', slug)

    # ---------- guide ----------
    g = load(GUIDE)
    arch = json.load(open(os.path.join(ROOT, 'src/data/pages', HOMES + '.json'), encoding='utf-8'))['blocks']
    moved = []
    for b in arch:
        tx = b.get('text', '') if b['t'] in ('p', 'h') else ''
        if b['t'] == 'h' and tx == MOVED_H: moved.append({'t': 'h', 'level': 3, 'text': tx, 'gen': GEN})
        elif b['t'] == 'p' and any(tx.startswith(x) for x in MOVED_P): moved.append({'t': 'p', 'text': tx, 'gen': GEN})
    glance = [['Houses', L.num(h['inventory']), L.num(h['sales']), L.pct(h['ratio'])], ['Condos and townhomes', L.num(c['inventory']), L.num(c['sales']), L.pct(c['ratio'])]]
    gb = [H(f'{NAME} at a glance, {mn} {yr}'),
          P(f'{NAME} is a {CITY} community around Brentwood Town Centre. In {mn} {yr} it had {L.num(all_listed)} homes listed: {L.num(c["inventory"])} condos and townhomes and {L.num(h["inventory"])} houses. It ranks number {rank} of {len(rk)} {CITY} communities by condo and townhome listings, and houses are {pct_h:.0f}% of what is for sale.'),
          {'t': 'table', 'caption': f'{NAME} by home type, {mn} {yr}', 'head': ['Home type', 'Listed', 'Sold', 'Sales ratio'], 'rows': glance,
           'source': L.SRC + L.RATIO_NOTE + ' Condos and townhomes are one line in the reports.', 'gen': GEN},
          H(f'Browse {NAME} by home type'),
          links([(f'{NAME} houses for sale', f'/{HOMES}.html'), (f'{NAME} condos for sale', f'/{CONDO}.html'), (f'{NAME} townhomes for sale', f'/{TOWN}.html')]),
          *moved]
    keepg = [b for b in g['blocks'] if b.get('gen') not in ('snapstats', 'condopage', GEN)]
    g['blocks'] = gb + keepg
    save(GUIDE, g); print('wrote', GUIDE)


if __name__ == '__main__':
    main()
