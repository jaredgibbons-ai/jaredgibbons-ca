"""Final pass over src/data/local/*.json: research-process wording must not reach a public page.

Rules (applied to every text string except links, tags and slugs):
  1. 'UNCONFIRMED' / 'UNVERIFIED' become plain 'not confirmed' / 'not verified'.
  2. A citation like '(as of September 2026, Source: SnapStats FVR September 2026 report)' becomes '(SnapStats, September 2026)'; a bare 'Source: SnapStats ... report.' is removed.
  3. A sentence that talks about the research itself or the old page it was read from ('at reading', 'for the rebuild', 'the page promises ...') (sibling files, batches, 'in this research', 'the notes', Jared's reports, locator results, a page 'at its reading') is dropped.
  4. A FAQ whose answer is left under 40 characters, or under 40% of a long answer, is dropped; an empty paragraph or list item is dropped; a heading left with nothing under it is dropped.
Idempotent.  Run last in the chain, before npm run build:   python3 -I tools/scrub_research_wording.py [--dry]
"""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
LOCAL = os.path.join(ROOT, 'src/data/local')
SKIP_KEYS = {'h', 'gen', 'slug', 'id', 'pos', 'level', 'status', 'href', 'img', 'src', 'alt'}
CITE = re.compile(r'\(?\bas of (\w+ 20\d\d),? Source: SnapStats(?: (?:FVR|GVR))?(?: \w+ 20\d\d)? report\)?\.?', re.I)
BARE = re.compile(r'\s*Source: SnapStats(?: (?:FVR|GVR))?(?: \w+ 20\d\d)? report\.?', re.I)
PROC = re.compile(r"\bsiblings?\b|\bbatch[- ]?\d|\bslug\b|research file|Jared.s reports|\bthe notes\b|\bin this research\b|\bthis research\b|\bat its reading\b|reading was|page text read|live page text|locator (?:returned|result)|no locator|\bnot read\b|were not read|was not read|\bfeed was\b|\bvisible feed\b|\bat reading\b|\bas read\b|\bfor the rebuild\b|\bpromises an? \w+|\bCentral absence\b|\bFeed snapshot\b|\bthis topic page\b", re.I)
SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9“"(])')
counts = {'sent': 0, 'case': 0, 'cite': 0, 'faq': 0, 'item': 0, 'head': 0}


def scrub(s):
    o = s
    s = CITE.sub(lambda m: f'(SnapStats, {m.group(1)})', s)
    s = BARE.sub('', s)
    if s != o: counts['cite'] += 1
    if re.search(r'\bUN(?:CONFIRMED|VERIFIED)\b', s):
        counts['case'] += 1
        s = re.sub(r'(^|[.!?]\s+|:\s+|\(\s*)UNCONFIRMED', lambda m: m.group(1) + 'Not confirmed', s)
        s = re.sub(r'(^|[.!?]\s+|:\s+|\(\s*)UNVERIFIED', lambda m: m.group(1) + 'Not verified', s)
        s = s.replace('UNCONFIRMED', 'not confirmed').replace('UNVERIFIED', 'not verified')
    s = re.sub(r'\s*\b(?:in|from|across) (?:this|the) research\b', '', s)   # 'verified in this research' reads fine as 'verified'
    s = re.sub(r'\s+as read in this pass\b', '', s); s = re.sub(r'\s+as read (?=in )', ' ', s)   # 'as read in Township council reports' is a real source, keep the sentence
    if PROC.search(s):
        parts = SENT.split(s); keep = [p for p in parts if not PROC.search(p)]
        if len(keep) != len(parts): counts['sent'] += len(parts) - len(keep); s = ' '.join(keep)
    return re.sub(r'\s{2,}', ' ', s).strip()


def walk(o, key=None):
    """Returns the cleaned value, or None when a string ends up empty."""
    if isinstance(o, str):
        if key in SKIP_KEYS: return o
        n = scrub(o) if (len(o) > 6 or 'UN' in o) else o
        return n if n or not o else None
    if isinstance(o, list):
        out = []
        for x in o:
            n = walk(x, key)
            if n is None or n == [] : counts['item'] += 1 if n is None else 0; continue
            out.append(n)
        return out
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            n = walk(v, k) if k not in SKIP_KEYS else v
            if n is None and k in ('text', 't') and 'h' not in o: return None
            out[k] = n if n is not None else v
        return out
    return o


def clean_file(j):
    bl = []
    for b in j.get('blocks', []):
        n = walk(b)
        if n is None: continue
        if n.get('t') in ('p', 'notice') and not (n.get('text') or n.get('parts')): continue
        if n.get('t') == 'list':
            n['items'] = [it for it in n.get('items', []) if it and any((x.get('t') or '').strip() for x in it)]
            if not n['items']: continue
        bl.append(n)
    # orphan headings (a heading followed by another heading of the same or higher level, or by nothing)
    out = []
    for i, b in enumerate(bl):
        if b.get('t') == 'h':
            nxt = bl[i + 1] if i + 1 < len(bl) else None
            if nxt is None or (nxt.get('t') == 'h' and nxt.get('level', 2) <= b.get('level', 2) and b.get('gen') == nxt.get('gen')):
                if b.get('gen'): counts['head'] += 1; continue
        out.append(b)
    j['blocks'] = out
    if j.get('faq'):
        fq = []
        for x in j['faq']:
            q = scrub(x.get('q', '')); a = scrub(x.get('a', ''))
            if len(a) < 40 or not q or (len(x.get('a', '')) > 160 and len(a) < max(70, 0.4 * len(x['a']))): counts['faq'] += 1; continue   # most of the answer was process wording: drop the question
            fq.append({**x, 'q': q, 'a': a})
        if fq: j['faq'] = fq
        else: j.pop('faq')
    return j


def main():
    dry = '--dry' in sys.argv; changed = 0
    for f in sorted(glob.glob(os.path.join(LOCAL, '*.json'))):
        j = json.load(open(f, encoding='utf-8'))
        before = json.dumps(j, sort_keys=True, ensure_ascii=False)
        j = clean_file(json.loads(before))
        if json.dumps(j, sort_keys=True, ensure_ascii=False) != before:
            changed += 1
            if not dry: json.dump(j, open(f, 'w', encoding='utf-8'), indent=2, ensure_ascii=False); open(f, 'a').write('\n')
    print(('would change' if dry else 'changed'), changed, 'pages;', counts)


if __name__ == '__main__':
    main()
