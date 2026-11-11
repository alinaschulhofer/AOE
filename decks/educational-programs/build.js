// Builds both PDFs from index.html:  node decks/educational-programs/build.js
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const src = 'file://' + path.join(__dirname, 'index.html');
  const out = path.join(__dirname, '..', '..', 'assets');
  for (const [theme, name] of [['dark', 'Dark'], ['light', 'Light']]) {
    await page.goto(`${src}?theme=${theme}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(out, `AOE_Educational_Programs_${name}.pdf`),
      width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true,
    });
  }
  await browser.close();
})();
