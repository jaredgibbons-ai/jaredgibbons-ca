"""FAQ sections from Muse's area research workbook (docs/research/muse-area-research-master-2026-11-01.xlsx, tab "7 FAQs").

Rules (Jared, 2026-11-01: Muse is reference only): an answer is used only if it carries no UNVERIFIED / cannot / not-confirmed wording, is under 700
characters, and does not depend on a monthly market number (we compute those ourselves, so they never go stale). Source links in brackets are lifted
out of the answer text into a "Sources" list at the end of the page. Pages that end up with fewer than 3 questions get the honest generic pair below.
Every FAQ written here carries gen:"muse" so a re-run replaces it.        python3 -I tools/build_muse_faq.py
"""
import glob, json, os, re, sys
from urllib.parse import urlparse
import openpyxl
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXEMPT = {'404', 'privacy', 'subscribe-to-our-newsletter', 'reviews', 'index', 'blog', 'about', 'thank-you', 'contact', 'unsubscribe', 'terms', 'accessibility'}
import csv
AREA = {r['slug']: r['area'] for r in csv.DictReader(open(os.path.join(ROOT, 'docs/research/muse-keywords-2026-11-01.csv'), encoding='utf-8'))}
BAD = re.compile(r'UNVERIFIED|cannot|not confirmed|not published|could not', re.I)
MARKET = re.compile(r'SnapStats|September 2026|August 2026|sales ratio|inventory', re.I)
PAREN = re.compile(r'\s*\((?:https?://[^()]*|[^()]*https?://[^()]*)\)')
URL = re.compile(r'https?://[^\s,;)]+')


def clean(a):
    urls = [u.rstrip('.,') for p in PAREN.findall(a) for u in URL.findall(p)]
    a = PAREN.sub('', a); a = re.sub(r'\s+([.,;])', r'\1', a); a = re.sub(r'\s{2,}', ' ', a).strip()
    return a, urls


def main():
    wb = openpyxl.load_workbook(os.path.join(ROOT, 'docs/research/muse-area-research-master-2026-11-01.xlsx'), read_only=True, data_only=True)
    muse = {}
    for r in list(wb['7 FAQs'].iter_rows(values_only=True))[1:]:
        items = []
        for c in r[2:]:
            m = re.match(r'Q:\s*(.*?)\nA:\s*(.*)', c or '', re.S)
            if not m: continue
            q, a = m.group(1).strip(), m.group(2).strip()
            if BAD.search(a) or len(a) > 700 or MARKET.search(q + a): continue
            a, urls = clean(a)
            if 'http' in a or len(a) < 40: continue
            items.append({'q': q, 'a': a, 'gen': 'muse', 'urls': urls})
        muse[r[0]] = items
    pages = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    n_new = n_ext = n_gen = 0
    seen = set()      # Muse repeats the same question on an area page and its guide; each question is used once so twin pages do not share text
    slugs = sorted(set(pages) | {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}, key=lambda x: (x.endswith('-guide'), x))
    for s in slugs:
        if s in EXEMPT: continue
        lf = os.path.join(ROOT, 'src/data/local', s + '.json')
        j = json.load(open(lf, encoding='utf-8')) if os.path.exists(lf) else None
        if j and j.get('hand_edited'): continue
        title = (pages[s]['title'] if s in pages else j['new_page']['title']) if (s in pages or (j and j.get('new_page'))) else None
        if title is None: continue
        if j is None: j = {'status': 'draft', 'slug': s, 'updated': '2026-11-01', 'blocks': []}
        own = [f for f in j.get('faq', []) if f.get('gen') not in ('muse', 'muse-generic')]
        want = 5 if not own else 3
        pick = []
        for p_ in muse.get(s, []):
            key = (re.sub(r'\W+', ' ', p_['q'].lower()).strip(), re.sub(r'\W+', ' ', p_['a'].lower())[:80])
            if key[0] in {k[0] for k in seen} or key[1] in {k[1] for k in seen}: continue
            pick.append(p_); seen.add(key)
            if len(pick) == want: break
        faq = own + [{k: v for k, v in p.items() if k != 'urls'} for p in pick]
        name = AREA.get(s) or re.sub(r'^(Homes|Houses|Condos|Townhomes|Acreages?|Farms?|Land|Lots)( & \w+)* (for Sale )?(in|near) ', '', re.split(r'\s[|:–-]\s|,', title)[0].strip())
        name = re.sub(r'\s+(Homes|Houses|Condos|Townhomes|Acreages?|Real Estate|Guide|Listings)\b.*$', '', name).strip() or name
        if len(faq) < 3:
            where = f' in {name}' if s in AREA else ''
            for q, a in ((f'Can Jared show me homes{where}?' if s in AREA else 'Can I book a private showing with Jared?', f'Yes. Jared Gibbons, REALTOR® with Royal LePage Little Oak Realty, books private showings across the Fraser Valley and Metro Vancouver. Call or text 604-928-1361, or use the contact form on this site.'),
                         (f'How do I find out what my home{where} is worth?', 'Jared prepares a home evaluation from recent comparable sales and the condition of your home. Contact him on 604-928-1361 or through the form on this site to arrange one.')):
                faq.append({'q': q, 'a': a, 'gen': 'muse-generic'})
            n_gen += 1
        if not any(f.get('gen') == 'muse' for f in faq) and len(own) == len(faq): continue
        j['faq'] = faq
        urls = []
        for p in pick:
            for u in p['urls']:
                if 'jaredgibbons.ca' not in u and u not in urls: urls.append(u)
        j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'musefaq']
        if urls:
            j['blocks'] += [{'t': 'h', 'level': 2, 'text': 'Sources', 'gen': 'musefaq', 'pos': 'end'},
                            {'t': 'list', 'items': [[{'t': 'Source: ' + urlparse(u).netloc.lower().replace('www.', '') + (f' ({i + 1})' if sum(urlparse(x).netloc.lower() == urlparse(u).netloc.lower() for x in urls[:6]) > 1 else ''), 'h': u}] for i, u in enumerate(urls[:6])], 'gen': 'musefaq', 'pos': 'end'}]
        if os.path.exists(lf): n_ext += 1
        else: n_new += 1
        json.dump(j, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n')
    print('new local files', n_new, '| extended existing', n_ext, '| generic fill', n_gen)


if __name__ == '__main__':
    main()
