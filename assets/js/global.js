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
  // The 한 / EN switch remembers the pick, so arcadiatripper.com (/) opens in that language next time.
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
  // Day / night: the page opens in day; the pick is kept for the next visit.
  const keys = document.querySelectorAll('[data-theme-set]');
  if (!keys.length) return;
  const root = document.documentElement;
  const show = () => {
    const night = root.dataset.theme === 'night';
    keys.forEach((key) => key.setAttribute('aria-pressed', String((key.dataset.themeSet === 'night') === night)));
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
      if (key.dataset.themeSet === 'night') root.dataset.theme = 'night';
      else delete root.dataset.theme;
      try {
        localStorage.setItem('theme', key.dataset.themeSet);
      } catch (error) {
        // nothing to keep
      }
      show();
    });
  });
  show();
})();
