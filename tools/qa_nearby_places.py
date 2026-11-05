# Headless check of the "Show nearby places" buttons against a stand-in for Google (no network). Needs `PUBLIC_GOOGLE_MAPS_KEY=TESTKEY npm run build`, `python3 -m http.server 4399` in dist/, then: python3 tools/qa_nearby_places.py <page.html>
import sys, json
from playwright.sync_api import sync_playwright
STUB = r"""
(function(){
  const calls = window.__calls = [];
  class LatLng{constructor(a,b){this._a=a;this._b=b} lat(){return this._a} lng(){return this._b}}
  class OverlayView{ setMap(m){ if(m){ this._m=m; this.onAdd&&this.onAdd(); this.draw&&this.draw(); } else { this.onRemove&&this.onRemove(); } } getPanes(){ const mk=()=>{let d=document.querySelector('.stub-pane'); if(!d){d=document.createElement('div');d.className='stub-pane';document.querySelector('.areamap__map').appendChild(d);} return d;}; return {floatPane:mk(),overlayMouseTarget:mk()}; } getProjection(){ return {fromLatLngToDivPixel:()=>({x:100,y:100})}; } }
  class MapC{constructor(h,o){this.h=h;this.o=o} fitBounds(){} getCenter(){return new LatLng(49.1,-122.7)} getBounds(){return {getNorthEast:()=>({lat:()=>49.14,lng:()=>-122.65}),getSouthWest:()=>({lat:()=>49.06,lng:()=>-122.75})}}}
  class Poly{constructor(o){this.o=o} addListener(){} setOptions(){}}
  class IW{setContent(){} setPosition(){} open(){}}
  const Place={ searchNearby: async (req)=>{ calls.push(req); const base=req.locationRestriction.center; return {places:[{displayName:'B '+req.includedPrimaryTypes[0],location:new LatLng(base.lat+0.01,base.lng)},{displayName:'A '+req.includedPrimaryTypes[0],location:new LatLng(base.lat+0.002,base.lng)}]}; } };
  window.google={maps:{OverlayView,LatLng,InfoWindow:IW,event:{trigger(){}},importLibrary: async (n)=>{ if(n==='maps') return {Map:MapC,Polygon:Poly,InfoWindow:IW}; if(n==='places') return {Place}; if(n==='maps3d') throw new Error('no3d'); return {}; }}};
  setTimeout(()=>window.__gmapsReady&&window.__gmapsReady(),10);
})();
"""
page=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1200,'height':900})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('https://maps.googleapis.com/**',lambda r:r.fulfill(status=200,content_type='text/javascript',body=STUB))
    pg.goto(f'http://127.0.0.1:4399/{page}'); 
    pg.locator('.areamap__map').scroll_into_view_if_needed(); pg.wait_for_timeout(800)
    print('near hidden before map?', pg.locator('#areamap-near').get_attribute('hidden'))
    print('calls before press:', pg.evaluate('window.__calls.length'))
    pg.click('.areamap__nb[data-cat=park]'); pg.wait_for_timeout(300)
    print('calls after park:', pg.evaluate('window.__calls.length'))
    print('pressed:', pg.get_attribute('.areamap__nb[data-cat=park]','aria-pressed'))
    print('pins:', pg.locator('.areamap__pin').count(), 'list:', [t for t in pg.locator('#areamap-near-list li').all_inner_texts()])
    print('note:', pg.inner_text('#areamap-near-note'))
    pg.click('.areamap__nb[data-cat=cafe]'); pg.wait_for_timeout(300)
    print('pins after cafe:', pg.locator('.areamap__pin').count(), 'list:', pg.locator('#areamap-near-list li').all_inner_texts())
    print('req:', json.dumps(pg.evaluate('window.__calls[1]')))
    pg.click('.areamap__nb[data-cat=park]'); pg.wait_for_timeout(200)
    print('after park off -> pins:', pg.locator('.areamap__pin').count(), 'calls:', pg.evaluate('window.__calls.length'))
    pg.locator('#areamap-near').scroll_into_view_if_needed(); pg.screenshot(path='/tmp/near.png')
    print('errors:', errs)
    b.close()
