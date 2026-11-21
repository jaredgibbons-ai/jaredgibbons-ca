"""Area facts for the commercial pages (D-391), from Muse's research of Nov 20, 2026 (docs/research/commercial/commercial-facts-2026-11-20.md).
Every fact here was re-opened on its source on Nov 20, 2026 before use (city PDFs and pages, the Metro Vancouver 2025 Industrial Lands
Inventory). Items Muse marked "not found", and figures that could not be re-opened (Abbotsford's 2017 hectare totals), are left out.
Each fact is (text, source label, url)."""
MV = ('Metro Vancouver 2025 Industrial Lands Inventory', 'https://metrovancouver.org/services/regional-planning/Documents/mv-industrial-lands-inventory-summary-report-appendices-2025.pdf')
CH = ('City of Surrey, Campbell Heights Business Park', 'https://www.surrey.ca/sites/default/files/media/documents/CampbellHeightsBusinessPark.pdf')
H99 = ('City of Surrey, Highway 99 Corridor', 'https://www.surrey.ca/sites/default/files/media/documents/Hwy99CorridorIndustrialArea.pdf')
RH = ('City of Surrey, Rosemary Heights Business Park', 'https://www.surrey.ca/sites/default/files/media/documents/RosemaryHeightsBusinessPark.pdf')
DG = ('City of Surrey, Douglas Industrial Area', 'https://www.surrey.ca/sites/default/files/media/documents/DouglasIndustrialArea.pdf')
CL = ('City of Surrey, Cloverdale Industrial Area', 'https://www.surrey.ca/sites/default/files/media/documents/CloverdaleIndustrialArea.pdf')
SCH = ('City of Surrey, South Campbell Heights plan', 'https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning/south-surrey-land-use-plans/south-campbell-heights')
STC = ('City of Surrey, Semiahmoo Town Centre Plan', 'https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning/south-surrey-land-use-plans/semiahmoo-town-centre-plan')
CTC = ('City of Surrey, Cloverdale Town Centre Plan', 'https://www.surrey.ca/renovating-building-development/land-planning-development/land-use-planning/cloverdale-land-use-plans/cloverdale-town-centre-plan')
SBL = ('City of Surrey, updating your business licence', 'https://www.surrey.ca/business-economy/business-licensing/updating-your-business-licence')
TOLBL = ('Township of Langley, business licences', 'https://www.tol.ca/en/services/business-licences.aspx')
FHE = ('Township of Langley, Fraser Highway Employment Lands', 'https://www.tol.ca/en/connect/fraser-highway-employment-lands.aspx')
ALD = ('Township of Langley, Aldergrove', 'https://www.tol.ca/en/the-township/aldergrove.aspx')
LCBL = ('City of Langley, business licences', 'https://www.langleycity.ca/business-development/permits-licensing/business-licences')
LCOCP = ('City of Langley Official Community Plan', 'https://www.langleycity.ca/media/file/ocp-official-community-plan-bylaw-r')
ABBL = ('City of Abbotsford, business licences', 'https://www.abbotsford.ca/business-development/business-licences')
ABIL = ('City of Abbotsford, Industrial Land Strategy (April 2017)', 'https://www.abbotsford.ca/sites/default/files/2021-02/Industrial%20Land%20Strategy.pdf')

SURREY_LICENCE = [("Buying a Surrey business: the City licence does not simply carry over. A change of owner costs $25 and needs a copy of the purchase and sale agreement, and the City may ask for more, such as health permits.",) + SBL]

AREA = {
 'south-surrey': {
  'industrial': ('Where South Surrey’s industrial land is', [
    ("Campbell Heights Business Park covers 1,900 acres along Surrey’s eastern edge by the Langley border. It is home to 495 businesses and more than 12,600 jobs, and its zoning is mainly IB-1 and IB-2 business park.",) + CH,
    ("Campbell Heights is Surrey’s largest industrial area in the regional inventory (770 hectares), and it had the region’s largest addition of new industrial parcels between 2020 and 2025 (154.4 hectares).",) + MV,
    ("South Campbell Heights, approved by Council on December 16, 2024, adds about 249 hectares (615 acres) south of the existing park, about 350 acres of it employment land.",) + SCH,
    ("BC Hydro’s new 230 kV Brookswood substation, a $450 million investment, is planned for 2033 to serve growth in the area.",) + CH,
    ("The Douglas Industrial Area (26 acres) sits at the Pacific border crossing and holds 113 businesses, including customs brokers and logistics companies.",) + DG]),
  'office': ('Where South Surrey’s offices are', [
    ("Rosemary Heights Business Park (77 acres) is bounded by 32 Avenue, 156 Street and Highway 99, with 213 businesses. Its plan envisions high-tech, research and development, light manufacturing and corporate head offices.",) + RH,
    ("The Highway 99 Corridor (390 acres) is home to 253 businesses, mostly commercial.",) + H99,
    ("Campbell Heights’ IB-1 and IB-2 business park zoning allows offices alongside light industry and warehousing.",) + CH]),
  'retail': ('Where South Surrey shops and services are', [
    ("Semiahmoo Town Centre, from 16 Avenue (North Bluff Road) to 24 Avenue, is planned by the City as the cultural and commercial heart of South Surrey. Council approved the plan on January 31, 2022; the plan area is 136 hectares (336 acres).",) + STC,
    ("Morgan Crossing and Grandview Corners serve the Highway 99 Corridor, and the City plans road improvements along 20 Avenue, including an overpass over Highway 99.",) + H99]),
  'land': ('Employment land in South Surrey', [
    ("Surrey has 2,713 hectares of industrial land in the regional inventory (July 1, 2025), 22% of Metro Vancouver’s total and the largest share of any city. The City’s own industrial land page still shows the 2020 total of 2,534 hectares.",) + MV,
    ("South Campbell Heights (approved December 16, 2024) adds about 249 hectares, the newest planned employment land in South Surrey.",) + SCH]),
  'business': ('Buying a business in South Surrey', SURREY_LICENCE),
 },
 'cloverdale': {
  'industrial': ('Where Cloverdale’s industrial land is', [
    ("The Cloverdale industrial area covers 700 acres in three parts: Cloverdale East (333 acres), Cloverdale South (268 acres) and Cloverdale North (98 acres). It is home to 731 companies.",) + CL,
    ("It sits where Highway 15, the route to Highway 1 and the Pacific border crossing, meets Highway 10, an east–west trucking route. The 72 Avenue improvements and extension started in May 2025.",) + CL]),
  'office': ('Offices in Cloverdale', [
    ("The City’s business overview counts 617 office jobs in the Cloverdale industrial area; the City does not publish a separate office district for Cloverdale.",) + CL]),
  'retail': ('Cloverdale Town Centre', [
    ("Cloverdale Town Centre is at Highway 10 and Highway 15. Council endorsed its plan on November 18, 2019 and an update on October 30, 2023 to support the planned new hospital and BC Cancer Centre.",) + CTC,
    ("On July 22, 2024 the plan area was expanded north, adding roughly 80.8 hectares.",) + CTC]),
  'land': ('Employment land in Cloverdale', [
    ("Cloverdale’s 700 acres of industrial land are counted within Surrey’s 2,713 hectares in the regional inventory (July 1, 2025).",) + CL]),
  'business': ('Buying a business in Cloverdale', SURREY_LICENCE),
 },
 'langley': {
  'industrial': ('Where Langley’s industrial land is', [
    ("The Langleys have 1,000 hectares of industrial land in the regional inventory. The two largest areas are both in the Township: Port Kells (317 hectares) and Gloucester (237 hectares).",) + MV,
    ("Aldergrove is home to the Gloucester Industrial Park.",) + ALD,
    ("The Township’s Fraser Highway Employment Lands, about 500 acres between 228 Street and 240 Street outside the Agricultural Land Reserve, are planned to add industrial land. Council endorsed the reference plan on December 15, 2025; each site still needs a regional growth strategy amendment.",) + FHE]),
  'office': ('Offices in Langley', [
    ("The City of Langley’s Official Community Plan sets out to encourage office space near the planned 196 Street and 203 Street SkyTrain stations, for example by exempting one floor of office from floor area limits.",) + LCOCP]),
  'retail': ('Shops and services in Langley', [
    ("The City of Langley’s Official Community Plan names neighbourhood corner commercial sites at 203 Street by Portage Park, 200 Street and 50 Avenue, 200 Street and 56 Avenue, and 208 Street and 48 Avenue.",) + LCOCP,
    ("Aldergrove, on the Township’s eastern edge, has shops as well as the Gloucester Industrial Park.",) + ALD]),
  'land': ('Employment land in Langley', [
    ("Langley Township has 918 hectares of industrial land in the regional inventory (July 1, 2025) and the City of Langley 82 hectares.",) + MV,
    ("The City of Langley’s Official Community Plan says all its employment land is developed, so new space there comes from redevelopment.",) + LCOCP,
    ("The Township’s Fraser Highway Employment Lands (about 500 acres between 228 and 240 Street) are the main planned addition; Council endorsed the reference plan on December 15, 2025.",) + FHE]),
  'business': ('Buying a business in Langley', [
    ("Township of Langley licences cannot be transferred: a new owner must apply for a new licence, and new or relocating businesses should allow at least 30 business days.",) + TOLBL,
    ("Every business operating in the City of Langley needs a valid City licence before it starts.",) + LCBL]),
 },
 'abbotsford': {
  'industrial': ('Where Abbotsford’s industrial growth is planned', [
    ("The City’s 2017 Industrial Land Strategy found Special Study Areas A and B had the highest potential for new industrial land: Area A suited to large logistics, warehousing and distribution users, and Area B, near Mt Lehman Road and the airport, to smaller and medium-bay industrial businesses.",) + ABIL]),
  'land': ('Industrial land in Abbotsford', [
    ("The City’s 2017 Industrial Land Strategy named Special Study Areas A and B as the best places for future industrial land; Area B lies near Mt Lehman Road and the airport.",) + ABIL,
    ("Abbotsford is in the Fraser Valley Regional District, so it is not counted in Metro Vancouver’s industrial land inventory.",) + MV]),
  'business': ('Buying a business in Abbotsford', [
    ("Abbotsford business licences are not transferable: after a change of ownership, a new application is made and the old licence cancelled. Every business located in the City needs an inspection.",) + ABBL]),
 },
}

CITY = {
 'surrey': [("Surrey has 2,713 hectares of industrial land in the regional inventory (July 1, 2025), the most of any city. Its largest areas are Campbell Heights (770 ha), Newton (449 ha), Bridgeview (343 ha) and South Westminster (341 ha).",) + MV] + SURREY_LICENCE,
 'maple-ridge': [("Maple Ridge has 749 hectares of industrial land in the regional inventory (July 1, 2025).",) + MV,
                 ("The City says it has over 300 hectares of industrial and employment land available. Its main shopping centres, Haney Place Mall and Valley Fair Mall in the town centre and Westridge Centre and Westgate Shopping Centre in west Maple Ridge, are all off Lougheed Highway.", 'City of Maple Ridge, industries', 'https://www.mapleridge.ca/build-do-business/invest-maple-ridge/industries'),
                 ("All businesses operating in Maple Ridge need a business licence.", 'City of Maple Ridge, business licensing', 'https://www.mapleridge.ca/build-do-business/business-licensing')],
 'richmond': [("Richmond has 1,738 hectares of industrial land, 14% of Metro Vancouver’s inventory (July 1, 2025).",) + MV,
              ("After a change of ownership, Richmond asks for a Transfer of Licence Form with the business licence paperwork.", 'City of Richmond, business licences', 'https://www.richmond.ca/business-development/resources/business-licences.htm')],
 'new-westminster': [("New Westminster has 201 hectares of industrial land in the regional inventory (July 1, 2025).",) + MV],
 'port-coquitlam': [("Port Coquitlam has 445 hectares of industrial land (July 1, 2025); Mary Hill (396 hectares) is the largest industrial area in the Northeast Sector.",) + MV,
                    ("Industrial zones in Port Coquitlam are M1 to M4, and building, plumbing and fire inspectors visit before an industrial business licence is issued.", 'City of Port Coquitlam, business licencing', 'https://www.portcoquitlam.ca/business-development/doing-business/business-licencing')],
 'port-moody': [("Port Moody has 443 hectares of industrial land (July 1, 2025), including Ioco (230 hectares) and St John’s / Barnett Highway (212 hectares).",) + MV,
                ("A new business in a commercial space needs its building and fire inspections accepted before the licence is approved.", 'City of Port Moody, business licences', 'https://www.portmoody.ca/business-development-and-planning/business-licences-and-permits/')],
 'north-vancouver': [("The City of North Vancouver has 136 hectares of industrial land and the District 292 hectares (July 1, 2025).",) + MV,
                     ("The City lists five industrial centres: the Waterfront; East of Heywood and north of CN Rail; Mackay to Bewicke between 3rd Street and BC Rail; Lower Lonsdale; and Harbourside Business Park.", 'City of North Vancouver, industrial land use', 'https://www.cnv.org/Community-Environment/land-use/industrial')],
 'mission': [("In Mission, a transfer of ownership needs a full new business licence application.", 'City of Mission, business licence', 'https://www.mission.ca/business-licence')],
 'chilliwack': [("A business licence is required to operate a business in the City of Chilliwack; check the property’s zoning for the businesses it allows.", 'City of Chilliwack, business licences', 'https://www.chilliwack.com/main/page.cfm?id=1086')],
}
