"""Second review pass, 2026-11-08: removes research-process wording from the visitor-facing local layer.
Idempotent; edits only string values (no trimming of other text).  python3 -I tools/review_fixes_2026_11_08b.py [--dry]
Rules: (1) drop 'check current' tags; (2) drop sentences or ';' clauses that talk about the old page, 'site copy', 'source pass' etc.;
(3) drop bare 'Label: Not verified.' stubs and '(label: not verified)' parentheticals; items, blocks and FAQ pairs left empty are removed."""
import re, glob, json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DRY = '--dry' in sys.argv
META = re.compile(r"guide page|\bthe page(?:'|’)s\b|\bthe (?:current|existing|old|live|archived) page\b|site copy|[Ll]ive-page|source pass|\b(?:this|that|in this|in that) pass\b|opened pass|\bpass\b[^.;]{0,25}(?:not verified|not opened|could not|did not surface)|research pass|area research (?:recorded|confirmed|found)|Read gap|fetch[- ]service|working scope|\bper the page\b|the page itself|page names it|a question for Jared|existing sections|(?:the|a) page(?:'|’)s (?:stated|claimed|own)|stale twin")
CHECK = [
    (re.compile(r"; catchment not confirmed"), "; confirm the catchment with the district"),
    (re.compile(r"\(catchment not confirmed\)"), "(confirm the catchment with the district)"),
    (re.compile(r"\(check current[;:]\s*([^)]+)\)"), r"(\1)"),
    (re.compile(r"\(check current\s*[—-]\s*([^)]+)\)"), r"(\1)"),
    (re.compile(r"\(check current schedule\)"), "(check the current schedule)"),
    (re.compile(r"\s*\((?:status is[^)]*?\s)?check current(?: with [^)]*)?\)"), ''),
    (re.compile(r"\s*\(check current\s*[—-]\s*(\d{4})\)"), ''),
    (re.compile(r"\s*[—-]\s*check current(?: with the [A-Z][A-Za-z ]+)?(?=[.;,)])"), ''),
    (re.compile(r",\s*check current(?=[.;])"), ''),
    (re.compile(r"\s*[—-]\s*check current(?= \(as of)"), ''),
    (re.compile(r"check current with the "), 'confirm with the '),
    (re.compile(r"\s*[—-]\s*check current\b"), ''),
]
ABBR = {'No', 'Nos', 'St', 'Ave', 'Rd', 'Dr', 'Mt', 'Hwy', 'Blvd', 'vs', 'Ltd', 'Inc', 'Co', 'Mr', 'Mrs', 'Ms', 'approx', 'Sec', 'ss', 's', 'e.g', 'i.e', 'Ste', 'Cres', 'Pl'}
STUB_PAREN = re.compile(r"\s*\((?:[^()]*?:\s*)?[Nn]ot verified[^()]*\)")
STUB_SENT = re.compile(r"^[^.;:]{3,150}:\s*[Nn]ot (?:verified|confirmed)(?: (?:at|for|as|by|on|in|from|per|here|beyond|pass|parcel)[^.;:—]{0,70}| \((?:none confirmed|community level only|SnapStats[^)]*)\))?(?: — (?:no source[^.;:]{0,60}))?[.]?$")
STUB_ACTION = re.compile(r"^([^.;:]{3,150}):\s*[Nn]ot (?:verified|confirmed)[^.;:—]{0,70} — ((?:confirm|check|run|ask)[^.;]{0,90}[.]?)$")

def split_sent(t):
    out, start = [], 0
    for m in re.finditer(r'(?<=[.!?])(\s+)(?=[A-Z“"(\[])', t):
        w = re.search(r'(\S+)$', t[start:m.start()])
        last = w.group(1).rstrip('.!?') if w else ''
        if last in ABBR or re.fullmatch(r'[A-Z]', last):
            continue
        out.append(t[start:m.end()]); start = m.end()
    out.append(t[start:]); return out

def clean_sentence(s):
    lead = re.match(r'\s*', s).group(0); body = s[len(lead):]
    trail = re.search(r'\s*$', body).group(0); body = body[:len(body)-len(trail)]
    if not body: return s
    if STUB_SENT.match(body): return ''
    ma = STUB_ACTION.match(body)
    if ma and not META.search(body): return lead + ma.group(1) + ': ' + ma.group(2) + trail
    if META.search(body):
        clauses = body.split('; ')
        keep = [c for c in clauses if not META.search(c)]
        if not keep: return ''
        if len(keep) == len(clauses): return ''
        body2 = '; '.join(keep)
        if keep[0] is not clauses[0]: body2 = body2[0].upper() + body2[1:]
        if body.endswith(('.', '!', '?')) and not body2.endswith(('.', '!', '?')): body2 += body[-1]
        return lead + body2 + trail
    return s

def clean_text(t):
    o = t
    for rx, rep in CHECK: t = rx.sub(rep, t)
    t = STUB_PAREN.sub('', t)
    parts = split_sent(t)
    new = [clean_sentence(p) for p in parts]
    if new != parts:
        t = ''.join(new)
        t = re.sub(r'\s+([.,;:])', r'\1', t)
        t = re.sub(r'([.;:])\s*([.;:])', r'\1', t) if False else t
    if o and not o[-1].isspace(): t = t.rstrip()
    if o and not o[0].isspace(): t = t.lstrip()
    return t

REMOVE = object()
changed = [0]
def piece(o):
    new = clean_text(o['t'])
    if new != o['t']:
        changed[0] += 1
        o['t'] = new
    return o

def walk_blocks(blocks):
    out = []
    for b in blocks:
        if not isinstance(b, dict): out.append(b); continue
        if b.get('t') in ('p', 'notice') and isinstance(b.get('text'), str):
            n = clean_text(b['text'])
            if n != b['text']: changed[0] += 1; b['text'] = n
            if not n.strip(): continue
        if b.get('t') == 'list' and isinstance(b.get('items'), list):
            items = []
            for it in b['items']:
                if isinstance(it, list):
                    for p in it:
                        if isinstance(p, dict) and isinstance(p.get('t'), str): piece(p)
                    if not ''.join(p.get('t', '') for p in it if isinstance(p, dict)).strip(' .;:,—-'): continue
                items.append(it)
            if not items: continue
            b['items'] = items
        out.append(b)
    return out

FORMATS = [dict(indent=2, ensure_ascii=False), dict(indent=1, ensure_ascii=False), dict(separators=(',', ':'), ensure_ascii=False), dict(indent=2, ensure_ascii=True)]
def dump_like(raw, d):
    base = json.loads(raw)
    for kw in FORMATS:
        for tail in ('\n', ''):
            if json.dumps(base, **kw) + tail == raw: return json.dumps(d, **kw) + tail
    return json.dumps(d, indent=2, ensure_ascii=False) + '\n'

def fix_file(f):
    raw = open(f, encoding='utf-8').read(); d = json.loads(raw); before = json.dumps(d, ensure_ascii=False)
    if isinstance(d.get('blocks'), list): d['blocks'] = walk_blocks(d['blocks'])
    if isinstance(d.get('faq'), list):
        faq = []
        for q in d['faq']:
            for k in ('q', 'a'):
                if isinstance(q.get(k), str):
                    n = clean_text(q[k])
                    if n != q[k]: changed[0] += 1; q[k] = n
            if q.get('q', '').strip() and q.get('a', '').strip(' .'): faq.append(q)
        d['faq'] = faq
    after = json.dumps(d, ensure_ascii=False)
    if after != before and not DRY:
        open(f, 'w', encoding='utf-8').write(dump_like(raw, d))
    return after != before

n = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
    if fix_file(f): n += 1
print('local files changed:', n, '| strings changed:', changed[0], '(dry)' if DRY else '')
