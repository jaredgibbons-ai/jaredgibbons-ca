// Pure maths for the mortgage calculator (src/components/MortgageCalc.astro) and its tests.
// Every figure here comes from an official page and is listed in docs/04-decisions-and-exceptions.md (D-100):
//  - BC property transfer tax rates, first-time buyer and newly built exemptions: www2.gov.bc.ca (property transfer tax pages, checked 2026-11-04)
//  - CMHC premium by loan-to-value: cmhc-schl.gc.ca "CMHC mortgage loan insurance cost" (checked 2026-11-04)
//  - Canadian fixed-rate mortgages compound semi-annually (Interest Act). Minimum down payment rule is the one already stated on /mortgage-calculator.html.
// No interest rate is built in: the visitor types the rate their lender quoted.

export const PAY_PER_YEAR = { monthly: 12, semimonthly: 24, biweekly: 26, weekly: 52 };

/** BC property transfer tax before exemptions. 1% to $200k, 2% to $2M, 3% above, a further 2% on residential value above $3M. */
export function ptt(price) {
  if (!(price > 0)) return 0;
  let t = Math.min(price, 200000) * 0.01;
  if (price > 200000) t += (Math.min(price, 2000000) - 200000) * 0.02;
  if (price > 2000000) t += (price - 2000000) * 0.03;
  if (price > 3000000) t += (price - 3000000) * 0.02;
  return t;
}

/** First-time home buyers' exemption (registered on or after April 1, 2024), assuming every buyer qualifies. */
export function firstTimeExemption(price, tax = ptt(price)) {
  let e;
  if (price <= 500000) e = tax;
  else if (price <= 835000) e = 8000;
  else if (price < 860000) e = 8000 - 320 * ((price - 835000) / 1000);
  else e = 0;
  return Math.max(0, Math.min(e, tax));
}

/** Newly built home exemption (registered on or after April 1, 2024): full to $1.1M, phased out to $0 at $1.15M. */
export function newBuildExemption(price, tax = ptt(price)) {
  if (price <= 1100000) return tax;
  if (price < 1150000) return tax * ((1150000 - price) / 50000);
  return 0;
}

/** CMHC premium rate (percent of the loan) for a loan-to-value ratio in percent, or null above 95%. */
export function premiumPct(ltv) {
  if (ltv <= 65) return 0.6;
  if (ltv <= 75) return 1.7;
  if (ltv <= 80) return 2.4;
  if (ltv <= 85) return 2.8;
  if (ltv <= 90) return 3.1;
  if (ltv <= 95) return 4.0;
  return null;
}

/** Minimum down payment in dollars: 5% of the first $500,000, 10% of the part to $1.5M, 20% at $1.5M and above. */
export function minDown(price) {
  if (price >= 1500000) return price * 0.2;
  if (price <= 500000) return price * 0.05;
  return 25000 + (price - 500000) * 0.1;
}

/** Periodic payment on a Canadian fixed-rate mortgage (semi-annual compounding). ratePct is the nominal annual rate in percent. */
export function payment(loan, ratePct, years, perYear) {
  const n = Math.round(years * perYear);
  if (!(loan > 0) || n <= 0) return 0;
  if (!(ratePct > 0)) return loan / n;
  const i = Math.pow(1 + ratePct / 200, 2 / perYear) - 1;
  return (loan * i) / (1 - Math.pow(1 + i, -n));
}

/**
 * Full estimate. opts: { price, downPct, ratePct (null when blank), years, freq, exemption: 'none'|'first'|'new' }
 * Returns numbers plus a list of plain-language notices.
 */
export function estimate(o) {
  const price = o.price, notices = [];
  const down = price * (o.downPct / 100);
  const tax = ptt(price);
  const exempt = o.exemption === 'first' ? firstTimeExemption(price, tax) : o.exemption === 'new' ? newBuildExemption(price, tax) : 0;
  const r = { price, down, tax, exempt, taxDue: tax - exempt, premium: 0, premiumPct: 0, loan: price - down, pay: null, perYear: PAY_PER_YEAR[o.freq] || 12, notices };
  const need = minDown(price);
  if (down + 0.005 < need) notices.push('The minimum down payment at this price is about $' + Math.round(need).toLocaleString('en-CA') + '. Below that, a lender will not approve the mortgage.');
  if (o.downPct < 20) {
    if (price >= 1500000) notices.push('Homes at $1,500,000 or more cannot have default-insured mortgages, so lenders ask for at least 20% down.');
    else {
      const ltv = ((price - down) / price) * 100, pct = premiumPct(ltv);
      if (pct == null) notices.push('The down payment is under the 5% minimum, so no insurance premium can be shown.');
      else {
        r.premiumPct = pct; r.premium = r.loan * (pct / 100); r.loan += r.premium;
        if (o.years > 25) notices.push('Insured mortgages over 25 years are limited to certain buyers, and your lender may add to the premium shown. Ask your lender.');
      }
    }
  }
  if (o.ratePct != null) r.pay = payment(r.loan, o.ratePct, o.years, r.perYear);
  r.cash = down + r.taxDue;
  return r;
}
