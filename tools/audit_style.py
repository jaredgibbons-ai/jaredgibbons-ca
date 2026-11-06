#!/usr/bin/env python3
"""Style consistency audit. Serve dist on :4321 first (npx serve dist -l 4321), then:  python3 tools/audit_style.py [sample_per_kind]
Samples pages of every kind (home, designed, generic by slug family, blog, listing, hub, calculator...) and reports, per page, the computed size of the H1,
every H2 (size + whether the short bar is present), card borders, link-tile styles, and section padding, then lists pages that differ from the site standard."""
import sys, json, random, glob, os, re
from playwright.sync_api import sync_playwright
random.seed(7)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
pages = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROOT, 'dist/*.html')))
fam = lambda s: ('blog' if s.startswith('blog') else 'listing' if re.match(r'^\d', s) else 'hub' if s.endswith('neighbourhood-guides') else 'bedroom' if 'bedroom' in s else
                 'under/over' if re.search(r'-(under|over)-', s) else '55+' if '55-plus' in s else 'community' if s.endswith('-for-sale') else 'other')
by = {}
for s in pages: by.setdefault(fam(s), []).append(s)
sample = ['index', 'selling', 'buying', 'fort-langley', 'reviews', 'home-evaluation', 'contact', 'mortgage-calculator', 'fraser-valley-market-stats', 'south-surrey-townhomes-for-sale', '404']
for k, v in by.items(): sample += random.sample(v, min(n, len(v)))
JS = """() => {
  const px = (e, p) => parseFloat(getComputedStyle(e)[p]);
  const h1 = document.querySelector('main h1, h1');
  const h2 = [...document.querySelectorAll('main h2')].filter(e => e.offsetParent);
  const bar = e => { const b = getComputedStyle(e, '::before'); return b.content !== 'none' && parseFloat(b.height) >= 2; };
  return {
    h1: h1 ? Math.round(px(h1, 'fontSize')) : null,
    h2: [...new Set(h2.map(e => Math.round(px(e, 'fontSize'))))].sort((a, b) => a - b),
    h2nobar: h2.filter(e => !bar(e)).length, h2n: h2.length,
    over: document.documentElement.scrollWidth > innerWidth + 2,
    left: h1 ? Math.round(h1.getBoundingClientRect().left) : null,
    sec: [...new Set([...document.querySelectorAll('main > section')].map(e => Math.round(px(e, 'paddingTop'))))].sort((a, b) => a - b),
  };
}"""
rows = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900})
    for s in sample:
        r = pg.goto(f'http://localhost:4321/{"" if s == "index" else s}', wait_until='domcontentloaded')
        if not r or r.status != 200: rows.append((s, {'status': r.status if r else None})); continue
        pg.wait_for_timeout(300); rows.append((s, pg.evaluate(JS)))
    b.close()
print(f'{"page":58} {"h1":>3} {"h2 sizes":14} {"nobar":>5} {"left":>4}  sec padding')
bad = []
for s, d in rows:
    if 'h1' not in d: print(f'{s:58} status {d}'); continue
    flag = []
    if d['h1'] is not None and d['h1'] > 64 and s != 'index': flag.append('H1 big')
    if any(x > 40 for x in d['h2']): flag.append('H2 big')
    if d['h2nobar']: flag.append('H2 no bar')
    if d['over']: flag.append('overflow')
    if d['left'] not in (None, 120, 20, 16, 24): flag.append(f'left {d["left"]}')
    print(f'{s[:58]:58} {str(d["h1"]):>3} {str(d["h2"]):14} {d["h2nobar"]:>5} {str(d["left"]):>4}  {d["sec"]}  {" | ".join(flag)}')
    if flag: bad.append((s, flag))
print('\nOUTLIERS:', len(bad), 'of', len(rows))
for s, f in bad: print(' ', s, f)
