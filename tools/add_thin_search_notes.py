#!/usr/bin/env python3
"""Adds one short paragraph under the live-listings widget on pages whose saved search had fewer than 5 listings when it was built
(Jerry's worksheets in docs/review/idx, Status "under 5" or Count < 5). The paragraph tells the visitor the search may be short, links to the
city's listings page and neighbourhood map, and offers a saved search. Idempotent: rewrites its own block (gen 'thin'). Run after the other build_* generators.
  python3 -I tools/add_thin_search_notes.py"""
import json, os, re, openpyxl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'docs/review/idx')
SHEETS = (('houses-searches-2026-11-04.xlsx', 'Houses searches', 'houses'), ('condos-townhomes-searches-2026-11-05.xlsx', 'Condos & townhomes searches', 'condos and townhomes'),
          ('area-searches-2026-11-05.xlsx', 'Area searches', 'homes'))
CITIES = {'coquitlam': 'Coquitlam', 'burnaby': 'Burnaby', 'port-moody': 'Port Moody', 'abbotsford': 'Abbotsford', 'surrey': 'Surrey',
          'port-coquitlam': 'Port Coquitlam', 'new-westminster': 'New Westminster', 'langley': 'Langley'}
VAR = ["Few {t} are listed in {a} right now, so this {a} search may be short. {c} and I will save it for you.",
       "{a} has only a handful of {t} on the market today. {c} and I will send each new {a} listing as it appears.",
       "This {a} list is short at the moment. {c} and I will watch {a} for you and send new listings early."]
def exists(s): return os.path.exists(os.path.join(ROOT, 'src/data/local', s + '.json'))
def main():
    n = 0
    for fn, sheet, kind in SHEETS:
        for r in list(openpyxl.load_workbook(os.path.join(D, fn), read_only=True)[sheet].iter_rows(values_only=True))[1:]:
            if not r[0] or not (r[10] or '').startswith('Built'): continue
            if not ('under 5' in (r[10] or '') or 'under 5' in (r[8] or '') or int(r[9] or 99) < 5): continue
            slug = re.sub(r'\.html$', '', (r[3] or '').strip().lstrip('/')); fp = os.path.join(ROOT, 'src/data/local', slug + '.json')
            if not os.path.exists(fp): print('NO PAGE', slug); continue
            area = r[0].split(',')[0].strip(); tail = r[0].split(',')[1]
            city = next((CITIES[c] for c in sorted(CITIES, key=len, reverse=True) if tail.strip().startswith(CITIES[c])), None)
            if not city: print('NO CITY', r[0]); continue
            cs = next(c for c in CITIES if CITIES[c] == city)
            links = [{'t': f'{city} homes for sale', 'h': f'/{cs}-homes-for-sale.html'}]
            if exists(f'{cs}-neighbourhood-guides'): links.append({'t': f'the {city} neighbourhood map', 'h': f'/{cs}-neighbourhood-guides.html'})
            j = json.load(open(fp)); blocks = [b for b in j['blocks'] if b.get('gen') != 'thin']
            gi = next((i for i, b in enumerate(blocks) if b.get('t') == 'grid'), None)
            if gi is None: print('NO GRID', slug); continue
            txt = VAR[sum(map(ord, slug)) % 3]; fmt = dict(t=kind, a=area)
            pre, post = txt.split('{c}')
            parts = [{'t': pre.format(**fmt)}, {'t': 'Contact me', 'h': '/contact.html'}, {'t': post.format(**fmt)}]
            blocks.insert(gi + 1, {'t': 'p', 'parts': parts, 'gen': 'thin'})
            blocks.insert(gi + 2, {'t': 'list', 'items': [[l] for l in links], 'gen': 'thin'})
            j['blocks'] = blocks; json.dump(j, open(fp, 'w'), ensure_ascii=False, indent=1); n += 1
    print(n, 'pages updated')
if __name__ == '__main__': main()
