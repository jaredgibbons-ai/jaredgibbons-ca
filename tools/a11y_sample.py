"""axe + lab CLS/LCP over a sample of generated pages.  python3 tools/a11y_sample.py slug,slug,...  (server on :4321)"""
import asyncio, json, sys
from playwright.async_api import async_playwright
BASE = 'http://localhost:4321'
AXE = open('node_modules/axe-core/axe.min.js').read()
slugs = sys.argv[1].split(',')
OUT = sys.argv[2] if len(sys.argv) > 2 else 'docs/test-results/a11y-generic-sample.json'
async def main():
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp, mob in [('desktop', {'width': 1440, 'height': 900}, False), ('mobile', {'width': 390, 'height': 844}, True)]:
            ctx = await b.new_context(viewport=vp, is_mobile=mob, has_touch=mob)
            pg = await ctx.new_page()
            for slug in slugs:
                await pg.add_init_script("window.__m={cls:0,lcp:0};new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__m.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{const e=l.getEntries().pop();if(e)window.__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});")
                await pg.goto(f'{BASE}/{slug}.html' if not slug.startswith('=') else BASE + slug[1:], wait_until='networkidle')
                await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                await pg.evaluate(AXE)
                r = await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}}).then(r=>({v:r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length})),passes:r.passes.length}))")
                m = await pg.evaluate("window.__m")
                ow = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                out[f'{slug[:70]}-{name}'] = dict(axe=r['v'], lcp_ms=round(m['lcp']), cls=round(m['cls'], 4), h_overflow_px=ow)
            await ctx.close()
        await b.close()
    json.dump(out, open(OUT, 'w'), indent=1)
    agg = {}
    for k, v in out.items():
        for x in v['axe']: agg.setdefault((x['id'], x['impact']), [0, 0]); agg[(x['id'], x['impact'])][0] += 1; agg[(x['id'], x['impact'])][1] += x['n']
    print('page-views', len(out), '| max LCP', max(v['lcp_ms'] for v in out.values()), 'ms | max CLS', max(v['cls'] for v in out.values()), '| overflow>0:', [k for k, v in out.items() if v['h_overflow_px'] > 0])
    for (i, imp), (pages, nodes) in sorted(agg.items(), key=lambda x: -x[1][0]): print(f'  axe {i} [{imp}] on {pages} page-views, {nodes} nodes')
asyncio.run(main())
