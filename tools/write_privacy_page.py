"""Writes the privacy policy text (D-123) into src/data/pages/privacy.json and clears the old generated research-note layer in src/data/local/privacy.json.
The archived policy was generic boilerplate ("I/we", "personal account") and the generated layer was research notes about it, neither a real policy.
Plain language, under BC's PIPA; states only what this site does today.  Run: python3 -I tools/write_privacy_page.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*parts): return {'t': 'p', 'parts': [{'t': x} if isinstance(x, str) else {'t': x[0], 'h': x[1]} for x in parts]}
def H(text, level=2): return {'t': 'h', 'level': level, 'text': text}
def L(*items): return {'t': 'list', 'items': [[{'t': x} if isinstance(x, str) else {'t': x[0], 'h': x[1]} for x in (i if isinstance(i, list) else [i])] for i in items]}
BLOCKS = [
 H('PRIVACY POLICY', 1),
 P('This page explains what personal information this website collects, why, who sees it, and how you can ask us about it. Last updated November 5, 2026.'),
 H('Who is responsible'),
 P('Jared Gibbons Personal Real Estate Corporation, a REALTOR® with Royal LePage Little Oak Realty, Suite 201 – 15272 Croydon Dr, Surrey, BC, runs this website and is responsible for the personal information collected through it. Jared Gibbons is the privacy contact: ', ('jaredgibbons@royallepage.ca', 'mailto:jaredgibbons@royallepage.ca'), ' or 604-928-1361.'),
 H('What we collect'),
 L('What you type into a form on this site: your name, email, phone number, the address of a property if you ask for a home evaluation, and your message.',
   'What you give the home search tool when you register or save a search. That tool is run by our listing-search provider (see "Who sees it" below).',
   'Basic technical information every website receives when you visit, such as your IP address, browser type and the pages you open.'),
 H('Why we collect it'),
 L('To answer your question, prepare a home evaluation, or send the listings and market updates you asked for.',
   'To act on your behalf when you decide to buy or sell with us.',
   'To keep the site secure and stop spam, and to meet legal and professional record-keeping duties for real estate services.'),
 P('We collect and use your information with your consent, which you give when you submit a form or register. You can withdraw it at any time (see "Your choices").'),
 H('Who sees it'),
 P('We do not sell your personal information. It may be seen by:'),
 L('Jared Gibbons and the people who work with him at Royal LePage Little Oak Realty, so your request is handled.',
   'Service providers that help run this site: website hosting and spam protection (Cloudflare), email, our client-management system, and the listing-search provider that powers the home searches on this site. They may only use your information to provide their service to us.',
   'The mortgage, legal or other professionals you ask us to connect you with, and only for that purpose.',
   'Regulators or others where the law requires it.'),
 P('Some of these providers store information outside Canada, including in the United States, where it may be accessible under local law.'),
 H('Maps and address suggestions (Google)'),
 P('Some pages load Google Maps in your browser to show a map, suggest addresses as you type, or estimate a drive time. That sends the page address and what you type into those fields to Google. We do not receive or store it. See ', ('Google\'s privacy policy', 'https://policies.google.com/privacy'), '.'),
 H('Cookies'),
 P('This site uses only the cookies needed to keep forms working and protected from spam, and the home search tool may set its own cookies to remember your searches. You can block or clear cookies in your browser settings; some features may then not work.'),
 H('Your choices and your rights'),
 L('Ask what personal information we hold about you, and ask us to correct it.',
   'Withdraw your consent, or unsubscribe from emails at any time using the link in the email or by contacting us. We send commercial emails only as Canada\'s anti-spam law allows.',
   'Ask us to delete your information, unless we need to keep it for legal or professional reasons.'),
 P('We keep personal information only as long as needed for the reasons above and as the law and brokerage record rules require, then delete or anonymize it.'),
 H('Questions and complaints'),
 P('Write or call the privacy contact above. If you are not satisfied with our answer, you can contact the ', ('Office of the Information and Privacy Commissioner for British Columbia', 'https://www.oipc.bc.ca/'), '.'),
 H('Changes'),
 P('If we change how we handle personal information, we will update this page and its date.'),
]
def main():
    p = os.path.join(ROOT, 'src/data/pages/privacy.json'); d = json.load(open(p, encoding='utf-8'))
    d['blocks'] = BLOCKS
    d['seo']['Meta description'] = d['seo']['OG description'] = 'How Jared Gibbons, a Fraser Valley REALTOR, collects, uses and protects your personal information, including forms, searches, Google Maps and cookies.'
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(p, 'a').write('\n')
    q = os.path.join(ROOT, 'src/data/local/privacy.json'); l = json.load(open(q, encoding='utf-8'))
    l['blocks'] = []; l['faq'] = []; l['status'] = 'draft'
    json.dump(l, open(q, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); open(q, 'a').write('\n')
if __name__ == '__main__': main()
