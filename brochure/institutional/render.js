// Renders the institutional brochure to PDF (dark + light), page previews, and
// standalone vector SVGs of every diagram.  Usage: node render.js [previewDir]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PREV = process.argv[2] || path.join(__dirname, 'previews');
// Document A is the complete reference; B and C are shorter modular editions built from the same pages.
const DOCS = [
  { src: 'institutional.html', pdf: 'AOE_Institutional_Framework', tag: 'A', diagrams: true },
  { src: 'competency-framework.html', pdf: 'AOE_Competency_Framework', tag: 'B' },
  { src: 'implementation-methodology.html', pdf: 'AOE_Implementation_Methodology', tag: 'C' },
  { src: 'pillar-reference-internal.html', pdf: 'AOE_Pillar_Reference_INTERNAL', tag: 'D' },
];

(async () => {
  fs.mkdirSync(PREV, { recursive: true });
  fs.mkdirSync(path.join(__dirname, 'diagrams'), { recursive: true });
  const browser = await chromium.launch();
  for (const doc of DOCS) for (const theme of ['dark']) {
    const SRC = 'file://' + path.join(__dirname, doc.src);
    const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1 });
    await page.goto(SRC + '#' + theme, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    // Layout check: content must not run into the footer.
    const report = await page.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
      const foot = pg.querySelector('footer').getBoundingClientRect();
      let last = 0;
      pg.querySelectorAll('*').forEach(el => {
        if (el.closest('footer') || el.closest('svg') && el.tagName !== 'svg') return;
        const r = el.getBoundingClientRect();
        if (r.height) last = Math.max(last, r.bottom);
      });
      const pb = pg.getBoundingClientRect();
      return { page: i + 1, spaceAboveFooter: Math.round(foot.top - last), footerInside: Math.round(pb.bottom - foot.bottom) };
    }));
    const bad = report.filter(r => r.spaceAboveFooter < 0 || r.footerInside < 0);
    console.log(doc.tag, theme, bad.length ? 'OVERFLOW ' + JSON.stringify(bad) : 'layout ok', JSON.stringify(report.map(r => r.spaceAboveFooter)));

    const els = await page.$$('.page');
    for (let i = 0; i < els.length; i++) {
      await els[i].screenshot({ path: path.join(PREV, `${doc.tag}-${theme}-${String(i + 1).padStart(2, '0')}.png`) });
    }
    await page.pdf({ path: path.join(__dirname, `${doc.pdf}_${theme}.pdf`), preferCSSPageSize: true, printBackground: true });

    if (!doc.diagrams) { await page.close(); continue; }
    // Export each diagram as a self-contained SVG with resolved colours.
    const svgs = await page.evaluate((theme) => {
      const PROPS = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linecap', 'stroke-linejoin',
                     'font-family', 'font-size', 'font-weight', 'letter-spacing', 'opacity'];
      const out = {};
      document.querySelectorAll('svg.dg[id^="diagram-"]').forEach(svg => {
        const clone = svg.cloneNode(true);
        const src = [svg, ...svg.querySelectorAll('*')];
        const dst = [clone, ...clone.querySelectorAll('*')];
        src.forEach((el, i) => {
          const cs = getComputedStyle(el), d = dst[i];
          if (el.tagName === 'svg' || el.tagName === 'defs' || el.tagName === 'marker' || el.tagName === 'tspan') { d.removeAttribute('class'); return; }
          PROPS.forEach(p => {
            let v = cs.getPropertyValue(p);
            if (!v || v === 'normal' || v === 'none' && p === 'stroke-dasharray') return;
            if (p === 'font-family' && el.tagName !== 'text') return;
            if (p.startsWith('font') || p === 'letter-spacing') { if (el.tagName !== 'text') return; }
            d.setAttribute(p, v);
          });
          d.removeAttribute('class');
        });
        clone.removeAttribute('class');
        clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        const vb = clone.getAttribute('viewBox').split(' ');
        clone.setAttribute('width', vb[2]); clone.setAttribute('height', vb[3]);
        const bg = getComputedStyle(document.body).backgroundColor;
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', -24); rect.setAttribute('y', -24);
        rect.setAttribute('width', +vb[2] + 48); rect.setAttribute('height', +vb[3] + 48); rect.setAttribute('fill', bg);
        clone.setAttribute('viewBox', `-24 -24 ${+vb[2] + 48} ${+vb[3] + 48}`);
        clone.setAttribute('width', +vb[2] + 48); clone.setAttribute('height', +vb[3] + 48);
        clone.insertBefore(rect, clone.firstChild);
        out[svg.id] = '<?xml version="1.0" encoding="UTF-8"?>\n' + clone.outerHTML;
      });
      return out;
    }, theme);
    for (const [id, s] of Object.entries(svgs)) {
      fs.writeFileSync(path.join(__dirname, 'diagrams', `${id}-${theme}.svg`), s);
    }
    await page.close();
  }
  await browser.close();
})();
