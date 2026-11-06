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
    # Sub-area new-construction searches (Age 0 or less), one per board sub-area with 5 or more new listings (tab Counts, Status 'Built').
    SUB_XLSX = os.path.join(ROOT, 'docs/review/idx/new-construction-subarea-searches-2026-11-04.xlsx')
    if os.path.exists(SUB_XLSX):
        swb = openpyxl.load_workbook(SUB_XLSX, read_only=True)
        codes = {str(r[1]): (r[7] or '') for r in list(swb['Sub-area searches'].iter_rows(values_only=True))[1:] if r[0]}
        for r in list(swb['Counts'].iter_rows(values_only=True))[1:]:
            if r[3] != 'Built': continue
            name, sid, addr = r[1], str(r[4]), r[5]
            slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/'))
            code = codes.get(sid, '')
            if f'search-{sid}' not in code or ACCOUNT not in code:
                problems.append(('sub-area embed code does not match its search id/account', name, slug)); continue
            lp = os.path.join(ROOT, 'src/data/local', slug + '.json')
            if not os.path.exists(lp) or not any(b.get('t') == 'grid' for b in json.load(open(lp))['blocks']):
                problems.append(('sub-area new-construction page missing or has no listings placeholder', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # 395-page job (houses, condos and townhomes, area pages), built 2026-11-04/05 in account 67649, one search per page. Only rows whose Status starts with "Built" are wired;
    # rows marked HOLD ("Not built") stay unwired until Jared answers. Pages are the local layers (src/data/local) or the original pages.
    for fn, sheet in (('houses-searches-2026-11-04.xlsx', 'Houses searches'), ('condos-townhomes-searches-2026-11-05.xlsx', 'Condos & townhomes searches'), ('area-searches-2026-11-05.xlsx', 'Area searches')):
        fp = os.path.join(ROOT, 'docs/review/idx', fn)
        if not os.path.exists(fp): continue
        for r in list(openpyxl.load_workbook(fp, read_only=True)[sheet].iter_rows(values_only=True))[1:]:
            name, sid, _old, addr, _u, _t, _sc, code, _notes, _cnt, status = r[:11]
            if not name or not (status or '').startswith('Built'): continue
            sid = str(sid); slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/'))
            if f'search-{sid}' not in (code or '') or ACCOUNT not in (code or ''):
                problems.append(('395-job embed code does not match id/account', name, slug)); continue
            pj = [q for q in (os.path.join(ROOT, 'src/data/local', slug + '.json'), os.path.join(ROOT, 'src/data/pages', slug + '.json')) if os.path.exists(q)]
            if not pj or not any(b.get('t') == 'grid' for b in json.load(open(pj[0]))['blocks']):
                problems.append(('395-job page missing or has no listings placeholder', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # 55+ batch (53 searches, ids 1451141-1451228, account 67649), one search per page. Different column layout from the 395-job worksheets:
    # Row, Page address, Name, H1, Area used, Type, Restricted Age, Price cap, Search ID, Count, Status, Verify URL, Embed code, ...  Rows with Status "Skipped" stay unwired.
    fp55 = os.path.join(ROOT, 'docs/review/idx/55plus-searches-2026-11-05.xlsx')
    if os.path.exists(fp55):
        for r in list(openpyxl.load_workbook(fp55, read_only=True)['55+ searches'].iter_rows(values_only=True))[1:]:
            _row, addr, name, _h1, _area, _t, _age, _cap, sid, _cnt, status, _verify, code = r[:13]
            if not name or not (status or '').startswith('Built'): continue
            sid = str(sid); slug = re.sub(r'\.html$', '', (addr or '').strip().lstrip('/'))
            if f'search-{sid}' not in (code or '') or ACCOUNT not in (code or ''):
                problems.append(('55+ embed code does not match id/account', name, slug)); continue
            pj = [q for q in (os.path.join(ROOT, 'src/data/local', slug + '.json'), os.path.join(ROOT, 'src/data/pages', slug + '.json')) if os.path.exists(q)]
            if not pj or not any(b.get('t') == 'grid' for b in json.load(open(pj[0]))['blocks']):
                problems.append(('55+ page missing or has no listings placeholder', name, slug)); continue
            if slug in pages and pages[slug] != sid:
                problems.append(('page has two searches', slug, f'{pages[slug]} / {sid}')); continue
            pages[slug] = sid
    # Bedroom searches (24) and the 2026-11-06 new searches (29, coach houses, suites, penthouses): worksheets Jerry returns with the two "(Jerry fills)" columns filled.
    # Drop the returned file in docs/review/idx under the name shown; columns are read by header, rows with no search id or an embed code that does not match are skipped and reported.
    for fn in ('bedroom-searches-2026-11-04-DONE.xlsx', 'new-searches-2026-11-06-DONE.xlsx'):
        fp = os.path.join(ROOT, 'docs/review/idx', fn)
        if not os.path.exists(fp): continue
        wsx = openpyxl.load_workbook(fp, read_only=True).worksheets[0]
        rows = list(wsx.iter_rows(values_only=True)); head = [str(h or '') for h in rows[0]]
        ci = lambda key: next(i for i, h in enumerate(head) if h.startswith(key))
        c_slug, c_id, c_code = ci('Page slug'), ci('Search ID'), ci('Embed code')
        for r in rows[1:]:
            slug, sid, code = r[c_slug], str(r[c_id] or '').strip(), r[c_code] or ''
            if not slug: continue
            if not sid.isdigit(): problems.append((fn + ': no search id', slug, sid)); continue
            if f'search-{sid}' not in code or ACCOUNT not in code:
                problems.append((fn + ': embed code does not match id/account', slug, sid)); continue
            pj = [q for q in (os.path.join(ROOT, 'src/data/local', slug + '.json'), os.path.join(ROOT, 'src/data/pages', slug + '.json')) if os.path.exists(q)]
            if not pj or not any(b.get('t') == 'grid' for b in json.load(open(pj[0]))['blocks']):
                problems.append((fn + ': page missing or has no listings placeholder', slug, sid)); continue
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
