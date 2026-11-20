"""D-380: Jared's second batch of area overviews (Area-overviews-SEO-batch2.docx, Nov 20 2026), 16 hub pages.
Source text: docs/research/area-overviews/batch2-2026-11-20.md (pandoc of his file). His words are kept; the edits below are
the only changes, each where the site's own sourced data says something different:
  - Panorama Ridge: the City's own Panorama Ridge is the ridge just south of Highway 10, between 120 Street and King George
    Boulevard (panorama-ridge-guide, City park engagement document); the area he describes is the MLS® one. Joe Brown Park
    (125A Street and 54 Avenue) is south of Highway 10, so it is named as such. "(56 Avenue)" dropped: Highway 10 is 58 Avenue there.
    "The City of Surrey refers to it as the Panorama neighbourhood" dropped, since the City's documents use "Panorama Ridge".
  - Fort Langley: the library is in Salishan Place by the River, 23430 Mavis Avenue (FVRL; fort-langley-guide), not on Glover Road.
Links added: the school locator wherever he names it, his "described on the ... page" references, Yorkson, and the area guide
at the end of each overview.
Old archive marketing text whose claims had no source is removed where the overview replaces it: Clayton ("Surrey's
Master-Planned Community"), Panorama Ridge ("Established Estates", "executive homes"), Sullivan Station ("Family Homes in
Sullivan Heights"), Fleetwood ("Surrey's Family Favourite", "consistently ranks among Surrey's most desirable"), and the
Fort Langley page's "Historic Village Charm" (its two links move into the overview).
Run once from the repo root: python3 tools/area_overviews_2_2026_11_20.py
"""
import json, re

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

SD35 = 'https://www.sd35.bc.ca/school-locator'
SD36 = 'https://www.surreyschools.ca/page/78827/school-catchment-locator'

# Section title in his file -> (hub page, area guide)
PAGES = {
    'White Rock': ('white-rock', 'white-rock-guide', 'White Rock guide'),
    'Grandview Heights (Surrey)': ('grandview-surrey', 'grandview-heights-guide', 'Grandview Heights guide'),
    'Morgan Creek (Surrey)': ('morgan-creek', 'morgan-creek-guide', 'Morgan Creek guide'),
    'Crescent Beach / Ocean Park (Surrey)': ('crescent-bch-ocean-pk', 'crescent-beach-ocean-park-guide', 'Crescent Beach and Ocean Park guide'),
    'Walnut Grove (Langley Township)': ('walnut-grove', 'walnut-grove-guide', 'Walnut Grove guide'),
    'Willoughby, including Yorkson (Langley Township)': ('willoughby-heights', 'willoughby-guide', 'Willoughby guide'),
    'Fort Langley (Langley Township)': ('fort-langley', 'fort-langley-guide', 'Fort Langley neighbourhood guide'),
    'Clayton / East Clayton (Surrey)': ('clayton', 'clayton-guide', 'Clayton guide'),
    'Panorama Ridge (Surrey)': ('panorama-ridge', 'panorama-ridge-guide', 'Panorama Ridge guide'),
    'Sullivan Station (Surrey)': ('sullivan-station', 'sullivan-station-guide', 'Sullivan Station guide'),
    'Cloverdale (Surrey)': ('cloverdale-bc', 'cloverdale-bc-guide', 'Cloverdale guide'),
    'Brookswood (Langley Township)': ('brookswood', 'brookswood-guide', 'Brookswood guide'),
    'Aldergrove (Langley Township)': ('aldergrove', 'aldergrove-guide', 'Aldergrove guide'),
    'Langley City': ('langley-city', 'langley-city-guide', 'Langley City guide'),
    'Fleetwood (Surrey)': ('fleetwood-tynehead', 'fleetwood-tynehead-guide', 'Fleetwood Tynehead guide'),
    'Guildford (Surrey)': ('guildford', 'guildford-guide', 'Guildford guide'),
}

EDITS = {
    'Fort Langley (Langley Township)': [
        ('Amenities include the Fort Langley Library on Glover Road,', 'Amenities include the Fort Langley Library, in Salishan Place by the River on Mavis Avenue,'),
    ],
    'Panorama Ridge (Surrey)': [
        (' The City of Surrey refers to it as the Panorama neighbourhood.', ''),
        ('It is generally the area around 64 Avenue, west of 152 Street and north of Highway 10 (56 Avenue). Those edges are approximate, so ask if a specific address is included.',
         'On MLS® it generally covers the area around 64 Avenue, west of 152 Street and north of Highway 10; the City’s own Panorama Ridge is the ridge just south of Highway 10, between 120 Street and King George Boulevard. Those edges are approximate, so ask if a specific address is included.'),
        ('Local parks include Joe Brown Park and Panorama Heights Park.', 'Local parks include Joe Brown Park, just south of Highway 10, and Panorama Heights Park.'),
    ],
}

# Phrases that become links.
LINKS = [
    ('Surrey Schools (SD36) locator', SD36), ('SD35 school locator', SD35),
    ('described on the North Surrey page', None),
]

def clean(s):
    s = s.replace('\\--', '–').replace('---', '—').replace('--', '–').replace("\\'", "'")
    s = s.replace("'", '’')
    return s.strip()

def parts_of(text):
    """Plain text with **bold** leads and link phrases turned into parts."""
    out = []
    for chunk in re.split(r'(\*\*[^*]+\*\*)', text):
        if not chunk: continue
        if chunk.startswith('**'): out.append({'t': chunk.strip('*')}); continue
        pos = 0
        rx = re.compile('|'.join(re.escape(p) for p, _ in LINKS))
        for m in rx.finditer(chunk):
            if m.start() > pos: out.append({'t': chunk[pos:m.start()]})
            ph = m.group(0)
            if ph == 'described on the North Surrey page':
                out += [{'t': 'described on the '}, {'t': 'North Surrey page', 'h': '/north-surrey-homes-for-sale.html'}]
            else:
                out.append({'t': ph, 'h': dict(LINKS)[ph]})
            pos = m.end()
        if pos < len(chunk): out.append({'t': chunk[pos:]})
    # bold area names that have their own page
    for x in out:
        if x['t'] == 'Yorkson' and 'h' not in x: x['h'] = '/yorkson-langley-guide.html'
    # merge adjacent plain parts
    m = []
    for x in out:
        if m and 'h' not in x and 'h' not in m[-1]: m[-1]['t'] += x['t']
        else: m.append(dict(x))
    return m

src = open('docs/research/area-overviews/batch2-2026-11-20.md').read()
secs = re.split(r'^## ', src, flags=re.M)[1:]
done = {}
for sec in secs:
    name, body = sec.split('\n', 1)
    name = name.strip()
    if name not in PAGES: continue
    h2 = clean(re.search(r'\*\*Suggested H2:\*\*\s*(.+)', body).group(1))
    text = body.split('**Keyword phrases:**', 1)[1].split('\n', 1)[1]
    for a, b in EDITS.get(name, []):
        assert a in text.replace('\\--', '--'), (name, a[:40]); text = text.replace(a, b)
    blocks = [{'t': 'h', 'level': 2, 'text': h2}]
    lst = None
    for para in [p.strip() for p in text.split('\n\n') if p.strip()]:
        if para.startswith('-   '):
            item = parts_of(clean(para[4:]))
            if lst is None: lst = {'t': 'list', 'items': []}; blocks.append(lst)
            lst['items'].append(item)
        else:
            lst = None
            blocks.append({'t': 'p', 'parts': parts_of(clean(para))})
    slug, guide, glabel = PAGES[name]
    last = blocks[-1]
    last['parts'] = last['parts'] + [{'t': ' More in my '}, {'t': glabel, 'h': f'/{guide}.html'}, {'t': '.'}]
    if name.startswith('Fort Langley'):
        last['parts'][-1:] = [{'t': ', or see '}, {'t': 'Walnut Grove homes for sale', 'h': '/walnut-grove.html'}, {'t': '.'}]
    for b in blocks:
        if b['t'] == 'p' and all('h' not in x for x in b['parts']): b['text'] = b.pop('parts')[0]['t']
    done[slug] = blocks
assert len(done) == len(PAGES), set(v[0] for v in PAGES.values()) - set(done)

def gen_html(blocks):
    """Fort Langley is a hand-built page: the overview as plain HTML."""
    import html as H
    def ps(b):
        if 'text' in b: return H.escape(b['text'])
        return ''.join(f'<a href="{x["h"]}">{H.escape(x["t"])}</a>' if 'h' in x else H.escape(x['t']) for x in b['parts'])
    body = ''.join(f'        <p>{ps(b)}</p>\n' for b in blocks[1:])
    return ('  <!-- ░░ Living in Fort Langley (Jared’s overview, D-380) ░░ -->\n'
            '  <section class="section" id="living" aria-labelledby="h-living">\n    <div class="wrap">\n'
            f'      <h2 id="h-living" class="h2">{H.escape(blocks[0]["text"])}</h2>\n      <div class="prose">\n{body}      </div>\n    </div>\n  </section>\n\n')

for slug, blocks in done.items():
    if slug == 'fort-langley':
        p = 'src/pages/fort-langley.astro'; s = open(p).read()
        if 'id="h-living"' not in s:
            s = s.replace('  <!-- ░░ Market ░░ -->\n', gen_html(blocks) + '  <!-- ░░ Market ░░ -->\n', 1)
            s = re.sub(r'\n  <section class="section" aria-labelledby="h-charm">.*?</section>\n', '\n', s, count=1, flags=re.S)
            open(p, 'w').write(s); print('overview added: fort-langley (astro)')
        continue
    p = f'src/data/local/{slug}.json'; d = load(p)
    if any(b.get('gen') == 'ov1120' for b in d['blocks']): continue
    d['blocks'] = [dict(b, gen='ov1120') for b in blocks] + d['blocks']
    save(p, d); print('overview added:', slug)

# Old unsourced archive text the overviews replace (H3 and its paragraphs).
OLD = {'clayton': "Clayton: Surrey's Master-Planned Community", 'panorama-ridge': 'Panorama Ridge: Established Estates in Surrey',
       'sullivan-station': 'Sullivan Station: Family Homes in Sullivan Heights', 'fleetwood-tynehead': "Fleetwood-Tynehead: Surrey's Family Favourite"}
for slug, head in OLD.items():
    p = f'src/data/pages/{slug}.json'; d = load(p); out, skip = [], False
    for b in d['blocks']:
        if b['t'] == 'h': skip = b.get('text') == head
        if not skip: out.append(b)
    if len(out) != len(d['blocks']): d['blocks'] = out; save(p, d); print('removed old text:', slug)
