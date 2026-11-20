"""D-382: Jared's third batch of area overviews (Area-overviews-SEO-batch3.docx, Nov 20 2026).
Source text: docs/research/area-overviews/batch3-2026-11-20.md. His words are kept; every fact checked against the sources the
area guides already cite (Sunnyside Park pool, Historic Stewart Farm 1894, King George Corridor plan bounds, Rosemary Heights
bounds, Xw'epiteng Elementary at 18035 8 Avenue, Rowlatt Farmstead, Fraser Heights schools and rec centre, West Newton plan
bounds and schools). No edits were needed.
Three of his sections pair two areas that have separate pages, so each page gets the shared opening, its own area's part, and
the shared closing, under an H2 naming that area:
  Sunnyside / Elgin-Chantrell  -> sunnyside-park-surrey, elgin-chantrell
  Rosemary Heights / King George Corridor -> king-george-corridor (both parts), rosemary-heights-guide (Rosemary Heights part)
  Hazelmere / Campbell Valley  -> hazelmere, campbell-valley
Fraser Heights and West Newton go on their hub pages whole. Old unsourced archive text removed: Campbell Valley ("Langley's
Rural Escape") and West Newton ("Surrey's Affordable Family Hub").
Run once from the repo root: python3 tools/area_overviews_3_2026_11_20.py
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
LINKS = [('Surrey Schools (SD36) locator', SD36), ('SD35 school locator', SD35)]

def clean(s):
    s = s.replace('\\--', '–').replace('---', '—').replace('--', '–').replace("\\'", "'").replace("'", '’')
    return s.strip()

def parts_of(text):
    text = re.sub(r'^\*\*([^*]+)\*\*\s*', r'\1 ', text)      # a bullet's bold lead ("Rosemary Heights.") stays as plain text
    rx = re.compile('|'.join(re.escape(p) for p, _ in LINKS)); out, pos = [], 0
    for m in rx.finditer(text):
        if m.start() > pos: out.append({'t': text[pos:m.start()]})
        out.append({'t': m.group(0), 'h': dict(LINKS)[m.group(0)]}); pos = m.end()
    if pos < len(text): out.append({'t': text[pos:]})
    return out

src = open('docs/research/area-overviews/batch3-2026-11-20.md').read()
SEC = {}
for sec in re.split(r'^## ', src, flags=re.M)[1:]:
    name, body = sec.split('\n', 1)
    if '**Keyword phrases:**' not in body: continue
    text = body.split('**Keyword phrases:**', 1)[1].split('\n', 1)[1]
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    SEC[name.strip()] = {'intro': [p for p in paras[:1]], 'bullets': [p[4:] for p in paras if p.startswith('-   ')],
                         'rest': [p for p in paras[1:] if not p.startswith('-   ')], 'all': paras}

def para(t): return {'t': 'p', 'parts': parts_of(clean(t))}

def build(h2, paras, guide=None, glabel=None):
    blocks = [{'t': 'h', 'level': 2, 'text': h2}] + [para(p) for p in paras]
    if guide: blocks[-1]['parts'] += [{'t': ' More in my '}, {'t': glabel, 'h': f'/{guide}.html'}, {'t': '.'}]
    for b in blocks:
        if b['t'] == 'p' and all('h' not in x for x in b['parts']): b['text'] = ''.join(x['t'] for x in b.pop('parts'))
    return blocks

S = SEC['Sunnyside / Elgin-Chantrell (South Surrey)']
R = SEC['Rosemary Heights / King George Corridor (South Surrey)']
H = SEC['Hazelmere and Campbell Valley (South Surrey / Langley Township)']
F = SEC['Fraser Heights (Surrey)']; W = SEC['West Newton (Surrey)']
rh_close, kgc_close = re.split(r'(?<=\.)\s+(?=The King George Corridor is)', R['rest'][1])

PAGES = {
    'sunnyside-park-surrey': build('Living in Sunnyside, Surrey', S['intro'] + [S['bullets'][0]] + S['rest'], 'sunnyside-park-surrey-guide', 'Sunnyside Park guide'),
    'elgin-chantrell': build('Living in Elgin-Chantrell, Surrey', S['intro'] + [S['bullets'][1]] + S['rest'], 'elgin-chantrell-guide', 'Elgin-Chantrell guide'),
    'king-george-corridor': build('Living in the King George Corridor and Rosemary Heights, Surrey', R['intro'] + [R['bullets'][1], R['bullets'][0], R['rest'][0], kgc_close + ' ' + rh_close],
                                  'king-george-corridor-guide', 'King George Corridor guide'),
    'rosemary-heights-guide': build('Living in Rosemary Heights, Surrey', R['intro'] + [R['bullets'][0], R['rest'][0], rh_close]),
    'hazelmere': build('Living in Hazelmere, Surrey', H['intro'] + [H['bullets'][0]] + H['rest'], 'hazelmere-guide', 'Hazelmere guide'),
    'campbell-valley': build('Living in Campbell Valley, Langley', H['intro'] + [H['bullets'][1]] + H['rest'], 'campbell-valley-guide', 'Campbell Valley guide'),
    'fraser-heights': build('Living in Fraser Heights, Surrey', F['all'], 'fraser-heights-guide', 'Fraser Heights guide'),
    'west-newton': build('Living in West Newton, Surrey', W['all'], 'west-newton-guide', 'West Newton guide'),
}
for slug, blocks in PAGES.items():
    p = f'src/data/local/{slug}.json'; d = load(p)
    if any(b.get('gen') == 'ov1120b' for b in d['blocks']): continue
    d['blocks'] = [dict(b, gen='ov1120b') for b in blocks] + d['blocks']
    save(p, d); print('overview added:', slug, len(blocks) - 1, 'paragraphs')

OLD = {'campbell-valley': "Campbell Valley: Langley's Rural Escape", 'west-newton': "West Newton: Surrey's Affordable Family Hub"}
for slug, head in OLD.items():
    p = f'src/data/pages/{slug}.json'; d = load(p); out, skip = [], False
    for b in d['blocks']:
        if b['t'] == 'h': skip = b.get('text') == head
        if not skip: out.append(b)
    if len(out) != len(d['blocks']): d['blocks'] = out; save(p, d); print('removed old text:', slug)
