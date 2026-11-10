"""Tidy the archive blocks of every neighbourhood guide (D-202, the guide-heading clean-up from the Nov 9 review).

On a guide, the archive page and the newer local layer both carried some sections, so readers saw:
- three seller boxes: "Own in X?" + "Contact Form" (or "Contact Me") + "Free X property check", besides the newer
  "What is your X home worth?" form. The archive ones are removed; the home-value form stays.
- a second, old title inside the page ("Fort Langley Homes for Sale | Historic Fort Langley Real Estate"): heading removed, text kept.
- two question sections ("Common questions" and "X questions"): handled at render time by GenericPage, which adds the local
  questions to the archive's own section (each question once) so the archive answers keep their source links.
- "Schools in X" twice: the archive list goes when the local schools table (kept up to date by its builder) is there.
- the one-word labels that sat above those sections ("Selling", "FAQ").
Idempotent. python3 -I tools/tidy_guides.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SELLER = re.compile(r'^(Own in .+\?|Contact Form|Contact Me|Free .+ property check)$')
EYEBROW = {'Selling', 'FAQ', 'Sell', 'Contact'}
stats = collections.Counter()


def ptext(b):
    if b.get('t') != 'p': return ''
    return (b.get('text') or ' '.join(p.get('t', '') for p in b.get('parts', []))).strip()


def qkey(q): return re.sub(r'[^a-z0-9 ]', '', q.lower()).strip()


def sh(s):
    w = re.findall(r'[a-z0-9]+', s.lower()); return {' '.join(w[i:i + 4]) for i in range(max(1, len(w) - 3))}


def tidy(slug):
    pp = os.path.join(ROOT, 'src/data/pages', slug + '.json'); lp = os.path.join(ROOT, 'src/data/local', slug + '.json')
    if not os.path.exists(pp): return
    page = json.load(open(pp, encoding='utf-8')); local = json.load(open(lp, encoding='utf-8')) if os.path.exists(lp) else None
    bl = page['blocks']; out = []; i = 0
    has_local_schools = bool(local and any(b.get('gen') == 'schools' and b.get('t') == 'h' for b in local['blocks']))
    faq_new = []
    first_h1 = next((k for k, b in enumerate(bl) if b.get('t') == 'h' and b.get('level') == 1), None)
    while i < len(bl):
        b = bl[i]
        nxt = bl[i + 1] if i + 1 < len(bl) else {}
        # one-word label right above a section that goes
        if ptext(b) in EYEBROW and nxt.get('t') == 'h' and (SELLER.match(nxt.get('text', '')) or re.search(r'questions$', nxt.get('text', ''), re.I)) and local:
            stats['label'] += 1; i += 1; continue
        if b.get('t') == 'h' and b.get('level') == 1 and i != first_h1 and ' | ' in b.get('text', ''):
            stats['old title heading'] += 1; i += 1; continue
        if b.get('t') == 'h' and b.get('level') == 2:
            t = b.get('text', '')
            j = i + 1
            while j < len(bl) and not (bl[j].get('t') == 'h' and bl[j].get('level') in (1, 2)): j += 1
            body = bl[i + 1:j]
            if SELLER.match(t) and local:
                stats['seller box'] += 1; i = j; continue
            if re.match(r'^Schools in ', t) and has_local_schools:
                stats['duplicate schools'] += 1; i = j; continue
            if False and re.search(r'\bquestions$', t, re.I):   # questions now join at render time (GenericPage), links kept
                k = 0; pairs = []
                while k < len(body):
                    q = ptext(body[k])
                    if q.endswith('?') and k + 1 < len(body) and ptext(body[k + 1]) and not ptext(body[k + 1]).endswith('?'):
                        a = [ptext(body[k + 1])]; k += 2
                        while k < len(body) and ptext(body[k]) and not ptext(body[k]).endswith('?'): a.append(ptext(body[k])); k += 1
                        pairs.append((q, ' '.join(a)))
                    else: k += 1
                if pairs and len(pairs) * 2 >= len([x for x in body if ptext(x)]) - 1:   # the section is only Q and A
                    faq_new += pairs; stats['question section merged'] += 1; i = j; continue
        out.append(b); i += 1
    if faq_new and local is not None:
        have = local.setdefault('faq', [])
        keys = [sh(f['q']) for f in have]
        for q, a in faq_new:
            S = sh(q)
            if any(len(S & k) / max(1, len(S)) >= 0.6 for k in keys): stats['question already there'] += 1; continue
            have.append({'q': q, 'a': a}); keys.append(S); stats['question moved'] += 1
        raw = open(lp, encoding='utf-8').read()
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(local, ensure_ascii=False, indent=ind) if ind else json.dumps(local, ensure_ascii=False, separators=(',', ':'))
        open(lp, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
    if out != bl:
        page['blocks'] = out
        raw = open(pp, encoding='utf-8').read()                # keep the file's own format
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(page, ensure_ascii=False, indent=ind) if ind else json.dumps(page, ensure_ascii=False, separators=(',', ':'))
        open(pp, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))


for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/pages/*-guide.json'))):
    tidy(os.path.basename(f)[:-5])
print(dict(stats))
