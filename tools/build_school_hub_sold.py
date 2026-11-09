"""Adds a 'What homes sold for near these schools' table to each city schools hub, built only from the sold tables already on the school pages
(Paragon closed and pending sales, Nov 1 2025 to Oct 31 2026, straight-line radius per school).  Idempotent.  python3 -I tools/build_school_hub_sold.py"""
import json, glob, os, re, collections
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
L = os.path.join(ROOT, 'src/data/local')
WIN = 'November 1, 2025 and October 31, 2026'
def val(s): return int(re.sub(r'[^\d]', '', s)) if re.search(r'\d', s or '') else None
hubs = collections.defaultdict(list)
for f in sorted(glob.glob(f'{L}/homes-near-*.json')):
    d = json.load(open(f, encoding='utf-8')); slug = os.path.basename(f)[:-5]
    crumb = next((c for c in d.get('breadcrumbs', []) if c['name'].startswith('Schools in')), None)
    t = next((b for b in d['blocks'] if b.get('t') == 'table' and re.match(r'Homes sold within .* of .*, by type', b.get('caption', ''))), None)
    if not crumb or not t: continue
    m = re.match(r'Homes sold within (\S+ km) of (.*), by type', t['caption'])
    rows = {r[0]: r[1:] for r in t['rows']}; head = t['head'][1:]
    col = lambda lab, row: (rows[row][head.index(lab)] if row in rows and lab in head else '—')
    n = val(col('All homes', 'Sales')); med = val(col('All homes', 'Median price'))
    if not n or not med: continue
    hubs[crumb['href'][1:-5]].append(dict(slug=slug, school=m.group(2), rk=m.group(1), n=n, med=med, medtxt=col('All homes', 'Median price'),
        house=col('Houses', 'Median price'), th=col('Townhomes', 'Median price')))
def money(v): return f'${v:,}'
for hub, rows in hubs.items():
    f = f'{L}/{hub}.json'; d = json.load(open(f, encoding='utf-8')); raw = open(f, encoding='utf-8').read()
    d['blocks'] = [b for b in d['blocks'] if b.get('gen') != 'schoolsold']
    if len(rows) < 3: continue
    city = re.sub(r'^Schools in ', '', next(c['name'] for c in d['breadcrumbs'] if c['name'].startswith('Schools in')) if False else d['new_page']['h1']).replace(', BC', '')
    rows.sort(key=lambda r: -r['med']); hi, lo = rows[0], rows[-1]
    intro = (f"For {len(rows)} of these schools there are enough sales to show what homes sold for nearby. Between {WIN}, the middle price of all homes sold within the radius shown "
             f"ran from {money(lo['med'])} near {lo['school']} to {money(hi['med'])} near {hi['school']}. "
             "The figures are by distance from the school, not by catchment, and a house and a townhome sell at very different prices, so compare like with like. "
             "A school's own page has the full table with condos, days to sell and the share of sales over the list price.")
    tbl = {'t': 'table', 'caption': f'Homes sold near {len(rows)} {city} schools, highest median price first', 'head': ['School', 'Radius', 'Homes sold', 'Median, all homes', 'Median, houses', 'Median, townhomes'],
           'rows': [[{'t': r['school'], 'h': f"/{r['slug']}.html"}, r['rk'], f"{r['n']:,}", r['medtxt'], r['house'], r['th']] for r in rows], 'gen': 'schoolsold',
           'source': f"Source: Paragon closed and pending sales, {WIN}, within the radius shown of each school address (straight-line distance). A pending sale is firm but not completed. A median is shown only where at least 5 homes of that type sold; schools with fewer than 10 sales are left out."}
    blocks = [{'t': 'h', 'level': 2, 'text': f'What homes sold for near {city} schools', 'gen': 'schoolsold'}, {'t': 'p', 'text': intro, 'gen': 'schoolsold'}, tbl]
    at = next((i for i, b in enumerate(d['blocks']) if b.get('gen') == 'schoollinks'), None)
    if at is None: at = next((i for i, b in enumerate(d['blocks']) if b.get('gen') == 'relatedlinks'), len(d['blocks']))
    d['blocks'][at:at] = blocks
    for kw in (dict(indent=2, ensure_ascii=False), dict(indent=1, ensure_ascii=False), dict(separators=(',', ':'), ensure_ascii=False)):
        for tail in ('\n', ''):
            if json.dumps(json.loads(raw), **kw) + tail == raw: out = json.dumps(d, **kw) + tail; break
        else: continue
        break
    else: out = json.dumps(d, indent=2, ensure_ascii=False) + '\n'
    open(f, 'w', encoding='utf-8').write(out); print(hub, len(rows), 'schools;', money(lo['med']), '-', money(hi['med']))
