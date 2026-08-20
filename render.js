// render.js - Node script using Puppeteer to render index.html or a URL to PDF
// Usage: node render.js <path-or-url> [output.pdf]

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

(async () => {
  const target = process.argv[2] || `file://${path.resolve(__dirname, 'index.html')}`;
  const out = process.argv[3] || 'cmy-rd-dashboard.pdf';

  console.log('Rendering', target, '->', out);
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 900, deviceScaleFactor: 2 });
  await page.goto(target, { waitUntil: 'networkidle0' });
  // wait a moment for charts to paint
  await page.waitForTimeout(800);
  await page.pdf({ path: out, format: 'A4', printBackground: true, margin: { top: '10mm', bottom: '10mm', left: '8mm', right: '8mm' } });
  await browser.close();
  console.log('Done. PDF saved to', out);
})();
