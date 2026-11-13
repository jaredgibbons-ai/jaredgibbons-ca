#!/usr/bin/env python3
"""Local context for short or unlinked blog posts (D-267).

Posts under 300 words, or with no link to another page of the site in their text, get one section at the end of the article:
where that area's market stands now (the newest board figures in src/data/market/), what the post means for buyers and sellers,
and links to the area's live listings, guide and market stats. Writes src/data/post-context.json; [slug].astro inserts it before
the author box. Every linked page must be built (run after `npm run build`).
    python3 -I tools/build_post_context.py
"""
import glob, html, json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
OUT = ROOT / 'src/data/post-context.json'
MKT = json.loads(sorted((ROOT / 'src/data/market').glob('20??-??.json'))[-1].read_text())
MONTH = __import__('datetime').date(int(MKT['month'][:4]), int(MKT['month'][5:]), 1).strftime('%B %Y')

# area: words that pick it (title or slug), label, (board, key), links
AREAS = [
 ('south-surrey', r'south surrey|white rock|crescent beach|ocean park|morgan|grandview|redwood|hazelmere|campbell heights|douglas|semiahmoo|holden|axis|kingsgate|xw.epiteng|ta.talu|heppell|biofuel|costco|nicomekl|highway|hwy 99', 'South Surrey and White Rock', ('fvreb', 'South Surrey & White Rock'),
  [('South Surrey homes for sale', '/south-surrey-homes-for-sale.html'), ('South Surrey and White Rock neighbourhood guides', '/south-surrey-neighbourhoods.html'), ('South Surrey and White Rock market stats', '/south-surrey-white-rock-real-estate-market-stats.html'), ('White Rock homes for sale', '/white-rock.html')]),
 ('cloverdale', r'cloverdale|clayton|waterstone|greenside', 'Cloverdale and Clayton', ('fvreb', 'Cloverdale'),
  [('Cloverdale homes for sale', '/cloverdale-bc.html'), ('Clayton guide', '/clayton-guide.html'), ('Cloverdale guide', '/cloverdale-bc-guide.html'), ('Cloverdale market stats', '/cloverdale-real-estate-market-stats.html')]),
 ('langley', r'langley|willoughby|yorkson|archstone|brookswood|aldergrove|walnut grove|campbell valley|gabby|pne|208a', 'Langley', ('fvreb', 'Langley'),
  [('Langley homes for sale', '/langley-homes-for-sale.html'), ('Langley neighbourhood guides', '/langley-neighbourhood-guides.html'), ('Langley market stats', '/langley-real-estate-market-stats.html'), ('Langley acreages for sale', '/langley-acreages-for-sale.html')]),
 ('maple-ridge', r'maple ridge', 'Maple Ridge', ('gvr', 'Maple Ridge'),
  [('Maple Ridge homes for sale', '/maple-ridge-homes-for-sale.html'), ('Maple Ridge neighbourhood guides', '/maple-ridge-neighbourhood-guides.html'), ('Maple Ridge market stats', '/maple-ridge-real-estate-market-stats.html')]),
 ('mission', r'mission', 'Mission', ('fvreb', 'Mission'),
  [('Mission homes for sale', '/mission-homes-for-sale.html'), ('Mission neighbourhood guides', '/mission-neighbourhood-guides.html'), ('Mission market stats', '/mission-real-estate-market-stats.html')]),
 ('chilliwack', r'chilliwack|vedder|sardis', 'Chilliwack', None,
  [('Chilliwack homes for sale', '/chilliwack-homes-for-sale.html'), ('Chilliwack neighbourhood guides', '/chilliwack-neighbourhood-guides.html'), ('Vedder Crossing guide', '/vedder-crossing-guide.html')]),
 ('abbotsford', r'abbotsford', 'Abbotsford', ('fvreb', 'Abbotsford'),
  [('Abbotsford homes for sale', '/abbotsford-homes-for-sale.html'), ('Abbotsford neighbourhood guides', '/abbotsford-neighbourhood-guides.html'), ('Abbotsford market stats', '/abbotsford-real-estate-market-stats.html')]),
 ('port-coquitlam', r'port coquitlam|poco', 'Port Coquitlam', ('gvr', 'Port Coquitlam'),
  [('Port Coquitlam homes for sale', '/port-coquitlam-homes-for-sale.html'), ('Port Coquitlam market stats', '/port-coquitlam-real-estate-market-stats.html')]),
 ('coquitlam', r'coquitlam', 'Coquitlam', ('gvr', 'Coquitlam'),
  [('Coquitlam homes for sale', '/coquitlam-homes-for-sale.html'), ('Coquitlam presale condos and townhomes', '/coquitlam-presale-condos-and-townhomes.html'), ('Coquitlam market stats', '/coquitlam-real-estate-market-stats.html')]),
 ('richmond', r'richmond', 'Richmond', ('gvr', 'Richmond'),
  [('Richmond homes for sale', '/richmond-homes-for-sale.html'), ('Richmond market stats', '/richmond-real-estate-market-stats.html')]),
 ('vancouver', r'vancouver|mount pleasant|firenze|matteo', 'Vancouver', ('gvr', 'Vancouver East'),
  [('Vancouver homes for sale', '/vancouver-homes-for-sale.html'), ('Vancouver neighbourhood guides', '/vancouver-neighbourhood-guides.html'), ('Vancouver market stats', '/vancouver-real-estate-market-stats.html')]),
 ('penticton', r'penticton', 'Penticton', None,
  [('the map search', '/map-search.html'), ('my listings', '/our-listings.html')]),
 ('surrey', r'surrey|bolivar', 'Surrey', ('fvreb', 'Surrey'),
  [('Surrey homes for sale', '/surrey-homes-for-sale.html'), ('Surrey neighbourhood guides', '/surrey-neighbourhood-guides.html'), ('Surrey market stats', '/surrey-real-estate-market-stats.html')]),
]
FALLBACK = ('fraser-valley', 'the Fraser Valley', ('fvreb', 'Fraser Valley Board'),
  [('the map search', '/map-search.html'), ('Fraser Valley market stats', '/fraser-valley-market-stats.html'), ('South Surrey homes for sale', '/south-surrey-homes-for-sale.html'), ('Langley homes for sale', '/langley-homes-for-sale.html')])

TOPICS = [
 ('sold', r'act fast|\bcondo\b|\bsold\b|just sold|for sale|listing|price drop|priced|penthouse|townhome|condo for|corner unit|home tour|acreage|double-wide|4-plex|fourplex|assignment|spotlight|laundromat|coin laundry|development property|\d+ ?bed'),
 ('rates', r'bank of canada|rate cut|overnight rate|market update|market shifts|real estate trends|real estate update|happening in the fraser valley|farmland value|pre-sales'),
 ('policy', r'speculation|gst|budget|suite incentive|depreciation|love letters|tax\b'),
 ('growth', r'skytrain|guideway|highway|intersection|bridge|costco|development|supportive housing|redwood heights|biofuel|hotel|lease|school|elementary|housing (targets|project|needs)|transit|float homes|cannabis|public works|gabby'),
 ('life', r'.'),
]

def T(t, h=None): return {'t': t, **({'h': h} if h else {})}

def money(v): return '${:,.0f}'.format(v)

def pct(v): return ('up ' if v > 0 else 'down ' if v < 0 else 'flat ') + (f'{abs(v):.1f}%' if v else '')

def built(h): return (DIST / h.lstrip('/')).exists()

def market_list(label, board, key):
    src = MKT[board]['hpi'][key]
    rows = []
    for k, name in (('detached', 'Detached house'), ('townhouse', 'Townhouse'), ('apartment', 'Condo')):
        x = src.get(k)
        if x and x.get('benchmark'):
            rows.append([T(f'{name}: '), T(money(x['benchmark'])), T(f", {pct(x['chg_1y'])} from a year earlier".replace(', flat  from', ', flat from'))])
    who = 'Fraser Valley Real Estate Board' if board == 'fvreb' else 'Greater Vancouver REALTORS®'
    return rows, who

def topic_para(topic, area, links):
    # roles: the area's all-homes page, its guide (or guides index) and its market stats page
    home = links[0]
    guide = next((l for l in links if 'guide' in l[0].lower()), None)
    stats = next((l for l in links if 'market stats' in l[0]), None)
    if topic == 'sold':
        return [T(f'Thinking of selling a similar home in {area}? I price every listing on recent sales nearby and market it with professional photos, drone and video, laser floor plans and paid ads. See'),
                T('my marketing plan', '/selling.html'), T('or get a'), T('free home evaluation', '/home-evaluation.html'), T('. Buying? Browse'), T(home[0], home[1]),
                T('and set up an email alert so new listings reach you first.')]
    if topic == 'rates':
        return [T('Prices and rates change every month. For the newest numbers, see'), T(*(stats or ('Fraser Valley market stats', '/fraser-valley-market-stats.html'))), T(', and work out your own payment with the'),
                T('mortgage calculator', '/mortgage-calculator.html'), T('. If you are weighing whether to buy or sell now, I am happy to run the numbers for your situation.')]
    if topic == 'policy':
        return [T('Rules like this change what it costs to buy, own or sell. First-time buyers can check the'), T('first-time home buyer programs', '/first-time-home-buyer-program.html'),
                T('and the'), T('first-time buyer calculator', '/first-time-buyer-calculator.html'), T('; owners can see what their home is worth today with a'), T('free home evaluation', '/home-evaluation.html'), T('. Ask me how it applies to your home.')]
    ref = guide or stats or home
    ref = (re.sub(r'^the ', '', ref[0]), ref[1])
    what = 'for each neighbourhood and what is planned' if guide else 'for current prices by area' if ref is stats else 'for what is for sale'
    if topic == 'growth':
        return [T(f'New transit, roads, schools and buildings are among the first things buyers ask about in {area}, and they shape what nearby homes sell for over time. See the'), T(ref[0], ref[1]),
                T(what + ', and'), T(home[0], home[1]), T('for what you can buy there today.')]
    return [T(f'Community life is a big reason people choose {area}. Thinking of moving here? See the'), T(ref[0], ref[1]), T(what + ', and'), T(home[0], home[1]), T('for what is for sale now.')]

def main():
    P = json.loads((ROOT / 'src/data/post-listing-seo.json').read_text())
    prev = json.loads(OUT.read_text()) if OUT.exists() else {}
    out = {}
    for f in sorted(glob.glob(str(DIST / 'internal/blog/*.html'))):
        slug = os.path.basename(f)[:-5]
        t = open(f).read(); m = t[t.index('<main'):t.index('</main>')]
        art = re.sub(r'<(script|style)[\s\S]*?</\1>', '', m).split('class="abox"')[0]
        art = art.split('post-context')[0]
        words = len(html.unescape(re.sub(r'<[^>]+>', ' ', art)).split())
        inlinks = len(re.findall(r'href="/(?!about\.html|contact\.html)', art.split('byline')[-1]))
        if slug in prev: words = prev[slug]['words']
        elif words >= 300 and inlinks > 0: continue
        d = json.loads((ROOT / f'src/data/posts/{slug}.json').read_text())
        title = (P.get(slug, {}).get('title') or d['title'])
        hay = (title + ' ' + slug.replace('-', ' ') + ' ' + ' '.join(b.get('text', '') for b in d['blocks'] if b['t'] == 'h')).lower()
        a = next((x for x in AREAS if re.search(x[1], hay)), None)
        key, label, data, links = (a[0], a[2], a[3], a[4]) if a else FALLBACK
        topic = next(n for n, rx in TOPICS if re.search(rx, title.lower() + ' ' + slug.replace('-', ' ')))
        links = [l for l in links if built(l[1])]
        blocks = [{'t': 'h', 'level': 2, 'text': f"{re.sub(r'^the ', '', label)} real estate today ({MONTH})"}]
        if data:
            rows, who = market_list(label, *data)
            blocks.append({'t': 'p', 'parts': [T(f"Benchmark prices in {'Vancouver East' if data[1] == 'Vancouver East' else label} for {MONTH}, from the {who}:")]})
            blocks.append({'t': 'list', 'items': rows})
        blocks.append({'t': 'p', 'parts': topic_para(topic, label, links)})
        blocks.append({'t': 'p', 'parts': [T(f'More on {label}:')] + sum([[T(l[0], l[1]), T(',' if i < len(links) - 2 else (' and' if i == len(links) - 2 else '.'))] for i, l in enumerate(links)], [])})
        for b in blocks:
            for p in b.get('parts', []) + [q for it in b.get('items', []) for q in it]:
                if p.get('h'): assert built(p['h']), (slug, p['h'])
        out[slug] = {'words': words, 'area': key, 'topic': topic, 'blocks': blocks}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    import collections
    print(len(out), 'posts;', dict(collections.Counter(v['area'] for v in out.values())), dict(collections.Counter(v['topic'] for v in out.values())))

if __name__ == '__main__':
    main()
