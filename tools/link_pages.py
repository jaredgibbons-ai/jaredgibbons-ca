"""Related-links list (gen "relatedlinks", end of page) for every page that has fewer than 5 contextual links in its main content.
The region comes from the page's title/slug (Vancouver, Richmond, North Vancouver, ...). The list holds the region's hub, market stats, selling page,
schools list, home-type pages and neighbouring pages in the same region (ring order, so every page also gains inbound links). Pages with no
region get the main hubs. Minimum after this run: 5 links in main on every content page.   python3 -I tools/link_pages.py [--min 5]
Run after build_muse_faq.py and npm run build (reads dist/ to count existing links)."""
import glob, json, os, re, sys, hashlib
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MIN = 5
SKIP = {'404', 'privacy', 'subscribe-to-our-newsletter', 'contact'}
REGIONS = [('North Vancouver', 'north-vancouver'), ('West Vancouver', 'west-vancouver'), ('New Westminster', 'new-westminster'), ('Port Coquitlam', 'port-coquitlam'), ('Port Moody', 'port-moody'),
           ('Pitt Meadows', 'pitt-meadows'), ('Maple Ridge', 'maple-ridge'), ('South Surrey', 'south-surrey'), ('White Rock', 'south-surrey-white-rock'), ('Vancouver', 'vancouver'), ('Richmond', 'richmond'),
           ('Burnaby', 'burnaby'), ('Coquitlam', 'coquitlam'), ('Surrey', 'surrey'), ('Langley', 'langley'), ('Abbotsford', 'abbotsford'), ('Mission', 'mission'), ('Chilliwack', 'chilliwack'),
           ('Delta', 'delta'), ('Ladner', 'delta'), ('Tsawwassen', 'delta'), ('Squamish', 'squamish'), ('Whistler', 'whistler')]
SUFFIX = {'-nv': 'north-vancouver', '-wv': 'west-vancouver', '-ve': 'vancouver', '-vw': 'vancouver', '-ri': 'richmond', '-bn': 'burnaby', '-be': 'burnaby', '-bs': 'burnaby', '-nw': 'new-westminster', '-pm': 'port-moody', '-pq': 'port-coquitlam'}
FALLBACK = [('surrey-homes-for-sale', 'Surrey homes for sale'), ('south-surrey-homes-for-sale', 'South Surrey homes for sale'), ('langley-homes-for-sale', 'Langley homes for sale'),
            ('abbotsford-homes-for-sale', 'Abbotsford homes for sale'), ('burnaby-homes-for-sale', 'Burnaby homes for sale'), ('maple-ridge-homes-for-sale', 'Maple Ridge homes for sale'),
            ('sell-my-house-in-surrey', 'Sell my house in Surrey'), ('surrey-real-estate-market-stats', 'Surrey real estate market stats'), ('buying.html', 'Buying a home')]


def main():
    mn = MIN
    if '--min' in sys.argv: mn = int(sys.argv[sys.argv.index('--min') + 1])
    pages = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/pages/*.json'))}
    locs = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))}
    title = {s: d['title'] for s, d in pages.items()}
    for s, j in locs.items():
        if j.get('new_page'): title[s] = j['new_page']['title']
    exists = lambda s: s in title
    def region_of(s):
        t = title[s] + ' ' + s
        for suf, r in SUFFIX.items():
            if s.endswith(suf): return r
        for name, pre in REGIONS:
            if re.search(r'\b' + name + r'\b', title[s]): return pre
        return None
    reg = {s: region_of(s) for s in title}
    by_reg = {}
    for s, r in reg.items():
        if r and not s.endswith('-guide') and not re.search(r'under|over|foreclos|open-houses|schools-in|market-stats|presale|sell-my|mobile', s): by_reg.setdefault(r, []).append(s)
    for r in by_reg: by_reg[r].sort()
    # existing link count per page from dist
    n_existing = {}
    for f in glob.glob(os.path.join(ROOT, 'dist/*.html')):
        s = os.path.basename(f)[:-5]; h = open(f, encoding='utf-8').read(); m = re.search(r'<main[^>]*>(.*?)</main>', h, re.S)
        n_existing[s] = len(set(re.findall(r'<a [^>]*href="(/[^"#]*?)(?:#[^"]*)?"', m.group(1) if m else '')))
    done = 0
    for s in sorted(title):
        if s in SKIP or n_existing.get(s, 99) >= mn: continue
        r = reg.get(s); items = []
        def add(sl, text):
            if exists(sl) and sl != s and not any(i[0]['h'] == f'/{sl}.html' for i in items): items.append([{'t': text, 'h': f'/{sl}.html'}])
        if r:
            label = next(n for n, p in REGIONS if p == r) if any(p == r for _, p in REGIONS) else r.replace('-', ' ').title()
            for sl, text in ((f'{r}-homes-for-sale', f'{label} homes for sale'), (f'{r}-real-estate-market-stats', f'{label} real estate market stats'), (f'sell-my-house-in-{r}', f'Sell my house in {label}'),
                             (f'schools-in-{r}-bc', f'Schools in {label}'), (f'{r}-presale-condos-and-townhomes', f'{label} presale condos and townhomes'), (f'{r}-condos-for-sale', f'{label} condos for sale'),
                             (f'{r}-houses-for-sale', f'{label} houses for sale'), (f'{r}-townhomes-for-sale', f'{label} townhomes for sale')): add(sl, text)
            sib = by_reg.get(r, [])
            if s in sib:
                i = sib.index(s)
                for k in range(1, len(sib)):
                    if len(items) >= 12: break
                    o = sib[(i + k) % len(sib)]
                    add(o, re.split(r'\s[|:–-]\s|,', title[o])[0].replace(' Homes for Sale', '').strip() + ' real estate')
            elif sib:
                h0 = int(hashlib.md5(s.encode()).hexdigest(), 16)
                for k in range(len(sib)):
                    if len(items) >= 12: break
                    o = sib[(h0 + k) % len(sib)]; add(o, re.split(r'\s[|:–-]\s|,', title[o])[0].replace(' Homes for Sale', '').strip() + ' real estate')
        for sl, text in FALLBACK:
            if len(items) >= max(8, mn + 3): break
            add(sl.replace('.html', ''), text)
        lf = os.path.join(ROOT, 'src/data/local', s + '.json')
        j = locs.get(s) or {'status': 'draft', 'slug': s, 'updated': '2026-11-01', 'blocks': []}
        if j.get('hand_edited'): continue
        j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'relatedlinks']
        j['blocks'] += [{'t': 'h', 'level': 2, 'text': 'More real estate nearby' if r else 'Explore more', 'gen': 'relatedlinks', 'pos': 'end'}, {'t': 'list', 'items': items, 'gen': 'relatedlinks', 'pos': 'end'}]
        json.dump(j, open(lf, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(lf, 'a').write('\n'); done += 1
    print('pages given a related-links list:', done)


if __name__ == '__main__':
    main()
