// Renders the LinkedIn banner:
//   aoe-linkedin-banner-1584x396.png     upload this (LinkedIn's exact size)
//   aoe-linkedin-banner-3168x792@2x.png  sharper master for high-density screens
//   preview-with-guides.png              shows the profile-photo area and mobile side crop
// Requires Playwright (npm i -D playwright, or a global install).
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const url = 'file://' + path.join(__dirname, 'banner.html');
  const browser = await chromium.launch();
  const shots = [
    { scale: 1, query: '', file: 'aoe-linkedin-banner-1584x396.png' },
    { scale: 2, query: '', file: 'aoe-linkedin-banner-3168x792@2x.png' },
    { scale: 1, query: '?guides=1', file: 'preview-with-guides.png' },
  ];
  for (const s of shots) {
    const page = await browser.newPage({ viewport: { width: 1584, height: 396 }, deviceScaleFactor: s.scale });
    await page.goto(url + s.query);
    await page.evaluate(() => document.fonts.ready);
    await (await page.$('.banner')).screenshot({ path: path.join(__dirname, s.file) });
    await page.close();
    console.log('wrote', s.file);
  }
  await browser.close();
})();
