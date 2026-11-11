#!/usr/bin/env python3
"""Short source lines under tables (D-227, Nov 11, 2026).

2,594 tables carry a source line; most repeat the same definitions after the source itself ("A pending sale is firm but has not
completed…", "Median means the middle price…", "On the reports' own scale under 12% is a buyers' market…"). Those definitions were
the largest block of identical text on the data pages. Each source line now keeps its first sentence (who published the data and for which
dates) and any note about that table alone; a definition repeated under 5 or more tables moves; GenericPage already links "How these figures are defined and sourced" after any line starting "Source:". Every
definition removed is listed once on the Data and methodology page under "Notes that used to sit under each table", so nothing is lost.
Idempotent. python3 -I tools/short_table_sources_2026_11_11.py"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
NOTES = [
    'Sales come from Paragon, the MLS® system Jared’s office uses. Where a table counts pending sales, a pending sale is firm but has not completed, so its price can still change; sales that fell through are left out. Where a source line says closed sales, pending sales are not counted.',
    'Median means the middle price: half sold for more and half for less. An average is the total of sale prices divided by the number of sales, so it moves with the mix of homes that sold. A monthly median or average from fewer than 3 sales is not read as a trend.',
    'A median, row, community, building, price band or quarter is shown only where at least 5 homes sold; with fewer, one sale would be the whole figure. A dash means fewer than 5.',
    'Lists of a niche type (legal suites, penthouses, golf course homes) name a neighbourhood at 3 or more sales and show its median at 5 or more. School tables leave out schools with fewer than 10 sales nearby.',
    'Duplexes and row houses count in "All homes" only. A quarter is shown only when each of the four has 5 or more sales, and the change is not called a trend.',
    'Sold vs list is the sale price as a percentage of the last list price.',
    'A legal suite means Paragon lists the suite as Legal Suite or Licensed Suite; an unauthorized suite is one the listing marks Unauthorized Suite; houses with no suite, or with the field left blank, are in neither column.',
    'A penthouse is a condo whose Paragon style field includes Penthouse. A golf course home is a detached house whose Site Influences field lists Golf Course Nearby or Golf Course Dev.; the listing agent chooses the flag, so treat counts as a floor.',
    'Building names are as entered in the MLS® listings; a building’s price is the median of its sales, not any one home.',
    'The benchmark (MLS® Home Price Index) is the board’s modelled price for a typical home of a type and area, not an average or median of sales. The index sets January 2005 at 100. Changes are as published; the text calls a change a rise or fall only at 1.5% or more.',
    'Monthly listing and sales counts are MLS® data from the Greater Vancouver REALTORS® and the Fraser Valley Real Estate Board, compiled by SnapStats®. Sales ratio is homes sold divided by homes listed in the month; on the reports’ own scale under 12% is a buyers’ market, 12% to 20% balanced and over 20% a sellers’ market. With fewer than ten homes listed, one sale moves the ratio a long way, and ranks count only communities with at least ten listed.',
    'Shares are a community’s count divided by its city’s total for the same month and home type. The reports count condos and townhomes together in one line, and give one sale-price figure a month without saying whether it is an average or a median, so use it for direction, not as a valuation.',
    'Falling listings with steady sales mean homes are being absorbed faster; rising listings with steady sales mean more choice for buyers. A sellers’ best bet is a community where homes sell quickly against the number listed; a buyers’ best bet is the reverse.',
    'Price-range tables show the five ranges with the most listings and leave out ranges with nothing listed and nothing sold. Period totals add up the sales in every neighbourhood.',
    'Distances to schools are straight-line from the school coordinates, not walking or driving routes.',
]
SPLIT = re.compile(r'(?<=[.)])\s+(?=[A-Z])')


def first_sentence(s):
    parts = SPLIT.split(s, maxsplit=1)
    return (parts[0], parts[1]) if len(parts) == 2 else (s, '')


def tails():
    """How often each definition sentence (numbers normalised) follows a source line across the site."""
    import collections
    c = collections.Counter()
    for f in glob.glob('src/data/local/*.json'):
        if f.endswith('/data-and-methodology.json'): continue
        raw = open(f, encoding='utf-8').read()
        if '"source"' not in raw: continue
        for b in json.loads(raw).get('blocks', []) or []:
            s = b.get('source') if isinstance(b, dict) and b.get('t') == 'table' else None
            if isinstance(s, str) and s.startswith('Source:'):
                for t in SPLIT.split(first_sentence(s)[1]):
                    if t: c[re.sub(r'\d[\d,.]*', '#', t)] += 1
    return c


def main():
    notes, files, lines = {}, 0, 0
    common = tails()
    for f in sorted(glob.glob('src/data/local/*.json')):
        if f.endswith('/data-and-methodology.json'): continue
        raw = open(f, encoding='utf-8').read()
        if '"source"' not in raw: continue
        d = json.loads(raw); ch = False
        for b in d.get('blocks', []) if isinstance(d.get('blocks'), list) else []:
            s = b.get('source') if b.get('t') == 'table' else None
            if not isinstance(s, str) or not s.startswith('Source:'): continue
            head, tail = first_sentence(s)
            if not tail or len(head) < 25: continue
            keep, moved = [], []
            for t in SPLIT.split(tail):   # a definition repeated under 5+ tables moves; a note about this table stays
                (moved if common[re.sub(r'\d[\d,.]*', '#', t)] >= 5 and '(as of' not in t else keep).append(t)
            if not moved: continue
            b['source'] = ' '.join([head] + keep); ch = True; lines += 1
            for t in moved: notes.setdefault(re.sub(r'\d[\d,.]*', '#', t), t)
        if ch:
            ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
            open(f, 'w', encoding='utf-8').write((json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
            files += 1
    # the methodology page states every moved definition once (merged by hand from the list the first run printed, D-227)
    mf = 'src/data/local/data-and-methodology.json'; raw = open(mf).read(); m = json.loads(raw)
    if not any(b.get('gen') == 'tblnotes' for b in m['blocks']):
        at = next((i for i, b in enumerate(m['blocks']) if b['t'] == 'h' and b['text'] == 'Related'), len(m['blocks']))
        m['blocks'][at:at] = [{'t': 'h', 'level': 2, 'text': 'Notes that apply to every table', 'gen': 'tblnotes'},
                              {'t': 'p', 'gen': 'tblnotes', 'text': 'Each table on this site names its source in one line and links here. These are the definitions and limits behind those lines.'},
                              {'t': 'list', 'gen': 'tblnotes', 'items': [[{'t': x}] for x in NOTES]}]
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        open(mf, 'w').write((json.dumps(m, ensure_ascii=False, indent=ind) if ind else json.dumps(m, ensure_ascii=False, separators=(',', ':'))) + ('\n' if raw.endswith('\n') else ''))
    print('source lines shortened:', lines, 'in', files, 'files | distinct definitions moved:', len(notes))
    if '--list' in sys.argv:
        for v in sorted(notes.values()): print(' -', v)


if __name__ == '__main__': main()
