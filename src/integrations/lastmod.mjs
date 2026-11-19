// <lastmod> for every sitemap URL (D-140). A date changes only when the page's own content changes, not when the header, footer or a stylesheet does:
// each built page's <main> is hashed (component scoping ids removed) and compared with src/data/lastmod.json.
//  - same hash  -> keep the stored date
//  - new/changed -> today (the build date), written back to the manifest only when LASTMOD_WRITE=1 (done when committing, so Cloudflare's build reproduces the same dates)
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

export default function lastmod() {
  return {
    name: 'lastmod',
    hooks: {
      'astro:build:done': ({ dir }) => {
        const root = fileURLToPath(dir);
        const here = path.dirname(fileURLToPath(import.meta.url));
        const manifestPath = path.join(here, '../data/lastmod.json');
        const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, 'utf8')) : {};
        const smPath = path.join(root, 'sitemap.xml');
        if (!fs.existsSync(smPath)) return;
        const today = new Date().toISOString().slice(0, 10);
        const fileFor = (loc) => {
          const p = new URL(loc).pathname;
          const cands = [p === '/' ? 'index.html' : p.replace(/^\//, ''), p.replace(/^\/blog\.html\//, 'internal/blog/') + '.html', p.replace(/^\/our-listings\.html\//, 'internal/listings/') + '.html'];
          return cands.map((c) => path.join(root, c)).find((c) => fs.existsSync(c) && fs.statSync(c).isFile());
        };
        let xml = fs.readFileSync(smPath, 'utf8'); const next = {}; let changed = 0;
        xml = xml.replace(/<url><loc>([^<]+)<\/loc><\/url>/g, (all, loc) => {
          const f = fileFor(loc.replace(/&amp;/g, '&')); if (!f) return all;
          const html = fs.readFileSync(f, 'utf8');
          const a = html.indexOf('<main'), b = html.lastIndexOf('</main>');
          // The Google Maps key is a build variable on Cloudflare and is absent in a local build, so data-key="AIza…" there is data-key or data-key="" here.
          // Without this, every page with a form or a map hashed differently on Cloudflare and got the build day as its date (review of Nov 15 2026).
          const body = (a >= 0 && b > a ? html.slice(a, b) : html).replace(/ data-astro-cid-[a-z0-9]+/g, '').replace(/ data-key(?:="(?:AIza[\w-]{30,})?")?(?=[\s>])/g, ' data-key')
            // Scripts are behaviour, not content: a change to how a listings box loads must not re-date 1,300 pages. Structured data (ld+json) stays in.
            .replace(/<script(?![^>]*ld\+json)[^>]*>[\s\S]*?<\/script>/g, '')
            // The quick-search menu's option list (data-qs, every page with the search quiz) is site navigation, not the page's content:
            // a new search page added to it must not re-date ~1,000 pages (D-316).
            .replace(/ data-qs="[^"]*"/g, ' data-qs')
            // The "Updated <date>" line shows this very date (D-373): it is the result, not part of what is compared.
            .replace(/<time data-lm datetime="[^"]*"[^>]*>[^<]*<\/time>/g, '<time data-lm></time>');
          const h = crypto.createHash('sha1').update(body).digest('hex').slice(0, 12);
          const prev = manifest[loc];
          // LASTMOD_REHASH=1 (once, after a change to what is hashed): store the new hashes and keep every page's date.
          const d = prev && (prev.h === h || process.env.LASTMOD_REHASH === '1') ? prev.d : today;
          if (!prev || prev.h !== h) changed++;
          next[loc] = { h, d };
          // Write the final date into the page: the "Updated" line and the WebPage dateModified (both rendered from the manifest before this build).
          if (html.includes('data-lm')) {
            const label = new Date(`${d}T12:00:00Z`).toLocaleDateString('en-CA', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
            const out = html.replace(/<time data-lm datetime="[^"]*"([^>]*)>[^<]*<\/time>/g, `<time data-lm datetime="${d}"$1>${label}</time>`)
              .replace(/("@type":"WebPage","url":"[^"]*","name":"(?:[^"\\]|\\.)*","dateModified":")\d{4}-\d{2}-\d{2}/, `$1${d}`);
            if (out !== html) fs.writeFileSync(f, out);
          }
          return `<url><loc>${loc}</loc><lastmod>${d}</lastmod></url>`;
        });
        fs.writeFileSync(smPath, xml);
        if (process.env.LASTMOD_WRITE === '1') fs.writeFileSync(manifestPath, JSON.stringify(next, null, 0).replace(/\},"/g, '},\n"'));
        console.log(`[lastmod] ${Object.keys(next).length} urls, ${changed} new or changed${process.env.LASTMOD_WRITE === '1' ? ', manifest written' : ''}`);
      },
    },
  };
}
