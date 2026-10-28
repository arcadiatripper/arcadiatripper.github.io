// SPDX-License-Identifier: MIT
// (c) tripper by RENÉ — flipper's pond (the animation in the plug-in's top bar), the same code the plug-in's
// JUCE port was made from: the lab host, then the four looks the plug-in ships (paper, strings, ink, koi).
'use strict';
// pond lab: the host for pond concepts (flipper's header animation).
// A concept registers itself with PONDS.push({ id, name, ko, idea, make }) — see README.md.
'use strict';
window.PONDS = window.PONDS || [];

const lab = (() => {
  // --- palette (flipper 0.2.2, 버터 day / night) ---------------------------------------------------------------
  const DAY = { paper: '#fff7e6', dot: '#ecdcbd', card: '#fffdf7', ink: '#3b2a24', soft: '#766256', well: '#f2e3c4',
    pick: '#ffd23f', led: '#ff4b3e', meter: '#ffab70', track: '#f3e7cf', play: '#ffd9d2', shadow: '#3b2a24' };
  const NIGHT = { paper: '#211b17', dot: '#2f2721', card: '#2b231e', ink: '#f7ecd9', soft: '#b59f8b', well: '#3a2f27',
    pick: '#ffd23f', led: '#ff5a4a', meter: '#ffab70', track: '#33291f', play: '#6b3f36', shadow: '#0f0b09' };

  // --- colour helpers ---------------------------------------------------------------------------------------------
  function hex (h) { const n = parseInt (h.slice (1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
  function toHex ([r, g, b]) { return '#' + [r, g, b].map (v => Math.max (0, Math.min (255, Math.round (v))).toString (16).padStart (2, '0')).join (''); }
  function mix (a, b, t) { const A = hex (a), B = hex (b); return toHex (A.map ((v, i) => v + (B[i] - v) * t)); }
  function rgba (h, a) { const [r, g, b] = hex (h); return `rgba(${r},${g},${b},${a})`; }
  function oklch (L, C, H) {
    const hr = H * Math.PI / 180, a = C * Math.cos (hr), b = C * Math.sin (hr);
    const l_ = L + 0.3963377774 * a + 0.2158037573 * b, m_ = L - 0.1055613458 * a - 0.0638541728 * b, s_ = L - 0.0894841775 * a - 1.2914855480 * b;
    const l = l_ ** 3, m = m_ ** 3, s = s_ ** 3;
    let rgb = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
      -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
    rgb = rgb.map (c => { c = Math.max (0, Math.min (1, c)); return 255 * (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055); });
    return toHex (rgb);
  }
  // flipper's pad colour ("sound" mode) and the pond colour (a step deeper)
  const sliceColour = b => oklch (0.84, 0.12, 20 + b * 290);
  const pondColour = b => oklch (0.69, 0.17, 20 + b * 290);
  // deterministic random numbers (concepts must not use Math.random: the sheets must repeat)
  function rand (seed) { let s = (seed >>> 0) || 1; return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 1e9) / 1e9; }; }
  const util = { hex, toHex, mix, rgba, oklch, rand, sliceColour, pondColour };

  // --- the demo slices: a drum break chopped in 8 ----------------------------------------------------------------
  const SLICES = [
    { x: 0.04, b: 0.08, what: 'kick' }, { x: 0.17, b: 0.92, what: 'hat' }, { x: 0.29, b: 0.48, what: 'snare' },
    { x: 0.42, b: 0.88, what: 'hat' }, { x: 0.55, b: 0.12, what: 'kick' }, { x: 0.67, b: 0.80, what: 'open hat' },
    { x: 0.80, b: 0.50, what: 'snare' }, { x: 0.93, b: 0.65, what: 'perc' } ];
  function hitFor (slice, t, velocity = 0.9, reversed = false) {
    const s = SLICES[slice];
    return { slice, x: s.x, brightness: s.b, colour: sliceColour (s.b), deep: pondColour (s.b), velocity, reversed, t };
  }
  // 92 BPM boom bap, 16ths: [step, slice, velocity]
  const BEAT = [[0, 0, 1], [2, 1, .55], [4, 2, .95], [6, 3, .5], [7, 7, .6], [8, 1, .55], [10, 4, .9], [12, 6, 1], [14, 5, .7]];
  const STEP_MS = 60000 / 92 / 4;

  // the sheet's script: a kick, a hat, a snare, a roll of hats, then quiet
  const SCRIPT = [[0, 0, 1], [260, 3, .6], [520, 2, .95], [700, 5, .7], [780, 4, .9],
    [1000, 1, .5], [1080, 3, .5], [1160, 1, .55], [1240, 3, .5], [1320, 1, .6], [1400, 3, .55], [1480, 1, .6], [1560, 3, .65],
    [1800, 6, 1], [1900, 7, .6, true]];
  const FRAMES = [-10, 40, 100, 180, 280, 400, 560, 760, 900, 1100, 1400, 1700, 1950, 2400, 3000, 4500];

  // --- one pond on a canvas ---------------------------------------------------------------------------------------
  class Stage {
    constructor (concept, canvas, { w = 230, h = 34, night = false, dpr = window.devicePixelRatio || 1, zoom = 1 } = {}) {
      this.concept = concept; this.canvas = canvas; this.w = w; this.h = h; this.night = night; this.dpr = dpr; this.zoom = zoom;
      canvas.width = Math.round (w * dpr * zoom); canvas.height = Math.round (h * dpr * zoom);
      canvas.style.width = (w * zoom) + 'px'; canvas.style.height = (h * zoom) + 'px';
      this.ctx = canvas.getContext ('2d');
      this.inst = concept.make ({ w, h, dpr: dpr * zoom, theme: this.theme(), util });
      this.moving = true; this.drawMs = 0; this.frames = 0;
    }
    theme () { return { night: this.night, t: this.night ? NIGHT : DAY }; }
    setNight (n) { this.night = n; this.inst.setTheme && this.inst.setTheme (this.theme()); this.moving = true; }
    hit (h) { this.inst.hit (h); this.moving = true; }
    click (x, t) { this.inst.click ? this.inst.click (x, t) : null; this.moving = true; }
    draw (t) {
      const { ctx, w, h } = this, s = this.dpr * this.zoom;
      ctx.setTransform (1, 0, 0, 1, 0, 0);
      ctx.clearRect (0, 0, this.canvas.width, this.canvas.height);
      ctx.setTransform (s, 0, 0, s, 0, 0);
      const T = this.theme().t;
      if (! this.concept.ownWell) {
        // the well: radius 12, an inset shadow (ink 18 %) — the same as the other wells on the screen
        ctx.save(); roundRect (ctx, 0, 0, w, h, 12); ctx.fillStyle = T.well; ctx.fill(); ctx.clip();
      } else ctx.save();
      const t0 = performance.now();
      this.moving = this.inst.draw (ctx, t) !== false;
      this.drawMs += performance.now() - t0; this.frames++;
      ctx.restore();
      if (! this.concept.ownWell) {
        ctx.save(); roundRect (ctx, 0, 0, w, h, 12); ctx.clip();
        ctx.lineWidth = 3; ctx.strokeStyle = rgba (T.ink, this.night ? 0.35 : 0.18);
        roundRect (ctx, -0.75, -0.75 + 1, w + 1.5, h + 1.5, 12.5); ctx.stroke(); ctx.restore();
      }
    }
  }
  function roundRect (ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo (x + r, y); ctx.arcTo (x + w, y, x + w, y + h, r); ctx.arcTo (x + w, y + h, x, y + h, r);
    ctx.arcTo (x, y + h, x, y, r); ctx.arcTo (x, y, x + w, y, r); ctx.closePath();
  }

  // --- the header around the pond (flipper 0.2.2 at 100 %, 960 wide) ----------------------------------------------
  function header (night, pondW = 156) {
    const el = document.createElement ('div');
    el.className = 'hdr' + (night ? ' night' : '');
    el.innerHTML = `
      <div class="logo">flipper<span>.</span></div>
      <div class="key sm">↶</div><div class="key sm">↷</div>
      <div class="field">‹&nbsp; boom bap break &nbsp;›</div>
      <div class="tabs"><div class="tab on">sound</div><div class="tab">FX <i>soon</i></div></div>
      <div class="pondslot" style="width:${pondW}px"></div>
      <div class="key sm led">!</div>
      <div class="vol"><div class="knob"></div><div class="vt"><b>volume</b><span>0.0 dB</span></div></div>
      <div class="key sm">?</div><div class="key sm">⚙</div><div class="key sm">${night ? '☀' : '☾'}</div>`;
    return el;
  }

  // --- live pages -------------------------------------------------------------------------------------------------
  const live = [];
  let beatOn = false, beatStart = 0, beatNext = 0;
  function tick () {
    const t = performance.now();
    if (beatOn) {
      while (beatNext <= t) {
        const step = Math.round ((beatNext - beatStart) / STEP_MS) % 16;
        for (const [s, slice, v] of BEAT) if (s === step) for (const st of live) st.hit (hitFor (slice, beatNext, v));
        beatNext += STEP_MS;
      }
    }
    for (const st of live) if (st.moving || beatOn) st.draw (t);
    requestAnimationFrame (tick);
  }
  function setBeat (on) { beatOn = on; beatStart = beatNext = performance.now() + 30; }
  function hitAll (slice, v = 0.9, reversed = false) { const t = performance.now(); for (const st of live) st.hit (hitFor (slice, t, v, reversed)); }

  function card (concept, { widths = [230], zoom = 3 } = {}) {
    const c = document.createElement ('section'); c.className = 'concept'; c.id = 'c-' + concept.id;
    c.innerHTML = `<h2>${concept.name} <small>${concept.ko || ''}</small></h2><p>${concept.idea || ''}</p>`;
    for (const night of [false, true]) {
      for (const w of widths) {
        const hd = header (night, w); c.appendChild (hd);
        const cv = document.createElement ('canvas'); hd.querySelector ('.pondslot').appendChild (cv);
        const st = new Stage (concept, cv, { w, night }); live.push (st);
        cv.addEventListener ('pointerdown', e => { const r = cv.getBoundingClientRect(); st.click ((e.clientX - r.left) / r.width, performance.now()); });
      }
    }
    if (zoom > 1) {
      const z = document.createElement ('div'); z.className = 'zoom';
      for (const night of [false, true]) {
        const cv = document.createElement ('canvas'); z.appendChild (cv);
        live.push (new Stage (concept, cv, { w: 230, night, zoom }));
      }
      c.appendChild (z);
    }
    return c;
  }

  function pads () {
    const p = document.createElement ('div'); p.className = 'pads';
    SLICES.forEach ((s, i) => {
      const b = document.createElement ('button'); b.textContent = (i + 1) + ' ' + s.what; b.style.background = sliceColour (s.b);
      b.onpointerdown = e => hitAll (i, 0.9, e.shiftKey); p.appendChild (b);
    });
    const beat = document.createElement ('button'); beat.className = 'beat'; beat.textContent = '▶ beat';
    beat.onclick = () => { setBeat (! beatOn); beat.textContent = beatOn ? '■ stop' : '▶ beat'; }; p.prepend (beat);
    window.addEventListener ('keydown', e => { const i = '12345678'.indexOf (e.key); if (i >= 0 && ! e.repeat) hitAll (i, 0.9, e.shiftKey); });
    return p;
  }

  // --- the contact sheet (deterministic: a virtual clock at 60 fps) -----------------------------------------------
  function sheet (concept) {
    const root = document.createElement ('div'); root.id = 'sheet';
    const head = document.createElement ('div'); head.className = 'shead'; root.appendChild (head);
    const grid = document.createElement ('div'); grid.className = 'sgrid'; root.appendChild (grid);
    const ms = [];
    for (const night of [false, true]) {
      const off = document.createElement ('canvas');
      const st = new Stage (concept, off, { w: 230, h: 34, night, dpr: 3 });
      let si = 0, fi = 0;
      for (let t = -20; fi < FRAMES.length; t += 1000 / 60) {
        while (si < SCRIPT.length && SCRIPT[si][0] <= t) { const [at, slice, v, rev] = SCRIPT[si++]; st.hit (hitFor (slice, at, v, !! rev)); }
        st.draw (t);
        while (fi < FRAMES.length && FRAMES[fi] <= t) {
          const cell = document.createElement ('div'); cell.className = 'cell' + (night ? ' night' : '');
          const c2 = document.createElement ('canvas'); c2.width = off.width; c2.height = off.height;
          c2.style.width = '690px'; c2.style.height = '102px';
          c2.getContext ('2d').drawImage (off, 0, 0);
          cell.appendChild (c2);
          const lab = document.createElement ('span'); lab.textContent = (FRAMES[fi] < 0 ? 'idle' : FRAMES[fi] + ' ms') + (night ? ' · night' : '');
          cell.appendChild (lab); grid.appendChild (cell); fi++;
        }
      }
      ms.push ((st.drawMs / st.frames).toFixed (3));
      // one header at 100 % for context, at the "760 ms" moment: re-run to there
      const hd = header (night, 230); root.appendChild (hd);
      const cv = document.createElement ('canvas'); hd.querySelector ('.pondslot').appendChild (cv);
      const s2 = new Stage (concept, cv, { w: 230, night, dpr: 2 });
      let sj = 0;
      for (let t = -20; t <= 760; t += 1000 / 60) {
        while (sj < SCRIPT.length && SCRIPT[sj][0] <= t) { const [at, slice, v, rev] = SCRIPT[sj++]; s2.hit (hitFor (slice, at, v, !! rev)); }
        s2.draw (t);
      }
    }
    head.textContent = `${concept.id} — ${concept.name} · draw ${ms[0]} ms day / ${ms[1]} ms night per frame (Chrome, 690×102 px) · script: kick 0, hat 260, snare 520, open hat 700, kick 780, hat roll 1000–1560, snare 1800, reversed perc 1900`;
    return root;
  }

  function boot () {
    const q = new URLSearchParams (location.search);
    const only = q.get ('only'), sh = q.get ('sheet');
    const list = PONDS.filter (p => ! only || p.id === only);
    if (sh) { const c = PONDS.find (p => p.id === sh); document.body.appendChild (c ? sheet (c) : Object.assign (document.createElement ('p'), { textContent: 'no concept ' + sh })); document.body.dataset.ready = '1'; return; }
    document.body.appendChild (pads());
    for (const c of list) document.body.appendChild (card (c));
    requestAnimationFrame (tick);
    document.body.dataset.ready = '1';
  }
  return { STEP_MS, BEAT, util, SLICES, hitFor, Stage, header, boot, setBeat, hitAll, roundRect, DAY, NIGHT };
}) ();


// paper — paper-cut confetti stickers. A hit pops flat paper shapes (dots, puffy stars, petals, squiggles,
// sprinkles) out of its spot; they tumble (spin, a 3D flip that shows the white back), flutter, bounce on the floor,
// settle like stickers and peel away; a kick makes the stickers already lying on the floor hop. Reversed slices play
// the same recorded flight backwards: the pieces un-peel on the floor, lift off and fly back together into the spot.
PONDS.push ({
  id: 'paper',
  name: 'paper confetti',
  ko: '종이 꽃가루',
  idea: 'paper-cut confetti stickers pop out of each hit, tumble, bounce, settle and peel away; reversed, they fly back together',
  make ({ w, h, dpr, theme, util }) {
    let W = w, H = h, T = theme;
    const DOT = 0, STAR = 1, PETAL = 2, SQUIG = 3, SPRINK = 4, TRI = 5;
    // per kind: gravity, drag (k0 + k1 · face-on), bounce, floor friction, tumble rate, spin, sway (px) and its rate,
    // tilt while swaying, rest time on the floor (ms), stroked or filled, outline width, the thinnest it looks
    // edge-on, and how far its hard shadow drops
    const KP = [
      { g: 560, k0: 0.5, k1: 0.0, e: 0.46, fric: 6, om: [1, 2.6], spin: 5, sway: 0, ws: 0, tilt: 0, rest: 380, stroke: false, ow: 0.85, fmin: 0.36, sh: 1.2 },
      { g: 560, k0: 0.7, k1: 0.3, e: 0.38, fric: 10, om: [1.5, 3.5], spin: 9, sway: 0, ws: 0, tilt: 0, rest: 380, stroke: false, ow: 0.85, fmin: 0.36, sh: 1.2 },
      { g: 520, k0: 3.0, k1: 6.0, e: 0.12, fric: 16, om: [3, 6], spin: 2, sway: 4, ws: 12, tilt: 0.6, rest: 300, stroke: false, ow: 0.8, fmin: 0.32, sh: 1.1 },
      { g: 520, k0: 2.6, k1: 4.0, e: 0.16, fric: 16, om: [9, 15], spin: 6, sway: 2.5, ws: 10, tilt: 0.3, rest: 300, stroke: true, ow: 0.72, fmin: 0.2, sh: 1.0 },
      { g: 720, k0: 4.0, k1: 2.0, e: 0.30, fric: 14, om: [10, 20], spin: 15, sway: 0, ws: 0, tilt: 0, rest: 90, stroke: true, ow: 0.55, fmin: 0.12, sh: 0.85 },
      { g: 560, k0: 2.6, k1: 4.5, e: 0.18, fric: 16, om: [8, 14], spin: 8, sway: 2.5, ws: 11, tilt: 0.4, rest: 280, stroke: false, ow: 0.8, fmin: 0.26, sh: 1.05 },
    ];
    const FR = 1000 / 60, REC = 120, POOL = 120, CROWD = 40, ST = 5, PEEL = 190, REV_SPEED = 1.25, REV_FLOOR = 3.5;
    const pool = [], free = [], act = [];
    for (let i = 0; i < POOL; i++) {
      const p = { rec: new Float32Array (REC * ST), jit: new Float32Array (10), n: 0, restAt: 0, kind: 0, born: 0, rev: false,
        hx: 1, hy: 1, size: 1, wd: 1, face: '#000', back: '#fff', hold: 0, endBy: 1e12, flightStart: 0, fo: 0, landAt: 0 };
      pool.push (p); free.push (p);
    }
    const spots = [];   // the pop at the hit point (forward: bursts open; reversed: the pieces merge into it)
    for (let i = 0; i < 10; i++) spots.push ({ on: false, x: 0, y: 0, r: 3, t0: 0, rev: false, colour: '#000' });
    // a kick thumps the table: stickers already lying on the floor hop (a little ballistic hop, higher when close)
    const thumps = [];
    for (let i = 0; i < 3; i++) thumps.push ({ t: -1e9, x: 0, k: 0 });
    let thumpI = 0;
    const HOP = 250;

    let FO = 0;   // the piece being simulated sits a hair higher or lower (a handmade, uneven floor)
    const floorY = x => {
      const R = 12, inset = 2.6 + FO;
      let lift = 0;
      if (x < R) lift = R - Math.sqrt (Math.max (0, R * R - (R - x) * (R - x)));
      else if (x > W - R) lift = R - Math.sqrt (Math.max (0, R * R - (x - W + R) * (x - W + R)));
      return H - inset - lift;
    };
    const ext = (p, rot, f) => {   // half height of the piece (an ellipse of hx·f × hy, rotated)
      const s = Math.sin (rot), c = Math.cos (rot), a = p.hx * f * s, b = p.hy * c;
      return Math.sqrt (a * a + b * b) + (KP[p.kind].stroke ? p.wd * 0.5 : 0);
    };
    const restAngle = (p, rot) => {
      if (p.kind === DOT) return rot;
      const step = p.kind === STAR ? Math.PI * 2 / 5 : p.kind === TRI ? Math.PI * 2 / 3 : Math.PI;
      return Math.round ((rot - p.jit[9]) / step) * step + p.jit[9];
    };

    // run the flight once at the hit (fixed 240 Hz steps) and record 60 Hz frames: x, y, rot, flip, air
    function simulate (p, x, y, vx, vy, rnd) {
      const K = KP[p.kind], dt = 1 / 240;
      let rot = rnd() * 6.283, spin = (rnd() - 0.5) * 2 * K.spin, ph = (rnd() - 0.5) * 2.4;
      const om = (K.om[0] + rnd() * (K.om[1] - K.om[0])) * (rnd() < 0.5 ? -1 : 1);
      let psi = rnd() * 6.283, onFloor = false, settled = 0, restAt = -1, n = 0, omv = om, landAt = -1;
      FO = p.fo;
      const ws = K.ws, swayA = K.sway * ws * Math.sqrt (ws * ws + (K.k0 + K.k1 * 0.6) ** 2);
      for (let step = 0; n < REC; step++) {
        const f = Math.cos (ph), af = Math.abs (f);
        let ff = 0;
        if (! onFloor) {
          const k = K.k0 + K.k1 * af;
          ff = Math.max (0, Math.min (1, vy / 30));
          vy += K.g * dt; vx += swayA * Math.sin (psi) * ff * dt;
          vx -= vx * k * dt; vy -= vy * k * dt;
          x += vx * dt; y += vy * dt; rot += spin * dt; ph += omv * dt; psi += ws * dt;
          const e0 = ext (p, rot, Math.max (K.fmin, af)), xl = 4 + p.hx, xr = W - 4 - p.hx;
          if (x < xl) { x = xl; vx = Math.abs (vx) * 0.5; }
          if (x > xr) { x = xr; vx = -Math.abs (vx) * 0.5; }
          const fy = floorY (x);
          if (y + e0 >= fy && vy > 0) {
            y = fy - e0; if (landAt < 0) landAt = n;
            vy = -vy * K.e; vx *= 0.55; spin *= 0.5; omv *= 0.4;
            if (p.kind === DOT) spin = vx / p.hx;
            if (Math.abs (vy) < 26) { vy = 0; onFloor = true; }
          }
        } else {
          // on the floor: slide or roll to a stop, flop face up, turn to a resting angle
          const sl = (floorY (x + 0.5) - floorY (x - 0.5));
          vx += sl * 300 * dt; vx *= Math.exp (-K.fric * dt); x += vx * dt;
          const xl = 4 + p.hx, xr = W - 4 - p.hx;
          if (x < xl) { x = xl; vx = 0; } if (x > xr) { x = xr; vx = 0; }
          if (p.kind === DOT) rot += vx / p.hx * dt;
          const tr = restAngle (p, rot), tp = Math.round (ph / 6.2832) * 6.2832;
          const ease = 1 - Math.exp (-20 * dt);
          rot += (tr - rot) * ease; ph += (tp - ph) * ease;
          y = floorY (x) - ext (p, rot, Math.max (K.fmin, Math.abs (Math.cos (ph))));
          if (Math.abs (vx) < 2 && Math.abs (tr - rot) < 0.04 && Math.abs (tp - ph) < 0.06) settled++;
        }
        if ((step & 3) === 0) {
          const o = n * ST, tl = K.tilt * Math.cos (psi) * ff;
          p.rec[o] = x; p.rec[o + 1] = y; p.rec[o + 2] = rot + tl; p.rec[o + 3] = Math.cos (ph);
          p.rec[o + 4] = onFloor ? 0 : Math.min (1, Math.max (0, (floorY (x) - y - p.hy) / 5));
          n++;
          if (settled > 0 && restAt < 0) restAt = n - 1;
          if (restAt >= 0 && n > restAt) break;
        }
      }
      p.n = n; p.restAt = restAt < 0 ? n - 1 : restAt; p.landAt = landAt < 0 ? p.restAt : Math.min (p.restAt, landAt + 4);
      FO = 0;
    }

    const take = () => free.length ? free.pop() : act.shift();   // pool exhausted: recycle the oldest
    const spotFree = () => { for (const s of spots) if (! s.on) return s; return spots[0]; };

    function hit (e) {
      const b = e.brightness, v = e.velocity, rnd = util.rand ((e.t * 7.13 + e.slice * 977 + 13) | 0);
      for (let k = 0; k < 6; k++) rnd();
      const x0 = Math.max (14, Math.min (W - 14, e.x * W)), y0 = H * 0.6;
      let kinds, n, spd, fan;
      if (b < 0.3) { kinds = [DOT, STAR, DOT, STAR]; n = 3 + (v > 0.8 ? 1 : 0); spd = 130; fan = 0.95; }
      else if (b < 0.6) { kinds = [PETAL, SQUIG, PETAL, PETAL, SQUIG]; n = 4 + (v > 0.8 ? 1 : 0); spd = 225; fan = 1.3; }
      else if (b < 0.78) { kinds = [TRI, TRI, SQUIG, TRI]; n = 3 + (v > 0.8 ? 1 : 0); spd = 200; fan = 1.25; }
      else { kinds = [SPRINK]; n = 2 + (v > 0.62 ? 1 : 0) + (b < 0.85 ? 1 : 0); spd = 160; fan = 0.75; }
      const sz = 0.85 + 0.25 * v, hue = 20 + b * 290;
      const third = util.oklch (0.78, 0.15, hue + 26);   // a neighbouring hue, for a livelier handful
      const night = T.night, paperBack = night ? '#e9dcc6' : '#fffdf7';
      if (W < 160 && n > 2) n--;                                   // a narrow well gets a smaller handful
      const crowd = act.length + n - Math.round (CROWD * Math.min (1, W / 230));
      for (let i = 0; i < crowd && i < act.length; i++) act[i].endBy = Math.min (act[i].endBy, e.t + 40 + i * 10);
      const first = (rnd() * kinds.length) | 0;
      // near the ends of the well the handful leans toward the middle
      const lean = x0 < 50 ? (50 - x0) / 36 * 0.75 : x0 > W - 50 ? -(x0 - W + 50) / 36 * 0.75 : 0;
      for (let i = 0; i < n; i++) {
        const p = take();
        p.kind = kinds[(i + first) % kinds.length];
        for (let j = 0; j < 9; j++) p.jit[j] = rnd() * 2 - 1;
        const K = KP[p.kind];
        p.jit[9] = (p.kind === DOT || p.kind === STAR) ? 0 : (rnd() - 0.5) * 0.3;
        switch (p.kind) {
          case DOT: p.size = (3.8 + rnd() * 1.3) * sz; p.hx = p.hy = p.size; break;
          case STAR: p.size = (5.0 + rnd() * 1.1) * sz; p.hx = p.hy = p.size * 0.85; break;
          case PETAL: p.size = (7.2 + rnd() * 1.6) * sz; p.hx = p.size * 0.5; p.hy = p.size * 0.25; break;
          case SQUIG: p.size = (7.5 + rnd() * 1.5) * sz; p.wd = 1.5; p.hx = p.size * 0.5; p.hy = 1.3; break;
          case SPRINK: p.size = (3.4 + rnd() * 1.3) * sz; p.wd = 1.5; p.hx = p.size * 0.5; p.hy = 0.2; break;
          case TRI: p.size = (3.5 + rnd() * 0.8) * sz; p.hx = p.hy = p.size * 0.8; break;
        }
        const pick = rnd();
        p.face = pick < 0.5 ? e.colour : pick < 0.8 ? e.deep : third;
        p.fo = (rnd() - 0.7) * 1.6;
        // the back of the paper is white-ish; a sprinkle is a little rod, the same colour all round
        p.back = p.kind === SPRINK ? p.face : util.mix (e.colour, paperBack, night ? 0.5 : 0.62);
        const fu = (n > 1 ? i / (n - 1) : 0.5) - 0.5;
        const a = -Math.PI / 2 + lean + fan * (1 - Math.abs (lean) * 0.3) * fu * 2 + (rnd() - 0.5) * 0.3;
        let sp = spd * (0.8 + 0.28 * v) * (0.82 + rnd() * 0.32);
        let ca = Math.cos (a), sa = Math.sin (a), delay = i * 10;
        if (b < 0.3) {
          // heavy dots and stars: there is little room above, so they spread sideways — a sideways speed by place in
          // the fan, and an upward one from a chosen hop height
          const wl = Math.min (1, Math.abs (lean) / 0.75), side = Math.sign (lean);
          const vx = (fu * 2 * 125 * (1 - wl * 0.55) + side * wl * 80 + (rnd() - 0.5) * 30) * (0.8 + 0.3 * v), vy = -Math.sqrt (2 * K.g * (5 + rnd() * 6) * (0.8 + 0.3 * v));
          sp = Math.hypot (vx, vy); ca = vx / sp; sa = vy / sp;
          delay = Math.max (0, 1 - Math.abs (vx) / 150) * 50;   // the fastest leave first, so none catch up
        }
        const seed = rnd() * 1e9;
        let kx = 0.55 + 0.45 * Math.min (1, W / 230);   // a narrow well gets a narrower throw
        // fly it; if it would sail out under the rim, throw it a little softer (the same seed, so the same tumble)
        for (let k = 0; k < 4; k++) {
          const r2 = util.rand (seed | 0);
          simulate (p, x0 + ca * 3.5, y0 + sa * 3.5, ca * sp * kx, sa * sp, r2);
          let top = 99; for (let f = 0; f < p.n; f++) top = Math.min (top, p.rec[f * ST + 1] - p.hy);
          if (top > 3) break;
          sp *= 0.86; kx /= 0.86;   // softer upward only: keep the sideways throw
        }
        p.born = e.t + delay + rnd() * 6; p.rev = !! e.reversed;
        p.hold = K.rest * (0.8 + rnd() * 0.45); p.endBy = 1e12;
        act.push (p);
      }
      if (b < 0.3 && ! e.reversed) { const th = thumps[thumpI++ % 3]; th.t = e.t; th.x = x0; th.k = 2.2 + 2.2 * v; }
      if (b >= 0.78 && ! e.reversed) return;   // hats are fine enough without a pop dot (no blinking in a roll)
      const s = spotFree();
      s.on = true; s.x = x0; s.y = y0; s.colour = e.deep; s.rev = !! e.reversed;
      if (e.reversed) {
        // reversed: the stickers un-peel where the forward flight would have left them, then fly the recorded path
        // backwards (a bit quicker), every flight ending at the same moment in the spot
        let maxF = 0;
        // the time to play one piece backwards: its floor part (roll, flop) quickly, its flight at REV_SPEED
        const revDur = p => (p.restAt - p.landAt) * FR / REV_FLOOR + p.landAt * FR / REV_SPEED;
        for (let i = act.length - n; i < act.length; i++) maxF = Math.max (maxF, revDur (act[i]));
        for (let i = act.length - n; i < act.length; i++) {
          const p = act[i], k = i - act.length + n;
          p.born = e.t + k * 16; p.flightStart = e.t + PEEL + 60 + maxF - revDur (p);
        }
        s.t0 = e.t + PEEL + 60 + maxF; s.r = 2.4 + (1 - b) * 1.8;
      } else { s.t0 = e.t; s.r = 2.0 + (1 - b) * 2.4; }
    }

    const easeOutBack = u => { const c = 1.9; u -= 1; return 1 + (c + 1) * u * u * u + c * u * u; };
    const OCT = [], DEC = [];
    for (let i = 0; i < 8; i++) OCT.push ([Math.cos (i * Math.PI / 4), Math.sin (i * Math.PI / 4)]);
    for (let i = 0; i < 10; i++) DEC.push ([Math.cos (i * Math.PI / 5 - Math.PI / 2), Math.sin (i * Math.PI / 5 - Math.PI / 2)]);
    const SX = new Float32Array (10), SY = new Float32Array (10);

    // the shape's path in local coordinates (the caller has set the piece's transform)
    function shape (ctx, p) {
      const s = p.size, j = p.jit;
      ctx.beginPath();
      switch (p.kind) {
        case DOT: case STAR: {
          // a hand-cut circle (8 slightly uneven points) or a puffy star (10 points), smoothed through midpoints
          const m = p.kind === DOT ? 8 : 10, tab = p.kind === DOT ? OCT : DEC;
          for (let i = 0; i < m; i++) {
            const rr = (p.kind === DOT ? s * 1.06 : (i & 1 ? s * 0.5 : s)) * (1 + j[i % 9] * (p.kind === DOT ? 0.065 : 0.05));
            SX[i] = tab[i][0] * rr; SY[i] = tab[i][1] * rr;
          }
          ctx.moveTo ((SX[m - 1] + SX[0]) / 2, (SY[m - 1] + SY[0]) / 2);
          for (let i = 0; i < m; i++) { const k = (i + 1) % m; ctx.quadraticCurveTo (SX[i], SY[i], (SX[i] + SX[k]) / 2, (SY[i] + SY[k]) / 2); }
          break;
        }
        case PETAL: {
          const L = s / 2, Wd = s * 0.3;
          ctx.moveTo (L, 0);
          ctx.bezierCurveTo (L * 0.25, -Wd * 1.25, -L, -Wd * 1.05, -L, 0);
          ctx.bezierCurveTo (-L, Wd * 1.05, L * 0.25, Wd * 1.25, L, 0);
          break;
        }
        case SQUIG: {
          const L = s / 2, A = 1.25 + j[2] * 0.2, d = s / 3;
          ctx.moveTo (-L, 0);
          ctx.quadraticCurveTo (-L + d / 2, -2 * A, -L + d, 0);
          ctx.quadraticCurveTo (-L + d * 1.5, 2 * A, -L + d * 2, 0);
          ctx.quadraticCurveTo (-L + d * 2.5, -2 * A, L, 0);
          break;
        }
        case SPRINK: { const L = s / 2; ctx.moveTo (-L, 0); ctx.lineTo (L, 0); break; }
        case TRI: {
          const R = s;
          ctx.moveTo (0, -R); ctx.lineTo (R * 0.866, R * 0.5); ctx.lineTo (-R * 0.866, R * 0.5); ctx.closePath();
          break;
        }
      }
    }

    let ink = '#000', shadow = '#000', owK = 1;
    const setInk = () => {
      // night: the keys' cream outline, a touch softer and thinner so tiny pieces keep their colour
      ink = T.night ? util.mix (T.t.ink, T.t.well, 0.22) : T.t.ink; shadow = T.t.shadow; owK = T.night ? 0.85 : 1;
    };
    setInk();
    function drawPiece (ctx, p, x, y, rot, flip, sc, air) {
      const K = KP[p.kind], D = dpr;
      const af = Math.max (K.fmin, Math.abs (flip));
      const fx = af * sc * (flip < 0 ? -1 : 1), fy = sc;
      const c = Math.cos (rot), s = Math.sin (rot), a = c * fx, b = s * fx, cc = -s * fy, d = c * fy;
      const sk = 0.45 + 0.55 * Math.min (1, sc), ow = K.ow * owK * (0.35 + 0.65 * Math.min (1, sc)), oy = (K.sh + air * 0.9) * sk, ox = (0.2 + air * 0.5) * sk;
      // hard little shadow, straight down like the keys' (a touch further while the piece is up in the air)
      ctx.setTransform (D * a, D * b, D * cc, D * d, D * (x + ox), D * (y + oy));
      shape (ctx, p);
      ctx.setTransform (D, 0, 0, D, 0, 0);
      ctx.fillStyle = shadow; ctx.strokeStyle = shadow;
      if (K.stroke) { ctx.lineWidth = p.wd + ow * 2; ctx.stroke(); }
      else { ctx.lineWidth = ow * 2; ctx.fill(); ctx.stroke(); }
      // the paper: flat colour (the white-ish back when it flips over), a thin ink outline
      ctx.setTransform (D * a, D * b, D * cc, D * d, D * x, D * y);
      shape (ctx, p);
      ctx.setTransform (D, 0, 0, D, 0, 0);
      const col = flip < 0 ? p.back : p.face;
      if (K.stroke) {
        ctx.strokeStyle = ink; ctx.lineWidth = p.wd + ow * 2; ctx.stroke();
        ctx.strokeStyle = col; ctx.lineWidth = p.wd; ctx.stroke();
      } else {
        ctx.fillStyle = col; ctx.fill();
        ctx.strokeStyle = ink; ctx.lineWidth = ow; ctx.stroke();
      }
    }

    function drawSpot (ctx, s, t) {
      let sc;
      if (! s.rev) {
        const u = (t - s.t0) / 120; if (u >= 1) { s.on = false; return false; } if (u < 0) return true;
        sc = u < 0.3 ? 0.6 + u / 0.3 * 0.55 : 1.15 * (1 - ((u - 0.3) / 0.7) ** 2);
      } else {
        const u = (t - s.t0) / 280; if (u >= 1) { s.on = false; return false; } if (u < -0.1) return true;
        sc = u < 0 ? (1 + u / 0.1) * 1.3 : u < 0.25 ? 1.3 - u / 0.25 * 0.3 : 1 - ((u - 0.25) / 0.75) ** 2;
      }
      if (sc <= 0.02) return true;
      const r = s.r * sc, D = dpr;
      ctx.setTransform (D, 0, 0, D, 0, 0);
      ctx.beginPath(); ctx.arc (s.x + 0.2, s.y + 1.15, r + 0.42, 0, 6.2832); ctx.fillStyle = shadow; ctx.fill();
      ctx.beginPath(); ctx.arc (s.x, s.y, r, 0, 6.2832); ctx.fillStyle = s.colour; ctx.fill();
      ctx.strokeStyle = ink; ctx.lineWidth = 0.85 * owK; ctx.stroke();
      return true;
    }

    return {
      setTheme (t) { T = t; setInk(); },
      hit,
      draw (ctx, t) {
        ctx.lineCap = 'round'; ctx.lineJoin = 'round';
        let any = false;
        for (const s of spots) if (s.on) any = drawSpot (ctx, s, t) || any;
        let j = 0;
        for (let i = 0; i < act.length; i++) {
          const p = act[i], life = t - p.born;
          if (life < 0) { act[j++] = p; continue; }
          let fi, sc = 1, pu = 0, live = true;
          if (! p.rev) {
            fi = life / FR;
            if (life < 110) sc = 0.12 + 0.88 * easeOutBack (life / 110);
            pu = (t - Math.min (p.born + p.restAt * FR + p.hold, p.endBy)) / PEEL;
            if (pu >= 1) live = false;
          } else {
            const fl = t - p.flightStart;
            const d1 = (p.restAt - p.landAt) * FR / REV_FLOOR;
            fi = fl <= 0 ? p.restAt : fl < d1 ? p.restAt - fl * REV_FLOOR / FR : p.landAt - (fl - d1) * REV_SPEED / FR;
            if (life < PEEL) pu = 1 - life / PEEL;          // un-peel: the peel, backwards
            if (fi <= 0) live = false;
            else if (fi * FR < 70) sc = Math.max (0, fi * FR / 70);
          }
          if (! live) { free.push (p); continue; }
          act[j++] = p;
          const resting = fi >= p.restAt;
          if (resting) fi = p.restAt;
          const i0 = Math.floor (fi), i1 = Math.min (p.n - 1, i0 + 1), u = fi - i0, r = p.rec, o0 = i0 * ST, o1 = i1 * ST;
          let x = r[o0] + (r[o1] - r[o0]) * u, y = r[o0 + 1] + (r[o1 + 1] - r[o0 + 1]) * u;
          let rot = r[o0 + 2] + (r[o1 + 2] - r[o0 + 2]) * u;
          let fl = r[o0 + 3] + (r[o1 + 3] - r[o0 + 3]) * u, air = r[o0 + 4] + (r[o1 + 4] - r[o0 + 4]) * u;
          if (resting) for (let k = 0; k < 3; k++) {
            const th = thumps[k], hu = (t - th.t) / HOP;
            if (hu <= 0 || hu >= 1 || th.t < p.born + p.restAt * FR) continue;
            const hg = th.k * Math.exp (-Math.abs (x - th.x) / 85) * (0.75 + 0.25 * p.jit[3]), arc = 4 * hu * (1 - hu);
            y -= hg * arc; air = Math.max (air, hg * arc / 4); rot += hg * 0.07 * p.jit[4] * Math.sin (hu * 6.2832);
          }
          if (pu > 0) {
            // peel: the sticker swells a hair, lifts off the page (its shadow drops away), tips and shrinks to nothing
            const q = pu * pu;
            sc *= (1 + 0.16 * Math.sin (Math.min (1, pu * 2.4) * Math.PI)) * (1 - q * pu);
            fl *= Math.cos (pu * 0.7); y -= 1.8 * pu; air = Math.max (air, pu * 1.2);
          }
          if (sc > 0.02) drawPiece (ctx, p, x, y, rot, fl, sc, air);
        }
        act.length = j;
        any = any || j > 0;
        ctx.setTransform (dpr, 0, 0, dpr, 0, 0);
        return any;
      },
    };
  },
});

// strings: three fine strings run across the well, tied to small brass pins. A hit plucks them at its x; each string
// rings with real modal (standing-wave) motion that decays. The blur of the moving string (its envelope) shows as a
// soft lens of the slice's colour that runs out from the pluck point with the wave and fades.
'use strict';
PONDS.push ({
  id: 'strings',
  name: 'strings',
  ko: '줄 울림',
  idea: 'three fine strings across the well; a hit plucks them at its x and they ring with real standing waves, lit in the slice colour',
  make ({ w, h, dpr, theme, util }) {
    const W = w, H = h;
    let T = theme;
    const PIN = 9, X0 = PIN, X1 = W - PIN, L = X1 - X0;
    const NP = Math.max (20, Math.min (72, Math.round (L / 3))) + 1;    // samples along a string
    const NM = 18;                                                        // modes per string
    const PULL = 0.018, SNAP = 0.05;                                     // s
    const NSTR = 3, NSTOP = 7;
    // strings, bottom (low, kick) to top (high, hat)
    const SPEC = [
      { dy: 8, lw: 1.5, period: 0.48, tau: 0.58, D: 7, B: 0.0012, amp: 9.0, lim: 7.5, a0: 0.30 },
      { dy: 0, lw: 1.1, period: 0.27, tau: 0.46, D: 7, B: 0.0008, amp: 5.0, lim: 5.0, a0: 0.27 },
      { dy: -8, lw: 0.8, period: 0.13, tau: 0.30, D: 5, B: 0.0004, amp: 2.4, lim: 3.0, a0: 0.25 } ];
    const S = SPEC.map (sp => {
      const om = new Float32Array (NM), ga = new Float32Array (NM);
      for (let n = 1; n <= NM; n++) {
        om[n - 1] = n * (2 * Math.PI / sp.period) * Math.sqrt (1 + sp.B * n * n);   // a touch of stiffness
        ga[n - 1] = 1 / sp.tau + (n - 1) * (n - 1) / sp.D;                          // highs die first
      }
      return { ...sp, y: H / 2 + sp.dy + 0.5, om, ga,
        re: new Float32Array (NM), im: new Float32Array (NM), m2: new Float32Array (NM), Y: new Float32Array (NP), E: new Float32Array (NP),
        hf: new Float32Array (NP), cr: new Float32Array (NP), cg: new Float32Array (NP), cb: new Float32Array (NP),
        rw: new Float32Array (NP), live: false, emax: 0, hmax: 0, plucks: [] };
    });
    const SIN = new Float32Array (NP * NM);   // SIN[j * NM + n] = sin ((n+1) pi u_j)
    for (let j = 0; j < NP; j++) for (let n = 0; n < NM; n++) SIN[j * NM + n] = Math.sin ((n + 1) * Math.PI * j / (NP - 1));
    const XS = new Float32Array (NP); for (let j = 0; j < NP; j++) XS[j] = X0 + L * j / (NP - 1);

    const hex = util.hex;
    let inkRGB = hex (T.t.ink);
    const rgba = (r, g, b, a) => 'rgba(' + (r | 0) + ',' + (g | 0) + ',' + (b | 0) + ',' + (a < 0 ? 0 : a > 1 ? 1 : a).toFixed (3) + ')';
    const smooth = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);

    return {
      setTheme (t) { T = t; inkRGB = hex (T.t.ink); },
      hit (e) {
        const b = e.brightness, sPos = b * (NSTR - 1), rnd = util.rand ((e.t * 7.3 + e.slice * 131 + 17) | 0);
        const ws = []; let wm = 0;
        for (let i = 0; i < NSTR; i++) { ws[i] = Math.exp (- (i - sPos) * (i - sPos) / 0.5); wm = Math.max (wm, ws[i]); }
        const p = Math.min (0.95, Math.max (0.05, 0.04 + e.x * 0.92));
        const v = e.velocity;
        const day = hex (util.mix (e.deep, '#3b2a24', 0.08)), night = hex (e.colour);
        const glow = hex (util.mix (e.colour, '#fffdf7', 0.45));   // the light core of a night glint
        for (let i = 0; i < NSTR; i++) {
          const wi = ws[i] / wm; if (wi < 0.15) continue;
          const st = S[i];
          // how much already rings on this string (a bound): a busy string takes new plucks more gently
          let busy = 0;
          for (const q of st.plucks) busy += Math.abs (q.h) * Math.exp (- Math.max (0, (e.t - q.t0) / 1000) / st.tau);
          const sign = rnd() < 0.5 ? -1 : 1;
          const hgt = sign * st.amp * (0.35 + 0.65 * v) * wi / (1 + 0.5 * busy / st.amp);
          // a triangle pluck at p, softened by the finger: a wide thumb for lows, a sharp pick for highs
          const A = new Float32Array (NM), k = 2 * hgt / (Math.PI * Math.PI * p * (1 - p)), fw = 0.085 * (1 - b);
          for (let n = 1; n <= NM; n++) A[n - 1] = k * Math.sin (n * Math.PI * p) / (n * n) * Math.exp (- (n * fw) * (n * fw));
          const heat = (0.45 + 0.55 * v) * wi * wi;   // sympathetic neighbours move but hardly light up
          const TR = e.reversed ? 1.7 * st.tau : 0;
          const life = e.reversed ? TR + SNAP + 0.14
            : PULL + Math.max (st.tau * Math.log (Math.abs (hgt) / 0.07), 0.6 * st.tau * Math.log (heat / 0.006));
          const gd = wi > 0.6 ? 0.14 + 0.24 * (1 - b) : 0;   // the glint where the finger let go
          st.plucks.push ({ t0: e.t, A, h: hgt, p, heat, rev: !! e.reversed, TR, life, day, night, glow,
            gd, gr: 1.6 + 1.3 * (1 - b), gv: 0.55 + 0.45 * v });
          if (st.plucks.length > 10) st.plucks.shift();
        }
      },
      draw (ctx, t) {
        const night = T.night;
        let anyLive = false;
        // --- 1. modal state per string --------------------------------------------------------------------------
        for (let i = 0; i < NSTR; i++) {
          const st = S[i], { re, im, m2, hf, cr, cg, cb, rw } = st;
          if (st.plucks.length === 0) { st.live = false; continue; }
          re.fill (0); im.fill (0); hf.fill (0); cr.fill (0); cg.fill (0); cb.fill (0); rw.fill (0);
          let wsum = 0, fH = 0, fR = 0, fG = 0, fB = 0, fA = 0;   // sums of plucks that already fill the string
          for (let q = st.plucks.length - 1; q >= 0; q--) {
            const pk = st.plucks[q], age = (t - pk.t0) / 1000;
            if (age > pk.life) { st.plucks.splice (q, 1); continue; }
            if (age < 0) continue;
            let tau, k = 1, still = false, heat, lens = 1;
            if (! pk.rev) {
              if (age < PULL) { const u = age / PULL; k = 1 - (1 - u) * (1 - u); still = true; tau = 0; }   // the finger pulls
              else tau = age - PULL;
              heat = pk.heat * Math.exp (- tau / (st.tau * 0.6));
              lens = smooth (tau / (st.period * 0.3));   // the blur appears once the string moves
            } else {
              if (age < pk.TR) {   // time runs backwards: the ring swells, the highs come last
                tau = pk.TR - age; k = smooth (age / (pk.TR * 0.45));
                heat = pk.heat * Math.exp (- tau / (st.tau * 0.6)) * k;
              } else {             // ...and it ends in the pluck shape, let go of all at once
                const u = (age - pk.TR) / SNAP; k = 1 - smooth (u); still = true; tau = 0;
                const hu = Math.min (1, (age - pk.TR) / 0.14); heat = pk.heat * (1 - hu) * (1 - hu);
              }
            }
            const amp = Math.abs (pk.h) * k * Math.exp (- tau / st.tau);
            const A = pk.A;
            if (still) { for (let n = 0; n < NM; n++) re[n] += A[n] * k; }
            else for (let n = 0; n < NM; n++) {
              const dec = Math.exp (- st.ga[n] * tau); if (dec < 1e-3) break;   // the highs are gone
              const a = A[n] * k * dec, ph = st.om[n] * tau;
              re[n] += a * Math.cos (ph); im[n] += a * Math.sin (ph);
            }
            // the colour (and the blur) run out from the pluck point with the wave
            const col = night ? pk.night : pk.day;
            const reach = pk.rev ? 2 : 2 * age / st.period + 0.04;
            wsum += amp;
            if (reach - 0.16 >= Math.max (pk.p, 1 - pk.p)) {
              fA += amp * lens; fH += heat; fR += col[0] * heat; fG += col[1] * heat; fB += col[2] * heat;
              continue;
            }
            for (let j = 0; j < NP; j++) {
              const d = Math.abs (j / (NP - 1) - pk.p);
              const win = d <= reach ? 1 : 1 - smooth ((d - reach) / 0.16);
              if (win <= 0) continue;
              rw[j] += amp * win * lens;
              const hh = heat * win;
              hf[j] += hh; cr[j] += col[0] * hh; cg[j] += col[1] * hh; cb[j] += col[2] * hh;
            }
          }
          st.live = st.plucks.length > 0;
          if (! st.live) continue;
          anyLive = true;
          // synthesis: displacement and envelope at each sample (soft-limited so a string never leaves its lane)
          let nmax = 0;
          for (let n = 0; n < NM; n++) { m2[n] = re[n] * re[n] + im[n] * im[n]; if (m2[n] > 1e-5) nmax = n + 1; }
          const { Y, E } = st; let emax = 0, hmax = 0;
          const iw = wsum > 1e-6 ? 1 / wsum : 0, lim = st.lim;
          for (let j = 0; j < NP; j++) {
            let y = 0, e2 = 0; const o = j * NM;
            for (let n = 0; n < nmax; n++) { const s = SIN[o + n]; y += re[n] * s; e2 += m2[n] * s * s; }
            Y[j] = lim * Math.tanh (y / lim);
            hf[j] += fH; cr[j] += fR; cg[j] += fG; cb[j] += fB;
            const e = lim * Math.tanh (Math.sqrt (e2) / lim) * Math.min (1, (rw[j] + fA) * iw);
            E[j] = e;
            if (e > emax) emax = e;
            if (hf[j] > hmax) hmax = hf[j];
          }
          st.emax = emax; st.hmax = hmax;
        }

        // --- 2. the strings: the lens of the blur, then the string itself ---------------------------------------
        ctx.lineJoin = 'round'; ctx.lineCap = 'round';
        const LA = night ? 0.26 : 0.22, EA = night ? 0.34 : 0.3, SHY = 2;
        const shadowCol = night ? 'rgba(10,7,5,0.32)' : rgba (inkRGB[0], inkRGB[1], inkRGB[2], 0.09);
        for (let i = 0; i < NSTR; i++) {
          const st = S[i], a0 = night ? st.a0 * 0.85 : st.a0;
          ctx.lineWidth = st.lw;
          if (! st.live) {
            ctx.beginPath(); ctx.moveTo (X0, st.y); ctx.lineTo (X1, st.y);
            ctx.strokeStyle = shadowCol; ctx.translate (0, SHY); ctx.stroke(); ctx.translate (0, -SHY);
            ctx.strokeStyle = rgba (inkRGB[0], inkRGB[1], inkRGB[2], a0);
            ctx.stroke(); continue;
          }
          const { Y, E, hf, cr, cg, cb } = st, em = st.emax + 1e-4;
          // gradients along the string: the lens colour (alpha = heat) and the string colour (ink -> slice colour)
          const gl = ctx.createLinearGradient (X0, 0, X1, 0), gs = ctx.createLinearGradient (X0, 0, X1, 0);
          for (let s = 0; s <= NSTOP; s++) {
            const j = Math.round (s * (NP - 1) / NSTOP), hv = hf[j];
            const R = hv > 1e-5 ? cr[j] / hv : inkRGB[0], Gc = hv > 1e-5 ? cg[j] / hv : inkRGB[1], Bc = hv > 1e-5 ? cb[j] / hv : inkRGB[2];
            const m = Math.min (1, hv * 1.5), ms = m * Math.min (1, Math.sqrt (E[j] / em) * 1.4), mc = Math.sqrt (ms);
            gl.addColorStop (s / NSTOP, rgba (R, Gc, Bc, m));
            gs.addColorStop (s / NSTOP, rgba (inkRGB[0] + (R - inkRGB[0]) * mc, inkRGB[1] + (Gc - inkRGB[1]) * mc,
              inkRGB[2] + (Bc - inkRGB[2]) * mc, a0 + (1 - a0) * ms));
          }
          if (em > 0.25 && st.hmax > 0.01) {
            // the lens: where the string sweeps, with firmer edges (a string lingers at its turning points)
            ctx.beginPath(); ctx.moveTo (X0, st.y);
            for (let j = 2; j < NP - 1; j += 2) ctx.lineTo (XS[j], st.y - E[j]);
            ctx.lineTo (X1, st.y);
            for (let j = (NP - 2) & ~1; j > 0; j -= 2) ctx.lineTo (XS[j], st.y + E[j]);
            ctx.closePath();
            ctx.fillStyle = gl; ctx.globalAlpha = LA; ctx.fill();
            ctx.strokeStyle = gl; ctx.lineWidth = 0.9; ctx.globalAlpha = EA; ctx.stroke();
            ctx.globalAlpha = 1; ctx.lineWidth = st.lw;
          }
          ctx.beginPath(); ctx.moveTo (X0, st.y + Y[0]);
          for (let j = 1; j < NP; j++) ctx.lineTo (XS[j], st.y + Y[j]);
          ctx.strokeStyle = shadowCol; ctx.translate (0, SHY); ctx.stroke(); ctx.translate (0, -SHY);   // its shadow on the floor
          if (night && st.hmax > 0.01) {   // at night, a soft halo of light around the lit string
            ctx.strokeStyle = gl; ctx.lineWidth = st.lw + 2.8; ctx.globalAlpha = 0.22; ctx.stroke();
            ctx.globalAlpha = 1; ctx.lineWidth = st.lw;
          }
          ctx.strokeStyle = gs; ctx.stroke();
        }

        // --- 3. glints: a bead of light where the finger let go, riding the string ------------------------------
        for (let i = 0; i < NSTR; i++) {
          const st = S[i]; if (! st.live) continue;
          for (const pk of st.plucks) {
            if (! pk.gd) continue;
            const age = (t - pk.t0) / 1000;
            let a, pop = 1;
            if (! pk.rev) {   // a quick flash that settles into a bead and fades
              const u = age / pk.gd; if (u >= 1 || u < 0) continue;
              a = (1 - u) * (1 - u) * smooth (age / 0.012); pop = 1 + 0.25 * (1 - smooth (u / 0.3));
            } else {          // reversed: the bead gathers as the ring swells, and vanishes with the cut
              const u = (age - (pk.TR - 0.3)) / 0.3; if (u <= 0 || age > pk.TR + SNAP) continue;
              a = u < 1 ? u * u : 1 - (age - pk.TR) / SNAP; pop = 0.7 + 0.3 * Math.min (1, u);
            }
            a *= pk.gv;
            const jf = pk.p * (NP - 1), j = Math.min (NP - 2, jf | 0), f = jf - j;
            const x = X0 + pk.p * L, y = st.y + st.Y[j] + (st.Y[j + 1] - st.Y[j]) * f, r = pk.gr * pop;
            const c = night ? pk.night : pk.day, g = pk.glow;
            const R = night ? r * 2.2 : r * 1.45;
            const rg = ctx.createRadialGradient (x, y, 0, x, y, R);
            if (night) {
              rg.addColorStop (0, rgba (g[0], g[1], g[2], a)); rg.addColorStop (0.25, rgba (c[0], c[1], c[2], a * 0.75));
            } else {
              rg.addColorStop (0, rgba (c[0], c[1], c[2], a)); rg.addColorStop (0.38, rgba (c[0], c[1], c[2], a * 0.85));
              rg.addColorStop (0.5, rgba (c[0], c[1], c[2], a * 0.3));
            }
            rg.addColorStop (1, rgba (c[0], c[1], c[2], 0));
            ctx.fillStyle = rg; ctx.beginPath(); ctx.arc (x, y, R, 0, Math.PI * 2); ctx.fill();
          }
        }

        // --- 4. pins: small brass knots where the strings are tied ----------------------------------------------
        ctx.fillStyle = night ? '#c9a25e' : '#b88a3e';
        ctx.globalAlpha = night ? 0.75 : 0.8;
        ctx.beginPath();
        for (let i = 0; i < NSTR; i++) {
          const y = S[i].y, r = 0.55 + S[i].lw * 0.45;
          ctx.moveTo (X0 + r, y); ctx.arc (X0, y, r, 0, Math.PI * 2);
          ctx.moveTo (X1 + r, y); ctx.arc (X1, y, r, 0, Math.PI * 2);
        }
        ctx.fill(); ctx.globalAlpha = 1;
        return anyLive;
      },
    };
  },
});

// ink — suminagashi (floating ink). Every hit drops ink into still water: it blooms into rings that push the older
// ink aside (area-preserving, so colours never overlap and never turn to mud), the water curls them into marbled
// swirls, then a drop of clear water opens each bloom into thin rings that fade away. Ink boundaries are closed
// curves moved by closed-form flows (the maths of marbling), drawn back to front as smooth filled paths.
PONDS.push ({
  id: 'ink',
  name: 'ink',
  ko: '먹물 마블링',
  idea: 'suminagashi: each hit drops ink that blooms into rings, curls with the water and clears',
  make ({ w, h, dpr, theme, util }) {
    const W = w, H = h, K = 1.35;          // K: the pond is seen a little from the side (plan y = screen y * K)
    const PH = H * K, YM = PH / 2;
    let T = theme;
    const STEPS = 24;                       // fade ramp steps (precomputed colour strings, no per-frame allocation)
    const MAX2 = 3.8 * 3.8, MIN2 = 1.2 * 1.2, MAXN = 220;
    const SHEAR = 0.12;                     // the water drifts: a slow shear along the strip (1/s)
    const BUDGET = 1500;                    // most live curve points before the oldest ink is cleared early
    const drops = [], curves = [], flows = [];
    let lastT = null, lastCut = -1e9;

    // ---- curves: closed polylines, drawn as smooth quadratic paths ----------------------------------------------
    function inside (c, x, y) {
      const p = c.p, n = c.n; let s = false;
      for (let i = 0, j = n - 1; i < n; j = i++) {
        const yi = p[2 * i + 1], yj = p[2 * j + 1];
        if ((yi > y) !== (yj > y) && x < (p[2 * j] - p[2 * i]) * (y - yi) / (yj - yi) + p[2 * i]) s = ! s;
      }
      return s;
    }
    function addCircle (drop, cx, cy, r, ci, f) {
      const n = Math.max (10, Math.min (120, Math.ceil (2 * Math.PI * r / 1.6)));
      const cap = Math.max (48, n * 2);
      const c = { p: new Float64Array (cap * 2), q: new Float64Array (cap * 2), cap, n, drop, ci, f, edge: 0, parent: null, x0: 0, x1: 0, y0: 0, y1: 0 };
      drop.nc++;
      for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; c.p[2 * i] = cx + Math.cos (a) * r; c.p[2 * i + 1] = cy + Math.sin (a) * r; }
      for (let i = curves.length - 1; i >= 0; i--) if (inside (curves[i], cx, cy)) { c.parent = curves[i]; break; }
      bbox (c); curves.push (c);
      return c;
    }
    function bbox (c) {
      const p = c.p; let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
      for (let i = 0; i < c.n; i++) { const x = p[2 * i], y = p[2 * i + 1]; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      c.x0 = x0; c.x1 = x1; c.y0 = y0; c.y1 = y1;
    }
    function far2 (c, x, y) {               // squared distance from a point to a curve's box
      const dx = x < c.x0 ? c.x0 - x : x > c.x1 ? x - c.x1 : 0, dy = y < c.y0 ? c.y0 - y : y > c.y1 ? y - c.y1 : 0;
      return dx * dx + dy * dy;
    }
    // keep segments between MIN and MAX: the 4-point interpolating subdivision keeps the curve smooth
    function refine (c, sh) {
      const n = c.n;
      if (sh) { const p = c.p; for (let i = 0; i < n; i++) p[2 * i] += sh * (p[2 * i + 1] - YM); }
      if (c.cap < Math.min (MAXN, n * 2)) {
        const cap = Math.min (MAXN + 4, n * 2 + 16), p = new Float64Array (cap * 2);
        p.set (c.p.subarray (0, n * 2)); c.p = p; c.q = new Float64Array (cap * 2); c.cap = cap;
      }
      const p = c.p, q = c.q; let m = 0, gone = 0;
      for (let i = 0; i < n; i++) {
        const i1 = i + 1 < n ? i + 1 : 0, x1 = p[2 * i], y1 = p[2 * i + 1], x2 = p[2 * i1], y2 = p[2 * i1 + 1];
        q[2 * m] = x1; q[2 * m + 1] = y1; m++;
        const dx = x2 - x1, dy = y2 - y1, L2 = dx * dx + dy * dy;
        if (L2 > MAX2 && m < c.cap - 1 && n + m - i < MAXN) {
          const i0 = i > 0 ? i - 1 : n - 1, i2 = i1 + 1 < n ? i1 + 1 : 0;
          q[2 * m] = (9 * (x1 + x2) - p[2 * i0] - p[2 * i2]) / 16; q[2 * m + 1] = (9 * (y1 + y2) - p[2 * i0 + 1] - p[2 * i2 + 1]) / 16; m++;
        } else if (L2 < MIN2 && n - gone > 10 && i1 !== 0) {
          const i2 = i1 + 1 < n ? i1 + 1 : 0, ex = p[2 * i2] - x1, ey = p[2 * i2 + 1] - y1;
          if (ex * ex + ey * ey < MAX2) { i++; gone++; }
        }
      }
      c.q = p; c.p = q; c.n = m; bbox (c);
    }

    // ---- flows (plan coordinates) ------------------------------------------------------------------------------
    // a drop of area dA at (cx, cy): every point moves out so that |p-c|^2 grows by dA (negative = a sink)
    function movePt (o, cx, cy, dA) { const dx = o.x - cx, dy = o.y - cy, d2 = dx * dx + dy * dy; if (d2 < 1e-6) return; const k = d2 + dA > 0 ? Math.sqrt ((d2 + dA) / d2) : 0; o.x = cx + dx * k; o.y = cy + dy * k; }
    function pushAll (cx, cy, dA, self, skipSelf) {
      const lim = dA * dA * 2.5e5, rl2 = Math.sqrt (lim);
      for (let kc = 0; kc < curves.length; kc++) { const c = curves[kc];
        if (skipSelf && c.drop === self) continue;
        if (far2 (c, cx, cy) > rl2) continue;
        const p = c.p, n = c.n;
        for (let i = 0; i < n; i++) {
          const dx = p[2 * i] - cx, dy = p[2 * i + 1] - cy, d2 = dx * dx + dy * dy;
          if (d2 * d2 > lim) continue;
          const k = d2 + dA > 0 ? Math.sqrt ((d2 + dA) / (d2 + 1e-9)) : 0;
          p[2 * i] = cx + dx * k; p[2 * i + 1] = cy + dy * k;
        }
      }
      for (let kd = 0; kd < drops.length; kd++) { const d = drops[kd]; if (d !== self) movePt (d, cx, cy, dA); }
      for (let kf = 0; kf < flows.length; kf++) { const f = flows[kf]; movePt (f, cx, cy, dA); }
    }
    function env (o, t) {                    // smooth rise, then exponential decay
      const a = t - o.born; if (a <= 0) return 0;
      const r = a < o.rise ? (a / o.rise) * (a / o.rise) * (3 - 2 * a / o.rise) : 1;
      return r * Math.exp (-Math.max (0, a - o.rise) / o.tau);
    }
    // one local eddy: a turn (angle a at the centre) plus a strain (s), both fading as (1 - r^2/L)^3 to nothing at
    // sqrt(L). The turn is an exact rotation, the strain comes from psi = s u v (1 - r^2/L)^3: both keep area.
    const MV = [0, 0];
    function eddyAt (x, y, f, a, s) {
      const dx = x - f.x, dy = y - f.y, q = 1 - (dx * dx + dy * dy) * f.iL;
      if (q <= 0) return false;
      const q2 = q * q, th = 0.5 * a * q2 * q, k = 1 / (1 + th * th), co = (1 - th * th) * k, si = 2 * th * k;
      let nx = dx * co - dy * si, ny = dx * si + dy * co;
      if (s !== 0) {
        const u = dx * f.co + dy * f.si, v = -dx * f.si + dy * f.co, iL6 = 6 * f.iL;
        const du = s * u * q2 * (q - iL6 * v * v), dv = -s * v * q2 * (q - iL6 * u * u);
        nx += du * f.co - dv * f.si; ny += du * f.si + dv * f.co;
      }
      MV[0] = f.x + nx; MV[1] = f.y + ny; return true;
    }
    function eddy (f, a, s) {
      const L = f.L;
      for (let kc = 0; kc < curves.length; kc++) { const c = curves[kc];
        if (f.only && c.drop !== f.only) continue;
        if (far2 (c, f.x, f.y) > L) continue;
        const p = c.p, n = c.n;
        for (let i = 0; i < n; i++) if (eddyAt (p[2 * i], p[2 * i + 1], f, a, s)) { p[2 * i] = MV[0]; p[2 * i + 1] = MV[1]; }
      }
      if (f.only) return;
      for (let kd = 0; kd < drops.length; kd++) { const d = drops[kd]; if (d.next < d.pat.length || d.kind < 2) { if (eddyAt (d.x, d.y, f, a, s)) { d.x = MV[0]; d.y = MV[1]; } } }
    }
    function flow (t, dt) {
      const sec = dt / 1000, sh = SHEAR * sec;          // (the curves get the shear in refine)
      for (let kd = 0; kd < drops.length; kd++) { const d = drops[kd]; d.x += sh * (d.y - YM); }
      for (let kf = 0; kf < flows.length; kf++) { const f = flows[kf]; f.x += sh * (f.y - YM); }
      for (let kf = 0; kf < flows.length; kf++) { const f = flows[kf];
        const e = env (f, t) * sec; if (e < 2e-4) continue;
        eddy (f, f.w * e, f.st * e);
      }
    }
    function addFlow (o) { o.L = o.r * o.r; o.iL = 1 / o.L; o.st = o.st || 0; o.co = o.co ?? 1; o.si = o.si || 0; flows.push (o); return o; }

    // ---- colours -----------------------------------------------------------------------------------------------
    function ramp (hex) { const well = T.t.well, a = []; for (let i = 0; i <= STEPS; i++) a.push (util.mix (hex, well, i / STEPS)); return a; }
    function paint (d) {
      const night = T.night;
      const deep = night ? util.mix (d.deep, d.colour, 0.3) : d.deep;
      const light = night ? d.colour : util.mix (d.colour, d.deep, 0.12);
      // 0 deep, 1 light, 2 the clear-water hairline (a glint by day, a dark gap by night), 3 between deep and light
      d.ramps = [ramp (deep), ramp (light), ramp (night ? util.mix (T.t.well, T.t.shadow, 0.2) : util.mix (T.t.well, T.t.card, 0.8)), ramp (util.mix (deep, light, 0.5))];
      // a faint bleed of ink into the water around the drop's rim
      d.halo = []; for (let i = 0; i <= STEPS; i++) d.halo.push (util.rgba (deep, (night ? 0.2 : 0.16) * (1 - i / STEPS)));
    }

    // ring patterns, by radius from the rim inwards: [radius fraction where the band starts, colour, hairline]
    // colour 0 deep, 1 light, 3 between; hairline = a thin line of clear water drawn on the band's rim, as in suminagashi
    const RINGS = [
      [[[1, 0], [0.84, 1, 1], [0.67, 3, 1], [0.49, 1, 1], [0.3, 0, 1]],                // low (kick)
       [[1, 0], [0.82, 3, 1], [0.64, 1, 1], [0.47, 0, 1], [0.33, 1, 1]]],
      [[[1, 0], [0.77, 1, 1], [0.46, 0, 1]],                                          // mid (snare)
       [[1, 1], [0.8, 0, 1], [0.5, 1, 1]]],
      [[[1, 0], [0.45, 1]], [[1, 0]]],                                                 // high (hat)
      [[[1, 1], [0.62, 0]], [[1, 0], [0.55, 1]]],                                      // open hat
    ];
    function pattern (pk, rnd) {           // as emitted-area fractions, with a little play in every band
      return RINGS[pk][rnd () < 0.5 ? 0 : 1].map (([rho, ci, e], i) => { const r = i ? rho + (rnd () - 0.5) * 0.05 : 1; return [1 - r * r, ci, e || 0]; });
    }

    function strength (d, t) {               // 0..1: how much ink colour is left (1 = full)
      const a = t - d.born;
      if (d.cut && t > d.cut) { const k = Math.min (1, (t - d.cut) / 350); if (k >= 1) return 0; return Math.min (1 - k * k * (3 - 2 * k), d.rev ? 1 : strength0 (d, a)); }
      return d.rev ? strengthRev (d, a) : strength0 (d, a);
    }
    function strength0 (d, a) {
      const k = Math.max (0, (a / d.life - 0.55) / 0.45); return k >= 1 ? 0 : 1 - k * k * (3 - 2 * k);
    }
    function strengthRev (d, a) { if (a < d.dur) { const u = a / d.dur; return 0.3 + 0.7 * u * u; } return 1; }

    return {
      setTheme (t) { T = t; for (const d of drops) paint (d); },
      hit (e) {
        const rnd = util.rand ((e.slice + 1) * 7919 + Math.round (e.t * 13));
        const b = e.brightness, v = e.velocity, kind = b < 0.3 ? 0 : b < 0.7 ? 1 : 2, pk = kind === 2 && b < 0.86 ? 3 : kind;
        const R = (kind === 2 ? (2.4 + 7 * (1 - b)) * (0.7 + 0.3 * v) : (3 + 21 * Math.pow (1 - b, 1.4)) * (0.62 + 0.38 * v)) * Math.min (1, Math.pow (W / 230, 0.35));
        const jx = kind === 2 ? 14 : 4, jy = kind === 0 ? 2 : kind === 1 ? 5 : 16;
        const d = {
          x: 12 + e.x * (W - 24) + (rnd () - 0.5) * jx, y: (H / 2 + (rnd () - 0.5) * jy) * K,
          born: e.t, A: R * R, a: 0, dur: 110 + 900 * Math.pow (1 - b, 1.5), life: 1100 + 1400 * (1 - b),
          pat: pattern (pk, rnd), next: 0, nc: 0, rev: e.reversed, colour: e.colour, deep: e.deep, ramps: null, k: 1, kind, R,
          clear: null, ca: 0, end: 0, room: 0,
        };
        paint (d);
        drops.push (d);

        const dir = rnd () < 0.5 ? 1 : -1, wob = (rnd () - 0.5) * 0.8, th = rnd () * Math.PI * 2;
        if (d.rev) {
          // reversed: the rings are already there (faint, curled); they unwind and gather into one bead
          d.dur = 300 + 650 * Math.pow (1 - b, 1.3);
          for (const [f, ci, ed] of d.pat) addCircle (d, d.x, d.y, Math.sqrt (d.A * (1 - f)), ci, f).edge = ed;
          d.next = d.pat.length; d.a = d.A;
          // the rings start stretched and twisted (as if they had been swirling); the twist unwinds as they gather
          const a = wob * 0.6, fl = addFlow ({ x: d.x, y: d.y, r: R * 2.4, w: dir * 2.4, st: 1.1, co: Math.cos (a), si: Math.sin (a), only: d });
          for (let i = 0; i < 24; i++) { eddy (fl, fl.w * 0.03, fl.st * 0.03); for (const c of curves) if (c.drop === d) refine (c); }
          Object.assign (fl, { w: -fl.w * 1.1, st: 0, born: e.t, rise: d.dur * 0.25, tau: d.dur * 0.4 });
          return;
        }
        // the water's answer: low = a slow wide turn (the rings lean into a soft curl), mid = a tighter turn
        // (a spiral), high = strain with a little turn (the speck pulls into a fine curved thread)
        if (kind === 0) addFlow ({ x: d.x + Math.cos (th) * R * 0.5, y: d.y + Math.sin (th) * R * 0.5, r: R * 2.6, w: dir * 1.7, born: e.t + d.dur * 0.15, rise: d.dur * 0.8, tau: 900 });
        else if (kind === 1) addFlow ({ x: d.x + Math.cos (th) * R * 0.55, y: d.y + Math.sin (th) * R * 0.55, r: R * 2.2, w: dir * 2.8, born: e.t + d.dur * 0.2, rise: d.dur, tau: 650 });
        else {
          const a = wob * 0.7;
          addFlow ({ x: d.x, y: d.y, r: R * 6, w: dir * 1.6, st: 2.6, co: Math.cos (a), si: Math.sin (a), born: e.t + d.dur * 0.3, rise: 100, tau: 380 });
        }
      },
      draw (ctx, t) {
        const dt = lastT === null ? 16 : Math.max (0, Math.min (50, t - lastT)); lastT = t;
        for (let kd = 0; kd < drops.length; kd++) { const d = drops[kd];
          const age = t - d.born;
          if (d.rev) {
            if (d.room < d.A) { const u = Math.min (1, age / 160), A = d.A * (1 - (1 - u) * (1 - u)); pushAll (d.x, d.y, A - d.room, d, true); d.room = A; }
            // gather: the area falls (slow, then fast) down to a small bead, then the bead lifts off
            const bead = 2.4 * 2.4, u = Math.min (1, Math.max (0, age / d.dur));
            let A = bead + (d.A - bead) * (1 - u * u * u);
            if (age > d.dur + 90) { const v = Math.min (1, (age - d.dur - 90) / 110); A = bead * (1 - v * v); if (v >= 1) d.end = 1; }
            const dA = A - d.a;
            if (dA < -1e-6) { pushAll (d.x, d.y, dA, d, false); d.a = A; }
            const wr = 0.04 + 0.3 * u * u;   // the rings round up as they gather, so the bead is a true drop
            for (let i = curves.length - 1; i >= 0; i--) {
              const c = curves[i]; if (c.drop !== d) continue;
              const r2 = A - c.f * d.A;
              if (r2 < 0.05 || d.end) { curves.splice (i, 1); d.nc--; continue; }
              const r = Math.sqrt (r2), p = c.p;
              for (let j = 0; j < c.n; j++) {
                const dx = p[2 * j] - d.x, dy = p[2 * j + 1] - d.y, k = 1 + wr * (r / (Math.sqrt (dx * dx + dy * dy) + 1e-9) - 1);
                p[2 * j] = d.x + dx * k; p[2 * j + 1] = d.y + dy * k;
              }
            }
            d.k = strength (d, t);
            continue;
          }
          const u = Math.min (1, Math.max (0, age / d.dur));
          const A = d.A * (1 - (1 - u) * (1 - u));
          const dA = A - d.a;
          if (dA > 1e-6) { pushAll (d.x, d.y, dA, d, false); d.a = A; }
          while (d.next < d.pat.length && d.pat[d.next][0] * d.A <= A + 1e-9) {
            const [f, ci, ed] = d.pat[d.next++];
            addCircle (d, d.x, d.y, Math.sqrt (Math.max (0.02, A - f * d.A)), ci, f).edge = ed;
          }
          // later, a drop of clear water opens the bloom: its rings thin out while they fade
          if (d.kind < 2) {
            const c0 = age - d.life * 0.36;
            if (c0 > 0) {
              const v = Math.min (1, c0 / (d.life * 0.5)), Ac = d.A * 0.55 * (1 - (1 - v) * (1 - v) * (1 - v));
              if (! d.clear) { d.clear = addCircle (d, d.x, d.y, 0.3, -1, 1); d.ca = 0.09; }
              if (Ac - d.ca > 1e-6) { pushAll (d.x, d.y, Ac - d.ca, d, false); d.ca = Ac; }
            }
          }
          d.k = strength (d, t);
          if (d.k <= 0) d.end = 1;
        }
        flow (t, dt);
        const sh = SHEAR * dt / 1000;
        for (let kc = 0; kc < curves.length; kc++) { const c = curves[kc]; refine (c, sh); }

        // tidy: a finished curve can go once nothing older and alive lies under it (else it stays as clear water)
        for (let i = 0; i < curves.length; i++) {
          const c = curves[i]; if (! c.drop.end) continue;
          let p = c.parent; while (p && p.drop.end) p = p.parent;
          if (! p) { curves.splice (i--, 1); c.drop.nc--; }
        }
        for (let i = drops.length - 1; i >= 0; i--) if (drops[i].end && drops[i].nc <= 0) drops.splice (i, 1);
        for (let i = flows.length - 1; i >= 0; i--) if (t - flows[i].born > flows[i].rise + flows[i].tau * 3.2) flows.splice (i, 1);

        // budget: when the pond gets very busy, the oldest ink clears early (keeps a frame near 0.3 ms)
        let np = 0; for (let kc = 0; kc < curves.length; kc++) { const c = curves[kc]; if (! c.drop.cut && ! c.drop.end) np += c.n; }
        if (np > BUDGET && t - lastCut > 120) for (let kd = 0; kd < drops.length; kd++) { const d = drops[kd]; if (! d.end && ! d.cut && ! d.rev) { d.cut = lastCut = t; break; } }
        const well = T.t.well;
        ctx.save (); ctx.scale (1, 1 / K); ctx.lineWidth = 0.85;
        for (let kc = 0; kc < curves.length; kc++) { const c = curves[kc];
          if (c.x1 < -2 || c.x0 > W + 2 || c.y1 < -2 || c.y0 > PH + 2) continue;
          const d = c.drop, n = c.n, p = c.p;
          const step = Math.round ((1 - d.k) * STEPS);
          ctx.fillStyle = c.ci < 0 || d.end ? well : d.ramps[c.ci][step];
          const halo = c.f === 0 && d.kind < 2 && ! d.end;
          ctx.beginPath ();
          ctx.moveTo ((p[2 * n - 2] + p[0]) / 2, (p[2 * n - 1] + p[1]) / 2);
          for (let i = 0; i < n; i++) {
            const x = p[2 * i], y = p[2 * i + 1], j = i + 1 < n ? i + 1 : 0;
            ctx.quadraticCurveTo (x, y, (x + p[2 * j]) / 2, (y + p[2 * j + 1]) / 2);
          }
          if (halo) { ctx.lineWidth = 2.8; ctx.strokeStyle = d.halo[step]; ctx.stroke (); ctx.lineWidth = 0.85; }
          ctx.fill ();
          if (c.edge && ! d.end) { ctx.strokeStyle = d.ramps[2][step]; ctx.stroke (); }
        }
        ctx.restore ();
        return curves.length > 0;
      },
    };
  },
});

// koi — 연못: a little pond seen from above. A few koi drift lazily; a hit drops something on the water at the slice's
// x (kick: a blossom petal, snare/perc: a pinch of food, hat: a glint of light) and the nearest fish dart to it with a
// flick of the tail, then slow down and nibble. Reversed slices run the drop backwards and the fish scatter away.
'use strict';
PONDS.push ({
  id: 'koi',
  name: 'koi pond',
  ko: '잉어 연못',
  idea: 'a tiny pond seen from above: koi drift lazily; a hit drops a petal, food or a glint and the nearest fish dart to it — reversed, they scatter',
  make ({ w, h, dpr, theme, util }) {
    const W = w, H = h, TAU = Math.PI * 2, PI = Math.PI;
    const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
    const wrap = a => a - TAU * Math.round (a / TAU);
    const ex = (dt, tau) => 1 - Math.exp (-dt / tau);
    let T = theme;

    // ---- the fish's shape ----------------------------------------------------------------------------------------
    const N = 6;                 // spine points, head → tail root
    const K = 4.2;               // body wave: phase lag (rad) from head to tail root
    const TAILF = 0.52;          // tail fin length / body length
    const MAXB = 0.42;           // max bend per spine joint (rad)
    // half width along the body (s = 0 head point, 1 tail root; the nose sits a little ahead)
    const PS = [-0.08, 0.0, 0.12, 0.26, 0.42, 0.58, 0.74, 0.88, 1.0];
    const PW = [0, 0.128, 0.176, 0.19, 0.172, 0.134, 0.09, 0.056, 0.033];
    function prof (s) {
      if (s <= PS[0]) return 0; if (s >= 1) return PW[8];
      let i = 1; while (PS[i] < s) i++;
      const u = (s - PS[i - 1]) / (PS[i] - PS[i - 1]); return PW[i - 1] + (PW[i] - PW[i - 1]) * u;
    }

    // ---- colours -------------------------------------------------------------------------------------------------
    // koi varieties: white with a red crown (tancho), orange (ogon), white with red (kohaku), gold (yamabuki)
    const KINDS = [
      { day: { edge: '#e6d6c2', main: '#fffaf1', hi: '#ffffff', fin: '#fffaf1', finA: 0.82, spot: '#ee4b35' },
        night: { edge: '#d9c9b4', main: '#f8eedf', hi: '#fffaf1', fin: '#f8eedf', finA: 0.8, spot: '#f0553f' }, crown: true },
      { day: { edge: '#ec7330', main: '#ff9a4c', hi: '#ffc48c', fin: '#ff9650', finA: 0.62, spot: '#ff9a4c' },
        night: { edge: '#e86f2e', main: '#ff9a4c', hi: '#ffc48c', fin: '#ff9650', finA: 0.8, spot: '#ff9a4c' }, gloss: true },
      { day: { edge: '#e6d6c2', main: '#fffaf1', hi: '#ffffff', fin: '#fffaf1', finA: 0.82, spot: '#f0573c' },
        night: { edge: '#d9c9b4', main: '#f8eedf', hi: '#fffaf1', fin: '#f8eedf', finA: 0.8, spot: '#f25d42' },
        patches: [[0.06, 0.44, 0.92, 0.12], [0.56, 0.84, 0.78, -0.18]] },
      { day: { edge: '#e39d22', main: '#ffc443', hi: '#ffe7a3', fin: '#ffc450', finA: 0.62, spot: '#ffc443' },
        night: { edge: '#e39d22', main: '#ffc443', hi: '#ffe7a3', fin: '#ffc450', finA: 0.8, spot: '#ffc443' }, gloss: true },
    ];
    // a deep fish is seen through more water: its colours, mixed toward the water, in LV steps (made once per theme)
    const LV = 9;
    let P;
    function palette () {
      const n = T.night, t = T.t;
      P = {
        n,
        shadow: n ? 'rgba(10,7,5,0.42)' : util.rgba (t.ink, 0.15),
        pad: n ? util.oklch (0.46, 0.05, 128) : util.oklch (0.82, 0.07, 124),
        padEdge: n ? util.oklch (0.39, 0.045, 130) : util.oklch (0.72, 0.075, 130),
        padHi: n ? util.oklch (0.54, 0.055, 120) : util.oklch (0.89, 0.065, 112),
        vein: n ? util.oklch (0.41, 0.045, 130) : util.oklch (0.75, 0.075, 130),
        padShadow: n ? 'rgba(10,7,5,0.35)' : util.rgba (t.ink, 0.10),
        lotus: n ? '#e88e86' : '#ffa99c', lotusIn: n ? '#f7b3a8' : '#ffd2c8', lotusC: '#ffd23f',
      };
      const veil = n ? 0.3 : 0.42;
      for (const f of fish) {
        const k = n ? f.kind.night : f.kind.day;
        f.lv = [];
        for (let i = 0; i < LV; i++) {
          const m = i / (LV - 1) * veil, mx = c => util.mix (c, t.well, m);
          f.lv.push ({ edge: mx (k.edge), main: mx (k.main), hi: mx (k.hi), spot: mx (k.spot), fin: util.rgba (mx (k.fin), k.finA), eye: util.rgba (mx (n ? '#1a120e' : t.ink), n ? 0.8 : 0.72) });
        }
      }
      paintPads();
    }

    // ---- fish ----------------------------------------------------------------------------------------------------
    const CRUISE = 0, DART = 1, NIBBLE = 2, FLEE = 3;
    const R = util.rand (0x6b6f69);
    const count = W >= 190 ? 4 : 3;
    const SIZES = [12, 13.5, 14.5, 11.5];
    const fish = [];
    for (let i = 0; i < count; i++) {
      const L = SIZES[i] * clamp (H / 34, 0.8, 1.3) * (W < 150 ? 0.88 : 1);
      const hx = 26 + (i + 0.5) / count * (W - 52);
      const f = {
        i, kind: KINDS[i % KINDS.length], lv: null, L, seg: L / (N - 1),
        px: new Float64Array (N), py: new Float64Array (N), rx: new Float64Array (N), ry: new Float64Array (N),
        nx: new Float64Array (N), ny: new Float64Array (N),
        qx: new Float64Array (3), qy: new Float64Array (3), tx: new Float64Array (3), ty: new Float64Array (3),
        tnx: new Float64Array (3), tny: new Float64Array (3),
        x: hx + (R () - 0.5) * 20, y: H * (0.34 + 0.32 * ((i * 0.618) % 1)), a: (i % 2 ? PI : 0) + (R () - 0.5) * 0.4,
        v: 3, vc: 2.6 + R () * 1.6, w: 0, ph: R () * TAU, amp: 0.5, flick: 0, glance: 0, ga: 0,
        depth: 0.5, dbase: [0.3, 0.55, 0.42, 0.62][i % 4], home: hx, bob: 0,
        state: CRUISE, calm: false, follow: false, food: null, lastFood: null, ox: 0, oy: 0, gx: 0, gy: 0, timer: 0,
      };
      const ca = Math.cos (f.a), sa = Math.sin (f.a);
      for (let k = 0; k < N; k++) { f.px[k] = f.x - ca * f.seg * k; f.py[k] = f.y - sa * f.seg * k; }
      for (let k = 0; k < 3; k++) { f.qx[k] = f.px[N - 1] - ca * L * TAILF * 0.5 * k; f.qy[k] = f.py[N - 1] - sa * L * TAILF * 0.5 * k; }
      fish.push (f); wander (f, true);
    }
    function wander (f, ahead) {
      // a lazy goal in the fish's own stretch of the pond, mostly sideways
      // (to and fro around its home spot, so the long runs are level and the turns are few)
      const span = W / count * 0.8, face = Math.cos (f.a) > 0 ? 1 : -1;
      let side = f.x < f.home ? 1 : -1;
      if (ahead && (f.home + face * span - f.x) * face > 14) side = face;   // carry on the way it faces
      f.gx = clamp (f.home + side * span * (0.45 + 0.55 * R ()), 20, W - 20); f.gy = 11 + R () * (H - 22);
      if (ahead && side === face && (f.gx - f.x) * face < 14) f.gx = clamp (f.x + face * 14, 20, W - 20);
    }
    const order = fish.slice (), layer = fish.slice ();
    function homes () {
      // the fish keep their order along the pond (the i-th from the left lives in the i-th stretch): no tangles
      // (homes swap only when two fish have clearly passed each other, so nobody turns round for nothing)
      order.sort ((a, b) => a.home - b.home);
      for (let pass = 0; pass < count; pass++) {
        let swapped = false;
        for (let i = 0; i + 1 < count; i++) {
          const a = order[i], b = order[i + 1];
          if (a.x - b.x > 10) { const hm = a.home; a.home = b.home; b.home = hm; order[i] = b; order[i + 1] = a; swapped = true;
            for (const f of [a, b]) if (f.state === CRUISE && Math.abs (f.gx - f.home) > W / count * 1.2) wander (f, true); }
        }
        if (! swapped) break;
      }
    }

    // ---- surface things: items (petal, pellet, glint) and rings ---------------------------------------------------
    const PETAL = 0, PELLET = 1, GLINT = 2;
    const items = [], rings = [];
    const PADX = 18;
    function ring (x, y, born, dur, r0, r1, crest, trough, lw, peak, rev) {
      rings.push ({ x, y, born, dur, r0, r1, crest, trough, lw, peak, rev });
    }

    let last = null, acc = 0, lastHit = -1e9;
    function nearest (x, y, k, filter) {
      const out = [];
      for (const f of fish) { if (filter && ! filter (f)) continue; out.push (f); }
      out.sort ((a, b) => Math.hypot (a.x - x, a.y - y) - Math.hypot (b.x - x, b.y - y));
      return out.slice (0, k);
    }
    function sendTo (f, it, calm, follow) {
      if (f.food && f.food !== it) f.food.claims--;
      f.follow = !! follow;
      if (follow) {
        // a look from a little way off, beside the one that eats
        f.ox = (f.x > it.x ? 1 : -1) * 10; f.oy = (it.y > H / 2 ? -1 : 1) * 6;
        f.food = it; f.flick = 0.7; f.state = DART; f.timer = 0; f.calm = false; it.claims++; return;
      }
      // come at it from the fish's own side, level (the pond is only 34 px from bank to bank); a second fish from
      // the same side noses in next to the first, a little above or below
      let a = Math.atan2 (clamp (f.y - it.y, -0.5 * Math.abs (f.x - it.x) - 1, 0.5 * Math.abs (f.x - it.x) + 1), f.x - it.x);
      if (it.claims > 0 && Math.cos (a) * Math.cos (it.ang) > 0) {
        const a1 = it.ang + 0.6, a2 = it.ang - 0.6;
        a = (Math.sin (a1) > 0) === (f.y > it.y + Math.sin (it.ang) * 3) ? a1 : a2;
      } else if (! it.claims) it.ang = a;
      const rr = it.kind === PETAL ? 3.3 : 1.2;
      f.ox = Math.cos (a) * rr; f.oy = Math.sin (a) * rr * 0.8;
      f.food = it; it.claims++;
      if (f.state !== DART) f.flick = calm ? 0.4 : 1;
      f.state = DART; f.timer = 0; f.calm = !! calm;
    }
    function edible (it, f) {
      if (it.rev || it.eaten || it.gone || it.kind === GLINT || last < it.land || it === f.lastFood) return false;
      return it.kind === PELLET ? it.claims === 0 : it.bites + it.claims < 2;
    }
    function hungry (f, range) {
      let best = null, bd = range;
      for (const o of items) if (edible (o, f)) { const d = Math.hypot (o.x - f.x, o.y - f.y); if (d < bd) { bd = d; best = o; } }
      return best;
    }
    function free (f) { return f.state !== NIBBLE || f.timer > 0.25; }
    function freeFor (x, y) {
      // free to come: not in the middle of a bite, and not already on its way to something nearer
      return f => free (f) && ! (f.state === DART && ! f.calm && f.food && Math.hypot (f.food.x - f.x, f.food.y - f.y) < Math.hypot (x - f.x, y - f.y));
    }

    function drop (e, x, y, r) {
      const b = e.brightness, v = e.velocity;
      const hi = util.mix (e.colour, '#ffffff', 0.5);
      if (b < 0.3) {
        // kick: a blossom petal lands with a wide, slow ring; the two nearest fish dart to it
        const it = { kind: PETAL, x, y, x0: x, y0: y, born: e.t, land: e.t + 90, end: e.t + 2400, size: 2.7 + 1.2 * v,
          rot: r () * TAU, vr: (r () - 0.5) * 0.5, vx: (r () - 0.5) * 2, col: e.colour, deep: e.deep, hi, claims: 0, bites: 0, ang: 0, eaten: 0, gone: 0 };
        items.push (it);
        ring (x, y, e.t + 90, 1350, 3, 14 + 7 * v, hi, e.deep, 1.15, 0.5, false);
        ring (x, y, e.t + 300, 1100, 2, 8 + 4 * v, hi, e.deep, 0.9, 0.34, false);
        // the nearest fish darts in to nibble it; the next one comes for a curious look, then drifts off
        const [a, b2] = nearest (x, y, 2, freeFor (x, y));
        if (a) sendTo (a, it); if (b2) sendTo (b2, it, false, true);
      } else if (b < 0.72) {
        // snare / perc: a pinch of food scatters; fish gulp the pellets one by one
        const n = b < 0.6 ? 3 : 2, list = [];
        for (let k = 0; k < n; k++) {
          const a = (k / n) * TAU + r () * 1.2, d = 3.2 + r () * 2.6;
          const it = { kind: PELLET, x: clamp (x + Math.cos (a) * d * 1.3, 8, W - 8), y: clamp (y + Math.sin (a) * d, 8, H - 8), x0: x, y0: y,
            born: e.t, land: e.t + 60 + k * 38, end: e.t + 1500, size: 0.85 + 0.3 * v, col: e.colour, deep: e.deep, hi, claims: 0, bites: 0, ang: 0, eaten: 0, gone: 0 };
          items.push (it); list.push (it);
          ring (it.x, it.y, it.land, 360, 0.8, 3.6 + 1.4 * v, hi, e.deep, 0.6, 0.42, false);
        }
        const hunters = nearest (x, y, b < 0.6 ? 2 : 1, freeFor (x, y));
        for (const f of hunters) {
          let best = null, bd = 1e9;
          for (const it of list) { const d = Math.hypot (it.x - f.x, it.y - f.y) + it.claims * 40; if (d < bd) { bd = d; best = it; } }
          if (best) sendTo (f, best);
        }
      } else {
        // hats: a glint of light on the water; the fish mostly ignore it, the nearest one glances
        // (a closed hat: one glint and a tiny echo; an open hat: a longer glint with two echoes and a faint ring)
        const open = b < 0.85, n = open ? 3 : 2, gx = x + (r () - 0.5) * 6, gy = clamp (y + (r () - 0.5) * 10, 8, H - 8);
        for (let k = 0; k < n; k++) {
          const a = r () * TAU, d = k ? 3.2 + r () * 1.5 : 0, life = (open ? 600 : 320) * (k ? 0.75 : 1);
          items.push ({ kind: GLINT, x: gx + Math.cos (a) * d * 1.3, y: clamp (gy + Math.sin (a) * d, 5, H - 5), born: e.t + k * 50,
            end: e.t + k * 50 + life, size: (2.3 + 1.1 * v) * (k ? 0.5 : 1) * (open ? 1.12 : 1), rot: r () * 0.5 - 0.25,
            col: e.colour, deep: e.deep, hi, claims: 0, gone: 0 });
        }
        if (open) ring (gx, gy, e.t, 560, 1, 6.5, hi, e.deep, 0.7, 0.32, false);
        const [f] = nearest (gx, gy, 1, g => g.state === CRUISE);
        if (f && Math.hypot (f.x - gx, f.y - gy) < 45) { f.glance = 1; f.ga = Math.atan2 (gy - f.y, gx - f.x); f.flick = Math.max (f.flick, 0.3); }
      }
    }
    function undrop (e, x, y, r) {
      // reversed: the drop runs backwards — rings close in on the spot, the thing lifts off the water,
      // and every fish nearby scatters away from it
      const v = e.velocity, hi = util.mix (e.colour, '#ffffff', 0.5), b = e.brightness;
      const dur = 640;
      ring (x, y, e.t, dur, 2, 13 + 5 * v, hi, e.deep, 1.0, 0.5, true);
      ring (x, y, e.t - 160, dur, 2, 8 + 3 * v, hi, e.deep, 0.8, 0.34, true);
      // the things ride the closing ring in, like beads on a string, and lift off where it closes
      const n = b < 0.3 ? 1 : b < 0.72 ? 3 : 2;
      for (let k = 0; k < n; k++) {
        const a = (k / n) * TAU + r () * 0.8;
        items.push ({ kind: b < 0.3 ? PETAL : b < 0.72 ? PELLET : GLINT, rev: true, x, y, x0: Math.cos (a), y0: Math.sin (a),
          r0: n > 1 ? 1.2 : 0, r1: n > 1 ? (13 + 5 * v) * 0.8 : 0,
          born: e.t, land: e.t + dur, end: e.t + dur + 170, size: b < 0.3 ? 2.7 + v : b < 0.72 ? 1.0 + 0.3 * v : 2.2, rot: r () * TAU, vr: 0, vx: 0,
          col: e.colour, deep: e.deep, hi, claims: 0, eaten: 0, gone: 0 });
      }
      for (const f of fish) {
        let dx = f.x - x, dy = f.y - y; const d = Math.hypot (dx, dy);
        if (d > 90) continue;
        if (d < 1) { dx = Math.cos (f.a); dy = Math.sin (f.a); } else { dx /= d; dy /= d; }
        const push = 34 + (90 - d) * 0.45;
        if (f.food) { f.food.claims--; f.food = null; }
        // (each fish keeps its own lane and its own stop near a bank, so they scatter instead of piling up)
        const lo = 22 + f.i * 7, hi = W - 22 - f.i * 7;
        f.gx = clamp (f.x + dx * push, lo, hi);
        if (Math.abs (f.gx - f.x) < 14) f.gx = clamp (f.x + (f.x > x ? 1 : -1) * 30, lo, hi);
        if (Math.abs (f.gx - f.x) < 14) f.gx = clamp (f.x - (f.x > x ? 1 : -1) * 30, lo, hi);
        f.gy = clamp (f.y + dy * push * 0.5, 10, H - 10) * 0.5 + (10 + f.i / Math.max (1, count - 1) * (H - 20)) * 0.5;
        f.state = FLEE; f.timer = 0; f.flick = 1;
      }
    }

    // ---- the simulation --------------------------------------------------------------------------------------------
    function stepFish (f, dt) {
      let gx, gy, vd, turnMax, gain, wt;
      const fast = f.state === DART || f.state === FLEE;
      if (f.state === CRUISE) {
        if (Math.abs (f.gx - f.x) < 6) wander (f);
        gx = f.gx; gy = f.gy;
        // cruising fish stay level: never steeper than about 27 degrees
        const ax = Math.abs (gx - f.x); if (Math.abs (gy - f.y) * 2 > ax) gy = f.y + Math.sign (gy - f.y) * ax * 0.5;
        // a lazy glide, a little quicker when far from home
        vd = f.vc + Math.min (20, Math.max (0, Math.abs (f.x - f.home) - W / count * 0.5) * 0.3);
        turnMax = (0.75 + f.v * 0.1) * (Math.abs (wrap (Math.atan2 (gy - f.y, gx - f.x) - f.a)) > 1.2 ? 1.6 : 1); gain = 1.6 + f.v * 0.12; wt = f.v > 12 ? 0.12 : 0.35;
      } else if (f.state === DART) {
        const it = f.food;
        if (! it || it.eaten || it.gone) { toCruise (f); return stepFish (f, dt); }
        gx = it.x + f.ox; gy = clamp (it.y + f.oy, 8, H - 8);
        const d = Math.hypot (gx - f.x, gy - f.y);
        if (f.follow && d < 4) { f.lastFood = it; toCruise (f); return stepFish (f, dt); }   // just had a look
        if (d < 2.4) { f.state = NIBBLE; f.timer = 0; }
        vd = clamp (Math.sqrt (d) * 26, 6, f.calm ? 40 : f.follow ? 70 : 160);   // brake late, glide in
        turnMax = f.calm ? 8 : 22; gain = 18; wt = 0.03;
      } else if (f.state === FLEE) {
        f.timer += dt;
        const d = Math.hypot (f.gx - f.x, f.gy - f.y);
        if (d < 6 || f.timer > 1.4) { toCruise (f); return stepFish (f, dt); }
        gx = f.gx; gy = f.gy; vd = clamp (d * 3.6, 9, 130); turnMax = 12; gain = 14; wt = 0.045;
      } else {
        // NIBBLE: hold the mouth at the food, little bites
        const it = f.food;
        f.timer += dt;
        if (it && ! it.gone) {
          f.x += (it.x + f.ox * 0.5 - f.x) * ex (dt, 0.12); f.y += (it.y + f.oy * 0.5 - f.y) * ex (dt, 0.12);
          // face the food, but stay fairly level
          const want = Math.atan2 (-f.oy * 0.3, -f.ox);
          f.a = wrap (f.a + wrap (want - f.a) * ex (dt, 0.25));
        }
        f.v += (0 - f.v) * ex (dt, 0.09);
        f.bob = f.timer < 0.5 ? Math.sin (f.timer * TAU * 6.5) * (1 - f.timer / 0.5) : 0;
        const done = it && it.kind === PELLET ? 0.22 : 0.7;
        if (f.timer > done) {
          if (it) {
            it.claims--;
            if (it.kind === PELLET && ! it.eaten) { it.eaten = 1; ring (it.x, it.y, last, 300, 0.8, 4, it.hi, it.deep, 0.7, 0.5, false); }
            else if (it.kind === PETAL) { it.bites++; it.size *= 0.86; ring (it.x + f.ox, it.y + f.oy, last, 260, 0.6, 3, it.hi, it.deep, 0.6, 0.4, false); }
          }
          f.lastFood = it; f.food = null;
          // another bite close by? go on eating
          const next = hungry (f, 34);
          if (next) { sendTo (f, next, true); f.flick = 0.5; } else toCruise (f);
        }
        tail (f, dt, 0); moveSpine (f); return;
      }
      // where to head: the goal, pushed away from the walls and from the other fish
      let dx = gx - f.x, dy = gy - f.y; const dl = Math.hypot (dx, dy) || 1; dx /= dl; dy /= dl;
      // the other fish: keep a little room (capped, so it never outweighs the goal)
      let sx = 0, sy = 0;
      for (const o of fish) {
        if (o === f) continue;
        for (let j = 0; j < N; j += 2) {
          const ox = f.x - o.px[j], oy = f.y - o.py[j], d = Math.hypot (ox, oy);
          if (d < 14 && d > 0.01) { const k = (14 - d) / 14; sx += ox / d * k; sy += oy / d * k; }
        }
      }
      const sl = Math.hypot (sx, sy);
      if (sl > 0.001) { const m = Math.min (sl, 1) * (fast ? 0.3 : 0.8) / sl; dx += sx * m; dy += sy * m; }
      // the banks: steer back in, by where the fish is and where it is heading
      const lx = f.x + Math.cos (f.a) * 8, ly = f.y + Math.sin (f.a) * 8, wall = fast ? 0.8 * Math.min (1, dl / 25) : 1, m = 9;
      if (ly < m) dy += (m - ly) / m * 1.6 * wall; if (ly > H - m) dy -= (ly - H + m) / m * 1.6 * wall;
      if (f.y < m) dy += (m - f.y) / m * 1.5 * wall; if (f.y > H - m) dy -= (f.y - H + m) / m * 1.5 * wall;
      if (lx < 10) dx += (10 - lx) / 10 * 1.6 * wall; if (lx > W - 10) dx -= (lx - W + 10) / 10 * 1.6 * wall;
      if (f.glance > 0.02) { dx += Math.cos (f.ga) * f.glance * 0.5; dy += Math.sin (f.ga) * f.glance * 0.1; }
      const want = Math.atan2 (dy, dx);
      let diff = wrap (want - f.a);
      // turning right round: go by the side with more water
      if (Math.abs (diff) > 2.4) diff = Math.abs (diff) * (f.y < H / 2 ? 1 : -1) * (Math.cos (f.a) > 0 ? 1 : -1);
      const align = Math.cos (diff);
      vd *= fast ? clamp (0.3 + 0.7 * align, 0.22, 1) : clamp (0.55 + 0.45 * align, 0.35, 1);
      f.w += (clamp (diff * gain, -turnMax, turnMax) - f.w) * ex (dt, wt);
      f.a = wrap (f.a + f.w * dt);
      const v0 = f.v;
      f.v += (vd - f.v) * ex (dt, vd > f.v ? (fast ? 0.06 : 0.9) : (fast ? 0.17 : 0.42));
      tail (f, dt, (f.v - v0) / dt);
      f.x = clamp (f.x + Math.cos (f.a) * f.v * dt, 3, W - 3);
      f.y = clamp (f.y + Math.sin (f.a) * f.v * dt, 4.5, H - 4.5);
      f.bob *= 1 - ex (dt, 0.08);
      moveSpine (f);
    }
    function toCruise (f) {
      if (f.food) { f.food.claims--; f.food = null; }
      f.state = CRUISE; f.timer = 0;
      homes ();
      // still something to eat nearby (say, after a scare)? go back for it, a little calmer
      const next = hungry (f, 70);
      if (next) sendTo (f, next, true); else wander (f, true);
    }
    function tail (f, dt, accel) {
      f.flick *= 1 - ex (dt, 0.22);
      f.glance *= 1 - ex (dt, 0.35);
      const freq = 0.55 + f.v * 0.042 + f.flick * 4.5;
      let at = 0.42 + Math.min (1.2, f.v * 0.013) + f.flick * 1.5 + Math.min (0.5, Math.abs (f.w) * 0.12);
      if (accel < 0) at -= Math.min (0.35, -accel * 0.004);      // gliding: the tail rests
      f.amp += (at - f.amp) * ex (dt, at > f.amp ? 0.06 : 0.35);
      f.ph += TAU * freq * dt;
    }
    function follow (xs, ys, i, seg, bx, by) {
      // point i trails point i-1 at distance seg; (bx, by) is the direction of the segment before
      let dx = xs[i] - xs[i - 1], dy = ys[i] - ys[i - 1];
      const l = Math.hypot (dx, dy) || 1e-6; dx /= l; dy /= l;
      const sn = bx * dy - by * dx, cs = bx * dx + by * dy, ang = Math.atan2 (sn, cs);
      if (ang > MAXB || ang < -MAXB) {
        const aa = ang > 0 ? MAXB : -MAXB, c = Math.cos (aa), s = Math.sin (aa);
        dx = bx * c - by * s; dy = bx * s + by * c;
      }
      xs[i] = xs[i - 1] + dx * seg; ys[i] = ys[i - 1] + dy * seg;
    }
    function moveSpine (f) {
      const { px, py, qx, qy, seg } = f, ca = Math.cos (f.a), sa = Math.sin (f.a);
      px[0] = f.x; py[0] = f.y; px[1] = f.x - ca * seg; py[1] = f.y - sa * seg;
      for (let i = 2; i < N; i++) {
        let bx = px[i - 1] - px[i - 2], by = py[i - 1] - py[i - 2]; const bl = Math.hypot (bx, by) || 1e-6;
        follow (px, py, i, seg, bx / bl, by / bl);
      }
      qx[0] = px[N - 1]; qy[0] = py[N - 1];
      const ts = f.L * TAILF * 0.5;
      let bx = px[N - 1] - px[N - 2], by = py[N - 1] - py[N - 2], bl = Math.hypot (bx, by) || 1e-6;
      follow (qx, qy, 1, ts, bx / bl, by / bl);
      bx = qx[1] - qx[0]; by = qy[1] - qy[0]; bl = Math.hypot (bx, by) || 1e-6;
      follow (qx, qy, 2, ts, bx / bl, by / bl);
    }
    function stepItems (dt, t) {
      for (let i = items.length - 1; i >= 0; i--) {
        const it = items[i];
        let remove = it.eaten;
        if (! remove && t >= it.end) {
          if (it.kind !== GLINT && ! it.rev && ! it.gone) { it.gone = t; it.end = t + 420; }   // uneaten: sinks away
          else remove = true;
        }
        if (remove) { items.splice (i, 1); for (const f of fish) if (f.food === it) toCruise (f); continue; }
        if (it.kind === PETAL && ! it.rev && t > it.land) { it.rot += it.vr * dt; it.x = clamp (it.x + it.vx * dt, 8, W - 8); }
      }
      for (let i = rings.length - 1; i >= 0; i--) if (t > rings[i].born + rings[i].dur) rings.splice (i, 1);
    }
    function busy (t) {
      if (items.length || rings.length || t - lastHit < 2500) return true;
      for (const f of fish) if (f.state !== CRUISE || f.flick > 0.02 || f.v > f.vc * 1.6) return true;
      return false;
    }
    function step (dt, t) {
      for (const f of fish) {
        stepFish (f, dt);
        // depth: up to the surface to eat, down to the bottom when scared, in between when cruising
        const d = f.state === DART || f.state === NIBBLE ? 0 : f.state === FLEE ? 1 : f.dbase;
        f.depth += (d - f.depth) * ex (dt, f.state === CRUISE ? 1.4 : f.state === FLEE ? 0.22 : 0.3);
      }
      stepItems (dt, t);
    }
    // warm up: let the fish swim a while, so the first picture already has natural curves
    for (let k = 0; k < 90; k++) step (1 / 20, -1e6);

    // ---- drawing -------------------------------------------------------------------------------------------------
    const LX = new Float64Array (24), LY = new Float64Array (24);
    let SX = 0, SY = 0, SNX = 0, SNY = 0;
    function crLoop (ctx, n, ox, oy) {
      // closed Catmull-Rom spline through (LX, LY)[0..n), as cubic beziers
      ctx.moveTo (LX[0] + ox, LY[0] + oy);
      for (let i = 0; i < n; i++) {
        const a = (i + n - 1) % n, b = (i + 1) % n, c = (i + 2) % n;
        ctx.bezierCurveTo (LX[i] + (LX[b] - LX[a]) / 6 + ox, LY[i] + (LY[b] - LY[a]) / 6 + oy,
          LX[b] - (LX[c] - LX[i]) / 6 + ox, LY[b] - (LY[c] - LY[i]) / 6 + oy, LX[b] + ox, LY[b] + oy);
      }
      ctx.closePath ();
    }
    function pose (f) {
      const { px, py, rx, ry, nx, ny, qx, qy, tx, ty, tnx, tny } = f;
      const bx = Math.cos (f.a) * f.bob * 0.45, by = Math.sin (f.a) * f.bob * 0.45;
      for (let i = 0; i < N; i++) {
        const a = i === 0 ? 0 : i - 1, b = i === N - 1 ? N - 1 : i + 1;
        let fx = px[a] - px[b], fy = py[a] - py[b]; const l = Math.hypot (fx, fy) || 1; fx /= l; fy /= l;
        const s = i / (N - 1), lat = f.amp * (0.1 + 0.9 * s * s) * Math.sin (f.ph - s * K);
        rx[i] = px[i] - fy * lat + bx; ry[i] = py[i] + fx * lat + by;
      }
      for (let j = 0; j < 3; j++) {
        const a = j === 0 ? 0 : j - 1, b = j === 2 ? 2 : j + 1;
        let fx = qx[a] - qx[b], fy = qy[a] - qy[b]; const l = Math.hypot (fx, fy) || 1; fx /= l; fy /= l;
        if (j === 0) { fx = px[N - 2] - qx[1]; fy = py[N - 2] - qy[1]; const l2 = Math.hypot (fx, fy) || 1; fx /= l2; fy /= l2; }
        const s = 1 + j * TAILF * 0.5, lat = f.amp * (0.1 + 0.9 * s * s) * Math.sin (f.ph - s * K - j * 0.35);
        tx[j] = qx[j] - fy * lat + bx; ty[j] = qy[j] + fx * lat + by;
      }
      tx[0] = rx[N - 1]; ty[0] = ry[N - 1];
      for (let i = 0; i < N; i++) {
        const a = i === 0 ? 0 : i - 1, b = i === N - 1 ? N - 1 : i + 1;
        let fx = rx[a] - rx[b], fy = ry[a] - ry[b]; const l = Math.hypot (fx, fy) || 1;
        nx[i] = -fy / l; ny[i] = fx / l;
      }
      for (let j = 0; j < 3; j++) {
        const a = j === 0 ? 0 : j - 1, b = j === 2 ? 2 : j + 1;
        let fx = tx[a] - tx[b], fy = ty[a] - ty[b]; const l = Math.hypot (fx, fy) || 1;
        tnx[j] = -fy / l; tny[j] = fx / l;
      }
    }
    function at (f, s) {
      const { rx, ry, nx, ny } = f;
      if (s <= 0) {
        let fx = rx[0] - rx[1], fy = ry[0] - ry[1]; const l = Math.hypot (fx, fy) || 1;
        SX = rx[0] + fx / l * (-s) * f.L; SY = ry[0] + fy / l * (-s) * f.L; SNX = nx[0]; SNY = ny[0]; return;
      }
      const q = s * (N - 1); let i = q | 0; if (i > N - 2) i = N - 2; const u = q - i;
      SX = rx[i] + (rx[i + 1] - rx[i]) * u; SY = ry[i] + (ry[i + 1] - ry[i]) * u;
      let mx = nx[i] + (nx[i + 1] - nx[i]) * u, my = ny[i] + (ny[i + 1] - ny[i]) * u; const l = Math.hypot (mx, my) || 1;
      SNX = mx / l; SNY = my / l;
    }
    function bodyPath (ctx, f, ox, oy, wf) {
      // nose, then down the left side, then back up the right side
      at (f, PS[0]); LX[0] = SX; LY[0] = SY;
      for (let k = 1; k < 9; k++) {
        at (f, PS[k]); const hw = PW[k] * f.L * wf;
        LX[k] = SX + SNX * hw; LY[k] = SY + SNY * hw;
        LX[17 - k] = SX - SNX * hw; LY[17 - k] = SY - SNY * hw;
      }
      crLoop (ctx, 17, ox, oy);
    }
    function subPath (ctx, f, s0, s1, wf, off, ox, oy) {
      // a patch inside the body between s0 and s1, its width a fraction wf, shifted sideways by off
      const M = 4;
      at (f, s0); let o = off * prof (s0) * f.L; LX[0] = SX + SNX * o; LY[0] = SY + SNY * o;
      at (f, s1); o = off * prof (s1) * f.L; LX[M + 1] = SX + SNX * o; LY[M + 1] = SY + SNY * o;
      for (let j = 1; j <= M; j++) {
        const u = j / (M + 1), s = s0 + (s1 - s0) * u; at (f, s);
        const p = prof (s) * f.L, hw = p * wf * Math.sqrt (Math.sin (PI * u)), c = off * p;
        LX[j] = SX + SNX * (c + hw); LY[j] = SY + SNY * (c + hw);
        LX[2 * M + 2 - j] = SX + SNX * (c - hw); LY[2 * M + 2 - j] = SY + SNY * (c - hw);
      }
      crLoop (ctx, 2 * M + 2, ox, oy);
    }
    function tailPath (ctx, f, ox, oy) {
      const { tx, ty, tnx, tny, L } = f, hp = 0.045 * L, sp = 0.17 * L;
      let dx = tx[2] - tx[1], dy = ty[2] - ty[1]; const dl = Math.hypot (dx, dy) || 1; dx /= dl; dy /= dl;
      // a butterfly fan: two soft lobes and a shallow notch
      const e = 0.12 * L, b = 0.03 * L;
      LX[0] = tx[0] + tnx[0] * hp; LY[0] = ty[0] + tny[0] * hp;
      LX[1] = tx[1] + tnx[1] * sp * 0.55; LY[1] = ty[1] + tny[1] * sp * 0.55;
      LX[2] = tx[2] + tnx[2] * sp - dx * b; LY[2] = ty[2] + tny[2] * sp - dy * b;
      LX[3] = tx[2] + tnx[2] * sp * 0.5 + dx * e; LY[3] = ty[2] + tny[2] * sp * 0.5 + dy * e;
      LX[4] = tx[2] + dx * e * 0.15; LY[4] = ty[2] + dy * e * 0.15;
      LX[5] = tx[2] - tnx[2] * sp * 0.5 + dx * e; LY[5] = ty[2] - tny[2] * sp * 0.5 + dy * e;
      LX[6] = tx[2] - tnx[2] * sp - dx * b; LY[6] = ty[2] - tny[2] * sp - dy * b;
      LX[7] = tx[1] - tnx[1] * sp * 0.55; LY[7] = ty[1] - tny[1] * sp * 0.55;
      LX[8] = tx[0] - tnx[0] * hp; LY[8] = ty[0] - tny[0] * hp;
      crLoop (ctx, 9, ox, oy);
    }
    function finPath (ctx, f) {
      at (f, 0.2);
      const cx = SX, cy = SY, nx = SNX, ny = SNY, fx = ny, fy = -nx;   // forward = normal turned back a quarter
      const len = 0.27 * f.L, p = prof (0.2) * f.L * 0.8;
      for (let side = -1; side <= 1; side += 2) {
        const beta = 0.8 + 0.18 * Math.sin (f.ph * 0.5 + side) + Math.min (0.5, f.flick * 0.4);
        const dx = -fx * Math.cos (beta) + nx * side * Math.sin (beta), dy = -fy * Math.cos (beta) + ny * side * Math.sin (beta);
        const bx = cx + nx * side * p, by = cy + ny * side * p;
        ctx.moveTo (bx + dx * len, by + dy * len);
        ctx.ellipse (bx + dx * len * 0.5, by + dy * len * 0.5, len * 0.5, len * 0.2, Math.atan2 (dy, dx), 0, TAU);
      }
    }
    function drawFish (ctx, f) {
      const c = f.lv[Math.round (clamp (f.depth, 0, 1) * (LV - 1))];
      ctx.fillStyle = c.fin; ctx.beginPath (); tailPath (ctx, f, 0, 0); finPath (ctx, f); ctx.fill ();
      ctx.fillStyle = c.edge; ctx.beginPath (); bodyPath (ctx, f, 0, 0, 1); ctx.fill ();
      ctx.fillStyle = c.main; ctx.beginPath (); subPath (ctx, f, -0.06, 0.97, 0.8, 0.12, -0.12, -0.28); ctx.fill ();
      if (f.kind.patches) {
        ctx.fillStyle = c.spot; ctx.beginPath ();
        for (const [s0, s1, wf, off] of f.kind.patches) subPath (ctx, f, s0, s1, wf, off, 0, 0);
        ctx.fill ();
      }
      if (f.kind.crown) {
        at (f, 0.11); ctx.fillStyle = c.spot; ctx.beginPath (); ctx.arc (SX, SY, prof (0.11) * f.L * 0.62, 0, TAU); ctx.fill ();
      }
      if (f.kind.gloss) { ctx.fillStyle = c.hi; ctx.globalAlpha = 0.7; ctx.beginPath (); subPath (ctx, f, 0.02, 0.6, 0.34, 0.3, -0.25, -0.4); ctx.fill ();
      ctx.globalAlpha = 1; }
      at (f, 0.035); const p = prof (0.035) * f.L * 0.74, er = 0.36 * f.L / 13;
      ctx.fillStyle = c.eye; ctx.beginPath ();
      ctx.moveTo (SX + SNX * p + er, SY + SNY * p); ctx.arc (SX + SNX * p, SY + SNY * p, er, 0, TAU);
      ctx.moveTo (SX - SNX * p + er, SY - SNY * p); ctx.arc (SX - SNX * p, SY - SNY * p, er, 0, TAU);
      ctx.fill ();
    }
    function petalPath (ctx, s) {
      ctx.moveTo (-s, 0);
      ctx.bezierCurveTo (-s * 0.45, -s * 0.78, s * 0.5, -s * 0.9, s, -s * 0.3);
      ctx.quadraticCurveTo (s * 0.7, 0, s, s * 0.3);
      ctx.bezierCurveTo (s * 0.5, s * 0.9, -s * 0.45, s * 0.78, -s, 0);
      ctx.closePath ();
    }
    function starPath (ctx, x, y, r, rot) {
      const k = r * 0.16;
      for (let i = 0; i < 4; i++) {
        const a = rot + i * PI / 2, b = a + PI / 2, m = a + PI / 4;
        if (i === 0) ctx.moveTo (x + Math.cos (a) * r, y + Math.sin (a) * r);
        ctx.quadraticCurveTo (x + Math.cos (m) * k, y + Math.sin (m) * k, x + Math.cos (b) * r, y + Math.sin (b) * r);
      }
      ctx.closePath ();
    }
    const easeOut3 = u => 1 - (1 - u) * (1 - u) * (1 - u);
    function drawRings (ctx, t) {
      for (const g of rings) {
        let u = (t - g.born) / g.dur; if (u < 0 || u >= 1) continue;
        if (g.rev) u = 1 - u;                       // a reversed ring is the same ring, played backwards
        const r = g.r0 + (g.r1 - g.r0) * easeOut3 (u);
        const a = g.peak * Math.pow (1 - u, 1.5) * (g.rev ? 1 : Math.min (1, u * 14));
        const lw = g.lw * (1 - 0.45 * u);
        ctx.lineWidth = lw;
        ctx.globalAlpha = a; ctx.strokeStyle = g.trough;
        ctx.beginPath (); ctx.arc (g.x, g.y, r, 0, TAU); ctx.stroke ();
        if (r > lw * 1.2) {
          ctx.globalAlpha = a * (P.n ? 0.9 : 1); ctx.strokeStyle = g.crest;
          ctx.beginPath (); ctx.arc (g.x, g.y, r - lw * 0.95, 0, TAU); ctx.stroke ();
        }
      }
      ctx.globalAlpha = 1;
    }
    function drawItems (ctx, t) {
      for (const it of items) {
        if (t < it.born) continue;
        let x = it.x, y = it.y, sc = 1, al = 1;
        if (it.rev) {
          // ride the closing ring in, then lift off the water (grow and fade, as if rising toward us)
          const u = clamp ((t - it.born) / (it.land - it.born), 0, 1), rr = it.r0 + (it.r1 - it.r0) * easeOut3 (1 - u);
          x = it.x + it.x0 * rr; y = it.y + it.y0 * rr * 0.9; al = Math.min (1, u * 2.5);
          if (t > it.land) { const v = (t - it.land) / (it.end - it.land); sc = 1 + v * 1.1; al = 1 - v * v; }
        } else if (t < it.land) {
          const u = (t - it.born) / (it.land - it.born), e = easeOut3 (u);
          x = it.x0 + (it.x - it.x0) * e; y = it.y0 + (it.y - it.y0) * e; sc = 1.7 - 0.7 * u; al = 0.35 + 0.65 * u;
        }
        if (it.gone) { const v = clamp ((t - it.gone) / (it.end - it.gone), 0, 1); sc *= 1 - 0.35 * v; al *= 1 - v; }
        if (it.eaten) continue;
        if (al <= 0.01) continue;
        if (it.kind === PETAL) {
          let jig = 0;
          for (const f of fish) if (f.food === it && f.state === NIBBLE) jig += f.bob * 0.35;
          ctx.save (); ctx.translate (x + jig, y); ctx.rotate (it.rot + jig * 0.2); ctx.scale (sc, sc);
          ctx.globalAlpha = al * (P.n ? 0.4 : 0.14); ctx.fillStyle = P.n ? '#0a0705' : '#3b2a24';
          ctx.beginPath (); ctx.translate (0.5, 0.9); petalPath (ctx, it.size); ctx.fill (); ctx.translate (-0.5, -0.9);
          ctx.globalAlpha = al; ctx.fillStyle = it.col; ctx.beginPath (); petalPath (ctx, it.size); ctx.fill ();
          ctx.fillStyle = it.hi; ctx.globalAlpha = al * 0.75; ctx.beginPath (); ctx.translate (it.size * 0.15, -it.size * 0.12); petalPath (ctx, it.size * 0.55); ctx.fill ();
          ctx.restore ();
        } else if (it.kind === PELLET) {
          const r = it.size * sc;
          ctx.globalAlpha = al * (P.n ? 0.45 : 0.16); ctx.fillStyle = P.n ? '#0a0705' : '#3b2a24';
          ctx.beginPath (); ctx.arc (x + 0.4, y + 0.7, r, 0, TAU); ctx.fill ();
          ctx.globalAlpha = al; ctx.fillStyle = it.deep; ctx.beginPath (); ctx.arc (x, y, r, 0, TAU); ctx.fill ();
          ctx.fillStyle = it.hi; ctx.beginPath (); ctx.arc (x - r * 0.3, y - r * 0.32, r * 0.42, 0, TAU); ctx.fill ();
        } else {
          const u = clamp ((t - it.born) / (it.end - it.born), 0, 1);
          // a twinkle: pops open in a few frames, then closes slowly while turning a little
          const k = it.rev ? sc * (1 - u * 0.2) : (u < 0.12 ? easeOut3 (u / 0.12) : Math.pow ((1 - u) / 0.88, 1.3));
          const r = it.size * (0.35 + 0.65 * k);
          if (r < 0.3) continue;
          ctx.globalAlpha = al * Math.min (1, k * 1.4) * 0.95; ctx.fillStyle = P.n ? it.col : it.deep;
          ctx.beginPath (); starPath (ctx, x, y, r, it.rot + u * 0.6); ctx.fill ();
          ctx.globalAlpha = al * Math.min (1, k * 1.6); ctx.fillStyle = '#ffffff';
          ctx.beginPath (); starPath (ctx, x, y, r * 0.52, it.rot + u * 0.6); ctx.fill ();
        }
      }
      ctx.globalAlpha = 1;
    }

    // lily pads at the two ends (floating above the fish), painted once into an image
    const padCanvas = document.createElement ('canvas');
    padCanvas.width = Math.ceil (W * dpr); padCanvas.height = Math.ceil (H * dpr);
    const PADS = [
      { x: 2.5, y: 4.5, r: 10, notch: 0.75 },
      { x: 15, y: 31.5, r: 5.4, notch: -1.75 },
      { x: W - 3.5, y: 27, r: 10.5, notch: 3.75, lotus: true },
      { x: W - 21, y: 3, r: 5, notch: 2.35 },
    ];
    function padShape (c, p, ox, oy, r) {
      const half = 0.17;
      c.moveTo (p.x + ox, p.y + oy);
      c.arc (p.x + ox, p.y + oy, r, p.notch + half, p.notch - half + TAU);
      c.closePath ();
    }
    function paintPads () {
      const c = padCanvas.getContext ('2d');
      c.setTransform (1, 0, 0, 1, 0, 0); c.clearRect (0, 0, padCanvas.width, padCanvas.height);
      c.setTransform (dpr, 0, 0, dpr, 0, 0);
      for (const p of PADS) { c.fillStyle = P.padShadow; c.beginPath (); padShape (c, p, 0.9, 1.6, p.r); c.fill (); }
      for (const p of PADS) {
        c.fillStyle = P.padEdge; c.beginPath (); padShape (c, p, 0, 0, p.r); c.fill ();
        c.fillStyle = P.pad; c.beginPath (); padShape (c, p, -0.2, -0.3, p.r - 0.75); c.fill ();
        c.strokeStyle = P.vein; c.lineWidth = 0.45; c.globalAlpha = 0.55; c.beginPath ();
        for (let k = 0; k < 9; k++) {
          const a = p.notch + 0.5 + k * (TAU - 1.0) / 8;
          c.moveTo (p.x + Math.cos (a) * p.r * 0.1, p.y + Math.sin (a) * p.r * 0.1);
          c.lineTo (p.x + Math.cos (a) * p.r * 0.8, p.y + Math.sin (a) * p.r * 0.8);
        }
        c.stroke ();
        c.strokeStyle = P.padHi; c.lineWidth = 0.7; c.globalAlpha = 0.9; c.beginPath ();
        c.arc (p.x - 0.2, p.y - 0.3, p.r - 1.5, PI * 0.95, PI * 1.55); c.stroke ();
        c.globalAlpha = 1;
        if (p.lotus) {
          const lx = p.x - p.r * 0.42, ly = p.y - p.r * 0.38;
          c.fillStyle = P.padShadow; c.beginPath (); c.arc (lx + 0.6, ly + 1.1, 2.9, 0, TAU); c.fill ();
          for (let k = 0; k < 6; k++) {
            const a = k * TAU / 6 + 0.3; c.fillStyle = P.lotus; c.beginPath ();
            c.ellipse (lx + Math.cos (a) * 1.55, ly + Math.sin (a) * 1.55, 1.85, 1.0, a, 0, TAU); c.fill ();
          }
          for (let k = 0; k < 5; k++) {
            const a = k * TAU / 5 + 0.9; c.fillStyle = P.lotusIn; c.beginPath ();
            c.ellipse (lx + Math.cos (a) * 0.85, ly + Math.sin (a) * 0.85, 1.15, 0.68, a, 0, TAU); c.fill ();
          }
          c.fillStyle = P.lotusC; c.beginPath (); c.arc (lx, ly, 0.7, 0, TAU); c.fill ();
        }
      }
    }
    palette ();

    return {
      setTheme (t) { T = t; palette (); },
      hit (e) {
        const r = util.rand ((((e.t * 13) | 0) ^ (e.slice * 7919)) + 11);
        const x = PADX + e.x * (W - 2 * PADX), y = H * 0.5 + (r () - 0.5) * 9;
        lastHit = e.t;
        if (e.reversed) undrop (e, x, y, r); else drop (e, x, y, r);
      },
      draw (ctx, t) {
        if (last === null) last = t;
        let dt = (t - last) / 1000; last = t;
        if (dt > 0.1) dt = 0.1; if (dt < 0) dt = 0;
        if (busy (t)) {
          acc = 0;
          while (dt > 1e-6) { const d = Math.min (dt, 1 / 60); step (d, t); dt -= d; }
        } else {
          // idle: a slow glide, stepped at 20 fps
          acc += dt;
          if (acc >= 0.05) { step (acc, t); acc = 0; }
        }
        for (const f of fish) pose (f);
        // deepest fish first, the ones up at the surface last; each casts its hard little shadow on the floor (and on
        // any fish below it) and a deep fish's colours are veiled by the water over it (see palette)
        for (let i = 1; i < count; i++) {
          const f = layer[i]; let j = i - 1;
          while (j >= 0 && layer[j].depth < f.depth) { layer[j + 1] = layer[j]; j--; }
          layer[j + 1] = f;
        }
        for (const f of layer) {
          const k = 1 - f.depth, sx = 0.55 + 0.95 * k, sy = 1.0 + 1.7 * k;
          ctx.fillStyle = P.shadow; ctx.beginPath (); bodyPath (ctx, f, sx, sy, 1); tailPath (ctx, f, sx, sy); ctx.fill ();
          drawFish (ctx, f);
        }
        drawRings (ctx, t);
        drawItems (ctx, t);
        ctx.drawImage (padCanvas, 0, 0, W, H);
        return true;   // the fish always glide; see isIdle for the frame rate
      },
      // true when only the lazy glide is left: the host may then repaint at 20 fps (the physics steps at 20 fps anyway)
      isIdle () { return last !== null && ! busy (last); },
    };
  },
});


// --- the site's visualizer board: the four looks side by side, a silent beat playing into them --------------------
// (one board per page; the preview holds two). The beat runs by itself; pause and reverse sit under the looks.
document.querySelectorAll('[data-pond]').forEach(root => {
  const night = () => document.documentElement.dataset.theme === 'night';
  const stages = [];
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let reversed = false, beatOn = !still, beatStart = 0, beatNext = 0, seen = false, running = false;

  for (const box of root.querySelectorAll('[data-pond-look]')) {
    const concept = PONDS.find(p => p.id === box.dataset.pondLook);
    if (!concept) continue;
    const cv = document.createElement('canvas');
    box.appendChild(cv);
    const zoom = Math.max(1.4, Math.min(4, box.clientWidth / 230 || 2.6));
    const st = new lab.Stage(concept, cv, { w: 230, h: 34, zoom, night: night() });
    cv.style.width = '100%';
    cv.style.height = 'auto';
    stages.push(st);
    cv.addEventListener('pointerdown', e => {
      const r = cv.getBoundingClientRect(), x = (e.clientX - r.left) / r.width;
      let best = 0;
      lab.SLICES.forEach((s, i) => { if (Math.abs(s.x - x) < Math.abs(lab.SLICES[best].x - x)) best = i; });
      const t = performance.now();
      for (const st of stages) st.hit(lab.hitFor(best, t, 0.9, reversed));
      start();
    });
  }

  const pause = root.querySelector('[data-pond-pause]');
  const label = () => {
    pause.setAttribute('aria-pressed', String(!beatOn));
    pause.querySelector('span').textContent = beatOn ? '❚❚' : '▶';
    pause.querySelector('b').textContent = beatOn ? pause.dataset.pause : pause.dataset.resume;
  };
  pause.addEventListener('click', () => {
    beatOn = !beatOn;
    beatStart = beatNext = performance.now() + 30;
    label();
    start();
  });
  label();
  const rev = root.querySelector('[data-pond-rev]');
  rev.addEventListener('click', () => { reversed = !reversed; rev.setAttribute('aria-pressed', String(reversed)); });

  new MutationObserver(() => { for (const st of stages) st.setNight(night()); start(); })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // draw only while the board is on screen and the tab is visible
  function tick() {
    if (!seen || document.hidden) { running = false; return; }
    const t = performance.now();
    if (beatOn) {
      while (beatNext <= t) {
        const step = Math.round((beatNext - beatStart) / lab.STEP_MS) % 16;
        for (const [s, slice, v] of lab.BEAT) if (s === step) for (const st of stages) st.hit(lab.hitFor(slice, beatNext, v, reversed));
        beatNext += lab.STEP_MS;
      }
    }
    let moving = beatOn;
    for (const st of stages) if (st.moving || beatOn) { st.draw(t); moving = moving || st.moving; }
    if (moving) requestAnimationFrame(tick); else running = false;
  }
  function start() {
    if (running || !seen || document.hidden) return;
    running = true;
    if (beatOn) beatStart = beatNext = performance.now() + 30;
    requestAnimationFrame(tick);
  }
  new IntersectionObserver(entries => { seen = entries.some(e => e.isIntersecting); start(); }).observe(root);
  document.addEventListener('visibilitychange', start);
  for (const st of stages) st.draw(performance.now());
});
