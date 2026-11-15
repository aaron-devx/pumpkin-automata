/* SnapTrips interactions: Lenis smooth scroll, GSAP ScrollTrigger reveals, layered hero parallax, nav. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nav = document.getElementById('nav');
  var burger = document.getElementById('burger');
  var drawer = document.getElementById('drawer');
  var lenis = null;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  var NAV_OFFSET = function () { return nav ? nav.offsetHeight - 8 : 0; };

  /* ---------- nav state ---------- */
  function setScrolled(y) { nav.classList.toggle('scrolled', y > 40); }
  setScrolled(window.scrollY);

  /* ---------- SMIL (<animate>) ignores CSS: pause it from script ---------- */
  function setSmil(el, run) {
    el.querySelectorAll('svg').forEach(function (s) {
      if (!s.pauseAnimations) return;
      if (run && !reduce) s.unpauseAnimations(); else s.pauseAnimations();
    });
  }
  if (reduce) setSmil(document, false);

  /* ---------- pause offscreen art (perf) ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { e.target.classList.toggle('paused', !e.isIntersecting); setSmil(e.target, e.isIntersecting); });
    }, { rootMargin: '120px 0px' });
    document.querySelectorAll('.hero-art, .scene, .foot-art').forEach(function (el) { io.observe(el); });
  }

  /* ---------- drawer ---------- */
  function setMenu(open) {
    root.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (lenis) { open ? lenis.stop() : lenis.start(); }
    document.body.style.overflow = open ? 'hidden' : '';
  }
  burger.addEventListener('click', function () { setMenu(!root.classList.contains('menu-open')); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 960) setMenu(false); });

  /* ---------- anchor links ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id === '#') { e.preventDefault(); return; }
      var t = document.querySelector(id);
      if (!t) return;
      e.preventDefault();
      setMenu(false);
      if (lenis) lenis.scrollTo(id === '#top' ? 0 : t, { offset: -NAV_OFFSET(), duration: 1.4 });
      else window.scrollTo({ top: id === '#top' ? 0 : t.getBoundingClientRect().top + window.scrollY - NAV_OFFSET(), behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  if (reduce || !hasGsap) {
    root.classList.remove('js-anim');
    document.querySelectorAll('.sw').forEach(function (s) { s.classList.add('in'); });
    window.addEventListener('scroll', function () { setScrolled(window.scrollY); }, { passive: true });
    window.__animReady = true;
    return;
  }

  var gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);

  /* ---------- Lenis ---------- */
  if (window.Lenis) {
    lenis = new window.Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true, wheelMultiplier: 1 });
    lenis.on('scroll', function (e) { ST.update(); setScrolled(e.scroll); });
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  } else {
    window.addEventListener('scroll', function () { setScrolled(window.scrollY); }, { passive: true });
  }
  window.__animReady = true;

  /* ---------- hero intro ---------- */
  var heroBits = gsap.utils.toArray('[data-hero]');
  gsap.fromTo(heroBits, { y: 34, opacity: 0 }, {
    y: 0, opacity: 1, duration: 1.2, ease: 'power3.out', stagger: 0.14, delay: 0.15,
    onComplete: function () { gsap.set(heroBits, { clearProps: 'transform' }); }
  });
  gsap.fromTo('.hero-art', { scale: 1.06 }, { scale: 1, duration: 2.2, ease: 'power2.out', transformOrigin: '50% 100%' });
  setTimeout(function () { document.querySelectorAll('.hero .sw').forEach(function (s) { s.classList.add('in'); }); }, 650);

  /* ---------- hero parallax (scroll) ---------- */
  var stage = document.querySelector('.hero-stage');
  gsap.utils.toArray('.hero .layer').forEach(function (layer) {
    var sp = parseFloat(layer.dataset.speed) || 0;
    if (!sp) return;
    gsap.to(layer, {
      y: function () { return sp * stage.offsetHeight; }, ease: 'none',
      scrollTrigger: { trigger: stage, start: 'top top', end: 'bottom top', scrub: true, invalidateOnRefresh: true }
    });
  });
  gsap.to('.hero-content', {
    y: function () { return -0.16 * stage.offsetHeight; }, opacity: 0, ease: 'none',
    scrollTrigger: { trigger: stage, start: 'top top', end: '70% top', scrub: true, invalidateOnRefresh: true }
  });

  /* ---------- hero parallax (pointer, desktop) ---------- */
  if (window.matchMedia('(pointer: fine)').matches) {
    var movers = gsap.utils.toArray('.hero .layer').map(function (layer) {
      var svg = layer.querySelector('.lay');
      return { d: parseFloat(layer.dataset.depth) || 0, x: gsap.quickTo(svg, 'x', { duration: 1.4, ease: 'power3.out' }), y: gsap.quickTo(svg, 'y', { duration: 1.4, ease: 'power3.out' }) };
    });
    var heroEl = document.querySelector('.hero');
    heroEl.addEventListener('pointermove', function (e) {
      if (window.innerWidth <= 860) return;
      var nx = e.clientX / window.innerWidth - 0.5, ny = e.clientY / window.innerHeight - 0.5;
      movers.forEach(function (m) { m.x(-nx * m.d * 1.6); m.y(-ny * m.d * 0.7); });
    });
    heroEl.addEventListener('pointerleave', function () { movers.forEach(function (m) { m.x(0); m.y(0); }); });
  }

  /* ---------- section reveals ---------- */
  function reveal(els, opts) {
    gsap.to(els, Object.assign({
      opacity: 1, x: 0, y: 0, scale: 1, duration: 1.05, ease: 'power3.out', stagger: 0.12, overwrite: true,
      onComplete: function () {
        els.forEach(function (el) { el.removeAttribute('data-reveal'); el.removeAttribute('data-card'); el.removeAttribute('data-plan'); });
        gsap.set(els, { clearProps: 'transform,opacity' });
      }
    }, opts || {}));
    els.forEach(function (el) { el.querySelectorAll ? el.querySelectorAll('.sw').forEach(function (s) { s.classList.add('in'); }) : 0; if (el.classList && el.classList.contains('sw')) el.classList.add('in'); });
  }
  ST.batch('[data-reveal]', { start: 'top 88%', once: true, onEnter: function (b) { reveal(b); } });
  ST.batch('[data-card]', { start: 'top 90%', once: true, onEnter: function (b) { reveal(b, { stagger: 0.16, duration: 1.2 }); } });
  ST.batch('[data-plan]', { start: 'top 90%', once: true, onEnter: function (b) { reveal(b, { stagger: 0.15, duration: 1.15 }); } });

  /* gentle depth drift on the staggered cards and the scene art */
  ST.matchMedia({
    '(min-width: 901px)': function () {
      gsap.fromTo('.dest .plants', { y: 60 }, { y: -60, ease: 'none', scrollTrigger: { trigger: '.dest', start: 'top bottom', end: 'bottom top', scrub: true } });
    }
  });

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ST.refresh(); });
  window.addEventListener('load', function () { ST.refresh(); });
})();

/* ---------- example-cards carousel: 3 pages, auto-advance ---------- */
(function () {
  'use strict';
  var root = document.getElementById('tcards');
  if (!root) return;
  var track = root.querySelector('.ctrack');
  var pages = Array.prototype.slice.call(root.querySelectorAll('.cpage'));
  var dots = Array.prototype.slice.call(root.querySelectorAll('.cdots button'));
  var INTERVAL_MS = 5000;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var index = 0, timer = null, held = false, offscreen = false, stopped = false;

  function show(i) {
    index = (i + pages.length) % pages.length;
    track.style.transform = 'translateX(' + (-100 * index) + '%)';
    pages.forEach(function (p, n) {
      p.toggleAttribute('inert', n !== index);
      p.setAttribute('aria-hidden', n === index ? 'false' : 'true');
    });
    dots.forEach(function (d, n) {
      if (n === index) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
    });
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }
  function start() {
    stop();
    if (reduce || stopped || held || offscreen || document.hidden) return;
    timer = setInterval(function () { show(index + 1); }, INTERVAL_MS);
  }
  function hold(on) { held = on; start(); }

  // First dot click stops autoplay for good (WCAG 2.2.2); keyboard focus pauses it.
  dots.forEach(function (d, n) { d.addEventListener('click', function () { show(n); stopped = true; stop(); }); });
  root.addEventListener('focusin', function (e) { if (e.target.matches(':focus-visible')) hold(true); });
  root.addEventListener('focusout', function () { hold(false); });
  document.addEventListener('visibilitychange', start);
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (ents) { offscreen = !ents[0].isIntersecting; start(); }).observe(root);
  }
  show(0);
  start();
})();
