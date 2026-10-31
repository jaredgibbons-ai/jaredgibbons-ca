import asyncio
from playwright.async_api import async_playwright
BASE='http://localhost:4321'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        # desktop: communities mega panel via hover, keyboard open, Esc close
        ctx = await b.new_context(viewport={'width':1440,'height':900}); pg = await ctx.new_page()
        await pg.goto(BASE+'/fort-langley.html', wait_until='networkidle')
        await pg.hover('text=Communities'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='shots/i-desktop-mega.png', clip={'x':0,'y':0,'width':1440,'height':700})
        await pg.keyboard.press('Escape'); await pg.mouse.move(700,600)
        hidden = await pg.eval_on_selector('#np-3','e=>e.hidden'); print('mega hidden after Esc/mouseleave:', hidden)
        # keyboard: tab to a toggle, Enter opens, Escape closes & returns focus
        await pg.focus('button[aria-label="My Listings submenu"]'); await pg.keyboard.press('Enter')
        print('expanded after Enter:', await pg.get_attribute('button[aria-label="My Listings submenu"]','aria-expanded'))
        await pg.keyboard.press('Escape')
        print('expanded after Esc:', await pg.get_attribute('button[aria-label="My Listings submenu"]','aria-expanded'),
              'focus on toggle:', await pg.evaluate('document.activeElement.getAttribute("aria-label")'))
        # FAQ open + card hover/focus
        await pg.click('summary:has-text("Is Fort Langley a heritage area?")')
        await pg.locator('summary:has-text("Is Fort Langley a heritage area?")').scroll_into_view_if_needed()
        await pg.screenshot(path='shots/i-desktop-faq.png')
        await pg.locator('.pcard').nth(1).scroll_into_view_if_needed(); await pg.locator('.pcard').nth(1).hover()
        await pg.screenshot(path='shots/i-desktop-cardhover.png')
        await ctx.close()
        # mobile menu
        ctx = await b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True); pg = await ctx.new_page()
        await pg.goto(BASE+'/', wait_until='networkidle')
        await pg.tap('#menu-btn'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='shots/i-mobile-menu.png')
        print('menu label:', await pg.inner_text('#menu-btn'))
        await pg.tap('button[aria-label="Communities submenu"]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='shots/i-mobile-menu-open.png')
        await pg.tap('#menu-btn'); print('closed label:', await pg.inner_text('#menu-btn'))
        # no horizontal overflow
        for path in ['/','/fort-langley.html']:
            await pg.goto(BASE+path, wait_until='networkidle')
            print(path, 'overflow-x:', await pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth'))
        await b.close()
asyncio.run(main())
