// Renders the brochure HTML in this folder to a two-page A4 PDF.
// Usage: node brochures/build-pdf.js   (requires the `playwright` package)
const path = require('path');
const { chromium } = require('playwright');

const name = 'AOE_Executive_Leadership_360_Assessment';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, name + '.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(__dirname, name + '.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });
  await browser.close();
})();
