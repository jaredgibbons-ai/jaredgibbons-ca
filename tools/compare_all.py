"""Archive-vs-render comparison for every generated page (no browser needed).

    python3 -I tools/compare_all.py --pages /home/claude/cache09/pages --dist dist [--out docs/test-results/compare-all.json]

Per page: title, canonical, meta description (vs seo.csv), heading texts, link destinations,
and line-level visible-text coverage against the archived record. Deviations are classified:
  idx-grid  lines inside the MLS listing grid (other brokerages' data; not retained, A-03)
  vendor    MyRealPage login/extend/verify widget (D-10)
  missing   anything else -> a real defect to fix
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys
from html.parser import HTMLParser
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import records, import_pages as ip  # noqa: E402

norm = ip.norm
alnum = lambda s: re.sub(r'[^a-z0-9$%]', '', s.lower())


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.hrefs, self.heads, self.skip, self._h = [], [], [], 0, None
        self.title = ''; self.canon = ''; self.meta = {}; self._in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('script', 'style'): self.skip += 1
        if tag == 'title': self._in_title = True
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag == 'link' and a.get('rel') == 'canonical': self.canon = a.get('href', '')
        if tag == 'meta':
            k = a.get('name') or a.get('property')
            if k: self.meta[k] = a.get('content', '')
        if re.fullmatch(r'h[1-6]', tag): self._h = [int(tag[1]), '']
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip -= 1
        if tag == 'title': self._in_title = False
        if self._h and tag == f'h{self._h[0]}': self.heads.append((self._h[0], norm(self._h[1]))); self._h = None
    def handle_data(self, d):
        if self._in_title: self.title += d
        if self.skip: return
        self.text.append(d)
        if self._h: self._h[1] += d


def grid_lines(body):
    out, i = set(), 0
    while i < len(body):
        if body[i] == ip.SORT:
            j = i
            while j < len(body) and not body[j].startswith(ip.MLS_DISCLAIMER): j += 1
            out.update(norm(x) for x in body[i:j]); i = j
        i += 1
    return out


def local(u):
    u = re.sub(r'^https://jaredgibbons\.ca(?=/|$)', '', u)
    return u or '/'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', required=True); ap.add_argument('--dist', required=True)
    ap.add_argument('--out', default='docs/test-results/compare-all.json'); ap.add_argument('--only', default='')
    ap.add_argument('--data', default='src/data/pages')
    a = ap.parse_args()
    only = {s for s in a.only.split(',') if s}
    results, tot = [], Counter()
    for f in sorted(os.listdir(a.data)):
        slug = f[:-5]
        if only and slug not in only: continue
        page = json.load(open(os.path.join(a.data, f), encoding='utf-8'))
        r = records.parse(os.path.join(a.pages, slug + '.html.md'))
        sc = Scan(); sc.feed(open(os.path.join(a.dist, slug + '.html'), encoding='utf-8').read())
        text = norm(' '.join(sc.text)); hay = text.lower(); hay_a = alnum(text)
        start, end = ip.body_bounds(r)
        body = r.lines[start:end]
        G = grid_lines(body)
        missing, idx, vendor = [], 0, 0
        for l in r.lines:
            n = norm(l)
            if n.lower() in hay or (alnum(n) and alnum(n) in hay_a): continue
            if n in G: idx += 1; continue
            if n in ip.VENDOR: vendor += 1; continue
            if n.startswith(ip.MLS_DISCLAIMER) or n == '-- Sort by: --': continue
            if n == 'Filters': idx += 1; continue            # IDX widget control
            missing.append(n)
        rendered_heads = {t.lower() for _, t in sc.heads}
        vis = {norm(l).lower() for l in r.lines}
        joined = set(vis)
        for sp in (2, 3):
            for q in range(len(r.lines) - sp + 1):
                joined.add(norm(' '.join(r.lines[q:q + sp])).lower())
        outline_only = [t for _, t in r.outline if norm(t).lower() not in joined]          # hidden / not in visible text
        heads_missing = [t for _, t in r.outline if norm(t).lower() in joined and norm(t) not in G
                         and norm(t).lower() not in rendered_heads and 'MLS R' not in t]
        rend_links = {local(h) for h in sc.hrefs}
        want = set()
        for k, lab, tgt in r.comps:
            if k != 'LINK' or not tgt: continue
            if norm(lab) in G: continue
            if tgt.startswith(('javascript:', 'data:')) or 'myrealpage.com/wps' in tgt or 'iss-cdn' in tgt or '/wps/rest' in tgt: continue
            if '/listing.' in tgt: continue                       # IDX / listing-detail card links (A-03, own listings later)
            if tgt.endswith(('/recip.html?showlogin', '/recip.html?showsignup')): continue   # D-10
            want.add(local(tgt))
        links_missing = sorted(u for u in want if u not in rend_links and u.replace('tel:6049281361', 'tel:604-928-1361') not in rend_links)
        seo = page.get('seo') or {}
        res = dict(slug=slug,
                   title_ok=(norm(sc.title) == norm(r.title)), canonical_ok=(sc.canon == r.canonical),
                   desc_ok=(sc.meta.get('description', '') == (seo.get('Meta description', '') or '')),
                   lines=len(r.lines), lines_missing=len(missing), lines_idx=idx, lines_vendor=vendor,
                   headings=len(r.outline), headings_missing=len(heads_missing), headings_outline_only=len(outline_only),
                   links=len(want), links_missing=len(links_missing),
                   h1_count=sum(1 for l, _ in sc.heads if l == 1),
                   missing_sample=missing[:6], heads_missing_sample=heads_missing[:4], links_missing_sample=links_missing[:4])
        results.append(res)
        for k in ('lines', 'lines_missing', 'lines_idx', 'lines_vendor', 'headings', 'headings_missing', 'headings_outline_only', 'links', 'links_missing'): tot[k] += res[k]
        for k in ('title_ok', 'canonical_ok', 'desc_ok'): tot[k + '_fail'] += (not res[k])
    summary = dict(pages=len(results), **tot,
                   pages_clean=sum(1 for x in results if not x['lines_missing'] and not x['headings_missing'] and not x['links_missing'] and x['title_ok'] and x['canonical_ok'] and x['desc_ok']))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(dict(summary=summary, pages=results), open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
