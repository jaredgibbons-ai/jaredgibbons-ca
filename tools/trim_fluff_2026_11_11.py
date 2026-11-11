#!/usr/bin/env python3
"""Fluff pass (D-223, Nov 11, 2026). Jared asked to remove fluff and unnecessary words across the site.

Three kinds of cut, in the archive pages, the local layer and the blog posts (never in reviews, quotes, Jared's take or listing remarks):
  1. Method notes repeated on hundreds of pages ("Facts here come from…", "Walking and driving times were measured…", "For each
     building named below…", "explained once, with sources, on the page linked below") are cut or cut down to a few words; the
     sources lists and links they pointed at stay.
  2. Research shorthand rewritten in plain words: the ALR residence-cap line with its statute citations, the farm-class line ("three-
     tiered … a flat $2,500+ line is an error"), "ALR block (provincial frame …)". Same facts.
  3. Filler phrases: "in order to", "It's important to note that", "In today's market,", "Additionally/Furthermore/Moreover,",
     "truly", "nestled in", "boasts", "a wide range of", "stunning", "sought-after", "vibrant", and "Whether you're X or Y," openers.
Idempotent; prints counts and --sample N examples. python3 -I tools/trim_fluff_2026_11_11.py [--dry] [--sample 20]"""
import collections, glob, json, os, random, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CNT = collections.Counter(); SAMPLES = collections.defaultdict(list)
up = lambda m, g: m.group(1) + m.group(g)[0].upper() + m.group(g)[1:]

ALR_CAP = re.compile(r'[;:]?\s*ALC residence caps(?: are|:) principal(?: residence)? ≤500 m²(?: \(no more than 1,000 m² of fill\))?, (?:a )?(?:secondary )?suite within (?:the )?principal(?: residence)? only, additional residence 90 m² \(≤40 ha\) / 186 m² \(>40 ha\)')
ALR_CAP_TXT = '. On ALR land the main house can be up to 500 m², a suite is allowed only inside it, and an extra residence can be up to 90 m² (186 m² on parcels over 40 ha)'
FARM = re.compile(r'(?:BC Assessment )?[Ff]arm(?:-| )class(?: thresholds in full three-tier form| is three-tiered) \(\$2,500 on 0\.8–4 ha; \$2,500 \+ 5% (?:of (?:the land\'s )?value )?over 4 ha; \$10,000 under 0\.8 ha; (?:applications )?by Oct(?:ober)? 31\)(?: — a flat "\$2,500\+" (?:line is an error|figure is wrong)(?:[,;] and (?:no flat line|no farm-class claim|it) is (?:not )?asserted[^.]*| \([^)]*\))?)?')
FARM_TXT = 'For farm class, BC Assessment looks for farm income of $10,000 a year on under 0.8 ha, $2,500 on 0.8 to 4 ha, and $2,500 plus 5% of the value of land over 4 ha; applications are due by October 31'

SENT = [   # (pattern, replacement) on whole strings or inside them
    (r' ?Facts here come from the municipality, TransLink or BC Transit, the Ministry of Education and Child Care, and the retailers’ own pages, listed under Sources\.', ''),
    (r'Walking and driving times were measured on OpenStreetMap routing on November 2, 2026, from the point named under the table\.', 'Times are from OpenStreetMap routing, November 2026.'),
    (r' ?For each building named below, the nearest transit, parks, schools and shopping come from TransLink or BC Transit, the municipality, the Ministry of Education and Child Care and the retailers’ own pages, listed under Sources\.', ''),
    (r'Walking and driving times were measured on November 2, 2026 on OpenStreetMap routing, starting at the building’s street address \(or the nearest point on its street where the map has no point for the building itself, marked in the table\)\.', 'Times are from OpenStreetMap routing from each building’s address, November 2026.'),
    (r' ?Facts that neighbouring buildings share are listed once, under the first of them\.', ''),
    (r' ?Details change, so use the links on each card to (?:double-check|confirm)\.', ''),
    (r' ?Facts come from the official sources noted on this page\.', ''),
    (r'These are the (\d+) closest neighbourhoods we cover to the centre point we use for [^.]+?, nearest first\.', r'The \1 closest neighbourhoods we cover, nearest first.'),
    (r'^What the official sources say about the homes and lots, then the questions I go through with buyers\.$', ''),
    (r'^This page names each building, says what type it is and what the sources show, and covers local rules and the questions buyers ask\.$', ''),
    (r'^Notes that also apply here are written up once, on these pages:$', 'See also:'),
    (r'^The BC rules on 55\+ age bylaws, who may own and who may live in a unit, the exemptions and rentals apply in every strata and are explained once, with sources, on the BC 55\+ strata rules page\.$',
     'BC’s 55+ rules (age bylaws, who may live in a unit, exemptions and rentals) apply in every strata and are on the BC 55+ strata rules page.'),
    (r'ALR block \(provincial frame, applied only where a parcel is in the ALR\): ([a-z])', lambda m: 'If a parcel is in the ALR: ' + m.group(1)),
    (r'ALR rules \(for completeness — no [^)]{3,80} is confirmed here\): ([a-z])', lambda m: 'If a parcel is in the ALR: ' + m.group(1)),
    (r'ALR rules — general framework, no ALR ground documented in this sub-area: where a parcel is in the ALR, ([a-z])', lambda m: 'If a parcel is in the ALR: ' + m.group(1)),
    (r' \((?:ALC Bulletin 09 s\. ?6; (?:SPA|Strata Property Act) s\. ?239; (?:ALCA|Agricultural Land Commission Act) s\. ?21\(1\))\)', ''),
]
SENT = [(re.compile(a), b) for a, b in SENT]
FLUFF = [
    (re.compile(r'\bin order to\b'), 'to'),
    (re.compile(r'(^|[.!?]\s+)(?:It’s|It\'s|It is) (?:important|worth) (?:to note|noting) that ([a-z])'), lambda m: up(m, 2)),
    (re.compile(r'(^|[.!?]\s+)In today(?:’|\')s (?:real estate |competitive |current )?market, ([a-z])'), lambda m: up(m, 2)),
    (re.compile(r'(^|[.!?]\s+)(?:Additionally|Furthermore|Moreover), ([a-z])'), lambda m: up(m, 2)),
    # "Whether you're X or Y," openers, unless the clause names places or types (it then carries the page's search terms)
    (re.compile(r'(^|[.!?]\s+)Whether you(?:’re|\'re| are) ([^.?!]{3,200}? or [^,.?!]{2,120}), ([a-z])'), lambda m: m.group(0) if re.search(r'[A-Z]', m.group(2)) else m.group(1) + m.group(3).upper()),
    (re.compile(r'\btruly '), ''),
    (re.compile(r'\bnestled (in|on|among|between|along|at|beside|within)\b'), r'\1'),
    (re.compile(r'\bNestled (in|on|among|between|along|at|beside|within)\b'), lambda m: m.group(1).capitalize()),
    (re.compile(r'\bboasts\b'), 'has'), (re.compile(r'\bboasting\b'), 'with'),
    (re.compile(r'\ba wide (?:range|variety) of\b'), 'many'),
    (re.compile(r'\b(a|an|the|this|its|their|with|of) (?:stunning|vibrant|sought-after) (?=[a-z0-9])'), lambda m: ('a' if m.group(1) == 'an' else m.group(1)) + ' '),
]


def clean(s, where):
    if not s or s.startswith('“') or s.startswith('"'): return s
    o = s
    for r, b in SENT:
        n = len(r.findall(s))
        if n: s = r.sub(b, s); CNT['method / research: ' + r.pattern[:40]] += n
    if ALR_CAP.search(s): s = ALR_CAP.sub(ALR_CAP_TXT, s); CNT['ALR cap line'] += 1
    if FARM.search(s):
        s = FARM.sub(FARM_TXT, s); CNT['farm class line'] += 1
        s = re.sub(r'([;,]) For farm class', r'. For farm class', s)
    for r, b in FLUFF:
        n = len(r.findall(s))
        if n: s = r.sub(b, s); CNT['filler: ' + r.pattern[:34]] += n
    s = re.sub(r'\.\.(?=\s|$)', '.', re.sub(r' {2,}', ' ', s)).replace(' .', '.') if s != o else s
    if s != o: SAMPLES[where].append((o, s))
    return s.strip() if s != o else s


def walk(o, where, skip=False):
    if isinstance(o, dict):
        if o.get('t') == 'reviews' or o.get('by') == 'jared' or o.get('quote'): return o
        return {k: (walk(v, where) if k not in ('h', 'href', 'id', 'gen', 'pos', 'slug', 'url', 'canonical', 'path', 'cls', 'seo') else v) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, where) for v in o]
    if isinstance(o, str): return clean(o, where)
    return o


def merge_rule_links(blocks):
    """'The BC rules … are explained once, with sources, on the page linked below.' + a one-link list -> one line with the link."""
    out, i, n = [], 0, 0
    while i < len(blocks):
        b = blocks[i]; nx = blocks[i + 1] if i + 1 < len(blocks) else None
        txt = b.get('text', '') if isinstance(b, dict) and b.get('t') == 'p' else ''
        if txt and re.search(r'explained once, with sources, on the page linked below\.$', txt) and isinstance(nx, dict) and nx.get('t') == 'list' and len(nx['items']) == 1 and len(nx['items'][0]) == 1 and nx['items'][0][0].get('h'):
            link = nx['items'][0][0]
            keep = {k: v for k, v in b.items() if k in ('gen', 'pos')}
            out.append({**keep, 't': 'p', 'parts': [{'t': 'The province-wide rules are on one page: '}, {'t': link['t'], 'h': link['h']}, {'t': '.'}]})
            i += 2; n += 1; continue
        out.append(b); i += 1
    return out, n


def prune(bl):
    return [b for b in bl if not (isinstance(b, dict) and b.get('t') == 'p' and 'text' in b and not b['text'].strip() and not b.get('parts'))]


def main():
    dry = '--dry' in sys.argv; ns = int(sys.argv[sys.argv.index('--sample') + 1]) if '--sample' in sys.argv else 0
    files = 0
    for f in sorted(glob.glob('src/data/pages/*.json') + glob.glob('src/data/local/*.json') + glob.glob('src/data/posts/*.json')):
        raw = open(f, encoding='utf-8').read(); d = json.loads(raw)
        before = json.dumps(d, ensure_ascii=False, sort_keys=True)
        if isinstance(d.get('blocks'), list):
            d['blocks'], m = merge_rule_links(d['blocks']); CNT['rules line + link merged'] += m
        d = walk(d, os.path.basename(f))
        if isinstance(d.get('blocks'), list): d['blocks'] = prune(d['blocks'])
        if json.dumps(d, ensure_ascii=False, sort_keys=True) == before: continue
        files += 1
        if dry: continue
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
    for k, v in sorted(CNT.items(), key=lambda kv: -kv[1]): print(f'{v:6}  {k}')
    print('files changed:', files, '(dry run)' if dry else '')
    if ns:
        allx = [(w, a, b) for w, xs in SAMPLES.items() for a, b in xs]; random.seed(1)
        for w, a, b in random.sample(allx, min(ns, len(allx))): print(f'\n[{w}]\n  - {a[:300]}\n  + {b[:300]}')


if __name__ == '__main__': main()
