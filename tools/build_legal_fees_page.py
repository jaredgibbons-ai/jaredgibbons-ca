"""Writes src/data/local/real-estate-lawyer-notary-fees-langley-surrey-white-rock.json from the fee survey of 2026-11-02
(docs/research/legal-fees-2026-11-02.md). Only prices a firm publishes on its own website are used; directory and third-party ranges are not.
Averages are not published (2 to 4 firms is too few); the page shows each firm's own figures and the low-high range per area.   python3 -I tools/build_legal_fees_page.py"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SLUG = 'real-estate-lawyer-notary-fees-langley-surrey-white-rock'
G = 'legalfees'
H = lambda t, l=2: {'t': 'h', 'level': l, 'text': t, 'gen': G}
P = lambda t: {'t': 'p', 'text': t, 'gen': G}
def T(cap, head, rows, src=None): return {'t': 'table', 'caption': cap, 'head': head, 'rows': rows, **({'source': src} if src else {}), 'gen': G}
def LI(items): return {'t': 'list', 'items': [[{'t': i}] for i in items], 'gen': G}
def LK(items): return {'t': 'list', 'items': [[{'t': a, 'h': h}] for a, h in items], 'gen': G}

blocks = [
 {'t': 'notice', 'text': 'Draft for Jared\'s approval. Every price below is one a firm publishes on its own website, read on November 2, 2026. Fees change; get a written quote before you hire anyone.', 'gen': G},
 P('Almost no notary or lawyer in Langley, Surrey, South Surrey or White Rock puts a conveyancing price on their website, so most buyers and sellers cannot compare before they call. This page collects the prices that are published, says exactly what each one covers, and shows what is missing. It is not legal advice, and naming a firm here is not a recommendation: these are simply the firms that publish a price.'),
 {'t': 'grid', 'gen': G},
 H('What we found'),
 LI(['We checked the websites of 21 conveyancing firms in Langley, 36 in Surrey and 15 in South Surrey and White Rock. Only six distinct firms publish any price at all, and one of them has offices in both Langley and Surrey.',
     'Langley: three firms publish a price, and two of them publish a usable fee schedule. Surrey: four firms publish something, and three have a fee schedule.',
     'South Surrey and White Rock: none of the 15 firms publishes its own price. Every one quotes by phone.',
     'Notaries: not one notary in the three areas publishes a conveyancing fee schedule. Every usable price came from a law firm.']),
 H('Published legal fees by area'),
 P('These are the legal fee only, before taxes and disbursements, for the standard job: a purchase with a mortgage, a sale with one mortgage discharge, and a refinance with one payout. The range runs from the lowest to the highest firm that publishes the figure. With only two or three firms in each area, treat it as a guide to the order of magnitude, not an average.'),
 T('Published legal fee only, by area (before taxes and disbursements)', ['Job', 'Langley', 'Surrey', 'South Surrey and White Rock'], [
   ['Purchase with a mortgage', '$995 to $1,095 (2 firms)', '$995 to $1,475 (3 firms)', 'No firm publishes'],
   ['Purchase, cash', '$795 to $995 (2 firms)', '$795 to $1,300 (2 firms)', 'No firm publishes'],
   ['Sale with one mortgage discharge', '$795 to $995 (2 firms)', '$795 to $1,200 (3 firms)', 'No firm publishes'],
   ['Sale, clear title', '$645 to $895 (2 firms)', '$645 to $1,050 (2 firms)', 'No firm publishes'],
   ['Refinance, one payout', '$845 to $1,025 (2 firms)', '$845 to $1,350 (3 firms)', 'No firm publishes'],
 ], 'Source: each firm\'s own website, read November 2, 2026. One firm has offices in both Langley and Surrey and appears in both columns. Several figures are "from" prices.'),
 H('Each firm\'s published fees'),
 T('Law firms that publish a fee schedule (legal fee only, before taxes and disbursements)', ['Firm', 'Office', 'Purchase with mortgage', 'Sale with one discharge', 'Refinance', 'Notes'], [
   ['Alpine Legal Services', 'Langley and Surrey', '$995', '$795', '$845', 'Price sheet dated January 2026; fees unchanged since September 2022. Plus $100 for each extra discharge on a refinance.'],
   ['Peak Law Group', 'Langley (by appointment)', '$1,095', '$995', '$1,025', 'Also publishes an approximate all-in column (below). No date on the page.'],
   ['Raj Dhillon and Associates', 'Surrey (Newton)', 'From $1,050', 'From $950', 'From $950', 'Starting fees; taxes, registration, searches and other disbursements are extra. Each extra payout from $150.'],
   ['LeBeau Law Corporation', 'Signing hours in Cloverdale', 'From $1,475', 'From $1,200', 'From $1,350', 'Price list dated July 2024, so it may be out of date. Transactions over $1,000,000 add $100; some lenders add $100 to $400.'],
 ], 'Source: the firms\' own price pages and price sheets, read November 2, 2026.'),
 H('What a client pays all-in'),
 P('Only one firm, Peak Law Group in Langley, prints an all-in figure. Its page says the all-in column includes disbursements, taxes and Land Title Office registration costs, and leaves out third-party charges such as insurance binders and strata forms. Property Transfer Tax is not part of any figure on this page.'),
 T('Peak Law Group: legal fee and approximate all-in', ['Job', 'Legal fee', 'Approximate all-in'], [
   ['Purchase with one mortgage', '$1,095', '$1,772'], ['Purchase, cash', '$995', '$1,577'], ['Sale with one mortgage discharge', '$995', '$1,485'], ['Sale, clear title', '$895', '$1,333'], ['Refinance, one discharge', '$1,025', '$1,633'],
 ], 'Source: Peak Law Group pricing page, read November 2, 2026.'),
 P('LeBeau Law Corporation prints its tax and an estimated standard disbursement beside each fee. For a purchase with a mortgage, the printed $1,475 fee, $177 tax and about $270 of disbursements add to about $1,922. For a refinance, $1,350, $162 and about $230 add to about $1,742. Those totals are our addition of the firm\'s own printed amounts, not figures the firm states, and the list is dated July 2024.'),
 H('Other prices that are not a firm\'s fee schedule'),
 LI(['Spagnuolo LLP says to budget approximately $1,600 for a purchase with a mortgage and $1,200 for a sale (homes or mortgages under $2,000,000), and says third-party charges of a further $750 to $1,000 are not included. Its page does not split the legal fee from the firm\'s own disbursements, so we did not put it in the fee tables.',
     'Zancope Notary Public in Langley shows "prices starting from $1,220" for real estate. The page does not say whether that includes taxes or disbursements and does not split purchase, sale and refinance, so it is not in the tables.',
     'Pacific Point Law in South Surrey does not publish its own fee. Its real estate FAQ describes the general BC market as roughly $1,300 to $2,100 for a purchase with a mortgage and $1,000 to $1,600 for a straightforward sale, plus disbursements, and says it quotes its own fee at consultation.']),
 H('What is not in the legal fee'),
 LI(['Disbursements: Land Title Office registration charges, tax certificates, title searches, courier costs, title insurance and the strata documents for a condo or townhome. The firms that list them price them separately from the fee.',
     'Taxes on the fee, which the fee-only figures above leave out.',
     'Property Transfer Tax on a purchase, which is paid on top of everything on this page.',
     'Extras that raise the price: each additional mortgage discharge, new construction, a purchase price over a firm\'s threshold, and some lenders\' requirements.']),
 H('How to compare quotes'),
 LI(['Ask for the fee, the taxes and the disbursements as three separate numbers, in writing, for your exact transaction.',
     'Ask what changes the price: a second mortgage, a strata property, a new build, a price over $1,000,000 or $2,000,000.',
     'A BC notary public or a lawyer can handle a residential purchase or sale. Because no notary in these areas publishes a price, you cannot compare notary and lawyer fees from websites; phone two or three of each.',
     'In South Surrey and White Rock, where nobody publishes a price, a written quote from at least two firms is the only benchmark you will get.']),
 H('Sources'),
 P('Prices were read on each firm\'s own website on November 2, 2026. Directory and review-site price ranges were not used.'),
 LK([('Alpine Legal Services: real estate pricing sheet, January 2026', 'https://alpinelawyers.com/wp-content/uploads/2026/02/Real-Estate-Pricing-Jan.-2026-Updated.pdf'),
     ('Peak Law Group: pricing', 'https://www.peaklaw.ca/pricing'),
     ('Raj Dhillon and Associates: real estate lawyer Surrey', 'https://www.rajdhillonlaw.ca/real-estate-lawyer-surrey.html'),
     ('LeBeau Law Corporation: price list, July 2024', 'https://lebeaulaw.ca/wp-content/uploads/2024/06/2024-07-Lebeau-Price-List.pdf'),
     ('Spagnuolo LLP: our prices', 'https://bcrealestatelawyers.com/pricing/our-prices/'),
     ('Zancope Notary Public: our services', 'https://www.zancopenotary.com/our-services/'),
     ('Pacific Point Law: real estate', 'https://www.pacificpointlaw.ca/services/real-estate')]),
 {**H('More on selling and buying costs'), 'pos': 'end'},
 {**LK([('Seller net proceeds calculator', '/seller-net-proceeds-calculator.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Data and methodology', '/data-and-methodology.html'), ('Free home evaluation', '/home-evaluation.html'), ('Contact Jared', '/contact.html')]), 'pos': 'end'},
]
faq = [
 {'q': 'How much are legal fees to buy a house in Langley or Surrey?', 'a': 'Among the firms that publish a price, the legal fee for a purchase with a mortgage runs from $995 to $1,095 in Langley and from $995 to $1,475 in Surrey, before taxes and disbursements. A cash purchase is lower, from $795. The one firm that publishes an all-in figure puts a purchase with a mortgage at about $1,772.'},
 {'q': 'How much are legal fees to sell a house in Langley or Surrey?', 'a': 'For a sale that needs one mortgage discharged, published legal fees run from $795 to $995 in Langley and from $795 to $1,200 in Surrey, before taxes and disbursements. With a clear title they start at $645. The one firm that publishes an all-in total puts a sale with a discharge at about $1,485.'},
 {'q': 'What do lawyers and notaries charge in South Surrey and White Rock?', 'a': 'Nobody can say from a website, because none of the 15 firms we checked publishes its own price. One South Surrey firm\'s FAQ describes the general BC market as roughly $1,300 to $2,100 to buy with a mortgage and $1,000 to $1,600 to sell, plus disbursements. Get written quotes from two or three firms.'},
 {'q': 'Are notaries cheaper than lawyers for a home purchase?', 'a': 'We cannot tell from published prices. No notary in Langley, Surrey, South Surrey or White Rock publishes a conveyancing fee schedule, so there is nothing to compare. The only notary figure found was a "starting from" line with no stated basis.'},
 {'q': 'Does the legal fee include Property Transfer Tax?', 'a': 'No. Property Transfer Tax is paid on a purchase on top of the legal fee, taxes and disbursements, and it is not part of any figure on this page.'},
 {'q': 'What is the difference between a legal fee and disbursements?', 'a': 'The legal fee is what the lawyer or notary charges for the work. Disbursements are costs they pay to others on your behalf, such as Land Title Office registration, tax certificates, searches, title insurance and strata documents, and they are billed on top of the fee.'},
 {'q': 'How current are these prices?', 'a': 'They were read on each firm\'s own website on November 2, 2026. One price list is dated July 2024 and may be out of date, one sheet is dated January 2026, and one page carries no date. Confirm any figure with the firm.'},
]
d = {'status': 'draft', 'slug': SLUG, 'updated': '2026-11-02', 'blocks': blocks, 'faq': faq, 'faq_heading': 'Real estate lawyer and notary fees: your questions answered', 'hand_edited': True,
     'new_page': {'title': 'Real Estate Lawyer & Notary Fees: Langley, Surrey, White Rock', 'description': 'What lawyers and notaries publish for buying, selling and refinancing in Langley, Surrey, South Surrey and White Rock: fees, all-in costs, and what is missing.', 'h1': 'Real Estate Lawyer and Notary Fees in Langley, Surrey and White Rock'},
     'breadcrumbs': [{'name': 'Home', 'href': '/'}, {'name': 'Selling', 'href': '/selling.html'}, {'name': 'Lawyer and notary fees', 'href': f'/{SLUG}.html'}],
     'needs_from_muse': ['Jared\'s view on which lawyers or notaries he recommends and what clients usually pay', 'Fresh quotes if he wants South Surrey and White Rock covered']}
json.dump(d, open(os.path.join(ROOT, f'src/data/local/{SLUG}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', SLUG)
