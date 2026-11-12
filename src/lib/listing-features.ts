// Standout features of a listing, read from its photo descriptions (src/data/photo-alts.json, D-250), for the search snippet (D-251).
// Only what a photo shows; nothing about condition or value. Nearby places and aerial context shots are ignored.
type Rule = [RegExp, string | ((strata: boolean) => string)];
const RULES: Rule[] = [
  [/\bcarriage house\b/, 'a carriage house'],
  [/\b(detached |large |metal )?shop\b(?!s|ping)/, 'a detached shop'],
  [/\b(outdoor|indoor|swimming|above-ground)? ?pool\b(?! table| and gym)/, (s) => (s ? 'a pool' : 'a pool')],
  [/\b(ocean|bay|harbour|water)\b.*\bview|view[^,]*\b(the )?(ocean|bay|harbour|false creek|water)\b/, 'ocean views'],
  [/\bmountain(s)? view|view[^,]*\bmountains?\b/, 'mountain views'],
  [/\bcity view|view[^,]*\b(city|skyline|downtown|towers)\b/, 'city views'],
  [/\brooftop (deck|terrace|patio)\b/, 'a rooftop deck'],
  [/\b(basement suite|suite (kitchen|living|bedroom|dining|room)|second kitchen)\b/, 'a suite'],
  [/\bbarn\b/, 'a barn'],
  [/\bgreenhouse\b/, 'a greenhouse'],
  [/\bhot tub\b/, 'a hot tub'],
  [/\bpond\b/, 'a pond'],
  [/\bcreek\b(?! trail)/, 'a creek'],
  [/\b(large|wide) terrace|\bterrace with\b/, 'a large terrace'],
  [/\bcovered (deck|patio)\b[^,]*\b(fireplace|fire table|outdoor kitchen)\b|\boutdoor (kitchen|living area)\b/, 'covered outdoor living'],
  [/\bgazebo\b/, 'a gazebo'],
  [/\bvaulted\b/, 'vaulted ceilings'],
  [/\b(double|triple) garage/, 'a double garage'],
  [/\bclubhouse\b|\bamenity (lounge|room)\b|\bfitness (room|centre)\b/, 'building amenities'],
  [/\bfireplace\b/, 'a fireplace'],
];
const SKIP = /^(nearby|floor plan|aerial view of the (area|town|neighbourhood|city|street|residential)|aerial view (along|toward|over the city|over the rooftops))/i;
export function listingFeatures(alts: string[], strata = false): string[] {
  const text = alts.filter((a) => a && !SKIP.test(a)).map((a) => a.toLowerCase());
  const out: string[] = [];
  for (const [re, label] of RULES) {
    if (!text.some((t) => re.test(t))) continue;
    const l = typeof label === 'string' ? label : label(strata);
    if (!out.includes(l)) out.push(l);
  }
  // one view phrase is enough
  const views = out.filter((x) => x.endsWith('views'));
  return out.filter((x) => !x.endsWith('views') || x === views[0]);
}
