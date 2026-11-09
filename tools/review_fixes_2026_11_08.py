"""One-off clean-up from the 2026-11-08 review of the new pages (D-188). Idempotent; edits src/data/local/*.json in place without trimming text pieces
(a piece such as " using its" sits between two links and its spaces matter).  Run: python3 -I tools/review_fixes_2026_11_08.py"""
import glob, json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
L = os.path.join(ROOT, 'src/data/local')
def load(s): return json.load(open(f'{L}/{s}.json', encoding='utf-8'))
def save(s, d):
    with open(f'{L}/{s}.json', 'w', encoding='utf-8') as f: json.dump(d, f, ensure_ascii=False, indent=1); f.write('\n')

# 1. breadcrumbs: guide pages hang off the city's guide hub (or sentence-case city page), never a "Condos For Sale" page or the home page
HUB = {'abbotsford': ('Abbotsford neighbourhood guides', 'abbotsford-neighbourhood-guides'), 'chilliwack': ('Chilliwack neighbourhood guides', 'chilliwack-neighbourhood-guides'),
       'surrey': ('Surrey neighbourhood guides', 'surrey-neighbourhood-guides'), 'richmond': ('Richmond neighbourhood guides', 'richmond-neighbourhood-guides'),
       'new-westminster': ('New Westminster neighbourhood guides', 'new-westminster-neighbourhood-guides'), 'vancouver': ('Vancouver neighbourhood guides', 'vancouver-neighbourhood-guides'),
       'north-vancouver': ('North Vancouver homes', 'north-vancouver-homes-for-sale'), 'west-vancouver': ('West Vancouver homes', 'west-vancouver-homes-for-sale')}
M = {'agassiz-bc-guide': 'chilliwack', 'harrison-hot-springs-bc-guide': 'chilliwack', 'hope-bc-guide': 'chilliwack', 'kent-bc-guide': 'chilliwack', 'lindell-beach-bc-guide': 'chilliwack',
     'mt-lehman-abbotsford-guide': 'abbotsford', 'barnston-island-surrey-guide': 'surrey', 'brighouse-richmond-guide': 'richmond', 'south-arm-richmond-guide': 'richmond',
     'brunette-new-westminster-guide': 'new-westminster', 'furry-creek-bc-guide': 'west-vancouver'}
for f in glob.glob(f'{L}/*-guide.json'):
    s = os.path.basename(f)[:-5]
    k = M.get(s) or ('north-vancouver' if s.endswith('north-vancouver-guide') else 'west-vancouver' if s.endswith('west-vancouver-guide') else 'vancouver' if s.endswith('-vancouver-guide') else None)
    if not k: continue
    d = load(s); b = d.get('breadcrumbs')
    if b and len(b) == 3 and 'For Sale' in b[1]['name']: b[1] = {'name': HUB[k][0], 'href': f'/{HUB[k][1]}.html'}; save(s, d)
d = load('mount-currie-bc-guide'); b = d['breadcrumbs']
if 'For Sale' in b[1]['name']: b[1] = {'name': 'BC land buying rules', 'href': '/bc-land-buying-rules.html'}; save('mount-currie-bc-guide', d)
for s, t in {'edgemont-55-plus-homes-for-sale': 'edgemont-north-vancouver-guide', 'fort-langley-55-plus-homes-for-sale': 'fort-langley', 'south-cambie-55-plus-homes-for-sale': 'south-cambie-vancouver-guide',
             'university-vw-55-plus-homes-for-sale': 'university-endowment-lands-vancouver-guide', 'upper-lonsdale-55-plus-homes-for-sale': 'upper-lonsdale-north-vancouver-guide',
             'whitby-estates-55-plus-homes-for-sale': 'whitby-estates-west-vancouver-guide'}.items():
    d = load(s)
    if d['breadcrumbs'][1]['href'] == '/index.html': d['breadcrumbs'][1]['href'] = f'/{t}.html'; save(s, d)


# slugs of other pages written into prose (research shorthand) -> plain wording
SLUGPROSE = [
 (' (the same address appears in the surrey-mobile-homes feed)', ''),
 (' that also appear in the surrey-mobile-homes feed', ' that also appear in Surrey mobile-home listings'),
 ('Named once here, with detail in the earlier highgate-burnaby-condos-townhomes-for-sale and highgate-burnaby notes:', 'Named once here:'),
 ('Home-type detail is in the sardis-condos-for-sale, sardis-townhomes-for-sale and sardis-houses-for-sale notes.', 'Home-type detail is on the Sardis condos, townhomes and houses pages.'),
 ('City-wide rules are in the chilliwack-houses-for-sale and chilliwack-duplexes-for-sale notes.', 'City-wide rules are on the Chilliwack houses and duplexes pages.'),
 (' (central-park-bs)', ''),
 ('see the sunnyside-park-south-surrey-houses-for-sale and king-george-corridor-south-surrey-houses-for-sale notes.', 'see the Sunnyside Park and King George Corridor house pages.'),
 ('on the surrey-homes-for-sale feed only', 'in Surrey home listings only'),
 ('while the tsawwassen-east-guide land home asserts 8288 in governing terms. ( disk-checked as the guide land home for that ground.)', 'while the Tsawwassen East guide asserts 8288 in governing terms.'),
 ('carried in the east-newton-guide and east-newton notes.', 'carried on the East Newton guide and area pages.'),
 ('(see sardis-condos-for-sale)', '(see the Sardis condos page)'),
 ('see sardis-condos-for-sale.', 'see the Sardis condos page.'),
 ('see the coquitlam-homes-for-sale condos documentation for the buildings', 'see the Coquitlam condos page for the buildings'),
 ('on the mission-west and mission-mobile-homes feeds and "Stave Falls" on the stave-falls feed', 'in the Mission West and Mission mobile-home listings and "Stave Falls" in the Stave Falls listings'),
 ('It is not the same page as campbell-valley-acreages-farms-for-sale, the separate topic feed page.', 'It is not the same page as the Campbell Valley acreages and farms page.'),
 ('and covered in the albion-maple-ridge-houses-for-sale, east-central-maple-ridge-houses-for-sale and thornhill-maple-ridge-houses-for-sale notes.', 'and covered on the Albion, East Central and Thornhill house pages.'),
]

# 2. text repairs (strings are changed in place, never trimmed)
def fix(s):
    o = s
    s = re.sub(r'\s*\.?\s*and Persons with\s*$', '.', s)
    s = re.sub(r'\.\s+and\s+\($', '.', s)
    if re.search(r'[.:]\s+and\s*$', s): s = re.sub(r'\s*\.?\s+and\s*$', '.', s)
    s = re.sub(r'\s+\($', '', s)
    s = re.sub(r'^\(\s+(?=[A-Z])', '', s)
    if s.rstrip().endswith('Act, s. 11'): s = s.rstrip() + ').'
    if s.count('(') > s.count(')'):
        def rep(m):
            before, nxt = m.group(1), m.group(2)
            if nxt.lower() == 'and' or nxt[0].islower(): return before + ', ' + nxt
            return before + (', ' if re.search(r'\b[A-Z][a-z]*$', before) else '. ') + nxt
        s = re.sub(r'(\S) \( (\S+)', rep, s, count=s.count('(') - s.count(')'))
    if s != o and not re.search(r'[.!?:”")]$', s): s = s.rstrip(', ') + '.'
    # citations whose closing part was lost: close them or drop the dangling bit
    s = re.sub(r'\s*\(55\+ notes\s*$', '', s)
    s = re.sub(r'\(SnapStats (?:FVR|GVR) (\w+ 20\d\d) report\s*$', r'(SnapStats, \1)', s)
    if s.count('(') > s.count(')'):
        s = re.sub(r'\s*\(i\.e\. (?=[A-Z])', '. ', s, count=1)
        s = re.sub(r'\(([^()]{3,80}?) (?:s|ss|sec|Sec)\. (?=[A-Z])', r'(\1). ', s, count=1)
    if s.count('(') > s.count(')'):
        s = re.sub(r'\(([^():]{3,80}): (?=[A-Z][a-z])', r'(\1). ', s, count=1)
    if s.count('(') > s.count(')'):
        i = s.rfind('(')
        if ')' not in s[i:] and len(s) - i <= 90 and i > 20: s = s[:i].rstrip(' ,;:') + ('.' if not re.search(r'[.!?]$', s[:i].rstrip()) else '')
    s = re.sub(r'\b([Aa]) (?=(?:Abbotsford|Aldergrove|Anmore|Agassiz|Ambleside|Annieville|Albion|Aberdeen)\b)', lambda m: ('An' if m.group(1) == 'A' else 'an') + ' ', s)
    s = re.sub(r'(?<![\d.])\b1 (years|bedrooms|bathrooms)\b', lambda m: '1 ' + m.group(1)[:-1], s)
    s = re.sub(r'(20\d\d\.) ([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), s)
    for a, b in SLUGPROSE: s = s.replace(a, b)
    if s.startswith(': a name that surfaced'): s = 'A name' + s[len(': a name'):]
    s = s.replace('workshop. provincial law', 'workshop. Provincial law').replace('east-side side streets', 'east-side streets')
    s = s.replace('official Official Community Plan', 'official Community Plan').replace('(MLS® )', '(MLS®)').replace('MLS® and ) — strata tenure', 'MLS® — strata tenure').replace('recreation center', 'recreation centre')
    s = s.replace('LINDELL BEACH condos home ( — which counts 0 apartment condos for this ground) and carried in the townhomes home ( — which counts 0 townhouse-form complexes).', 'Lindell Beach condos page (which counts 0 apartment condos for this ground) and carried in the townhomes page (which counts 0 townhouse-form complexes).')
    s = s.replace('through the Form B (SPA s. ', 'through the Form B (Strata Property Act). ').replace('(Taxation (Rural Area) Act s. Mission taxes', '(Taxation (Rural Area) Act). Mission taxes')
    s = s.replace('age restrictions. —', 'age restrictions —').replace('Fairview only. —', 'Fairview only —')
    s = s.replace('5535 Admiral Way. Fairwinds', '5535 Admiral Way, Fairwinds').replace('5550 Admiral Way. Beaufort', '5550 Admiral Way, Beaufort')
    return s
def walk(o):
    if isinstance(o, str): return fix(o)
    if isinstance(o, dict): return {k: walk(v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v) for v in o]
    return o
n = 0
for f in glob.glob(f'{L}/*.json'):
    d = json.load(open(f, encoding='utf-8'))
    # notes left in the page: "Internal links: slug-a — ..." lists
    for b in d.get('blocks', []):
        if b.get('t') == 'list': b['items'] = [it for it in b['items'] if not re.search(r'^\s*Internal links?:|^\s*[a-z0-9]+(?:-[a-z0-9]+){2,} — ', ' '.join(x.get('t', '') for x in it))]
    d['blocks'] = [b for b in d.get('blocks', []) if not (b.get('t') == 'list' and not b['items'])]
    r = walk(d)
    if r != json.load(open(f, encoding='utf-8')): json.dump(r, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(f, 'a').write('\n'); n += 1
print('local files changed:', n)
