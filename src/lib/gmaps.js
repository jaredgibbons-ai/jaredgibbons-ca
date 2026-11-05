// One loader for every Google Maps feature on the site (neighbourhood maps, address autocomplete, commute time, 3D flyover).
// The script is added once, only when something needs it, and every feature asks for its own library with importLibrary.
// Key: PUBLIC_GOOGLE_MAPS_KEY, a browser key restricted to our domains and to the APIs listed in docs/google-maps-key-setup.md.
let pending = null;
const failHandlers = [];

export function loadGoogle(key) {
  if (typeof window === 'undefined') return Promise.reject(new Error('no window'));
  if (window.google?.maps?.importLibrary) return Promise.resolve(window.google);
  if (pending) return pending;
  pending = new Promise((resolve, reject) => {
    const cb = '__gmapsReady';
    window[cb] = () => resolve(window.google);
    const s = document.createElement('script');
    s.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(key)}&v=weekly&loading=async&callback=${cb}`;
    s.async = true;
    s.onerror = () => { pending = null; reject(new Error('script')); };
    document.head.appendChild(s);
  });
  return pending;
}

/** Google calls window.gm_authFailure when the key is refused (wrong domain, API not allowed, billing off). Every feature can listen. */
export function onAuthFailure(fn) {
  failHandlers.push(fn);
  window.gm_authFailure = () => failHandlers.forEach((h) => { try { h(); } catch { /* keep going */ } });
}
