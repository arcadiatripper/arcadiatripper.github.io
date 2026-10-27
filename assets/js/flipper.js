(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Sections fade in as they come up.
  const revealItems = document.querySelectorAll('[data-reveal]');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  // Engines: the tabs pick a panel, and the band wears that engine's skin.
  document.querySelectorAll('[data-engines]').forEach((engines) => {
    const tabs = [...engines.querySelectorAll('[role="tab"]')];
    const pick = (tab, focus) => {
      tabs.forEach((other) => {
        const on = other === tab;
        other.setAttribute('aria-selected', String(on));
        other.tabIndex = on ? 0 : -1;
        document.getElementById(other.getAttribute('aria-controls')).hidden = !on;
      });
      engines.dataset.skin = tab.dataset.skin;
      if (focus) tab.focus();
    };
    // day / night for the engine pictures only; it starts from the page's look and follows the page's button
    const looks = [...engines.querySelectorAll('[data-look-set]')];
    const look = (name) => {
      engines.dataset.look = name;
      looks.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.lookSet === name)));
    };
    looks.forEach((b) => b.addEventListener('click', () => {
      document.documentElement.classList.add('theme-switching');
      look(b.dataset.lookSet);
      requestAnimationFrame(() => requestAnimationFrame(() => document.documentElement.classList.remove('theme-switching')));
    }));
    look(document.documentElement.dataset.theme === 'night' ? 'night' : 'day');
    new MutationObserver(() => look(document.documentElement.dataset.theme === 'night' ? 'night' : 'day'))
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    tabs.forEach((tab, i) => {
      tab.tabIndex = i === 0 ? 0 : -1;
      tab.addEventListener('click', () => pick(tab, false));
      tab.addEventListener('keydown', (event) => {
        const move = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
        if (event.key === 'Home') pick(tabs[0], true);
        else if (event.key === 'End') pick(tabs[tabs.length - 1], true);
        else if (move) pick(tabs[(i + move + tabs.length) % tabs.length], true);
        else return;
        event.preventDefault();
      });
    });
  });

  // Features: arrows and dots turn the slides; swiping or scrolling the track works too.
  document.querySelectorAll('[data-slides]').forEach((box) => {
    const track = box.querySelector('[data-slides-track]');
    const slides = [...track.children];
    const dots = [...box.querySelectorAll('[data-slide-to]')];
    const prev = box.querySelector('[data-slides-prev]');
    const next = box.querySelector('[data-slides-next]');
    let current = 0;

    const mark = (index) => {
      current = index;
      dots.forEach((dot, i) => dot.setAttribute('aria-current', String(i === index)));
      prev.disabled = index === 0;
      next.disabled = index === slides.length - 1;
    };
    const go = (index) => {
      const target = Math.max(0, Math.min(slides.length - 1, index));
      track.scrollTo({ left: slides[target].offsetLeft, behavior: reducedMotion ? 'auto' : 'smooth' });
      mark(target);
    };

    prev.addEventListener('click', () => go(current - 1));
    next.addEventListener('click', () => go(current + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => go(i)));
    track.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowRight') go(current + 1);
      else if (event.key === 'ArrowLeft') go(current - 1);
      else return;
      event.preventDefault();
    });
    let settle = 0;
    track.addEventListener('scroll', () => {
      clearTimeout(settle);
      settle = setTimeout(() => mark(Math.round(track.scrollLeft / track.clientWidth)), 80);
    });
    mark(0);
  });

  // Key and tempo: in repitch, a key change of st semitones moves the tempo by 2^(st/12).
  document.querySelectorAll('[data-tempo]').forEach((tempo) => {
    const bpm = tempo.querySelector('[data-tempo-bpm]');
    const key = tempo.querySelector('[data-tempo-key]');
    const keyOut = tempo.querySelector('[data-tempo-key-out]');
    const out = tempo.querySelector('[data-tempo-out]');
    const target = tempo.querySelector('[data-tempo-target]');
    const reverse = tempo.querySelector('[data-tempo-rev-out]');
    const st = reverse.dataset.st;
    const ct = reverse.dataset.ct;
    const signed = (n) => (n > 0 ? `+${n}` : n < 0 ? `−${Math.abs(n)}` : '0');

    const update = () => {
      const from = Number(bpm.value);
      const semitones = Number(key.value);
      keyOut.textContent = `${signed(semitones)} ${st}`;
      out.textContent = from > 0 ? `${(from * 2 ** (semitones / 12)).toFixed(1)} BPM` : '—';

      const to = Number(target.value);
      if (from > 0 && to > 0) {
        const cents = 1200 * Math.log2(to / from);
        let whole = Math.round(cents / 100);
        let rest = Math.round(cents - whole * 100);
        if (rest === -50) {
          whole -= 1;
          rest = 50;
        }
        reverse.textContent = `${signed(whole)} ${st} ${signed(rest)} ${ct}`;
      } else {
        reverse.textContent = '—';
      }
    };

    [bpm, key, target].forEach((input) => input.addEventListener('input', update));
    update();
  });
})();
