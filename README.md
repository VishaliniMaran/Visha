# CMY R&D Dashboard

This repo adds a single-page dashboard to showcase CMY R&D services and includes scripts to generate a PDF snapshot.

Files added:
- index.html - dashboard UI (Chart.js) with embedded sample data
- styles.css - styling
- script.js - chart rendering and browser PDF export
- render.js - Node + Puppeteer script to render index.html or a URL to PDF
- render.py - Python Playwright script to render index.html or a URL to PDF
- README.md - this file


Quick start (Node / Puppeteer)

1. Clone the repo (or work in this repo):
   git clone https://github.com/VishaliniMaran/Visha.git
   cd Visha

2. Install dependencies:
   npm init -y
   npm install puppeteer

3. Render PDF (local file):
   node render.js

   Or render a hosted URL:
   node render.js https://example.com/path/to/index.html out.pdf


Python (Playwright)

1. Set up virtualenv and install Playwright:
   python -m venv .venv
   source .venv/bin/activate    # Windows: .venv\\Scripts\\activate
   pip install playwright
   playwright install

2. Run the renderer:
   python render.py


Browser export (quick)

Open index.html in your browser and click "Export PDF (browser)" — this uses html2canvas + jsPDF to produce a PDF.


Notes

- The dashboard uses the provided sample data (Project Coordination, Testing, Documentation) baked into script.js.
- The Node script uses Puppeteer; in CI environments you may need additional flags or packages (see Puppeteer docs).
- The Python script uses Playwright sync API to render the page.

