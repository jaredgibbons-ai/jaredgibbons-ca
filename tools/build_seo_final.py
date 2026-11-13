#!/usr/bin/env python3
"""Writes src/data/seo-final.json from the reviewed batch files in tools/seo_final/batch_*.json (D-144).

Each batch maps slug -> {title, h1, description, flag?}. This script re-checks every entry against the same rules the
copywriters were given (title 38-60, H1 20-60 with no pipe, description 135-158 ending in a full stop, no stale month
figures, no banned wording, no duplicate title or description anywhere on the site) and refuses to write on any failure.
[...slug].astro applies the file last, so deleting an entry falls back to the layer underneath.
Also writes docs/review/seo/seo-before-after-2026-11-05.csv (current vs new) for review.

DO NOT RE-RUN AS IS (2026-11-12): src/data/seo-final.json was edited after the last run by tools/protect_top_pages_2026_11_12.py and
tools/gsc_titles_2026_11_12.py (D-231, D-232: 32 titles written from Search Console queries). A re-run puts the older titles back.
Move those titles into a fix_*.json here first, or edit seo-final.json by hand (as D-256 did for the selling page).
"""
import csv, glob, json, os, re, sys
sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAN = ['sales ratio', 'snapstats', 'nothing listed', 'muse', 'in this pass', 'research note', 'top 1%', '#1', 'top-rated',
       'dream home', '!', '…', '...', '604.']
BANW = [r'\bbest\b', r'\bleading\b', r'\btrusted\b']
MONTH = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b'


def problems(slug, e):
    t, h, d = e.get('title', ''), e.get('h1', ''), e.get('description', '')
    p = []
    if not 38 <= len(t) <= 60: p.append(f'title {len(t)}')
    if not 20 <= len(h) <= 60: p.append(f'h1 {len(h)}')
    if '|' in h: p.append('pipe in h1')
    if not 135 <= len(d) <= 158: p.append(f'desc {len(d)}')
    if not d.endswith('.'): p.append('desc not ending in a full stop')
    low = f'{t} {h} {d}'.lower()
    p += [f'banned "{b}"' for b in BAN if b in low]
    p += [f'banned word {b}' for b in BANW if re.search(b, low)]
    if re.search(MONTH + r'.*20\d\d|20\d\d.*' + MONTH, d + ' ' + t): p.append('month/year date')
    if 'REALTOR' in t: p.append('REALTOR in title')
    return p


def main():
    final = {}
    # batch_* is the first pass; pass2_* (named specifics added to weak descriptions) is applied over it; fix_* (later hand corrections) are applied last
    for f in sorted(glob.glob(f'{ROOT}/tools/seo_final/batch_*.json')) + sorted(glob.glob(f'{ROOT}/tools/seo_final/pass2_*.json')) + sorted(glob.glob(f'{ROOT}/tools/seo_final/fix_*.json')):
        final.update(json.load(open(f)))
    bad = {s: problems(s, e) for s, e in final.items() if problems(s, e)}
    seen_t, seen_d = {}, {}
    for s, e in final.items():
        for seen, key in ((seen_t, 'title'), (seen_d, 'description')):
            k = e[key].strip().lower()
            if k in seen: bad.setdefault(s, []).append(f'duplicate {key} with {seen[k]}')
            seen[k] = s
    if bad:
        for s, p in sorted(bad.items()): print(s, '; '.join(p))
        print(f'{len(bad)} entries failed; nothing written'); sys.exit(1)
    out = {s: {k: final[s][k] for k in ('title', 'h1', 'description')} for s in sorted(final)}
    json.dump(out, open(f'{ROOT}/src/data/seo-final.json', 'w'), indent=1, ensure_ascii=False)
    print(f'seo-final.json: {len(out)} pages')
    cur = {}
    cf = f'{ROOT}/tools/seo_final/current.json'
    if os.path.exists(cf): cur = json.load(open(cf))
    os.makedirs(f'{ROOT}/docs/review/seo', exist_ok=True)
    with open(f'{ROOT}/docs/review/seo/seo-before-after-2026-11-05.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['Page', 'Old title', 'New title', 'Old H1', 'New H1', 'Old description', 'New description', 'Note'])
        for s in sorted(out):
            c = cur.get(s, {})
            w.writerow([f'/{s}.html', c.get('title', ''), out[s]['title'], c.get('h1', ''), out[s]['h1'],
                        c.get('description', ''), out[s]['description'], final[s].get('flag', '')])


if __name__ == '__main__':
    main()
