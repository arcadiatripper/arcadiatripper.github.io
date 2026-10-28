(() => {
  // A visitor whose browser is in English sees a small "English version →" band on a Korean page (never a redirect).
  const hint = document.querySelector('[data-lang-hint]');
  if (!hint) return;

  let dismissed = false;
  try {
    dismissed = localStorage.getItem('lang-hint-dismissed') === '1';
  } catch (error) {
    dismissed = false;
  }

  const prefersEnglish = (navigator.languages || [navigator.language || ''])
    .some((language) => /^en\b/i.test(language)) && !/^ko\b/i.test(navigator.language || '');

  if (prefersEnglish && !dismissed) hint.classList.add('is-shown');

  hint.querySelector('button')?.addEventListener('click', () => {
    hint.classList.remove('is-shown');
    try {
      localStorage.setItem('lang-hint-dismissed', '1');
    } catch (error) {
      // nothing to keep
    }
  });
})();

(() => {
  // The ko / en switch remembers the pick, so arcadiatripper.com (/) opens in that language next time.
  document.querySelectorAll('.gnav__lang a[hreflang]').forEach((link) => {
    link.addEventListener('click', () => {
      try {
        localStorage.setItem('lang', link.getAttribute('hreflang'));
      } catch (error) {
        // nothing to keep
      }
    });
  });
})();

(() => {
  // PLUGINS: a click opens the list; a click elsewhere or Escape closes it.
  document.querySelectorAll('[data-menu]').forEach((menu) => {
    const key = menu.querySelector('button');
    const list = menu.querySelector('.gnav__drop');
    const set = (open) => {
      key.setAttribute('aria-expanded', String(open));
      list.hidden = !open;
    };
    key.addEventListener('click', (event) => {
      event.stopPropagation();
      set(list.hidden);
    });
    document.addEventListener('click', (event) => {
      if (!menu.contains(event.target)) set(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !list.hidden) {
        set(false);
        key.focus();
      }
    });
  });
})();

(() => {
  // A phone shows only the logo and a menu key; the key opens the links, day / night and ko / en below the bar.
  document.querySelectorAll('[data-burger]').forEach((key) => {
  const bar = key.closest('.gnav');
  const set = (open) => {
    bar.classList.toggle('is-open', open);
    key.setAttribute('aria-expanded', String(open));
  };
  key.addEventListener('click', (event) => {
    event.stopPropagation();
    set(!bar.classList.contains('is-open'));
  });
  document.addEventListener('click', (event) => {
    if (!bar.contains(event.target)) set(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && bar.classList.contains('is-open')) {
      set(false);
      key.focus();
    }
  });
  bar.querySelectorAll('.gnav__panel a').forEach((link) => link.addEventListener('click', () => set(false)));
  matchMedia('(min-width: 721px)').addEventListener('change', () => set(false));
  });
})();

(() => {
  // Day / night: the page opens in day; the pick is kept for the next visit. One key, as in the plug-in: the moon
  // by day, the sun by night.
  const keys = document.querySelectorAll('[data-theme-toggle]');
  if (!keys.length) return;
  const root = document.documentElement;
  const show = () => {
    const night = root.dataset.theme === 'night';
    keys.forEach((key) => key.setAttribute('aria-pressed', String(night)));
  };
  // the switch is instant: no colour fades while it happens
  const still = () => {
    root.classList.add('theme-switching');
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.remove('theme-switching')));
  };
  // the other look's pictures load once the page is in, so a switch never waits for them
  const warm = () => document.querySelectorAll('img.shot--day, img.shot--night').forEach((img) => {
    img.loading = 'eager';
    if (img.decode) img.decode().catch(() => {});
  });
  if (document.readyState === 'complete') setTimeout(warm, 300);
  else window.addEventListener('load', () => setTimeout(warm, 300));
  keys.forEach((key) => {
    key.addEventListener('pointerenter', warm, { once: true });
    key.addEventListener('click', () => {
      still();
      const night = root.dataset.theme !== 'night';
      if (night) root.dataset.theme = 'night';
      else delete root.dataset.theme;
      try {
        localStorage.setItem('theme', night ? 'night' : 'day');
      } catch (error) {
        // nothing to keep
      }
      show();
    });
  });
  show();
})();

// the bar's dot board: faint dots on the logo's grid with water sloshing through them: a surface that rolls in
// waves left to right, the dots under it lit, the crest brightest. Still for reduced motion; resting while the tab
// is hidden
(() => {
  const canvas = document.querySelector('.gnav__dots');
  if (!canvas) return;
  const bar = canvas.parentElement;
  const ctx = canvas.getContext('2d');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const PITCH = 7, R = 1.3;
  let w = 0, h = 0, cols = 0, rows = 0, ink = '#000', logo = null;
  const size = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = bar.clientWidth; h = bar.clientHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.ceil(w / PITCH) + 1; rows = Math.ceil(h / PITCH) + 1;
    const l = bar.querySelector('.gnav__logo');
    logo = null;
    if (l) {  // the logo keeps its own dots: none of the board's under it
      const b = bar.getBoundingClientRect(), r = l.getBoundingClientRect();
      logo = { x0: r.left - b.left - 6, x1: r.right - b.left + 6, y0: r.top - b.top - 6, y1: r.bottom - b.top + 6 };
    }
  };
  const colour = () => { ink = getComputedStyle(bar).color; };
  // the water's surface at x (pixels from the top): two rolling waves and a slow swell
  const surface = (x, t) => h * (0.55
    + 0.16 * Math.sin(x * 0.018 - t * 0.0019)
    + 0.10 * Math.sin(x * 0.041 + t * 0.0013)
    + 0.06 * Math.sin(t * 0.0007));
  const draw = (t) => {
    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = ink;
    for (let x = 0; x < cols; x++) {
      const px = x * PITCH + PITCH / 2;
      const top = surface(px, t);
      for (let y = 0; y < rows; y++) {
        const py = y * PITCH + PITCH / 2;
        if (logo && px > logo.x0 && px < logo.x1 && py > logo.y0 && py < logo.y1) continue;
        const d = py - top;  // below the surface: > 0
        let a = 0.05, r = R;
        if (d > 0) a = 0.11 + 0.05 * Math.sin(px * 0.07 + py * 0.11 - t * 0.003);
        if (Math.abs(d) < PITCH) { a = 0.26 * (1 - Math.abs(d) / PITCH) + a; r = R * (1 + 0.35 * (1 - Math.abs(d) / PITCH)); }
        ctx.globalAlpha = a;
        ctx.beginPath(); ctx.arc(px, py, r, 0, Math.PI * 2); ctx.fill();
      }
    }
    ctx.globalAlpha = 1;
  };
  let last = 0;
  const tick = (t) => {
    if (!document.hidden && t - last > 33) { draw(t); last = t; }
    requestAnimationFrame(tick);
  };
  size(); colour();
  new ResizeObserver(() => { size(); draw(last); }).observe(bar);
  new MutationObserver(() => { colour(); draw(last); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  if (still) draw(0); else requestAnimationFrame(tick);
})();
