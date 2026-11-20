"""D-383: Jared's area overviews for every remaining area page (Jared-area-overviews-all.zip, Nov 20 2026, batches 4-21:
core leftovers, Delta, Abbotsford, Chilliwack, Maple Ridge, Mission, Pitt Meadows, Agassiz/Harrison, Hope, Vancouver, Burnaby,
Richmond, Coquitlam, North Vancouver, West Vancouver, New Westminster, Port Coquitlam, Port Moody).
Source text: docs/research/area-overviews/batch4..21 (pandoc of his files; table-layout artifacts in batches 14-21 cleaned:
table rules, cell indents, escaped headings, and one Burnaby paragraph that had been styled as a heading).

- Each section goes on the page his file names (checked against the area map's link for that area: all match) as the first
  section under the H1, under his suggested H2. Pages that cover several of his areas (Hope, Cultus Lake, Harrison Hot Springs,
  Mount Pleasant) get one section per area, in his order.
- His words are kept. 834 named schools, parks, community centres and street addresses were checked against the site's sourced
  data; the 95 not already in it are real, well-known places (Queen Elizabeth Park, Minoru Park, Manning Park ...) and a few
  addresses checked by hand (Marpole Community Centre at 7780 Oak Street, the Otter Co-op at 3650 248 Street).
- His suggested meta title and description are applied only to pages Google has not shown yet (Search Console, Nov 12-18):
  the current titles of pages that already get views stay. Pages with several of his sections keep their titles.
- The school-locator phrase he uses links to the district's catchment page where the site already cites one (SD34-39, SD42).
- Old archive marketing text the overviews replace is removed on 13 pages ("Mission's Lakeside Gem", "Surrey's Nature
  Escape", "Langley's Rural Beauty" ...): none of its claims were sourced.
Run once from the repo root: python3 tools/area_overviews_all_2026_11_20.py <map.json> <pages-not-in-top-20.csv>
"""
import csv, json, os, re, sys, html

_FMT = {}
def load(p):
    raw = open(p).read(); d = json.loads(raw)
    for st in (dict(indent=None, separators=(',', ':')), dict(indent=None), dict(indent=1), dict(indent=2), dict(indent=0)):
        for ea in (False, True):
            for tail in ('', '\n'):
                if json.dumps(d, ensure_ascii=ea, **st) + tail == raw: _FMT[p] = (st, ea, tail); return d
    raise SystemExit(f'format not matched: {p}')
def save(p, d):
    st, ea, tail = _FMT[p]; open(p, 'w').write(json.dumps(d, ensure_ascii=ea, **st) + tail)

MAP = json.load(open(sys.argv[1]))
NOVIEWS = {r['Page'].split('/')[-1][:-5] for r in csv.DictReader(open(sys.argv[2])) if r['Status'].startswith('No Google views')}

LOC = {'34': 'https://www.abbyschools.ca/schools/catchments', '35': 'https://www.sd35.bc.ca/school-locator',
       '36': 'https://www.surreyschools.ca/page/78827/school-catchment-locator', '37': 'https://www.deltasd.bc.ca/schools/school-locator/',
       '38': 'https://sd38.bc.ca/schools/locations-catchments', '39': 'https://vsb.bc.ca/catchment-boundaries', '42': 'https://www.sd42.ca/school-locator/'}
LOCRX = re.compile(r"((?:[A-Z][\w–-]*\s)*(?:School District\s|Schools\s|School Board\s)?\(?SD(\d\d)\)?\s(?:school\s)?locator)")

def clean(s):
    s = s.replace('\\|', '|').replace('\\--', '–').replace('---', '—').replace('--', '–').replace("\\'", "'").replace('\\', '')
    return s.replace("'", '’').strip()

def parts_of(text):
    text = re.sub(r'^\*\*([^*]+)\*\*\s*', r'\1 ', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    out, pos = [], 0
    for m in LOCRX.finditer(text):
        url = LOC.get(m.group(2))
        if not url: continue
        if m.start() > pos: out.append({'t': text[pos:m.start()]})
        out.append({'t': m.group(1), 'h': url}); pos = m.end()
    if pos < len(text): out.append({'t': text[pos:]})
    return out

def section(body):
    h2 = clean(re.search(r'\*\*Suggested H2:\*\*\s*(.+)', body).group(1))
    mt = re.search(r'\*\*Suggested meta title:\*\*\s*(.+)', body); md = re.search(r'\*\*Suggested meta description:\*\*\s*(.+)', body)
    text = body.split('**Keyword phrases:**', 1)[1].split('\n', 1)[1]
    blocks = [{'t': 'h', 'level': 2, 'text': h2}]; lst = None
    for para in [p.strip() for p in text.split('\n\n') if p.strip()]:
        if para.startswith('-   '):
            if lst is None: lst = {'t': 'list', 'items': []}; blocks.append(lst)
            lst['items'].append(parts_of(clean(para[4:])))
        else:
            lst = None; blocks.append({'t': 'p', 'parts': parts_of(clean(para))})
    for b in blocks:
        if b['t'] == 'p' and all('h' not in x for x in b['parts']): b['text'] = ''.join(x['t'] for x in b.pop('parts'))
    return blocks, (clean(mt.group(1)) if mt else None), (clean(md.group(1)) if md else None)

secs = {}
for o in MAP:
    for sec in re.split(r'^## ', open(o['file']).read(), flags=re.M)[1:]:
        name, body = sec.split('\n', 1)
        if name.strip() == o['name'] and 'Suggested H2' in body: secs[(o['file'], o['name'])] = body

by_page = {}
for o in MAP: by_page.setdefault(o['page'], []).append(o)

sf = load('src/data/seo-final.json'); titled = 0
for page, items in by_page.items():
    p = f'src/data/local/{page}.json'; d = load(p)
    if any(b.get('gen') == 'ov1120c' for b in d['blocks']): continue
    new = []; metas = []
    for o in items:
        blocks, mt, md = section(secs[(o['file'], o['name'])]); new += blocks; metas.append((mt, md))
    guide = f'{page}-guide'
    if os.path.exists(f'dist/{guide}.html') and not page.endswith('-guide'):
        last = next(b for b in reversed(new) if b['t'] == 'p')
        if 'text' in last: last['parts'] = [{'t': last.pop('text')}]
        g = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', open(f'dist/{guide}.html').read(), re.S).group(1))).strip()
        last['parts'] += [{'t': ' More in my guide: '}, {'t': g, 'h': f'/{guide}.html'}, {'t': '.'}]
    d['blocks'] = [dict(b, gen='ov1120c') for b in new] + d['blocks']; save(p, d)
    if len(items) == 1 and page in NOVIEWS and page in sf:
        mt, md = metas[0]
        if mt and len(mt) <= 60: sf[page]['title'] = mt; titled += 1
        if md and len(md) <= 160: sf[page]['description'] = md
save('src/data/seo-final.json', sf)
print('pages:', len(by_page), 'sections:', len(MAP), 'titles applied:', titled)

FLUFF = {'bear-creek-green-timbers': "Bear Creek & Green Timbers: Surrey's Nature Escape", 'chilliwack-downtown': 'Chilliwack Downtown: Urban Revival',
         'chilliwack-proper-south': 'Chilliwack Proper South: Established Family Living', 'county-line-glen-valley': "County Line & Glen Valley: Langley's Rural Beauty",
         'dewdney-deroche': "Dewdney-Deroche: Mission's Rural Frontier", 'durieu': 'Durieu: Acreage and Outdoor Lifestyle', 'hatzic': "Hatzic: Mission's Lakeside Living",
         'lake-errock': "Lake Errock: Mission's Lakeside Gem", 'mission-bc': 'Mission, BC: Scenic Views and Room to Grow', 'mission-west': 'Mission West: Scenic and Established',
         'serpentine': "Serpentine: Surrey's Equestrian Country", 'stave-falls': "Stave Falls: Mission's Waterfront Community", 'anmore-homes-for-sale': 'Anmore: Mountain Village Living'}
for slug, head in FLUFF.items():
    p = f'src/data/pages/{slug}.json'; d = load(p); out, skip = [], False
    for b in d['blocks']:
        if b['t'] == 'h': skip = b.get('text') == head
        if not skip: out.append(b)
    if len(out) != len(d['blocks']): d['blocks'] = out; save(p, d)
    else: print('not found:', slug)
