# render.py - Playwright script (Python) to render index.html or URL to PDF
# Usage: python render.py [path-or-url] [output.pdf]

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.joinpath('index.html').as_uri()
    out = sys.argv[2] if len(sys.argv) > 2 else 'cmy-rd-dashboard.pdf'
    print(f'Rendering {target} -> {out}')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width':1200, 'height':900})
        page.goto(target, wait_until='networkidle')
        page.wait_for_timeout(800)
        page.pdf(path=out, format='A4', print_background=True, margin={'top':'10mm','bottom':'10mm','left':'8mm','right':'8mm'})
        browser.close()
    print('Done. PDF saved to', out)

if __name__ == '__main__':
    main()
