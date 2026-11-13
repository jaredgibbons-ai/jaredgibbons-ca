// The open MyRealPage map search, full screen. The two map pages frame this same address on desktop (D-242)
// and link to it with a button on phones (D-255), so it lives in one place.
export const mapSearchUrl = (account: string): string =>
  `https://idx.myrealpage.com/wps/-/tmpl~v2,idx_v2_map_pos~49.10058663823867%7C-122.78651742876207,idx_v2_map_radius~15/recip/${account}/idx.search`;
