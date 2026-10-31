"""axe (WCAG 2.0-2.2 A/AA + best-practice), horizontal overflow, console errors for every built page.

    python3 tools/a11y_all.py --root dist --port 4322 [--workers 4] [--out docs/test-results/a11y-all.json]

Serves a snapshot of dist/ itself, so rebuilding dist while this runs is safe when --root is a copy.
Desktop (1440) and mobile (390) page-views for every page, post and listing."""
import argparse, asyncio, http.server, json, os, socketserver, threading
from playwright.async_api import async_playwright

ap = argparse.ArgumentParser()
ap.add_argument('--root', default='dist'); ap.add_argument('--port', type=int, default=4322)
ap.add_argument('--workers', type=int, default=4); ap.add_argument('--out', default='docs/test-results/a11y-all.json')
ap.add_argument('--limit', type=int, default=0)
a = ap.parse_args()
AXE = open('node_modules/axe-core/axe.min.js').read()

paths = []
for dp, _, fs in os.walk(a.root):
    for f in fs:
        if f.endswith('.html'):
            paths.append('/' + os.path.relpath(os.path.join(dp, f), a.root).replace(os.sep, '/'))
paths.sort()
if a.limit: paths = paths[:a.limit]

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *x, **k): super().__init__(*x, directory=a.root, **k)
    def log_message(s, *x): pass
socketserver.ThreadingTCPServer.allow_reuse_address = True
srv = socketserver.ThreadingTCPServer(('127.0.0.1', a.port), H); srv.daemon_threads = True
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{a.port}'
VIEWS = [('desktop', {'width': 1440, 'height': 900}, False), ('mobile', {'width': 390, 'height': 844}, True)]

async def worker(b, q, out):
    ctxs = {}
    for name, vp, mob in VIEWS:
        ctxs[name] = await b.new_context(viewport=vp, is_mobile=mob, has_touch=mob)
    while True:
        try: path = q.get_nowait()
        except asyncio.QueueEmpty: break
        for name, vp, mob in VIEWS:
            pg = await ctxs[name].new_page(); errs = []
            pg.on('console', lambda m, e=errs: e.append(m.text[:120]) if m.type == 'error' else None)
            pg.on('requestfailed', lambda r, e=errs: e.append('FAILED ' + r.url[:100]))
            try:
                await pg.goto(BASE + path, wait_until='load', timeout=30000)
                await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
                await pg.evaluate(AXE)
                r = await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}}).then(r=>r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length})))")
                ow = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                out[f'{path}|{name}'] = dict(axe=r, overflow=ow, errors=errs[:3])
            except Exception as e:                      # noqa: BLE001
                out[f'{path}|{name}'] = dict(error=repr(e)[:200])
            await pg.close()
    for c in ctxs.values(): await c.close()

async def main():
    q = asyncio.Queue()
    for p in paths: q.put_nowait(p)
    out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        await asyncio.gather(*[worker(b, q, out) for _ in range(a.workers)])
        await b.close()
    json.dump(out, open(a.out, 'w'), indent=0)
    agg = {}
    for k, v in out.items():
        for x in v.get('axe', []):
            g = agg.setdefault((x['id'], x['impact']), [0, 0]); g[0] += 1; g[1] += x['n']
    print('page-views', len(out), '| errors', sum(1 for v in out.values() if 'error' in v),
          '| overflow>0', sum(1 for v in out.values() if v.get('overflow', 0) > 0),
          '| console/network errors', sum(1 for v in out.values() if v.get('errors')))
    for (i, imp), (pg_, n) in sorted(agg.items(), key=lambda x: -x[1][0]): print(f'  axe {i} [{imp}] on {pg_} page-views, {n} nodes')

asyncio.run(main())
