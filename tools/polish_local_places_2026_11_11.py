"""D-230: section headings on local layers carried the page title as the place name
("Good to know about Willoughby Guide", "Townhome complexes in Yaletown Condos for Sale Townhomes").
Use the plain place name. Also removes research-queue sections ("Queue", "at the rule level only")."""
import json, glob, re
CLEAN = {
 'Anmore Homes for Sale':'Anmore','Beach Grove Guide':'Beach Grove','Bridal Falls Guide':'Bridal Falls',
 'Broiler Farms for Sale BC':'BC broiler farms','Egg Farms for Sale BC':'BC egg farms','Poultry Farms for Sale BC':'BC poultry farms','Turkey Farms for Sale BC':'BC turkey farms',
 'Brookswood Real Estate Development Guide':'Brookswood','Campbell Valley Acreages & Farms for Sale':'Campbell Valley','Campbell Valley Townhomes':'Campbell Valley',
 'Chilliwack Downtown Townhomes':'Downtown Chilliwack','Chilliwack Land Use Plans':'Chilliwack','Chilliwack Land Use Plans Townhomes':'Chilliwack',
 'City of Maple Ridge Real Estate & Homes':'Maple Ridge','City of Maple Ridge Townhomes':'Maple Ridge','City of Maple Ridge':'Maple Ridge',
 'City of Mission Land Use Plans':'Mission','City of Mission Townhomes':'Mission','Cloverdale Neighbourhood Guides':'Cloverdale',
 'Dewdney Deroche Mission Guide':'Dewdney and Deroche','Downtown Vancouver Condos for Sale':'Downtown Vancouver','Downtown Vancouver Condos for Sale Townhomes':'Downtown Vancouver',
 'Durieu Mission Guide':'Durieu','Durieu Townhomes':'Durieu','Elgin Chantrell Guide':'Elgin Chantrell','Elgin Chantrell Townhomes':'Elgin Chantrell',
 'Fleetwood Tynehead Townhomes':'Fleetwood Tynehead','Fox & Aikins North Townhomes':'Fox & Aikins North','Hatzic Townhomes':'Hatzic','Hazelmere Townhomes':'Hazelmere',
 'Langley Acreages for Sale':'Langley','Langley City Townhomes':'Langley City','Langley Condos for Sale':'Langley','Langley Condos for Sale Townhomes':'Langley',
 'Langley Houses for Sale':'Langley','Langley Houses with Coach Houses':'Langley','Langley Houses with Coach Houses for Sale':'Langley','Langley Poultry Farms for Sale':'Langley',
 'Mission Homes for Sale':'Mission','Mission West Townhomes':'Mission West','North Maple Ridge Guide':'North Maple Ridge','North Vancouver Homes for Sale':'North Vancouver',
 'Northwest Maple Ridge Guide':'Northwest Maple Ridge','Otter District Townhomes':'Otter District','Pacific Douglas Townhomes':'Pacific Douglas','Popkum Guide':'Popkum',
 'Serpentine Townhomes':'Serpentine','Silver Valley Townhomes':'Silver Valley','South Surrey Duplexes with Suites':'South Surrey','South Surrey Duplexes with Suites for Sale':'South Surrey',
 'South Surrey Luxury Homes':'South Surrey','South Surrey New Construction Presales Townhomes':'South Surrey','Steelhead Mission Guide':'Steelhead',
 'Thornhill Maple Ridge Guide':'Thornhill','West Central Maple Ridge Guide':'West Central Maple Ridge','West Vancouver Homes for Sale':'West Vancouver',
 'Willoughby Guide':'Willoughby','Yaletown Condos for Sale Townhomes':'Yaletown','Yaletown Condos for Sale':'Yaletown',
}
KEYS = sorted(CLEAN, key=len, reverse=True)
PREP = re.compile(r'(\b(?:in|about|on|around|across)\s+)(' + '|'.join(re.escape(k) for k in KEYS) + r')(?=$|[\s.,;:)’\'])')
DROP_HEAD = re.compile(r'^(Queue|.*at the rule level only)$')
files = 0
for p in sorted(glob.glob('src/data/local/*.json')):
    raw = open(p).read(); d = json.loads(raw); IND = len(re.match(r'\{\n( *)', raw).group(1)) if raw.startswith('{\n') else None; before = json.dumps(d)
    def fix(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('text', 't') and isinstance(v, str): o[k] = PREP.sub(lambda m: m.group(1) + CLEAN[m.group(2)], v)
                else: fix(v)
        elif isinstance(o, list):
            for v in o: fix(v)
    fix(d)
    def drop(lst):
        out, skip = [], False
        for b in lst:
            if isinstance(b, dict) and b.get('t') == 'h' and DROP_HEAD.match(b.get('text', '')): skip = True; continue
            if skip and isinstance(b, dict) and b.get('t') in ('list', 'p'): continue
            skip = False; out.append(b)
        return out
    if isinstance(d.get('blocks'), list): d['blocks'] = drop(d['blocks'])
    if json.dumps(d) != before:
        files += 1
        open(p, 'w').write(json.dumps(d, ensure_ascii=False, indent=IND) + ('\n' if raw.endswith('\n') else ''))
print('files', files)
