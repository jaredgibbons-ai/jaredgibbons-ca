// After the build: make every internal link in the built pages land on a real page.
//  1. A link to an old URL the Worker redirects is rewritten to the redirect's destination (no redirect hop for visitors or crawlers).
//  2. A link in src/data/link-fixes.json is rewritten to its live equivalent, or removed (null) with its words kept.
//  3. A link to /x.html with no page, where /x-guide.html exists, goes to the guide.
// Links the Worker serves itself (/blog.html/<post>, listing detail routes, /recip.html/...) are left alone.
// It also keeps heading levels in order: a second H1 becomes an H2 and a heading never jumps more than one level (H1 then H3 becomes H1 then H2); classes stay, so nothing looks different.
// Wording (D-140, from the pre-launch audit): a few claims were written two ways on the old site; WORDING below makes each one read one way everywhere (titles, descriptions, body, JSON-LD). Nothing else in the archive text is touched.
// Anything still unresolved is printed and fails tests/links.test.mjs.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const WORKER_SERVED = /^\/(?:listing-photos\/|blog\.html\/|our-listings\.html\/|recip\.html\/|mylistings\.html\/|fort-langley\.html\/listing\.|[a-z0-9-]+\.html\/listing\.)/;

// One claim, one wording. Order matters: longer patterns first.
const WORDING = [
  [/\b[Mm]ore than \$500\s?(?:M|million) in (?:career )?sales\b/g, '$500M+ in career sales'],
  [/\$500M\+ in sales\b/g, '$500M+ in career sales'],
  [/\b10 consecutive years in the FVREB Medallion Club\b/g, '10 straight years in the FVREB Medallion Club'],
  [/\b10 consecutive years FVREB Medallion Club\b/g, '10 straight years in the FVREB Medallion Club'],
  [/Royal LePage Little Oak(?! Realty)(?=[.,;:"'<)\s])/g, 'Royal LePage Little Oak Realty'],
];

// Other agents', teams' and brokerages' sites cited as sources (D-200). Developers, governments and news stay followed.
// Other agents', brokerages' and listing portals' sites (D-204, D-209: src/data/other-agent-domains.json). Source lists swap them at render time;
// any link to them left elsewhere on a page (old blog posts, archive text) is unlinked here, text kept. realtor.ca (CREA) only gets nofollow.
const OTHER_AGENTS = JSON.parse(fs.readFileSync(new URL('../data/other-agent-domains.json', import.meta.url), 'utf8')).domains;
const NOFOLLOW_ONLY = ['realtor.ca'];
const HTTPS_HOSTS = ['gov.bc.ca', 'gc.ca', 'canada.ca', 'delta.ca', 'mapleridge.ca', 'burnaby.ca', 'burnaby.bc.ca', 'translink.ca', 'portmoody.ca', 'newwestcity.ca', 'surrey.ca',
  'portcoquitlam.ca', 'nvrc.ca', 'coquitlam.ca', 'sd43.bc.ca', 'vancouver.ca', 'vpl.ca', 'fvrd.ca', 'surreylibraries.ca', 'chilliwack.com', 'mission.ca', 'richmond.ca',
  'fvrl.bc.ca', 'bcfsa.ca', 'tol.ca', 'metrovancouver.org', 'pittmeadows.ca', 'coqlibrary.ca', 'bcassessment.ca', 'abbotsford.ca', 'dnv.org', 'nvdpl.ca', 'cnv.org',
  'kentbc.ca', 'vch.ca', 'nvcl.ca', 'bpl.bc.ca', 'heritagevancouver.org', 'mybaragar.com', 'engagechilliwack.com', 'bchousing.org', 'westvancouver.ca', 'whiterockcity.ca'];

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
        const isFile = (p) => { try { return fs.statSync(path.join(root, p.replace(/^\//, ''))).isFile(); } catch { return false; } };
        const resolve = (href) => {
          const m = href.match(/^([^?#]*)([?#].*)?$/); const p = decodeURI(m[1]); const tail = m[2] || '';
          if (!p.startsWith('/') || p.startsWith('//')) return { keep: true };
          if (redirects.has(p) && WORKER_SERVED.test(p)) { const to = redirects.get(p).replace(/^https:\/\/jaredgibbons\.ca/, ''); return { to: to + (to.includes('?') || to.includes('#') ? '' : tail) }; }
          if (WORKER_SERVED.test(p)) return p in manual ? (manual[p] === null ? { drop: true } : { to: manual[p] + tail }) : { keep: true };
          // /x with no extension where /x.html is the page: link straight to /x.html (the Worker would only 301 it)
          if (p !== '/' && !/\.[a-z0-9]+$/i.test(p) && !isFile(p) && !redirects.has(p) && fs.existsSync(path.join(root, p.replace(/^\//, '') + '.html'))) return { to: p + '.html' + tail };
          let cur = p, hops = 0;
          while (hops++ < 4) {
            if (redirects.has(cur) && !isFile(cur)) { cur = redirects.get(cur).replace(/^https:\/\/jaredgibbons\.ca/, ''); continue; }
            break;
          }
          if (cur !== p) { const q = cur.split(/[?#]/)[0]; if (exists(q) || WORKER_SERVED.test(q)) return { to: cur + (cur.includes('?') || cur.includes('#') ? '' : tail) }; }
          if (exists(p)) return { keep: true };
          if (p in manual) return manual[p] === null ? { drop: true } : { to: manual[p] + tail };
          const g = p.replace(/\.html$/, '') + '-guide.html';
          if (p.endsWith('.html') && exists(g)) return { to: g + tail };
          return { unresolved: true };
        };
        let httpsUp = 0, rewritten = 0, dropped = 0, headingsFixed = 0, wording = 0, nofollow = 0, unlinked = 0; const unresolved = new Map();
        for (const f of files) {
          let t = fs.readFileSync(f, 'utf8'); let changed = false;
          t = t.replace(/<a\b([^>]*?)\shref="([^"]*)"([^>]*)>([\s\S]*?)<\/a>/g, (all, a, href, b, inner) => {
            if (!href.startsWith('/')) {
              // D-218: public bodies' links written as http:// go out as https:// (all of these serve https)
              if (/^http:\/\//i.test(href)) { const h0 = (href.match(/^http:\/\/([^/:?#]+)/i) || [])[1]?.toLowerCase() || ''; if (HTTPS_HOSTS.some((d) => h0 === d || h0.endsWith('.' + d))) { href = 'https://' + href.slice(7); all = `<a${a} href="${href}"${b}>${inner}</a>`; changed = true; httpsUp++; } }
              // D-200: sources on other agents' and brokerages' sites stay as citations but pass no ranking credit (rel="nofollow")
              const host = (href.match(/^https?:\/\/(?:www\.)?([^/:?#]+)/i) || [])[1]?.toLowerCase();
              if (host && OTHER_AGENTS.some((d) => host === d || host.endsWith('.' + d))) { changed = true; unlinked++; return inner; }
              if (!host || !NOFOLLOW_ONLY.some((d) => host === d || host.endsWith('.' + d))) return all;
              const attrs = a + b;
              if (/\brel="[^"]*\bnofollow\b/.test(attrs)) return all;
              changed = true; nofollow++;
              if (/\srel="/.test(a)) return `<a${a.replace(/\srel="([^"]*)"/, ' rel="$1 nofollow"')} href="${href}"${b}>${inner}</a>`;
              if (/\srel="/.test(b)) return `<a${a} href="${href}"${b.replace(/\srel="([^"]*)"/, ' rel="$1 nofollow"')}>${inner}</a>`;
              return `<a${a} href="${href}" rel="nofollow"${b}>${inner}</a>`;
            }
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
          { const before = t; for (const [re, to] of WORDING) t = t.replace(re, to); if (t !== before) { changed = true; wording++; } }
          if (changed) fs.writeFileSync(f, t);
        }
        console.log(`[fix-links] rewritten ${rewritten}, removed ${dropped}, unresolved ${unresolved.size}, headings fixed ${headingsFixed}, wording ${wording} pages, nofollow ${nofollow}, other-agent links unlinked ${unlinked}, http→https ${httpsUp}`);
        if (unresolved.size) fs.writeFileSync(path.join(root, '..', 'link-unresolved.json'), JSON.stringify([...unresolved], null, 1));
        else if (fs.existsSync(path.join(root, '..', 'link-unresolved.json'))) fs.unlinkSync(path.join(root, '..', 'link-unresolved.json'));
      },
    },
  };
}
