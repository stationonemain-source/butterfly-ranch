/* Torn-poster footer: a vanilla port of the "Pushpin Tear Footer" React component (21st.dev, @kedhareswer), dressed for
   Butterfly Ranch. A magenta sheet carries the footer's links; its bottom is ripped away from a pushpin and the ranch's
   name is printed on the paper underneath. When it scrolls in, the chrome assembles, the pin drops and the sheet rips from
   the pin outwards (jagged ridge, white fibre rim, curled flaps). Click the pin to tear a new edge. No dependencies. */
(function () {
  var root = document.querySelector('.tpf');
  if (!root) return;

  // ---- the tear (same maths as the component) -------------------------------------------------------------------------
  var RIDGE_N = 84, START = 1.06, FLAPS = 6;
  function clamp01(v) { return isFinite(v) ? (v < 0 ? 0 : v > 1 ? 1 : v) : 0; }
  function rng(seed) {
    var a = (isFinite(seed) ? Math.floor(seed) : 0) >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0; var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var XS = (function () {
    var r = rng(911), out = [];
    for (var i = 0; i < RIDGE_N; i++) {
      var u = i / (RIDGE_N - 1), j = i > 0 && i < RIDGE_N - 1 ? (r() - 0.5) * (0.8 / RIDGE_N) : 0;
      out.push(-0.02 + u * 1.04 + j);
    }
    return out;
  })();
  // the lowest the ridge may climb at x, so it never crosses the sheet's content
  function ridgeFloor(x) { var d = Math.abs(x - 0.5); return d < 0.13 ? 0.39 : d < 0.25 ? 0.43 : 0.5; }
  function makeTear(seed) {
    var r = rng(seed), ph = [r() * 6.283, r() * 6.283, r() * 6.283], ys = [], rim = [], lag = [];
    for (var i = 0; i < RIDGE_N; i++) {
      var x = XS[i], d = Math.min(1, Math.abs(x - 0.5) * 2);
      var base = 0.43 + 0.3 * Math.pow(d, 1.35);   // a mountain: lowest under the pin, falling away to both edges
      var wander = (0.022 * Math.sin(x * 7 + ph[0]) + 0.016 * Math.sin(x * 13 + ph[1]) + 0.01 * Math.sin(x * 29 + ph[2])) * (0.45 + 0.55 * d);
      var spike = r() < 0.16 ? 2.3 : 1, jag = (r() - 0.5) * 0.022 * spike;
      ys.push(Math.min(0.8, Math.max(ridgeFloor(x), base + wander + jag)));
      rim.push(1.2 + r() * 3.6);
      lag.push(Math.min(0.48, d * 0.4 + 0.04 + 0.03 * Math.sin(x * 23 + ph[1]) + r() * 0.012));   // rips from the pin outwards
    }
    var slots = [0.05, 0.19, 0.33, 0.67, 0.81, 0.95], up = r() < 0.5 ? [2, 4] : [1, 3];
    var flaps = slots.map(function (slot, k) {
      var x = slot + (r() - 0.5) * 0.05, span = 3 + Math.floor(r() * 5);
      var at = Math.max(0, Math.min(RIDGE_N - 1 - span, Math.round(x * (RIDGE_N - 1))));
      var dir = up.indexOf(k) >= 0 ? -1 : 1, outer = k === 0 || k === slots.length - 1;
      var len = dir < 0 ? 0.022 + r() * 0.022 : outer ? 0.085 + r() * 0.04 : 0.045 + r() * 0.05;
      return { at: at, span: span, len: len, skew: (r() - 0.5) * 1.1, dir: dir, jag: [r() - 0.5, r() - 0.5, r() - 0.5, r() - 0.5] };
    });
    return { ys: ys, rim: rim, lag: lag, flaps: flaps };
  }
  function easeTear(t) { var x = clamp01(t); if (x === 0 || x === 1) return x; var c = 0.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }
  function easeInOut(t) { var x = clamp01(t); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
  function introYs(tear, t) { return tear.ys.map(function (y, i) { return START + (y - START) * easeTear((t - tear.lag[i]) / 0.5); }); }
  function morphYs(from, to, t) { return to.ys.map(function (y, i) { var a = from[i] != null ? from[i] : y; return a + (y - a) * easeInOut((t - to.lag[i] * 0.6) / 0.6); }); }
  function flapOpen(tear, f, t) { return easeTear((t - tear.lag[f.at] - 0.18) / 0.32); }
  function flapPoly(ys, f, W, H, open) {
    var b = Math.min(ys.length - 1, f.at + f.span), top = [];
    for (var k = f.at; k <= b; k++) top.push([XS[k] * W, ys[k] * H]);
    var A = top[0], B = top[top.length - 1], mx = (A[0] + B[0]) / 2, my = (A[1] + B[1]) / 2;
    var L = f.len * H * Math.max(0, open), tip = [mx + f.skew * L, my + f.dir * L];
    function side(P, Q, j0, j1) {
      var dx = Q[0] - P[0], dy = Q[1] - P[1], len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
      return [[P[0] + dx / 3 + nx * j0 * 0.22 * L, P[1] + dy / 3 + ny * j0 * 0.22 * L],
              [P[0] + dx * 2 / 3 + nx * j1 * 0.22 * L, P[1] + dy * 2 / 3 + ny * j1 * 0.22 * L]];
    }
    return top.concat(side(B, tip, f.jag[0], f.jag[1]), [tip], side(tip, A, f.jag[2], f.jag[3]));
  }
  function n1(v) { return Math.round(v * 10) / 10; }
  function polyD(p) { return p.length ? 'M' + p.map(function (q) { return n1(q[0]) + ' ' + n1(q[1]); }).join('L') + 'Z' : ''; }
  function sheetD(ys, W, H, off) {
    var d = 'M-20 -20L' + (W + 20) + ' -20';
    for (var i = ys.length - 1; i >= 0; i--) d += 'L' + n1(XS[i] * W) + ' ' + n1(ys[i] * H - (off ? off[i] : 0));
    return d + 'Z';
  }

  // ---- elements ---------------------------------------------------------------------------------------------------------
  var svg = root.querySelector('.tpf-stage'), sheetEl = root.querySelector('#tpf-s'), rimEl = root.querySelector('.tpf-rim');
  var flapEls = [], gradEls = [];
  for (var k = 0; k < FLAPS * 2; k++) { flapEls.push(root.querySelector('#tpf-f' + k)); gradEls.push(root.querySelector('#tpf-fg' + k)); }
  var pin = root.querySelector('.tpf-pin');
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var timers = [];
  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }

  var S = { W: 0, H: 0, seed: +root.dataset.seed || 7, tear: null, prev: null, from: [], ys: [], mode: 'wait', t0: 0, dur: 1, raf: 0,
            px: -1e4, py: -1e4, lift: [0, 0, 0, 0, 0, 0], busy: false, stage: 0 };
  S.tear = makeTear(S.seed);

  // ---- drawing ----------------------------------------------------------------------------------------------------------
  function frame(now) {
    S.raf = 0;
    var W = S.W, H = S.H, tear = S.tear, busy = false, ys, i;
    if (!W || !H) return;
    var open = [1, 1, 1, 1, 1, 1], openOld = [0, 0, 0, 0, 0, 0];
    if (S.mode === 'wait') { ys = tear.ys.map(function () { return START; }); open = [0, 0, 0, 0, 0, 0]; }
    else if (S.mode === 'intro') {
      var p = (now - S.t0) / S.dur;
      ys = introYs(tear, Math.min(1, p));
      tear.flaps.forEach(function (f, k) { open[k] = flapOpen(tear, f, Math.min(1, p)); });
      if (p >= 1) S.mode = 'rest'; else busy = true;
    } else if (S.mode === 'morph') {
      var q = (now - S.t0) / S.dur;
      ys = morphYs(S.from, tear, Math.min(1, q));
      for (i = 0; i < FLAPS; i++) { open[i] = easeTear((q - 0.5) / 0.5); openOld[i] = 1 - easeInOut(q / 0.35); }
      if (q >= 1) S.mode = 'rest'; else busy = true;
    } else ys = tear.ys;
    S.ys = ys;
    // flaps lift towards a nearby pointer
    tear.flaps.forEach(function (f, k) {
      var b = Math.min(ys.length - 1, f.at + f.span);
      var mx = (XS[f.at] + XS[b]) / 2 * W, my = (ys[f.at] + ys[b]) / 2 * H;
      var target = still ? 0 : clamp01(1 - Math.hypot(S.px - mx, S.py - my) / (0.2 * Math.max(W, 520)));
      S.lift[k] += (target - S.lift[k]) * 0.14;
      if (Math.abs(target - S.lift[k]) > 0.003) busy = true;
      open[k] *= 1 + 0.32 * S.lift[k];
    });
    // phones: the sheet holds more (stacked links), so the tear sits lower; full shift at rest, none at the off-screen start
    if (W <= 620) ys = ys.map(function (y) { return y + 0.1 * clamp01((START - y) / (START - 0.8)); });
    sheetEl.setAttribute('d', sheetD(ys, W, H, tear.rim));
    rimEl.setAttribute('d', sheetD(ys, W, H));
    function draw(k, f, o) {
      var el = flapEls[k], g = gradEls[k];
      if (!el || !g) return;
      if (!f || o < 0.01) { el.setAttribute('d', ''); return; }
      var pts = flapPoly(ys, f, W, H, o), b = Math.min(ys.length - 1, f.at + f.span), tip = pts[f.span + 3];
      el.setAttribute('d', polyD(pts));
      g.setAttribute('x1', (XS[f.at] + XS[b]) / 2 * W); g.setAttribute('y1', (ys[f.at] + ys[b]) / 2 * H);
      g.setAttribute('x2', tip[0]); g.setAttribute('y2', tip[1]);
    }
    for (i = 0; i < FLAPS; i++) { draw(i, tear.flaps[i], open[i]); draw(FLAPS + i, S.prev && S.prev.flaps[i], openOld[i]); }
    if (busy) S.raf = requestAnimationFrame(frame);
  }
  function kick() { if (!S.raf) S.raf = requestAnimationFrame(frame); }

  function size() {
    S.W = root.clientWidth; S.H = root.clientHeight;
    svg.setAttribute('width', S.W); svg.setAttribute('height', S.H); svg.setAttribute('viewBox', '0 0 ' + S.W + ' ' + S.H);
    kick();
  }
  if (window.ResizeObserver) new ResizeObserver(size).observe(root); else addEventListener('resize', size);
  size();

  // paper grain, made once on a canvas
  (function () {
    var c = document.createElement('canvas'); c.width = c.height = 160;
    var g = c.getContext('2d'); if (!g) return;
    var img = g.createImageData(160, 160), r = rng(42);
    for (var i = 0; i < img.data.length; i += 4) {
      var v = r() < 0.5 ? 0 : 255;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = Math.floor(r() * 46);
    }
    g.putImageData(img, 0, 0);
    var im = root.querySelector('#tpf-grain-img'); if (im) im.setAttribute('href', c.toDataURL());
  })();

  // ---- the opening: chrome, pin, rip ------------------------------------------------------------------------------------
  function setStage(n) { S.stage = n; root.classList.toggle('s1', n >= 1); root.classList.toggle('s2', n >= 2); root.classList.toggle('s3', n >= 3); }
  function open() {
    if (S.stage > 0) return;
    if (still) { setStage(3); S.mode = 'rest'; kick(); return; }
    setStage(1);
    later(function () { setStage(2); }, 640);
    later(function () { root.classList.add('is-hit'); setStage(3); S.mode = 'intro'; S.t0 = performance.now(); S.dur = 1550; kick(); }, 1140);
    later(function () { root.classList.remove('is-hit'); }, 1480);
  }
  if (window.IntersectionObserver) {
    var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { open(); io.disconnect(); } }, { threshold: 0.22 });
    io.observe(root);
  } else open();

  // ---- actions ----------------------------------------------------------------------------------------------------------
  root.addEventListener('pointermove', function (e) {
    if (still) return;
    var r = root.getBoundingClientRect();
    S.px = e.clientX - r.left; S.py = e.clientY - r.top;
    pin.style.setProperty('--tilt', Math.max(-9, Math.min(9, (S.px / r.width - 0.5) * 18)).toFixed(2) + 'deg');
    kick();
  });
  root.addEventListener('pointerleave', function () { S.px = S.py = -1e4; pin.style.setProperty('--tilt', '0deg'); kick(); });

  pin.addEventListener('click', function () {
    if (S.busy || S.stage < 3) return;
    var next = S.seed + 1;
    function swap() { S.seed = next; S.prev = S.tear; S.from = S.ys.length ? S.ys : S.tear.ys; S.tear = makeTear(next); }
    if (still) { swap(); S.prev = null; S.mode = 'rest'; kick(); return; }
    S.busy = true; pin.dataset.pin = 'lift';
    later(function () { swap(); S.mode = 'morph'; S.t0 = performance.now(); S.dur = 1150; kick(); }, 300);
    later(function () { pin.dataset.pin = 'stab'; }, 1280);
    later(function () { pin.dataset.pin = 'idle'; S.busy = false; }, 1720);
  });

  var toast = root.querySelector('.tpf-toast');
  function flash(msg) { toast.textContent = msg; toast.classList.add('on'); later(function () { toast.classList.remove('on'); }, 1600); }
  var copy = root.querySelector('.tpf-mail');
  if (copy) copy.addEventListener('click', function () {
    var v = copy.dataset.copy;
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(function () { flash('number copied'); }, function () { flash(v); });
    else flash(v);
  });
  var up = root.querySelector('.tpf-up');
  if (up) up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: still ? 'auto' : 'smooth' }); });

  // newsletter: the pill flips to its sent state; give.js posts the address and writes the result into .tpf-sent
  var form = root.querySelector('.tpf-news');
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var input = form.querySelector('input'), v = input.value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { flash('check that email'); return; }
    form.querySelector('.tpf-pill').dataset.sent = 'true';
    input.disabled = true; form.querySelector('.tpf-knob').disabled = true;
  });

  // live Norman time, blinking colon
  var clock = root.querySelector('.tpf-clock');
  if (clock) {
    var f;
    try { f = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: clock.dataset.zone }); }
    catch (x) { f = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }); }
    var hh = clock.querySelector('.h'), mm = clock.querySelector('.m');
    function tick() { var t = f.format(new Date()).split(':'); hh.textContent = t[0]; mm.textContent = t[1]; }
    tick(); setInterval(tick, 10000);
  }
})();
