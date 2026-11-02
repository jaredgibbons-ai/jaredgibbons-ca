"""Assigns three Google review excerpts to every page so that no two pages show the same three and no excerpt is on more than ~12% of pages.
Match rules mirror the page topic (condo/townhome/sell/first-time/commercial/area words in the slug against the tags on each excerpt, see
tools/build_review_pool.py). Writes src/data/review-assign.json {slug: [excerpt index x3]}; src/lib/reviews.ts reads it.
    python3 -I tools/assign_reviews.py        (after npm run build, which lists the slugs in dist/)"""
import glob, hashlib, json, math, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EXEMPT = {'404', 'privacy', 'subscribe-to-our-newsletter', 'contact', 'reviews'}
WANT = [(r'condo|apartment|penthouse|presale|strata', 'condo', 3), (r'townho(me|use)', 'townhome', 3), (r'duplex', 'duplex', 3),
        (r'sell|selling|sold|evaluation|home-value|listing-presentation', 'sell', 2.5), (r'first-time|first-home|ftb|gst-rebate|ptt', 'first', 2.5),
        (r'commercial|lease|industrial|tilbury|annacis|west-chilliwack', 'commercial', 3), (r'invest|rental', 'invest', 3),
        (r'langley|aldergrove|willoughby|walnut-grove|murrayville|brookswood', 'langley', 1.5), (r'surrey|white-rock|ocean-park|crescent|cloverdale|grandview|morgan|elgin', 'surrey', 1.5),
        (r'ladner|tsawwassen|delta', 'ladner', 1.5), (r'port-coquitlam|coquitlam|poco', 'poco', 1.5), (r'vancouver|burnaby|new-westminster', 'vancouver', 1.2),
        (r'homes-for-sale|houses|real-estate|guide|acreage|waterfront|ocean-view', 'house', 0.8), (r'homes-for-sale|buy|guide|real-estate', 'buy', 0.6)]


def jitter(slug, i): return int(hashlib.md5(f'{slug}:{i}'.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF * 2.6


def main():
    items = json.load(open(os.path.join(ROOT, 'src/data/review-excerpts.json'), encoding='utf-8'))['items']
    slugs = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'dist/*.html')) if os.path.basename(f)[:-5] not in EXEMPT)
    cap = math.ceil(len(slugs) * 3 * 0.04)         # an excerpt may appear on at most ~12% of pages
    used, triples, out = {}, set(), {}
    for slug in slugs:
        want = {}
        for rx, tag, w in WANT:
            if re.search(rx, slug): want[tag] = w
        sell = 'sell' in want
        sc = []
        for i, r in enumerate(items):
            tags = r.get('tags', []); s = sum(want.get(t, 0) for t in tags)
            if sell and 'buy' in tags and 'sell' not in tags: s -= 2
            if not sell and 'sell' in tags and 'buy' not in tags and not ({'condo', 'townhome', 'duplex'} & set(want)): s -= 0.5
            sc.append((s + jitter(slug, i), i))
        sc.sort(reverse=True)
        pick = []
        for _, i in sc:
            if used.get(i, 0) < cap: pick.append(i)
            if len(pick) == 3: break
        k = 3
        while tuple(sorted(pick)) in triples:       # never repeat a set of three
            pick = pick[:2] + [next(i for _, i in sc[k:] if used.get(i, 0) < cap and i not in pick)]; k += 1
        triples.add(tuple(sorted(pick))); out[slug] = pick
        for i in pick: used[i] = used.get(i, 0) + 1
    json.dump(out, open(os.path.join(ROOT, 'src/data/review-assign.json'), 'w'), indent=0)
    print(len(out), 'pages;', len(triples), 'different sets; most-used excerpt on', max(used.values()), 'pages (cap', cap, '); excerpts used', len(used), 'of', len(items))


if __name__ == '__main__':
    main()
