#!/usr/bin/env python3
"""Zoning directory data (D-268).

The old /zonings.html was an interactive directory (filters, 278 zone cards). The archive captured it as 2,000 flat blocks, so the
rebuilt page showed the filter controls as a plain list and every zone as loose paragraphs. This reads the archive record and
writes the same wording as structured data for src/components/ZoningPage.astro:

    python3 -I tools/build_zonings.py        -> src/data/zonings.json

Nothing is reworded. Labels whose value the archive lost (a bare "Min. new lot") are dropped rather than shown empty.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = json.loads((ROOT / 'src/data/pages/zonings.json').read_text())['blocks']
OUT = ROOT / 'src/data/zonings.json'
TYPES = ('Agricultural / Farm', 'Rural / Acreage', 'Residential', 'Other')
LABELS = {'Intent', 'Min. new lot', 'Main uses', 'ALR', 'Purpose', 'Min. lot', 'Homes', 'Extra homes', 'Also allowed', 'Subdivision',
          'Agriculture', 'Floodplain', 'Farm home plate', 'Limits', 'Principal use', 'Lot coverage'}
CHECKED = 'Checked Oct 2, 2026'


def tx(b):
    return b.get('text') or ''.join(p['t'] for p in b.get('parts', []))


def parts(b):
    """Text with its links, as [{t, h?}] (site links made relative)."""
    out = []
    for p in b.get('parts') or [{'t': b.get('text', '')}]:
        t = p['t'].strip(' |') if not p.get('h') else p['t']
        m = re.match(r'^(.*?)<((?:https?|tel|mailto):[^>]+)>$', p['t'])
        if m and not p.get('h'):
            p = {'t': m.group(1), 'h': m.group(2)}
        if p.get('h'):
            out.append({'t': p['t'].strip(), 'h': re.sub(r'^https://jaredgibbons\.ca(?=/)', '', p['h'])})
        elif t.strip():
            out.append({'t': p['t'].replace(' | ', ' ').strip(' |')})
    return out


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def h2_at(text):
    return next(i for i, b in enumerate(B) if b['t'] == 'h' and b.get('level') == 2 and b.get('text') == text)


# --- municipalities and zones ---------------------------------------------------------------------------------------------
starts = [i for i, b in enumerate(B) if b['t'] == 'h' and b.get('level') == 2 and b.get('text', '').endswith(' zoning')]
end_all = h2_at('ALR basics')
munis = []
for n, s in enumerate(starts):
    e = starts[n + 1] if n + 1 < len(starts) else end_all
    name = B[s]['text'][:-len(' zoning')]
    mid = B[s].get('id') or 'zd-' + slug(name).replace('township-of-', '').replace('-', '')
    bp = B[s + 1]['parts']
    card = B[s + 2]
    assert card['t'] == 'card', name
    m = {'id': mid, 'name': name, 'bylaw': bp[0]['t'].strip(), 'source': ''.join(p['t'] for p in bp[1:]).lstrip('. ').strip(),
         'href': card['href'], 'zones': []}
    kind = None
    i = s + 3
    while i < e:
        b = B[i]
        t = tx(b)
        if b['t'] == 'list':
            for it in b['items']:
                if it[0]['t'] in TYPES:
                    kind = it[0]['t']
        elif b['t'] == 'p' and t in TYPES:
            kind = t
        elif b['t'] == 'h' and b.get('level') == 3:
            name3 = b['text']
            code = name3.split(' ', 1)[0]
            z = {'id': f"{mid}-{slug(code)}", 'code': code, 'name': name3[len(code):].strip(), 'type': kind, 'fields': []}
            j = i + 1
            while B[j]['t'] != 'card':
                s3 = tx(B[j])
                if s3.startswith('Formerly'):
                    z['formerly'] = s3[len('Formerly'):].strip()
                elif s3 in LABELS:
                    z['fields'].append([s3, ''])
                elif s3.startswith('Note:'):
                    z['note'] = s3[len('Note:'):].strip()
                else:
                    assert z['fields'], (name3, s3)
                    z['fields'][-1][1] = (z['fields'][-1][1] + ' ' + s3).strip()
                j += 1
            z['fields'] = [f for f in z['fields'] if f[1]]
            z['href'] = B[j]['href']
            z['ref'] = B[j]['lines'][0]['text'].replace('Official bylaw, ', '')
            assert tx(B[j + 1]) == CHECKED or (B[j + 1]['t'] == 'list' and B[j + 1]['items'][0][0]['t'] == CHECKED), name3
            m['zones'].append(z)
            i = j
        i += 1
    # unique ids inside a municipality (two zones can share a code prefix)
    seen = {}
    for z in m['zones']:
        k = z['id']; seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1:
            z['id'] = f"{k}-{seen[k]}"
    munis.append(m)

# --- the rest of the page ----------------------------------------------------------------------------------------------------
a = h2_at('ALR basics')
alr = {'paras': [tx(B[k]) for k in range(a + 1, a + 6)],
       'links': [{'t': it[0]['t'], 'h': it[0]['h']} for it in B[a + 6]['items']],
       'source': tx(B[a + 7])}
c = h2_at('Before you buy: what to check')
checks = []
k = c + 1
while tx(B[k]) != 'Send me an address':
    checks.append({'k': tx(B[k]).rstrip('.'), 'd': parts(B[k + 1])})
    k += 2
r = h2_at('Related guides and listings')
related = [{'t': it[0]['t'], 'h': re.sub(r'^https://jaredgibbons\.ca(?=/)', '', it[0]['h'])} for it in B[r + 1]['items']]
d = h2_at('Disclaimer')

data = {
    'eyebrow': tx(B[1]),
    'h2': tx(B[2]),
    'lead': tx(B[3]),
    'checked': tx(B[4]),
    'general': [tx(B[6]), tx(B[7])],
    'lookup': {'h': tx(B[8]), 'd': tx(B[9]), 'labels': B[10]['labels'], 'submit': B[10]['submit'], 'fine': tx(B[12]).replace(' Prefer to write directly?', '')},
    'types': list(TYPES),
    'munis': munis,
    'alr': alr,
    'checks': checks,
    'related': related,
    'disclaimer': tx(B[d + 1]),
}
total = sum(len(m['zones']) for m in munis)
assert total == 278, total
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
print(f'{len(munis)} municipalities, {total} zones -> {OUT.relative_to(ROOT)}')
for m in munis:
    print(f"  {m['id']:16} {m['name']:22} {len(m['zones'])}")
