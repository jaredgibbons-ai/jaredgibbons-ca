"""Condo, townhome and lots-and-land sections from Jared's verified local notes (docs/research/local-notes-types/{condos,townhomes,lots-and-land}/*.md,
researched 2026-11-01), plus three shared "BC buying rules" pages.

Where each note goes (mine; Jared sent no routing):
 - condos and townhome notes -> the community's "<community>-<city>-condos-townhomes-for-sale" page if it exists, else its guide, else the community page.
 - lots-and-land notes       -> the community guide, else the community page.
 Notes for topic pages (price bands, farms, open houses, homepage, reviews ...) and for names with no page on this site are skipped and listed in the report.
Provincial rules that repeat across many notes (same bold lead or same question in 8+ notes) are written once on a rules page and dropped from the community
sections, so the community sections are about the community. Text is cleaned like build_55plus_notes (no MLS numbers, listing links, board counts, file paths,
note-internal references). Only official or building-level sources are listed.   python3 -I tools/build_typenotes.py   (after build_55plus_notes.py)"""
import collections, glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('n55', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build_55plus_notes.py'))
N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
NOTES = os.path.join(ROOT, 'docs/research/local-notes-types'); LOCAL = N.LOCAL; PAGES = N.PAGES
G = 'tn'
KIND = {'condos': dict(hub='bc-condo-buying-rules', noun='condo', title='Condo buildings', sfx='-condos-2026-11-01.md'),
        'townhomes': dict(hub='bc-townhome-buying-rules', noun='townhome', title='Townhome complexes', sfx='-townhomes-2026-11-01.md'),
        'lots-and-land': dict(hub='bc-land-buying-rules', noun='land', title='Lots and land', sfx='-lots-and-land-2026-11-01.md')}
ALIAS = {'aldergrove-langley': 'aldergrove', 'brookswood-langley': 'brookswood', 'brookswood-real-estate-development': 'brookswood-real-estate-development-guide', 'citadel-pq': 'citadel-port-coquitlam',
         'college-park-pm': 'college-park-port-moody', 'cultus-lake-east': 'cultus-lake', 'cultus-lake-north': 'cultus-lake', 'cultus-lake-south': 'cultus-lake', 'east-central-maple-ridge': 'east-central',
         'glenwood-pq': 'glenwood-port-coquitlam', 'heritage-woods-pm': 'heritage-woods-port-moody', 'north-meadows-pi': 'north-meadows-pitt-meadows', 'riverwood': 'riverwood-port-coquitlam',
         'sapperton': 'sapperton-new-westminster', 'simon-fraser-univer': 'simon-fraser-university-area-burnaby', 'sperling-duthie': 'sperling-duthie-burnaby', 'steveston-north': 'steveston-homes-for-sale',
         'steveston-south': 'steveston-homes-for-sale', 'steveston-village': 'steveston-homes-for-sale', 'uptown-nw': 'uptown-new-westminster', 'vancouver-heights': 'vancouver-heights-burnaby',
         'west-central-maple-ridge': 'west-central', 'port-kells': 'port-kells-surrey', 'dewdney-deroche-mission': 'dewdney-deroche', 'durieu-mission': 'durieu', 'mission-west-mission': 'mission-west',
         'stave-falls-mission': 'stave-falls', 'steelhead-mission': 'steelhead', 'thornhill-maple-ridge': 'thornhill-maple-ridge-guide', 'north-maple-ridge': 'north-maple-ridge-guide',
         'west-meadows-pitt-meadows': 'west-meadows-pitt-meadows-guide', 'crescent-beach-ocean-park': 'crescent-beach-ocean-park-guide', 'westham-island': 'westham-island-guide', 'fort-langley': 'fort-langley-guide', 'willoughby': 'willoughby-guide', 'lower-landing': 'lower-landing-guide', 'crescent-bch-ocean-pk': 'crescent-beach-ocean-park-guide', 'central-pt-coquitlam': 'central-port-coquitlam', 'north-shore-pt-moody': 'north-shore-port-moody'}
EXC = {'condos': r'townhom|townhouse|trap|exclud|not counted|cross-ref|caution|named in sources|not a strata|do not count|context|not apartment|row',
       'townhomes': r'apartment|condos|trap|exclud|presale|cross|other forms|never|caution|not counted|not townhom|do not count|named in sources',
       'lots-and-land': r'cross-ref|not land|not land stock'}
# Names Jared asked for pages on (2026-11-02). (display name, city). Existing pages get the sections; names with no page get a new guide page.
PLACES = {'agassiz': ('Agassiz', 'District of Kent'), 'annacis-island': ('Annacis Island', 'Delta'), 'barnston-island': ('Barnston Island', 'Surrey'), 'boulevard': ('Boulevard', 'North Vancouver'),
          'boyd-park': ('Boyd Park', 'Richmond'), 'bridal-falls': ('Bridal Falls', 'FVRD'), 'bridgeport-ri': ('Bridgeport', 'Richmond'), 'brighouse': ('Brighouse', 'Richmond'),
          'british-properties': ('British Properties', 'West Vancouver'), 'brunette': ('Brunette', 'New Westminster'), 'cambie': ('Cambie', 'Vancouver'), 'cedardale': ('Cedardale', 'West Vancouver'),
          'central-lonsdale': ('Central Lonsdale', 'North Vancouver'), 'central-pt-coquitlam': ('Central Port Coquitlam', 'Port Coquitlam'), 'chilliwack-mountain': ('Chilliwack Mountain', 'Chilliwack'),
          'collingwood-ve': ('Renfrew-Collingwood', 'Vancouver'), 'crescent-bch-ocean-pk': ('Crescent Beach and Ocean Park', 'South Surrey'), 'delbrook': ('Delbrook', 'North Vancouver'),
          'downtown-ve': ('Downtown Vancouver', 'Vancouver'), 'dundarave': ('Dundarave', 'West Vancouver'), 'edgemont': ('Edgemont', 'North Vancouver'), 'fairview-vw': ('Fairview', 'Vancouver'),
          'furry-creek': ('Furry Creek', 'SLRD'), 'grandview-woodland': ('Grandview-Woodland', 'Vancouver'), 'harrison-hot-springs': ('Harrison Hot Springs', 'BC'), 'hope': ('Hope', 'BC'),
          'hyde-park-south-surrey': ('Hyde Park', 'South Surrey'), 'kent': ('Kent', 'BC'), 'kerrisdale': ('Kerrisdale', 'Vancouver'), 'lindell-beach': ('Lindell Beach', 'FVRD'), 'lynnmour': ('Lynnmour', 'North Vancouver'),
          'mount-currie': ('Mount Currie', 'BC'), 'mount-pleasant-ve': ('Mount Pleasant', 'Vancouver'), 'mt-lehman': ('Mt. Lehman', 'Abbotsford'), 'norgate': ('Norgate', 'North Vancouver'),
          'north-shore-pt-moody': ('North Shore', 'Port Moody'), 'oakridge-vw': ('Oakridge', 'Vancouver'), 'park-royal': ('Park Royal', 'West Vancouver'), 'pemberton-nv': ('Pemberton Heights', 'North Vancouver'),
          'popkum': ('Popkum', 'FVRD'), 'riverdale-ri': ('Riverdale', 'Richmond'), 'sardis-east-vedder': ('Sardis East Vedder', 'Chilliwack'), 'sardis-south': ('Sardis South', 'Chilliwack'),
          'sardis-west-vedder': ('Sardis West Vedder', 'Chilliwack'), 'shaughnessy': ('Shaughnessy', 'Vancouver'), 'south-arm': ('South Arm', 'Richmond'), 'south-cambie': ('South Cambie', 'Vancouver'),
          'south-granville': ('South Granville', 'Vancouver'), 'surrey-city-centre': ('Surrey City Centre', 'Surrey'), 'sw-marine': ('SW Marine', 'Vancouver'), 'tilbury': ('Tilbury', 'Delta'),
          'university-vw': ('University Endowment Lands', 'Vancouver'), 'upper-lonsdale': ('Upper Lonsdale', 'North Vancouver'), 'whitby-estates': ('Whitby Estates', 'West Vancouver')}
CITYHUB = {'Richmond': ['richmond-homes-for-sale'], 'Vancouver': ['vancouver-homes-for-sale'], 'North Vancouver': ['north-vancouver-homes-for-sale'], 'West Vancouver': ['west-vancouver-homes-for-sale'],
           'New Westminster': ['new-westminster-condos-for-sale', 'new-westminster-homes-for-sale'], 'Surrey': ['surrey-condos-for-sale', 'surrey-homes-for-sale'], 'South Surrey': ['south-surrey-homes-for-sale', 'surrey-homes-for-sale'],
           'Delta': ['tsawwassen-homes-for-sale', 'ladner-homes-for-sale', 'delta-homes-for-sale'], 'Port Coquitlam': ['port-coquitlam-condos-for-sale', 'port-coquitlam-homes-for-sale'], 'Port Moody': ['port-moody-condos-for-sale', 'port-moody-homes-for-sale'],
           'Chilliwack': ['chilliwack-condos-for-sale', 'chilliwack-homes-for-sale'], 'Abbotsford': ['abbotsford-condos-for-sale', 'abbotsford-homes-for-sale'], 'District of Kent': ['chilliwack-homes-for-sale'], 'FVRD': ['chilliwack-homes-for-sale', 'mission-homes-for-sale'],
           'BC': ['chilliwack-homes-for-sale'], 'SLRD': ['west-vancouver-homes-for-sale']}
SHARED_MIN = 8
MAPPED = set(json.load(open(os.path.join(ROOT, 'src/data/snapstats/_mapping.json')))['mapped'])  # community and guide pages only; site pages like faq, privacy, selling are not communities
COMM = set(ALIAS.values()) | MAPPED | set(PLACES) | {re.sub(r'-55-plus-homes-2026-11-01\.md$', '', os.path.basename(p)) for p in glob.glob(os.path.join(ROOT, 'docs/research/local-notes-55plus/*.md'))}  # plus every community Jared's 55+ notes name


def exists(s): return os.path.exists(f'{PAGES}/{s}.json') or os.path.exists(f'{LOCAL}/{s}.json')


def slugify(t): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')


NEWSLUG = {}


def resolve(x, kind):
    if x in NEWSLUG: return NEWSLUG[x]
    cands = [ALIAS.get(x)] if x in ALIAS else []
    cands += [x]
    if kind != 'lots-and-land':
        tp = sorted(glob.glob(f'{LOCAL}/{x}-*-condos-townhomes-for-sale.json') + glob.glob(f'{LOCAL}/{x}-condos-townhomes-for-sale.json'))
        for c in cands:
            if c:
                tp += sorted(glob.glob(f'{LOCAL}/{c}-*-condos-townhomes-for-sale.json') + glob.glob(f'{LOCAL}/{c}-condos-townhomes-for-sale.json'))
        if tp: return os.path.basename(tp[0])[:-5]
    if kind == 'lots-and-land':
        for c in cands:
            if c and exists(f'{c}-lots-land'): return f'{c}-lots-land'
    for c in cands:
        if c and (f'{c}-guide' in MAPPED or (c in COMM and exists(f'{c}-guide'))): return f'{c}-guide'
        if c and c in COMM and exists(c): return c
    return None


def load(s):
    p = f'{LOCAL}/{s}.json'
    if os.path.exists(p): return json.load(open(p, encoding='utf-8'))
    return {'status': 'generated', 'slug': s, 'updated': '2026-11-02', 'blocks': [], 'faq': []}


def save(s, d):
    with open(f'{LOCAL}/{s}.json', 'w', encoding='utf-8') as f: json.dump(d, f, indent=2, ensure_ascii=False); f.write('\n')


def parse_note(path, kind):
    t = open(path, encoding='utf-8').read(); lines = t.split('\n'); title = lines[0][2:].strip()
    pre = []; sec = {}; cur = None; grp = '_'
    for ln in lines[1:]:
        m = re.match(r'^## (\d)\.', ln)
        if m: cur = int(m.group(1)); sec[cur] = {'_': []}; grp = '_'; continue
        if cur is None:
            if ln.strip() and not ln.startswith('Researched Nov'): pre.append(ln.strip())
            continue
        m = re.match(r'^### (.*)', ln)
        if m: grp = m.group(1).strip(); sec[cur][grp] = []; continue
        if ln.startswith('- '): sec[cur].setdefault(grp, []).append(ln[2:])
        elif cur == 4 and ln.startswith('**Q:'): sec[cur].setdefault(grp, []).append(ln.strip())
        elif cur == 4 and ln.startswith('A:') and sec[cur].get(grp): sec[cur][grp][-1] += ' ' + ln[2:].strip()
    return title, pre, sec


def bl4(sec, n): return [b for g in sec.get(n, {}).values() for b in g]


def key(b):
    nm, rest = N.split_bold(b)
    return re.sub(r'\W+', '', (nm or N.clean(b)[:60]).lower())[:50]


def qkey(q): return re.sub(r'\W+', '', q.lower())[:45]


def main():
    files = {k: sorted(glob.glob(f'{NOTES}/{k}/*{v["sfx"]}')) for k, v in KIND.items()}
    notes = []
    for kind, fl in files.items():
        for f in fl:
            x = os.path.basename(f)[:-len(KIND[kind]['sfx'])]; x = re.sub(r'-guide$', '', x)
            title, pre, sec = parse_note(f, kind); notes.append(dict(kind=kind, x=x, path=f, title=title, pre=pre, sec=sec))
    # shared (provincial) items per kind
    shared = {}
    for kind in KIND:
        cb, cq = collections.Counter(), collections.Counter(); best_b, best_q = {}, {}
        for n in [n for n in notes if n['kind'] == kind]:
            seen = set()
            for b in bl4(n['sec'], 3):
                k = key(b)
                if k and k not in seen: seen.add(k); cb[k] += 1; best_b[k] = max(best_b.get(k, b), b, key=len)
            seen = set()
            for b in bl4(n['sec'], 4):
                m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
                if m:
                    k = qkey(m.group(1))
                    if k not in seen: seen.add(k); cq[k] += 1; best_q[k] = max(best_q.get(k, b), b, key=len)
        shared[kind] = dict(b={k for k, c in cb.items() if c >= SHARED_MIN}, q={k for k, c in cq.items() if c >= SHARED_MIN}, bb=best_b, bq=best_q, cb=cb, cq=cq)
    def verified(n):
        c = 0
        for g, bs in n['sec'].get(2, {}).items():
            if g != '_' and re.search(EXC[n['kind']], g, re.I): continue
            c += sum(1 for b in bs if b.startswith('**'))
        return (c, os.path.getsize(n['path']))
    best = {}
    for n in notes:
        k = (n['kind'], n['x'])
        if k not in best or verified(n) > verified(best[k]): best[k] = n
    notes = [n for n in notes if best[(n['kind'], n['x'])] is n]
    for x, (dn, city) in PLACES.items():
        if not resolve(x, 'condos') and any(n['x'] == x for n in notes):
            NEWSLUG[x] = f'{slugify(dn)}-guide' if slugify(city) in slugify(dn) else f'{slugify(dn)}-{slugify(city)}-guide' if city != 'BC' else f'{slugify(dn)}-bc-guide'
            NEWSLUG[x] = NEWSLUG[x].replace('-district-of-kent-', '-bc-').replace('-slrd-', '-bc-').replace('-fvrd-', '-bc-')
    report = collections.defaultdict(list); targets = collections.defaultdict(list)
    for n in notes:
        tgt = resolve(n['x'], n['kind'])
        if not tgt or n['x'] in ('homepage', 'reviews') or N.TOPIC.search(n['x']): report['skipped'].append((n['kind'], n['x'])); continue
        targets[tgt].append(n)
    # remove community guides this script made in an earlier run that are no longer wanted (renamed slug, or the community turned out to have a page)
    for pth in glob.glob(f'{LOCAL}/*-guide.json'):
        sl = os.path.basename(pth)[:-5]
        if sl not in NEWSLUG.values() and json.load(open(pth, encoding='utf-8')).get('tn_page'): os.remove(pth)
    # strip old blocks everywhere
    for p in glob.glob(f'{LOCAL}/*.json'):
        j = json.load(open(p, encoding='utf-8'))
        if any(b.get('gen') == G for b in j.get('blocks', [])) or any(f.get('gen') == G for f in j.get('faq', [])):
            j['blocks'] = [b for b in j['blocks'] if b.get('gen') != G]; j['faq'] = [f for f in j.get('faq', []) if f.get('gen') != G]; save(os.path.basename(p)[:-5], j)
    # Streets, rules and local-detail bullets are written once site-wide: the 55+ pages own theirs, and a later section skips any bullet already published.
    seen = set()
    for pth in glob.glob(f'{LOCAL}/*.json'):
        jj = json.load(open(pth, encoding='utf-8'))
        for b in jj.get('blocks', []):
            if b.get('gen') in ('n55', 'n55mh', 'n55fold') and b.get('t') == 'list':
                for it in b['items']: seen.add(it[0]['t'][:70])
    wrote = 0
    for x, sl in NEWSLUG.items(): make_base(x, sl, [n for n in notes if n['x'] == x])
    for tgt, ns in sorted(targets.items()):
        j = load(tgt); bl = []; faq = []; urls_all = []
        for n in sorted(ns, key=lambda n: ['condos', 'townhomes', 'lots-and-land'].index(n['kind'])):
            b, f, u = section(n, shared[n['kind']], seen); bl += b; faq += f; urls_all += u
        # drop junk fragments, empty lists and headings left with nothing under them
        for b in bl:
            if b['t'] == 'list': b['items'] = [i for i in b['items'] if len(i[0]['t']) >= 18 and not i[0]['t'].lower().startswith('none verified')]
        bl = [b for b in bl if not (b['t'] == 'list' and not b['items']) and not (b['t'] == 'p' and len(b['text']) < 18)]
        bl = [b for i, b in enumerate(bl) if not (b['t'] == 'h' and (i + 1 == len(bl) or bl[i + 1]['t'] == 'h' and bl[i + 1]['level'] <= b['level']))]
        if len(bl) < 4: continue
        j['blocks'] = j.get('blocks', []) + bl
        have = {qkey(x['q']) for x in j.get('faq', [])}
        j['faq'] = j.get('faq', []) + [x for x in faq if qkey(x['q']) not in have][:8]
        j.setdefault('slug', tgt); save(tgt, j); wrote += 1
    for x, sl in NEWSLUG.items(): finish_base(x, sl, shared)
    # inbound links: each city hub lists the new guides for its city
    for pth in glob.glob(f'{LOCAL}/*.json'):
        jj = json.load(open(pth, encoding='utf-8'))
        if any(b.get('gen') == 'tn_hub' for b in jj.get('blocks', [])): jj['blocks'] = [b for b in jj['blocks'] if b.get('gen') != 'tn_hub']; save(os.path.basename(pth)[:-5], jj)
    byhub = collections.defaultdict(list)
    for x, sl in NEWSLUG.items():
        hs = [h for h in CITYHUB.get(PLACES[x][1], []) if exists(h)]
        if hs: byhub[hs[0]].append((f'{PLACES[x][0]} real estate guide', f'/{sl}.html'))
    for hub, items in byhub.items():
        jj = load(hub); nice = hub.replace('-homes-for-sale', '').replace('-condos-for-sale', '').replace('-', ' ').title()
        jj['blocks'] += [{**N.H(f'{nice} neighbourhood guides', 2), 'gen': 'tn_hub', 'pos': 'end'}, {**N.LK(items), 'gen': 'tn_hub', 'pos': 'end'}]
        save(hub, jj)
    hubs(notes, shared)
    print('sections written to', wrote, 'pages;', 'notes used', sum(len(v) for v in targets.values()), 'skipped', len(report['skipped']))
    json.dump({'skipped': report['skipped']}, open(os.path.join(ROOT, 'docs/research/local-notes-types/_skipped.json'), 'w'), indent=1)


def H(t, l=2): return {**N.H(t, l), 'gen': G, 'pos': 'end'}
def P(t): return {**N.P(t), 'gen': G, 'pos': 'end'}
def LI(items): return {**N.LI(items), 'gen': G, 'pos': 'end'}
def LK(items): return {**N.LK(items), 'gen': G, 'pos': 'end'}


def area_label(title, kind):
    head = title.split(' — ')[0].strip()
    head = re.sub(r'\s*[—-]\s*(Condos|Townhomes|Lots and Land).*$', '', head).strip()
    return head


def section(n, sh, seen):
    kind, sec = n['kind'], n['sec']; K = KIND[kind]; area = area_label(n['title'], kind); name = re.sub(r'\s*\(.*?\)', '', area).split(',')[0].strip()
    pre = ' '.join(N.clean(re.sub(r'^\*\*(.*?)\*\*', r'\1', p)) for p in n['pre'] if not p.startswith(('#', '>')) and 'FILE STATUS' not in p)
    pre = N.clean(pre)
    bl = [H(f'{K["title"]} in {name}')]
    if pre and len(pre) > 40: bl.append(P(pre))
    items = []
    for g, bs in sec.get(2, {}).items():
        if g == '_' and kind != 'lots-and-land': continue
        if re.search(EXC[kind], g, re.I) and g != '_': continue
        for b in bs:
            if kind != 'lots-and-land' and not (b.startswith('**') and N.real(b)): continue
            items.append((g, b))
    cnt = 0
    if kind == 'lots-and-land':
        groups = collections.OrderedDict()
        for g, b in items:
            tx = N.J(b) if b.startswith('**') else N.clean(b)
            if tx: groups.setdefault(re.split(r' — |\s*\(', g)[0].strip() if g != '_' else 'What trades here', []).append(tx)
        for g, txs in groups.items(): bl += [H('What trades here' if re.search(r'\bfiles?\b|sibling|variant|program|position', g, re.I) else g, 3), LI(txs)]; cnt += len(txs)
    else:
        for g, b in items:
            nm, rest = N.split_bold(b); tx = N.clean(rest)
            if nm and tx: bl += [H(N.clean(nm), 3), P(tx)]; cnt += 1
    def fresh(xs):
        out = []
        for x in xs:
            if x and x[:70] not in seen: seen.add(x[:70]); out.append(x)
        return out
    s1 = fresh([N.clean(b) for b in bl4(sec, 1) if N.real(b) and not b.startswith('Market figures') and N.clean(b)])
    if s1: bl += [H(f'Streets, schools and getting around {name}', 3), LI(s1)]
    s3 = [b for b in bl4(sec, 3) if N.real(b) and key(b) not in sh['b']]
    s3 = fresh([N.J(b) for b in s3 if N.clean(b)])
    if s3: bl += [H(f'Local rules that affect {K["noun"]} buyers in {name}', 3), LI(s3)]
    s5 = fresh([N.clean(b) for b in bl4(sec, 5) if N.real(b) and N.clean(b)])
    if s5: bl += [H(f'Good to know about {name}', 3), LI(s5)]
    bl.append(P(f'The BC rules that apply to every {K["noun"]} purchase are explained once, with sources, on the page linked below.'))
    bl.append(LK([(f'BC {K["noun"]} buying rules', f'/{K["hub"]}.html')]))
    u = [x for k in (1, 2, 3, 4, 5) for b in bl4(sec, k) for x in N.urls(b)]
    sl = N.src_links(u, skip=('age-restriction-bylaws', 'changes-to-legislation'))
    if sl: bl += [H(f'Sources for the {K["noun"]} notes on {name}', 3), LK(sl[:14])]
    faq = []
    for b in bl4(sec, 4):
        m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', b)
        if m and qkey(m.group(1)) not in sh['q'] and not N.FQ_BAD.search(m.group(1)) and N.clean(m.group(2)): faq.append({'gen': G, 'q': m.group(1).strip(), 'a': N.clean(m.group(2))})
    return bl, faq[:5], u


def make_base(x, slug, ns):
    dn, city = PLACES[x]; d = dict(status='draft', slug=slug, updated='2026-11-02', tn_page=True, hand_edited=True, blocks=[], faq=[])
    first = None
    for kind in ('condos', 'townhomes', 'lots-and-land'):
        for n in ns:
            if n['kind'] == kind and first is None:
                for b in bl4(n['sec'], 1):
                    t = N.clean(b)
                    if len(t) > 60 and N.real(b) and not re.match(r'(Page scope|Market figures|Filing position)', b): first = t; break
    place = dn if city == 'BC' or city.lower() in dn.lower() else f'{dn}, {city}'
    has55 = os.path.exists(f'{LOCAL}/{x}-55-plus-homes-for-sale.json')
    d['blocks'] = [{'t': 'notice', 'text': "Draft for Jared's approval. Written from Jared's verified local notes (researched November 1, 2026). Listing-stated figures are labelled; unconfirmed items say so. No live listing feed or board statistics are attached to this page yet.", 'gen': 'tn_new'}]
    if first: d['blocks'].append({**N.P(first), 'gen': 'tn_new'})
    d['blocks'].append({**N.P(f'This guide covers {dn}\'s condo buildings, townhome complexes and land: what each source verifies, the local rules, and what buyers ask. Anything no source states is marked unconfirmed.' + (' Seniors housing has its own page.' if has55 else '')), 'gen': 'tn_new'})
    d['blocks'].append({'t': 'grid', 'gen': 'tn_new'})
    d['new_page'] = dict(title=(f'{place} Real Estate Guide | Jared Gibbons' if len(f'{place} Real Estate Guide | Jared Gibbons') <= 66 else f'{place} Real Estate Guide')[:70],
                         description=f'{place}: verified condo buildings, townhome complexes, land and local rules, with sources. Jared Gibbons, REALTOR®.'[:158], h1=f'{dn} Real Estate Guide: {city}' if city != 'BC' and city.lower() not in dn.lower() else f'{dn} Real Estate Guide')
    d['needs_from_muse'] = [f'Jared’s own notes on {dn}: how it sells, what buyers ask', 'Live listing feed and board statistics for this area', 'Photos']
    save(slug, d)


def finish_base(x, slug, shared):
    d = load(slug); dn, city = PLACES[x]
    hubs_ = [h for h in CITYHUB.get(city, []) if exists(h)][:2]
    links = [(f'{c.replace("-", " ").title()}', f'/{c}.html') for c in hubs_]
    if os.path.exists(f'{LOCAL}/{x}-55-plus-homes-for-sale.json'): links.append((f'{dn} 55+ homes for sale', f'/{x}-55-plus-homes-for-sale.html'))
    links += [('BC condo buying rules', '/bc-condo-buying-rules.html'), ('BC townhome buying rules', '/bc-townhome-buying-rules.html'), ('BC land buying rules', '/bc-land-buying-rules.html'),
              ('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Contact Jared', '/contact.html')]
    d['blocks'] += [{**N.H(f'More {dn} real estate', 2), 'gen': 'tn_new', 'pos': 'end'}, {**N.LK(links), 'gen': 'tn_new', 'pos': 'end'}]
    d['faq_heading'] = f'{dn} real estate: your questions answered'
    d['breadcrumbs'] = [{'name': 'Home', 'href': '/index.html'}] + ([{'name': c.replace('-', ' ').title(), 'href': f'/{c}.html'} for c in hubs_[:1]]) + [{'name': dn, 'href': f'/{slug}.html'}]
    save(slug, d)


def hubs(notes, sh_all):
    meta = {'condos': ('BC Condo Buying Rules: Strata Fees, Depreciation Reports and Form B | Jared Gibbons', 'BC condo buying rules: strata fees, depreciation reports, Form B, rentals and pets, explained with provincial sources. Jared Gibbons, REALTOR®.', 'BC Condo Buying Rules: What Every Buyer Should Check'),
            'townhomes': ('BC Townhome Buying Rules: Strata vs Fee Simple | Jared Gibbons', 'BC townhome buying rules: strata townhouses versus fee-simple row homes, fees, bylaws and what to check, with provincial sources. Jared Gibbons, REALTOR®.', 'BC Townhome Buying Rules: Strata vs Fee Simple'),
            'lots-and-land': ('BC Land Buying Rules: ALR, Bare-Land Strata and Fee Simple | Jared Gibbons', 'BC land buying rules: fee-simple lots, bare-land strata, Agricultural Land Reserve limits and what to check before buying land. Jared Gibbons, REALTOR®.', 'BC Land Buying Rules: ALR, Bare-Land Strata, Fee Simple')}
    for kind, K in KIND.items():
        sh = sh_all[kind]; ks = sorted(sh['b'], key=lambda k: -sh['cb'][k])
        if not ks: continue
        bl = [{'t': 'notice', 'text': "Draft for Jared's approval. Built from provincial and municipal pages named under Sources, read November 1, 2026.", 'gen': G},
              {**N.P(f'These BC rules apply to every {K["noun"]} purchase on this site, whichever neighbourhood it is in. They are written once here; each community page covers only what is specific to that community.'), 'gen': G}, {'t': 'grid', 'gen': G}]
        urls_all = []
        for k in ks[:14]:
            b = sh['bb'][k]; nm, rest = N.split_bold(b)
            if nm and len(N.clean(rest)) > 60 and not re.search(r'documented in the research|none imported|-specific position', N.clean(rest)): bl += [{**N.H(N.clean(nm), 2), 'gen': G}, {**N.P(N.clean(rest)), 'gen': G}]
            urls_all += N.urls(b)
        sl = N.src_links(urls_all)
        links = [('Home evaluation', '/home-evaluation.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('BC 55+ strata rules', '/bc-55-plus-strata-rules.html'), ('Data and methodology', '/data-and-methodology.html'), ('Contact Jared', '/contact.html')]
        if sl: bl += [{**N.H('Sources', 2), 'gen': G}, {**N.LK(sl), 'gen': G}]
        bl += [{**N.H('More real estate', 2), 'gen': G, 'pos': 'end'}, {**N.LK(links), 'gen': G, 'pos': 'end'}]
        faq = []
        for k in sorted(sh['q'], key=lambda k: -sh['cq'][k])[:8]:
            m = re.match(r'\*\*Q:\s*(.*?)\*\*\s*(.*)', sh['bq'][k])
            if m and N.clean(m.group(2)): faq.append({'q': m.group(1).strip(), 'a': N.clean(m.group(2))})
        d = {'status': 'draft', 'slug': K['hub'], 'updated': '2026-11-02', 'tn_page': True, 'hand_edited': True, 'blocks': bl, 'faq': faq, 'faq_heading': f'BC {K["noun"]} buying: your questions answered',
             'new_page': {'title': meta[kind][0], 'description': meta[kind][1][:158], 'h1': meta[kind][2]},
             'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': meta[kind][2], 'href': f'/{K["hub"]}.html'}], 'needs_from_muse': ['Jared’s review of the wording']}
        save(K['hub'], d); print('hub', K['hub'], len(bl), 'blocks', len(faq), 'faq')


if __name__ == '__main__':
    main()
