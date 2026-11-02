"""Writes src/data/local/seller-net-proceeds-calculator.json. The calculator (src/components/NetProceedsCalc.astro) has no built-in
rates: commission, legal and closing costs are typed in by the visitor. Jared has not supplied his figures, so none are published (D-68).
python3 -I tools/build_calculator_page.py"""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
G = 'calc'
H = lambda t, l=2: {'t': 'h', 'level': l, 'text': t, 'gen': G}
P = lambda t: {'t': 'p', 'text': t, 'gen': G}
LINKS = [('Lawyer and notary fees in Langley, Surrey and White Rock', '/real-estate-lawyer-notary-fees-langley-surrey-white-rock.html'), ('Free home evaluation', '/home-evaluation.html'), ('Selling your home', '/selling.html'), ('FAQ for home sellers in BC', '/faq-for-home-sellers.html'), ('Data and methodology', '/data-and-methodology.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('Contact Jared', '/contact.html')]
blocks = [
 P('Selling a home is more than the sale price. The mortgage payout, commission, legal fees and other costs all come off before you receive anything. This calculator adds up what you tell it and shows what you would be left with. The figures come from you: your listing agreement, your lender’s payout statement and your lawyer’s or notary’s estimate.'),
 H('Estimate what you would walk away with'),
 {'t': 'calc', 'gen': G},
 H('What each line means'),
 {'t': 'table', 'caption': 'Lines in the net-proceeds estimate', 'head': ['Line', 'What it is', 'Where to find the figure'], 'rows': [
   ['Sale price', 'The price you expect to sell for.', 'Your own expectation, or a comparable-sales review from Jared.'],
   ['Mortgage and debts', 'What you still owe that must be paid out when the sale completes.', 'Your lender’s payout statement.'],
   ['Commission', 'The fee to the listing and selling brokerages, entered as a percentage of the sale price.', 'Your listing agreement. Commission is negotiable.'],
   ['Tax on commission', 'Sales tax charged on the commission, if it is not already in the percentage.', 'Your listing agreement or the brokerage’s statement.'],
   ['Legal or notary fees', 'Your lawyer’s or notary’s fee and disbursements for the sale.', 'Their written estimate. Published fees are on the lawyer and notary fees page.'],
   ['Prepayment penalty or discharge fee', 'What your lender charges if the mortgage is closed before its term ends.', 'Your lender.'],
   ['Adjustments owed', 'Property tax, utilities and strata costs that are split between seller and buyer at the completion date.', 'The statement of adjustments your lawyer or notary prepares.'],
   ['Other costs', 'Staging, repairs, cleaning, moving, advertising and similar costs.', 'Quotes you have received.'],
 ], 'gen': G},
 H('Related pages'),
 {'t': 'list', 'items': [[{'t': t, 'h': h}] for t, h in LINKS], 'gen': G},
 H('What this estimate leaves out'),
 P('It does not include income tax or capital gains tax. A home that has been your principal residence is often exempt from capital gains tax, but that depends on your situation, so ask an accountant. It also does not model a purchase that completes on a different date from your sale, bridge financing, a seller credit to the buyer or a price that changes after offers. Treat the result as a planning number and ask Jared to walk through it with the real figures once you are ready to list.'),
]
faq = [
 {'q': 'How much will I walk away with after selling my home?', 'a': 'Take the sale price and subtract your mortgage payout, the commission and any tax on it, legal or notary fees, any prepayment penalty, the adjustments you owe and other costs of selling. The calculator above does that with the figures you enter.'},
 {'q': 'What commission rate does the calculator use?', 'a': 'None. Commission is negotiable and set in your listing agreement, so you type in the percentage that applies to you. The calculator has no built-in rates.'},
 {'q': 'Are my numbers saved or sent anywhere?', 'a': 'No. The calculation runs in your browser, and nothing you type is sent to Jared or stored.'},
 {'q': 'Does the estimate include income tax or capital gains tax?', 'a': 'No. Whether tax applies depends on your situation, for example whether the home was your principal residence, so ask an accountant.'},
 {'q': 'Can Jared give me a number for my own home?', 'a': 'Yes. Jared can review comparable sales for your address and go through the costs with you. Start with the free home evaluation.'},
]
d = {'status': 'draft', 'slug': 'seller-net-proceeds-calculator', 'updated': '2026-11-01', 'blocks': blocks, 'faq': faq, 'hand_edited': True,
     'new_page': {'title': 'Seller Net Proceeds Calculator | Jared Gibbons', 'description': 'Estimate what you would walk away with after selling your BC home: enter sale price, mortgage payout, commission, legal and other costs. Nothing is saved or sent.', 'h1': 'Seller Net Proceeds Calculator'},
     'breadcrumbs': [{'name': 'Home', 'href': '/index.html'}, {'name': 'Seller net proceeds calculator', 'href': '/seller-net-proceeds-calculator.html'}],
     'needs_from_muse': ['Jared’s commission, legal and other closing-cost figures if he wants example costs shown (none are published until he supplies them)', 'Whether to add the calculator to the sellers menu and home evaluation page']}
json.dump(d, open(os.path.join(ROOT, 'src/data/local/seller-net-proceeds-calculator.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote calculator page')

# link the calculator from the seller pages (own block, rebuilt each run)
for slug in ('home-evaluation', 'faq-for-home-sellers', 'selling'):
    f = os.path.join(ROOT, 'src/data/local', slug + '.json')
    if not os.path.exists(f): j = {'status': 'generated', 'slug': slug, 'updated': '2026-11-01', 'blocks': []}
    else: j = json.load(open(f, encoding='utf-8'))
    j['blocks'] = [b for b in j.get('blocks', []) if b.get('gen') != 'calclink']
    j['blocks'].append({'t': 'p', 'text': 'Seller net proceeds calculator: estimate what you would walk away with', 'h': '/seller-net-proceeds-calculator.html', 'pos': 'end', 'gen': 'calclink'})
    json.dump(j, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('linked from seller pages')
