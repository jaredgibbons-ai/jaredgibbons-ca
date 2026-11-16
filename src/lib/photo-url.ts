// One place that knows where a listing photo lives.
// - { id }: web-size WebP made by tools/process_photos.py, served from the R2 route (/listing-photos/<id>-480|960|1600.webp).
// - { u: { s, l } }: a listing page the sync job made on its own (tools/sync_listings.mjs). Its photos load from MyRealPage's
//   photo server until they are processed like the rest: s is the 320-wide copy, l the full-size one (the only two sizes MyRealPage signs).
export type Photo = { p: number; id?: string; w: number; h: number; u?: { s?: string; l: string }; cap?: string; g?: 1 };   // g: width and height are a guess (the photo could not be measured)
const BASE = import.meta.env.PUBLIC_PHOTO_BASE ?? '/listing-photos/';
export const photoUrl = (ph: Photo, size: 480 | 960 | 1600, base = BASE) => ph.u ? (size === 480 ? ph.u.s || ph.u.l : ph.u.l) : `${base}${ph.id}-${size}.webp`;
export const photoSrcset = (ph: Photo, sizes: (480 | 960 | 1600)[], base = BASE, extra = '') =>
  ph.u ? (ph.u.s ? `${ph.u.s} 320w, ${ph.u.l} ${ph.w || 1600}w` : undefined) : sizes.map((s) => `${base}${ph.id}-${s}.webp ${s}w`).join(', ').replace(/( 480w, )/, `$1${extra}`);
