"""Remove research-note wording from published page copy (D-194).

The notes builders (uniqueness, nearby buildings, 55+, types, acreages, Muse FAQs) carried the researchers' own voice onto the pages:
"not verified in the sources read", "in any pass", "What is not confirmed about X", "Fresh-verified Nov 2", "Counted: 1.",
lines that lost their label and start with ": ". A reader cannot act on any of that, so it comes off. Pages keep only what the
sources state.

What it does, on src/data/local/*.json and src/data/pages/*.json (blocks and FAQ):
  - drops a heading that is about what is not confirmed ("What is not confirmed about X", "Not confirmed", "Not verified")
    and the content under it, up to the next heading of the same or a higher level;
  - drops any sentence written in research voice (RV below), then any list item, paragraph or FAQ answer left empty or too short;
  - a list item that lost its label (starts with ": ") loses the colon, and a leading dash after it;
  - table cells that only say "Not confirmed" / "Not verified" become an em dash;
  - drops a heading left with nothing under it.
Idempotent. Writes each file back in its own style (indent, trailing newline).
python3 -I tools/clean_research_voice.py [--dry]"""
import glob, json, os, re, sys, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
RV = re.compile(r"""
  \bnot\s+(?:yet\s+|been\s+|independently\s+|separately\s+)?(?:confirmed|verified)\b
 |\bun(?:confirmed|verified)\b
 |\bsources?\s+(?:read|checked|opened|reviewed|consulted)\b
 |\b(?:in|from)\s+(?:the|any)\s+sources?\b
 |\bno\s+(?:official\s+)?source\s+(?:checked|read|opened|found|states?)\b
 |\b(?:in|from)\s+(?:any|this|that|the|a|each|every)\s+(?:research\s+)?pass\b|\b(?:55-plus|55\+|guide|research|types?|acreage)\s+pass\b
 |\bguide\s+research\b|\bthe\s+research\b|\bresearch\s+(?:team|notes?|file)\b
 |\bfresh-verified\b|\bre-verified\b|\bCounted:\s*\d|\bin-entry\b|\bflagged\s+here\b
 |\bper-address\s+checks?\b|\bthe\s+checking\b|\bopen\s+items\b|\bentries\s+in\s+below\b|\bunresolved\s+on\b
 |\bthe\s+(?:guide|notes?|brief|directory\s+entry)\s+(?:frames|says|states|lists|gives|records|counts|flags)\b
 |\b(?:could|can)\s*not\s+(?:be\s+)?(?:confirm|verif|establish|locate|match)\w*
 |\bwas\s+not\s+(?:found|returned|located|identified)\b|\bwere\s+not\s+(?:found|returned|located|identified)\b
 |\bnot\s+(?:found|identified)\s+in\b|\bnone\s+(?:was|were)\s+(?:found|identified)\b
 |\bas\s+a\s+check\b|\bspot-check|\bcross-check
 |\bconfirmed\s+(?:on|in|from)\s+(?:a|an|the|any)\s+(?:\w+\s+)?(?:source|page|record)s?\b|\bsample\s+address\b|\breturned\s+no\b
 |\bor\s+verified\b|\bno\s+phase\s+selling\b|\bnever\s+mixed\s+with\b|\bsold\s+on\s+this\s+page\b|\bwording\s+in\s+this\s+section\b|\bwas\s+changed\b
 |\b(?:is|are)\s+(?:documented|named)\s+(?:here|in\s+this)\b|\bdocumented\s+here\s+by\s+name\b|\bsite\s+copy\b|\bguide-only\b
 |\bon\s+the\s+sources\s+here\b|\bempty\s+set\b|\b(?:our\s+own\s+|earlier\s+)?area\s+research\b|\bthese\s+notes\b|\bwere\s+researched\b|\bdirectory\s+source\b
 |\bmy\s+tools\b|\bI\s+have\s+not\s+stated\b|\bpage's\s+feed\b|\bcitable\s+source\b|\bdirectory-stated\b
 |(?<!your\s)(?<!do\s)\bresearch(?:ed)?\b(?!\s+(?:park|centre|center|institute|university|facility|campus|and\s+innovation))
 |\bruling\s+note\b|\bnever\s+(?:merged|as\s+inventory)\b|\bdocumented\s+as\s+such\b|\bthe\s+two\s+are\s+never\b
 |\bread\s+by\s+me\b|\blocator\s+sample\b|\(run\s+20\d\d-\d\d-\d\d\)|\bolder\s+brief\b
 |\bin\s+the\s+source\b|\bper\s+the\s+(?:\w+\s+)?(?:source|data\s+sheet)\b|\bdata\s+sheet\b|\bthe\s+sources\s+used\b
 |\b(?:this|the|its|our|that|live)\s+(?:live\s+)?feed\b|\bfeed's\b|\b[a-z]+(?:-[a-z]+)+\s+feed\b|\bfeed\s+cards?\b|\bpage\s+feed\b
 |\bthe\s+page\s+(?:is\s+headed|title|says)\b|\bthis\s+page's\b|\bpage\s+title\b|\beditorial\s+(?:copy|heading)\b|\bwhat\s+the\s+page\s+is\b|\bcontradicts\s+(?:itself|its\s+own)\b
 |\bflagged\s+(?:in|here|at|above|below)\b|\bname\s+trap\b|\bstale\s+citations?\b|\bfor\s+the\s+record\b|\brules-gaps\b|\bstated\s+expressly\b|\bnever\s+borrow\b|\bconflated\b
 |\bnone\s+(?:is\s+|are\s+)?verified\b|\bno\b[^.;]{0,60}?\b(?:is|are|was|were)\s+verified\b|\bverified\s+(?:below|above|here)\b|\bhas\s+none\s+verified\b|\bno\s+figure\s+of\s+any\s+kind\b
""", re.I | re.X)
NC_HEAD = re.compile(r'^\s*(?:what\s+is\s+)?(?:not|un)\s*(?:confirmed|verified)\b|^\s*what\s+is\s+not\s+confirmed\b', re.I)
NC_CELL = re.compile(r'^\s*(?:not|un)\s*(?:confirmed|verified)\.?\s*(?:\(.*\))?\s*$', re.I)
STATED_CELL = re.compile(r'^\s*not\s+stated\s+in\s+(?:the\s+)?sources?\s*\.?\s*$', re.I)


def clean_heading(s):
    """Building and section headings: drop research asides such as '(building name not confirmed)' or '; strata vs fee simple: Not confirmed'."""
    o = s
    s = re.sub(r'\s*\([^()]*\)', lambda m: '' if RV.search(m.group(0)) else m.group(0), s)
    parts = re.split(r'(\s+[—–]\s+|;\s+|\.\s+|:\s+)', s); keep = ''
    for i in range(0, len(parts), 2):
        if RV.search(parts[i]): break
        nxt_rv = i + 2 < len(parts) and RV.search(parts[i + 2])
        if nxt_rv and i + 1 < len(parts) and parts[i + 1].strip() == ':': break
        keep += parts[i] + (parts[i + 1] if i + 1 < len(parts) and not nxt_rv else '')
    keep = re.sub(r'[\s—–;:.,]+$', '', keep).strip()
    if keep != o: stats['heading trimmed'] += 1
    return keep
ABBR = ''.join(rf'(?<!\b{a}\.)' for a in ('St', 'No', 'Ave', 'Rd', 'Dr', 'Mt', 'Ft', 'vs', 'g', 'e', 'Inc', 'Ltd', 'approx', 'Sec', 's', 'ss', 'Hwy', 'Blvd', 'Cres', 'Pl', 'Jr', 'Sr'))
SPLIT = re.compile(r'(?<=[.!?])' + ABBR + r'\s+(?=[A-Z"“(\'‘0-9$])')
stats = collections.Counter(); samples = collections.defaultdict(list)


VERIFIED = re.compile(r'\b(the|a|an|its|two|three|four|one|only|both)\s+verified\s+', re.I)


def clean_text(s, where, first=True):
    if not isinstance(s, str) or not s.strip(): return s
    o = s
    s = VERIFIED.sub(lambda m: m.group(1) + ' ', s)
    s = re.sub(r'\b(this|that|the same) ground\b', lambda m: m.group(1) + ' area', s)
    if first and re.match(r'^\s*:\s', s):
        s = re.sub(r'^\s*:\s*(?:[—–-]\s*)?', '', s); stats['label colon'] += 1
        if s: s = s[0].upper() + s[1:]
    if re.match(r'^Sources?:\s', s) and RV.search(s):
        head = re.match(r'^(Sources?:\s*)', s); body = s[head.end():]
        keep = [x for x in re.split(r';\s+', body.rstrip('.')) if not RV.search(x)]
        stats['sources line'] += 1
        return (head.group(1) + '; '.join(keep) + '.') if keep else ''
    out = []
    for sen in SPLIT.split(s):
        if RV.search(sen):
            sen2 = re.sub(r'\s*\([^()]*\)', lambda m: '' if RV.search(m.group(0)) else m.group(0), sen)
            if not RV.search(sen2): stats['paren dropped'] += 1; out.append(sen2); continue
            keep = lead_clause(sen)
            stats['sentence trimmed' if keep else 'sentence'] += 1
            if len(samples['sentence']) < 400: samples['sentence'].append((where, sen, keep))
            if keep: out.append(keep)
            continue
        out.append(sen)
    s = ' '.join(out).strip()
    s = re.sub(r'\s+', ' ', s)
    if first: s = re.sub(r'^[—–:;,\-\s]+', '', s)
    if first and s and s != o and s[0].islower(): s = s[0].upper() + s[1:]
    if not first and s != o and s and not s.startswith((' ', ':', ',', '.', ';', ')')): s = ' ' + s
    return s


CLAUSE = re.compile(r'(;\s+|\s+[—–]\s+|,\s+but\s+|,\s+while\s+|,\s+so\s+|,\s+although\s+)')


def lead_clause(sen):
    """The part of a sentence before its first research-voice clause, when that part says something on its own."""
    bits = CLAUSE.split(sen); keep = ''
    for i in range(0, len(bits), 2):
        if RV.search(bits[i]): break
        keep += bits[i] + (bits[i + 1] if i + 1 < len(bits) else '')
    keep = re.sub(r'(?:;|\s[—–]|,\s*but|,\s*while|,\s*so|,\s*although)\s*$', '', keep.strip()).strip()
    keep = keep.rstrip(':,; ')
    if len(keep) < 45 or keep == sen.strip() or re.search(r':\s*\S{0,3}$', keep): return ''
    if keep.count('(') > keep.count(')'): return ''
    return keep if keep[-1] in '.!?' else keep + '.'


def short(s): return len(re.sub(r'[^A-Za-z]', '', s or '')) < 12


def clean_parts(parts, where):
    out = []; changed = False
    for i, p in enumerate(parts):
        if isinstance(p, dict) and 'h' not in p and isinstance(p.get('t'), str):
            t = clean_text(p['t'], where, first=(i == 0))
            if t != p['t']:
                changed = True
                if short(t): continue
                p = {**p, 't': t}
        out.append(p)
    if changed and not any(isinstance(p, dict) and ('h' in p or not short(p.get('t'))) for p in out): return []
    return out


def clean_blocks(blocks, where):
    out = []; skip_level = None
    for b in blocks:
        if not isinstance(b, dict): out.append(b); continue
        t = b.get('t')
        if t == 'h':
            lvl = b.get('level', 2)
            if skip_level is not None and lvl <= skip_level: skip_level = None
            if skip_level is not None: stats['under nc heading'] += 1; continue
            if NC_HEAD.search(b.get('text', '') or ''):
                skip_level = lvl; stats['nc heading'] += 1; continue
            if RV.search(b.get('text', '') or ''):
                x = clean_heading(b['text'])
                if len(x) < 4: stats['nc heading'] += 1; skip_level = lvl; continue
                b = {**b, 'text': x}
            out.append(b); continue
        if skip_level is not None: stats['under nc heading'] += 1; continue
        if t == 'p':
            if isinstance(b.get('text'), str) and 'h' not in b:
                x = clean_text(b['text'], where)
                if x != b['text'] and short(x): stats['p dropped'] += 1; continue
                b = {**b, 'text': x}
            elif isinstance(b.get('parts'), list):
                ps = clean_parts(b['parts'], where)
                if not ps: stats['p dropped'] += 1; continue
                b = {**b, 'parts': ps}
        elif t == 'list' and isinstance(b.get('items'), list):
            items = []
            for it in b['items']:
                if isinstance(it, list):
                    ps = clean_parts(it, where)
                    if ps: items.append(ps)
                    else: stats['item dropped'] += 1
                else: items.append(it)
            if not items: stats['list dropped'] += 1; continue
            b = {**b, 'items': items}
        if t == 'table' and isinstance(b.get('source'), str) and RV.search(b['source']):
            src = b['source']; head = re.match(r'^(Sources?:\s*)', src); body = src[head.end():] if head else src
            keep = [x for x in re.split(r';\s+', body.rstrip('.')) if not RV.search(x)]
            stats['table source'] += 1
            b = {**b, 'source': ((head.group(1) if head else '') + '; '.join(keep) + '.') if keep else ''}
            if not b['source']: b = {k: v for k, v in b.items() if k != 'source'}
        if t == 'table' and isinstance(b.get('rows'), list):
            rows = []
            for r in b['rows']:
                nr = []
                for c in r:
                    if isinstance(c, str) and NC_CELL.match(c): nr.append('—'); stats['cell'] += 1
                    elif isinstance(c, str) and STATED_CELL.match(c): nr.append('Not stated'); stats['cell'] += 1
                    elif isinstance(c, str) and RV.search(c):
                        x = clean_text(c, where); nr.append(x if x.strip() else '—')
                    else: nr.append(c)
                rows.append(nr)
            b = {**b, 'rows': rows}
        out.append(b)
    # drop headings left with no content before the next heading of the same or higher level
    res = []
    for i, b in enumerate(out):
        if isinstance(b, dict) and b.get('t') == 'h':
            lvl = b.get('level', 2); j = i + 1; has = False
            while j < len(out):
                n = out[j]
                if isinstance(n, dict) and n.get('t') == 'h':
                    if n.get('level', 2) <= lvl: break
                    has = True; break
                has = True; break
            if not has and lvl >= 2: stats['empty heading'] += 1; continue
        res.append(b)
    return res


def clean_faq(faq, where):
    out = []
    for f in faq:
        if not isinstance(f, dict): out.append(f); continue
        a = f.get('a')
        if isinstance(a, str):
            x = clean_text(a, where)
            if len(x) < 40: stats['faq dropped'] += 1; continue
            f = {**f, 'a': x}
        q = f.get('q')
        if isinstance(q, str) and RV.search(q): stats['faq dropped'] += 1; continue
        out.append(f)
    return out


def dump(d, t):
    lines = t.split('\n')
    if len(lines) > 2:
        m = re.match(r'^( +)\S', lines[1]); s = json.dumps(d, indent=len(m.group(1)) if m else 2, ensure_ascii=False)
    else:
        s = json.dumps(d, separators=(',', ':'), ensure_ascii=False)
    return s + ('\n' if t.endswith('\n') else '')


def main():
    dry = '--dry' in sys.argv; changed = 0
    for f in sorted(glob.glob(f'{ROOT}/src/data/local/*.json') + glob.glob(f'{ROOT}/src/data/pages/*.json')):
        t = open(f, encoding='utf-8').read(); d = json.loads(t)
        if not isinstance(d, dict): continue
        where = os.path.basename(f)
        if isinstance(d.get('blocks'), list): d['blocks'] = clean_blocks(d['blocks'], where)
        if isinstance(d.get('faq'), list): d['faq'] = clean_faq(d['faq'], where)
        s = dump(d, t)
        if s != t:
            changed += 1
            if not dry: open(f, 'w', encoding='utf-8').write(s)
    print(f'files changed: {changed}', dict(stats))
    if dry:
        json.dump(samples, open('/tmp/rv_samples.json', 'w'), ensure_ascii=False, indent=0)


if __name__ == '__main__': main()
