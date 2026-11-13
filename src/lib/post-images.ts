// Blog post lead photos (D-259). src/data/post-images.json is written by tools/build_post_images.py; the files are in public/img/blog/.
// One record per post that has a photo: its alt text, the sizes on disk and how a card or the share card may crop it.
import DATA from '../data/post-images.json';

type Rec = { alt: string; w: number; h: number; widths: number[]; og: false | [number, number]; fit?: 'contain'; bg?: string; pos?: string; share?: string };
const ALL = DATA as unknown as Record<string, Rec>;
const SITE = 'https://jaredgibbons.ca';
/** The tallest a post's lead photo is shown, and the widest (px): a portrait graphic is held to the height, not the column width. */
const HERO_MAX_H = 640;
const HERO_MAX_W = 832;

export type PostImage = Rec & {
  /** largest size on disk (the `src` fallback) */ src: string;
  srcset: string;
  /** widest the lead photo is shown on its post, in CSS px (never wider than the file) */ heroW: number;
  /** absolute address of the 1200 x 630 share card, when the original was large enough for one */ ogUrl: string | null;
  /** absolute address of the largest size */ url: string;
};

export function postImage(slug: string): PostImage | null {
  const r = ALL[slug];
  if (!r) return null;
  const file = (w: number) => `/img/blog/${slug}-${w}.webp`;
  const top = r.widths[r.widths.length - 1];
  return {
    ...r,
    src: file(top),
    srcset: r.widths.map((w) => `${file(w)} ${w}w`).join(', '),
    heroW: Math.min(HERO_MAX_W, r.w, Math.round((HERO_MAX_H * r.w) / r.h)),
    ogUrl: r.og ? `${SITE}/img/blog/${slug}-og.jpg` : null,
    url: SITE + file(top),
  };
}
