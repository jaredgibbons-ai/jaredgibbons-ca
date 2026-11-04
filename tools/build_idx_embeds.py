#!/usr/bin/env python3
"""Reads the MyRealPage embed worksheet and writes src/data/idx-embeds.json.

pages   : {slug: search id} for pages that already exist on the site (one search per page)
pending : searches for new pages that are NOT wired up (names and addresses disagree, copy not written)
Only the numeric search id is stored; the account id is public in the embed code.
"""
import json, os, re, sys, glob, collections
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, 'docs/review/idx/embed-list-2026-11-04.xlsx')
OUT = os.path.join(ROOT, 'src/data/idx-embeds.json')
ACCOUNT = '67649'
NC_XLSX = os.path.join(ROOT, 'docs/review/idx/new-construction-searches-2026-11-04.xlsx')
NC_ADDR_FIX = {'sardis-homes-for-sale': 'new-construction-sardis'}
# Searches the worksheet lists as "not on any live page" whose name is the page's own name.
NAME_MATCH = {
    'metrotown-homes-for-sale': '1450248',          # "Metrotown Homes for Sale"
    'cloverale-foreclosures-court-ordered-sales': '1450032',  # "Cloverdale Foreclosures & Court Ordered Sales"
    'langley-farms': '1450183',                     # "Langley Farms for Sale"
}

def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    copied = list(wb['Copied searches'].iter_rows(values_only=True))[1:]
    new = list(wb['New pages'].iter_rows(values_only=True))[1:]
    pages, problems = {}, []
    for r in copied:
        name, sid, _old, addr, _u, _t, _sc, code = r[:8]
        sid = str(sid)
        if f'search-{sid}.def' not in (code or '') or f'/{ACCOUNT}/' not in code:
            problems.append(('embed code does not match id/account', name, sid)); continue
        if not addr or addr.startswith('Not on'):
            continue
        for p in addr.split('|'):
            slug = re.sub(r'\.html$', '', p.strip().lstrip('/'))
            if not os.path.exists(os.path.join(ROOT, 'src/data/pages', slug + '.json')):
                problems.append(('address has no page on our site', name, slug)); continue
            if not any(b.get('t') == 'grid' for b in json.load(open(os.path.join(ROOT, 'src/data/pages', slug + '.json')))['blocks']):
                problems.append(('page has no listings placeholder, not wired', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # Searches built for pages that used an unsaved widget on the old site (one search per page).
    if 'Built for pages (57)' in wb.sheetnames:
        for r in list(wb['Built for pages (57)'].iter_rows(values_only=True))[1:]:
            name, sid, _old, addr, _u, _t, _sc, code = r[:8]
            if not name: continue
            sid = str(sid); slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/'))
            if f'search-{sid}.def' not in (code or '') or f'/{ACCOUNT}/' not in code:
                problems.append(('embed code does not match id/account', name, sid)); continue
            pj = os.path.join(ROOT, 'src/data/pages', slug + '.json')
            if not os.path.exists(pj):
                problems.append(('address has no page on our site', name, slug)); continue
            if not any(b.get('t') == 'grid' for b in json.load(open(pj))['blocks']):
                problems.append(('page has no listings placeholder, not wired', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # New-construction searches (Age 0 or less), one per city; second workbook. Sardis lands on its own new page, not the general Sardis homes page.
    if os.path.exists(NC_XLSX):
        nwb = openpyxl.load_workbook(NC_XLSX, read_only=True)
        for r in list(nwb['New construction searches'].iter_rows(values_only=True))[1:]:
            name, sid, _old, addr = r[0], r[1], r[2], r[3]
            if not name: continue
            sid = str(sid); slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/')); slug = NC_ADDR_FIX.get(slug, slug)
            lp = os.path.join(ROOT, 'src/data/local', slug + '.json')
            if not os.path.exists(lp) or not any(b.get('t') == 'grid' for b in json.load(open(lp))['blocks']):
                problems.append(('new-construction page missing or has no listings placeholder', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # Three special widgets (my listings active/sold, the open search form). Stored as the path after /l/idx2/.
    special = {}
    if 'Special embeds (3)' in wb.sheetnames:
        pat = re.compile(r'src="https://idx\.myrealpage\.com/wps/rest/' + ACCOUNT + r'/l/idx2/([A-Za-z0-9~,%._()/-]+/in\.js)"')
        for r in list(wb['Special embeds (3)'].iter_rows(values_only=True))[1:]:
            name, _sid, _old, addr, _u, _t, _sc, code = r[:8]
            if not name: continue
            slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/'))
            m = pat.search(code or '')
            if not m or not os.path.exists(os.path.join(ROOT, 'src/data/pages', slug + '.json')):
                problems.append(('special embed not usable', name, slug)); continue
            special[slug] = m.group(1)
    for slug, sid in NAME_MATCH.items():
        pages.setdefault(slug, sid)
    pending = []
    for r in new:
        slug = re.sub(r'\.html$', '', (r[3] or '').strip().lstrip('/'))
        lp = os.path.join(ROOT, 'src/data/local', slug + '.json')
        if os.path.exists(lp) and json.load(open(lp)).get('new_page') and any(b.get('t') == 'grid' for b in json.load(open(lp))['blocks']):
            pages[slug] = str(r[1])
        else:
            pending.append({'name': r[0], 'id': str(r[1]), 'address': r[3]})
    ids = collections.Counter(pages.values())
    dup = [i for i, n in ids.items() if n > 1]
    out = {'account': ACCOUNT, 'pages': dict(sorted(pages.items())), 'special': dict(sorted(special.items())), 'pending': pending}
    json.dump(out, open(OUT, 'w'), indent=1)
    print(len(pages), 'pages wired;', len(special), 'special;', len(pending), 'pending;', 'ids shared by several pages:', len(dup))
    for p in problems: print('PROBLEM', p)

if __name__ == '__main__':
    main()
