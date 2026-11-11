// Builds both PDFs from index.html:  node decks/educational-programs/build.js
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  const src = 'file://' + path.join(__dirname, 'index.html');
  const out = path.join(__dirname, '..', '..', 'assets');
  for (const [theme, name] of [['dark', 'Dark'], ['light', 'Light']]) {
    await page.goto(`${src}?theme=${theme}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(out, `AOE_Educational_Programs_${name}.pdf`),
      format: 'A4', printBackground: true, preferCSSPageSize: true,
    });
  }
  await browser.close();
})();
