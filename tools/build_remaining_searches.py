#!/usr/bin/env python3
"""Worksheet of every saved search Jerry still has to build (the held "B" pages in the launch pack, minus the 20 price-band pages
that have their own sheet): one row per page with the page link and the search criteria.
Writes docs/review/idx/remaining-searches-2026-11-08.xlsx. Jerry fills Search ID and Embed code; filled sheets are read by build_idx_embeds.py
(add the -DONE file to its worksheet loop when it comes back)."""
import csv, glob, json, os, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..'); sys.path.insert(0, HERE)
import build_gvr_pages as GV
OUT = os.path.join(ROOT, 'docs/review/idx/remaining-searches-2026-11-08.xlsx')
SEO = json.load(open(os.path.join(ROOT, 'src/data/seo-final.json')))

HELD = [r for r in csv.DictReader(open(glob.glob(os.path.join(ROOT, 'docs/review/launch/launch-approval-*.csv'))[0])) if r['Batch'].startswith('B.') and r['Group'] != 'Price band searches']
INV = {sl: k for k, (sl, new) in GV.PLAN.items() if sl}      # slug -> 'Board|Sub-area'

CITY = {  # slug prefix -> (name, MLS area, sub-area filter)
    'burnaby': ('Burnaby', 'Burnaby North + Burnaby South + Burnaby East', '(none)'), 'coquitlam': ('Coquitlam', 'Coquitlam', '(none)'),
    'port-coquitlam': ('Port Coquitlam', 'Port Coquitlam', '(none)'), 'port-moody': ('Port Moody', 'Port Moody', '(none)'),
    'new-westminster': ('New Westminster', 'New Westminster', '(none)'), 'mission': ('Mission', 'Mission', '(none)'),
    'north-delta': ('North Delta', 'N. Delta', '(none)'), 'ladner': ('Ladner', 'Ladner', '(none)'), 'cloverdale': ('Cloverdale', 'Cloverdale', '(none)'),
    'south-surrey': ('South Surrey', 'South Surrey White Rock', 'Leave out the White Rock sub-area'), 'surrey': ('Surrey', 'Surrey + North Surrey', '(none)'),
}
TYPES = {  # slug suffix -> (label, property type, other filters)
    'condos-for-sale': ('Condos', 'Apartment/Condo', '(none)'), 'townhomes-for-sale': ('Townhomes', 'Townhouse', '(none)'),
    'acreages-for-sale': ('Acreages', '(none: leave the type open)', 'Lot size 1 acre or more'), 'lots-land': ('Lots and Land', 'Land Only (vacant land)', '(none)'),
    'mobile-homes-for-sale': ('Mobile Homes', 'Manufactured / Mobile', '(none)'),
}
ALLRES = '(none: leave the type open, so every residential type shows)'
HUBS = {'burnaby-neighbourhood-guides': 'burnaby', 'coquitlam-neighbourhood-guides': 'coquitlam', 'new-westminster-neighbourhood-guides': 'new-westminster',
        'richmond-neighbourhood-guides': 'richmond', 'vancouver-neighbourhood-guides': 'vancouver'}
HUBAREA = {'burnaby': ('Burnaby', 'Burnaby North + Burnaby South + Burnaby East'), 'coquitlam': ('Coquitlam', 'Coquitlam'), 'new-westminster': ('New Westminster', 'New Westminster'),
           'richmond': ('Richmond', 'Richmond'), 'vancouver': ('Vancouver', 'Vancouver West + Vancouver East')}
SUB = {  # pages that sit on one board sub-area, from the subarea map
    'brentwood-park-condos-for-sale': ('Brentwood Park Condos', 'Burnaby North', 'Brentwood Park', 'Apartment/Condo'),
    'brentwood-park-townhomes-for-sale': ('Brentwood Park Townhomes', 'Burnaby North', 'Brentwood Park', 'Townhouse'),
    'cariboo-condos-for-sale': ('Cariboo Condos', 'Burnaby North', 'Cariboo', 'Apartment/Condo'),
    'edmonds-condos-for-sale': ('Edmonds Condos', 'Burnaby East', 'Edmonds BE', 'Apartment/Condo'),
}
GUIDE = {  # slug -> (name, MLS area, sub-area, type, other, note)
    'barnston-island-surrey-guide': ('Barnston Island', 'Surrey + North Surrey', '(none)', ALLRES, 'Keyword “Barnston Island” in the listing remarks', 'If the board has a Barnston Island sub-area, use that instead of the keyword.'),
    'brunette-new-westminster-guide': ('Brunette', 'New Westminster', 'Brunette (if the sub-area list has it)', ALLRES, 'If there is no Brunette sub-area, keyword “Brunette” in the remarks', 'Check the sub-area spelling in the picker.'),
    'lindell-beach-bc-guide': ('Lindell Beach', 'Cultus Lake / Columbia Valley (pick the area Lindell Beach sits in)', '(none)', ALLRES, 'Keyword “Lindell Beach” in the listing remarks', 'Please confirm which board area Lindell Beach sits in.'),
    'mount-currie-bc-guide': ('Mount Currie', 'Pemberton (pick the area Mount Currie sits in)', '(none)', ALLRES, 'Keyword “Mount Currie” in the listing remarks', 'Please confirm the board area; tell me if MyRealPage has no listings feed for it.'),
    'mt-lehman-abbotsford-guide': ('Mt. Lehman', 'Abbotsford', 'Mt Lehman (if the sub-area list has it)', ALLRES, '(none)', 'Check the sub-area spelling in the picker.'),
    'real-estate-lawyer-notary-fees-langley-surrey-white-rock': ('Langley, Surrey and White Rock Homes', 'Langley + Surrey + North Surrey + South Surrey White Rock', '(none)', ALLRES, '(none)', 'A wide search; the page is about legal fees, so the box only shows what is on the market.'),
}
RULES = {  # BC-wide rules guides: lowest priority, see Notes
    'bc-55-plus-strata-rules': ('BC 55+ Strata', 'Surrey + North Surrey + Langley + Abbotsford + Chilliwack + Maple Ridge + Mission', '(none)', 'Apartment/Condo + Townhouse', 'Age restricted / 55+ (use the same filter as the 55+ city searches)'),
    'bc-acreage-buying-rules': ('BC Acreage', 'Langley + Surrey + Abbotsford + Chilliwack + Maple Ridge + Mission', '(none)', '(none: leave the type open)', 'Lot size 1 acre or more'),
    'bc-condo-buying-rules': ('BC Condos', 'Surrey + North Surrey + Langley + Burnaby North + Burnaby South + Burnaby East + Richmond + Vancouver West + Vancouver East', '(none)', 'Apartment/Condo', '(none)'),
    'bc-townhome-buying-rules': ('BC Townhomes', 'Surrey + North Surrey + Langley + Burnaby North + Burnaby South + Burnaby East + Richmond + Coquitlam', '(none)', 'Townhouse', '(none)'),
    'bc-land-buying-rules': ('BC Land', 'Langley + Surrey + Abbotsford + Chilliwack + Maple Ridge + Mission', '(none)', 'Land Only (vacant land)', '(none)'),
    'bc-duplex-half-duplex-buying-rules': ('BC Duplexes', 'Surrey + North Surrey + Langley + Abbotsford + Burnaby North + Burnaby South + Burnaby East', '(none)', 'Duplex + 1/2 Duplex', '(none)'),
    'bc-mobile-home-buying-rules': ('BC Mobile Homes', 'Surrey + North Surrey + Langley + Abbotsford + Maple Ridge + Mission', '(none)', 'Manufactured / Mobile', '(none)'),
}

def h1(slug):
    j = json.load(open(os.path.join(ROOT, 'src/data/local', slug + '.json')))
    return (j.get('new_page') or {}).get('h1') or (SEO.get(slug) or {}).get('h1') or slug

def row(slug, name, area, sub, typ, other, note='', price='(none)'):
    return [slug, h1(slug), f'https://jaredgibbons.ca/{slug}.html', name, area, sub, typ, other, price, 'Active', None, None, note]

pages, hubs, rules, skipped = [], [], [], []
for r in sorted(HELD, key=lambda r: (r['Group'], r['Slug'])):
    s = r['Slug']
    if s in HUBS:
        nm, area = HUBAREA[HUBS[s]]; hubs.append(row(s, f'HUB {nm} All Homes', area, '(none)', ALLRES, '(none)', 'Whole-city search for the neighbourhood guide hub.'))
    elif s in SUB:
        nm, area, sub, typ = SUB[s]; pages.append(row(s, f'AREA {nm}', area, sub, typ, '(none)'))
    elif s in GUIDE:
        nm, area, sub, typ, other, note = GUIDE[s]; pages.append(row(s, f'AREA {nm}', area, sub, typ, other, note))
    elif s in RULES:
        nm, area, sub, typ, other = RULES[s]; rules.append(row(s, f'GUIDE {nm}', area, sub, typ, other, 'Rules guide: lowest priority. A broad search that shows what is on the market in the places we cover.'))
    elif s in INV:
        b, sa = INV[s].split('|'); disp = GV.disp(INV[s]) if hasattr(GV, 'disp') else sa
        pages.append(row(s, f'AREA {disp}', b, sa, ALLRES, '(none)'))
    else:
        for pre, (cn, area, sub) in sorted(CITY.items(), key=lambda x: -len(x[0])):
            if s.startswith(pre + '-'):
                suf = s[len(pre) + 1:]
                if suf in TYPES:
                    lab, typ, other = TYPES[suf]
                    pages.append(row(s, f'TYPE {cn} {lab}', area, sub, typ, other)); break
        else: skipped.append(s)
assert not skipped, skipped
assert len(pages) + len(hubs) + len(rules) == len(HELD) == 77, (len(pages), len(hubs), len(rules), len(HELD))

HEAD = ['Page slug', 'Page heading', 'Page URL', 'Search name to save in MyRealPage', 'MLS area', 'Sub-area filter', 'Property type (Type of Dwelling)', 'Other filters', 'Price filter', 'Status', 'Search ID (Jerry fills)', 'Embed code (Jerry fills)', 'Notes']
wb = openpyxl.Workbook()
def sheet(ws, title, rows):
    ws.title = title; ws.append(HEAD)
    for r in rows: ws.append(r)
    for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='222222'); c.alignment = Alignment(wrap_text=True, vertical='top')
    for col, w in zip('ABCDEFGHIJKLM', (34, 40, 44, 34, 34, 30, 28, 34, 12, 9, 16, 30, 50)): ws.column_dimensions[col].width = w
    ws.freeze_panes = 'D2'
sheet(wb.active, f'Page searches ({len(pages)})', pages)
sheet(wb.create_sheet(), f'Hub searches ({len(hubs)})', hubs)
sheet(wb.create_sheet(), f'BC rules guides ({len(rules)})', rules)
ws = wb.create_sheet('Embed fixes (5)')
ws.append(['Embed line', 'What it was', 'Status', 'What Jerry needs to do'])
for r in [
    ('Fort Langley (1449924)', 'Worksheet also lists the old address /fort-langley.html', 'Fine already: the search is on /fort-langley-guide.html', 'Nothing'),
    ('Langley Poultry Farms for Sale (1450214)', 'Page had no listings box', 'Fixed by Claude 2026-11-08: box added, search wired', 'Nothing'),
    ('Pitt Meadows 55+ Condos for Sale (1450291)', 'Page had no listings box', 'Fixed by Claude 2026-11-08: box added, search wired', 'Nothing'),
    ('Mission BC (1450251), new-construction-mission-bc', 'Extra address for a page not on the new site', 'Fine already: the search is on /mission-bc-mission-guide.html', 'Nothing'),
    ('Salmon River Condos & Townhomes (395-job sheet)', 'Page is not on the new site yet', 'Held until the page goes live', 'Nothing'),
]: ws.append(list(r))
for c in ws[1]: c.font = Font(bold=True)
for col, w in zip('ABCD', (48, 52, 58, 20)): ws.column_dimensions[col].width = w
ws = wb.create_sheet('Notes')
for t in ['One saved MyRealPage search per row, noframe template, Status Active, then send back the Search ID and the embed code (same as the earlier sheets).',
          f'Page searches ({len(pages)}): city and type pages (condos, townhomes, acreages, lots and land, mobile homes), the Richmond and Vancouver neighbourhood pages, the Burnaby sub-area pages and the area guides. The MLS area strings match the ones already used on the other sheets.',
          f'Hub searches ({len(hubs)}): whole-city searches for the Burnaby, Coquitlam, New Westminster, Richmond and Vancouver neighbourhood guide hubs. Leave the type open.',
          f'BC rules guides ({len(rules)}): lowest priority. They are provincial rules pages, so each gets one broad search. If you would rather skip them, say so and Claude will take the listings box off those pages instead.',
          'Sub-area names are the board’s own labels (for example “Renfrew VE”, “Hamilton RI”). Where a row says “if the sub-area list has it”, check the spelling in the picker and use a keyword in the remarks if there is no such sub-area.',
          'Do not build searches for the 20 price-band pages here; they are on their own sheet (price-band-searches-2026-11-07).']: ws.append([t])
ws.column_dimensions['A'].width = 150
wb.save(OUT); print(OUT, len(pages), len(hubs), len(rules))
