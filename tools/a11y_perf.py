import asyncio, json
from playwright.async_api import async_playwright
BASE='http://localhost:4321'
AXE=open('node_modules/axe-core/axe.min.js').read()
async def main():
    out={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,vp,mob in [('desktop',{'width':1440,'height':900},False),('mobile',{'width':390,'height':844},True)]:
            ctx=await b.new_context(viewport=vp,is_mobile=mob,has_touch=mob)
            pg=await ctx.new_page()
            for slug,path in [('home','/'),('fort-langley','/fort-langley.html')]:
                await pg.add_init_script("""window.__m={cls:0,lcp:0};new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__m.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())window.__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});""")
                await pg.goto(BASE+path,wait_until='networkidle')
                await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                await pg.evaluate(AXE)
                r=await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}}).then(r=>({v:r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,help:v.help,ex:v.nodes[0].target.join(' ')})),passes:r.passes.length}))")
                m=await pg.evaluate("window.__m")
                out[f'{slug}-{name}']=dict(axe_violations=r['v'],axe_passes=r['passes'],lab_lcp_ms=round(m['lcp']),lab_cls=round(m['cls'],4))
            await ctx.close()
        await b.close()
    json.dump(out,open('docs/test-results/a11y-perf-lab.json','w'),indent=1)
    for k,v in out.items(): print(k,'LCP',v['lab_lcp_ms'],'CLS',v['lab_cls'],'axe:',[(x['id'],x['impact'],x['n']) for x in v['axe_violations']])
asyncio.run(main())
