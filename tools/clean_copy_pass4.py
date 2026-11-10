"""Fourth copy pass (D-199, from the Nov 10 two-day review): research wording that the D-194 passes did not cover, and generator glitches.

- "verified" used as a research note ("no verified condo stock", "None was verified", "the verified list") -> "known" / "that I know of".
  Buyer instructions ("must be verified in the depreciation report", "verify it on title") are left alone.
- "Sub-area medians are not published" read as if the site had no medians, while the guide's quick-facts box shows them: it meant the board.
- "the export" (Jared's MLS® export) -> "the MLS® data"; a capital "Published" mid-sentence; doubled words; ". ." endings;
  "lines in are" where an old generator dropped the area name (now "lines here are").
Idempotent; walks every string in src/data/{pages,local,posts,designed} except link/slug fields. python3 -I tools/clean_copy_pass4.py"""
import collections, glob, json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SKIP = {'h', 'href', 'url', 'src', 'slug', 'path', 'canonical', 'gen', 'id', 't', 'cls', 'kind', 'status', 'photo', 'needs_from_muse'}
NOUN = (r'condo|condos|townhouse|townhouses|townhome|townhomes|apartment|apartments|stock|entries|entry|list|building|buildings|complex|complexes|'
        r'project|projects|55\+|duplex|duplexes|ones?|tower|towers|buyable|named|attached|strata|rental|units?|homes?|age-restricted|seniors|co-op|'
        r'care|examples?|counts?|address|addresses|presales?|forms?|names?|figures?|developments?|parks?|blocks?|options?|choices?|sites?|properties|property|lots?|'
        r'facilities|facility|schools?|stops?|routes?|condo-only|mid-rise|low-rise|high-rise|concrete|wood-frame|apartment-condo|fee-simple|independent|assisted')
RULES = [
    ('transit frame', re.compile(r'\s*[—–-]\s*verified frame:'), ':'),
    ('no verified one', re.compile(r'\bNo verified one\.'), 'None that I know of.'),
    ('nowhere verified', re.compile(r'\bnowhere verified\b'), 'nowhere that I know of'),
    ('none was verified', re.compile(r'\b([Nn])one (?:completed and named in the sub-area )?(?:was|were|is|are) (?:independently )?verified(?: yet)?\b'), r'\1one that I know of'),
    ('no verified', re.compile(r'\b([Nn])o verified\b'), r'\1o known'),
    ('could be verified by name', re.compile(r'\bcould be (?:verified|known) by name on a public source\b'), 'is named on a public source'),
    ('verified by name', re.compile(r'\bverified by name\b'), 'known by name'),
    ('everything was verified', re.compile(r'\bEverything was verified on the official pages on\b'), 'Everything was checked against the official pages on'),
    ('verified not age-restricted', re.compile(r'\s*[—–]\s*verified not age-restricted'), ', not age-restricted'),
    ('no name anyone has verified', re.compile(r'\bhas no name anyone has verified\b'), 'has no known name'),
    ('verified (adjective)', re.compile(r'\bverified (?=(?:' + NOUN + r')(?:\b|(?<=\+)))'), 'known '),
    ('Verified (adjective)', re.compile(r'\bVerified (?=(?:' + NOUN + r')(?:\b|(?<=\+)))'), 'Known '),
    # second round (same review): the remaining research uses of "verified"
    ('standing ledger', re.compile(r'\s*\(Standing verified ledger[^)]*\)'), ''),
    ('one tile', re.compile(r'One tile verified at City-source level pass:\s*'), ''),
    ('this pass verified', re.compile(r'\bThis pass verified (\d+) apartment-condo buildings by name on\b'), r'\1 apartment-condo buildings are known by name from'),
    ('kerrisdale roster', re.compile(r'\bHow many verified Kerrisdale apartment-condo buildings are on this roster\?'), 'How many apartment-condo buildings does Kerrisdale have?'),
    ('albion verifies', re.compile(r'\bAlbion verifies zero\b'), 'Albion has zero known'),
    ('(verified)', re.compile(r'\s*\(verified\)'), ''),
    ('verified + date', re.compile(r'\bverified (?=(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d)'), 'as of '),
    ('bylaw 8830', re.compile(r'(Bylaw 8830 \(1986\)) (?:is )?verified(?: from City pages)?\.'), r'\1 applies.'),
    (') verified:', re.compile(r'\) verified:'), '):'),
    ('verified City instruments', re.compile(r'[—–-] verified City instruments:'), '— City instruments:'),
    ('verified not', re.compile(r',\s*verified not\b'), ', not'),
    ('stock verified by tenure', re.compile(r'\bstock verified by tenure\b'), 'stock by tenure'),
    ('buildings verified (row)', re.compile(r'\bApartment-condo buildings verified\b'), 'Known apartment-condo buildings'),
    ('winery sites', re.compile(r'\bverified on each winery.s own site\b'), "each listed on the winery's own site"),
    ('own sites', re.compile(r'\bverified on their own sites\b'), 'listed on their own sites'),
    ('city portal', re.compile(r',?\s*verified on the City portal\b'), ', on the City portal'),
    ('what is verified', re.compile(r'\bWhat is verified is\b'), 'What is known is'),
    ('is verified for', re.compile(r'\bis verified for\b'), 'is on record for'),
    ('N verified', re.compile(r"\b(zero|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|every|all|other|nearest|[Tt]he|its|their|[A-Z][a-z]+(?:'|’)s|sub-area(?:'|’)s) verified\b"), r'\1 known'),
    ('no X verified', re.compile(r'\b([Nn]o (?:named )?[^.;:—]{1,60}?) verified(?=\s*[.;:,—])'), r'\1 known'),
    ('was verified', re.compile(r'\bwas verified(?=\s*[.;,—–:)])'), 'is known'),
    ('were verified', re.compile(r'\bwere verified(?=\s*[.;,—–:)])'), 'are known'),
    # internal research jargon left in older pages
    ('banked batch', re.compile(r'\s*\(verified, banked in the [^)]*\)'), ''),
    ('stated for completeness', re.compile(r'\s*[—–]\s*stated for (?:edge )?completeness(?=[,:;)])|,?\s*stated for (?:edge )?completeness(?=[,:;)])'), ''),
    ('inside this scope', re.compile(r'\binside this scope\b'), 'in this area'),
    ("this scope's", re.compile(r"\bon this scope(?:'|’)s\b"), "on the area's"),
    ('in scope', re.compile(r'\bThe one seniors complex in scope\b'), 'The one seniors complex here'),
    ('counted entries', re.compile(r'\b(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten) counted(?: entries)?:'), r'\1:'),
    ('roster question', re.compile(r'\bHow many verified ([A-Z][\w ]*?) (condo|apartment-condo|townhouse) buildings are on this roster\?'), r'How many \2 buildings does \1 have?'),
    ('this pass found', re.compile(r'\bThis pass found the stock in\b'), 'The stock sits in'),
    ('directory verified to exist', re.compile(r';\s*the directory page was verified to exist for this building and address'), ''),
    ('tenure-verified evidence', re.compile(r'\bOn named, tenure-verified evidence, yes:'), 'Yes:'),
    ('verified so far', re.compile(r'\bevery complex verified so far\b'), 'every known complex'),
    ('listing-copy flag', re.compile(r'\s*Counted with the name flagged as listing-copy sourced\.'), ''),
    ('index listings', re.compile(r'\b(tower|low-rise) verified through current (?:[A-Z][\w ]*? )?index listings\b'), r'\1 seen in current listings'),
    ('are verified in', re.compile(r'\bare verified in\b'), 'are in'),
    ('medians not published', re.compile(r'\b(?:Per-sub-area|Sub-area) medians are not published\b'), 'The board does not publish sub-area medians'),
    ('medians not published (lower)', re.compile(r'\((?:per-)?sub-area medians are not published\)'), '(the board does not publish sub-area medians)'),
    ('the export', re.compile(r'\b([Tt])he export\b'), r'\1he MLS® data'),
    ('Published mid-sentence', re.compile(r'(?<=[a-z,;] )Published (?=municipal records)'), 'published '),
    ('Not found + Published', re.compile(r'\bNot found Published municipal records\b'), 'Published municipal records'),
    # an old generator dropped the area name: "rental/pet lines in are listing data" -> "lines here are"
    ('missing area name', re.compile(r'\b(buildings|building|complexes|complex|co-operatives|residences|residence|towers|figures|set|addresses|listing|lines|stock|named)'
                                     r' in (?=(?:are|is|sits|sit|have|has)\b)'), r'\1 here '),
    ('everything else verified', re.compile(r'\bEverything else verified in\b'), 'Everything else in'),
    ('specific specific', re.compile(r'\bspecific specific\b'), 'specific'),
    ('records records', re.compile(r'\brecords records\b'), 'records'),
    ('parcel parcel-by-parcel', re.compile(r'\bPrice a Glen Valley parcel parcel-by-parcel\b'), 'Price each Glen Valley parcel on its own'),
    ('. .', re.compile(r'(?<=\S)\.\s+\.(?=\s|$)'), '.'),
]
stats = collections.Counter(); changed_files = 0


def fix(s):
    for name, rx, rep in RULES:
        s2, n = rx.subn(rep, s)
        if n: stats[name] += n; s = s2
    return s


def walk(o):
    if isinstance(o, dict): return {k: (v if k in SKIP and not (k == 't' and isinstance(v, str) and ' ' in v) else walk(v)) for k, v in o.items()}   # 't' is a block type or, in a link part, the text
    if isinstance(o, list): return [walk(v) for v in o]
    if isinstance(o, str): return fix(o)
    return o


for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/*/*.json'))):
    if not re.search(r'/src/data/(pages|local|posts|designed)/', f): continue
    raw = open(f, encoding='utf-8').read(); d = json.loads(raw); d2 = walk(d)
    if d2 != d:
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        out = json.dumps(d2, ensure_ascii=False, indent=ind) if ind else json.dumps(d2, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(out + ('\n' if raw.endswith('\n') else '')); changed_files += 1
print('files changed', changed_files); [print(f'  {n:5}  {k}') for k, n in stats.most_common()]
