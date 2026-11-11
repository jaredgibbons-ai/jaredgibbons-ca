#!/usr/bin/env python3
"""Search titles and descriptions for blog posts and own-listing pages (D-221, Nov 11, 2026).

The Cursor audit (docs/review/cursor-audit-2026-11-11.md) found 169 post and listing pages whose title or description is cut off
("…"), too long, too short, or about a different property or story than the page. Those two page types never went through the
reviewed SEO pass (src/data/seo-final.json covers the main pages only).

This writes src/data/post-listing-seo.json: slug -> {title, description}, applied last by internal/blog/[slug].astro and
ListingPage.astro. Every value is built from the page's own H1, facts and opening sentences (nothing new is claimed), then
hand corrections in tools/seo_final/posts_fix.json win. Rules: title 30-60 characters, no ellipsis; description 120-158
characters, whole sentences, ending in a full stop. The script refuses to write if any entry breaks a rule.
python3 -I tools/build_post_listing_seo.py [--report]"""
import glob, html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
TMAX, MMIN, MMAX = 60, 120, 158
BAN = ['…', '...', 'top 1%', '#1', 'snapstats', 'muse', 'dream home']


def ptxt(b):
    out = ''
    for i, x in enumerate(b.get('parts', [])):
        t = str(x.get('t', ''))
        out += ('' if (not i or re.match(r'^[,.;:!?)\]”’]', t)) else ' ') + t
    return re.sub(r'\s+', ' ', re.sub(r'\s+([,.;:!?])', r'\1', out)).strip()


def fit_title(t):
    t = re.sub(r'\s+', ' ', html.unescape(t)).strip().replace('!', '').strip('"“” ')
    t = re.sub(r'^[^\w$#]+', '', t)
    t = re.sub(r'\s*\|\s*Jared Gibbons.*$', '', t)
    if len(t) <= TMAX: return t
    for sep in (' | ', ' – ', ' — ', ' - ', ': ', ', '):
        while len(t) > TMAX and sep in t:
            i = t.rfind(sep)
            if i < 30: break
            t = t[:i]
    return t


def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.?!])\s+(?=[A-Z0-9$“"])', text) if s.strip()]


def build_meta(paras, tail):
    best = ''
    for p in paras[:3]:
      sents = sentences(p)
      for i in range(min(1, len(sents))):
        cur = ''
        for s in sents[i:i + 4]:
            nxt = (cur + ' ' + s).strip()
            if len(nxt) > MMAX: break
            cur = nxt
            if MMIN <= len(cur) and cur[-1] in '.?!': return cur
        if not best and cur and len(cur) + 1 + len(tail) <= MMAX and len(cur) >= 40 and cur[-1] in '.?!': best = cur
      if best: break
    if best and len(best) + 1 + len(tail) >= MMIN: return best + ' ' + tail
    return ''


def problems(t, d):
    p = []
    if not 30 <= len(t) <= TMAX: p.append(f'title {len(t)}')
    if not MMIN <= len(d) <= MMAX: p.append(f'desc {len(d)}')
    if d and d[-1] not in '.?!)': p.append('desc end')
    low = (t + ' ' + d).lower()
    p += [f'banned {b}' for b in BAN if b in low]
    return p


def fit_meta_like_base(d):
    d = re.sub(r'\s+', ' ', d or '').replace('[SOLD]:', '').strip()
    if len(d) <= MMAX: return d
    cut = d[:MMAX]; end = max(cut.rfind('. '), cut.rfind('! '), cut.rfind('? '))
    if end >= 90: return cut[:end + 1]
    return d[:d[:MMAX - 1].rfind(' ')] + '…'


def main():
    fix = json.load(open('tools/seo_final/posts_fix.json', encoding='utf-8')) if os.path.exists('tools/seo_final/posts_fix.json') else {}
    out, bad, auto = {}, {}, 0
    for kind, pat in (('post', 'src/data/posts/*.json'), ('listing', 'src/data/listings/*.json')):
        for f in sorted(glob.glob(pat)):
            d = json.load(open(f, encoding='utf-8')); slug = d['slug']; seo = d.get('seo') or {}
            if not d.get('canonical'): continue
            cur_t = re.sub(r'\s+', ' ', str(d.get('title') or '')).strip()
            cur_d = fit_meta_like_base(seo.get('Meta description', ''))
            if kind == 'listing': cur_d = cur_d if len(cur_d) >= 70 else ''   # ListingPage builds its own when short
            if not problems(cur_t, cur_d or 'x' * 129 + '.') and slug not in fix: continue
            h1 = next((b.get('text', '') for b in d.get('blocks', []) if b.get('t') == 'h' and b.get('level') == 1), '')
            paras = [ptxt(b) for b in d.get('blocks', []) if b.get('t') == 'p']
            paras = [p for p in paras if len(p) > 60 and not re.match(r'(Posted on|by )', p) and not re.search(r'accurate as of|legal or tax advice|general information', p, re.I)]
            if kind == 'post':
                ok = lambda x: 30 <= len(x) <= TMAX and not any(b in x.lower() for b in BAN)
                t = next((x for x in (fit_title(cur_t), fit_title(h1)) if ok(x)), fit_title(cur_t))
                raw = re.sub(r'\s+', ' ', seo.get('Meta description', '') or '').strip()
                m = cur_d if not problems(t, cur_d) else (build_meta([raw], 'By Jared Gibbons, REALTOR®.') or build_meta(paras, 'By Jared Gibbons, REALTOR®.'))
            else:
                t = cur_t if 30 <= len(cur_t) <= TMAX and '…' not in cur_t else fit_title(cur_t)
                m = '' if problems(t, cur_d or '') and cur_d else cur_d
            e = {'title': t, 'description': m, 'kind': kind}
            e.update({k: v for k, v in fix.get(slug, {}).items()})
            if kind == 'listing' and not e.get('description'): e['description'] = ''    # '' = ListingPage builds the line from the page's facts
            auto += 1
            out[slug] = e
            pr = problems(e['title'], e.get('description') or 'x' * 129 + '.')
            if pr: bad[slug] = (pr, e, h1, cur_t, cur_d)
    if '--report' in sys.argv or bad:
        for s, (pr, e, h1, ct, cd) in bad.items():
            print(f'\n## {s}\n  problems: {pr}\n  H1: {h1}\n  current title: {ct}\n  current desc: {cd}\n  new: {e}')
        print(f'\n{len(bad)} entries need a hand correction in tools/seo_final/posts_fix.json')
        if bad: sys.exit(1)
    json.dump({k: {x: y for x, y in v.items() if x != 'kind'} for k, v in sorted(out.items())}, open('src/data/post-listing-seo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('post and listing SEO entries:', len(out))


if __name__ == '__main__': main()
