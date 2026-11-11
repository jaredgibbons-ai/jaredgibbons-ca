#!/usr/bin/env python3
"""Guide format v2 on every guide: works / doesn't lists and sub-area prices (D-219, Nov 11, 2026).

Jared asked for the guide format to be finished on all guides. For the 109 guides that had only his verdict:
  - "What works / what doesn't": two of each per guide, in docs/research/guide-v2/wd-*.py. A line marked J is his own words from
    his take (shown with the "Jared" tag); a line marked F is a fact already sourced on that guide (no tag). Nothing new is claimed:
    every F line restates something the guide's own text and sources already say, and comparisons the guide doesn't source were cut.
  - The guide's MLS® sub-area key (from src/data/guide-facts.json, D-217), so the quick answer adds what homes sold for and the quick
    facts add the typical house and acreage.
Drive times wait for a working route service (the browser that runs them was unavailable on Nov 11). Idempotent.
python3 -I tools/build_guide_works_2026_11_11.py"""
import glob, json, os, runpy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)


def main():
    WD = {}
    for f in sorted(glob.glob('docs/research/guide-v2/wd-*.py')): WD.update(runpy.run_path(f)['WD'])
    gp = json.load(open('src/data/guide-plus.json', encoding='utf-8')); gf = json.load(open('src/data/guide-facts.json', encoding='utf-8'))
    lists = subs = 0; missing = []
    for slug, v in gp.items():
        if not isinstance(v, dict) or not v.get('lite'): continue
        if slug in WD and not any(x.get('by') == 'jared' and slug in ('port-kells-surrey-guide',) for x in v.get('works', [])):
            w, d = WD[slug]
            if not v.get('works'):
                v['works'] = [{'t': t, **({'by': 'jared'} if k == 'J' else {})} for k, t in w]
                v['doesnt'] = [{'t': t, **({'by': 'jared'} if k == 'J' else {})} for k, t in d]
                lists += 1
        elif not v.get('works'): missing.append(slug)
        k = gf.get(slug, {}).get('key')
        if k and not v.get('sub'): v['sub'] = k; subs += 1
    open('src/data/guide-plus.json', 'w', encoding='utf-8').write(json.dumps(gp, ensure_ascii=False, indent=1) + '\n')
    print('works/doesn’t added:', lists, '| sub-area keys:', subs, '| still without a list:', missing)


if __name__ == '__main__': main()
