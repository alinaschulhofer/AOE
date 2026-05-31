/* lead-magnet.js — timed popup for free guide download */
(function () {
  var STORAGE_KEY = 'aoe-lm-dismissed';
  var DELAY_MS = 35000; // show after 35 seconds

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
          '<form class="lm-form" id="lm-mc-form" novalidate>',
            '<input class="lm-input" type="text" name="FNAME" placeholder="First name" required />',
            '<input class="lm-input" type="email" name="EMAIL" placeholder="Email address" required />',
            '<button type="submit" class="btn btn-primary lm-submit">Send Me the Guide</button>',
          '</form>',
          '<p class="lm-note">No spam. Unsubscribe at any time.</p>',
        '</div>',
        '<div class="lm-success" id="lm-success">',
          '<h3>Check your inbox.</h3>',
          '<p>The guide is on its way. Thank you for your interest — and welcome.</p>',
        '</div>',
      '</div>'
    ].join('');
    document.body.appendChild(overlay);

    // Close on X
    overlay.querySelector('.lm-close').addEventListener('click', function () {
      dismiss(overlay);
    });

    // Close on overlay click
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) dismiss(overlay);
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('open')) dismiss(overlay);
    });

    // Form submit — posts to Mailchimp via their hidden form URL
    var form = overlay.querySelector('#lm-mc-form');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fname = form.querySelector('[name="FNAME"]').value.trim();
      var email = form.querySelector('[name="EMAIL"]').value.trim();
      if (!email) return;

      // ── MAILCHIMP: replace MC_ACTION_URL with your Mailchimp form action URL ──
      var MC_ACTION_URL = 'REPLACE_WITH_MAILCHIMP_ACTION_URL';

      if (MC_ACTION_URL === 'REPLACE_WITH_MAILCHIMP_ACTION_URL') {
        // Preview mode — just show success
        showSuccess(overlay);
        return;
      }

      var data = new FormData();
      data.append('EMAIL', email);
      data.append('FNAME', fname);
      data.append('b_PLACEHOLDER', ''); // honeypot

      // Mailchimp JSONP submit
      var callbackName = 'mcCallback_' + Date.now();
      var url = MC_ACTION_URL.replace('/post?', '/post-json?') + '&c=' + callbackName;
      Object.keys(Object.fromEntries(data)).forEach(function (k) {
        url += '&' + encodeURIComponent(k) + '=' + encodeURIComponent(data.get(k));
      });

      window[callbackName] = function (res) {
        delete window[callbackName];
        document.body.removeChild(script);
        if (res.result === 'success' || res.result === 'error' && res.msg.indexOf('already subscribed') > -1) {
          showSuccess(overlay);
        }
      };
      var script = document.createElement('script');
      script.src = url;
      document.body.appendChild(script);
    });

    return overlay;
  }

  function showSuccess(overlay) {
    overlay.querySelector('#lm-form-wrap').style.display = 'none';
    var success = overlay.querySelector('#lm-success');
    success.style.display = 'block';
    try { localStorage.setItem(STORAGE_KEY, '1'); } catch (e) {}
    setTimeout(function () { dismiss(overlay); }, 4000);
  }

  function init() {
    if (alreadyDismissed()) return;
    var overlay = buildPopup();
    setTimeout(function () {
      overlay.style.display = 'flex';
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          overlay.classList.add('open');
        });
      });
    }, DELAY_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
