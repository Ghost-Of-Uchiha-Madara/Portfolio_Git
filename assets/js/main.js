/* =========================================================================
   Portfolio behaviour. Vanilla, no dependencies, no build step.
   Every block bails out quietly if its markup is absent, so the same file
   can be loaded by index.html and by the case-study pages.
   ========================================================================= */
'use strict';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* --- Mobile nav ---------------------------------------------------------- */
(function nav() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const links = document.querySelector('[data-nav-links]');
  if (!toggle || !links) return;

  const setOpen = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    links.classList.toggle('is-open', open);
  };

  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  links.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });
})();

/* --- Header border once scrolled ----------------------------------------- */
(function stickyHeader() {
  const header = document.querySelector('[data-header]');
  if (!header) return;

  const update = () => header.classList.toggle('is-stuck', window.scrollY > 8);
  update();
  window.addEventListener('scroll', update, { passive: true });
})();

/* --- Scroll spy ----------------------------------------------------------
   Highlights the nav link for whichever section owns the top third of the
   viewport. Only runs on pages that actually have in-page section links. */
(function scrollSpy() {
  const links = [...document.querySelectorAll('[data-nav-links] a[href^="#"]')];
  if (links.length === 0) return;

  const sections = links
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if (sections.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((link) => {
          link.classList.toggle(
            'is-active',
            link.getAttribute('href') === '#' + entry.target.id
          );
        });
      });
    },
    { rootMargin: '-25% 0px -65% 0px' }
  );

  sections.forEach((section) => observer.observe(section));
})();

/* --- Scroll reveal -------------------------------------------------------- */
(function reveal() {
  const items = document.querySelectorAll('.reveal');
  if (items.length === 0) return;

  if (reduceMotion || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-in'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        obs.unobserve(entry.target);
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
  );

  items.forEach((el) => observer.observe(el));
})();

/* --- Work filter ---------------------------------------------------------- */
(function workFilter() {
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('[data-category]')];
  if (buttons.length === 0 || cards.length === 0) return;

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;

      buttons.forEach((b) => {
        const on = b === button;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', String(on));
      });

      cards.forEach((card) => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.classList.toggle('is-hidden', !show);
      });
    });
  });
})();

/* --- Role typewriter -----------------------------------------------------
   Replaces the old typed.js dependency (~15 KB over the network) with the
   ~30 lines actually needed. Falls back to the first phrase when the user
   has asked for reduced motion. */
(function typeRole() {
  const target = document.querySelector('[data-typed]');
  if (!target) return;

  let phrases;
  try {
    phrases = JSON.parse(target.dataset.typed);
  } catch {
    return;
  }
  if (!Array.isArray(phrases) || phrases.length === 0) return;

  if (reduceMotion) {
    target.textContent = phrases[0];
    return;
  }

  const TYPE_MS = 70;
  const ERASE_MS = 35;
  const HOLD_MS = 1600;
  let phraseIndex = 0;
  let charIndex = 0;
  let erasing = false;

  const tick = () => {
    const phrase = phrases[phraseIndex];
    charIndex += erasing ? -1 : 1;
    target.textContent = phrase.slice(0, charIndex);

    let delay = erasing ? ERASE_MS : TYPE_MS;

    if (!erasing && charIndex === phrase.length) {
      erasing = true;
      delay = HOLD_MS;
    } else if (erasing && charIndex === 0) {
      erasing = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      delay = 320;
    }

    setTimeout(tick, delay);
  };

  setTimeout(tick, 600);
})();

/* --- Count-up stats ------------------------------------------------------- */
(function countUp() {
  const nums = document.querySelectorAll('[data-count]');
  if (nums.length === 0) return;

  const render = (el, value) => {
    el.textContent = (el.dataset.prefix || '') + value + (el.dataset.suffix || '');
  };

  if (reduceMotion || !('IntersectionObserver' in window)) {
    nums.forEach((el) => render(el, Number(el.dataset.count)));
    return;
  }

  const run = (el) => {
    const target = Number(el.dataset.count);
    const duration = 1200;
    const start = performance.now();

    const frame = (now) => {
      const t = Math.min((now - start) / duration, 1);
      // easeOutCubic
      const eased = 1 - Math.pow(1 - t, 3);
      render(el, Math.round(target * eased));
      if (t < 1) requestAnimationFrame(frame);
    };

    requestAnimationFrame(frame);
  };

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        run(entry.target);
        obs.unobserve(entry.target);
      });
    },
    { threshold: 0.5 }
  );

  nums.forEach((el) => {
    render(el, 0);
    observer.observe(el);
  });
})();

/* --- Contact form --------------------------------------------------------
   Posts to Formspree over fetch so the visitor stays on the page. If the
   request fails for any reason the form falls back to a normal submit. */
(function contactForm() {
  const form = document.querySelector('[data-form]');
  if (!form) return;

  const button = form.querySelector('[data-form-btn]');
  const status = form.querySelector('[data-form-status]');
  const label = button ? button.querySelector('span') : null;
  const idleText = label ? label.textContent : '';

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;

    if (button) button.disabled = true;
    if (label) label.textContent = 'Sending…';
    if (status) status.textContent = '';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });

      if (!response.ok) throw new Error('Request failed: ' + response.status);

      form.reset();
      if (label) label.textContent = 'Message sent';
      if (status) status.textContent = 'Thanks — I will get back to you shortly.';
    } catch {
      if (status) {
        status.textContent =
          'Could not send. Email sankar.gamedev@gmail.com directly and I will reply.';
      }
      if (label) label.textContent = idleText;
    } finally {
      if (button) button.disabled = false;
      setTimeout(() => {
        if (label) label.textContent = idleText;
      }, 4000);
    }
  });
})();

/* --- XP bar: how far down the page you are ------------------------------- */
(function xpBar() {
  const fill = document.querySelector('[data-xp]');
  if (!fill) return;

  let ticking = false;

  const update = () => {
    const doc = document.documentElement;
    const scrollable = doc.scrollHeight - doc.clientHeight;
    const pct = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
    fill.style.width = Math.min(100, Math.max(0, pct)) + '%';
    ticking = false;
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  };

  update();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();

/* --- Gameplay clips ------------------------------------------------------
   Autoplaying video is a bandwidth and attention cost, so a clip only starts
   once it is actually on screen and stops again when it leaves. With reduced
   motion requested nothing plays: the poster frame stands in, and controls
   appear so the clip is still reachable on purpose. */
(function autoLoopVideos() {
  const videos = [...document.querySelectorAll('video[data-autoloop]')];
  if (videos.length === 0) return;

  if (reduceMotion) {
    videos.forEach((v) => {
      v.controls = true;
      v.preload = 'metadata';
    });
    return;
  }

  if (!('IntersectionObserver' in window)) {
    videos.forEach((v) => (v.controls = true));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const v = entry.target;
        if (entry.isIntersecting) {
          // preload="none" means there is nothing buffered until we ask.
          if (v.preload === 'none') v.preload = 'auto';
          const played = v.play();
          // Autoplay can still be refused; fall back to visible controls.
          if (played && typeof played.catch === 'function') {
            played.catch(() => { v.controls = true; });
          }
        } else if (!v.paused) {
          v.pause();
        }
      });
    },
    { threshold: 0.35 }
  );

  videos.forEach((v) => observer.observe(v));
})();

/* --- Footer year ---------------------------------------------------------- */
(function year() {
  const el = document.querySelector('[data-year]');
  if (el) el.textContent = String(new Date().getFullYear());
})();
