"""Import own-listing detail pages (our-listings.html__listing.*.md) into src/data/listings/<slug>.json.

    python3 -I tools/import_listings.py --pages /home/claude/cache09/pages --seo /home/claude/cache09/seo.csv --out src/data/listings

Listing records are a flat list of lines from the MyRealPage listing widget. This importer rebuilds the
structure (title, summary, label/value facts, room and bathroom tables, feature notes, agent card,
brokerage credit, MLS disclaimer) from the line pattern and keeps every non-widget line, in order.
Dropped (documented, D-30): widget chrome (share buttons, Details/Photos/Map tabs, buttons, map and
Walk Score links, "Schedule a viewing" widget, gallery captions that repeat image alt text, the feed's
"Data was last updated" stamp) and exact repeats of a block already shown (summary facts, area
statistics, agent card). Nothing is reworded.
"""
from __future__ import annotations
import argparse, csv, json, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import records, import_pages as ip  # noqa: E402

norm = ip.norm

WIDGET = {'more maps', 'Location Score', 'See more', 'Share on X', 'Share on Facebook', 'Share on Pinterest', 'Share Link',
          'Share on', 'Twitter', 'Pinterest', 'Share', 'Link', 'Details', 'Photos', 'Map', 'Videos', 'Virtual Tour',
          'Contact about details', 'Send listing', 'Mortgage calculator', 'Print listing', 'Larger map options:',
          'Larger map', 'Satellite map', 'Street View', 'Walkscore', 'MAIN PHOTO', 'Schedule / Email',
          'Apple calendar', 'Office365', 'Outlook', 'Yahoo calendar', 'Other calendars'}
WIDGET_RE = re.compile(r'^(Photos \(\d+\)|Photo \d+ of \d+|Data was last updated .*)$')
AGENT = ['JARED GIBBONS', 'Royal LePage Little Oak Realty', '604-928-1361', 'jaredgibbons@royallepage.ca']
SIZE_RE = re.compile(r"""^(\d+(\.\d+)?('(\d+(\.\d+)?"?)?|"| m)|×)$""")
SECTION_NOCOLON = {'Area Statistics'}
STOP_PREFIX = ('Listed by', ip.MLS_DISCLAIMER)


def is_label(s):
    return s.endswith(':') and len(s) <= 45 and not s.startswith('Listed by')


def img_alts(r):
    out = set()
    for k, a, b in r.comps:
        if k == 'IMAGE':
            m = re.match(r'alt="(.*?)" src=', b)
            if m: out.add(norm(m.group(1)))
    return out


def clean_lines(r, start, end):
    """Body lines minus widget chrome -> (lines, absolute indexes, photo count, dropped counter)."""
    alts = img_alts(r)
    out, idx, dropped, photos = [], [], Counter(), 0
    i = start
    while i < end:
        s = norm(r.lines[i])
        m = re.match(r'^Photos \((\d+)\)$', s)
        if m: photos = max(photos, int(m.group(1)))
        if s == 'Schedule a viewing:':                       # widget: dates, in-person/virtual toggle
            j = i
            while j < end and norm(r.lines[j]) != 'Schedule / Email': j += 1
            dropped['schedule-widget'] += j - i + 1; i = j + 1; continue
        if s in WIDGET or WIDGET_RE.match(s):
            dropped['widget'] += 1; i += 1; continue
        if s in alts and s not in AGENT:
            dropped['gallery-caption'] += 1; i += 1; continue
        out.append(r.lines[i]); idx.append(i); i += 1
    # gallery captions not present as image alt text: runs of >=3 lines "<same base> (n)" / "<same base>-n"
    CAP = re.compile(r'^(.*?)[\s-]*\(?(\d+)\)?$')
    keep, k = [True] * len(out), 0
    while k < len(out):
        m = CAP.match(norm(out[k]))
        if m and m.group(1):
            j = k
            while j < len(out):
                mj = CAP.match(norm(out[j]))
                if not (mj and mj.group(1).lower().rstrip(' -(') == m.group(1).lower().rstrip(' -(')): break
                j += 1
            if j - k >= 3:
                for q in range(k, j): keep[q] = False
                dropped['gallery-caption'] += j - k; k = j; continue
        k += 1
    # lightbox captions: everything between the sidebar agent card and the brokerage credit line
    a0 = next((q for q in range(len(out) - 3) if [norm(x) for x in out[q:q + 4]] == AGENT), None)
    cr = next((q for q in range(a0 or 0, len(out)) if norm(out[q]).startswith('Listed by ')), None)
    caps = []
    if a0 is not None and cr is not None and cr > a0 + 4:
        for q in range(a0 + 4, cr):
            if keep[q]: keep[q] = False; caps.append(norm(out[q]))
        dropped['gallery-caption'] += len(caps)
    out2 = [x for x, kp in zip(out, keep) if kp]; idx2 = [x for x, kp in zip(idx, keep) if kp]
    clean_lines.captions = caps
    return out2, idx2, photos, dropped


def parse_rooms(toks):
    """Room table tokens after the header (Floor, Type, Size[, Other]) -> rows or None."""
    rows, i = [], 0
    while i < len(toks):
        if i + 1 >= len(toks): return None
        floor, typ = toks[i], toks[i + 1]; i += 2
        size = []
        while i < len(toks) and SIZE_RE.match(toks[i]):
            size.append(toks[i]); i += 1
        other = ''
        if i < len(toks) and toks[i] == '-':
            other = '-'; i += 1
        rows.append([floor, typ, ' '.join(size), other])
    return rows


def parse_baths(toks):
    rows, i = [], 0
    while i < len(toks):
        if i + 2 >= len(toks) or toks[i + 1] not in ('Yes', 'No') or not re.fullmatch(r'\d+', toks[i + 2]): return None
        rows.append([toks[i], toks[i + 1], toks[i + 2]]); i += 3
    return rows


def import_record(r, srow):
    start, end = ip.body_bounds(r)
    hmap, _, _ = ip.align_links(r)
    lines, idx, photos, dropped = clean_lines(r, start, end)
    h1 = next((t for lv, t in r.outline if lv == 1), '')
    blocks = []
    n = len(lines)
    L = [norm(x) for x in lines]
    # --- title: the smallest run of lines that joins to the outline H1
    i = 0
    for k in range(1, 7):
        if norm(' '.join(L[:k])) == norm(h1): i = k; break
    if i == 0: i = 1
    blocks.append({'t': 'h', 'level': 1, 'text': norm(h1) if h1 else L[0]})
    # --- summary (price, type, beds/baths/size/built) up to the first label
    summ = []
    while i < n and L[i] != 'Status:' and len(summ) < 24:
        summ.append(L[i]); i += 1
    h2 = next((t for lv, t in r.outline if lv == 2 and norm(t).startswith('$')), None)
    if summ:
        m = next((q for q in range(len(summ), 0, -1) if h2 and norm(' '.join(summ[:q])).lower() == norm(h2).lower()), 0)
        blocks.append({'t': 'summary', 'lines': summ, 'heading_n': m})
    seen = set()

    first_facts = []

    def add(b):
        if b['t'] == 'facts':
            if not first_facts: first_facts.extend(b['items'])
            elif len(b['items']) >= len(first_facts) and b['items'][-len(first_facts):] == first_facts:
                b = {**b, 'items': b['items'][:-len(first_facts)]}        # the widget's repeated summary facts
                dropped['repeat-block'] += 1
                if not b['items']: return
        key = json.dumps(b, sort_keys=True, ensure_ascii=False)
        if b['t'] in ('facts', 'agent', 'p', 'table', 'list') and key in seen:
            dropped['repeat-block'] += 1; return
        seen.add(key); blocks.append(b)

    tokens = []                      # pending plain text run: (line, href)

    def flush_text():
        nonlocal tokens
        if not tokens: return
        for b in ip.assemble(tokens): add(b)
        tokens = []

    def table_at(k):
        return k + 1 < n and L[k] in ('Room Information:', 'Bathrooms:') and L[k + 1] == 'Floor'

    def stop(k):
        return k >= n or table_at(k) or is_label(L[k]) or L[k] in SECTION_NOCOLON or L[k].startswith(STOP_PREFIX) or L[k:k + 4] == AGENT

    while i < n:
        s = L[i]
        if L[i:i + 4] == AGENT:
            flush_text(); add({'t': 'agent', 'lines': AGENT}); i += 4; continue
        if s.startswith('Listed by '):
            flush_text(); add({'t': 'credit', 'text': s}); i += 1; continue
        if s.startswith(ip.MLS_DISCLAIMER):
            flush_text(); add({'t': 'disclaimer', 'text': s}); i += 1; continue
        if s in ('Room Information:', 'Bathrooms:') and i + 1 < n and L[i + 1] == 'Floor':
            j = i + 2
            head = ['Floor']
            while j < n and L[j] in ('Type', 'Size', 'Other', 'Ensuite', 'Pieces'):
                head.append(L[j]); j += 1
            k = j
            while not stop(k): k += 1
            toks = L[j:k]
            rows = parse_rooms(toks) if s == 'Room Information:' else parse_baths(toks)
            flush_text()
            if rows is not None:
                if s == 'Room Information:' and 'Other' not in head: head.append('Other')
                add({'t': 'table', 'caption': s.rstrip(':'), 'head': head, 'rows': rows})
            else:                                          # keep the text if the table shape is unexpected
                add({'t': 'h', 'level': 3, 'text': s.rstrip(':')})
                for x in ['Floor'] + head[1:] + toks: add({'t': 'p', 'parts': [{'t': x}]})
                dropped['table-fallback'] += 1
            i = k; continue
        if is_label(s) or s in SECTION_NOCOLON:
            nxt = L[i + 1] if i + 1 < n else ''
            if s in SECTION_NOCOLON or not nxt or is_label(nxt) or nxt.startswith(STOP_PREFIX) or nxt in SECTION_NOCOLON:
                flush_text(); add({'t': 'h', 'level': 3, 'text': s.rstrip(':')}); i += 1; continue
            flush_text()
            items = []
            while i < n and is_label(L[i]) and not table_at(i):
                k = L[i]; i += 1
                v = []
                if not stop(i):
                    v.append(L[i]); i += 1
                    while not stop(i) and len(L[i]) <= 40 and not L[i].endswith('.'):
                        v.append(L[i]); i += 1
                items.append({'k': k, 'v': v})
                if not v and items and len(items) > 1:       # empty label after values = new section heading
                    items.pop(); i -= 1; break
            add({'t': 'facts', 'items': items})
            continue
        tokens.append((lines[i], hmap.get(idx[i])))
        i += 1
    flush_text()
    slug = r.canonical.rsplit('/', 1)[-1]
    out = {
        'slug': slug, 'path': '/our-listings.html/' + slug, 'url': r.url, 'kind': 'listing', 'title': r.title,
        'canonical': r.canonical, 'seo': srow,
        'status': next((norm(r.lines[q + 1]) for q, x in enumerate(r.lines) if x == 'Status:'), ''),
        'brokerage': next((norm(x)[len('Listed by '):] for x in r.lines if x.startswith('Listed by ')), ''),
        'photos': {'count': photos, 'alts': sorted(a for a in img_alts(r) if a.startswith('Photo ')), 'captions': clean_lines.captions},
        'blocks': blocks,
    }
    stats = {'slug': slug, 'dropped': dict(dropped), 'blocks': len(blocks), 'status': out['status']}
    return out, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', required=True); ap.add_argument('--seo', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    csv.field_size_limit(10**9)
    seo = {row['Canonical']: row for row in csv.DictReader(open(a.seo, encoding='utf-8', newline=''))}
    os.makedirs(a.out, exist_ok=True)
    report, written = [], 0
    for f in sorted(os.listdir(a.pages)):
        if not f.startswith('our-listings.html__listing.') or not f.endswith('.md'): continue
        r = records.parse(os.path.join(a.pages, f))
        row = seo.get(r.canonical) or seo.get(r.url)
        srow = {k: row[k] for k in ('Title', 'Meta description', 'H1', 'Canonical', 'Meta robots', 'OG title', 'OG description', 'OG image', 'Published', 'Modified')} if row else None
        try:
            out, st = import_record(r, srow)
        except Exception as e:                       # noqa: BLE001
            report.append({'file': f, 'error': repr(e)}); continue
        if not srow: st['no_seo_row'] = True
        report.append(st)
        json.dump(out, open(os.path.join(a.out, out['slug'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        written += 1
    json.dump({'written': written, 'pages': report}, open(os.path.join(os.path.dirname(a.out.rstrip('/')), 'listings-report.json'), 'w'), indent=1, ensure_ascii=False)
    print('written', written, 'errors', sum(1 for x in report if 'error' in x),
          'table fallbacks', sum(x.get('dropped', {}).get('table-fallback', 0) for x in report))
    for x in report:
        if 'error' in x: print(x)


if __name__ == '__main__':
    main()
