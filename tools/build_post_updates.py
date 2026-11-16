#!/usr/bin/env python3
"""Updates on old blog posts (D-322). From the sitewide check (D-321) and 12 months of Search Console: posts with no clicks.

    python3 -I tools/build_post_updates.py   -> src/data/post-updates.json

Each entry: a dated update note shown under the title, and/or noindex (the post stays on the site and keeps its links; it leaves
the sitemap and Google's index). Applied in src/pages/internal/blog/[slug].astro; the sitemap skips noindex posts.
  - Articles that are still useful get an update with today's figures (Paragon 12-month aggregate) or the newer news, and stay indexed.
  - Old listing ads (new listing, price drop, sold) get a note that the listing has ended, with a link to homes for sale now, and are noindexed.
  - Past community events are noindexed.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import build_sold_layer as S  # noqa: E402

DAY = '2026-11-16'
agg = S.load()
SS = agg['city']['south-surrey']['groups']
WR = agg['sub']['South Surrey White Rock|White Rock']['groups']
W = S.WINDOW
m = S.money


def note(*parts):
    """'text', ('link text', '/href'), 'text' -> parts"""
    return [{'t': p} if isinstance(p, str) else {'t': p[0], 'h': p[1]} for p in parts]


ARTICLES = {
    'south-surrey-to-produce-skytrain-guideway-segments-for-transit-expansi-8243032': note(
        'Update, November 2026: the Surrey Langley SkyTrain guideway is about 65% built and its foundations more than 95%, with work under way at all eight new stations between King George and Langley City Centre. The Province expects the line to open in 2029 (', ('B.C. government, September 21, 2026', 'https://news.gov.bc.ca/releases/2026TT0102-001115'), ').'),
    'surrey-council-reviews-new-costco-plan-oct-2025-8836736': note(
        'Update: the Costco application went on to its third reading in November 2025. See ', ('New South Surrey Costco moves forward after council approval', '/blog.html/new-south-surrey-costco-moves-forward-after-council-approval-8860491'), '.'),
    'south-surrey-realtor-july-2025-market-update-8773603': note(
        f'Update, November 2026: from {W}, {SS["house"]["n"]} South Surrey houses sold at a median {m(SS["house"]["price"])}, {SS["townhome"]["n"]} townhomes at {m(SS["townhome"]["price"])} and {SS["condo"]["n"]} condos at {m(SS["condo"]["price"])} (Paragon closed sales, White Rock counted separately). The monthly numbers are on ',
        ('South Surrey and White Rock market stats', '/south-surrey-white-rock-real-estate-market-stats.html'), '.'),
    'top-south-surrey-realtor-jared-gibbons---south-surrey-real-estate-expe-8760189': note(
        'Update: each South Surrey neighbourhood now has its own page with live listings and what homes sold for: ',
        ('Crescent Beach and Ocean Park', '/crescent-beach-ocean-park-houses-for-sale.html'), ', ', ('Grandview', '/grandview-south-surrey-houses-for-sale.html'), ', ',
        ('King George Corridor', '/king-george-corridor-south-surrey-houses-for-sale.html'), ', ', ('Morgan Creek', '/morgan-creek-south-surrey-houses-for-sale.html'), ', ',
        ('Elgin Chantrell', '/elgin-chantrell-south-surrey-houses-for-sale.html'), ', ', ('Sunnyside Park', '/sunnyside-park-south-surrey-houses-for-sale.html'), ', ',
        ('Pacific Douglas', '/pacific-douglas-south-surrey-houses-for-sale.html'), ' and ', ('White Rock', '/white-rock.html'), '.'),
    'langley-acreages-over-4-acres-best-prices-in-years-8774922': note(
        'Update: the acreages for sale today, with what Langley acreages have sold for, are on ', ('Langley acreages for sale', '/langley-acreages-for-sale.html'), '.'),
    'south-surrey-3-bed-townhomes-under-800k-best-prices-in-years-8774919': note(
        f'Update, November 2026: from {W}, {SS["townhome"]["n"]} South Surrey townhomes sold at a median {m(SS["townhome"]["price"])}, half of them within {SS["townhome"]["dom"]} days (Paragon closed sales). See ',
        ('South Surrey townhomes for sale', '/south-surrey-townhomes-for-sale.html'), ' and ', ('townhomes under $1.2M', '/south-surrey-townhomes-under-1-2m.html'), '.'),
    'south-surrey-condos-under-420k-affordable-coastal-8774918': note(
        f'Update, November 2026: from {W}, {SS["condo"]["n"]} South Surrey condos sold at a median {m(SS["condo"]["price"])} and {WR["condo"]["n"]} White Rock condos at {m(WR["condo"]["price"])} (Paragon closed sales). See ',
        ('South Surrey condos for sale', '/south-surrey-condos-for-sale.html'), ' and ', ('White Rock condos for sale', '/white-rock-condos-for-sale.html'), '.'),
    'why-now-is-the-time-to-buy-or-sell-in-langley-real-estate-8741014': note(
        'Update: this was written in July 2025. Today\'s figures are on ', ('Langley real estate market stats', '/langley-real-estate-market-stats.html'), '.'),
}
# old listing ads: id -> (where to look now, link)
ADS = {
    '8428837': ('Langley', '/langley-townhomes-for-sale.html'), '8431723': ('BC farms', '/farms.html'), '8488866': ('Maple Ridge', '/maple-ridge-homes-for-sale.html'),
    '8539204': ('Langley', '/langley-houses-for-sale.html'), '8888665': ('Chilliwack', '/chilliwack-condos-for-sale.html'), '8833648': ('Langley', '/langley-condos-for-sale.html'),
    '8742340': ('Langley', '/langley-acreages-for-sale.html'), '8672454': ('Vancouver', '/vancouver-homes-for-sale.html'), '8427440': ('Langley', '/langley-acreages-for-sale.html'),
    '8654085': ('Mission', '/mission-mobile-homes.html'), '8685830': ('Langley', '/langley-houses-for-sale.html'), '8735091': ('Langley', '/langley-houses-for-sale.html'),
    '8673946': ('Maple Ridge', '/maple-ridge-townhomes-for-sale.html'), '8660216': ('Langley', '/langley-houses-for-sale.html'), '8727619': ('Surrey', '/surrey-condos-for-sale.html'),
    '8702460': ('Vancouver', '/vancouver-homes-for-sale.html'), '8777220': ('South Surrey', '/south-surrey-condos-for-sale.html'), '8886776': ('South Surrey', '/south-surrey-condos-for-sale.html'),
}
EVENTS = ['8243011', '8240652', '8240649', '8243016', '8240650', '8423107']


def main():
    posts = {p.stem for p in (ROOT / 'src/data/posts').glob('*.json')}
    pages = {p.stem for p in (ROOT / 'src/data/local').glob('*.json')} | {p.stem for p in (ROOT / 'src/data/pages').glob('*.json')}
    out = {}
    for s, parts in ARTICLES.items():
        assert s in posts, s
        out[s] = {'updated': DAY, 'note': parts}
    by_id = {p[-7:]: p for p in posts}
    for i, (where, href) in ADS.items():
        assert href.strip('/').replace('.html', '') in pages, href
        out[by_id[i]] = {'updated': DAY, 'noindex': True, 'note': note('Update: this listing has ended. See ', (f'{where} homes for sale now' if where != 'BC farms' else 'farms for sale now', href), '.')}
    for i in EVENTS:
        out[by_id[i]] = {'noindex': True}
    for v in out.values():
        for p in v.get('note', []):
            h = p.get('h', '')
            if h.startswith('/') and not h.startswith('/blog.html/'): assert h.strip('/').replace('.html', '') in pages, h
    (ROOT / 'src/data/post-updates.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(len(out), 'posts;', sum(1 for v in out.values() if v.get('noindex')), 'noindex;', sum(1 for v in out.values() if v.get('note') and not v.get('noindex')), 'updated and indexed')


if __name__ == '__main__':
    main()
