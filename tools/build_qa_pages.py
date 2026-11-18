"""Short question-and-answer pages (D-357): one BC real estate question per page, answered in the first paragraph,
then the detail, a worked example where numbers help, sources and related guides. Plus a hub page that lists them.

Facts were read from the official pages listed under each page's Sources on November 18, 2026 (gov.bc.ca, canada.ca,
bcfsa.ca, bcassessment.ca). Re-run after editing: python3 tools/build_qa_pages.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'src', 'data', 'local')
READ = 'November 18, 2026'
HUB = 'bc-real-estate-questions'

def money(x): return f"${x:,.0f}"
def ptt(v):
    t = min(v, 200_000) * 0.01 + max(0, min(v, 2_000_000) - 200_000) * 0.02 + max(0, v - 2_000_000) * 0.03
    return t + max(0, v - 3_000_000) * 0.02          # further 2% on the residential value above $3M
def P(*parts):
    out = []
    for x in parts:
        out.append({'t': x[0], 'h': x[1]} if isinstance(x, tuple) else {'t': x})
    return {'t': 'p', 'parts': out}
H2 = lambda t: {'t': 'h', 'level': 2, 'text': t}
def L(*items): return {'t': 'list', 'items': [[{'t': i[0], 'h': i[1]}] if isinstance(i, tuple) else [{'t': i}] for i in items]}

# ---- worked numbers ----
EX = [600_000, 900_000, 1_400_000, 2_500_000, 3_500_000]
nb_partial = lambda v: ptt(v) * ((1_100_000 + 50_000 - v) / 50_000)

PAGES = [
 dict(slug='how-much-is-property-transfer-tax-in-bc',
  q='How much is property transfer tax in BC?',
  title='How Much Is Property Transfer Tax in BC? 2026 Rates & Examples',
  desc='BC property transfer tax is 1% of the first $200,000, 2% up to $2 million and 3% above, plus 2% on homes over $3 million. Worked examples inside.',
  answer=f'Property transfer tax in BC is 1% of the first $200,000 of the fair market value, 2% of the part from $200,000 to $2,000,000, and 3% of the part above $2,000,000. Homes over $3,000,000 pay a further 2% on the residential value above $3,000,000. On a {money(900_000)} home that is {money(ptt(900_000))}.',
  body=[
   H2('The rates'),
   L('1% on the first $200,000', '2% on the portion from $200,000 to $2,000,000', '3% on the portion above $2,000,000', 'A further 2% on the residential value above $3,000,000 (only the residential part of a mixed property)'),
   P('The tax is worked out on the fair market value on the day the transfer is registered at the Land Title Office. In an ordinary open-market sale that is the purchase price.'),
   H2('What it costs at common prices'),
   L(*[f'{money(v)} home: {money(ptt(v))}' for v in EX]),
   H2('Who pays it, and when'),
   P('The buyer pays it, as part of closing. Your lawyer or notary files the return and pays the tax when the transfer is registered, so you need it in cash on top of your down payment. Your mortgage does not cover it.'),
   H2('Ways to pay less'),
   P('First-time buyers can save up to $8,000 on homes up to $835,000 (fully exempt up to $500,000). Buyers of a newly built home that will be their home pay nothing up to $1,100,000. Foreign buyers pay an extra 20% in the Fraser Valley and Metro Vancouver.'),
  ],
  faq=[('Is property transfer tax paid on the assessed value?', 'No, on the fair market value at registration. For an ordinary sale that is the price you paid. BC Assessment values are used only for sales that are not on the open market, such as transfers between family.'),
       ('Can I add property transfer tax to my mortgage?', 'Generally no. It is a closing cost paid in cash through your lawyer or notary, so budget it with your down payment.')],
  src=[('www2.gov.bc.ca · Property transfer tax', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax')],
  rel=[('First-time buyer calculator (PTT, GST, FHSA)', '/first-time-buyer-calculator.html'), ('First-time home buyer programs in BC', '/first-time-home-buyer-program.html'), ('Mortgage calculator', '/mortgage-calculator.html')]),

 dict(slug='bc-newly-built-home-exemption',
  q='Is there property transfer tax on a new home in BC?',
  title='Property Transfer Tax on a New Home in BC: Newly Built Exemption',
  desc='A newly built home you will live in is exempt from BC property transfer tax up to $1,100,000, with a partial exemption up to $1,150,000. How it works.',
  answer='Usually not, if it will be your home. Since April 1, 2024 the newly built home exemption removes property transfer tax entirely on a new home with a fair market value up to $1,100,000, and partly up to $1,150,000. You do not have to be a first-time buyer.',
  body=[
   H2('How much you save'),
   L(f'{money(800_000)} new condo: saves {money(ptt(800_000))}', f'{money(1_100_000)} new townhouse: saves {money(ptt(1_100_000))}', f'{money(1_125_000)}: saves about {money(nb_partial(1_125_000))} (partial)', '$1,150,000 or more: no exemption'),
   P('Between $1,100,000 and $1,150,000 the exemption shrinks in a straight line to zero. If only one of two buyers qualifies, the exemption covers that buyer\'s share.'),
   H2('What counts'),
   P('The home must be newly built and used as your principal residence. Presale condos and townhomes bought from the builder are the common case in Surrey, Langley and South Surrey. Land over half a hectare (about 1.24 acres) is worked out differently: only the home and a share of the land count.'),
   H2('Also check the GST'),
   P('New homes carry 5% GST. First-time buyers can get up to $50,000 of it back on a new home under $1 million, with a partial rebate up to $1.5 million.', ('See the GST rebate guide.', '/gst-rebate-in-bc.html')),
  ],
  faq=[('Do I have to be a first-time buyer for the new home exemption?', 'No. Any buyer who will live in the newly built home as their principal residence can qualify, if they meet the other requirements.'),
       ('Does it apply to a presale assignment?', 'Ask your lawyer or notary before you sign. An assignment changes who registers the home and when, which affects both this exemption and the home flipping tax.')],
  src=[('www2.gov.bc.ca · Newly built home exemption amounts', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/exemptions/newly-built-home-exemption/exemption-amounts')],
  rel=[('Presale projects in the Fraser Valley and Metro Vancouver', '/presale-projects-fraser-valley-and-metro-vancouver.html'), ('South Surrey new construction and presales', '/south-surrey-new-construction-presales.html'), ('First-time buyer GST rebate in BC', '/gst-rebate-in-bc.html')]),

 dict(slug='bc-home-flipping-tax',
  q='What is the BC home flipping tax?',
  title='BC Home Flipping Tax: 20% on Sales Within 2 Years (2026 Guide)',
  desc='Sell a BC home or presale contract within two years and the home flipping tax may apply: 20% of the profit inside 365 days, falling to zero at 730 days.',
  answer='Since January 1, 2025, BC taxes the profit when you sell a home, or assign a presale contract, that you owned for less than 730 days. The rate is 20% of the profit if you sell within 365 days, then it falls gradually to zero at 730 days. It is a separate return, usually due within 90 days of the sale.',
  body=[
   H2('What it applies to'),
   P('Residential property in BC, and the right to buy it, which includes presale contracts. The clock runs from the day you acquired it to the day you sell or assign it.'),
   H2('Exemptions and the principal residence deduction'),
   P('Some life events can exempt a sale, and some exemptions need a return to be filed. If the home was your principal residence and you owned it at least 365 days in a row, up to $20,000 of the profit can be deducted. That deduction is not available when you assign a presale.'),
   H2('Filing'),
   P('The flipping tax return is separate from your income tax return. If the tax applies, or an exemption needs a return, you generally file within 90 days of the sale. The federal anti-flipping rule (profit taxed as business income if you sell within 365 days) is separate and can apply as well.'),
   H2('Before you buy to sell'),
   P('If you might sell within two years, for a move, a presale assignment or a renovation project, plan the dates with your accountant before you buy. Selling on day 731 instead of day 700 can change the bill.'),
  ],
  faq=[('Does the BC flipping tax apply if I owned the home for over two years?', 'No. It applies only when you owned it for less than 730 days.'),
       ('Does it apply to presale assignments?', 'Yes. A presale contract is a right to acquire residential property, so assigning it within 730 days of signing can be taxed.')],
  src=[('www2.gov.bc.ca · BC home flipping tax', 'https://www2.gov.bc.ca/gov/content/taxes/income-taxes/bc-home-flipping-tax')],
  rel=[('Presale projects in the Fraser Valley and Metro Vancouver', '/presale-projects-fraser-valley-and-metro-vancouver.html'), ('Seller net proceeds calculator', '/seller-net-proceeds-calculator.html'), ('FAQ for home sellers', '/faq-for-home-sellers.html')]),

 dict(slug='speculation-and-vacancy-tax-surrey-langley',
  q='Does the speculation and vacancy tax apply in Surrey, Langley and the Fraser Valley?',
  title='Speculation and Vacancy Tax in Surrey, Langley & Fraser Valley (2026)',
  desc='Surrey, White Rock, both Langleys, Abbotsford, Chilliwack and Mission are taxable areas. 2026 rates are 1% for Canadians and 3% for foreign owners.',
  answer='Yes. Surrey, White Rock, the City and Township of Langley, Delta, Maple Ridge, Pitt Meadows, Abbotsford, Chilliwack and Mission are all taxable areas. Every residential owner there must declare each year by March 31. Most owners who live in their home or rent it out are exempt, but they still have to declare.',
  body=[
   H2('2026 rates'),
   L('1% of assessed value: Canadian citizens and permanent residents', '3% of assessed value: foreign owners and untaxed worldwide earners (including satellite families)', 'From January 1, 2027 the foreign owner rate rises to 4%; the 1% rate stays'),
   P('For 2025 the rates were 0.5% and 2%. Tax for a calendar year is due the following July.'),
   H2('The two common exemptions'),
   L('Principal residence: an owner who lives and works in BC and lives in the home', 'Rented: a tenant occupies the home for at least six months of the calendar year'),
   P('A second home or a condo left empty most of the year is where owners get caught. Check before you buy a second property in a taxable area.'),
   H2('Every taxable area near you'),
   P('Fraser Valley: Abbotsford, Chilliwack and Mission. Metro Vancouver: Burnaby, Coquitlam, Delta, Langley City, Township of Langley, Maple Ridge, New Westminster, North Vancouver (City and District), Pitt Meadows, Port Coquitlam, Port Moody, Richmond, Surrey, Vancouver, West Vancouver, White Rock, Anmore, Belcarra, UBC and the University Endowment Lands.'),
  ],
  faq=[('Do I have to declare if I live in my home?', 'Yes. Every owner of residential property in a taxable area declares every year, even when the home is exempt. You can declare once you receive the letter the Province mails.'),
       ('Is the speculation tax the same as Vancouver\'s empty homes tax?', 'No. The empty homes tax is the City of Vancouver\'s own tax. The speculation and vacancy tax is provincial and covers all the areas listed here.')],
  src=[('www2.gov.bc.ca · Taxable areas', 'https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax/how-tax-works/taxable-areas'), ('www2.gov.bc.ca · Tax rates', 'https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax/how-tax-works/tax-rates'), ('www2.gov.bc.ca · Exemptions for individuals', 'https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax/exemptions-speculation-and-vacancy-tax/individuals')],
  rel=[('2026 speculation tax guide for South Surrey owners', '/blog.html/2026-bc-speculation-tax-guide-for-south-surrey-owners-8918934'), ('BC landlord and tenant resources', '/bc-landlord-tenant-resources.html'), ('FAQ for home buyers', '/faq-for-home-buyers-in-bc.html')]),

 dict(slug='can-foreigners-buy-property-in-bc',
  q='Can foreigners buy a home in BC?',
  title='Can Foreigners Buy a Home in BC? Federal Ban & 20% Foreign Buyer Tax',
  desc='The federal ban on non-Canadians buying homes is set to end January 1, 2027. In the Fraser Valley and Metro Vancouver, foreign buyers also pay an extra 20% tax.',
  answer='For now, mostly not. A federal law bars most non-Canadians from buying residential property, and it is set to expire on January 1, 2027. On top of that, BC charges foreign buyers an additional 20% property transfer tax on residential property in the Fraser Valley and Metro Vancouver.',
  body=[
   H2('The federal ban'),
   P('The Prohibition on the Purchase of Residential Property by Non-Canadians Act took effect in 2023 and was extended to January 1, 2027. It has exceptions, for example for some temporary workers and for spouses of Canadians. Whether it is extended again was not announced when this page was checked, so confirm with a lawyer before you make plans.'),
   H2('BC\'s additional property transfer tax'),
   P(f'Foreign nationals, foreign corporations and taxable trustees pay 20% of the residential value, on top of the regular property transfer tax, in the Fraser Valley, Metro Vancouver, Capital, Central Okanagan and Nanaimo regional districts. On a {money(1_000_000)} home that is {money(200_000)} extra, plus {money(ptt(1_000_000))} of regular tax.'),
   H2('The yearly tax'),
   P('Foreign owners who keep a home in a taxable area also pay the speculation and vacancy tax: 3% of assessed value in 2026, rising to 4% in 2027, unless an exemption applies.'),
  ],
  faq=[('Do permanent residents pay the foreign buyer tax?', 'No. Canadian citizens and permanent residents do not pay the additional 20% tax.'),
       ('Does the foreign buyer tax apply to farmland?', 'The 20% tax applies to the residential portion of a property. Farmland has its own rules, covered in the farmland guide below.')],
  src=[('www2.gov.bc.ca · Additional property transfer tax', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/additional-property-transfer-tax'), ('www2.gov.bc.ca · Speculation and vacancy tax rates', 'https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax/how-tax-works/tax-rates')],
  rel=[('Can foreigners buy farmland in BC?', '/blog.html/can-foreigners-buy-farmland-in-bc-fraser-valley-rules-9186434'), ('How much is property transfer tax in BC?', '/how-much-is-property-transfer-tax-in-bc.html')]),

 dict(slug='fhsa-first-home-savings-account-bc',
  q='How does the FHSA work when you buy a home?',
  title='FHSA Explained for BC Home Buyers: $8,000 a Year, $40,000 Total',
  desc='The First Home Savings Account lets first-time buyers save $8,000 a year, $40,000 in total, with a tax deduction going in and no tax coming out.',
  answer='A First Home Savings Account (FHSA) lets a first-time buyer save up to $8,000 a year and $40,000 in total. Contributions are tax-deductible, growth is tax-free, and a qualifying withdrawal to buy your first home is not taxed. Two buyers can each have one, so a couple can bring $80,000 plus growth.',
  body=[
   H2('The limits'),
   L('$8,000 a year, starting the year you open it', 'Up to $8,000 of unused room carries to the next year', '$40,000 lifetime', 'Close it by December 31 of the year that comes first: the 15th anniversary of opening, the year you turn 71, or the year after your first qualifying withdrawal'),
   H2('Who can open one'),
   P('A Canadian resident aged 18 to 71 who is a first-time home buyer.'),
   H2('With the RRSP Home Buyers\' Plan'),
   P('You can use your FHSA and the Home Buyers\' Plan on the same purchase. Together a couple can have $80,000 of FHSA savings and $120,000 from RRSPs available for a down payment.', ('How the Home Buyers\' Plan works.', '/rrsp-home-buyers-plan-bc.html')),
   H2('If you don\'t buy'),
   P('You can move the balance to your RRSP or RRIF without tax and without using RRSP room.'),
  ],
  faq=[('Is the FHSA better than an RRSP for a down payment?', 'For a first home, usually yes: the deduction works like an RRSP but the withdrawal is not paid back. Many buyers use both.'),
       ('Can I open an FHSA if my spouse owns a home?', 'Check the CRA\'s first-time buyer definition before you open one: it looks at homes you or your spouse or common-law partner lived in and owned in recent years.')],
  src=[('canada.ca · First Home Savings Account tax tip', 'https://www.canada.ca/en/revenue-agency/news/newsroom/tax-tips/tax-tips-2023/saving-first-home-find-out-how-first-home-savings-account-can-help.html')],
  rel=[('First-time buyer calculator', '/first-time-buyer-calculator.html'), ('The FHSA and HBP stack for BC couples', '/blog.html/the-fhsa-hbp-stack-a-200000-down-payment-for-bc-couples-9150992'), ('First-time home buyer programs in BC', '/first-time-home-buyer-program.html')]),

 dict(slug='rrsp-home-buyers-plan-bc',
  q='How much can I take from my RRSP to buy a home?',
  title="RRSP Home Buyers' Plan: $60,000 Limit & When You Repay (2026)",
  desc="The Home Buyers' Plan lets first-time buyers take up to $60,000 from their RRSPs, tax-free, and repay it over 15 years. Repayments start in the fifth year.",
  answer="Up to $60,000 each under the Home Buyers' Plan (HBP), so $120,000 for a couple who both qualify. The withdrawal is not taxed, and you repay it to your RRSP over 15 years. For withdrawals made from 2022 to 2028, repayments start in the fifth year after the first withdrawal.",
  body=[
   H2('How it works'),
   P("You withdraw from your RRSPs to buy or build a qualifying home for yourself (or for a related person with a disability). Each year you repay at least one-fifteenth; anything you skip is added to your income for that year."),
   H2('Example'),
   P(f"Take $60,000 in 2026. Repayments start in 2030 at $4,000 a year ($60,000 ÷ 15) and finish in 2044."),
   H2('Using it with the FHSA'),
   P('The HBP and the First Home Savings Account can be used on the same purchase, which is how many couples in South Surrey and Langley reach a 10% to 20% down payment.', ('How the FHSA works.', '/fhsa-first-home-savings-account-bc.html')),
  ],
  faq=[("Do I have to be a first-time buyer to use the Home Buyers' Plan?", "Generally yes, under the CRA's definition, though there are exceptions such as after a marriage or common-law breakdown, and for buying a home for a person with a disability."),
       ('Can I use RRSP money I deposited last week?', 'Money must be in the RRSP for at least 90 days before you withdraw it under the plan, or it may not be deductible.')],
  src=[("canada.ca · The Home Buyers' Plan", 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/rrsps-related-plans/what-home-buyers-plan.html')],
  rel=[('First-time buyer calculator', '/first-time-buyer-calculator.html'), ('Mortgage calculator', '/mortgage-calculator.html'), ('How much down payment do I need?', '/minimum-down-payment-canada.html')]),

 dict(slug='minimum-down-payment-canada',
  q='How much down payment do I need to buy a home?',
  title='Minimum Down Payment in Canada: 5%, 10% or 20% (Examples)',
  desc='5% on the first $500,000, 10% on the rest up to $1.5 million, and 20% at $1.5 million or more. Worked examples at South Surrey and Langley prices.',
  answer='5% of the first $500,000 of the price, plus 10% of the part from $500,000 to $1.5 million. At $1.5 million or more the minimum is 20%. With less than 20% down you will need mortgage default insurance.',
  body=[
   H2('Minimum down payment at common prices'),
   L(*[f'{money(v)}: {money(v * 0.2 if v >= 1_500_000 else min(v, 500_000) * 0.05 + max(0, v - 500_000) * 0.10)}' for v in [500_000, 750_000, 1_000_000, 1_400_000, 1_600_000]]),
   H2('Cash you need on top'),
   P('Property transfer tax (unless you are exempt), legal fees, a home inspection and adjustments for property tax and strata fees. Budget these separately from the down payment.'),
   H2('Where the down payment can come from'),
   P("Savings, an FHSA, the RRSP Home Buyers' Plan, and a gift from family with a signed gift letter. Your lender will ask for 90 days of history on most of it."),
  ],
  faq=[('Is mortgage insurance required with less than 20% down?', 'Usually yes. The insurance premium is added to the mortgage, and the price limits for insured mortgages change from time to time, so ask your lender for the current rules.'),
       ('Does a down payment gift have to be paid back?', 'No. Lenders accept gifts from immediate family with a letter saying the money does not have to be repaid.')],
  src=[('canada.ca · How much you need for a down payment', 'https://www.canada.ca/en/financial-consumer-agency/services/mortgages/down-payment.html')],
  rel=[('Mortgage calculator', '/mortgage-calculator.html'), ('First-time buyer calculator', '/first-time-buyer-calculator.html'), ('How much is property transfer tax in BC?', '/how-much-is-property-transfer-tax-in-bc.html')]),

 dict(slug='bc-home-owner-grant-2026',
  q='What is the BC home owner grant threshold for 2026?',
  title='BC Home Owner Grant 2026: $2,075,000 Threshold & How to Claim',
  desc='The 2026 BC home owner grant threshold is $2,075,000. Above it the grant falls by $5 for every $1,000 of value. You must apply every year.',
  answer='$2,075,000. If your home is assessed at or below that, you can claim the full grant on your 2026 property taxes. Above it, the grant drops by $5 for every $1,000 of extra value until it reaches zero. You must apply every year, and pay at least $350 in property tax.',
  body=[
   H2('How much the grant is'),
   P('From January 1, 2027 the regular grant is $570. Seniors 65 and over, veterans and people with disabilities can get a larger, additional grant. The Province lists the current amounts on its home owner grant page.'),
   H2('Above the threshold'),
   P('The regular grant reaches $0 at an assessed value of $2,189,000. The additional grant reaches $0 at $2,244,000.'),
   H2('How to apply'),
   P('Online through the Province, each year after your property tax notice arrives. The home has to be your principal residence.'),
  ],
  faq=[('Do I get the home owner grant automatically?', 'No. You apply each year, even if nothing changed.'),
       ('Does a rental property get the grant?', 'No. The grant is for the home you live in as your principal residence.')],
  src=[('www2.gov.bc.ca · Home owner grant', 'https://www2.gov.bc.ca/gov/content/taxes/property-taxes/annual-property-tax/home-owner-grant')],
  rel=[('How do I appeal my BC Assessment?', '/how-to-appeal-bc-assessment.html'), ('What the 2026 BC Assessment means for owners', '/blog.html/what-the-2026-bc-assessment-means-for-property-owners-in-bc-8884331'), ("What's my home worth?", '/home-evaluation.html')]),

 dict(slug='how-to-appeal-bc-assessment',
  q='How do I appeal my BC Assessment?',
  title='How to Appeal Your BC Assessment: Deadline & Steps',
  desc='Call BC Assessment first. If you still disagree, file a complaint with the Property Assessment Review Panel by January 31. What evidence helps.',
  answer='Call BC Assessment first: many values are fixed by agreement without a hearing. If you still disagree, file a complaint with the Property Assessment Review Panel by January 31 of the assessment year (the date can move when it falls on a weekend). The panel hears complaints from February to March.',
  body=[
   H2('Step by step'),
   L('Check the property details on your notice: lot size, floor area, bedrooms, suites, age', 'Compare with sales of similar homes near the valuation date', 'Call BC Assessment and ask for a review', 'If that does not settle it, file a Notice of Complaint by the January deadline', 'Bring your evidence to the panel hearing; you can appeal further to the Property Assessment Appeal Board'),
   H2('Evidence that works'),
   P('Sales of truly similar homes close to the valuation date, and facts the assessor got wrong (an unpermitted suite counted as legal, the wrong lot size, a home that needs major repairs). A higher or lower tax bill is not a reason the panel can use.'),
   H2('Will it lower my taxes?'),
   P('Property tax is shared out by value, so your bill drops only if your value falls relative to the rest of your area. A correction still matters for the home owner grant if you are near the threshold.'),
  ],
  faq=[('Is my BC Assessment what my home would sell for?', 'Not exactly. It reflects the market on July 1 of the year before, and a mass appraisal can miss your home\'s details. For a current price, ask for a market evaluation.'),
       ('Does it cost money to appeal?', 'Filing with the Property Assessment Review Panel has no fee listed by BC Assessment. A further appeal to the Property Assessment Appeal Board has a fee.')],
  src=[('bcassessment.ca · About appeals', 'https://info.bcassessment.ca/Services-products/appeals/about-appeals')],
  rel=[("What's my home worth?", '/home-evaluation.html'), ('BC home owner grant 2026', '/bc-home-owner-grant-2026.html'), ('What the 2026 BC Assessment means for owners', '/blog.html/what-the-2026-bc-assessment-means-for-property-owners-in-bc-8884331')]),

 dict(slug='bc-home-buyer-rescission-period',
  q='Can I back out of buying a home in BC after my offer is accepted?',
  title='BC Home Buyer Rescission Period: 3 Days & the 0.25% Fee',
  desc='BC buyers can cancel an accepted offer within three business days by written notice and paying 0.25% of the offer price. What it covers and what it doesn\'t.',
  answer=f'Yes, within three business days. Since January 3, 2023, a buyer of most homes in BC can cancel an accepted offer by giving the seller written notice before the rescission period ends and paying a fee of 0.25% of the offer price. On a {money(1_000_000)} home the fee is {money(2_500)}.',
  body=[
   H2('What it covers'),
   P('Detached homes, semi-detached homes, townhouses, condos and other strata lots, units in duplexes and multi-unit buildings, manufactured homes on land, and co-op interests.'),
   H2('What it does not cover'),
   L('Homes on leased land and leasehold interests', 'Homes sold at auction', 'Court-ordered sales'),
   P('Weekends and statutory holidays do not count. Only the buyer can rescind, and the seller cannot ask the buyer to waive it.'),
   H2('Subjects are still the better protection'),
   P('The rescission period is short and costs money. Subject clauses for financing, inspection and strata documents give you time to check the home without a fee, so most buyers still write them in.'),
  ],
  faq=[('Does the rescission period apply to presales?', 'Presales from a developer are covered by their own cancellation right under BC\'s real estate development rules: seven days after receiving the disclosure statement.'),
       ('Can a seller back out during the three days?', 'No. The right belongs to the buyer only.')],
  src=[('bcfsa.ca · Home buyer rescission period', 'https://www.bcfsa.ca/public-resources/real-estate/buying-home/home-buyer-rescission-period')],
  rel=[('FAQ for home buyers in BC', '/faq-for-home-buyers-in-bc.html'), ('Presale projects in the Fraser Valley and Metro Vancouver', '/presale-projects-fraser-valley-and-metro-vancouver.html')]),
]

OTHER = [('Do first-time buyers pay property transfer tax in BC?', '/first-time-home-buyer-program.html'),
         ('Do first-time buyers get the GST back on a new home?', '/gst-rebate-in-bc.html'),
         ('What can I build on my lot? (zoning guide)', '/zonings.html')]

def page(p):
    blocks = [P(p['answer'])] + p['body']
    blocks += [H2('Sources'), P(f'Read on {READ}. Rules change, so confirm with the source or your lawyer, notary or accountant before you act.'),
               L(*p['src']), H2('Related guides'), L(*p['rel'], ('All BC real estate questions', f'/{HUB}.html'))]
    return {'slug': p['slug'], 'status': 'live', 'updated': '2026-11-18', 'qa_page': True,
            'new_page': {'title': p['title'], 'h1': p['q'], 'description': p['desc']},
            'breadcrumbs': [{'href': '/', 'name': 'Home'}, {'href': f'/{HUB}.html', 'name': 'Real estate questions'}, {'href': f"/{p['slug']}.html", 'name': p['q']}],
            'faq_heading': 'More questions', 'faq': [{'q': q, 'a': a} for q, a in p['faq']], 'blocks': blocks}

hub_blocks = [P('Short, sourced answers to the questions buyers and sellers in South Surrey, White Rock, Langley and the Fraser Valley ask most. Each page answers in the first paragraph, then shows the numbers and links to the official source.'),
              H2('Taxes when you buy'), L(*[(p['q'], f"/{p['slug']}.html") for p in PAGES if p['slug'] in ('how-much-is-property-transfer-tax-in-bc', 'bc-newly-built-home-exemption', 'can-foreigners-buy-property-in-bc')], OTHER[0], OTHER[1]),
              H2('Saving for a down payment'), L(*[(p['q'], f"/{p['slug']}.html") for p in PAGES if p['slug'] in ('minimum-down-payment-canada', 'fhsa-first-home-savings-account-bc', 'rrsp-home-buyers-plan-bc')]),
              H2('Owning and selling'), L(*[(p['q'], f"/{p['slug']}.html") for p in PAGES if p['slug'] in ('speculation-and-vacancy-tax-surrey-langley', 'bc-home-owner-grant-2026', 'how-to-appeal-bc-assessment', 'bc-home-flipping-tax')], OTHER[2]),
              H2('Making an offer'), L(*[(p['q'], f"/{p['slug']}.html") for p in PAGES if p['slug'] == 'bc-home-buyer-rescission-period'], ('FAQ for home buyers in BC', '/faq-for-home-buyers-in-bc.html'), ('FAQ for home sellers', '/faq-for-home-sellers.html')),
              H2('Ask me'), P('Have a question that is not here? Call or text 604-928-1361, or ', ('send me a message', '/contact.html'), '.')]
hub = {'slug': HUB, 'status': 'live', 'updated': '2026-11-18', 'qa_hub': True,
       'new_page': {'title': 'BC Real Estate Questions Answered: Taxes, Down Payment & More', 'h1': 'BC Real Estate Questions, Answered',
                    'description': 'Quick answers on property transfer tax, the speculation tax, flipping tax, FHSA, down payments, assessments and the 3-day rescission period in BC.'},
       'breadcrumbs': [{'href': '/', 'name': 'Home'}, {'href': f'/{HUB}.html', 'name': 'Real estate questions'}], 'blocks': hub_blocks}

for d in [page(p) for p in PAGES] + [hub]:
    path = os.path.join(OUT, d['slug'] + '.json')
    assert not os.path.exists(path) or json.load(open(path)).get('qa_page') or json.load(open(path)).get('qa_hub'), path
    open(path, 'w').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
print(len(PAGES) + 1, 'pages')
for p in PAGES: print(len(p['title']), len(p['desc']), p['slug'])
