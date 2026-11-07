#!/usr/bin/env python3
"""Lead blocks (2026-11-07): which closing lead block each page gets, written to the local layer as `lead` (+ `lead_place`).

  quiz       "Where are you starting?" (5-step search quiz, posts to the forms Worker)   buyer pages: every page with a listings search, and the school pages
  homevalue  "What is your {place} home worth?" (name, email, phone, address)            seller-intent pages: neighbourhood guides, market stats, sold prices, city hubs
Pages that already carry a form or a calculator for it (home-evaluation, contact, the designed buying/selling pages), utility pages and the 404 get neither.
python3 -I tools/build_lead_blocks.py
"""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_area_gap_pages as A

IDX = json.load(open('src/data/idx-embeds.json'))
MAP = json.load(open('src/data/snapstats/_mapping.json'))['mapped']
SKIP = {'404', 'contact', 'privacy', 'blog', 'reviews', 'testimonials', 'subscribe-to-our-newsletter', 'photo-credits', 'data-and-methodology', 'home-evaluation', 'buying', 'selling', 'index',
        'first-time-buyer-calculator', 'mortgage-calculator', 'net-proceeds-calculator'}
HUBS = {'south-surrey-homes-for-sale', 'langley-homes-for-sale', 'surrey-homes-for-sale', 'abbotsford-homes-for-sale', 'white-rock', 'chilliwack-homes-for-sale', 'delta-homes-for-sale',
        'mission-homes-for-sale', 'maple-ridge-homes-for-sale', 'coquitlam-homes-for-sale', 'burnaby-homes-for-sale', 'north-vancouver-homes-for-sale', 'west-vancouver-homes-for-sale',
        'vancouver-homes-for-sale', 'richmond-homes-for-sale', 'new-westminster-homes-for-sale', 'port-coquitlam-homes-for-sale', 'port-moody-homes-for-sale', 'sold-properties'}
buyer_pages = set(IDX['pages']) | set(IDX.get('special', {}))


def kind(slug):
    if slug in SKIP: return None, None
    if slug in HUBS or slug.endswith('-guide') or 'market-stats' in slug:
        place = MAP.get(slug, [None, None])[1] if slug.endswith('-guide') else None
        if place and re.fullmatch(r'[A-Za-z .\'-]+', place): return 'homevalue', place
        return 'homevalue', None
    if slug in buyer_pages or slug.startswith('homes-near-'): return 'quiz', None
    return None, None


n = {'quiz': 0, 'homevalue': 0, 'none': 0}
for f in sorted(glob.glob('src/data/local/*.json')):
    slug = os.path.basename(f)[:-5]
    k, place = kind(slug)
    def fn(d, k=k, place=place):
        for key in ('lead', 'lead_place'): d.pop(key, None)
        if k: d['lead'] = k
        if place: d['lead_place'] = place
    A.host_edit(slug, fn)
    n[k or 'none'] += 1
print(n)
