/* Gallery page: (1) a lead rope with polaroids pegged on it — a vanilla port of the 21st.dev "Hanging Polaroid Image
   Carousel" (@kedhareswer): drag the rope and the prints slide along it, swinging on their pegs with your speed and
   settling with a little overshoot; arrows, keyboard and autoplay; (2) category tabs over a photo wall; (3) a lightbox
   with swipe, arrows and Esc. Data: assets/gallery/gallery.json (built by _src/gallery_build.py from the class photos). */
(function () {
  var page = document.querySelector('[data-gallery]');
  if (!page) return;
  var BASE = page.getAttribute('data-base') || '';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  fetch(BASE + 'assets/gallery/gallery.json').then(function (r) { return r.json(); }).then(function (G) {
    rope(G.rope); wall(G.cats);
  });

  /* ---------------------------------------------------------------- the rope */
  function rope(slides) {
    var root = page.querySelector('[data-rope]'); if (!root || !slides || !slides.length) return;
    var n = slides.length, svg = root.querySelector('.rp-line path'), cards = [], cap = root.querySelector('.rp-cap'), count = root.querySelector('.rp-count');
    slides.forEach(function (s, i) {
      var c = el('div', 'rp-card'); c.setAttribute('data-i', i);
      c.innerHTML = '<div class="rp-print"><div class="rp-shot"><img src="' + BASE + s.thumb + '" alt="' + (s.alt || '') + '" draggable="false" loading="' + (i < 4 ? 'eager' : 'lazy') + '"></div><div class="rp-note">' + s.title + '</div></div><div class="rp-peg"></div>';
      root.querySelector('.rp-cards').appendChild(c); cards.push(c);
    });
    var W = 0, H = 0, cw = 260, spacing = 280, S = { off: 0, vel: 0, target: 0, a: [], w: [] }, active = -1, drag = null, lastTouch = 0, raf = 0, prev = performance.now(), visible = true;
    function size() { var r = root.getBoundingClientRect(); W = r.width; H = r.height; cw = Math.round(Math.max(150, Math.min(W < 700 ? 300 : 270, W * (W < 700 ? 0.62 : 0.42), H * 0.5))); spacing = cw * 1.08; root.style.setProperty('--rp-cw', cw + 'px'); S.target = Math.max(0, active) * spacing; S.off = S.target; }
    function setActive(i) {
      if (i === active) return; active = i;
      cards.forEach(function (c, j) { c.setAttribute('data-on', j === i ? '1' : '0'); });
      var s = slides[i]; cap.innerHTML = '<span class="rp-title">' + s.title + '</span><span class="rp-sub">' + (s.caption || '') + '</span>';
      count.innerHTML = '<b>' + ('0' + (i + 1)).slice(-2) + '</b> / ' + ('0' + n).slice(-2);
    }
    function goTo(i) { S.target = clamp(i, 0, n - 1) * spacing; }
    function frame(now) {
      raf = 0; if (!visible) return;
      var dt = Math.min(0.033, (now - prev) / 1000); prev = now;
      var y0 = Math.max(46, H * 0.16), sag = Math.min(54, W * 0.05), lineVel;
      if (drag && drag.moved) lineVel = drag.v * 1000;
      else { var before = S.off, k = 70, c = 2 * Math.sqrt(k); S.vel += (k * (S.target - S.off) - c * S.vel) * dt; S.off += S.vel * dt; lineVel = -(S.off - before) / Math.max(dt, 1e-3); }
      var g = reduce ? 0 : 1, near = clamp(Math.round(S.off / spacing), 0, n - 1);
      for (var i = 0; i < n; i++) {
        var c = cards[i], x = W / 2 + i * spacing - S.off;
        if (x < -cw * 1.5 || x > W + cw * 1.5) { c.style.visibility = 'hidden'; continue; }
        c.style.visibility = 'visible';
        var a = S.a[i] || 0, av = S.w[i] || 0;
        av += (-38 * a - 4.2 * av + lineVel * 0.0034 * g) * dt; a = clamp(a + av * dt, -0.6, 0.6);
        if (g) a += Math.sin(now / 1300 + i * 1.7) * 0.0009;
        S.a[i] = a; S.w[i] = av;
        var t = clamp(x / W, 0, 1), y = y0 + 4 * sag * t * (1 - t) - 6;
        c.style.transform = 'translate(' + (x - cw / 2).toFixed(1) + 'px,' + y.toFixed(1) + 'px) rotate(' + a.toFixed(4) + 'rad)';
        c.style.zIndex = String(i === near ? n + 1 : n - Math.abs(i - near));
      }
      svg.setAttribute('d', 'M0 ' + y0 + ' Q' + W / 2 + ' ' + (y0 + 2 * sag) + ' ' + W + ' ' + y0);
      setActive(near);
      raf = requestAnimationFrame(frame);
    }
    function kick() { if (!raf) { prev = performance.now(); raf = requestAnimationFrame(frame); } }
    new ResizeObserver(function () { size(); kick(); }).observe(root);
    new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) kick(); }).observe(root);
    size(); setActive(0); kick();
    root.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.rp-bar')) return;
      lastTouch = performance.now(); drag = { x: e.clientX, off: S.off, lx: e.clientX, lt: e.timeStamp, v: 0, moved: false };
    });
    root.addEventListener('pointermove', function (e) {
      var d = drag; if (!d) return; var dx = e.clientX - d.x;
      if (!d.moved && Math.abs(dx) > 5) { d.moved = true; root.setAttribute('data-drag', '1'); root.setPointerCapture(e.pointerId); }
      if (!d.moved) return;
      var dtt = Math.max(1, e.timeStamp - d.lt); d.v = 0.7 * ((e.clientX - d.lx) / dtt) + 0.3 * d.v; d.lx = e.clientX; d.lt = e.timeStamp;
      var max = (n - 1) * spacing, off = d.off - dx; if (off < 0) off *= 0.35; if (off > max) off = max + (off - max) * 0.35; S.off = off;
    });
    function up(e) {
      var d = drag; drag = null; lastTouch = performance.now(); if (!d) return;
      if (d.moved) { root.removeAttribute('data-drag'); S.vel = -d.v * 1000; goTo(Math.round((S.off - d.v * 180) / spacing)); return; }
      var card = e.target.closest('[data-i]'); if (!card) return;
      var i = +card.getAttribute('data-i');
      if (i === active) openCat(slides[i].cat); else goTo(i);     // tap the front print: jump to its photos
    }
    root.addEventListener('pointerup', up); root.addEventListener('pointercancel', up);
    root.querySelector('.rp-prev').addEventListener('click', function () { lastTouch = performance.now(); goTo(active - 1); });
    root.querySelector('.rp-next').addEventListener('click', function () { lastTouch = performance.now(); goTo(active + 1); });
    root.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') goTo(active + 1); else if (e.key === 'ArrowLeft') goTo(active - 1); else return; e.preventDefault(); });
    if (!reduce) setInterval(function () { if (document.hidden || drag || performance.now() - lastTouch < 6000) return; goTo(active >= n - 1 ? 0 : active + 1); }, 4500);
  }

  /* ----------------------------------------------------- tabs + photo wall */
  var CATS = null, current = null;
  function openCat(key) {
    var b = page.querySelector('.gtab[data-cat="' + key + '"]'); if (b) b.click();
    var w = page.querySelector('[data-wall-head]'); if (w) w.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }
  function wall(cats) {
    CATS = cats; var tabs = page.querySelector('.gtabs'), grid = page.querySelector('.gwall'), lede = page.querySelector('[data-cat-lede]');
    cats.forEach(function (c, i) {
      var b = el('button', 'gtab', c.title + ' <span>' + c.photos.length + '</span>'); b.type = 'button'; b.setAttribute('data-cat', c.key); b.setAttribute('role', 'tab');
      b.addEventListener('click', function () { show(c); }); tabs.appendChild(b);
    });
    var want = (location.hash || '').slice(1), first = cats.filter(function (c) { return c.key === want; })[0] || cats[0];
    show(first, true);
    function show(c, initial) {
      current = c;
      tabs.querySelectorAll('.gtab').forEach(function (b) { var on = b.getAttribute('data-cat') === c.key; b.setAttribute('aria-selected', on); b.classList.toggle('on', on); });
      lede.textContent = c.lede;
      grid.innerHTML = '';
      c.photos.forEach(function (p, i) {
        var a = el('button', 'gph'); a.type = 'button'; a.style.setProperty('--ar', (p.w / p.h).toFixed(3));
        a.innerHTML = '<img src="' + BASE + p.thumb + '" alt="' + (p.alt || '') + '" loading="lazy" decoding="async" width="' + p.w + '" height="' + p.h + '">';
        a.addEventListener('click', function () { lightbox(c.photos, i); }); grid.appendChild(a);
      });
      if (!initial && history.replaceState) history.replaceState(null, '', '#' + c.key);
    }
  }

  /* --------------------------------------------------------------- lightbox */
  var lb = null;
  function lightbox(list, start) {
    if (!lb) {
      lb = el('div', 'glb'); lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Photo viewer');
      lb.innerHTML = '<button class="glb-x" type="button" aria-label="Close">×</button><button class="glb-p" type="button" aria-label="Previous">‹</button>' +
        '<figure><img alt=""><figcaption></figcaption></figure><button class="glb-n" type="button" aria-label="Next">›</button>';
      document.body.appendChild(lb);
    }
    var img = lb.querySelector('img'), capn = lb.querySelector('figcaption'), i = start, sx = null;
    function draw() { var p = list[i]; img.src = BASE + p.src; img.alt = p.alt || ''; capn.textContent = (i + 1) + ' / ' + list.length + (p.alt ? ' · ' + p.alt : ''); var nx = list[(i + 1) % list.length]; (new Image()).src = BASE + nx.src; }
    function go(d) { i = (i + d + list.length) % list.length; draw(); }
    function close() { lb.classList.remove('on'); document.documentElement.style.overflow = ''; removeEventListener('keydown', key); }
    function key(e) { if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') go(1); else if (e.key === 'ArrowLeft') go(-1); }
    lb.querySelector('.glb-x').onclick = close; lb.querySelector('.glb-p').onclick = function () { go(-1); }; lb.querySelector('.glb-n').onclick = function () { go(1); };
    lb.onclick = function (e) { if (e.target === lb) close(); };
    lb.ontouchstart = function (e) { sx = e.touches[0].clientX; };
    lb.ontouchend = function (e) { if (sx == null) return; var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1); sx = null; };
    addEventListener('keydown', key);
    draw(); lb.classList.add('on'); document.documentElement.style.overflow = 'hidden'; lb.querySelector('.glb-x').focus({ preventScroll: true });
  }
})();
