"""City school lists: one 'Schools in <city>, BC' page per city, built only from education-inventory.csv.

Every number and row comes from the CSV (BC Ministry of Education and Child Care school list 2025/26 updated July 2026; Province's
post-secondary locations file; Child Care Map registry). Nothing is estimated. Level is read from the school's name where the name says
secondary or middle, because the Ministry's own level field mislabels some secondary schools as elementary (Muse confirmed this on the raw file).

Writes src/data/local/schools-in-<slug>-bc.json (new pages, status 'generated') and a link block (gen 'schoollist') on each city hub page.
    python3 -I tools/build_school_lists.py
"""
import csv, glob, json, os, re, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CSV = os.path.join(ROOT, 'docs/research/education-inventory-v2-2026-11-01.csv')
UPDATED = '2026-11-01'

# slug, display name, csv cities, hub pages that get a link, nearby-context sentence (verifiable only)
CITIES = [
    ('surrey', 'Surrey', ['Surrey'], ['surrey-homes-for-sale', 'surrey-neighbourhood-guides', 'south-surrey-homes-for-sale'], 'surrey-homes-for-sale', 'surrey-neighbourhood-guides'),
    ('langley', 'Langley', ['Langley', 'Aldergrove', 'Fort Langley'], ['langley-homes-for-sale', 'langley-neighbourhood-guides', 'city-of-langley-homes-for-sale'], 'langley-homes-for-sale', 'langley-neighbourhood-guides'),
    ('abbotsford', 'Abbotsford', ['Abbotsford'], ['abbotsford-homes-for-sale', 'abbotsford-neighbourhood-guides'], 'abbotsford-homes-for-sale', 'abbotsford-neighbourhood-guides'),
    ('chilliwack', 'Chilliwack', ['Chilliwack', 'Cultus Lake', 'Rosedale'], ['chilliwack-homes-for-sale', 'chilliwack-neighbourhood-guides'], 'chilliwack-homes-for-sale', 'chilliwack-neighbourhood-guides'),
    ('delta', 'Delta', ['Delta'], ['delta-homes-for-sale', 'delta-neighbourhood-guides'], 'delta-homes-for-sale', 'delta-neighbourhood-guides'),
    ('maple-ridge-pitt-meadows', 'Maple Ridge and Pitt Meadows', ['Maple Ridge', 'Pitt Meadows'], ['maple-ridge-homes-for-sale', 'maple-ridge-neighbourhood-guides', 'pitt-meadows-homes-for-sale'], 'maple-ridge-homes-for-sale', 'maple-ridge-neighbourhood-guides'),
    ('mission', 'Mission', ['Mission', 'Dewdney', 'Deroche'], ['mission-homes-for-sale', 'mission-neighbourhood-guides'], 'mission-homes-for-sale', 'mission-neighbourhood-guides'),
    ('hope-agassiz-harrison', 'Hope, Agassiz and Harrison Hot Springs', ['Hope', 'Agassiz', 'Harrison Hot Springs'], [], None, None),
    ('vancouver', 'Vancouver', ['Vancouver'], ['vancouver-homes-for-sale'], 'vancouver-homes-for-sale', None),
    ('burnaby', 'Burnaby', ['Burnaby'], ['burnaby-homes-for-sale'], 'burnaby-homes-for-sale', None),
    ('richmond', 'Richmond', ['Richmond'], ['richmond-homes-for-sale'], 'richmond-homes-for-sale', None),
    ('coquitlam', 'Coquitlam', ['Coquitlam'], ['coquitlam-homes-for-sale'], 'coquitlam-homes-for-sale', None),
    ('port-coquitlam', 'Port Coquitlam', ['Port Coquitlam'], ['port-coquitlam-homes-for-sale'], 'port-coquitlam-homes-for-sale', None),
    ('port-moody-anmore', 'Port Moody and Anmore', ['Port Moody', 'Anmore'], ['port-moody-homes-for-sale', 'anmore-homes-for-sale'], 'port-moody-homes-for-sale', None),
    ('new-westminster', 'New Westminster', ['New Westminster'], ['new-westminster-homes-for-sale'], 'new-westminster-homes-for-sale', None),
    ('north-vancouver', 'North Vancouver', ['North Vancouver'], ['north-vancouver-homes-for-sale'], 'north-vancouver-homes-for-sale', None),
    ('west-vancouver', 'West Vancouver', ['West Vancouver'], ['west-vancouver-homes-for-sale'], 'west-vancouver-homes-for-sale', None),
]
SMALL_JOIN = {'Maple Ridge and Pitt Meadows', 'Port Moody and Anmore', 'Hope, Agassiz and Harrison Hot Springs'}


def num(n): return f'{n:,}'
def plural(n, one, many=None): return f'{num(n)} {one if n == 1 else (many or one + "s")}'


def lvl(r):
    n, c = r['name'].lower(), r['category']
    if c in ('college', 'university'): return 'post'
    if r['public_or_private'] != 'Public': return 'independent'
    if 'secondary' in n or 'senior sec' in n: return 'secondary'
    if r.get('alternate_program') == 'YES' or r.get('online_program') == 'YES': return 'other'
    if re.search(r'alternate|continuing ed|online|education services|learning cent|distributed|adult', n): return 'other'
    if 'middle' in n: return 'middle'
    return {'elementary': 'elementary', 'middle': 'middle', 'secondary': 'secondary'}.get(c, 'other')


def addr(a):
    a = (a or '').strip()
    return a if re.match(r'^[0-9#]', a) and re.search(r'[A-Za-z]', a) else 'Mailing address only in the source'


def nm(n):
    n = re.sub(r'^Ecole ', 'École ', n)
    m = re.match(r'^(.+?) — (.+)$', n)
    return n if not m else (m.group(1) if (m.group(1) in m.group(2) or 'Campus' in m.group(2) or 'Main' in m.group(2)) else f'{m.group(1)} ({m.group(2)})')


def dist(r): return r['district_or_authority']


def dlong(d): return re.sub(r'^SD(\d+) (.*)$', r'School District \1 (\2)', d)


def main():
    rows = list(csv.DictReader(open(CSV, encoding='utf-8')))
    out_slugs = []
    for slug, disp, cities, hubs, homes, guides in CITIES:
        sch = [r for r in rows if r['city'] in cities and r['category'] != 'daycare']
        kids = [r for r in rows if r['city'] in cities and r['category'] == 'daycare']
        groups = collections.defaultdict(list)
        for r in sch: groups[lvl(r)].append(r)
        k12 = sum(len(v) for k, v in groups.items() if k != 'post')
        pub = sum(len(groups[k]) for k in ('elementary', 'middle', 'secondary', 'other'))
        ind = len(groups['independent']); post = len(groups['post'])
        districts = sorted({dist(r) for r in sch if lvl(r) in ('elementary', 'middle', 'secondary', 'other')})
        main_d = collections.Counter(dist(r) for r in sch if lvl(r) in ('elementary', 'middle', 'secondary', 'other')).most_common()
        group_n = sum(1 for r in kids if 'Licensed Group' in r['district_or_authority']); fam_n = sum(1 for r in kids if 'Licensed Family' in r['district_or_authority'])
        title = next(x for x in (f'Schools in {disp}, BC | Full List by Level | Jared Gibbons', f'Schools in {disp}, BC | Full List | Jared Gibbons', f'Schools in {disp}, BC | Jared Gibbons') if len(x) <= 66)
        desc = (f'Browse {num(k12)} public and independent schools with a {disp} address, grouped by level with street addresses. '
                f'From the BC Ministry of Education and Child Care list.')[:158]
        h1 = f'Schools in {disp}, BC'
        parts = []
        dtxt = ', '.join(f'{dlong(d)}: {num(c)}' for d, c in main_d)
        intro = (f'The BC Ministry of Education and Child Care school list shows {num(k12)} schools with a {disp} street address: '
                 f'{plural(pub, "public school")} and {plural(ind, "independent school")}'
                 + (f'. It also shows {plural(post, "college or university campus", "college and university campuses")}.' if post else '.'))
        n_alt = sum(1 for r in sch if r.get('alternate_program') == 'YES'); n_onl = sum(1 for r in sch if r.get('online_program') == 'YES')
        n_fi = sum(1 for r in sch if r.get('french_immersion') == 'YES'); n_fr = sum(1 for r in sch if r.get('francophone') == 'YES')
        extra = []
        if n_fi: extra.append(f'{plural(n_fi, "school")} marked as offering French Immersion')
        if n_fr: extra.append(f'{plural(n_fr, "Francophone school")} run by the Conseil scolaire francophone')
        if n_alt: extra.append(f'{plural(n_alt, "alternate program")}')
        if n_onl: extra.append(f'{plural(n_onl, "online school")}')
        if extra: intro += ' In that list, ' + oxford(extra) + '.'
        blocks = [{'t': 'p', 'text': intro}]
        if main_d:
            blocks.append({'t': 'p', 'text': f'Public schools here are run by {oxford([dlong(d) for d, c in main_d])}. Count by district: {dtxt}.'})
        blocks.append({'t': 'p', 'text': 'Alternate programs, continuing education centres and online schools that have a street address sit under "other public schools and programs"; the level of every school is read from its name.'})
        comm = collections.Counter(r['city'] for r in sch if lvl(r) != 'post').most_common()
        if len(comm) > 1:
            blocks.append({'t': 'p', 'text': f'By mailing community, the {disp} list splits as ' + oxford([f'{c} ({num(n)})' for c, n in comm]) + '.'})
        def names(key, limit=8):
            g = sorted({nm(r['name']) for r in groups.get(key, [])})
            return oxford(g[:limit]) + (f' and {num(len(g) - limit)} more' if len(g) > limit else '')
        if groups.get('secondary'):
            blocks.append({'t': 'p', 'text': f'Public secondary schools with a {disp} address: {names("secondary")}.'})
        fi_names = sorted({nm(r['name']) for r in sch if r.get('french_immersion') == 'YES'})
        if fi_names:
            blocks.append({'t': 'p', 'text': f'The Ministry file marks these {disp} schools as offering French Immersion: {oxford(fi_names[:10])}' + (f' and {num(len(fi_names) - 10)} more.' if len(fi_names) > 10 else '.')})
        if groups.get('independent'):
            blocks.append({'t': 'p', 'text': f'Independent schools listed for {disp} include {names("independent", 6)}.'})
        blocks.append({'t': 'p', 'text': 'Before an offer, ask the district which school serves the exact street address.'})
        NOTE = {'surrey': 'The list covers the whole city, so schools in South Surrey, Cloverdale, Newton, Fleetwood and Guildford are in it because they carry Surrey addresses.',
                'langley': 'Langley is two municipalities, the City of Langley and the Township of Langley. This list covers both, plus Aldergrove and Fort Langley, and the Community column shows where each school sits.',
                'delta': 'Delta is one municipality made up of North Delta, Ladner and Tsawwassen, and this list covers all three.',
                'maple-ridge-pitt-meadows': 'Maple Ridge and Pitt Meadows are separate cities served by one school district, so they share this list and the Community column shows which city each school is in.',
                'mission': 'Dewdney and Deroche carry their own mailing communities but sit in the Mission school district, so they are listed here.',
                'port-moody-anmore': 'Port Moody and Anmore are separate municipalities that share a school district, so they share this list.',
                'hope-agassiz-harrison': 'These three communities share one school district, so they share this list.',
                'chilliwack': 'Cultus Lake and Rosedale carry their own mailing communities but sit in the Chilliwack school district, so they are listed here.'}
        if slug in NOTE: blocks.append({'t': 'p', 'text': NOTE[slug]})
        if slug == 'surrey':
            blocks.append({'t': 'p', 'text': 'Read how South Surrey school catchments work', 'h': '/south-surrey-school-catchments.html'})
        SECT = [('elementary', 'Public elementary schools in {c}'), ('middle', 'Public middle schools in {c}'), ('secondary', 'Public secondary schools in {c}'),
                ('other', 'Other public schools and programs in {c}'), ('independent', 'Independent schools in {c}'), ('post', 'Colleges and universities in {c}')]
        for key, head in SECT:
            g = sorted(groups.get(key, []), key=lambda r: (r['city'] != cities[0], r['city'], r['name'].lower()))
            if not g: continue
            multi = len({r['city'] for r in g}) > 1 or disp in SMALL_JOIN
            blocks.append({'t': 'h', 'level': 2, 'text': head.format(c=disp) + f' ({num(len(g))})'})
            if key == 'independent':
                blocks.append({'t': 'p', 'text': 'An address gives no priority for a place at an independent school.'})
            hd = (['School', 'District area', 'Street address'] if key == 'independent' else ['Campus', 'Street address'] if key == 'post' else ['School', 'District', 'Street address'])
            fi = key in ('elementary', 'middle', 'secondary', 'other') and any(r.get('french_immersion') == 'YES' for r in g)
            if fi: hd = hd[:-1] + ['French Immersion', hd[-1]]
            if multi: hd = hd + ['Community']
            tr = []
            for r in g:
                row = [nm(r['name'])] + ([] if key == 'post' else [r['district_or_authority']]) + ([('Yes' if r.get('french_immersion') == 'YES' else '—')] if fi else []) + [addr(r['street_address'])] + ([r['city']] if multi else [])
                tr.append(row)
            blocks.append({'t': 'table', 'caption': head.format(c=disp).replace(' in ', ' with street addresses in ', 1), 'head': hd, 'rows': tr,
                           'source': 'Source: ' + ('Locations of B.C. Post-Secondary Institutions (Province of BC)' if key == 'post' else 'BC Schools K-12 with Francophone Indicators (BC Ministry of Education and Child Care), 2025/26 file updated July 2026') + ', read 2026-11-01.'})
        if kids:
            blocks.append({'t': 'h', 'level': 2, 'text': f'Licensed childcare in {disp}'})
            blocks.append({'t': 'p', 'text': (f'The Ministry\'s Child Care Map registry lists {plural(len(kids), "licensed childcare facility", "licensed childcare facilities")} with a {disp} address: '
                                              f'{num(group_n)} licensed group and {num(fam_n)} licensed family. Unlicensed care is not in the registry.')})
        faq = [{'q': f'How many schools are in {disp}, BC?', 'a': f'The BC Ministry of Education and Child Care list shows {num(k12)} schools with a {disp} street address: {plural(pub, "public school")} and {plural(ind, "independent school")}. The count includes alternate programs and online schools that have a street address.'},
               {'q': f'Which school district covers {disp}?', 'a': (f'Public schools with a {disp} address are run by {oxford([dlong(d) for d, c in main_d])}.' if main_d else 'See the district listed beside each school.')},
               {'q': f'How do I find the catchment school for a {disp} address?', 'a': f'Ask {oxford([dlong(d) for d, c in main_d][:2]) if main_d else "the school district"} to confirm it for the exact street address.'}]
        d = {'status': 'generated', 'slug': f'schools-in-{slug}-bc', 'updated': UPDATED,
             'new_page': {'title': title, 'description': desc, 'h1': h1},
             'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': h1, 'href': f'/schools-in-{slug}-bc.html'}],
             'faq_heading': f'{disp} schools: your questions answered', 'blocks': blocks, 'faq': faq}
        path = os.path.join(ROOT, f'src/data/local/schools-in-{slug}-bc.json')
        json.dump(d, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(path, 'a').write('\n')
        out_slugs.append((slug, disp, hubs, k12))
    ssw = south_surrey(rows)
    out_slugs.append(('south-surrey-white-rock', 'South Surrey and White Rock', ['south-surrey-homes-for-sale', 'white-rock', 'south-surrey-school-catchments'], ssw))
    # link blocks on hub pages
    for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json')):
        d = json.load(open(f, encoding='utf-8'))
        if any(b.get('gen') == 'schoollist' for b in d.get('blocks', [])):
            d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'schoollist']
            if not d['blocks'] and d.get('status') == 'generated': os.remove(f); continue
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
    for slug, disp, hubs, k12 in out_slugs:
        for h in hubs:
            if not os.path.exists(os.path.join(ROOT, f'src/data/pages/{h}.json')): continue
            f = os.path.join(ROOT, f'src/data/local/{h}.json')
            blk = {'t': 'p', 'text': (f'See all {num(k12)} schools in {disp}, BC' if slug != 'south-surrey-white-rock' else f'See all {num(k12)} South Surrey and White Rock public schools with street addresses'), 'h': f'/schools-in-{slug}-bc.html', 'gen': 'schoollist'}
            d = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {'status': 'generated', 'slug': h, 'updated': UPDATED, 'blocks': []}
            d['blocks'].append(blk)
            json.dump(d, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
    print('built', len(out_slugs), 'school list pages;', ', '.join(f'{s}:{k}' for s, _, _, k in out_slugs))


# ---- South Surrey and White Rock: families of schools (from Jared's own catchment guide, which takes them from Surrey Schools) + CSV addresses
FAMILIES = [('Earl Marriott Secondary', ['Douglas', 'Jessie Lee', 'Laronde', 'Peace Arch', 'South Meridian', "Ta'talu", "Xw'epiteng"]),
            ('Elgin Park Secondary', ['Chantrell Creek', 'Crescent Park', 'Ocean Cliff', 'Ray Shepherd', 'Semiahmoo Trail']),
            ('Grandview Heights Secondary', ['East Kensington', 'Edgewood', 'Morgan', 'Pacific Heights', 'Rosemary Heights', 'Sunnyside']),
            ('Semiahmoo Secondary', ['Bayridge', 'H.T. Thrift', 'White Rock'])]
INDEP = ['White Rock Christian Academy', 'Southridge School']


def _k(x): return re.sub(r"[^a-z0-9]", "", x.lower().replace('\u2019', "'"))


def south_surrey(rows):
    pool = [r for r in rows if r['category'] in ('elementary', 'secondary', 'middle', 'private', 'elementary+secondary') and r['city'] in ('Surrey', 'White Rock')]
    def find(name, elem):
        want = _k(name + (' elementary' if elem else ''))
        m = [r for r in pool if _k(r['name']) == want and r['public_or_private'] == 'Public']
        if not m: raise SystemExit('not found in CSV: ' + name)
        return m[0]
    blocks = [{'t': 'p', 'text': ('South Surrey and White Rock are both in School District 36 (Surrey). The district groups each secondary school with the elementary schools that feed it, and this page lists those four families with the street address of every school, '
                                  'taken from the BC Ministry of Education and Child Care school list.')},
              {'t': 'p', 'text': 'Catchments are set by street address, not by neighbourhood name, so two homes a block apart can fall into different schools. Check the exact address in the district\'s School Locator and again before you remove subjects.'},
              {'t': 'p', 'text': 'Read how South Surrey school catchments work, with the area-by-area boundary notes', 'h': '/south-surrey-school-catchments.html'}]
    total = 0
    for sec, els in FAMILIES:
        sr = find(sec, False)
        hd = ['School', 'Level', 'French Immersion', 'Street address', 'Community']
        yn = lambda r: 'Yes' if r.get('french_immersion') == 'YES' else '—'
        tr = [[sr['name'], 'Secondary', yn(sr), sr['street_address'], sr['city']]]
        for e in els:
            er = find(e, True); tr.append([er['name'].replace('H T ', 'H.T. '), 'Elementary', yn(er), er['street_address'], er['city']])
        total += len(tr)
        blocks.append({'t': 'h', 'level': 2, 'text': f'{sec} and its elementary schools ({len(tr)})'})
        blocks.append({'t': 'table', 'caption': f'{sec} family of schools with street addresses', 'head': hd, 'rows': tr, 'source': 'Source: Surrey Schools families of schools (as set out on the South Surrey catchments guide) and the BC Ministry of Education and Child Care school list, read 2026-11-01.'})
    blocks.append({'t': 'p', 'text': ('French Immersion has its own registration. Crescent Park, Jessie Lee, Laronde and Peace Arch Elementary feed French Immersion into Earl Marriott Secondary. '
                                      'The Ministry file also marks Pacific Heights Elementary as offering French Immersion, so ask the district how that program is fed. '
                                      'White Rock is not one catchment: White Rock Elementary feeds Semiahmoo Secondary and Peace Arch Elementary feeds Earl Marriott.')})
    ir = []
    for n in INDEP:
        m = [r for r in pool if _k(r['name']) == _k(n) and r['public_or_private'] != 'Public']
        if not m: raise SystemExit('independent not found: ' + n)
        ir.append([m[0]['name'], m[0]['street_address'], m[0]['city']])
    blocks.append({'t': 'h', 'level': 2, 'text': f'Independent schools in the South Surrey area ({len(ir)})'})
    blocks.append({'t': 'p', 'text': 'Independent schools set their own admission rules and fees, and a home\'s address gives no priority for a place. This is not a full list of independent schools nearby; contact each school directly.'})
    blocks.append({'t': 'table', 'caption': 'Independent schools in the South Surrey area with street addresses', 'head': ['School', 'Street address', 'Community'], 'rows': ir,
                   'source': 'Source: BC Ministry of Education and Child Care school list, read 2026-11-01.'})
    faq = [{'q': 'Which school district covers South Surrey and White Rock?', 'a': 'Both are in School District 36 (Surrey).'},
           {'q': 'Which secondary schools serve South Surrey and White Rock?', 'a': 'Earl Marriott, Elgin Park, Grandview Heights and Semiahmoo Secondary each have a group of feeder elementary schools. Which one applies depends on the exact street address.'},
           {'q': 'Does all of White Rock go to the same secondary school?', 'a': 'No. White Rock Elementary feeds Semiahmoo Secondary, while Peace Arch Elementary feeds Earl Marriott Secondary.'}]
    d = {'status': 'generated', 'slug': 'schools-in-south-surrey-white-rock-bc', 'updated': UPDATED,
         'new_page': {'title': 'Schools in South Surrey & White Rock | Elementary & Secondary List', 'description': f'All {total} public schools in the four South Surrey and White Rock secondary families, with street addresses, plus independent schools. Check any address with the district.', 'h1': 'Schools in South Surrey and White Rock, BC'},
         'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'South Surrey and White Rock schools', 'href': '/schools-in-south-surrey-white-rock-bc.html'}],
         'faq_heading': 'South Surrey and White Rock schools: your questions answered', 'blocks': blocks, 'faq': faq}
    path = os.path.join(ROOT, 'src/data/local/schools-in-south-surrey-white-rock-bc.json')
    json.dump(d, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(path, 'a').write('\n')
    return total


def oxford(ns):
    ns = list(ns)
    return ns[0] if len(ns) == 1 else ' and '.join(ns) if len(ns) == 2 else ', '.join(ns[:-1]) + ' and ' + ns[-1]


if __name__ == '__main__':
    main()
