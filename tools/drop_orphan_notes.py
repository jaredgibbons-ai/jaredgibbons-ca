"""Drop the one-line "Good to know" notes that lost their explanation (D-202, from the trim review).

Each "Good to know" item was written as a headline plus an explanation. The D-194 research-wording passes removed explanations that
were research notes, which left headlines standing alone on public pages: "The two Proper pages are mostly the same page.",
"The bus diagram does not prove the bus.", "The 156 count is the rare page figure that clears the bar." A reader cannot use these.
Removed: a Good-to-know item that is one sentence of 18 words or fewer with no link and no figure, and any one-line item that talks
about pages, sources, counts or searches (research talk). Items with a link (the "BC condo buying rules" pointers) always stay.
Idempotent. python3 -I tools/drop_orphan_notes.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
META = re.compile(r"\b(page|pages|guide|feed|feeds|sources?|cite|citable|citation|claim|count|counts|figure|label|listing text|locator|"
                  r"sample|on the record|on paper|programs?|settled|unsettled|SnapStats|statistics?|quoting|market data|median|search|exist only|"
                  r"two addresses|page names|framing|extra word|diagram|plan boundary|public sources|automated|misfile|disagree|clears the bar|backs|"
                  r"loosely|header|basis|chain|artifact|mislabelled|mapping|no settled|wear two|does not prove|needs a fresh|directory|filing|superseded|"
                  r"read two ways|banned|uncited|double count|zero row|zero is a statistic|a gap)\b", re.I)
stats = collections.Counter()


def short(t): return len(re.findall(r'[.!?](?:\s|$)', t)) <= 1 and len(t.split()) <= 18


for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json'))):
    raw = open(f, encoding='utf-8').read()
    if 'Good to know' not in raw: continue
    d = json.loads(raw); cur = None; changed = False
    for b in d['blocks']:
        if b.get('t') == 'h': cur = b.get('text', '') if b.get('level') == 3 else None; continue
        if not (cur and cur.startswith('Good to know') and b.get('t') == 'list'): continue
        keep = []
        for it in b['items']:
            parts = [p for p in it if isinstance(p, dict)]
            t = ' '.join(p.get('t', '') for p in parts).strip()
            if any(p.get('h') for p in parts) or not short(t): keep.append(it); continue
            if META.search(t) or not re.search(r'\d', t): stats['dropped'] += 1; changed = True; continue
            keep.append(it)
        b['items'] = keep
    if changed:
        d['blocks'] = [b for b in d['blocks'] if not (b.get('t') == 'list' and not b.get('items'))]
        # a Good-to-know heading left with nothing under it goes too
        out = []
        for i, b in enumerate(d['blocks']):
            if b.get('t') == 'h' and b.get('level') == 3 and b.get('text', '').startswith('Good to know'):
                nxt = d['blocks'][i + 1] if i + 1 < len(d['blocks']) else {}
                if nxt.get('t') == 'h' or not nxt: stats['empty heading'] += 1; continue
            out.append(b)
        d['blocks'] = out
        ind = 2 if raw.startswith('{\n  "') else (1 if raw.startswith('{\n "') else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
print(dict(stats))
