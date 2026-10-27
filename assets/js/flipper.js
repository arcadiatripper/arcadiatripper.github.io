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

  // The little plug-in in the hero plays a flip of its 16 slices at 90 BPM, one slice per eighth note.
  const mini = document.querySelector('.mini');
  if (mini) {
    const head = mini.querySelector('.mini__head');
    const lit = mini.querySelector('.mini__lit');
    const count = mini.querySelector('[data-mini-count]');
    const pads = [...mini.querySelectorAll('.pad')];
    const padFor = (slice) => pads.find((pad) => Number(pad.dataset.slice) === slice);
    const flip = [0, 1, 2, 3, 4, 5, 4, 5, 8, 9, 10, 11, 12, 0, 14, 15, 0, 1, 2, 3, 6, 7, 6, 7, 8, 9, 10, 11, 12, 13, 13, 15];
    const step = 60000 / 90 / 2;
    const width = 960 / 16;

    const show = (slice, within) => {
      const x = slice * width + within * width;
      head.setAttribute('x1', x.toFixed(1));
      head.setAttribute('x2', x.toFixed(1));
      lit.setAttribute('x', (slice * width).toFixed(1));
    };

    let index = -1;
    let start = 0;
    let running = false;
    let frame = 0;

    const tick = (now) => {
      if (!running) return;
      if (!start) start = now;
      const position = (now - start) / step;
      const next = Math.floor(position) % flip.length;
      const slice = flip[next];
      if (next !== index) {
        const previous = flip[index];
        if (previous !== undefined) padFor(previous)?.classList.remove('is-hit');
        padFor(slice)?.classList.add('is-hit');
        count.textContent = String(slice + 1);
        index = next;
      }
      show(slice, position - Math.floor(position));
      frame = requestAnimationFrame(tick);
    };

    const play = () => {
      if (running || reducedMotion || document.hidden) return;
      running = true;
      start = 0;
      frame = requestAnimationFrame(tick);
    };

    const stop = () => {
      running = false;
      cancelAnimationFrame(frame);
    };

    if (reducedMotion) {
      show(4, 0.5);
      padFor(4)?.classList.add('is-hit');
      count.textContent = '5';
    } else if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => (entry.isIntersecting ? play() : stop()), { threshold: 0.2 }).observe(mini);
      document.addEventListener('visibilitychange', () => (document.hidden ? stop() : play()));
    } else {
      play();
    }
  }

  // Engines: the tabs pick a panel, and the band wears that engine's skin.
  const engines = document.querySelector('[data-engines]');
  if (engines) {
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
  }

  // Key and tempo: in repitch, a key change of st semitones moves the tempo by 2^(st/12).
  const tempo = document.querySelector('[data-tempo]');
  if (tempo) {
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
  }
})();
