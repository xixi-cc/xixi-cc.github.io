"""Check every generated formula in a real browser against its retained TeX.

Run: uv run --with playwright python scripts/check_blog_rendering.py
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('response', lambda r: errors.append(f'{r.status}: {r.url}') if r.status >= 400 else None)
            page.route('https://static.cloudflareinsights.com/**', lambda r: r.abort())
            for width in (1440, 390):
                page.set_viewport_size({'width': width, 'height': 1000})
                for path in sorted(ROOT.glob('blog/*/index.html')):
                    page.goto(f'http://127.0.0.1:{server.server_port}/blog/{path.parent.name}/')
                    expected = page.locator('.arithmatex').count()
                    if expected:
                        page.evaluate('MathJax.startup.promise')
                        page.evaluate('document.fonts.ready')
                    assert page.locator('mjx-merror, [data-mjx-error], mjx-utext').count() == 0, path
                    assert page.locator('.arithmatex').evaluate_all('(es)=>es.every(e=>e.querySelectorAll("mjx-container").length===1)'), path
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), path
                    if expected:
                        math = page.evaluate('()=>Array.from(MathJax.startup.document.math).map(x=>({tex:x.math,mml:MathJax.startup.toMML(x.root)}))')
                        for item in math:
                            if r'\Delta' in item['tex']:
                                assert '&#x394;' in item['mml'], item
                            if r'\begin{aligned}' in item['tex']:
                                assert '<mtable' in item['mml'], item
                    print(f'{path.parent.name}: {expected} expressions OK at {width}px')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
