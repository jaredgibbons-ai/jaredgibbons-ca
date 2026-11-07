#!/usr/bin/env python3
"""Final text pass over src/data/local/*.json: a count of exactly 1 takes the singular noun ("1 houses sold" -> "1 house sold").
Edits the raw file text, so file formatting is untouched.  Safe to rerun.  Labels such as "Phase 1 homes", "Hive 1 units" and "FM-1 houses" are left alone.
Run after any generator that writes counts:   python3 -I tools/fix_counts.py [--check]
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUB = [('condos and townhomes', 'condo or townhome'), ('houses', 'house'), ('condos', 'condo'), ('townhomes', 'townhome'), ('homes', 'home'), ('sales', 'sale'),
       ('listings', 'listing'), ('days', 'day'), ('neighbourhoods', 'neighbourhood'), ('buildings', 'building'), ('schools', 'school')]
PAT = re.compile(r'(?<![\w\-/$.,#:])1 (' + '|'.join(re.escape(a) for a, _ in SUB) + r')\b')
LABEL = re.compile(r'(Phase|Hive|Tower|Building|Block|Stage|Wave|Lot|Unit|Zone|Type|Level|Floor|Option|Step|Plan|Schedule|Part|Group|Class|Grade|Category|Section|Rule|Rank|No\.|Number) $')
MAP = dict(SUB)


def fix(t):
    def r(m):
        if LABEL.search(t[max(0, m.start() - 12):m.start()]): return m.group(0)
        return '1 ' + MAP[m.group(1)]
    return PAT.sub(r, t)


if __name__ == '__main__':
    check = '--check' in sys.argv; n = files = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
        t = open(f, encoding='utf-8').read(); u = fix(t)
        if u != t:
            c = len(PAT.findall(t)); n += 1; files += 1
            if not check: open(f, 'w', encoding='utf-8').write(u)
    print(('would change' if check else 'changed'), files, 'files')
    sys.exit(1 if check and files else 0)
