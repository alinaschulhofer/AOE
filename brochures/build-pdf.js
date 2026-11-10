// Renders every brochure HTML file in this folder to a two-page A4 PDF.
// Usage: node brochures/build-pdf.js   (requires the `playwright` package)
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  for (const file of fs.readdirSync(__dirname).filter((f) => f.endsWith('.html'))) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(__dirname, file));
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(__dirname, file.replace(/\.html$/, '.pdf')),
      format: 'A4',
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
    });
    await page.close();
  }
  await browser.close();
})();
