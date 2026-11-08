import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { NEWSLETTER_CONSENT_TEXT } from '../src/lib/newsletter.js';

const html = fs.readFileSync('dist/subscribe-to-our-newsletter.html', 'utf8');
test('newsletter page has a working sign-up form with an unticked consent box, honeypot and privacy link', () => {
  assert.match(html, /<form[^>]*data-nl/);
  assert.match(html, /name="consent" type="checkbox"/);
  assert.doesNotMatch(html, /name="consent"[^>]*checked/);
  assert.ok(html.includes(NEWSLETTER_CONSENT_TEXT));
  assert.match(html, /name="_hp_url"/);
  assert.match(html, /href="\/privacy\.html"/);
  assert.ok(html.includes('/api/forms/newsletter'));
});
test('newsletter page no longer carries the flattened archive form labels, and the form does not share the listing-alert hook', () => {
  assert.doesNotMatch(html, /Yes, I agree to be contacted and receive helpful emails/);
  assert.doesNotMatch(html, /\/api\/forms\/listing-alert/);
  assert.doesNotMatch(html, /data-la[ >]/);
});
test('privacy page covers newsletter sign-ups, consent records, reviews and the analytics and advertising statement', () => {
  const p = fs.readFileSync('dist/privacy.html', 'utf8');
  for (const re of [/newsletter/i, /record of what you agreed to/, /public Google Business Profile/, /uses Google Analytics and Google Ads measurement/, /Last updated November 8, 2026/]) assert.match(p, re);
});
