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
          const body = (a >= 0 && b > a ? html.slice(a, b) : html).replace(/ data-astro-cid-[a-z0-9]+/g, '');
          const h = crypto.createHash('sha1').update(body).digest('hex').slice(0, 12);
          const prev = manifest[loc];
          const d = prev && prev.h === h ? prev.d : today;
          if (!prev || prev.h !== h) changed++;
          next[loc] = { h, d };
          return `<url><loc>${loc}</loc><lastmod>${d}</lastmod></url>`;
        });
        fs.writeFileSync(smPath, xml);
        if (process.env.LASTMOD_WRITE === '1') fs.writeFileSync(manifestPath, JSON.stringify(next, null, 0).replace(/\},"/g, '},\n"'));
        console.log(`[lastmod] ${Object.keys(next).length} urls, ${changed} new or changed${process.env.LASTMOD_WRITE === '1' ? ', manifest written' : ''}`);
      },
    },
  };
}
