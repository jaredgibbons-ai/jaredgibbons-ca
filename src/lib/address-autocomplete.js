// Address suggestions for a plain text input (home evaluation, property check, contact, commute). Progressive enhancement:
// the input works without this; the Google script is only requested the first time someone clicks into the field.
// Uses the Places API (New) autocomplete data call from the browser with our restricted key. Suggestions are Google Maps content: they are shown while typing,
// never stored by us, and carry the required "Google Maps" attribution. Canada only, biased to the Fraser Valley.
import { loadGoogle } from './gmaps.js';

export const MIN_CHARS = 4, DELAY_MS = 300;
export const BIAS = { center: { lat: 49.1, lng: -122.7 }, radius: 60000 };
export const shouldSuggest = (text) => typeof text === 'string' && text.trim().length >= MIN_CHARS;

export function attachAddressAutocomplete(input, key) {
  if (!input || !key || input.dataset.addrReady) return;
  input.dataset.addrReady = '1';
  let lib = null, token = null, items = [], active = -1, timer = 0, seq = 0, loading = null;
  const id = input.id || `addr${Math.random().toString(36).slice(2, 7)}`;
  const box = document.createElement('div'); box.className = 'addrsug'; box.hidden = true;
  const list = document.createElement('ul'); list.id = `${id}-sug`; list.setAttribute('role', 'listbox'); list.setAttribute('aria-label', 'Address suggestions');
  const attr = document.createElement('p'); attr.className = 'addrsug__attr'; attr.setAttribute('translate', 'no'); attr.textContent = 'Google Maps';
  const live = document.createElement('div'); live.className = 'sr-only'; live.setAttribute('aria-live', 'polite');
  box.append(list, attr);
  input.insertAdjacentElement('afterend', box); box.insertAdjacentElement('afterend', live);
  input.setAttribute('role', 'combobox'); input.setAttribute('aria-autocomplete', 'list'); input.setAttribute('aria-expanded', 'false'); input.setAttribute('aria-controls', list.id); input.setAttribute('autocomplete', 'off');

  const close = () => { box.hidden = true; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); active = -1; };
  const mark = (i) => { active = i; [...list.children].forEach((li, n) => { li.setAttribute('aria-selected', String(n === i)); li.classList.toggle('is-active', n === i); }); if (i >= 0) input.setAttribute('aria-activedescendant', list.children[i].id); else input.removeAttribute('aria-activedescendant'); };
  const choose = (i) => { const it = items[i]; if (!it) return; input.value = it; input.dispatchEvent(new Event('input', { bubbles: true })); close(); token = null; };
  const show = (texts) => {
    items = texts; list.replaceChildren();
    texts.forEach((t, i) => { const li = document.createElement('li'); li.id = `${id}-o${i}`; li.setAttribute('role', 'option'); li.setAttribute('aria-selected', 'false'); li.textContent = t; li.addEventListener('mousedown', (e) => { e.preventDefault(); choose(i); }); list.appendChild(li); });
    if (!texts.length) { close(); live.textContent = ''; return; }
    box.hidden = false; input.setAttribute('aria-expanded', 'true'); live.textContent = `${texts.length} address suggestions. Use the up and down arrows, then Enter.`;
  };
  const ensure = () => loading || (loading = loadGoogle(key).then((g) => g.maps.importLibrary('places')).then((l) => { lib = l; }).catch(() => { loading = null; input.removeAttribute('role'); input.removeAttribute('aria-controls'); input.removeAttribute('aria-expanded'); input.removeAttribute('aria-autocomplete'); input.removeAttribute('autocomplete'); box.remove(); }));
  const ask = async () => {
    const text = input.value.trim(); const mine = ++seq;
    if (!shouldSuggest(text)) { show([]); return; }
    await ensure(); if (!lib) return;
    try {
      token = token || new lib.AutocompleteSessionToken();
      const { suggestions } = await lib.AutocompleteSuggestion.fetchAutocompleteSuggestions({ input: text, includedRegionCodes: ['ca'], locationBias: BIAS, sessionToken: token });
      if (mine !== seq) return;
      show((suggestions || []).map((s) => s.placePrediction && s.placePrediction.text && s.placePrediction.text.text).filter(Boolean).slice(0, 5));
    } catch { if (mine === seq) show([]); }
  };
  input.addEventListener('focus', () => { ensure(); });
  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(ask, DELAY_MS); });
  input.addEventListener('keydown', (e) => {
    if (box.hidden) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); mark((active + 1) % items.length); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); mark((active - 1 + items.length) % items.length); }
    else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); choose(active); }
    else if (e.key === 'Escape') { e.preventDefault(); close(); }
  });
  input.addEventListener('blur', () => setTimeout(close, 120));
}
