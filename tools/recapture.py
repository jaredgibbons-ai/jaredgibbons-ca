"""Turn a browser re-capture of live pages into archive-format records (same layout as folder 09).

Used only for URLs the archive discovered but has no page-text record for (docs/05 OI-23, OI-25).
Input files are produced in the owner's Chrome by fetching each live page's raw HTML and walking its
text nodes (the walk was validated against an archived page: every visible-text line matched except the
<title> line, which this script adds first, text nodes with embedded line breaks, which it splits, and
live IDX data that is dropped from the site anyway).

    python3 -I tools/recapture.py --text jg-recapture.json --meta jg-recapture-meta-b.json \
        --pages /home/claude/cache09/pages --seo /home/claude/cache09/seo.csv [--skip /guildford-condos-for-sale.html]

Nothing is reworded; records are marked as re-captures in their Captured line.
"""
import argparse, csv, html, json, os, re, sys


def meta(head, attr, key):
    for m in re.finditer(r'<meta\b[^>]*>', head):
        t = m.group(0)
        if re.search(r'\b%s=["\']%s["\']' % (attr, re.escape(key)), t):
            c = re.search(r'\bcontent=("([^"]*)"|\'([^\']*)\')', t)
            if c:
                return html.unescape(c.group(2) if c.group(2) is not None else c.group(3))
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--text', required=True); ap.add_argument('--meta', required=True)
    ap.add_argument('--pages', required=True); ap.add_argument('--seo', required=True)
    ap.add_argument('--skip', default='/guildford-condos-for-sale.html')
    a = ap.parse_args()
    T = json.load(open(a.text, encoding='utf-8')); M = json.load(open(a.meta, encoding='utf-8'))
    skip = {s for s in a.skip.split(',') if s}
    csv.field_size_limit(10 ** 9)
    rows = list(csv.DictReader(open(a.seo, encoding='utf-8', newline='')))
    fields = list(rows[0].keys()); have = {r['URL'] for r in rows}
    new_rows, made = [], []
    for path, c in T['pages'].items():
        if path in skip:
            continue
        mm = M['pages'][path]; head = mm['head']
        url = 'https://jaredgibbons.ca' + path
        canon = c['canon'] or url
        kind = 'listing' if '/listing.' in path else 'page'
        fn = path.lstrip('/') .replace('/listing.', '__listing.') + '.md'
        out = [f'# Page record — {url}', '',
               f'- Source sitemap/kind: {kind}', f'- Final URL: {url}', f'- HTTP status: {c["status"]}',
               f'- Captured: {T["captured"]} (browser re-capture of the live page; not part of the original 2026-10-31 archive)',
               f'- SHA-256 of source: {mm["sha"]}', f'- Title: {c["title"]}', f'- Canonical: {canon}', '',
               '## Heading outline (in page order)']
        out += ['#' * (lvl + 1) + ' ' + t for lvl, t in c['outline']]
        out += ['', '## Components in order of appearance (links, images, forms, iframes as extracted from source HTML)']
        for k, lab, tgt in c['comps']:
            out.append(f'- LINK [{lab}] -> {tgt}' if k == 'LINK' else f'- IMAGE alt="{lab}" src={tgt}')
        lines = [c['title']]
        for l in c['lines']:
            lines += [x.strip() for x in l.split('\n') if x.strip()]
        out += ['', '## Exact visible text (extracted; verify against source.bin)', ''] + lines
        open(os.path.join(a.pages, fn), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
        made.append((fn, len(lines), len(c['comps'])))
        if url not in have and 'http://jaredgibbons.ca' + path not in have:
            h1 = next((t for lvl, t in c['outline'] if lvl == 1), '')
            new_rows.append({
                'URL': url, 'Title': c['title'], 'Meta description': c['desc'], 'H1': h1,
                'H2s': ' | '.join(t for lvl, t in c['outline'] if lvl == 2), 'Canonical': canon,
                'Meta robots': meta(head, 'name', 'robots'), 'OG title': meta(head, 'property', 'og:title'),
                'OG description': meta(head, 'property', 'og:description'), 'OG image': meta(head, 'property', 'og:image'),
                'Published': meta(head, 'property', 'article:published_time'), 'Modified': meta(head, 'property', 'article:modified_time'),
                'Author': meta(head, 'name', 'author'), 'Word count': '', 'JSON-LD blocks': str(len(mm['jsonld']))})
    with open(a.seo, 'a', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); [w.writerow(r) for r in new_rows]
    for m in made: print(*m)
    print('records', len(made), 'seo rows added', len(new_rows))


if __name__ == '__main__':
    main()
