"""Rewrite research-note wording that reached public pages (D-367). Idempotent: each rule only matches the old wording."""
import glob, re
R = [
 (r'are listing-stated for one home on one date, not a park tariff', 'come from one listing on one date, not a park\'s posted rates'),
 (r'solid enough to print as listing-stated, not a substitute', 'a useful guide, not a substitute'),
 (r'and listing-stated only:', 'and comes from listings only:'),
 (r'listing-stated figures are \$', 'figures from listings are $'),
 (r'listing-stated figures are per-home and dated', 'figures in listings are per home and dated'),
 (r'listing-stated figures for individual units', 'figures from listings for individual units'),
 (r'Those dollar figures are listing-stated for specific homes', 'Those dollar figures come from listings for specific homes'),
 (r'(they are|it is) listing-stated, not a published tariff', r'\1 from a listing, not a published rate'),
 (r'with listing-stated terms', 'with terms stated in the listing'),
 (r'listing-stated building history', 'building history from the listing'),
 (r'\(listing-stated builder claim\)', '(builder named in the listing)'),
 (r'\(listing-stated expiry (\d{4}) with an option to extend\)', r'(expiry \1 with an option to extend, per the listing)'),
 (r'a listing-stated lease expiry of (\d{4}) plus an option to extend', r'a lease expiry of \1 plus an option to extend, per the listing'),
 (r'listing-stated lease expiry (\d{4}) plus an option to extend', r'lease expiry \1 plus an option to extend, per the listing'),
 (r'with listing-stated pad rents from', 'with pad rents in listings from'),
 (r'the listing-stated 55\+ rule', 'the 55+ rule in the listing'),
 (r'listing-stated 55\+\)', '55+ per the listing)'),
 (r'listing-stated no age restrictions', 'no age restrictions per the listing'),
 (r'a listing-stated monthly pad rent of (\$[\d,.]+)', r'a monthly pad rent of \1 in the listing'),
 (r'\(listing-stated \$', '(per the listing, $'),
 (r'a listing-stated figure for that one home', 'a figure for that one home'),
 (r'\(listing-stated figures\)', '(figures from listings)'),
 (r'These are listing-stated figures', 'These figures come from listings'),
 (r'All figures and rules are listing-stated', 'All figures and rules come from listings'),
 (r'All figures are listing-stated', 'All figures come from listings'),
 (r'All listing-stated:', 'All from listings:'),
 (r'Pad rent is listing-stated per home', 'Pad rent varies by home in listings'),
 (r'Treat every one of those as listing-stated for that home and date', 'Treat each one as true for that home and date only'),
 (r'Treat it as listing-stated and trace', 'Treat it as the listing\'s description and trace'),
 (r'are listing-stated park rules to confirm', 'are park rules from listings, to confirm'),
 (r'phase years as listing-stated\)', 'phase years from listings)'),
 (r'a 20-unit \(listing-stated\), ', 'a 20-unit (per the listing) '),
 (r'\(listing-stated[;,] confirm', '(from the listing; confirm'),
 (r'\(listing-stated — confirm', '(from the listing — confirm'),
 (r'\(listing-stated\)', '(from the listing)'),
 (r', listing-stated\)', ', from the listing)'),
 (r'— listing-stated only([;.])', r'— from the listing only\1'),
 (r'— listing-stated[;,] (confirm|the filed)', r'— from the listing; \1'),
 (r'records pets not allowed \(no cats, no dogs\) — listing-stated;', 'records pets not allowed (no cats, no dogs), per the listing;'),
 # "on the record"
 (r', on the record\.', '.'),
 (r'Both, on the record:', 'Both:'),
 (r'is on the record from the owner\'s side', 'has been raised by the owner'),
 (r'Completion timing on the record read: TBA', 'Completion timing listed: TBA'),
 (r'No — on the records read it is', 'No — it is'),
 (r', on the record before it is built\.', ', before it is built.'),
 (r'protected character is on the record, and', 'protected character is set in that plan, and'),
 (r'Dike work on the record:', 'Dike work:'),
 (r'Strata on the record read —', 'Strata —'),
 (r'still a design, on the record:', 'still a design:'),
 (r'no presale lot offering on the record\.', 'no presale lot offering.'),
 # "listing text only"
 (r'in listing text only\.', 'only in a listing.'),
 (r'are listing text only —', 'come only from listings —'),
 (r'are listing text only\.', 'come only from listings.'),
 (r'is listing text only, not a City confirmation', 'comes from a listing, not the City'),
 (r'named in listing text only', 'named only in a listing'),
 (r'line is listing text only\)', 'line comes from a listing)'),
 (r'\(snapshot, listing text only\)', '(from listings at one point in time)'),
 (r'claim is listing text only\.', 'claim comes only from listings.'),
 (r'is a claim to verify against the City, not a fact\.', 'is a claim to verify with the City.'),
]
n = 0
for f in glob.glob('src/data/**/*.json', recursive=True):
    if 'explore' in f or 'lastmod' in f: continue
    s = open(f, encoding='utf-8').read(); s0 = s
    for a, b in R:
        s, k = re.subn(a, b, s); n += k
    if s != s0: open(f, 'w', encoding='utf-8').write(s)
print(n)
