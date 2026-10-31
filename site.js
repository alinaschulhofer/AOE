/* site.js — shared behaviour across all pages */
(function () {
  // ── Nav scroll state ─────────────────────────────────
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Scroll reveal ─────────────────────────────────────
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }),
      { threshold: 0.12 }
    );
    revealEls.forEach(el => io.observe(el));
  }

  // ── Gold ornament fade-in ─────────────────────────────
  document.querySelectorAll('.gold-ornament').forEach(el => {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.2 });
    io.observe(el);
  });

  // ── Services dropdown ─────────────────────────────────
  const dd = document.querySelector('.nav-dd');
  const trigger = document.querySelector('.nav-dd-trigger');
  if (dd && trigger) {
    trigger.addEventListener('click', e => {
      e.stopPropagation();
      dd.classList.toggle('open');
    });
    document.addEventListener('click', () => dd.classList.remove('open'));
  }

  // ── Mobile menu ───────────────────────────────────────
  const toggle = document.querySelector('.nav-toggle');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (toggle && mobileMenu) {
    toggle.addEventListener('click', () => {
      const isOpen = toggle.classList.toggle('open');
      mobileMenu.classList.toggle('open', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        toggle.classList.remove('open');
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }
})();

// ── Process connector line animation ─────────────────
(function(){
  const connector = document.querySelector('.hwb-connector');
  if (!connector) return;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        connector.classList.add('animate');
        obs.disconnect();
      }
    });
  }, { threshold: 0.5 });
  obs.observe(connector);
})();

// ── Process steps staggered reveal ───────────────────
(function(){
  const steps = document.querySelectorAll('.hwb-step--anim');
  if (!steps.length) return;
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); } });
  }, { threshold: 0.3 });
  steps.forEach(s => obs.observe(s));
})();

// ── Who It's For circles staggered reveal ────────────
(function(){
  const items = document.querySelectorAll('.dfc-item[data-dfc]');
  if (!items.length) return;
  items.forEach(i => i.classList.add('dfc-hidden'));
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.remove('dfc-hidden'); obs.unobserve(e.target); } });
  }, { threshold: 0.15 });
  items.forEach(i => obs.observe(i));
})();

// ── Cal.com booking pop-ups ──────────────────────────
// Any element with data-book="<cal link>" opens that Cal.com event in a
// pop-up. Each element's href points straight to the Cal.com page, so if the
// embed script can't load (ad blockers, etc.) the link still works normally.
(function () {
  const triggers = document.querySelectorAll('[data-book]');
  if (!triggers.length) return;

  (function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");

  let ready = false;
  const s = document.querySelector('script[src="https://app.cal.com/embed/embed.js"]');
  if (s) s.addEventListener('load', () => { ready = true; });

  Cal('init', { origin: 'https://cal.com' });
  Cal('ui', {
    theme: 'light',
    cssVarsPerTheme: { light: { 'cal-brand': '#A8824E' } },
    hideEventTypeDetails: false,
    layout: 'month_view'
  });

  triggers.forEach(el => {
    el.addEventListener('click', e => {
      if (!ready) return; // fall back to opening the Cal.com page
      e.preventDefault();
      Cal('modal', { calLink: el.getAttribute('data-book'), config: { layout: 'month_view' } });
    });
  });
})();
