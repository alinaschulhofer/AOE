// Renders every concept in both formats to PDF (exact trim size, vector text)
// and to PNG previews.
//
//   node export.js              -> all concepts
//   node export.js concept-2    -> only files whose name starts with "concept-2"
//
// Requires Playwright (npm i -D playwright, or a global install).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FORMATS = {
  h: { width: '210mm', height: '148mm', label: 'horizontal-210x148' },
  v: { width: '148mm', height: '210mm', label: 'portrait-148x210' },
  a4: { width: '210mm', height: '297mm', label: 'A4-210x297' },
};

(async () => {
  const filter = process.argv[2] || 'concept-';
  const dir = __dirname;
  const out = path.join(dir, 'export');
  fs.mkdirSync(out, { recursive: true });
  const concepts = fs.readdirSync(dir).filter(f => f.startsWith(filter) && f.endsWith('.html'));

  const browser = await chromium.launch();
  for (const file of concepts) {
    // Concepts that style body[data-theme="dark"] also get a dark export.
    const themes = fs.readFileSync(path.join(dir, file), 'utf8').includes('data-theme="dark"') ? ['', 'dark'] : [''];
    for (const theme of themes)
    for (const [key, fmt] of Object.entries(FORMATS)) {
      const page = await browser.newPage({ deviceScaleFactor: 3 });
      await page.goto('file://' + path.join(dir, file) + '?format=' + key + (theme ? '&theme=' + theme : ''));
      await page.evaluate(() => document.fonts.ready);
      const base = path.join(out, file.replace('.html', '') + (theme ? '-' + theme : '') + '--' + fmt.label);
      await page.emulateMedia({ media: 'print' });
      await page.pdf({ path: base + '.pdf', width: fmt.width, height: fmt.height, printBackground: true, preferCSSPageSize: true });
      await page.emulateMedia({ media: 'screen' });
      await (await page.$('.ad')).screenshot({ path: base + '.png' });
      await page.close();
      console.log('wrote', path.relative(dir, base) + '.{pdf,png}');
    }
  }
  await browser.close();
})();
