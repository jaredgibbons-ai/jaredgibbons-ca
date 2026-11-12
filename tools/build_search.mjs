// Site search index (D-238). Runs after `astro build`: node tools/build_search.mjs [outDir]
// Pagefind indexes each page's <main> into <outDir>/pagefind/ (static files; the search runs in the visitor's browser,
// no outside service). Pages are added with their PUBLIC address (blog posts and own listings are built under
// /internal/ but live at /blog.html/… and /our-listings.html/…). Pages that are noindex in the launch build (held,
// utility, 404) are left out; on the preview, where every page is noindex, everything but the 404 is indexed.
import * as pagefind from 'pagefind';
import fs from 'node:fs';
import path from 'node:path';

const out = process.argv[2] || 'dist';
const files = [];
(function walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) { if (e.name !== 'pagefind' && e.name !== '_astro') walk(p); } else if (e.name.endsWith('.html')) files.push(p); } })(out);

const publicUrl = (rel) => {
  rel = '/' + rel.split(path.sep).join('/');
  let m;
  if ((m = rel.match(/^\/internal\/blog\/(.+)\.html$/))) return `/blog.html/${m[1]}`;
  if ((m = rel.match(/^\/internal\/listings\/(.+)\.html$/))) return `/our-listings.html/${m[1]}`;
  if (rel === '/index.html') return '/';
  return rel;
};
const { index } = await pagefind.createIndex({ rootSelector: 'main', excludeSelectors: ['nav', '.crumbs', '.toc', '[data-pagefind-ignore]', 'form', '.idx', '.ig', '.mt', 'script', 'style', 'section[aria-labelledby^="h-reviews"]', '.reviews', '.awm', '.seen'] });
let added = 0, skipped = 0;
for (const f of files) {
  const rel = path.relative(out, f);
  if (rel === '404.html' || rel.startsWith('internal' + path.sep) && !/^internal[\\/](blog|listings)[\\/]/.test(rel)) { skipped++; continue; }
  const html = fs.readFileSync(f, 'utf8');
  const preview = html.includes('class="preview-banner"');
  const robots = (html.match(/<meta name="robots" content="([^"]*)"/) || [])[1] || '';
  if (!preview && /noindex/i.test(robots)) { skipped++; continue; }
  if (!/<main[\s>]/.test(html)) { skipped++; continue; }
  // The page's search title counts most: its words are added once, weighted, at the top of the indexed area.
  const title = ((html.match(/<title>([^<]*)<\/title>/) || [])[1] || '').split(' | ')[0].trim();
  // (own listing pages get no boost, so a place name finds the area pages before individual sold homes)
  const boost = title && !rel.startsWith('internal' + path.sep + 'listings');
  const content = title ? html.replace(/<main([^>]*)>/, (_, a) => `<main${a}><p ${boost ? 'data-pagefind-weight="10" ' : ''}data-pagefind-meta="title">${title}</p>`) : html;
  const { errors } = await index.addHTMLFile({ url: publicUrl(rel), content });
  if (errors?.length) { console.error(rel, errors); skipped++; } else added++;
}
await index.writeFiles({ outputPath: path.join(out, 'pagefind') });
await pagefind.close();
console.log(`[search] ${added} pages indexed, ${skipped} skipped -> ${out}/pagefind`);
