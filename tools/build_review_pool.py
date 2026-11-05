"""Builds src/data/review-excerpts.json from Jared's Google 5-star review export (Nov 1, 2026): tools/data/google-reviews-2026-11-01.json
(extracted from docs/research/jared-google-5-star-reviews-2026-11-01.pdf). Rules: wording is verbatim (whole sentences, cut with a trailing
ellipsis), initials only, no team or third-party names, no reviews about a death in the family or a hard time in someone's life, rating-only
reviews skipped. Each excerpt is tagged from the words in the excerpt itself, so a page only gets an excerpt about condos if the
excerpt says condo.   python3 -I tools/build_review_pool.py
"""
import json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
raw = json.load(open(os.path.join(ROOT, 'tools/data/google-reviews-2026-11-01.json'), encoding='utf-8'))
old = json.load(open(os.path.join(ROOT, 'src/data/review-excerpts.json'), encoding='utf-8'))
SKIP_TEXT = re.compile(r'estate\.|tough time in my life|Being on my own|Realty\b')     # personal circumstances, a firm name
NAMES = re.compile(r'\b(Tyler|Pam|Marilyn|Turnbull)\b')                                 # team members and signatures
MAXLEN = 250
TAGS = {'condo': r'\bcondos?\b|\bapartment', 'townhome': r'townho(me|use)', 'duplex': r'duplex', 'house': r'\bhouses?\b|family home|single[- ]family',
        'sell': r'\bsell|\bsold\b|\bsale\b|\blisting\b|\blisted\b', 'buy': r'\bbuy|\bbought\b|purchas|home-?buyer', 'first': r'first[- ]time|first home|newcomers',
        'invest': r'investment propert', 'commercial': r'commercial|lease', 'langley': r'Langley', 'surrey': r'Surrey|White Rock', 'ladner': r'Ladner|Delta',
        'poco': r'Port Coquitlam', 'vancouver': r'Vancouver|lower mainland', 'negotiate': r'negotiat', 'repeat': r'\b(two|three|four|2|3|4) (houses|homes|times|properties)|multiple|many times|both buying and selling|buy and sell|bought and sold|purchase and sale|buying and selling|selling or buying|Purchase/Sale|10 years'}


def initials(s): return ''.join(c + '.' for c in s)
def sentences(t): return re.split(r'(?<=[.!?”"])\s+(?=[A-Z“"])', t)


def excerpt(t):
    t = re.sub(r'\s+[A-Z]{2}$', '', t) if re.search(r'\.\s+[A-Z]{2}$', t) else t   # trailing self-signed initials
    t = re.sub(r'\s+([,.;:!?])', r'\1', t.strip('"').strip())
    if SKIP_TEXT.search(t): return None
    ss = [s for s in sentences(t) if not NAMES.search(s)]
    if not ss: return None
    if len(' '.join(ss)) <= MAXLEN and len(ss) == len(sentences(t)): return ' '.join(ss)
    out = ''
    for s in ss:
        if out and len(out) + len(s) + 1 > MAXLEN: break
        if not out and len(s) > MAXLEN: return None
        out = (out + ' ' + s).strip()
    return re.sub(r'[.]$', '', out) + '…' if out else None


oldwhen = {(o['who'], re.sub(r'[“”…\s]+', ' ', o['quote'])[:40]): o['when'] for o in old['items']}
items = []
for r in raw:
    q = excerpt(r['text'])
    if not q or len(q) < 40 or (q.endswith('…') and len(q) < 90): continue
    who = initials(r['i'])
    when = next((w for (k, s), w in oldwhen.items() if k == who and s.strip()[:25] == re.sub(r'[“”…\s]+', ' ', q)[:25].strip()), 'Google review')
    tags = [k for k, rx in TAGS.items() if re.search(rx, q, re.I)]
    items.append({'stars': 5, 'quote': '“' + q + '”', 'who': who, 'when': when, 'tags': tags})
out = {'heading': old['heading'], 'intro': old['intro'], 'items': items}
json.dump(out, open(os.path.join(ROOT, 'src/data/review-excerpts.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
import collections
c = collections.Counter(t for i in items for t in i['tags'])
print(len(items), 'excerpts;', dict(c))
