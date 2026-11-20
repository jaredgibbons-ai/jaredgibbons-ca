#!/usr/bin/env python3
"""Stock sales phrases out of Jared's own copy (buyer/seller review of Nov 20 2026; Jared: "Yes, outside of reviews"). D-388.

Old blog posts (src/data/posts) and four pages lose "Don't miss out", "stunning", "breathtaking", "nestled" and "dream home" phrasing, and
exclamation marks in post text become full stops. Left alone on purpose: Google review quotes, quoted listing copy ("YOU OWN YOUR LOT!"),
MLS® listing remarks (src/data/listings), post titles and H1s (they are what Google shows; URLs and titles stay), event names ("Lights On!"),
the PNE Prize Home ("Dream Home" is the lottery's name) and a news quote ("captured some stunning photos").
Idempotent: a second run changes nothing.   python3 -I tools/stock_copy_2026_11_20.py
"""
import glob, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DM = "Don[’']t [Mm]iss [Oo]ut"
EXACT = {   # whole-text swaps (part or heading text)
    "Your dream home should take priority over a new ride.": "The home should take priority over a new ride.",
    "Jared will help you find exactly what you're looking for, whether it's your dream home or a smart investment.": "Jared will help you find exactly what you're looking for, whether it's a home to live in or an investment.",
    "Whether you want to invest, develop, or find your dream home, Jared is ready to assist you.": "Whether you want to invest, develop or find a home to live in, Jared is ready to help.",
    "Don’t Miss Out on This Clayton/Cloverdale Condo!": "About This Clayton/Cloverdale Condo",
    "Find Your Dream Home at Matteo Residential Project": "Homes at the Matteo Residential Project",
    "Don’t miss this chance to own a stunning": "A chance to own a",
    "Nestled right beside": "Right beside",
    "$100,000 Price Drop Home in Langley – Don’t Miss Out!": "$100,000 Price Drop on a Langley Home",
    "Stunning Archstone Yorkson Townhome in Willoughby Heights": "Archstone Yorkson Townhome in Willoughby Heights",
}
SUBS = [   # inside any text
    (re.compile(DM + r"\s*[—–-]\s*act now and be part of the excitement!"), ''),
    (re.compile(DM + r" on this (incredible|fantastic) opportunity[^.!]*[.!]"), ''),
    (re.compile(r"discover your next dream home in"), 'find your next home in'),
    (re.compile(r"guide you toward your dream home"), 'help you find the right home'),
    (re.compile(r"\b[Ss]tunning(,\s*|\s+|(?=[a-z]))(?!photos)"), ''),
    (re.compile(r"\b[Bb]reathtaking\s*"), ''),
]
KEEP_EXCL = re.compile(r"Lights On!")

def fix_text(t, heading=False, excl=False):
    if t in EXACT: return EXACT[t]
    for rx, rep in SUBS: t = rx.sub(rep, t)
    if excl and not heading and '“' not in t and '"' not in t and not KEEP_EXCL.search(t):
        t = re.sub(r"!+(?=\s|$)", '.', t)
    return t

def fix_parts(parts, heading=False, excl=False):
    out = [dict(p) for p in parts]
    for i, p in enumerate(out):
        if not isinstance(p.get('t'), str): continue
        t = p['t']
        # "Don’t miss out—" / "Don’t miss out" + "— contact": drop the lead-in and capitalise what follows
        m = re.match(r"^(📞\s*)?" + DM + r"\s*[—–-]?\s*$", t)
        if m and i + 1 < len(out) and isinstance(out[i + 1].get('t'), str):
            p['t'] = m.group(1) or ''
            n = re.sub(r"^\s*[—–-]\s*", '', out[i + 1]['t'])
            out[i + 1]['t'] = n[:1].upper() + n[1:]
            continue
        t = re.sub(r"^(📞\s*)?" + DM + r"\s*[—–-]\s*(\w)", lambda mm: (mm.group(1) or '') + mm.group(2).upper(), t)
        p['t'] = fix_text(t, heading, excl)
    return out

def walk(path, excl):
    d = json.loads(path.read_text()); before = json.dumps(d, ensure_ascii=False)
    for b in d.get('blocks', []):
        if b.get('t') == 'h' and b.get('level') == 1: continue          # titles stay
        heading = b.get('t') == 'h'
        if isinstance(b.get('text'), str): b['text'] = fix_text(b['text'], heading, excl)
        if isinstance(b.get('parts'), list): b['parts'] = fix_parts(b['parts'], heading, excl)
        if b.get('t') == 'list':
            b['items'] = [fix_parts(it, False, excl) if isinstance(it, list) else it for it in b.get('items', [])]
    # a paragraph emptied by the swaps (a lone "Don't miss out on this incredible opportunity!") is dropped
    d['blocks'] = [b for b in d.get('blocks', []) if not (b.get('t') == 'p' and isinstance(b.get('parts'), list) and b['parts'] and not ''.join(str(x.get('t', '')) for x in b['parts']).strip() and json.dumps(b, ensure_ascii=False) not in before.split('"blocks"')[0])]
    if json.dumps(d, ensure_ascii=False) != before:
        raw = path.read_text(); ind = 2 if raw.startswith('{\n  "') else (1 if raw.startswith('{\n "') else None)
        sep = (',', ':') if ind is None and '":"' in raw[:200] else None
        path.write_text(json.dumps(d, ensure_ascii=False, indent=ind, separators=sep) + ('\n' if raw.endswith('\n') else ''))
        return True
    return False

changed = [p.name for p in sorted((ROOT / 'src/data/posts').glob('*.json')) if walk(p, True)]
PAGES = {   # four non-blog pages: one phrase each (archive copy)
    'src/data/pages/open-houses.json': ("Check out any Open House in your area!", "Check out any open house in your area."),
    'src/data/pages/fraser-valley-acreages-for-sale.json': ("stunning mountain backdrops", "mountain backdrops"),
    'src/data/pages/queens-park.json': ("breathtaking Victorian", "Victorian"),
    'src/data/pages/capitol-hill-bn.json': ("prized for its breathtaking views", "known for its views"),
}
for f, (a, b) in PAGES.items():
    p = ROOT / f
    if p.exists() and a in p.read_text():
        p.write_text(p.read_text().replace(a, b)); changed.append(p.name)
print(len(changed), 'files changed'); print('\n'.join(changed))
