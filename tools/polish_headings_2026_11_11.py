"""D-230: the same h3 "Where it sits and what to know here" sat under every property-type section on 80+ guides.
Name it for the section's property type instead. Also hides 3 headings left with nothing under them."""
import json, glob, re, sys
NAMES = [('Condo buildings', 'Where the condos are and what to know'),
         ('Townhome complexes', 'Where the townhomes are and what to know'),
         ('Lots and land', 'Where lots come up and what to know'),
         ('Acreage and rural land', 'Where the acreages are and what to know'),
         ('Duplexes', 'Where duplexes come up and what to know'),
         ('Mobile and manufactured', 'Mobile home parks and what to know')]
OLD = 'Where it sits and what to know here'
changed = 0
for p in sorted(glob.glob('src/data/local/*.json')):
    raw = open(p).read(); d = json.loads(raw); IND = len(re.match(r'\{\n( *)', raw).group(1)) if raw.startswith('{\n') else None; n = [0]
    def walk(o):
        if isinstance(o, list):
            h2 = ''
            for b in o:
                if isinstance(b, dict) and b.get('t') == 'h' and b.get('level') == 2: h2 = b.get('text', '')
                if isinstance(b, dict) and b.get('text') == OLD:
                    for k, v in NAMES:
                        if h2.startswith(k): b['text'] = v; n[0] += 1; break
                walk(b)
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
    walk(d)
    if n[0]:
        changed += 1
        open(p, 'w').write(json.dumps(d, ensure_ascii=False, indent=IND) + ('\n' if raw.endswith('\n') else ''))
print('files', changed)

# Pass 2: the same h3 ("Good to know about Mission", "Streets, schools and getting around Mission") under each
# property-type h2 on one page. Where a text repeats on a page, name the property type in it.
import collections
TYPES = [('Condo buildings', 'condos'), ('Townhome complexes', 'townhomes'), ('Lots and land', 'lots'),
         ('Acreage and rural land', 'acreages'), ('Duplexes', 'duplexes'), ('Mobile and manufactured', 'mobile homes')]
def typed(text, typ):
    m = re.match(r'^Streets, schools and getting around (.+)$', text)
    if m: return f'Streets, schools and transit near {m.group(1)} {typ}'
    m = re.match(r'^Good to know about (.+)$', text)
    if m: return f'Good to know about {m.group(1)} {typ}'
    return None
changed2 = 0
for p in sorted(glob.glob('src/data/local/*.json')):
    raw = open(p).read(); d = json.loads(raw); IND = len(re.match(r'\{\n( *)', raw).group(1)) if raw.startswith('{\n') else None
    bl = d.get('blocks')
    if not isinstance(bl, list): continue
    cnt = collections.Counter(b.get('text') for b in bl if isinstance(b, dict) and b.get('t') == 'h' and b.get('level') == 3)
    typ, n = None, 0
    for b in bl:
        if not isinstance(b, dict) or b.get('t') != 'h': continue
        if b.get('level') == 2: typ = next((v for k, v in TYPES if b.get('text', '').startswith(k)), None)
        elif b.get('level') == 3 and typ and cnt[b.get('text')] > 1:
            t = typed(b['text'], typ)
            if t: b['text'] = t; n += 1
    if n:
        changed2 += 1
        open(p, 'w').write(json.dumps(d, ensure_ascii=False, indent=IND) + ('\n' if raw.endswith('\n') else ''))
print('pass 2 files', changed2)
