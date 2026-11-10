// Copy hygiene for published pages (D-194, from the Nov 9 QA review): no research-note wording, no dead feed link,
// no old awards block, no missing-value sentences, no doubled generator words.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const DIRS = ['src/data/local', 'src/data/pages', 'src/data/posts', 'src/data/designed'];
const files = [];
for (const d of DIRS) for (const f of fs.readdirSync(d)) if (f.endsWith('.json')) files.push([`${d}/${f}`, fs.readFileSync(path.join(d, f), 'utf8')]);
// link targets are allowed to contain anything; check only the words a reader sees
// preview-only review notes ("Draft for Jared…") never reach the launch build (src/lib/preview.ts)
const words = (t) => t.replace(/"(?:h|href|url|src|slug|path|canonical)"\s*:\s*"[^"]*"/g, '""').replace(/"Draft for Jared(?:[^"\\]|\\.)*"/g, '""')
  .replace(/"needs_from_muse"\s*:\s*\[[^\]]*\]/g, '[]');   // internal request list, not rendered

const RULES = [
  ['research-note heading', /What is not confirmed about/],
  ['research voice', /\bnot (?:been )?(?:confirmed|verified)\b|\bun(?:confirmed|verified)\b|\bsources? (?:read|checked|opened)\b|\bin any pass\b|\bFresh-verified\b/i],
  ['dead RSS link', /blog\.feed/],
  ['old awards block', /Medallion Club Qualifier|Top 10% in the Fraser Valley Real Estate Board/],
  ['missing sales ratio', /sales ratio of (?:—|not published)/],
  ['Between … to', /Between November 2025 to/],
  ['doubled words', /real estate real estate|Rural homes Homes/],
  ['jargon', /\bsolds\b/],
  // D-199 (Nov 10 review): "verified" as a research note, a medians line that read as if the site had none, a dropped area name
  ['research "verified"', /\b[Nn]o verified\b|\bnowhere verified\b|\b[Nn]one (?:was|were) verified\b|\bverified by name\b/],
  ['medians line', /\b(?:Per-sub-area|Sub-area) medians are not published\b/],
  ['dropped area name', /\b(?:lines|buildings|complexes|co-operatives|residences|towers|figures|addresses|listing|named) in (?:are|is|sits|sit|have|has)\b/],
  ['generator doubles', /\bspecific specific\b|\brecords records\b/],
];

for (const [name, re] of RULES) {
  test(`page copy: no ${name}`, () => {
    const bad = files.filter(([, t]) => re.test(words(t))).map(([f]) => f);
    assert.equal(bad.length, 0, `${bad.length} files, e.g. ${bad.slice(0, 5).join(', ')}`);
  });
}

test('listing page: the "not connected in the preview" note is preview-only', () => {
  const t = fs.readFileSync('src/components/ListingPage.astro', 'utf8');
  assert.match(t, /\{isPreview && page\.status === 'Active' && \(/);
});
