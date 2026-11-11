#!/usr/bin/env python3
"""Research-note wording left on public pages (D-213, Nov 11, 2026).

The condo, townhome and area notes still carried the researchers' working voice in places: "Queued, counted nowhere", "Held here as a
named candidate", "verify fresh", "Board geography:", "(expressly not X's own figures)", "per the directory's market report",
"per listing text". This rewrites those phrases in plain words without changing any fact. Idempotent; prints what it changed.
python3 -I tools/sweep_research_voice_2026_11_11.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)

EXACT = [   # one-off sentences first
    (' Held here as a named candidate, not counted, and no fact from any other Murrayville building may be carried to it.', ''),
    ('Held here as a named candidate, not counted, and no fact from any other Murrayville building may be carried to it.', ''),
    ('Queued, counted nowhere — ', ''),
    ('. Queued, counted nowhere', '.'),
    ('Queued, counted nowhere', ''),
    ('Name and townhouse form verify fresh: listings name', 'Listings name'),
    ('Form per listing text: duplex-style townhouses in a gated community, with clubhouse amenities per the directory (listing/directory copy, attributed as such).',
     'Listings describe duplex-style townhouses in a gated community, and the strata directory lists clubhouse amenities.'),
    ('"45+" per listing text is', '"45+" in the listings is'),
    ('amenities per listing text include', 'amenities in the listings include'),
    ('per the directory bylaw record and per listings', 'according to the strata directory and the listings'),
    ('carried as built 2014 per the directory', 'shown as built 2014 in the strata directory'),
    ('Board geography differs from City geography:', 'MLS® areas don’t match City boundaries:'),
    ('Board geography, with its caveat:', 'On MLS®, with one caveat:'),
    # second pass, same day: "contested / flagged / resolved nowhere" notes
    ('OCP citation contested — flagged, resolved nowhere; Albion Area Plan settled: The settled part: the Albion Area Plan', 'The Albion Area Plan'),
    ('City rules: OCP citation contested (7060-2014 vs 7998-2024) — flag, resolve nowhere.', ''),
    ('Maple Ridge frame flags: Zoning Bylaw No. 7600-2019; OCP citation contested (7060-2014 vs 7998-2024).', 'Maple Ridge zoning: Zoning Bylaw No. 7600-2019.'),
    ('OCP citation contested (7060-2014 vs 7998-2024) — flagged, resolved nowhere.', ''),
    ('OCP citation contested — flagged, resolved nowhere (7060-2014 vs 7998-2024).', ''),
    ('OCP citation contested — flagged, resolved nowhere', ''),
    ('OCP citation — contested, flagged, never resolved: ', ''),
    ('Twin Lakes 55+ disagreement — carried both ways, resolved nowhere: Both positions are carried here exactly; neither is adopted.',
     'Twin Lakes and 55+: the sources disagree, so both are given here. Confirm the current bylaws with the strata before you rely on either.'),
    ('Delta zoning number: contested — flagged, never asserted (City side): (sheets cite No. 7600, 2017; an internal title reads "8400, 2025"). Residential ladder:',
     'Delta zoning: Zoning Bylaw No. 7600. Minimum lot sizes for subdivision:'),
    ('Delta zoning number: contested — flagged, not asserted: ', 'Delta zoning: '),
    ('Zoning — number flagged, not asserted: ', 'Zoning: '),
    ('Zoning — codes documented, standards and bylaw number flagged: ', 'Zoning: '),
    (' — flagged check-current against the 2050 OCP', '; check it against the current 2050 plan'),
    ('(some listings record 2010 — flagged)', '(some listings record 2010)'),
    ('are flagged, not merged', 'are listed separately'),
    ('Presale — built-form, counted nowhere as land', 'Presale homes, not land'),
    ('Condo presale product on development ground — counted nowhere as land, and the seniors tower is not stock anywhere until built and offered.',
     'It is a presale on a development site, and the seniors tower is not for sale until it is built and offered.'),
    ('Documented, not counted: Queued; counted nowhere.', ''),
    (' Queued; counted nowhere in this batch.', ''),
    (' — queued, counted nowhere:', ':'),
    (' (read via search result 2026-11-01)', ''),
    (' It stays queued here, counted nowhere, until its sub-area filing is settled on a directory or developer source.', ' Which sub-area it is filed under is not settled yet.'),
    ('Longlea Estates, if purchased as strata, would sit under this block — it is queued here, so the block is stated for the form only.', 'If Longlea Estates is bought as strata, these strata rules apply to it.'),
    ('A coach house is not a townhouse complex and is counted nowhere as one.', 'A coach house is not a townhouse complex.'),
    (' — stalled/receivership presale, counted nowhere', ': a presale that stalled and went into receivership'),
    (' — and that complex (Eden Court) sits queued for the Abbotsford West home, counted nowhere.', ': Eden Court is covered with Abbotsford West.'),
    ('54 Ladner houses were flagged, and', '54 Ladner houses mention the golf course, and'),
    ('189 Langley houses were flagged, and', '189 Langley houses mention a golf course, and'),
    ('and it is a plan, not a presale, not a lot offering, and counted nowhere as inventory;', 'and it is a plan, not a presale or a lot for sale;'),
    (' — the Ministry name; the guide\'s "Shortreed Community Elementary" wording is flagged, not adopted.', ' (the Ministry’s name for it).'),
    ('Platform\'s townhouse-form units are Port Moody Centre ground, counted nowhere as townhomes.', 'Platform’s townhouse-style units are in Port Moody Centre, not here.'),
    ('Shortreed Community School, 27330 28 Ave (the Ministry’s name for it). Poppy Secondary) belongs to that address only.', 'Shortreed Community School, 27330 28 Ave, came up for one address checked here; confirm the catchment for yours.'),
    ('Delta zoning — number contested, flagged, not settled: City pages and amendment bylaws cite "Delta Zoning Bylaw No. 7600, 2017" (the bylaw whose). What is not contested: ', 'Delta zoning: Zoning Bylaw No. 7600, 2017. '),
    ('Delta zoning — number contested, flagged, not settled: ', 'Delta zoning: '),
    ('Delta zoning — number contested, flagged not settled, plus the village permit areas: City zone sheets cite the zoning bylaw as No. 7600, 2017, parcel by parcel; an internal consolidated title reading "8400, 2025" also circulates — neither number is asserted as settled here. On top of zoning,',
     'Delta zoning and the village permit areas: zoning is Zoning Bylaw No. 7600, 2017, parcel by parcel. On top of zoning,'),
    (' (zoning bylaw number contested)', ''), (' (zoning number contested)', ''),
    ('Filing-trap cross-references — never land, counted nowhere here: ', 'Not in this sub-area: '),
    ('documented here as its own form, never townhouse stock and never bare-land inventory; counted nowhere as townhomes.', 'their own form, not townhomes and not bare land.'),
]
RX = [
    (re.compile(r"per the directory's [A-Za-z\- ]*?(?:list|report|table|description of the complex set|description|headline|entry)\b"), 'according to the strata directory'),
    (re.compile(r'per the directory entry'), 'in the strata directory'),
    (re.compile(r'\bper the directory\b'), 'according to the strata directory'),
    (re.compile(r',? per listing text\b'), ', according to the listings'),
    (re.compile(r'Board geography:'), 'On MLS®:'),
    (re.compile(r'Community context only \(expressly not'), 'For context only (not'),
    (re.compile(r'Community context \(expressly not'), 'For context (not'),
    (re.compile(r'\bexpressly not\b'), 'not'),
    (re.compile(r'Queued — (.+?), counted nowhere'), r'\1'),
    # third pass (D-218): "conflict flagged", "queued", "not asserted" and similar, found by tools/site_audit.py
    (re.compile(r'(?:source |address |year |pad-rent |Pad-rent |unit count — |sub-area |Sub-area |feed-source |Feed-source )?conflict,? flagged(?: transparently)?:'), 'sources differ:'),
    (re.compile(r'— conflict flagged,'), '— sources differ;'),
    (re.compile(r'(?:Source conflict on build year|Source conflict), flagged:'), 'Sources differ on the build year:'),
    (re.compile(r'Feed-source conflict flagged\. ?'), ''),
    (re.compile(r'\bboundary[- ]flagged\b'), 'near the boundary'),
    (re.compile(r'the unit count is flagged as source-conflicted(?:, not resolved)?'), 'sources give different unit counts'),
    (re.compile(r'(?:, )?with the conflict flagged'), ', though some sources differ'),
    (re.compile(r'the conflict is flagged rather than resolved here'), 'the sources differ'),
    (re.compile(r'the conflict is flagged;'), 'sources differ;'),
    (re.compile(r'and the difference is flagged'), 'and the sources differ'),
    (re.compile(r'are both flagged'), 'both differ between sources'),
    (re.compile(r'are flagged as internally conflicted, not resolved'), 'are inconsistent within the source'),
    (re.compile(r'— a one-year conflict, flagged\.'), '— a one-year difference.'),
    (re.compile(r'CLASSIFICATION NOTE \(flagged up front\):'), 'Note:'),
    (re.compile(r'Conflicts flagged up front:'), 'Where sources differ:'),
    (re.compile(r', flagged first because it governs everything in this sub-area:'), ' first, because it governs everything in this sub-area:'),
    (re.compile(r'internal inconsistency flagged transparently:'), 'the City’s material is inconsistent:'),
    (re.compile(r',? with the stale framing flagged:'), ':'),
    (re.compile(r' citations flagged\)'), ' citations are out of date)'),
    (re.compile(r',? and it is flagged again in\.'), '.'),
    (re.compile(r' compresses 3% \+ 2%(?:, flagged| and is flagged)\.'), ' combines the 3% and 2% rates.'),
    (re.compile(r'PTT \+ exemptions, compression flagged:'), 'PTT and exemptions:'),
    (re.compile(r', which is repealed and should be flagged as such wherever a source still cites it'), ', which is repealed, so ignore any source that still cites it'),
    (re.compile(r',? and flagged as such\.'), '.'),
    (re.compile(r'OCP citation — contested, flagged, never resolved by guessing: '), ''),
    (re.compile(r'55\+ label flagged'), '55+ label: check the bylaws'),
    (re.compile(r'plus flagged additions'), 'plus possible additions'),
    (re.compile(r'the flagged Camberley Green tension'), 'the open question about Camberley Green'),
    (re.compile(r'plan history, flagged:'), 'plan history:'),
    (re.compile(r'Corridor facts west of Hastings-Sunrise are flagged as corridor facts wherever they appear\. ?'), ''),
    (re.compile(r'stays a flagged conflict without'), 'stays an open question without'),
    (re.compile(r'the one flagged rancher complex'), 'the one rancher complex whose age rule needs checking'),
    (re.compile(r'if not flagged up front'), 'if not pointed out first'),
    (re.compile(r'had the most flagged sales'), 'had the most golf-course sales'),
    (re.compile(r'Conflict flagged: '), 'Sources differ: '),
    (re.compile(r'Queued, documented-not-counted — '), ''),
    (re.compile(r'Queued item '), 'Planned: '),
    (re.compile(r'Queued(?::)? (?=Avalon Mews)'), 'Planned: '),
    (re.compile(r'is a queued project and is not counted in this area\'s inventory'), 'is a planned project, not homes you can buy today'),
    (re.compile(r'Plan expectations and queued items'), 'Plan expectations and planned projects'),
    (re.compile(r'plus whatever is queued'), 'plus whatever is coming'),
    (re.compile(r'No cross-referenced or queued complex is published'), 'No complex is published'),
    (re.compile(r'the building is queued, not counted:'), 'the building is not part of this count:'),
    (re.compile(r'The queued building'), 'The building'),
    (re.compile(r'Queued: (?=The Meadows)'), ''),
    (re.compile(r'(?<=TOWNHOUSE-form\. )Queued '), ''),
    (re.compile(r'(?<=listing title line\)\. )Queued '), ''),
    (re.compile(r'is therefore not asserted for this area'), 'does not apply here'),
    (re.compile(r' — a flat "\$2,500\+" line is an error,? and (?:it )?is not asserted for (?:this area|any S\.W\. Marine parcel)'), ' — a flat "$2,500+" figure is wrong'),
    (re.compile(r'Verify fresh from the strata plan / Form B before any use\.'), 'Check the strata plan and Form B before you rely on it.'),
    (re.compile(r'Counted nowhere as land;'), 'It is not land for sale;'),
    (re.compile(r'Counted nowhere as land\.'), 'Not land for sale.'),
    (re.compile(r'Note for board geography: north-arm is'), 'On MLS®, North Arm is'),
    (re.compile(r'different board geography'), 'different MLS® area'),
    (re.compile(r'non-residential board geography'), 'non-residential MLS® area'),
    (re.compile(r'it is a board geography label'), 'it is an MLS® area name'),
    (re.compile(r'(?i)\b(?:address |pad-rent |sub-area )?conflict,? (?:also )?flagged:'), 'Sources differ:'),
    (re.compile(r'\(address conflict, flagged\)'), '(sources differ on the address)'),
    (re.compile(r'Sub-area conflict flagged \(see headnote\)'), 'Sources differ on the sub-area'),
    (re.compile(r', with the per-address variation flagged'), ', though it varies by address'),
    (re.compile(r'Flagged change of plan:'), 'Change of plan:'),
    (re.compile(r'One directory labelling conflict is flagged:'), 'One directory label differs:'),
    (re.compile(r'^Queued item$'), 'Planned'), (re.compile(r'^Queued$'), ''),
    (re.compile(r'The variance is carried unresolved; '), ''),
    (re.compile(r'Fresh verification Nov 2, 2026: '), ''),
    (re.compile(r' \(fresh listing title line\)'), ''),
    (re.compile(r'([.!?"”)]) sources differ'), r'\1 Sources differ'),
    (re.compile(r'^Queued for re-verification by strata plan/title in the townhomes home; it is not land stock and is not absorbed here\.$'), ''),
    (re.compile(r'^It is in any event a built strata building, not land stock\. '), 'It is a built strata building, not land. '),
]


def fix(s):
    o = s
    for a, b in EXACT: s = s.replace(a, b)
    for r, b in RX: s = r.sub(b, s)
    return o if s == o else re.sub(r' {2,}', ' ', s).strip()


def walk(x, hits):
    if isinstance(x, dict): return {k: walk(v, hits) for k, v in x.items()}
    if isinstance(x, list): return [walk(v, hits) for v in x]
    if isinstance(x, str):
        y = fix(x)
        if y != x: hits.append((x, y))
        return y
    return x


def main():
    files = changed = 0
    for f in sorted(glob.glob('src/data/local/*.json')):
        raw = open(f, encoding='utf-8').read(); hits = []
        d = walk(json.loads(raw), hits)
        if not hits: continue
        for b in d.get('blocks', []) if isinstance(d.get('blocks'), list) else []:   # list items the sweep emptied
            if b.get('t') == 'list': b['items'] = [it for it in b['items'] if ''.join(x.get('t', '') for x in it).strip()]
        if isinstance(d.get('blocks'), list):
            d['blocks'] = [b for b in d['blocks'] if not (b.get('t') == 'list' and not b['items']) and not (b.get('t') in ('p', 'h') and 'text' in b and not b['text'].strip() and not b.get('parts'))]
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        s = json.dumps(d, ensure_ascii=False, indent=ind) if ind else json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
        files += 1; changed += len(hits)
    print('files', files, '| strings changed', changed)


if __name__ == '__main__': main()
