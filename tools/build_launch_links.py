#!/usr/bin/env python3
"""Inbound links for the 14 pages that had only one page linking to them (found by tools/launch_pack.py).
Each target gets links from up to three related hubs, in one 'More guides and searches' list per hub (gen 'launchlinks').
    python3 -I tools/build_launch_links.py
"""
import json, os, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_new_searches as N
import build_area_gap_pages as A
seo = json.load(open('src/data/seo-final.json'))
NV = ['north-vancouver-homes-for-sale', 'north-vancouver-condos-for-sale', 'north-vancouver-real-estate-market-stats']
T = {
    'braemar-55-plus-homes-for-sale': NV, 'delbrook-55-plus-homes-for-sale': NV,
    'chartwell-55-plus-homes-for-sale': ['west-vancouver-homes-for-sale', 'west-vancouver-real-estate-market-stats', 'ambleside-55-plus-homes-for-sale'],
    'abbotsford-golf-course-homes-for-sale': ['abbotsford-homes-for-sale', 'abbotsford-neighbourhood-guides', 'abbotsford-real-estate-market-stats'],
    'langley-golf-course-homes-for-sale': ['langley-homes-for-sale', 'langley-neighbourhood-guides', 'langley-real-estate-market-stats'],
    'surrey-golf-course-homes-for-sale': ['surrey-homes-for-sale', 'surrey-neighbourhood-guides', 'surrey-real-estate-market-stats'],
    'west-vancouver-golf-course-homes-for-sale': ['west-vancouver-real-estate-market-stats', 'british-properties', 'dundarave-west-vancouver-guide'],
    'barnston-island-surrey-guide': ['surrey-neighbourhood-guides', 'surrey-real-estate-market-stats'],
    'lindell-beach-bc-guide': ['cultus-lake-guide', 'chilliwack-neighbourhood-guides'],
    'mount-currie-bc-guide': ['bc-condo-buying-rules', 'bc-townhome-buying-rules', 'bc-land-buying-rules'],
    'cloverdale-houses-with-suites-for-sale': ['cloverdale-neighbourhood-guides', 'surrey-homes-for-sale', 'cloverdale-real-estate-market-stats'],
    'north-delta-houses-with-suites-for-sale': ['north-delta-homes-for-sale', 'delta-homes-for-sale', 'delta-real-estate-market-stats'],
    'harrison-hot-springs-bc-guide': ['chilliwack-homes-for-sale', 'mission-homes-for-sale', 'fraser-valley-market-stats'],
    'hope-bc-guide': ['mission-homes-for-sale', 'fraser-valley-market-stats', 'fraser-valley-acreages-for-sale'],
    'kent-bc-guide': ['chilliwack-homes-for-sale', 'abbotsford-homes-for-sale', 'fraser-valley-market-stats'],
    'fraser-valley-commercial-market-report': ['fraser-valley-market-stats', 'langley-real-estate-market-stats', 'abbotsford-real-estate-market-stats'],
    'surrey-home-buyer-checklist': ['surrey-homes-for-sale', 'surrey-condos-for-sale', 'first-time-home-buyer-program'],
    'tsawwassen-home-buyer-checklist': ['tsawwassen-homes-for-sale', 'delta-homes-for-sale', 'first-time-home-buyer-program'],
}
GEN = 'launchlinks'
by = collections.defaultdict(list)
for tgt, hosts in T.items():
    if not N.exists(tgt): print('missing', tgt); continue
    got = 0
    for h in hosts:
        if h != tgt and os.path.exists(f'src/data/local/{h}.json') and got < 3: by[h].append(tgt); got += 1
    if got < 2: print('only', got, tgt)
for h, tg in by.items():
    A.end_link(h, GEN, 'More guides and searches', [((seo.get(t) or {}).get('h1') or t.replace('-', ' ').title(), t) for t in tg])
print(len(by), 'hubs updated')
