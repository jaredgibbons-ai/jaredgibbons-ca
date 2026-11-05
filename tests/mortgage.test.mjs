import test from 'node:test';
import assert from 'node:assert/strict';
import { ptt, firstTimeExemption, newBuildExemption, premiumPct, minDown, payment, estimate } from '../src/lib/mortgage.js';

// Examples below are the worked examples on the gov.bc.ca property transfer tax pages (checked 2026-11-04).
test('property transfer tax matches the BC worked examples', () => {
  assert.equal(ptt(650000), 11000);
  assert.equal(ptt(500000), 8000);
  assert.equal(ptt(4500000), 143000);
  assert.equal(ptt(860000), 15200);
  assert.equal(ptt(1120000), 20400);
});

test('first-time buyer exemption follows the gov.bc.ca table', () => {
  assert.equal(firstTimeExemption(475000), 7500);
  assert.equal(ptt(800000) - firstTimeExemption(800000), 6000);
  assert.equal(firstTimeExemption(835000), 8000);
  assert.ok(Math.abs(firstTimeExemption(836000) - 7680) < 1e-6);
  assert.ok(Math.abs(firstTimeExemption(850000) - 3200) < 1e-6);
  assert.equal(firstTimeExemption(860000), 0);
});

test('newly built home exemption is full to $1.1M and phases out at $1.15M', () => {
  assert.equal(newBuildExemption(1100000), 20000);
  assert.ok(Math.abs(newBuildExemption(1120000) - 12240) < 1e-6);
  assert.equal(newBuildExemption(1150000), 0);
});

test('CMHC premium bands and minimum down payment', () => {
  assert.equal(premiumPct(65), 0.6); assert.equal(premiumPct(80), 2.4); assert.equal(premiumPct(85), 2.8);
  assert.equal(premiumPct(90), 3.1); assert.equal(premiumPct(95), 4.0); assert.equal(premiumPct(95.1), null);
  assert.equal(minDown(500000), 25000); assert.equal(minDown(1000000), 75000); assert.equal(minDown(1500000), 300000);
});

test('payment uses semi-annual compounding', () => {
  const m = payment(400000, 5, 25, 12);
  assert.ok(Math.abs(m - 2327.4) < 1, String(m)); // $400,000 at 5.00% over 25 years, monthly
  assert.ok(Math.abs(payment(120000, 0, 10, 12) - 1000) < 1e-9);
  assert.equal(payment(0, 5, 25, 12), 0);
});

test('estimate adds the premium to the loan and flags rules', () => {
  const e = estimate({ price: 700000, downPct: 10, ratePct: null, years: 25, freq: 'monthly', exemption: 'none' });
  assert.equal(e.pay, null);
  assert.ok(Math.abs(e.premium - 630000 * 0.031) < 1e-6);
  assert.ok(Math.abs(e.loan - 630000 * 1.031) < 1e-6);
  const big = estimate({ price: 1800000, downPct: 10, ratePct: 5, years: 25, freq: 'monthly', exemption: 'none' });
  assert.ok(big.notices.length >= 1);
  const low = estimate({ price: 700000, downPct: 3, ratePct: 5, years: 25, freq: 'monthly', exemption: 'none' });
  assert.ok(low.notices.some((n) => /minimum down payment/.test(n)));
});
