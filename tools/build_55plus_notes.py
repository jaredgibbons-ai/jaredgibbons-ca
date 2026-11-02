"""Community 55+ pages, the BC 55+ strata rules hub and the mobile-home guide section, built from Jared's verified local notes
(docs/research/local-notes-55plus/*.md, researched 2026-11-01; batch 2 of 4 not yet received).

A community gets its own page only if its note verifies at least one 55+ home you can BUY (strata, bare-land strata, co-op, life lease or a 55+ manufactured-home park).
Communities whose note found no buyable 55+ stock get no page. Text is the notes' own findings, URLs removed from the prose and listed once in a Sources section
(listing-level pages that identify a unit are not listed); MLS numbers are stripped. The provincial rules that repeat in every note live once on /bc-55-plus-strata-rules.html.
    python3 -I tools/build_55plus_notes.py        (run after build_gap_pages / build_poco_55plus / build_muse_faq)"""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
NOTES = os.path.join(ROOT, 'docs/research/local-notes-55plus')
LOCAL = os.path.join(ROOT, 'src/data/local'); PAGES = os.path.join(ROOT, 'src/data/pages')
G = 'n55'; HUB = 'bc-55-plus-strata-rules'
CITY = {'central-abbotsford': 'Abbotsford', 'abbotsford-west': 'Abbotsford', 'poplar': 'Abbotsford', 'ladner-elementary': 'Ladner', 'neilsen-grove': 'Ladner'}
FOLD = {'cliff-drive': 'tsawwassen-central', 'pebble-hill': 'tsawwassen-central', 'chelsea-park': 'ambleside', 'caulfeild': 'ambleside', 'altamont': 'ambleside'}  # no 55+ building of their own: folded into the page of the building they point to
MERGE = {'chilliwack-55-plus-neighbourhood-guide': ('Chilliwack', ['chilliwack-downtown', 'chilliwack-proper-east', 'chilliwack-proper-south', 'chilliwack-proper-west'])}
MERGED = {n for _, (_, ns) in MERGE.items() for n in ns}
SKIP = {'canyon-springs': 'the note covers the North Vancouver complex of that name; this site\'s Canyon Springs is the Coquitlam community'}
CITY_55 = {  # community -> existing city-level 55+ page(s) that should list it
 'surrey': ['surrey-55-plus-homes-for-sale'], 'coquitlam': ['coquitlam-55-plus-homes-for-sale'], 'burnaby': ['burnaby-55-plus-homes-for-sale'],
 'abbotsford': ['abbotsford-55-plus-condos-for-sale', 'abbotsford-55-plus-townhomes-for-sale'], 'langley': ['langley-55-plus-condos-for-sale', 'langley-55-plus-townhomes-for-sale'],
 'pitt meadows': ['pitt-meadows-55-plus-condos-for-sale', 'pitt-meadows-55-plus-townhomes-for-sale'],
 'maple ridge': ['maple-ridge-55-plus-condos-for-sale', 'maple-ridge-55-plus-townhomes-for-sale'],
 'chilliwack': ['chilliwack-55-plus-condos-for-sale', 'chilliwack-55-plus-townhomes-for-sale'],
 'south surrey': ['south-surrey-white-rock-55-plus-condos-for-sale', 'south-surrey-white-rock-55-plus-townhomes-for-sale'],
}
TOPIC = re.compile(r'(under|over)-|open-houses|foreclosure|farms|lots-land|mobile-homes|calculator|^blog$|^contact$|our-listings|sold-properties|newsletter|marketing|commercial|land-use|landplans|home-evaluation|neighbourhood-guides|school-catchments|luxury|acreages|pad-rental|homes-for-sale$|first-time')
PARK_PAGES = {'surrey-mobile-homes': 'surrey-mobile-homes', 'south-surrey-mobile-homes': 'south-surrey-mobile-homes', 'chilliwack-mobile-homes': 'chilliwack-mobile-homes',
              'mission-mobile-homes': 'mission-mobile-homes', 'maple-ridge-mobile-homes': 'maple-ridge-mobile-homes', 'cost-of-mobile-home-pad-rental-fees-in-langley': 'cost-of-mobile-home-pad-rental-fees-in-langley'}
SHARED_Q = re.compile(r"under 55.*(investment|parent)|spouse is under 55|rent out (a|my) unit|resale buyer pool", re.I)
SHARED_LEAD = ('Only 55+ age bylaws', 'The bylaw restricts who', 'Built-in exemptions', 'Rental-restriction bylaws')
DROP_URL = re.compile(r'R[23]\d{6}|plsrealestate|condos\.ca/.*unit|zolo\.ca|estateblock|realtor\.ca|soldbycraig|zealty|rodfriesen|rew\.ca/properties|/listing|/property/|PropertyDetails|-mls_|surreytownhouse\.com/buildings/view|rentitfurnished|apartments\.com|mhbo\.com|housesigma|point2|strata\.ca/listing|bcrealestatefinder', re.I)


NOTE_REF = re.compile(r"\b(?:see|in) (?:[\w' ]{0,40} )?Section [1-5]\b")
DROP_SENT = re.compile(r"^Sources?:|building entries|base guide|\broundup\b|\bthe (?:note|brief)\b|\b\d[\d,]* (?:attached|detached|active) (?:listings?|sales?)|listings? (?:versus|vs\.?) |\bParagon\b|research file|in this pass|\broster\b|\d+ active\b|active / \d+ sold|\d+ of the city's \d+ active", re.I)


def clean(s):
    s = re.sub(r'\s*(?:[,;]|\band\b|\bor\b)?\s*https?://\S+', '', s)
    s = re.sub(r'\s*(?:\band\b\s+)?[^.]*?\S*[&?]\w+=\S*', '', s)
    s = re.sub(r'\s*(?:\band\b\s+)?~/\S+', '', s)
    s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
    s = re.sub(r'\s*\((?:[^()]*?[;,] ?)?(?:see|in) [^()]*Section [1-5][^()]*\)', '', s)
    s = re.sub(r'\s*[;:,]? see [^.()]*Section [1-5]\b', '', s)
    s = re.sub(r'\s*\((?:see )?Sections? [1-5](?:[^()]*)\)', '', s)
    s = re.sub(r'\b(?:Read|read|See|see)[^.:]{0,60}Section [1-5]:\s*', '', s)
    s = re.sub(r',? Section [1-5]\b(?![\d.]\d)', '', s)
    s = re.sub(r'\(?\bMLS R\d{7}, ?', '(', s); s = re.sub(r'\s*\(MLS R\d{7}\)', '', s); s = re.sub(r'\bMLS R\d{7}\b', 'MLS®', s); s = re.sub(r'\bR[23]\d{6}\b', '', s)
    sents = re.split(r'(?<=[.!?])\s+', s.strip())
    sents = [x for x in sents if not DROP_SENT.search(x) and not NOTE_REF.search(x)]
    s = ' '.join(sents)
    s = re.sub(r'\(\s*[,;\s]*\)', '', s); s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\b(and|or)(\s+(and|or))+\b', r'\1', s)
    s = re.sub(r'(?:\s+(?:and|or)|[;,:])\s*$', '', s).strip()
    s = re.sub(r'(?<=[.!?])\s+(?:and|or)\s*$', '', s).strip()
    s = re.sub(r'\s+([.,;])', r'\1', s)
    s = re.sub(r':\s*(?=,)', '', s)
    return s


def urls(s): return [u.rstrip('.,);') for u in re.findall(r'https?://\S+', s)]


def parse(path):
    t = open(path, encoding='utf-8').read(); lines = t.split('\n')
    title = lines[0][2:].strip(); sec = {}; grp = None; cur = None
    for ln in lines[1:]:
        m = re.match(r'^## (\d)\.', ln)
        if m: cur = int(m.group(1)); sec[cur] = {}; grp = '_'; sec[cur][grp] = []; continue
        m = re.match(r'^### (.*)', ln)
        if m and cur: grp = m.group(1).strip(); sec[cur][grp] = []; continue
        if ln.startswith('- ') and cur: sec[cur].setdefault(grp, []).append(ln[2:])
    return title, sec, t


def bullets(sec, n): return [b for g in sec.get(n, {}).values() for b in g]
def split_bold(b):
    m = re.match(r'\*\*(.*?)\*\*\s*(.*)', b)
    return (m.group(1).strip().rstrip('.:'), m.group(2)) if m else (None, b)
def real(b): return not re.match(r'(\*\*)?None verified|None found|None\b', b) and not re.search(r'^(\*\*)?[^.]{0,40}\bnone verified', b, re.I)


def H(t, l=2, **k): return {'t': 'h', 'level': l, 'text': t, 'gen': G, **k}
def P(t, **k): return {'t': 'p', 'text': t, 'gen': G, **k}
def LI(items):
    seen, out = set(), []
    for i in items:
        if i and i not in seen: seen.add(i); out.append(i)
    return {'t': 'list', 'items': [[{'t': i}] for i in out], 'gen': G}
def LK(items): return {'t': 'list', 'items': [[{'t': a, 'h': h}] for a, h in items], 'gen': G}


def src_links(all_urls, skip=()):
    out, seen = [], set()
    for u in all_urls:
        if u in seen or DROP_URL.search(u) or any(x in u for x in skip): continue
        seen.add(u); out.append(u)
    res = []
    for u in out:
        d = re.sub(r'^www\.', '', u.split('/')[2]); seg = [x for x in re.split(r'[/?#]', u.split('/', 3)[3] if u.count('/') >= 3 else '') if x]
        seg = [x for x in seg if not re.fullmatch(r'[\d_%A-Za-z]{0,3}|index\.\w+|page\.cfm|main|attachments|Files|default|files|wp-content|uploads|sites|\d+', x)]
        last = re.sub(r'\.(pdf|html?|php)$', '', seg[-1], flags=re.I) if seg else ''
        last = re.sub(r'%\w\w', ' ', last); last = re.sub(r'[-_+=]+', ' ', last).strip()
        lab = d + (' · ' + last[:48] if last and not re.fullmatch(r'[\d\s.]*', last) else '')
        res.append((lab, u))
    labs = {}; fin = []
    for l, u in res:
        labs[l] = labs.get(l, 0) + 1; fin.append((l if labs[l] == 1 else f'{l} ({labs[l]})', u))
    return fin[:24]


def exists(slug): return os.path.exists(f'{PAGES}/{slug}.json') or os.path.exists(f'{LOCAL}/{slug}.json')
def save(slug, d):
    with open(f'{LOCAL}/{slug}.json', 'w', encoding='utf-8') as f: json.dump(d, f, indent=2, ensure_ascii=False); f.write('\n')
def load(slug): return json.load(open(f'{LOCAL}/{slug}.json', encoding='utf-8')) if os.path.exists(f'{LOCAL}/{slug}.json') else None


def name_city(slug, title):
    head = title.split(' — ')[0].strip()
    m = re.match(r'(.*?)\s*\((.*)\)$', head)
    if m: name, city = m.group(1), m.group(2)
    elif ',' in head: name, city = [x.strip() for x in head.rsplit(',', 1)]
    else: name, city = head, CITY.get(slug, '')
    city = re.sub(r'^(City|District|Township) of ', '', city).strip()
    return name, city


def J(b):
    nm, rest = split_bold(b); nm, rest = clean(nm), clean(rest)
    return f'{nm}{rest}' if rest[:1] in ',;.' else f'{nm}: {rest}'


def kind(g):
    gl = g.lower()
    if 'manufactured' in gl or 'pad-rental' in gl or 'mobile' in gl: return 'park'
    if 'life lease' in gl: return 'life'
    if 'co-op' in gl or 'membership' in gl or 'buyable' in gl: return 'member'
    if 'strata' in gl: return 'strata'
    return 'own'


def build_community(path, written):
    slug0 = os.path.basename(path).replace('-55-plus-homes-2026-11-01.md', '')
    if slug0 in SKIP or slug0 in ('how-to-buy-a-mobile-home-in-bc', 'port-coquitlam') or TOPIC.search(slug0) or slug0 in FOLD or slug0 in MERGED: return
    title, sec, raw = parse(path)
    buy = []; other = []
    for g, bs in sec.get(2, {}).items():
        gl = g.lower()
        isoth = gl.startswith(('verified 55+ rental', 'retirement', 'subsidized', 'the chartwell')) or '(not ownership' in gl or 'not townhouse' in gl
        isbuy = (gl.startswith(('verified', 'life lease', 'pad-rental', 'co-operative', 'manufactured-home parks')) and not isoth
                 and 'elsewhere' not in gl and 'roster context' not in gl and 'checked' not in gl)
        for b in bs:
            if not real(b) or not b.startswith('**'): continue
            (buy if isbuy else other if isoth else []).append((g, b))
    if not buy: return
    name, city = name_city(slug0, title); slug = f'{slug0}-55-plus-homes-for-sale'
    if exists(slug) and not (load(slug) or {}).get('n55_page'): print('skip (page exists)', slug); return
    disp = f'{name}, {city}' if city and city.lower() not in name.lower() and name.lower() not in city.lower() else name
    names = [split_bold(b)[0].split(' — ')[0].split(' (')[0] for _, b in buy]
    nl = names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1] if len(names) <= 4 else ', '.join(names[:4]) + f' and {len(names) - 4} more'
    nl = nl.replace(', ' + 'and ', ' and ')
    KN = {'strata': 'strata', 'park': 'manufactured-home park', 'life': 'life lease', 'member': 'co-op or membership', 'own': 'ownership'}
    kinds = [KN[k] for k in dict.fromkeys(kind(g) for g, _ in buy)]
    kt = kinds[0] if len(kinds) == 1 else ', '.join(kinds[:-1]) + ' and ' + kinds[-1]
    others = sorted({'rental' if g.lower().startswith('verified 55+ rental') else 'retirement residence or care' if g.lower().startswith(('retirement', 'the chartwell')) else 'subsidized rental' for g, _ in other})
    intro = f'In {disp}, the 55+ homes you can buy are {nl}' + (f' ({kt})' if kt else '') + '.' + (f' The other seniors housing here, which you cannot buy into, is {", ".join(others[:-1]) + " and " + others[-1] if len(others) > 1 else others[0]}.' if others else '') + ' This page names each building, says what type it is and what the sources show, and covers local rules and the questions buyers ask. Anything no source states is marked unconfirmed.'
    bl = [{'t': 'notice', 'text': 'Draft for Jared\'s approval. Written from Jared\'s verified local notes (researched November 1, 2026). Listing-stated figures are labelled; unconfirmed items say so. No live feed filtered to 55+ homes yet.', 'gen': G},
          P(intro), {'t': 'grid', 'gen': G}]
    groups = {}
    for g, b in buy: groups.setdefault(g, []).append(b)
    for g, bs in groups.items():
        gl = g.lower()
        k = kind(g)
        h = {'strata': f'55+ strata buildings you can buy in {name}', 'park': f'55+ manufactured-home parks in {name}', 'life': f'Life lease residences in {name} (an occupancy right, not strata)',
             'member': f'55+ co-op and membership housing in {name} (not strata)', 'own': f'55+ ownership in {name}'}[k]
        bl.append(H(h))
        for b in bs:
            nm, rest = split_bold(b); tx = clean(rest)
            if nm and tx: bl += [H(clean(nm), 3), P(tx)]
    if other:
        bl.append(H(f'Rental, care and subsidized seniors housing in {name} (not for sale)'))
        bl.append(LI([J(b) for _, b in other if clean(split_bold(b)[1])]))
    s1 = [clean(b) for b in bullets(sec, 1) if real(b)]
    s1 = [x for x in s1 if x]
    if s1: bl += [H(f'Streets, schools and getting around {name}'), LI(s1)]
    s3 = [b for b in bullets(sec, 3) if real(b) and not split_bold(b)[0].startswith(SHARED_LEAD)]
    bl += [H(f'Local rules and plans in {name}')]
    if s3: bl.append(LI([J(b) if split_bold(b)[0] else clean(b) for b in s3 if clean(b)]))
    bl.append(P('The BC rules on 55+ age bylaws, who may own and who may live in a unit, the exemptions and rentals apply in every strata and are explained once, with sources, on the BC 55+ strata rules page.'))
    bl.append(LK([('BC 55+ strata rules', f'/{HUB}.html')]))
    s5 = [clean(b) for b in bullets(sec, 5) if real(b)]
    s5 = [x for x in s5 if x]
    if s5: bl += [H(f'Good to know about {name}'), LI(s5)]
    allu = [u for n in (1, 2, 3, 4, 5) for b in bullets(sec, n) for u in urls(b)]
    sl = src_links(allu, skip=('age-restriction-bylaws', 'changes-to-legislation', '2023HOUS0038'))
    if sl: bl += [H('Sources'), P('Facts on this page come from these public sources, read on November 1, 2026. Listing-level pages are not listed.'), LK(sl)]
    comm = slug0 if exists(slug0) else None; guide = f'{slug0}-guide' if exists(f'{slug0}-guide') else None
    mk = [(f'{name} real estate', f'/{comm}.html')] if comm else []
    mk += [(f'{name} neighbourhood guide', f'/{guide}.html')] if guide else []
    csl = [c for c in (CITY_55.get(city.lower().replace('-', ' ')) or [])]
    mk += [(f'{city} 55+ homes for sale', f'/{csl[0]}.html')] if csl and exists(csl[0]) else []
    mk += [('BC 55+ strata rules', f'/{HUB}.html'), ('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Contact Jared', '/contact.html')]
    bl += [H(f'More {name} real estate', pos='end'), {**LK(mk), 'pos': 'end'}]
    faq = []
    for b in bullets(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if not m: continue
        q, a = m.group(1).strip(), clean(m.group(2))
        if a and not SHARED_Q.search(q): faq.append({'q': q, 'a': a})
    if len(faq) < 5:
        for b in bullets(sec, 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
            if m and SHARED_Q.search(m.group(1)) and len(faq) < 5 and clean(m.group(2)): faq.append({'q': m.group(1).strip(), 'a': clean(m.group(2))})
    first = names[0]
    desc = f'{disp} 55+ homes: {", ".join(names[:3])}, what is rental or care, local rules and buyer questions. Jared Gibbons, REALTOR®.'
    ttl = f'{disp} 55+ Homes for Sale'; ttl = ttl + ' | Jared Gibbons' if len(ttl) + 16 <= 66 else ttl
    d = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'n55_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq, 'faq_heading': f'{name} 55+ homes: your questions answered',
         'new_page': {'title': ttl[:70], 'description': desc[:158], 'h1': f'{name} 55+ Homes for Sale | {city} Real Estate' if city else f'{name} 55+ Homes for Sale'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': f'{name}', 'href': f'/{comm}.html' if comm else '/index.html'}, {'name': '55+ homes', 'href': f'/{slug}.html'}],
         'needs_from_muse': [f'Jared’s own notes on the {name} 55+ buildings: how units sell, what buyers ask', 'Unit counts and years built marked unconfirmed in the sources', 'Live listing feed filtered to 55+ homes']}
    save(slug, d); written.append((slug, name, city, comm)); print('wrote', slug, len(bl), 'blocks', len(faq), 'faq')


def build_hub():
    title, sec, raw = parse(os.path.join(NOTES, 'east-newton-55-plus-homes-2026-11-01.md'))
    rules = [b for b in bullets(sec, 3) if split_bold(b)[0] and split_bold(b)[0].startswith(SHARED_LEAD)]
    allf = {}
    for f in glob.glob(f'{NOTES}/*.md'):
        _, s, _ = parse(f)
        for b in bullets(s, 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
            if m and SHARED_Q.search(m.group(1)) and 'elsewhere' not in m.group(1): allf.setdefault(re.sub(r'\W+', ' ', m.group(1).lower())[:40], (m.group(1).strip(), b))
    bl = [{'t': 'notice', 'text': 'Draft for Jared\'s approval. Built from the provincial pages named under Sources, read November 1, 2026.', 'gen': G},
          P('If you are buying a 55+ home in BC, these provincial rules apply in every strata, whichever city the building is in. They decide who can live in a unit, who can own it, who is exempt from the age limit and whether the unit can be rented. A manufactured-home park is different: it is governed by park tenancy law, not by strata bylaws.'),
          {'t': 'grid', 'gen': G}]
    for b in rules:
        nm, rest = split_bold(b); bl += [H(nm, 2), P(clean(rest))]
    bl += [H('Not every 55+ home is a strata'), P('Some 55+ homes are manufactured homes on rented pads, bare-land strata lots, co-op shares, life leases or memberships. Each works differently and each page on this site names which kind a building is.'),
           LK([('Port Coquitlam 55+ homes', '/port-coquitlam-55-plus-homes-for-sale.html'), ('How to buy a mobile home in BC', '/how-to-buy-a-mobile-home-in-bc-guide.html'), ('Surrey 55+ homes', '/surrey-55-plus-homes-for-sale.html'), ('Coquitlam 55+ homes', '/coquitlam-55-plus-homes-for-sale.html'), ('Burnaby 55+ homes', '/burnaby-55-plus-homes-for-sale.html')])]
    allu = [u for b in rules for u in urls(b)]
    bl += [H('Sources'), P('Read on November 1, 2026.'), LK(src_links(allu)), {**H('More real estate', pos='end'), 'pos': 'end'},
           {**LK([('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Seller net proceeds calculator', '/seller-net-proceeds-calculator.html'), ('Data and methodology', '/data-and-methodology.html'), ('Contact Jared', '/contact.html')]), 'pos': 'end'}]
    faq = [{'q': q, 'a': clean(re.match(r'\*\*Q:.*?\*\*\s*(.*)', b).group(1))} for q, b in allf.values()]
    seen = set(); fq = []
    for f in faq:
        k = f['q'][:30]
        if k not in seen: seen.add(k); fq.append(f)
    d = {'status': 'draft', 'slug': HUB, 'updated': '2026-11-01', 'n55_page': True, 'hand_edited': True, 'blocks': bl, 'faq': fq[:8], 'faq_heading': 'BC 55+ strata rules: your questions answered',
         'new_page': {'title': 'BC 55+ Strata Rules: Age Bylaws and Rentals | Jared Gibbons', 'description': 'BC 55+ strata rules: only 55+ age bylaws are valid, who may own versus live in a unit, exemptions for spouses and caregivers, and rentals. Jared Gibbons, REALTOR®.', 'h1': 'BC 55+ Strata Rules: What Buyers Need to Know'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'BC 55+ strata rules', 'href': f'/{HUB}.html'}], 'needs_from_muse': ['Jared’s review of the wording']}
    save(HUB, d); print('wrote hub', len(bl), 'blocks', len(d['faq']), 'faq')


def build_mobile():
    path = os.path.join(NOTES, 'how-to-buy-a-mobile-home-in-bc-55-plus-homes-2026-11-01.md'); slug = 'how-to-buy-a-mobile-home-in-bc-guide'
    title, sec, raw = parse(path); j = load(slug) or {'status': 'generated', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
    j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != G]
    parks = [(g, b) for g, bs in sec.get(2, {}).items() if g.lower().startswith(('pad-rental', 'co-operative')) for b in bs if b.startswith('**')]
    bl = [H('55+ manufactured-home parks in BC: named examples'), P('This is a representative set, not a full list. Each park below was verified by name from a public source that states its age restriction. Pad rents and fees are listing-stated for one home on one date, not a park tariff, so confirm them with the park.')]
    for g, b in parks:
        nm, rest = split_bold(b); bl += [H(nm, 3), P(clean(rest))]
    bl += [P('Check each park yourself. Breakaway Bays in South Surrey produced conflicting age claims in the sources, and Crispen Bays and Crestway Bays on King George Boulevard are listed as all-ages, so a park’s age label cannot be assumed from its city.')]
    s3 = [b for b in bullets(sec, 3) if real(b)]
    bl += [H('BC rules for park tenancies and 55+ parks')]
    for b in s3:
        nm, rest = split_bold(b)
        if nm and clean(rest): bl += [H(nm, 3), P(clean(rest))]
    allu = [u for n in (1, 2, 3, 4) for b in bullets(sec, n) for u in urls(b)]
    bl += [H('Sources for this section'), LK(src_links(allu))]
    j['blocks'] += bl
    faq = []
    for b in bullets(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if m and clean(m.group(2)): faq.append({'gen': G, 'q': m.group(1).strip(), 'a': clean(m.group(2))})
    j['faq'] = [f for f in j.get('faq', []) if f.get('gen') != G] + faq
    save(slug, j); print('wrote mobile guide section', len(bl), 'blocks', len(faq), 'faq')


def note(slug0): return parse(os.path.join(NOTES, f'{slug0}-55-plus-homes-2026-11-01.md'))


def area_name(slug0):
    return name_city(slug0, note(slug0)[0])


def buyables(sec):
    out = []
    for g, bs in sec.get(2, {}).items():
        gl = g.lower()
        isoth = gl.startswith(('verified 55+ rental', 'retirement', 'subsidized', 'the chartwell')) or '(not ownership' in gl or 'not townhouse' in gl
        if gl.startswith(('verified', 'life lease', 'pad-rental', 'co-operative', 'manufactured-home parks')) and not isoth and 'elsewhere' not in gl and 'roster context' not in gl and 'checked' not in gl:
            out += [(g, b) for b in bs if b.startswith('**') and real(b)]
    return out


def fold_in(primary_slug0, written):
    slug = f'{primary_slug0}-55-plus-homes-for-sale'; j = load(slug)
    if j is None: return
    j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'n55fold']
    names = [area_name(k)[0] for k, v in FOLD.items() if v == primary_slug0]; pname, pcity = area_name(primary_slug0)
    new = [{**H(f'Nearby areas with no 55+ building of their own: {" and ".join(names)}'), 'gen': 'n55fold'},
           {**P(f'{" and ".join(names)} sit next to {pname}, and the sources found no 55+ strata, park or co-op building inside them. The 55+ homes a buyer can own in this part of {pcity} are the buildings above. What each area is like, from the same notes:'), 'gen': 'n55fold'}]
    faq = []
    for k, v in FOLD.items():
        if v != primary_slug0: continue
        title, sec, raw = note(k); nm = area_name(k)[0]
        s1 = [clean(b) for b in bullets(sec, 1) if real(b) and clean(b)]
        s5 = [clean(b) for b in bullets(sec, 5) if real(b) and clean(b)]
        new += [{**H(f'{nm}: streets, schools and what to know', 3), 'gen': 'n55fold'}, {**LI(s1 + s5), 'gen': 'n55fold'}]
        for b in bullets(sec, 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
            if m and clean(m.group(2)) and not SHARED_Q.search(m.group(1)): faq.append({'gen': 'n55fold', 'q': m.group(1).strip(), 'a': clean(m.group(2))})
        comm = k if exists(k) else None
        written.append((slug, nm, pcity, comm))
    i = next((n for n, b in enumerate(j['blocks']) if b.get('t') == 'h' and b.get('text') == 'Sources'), len(j['blocks']))
    j['blocks'][i:i] = new
    have = {f['q'] for f in j['faq']}
    j['faq'] = [f for f in j['faq'] if f.get('gen') != 'n55fold'] + [f for f in faq if f['q'] not in have][:4]
    save(slug, j); print('folded', [k for k, v in FOLD.items() if v == primary_slug0], 'into', slug)


def build_merged(slug, city, ns, written):
    j0 = {}
    parts = [(k,) + note(k) for k in ns]
    names = [area_name(k)[0] for k in ns]
    seenb = {}
    for k, title, sec, raw in parts:
        for g, b in buyables(sec):
            key = re.sub(r'\W+', '', split_bold(b)[0].split(' — ')[0].split(' (')[0].lower())
            seenb.setdefault(key, (g, b, k))
    byarea = {}
    for key, (g, b, k) in seenb.items(): byarea.setdefault(k, []).append((g, b))
    allnames = [split_bold(b)[0].split(' — ')[0].split(' (')[0] for g, b, k in seenb.values()]
    nl = ', '.join(allnames[:-1]) + ' and ' + allnames[-1] if len(allnames) > 1 else allnames[0]
    bl = [{'t': 'notice', 'text': "Draft for Jared's approval. Written from Jared's verified local notes (researched November 1, 2026). Listing-stated figures are labelled; unconfirmed items say so. No live feed filtered to 55+ homes yet.", 'gen': G},
          P(f'Across central {city} ({", ".join(names[:-1])} and {names[-1]}), the 55+ homes a buyer can own that the sources verify are {nl}. This guide takes the neighbourhoods in turn, says what type each building is, and gives the streets, schools and local rules around it. Anything no source states is marked unconfirmed.'), {'t': 'grid', 'gen': G}]
    faq, qseen, allu = [], set(), []
    for k, title, sec, raw in parts:
        nm = area_name(k)[0]
        bl.append(H(f'{nm}: 55+ homes you can buy'))
        for g, b in byarea.get(k, []):
            n2, rest = split_bold(b); tx = clean(rest)
            if n2 and tx: bl += [H(clean(n2), 3), P(tx)]
        if not byarea.get(k): bl.append(P(f'No separate 55+ building is verified inside {nm}; the buildings in the neighbouring sections are the nearest.'))
        s1 = [clean(b) for b in bullets(sec, 1) if real(b) and clean(b)]
        s5 = [clean(b) for b in bullets(sec, 5) if real(b) and clean(b)]
        if s1 or s5: bl += [H(f'{nm}: streets, schools and what to know', 3), LI(s1 + s5)]
        for b in bullets(sec, 4):
            m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
            if not m or SHARED_Q.search(m.group(1)): continue
            q, a = m.group(1).strip(), clean(m.group(2)); kq = re.sub(r'\W+', '', q.lower())[:40]
            if a and kq not in qseen: qseen.add(kq); faq.append({'q': q, 'a': a})
        allu += [u for n in (1, 2, 3, 4, 5) for b in bullets(sec, n) for u in urls(b)]
    rules, rseen = [], set()
    for k, title, sec, raw in parts:
        for b in bullets(sec, 3):
            if real(b) and not split_bold(b)[0].startswith(SHARED_LEAD) and J(b)[:50] not in rseen: rseen.add(J(b)[:50]); rules.append(J(b))
    bl += [H(f'Local rules and plans in {city}'), LI(rules), P('The BC rules on 55+ age bylaws, who may own and who may live in a unit, the exemptions and rentals apply in every strata and are explained once, with sources, on the BC 55+ strata rules page.'), LK([('BC 55+ strata rules', f'/{HUB}.html')])]
    sl = src_links(allu, skip=('age-restriction-bylaws', 'changes-to-legislation', '2023HOUS0038'))
    if sl: bl += [H('Sources'), P('Facts on this page come from these public sources, read on November 1, 2026. Listing-level pages are not listed.'), LK(sl)]
    mk = [(f'{area_name(k)[0]} real estate', f'/{k}.html') for k in ns if exists(k)]
    mk += [(f'{city} 55+ condos for sale', '/chilliwack-55-plus-condos-for-sale.html'), (f'{city} 55+ townhomes for sale', '/chilliwack-55-plus-townhomes-for-sale.html'), ('BC 55+ strata rules', f'/{HUB}.html'), ('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Contact Jared', '/contact.html')]
    bl += [H(f'More {city} real estate', pos='end'), {**LK(mk), 'pos': 'end'}]
    d = {'status': 'draft', 'slug': slug, 'updated': '2026-11-01', 'n55_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq[:12], 'faq_heading': f'{city} 55+ homes: your questions answered',
         'new_page': {'title': f'{city} 55+ Homes by Neighbourhood | Jared Gibbons', 'description': f'{city} 55+ homes by neighbourhood: {", ".join(allnames[:3])} and more, what type each is, local rules and buyer questions. Jared Gibbons, REALTOR®.'[:158], 'h1': f'{city} 55+ Homes for Sale by Neighbourhood'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': f'{city} 55+ homes', 'href': '/chilliwack-55-plus-condos-for-sale.html'}, {'name': 'By neighbourhood', 'href': f'/{slug}.html'}],
         'needs_from_muse': [f'Jared’s own notes on the {city} 55+ buildings: how units sell, what buyers ask', 'Unit counts and years built marked unconfirmed in the sources', 'Live listing feed filtered to 55+ homes']}
    save(slug, d); print('wrote merged', slug, len(bl), 'blocks', len(d['faq']), 'faq')
    for k in ns: written.append((slug, area_name(k)[0], city, k if exists(k) else None))


def build_parks(path, slug0, written):
    slug = PARK_PAGES[slug0]; title, sec, raw = parse(path); j = load(slug)
    if j is None: return
    label = title.split(' — ')[0].replace('(City of Chilliwack)', '').replace('(City + Township)', '').strip()
    j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'n55mh']
    buy = [(g, b) for g, bs in sec.get(2, {}).items() if g.lower().startswith('verified') and '(not ownership' not in g.lower() and 'rental' not in g.lower() and 'elsewhere' not in g.lower() and 'roster' not in g.lower() for b in bs if b.startswith('**') and real(b)]
    if not buy: return
    def T(t, l=2): return {**H(t, l), 'gen': 'n55mh', 'pos': 'end'}
    def PP(t): return {**P(t), 'gen': 'n55mh', 'pos': 'end'}
    bl = [T('Verified 55+ manufactured-home parks and co-ops: what the sources show'),
          PP('These are the 55+ places named in public sources where you can own the home. Pad rent, shares and fees quoted below are listing-stated for one home on one date, not a park tariff, so confirm them with the park. Anything no source states is marked unconfirmed.')]
    for g, b in buy:
        nm, rest = split_bold(b); tx = clean(rest)
        if nm and tx: bl += [T(clean(nm), 3), PP(tx)]
    s3 = [b for b in bullets(sec, 3) if real(b) and not split_bold(b)[0].startswith(SHARED_LEAD)]
    s3 = [J(b) if split_bold(b)[0] else clean(b) for b in s3 if clean(b)]
    if s3: bl += [T('Rules that affect 55+ park homes'), {**LI(s3), 'pos': 'end', 'gen': 'n55mh'}]
    s5 = [clean(b) for b in bullets(sec, 5) if real(b) and clean(b)]
    if s5: bl += [T('Good to know before you buy a park home'), {**LI(s5), 'pos': 'end', 'gen': 'n55mh'}]
    allu = [u for n in (1, 2, 3, 4, 5) for b in bullets(sec, n) for u in urls(b)]
    sl = src_links(allu, skip=('age-restriction-bylaws', 'changes-to-legislation', '2023HOUS0038'))
    if sl: bl += [T('Sources for this section'), {**LK(sl), 'pos': 'end', 'gen': 'n55mh'}, {**LK([('BC 55+ strata rules', f'/{HUB}.html'), ('How to buy a mobile home in BC', '/how-to-buy-a-mobile-home-in-bc-guide.html')]), 'pos': 'end', 'gen': 'n55mh'}]
    j['blocks'] += bl
    faq = []
    for b in bullets(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if m and clean(m.group(2)) and not SHARED_Q.search(m.group(1)): faq.append({'gen': 'n55mh', 'q': m.group(1).strip(), 'a': clean(m.group(2))})
    j['faq'] = [f for f in j.get('faq', []) if f.get('gen') != 'n55mh'] + faq
    j.setdefault('status', 'generated'); save(slug, j); print('wrote park section', slug, len(bl), 'blocks', len(faq), 'faq')


def link_back(written):
    for f in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(f, encoding='utf-8'))
        if any(b.get('gen') == 'n55link' for b in j.get('blocks', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'n55link']; save(os.path.basename(f)[:-5], j)
    byc = {}
    for slug, name, city, comm in written:
        if comm:
            j = load(comm)
            if j is not None:
                j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'n55link']
                j['blocks'].append({'t': 'p', 'text': f'{name} 55+ homes for sale', 'h': f'/{slug}.html', 'pos': 'end', 'gen': 'n55link'}); save(comm, j)
        byc.setdefault(city.lower(), []).append((slug, name))
    for city, items in byc.items():
        for tgt in CITY_55.get(city.replace('-', ' ')) or CITY_55.get(city, []):
            j = load(tgt)
            if j is None: continue
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != 'n55links']
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': f'55+ homes in {city.title()} by community', 'pos': 'end', 'gen': 'n55links'}, {'t': 'list', 'items': [[{'t': f'{n} 55+ homes for sale', 'h': f'/{s}.html'}] for s, n in items], 'pos': 'end', 'gen': 'n55links'}]
            save(tgt, j)


if __name__ == '__main__':
    written = []
    for p in sorted(glob.glob(f'{NOTES}/*.md')): build_community(p, written)
    for p in sorted(glob.glob(f'{NOTES}/*.md')):
        k = os.path.basename(p).replace('-55-plus-homes-2026-11-01.md', '')
        if k in PARK_PAGES: build_parks(p, k, written)
    for slug, (city, ns) in MERGE.items(): build_merged(slug, city, ns, written)
    for prim in sorted(set(FOLD.values())): fold_in(prim, written)
    build_hub(); build_mobile(); link_back(written)
    print(len(written), 'community 55+ pages')
