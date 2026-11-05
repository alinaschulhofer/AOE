const { chromium } = require('playwright');
const src = process.argv[2] || 'services-and-fees-source.html';
const out = process.argv[3] || 'Psychotherapy-Services-and-Fees.pdf';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + __dirname + '/' + src, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const info = await p.evaluate(() => {
    const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
    const pages = [...document.querySelectorAll('.page')].map(pg => {
      const f = pg.querySelector('.footer').getBoundingClientRect();
      const kids = [...pg.children].filter(c => !c.classList.contains('footer'));
      const last = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
      return { gapAboveFooter: Math.round(f.top - last), overflow: pg.scrollHeight - pg.clientHeight, footBottom: Math.round(f.bottom - pg.getBoundingClientRect().bottom) };
    });
    return { fonts: [...new Set(fonts)], pages };
  });
  console.log(JSON.stringify(info));
  const els = await p.$$('.page');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: require('os').tmpdir() + `/p${i+1}.png` });
  await p.pdf({ path: __dirname + '/' + out, width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
