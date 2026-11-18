/* Runs inside MyRealPage's listing pages for jaredgibbons.ca (D-347). Loaded by MyRealPage itself: Listings > Settings > Advanced >
   Custom Footer Content holds one <script> tag pointing at this file. To undo, delete that line in MyRealPage.
   1. A listing opened on its own (a share link, a link in a listing alert email) is shown on jaredgibbons.ca instead.
   2. The share buttons (copy link, Facebook, X, Pinterest) hand out the jaredgibbons.ca address, not idx.myrealpage.com. */
(function () {
  var SITE = 'https://jaredgibbons.ca/recip.html/';
  var LISTING = /(listing\.[a-z0-9.\-]+\.\d{6,})/i;
  var framed;
  try { framed = window.top !== window.self; } catch (e) { framed = true; }
  var here = location.pathname.match(new RegExp('/' + LISTING.source + '/?$', 'i'));
  if (here && !framed) { location.replace(SITE + here[1]); return; }

  var PLAIN = /https?:\/\/idx\.myrealpage\.com\/[^\s"'&]*?(listing\.[a-z0-9.\-]+\.\d{6,})/gi;
  var ENCODED = /https?%3A%2F%2Fidx\.myrealpage\.com[^&\s"']*?(listing\.[a-z0-9.\-]+\.\d{6,})/gi;
  function swap(u) {
    return u.replace(ENCODED, function (_, l) { return encodeURIComponent(SITE + l); })
            .replace(PLAIN, function (_, l) { return SITE + l; });
  }
  function fix() {
    var els = document.querySelectorAll('[data-url*="idx.myrealpage.com"]');
    for (var i = 0; i < els.length; i++) {
      var u = els[i].getAttribute('data-url'), n = swap(u);
      if (n !== u) els[i].setAttribute('data-url', n);
    }
  }
  function start() {
    fix();
    if (window.MutationObserver && document.body) {
      new MutationObserver(fix).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['data-url'] });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
