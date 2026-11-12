#!/usr/bin/env python3
"""Research-note wording, sixth pass (D-243, Nov 12, 2026), from the post-launch review.

Rewrites sentences that talk to a writer or about "the page" ("do not quote", "a page that calls ... would be inventing",
"this page does not claim") into plain statements for a buyer. No fact is changed. Idempotent; prints every change.
python3 -I tools/sweep_research_voice_pass6_2026_11_12.py"""
import glob, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
Q = '["“”]'
RX = [
    (r', but a page that calls every age-flagged building ' + Q + r'55\+' + Q + r' would be inventing the number for ([^.]+)\.', r', but the generic flag does not prove a 55+ bylaw for \1. Read the registered bylaws.'),
    (r' — do not quote the early ones\.', ', so rely on the latest.'),
    (r', so the figure cannot be quoted as an MLS Big Bend statistic', ', so it is not an MLS Big Bend statistic'),
    (r'Any page copy implying a Big Bend condo scene would be inventing one\.', 'Big Bend does not have a condo scene.'),
    (r'Any page giving Big Bend a neighbourhood population is inventing it\.', 'No neighbourhood population figure is published for Big Bend.'),
    (r', and neither should be quoted as the other\.', ', so the two are not interchangeable.'),
    (r', so this page does not quote a typical price\.', ', so there is no meaningful typical price.'),
    (r'Any source quoting an? (' + Q + r'[^"“”]+' + Q + r') is inventing a figure the publisher does not produce\.', r'No \1 is published for this sub-area.'),
    (r'; blending them invents a market neither one had\.', '; a blended figure describes neither one.'),
    (r'Several for-lease cards on the first page display the price as masked \(([^)]*)\) in the page text; the page does not explain the masking, so', r'Several for-lease listings show the price as masked (\1), so'),
    (r' \(dated context\)', ''),
    (r' and the page calls Durieu ' + Q + r"Mission['’]s most remote rural area,?" + Q + r',? but', ', but'),
    (r' — do not cite it(?: as current)?\.', '.'),
    (r' before promising library proximity in a listing', ''),
    (r'(and|,|—) the page does not (state|give|tell)\b', r'\1 that does not \2'),
    (r'Neither figure should be quoted in a listing — ', 'Neither figure is reliable — '),
    (r" — a small, concrete example of the sub-area['’]s non-seniors character in the board['’]s own data", ''),
    (r'; do not quote it as one\.', '.'),
    (r' — do not quote one as the other\.', ', so they are not comparable.'),
    (r'do not quote either figure as fact', 'treat neither figure as fact'),
    (r'do not quote either number as fact', 'treat neither number as fact'),
    (r'do not quote any of the three figures as', 'treat none of the three figures as'),
    (r'; do not quote a single figure from a listing\.', '; do not rely on a single figure from a listing.'),
    (r' — do not cite the old vision as current policy for', ' — the old vision is no longer current policy for'),
    (r'^Date-check any policy citation for the King Edward node: t', 'T'),
    (r'No sub-area figures are published and none are invented here\.', 'No sub-area figures are published.'),
    (r', but this page does not claim any (building|complex) is age-restricted', r', but that alone does not mean any \1 is age-restricted'),
    (r' — full text in the langleycity note', ''),
    (r' — they are stated here only so no page invents a Mount Currie application of them; they do not price', ' — they do not price'),
    (r' — do not publish any one of them as (' + Q + 'the' + Q + r') park rate; confirm', r' — none of them is \1 park rate; confirm'),
    (r'No such school exists — the name was invented from a park name in other copy\.', 'No. There is no school by that name; check the district school locator for your address.'),
    (r', so no Serpentine median, pace or supply figure should be quoted from either source\.', ', so there is no reliable Serpentine median, pace or supply figure.'),
    (r'No ALR percentage split is stated or invented\.', 'No ALR percentage split is published.'),
    (r' should not be quoted for RA-1 lots without', ' do not apply to RA-1 lots without'),
    (r' — do not quote a current pad rent from it; confirm the current pad rent and park rules with the park before writing\.', ' — confirm the current pad rent and park rules with the park before writing an offer.'),
    (r' for this building should be published as fact\.', ' for this building should be taken as fact.'),
]
RX = [(re.compile(a), b) for a, b in RX]

RX2 = [
    (r'^What the page covers(?: — IDENTITY CALL)?: ', 'Area covered: '),
    (r'^IDENTITY (?:CALL|LOCK): ', ''),
    (r'^Feed scope — the identity call: every first-page card is labelled ', 'Listings here carry the '),
    (r'^Page and ground: ', ''),
    (r'\b[Ee]very first-page card (?:is|was) labelled (?:with )?(?:the )?board sub-area', 'listings here carry the board sub-area'),
    (r'Not on the evidence of the first page: (\w+) of the (\w+) cards carried an open-house time block and (.+?) carried no open-house label or time at all in the page text, so treat an unlabelled card as', lambda m: f'Not always: when checked, {m.group(1)} of the {m.group(2)} listings showed an open-house time and {m.group(3).replace(" card", " listing")} showed none, so treat an unlabelled listing as'),
    (r'The cards visible in the page text are labelled', 'Current listings are labelled'),
    (r'^Market context: none quoted\.$', ''),
    (r'Board row, stated as a board row only \(not a market figure, and no SnapStats claim is made from it\): ', 'Board counts: '),
    (r'PROPOSAL, never inventory: ', 'Proposal only: '),
    (r' — documented as a project, never inventory:', ':'),
    (r'It creates no lots and is never inventory\.', 'It creates no lots for sale.'),
    (r' — feed evidence only, never inventory', ''),
    (r' — feed evidence only, no count added\.', '.'),
    (r"This guide['’]s appended cards show", 'Current listings show'),
    (r'Suite evidence — feed level only: several feed listings describe', 'Suites: several listings describe'),
    (r' — listing copy cited as feed evidence of the SSMUH/suite pattern in the pocket, not as a count of legal suites\.', '. That is not a count of legal suites.'),
    (r'Lot character, as the page states it — page description only: ', 'Lot character: '),
    (r'Zoning character, as the page states it: ', 'Zoning character: '),
    (r"The site['’]s own copy says much of the belt is in the Agricultural Land Reserve — page copy, not a measured split\.", 'Much of the belt is in the Agricultural Land Reserve; no measured split is published.'),
    (r"The site['’]s own copy describes Ladner Rural as (.+?) — cited as page identity only\.", r'Ladner Rural is \1.'),
    (r"The hamlet names in the page copy are not official names: (.+?) appear only as the site['’]s own copy\.", r'The hamlet names are not official names: \1 are informal labels.'),
    (r'Band ceiling named by the page', 'Price ceiling'),
    (r'None — feed filter only', 'None (price filter only)'),
    (r' — quote either with its source\)', ')'),
    (r'A buyer \(or a page\) quoting', 'A buyer quoting'),
    (r'Any page copy citing', 'Anything citing'),
    (r'any Forest Glen page quoting', 'any Forest Glen document quoting'),
    (r'older page copy citing', 'older material citing'),
    (r'Do not quote a Canyon Springs median\.', 'There is no Canyon Springs median.'),
    (r'Do not quote a single year for Yale Court without the strata plan\.', "Confirm Yale Court's build year on the strata plan."),
    (r'Do not quote it as known 55\+ on the strength of the townhome count, and do not strike the townhome count on the strength of the age uncertainty\.', 'The townhome count does not prove it is 55+, and the age uncertainty does not change the townhome count.'),
    (r'None(?: of these)? is safe to quote singly — ', 'No single figure is reliable — '),
    (r'Do not present it as a lot subdivision\.', 'It is not a lot subdivision.'),
    (r'Do not present Rail District ground as buyable lots\.', 'Rail District ground is not buyable lots.'),
    (r'Do not present Mount Currie housing as freehold or strata in any page copy\.', 'Mount Currie housing is not freehold or strata.'),
    (r'(?:;| —) none is quoted (?:lot-by-lot )?here\.', '.'),
    (r'Do not quote a plan number, a lot count or a fee for a bare-land strata lot here until the title and Form B are pulled\.', 'Confirm the plan number, lot count and fee for a bare-land strata lot here on the title and Form B.'),
    (r"Do not quote any city['’]s tax dates for", "No city's tax dates apply to"),
    (r'Never cite these (City|District) rules for a (District|City) address\.', r'These \1 rules do not apply to a \2 address.'),
    (r'Never cite the replaced OCP Bylaw No\. 18020 as current\.', 'The replaced OCP Bylaw No. 18020 is no longer current.'),
    (r'Do not quote R1-1 permissions for a Southlands lot without', 'R1-1 permissions do not apply to a Southlands lot without'),
    (r'Do not quote either figure as settled\.', 'Neither figure is settled.'),
    (r' — a different place with its own board row, never used for this page\.', ', which is a different place.'),
    (r' with its own row, never used for Grandview\.', ' with its own figures.'),
    (r' — never used for Grandview\. Morgan Crossing ≠ Morgan Creek\.', '. Morgan Crossing is not Morgan Creek.'),
    (r'is the working north edge used for this page', 'is the practical north edge'),
    (r' needs a City check, not the page copy\.', ' needs a City check.'),
    (r'^\(3\) The quoted City tax-exemption notice spells .*? as rendered on the page\.$', ''),
    (r' ?No feed-count header was visible, so no total count is stated\.', ''),
    (r'Also visible: a unit-numbered Murrayville card \(([^)]*)\) whose form \(detached house vs strata unit\) cannot be settled from the card text read\.', r'One unit-numbered Murrayville listing (\1) may be a strata unit rather than a detached house; check the listing.'),
    (r' in the designation text read\)', ' in the designation text)'),
    (r'the first-page cards came from', 'the current listings came from'),
    (r'\bOne first-page card\b', 'One current listing'),
    (r'across the first-page cards', 'across the current listings'),
    (r', and one card itself discloses', ', and one listing discloses'),
    (r'the townhome areas the page leads with are thinner', 'the main townhome areas are thinner'),
    (r' cluster the page leads with;', ' cluster;'),
    (r' in two groups as the page structures them — four parks it groups as', ' in two groups — four parks listed as'),
    (r', plus two it groups as', ', plus two listed as'),
    (r'All six addresses the page names are in the Township of Langley; no City of Langley park is named on the page\.', 'All six addresses are in the Township of Langley; none is in the City of Langley.'),
    (r'no City of Langley park is named on the page', 'none is in the City of Langley'),
    (r' — all sourced by the page from recent listings', ' — all taken from recent listings'),
    (r' as the page and the Agricultural Area Plan describe them', ' as the Agricultural Area Plan describes them'),
    (r'; the page names an October 21 meeting without a year', '; an October 21 meeting is named without a year'),
    (r'\b[Tt]he page covers\b', 'this page covers'),
    (r' — cross-reference only, not land stock$', ''),
    (r' \(cross-reference only, not met in Braemar\)$', ''),
]
RX += [(re.compile(a), b) for a, b in RX2]

# Paragraphs that describe the web page itself (its headline, blocks and feed) rather than the place: dropped or cut back to the fact.
RX3 = [
    (r'^(?:Area covered: )?(?:[Tt]he|A) Campbell Valley area(?: / homes)? page, headed .*$', ''),
    (r'^A City of Chilliwack neighbourhood guide headed .*$', ''),
    (r'^A Township of Langley neighbourhood guide headed .*$', ''),
    (r"^Jared Gibbons['’] (?:South Surrey )?agent[- ](?:bio|profile) page — .*$", ''),
    (r'^A property-type page headed .*$', ''),
    (r'^The page carries no FAQ block, so .*$', ''),
    (r'^Reviews block — page statement only: .*$', ''),
    (r'^The page has no FAQ and no OCP-vs-zoning explainer; .*$', ''),
    (r'^Area covered: a communities/parks directory headed .*$', ''),
    (r'^Listings feed: the Walnut Grove guide has .*$', ''),
    (r'^A named-complex page headed ["“][^"”]+["”],? for one townhome community at', 'One townhome community at'),
    (r'^A named-complex page headed ["“][^"”]+["”],? for the NORTH phase only, at', 'The north phase only, at'),
    (r'^A named-complex page headed ["“][^"”]+["”],? for ', ''),
    (r'^An index\. The page, headed ["“][^"”]+["”],? links one guide', 'This index links one guide'),
    (r', and it carries no single-neighbourhood profile of its own\.', '.'),
    (r'^A neighbourhood guide headed ["“][^"”]+["”] for Bridal Falls, a small', 'Bridal Falls is a small'),
    (r'^A communities/parks directory page headed ["“][^"”]+["”] — four parks it groups as', 'Four parks are listed as'),
    (r'; this page is headed ["“][^"”]+["”],? subtitled ["“][^"”]+["”],? and carries no listing feed — its content is .*$', '.'),
    (r' The guide feed sits inline with a count header ["“][^"”]+["”] \(snapshot only\),(?: headed ["“][^"”]+["”],)? and every listing we checked is labelled', ' Every listing we checked is labelled'),
]
RX += [(re.compile(a), b) for a, b in RX3]

RX4 = [
    (r'^The page does not say\. Under the BC framework', 'Under the BC framework'),
    (r'This is a named-complex page, not an area page: (.)', lambda m: m.group(1).upper()),
    (r' ?Market context: none quoted\.', ''),
    (r'every first-page card is labelled ', 'every listing checked is labelled '),
    (r',? all sourced by the page from recent listings', ', all taken from recent listings'),
    (r', never a lot offering and never inventory', ', not a lot offering'),
    (r' in the bylaw text read\.', ' in the bylaw text.'),
]
RX += [(re.compile(a), b) for a, b in RX4]

RX5 = [
    (r' verified: \(verified ledger, carried exactly\):', ':'),
    (r' ?\(Verified ledger, as instructed\.\)', ''),
    (r' It belongs to a future verification pass\.', ''),
    (r' — verified ledger entry:', ':'),
    (r' — carried exactly from the standing verified ledger', ''),
    (r', verified ledger:', ':'),
    (r' ?\(Standing ledger position\.\)', ''),
    (r' ?\(Checked 2026-11-02\.\)', ''),
    (r'Zone 4 belongs to Brunette only in this ledger — it is not', 'Zone 4 here is Brunette only — it is not'),
    (r'Off-reserve ledger numbers from other jurisdictions', 'Off-reserve bylaw numbers from other jurisdictions'),
    (r'; the ledger holds it was never adopted', '; it was never adopted'),
    (r'before suggesting demolition of a character house', 'before planning to demolish a character house'),
    (r" permissions must never be quoted for a Southlands lot without", ' permissions do not apply to a Southlands lot without'),
]
RX += [(re.compile(a), b) for a, b in RX5]

RX6 = [
    (r'\bIdentity call: ', ''),
    (r' ?\(Checked against .*?\.csv \(as of [^)]*\)\.\)', ''),
    (r'^Cross-reference, directory data-quality trap — carried exactly as the land home carries it$', ''),
    (r'; not yet checked against the OCP text by me', ''),
    (r' - see notes\b', ''),
    (r'The plan stack, as verified: ', 'The plan stack: '),
]
RX += [(re.compile(a), b) for a, b in RX6]


def prune(o):
    if isinstance(o, dict):
        o = {k: prune(v) for k, v in o.items()}
        if isinstance(o.get('parts'), list): o['parts'] = [p for p in o['parts'] if not (isinstance(p, dict) and set(p) <= {'t'} and not str(p.get('t', '')).strip())]
        if isinstance(o.get('items'), list): o['items'] = [it for it in o['items'] if not (isinstance(it, list) and not ''.join(str(x.get('t', '')) for x in it if isinstance(x, dict)).strip()) and it != '']
        return o
    if isinstance(o, list):
        out = [prune(v) for v in o]
        return [b for b in out if not (isinstance(b, dict) and b.get('t') in ('p', 'h', 'list') and not (b.get('text') or '').strip() and not b.get('parts') and not b.get('items'))]
    return o

def fix(s):
    o = s
    for r, b in RX: s = r.sub(b, s)
    if s == o: return o
    s = re.sub(r'(^|[.?!] )(this page covers|listings here carry)', lambda m: m.group(1) + m.group(2)[0].upper() + m.group(2)[1:], s)
    if s[:1].islower() and o[:1].isupper(): s = s[0].upper() + s[1:]
    return re.sub(r' {2,}', ' ', s).strip() if not o.startswith(' ') and not o.endswith(' ') else s

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
    for f in sorted(glob.glob('src/data/local/*.json') + glob.glob('src/data/pages/*.json') + glob.glob('src/data/*.json') + glob.glob('src/data/presales/*.json')):
        raw = open(f, encoding='utf-8').read()
        if not any(k in raw for k in ('quote', 'invent', 'the page', 'this page', 'do not cite', 'dated context', 'langleycity note', 'published as fact', 'concrete example', 'do not publish', 'promising library', 'Date-check', 'page', 'IDENTITY', 'inventory', 'feed', 'cite', 'card', 'cross-reference', 'never used', 'Board row', 'headed', 'FAQ', 'count header', 'ledger', 'verification pass', 'Checked 2026', 'suggesting demolition', 'never be quoted', 'Identity call', '.csv', 'see notes', 'as verified', 'not yet checked')): continue
        hits = []; d = walk(json.loads(raw), hits)
        if any(b == '' for _, b in hits): d = prune(d)
        if not hits: continue
        for a, b in hits:
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), 0)
            print(f'{os.path.basename(f)}\n  - {a[max(0,i-60):i+170]}\n  + {b[max(0,i-60):i+170]}')
        ind = 1 if '\n "' in raw[:200] else (2 if '\n  "' in raw[:200] else None)
        asc = '\\u' in raw
        s = json.dumps(d, ensure_ascii=asc, indent=ind) if ind else json.dumps(d, ensure_ascii=asc, separators=(',', ':'))
        open(f, 'w', encoding='utf-8').write(s + ('\n' if raw.endswith('\n') else ''))
        files += 1; changed += len(hits)
    print('files', files, '| strings changed', changed)

if __name__ == '__main__': main()
