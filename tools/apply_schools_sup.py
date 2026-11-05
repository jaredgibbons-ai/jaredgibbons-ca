"""Overlay the SD33-SD37 schools supplement onto the five existing 'Schools in <city>, BC' pages (Chilliwack, Abbotsford, Langley, Surrey, Delta).

Source: docs/research/schools-sd33-37-2026-11-04/  (DataBC K-12 2025/26, BC School Contacts registry, district sites; read 2026-11-04).
Adds, in place (other generated blocks on the page are left alone):
  - a 'Grades' column on the public and independent school tables (from the supplement; '—' where it has none)
  - gen 'schools-sup' blocks: district school-finder link (catchments are map-only) and the schools where district pages list French Immersion but the Ministry flag reads No
Re-runnable: it strips its own gen blocks and only adds the Grades column once.
    python3 -I tools/apply_schools_sup.py
"""
import csv, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SUP_DIR = os.path.join(ROOT, 'docs/research/schools-sd33-37-2026-11-04')
LOCAL = os.path.join(ROOT, 'src/data/local')
CITY = {'chilliwack': ('33', 'Chilliwack', 'https://www.sd33.bc.ca/find-your-school'), 'abbotsford': ('34', 'Abbotsford', 'https://www.abbyschools.ca/schools/catchments'),
        'langley': ('35', 'Langley', 'https://www.sd35.bc.ca/catchment-maps'), 'surrey': ('36', 'Surrey', 'https://www.surreyschools.ca/school-locator'),
        'delta': ('37', 'Delta', 'https://www.deltasd.bc.ca/schools/student-registration/catchment-area-maps/')}


def k(s): return re.sub(r'[^a-z0-9]', '', s.lower().replace('é', 'e'))
def oxford(x): return x[0] if len(x) == 1 else ', '.join(x[:-1]) + (',' if len(x) > 2 else '') + ' and ' + x[-1]


sup = {}
for f in ('all_public_schools.csv', 'independent_schools.csv'):
    for r in csv.DictReader(open(os.path.join(SUP_DIR, f), encoding='utf-8')):
        sup.setdefault(k(r['school_name']), []).append(r)


def look(name, dn):
    c = [r for r in sup.get(k(name), []) if r['district_number'] == dn]
    return c[0] if c else None


def main():
    for slug, (dn, disp, url) in CITY.items():
        p = os.path.join(LOCAL, f'schools-in-{slug}-bc.json')
        raw = open(p, encoding='utf-8').read()
        d = json.loads(raw)
        indent = 2
        blocks = [b for b in d['blocks'] if b.get('gen') != 'schools-sup']
        hit = tot = 0
        for b in blocks:
            if b.get('t') != 'table' or 'School' not in (b.get('head') or [''])[:1] or 'Grades' in b['head']: continue
            rows = b['rows']
            gs = [(look(r[0] if isinstance(r[0], str) else r[0]['t'], dn) or {}).get('grades') for r in rows]
            if sum(1 for g in gs if g) < max(1, len(rows) // 2): continue
            b['head'] = b['head'][:-2] + ['Grades'] + b['head'][-2:] if 'Community' in b['head'] else b['head'][:-1] + ['Grades', b['head'][-1]]
            for r, g in zip(rows, gs):
                i = len(r) - 1 if 'Community' not in b['head'] else len(r) - 2
                r.insert(i, g or '—')
            hit += sum(1 for g in gs if g); tot += len(rows)
        fi = sorted({re.sub(r'^Ecole ', 'École ', r['school_name']) for rs in sup.values() for r in rs if r['district_number'] == dn and 'District lists French Immersion' in r['notes']})
        add = [{'t': 'p', 'text': f'The {disp} school district publishes its catchments only as an interactive map, not as a list of streets. Use the district\'s own school finder to check an address:', 'gen': 'schools-sup'},
               {'t': 'p', 'text': f'{disp} school district school finder', 'h': url, 'gen': 'schools-sup'}]
        if fi:
            add.append({'t': 'p', 'text': f'The district\'s own school pages also list French Immersion at {oxford(fi[:12])}' + (f' and {len(fi) - 12} more' if len(fi) > 12 else '') +
                        ', where the Ministry file flag reads No. Confirm the program with the school before relying on either.', 'gen': 'schools-sup'})
        # place after the "Before an offer" paragraph
        at = next((i for i, b in enumerate(blocks) if b.get('t') == 'p' and b.get('text', '').startswith('Before an offer')), None)
        if at is None: raise SystemExit(f'{slug}: anchor paragraph missing')
        blocks[at + 1:at + 1] = add
        d['blocks'] = blocks
        out = json.dumps(d, indent=2, ensure_ascii=False) + ('\n' if raw.endswith('\n') else '')
        open(p, 'w', encoding='utf-8').write(out)
        print(f'{slug}: grades on {hit}/{tot} rows; district-listed FI {len(fi)}')


if __name__ == '__main__': main()
