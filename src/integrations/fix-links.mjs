// After the build: make every internal link in the built pages land on a real page.
//  1. A link to an old URL the Worker redirects is rewritten to the redirect's destination (no redirect hop for visitors or crawlers).
//  2. A link in src/data/link-fixes.json is rewritten to its live equivalent, or removed (null) with its words kept.
//  3. A link to /x.html with no page, where /x-guide.html exists, goes to the guide.
// Links the Worker serves itself (/blog.html/<post>, listing detail routes, /recip.html/...) are left alone.
// It also keeps heading levels in order: a second H1 becomes an H2 and a heading never jumps more than one level (H1 then H3 becomes H1 then H2); classes stay, so nothing looks different.
// Archived wording is never changed. Anything still unresolved is printed and fails tests/links.test.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const WORKER_SERVED = /^\/(?:listing-photos\/|blog\.html\/|our-listings\.html\/|recip\.html\/|mylistings\.html\/|fort-langley\.html\/listing\.|[a-z0-9-]+\.html\/listing\.)/;

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

export default function fixLinks() {
  return {
    name: 'fix-links',
    hooks: {
      'astro:build:done': ({ dir }) => {
        const root = fileURLToPath(dir);
        const here = path.dirname(fileURLToPath(import.meta.url));
        const rules = JSON.parse(fs.readFileSync(path.join(here, '../worker/rules.json'), 'utf8'));
        const manual = JSON.parse(fs.readFileSync(path.join(here, '../data/link-fixes.json'), 'utf8'));
        const redirects = new Map(rules.redirects.filter((r) => r.status === 301 || r.status === 302).map((r) => [r.from, r.to]));
        const files = walk(root);
        const exists = (p) => { const q = p.replace(/^\//, ''); if (!q) return true; return !!q && (fs.existsSync(path.join(root, q)) || fs.existsSync(path.join(root, q + '.html')) || (fs.existsSync(path.join(root, q)) && fs.statSync(path.join(root, q)).isDirectory())); };
        const resolve = (href) => {
          const m = href.match(/^([^?#]*)([?#].*)?$/); const p = decodeURI(m[1]); const tail = m[2] || '';
          if (!p.startsWith('/') || p.startsWith('//')) return { keep: true };
          if (WORKER_SERVED.test(p)) return p in manual ? (manual[p] === null ? { drop: true } : { to: manual[p] + tail }) : { keep: true };
          let cur = p, hops = 0;
          while (hops++ < 4) {
            if (redirects.has(cur) && !exists(cur)) { cur = redirects.get(cur).replace(/^https:\/\/jaredgibbons\.ca/, ''); continue; }
            break;
          }
          if (cur !== p) { const q = cur.split(/[?#]/)[0]; if (exists(q) || WORKER_SERVED.test(q)) return { to: cur + (cur.includes('?') || cur.includes('#') ? '' : tail) }; }
          if (exists(p)) return { keep: true };
          if (p in manual) return manual[p] === null ? { drop: true } : { to: manual[p] + tail };
          const g = p.replace(/\.html$/, '') + '-guide.html';
          if (p.endsWith('.html') && exists(g)) return { to: g + tail };
          return { unresolved: true };
        };
        let rewritten = 0, dropped = 0, headingsFixed = 0; const unresolved = new Map();
        for (const f of files) {
          let t = fs.readFileSync(f, 'utf8'); let changed = false;
          t = t.replace(/<a\b([^>]*?)\shref="([^"]*)"([^>]*)>([\s\S]*?)<\/a>/g, (all, a, href, b, inner) => {
            if (!href.startsWith('/')) return all;
            const r = resolve(href);
            if (r.keep) return all;
            if (r.to) { changed = true; rewritten++; return `<a${a} href="${r.to}"${b}>${inner}</a>`; }
            if (r.drop) { changed = true; dropped++; return inner; }
            const k = href.split(/[?#]/)[0]; unresolved.set(k, (unresolved.get(k) || 0) + 1); return all;
          });
          const mi = t.indexOf('<main'), mj = t.indexOf('</main>');
          if (mi >= 0 && mj > mi) {
            let prev = 0, seenH1 = false, n = 0;
            const mid = t.slice(mi, mj).replace(/<h([1-6])(\b[^>]*)>([\s\S]*?)<\/h\1>/g, (all, lv, attrs, inner) => {
              let L = +lv; if (L === 1) { if (seenH1) L = 2; else seenH1 = true; }
              if (prev > 0 && L > prev + 1) L = prev + 1;
              prev = L; if (L === +lv) return all; n++; return `<h${L}${attrs}>${inner}</h${L}>`;
            });
            if (n) { t = t.slice(0, mi) + mid + t.slice(mj); changed = true; headingsFixed += n; }
          }
          if (changed) fs.writeFileSync(f, t);
        }
        console.log(`[fix-links] rewritten ${rewritten}, removed ${dropped}, unresolved ${unresolved.size}, headings fixed ${headingsFixed}`);
        if (unresolved.size) fs.writeFileSync(path.join(root, '..', 'link-unresolved.json'), JSON.stringify([...unresolved], null, 1));
        else if (fs.existsSync(path.join(root, '..', 'link-unresolved.json'))) fs.unlinkSync(path.join(root, '..', 'link-unresolved.json'));
      },
    },
  };
}
