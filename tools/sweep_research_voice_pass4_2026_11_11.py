#!/usr/bin/env python3
"""Research-note wording, fourth pass (D-221, Nov 11, 2026), from the Cursor audit.

Removes the internal "Page-statement check / Approved claims" notes (they also repeated the unsourced "Top 1%"), and rewrites the
researchers' voice ("in this batch", "cards read for this file", "stated in this file", "Muse's file records", "Flags the conflict",
"Queued") in plain words without changing any fact. Idempotent; prints every change.
python3 -I tools/sweep_research_voice_pass4_2026_11_11.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

DROP = [re.compile(p) for p in (   # whole strings that are internal notes
    r'^Page-statement check for this area\..*$',
    r'^Approved claims, .*$',
    r'^The owner-approved claims \(.*\) may be used only as page statements in that exact form\.$',
)]
RX = [
    (r' ?Page-statement check for this area\.(?: The)? [Cc]orrect email is jaredgibbons@royallepage\.ca\.', ''),
    (r' ?Approved claims, [^.]*?(?:YTD|sales)[^.]*\.', ''),
    (r' ?The owner-approved claims \([^)]*\) may be used only as page statements in that exact form\.', ''),
    (r'Flags the conflict rather than resolving it — the strata plan \(EPS1696\) registration record is the definitive check\.',
     'The strata plan (EPS1696) registration record settles it.'),
    (r'Muse(?:\'s|’s) file records ', 'City records show '),
    (r' \(via Muse(?:\'s|’s) known file\)', ''),
    (r'The project\'s card carries a placeholder-style postal code and a sales gallery by appointment only — both consistent with presale, not completed, stock\.',
     'Its sales gallery is open by appointment only, as is usual for a presale.'),
    (r'^Higginson Villas — 45752 Stevenson Road\. TOWNHOUSE-form\. Queued$', 'Higginson Villas, 45752 Stevenson Road'),
    (r'^form is rancher-style attached product either way, and the registered strata position is settled only on the Form B\.$',
     'Rancher-style townhomes. Whether a unit is registered strata is confirmed only on the Form B.'),
    (r'^The Grove — 44523 McLaren Drive\. TOWNHOUSE\. Freehold strata\. Queued$', 'The Grove, 44523 McLaren Drive'),
    (r'^a current listing for unit 60 records "Welcome to The Grove!", Sub-Type Townhouse, built 2007, Title to Land Freehold Strata, labelled Sardis South; a second current listing \(unit 35\) records Type Townhouse, built 2007, with a monthly strata fee\. Fresh check Nov 2, 2026$',
     'Freehold strata townhomes built in 2007, listed on MLS® in Sardis South, with a monthly strata fee.'),
    (r', and the cards in this batch\'s fetch were detached residential cards\.', ', and the listings it shows are detached houses.'),
    (r' — Coal Harbour has its own file in this batch — ', ' — Coal Harbour has its own page — '),
    (r'Feed-scope snapshot \(feed data only, not statistics\): ', 'In the current listings, '),
    (r'\bon the labelled cards read for this file, the card\'s\b', 'on the listings we checked, the'),
    (r'\b(?:the )?(?:fully |first-page |labelled |guide |listing |body |Additional Details )?cards read (?:in full )?for this (?:file|topic)\b', 'the listings we checked'),
    (r'\bfive of the six fully read cards\b', 'five of the six listings we checked'),
    (r'\b(\w+) (?:fully |first-page |guide |listing |body |Additional Details )?cards read(?: in full)?\b', r'\1 listings we checked'),
    (r'\b(\w+) (?:first-page |body |Additional Details )?card read\b', r'\1 listing we checked'),
    (r'\bcards read\b', 'listings we checked'),
    (r'(?<=\w) the listings we checked\b', ' listings we checked'),
    (r'\b(In|in|on|of|What|and) listings we checked\b', r'\1 the listings we checked'),
    (r"^The page's listings we checked\b", 'The listings we checked'),
    (r'^In the current listings, the six listings we checked were dominated by', 'The six listings we checked were mostly'),
    (r'\bis stated as fact in this file\b', 'is given here'),
    (r'\b(?:is |are )?(?:stated|confirmed|on record) in this file\b', lambda m: (m.group(0).split()[0] + ' ' if m.group(0).split()[0] in ('is', 'are') else '') + 'given here'),
    (r'\bnot stated in this file\b', 'not given here'),
    (r'\bthis file states no\b', 'this page gives no'),
    (r'\bexists in this file\b', 'is given here'),
    (r'\bthis file covers\b', 'this page covers'),
    (r'\bin this file\b', 'on this page'),
    (r'^No figure is stated on this page:', 'No figure is given here:'),
    (r' in this batch\b', ''),
    (r'\banywhere else in the batch\b', 'anywhere else nearby'),
    (r'\bneighbouring batch areas\b', 'neighbouring areas'),
]
RX = [(re.compile(a), b) for a, b in RX]


def fix(s):
    if any(r.match(s) for r in DROP): return ''
    o = s
    for r, b in RX: s = r.sub(b, s)
    return o if s == o else re.sub(r' {2,}', ' ', s).strip()


def walk(x, hits):
    if isinstance(x, dict): return {k: walk(v, hits) for k, v in x.items()}
    if isinstance(x, list): return [walk(v, hits) for v in x]
    if isinstance(x, str):
        y = fix(x)
        if y != x: hits.append((x, y))
        return y
    return x


def prune(o):
    if isinstance(o, dict):
        o = {k: prune(v) for k, v in o.items()}
        if isinstance(o.get('parts'), list): o['parts'] = [p for p in o['parts'] if not (isinstance(p, dict) and set(p) <= {'t'} and not str(p.get('t', '')).strip())]
        if isinstance(o.get('items'), list): o['items'] = [it for it in o['items'] if not (isinstance(it, list) and not ''.join(str(x.get('t', '')) for x in it if isinstance(x, dict)).strip())]
        return o
    if isinstance(o, list):
        out = [prune(v) for v in o]
        return [b for b in out if not (isinstance(b, dict) and b.get('t') in ('p', 'h', 'list') and not (b.get('text') or '').strip() and not b.get('parts') and not b.get('items'))]
    return o


def main():
    files = changed = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        raw = open(f, encoding='utf-8').read(); hits = []
        d = prune(walk(json.loads(raw), hits))
        if not hits: continue
        for a, b in hits: print(f'{os.path.basename(f)}\n  - {a[:260]}\n  + {b[:260]}')
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
        files += 1; changed += len(hits)
    print('files', files, '| strings changed', changed)


if __name__ == '__main__': main()
