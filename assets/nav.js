/* Multiworks Construction — nav + hero rotation + reveal + FAQ
 * Rewritten per /impeccable audit + critique:
 *   - Hero rotation slowed from 1.8s to 6.5s (was "PowerPoint autoplay" pace).
 *   - Honors prefers-reduced-motion across rotation, reveal, FAQ animation.
 *   - Pauses rotation on hover/focus so a visitor can read the headline.
 *   - FAQ buttons get real aria-expanded + aria-controls wiring.
 *   - Hero slides are now <img> elements — drop the legacy data-bg → backgroundImage hop
 *     for them. data-bg is still used by page-hero backgrounds (left as div+background until
 *     a future refactor).
 */
(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var nav = document.querySelector('.nav');
  var isLight = nav && nav.classList.contains('is-light');

  function onScroll() {
    if (!nav || isLight) return;
    if (window.scrollY > 60) nav.classList.add('is-scrolled');
    else nav.classList.remove('is-scrolled');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = document.querySelector('.nav__toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var isOpen = toggle.classList.toggle('is-open');
      document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    toggle.setAttribute('aria-expanded', 'false');
  }
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (toggle) {
        toggle.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
      document.body.classList.remove('nav-open');
    });
  });

  // Hero rotation
  var slides = document.querySelectorAll('.hero__slide');
  if (slides.length > 1 && !prefersReducedMotion) {
    var i = 0;
    var rotationInterval = null;
    var ROTATION_MS = 8000;

    function advance() {
      slides[i].classList.remove('is-active');
      i = (i + 1) % slides.length;
      slides[i].classList.add('is-active');
    }
    function start() {
      if (rotationInterval) return;
      rotationInterval = setInterval(advance, ROTATION_MS);
    }
    function stop() {
      if (!rotationInterval) return;
      clearInterval(rotationInterval);
      rotationInterval = null;
    }

    var heroEl = document.querySelector('.hero');
    if (heroEl) {
      // Pause on hover/focus — gives visitors time to read the H1.
      heroEl.addEventListener('mouseenter', stop);
      heroEl.addEventListener('mouseleave', start);
      heroEl.addEventListener('focusin', stop);
      heroEl.addEventListener('focusout', start);
    }
    // Pause when tab is hidden to save battery + avoid wakelock.
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stop(); else start();
    });

    start();
  }

  // (Legacy data-bg apply loop removed in the polish pass — all photographic content
  //  is now <img> with native attributes. Kept only as a one-line guard for any
  //  future ad-hoc data-bg uses that don't go through the <img> pipeline.)

  // Reveal-on-scroll. Honors prefers-reduced-motion by revealing immediately.
  if (prefersReducedMotion) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  } else if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Contact form: progressive AJAX submit so the user never leaves the page.
  // Pages Function at /api/contact handles validation + email send + logging.
  var contactForm = document.getElementById('contactForm');
  if (contactForm) {
    var statusEl = document.getElementById('formStatus');
    var submitBtn = document.getElementById('contactSubmit');
    var labelEl = submitBtn ? submitBtn.querySelector('.btn__label') : null;
    var originalLabel = labelEl ? labelEl.textContent : 'Send message';

    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (statusEl) {
        statusEl.textContent = '';
        statusEl.className = 'form-status';
      }
      if (submitBtn) submitBtn.disabled = true;
      if (labelEl) labelEl.textContent = 'Sending';

      var fd = new FormData(contactForm);
      fetch(contactForm.action, {
        method: 'POST',
        body: fd,
        headers: { 'Accept': 'application/json' },
      })
        .then(function (r) {
          return r.json().then(function (data) { return { ok: r.ok, data: data }; });
        })
        .then(function (res) {
          if (res.ok && res.data && res.data.ok) {
            if (statusEl) {
              statusEl.textContent = 'Thanks. We received your request and will reach out within one business day.';
              statusEl.className = 'form-status is-success';
            }
            contactForm.reset();
            if (labelEl) labelEl.textContent = 'Sent';
          } else {
            if (statusEl) {
              statusEl.textContent = (res.data && res.data.error)
                ? res.data.error
                : 'Something went wrong. Please call us at ' + (document.querySelector('.contact-card__value a[href^="tel:"]') || {}).textContent + ' or try again.';
              statusEl.className = 'form-status is-error';
            }
            if (submitBtn) submitBtn.disabled = false;
            if (labelEl) labelEl.textContent = originalLabel;
          }
        })
        .catch(function () {
          if (statusEl) {
            statusEl.textContent = "Couldn't reach the server. Please call us or try again.";
            statusEl.className = 'form-status is-error';
          }
          if (submitBtn) submitBtn.disabled = false;
          if (labelEl) labelEl.textContent = originalLabel;
        });
    });
  }

  // FAQ accordion with proper ARIA (was: class toggle only — VoiceOver/JAWS silent).
  document.querySelectorAll('.faq__q').forEach(function (q, idx) {
    var item = q.closest('.faq__item');
    var panel = item ? item.querySelector('.faq__a') : null;
    if (panel && !panel.id) panel.id = 'faq-panel-' + idx;
    if (panel) {
      q.setAttribute('aria-controls', panel.id);
      panel.setAttribute('role', 'region');
    }
    q.setAttribute('aria-expanded', 'false');
    q.addEventListener('click', function () {
      var willOpen = !item.classList.contains('is-open');
      item.classList.toggle('is-open');
      q.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
  });
})();
