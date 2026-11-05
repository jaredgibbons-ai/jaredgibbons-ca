"""Overlay the BC schools supplements onto the 'Schools in <city>, BC' pages.

Sources (BC K-12 2025/26 DataBC file + BC School Contacts registry + district sites; read 2026-11-04 and 2026-11-05):
  docs/research/schools-sd33-37-2026-11-04/   SD33 Chilliwack, SD34 Abbotsford, SD35 Langley, SD36 Surrey, SD37 Delta
  docs/research/schools-sd38-93-2026-11-05/   SD38 Richmond, SD39 Vancouver, SD40 New Westminster, SD41 Burnaby, SD42 Maple Ridge-Pitt Meadows, SD43 Coquitlam,
                                              SD44 North Vancouver, SD45 West Vancouver, SD75 Mission, SD78 Fraser-Cascade, SD93 Conseil scolaire francophone
Adds, in place (other generated blocks on the page are left alone):
  - a 'Grades' column on the school tables (from the supplements; a dash where they have none)
  - gen 'schools-sup' blocks: the district's own catchment/school-finder link (with what the district publishes: map, PDF map or street list), the Conseil scolaire
    francophone zones link when SD93 schools are listed, schools where district pages list French Immersion but the Ministry flag reads No, and (Richmond) the
    Hugh McRoberts Secondary catchment streets as the school publishes them.
Re-runnable: it strips its own gen blocks, adds the Grades column once and fills dashes on later runs.
    python3 -I tools/apply_schools_sup.py
"""
import csv, json, os, re, unicodedata, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PACKS = [os.path.join(ROOT, 'docs/research/schools-sd33-37-2026-11-04'), os.path.join(ROOT, 'docs/research/schools-sd38-93-2026-11-05')]
LOCAL = os.path.join(ROOT, 'src/data/local')
# page slug -> (display name, district numbers whose schools can appear on it; 93 is added to every page)
PAGES = {
    'chilliwack': ('Chilliwack', ['33']), 'abbotsford': ('Abbotsford', ['34']), 'langley': ('Langley', ['35']), 'surrey': ('Surrey', ['36']), 'delta': ('Delta', ['37']),
    'south-surrey-white-rock': ('South Surrey and White Rock', ['36']),
    'richmond': ('Richmond', ['38']), 'vancouver': ('Vancouver', ['39']), 'new-westminster': ('New Westminster', ['40']), 'burnaby': ('Burnaby', ['41']),
    'maple-ridge-pitt-meadows': ('Maple Ridge and Pitt Meadows', ['42']), 'coquitlam': ('Coquitlam', ['43', '41']), 'port-coquitlam': ('Port Coquitlam', ['43']),
    'port-moody-anmore': ('Port Moody and Anmore', ['43']), 'north-vancouver': ('North Vancouver', ['44']), 'west-vancouver': ('West Vancouver', ['45']),
    'mission': ('Mission', ['75']), 'hope-agassiz-harrison': ('Hope, Agassiz and Harrison Hot Springs', ['78']),
}
NOFINDER = {'south-surrey-white-rock'}  # that page has its own catchment guide; only grades are added there


def k(s):
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s)
def oxford(x): return x[0] if len(x) == 1 else ', '.join(x[:-1]) + (',' if len(x) > 2 else '') + ' and ' + x[-1]
def rd(path): return list(csv.DictReader(open(path, encoding='utf-8')))


sup = {}; catch = {}; ctext = []
for d in PACKS:
    if not os.path.isdir(d): continue
    for f in ('all_public_schools.csv', 'independent_schools.csv'):
        for r in rd(os.path.join(d, f)): sup.setdefault(k(r['school_name']), []).append(r)
    by = collections.defaultdict(list)
    for r in rd(os.path.join(d, 'all_catchments.csv')): by[r['district_number']].append(r)
    for dn, rows in by.items():
        t = collections.Counter(r.get('catchment_type') or 'map only' for r in rows).most_common(1)[0][0]
        catch[dn] = (t, rows[0]['source_url'] or rows[0]['catchment_page_url'])
    if os.path.exists(os.path.join(d, 'catchments_text.csv')): ctext += rd(os.path.join(d, 'catchments_text.csv'))
DNAME = {r['district_number']: r['district_name'] for rs in sup.values() for r in rs}
DNAME['93'] = 'Conseil scolaire francophone'


def look(name, dns):
    c = [r for r in sup.get(k(name), []) if r['district_number'] in dns]
    return c[0] if c else None


def finder_blocks(slug, disp, dns, names_on_page, has93):
    out = []
    if slug not in NOFINDER:
        for dn in dns[:2] if slug != 'coquitlam' else dns[:1]:
            if dn not in catch: continue
            kind, url = catch[dn]
            nm = DNAME.get(dn, dn)
            what = {'map only': 'only as an interactive map', 'PDF map': 'as maps (PDF files)', 'street list': 'as a list of streets'}.get(kind, 'only as a map')
            out.append({'t': 'p', 'text': f'The {nm} school district publishes its catchments {what}' + (', not as a list of streets' if kind != 'street list' else '') + '. Use the district\'s own page to check an address:', 'gen': 'schools-sup'})
            out.append({'t': 'p', 'text': f'{nm} school district catchments and school finder', 'h': url, 'gen': 'schools-sup'})
    if has93 and '93' in catch and slug not in NOFINDER:
        out += [{'t': 'p', 'text': 'The Conseil scolaire francophone publishes its attendance zones (zones de fréquentation) on its own site:', 'gen': 'schools-sup'},
                {'t': 'p', 'text': 'Conseil scolaire francophone attendance zones', 'h': catch['93'][1], 'gen': 'schools-sup'}]
    fi = sorted({re.sub(r'^Ecole ', 'École ', r['school_name']) for rs in sup.values() for r in rs
                 if r['district_number'] in dns and 'District lists French Immersion' in r['notes'] and k(r['school_name']) in names_on_page})
    if fi and slug not in NOFINDER:
        out.append({'t': 'p', 'text': f'The district\'s own school pages also list French Immersion at {oxford(fi[:12])}' + (f' and {len(fi) - 12} more' if len(fi) > 12 else '') +
                    ', where the Ministry file flag reads No. Confirm the program with the school before relying on either.', 'gen': 'schools-sup'})
    if slug == 'richmond':
        for r in ctext:
            if r['district_number'] == '38' and r['catchment_text'].strip():
                out.append({'t': 'p', 'text': f'One Richmond school publishes its catchment as streets: {r["school_name"]}\'s page describes it as running from No. 3 Road and Francis Road east along Francis Road to Garden City Road, south to Williams Road, east to No. 4 Road, south to Steveston Highway and back west to No. 3 Road, in the version dated July 1, 1997. Confirm any address with the district locator, since catchments change.', 'gen': 'schools-sup'})
                out.append({'t': 'p', 'text': f'{r["school_name"]} catchment page', 'h': r['page_url'], 'gen': 'schools-sup'})
    return out


def main():
    for slug, (disp, dns0) in PAGES.items():
        p = os.path.join(LOCAL, f'schools-in-{slug}-bc.json')
        if not os.path.exists(p): print('missing', slug); continue
        raw = open(p, encoding='utf-8').read(); d = json.loads(raw)
        dns = dns0 + ['93']
        blocks = [b for b in d['blocks'] if b.get('gen') != 'schools-sup']
        hit = tot = 0; names = set()
        for b in blocks:
            if b.get('t') != 'table' or (b.get('head') or [''])[0] != 'School': continue
            rows = b['rows']
            for r in rows: names.add(k(r[0] if isinstance(r[0], str) else r[0]['t']))
            gs = [(look(r[0] if isinstance(r[0], str) else r[0]['t'], dns) or {}).get('grades') for r in rows]
            if 'Grades' in b['head']:
                gi = b['head'].index('Grades')
                for r, g in zip(rows, gs):
                    if g and r[gi] == '—': r[gi] = g
                hit += sum(1 for r in rows if r[gi] != '—'); tot += len(rows); continue
            if sum(1 for g in gs if g) < max(1, len(rows) // 2): continue
            has_comm = 'Community' in b['head']
            at = len(b['head']) - (2 if has_comm else 1)
            b['head'].insert(at, 'Grades')
            for r, g in zip(rows, gs): r.insert(at, g or '—')
            hit += sum(1 for g in gs if g); tot += len(rows)
        has93 = any('SD93' in str(r) or 'Conseil' in str(r) for b in blocks if b.get('t') == 'table' for r in b['rows'])
        add = finder_blocks(slug, disp, dns0, names, has93)
        if add:
            at = next((i for i, b in enumerate(blocks) if b.get('t') == 'p' and b.get('text', '').startswith('Before an offer')), None)
            if at is None: print(f'{slug}: anchor paragraph missing, finder blocks skipped'); at = None
            else: blocks[at + 1:at + 1] = add
        d['blocks'] = blocks
        open(p, 'w', encoding='utf-8').write(json.dumps(d, indent=2, ensure_ascii=False) + ('\n' if raw.endswith('\n') else ''))
        print(f'{slug}: grades on {hit}/{tot} rows; {len(add)} sup blocks')


if __name__ == '__main__': main()
