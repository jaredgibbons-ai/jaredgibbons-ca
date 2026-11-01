#!/usr/bin/env python3
"""Parse SnapStats(R) monthly PDF reports into structured JSON.

Usage:
  python3 -I tools/parse_snapstats.py <dir-with-pdfs> [--out src/data/snapstats]

Reads files named GVR-YYYY-MM.pdf / FVR-YYYY-MM.pdf (Greater Vancouver and Fraser
Valley reports, one page per city x property type from page 2) and writes one JSON
per month: src/data/snapstats/YYYY-MM.json.

The PDFs themselves are NOT stored in the repo (licensed material). The JSON keeps
only the figures. Publication of figures on the public site is gated on Jared
confirming his SnapStats licence allows it (see docs/04-decisions-and-exceptions.md).
"""
import json, re, sys, os, glob
import pdfplumber

# page order is fixed in each report (page 1 = cover). Verified against page text.
PAGES = {
    'GVR': [
        ('burnaby', 'Burnaby', 'BURNABY'), ('new-westminster', 'New Westminster', 'NEW WESTMINSTER'),
        ('coquitlam', 'Coquitlam', 'COQUITLAM'), ('port-coquitlam', 'Port Coquitlam', 'PORT COQUITLAM'),
        ('port-moody', 'Port Moody', 'PORT MOODY'), ('pitt-meadows', 'Pitt Meadows', 'PITT MEADOWS'),
        ('maple-ridge', 'Maple Ridge', 'MAPLE RIDGE'),
    ],
    'FVR': [
        ('surrey', 'Surrey', 'SURREY'), ('south-surrey-white-rock', 'South Surrey / White Rock', 'WHITE ROCK'),
        ('north-delta', 'North Delta', 'NORTH DELTA'), ('cloverdale', 'Cloverdale', 'CLOVERDALE'),
        ('langley', 'Langley', 'LANGLEY'), ('abbotsford', 'Abbotsford', 'ABBOTSFORD'),
        ('mission', 'Mission', 'MISSION'),
    ],
}
TYPES = ['detached', 'condo_townhome']
TYPE_WORD = {'detached': 'DETACHED HOUSES', 'condo_townhome': 'CONDOS & TOWNHOMES'}
MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
ROW = re.compile(r'^(?P<label>.+?)\s+(?P<inv>[\d,]+)\s+(?P<sales>[\d,]+)\s+(?P<ratio>(?:\d+%|NA)\*?)$')
SUMROW = re.compile(r'^(?P<label>Inventory|Solds|Sale Price SQFT|Sale Price|Sale to List Price Ratio|Days on Market)\s+(?P<a>\S+)\s+(?P<b>\S+)\s+(?P<v>-?\S+%)$')


def num(s):
    if s is None:
        return None
    s = s.replace('$', '').replace(',', '').replace('*', '').strip()
    if s in ('NA', ''):
        return None
    if s.endswith('%'):
        return int(s[:-1])
    return int(s)


def lines(words, tol=2.5):
    rows = []
    for w in sorted(words, key=lambda w: (round(w['top']), w['x0'])):
        if rows and abs(rows[-1][0] - w['top']) <= tol:
            rows[-1][1].append(w)
        else:
            rows.append([w['top'], [w]])
    return [(t, ' '.join(x['text'] for x in sorted(ws, key=lambda x: x['x0']))) for t, ws in rows]


def parse_page(pg):
    words = pg.extract_words(extra_attrs=['non_stroking_color'])
    out = {'price_bands': [], 'bedrooms': [], 'communities': [], 'summary': {}, 'market_summary': [], 'trend': {}}
    # left column (x<300), body
    left = [w for w in words if w['x1'] < 300 and 90 < w['top'] < 520]
    totals = 0
    for _, ln in lines(left):
        m = SUMROW.match(ln)
        if m:
            out['summary'][m['label']] = {'prev': num(m['a']), 'cur': num(m['b']), 'variance_pct': num(m['v'])}
            continue
        m = ROW.match(ln)
        if m:
            rec = {'label': m['label'], 'inventory': num(m['inv']), 'sales': num(m['sales']), 'ratio': num(m['ratio'])}
            if m['label'].startswith('TOTAL'):
                totals += 1
                if totals == 1:
                    out['total'] = rec
                continue
            (out['bedrooms'] if 'edroom' in m['label'] else out['price_bands']).append(rec)
            continue
    # communities (x>=300)
    right = [w for w in words if w['x0'] >= 300 and 90 < w['top'] < 520]
    for _, ln in lines(right):
        m = ROW.match(ln)
        if not m or m['label'].startswith(('TOTAL', 'SnapStats')):
            continue
        out['communities'].append({'name': m['label'], 'inventory': num(m['inv']), 'sales': num(m['sales']), 'ratio': num(m['ratio'])})
    # market summary bullets
    txt = pg.crop((0, 395, 612, 560)).extract_text() or ''
    for ln in txt.split('\n'):
        if ln.strip().startswith('•') or 'Market Type Indicator' in ln:
            out['market_summary'].append(ln.split('•', 1)[-1].strip() if '•' in ln else ln.strip())
    # trend
    tw = [w for w in words if w['top'] > 540 and w['top'] < 690]
    labels = [w for w in tw if w['text'] in MONTHS]
    labels = sorted(labels, key=lambda w: w['x0'])
    if len(labels) == 13:
        xs = [(w['x0'] + w['x1']) / 2 for w in labels]
        ser = {'price': [None] * 13, 'inventory': [None] * 13, 'solds': [None] * 13}
        for w in tw:
            if w['text'] in MONTHS or not re.fullmatch(r'\$?[\d,]+', w['text']):
                continue
            c = (w['x0'] + w['x1']) / 2
            i = min(range(13), key=lambda k: abs(xs[k] - c))
            if abs(xs[i] - c) > 22:
                continue
            col = w['non_stroking_color']
            if w['text'].startswith('$'):
                key = 'price'
            elif col and len(col) == 3 and col[0] > 0.5 and col[2] < 0.2:
                key = 'inventory'
            elif col and len(col) == 3 and col[2] > 0.5:
                key = 'solds'
            else:
                continue
            ser[key][i] = num(w['text'])
        out['trend'] = {'months': [w['text'] for w in labels], **ser}
    return out


def main():
    src = sys.argv[1]
    outdir = 'src/data/snapstats'
    if '--out' in sys.argv:
        outdir = sys.argv[sys.argv.index('--out') + 1]
    os.makedirs(outdir, exist_ok=True)
    by_month = {}
    for f in sorted(glob.glob(os.path.join(src, '*.pdf'))):
        m = re.match(r'(GVR|FVR)-(\d{4})-(\d{2})\.pdf$', os.path.basename(f))
        if not m:
            continue
        board, yy, mm = m.groups()
        pdf = pdfplumber.open(f)
        month = f'{yy}-{mm}'
        d = by_month.setdefault(month, {'month': month, 'source': 'SnapStats(R) Publishing Co. monthly reports; MLS(R) data from Greater Vancouver REALTORS(R) and Fraser Valley Real Estate Board', 'areas': {}})
        idx = 1
        for key, name, kw in PAGES[board]:
            area = d['areas'].setdefault(key, {'name': name, 'board': board})
            for t in TYPES:
                pg = pdf.pages[idx]
                idx += 1
                text = pg.extract_text() or ''
                if TYPE_WORD[t] not in text or kw not in text.replace('S SURREY', 'SURREY') and kw not in text:
                    print(f'WARN {f} page {idx}: expected {kw} / {t}', file=sys.stderr)
                area[t] = parse_page(pg)
    for month, d in by_month.items():
        with open(os.path.join(outdir, f'{month}.json'), 'w') as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
        n = sum(len(a[t]['communities']) for a in d['areas'].values() for t in TYPES)
        print(month, 'areas', len(d['areas']), 'community rows', n)


if __name__ == '__main__':
    main()
