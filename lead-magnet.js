/* lead-magnet.js — timed popup, email captured via Formspree, instant PDF download */
(function () {
  var STORAGE_KEY = 'aoe-lm-dismissed';
  var DELAY_MS = 35000;
  var FORMSPREE_ID = 'xzdwqnvk'; // same account, submissions tagged by subject
  var GUIDE_URL = 'assets/AOE_Free_Guide.pdf';

  function alreadyDismissed() {
    try { return !!localStorage.getItem(STORAGE_KEY); } catch (e) { return false; }
  }

  function dismiss(overlay) {
    overlay.classList.remove('open');
    try { localStorage.setItem(STORAGE_KEY, '1'); } catch (e) {}
    setTimeout(function () { overlay.style.display = 'none'; }, 500);
  }

  function buildPopup() {
    var overlay = document.createElement('div');
    overlay.className = 'lm-overlay';
    overlay.id = 'lm-overlay';
    overlay.innerHTML = [
      '<div class="lm-modal" role="dialog" aria-modal="true" aria-labelledby="lm-headline">',
        '<button class="lm-close" aria-label="Close">&times;</button>',

        '<div id="lm-form-wrap">',
          '<p class="lm-eyebrow">Free Guide</p>',
          '<h2 class="lm-headline" id="lm-headline">',
            'The Inner Architecture<br /><em style="color:var(--accent);font-style:italic;">of High Performance</em>',
          '</h2>',
          '<p class="lm-body">',
            'A complimentary guide from Dr. Alina Schulhofer — exploring the internal foundations',
            ' that separate sustainable excellence from performance that burns out.',
          '</p>',
          '<form class="lm-form" id="lm-guide-form" novalidate>',
            '<input class="lm-input" type="text" name="name" placeholder="First name" />',
            '<input class="lm-input" type="email" name="email" placeholder="Email address" required />',
            '<input type="hidden" name="subject" value="Free Guide Download" />',
            '<button type="submit" class="btn btn-primary lm-submit">Download the Guide</button>',
          '</form>',
          '<p class="lm-note">No spam. Unsubscribe at any time.</p>',
          '<p class="lm-error" id="lm-error" style="display:none;font-size:.78rem;color:#b94040;margin-top:.5rem;"></p>',
        '</div>',

        '<div class="lm-success" id="lm-success">',
          '<h3>Your guide is ready.</h3>',
          '<p>Thank you — click below to download your complimentary copy.</p>',
          '<a href="' + GUIDE_URL + '" download class="btn btn-primary lm-submit" style="margin-top:1.5rem;text-align:center;justify-content:center;">',
            'Download Now',
          '</a>',
        '</div>',
      '</div>'
    ].join('');

    document.body.appendChild(overlay);

    overlay.querySelector('.lm-close').addEventListener('click', function () { dismiss(overlay); });
    overlay.addEventListener('click', function (e) { if (e.target === overlay) dismiss(overlay); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) dismiss(overlay);
    });

    var form = overlay.querySelector('#lm-guide-form');
    var errorEl = overlay.querySelector('#lm-error');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorEl.style.display = 'none';

      var email = form.querySelector('[name="email"]').value.trim();
      if (!email || !email.includes('@')) {
        errorEl.textContent = 'Please enter a valid email address.';
        errorEl.style.display = 'block';
        return;
      }

      var submitBtn = form.querySelector('[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'One moment…';

      var data = new FormData(form);

      fetch('https://formspree.io/f/' + FORMSPREE_ID, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.ok || (res.errors && res.errors.length === 0)) {
          showSuccess(overlay);
        } else {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Download the Guide';
          errorEl.textContent = 'Something went wrong — please try again.';
          errorEl.style.display = 'block';
        }
      })
      .catch(function () {
        // Network error — still show download so user isn't blocked
        showSuccess(overlay);
      });
    });

    return overlay;
  }

  function showSuccess(overlay) {
    overlay.querySelector('#lm-form-wrap').style.display = 'none';
    var success = overlay.querySelector('#lm-success');
    success.style.display = 'block';
    try { localStorage.setItem(STORAGE_KEY, '1'); } catch (e) {}
  }

  function init() {
    if (alreadyDismissed()) return;
    var overlay = buildPopup();
    setTimeout(function () {
      overlay.style.display = 'flex';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { overlay.classList.add('open'); });
      });
    }, DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
