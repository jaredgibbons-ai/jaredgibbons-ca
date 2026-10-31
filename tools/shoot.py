import sys, asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:4321'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, vp, mobile in [('desktop',{'width':1440,'height':900},False),('mobile',{'width':390,'height':844},True)]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobile, has_touch=mobile)
            pg = await ctx.new_page()
            msgs=[]
            pg.on('console', lambda m: msgs.append(m.text) if m.type in ('error','warning') else None)
            pg.on('requestfailed', lambda r: msgs.append('FAILED '+r.url))
            for slug, path in [('home','/'),('fort-langley','/fort-langley.html'),('reviews','/reviews.html')]:
                await pg.goto(BASE+path, wait_until='networkidle')
                await pg.screenshot(path=f'shots/{slug}-{name}-top.png')
                await pg.screenshot(path=f'shots/{slug}-{name}-full.png', full_page=True)
            print(name, msgs)
            await ctx.close()
        await b.close()
asyncio.run(main())
