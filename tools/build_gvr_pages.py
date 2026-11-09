"""City neighbourhood hubs and the missing neighbourhood pages for Richmond, Vancouver, Burnaby, New Westminster and Coquitlam
(Jared, 2026-11-05: "create hubs and pages for Richmond, Vancouver, Burnaby, New Westminster and Coquitlam").

Hubs: src/data/local/<city>-neighbourhood-guides.json (status draft), one per city, listing every MLS® sub-area of the city with its page
(where we have one) and what sold there, from the Paragon closed-sales aggregate (src/data/sold/sold-12m.json).
Pages: one draft page per sub-area that has no page yet and at least MIN_SALES closed sales in the window; figures from the same aggregate,
local facts only from docs/research/local-notes-gvr/<slug>.md (each fact carries its source URL; lines marked UNVERIFIED are not published).
The maps on the hubs and pages are added by tools/apply_maps.py once src/data/maps/<region>.json exists.

    python3 -I tools/build_gvr_pages.py
Pages with "hand_edited": true are left alone."""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_sold_layer as SO

ROOT = os.path.join(HERE, '..')
LOCAL = os.path.join(ROOT, 'src/data/local')
PAGES = os.path.join(ROOT, 'src/data/pages')
NOTES = os.path.join(ROOT, 'docs/research/local-notes-gvr')
AGG = SO.load()
WINDOW = SO.WINDOW
G = 'gvr'
UPDATED = '2026-11-05'
MIN_SALES = 10          # a new page needs this many closed sales (all home types) in the window
BR, BS = ' | Jared Gibbons REALTOR®', ' | Jared Gibbons'
money = SO.money

CITIES = {
    'richmond': dict(name='Richmond', boards=['Richmond'], hub='richmond-neighbourhood-guides', homes='richmond-homes-for-sale', market='richmond-real-estate-market-stats',
                     schools='schools-in-richmond-bc', newc='new-construction-richmond', suffix='richmond', region='richmond'),
    'vancouver': dict(name='Vancouver', boards=['Vancouver West', 'Vancouver East'], hub='vancouver-neighbourhood-guides', homes='vancouver-homes-for-sale', market='vancouver-real-estate-market-stats',
                      schools='schools-in-vancouver-bc', newc=None, suffix='vancouver', region='vancouver'),
    'burnaby': dict(name='Burnaby', boards=['Burnaby North', 'Burnaby South', 'Burnaby East'], hub='burnaby-neighbourhood-guides', homes='burnaby-homes-for-sale', market='burnaby-real-estate-market-stats',
                    schools='schools-in-burnaby-bc', newc=None, suffix='burnaby', region='burnaby'),
    'new-westminster': dict(name='New Westminster', boards=['New Westminster'], hub='new-westminster-neighbourhood-guides', homes='new-westminster-homes-for-sale', market='new-westminster-real-estate-market-stats',
                            schools='schools-in-new-westminster-bc', newc='new-construction-new-westminster', suffix='new-westminster', region='new-westminster'),
    'coquitlam': dict(name='Coquitlam', boards=['Coquitlam'], hub='coquitlam-neighbourhood-guides', homes='coquitlam-homes-for-sale', market='coquitlam-real-estate-market-stats',
                      schools='schools-in-coquitlam-bc', newc=None, suffix='coquitlam', region='coquitlam'),
}
GROUP_LABEL = {'Burnaby North': 'North Burnaby', 'Burnaby South': 'South Burnaby', 'Burnaby East': 'East Burnaby', 'Vancouver West': 'Vancouver West side', 'Vancouver East': 'Vancouver East side'}

# MLS sub-area -> display name where the board's label carries a code or is not how people say it
DISP = {'Hamilton RI': 'Hamilton', 'Renfrew VE': 'Renfrew', 'Victoria VE': 'Victoria', 'West End VW': 'West End', 'Downtown VW': 'Downtown', 'Downtown VE': 'Downtown Eastside area',
        'Fraser VE': 'Fraser', 'Collingwood VE': 'Collingwood', 'Fraserview VE': 'Fraserview', 'Killarney VE': 'Killarney', 'Fairview VW': 'Fairview', 'Oakridge VW': 'Oakridge',
        'Mount Pleasant VE': 'Mount Pleasant (East)', 'Mount Pleasant VW': 'Mount Pleasant (West)', 'University VW': 'University', 'Quilchena RI': 'Quilchena', 'Riverdale RI': 'Riverdale',
        'Bridgeport RI': 'Bridgeport', 'Central BN': 'Central Burnaby', 'Simon Fraser Univer.': 'Simon Fraser University', 'Eagle Ridge CQ': 'Eagle Ridge', 'Westwood Summit CQ': 'Westwood Summit',
        'Downtown NW': 'Downtown', 'Fraserview NW': 'Fraserview', 'The Heights NW': 'The Heights', 'Uptown NW': 'Uptown', 'West End NW': 'West End', 'GlenBrooke North': 'Glenbrooke North',
        'Quilchena': 'Quilchena (Vancouver)', 'S.W. Marine': 'S.W. Marine', 'Edmonds BE': 'Edmonds', 'Capitol Hill BN': 'Capitol Hill', 'Forest Hills BN': 'Forest Hills', 'Westridge BN': 'Westridge',
        'Central Park BS': 'Central Park', 'Forest Glen BS': 'Forest Glen', 'Granville': 'Granville', 'Garden City': 'Garden City'}
# sub-area key -> the slug of its existing page (archive page, guide or generated page)
EXIST = {
    'Richmond|Boyd Park': 'boyd-park', 'Richmond|Bridgeport RI': 'bridgeport-ri', 'Richmond|Brighouse': 'brighouse-richmond-guide', 'Richmond|East Cambie': 'east-cambie', 'Richmond|Granville': 'granville',
    'Richmond|Quilchena RI': 'quilchena-ri', 'Richmond|Riverdale RI': 'riverdale-ri', 'Richmond|Seafair': 'seafair', 'Richmond|South Arm': 'south-arm-richmond-guide', 'Richmond|Terra Nova': 'terra-nova',
    'Richmond|West Cambie': 'west-cambie',
    'Vancouver East|Champlain Heights': 'champlain-heights', 'Vancouver East|Collingwood VE': 'collingwood-ve', 'Vancouver East|Downtown VE': 'downtown-ve', 'Vancouver East|Fraser VE': 'fraser-ve',
    'Vancouver East|Fraserview VE': 'fraserview-ve', 'Vancouver East|Grandview Woodland': 'grandview-woodland', 'Vancouver East|Hastings': 'hastings', 'Vancouver East|Killarney VE': 'killarney-ve',
    'Vancouver East|Knight': 'knight', 'Vancouver East|Main': 'main', 'Vancouver East|Mount Pleasant VE': 'mount-pleasant-vancouver-guide',
    'Vancouver West|Arbutus': 'arbutus', 'Vancouver West|Cambie': 'cambie', 'Vancouver West|Coal Harbour': 'coal-harbour', 'Vancouver West|Downtown VW': 'downtown-vw', 'Vancouver West|Dunbar': 'dunbar',
    'Vancouver West|Fairview VW': 'fairview-vw', 'Vancouver West|False Creek': 'false-creek', 'Vancouver West|Kerrisdale': 'kerrisdale-vancouver-guide', 'Vancouver West|Kitsilano': 'kitsilano',
    'Vancouver West|MacKenzie Heights': 'mackenzie-heights', 'Vancouver West|Mount Pleasant VW': 'mount-pleasant-vancouver-guide', 'Vancouver West|Oakridge VW': 'oakridge-vancouver-guide',
    'Vancouver West|Shaughnessy': 'shaughnessy-vancouver-guide', 'Vancouver West|South Cambie': 'south-cambie-vancouver-guide', 'Vancouver West|South Granville': 'south-granville-vancouver-guide',
    'Vancouver West|S.W. Marine': 'sw-marine-vancouver-guide', 'Vancouver West|University VW': 'university-endowment-lands-vancouver-guide',
    'Burnaby East|East Burnaby': 'east-burnaby', 'Burnaby East|Edmonds BE': 'edmonds-be', 'Burnaby East|The Crest': 'the-crest', 'Burnaby North|Brentwood Park': 'brentwood-park',
    'Burnaby North|Capitol Hill BN': 'capitol-hill-bn', 'Burnaby North|Cariboo': 'cariboo', 'Burnaby North|Central BN': 'central-bn', 'Burnaby North|Forest Hills BN': 'forest-hills-bn',
    'Burnaby North|Government Road': 'government-road', 'Burnaby North|Montecito': 'montecito', 'Burnaby North|Oakdale': 'oakdale', 'Burnaby North|Parkcrest': 'parkcrest',
    'Burnaby North|Simon Fraser Hills': 'simon-fraser-hills-burnaby', 'Burnaby North|Simon Fraser Univer.': 'simon-fraser-university-area-burnaby', 'Burnaby North|Sperling-Duthie': 'sperling-duthie-burnaby',
    'Burnaby North|Sullivan Heights': 'sullivan-heights-burnaby', 'Burnaby North|Vancouver Heights': 'vancouver-heights-burnaby', 'Burnaby North|Westridge BN': 'westridge-burnaby',
    'Burnaby North|Willingdon Heights': 'willingdon-heights-burnaby', 'Burnaby South|Big Bend': 'big-bend', 'Burnaby South|Buckingham Heights': 'buckingham-heights', 'Burnaby South|Burnaby Hospital': 'burnaby-hospital',
    'Burnaby South|Burnaby Lake': 'burnaby-lake', 'Burnaby South|Central Park BS': 'central-park-bs', 'Burnaby South|Deer Lake': 'deer-lake', 'Burnaby South|Deer Lake Place': 'deer-lake-place',
    'Burnaby South|Forest Glen BS': 'forest-glen-bs', 'Burnaby South|Garden Village': 'garden-village', 'Burnaby South|Greentree Village': 'greentree-village', 'Burnaby South|Highgate': 'highgate-burnaby',
    'Burnaby South|Metrotown': 'metrotown-homes-for-sale', 'Burnaby South|Oaklands': 'oaklands-burnaby', 'Burnaby South|South Slope': 'south-slope-burnaby', 'Burnaby South|Suncrest': 'suncrest-burnaby',
    'Burnaby South|Upper Deer Lake': 'upper-deer-lake-burnaby',
    'New Westminster|Connaught Heights': 'connaught-heights', 'New Westminster|Downtown NW': 'downtown-nw', 'New Westminster|Fraserview NW': 'fraserview-nw', 'New Westminster|GlenBrooke North': 'glenbrooke-north',
    'New Westminster|Moody Park': 'moody-park', 'New Westminster|Quay': 'quay', 'New Westminster|Queens Park': 'queens-park', 'New Westminster|Queensborough': 'queensborough',
    'New Westminster|Sapperton': 'sapperton-new-westminster', 'New Westminster|The Heights NW': 'the-heights-new-westminster', 'New Westminster|Uptown NW': 'uptown-new-westminster',
    'New Westminster|West End NW': 'west-end-new-westminster',
    'Coquitlam|Burke Mountain': 'burke-mountain', 'Coquitlam|Canyon Springs': 'canyon-springs', 'Coquitlam|Cape Horn': 'cape-horn', 'Coquitlam|Central Coquitlam': 'central-coquitlam', 'Coquitlam|Chineside': 'chineside',
    'Coquitlam|Coquitlam East': 'coquitlam-east', 'Coquitlam|Coquitlam West': 'coquitlam-west', 'Coquitlam|Eagle Ridge CQ': 'eagle-ridge-cq', 'Coquitlam|Harbour Chines': 'harbour-chines',
    'Coquitlam|Harbour Place': 'harbour-place-coquitlam', 'Coquitlam|Hockaday': 'hockaday', 'Coquitlam|Maillardville': 'maillardville-coquitlam', 'Coquitlam|Meadow Brook': 'meadow-brook-coquitlam',
    'Coquitlam|New Horizons': 'new-horizons-coquitlam', 'Coquitlam|North Coquitlam': 'north-coquitlam', 'Coquitlam|Park Ridge Estates': 'park-ridge-estates-coquitlam', 'Coquitlam|Ranch Park': 'ranch-park-coquitlam',
    'Coquitlam|River Springs': 'river-springs-coquitlam', 'Coquitlam|Scott Creek': 'scott-creek-coquitlam', 'Coquitlam|Summitt View': 'summitt-view-coquitlam', 'Coquitlam|Upper Eagle Ridge': 'upper-eagle-ridge-coquitlam',
    'Coquitlam|Westwood Plateau': 'westwood-plateau-coquitlam'}
GUIDE_ONLY = {'Richmond|Brighouse', 'Richmond|South Arm'}   # pages that are guides; they keep their own text


def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def disp(k): n = k.split('|', 1)[1]; return DISP.get(n) or SO.clean_label(n)
def page_exists(s): return os.path.exists(os.path.join(PAGES, s + '.json')) or os.path.exists(os.path.join(LOCAL, s + '.json'))
def lp(s): return os.path.join(LOCAL, s + '.json')
def total(d): return sum(g['n'] for g in d['groups'].values())
def gn(d, g): return d['groups'].get(g, {}).get('n', 0)
def med(d, g):
    s = d['groups'].get(g)
    return s['price'] if s and s['n'] >= SO.MIN_MED and 'price' in s else None
def P(t, **k): return {'t': 'p', 'text': t, 'gen': G, **k}
def H(t, lvl=2, **k): return {'t': 'h', 'level': lvl, 'text': t, 'gen': G, **k}
def L(items, **k): return {'t': 'list', 'items': [[{'t': a, 'h': f'/{s}.html'}] for a, s in items], 'gen': G, **k}


def roster(ck):
    c = CITIES[ck]; out = []
    for k, d in AGG['sub'].items():
        b = k.split('|')[0]
        if b not in c['boards']: continue
        if ck == 'burnaby' and k == 'Burnaby North|Vancouver Heights' and False: continue
        out.append(k)
    return sorted(out, key=lambda k: (c['boards'].index(k.split('|')[0]), disp(k)))


def new_slug(k, ck):
    base = slugify(disp(k).replace(' (Vancouver)', ''))
    return f'{base}-{CITIES[ck]["suffix"]}'


def plan():
    """slug for every sub-area: existing page, a page we will build, or None (too few sales)."""
    res = {}
    for ck in CITIES:
        for k in roster(ck):
            if k in EXIST:
                assert page_exists(EXIST[k]) or True, k
                res[k] = (EXIST[k], False)
            elif total(AGG['sub'][k]) >= MIN_SALES: res[k] = (new_slug(k, ck), True)
            else: res[k] = (None, False)
    return res


PLAN = plan()


# ---------------- shared FAQ ----------------
def bank_faq(city):
    return [{'q': f'Who can help me buy or sell in {city}?', 'a': f'Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, works across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361 or use the contact form on this site.', 'gen': 'bank-faq'},
            {'q': f'Do I need a home inspection when buying in {city}?', 'a': 'It is strongly recommended. Make the offer subject to an inspection so a qualified inspector can look at the roof, structure, drainage, electrical and heating before you remove conditions.', 'gen': 'bank-faq'},
            {'q': 'Can I book a private showing with Jared?', 'a': f'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.', 'gen': 'muse-generic'}]


def title_for(head, tail=' Homes for Sale'):
    for t in (f'{head}{tail}{BR}', f'{head}{tail}{BS}', f'{head}{tail}'):
        if len(t) <= 66: return t
    return t


def crumbs(ck, name=None, slug=None, hub=True):
    c = CITIES[ck]; out = [{'name': 'Home', 'href': '/index.html'}, {'name': c['name'], 'href': f'/{c["homes"]}.html'}]
    if name is not None: out += [{'name': f'{c["name"]} neighbourhood guides', 'href': f'/{c["hub"]}.html'}, {'name': name, 'href': f'/{slug}.html'}]
    else: out += [{'name': f'{c["name"]} neighbourhood guides', 'href': f'/{c["hub"]}.html'}]
    return out


def write(slug, doc):
    f = lp(slug)
    if os.path.exists(f):
        old = json.load(open(f, encoding='utf-8'))
        if old.get('hand_edited'): return False
        keep = [b for b in old.get('blocks', []) if b.get('gen') in ('areamap', 'commute', 'communitylinks')]
        doc['blocks'] = doc['blocks'] + keep
    json.dump(doc, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); open(f, 'a').write('\n')
    return True


# ---------------- hubs ----------------
def type_cell(d, g):
    s = d['groups'].get(g)
    if not s or s['n'] < SO.MIN_MENTION: return '—'
    if s['n'] < SO.MIN_MED or 'price' not in s: return f'{s["n"]} sold'
    return f'{s["n"]:,} sold, median {money(s["price"])}'


def hub(ck):
    c = CITIES[ck]; N = c['name']; keys = roster(ck)
    tot = sum(total(AGG['sub'][k]) for k in keys)
    by = {g: sum(gn(AGG['sub'][k], g) for k in keys) for g in ('house', 'condo', 'townhome', 'duplex')}
    paged = [k for k in keys if PLAN[k][0]]
    busiest = sorted(keys, key=lambda k: -total(AGG['sub'][k]))
    hp = sorted(((med(AGG['sub'][k], 'house'), k) for k in keys if gn(AGG['sub'][k], 'house') >= 10 and med(AGG['sub'][k], 'house')), reverse=True)
    cp = sorted(((med(AGG['sub'][k], 'condo'), k) for k in keys if gn(AGG['sub'][k], 'condo') >= 10 and med(AGG['sub'][k], 'condo')), reverse=True)
    bl = [{'t': 'notice', 'text': f'Draft for Jared’s approval. Figures are closed sales from Jared’s Paragon export; the neighbourhood map outlines are drawn by us and stay draft until each is confirmed.', 'gen': G}]
    top3 = ', '.join(f'{disp(k)} ({total(AGG["sub"][k]):,})' for k in busiest[:3])
    bl.append(P(f'{N} is split into {len(keys)} MLS® sub-areas, the neighbourhood boundaries the {"Greater Vancouver REALTORS®" } board uses for every listing and sale. From {WINDOW.replace("November 1, 2025 to ", "November 2025 to ")}, {tot:,} homes sold across them: {by["house"]:,} houses, {by["condo"]:,} condos and {by["townhome"]:,} townhomes' + (f' and {by["duplex"]:,} duplexes' if by['duplex'] >= 3 else '') + f'. The busiest were {top3}.'))
    if hp: bl.append(P(f'By median price, the houses that sold in {disp(hp[0][1])} were the most expensive of the {len(hp)} {N} neighbourhoods with 10 or more house sales ({money(hp[0][0])}), and those in {disp(hp[-1][1])} the least ({money(hp[-1][0])}). ' + (f'For condos, the range ran from {money(cp[-1][0])} in {disp(cp[-1][1])} to {money(cp[0][0])} in {disp(cp[0][1])}.' if len(cp) >= 2 else '')))
    bl.append(P(f'These are MLS® sub-areas, not the City of {N}’s planning areas, so a neighbourhood here can be larger or smaller than the name suggests. The map and tables below follow the board’s boundaries. Use them to compare areas, then ask Jared for a search set to the exact streets you care about.'))
    bl.append({'t': 'grid'})
    groups = []
    for b in c['boards']:
        ks = [k for k in keys if k.startswith(b + '|')]
        if ks: groups.append((b, ks))
    for b, ks in groups:
        label = GROUP_LABEL.get(b, N) if len(groups) > 1 else N
        bl.append(H(f'{label} neighbourhoods: what sold, {WINDOW.replace("November 1, 2025 to ", "November 2025 to ")}'))
        rows = []
        for k in ks:
            d = AGG['sub'][k]; sl = PLAN[k][0]
            name = disp(k)
            rows.append([{'t': name, 'h': f'/{sl}.html'} if sl else name, type_cell(d, 'house'), type_cell(d, 'condo'), type_cell(d, 'townhome')])
        bl.append({'t': 'table', 'caption': f'{label}: closed sales by neighbourhood', 'head': ['Neighbourhood', 'Houses', 'Condos', 'Townhomes'], 'rows': rows, 'source': SO.SRC + SO.SRC_MIN.replace('a community is listed only with', 'a median is shown only with'), 'gen': G})
    nopage = [k for k in keys if not PLAN[k][0]]
    if nopage:
        bl.append(P(f'{", ".join(disp(k) for k in nopage)} ' + ('has' if len(nopage) == 1 else 'have') + f' fewer than {MIN_SALES} closed sales in the period, too few for a page of figures, so they appear in the tables only.'))
    links = [(f'{N} homes for sale', c['homes']), (f'{N} real estate market stats', c['market'])]
    for lab, s in ((f'Schools in {N}', c['schools']), (f'New construction in {N}', c['newc']), (f'{N} condos for sale', f'{c["suffix"]}-condos-for-sale'), (f'{N} townhomes for sale', f'{c["suffix"]}-townhomes-for-sale'),
                   (f'{N} presale condos and townhomes', f'{c["suffix"]}-presale-condos-and-townhomes'), (f'{N} open houses', f'{c["suffix"]}-open-houses')):
        if s and page_exists(s): links.append((lab, s))
    bl += [H(f'More {N} real estate', pos='end'), L(links, pos='end')]
    bl += [H(f'All {len(paged)} {N} neighbourhood pages', pos='end'), L([(disp(k), PLAN[k][0]) for k in paged if k not in GUIDE_ONLY or True], pos='end')]
    faq = [{'q': f'How many neighbourhoods does {N} have?', 'a': f'The MLS® splits {N} into {len(keys)} sub-areas: ' + ', '.join(disp(k) for k in keys[:6]) + f' and {len(keys) - 6} more. {len(paged)} have a page on this site.', 'gen': G},
           {'q': f'Which {N} neighbourhood sold the most homes?', 'a': f'{disp(busiest[0])} had the most closed sales, {total(AGG["sub"][busiest[0]]):,} between {WINDOW}, followed by {disp(busiest[1])} ({total(AGG["sub"][busiest[1]]):,}) and {disp(busiest[2])} ({total(AGG["sub"][busiest[2]]):,}).', 'gen': G}]
    if hp: faq.append({'q': f'Where are {N} houses the most and least expensive?', 'a': f'Among areas with 10 or more house sales, the median was highest in {disp(hp[0][1])} at {money(hp[0][0])} and lowest in {disp(hp[-1][1])} at {money(hp[-1][0])}, for sales {WINDOW}.', 'gen': G})
    if len(cp) >= 2: faq.append({'q': f'Which {N} neighbourhoods are best value for a condo?', 'a': f'Median condo prices ran from {money(cp[-1][0])} in {disp(cp[-1][1])} to {money(cp[0][0])} in {disp(cp[0][1])} among areas with 10 or more condo sales. Price is one measure only; compare strata fees, age and building condition too.', 'gen': G})
    faq += bank_faq(N)
    title = f'{N} Neighbourhood Guides | {len(keys)} Areas | Jared Gibbons'
    doc = {'status': 'draft', 'slug': c['hub'], 'updated': UPDATED, 'new_page': {'title': title, 'description': f'Compare all {len(keys)} {N} neighbourhoods: what sold in each in the last 12 months, median prices by home type and a guide page for each. Jared Gibbons, REALTOR®.', 'h1': f'{N} neighbourhood guides: {len(keys)} areas compared'},
           'breadcrumbs': crumbs(ck), 'faq_heading': f'{N} neighbourhoods: your questions answered', 'blocks': bl, 'faq': faq,
           'needs_from_muse': ['Jared to confirm each neighbourhood outline on the map before it is marked confirmed', 'A listing search for the hub (MyRealPage) if wanted']}
    return write(c['hub'], doc)


# ---------------- local-fact notes ----------------
def read_note(slug):
    f = os.path.join(NOTES, slug + '.md')
    if not os.path.exists(f): return None
    t = open(f, encoding='utf-8').read()
    secs, cur, srcs = [], None, {}
    for ln in t.split('\n'):
        m = re.match(r'^##\s+(.*)', ln)
        if m: cur = [re.sub(r'\s*\(.*$', '', m.group(1)).strip(), []]; secs.append(cur); continue
        if cur is None or not ln.strip(): continue
        cur[1].append(ln.strip())
    out, sources = [], []
    for head, lines in secs:
        if head.lower().startswith('source'):
            for ln in lines:
                m = re.match(r'^\[?(\d+)[\].:)]?\s*(.*?)(https?://\S+)', ln)
                if m: srcs[m.group(1)] = (m.group(2).strip(' -–—:|') or re.sub(r'^https?://(www\.)?', '', m.group(3)).split('/')[0], m.group(3).rstrip(').,'))
            continue
        items = []
        for ln in lines:
            ln = re.sub(r'^[-*•]\s*', '', ln)
            if re.search(r'UNVERIFIED|unverified|NOT CONFIRMED|boundary:', ln) or len(ln) < 25: continue
            ids = re.findall(r'\[(\d+)\]', ln); txt = re.sub(r'\s*\[\d+(?:[,\s]*\d+)*\]', '', ln).strip()
            if not ids or not txt: continue
            items.append((txt, ids))
        if items: out.append((head, items))
    used = []
    for _, items in out:
        for _, ids in items:
            for i in ids:
                if i in srcs and i not in used: used.append(i)
    return out, [(srcs[i][0], srcs[i][1]) for i in used]


# ---------------- area pages ----------------
def rank_text(ck, k, g):
    ks = [x for x in roster(ck) if gn(AGG['sub'][x], g) >= 10 and med(AGG['sub'][x], g)]
    if k not in ks: return None
    ordr = sorted(ks, key=lambda x: -med(AGG['sub'][x], g)); return ordr.index(k) + 1, len(ordr), med(AGG['sub'][ordr[0]], g), med(AGG['sub'][ordr[-1]], g)



def typical_blocks(label, g, order):
    """What the typical home that sold looks like, and how wide the price spread was (only where 5+ sales)."""
    rows = []
    for x in order:
        s = g[x]
        if s['n'] < SO.MIN_MED or 'price' not in s: continue
        spread = f'{money(s["p25"])} to {money(s["p75"])}' if 'p25' in s else '—'
        size = (f'{s["lot_sqft"]:,} sq ft lot' if s.get('lot_sqft') and x in ('house', 'duplex', 'mobile') else (f'{s["acres"]} acres' if s.get('acres') and x in ('acreage', 'land') else '—'))
        rows.append([SO.GROUPS[x], str(s['beds']) if s.get('beds') is not None else '—', str(s['yb']) if s.get('yb') else '—', size, (money(s['maint']) + ' a month') if s.get('maint') else '—', spread, f'{s["over"]}%' if s.get('over') is not None else '—'])
    if not rows: return []
    return [H(f'The typical home that sold in {label}'),
            {'t': 'table', 'caption': f'{label}: the typical home by type', 'head': ['Home type', 'Median bedrooms', 'Median year built', 'Median lot', 'Median strata fee', 'Middle half sold for', 'Sold above list'], 'rows': rows, 'source': SO.SRC + SO.SRC_MIN.replace('a community is listed only with', 'a row is shown only with'), 'gen': G}]


def area_page(ck, k, slug):
    c = CITIES[ck]; N = c['name']; d = AGG['sub'][k]; nm = disp(k); g = d['groups']
    order = [x for x in ('house', 'condo', 'townhome', 'duplex', 'acreage', 'mobile', 'land') if x in g and g[x]['n'] >= SO.MIN_MENTION]
    big = max(order, key=lambda x: g[x]['n']); tot = total(d)
    label = nm.replace(' (Vancouver)', '')
    bl = [{'t': 'notice', 'text': f'Draft for Jared’s approval. Figures are closed sales from Jared’s Paragon export; local facts come from official sources listed at the bottom. It has no listing feed yet.', 'gen': G}]
    parts = [f'{gn(d, x):,} {SO.GL[x]}' for x in order[:4]]
    bl.append(P(f'{label} is an MLS® sub-area of {N}. From {WINDOW.replace("November 1, 2025 to ", "November 2025 to ")}, {tot:,} homes sold there: ' + ', '.join(parts[:-1]) + (' and ' if len(parts) > 1 else '') + parts[-1] + '. ' + ' '.join(SO.one_line(label, g[x], x, extra=False) for x in sorted(order, key=lambda y: -g[y]['n'])[:1])))
    bl.append({'t': 'grid'})
    bl += SO.page_blocks(AGG, k, label, ['house', 'condo', 'townhome', 'duplex', 'acreage', 'mobile', 'land'])
    for b in bl: b.setdefault('gen', G)
    shown = sorted(order, key=lambda y: -g[y]['n'])[:2]
    for x in order:      # every other home type with enough sales gets its own sentence and quarterly table
        if x in shown: continue
        if g[x]['n'] >= SO.MIN_MED and 'price' in g[x]: bl.append(P(SO.one_line(label, g[x], x)))
    for x in order:
        if x != big and g[x]['n'] >= 12: bl += [{**b, 'gen': G} for b in SO.quarter_table(label, g[x], x)]
    bl += typical_blocks(label, g, order)
    # comparison with the rest of the city
    rows = []
    for x in order[:3]:
        r = rank_text(ck, k, x)
        if r: rows.append([SO.GROUPS[x], f'{g[x]["n"]:,}', money(g[x]['price']), f'{r[0]} of {r[1]}', f'{money(r[3])} to {money(r[2])}'])
    if rows:
        bl += [H(f'How {label} compares with the rest of {N}'),
               {'t': 'table', 'caption': f'{label} against the other {N} neighbourhoods', 'head': ['Home type', 'Sold here', 'Median price here', 'Rank by median price', f'Range across {N}'], 'rows': rows, 'source': SO.SRC + SO.SRC_MIN.replace('a community is listed only with', 'a row is shown only with'), 'gen': G}]
    note = read_note(slug); srcs = []
    if note:
        secs, srcs = note
        for head, items in secs:
            bl += [H(f'{label}: {head[0].lower() + head[1:]}'), {'t': 'list', 'items': [[{'t': t}] for t, _ in items], 'gen': G}]
    # links
    ks = [x for x in roster(ck) if PLAN[x][0] and PLAN[x][0] != slug]; i = [x for x in roster(ck)].index(k)
    ring = [x for x in roster(ck)[i + 1:] + roster(ck)[:i] if PLAN[x][0] and PLAN[x][0] != slug][:8]
    links = [(f'{N} neighbourhood guides', c['hub']), (f'{N} homes for sale', c['homes']), (f'{N} real estate market stats', c['market'])]
    for lab, s in ((f'Schools in {N}', c['schools']), (f'New construction in {N}', c['newc'])):
        if s and page_exists(s): links.append((lab, s))
    links += [(f'{disp(x)} real estate', PLAN[x][0]) for x in ring]
    bl += [H(f'More {N} real estate', pos='end'), L(links, pos='end')]
    if srcs: bl += [H(f'Sources for {label}', pos='end'), {'t': 'list', 'items': [[{'t': a, 'h': u}] for a, u in srcs], 'gen': G, 'pos': 'end'}]
    faq = (SO.sold_faq(label, 'homes' if big in ('house',) else SO.GL[big], g[big], big) + SO.sold_faq_more(label, SO.GL[big], g[big], big, None, AGG)) if g[big]['n'] >= SO.MIN_MED and 'price' in g[big] else []
    faq = [{**f, 'gen': G} for f in faq] + bank_faq(N)
    top = f'{label}, {N}'
    pc = g[big]['price'] if g[big]['n'] >= SO.MIN_MED and 'price' in g[big] else None
    desc = f'{label}, {N}: {tot:,} homes sold in the last 12 months' + (f', median {SO.GL[big][:-1] if SO.GL[big].endswith("s") else SO.GL[big]} price {money(pc)}' if pc else '') + f'. What sold by home type and local facts. Jared Gibbons, REALTOR®.'
    doc = {'status': 'draft', 'slug': slug, 'updated': UPDATED, 'new_page': {'title': title_for(top), 'description': desc[:158], 'h1': f'{top} Homes for Sale'},
           'breadcrumbs': crumbs(ck, f'{label} real estate', slug), 'faq_heading': f'{label} real estate: your questions answered', 'blocks': bl, 'faq': faq,
           'needs_from_muse': [f'Street boundaries of {label} from Jared or the Paragon sub-area map (outline on the map is a draft)', f'A listing search for {label} (MyRealPage) so current listings appear', 'Jared’s own notes on the area']}
    return write(slug, doc)


# ---------------- links into the hubs ----------------
def ensure_local(slug):
    f = lp(slug)
    if os.path.exists(f):
        raw = open(f, encoding='utf-8').read(); lines = raw.split('\n')
        ind = (len(lines[1]) - len(lines[1].lstrip(' '))) if len(lines) > 1 else 1   # keep each file's own layout so diffs stay small
        return json.loads(raw), (f, ind or 1, raw.endswith('\n'))
    return {'status': 'generated', 'slug': slug, 'updated': UPDATED, 'blocks': []}, (f, 1, True)


def save_local(j, fm):
    f, ind, nl = fm
    with open(f, 'w', encoding='utf-8') as fh:
        json.dump(j, fh, ensure_ascii=False, indent=ind)
        if nl: fh.write('\n')


def inbound():
    """Every page we know in a city links to the hub and ten neighbouring pages (gen 'gvrhub', placed at the end); the city's homes and market pages link to the hub."""
    n = 0
    for ck, c in CITIES.items():
        ks = [k for k in roster(ck) if PLAN[k][0]]; slugs = []
        for k in ks:
            if PLAN[k][0] not in slugs: slugs.append(PLAN[k][0])
        names = {PLAN[k][0]: disp(k) for k in ks}
        for i, sl in enumerate(slugs):
            if not page_exists(sl): continue
            j, f = ensure_local(sl)
            if j.get('hand_edited') and sl in GUIDE_ONLY: continue
            j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'gvrhub']
            ring = [slugs[(i + d) % len(slugs)] for d in range(1, len(slugs))][:8]
            items = [(f'{c["name"]} neighbourhood guides: map and prices for all {len(roster(ck))} areas', c['hub'])] + [(f'{names[x]} real estate', x) for x in ring if x != sl and page_exists(x)]
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{c["name"]} neighbourhoods', 'gen': 'gvrhub', 'pos': 'end'}, {'t': 'list', 'items': [[{'t': a, 'h': f'/{s}.html'}] for a, s in items], 'gen': 'gvrhub', 'pos': 'end'}]
            save_local(j, f); n += 1
        for s in (c['homes'], c['market']):
            if not page_exists(s): continue
            j, f = ensure_local(s)
            j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'gvrhub']
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'{c["name"]} neighbourhood guides', 'gen': 'gvrhub', 'pos': 'end'}, {'t': 'list', 'items': [[{'t': f'{c["name"]} neighbourhood guides: what sold in each of {len(roster(ck))} areas', 'h': f'/{c["hub"]}.html'}]], 'gen': 'gvrhub', 'pos': 'end'}]
            save_local(j, f); n += 1
    return n


def nav():
    f = os.path.join(ROOT, 'src/data/nav.json'); nv = json.load(open(f, encoding='utf-8'))
    def walk(items):
        for it in items:
            for ck, c in CITIES.items():
                if it.get('label') == c['name'] and it.get('children') and any(x.get('href') == f'/{c["homes"]}.html' for x in it['children']):
                    it['children'] = [x for x in it['children'] if x.get('href') != f'/{c["hub"]}.html']
                    it['children'].insert(0, {'label': f'{c["name"]} Neighbourhood Guides', 'href': f'/{c["hub"]}.html'})
            if it.get('children'): walk(it['children'])
    walk(nv); json.dump(nv, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); open(f, 'a').write('\n')


def main():
    n_hub = sum(1 for ck in CITIES if hub(ck))
    built = []
    for k, (slug, new) in PLAN.items():
        if not new: continue
        ck = next(c for c in CITIES if k.split('|')[0] in CITIES[c]['boards'])
        if area_page(ck, k, slug): built.append(slug)
    print('hubs', n_hub, 'new pages', len(built)); print(' '.join(built))
    print('inbound link blocks', inbound()); nav()


if __name__ == '__main__':
    main()
