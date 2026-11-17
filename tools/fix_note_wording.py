"""Second pass over src/data/local/*.json (after scrub_research_wording.py): research-note wording that the first pass does not catch.

The local sections were written from research notes, and some note labels and asides reached public pages (site review 2026-11-17, D-327):
"Question 1 for Jared", "The page cannot agree with itself", "How people search for it: ...", "Built stock — cross-reference only, never land",
"(the BC strata block — applies ...)", "recorded locator run", "NAME NOTE:", "Tenure flag, stated at the top", "(Ministry-listed names only)".
Rules, applied only to strings that contain one of these markers (other strings are left exactly as they are):
  1. MANUAL: whole sentences rewritten by hand (exact text).
  2. DROP: a sentence that is only about the research or the page is removed.
  3. SUBS: note labels are reworded in place ("locator run" -> "School Locator check", "BC strata block" -> "BC strata rules", ...).
  4. A list item or paragraph left empty is removed, and a list left with no items is removed.
Idempotent.   python3 -I tools/fix_note_wording.py [--dry]      (run after scrub_research_wording.py, before npm run build)
"""
import glob, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FILES = sorted(glob.glob(os.path.join(ROOT, 'src/data/local/*.json')))
SKIP_KEYS = {'h', 'gen', 'slug', 'id', 'pos', 'level', 'status', 'href', 'img', 'src', 'alt', 'url', 'canonical'}

MANUAL = {
    'Bench (City of Mission ground): 233–234; City page: taxes due Thursday, July 2, 2026, 10% penalty on current balances outstanding July 3, 2026) — city ground only ( Mission has no Supreme Court registry (standing note — relevant to foreclosure/court-ordered-sale searches, not to townhouse tenure).':
        'Bench (City of Mission ground): taxes were due Thursday, July 2, 2026, with a 10% penalty on current balances outstanding on July 3, 2026.',
    'City property taxes — flat 10% penalty: 233–234 plus Municipal Tax Regulation': 'City property taxes — flat 10% penalty: Community Charter ss. 233–234 plus Municipal Tax Regulation',
    ' — state both regimes only to keep them apart, and quote the flat 10% for a Stave Falls parcel inside the City.': '. A Stave Falls parcel inside the City pays the flat 10%.',
    'City of Mission property taxes — CITY regime only:': 'City of Mission property taxes:',
    'RT CORRECTION — required: The actual townhouse residential districts': 'The townhouse residential districts',
    'CITY AFFORDABLE-HOUSING PROCESS, not for-sale land:': 'City affordable-housing process, not land for sale:',
    'TENURE RECORD only — Mayfair Terrace, 2266 Atkins Ave: It is an apartment-form strata, recorded here only so its tenure is never mistaken for land stock.': 'Mayfair Terrace, 2266 Atkins Ave, is an apartment-form strata, not land.',
    'LOUGHEED TRANSIT CORRIDOR — adopted Jan 27, 2026 per the City record:': 'Lougheed Transit Corridor plan, adopted Jan 27, 2026:',
    ' — TENURE RECORD, never freehold land stock:': ' — leasehold, not freehold land:',
    'Its FAQ credits the Fraser Valley board\'s MLS® feed; CADREB\'s own territory description makes Chilliwack a CADREB market. Board identity matters because it decides whose statistics (here: none published at sub-area level) a buyer can ask for.':
        'Chilliwack is in the Chilliwack and District Real Estate Board\'s (CADREB) territory, even though some listing feeds credit the Fraser Valley board. The board decides whose statistics a buyer can ask for, and neither publishes figures for this sub-area.',
    'Its build year is itself unsettled (2020 vs 2021 across listings).': 'Its build year is unclear: listings give both 2020 and 2021.',
    'Schools: only are carried — Shortreed Community School, 27330 28 Ave, SD35, and Dorothy Peacock Elementary, 20292 91A Ave, SD35. Spelling lock: AREA = "Neilsen Grove", SCHOOL = "Neilson Grove Elementary" — neither asserted as a catchment here.':
        'Schools: Shortreed Community School, 27330 28 Ave (SD35), and Dorothy Peacock Elementary, 20292 91A Ave (SD35). In Delta, note the spelling: the area is "Neilsen Grove" and the school is "Neilson Grove Elementary". No catchment is confirmed for any listing here; check the address with the school district.',
    'TOWNSHIP — R-CL small lots:': 'Township of Langley R-CL small lots:',
    'CITY — zoning + SSMUH: City of Langley Zoning Bylaw 3300 by number — cite the number.': 'City of Langley zoning and small-scale housing: Zoning Bylaw 3300.',
    'Where condo stock concentrates: this page names no buildings and no concentration — it is a plans page.': '',
    'Where condo stock concentrates under these plans: this page names no buildings, so no concentration is stated from it. As plan context only, the Township\'s': 'Where condo stock concentrates under these plans: the Township\'s',
    'Named buildings/complexes: None is a land development, a subdivision or a lot offering here.': 'None of the named buildings or complexes here is a land development, a subdivision or a lot for sale.',
    'Named stock cross-references (no land count taken): None is a land offering and none is re-documented here.': '',
    'Built stock, all of it — never land.': '',
    'The page names a 60-unit project and a 37-lot subdivision — can I price against them?': 'Sources name a 60-unit project and a 37-lot subdivision — can I price against them?',
    'Serpentine, Surrey 55+ homes: None. Zero stock, stated plainly at the top of this section as required, what is rental or care, local rules and buyer questions':
        'Serpentine, Surrey 55+ homes: none for sale right now, plus seniors rental and care, local rules and buyer questions',
    'Cross-referenced stock (never re-documented here)': 'Related buildings nearby',
    'Any marketing that quotes a "North Maple Ridge market" figure is running ahead of an unsettled mapping that is Question 1 for Jared.':
        'The real estate board does not publish a separate "North Maple Ridge" market figure, so treat any quoted North Maple Ridge average with caution.',
    'In Serpentine, Surrey, the 55+ homes you can buy are None. Zero stock, stated plainly at the top of this section as required (strata).':
        'In Serpentine, Surrey, there are no 55+ homes to buy right now: no age-restricted strata buildings were found here.',
    'The "Beach Grove condo" is a corridor product, not a beach product. A buyer searching the page name expecting waterfront condos will not find one.':
        'Beach Grove condos are along the main road corridor, not on the beach. There are no waterfront condo buildings in Beach Grove.',
    'The school is the neighbourhood\'s search anchor. "École Braemar" is itself a common search term for the area, and the school at 3600 Mahon Avenue runs English, Early French Immersion and Late French Immersion in one building — a draw that detached-house listings trade on, while the catchment for any given house still has to be locator-checked.':
        'École Braemar, at 3600 Mahon Avenue, is the neighbourhood\'s best-known landmark. It runs English, Early French Immersion and Late French Immersion in one building, and house listings often mention it. Check the catchment for any given house with the North Vancouver School District\'s School Locator.',
    'The school is the neighbourhood\'s search anchor — and its catchment proof is one address deep. "École Braemar" is itself a common search term for the area, the school sits inside Braemar at 3600 Mahon Avenue with English + Early and Late French Immersion, and the only locator-verified chain is that address\'s own (→ Carson Graham Secondary). A listing that promises the catchment for any other street is ahead of the evidence.':
        'École Braemar sits inside Braemar at 3600 Mahon Avenue, with English plus Early and Late French Immersion. For the school\'s own address the School Locator gives Carson Graham Secondary as the high school. Catchments are set address by address, so confirm it for any other street before relying on a listing\'s claim.',
}
DROP = re.compile(r'How people search for it|Buyers also search|common search term|search anchor|Question \d for Jared|agree with itself|searching the page name|'
                  r'carried only to prevent misapplication|figure was opened|were not opened|was not opened|ahead of the evidence|'
                  r'never re-documented|This page names each building|it is a plans page', re.I)
SUBS = [
    (r'\s*\(Ministry-listed\)', ''),
    (r',\s*labelled correctly\b', ''), (r'\bnever land figures\b', 'not land figures'),
    (r'\s*\(\s+[^()]*?\.pdf\)', ''),
    (r'Floodplain (?:Bylaw No\. )?Designation and Construction Control Bylaw No\. Designation and Construction Control Bylaw No\. 2384, 2008 - Consolidated\.pdf', 'Floodplain Designation and Construction Control Bylaw No. 2384, 2008.'),
    (r'Floodplain Bylaw No\. Designation and Construction Control Bylaw No\. 2384, 2008 - Consolidated\.pdf', 'Floodplain Designation and Construction Control Bylaw No. 2384, 2008.'),
    (r'\s*\b(?:Designation and Construction Control Bylaw No\. 2384, 2008 - Consolidated|(?:Drainage )?System Protection Bylaw No\. 2266, 2007 - Consolidated Version|Bylaw No\. 2505, 2011 - Consolidated Version_0)\.pdf\b\.?', ''),
    (r'^Ravine-edge character: Parks and Open Space\.pdf$', ''),
    (r'\s*\bArea [A-H] - Residential Rates 20\d\d\.pdf\b\.?', ''),   # a file name left after a sentence (D-331)
    (r'(?:(?<=[.!?)"”])(?<![Nn]o\.)\s+|^)(?:- )?[^.!?/—:\n]{1,70}?\.pdf\b\.?(?=\s|$)', ''),
    (r'\b(excluded|named|detailed|described|carried|stated|noted|corrected|blended|established|row|table|zones|townhomes|frame|thresholds|minimums|product|buildings|building|rule|rules|facts|exemptions|checks|Road|sources|complex|categories|covenants|centre|chains|area|Area|unresolved|zero|consent) in\.(?=\s|$)', r'\1.'),
    (r'\bMarket context, labelled correctly:\s*', 'Market context: '), (r'\b(\w+ 20\d\d) context only, never land figures:', r'\1 figures for homes, not land:'),
    (r'\bTenure record only — never (?:strata|land stock), never (?:land stock|strata|a counted building here):\s*', 'Tenure note: '), (r'\bTenure record only:\s*', 'Tenure note: '), (r':\s*Tenure record only\.', '.'), (r'\s*Tenure record only\.', ''),
    (r'\bCount-once reminders \(never land\):\s*', ''), (r'\s*— POINTER\b', ''), (r'\bCross-reference only:\s*', ''),
    (r', named here only so a land reader does not mistake it for lot inventory\.', '. It is not a lot for sale.'), (r', named here only so a land reader does not mistake them for lot inventory\.', '. They are not lots for sale.'), (r'\bland reader\b', 'land buyer'),
    (r'\bis a page name, not a District (?:planning )?name\b', 'is a local neighbourhood name, not a District planning name'),
    (r'\bsearches run under only the page name\b', 'searches under only that name'), (r',? and page name\)', ')'), (r'\bshare one page name\b', 'share one name'), (r'\bunder one page name\b', 'under one name'),
    (r'\bSpelling lock, kept exact throughout: the AREA is\b', 'Note the spelling: the area is'), (r'; the SCHOOL is\b', ' and the school is'),
    (r'\bMLS listing cards using "Neilson Grove" for the AREA are feed text, not the area name\.', 'Some MLS® listings spell the area "Neilson Grove".'),
    (r'\ban unsettled\b', 'an unclear'), (r'\bunsettled\b', 'unclear'), (r'\bare not re-documented here as land\b', 'are not counted here as land'),
    (r'\bis not re-documented as land stock\b', 'is not counted as land'), (r'\bquoting an unclear list\b', 'relying on a list that may not apply to that address'),
    (r'\bSchool names (?:here )?are Ministry-listed names, spelled exactly\.', 'School names are spelled as the Ministry of Education lists them.'), (r'\bSchool Locator run\b', 'School Locator check'),
    (r'[,;]?\s*Ministry-listed (?:names and addresses|names/addresses|name and address|name/address|names|name)(?: only)?(?:, physical locations, not catchments)?', ''),
    (r'\(\s*[,;:]?\s*\)', ''), (r'\(\s*[,;:]\s*', '('), (r'\s*[,;]\s*\)', ')'),
    (r',?\s*cited to (?:the |its )?[^.;:]*?(?=[.;])', ''),
    (r'\s*—\s*cross-reference only here, never land\.', ', not land.'), (r'\bis a cross-reference only and\b', 'is listed for reference only and'),
    (r'\s*—\s*cross-reference only(?:, never land(?: inventory| stock)?)?', ''),
    (r'\s*\(cross-reference only\)', ''),
    (r',?\s*\bcross-reference only(?:, never land)?\b,?', ''),
    (r'\s*\((?:a )?single-address basis[^)]*\)', ''),
    (r'\bCatchments? — recorded locator runs?:', 'Catchment check:'),
    (r'\bCatchment, single-address only:', 'Catchment (one address):'),
    (r'\b[Rr]ecorded (SD\d+ )?locator runs\b', r'\1School Locator checks'), (r'\b[Rr]ecorded (SD\d+ )?locator run\b', r'\1School Locator check'),
    (r'\b(?:the |a )?recorded\s+(?=(?:SD\d+ )?School Locator)', 'the '),
    (r'(?<!School Locator )\b(SD\d+ )?locator runs\b', r'\1School Locator checks'), (r'(?<!School Locator )\b(SD\d+ )?locator run\b', r'\1School Locator check'),
    (r'\bSchool Locator School Locator\b', 'School Locator'),
    (r'\(the BC strata block — (applies|it applies)', '(BC strata rules apply'), (r'\bthe BC strata block applies\b', 'BC strata rules apply'),
    (r'\bthe BC strata block\b', 'BC strata rules'), (r'\bBC strata block\b', 'BC strata rules'), (r'\b([Bb])are-land strata block\b', r'\1are-land strata rules'),
    (r'\bthe strata block\b', 'the strata rules'), (r'\bstrata block\b', 'strata rules'), (r'\bthe land block\b', 'the land rules'), (r'\bland block\b', 'land rules'),
    (r'\bstrata rules — applies\b', 'strata rules — apply'), (r'\bstrata rules applies\b', 'strata rules apply'), (r'\bstrata rules \(applies\b', 'strata rules (apply'),
    (r'\b(Geography|Tenure|Classification) flag\b', r'\1'),
    (r'\bNAME NOTE:\s*', 'Name: '), (r'\b[Nn]aming note(?:, stated at the top)?:\s*', ''), (r'\bBoard-name note:\s*', ''),
    (r'\bTenure flag, stated at the top — ', 'Tenure — '), (r',?\s*stated at the top\b', ''), (r',?\s*stated plainly\b', ''),
    (r'\s*\(redirect case\)', ''), (r'\bredirect case only:\s*', ''),
    (r'\bconflict IN SOURCES\b', 'sources conflict'), (r'\bgenuinely unsettled\b', 'unclear'), (r'\bis unsettled in current sources\b', 'is unclear in current sources'),
    (r'\buntil the School Locator check\b', 'until a School Locator check'),
    (r'\s+and is non-transferable\b', ''), (r',?\s*labelled as community-level only\b', ' (community-level figures only)'),
    (r'\bTOWNSHIP — plans \+ zoning:', 'Township plans and zoning:'), (r'\bCITY — plans \+ zoning:', 'City plans and zoning:'),
]
SUBS = [(re.compile(a), b) for a, b in SUBS]
MARK = re.compile(DROP.pattern + r'|Ministry-listed|cited to|cross-reference only|single-address|locator run|strata block|land block|NAME NOTE|[Nn]aming note|Board-name note|'
                  r'stated at the top|stated plainly|redirect case|conflict IN SOURCES|unsettled|non-transferable|labelled as community-level|TOWNSHIP —|CITY —|labelled correctly|never land|Tenure record only|POINTER|Cross-reference only|land reader|page name|Spelling lock|the AREA|re-documented|Count-once|\.pdf\b| in\.(?:\s|$)|standing note|233–234', re.I)
EMPH = re.compile(r'(?<![A-Z-])(LEASEHOLD PREPAID(?=[ -]strata)|LEASEHOLD|PREPAID|FEE-SIMPLE|UNDIVIDED-INTEREST|HOUSING|CURRENT|UNDER|INCLUDING|TAXABLE|RENTAL|DISTINCT|DIFFERENT|THREE|FULL|LEASE|NOT|NEVER|ONLY|IF|AND|OR|TOWNHOME|TOWNHOUSE|PRESALE|RESTRICTIONS|STATUS|CO-OP|PREPAID(?=-strata))(?![A-Z]|-[A-Z])')


def unshout(s):
    if ' · ' in s: return s   # a source label: the publisher's own title
    def rep(m):
        a, b = m.start(), m.end()
        if s[:a].count('"') % 2 or s[:a].count('“') > s[:a].count('”'): return m.group(0)   # inside a quotation
        if re.search(r'\b[A-Z]{2,}\s*$', s[:a]) or re.match(r'\s*[A-Z]{2,}\b', s[b:]): return m.group(0)   # part of a capitalised name or heading
        w = m.group(0).lower()
        return w[0].upper() + w[1:] if a == 0 or re.search(r'[.!?:]\s$', s[:a]) else w
    return EMPH.sub(rep, s)


SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9“"(É])')
count = {'rewrite': 0, 'manual': 0, 'drop': 0, 'sub': 0, 'strings': 0, 'removed': 0}


def _fix(s):
    if EMPH.search(s) and len(s) > 40:
        u = unshout(s)
        if u != s: count['sub'] += 1; s = u
    if not MARK.search(s) and s.strip() not in MANUAL and not any(k in s for k in MANUAL): return s
    o = s
    for k, v in MANUAL.items():
        if k in s: s = s.replace(k, v); count['manual'] += 1
    if DROP.search(s):
        parts = SENT.split(s); keep = [p for p in parts if not DROP.search(p)]
        count['drop'] += len(parts) - len(keep); s = ' '.join(keep)
    for rx, to in SUBS:
        s2 = rx.sub(to, s)
        if s2 != s: count['sub'] += 1; s = s2
    s = re.sub(r'^\s*([a-z])', lambda m: m.group(1).upper(), s) if s != o else s   # a label removed from the front
    s = re.sub(r'(:\s+)([a-z])(?=[a-z]+ )', lambda m: m.group(1) + m.group(2), s)
    s = re.sub(r'\s{2,}', ' ', s).replace(' ,', ',').replace(' .', '.').replace('( ', '(')
    if s != o: count['strings'] += 1
    return s.strip() if s != o else s


# Plain-language rewrites of whole research-note sentences (D-329), keyed by the sentence as the passes above leave it, so they
# still apply after the local layer is regenerated from the same notes. A sentence whose source note changed no longer matches
# and keeps its generated wording until it is rewritten again.
RW = json.load(open(os.path.join(ROOT, 'tools/data/plain-rewrites.json'), encoding='utf-8'))


def fix(s):
    if s in RW: count['rewrite'] += 1; return RW[s]
    r = _fix(s)
    if r in RW: count['rewrite'] += 1; return RW[r]
    return r


def walk(o, key=None):
    if isinstance(o, str):
        return o if key in SKIP_KEYS else fix(o)
    if isinstance(o, list):
        out = []
        for x in o:
            n = walk(x, key)
            if (isinstance(n, str) and not n.strip() and isinstance(x, str) and x.strip()) or n is None: count['removed'] += 1; continue
            if isinstance(n, list) and not n and x: count['removed'] += 1; continue
            out.append(n)
        return out
    if isinstance(o, dict):
        out = {k: (walk(v, k) if k not in SKIP_KEYS else v) for k, v in o.items()}
        for k in ('t', 'text'):   # a part or paragraph whose only text was removed
            if k in o and isinstance(o[k], str) and o[k].strip() and not out[k].strip() and 'h' not in o: return None
        if o.get('t') == 'list' and o.get('items') and not out.get('items'): return None
        if o.get('t') == 'p' and o.get('parts') and not any((p.get('t') or '').strip() for p in out.get('parts') or []): return None
        if 'q' in o and 'a' in o and (not out['a'].strip() or not out['q'].strip()): return None
        return out
    return o


def main():
    dry = '--dry' in sys.argv; changed = 0
    for f in FILES:
        raw = open(f, encoding='utf-8').read(); j = json.loads(raw)
        n = walk(j)
        n['blocks'] = [b for b in n.get('blocks', []) if b is not None and not (b.get('t') == 'list' and not b.get('items'))]
        if n != j:
            changed += 1
            if not dry:
                m = re.match(r'[\[{]\n( +)', raw); s = json.dumps(n, indent=len(m.group(1)) if m else 2, ensure_ascii=False)   # keep the file's own indent
                open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
    print(('would change' if dry else 'changed'), changed, 'pages;', count)


if __name__ == '__main__':
    main()
