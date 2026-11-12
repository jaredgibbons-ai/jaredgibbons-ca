#!/usr/bin/env python3
"""SUPERSEDED by tools/gsc_titles_2026_11_12.py (D-232, Jared chose the new titles); do not re-run.
D-231: keep the titles Google already ranks on the pages that earn search clicks.

Search Console (jaredgibbons.ca, 3 months to Nov 11, 2026, page report) lists the pages with 5+ clicks. Their new
titles (D-221 SEO pass) are swapped back to the archived title for launch, so the move changes only the platform,
not the words Google ranks. Retitle them later, a few at a time, once Search Console shows the move has settled.
Exceptions: the archived Richmond post title was cut off ("Just Sold! Thr..."), so the new title stays; "cloverdale"
gets its capital. H1s and descriptions are left as they are.
python3 -I tools/protect_top_pages_2026_11_12.py"""
import json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
PAGES = ['langley-mobile-homes', 'index', 'mission-mobile-homes', 'langley-foreclosures-court-ordered-sales', 'abbotsford-mobile-homes',
 'langley-horse-properties-equestrian-farms-for-sale-mls-listings', 'our-listings', 'broiler-farms-for-sale-bc', 'langley-acreages-for-sale',
 'abbotsford-farms', 'surrey-mobile-homes', 'campbell-valley-acreages-farms-for-sale', 'maple-ridge-mobile-homes', 'chicken-farms',
 'south-surrey-open-houses', 'south-surrey-mobile-homes', 'mobile-home-parks-fraser-valley', 'zonings', 'chilliwack-poultry-farms-for-sale',
 'egg-farms-for-sale-bc', 'surreyforeclosuresandcourtsales', 'langley-farms-for-sale-acreages-agricultural-land-mls', 'langley-poultry-farms-for-sale',
 'cost-of-mobile-home-pad-rental-fees-in-langley', 'cloverale-foreclosures-court-ordered-sales', 'poultry-farms-for-sale-bc',
 'langley-mobile-home-communities', 'jacobsen-townhomes-south-surrey', 'river-valley-guide', 'abbotsford-poultry-farms']
POSTS = ['a1-zoning-in-bc-what-it-means-for-buyers-jared-gibbons-8957123', '-safeway-sale-at-ocean-park-what-it-means-for-south-surrey-9116750',
 'ocean-park-townhomes-89-new-units-at-128-street-24-avenue-surrey-8969237', '20-avenue-overpass-at-highway-99-major-south-surrey-traffic-upgrade--8895555',
 'how-poultry-quota-works-in-bc-chicken-egg-and-turkey-farms-explained-9126255', 'new-south-surrey-condos-with-lock-off-suites-kingsgate-9093859',
 'buying-acreage-in-langley-alr-rural-plan-well-rules-9171874', 'brookswoods-big-new-development-langley-township-8939669']
FIX = {'cloverdale Foreclosures & Court Ordered Sales': 'Cloverdale Foreclosures & Court Ordered Sales'}

def archived(path):
    d = json.load(open(path)); t = ((d.get('seo') or {}).get('Title') or d.get('title') or '').strip()
    return FIX.get(t, t)

sf = json.load(open('src/data/seo-final.json')); n = 0
for slug in PAGES:
    f = f'src/data/pages/{slug}.json'
    if not os.path.exists(f): print('no archive page', slug); continue
    t = archived(f)
    if t and slug in sf and sf[slug].get('title') != t:
        print(f'{slug}: {sf[slug]["title"]!r} -> {t!r}'); sf[slug]['title'] = t; n += 1
    elif slug not in sf: print('not in seo-final', slug)
json.dump(sf, open('src/data/seo-final.json', 'w'), ensure_ascii=False, indent=1)
pl = json.load(open('src/data/post-listing-seo.json'))
for slug in POSTS:
    f = (glob.glob(f'src/data/posts/{slug}.json') or glob.glob(f'src/data/posts/*{slug}*.json'))
    if not f: print('no archive post', slug); continue
    t = archived(f[0])
    if slug in pl and pl[slug].get('title') != t:
        print(f'{slug}: {pl[slug]["title"]!r} -> {t!r}'); pl[slug]['title'] = t; n += 1
json.dump(pl, open('src/data/post-listing-seo.json', 'w'), ensure_ascii=False, indent=1)
print('titles restored', n)
