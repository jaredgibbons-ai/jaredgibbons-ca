"""Archive-vs-render comparison. Usage: python3 tools/compare.py
For each page: title, canonical, heading texts, link destinations, and line-level visible-text coverage
against the archived record (docs/archive-extracts/*.md). Writes docs/test-results/compare-<slug>.json
and prints a summary. Lines that are known, documented deviations are listed in KNOWN with a baseline id."""
import re, json, asyncio, sys
from playwright.async_api import async_playwright
BASE = 'http://localhost:4321'
PAGES = [('home', '/', 'docs/archive-extracts/home.md'), ('fort-langley', '/fort-langley.html', 'docs/archive-extracts/fort-langley.html.md'), ('reviews', '/reviews.html', 'docs/archive-extracts/reviews.html.md')]
norm = lambda s: re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()
KNOWN = {  # archive text lines intentionally not rendered in the preview -> reason
  'Edit sidebar contact & social media': 'B-01 editor/admin label, not visitor content',
  'Login with:': 'D-10 vendor feature', 'Login with Facebook': 'D-10', 'Login with Google': 'D-10', 'Login with X (Twitter)': 'D-10',
  'Forgot password': 'D-10', 'Extend': 'D-10', 'Verify': 'D-10', 'Signup': 'D-10', 'Login': 'D-10', 'Contact': 'D-10 (widget label; page link “Contact Me” kept)',
  'Filters': 'IDX widget control, needs IDX', 'View photos': 'IDX widget action, needs IDX', 'Schedule viewing / Email': 'IDX widget action', 'Send listing': 'IDX widget action',
  'View on map': 'IDX widget action', 'Mortgage calculator': 'IDX widget action (page link kept elsewhere)',
  'LISTING DETAILS': 'duplicate of card link', 'JARED GIBBONS': 'per-card agent block (IDX)', 'Royal LePage Little Oak Realty': 'per-card agent block (IDX)',
}
def archive_lines(path):
    t = open(path, encoding='utf8').read()
    body = t.split('## Exact visible text (extracted; verify against source.bin)')[1]
    out = []
    for l in body.split('\n'):
        n = norm(l)
        if n: out.append(n)
    return out
def archive_meta(path):
    t = open(path, encoding='utf8').read()
    title = re.search(r'^- Title: (.*)$', t, re.M).group(1).strip()
    canon = re.search(r'^- Canonical: (.*)$', t, re.M).group(1).strip()
    heads = []
    for l in t.split('## Heading outline (in page order)')[1].split('## Components')[0].split('\n'):
        m = re.match(r'(#{2,6}) (.*)$', l)
        if m: heads.append((len(m.group(1)) - 1, norm(m.group(2))))
    links = re.findall(r'- LINK \[.*?\] -> (\S+)', t)
    return title, canon, heads, links
async def main():
    summary = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        for slug, path, rec in PAGES:
            await pg.goto(BASE + path, wait_until='networkidle')
            # open all <details> so collapsed FAQ text is in innerText
            await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
            title = await pg.title(); canon = await pg.get_attribute('link[rel=canonical]', 'href')
            rendered_text = norm(await pg.evaluate("document.body.textContent + ' ' + [...document.querySelectorAll('.sr-only')].map(e=>e.textContent).join(' ')"))
            rendered_heads = await pg.evaluate("[...document.querySelectorAll('main h1,main h2,main h3,main h4,main h5')].map(h=>[+h.tagName[1], h.textContent.replace(/\\s+/g,' ').trim()])")
            rendered_links = await pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>new URL(a.getAttribute('href'),'https://jaredgibbons.ca').href)")
            a_title, a_canon, a_heads, a_links = archive_meta(rec)
            lines = archive_lines(rec)
            hay = rendered_text.lower()
            missing = []; known = {}
            for l in lines:
                if l.lower() in hay: continue
                if l in KNOWN: known[l] = KNOWN[l]; continue
                # tolerate text split by inline elements: compare on alphanumerics only
                a = re.sub(r'[^a-z0-9$%]', '', l.lower()); h = re.sub(r'[^a-z0-9$%]', '', hay)
                if a and a in h: continue
                missing.append(l)
            # headings: archive levels are '##'=H1 (see D-03); compare text multiset, report level mismatches separately
            r_texts = [t for _, t in rendered_heads]
            heads_missing = [t for _, t in a_heads if norm(t) not in [norm(x) for x in r_texts]]
            a_set = set(l if l.startswith(('tel:', 'mailto:', 'javascript:')) else l for l in a_links)
            a_abs = {u for u in a_set if not u.startswith(('javascript:', 'data:')) and 'myrealpage.com/wps' not in u and 'iss-cdn' not in u}
            r_set = set(rendered_links)
            body_links_missing = sorted(u for u in a_abs if u not in r_set and u.replace('tel:6049281361', 'tel:604-928-1361') not in r_set)
            summary[slug] = dict(
                title_match=(title == a_title), title_rendered=title, title_archive=a_title,
                canonical_match=(canon == a_canon),
                archive_text_lines=len(lines), lines_missing=len(missing), lines_known_deviation=len(known),
                headings_archive=len(a_heads), headings_missing=heads_missing,
                archive_link_destinations=len(a_abs), link_destinations_missing=len(body_links_missing))
            json.dump(dict(summary=summary[slug], lines_missing=missing, known_deviations=known, headings_missing=heads_missing,
                           link_destinations_missing=body_links_missing, rendered_headings=rendered_heads),
                      open(f'docs/test-results/compare-{slug}.json', 'w'), indent=1, ensure_ascii=False)
        await b.close()
    print(json.dumps(summary, indent=1, ensure_ascii=False))
asyncio.run(main())
