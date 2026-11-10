"""October 2026 board figures for the hand-written archive pages the D-192 refresh did not reach (D-200, 2026-11-10 review).

Found by searching the built pages for a benchmark tied to "September 2026" after the October packages went in:
- South Surrey & White Rock snapshot tables (Morgan Creek, Crescent Beach & Ocean Park, Grandview Heights): September figures under an
  "as of October 2026" heading on Morgan Creek. Now October: FVREB package released November 3, 2026 (docs/research/market-data).
- Maple Ridge and Pitt Meadows house/townhome pages quoted a "September 2026" GVR benchmark; the Maple Ridge figures ($746,600,
  $1,231,900) were not September's either. Now the October GVR benchmark.
- North Vancouver condos: the figure was already October's ($736,300) but still said September.
Every number below is read from src/data/market/2026-10.json, which was checked line by line against both PDFs. Idempotent.
python3 -I tools/refresh_september_leftovers.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
M = json.load(open(os.path.join(ROOT, 'src/data/market/2026-10.json'), encoding='utf-8'))
G, F, S = M['gvr']['hpi'], M['fvreb']['hpi'], M['fvreb']['summary']['White Rock / South Surrey']
money = lambda v: f'${v:,.0f}'
pct = lambda v: ('+' if v > 0 else '−' if v < 0 else '') + f'{abs(v):.1f}%'

# table cells: (old September cell values) -> October values, per row
ROWS = {}
for typ, old in (('detached', ['$1,612,500', '−2.2%', '−7.4%', '$1,628,000', '60', '600']),
                 ('townhouse', ['$797,100', '−2.8%', '−11.2%', '$800,000', '47', '283']),
                 ('apartment', ['$544,400', '−1.2%', '−7.7%', '$510,500', '43', '310'])):
    h, s = F['South Surrey & White Rock'][typ], S[typ]
    ROWS[typ] = (old, [money(h['benchmark']), pct(h['chg_1m']), pct(h['chg_1y']), money(s['median']['now']), str(s['sales']['now']), str(s['active']['now'])])

ssd, sst, ssa = (F['South Surrey & White Rock'][t] for t in ('detached', 'townhouse', 'apartment'))
mrd, mrt = G['Maple Ridge']['detached'], G['Maple Ridge']['townhouse']
pmd, pmt = G['Pitt Meadows']['detached'], G['Pitt Meadows']['townhouse']
ratio = round(100 * S['detached']['sales']['now'] / S['detached']['active']['now'])
TEXT = [
    # South Surrey & White Rock snapshot wording
    (r'South Surrey & White Rock \(Sep 2026\)', 'South Surrey & White Rock (Oct 2026)'),
    (r'South Surrey & White Rock, Sep 2026', 'South Surrey & White Rock, Oct 2026'),
    (r'^vs\. Aug 2026$', 'vs. Sep 2026'), (r'^vs\. Sep 2025$', 'vs. Oct 2025'),
    (r'figures \(released October 5, 2026\):', 'figures (released November 3, 2026):'),
    (r'figures, released October 5, 2026:', 'figures, released November 3, 2026:'),
    (r'\(MLS® Summary, White Rock / South Surrey\), released October 5, 2026\.', '(MLS® Summary, White Rock / South Surrey), released November 3, 2026.'),
    (r'^FVREB September 2026 statistics package$', 'FVREB October 2026 statistics package'),
    (r'^Market Snapshot · September 2026$', 'Market Snapshot · October 2026'),
    (r'(Crescent Beach & Ocean Park|Grandview Heights) market snapshot \(as of September 2026\)', r'\1 market snapshot (as of October 2026)'),
    (r'By my calculation from FVREB\'s figures, September detached sales were about \d+% of active detached listings',
     f"By my calculation from FVREB's figures, October detached sales were about {ratio}% of active detached listings"),
    (r'the townhouse benchmark was \$797,100 in September 2026, down 11\.2% from September 2025',
     f'the townhouse benchmark was {money(sst["benchmark"])} in October 2026, down {abs(sst["chg_1y"]):.1f}% from October 2025'),
    (r'In September 2026 the apartment benchmark there was \$544,400, 7\.7% lower than a year earlier, and the median sale price was \$510,500',
     f'In October 2026 the apartment benchmark there was {money(ssa["benchmark"])}, {abs(ssa["chg_1y"]):.1f}% lower than a year earlier, and the median sale price was {money(S["apartment"]["median"]["now"])}'),
    (r'^FVREB Statistics Package, September 2026$', 'FVREB Statistics Package, October 2026'),
    (r'The South Surrey & White Rock detached benchmark was \$1,612,500 in September 2026',
     f'The South Surrey & White Rock detached benchmark was {money(ssd["benchmark"])} in October 2026'),
    # GVR: Maple Ridge, Pitt Meadows, North Vancouver
    (r'September 2026 MLS® (Home Price Index report|HPI), the benchmark price for a strata townhome in Maple Ridge is \$746,600',
     rf'October 2026 MLS® \1, the benchmark price for a strata townhome in Maple Ridge is {money(mrt["benchmark"])}'),
    (r'September 2026 MLS® HPI, the benchmark price for a detached house in Maple Ridge is \$1,231,900',
     f'October 2026 MLS® HPI, the benchmark price for a detached house in Maple Ridge is {money(mrd["benchmark"])}'),
    (r'MLS® Home Price Index for September 2026, a single-family detached house in Maple Ridge has a benchmark price of \$1,231,900',
     f'MLS® Home Price Index for October 2026, a single-family detached house in Maple Ridge has a benchmark price of {money(mrd["benchmark"])}'),
    (r'September 2026 MLS® (Home Price Index report|HPI), the benchmark price for a single-family detached house in Pitt Meadows is \$1,178,600',
     rf'October 2026 MLS® \1, the benchmark price for a single-family detached house in Pitt Meadows is {money(pmd["benchmark"])}'),
    (r'September 2026 MLS® Home Price Index report, the Pitt Meadows benchmark price was \$1,178,600 for a single-family detached house and \$737,500 for a strata townhome',
     f'October 2026 MLS® Home Price Index report, the Pitt Meadows benchmark price was {money(pmd["benchmark"])} for a single-family detached house and {money(pmt["benchmark"])} for a strata townhome'),
    (r'September 2026 MLS® HPI, the benchmark price in Pitt Meadows is \$1,178,600 for a single-family detached house and \$737,500 for a townhome',
     f'October 2026 MLS® HPI, the benchmark price in Pitt Meadows is {money(pmd["benchmark"])} for a single-family detached house and {money(pmt["benchmark"])} for a townhome'),
    (r'September 2026 MLS® Home Price Index report, the benchmark price for a strata townhome in Pitt Meadows is \$737,500',
     f'October 2026 MLS® Home Price Index report, the benchmark price for a strata townhome in Pitt Meadows is {money(pmt["benchmark"])}'),
    (r'September 2026 MLS® HPI, the Pitt Meadows townhouse benchmark price is \$737,500',
     f'October 2026 MLS® HPI, the Pitt Meadows townhouse benchmark price is {money(pmt["benchmark"])}'),
    (r'to \$736,300 in September 2026', 'to $736,300 in October 2026'),
    (r'The apartment benchmark was \$736,300 in September 2026', 'The apartment benchmark was $736,300 in October 2026'),
]
TEXT = [(re.compile(a), b) for a, b in TEXT]
URL = ('https://fvreb.bc.ca/statistics/Package202609.pdf', 'https://www.fvreb.bc.ca/statistics/Package202609.pdf')
NEWURL = 'https://www.fvreb.bc.ca/statistics/Package202610.pdf'
stats = collections.Counter()


def fix_table(items):
    flat = [it[0].get('t') if len(it) == 1 and isinstance(it[0], dict) else None for it in items]
    for typ, (old, new) in ROWS.items():
        for i in range(len(flat)):
            if flat[i] != old[0]: continue
            j = i                                            # cells in order; a table without a median column just skips it
            for o, n in zip(old, new):
                k = next((x for x in range(j, min(len(flat), i + 8)) if flat[x] == o), None)
                if k is not None: items[k][0]['t'] = n; j = k + 1; stats['cell'] += 1
            break


def walk(o):
    if isinstance(o, dict):
        if o.get('t') == 'list' and any(len(it) == 1 and isinstance(it[0], dict) and it[0].get('t') == '$1,612,500' for it in o.get('items', [])):
            fix_table(o['items'])
        if o.get('h') in URL: o['h'] = NEWURL; stats['url'] += 1
        ps = o.get('parts')
        if isinstance(ps, list):                              # "These are its [September 2026] [figures (released …)]"
            for a, b in zip(ps, ps[1:]):
                if isinstance(a, dict) and isinstance(b, dict) and a.get('t') == 'September 2026' and str(b.get('t', '')).startswith('figures'):
                    a['t'] = 'October 2026'; stats['text'] += 1
        for k, v in list(o.items()):
            if isinstance(v, str) and k in ('t', 'text', 'a', 'q'):
                for rx, rep in TEXT:
                    v2, n = rx.subn(rep, v)
                    if n: v = v2; stats['text'] += n
                o[k] = v
            elif not isinstance(v, str): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)


changed = 0
for f in glob.glob(os.path.join(ROOT, 'src/data/*/*.json')):
    if not re.search(r'/src/data/(pages|local)/', f): continue
    raw = open(f, encoding='utf-8').read()
    if 'September 2026' not in raw and 'Sep 2026' not in raw and 'Package202609' not in raw and 'October 5, 2026' not in raw: continue
    if re.search(r'september-2026-market-update', f): continue          # the September market-update post stays September
    d = json.loads(raw); before = json.dumps(d, ensure_ascii=False); walk(d)
    if json.dumps(d, ensure_ascii=False) != before:
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        out = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(out + ('\n' if raw.endswith('\n') else '')); changed += 1
print('files changed', changed, dict(stats)); print({k: v[1] for k, v in ROWS.items()})
