/* Multiworks Construction — nav + hero rotation + reveal + FAQ */
(function () {
  'use strict';

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
      toggle.classList.toggle('is-open');
      document.body.classList.toggle('nav-open');
    });
  }
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (toggle) toggle.classList.remove('is-open');
      document.body.classList.remove('nav-open');
    });
  });

  // Hero rotation: 1.8s interval, crossfade, looped
  var slides = document.querySelectorAll('.hero__slide');
  if (slides.length > 1) {
    var i = 0;
    slides.forEach(function (s) {
      var url = s.getAttribute('data-bg');
      if (url) {
        var img = new Image();
        img.src = url;
        s.style.backgroundImage = "url('" + url + "')";
      }
    });
    setInterval(function () {
      slides[i].classList.remove('is-active');
      i = (i + 1) % slides.length;
      slides[i].classList.add('is-active');
    }, 1800);
  }

  // Apply data-bg to any other elements (page-hero, split images, etc.)
  document.querySelectorAll('[data-bg]').forEach(function (el) {
    if (el.classList.contains('hero__slide')) return;
    el.style.backgroundImage = "url('" + el.getAttribute('data-bg') + "')";
  });

  if ('IntersectionObserver' in window) {
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

  document.querySelectorAll('.faq__q').forEach(function (q) {
    q.addEventListener('click', function () {
      q.closest('.faq__item').classList.toggle('is-open');
    });
  });
})();
