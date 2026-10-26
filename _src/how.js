/* "How it works" switch (2026-10-25). A showcase for Braxton and the OU class: with the switch on, every feature a
   Station product runs gets a thin magenta outline and a small note naming the product and what it does ON THE LIVE
   SITE. Nothing on this preview is connected; the notes never say otherwise. Copy lives in _src/data.json ("how");
   build.py writes it into assets/how.js in place of the HOW_DATA marker. Off by default; the choice is a view
   preference, so it may sit in localStorage. */
(function () {
  var DATA = /*HOW_DATA*/null;
  var btn = document.querySelector('.how-btn'), root = document.documentElement, KEY = 'br-how', built = false;
  if (!btn || !DATA) return;
  btn.hidden = false;

  function el(tag, cls, text) { var d = document.createElement(tag); if (cls) d.className = cls; if (text != null) d.textContent = text; return d; }
  function note(key, extra) {
    var rows = DATA.notes[key]; if (!rows) return null;
    var n = el('div', 'how-note' + (extra ? ' ' + extra : ''));
    n.setAttribute('role', 'note');
    n.setAttribute('aria-label', 'How it works: ' + rows.map(function (r) { return r[0]; }).join(', '));
    n.appendChild(el('p', 'how-eye', 'On the live site:'));
    var list = el('div', 'how-rows');
    rows.forEach(function (r) { var row = el('div', 'how-row'); row.appendChild(el('b', 'how-p', r[0])); row.appendChild(el('p', null, r[1])); list.appendChild(row); });
    n.appendChild(list);
    return n;
  }
  function place(target, n, at) {
    if (at === 'before') target.parentNode.insertBefore(n, target);
    else if (at === 'start') target.insertBefore(n, target.firstChild);
    else if (at === 'end') target.appendChild(n);
    else target.parentNode.insertBefore(n, target.nextSibling);   // 'after'
  }
  function build() {
    built = true;
    // the legend: under the film on home, at the top of the page everywhere else
    var lg = el('div', 'how-legend'), w = el('div', 'wrap');
    w.appendChild(el('b', 'how-p', 'How it works')); w.appendChild(el('p', null, DATA.legend)); lg.appendChild(w);
    var film = document.querySelector('.home .film'), main = document.getElementById('main');
    if (film) film.parentNode.insertBefore(lg, film.nextSibling); else if (main) main.insertBefore(lg, main.firstChild);

    document.querySelectorAll('[data-how]').forEach(function (f) {
      var n = note(f.getAttribute('data-how')); if (n) place(f, n, f.getAttribute('data-how-at') || 'after');
    });
    (DATA.spots || []).forEach(function (s) {
      var t = document.querySelector(s.sel); if (!t) return;
      var n = note(s.note); if (!n) return;
      t.setAttribute('data-how-mark', '');
      if (s.mark) t.querySelectorAll(s.mark).forEach(function (m) { m.setAttribute('data-how-mark', ''); });
      if (s.at === 'fly') {
        // the chat bubble is fixed to the corner, so its note can't sit in the page without covering it. A small tab
        // floats above the bubble (and hides with it); the note opens from the tab, so nothing is covered by default.
        var fly = el('div', 'how-fly'), id = 'how-' + s.note;
        var tab = el('button', 'how-tab', DATA.notes[s.note].map(function (r) { return r[0]; }).join(', ') + ' · how the chat works');
        tab.type = 'button'; tab.setAttribute('aria-expanded', 'false'); tab.setAttribute('aria-controls', id);
        var x = el('button', 'how-x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'Close this note');
        n.id = id; n.hidden = true; n.insertBefore(x, n.firstChild);
        function show(o) { n.hidden = !o; tab.hidden = o; tab.setAttribute('aria-expanded', o ? 'true' : 'false'); (o ? x : tab).focus({ preventScroll: true }); }
        tab.addEventListener('click', function () { show(true); });
        x.addEventListener('click', function () { show(false); });
        fly.appendChild(tab); fly.appendChild(n);
        t.parentNode.insertBefore(fly, t.nextSibling);
      } else if (s.at === 'before') {
        var wrap = el('div', 'wrap how-out'); wrap.appendChild(n); t.parentNode.insertBefore(wrap, t);
      } else place(t, n, s.at);
    });
  }
  function set(on, save) {
    if (on && !built) build();
    root.classList.toggle('how-on', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (save) { try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {} }
  }
  btn.addEventListener('click', function () { set(!root.classList.contains('how-on'), true); });
  var saved = false;
  try { saved = localStorage.getItem(KEY) === '1'; } catch (e) {}
  set(saved, false);
})();
