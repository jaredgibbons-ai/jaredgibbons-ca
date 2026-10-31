"""Import archived page records (folder 09) + seo.csv into structured page JSON.

    python3 -I tools/import_pages.py --pages /home/claude/cache09/pages \
        --seo /home/claude/cache09/seo.csv --out src/data/pages [--only slug,slug]

Rules (docs/04 D-03, A-03, D-10, D-22):
  * Wording is never edited. Lines are whitespace-trimmed only; inline links are
    re-joined into their sentence by aligning visible-text lines with the record's
    ordered LINK list.
  * Heading levels: archive '##' = H1, '###' = H2, '####' = H3 (D-03).
  * The IDX listing grid (other brokerages' MLS data) is NOT retained (A-03); a
    `grid` block marks where live listings belong.
  * MyRealPage vendor widgets (login / extend / verify) are dropped (D-10).
  * The repeated Google-review excerpt block becomes one shared `reviews` block.
Writes one JSON per page plus src/data/pages-report.json (what was dropped / unmatched).
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import records  # noqa: E402

NB = ' '
def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s.replace(NB, ' ')).strip()

NAV_END = 'Fraser Valley Market Stats'       # last line of the shared header nav
NAV_END_PREV = 'First-Time Buyer Calculator BC | PTT, GST Rebate & FHSA'
VENDOR = {'Login with:', 'Login with Facebook', 'Login with Google', 'Login with X (Twitter)',
          'Forgot password', 'Extend', 'Verify', 'Contact', 'Signup', 'Login'}
SORT = '-- Sort by: --'
FILTER_UI = {'Price:', 'Bedrooms:', 'Bathrooms:', 'Year built:', 'Sq. Feet:', 'Save search', 'Reset', 'Hide filters'}   # IDX filter bar that precedes the sort control
MLS_DISCLAIMER = 'The data relating to real estate on this website comes in part from'
CTA = 'Ready to get started?'
REVIEWS_H = 'What Buyers & Sellers Say'
FORM_LABELS = ('Your email:', 'Your name:', 'Your phone number:', 'Subject:', 'Message:')


def body_bounds(r):
    L = r.lines
    # start: first line after the nav tail
    start = None
    for i in range(1, min(len(L), 900)):
        if L[i] == NAV_END and L[i - 1] == NAV_END_PREV:
            start = i + 1
    if start is None:
        raise ValueError('nav end not found')
    end = max(i for i, l in enumerate(L) if l == CTA)
    return start, end


class Linker:
    """Sequentially assigns record LINK entries to visible-text lines."""
    def __init__(self, comps):
        self.links = [(norm(lab), tgt) for k, lab, tgt in comps if k == 'LINK']
        self.c = 0
    def take(self, line, window=60):
        n = norm(line)
        for k in range(self.c, min(self.c + window, len(self.links))):
            if self.links[k][0] == n:
                self.c = k + 1
                return self.links[k][1]
        return None
    def at(self, line, c=None, window=60):
        """Index of the link that `line` would consume from position c, else None (no state change)."""
        n = norm(line); c = self.c if c is None else c
        for k in range(c, min(c + window, len(self.links))):
            if self.links[k][0] == n:
                return k
        return None
    def skip_nav(self, nav_lines):
        for l in nav_lines:
            self.take(l)


def ends_sentence(s):
    return s.rstrip().endswith(('.', '?', '!', ':', '…', '”', '"', ';'))

OPEN_END = {'a', 'an', 'the', 'its', 'their', 'our', 'your', 'my', 'his', 'her', 'for', 'of', 'to', 'in', 'on', 'at', 'by', 'with',
            'from', 'as', 'and', 'or', 'but', 'than', 'that', 'which', 'is', 'are', 'was', 'were', 'be', 'into', 'over', 'under',
            'about', 'between', 'through', 'across', 'per', 'up', 'of'}

def starts_cont(s):
    return s[:1] in ',.;:)!?—–' or s[:1].islower()

def open_end(s):
    w = re.findall(r"[A-Za-z']+", s)
    return bool(w) and w[-1].lower() in OPEN_END and len(s) >= 12   # a sentence cut mid-clause by inline markup


def assemble(tokens):
    """tokens: [(text, href|None)] -> list of blocks p/lines (no headings)."""
    paras = []          # each: list of parts {t, h?}
    for text, href in tokens:
        part = {'t': text} if not href else {'t': text, 'h': href}
        if not paras:
            paras.append([part]); continue
        prev = paras[-1][-1]
        join = False
        if href and not prev.get('h') and not ends_sentence(prev['t']):
            join = True
        elif not href and prev.get('h') and starts_cont(text):
            join = True
        elif not href and not prev.get('h') and (starts_cont(text) or open_end(prev['t'])) and not ends_sentence(prev['t']):
            join = True
        elif not href and not prev.get('h') and prev['t'].endswith(':') and len(prev['t']) <= 48 and len(paras[-1]) == 1:
            join = True            # "Label:" + sentence (was <strong>label</strong> text)
            part['lead'] = True
        elif href and prev.get('h') and prev['t'][-1:] in ',(' :
            join = True
        if join:
            paras[-1].append(part)
        else:
            paras.append([part])
    # group runs of >=3 short single-part paragraphs into a list
    out, run = [], []
    def flush():
        nonlocal run
        if len(run) >= 3:
            out.append({'t': 'list', 'items': [p for p in run]})
        else:
            out.extend({'t': 'p', 'parts': p} for p in run)
        run = []
    for p in paras:
        short = len(p) == 1 and len(p[0]['t']) <= 64 and not ends_sentence(p[0]['t'])
        if short:
            run.append(p)
        else:
            flush(); out.append({'t': 'p', 'parts': p})
    flush()
    return out


def align_links(r):
    """Map absolute visible-line index -> href by aligning the ordered line sequence with the
    ordered LINK-label sequence (difflib longest matching blocks; robust to dropped regions)."""
    import difflib
    L = [norm(x) for x in r.lines]
    links = [(norm(lab), tgt) for k, lab, tgt in r.comps if k == 'LINK' and norm(lab)]
    sm = difflib.SequenceMatcher(None, L, [a for a, _ in links], autojunk=False)
    m, used_link = {}, set()
    for a, b, size in sm.get_matching_blocks():
        for t in range(size):
            m[a + t] = links[b + t][1]; used_link.add(b + t)
    # second pass: links the monotonic alignment could not place because the DOM order of the links
    # differs from the visible-text order (e.g. the byline author link sits after body links). Pair
    # each leftover link with a leftover line of identical text, in order, only when every
    # leftover link of that label has a distinct line to take.
    free = {}
    for i, x in enumerate(L):
        if i not in m and x: free.setdefault(x, []).append(i)
    left = {}
    for j, (lab, tgt) in enumerate(links):
        if j not in used_link: left.setdefault(lab, []).append((j, tgt))
    for lab, items in left.items():
        idxs = free.get(lab, [])
        if idxs and len(idxs) >= len(items):
            for (j, tgt), i in zip(items, idxs):
                m[i] = tgt; used_link.add(j)
    # anchors that wrap several text lines (title + description): label == join of 2..6 free lines
    spans, ptr = {}, 0
    for j, (lab, tgt) in enumerate(links):
        if j in used_link or len(lab) < 12: continue
        for sidx in range(ptr, len(L)):
            if sidx in m or L[sidx] == '' or not lab.startswith(L[sidx]): continue
            acc, e = L[sidx], sidx
            while e + 1 < len(L) and len(acc) < len(lab) and (e + 1) not in m and e - sidx < 6:
                e += 1; acc = acc + ' ' + L[e]
            if acc == lab and e > sidx:
                spans[sidx] = (tgt, e - sidx + 1); ptr = e + 1; break
    return m, len(links), spans


def slugify(url):
    m = re.match(r'https://jaredgibbons\.ca/([^/?#]+)\.html$', url)
    return m.group(1) if m else None


def post_slug(url):
    m = re.match(r'https://jaredgibbons\.ca/blog\.html/([^/?#]+)$', url)
    return m.group(1) if m else None


def import_record(r, seo_row, reviews_ref):
    start, end = body_bounds(r)
    L = r.lines
    hmap, n_links, spans = align_links(r)
    body = L[start:end]
    # texts that sit inside IDX grid regions can never be body headings
    grid_texts, bi = set(), 0
    while bi < len(body):
        if body[bi] == SORT:
            bj = bi
            while bj < len(body) and not body[bj].startswith(MLS_DISCLAIMER): bj += 1
            grid_texts.update(norm(x) for x in body[bi:bj]); bi = bj
        bi += 1
    outside = {norm(x) for x in body} - grid_texts
    outside_l = {x.lower() for x in outside}
    bl = [b for b in body if norm(b).lower() in outside_l or True]
    for sp in (2, 3):
        for q in range(len(body) - sp + 1):
            outside_l.add(norm(' '.join(body[q:q + sp])).lower())
    H = [(lv, t) for lv, t in r.outline if norm(t).lower() in outside_l]
    remaining = {}
    for lv, t in H:
        remaining.setdefault(norm(t).lower(), []).append(lv)
    # Outline order can differ from visible-text order; visible-text order is the reading order.
    order_mismatch = False
    blocks, tokens = [], []
    dropped = Counter()
    unmatched_h = []

    def flush_tokens():
        nonlocal tokens
        if tokens:
            blocks.extend(assemble(tokens))
            tokens = []

    i = 0
    n = len(body)
    while i < n:
        line = body[i]
        # --- vendor widget cluster (D-10)
        if line in VENDOR:
            j = i
            while j < n and body[j] in VENDOR: j += 1
            dropped['vendor'] += j - i; i = j; continue
        # --- IDX search bar: selected-area chips, Price:, type options, filters, login widget ... up to the sort control
        if line == 'Price:' and SORT in body[i + 1:i + 80]:
            j = body.index(SORT, i)
            if tokens and tokens[-1][1] is None and len(tokens[-1][0]) <= 60 and not ends_sentence(tokens[-1][0]):
                tokens.pop(); dropped['idx_grid_lines'] += 1          # the selected-area line right before it
            dropped['idx_grid_lines'] += j - i; i = j; continue
        # --- IDX filter bar immediately before the sort control (vendor widget, part of the grid)
        if line in FILTER_UI:
            j = i
            while j < n and body[j] in FILTER_UI: j += 1
            if j < n and body[j] == SORT:
                dropped['idx_grid_lines'] += j - i; i = j; continue
        # --- IDX grid region: sort control .. MLS disclaimer (A-03: not retained)
        if line == SORT:
            flush_tokens()
            j = i
            while j < n and not body[j].startswith(MLS_DISCLAIMER): j += 1
            dropped['idx_grid_lines'] += j - i
            blocks.append({'t': 'grid'})
            i = j + 1 if j < n else j        # disclaimer is rendered by the shared footer
            continue
        if line.startswith(MLS_DISCLAIMER):
            dropped['mls_disclaimer'] += 1; i += 1; continue
        # --- shared Google-review excerpt block
        if line == REVIEWS_H:
            flush_tokens()
            j = i + 1
            while j < n and (body[j].startswith('Excerpts from Google reviews') or body[j] == '★★★★★'
                             or body[j].startswith('“') or re.fullmatch(r'[A-Z]\.?([A-Z]\.)*', body[j]) or body[j].endswith('Google review')):
                j += 1
            seg = body[i + 1:j]
            intro = seg[0] if seg and seg[0].startswith('Excerpts from Google reviews') else ''
            rest = seg[1:] if intro else seg
            items = []
            for q in range(0, len(rest) - 3, 4):
                st, quote, who, when = rest[q:q + 4]
                items.append({'stars': st.count('★'), 'quote': quote, 'who': who, 'when': when})
            if len(rest) % 4: dropped['reviews_unparsed'] += len(rest) % 4
            blocks.append({'t': 'reviews', 'heading': REVIEWS_H, 'intro': intro, 'items': items})
            reviews_ref.append(tuple(body[i:j]))
            if remaining.get(REVIEWS_H.lower()): remaining[REVIEWS_H.lower()].pop(0)
            i = j; continue
        # --- multi-line anchor (card link)
        if (start + i) in spans:
            tgt, ln = spans[start + i]
            flush_tokens()
            items = []
            for q in range(ln):
                kq = norm(body[i + q]).lower()
                lv = remaining[kq].pop(0) if remaining.get(kq) else None
                items.append({'text': body[i + q], **({'level': lv} if lv else {})})
            blocks.append({'t': 'card', 'href': tgt, 'lines': items})
            i += ln; continue
        # --- heading (ordered match against the outline)
        hit = None
        key = norm(line).lower()
        if remaining.get(key):
            hit = remaining[key][0]
            # a jump-nav / list link that shares its text with a heading stays a link
            if (start + i) in hmap:
                nxt_link = (start + i + 1) in hmap
                prv_link = bool(tokens) and tokens[-1][1] is not None
                nxt_len = len(body[i + 1]) if i + 1 < n else 0
                if (nxt_link or (prv_link and nxt_len <= 80)) and not (i + 1 < n and body[i + 1] == 'by'):
                    hit = None   # (a post-list title followed by its byline stays a heading)
        span = 1
        if hit is None:
            for sp in (2, 3):
                if i + sp <= n and (start + i) not in hmap or (i + sp <= n and sp == 2 and (start + i) in hmap and (start + i + 1) not in hmap):
                    cand = norm(' '.join(body[i:i + sp])).lower()
                    if remaining.get(cand):
                        key, hit, span = cand, remaining[cand][0], sp; break
        if hit is not None:
            flush_tokens()
            remaining[key].pop(0)
            hb = {'t': 'h', 'level': hit, 'text': norm(' '.join(body[i:i + span]))}
            if hmap.get(start + i): hb['href'] = hmap[start + i]   # heading that is itself a link (first line's anchor)
            blocks.append(hb)
            i += span; continue
        # --- post byline: "Posted on" <date> "by" <author>
        if line == 'Posted on' and i + 3 < n and body[i + 2] == 'by':
            flush_tokens()
            parts = [{'t': 'Posted on'}, {'t': body[i + 1]}, {'t': 'by'}]
            au = {'t': body[i + 3]}
            if hmap.get(start + i + 3): au['h'] = hmap[start + i + 3]
            parts.append(au)
            blocks.append({'t': 'p', 'parts': parts, 'cls': 'byline'})
            i += 4; continue
        # --- property-check form (recurs on guide pages): address + optional name + submit label
        if line == 'Property address' and i + 2 < n and body[i + 1] == 'Your name (optional)':
            flush_tokens()
            blocks.append({'t': 'form', 'labels': [body[i], body[i + 1]], 'submit': body[i + 2]})
            i += 3; continue
        # --- form labels
        if line == FORM_LABELS[0]:
            j = i
            labels = []
            while j < n and body[j] in FORM_LABELS:
                labels.append(body[j]); j += 1
            submit = body[j] if j < n else ''
            flush_tokens()
            blocks.append({'t': 'form', 'labels': labels, 'submit': submit})
            i = j + 1; continue
        # --- ordinary text / link line
        href = hmap.get(start + i)
        tokens.append((line, href))
        i += 1
    flush_tokens()

    slug = (post_slug(r.canonical or r.url) or slugify(r.canonical or r.url)) if r.kind == 'blog' else slugify(r.canonical or r.url)
    # --- same-page fragment targets: attach ids to headings only where the label clearly matches
    base = (r.canonical or r.url).split('#')[0]
    frag = [(norm(lab), tgt.split('#', 1)[1]) for k, lab, tgt in r.comps
            if k == 'LINK' and tgt.startswith(base + '#') and norm(lab)]
    unmapped_ids, seen_ids = [], set()
    for lab, fid in frag:
        if fid in seen_ids: continue
        seen_ids.add(fid)
        ll = lab.lower()
        cand = [b for b in blocks if b['t'] == 'h' and b['level'] >= 2 and 'id' not in b and
                (ll in b['text'].lower() or (len(b['text']) > 3 and b['text'].lower() in ll))]
        if not cand:
            kind_re = (r'questions|faq' if 'faq' in fid.lower() else r'related|nearby' if 'related' in fid.lower()
                       else r'reviews|say' if fid.lower().endswith('reviews') else None)
            if kind_re:
                cand = [b for b in blocks if b['t'] == 'h' and b['level'] >= 2 and 'id' not in b and re.search(kind_re, b['text'], re.I)]
        if cand and len(ll) > 2:
            cand[0]['id'] = fid
        else:
            unmapped_ids.append(fid)
    out = {
        'slug': slug, 'path': (f'/blog.html/{slug}' if (r.kind == 'blog' and post_slug(r.canonical or r.url)) else f'/{slug}.html'), 'url': r.url, 'kind': r.kind,
        'title': r.title, 'canonical': r.canonical,
        'seo': seo_row,
        'blocks': blocks,
        'forms': [b for k, a, b in r.comps if k == 'FORM' and not b.endswith('fields=3')],
        'iframes': [b for k, a, b in r.comps if k == 'IFRAME'],
    }
    stats = {'slug': slug, 'anchors_unmapped': unmapped_ids, 'anchors_total': len(seen_ids), 'dropped': dict(dropped), 'headings_in_outline': len(H), 'headings_matched': sum(1 for b in blocks if b['t'] == 'h'), 'headings_left': sum(len(v) for v in remaining.values()),
             'blocks': len(blocks), 'links_assigned': sum(1 for k in hmap if start <= k < end), 'links_total': n_links}
    return out, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', required=True); ap.add_argument('--seo', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--only', default=''); ap.add_argument('--skip', default='fort-langley,reviews'); ap.add_argument('--kind', default='page', choices=['page', 'blog'])
    a = ap.parse_args()
    csv.field_size_limit(10**9)
    seo = {}
    for row in csv.DictReader(open(a.seo, encoding='utf-8', newline='')):
        seo.setdefault(row['URL'], row)
    only = {s for s in a.only.split(',') if s}; skip = {s for s in a.skip.split(',') if s}
    os.makedirs(a.out, exist_ok=True)
    reviews_ref, report, written = [], [], 0
    for f in sorted(os.listdir(a.pages)):
        if not f.endswith('.md') or f.startswith('home.md'):
            continue
        if a.kind == 'page' and ('__' in f or f.startswith('blog.html__')):
            continue
        if a.kind == 'blog' and not f.startswith('blog.html__'):
            continue
        r = records.parse(os.path.join(a.pages, f))
        if r.kind != a.kind and not (a.kind == 'page' and f == 'blog.html.md'):   # blog index is a page route
            continue
        slug = post_slug(r.canonical or r.url) if a.kind == 'blog' else slugify(r.canonical or r.url)
        if not slug or slug in skip or slug == 'index' or (only and slug not in only):
            continue
        row = seo.get(r.canonical) or seo.get(r.url)
        srow = None
        if row:
            srow = {k: row[k] for k in ('Title', 'Meta description', 'H1', 'Canonical', 'Meta robots', 'OG title', 'OG description', 'OG image', 'Published', 'Modified')}
        try:
            out, st = import_record(r, srow, reviews_ref)
        except Exception as e:                    # noqa: BLE001
            report.append({'slug': slug, 'error': repr(e)}); continue
        if not srow:
            st['no_seo_row'] = True
        report.append(st)
        json.dump(out, open(os.path.join(a.out, slug + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        written += 1
    uniq = Counter(reviews_ref)
    json.dump({'written': written, 'reviews_variants': len(uniq), 'pages': report}, open(os.path.join(os.path.dirname(a.out.rstrip('/')), 'pages-report.json' if a.kind == 'page' else 'posts-report.json'), 'w'), indent=1, ensure_ascii=False)
    print('written', written, 'errors', sum(1 for x in report if 'error' in x), 'review variants', len(uniq))


if __name__ == '__main__':
    main()
