// Picks the ad format from ?format=h|v|a4 (default: v) and sizes the printed page to match.
// a4 is the portrait layout scaled up to a full A4 page.
// ?theme=dark switches concepts that offer a dark variant.
// ?embed=1 scales the ad to fill the window (used by the index.html gallery).
(function () {
  var q = new URLSearchParams(location.search);
  var a4 = q.get('format') === 'a4';
  var f = q.get('format') === 'h' ? 'h' : 'v';
  document.body.setAttribute('data-format', f);
  if (a4) document.body.setAttribute('data-page', 'a4');
  if (q.get('theme') === 'dark') document.body.setAttribute('data-theme', 'dark');
  var size = a4 ? '210mm 297mm' : f === 'h' ? '210mm 148mm' : '148mm 210mm';
  var s = document.createElement('style');
  s.textContent = '@page { size: ' + size + '; margin: 0; }';
  document.head.appendChild(s);

  if (q.get('embed') === '1') {
    var st = document.body.style;
    st.padding = '0'; st.minHeight = '0'; st.display = 'block'; st.background = 'none'; st.overflow = 'hidden';
    var ad = document.querySelector('.ad');
    var fit = function () {
      ad.style.position = 'absolute'; ad.style.left = '0'; ad.style.top = '0';
      ad.style.transformOrigin = '0 0';
      ad.style.transform = 'scale(' + (window.innerWidth / ad.getBoundingClientRect().width * (parseFloat(ad.style.transform.slice(6)) || 1)) + ')';
    };
    fit();
    window.addEventListener('resize', fit);
  }
})();
