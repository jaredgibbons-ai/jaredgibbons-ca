// Opt-in "Show nearby places" on the neighbourhood maps. Pure helpers (no Google calls here) so the rules are testable.
// Rules: one Nearby Search per button press, only the fields below (name and position, no ratings, hours or photos: cheapest Google tier and our no-ratings rule),
// results live only in the page's memory (Google limits storing), and nothing runs until someone presses a button.
export const PLACE_FIELDS = ['displayName', 'location'];
export const NEARBY = [
  { id: 'park', label: 'Parks', singular: 'Park', pin: 'P', types: ['park'] },
  { id: 'cafe', label: 'Cafés', singular: 'Café', pin: 'C', types: ['cafe', 'coffee_shop'] },
  { id: 'grocery', label: 'Groceries', singular: 'Grocery', pin: 'G', types: ['grocery_store', 'supermarket'] },
];
export const MIN_RADIUS = 500, MAX_RADIUS = 5000, MAX_RESULTS = 20;

const rad = (d) => (d * Math.PI) / 180;
/** Straight-line distance in metres between two {lat,lng} points. */
export function distanceM(a, b) {
  const R = 6371008.8, dLat = rad(b.lat - a.lat), dLng = rad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}
/** Search radius: half the shorter side of what is on screen, kept between 500 m and 5 km. */
export function radiusFor(widthM, heightM) {
  const half = Math.min(widthM, heightM) / 2;
  if (!Number.isFinite(half)) return MIN_RADIUS * 2;
  return Math.round(Math.min(MAX_RADIUS, Math.max(MIN_RADIUS, half)));
}
/** The Places API (New) Place.searchNearby request for one category. */
export function nearbyRequest(cat, center, radius) {
  return {
    fields: PLACE_FIELDS,
    locationRestriction: { center: { lat: center.lat, lng: center.lng }, radius },
    includedPrimaryTypes: cat.types,
    maxResultCount: MAX_RESULTS,
    rankPreference: 'DISTANCE',
    language: 'en',
    region: 'ca',
  };
}
export const kmLabel = (m) => (m >= 1000 ? `${(m / 1000).toFixed(m >= 9500 ? 0 : 1).replace(/\.0$/, '')} km` : `${Math.round(m / 10) * 10} m`);
/** Plain rows for the text list: nearest first, named places only. `pos` may be a google LatLng or a {lat,lng}. */
export function describePlaces(places, cat, center) {
  return (places || [])
    .map((p) => {
      const L = p.location, loc = L ? { lat: typeof L.lat === 'function' ? L.lat() : L.lat, lng: typeof L.lng === 'function' ? L.lng() : L.lng } : null; // google LatLng.lat() needs its `this`
      const name = typeof p.displayName === 'string' ? p.displayName : p.displayName?.text;
      return loc && Number.isFinite(loc.lat) && Number.isFinite(loc.lng) && name ? { name: String(name).trim(), cat: cat.id, label: cat.singular, pin: cat.pin, lat: loc.lat, lng: loc.lng, m: distanceM(center, loc) } : null;
    })
    .filter(Boolean)
    .sort((a, b) => a.m - b.m);
}
